"""
tests/test_months_since_last_reported_price.py
================================================
Test months_since_last_reported_price feature calculation logic.
"""
import pandas as pd
import numpy as np

def test_months_since_last_reported_price_calculation():
    # Synthetic irregular time series
    df = pd.DataFrame({
        "district_key": ["HARARE"] * 4,
        "commodity_name": ["Maize"] * 4,
        "month": pd.to_datetime(["2023-01-15", "2023-02-15", "2023-05-15", "2023-06-15"]),
    })
    
    df = df.sort_values(["district_key", "commodity_name", "month"]).reset_index(drop=True)
    df["prev_month"] = df.groupby(["district_key", "commodity_name"])["month"].shift(1)
    df["months_since_last_reported_price"] = (df["month"] - df["prev_month"]).dt.days / 30.44
    df["months_since_last_reported_price"] = df["months_since_last_reported_price"].round(2)
    
    vals = df["months_since_last_reported_price"].tolist()
    
    # First entry should be NaN
    assert np.isnan(vals[0])
    # Second entry (~1 month later) should be ~1.0
    assert np.isclose(vals[1], 1.0, atol=0.1)
    # Third entry (Feb to May = 3 months later) should be ~3.0
    assert np.isclose(vals[2], 3.0, atol=0.2)
    # Fourth entry (May to June = 1 month later) should be ~1.0
    assert np.isclose(vals[3], 1.0, atol=0.1)
