# Zimbabwe Food Price Stress — Machine Learning Pipeline

**Project:** Machine Learning Classification of Commodity-Level Food Price Stress in
Zimbabwean Districts Using CHIRPS Rainfall and Market Data.

The final modelling unit is **commodity × district × month**. Every step is a standalone,
numbered script; run them in order (or via `python -m src.run_all`).

## Project structure

```
another/
├─ config.py                      # paths, constants, assumptions (single source of truth)
├─ README.md
├─ data/
│  ├─ raw/                        # RAW INPUTS — never edited
│  │  ├─ hdx_hapi_food_price_zwe.csv
│  │  ├─ hdx_hapi_population_zwe.csv
│  │  ├─ hdx_hapi_poverty_rate_zwe.csv
│  │  ├─ hdx_hapi_rainfall_zwe.csv
│  │  ├─ chirps_v3_monthly_global.nc     # CHIRPS v3 gridded rainfall (8.5 GB)
│  │  ├─ DataDetails.xls
│  │  └─ geo/                     # geoBoundaries ADM1 / ADM2
│  └─ processed/                  # GENERATED — safe to delete and regenerate
├─ src/
│  ├─ utils.py                    # shared helpers (config-aware I/O, SPI, plotting)
│  ├─ step01_data_audit.py
│  ├─ step02_preprocess.py
│  ├─ step03_ingest_rainfall.py
│  ├─ step04_build_training_table.py
│  ├─ step05_eda.py
│  ├─ step06_feature_selection.py
│  ├─ step07_model_training.py
│  ├─ step08_model_evaluation.py
│  ├─ step09_explainability.py
│  ├─ step10_dashboard.py
│  └─ run_all.py
├─ app/
│  ├─ dashboard.py                # Streamlit entry point (7-page app)
│  ├─ data_loader.py              # cached data/model access layer
│  ├─ charts.py                   # reusable Plotly charts
│  ├─ maps.py                     # district choropleth (GeoPandas + Matplotlib)
│  ├─ components.py               # UI components (cards, panels, warnings)
│  └─ styles.py                   # theme + shared strings
├─ outputs/
│  ├─ figures/                    # PNG figures
│  ├─ results/                    # CSV tables / audits
│  ├─ models/                     # trained model artifacts (.joblib)
│  └─ _stepNN_log.txt             # per-step run logs
└─ reports/                       # Markdown reports (one per step)
```

## Pipeline

| Step | Script | Produces |
|---|---|---|
| 1 | `step01_data_audit.py` | Raw-source profiles, missingness/missing reports, `reports/step01_data_audit.md` |
| 2 | `step02_preprocess.py` | Cleaned tables `d_*.csv` (poverty, population, rainfall, price panel, basket, district base) |
| 3 | `step03_ingest_rainfall.py` | CHIRPS → `d_rainfall_chirps_district_month.csv` (district × month, 1981–present) |
| 4 | `step04_build_training_table.py` | `commodity_training_table.csv` (final training table) |
| 5 | `step05_eda.py` | EDA figures + `reports/step05_eda.md` |
| 6 | `step06_feature_selection.py` | Feature ranking + `selected_features.json` |
| 7 | `step07_model_training.py` | CV results + fitted models |
| 8 | `step08_model_evaluation.py` | Held-out metrics, predictions, confusion matrices, ROC/PR curves |
| 9 | `step09_explainability.py` | Permutation importance (+ SHAP if available) |
| 10 | `step10_dashboard.py` | Verifies the dashboard app files + artefacts (does not overwrite `app/`) |

## How to run

```powershell
# everything (recommended)
python -m src.run_all

# or a single step
python src/step04_build_training_table.py

# dashboard
streamlit run app/dashboard.py
```

## Dashboard

Research proof-of-concept decision-support app for **commodity-level food price stress**
(`price_stress = 1` when the spatial price index exceeds 1.0). It only reads pipeline outputs;
it never re-runs CHIRPS ingestion, retrains models, or fabricates results.

Pages:

1. **Home** — headline cards + latest price-stress map.
2. **Price Stress Map** — filter by commodity / province / district / month / model; colour by
   predicted class or probability.
3. **District & Commodity Detail** — classification summary, price history, rainfall analysis,
   probability over time, a **per-observation SHAP explanation** (XGBoost) showing features
   increasing vs decreasing price stress, and feature values.
4. **Model Insights** — held-out metrics, cross-validation, interactive confusion matrix,
   ROC/PR curves, and feature importance (SHAP / permutation / mutual information / XGBoost native).
5. **Data Explorer** — filterable table with column selector and CSV download.
6. **Methodology** — pipeline, modelling unit, target and data sources.
7. **About / Limitations** — purpose, intended users, limitations.

SHAP is used when importable. Step 9 computes XGBoost SHAP values with the fast
`TreeExplainer`; the Model Insights page shows global mean |SHAP| and the Detail page shows the
per-observation breakdown. If a host blocks scikit-learn's `_gradient_boosting` DLL, SHAP import
fails (`shap` imports `sklearn.ensemble`); step 9 then saves permutation importance only and the
dashboard labels that as *not* SHAP. The binary target has no "medium" category, so maps use red
(high) / green (low) only.

## Requirements

`pandas`, `numpy`, `geopandas`, `xarray`, `netCDF4`, `matplotlib`, `seaborn`, `scikit-learn`,
`xgboost`, `shap`, `streamlit`, `plotly`, `joblib`.

> **Environment note:** Windows Application Control intermittently blocked scikit-learn's
> `_gradient_boosting` DLL on this machine, which broke `RandomForest`/`GradientBoosting` and,
> transitively, `import shap`. The pipeline therefore uses `LogisticRegression` and `XGBoost`
> and falls back from SHAP to permutation importance, so it runs whether or not the DLL is
> available. Where the policy is not active (as in the current environment) SHAP works and is
> used.

## Key assumptions (full list in `config.py`)

- **Commodity-level grain** is the primary modelling unit.
- Rainfall is **district-level** from CHIRPS v3 (1981–present); the legacy province-level FEWS
  NET table is retained as a fallback.
- Poverty is **province-level and time-invariant** (latest survey wave).
- Target: `price_stress = 1 if spatial_price_index > 1.0 else 0`.
- CV: `StratifiedKFold` (reference) **and** `GroupKFold` by district (primary, leakage-safe).
