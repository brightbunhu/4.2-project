"""
tests/test_duplicate_removal.py
================================
Test deduplication audit outputs and deduplication logic.
"""
from pathlib import Path
import pandas as pd
import config as C

def test_duplicate_audit_files_exist():
    res_dir = C.OUT_RES
    price_dup = res_dir / "step02_price_duplicate_audit.csv"
    rain_dup = res_dir / "step02_rainfall_duplicate_audit.csv"
    pop_dup = res_dir / "step02_population_duplicate_audit.csv"
    
    assert price_dup.exists(), "Price duplicate audit missing"
    assert rain_dup.exists(), "Rainfall duplicate audit missing"
    assert pop_dup.exists(), "Population duplicate audit missing"

def test_training_table_has_no_exact_key_duplicates():
    tbl_file = C.DATA_PROC / "commodity_training_table.csv"
    if tbl_file.exists():
        df = pd.read_csv(tbl_file)
        if "district_key" in df.columns and "commodity_name" in df.columns and "month" in df.columns and "currency_code" in df.columns:
            dups = df.duplicated(subset=["district_key", "commodity_name", "month", "currency_code"]).sum()
            assert dups == 0, f"Training table contains {dups} duplicate grain keys"
