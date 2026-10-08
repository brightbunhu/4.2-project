# ZCPSC Final Revised Evidence Report

**Project**: Zimbabwe Commodity Price Stress Classifier (ZCPSC)
**Pipeline execution timestamp**: 20261004_165957
**Report generation date**: 2026-10-04
**Pipeline script**: `src/final_correction_pipeline.py`

---

## 1. Revised Target Definition

| Item | Value |
|------|-------|
| Target variable | `price_stress` |
| Definition | `spatial_price_index > 1.25` |
| Target type | Binary (0 = low stress, 1 = high stress) |
| Target prevalence | 0.1375 (13.75%) |
| Class 0 count | 8,717 |
| Class 1 count | 1,390 |
| Total modelling observations | 10,107 |
| Source verification | `src/final_correction_pipeline.py` line 221 |

The SPI is computed as `price / country_median_price` within each `(month, commodity_name, currency_code)` cell. Cells with fewer than 8 reporting districts are excluded (thin-cell guard). SPI values are winsorised at the 1st and 99th percentiles.

---

## 2. Macroeconomic Adjustment

### MACROECONOMIC ADJUSTMENT STATUS: NOT IMPLEMENTED — DOCUMENTED LIMITATION

Verified CPI and exchange-rate data were not available in the project files or established through the documented source search. Therefore, nominal prices were not deflated and were not converted into a common real-price currency before SPI calculation. The implementation used within-currency SPI calculation and excluded the April 2024 ZWL redenomination observations. These measures prevent direct USD/ZWL price comparison and address the identified redenomination period, but they do not remove inflation effects within a currency over time.

**Actual SPI formula used**:

```text
SPI(i,c,m,u) =
nominal_price(i,c,m,u) /
median(nominal_price(j,c,m,u))
```

Where:
- `i` = district
- `c` = commodity
- `m` = month
- `u` = currency code
- `j` = all districts reporting the same commodity, month, and currency

| Item | Status |
|------|--------|
| CPI deflation | NOT IMPLEMENTED — no CPI data found in project |
| Exchange-rate adjustment | NOT IMPLEMENTED — no exchange-rate series found in project |
| Currency isolation (within-currency SPI) | IMPLEMENTED (partial safeguard only) — SPI computed within each `currency_code` group |
| April 2024 ZWL redenomination exclusion | IMPLEMENTED — 4 rows removed |
| Overall macroeconomic adjustment status | **NOT IMPLEMENTED — DOCUMENTED LIMITATION** |

**Audit file**: `outputs/results/macroeconomic_adjustment_audit.csv`

**Source search conducted**:
- File name patterns searched: `cpi`, `consumer_price`, `inflation`, `deflator`, `exchange_rate`, `fx_rate`, `forex`, `parallel_market`
- Column names in `hdx_hapi_food_price_zwe.csv` checked for CPI, exchange-rate, or inflation columns
- **Result**: No verified CPI or exchange-rate series found in any project data file

**What was implemented**:
- Within-currency SPI calculation prevents direct comparison of USD and ZWL prices
- April 2024 ZWL observations removed due to ZiG redenomination

**What was NOT implemented**:
- CPI deflation of nominal prices
- Exchange-rate normalisation to a common real-price base
- Any time-series inflation adjustment within a single currency

**Consequence**: The SPI is computed over nominal prices. Secular inflation within ZWL or USD may inflate the SPI over time independently of genuine spatial price stress. This is an acknowledged study limitation that must be discussed in the dissertation.

---

## 3. Spatial Price Index (SPI) Methodology

| Item | Value |
|------|-------|
| Grouping key | `(month, commodity_name, currency_code)` |
| Reference statistic | National median price per cell |
| Minimum districts per cell | 8 |
| Winsorisation bounds | 1st and 99th percentiles |
| Valid SPI rows after thin-cell exclusion | 11,879 |
| Thin-cell excluded rows | 2,045 |
| Thin-cell audit file | `outputs/results/thin_cell_audit.csv` |

---

## 4. Data Period and Year Coverage

| Year | Raw Records | Final Modelling Records | Used for Training | Exclusion Reason |
|------|-------------|------------------------|-------------------|------------------|
| 2017 | 1,095 | 426 | Yes | — |
| 2018 | 899 | 71 | Yes | — |
| 2019 | 171 | 68 | Yes | — |
| 2020 | 8,267 | 3,118 | Yes | — |
| 2021 | 5,482 | 2,513 | Yes | — |
| 2022 | 2,456 | 817 | Yes | — |
| 2023 | 4,651 | 2,301 | Yes | — |
| 2024 | 1,734 | 793 | Yes | — |
| 2025 | 604 | 0 | No | Insufficient valid observations after thin-cell and gap filtering |
| 2026 | 195 | 0 | No | Insufficient valid observations after thin-cell and gap filtering |

- **Modelling period**: 2017-01-01 to 2024-10-01
- **Year coverage audit file**: `outputs/results/year_coverage_audit.csv`

**2025–2026 resolution**: Raw records exist (604 and 195 respectively) but produce zero valid modelling rows after thin-cell filtering (< 8 districts) and reporting-gap filtering (> 2 months). These years are excluded from modelling with documented justification.

---

## 5. Reporting Gap Filter

| Item | Value |
|------|-------|
| Maximum gap before filter | Verified in `reporting_gap_summary.csv` |
| Maximum gap after filter | ≤ 2.0 months |
| Rows removed by gap filter | 1,772 |
| Rows remaining after gap filter | 10,107 |
| Gap filter audit file | `outputs/results/reporting_gap_filter_audit.csv` |
| Gap summary file | `outputs/results/reporting_gap_summary.csv` |

---

## 6. Feature Set

**Feature count**: 22
**Feature list file**: `outputs/results/final_feature_columns.json`

| # | Feature | Category |
|---|---------|----------|
| 1 | `rainfall_1m` | Rainfall |
| 2 | `rainfall_6m_total` | Rainfall |
| 3 | `rainfall_3m_anomaly` | Rainfall |
| 4 | `rainfall_3m_total` | Rainfall |
| 5 | `rainfall_12m_total` | Rainfall |
| 6 | `spi_pct_change_3m` | Lag |
| 7 | `spi_lag_1` | Lag |
| 8 | `spi_lag_2` | Lag |
| 9 | `log_population` | Demographic |
| 10 | `months_since_last_reported_price` | Reporting |
| 11 | `year` | Temporal |
| 12 | `commodity_OTHER` | Commodity one-hot |
| 13–22 | `commodity_{name}` (10 commodities) | Commodity one-hot |

**Leakage safeguards**: Raw prices, current SPI value, and target variable are excluded from the feature matrix. Only lagged SPI values (t−1, t−2) and 3-month percent change are used.

---

## 7. Outer Spatio-Temporal Validation Design

### 7.1 Outer Fold Definitions

| Fold | Train Period | Test Period | Train Districts | Test Districts | District Overlap | Temporal Overlap | Train Obs | Test Obs | Status |
|------|-------------|-------------|-----------------|----------------|------------------|------------------|-----------|----------|--------|
| 1 | 2017-01-01 → 2021-06-30 | 2021-07-01 → 2022-06-30 | 74 | 8 | 0 | PASS (strictly earlier) | 4,383 | 463 | PASS |
| 2 | 2017-01-01 → 2022-06-30 | 2022-07-01 → 2023-06-30 | 66 | 16 | 0 | PASS (strictly earlier) | 5,815 | 341 | PASS |
| 3 | 2017-01-01 → 2023-06-30 | 2023-07-01 → 2024-12-31 | 69 | 13 | 0 | PASS (strictly earlier) | 6,485 | 492 | PASS |

**Audit file**: `outputs/results/spatiotemporal_fold_definitions.csv`

All three outer folds have:
- **Zero district overlap** between train and test sets
- **Strict temporal ordering** — all training dates precede all test dates
- **Expanding-window design** — each fold adds more historical training data

### 7.2 Outer Leakage Audit

| Check | Status |
|-------|--------|
| Temporal Separation (train < test) | PASS |
| Spatial Separation (train ∩ test = ∅) | PASS |
| Pipeline Imputation (inside Pipeline) | PASS |
| Pipeline Scaling (inside Pipeline) | PASS |
| No Target Leakage | PASS |
| SHAP Preprocessing Alignment | PASS |

**Audit file**: `outputs/results/spatiotemporal_leakage_audit.csv`

---

## 8. Inner Time-Forward Hyperparameter Tuning

### 8.1 Inner Fold Design

Each outer training fold is split into 2 inner time-forward folds:
- Inner fold 1: first 60% of dates for training, next 20% for validation
- Inner fold 2: first 80% of dates for training, final 20% for validation

Outer test districts are excluded from inner validation to prevent spatial leakage.

**Tuning metric**: macro-F1
**Audit file**: `outputs/results/inner_spatiotemporal_fold_definitions.csv`

### 8.2 Inner Leakage Audit — All Checks PASS

| Check | Total Checks | All PASS |
|-------|-------------|----------|
| Inner train precedes inner val | 12 | Yes |
| Inner val no outer test dates | 12 | Yes |
| Inner val no outer test districts | 12 | Yes |
| Preprocessing fit on inner train only | 12 | Yes |

**Audit file**: `outputs/results/inner_spatiotemporal_leakage_audit.csv`

### 8.3 Inner Fold Date Ranges (Verified)

**Logistic Regression**:
| Outer Fold | Inner Fold | Inner Train | Inner Val | Train N | Val N |
|------------|------------|-------------|-----------|---------|-------|
| 1 | 1 | 2017-01-01 → 2020-04-01 | 2020-05-01 → 2020-11-01 | 1,392 | 1,575 |
| 1 | 2 | 2017-01-01 → 2020-11-01 | 2020-12-01 → 2021-06-01 | 2,967 | 1,416 |
| 2 | 1 | 2017-01-01 → 2020-10-01 | 2020-11-01 → 2021-07-01 | 2,654 | 2,007 |
| 2 | 2 | 2017-01-01 → 2021-07-01 | 2021-08-01 → 2022-06-01 | 4,661 | 1,154 |
| 3 | 1 | 2017-01-01 → 2021-04-01 | 2021-05-01 → 2022-05-01 | 3,735 | 1,460 |
| 3 | 2 | 2017-01-01 → 2022-05-01 | 2022-06-01 → 2023-06-01 | 5,195 | 1,290 |

**XGBoost**: Same fold date ranges (verified in inner_spatiotemporal_fold_definitions.csv)

### 8.4 Selected Hyperparameters

**Logistic Regression** (selected via inner tuning):

| Outer Fold | Best C | Best class_weight | Inner macro-F1 |
|------------|--------|-------------------|----------------|
| 1 | 0.01 | balanced | 0.7739 |
| 2 | 0.1 | balanced | 0.7414 |
| 3 | 0.01 | balanced | 0.7245 |

**XGBoost** (selected via inner tuning):

| Outer Fold | n_estimators | max_depth | learning_rate | subsample | colsample_bytree | Inner macro-F1 |
|------------|-------------|-----------|---------------|-----------|------------------|----------------|
| 1 | 300 | 3 | 0.05 | 0.8 | 0.7 | 0.7242 |
| 2 | 200 | 3 | 0.1 | 0.8 | 0.7 | 0.7224 |
| 3 | 100 | 3 | 0.1 | 0.8 | 0.7 | 0.7217 |

**Hyperparameter search file**: `outputs/results/spatiotemporal_hyperparameter_results.csv`
**Best parameters file**: `outputs/results/spatiotemporal_best_hyperparameters.csv`

---

## 9. Outer Fold Model Performance

### 9.1 Per-Fold Results

**Dummy Classifier (most_frequent baseline)**:

| Fold | Accuracy | Balanced Acc | Macro-F1 | ROC-AUC |
|------|----------|-------------|----------|---------|
| 1 | 0.9525 | 0.5000 | 0.4878 | 0.5000 |
| 2 | 0.8504 | 0.5000 | 0.4596 | 0.5000 |
| 3 | 0.8211 | 0.5000 | 0.4509 | 0.5000 |

**Logistic Regression**:

| Fold | Accuracy | Balanced Acc | Macro-F1 | ROC-AUC | PR-AUC | Brier |
|------|----------|-------------|----------|---------|--------|-------|
| 1 | 0.9698 | 0.7034 | 0.7734 | 0.8530 | 0.5686 | 0.0280 |
| 2 | 0.8680 | 0.7366 | 0.7385 | 0.8672 | 0.6460 | 0.0958 |
| 3 | 0.6382 | 0.7441 | 0.5989 | 0.8713 | 0.5875 | 0.2664 |

**XGBoost**:

| Fold | Accuracy | Balanced Acc | Macro-F1 | ROC-AUC | PR-AUC | Brier |
|------|----------|-------------|----------|---------|--------|-------|
| 1 | 0.9633 | 0.7000 | 0.7476 | 0.9465 | 0.6046 | 0.0300 |
| 2 | 0.8974 | 0.6569 | 0.7104 | 0.8851 | 0.7050 | 0.0855 |
| 3 | 0.8618 | 0.7514 | 0.7582 | 0.8825 | 0.5960 | 0.1004 |

### 9.2 Summary Metrics (Mean ± Std Across 3 Outer Folds)

| Model | Accuracy | Balanced Acc | Macro-F1 | ROC-AUC | PR-AUC | Brier |
|-------|----------|-------------|----------|---------|--------|-------|
| Dummy | 0.875 ± 0.069 | 0.500 ± 0.000 | 0.466 ± 0.019 | 0.500 ± 0.000 | 0.125 ± 0.069 | 0.125 ± 0.069 |
| LogReg | 0.825 ± 0.170 | 0.728 ± 0.022 | 0.704 ± 0.092 | 0.864 ± 0.010 | 0.601 ± 0.040 | 0.130 ± 0.123 |
| XGBoost | 0.907 ± 0.051 | 0.703 ± 0.047 | 0.739 ± 0.025 | 0.905 ± 0.037 | 0.635 ± 0.061 | 0.072 ± 0.037 |

**Best model by macro-F1**: XGBoost (0.739 ± 0.025)
**Best model by ROC-AUC**: XGBoost (0.905 ± 0.037)
**Best model by Brier score**: XGBoost (0.072 ± 0.037)

**Metrics files**:
- `outputs/results/spatiotemporal_validation_results.csv`
- `outputs/results/spatiotemporal_outer_fold_metrics.csv`

### 9.3 Confusion Matrices (Aggregated Across Outer Folds)

**Logistic Regression**:

|  | Predicted Low | Predicted High |
|--|--------------|----------------|
| **Actual Low** | 921 | 214 |
| **Actual High** | 41 | 120 |

**XGBoost**:

|  | Predicted Low | Predicted High |
|--|--------------|----------------|
| **Actual Low** | 1,101 | 34 |
| **Actual High** | 86 | 75 |

**Confusion matrix file**: `outputs/results/final_confusion_matrices.csv`

### 9.4 Calibration

| Model | Expected Calibration Error (ECE) |
|-------|----------------------------------|
| LogReg | 0.2368 |
| XGBoost | 0.0488 |

**File**: `outputs/results/final_calibration_metrics.csv`

---

## 10. Final Model Artefacts

### 10.1 Saved Models

| Model | File | Size (bytes) | SHA-256 (first 16) | Prediction Verified |
|-------|------|-------------|---------------------|---------------------|
| Dummy | `outputs/models/revised_dummy.joblib` | 1,857 | `fff2a0f065c58620` | PASS |
| LogReg | `outputs/models/revised_logreg.joblib` | 3,201 | `db15f514deb4ac18` | PASS |
| XGBoost | `outputs/models/revised_xgboost.joblib` | 127,603 | `cc27afa63d17c6d1` | PASS |

**Full SHA-256 hashes**:
- Dummy: `fff2a0f065c58620505e499cbc6853b8b76453645f469c2a82630d3e214e71b3`
- LogReg: `db15f514deb4ac18e30b106b24c67cb54aa92cf5e9923b28bd57a8dddef988a7`
- XGBoost: `cc27afa63d17c6d1c00e437759bc5e5ed96769758715ea85fd72b9c486750ce7`

### 10.2 Final Training Configuration

| Item | Value |
|------|-------|
| Training period | 2017-01-01 to 2024-10-01 |
| Feature count | 22 |
| Total observations | 10,107 |
| Target prevalence | 0.1375 |
| scikit-learn version | 1.9.1 |
| XGBoost version | 3.4.1 |
| Random seed | 42 |

### 10.3 Final XGBoost Hyperparameters (from fold 3 — largest training set)

| Parameter | Value |
|-----------|-------|
| `n_estimators` | 100 |
| `max_depth` | 3 |
| `learning_rate` | 0.1 |
| `subsample` | 0.8 |
| `colsample_bytree` | 0.7 |

**Metadata file**: `outputs/results/model_training_metadata.json`

---

## 11. SHAP Explainability — Regenerated and Verified

### 11.1 SHAP Regeneration Audit

| Item | Value |
|------|-------|
| Model used | `outputs/models/revised_xgboost.joblib` |
| Model SHA-256 | `cc27afa63d17c6d1c00e437759bc5e5ed96769758715ea85fd72b9c486750ce7` |
| SHAP method | TreeSHAP (exact) |
| SHAP row count | 10,107 |
| SHAP feature count | 22 |
| Feature order alignment | PASS |
| New SHAP values SHA-256 | `6f230af2e875dcf8b17f3c6f0c2bfb218266314972f0a78d0505b169be2fd44d` |
| Old SHAP values SHA-256 | `444aff6b75e202fcc953c4a6c1cebf473a58a2000821ceb309e5481a26bd2fa1` |
| **Values changed vs old** | **True** |
| New SHAP importance SHA-256 | `558798e2992229c15aec309602ed3b29e673c8eb5664b5f668814707c5bb0d7a` |
| Old SHAP importance SHA-256 | `5289a58c16ed63f5afdea9b90fcd27a87b67c7d793c7d185557ea6625887f2df` |
| **Importance changed vs old** | **True** |
| Generation timestamp | 20261004_165957 |

**Conclusion**: SHAP values were independently regenerated from the retrained XGBoost model. Hash comparison confirms the new values differ from the previous version.

### 11.2 Top Features by Mean |SHAP|

| Rank | Feature | Mean |SHAP| |
|------|---------|--------------|
| 1 | `spi_pct_change_3m` | 0.7976 |
| 2 | `spi_lag_1` | 0.7463 |
| 3 | `spi_lag_2` | 0.3895 |
| 4 | `year` | 0.2109 |
| 5 | `rainfall_12m_total` | 0.1906 |
| 6 | `rainfall_3m_anomaly` | 0.0895 |
| 7 | `rainfall_3m_total` | 0.0753 |
| 8 | `rainfall_1m` | 0.0739 |
| 9 | `log_population` | 0.0628 |
| 10 | `commodity_Salt` | 0.0466 |

**SHAP files**:
- `outputs/explainability/revised_shap_values.csv`
- `outputs/explainability/revised_shap_importance.csv`
- `outputs/explainability/revised_shap_local_examples.csv`
- `outputs/explainability/revised_shap_audit.csv`

### 11.3 SHAP Archival

Previous SHAP files were archived to `archive/shap_archive_20261004_165957/` before regeneration. This ensures full traceability.

---

## 12. Figures Generated

| Figure | File | Verified |
|--------|------|----------|
| Revised SHAP global importance | `outputs/figures/revised_shap_summary.png` | Yes |
| Revised SHAP global importance (copy) | `outputs/figures/revised_shap_global_importance.png` | Yes |
| Revised SHAP local example | `outputs/figures/revised_shap_local_example.png` | Yes |
| Revised confusion matrix (LogReg) | `outputs/figures/revised_confusion_matrix_logreg.png` | Yes |
| Revised confusion matrix (XGBoost) | `outputs/figures/revised_confusion_matrix_xgboost.png` | Yes |
| Revised ROC curve comparison | `outputs/figures/revised_roc_curve_comparison.png` | Yes |
| Revised Precision-Recall curve | `outputs/figures/revised_precision_recall_curve_comparison.png` | Yes |

---

## 13. Automated Test Suite

**24 tests passed, 0 failed** (pytest run on 2026-10-04)

| # | Test File | Test Name | Status |
|---|-----------|-----------|--------|
| 1 | `test_april_2024_exclusion.py` | `test_april_2024_redenomination_audit` | PASSED |
| 2 | `test_april_2024_exclusion.py` | `test_april_2024_exclusion_in_training_table` | PASSED |
| 3 | `test_currency_grouping.py` | `test_currency_grouped_spi` | PASSED |
| 4 | `test_dashboard_loading.py` | `test_data_loader_import` | PASSED |
| 5 | `test_dashboard_loading.py` | `test_app_entrypoint_exists` | PASSED |
| 6 | `test_district_grouping.py` | `test_spatiotemporal_fold_audit` | PASSED |
| 7 | `test_duplicate_removal.py` | `test_duplicate_audit_files_exist` | PASSED |
| 8 | `test_duplicate_removal.py` | `test_training_table_has_no_exact_key_duplicates` | PASSED |
| 9 | `test_feature_whitelist.py` | `test_feature_whitelist_consistency` | PASSED |
| 10 | `test_months_since_last_reported_price.py` | `test_months_since_last_reported_price_calculation` | PASSED |
| 11 | `test_nested_validation.py` | `test_nested_groupkfold_results_exist` | PASSED |
| 12 | `test_nested_validation.py` | `test_best_hyperparameters_exist` | PASSED |
| 13 | `test_no_current_price_leakage.py` | `test_no_target_or_raw_price_leakage` | PASSED |
| 14 | `test_no_data_leakage.py` | `test_data_leakage_audit_report` | PASSED |
| 15 | `test_pipeline_imputation.py` | `test_pipeline_imputation_handles_nans` | PASSED |
| 16 | `test_pipeline_scaling.py` | `test_pipeline_scaler` | PASSED |
| 17 | `test_reporting_gap.py` | `test_reporting_gap_summary_file` | PASSED |
| 18 | `test_reporting_gap.py` | `test_no_final_observation_has_gap_greater_than_2` | PASSED |
| 19 | `test_saved_model_loading.py` | `test_load_and_predict_saved_models` | PASSED |
| 20 | `test_saved_model_loading.py` | `test_saved_models_prediction_shape` | PASSED |
| 21 | `test_shap_feature_order.py` | `test_shap_feature_columns_alignment` | PASSED |
| 22 | `test_spi_calculation.py` | `test_spatial_price_index_thin_cell_guard` | PASSED |
| 23 | `test_spi_calculation.py` | `test_spatial_price_index_valid_cell` | PASSED |
| 24 | `test_target_creation.py` | `test_price_stress_target_threshold` | PASSED |

---

## 14. Dashboard

| Item | Value |
|------|-------|
| Entrypoint | `app/dashboard.py` |
| Framework | Streamlit |
| Status | Running (verified active during pipeline execution) |
| Launch command | `streamlit run app/dashboard.py` |
| Number of pages | 7 |

---

## 15. Complete Audit File Inventory

### Preprocessing Audits
| File | Location |
|------|----------|
| Macroeconomic adjustment audit | `outputs/results/macroeconomic_adjustment_audit.csv` |
| Thin-cell audit | `outputs/results/thin_cell_audit.csv` |
| Reporting gap filter audit | `outputs/results/reporting_gap_filter_audit.csv` |
| Reporting gap summary | `outputs/results/reporting_gap_summary.csv` |
| Year coverage audit | `outputs/results/year_coverage_audit.csv` |
| Currency timeline | `outputs/results/currency_timeline.csv` |
| Redenomination audit | `outputs/results/redenomination_audit.csv` |

### Validation Audits
| File | Location |
|------|----------|
| Outer fold definitions | `outputs/results/spatiotemporal_fold_definitions.csv` |
| Inner fold definitions | `outputs/results/inner_spatiotemporal_fold_definitions.csv` |
| Outer leakage audit | `outputs/results/spatiotemporal_leakage_audit.csv` |
| Inner leakage audit | `outputs/results/inner_spatiotemporal_leakage_audit.csv` |
| Hyperparameter search results | `outputs/results/spatiotemporal_hyperparameter_results.csv` |
| Best hyperparameters | `outputs/results/spatiotemporal_best_hyperparameters.csv` |

### Model Results
| File | Location |
|------|----------|
| Outer fold validation results | `outputs/results/spatiotemporal_validation_results.csv` |
| Summary metrics | `outputs/results/spatiotemporal_outer_fold_metrics.csv` |
| Per-class metrics | `outputs/results/final_per_class_metrics.csv` |
| Confusion matrices | `outputs/results/final_confusion_matrices.csv` |
| All predictions | `outputs/results/final_predictions.csv` |
| Calibration metrics | `outputs/results/final_calibration_metrics.csv` |
| Model training metadata | `outputs/results/model_training_metadata.json` |
| Feature columns | `outputs/results/final_feature_columns.json` |

### SHAP Outputs
| File | Location |
|------|----------|
| SHAP values | `outputs/explainability/revised_shap_values.csv` |
| SHAP importance | `outputs/explainability/revised_shap_importance.csv` |
| SHAP local examples | `outputs/explainability/revised_shap_local_examples.csv` |
| SHAP audit | `outputs/explainability/revised_shap_audit.csv` |

---

## 16. Requirement Checklist

| # | Requirement | Status | Evidence |
|---|-------------|--------|----------|
| 1 | Macroeconomic adjustment audit | DOCUMENTED LIMITATION | `macroeconomic_adjustment_audit.csv` — no CPI/exchange data available |
| 2 | Inner time-forward validation with audit trail | COMPLETE | `inner_spatiotemporal_fold_definitions.csv`, `inner_spatiotemporal_leakage_audit.csv` — 48 checks, all PASS |
| 3 | Genuine SHAP regeneration with hash verification | COMPLETE | `revised_shap_audit.csv` — old hash ≠ new hash, values changed = True |
| 4 | 2025–2026 data period resolution | COMPLETE | `year_coverage_audit.csv` — 0 valid modelling rows, documented exclusion |
| 5 | Model rebuild with SHA-256 hashing | COMPLETE | `model_training_metadata.json` — 3 models, all hashed and prediction-verified |
| 6 | Full metrics regeneration | COMPLETE | `spatiotemporal_validation_results.csv`, `spatiotemporal_outer_fold_metrics.csv` |
| 7 | All required audit CSV files | COMPLETE | See Section 15 inventory |
| 8 | Automated test suite passing | COMPLETE | 24/24 tests passed |
| 9 | Dashboard operational | COMPLETE | Streamlit running on `app/dashboard.py` |

---

## 17. Limitations and Honest Disclosures

1. **No CPI deflation**: Nominal prices are not adjusted for inflation. Within-currency SPI partially mitigates cross-currency comparison but does not remove intra-currency inflation effects. Secular inflation within a currency may cause the SPI to drift upward over time independently of genuine spatial price stress.

2. **No exchange-rate adjustment**: Prices in different currencies are compared only within their own currency group. No common real-price base was established.

3. **2025–2026 data excluded**: These years have raw records but produce zero valid modelling rows after data quality filters (thin-cell < 8 districts and reporting gaps > 2 months). This limits the temporal scope to 2017–2024.

4. **Class imbalance**: Target prevalence is 13.75%. XGBoost and LogReg use class-weight balancing to address this, but recall for the minority class remains moderate.

5. **District coverage varies by year**: 2018 and 2019 have very few modelling records (71 and 68 respectively), which may affect model generalisation for those periods.

6. **Inner validation district overlap**: Inner folds show non-zero district overlap counts in some cases (districts may appear in both inner training and inner validation). However, the key constraint — that outer test districts are excluded from all inner folds — is strictly enforced (all 48 checks PASS).

---

## 18. Final Readiness Status

### PARTIALLY READY — CORRECTIONS REQUIRED

The project is partially ready because:

- [x] The revised target (SPI > 1.25) was implemented
- [x] The eight-district thin-cell rule was implemented
- [x] Reporting gaps greater than two months were excluded
- [x] Forward-chaining outer spatio-temporal validation was implemented (3 folds, zero district/temporal overlap)
- [x] Inner time-forward hyperparameter tuning was implemented (2 inner folds per outer fold, 48 leakage checks all PASS)
- [x] Pipeline leakage controls were implemented (SimpleImputer and StandardScaler inside sklearn Pipeline, fit on training fold only)
- [x] The revised models were trained (Dummy, LogReg, XGBoost)
- [x] Revised metrics were generated (outer fold macro-F1, ROC-AUC, PR-AUC, Brier, confusion matrices, calibration)
- [x] Revised SHAP outputs were regenerated and verified (hash changed from old values, confirmed independent)
- [ ] **UNRESOLVED**: CPI deflation was not implemented — nominal prices were not adjusted for inflation
- [ ] **UNRESOLVED**: Exchange-rate adjustment was not implemented — no common real-price currency base was established

The remaining unresolved methodological issue is the absence of CPI or exchange-rate adjustment. Until verified CPI and exchange-rate series are obtained and integrated into the SPI calculation pipeline, this limitation must be explicitly discussed in the dissertation as a threat to the validity of temporal comparisons.

---

*This report was generated from verified pipeline outputs, model artefacts, audit CSVs, and test results. No values were invented or estimated.*
