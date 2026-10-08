"""
tests/test_district_grouping.py
================================
Test forward-chaining spatio-temporal validation:
1. Temporal train-test ordering (train dates < test dates)
2. Spatial train-test separation (held-out test districts absent from training fold)
"""
import pandas as pd
import config as C

def test_spatiotemporal_fold_audit():
    fold_file = C.OUT_RES / "spatiotemporal_fold_definitions.csv"
    assert fold_file.exists(), f"Fold definitions file missing: {fold_file}"
    
    df = pd.read_csv(fold_file)
    assert len(df) >= 3, "Must contain at least 3 spatio-temporal folds"
    
    for idx, row in df.iterrows():
        # Assert temporal ordering: train end date < test start date
        tr_end = pd.to_datetime(row["train_end_date"])
        te_start = pd.to_datetime(row["test_start_date"])
        assert tr_end < te_start, f"Fold {row['fold']} temporal leakage! tr_end={tr_end}, te_start={te_start}"
        
        # Assert zero district overlap
        assert row["district_overlap_count"] == 0, f"Fold {row['fold']} spatial leakage! Overlap={row['district_overlap_count']}"
        assert row["status"] == "PASS"
