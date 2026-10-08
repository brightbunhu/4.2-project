# Option B Data Quality & Natural Key Audit Report

## 1. Overview & Data Provenance

The Option B pipeline ingests four primary datasets for predictive modeling:
1. **WFP Market Prices:** 25,554 raw entries across 73+ districts and 28 commodity definitions.
2. **CHIRPS Gridded Rainfall (v3):** District-aggregated monthly totals, 3-month/6-month/12-month rolling totals, and 3-month standardized anomalies.
3. **UNFPA Population:** 2020 district population totals and urban/rural classification.
4. **geoBoundaries ADM2 Boundaries:** Canonical district polygons for spatial aggregation and mapping.

## 2. Natural Key Audit

The primary unit of analysis for Option B is:
$$\text{district\_key} \times \text{commodity\_name} \times \text{prediction\_month} \times \text{currency\_code}$$

### Natural Key Verification Metrics
- **Total Valid Observations in Final Modelling Table:** 6,908
- **Duplicate Keys:** 0 (Verified zero exact duplicated natural keys)
- **Null Keys:** 0 (Verified zero missing values across key fields)
- **Distinct Reporting Districts:** 73
- **Distinct Commodities:** 16 (Top 10 explicitly one-hot encoded; remainder captured in contextual basket)
- **Distinct Currency Codes:** USD and ZWL (modeled with isolated median references)
- **Prediction Month Range:** January 2017 to September 2024 (57 distinct monthly observation periods)
- **Target Month Range:** February 2017 to October 2024 (57 distinct monthly target periods)
- **Audit Outcome:** **PASSED** (Logged in `outputs/option_b/results/natural_key_audit.csv`)

## 3. Spatial Price Index (SPI) Construction & Thresholding

For district $i$, commodity $c$, prediction month $t$, and currency $u$:
$$\text{SPI}(i,c,t,u) = \frac{\text{Price}(i,c,t,u)}{\text{Median}_{j \in \mathcal{D}(c,t,u)}(\text{Price}(j,c,t,u))}$$
where $\mathcal{D}(c,t,u)$ represents eligible reporting districts with $|\mathcal{D}| \ge 8$.

- **Thin Cell Protection:** 2,045 commodity-month-currency cells had $<8$ reporting districts and were excluded to prevent reference median instability.
- **Extreme Outlier Winsorization:** The empirical raw ratio was winsorized at $[0.01, 0.99]$ to shield the model from border quote recording errors.
- **Operational Project Threshold:** $\text{price\_stress} = 1$ if $\text{SPI} > 1.25$, and $0$ otherwise.

## 4. Target Shifting Audit ($T \to T+1$)

- **Total Rows with Valid SPI at Month T:** 11,879
- **Rows with Valid Next Month in Series:** 10,712
- **Rows Dropped Due to Series Termination (No Next Month):** 1,167
- **Rows Dropped Due to Calendar Gap $> 1$ Month:** 2,423
- **Rows Retained with Verified Exact Calendar Lag ($T+1$):** 8,289
- **Rows Retained After Irregular Reporting Gap Filter ($\le 2$ Months):** 6,908
- **Positive Stress Class Count ($T+1$):** 1,136 (13.70% of 8,289; 14.2% of 6,908)
- **Negative Class Count ($T+1$):** 7,153 (86.30% of 8,289; 85.8% of 6,908)
- **Calendar Lag Range:** Exactly 1 calendar month ($\Delta m = 1$). No multi-month substitutions permitted.
- **Audit Outcome:** **PASSED** (Logged in `outputs/option_b/results/target_shift_audit.csv`)

## 5. Missing Data Treatment & Preprocessing Hygiene

1. **Market Lags:** Lags (`spi_lag_1`, `spi_lag_2`, `spi_pct_change_3m`) naturally create warm-up missingness at the beginning of each series. These are imputed using median imputation fitted **strictly inside each training fold**.
2. **Rainfall Gaps:** Matched on calendar month $T$. Any rare missing district rainfall is imputed via median imputation inside training folds.
3. **Zero Information Leakage:** Scalers (`StandardScaler`) and imputers (`SimpleImputer`) are instantiated inside scikit-learn `Pipeline` objects and fitted exclusively on outer training data.
