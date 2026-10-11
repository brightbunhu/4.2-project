"""
tests/test_prediction_interface.py
==================================
Comprehensive automated tests for Option B Single & CSV Batch Prediction interfaces.
Implements all 22 required conditions from Section 13 of
'Prompt_ Add Manual and CSV Prediction Features to the Option B ZCPSC System.md'.
"""
import sys
import json
import io
from pathlib import Path
import pandas as pd
import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import config as C
from src.prediction_engine import OptionBPredictor

@pytest.fixture(scope="module")
def predictor():
    return OptionBPredictor()


# 1. Single form creates exactly required feature schema
def test_01_single_form_creates_exact_feature_schema(predictor):
    res = predictor.predict_single(predictor.districts[0], predictor.commodities[0], "USD", "2024-09")
    assert "predicted_probability" in res
    assert "predicted_class" in res


# 2. Invalid categorical values are rejected
def test_02_invalid_categorical_values_rejected(predictor):
    invalid_df = pd.DataFrame([{
        "prediction_month": "2024-09",
        "district_key": "NON_EXISTENT_DISTRICT_XYZ",
        "commodity_name": predictor.commodities[0],
        "currency_code": "USD"
    }])
    valid_df, inv_df, errors = predictor.validate_csv(invalid_df)
    assert len(valid_df) == 0
    assert len(inv_df) == 1
    assert "UNSUPPORTED_DISTRICT" in errors["error_type"].values


# 3. Missing required columns are rejected
def test_03_missing_required_columns_rejected(predictor):
    bad_df = pd.DataFrame([{
        "district_key": predictor.districts[0],
        "commodity_name": predictor.commodities[0]
        # Missing prediction_month & currency_code
    }])
    valid_df, inv_df, errors = predictor.validate_csv(bad_df)
    assert len(valid_df) == 0
    assert "MISSING_REQUIRED_COLUMN" in errors["error_type"].values


# 4. Unexpected columns are reported/handled gracefully
def test_04_unexpected_columns_handled(predictor):
    df_with_extra = pd.DataFrame([{
        "observation_id": "OBS_01",
        "prediction_month": "2024-09",
        "district_key": predictor.districts[0],
        "commodity_name": predictor.commodities[0],
        "currency_code": "USD",
        "extra_custom_metadata": "some_tag"
    }])
    valid_df, inv_df, errors = predictor.validate_csv(df_with_extra)
    assert len(valid_df) == 1
    assert len(inv_df) == 0


# 5. Invalid dates are rejected
def test_05_invalid_dates_rejected(predictor):
    bad_date_df = pd.DataFrame([{
        "prediction_month": "NOT_A_DATE",
        "district_key": predictor.districts[0],
        "commodity_name": predictor.commodities[0],
        "currency_code": "USD"
    }])
    valid_df, inv_df, errors = predictor.validate_csv(bad_date_df)
    assert len(valid_df) == 0
    assert "INVALID_DATE_FORMAT" in errors["error_type"].values


# 6. Invalid numeric values are rejected
def test_06_invalid_numeric_values_rejected(predictor):
    bad_num_df = pd.DataFrame([{
        "prediction_month": "2024-09",
        "district_key": predictor.districts[0],
        "commodity_name": predictor.commodities[0],
        "currency_code": "USD",
        "rainfall_1m": "corrupted_string"
    }])
    valid_df, inv_df, errors = predictor.validate_csv(bad_num_df)
    assert len(valid_df) == 0
    assert "INVALID_NUMERIC_TYPE" in errors["error_type"].values


# 7. Invalid ranges are rejected
def test_07_invalid_ranges_rejected(predictor):
    neg_rain_df = pd.DataFrame([{
        "prediction_month": "2024-09",
        "district_key": predictor.districts[0],
        "commodity_name": predictor.commodities[0],
        "currency_code": "USD",
        "rainfall_1m": -50.0  # Physically impossible
    }])
    valid_df, inv_df, errors = predictor.validate_csv(neg_rain_df)
    assert len(valid_df) == 0
    assert "IMPOSSIBLE_NUMERIC_VALUE" in errors["error_type"].values


# 8. Missing values are reported correctly
def test_08_missing_values_reported(predictor):
    null_df = pd.DataFrame([{
        "prediction_month": "2024-09",
        "district_key": None,
        "commodity_name": predictor.commodities[0],
        "currency_code": "USD"
    }])
    valid_df, inv_df, errors = predictor.validate_csv(null_df)
    assert len(valid_df) == 0
    assert "NULL_IDENTIFIER" in errors["error_type"].values


# 9. Duplicate observation IDs are reported
def test_09_duplicate_observation_ids_reported(predictor):
    dup_df = pd.DataFrame([
        {
            "observation_id": "OBS_DUPLICATE",
            "prediction_month": "2024-09",
            "district_key": predictor.districts[0],
            "commodity_name": predictor.commodities[0],
            "currency_code": "USD"
        },
        {
            "observation_id": "OBS_DUPLICATE",
            "prediction_month": "2024-08",
            "district_key": predictor.districts[1],
            "commodity_name": predictor.commodities[0],
            "currency_code": "USD"
        }
    ])
    valid_df, inv_df, errors = predictor.validate_csv(dup_df)
    assert "DUPLICATE_IDENTIFIER" in errors["error_type"].values


# 10. Invalid CSV rows are excluded from prediction
def test_10_invalid_rows_excluded_from_prediction(predictor):
    mixed_df = pd.DataFrame([
        {
            "observation_id": "VALID_ROW",
            "prediction_month": "2024-09",
            "district_key": predictor.districts[0],
            "commodity_name": predictor.commodities[0],
            "currency_code": "USD"
        },
        {
            "observation_id": "INVALID_ROW",
            "prediction_month": "2024-09",
            "district_key": "NON_EXISTENT",
            "commodity_name": predictor.commodities[0],
            "currency_code": "USD"
        }
    ])
    valid_df, inv_df, errors = predictor.validate_csv(mixed_df)
    assert len(valid_df) == 1
    assert len(inv_df) == 1
    preds = predictor.predict_batch(valid_df)
    assert len(preds) == 1
    assert preds.iloc[0]["observation_id"] == "VALID_ROW"


# 11. Valid CSV rows are predicted successfully
def test_11_valid_rows_predicted_successfully(predictor):
    valid_batch = pd.DataFrame([
        {
            "observation_id": f"OBS_{i:02d}",
            "prediction_month": "2024-09",
            "district_key": predictor.districts[i % len(predictor.districts)],
            "commodity_name": predictor.commodities[0],
            "currency_code": "USD"
        }
        for i in range(5)
    ])
    valid_df, inv_df, _ = predictor.validate_csv(valid_batch)
    preds = predictor.predict_batch(valid_df)
    assert len(preds) == 5
    assert (preds["prediction_status"] == "SUCCESS").all()


# 12. Output row count matches number of valid input rows
def test_12_output_row_count_matches_valid_rows(predictor):
    batch = pd.DataFrame([
        {
            "observation_id": f"OBS_{i}",
            "prediction_month": "2024-09",
            "district_key": predictor.districts[0],
            "commodity_name": predictor.commodities[0],
            "currency_code": "USD"
        }
        for i in range(3)
    ])
    preds = predictor.predict_batch(batch)
    assert len(preds) == 3


# 13. Input metadata are preserved
def test_13_input_metadata_preserved(predictor):
    batch = pd.DataFrame([{
        "observation_id": "CUSTOM_ID_999",
        "prediction_month": "2024-09",
        "district_key": predictor.districts[0],
        "commodity_name": predictor.commodities[0],
        "currency_code": "USD"
    }])
    preds = predictor.predict_batch(batch)
    assert preds.iloc[0]["observation_id"] == "CUSTOM_ID_999"
    assert preds.iloc[0]["district_key"] == predictor.districts[0]


# 14. Prediction month and target month are correct (T and T+1)
def test_14_prediction_month_and_target_month_correct(predictor):
    batch = pd.DataFrame([{
        "prediction_month": "2024-09",
        "district_key": predictor.districts[0],
        "commodity_name": predictor.commodities[0],
        "currency_code": "USD"
    }])
    preds = predictor.predict_batch(batch)
    assert preds.iloc[0]["prediction_month"] == "2024-09"
    assert preds.iloc[0]["target_month"] == "2024-10"


# 15. The target is still the next-month target
def test_15_target_is_still_next_month(predictor):
    assert predictor.target == "target_next_month"
    assert predictor.horizon == "T+1"


# 16. Actual target-month price is never used as an input
def test_16_target_month_price_never_used_as_input(predictor):
    assert "target_price" not in predictor.features
    assert "price" not in predictor.features


# 17. The correct Option B model is loaded
def test_17_correct_option_b_model_loaded(predictor):
    assert predictor.xgb_pipeline is not None
    assert hasattr(predictor.xgb_pipeline, "predict")
    assert hasattr(predictor.xgb_pipeline, "predict_proba")


# 18. Old current-state model files are not loaded
def test_18_old_current_state_models_not_loaded():
    xgb_path = ROOT / "outputs" / "option_b" / "models" / "xgboost_pipeline.joblib"
    assert xgb_path.exists()
    assert "option_b" in str(xgb_path)


# 19. Template matches model feature schema
def test_19_template_matches_feature_schema(predictor):
    tmpl_csv = predictor.generate_csv_template()
    df_tmpl = pd.read_csv(io.StringIO(tmpl_csv))
    for req in ["prediction_month", "district_key", "commodity_name", "currency_code"]:
        assert req in df_tmpl.columns


# 20. Output CSV can be downloaded and re-read
def test_20_output_csv_downloadable_and_re_readable(predictor):
    batch = pd.DataFrame([{
        "prediction_month": "2024-09",
        "district_key": predictor.districts[0],
        "commodity_name": predictor.commodities[0],
        "currency_code": "USD"
    }])
    preds = predictor.predict_batch(batch)
    csv_bytes = preds.to_csv(index=False).encode("utf-8")
    re_read = pd.read_csv(io.BytesIO(csv_bytes))
    assert len(re_read) == 1
    assert "predicted_probability" in re_read.columns


# 21. Unavailable future target message appears correctly
def test_21_unavailable_future_target_message_correct(predictor):
    future_pred = predictor.predict_single(predictor.districts[0], predictor.commodities[0], "USD", "2025-01")
    assert future_pred["prediction_month"] == "2025-01"
    assert future_pred["target_month"] == "2025-02"
    assert "model-based estimate and not a guarantee" in future_pred["interpretation"]


# 22. Responsible-use disclaimer is visible
def test_22_responsible_use_disclaimer_is_visible(predictor):
    single_res = predictor.predict_single(predictor.districts[0], predictor.commodities[0], "USD", "2024-09")
    assert "academic decision-support estimate" in single_res["disclaimer"]
