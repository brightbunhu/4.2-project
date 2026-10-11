# 03 · Installation & Setup

Everything needed to get from a clean checkout to a running dashboard, on **Windows +
PowerShell** (adapt paths on macOS/Linux).

---

## 1. Prerequisites

| Requirement | Notes |
|-------------|-------|
| **Python 3.10–3.12** | 3.12 recommended. Some optional geospatial wheels are not yet built for 3.13/3.14. |
| **pip** | Ships with Python. |
| **Git** (optional) | Only if cloning. |
| **~2 GB free disk** | For dependencies (XGBoost, geopandas, etc.) and artefacts. |
| **No API keys** | The dashboard needs no Mapbox/other tokens (maps use a tokenless basemap). |

Check your version:

```powershell
python --version
```

---

## 2. Get the code and create a virtual environment

```powershell
# from the repository root
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, allow scripts for this session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

---

## 3. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

`requirements.txt` covers: pandas, numpy, scikit-learn, xgboost, shap, geopandas, plotly,
matplotlib, seaborn, streamlit, joblib, xarray, netCDF4, scipy, pyarrow.

> **Geospatial on Windows:** if `pip install geopandas` fails, install the
> [GDAL/Fiona wheels from the `geopandas` docs](https://geopandas.org/en/stable/getting_started/install.html)
> (or use conda: `conda install -c conda-forge geopandas`). See
> [06_Troubleshooting_and_FAQ.md](06_Troubleshooting_and_FAQ.md).

---

## 4. Raw data (only needed to regenerate artefacts)

The dashboard reads **pre-computed artefacts** in `outputs/option_b/`. If those are already
present (e.g. shipped with the project or a previous pipeline run), you can **skip** this
section and go to §6.

To run the full pipeline from scratch you need the raw inputs in `data/raw/`:

| Source | Role | Expected location (per `config.py`) |
|--------|------|-------------------------------------|
| HDX HAPI market prices | commodity prices | `data/raw/…` (see `config.DATASET_REGISTRY`) |
| Population (UNFPA census) | population / urban flag | `data/raw/…` |
| Poverty reference | context | `data/raw/…` |
| geoBoundaries ZWE ADM1/ADM2 | district geometry | `data/raw/…` |
| CHIRPS v3 rainfall (NetCDF) | rainfall features | `data/raw/…` |

Open `config.py` and confirm each `DATASET_REGISTRY` entry points at a file that actually
exists before running the pipeline.

---

## 5. Generate artefacts (Option B pipeline)

```powershell
python -m src.run_option_b_pipeline
```

This is the **authoritative** runner. It performs ingest → preprocess → feature engineering
→ train (Dummy / LogisticRegression / XGBoost) → evaluate → explainability, and writes:

- `outputs/option_b/models/*.joblib`
- `outputs/option_b/data/option_b_feature_columns.json`, `option_b_modelling_table.csv`,
  `option_b_prediction_template.csv`
- `outputs/option_b/results/*.csv`
- `outputs/option_b/explainability/*.csv`
- `outputs/option_b/figures/*.png`
- `outputs/option_b/logs/pipeline_run.log`

Confirm success by checking the log tail:

```powershell
Get-Content outputs\option_b\logs\pipeline_run.log -Tail 30
```

> The legacy step pipeline (`python -m src.run_all`, `src/step01…step10`) writes to
> `outputs/` (not `outputs/option_b/`). It is **not** what the current dashboard reads.

---

## 6. Launch the dashboard

```powershell
python -m streamlit run app.py
```

- Opens at <http://localhost:8501>.
- Stop with `Ctrl + C`.

Useful variants:

```powershell
python -m streamlit run app.py --server.port 8502      # different port
python -m streamlit run app.py --server.headless true  # no auto-open
```

---

## 7. Verify the installation

Run the automated tests:

```powershell
python -m pytest -v
```

Option B–specific suites:

```powershell
python -m pytest tests/test_option_b_acceptance.py -v
python -m pytest tests/test_prediction_interface.py -v
python -m pytest tests/test_saved_model_loading.py -v
```

Quick smoke test that the app imports and boots without errors:

```powershell
python -c "import streamlit, plotly, xgboost, shap, geopandas, sklearn, pandas, numpy, joblib; print('imports OK')"
```

---

## 8. Theme configuration

`.streamlit/config.toml` controls the visual theme:

```toml
[theme]
primaryColor="#147BB5"
backgroundColor="#F3F6FA"
secondaryBackgroundColor="#FFFFFF"
textColor="#172A40"
font="Inter"
```

Change colours here for the app-wide theme, and in `app/styles.py` (`COLORS`) for the CSS
components. See [07_Developer_Guide.md](07_Developer_Guide.md).

---

## 9. Project paths (from `config.py`)

| Constant | Points to | Purpose |
|----------|-----------|---------|
| `DATA_RAW` | `data/raw/` | Immutable source inputs |
| `DATA_PROCESSED` | `data/processed/` | Regenerable intermediate tables |
| `OUT_RES` / `OUT_MODELS` / `OUT_FIGS` | `outputs/…` | Legacy pipeline outputs |
| (`OPT_B_DIR` in `src/`) | `outputs/option_b/` | Option B artefacts the app reads |

---

## 10. Uninstall / reset

```powershell
deactivate                       # leave the venv
Remove-Item -Recurse -Force .venv
```

To force a pipeline re-run, delete `outputs/option_b/` (or just the subfolders you want to
rebuild) and re-run `python -m src.run_option_b_pipeline`.
