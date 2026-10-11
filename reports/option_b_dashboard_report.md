# Option B Dashboard Architecture & Features Report

## 1. System Overview

The Streamlit dashboard serves as the operational prototype for the Zimbabwe Commodity Price Stress Classifier (ZCPSC). It adheres strictly to the predictive horizon:
$$\text{Information at Month } T \longrightarrow \text{Stress at Month } T+1$$

## 2. Page Hierarchy & Functional Capabilities

The application consists of 8 core pages organized in `pages/`:

1. **`1_Home.py` (Project Identity & Headline Overview):**
   - High-level KPIs: 6,908 observations, 79 monitored districts, 16 commodities, 14.2% target stress prevalence.
   - Model performance summary table comparing Dummy, Logistic Regression, and XGBoost.
   - Mandatory responsible-use disclaimer banner.
2. **`2_Next_Month_Prediction.py` (Dedicated Interactive Prediction Page):**
   - *Mode A: Single Observation Prediction:* Select District, Commodity, Currency, and Month $T$. Derives historical lags and rainfall automatically. Computes predicted class, probability, and per-observation TreeSHAP explanation.
   - *Mode B: CSV Batch Prediction:* Upload multi-row CSV, validate row-by-row, download validation error logs, and generate downloadable predictions CSV.
   - Official template download button (`option_b_prediction_template.csv`).
3. **`3_Price_Stress_Map.py` (ADM2 Geographic Choropleth):**
   - District-level spatial distribution of predicted stress probabilities and classes across Zimbabwe for Month $T+1$.
4. **`4_District_Commodity_Detail.py` (Comparative Time Series):**
   - Plots historical observed SPI leading up to Month $T$ alongside forecasted stress probability for Month $T+1$.
5. **`5_Model_Insights.py` (Evaluation & TreeSHAP Explanations):**
   - Out-of-sample forward-chaining ROC/PR curves, confusion matrices, calibration plots, global SHAP importance rankings, and summary beeswarm plot.
6. **`6_Data_Explorer.py` (Interactive Table Browser):**
   - Filterable data browser with column selection and CSV download.
7. **`7_Methodology.py` (Mathematical & Operational Framework):**
   - Detailed formulations of SPI, the 1.25 threshold, target shifting logic, and forbidden future variables.
8. **`8_About_Limitations.py` (Ethical Guidance & Non-Claims):**
   - Explicit non-claims (not IPC, not household food insecurity, not causal rainfall model).
