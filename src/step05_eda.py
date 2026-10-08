"""
step05_eda.py
=============
STEP 5 - EXPLORATORY DATA ANALYSIS of the commodity-level training table.

Answers the practical questions before modelling: how balanced is the target, which features
co-vary with it, is there seasonality, and does stress vary by province/commodity.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config as C  # noqa: E402
from src.utils import banner, save_df, save_fig, write_text

TARGET = "price_stress"


def numeric_features(df: pd.DataFrame) -> list[str]:
    drop = {TARGET, "spatial_price_index"}
    return [c for c in df.columns
            if pd.api.types.is_numeric_dtype(df[c]) and c not in drop]


def main() -> None:
    banner("5", "EXPLORATORY DATA ANALYSIS")
    df = pd.read_csv(C.TRAIN_COMMODITY, parse_dates=["month"])
    print(f"loaded {C.TRAIN_COMMODITY.name}: {df.shape}")

    # --- target balance -------------------------------------------------------------
    tc = df[TARGET].value_counts().sort_index()
    tp = (df[TARGET].value_counts(normalize=True).sort_index() * 100).round(2)
    print("\ntarget:\n", pd.concat([tc.rename("count"), tp.rename("pct")], axis=1).to_string())

    # --- numeric summary ------------------------------------------------------------
    num = numeric_features(df)
    summary = df[num + [TARGET]].describe().T.round(4)
    save_df(summary, "step05_numeric_summary")
    print("\nnumeric summary:\n", summary.to_string())

    # --- correlation with target ----------------------------------------------------
    corr = (df[num + [TARGET]].corr()[TARGET].drop(TARGET)
            .sort_values(ascending=False).round(4))
    save_df(corr.rename("corr_with_target").reset_index().rename(columns={"index": "feature"}),
            "step05_correlation_target")
    print("\ntop correlations with target:\n", corr.head(12).to_string())

    # --- figure 1: target balance ---------------------------------------------------
    fig, ax = plt.subplots(figsize=(4.5, 3.5))
    tc.plot(kind="bar", ax=ax, rot=0, color=["#2c7fb8", "#d95f0e"])
    ax.set_title("Target balance - price_stress")
    ax.set_xlabel("price_stress")
    ax.set_ylabel("rows")
    for i, v in enumerate(tc.values):
        ax.text(i, v, f"{v:,}", ha="center", va="bottom")
    save_fig(fig, "step05_target_balance")
    plt.close(fig)

    # --- figure 2: feature correlation bar ------------------------------------------
    top = corr.head(15)
    fig, ax = plt.subplots(figsize=(7, 5))
    top[::-1].plot(kind="barh", ax=ax, color="#3182bd")
    ax.set_title("Top feature correlations with price_stress")
    ax.set_xlabel("Pearson r")
    save_fig(fig, "step05_top_correlations")
    plt.close(fig)

    # --- figure 3: seasonality ------------------------------------------------------
    seas = df.groupby("month_of_year")[TARGET].mean() * 100
    fig, ax = plt.subplots(figsize=(7, 3.5))
    seas.plot(kind="bar", ax=ax, rot=0, color="#e6550d")
    ax.set_title("Share of commodity-months in price stress by calendar month")
    ax.set_ylabel("% stressed")
    ax.set_xlabel("month")
    save_fig(fig, "step05_seasonality")
    plt.close(fig)

    # --- figure 4: stress by province -----------------------------------------------
    if "province_key" in df.columns:
        prov = (df.groupby("province_key")[TARGET].mean() * 100).sort_values()
        save_df(prov.rename("stress_pct").reset_index(), "step05_stress_by_province")
        fig, ax = plt.subplots(figsize=(7, 4))
        prov.plot(kind="barh", ax=ax, color="#756bb1")
        ax.set_title("Share of commodity-months in price stress by province")
        ax.set_xlabel("% stressed")
        save_fig(fig, "step05_stress_by_province")
        plt.close(fig)

    # --- figure 5: stress by commodity ----------------------------------------------
    comm = (df.groupby("commodity_name")[TARGET].agg(["mean", "size"])
            .assign(stress_pct=lambda d: (d["mean"] * 100).round(1))
            .sort_values("stress_pct", ascending=False))
    save_df(comm.reset_index(), "step05_stress_by_commodity")
    fig, ax = plt.subplots(figsize=(7, max(4, 0.3 * len(comm))))
    comm["stress_pct"][::-1].plot(kind="barh", ax=ax, color="#31a354")
    ax.set_title("Share of commodity-months in price stress by commodity")
    ax.set_xlabel("% stressed")
    save_fig(fig, "step05_stress_by_commodity")
    plt.close(fig)

    # --- report ---------------------------------------------------------------------
    lines = ["# Step 5 - Exploratory Data Analysis", ""]
    lines.append(f"Loaded `{C.TRAIN_COMMODITY.name}`: **{len(df):,} rows x {df.shape[1]} cols**.")
    lines.append("")
    lines.append("## Target balance")
    lines.append("```")
    lines.append(pd.concat([tc.rename("count"), tp.rename("pct")], axis=1).to_string())
    lines.append("```")
    lines.append("")
    lines.append("## Strongest feature correlations with `price_stress`")
    lines.append("```")
    lines.append(corr.head(15).to_frame("pearson_r").to_string())
    lines.append("```")
    lines.append("")
    lines.append("## Seasonality (% in stress by calendar month)")
    lines.append("```")
    lines.append(seas.round(1).to_frame("stress_pct").to_string())
    lines.append("```")
    lines.append("")
    if "province_key" in df.columns:
        lines.append("## Stress by province (%)")
        lines.append("```")
        lines.append(prov.round(1).to_frame("stress_pct").to_string())
        lines.append("```")
    write_text("\n".join(lines), "step05_eda", C.REPORTS)

    banner("5", "EDA COMPLETE -> reports/step05_eda.md")


if __name__ == "__main__":
    main()
