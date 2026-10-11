# 04 · Data & CSV Guide

Everything about the data behind the dashboard and the exact format for batch uploads.

---

## 1. Data sources

| Source | Used for | Grain |
|--------|----------|-------|
| HDX / WFP HAPI market prices | commodity prices → SPI | district × commodity × month × currency |
| CHIRPS v3 rainfall (NetCDF) | rainfall features | district/province × month |
| UNFPA census / population | `population`, `log_population`, `is_urban` | district |
| geoBoundaries ZWE ADM1/ADM2 | district geometry / centroids | district |
| Poverty national/province reference | context / reporting-gap handling | province / national |

Provenance shown in the app: **WFP Market Prices, CHIRPS v3 Rainfall, UNFPA Census (2017–2024)**.

---

## 2. Modelling grain and target

- **One row of the modelling table =** `district_key` × `commodity_name` × `prediction_month`
  × `currency_code`.
- **Target (`target_next_month`):** the *relative price-stress* label of the **next** month
  (T+1), where stress is defined by the SPI crossing the project threshold.
- **Horizon:** `T+1` (exactly one calendar month ahead).

The label used for display/exploration in the dashboard is **SPI > 1.25**
("High Stress") vs **SPI ≤ 1.25** ("Normal / Low Stress").

> **April 2024 ZWL redenomination** is handled in preprocessing (`config.py` constant); the
> currency dimension remains in the model key.

---

## 3. Features the model consumes

From `outputs/option_b/data/option_b_feature_columns.json` (exact order matters):

```
spi_lag_1, spi_lag_2, spi_pct_change_3m, months_since_last_reported_price,
rainfall_1m, rainfall_3m_total, rainfall_6m_total, rainfall_12m_total, rainfall_3m_anomaly,
log_population, is_urban, month_of_year, year,
commodity_laundry_soap, commodity_sugar, commodity_oil_(vegetable), commodity_rice,
commodity_toothpaste, commodity_handwash_soap, commodity_salt, commodity_fish_(kapenta),
commodity_maize_meal, commodity_beans_(sugar)
```

| Group | Notes |
|-------|-------|
| Price dynamics | `spi_lag_1`, `spi_lag_2`, `spi_pct_change_3m` |
| Reporting gap | `months_since_last_reported_price` |
| Rainfall | 1/3/6/12-month totals + 3-month anomaly |
| Population | `log_population`, `is_urban` |
| Calendar | `month_of_year`, `year` |
| Commodity | one-hot `commodity_*` columns |

---

## 4. The official CSV template

Download it from **Page 3 → 📥 Download CSV template**, or use
`outputs/option_b/data/option_b_prediction_template.csv`.

Header (canonical):

```
observation_id, prediction_month, district_key, commodity_name, currency_code,
spi_lag_1, spi_lag_2, spi_pct_change_3m, months_since_last_reported_price,
rainfall_1m, rainfall_3m_total, rainfall_6m_total, rainfall_12m_total,
rainfall_3m_anomaly, log_population, is_urban
```

Example row:

```csv
OBS_SAMPLE_001,2024-09,BEITBRIDGE,Beans,USD,1.05,1.02,4.5,1.0,45.2,120.5,450.0,780.0,0.12,11.52,0
```

### Column reference

| Column | Required | Type | Rules |
|--------|:--------:|------|-------|
| `observation_id` | Recommended | text | Unique. Duplicates are flagged. |
| `prediction_month` | ✅ | `YYYY-MM` | The cut-off month **T**. Parsed strictly. |
| `district_key` | ✅ | text | Must be an approved ADM2 district (e.g. `HARARE`, `BEITBRIDGE`). |
| `commodity_name` | ✅ | text | Must match an approved commodity exactly. |
| `currency_code` | ✅ | text | e.g. `USD`, `ZWL`. |
| `spi_lag_1`, `spi_lag_2`, `spi_pct_change_3m` | optional | number | If omitted, derived from history. |
| `months_since_last_reported_price` | optional | number | If omitted, derived. |
| `rainfall_1m`, `rainfall_3m_total`, `rainfall_6m_total`, `rainfall_12m_total` | optional | number ≥ 0 | Negative rainfall is rejected. |
| `rainfall_3m_anomaly` | optional | number | Can be negative. |
| `log_population` | optional | number | If omitted, derived. |
| `is_urban` | optional | 0/1 | If omitted, derived. |

**Only the four ✅ identifier columns are mandatory.** Any feature column you omit is filled
from the historical reference table (median fallback).

---

## 5. Validation rules and error codes

The engine (`OptionBPredictor.validate_csv`) produces an **error report** with these codes:

| Error code | Cause | Fix |
|------------|-------|-----|
| `MISSING_REQUIRED_COLUMN` | One of the four mandatory columns absent | Add the column(s) |
| `NULL_IDENTIFIER` | A mandatory cell is empty | Fill it |
| `DUPLICATE_IDENTIFIER` | `observation_id` repeated | Make IDs unique |
| `INVALID_DATE_FORMAT` | `prediction_month` unparseable | Use `YYYY-MM` |
| `UNSUPPORTED_DISTRICT` | District not in approved list | Use an approved district name |
| `UNSUPPORTED_COMMODITY` | Commodity not in approved list | Use an approved commodity name |
| `IMPOSSIBLE_NUMERIC_VALUE` | Negative rainfall | Correct the value |
| `INVALID_NUMERIC_TYPE` | Non-numeric where a number is required | Clean the value |

Invalid rows are excluded; valid rows are still scored.

---

## 6. Preparing a file: step by step

1. Download the template.
2. Keep the header row exactly as-is.
3. Add one row per district × commodity × month × currency you want scored.
4. Use `YYYY-MM` for `prediction_month` (e.g. `2024-09` meaning T = September 2024).
5. Leave feature columns blank to have them derived, or fill them to override.
6. Save as **UTF-8 CSV**.
7. Upload on Page 3, check the validation table, then predict.

### Minimal valid example

```csv
observation_id,prediction_month,district_key,commodity_name,currency_code
OBS_1,2024-09,HARARE,Maize grain,USD
OBS_2,2024-09,BULAWAYO,Cooking oil,USD
```

### Example with an intentional error

```csv
observation_id,prediction_month,district_key,commodity_name,currency_code,rainfall_3m_total
OBS_1,2024-09,HARARE,Maize grain,USD,120
OBS_2,2024-09,INVALID_LOCATION,Maize grain,USD,120
OBS_3,2024-09,BULAWAYO,Cooking oil,USD,-99
```

→ `OBS_2` fails `UNSUPPORTED_DISTRICT`; `OBS_3` fails `IMPOSSIBLE_NUMERIC_VALUE`;
`OBS_1` passes.

---

## 7. Where processed tables live

| File | Description |
|------|-------------|
| `data/processed/commodity_training_table.csv` | Legacy training table |
| `outputs/option_b/data/option_b_modelling_table.csv` | **Option B** modelling table (features + target) |
| `outputs/option_b/data/option_b_feature_columns.json` | Feature order + target/horizon metadata |
| `data/processed/d_*.csv`, `selected_features.json`, `feature_columns.json` | Intermediate components |

A full data dictionary is maintained in `reports/data_dictionary.md`.
