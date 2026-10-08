# Option B Pre-Implementation Audit Report

## 1. Executive Summary

This pre-implementation audit documents the architectural transition of the Zimbabwe Commodity Price Stress Classifier (ZCPSC) from a contemporaneous (current-month) diagnostic classifier to a genuinely predictive, forward-looking machine learning system (Option B):

> **Predictive Horizon:** Information available at calendar month $T \longrightarrow$ Relative commodity-price stress at month $T+1$.

## 2. Inventory of Baseline System State vs. Option B Requirements

| Architectural Dimension | Legacy Implementation | Option B Specification | Audit Finding |
|---|---|---|---|
| **Target Definition** | Contemporaneous: $y(T) = \mathbb{I}(\text{SPI}(T) > 1.25)$ | Forward-Shifted: $y(T) = \text{price\_stress}(T+1)$ | Transition required full regeneration of target column. |
| **Prediction Horizon** | Month $T$ to Month $T$ (diagnostic) | Month $T$ to Month $T+1$ (one-month-ahead predictive) | Strict calendar continuity required: $\text{target\_month} = \text{prediction\_month} + 1 \text{ month}$. |
| **Predictor Eligibility** | Included concurrent rainfall & market metrics | Predictors strictly $\le T$. Forbidden: target-month price, target SPI, target stress. | Automated leakage audit required with immediate halt on violation. |
| **Validation Scheme** | Spatial / Stratified K-Fold | Strict Expanding Temporal Forward-Chaining ($T_{\text{train}} < T_{\text{test}}$) | Prevents temporal leakage across price inflation regimes. |
| **Storage Structure** | Mixed in `outputs/` | Dedicated, segregated `outputs/option_b/` hierarchy | Protects historical evidence while providing clean Option B artifacts. |

## 3. Data Integration & Provenance Verification

1. **WFP Market Price Records (`hdx_hapi_food_price_zwe.csv`):** 25,554 raw records covering 2017 to 2024.
2. **April 2024 Currency Redenomination Audit:** 4 raw ZWL quotes in April 2024 were audited and purged due to currency changeover distortions (introduction of Zimbabwe Gold, ZiG).
3. **Thin-Cell Protection:** Established minimum reporting threshold of $\ge 8$ districts per commodity-month-currency cell. 2,045 sparse records suppressed from national reference median computation.
4. **CHIRPS v3 Gridded Rainfall:** Processed monthly district precipitations (1981–2024) matched strictly to prediction month $T$.
5. **UNFPA Population Baselines:** District-level log population and urban/rural classification joined statically on canonical district keys.

## 4. Pre-Implementation Audit Sign-Off

The audit confirmed that all architectural preconditions for Option B were met:
- Natural key standardisation established (`district_key + commodity_name + prediction_month + currency_code`).
- Zero tolerance for future information leakage confirmed.
- Model family approved: Dummy Baseline, Logistic Regression, XGBoost.
