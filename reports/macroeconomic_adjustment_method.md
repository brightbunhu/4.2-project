# Macroeconomic and Currency Adjustment Method

## 1. Overview and Rationale

The Zimbabwe Commodity Price Stress Classifier (ZCPSC) analyzes commodity prices across Zimbabwe from 2017 to 2026. During this decade, Zimbabwe experienced extreme macroeconomic instability, hyperinflation, multiple currency transitions (ZWL, USD, ZWG), and redenomination events (most notably the April 2024 transition to Zimbabwe Gold / ZWG).

To prevent inflation spikes and currency currency fluctuations from distorting spatial price stress classification, the project implements a rigorous currency isolation and Spatial Price Index (SPI) methodology.

## 2. Macroeconomic Safeguards Implemented

### 2.1 Currency-Isolated Reference Groups
Rather than attempting to convert volatile local currency quotes into USD using unreliable or unverified parallel market exchange rates, raw prices are grouped strictly within their reported currency code:

$$\text{SPI}(i, c, m, u) = \frac{\text{Price}(i, c, m, u)}{\text{Median}(\text{Price}(j, c, m, u))}$$

where:
- $i$ = target district
- $c$ = commodity
- $m$ = calendar month
- $u$ = currency (`USD` or `ZWL`)
- $j$ = reporting districts for the same commodity, month, and currency

By taking the ratio of local district price against the national median for the **same commodity, same month, and same currency**, hyperinflation and general price level changes in both numerator and denominator cancel out exactly. This extracts pure relative spatial price elevation.

### 2.2 Redenomination & Currency Shock Treatment (April 2024)
In April 2024, the Zimbabwean authorities redenominated the ZWL and introduced the ZWG (Zimbabwe Gold). Price quotations collected during April 2024 in ZWL are unstable due to currency transition turbulence. All ZWL observations during April 2024 are audited and excluded from model training.

### 2.3 Unresolved Limitations
No complete, verified monthly Consumer Price Index (CPI) or official/parallel exchange rate time series covering all 73 districts continuously from 2017 to 2026 was available in the raw data files. Converting all prices to a single real currency baseline using an unverified rate would introduce synthetic error. Therefore, currency isolation remains the primary methodological safeguard.
