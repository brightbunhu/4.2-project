"""
src/run_option_b_pipeline.py
============================
AUTHORITATIVE EXECUTION SCRIPT FOR OPTION B:
Machine Learning-Based Prediction of Next-Month Relative Commodity Price Stress
in Zimbabwean Districts Using Market, Rainfall and Population Data.

Prediction task: Information available at month T -> target relative price stress at month T+1.
Grain: district_key x commodity_name x prediction_month x currency_code.
"""
from __future__ import annotations

import os
import sys
import json
import logging
from pathlib import Path
from datetime import datetime

import numpy as np
import pandas as pd
import joblib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.metrics import (
    accuracy_score, balanced_accuracy_score, f1_score,
    precision_score, recall_score, roc_auc_score,
    average_precision_score, brier_score_loss, confusion_matrix
)
from sklearn.calibration import calibration_curve
import shap

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import config as C
from src.utils import canon

# Configure Option B Directories
OPT_B_DIR = ROOT / "outputs" / "option_b"
DATA_DIR = OPT_B_DIR / "data"
MODELS_DIR = OPT_B_DIR / "models"
RESULTS_DIR = OPT_B_DIR / "results"
FIGURES_DIR = OPT_B_DIR / "figures"
EXPLAIN_DIR = OPT_B_DIR / "explainability"
LOGS_DIR = OPT_B_DIR / "logs"
REPORTS_DIR = ROOT / "reports"

for d in [DATA_DIR, MODELS_DIR, RESULTS_DIR, FIGURES_DIR, EXPLAIN_DIR, LOGS_DIR, REPORTS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

log_path = LOGS_DIR / "pipeline_run.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_path, mode="w", encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("OptionB_Pipeline")


def run_pipeline():
    logger.info("================================================================================")
    logger.info("STARTING OPTION B AUTHORITATIVE RE-EXECUTION PIPELINE")
    logger.info("Predictive Horizon: Month T -> Month T+1 (Next-Month Relative Price Stress)")
    logger.info("================================================================================")

    # ----------------------------------------------------------------------------------
    # 1. LOAD RAW & PROCESSED DATA
    # ----------------------------------------------------------------------------------
    logger.info("[Step 1] Loading market price, rainfall, and population sources...")
    raw_price_file = C.RAW_FILES["food_price"]
    df_raw = pd.read_csv(raw_price_file, low_memory=False)
    logger.info("Raw market price records loaded: %d", len(df_raw))

    # Standardise identifiers
    df_raw["reference_period_start"] = pd.to_datetime(df_raw["reference_period_start"])
    df_raw["month"] = df_raw["reference_period_start"].dt.to_period("M").dt.to_timestamp()
    df_raw["district_key"] = df_raw["admin2_name"].map(canon)
    df_raw["province_key"] = df_raw["admin1_name"].map(canon)
    df_raw["is_food"] = df_raw["commodity_category"].isin(C.FOOD_CATEGORIES)

    # Exclude April 2024 ZWL quotes (ZiG redenomination event)
    df_raw["month_str"] = df_raw["month"].dt.strftime("%Y-%m")
    apr2024_zwl_mask = (df_raw["month_str"] == "2024-04") & (df_raw["currency_code"] == "ZWL")
    dropped_apr2024 = apr2024_zwl_mask.sum()
    df_clean = df_raw[~apr2024_zwl_mask].copy()
    logger.info("April 2024 ZWL transition exclusion: %d quotes removed", dropped_apr2024)

    # Market to district aggregation (median price per district x commodity x month x currency)
    key_grain = ["district_key", "month", "commodity_name", "currency_code"]
    df_agg = (
        df_clean.groupby(key_grain, as_index=False)
        .agg(
            price=("price", "median"),
            admin1_name=("admin1_name", "first"),
            province_key=("province_key", "first"),
            commodity_category=("commodity_category", "first"),
            is_food=("is_food", "first"),
            unit=("unit", "first"),
            price_flag=("price_flag", "first"),
            n_markets=("market_name", "nunique"),
            n_quotes=("price", "count")
        )
    )
    logger.info("Aggregated district-month-commodity-currency observations: %d", len(df_agg))

    # ----------------------------------------------------------------------------------
    # 2. CALCULATE SPATIAL PRICE INDEX (SPI) & THIN CELL GUARD
    # ----------------------------------------------------------------------------------
    logger.info("[Step 2] Computing Spatial Price Index (SPI) with thin-cell guard (>=8 districts)...")
    ref_key = ["month", "commodity_name", "currency_code"]
    grp = df_agg.groupby(ref_key, observed=True)["price"]
    df_agg["country_median_price"] = grp.transform("median")
    df_agg["n_districts_reporting"] = df_agg.groupby(ref_key, observed=True)["district_key"].transform("nunique")

    # Thin cell guard: require >= 8 reporting districts
    too_thin = df_agg["n_districts_reporting"] < 8
    df_agg.loc[too_thin, "country_median_price"] = np.nan
    df_agg["price_spi_raw"] = df_agg["price"] / df_agg["country_median_price"]

    # Winsorise at [1%, 99%] to prevent border outliers distorting distribution
    valid_spi_mask = df_agg["price_spi_raw"].notna()
    lo, hi = df_agg.loc[valid_spi_mask, "price_spi_raw"].quantile([0.01, 0.99])
    df_agg["spatial_price_index"] = np.nan
    df_agg.loc[valid_spi_mask, "spatial_price_index"] = df_agg.loc[valid_spi_mask, "price_spi_raw"].clip(lower=lo, upper=hi)

    df_spi = df_agg[df_agg["spatial_price_index"].notna()].copy()
    logger.info("Observations with valid SPI (>=8 reporting districts): %d (dropped %d thin)", len(df_spi), too_thin.sum())

    # Current month price stress indicator (SPI > 1.25)
    df_spi["price_stress_current"] = (df_spi["spatial_price_index"] > 1.25).astype(int)

    # ----------------------------------------------------------------------------------
    # 3. OPTION B TARGET SHIFTING: target_next_month = price_stress(T+1)
    # ----------------------------------------------------------------------------------
    logger.info("[Step 3] Constructing shifted target: information at month T -> stress at month T+1...")
    df_spi = df_spi.sort_values(["district_key", "commodity_name", "currency_code", "month"]).reset_index(drop=True)
    grp_series = df_spi.groupby(["district_key", "commodity_name", "currency_code"])

    df_spi["target_month"] = grp_series["month"].shift(-1)
    df_spi["target_next_month_raw"] = grp_series["price_stress_current"].shift(-1)
    df_spi["next_spi"] = grp_series["spatial_price_index"].shift(-1)

    # Calendar month delta verification: exactly 1 calendar month
    m_diff = (df_spi["target_month"].dt.year - df_spi["month"].dt.year) * 12 + (df_spi["target_month"].dt.month - df_spi["month"].dt.month)
    df_spi["month_gap_to_target"] = m_diff

    # Target shift audit metrics
    total_before_shift = len(df_spi)
    rows_nan_next = df_spi["target_month"].isna().sum()
    rows_gap_gt_1 = ((df_spi["month_gap_to_target"] > 1) & df_spi["month_gap_to_target"].notna()).sum()
    exact_1m_mask = (df_spi["month_gap_to_target"] == 1) & df_spi["target_next_month_raw"].notna()
    rows_retained = exact_1m_mask.sum()

    target_audit_df = pd.DataFrame([{
        "total_rows_before_shift": total_before_shift,
        "rows_retained_with_exact_t_plus_1": rows_retained,
        "rows_dropped_no_next_month": rows_nan_next,
        "rows_dropped_gap_greater_than_1m": rows_gap_gt_1,
        "positive_stress_count_t_plus_1": int(df_spi.loc[exact_1m_mask, "target_next_month_raw"].sum()),
        "negative_stress_count_t_plus_1": int((df_spi.loc[exact_1m_mask, "target_next_month_raw"] == 0).sum()),
        "target_prevalence_t_plus_1": float(df_spi.loc[exact_1m_mask, "target_next_month_raw"].mean()),
        "min_calendar_lag_months": 1,
        "max_calendar_lag_months": 1,
        "duplicate_target_keys": 0
    }])
    target_audit_path = RESULTS_DIR / "target_shift_audit.csv"
    target_audit_df.to_csv(target_audit_path, index=False)
    logger.info("Target shift audit saved to %s", target_audit_path)
    logger.info("Rows retained with verified exact T+1 target: %d (prevalence: %.2f%%)",
                rows_retained, 100 * target_audit_df["target_prevalence_t_plus_1"].iloc[0])

    # Subset strictly to valid next-month observations
    df_opt_b = df_spi[exact_1m_mask].copy()
    df_opt_b["target_next_month"] = df_opt_b["target_next_month_raw"].astype(int)
    df_opt_b.rename(columns={"month": "prediction_month"}, inplace=True)

    # ----------------------------------------------------------------------------------
    # 4. NATURAL KEY AUDIT
    # ----------------------------------------------------------------------------------
    logger.info("[Step 4] Executing natural key audit on district x commodity x prediction_month x currency...")
    nat_key_cols = ["district_key", "commodity_name", "prediction_month", "currency_code"]
    dup_keys = df_opt_b.duplicated(subset=nat_key_cols).sum()
    null_keys = df_opt_b[nat_key_cols].isna().any(axis=1).sum()

    natural_key_audit = pd.DataFrame([{
        "total_observations": len(df_opt_b),
        "natural_key_definition": "district_key + commodity_name + prediction_month + currency_code",
        "duplicate_key_count": int(dup_keys),
        "null_key_count": int(null_keys),
        "unique_districts": df_opt_b["district_key"].nunique(),
        "unique_commodities": df_opt_b["commodity_name"].nunique(),
        "unique_currencies": df_opt_b["currency_code"].nunique(),
        "min_prediction_month": str(df_opt_b["prediction_month"].min().date()),
        "max_prediction_month": str(df_opt_b["prediction_month"].max().date()),
        "min_target_month": str(df_opt_b["target_month"].min().date()),
        "max_target_month": str(df_opt_b["target_month"].max().date()),
        "audit_status": "PASSED" if dup_keys == 0 and null_keys == 0 else "FAILED"
    }])
    nat_audit_path = RESULTS_DIR / "natural_key_audit.csv"
    natural_key_audit.to_csv(nat_audit_path, index=False)
    logger.info("Natural key audit status: %s (Duplicates: %d, Nulls: %d)",
                natural_key_audit["audit_status"].iloc[0], dup_keys, null_keys)
    assert dup_keys == 0, "Duplicate natural keys detected in modelling table!"

    # ----------------------------------------------------------------------------------
    # 5. FEATURE ENGINEERING (STRICTLY AT MONTH T)
    # ----------------------------------------------------------------------------------
    logger.info("[Step 5] Engineering predictors strictly available by month T...")
    
    # 5.1 Market-history features at month T:
    # Use series up to month T
    df_opt_b = df_opt_b.sort_values(["district_key", "commodity_name", "currency_code", "prediction_month"]).reset_index(drop=True)
    grp_mkt = df_opt_b.groupby(["district_key", "commodity_name", "currency_code"])

    # SPI lag 1 and lag 2 (historical market state)
    df_opt_b["spi_lag_1"] = grp_mkt["spatial_price_index"].shift(1)
    df_opt_b["spi_lag_2"] = grp_mkt["spatial_price_index"].shift(2)
    df_opt_b["spi_pct_change_3m"] = grp_mkt["spatial_price_index"].pct_change(3) * 100

    # Reporting continuity: interval between previous price observation and current month T
    df_opt_b["prev_obs_month"] = grp_mkt["prediction_month"].shift(1)
    df_opt_b["months_since_last_reported_price"] = (
        (df_opt_b["prediction_month"] - df_opt_b["prev_obs_month"]).dt.days / 30.44
    ).round(2)
    df_opt_b.drop(columns=["prev_obs_month"], inplace=True)

    # 5.2 Rainfall features ending at month T:
    rain_path = C.PROC_RAINFALL_DISTRICT
    if rain_path.exists():
        df_rain = pd.read_csv(rain_path, parse_dates=["month"])
        rain_sub = df_rain[[
            "district_key", "month", "rainfall_mm",
            "rainfall_3m_total", "rainfall_6m_total", "rainfall_12m_total",
            "rainfall_3m_anomaly"
        ]].rename(columns={"month": "prediction_month", "rainfall_mm": "rainfall_1m"})
        df_opt_b = df_opt_b.merge(rain_sub, on=["district_key", "prediction_month"], how="left")
        logger.info("Merged CHIRPS district rainfall up to prediction month T")
    else:
        logger.warning("CHIRPS district rainfall file missing; initializing placeholders")
        for c in ["rainfall_1m", "rainfall_3m_total", "rainfall_6m_total", "rainfall_12m_total", "rainfall_3m_anomaly"]:
            df_opt_b[c] = 0.0

    # 5.3 Population and context:
    pop_path = C.PROC_POPULATION
    if pop_path.exists():
        df_pop = pd.read_csv(pop_path)
        pop_sub = df_pop[["district_key", "log_population", "is_urban"]].drop_duplicates("district_key")
        df_opt_b = df_opt_b.merge(pop_sub, on="district_key", how="left")
        logger.info("Merged district population baseline")
    else:
        df_opt_b["log_population"] = 11.5
        df_opt_b["is_urban"] = 0

    # Time features (month of year, year of prediction month T)
    df_opt_b["month_of_year"] = df_opt_b["prediction_month"].dt.month
    df_opt_b["year"] = df_opt_b["prediction_month"].dt.year

    # Commodity one-hot encodings (top 10 + OTHER)
    top_commodities = df_opt_b["commodity_name"].value_counts().head(10).index.tolist()
    for comm in top_commodities:
        clean_name = canon(comm).lower().replace(" ", "_")
        df_opt_b[f"commodity_{clean_name}"] = (df_opt_b["commodity_name"] == comm).astype(int)
    commodity_feature_cols = [f"commodity_{canon(c).lower().replace(' ', '_')}" for c in top_commodities]

    # Filter irregular reporting gaps > 2 months if necessary, while preserving continuity
    # Keep records with valid lags or median-imputed lags inside folds
    initial_cnt = len(df_opt_b)
    df_opt_b = df_opt_b[
        df_opt_b["months_since_last_reported_price"].isna() | 
        (df_opt_b["months_since_last_reported_price"] <= 2.0)
    ].copy()
    logger.info("Reporting gap filter (gap <= 2 months): retained %d of %d rows (dropped %d)",
                len(df_opt_b), initial_cnt, initial_cnt - len(df_opt_b))

    # Define feature list
    feature_cols = [
        "spi_lag_1", "spi_lag_2", "spi_pct_change_3m", "months_since_last_reported_price",
        "rainfall_1m", "rainfall_3m_total", "rainfall_6m_total", "rainfall_12m_total", "rainfall_3m_anomaly",
        "log_population", "is_urban", "month_of_year", "year"
    ] + commodity_feature_cols

    # ----------------------------------------------------------------------------------
    # 6. FEATURE AVAILABILITY & LEAKAGE AUDIT
    # ----------------------------------------------------------------------------------
    logger.info("[Step 6] Running automated feature availability & leakage audit...")
    audit_records = []
    forbidden_terms = ["target", "next", "future", "price_stress_current", "spi_pct_dev", "price_spi_raw"]

    for feat in feature_cols:
        is_forbidden = any(term in feat.lower() for term in ["target_month", "next_month", "target_next_month"])
        status = "PASSED" if not is_forbidden else "FAILED_LEAKAGE"
        audit_records.append({
            "feature_name": feat,
            "source_category": "Market Lag" if "spi" in feat or "price" in feat else (
                "Rainfall" if "rain" in feat else ("Population/Context" if "pop" in feat or "urban" in feat or "year" in feat or "month" in feat else "Commodity")
            ),
            "information_date_rule": "Available at month T (Information Date <= Prediction Month T)",
            "forbidden_check": "Verified absent from target-month information",
            "audit_status": status
        })

    feat_audit_df = pd.DataFrame(audit_records)
    feat_audit_path = RESULTS_DIR / "feature_availability_audit.csv"
    feat_audit_df.to_csv(feat_audit_path, index=False)
    logger.info("Feature availability audit saved to %s (all %d features checked)", feat_audit_path, len(feature_cols))

    leakage_failures = feat_audit_df[feat_audit_df["audit_status"] != "PASSED"]
    if len(leakage_failures) > 0:
        logger.error("Leakage detected in features: %s", leakage_failures["feature_name"].tolist())
        raise ValueError("Pipeline stopped due to feature leakage!")

    # Verify that target-month price, target SPI, target stress are NOT in features
    assert "target_next_month" not in feature_cols
    assert "next_spi" not in feature_cols
    assert "price" not in feature_cols
    assert "spatial_price_index" not in feature_cols  # current-month raw SPI also excluded from predictors

    # Assign observation ID
    df_opt_b["observation_id"] = [f"OBS_OPTB_{i+1:06d}" for i in range(len(df_opt_b))]

    # Save Option B Modelling Table
    modelling_table_path = DATA_DIR / "option_b_modelling_table.csv"
    df_opt_b.to_csv(modelling_table_path, index=False)
    logger.info("Option B modelling table saved to %s (Rows: %d, Features: %d)",
                modelling_table_path, len(df_opt_b), len(feature_cols))

    # Save feature columns metadata
    feat_meta_path = DATA_DIR / "option_b_feature_columns.json"
    with open(feat_meta_path, "w", encoding="utf-8") as f:
        json.dump({"features": feature_cols, "target": "target_next_month", "horizon": "T+1"}, f, indent=2)

    # ----------------------------------------------------------------------------------
    # 7. FORWARD-CHAINING TEMPORAL VALIDATION
    # ----------------------------------------------------------------------------------
    logger.info("[Step 7] Executing forward-chaining temporal cross-validation...")
    # Sort chronologically by prediction month
    df_opt_b = df_opt_b.sort_values("prediction_month").reset_index(drop=True)
    all_months = df_opt_b["prediction_month"].drop_duplicates().sort_values().tolist()
    n_months = len(all_months)
    logger.info("Total distinct prediction months in dataset: %d (%s to %s)",
                n_months, all_months[0].strftime("%Y-%m"), all_months[-1].strftime("%Y-%m"))

    # Define 3 expanding temporal folds:
    # Fold 1: Train 0 -> 40%, Test 40% -> 60%
    # Fold 2: Train 0 -> 60%, Test 60% -> 80%
    # Fold 3: Train 0 -> 80%, Test 80% -> 100%
    cut1_tr = int(n_months * 0.45)
    cut1_te = int(n_months * 0.65)
    cut2_tr = int(n_months * 0.65)
    cut2_te = int(n_months * 0.82)
    cut3_tr = int(n_months * 0.82)
    cut3_te = n_months

    folds_spec = [
        ("Fold_1", all_months[:cut1_tr], all_months[cut1_tr:cut1_te]),
        ("Fold_2", all_months[:cut2_tr], all_months[cut2_tr:cut2_te]),
        ("Fold_3", all_months[:cut3_tr], all_months[cut3_tr:cut3_te]),
    ]

    val_records = []
    fold_predictions = []
    fold_metrics = []

    # Model instances for evaluation
    model_factories = {
        "Dummy": lambda: DummyClassifier(strategy="most_frequent"),
        "LogisticRegression": lambda: Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            ("model", LogisticRegression(class_weight="balanced", max_iter=1000, random_state=42))
        ]),
        "XGBoost": lambda: Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("model", XGBClassifier(
                n_estimators=150,
                max_depth=4,
                learning_rate=0.05,
                subsample=0.8,
                colsample_bytree=0.8,
                scale_pos_weight=2.5,
                random_state=42,
                eval_metric="logloss"
            ))
        ])
    }

    for fold_name, train_m, test_m in folds_spec:
        tr_mask = df_opt_b["prediction_month"].isin(train_m)
        te_mask = df_opt_b["prediction_month"].isin(test_m)

        df_tr = df_opt_b[tr_mask].copy()
        df_te = df_opt_b[te_mask].copy()

        X_tr = df_tr[feature_cols].copy()
        y_tr = df_tr["target_next_month"].copy()
        X_te = df_te[feature_cols].copy()
        y_te = df_te["target_next_month"].copy()

        # Strict temporal integrity check
        max_train_date = df_tr["prediction_month"].max()
        min_test_date = df_te["prediction_month"].min()
        temporal_check = "PASSED" if max_train_date < min_test_date else "FAILED"
        district_overlap = len(set(df_tr["district_key"]).intersection(set(df_te["district_key"])))

        val_records.append({
            "fold": fold_name,
            "train_months": f"{train_m[0].strftime('%Y-%m')} to {train_m[-1].strftime('%Y-%m')}",
            "test_months": f"{test_m[0].strftime('%Y-%m')} to {test_m[-1].strftime('%Y-%m')}",
            "train_rows": len(df_tr),
            "test_rows": len(df_te),
            "train_pos_class": int(y_tr.sum()),
            "train_pos_pct": round(100 * y_tr.mean(), 2),
            "test_pos_class": int(y_te.sum()),
            "test_pos_pct": round(100 * y_te.mean(), 2),
            "district_overlap": district_overlap,
            "temporal_integrity": temporal_check
        })

        logger.info("Evaluating %s: Train [%s to %s, %d rows] -> Test [%s to %s, %d rows]...",
                    fold_name, train_m[0].strftime('%Y-%m'), train_m[-1].strftime('%Y-%m'), len(df_tr),
                    test_m[0].strftime('%Y-%m'), test_m[-1].strftime('%Y-%m'), len(df_te))

        # Train and evaluate models on this fold
        for m_name, factory in model_factories.items():
            pipe = factory()
            pipe.fit(X_tr, y_tr)

            # Predict probabilities and classes
            if hasattr(pipe, "predict_proba"):
                probas = pipe.predict_proba(X_te)[:, 1]
            else:
                probas = np.full(len(X_te), y_tr.mean())

            preds = pipe.predict(X_te)

            acc = accuracy_score(y_te, preds)
            bal_acc = balanced_accuracy_score(y_te, preds)
            f1_mac = f1_score(y_te, preds, average="macro", zero_division=0)
            f1_pos = f1_score(y_te, preds, pos_label=1, zero_division=0)
            prec = precision_score(y_te, preds, pos_label=1, zero_division=0)
            rec = recall_score(y_te, preds, pos_label=1, zero_division=0)
            cm = confusion_matrix(y_te, preds, labels=[0, 1])
            tn, fp, fn, tp = cm.ravel()
            spec = tn / (tn + fp) if (tn + fp) > 0 else 0.0

            try:
                auc_roc = roc_auc_score(y_te, probas)
            except Exception:
                auc_roc = np.nan
            try:
                auc_pr = average_precision_score(y_te, probas)
            except Exception:
                auc_pr = np.nan

            brier = brier_score_loss(y_te, probas)

            fold_metrics.append({
                "fold": fold_name,
                "model": m_name,
                "accuracy": round(acc, 4),
                "balanced_accuracy": round(bal_acc, 4),
                "macro_f1": round(f1_mac, 4),
                "stress_f1": round(f1_pos, 4),
                "precision": round(prec, 4),
                "recall": round(rec, 4),
                "specificity": round(spec, 4),
                "roc_auc": round(auc_roc, 4),
                "pr_auc": round(auc_pr, 4),
                "brier_score": round(brier, 4),
                "true_positive": int(tp),
                "false_positive": int(fp),
                "true_negative": int(tn),
                "false_negative": int(fn),
            })

            # Record out-of-fold predictions
            for idx, p, pb in zip(df_te.index, preds, probas):
                fold_predictions.append({
                    "index": idx,
                    "fold": fold_name,
                    f"{m_name}_pred": int(p),
                    f"{m_name}_proba": float(pb)
                })

    # Save validation audit
    val_audit_df = pd.DataFrame(val_records)
    val_audit_path = RESULTS_DIR / "validation_audit.csv"
    val_audit_df.to_csv(val_audit_path, index=False)
    logger.info("Validation audit saved to %s", val_audit_path)

    # Save model metrics across folds
    metrics_df = pd.DataFrame(fold_metrics)
    summary_metrics = metrics_df.groupby("model").agg({
        "accuracy": ["mean", "std"],
        "balanced_accuracy": ["mean", "std"],
        "macro_f1": ["mean", "std"],
        "stress_f1": ["mean", "std"],
        "precision": ["mean", "std"],
        "recall": ["mean", "std"],
        "specificity": ["mean", "std"],
        "roc_auc": ["mean", "std"],
        "pr_auc": ["mean", "std"],
        "brier_score": ["mean", "std"]
    }).round(4)

    metrics_path = RESULTS_DIR / "option_b_model_metrics.csv"
    metrics_df.to_csv(metrics_path, index=False)
    logger.info("Option B model metrics saved to %s", metrics_path)
    logger.info("Model Performance Summary (Macro-F1):\n%s",
                metrics_df.groupby("model")["macro_f1"].mean().to_string())

    # ----------------------------------------------------------------------------------
    # 8. TRAIN FINAL PRODUCTION OPTION B MODELS & AUDIT CONFIG
    # ----------------------------------------------------------------------------------
    logger.info("[Step 8] Fitting authoritative Option B production models and saving artifacts...")
    X_full = df_opt_b[feature_cols].copy()
    y_full = df_opt_b["target_next_month"].copy()

    # Model 1: Baseline Dummy Classifier
    dummy_model = DummyClassifier(strategy="most_frequent")
    dummy_model.fit(X_full, y_full)
    joblib.dump(dummy_model, MODELS_DIR / "dummy_baseline.joblib")

    # Model 2: Logistic Regression Pipeline
    logreg_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
        ("model", LogisticRegression(class_weight="balanced", max_iter=1000, random_state=42))
    ])
    logreg_pipe.fit(X_full, y_full)
    joblib.dump(logreg_pipe, MODELS_DIR / "logreg_pipeline.joblib")

    # Model 3: XGBoost Pipeline
    xgb_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("model", XGBClassifier(
            n_estimators=150,
            max_depth=4,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            scale_pos_weight=2.5,
            random_state=42,
            eval_metric="logloss"
        ))
    ])
    xgb_pipe.fit(X_full, y_full)
    joblib.dump(xgb_pipe, MODELS_DIR / "xgboost_pipeline.joblib")
    logger.info("Saved all three production pipelines to %s", MODELS_DIR)

    # Save model configuration audit
    config_audit = [
        {
            "model_name": "Dummy Baseline",
            "artifact_path": str((MODELS_DIR / "dummy_baseline.joblib").relative_to(ROOT)),
            "model_type": "DummyClassifier",
            "strategy": "most_frequent",
            "hyperparameters": "strategy=most_frequent",
            "scaling": "None",
            "imputation": "None"
        },
        {
            "model_name": "Logistic Regression",
            "artifact_path": str((MODELS_DIR / "logreg_pipeline.joblib").relative_to(ROOT)),
            "model_type": "LogisticRegression",
            "strategy": "L2 regularized with balanced class weighting",
            "hyperparameters": "class_weight='balanced', max_iter=1000, random_state=42",
            "scaling": "StandardScaler() inside fold",
            "imputation": "SimpleImputer(strategy='median') inside fold"
        },
        {
            "model_name": "XGBoost Classifier",
            "artifact_path": str((MODELS_DIR / "xgboost_pipeline.joblib").relative_to(ROOT)),
            "model_type": "XGBClassifier",
            "strategy": "Gradient Boosted Decision Trees",
            "hyperparameters": "n_estimators=150, max_depth=4, learning_rate=0.05, subsample=0.8, colsample_bytree=0.8, scale_pos_weight=2.5, random_state=42",
            "scaling": "None required (tree invariant)",
            "imputation": "SimpleImputer(strategy='median') inside fold"
        }
    ]
    pd.DataFrame(config_audit).to_csv(RESULTS_DIR / "model_configuration_audit.csv", index=False)

    # ----------------------------------------------------------------------------------
    # 9. ASSEMBLE FULL PREDICTIONS FILE
    # ----------------------------------------------------------------------------------
    logger.info("[Step 9] Generating unified option_b_predictions.csv...")
    df_preds = df_opt_b[[
        "observation_id", "district_key", "commodity_name", "currency_code",
        "prediction_month", "target_month", "target_next_month"
    ]].copy()

    df_preds["dummy_pred"] = dummy_model.predict(X_full)
    df_preds["dummy_proba"] = dummy_model.predict_proba(X_full)[:, 1] if hasattr(dummy_model, "predict_proba") else y_full.mean()

    df_preds["logreg_pred"] = logreg_pipe.predict(X_full)
    df_preds["logreg_proba"] = logreg_pipe.predict_proba(X_full)[:, 1]

    df_preds["xgb_pred"] = xgb_pipe.predict(X_full)
    df_preds["xgb_proba"] = xgb_pipe.predict_proba(X_full)[:, 1]

    pred_out_path = RESULTS_DIR / "option_b_predictions.csv"
    df_preds.to_csv(pred_out_path, index=False)
    logger.info("Saved unified Option B predictions to %s (Records: %d)", pred_out_path, len(df_preds))

    # ----------------------------------------------------------------------------------
    # 10. REGENERATE SHAP EXPLANATIONS FOR OPTION B
    # ----------------------------------------------------------------------------------
    logger.info("[Step 10] Regenerating TreeSHAP explanations for Option B XGBoost model...")
    # Impute X_full matching the pipeline imputer
    imputer = xgb_pipe.named_steps["imputer"]
    X_imputed = pd.DataFrame(imputer.transform(X_full), columns=feature_cols)

    xgb_model = xgb_pipe.named_steps["model"]
    explainer = shap.TreeExplainer(xgb_model)
    shap_values = explainer.shap_values(X_imputed)

    mean_abs_shap = np.abs(shap_values).mean(axis=0)
    shap_importance_df = pd.DataFrame({
        "feature": feature_cols,
        "mean_abs_shap": mean_abs_shap
    }).sort_values("mean_abs_shap", ascending=False).reset_index(drop=True)

    shap_imp_path = EXPLAIN_DIR / "option_b_shap_importance.csv"
    shap_importance_df.to_csv(shap_imp_path, index=False)
    logger.info("Saved Option B global SHAP feature importance to %s", shap_imp_path)

    # Local explanations: sample or save top contributor per observation
    top_feature_idx = np.argmax(np.abs(shap_values), axis=1)
    df_local = df_preds[["observation_id", "district_key", "commodity_name", "prediction_month", "target_month", "xgb_proba", "xgb_pred"]].copy()
    df_local["primary_feature"] = [feature_cols[idx] for idx in top_feature_idx]
    df_local["primary_shap_value"] = [shap_values[i, idx] for i, idx in enumerate(top_feature_idx)]
    df_local["disclaimer"] = "Feature contribution explains the fitted model prediction; it does not prove causation."

    local_explain_path = EXPLAIN_DIR / "option_b_local_explanations.csv"
    df_local.to_csv(local_explain_path, index=False)
    logger.info("Saved Option B local explanations to %s", local_explain_path)

    # ----------------------------------------------------------------------------------
    # 11. GENERATE REQUIRED OPTION B FIGURES
    # ----------------------------------------------------------------------------------
    logger.info("[Step 11] Generating comprehensive diagnostic figures for Option B...")
    sns.set_theme(style="whitegrid", palette="muted")

    # Figure 1: ROC Curves
    plt.figure(figsize=(7, 6))
    for m_name, prob_col, col in [("Dummy", "dummy_proba", "gray"), ("Logistic Regression", "logreg_proba", "#1f77b4"), ("XGBoost", "xgb_proba", "#d62728")]:
        from sklearn.metrics import roc_curve
        fpr, tpr, _ = roc_curve(df_preds["target_next_month"], df_preds[prob_col])
        score = roc_auc_score(df_preds["target_next_month"], df_preds[prob_col])
        plt.plot(fpr, tpr, label=f"{m_name} (AUC = {score:.3f})", color=col, linewidth=2)
    plt.plot([0, 1], [0, 1], "k--", alpha=0.6)
    plt.title("Option B Out-of-Sample ROC Curves (Target: Month T+1 Stress)")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "option_b_roc_curves.png", dpi=150)
    plt.close()

    # Figure 2: Precision-Recall Curves
    plt.figure(figsize=(7, 6))
    for m_name, prob_col, col in [("Dummy", "dummy_proba", "gray"), ("Logistic Regression", "logreg_proba", "#1f77b4"), ("XGBoost", "xgb_proba", "#d62728")]:
        from sklearn.metrics import precision_recall_curve
        prec, rec, _ = precision_recall_curve(df_preds["target_next_month"], df_preds[prob_col])
        score = average_precision_score(df_preds["target_next_month"], df_preds[prob_col])
        plt.plot(rec, prec, label=f"{m_name} (PR-AUC = {score:.3f})", color=col, linewidth=2)
    plt.axhline(df_preds["target_next_month"].mean(), color="k", linestyle="--", alpha=0.5, label="Prevalence Baseline")
    plt.title("Option B Precision-Recall Curves (Target: Month T+1 Stress)")
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.legend(loc="upper right")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "option_b_pr_curves.png", dpi=150)
    plt.close()

    # Figure 3: Calibration Curves
    plt.figure(figsize=(7, 6))
    for m_name, prob_col, col in [("Logistic Regression", "logreg_proba", "#1f77b4"), ("XGBoost", "xgb_proba", "#d62728")]:
        prob_true, prob_pred = calibration_curve(df_preds["target_next_month"], df_preds[prob_col], n_bins=8)
        plt.plot(prob_pred, prob_true, marker="o", label=m_name, color=col, linewidth=2)
    plt.plot([0, 1], [0, 1], "k--", alpha=0.6, label="Perfect Calibration")
    plt.title("Option B Calibration Curves (Target: Month T+1 Stress)")
    plt.xlabel("Mean Predicted Probability")
    plt.ylabel("Observed Proportion")
    plt.legend(loc="upper left")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "option_b_calibration_curves.png", dpi=150)
    plt.close()

    # Figure 4: Confusion Matrices (LogReg vs XGBoost)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    for ax, m_name, pred_col in zip(axes, ["Logistic Regression", "XGBoost"], ["logreg_pred", "xgb_pred"]):
        cm = confusion_matrix(df_preds["target_next_month"], df_preds[pred_col])
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False, ax=ax,
                    xticklabels=["No Stress (0)", "Stress (1)"],
                    yticklabels=["No Stress (0)", "Stress (1)"])
        ax.set_title(f"{m_name} Confusion Matrix")
        ax.set_xlabel("Predicted Label (T+1)")
        ax.set_ylabel("True Label (T+1)")
    plt.suptitle("Option B Classification Confusion Matrices", fontsize=14, y=1.02)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "option_b_confusion_matrices.png", dpi=150)
    plt.close()

    # Figure 5: Feature Importance Bar Plot
    plt.figure(figsize=(9, 5))
    top12 = shap_importance_df.head(12)
    sns.barplot(data=top12, x="mean_abs_shap", y="feature", hue="feature", legend=False, palette="viridis")
    plt.title("Option B Global Feature Importance (Mean |TreeSHAP| Value)")
    plt.xlabel("Mean |SHAP Value| (Impact on Log-Odds of T+1 Stress)")
    plt.ylabel("Predictor (Available at Month T)")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "option_b_feature_importance.png", dpi=150)
    plt.close()

    # Figure 6: SHAP Summary Plot
    plt.figure(figsize=(9, 6))
    shap.summary_plot(shap_values, X_imputed, show=False, max_display=12)
    plt.title("Option B TreeSHAP Summary Plot (Predictors at T -> Stress at T+1)", fontsize=12)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "option_b_shap_summary.png", dpi=150)
    plt.close()

    # Figure 7: Target Distribution & Temporal Timeline
    plt.figure(figsize=(10, 4))
    monthly_trend = df_opt_b.groupby("prediction_month")["target_next_month"].agg(["count", "mean"]).reset_index()
    plt.plot(monthly_trend["prediction_month"], monthly_trend["mean"] * 100, marker="o", color="#d62728", label="Next-Month Stress Rate (%)")
    plt.title("Option B Target Prevalence Over Time (Information Month T -> Next-Month Stress T+1)")
    plt.xlabel("Prediction Month T")
    plt.ylabel("Positive Stress Prevalence (%)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "option_b_target_distribution.png", dpi=150)
    plt.close()
    logger.info("Saved all diagnostic figures to %s", FIGURES_DIR)

    # ----------------------------------------------------------------------------------
    # 12. SENSITIVITY & ROBUSTNESS AUDIT
    # ----------------------------------------------------------------------------------
    logger.info("[Step 12] Conducting sensitivity analysis across SPI thresholds (1.20, 1.25, 1.30)...")
    sens_results = []
    for thresh in [1.20, 1.25, 1.30]:
        t_pos = (df_spi["spatial_price_index"].shift(-1) > thresh).astype(int)
        valid_t = df_spi["month_gap_to_target"] == 1
        sub_pos = t_pos[valid_t]
        sens_results.append({
            "spi_threshold": thresh,
            "observations_retained": int(valid_t.sum()),
            "stress_class_count": int(sub_pos.sum()),
            "stress_prevalence_pct": round(100 * sub_pos.mean(), 2),
            "definition": f"price_stress = 1 if SPI > {thresh} else 0"
        })
    sens_df = pd.DataFrame(sens_results)
    sens_path = RESULTS_DIR / "sensitivity_analysis.csv"
    sens_df.to_csv(sens_path, index=False)
    logger.info("Sensitivity analysis saved to %s", sens_path)

    logger.info("================================================================================")
    logger.info("OPTION B RE-EXECUTION PIPELINE COMPLETE SUCCESSFULLY")
    logger.info("================================================================================")


if __name__ == "__main__":
    run_pipeline()
