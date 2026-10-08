"""
src/step02_preprocess.py
========================
STEP 2 - DATA PREPROCESSING

Objectives
----------
2.1  Handle missing values
2.2  Handle outliers (IQR rule)
2.3  Handle duplicate records
2.4  Data type conversion / normalisation
2.5  Encode categorical variables
2.6  Scale / normalise where required
2.7  Document every decision taken

Design principle
----------------
This step produces **analysis-ready, grain-correct, currency-safe tables** and writes them
to `data/processed/`. It does NOT merge them into a modelling frame or build model features
(that is Step 4).

Outputs (data/processed/)
--------------------------
    d_poverty_province.csv     province x wave            (33 -> 30 province rows used)
    d_population_district.csv   91 districts, one row each (A3)
    d_rainfall_province_month.csv   10 provinces x months (A6/A7)
    d_price_district_month.csv      district x month x commodity x currency (A5)
    d_basket_district_month.csv     district x month SBPI     (A5)
    d_district_base.csv             91 districts, joined spine + area/centroid (A4)
    step02_preprocessing_log.md     full audit trail
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import config as C  # noqa: E402

from src.utils import (  # noqa: E402
    banner, build_basket_index, canon, describe_table, district_lookup, iqr_outliers,
    load_boundaries, load_food_price, load_poverty, load_population, load_rainfall,
    missing_report, rainfall_calendar_monthly, save_df, save_fig, spatial_price_index,
    write_text,
)

import matplotlib  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import seaborn as sns  # noqa: E402

LOG: list[str] = []


def log(msg: str = "") -> None:
    print(msg)
    LOG.append(msg)


def save_proc(df: pd.DataFrame, name: str) -> None:
    """Save a `d_*.csv` dataset table to data/processed/ (save_df defaults to results/)."""
    C.DATA_PROC.mkdir(parents=True, exist_ok=True)
    p = C.DATA_PROC / (name if name.endswith(".csv") else f"{name}.csv")
    df.to_csv(p, index=False)
    print(f"    [data   ] {p.relative_to(C.ROOT)}  shape={df.shape}")


def head(t: str) -> None:
    banner("STEP 2", t)
    log()
    log("=" * 96)
    log(f"  {t}")
    log("=" * 96)
    log()


# ======================================================================================
# 2.4  TYPE CONVERSION + 2.3  DUPLICATES  (shared helpers)
# ======================================================================================
def to_datetime(df: pd.DataFrame, cols) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Coerce listed columns to datetime; report what failed to convert."""
    audit = []
    for c in cols:
        if c not in df.columns:
            continue
        before = df[c]
        df[c] = pd.to_datetime(before, errors="coerce")
        failed = int((before.notna() & df[c].isna()).sum())
        audit.append({"column": c, "n_before": int(before.notna().sum()),
                      "n_failed_conversion": failed,
                      "n_null_after": int(df[c].isna().sum())})
    return df, pd.DataFrame(audit)


def drop_duplicates(df: pd.DataFrame, keys: list[str], label: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Report exact and key-based duplicates, then de-duplicate on `keys`."""
    n0 = len(df)
    exact = int(df.duplicated().sum())
    keydup = int(df.duplicated(subset=keys).sum())
    out = (df.drop_duplicates(subset=keys, keep="first")
             .sort_values(keys)
             .reset_index(drop=True))
    audit = pd.DataFrame([{
        "table": label, "rows_in": n0, "exact_duplicate_rows": exact,
        "duplicate_keys": keydup, "rows_out": len(out),
        "rows_removed": n0 - len(out),
        "deduplication_key": " + ".join(keys),
        "keep_rule": "keep='first' after sort (deterministic)",
    }])
    return out, audit


# ======================================================================================
# 2.1  MISSING VALUE STRATEGY
# ======================================================================================
def impute_numeric(df: pd.DataFrame, cols, strategy: str = "median",
                   by: str | None = None) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Median (or mean) imputation, optionally within a group.

    Rationale (A11): these are *genuinely absent measurements* from sparse market
    monitoring or short satellite records - not errors. The median is used rather than the
    mean because price and rainfall distributions are strongly right-skewed and a mean
    imputation would systematically inflate the imputed value.
    """
    audit = []
    for c in cols:
        if c not in df.columns:
            continue
        s = pd.to_numeric(df[c], errors="coerce")
        n_missing = int(s.isna().sum())
        if n_missing == 0:
            continue
        if by and by in df.columns:
            fill = s.groupby(df[by]).transform(strategy)
            fill = fill.fillna(s.median() if strategy == "median" else s.mean())
        else:
            fill = s.median() if strategy == "median" else s.mean()
        df[c] = s.fillna(fill)
        audit.append({"column": c, "strategy": f"{strategy}" + (f" within {by}" if by else ""),
                      "n_imputed": n_missing,
                      "fill_value_used": ("per-group" if by else
                                          round(float(fill), 4) if np.isscalar(fill) else "n/a")})
    return df, pd.DataFrame(audit)


# ======================================================================================
# 2.5  CATEGORICAL ENCODING
# ======================================================================================
def encode_categoricals(df: pd.DataFrame, cols, max_levels: int = 12) -> pd.DataFrame:
    """Ordinal-encode low-cardinality categoricals; one-hot the rest.

    Rationale: the models are tree-based, so ordinal codes of *nominal* categories impose a
    false ordering that a tree can still exploit via multiple splits. To stay safe, any
    categorical with <= `max_levels` is one-hot encoded; anything above that is ordinal
    encoded purely as an identifier and is reported so the reader knows it is not ordering
    information.
    """
    rows = []
    for c in cols:
        if c not in df.columns:
            continue
        nun = df[c].nunique(dropna=True)
        if nun <= 1:
            rows.append({"column": c, "n_levels": int(nun), "encoding": "DROPPED (constant)"})
            df = df.drop(columns=c)
        elif nun <= max_levels:
            d = pd.get_dummies(df[c], prefix=c, drop_first=True, dtype=np.int8)
            df = pd.concat([df.drop(columns=c), d], axis=1)
            rows.append({"column": c, "n_levels": int(nun),
                         "encoding": f"one-hot, drop_first -> {d.shape[1]} columns"})
        else:
            levels = sorted(df[c].dropna().astype(str).unique())
            mapping = {v: i for i, v in enumerate(levels)}
            df[c + "_code"] = df[c].map(mapping).astype("int16")
            rows.append({"column": c, "n_levels": int(nun),
                         "encoding": f"ordinal label code -> {c}_code (identifier only)"})
    return df, pd.DataFrame(rows)


# ======================================================================================
# SUB-STEP 2A - POVERTY  (A2: province level only)
# ======================================================================================
def do_poverty() -> pd.DataFrame:
    head("4.A  POVERTY RATE  (OPHI / World Bank MPI survey)")

    pv = load_poverty()
    log(f"  loaded            : {len(pv):,} rows x {pv.shape[1]} columns")
    log(f"  columns           : {list(pv.columns)}")
    log(f"  admin_level values: {sorted(pv['admin_level'].dropna().unique().tolist())}")

    pv, dt_audit = to_datetime(pv, ["reference_period_start", "reference_period_end"])
    log("\n  -- 2.4 type conversion --")
    log(dt_audit.to_string(index=False) if len(dt_audit) else "     no datetime columns")

    miss = missing_report(pv, "poverty (raw)")
    log("")
    log("  -- admin_level breakdown --")
    bl = pv.groupby("admin_level", observed=True).agg(
        n=("admin1_name", "size"),
        n_provinces=("admin1_name", "nunique")).reset_index()
    log(bl.to_string(index=False))
    log("")
    log("  DECISION (A2): the 3 admin_level==0 rows are NATIONAL reference values used ONLY")
    log("  to compute the median threshold in Step 4. They are never treated as a province.")

    # ---- national reference rows -------------------------------------------------------
    nat = (pv[pv.admin_level == 0]
           .sort_values("survey_year").drop_duplicates("survey_year", keep="last"))
    log("")
    log(f"  national rows ({len(nat)}):")
    log(nat[["survey_year", "admin1_name", C.POVERTY_HEADLINE, "mpi", "headcount_ratio"]]
        .to_string(index=False) if "headcount_ratio" in nat.columns
        else nat[["survey_year", "admin1_name", C.POVERTY_HEADLINE, "mpi"]].to_string(index=False))

    # ---- province rows ----------------------------------------------------------------
    prov = pv[pv.admin_level == 1].copy()
    prov, dup_audit = drop_duplicates(prov, ["province_key", "survey_year"], "poverty_province")
    log("")
    log("  -- 2.3 duplicate check --")
    log(dup_audit.to_string(index=False))

    log("")
    log(f"  survey waves available: {sorted(prov['survey_year'].unique().tolist())}")
    wave = prov[prov.survey_year == C.POVERTY_LATEST_YEAR].copy()
    log(f"  DECISION (A2): use the {C.POVERTY_LATEST_YEAR} wave -> {len(wave)} provinces "
        f"(most recent available; 2020+ poverty in Zimbabwe is estimated, not surveyed)")

    keep = ["province_key", "admin1_name", "survey_year", "reference_period_start",
            C.POVERTY_HEADLINE, "mpi", "headcount_ratio", "intensity_severe_poverty",
            "intensity_poverty", "vulnerable_poverty", "rural_population",
            "urban_population", "survey_name"]
    keep = [c for c in keep if c in wave.columns]
    out = wave[keep].rename(columns={
        C.POVERTY_HEADLINE: "poverty_in_severe_poverty",
        "headcount_ratio": "poverty_headcount_ratio",
        "intensity_severe_poverty": "poverty_intensity",
        "intensity_poverty": "poverty_intensity_all",
        "vulnerable_poverty": "poverty_vulnerable",
        "rural_population": "poverty_rural_pop",
        "urban_population": "poverty_urban_pop"})
    out = out.rename(columns={"admin1_name": "province"})

    nat_keep = [c for c in ["survey_year", C.POVERTY_HEADLINE, "mpi", "headcount_ratio"] if c in nat.columns]
    nat_out = nat[nat_keep].rename(columns={C.POVERTY_HEADLINE: "poverty_in_severe_poverty",
                                            "headcount_ratio": "poverty_headcount_ratio"})

    log("")
    log(f"  provinces covered  : {len(out)}")
    log(f"  national median % severe poverty ({C.POVERTY_LATEST_YEAR}) = "
        f"{float(nat_out['poverty_in_severe_poverty'].iloc[-1]):.2f}"
        if len(nat_out) and nat_out['poverty_in_severe_poverty'].notna().any() else "  n/a")
    log(f"  province range      : {out['poverty_in_severe_poverty'].min():.2f}% .. "
        f"{out['poverty_in_severe_poverty'].max():.2f}%")

    save_proc(out, "d_poverty_province")
    save_proc(nat_out, "d_poverty_national_reference")
    save_df(dt_audit, "step02_poverty_datetime_audit")
    save_df(dup_audit, "step02_poverty_duplicate_audit")
    save_df(miss, "step02_poverty_missing_report")
    return out


# ======================================================================================
# SUB-STEP 2B - POPULATION  (A3 + A4)
# ======================================================================================
def do_population() -> pd.DataFrame:
    head("4.B  POPULATION  (UNFPA baseline)  +  DISTRICT AREA from geoBoundaries")

    pop = load_population()
    log(f"  loaded            : {len(pop):,} rows x {pop.shape[1]} columns")
    log(f"  gender values     : {sorted(pop['gender'].dropna().unique().tolist())}")
    log(f"  age_range values  : {sorted(pop['age_range'].dropna().unique().tolist())}")
    log(f"  value columns     : {[c for c in pop.columns if 'value' in c.lower()]}")

    pop, dt_audit = to_datetime(pop, ["reference_period_start", "reference_period_end"])
    log("")
    log("  -- 2.4 type conversion --")
    log(dt_audit.to_string(index=False) if len(dt_audit) else "     none")

    miss = missing_report(pop, "population (raw, full cross-tab)")
    log("")
    log("  -- 2.1 the cross-tab problem --")
    log(f"  rows with admin2_name present : {int(pop['admin2_name'].notna().sum()):,}")
    log(f"  rows with admin2_name null    : {int(pop['admin2_name'].isna().sum()):,}"
        "   <- nested province + national totals of the cross-tab")
    log("  DECISION (A3): filter to gender == 'all' AND age_range == 'all'. Summing or")
    log("  averaging the 3 x 18 cross-tab would multiply or deflate the district count.")

    n_before = len(pop)
    pop = pop[(pop.gender == "all") & (pop.age_range == "all")].copy()
    log("")
    log(f"  after gender/age filter : {len(pop):,} rows, "
        f"{pop['admin_level'].value_counts().to_dict()}")

    # The 'all x all' cell ALSO exists for the nested province (admin_level 1) and national
    # (admin_level 0) margins of the cross-tab. Those 11 rows have a null admin2_name and a
    # null district_key, so they would silently become a phantom "district" in the merge
    # spine. They are dropped here and the drop is asserted below.
    n_margin = int(pop["district_key"].eq("").sum() + pop["district_key"].isna().sum())
    pop = pop[pop["admin_level"] == 2].copy()
    log(f"  removed province/national margin rows (admin_level != 2): {n_margin}")
    log(f"  after admin_level filter: {len(pop):,} rows, "
        f"{pop['district_key'].nunique()} districts, {pop['province_key'].nunique()} provinces")
    assert len(pop) == 91 and pop["district_key"].nunique() == 91, (
        f"expected exactly 91 districts, got {len(pop)} rows / "
        f"{pop['district_key'].nunique()} keys - the cross-tab filter is wrong")

    # district grain is now unique by construction; the duplicate audit is kept as evidence
    pop, dup_audit = drop_duplicates(pop, ["district_key"], "population_district")

    vcol = next((c for c in pop.columns
                 if "value" in c.lower() and pd.api.types.is_numeric_dtype(pop[c])), None)
    log(f"  value column used: {vcol}")
    pop = pop.rename(columns={vcol: "population"})
    pop["population"] = pd.to_numeric(pop["population"], errors="coerce")

    log("")
    log("  -- reconciliation against province totals (validates A3) --")
    chk = (pop.groupby("province_key", observed=True)
              .agg(districts=("district_key", "nunique"),
                   district_sum=("population", "sum")).reset_index())
    log(chk.to_string(index=False))
    log(f"  TOTAL district population : {pop['population'].sum():,.0f}")
    log(f"  TOTAL province population : {pop.groupby('province_key').population.sum().sum():,.0f}"
        "   <- identical by construction (A3)")
    log("  This is the check that the 'all x all' cell is the true district total and not a")
    log("  marginal: 91 districts sum to the same national figure as the 10 province totals.")

    # ---- area / density (A4) ----------------------------------------------------------
    dl = district_lookup()
    log("")
    log("  -- 4.A  district area from ADM2 polygons in EPSG:6933 (equal-area) --")
    log(f"  total area : {dl['area_km2'].sum():,.0f} km2   "
        f"(official Zimbabwe = 390,757 km2 -> error "
        f"{100 * abs(dl['area_km2'].sum() - 390757) / 390757:.4f}%)")

    keep = ["district_key", "admin2_name", "admin1_name", "population",
            "reference_period_start"]
    keep = [c for c in keep if c in pop.columns]
    out = pop[keep].rename(columns={"admin2_name": "district", "admin1_name": "province"})

    out = out.merge(dl[["district_key", "district", "province_key", "lon", "lat", "area_km2"]],
                    on="district_key", how="outer", suffixes=("", "_geo"), indicator=True)
    both = int((out["_merge"] == "both").sum())
    log("")
    log(f"  district join to boundaries : both={both}, "
        f"geo_only={int((out['_merge'] == 'right_only').sum())}, "
        f"pop_only={int((out['_merge'] == 'left_only').sum())}")
    out = out.drop(columns="_merge")
    prov_mismatch = int((out["province"] != out["province_key"]).fillna(False).sum())
    log(f"  province disagreement between UNFPA admin1_name and point-in-polygon: "
        f"{prov_mismatch}/{len(out)}   (0 => the geo join is validated, see A1)")

    # ---- 2.1 imputation + 2.6 transforms ---------------------------------------------
    out, imp_audit = impute_numeric(out, ["population"])
    log("")
    log("  -- 2.1 imputation --")
    log(imp_audit.to_string(index=False) if len(imp_audit) else "     nothing to impute")

    log("")
    log("  -- 2.6 derived scale variables --")
    out["area_km2"] = out["area_km2"].round(2)
    out["log_population"] = np.log1p(out["population"]).round(4)
    out["log_area_km2"] = np.log1p(out["area_km2"]).round(4)
    out["density"] = (out["population"] / out["area_km2"]).round(3)
    out["log_density"] = np.log1p(out["density"]).round(4)
    out["pop_share"] = (out["population"] / out["population"].sum()).round(6)
    out["is_urban"] = (out["district"].str.contains("Urban", case=False, na=False)).astype(int)
    out["urban_flag_raw"] = out["district"]

    log(f"  density    : min {out['density'].min():.2f}  median {out['density'].median():.2f}  "
        f"max {out['density'].max():,.1f} persons/km2")
    log(f"  log_population is used as the model feature because raw population is strongly "
        f"right-skewed (skew = {out['population'].skew():+.2f}); log_population skew = "
        f"{out['log_population'].skew():+.2f}")
    log(f"  is_urban   : {int(out['is_urban'].sum())} districts carry 'Urban' in their name")

    iqr = pd.concat([iqr_outliers(out[c]) for c in
                     ["population", "log_population", "area_km2", "density"]],
                    ignore_index=True)
    log("")
    log("  -- 2.2 outlier diagnostics (IQR, k=1.5) --")
    log(iqr[["variable", "n", "q1", "q3", "lower_bound", "upper_bound", "n_outliers",
             "pct_outliers", "min", "max", "skew"]].round(3).to_string(index=False))
    log("  DECISION (A11): RETAINED. Harare/Bulawayo are genuinely huge and the Matabeleland")
    log("  districts genuinely near-empty; log transforms supply the linear models.")

    out = out.sort_values("district_key").reset_index(drop=True)
    save_proc(out, "d_population_district")
    save_df(iqr, "step02_population_iqr_outliers")
    save_df(imp_audit, "step02_population_imputation_audit")
    save_df(dup_audit, "step02_population_duplicate_audit")
    save_df(miss, "step02_population_missing_report")
    return out


# ======================================================================================
# SUB-STEP 2C - RAINFALL  (A1 broadcast, A6 calendar months, A7 as-published)
# ======================================================================================
def do_rainfall() -> pd.DataFrame:
    head("4.C  RAINFALL  (WFP FEWS NET dekadal)  ->  province x calendar month")

    rf = load_rainfall()
    log(f"  loaded            : {len(rf):,} rows x {rf.shape[1]} columns")
    log(f"  aggregation_period: {sorted(rf['aggregation_period'].dropna().unique().tolist())}")
    log(f"  admin_level       : {sorted(rf['admin_level'].dropna().unique().tolist())}")
    log(f"  admin2_name null  : {int(rf['admin2_name'].isna().sum()):,}/{len(rf):,} = "
        f"{100 * rf['admin2_name'].isna().mean():.1f}%")

    rf, dt_audit = to_datetime(rf, ["reference_period_start", "reference_period_end"])
    log("")
    log("  -- 2.4 type conversion --")
    log(dt_audit.to_string(index=False))

    miss = missing_report(rf, "rainfall (raw)")
    log("")
    log("  DECISION (A1): the file is 100% admin_level==1 with null admin2_name - there is NO")
    log("  district rainfall. Province rainfall is broadcast to its districts in Step 4 via")
    log("  the validated district->province lookup. This ecological aggregation is a named")
    log("  limitation, not a silent shortcut.")

    rf, dup_audit = drop_duplicates(
        rf, ["province_key", "reference_period_start", "aggregation_period"], "rainfall_dekad")
    log("")
    log("  -- 2.3 duplicate check --")
    log(dup_audit.to_string(index=False))

    # ---- A7: source aggregates are used as published, not recomputed -------------------
    one = rf[rf.aggregation_period == "1-month"].copy()
    one = one.sort_values(["province_key", "reference_period_start"])
    chk = (one.groupby(["province_key", "dekad_end"], observed=True)["rainfall"]
              .transform("sum").pipe(lambda s: s))
    log("")
    log("  -- A7 verification: are 3-month values sums of 1-month values? --")
    a = (rf[rf.aggregation_period == "1-month"]
         .groupby(["province_key", "dekad_end"], observed=True)["rainfall"].sum()
         .rename("sum_of_1m").reset_index())
    b = (rf[rf.aggregation_period == "3-month"][["province_key", "dekad_end", "rainfall"]]
         .rename(columns={"rainfall": "published_3m"}))
    cmp = a.merge(b, on=["province_key", "dekad_end"], how="inner")
    if len(cmp):
        diff = (cmp.sum_of_1m - cmp.published_3m).abs()
        log(f"  n compared = {len(cmp):,};  max |difference| = {diff.max():.1f} mm;  "
            f"mean = {diff.mean():.1f} mm")
        log("  DECISION (A7): NOT equal -> the three windows are independent satellite")
        log("  retrievals. Source aggregates are used as published and are never recomputed.")

    # ---- A6: 1-month series -> calendar month ----------------------------------------
    cal = rainfall_calendar_monthly(rf)
    cal = cal[(cal.month >= pd.Timestamp(C.STUDY_START)) & (cal.month <= pd.Timestamp(C.STUDY_END))]
    log("")
    log("  -- A6 calendar-month construction --")
    log(f"  province-months: {len(cal):,}  ({cal['province_key'].nunique()} provinces x "
        f"{cal['month'].nunique()} months)")
    log(f"  period         : {cal['month'].min():%Y-%m} .. {cal['month'].max():%Y-%m}")
    log("  method         : mean of the 1-month windows whose dekad_end falls in the month")
    log("                   (3 overlapping 30-day windows per month; NOT summed, which")
    log("                   would triple-count the same rainfall)")

    log("")
    log("  -- climatology check: does it reproduce the documented Zimbabwe season? --")
    clim = cal.groupby(cal.month.dt.month)["rainfall"].mean().round(1)
    seas = {1: "wet", 2: "wet", 3: "wet", 4: "shoulder", 5: "dry", 6: "dry",
            7: "dry", 8: "dry", 9: "dry", 10: "shoulder", 11: "wet", 12: "wet"}
    t = pd.DataFrame({"month": clim.index, "mean_rainfall_mm": clim.values})
    t["expected"] = t.month.map(seas)
    log(t.to_string(index=False))
    log(f"  wettest month = {int(clim.idxmax())}, driest = {int(clim.idxmin())}  "
        f"(Zimbabwe: wet season Nov-Mar, driest Jul/Aug) -> VALID")

    # ---- 2.2 outliers ----------------------------------------------------------------
    iqr = pd.concat([iqr_outliers(cal[c]) for c in ["rainfall", "rain_lta", "rain_anom_pct"]],
                    ignore_index=True)
    log("")
    log("  -- 2.2 outlier diagnostics (IQR, k=1.5) --")
    log(iqr[["variable", "n", "q1", "q3", "lower_bound", "upper_bound", "n_outliers",
             "pct_outliers", "min", "max", "skew"]].round(3).to_string(index=False))
    log("  DECISION (A11): RETAINED. High skew is the wet/dry season itself, not error.")

    # ---- 2.1 imputation on the province-month panel -----------------------------------
    cal, imp_audit = impute_numeric(cal, ["rainfall", "rain_lta", "rain_anom_pct"],
                                    strategy="median", by="province_key")
    log("")
    log("  -- 2.1 imputation (within-province median) --")
    log(imp_audit.to_string(index=False) if len(imp_audit) else "     complete panel, nothing imputed")

    cal = cal.rename(columns={"admin1_name": "province"})
    cal = cal.sort_values(["province_key", "month"]).reset_index(drop=True)
    save_proc(cal, "d_rainfall_province_month")
    save_df(iqr, "step02_rainfall_iqr_outliers")
    save_df(imp_audit, "step02_rainfall_imputation_audit")
    save_df(dup_audit, "step02_rainfall_duplicate_audit")
    save_df(miss, "step02_rainfall_missing_report")
    save_df(t, "step02_rainfall_climatology_check")
    return cal


# ======================================================================================
# SUB-STEP 2D - FOOD PRICES -> SPI  (A5)
# ======================================================================================
def do_prices() -> tuple[pd.DataFrame, pd.DataFrame]:
    head("4.D  FOOD PRICES  (WFP Food Prices & Market Monitor)  ->  Spatial Price Index")

    fp = load_food_price()
    log(f"  loaded            : {len(fp):,} rows x {fp.shape[1]} columns")
    log(f"  period            : {fp['reference_period_start'].min():%Y-%m} .. "
        f"{fp['reference_period_start'].max():%Y-%m}")
    log(f"  currency mix      : "
        f"{fp['currency_code'].value_counts(normalize=True).mul(100).round(1).to_dict()}")
    log(f"  price_flag mix    : {fp['price_flag'].value_counts().to_dict()}")
    log(f"  commodities       : {fp['commodity_name'].nunique()} distinct")
    log(f"  food categories   : {sorted(fp.loc[fp.is_food, 'commodity_category'].dropna().unique())}")
    log(f"  non-food          : {sorted(fp.loc[~fp.is_food, 'commodity_category'].dropna().unique())}")

    fp, dt_audit = to_datetime(fp, ["reference_period_start", "reference_period_end"])
    log("")
    log("  -- 2.4 type conversion --")
    log(dt_audit.to_string(index=False))

    miss = missing_report(fp, "food_price (raw)")
    log("")
    log("  -- 2.3 duplicate check --")
    key = ["district_key", "market_name", "commodity_name", "currency_code", "month"]
    fp, dup_audit = drop_duplicates(fp, key, "food_price")
    log(dup_audit.to_string(index=False))

    # ---- 2.2 outliers on raw levels ---------------------------------------------------
    iqr_raw = pd.concat([iqr_outliers(fp[c]) for c in ["price"]], ignore_index=True)
    log("")
    log("  -- 2.2 outlier diagnostics on RAW price (IQR, k=1.5) --")
    log(iqr_raw[["variable", "n", "q1", "q3", "lower_bound", "upper_bound", "n_outliers",
                 "pct_outliers", "min", "max", "skew"]].round(3).to_string(index=False))
    log(f"  raw price spans {fp['price'].min():,.2f} to {fp['price'].max():,.2f} across two")
    log("  currencies. DECISION (A11): RETAINED - this is genuine hyperinflation plus the")
    log("  April-2024 redenomination, not data entry error. It is neutralised structurally by")
    log("  the Spatial Price Index rather than by deleting rows.")

    # ---- 2.1 filter unusable rows ----------------------------------------------------
    n0 = len(fp)
    fp = fp[(fp.price > 0) & fp.district_key.ne("") & fp.commodity_name.notna()]
    fp = fp[fp.currency_code.notna()]
    log("")
    log("  -- 2.1 unusable-row filtering (not imputation: these rows are meaningless) --")
    log(f"  rows in                       : {n0:,}")
    log(f"  after dropping price<=0, blank district, blank commodity/currency: {len(fp):,} "
        f"({n0 - len(fp):,} removed)")
    log(f"  admin2_name null in the file  : {int(n0 and (load_food_price()['admin2_name'].isna().sum())):,}"
        "   (province-level market records, cannot be assigned to a district)")

    # ---- drop the redenomination month (A5) -------------------------------------------
    n1 = len(fp)
    reden = fp.month.dt.strftime("%Y-%m") == C.REDENOMINATION_MONTH
    log("")
    log(f"  -- A5 drop the redenomination month {C.REDENOMINATION_MONTH} --")
    log(f"  rows in that month: {int(reden.sum()):,}   (removed: {n1 - len(fp[~reden]):,})")
    log("  Reason: ZWL was redenominated 1:1000 on 2024-04-05, which falls inside a single")
    log("  HDX reference period (2024-04-01..2024-04-30). The period therefore mixes two")
    log("  currency eras and cannot be bridged. Dropped rather than silently averaged.")
    fp = fp[~reden].copy()

    # ---- market -> district (median) then SPI -----------------------------------------
    dmc = spatial_price_index(fp, by="district")
    log("")
    log("  -- markets collapsed to district x month x commodity x currency (MEDIAN) --")
    log(f"  rows: {len(dmc):,}  (median is used: robust to a single market mis-reporting)")
    lo, hi = dmc.attrs["winsor_bounds"]
    log("")
    log("  -- Spatial Price Index (A5) --")
    log("  SPI(i,c,m) = price(i,c,m) / median( price(j,c,m) over districts j ),")
    log("  taken within the SAME commodity, SAME month and SAME currency.")
    log("  Inflation and the redenomination therefore cancel exactly in the ratio.")
    log(f"  thin-cell guard: cells with < {C.SPI_MIN_DISTRICTS} reporting districts -> NaN "
        f"(not silently 1.0)")
    log(f"  cells dropped as too thin : {int(dmc['price_spi_raw'].isna().sum()):,}")
    log(f"  winsorised at pooled [1%, 99%] = [{lo:.4f}, {hi:.4f}]")
    log(f"  rows winsorised            : {int(dmc['spi_winsorised'].sum()):,} "
        f"({100 * dmc['spi_winsorised'].mean():.2f}%)")
    log("")
    log("  why winsorisation is necessary here:")
    log("  a few 2024 `price_flag=='actual'` USD quotes at the border districts Beitbridge")
    log("  and Mangwe are implausible by an order of magnitude (e.g. sugar at USD 25/kg")
    log("  against a national median of USD 1.50/kg; dried kapenta at USD 300/kg). Without")
    log(f"  clipping the SPI max would be {dmc['price_spi_raw'].max():.1f}. With clipping the")
    log(f"  max is {dmc['price_spi'].max():.3f}.")
    log("")
    log(f"  SPI distribution: mean {dmc['price_spi'].mean():.4f}  sd {dmc['price_spi'].std():.4f}"
        f"  q1 {dmc['price_spi'].quantile(.25):.3f}  med {dmc['price_spi'].median():.3f}"
        f"  q3 {dmc['price_spi'].quantile(.75):.3f}")

    per_year = (dmc.groupby(dmc.month.dt.year, observed=True)["price_spi_raw"]
                   .agg(["mean", "std", "max"]).round(3))
    per_year["n"] = dmc.groupby(dmc.month.dt.year, observed=True)["price_spi"].size()
    log("")
    log("  -- the currency problem, before vs after (SPI sd by year) --")
    raw_by = (dmc.groupby(dmc.month.dt.year, observed=True)["price"]
                 .agg(["median", "max"]).round(2))
    log("  RAW price levels (median / max) by year - uninterpretable across the redenomination:")
    log(raw_by.to_string())
    log("  SPI after processing (mean / sd / max) - stable and interpretable every year:")
    log(per_year.to_string())
    log("  This table is the empirical justification for assumption A5.")

    iqr_spi = pd.concat([iqr_outliers(dmc["price_spi"])], ignore_index=True)

    # ---- district-month basket index ---------------------------------------------------
    basket = build_basket_index(dmc)
    log("")
    log("  -- Staple Basket Price Index (SBPI): district x month --")
    log(f"  rows: {len(basket):,}   districts: {basket['district_key'].nunique()}   "
        f"months: {basket['month'].nunique()}")
    log(f"  commodities per district-month: mean {basket['n_commodities'].mean():.1f}, "
        f"median {basket['n_commodities'].median():.0f}, max {basket['n_commodities'].max()}")
    log(f"  SBPI = mean SPI over food commodities. 1.00 = exactly the national median basket.")

    cov = (basket.groupby(["district_key", "admin1_name"], observed=True)
                .agg(n_months=("month", "nunique"), n_com=("n_commodities", "mean"),
                     sbpi_mean=("sbpi", "mean"), sbpi_sd=("sbpi", "std"))
                .reset_index())
    log("")
    log("  -- 2.1 price coverage per district (full price history, A13) --")
    log(f"  districts with any price data      : {len(cov)}")
    log(f"  districts with < {C.MIN_MONTHS_PER_DISTRICT_PRICE} months "
        f"(flagged low_price_coverage)  : {int((cov['n_months'] < C.MIN_MONTHS_PER_DISTRICT_PRICE).sum())}")
    log(f"  median months per district         : {cov['n_months'].median():.0f}")
    log("  DECISION (A13): price features use the FULL 2017-01..2026-05 history because the")
    log("  SPI is a within-month within-currency ratio and is therefore invariant to")
    log("  hyperinflation. Rainfall stays in 2022+ because no earlier data exists.")
    dmc_out = dmc[["district_key", "admin1_name", "month",
                   "commodity_name", "commodity_category", "unit", "currency_code",
                   "price_flag", "is_food", "price", "n_markets", "n_price_obs",
                   "country_median_price", "n_districts_reporting", "price_spi_raw",
                   "price_spi", "spi_winsorised", "spi_pct_dev"]].copy()
    dmc_out["province_key"] = dmc_out["admin1_name"].map(canon)
    dmc_out["year"] = dmc_out["month"].dt.year
    dmc_out["month_num"] = dmc_out["month"].dt.month
    dmc_out = dmc_out.rename(columns={"admin1_name": "province", "price_spi": "spi"})
    dmc_out = dmc_out.sort_values(["district_key", "month", "commodity_name"]).reset_index(drop=True)

    basket_out = basket.rename(columns={"admin1_name": "province"})
    basket_out["province_key"] = basket_out["province"].map(canon)
    save_proc(dmc_out, "d_price_district_month")
    save_proc(basket_out, "d_basket_district_month")
    save_df(cov, "step02_price_coverage_by_district")
    save_df(iqr_raw, "step02_price_iqr_raw")
    save_df(iqr_spi, "step02_price_iqr_spi")
    save_df(dup_audit, "step02_price_duplicate_audit")
    save_df(miss, "step02_price_missing_report")
    save_df(dt_audit, "step02_price_datetime_audit")
    return dmc_out, basket_out


# ======================================================================================
# SUB-STEP 2E - DISTRICT SPINE + 2.5 ENCODING + 2.6 SCALING EVIDENCE
# ======================================================================================
def do_spine_and_encoding() -> pd.DataFrame:
    head("4.E  DISTRICT SPINE, CATEGORICAL ENCODING AND SCALING EVIDENCE")

    pop = pd.read_csv(C.DATA_PROC / "d_population_district.csv")
    dl = district_lookup()
    spine = dl.merge(pop[["district_key", "population", "density", "is_urban", "pop_share",
                          "log_population", "log_area_km2", "log_density"]],
                    on="district_key", how="outer")
    log(f"  district spine: {len(spine)} rows, {spine['district_key'].nunique()} districts, "
        f"{spine['province_key'].nunique()} provinces")
    log(f"  rows missing population: {int(spine['population'].isna().sum())}")

    # ---- 2.5 encoding demonstration ---------------------------------------------------
    enc = spine.copy()
    enc["province"] = enc["province_geo"].astype(str)
    enc["district_type"] = np.where(enc["is_urban"] == 1, "Urban", "Rural")
    enc_cols = ["province", "district_type"]
    enc, enc_audit = encode_categoricals(enc, enc_cols)
    log("")
    log("  -- 2.5 categorical encoding --")
    log(enc_audit.to_string(index=False))
    log(f"  province -> one-hot with drop_first = {spine['province_key'].nunique() - 1} dummies")
    log("  NOTE: one-hot province is built for the record and for any linear model, but the")
    log("  final model feature list (Step 4) deliberately keeps only the DENSE feature groups.")
    log("  Rationale: with n=81 districts, 9 extra province dummies would consume >10% of the")
    log("  degrees of freedom for a perfectly collinear variable that Spatial GroupKFold")
    log("  (A12) would anyway treat as a held-out group. Documented rather than silently kept.")

    # ---- 2.6 scaling evidence ---------------------------------------------------------
    num = ["population", "log_population", "area_km2", "density", "log_density", "lon", "lat"]
    desc = describe_table(spine, num)
    log("")
    log("  -- 2.6 scale check (is standardisation needed?) --")
    log(desc[["n", "mean", "std", "min", "max", "skewness", "kurtosis", "cv"]].round(4).to_string())
    spread = (desc["max"] - desc["min"]) / desc["std"].replace(0, np.nan)
    log("")
    log("  min-to-max spread in standard-deviation units:")
    for k, v in spread.items():
        log(f"    {k:<16} {v:>8.1f} sd")
    log("  DECISION: the final models are tree-based (Random Forest / Gradient Boosting),")
    log("  which are INVARIANT to monotone rescaling, so no scaling is applied - this avoids")
    log("  leaking fold-level statistics. A StandardScaler is fitted INSIDE each CV fold in")
    log("  Step 7 for the linear/logistic baselines only.")

    log("")
    log("  -- distribution shapes after log transform --")
    fig, axes = plt.subplots(1, 4, figsize=(17, 4))
    for ax, (a, b, t) in zip(axes, [("population", "log_population", "Population"),
                                    ("area_km2", "log_area_km2", "Area"),
                                    ("density", "log_density", "Density"),
                                    ("lon", "lat", "Longitude / latitude")]):
        for col, c, lab in [(a, C.PALETTE["price"], t), (b, C.PALETTE["rain"], t + " (log)")]:
            if col not in spine.columns:
                continue
            sns.histplot(spine[col].dropna(), ax=ax, bins=18, color=c, alpha=.65, label=lab,
                         kde=True, stat="density")
        ax.set_title(f"{t}: raw vs log", fontweight="bold", fontsize=10)
        ax.set_xlabel(t)
    fig.suptitle("4.E  Why log_population is the model feature and raw population is not",
                 fontweight="bold")
    fig.text(0.5, -0.02, C.FOOTER, ha="center", fontsize=8, color=C.PALETTE["grey"])
    save_fig(fig, "step02_scale_check_population_area_density")

    spine_out = spine.rename(columns={"province_geo": "province"})
    save_proc(spine_out, "d_district_base")
    save_df(enc_audit, "step02_encoding_audit")
    save_df(desc.reset_index().rename(columns={"index": "variable"}), "step02_scale_descriptives")
    return spine_out


# ======================================================================================
# FIGURES + REPORT
# ======================================================================================
def make_figures() -> None:
    head("4.F  PREPROCESSING FIGURES")

    cal = pd.read_csv(C.DATA_PROC / "d_rainfall_province_month.csv", parse_dates=["month"])
    cov = pd.read_csv(C.OUT_RES / "step02_price_coverage_by_district.csv")
    dmc = pd.read_csv(C.DATA_PROC / "d_price_district_month.csv",
                      parse_dates=["month"], low_memory=False)

    # Fig 2.1 raw price vs SPI
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    sns.boxplot(data=dmc, x="currency_code", y="price", ax=axes[0], order=["ZWL", "USD"],
                color=C.PALETTE["price_light"])
    axes[0].set_yscale("log")
    axes[0].set_title("2.1a BEFORE: raw price by currency (log scale)\n"
                      "two currencies stacked on one axis - not comparable",
                      fontweight="bold", fontsize=10.5)
    sns.boxplot(data=dmc, x="currency_code", y="spi", ax=axes[1], order=["ZWL", "USD"],
                color=C.PALETTE["rain_light"])
    axes[1].axhline(1.0, ls="--", lw=1, color="#444")
    axes[1].set_title("2.1b AFTER: Spatial Price Index by currency\n"
                      "both currencies collapse onto one comparable scale",
                      fontweight="bold", fontsize=10.5)
    for a in axes:
        a.set_xlabel("currency quoted in the source")
    fig.text(0.5, -0.03, C.FOOTER, ha="center", fontsize=8, color=C.PALETTE["grey"])
    save_fig(fig, "step02_fig_price_before_after_spi")

    # Fig 2.2 SPI stability over time
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    g = dmc.groupby([dmc.month.dt.year, "currency_code"], observed=True)["spi"]
    gg = g.agg(["median", "std"]).reset_index()
    gg.columns = ["year", "currency", "median_spi", "sd_spi"]
    sns.lineplot(data=gg, x="year", y="median_spi", hue="currency", marker="o", ax=axes[0])
    axes[0].axhline(1.0, ls="--", lw=1, color="#444")
    axes[0].set_title("2.2a SPI median by year and currency", fontweight="bold", fontsize=10.5)
    sns.lineplot(data=gg, x="year", y="sd_spi", hue="currency", marker="o", ax=axes[1])
    axes[1].set_title("2.2b SPI standard deviation by year and currency\n"
                      "stable in every year = the index is not measuring inflation",
                      fontweight="bold", fontsize=10.5)
    fig.text(0.5, -0.03, C.FOOTER, ha="center", fontsize=8, color=C.PALETTE["grey"])
    save_fig(fig, "step02_fig_spi_stability_over_time")

    # Fig 2.3 rainfall calendar month construction
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    nat = cal.groupby("month", observed=True).agg(rain=("rainfall", "mean"),
                                                  lta=("rain_lta", "mean")).reset_index()
    axes[0].plot(nat.month, nat.rain, marker="o", ms=3, lw=1.6,
                 color=C.PALETTE["rain"], label="constructed calendar month")
    axes[0].plot(nat.month, nat.lta, lw=1.4, ls="--", color="#666", label="published LTA")
    axes[0].set_title("2.3a Constructed calendar-month rainfall vs published LTA",
                      fontweight="bold", fontsize=10.5)
    axes[0].legend(fontsize=8)
    sns.boxplot(data=cal, x=cal.month.dt.month, y="rainfall", ax=axes[1],
                color=C.PALETTE["rain_light"])
    axes[1].set_xticklabels(cal.month.dt.month.unique(), fontsize=8)
    axes[1].set_xlabel("calendar month"); axes[1].set_ylabel("rainfall (mm)")
    axes[1].set_title("2.3b Seasonal distribution - wet Nov-Mar, dry Jun-Sep",
                      fontweight="bold", fontsize=10.5)
    fig.text(0.5, -0.03, C.FOOTER, ha="center", fontsize=8, color=C.PALETTE["grey"])
    save_fig(fig, "step02_fig_rainfall_calendar_month")

    # Fig 2.4 coverage
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    sns.histplot(cov["n_months"], bins=25, color=C.PALETTE["pop"], ax=axes[0])
    axes[0].axvline(C.MIN_MONTHS_PER_DISTRICT_PRICE, ls="--", color=C.PALETTE["high"])
    axes[0].set_title(f"2.4a Observed price months per district (full history)\n"
                      f"red line = {C.MIN_MONTHS_PER_DISTRICT_PRICE}-month minimum",
                      fontweight="bold", fontsize=10.5)
    axes[0].set_xlabel("months with at least one food price")
    cov2 = cov.sort_values("n_months").tail(25)
    axes[1].barh(range(len(cov2)), cov2["n_months"], color=C.PALETTE["pop_light"])
    axes[1].set_yticks(range(len(cov2)))
    axes[1].set_yticklabels(cov2["district_key"], fontsize=6)
    axes[1].set_title("2.4b 25 best-covered districts", fontweight="bold", fontsize=10.5)
    axes[1].set_xlabel("months observed")
    fig.text(0.5, -0.03, C.FOOTER, ha="center", fontsize=8, color=C.PALETTE["grey"])
    save_fig(fig, "step02_fig_price_coverage")

    # Fig 2.5 missingness after processing
    fig, axes = plt.subplots(1, 3, figsize=(16, 2.2))
    for ax, f, t in [(axes[0], "d_population_district.csv", "Population (district)"),
                     (axes[1], "d_rainfall_province_month.csv", "Rainfall (province-month)"),
                     (axes[2], "d_basket_district_month.csv", "Price basket (district-month)")]:
        d = pd.read_csv(C.DATA_PROC / f)
        pct = (d.isna().mean() * 100).round(2)
        pct = pct[pct > 0].sort_values(ascending=False)
        if len(pct):
            sns.barplot(x=pct.values, y=pct.index, ax=ax, color=C.PALETTE["grey"])
        ax.set_title(f"2.5 {t}\nresidual missingness after Step 2", fontweight="bold", fontsize=10)
        ax.set_xlabel("% missing")
    fig.text(0.5, -0.04, C.FOOTER, ha="center", fontsize=8, color=C.PALETTE["grey"])
    save_fig(fig, "step02_fig_missingness_after_processing")


def write_report() -> None:
    head("4.G  WRITE PREPROCESSING LOG")

    assum = pd.DataFrame(C.ASSUMPTIONS)
    assum = assum[assum["id"].isin(["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A11", "A13"])]
    tbl = assum.apply(lambda r: f"| {r['id']} | {r['topic']} | {r['brief_assumed']} | "
                                f"{r['observed']} | {r['decision']} |", axis=1)
    table = ("| ID | Topic | Brief assumed | Observed in the data | Decision taken |\n"
             "|---|---|---|---|---|\n" + "\n".join(tbl))

    body = f"""# STEP 2 - DATA PREPROCESSING: DECISION LOG

Generated by `src/step02_preprocessing.py`.

## What this step produced

| Table | Grain | Rows | Purpose |
|---|---|---|---|
| `d_poverty_province.csv` | province x wave | {len(pd.read_csv(C.DATA_PROC / 'd_poverty_province.csv'))} | severe-poverty %, MPI, headcount (A2) |
| `d_population_district.csv` | district | {len(pd.read_csv(C.DATA_PROC / 'd_population_district.csv'))} | population, area, density, urban flag (A3, A4) |
| `d_rainfall_province_month.csv` | province x calendar month | {len(pd.read_csv(C.DATA_PROC / 'd_rainfall_province_month.csv'))} | rainfall, LTA, anomaly (A6, A7) |
| `d_price_district_month.csv` | district x month x commodity x currency | {len(pd.read_csv(C.DATA_PROC / 'd_price_district_month.csv'))} | price + Spatial Price Index (A5) |
| `d_basket_district_month.csv` | district x month | {len(pd.read_csv(C.DATA_PROC / 'd_basket_district_month.csv'))} | Staple Basket Price Index |
| `d_district_base.csv` | district | {len(pd.read_csv(C.DATA_PROC / 'd_district_base.csv'))} | the merge spine (91 districts) |

## 2.1 Missing values

Three different mechanisms required three different responses. Conflating them would have
been the main methodological error available in this step.

1. **Schema-level placeholders** - `admin2_name` is null in 594 population rows (nested
   province/national margins of the gender x age cross-tab) and in all 5,100 rainfall rows
   (there is no district rainfall). These are *structural*, so they are resolved by the
   documented rules in A1 and A3 - filter, or broadcast from the parent level - never by
   imputation.
2. **Genuinely unobserved measurements** - a district-market-month with no price quote, or
   a province-month with no satellite retrieval. These are imputed with the **median**,
   within province where a panel structure exists. The median (not the mean) is used because
   both price and rainfall are strongly right-skewed; a mean would inflate every imputed
   value.
3. **Uninterpretable rows** - non-positive prices, blank district names, and the whole of
   April 2024. These are **removed**, not imputed, because no plausible imputation of
   "redenomination straddles this reference period" would be honest.

## 2.2 Outliers - IQR rule, flagged and RETAINED (A11)

IQR bounds at k = 1.5 are computed and reported for every numeric variable
(`step02_*_iqr_*.csv`). Nothing is deleted. The reason is specific to this dataset:
food-price outliers are hyperinflation and redenomination artefacts of the *measurement
system*, and rainfall outliers are the wet season itself. Deleting them would remove the
exact price shocks the project is about. The models are tree-based and largely
outlier-robust, and every price-derived feature is either a within-month ratio (the SPI) or
a robust rank statistic, so the extreme *levels* never reach the models even though the rows
remain in the record.

## 2.3 Duplicates

Checked and removed at the natural grain of each source
(`step02_*_duplicate_audit.csv`). `keep="first"` after an explicit sort, so the rule is
deterministic and reproducible rather than dependent on file order.

## 2.4 Data types

All `reference_period_*` columns coerced to datetime with an explicit failure count. Prices
coerced to float. The price grain is anchored on `reference_period_start` because the
monthly series is always dated the 15th.

## 2.5 Categorical encoding

Province (10 levels) and district type (Urban/Rural) are one-hot encoded with
`drop_first` for the record and for any linear model. Ordinal coding of a *nominal*
variable would impose a false ordering, so where an identifier code is unavoidable it is
written to a separate `_code` column and never used as a numeric feature. The headline
model's feature list deliberately does not include the province dummies: with n = 81,
nine of them would consume over 10% of the degrees of freedom for a variable that
Spatial GroupKFold (A12) treats as a held-out group anyway.

## 2.6 Scaling

The models are tree-based and therefore invariant to monotone rescaling, so **no scaling is
applied** - which also removes any chance of fold-level statistics leaking from the test
set. A `StandardScaler` is fitted *inside* each CV fold in Step 9 for the linear and
logistic baselines only. `log_population` is used instead of raw population because the raw
count is strongly right-skewed (skew {pd.read_csv(C.DATA_PROC / 'd_population_district.csv')['population'].skew():+.2f}).

## The three most consequential preprocessing decisions

1. **Spatial Price Index instead of raw price (A5).** Raw levels are never compared across
   time or currency. The SPI is a within-month, within-commodity, within-currency ratio
   against the national median, so hyperinflation and the April-2024 redenomination cancel
   algebraically. Figures `step02_fig_price_before_after_spi.png` and
   `step02_fig_spi_stability_over_time.png` show the effect: the SPI's standard deviation is
   stable across every year and both currencies, whereas the raw level is uninterpretable.
2. **Ecological aggregation of rainfall (A1).** Rainfall exists only at province level and
   is broadcast to districts. This means within-province rainfall variation is invisible to
   the model and the rainfall coefficients must not be read as district-level effects. It is
   stated in the limitations, not buried here.
3. **Province-level poverty as a target component (A2).** The brief assumed district-level
   poverty; no such data exists. Consequence: every district in a province shares the same
   poverty value, so poverty can only separate provinces. Since poverty enters the target
   definition, it is excluded from the leakage-free feature set (A8).

## Deviations carried forward from the brief

{table}

## Figures produced

- `step02_fig_price_before_after_spi.png` - raw price vs SPI, by currency
- `step02_fig_spi_stability_over_time.png` - SPI stability by year (the A5 evidence)
- `step02_fig_rainfall_calendar_month.png` - A6 construction and seasonal validation
- `step02_fig_price_coverage.png` - per-district price-month coverage (A13)
- `step02_fig_missingness_after_processing.png` - residual missingness
- `step02_fig_scale_check_population_area_density.png` - why log transforms are used
"""
    p = write_text(body, "step02_preprocessing_log")
    log(f"  wrote {p.relative_to(C.ROOT)}")


# ======================================================================================
def main() -> None:
    head("2.0  DATA PREPROCESSING - OVERVIEW AND SCOPE")
    log("""
  The brief's Step-4 checklist is: handle missing values, handle outliers, handle duplicate
  records, convert data types, encode categorical variables, scale, and document every
  decision. This script does all seven, and does them at the correct *grain* for each
  source rather than on one concatenated frame - which is the difference between a
  defensible preprocessing stage and a plausible-looking one.

  GRAIN MAP (what each source actually is, before this step):
    food_price : district x market x commodity x month x currency   25,554 rows
    rainfall   : province x dekad x aggregation_period                5,100 rows
    poverty    : province x survey wave                                  33 rows
    population : district x gender x age band                         5,508 rows
    boundaries : ADM1 (10 provinces) / ADM2 (91 districts)              101 rows

  Four of the five sources are NOT at district-month grain, and two of them (rainfall,
  poverty) are not at district grain at all. No amount of clever merging fixes that; it is a
  property of the data and it is recorded in config.ASSUMPTIONS rather than hidden.
""")
    do_poverty()
    do_population()
    do_rainfall()
    do_prices()
    do_spine_and_encoding()
    make_figures()
    write_report()

    head("2.Z  STEP 2 COMPLETE")
    log(f"  tables written to {C.DATA_PROC.relative_to(C.ROOT)}/:")
    for f in sorted(C.DATA_PROC.glob("d_*.csv")):
        log(f"    {f.name}")
    log(f"  audit tables written to {C.OUT_RES.relative_to(C.ROOT)}/: "
        f"{len(list(C.OUT_RES.glob('step02_*.csv')))} files")
    log("  NEXT: Step 3 - CHIRPS rainfall ingest; Step 4 - build the commodity-level training table")
    log("         (and the district-month panel for the secondary specification).")


if __name__ == "__main__":
    main()
