"""
pages/7_About_Limitations.py - Option B Dashboard: Data Quality & Limitations
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
from app.data_loader import (
    load_option_b_predictions, load_option_b_target_audit,
    load_option_b_validation_audit
)

st.title("ℹ️ Data Quality, Limitations & Responsible Use")
st.caption("Coverage audits, known empirical constraints, and ethical decision-support guidance.")

# Mandatory Disclaimer
st.warning(
    "**Mandatory Disclaimer:** This dashboard provides model-based predictions of next-month relative commodity-price stress. "
    "It is an academic decision-support prototype. It does not constitute an official food-security assessment, an IPC classification "
    "or a guaranteed forecast. Predictions should be interpreted alongside official data, expert judgement and wider food-security evidence.",
    icon="⚠️"
)

st.markdown("""
### 📋 System Scope & Non-Claims
The **Zimbabwe Commodity Price Stress Classifier (Option B)** is strictly bounded by the following non-claims:
1. **Not Household Food Insecurity:** The system predicts relative commodity price deviations, not caloric intake or biological malnutrition.
2. **Not IPC Phases:** The system does not classify Integrated Food Security Phase Classification (IPC) phases.
3. **Not Causal Models:** TreeSHAP attributions and regression weights reflect empirical predictive associations, not agronomic causality.
4. **Not Guaranteed Forecasts:** Predictions represent probabilistic estimates under historical distributions and cannot account for unforeseen policy or geopolitical shocks.
5. **Not an Official Replacement:** This tool does not replace ZimVAC, WFP VAM, or Government of Zimbabwe official surveys.
""")

st.markdown("---")
st.markdown("### 📊 Empirical Coverage Metrics")

df_preds = load_option_b_predictions()
df_target_audit = load_option_b_target_audit()
df_val_audit = load_option_b_validation_audit()

if not df_preds.empty:
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Date Span", "2017 – 2024", "57 monthly periods")
    with c2:
        st.metric("Districts", f"{df_preds['district_key'].nunique()}", "Active reporting districts")
    with c3:
        st.metric("Commodities", f"{df_preds['commodity_name'].nunique()}", "Monitored food items")
    with c4:
        st.metric("Currencies", "USD & ZWL", "Isolated within medians")

if not df_target_audit.empty:
    st.markdown("#### 🎯 Target Shifting & Calendar Continuity Audit")
    st.dataframe(df_target_audit, use_container_width=True)

if not df_val_audit.empty:
    st.markdown("#### ⏳ Temporal Cross-Validation Audit")
    st.dataframe(df_val_audit, use_container_width=True)
