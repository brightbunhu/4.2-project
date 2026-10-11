"""Export structured Option B fold metrics and check confusion arithmetic.

This reads the repository's already-recorded fold metric table. It does not
fit models or turn full-table/in-sample predictions into held-out predictions.
"""
from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parents[1]
METRICS = ROOT / "outputs/option_b/results/option_b_model_metrics.csv"
WINDOWS = ROOT / "outputs/option_b/results/validation_audit.csv"


def read_csv(path: Path):
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def div(a: float, b: float) -> float:
    return a / b if b else 0.0


def main() -> None:
    metrics = read_csv(METRICS)
    available = read_csv(OUT / "scripts/available_method_metrics.csv")
    windows = {r["fold"]: r for r in read_csv(WINDOWS)}
    records = []
    cms = defaultdict(list)
    checked = []
    numeric = ["accuracy", "balanced_accuracy", "macro_f1", "stress_f1", "precision", "recall",
               "specificity", "roc_auc", "pr_auc", "brier_score"]
    for src in metrics:
        fold, model = src["fold"], src["model"]
        w = windows[fold]
        tn, fp, fn, tp = (int(src[k]) for k in ("true_negative", "false_positive", "false_negative", "true_positive"))
        n = tn + fp + fn + tp
        pos = int(w["test_pos_class"])
        prevalence = pos / int(w["test_rows"])
        p0, r0 = div(tn, tn + fn), div(tn, tn + fp)
        f10 = div(2 * p0 * r0, p0 + r0)
        p1, r1 = div(tp, tp + fp), div(tp, tp + fn)
        f11 = div(2 * p1 * r1, p1 + r1)
        derived = {
            "accuracy": div(tn + tp, n),
            "balanced_accuracy": (r0 + r1) / 2,
            "macro_f1": (f10 + f11) / 2,
            "stress_precision": p1,
            "stress_recall": r1,
            "stress_f1": f11,
            "negative_precision": p0,
            "negative_recall": r0,
            "negative_f1": f10,
            "specificity": r0,
        }
        for name in ("accuracy", "balanced_accuracy", "macro_f1", "stress_f1", "precision", "recall", "specificity"):
            src_name = "stress_precision" if name == "precision" else ("stress_recall" if name == "recall" else name)
            ok = abs(float(src[name]) - derived[src_name]) <= 0.00016
            checked.append({"fold": fold, "model": model, "metric": name, "source_value": src[name],
                            "recomputed_from_confusion_matrix": f"{derived[src_name]:.6f}",
                            "status": "PASS" if ok else "FAIL"})
        rec = {
            "fold": fold, "model": model,
            "train_months": w["train_months"], "test_months": w["test_months"],
            "n_test": n, "positive_count": pos, "prevalence": f"{prevalence:.6f}",
            "accuracy": src["accuracy"], "balanced_accuracy": src["balanced_accuracy"],
            "macro_f1": src["macro_f1"], "negative_precision": f"{p0:.4f}",
            "negative_recall": f"{r0:.4f}", "negative_f1": f"{f10:.4f}",
            "stress_precision": src["precision"], "stress_recall": src["recall"],
            "stress_f1": src["stress_f1"], "specificity": src["specificity"],
            "TN": tn, "FP": fp, "FN": fn, "TP": tp,
            "roc_auc": src["roc_auc"], "pr_auc_average_precision": src["pr_auc"],
            "brier_score": src["brier_score"],
            "probability_source": "existing structured Option B fold metric export; fold score vectors are not saved",
        }
        records.append(rec)
        cms[fold].append({"model": model, "TN": tn, "FP": fp, "FN": fn, "TP": tp, "n_test": n,
                          "confusion_total": tn + fp + fn + tp,
                          "total_matches_test_rows": int(n == int(w["test_rows"]))})

    # The saved pipeline did not export persistence metrics. Add the independently
    # reconstructed fold-only comparator; cross-check reconstructed Dummy values
    # against the source table instead of duplicating them.
    src_dummy = {(r["fold"], r["model"]): r for r in metrics if r["model"] == "Dummy"}
    for src in available:
        fold, model = src["fold"], src["method"]
        if model == "Dummy":
            old = src_dummy[(fold, "Dummy")]
            for key in ("accuracy", "balanced_accuracy", "macro_f1", "stress_f1", "roc_auc", "pr_auc_average_precision", "brier_score"):
                old_key = "pr_auc" if key == "pr_auc_average_precision" else key
                checked.append({"fold": fold, "model": "Dummy", "metric": f"independent_prediction_crosscheck:{key}",
                                "source_value": old[old_key], "recomputed_from_confusion_matrix": f"{float(src[key]):.6f}",
                                "status": "PASS" if abs(float(old[old_key]) - float(src[key])) <= 0.00016 else "FAIL"})
            continue
        tn, fp, fn, tp = (int(src[k]) for k in ("TN", "FP", "FN", "TP"))
        n = int(src["n_test"])
        w = windows[fold]
        rec = {
            "fold": fold, "model": model,
            "train_months": src["train_months"], "test_months": src["test_months"],
            "n_test": n, "positive_count": int(src["positive_count"]), "prevalence": f"{float(src['prevalence']):.6f}",
            "accuracy": f"{float(src['accuracy']):.4f}", "balanced_accuracy": f"{float(src['balanced_accuracy']):.4f}",
            "macro_f1": f"{float(src['macro_f1']):.4f}", "negative_precision": f"{float(src['negative_precision']):.4f}",
            "negative_recall": f"{float(src['negative_recall']):.4f}", "negative_f1": f"{float(src['negative_f1']):.4f}",
            "stress_precision": f"{float(src['stress_precision']):.4f}", "stress_recall": f"{float(src['stress_recall']):.4f}",
            "stress_f1": f"{float(src['stress_f1']):.4f}", "specificity": f"{float(src['specificity']):.4f}",
            "TN": tn, "FP": fp, "FN": fn, "TP": tp,
            "roc_auc": src["roc_auc"], "pr_auc_average_precision": src["pr_auc_average_precision"],
            "brier_score": src["brier_score"],
            "probability_source": src["probability_source"],
        }
        records.append(rec)
        cms[fold].append({"model": model, "TN": tn, "FP": fp, "FN": fn, "TP": tp, "n_test": n,
                          "confusion_total": tn + fp + fn + tp,
                          "total_matches_test_rows": int(n == int(w["test_rows"]))})

    fields = list(records[0])
    with (OUT / "metrics_by_fold.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(records)

    summary_fields = ["model", "fold_count", "fold_aggregation", "n_test_rows_sum", "mean_test_rows",
                      "mean_positive_count", "mean_prevalence", "mean_accuracy", "mean_balanced_accuracy",
                      "mean_macro_f1", "mean_negative_precision", "mean_negative_recall", "mean_negative_f1",
                      "mean_stress_precision", "mean_stress_recall", "mean_stress_f1", "mean_specificity",
                      "mean_TN", "mean_FP", "mean_FN", "mean_TP", "mean_roc_auc",
                      "mean_pr_auc_average_precision", "mean_brier_score"]
    summary = []
    for model in sorted({r["model"] for r in records}):
        rs = [r for r in records if r["model"] == model]
        out = {"model": model, "fold_count": len(rs), "fold_aggregation": "unweighted arithmetic mean of fold metrics; not pooled"}
        out["n_test_rows_sum"] = sum(int(r["n_test"]) for r in rs)
        out["mean_test_rows"] = f"{sum(int(r['n_test']) for r in rs) / len(rs):.4f}"
        mappings = {
            "positive_count": "positive_count", "prevalence": "prevalence", "accuracy": "accuracy",
            "balanced_accuracy": "balanced_accuracy", "macro_f1": "macro_f1",
            "negative_precision": "negative_precision", "negative_recall": "negative_recall", "negative_f1": "negative_f1",
            "stress_precision": "stress_precision", "stress_recall": "stress_recall", "stress_f1": "stress_f1",
            "specificity": "specificity", "TN": "TN", "FP": "FP", "FN": "FN", "TP": "TP",
            "roc_auc": "roc_auc", "pr_auc_average_precision": "pr_auc_average_precision", "brier_score": "brier_score",
        }
        for dst, src_key in mappings.items():
            vals = [float(r[src_key]) for r in rs if str(r[src_key]).strip() != ""]
            out[f"mean_{dst}"] = f"{sum(vals) / len(vals):.6f}" if vals else ""
        summary.append(out)
    with (OUT / "metrics_summary.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=summary_fields)
        w.writeheader(); w.writerows(summary)

    for fold, rows in cms.items():
        with (OUT / "confusion_matrices" / f"{fold.lower()}_confusion.csv").open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader(); w.writerows(rows)

    with (OUT / "scripts" / "metric_matrix_checks.json").open("w", encoding="utf-8") as f:
        json.dump({"matrix_recomputations": checked, "all_classification_metrics_match_rounded_source": all(r["status"] == "PASS" for r in checked)}, f, indent=2)
    print(json.dumps({"metrics_rows": len(records), "fold_rows": {k: windows[k]["test_rows"] for k in windows},
                      "summary": summary,
                      "all_confusion_totals_match_fold_rows": all(r["total_matches_test_rows"] for rows in cms.values() for r in rows),
                      "all_classification_metrics_recomputed_from_confusion": all(r["status"] == "PASS" for r in checked)}, indent=2))


if __name__ == "__main__":
    main()
