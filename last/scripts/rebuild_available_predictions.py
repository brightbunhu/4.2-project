"""Regenerate fold-test predictions only for methods reproducible without sklearn.

DummyClassifier(strategy='most_frequent') is reconstructed from each saved
training window; persistence predicts the observed class at prediction month T.
Logistic Regression and XGBoost fold predictions are not stored by the source run.
"""
from __future__ import annotations

import csv
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "outputs/option_b/data/option_b_modelling_table.csv"


def month(v: str) -> date:
    y, m, _ = map(int, v[:10].split("-"))
    return date(y, m, 1)


def span(s: str) -> tuple[str, str]:
    a, b = s.split(" to ")
    return a, b


def metrics(ys: list[int], ps: list[int]) -> dict:
    tn = sum(y == 0 and p == 0 for y, p in zip(ys, ps))
    fp = sum(y == 0 and p == 1 for y, p in zip(ys, ps))
    fn = sum(y == 1 and p == 0 for y, p in zip(ys, ps))
    tp = sum(y == 1 and p == 1 for y, p in zip(ys, ps))
    div = lambda a, b: a / b if b else 0.0
    p0, r0 = div(tn, tn + fn), div(tn, tn + fp)
    p1, r1 = div(tp, tp + fp), div(tp, tp + fn)
    f0, f1 = div(2 * p0 * r0, p0 + r0), div(2 * p1 * r1, p1 + r1)
    n = len(ys)
    return {"n_test": n, "positive_count": sum(ys), "prevalence": sum(ys) / n,
            "accuracy": (tn + tp) / n, "balanced_accuracy": (r0 + r1) / 2,
            "macro_f1": (f0 + f1) / 2, "negative_precision": p0,
            "negative_recall": r0, "negative_f1": f0, "stress_precision": p1,
            "stress_recall": r1, "stress_f1": f1, "specificity": r0,
            "TN": tn, "FP": fp, "FN": fn, "TP": tp}


def main() -> None:
    with (ROOT / "outputs/option_b/results/validation_audit.csv").open(newline="", encoding="utf-8-sig") as f:
        windows = list(csv.DictReader(f))
    with TABLE.open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    predictions = []
    method_metrics = []
    for w in windows:
        fold = w["fold"]
        tr_lo, tr_hi = span(w["train_months"])
        te_lo, te_hi = span(w["test_months"])
        train = [r for r in rows if tr_lo <= r["prediction_month"][:7] <= tr_hi]
        test = [r for r in rows if te_lo <= r["prediction_month"][:7] <= te_hi]
        counts = Counter(int(float(r["target_next_month"])) for r in train)
        majority = min(counts, key=lambda c: (-counts[c], c))
        for method in ("Dummy", "Persistence"):
            ys, ps = [], []
            for r in test:
                y = int(float(r["target_next_month"]))
                if method == "Dummy":
                    pred, prob = majority, float(majority == 1)
                    run_id = "reconstructed_20261011_dummy_most_frequent"
                else:
                    # This is the observed current-month class at T; target_next_month is used only as y_true.
                    pred, prob = int(float(r["price_stress_current"])), ""
                    run_id = "reconstructed_20261011_persistence_observed_class_at_T"
                ys.append(y); ps.append(pred)
                predictions.append({
                    "district_key": r["district_key"], "commodity_name": r["commodity_name"],
                    "currency_code": r["currency_code"], "prediction_month": r["prediction_month"],
                    "target_month": r["target_month"], "fold": fold, "method": method,
                    "y_true": y, "y_pred": pred, "probability": prob,
                    "model_run_id": run_id,
                })
            m = metrics(ys, ps)
            m.update({"fold": fold, "method": method, "train_months": w["train_months"],
                      "test_months": w["test_months"],
                      "roc_auc": 0.5 if method == "Dummy" and len(set(ys)) == 2 else ("" if method == "Persistence" else ""),
                      "pr_auc_average_precision": (sum(ys) / len(ys)) if method == "Dummy" and len(set(ys)) == 2 else "",
                      "brier_score": (sum((0.0 - y) ** 2 for y in ys) / len(ys)) if method == "Dummy" else "",
                      "probability_source": "deterministic DummyClassifier score" if method == "Dummy" else "unavailable; persistence is a class comparator, not a probability model"})
            method_metrics.append(m)

    with (OUT / "fold_predictions.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(predictions[0]))
        w.writeheader(); w.writerows(predictions)
    with (OUT / "scripts" / "available_method_metrics.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(method_metrics[0]))
        w.writeheader(); w.writerows(method_metrics)
    with (OUT / "fold_predictions_index.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["method", "status", "source_or_reason", "row_count"])
        w.writerow(["Dummy", "RECONSTRUCTED", "Most-frequent class fit from each saved training window", sum(r["method"] == "Dummy" for r in predictions)])
        w.writerow(["Persistence", "RECONSTRUCTED", "Observed price_stress_current at T; no T+1 predictor use", sum(r["method"] == "Persistence" for r in predictions)])
        w.writerow(["LogisticRegression", "UNAVAILABLE", "Original fold score/prediction vectors were not persisted; sklearn unavailable in execution runtime", 0])
        w.writerow(["XGBoost", "UNAVAILABLE", "Original fold score/prediction vectors were not persisted; xgboost/sklearn unavailable in execution runtime", 0])
    print("fold_test_predictions", len(predictions))
    for r in method_metrics:
        print(r["fold"], r["method"], "n", r["n_test"], "macro_f1", f"{r['macro_f1']:.4f}", "TP", r["TP"], "AUC", r["roc_auc"])


if __name__ == "__main__":
    main()
