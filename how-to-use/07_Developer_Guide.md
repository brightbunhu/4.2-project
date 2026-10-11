# 07 · Developer Guide

For anyone reading, extending, re-styling or debugging the code.

---

## 1. Code map

| File | Responsibility |
|------|----------------|
| `app.py` | Entry point. `st.set_page_config`, `inject_css()`, then `st.navigation` mounting the 7 pages, with sidebar header/footer. |
| `pages/1..7_*.py` | One file per dashboard page. Each is a standalone Streamlit script that imports shared helpers. |
| `app/styles.py` | `COLORS` palette + injected `_CSS`; helpers `inject_css`, `page_header`, `sidebar_header`, `sidebar_footer`, `disclaimer_banner`. |
| `app/components.py` | Reusable HTML builders: `render_html`, `kpi_card`, `prediction_summary_card`, `workflow_steps`, `probability_meter`. |
| `app/data_loader.py` | `@st.cache_data` / `@st.cache_resource` readers for every artefact. |
| `src/prediction_engine.py` | `OptionBPredictor` — model loading + feature assembly + scoring. |
| `src/run_option_b_pipeline.py` | Authoritative Option B pipeline. |
| `config.py` | Paths, constants, `ASSUMPTIONS`, `DATASET_REGISTRY`. |
| `tests/` | Pytest suites. |

---

## 2. Page loading pattern

Every page starts with the same preamble so it works both under `app.py` and when run
directly:

```python
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
from app.styles import inject_css, page_header, disclaimer_banner

inject_css()
page_header(title="…", subtitle="…")
```

`app.py` registers the pages (order = sidebar order):

```python
pg = st.navigation([...])   # the 7 pages
pg.run()
```

---

## 3. Design tokens (`app/styles.py`)

`COLORS` is the single palette consumed by CSS and components:

| Token | Hex | Use |
|-------|-----|-----|
| navy | `#102F50` | sidebar background |
| navy_dark | `#0B2743` | responsible-use banner |
| blue | `#147BB5` | primary actions / links |
| blue_active | `#1676B8` | active nav item |
| teal | `#21A99F` | neutral charts / low risk |
| green | `#199B70` | valid / success |
| amber | `#F0B83F` | moderate / warning |
| red | `#D94343` | high risk / error |
| bg | `#F3F6FA` | page background |
| card | `#FFFFFF` | card surfaces |
| text | `#172A40` | primary text |
| text_muted | `#748397` | secondary text |
| border | `#E2E8F0` | borders |
| pale_blue / pale_green / pale_amber / pale_red | `#EAF4FC` / `#E8F6EF` / `#FFF4D6` / `#FCEBEC` | status chip backgrounds |
| sidebar_text_muted | `#C8D6E4` | sidebar muted text |

### Change the theme
1. **App-wide theme:** edit `.streamlit/config.toml` (`primaryColor`, `backgroundColor`,
   `secondaryBackgroundColor`, `textColor`, `font`).
2. **CSS/components:** edit `COLORS` in `app/styles.py`. Inline colours in pages/components
   should reference these values to stay consistent.

> Note: `app/charts.py`, `app/maps.py`, `app/dashboard.py` and the `PALETTE` in `config.py`
> are from the **legacy** dashboard and are not used by the current app.

---

## 4. Data access (`app/data_loader.py`)

Always read artefacts through the loaders; do not read CSVs directly in pages.

| Loader | Returns |
|--------|---------|
| `load_option_b_predictions()` | `option_b_predictions.csv` (prediction_month → target_month) |
| `load_option_b_modelling_table()` | `option_b_modelling_table.csv` |
| `load_training_table()` | legacy training table (fallback) |
| `load_geo()` | district geometry (GeoDataFrame) for centroids/maps |
| `load_option_b_shap_importance()` | global SHAP importance |
| `load_option_b_local_explanations()` | per-observation SHAP |

Loaders are cached with `st.cache_data` (tables) and `st.cache_resource` (models, geo,
explainer). To bust the cache press **C** in the app or restart Streamlit.

---

## 5. Prediction engine API (`src/prediction_engine.py`)

```python
from src.prediction_engine import OptionBPredictor

predictor = OptionBPredictor()           # loads metadata + models once

predictor.districts                     # approved district keys
predictor.commodities                   # approved commodities
predictor.currencies                    # approved currencies
predictor.features                      # ordered feature list
predictor.compute_target_month(ts)      # returns T+1 month (handles December wrap)
predictor.derive_features_for_unit(district, commodity, currency, pred_month)
predictor.predict_single(district, commodity, currency, pred_month,
                         feature_overrides=None, model_name="XGBoost")
predictor.validate_csv(df_upload)       # -> (valid_df, invalid_df, error_df)
predictor.predict_batch(valid_df, model_name="XGBoost")
predictor.generate_csv_template()       # -> CSV string
```

`predict_single` returns a dict with keys:
`prediction_month`, `target_month`, `district`, `commodity`, `currency`, `model_name`,
`model_version`, `predicted_class`, `predicted_label`, `predicted_probability`,
`explanation` (`top_increasing`, `top_decreasing`, `disclaimer`), `interpretation`,
`disclaimer`.

`predict_batch` returns a DataFrame with:
`observation_id`, `prediction_month`, `target_month`, `district_key`, `commodity_name`,
`currency_code`, `predicted_class`, `predicted_label`, `predicted_probability`,
`model_name`, `model_version`, `validation_status`, `prediction_status`.

---

## 6. Wiring the prediction engine

The engine is correct; the **pages currently call it with mismatched names**, so the UI
falls back to sample values (see
[06_Troubleshooting_and_FAQ.md §6](06_Troubleshooting_and_FAQ.md#6-current-integration-status)).
To enable live scoring, align the page calls with the engine's real API.

**Page 2 — single prediction** (`pages/2_Next_Month_Prediction.py`):

```python
pred_res = predictor.predict_single(
    district=sel_district,
    commodity=sel_comm,
    currency=sel_curr,
    pred_month=p_month_ts,                       # NOTE: pred_month, not prediction_month
    feature_overrides={"spi_lag_1": val_spi,     # NOTE: feature_overrides, not overrides
                        "rainfall_3m_total": val_rain},
    model_name="XGBoost",                        # NOTE: "XGBoost", not "xgboost"
)
prob  = pred_res["predicted_probability"]        # not "probability"
klass = pred_res["predicted_class"]              # not "prediction"
expl  = pred_res["explanation"]                  # dict, not "top_features"
```

Also note the engine derives `log_population` (not raw `population`); map the page's
"Population" input to `np.log(pop)` in `feature_overrides` if you want it to take effect.

**Page 3 — batch prediction** (`pages/3_CSV_Batch_Prediction.py`):

```python
valid_df, invalid_df, error_df = predictor.validate_csv(user_df)
results = predictor.predict_batch(valid_df, model_name="XGBoost")
```

There is **no `validate_batch_dataframe`** method; use `validate_csv`. The engine template
(`generate_csv_template`) uses identifier columns `district_key`, `commodity_name`,
`currency_code`, `prediction_month` — make the download template match it so uploaded files
validate cleanly.

> Tip: replace the broad `except Exception:` fallbacks with narrower handling so wiring bugs
> surface instead of silently showing sample numbers.

---

## 7. Add a new page

1. Create `pages/8_My_Page.py` using the preamble from §2.
2. Add it to the `st.navigation([...])` list in `app.py` (order controls sidebar order).
3. Reuse `page_header`, `kpi_card`, `render_html`, and the loaders.
4. Add a test (see §9) and update the file lists in this folder's docs.

---

## 8. Configuration (`config.py`)

Key items: `DATA_RAW`, `DATA_PROCESSED`, `OUT_RES`/`OUT_MODELS`/`OUT_FIGS`, the study window,
the April-2024 redenomination month, rainfall/rolling-window parameters, `ASSUMPTIONS`
(documented modelling assumptions) and `DATASET_REGISTRY` (raw input paths). Option B paths
(`outputs/option_b/...`) are defined at the top of `src/run_option_b_pipeline.py` and
`src/prediction_engine.py`.

---

## 9. Testing

```powershell
python -m pytest -v
python -m pytest tests/test_option_b_acceptance.py -v
python -m pytest tests/test_prediction_interface.py -v
python -m pytest tests/test_dashboard_loading.py -v
```

Relevant suites:

| Test | Guards |
|------|--------|
| `test_no_data_leakage.py`, `test_no_current_price_leakage.py` | leakage prevention |
| `test_target_creation.py`, `test_nested_validation.py` | target/variable construction |
| `test_spi_calculation.py`, `test_reporting_gap.py` | feature maths |
| `test_saved_model_loading.py`, `test_prediction_interface.py` | model load + API contract |
| `test_option_b_acceptance.py` | end-to-end Option B acceptance |
| `test_dashboard_loading.py` | dashboard can load artefacts |

Streamlit UI smoke tests can use `streamlit.testing.v1.AppTest`:

```python
from streamlit.testing.v1 import AppTest
at = AppTest.from_file("pages/1_Overview.py", default_timeout=30).run()
assert not at.exception
```

---

## 10. Conventions in this codebase

- No comments unless necessary; prefer clear names and section banners.
- Pages are independent scripts; keep shared logic in `app/` or `src/`.
- All colours come from the `COLORS` palette.
- Read data only through `app/data_loader.py`.
- Keep the pipeline authoritative: regenerate rather than hand-edit artefacts.
- Update docs in `how-to-use/` when you change behaviour, paths or the palette.
