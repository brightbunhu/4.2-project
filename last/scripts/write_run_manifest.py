"""Write the final run manifest and hash every package output."""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parents[1]

INPUTS = [
    ("data/raw/hdx_hapi_food_price_zwe.csv", 4613370, "92a7def85f683a2fdabaa7edb48cbbbebb02633a9e51e5c0e0488275a543913f", "direct raw input", "WFP Food Prices & Market Monitor via HDX HAPI", "2017-01-15..2026-05-15 in reference_period_start", "UNKNOWN", "UNKNOWN", "UNKNOWN"),
    ("data/raw/hdx_hapi_population_zwe.csv", 650678, "8d74a4f4eb86977494b3c2c15418f56c2a4d944af14566e6d1f6afc8049ac399", "upstream source input", "UNFPA population baseline via HDX HAPI", "2023-01-01..2023-12-31 in raw rows; reports also call it 2020", "UNKNOWN", "UNKNOWN", "UNKNOWN"),
    ("data/processed/d_rainfall_chirps_district_month.csv", 8888072, "e8537658ef07d9d71ef1079209cb48f46ecbd338cef56e6debfb766888046d8a", "direct pipeline input", "CHIRPS v3 processed district-month data", "1981-01..2026-08", "UNKNOWN", "UNKNOWN", "UNKNOWN; release and retrieval date not recorded"),
    ("data/processed/d_population_district.csv", 15879, "02ad6652f215cacf358358eb4f7ac9398ea74ffbf8a78e72b672cfbbeff9046f", "direct pipeline input", "Processed UNFPA district population joined to ADM2", "reference period starts 2023-01-01", "UNKNOWN", "UNKNOWN", "UNKNOWN"),
    ("data/raw/chirps_v3_monthly_global.nc", 134, "9205bede991610bd986a1ec9f4b32c04326db022b42f7fa854c0396eeeecccaa", "upstream rainfall input; current workspace file is an LFS pointer", "CHIRPS v3 monthly global NetCDF pointer; expected object sha256 205f4f41011c94f47442f60e54c89af46bca8c23f865d310c53b6d2392282e60", "pointer expects a 353488971-byte object; actual file release/vintage UNKNOWN", "UNKNOWN", "UNKNOWN", "UNKNOWN"),
    ("data/raw/geo/zwe_adm2_geoboundaries.geojson", 17379177, "074a3632634b9448bb4043580fe7199e0b2f64ec68bd2f98932a2c68b3795b88", "upstream spatial reference", "geoBoundaries ZWE ADM2, boundaryID ZWE-ADM2-62879985", "represented 2020; source update 2023-01-19; build 2023-12-12", "https://github.com/wmgeolab/geoBoundaries/raw/9469f09/releaseData/gbOpen/ZWE/ADM2/geoBoundaries-ZWE-ADM2.geojson", "UNKNOWN retrieval date", "metadata: CC BY 3.0 IGO; config.py and Chapter 3 narrative say CC BY 4.0 IGO"),
    ("data/raw/geo/zwe_adm2_metadata.json", 1978, "7431de39f885696df85c8f5f207158a32470135e34fed155f5d558c2e0961a97", "spatial metadata", "geoBoundaries ADM2 metadata", "represented 2020; update 2023-01-19; build 2023-12-12", "https://github.com/wmgeolab/geoBoundaries/raw/9469f09/releaseData/gbOpen/ZWE/ADM2/geoBoundaries-ZWE-ADM2.geojson", "UNKNOWN", "CC BY 3.0 IGO in metadata; config.py conflicts"),
    ("data/processed/d_district_base.csv", 14053, "1a804b69ca633754ec088b2dc7f9d47f86a2adeeafa8f496794bc6606bfa5a09", "upstream spatial join input", "District lookup constructed from local administrative boundaries", "boundary represented 2020", "see ADM2 metadata", "UNKNOWN", "UNKNOWN"),
    ("src/run_option_b_pipeline.py", 38075, "92072b34d09e22e6cc06c3742d7482c0757a88c77e95013445a448642f36720d", "authoritative source code", "Option B T+1 modelling pipeline", "Git commit af7c134f2dafdce59e3f7d1d94ae553943799b39", "not applicable", "not applicable", "project source"),
    ("src/utils.py", 23421, "d156355a102108e4c465eb89939685f183636ac1949fed8a38725141c6b7c1f6", "source helper", "canon() key normalization and shared utilities", "Git commit af7c134f2dafdce59e3f7d1d94ae553943799b39", "not applicable", "not applicable", "project source"),
    ("src/step03_ingest_rainfall.py", 7903, "c37fad9f06d0a40b29db6133c1bcdd3804dff2eae918709b270630331fd2a5de", "rainfall processing source", "CHIRPS v3 grid-to-district processing", "Git commit af7c134f2dafdce59e3f7d1d94ae553943799b39", "not applicable", "not applicable", "project source"),
    ("config.py", 22815, "56984a778e8b4b8ad4b2d73a4fe3accc691305300c5d3a6d11a4e88893105212", "project configuration", "Option B paths and configuration", "Git commit af7c134f2dafdce59e3f7d1d94ae553943799b39", "not applicable", "not applicable", "project source"),
    ("outputs/option_b/data/option_b_modelling_table.csv", 2691861, "546e07d71c0204e95eaf341a51e207d1776ecc08941350605dc431cfacb83f25", "saved final modelling table", "6,908-row Option B table", "T 2017-01..2024-09; target through 2024-10", "not applicable", "not applicable", "existing project output"),
    ("outputs/option_b/data/option_b_feature_columns.json", 675, "2d7fd47452c2596a78c90cd04345d8e8a41b7847de816e0bcadd4051464da5d7", "feature contract", "23 ordered model feature names, target and horizon", "Option B run", "not applicable", "not applicable", "existing project output"),
    ("outputs/option_b/results/option_b_model_metrics.csv", 1033, "b5bf62a324c38eb61634728bbb839aa77ca44699605db9f333ddfa8dfe18903c", "structured fold metrics", "Three saved expanding-window folds", "run log timestamp 2026-10-08", "not applicable", "not applicable", "existing project output"),
    ("outputs/option_b/results/validation_audit.csv", 398, "a732353cd00c2ea41c4aa492ca351cbc45da432e19f53293777a8bc47c6107e4", "fold windows", "Saved train/test windows and row totals", "run log timestamp 2026-10-08", "not applicable", "not applicable", "existing project output"),
    ("outputs/option_b/results/target_shift_audit.csv", 336, "ff5cf7af7a84a014c9ba54a95726621726d472f5cf8927413a5b10df888c2284", "target stage audit", "11,879 SPI cells; 8,289 exact pairs; 1,136 positives", "run log timestamp 2026-10-08", "not applicable", "not applicable", "existing project output"),
    ("outputs/option_b/results/sensitivity_analysis.csv", 263, "c8294611a226cc9850f7344a49e799820a3d64695e91352f3661f408cabc0108", "existing label sensitivity output", "Thresholds 1.20, 1.25, 1.30 on exact-pair population", "run log timestamp 2026-10-08", "not applicable", "not applicable", "existing project output"),
    ("outputs/option_b/results/option_b_predictions.csv", 738187, "2ee64d5e8b2ec07e6f15ca39775774e1ba51c8cb0fa3f43f7eab5174708e33d3", "saved full-data predictions", "Final models predicted on same full 6,908 rows used to fit", "run log timestamp 2026-10-08", "not applicable", "not applicable", "in-sample production predictions; not fold predictions"),
    ("outputs/option_b/models/dummy_baseline.joblib", 1287, "8b69744c45303621348045e25b579f0629a62b4616fdfe33f71390898d4c943c", "saved final model", "DummyClassifier most_frequent", "full 6,908-row fit; seed not applicable", "not applicable", "not applicable", "existing project output"),
    ("outputs/option_b/models/logreg_pipeline.joblib", 3249, "48ceebbf74d2dbf360690cb2c91db2c499c59427aacba3c073fa0a157160bd42", "saved final model", "median imputer + scaler + balanced LogisticRegression, max_iter=1000, random_state=42", "full 6,908-row fit", "not applicable", "not applicable", "existing project output"),
    ("outputs/option_b/models/xgboost_pipeline.joblib", 254160, "775566985104eaa126795f6fa999e1b52017e80774b6ae741983c93fdacf5233", "saved final model", "median imputer + XGBoost (150 estimators, depth 4, learning rate .05, subsample/colsample .8, pos weight 2.5, seed 42)", "full 6,908-row fit", "not applicable", "not applicable", "existing project output"),
    ("outputs/_step03_log.txt", 1597, "2b7e6a1e16fbd0f261836ab05f584d446ebe9ddefa837ea3bf2a59ea9425b3c8", "rainfall processing log", "28,800 grid centres; 13,411 matched; 90 districts; Mvurwi nearest-cell fallback; 91 output districts", "log file timestamp not recorded", "not applicable", "not applicable", "existing project output"),
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_csv(path: Path):
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def main() -> None:
    source_inputs = []
    for rel, size, digest, role, identifier, vintage, url, retrieval, license_note in INPUTS:
        actual = ROOT / rel
        source_inputs.append({"path": rel, "size_bytes": size, "sha256": digest, "role": role,
                              "source_or_identifier": identifier, "reference_period_or_version": vintage,
                              "source_url": url, "retrieval_date": retrieval, "license": license_note,
                              "on_disk_size_matches_record": actual.stat().st_size == size,
                              "on_disk_sha256_matches_record": sha256(actual) == digest})
    package_files = []
    for path in sorted(OUT.rglob("*")):
        if path.is_file() and path.name != "run_manifest.json":
            package_files.append({"path": path.relative_to(ROOT).as_posix(),
                                  "size_bytes": path.stat().st_size, "sha256": sha256(path)})

    features = json.loads((OUT / "models/option_b_feature_columns.json").read_text(encoding="utf-8"))["features"]
    windows = read_csv(OUT / "validation_windows.csv")
    manifest = {
        "manifest_version": 1,
        "manifest_generated_date": "2026-10-11",
        "project_root": ".",
        "project_git_commit": "af7c134f2dafdce59e3f7d1d94ae553943799b39",
        "project_name_from_sources": "Option B Zimbabwe district-level next-month relative commodity-price stress",
        "requested_Bunhu_folder_found": False,
        "script_entry_point": "src/run_option_b_pipeline.py",
        "reference_run_command": "python src/run_option_b_pipeline.py",
        "current_session_authoritative_pipeline_rerun": {
            "status": "NOT PERFORMED",
            "reason": "Available bundled Python 3.12.14 runtime lacks scikit-learn, XGBoost, SHAP, joblib and pytest; source entry point also writes to existing outputs/option_b and reports directories.",
            "prior_project_record": {"status": "SUCCESS according to existing log; not independently rerun", "started": "2026-10-08 12:34:03 local log time", "ended": "2026-10-08 12:34:10 local log time", "source_log": "outputs/option_b/logs/pipeline_run.log"},
        },
        "audit_commands_executed": [
            {"command": "python last/scripts/reconcile_counts.py", "status": "PASS", "description": "Standard-library reconstruction of price aggregation, SPI, exact T+1 pairs, reporting-gap attrition, price comparison, and name-based spatial key audit.", "runtime": "Python 3.12.14; standard library only", "exact_start_end_time": "UNKNOWN (not captured by execution wrapper)"},
            {"command": "python last/scripts/rebuild_available_predictions.py", "status": "PASS for Dummy and persistence only", "description": "Test-window rows only; Dummy trained by majority count in training rows; persistence uses observed price_stress_current at T.", "exact_start_end_time": "UNKNOWN (not captured by execution wrapper)"},
            {"command": "python last/scripts/export_metrics.py", "status": "PASS for confusion and classification metric recomputation", "description": "Exports structured fold metrics, arithmetic means, confusion CSVs, and independent persistence fold scores. Probability metrics remain source-reported.", "exact_start_end_time": "UNKNOWN (not captured by execution wrapper)"},
            {"command": "python last/scripts/run_validation_checks.py", "status": "COMPLETED WITH FAILURES AND NOT-RUN CHECKS", "description": "Validation outcomes are in validation_checks.txt.", "exact_start_end_time": "UNKNOWN (not captured by execution wrapper)"}
        ],
        "runtime": {
            "audit_python": "3.12.14",
            "audit_python_path": "C:/Users/brigh/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe",
            "audit_importable_versions": {"pandas": "3.0.1 (available but not used by audit scripts)", "numpy": "2.3.5 (available but not used by audit scripts)"},
            "unavailable_in_audit_runtime": ["scikit-learn", "xgboost", "shap", "matplotlib", "seaborn", "joblib", "geopandas", "xarray", "pytest"],
            "recorded_source_run_environment_not_reverified": {"python": "3.14.3", "pandas": "3.0.2", "numpy": "2.4.4", "scikit-learn": "1.8.0", "xgboost": "3.4.1", "shap": "0.52.0", "joblib": "1.5.3", "streamlit": "1.65.0", "pytest": "9.1.1"}
        },
        "primary_data_inputs_and_source_artifacts": source_inputs,
        "observed_file_change_during_audit": {
            "path": "data/raw/chirps_v3_monthly_global.nc",
            "initial_observation": {"size_bytes": 8943423563, "sha256": "26052751cc1077329798b2e79d34606473a242fcd03f4912acd8d07f91835bf3", "observed_before": "2026-10-11 07:34:56 UTC"},
            "current_observation": {"size_bytes": 134, "sha256": "9205bede991610bd986a1ec9f4b32c04326db022b42f7fa854c0396eeeeccaa", "git_lfs_object_sha256": "205f4f41011c94f47442f60e54c89af46bca8c23f865d310c53b6d2392282e60", "git_lfs_object_size_bytes": 353488971, "last_write_time_utc": "2026-10-11 07:34:56"},
            "cause": "UNKNOWN",
            "audit_scripts_wrote_to_this_existing_file": False,
            "effect": "The Option B count reconstruction used the existing processed district rainfall CSV, not this NetCDF. A fresh CHIRPS ingest cannot be reproduced from the current pointer without retrieving the LFS object."
        },
        "target_definition": {
            "unit_key": ["district_key", "commodity_name", "prediction_month", "currency_code"],
            "forecast_horizon": "one exact calendar month T to T+1",
            "label": "1 iff spatial_price_index at T+1 > 1.25",
            "spi": "district aggregated price divided by same-month, same-commodity, same-currency peer median; peer groups require at least 8 distinct district strings",
            "price_aggregation": "median of market quotes at district × month × commodity × currency",
            "currency_handling": "USD and ZWL are separate peer groups; no conversion",
            "stage_counts": {"raw_quotes": 25554, "after_April_2024_ZWL_exclusion": 25550, "aggregated_cells": 13924, "valid_SPI_cells": 11879, "exact_T_plus_1_pairs": 8289, "final_model_rows": 6908, "exact_pair_positives": 1136, "final_model_positives": 904, "excluded_by_reporting_gap_rule": 1381},
            "competing_aggregation_count": {"count": 13934, "status": "not found in available source; unresolved origin"}
        },
        "random_seed": 42,
        "fold_boundaries": windows,
        "predictor_order": features,
        "preprocessing": {
            "spi_winsorization": "global 1st/99th quantiles over all valid SPI values before folds; temporal leakage risk",
            "commodity_encoding": "top-10 commodity vocabulary selected on full exact-pair dataset before folds; future distribution information risk",
            "imputation": "median SimpleImputer inside fold model pipelines; code indicates fit on fold training rows",
            "scaling": "StandardScaler inside Logistic Regression pipeline; code indicates fit on fold training rows; none for XGBoost",
            "population": "processed reference-period 2023 baseline; used in earlier forecast folds; historical availability is unknown and is a look-ahead concern",
            "rainfall": "CHIRPS v3 district-month, grid centres within ADM2; Mvurwi nearest-cell fallback recorded; cos(latitude) weights; 3/6/12-month totals and 1991-2020 climatology; data release availability at T unknown",
            "blank_admin2": "214 raw quotes have blank admin2; 32 exact target pairs (26 final rows) have blank district_key, although original audit counts zero nulls"
        },
        "sensitivity_label_counts_only": read_csv(OUT / "target_threshold_sensitivity.csv"),
        "metrics_provenance": {
            "structured_metrics_source": "outputs/option_b/results/option_b_model_metrics.csv",
            "metric_summary_rule": "unweighted arithmetic mean across folds; not pooled",
            "classification_metrics": "recomputed from saved fold confusion counts and agree to four-decimal source values",
            "roc_pr_brier": "structured values retained from source; raw fold probability vectors unavailable for independent recalculation",
            "persistence_macro_f1": {"fold_1": 0.7259, "fold_2": 0.7319, "fold_3": 0.7594, "unweighted_mean": 0.7391},
            "figure_discrepancy": "saved full-table predictions reproduce disputed LR TP/AUC 682/0.849233 and XGB 626/0.941730; source figures are resubstitution outputs, while fold-held-out TP totals are 375 and 148"
        },
        "model_artifacts_copied_to_last_models": ["dummy_baseline.joblib", "logreg_pipeline.joblib", "xgboost_pipeline.joblib", "option_b_feature_columns.json", "model_contract.json"],
        "inference_contract_status": "Feature names/order, classes, model configurations, and script are included. Inference script not run because joblib/scikit-learn/XGBoost are unavailable. Saved estimators are full-data fits, not fold models.",
        "validation_results_file": "last/validation_checks.txt",
        "package_output_hash_scope": "All regular files under last/ except run_manifest.json itself (a self-hash would be recursive).",
        "unresolved_limitations": [
            "Bunhu project folder absent in available workspace.",
            "Full source pipeline not rerun in the current session.",
            "Logistic Regression and XGBoost row-level test predictions and fold probability scores were not persisted; not recreated.",
            "No fold-level ROC/PR figures generated because held-out score vectors are unavailable.",
            "Global SPI quantiles and full-data top-10 commodity selection precede folds.",
            "2023 population baseline release timing relative to 2017-2024 forecast origins unknown.",
            "HAPI and CHIRPS source URLs, retrieval dates and licences unknown in local files.",
            "geoBoundaries metadata says CC BY 3.0 IGO; config.py and Chapter 3 narrative say CC BY 4.0 IGO.",
            "The 13,934 aggregation claim was not found in the available project; 13,924 is supported locally.",
            "Market rows include 32 blank-district exact pairs (26 final rows).",
            "No alternate-threshold model retraining performed; sensitivity file contains prevalence counts only."
        ],
        "package_outputs": package_files,
    }
    (OUT / "run_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"source_inputs={len(source_inputs)} all_sizes_hashes_match={all(x['on_disk_size_matches_record'] and x['on_disk_sha256_matches_record'] for x in source_inputs)}")
    print(f"package_outputs_hashed={len(package_files)} manifest={OUT / 'run_manifest.json'}")


if __name__ == "__main__":
    main()
