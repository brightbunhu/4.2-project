# Preprocessing scope and temporal availability audit

## Target and fold protocol recorded by the source

The Option B source labels `target_next_month = 1` when the SPI for the exact next calendar month is strictly greater than 1.25. Target pairing is performed within `district_key × commodity_name × currency_code`. The saved validation windows are expanding in time, with prediction-month windows:

| Fold | Training | Test |
|---|---|---|
| Fold 1 | 2017-01 to 2021-02 | 2021-03 to 2022-10 |
| Fold 2 | 2017-01 to 2022-10 | 2022-11 to 2023-07 |
| Fold 3 | 2017-01 to 2023-07 | 2023-08 to 2024-09 |

These windows come from the available 2026-10-08 Option B run outputs. They are dynamically generated from fractions of the available months by the current source script; no frozen fold-date configuration file was found.

## Transformations and feature selection

| Operation | Source-code scope | Finding |
|---|---|---|
| SPI 1st/99th percentile clipping | `src/run_option_b_pipeline.py` computes quantiles over all valid SPI observations before target folds are built | **Temporal leakage risk.** Future distribution values affect clipped SPI and can affect both predictors and target labels. It was not recomputed fold-wise because that would change the recorded primary analysis. |
| Top-10 commodity vocabulary | `value_counts().head(10)` over the full exact-pair table, before folds | **Temporal information risk.** Category vocabulary uses future data. |
| Market price and rainfall joins | Market SPI/lags and rainfall are attached at prediction month T | Code-level date rule is at/before T. Actual publication/retrieval vintage at each historical origin is not recorded. |
| `SimpleImputer(strategy='median')` | Inside each Logistic Regression/XGBoost scikit-learn pipeline fitted on each fold's training rows | Training-fold fit scope is supported by source code. This pipeline was not rerun in this session. |
| `StandardScaler()` | Inside Logistic Regression pipeline fitted on each fold's training rows | Training-fold fit scope is supported by source code. XGBoost has no scaler. |
| Final production models | Refit on all 6,908 final rows after outer evaluation | These are inference artifacts, not fold-held-out estimators. Their predictions over the same 6,908 rows are in-sample. |
| Market history lags | `shift()` is applied after filtering to exact T+1 candidate pairs | A lag means the prior retained pair observation, which may be more than one calendar month earlier; the separate gap filter only rejects gaps above 2.0 months. |

## Feature vintage and availability

The raw population CSV and processed district baseline show `reference_period_start=2023-01-01`; the dissertation evidence text also calls this a 2020 baseline, while the source utility docstring describes a 2023 vintage. The actual local table is a 2023 reference-period file. Its release/retrieval date is unknown. Using these values for folds whose forecast origins precede 2023 is not demonstrably historically available and is a temporal look-ahead concern.

The model uses processed CHIRPS v3 district-month features, not the province-level HAPI rainfall CSV. The processing code identifies the global NetCDF as CHIRPS v3 and uses grid-cell centres inside geoBoundaries ADM2 polygons; unmatched districts receive a nearest representative-point cell fallback. The district series uses cosine-latitude weighting, rolling 3/6/12-month totals and a 1991–2020 monthly climatology. Exact CHIRPS release/retrieval date, file metadata vintage and monthly operational publication lag are not recorded. Availability of finalized rainfall at each forecast origin is therefore **UNKNOWN**.

The saved feature audit checks column names and describes an information date at or before T, but it does not independently establish publication dates for CHIRPS or the 2023 population baseline. The raw-to-model market district key is name-based (`canon(admin2_name)`); blank district names become an empty string and were not treated as null by the source's natural-key audit. The independent audit found 214 raw quotations with blank ADM2 and 32 exact-pair rows (26 final rows) with blank `district_key`.

## Interpretation

The fold-specific model scores remain those in the structured Option B results and are not recalculated here. They should be reported alongside the two identified full-data transformation risks and the unresolved historical feature-vintage evidence. No threshold was selected using outer-fold results, and no target definition or dissertation objective was changed.
