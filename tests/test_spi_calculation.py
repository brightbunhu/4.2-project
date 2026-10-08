"""
tests/test_spi_calculation.py
==============================
Test Spatial Price Index (SPI) formula and thin-cell guard of min 8 districts.
"""
import numpy as np
import pandas as pd
from src.train_spatiotemporal_revised import spatial_price_index_revised

def test_spatial_price_index_thin_cell_guard():
    # Synthetic dataset with 5 reporting districts (< 8 min threshold)
    df_thin = pd.DataFrame({
        "district_key": [f"DIST_{i}" for i in range(5)],
        "month": pd.to_datetime(["2023-01-01"] * 5),
        "commodity_name": ["Maize"] * 5,
        "currency_code": ["USD"] * 5,
        "price": [10.0, 12.0, 8.0, 10.0, 10.0],
        "is_food": [True] * 5,
    })
    
    res_thin = spatial_price_index_revised(df_thin, min_districts=8)
    # Target / SPI should be NaN because n_districts < 8
    assert res_thin["spatial_price_index"].isna().all()

def test_spatial_price_index_valid_cell():
    # Synthetic dataset with 10 reporting districts (>= 8 min threshold)
    df_valid = pd.DataFrame({
        "district_key": [f"DIST_{i}" for i in range(10)],
        "month": pd.to_datetime(["2023-01-01"] * 10),
        "commodity_name": ["Maize"] * 10,
        "currency_code": ["USD"] * 10,
        "price": [10.0] * 10,
        "is_food": [True] * 10,
    })
    
    res_valid = spatial_price_index_revised(df_valid, min_districts=8)
    assert not res_valid["spatial_price_index"].isna().any()
    assert np.allclose(res_valid["spatial_price_index"], 1.0)
