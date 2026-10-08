"""
tests/test_currency_grouping.py
================================
Test currency handling and grouping for spatial price index calculation.
"""
import pandas as pd
import numpy as np
from src.utils import spatial_price_index

def test_currency_grouped_spi():
    # Synthetic dataset with USD and ZWL prices in the same month and commodity
    data = pd.DataFrame({
        "district_key": ["HARARE", "BULAWAYO", "MUTARE", "HARARE", "BULAWAYO", "MUTARE"],
        "month": pd.to_datetime(["2023-01-01"] * 6),
        "commodity_name": ["Maize"] * 6,
        "currency_code": ["USD", "USD", "USD", "ZWL", "ZWL", "ZWL"],
        "price": [10.0, 12.0, 8.0, 10000.0, 12000.0, 8000.0],
        "is_food": [True] * 6,
    })
    
    # Calculate SPI
    spi_df = spatial_price_index(data, by="district", winsor=(0.0, 1.0))
    
    # Check that country_median_price for USD is 10.0 and for ZWL is 10000.0
    usd_rows = spi_df[spi_df["currency_code"] == "USD"]
    zwl_rows = spi_df[spi_df["currency_code"] == "ZWL"]
    
    assert np.isclose(usd_rows["country_median_price"].iloc[0], 10.0)
    assert np.isclose(zwl_rows["country_median_price"].iloc[0], 10000.0)
    
    # SPI values should be identical across currencies for corresponding relative prices
    harare_usd_spi = usd_rows[usd_rows["district_key"] == "HARARE"]["price_spi_raw"].iloc[0]
    harare_zwl_spi = zwl_rows[zwl_rows["district_key"] == "HARARE"]["price_spi_raw"].iloc[0]
    
    assert np.isclose(harare_usd_spi, 1.0)
    assert np.isclose(harare_zwl_spi, 1.0)
    assert np.isclose(harare_usd_spi, harare_zwl_spi)
