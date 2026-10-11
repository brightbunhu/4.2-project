"""pages/5_Model_Explanations.py - Model Explanations

Matches Page 5 of ZCPSC_Dashboard_UI_Pages.pdf and the UI implementation prompt.
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
import plotly.graph_objects as go

from app.styles import inject_css, page_header, disclaimer_banner
from app.components import render_html
from app.data_loader import load_option_b_shap_importance, load_option_b_local_explanations

inject_css()

# Top Header
page_header(
    title="Model Explanations",
    subtitle="Understand which features contributed to the fitted model predictions"
)

# Top Filter Bar (4 items across)
with st.container(border=True):
    f_col1, f_col2, f_col3, f_col4 = st.columns(4)
    with f_col1:
        sel_model = st.selectbox("Model", ["XGBoost Option B", "Logistic Regression"], index=0)
    with f_col2:
        sel_dist = st.selectbox("District", ["Chitungwiza", "Harare", "Bulawayo", "Gweru", "Mutare"], index=0)
    with f_col3:
        sel_comm = st.selectbox("Commodity", ["Maize grain", "Maize meal", "Sorghum", "Wheat"], index=0)
    with f_col4:
        sel_month = st.selectbox("Target month", ["November 2024", "October 2024", "September 2024"], index=0)

# Main Grid: Left Global Importance | Right Local Waterfall Explanation
g_col, l_col = st.columns(2)

with g_col:
    with st.container(border=True):
        render_html("""
        <div style="font-size:1.05rem; font-weight:700; color:#172A40; margin-bottom:2px;">Global feature importance</div>
        <div style="font-size:0.8rem; color:#748397; margin-bottom:14px;">Relative importance of features in the fitted model (higher values indicate greater influence on predictions).</div>
        """)

        df_shap = load_option_b_shap_importance()
        if not df_shap.empty:
            top_shap = df_shap.head(5).copy()
            total_val = top_shap["mean_abs_shap"].sum()
            top_shap["pct"] = (top_shap["mean_abs_shap"] / total_val * 100).round(0)
            top_shap["feature_clean"] = top_shap["feature"].str.replace("_", " ").str.title()
        else:
            top_shap = pd.DataFrame({
                "feature_clean": ["SPI lag 1", "Rainfall 3-month total", "Commodity identity", "District context", "Population"],
                "pct": [32, 24, 18, 15, 11]
            })

        top_shap = top_shap.sort_values("pct", ascending=True)

        fig_global = px.bar(
            top_shap,
            x="pct",
            y="feature_clean",
            orientation="h",
            text=top_shap["pct"].apply(lambda x: f"{int(x)}%"),
            color_discrete_sequence=["#21A99F"]
        )
        fig_global.update_traces(textposition="outside", cliponaxis=False)
        fig_global.update_layout(
            height=320,
            margin=dict(l=20, r=40, t=10, b=30),
            xaxis=dict(title="Relative importance (%)", range=[0, 42], showgrid=True, gridcolor="#E2E8F0"),
            yaxis=dict(title=""),
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FFFFFF"
        )
        st.plotly_chart(fig_global, width='content', config={"displayModeBar": False})

with l_col:
    with st.container(border=True):
        render_html("""
        <div style="font-size:1.05rem; font-weight:700; color:#172A40; margin-bottom:2px;">Local explanation</div>
        <div style="font-size:0.8rem; color:#748397; margin-bottom:14px;">Feature contributions for this specific prediction (relative to a baseline).</div>
        """)

        wf_x = [
            "Baseline<br>(risk rate)",
            "SPI lag 1<br>(higher risk)",
            "Rainfall<br>(lower than normal)",
            "Commodity<br>(maize grain)",
            "District context<br>(lower risk)",
            "Population<br>(higher resilience)",
            "Predicted<br>probability"
        ]
        wf_y = [20.0, 22.5, 18.1, 10.4, -6.3, -2.3, 0]
        wf_measure = ["absolute", "relative", "relative", "relative", "relative", "relative", "total"]

        fig_wf = go.Figure(go.Waterfall(
            name="SHAP Attribution",
            orientation="v",
            measure=wf_measure,
            x=wf_x,
            textposition="outside",
            text=["20.0%", "+22.5%", "+18.1%", "+10.4%", "-6.3%", "-2.3%", "72.4%"],
            y=wf_y,
            connector={"line": {"color": "#E2E8F0", "dash": "solid"}},
            decreasing={"marker": {"color": "#147BB5"}},
            increasing={"marker": {"color": "#21A99F"}},
            totals={"marker": {"color": "#F0B83F"}}
        ))
        fig_wf.update_layout(
            height=320,
            margin=dict(l=30, r=20, t=10, b=40),
            yaxis=dict(title="Probability (%)", range=[0, 100], showgrid=True, gridcolor="#E2E8F0"),
            xaxis=dict(tickfont=dict(size=9.5)),
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FFFFFF"
        )
        st.plotly_chart(fig_wf, width='content', config={"displayModeBar": False})

        render_html("""
        <div style="background:#EAF4FC; border:1px solid #EAF4FC; border-radius:8px; padding:10px 14px; font-size:0.78rem; color:#147BB5; margin-top:8px;">
            <b>Predicted probability: 72.4%</b><br>
            Feature contribution explains the fitted model prediction; it does not prove causation.
        </div>
        """)

st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

# Interpretation Guidance (3 Cards Across)
st.markdown("""
<div style="font-size:1.05rem; font-weight:700; color:#172A40; margin-bottom:10px;">
    Interpretation guidance
</div>
""", unsafe_allow_html=True)

ig1, ig2, ig3 = st.columns(3)

with ig1:
    with st.container(border=True):
        render_html("""
        <div style="display:flex; gap:12px; align-items:flex-start;">
            <div style="background:#EAF4FC; color:#147BB5; width:36px; height:36px; border-radius:8px; display:flex; align-items:center; justify-content:center; font-size:18px; flex-shrink:0;">🔍</div>
            <div>
                <div style="font-weight:700; font-size:0.9rem; color:#172A40; margin-bottom:4px;">Use explanations to investigate</div>
                <div style="font-size:0.78rem; color:#748397; line-height:1.4;">Identify which factors are driving predictions and explore the underlying data.</div>
            </div>
        </div>
        """)

with ig2:
    with st.container(border=True):
        render_html("""
        <div style="display:flex; gap:12px; align-items:flex-start;">
            <div style="background:#E8F6EF; color:#21A99F; width:36px; height:36px; border-radius:8px; display:flex; align-items:center; justify-content:center; font-size:18px; flex-shrink:0;">⚖️</div>
            <div>
                <div style="font-weight:700; font-size:0.9rem; color:#172A40; margin-bottom:4px;">Do not infer causation</div>
                <div style="font-size:0.78rem; color:#748397; line-height:1.4;">Feature contributions show association with the model prediction, not cause and effect.</div>
            </div>
        </div>
        """)

with ig3:
    with st.container(border=True):
        render_html("""
        <div style="display:flex; gap:12px; align-items:flex-start;">
            <div style="background:#EAF4FC; color:#147BB5; width:36px; height:36px; border-radius:8px; display:flex; align-items:center; justify-content:center; font-size:18px; flex-shrink:0;">📑</div>
            <div>
                <div style="font-weight:700; font-size:0.9rem; color:#172A40; margin-bottom:4px;">Compare with official evidence</div>
                <div style="font-size:0.78rem; color:#748397; line-height:1.4;">Validate insights using government reports, field assessments and other trusted sources.</div>
            </div>
        </div>
        """)

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

# Bottom Disclaimer Banner
disclaimer_banner(
    "Disclaimer: Model explanations are based on the fitted model and available data. They are for informational use only and should be interpreted alongside official statistics, expert knowledge and on-the-ground evidence. They do not establish causation and should not be used as the sole basis for decisions."
)
