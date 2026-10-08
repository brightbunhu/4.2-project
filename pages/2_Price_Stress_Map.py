"""
pages/2_Price_Stress_Map.py - Option B Dashboard: Prediction Explorer & Spatial Map
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
from app.data_loader import load_option_b_predictions, load_geo

st.title("🗺️ Prediction Explorer & District Spatial Map")
st.caption("Predicting Relative Commodity-Price Stress for Target Month T+1 Using Information Available at Month T")

st.info(
    "⚠️ **Operational Notice:** The target month **T+1** is exactly one calendar month ahead of the prediction month **T**. "
    "All model predictors rely strictly on data available at or before month **T**.",
    icon="ℹ️"
)

df_preds = load_option_b_predictions()
if df_preds.empty:
    st.error("Option B prediction artifacts not found. Please run `python src/run_option_b_pipeline.py`.")
    st.stop()

tab_pred, tab_map = st.tabs(["🎯 Next-Month Prediction Query (T → T+1)", "🌍 ADM2 Spatial District Map"])

with tab_pred:
    st.markdown("### 🔍 Filter District–Commodity Unit")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        districts = sorted(df_preds["district_key"].unique())
        sel_district = st.selectbox("Select District (ADM2):", districts, index=0)
    with col2:
        commodities = sorted(df_preds["commodity_name"].unique())
        sel_comm = st.selectbox("Select Commodity:", commodities, index=0)
    with col3:
        currencies = sorted(df_preds["currency_code"].unique())
        sel_curr = st.selectbox("Select Currency:", currencies, index=0)

    # Filter available months for this selection
    sub_df = df_preds[
        (df_preds["district_key"] == sel_district) &
        (df_preds["commodity_name"] == sel_comm) &
        (df_preds["currency_code"] == sel_curr)
    ].sort_values("prediction_month")

    if sub_df.empty:
        st.warning("⚠️ **Prediction Unavailable:** No historical data coverage exists for this district-commodity-currency combination.")
    else:
        col4, col5 = st.columns(2)
        with col4:
            available_p_months = sub_df["prediction_month"].dt.strftime("%Y-%m").tolist()
            sel_p_month_str = st.selectbox("Select Prediction Month (T):", available_p_months, index=len(available_p_months)-1)
            sel_row = sub_df[sub_df["prediction_month"].dt.strftime("%Y-%m") == sel_p_month_str].iloc[0]
        with col5:
            model_choice = st.radio("Select Prediction Model:", ["XGBoost (Champion)", "Logistic Regression", "Dummy Baseline"], horizontal=True)

        target_month_str = sel_row["target_month"].strftime("%Y-%m")
        st.markdown("---")
        st.markdown(f"#### Results for **{sel_district}** — **{sel_comm}** ({sel_curr})")

        m_key = "xgb" if "XGBoost" in model_choice else ("logreg" if "Logistic" in model_choice else "dummy")
        pred_val = int(sel_row[f"{m_key}_pred"])
        proba_val = float(sel_row[f"{m_key}_proba"])

        c_res1, c_res2, c_res3, c_res4 = st.columns(4)
        with c_res1:
            st.metric("Prediction Month (T)", sel_p_month_str, "Available data cut-off")
        with c_res2:
            st.metric("Target Forecast Month (T+1)", target_month_str, "Evaluation window")
        with c_res3:
            status_text = "HIGH STRESS (SPI > 1.25)" if pred_val == 1 else "LOW / NORMAL STRESS"
            status_color = "red" if pred_val == 1 else "green"
            st.metric("Predicted Stress Class", status_text)
        with c_res4:
            st.metric("Predicted Stress Probability", f"{proba_val * 100:.1f}%")

        if pred_val == 1:
            st.error(f"🚨 **High Relative Price Stress Predicted for {target_month_str}**: The model projects a relative price spike exceeding 1.25 times the national median.")
        else:
            st.success(f"✅ **Normal Relative Price Projected for {target_month_str}**: The model predicts relative prices will remain within standard bounds.")

with tab_map:
    st.markdown("### 🗺️ Geographic Distribution of Next-Month Stress Predictions")
    
    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        map_comm = st.selectbox("Filter Map Commodity:", commodities, key="map_comm")
    with m_col2:
        all_p_months = sorted(df_preds["prediction_month"].dt.strftime("%Y-%m").unique())
        map_p_month = st.selectbox("Filter Map Prediction Month (T):", all_p_months, index=len(all_p_months)-1, key="map_month")
    with m_col3:
        map_mode = st.radio("Map Display Mode:", ["Predicted Probability (XGBoost)", "Predicted Stress Class (Binary)", "True Target Class (Validation)"], horizontal=True)

    map_slice = df_preds[
        (df_preds["commodity_name"] == map_comm) &
        (df_preds["prediction_month"].dt.strftime("%Y-%m") == map_p_month)
    ].copy()

    if map_slice.empty:
        st.warning(f"No district reporting coverage found for **{map_comm}** in prediction month **{map_p_month}**.")
    else:
        target_disp = map_slice["target_month"].iloc[0].strftime("%B %Y")
        st.markdown(f"**Map Target Horizon:** Forecast for **Month T+1 ({target_disp})** | Monitored Districts: **{len(map_slice)}**")

        if "Probability" in map_mode:
            fig = px.bar(
                map_slice.sort_values("xgb_proba", ascending=False),
                x="district_key", y="xgb_proba",
                labels={"district_key": "District", "xgb_proba": "Predicted Probability of Stress (T+1)"},
                color="xgb_proba", color_continuous_scale="Reds",
                title=f"Predicted Probability of Stress by District for {map_comm} ({target_disp})"
            )
            fig.update_layout(xaxis_tickangle=-45, yaxis_range=[0, 1])
            st.plotly_chart(fig, use_container_width=True)
        else:
            col_target = "xgb_pred" if "Predicted" in map_mode else "target_next_month"
            label_text = "Predicted Class (T+1)" if "Predicted" in map_mode else "Observed Class (T+1)"
            map_slice["Display_Class"] = np.where(map_slice[col_target] == 1, "High Stress (SPI > 1.25)", "Normal / Low Stress")
            fig = px.bar(
                map_slice.sort_values("district_key"),
                x="district_key", y=col_target,
                color="Display_Class",
                color_discrete_map={"High Stress (SPI > 1.25)": "#d62728", "Normal / Low Stress": "#2ca02c"},
                labels={"district_key": "District", col_target: label_text},
                title=f"{label_text} for {map_comm} in Month T+1 ({target_disp})"
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
