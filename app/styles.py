"""Visual design system and shared strings for the ZFPS dashboard.

The stylesheet is a plain string built on CSS custom properties so that the exact colour
system is defined once (``:root``) and reused throughout. The same palette is mirrored in the
``COLORS`` dict for the Plotly figures.
"""
from __future__ import annotations

TITLE = "Zimbabwe Food Price Stress Classifier"
SUBTITLE = ("Machine Learning Classification of Commodity-Level Food Price Stress in "
            "Zimbabwean Districts Using CHIRPS Rainfall and Market Data")
DESCRIPTION = ("A research proof-of-concept decision-support dashboard integrating market "
               "prices, CHIRPS rainfall and socioeconomic indicators.")
DISCLAIMER = ("This application is a research proof of concept. It is not an official "
              "food-price assessment, government classification, IPC assessment, or "
              "operational early-warning system.")

# Stress is binary by construction: price_stress = 1 if spatial_price_index > 1.0
STRESS_LABELS = {0: "Low Price Stress", 1: "High Price Stress"}
STRESS_COLOURS = {"Low Price Stress": "#2E8B57", "High Price Stress": "#D92D20"}

COLORS = {
    # surfaces
    "bg": "#F7F9FC",
    "sidebar": "#0B2545",
    "map_bg": "#EEF3F8",
    "card": "#FFFFFF",
    "border": "#E5EAF0",
    # navy scale
    "navy": "#0B2545",
    "navy_2": "#12395F",
    # text
    "text": "#172033",
    "text2": "#667085",
    "muted": "#98A2B3",
    # accents
    "accent": "#2563EB",
    "accent_hover": "#1D4ED8",
    "warning": "#F59E0B",
    # semantic
    "low": "#2E8B57",
    "high": "#D92D20",
    "nodata": "#D0D5DD",
    "district_border": "#FFFFFF",
    # chart series
    "rain": "#2E86AB",
    "price": "#12395F",
    "green": "#2E8B57",
    "yellow": "#F59E0B",
    "red": "#D92D20",
    "grey": "#98A2B3",
    "secondary": "#12395F",
}

# Blue sequential scale for the probability map (red is reserved for High Price Stress).
PROB_SCALE = [
    [0.0, "#DBEAFE"],
    [0.5, "#60A5FA"],
    [1.0, "#1D4ED8"],
]

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
    --bg: #F7F9FC;
    --sidebar: #0B2545;
    --map-bg: #EEF3F8;
    --card: #FFFFFF;
    --border: #E5EAF0;
    --navy: #0B2545;
    --navy-2: #12395F;
    --text: #172033;
    --text-2: #667085;
    --muted: #98A2B3;
    --accent: #2563EB;
    --accent-hover: #1D4ED8;
    --warning: #F59E0B;
    --low: #2E8B57;
    --high: #D92D20;
    --nodata: #D0D5DD;
    --shadow: 0 2px 8px rgba(16, 24, 40, 0.05);
}

html, body, [class*="css"], .stApp, button, input, select, textarea {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.stApp { background: var(--bg); }

/* --- layout --- */
.block-container {
    padding: 1.6rem 2.4rem 3rem 2.4rem !important;
    max-width: 1480px;
}
header[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { visibility: hidden; }
[data-testid="stToolbar"] { right: 1rem; }
[data-testid="stDecoration"] { display: none; }

/* --- top navigation bar --- */
div[data-testid="stSegmentedControl"], div[data-testid="stButtonGroup"] {
    margin: 0 0 14px 0;
}
div[data-testid="stSegmentedControl"] button, div[data-testid="stButtonGroup"] button {
    border-radius: 8px !important; font-weight: 600 !important;
}

h1, h2, h3, h4, h5 { color: var(--text); font-weight: 700; letter-spacing: -0.01em; }

/* --- sidebar --- */
section[data-testid="stSidebar"] {
    background: var(--sidebar);
    min-width: 270px; width: 270px; max-width: 270px;
    border-right: none;
    transform: translateX(0) !important;
    margin-left: 0 !important;
    visibility: visible !important;
    display: block !important;
}
section[data-testid="stSidebar"] > div:first-child { background: var(--sidebar); }
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] { padding-top: 1.4rem; }
section[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.12); margin: 14px 4px; }
[data-testid="stSidebarCollapsedControl"],
[data-testid="stSidebarCollapseButton"] { visibility: visible !important; }

.zfps-brand { padding: 4px 8px 10px 8px; }
.zfps-brand .logo { color: #FFFFFF; font-size: 1.5rem; font-weight: 700; letter-spacing: -0.02em; }
.zfps-brand .sub { color: #A9BCD8; font-size: 0.76rem; font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.14em; margin-top: 2px; }

/* nav buttons */
section[data-testid="stSidebar"] div[data-testid="stButton"] > button,
section[data-testid="stSidebar"] .stButton > button {
    width: 100%; justify-content: flex-start; text-align: left;
    background: transparent; color: #D0D9E5; border: 1px solid transparent;
    border-radius: 8px; padding: 9px 12px; margin: 2px 0; font-size: 0.94rem;
    font-weight: 500; transition: background .15s ease, color .15s ease;
    box-shadow: none; cursor: pointer;
}
section[data-testid="stSidebar"] div[data-testid="stButton"] > button p,
section[data-testid="stSidebar"] .stButton > button p {
    text-align: left; width: 100%; margin: 0;
}
section[data-testid="stSidebar"] div[data-testid="stButton"] > button:hover,
section[data-testid="stSidebar"] .stButton > button:hover {
    background: var(--navy-2); color: #FFFFFF; border-color: transparent;
}
section[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="primary"],
section[data-testid="stSidebar"] div[data-testid="stButton"] > button[data-testid="stBaseButton-primary"],
section[data-testid="stSidebar"] .stButton > button[kind="primary"],
section[data-testid="stSidebar"] .stButton > button[data-testid="stBaseButton-primary"] {
    background: var(--accent); color: #FFFFFF; font-weight: 600;
}
section[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="primary"]:hover,
section[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
    background: var(--accent-hover); color: #FFFFFF;
}

.zfps-sidefoot {
    margin-top: 26px; padding: 14px 10px 4px 10px;
    border-top: 1px solid rgba(255,255,255,0.12);
    color: #8FA3BF; font-size: 0.72rem; line-height: 1.5;
}
.zfps-sidefoot .h { color: #C7D4E6; font-weight: 600; font-size: 0.74rem;
    text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px; }
.zfps-sidefoot .warn { color: #E3B341; margin-top: 8px; }

/* --- page headers --- */
.zfps-page-title { color: var(--text); font-size: 2rem; font-weight: 700;
    letter-spacing: -0.02em; margin: 2px 0 2px 0; line-height: 1.15; }
.zfps-page-sub { color: var(--text-2); font-size: 1.0rem; margin: 0 0 6px 0;
    max-width: 900px; line-height: 1.5; }
.zfps-section-title { color: var(--text); font-size: 1.15rem; font-weight: 600; margin: 0 0 2px 0; }
.zfps-section-sub { color: var(--text-2); font-size: 0.86rem; margin: 0 0 8px 0; }

/* --- cards / containers --- */
.zfps-card {
    background: var(--card); border: 1px solid var(--border); border-radius: 12px;
    box-shadow: var(--shadow); padding: 20px; height: 100%;
}
.zfps-kpi .label { color: var(--text-2); font-size: 0.74rem; font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.06em; }
.zfps-kpi .value { color: var(--text); font-size: 1.9rem; font-weight: 700;
    line-height: 1.15; margin-top: 4px; }
.zfps-kpi .foot { color: var(--muted); font-size: 0.75rem; margin-top: 2px; }
.zfps-kpi { border-top: 3px solid var(--accent); }

/* bordered Streamlit containers become cards */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--card);
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    box-shadow: var(--shadow);
    padding: 6px 8px;
}
div[data-testid="stVerticalBlockBorderWrapper"] > div { border: none !important; }

/* --- pills / badges --- */
.zfps-pill { display: inline-block; padding: 4px 12px; border-radius: 999px;
    font-size: 0.8rem; font-weight: 600; color: #FFFFFF; }
.zfps-pill.low { background: var(--low); }
.zfps-pill.high { background: var(--high); }

/* --- prediction card --- */
.zfps-pred {
    background: var(--card); border: 1px solid var(--border); border-radius: 12px;
    box-shadow: var(--shadow); padding: 22px 24px;
    display: flex; justify-content: space-between; align-items: center; gap: 24px;
    border-left: 5px solid var(--muted);
}
.zfps-pred.high { border-left-color: var(--high); }
.zfps-pred.low { border-left-color: var(--low); }
.zfps-pred .comm { color: var(--text); font-size: 1.25rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.02em; }
.zfps-pred .where { color: var(--text-2); font-size: 0.95rem; margin-top: 3px; }
.zfps-pred .when { color: var(--muted); font-size: 0.82rem; margin-top: 1px; }
.zfps-pred .right { text-align: right; }
.zfps-pred .class { font-size: 1.05rem; font-weight: 700; }
.zfps-pred .class.high { color: var(--high); }
.zfps-pred .class.low { color: var(--low); }
.zfps-pred .prob { font-size: 2rem; font-weight: 700; color: var(--text); line-height: 1.1; }
.zfps-pred .prob-label { color: var(--muted); font-size: 0.72rem; text-transform: uppercase;
    letter-spacing: 0.08em; }

/* --- info panel --- */
.zfps-panel { background: var(--card); border: 1px solid var(--border);
    border-radius: 12px; box-shadow: var(--shadow); padding: 18px 20px; }
.zfps-panel .row { display: flex; justify-content: space-between; align-items: center;
    padding: 8px 0; border-bottom: 1px solid var(--border); font-size: 0.9rem; }
.zfps-panel .row:last-child { border-bottom: none; }
.zfps-panel .k { color: var(--text-2); }
.zfps-panel .v { color: var(--text); font-weight: 600; }

/* --- disclaimer --- */
.zfps-disclaimer { background: #FFF8E1; border: 1px solid #FCE9B8;
    border-left: 4px solid var(--warning); color: #6b5200;
    padding: 10px 14px; border-radius: 8px; font-size: 0.84rem; }

/* --- methodology flow --- */
.zfps-flow { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
.zfps-step { background: var(--card); border: 1px solid var(--border); border-radius: 10px;
    box-shadow: var(--shadow); padding: 12px 14px; min-width: 130px; flex: 1; }
.zfps-step .n { color: var(--accent); font-size: 0.78rem; font-weight: 700; }
.zfps-step .t { color: var(--text); font-size: 0.86rem; font-weight: 600; margin-top: 2px; }
.zfps-arrow { color: var(--muted); font-size: 1.1rem; }

/* --- buttons --- */
.stButton > button, .stDownloadButton > button {
    border-radius: 8px; font-weight: 600; border: 1px solid var(--border);
}
.stDownloadButton > button, .stDownloadButton > button:focus {
    background: var(--accent); color: #FFFFFF; border: none;
}
.stDownloadButton > button:hover { background: var(--accent-hover); color: #FFFFFF; }

/* --- widgets --- */
[data-baseweb="select"] > div, .stTextInput input, .stDateInput input {
    border-color: var(--border) !important; border-radius: 8px !important;
}
label, .stSelectbox label, .stMultiSelect label, .stSlider label {
    color: var(--text-2) !important; font-size: 0.82rem !important; font-weight: 600 !important;
}
</style>
"""


def inject_css() -> None:
    """Inject the global stylesheet into the Streamlit page."""
    import streamlit as st
    st.markdown(_CSS, unsafe_allow_html=True)
