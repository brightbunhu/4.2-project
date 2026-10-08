"""
pages/3_District_Commodity_Detail.py - Option B Dashboard: Commodity and District Analysis
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from app.data_loader import load_option_b_predictions, load_option_b_modelling_table

st.title("📊 Commodity & District Comparative Analytics")
st.caption("Deep-dive comparative analysis across Zimbabwean districts and food commodities.")

df_preds = load_option_b_predictions()
df_mod = load_option_b_modelling_table()

if df_preds.empty or df_mod.empty:
    st.error("Option B data not loaded.")
    st.stop()

st.markdown("""
> **Time Horizon Labeling Note:** Charts below clearly distinguish between **Historical Observed SPI (Month T and prior)** 
> and **Predicted Forward Stress Probability (Month T+1)**.
""")

col1, col2 = st.columns(2)
with col1:
    districts = sorted(df_preds["district_key"].unique())
    sel_district = st.selectbox("Select District:", districts, index=0)
with col2:
    commodities = sorted(df_preds["commodity_name"].unique())
    sel_comm = st.selectbox("Select Commodity:", commodities, index=0)

# Historical Trajectory up to Month T
sub_hist = df_mod[
    (df_mod["district_key"] == sel_district) &
    (df_mod["commodity_name"] == sel_comm)
].sort_values("prediction_month")

sub_preds = df_preds[
    (df_preds["district_key"] == sel_district) &
    (df_preds["commodity_name"] == sel_comm)
].sort_values("prediction_month")

st.markdown(f"### 📈 Historical Price Index (SPI) up to Month T for {sel_district} — {sel_comm}")
if sub_hist.empty:
    st.info(f"No continuous series found for {sel_district} and {sel_comm}.")
else:
    fig_hist = px.line(
        sub_hist, x="prediction_month", y="spi_lag_1",
        labels={"prediction_month": "Information Month T", "spi_lag_1": "Spatial Price Index (Lag 1 / Historical)"},
        title=f"Historical Observed Relative Price Index (SPI) Leading to Month T ({sel_district} - {sel_comm})",
        markers=True
    )
    fig_hist.add_hline(y=1.25, line_dash="dash", line_color="red", annotation_text="Stress Threshold (SPI = 1.25)")
    st.plotly_chart(fig_hist, use_container_width=True)

st.markdown(f"### 🔮 Forecasted Next-Month Stress Probability (Month T+1) Over Time")
if not sub_preds.empty:
    fig_pred = px.line(
        sub_preds, x="target_month", y="xgb_proba",
        labels={"target_month": "Target Forecast Month T+1", "xgb_proba": "Predicted Stress Probability (XGBoost)"},
        title=f"Option B Predicted Probability of Stress in Month T+1 ({sel_district} - {sel_comm})",
        markers=True, color_discrete_sequence=["#d62728"]
    )
    fig_pred.add_hline(y=0.5, line_dash="dash", line_color="gray", annotation_text="Classification Cutoff (0.50)")
    fig_pred.update_layout(yaxis_range=[0, 1])
    st.plotly_chart(fig_pred, use_container_width=True)

st.markdown("---")
st.markdown("### 🌐 Cross-Commodity & Cross-District Rankings")
col_c1, col_c2 = st.columns(2)

with col_c1:
    comm_stress = df_preds.groupby("commodity_name")["xgb_proba"].mean().reset_index().sort_values("xgb_proba", ascending=False)
    fig_comm = px.bar(
        comm_stress, x="xgb_proba", y="commodity_name", orientation="h",
        labels={"xgb_proba": "Mean Predicted Stress Probability (T+1)", "commodity_name": "Commodity"},
        title="Average Forecasted Stress Risk by Commodity",
        color="xgb_proba", color_continuous_scale="Reds"
    )
    st.plotly_chart(fig_comm, use_container_width=True)

with col_c2:
    dist_stress = df_preds.groupby("district_key")["xgb_proba"].mean().reset_index().sort_values("xgb_proba", ascending=False).head(15)
    fig_dist = px.bar(
        dist_stress, x="xgb_proba", y="district_key", orientation="h",
        labels={"xgb_proba": "Mean Predicted Stress Probability (T+1)", "district_key": "District"},
        title="Top 15 Districts by Average Predicted Stress Risk",
        color="xgb_proba", color_continuous_scale="Reds"
    )
    st.plotly_chart(fig_dist, use_container_width=True)
