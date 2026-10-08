"""
step07_model_training.py
========================
STEP 7 - MODEL TRAINING with cross-validation.

Models: Dummy (baseline), Logistic Regression, XGBoost.
CV strategies:
  * StratifiedKFold        - random, for reference
  * GroupKFold(district)   - the primary, honest estimate: rows from one district never
                             appear in both train and test (they are serially correlated).

NOTE: scikit-learn RandomForest / GradientBoosting are unavailable in this environment
(Windows Application Control blocks the `_gradient_boosting` DLL). Logistic Regression and
XGBoost are used instead. XGBoost is skipped gracefully if it cannot be imported.

Outputs: outputs/results/step07_cv_results.csv, outputs/models/*.joblib
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config as C  # noqa: E402
from src.utils import banner, save_df, write_text

TARGET = "price_stress"


def build_models() -> dict:
    from sklearn.dummy import DummyClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler

    models = {
        "dummy": DummyClassifier(strategy="most_frequent"),
        "logreg": Pipeline([
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(max_iter=2000, class_weight="balanced",
                                       random_state=C.RANDOM_STATE)),
        ]),
    }
    try:
        from xgboost import XGBClassifier
        models["xgboost"] = XGBClassifier(
            n_estimators=400, max_depth=4, learning_rate=0.05,
            subsample=0.8, colsample_bytree=0.8, eval_metric="logloss",
            random_state=C.RANDOM_STATE, n_jobs=4,
        )
    except Exception as exc:  # pragma: no cover
        print(f"  [skip] xgboost unavailable: {exc}")
    return models


def score(model, X_tr, y_tr, X_te, y_te) -> dict:
    from sklearn.metrics import balanced_accuracy_score, f1_score, roc_auc_score
    model.fit(X_tr, y_tr)
    pred = model.predict(X_te)
    out = {
        "balanced_accuracy": balanced_accuracy_score(y_te, pred),
        "macro_f1": f1_score(y_te, pred, average="macro"),
    }
    if hasattr(model, "predict_proba"):
        try:
            out["roc_auc"] = roc_auc_score(y_te, model.predict_proba(X_te)[:, 1])
        except Exception:
            out["roc_auc"] = np.nan
    else:
        out["roc_auc"] = np.nan
    return out


def main() -> None:
    from sklearn.model_selection import GroupKFold, StratifiedKFold, cross_val_score

    banner("7", "MODEL TRAINING")
    df = pd.read_csv(C.TRAIN_COMMODITY, parse_dates=["month"])
    selected = json.loads((C.DATA_PROC / "selected_features.json").read_text())["selected"]
    X = df[selected].fillna(df[selected].median(numeric_only=True))
    y = df[TARGET].astype(int)
    groups = df["district_key"].astype("category").cat.codes.values
    print(f"X={X.shape}, y={y.shape}, districts={df['district_key'].nunique()}")

    models = build_models()
    rows = []

    # --- StratifiedKFold (random reference) -----------------------------------------
    skf = StratifiedKFold(n_splits=C.N_SPLITS, shuffle=True, random_state=C.RANDOM_STATE)
    for name, model in models.items():
        for fold, (tr, te) in enumerate(skf.split(X, y), 1):
            m = score(model, X.iloc[tr], y.iloc[tr], X.iloc[te], y.iloc[te])
            rows.append({"cv": "stratified_kfold", "model": name, "fold": fold, **m})

    # --- GroupKFold by district (primary) -------------------------------------------
    gkf = GroupKFold(n_splits=C.N_SPLITS)
    for name, model in models.items():
        for fold, (tr, te) in enumerate(gkf.split(X, y, groups), 1):
            m = score(model, X.iloc[tr], y.iloc[tr], X.iloc[te], y.iloc[te])
            rows.append({"cv": "group_kfold_district", "model": name, "fold": fold, **m})

    res = pd.DataFrame(rows)
    save_df(res, "step07_cv_results")

    summary = (res.groupby(["cv", "model"])[["balanced_accuracy", "macro_f1", "roc_auc"]]
               .agg(["mean", "std"]).round(4))
    save_df(summary.reset_index(), "step07_cv_summary")
    print("\nCV summary:\n", summary.to_string())

    # --- Fit final models on all data and persist -----------------------------------
    for name, model in models.items():
        model.fit(X, y)
        try:
            import joblib
            joblib.dump(model, C.OUT_MODELS / f"step07_{name}.joblib")
        except Exception as exc:  # pragma: no cover
            print(f"  [warn] could not save {name}: {exc}")

    lines = ["# Step 7 - Model Training", "",
             f"Features: {len(selected)}; models: {list(models)}", "",
             "## CV summary (mean +/- std across folds)", "```",
             summary.to_string(), "```", "",
             "GroupKFold by district is the primary, leakage-safe estimate."]
    write_text("\n".join(lines), "step07_model_training", C.REPORTS)

    banner("7", "TRAINING COMPLETE -> outputs/results/step07_cv_summary.csv")


if __name__ == "__main__":
    main()
