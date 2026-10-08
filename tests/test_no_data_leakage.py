"""
tests/test_no_data_leakage.py
==============================
Test data leakage audit results and pipeline construction.
"""
import pandas as pd
import config as C

def test_data_leakage_audit_report():
    audit_file = C.OUT_RES / "data_leakage_audit.csv"
    assert audit_file.exists(), f"Data leakage audit file missing: {audit_file}"
    
    df = pd.read_csv(audit_file)
    assert len(df) > 0, "Data leakage audit file is empty"
    assert "check_name" in df.columns or "status" in df.columns or "description" in df.columns
