"""
tests/test_saved_model_loading.py
==================================
Test loading saved joblib models and checking prediction interface.
"""
import joblib
import pandas as pd
import numpy as np
import config as C

def test_load_and_predict_saved_models():
    models_dir = C.OUT_MODELS
    
    for name in ["dummy", "logreg", "xgboost"]:
        model_file = models_dir / f"revised_{name}.joblib"
        assert model_file.exists(), f"Model file missing: {model_file}"
        
        model = joblib.load(model_file)
        assert hasattr(model, "predict"), f"Model {name} missing predict method"
        assert hasattr(model, "predict_proba"), f"Model {name} missing predict_proba method"

def test_saved_models_prediction_shape():
    # Load training table and final feature columns
    tbl_file = C.DATA_PROC / "commodity_training_table.csv"
    final_cols_file = C.OUT_RES / "final_feature_columns.json"
    
    if tbl_file.exists() and final_cols_file.exists():
        import json
        df = pd.read_csv(tbl_file, nrows=10)
        with open(final_cols_file) as f:
            cols = json.load(f)
            
        X_sample = df[cols]
        xgb_model = joblib.load(C.OUT_MODELS / "revised_xgboost.joblib")
        preds = xgb_model.predict(X_sample)
        probas = xgb_model.predict_proba(X_sample)
        
        assert len(preds) == 10
        assert probas.shape == (10, 2)
