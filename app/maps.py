"""Static Zimbabwe district choropleth for the ZFPS dashboard.

Why this is no longer Plotly
----------------------------
The original map used ``plotly.express.choropleth`` with a categorical colour column, which
builds *one trace per category* and paints the whole country with the last trace's colour (the
solid red rectangle). A single ``go.Choropleth`` trace over a custom GeoJSON was tried as a
fix, but in this environment Plotly's custom-GeoJSON matching is unreliable and every trace
collapses to a single fill colour. To guarantee correct per-district colouring we render the
map with **GeoPandas + Matplotlib** and display the resulting figure with ``st.pyplot``.

Colour system (exact):

    Low Price Stress  -> #2E8B57  (green)
    High Price Stress -> #D92D20  (red)
    No Data           -> #D0D5DD  (grey)

The probability mode uses a blue sequential scale only; red is reserved for High Price Stress.
"""
from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap, Normalize, to_rgba  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from styles import COLORS  # noqa: E402

LOW = "Low Price Stress"
HIGH = "High Price Stress"
NODATA = "No Data"

_CLASS_COLOR = {LOW: COLORS["low"], HIGH: COLORS["high"], NODATA: COLORS["nodata"]}
_PROB_CMAP = LinearSegmentedColormap.from_list(
    "zfps_prob", ["#DBEAFE", "#60A5FA", "#1D4ED8"])


def _figure(height: int = 560):
    h_in = max(height, 280) / 92.0
    fig = plt.figure(figsize=(h_in * 1.44, h_in), dpi=150)
    fig.patch.set_facecolor(COLORS["map_bg"])
    return fig


def _empty(message: str, height: int = 560):
    fig = _figure(height)
    fig.text(0.5, 0.5, message, ha="center", va="center",
             color=COLORS["muted"], fontsize=12)
    return fig


def stress_map(gdf, frame: pd.DataFrame | None = None, mode: str = "class",
               height: int = 560, show_legend: bool = True):
    """Render the district price-stress map and return a Matplotlib ``Figure``.

    Parameters
    ----------
    gdf : geopandas.GeoDataFrame
        ADM2 boundaries with a ``district_key`` column (see ``data_loader.load_geo``).
    frame : one row per district, optionally containing ``predicted_label`` and
        ``probability``. Districts absent from ``frame`` are shown as *No Data*.
    mode : ``"class"`` (discrete Low/High/No Data) or ``"probability"`` (blue scale).
    """
    if gdf is None or getattr(gdf, "empty", True) or "geometry" not in getattr(gdf, "columns", []):
        return _empty("District boundaries are unavailable. Run the pipeline first.", height)

    base = gdf[["district_key", "geometry"]].copy()

    if frame is not None and not frame.empty and "district_key" in frame.columns:
        f = frame.drop_duplicates("district_key", keep="first")
        keep = [c for c in ("predicted_label", "probability") if c in f.columns]
        if keep:
            base = base.merge(f[["district_key", *keep]], on="district_key", how="left")

    prob_mode = mode == "probability" and "probability" in base.columns

    if prob_mode:
        vals = base["probability"].astype(float)
        norm = Normalize(vmin=0.0, vmax=1.0)
        base["_color"] = [
            _PROB_CMAP(norm(v)) if np.isfinite(v) else to_rgba(COLORS["nodata"])
            for v in vals]
    else:
        if "predicted_label" in base.columns:
            labels = base["predicted_label"].fillna(NODATA)
        else:
            labels = pd.Series([NODATA] * len(base), index=base.index)
        base["_color"] = [to_rgba(_CLASS_COLOR.get(lab, COLORS["nodata"])) for lab in labels]

    fig = _figure(height)
    ax = fig.add_axes([0.01, 0.02, 0.98, 0.96])
    ax.set_facecolor(COLORS["map_bg"])
    base.plot(color=list(base["_color"]), edgecolor=COLORS["district_border"],
              linewidth=0.6, ax=ax)
    ax.set_axis_off()
    ax.set_aspect("equal")

    minx, miny, maxx, maxy = base.total_bounds
    padx = max((maxx - minx) * 0.02, 0.05)
    pady = max((maxy - miny) * 0.02, 0.05)
    ax.set_xlim(minx - padx, maxx + padx)
    ax.set_ylim(miny - pady, maxy + pady)

    if show_legend:
        if prob_mode:
            sm = plt.cm.ScalarMappable(cmap=_PROB_CMAP, norm=Normalize(0.0, 1.0))
            cbar = fig.colorbar(sm, ax=ax, fraction=0.030, pad=0.015,
                                orientation="horizontal", shrink=0.55)
            cbar.set_label("P(high price stress)", color=COLORS["text2"], fontsize=9)
            cbar.ax.tick_params(labelsize=8, colors=COLORS["text2"], length=0)
            cbar.outline.set_edgecolor(COLORS["border"])
        else:
            handles = [
                Patch(facecolor=_CLASS_COLOR[LOW], edgecolor="white", label=LOW),
                Patch(facecolor=_CLASS_COLOR[HIGH], edgecolor="white", label=HIGH),
                Patch(facecolor=_CLASS_COLOR[NODATA], edgecolor="white", label=NODATA),
            ]
            leg = ax.legend(handles=handles, loc="lower right", frameon=True,
                            fontsize=9, borderpad=0.7, handlelength=1.2,
                            labelspacing=0.55, title=None)
            leg.get_frame().set_facecolor("white")
            leg.get_frame().set_edgecolor(COLORS["border"])
            leg.get_frame().set_alpha(0.95)
            for text in leg.get_texts():
                text.set_color(COLORS["text"])
    return fig


def render_map(gdf, frame: pd.DataFrame | None = None, mode: str = "class",
               height: int = 560, show_legend: bool = True) -> None:
    """Render :func:`stress_map` inside Streamlit and release the figure."""
    import streamlit as st

    fig = stress_map(gdf, frame, mode, height, show_legend)
    st.pyplot(fig)
    plt.close(fig)
