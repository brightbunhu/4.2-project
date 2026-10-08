# Option B Reproducibility Report

## 1. System Environment & Execution Specification

- **Host Operating System:** Microsoft Windows 11 Enterprise (AMD64)
- **Python Version:** 3.14.3 (64-bit)
- **Core Scientific Libraries:**
  - `pandas`: 3.0.2
  - `numpy`: 2.4.4
  - `scikit-learn`: 1.8.0
  - `xgboost`: 3.4.1
  - `shap`: 0.52.0
  - `streamlit`: 1.65.0
  - `pytest`: 9.1.1
  - `geopandas`: 1.1.4
  - `joblib`: 1.5.3

## 2. Deterministic Pipeline Execution

- **Random State:** Fixed at `42` across all model initializations, cross-validation splits, and bagging operations.
- **Master Execution Command:**
  ```powershell
  python src/run_option_b_pipeline.py
  ```
- **Test Suite Command:**
  ```powershell
  python -m pytest -v
  ```
- **Dashboard Command:**
  ```powershell
  streamlit run app.py
  ```

## 3. Persistent Output Artifact Directories

```text
outputs/option_b/
├── data/option_b_modelling_table.csv
├── data/option_b_feature_columns.json
├── models/dummy_baseline.joblib
├── models/logreg_pipeline.joblib
├── models/xgboost_pipeline.joblib
├── results/natural_key_audit.csv
├── results/target_shift_audit.csv
├── results/feature_availability_audit.csv
├── results/validation_audit.csv
├── results/model_configuration_audit.csv
├── results/option_b_predictions.csv
├── results/option_b_model_metrics.csv
├── results/sensitivity_analysis.csv
├── figures/option_b_roc_curves.png
├── figures/option_b_pr_curves.png
├── figures/option_b_confusion_matrices.png
├── figures/option_b_calibration_curves.png
├── figures/option_b_feature_importance.png
├── figures/option_b_shap_summary.png
├── figures/option_b_target_distribution.png
├── explainability/option_b_shap_importance.csv
├── explainability/option_b_local_explanations.csv
└── logs/pipeline_run.log
```

## 4. Reproducibility Verification
Running `python src/run_option_b_pipeline.py` executes end-to-end deterministically in $\sim 7$ seconds, regenerating identical row counts (6,908 rows in modelling table), exact matching metrics, TreeSHAP importance values, and diagnostic figures.
