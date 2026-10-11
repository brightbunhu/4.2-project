# Option B Reference and Claim Audit

## 1. Purpose & Scope

This audit verifies all scientific claims, references, and empirical facts asserted in Chapters 1–4 of the dissertation against the empirical code and output files generated under Option B.

## 2. Empirical Verification Audit Matrix

| Dissertation Assertion | Empirical Source | Verification Status | Fact / Metric |
|---|---|---|---|
| **Predictive Horizon** | `outputs/option_b/data/option_b_modelling_table.csv` | **VERIFIED** | $\text{target\_month} = \text{prediction\_month} + 1 \text{ month}$ strictly enforced. |
| **Observation Unit** | `outputs/option_b/results/natural_key_audit.csv` | **VERIFIED** | Natural key: `district_key + commodity_name + prediction_month + currency_code`. Zero duplicates. |
| **SPI Thin-Cell Guard** | `src/run_option_b_pipeline.py` | **VERIFIED** | Threshold $\ge 8$ reporting districts. 2,045 thin cells filtered from medians. |
| **Operational Threshold** | `outputs/option_b/results/sensitivity_analysis.csv` | **VERIFIED** | $\text{SPI} > 1.25$ operational stress threshold (13.70% overall prevalence). |
| **Zero Future Leakage** | `outputs/option_b/results/feature_availability_audit.csv` | **VERIFIED** | All 23 predictors satisfy $\text{information\_date} \le T$. |
| **Forward Temporal CV** | `outputs/option_b/results/validation_audit.csv` | **VERIFIED** | 3 expanding folds; $\max(T_{\text{train}}) < \min(T_{\text{test}})$ in all folds. |
| **Baseline Superiority** | `outputs/option_b/results/option_b_model_metrics.csv` | **VERIFIED** | XGBoost (Macro-F1 0.6200) and LogReg (0.5921) exceed Dummy (0.4479). |
| **Explainability Method** | `outputs/option_b/explainability/option_b_shap_importance.csv` | **VERIFIED** | TreeSHAP computed on production XGBoost pipeline. |
| **Non-Claims Compliance** | `reports/option_b_limitations.md` | **VERIFIED** | Excludes household food security, IPC phase assignment, and causal rainfall claims. |
