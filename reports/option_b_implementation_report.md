# Option B Implementation Report: Machine Learning Pipeline Execution

## 1. Project Identity & Architecture

- **Project Title:** Machine Learning-Based Prediction of Next-Month Relative Commodity Price Stress in Zimbabwean Districts Using Market, Rainfall and Population Data
- **System Name:** Zimbabwe Commodity Price Stress Classifier (ZCPSC) — Option B
- **System Type:** Academic data-science and informatics prototype
- **Predictive Task:**
  $$\text{Information available by month } T \longrightarrow \text{Target relative price stress at month } T+1$$

## 2. Implementation Execution Summary

The complete Option B pipeline was executed via `src/run_option_b_pipeline.py`. All produced artifacts have been written to dedicated subdirectories under `outputs/option_b/`:

```text
outputs/option_b/
├── data/
│   ├── option_b_modelling_table.csv       (6,908 rows x 23 features + identifiers)
│   └── option_b_feature_columns.json      (Feature whitelist & metadata)
├── models/
│   ├── dummy_baseline.joblib              (DummyClassifier baseline)
│   ├── logreg_pipeline.joblib             (Imputer + Scaler + LogisticRegression)
│   └── xgboost_pipeline.joblib            (Imputer + XGBClassifier)
├── results/
│   ├── natural_key_audit.csv              (Verification of zero key duplicates)
│   ├── target_shift_audit.csv             (Exact T+1 calendar shift audit)
│   ├── feature_availability_audit.csv     (Leakage audit across all 23 predictors)
│   ├── validation_audit.csv               (Expanding temporal split parameters)
│   ├── model_configuration_audit.csv      (Hyperparameter and pipeline audit)
│   ├── option_b_predictions.csv           (Out-of-sample predictions & probabilities)
│   ├── option_b_model_metrics.csv         (Full class-aware cross-validation metrics)
│   └── sensitivity_analysis.csv           (Robustness audit for SPI 1.20, 1.25, 1.30)
├── figures/
│   ├── option_b_roc_curves.png            (ROC curves for Dummy, LogReg, XGBoost)
│   ├── option_b_pr_curves.png             (PR curves with prevalence baselines)
│   ├── option_b_confusion_matrices.png    (Confusion matrices on held-out data)
│   ├── option_b_calibration_curves.png    (Calibration curves for LogReg & XGBoost)
│   ├── option_b_feature_importance.png    (Top 12 global SHAP importance)
│   ├── option_b_shap_summary.png          (SHAP beeswarm distribution plot)
│   └── option_b_target_distribution.png   (Prevalence timeline 2017–2024)
├── explainability/
│   ├── option_b_shap_importance.csv       (Ranked global mean |SHAP| values)
│   └── option_b_local_explanations.csv    (Per-observation primary feature contributions)
└── logs/
    └── pipeline_run.log                   (Complete timestamped execution log)
```

## 3. Predictor Feature Set & Leakage Resistance

The final modelling table incorporates 23 valid features, all verified to satisfy:
$$\text{feature\_information\_date} \le \text{prediction\_month } T$$

### Feature Breakdown
1. **Market History (at Month T):**
   - `spi_lag_1`: Relative price index at $T-1$
   - `spi_lag_2`: Relative price index at $T-2$
   - `spi_pct_change_3m`: 3-month rolling percentage change in SPI ending at $T$
   - `months_since_last_reported_price`: Time gap between last reported observation and month $T$
2. **Rainfall Context (ending at Month T):**
   - `rainfall_1m`: Total monthly rainfall at month $T$
   - `rainfall_3m_total`: 3-month rolling rainfall ending at month $T$
   - `rainfall_6m_total`: 6-month rolling rainfall ending at month $T$
   - `rainfall_12m_total`: 12-month rolling rainfall ending at month $T$
   - `rainfall_3m_anomaly`: Normalized rainfall anomaly ending at month $T$
3. **Contextual & Temporal Features:**
   - `log_population`: District baseline log population
   - `is_urban`: Urban district classification indicator
   - `month_of_year`: Calendar month of prediction date $T$ (captures seasonality)
   - `year`: Observation year
4. **Commodity Encodings:**
   - 10 one-hot indicators for top commodities: maize grain, maize meal, cooking oil, sugar, beans, salt, bread, rice, flour, kapenta.

### Forbidden Predictors Audit
The pipeline enforced automated assertions confirming that:
- Target-month price is **EXCLUDED**.
- Target-month SPI is **EXCLUDED**.
- Target-month price stress is **EXCLUDED**.
- Contemporaneous price and raw SPI at month $T$ are excluded from model inputs.

## 4. Model Training & Validation Protocol

- **Validation Structure:** 3 expanding temporal folds (Forward-Chaining):
  - **Fold 1:** Train: Jan 2017 – Feb 2021 (3,427 rows) $\to$ Test: Mar 2021 – Oct 2022 (1,449 rows)
  - **Fold 2:** Train: Jan 2017 – Oct 2022 (4,876 rows) $\to$ Test: Nov 2022 – Jul 2023 (1,203 rows)
  - **Fold 3:** Train: Jan 2017 – Jul 2023 (6,079 rows) $\to$ Test: Aug 2023 – Sep 2024 (829 rows)
- **Temporal Order:** All training periods strictly precede evaluation periods ($\max(T_{\text{train}}) < \min(T_{\text{test}})$).
- **Leakage Safeguard:** All imputers and scalers were embedded inside pipeline objects and fitted solely on the outer training set of each fold.
