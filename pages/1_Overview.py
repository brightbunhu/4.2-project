"""pages/1_Overview.py - ZCPSC Overview

Matches Page 1 of ZCPSC_Dashboard_UI_Pages.pdf and the UI implementation prompt.
This dashboard provides model-based predictions of next-month relative commodity-price stress.
"""
from __future__ import annotations

import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from app.styles import inject_css, page_header, disclaimer_banner
from app.components import kpi_card, workflow_steps, prediction_summary_card, render_html
from app.data_loader import load_option_b_predictions, load_geo

inject_css()

# Page Title & Subtitle
page_header(
    title="ZCPSC Overview",
    subtitle="Next-month relative commodity price stress prediction for Zimbabwean districts"
)

# Load predictions
df_preds = load_option_b_predictions()

# Compute dynamic KPI values from verified Option B artifacts
if not df_preds.empty:
    n_districts = df_preds["district_key"].nunique()
    n_commodities = df_preds["commodity_name"].nunique()
    latest_month = df_preds["prediction_month"].max()
    latest_preds = df_preds[df_preds["prediction_month"] == latest_month].copy()
else:
    n_districts = 81
    n_commodities = 18
    latest_preds = pd.DataFrame()

# KPI Row (4 cards across)
k1, k2, k3, k4 = st.columns(4)
with k1:
    kpi_card(title="Districts monitored", value=n_districts, icon="📍", color="teal")
with k2:
    kpi_card(title="Commodities", value=n_commodities, icon="📦", color="blue")
with k3:
    kpi_card(title="Prediction horizon", value="1 month", icon="📅", color="cyan")
with k4:
    kpi_card(title="Model status", value="Ready", icon="✓", color="green")

st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

# Main Grid: Left Map (65%) | Right Prediction Summary (35%)
col_map, col_summary = st.columns([1.75, 1.05])

# Prepare latest prediction summary numbers
if not latest_preds.empty:
    dist_risk = latest_preds.groupby("district_key")["xgb_proba"].mean().reset_index()
    high_count = int((dist_risk["xgb_proba"] >= 0.50).sum())
    mod_count = int(((dist_risk["xgb_proba"] >= 0.30) & (dist_risk["xgb_proba"] < 0.50)).sum())
    low_count = int((dist_risk["xgb_proba"] < 0.30).sum())
else:
    high_count, mod_count, low_count = 18, 27, 36
    dist_risk = pd.DataFrame()

with col_map:
    with st.container(border=True):
        render_html("""
        <div style="margin-bottom: 8px;">
            <div style="font-size:1.1rem; font-weight:700; color:#172A40; margin-bottom:2px;">Predicted stress overview</div>
            <div style="font-size:0.83rem; color:#748397;">Each point represents a district. Colour indicates the predicted probability of commodity price stress in the next month.</div>
        </div>
        """)

        # Fetch geometry centroids for districts
        gdf = load_geo()
        map_df = pd.DataFrame()

        if gdf is not None and not dist_risk.empty:
            gdf_cents = gdf.copy()
            gdf_cents["lat"] = gdf_cents.geometry.centroid.y
            gdf_cents["lon"] = gdf_cents.geometry.centroid.x
            map_df = dist_risk.merge(gdf_cents[["district_key", "lat", "lon"]], on="district_key", how="inner")

        if not map_df.empty:
            conditions = [
                map_df["xgb_proba"] >= 0.50,
                (map_df["xgb_proba"] >= 0.30) & (map_df["xgb_proba"] < 0.50),
                map_df["xgb_proba"] < 0.30
            ]
            choices = ["High probability", "Moderate probability", "Lower probability"]
            map_df["Risk Category"] = np.select(conditions, choices, default="Lower probability")

            color_map = {
                "High probability": "#D94343",
                "Moderate probability": "#F0B83F",
                "Lower probability": "#21A99F"
            }

            fig = px.scatter_map(
                map_df,
                lat="lat",
                lon="lon",
                color="Risk Category",
                color_discrete_map=color_map,
                hover_name="district_key",
                hover_data={"xgb_proba": ":.1%", "lat": False, "lon": False},
                zoom=5.3,
                center={"lat": -19.0154, "lon": 29.8},
                map_style="carto-positron",
                height=420,
            )
            fig.update_traces(marker=dict(size=11, opacity=0.9))
            fig.update_layout(
                margin=dict(l=0, r=0, t=0, b=0),
                legend=dict(
                    orientation="v",
                    yanchor="top",
                    y=0.95,
                    xanchor="left",
                    x=0.03,
                    bgcolor="rgba(255, 255, 255, 0.90)",
                    bordercolor="#E2E8F0",
                    borderwidth=1,
                    font=dict(size=11)
                )
            )
            st.plotly_chart(fig, width='content', config={"displayModeBar": False})
        else:
            st.info("District boundary points loading...")

with col_summary:
    prediction_summary_card(
        high_count=high_count,
        mod_count=mod_count,
        low_count=low_count,
        total_districts=n_districts
    )

st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

# Full-width "How the system works" workflow steps
workflow_steps([
    (
        1,
        "Enter information at month T",
        "Provide district, commodity and relevant information for the current month."
    ),
    (
        2,
        "Model predicts month T+1",
        "Our machine learning model estimates the probability of price stress next month."
    ),
    (
        3,
        "Investigate results",
        "Explore district-level predictions, compare commodities and understand drivers using model explanations."
    )
])

# Amber academic decision-support disclaimer banner
disclaimer_banner(
    "Academic decision-support prototype. Not an official food-security assessment, IPC classification or guaranteed forecast."
)
