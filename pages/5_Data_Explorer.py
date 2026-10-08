"""
pages/5_Data_Explorer.py - Option B Dashboard: Interactive Data Explorer
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
from app.data_loader import load_option_b_predictions, load_option_b_modelling_table

st.title("🗂️ Option B Data & Predictions Explorer")
st.caption("Inspect and download the unified Option B modelling table and out-of-sample predictions.")

df_preds = load_option_b_predictions()
df_mod = load_option_b_modelling_table()

if df_preds.empty or df_mod.empty:
    st.error("Option B data not loaded.")
    st.stop()

dataset_choice = st.radio("Choose Dataset to Inspect:", ["Unified Predictions Table (T -> T+1)", "Full Modelling Table (Features at T)"], horizontal=True)

df_target = df_preds if "Predictions" in dataset_choice else df_mod

# Interactive filters
col1, col2, col3 = st.columns(3)
with col1:
    dist_filter = st.multiselect("Filter District:", sorted(df_target["district_key"].unique()))
with col2:
    comm_filter = st.multiselect("Filter Commodity:", sorted(df_target["commodity_name"].unique()))
with col3:
    stress_filter = st.multiselect("Filter Target Stress (T+1):", [0, 1], format_func=lambda x: "Stress (1)" if x == 1 else "No Stress (0)")

filtered = df_target.copy()
if dist_filter:
    filtered = filtered[filtered["district_key"].isin(dist_filter)]
if comm_filter:
    filtered = filtered[filtered["commodity_name"].isin(comm_filter)]
if stress_filter:
    filtered = filtered[filtered["target_next_month"].isin(stress_filter)]

st.markdown(f"**Showing {len(filtered):,} of {len(df_target):,} rows**")
st.dataframe(filtered.head(1000), use_container_width=True)

# CSV Download
csv_data = filtered.to_csv(index=False).encode('utf-8')
st.download_button(
    "📥 Download Filtered Data as CSV",
    csv_data,
    "option_b_filtered_data.csv",
    "text/csv"
)
