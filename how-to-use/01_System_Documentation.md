# 01 · System Documentation

## 1. Purpose and scope

The **ZCPSC** is a research proof-of-concept that classifies **relative commodity-price
stress** for Zimbabwean districts. Its predictive question is:

> *Using only information available by the end of month **T**, what is the probability
> that a given commodity in a given district is under relative price stress in month
> **T+1**?*

The system is delivered as an interactive **Streamlit** web application backed by a
reproducible Python data-science pipeline.

**In scope:** interactive single and batch prediction, historical data exploration, model
explainability, methodology and limitations.

**Out of scope:** official IPC phase classification, household food-insecurity scoring,
real-time market feeds, and operational (non-prototype) decision use.

---

## 2. High-level architecture

```
┌────────────────────────────────────────────────────────────────────────────┐
│                              RAW DATA (read-only)                          │
│  HDX HAPI market prices · population · poverty · GeoBoundaries · CHIRPS     │
└────────────────────────────────────────────────────────────────────────────┘
                                     │
                                     ▼
┌────────────────────────────────────────────────────────────────────────────┐
│                        PIPELINE  (src/, config.py)                          │
│  ingest → preprocess → feature engineering → train → evaluate → explain     │
│  Authoritative entry point:  python -m src.run_option_b_pipeline            │
└────────────────────────────────────────────────────────────────────────────┘
                                     │  writes
                                     ▼
┌────────────────────────────────────────────────────────────────────────────┐
│                    ARTEFACTS  (outputs/option_b/)                           │
│  models/*.joblib · data/*.csv & *.json · results/*.csv · explainability/*   │
└────────────────────────────────────────────────────────────────────────────┘
                                     │  read (cached)
                                     ▼
┌────────────────────────────────────────────────────────────────────────────┐
│                       DASHBOARD  (Streamlit)                                │
│  app.py  →  pages/1..7  →  app/data_loader.py  →  app/styles.py/components  │
│  prediction_engine.OptionBPredictor  →  loaded joblib pipelines             │
└────────────────────────────────────────────────────────────────────────────┘
```

The dashboard is **presentation-only**: it never re-ingests CHIRPS, never retrains
models and never fabricates results. If an artefact is missing, the relevant page shows a
clear "missing artifact" / informational message instead of failing silently.

---

## 3. Technology stack

| Layer | Technology |
|-------|------------|
| Dashboard | Streamlit, Plotly (Express + Graph Objects) |
| Design system | Custom CSS injected from `app/styles.py` |
| Data access | pandas, cached with `st.cache_data` / `st.cache_resource` |
| Modelling | scikit-learn (`Pipeline`, `SimpleImputer`, `StandardScaler`, `LogisticRegression`, `DummyClassifier`), XGBoost |
| Explainability | SHAP `TreeExplainer` (with graceful fallback) |
| Geospatial | GeoPandas (district centroids / boundaries) |
| Config | `config.py` (single source of truth) + `.streamlit/config.toml` (theme) |

---

## 4. Repository layout

| Path | Role |
|------|------|
| `app.py` | Streamlit entry point. Configures the page and mounts the 7 pages via `st.navigation`. |
| `pages/1_Overview.py` … `pages/7_Limitations.py` | The seven dashboard pages. |
| `app/styles.py` | Global CSS + `COLORS` palette (`inject_css`, `page_header`, `sidebar_header/footer`, `disclaimer_banner`). |
| `app/components.py` | Reusable HTML components (KPI cards, prediction summary, workflow steps, probability meter). |
| `app/data_loader.py` | Cached readers for every pipeline artefact and model. |
| `app/charts.py`, `app/maps.py`, `app/dashboard.py` | **Legacy** modules from the earlier step-based dashboard. Not used by the current `app.py` app. |
| `src/prediction_engine.py` | `OptionBPredictor` — loads Option B models and scores single/batch observations. |
| `src/run_option_b_pipeline.py` | Authoritative Option B pipeline (data → model → evaluation → explainability). |
| `src/step01…step10_*.py` | The original, step-numbered pipeline (food-price-stress classifier). |
| `config.py` | Paths, study window, feature parameters, assumptions, dataset registry, colour palette. |
| `.streamlit/config.toml` | Streamlit theme (primary colour, background, text). |
| `outputs/option_b/` | All artefacts the dashboard reads (see §6). |
| `data/raw/` | Immutable raw inputs. |
| `data/processed/` | Regenerable intermediate tables. |
| `reports/` | Markdown evidence reports, one per pipeline step/topic. |
| `tests/` | Automated tests (leakage, target creation, SPI, acceptance, prediction interface). |

---

## 5. Runtime data flow (dashboard)

1. `app.py` calls `st.set_page_config`, then `app.styles.inject_css()`.
2. `st.navigation` registers the seven pages in the sidebar; the cloned environment
   injects `sidebar_header()` / `sidebar_footer()` branding.
3. A page runs and calls loaders in `app/data_loader.py`, which read CSVs/JSON/`joblib`
   from `outputs/option_b/` (and `outputs/results/` for the legacy tables).
4. `@st.cache_data` caches tabular reads; `@st.cache_resource` caches models, GeoPandas
   boundaries and the SHAP explainer so heavy objects load once per session.
5. On the prediction pages, `src/prediction_engine.OptionBPredictor` assembles a feature
   row and calls the fitted pipeline's `predict` / `predict_proba`.

---

## 6. Artefact catalogue (`outputs/option_b/`)

### Models — `models/`
| File | Description |
|------|-------------|
| `dummy_baseline.joblib` | Majority-class baseline. |
| `logreg_pipeline.joblib` | Logistic-regression pipeline (impute → scale → classify). |
| `xgboost_pipeline.joblib` | **Champion** XGBoost pipeline. |

### Data — `data/`
| File | Description |
|------|-------------|
| `option_b_feature_columns.json` | Ordered feature list, target name and horizon. |
| `option_b_modelling_table.csv` | Final modelling table (features + shifted target). |
| `option_b_prediction_template.csv` | Officially shaped CSV template for batch upload. |

### Results — `results/`
| File | Description |
|------|-------------|
| `option_b_model_metrics.csv` | Per-fold metrics for Dummy / LogisticRegression / XGBoost. |
| `option_b_predictions.csv` | Unified predictions (prediction_month → target_month). |
| `validation_audit.csv`, `target_shift_audit.csv`, `feature_availability_audit.csv`, `natural_key_audit.csv`, `model_configuration_audit.csv`, `sensitivity_analysis.csv` | Leakage, target-shift, feature-availability and sensitivity audits. |

### Explainability — `explainability/`
| File | Description |
|------|-------------|
| `option_b_shap_importance.csv` | Global mean |SHAP| per feature. |
| `option_b_local_explanations.csv` | Per-observation SHAP explanations. |

### Figures — `figures/`
`option_b_roc_curves.png`, `option_b_pr_curves.png`, `option_b_confusion_matrices.png`,
`option_b_calibration_curves.png`, `option_b_feature_importance.png`,
`option_b_shap_summary.png`, `option_b_target_distribution.png`.

### Logs — `logs/`
`pipeline_run.log` — full pipeline console log.

---

## 7. Configuration

### `config.py`
Central constants: project paths (`DATA_RAW`, `OUT_RES`, `OUT_MODELS`, …), the study
window (`STUDY_START`/`STUDY_END`), the April-2024 ZWL redenomination month, feature
engineering parameters (`RAINFALL_WINDOWS`, `PRICE_ROLLING_MONTHS`, …), the documented
`ASSUMPTIONS` list and the `DATASET_REGISTRY`.

### `.streamlit/config.toml`
```toml
[theme]
primaryColor="#147BB5"
backgroundColor="#F3F6FA"
secondaryBackgroundColor="#FFFFFF"
textColor="#172A40"
font="Inter"
```

### Design palette (`app/styles.py` `COLORS`)
Navy sidebar `#102F50`, primary blue `#147BB5`, teal `#21A99F`, green `#199B70`,
amber `#F0B83F`, red `#D94343`, page background `#F3F6FA`, cards `#FFFFFF`,
text `#172A40`, muted text `#748397`, borders `#E2E8F0`, and pale status backgrounds.
See [07_Developer_Guide.md](07_Developer_Guide.md) for the full token map.

---

## 8. Two "generations" of pipeline (important)

| | Legacy step pipeline | Option B pipeline (authoritative) |
|---|---|---|
| Scripts | `src/step01…step10` | `src/run_option_b_pipeline.py` |
| Target | `price_stress` (SPI > 1.0), concurrent | `target_next_month` (T → T+1 relative stress) |
| Runner | `python -m src.run_all` | `python -m src.run_option_b_pipeline` |
| Artefacts | `outputs/{results,models,figures}` | `outputs/option_b/{...}` |
| Used by dashboard | Partly (legacy loaders) | **Yes — the current 7-page app** |

The running dashboard (`app.py`) reads **Option B** artefacts.

---

## 9. Security, privacy and responsible use

- No external API keys, credentials or personal data are required at runtime.
- The maps use the tokenless Carto/MapLibre basemap (no Mapbox key needed).
- All data are aggregate, publicly sourced development/statistics datasets.
- The system is a decision-support **prototype** and must be interpreted alongside
  official data, expert judgement and wider food-security evidence.

See [06_Troubleshooting_and_FAQ.md](06_Troubleshooting_and_FAQ.md) and
[02_User_Manual.md](02_User_Manual.md) for day-to-day use.
