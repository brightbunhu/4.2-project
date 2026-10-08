"""
tests/test_target_creation.py
==============================
Test binary target variable creation logic under revised threshold SPI > 1.25.
"""
import numpy as np
import pandas as pd

def test_price_stress_target_threshold():
    df = pd.DataFrame({
        "spatial_price_index": [0.8, 1.0, 1.20, 1.25, 1.26, 1.5]
    })
    
    # Revised target definition: price_stress = 1 if SPI > 1.25 else 0
    df["price_stress"] = (df["spatial_price_index"] > 1.25).astype(int)
    
    expected = [0, 0, 0, 0, 1, 1]
    assert df["price_stress"].tolist() == expected
