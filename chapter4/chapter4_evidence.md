# Chapter 4 Evidence: Results and Findings

## 1. Evidence generation information

- Date and time: 2026-10-06 12:54:36
- Python version: 3.12.10 (tags/v3.12.10:0cc8128, Apr  8 2025, 12:21:36) [MSC v.1943 64 bit (AMD64)]
- Operating system: Windows
- Final pipeline command: python src/final_correction_pipeline.py
- Test command: python -m pytest -v

## 5. Dataset summary

- Total observations: 10107
- Columns: 39
- Date range: 2017-01-01 to 2024-10-01
- Distinct district_key: 81
- Distinct commodity_name: 18
- Distinct currency_code: 2
- price_stress=1: 1390 (13.8%)
- price_stress=0: 8717 (86.2%)


## 9. Model-performance results

- dummy: acc=0.862, bacc=0.500, macrof1=0.463, rocauc=0.500, prauc=0.138
- logreg: acc=0.857, bacc=0.823, macrof1=0.756, rocauc=0.901, prauc=0.627
- xgboost: acc=0.924, bacc=0.777, macrof1=0.817, rocauc=0.948, prauc=0.796


## 17. Reproducibility checklist

- Final pipeline completed: yes
- Tests completed: yes (24 passed)
- Results generated: yes
- Figures generated: yes (13)
- Tables generated: yes
- Models serialized: yes
- SHAP completed: yes
- Dashboard inspected: yes
- No results invented: confirmed
- No raw data deleted: confirmed
