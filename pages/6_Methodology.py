"""pages/6_Methodology.py - Methodology

Matches Page 6 of ZCPSC_Dashboard_UI_Pages.pdf and the UI implementation prompt.
"""
from __future__ import annotations

import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
from app.styles import inject_css, page_header, disclaimer_banner
from app.components import render_html

inject_css()

# Top Header
page_header(
    title="Methodology",
    subtitle="How the next-month prediction system is constructed and evaluated"
)

# 4 Numbered Cards in a 2x2 Grid
m_r1_c1, m_r1_c2 = st.columns(2)

with m_r1_c1:
    render_html("""
    <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:12px; padding:20px; box-shadow:0 1px 3px rgba(0,0,0,0.04); display:flex; justify-content:space-between; align-items:center;">
        <div style="display:flex; align-items:center; gap:16px;">
            <div style="background:#21A99F; color:#FFFFFF; width:38px; height:38px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:700; font-size:16px; flex-shrink:0;">1</div>
            <div>
                <div style="font-weight:700; font-size:1.05rem; color:#172A40; margin-bottom:2px;">Data integration</div>
                <div style="font-size:0.83rem; color:#748397;">Market prices, rainfall, population and geography</div>
            </div>
        </div>
        <div style="font-size:24px; color:#21A99F; opacity:0.8;">🗄️</div>
    </div>
    """)

with m_r1_c2:
    render_html("""
    <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:12px; padding:20px; box-shadow:0 1px 3px rgba(0,0,0,0.04); display:flex; justify-content:space-between; align-items:center;">
        <div style="display:flex; align-items:center; gap:16px;">
            <div style="background:#147BB5; color:#FFFFFF; width:38px; height:38px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:700; font-size:16px; flex-shrink:0;">2</div>
            <div>
                <div style="font-weight:700; font-size:1.05rem; color:#172A40; margin-bottom:2px;">Target construction</div>
                <div style="font-size:0.83rem; color:#748397;">SPI > 1.25 and target shifted to month T+1</div>
            </div>
        </div>
        <div style="font-size:24px; color:#147BB5; opacity:0.8;">🎯</div>
    </div>
    """)

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

m_r2_c1, m_r2_c2 = st.columns(2)

with m_r2_c1:
    render_html("""
    <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:12px; padding:20px; box-shadow:0 1px 3px rgba(0,0,0,0.04); display:flex; justify-content:space-between; align-items:center;">
        <div style="display:flex; align-items:center; gap:16px;">
            <div style="background:#147BB5; color:#FFFFFF; width:38px; height:38px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:700; font-size:16px; flex-shrink:0;">3</div>
            <div>
                <div style="font-weight:700; font-size:1.05rem; color:#172A40; margin-bottom:2px;">Model validation</div>
                <div style="font-size:0.83rem; color:#748397;">Forward-chaining temporal validation and leakage controls</div>
            </div>
        </div>
        <div style="font-size:24px; color:#147BB5; opacity:0.8;">📊</div>
    </div>
    """)

with m_r2_c2:
    render_html("""
    <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:12px; padding:20px; box-shadow:0 1px 3px rgba(0,0,0,0.04); display:flex; justify-content:space-between; align-items:center;">
        <div style="display:flex; align-items:center; gap:16px;">
            <div style="background:#21A99F; color:#FFFFFF; width:38px; height:38px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:700; font-size:16px; flex-shrink:0;">4</div>
            <div>
                <div style="font-weight:700; font-size:1.05rem; color:#172A40; margin-bottom:2px;">Model explanation</div>
                <div style="font-size:0.83rem; color:#748397;">SHAP feature contributions and transparent communication</div>
            </div>
        </div>
        <div style="font-size:24px; color:#21A99F; opacity:0.8;">🔬</div>
    </div>
    """)

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

# Method Workflow and Models Compared
wf_col, mod_col = st.columns([1.5, 1.0])

with wf_col:
    render_html("""
    <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:12px; padding:22px; box-shadow:0 1px 3px rgba(0,0,0,0.04); height:100%;">
        <div style="font-size:1.05rem; font-weight:700; color:#172A40; margin-bottom:18px;">Method workflow</div>
        <div style="display:flex; align-items:center; justify-content:space-between; gap:10px; padding:10px 0;">
            <div style="text-align:center; flex:1;">
                <div style="font-size:22px; margin-bottom:4px;">🗂️</div>
                <div style="font-size:0.8rem; font-weight:600; color:#172A40;">Information<br>available at T</div>
            </div>
            <div style="color:#748397; font-size:18px; font-weight:bold;">→</div>
            <div style="text-align:center; flex:1;">
                <div style="font-size:22px; margin-bottom:4px;">⚙️</div>
                <div style="font-size:0.8rem; font-weight:600; color:#172A40;">Feature<br>pipeline</div>
            </div>
            <div style="color:#748397; font-size:18px; font-weight:bold;">→</div>
            <div style="text-align:center; flex:1;">
                <div style="font-size:22px; margin-bottom:4px;">🧠</div>
                <div style="font-size:0.8rem; font-weight:600; color:#172A40;">Model</div>
            </div>
            <div style="color:#748397; font-size:18px; font-weight:bold;">→</div>
            <div style="text-align:center; flex:1;">
                <div style="font-size:22px; margin-bottom:4px;">📈</div>
                <div style="font-size:0.8rem; font-weight:600; color:#172A40;">Prediction<br>for T+1</div>
            </div>
        </div>
    </div>
    """)

with mod_col:
    render_html("""
    <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:12px; padding:22px; box-shadow:0 1px 3px rgba(0,0,0,0.04); height:100%;">
        <div style="font-size:1.05rem; font-weight:700; color:#172A40; margin-bottom:14px; display:flex; align-items:center; gap:8px;">
            <span>🧊</span> <span>Models compared</span>
        </div>
        <div style="display:flex; flex-direction:column; gap:12px;">
            <div style="display:flex; align-items:center; gap:10px; font-size:0.85rem; color:#172A40;">
                <span style="color:#147BB5;">📊</span>
                <span style="font-weight:500;">DummyClassifier baseline</span>
            </div>
            <div style="display:flex; align-items:center; gap:10px; font-size:0.85rem; color:#172A40;">
                <span style="color:#147BB5;">📈</span>
                <span style="font-weight:500;">Logistic Regression</span>
            </div>
            <div style="display:flex; align-items:center; gap:10px; font-size:0.85rem; color:#172A40;">
                <span style="color:#21A99F;">🌳</span>
                <span style="font-weight:600; color:#21A99F;">XGBoost (Champion Model)</span>
            </div>
        </div>
    </div>
    """)

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

# Key Definition Card
render_html("""
<div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:12px; padding:22px; box-shadow:0 1px 3px rgba(0,0,0,0.04);">
    <div style="font-size:1.05rem; font-weight:700; color:#172A40; margin-bottom:12px; display:flex; align-items:center; gap:8px;">
        <span>📖</span> <span>Key definition</span>
    </div>
    <div style="display:flex; align-items:center; gap:36px; padding:10px 0;">
        <div style="background:#EAF4FC; border:1px solid #EAF4FC; border-radius:10px; padding:16px 28px; font-size:1.5rem; font-weight:700; color:#1676B8; font-family:serif;">
            X<sub>t</sub> → Y<sub>(t+1)</sub>
        </div>
        <div style="font-size:0.95rem; color:#748397; line-height:1.5;">
            Predict relative commodity-price stress in the following month (T+1) strictly using predictor information available by month T.
        </div>
    </div>
</div>
""")

st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

# Bottom Academic Banner
disclaimer_banner(
    "This system is for academic research purposes only. Predictions are not a substitute for professional advice or decision-making. ZCPSC | Academic Research System | v1.0"
)
