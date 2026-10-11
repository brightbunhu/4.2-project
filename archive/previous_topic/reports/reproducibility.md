# Reproducibility
1. Run preprocessing: python src/step01_data_audit.py; python src/step02_preprocess.py; python src/step03_ingest_rainfall.py
2. Build table: python src/step04_build_training_table.py
3. EDA/selection: python src/step05_eda.py; python src/step06_feature_selection.py
4. Train/eval: python src/step07_model_training.py; python src/step08_model_evaluation.py
5. Explainability: python src/step09_explainability.py
6. Dashboard: streamlit run app/dashboard.py
