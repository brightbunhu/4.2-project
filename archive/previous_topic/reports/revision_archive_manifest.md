# Revision Archive Manifest

This document records all pre-revision model artifacts, evaluation outputs, and result files that have been safely archived to `archive/pre_revision_outputs/` following formal examination feedback.

## Archive Manifest Table

| Old File Path | Archived Path | Reason for Archiving | Used in Old Dissertation? | Exclude from Revised Dissertation? |
|---|---|---|---|---|
| `outputs/models/step07_dummy.joblib` | `archive/pre_revision_outputs/models/step07_dummy.joblib` | Superseded by revised spatio-temporal target/split model | Yes | Yes |
| `outputs/models/step07_logreg.joblib` | `archive/pre_revision_outputs/models/step07_logreg.joblib` | Superseded by revised spatio-temporal target/split model | Yes | Yes |
| `outputs/models/step07_xgboost.joblib` | `archive/pre_revision_outputs/models/step07_xgboost.joblib` | Superseded by revised spatio-temporal target/split model | Yes | Yes |
| `outputs/results/nested_groupkfold_results.csv` | `archive/pre_revision_outputs/results/nested_groupkfold_results.csv` | Old GroupKFold results replaced by forward-chaining spatio-temporal validation | Yes | Yes |
| `outputs/results/best_hyperparameters.csv` | `archive/pre_revision_outputs/results/best_hyperparameters.csv` | Old hyperparameter search results under SPI > 1.0 | Yes | Yes |
| `outputs/results/step08_model_comparison.csv` | `archive/pre_revision_outputs/results/step08_model_comparison.csv` | Old evaluation metrics under SPI > 1.0 | Yes | Yes |
| `outputs/results/step09_shap_values.csv` | `archive/pre_revision_outputs/results/step09_shap_values.csv` | Old SHAP values computed under legacy model | Yes | Yes |
| `outputs/results/step09_shap_importance.csv` | `archive/pre_revision_outputs/results/step09_shap_importance.csv` | Old SHAP feature importances | Yes | Yes |
