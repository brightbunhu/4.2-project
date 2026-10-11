"""app.py - Main entrypoint for ZCPSC Streamlit Dashboard (Option B).

Uses Streamlit's official st.navigation to maintain ONE consistent, clean navbar
matching the exact design specifications from ZCPSC_Dashboard_UI_Pages.pdf and
the Complete ZCPSC Dashboard UI Implementation Prompt.

Prediction Horizon: Month T -> Month T+1 (Relative Commodity Price Stress)
Mandatory Disclaimer:
This dashboard provides model-based predictions of next-month relative commodity-price stress.
It is an academic decision-support prototype. It does not constitute an official food-security assessment,
an IPC classification or a guaranteed forecast. Predictions should be interpreted alongside official data,
expert judgement and wider food-security evidence.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
from app.styles import inject_css, sidebar_header, sidebar_footer

st.set_page_config(
    page_title="ZCPSC | Zimbabwe Commodity Price Stress Classifier",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject Global Visual Design System
inject_css()

# Consistent Sidebar Top Branding
sidebar_header()

# Define the single authoritative, consistent navigation bar (7 Pages from Design Spec & PDF)
pages = [
    st.Page("pages/1_Overview.py", title="Overview", icon="🏠", default=True),
    st.Page("pages/2_Next_Month_Prediction.py", title="Next-Month Prediction", icon="🔮"),
    st.Page("pages/3_CSV_Batch_Prediction.py", title="CSV Batch Upload", icon="📄"),
    st.Page("pages/4_Explore_Data.py", title="Explore Data", icon="📊"),
    st.Page("pages/5_Model_Explanations.py", title="Model Explanations", icon="💡"),
    st.Page("pages/6_Methodology.py", title="Methodology", icon="📖"),
    st.Page("pages/7_Limitations.py", title="Limitations", icon="ℹ️"),
]

# Run single consistent navigation
nav = st.navigation(pages, position="sidebar")

# Consistent Sidebar Bottom Branding
sidebar_footer()

nav.run()
