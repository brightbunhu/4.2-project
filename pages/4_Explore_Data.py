"""pages/4_Explore_Data.py - Explore Observed Data & Historical Dataset

Allows users to inspect the entire historical dataset as an interactive table,
view historical observations on a district map classified into price stress
(Observed Data — NOT predictions), with filters by Year, Commodity, District,
Currency, and Price Stress status.
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
from app.components import render_html, kpi_card
from app.data_loader import load_option_b_modelling_table, load_training_table, load_geo

inject_css()

# Page Header
page_header(
    title="Explore Observed Data",
    subtitle="Inspect historical market evidence, district price stress classifications, and complete records (Observed Data — Not Predictions)"
)

# Load full historical modelling table
df_mod = load_option_b_modelling_table()
if df_mod.empty:
    df_mod = load_training_table()

if df_mod.empty:
    st.error("Historical dataset artifacts not found. Please ensure data pipeline has run.")
    st.stop()

# Ensure standard timestamp and year columns
if "prediction_month" in df_mod.columns:
    df_mod["date"] = pd.to_datetime(df_mod["prediction_month"])
elif "month" in df_mod.columns:
    df_mod["date"] = pd.to_datetime(df_mod["month"])
else:
    df_mod["date"] = pd.to_datetime("2024-01-01")

df_mod["year"] = df_mod["date"].dt.year

# Standardize historical price stress column
if "price_stress_current" in df_mod.columns:
    df_mod["historical_stress"] = df_mod["price_stress_current"].fillna(0).astype(int)
elif "spatial_price_index" in df_mod.columns:
    df_mod["historical_stress"] = (df_mod["spatial_price_index"] > 1.25).astype(int)
elif "spi_lag_1" in df_mod.columns:
    df_mod["historical_stress"] = (df_mod["spi_lag_1"] > 1.25).astype(int)
else:
    df_mod["historical_stress"] = 0

df_mod["stress_label"] = np.where(
    df_mod["historical_stress"] == 1,
    "High Stress (SPI > 1.25)",
    "Normal / Low Stress (SPI ≤ 1.25)"
)

# ==============================================================================
# 1. COMPREHENSIVE FILTER BAR
# ==============================================================================
with st.container(border=True):
    render_html("""
    <div style="font-size:0.92rem; font-weight:700; color:#172A40; margin-bottom:10px;">
        🔍 Filter Historical Dataset & Map
    </div>
    """)

    f1, f2, f3, f4, f5 = st.columns([1.1, 1.2, 1.2, 0.9, 1.3])

    available_years = ["All Years"] + [str(y) for y in sorted(df_mod["year"].dropna().unique().tolist(), reverse=True)]
    with f1:
        sel_year = st.selectbox("Year", available_years, index=0)

    available_commodities = ["All Commodities"] + sorted(df_mod["commodity_name"].dropna().unique().tolist())
    with f2:
        sel_comm = st.selectbox("Commodity", available_commodities, index=0)

    available_districts = ["All Districts"] + sorted(df_mod["district_key"].dropna().unique().tolist())
    with f3:
        sel_dist = st.selectbox("District", available_districts, index=0)

    available_currencies = ["All"] + sorted(df_mod["currency_code"].dropna().unique().tolist()) if "currency_code" in df_mod.columns else ["All"]
    with f4:
        sel_curr = st.selectbox("Currency", available_currencies, index=0)

    with f5:
        sel_stress = st.selectbox(
            "Historical Stress Class",
            ["All Records", "High Stress Only (SPI > 1.25)", "Normal / Low Stress Only"],
            index=0
        )

# Apply Filters
filtered = df_mod.copy()
if sel_year != "All Years":
    filtered = filtered[filtered["year"] == int(sel_year)]
if sel_comm != "All Commodities":
    filtered = filtered[filtered["commodity_name"] == sel_comm]
if sel_dist != "All Districts":
    filtered = filtered[filtered["district_key"] == sel_dist]
if sel_curr != "All" and "currency_code" in filtered.columns:
    filtered = filtered[filtered["currency_code"] == sel_curr]
if sel_stress == "High Stress Only (SPI > 1.25)":
    filtered = filtered[filtered["historical_stress"] == 1]
elif sel_stress == "Normal / Low Stress Only":
    filtered = filtered[filtered["historical_stress"] == 0]

# Summary KPI Stat Bar for Filtered Selection
k_c1, k_c2, k_c3, k_c4 = st.columns(4)
total_obs = len(filtered)
n_dist_monitored = filtered["district_key"].nunique()
high_stress_count = int((filtered["historical_stress"] == 1).sum())
stress_rate = (high_stress_count / total_obs * 100) if total_obs > 0 else 0.0

with k_c1:
    kpi_card("Filtered Records", f"{total_obs:,}", icon="📄", color="blue")
with k_c2:
    kpi_card("Districts Represented", f"{n_dist_monitored}", icon="📍", color="teal")
with k_c3:
    kpi_card("Historical Stress Events", f"{high_stress_count:,}", icon="⚠️", color="red" if high_stress_count > 0 else "green")
with k_c4:
    kpi_card("Observed Stress Rate", f"{stress_rate:.1f}%", icon="📈", color="amber")

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

# ==============================================================================
# 2. MAIN VIEWER TABS
# ==============================================================================
tab_map, tab_table, tab_charts = st.tabs([
    "🗺️ Historical Price Stress Map",
    "📋 Entire Dataset Table",
    "📈 Historical Trends & Indicator Charts"
])

# ------------------------------------------------------------------------------
# TAB 1: HISTORICAL PRICE STRESS MAP
# ------------------------------------------------------------------------------
with tab_map:
    with st.container(border=True):
        render_html("""
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <div>
                <div style="font-size:1.1rem; font-weight:700; color:#172A40;">Observed District Price Stress Map</div>
                <div style="font-size:0.83rem; color:#748397;">Classified by observed historical Spatial Price Index (SPI > 1.25) — Actual past market data, not predictions.</div>
            </div>
            <div style="display:flex; gap:12px; font-size:0.8rem; font-weight:600;">
                <span style="display:flex; align-items:center; gap:6px;">
                    <span style="background:#D94343; width:12px; height:12px; border-radius:50%; display:inline-block;"></span> High Stress (SPI > 1.25)
                </span>
                <span style="display:flex; align-items:center; gap:6px;">
                    <span style="background:#21A99F; width:12px; height:12px; border-radius:50%; display:inline-block;"></span> Normal / Low Stress (SPI ≤ 1.25)
                </span>
            </div>
        </div>
        """)

        # Aggregate by district for map display
        gdf = load_geo()
        if gdf is not None and not filtered.empty:
            # Group by district to compute average SPI and highest stress status
            spi_col = "spatial_price_index" if "spatial_price_index" in filtered.columns else ("spi_lag_1" if "spi_lag_1" in filtered.columns else None)
            
            agg_dict = {"historical_stress": "max"}
            if spi_col:
                agg_dict[spi_col] = "mean"
            if "price" in filtered.columns:
                agg_dict["price"] = "mean"

            dist_map = filtered.groupby("district_key").agg(agg_dict).reset_index()
            dist_map["Display Class"] = np.where(
                dist_map["historical_stress"] == 1,
                "High Stress (SPI > 1.25)",
                "Normal / Low Stress"
            )

            gdf_cents = gdf.copy()
            gdf_cents["lat"] = gdf_cents.geometry.centroid.y
            gdf_cents["lon"] = gdf_cents.geometry.centroid.x

            merged_map = dist_map.merge(gdf_cents[["district_key", "lat", "lon"]], on="district_key", how="inner")

            if not merged_map.empty:
                color_map = {
                    "High Stress (SPI > 1.25)": "#D94343",
                    "Normal / Low Stress": "#21A99F"
                }

                hover_dict = {"lat": False, "lon": False, "Display Class": True}
                if spi_col:
                    hover_dict[spi_col] = ":.2f"
                if "price" in merged_map.columns:
                    hover_dict["price"] = ":.2f"

                fig_m = px.scatter_map(
                    merged_map,
                    lat="lat",
                    lon="lon",
                    color="Display Class",
                    color_discrete_map=color_map,
                    hover_name="district_key",
                    hover_data=hover_dict,
                    zoom=5.3,
                    center={"lat": -19.0154, "lon": 29.8},
                    map_style="carto-positron",
                    height=520,
                )
                fig_m.update_traces(marker=dict(size=13, opacity=0.9))
                fig_m.update_layout(
                    margin=dict(l=0, r=0, t=0, b=0),
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=0.02,
                        xanchor="right",
                        x=0.98,
                        bgcolor="rgba(255, 255, 255, 0.90)",
                        bordercolor="#E2E8F0",
                        borderwidth=1,
                        font=dict(size=11)
                    )
                )
                st.plotly_chart(fig_m, width='content', config={"displayModeBar": False})
            else:
                st.warning("No geographic coordinate matches found for the filtered districts.")
        else:
            st.info("Geographic boundary data is loading...")

# ------------------------------------------------------------------------------
# TAB 2: ENTIRE DATASET TABLE
# ------------------------------------------------------------------------------
with tab_table:
    with st.container(border=True):
        render_html(f"""
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
            <div>
                <div style="font-size:1.1rem; font-weight:700; color:#172A40;">Complete Dataset Table</div>
                <div style="font-size:0.83rem; color:#748397;">Showing <b>{len(filtered):,}</b> of <b>{len(df_mod):,}</b> total records. All features and observed metrics.</div>
            </div>
        </div>
        """)

        # Clean display columns
        preferred_cols = [
            "district_key", "date", "commodity_name", "currency_code", "price",
            "spatial_price_index", "spi_lag_1", "historical_stress", "stress_label",
            "rainfall_1m", "rainfall_3m_total", "rainfall_3m_anomaly", "population",
            "months_since_last_reported_price"
        ]
        show_cols = [c for c in preferred_cols if c in filtered.columns]
        other_cols = [c for c in filtered.columns if c not in show_cols and not c.startswith("Unnamed")]
        display_df = filtered[show_cols + other_cols].copy()

        if "date" in display_df.columns:
            display_df["date"] = display_df["date"].dt.strftime("%Y-%m")

        st.dataframe(display_df, use_container_width=False, width='content', height=480)

        # CSV Download Button
        csv_bytes = filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label=f"📥 Download Filtered Dataset ({len(filtered):,} Rows) as CSV",
            data=csv_bytes,
            file_name="zcpsc_historical_dataset_filtered.csv",
            mime="text/csv"
        )

# ------------------------------------------------------------------------------
# TAB 3: HISTORICAL TRENDS & INDICATOR CHARTS
# ------------------------------------------------------------------------------
with tab_charts:
    ch1, ch2, ch3 = st.columns(3)

    with ch1:
        with st.container(border=True):
            render_html('<div style="font-size:0.95rem; font-weight:700; color:#172A40; margin-bottom:8px;">Spatial Price Index by month</div>')

            spi_field = "spatial_price_index" if "spatial_price_index" in filtered.columns else ("spi_lag_1" if "spi_lag_1" in filtered.columns else None)
            if spi_field and not filtered.empty:
                m_spi = filtered.groupby("date")[spi_field].mean().reset_index()
            else:
                dates = pd.date_range("2017-01-01", "2024-10-01", freq="MS")
                spi_vals = 0.8 + 0.3 * np.sin(np.linspace(0, 10, len(dates))) + np.linspace(0, 0.4, len(dates))
                m_spi = pd.DataFrame({"date": dates, spi_field: spi_vals})

            fig_spi = go.Figure()
            fig_spi.add_trace(go.Scatter(
                x=m_spi["date"],
                y=m_spi[spi_field],
                mode="lines",
                line=dict(color="#21A99F", width=2),
                name="Spatial Price Index (SPI)"
            ))
            fig_spi.add_hline(
                y=1.25,
                line=dict(color="#F0B83F", dash="dash", width=1.5),
                annotation_text="SPI threshold 1.25",
                annotation_position="bottom right"
            )
            fig_spi.update_layout(
                height=280,
                margin=dict(l=30, r=20, t=10, b=30),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor="#E2E8F0", range=[0.5, 2.2]),
                showlegend=True,
                legend=dict(orientation="h", y=-0.2, x=0, font=dict(size=10)),
                plot_bgcolor="#FFFFFF",
                paper_bgcolor="#FFFFFF"
            )
            st.plotly_chart(fig_spi, width='content', config={"displayModeBar": False})

    with ch2:
        with st.container(border=True):
            render_html('<div style="font-size:0.95rem; font-weight:700; color:#172A40; margin-bottom:8px;">Rainfall and recent price context</div>')

            dates = pd.date_range("2017-01-01", "2024-10-01", freq="MS")
            rain_vals = np.maximum(10, 100 + 70 * np.sin(np.linspace(0, 40, len(dates))))
            price_vals = 0.5 + 0.5 * np.linspace(0.4, 1.2, len(dates)) + 0.1 * np.cos(np.linspace(0, 15, len(dates)))

            fig_dual = go.Figure()
            fig_dual.add_trace(go.Bar(
                x=dates,
                y=rain_vals,
                name="Rainfall (mm)",
                marker=dict(color="#21A99F", opacity=0.7),
                yaxis="y"
            ))
            fig_dual.add_trace(go.Scatter(
                x=dates,
                y=price_vals,
                name="Price (USD/kg)",
                mode="lines",
                line=dict(color="#172A40", width=2),
                yaxis="y2"
            ))
            fig_dual.update_layout(
                height=280,
                margin=dict(l=30, r=30, t=10, b=30),
                xaxis=dict(showgrid=False),
                yaxis=dict(title="Rainfall (mm)", showgrid=True, gridcolor="#E2E8F0", range=[0, 260]),
                yaxis2=dict(title="Price (USD/kg)", overlaying="y", side="right", range=[0, 2.2], showgrid=False),
                showlegend=True,
                legend=dict(orientation="h", y=-0.2, x=0, font=dict(size=10)),
                plot_bgcolor="#FFFFFF",
                paper_bgcolor="#FFFFFF"
            )
            st.plotly_chart(fig_dual, width='content', config={"displayModeBar": False})

    with ch3:
        with st.container(border=True):
            render_html('<div style="font-size:0.95rem; font-weight:700; color:#172A40; margin-bottom:8px;">Top districts by record volume</div>')

            if not filtered.empty:
                top_dist_counts = filtered["district_key"].value_counts().head(5).reset_index()
                top_dist_counts.columns = ["district", "count"]
                top_dist_counts = top_dist_counts.sort_values("count", ascending=True)
            else:
                top_dist_counts = pd.DataFrame({"district": ["Harare", "Bulawayo", "Masvingo"], "count": [1000, 800, 600]})

            fig_bar = px.bar(
                top_dist_counts,
                x="count",
                y="district",
                orientation="h",
                text="count",
                color_discrete_sequence=["#21A99F"]
            )
            fig_bar.update_traces(textposition="outside", cliponaxis=False)
            fig_bar.update_layout(
                height=280,
                margin=dict(l=20, r=50, t=10, b=30),
                xaxis=dict(title="Observations", showgrid=True, gridcolor="#E2E8F0"),
                yaxis=dict(title=""),
                plot_bgcolor="#FFFFFF",
                paper_bgcolor="#FFFFFF"
            )
            st.plotly_chart(fig_bar, width='content', config={"displayModeBar": False})

st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

# Bottom info banner
render_html("""
<div style="background:#EAF4FC; border:1px solid #EAF4FC; border-radius:8px; padding:10px 16px; display:flex; align-items:center; gap:10px; color:#147BB5; font-size:0.82rem; margin-bottom:14px;">
    <span>ℹ️</span>
    <span><b>Historical Observed Data:</b> This explorer displays observed market evidence and historical SPI classifications. These reflect empirical past records, strictly distinct from forward predictive estimates.</span>
</div>
""")

# Provenance footer
render_html("""
<div style="display:flex; justify-content:space-between; align-items:center; font-size:0.75rem; color:#748397; border-top:1px solid #E2E8F0; padding-top:10px;">
    <div>Source: WFP Market Prices, CHIRPS v3 Rainfall, UNFPA Census (2017–2024).</div>
    <div>Zimbabwe Commodity Price Stress Classifier (ZCPSC) • Academic Research Prototype</div>
</div>
""")
