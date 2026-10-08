"""
tests/test_shap_feature_order.py
=================================
Test that SHAP importance feature ordering matches feature columns.
"""
import json
import pandas as pd
import config as C

def test_shap_feature_columns_alignment():
    shap_imp_file = C.OUT_RES / "step09_shap_importance.csv"
    final_cols_file = C.OUT_RES / "final_feature_columns.json"
    
    assert shap_imp_file.exists(), f"SHAP importance file missing: {shap_imp_file}"
    assert final_cols_file.exists(), f"Final feature columns missing: {final_cols_file}"
    
    df_shap = pd.read_csv(shap_imp_file)
    with open(final_cols_file) as f:
        feature_cols = json.load(f)
        
    assert "feature" in df_shap.columns or "feature_name" in df_shap.columns
    col_name = "feature" if "feature" in df_shap.columns else "feature_name"
    
    shap_features = set(df_shap[col_name])
    expected_features = set(feature_cols)
    
    assert shap_features == expected_features, "SHAP importance feature set does not match final feature columns"
