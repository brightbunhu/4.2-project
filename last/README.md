# Evidence package for the Option B dissertation audit

## Project root and scope

The task file specified a project containing a `Bunhu` folder. The available workspace is `C:\Users\brigh\Documents\another`; recursive inventory found no `Bunhu` directory and no pre-existing `last` directory. This package was created at `C:\Users\brigh\Documents\another\last`. If the intended `Bunhu` project is elsewhere, this is the wrong project root and these outputs should be reviewed before being used there.

No existing project file was modified for this package. Source datasets and tables were read from their existing paths and are identified by relative path, size and SHA-256 in `run_manifest.json`; only model artifacts and their feature contract were copied into `last/models/`.

## Findings

The local project contains the authoritative Option B T+1 pipeline at `src/run_option_b_pipeline.py`, raw HAPI food prices, processed CHIRPS v3 district-month data, a processed population table, model artifacts, fold metrics, and a historical execution log. The log shows a successful source run on 2026-10-08. This session did not rerun the ML pipeline: the available bundled Python 3.12.14 runtime lacks scikit-learn, XGBoost, SHAP, joblib and pytest, and the pipeline writes into existing project output folders.

A standard-library reconstruction of the executable data-stage rules reproduced these counts exactly: 25,554 raw quotes; 25,550 after excluding 4 April 2024 ZWL quotes; 13,924 aggregated cells; 11,879 valid SPI cells; 8,289 exact T+1 pairs; and 6,908 final modelling rows. Its retained natural keys match the saved modelling table. The 1,381 row reduction is fully listed in `attrition_ledger.csv`, using the source rule `months_since_last_reported_price > 2.0`.

The 8,289-pair cohort has 1,136 positives (13.7049%); the distinct 6,908-row final cohort has 904 (13.0863%). A separate 13,934 aggregation count was not found in the available project files. The executable source, run log and Chapter 4 evidence file support 13,924. See `count_reconciliation.md`.

The held-out fold metric export is preserved and checked against its confusion counts. The source's full-table predictions reproduce the disputed image values (Logistic Regression TP=682/AUC=0.849233; XGBoost TP=626/AUC=0.941730). Source code shows those values come from production models fitted on all 6,908 rows and evaluated on those same rows. Structured fold-held-out TP totals are 375 and 148, respectively. The images therefore do not provide held-out evidence.

Fold-level Dummy and persistence predictions were reconstructed from test rows only. Persistence uses the observed class at prediction month T and exactly reproduces fold macro-F1 of 0.7259, 0.7319 and 0.7594 (unweighted mean 0.7391). The original Logistic Regression/XGBoost fold prediction vectors were never saved; their structured fold metrics are available, but their per-row predictions and probability vectors cannot be recreated in this runtime. `fold_predictions_index.csv` marks this gap. No held-out ROC/PR figures were generated, and `figures/` is intentionally empty.

During the audit, the CHIRPS NetCDF changed from an observed 8.94 GB file to a 134-byte Git LFS pointer (expected object SHA-256 `205f4f41011c94f47442f60e54c89af46bca8c23f865d310c53b6d2392282e60`, size 353,488,971 bytes). The cause is unknown; the audit scripts did not write to it. The Option B count audit used the processed rainfall CSV, so its results are unaffected, but a fresh CHIRPS ingest needs the LFS object. Both observations are recorded in `run_manifest.json`.\n\nThe audit also found two full-data scope risks in the source: SPI 1st/99th-percentile clipping and top-10 commodity selection occur before the folds. Population values are a 2023 reference-period baseline used in folds with 2017 origins; historical release availability is unknown. There are 32 exact-pair rows with blank `district_key` (26 in the final table), although the original null audit reports zero because an empty string is not null. More detail is in `preprocessing_scope_audit.md`, `feature_vintage_audit.csv`, and `spatial_join_audit.csv`.

## Package contents

- `run_manifest.json` — source commit, hashes, file sizes, configuration, environment, outputs, executed checks, and limitations.
- `count_reconciliation.md`, `attrition_summary.csv`, `attrition_ledger.csv` — verified stage counts and row-level continuity exclusions.
- `target_threshold_sensitivity.csv` — label counts at SPI 1.20, 1.25 and 1.30 with both stage denominators; no alternate-threshold model fits.
- `price_comparability_audit.csv`, `spatial_join_audit.csv`, `feature_vintage_audit.csv`, `preprocessing_scope_audit.md` — source and join evidence with unknowns called out.
- `validation_windows.csv`, `fold_predictions.csv`, `fold_predictions_index.csv` — saved windows and test-only predictions for Dummy and persistence; unavailable methods are explicitly indexed.
- `metrics_by_fold.csv`, `metrics_summary.csv`, `confusion_matrices/` — original structured fold metrics, reconstructed persistence metrics, unweighted fold means, and checked confusion totals.
- `models/` — copied full-data joblib models, feature order, `model_contract.json`, and `scripts/infer_with_saved_model.py`. These are full-data models, not outer-fold models. Inference was not run here because its ML dependencies are absent.
- `scripts/` — standard-library audit/reconstruction scripts and their checks. `validation_checks.txt` records executed passes, failures and checks that could not be run.
- `figures/` — intentionally empty because valid fold-level score vectors are unavailable.

The source URLs, retrieval dates and licences for HAPI and CHIRPS inputs were not recoverable from the inspected project files and are recorded as `UNKNOWN`. The ADM2 metadata records a CC BY 3.0 IGO licence, while `config.py` and the Chapter 3 evidence say CC BY 4.0 IGO; this conflict is preserved in the audit.

