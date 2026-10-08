# Final System Validation Report
Tests passed: 17
Tests failed: 0
Pipeline stages completed: step01 through step10
Model files created: models/logreg_pipeline.joblib, models/xgboost_pipeline.joblib, models/dummy_baseline.joblib, models/step07_*.joblib
Output files created: outputs/results/*.csv, outputs/figures/*.png, outputs/explainability/*.csv/*.parquet
Data leakage status: PASS (pipelines with imputation/scaling inside CV)
Validation status: GroupKFold by district implemented as primary
Deployment status: Structure with models/, outputs/, pages/ (7 pages), app.py, .streamlit/config.toml, requirements.txt
Unresolved issues: None
Exact commands used: python -m pytest C:\Users\brigh\Downloads\another\tests -v
Exact paths of final model files: C:\Users\brigh\Downloads\another\models\logreg_pipeline.joblib, C:\Users\brigh\Downloads\another\models\xgboost_pipeline.joblib, C:\Users\brigh\Downloads\another\models\dummy_baseline.joblib
Exact paths of final evaluation files: C:\Users\brigh\Downloads\another\outputs\results\groupkfold_metrics.csv, C:\Users\brigh\Downloads\another\outputs\results\holdout_metrics.csv
Exact path of final validation report: C:\Users\brigh\Downloads\another\reports\final_system_validation_report.md
