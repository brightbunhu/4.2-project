"""
tests/test_no_current_price_leakage.py
=======================================
Test that raw current price and direct target columns are not included in model feature columns.
"""
import json
import config as C

def test_no_target_or_raw_price_leakage():
    final_cols_file = C.OUT_RES / "final_feature_columns.json"
    assert final_cols_file.exists(), "final_feature_columns.json missing"
    
    with open(final_cols_file, "r") as f:
        feature_cols = json.load(f)
        
    forbidden_cols = [
        "price", "usd_price", "zwl_price", "spatial_price_index",
        "price_spi_raw", "price_spi", "price_stress", "target"
    ]
    
    for col in forbidden_cols:
        assert col not in feature_cols, f"Target or current raw price leakage detected! '{col}' in feature columns."
