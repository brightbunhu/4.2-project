# Option B Target Shift Audit Report

## 1. Overview & Mathematical Definition

Under Option B, the target variable represents the relative commodity-price stress state in the **following calendar month**:
$$\text{target\_next\_month}(T) = \text{price\_stress}(T+1)$$
$$\text{Condition: } \text{target\_month} = \text{prediction\_month} + 1 \text{ calendar month}$$

Where current-month price stress is defined by the operational project benchmark:
$$\text{price\_stress}(t) = \mathbb{I}(\text{SPI}(t) > 1.25)$$

## 2. Empirical Target Shift Verification Metrics

The following metrics are extracted directly from the verified execution record (`outputs/option_b/results/target_shift_audit.csv`):

- **Total Series Analyzed:** 1,167 district–commodity–currency series
- **Observations with Valid SPI at Month T:** 11,879
- **Observations with Valid Next Observation in Series:** 10,712
- **Observations Dropped Due to Series Termination (No Next Month):** 1,167
- **Observations Dropped Due to Multi-Month Calendar Gap ($\Delta m > 1$):** 2,423
- **Observations Retained with Exact Calendar Lag ($\Delta m = 1$):** 8,289
- **Observations Retained Following Reporting Gap Filter ($\le 2$ Months):** 6,908
- **Positive Stress Observations ($T+1$):** 1,136 (13.70% of 8,289; 14.2% of 6,908)
- **Negative Observations ($T+1$):** 7,153 (86.30% of 8,289; 85.8% of 6,908)
- **Minimum Calendar Lag:** Exactly 1 calendar month
- **Maximum Calendar Lag:** Exactly 1 calendar month
- **Duplicate Natural Keys:** 0 (Verified in `outputs/option_b/results/natural_key_audit.csv`)

## 3. Strict Absence of Multi-Month Substitutions

The audit strictly enforced that if an observation in month $T$ was followed by a quote in month $T+2$ or $T+3$ rather than $T+1$, that observation was **excluded from modeling**. No synthetic multi-month substitutions were permitted.
