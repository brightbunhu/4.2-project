"""
tests/test_feature_whitelist.py
================================
Test feature selection whitelist against final selected features.
"""
import json
import config as C

def test_feature_whitelist_consistency():
    proc_dir = C.DATA_PROC
    features_file = proc_dir / "selected_features.json"
    final_cols_file = C.OUT_RES / "final_feature_columns.json"
    
    assert features_file.exists(), "selected_features.json missing"
    assert final_cols_file.exists(), "final_feature_columns.json missing"
    
    with open(features_file, "r") as f:
        selected_payload = json.load(f)
        
    with open(final_cols_file, "r") as f:
        final_features = json.load(f)
        
    if isinstance(selected_payload, dict):
        selected_features = selected_payload.get("selected", [])
    else:
        selected_features = selected_payload
        
    assert isinstance(selected_features, list)
    assert isinstance(final_features, list)
    assert len(final_features) > 0
    # Every feature in final_features must be valid
    assert set(final_features).issubset(set(selected_features) | {"months_since_last_reported_price"})
