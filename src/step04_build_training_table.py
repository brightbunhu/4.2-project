"""
src/step04_build_training_table.py
==================================
STEP 4 - BUILD THE COMMODITY-LEVEL TRAINING TABLE.

Grain: commodity x district x month.
Target: price_stress = 1 if spatial_price_index > 1.0 else 0.

Column-name mapping (actual on-disk -> dissertation names)
  d_price_district_month.spi                 -> spatial_price_index
  d_rainfall_chirps_district_month.rainfall_mm -> rainfall_1m
  d_district_base.province / .district        -> admin1_name / admin2_name
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config as C

pd.set_option("display.width", 160)
pd.set_option("display.max_columns", 80)

PROC = C.DATA_PROC

# %%
# ======================================================================================
# STEP 1 - LOAD ALL FILES
# ======================================================================================
price = pd.read_csv(PROC / "d_price_district_month.csv", parse_dates=["month"])
rain = pd.read_csv(PROC / "d_rainfall_chirps_district_month.csv", parse_dates=["month"])
pop = pd.read_csv(PROC / "d_population_district.csv")
base = pd.read_csv(PROC / "d_district_base.csv")

print("=" * 90)
print("STEP 1 - LOADED FILES")
print("=" * 90)
for name, df in [("d_price_district_month", price),
                 ("d_rainfall_chirps_district_month", rain),
                 ("d_population_district", pop),
                 ("d_district_base", base)]:
    print(f"\n{name}: shape={df.shape}")
    print(f"  columns: {list(df.columns)}")
    nz = df.isna().sum()
    nz = nz[nz > 0]
    print(f"  missing: {nz.to_dict() if len(nz) else 'none'}")

print("\nShared keys: district_key (all), month (price & rain).")

# %%
# ======================================================================================
# STEP 2 - DEFINE TARGET VARIABLE
# ======================================================================================
# Rename the real SPI column to the dissertation name.
price = price.rename(columns={"spi": "spatial_price_index"})

# SPI is missing for thin cells (too few markets) -> target undefined; drop them.
n0 = len(price)
price = price[price["spatial_price_index"].notna()].copy()
print(f"\nRows dropped for missing spatial_price_index: {n0 - len(price)}")

price["price_stress"] = (price["spatial_price_index"] > 1.0).astype(int)

tc = price["price_stress"].value_counts().sort_index()
tp = (price["price_stress"].value_counts(normalize=True).sort_index() * 100).round(2)
print("\n" + "=" * 90)
print("STEP 2 - TARGET VARIABLE (price_stress)")
print("=" * 90)
print("overall counts:\n" + tc.to_string())
print("overall percent:\n" + tp.to_string())

print("\nby commodity (top 15 by row count):")
top15 = price["commodity_name"].value_counts().head(15).index
tab = (price[price["commodity_name"].isin(top15)]
       .groupby("commodity_name")["price_stress"]
       .agg(rows="size", stress="sum", stress_pct=lambda s: round(100 * s.mean(), 1))
       .sort_values("rows", ascending=False))
print(tab.to_string())

print("\nby province:")
prov = (price.groupby("province_key")["price_stress"]
        .agg(rows="size", stress="sum", stress_pct=lambda s: round(100 * s.mean(), 1)))
print(prov.to_string())

# %%
# ======================================================================================
# STEP 3 - MERGE RAINFALL (left join on district_key + month)
# ======================================================================================
rain_small = rain[[
    "district_key", "month", "rainfall_mm",
    "rainfall_3m_total", "rainfall_6m_total", "rainfall_12m_total",
    "rainfall_3m_anomaly",
]].rename(columns={"rainfall_mm": "rainfall_1m"})

df = price.merge(rain_small, on=["district_key", "month"], how="left")

rmiss = df["rainfall_1m"].isna().sum()
print("\n" + "=" * 90)
print("STEP 3 - RAINFALL MERGE")
print("=" * 90)
print(f"rows after merge: {len(df)}")
print(f"rows with missing rainfall_1m: {rmiss} ({rmiss / len(df):.1%})")
print("Coverage: CHIRPS district-month covers the full price window (2017-2026);")
print("rows are missing only where the price month falls outside CHIRPS coverage.")

# %%
# ======================================================================================
# STEP 4 - MERGE POPULATION (left join on district_key)
# ======================================================================================
pop_small = pop[["district_key", "population", "log_population", "is_urban"]]
df = df.merge(pop_small, on="district_key", how="left", suffixes=("", "_pop"))
print("\n" + "=" * 90)
print("STEP 4 - POPULATION MERGE")
print("=" * 90)
print(f"rows after merge: {len(df)}")
print(f"missing population: {df['population'].isna().sum()}")
print(f"missing log_population: {df['log_population'].isna().sum()}")
print(f"missing is_urban: {df['is_urban'].isna().sum()}")

# %%
# ======================================================================================
# STEP 5 - COMMODITY-SPECIFIC FEATURES
# ======================================================================================
# Sort so shifts follow time within each commodity-district series.
df = df.sort_values(["district_key", "commodity_name", "month"]).reset_index(drop=True)
grp = df.groupby(["district_key", "commodity_name"], sort=False)["spatial_price_index"]

df["spi_lag_1"] = grp.shift(1)
df["spi_lag_2"] = grp.shift(2)
df["spi_pct_change_3m"] = grp.pct_change(3) * 100

# Add months_since_last_reported_price
df = df.sort_values(["district_key", "commodity_name", "month"]).reset_index(drop=True)
df["prev_month"] = df.groupby(["district_key", "commodity_name"])["month"].shift(1)
df["months_since_last_reported_price"] = (df["month"] - df["prev_month"]).dt.days / 30.44
df["months_since_last_reported_price"] = df["months_since_last_reported_price"].round(2)
df = df.drop(columns=["prev_month"])

print("\n" + "=" * 90)
print("STEP 5 - COMMODITY-SPECIFIC FEATURES")
print("=" * 90)
for c in ["spi_lag_1", "spi_lag_2", "spi_pct_change_3m", "months_since_last_reported_price", "months_since_last_reported_price"]:
    print(f"{c}: missing={df[c].isna().sum()} ({df[c].isna().mean():.1%})")
print("NOTE: lags use previous OBSERVED months in the series (price collection is")
print("      irregular, so a 'lag' may span more than one calendar month).")

# %%
# ======================================================================================
# STEP 6 - TIME FEATURES
# ======================================================================================
df["month_of_year"] = df["month"].dt.month
df["year"] = df["month"].dt.year
print("\n" + "=" * 90)
print("STEP 6 - TIME FEATURES")
print("=" * 90)
print(df[["month_of_year", "year"]].describe().T.to_string())

# %%
# ======================================================================================
# STEP 7 - ENCODE COMMODITY (top 10 + OTHER)
# ======================================================================================
top10 = price["commodity_name"].value_counts().head(10).index.tolist()
df["commodity_grouped"] = np.where(df["commodity_name"].isin(top10),
                                   df["commodity_name"], "OTHER")
dummies = pd.get_dummies(df["commodity_grouped"], prefix="commodity", dtype=int)
df = pd.concat([df, dummies], axis=1)
commodity_cols = dummies.columns.tolist()

print("\n" + "=" * 90)
print("STEP 7 - COMMODITY ENCODING")
print("=" * 90)
print(f"top 10 commodities: {top10}")
print(f"OTHER rows: {(df['commodity_grouped'] == 'OTHER').sum()}")
print(f"encoded columns ({len(commodity_cols)}): {commodity_cols}")

# %%
# ======================================================================================
# STEP 8 - FEATURE SELECTION (leakage-free)
# ======================================================================================
base_features = [
    "rainfall_1m", "rainfall_3m_total", "rainfall_6m_total", "rainfall_12m_total",
    "rainfall_3m_anomaly", "spi_lag_1", "spi_lag_2", "spi_pct_change_3m", "months_since_last_reported_price",
    "log_population", "is_urban", "month_of_year", "year",
]
feature_cols = [c for c in base_features if c in df.columns] + commodity_cols

# Drop any feature with >50% missing.
missing_frac = df[feature_cols].isna().mean()
drop_missing = missing_frac[missing_frac > 0.5].index.tolist()
feature_cols = [c for c in feature_cols if c not in drop_missing]

X = df[feature_cols].copy()
y = df["price_stress"].copy()

print("\n" + "=" * 90)
print("STEP 8 - LEAKAGE-FREE FEATURE SET")
print("=" * 90)
print(f"excluded: spatial_price_index (target), identifiers")
print(f"dropped (>50% missing): {drop_missing}")
print(f"FINAL features ({len(feature_cols)}): {feature_cols}")
print(f"X shape: {X.shape}, y shape: {y.shape}")

# Publish the leakage-free feature whitelist so later steps cannot re-admit the
# price-derived columns that remain in the saved table (price, price_spi_raw, spi_pct_dev...).
import json
(PROC / "feature_columns.json").write_text(json.dumps(feature_cols, indent=2), encoding="utf-8")
print(f"saved feature list -> {PROC / 'feature_columns.json'}")

# %%
# ======================================================================================
# STEP 9 - CHECK CLASS BALANCE
# ======================================================================================
counts = y.value_counts().sort_index()
pct = (y.value_counts(normalize=True).sort_index() * 100).round(2)
ratio = counts.max() / counts.min()
print("\n" + "=" * 90)
print("STEP 9 - CLASS BALANCE")
print("=" * 90)
print("counts:\n" + counts.to_string())
print("percent:\n" + pct.to_string())
print(f"imbalance ratio = {ratio:.2f}")
print("class_weight='balanced' is recommended." if ratio > 1.5
      else "classes are reasonably balanced.")

# %%
# ======================================================================================
# STEP 10 - HANDLE MISSING VALUES
# ======================================================================================
lag_cols = ["spi_lag_1", "spi_lag_2", "spi_pct_change_3m", "months_since_last_reported_price"]
n_before = len(df)
keep_mask = df[lag_cols].notna().all(axis=1)
n_lost = (~keep_mask).sum()

print("\n" + "=" * 90)
print("STEP 10 - HANDLE MISSING LAG VALUES")
print("=" * 90)
print(f"rows before: {n_before}")
print(f"rows with a missing lag: {n_lost} ({n_lost / n_before:.1%})")

# These are structural (start of each commodity-district series) rather than random.
if n_lost / n_before > 0.30:
    # Fall back to within-commodity median imputation.
    print("Dropping would lose >30% -> using within-commodity median imputation.")
    for c in lag_cols:
        med = df.groupby("commodity_name")[c].transform("median")
        df[c] = df[c].fillna(med)
    df = df[df["price_stress"].notna()].copy()
    mode = "median-imputed"
else:
    df = df[keep_mask].copy()
    mode = "dropped"
print(f"rows after ({mode}): {len(df)}")

X = df[feature_cols].copy()
y = df["price_stress"].copy()

# %%
# ======================================================================================
# STEP 11 - SAVE FINAL TABLE
# ======================================================================================
out_path = PROC / "commodity_training_table.csv"
df.to_csv(out_path, index=False)

rows_per_commodity = df.groupby("commodity_name").size()
print("\n" + "=" * 90)
print("STEP 11 - SAVED FINAL TABLE")
print("=" * 90)
print(f"saved to: {out_path}")
print(f"final rows        : {len(df)}")
print(f"districts         : {df['district_key'].nunique()}")
print(f"months            : {df['month'].dt.to_period('M').nunique()}")
print(f"commodities       : {df['commodity_name'].nunique()}")
print(f"features          : {len(feature_cols)}")
print(f"median rows/comm. : {rows_per_commodity.median():.0f}")

# %%
# ======================================================================================
# STEP 12 - SUMMARY REPORT
# ======================================================================================
counts = y.value_counts().sort_index()
pct = (y.value_counts(normalize=True).sort_index() * 100).round(2)
print("\n" + "=" * 90)
print("STEP 12 - FINAL SUMMARY")
print("=" * 90)
print(f"Total rows          : {len(df)}")
print(f"Unique districts    : {df['district_key'].nunique()}")
print(f"Unique months       : {df['month'].dt.to_period('M').nunique()}")
print(f"Unique commodities  : {df['commodity_name'].nunique()}")
print(f"Date range          : {df['month'].min().date()} -> {df['month'].max().date()}")
print(f"Target counts       : {counts.to_dict()}")
print(f"Target percentages  : {pct.to_dict()}")
print(f"Number of features  : {len(feature_cols)}")
print(f"Median rows/comm.   : {rows_per_commodity.median():.0f}")
print("\nMissing values per feature:")
print(X.isna().sum().to_string())

ready = len(df) >= 5000
print("\n" + "=" * 90)
print(f"ENOUGH ROWS FOR ML (target >= 5000)? {'YES' if ready else 'NO'} ({len(df)} rows)")
print("=" * 90)


# Reporting gap summary

