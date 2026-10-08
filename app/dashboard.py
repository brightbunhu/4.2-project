"""
Zimbabwe Food Price Stress Classifier (ZFPS)
============================================
Research proof-of-concept Streamlit dashboard.

Run with:
    streamlit run app/dashboard.py

The dashboard only reads artefacts produced by the research pipeline (src/step01..step10).
It never re-runs the CHIRPS ingestion, never retrains models, and never fabricates results.

Presentation layer only: the modelling grain (commodity x district x month), the target
(``price_stress = 1`` when ``spatial_price_index > 1.0``), the validation strategy and every
reported metric come from the pipeline outputs unchanged.
"""
from __future__ import annotations

import sys
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
ROOT = APP_DIR.parent
for _p in (str(ROOT), str(APP_DIR)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import streamlit as st  # noqa: E402

import config as C  # noqa: E402
import charts as ch  # noqa: E402
import components as ui  # noqa: E402
import data_loader as dl  # noqa: E402
import maps  # noqa: E402
import styles  # noqa: E402

st.set_page_config(page_title="Zimbabwe Food Price Stress Classifier",
                   page_icon="\U0001F32D", layout="wide",
                   initial_sidebar_state="expanded")
styles.inject_css()

TARGET = "price_stress"
STRESS_OPTIONS = {"High Price Stress": 1, "Low Price Stress": 0}
ACCENT = styles.COLORS["accent"]


# ======================================================================================
# Shared helpers
# ======================================================================================
def prediction_models(df: pd.DataFrame) -> list[str]:
    """Model keys that produced usable probabilities in the loaded predictions."""
    return [m for m in dl.PREDICTION_MODELS if f"{m}_proba" in df.columns]


def model_label(key: str) -> str:
    return dl.MODEL_LABELS.get(key, key)


def prepare_map_frame(sub: pd.DataFrame, model_key: str | None) -> pd.DataFrame:
    """Add display columns (labels, probability) to a one-row-per-district slice."""
    out = sub.drop_duplicates("district_key", keep="first").copy()
    out["district_label"] = out["district_key"].str.title()
    out["month_label"] = out["month"].dt.strftime("%B %Y")
    out["observed_label"] = np.where(out[TARGET] == 1, "High Price Stress", "Low Price Stress")
    if model_key and f"{model_key}_proba" in out.columns:
        out["probability"] = out[f"{model_key}_proba"]
        out["predicted_label"] = np.where(out[f"{model_key}_pred"] == 1,
                                          "High Price Stress", "Low Price Stress")
    return out


def show_map(gdf, frame: pd.DataFrame, mode: str = "class", height: int = 540) -> None:
    """Render a card-wrapped district map."""
    with st.container(border=True):
        maps.render_map(gdf, frame, mode, height=height)


# ======================================================================================
# Page 1 - Home
# ======================================================================================
def page_home(df: pd.DataFrame) -> None:
    ui.banner()
    st.write("")

    high = ui.kpi_high_stress(df)
    total = len(df)
    ui.kpi_row([
        ("Districts", f"{df['district_key'].nunique():,}", "distinct district_key", ACCENT),
        ("Commodities", f"{df['commodity_name'].nunique():,}", "distinct commodity_name", ACCENT),
        ("Observations", f"{total:,}", "commodity x district x month", ACCENT),
        ("High Price-Stress", f"{high:,}", f"{100 * high / total:.0f}% (SPI > 1.25)",
         styles.COLORS["high"]),
    ])

    st.write("")
    left, right = st.columns([1, 1.5])
    with left:
        with st.container(border=True):
            ui.section_title("Stress balance", "Share of all observations by class")
            st.plotly_chart(ch.stress_donut(df), width="stretch")
    with right:
        with st.container(border=True):
            ui.section_title("High-stress share over time",
                             "Monthly mean of price_stress across the panel")
            st.plotly_chart(ch.stress_trend(df), width="stretch")

    with st.container(border=True):
        ui.section_title("Share of observations in high price stress by province",
                         "Province-level composition of the modelling panel")
        st.plotly_chart(ch.stress_share_bar(df, "province", ""), width="stretch")

    st.write("")
    models = prediction_models(df)
    if not models:
        ui.missing_artifact("A fitted model", "python src/step07_model_training.py")
        ui.disclaimer()
        return

    with st.container(border=True):
        ui.section_title("Latest price-stress classification",
                         "Predicted class from the fitted model. Green = low, red = high "
                         "price stress.")
        f1, f2 = st.columns(2)
        commodities = sorted(df["commodity_name"].dropna().unique())
        default_commodity = df["commodity_name"].value_counts().idxmax()
        with f1:
            commodity = st.selectbox(
                "Commodity", commodities,
                index=commodities.index(default_commodity) if default_commodity in commodities else 0)
        with f2:
            model_key = st.selectbox("Model", models, format_func=model_label)

        cdf = df[df["commodity_name"] == commodity]
        coverage = cdf.groupby("month")["district_key"].nunique()
        threshold = max(3.0, coverage.max() * 0.6)
        broad = coverage[coverage >= threshold]
        latest = broad.index.max() if len(broad) else coverage.index.max()
        months = sorted(cdf["month"].unique())
        month = st.select_slider("Reference month", options=months, value=latest,
                                 format_func=ui.fmt_month)

        sub = cdf[cdf["month"] == month]
        frame = prepare_map_frame(sub, model_key)
        n_high = int((frame.get("predicted_label") == "High Price Stress").sum())
        n_total = len(frame)

        m1, m2, m3 = st.columns(3)
        m1.metric("Districts reporting", f"{n_total:,}")
        m2.metric("Predicted high stress", f"{n_high:,}")
        m3.metric("Predicted low stress", f"{max(n_total - n_high, 0):,}")

        show_map(dl.load_geo(), frame, "class", height=560)
        st.caption(f"{n_total} districts reported **{commodity}** in {ui.fmt_month(month)}; "
                   f"the model predicts high price stress in **{n_high}** of them.")

    st.write("")
    ui.disclaimer()


# ======================================================================================
# Page 2 - Price Stress Map
# ======================================================================================
def page_map(df: pd.DataFrame) -> None:
    ui.page_header("Price Stress Map",
                   "District-level classification of commodity price stress for a chosen "
                   "month.")

    models = prediction_models(df)
    if not models:
        ui.missing_artifact("Fitted models", "python src/step07_model_training.py")
        return

    with st.container(border=True):
        ui.section_title("Filters", "Scope the map by commodity, model, province and month")
        f1, f2, f3, f4 = st.columns([1.2, 1, 1, 1])
        with f1:
            commodity = st.selectbox("Commodity", sorted(df["commodity_name"].unique()))
        with f2:
            model_key = st.selectbox("Model", models, format_func=model_label)
        with f3:
            provinces = ["All provinces"] + sorted(df["province_key"].dropna().unique())
            province = st.selectbox("Province", provinces)
        with f4:
            colour_by = st.radio("Colour by", ["Predicted class", "Probability"],
                                 horizontal=True)

        scope = df[df["commodity_name"] == commodity]
        if province != "All provinces":
            scope = scope[scope["province_key"] == province]

        months = sorted(scope["month"].dropna().unique())
        if not months:
            st.warning("No observations for the current selection.")
            return
        month = st.select_slider("Month", options=months, value=months[-1],
                                 format_func=ui.fmt_month)
        districts = sorted(scope["district_key"].unique())
        chosen = st.multiselect("Districts (leave empty for all)", districts, default=[])

    sub = scope[scope["month"] == month]
    if chosen:
        sub = sub[sub["district_key"].isin(chosen)]

    frame = prepare_map_frame(sub, model_key)
    mode = "class" if colour_by == "Predicted class" else "probability"
    title = (f"{commodity} \u2014 {ui.fmt_month(month)}"
             + (f" ({province.title()})" if province != "All provinces" else ""))

    if frame.empty:
        st.info("No district rows match the current filters.")
        return

    show_map(dl.load_geo(), frame, mode, height=600)

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Districts mapped", f"{len(frame):,}")
    if "predicted_label" in frame.columns:
        k2.metric("Predicted high stress",
                  f"{int((frame['predicted_label'] == 'High Price Stress').sum()):,}")
    else:
        k2.metric("Predicted high stress", "n/a")
    k3.metric("Mean P(price stress)",
              f"{frame['probability'].mean():.2f}" if "probability" in frame else "n/a")
    k4.metric("Reference month", ui.fmt_month(month))
    st.caption(title)


# ======================================================================================
# Page 3 - District & Commodity Detail
# ======================================================================================
def page_detail(df: pd.DataFrame) -> None:
    ui.page_header("District & Commodity Detail",
                   "Observed and predicted price stress for a single district and commodity.")

    models = prediction_models(df)
    with st.container(border=True):
        ui.section_title("Selection", "Choose a district and commodity to profile")
        c1, c2, c3 = st.columns(3)
        with c1:
            provinces = sorted(df["province_key"].dropna().unique())
            province = st.selectbox("Province", provinces)
        pdistricts = sorted(df.loc[df["province_key"] == province, "district_key"].unique())
        with c2:
            district = st.selectbox("District", pdistricts)
        commodity_options = sorted(df.loc[df["district_key"] == district, "commodity_name"].unique())
        with c3:
            commodity = st.selectbox("Commodity", commodity_options)
        model_key = st.selectbox("Model", models, format_func=model_label) if models else None

    sub = df[(df["district_key"] == district) & (df["commodity_name"] == commodity)]
    sub = sub.sort_values("month")
    if sub.empty:
        st.warning("No observations for this district/commodity.")
        return

    ref = sub.iloc[-1]
    proba = ref.get(f"{model_key}_proba", np.nan) if model_key else np.nan
    pred_high = (bool(ref.get(f"{model_key}_pred", ref[TARGET]) == 1)
                 if model_key else bool(ref[TARGET] == 1))

    ui.prediction_card(commodity, f"{district.title()} \u2014 {str(ref['province']).title()}",
                       ui.fmt_month(ref["month"]), pred_high, proba)
    st.write("")

    left, right = st.columns([1, 1.3])
    with left:
        rows = [
            ("Observed price stress", ui.stress_pill(bool(ref[TARGET] == 1))),
            ("Model prediction", ui.stress_pill(pred_high) if model_key else "n/a"),
            ("Probability of price stress",
             ui.fmt_pct(proba) if np.isfinite(proba) else "n/a"),
            ("Spatial price index", ui.fmt_num(ref.get("spatial_price_index", np.nan))),
            ("Observed price", f"{ui.fmt_num(ref.get('price', np.nan))} "
                               f"{ref.get('currency_code', '')}".strip()),
            ("Rainfall (1m)", f"{ui.fmt_num(ref.get('rainfall_1m', np.nan), 1)} mm"),
        ]
        ui.info_panel("Classification summary", rows,
                      footer=None if model_key else
                      "No fitted model available; showing the observed class only.")
    with right:
        with st.container(border=True):
            ui.section_title("Modelled probability over time",
                             "P(price stress) from the selected model")
            if model_key:
                st.plotly_chart(ch.probability_history(sub, model_key), width="stretch")
            else:
                st.info("No fitted model available; only the observed class can be shown.")

    with st.container(border=True):
        ui.section_title("Price history",
                         "The Spatial Price Index is a within-month, within-currency ratio and "
                         "is comparable across the hyperinflation period. Raw prices are per "
                         "currency and are not comparable across currency regimes.")
        st.plotly_chart(ch.price_history(sub), width="stretch")
        currencies = sorted(sub["currency_code"].dropna().unique())
        if currencies:
            cur = st.selectbox("Currency (raw price)", currencies)
            st.plotly_chart(ch.raw_price_history(sub, cur), width="stretch")

    with st.container(border=True):
        ui.section_title("Rainfall analysis", "CHIRPS v3 district rainfall")
        rain_all = dl.load_rainfall_district()
        if rain_all.empty:
            ui.missing_artifact("District rainfall series", "python src/step03_ingest_rainfall.py")
        else:
            rain = rain_all[rain_all["district_key"] == district].sort_values("month")
            if rain.empty:
                st.info("No rainfall series for this district.")
            else:
                st.plotly_chart(ch.rainfall_history(rain), width="stretch")
                st.plotly_chart(ch.rainfall_rolling(rain), width="stretch")
                st.plotly_chart(ch.rainfall_anomaly(rain), width="stretch")

    with st.container(border=True):
        ui.section_title("Model explainability",
                         "Per-observation SHAP for XGBoost; permutation importance otherwise")
        shap_values = dl.load_shap_values()
        shap_base = dl.load_shap_base()
        shap_model_key = "xgboost" if not shap_values.empty else None
        ref_idx = sub.index[-1]

        if model_key is not None and model_key == shap_model_key and ref_idx in shap_values.index:
            row = shap_values.loc[ref_idx]
            contrib = pd.DataFrame({
                "feature": [c[len("shap_"):] for c in row.index],
                "shap_value": row.to_numpy(dtype=float),
            })
            st.caption("SHAP values explain the **XGBoost** prediction for the selected "
                       "observation. Positive values push towards High Price Stress; negative "
                       "values push towards Low Price Stress (log-odds).")
            st.plotly_chart(ch.shap_local_bar(contrib, shap_base), width="stretch")

            pos = (contrib[contrib["shap_value"] > 0]
                   .sort_values("shap_value", ascending=False).head(5)
                   .rename(columns={"feature": "Feature", "shap_value": "SHAP"}))
            neg = (contrib[contrib["shap_value"] < 0]
                   .sort_values("shap_value").head(5)
                   .rename(columns={"feature": "Feature", "shap_value": "SHAP"}))
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Features increasing price-stress**")
                st.dataframe(pos.round(4), hide_index=True)
            with c2:
                st.markdown("**Features decreasing price-stress**")
                st.dataframe(neg.round(4), hide_index=True)
        else:
            if shap_model_key is not None and model_key is not None:
                st.info(f"Per-observation SHAP explanation is available for the "
                        f"**{model_label(shap_model_key)}** model. The selected model "
                        f"(**{model_label(model_key)}**) is shown with global permutation "
                        f"importance below.")
            else:
                st.info("Per-observation SHAP explanation is unavailable; showing global "
                        "**Permutation Feature Importance** instead (a global, not "
                        "per-observation, measure).")
            imp = dl.read_result("step09_permutation_importance.csv")
            if imp.empty:
                ui.missing_artifact("Feature importance", "python src/step09_explainability.py")
            else:
                st.plotly_chart(ch.importance_bar(imp, "importance_mean", "importance_std",
                                                  "Permutation Feature Importance (global)"),
                                width="stretch")

    with st.expander("Feature values for the reference observation"):
        feats = dl.load_selected_features()
        cols = [c for c in feats if c in ref.index]
        st.dataframe(pd.DataFrame({"Feature": cols, "Value": [ref[c] for c in cols]}),
                     hide_index=True)


# ======================================================================================
# Page 4 - Model Insights
# ======================================================================================
IMPORTANCE_LABELS = {
    "shap": "SHAP (mean |value|, XGBoost)",
    "permutation": "Permutation Importance",
    "mutual_info": "Mutual Information (feature selection)",
    "model": "Model Importance (XGBoost native)",
}


def page_insights(df: pd.DataFrame) -> None:
    ui.page_header("Model Insights",
                   "Held-out evaluation, cross-validation and feature importance.")

    metrics = dl.read_result("step08_metrics_full.csv")

    with st.container(border=True):
        ui.section_title("Held-out test performance", "Read from step08_metrics_full.csv")
        if metrics.empty:
            ui.missing_artifact("Held-out evaluation results",
                                "python src/step08_model_evaluation.py")
        else:
            view = metrics.copy()
            view["model"] = view["model"].map(model_label)
            metric_cols = [c for c in ["accuracy", "balanced_accuracy", "macro_f1",
                                       "roc_auc", "pr_auc", "brier"] if c in view.columns]
            st.dataframe(view.set_index("model")[metric_cols].round(4), width="stretch")
            sel_metric = st.selectbox("Compare metric", metric_cols)
            plot_df = metrics.assign(model=metrics["model"].map(model_label))
            st.plotly_chart(ch.metric_bar(plot_df, sel_metric), width="stretch")

    with st.container(border=True):
        ui.section_title("Cross-validation",
                         "GroupKFold by district is the primary, leakage-aware validation.")
        cv = dl.read_result("step07_cv_results.csv")
        if cv.empty:
            ui.missing_artifact("Cross-validation results",
                                "python src/step07_model_training.py")
        else:
            agg = (cv.groupby(["cv", "model"])[["balanced_accuracy", "macro_f1", "roc_auc"]]
                   .agg(["mean", "std"]).round(4))
            st.dataframe(agg, width="stretch")
            st.caption("**GroupKFold by district** keeps every district in a single fold. "
                       "**StratifiedKFold** is a random reference and is more optimistic. "
                       "Neither proves future forecasting performance.")

    with st.container(border=True):
        ui.section_title("Confusion matrix", "Held-out test set")
        cm_models = [m for m in ["xgboost", "logreg", "dummy"]
                     if (C.OUT_RES / f"step08_confusion_{m}.csv").exists()]
        if not cm_models:
            ui.missing_artifact("Confusion matrices", "python src/step08_model_evaluation.py")
        else:
            cm_model = st.selectbox("Model", cm_models, format_func=model_label)
            cm = dl.read_result(f"step08_confusion_{cm_model}.csv")
            st.plotly_chart(ch.confusion_heatmap(cm, f"Confusion matrix \u2014 "
                                                f"{model_label(cm_model)}"),
                            width="stretch")

    with st.container(border=True):
        ui.section_title("ROC and precision\u2013recall curves", "Held-out test set")
        roc = dl.read_result("step08_roc_curves.csv")
        pr = dl.read_result("step08_pr_curves.csv")
        if roc.empty:
            ui.missing_artifact("ROC curve data", "python src/step08_model_evaluation.py")
        else:
            roc = roc.assign(model=roc["model"].map(model_label))
            st.plotly_chart(ch.roc_fig(roc), width="stretch")
        if not pr.empty:
            pr = pr.assign(model=pr["model"].map(model_label))
            st.plotly_chart(ch.pr_fig(pr), width="stretch")

    with st.container(border=True):
        ui.section_title("Global feature importance", "Choose a method")
        methods = dl.available_importance_methods()
        if not methods:
            ui.missing_artifact("Feature importance outputs",
                                "python src/step09_explainability.py")
        else:
            method = st.selectbox("Importance method", methods,
                                  format_func=lambda m: IMPORTANCE_LABELS.get(m, m))
            imp = dl.load_model_importance(method)
            if method == "mutual_info" and "mutual_info" in imp.columns:
                imp = imp.rename(columns={"mutual_info": "importance_mean"})
                imp["importance_std"] = 0.0
            st.plotly_chart(ch.importance_bar(imp, "importance_mean",
                                              "importance_std" if "importance_std" in imp else None,
                                              IMPORTANCE_LABELS.get(method, method)),
                            width="stretch")
            if method == "permutation":
                st.caption("Permutation importance measures the drop in balanced accuracy when "
                           "a feature is shuffled. It is **not** SHAP.")


# ======================================================================================
# Page 5 - Data Explorer
# ======================================================================================
EXPLORER_DEFAULT_COLS = [
    "month", "province", "district_key", "commodity_name", "price", "spatial_price_index",
    "spi_pct_change_3m", "rainfall_1m", "rainfall_3m_anomaly", "price_stress",
]


def page_explorer(df: pd.DataFrame) -> None:
    ui.page_header("Data Explorer",
                   "Filter and download the commodity-level training table.")

    with st.container(border=True):
        ui.section_title("Filters", "Scope the training table")
        f1, f2, f3 = st.columns(3)
        with f1:
            prov = st.multiselect("Province", sorted(df["province_key"].unique()), default=[])
        with f2:
            dist = st.multiselect("District", sorted(df["district_key"].unique()), default=[])
        with f3:
            comm = st.multiselect("Commodity", sorted(df["commodity_name"].unique()), default=[])

        d1, d2, d3 = st.columns(3)
        min_m, max_m = df["month"].min().date(), df["month"].max().date()
        with d1:
            start = st.date_input("From", value=min_m, min_value=min_m, max_value=max_m)
        with d2:
            end = st.date_input("To", value=max_m, min_value=min_m, max_value=max_m)
        with d3:
            stress = st.selectbox("Price stress",
                                  ["All", "High Price Stress", "Low Price Stress"])

    out = df.copy()
    if prov:
        out = out[out["province_key"].isin(prov)]
    if dist:
        out = out[out["district_key"].isin(dist)]
    if comm:
        out = out[out["commodity_name"].isin(comm)]
    out = out[(out["month"].dt.date >= start) & (out["month"].dt.date <= end)]
    if stress != "All":
        out = out[out[TARGET] == STRESS_OPTIONS[stress]]

    st.caption(f"{len(out):,} of {len(df):,} rows match the filters "
               f"({ui.fmt_pct(out[TARGET].mean() if len(out) else np.nan)} high price stress).")

    with st.container(border=True):
        default_cols = [c for c in EXPLORER_DEFAULT_COLS if c in out.columns]
        cols = st.multiselect("Columns to display", list(out.columns), default=default_cols)
        view = out[cols] if cols else out
        st.dataframe(view, hide_index=True, height=460)

    st.download_button("Download filtered data as CSV",
                       data=out.to_csv(index=False).encode("utf-8"),
                       file_name="zfps_filtered_data.csv", mime="text/csv",
                       width="stretch")


# ======================================================================================
# Page 6 - Methodology
# ======================================================================================
def _flow(steps: list[str]) -> str:
    parts = []
    for i, step in enumerate(steps):
        parts.append(f"<div class='zfps-step'><div class='n'>{i + 1:02d}</div>"
                     f"<div class='t'>{step}</div></div>")
        if i < len(steps) - 1:
            parts.append("<div class='zfps-arrow'>&rarr;</div>")
    return f"<div class='zfps-flow'>{''.join(parts)}</div>"


def page_methodology(_df: pd.DataFrame | None = None) -> None:
    ui.page_header("Methodology", "Reproducible pipeline behind the classifier.")

    with st.container(border=True):
        ui.section_title("Pipeline", "Ten reproducible steps (src/step01..step10)")
        st.markdown(_flow(["Data Audit", "Preprocessing", "CHIRPS Rainfall", "Training Table",
                           "EDA", "Feature Selection", "Model Training", "Evaluation",
                           "Explainability", "Dashboard"]),
                    unsafe_allow_html=True)

    with st.container(border=True):
        ui.section_title("Modelling unit and target", "Commodity x District x Month")
        st.markdown("**Commodity x District x Month** \u2014 each row is one commodity observed "
                    "in one district in one month.")
        st.code("price_stress = 1 if spatial_price_index > 1.0\nprice_stress = 0 otherwise",
                language="text")
        st.caption("The spatial price index is the price divided by the national median price of "
                   "the same commodity in the same month and currency (a within-month ratio, so "
                   "inflation and the 2024 redenomination cancel out).")

    with st.container(border=True):
        ui.section_title("Validation strategy", "Leakage-aware primary; random reference")
        st.markdown("- **Primary:** GroupKFold by district (leakage-aware).\n"
                    "- **Reference:** StratifiedKFold (random, more optimistic).")

    with st.container(border=True):
        ui.section_title("Data sources", "Raw inputs preserved under data/raw")
        registry = dl.dataset_registry()
        if registry:
            rows = [{"Source": d.get("title", d.get("key")), "Publisher": d.get("publisher", ""),
                     "Grain": d.get("unit", ""), "Span": d.get("temporal_span", "")}
                    for d in registry]
            rows.append({"Source": "CHIRPS v3 monthly rainfall", "Publisher": "UCSB CHC",
                         "Grain": "grid 0.05\u00b0 -> district x month", "Span": "1981\u2013present"})
            st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")
        else:
            st.info("Dataset registry unavailable in config.py.")

    with st.expander("Documented assumptions & deviations"):
        for a in getattr(C, "ASSUMPTIONS", []):
            st.markdown(f"**{a['id']} \u2014 {a['topic']}**")
            st.markdown(f"- *Observed:* {a['observed']}")
            st.markdown(f"- *Decision:* {a['decision']}")


# ======================================================================================
# Page 7 - About / Limitations
# ======================================================================================
def page_about(_df: pd.DataFrame | None = None) -> None:
    ui.page_header("About / Limitations")

    with st.container(border=True):
        ui.section_title("Purpose")
        st.markdown("This dashboard is a research prototype demonstrating how machine learning "
                    "can classify **commodity-level food price stress** from market prices, "
                    "CHIRPS rainfall and socioeconomic indicators. It is a decision-support "
                    "proof of concept, not an operational assessment product.")
        ui.disclaimer()

    with st.container(border=True):
        ui.section_title("Intended users")
        st.markdown("Researchers, government analysts, humanitarian organisations, "
                    "food-security analysts and agricultural planners. No official "
                    "institutional adoption is claimed or implied.")

    with st.container(border=True):
        ui.section_title("Limitations")
        limitations = [
            "**Commodity-level, not household-level.** The unit is a commodity\u2013district\u2013"
            "month market observation, so results do not describe household food insecurity.",
            "**Classification, not forecasting.** Models classify observed price stress; they do "
            "not predict future stress.",
            "**Poverty is province-level and time-invariant** (latest survey wave), so it cannot "
            "capture within-province or temporal poverty variation.",
            "**Rainfall is district-level from CHIRPS** (satellite + gauge estimate); very small "
            "districts are represented by few grid cells.",
            "**Market coverage is uneven.** Some districts have sparse or no price observations, "
            "and the panel is unbalanced across commodities and months.",
            "**Spatial price index limitations.** The target depends on a within-month, "
            "within-currency median ratio; thin markets can make the national reference noisy.",
            "**Validation limitations.** GroupKFold by district reduces spatial leakage but does "
            "not remove temporal autocorrelation and does not prove future generalisation.",
            "**Observed vs predicted.** Observed and model-predicted price stress are distinct; "
            "the dashboard labels them separately.",
        ]
        for item in limitations:
            st.markdown(f"- {item}")

    with st.container(border=True):
        ui.section_title("Reproduce the underlying results")
        st.code("python -m src.run_all", language="powershell")


# ======================================================================================
# Router
# ======================================================================================
PAGES = {
    "Home": page_home,
    "Price Stress Map": page_map,
    "District & Commodity Detail": page_detail,
    "Model Insights": page_insights,
    "Data Explorer": page_explorer,
    "Methodology": page_methodology,
    "About / Limitations": page_about,
}


def sidebar_nav() -> str:
    """Sidebar-only navigation with clickable buttons; returns the selected page."""
    pages = list(PAGES)
    if "page" not in st.session_state or st.session_state.page not in pages:
        st.session_state.page = pages[0]

    ui.sidebar_brand()
    st.sidebar.markdown("---")

    for name in pages:
        active = st.session_state.page == name
        if st.sidebar.button(
            name, key=f"nav_{name}", width="stretch",
            type="primary" if active else "secondary",
        ):
            st.session_state.page = name
            st.rerun()

    st.sidebar.markdown("---")
    ui.sidebar_footer()
    return st.session_state.page


def main() -> None:
    choice = sidebar_nav()

    df = dl.load_predictions()
    if df.empty:
        st.error("The commodity training table could not be loaded. Run the pipeline first:")
        st.code("python -m src.run_all", language="powershell")
        return

    PAGES[choice](df)


if __name__ == "__main__":
    main()
