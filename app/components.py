"""Reusable UI components for the ZCPSC Option B dashboard.

Matches the design specifications from ZCPSC_Dashboard_UI_Pages.pdf and
the Complete ZCPSC Dashboard UI Implementation Prompt.
"""
from __future__ import annotations

import html
import textwrap
import streamlit as st
import numpy as np


def render_html(raw_html: str) -> None:
    """Render HTML safely without indentation causing markdown code blocks.

    Blank lines terminate a CommonMark HTML block, so any following indented
    line is parsed as an indented code block and shown as literal markup.
    Dropping blank lines keeps the whole snippet inside one HTML block.
    """
    text = textwrap.dedent(raw_html).strip()
    lines = [line.rstrip() for line in text.splitlines() if line.strip()]
    st.markdown("\n".join(lines), unsafe_allow_html=True)


def kpi_card(title: str, value: str | int, icon: str = "📊", color: str = "blue") -> None:
    """Render a modern KPI card with a circular colored icon on the left."""
    render_html(f"""
    <div class="zcpsc-kpi-card">
        <div class="zcpsc-kpi-icon {color}">
            <span>{icon}</span>
        </div>
        <div class="zcpsc-kpi-body">
            <div class="zcpsc-kpi-title">{html.escape(title)}</div>
            <div class="zcpsc-kpi-value">{html.escape(str(value))}</div>
        </div>
    </div>
    """)


def prediction_summary_card(high_count: int, mod_count: int, low_count: int, total_districts: int) -> None:
    """Render the Recent Prediction Summary card on Overview matching PDF Page 1."""
    render_html(f"""
    <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:12px; padding:20px; box-shadow:0 1px 3px rgba(0,0,0,0.04); height:100%; display:flex; flex-direction:column; justify-content:space-between;">
        <div>
            <div style="font-size:1.1rem; font-weight:700; color:#172A40; margin-bottom:2px;">Recent prediction summary</div>
            <div style="font-size:0.83rem; color:#748397; margin-bottom:20px;">Number of districts in each predicted stress category for next month.</div>
            
            <div style="background:#F3F6FA; border:1px solid #E2E8F0; border-radius:10px; padding:12px 18px; margin-bottom:12px; display:flex; justify-content:space-between; align-items:center;">
                <div style="background:#FCEBEC; color:#D94343; border:1px solid #D94343; padding:4px 14px; border-radius:999px; font-weight:600; font-size:0.82rem;">
                    High probability
                </div>
                <div style="font-size:1.9rem; font-weight:800; color:#D94343; line-height:1;">
                    {high_count}
                </div>
            </div>

            <div style="background:#F3F6FA; border:1px solid #E2E8F0; border-radius:10px; padding:12px 18px; margin-bottom:12px; display:flex; justify-content:space-between; align-items:center;">
                <div style="background:#FFF4D6; color:#F0B83F; border:1px solid #F0B83F; padding:4px 14px; border-radius:999px; font-weight:600; font-size:0.82rem;">
                    Moderate probability
                </div>
                <div style="font-size:1.9rem; font-weight:800; color:#F0B83F; line-height:1;">
                    {mod_count}
                </div>
            </div>

            <div style="background:#F3F6FA; border:1px solid #E2E8F0; border-radius:10px; padding:12px 18px; margin-bottom:16px; display:flex; justify-content:space-between; align-items:center;">
                <div style="background:#E8F6EF; color:#199B70; border:1px solid #199B70; padding:4px 14px; border-radius:999px; font-weight:600; font-size:0.82rem;">
                    Lower probability
                </div>
                <div style="font-size:1.9rem; font-weight:800; color:#21A99F; line-height:1;">
                    {low_count}
                </div>
            </div>
        </div>

        <div style="font-size:0.78rem; color:#748397; margin-top:14px; border-top:1px solid #E2E8F0; padding-top:10px;">
            Out of {total_districts} monitored districts.
        </div>
    </div>
    """)


def workflow_steps(steps: list[tuple[int, str, str]]) -> None:
    """Render the 3-step 'How the system works' card with numbered circles and arrows."""
    items_html = []
    for idx, (num, title, desc) in enumerate(steps):
        step_html = f"""
        <div class="zcpsc-step-item">
            <div class="zcpsc-step-num">{num}</div>
            <div>
                <div class="zcpsc-step-title">{html.escape(title)}</div>
                <div class="zcpsc-step-desc">{html.escape(desc)}</div>
            </div>
        </div>
        """
        items_html.append(step_html)
        if idx < len(steps) - 1:
            items_html.append('<div class="zcpsc-arrow">→</div>')

    inner_html = "".join(items_html)
    render_html(f"""
    <div class="zcpsc-workflow-card">
        <div style="font-size:1.05rem; font-weight:700; color:#172A40; margin-bottom:4px;">How the system works</div>
        <div style="font-size:0.82rem; color:#748397; margin-bottom:16px;">A simple three-step workflow from input to insight.</div>
        <div class="zcpsc-workflow-row">
            {inner_html}
        </div>
    </div>
    """)


def probability_meter(prob: float) -> None:
    """Renders a horizontal probability meter bar: Low | Moderate | High with marker."""
    pct = max(0.0, min(100.0, prob * 100))
    render_html(f"""
    <div style="margin: 14px 0 10px 0;">
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; color:#748397; margin-bottom:6px; font-weight:600;">
            <span>Low</span>
            <span>Moderate</span>
            <span>High</span>
        </div>
        <div style="position:relative; width:100%; height:10px; background:linear-gradient(to right, #199B70 0%, #F0B83F 50%, #D94343 100%); border-radius:999px;">
            <div style="position:absolute; top:-3px; left:calc({pct}% - 4px); width:8px; height:16px; background:#0B2743; border-radius:2px; border:1px solid #FFFFFF;"></div>
        </div>
    </div>
    """)
