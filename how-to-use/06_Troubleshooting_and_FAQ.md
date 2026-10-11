# 06 · Troubleshooting & FAQ

Quick fixes for the most common issues. If something is not listed, check the pipeline log
at `outputs/option_b/logs/pipeline_run.log` and the reports in `reports/`.

---

## 1. The app won't start

| Symptom | Cause | Fix |
|---------|-------|-----|
| `ModuleNotFoundError: No module named 'streamlit'` | venv not active / deps not installed | Activate the venv and `pip install -r requirements.txt` |
| `streamlit : The term 'streamlit' is not recognized` | used bare `streamlit` | use `python -m streamlit run app.py` |
| `OSError: [WinError 10048] ... port 8501` | port already in use | `python -m streamlit run app.py --server.port 8502` |
| Browser never opens | headless/sandbox | open <http://localhost:8501> manually |
| `ImportError` for `app.styles` | wrong working directory | run from the repository root (the folder with `app.py`) |

---

## 2. "Artifacts not found" / pages look empty

The dashboard reads pre-computed files in `outputs/option_b/`. If a page reports missing
artifacts or shows placeholder/sample values:

1. Confirm the folder exists:
   ```powershell
   Test-Path outputs\option_b\models\xgboost_pipeline.joblib
   Test-Path outputs\option_b\data\option_b_modelling_table.csv
   ```
2. If missing, run the pipeline:
   ```powershell
   python -m src.run_option_b_pipeline
   ```
3. Check the log tail:
   ```powershell
   Get-Content outputs\option_b\logs\pipeline_run.log -Tail 40
   ```

---

## 3. The map used to ask for a Mapbox access token

**Symptom:** the map asked for / broke without a `MAPBOX_API_KEY`, or showed
*"Set your Mapbox access token"*.

**Cause:** older code used `plotly.express.scatter_mapbox` with
`mapbox_style="carto-positron"`, which requires a Mapbox token.

**Fix (already applied):** the map traces were migrated to the tokenless
`plotly.express.scatter_map` API with `map_style="carto-positron"`, in
`pages/1_Overview.py` and `pages/4_Explore_Data.py`.

If you see this again (e.g. after a merge), search for and replace:

```
px.scatter_mapbox   →  px.scatter_map
mapbox_style=...    →  map_style=...
```

```powershell
# find any leftover usages
Select-String -Path app\*.py,pages\*.py -Pattern "scatter_mapbox|mapbox_style"
```

No token or key is required for the current maps.

---

## 4. SHAP errors

| Symptom | Cause | Fix |
|---------|-------|-----|
| Feature contributions appear as generic/placeholder values | explainer unavailable (so engine returned `explanation=None` and the UI fell back) | ensure `shap` imports and `xgboost_pipeline.joblib` loads |
| `ImportError: shap` | not installed | `pip install shap` |
| Windows DLL / `xgboost` load error (`VCRUNTIME140.dll`) | missing MS VC++ redistributable | install **Microsoft Visual C++ Redistributable (x64)** |

The engine degrades gracefully: if the explainer cannot be built, predictions still run, just
without live SHAP detail.

---

## 5. Geospatial / CSV upload issues

| Symptom | Fix |
|---------|-----|
| `ImportError: geopandas` / `fiona` / GDAL on Windows | `pip install geopandas`; if it fails, use conda-forge or the GDAL/Fiona wheels linked in the geopandas install docs |
| Map shows *"No geographic coordinate matches found"* | district names in your filter don't match the boundary file; clear filters |
| Uploaded CSV → all rows invalid | check the four mandatory columns and their spelling (see §6) |
| `InvalidDate` / rows flagged `INVALID_DATE_FORMAT` | use `YYYY-MM` (e.g. `2024-09`) |

---

## 6. Current integration status

Being transparent about the current state of the code so expectations are correct:

- **Pages 1 and 4** (Overview, Explore Data) read real artefacts and render live maps/tables
  from `outputs/option_b/` and `data/processed/`.
- **Page 5** (Model Explanations) reads real SHAP artefacts when present and otherwise shows
  illustrative values.
- **Pages 2 and 3** present the prediction workflow. The prediction engine
  (`src/prediction_engine.OptionBPredictor`) exposes a working API
  (`predict_single`, `validate_csv`, `predict_batch`, `generate_csv_template`), but the
  page calls currently use **different argument names / method names** than the engine
  defines (e.g. the page calls `predict_single(prediction_month=…, overrides=…)` and
  `validate_batch_dataframe(...)`). Because those calls are wrapped in `try/except`, the UI
  falls back to **sample values** instead of failing. To enable live scoring, align the calls
  as shown in [07_Developer_Guide.md §6](07_Developer_Guide.md#6-wiring-the-prediction-engine).
- **Pages 6 and 7** (Methodology, Limitations) are static explanatory content.

This does **not** affect the validity of the trained models or the artefacts — it is a UI
wiring gap, documented here for anyone picking the project up.

---

## 7. FAQ

**Q: What exactly does a "probability" mean?**
A: The model's estimated chance that the district–commodity's relative price stress (SPI)
will exceed the threshold in month T+1. It is not a certainty.

**Q: Why is accuracy high but stress detection weak?**
A: Stress is rare. A model that always says "normal" has high accuracy but detects nothing.
Read balanced accuracy, stress-class F1, ROC-AUC and PR-AUC instead (Page 5 /
[05_Model_and_Methodology.md](05_Model_and_Methodology.md)).

**Q: Does a red district mean a food emergency?**
A: No. It means a higher *modelled probability of relative price stress*. Price stress is not
household food insecurity and is not an IPC phase.

**Q: Which model should I trust?**
A: XGBoost is the champion by stress-class F1/PR-AUC, but always compare with the Logistic
Regression benchmark and the caveats on Page 7.

**Q: Where do the numbers on the map come from?**
A: Page 1 uses `xgb_proba` from `outputs/option_b/results/option_b_predictions.csv`,
aggregated to the latest prediction month per district.

**Q: Can I use my own district/commodity?**
A: Only districts and commodities present in the approved lists (from the modelling table)
are supported; others are rejected as `UNSUPPORTED_DISTRICT` / `UNSUPPORTED_COMMODITY`.

**Q: Do I need internet / an API key?**
A: No API key. An internet connection is only needed if your basemap tiles don't cache.

**Q: How do I change colours or branding?**
A: `.streamlit/config.toml` (theme) and `app/styles.py` (`COLORS`, CSS). See
[07_Developer_Guide.md](07_Developer_Guide.md).

---

## 8. Useful diagnostics

```powershell
# Python & package versions
python --version
python -m streamlit version
python -c "import pandas, numpy, sklearn, xgboost, shap, plotly, geopandas; print('ok')"

# Artefact presence
Get-ChildItem -Recurse outputs\option_b | Select-Object FullName

# Run the tests
python -m pytest -v
```

`reports/files_requiring_manual_review.md` and `reports/option_b_*_report.md` contain
deeper technical context.
