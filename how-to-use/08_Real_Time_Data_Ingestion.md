# 08 · Real-Time Data & Automation

How to source, download, schedule and render fresh data for ZCPSC — and what
"real-time" honestly means for each input.

Companion script: [`scripts/fetch_hapi_data.py`](../scripts/fetch_hapi_data.py).

---

## 1. The honest picture

| Input | Changes over time? | Freshness available | Way to get it |
|-------|:------------------:|---------------------|----------------|
| Market prices | **Yes, every month** | monthly (published ~weekly) | **HDX HAPI (keyless)**; WFP Data Bridges (API key); FEWS NET / World Bank RTP |
| Rainfall | **Yes, every dekad/day** | ~2–7 days (preliminary) | **HDX HAPI climate/rainfall (keyless)**; CHIRPS v3 preliminary; IMERG |
| Population | No (annual) | yearly vintage | UNFPA census / WorldPop |
| Poverty (MPI) | No (survey waves) | multi-year | OPHI/World Bank via HAPI |
| District boundaries | Rarely | static | geoBoundaries API |

**So:** you can automate true "rolling" refresh for **prices + rainfall**; for
**population, poverty and boundaries** the job is an occasional/annual refresh.
There is **no single API that returns everything** — the script assembles four.

> Note on the model: even with live data, a *new-month* prediction needs the
> engineered history (SPI lags, trailing rainfall windows, reporting-gap months).
> So the workflow is always **fetch → rebuild features → predict**, never a single
> live point.

---

## 2. Sources, endpoints and formats

### 2a. HDX HAPI (recommended — keyless, returns CSV or JSON)

Base URL: `https://hapi.humdata.org/api/v2`. Every request needs an
`app_identifier` = `base64("app_name:email")` (query param or the
`X-HDX-HAPI-APP-IDENTIFIER` header).

| Dataset | Endpoint path | Filter | Returns |
|---------|---------------|--------|---------|
| Food prices | `/food-security-nutrition-poverty/food-prices-market-monitor` | `location_code=ZWE`, `start_date`, `end_date` | price rows |
| Poverty rate | `/food-security-nutrition-poverty/poverty-rate` | `location_code=ZWE` | MPI rows |
| Rainfall | `/climate/rainfall` | `location_code=ZWE`, `aggregation_period`, `version` | dekad/1-month/3-month |
| Baseline population | `/geography-infrastructure/baseline-population` | `location_code=ZWE` | population rows |

Common params: `app_identifier` (required), `location_code`, `output_format`
(`csv`|`json`), `limit` (max **10000**), `offset`, `start_date`, `end_date`,
`admin1_code`/`admin2_code`, etc.

Public docs: <https://docs.humdata.org/build/hdx-apis/hapi/api-reference.md> ·
Source: HDX/WFP · Licence: **CC BY-IGO**.

Quick manual test (PowerShell):

```powershell
$id = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes("zcpsc-dashboard:you@example.com"))
$u  = "https://hapi.humdata.org/api/v2/climate/rainfall?app_identifier=$id&location_code=ZWE&output_format=csv&limit=5"
(Invoke-WebRequest $u -UseBasicParsing).Content
```

### 2b. Other price providers (optional)

| Provider | Endpoint / entry | Auth | Cadence |
|----------|------------------|------|---------|
| WFP Data Bridges | `https://api.wfp.org/vam-data-bridges/5.0.0/MarketPrices/PriceMonthly` (also `PriceDaily`, `PriceWeekly`) | OAuth client id/secret | daily→monthly |
| WFP Data Bridges (Python) | `pip install DataBridgesKnots` → `client.get_prices("ZWE", ...)` | key/secret | — |
| World Bank Real Time Food Prices | HDX `global-real-time-food-prices` (CSV) | none | ~biweekly |
| FEWS NET Zimbabwe | HDX `fewsnet_staple_food_price_data_for_zimbabwe_monthly` (CSV/XLSX/JSON) | none | monthly |

### 2c. Rainfall (finer resolution)

| Source | Access | Latency | Notes |
|--------|--------|---------|-------|
| CHIRPS v3 preliminary | CHC repo / USGS-CHC EWX / Earth Engine `UCSB-CHC/CHIRPS/V3/DAILY_SAT` | ~2–7 days | the project's `data/raw/chirps_v3_monthly_global.nc` |
| ClimateSERV API | `https://climateserv.servirglobal.net/chirps/submitDataRequest/` | near-RT | point/bounding-box jobs |
| NASA IMERG / GPM | NASA GES DISC | hours–1 day | fastest |

The project already builds district-month rainfall from a CHIRPS monthly NetCDF
via `src/step03_ingest_rainfall.py` (variables: `precip`, `latitude`, `longitude`,
`time`). If you refresh CHIRPS, drop the new NetCDF where `config.CHIRPS_NC` points
and re-run that step.

### 2d. Boundaries (geoBoundaries API)

```powershell
$adm2 = Invoke-RestMethod "https://www.geoboundaries.org/api/current/gbOpen/ZWE/ADM2/"
Invoke-WebRequest $adm2.gjDownloadURL -OutFile "data\raw\geo\zwe_adm2_geoboundaries.geojson"
$adm1 = Invoke-RestMethod "https://www.geoboundaries.org/api/current/gbOpen/ZWE/ADM1/"
Invoke-WebRequest $adm1.gjDownloadURL -OutFile "data\raw\geo\zwe_adm1_geoboundaries.geojson"
```

The response also exposes `simplifiedGeometryGeoJSON`, `tjDownloadURL`, licence and
`admUnitCount` (ZWE ADM2 = 91 units) for validation.

---

## 3. Automated download (the script)

`scripts/fetch_hapi_data.py` downloads all four HAPI datasets, paginates (10k/page),
writes UTF-8 CSVs into a timestamped staging folder, records a manifest
(row counts, params, sha256, columns) and can install over `data/raw/` with a backup.

```powershell
# preview the targets
python scripts\fetch_hapi_data.py --dry-run

# download the four datasets (staged, nothing overwritten)
python scripts\fetch_hapi_data.py --start-date 2017-01-01 --end-date 2026-05-31

# fetch only some datasets
python scripts\fetch_hapi_data.py --datasets food_price rainfall

# then install into data/raw (originals backed up as *.bak_<timestamp>)
python scripts\fetch_hapi_data.py --install
```

Output layout:

```
data/raw/hapi_live/<UTC-stamp>/
  hdx_hapi_food_price_zwe.csv
  hdx_hapi_poverty_rate_zwe.csv
  hdx_hapi_rainfall_zwe.csv
  hdx_hapi_population_zwe.csv
  fetch_manifest.json
```

Set a real identity for polite/identifiable API use:

```powershell
$env:HAPI_APP_IDENTIFIER = [Convert]::ToBase64String(
  [Text.Encoding]::UTF8.GetBytes("ZCPSC-dashboard:your.name@institution.ac.zw"))
```

### Schema note

The live HAPI CSV is **drop-in compatible** with the pipeline: the loaders in
`src/utils.py` and `run_option_b_pipeline.py` use only
`reference_period_start/end`, `admin1_name`, `admin2_name`, `commodity_category`,
`commodity_name`, `currency_code`, `price`, `unit`, etc. Live output adds a
`location_name` column and may omit `has_hrp`/`in_gho` — neither is read by the code.
Poverty live rows also use ISO datetimes (`2019-01-01T00:00:00`), which
`pd.to_datetime` parses fine.

---

## 4. Scheduling (unattended refresh)

### Windows Task Scheduler

```powershell
$action  = New-ScheduledTaskAction -Execute "python" `
  -Argument "scripts\fetch_hapi_data.py --install" `
  -WorkingDirectory "C:\Users\brigh\Documents\another"
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At 6am
Register-ScheduledTask -TaskName "ZCPSC-fetch-HAPI" -Action $action -Trigger $trigger
```

Run the whole rebuild (see §5) from a `.ps1` wrapper and schedule that instead:

```powershell
# scripts\refresh_all.ps1
python scripts\fetch_hapi_data.py --install
python -m src.step02_preprocess
python -m src.step03_ingest_rainfall
python -m src.run_option_b_pipeline
```

### Linux / macOS cron

```cron
0 6 * * 1  cd /path/to/another && python scripts/fetch_hapi_data.py --install && python -m src.step02_preprocess && python -m src.run_option_b_pipeline
```

### GitHub Actions (scheduled)

```yaml
on:
  schedule: [{ cron: "0 6 * * 1" }]
  workflow_dispatch:
jobs:
  refresh:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install -r requirements.txt
      - run: python scripts/fetch_hapi_data.py --start-date 2017-01-01
      - run: python -m src.run_option_b_pipeline
```

---

## 5. Rendering: getting fresh data into the dashboard

The dashboard reads **artefacts** in `outputs/option_b/`. Fresh raw data only shows
up after a rebuild. The chain:

```
fetch (data/raw)  →  preprocess (data/processed)  →  option_b pipeline (outputs/option_b)  →  dashboard
```

```powershell
python scripts\fetch_hapi_data.py --install   # 1. new raw CSVs
python -m src.step02_preprocess               # 2. population + district price/basket tables
python -m src.step03_ingest_rainfall          #    district-month rainfall (from CHIRPS NetCDF)
python -m src.run_option_b_pipeline           # 3. rebuild models/data/results/explainability
```

`run_option_b_pipeline` reads the raw `food_price` directly and the processed
`d_rainfall_chirps_district_month.csv` + `d_population_district.csv`, so steps 2–3
must run before step 3 whenever those inputs change.

### Making Streamlit show the new artefacts

Streamlit caches artifacts with `st.cache_data`/`st.cache_resource`, so a running
app won't see rebuilt files until the cache is cleared or the process restarts.

**Option A — restart the app** (simplest, fully reliable):

```powershell
# stop (Ctrl+C) and relaunch, or:
python -m streamlit run app.py
```

**Option B — add an in-app refresh button** to any page (e.g. `pages/1_Overview.py`):

```python
import streamlit as st
if st.sidebar.button("🔄 Refresh data"):
    st.cache_data.clear()
    st.cache_resource.clear()
    st.rerun()
```

**Option C — show an "as-of" banner** so users know the data vintage. Read the
manifest the fetch script wrote:

```python
import json, pathlib
m = sorted(pathlib.Path("data/raw/hapi_live").glob("*/fetch_manifest.json"))
if m:
    info = json.loads(m[-1].read_text())
    st.caption(f"Data as of {info['generated_utc']} · source: HDX HAPI")
```

---

## 6. Quality guardrails for automation

Automated pulls should **fail loudly and keep the last good snapshot**, never
publish silently. The script already records row counts and `sha256`. Add checks:

```python
assert n_rows > 0, "empty download"
assert df["reference_period_start"].max() >= expected_recent_month
assert set(["reference_period_start", "admin2_name"]).issubset(df.columns)
assert df["price"].notna().any()
```

Because `--install` backs up existing files as `*.bak_<stamp>`, you can roll back a
bad refresh by copying the backup back over the canonical file.

---

## 7. Licensing, etiquette and limits

- HAPI is **keyless** but requires a valid `app_identifier`; use a real email so the
  provider can contact you. Do not hammer the API — HAPI caps pages at **10 000** rows.
- Data licences: HDX/WFP **CC BY-IGO**; geoBoundaries **CC BY 3.0/4.0 IGO**. Keep
  attribution in outputs (the dashboard footer already cites WFP/CHIRPS/UNFPA).
- WFP Data Bridges requires an OAuth2 client id/secret — store in env vars, never in git.
- CHIRPS v3 preliminary is updated on the 2nd, 7th, 12th, 17th, 22nd and 27th of each
  month; final is monthly (third week).

---

## 8. Quick reference

| Goal | Command |
|------|---------|
| Preview endpoints | `python scripts/fetch_hapi_data.py --dry-run` |
| Fetch all (staged) | `python scripts/fetch_hapi_data.py` |
| Fetch + install to data/raw | `python scripts/fetch_hapi_data.py --install` |
| Rebuild everything | `python -m src.step02_preprocess; python -m src.step03_ingest_rainfall; python -m src.run_option_b_pipeline` |
| Relaunch dashboard | `python -m streamlit run app.py` |
| Verify artefacts | `Get-Content outputs\option_b\logs\pipeline_run.log -Tail 30` |
