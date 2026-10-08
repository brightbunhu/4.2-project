"""Reusable Plotly chart builders for the ZFPS dashboard.

All charts share the same theme: white surfaces, very light gridlines, the dashboard palette
and the Inter typeface.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from styles import COLORS, STRESS_COLOURS  # noqa: E402

FONT = dict(family="Inter, Segoe UI, Roboto, sans-serif", color=COLORS["text"], size=12)
PALETTE = [COLORS["accent"], COLORS["secondary"], COLORS["rain"], COLORS["warning"],
           COLORS["low"], COLORS["high"]]
LABELS = ["Low Price Stress", "High Price Stress"]


def _theme(fig: go.Figure, height: int = 360, title: str | None = None) -> go.Figure:
    fig.update_layout(
        template="plotly_white",
        height=height,
        font=FONT,
        title=dict(text=title, font=dict(size=15, color=COLORS["text"])) if title else None,
        margin=dict(l=10, r=10, t=50 if title else 18, b=10),
        paper_bgcolor=COLORS["card"],
        plot_bgcolor=COLORS["card"],
        colorway=PALETTE,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0, bgcolor="rgba(0,0,0,0)"),
        hoverlabel=dict(bgcolor="white", bordercolor=COLORS["border"],
                        font=dict(color=COLORS["text"])),
    )
    fig.update_xaxes(showgrid=False, linecolor=COLORS["border"], zeroline=False,
                     tickfont=dict(color=COLORS["text2"]))
    fig.update_yaxes(showgrid=True, gridcolor=COLORS["border"], zeroline=False,
                     tickfont=dict(color=COLORS["text2"]))
    return fig


def _empty(message: str, height: int = 320) -> go.Figure:
    fig = go.Figure()
    fig.add_annotation(text=message, showarrow=False, x=0.5, y=0.5, xref="paper", yref="paper",
                       font=dict(size=14, color=COLORS["muted"]))
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    return _theme(fig, height)


# --------------------------------------------------------------------------------------
# Price / rainfall
# --------------------------------------------------------------------------------------
def price_history(sub: pd.DataFrame) -> go.Figure:
    s = sub.sort_values("month")
    fig = go.Figure(go.Scatter(x=s["month"], y=s["spatial_price_index"], mode="lines+markers",
                               name="Spatial Price Index", line=dict(color=COLORS["accent"])))
    fig.add_hline(y=1.0, line_dash="dash", line_color=COLORS["high"],
                  annotation_text="Stress threshold (SPI = 1.0)", annotation_position="top left",
                  annotation_font=dict(color=COLORS["high"], size=11))
    fig.update_yaxes(title_text="Spatial Price Index")
    fig.update_xaxes(title_text="Month")
    return _theme(fig, 360)


def raw_price_history(sub: pd.DataFrame, currency: str) -> go.Figure:
    s = sub[sub["currency_code"] == currency].sort_values("month")
    fig = go.Figure()
    if not s.empty:
        fig.add_trace(go.Scatter(x=s["month"], y=s["price"], mode="lines+markers",
                                 name=f"Price ({currency})", line=dict(color=COLORS["secondary"])))
    fig.update_yaxes(title_text=f"Price ({currency})")
    fig.update_xaxes(title_text="Month")
    return _theme(fig, 320, f"Observed price in {currency}")


def rainfall_history(rain_df: pd.DataFrame) -> go.Figure:
    s = rain_df.sort_values("month")
    fig = go.Figure()
    fig.add_trace(go.Bar(x=s["month"], y=s["rainfall_mm"], name="Monthly rainfall",
                         marker_color=COLORS["rain"]))
    if "rain_lta" in s.columns:
        fig.add_trace(go.Scatter(x=s["month"], y=s["rain_lta"], mode="lines",
                                 name="Long-term average",
                                 line=dict(color=COLORS["warning"], width=2)))
    fig.update_yaxes(title_text="Rainfall (mm)")
    fig.update_xaxes(title_text="Month")
    return _theme(fig, 340)


def rainfall_anomaly(rain_df: pd.DataFrame) -> go.Figure:
    s = rain_df.sort_values("month").copy()
    s["direction"] = s["rain_anom_pct"] >= 0
    fig = go.Figure(go.Bar(
        x=s["month"], y=s["rain_anom_pct"],
        marker_color=[COLORS["low"] if d else COLORS["warning"] for d in s["direction"]],
        name="Anomaly"))
    fig.add_hline(y=0, line_color=COLORS["muted"], line_width=1)
    fig.update_yaxes(title_text="Rainfall anomaly (% of baseline)")
    fig.update_xaxes(title_text="Month")
    return _theme(fig, 300)


def rainfall_rolling(rain_df: pd.DataFrame) -> go.Figure:
    s = rain_df.sort_values("month")
    specs = [("rainfall_3m_total", "3-month", "#66B2D6"),
             ("rainfall_6m_total", "6-month", COLORS["rain"]),
             ("rainfall_12m_total", "12-month", COLORS["secondary"])]
    fig = go.Figure()
    for col, label, colour in specs:
        if col in s.columns:
            fig.add_trace(go.Scatter(x=s["month"], y=s[col], mode="lines", name=label,
                                     line=dict(color=colour)))
    fig.update_yaxes(title_text="Rainfall (mm)")
    fig.update_xaxes(title_text="Month")
    return _theme(fig, 320)


def probability_history(sub: pd.DataFrame, model_key: str) -> go.Figure:
    s = sub.sort_values("month")
    col = f"{model_key}_proba"
    fig = go.Figure()
    if col in s.columns:
        fig.add_trace(go.Scatter(x=s["month"], y=s[col], mode="lines+markers",
                                 name="P(price stress)", line=dict(color=COLORS["accent"])))
    fig.add_hline(y=0.5, line_dash="dash", line_color=COLORS["muted"],
                  annotation_text="Decision threshold (0.5)",
                  annotation_font=dict(color=COLORS["text2"], size=11))
    fig.update_yaxes(title_text="P(price stress)", range=[0, 1])
    fig.update_xaxes(title_text="Month")
    return _theme(fig, 340)


# --------------------------------------------------------------------------------------
# Home-page visuals
# --------------------------------------------------------------------------------------
def stress_donut(df: pd.DataFrame) -> go.Figure:
    counts = df["price_stress"].value_counts().reindex([0, 1], fill_value=0)
    fig = go.Figure(go.Pie(
        labels=LABELS, values=[counts.get(0, 0), counts.get(1, 0)], hole=0.62,
        marker=dict(colors=[COLORS["low"], COLORS["high"]],
                    line=dict(color=COLORS["card"], width=2)),
        textinfo="percent", textfont=dict(color="white", size=12),
        hovertemplate="%{label}<br>%{value:,} observations (%{percent})<extra></extra>",
        sort=False))
    total = int(counts.sum())
    high = int(counts.get(1, 0))
    pct = 100 * high / total if total else 0
    fig.add_annotation(text=f"<b>{total:,}</b><br><span style='font-size:11px;color:#667085'>"
                            f"observations</span>", showarrow=False,
                       font=dict(size=20, color=COLORS["text"]))
    fig.update_layout(showlegend=True, annotations=[dict(text=f"<b>{total:,}</b><br>"
                       f"<span style='font-size:11px;color:#667085'>high-stress {pct:.0f}%</span>",
                       showarrow=False, font=dict(size=16, color=COLORS["text"]))])
    return _theme(fig, 320)


def stress_trend(df: pd.DataFrame) -> go.Figure:
    g = df.groupby(df["month"].dt.to_period("M"))["price_stress"].mean().sort_index()
    x = g.index.to_timestamp()
    fig = go.Figure(go.Scatter(x=x, y=g.values * 100, mode="lines+markers",
                               line=dict(color=COLORS["accent"], width=2),
                               marker=dict(size=5, color=COLORS["accent"]),
                               fill="tozeroy", fillcolor="rgba(37,99,235,0.08)",
                               name="% high stress"))
    fig.update_yaxes(title_text="% high price stress", range=[0, 100])
    fig.update_xaxes(title_text="Month")
    return _theme(fig, 320)


def stress_share_bar(df: pd.DataFrame, group_col: str, title: str) -> go.Figure:
    g = (df.groupby(group_col)["price_stress"].mean().mul(100)
         .sort_values().reset_index(name="stress_pct"))
    fig = go.Figure(go.Bar(x=g["stress_pct"], y=g[group_col], orientation="h",
                           marker_color=COLORS["accent"], text=g["stress_pct"].round(1),
                           textposition="auto"))
    fig.update_xaxes(title_text="% of observations in high price stress")
    return _theme(fig, max(300, 22 * len(g) + 90), title)


# --------------------------------------------------------------------------------------
# Model / explainability visuals
# --------------------------------------------------------------------------------------
def importance_bar(df: pd.DataFrame, value_col: str, err_col: str | None, title: str,
                   top_n: int = 15) -> go.Figure:
    if df.empty:
        return _empty("No importance data available.")
    d = df.dropna(subset=[value_col]).sort_values(value_col, ascending=False).head(top_n)
    d = d.iloc[::-1]
    err = d[err_col] if err_col and err_col in d.columns else None
    fig = go.Figure(go.Bar(
        x=d[value_col], y=d["feature"], orientation="h",
        error_x=dict(type="data", array=err, visible=err is not None) if err is not None else None,
        marker_color=COLORS["accent"]))
    fig.update_xaxes(title_text="Importance")
    return _theme(fig, max(320, 24 * len(d) + 90), title)


def shap_local_bar(contrib: pd.DataFrame, base_value: float | None = None,
                   top_n: int = 12) -> go.Figure:
    if contrib.empty:
        return _empty("No local explanation available.")
    d = contrib.reindex(contrib["shap_value"].abs().sort_values(ascending=False).index)
    d = d.head(top_n).sort_values("shap_value")
    colours = [COLORS["high"] if v >= 0 else COLORS["low"] for v in d["shap_value"]]
    fig = go.Figure(go.Bar(
        x=d["shap_value"], y=d["feature"], orientation="h", marker_color=colours,
        hovertemplate="%{y}<br>SHAP: %{x:.3f}<extra></extra>"))
    fig.add_vline(x=0, line_color=COLORS["muted"], line_width=1)
    title = "Why this prediction? (per-observation SHAP)"
    if base_value is not None and np.isfinite(base_value):
        title += f" \u2014 base log-odds = {base_value:.3f}"
    fig.update_xaxes(title_text="SHAP value (log-odds)")
    return _theme(fig, max(320, 26 * len(d) + 90), title)


def roc_fig(roc_df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode="lines",
                             line=dict(color=COLORS["muted"], dash="dash"), name="Chance"))
    for model, sub in roc_df.groupby("model"):
        sub = sub.sort_values("fpr")
        label = f"{model} (AUC={sub['auc'].iloc[0]:.3f})"
        fig.add_trace(go.Scatter(x=sub["fpr"], y=sub["tpr"], mode="lines", name=label))
    fig.update_xaxes(title_text="False positive rate", range=[0, 1])
    fig.update_yaxes(title_text="True positive rate", range=[0, 1])
    return _theme(fig, 420)


def pr_fig(pr_df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    for model, sub in pr_df.groupby("model"):
        sub = sub.sort_values("recall")
        fig.add_trace(go.Scatter(x=sub["recall"], y=sub["precision"], mode="lines", name=model))
    fig.update_xaxes(title_text="Recall", range=[0, 1])
    fig.update_yaxes(title_text="Precision", range=[0, 1])
    return _theme(fig, 420)


def confusion_heatmap(cm_df: pd.DataFrame, title: str) -> go.Figure:
    z = cm_df[LABELS].to_numpy()
    fig = go.Figure(go.Heatmap(
        z=z, x=LABELS, y=cm_df["actual"].tolist(),
        colorscale=[[0, "#EFF4FE"], [1, COLORS["accent"]]],
        text=z, texttemplate="%{text}", showscale=False,
        hovertemplate="Actual: %{y}<br>Predicted: %{x}<br>Count: %{z}<extra></extra>"))
    fig.update_xaxes(title_text="Predicted class", showgrid=False)
    fig.update_yaxes(title_text="Actual class", autorange="reversed", showgrid=False)
    return _theme(fig, 380, title)


def metric_bar(df: pd.DataFrame, metric: str) -> go.Figure:
    d = df.dropna(subset=[metric]).sort_values(metric)
    fig = go.Figure(go.Bar(x=d[metric], y=d["model"], orientation="h",
                           marker_color=COLORS["secondary"], text=d[metric].round(3),
                           textposition="auto"))
    fig.update_xaxes(title_text=metric)
    return _theme(fig, 260)
