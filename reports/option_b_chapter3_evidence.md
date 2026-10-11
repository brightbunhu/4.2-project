# Chapter 3: Methodology Evidence Base (Option B Implementation Record)

> **Document Purpose:** This document provides the complete, authoritative, and verified empirical evidence base for writing **Chapter 3 (Methodology)** of the undergraduate dissertation. Every statement, parameter, mathematical formulation, and architectural choice reflects code and data actually executed in this repository under **Option B**.

---

## 1. Research Methodology Used
The study applies the **Cross-Industry Standard Process for Data Mining (CRISP-DM)** lifecycle coupled with a **Design-Science Research (DSR)** artifact: an interactive decision-support dashboard built in Streamlit. The methodology progresses cyclically through Business/Problem Understanding, Data Understanding, Data Preparation, Modeling, Evaluation, and Deployment.

## 2. CRISP-DM Justification
CRISP-DM was selected because:
- It naturally accommodates the iterative transformation of raw observational data (market quotes, satellite gridded precipitation, census population) into a supervised learning problem.
- Its distinct separation between Data Preparation and Modeling enforces strict controls against temporal leakage, which is vital when transitioning from a diagnostic current-month formulation to a genuine one-month-ahead predictive task ($T \to T+1$).

## 3. Research Design
- **Paradigm:** Quantitative, empirical, supervised predictive machine learning classification.
- **Problem Formulation:** Binary classification estimating whether a district–commodity observation will experience relative price stress in month $T+1$ based strictly on information available at or before month $T$.
- **Predictive Horizon:** Exactly one calendar month forward ($\Delta m = 1$).

## 4. Data Sources and Acquisition
1. **WFP Food Prices & Market Monitor (HDX HAPI):** 25,554 raw market observations (2017–2024).
2. **CHIRPS v3 Monthly Gridded Rainfall (CHC/USGS):** High-resolution (0.05°) satellite rainfall gridded data aggregated across Zimbabwean districts (1981–2024).
3. **UNFPA Population Baseline (HDX HAPI):** 2020 district population aggregates (5,508 age-gender rows aggregated to 91 ADM2 district totals).
4. **geoBoundaries ADM1 & ADM2 Boundaries (2020, CC BY 4.0 IGO):** 10 provincial boundaries and 91 district polygons.

## 5. Data-Source Roles
- **Market Prices:** Primary source for Spatial Price Index (SPI) derivation, historical market price momentum, reporting continuity, and the shifted target label.
- **CHIRPS Rainfall:** Primary source for agro-climatological context (monthly rainfall, 3/6/12-month rolling totals, and standardized anomalies).
- **Population:** Demographic context (log population and urban/rural classification).
- **geoBoundaries:** Administrative spatial alignment and choropleth mapping.

## 6. Data Integration
Integration is performed via deterministic relational joins:
- Canonical district keys (`district_key`) and calendar timestamps (`prediction_month`) serve as the core join spine.
- Market prices aggregated to district median: $\text{district\_key} \times \text{commodity\_name} \times \text{prediction\_month} \times \text{currency\_code}$.
- Left join with CHIRPS rainfall on `[district_key, prediction_month]`.
- Left join with UNFPA population on `district_key`.

## 7. Natural Analytical Unit
The natural key throughout data preparation, modeling, and evaluation is:
$$\text{district\_key} + \text{commodity\_name} + \text{prediction\_month } T + \text{currency\_code}$$
- **Audit Result:** Verified zero duplicate natural keys across all 6,908 modelling table observations (`outputs/option_b/results/natural_key_audit.csv`).

## 8. Data Cleaning
1. **Canonical District Name Normalization:** Applied `canon()` helper to uppercase place names, collapse whitespace, and standardize boundary naming discrepancies (`CENTENARY MUZARABANI`, `MHONDORO NGEZI`).
2. **Exclusion of Non-Food Items:** Filtered raw price data to food categories using `config.FOOD_CATEGORIES`.
3. **April 2024 Redenomination Treatment:** 4 raw ZWL quotes in April 2024 were audited and purged due to currency changeover distortions during the introduction of Zimbabwe Gold (ZiG).

## 9. Missing-Value Handling
- **Structural Series Warm-Ups:** Lagged features (`spi_lag_1`, `spi_lag_2`, `spi_pct_change_3m`) produce missing values at the beginning of each district-commodity sequence. These are median-imputed **inside training folds only**.
- **Rainfall Gaps:** Imputed with outer training set medians inside pipeline objects.

## 10. Duplicate Handling
- Market-level quotes within the same district, commodity, month, and currency are collapsed to their median price.
- Exact natural key deduplication uses deterministic chronological sorting. Duplicate count in final modelling table is **0**.

## 11. Outlier Handling
- **Raw Extreme Prices:** Retained without artificial truncation, as genuine hyperinflationary episodes represent valid empirical history in Zimbabwe.
- **SPI Winsorization:** Raw relative price ratios winsorized at $[0.01, 0.99]$ quantiles to suppress border quote recording artifacts.

## 12. Spatial Price Index Construction
For district $i$, commodity $c$, month $t$, and currency $u$:
$$\text{SPI}(i,c,t,u) = \frac{\text{Price}(i,c,t,u)}{\text{Median}_{j \in \mathcal{D}(c,t,u)}(\text{Price}(j,c,t,u))}$$
where $\mathcal{D}(c,t,u)$ represents eligible reporting districts under a minimum reporting threshold of $|\mathcal{D}| \ge 8$ districts (thin-cell guard). 2,045 sparse cells were excluded from reference median calculation.

## 13. Target Threshold
The project operational stress threshold is defined as:
$$\text{price\_stress}(t) = \begin{cases} 1 & \text{if } \text{SPI}(t) > 1.25 \\ 0 & \text{if } \text{SPI}(t) \le 1.25 \end{cases}$$
This operational threshold identifies district prices exceeding national medians by over 25%.

## 14. Target Shifting to T+1
The Option B predictive target is constructed as:
$$\text{target\_next\_month}(T) = \text{price\_stress}(T+1)$$
- **Strict Verification:** $\text{target\_month} = \text{prediction\_month} + 1 \text{ calendar month}$.
- Observations without an immediate following month or with gaps $>1$ month were removed and audited (8,289 retained before reporting filter; 6,908 in final modelling table).

## 15. Feature Engineering
The feature matrix incorporates 23 predictors strictly available at month $T$:
1. **Market Lags:** `spi_lag_1`, `spi_lag_2`, `spi_pct_change_3m`, `months_since_last_reported_price`.
2. **Rainfall Context:** `rainfall_1m`, `rainfall_3m_total`, `rainfall_6m_total`, `rainfall_12m_total`, `rainfall_3m_anomaly`.
3. **Demographic & Contextual:** `log_population`, `is_urban`, `month_of_year`, `year`.
4. **Commodity Indicators:** 10 binary one-hot indicators for top food commodities.

## 16. Feature-Availability Audit
Every feature was checked against the availability constraint:
$$\text{feature\_information\_date} \le \text{prediction\_month } T$$
All 23 predictors passed without violation (`outputs/option_b/results/feature_availability_audit.csv`).

## 17. Leakage Prevention
Strict architectural controls were enforced:
- Target-month price, target SPI, target stress, and future rainfall were strictly excluded from predictor matrices.
- Preprocessing objects were fitted strictly inside outer training folds.

## 18. Preprocessing Pipeline
Pipelines were implemented using scikit-learn's `Pipeline`:
- **Logistic Regression:** `SimpleImputer(strategy='median')` $\to$ `StandardScaler()` $\to$ `LogisticRegression`.
- **XGBoost:** `SimpleImputer(strategy='median')` $\to$ `XGBClassifier`.

## 19. Model Selection and Justification
Three models were chosen for principled comparison:
1. `DummyClassifier`: Establishes majority-class baseline.
2. `LogisticRegression`: Transparent, interpretable linear benchmark.
3. `XGBoost`: Gradient-boosted decision trees capable of capturing nonlinear interactions between rainfall anomalies and market momentum.

## 20. DummyClassifier Specification
- `strategy="most_frequent"`
- Predicts class 0 for all instances, serving as the empirical baseline.

## 21. Logistic Regression Specification
- `class_weight="balanced"` to counteract class imbalance ($\approx 14\%$ positive class).
- L2 penalty, `max_iter=1000`, `random_state=42`.

## 22. XGBoost Specification
- `n_estimators=150`, `max_depth=4`, `learning_rate=0.05`, `subsample=0.8`, `colsample_bytree=0.8`, `scale_pos_weight=2.5`, `random_state=42`, `eval_metric="logloss"`.

## 23. Model Training Protocol
Models were trained across 3 expanding temporal folds and subsequently refitted on the full dataset for deployment in `outputs/option_b/models/`.

## 24. Hyperparameter Tuning
Hyperparameters were tuned using fixed conservative configurations derived from cross-validation experiments, with class weighting calibrated to positive class prevalence.

## 25. Forward-Chaining Validation
Validation was executed across 3 expanding temporal windows:
- **Fold 1:** Train: 2017-01 to 2021-02 (3,427 rows) $\to$ Test: 2021-03 to 2022-10 (1,449 rows).
- **Fold 2:** Train: 2017-01 to 2022-10 (4,876 rows) $\to$ Test: 2022-11 to 2023-07 (1,203 rows).
- **Fold 3:** Train: 2017-01 to 2023-07 (6,079 rows) $\to$ Test: 2023-08 to 2024-09 (829 rows).
- Verified: $\max(T_{\text{train}}) < \min(T_{\text{test}})$ in all folds.

## 26. Spatial-Overlap Policy
In this operational early-warning setting, historical monitoring series for known districts are used to forecast their future risk ($T+1$). Folds share 29–38 monitoring districts across time splits.

## 27. Evaluation Metrics
Evaluated on out-of-sample data:
- **Macro-F1** (headline metric for imbalanced data)
- **Balanced Accuracy**
- **Precision, Recall, Specificity**
- **ROC-AUC & PR-AUC**
- **Brier Score**
- **Confusion Matrix**

## 28. Statistical and Exploratory Analysis
Exploratory procedures included SPI ratio distributions, temporal stress trends, thin-cell frequency distributions, and rainfall anomaly correlations.

## 29. Explainable Machine Learning
Implemented using **TreeSHAP** (`shap.TreeExplainer`) on the production XGBoost model, producing:
- Global feature importance rankings (`outputs/option_b/explainability/option_b_shap_importance.csv`).
- Per-observation local attributions (`outputs/option_b/explainability/option_b_local_explanations.csv`).
- Mandatory disclaimer: *"Feature contribution explains the fitted model prediction; it does not prove causation."*

## 30. Software Tools and Selection Rationale
- **Python 3.14.3:** Modern, robust execution environment.
- **pandas 3.0.2 & numpy 2.4.4:** High-performance tabular manipulation.
- **scikit-learn 1.8.0:** Validated ML pipelines and evaluation metrics.
- **xgboost 3.4.1:** High-performance gradient boosting.
- **shap 0.52.0:** Game-theoretic feature attribution.
- **Streamlit 1.65.0:** Rapid, interactive decision-support application.
- **pytest 9.1.1:** Rigorous automated test execution.

## 31. Reproducibility and Version Control
- All random states fixed at `42`.
- Git repository tagged at `previous-topic-archive`.
- Deterministic pipeline executed via `python src/run_option_b_pipeline.py`.

## 32. Dashboard Implementation
Implemented in Streamlit across 8 modular pages: Home, Next-Month Prediction (Manual & CSV), Price Stress Map, Commodity/District Detail, Model Insights, Data Explorer, Methodology, and About/Limitations.

## 33. Ethical Considerations
The prototype enforces strict responsible-use notices:
- Excludes household-level poverty claims.
- Does not assign official IPC phases.
- Mandates human-in-the-loop triangulation with official ZimVAC and FEWS NET assessments.

## 34. Methodological Limitations
- Remote rural market collection gaps (addressed via reporting continuity filter $\le 2$ months).
- Currency transitions in Zimbabwe (addressed via within-currency reference medians and April 2024 ZWL quote exclusion).
- Sparse commodity reporting cells (mitigated by thin-cell guard $\ge 8$ reporting districts).
