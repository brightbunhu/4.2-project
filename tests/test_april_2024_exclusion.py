"""
tests/test_april_2024_exclusion.py
===================================
Test that April 2024 redenomination period is properly audited and excluded
or handled in training pipeline.
"""
from pathlib import Path
import pandas as pd
import pytest

import config as C

def test_april_2024_redenomination_audit():
    audit_file = C.OUT_RES / "redenomination_audit.csv"
    assert audit_file.exists(), f"Redenomination audit file missing: {audit_file}"
    df = pd.read_csv(audit_file)
    assert len(df) > 0, "Redenomination audit CSV is empty"
    assert "currency_code" in df.columns or "month" in df.columns or "note" in df.columns

def test_april_2024_exclusion_in_training_table():
    tbl_file = C.DATA_PROC / "commodity_training_table.csv"
    if tbl_file.exists():
        df = pd.read_csv(tbl_file)
        if "month" in df.columns:
            df["month_str"] = pd.to_datetime(df["month"]).dt.strftime("%Y-%m")
            # Verify ZWL currency rows in April 2024 are excluded or marked
            zwl_apr2024 = df[(df["month_str"] == "2024-04") & (df.get("currency_code", pd.Series()) == "ZWL")]
            assert len(zwl_apr2024) == 0, "ZWL quotes in April 2024 (redenomination month) should be excluded"
