# Pre-Option B Cleanup Inventory Report

## 1. Executive Summary

This inventory catalogues all existing repository components prior to final Option B consolidation, identifying active assets, archived legacy components, and files tagged for review.

## 2. Source-Code Files Inventory

| File Path | Description | Topic Alignment | Action |
|---|---|---|---|
| `config.py` | Central configuration paths, constants, data registry | Shared / Config | Retain & update with Option B paths |
| `app.py` | Streamlit multipage application entry point | Option B | Active |
| `app/dashboard.py` | Streamlit unified dashboard application | Legacy / Option B | Maintain compatibility |
| `app/data_loader.py` | Cached data access layer | Shared / Option B | Active (contains dedicated Option B loaders) |
| `app/charts.py` | Plotly visualization helpers | Reusable | Retain |
| `app/maps.py` | Matplotlib / GeoPandas choropleth renderer | Reusable | Retain |
| `app/components.py` | UI card and KPI components | Reusable | Retain |
| `app/styles.py` | CSS styling and palette tokens | Reusable | Retain |
| `src/run_option_b_pipeline.py` | Authoritative Option B pipeline runner | Option B | Active Master Runner |
| `src/utils.py` | Shared canonical keys, loaders, SPI calculations | Shared | Retain |
| `src/step01_data_audit.py` to `step10_dashboard.py` | Original 10-step exploration scripts | Previous Topic | Archived in Git & `archive/previous_topic/` |
| `src/final_correction_pipeline.py` | Interim correction pipeline | Previous Topic | Archived |
| `src/train_spatiotemporal_revised.py` | Interim contemporaneous pipeline | Previous Topic | Archived |

## 3. Data Files Inventory

| File Path | Category | Status |
|---|---|---|
| `data/raw/hdx_hapi_food_price_zwe.csv` | Raw market prices | **Preserve permanently** (used by Option B) |
| `data/raw/hdx_hapi_population_zwe.csv` | Raw population baseline | **Preserve permanently** (used by Option B) |
| `data/raw/hdx_hapi_rainfall_zwe.csv` | Legacy FEWS NET rainfall | Preserve for EDA reference |
| `data/raw/hdx_hapi_poverty_rate_zwe.csv` | Province MPI survey | Preserve for EDA reference |
| `data/raw/geo/*` | geoBoundaries ADM1 & ADM2 polygons | **Preserve permanently** (used by Option B) |
| `data/processed/d_price_district_month.csv` | Cleaned price panel | **Preserve** (used in pipeline) |
| `data/processed/d_rainfall_chirps_district_month.csv` | CHIRPS district rainfall series | **Preserve** (used in pipeline) |
| `data/processed/d_population_district.csv` | Aggregated population baseline | **Preserve** (used in pipeline) |
| `outputs/option_b/data/option_b_modelling_table.csv` | Authoritative Option B modelling table | **Active Option B Asset** |
| `outputs/option_b/data/option_b_feature_columns.json` | Whitelist feature columns | **Active Option B Asset** |

## 4. Models & Outputs Inventory

| Category | Legacy Location | Option B Active Location | Status |
|---|---|---|---|
| Models | `models/` & `outputs/models/` | `outputs/option_b/models/` | Legacy archived; Option B active |
| Predictions | `outputs/results/` | `outputs/option_b/results/option_b_predictions.csv` | Segregated |
| Metrics | `outputs/results/` | `outputs/option_b/results/option_b_model_metrics.csv` | Segregated |
| Figures | `outputs/figures/` | `outputs/option_b/figures/` | Segregated |
| SHAP | `outputs/explainability/` | `outputs/option_b/explainability/` | Segregated |

## 5. Audit Conclusion
All legacy files have been safely captured under Git tag `previous-topic-archive` and `archive/previous_topic/`. Option B assets are completely segregated under `outputs/option_b/`.
