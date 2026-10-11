# Option B Explainability Report: TreeSHAP Attribution Analysis

## 1. Overview & Methodological Framework

Explanations are derived strictly from the **new Option B production models** using TreeSHAP (`shap.TreeExplainer`). TreeSHAP computes game-theoretic Shapley values across the gradient-boosted decision trees, quantifying each feature's contribution in log-odds units to the forecast of month $T+1$ relative stress.

## 2. Global Feature Importance Rankings

Extracted from `outputs/option_b/explainability/option_b_shap_importance.csv`:

| Rank | Feature Name | Source Domain | Mean |SHAP| (Impact on Log-Odds) |
|---|---|---|---|
| 1 | `year` | Temporal Trend | 0.8338 |
| 2 | `is_urban` | Demographic Context | 0.1665 |
| 3 | `rainfall_3m_total` | Rainfall Context | 0.0773 |
| 4 | `log_population` | Demographic Context | 0.0654 |
| 5 | `spi_lag_1` | Market Price History | 0.0582 |
| 6 | `rainfall_12m_total` | Rainfall Context | 0.0491 |
| 7 | `month_of_year` | Seasonal Timing | 0.0435 |
| 8 | `spi_pct_change_3m` | Market Price History | 0.0388 |
| 9 | `rainfall_3m_anomaly`| Rainfall Context | 0.0321 |
| 10 | `rainfall_6m_total` | Rainfall Context | 0.0289 |

## 3. Mandatory Causal Caveat

All figures, reports, and interactive UI components prominently display:
> *"Feature contribution explains the fitted model prediction; it does not prove causation."*
