"""
step08_model_evaluation.py
==========================
STEP 8 - HELD-OUT EVALUATION.

Fit the candidate models on a stratified train split and evaluate on an untouched test set.
Besides the human-readable report and figures, this step persists machine-readable artefacts
so the dashboard can visualise the *actual* evaluation without retraining:

    outputs/results/step08_model_comparison.csv   headline metric table
    outputs/results/step08_metrics_full.csv       every metric that can be computed
    outputs/results/step08_predictions.csv        y_true + per-model probability & class
    outputs/results/step08_confusion_<model>.csv  confusion matrix (Low/High)
    outputs/results/step08_roc_curves.csv         ROC points per model
    outputs/results/step08_pr_curves.csv          precision-recall points per model
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config as C  # noqa: E402
from src.step07_model_training import build_models  # noqa: E402
from src.utils import banner, save_df, save_fig, write_text

TARGET = "price_stress"
LABELS = ["Low Price Stress", "High Price Stress"]


def _safe_auc(y_true, proba, kind: str) -> float:
    from sklearn.metrics import average_precision_score, roc_auc_score
    try:
        return (roc_auc_score if kind == "roc" else average_precision_score)(y_true, proba)
    except Exception:
        return float("nan")


def main() -> None:
    from sklearn.metrics import (ConfusionMatrixDisplay, balanced_accuracy_score,
                                 brier_score_loss, classification_report, confusion_matrix,
                                 f1_score, precision_recall_curve, roc_curve, auc,
                                 accuracy_score)
    from sklearn.model_selection import train_test_split

    banner("8", "MODEL EVALUATION")
    df = pd.read_csv(C.TRAIN_COMMODITY, parse_dates=["month"])
    selected = json.loads((C.DATA_PROC / "selected_features.json").read_text())["selected"]
    X = df[selected].fillna(df[selected].median(numeric_only=True))
    y = df[TARGET].astype(int)

    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=C.TEST_SIZE, stratify=y, random_state=C.RANDOM_STATE)
    print(f"train={X_tr.shape}, test={X_te.shape}")

    models = build_models()
    rows, full_rows, roc_rows, pr_rows = [], [], [], []
    preds = pd.DataFrame({"y_true": y_te.to_numpy()})

    for name, model in models.items():
        model.fit(X_tr, y_tr)
        pred = model.predict(X_te)
        report = classification_report(y_te, pred, output_dict=True, zero_division=0)
        row = {
            "model": name,
            "accuracy": accuracy_score(y_te, pred),
            "balanced_accuracy": balanced_accuracy_score(y_te, pred),
            "macro_f1": f1_score(y_te, pred, average="macro"),
        }
        rows.append(row)
        preds[f"{name}_pred"] = pred

        full = dict(row)
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(X_te)[:, 1]
            preds[f"{name}_proba"] = proba
            full["roc_auc"] = _safe_auc(y_te, proba, "roc")
            full["pr_auc"] = _safe_auc(y_te, proba, "pr")
            try:
                full["brier"] = brier_score_loss(y_te, proba)
            except Exception:
                full["brier"] = float("nan")
            if np.isfinite(full["roc_auc"]):
                fpr, tpr, _ = roc_curve(y_te, proba)
                roc_rows += [{"model": name, "fpr": a, "tpr": b, "auc": auc(fpr, tpr)}
                             for a, b in zip(fpr, tpr)]
            if np.isfinite(full["pr_auc"]):
                prec, rec, _ = precision_recall_curve(y_te, proba)
                pr_rows += [{"model": name, "recall": r, "precision": p}
                            for r, p in zip(rec, prec)]
        full_rows.append(full)

        cm = confusion_matrix(y_te, pred)
        cm_df = pd.DataFrame(cm, index=LABELS, columns=LABELS)
        cm_df.index.name = "actual"
        save_df(cm_df.reset_index(), f"step08_confusion_{name}")

        fig, ax = plt.subplots(figsize=(4.2, 3.6))
        ConfusionMatrixDisplay(cm, display_labels=["Low", "High"]).plot(
            ax=ax, cmap="Blues", colorbar=False)
        ax.set_title(f"Confusion - {name}")
        ax.set_xlabel("Predicted class")
        ax.set_ylabel("Actual class")
        save_fig(fig, f"step08_confusion_{name}")
        plt.close(fig)

    comp = pd.DataFrame(rows).round(4).sort_values("macro_f1", ascending=False)
    save_df(comp, "step08_model_comparison")
    print("\nmodel comparison:\n", comp.to_string(index=False))

    save_df(pd.DataFrame(full_rows).round(4), "step08_metrics_full")
    save_df(preds, "step08_predictions")
    if roc_rows:
        save_df(pd.DataFrame(roc_rows), "step08_roc_curves")
    if pr_rows:
        save_df(pd.DataFrame(pr_rows), "step08_pr_curves")

    if roc_rows:
        fig, ax = plt.subplots(figsize=(5, 4.5))
        for name in comp["model"]:
            sub = pd.DataFrame(roc_rows)
            sub = sub[sub["model"] == name]
            if len(sub):
                ax.plot(sub["fpr"], sub["tpr"], label=f"{name} (AUC={sub['auc'].iloc[0]:.3f})")
        ax.plot([0, 1], [0, 1], "k--", lw=1)
        ax.set_xlabel("False positive rate")
        ax.set_ylabel("True positive rate")
        ax.set_title("ROC curves - held-out test set")
        ax.legend(loc="lower right")
        save_fig(fig, "step08_roc_curves")
        plt.close(fig)

    lines = ["# Step 8 - Model Evaluation", "",
             f"Test size = {C.TEST_SIZE:.0%}; features = {len(selected)}.", "",
             "```", comp.to_string(index=False), "```", "",
             "Balanced accuracy (macro recall) and macro-F1 are the headline metrics.",
             "Class labels: 0 = Low Price Stress, 1 = High Price Stress."]
    write_text("\n".join(lines), "step08_model_evaluation", C.REPORTS)

    banner("8", "EVALUATION COMPLETE -> outputs/results/step08_*")


if __name__ == "__main__":
    main()
