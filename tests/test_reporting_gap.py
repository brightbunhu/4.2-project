"""
tests/test_reporting_gap.py
============================
Test price reporting gap summary and exclusion of gaps > 2 months.
"""
import pandas as pd
import config as C

def test_reporting_gap_summary_file():
    gap_file = C.OUT_RES / "reporting_gap_filter_audit.csv"
    assert gap_file.exists(), f"Reporting gap filter audit missing: {gap_file}"
    
    df = pd.read_csv(gap_file)
    assert len(df) > 0, "Reporting gap filter audit is empty"

def test_no_final_observation_has_gap_greater_than_2():
    tbl_file = C.DATA_PROC / "commodity_training_table.csv"
    if tbl_file.exists():
        df = pd.read_csv(tbl_file)
        if "months_since_last_reported_price" in df.columns:
            gaps = df["months_since_last_reported_price"].dropna()
            max_gap = gaps.max()
            assert max_gap <= 2.0, f"Found observation with gap > 2 months: {max_gap}"
