"""
app.py - Streamlit multipage entry point for the ZCPSC Option B dashboard.

Launch: streamlit run app.py
The pages/ directory contains the seven full dashboard pages.
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
from app.data_loader import (
    load_option_b_predictions, load_option_b_metrics
)

st.set_page_config(
    page_title="Zimbabwe Commodity Price Stress Classifier (ZCPSC)",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.sidebar.title("🌾 ZCPSC Dashboard (Option B)")
st.sidebar.caption("Prediction Horizon: Month T → Month T+1")
st.sidebar.markdown("---")
st.sidebar.markdown(
    "**System Purpose:**\n"
    "The Zimbabwe Commodity Price Stress Classifier is an academic decision-support prototype "
    "that uses information available by month T to estimate the probability of relative commodity-price "
    "stress in month T+1 across Zimbabwean districts."
)
st.sidebar.markdown("---")
st.sidebar.info("Use the sidebar pages to navigate through predictions, maps, and model insights.")

# Title & Description
st.title("🌾 Zimbabwe Commodity Price Stress Classifier (ZCPSC)")
st.subheader("Machine Learning-Based Prediction of Next-Month Relative Commodity Price Stress in Zimbabwean Districts")

st.markdown("""
> **System Description:**
> The Zimbabwe Commodity Price Stress Classifier is an academic decision-support prototype that uses information 
> available by month T to estimate the probability of relative commodity-price stress in month T+1 across Zimbabwean districts.
""")

# Mandatory Responsible-Use Disclaimer
st.warning(
    "**Mandatory Disclaimer:** This dashboard provides model-based predictions of next-month relative commodity-price stress. "
    "It is an academic decision-support prototype. It does not constitute an official food-security assessment, an IPC classification "
    "or a guaranteed forecast. Predictions should be interpreted alongside official data, expert judgement and wider food-security evidence.",
    icon="⚠️"
)

# Load Key Option B Summary Data
df_preds = load_option_b_predictions()
df_metrics = load_option_b_metrics()

if not df_preds.empty:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Modelling Observations", f"{len(df_preds):,}", "district x commodity x month")
    with col2:
        st.metric("Prediction Horizon", "Month T → T+1", "One calendar month ahead")
    with col3:
        st.metric("Stress Rate (T+1)", f"{df_preds['target_next_month'].mean() * 100:.1f}%", "SPI > 1.25 in month T+1")
    with col4:
        st.metric("Champion Model", "XGBoost", "Macro-F1 = 0.6200 | ROC-AUC = 0.7706")

st.markdown("---")
st.markdown("""
### 🧭 Navigation Guide (7 Core Pages)
1. **Home / Overview:** Project identity, data provenance, and headline KPIs.
2. **Prediction Explorer & Spatial Map:** Search any district-commodity series to view predicted probability and class for month T+1.
3. **Commodity & District Detail:** Compare historical observed SPI up to month T against forecasted risk in month T+1.
4. **Model Insights & TreeSHAP:** Out-of-sample forward-chaining metrics, ROC/PR curves, and global & local TreeSHAP attributions.
5. **Data Explorer:** Filter and download the full modelling table and prediction tables.
6. **Methodology:** Mathematical formulation of SPI, 1.25 threshold, target shifting logic, and leakage controls.
7. **About & Limitations:** Explicit system exclusions, responsible use guidelines, and data coverage audits.
""")
