"""pages/7_Limitations.py - Limitations and Responsible Use

Matches Page 7 of ZCPSC_Dashboard_UI_Pages.pdf and the UI implementation prompt.
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
    title="Limitations and Responsible Use",
    subtitle="Important information for interpreting model-based predictions"
)

# Large Amber Warning Card
render_html("""
<div style="background:#FFF4D6; border:1px solid #F0B83F; border-radius:12px; padding:20px 24px; box-shadow:0 1px 3px rgba(0,0,0,0.04); display:flex; align-items:center; gap:18px; margin-bottom:18px;">
    <div style="background:#F0B83F; color:#FFFFFF; width:44px; height:44px; border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:24px; font-weight:bold; flex-shrink:0;">
        ⚠️
    </div>
    <div>
        <div style="font-size:1.15rem; font-weight:700; color:#F0B83F; margin-bottom:2px;">Use predictions as supporting evidence</div>
        <div style="font-size:0.88rem; color:#F0B83F;">This prototype does not replace official food-security assessment, expert judgement or field verification.</div>
    </div>
</div>
""")

# 3 Limitations Cards Across
c1, c2, c3 = st.columns(3)

with c1:
    with st.container(border=True):
        render_html("""
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:14px;">
            <div style="color:#147BB5; font-size:20px;">🗄️</div>
            <div style="font-weight:700; font-size:1.05rem; color:#172A40;">Data limitations</div>
        </div>
        <ul style="padding-left:18px; margin:0; font-size:0.83rem; color:#748397; line-height:1.6;">
            <li style="margin-bottom:8px;">Uneven reporting coverage across commodities, markets and time periods.</li>
            <li style="margin-bottom:8px;">Based on historical public data, which may be incomplete or subject to revision.</li>
            <li>Possible missing values and data quality issues.</li>
        </ul>
        """)

with c2:
    with st.container(border=True):
        render_html("""
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:14px;">
            <div style="color:#147BB5; font-size:20px;">⚙️</div>
            <div style="font-weight:700; font-size:1.05rem; color:#172A40;">Model limitations</div>
        </div>
        <ul style="padding-left:18px; margin:0; font-size:0.83rem; color:#748397; line-height:1.6;">
            <li style="margin-bottom:8px;">Class imbalance (relatively few high price-stress events).</li>
            <li style="margin-bottom:8px;">Potential distribution shift if future conditions differ from historical patterns.</li>
            <li style="margin-bottom:8px;">Predictions include uncertainty and should be interpreted probabilistically.</li>
            <li>No guaranteed forecast — model performance may vary over time and across commodities.</li>
        </ul>
        """)

with c3:
    with st.container(border=True):
        render_html("""
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:14px;">
            <div style="color:#147BB5; font-size:20px;">📊</div>
            <div style="font-weight:700; font-size:1.05rem; color:#172A40;">Interpretation limits</div>
        </div>
        <ul style="padding-left:18px; margin:0; font-size:0.83rem; color:#748397; line-height:1.6;">
            <li style="margin-bottom:8px;">Price stress is not the same as household food insecurity.</li>
            <li style="margin-bottom:8px;">SHAP explains model behaviour, not causation.</li>
            <li>No IPC phase assignment — this dashboard does not classify areas into IPC phases.</li>
        </ul>
        """)

st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

# Dark Navy Responsible-Use & Checklist Banner
render_html("""
<div style="background:#0B2743; border-radius:12px; padding:26px 30px; color:#FFFFFF; box-shadow:0 2px 8px rgba(0,0,0,0.08); display:flex; gap:36px; align-items:flex-start;">
    <div style="flex:1.8;">
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:10px;">
            <span style="font-size:20px;">🛡️</span>
            <span style="font-weight:700; font-size:1.1rem; letter-spacing:-0.01em;">Responsible-use statement</span>
        </div>
        <div style="font-size:0.84rem; color:#C8D6E4; line-height:1.6;">
            This dashboard provides model-based predictions of next-month relative commodity-price stress. It is an academic decision-support prototype. It does not constitute an official food-security assessment, an IPC classification or a guaranteed forecast.
        </div>
    </div>
    <div style="width:1px; background:rgba(255,255,255,0.15); align-self:stretch;"></div>
    <div style="flex:1.2;">
        <div style="font-weight:700; font-size:0.95rem; margin-bottom:12px; color:#C8D6E4;">Before using results</div>
        <div style="display:flex; flex-direction:column; gap:8px; font-size:0.82rem; color:#C8D6E4;">
            <div style="display:flex; align-items:center; gap:8px;">
                <span style="border:1px solid #C8D6E4; width:16px; height:16px; border-radius:3px; display:inline-block;"></span>
                <span>Review data coverage</span>
            </div>
            <div style="display:flex; align-items:center; gap:8px;">
                <span style="border:1px solid #C8D6E4; width:16px; height:16px; border-radius:3px; display:inline-block;"></span>
                <span>Check prediction month and target month</span>
            </div>
            <div style="display:flex; align-items:center; gap:8px;">
                <span style="border:1px solid #C8D6E4; width:16px; height:16px; border-radius:3px; display:inline-block;"></span>
                <span>Consult official evidence</span>
            </div>
        </div>
    </div>
</div>
""")
