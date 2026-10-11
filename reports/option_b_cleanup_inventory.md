# Option B Cleanup Inventory

## 1. Summary of Archival & Cleanup Actions

- **Git Archive Tag Created:** `previous-topic-archive`
- **Archive Folder Created:** `archive/previous_topic/`
- **Legacy Files Archived:**
  - 10 historical step reports and validation summaries copied to `archive/previous_topic/reports/`
  - Legacy model artifacts copied to `archive/previous_topic/outputs/models/`
  - Legacy evaluation tables and figures copied to `archive/previous_topic/outputs/`
- **Raw Data Integrity:** 100% of raw inputs in `data/raw/` intact and preserved.
- **Option B Separation:** Clean dedicated directory hierarchy in `outputs/option_b/` containing only shifted-target ($T \to T+1$) artifacts.

## 2. Status of Output Directories

```text
outputs/option_b/
├── data/
│   ├── option_b_modelling_table.csv       [6,908 observations, verified zero leakage]
│   └── option_b_feature_columns.json      [23 approved predictor columns]
├── models/
│   ├── dummy_baseline.joblib              [Baseline model]
│   ├── logreg_pipeline.joblib             [Pipeline: SimpleImputer + StandardScaler + LogisticRegression]
│   └── xgboost_pipeline.joblib            [Pipeline: SimpleImputer + XGBClassifier]
├── results/
│   ├── natural_key_audit.csv              [Zero duplicate keys confirmed]
│   ├── target_shift_audit.csv             [Exact T+1 calendar lag confirmed]
│   ├── feature_availability_audit.csv     [All 23 features pass availability audit]
│   ├── validation_audit.csv               [3-fold expanding temporal validation]
│   ├── model_configuration_audit.csv      [Hyperparameter and architecture specs]
│   ├── option_b_predictions.csv           [Out-of-sample predictions and probabilities]
│   ├── option_b_model_metrics.csv         [Class-aware metrics across all folds]
│   └── sensitivity_analysis.csv           [Robustness across SPI 1.20, 1.25, 1.30]
├── figures/
│   ├── option_b_roc_curves.png
│   ├── option_b_pr_curves.png
│   ├── option_b_confusion_matrices.png
│   ├── option_b_calibration_curves.png
│   ├── option_b_feature_importance.png
│   ├── option_b_shap_summary.png
│   └── option_b_target_distribution.png
├── explainability/
│   ├── option_b_shap_importance.csv       [Mean |TreeSHAP| values]
│   └── option_b_local_explanations.csv    [Local per-observation primary feature contributions]
└── logs/
    └── pipeline_run.log                   [Complete timestamped execution log]
```
