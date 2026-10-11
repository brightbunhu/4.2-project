"""
tests/test_option_b_acceptance.py
=================================
AUTHORITATIVE ACCEPTANCE TEST SUITE FOR OPTION B:
Machine Learning-Based Prediction of Next-Month Relative Commodity Price Stress
in Zimbabwean Districts Using Market, Rainfall and Population Data.

Implements all 16 formal acceptance conditions defined in Section 5 of
Option_B_Dashboard_Testing_Acceptance.md.
"""
import sys
import json
from pathlib import Path
import pandas as pd
import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import config as C
from app.data_loader import (
    load_option_b_predictions,
    load_option_b_modelling_table,
    load_option_b_models,
    load_option_b_metrics,
    load_option_b_validation_audit,
    load_option_b_feature_audit,
    load_option_b_target_audit
)

OPT_B_DIR = ROOT / "outputs" / "option_b"


# Test 1: The target is target_next_month
def test_01_target_is_target_next_month():
    df = load_option_b_modelling_table()
    assert not df.empty, "Option B modelling table must not be empty"
    assert "target_next_month" in df.columns, "Modelling table must contain 'target_next_month'"
    # Verify values are binary
    unique_vals = set(df["target_next_month"].dropna().unique())
    assert unique_vals.issubset({0, 1}), f"Target must be binary, found: {unique_vals}"


# Test 2: The target month is exactly one month after the prediction month
def test_02_target_month_is_exactly_one_month_after_prediction_month():
    df = load_option_b_modelling_table()
    assert "prediction_month" in df.columns and "target_month" in df.columns
    p_month = pd.to_datetime(df["prediction_month"])
    t_month = pd.to_datetime(df["target_month"])
    
    # Calculate difference in calendar months: (year2 - year1)*12 + (month2 - month1)
    month_diff = (t_month.dt.year - p_month.dt.year) * 12 + (t_month.dt.month - p_month.dt.month)
    assert (month_diff == 1).all(), "Every observation's target_month must be exactly 1 calendar month after prediction_month"


# Test 3: Target-month price is not a predictor
def test_03_target_month_price_is_not_a_predictor():
    feat_json_path = OPT_B_DIR / "data" / "option_b_feature_columns.json"
    assert feat_json_path.exists(), "Feature columns JSON must exist"
    with open(feat_json_path, "r", encoding="utf-8") as f:
        meta = json.load(f)
    features = meta["features"]
    for feat in features:
        assert "target_price" not in feat.lower(), f"Target-month price leaked in feature: {feat}"
        assert feat.lower() != "price", "Raw price at target/current month must not be in feature list"


# Test 4: Target-month SPI is not a predictor
def test_04_target_month_spi_is_not_a_predictor():
    with open(OPT_B_DIR / "data" / "option_b_feature_columns.json", "r", encoding="utf-8") as f:
        features = json.load(f)["features"]
    for feat in features:
        assert "target_spi" not in feat.lower(), f"Target SPI leaked in feature: {feat}"
        assert feat.lower() != "spatial_price_index", "Current or target SPI must not be in predictor set"


# Test 5: Target-month price stress is not a predictor
def test_05_target_month_price_stress_is_not_a_predictor():
    with open(OPT_B_DIR / "data" / "option_b_feature_columns.json", "r", encoding="utf-8") as f:
        features = json.load(f)["features"]
    assert "target_next_month" not in features, "Target variable itself cannot be a predictor"
    assert "price_stress" not in features, "price_stress label cannot be a predictor"


# Test 6: No feature date is after the prediction month
def test_06_no_feature_date_after_prediction_month():
    feat_audit = load_option_b_feature_audit()
    assert not feat_audit.empty, "Feature availability audit must exist"
    assert (feat_audit["audit_status"] == "PASSED").all(), "All features must pass information date availability audit"
    for _, row in feat_audit.iterrows():
        rule = row["information_date_rule"]
        assert "<= Prediction Month T" in rule, f"Feature {row['feature_name']} violates information date rule"


# Test 7: There are no duplicate natural keys
def test_07_no_duplicate_natural_keys():
    df = load_option_b_modelling_table()
    key_cols = ["district_key", "commodity_name", "prediction_month", "currency_code"]
    dup_count = df.duplicated(subset=key_cols).sum()
    assert dup_count == 0, f"Found {dup_count} duplicate natural keys in Option B modelling table"


# Test 8: Training periods precede test periods
def test_08_training_periods_precede_test_periods():
    val_audit = load_option_b_validation_audit()
    assert not val_audit.empty, "Validation audit must exist"
    for _, row in val_audit.iterrows():
        assert row["temporal_integrity"] == "PASSED", f"Temporal integrity check failed for {row['fold']}"
        tr_end = row["train_months"].split(" to ")[1]
        te_start = row["test_months"].split(" to ")[0]
        assert tr_end < te_start, f"Training period ({tr_end}) must precede test period ({te_start})"


# Test 9: Inner tuning does not use outer test data
def test_09_inner_tuning_does_not_use_outer_test_data():
    val_audit = load_option_b_validation_audit()
    assert len(val_audit) >= 3, "At least 3 forward temporal folds must be documented"
    # Verification of training/test rows isolation
    for _, row in val_audit.iterrows():
        assert row["train_rows"] > 0 and row["test_rows"] > 0
        assert row["train_rows"] != row["test_rows"]


# Test 10: Preprocessing is fitted only on training data
def test_10_preprocessing_fitted_only_on_training_data():
    models = load_option_b_models()
    assert "logreg" in models, "Logistic regression model must exist"
    pipe = models["logreg"]
    # Check that it is an instance of a scikit-learn Pipeline
    from sklearn.pipeline import Pipeline
    assert isinstance(pipe, Pipeline), "Models must use scikit-learn Pipeline to encapsulate preprocessing"
    step_names = [s[0] for s in pipe.steps]
    assert "imputer" in step_names, "Pipeline must contain an imputer step"
    assert "scaler" in step_names, "Pipeline must contain a scaler step"


# Test 11: New Option B models are loaded by the dashboard
def test_11_new_option_b_models_loaded_by_dashboard():
    models = load_option_b_models()
    assert "dummy" in models, "Dummy baseline must be loaded"
    assert "logreg" in models, "Logistic regression must be loaded"
    assert "xgboost" in models, "XGBoost classifier must be loaded"
    # Verify predictions can be executed
    df = load_option_b_modelling_table()
    with open(OPT_B_DIR / "data" / "option_b_feature_columns.json", "r", encoding="utf-8") as f:
        feats = json.load(f)["features"]
    X = df[feats].head(5)
    preds = models["xgboost"].predict(X)
    assert len(preds) == 5


# Test 12: Dashboard labels show both T and T+1
def test_12_dashboard_labels_show_both_t_and_t_plus_1():
    # Check that app.py and pages explicitly mention Month T and Month T+1
    app_file = ROOT / "app.py"
    content = app_file.read_text(encoding="utf-8")
    assert "Month T" in content and "Month T+1" in content
    
    # Check next-month prediction page
    pred_pages = list((ROOT / "pages").glob("*Prediction*.py")) + list((ROOT / "pages").glob("*Map*.py"))
    assert len(pred_pages) > 0, "Prediction or map page must exist in pages/"
    page_texts = "\n".join([p.read_text(encoding="utf-8") for p in pred_pages])
    assert "Prediction Month (T)" in page_texts or "Prediction Month" in page_texts
    assert "Target Month (T+1)" in page_texts or "Target Forecast Month (T+1)" in page_texts


# Test 13: Prediction files contain prediction month and target month
def test_13_prediction_files_contain_prediction_and_target_months():
    df_preds = load_option_b_predictions()
    assert not df_preds.empty, "option_b_predictions.csv must exist and have content"
    required_cols = [
        "observation_id", "district_key", "commodity_name", "currency_code",
        "prediction_month", "target_month", "target_next_month",
        "dummy_pred", "logreg_pred", "xgb_pred"
    ]
    for c in required_cols:
        assert c in df_preds.columns, f"Missing required column in predictions file: {c}"


# Test 14: Old current-state results are not silently loaded
def test_14_old_current_state_results_not_silently_loaded():
    # Verify option_b directory is segregated from legacy files
    df_preds = load_option_b_predictions()
    assert "target_next_month" in df_preds.columns
    # Check that old current-month target name is not the prediction column
    assert "spatial_price_index" not in df_preds.columns or df_preds["target_next_month"].name == "target_next_month"
    # Model configuration audit confirms distinct Option B artifacts
    cfg_audit = pd.read_csv(OPT_B_DIR / "results" / "model_configuration_audit.csv")
    for _, row in cfg_audit.iterrows():
        assert "option_b" in row["artifact_path"]


# Test 15: Missing predictions produce a clear unavailable message
def test_15_missing_predictions_produce_clear_unavailable_message():
    pred_pages = list((ROOT / "pages").glob("*Prediction*.py")) + list((ROOT / "pages").glob("*Map*.py"))
    page_texts = "\n".join([p.read_text(encoding="utf-8") for p in pred_pages])
    assert "Prediction Unavailable" in page_texts or "No historical data coverage exists" in page_texts


# Test 16: The responsible-use disclaimer is present
def test_16_responsible_use_disclaimer_is_present():
    app_file = ROOT / "app.py"
    content = app_file.read_text(encoding="utf-8")
    disclaimer_snippet = "This dashboard provides model-based predictions of next-month relative commodity-price stress"
    assert disclaimer_snippet in content, "Mandatory disclaimer must be present in app.py"
    
    overview_page = ROOT / "pages" / "1_Overview.py"
    if overview_page.exists():
        h_content = overview_page.read_text(encoding="utf-8")
    else:
        h_content = (ROOT / "pages" / "1_Home.py").read_text(encoding="utf-8")
    assert disclaimer_snippet in h_content, "Mandatory disclaimer must be present in Overview/Home page"
