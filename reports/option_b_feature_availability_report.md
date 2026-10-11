# Option B Feature Availability & Leakage Audit Report

## 1. Information Horizon Policy

Every predictor variable in the Option B modelling table is governed by the strict temporal availability constraint:
$$\text{feature\_information\_date} \le \text{prediction\_month } T$$

## 2. Complete Whitelist Inventory & Verification

The feature set comprises exactly 23 predictors, audited in `outputs/option_b/results/feature_availability_audit.csv`:

| Feature Name | Source Domain | Temporal Scope | Verification Status |
|---|---|---|---|
| `spi_lag_1` | Market Price Series | Observed at $T-1$ | **PASSED (No Leakage)** |
| `spi_lag_2` | Market Price Series | Observed at $T-2$ | **PASSED (No Leakage)** |
| `spi_pct_change_3m` | Market Price Series | Rolling window $[T-3, T]$ | **PASSED (No Leakage)** |
| `months_since_last_reported_price` | Market Price Series | Interval leading up to $T$ | **PASSED (No Leakage)** |
| `rainfall_1m` | CHIRPS Gridded Rainfall | Precipitation in calendar month $T$ | **PASSED (No Leakage)** |
| `rainfall_3m_total` | CHIRPS Gridded Rainfall | Cumulative $[T-2, T]$ | **PASSED (No Leakage)** |
| `rainfall_6m_total` | CHIRPS Gridded Rainfall | Cumulative $[T-5, T]$ | **PASSED (No Leakage)** |
| `rainfall_12m_total` | CHIRPS Gridded Rainfall | Cumulative $[T-11, T]$ | **PASSED (No Leakage)** |
| `rainfall_3m_anomaly` | CHIRPS Gridded Rainfall | Climatological anomaly ending at $T$ | **PASSED (No Leakage)** |
| `log_population` | UNFPA Baseline | Static district demographic baseline | **PASSED (No Leakage)** |
| `is_urban` | Administrative Hierarchy | Static classification | **PASSED (No Leakage)** |
| `month_of_year` | Calendar Timestamp | Calendar month of prediction date $T$ | **PASSED (No Leakage)** |
| `year` | Calendar Timestamp | Observation year of date $T$ | **PASSED (No Leakage)** |
| 10 $\times$ `commodity_*` | Market Category | One-hot commodity identity at $T$ | **PASSED (No Leakage)** |

## 3. Forbidden Predictor Audit

The automated pipeline asserted and confirmed that:
- $\text{Price}(T+1)$ is **absent**.
- $\text{SPI}(T+1)$ is **absent**.
- $\text{price\_stress}(T+1)$ is **absent**.
- Contemporaneous raw $\text{Price}(T)$ and unadjusted $\text{SPI}(T)$ are **absent** from predictor vectors to prevent proxy leakage.
