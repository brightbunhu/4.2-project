"""Cached data access layer for the ZFPS dashboard.

The dashboard only *reads* artefacts produced by the research pipeline (src/step01..step10).
It never re-runs heavy processing (e.g. the 8.5 GB CHIRPS NetCDF) and never retrains models.
"""
from __future__ import annotations

import json
import re
import sys
from functools import lru_cache
from pathlib import Path

import pandas as pd

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import config as C  # noqa: E402

import streamlit as st  # noqa: E402

TARGET = "price_stress"
OPTION_B_DIR = _ROOT / "outputs" / "option_b"

MODEL_LABELS = {
    "logreg": "Logistic Regression",
    "xgboost": "XGBoost",
    "dummy": "Dummy (baseline)",
}
# Models that produce meaningful probabilities for per-observation prediction pages.
PREDICTION_MODELS = ["logreg", "xgboost"]


def normalize_district(name: object) -> str:
    """Upper-case, strip punctuation and collapse spaces so names join across sources.

    Handles the two known mismatches between the training table and the geoBoundaries
    ADM2 layer: 'CENTENARY MUZARABANI' <-> 'CENTENARY/ MUZARABANI' and
    'MHONDORO NGEZI' <-> 'MHONDORO-NGEZI'.
    """
    return re.sub(r"[^A-Z0-9]+", " ", str(name).upper()).strip()


# --------------------------------------------------------------------------------------
# Training table & derived feature lists
# --------------------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_training_table() -> pd.DataFrame:
    df = pd.read_csv(C.TRAIN_COMMODITY, parse_dates=["month"])
    df["district_key"] = df["district_key"].map(normalize_district)
    # Drop invalid rows
    mask_bad = df["district_key"].astype(str).str.upper().eq("NAN") | df["district_key"].isna()
    df = df[~mask_bad].copy()
    # Add province aliases from district base if missing
    if ("province_key" not in df.columns or df["province_key"].isna().all()) or \
       ("province" not in df.columns or df["province"].isna().all()):
        try:
            db = load_district_base()
            if not db.empty:
                map_cols = db[["district_key", "province", "province_key"]].drop_duplicates()
                df = df.merge(map_cols, on="district_key", how="left", suffixes=("", "_db"))
                if "province" not in df.columns or df["province"].isna().all():
                    if "province_db" in df.columns:
                        df["province"] = df["province_db"]
                if "province_key" not in df.columns or df["province_key"].isna().all():
                    if "province_key_db" in df.columns:
                        df["province_key"] = df["province_key_db"]
                for c in ["province_db", "province_key_db"]:
                    if c in df.columns:
                        df = df.drop(columns=[c])
        except Exception:
            pass
    # fallback from admin1_name if still missing
    if "province" not in df.columns or df["province"].isna().all():
        if "admin1_name" in df.columns:
            df["province"] = df["admin1_name"]
    if "province_key" not in df.columns or df["province_key"].isna().all():
        if "province" in df.columns:
            df["province_key"] = df["province"].astype(str).str.upper()
        elif "admin1_name" in df.columns:
            df["province_key"] = df["admin1_name"].astype(str).str.upper()
    # Clean NaN province keys
    if "province_key" in df.columns:
        df = df[df["province_key"].notna() & (df["province_key"].astype(str).str.upper() != "NAN")].copy()
    return df


@st.cache_data(show_spinner=False)
def load_selected_features() -> list[str]:
    path = C.DATA_PROC / "selected_features.json"
    if not path.exists():
        return []
    payload = json.loads(path.read_text())
    if isinstance(payload, dict):
        return list(payload.get("selected", []))
    return list(payload)


@st.cache_data(show_spinner=False)
def load_rainfall_district() -> pd.DataFrame:
    """Long district x month CHIRPS series already produced by step03."""
    if not C.PROC_RAINFALL_DISTRICT.exists():
        return pd.DataFrame()
    df = pd.read_csv(C.PROC_RAINFALL_DISTRICT, parse_dates=["month"])
    df["district_key"] = df["district_key"].map(normalize_district)
    return df


@st.cache_data(show_spinner=False)
def load_district_base() -> pd.DataFrame:
    if not C.PROC_DISTRICT_BASE.exists():
        return pd.DataFrame()
    df = pd.read_csv(C.PROC_DISTRICT_BASE)
    df["district_key"] = df["district_key"].map(normalize_district)
    return df


@st.cache_data(show_spinner=False)
def load_poverty_province() -> pd.DataFrame:
    if not C.PROC_POVERTY.exists():
        return pd.DataFrame()
    return pd.read_csv(C.PROC_POVERTY)


@st.cache_data(show_spinner=False)
def read_result(filename: str) -> pd.DataFrame:
    """Read a CSV from outputs/results by filename; empty frame if absent."""
    path = C.OUT_RES / filename
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


# --------------------------------------------------------------------------------------
# Geography
# --------------------------------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def load_geo():
    """Load the ADM2 boundary layer once per session."""
    try:
        import geopandas as gpd
    except Exception:
        return None
    if not C.GEO_FILES["adm2"].exists():
        return None
    gdf = gpd.read_file(C.GEO_FILES["adm2"])
    gdf["district_key"] = gdf["shapeName"].map(normalize_district)
    return gdf


@st.cache_data(show_spinner=False)
def load_geojson() -> dict:
    gdf = load_geo()
    if gdf is None:
        return {}
    return json.loads(gdf.to_json())


# --------------------------------------------------------------------------------------
# Models
# --------------------------------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def load_models() -> dict:
    """Discover and load every ``step07_*.joblib`` model in outputs/models."""
    import joblib
    models: dict[str, object] = {}
    for path in sorted(C.OUT_MODELS.glob("step07_*.joblib")):
        key = path.stem.replace("step07_", "")
        try:
            models[key] = joblib.load(path)
        except Exception:
            continue
    return models


@st.cache_data(show_spinner=False)
def load_predictions() -> pd.DataFrame:
    """Append per-model predictions to the training table using the fitted full-data models.

    The saved ``step07`` models are fitted on the full training table; these predictions are
    used for the interactive map/detail pages. Held-out evaluation lives in step08.
    """
    df = load_training_table()
    feats = load_selected_features()
    models = load_models()
    if not feats or not models:
        return df
    X = df[feats].fillna(df[feats].median(numeric_only=True))
    out = df.copy()
    for key, model in models.items():
        try:
            if hasattr(model, "predict_proba"):
                out[f"{key}_proba"] = model.predict_proba(X)[:, 1]
            out[f"{key}_pred"] = model.predict(X)
        except Exception:
            continue
    # Ensure province columns exist in predictions too
    if "province_key" not in out.columns or "province" not in out.columns:
        try:
            db = load_district_base()
            if not db.empty:
                mcols = db[["district_key", "province", "province_key"]].drop_duplicates()
                out = out.merge(mcols, on="district_key", how="left", suffixes=("", "_db"))
                if "province" not in out.columns:
                    if "province_db" in out.columns: out["province"] = out["province_db"]
                if "province_key" not in out.columns:
                    if "province_key_db" in out.columns: out["province_key"] = out["province_key_db"]
                for c in ["province_db", "province_key_db"]:
                    if c in out.columns: out = out.drop(columns=[c])
        except Exception:
            pass
    if "province" not in out.columns and "admin1_name" in out.columns:
        out["province"] = out["admin1_name"]
    if "province_key" not in out.columns:
        if "province" in out.columns:
            out["province_key"] = out["province"].astype(str).str.upper()
        elif "admin1_name" in out.columns:
            out["province_key"] = out["admin1_name"].astype(str).str.upper()
    mask_bad = out["district_key"].astype(str).str.upper().eq("NAN") | out["district_key"].isna()
    out = out[~mask_bad].copy()
    if "province_key" in out.columns:
        out = out[out["province_key"].notna() & (out["province_key"].astype(str).str.upper() != "NAN")].copy()
    return out


@st.cache_data(show_spinner=False)
def load_shap_importance() -> pd.DataFrame:
    """Global mean |SHAP| per feature (from the XGBoost TreeExplainer)."""
    df = read_result("step09_shap_importance.csv")
    if df.empty:
        return df
    return pd.DataFrame({"feature": df["feature"],
                         "importance_mean": df["mean_abs_shap"],
                         "importance_std": 0.0}).sort_values(
        "importance_mean", ascending=False).reset_index(drop=True)


@st.cache_data(show_spinner=False)
def load_shap_values() -> pd.DataFrame:
    """Per-observation SHAP values (index = training-table row number)."""
    df = read_result("step09_shap_values.csv")
    if df.empty or "row_index" not in df.columns:
        return pd.DataFrame()
    return df.set_index("row_index")


@st.cache_data(show_spinner=False)
def load_shap_base() -> float | None:
    df = read_result("step09_shap_base.csv")
    if df.empty or "expected_value_logodds" not in df.columns:
        return None
    return float(df["expected_value_logodds"].iloc[0])


@st.cache_data(show_spinner=False)
def load_model_importance(method: str) -> pd.DataFrame:
    """Feature-importance tables that actually exist.

    * ``shap``        -> outputs/results/step09_shap_importance.csv (mean |SHAP|)
    * ``permutation`` -> outputs/results/step09_permutation_importance.csv
    * ``mutual_info`` -> outputs/results/step06_feature_ranking.csv
    * ``model``       -> native XGBoost gain importance (computed from the fitted model)
    """
    if method == "shap":
        return load_shap_importance()
    if method == "permutation":
        return read_result("step09_permutation_importance.csv")
    if method == "mutual_info":
        return read_result("step06_feature_ranking.csv")
    if method == "model":
        feats = load_selected_features()
        model = load_models().get("xgboost")
        if model is None or not hasattr(model, "feature_importances_") or not feats:
            return pd.DataFrame()
        return pd.DataFrame({"feature": feats,
                             "importance_mean": model.feature_importances_,
                             "importance_std": 0.0})
    return pd.DataFrame()


def available_importance_methods() -> list[str]:
    methods = []
    if not load_shap_importance().empty:
        methods.append("shap")
    if not read_result("step09_permutation_importance.csv").empty:
        methods.append("permutation")
    if not read_result("step06_feature_ranking.csv").empty:
        methods.append("mutual_info")
    if "xgboost" in load_models() and load_selected_features():
        methods.append("model")
    return methods


@lru_cache(maxsize=1)
def dataset_registry() -> list[dict]:
    return list(getattr(C, "DATASET_REGISTRY", []))


# --------------------------------------------------------------------------------------
# Authoritative Option B (T -> T+1) Loaders
# --------------------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_option_b_predictions() -> pd.DataFrame:
    """Load unified predictions file for Option B (month T -> stress at T+1)."""
    p = OPTION_B_DIR / "results" / "option_b_predictions.csv"
    if not p.exists():
        return pd.DataFrame()
    df = pd.read_csv(p, parse_dates=["prediction_month", "target_month"])
    df["district_key"] = df["district_key"].map(normalize_district)
    return df


@st.cache_data(show_spinner=False)
def load_option_b_modelling_table() -> pd.DataFrame:
    """Load the final Option B modelling table with shifted target and lag features."""
    p = OPTION_B_DIR / "data" / "option_b_modelling_table.csv"
    if not p.exists():
        return pd.DataFrame()
    df = pd.read_csv(p, parse_dates=["prediction_month", "target_month"])
    df["district_key"] = df["district_key"].map(normalize_district)
    return df


@st.cache_data(show_spinner=False)
def load_option_b_metrics() -> pd.DataFrame:
    """Load out-of-sample temporal validation metrics for Option B."""
    p = OPTION_B_DIR / "results" / "option_b_model_metrics.csv"
    if not p.exists():
        return pd.DataFrame()
    return pd.read_csv(p)


@st.cache_resource(show_spinner=False)
def load_option_b_models() -> dict[str, object]:
    """Load the trained production Option B models (Dummy, LogReg, XGBoost)."""
    import joblib
    models: dict[str, object] = {}
    m_dir = OPTION_B_DIR / "models"
    for name, key in [
        ("dummy_baseline.joblib", "dummy"),
        ("logreg_pipeline.joblib", "logreg"),
        ("xgboost_pipeline.joblib", "xgboost"),
    ]:
        path = m_dir / name
        if path.exists():
            try:
                models[key] = joblib.load(path)
            except Exception:
                pass
    return models


@st.cache_data(show_spinner=False)
def load_option_b_shap_importance() -> pd.DataFrame:
    """Load Option B global TreeSHAP feature importance."""
    p = OPTION_B_DIR / "explainability" / "option_b_shap_importance.csv"
    if not p.exists():
        return pd.DataFrame()
    return pd.read_csv(p)


@st.cache_data(show_spinner=False)
def load_option_b_local_explanations() -> pd.DataFrame:
    """Load Option B local observation explanations."""
    p = OPTION_B_DIR / "explainability" / "option_b_local_explanations.csv"
    if not p.exists():
        return pd.DataFrame()
    return pd.read_csv(p, parse_dates=["prediction_month", "target_month"])


@st.cache_data(show_spinner=False)
def load_option_b_validation_audit() -> pd.DataFrame:
    """Load forward temporal validation audit for Option B."""
    p = OPTION_B_DIR / "results" / "validation_audit.csv"
    if not p.exists():
        return pd.DataFrame()
    return pd.read_csv(p)


@st.cache_data(show_spinner=False)
def load_option_b_target_audit() -> pd.DataFrame:
    """Load target shift audit for Option B."""
    p = OPTION_B_DIR / "results" / "target_shift_audit.csv"
    if not p.exists():
        return pd.DataFrame()
    return pd.read_csv(p)


@st.cache_data(show_spinner=False)
def load_option_b_feature_audit() -> pd.DataFrame:
    """Load feature availability and leakage audit for Option B."""
    p = OPTION_B_DIR / "results" / "feature_availability_audit.csv"
    if not p.exists():
        return pd.DataFrame()
    return pd.read_csv(p)
