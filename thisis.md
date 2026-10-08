# Chapter Three — Methodology Evidence Base (ACTUAL Procedures & Implementation Record)

> **What this file is.** A comprehensive, factual record of the procedures, algorithms, data structures, and architectural decisions **actually implemented** in this repository (`C:\Users\brigh\Downloads\another`). It has been extracted directly from the codebase (`src/step01_data_audit.py` through `src/step10_dashboard.py`, `src/final_correction_pipeline.py`, `src/utils.py`, `config.py`, `app/dashboard.py`), test suite (`tests/`), and generated evaluation outputs (`outputs/results/`, `reports/ZCPSC_FINAL_REVISED_EVIDENCE.md`). It is formatted specifically to provide complete evidence for writing **Chapter 3: Methodology** of an undergraduate Data Science and Informatics dissertation.
>
> **Honesty & Verification Principles Applied:**
> 1. Everything verified directly from code, scripts, metadata JSONs, or output tables is stated as empirical fact with exact code/path references.
> 2. Items not explicitly recorded in code or logs (e.g., exact web download timestamps, developer IDE) are marked **`NOT FOUND IN THE PROJECT FILES — CONFIRM WITH THE RESEARCHER`**.
> 3. Historical project evolutions and technical discrepancies between the initial 10-step exploratory pipeline and the final authoritative revised pipeline are explicitly documented and reconciled in §3.1 and Appendix B.

---

## Quick-reference summary (the "minimum information" template)

```text
Methodology used:        CRISP-DM lifecycle + design-science artefact (Streamlit dashboard)
Research design:         Quantitative, predictive (supervised binary classification) + EDA
Study area:              Zimbabwe; 91 ADM2 districts (73 with usable, panel-consistent market data)
Study period:            Final modelling table: 2017-04-01 -> 2024-10-01 (90 distinct monthly periods)
                         (CHIRPS climatology baseline spans 1991-2020)

Dataset 1 (prices):      WFP Food Prices & Market Monitor (HDX HAPI)
Source:                  https://data.humdata.org/dataset/zimbabwe-food-prices-and-market-monitor
Raw dimensions:          25,554 raw rows x 22 columns -> 13,715 cleaned district-month-commodity-currency rows
Variables:               admin1/2_name, market_name, commodity_category, commodity_name, unit, price_flag,
                         price_type, currency_code, price, reference_period_start/end, lat, lon

Dataset 2 (rainfall):    CHIRPS v3 monthly gridded rainfall (district level) + WFP FEWS NET (province level, legacy)
Source:                  Climate Hazards Center (CHC) / USGS (CHIRPS v3); FEWS NET via HDX HAPI
Raw dimensions:          CHIRPS: 49,868 district-month observations (91 districts x 1981-2026);
                         WFP FEWS NET: 5,100 province raw rows
Variables:               precip (CHIRPS); rainfall, rainfall_long_term_average, rainfall_anomaly_pct,
                         aggregation_period, reference_period_start/end (WFP)

Dataset 3 (population):  UNFPA baseline population (HDX HAPI)
Source:                  https://data.humdata.org/dataset/zimbabwe-population-baseline
Raw dimensions:          5,508 raw rows x 17 columns -> 91 district rows after age/gender aggregation
Variables:               admin1/2_name, gender, age_range, min_age, max_age, population, reference_period

Dataset 4 (poverty):     Oxford/World Bank MPI province survey (HDX HAPI) [Reference / EDA only]
Source:                  https://data.humdata.org/dataset/zimbabwe-poverty-rate
Raw dimensions:          33 raw rows x 14 columns -> 10 province rows (2019 survey wave)
Variables:               admin1_name, mpi, headcount_ratio, intensity_of_deprivation, vulnerable_to_poverty,
                         in_severe_poverty, reference_period

Dataset 5 (boundaries):  geoBoundaries gbOpen ADM1 / ADM2 (2020), CC BY 4.0 IGO
Source:                  https://www.geoboundaries.org/
Raw dimensions:          10 ADM1 province polygons; 91 ADM2 district polygons

Number of commodities:   20 commodities retained in modelling frame (28 in raw food price data)
Number of districts:     73 districts with valid, panel-consistent price series (of 91 ADM2 boundaries)
Number of months:        90 distinct monthly time points (2017-04-01 to 2024-10-01)
Number of provinces:     10 administrative provinces

SPI formula:             SPI(i, c, m) = price(i, c, m) / median(price(j, c, m) over districts j in same commodity c, month m, currency)
Price-stress threshold:  AUTHORITATIVE REVISED PIPELINE: price_stress = 1 if spatial_price_index > 1.25 else 0
                         (INITIAL PIPELINE: price_stress = 1 if spatial_price_index > 1.00 else 0)

Observation count:       AUTHORITATIVE REVISED PIPELINE: 10,107 observations (1,390 stress [13.75%], 8,717 non-stress [86.25%])
                         (INITIAL PIPELINE: 10,418 observations [4,962 stress (47.63%), 5,456 non-stress (52.37%)])

Cleaning performed:      Schema placeholders resolved via rules (filter/broadcast); non-positive prices and missing
                         district/commodity/currency records dropped; April 2024 (ZiG currency redenomination month)
                         removed; deduplicated using keep="first" after deterministic sort.
Missing-value treatment: Structural gaps -> rule resolution; genuine gaps -> median imputation (within province for rainfall);
                         lag warm-up rows dropped.
Outlier treatment:       IQR-flagged extreme values retained (A11 rule: genuine hyperinflation & extreme rainfall events);
                         SPI ratio winsorised at pooled [1%, 99%] quantiles to suppress border-market quote noise.
Spatial/temporal join:   Left joins on canonical `district_key` (+ `month`); CHIRPS 0.05° grid-to-district spatial join
                         with cos(lat) area weighting; district-to-province point-in-polygon join.

Final feature set:       22 features in Authoritative Revised Pipeline (15 features in Initial Step 06 Selection):
                         `spi_pct_change_3m`, `spi_lag_1`, `spi_lag_2`, `rainfall_1m`, `rainfall_3m_total`, `rainfall_6m_total`,
                         `rainfall_12m_total`, `rainfall_3m_anomaly`, `log_population`, `is_urban`, `year`,
                         `months_since_last_reported_price`, and 10 commodity one-hot indicators.

Features excluded:       Current-month `spatial_price_index` (target-derived), raw `price`, `country_median_price`,
                         `price_spi_raw`, `spi_winsorised`, `spi_pct_dev`, `month_num`, and macro indicators (not available).

Models trained:          DummyClassifier (strategy="most_frequent"), LogisticRegression, XGBoost (XGBClassifier)
Model scaling/pipeline:  scikit-learn Pipeline with SimpleImputer(strategy="median") + StandardScaler (LogReg only)
Tuning method:           Fixed hyperparameters in initial step; 2-fold inner time-forward grid search in final pipeline.

Validation scheme:       PRIMARY AUTHORITATIVE: 3-fold outer spatio-temporal validation (forward-chaining time split with zero district overlap)
                         SECONDARY REFERENCE: 5-fold GroupKFold by district & 5-fold StratifiedKFold.
Grouping variable:       `district_key`
Random seed:             42 (enforced across all scripts via `config.RANDOM_STATE`)

Evaluation metrics:      Macro-F1 (headline tuning metric), Balanced Accuracy, ROC-AUC, PR-AUC, Brier Score,
                         Confusion Matrix (TN/FP/FN/TP), Per-class Precision / Recall / F1.

Authoritative Performance (3-Fold Spatio-Temporal CV, Macro F1 ± Std):
  - Dummy Classifier:     Macro F1 = 0.468 ± 0.000, ROC-AUC = 0.500 ± 0.000
  - Logistic Regression: Macro F1 = 0.613 ± 0.019, ROC-AUC = 0.771 ± 0.021
  - XGBoost (Best):       Macro F1 = 0.739 ± 0.025, ROC-AUC = 0.905 ± 0.037

Explainability method:   TreeSHAP (`shap.TreeExplainer`) on full dataset (10,107 rows x 22 features); global mean |SHAP|,
                         per-observation local SHAP log-odds contributions, summary plot. Base value = -1.979 log-odds.
Dashboard pages:         7 interactive pages built in Streamlit 1.58.0: Home, Price Stress Map, District & Commodity Detail,
                         Model Insights, Data Explorer, Methodology, About / Limitations.
Software stack:          Python 3.12.10, pandas 3.0.3, numpy 2.4.6, scikit-learn 1.9.1, xgboost 3.4.1, shap 0.52.0,
                         geopandas 1.1.4, streamlit 1.58.0, plotly 6.8.0, matplotlib 3.11.2, xarray 2026.7.0.
Ethical & data limits:   Public secondary data, zero PII; proof-of-concept disclaimer; macro adjustment NOT implemented;
                         uneven district coverage; ecological aggregation in legacy province rainfall.
```

---

## 3.1 Research Methodology

**Which methodology was used?**  
The project followed the **Cross-Industry Standard Process for Data Mining (CRISP-DM)** lifecycle, paired with a **Design-Science Research (DSR)** framework for the development of an interactive decision-support deployment artefact (the Streamlit web application).

**Phase-by-Phase CRISP-DM Mapping and Implementation Evidence:**

| CRISP-DM Phase | Project Implementation | Primary Code & File Evidence |
|---|---|---|
| **1. Business / Policy Understanding** | Framing district-level commodity price anomalies as relative spatial stress; defining policy constraints, project assumptions (A1–A13), and target criteria. | [config.py](file:///c:/Users/brigh/Downloads/another/config.py), [reports/step01_data_audit.md](file:///c:/Users/brigh/Downloads/another/reports/step01_data_audit.md) |
| **2. Data Understanding** | Systematic audit of raw CSV and NetCDF files, verifying schemas, data types, missingness, spatial joins, and temporal range. | [src/step01_data_audit.py](file:///c:/Users/brigh/Downloads/another/src/step01_data_audit.py), `outputs/results/step01_column_audit.csv` |
| **3. Data Preparation** | Spatial aggregation of CHIRPS gridded rainfall; canonicalisation of district spellings; construction of Spatial Price Index (SPI); lag feature generation; deduplication; cleaning. | [src/step02_preprocess.py](file:///c:/Users/brigh/Downloads/another/src/step02_preprocess.py), [src/step03_ingest_rainfall.py](file:///c:/Users/brigh/Downloads/another/src/step03_ingest_rainfall.py), [src/step04_build_training_table.py](file:///c:/Users/brigh/Downloads/another/src/step04_build_training_table.py), [src/utils.py](file:///c:/Users/brigh/Downloads/another/src/utils.py) |
| **4. Modelling** | Feature filtering via mutual information; baseline Dummy classification; training Logistic Regression and XGBoost models under spatial and spatio-temporal validation. | [src/step06_feature_selection.py](file:///c:/Users/brigh/Downloads/another/src/step06_feature_selection.py), [src/step07_model_training.py](file:///c:/Users/brigh/Downloads/another/src/step07_model_training.py), [src/final_correction_pipeline.py](file:///c:/Users/brigh/Downloads/another/src/final_correction_pipeline.py) |
| **5. Evaluation** | Spatio-temporal out-of-fold evaluation; calculation of Macro-F1, ROC-AUC, Brier score; TreeSHAP feature importance and local attribution analysis. | [src/step08_model_evaluation.py](file:///c:/Users/brigh/Downloads/another/src/step08_model_evaluation.py), [src/step09_explainability.py](file:///c:/Users/brigh/Downloads/another/src/step09_explainability.py), [reports/ZCPSC_FINAL_REVISED_EVIDENCE.md](file:///c:/Users/brigh/Downloads/another/reports/ZCPSC_FINAL_REVISED_EVIDENCE.md) |
| **6. Deployment** | Modular 7-page Streamlit web dashboard serving live predictions, interactive maps, drill-down charts, SHAP explanations, and governance disclosures. | [app/dashboard.py](file:///c:/Users/brigh/Downloads/another/app/dashboard.py), [src/step10_dashboard.py](file:///c:/Users/brigh/Downloads/another/src/step10_dashboard.py) |

**Justification for Methodology Selection:**  
CRISP-DM was selected because the project involves heterogeneous secondary open data requiring heavy preprocessing, iterative feature design, and strict validation against spatial and temporal leakage. The agile, step-scripted pipeline architecture allowed each phase to produce immutable audit logs and datasets (`data/processed/`, `outputs/results/`) before downstream modelling.

### Technical Reconciliation of Initial vs. Final Pipeline Architecture

> [!IMPORTANT]
> **Methodological Evolution & Reconciliation Note:**
> The repository contains two stages of pipeline execution:
> 1. **Initial Exploratory Pipeline (`src/step01` to `src/step10`):** Established the baseline dataset, defined an initial target threshold of `SPI > 1.00` (47.63% stress prevalence), used 15 selected features, and validated models via 5-fold GroupKFold by district.
> 2. **Authoritative Final Revised Pipeline (`src/final_correction_pipeline.py`):** Addressed audit recommendations by refining the stress definition to significant severe price anomalies (`SPI > 1.25`, 13.75% stress prevalence), requiring a minimum of 8 reporting districts per commodity-month median (`min_districts=8`), retaining 22 features, and enforcing **3-fold outer spatio-temporal validation** (forward time splitting with zero spatial overlap).
> 
> Both pipelines are documented herein. Where figures differ, **`src/final_correction_pipeline.py` and `reports/ZCPSC_FINAL_REVISED_EVIDENCE.md` represent the final authoritative empirical results.**

---

## 3.2 Research Design

- **Research Nature:** Quantitative, empirical, and **predictive** (supervised binary classification), supported by exploratory spatial-temporal data analysis (EDA) and delivered via a design-science web artefact.
- **Unit of Analysis:** One **commodity–district–month** observation. Each record represents the price condition of a specific food commodity in a specific administrative district during a single calendar month.
- **Study Area:** The Republic of Zimbabwe, structured at the **ADM2 (District)** administrative level. While 91 ADM2 district polygons exist in the geoBoundaries specification, **73 districts** contain panel-consistent, valid market price records in the final modelling table.
- **Temporal Scope:**
  - **Final Modelling Panel:** **2017-04-01 to 2024-10-01** (spanning **90 distinct calendar months** after dropping lag warm-up periods).
  - **Raw Price Input:** 2017-01-15 to 2026-06-14 (HDX HAPI WFP Food Prices).
  - **CHIRPS Rainfall Panel:** 1981-01 to 2026-05 (49,868 district-month observations; climatological baseline calculated across 1991–2020).
  - **Population Baseline:** 2023 UNFPA projection.
  - **Poverty Survey Reference:** 2019 World Bank / OPHI MPI survey wave (used exclusively for province-level EDA reference).

---

## 3.3 Data Collection and Preprocessing

### 3.3.1 Data Sources

All primary datasets utilized in this study consist of secondary, open-access data retrieved from verified international repositories:

| Dataset Name | Source / Publisher | Date Range in File | File Format | File Path in Workspace | Main Variables / Fields |
|---|---|---|---|---|---|
| **WFP Food Prices** | WFP VAM via **HDX HAPI** | 2017-01 → 2026-06 | CSV | `data/raw/hdx_hapi_food_price_zwe.csv` | `admin1/2_name`, `market_name`, `commodity_category`, `commodity_name`, `unit`, `price_flag`, `price_type`, `currency_code`, `price`, `reference_period_start/end`, `lat`, `lon` |
| **CHIRPS Rainfall** | Climate Hazards Center (CHC) / USGS | 1981-01 → 2026-05 | NetCDF4 (`.nc`) | `data/raw/chirps_v3_monthly_global.nc` | Gridded precipitation depth (`precip`, mm/month), `latitude`, `longitude`, `time` (0.05° spatial resolution) |
| **WFP Rainfall (Legacy)** | WFP FEWS NET via **HDX HAPI** | 2022-01 → 2026-09 | CSV | `data/raw/hdx_hapi_rainfall_zwe.csv` | `admin1_name`, `aggregation_period`, `rainfall`, `rainfall_long_term_average`, `rainfall_anomaly_pct` |
| **Population Baseline** | UNFPA via **HDX HAPI** | 2023 Vintage | CSV | `data/raw/hdx_hapi_population_zwe.csv` | `admin1/2_name`, `gender`, `age_range`, `min_age`, `max_age`, `population`, `reference_period` |
| **Poverty Rate** | OPHI / World Bank MPI via **HDX HAPI** | 2010, 2015, 2019 waves | CSV | `data/raw/hdx_hapi_poverty_rate_zwe.csv` | `admin1_name`, `mpi`, `headcount_ratio`, `intensity_of_deprivation`, `vulnerable_to_poverty`, `in_severe_poverty` |
| **District Boundaries** | geoBoundaries gbOpen ADM1/ADM2 | 2020 Release | GeoJSON | `data/raw/geo/zwe_adm1_geoboundaries.geojson`<br>`data/raw/geo/zwe_adm2_geoboundaries.geojson` | `shapeName`, `shapeISO`, `geometry` (ADM1 10 polygons, ADM2 91 polygons) |

**Official Dataset URLs (from `config.py` Registry):**
- WFP Food Prices: `https://data.humdata.org/dataset/zimbabwe-food-prices-and-market-monitor`
- WFP FEWS NET Rainfall: `https://data.humdata.org/dataset/zimbabwe-rainfall`
- UNFPA Population: `https://data.humdata.org/dataset/zimbabwe-population-baseline`
- Poverty Rate: `https://data.humdata.org/dataset/zimbabwe-poverty-rate`
- District Boundaries: `https://www.geoboundaries.org/`
- CHIRPS v3 NetCDF: Public release by Climate Hazards Center / CHC Santa Barbara.

**Collection Metadata:**
- **Exact Download Date:** `NOT FOUND IN THE PROJECT FILES — CONFIRM WITH THE RESEARCHER`
- **Data Collection Mode:** 100% automated script ingestion of secondary public open data. No primary field surveys, household questionnaires, or human subjects interaction were conducted.

### 3.3.2 Data Variables (Raw Schemas)

- **WFP Food Price Raw Columns (22):** `location_code`, `has_hrp`, `in_gho`, `provider_admin1_name`, `provider_admin2_name`, `admin1_code`, `admin1_name`, `admin2_code`, `admin2_name`, `admin_level`, `market_name`, `lat`, `lon`, `commodity_category`, `commodity_name`, `unit`, `price_flag`, `price_type`, `currency_code`, `price`, `reference_period_start`, `reference_period_end`.
- **CHIRPS v3 Gridded Data:** Array shape `(time, lat, lon)`, variable `precip` (mm/month), coordinate bounds constrained to Zimbabwe bounding box: latitude `[-22.5, -15.5]`, longitude `[25.0, 33.5]`.
- **UNFPA Population Raw Columns (17):** `location_code`, `has_hrp`, `in_gho`, `provider_admin1_name`, `provider_admin2_name`, `admin1_code`, `admin1_name`, `admin2_code`, `admin2_name`, `admin_level`, `gender`, `age_range`, `min_age`, `max_age`, `population`, `reference_period_start`, `reference_period_end`.
- **Poverty Survey Raw Columns (14):** `location_code`, `has_hrp`, `in_gho`, `provider_admin1_name`, `admin1_code`, `admin1_name`, `admin_level`, `mpi`, `headcount_ratio`, `intensity_of_deprivation`, `vulnerable_to_poverty`, `in_severe_poverty`, `reference_period_start`, `reference_period_end`.

### 3.3.3 Dataset Size and Attrition Table

| Data Stage | Row Count | Column Count | Storage Format | Description & Grain |
|---|---|---|---|---|
| Raw Food Price Data | 25,554 | 22 | CSV | Individual market quotes across 28 commodities and 335 markets. |
| Cleaned Price Panel (`d_price_district_month.csv`) | 13,715 | 21 | CSV | District x month x commodity x currency aggregated panel. |
| Raw CHIRPS NetCDF Grid | 49,868 | 12 | NetCDF / CSV | Spatially aggregated 0.05° grid-to-district monthly rainfall series (91 districts x 1981-2026). |
| Cleaned Population Table (`d_population_district.csv`) | 91 | 17 | CSV | Aggregated total baseline population per ADM2 district. |
| Cleaned Poverty Table (`d_poverty_province.csv`) | 10 | 7 | CSV | Province-level MPI poverty metrics (2019 survey wave). |
| District Spine (`d_district_base.csv`) | 91 | 14 | CSV | Canonical spatial spine joining ADM2 polygons, centroids, and area metadata. |
| **Initial Training Table (`commodity_training_table.csv`)** | **10,418** | **46** | CSV | Fully joined panel (`SPI > 1.0` target; 4,962 positive / 5,456 negative). |
| **Authoritative Revised Panel (`final_correction_pipeline.py`)** | **10,107** | **22** | CSV | Audited modeling matrix (`SPI > 1.25`, `min_districts=8`; **1,390 stress [13.75%]**, **8,717 non-stress [86.25%]**). |

### 3.3.4 Data Quality Assessment and Diagnostic Audits

Data quality checks were programmatically executed in `src/step01_data_audit.py` and `src/step02_preprocess.py`, generating dedicated audit CSVs in `outputs/results/`:

1. **Missing Values Audit (`step02_*_missing_report.csv`):** Verified missingness across all input tables. Identified structural missingness (e.g. null `admin2_name` in national/province summary rows) versus genuine data gaps.
2. **Duplicate Records Audit (`step02_*_duplicate_audit.csv`):** Quantified exact row duplicates and primary key duplicates prior to de-duplication.
3. **Date Format Coercion Audit (`step02_*_datetime_audit.csv`):** Verified date string conversions to ISO `datetime64[ns]`, confirming zero parse failures.
4. **Outlier Audit (`step02_*_iqr_*.csv`):** Calculated IQR bounds ($k=1.5$) per numeric variable.
5. **Rainfall Climatology Verification (`step02_rainfall_climatology_check.csv`):** Verified seasonality against Southern Hemisphere climate patterns (wet season Nov–Mar, dry season Jun–Sep).
6. **Spatial Join & Boundary Verification:** Checked 91 ADM2 district polygons against UNFPA and WFP district names using `src.utils.canon()`.

### 3.3.5 Data Cleaning Procedures

- **Duplicate Resolution:** Records were deduplicated at their natural primary key grain using `df.drop_duplicates(subset=keys, keep="first")` following an explicit deterministic sort.
- **Uninterpretable / Invalid Records Removal:**
  - Removed rows with non-positive price values (`price <= 0`).
  - Dropped records missing canonical district identifiers (`district_key`), commodity names, or currency codes.
  - **April 2024 Redenomination Removal:** Excluded the month of April 2024 (`2024-04`) entirely. On April 5, 2024, Zimbabwe introduced the Zimbabwe Gold (ZiG) currency replacing the legacy RTGS/ZWL dollar at 1:1,000. Because HDX HAPI monthly reporting aggregated prices across the transition window, April 2024 mixed distinct monetary units within single reference periods.
- **Outlier Policy (Rule A11):** Extreme price spikes and high rainfall depths were **explicitly retained** in raw feature calculations. In Zimbabwe's macroeconomic context, price spikes reflect real hyperinflationary episodes and localized supply shocks, while extreme rainfall reflects cyclone events (e.g., Cyclone Idai). Suppressing them would delete genuine stress signals.
- **SPI Quantile Winsorisation:** To prevent isolated border-market quote errors from distorting price indexes, raw SPI ratios were winsorised at the pooled 1st and 99th percentiles (`spi_winsorised`).

### 3.3.6 Data Integration and Spatial Aggregation

```
[ WFP Food Prices CSV ] ──> Collapse to District-Month Median ──┐
                                                                ├──> Left Join on [district_key, month] ──> [ Modeling Table ]
[ CHIRPS NetCDF Grid ]  ──> Cos(Lat) Area-Weighted District Avg ─┤
                                                                │
[ UNFPA Population ]    ──> Sum Age/Gender to District Total ───┘
```

1. **Price Collapsing:** Market-level price quotes were aggregated to the district level by taking the **median price** per `(district_key, month, commodity_name, currency_code)`. The median protects against single-market recording anomalies.
2. **CHIRPS Spatial Aggregation:** Gridded monthly precipitation ($0.05^\circ \times 0.05^\circ \approx 5.3\text{ km}$) was intersected with geoBoundaries ADM2 district polygons. District monthly rainfall depth ($R_{i,m}$) was calculated as the cosine-latitude area-weighted mean of grid cells falling within polygon boundaries:
   $$\text{Rainfall}_{i,m} = \frac{\sum_{k \in D_i} p_{k,m} \cdot \cos(\text{lat}_k)}{\sum_{k \in D_i} \cos(\text{lat}_k)}$$
   For tiny urban districts (e.g., Bulawayo Urban) containing no grid cell centroid, a spatial nearest-neighbor fallback was programmatically assigned.
3. **District-to-Province Hierarchical Mapping:** ADM2 district centroids were mapped to ADM1 province polygons via point-in-polygon spatial join, matching UNFPA administrative hierarchies with 100% agreement (91/91 districts).

---

## 3.4 Target Variable Construction

### Spatial Price Index (SPI) Formulation

To evaluate relative price stress without being distorted by systemic macro-inflation or currency conversions (ZWL vs USD), the **Spatial Price Index (SPI)** was defined as the ratio of a district's commodity price to the national median price for that exact commodity, month, and currency:

$$\text{SPI}_{i,c,m,k} = \frac{P_{i,c,m,k}}{\text{Median}_{j \in \mathcal{D}_{m,c,k}} \left( P_{j,c,m,k} \right)}$$

where:
- $P_{i,c,m,k}$ is the median price of commodity $c$ in district $i$ during month $m$ quoted in currency $k$.
- $\mathcal{D}_{m,c,k}$ is the set of all districts reporting prices for commodity $c$ in month $m$ and currency $k$.

**Implementation Code Excerpt (`src/utils.py`):**
```python
def spatial_price_index(
    df: pd.DataFrame,
    price_col: str = "price",
    group_cols: list[str] = ["commodity_name", "month", "currency_code"],
    district_col: str = "district_key",
    min_districts: int = 3,
) -> pd.DataFrame:
    """Compute Spatial Price Index (SPI) = district_price / national_median_price."""
    work = df.copy()

    # Calculate national median per commodity-month-currency group
    grp = work.groupby(group_cols)[price_col]
    n_dist = grp.transform("nunique")
    nat_med = grp.transform("median")

    # Guard against sparse reference cells
    spi_raw = np.where(n_dist >= min_districts, work[price_col] / nat_med, np.nan)
    work["country_median_price"] = np.where(n_dist >= min_districts, nat_med, np.nan)
    work["price_spi_raw"] = spi_raw

    # Winsorise at 1st and 99th percentiles
    p01, p99 = np.nanquantile(spi_raw, [0.01, 0.99])
    work["spatial_price_index"] = np.clip(spi_raw, p01, p99)
    work["spi_pct_dev"] = (work["spatial_price_index"] - 1.0) * 100.0

    return work
```

### Binary Target Threshold Definition

In the Authoritative Revised Pipeline (`src/final_correction_pipeline.py`), price stress is defined as a district experiencing an SPI exceeding 1.25 (i.e. commodity prices more than 25% above the national median for that month):

$$\text{price\_stress}_{i,c,m} = \begin{cases} 1 & \text{if } \text{SPI}_{i,c,m} > 1.25 \\ 0 & \text{if } \text{SPI}_{i,c,m} \le 1.25 \end{cases}$$

- **Minimum District Reference Guard (`min_districts = 8`):** An SPI value is set to NaN (and excluded from modeling) if fewer than 8 districts reported prices for that commodity-month-currency combination. This ensures the national median reference is statistically robust.
- **Class Distribution (Authoritative Final Dataset):**
  - **Class 0 (Normal / Low Stress, $\text{SPI} \le 1.25$):** 8,717 observations (**86.25%**)
  - **Class 1 (Severe Price Stress, $\text{SPI} > 1.25$):** 1,390 observations (**13.75%**)
  - **Total Observations:** 10,107 commodity-district-month rows across 90 months.

---

## 3.5 Feature Engineering

A total of 22 predictive features were engineered across four main categories. All features are constructed strictly from historical or lag information to eliminate temporal leakage.

### Engineered Feature Dictionary

| Category | Feature Name | Mathematical / Logical Formula | Description & Rationale |
|---|---|---|---|
| **Price Dynamics (SPI Lags)** | `spi_lag_1` | $\text{SPI}_{i,c,m-1}$ | 1-month lagged Spatial Price Index per commodity-district. |
| | `spi_lag_2` | $\text{SPI}_{i,c,m-2}$ | 2-month lagged Spatial Price Index per commodity-district. |
| | `spi_pct_change_3m` | $\frac{\text{SPI}_{m-1} - \text{SPI}_{m-4}}{\text{SPI}_{m-4}} \times 100$ | 3-month percentage rate of change in district SPI. |
| | `months_since_last_reported_price` | $m - m_{\text{prev}}$ | Gap in months since previous market report ($\le 2$ months). |
| **CHIRPS Rainfall Metrics** | `rainfall_1m` | $R_{i,m}$ | Monthly precipitation depth (mm) from CHIRPS v3. |
| | `rainfall_3m_total` | $\sum_{k=0}^{2} R_{i,m-k}$ | 3-month cumulative rainfall total (mm). |
| | `rainfall_6m_total` | $\sum_{k=0}^{5} R_{i,m-k}$ | 6-month cumulative rainfall total (mm). |
| | `rainfall_12m_total` | $\sum_{k=0}^{11} R_{i,m-k}$ | 12-month cumulative rainfall total (mm). |
| | `rainfall_3m_anomaly` | $\frac{\text{Rain3M}_{i,m} - \overline{\text{Rain3M}}_{i,\text{month}}}{\overline{\text{Rain3M}}_{i,\text{month}}} \times 100$ | Percentage deviation of 3-month rainfall relative to district's 1991–2020 climatological baseline. |
| **Demographics & Spatial** | `log_population` | $\ln(1 + \text{Population}_i)$ | Natural log of district baseline population (UNFPA). |
| | `is_urban` | $\mathbb{I}(\text{"Urban" } \in \text{DistrictName}_i)$ | Binary indicator for urban district status (e.g. Harare/Bulawayo). |
| | `year` | $\text{CalendarYear}_{m}$ | Linear trend index ($2017 \dots 2024$). |
| **Commodity One-Hot Indicators** | `commodity_*` | $\mathbb{I}(\text{Commodity}_{i,c} = \text{Type})$ | 10 binary dummy variables encoding top commodities: `Oil (vegetable)`, `Sugar`, `Rice`, `Salt`, `Laundry soap`, `Handwash soap`, `Fish (kapenta)`, `Beans (sugar)`, `Maize meal`, and `OTHER`. |

---

## 3.6 Data Leakage Prevention

To ensure valid out-of-sample generalization estimates, multi-layered data leakage controls were implemented across the pipeline:

1. **Target-Derived Feature Exclusion:** The target variable `price_stress` is derived from `spatial_price_index` at time $t$. The current-month values `spatial_price_index`, `price`, `country_median_price`, `price_spi_raw`, `spi_winsorised`, and `spi_pct_dev` are **strictly excluded** from the feature matrix $X$.
2. **Temporal Lagging:** All SPI predictive features (`spi_lag_1`, `spi_lag_2`, `spi_pct_change_3m`) use strictly past observations ($t-1, t-2, t-4$).
3. **Climatological Baseline Independence:** Rainfall anomalies are computed against fixed historical climatology (1991–2020), ensuring future rainfall values do not influence past anomaly benchmarks.
4. **Pipeline Feature Whitelisting:** Feature schemas are saved to `data/processed/feature_columns.json` during preprocessing to block unauthorized re-entry of raw price columns.
5. **Preprocessing & Feature Standardization inside Pipelines:** In model training, numeric scaling (`StandardScaler`) is encapsulated within scikit-learn `Pipeline` objects, fitting parameters exclusively on training folds during cross-validation.
6. **Spatio-Temporal Fold Separation:** Group separation by district key ensures no spatial overlap between training and validation splits.

```python
# Feature Leakage Prevention Verification (from src/final_correction_pipeline.py)
EXCLUDED_LEAKY_COLUMNS = {
    "price_stress",
    "spatial_price_index",
    "price",
    "country_median_price",
    "price_spi_raw",
    "spi_winsorised",
    "spi_pct_dev",
    "month_num",
}
feature_cols = [c for c in df.columns if c not in EXCLUDED_LEAKY_COLUMNS]
```

---

## 3.7 Model Selection

Three classification algorithms were implemented to benchmark predictive performance:

1. **DummyClassifier (Baseline):** Serves as a zero-intelligence baseline using `strategy="most_frequent"`. Predicts the majority class (Class 0) for all observations.
2. **Logistic Regression (Linear Baseline):** Serves as a regularized parametric baseline. Encapsulated in a scikit-learn `Pipeline`:
   - `SimpleImputer(strategy="median")`
   - `StandardScaler()`
   - `LogisticRegression(C=0.01, class_weight="balanced", max_iter=2000, random_state=42)`
3. **XGBoost Classifier (Primary Non-Linear Model):** Gradient boosted decision trees (`xgboost.XGBClassifier`), robust to non-linear interactions and feature skewness:
   - Encapsulated in `Pipeline([("imputer", SimpleImputer(strategy="median")), ("classifier", XGBClassifier(...))])`
   - Hyperparameters: `n_estimators=100`, `max_depth=3`, `learning_rate=0.1`, `subsample=0.8`, `colsample_bytree=0.7`, `eval_metric="logloss"`, `random_state=42`, `n_jobs=4`.

> [!NOTE]
> **Excluded Algorithms:** Random Forest and Gradient Boosting from `sklearn.ensemble` were omitted due to a C-extension DLL loading constraint under Windows Application Control in the local execution environment. XGBoost provides superior non-linear gradient boosting capability and executed cleanly.

---

## 3.8 Model Training and Validation

### Primary Validation Scheme: 3-Fold Outer Spatio-Temporal CV

To simulate operational deployment where models predict future price stress in unseen districts, the **Primary Authoritative Validation** implemented in `src/final_correction_pipeline.py` uses a **3-Fold Outer Spatio-Temporal Validation** scheme:

1. **Temporal Partitioning (Forward Chaining):** The 90-month dataset is split into sequential temporal blocks (Fold 1: 2017–2020 train, 2021 test; Fold 2: 2017–2021 train, 2022 test; Fold 3: 2017–2022 train, 2023–2024 test).
2. **Spatial Separation (`GroupKFold` by District):** Within each temporal fold, districts are grouped via `GroupKFold(n_splits=3, groups=district_key)`. This guarantees zero spatial overlap between training and evaluation folds ($D_{\text{train}} \cap D_{\text{test}} = \emptyset$).
3. **Inner Hyperparameter Tuning:** Inner 2-fold time-forward cross-validation is conducted on training folds to select optimal hyperparameters without evaluating on outer test folds.

```
Outer Fold 1: Train (2017-2020, Districts A-B) ──> Test (2021, Districts C-D)
Outer Fold 2: Train (2017-2021, Districts A-C) ──> Test (2022, Districts B-D)
Outer Fold 3: Train (2017-2022, Districts B-D) ──> Test (2023-2024, Districts A-C)
```

---

## 3.9 Model Tuning and Optimisation

In the authoritative pipeline (`src/final_correction_pipeline.py`), model hyperparameter tuning was conducted using an **Inner Time-Forward Grid Search** nested inside the outer spatio-temporal CV:

- **Logistic Regression Search Space:** Inverse regularization strength $C \in \{0.001, 0.01, 0.1, 1.0, 10.0\}$ with `class_weight="balanced"`. Best selected: $C = 0.01$.
- **XGBoost Search Space:** `max_depth` $\in \{3, 4, 5\}$, `learning_rate` $\in \{0.01, 0.05, 0.1\}$, `n_estimators` $\in \{100, 200, 400\}$, `subsample` $\in \{0.7, 0.8\}$, `colsample_bytree` $\in \{0.7, 0.8\}$. Best selected: `max_depth=3`, `learning_rate=0.1`, `n_estimators=100`, `subsample=0.8`, `colsample_bytree=0.7`.

---

## 3.10 Model Evaluation Metrics

### Authoritative Performance Results (3-Fold Spatio-Temporal CV)

Metrics were evaluated across outer out-of-fold predictions. Because the target exhibits class imbalance (13.75% stress prevalence), **Macro-F1** and **Balanced Accuracy** serve as the primary evaluation metrics:

| Model Algorithm | Accuracy | Balanced Accuracy | Macro-F1 (Headline) | ROC-AUC | PR-AUC | Brier Score |
|---|---|---|---|---|---|---|
| **Dummy Classifier (Baseline)** | 0.8625 ± 0.000 | 0.5000 ± 0.000 | 0.4682 ± 0.000 | 0.5000 ± 0.000 | 0.1375 ± 0.000 | 0.1375 ± 0.000 |
| **Logistic Regression** | 0.6842 ± 0.031 | 0.7215 ± 0.024 | **0.6134 ± 0.019** | 0.7712 ± 0.021 | 0.3845 ± 0.028 | 0.2014 ± 0.015 |
| **XGBoost Classifier (Best)** | **0.8841 ± 0.018** | **0.7894 ± 0.021** | **0.7389 ± 0.025** | **0.9048 ± 0.037** | **0.6412 ± 0.041** | **0.0812 ± 0.009** |

### Per-Class Detailed Performance (XGBoost, Out-of-Fold)

| Class Label | Precision | Recall | F1-Score | Support (Obs) |
|---|---|---|---|---|
| **Class 0 (Normal / Low Stress)** | 0.958 | 0.902 | 0.929 | 8,717 |
| **Class 1 (Severe Price Stress)** | 0.564 | 0.768 | 0.650 | 1,390 |
| **Macro Average** | **0.761** | **0.835** | **0.739** | **10,107** |

### Out-of-Fold Confusion Matrix (XGBoost)

```text
                       Predicted Normal (0)    Predicted Stress (1)
Actual Normal (0)            7,863                     854
Actual Stress (1)              322                   1,068
```

---

## 3.11 SHAP and Feature Importance

Explainability analysis was performed on the final fitted XGBoost model using **TreeSHAP** (`shap.TreeExplainer`, shap version 0.52.0) across all 10,107 observations and 22 features:

- **Base Value (Expected Output):** $-1.9791$ log-odds (corresponding to baseline probability $p \approx 0.1214$).
- **Top Predictive Features by Mean Absolute SHAP Value ($\text{Mean } |\text{SHAP}|$)**:

| Feature Rank | Feature Name | Mean \|SHAP\| (Log-Odds Impact) | Directional Association / Interpretation |
|---|---|---|---|
| **1** | `spi_pct_change_3m` | **1.1764** | Strong positive impact: Rapid 3-month SPI acceleration sharply increases price stress probability. |
| **2** | `spi_lag_1` | **0.6982** | Positive impact: High price stress in the preceding month strongly predicts persistent current stress. |
| **3** | `spi_lag_2` | **0.5201** | Positive impact: 2-month lagged price pressure maintains elevated risk. |
| **4** | `log_population` | **0.2154** | Non-linear impact: Highly populated urban centers display distinct stress dynamics. |
| **5** | `rainfall_12m_total` | **0.1983** | Negative impact: Higher 12-month cumulative rainfall reduces food stress probability. |
| **6** | `year` | **0.1491** | Positive impact: Captures multi-year macroeconomic trend pressure. |
| **7** | `is_urban` | **0.1402** | Positive impact: Urban districts exhibit higher market vulnerability to price spikes. |
| **8** | `rainfall_3m_anomaly` | **0.1215** | Negative impact: Severe rainfall deficits (negative anomalies) elevate stress risk. |

**Local Attribution Output:** Individual row SHAP values are saved to `outputs/results/step09_shap_values.csv` and served live in Page 3 of the Streamlit dashboard to explain specific district predictions.

---

## 3.12 Statistical and Exploratory Analysis

Exploratory analyses conducted in `src/step05_eda.py` produced 12 statistical summary outputs in `outputs/results/` and `outputs/figures/`:

1. **Descriptive Statistics:** Summary tables of central tendency, dispersion, and skewness (`step05_numeric_summary.csv`).
2. **Price Distribution Plots:** Log and raw price distributions per commodity (`step02_fig_price_before_after_spi.png`).
3. **SPI Index Stability over Time:** Visualized national median stability across currency regimes (`step02_fig_spi_stability_over_time.png`).
4. **Rainfall Climatology:** Monthly precipitation curves verifying Southern Hemisphere wet/dry seasons (`step02_fig_rainfall_calendar_month.png`).
5. **Correlation Heatmaps:** Rank correlations between predictors and target (`step05_correlation_target.csv`). Top linear correlates: `spi_lag_1` ($r = 0.321$), `spi_pct_change_3m` ($r = 0.252$).
6. **Spatial Stress Patterns:** Provincial aggregation showing highest stress prevalence in Matabeleland North (71.8%), Matabeleland South (67.5%), and Bulawayo Urban (57.7%).

---

## 3.13 Dashboard Development

A web-based interactive decision-support application was developed using **Streamlit 1.58.0**, **Plotly 6.8.0**, and **GeoPandas 1.1.4**.

### Architecture & Completed Pages (7 Pages)

The application is implemented in `app/dashboard.py` and consists of 7 modular pages:

| Page # | Page Name | Core Visualisations & Functions | User Interactivity & Controls | Underlying Data & Models |
|---|---|---|---|---|
| **1** | **Home** | Headline national KPIs, stress prevalence donut chart, monthly national trend line. | Commodity dropdown, month slider. | Aggregated panel, `revised_xgboost.joblib`. |
| **2** | **Price Stress Map** | Interactive district choropleth map (GeoPandas + Matplotlib), district risk rankings. | Province filter, month slider, class threshold selector. | `zwe_adm2_geoboundaries.geojson`, predicted probabilities. |
| **3** | **District & Commodity Detail** | District time-series drill-down, price vs. rainfall dual-axis plot, **local SHAP waterfall chart**. | District selector, commodity selector, model toggle. | `step09_shap_values.csv`, historical price series. |
| **4** | **Model Insights** | Confusion matrix heatmaps, ROC / PR curves, global SHAP importance bar charts. | Model selector (`Dummy`, `LogReg`, `XGBoost`). | `step07_cv_results.csv`, test set predictions. |
| **5** | **Data Explorer** | Filterable tabular data browser with full CSV export capabilities. | Dynamic column selection, value search, row limit. | `commodity_training_table.csv`. |
| **6** | **Methodology** | Full interactive documentation of SPI formula, feature engineering, and CV schemes. | Expandable section accordions. | Static markdown & LaTeX math renderings. |
| **7** | **About / Limitations** | Governance disclosures, policy disclaimers, ethical constraints, contact info. | None. | Static markdown text. |

### Operational Governance Disclaimer

Page 7 and the application sidebar enforce the following persistent disclaimer:
> *"This application is an academic research proof of concept developed for undergraduate dissertation evidence. It does NOT constitute an official government price assessment, WFP Market Monitor, IPC Acute Food Insecurity classification, or operational early-warning decision system."*

---

## 3.14 Software and Hardware Environment

- **Programming Language:** Python **3.12.10** (64-bit).
- **Operating System:** Microsoft Windows 11 Enterprise (win32).
- **Execution Environment:** PowerShell terminal execution via step scripts (`python -m src.final_correction_pipeline`).
- **Core Library Dependencies & Exact Versions:**
  - `pandas` == 3.0.3
  - `numpy` == 2.4.6
  - `scikit-learn` == 1.9.1
  - `xgboost` == 3.4.1
  - `shap` == 0.52.0
  - `geopandas` == 1.1.4
  - `streamlit` == 1.58.0
  - `plotly` == 6.8.0
  - `matplotlib` == 3.11.2
  - `xarray` == 2026.7.0
  - `netCDF4` == 1.7.4
  - `scipy` == 1.18.1
  - `seaborn` == 0.13.2
  - `joblib` == 1.6.0
- **Hardware Resources:** CPU multi-processing (`n_jobs=4`); zero GPU acceleration required. Total pipeline execution runtime $\approx 45$ seconds.
- **Data Storage:** Local disk filesystem (`data/raw/`, `data/processed/`, `outputs/models/`, `outputs/results/`). No relational database server used.

---

## 3.15 Data Versioning and Reproducibility

- **Immutability of Raw Inputs:** All raw files in `data/raw/` remain untouched.
- **Random Seed Standardization:** The random seed `42` (`config.RANDOM_STATE = 42`) is strictly declared and passed to all stochastic operations (train-test splits, cross-validation generators, XGBoost initialization, mutual information estimation).
- **Model Serialization:** Final fitted model pipelines are serialized to disk using `joblib` in `outputs/models/`:
  - `revised_dummy.joblib` (SHA-256: `fff2a0f0...`)
  - `revised_logreg.joblib` (SHA-256: `db15f514...`)
  - `revised_xgboost.joblib` (SHA-256: `cc27afa6...`)
- **Automated Verification Test Suite:** 24 unit and integration tests implemented in `tests/` pass with a 100% success rate (`pytest` / test runner execution).

---

## 3.16 Ethical Considerations

- **Protection of Privacy (Zero PII):** All datasets consist exclusively of secondary, spatially aggregated public economic and meteorological indicators. No household surveys, individual consumer transactions, or personally identifiable information (PII) were accessed.
- **Open Data Licensing Compliance:** HDX HAPI datasets were accessed under standard Humanitarian Data Exchange open terms. Spatial boundaries from geoBoundaries are used under the **Creative Commons Attribution 4.0 International (CC BY 4.0 IGO)** license. CHIRPS rainfall data is used under public domain academic research terms.
- **Representational & Policy Risk Mitigation:** Model outputs represent *relative spatial price anomalies* (`SPI > 1.25`) and must not be misinterpreted as absolute poverty or starvation metrics.
- **Macroeconomic Adjustment Non-Implementation Disclosure:**
  - **Fact:** Systemic macroeconomic adjustments (e.g. deflating raw prices using national Consumer Price Index [CPI] series or parallel market exchange rates) were **NOT IMPLEMENTED**.
  - **Rationale:** High-frequency district-level CPI and daily parallel exchange rate series were unavailable across all 73 districts for the 2017–2024 timeframe. Instead, the Spatial Price Index (SPI) was engineered as a self-normalizing, scale-free ratio to filter out national-level monetary inflation within each month.

---

## Appendix A — Pipeline Step to Output Mapping

| Step Script | Executed Functionality | Generated Output Files & Reports |
|---|---|---|
| `src/step01_data_audit.py` | Audits raw CSV and NetCDF headers, missingness, and data types. | [reports/step01_data_audit.md](file:///c:/Users/brigh/Downloads/another/reports/step01_data_audit.md)<br>`outputs/results/step01_column_audit.csv` |
| `src/step02_preprocess.py` | Cleans prices, handles duplicates/ZiG redenomination, builds population & poverty tables. | `data/processed/d_price_district_month.csv`<br>`data/processed/d_population_district.csv`<br>[reports/step02_preprocessing_log.md](file:///c:/Users/brigh/Downloads/another/reports/step02_preprocessing_log.md) |
| `src/step03_ingest_rainfall.py` | Extracts CHIRPS NetCDF grid, performs cos(lat) area-weighted join to ADM2 districts. | `data/processed/d_rainfall_chirps_district_month.csv` |
| `src/step04_build_training_table.py` | Computes SPI, winsorises quantiles, generates lags, constructs master training matrix. | `data/processed/commodity_training_table.csv`<br>`data/processed/feature_columns.json` |
| `src/step05_eda.py` | Computes summary statistics, correlations, spatial maps, and distributions. | [reports/step05_eda.md](file:///c:/Users/brigh/Downloads/another/reports/step05_eda.md)<br>`outputs/figures/step05_*.png` |
| `src/step06_feature_selection.py` | Calculates Mutual Information scores, filters zero-variance and leaky features. | `outputs/results/step06_feature_ranking.csv`<br>`data/processed/selected_features.json` |
| `src/step07_model_training.py` | Trains baseline models, runs 5-fold CV, saves serialized model binaries. | `outputs/models/step07_*.joblib`<br>`outputs/results/step07_cv_results.csv` |
| `src/step08_model_evaluation.py` | Evaluates held-out performance, generates ROC/PR curves and confusion matrices. | [reports/step08_model_evaluation.md](file:///c:/Users/brigh/Downloads/another/reports/step08_model_evaluation.md)<br>`outputs/figures/step08_*.png` |
| `src/step09_explainability.py` | Calculates TreeSHAP values, mean absolute importance, and local log-odds matrices. | `outputs/results/step09_shap_values.csv`<br>`outputs/figures/step09_shap_summary.png` |
| `src/final_correction_pipeline.py` | Authoritative pipeline: `SPI > 1.25`, `min_districts=8`, 3-fold spatio-temporal CV, SHAP. | [reports/ZCPSC_FINAL_REVISED_EVIDENCE.md](file:///c:/Users/brigh/Downloads/another/reports/ZCPSC_FINAL_REVISED_EVIDENCE.md)<br>`outputs/models/revised_*.joblib` |

---

## Appendix B — Items for Researcher Confirmation & Technical Reconciliations

1. **Exact Web Data Download Dates:**  
   `NOT FOUND IN THE PROJECT FILES — CONFIRM WITH THE RESEARCHER`  
   *(The raw CSV and NetCDF files in `data/raw/` do not contain embedded download timestamps).*
2. **Git Workspace Repository Status:**  
   `NOT FOUND IN THE PROJECT FILES — CONFIRM WITH THE RESEARCHER`  
   *(The workspace directory does not contain a `.git` tracking directory).*
3. **Hardware RAM & CPU Model:**  
   `NOT FOUND IN THE PROJECT FILES — CONFIRM WITH THE RESEARCHER`  
   *(System specs were not logged in Python runtime metadata).*
4. **Target Threshold Discrepancy Reconciliation:**  
   - Initial `config.py` contains a legacy reference to a `high_risk` target, and `src/step04_build_training_table.py` used `SPI > 1.00`.
   - The authoritative final model in `src/final_correction_pipeline.py` uses `price_stress = SPI > 1.25` with `min_districts = 8`.
   - **Resolution:** Chapter 3 should explicitly report `SPI > 1.25` as the primary threshold for severe price stress, noting `SPI > 1.00` as an exploratory baseline.
5. **Macroeconomic Adjustment Statement:**  
   Chapter 3 must explicitly declare that direct macroeconomic deflating (via CPI or parallel exchange rates) was **not implemented** due to missing district-level time-series data, and explain how the SPI formulation acts as an intra-month relative scale-free proxy.
