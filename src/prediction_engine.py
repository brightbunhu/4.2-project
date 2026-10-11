"""
src/prediction_engine.py
========================
CORE PREDICTION ENGINE FOR OPTION B:
Supports both Single Manual Observation Prediction and CSV Batch Prediction
using the actual trained Option B pipeline and models.

Predictive Horizon: Month T -> Month T+1 (Relative Commodity Price Stress)
"""
from __future__ import annotations

import io
import json
from pathlib import Path
from datetime import datetime, date
from typing import Tuple, Dict, Any, List

import numpy as np
import pandas as pd
import joblib
import shap

ROOT = Path(__file__).resolve().parents[1]
OPT_B_DIR = ROOT / "outputs" / "option_b"
MODELS_DIR = OPT_B_DIR / "models"
DATA_DIR = OPT_B_DIR / "data"

FEATURE_JSON = DATA_DIR / "option_b_feature_columns.json"
MODELLING_TABLE = DATA_DIR / "option_b_modelling_table.csv"
XGB_MODEL_PATH = MODELS_DIR / "xgboost_pipeline.joblib"
LOGREG_MODEL_PATH = MODELS_DIR / "logreg_pipeline.joblib"


class OptionBPredictor:
    """Production prediction service for Option B."""

    def __init__(self):
        self._load_metadata()
        self._load_models()

    def _load_metadata(self):
        if not FEATURE_JSON.exists():
            raise FileNotFoundError(f"Feature metadata missing: {FEATURE_JSON}")
        with open(FEATURE_JSON, "r", encoding="utf-8") as f:
            meta = json.load(f)
        self.features: List[str] = meta["features"]
        self.target: str = meta.get("target", "target_next_month")
        self.horizon: str = meta.get("horizon", "T+1")

        # Load reference table for historical values and categorical domains
        if MODELLING_TABLE.exists():
            self.ref_df = pd.read_csv(MODELLING_TABLE, parse_dates=["prediction_month", "target_month"])
            self.districts = sorted(self.ref_df["district_key"].dropna().unique().tolist())
            self.commodities = sorted(self.ref_df["commodity_name"].dropna().unique().tolist())
            self.currencies = sorted(self.ref_df["currency_code"].dropna().unique().tolist())

            # Numeric ranges for validation
            self.feature_stats = {}
            for f in self.features:
                if f in self.ref_df.columns and pd.api.types.is_numeric_dtype(self.ref_df[f]):
                    self.feature_stats[f] = {
                        "min": float(self.ref_df[f].min()),
                        "max": float(self.ref_df[f].max()),
                        "median": float(self.ref_df[f].median()),
                    }
        else:
            self.ref_df = pd.DataFrame()
            self.districts = []
            self.commodities = []
            self.currencies = ["USD", "ZWL"]
            self.feature_stats = {}

    def _load_models(self):
        if not XGB_MODEL_PATH.exists():
            raise FileNotFoundError(f"XGBoost pipeline missing: {XGB_MODEL_PATH}")
        self.xgb_pipeline = joblib.load(XGB_MODEL_PATH)
        self.logreg_pipeline = joblib.load(LOGREG_MODEL_PATH) if LOGREG_MODEL_PATH.exists() else None

        # Prepare TreeSHAP explainer for XGBoost
        try:
            xgb_model = self.xgb_pipeline.named_steps["model"]
            self.explainer = shap.TreeExplainer(xgb_model)
        except Exception:
            self.explainer = None

    @staticmethod
    def compute_target_month(pred_month: pd.Timestamp | datetime | date) -> pd.Timestamp:
        """Calculate exact T+1 calendar month."""
        ts = pd.to_datetime(pred_month)
        year = ts.year + (1 if ts.month == 12 else 0)
        month = 1 if ts.month == 12 else ts.month + 1
        return pd.Timestamp(year=year, month=month, day=1)

    def derive_features_for_unit(
        self, district: str, commodity: str, currency: str, pred_month: pd.Timestamp
    ) -> Dict[str, float]:
        """Derive historical lags, rainfall, and context from data at month T if available."""
        derived: Dict[str, float] = {}
        if self.ref_df.empty:
            return derived

        # Search matching history
        match = self.ref_df[
            (self.ref_df["district_key"] == district)
            & (self.ref_df["commodity_name"] == commodity)
            & (self.ref_df["prediction_month"] <= pred_month)
        ].sort_values("prediction_month", ascending=False)

        if not match.empty:
            latest = match.iloc[0]
            for f in self.features:
                if f in latest and pd.notna(latest[f]):
                    derived[f] = float(latest[f])

        # Fill default medians for any missing feature
        for f in self.features:
            if f not in derived:
                if f in self.feature_stats:
                    derived[f] = self.feature_stats[f]["median"]
                else:
                    derived[f] = 0.0

        # Update calendar fields based on actual pred_month
        derived["month_of_year"] = float(pred_month.month)
        derived["year"] = float(pred_month.year)

        # Update commodity one-hot columns
        for f in self.features:
            if f.startswith("commodity_"):
                comm_clean = f.replace("commodity_", "").lower().replace("_", " ")
                derived[f] = 1.0 if comm_clean in commodity.lower() else 0.0

        return derived

    def predict_single(
        self,
        district: str,
        commodity: str,
        currency: str,
        pred_month: pd.Timestamp | datetime | date,
        feature_overrides: Dict[str, float] | None = None,
        model_name: str = "XGBoost",
    ) -> Dict[str, Any]:
        """Predict stress for a single observation at month T -> target T+1."""
        ts_pred = pd.to_datetime(pred_month).to_period("M").to_timestamp()
        ts_target = self.compute_target_month(ts_pred)

        # Construct feature vector
        feats_dict = self.derive_features_for_unit(district, commodity, currency, ts_pred)
        if feature_overrides:
            feats_dict.update(feature_overrides)

        # Assemble row into DataFrame in exact feature order
        row_df = pd.DataFrame([{f: feats_dict.get(f, 0.0) for f in self.features}])

        # Select model
        pipe = self.xgb_pipeline if model_name == "XGBoost" else (self.logreg_pipeline or self.xgb_pipeline)

        pred_class = int(pipe.predict(row_df)[0])
        pred_proba = float(pipe.predict_proba(row_df)[0, 1])

        # TreeSHAP explanation if XGBoost
        explanation = None
        if model_name == "XGBoost" and self.explainer:
            try:
                imputer = pipe.named_steps["imputer"]
                row_imputed = imputer.transform(row_df)
                shap_vals = self.explainer.shap_values(row_imputed)[0]

                # Top increasing and decreasing
                top_idx = np.argsort(shap_vals)
                dec_idx = top_idx[:3]  # most negative (decreasing stress)
                inc_idx = top_idx[::-1][:3]  # most positive (increasing stress)

                explanation = {
                    "top_increasing": [
                        {"feature": self.features[i], "shap_value": round(float(shap_vals[i]), 4), "value": round(float(row_df.iloc[0, i]), 4)}
                        for i in inc_idx if shap_vals[i] > 0
                    ],
                    "top_decreasing": [
                        {"feature": self.features[i], "shap_value": round(float(shap_vals[i]), 4), "value": round(float(row_df.iloc[0, i]), 4)}
                        for i in dec_idx if shap_vals[i] < 0
                    ],
                    "disclaimer": "Feature contribution explains the fitted model prediction; it does not prove causation.",
                }
            except Exception:
                explanation = None

        return {
            "prediction_month": ts_pred.strftime("%Y-%m"),
            "target_month": ts_target.strftime("%Y-%m"),
            "district": district,
            "commodity": commodity,
            "currency": currency,
            "model_name": model_name,
            "model_version": "Option_B_Production_v1.0",
            "predicted_class": pred_class,
            "predicted_label": "High Relative Stress (SPI > 1.25)" if pred_class == 1 else "Normal / Low Stress",
            "predicted_probability": round(pred_proba, 4),
            "explanation": explanation,
            "interpretation": (
                f"The model estimates a {pred_proba*100:.1f}% probability that {commodity} in {district} "
                f"will meet the project's relative price-stress definition in month {ts_target.strftime('%B %Y')} (T+1). "
                f"This is a model-based estimate and not a guarantee."
            ),
            "disclaimer": (
                "This prediction is an academic decision-support estimate. It does not constitute an official "
                "food-security assessment, an IPC classification or a guaranteed forecast."
            ),
        }

    def validate_csv(self, df_upload: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Validate an uploaded CSV file.

        Returns:
            (valid_df, invalid_df, error_report_df)
        """
        required_identifiers = ["prediction_month", "district_key", "commodity_name", "currency_code"]
        errors: List[Dict[str, Any]] = []
        valid_indices: List[int] = []
        invalid_indices: List[int] = []

        # Standardize column names (lowercase and strip)
        col_map = {c: c.strip().lower() for c in df_upload.columns}
        df_norm = df_upload.rename(columns=col_map).copy()

        # Check column presence
        missing_id_cols = [c for c in required_identifiers if c not in df_norm.columns]
        if missing_id_cols:
            for i in range(len(df_upload)):
                errors.append({
                    "row_number": i + 1,
                    "observation_id": df_upload.iloc[i].get("observation_id", f"ROW_{i+1}"),
                    "error_type": "MISSING_REQUIRED_COLUMN",
                    "affected_column": ", ".join(missing_id_cols),
                    "error_message": f"Uploaded CSV lacks mandatory columns: {missing_id_cols}",
                })
            return pd.DataFrame(), df_upload, pd.DataFrame(errors)

        # Check duplicate observation IDs if provided
        if "observation_id" in df_norm.columns:
            dups = df_norm["observation_id"].duplicated(keep=False)
            for idx in df_norm[dups].index:
                errors.append({
                    "row_number": idx + 1,
                    "observation_id": df_norm.loc[idx, "observation_id"],
                    "error_type": "DUPLICATE_IDENTIFIER",
                    "affected_column": "observation_id",
                    "error_message": f"Duplicate observation_id: {df_norm.loc[idx, 'observation_id']}",
                })

        for i, row in df_norm.iterrows():
            row_errors = []
            obs_id = row.get("observation_id", f"ROW_{i+1}")

            # Check null identifiers
            for col in required_identifiers:
                if pd.isna(row.get(col)):
                    row_errors.append({
                        "row_number": i + 1,
                        "observation_id": obs_id,
                        "error_type": "NULL_IDENTIFIER",
                        "affected_column": col,
                        "error_message": f"Mandatory column '{col}' is null or missing.",
                    })

            # Check valid date
            pred_dt = None
            try:
                pred_dt = pd.to_datetime(row["prediction_month"])
            except Exception:
                row_errors.append({
                    "row_number": i + 1,
                    "observation_id": obs_id,
                    "error_type": "INVALID_DATE_FORMAT",
                    "affected_column": "prediction_month",
                    "error_message": f"Cannot parse date '{row.get('prediction_month')}'. Expected YYYY-MM.",
                })

            # Check district
            dist = str(row.get("district_key", "")).strip().upper()
            if self.districts and dist not in self.districts:
                row_errors.append({
                    "row_number": i + 1,
                    "observation_id": obs_id,
                    "error_type": "UNSUPPORTED_DISTRICT",
                    "affected_column": "district_key",
                    "error_message": f"District '{dist}' is not in approved Zimbabwe ADM2 district list.",
                })

            # Check commodity
            comm = str(row.get("commodity_name", "")).strip()
            if self.commodities and comm not in self.commodities:
                row_errors.append({
                    "row_number": i + 1,
                    "observation_id": obs_id,
                    "error_type": "UNSUPPORTED_COMMODITY",
                    "affected_column": "commodity_name",
                    "error_message": f"Commodity '{comm}' is not in approved commodity list.",
                })

            # Check numeric feature ranges if explicitly provided in CSV
            for f in self.features:
                if f in row and pd.notna(row[f]):
                    try:
                        val = float(row[f])
                        if "rain" in f and val < 0:
                            row_errors.append({
                                "row_number": i + 1,
                                "observation_id": obs_id,
                                "error_type": "IMPOSSIBLE_NUMERIC_VALUE",
                                "affected_column": f,
                                "error_message": f"Negative rainfall value ({val}) is physically impossible.",
                            })
                    except (ValueError, TypeError):
                        row_errors.append({
                            "row_number": i + 1,
                            "observation_id": obs_id,
                            "error_type": "INVALID_NUMERIC_TYPE",
                            "affected_column": f,
                            "error_message": f"Value '{row[f]}' could not be parsed as a float.",
                        })

            if row_errors:
                errors.extend(row_errors)
                invalid_indices.append(i)
            else:
                valid_indices.append(i)

        valid_df = df_upload.iloc[valid_indices].copy()
        invalid_df = df_upload.iloc[invalid_indices].copy()
        error_df = pd.DataFrame(errors)

        return valid_df, invalid_df, error_df

    def predict_batch(self, valid_df: pd.DataFrame, model_name: str = "XGBoost") -> pd.DataFrame:
        """Run predictions on validated CSV rows."""
        if valid_df.empty:
            return pd.DataFrame()

        results: List[Dict[str, Any]] = []
        pipe = self.xgb_pipeline if model_name == "XGBoost" else (self.logreg_pipeline or self.xgb_pipeline)

        for i, row in valid_df.iterrows():
            obs_id = row.get("observation_id", f"OBS_{i+1:05d}")
            p_month = pd.to_datetime(row["prediction_month"]).to_period("M").to_timestamp()
            t_month = self.compute_target_month(p_month)
            dist = str(row["district_key"]).strip().upper()
            comm = str(row["commodity_name"]).strip()
            curr = str(row["currency_code"]).strip().upper()

            # Derive base features
            feats_dict = self.derive_features_for_unit(dist, comm, curr, p_month)

            # Override with any provided feature columns in row
            for f in self.features:
                if f in row and pd.notna(row[f]):
                    try:
                        feats_dict[f] = float(row[f])
                    except Exception:
                        pass

            row_features = pd.DataFrame([{f: feats_dict.get(f, 0.0) for f in self.features}])

            pred_c = int(pipe.predict(row_features)[0])
            pred_p = float(pipe.predict_proba(row_features)[0, 1])

            results.append({
                "observation_id": obs_id,
                "prediction_month": p_month.strftime("%Y-%m"),
                "target_month": t_month.strftime("%Y-%m"),
                "district_key": dist,
                "commodity_name": comm,
                "currency_code": curr,
                "predicted_class": pred_c,
                "predicted_label": "High Relative Stress (1)" if pred_c == 1 else "Normal / Low Stress (0)",
                "predicted_probability": round(pred_p, 4),
                "model_name": model_name,
                "model_version": "Option_B_Production_v1.0",
                "validation_status": "PASSED",
                "prediction_status": "SUCCESS",
            })

        return pd.DataFrame(results)

    def generate_csv_template(self) -> str:
        """Generate official CSV template containing sample row and feature schema."""
        sample_dist = self.districts[0] if self.districts else "HARARE"
        sample_comm = self.commodities[0] if self.commodities else "Maize grain"

        template_df = pd.DataFrame([{
            "observation_id": "OBS_SAMPLE_001",
            "prediction_month": "2024-09",
            "district_key": sample_dist,
            "commodity_name": sample_comm,
            "currency_code": "USD",
            "spi_lag_1": 1.05,
            "spi_lag_2": 1.02,
            "spi_pct_change_3m": 4.5,
            "months_since_last_reported_price": 1.0,
            "rainfall_1m": 45.2,
            "rainfall_3m_total": 120.5,
            "rainfall_6m_total": 450.0,
            "rainfall_12m_total": 780.0,
            "rainfall_3m_anomaly": 0.12,
            "log_population": 11.52,
            "is_urban": 0,
        }])
        return template_df.to_csv(index=False)
