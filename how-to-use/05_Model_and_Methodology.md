# 05 · Model & Methodology

The "why" behind the numbers on the dashboard. For the code-level view see
[07_Developer_Guide.md](07_Developer_Guide.md); for step-by-step evidence see
`reports/methodology_implementation.md` and `reports/option_b_*.md`.

---

## 1. The prediction task

```
X_t  ──────────►  Y_(t+1)
Set of features     Relative price stress
available at         in the following
month T              calendar month
```

- **Feasible/realistic setting:** only information available **by the cut-off month T** is
  used as predictors. The target is shifted one month forward (T+1).
- **Grain:** `district_key × commodity_name × prediction_month × currency_code`.
- **Definition of stress:** the Spatial Price Index crosses the project threshold
  (SPI > 1.25 for the dashboard's "High Stress" label).

---

## 2. Why shift the target? (leakage control)

If the model were allowed to see the *same-month* outcome, it would effectively read the
answer. Option B deliberately:
- shifts the label to `target_next_month`,
- restricts predictors to lagged/derived features (SPI lags, trailing rainfall windows,
  reporting-gap months),
- audits feature availability (`feature_availability_audit.csv`) and target shift
  (`target_shift_audit.csv`).

Tests enforce these guarantees: `test_no_data_leakage.py`,
`test_no_current_price_leakage.py`, `test_target_creation.py`, `test_feature_whitelist.py`.

---

## 3. Feature engineering (summary)

| Family | Features | Construction |
|--------|----------|--------------|
| Price momentum | `spi_lag_1`, `spi_lag_2`, `spi_pct_change_3m` | Lagged SPI + 3-month % change |
| Reporting gap | `months_since_last_reported_price` | Months since last observed price |
| Rainfall | `rainfall_1m/3m_total/6m_total/12m_total`, `rainfall_3m_anomaly` | Trailing windows + anomaly vs climatology |
| Population | `log_population`, `is_urban` | Log-scaled population + urban flag |
| Calendar | `month_of_year`, `year` | Seasonality and temporal trend |
| Commodity | `commodity_*` one-hots | Categorical commodity encoding |

See the full ordered list in
[04_Data_and_CSV_Guide.md §3](04_Data_and_CSV_Guide.md#3-features-the-model-consumes).

---

## 4. Models compared

| Model | Role | Pipeline |
|-------|------|----------|
| **DummyClassifier** | majority-class baseline | predict the most common class |
| **LogisticRegression** | interpretable linear benchmark | impute → standardise → logistic |
| **XGBoost** | **champion model** | impute → (tree model) gradient boosting |

All are `sklearn`/`imblearn`-style `Pipeline`s saved with `joblib` so that preprocessing
travels with the model (no train/serve skew). Saved as:
`dummy_baseline.joblib`, `logreg_pipeline.joblib`, `xgboost_pipeline.joblib`.

---

## 5. Validation strategy

- **Forward-chaining temporal validation** (three folds used in the shipped metrics),
  which respects time order and prevents training on the future.
- **Imputation & scaling fitted inside the pipeline** (see `test_pipeline_imputation.py`,
  `test_pipeline_scaling.py`) so no validation information leaks into training.
- **Audits** logged to `outputs/option_b/results/`: feature availability, target shift,
  natural key, model configuration, sensitivity.

---

## 6. Metrics (shipped `option_b_model_metrics.csv`)

Metrics per fold × model: accuracy, balanced accuracy, macro F1, **stress-class F1**,
precision, recall, specificity, **ROC-AUC**, **PR-AUC**, Brier score, and the confusion
counts.

Representative (Fold 1):

| Model | Accuracy | Balanced Acc. | Stress F1 | ROC-AUC | PR-AUC |
|-------|:--------:|:-------------:|:---------:|:-------:|:------:|
| Dummy | 0.950 | 0.500 | 0.000 | 0.500 | 0.050 |
| LogisticRegression | 0.874 | 0.749 | 0.325 | 0.846 | 0.364 |
| XGBoost | 0.952 | 0.665 | 0.417 | 0.836 | 0.457 |

**How to read this honestly:**
- Stress is **rare**, so *accuracy is misleading* (the Dummy baseline scores ~0.95 while
  detecting zero stress events). Prefer **balanced accuracy, stress-class F1, ROC-AUC and
  PR-AUC**.
- The Dummy row is reported deliberately to make this imbalance visible.
- Performance varies by fold; there is **no guarantee** it holds in future conditions.

Plots: `figures/option_b_roc_curves.png`, `option_b_pr_curves.png`,
`option_b_confusion_matrices.png`, `option_b_calibration_curves.png`,
`option_b_target_distribution.png`.

---

## 7. Explainability

- **Global:** mean absolute SHAP per feature →
  `explainability/option_b_shap_importance.csv` (and `figures/option_b_shap_summary.png`).
- **Local:** per-observation TreeSHAP contributions →
  `explainability/option_b_local_explanations.csv`. Served live by
  `OptionBPredictor.predict_single` under the `explanation` key
  (`top_increasing`, `top_decreasing`).
- The app's **Model Explanations** page visualises both.

**Critical interpretation rule:** SHAP shows how the *fitted model* weighted its inputs. It
is **association, not causation**, and explains model behaviour — not the real-world cause
of prices.

---

## 8. Reproducibility

- One authoritative runner: `python -m src.run_option_b_pipeline`.
- Fixed random seeds and saved pipelines.
- Full console log: `outputs/option_b/logs/pipeline_run.log`.
- Repro/audit reports: `reports/option_b_reproducibility_report.md`,
  `reports/reproducibility.md`, `reports/validation_audit.md`.

---

## 9. Known limitations (model-level)

- Class imbalance: few high-stress events relative to normal months.
- Potential distribution shift if future market/rainfall conditions differ from history.
- Relative (SPI-based) stress ≠ household food insecurity.
- Missing/uneven market reporting across commodities and districts.
- No IPC phase assignment.

See also Page 7 in the app and `reports/option_b_limitations.md`.
