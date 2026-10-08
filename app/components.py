"""Reusable UI components for the ZFPS dashboard."""
from __future__ import annotations

import html

import numpy as np
import pandas as pd
import streamlit as st

from styles import COLORS, DESCRIPTION, DISCLAIMER, STRESS_COLOURS, SUBTITLE, TITLE


# --------------------------------------------------------------------------------------
# Headers
# --------------------------------------------------------------------------------------
def page_header(title: str, subtitle: str = "") -> None:
    st.markdown(f"<div class='zfps-page-title'>{html.escape(title)}</div>", unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"<div class='zfps-page-sub'>{html.escape(subtitle)}</div>",
                    unsafe_allow_html=True)


def section_title(title: str, sub: str = "") -> None:
    st.markdown(f"<div class='zfps-section-title'>{html.escape(title)}</div>",
                unsafe_allow_html=True)
    if sub:
        st.markdown(f"<div class='zfps-section-sub'>{html.escape(sub)}</div>",
                    unsafe_allow_html=True)


def banner(title: str = TITLE, subtitle: str = SUBTITLE, description: str = DESCRIPTION) -> None:
    st.markdown(
        f"<div class='zfps-page-title'>{html.escape(title)}</div>"
        f"<div class='zfps-page-sub'>{html.escape(subtitle)}</div>",
        unsafe_allow_html=True)


# --------------------------------------------------------------------------------------
# Sidebar
# --------------------------------------------------------------------------------------
def sidebar_brand() -> None:
    st.markdown(
        "<div class='zfps-brand'>"
        "<div class='logo'>\U0001F33E ZFPS</div>"
        "<div class='sub'>Food Price Stress</div>"
        "</div>",
        unsafe_allow_html=True)


def sidebar_footer() -> None:
    st.markdown(
        "<div class='zfps-sidefoot'>"
        "<div class='h'>Research Prototype</div>"
        "Machine Learning Classification of Commodity-Level Food Price Stress in Zimbabwe."
        "<div class='warn'>Not an official food-price assessment or early-warning system.</div>"
        "</div>",
        unsafe_allow_html=True)


# --------------------------------------------------------------------------------------
# Cards
# --------------------------------------------------------------------------------------
def kpi_card(label: str, value: object, foot: str = "", accent: str | None = None) -> None:
    style = f" style='border-top-color:{accent}'" if accent else ""
    st.markdown(
        f"<div class='zfps-card zfps-kpi'{style}>"
        f"<div class='label'>{html.escape(str(label))}</div>"
        f"<div class='value'>{html.escape(str(value))}</div>"
        f"<div class='foot'>{html.escape(str(foot))}</div>"
        "</div>",
        unsafe_allow_html=True)


def kpi_row(items: list[tuple]) -> None:
    """items: list of (label, value, foot) or (label, value, foot, accent)."""
    cols = st.columns(len(items))
    for col, item in zip(cols, items):
        label, value, foot = item[0], item[1], item[2]
        accent = item[3] if len(item) > 3 else None
        with col:
            kpi_card(label, value, foot, accent)


def prediction_card(commodity: str, where: str, when: str, is_high: bool,
                    probability: float | None) -> None:
    klass = "high" if is_high else "low"
    label = "High Price Stress" if is_high else "Low Price Stress"
    if probability is not None and np.isfinite(probability):
        prob_html = (f"<div class='prob'>{probability * 100:.0f}%</div>"
                     f"<div class='prob-label'>Probability</div>")
    else:
        prob_html = "<div class='prob'>n/a</div><div class='prob-label'>Probability</div>"
    st.markdown(
        f"<div class='zfps-pred {klass}'>"
        f"  <div>"
        f"    <div class='comm'>{html.escape(str(commodity))}</div>"
        f"    <div class='where'>{html.escape(str(where))}</div>"
        f"    <div class='when'>{html.escape(str(when))}</div>"
        f"  </div>"
        f"  <div class='right'>"
        f"    <div class='class {klass}'>{label}</div>"
        f"    {prob_html}"
        f"  </div>"
        f"</div>",
        unsafe_allow_html=True)


def stress_pill(is_high: bool) -> str:
    klass = "high" if is_high else "low"
    label = "High Price Stress" if is_high else "Low Price Stress"
    return f"<span class='zfps-pill {klass}'>{html.escape(label)}</span>"


def info_panel(title: str, rows: list[tuple[str, str]], footer: str = "") -> None:
    body = "".join(
        f"<div class='row'><span class='k'>{html.escape(str(k))}</span>"
        f"<span class='v'>{v}</span></div>" for k, v in rows)
    foot = f"<div class='foot' style='margin-top:8px;color:#98A2B3'>{html.escape(footer)}</div>" if footer else ""
    st.markdown(f"<div class='zfps-panel'><h4 style='margin:0 0 8px 0'>{html.escape(title)}</h4>"
                f"{body}{foot}</div>", unsafe_allow_html=True)


def disclaimer() -> None:
    st.markdown(f"<div class='zfps-disclaimer'>{html.escape(DISCLAIMER)}</div>",
                unsafe_allow_html=True)


def missing_artifact(description: str, command: str | None = None) -> None:
    st.warning(f"{description} is not available.")
    if command:
        st.code(command, language="powershell")


# --------------------------------------------------------------------------------------
# Formatting
# --------------------------------------------------------------------------------------
def fmt_month(value) -> str:
    try:
        return pd.Timestamp(value).strftime("%B %Y")
    except Exception:
        return str(value)


def fmt_pct(value, digits: int = 1) -> str:
    try:
        v = float(value)
        if not np.isfinite(v):
            return "n/a"
        return f"{100 * v:.{digits}f}%"
    except Exception:
        return "n/a"


def fmt_num(value, digits: int = 2) -> str:
    try:
        v = float(value)
        if not np.isfinite(v):
            return "n/a"
        return f"{v:,.{digits}f}"
    except Exception:
        return "n/a"


def kpi_high_stress(df: pd.DataFrame) -> int:
    return int((df["price_stress"] == 1).sum())
