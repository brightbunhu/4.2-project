# Option B Prediction Interface Audit Report

## 1. Executive Summary

This audit evaluates the system architecture, model files, feature schema, and data validation rules governing the **Next-Month Prediction** interface (Single Manual Observation and CSV Batch Upload).

## 2. Model & Pipeline Verification

- **Production Model Artifact:** `outputs/option_b/models/xgboost_pipeline.joblib`
- **Linear Alternative Artifact:** `outputs/option_b/models/logreg_pipeline.joblib`
- **Baseline Artifact:** `outputs/option_b/models/dummy_baseline.joblib`
- **Encapsulated Preprocessing:** scikit-learn `Pipeline` encapsulating `SimpleImputer(strategy='median')` and (for Logistic Regression) `StandardScaler()`.
- **Target Specification:** `target_next_month` ($\text{SPI}(T+1) > 1.25$).
- **Predictive Horizon:** Month $T \to$ Month $T+1$. Target month is verified as exactly $\text{prediction\_month} + 1 \text{ calendar month}$.

## 3. Feature Schema & Whitelist Specification

The model consumes exactly 23 features in deterministic order, specified in `outputs/option_b/data/option_b_feature_columns.json`:

| Feature Name | Category | Training Min | Training Max | Description |
|---|---|---|---|---|
| `spi_lag_1` | Market Lag | 0.450 | 2.500 | Relative price index at $T-1$ |
| `spi_lag_2` | Market Lag | 0.450 | 2.500 | Relative price index at $T-2$ |
| `spi_pct_change_3m` | Market Lag | -85.0% | +250.0% | 3-month rolling SPI change ending at $T$ |
| `months_since_last_reported_price` | Continuity | 0.50 | 2.00 | Gap between last report and month $T$ |
| `rainfall_1m` | Rainfall | 0.00 mm | 450.00 mm | Precipitation during prediction month $T$ |
| `rainfall_3m_total` | Rainfall | 0.00 mm | 1,100.00 mm | 3-month cumulative rainfall ending at $T$ |
| `rainfall_6m_total` | Rainfall | 0.00 mm | 1,800.00 mm | 6-month cumulative rainfall ending at $T$ |
| `rainfall_12m_total` | Rainfall | 150.00 mm | 2,400.00 mm | 12-month cumulative rainfall ending at $T$ |
| `rainfall_3m_anomaly` | Rainfall | -3.50 | +3.50 | Standardized 3-month rainfall anomaly |
| `log_population` | Context | 10.20 | 14.50 | Natural logarithm of district population |
| `is_urban` | Context | 0 | 1 | Binary indicator for urban district status |
| `month_of_year` | Temporal | 1 | 12 | Calendar month of prediction date $T$ |
| `year` | Temporal | 2017 | 2024 | Observation year |
| 10 $\times$ `commodity_*` | Commodity | 0 | 1 | One-hot binary indicators for top commodities |

## 4. Input Domains & Categorical Constraints

- **Supported Districts:** 79 canonical Zimbabwean ADM2 districts (`HARARE`, `BULAWAYO`, `BEITBRIDGE`, `MUTARE`, etc.).
- **Supported Commodities:** 16 food commodities (`Maize grain`, `Maize meal`, `Cooking oil`, `Sugar`, `Beans`, etc.).
- **Supported Currencies:** `USD` and `ZWL`.

## 5. Input Validation Rules

The prediction engine rejects:
1. Missing mandatory identification columns (`prediction_month`, `district_key`, `commodity_name`, `currency_code`).
2. Unparseable dates or dates not mapping to valid months.
3. Negative values for rainfall features ($\text{rainfall} < 0$).
4. Unsupported district or commodity names not matching the administrative domain.
5. Non-numeric values in numerical feature slots.
6. Target-month features (strict zero-leakage guarantee: target price or SPI cannot be input).

## 6. Explainability Capabilities

TreeSHAP is connected directly to `xgboost_pipeline.joblib`. When a single prediction is made, TreeSHAP calculates the exact log-odds impact for each feature, identifying top factors increasing and decreasing forecasted risk, accompanied by the mandatory disclaimer:
> *"Feature contribution explains the fitted model prediction; it does not prove causation."*
