"""
pages/1_Home.py - Option B Dashboard: Project Overview & System Identity
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
from app.data_loader import (
    load_option_b_predictions, load_option_b_metrics,
    load_option_b_modelling_table, load_option_b_target_audit
)

st.title("🌾 Zimbabwe Commodity Price Stress Classifier (ZCPSC)")
st.subheader("Machine Learning-Based Prediction of Next-Month Relative Commodity Price Stress in Zimbabwean Districts")

# Mandatory Responsible-Use Disclaimer
st.warning(
    "**Mandatory Disclaimer:** This dashboard provides model-based predictions of next-month relative commodity-price stress. "
    "It is an academic decision-support prototype. It does not constitute an official food-security assessment, an IPC classification "
    "or a guaranteed forecast. Predictions should be interpreted alongside official data, expert judgement and wider food-security evidence.",
    icon="⚠️"
)

st.markdown("""
### 📌 System Purpose & Horizon Definition
The **Zimbabwe Commodity Price Stress Classifier** is an academic decision-support prototype that uses information available 
by **month T** to estimate the probability of relative commodity-price stress in **month T+1** across Zimbabwean districts.

$$\\text{Information Available at Month } T \\longrightarrow \\text{Relative Price Stress at Month } T+1$$
""")

# Load Option B Artifacts
df_preds = load_option_b_predictions()
df_metrics = load_option_b_metrics()
df_table = load_option_b_modelling_table()

if not df_preds.empty:
    total_obs = len(df_preds)
    districts = df_preds["district_key"].nunique()
    commodities = df_preds["commodity_name"].nunique()
    stress_rate = df_preds["target_next_month"].mean() * 100
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Observations", f"{total_obs:,}", "district x commodity x month")
    with col2:
        st.metric("Districts Monitored", f"{districts}", "ADM2 coverage")
    with col3:
        st.metric("Commodities Analyzed", f"{commodities}", "Food basket series")
    with col4:
        st.metric("Target Stress Rate (T+1)", f"{stress_rate:.1f}%", "SPI > 1.25 in month T+1")

st.markdown("---")
col_l, col_r = st.columns([1.2, 1])

with col_l:
    st.markdown("### 📊 Model Architecture & Baseline Comparison")
    st.markdown("""
    The system compares three models evaluated under **forward temporal cross-validation**:
    1. **Dummy Baseline:** Majority-class baseline predictor.
    2. **Logistic Regression:** Interpretable linear model with L2 regularization and balanced weights.
    3. **XGBoost Classifier:** Nonlinear gradient-boosted tree ensemble (Champion Model).
    """)
    if not df_metrics.empty:
        summary_m = df_metrics.groupby("model")[["macro_f1", "balanced_accuracy", "roc_auc", "brier_score"]].mean().reset_index()
        summary_m.columns = ["Model", "Macro-F1", "Balanced Acc", "ROC-AUC", "Brier Score"]
        st.dataframe(summary_m.style.highlight_max(subset=["Macro-F1", "ROC-AUC"], color="#d4edda")
                                     .highlight_min(subset=["Brier Score"], color="#d4edda")
                                     .format({"Macro-F1": "{:.4f}", "Balanced Acc": "{:.4f}", "ROC-AUC": "{:.4f}", "Brier Score": "{:.4f}"}),
                     use_container_width=True)

with col_r:
    st.markdown("### 🛰️ Data Integration & Provenance")
    st.markdown("""
    - **WFP Market Prices (HDX HAPI):** 25,554 market quotes aggregated to median district-month-commodity cells.
    - **CHIRPS v3 Gridded Rainfall:** 0.05° gridded satellite precipitation up to prediction month $T$.
    - **UNFPA Population Baseline:** District-level log population and urban/rural classification.
    - **geoBoundaries ADM2:** Official administrative boundaries for Zimbabwean districts.
    """)
    st.info("💡 **Temporal Integrity:** Predictor information date is strictly $\\le T$. Target price, SPI, and stress at month $T+1$ are strictly forbidden from predictors.")
