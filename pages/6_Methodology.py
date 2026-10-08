"""
pages/6_Methodology.py - Option B Dashboard: Formal Methodology
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st

st.title("📚 Methodology & Algorithmic Design (Option B)")
st.caption("Formal scientific framework, mathematical formulations, and leakage prevention rules.")

st.markdown("""
### 1. Unit of Analysis
The fundamental observational unit throughout data preparation, modeling, and dashboard display is:
$$\\text{district\\_key} \\times \\text{commodity\\_name} \\times \\text{prediction\\_month } T \\times \\text{currency\\_code}$$

### 2. Spatial Price Index (SPI)
For district $i$, commodity $c$, month $t$, and currency $u$:
$$\\text{SPI}(i,c,t,u) = \\frac{\\text{Price}(i,c,t,u)}{\\text{Median}_{j \\in \\mathcal{D}(c,t,u)}(\\text{Price}(j,c,t,u))}$$
where $\\mathcal{D}(c,t,u)$ includes eligible reporting districts under a strict **thin-cell guard** ($|\\mathcal{D}| \\ge 8$ reporting districts).
Raw ratios are winsorized at $[0.01, 0.99]$ to suppress quote reporting artifacts.

### 3. Operational Stress Threshold (1.25)
A binary relative stress indicator is computed as:
$$\\text{price\\_stress} = \\begin{cases} 1 & \\text{if } \\text{SPI} > 1.25 \\\\ 0 & \\text{if } \\text{SPI} \\le 1.25 \\end{cases}$$
> *Note:* The 1.25 threshold represents a relative market deviation benchmark (prices $>25\\%$ above the national median for the same commodity and currency), not an absolute measure of inflation or household poverty.

### 4. Option B Shifted Target ($T \\to T+1$)
The target variable is strictly shifted by **exactly one calendar month**:
$$\\text{target\\_next\\_month}(T) = \\text{price\\_stress}(T+1)$$
$$\\text{Condition: } \\text{target\\_month} = \\text{prediction\\_month} + 1 \\text{ calendar month}$$
Observations lacking an immediate following month or with reporting gaps $>1$ month are audited and dropped.

### 5. Information Availability & Forbidden Predictors
Every predictor variable must strictly satisfy:
$$\\text{feature\\_information\\_date} \\le \\text{prediction\\_month } T$$

**Forbidden Predictors (Strict Zero-Leakage Policy):**
- Target-month price at $T+1$ (Forbidden)
- Target-month SPI at $T+1$ (Forbidden)
- Target-month price stress at $T+1$ (Forbidden)
- Future rainfall or rolling aggregations ending after month $T$ (Forbidden)
- Full-dataset scaling, imputation, or hyperparameter fitting (Forbidden)

### 6. Validation Protocol: Expanding Forward-Chaining
Validation uses 3 expanding temporal folds:
- Models are trained on earlier calendar months and evaluated on strictly later calendar months.
- All imputers (`SimpleImputer`) and scalers (`StandardScaler`) are fitted strictly inside outer training folds.

### 7. Meaning of Predicted Probabilities
The predicted probability $P(\\text{stress}=1 \\mid \\mathbf{X}_T)$ represents the model's estimated likelihood that a district's relative commodity price in month $T+1$ will exceed the national median by more than 25%, given observed market history and rainfall up to month $T$.
""")
