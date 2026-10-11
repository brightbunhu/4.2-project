"""Run one of the saved full-data Option B estimators on a feature CSV.

Usage from the last/ directory:
  python scripts/infer_with_saved_model.py input_features.csv predictions.csv --model xgboost

The model artifacts are full-data fits, not fold-held-out estimators. The script
does not build raw-price/rainfall features; the supplied CSV must satisfy the
feature contract in models/model_contract.json.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import pandas as pd


HERE = Path(__file__).resolve().parents[1]
MODELS = HERE / "models"
ARTIFACTS = {
    "dummy": "dummy_baseline.joblib",
    "logreg": "logreg_pipeline.joblib",
    "xgboost": "xgboost_pipeline.joblib",
}
KEY_COLUMNS = ["district_key", "commodity_name", "prediction_month", "currency_code"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_csv", type=Path)
    parser.add_argument("output_csv", type=Path)
    parser.add_argument("--model", choices=ARTIFACTS, default="xgboost")
    args = parser.parse_args()

    metadata = json.loads((MODELS / "option_b_feature_columns.json").read_text(encoding="utf-8"))
    features = metadata["features"]
    frame = pd.read_csv(args.input_csv)
    missing = [c for c in features if c not in frame.columns]
    if missing:
        raise ValueError(f"Input is missing required feature columns: {missing}")
    X = frame.loc[:, features]
    model = joblib.load(MODELS / ARTIFACTS[args.model])
    classes = list(model.classes_)
    pred = model.predict(X)
    result = frame.loc[:, [c for c in KEY_COLUMNS if c in frame.columns]].copy()
    result["model_run_id"] = f"saved_full_data_{args.model}"
    result["predicted_class"] = pred
    result["predicted_label"] = ["Relative price stress" if int(p) == 1 else "No relative price stress" for p in pred]
    if hasattr(model, "predict_proba") and 1 in classes:
        result["probability_stress"] = model.predict_proba(X)[:, classes.index(1)]
    result.to_csv(args.output_csv, index=False)


if __name__ == "__main__":
    main()
