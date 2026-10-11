"""Visual design system and shared styles for the ZCPSC Option B dashboard.

Matches the design specifications from ZCPSC_Dashboard_UI_Pages.pdf and
the Complete ZCPSC Dashboard UI Implementation Prompt.
"""
from __future__ import annotations

import html
import streamlit as st

TITLE = "Zimbabwe Commodity Price Stress Classifier (ZCPSC)"
SUBTITLE = "Machine Learning-Based Prediction of Next-Month Relative Commodity Price Stress in Zimbabwean Districts"
DESCRIPTION = "Option B Predictive System: Information available at month T -> Relative price stress at month T+1."
DISCLAIMER = (
    "Academic decision-support prototype. Not an official food-security assessment, "
    "IPC classification or guaranteed forecast."
)

COLORS = {
    "bg": "#F3F6FA",
    "sidebar": "#102F50",
    "card": "#FFFFFF",
    "border": "#E2E8F0",
    "navy": "#0B2743",
    "navy_light": "#0B2743",
    "text": "#172A40",
    "text_muted": "#748397",
    "text_light": "#748397",
    "primary": "#147BB5",
    "primary_hover": "#0B2743",
    "teal": "#21A99F",
    "teal_light": "#E8F6EF",
    "blue": "#147BB5",
    "blue_light": "#EAF4FC",
    "green": "#199B70",
    "green_light": "#E8F6EF",
    "amber": "#F0B83F",
    "amber_light": "#FFF4D6",
    "red": "#D94343",
    "red_light": "#FCEBEC",
}

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
    --bg-app: #F3F6FA;
    --sidebar-bg: #102F50;
    --sidebar-text: #C8D6E4;
    --sidebar-active: #1676B8;
    --card-bg: #FFFFFF;
    --border-color: #E2E8F0;
    --text-main: #172A40;
    --text-muted: #748397;
    --primary: #147BB5;
    --primary-hover: #0B2743;
}

html, body, [class*="css"], .stApp, button, input, select, textarea {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
}

.stApp {
    background-color: #F3F6FA !important;
}

/* Container constraints to match 1440px target */
.block-container {
    padding-top: 1.8rem !important;
    padding-bottom: 3.5rem !important;
    padding-left: 2.2rem !important;
    padding-right: 2.2rem !important;
    max-width: 1440px !important;
}

/* Hide Streamlit default header decoration */
header[data-testid="stHeader"] {
    background: transparent !important;
}
#MainMenu, footer {
    visibility: hidden !important;
}

/* Sidebar styling to match PDF deep navy */
section[data-testid="stSidebar"] {
    background-color: #102F50 !important;
    min-width: 260px !important;
    max-width: 270px !important;
    border-right: 1px solid #0B2743 !important;
}
section[data-testid="stSidebar"] > div:first-child {
    background-color: #102F50 !important;
}
section[data-testid="stSidebar"] p, 
section[data-testid="stSidebar"] span, 
section[data-testid="stSidebar"] div {
    color: #C8D6E4;
}
section[data-testid="stSidebar"] hr {
    border-color: rgba(255, 255, 255, 0.12) !important;
}

/* Sidebar Navigation Items */
[data-testid="stSidebarNav"],
[data-testid="stSidebarNavItems"] {
    padding-top: 0.2rem !important;
}
[data-testid="stSidebarNav"] ul,
[data-testid="stSidebarNavItems"] ul {
    gap: 4px !important;
    list-style: none !important;
    padding: 0 !important;
}
[data-testid="stSidebarNav"] a,
[data-testid="stSidebarNavLink"],
a[data-testid="stSidebarNavLink"] {
    border-radius: 8px !important;
    padding: 9px 14px !important;
    font-weight: 500 !important;
    font-size: 0.92rem !important;
    color: #C8D6E4 !important;
    background-color: transparent !important;
    text-decoration: none !important;
    display: flex !important;
    align-items: center !important;
    gap: 10px !important;
    transition: all 0.2s ease !important;
}
[data-testid="stSidebarNav"] a:hover,
[data-testid="stSidebarNavLink"]:hover,
a[data-testid="stSidebarNavLink"]:hover {
    background-color: rgba(255, 255, 255, 0.08) !important;
    color: #FFFFFF !important;
}
[data-testid="stSidebarNav"] a[aria-current="page"],
[data-testid="stSidebarNavLink"][aria-current="page"],
a[data-testid="stSidebarNavLink"][aria-current="page"] {
    background-color: #1676B8 !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
}
[data-testid="stSidebarNavLink"] span {
    color: inherit !important;
}
[data-testid="stSidebarNavSeparator"] {
    display: none !important;
}

/* Cards & Containers */
.zcpsc-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 20px 22px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    margin-bottom: 16px;
}

/* KPI Card */
.zcpsc-kpi-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 18px 20px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    display: flex;
    align-items: center;
    gap: 16px;
}
.zcpsc-kpi-icon {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    flex-shrink: 0;
}
.zcpsc-kpi-icon.teal { background: #E8F6EF; color: #21A99F; }
.zcpsc-kpi-icon.blue { background: #EAF4FC; color: #147BB5; }
.zcpsc-kpi-icon.cyan { background: #EAF4FC; color: #147BB5; }
.zcpsc-kpi-icon.green { background: #E8F6EF; color: #199B70; }
.zcpsc-kpi-icon.amber { background: #FFF4D6; color: #F0B83F; }
.zcpsc-kpi-icon.red { background: #FCEBEC; color: #D94343; }

.zcpsc-kpi-body {
    display: flex;
    flex-direction: column;
}
.zcpsc-kpi-title {
    font-size: 0.8rem;
    color: #748397;
    font-weight: 500;
    margin-bottom: 2px;
}
.zcpsc-kpi-value {
    font-size: 1.75rem;
    font-weight: 700;
    color: #172A40;
    line-height: 1.2;
}

/* Status Badges & Pills */
.zcpsc-pill {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 9999px;
    font-size: 0.8rem;
    font-weight: 600;
}
.zcpsc-pill.high {
    background: #FCEBEC;
    color: #D94343;
    border: 1px solid #D94343;
}
.zcpsc-pill.moderate {
    background: #FFF4D6;
    color: #F0B83F;
    border: 1px solid #F0B83F;
}
.zcpsc-pill.low {
    background: #E8F6EF;
    color: #199B70;
    border: 1px solid #199B70;
}

/* System Workflow Step Card */
.zcpsc-workflow-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 20px 24px;
    margin-top: 14px;
    margin-bottom: 14px;
}
.zcpsc-workflow-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
}
.zcpsc-step-item {
    display: flex;
    align-items: flex-start;
    gap: 14px;
    flex: 1;
}
.zcpsc-step-num {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: #EAF4FC;
    color: #147BB5;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 14px;
    flex-shrink: 0;
}
.zcpsc-step-title {
    font-weight: 700;
    font-size: 0.92rem;
    color: #172A40;
    margin-bottom: 2px;
}
.zcpsc-step-desc {
    font-size: 0.8rem;
    color: #748397;
    line-height: 1.4;
}
.zcpsc-arrow {
    color: #748397;
    font-size: 20px;
    font-weight: bold;
}

/* Disclaimer Banners */
.zcpsc-disclaimer-banner {
    background: #FFF4D6;
    border: 1px solid #F0B83F;
    border-radius: 8px;
    padding: 10px 16px;
    display: flex;
    align-items: center;
    gap: 12px;
    color: #F0B83F;
    font-size: 0.82rem;
    margin-top: 16px;
}

/* Buttons */
.stButton > button {
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 8px 18px !important;
    transition: all 0.15s ease !important;
}
.stButton > button[kind="primary"] {
    background-color: #147BB5 !important;
    border: none !important;
    color: #FFFFFF !important;
}
.stButton > button[kind="primary"]:hover {
    background-color: #0B2743 !important;
}

/* Top Page Header */
.zcpsc-header-title {
    font-size: 1.85rem;
    font-weight: 700;
    color: #172A40;
    letter-spacing: -0.02em;
    margin-bottom: 4px;
}
.zcpsc-header-sub {
    font-size: 0.95rem;
    color: #748397;
    margin-bottom: 18px;
}
</style>
"""


def inject_css() -> None:
    """Inject global CSS stylesheet into page."""
    st.markdown(_CSS, unsafe_allow_html=True)


def sidebar_header() -> None:
    """Renders the top branding inside the sidebar."""
    st.sidebar.markdown(
        """
        <div style="padding: 10px 8px 16px 8px;">
            <div style="display:flex; align-items:center; gap:10px;">
                <div style="background:#21A99F; color:#FFFFFF; width:34px; height:34px; border-radius:8px; display:flex; align-items:center; justify-content:center; font-weight:700; font-size:16px;">
                    Z
                </div>
                <div>
                    <div style="color:#FFFFFF; font-weight:700; font-size:1.15rem; letter-spacing:-0.01em;">ZCPSC</div>
                    <div style="color:#C8D6E4; font-size:0.72rem; line-height:1.2;">Zimbabwe Commodity Price<br>Stress Classifier</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def sidebar_footer() -> None:
    """Renders the bottom branding inside the sidebar."""
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        """
        <div style="padding: 4px 8px; color:#748397; font-size:0.75rem; line-height:1.4;">
            <div style="color:#21A99F; font-weight:600; margin-bottom:4px;">Option B • Horizon T+1</div>
            <div>Research for a more food-secure Zimbabwe</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def page_header(title: str, subtitle: str) -> None:
    """Renders the standard page header."""
    st.markdown(
        f"""
        <div>
            <div class="zcpsc-header-title">{html.escape(title)}</div>
            <div class="zcpsc-header-sub">{html.escape(subtitle)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def disclaimer_banner(text: str = DISCLAIMER) -> None:
    """Renders the amber disclaimer banner."""
    st.markdown(
        f"""
        <div class="zcpsc-disclaimer-banner">
            <span style="font-size:16px;">⚠️</span>
            <span>{html.escape(text)}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
