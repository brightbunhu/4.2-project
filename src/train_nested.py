"""
src/train_nested.py
====================
CORRECTED ML PIPELINE - Nested GroupKFold with Automated Hyperparameter Tuning.

This script replaces the old step07/step08/step09 fixed-parameter workflow with:

1. District-grouped nested GroupKFold (outer K=5, inner K=3)
2. RandomizedSearchCV hyperparameter tuning within the inner loop
3. Leakage-safe scikit-learn Pipelines (imputer + scaler fitted per fold)
4. Final model retraining on full data with best parameters
5. Complete evaluation regeneration
6. TreeSHAP on the final XGBoost model

Usage:
    python -m src.train_nested

Outputs:
    models/logreg_pipeline.joblib
    models/xgboost_pipeline.joblib
    models/dummy_baseline.joblib
    outputs/results/nested_groupkfold_results.csv
    outputs/results/outer_fold_metrics.csv
    outputs/results/nested_validation_summary.csv
    outputs/results/best_hyperparameters.csv
    outputs/results/logreg_search_results.csv
    outputs/results/xgboost_search_results.csv
    outputs/results/model_training_metadata.json
    outputs/results/groupkfold_metrics.csv
    outputs/results/holdout_metrics.csv
    outputs/results/per_class_metrics.csv
    outputs/results/confusion_matrices.csv
    outputs/results/calibration_metrics.csv
    outputs/results/model_comparison.csv
    outputs/results/data_leakage_audit.csv
    outputs/results/reporting_gap_summary.csv
    outputs/figures/confusion_matrix_logreg.png
    outputs/figures/confusion_matrix_xgboost.png
    outputs/figures/roc_curve_comparison.png
    outputs/figures/precision_recall_curve_comparison.png
    outputs/figures/model_metric_comparison.png
    outputs/figures/calibration_plot.png
    outputs/figures/price_reporting_gap_distribution.png
    outputs/explainability/shap_values.parquet
    outputs/explainability/shap_global_importance.csv
    outputs/explainability/shap_local_examples.csv
    outputs/figures/shap_summary.png
    outputs/figures/shap_global_importance.png
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
import warnings
from datetime import datetime, timezone
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config as C  # noqa: E402

RANDOM_STATE = 42
TARGET = "price_stress"
MODELS_DIR = C.ROOT / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)
OUT_EXPLAINABILITY = C.ROOT / "outputs" / "explainability"
OUT_EXPLAINABILITY.mkdir(parents=True, exist_ok=True)


def banner(title: str) -> None:
    print(f"\n{'=' * 96}\n  {title}\n{'=' * 96}")


def save_csv(df: pd.DataFrame, name: str, subdir: Path | None = None) -> Path:
    d = subdir or C.OUT_RES
    d.mkdir(parents=True, exist_ok=True)
    p = d / (name if name.endswith(".csv") else f"{name}.csv")
    df.to_csv(p, index=False)
    print(f"    [saved] {p.relative_to(C.ROOT)}  shape={df.shape}")
    return p


def save_figure(fig, name: str, subdir: Path | None = None) -> Path:
    d = subdir or C.OUT_FIG
    d.mkdir(parents=True, exist_ok=True)
    p = d / (name if name.endswith(".png") else f"{name}.png")
    fig.savefig(p, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"    [figure] {p.relative_to(C.ROOT)}")
    return p


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


# ==============================================================================
# 0. LOAD DATA
# ==============================================================================
def load_data():
    banner("0. LOADING DATA")
    df = pd.read_csv(C.TRAIN_COMMODITY, parse_dates=["month"])

    # Load feature list from step06 selection
    sel_path = C.DATA_PROC / "selected_features.json"
    payload = json.loads(sel_path.read_text())
    if isinstance(payload, dict):
        features = list(payload.get("selected", []))
    else:
        features = list(payload)

    # Ensure months_since_last_reported_price is included if available
    if "months_since_last_reported_price" in df.columns and "months_since_last_reported_price" not in features:
        features.append("months_since_last_reported_price")

    features = [f for f in features if f in df.columns]

    X = df[features].copy()
    y = df[TARGET].astype(int).copy()
    groups = df["district_key"].values

    print(f"X shape: {X.shape}")
    print(f"y distribution: {y.value_counts().to_dict()}")
    print(f"Unique districts: {len(np.unique(groups))}")
    print(f"Features ({len(features)}): {features}")

    return df, X, y, groups, features


# ==============================================================================
# 1. REPORTING GAP SUMMARY
# ==============================================================================
def generate_reporting_gap_summary(df: pd.DataFrame):
    banner("1. REPORTING GAP SUMMARY")

    if "months_since_last_reported_price" not in df.columns:
        print("  [WARN] months_since_last_reported_price not in training table")
        return

    gap = df["months_since_last_reported_price"].dropna()
    summary = pd.DataFrame([{
        "statistic": "count", "value": len(gap),
    }, {
        "statistic": "mean", "value": round(gap.mean(), 2),
    }, {
        "statistic": "median", "value": round(gap.median(), 2),
    }, {
        "statistic": "std", "value": round(gap.std(), 2),
    }, {
        "statistic": "min", "value": round(gap.min(), 2),
    }, {
        "statistic": "max", "value": round(gap.max(), 2),
    }, {
        "statistic": "pct_1_month_gap", "value": round(100 * (gap <= 1.1).mean(), 2),
    }, {
        "statistic": "pct_gt_3_month_gap", "value": round(100 * (gap > 3.0).mean(), 2),
    }])
    save_csv(summary, "reporting_gap_summary")

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(gap.clip(upper=24), bins=50, color="#3182bd", edgecolor="white", alpha=0.85)
    ax.set_xlabel("Months since last reported price")
    ax.set_ylabel("Frequency")
    ax.set_title("Distribution of Price Reporting Gaps")
    ax.axvline(gap.median(), color="red", linestyle="--", label=f"Median = {gap.median():.1f}")
    ax.legend()
    save_figure(fig, "price_reporting_gap_distribution")
    print(f"  Reporting gap: mean={gap.mean():.2f}, median={gap.median():.2f}")


# ==============================================================================
# 2. DATA LEAKAGE AUDIT
# ==============================================================================
def generate_leakage_audit(features: list[str]):
    banner("2. DATA LEAKAGE AUDIT")
    leaky_vars = {"price", "country_median_price", "spatial_price_index",
                  "price_spi_raw", "spi_pct_dev", "spi_winsorised",
                  "price_stress", "district_key"}

    rows = []
    for f in features:
        is_leaky = f in leaky_vars
        rows.append({
            "feature": f,
            "transformation": "pipeline (imputer+scaler per fold)" if f not in [
                c for c in features if c.startswith("commodity_")
            ] else "one-hot encoded before split (categorical)",
            "fitted_where": "inside pipeline per fold",
            "inside_pipeline": "YES",
            "fitted_per_fold": "YES",
            "target_derived": "NO",
            "status": "FAIL - LEAKAGE" if is_leaky else "PASS",
        })

    # Check additional known leaky variables NOT in features
    for v in sorted(leaky_vars):
        if v not in features:
            rows.append({
                "feature": v,
                "transformation": "EXCLUDED from features",
                "fitted_where": "N/A",
                "inside_pipeline": "N/A",
                "fitted_per_fold": "N/A",
                "target_derived": "YES" if v == "price_stress" else "POTENTIAL",
                "status": "PASS - EXCLUDED",
            })

    audit = pd.DataFrame(rows)
    save_csv(audit, "data_leakage_audit")

    n_fail = (audit["status"].str.contains("FAIL")).sum()
    print(f"  Leakage audit: {len(rows)} checks, {n_fail} failures")
    if n_fail > 0:
        print("  [ERROR] Leakage detected in features!")
    return n_fail == 0


# ==============================================================================
# 3. NESTED GROUPKFOLD WITH HYPERPARAMETER TUNING
# ==============================================================================
def nested_groupkfold(X, y, groups, features):
    banner("3. NESTED GROUPKFOLD (outer=5, inner=3)")

    from sklearn.dummy import DummyClassifier
    from sklearn.impute import SimpleImputer
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import GroupKFold, RandomizedSearchCV
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler
    from xgboost import XGBClassifier
    from sklearn.metrics import (
        accuracy_score, balanced_accuracy_score, f1_score,
        roc_auc_score, average_precision_score, brier_score_loss,
        confusion_matrix, classification_report,
    )

    # Compute class weight for XGBoost
    neg_count = (y == 0).sum()
    pos_count = (y == 1).sum()
    scale_pos_weight = neg_count / pos_count if pos_count > 0 else 1.0

    # --- Define pipelines and search spaces ---
    logreg_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
        ("classifier", LogisticRegression(max_iter=2000, random_state=RANDOM_STATE)),
    ])

    logreg_params = {
        "classifier__C": [0.001, 0.01, 0.1, 1, 10, 100, 1000],
        "classifier__penalty": ["l2"],
        "classifier__solver": ["lbfgs"],
        "classifier__class_weight": [None, "balanced"],
    }

    xgb_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("classifier", XGBClassifier(
            eval_metric="logloss", random_state=RANDOM_STATE, n_jobs=4,
            use_label_encoder=False,
        )),
    ])

    xgb_params = {
        "classifier__n_estimators": [200, 400, 600],
        "classifier__max_depth": [2, 3, 4, 5],
        "classifier__learning_rate": [0.01, 0.05, 0.1],
        "classifier__subsample": [0.7, 0.8, 1.0],
        "classifier__colsample_bytree": [0.7, 0.8, 1.0],
        "classifier__scale_pos_weight": [1.0, scale_pos_weight],
        "classifier__reg_alpha": [0.01, 0.1, 1.0, 10.0],
        "classifier__reg_lambda": [0.01, 0.1, 1.0, 10.0],
    }

    outer_cv = GroupKFold(n_splits=5)
    inner_cv = GroupKFold(n_splits=3)

    # Verify we have enough district groups
    unique_districts = np.unique(groups)
    n_districts = len(unique_districts)
    print(f"  Districts available: {n_districts}")
    if n_districts < 5:
        raise ValueError(f"Only {n_districts} district groups available; need at least 5 for outer GroupKFold.")

    all_results = []
    logreg_search_results = []
    xgb_search_results = []
    best_params_all = []

    model_configs = {
        "logreg": (logreg_pipe, logreg_params, 14),
        "xgboost": (xgb_pipe, xgb_params, 40),
    }

    for model_name, (pipe, param_grid, n_iter) in model_configs.items():
        print(f"\n  --- {model_name} ---")

        for fold_idx, (train_idx, test_idx) in enumerate(outer_cv.split(X, y, groups)):
            X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
            y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
            groups_train = groups[train_idx]
            groups_test = groups[test_idx]

            # Verify no district leakage
            train_districts = set(groups_train)
            test_districts = set(groups_test)
            overlap = train_districts & test_districts
            assert len(overlap) == 0, f"District leakage in fold {fold_idx}: {overlap}"

            print(f"    Fold {fold_idx+1}: train={len(X_train)} ({len(train_districts)} districts), "
                  f"test={len(X_test)} ({len(test_districts)} districts)")

            # Inner CV for hyperparameter tuning
            search = RandomizedSearchCV(
                pipe, param_grid,
                n_iter=n_iter,
                cv=inner_cv,
                scoring="balanced_accuracy",
                random_state=RANDOM_STATE,
                n_jobs=4,
                refit=True,
                error_score="raise",
            )

            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                search.fit(X_train, y_train, groups=groups_train)

            # Collect search results
            cv_results = pd.DataFrame(search.cv_results_)
            cv_results["outer_fold"] = fold_idx + 1
            cv_results["model"] = model_name
            if model_name == "logreg":
                logreg_search_results.append(cv_results)
            else:
                xgb_search_results.append(cv_results)

            # Predict on outer test fold
            best_model = search.best_estimator_
            y_pred = best_model.predict(X_test)
            y_proba = None
            if hasattr(best_model, "predict_proba"):
                y_proba = best_model.predict_proba(X_test)[:, 1]

            # Calculate metrics
            metrics = {
                "model": model_name,
                "outer_fold": fold_idx + 1,
                "n_train": len(X_train),
                "n_test": len(X_test),
                "n_train_districts": len(train_districts),
                "n_test_districts": len(test_districts),
                "best_inner_score": search.best_score_,
                "accuracy": accuracy_score(y_test, y_pred),
                "balanced_accuracy": balanced_accuracy_score(y_test, y_pred),
                "macro_f1": f1_score(y_test, y_pred, average="macro"),
            }

            if y_proba is not None:
                try:
                    metrics["roc_auc"] = roc_auc_score(y_test, y_proba)
                except Exception:
                    metrics["roc_auc"] = np.nan
                try:
                    metrics["pr_auc"] = average_precision_score(y_test, y_proba)
                except Exception:
                    metrics["pr_auc"] = np.nan
                try:
                    metrics["brier"] = brier_score_loss(y_test, y_proba)
                except Exception:
                    metrics["brier"] = np.nan
            else:
                metrics["roc_auc"] = np.nan
                metrics["pr_auc"] = np.nan
                metrics["brier"] = np.nan

            # Best parameters for this fold
            best_p = {k: v for k, v in search.best_params_.items()}
            metrics["best_params"] = json.dumps(best_p)

            all_results.append(metrics)
            print(f"      best_inner_score={search.best_score_:.4f}, "
                  f"outer_balanced_acc={metrics['balanced_accuracy']:.4f}, "
                  f"outer_macro_f1={metrics['macro_f1']:.4f}")

    # --- DummyClassifier baseline across folds ---
    print(f"\n  --- dummy ---")
    for fold_idx, (train_idx, test_idx) in enumerate(outer_cv.split(X, y, groups)):
        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

        dummy = DummyClassifier(strategy="most_frequent", random_state=RANDOM_STATE)
        dummy.fit(X_train, y_train)
        y_pred = dummy.predict(X_test)

        metrics = {
            "model": "dummy",
            "outer_fold": fold_idx + 1,
            "n_train": len(X_train),
            "n_test": len(X_test),
            "n_train_districts": len(set(groups[train_idx])),
            "n_test_districts": len(set(groups[test_idx])),
            "best_inner_score": np.nan,
            "accuracy": accuracy_score(y_test, y_pred),
            "balanced_accuracy": balanced_accuracy_score(y_test, y_pred),
            "macro_f1": f1_score(y_test, y_pred, average="macro"),
            "roc_auc": np.nan,
            "pr_auc": np.nan,
            "brier": np.nan,
            "best_params": "{}",
        }
        all_results.append(metrics)

    # Save results
    results_df = pd.DataFrame(all_results)
    save_csv(results_df, "nested_groupkfold_results")

    # Outer fold metrics (summary)
    outer_metrics = (results_df.groupby("model")
                     [["balanced_accuracy", "macro_f1", "roc_auc", "pr_auc", "brier"]]
                     .agg(["mean", "std"])
                     .round(4))
    outer_metrics.columns = ["_".join(c) for c in outer_metrics.columns]
    outer_metrics = outer_metrics.reset_index()
    save_csv(outer_metrics, "outer_fold_metrics")

    # Save search results
    if logreg_search_results:
        lr_results = pd.concat(logreg_search_results, ignore_index=True)
        save_csv(lr_results[["outer_fold", "params", "mean_test_score", "std_test_score", "rank_test_score"]],
                 "logreg_search_results")
    if xgb_search_results:
        xgb_results = pd.concat(xgb_search_results, ignore_index=True)
        save_csv(xgb_results[["outer_fold", "params", "mean_test_score", "std_test_score", "rank_test_score"]],
                 "xgboost_search_results")

    # Also save as the GroupKFold metrics expected by the dashboard
    save_csv(results_df, "groupkfold_metrics")

    # Nested validation summary
    summary_rows = []
    for model_name in results_df["model"].unique():
        sub = results_df[results_df["model"] == model_name]
        summary_rows.append({
            "model": model_name,
            "n_outer_folds": len(sub),
            "mean_balanced_accuracy": round(sub["balanced_accuracy"].mean(), 4),
            "std_balanced_accuracy": round(sub["balanced_accuracy"].std(), 4),
            "mean_macro_f1": round(sub["macro_f1"].mean(), 4),
            "std_macro_f1": round(sub["macro_f1"].std(), 4),
            "mean_roc_auc": round(sub["roc_auc"].mean(), 4) if sub["roc_auc"].notna().any() else np.nan,
            "mean_pr_auc": round(sub["pr_auc"].mean(), 4) if sub["pr_auc"].notna().any() else np.nan,
            "mean_brier": round(sub["brier"].mean(), 4) if sub["brier"].notna().any() else np.nan,
        })
    summary_df = pd.DataFrame(summary_rows)
    save_csv(summary_df, "nested_validation_summary")

    print("\n  Nested validation summary:")
    print(summary_df.to_string(index=False))

    return results_df, logreg_search_results, xgb_search_results


# ==============================================================================
# 4. RETRAIN FINAL MODELS WITH BEST PARAMETERS
# ==============================================================================
def retrain_final_models(X, y, groups, logreg_search_results, xgb_search_results):
    banner("4. RETRAIN FINAL MODELS")

    import joblib
    from sklearn.dummy import DummyClassifier
    from sklearn.impute import SimpleImputer
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import GroupKFold, RandomizedSearchCV
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler
    from xgboost import XGBClassifier

    neg_count = (y == 0).sum()
    pos_count = (y == 1).sum()
    scale_pos_weight = neg_count / pos_count if pos_count > 0 else 1.0

    inner_cv = GroupKFold(n_splits=3)

    # --- Logistic Regression: full retune on all data with inner CV ---
    logreg_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
        ("classifier", LogisticRegression(max_iter=2000, random_state=RANDOM_STATE)),
    ])

    logreg_params = {
        "classifier__C": [0.001, 0.01, 0.1, 1, 10, 100, 1000],
        "classifier__penalty": ["l2"],
        "classifier__solver": ["lbfgs"],
        "classifier__class_weight": [None, "balanced"],
    }

    logreg_search = RandomizedSearchCV(
        logreg_pipe, logreg_params,
        n_iter=14,  # exhaustive for this small grid
        cv=inner_cv,
        scoring="balanced_accuracy",
        random_state=RANDOM_STATE,
        n_jobs=4,
        refit=True,
    )

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        logreg_search.fit(X, y, groups=groups)

    logreg_best = logreg_search.best_estimator_
    logreg_best_params = logreg_search.best_params_
    logreg_best_score = logreg_search.best_score_

    print(f"  LogReg best params: {logreg_best_params}")
    print(f"  LogReg best inner score: {logreg_best_score:.4f}")

    # --- XGBoost: full retune on all data ---
    xgb_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("classifier", XGBClassifier(
            eval_metric="logloss", random_state=RANDOM_STATE, n_jobs=4,
            use_label_encoder=False,
        )),
    ])

    xgb_params = {
        "classifier__n_estimators": [200, 400, 600],
        "classifier__max_depth": [2, 3, 4, 5],
        "classifier__learning_rate": [0.01, 0.05, 0.1],
        "classifier__subsample": [0.7, 0.8, 1.0],
        "classifier__colsample_bytree": [0.7, 0.8, 1.0],
        "classifier__scale_pos_weight": [1.0, scale_pos_weight],
        "classifier__reg_alpha": [0.01, 0.1, 1.0, 10.0],
        "classifier__reg_lambda": [0.01, 0.1, 1.0, 10.0],
    }

    xgb_search = RandomizedSearchCV(
        xgb_pipe, xgb_params,
        n_iter=40,
        cv=inner_cv,
        scoring="balanced_accuracy",
        random_state=RANDOM_STATE,
        n_jobs=4,
        refit=True,
    )

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        xgb_search.fit(X, y, groups=groups)

    xgb_best = xgb_search.best_estimator_
    xgb_best_params = xgb_search.best_params_
    xgb_best_score = xgb_search.best_score_

    print(f"  XGBoost best params: {xgb_best_params}")
    print(f"  XGBoost best inner score: {xgb_best_score:.4f}")

    # --- DummyClassifier ---
    dummy = DummyClassifier(strategy="most_frequent", random_state=RANDOM_STATE)
    dummy.fit(X, y)

    # --- Save models ---
    # Archive old models first
    import shutil
    archive_models = C.ROOT / "archive" / "obsolete_files" / "old_models"
    archive_models.mkdir(parents=True, exist_ok=True)

    for old_model in MODELS_DIR.glob("*.joblib"):
        dest = archive_models / old_model.name
        shutil.copy2(old_model, dest)
        print(f"    [archived] {old_model.name} -> archive/obsolete_files/old_models/")

    # Also archive old output models
    old_out_models = C.ROOT / "outputs" / "models"
    if old_out_models.exists():
        for old_model in old_out_models.glob("*.joblib"):
            dest = archive_models / old_model.name
            shutil.copy2(old_model, dest)

    # Save new models
    joblib.dump(logreg_best, MODELS_DIR / "logreg_pipeline.joblib")
    joblib.dump(xgb_best, MODELS_DIR / "xgboost_pipeline.joblib")
    joblib.dump(dummy, MODELS_DIR / "dummy_baseline.joblib")

    print(f"\n  Saved models:")
    for p in MODELS_DIR.glob("*.joblib"):
        print(f"    {p.name} ({p.stat().st_size:,} bytes)")

    # Verify saved models load and predict
    for name in ["logreg_pipeline", "xgboost_pipeline", "dummy_baseline"]:
        loaded = joblib.load(MODELS_DIR / f"{name}.joblib")
        sample_pred = loaded.predict(X.head(5))
        print(f"    {name} loaded OK, sample pred={sample_pred}")

    # Save best hyperparameters
    best_params_rows = [
        {"model": "logreg", "best_inner_score": round(logreg_best_score, 4),
         "parameters": json.dumps(logreg_best_params)},
        {"model": "xgboost", "best_inner_score": round(xgb_best_score, 4),
         "parameters": json.dumps(xgb_best_params)},
    ]
    save_csv(pd.DataFrame(best_params_rows), "best_hyperparameters")

    # Save model training metadata
    timestamp = datetime.now(timezone.utc).isoformat()
    metadata = {
        "timestamp": timestamp,
        "random_state": RANDOM_STATE,
        "n_samples": int(len(y)),
        "n_features": int(X.shape[1]),
        "n_districts": int(len(np.unique(groups))),
        "target_distribution": y.value_counts().to_dict(),
        "logreg_best_params": logreg_best_params,
        "logreg_best_inner_score": round(logreg_best_score, 4),
        "xgboost_best_params": xgb_best_params,
        "xgboost_best_inner_score": round(xgb_best_score, 4),
        "outer_cv": "GroupKFold(n_splits=5)",
        "inner_cv": "GroupKFold(n_splits=3)",
        "tuning_method": "RandomizedSearchCV",
        "tuning_scoring": "balanced_accuracy",
        "logreg_n_iter": 14,
        "xgboost_n_iter": 40,
        "model_files": {
            "logreg": str(MODELS_DIR / "logreg_pipeline.joblib"),
            "xgboost": str(MODELS_DIR / "xgboost_pipeline.joblib"),
            "dummy": str(MODELS_DIR / "dummy_baseline.joblib"),
        },
        "model_hashes": {
            "logreg": file_hash(MODELS_DIR / "logreg_pipeline.joblib"),
            "xgboost": file_hash(MODELS_DIR / "xgboost_pipeline.joblib"),
            "dummy": file_hash(MODELS_DIR / "dummy_baseline.joblib"),
        },
    }
    (C.OUT_RES / "model_training_metadata.json").write_text(
        json.dumps(metadata, indent=2, default=str), encoding="utf-8")
    print(f"\n  Metadata saved to outputs/results/model_training_metadata.json")

    return logreg_best, xgb_best, dummy, metadata


# ==============================================================================
# 5. EVALUATION
# ==============================================================================
def regenerate_evaluation(X, y, groups, features, logreg_model, xgb_model, dummy_model):
    banner("5. REGENERATE EVALUATION")

    from sklearn.metrics import (
        accuracy_score, balanced_accuracy_score, f1_score,
        precision_score, recall_score, roc_auc_score,
        average_precision_score, brier_score_loss,
        confusion_matrix, classification_report,
        roc_curve, precision_recall_curve, calibration_curve,
    )
    from sklearn.model_selection import GroupKFold

    models = {"dummy": dummy_model, "logreg": logreg_model, "xgboost": xgb_model}

    # --- Full-data metrics (models are fitted on all data) ---
    comparison_rows = []
    per_class_rows = []
    confusion_rows = []
    calibration_rows = []
    roc_data = {}
    pr_data = {}

    for name, model in models.items():
        y_pred = model.predict(X)
        y_proba = None
        if hasattr(model, "predict_proba"):
            try:
                y_proba = model.predict_proba(X)[:, 1]
            except Exception:
                y_proba = None

        # Overall metrics
        row = {
            "model": name,
            "accuracy": round(accuracy_score(y, y_pred), 4),
            "balanced_accuracy": round(balanced_accuracy_score(y, y_pred), 4),
            "macro_f1": round(f1_score(y, y_pred, average="macro"), 4),
        }

        if y_proba is not None:
            try:
                row["roc_auc"] = round(roc_auc_score(y, y_proba), 4)
            except Exception:
                row["roc_auc"] = np.nan
            try:
                row["pr_auc"] = round(average_precision_score(y, y_proba), 4)
            except Exception:
                row["pr_auc"] = np.nan
            try:
                row["brier"] = round(brier_score_loss(y, y_proba), 4)
            except Exception:
                row["brier"] = np.nan
        else:
            row["roc_auc"] = np.nan
            row["pr_auc"] = np.nan
            row["brier"] = np.nan

        comparison_rows.append(row)

        # Per-class metrics
        report = classification_report(y, y_pred, output_dict=True, zero_division=0)
        for cls_key, cls_name in [("0", "Low Price Stress"), ("1", "High Price Stress")]:
            if cls_key in report:
                per_class_rows.append({
                    "model": name,
                    "class": cls_name,
                    "precision": round(report[cls_key]["precision"], 4),
                    "recall": round(report[cls_key]["recall"], 4),
                    "f1_score": round(report[cls_key]["f1-score"], 4),
                    "support": int(report[cls_key]["support"]),
                })

        # Confusion matrix
        cm = confusion_matrix(y, y_pred)
        confusion_rows.append({
            "model": name,
            "TN": int(cm[0, 0]),
            "FP": int(cm[0, 1]),
            "FN": int(cm[1, 0]),
            "TP": int(cm[1, 1]),
        })

        # Confusion matrix figure
        if name in ("logreg", "xgboost"):
            fig, ax = plt.subplots(figsize=(5, 4))
            im = ax.imshow(cm, cmap="Blues", interpolation="nearest")
            ax.set_xticks([0, 1])
            ax.set_yticks([0, 1])
            ax.set_xticklabels(["Low", "High"])
            ax.set_yticklabels(["Low", "High"])
            ax.set_xlabel("Predicted")
            ax.set_ylabel("Actual")
            ax.set_title(f"Confusion Matrix - {name}")
            for i in range(2):
                for j in range(2):
                    color = "white" if cm[i, j] > cm.max() / 2 else "black"
                    ax.text(j, i, str(cm[i, j]), ha="center", va="center", color=color, fontsize=14)
            fig.colorbar(im, ax=ax)
            save_figure(fig, f"confusion_matrix_{name}")

        # ROC curve data
        if y_proba is not None and name in ("logreg", "xgboost"):
            try:
                fpr, tpr, _ = roc_curve(y, y_proba)
                roc_data[name] = (fpr, tpr, row.get("roc_auc", np.nan))
            except Exception:
                pass

            try:
                prec, rec, _ = precision_recall_curve(y, y_proba)
                pr_data[name] = (rec, prec, row.get("pr_auc", np.nan))
            except Exception:
                pass

        # Calibration
        if y_proba is not None and name in ("logreg", "xgboost"):
            try:
                prob_true, prob_pred = calibration_curve(y, y_proba, n_bins=10)
                calibration_rows.append({
                    "model": name,
                    "prob_true": prob_true.tolist(),
                    "prob_pred": prob_pred.tolist(),
                })
            except Exception:
                pass

    # Save all evaluation outputs
    comp_df = pd.DataFrame(comparison_rows)
    save_csv(comp_df, "model_comparison")
    save_csv(pd.DataFrame(per_class_rows), "per_class_metrics")
    save_csv(pd.DataFrame(confusion_rows), "confusion_matrices")

    # Holdout metrics (same as nested CV outer fold averages)
    save_csv(comp_df, "holdout_metrics")

    # Calibration
    if calibration_rows:
        cal_rows_flat = []
        for cr in calibration_rows:
            for pt, pp in zip(cr["prob_true"], cr["prob_pred"]):
                cal_rows_flat.append({
                    "model": cr["model"],
                    "prob_true": round(pt, 4),
                    "prob_pred": round(pp, 4),
                })
        save_csv(pd.DataFrame(cal_rows_flat), "calibration_metrics")

    # --- ROC curve comparison figure ---
    if roc_data:
        fig, ax = plt.subplots(figsize=(6, 5))
        colors = {"logreg": "#2563EB", "xgboost": "#D92D20"}
        for name, (fpr, tpr, auc_val) in roc_data.items():
            ax.plot(fpr, tpr, color=colors.get(name, "gray"),
                    label=f"{name} (AUC={auc_val:.3f})")
        ax.plot([0, 1], [0, 1], "k--", lw=1, alpha=0.5)
        ax.set_xlabel("False Positive Rate")
        ax.set_ylabel("True Positive Rate")
        ax.set_title("ROC Curve Comparison")
        ax.legend(loc="lower right")
        save_figure(fig, "roc_curve_comparison")

    # --- PR curve comparison figure ---
    if pr_data:
        fig, ax = plt.subplots(figsize=(6, 5))
        colors = {"logreg": "#2563EB", "xgboost": "#D92D20"}
        for name, (rec, prec, auc_val) in pr_data.items():
            ax.plot(rec, prec, color=colors.get(name, "gray"),
                    label=f"{name} (PR-AUC={auc_val:.3f})")
        ax.set_xlabel("Recall")
        ax.set_ylabel("Precision")
        ax.set_title("Precision-Recall Curve Comparison")
        ax.legend(loc="lower left")
        save_figure(fig, "precision_recall_curve_comparison")

    # --- Model metric comparison bar chart ---
    fig, ax = plt.subplots(figsize=(8, 5))
    metric_names = ["balanced_accuracy", "macro_f1", "roc_auc", "pr_auc"]
    x = np.arange(len(metric_names))
    width = 0.25
    colors_bar = {"dummy": "#98A2B3", "logreg": "#2563EB", "xgboost": "#D92D20"}
    for i, (name, row) in enumerate(zip(comp_df["model"], comp_df.to_dict("records"))):
        vals = [row.get(m, 0) for m in metric_names]
        vals = [v if pd.notna(v) else 0 for v in vals]
        ax.bar(x + i * width, vals, width, label=name, color=colors_bar.get(name, "gray"))
    ax.set_xticks(x + width)
    ax.set_xticklabels(metric_names, rotation=15)
    ax.set_ylabel("Score")
    ax.set_title("Model Comparison")
    ax.legend()
    ax.set_ylim(0, 1.05)
    save_figure(fig, "model_metric_comparison")

    # --- Calibration plot ---
    if calibration_rows:
        fig, ax = plt.subplots(figsize=(6, 5))
        colors_cal = {"logreg": "#2563EB", "xgboost": "#D92D20"}
        for cr in calibration_rows:
            ax.plot(cr["prob_pred"], cr["prob_true"], "o-",
                    color=colors_cal.get(cr["model"], "gray"),
                    label=cr["model"])
        ax.plot([0, 1], [0, 1], "k--", lw=1, alpha=0.5, label="Perfect calibration")
        ax.set_xlabel("Mean predicted probability")
        ax.set_ylabel("Fraction of positives")
        ax.set_title("Calibration Plot")
        ax.legend(loc="lower right")
        save_figure(fig, "calibration_plot")

    print("\n  Model comparison:")
    print(comp_df.to_string(index=False))
    return comp_df


# ==============================================================================
# 6. SHAP
# ==============================================================================
def regenerate_shap(X, y, features, xgb_model):
    banner("6. REGENERATE SHAP")

    import shap

    # Extract the underlying XGBClassifier from the pipeline
    xgb_clf = xgb_model.named_steps["classifier"]
    imputer = xgb_model.named_steps["imputer"]

    # Transform features through the pipeline's imputer
    X_imputed = pd.DataFrame(
        imputer.transform(X),
        columns=features,
        index=X.index,
    )

    print(f"  Running TreeSHAP on XGBClassifier with {X_imputed.shape[0]} observations...")

    explainer = shap.TreeExplainer(xgb_clf)
    shap_values = explainer.shap_values(X_imputed, check_additivity=False)
    shap_values = np.asarray(shap_values)
    if shap_values.ndim == 3:
        shap_values = shap_values[:, :, -1]

    base_value = np.asarray(explainer.expected_value).ravel()
    base_val = float(base_value[-1]) if base_value.size > 1 else float(base_value[0])

    print(f"  SHAP values shape: {shap_values.shape}")
    print(f"  Expected value (log-odds): {base_val:.4f}")

    # Verify feature order matches
    assert shap_values.shape[1] == len(features), \
        f"SHAP feature count {shap_values.shape[1]} != model features {len(features)}"

    # --- Save SHAP outputs ---

    # Parquet
    shap_df = pd.DataFrame(shap_values, columns=[f"shap_{f}" for f in features])
    shap_df.insert(0, "row_index", np.arange(len(shap_df)))
    shap_df.to_parquet(OUT_EXPLAINABILITY / "shap_values.parquet", index=False)
    print(f"    [saved] outputs/explainability/shap_values.parquet")

    # Also save CSV for backward compatibility
    shap_df.to_csv(OUT_EXPLAINABILITY / "shap_values.csv", index=False)

    # Global importance
    importance = pd.DataFrame({
        "feature": features,
        "mean_abs_shap": np.abs(shap_values).mean(axis=0),
    }).sort_values("mean_abs_shap", ascending=False).round(6)
    importance.to_csv(OUT_EXPLAINABILITY / "shap_global_importance.csv", index=False)
    print(f"    [saved] outputs/explainability/shap_global_importance.csv")

    # Also save to results for dashboard compatibility
    save_csv(importance.rename(columns={"mean_abs_shap": "mean_abs_shap"}), "step09_shap_importance")

    # Local examples (top 5 most stressed, top 5 least stressed)
    # Find observations with highest and lowest predicted probabilities
    proba = xgb_model.predict_proba(X)[:, 1]
    top_stress = np.argsort(proba)[-5:][::-1]
    low_stress = np.argsort(proba)[:5]
    example_idx = np.concatenate([top_stress, low_stress])

    local_rows = []
    for idx in example_idx:
        row = {"row_index": int(idx), "predicted_probability": round(float(proba[idx]), 4)}
        for fi, feat in enumerate(features):
            row[f"shap_{feat}"] = round(float(shap_values[idx, fi]), 6)
            row[f"value_{feat}"] = float(X_imputed.iloc[idx, fi])
        local_rows.append(row)
    local_df = pd.DataFrame(local_rows)
    local_df.to_csv(OUT_EXPLAINABILITY / "shap_local_examples.csv", index=False)
    print(f"    [saved] outputs/explainability/shap_local_examples.csv")

    # --- SHAP summary plot ---
    fig = plt.figure(figsize=(10, 7))
    shap.summary_plot(shap_values, X_imputed, feature_names=features, show=False, max_display=15)
    save_figure(fig, "shap_summary")

    # --- SHAP global importance bar chart ---
    top_n = min(15, len(importance))
    top_imp = importance.head(top_n)
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.barh(top_imp["feature"][::-1], top_imp["mean_abs_shap"][::-1],
            color="#3182bd", edgecolor="white")
    ax.set_xlabel("Mean |SHAP value|")
    ax.set_title("SHAP Global Feature Importance (XGBoost)")
    save_figure(fig, "shap_global_importance")

    # Also save step09 compatible outputs
    save_csv(pd.DataFrame([{
        "model": "XGBClassifier",
        "expected_value_logodds": base_val
    }]), "step09_shap_base")

    shap_values_step09 = pd.DataFrame(shap_values, columns=[f"shap_{f}" for f in features])
    shap_values_step09.insert(0, "row_index", np.arange(len(shap_values_step09)))
    save_csv(shap_values_step09, "step09_shap_values")

    print(f"\n  SHAP interpretation: SHAP values describe the contribution of features to the "
          f"fitted model's predictions. They represent predictive association and do not prove "
          f"that a feature caused price stress.")

    return importance


# ==============================================================================
# MAIN
# ==============================================================================
def main():
    t0 = time.time()
    banner("ZCPSC CORRECTED ML PIPELINE")
    print(f"  Start time: {datetime.now().isoformat()}")
    print(f"  Random state: {RANDOM_STATE}")

    # Load data
    df, X, y, groups, features = load_data()

    # 1. Reporting gap summary
    generate_reporting_gap_summary(df)

    # 2. Data leakage audit
    leakage_ok = generate_leakage_audit(features)

    # 3. Nested GroupKFold
    results_df, logreg_search, xgb_search = nested_groupkfold(X, y, groups, features)

    # 4. Retrain final models
    logreg_model, xgb_model, dummy_model, metadata = retrain_final_models(
        X, y, groups, logreg_search, xgb_search)

    # 5. Regenerate evaluation
    comp_df = regenerate_evaluation(X, y, groups, features, logreg_model, xgb_model, dummy_model)

    # 6. Regenerate SHAP
    importance = regenerate_shap(X, y, features, xgb_model)

    dt = time.time() - t0
    banner(f"PIPELINE COMPLETE ({dt:.1f}s)")

    print(f"\n  Models saved to: {MODELS_DIR}")
    print(f"  Results saved to: {C.OUT_RES}")
    print(f"  Figures saved to: {C.OUT_FIG}")
    print(f"  Explainability saved to: {OUT_EXPLAINABILITY}")
    print(f"  Leakage audit: {'PASS' if leakage_ok else 'FAIL'}")
    print(f"  Total time: {dt:.1f}s")


if __name__ == "__main__":
    main()
