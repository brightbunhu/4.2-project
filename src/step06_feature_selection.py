"""
step06_feature_selection.py
===========================
STEP 6 - FEATURE SELECTION.

Starting from the leakage-free feature set produced in step04, rank features and remove any
that carry no information (constant / near-zero variance). Selection is data-driven but
conservative: we report the ranking and only drop degenerate columns.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config as C  # noqa: E402
from src.utils import banner, save_df, write_text

TARGET = "price_stress"
# Columns that are identifiers or are derived directly from the price series / target and
# must never be used as predictors. Only relevant as a fallback if the step04 whitelist is
# missing.
LEAKY = {"price", "country_median_price", "price_spi_raw", "spatial_price_index",
         "spi_winsorised", "spi_pct_dev", "month_num"}
IDENTIFIERS = {"district_key", "month", "province_key", "province", "commodity_name",
               "commodity_category", "commodity_grouped", "unit", "currency_code",
               "price_flag", "is_food", TARGET} | LEAKY


def candidate_features(df: pd.DataFrame) -> list[str]:
    """Leakage-free feature whitelist published by step04 (fallback: safe numeric columns)."""
    whitelist_path = C.DATA_PROC / "feature_columns.json"
    if whitelist_path.exists():
        import json
        whitelist = json.loads(whitelist_path.read_text())
        if isinstance(whitelist, dict):
            whitelist = whitelist.get("selected", [])
        return [c for c in whitelist if c in df.columns]
    return [c for c in df.columns
            if c not in IDENTIFIERS and pd.api.types.is_numeric_dtype(df[c])]


def main() -> None:
    banner("6", "FEATURE SELECTION")
    df = pd.read_csv(C.TRAIN_COMMODITY, parse_dates=["month"])
    feats = candidate_features(df)
    X = df[feats].fillna(df[feats].median(numeric_only=True))
    y = df[TARGET].astype(int)
    print(f"candidate features: {len(feats)}")

    # 1. Near-zero variance filter.
    nunique = X.nunique()
    const = nunique[nunique <= 1].index.tolist()
    X = X.drop(columns=const)
    print(f"dropped constant features: {const}")

    # 2. Mutual-information ranking (works for non-linear relations).
    from sklearn.feature_selection import mutual_info_classif
    mi = mutual_info_classif(X, y, random_state=C.RANDOM_STATE)
    ranking = (pd.DataFrame({"feature": X.columns, "mutual_info": mi})
               .sort_values("mutual_info", ascending=False).reset_index(drop=True))
    ranking["rank"] = np.arange(1, len(ranking) + 1)
    save_df(ranking, "step06_feature_ranking")
    print("\nfeature ranking:\n", ranking.to_string())

    # 3. Drop zero-information features (conservative).
    zero = ranking.loc[ranking["mutual_info"] <= 0, "feature"].tolist()
    selected = [f for f in ranking["feature"] if f not in zero]
    print(f"\ndropped zero-information features: {zero}")
    print(f"selected features ({len(selected)}): {selected}")

    (C.DATA_PROC / "selected_features.json").write_text(
        json.dumps({"selected": selected, "dropped": const + zero}, indent=2),
        encoding="utf-8")

    lines = ["# Step 6 - Feature Selection", "",
             f"Candidates: **{len(feats)}**; dropped constant: {const}; "
             f"dropped zero-MI: {zero}.",
             f"Selected: **{len(selected)}** features.", "",
             "## Mutual-information ranking", "```",
             ranking.to_string(), "```"]
    write_text("\n".join(lines), "step06_feature_selection", C.REPORTS)

    banner("6", f"SELECTED {len(selected)} FEATURES -> data/processed/selected_features.json")


if __name__ == "__main__":
    main()
