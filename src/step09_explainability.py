"""
step09_explainability.py
========================
STEP 9 - EXPLAINABILITY.

Produces:
  * Permutation importance (model-agnostic; trained on a split, scored on the held-out part).
  * SHAP values for the XGBoost model using the fast TreeExplainer, when SHAP is importable.
    SHAP is explained here at the *observation* level, so the saved values line up with the
    dashboard's per-observation predictions (both use the saved step07 full-data model).

Artefacts written to outputs/results/:
    step09_permutation_importance.csv
    step09_shap_importance.csv        mean |SHAP| per feature
    step09_shap_values.csv            per-observation SHAP (row_index + shap_<feature>)
    step09_shap_base.csv              explainer expected value (log-odds)
and outputs/figures/step09_shap_summary.png.
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


def permutation_importance_manual(model, X, y, n_repeats, random_state):
    """Model-agnostic permutation importance scored by balanced accuracy."""
    from sklearn.metrics import balanced_accuracy_score
    rng = np.random.default_rng(random_state)
    base = balanced_accuracy_score(y, model.predict(X))
    rows = []
    for col in X.columns:
        drops = []
        col_vals = X[col].to_numpy()
        for _ in range(n_repeats):
            Xp = X.copy()
            Xp[col] = rng.permutation(col_vals)
            drops.append(base - balanced_accuracy_score(y, model.predict(Xp)))
        rows.append({"feature": col,
                     "importance_mean": float(np.mean(drops)),
                     "importance_std": float(np.std(drops))})
    return base, pd.DataFrame(rows)


def run_shap(model, X: pd.DataFrame, feature_names: list[str]) -> str:
    """Compute and persist SHAP values for a tree model. Returns a status note."""
    try:
        import shap
    except Exception as exc:  # pragma: no cover - depends on the host policy
        return f"SHAP import failed ({type(exc).__name__}); only permutation importance saved."

    try:
        explainer = shap.TreeExplainer(model)
        values = explainer.shap_values(X, check_additivity=False)
        values = np.asarray(values)
        if values.ndim == 3:            # (n, features, classes) -> positive class
            values = values[:, :, -1]
        base = np.asarray(explainer.expected_value).ravel()
        base_value = float(base[-1]) if base.size else float("nan")

        shap_df = pd.DataFrame(values, columns=[f"shap_{f}" for f in feature_names])
        shap_df.insert(0, "row_index", np.arange(len(shap_df)))
        save_df(shap_df, "step09_shap_values")

        save_df(pd.DataFrame([{"model": type(model).__name__, "expected_value_logodds": base_value}]),
                "step09_shap_base")

        importance = (pd.DataFrame({"feature": feature_names,
                                    "mean_abs_shap": np.abs(values).mean(axis=0)})
                      .sort_values("mean_abs_shap", ascending=False).round(6))
        save_df(importance, "step09_shap_importance")

        fig = plt.figure()
        shap.summary_plot(values, X, feature_names=feature_names, show=False, max_display=15)
        save_fig(fig, "step09_shap_summary")
        plt.close("all")
        return (f"SHAP computed for {type(model).__name__} "
                f"({values.shape[0]} observations x {values.shape[1]} features).")
    except Exception as exc:  # pragma: no cover
        plt.close("all")
        return f"SHAP computation failed ({type(exc).__name__}: {exc})."


def main() -> None:
    from sklearn.model_selection import train_test_split

    banner("9", "EXPLAINABILITY")
    df = pd.read_csv(C.TRAIN_COMMODITY, parse_dates=["month"])
    selected = json.loads((C.DATA_PROC / "selected_features.json").read_text())["selected"]
    X = df[selected].fillna(df[selected].median(numeric_only=True))
    y = df[TARGET].astype(int)

    # --- permutation importance (honest: fit on train, score on test) -----------------
    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=C.TEST_SIZE, stratify=y, random_state=C.RANDOM_STATE)
    split_model = build_models().get("xgboost") or build_models()["logreg"]
    split_model.fit(X_tr, y_tr)
    base_acc, imp_raw = permutation_importance_manual(
        split_model, X_te, y_te, n_repeats=15, random_state=C.RANDOM_STATE)
    print(f"baseline balanced accuracy on test: {base_acc:.4f}")
    imp = imp_raw.sort_values("importance_mean", ascending=False).round(5)
    save_df(imp, "step09_permutation_importance")
    print("\npermutation importance:\n", imp.to_string(index=False))

    top = imp.head(15)
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.barh(top["feature"][::-1], top["importance_mean"][::-1],
            xerr=top["importance_std"][::-1], color="#3182bd")
    ax.set_title("Permutation importance (balanced accuracy drop)")
    ax.set_xlabel("mean importance")
    save_fig(fig, "step09_permutation_importance")
    plt.close(fig)

    # --- SHAP on the saved full-data model (aligns with dashboard predictions) ---------
    shap_model = None
    try:
        import joblib
        shap_model = joblib.load(C.OUT_MODELS / "step07_xgboost.joblib")
    except Exception as exc:
        print(f"  [warn] could not load step07_xgboost.joblib ({exc}); using the split model.")
    if shap_model is None:
        shap_model = split_model

    shap_note = run_shap(shap_model, X, selected)
    print(f"\n{shap_note}")

    lines = ["# Step 9 - Explainability", "",
             f"Permutation model: `{type(split_model).__name__}`; {shap_note}", "",
             "## Permutation importance", "```", imp.to_string(index=False), "```", "",
             "## SHAP (mean |value|) - XGBoost TreeExplainer",
             "```",
             (pd.read_csv(C.OUT_RES / "step09_shap_importance.csv").to_string(index=False)
              if (C.OUT_RES / "step09_shap_importance.csv").exists() else "SHAP unavailable."),
             "```"]
    write_text("\n".join(lines), "step09_explainability", C.REPORTS)

    banner("9", "EXPLAINABILITY COMPLETE -> outputs/results/step09_*")


if __name__ == "__main__":
    main()
