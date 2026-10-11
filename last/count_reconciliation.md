# Count reconciliation

## Result

The available authoritative Option B source and the raw food-price input support **13,924** district × month × commodity × currency price cells. The supplied audit brief mentions a competing 13,934 count, but that value does not appear in the project reports, code outputs, or Option B run log inspected here. The origin of that separate value cannot be confirmed from this workspace. It remains an unresolved external table claim; the executable count in `src/run_option_b_pipeline.py` and its 2026-10-08 run log agree with an independent reconstruction in `scripts/reconcile_counts.py`.

The other counts refer to different stages and reconcile without treating one population as a correction to another:

| Stage | Rows | Positive labels | Denominator / rule | Evidence |
|---|---:|---:|---|---|
| Raw HAPI price quotations | 25,554 | — | Raw CSV rows | `data/raw/hdx_hapi_food_price_zwe.csv`; source run log |
| After April 2024 ZWL exclusion | 25,550 | — | 4 quotes excluded | `src/run_option_b_pipeline.py`; independently reproduced |
| Aggregated district price cells | 13,924 | — | Median within district × month × commodity × currency | Pipeline code, run log and independent reconstruction |
| Valid SPI cells | 11,879 | — | Same month × commodity × currency peer median; at least 8 named districts | Pipeline code and run log |
| Exact T+1 target pairs | 8,289 | 1,136 | Next valid observation exactly one calendar month later | `outputs/option_b/results/target_shift_audit.csv`; independent reconstruction |
| Final model rows | 6,908 | 904 | Exact target pairs retained by the source continuity rule (`months_since_last_reported_price <= 2.0`) | Existing Option B modelling table; independent row-level key match |

The 8,289-to-6,908 reduction is **1,381 rows**, all individually identified in `attrition_ledger.csv` with the executable exclusion reason `months_since_last_reported_price > 2.0 (pipeline rule)`. The rule computes elapsed days divided by 30.44, rounded to two decimals, since the previous exact-pair observation for the same district, commodity and currency; a first observation is retained. The source-rule retained keys equal the existing 6,908-row model table exactly.

The 1,136 positives among 8,289 pairs are **13.7049%**. The 904 positives among 6,908 final rows are **13.0863%**. The difference is 232 positive rows among the 1,381 excluded records. These are two distinct processing-stage populations, not a correction to the target labels.

## Source and code used

- Raw input: `data/raw/hdx_hapi_food_price_zwe.csv`.
- Executable source: `src/run_option_b_pipeline.py`, especially the aggregation, SPI, target-shift, and reporting-gap sections.
- Existing execution record: `outputs/option_b/logs/pipeline_run.log`, timestamped 2026-10-08 12:34:03–12:34:10. It records 25,554 quotes, 13,924 aggregates, 11,879 SPI-valid cells, 8,289 exact pairs and 6,908 final rows.
- Independent reconstruction: `scripts/reconcile_counts.py`, executed with bundled Python 3.12.14 on 2026-10-11. It uses Python standard-library CSV/date/math only, implements the source rules, writes `attrition_ledger.csv` and `attrition_summary.csv`, and checks retained natural keys against the existing model table.

`src/run_option_b_pipeline.py` computes the aggregation as `median(price)` at the stated grain; calculates within-month, commodity and currency median SPI; removes groups with fewer than 8 reporting districts; applies global 1st/99th percentile clipping; labels `SPI > 1.25`; shifts within district × commodity × currency; retains an exact one-month calendar gap; then applies the 2-month continuity filter.

## Positive-count and threshold reconciliation

The primary threshold is strictly `SPI > 1.25`. `outputs/option_b/results/sensitivity_analysis.csv` reports prevalence only over the 8,289 exact pairs: 1,416/8,289 at 1.20, 1,136/8,289 at 1.25, and 963/8,289 at 1.30. `target_threshold_sensitivity.csv` independently recomputes these counts and also provides the separate 6,908-row denominator: 1,132, 904 and 758 positives, respectively. No model was retrained at the alternative thresholds.

## Confusion-matrix and ROC-image discrepancy

The structured fold metrics in `outputs/option_b/results/option_b_model_metrics.csv` contain fold-held-out TP totals of 375 for Logistic Regression and 148 for XGBoost. Recalculation from the saved full-table predictions in `outputs/option_b/results/option_b_predictions.csv` gives TP=682 and ROC-AUC=0.849233 for Logistic Regression, and TP=626 and ROC-AUC=0.941730 for XGBoost. These round to the image claims of 682/0.849 and 626/0.942.

The source explains the difference: after cross-validation it fits final models on all 6,908 rows, writes predictions for those same rows, then creates the original ROC, precision-recall and confusion figures from that full-table prediction frame. Therefore the disputed figures are resubstitution/full-fit results, not the held-out fold results. This reconciles the displayed values' provenance; it does not make those figures valid held-out evaluation. No disputed figure was copied into this package.

## Remaining limitation

The `13,934` value is not supported by an underlying table in the available workspace. The current project files support `13,924`; the other value should be checked against the external dissertation table named in the supplied brief if that table is located.

## Metric conventions

The source sets `zero_division=0` for precision and F1, and the standard-library matrix reconstruction uses zero when a precision/recall denominator is zero. ROC-AUC and average precision are retained from the structured fold table; their underlying fold score vectors are unavailable, so they were not independently recomputed. Persistence is a deterministic class comparator without a calibrated probability; its ROC-AUC, PR-AUC and Brier values are left blank. Any undefined probability metric is left unavailable rather than imputed.
