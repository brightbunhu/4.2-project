"""Execute package validation checks using Python standard library only."""
from __future__ import annotations

import csv
import json
import math
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parents[1]


def rows(path: Path):
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def parse_month(s: str) -> date:
    y, m, _ = map(int, s[:10].split("-"))
    return date(y, m, 1)


def auc_rank(ys: list[int], scores: list[float]) -> float:
    pos, neg = sum(ys), len(ys) - sum(ys)
    if not pos or not neg:
        return math.nan
    order = sorted(range(len(scores)), key=lambda i: scores[i])
    rank_sum = 0.0
    i = 0
    while i < len(order):
        j = i + 1
        while j < len(order) and scores[order[j]] == scores[order[i]]:
            j += 1
        avg_rank = ((i + 1) + j) / 2
        rank_sum += avg_rank * sum(ys[k] for k in order[i:j])
        i = j
    return (rank_sum - pos * (pos + 1) / 2) / (pos * neg)


def average_precision(ys: list[int], scores: list[float]) -> float:
    positives = sum(ys)
    if positives == 0:
        return math.nan
    order = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
    tp = fp = 0
    prev_recall = 0.0
    ap = 0.0
    i = 0
    while i < len(order):
        j = i + 1
        while j < len(order) and scores[order[j]] == scores[order[i]]:
            j += 1
        for k in order[i:j]:
            if ys[k]: tp += 1
            else: fp += 1
        recall = tp / positives
        precision = tp / (tp + fp)
        ap += (recall - prev_recall) * precision
        prev_recall = recall
        i = j
    return ap


def main() -> None:
    checks = []
    def add(name, status, details):
        checks.append((name, status, details))

    ledger = rows(OUT / "attrition_ledger.csv")
    summary = {r["stage_or_check"]: int(r["count"]) for r in rows(OUT / "attrition_summary.csv")}
    candidates = [(r["district_key"], r["commodity_name"], r["prediction_month"], r["currency_code"]) for r in ledger]
    duplicates = len(candidates) - len(set(candidates))
    null_key = sum(any(v is None for v in key) for key in candidates)
    blank_district = sum(not r["district_key"] for r in ledger)
    add("Candidate natural-key uniqueness", "PASS" if duplicates == 0 else "FAIL", f"8,289 candidates; duplicate keys={duplicates}")
    add("Candidate natural-key null/blank audit", "FAIL" if null_key or blank_district else "PASS", f"null-key rows={null_key}; blank district_key rows={blank_district}; blank strings are not counted as null by the original audit")

    bad_lag = [r for r in ledger if parse_month(r["target_month"]) != date(parse_month(r["prediction_month"]).year + (parse_month(r["prediction_month"]).month == 12), 1 if parse_month(r["prediction_month"]).month == 12 else parse_month(r["prediction_month"]).month + 1, 1)]
    add("Exact T-to-T+1 lag", "PASS" if not bad_lag else "FAIL", f"bad rows={len(bad_lag)} of {len(ledger)}")

    features = json.loads((ROOT / "outputs/option_b/data/option_b_feature_columns.json").read_text(encoding="utf-8-sig"))["features"]
    forbidden = [f for f in features if any(t in f.lower() for t in ("target", "next_month", "future"))]
    add("No target/future-named predictors", "PASS" if not forbidden else "FAIL", f"predictor count={len(features)}; forbidden names={forbidden}")

    stage_ok = (summary.get("raw_market_quotes") == 25554 and
                summary.get("aggregated_market_to_district_cells") == 13924 and
                summary.get("valid_spi_cells") == 11879 and
                summary.get("exact_t_plus_1_pairs") == 8289 and
                summary.get("final_model_rows_by_source_rule") == 6908 and
                summary.get("existing_final_table_rows") == 6908 and
                summary.get("exact_pair_positive_labels") == 1136 and
                summary.get("existing_final_table_positive_labels") == 904)
    add("Stage count reconciliation", "PASS" if stage_ok else "FAIL", json.dumps(summary, sort_keys=True))
    sens = rows(OUT / "target_threshold_sensitivity.csv")
    sens_values = {(r["population_stage"], r["spi_threshold"]): (int(r["positive_count"]), int(r["denominator"])) for r in sens}
    sens_ok = (sens_values.get(("exact_t_plus_1_pairs", "1.20")) == (1416, 8289) and
               sens_values.get(("exact_t_plus_1_pairs", "1.25")) == (1136, 8289) and
               sens_values.get(("exact_t_plus_1_pairs", "1.30")) == (963, 8289) and
               sens_values.get(("final_model_rows", "1.25")) == (904, 6908))
    add("Threshold prevalence denominators", "PASS" if sens_ok else "FAIL", "Recomputed labels kept separate for 8,289 exact-pair and 6,908 final-row stages; no retraining at alternate thresholds")

    windows = rows(OUT / "validation_windows.csv")
    order_ok = True
    for w in windows:
        tr_end = w["train_months"].split(" to ")[1]
        te_start = w["test_months"].split(" to ")[0]
        if tr_end >= te_start:
            order_ok = False
    add("Train/test temporal order", "PASS" if order_ok else "FAIL", f"checked {len(windows)} saved fold windows; strict train end < test start")

    cms = []
    for path in sorted((OUT / "confusion_matrices").glob("*.csv")):
        cms.extend(rows(path))
    cm_ok = all(int(r["confusion_total"]) == int(r["n_test"]) and int(r["total_matches_test_rows"]) == 1 for r in cms)
    add("Confusion totals equal held-out fold row counts", "PASS" if cm_ok else "FAIL", f"checked {len(cms)} fold/method matrices")

    metric_check = json.loads((OUT / "scripts/metric_matrix_checks.json").read_text(encoding="utf-8"))
    add("Classification metric recomputation", "PASS" if metric_check["all_classification_metrics_match_rounded_source"] else "FAIL", "Accuracy, balanced accuracy, macro-F1, per-class/stress scores recomputed from the confusion matrices; rounded source values matched")
    add("ROC/PR/Brier metric recomputation", "NOT RUN", "Original fold probability vectors were not saved; structured values retained as reported, not independently recomputed")

    # Check full-table predictions separately to establish the scope of existing plots.
    prod = rows(ROOT / "outputs/option_b/results/option_b_predictions.csv")
    plot_scope = "source code constructs ROC/PR/confusion plots from full-table final-model predictions, not outer-fold predictions"
    for model, pred_col, prob_col in (("LogisticRegression", "logreg_pred", "logreg_proba"), ("XGBoost", "xgb_pred", "xgb_proba")):
        ys = [int(r["target_next_month"]) for r in prod]
        ps = [int(r[pred_col]) for r in prod]
        scores = [float(r[prob_col]) for r in prod]
        tp = sum(y == 1 and p == 1 for y, p in zip(ys, ps))
        auc = auc_rank(ys, scores)
        ap = average_precision(ys, scores)
        claimed_tp, claimed_auc = ((682, 0.849) if model == "LogisticRegression" else (626, 0.942))
        matches = tp == claimed_tp and round(auc, 3) == claimed_auc
        add(f"{model} full-table prediction comparison to disputed figure", "PASS" if matches else "UNRESOLVED", f"saved full-table predictions: TP={tp}, ROC-AUC={auc:.6f}, AP={ap:.6f}; cited figure claim TP={claimed_tp}, AUC={claimed_auc:.3f}; {plot_scope}")

    predrows = rows(OUT / "fold_predictions.csv")
    persistence = [r for r in predrows if r["method"] == "Persistence"]
    persistence_f1 = {}
    for fold in sorted({r["fold"] for r in persistence}):
        rs = [r for r in persistence if r["fold"] == fold]
        ys = [int(r["y_true"]) for r in rs]
        ps = [int(r["y_pred"]) for r in rs]
        tn = sum(y == 0 and p == 0 for y, p in zip(ys, ps)); fp = sum(y == 0 and p == 1 for y, p in zip(ys, ps))
        fn = sum(y == 1 and p == 0 for y, p in zip(ys, ps)); tp = sum(y == 1 and p == 1 for y, p in zip(ys, ps))
        div = lambda a, b: a / b if b else 0.0
        p0, r0 = div(tn, tn + fn), div(tn, tn + fp)
        p1, r1 = div(tp, tp + fp), div(tp, tp + fn)
        f0, f1 = div(2*p0*r0, p0+r0), div(2*p1*r1, p1+r1)
        persistence_f1[fold] = (f0 + f1) / 2
    expected = [0.7259, 0.7319, 0.7594]
    actual = list(persistence_f1.values())
    p_ok = len(actual) == 3 and all(round(a, 4) == e for a, e in zip(actual, expected))
    add("Persistence fold prediction and metric reconstruction", "PASS" if p_ok else "FAIL", f"reconstructed macro-F1={','.join(f'{v:.4f}' for v in actual)}; unweighted mean={sum(actual)/len(actual):.4f}; predictor=price_stress_current at T")

    add("Logistic Regression/XGBoost test-fold predictions", "NOT RUN", "Their stored outputs are full-table predictions from final models fitted on all 6,908 rows; the source's fold prediction list was not persisted and sklearn/xgboost are missing from the available Python runtime")
    add("Fold-level ROC/PR figures from held-out scores", "NOT RUN", "No held-out per-row probability vectors are available; last/figures is intentionally empty")

    chirps_path = ROOT / "data/raw/chirps_v3_monthly_global.nc"
    chirps_bytes = chirps_path.read_bytes()
    if chirps_path.stat().st_size == 134 and b"version https://git-lfs.github.com/spec/v1" in chirps_bytes:
        add("Raw CHIRPS NetCDF availability", "UNRESOLVED", "Current file is a 134-byte LFS pointer (object SHA256 205f4f41011c94f47442f60e54c89af46bca8c23f865d310c53b6d2392282e60; expected size 353,488,971). It was 8,943,423,563 bytes with SHA256 26052751cc1077329798b2e79d34606473a242fcd03f4912acd8d07f91835bf3 when first inventoried; cause of replacement is unknown. The audit scripts did not write to it.")
    else:
        add("Raw CHIRPS NetCDF availability", "PASS", f"Current file size={chirps_path.stat().st_size}; file is not an LFS pointer")

    # Scope checks for known transformation fit boundaries.
    src = (ROOT / "src/run_option_b_pipeline.py").read_text(encoding="utf-8-sig")
    global_winsor = "df_agg.loc[valid_spi_mask, \"price_spi_raw\"].quantile([0.01, 0.99])" in src
    full_data_commodity = "df_opt_b[\"commodity_name\"].value_counts().head(10)" in src
    add("Quantile transformation fit scope", "FAIL" if global_winsor else "PASS", "SPI 1st/99th percentiles are calculated across all valid months before folds" if global_winsor else "No global fit detected")
    add("Commodity feature vocabulary fit scope", "FAIL" if full_data_commodity else "PASS", "top 10 commodity categories are chosen from the full exact-pair table before temporal folds" if full_data_commodity else "No full-data vocabulary selection detected")

    lines = ["Evidence package validation checks", "", "Status reflects checks executed by scripts in last/scripts.", ""]
    lines += [f"{s}: {name} — {details}" for name, s, details in checks]
    lines += ["", "Full authoritative model rerun: NOT PERFORMED. The bundled Python 3.12.14 runtime does not have scikit-learn; this is an environment limitation, and the documented source run wrote into project output directories. No project files were overwritten."]
    (OUT / "validation_checks.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
