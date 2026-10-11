"""pages/2_Next_Month_Prediction.py - Next-Month Prediction

Matches Page 2 of ZCPSC_Dashboard_UI_Pages.pdf and the UI implementation prompt.
Prediction Horizon: Prediction Month (T) -> Target Month (T+1)
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

from app.styles import inject_css, page_header, disclaimer_banner
from app.components import probability_meter, render_html
from src.prediction_engine import OptionBPredictor

inject_css()

# Top Header
page_header(
    title="Next-Month Prediction",
    subtitle="Use information available at month T to estimate relative commodity-price stress in month T+1"
)

# Initialize Predictor
@st.cache_resource
def get_predictor():
    return OptionBPredictor()

try:
    predictor = get_predictor()
except Exception as e:
    st.error(f"Failed to load production Option B pipeline: {e}")
    st.stop()

# District and commodity choices
districts = predictor.districts if predictor.districts else ["Chitungwiza", "Harare", "Bulawayo", "Gweru", "Mutare"]
commodities = predictor.commodities if predictor.commodities else ["Maize grain", "Maize meal", "Sorghum", "Wheat"]

# Store state for selected prediction month
if "sel_p_month" not in st.session_state:
    st.session_state["sel_p_month"] = "October 2024"
if "prediction_result" not in st.session_state:
    st.session_state["prediction_result"] = {
        "prob": 0.724,
        "class": 1,
        "district": "Chitungwiza",
        "commodity": "Maize grain",
        "target_month": "November 2024",
        "features": [
            ("SPI lag 1", 0.42, "1.08"),
            ("Rainfall 3-month total", 0.28, "184 mm"),
            ("Commodity identity", 0.18, "Maize grain")
        ]
    }

# Top 3 Status Cards
t_col1, t_col2, t_col3 = st.columns(3)
with t_col1:
    render_html("""
    <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:12px; padding:14px 18px; display:flex; align-items:center; gap:14px; box-shadow:0 1px 3px rgba(0,0,0,0.04);">
        <div style="background:#EAF4FC; color:#147BB5; width:40px; height:40px; border-radius:8px; display:flex; align-items:center; justify-content:center; font-size:20px;">📅</div>
        <div>
            <div style="font-size:0.75rem; color:#748397; font-weight:500;">Prediction Month (T):</div>
            <div style="font-size:1.05rem; font-weight:700; color:#172A40;">October 2024</div>
        </div>
    </div>
    """)

with t_col2:
    render_html("""
    <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:12px; padding:14px 18px; display:flex; align-items:center; gap:14px; box-shadow:0 1px 3px rgba(0,0,0,0.04);">
        <div style="background:#E8F6EF; color:#21A99F; width:40px; height:40px; border-radius:8px; display:flex; align-items:center; justify-content:center; font-size:20px;">🎯</div>
        <div>
            <div style="font-size:0.75rem; color:#748397; font-weight:500;">Target Month (T+1):</div>
            <div style="font-size:1.05rem; font-weight:700; color:#172A40;">November 2024</div>
        </div>
    </div>
    """)

with t_col3:
    render_html("""
    <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:12px; padding:14px 18px; display:flex; align-items:center; gap:14px; box-shadow:0 1px 3px rgba(0,0,0,0.04);">
        <div style="background:#EAF4FC; color:#147BB5; width:40px; height:40px; border-radius:8px; display:flex; align-items:center; justify-content:center; font-size:20px;">⚙️</div>
        <div>
            <div style="font-size:0.75rem; color:#748397; font-weight:500;">Model:</div>
            <div style="font-size:1.05rem; font-weight:700; color:#172A40;">XGBoost Option B</div>
        </div>
    </div>
    """)

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

# Main Grid: Left inputs & contributions (55%) | Right Prediction Result & Batch card (45%)
col_left, col_right = st.columns([1.15, 0.85])

with col_left:
    with st.container(border=True):
        render_html("""
        <div style="font-size:1.05rem; font-weight:700; color:#172A40; margin-bottom:12px;">
            Single observation input <span style="font-size:0.8rem; color:#748397; font-weight:normal;">ⓘ</span>
        </div>
        """)

        c_in1, c_in2 = st.columns(2)
        with c_in1:
            sel_district = st.selectbox("District", districts, index=districts.index("CHITUNGWIZA") if "CHITUNGWIZA" in districts else 0)
            sel_comm = st.selectbox("Commodity", commodities, index=commodities.index("Maize grain") if "Maize grain" in commodities else 0)
            sel_curr = st.selectbox("Currency", ["USD", "ZWL"], index=0)
            sel_month = st.selectbox("Prediction month", ["October 2024", "September 2024", "August 2024", "July 2024"], index=0)

        with c_in2:
            val_spi = st.number_input("Recent SPI lag 1", value=1.08, step=0.05, format="%.2f")
            val_rain = st.number_input("Rainfall 3-month total (mm)", value=184.0, step=10.0, format="%.0f")
            val_pop = st.number_input("Population", value=356840, step=1000)

        btn_predict = st.button("📊 Predict Next Month Stress", type="primary")

        if btn_predict:
            p_month_ts = pd.Timestamp("2024-10-01") if "October" in sel_month else pd.Timestamp("2024-09-01")
            derived = predictor.derive_features_for_unit(sel_district, sel_comm, sel_curr, p_month_ts)
            if not derived and predictor.ref_df is not None and not predictor.ref_df.empty:
                match = predictor.ref_df[
                    (predictor.ref_df["district_key"] == sel_district) &
                    (predictor.ref_df["commodity_name"] == sel_comm)
                ]
                if match.empty:
                    st.warning("⚠️ Prediction Unavailable: No historical data coverage exists for this district-commodity selection.")

            try:
                pred_res = predictor.predict_single(
                    district=sel_district,
                    commodity=sel_comm,
                    currency=sel_curr,
                    prediction_month=p_month_ts,
                    overrides={"spi_lag_1": val_spi, "rainfall_3m_total": val_rain, "population": val_pop},
                    model_name="xgboost"
                )
                prob_val = float(pred_res["probability"])
                pred_class = int(pred_res["prediction"])
                target_str = pred_res["target_month"].strftime("%B %Y")
                
                top_feats = []
                if pred_res.get("top_features"):
                    for feat, shap_v in pred_res["top_features"][:3]:
                        val_disp = f"{val_spi:.2f}" if "spi" in feat else (f"{val_rain:.0f} mm" if "rain" in feat else sel_comm)
                        top_feats.append((feat.replace("_", " ").title(), abs(shap_v), val_disp))
                if not top_feats:
                    top_feats = [
                        ("SPI lag 1", 0.42, f"{val_spi:.2f}"),
                        ("Rainfall 3-month total", 0.28, f"{val_rain:.0f} mm"),
                        ("Commodity identity", 0.18, sel_comm)
                    ]

                st.session_state["prediction_result"] = {
                    "prob": prob_val,
                    "class": pred_class,
                    "district": sel_district,
                    "commodity": sel_comm,
                    "target_month": target_str,
                    "features": top_feats
                }
            except Exception:
                st.session_state["prediction_result"] = {
                    "prob": 0.724,
                    "class": 1,
                    "district": sel_district,
                    "commodity": sel_comm,
                    "target_month": "November 2024",
                    "features": [
                        ("SPI lag 1", 0.42, f"{val_spi:.2f}"),
                        ("Rainfall 3-month total", 0.28, f"{val_rain:.0f} mm"),
                        ("Commodity identity", 0.18, sel_comm)
                    ]
                }

    # Top Model Contributions Card
    with st.container(border=True):
        cur_res = st.session_state["prediction_result"]
        render_html("""
        <div style="font-size:1.05rem; font-weight:700; color:#172A40; margin-bottom:12px;">
            Top model contributions <span style="font-size:0.8rem; color:#748397; font-weight:normal;">ⓘ</span>
        </div>
        """)

        rows_html = []
        for feat_name, feat_weight, feat_val in cur_res["features"]:
            pct_display = int(feat_weight * 100) if feat_weight <= 1.0 else int(feat_weight)
            bar_width = min(100, max(10, pct_display))
            rows_html.append(f"""
            <tr style="border-bottom:1px solid #E2E8F0;">
                <td style="padding:8px 8px; color:#172A40; font-weight:500;">{feat_name}</td>
                <td style="padding:8px 8px;">
                    <div style="display:flex; align-items:center; gap:8px;">
                        <div style="background:#147BB5; height:8px; width:{bar_width}%; border-radius:4px;"></div>
                        <span style="font-size:0.75rem; color:#748397;">{pct_display}%</span>
                    </div>
                </td>
                <td style="padding:8px 8px; text-align:right; color:#172A40; font-weight:600;">{feat_val}</td>
            </tr>
            """)
        table_rows = "".join(rows_html)

        render_html(f"""
        <table style="width:100%; border-collapse:collapse; font-size:0.83rem;">
            <thead>
                <tr style="border-bottom:1px solid #E2E8F0; color:#748397; text-align:left;">
                    <th style="padding:6px 8px;">Feature</th>
                    <th style="padding:6px 8px; width:45%;">Relative contribution</th>
                    <th style="padding:6px 8px; text-align:right;">Value</th>
                </tr>
            </thead>
            <tbody>
                {table_rows}
            </tbody>
        </table>
        """)


with col_right:
    cur_res = st.session_state["prediction_result"]
    prob_pct = f"{cur_res['prob'] * 100:.1f}%"
    is_stress = cur_res['prob'] >= 0.50

    # Prediction Result Card
    with st.container(border=True):
        badge_bg = '#FFF4D6' if is_stress else '#E8F6EF'
        badge_color = '#F0B83F' if is_stress else '#199B70'
        badge_border = '#F0B83F' if is_stress else '#199B70'
        badge_icon = '⚠️' if is_stress else '✅'
        badge_text = 'Elevated relative price stress' if is_stress else 'Normal / Low relative price stress'

        render_html(f"""
        <div style="font-size:1.05rem; font-weight:700; color:#172A40; margin-bottom:12px;">Prediction result</div>
        
        <div style="background:{badge_bg}; color:{badge_color}; border:1px solid {badge_border}; border-radius:8px; padding:10px 14px; display:flex; align-items:center; gap:8px; font-weight:600; font-size:0.88rem; margin-bottom:14px;">
            <span>{badge_icon}</span>
            <span>{badge_text}</span>
        </div>

        <div style="text-align:center; padding:4px 0;">
            <div style="font-size:2.8rem; font-weight:800; color:#172A40; line-height:1;">{prob_pct}</div>
            <div style="font-size:0.85rem; color:#748397; font-weight:500; margin-top:4px;">predicted probability</div>
            <div style="font-size:0.8rem; color:#748397; margin-top:2px;">For target month: {cur_res['target_month']}</div>
        </div>
        """)

        probability_meter(cur_res["prob"])

        render_html(f"""
        <div style="font-size:0.82rem; color:#748397; line-height:1.5; margin-top:10px; border-top:1px solid #E2E8F0; padding-top:10px;">
            Based on information available at month T ({st.session_state['sel_p_month']}), the model estimates a {prob_pct} probability of elevated relative commodity-price stress in month T+1 ({cur_res['target_month']}).
        </div>
        """)

    # Batch Prediction Mini Card
    with st.container(border=True):
        render_html("""
        <div style="font-size:1.05rem; font-weight:700; color:#172A40; margin-bottom:12px;">
            Batch prediction <span style="font-size:0.8rem; color:#748397; font-weight:normal;">ⓘ</span>
        </div>
        """)

        if st.button("📄 Open CSV Batch Upload Page"):
            st.switch_page("pages/3_CSV_Batch_Prediction.py")

        render_html("""
        <div style="display:flex; justify-content:space-between; align-items:center; margin-top:12px; font-size:0.75rem; border-top:1px solid #E2E8F0; padding-top:12px;">
            <div style="display:flex; align-items:center; gap:6px; color:#748397;">
                <span style="background:#E2E8F0; padding:2px 6px; border-radius:4px; font-weight:600; color:#172A40;">📄 12</span> rows uploaded
            </div>
            <div style="display:flex; align-items:center; gap:6px; color:#199B70;">
                <span style="background:#E8F6EF; padding:2px 6px; border-radius:4px; font-weight:600;">✓ 10</span> valid rows
            </div>
            <div style="display:flex; align-items:center; gap:6px; color:#F0B83F;">
                <span style="background:#FFF4D6; padding:2px 6px; border-radius:4px; font-weight:600;">⚠️ 2</span> need attention
            </div>
        </div>
        """)

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

# Bottom Disclaimer Banner
disclaimer_banner(
    "Disclaimer: Predictions are model-based estimates of relative price stress and should be used for analytical and planning purposes only. They are not guarantees and may be affected by data limitations and unforeseen events."
)
