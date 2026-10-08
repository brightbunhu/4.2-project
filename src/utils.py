"""
src/utils.py
============
Shared helpers used by every pipeline step:

* consistent matplotlib / seaborn styling
* raw-file loaders with schema normalisation
* district / province canonical key standardisation
* the Spatial Price Index (the currency-safeguard for Zimbabwean food prices)
* rainfall calendar-month construction
* IQR outlier diagnostics
* a small plotting helper that always saves to outputs/figures
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import config as C  # noqa: E402

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import seaborn as sns  # noqa: E402

sns.set_theme(style="whitegrid", context="notebook")
plt.rcParams.update({
    "figure.dpi": 110, "savefig.dpi": 150, "savefig.bbox": "tight",
    "axes.titlesize": 13, "axes.labelsize": 11, "axes.titleweight": "bold",
    "figure.autolayout": False, "font.family": "DejaVu Sans",
    "axes.spines.top": False, "axes.spines.right": False,
})


# ======================================================================================
# SECTION 1 - CANONICAL KEYS
# ======================================================================================
_WS = re.compile(r"\s+")
# "Centenary/ Muzarabani" -> "CENTENARY MUZARABANI"; "Mhondoro-Ngezi" -> "MHONDORO NGEZI"
_DASH = re.compile(r"\s*[-/]\s*")


def canon(value) -> str:
    """Canonical UPPERCASE key for a place name.

    Rules (deliberately conservative - over-aggressive cleaning would silently merge
    genuinely different districts such as `Gokwe North` and `Gokwe South`):

    1. NaN / empty            -> ""            (unknown)
    2. strip leading/trailing whitespace, collapse internal runs of whitespace
    3. normalise the `/` and `-` used in "Centenary/ Muzarabani" and
       "Mhondoro-Ngezi" to a single space
    4. upper-case
    """
    if value is None or (isinstance(value, float) and np.isnan(value)) or pd.isna(value):
        return ""
    s = str(value).strip()
    if not s:
        return ""
    s = _WS.sub(" ", s)
    s = _DASH.sub(" ", s)
    return s.upper()


def add_canon_keys(df: pd.DataFrame) -> pd.DataFrame:
    """Attach `province_key` and `district_key` canonical columns."""
    df = df.copy()
    if "admin1_name" in df.columns:
        df["province_key"] = df["admin1_name"].map(canon)
    if "admin2_name" in df.columns:
        df["district_key"] = df["admin2_name"].map(canon)
    return df


# ======================================================================================
# SECTION 2 - LOADERS
# ======================================================================================
def _finalise(df: pd.DataFrame) -> pd.DataFrame:
    """Coerce HDX string dates to datetime and attach canonical keys."""
    for c in C.TIME_COLS:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce")
    return add_canon_keys(df)


def load_food_price() -> pd.DataFrame:
    """WFP Food Prices & Market Monitor - 25,554 rows, district x market x commodity x month."""
    df = pd.read_csv(C.RAW_FILES["food_price"], low_memory=False)
    df = _finalise(df)
    # calendar month anchor (reference_period_start is always the 15th for monthly series)
    df["month"] = df["reference_period_start"].dt.to_period("M").dt.to_timestamp()
    df["year"] = df["reference_period_start"].dt.year
    df["month_num"] = df["reference_period_start"].dt.month
    df["is_food"] = df["commodity_category"].isin(C.FOOD_CATEGORIES)
    return df


def load_poverty() -> pd.DataFrame:
    """OPHI/World Bank MPI survey - 33 rows, 10 provinces x 3 waves + 3 national rows."""
    df = pd.read_csv(C.RAW_FILES["poverty"], low_memory=False)
    df = _finalise(df)
    df["survey_year"] = df["reference_period_start"].dt.year
    return df


def load_rainfall() -> pd.DataFrame:
    """WFP FEWS NET rainfall - 5,100 rows, 10 provinces x 170 dekads x 3 aggregations."""
    df = pd.read_csv(C.RAW_FILES["rainfall"], low_memory=False)
    df = _finalise(df)
    df["dekad_start"] = df["reference_period_start"]
    df["dekad_end"] = df["reference_period_end"]
    return df


def load_population() -> pd.DataFrame:
    """UNFPA baseline population - 5,508 rows, district x gender x age band, 2023 vintage."""
    df = pd.read_csv(C.RAW_FILES["population"], low_memory=False)
    return _finalise(df)


def load_boundaries(level: str = "adm2"):
    """geoBoundaries polygons (CC BY 4.0 IGO)."""
    import geopandas as gpd
    return gpd.read_file(C.GEO_FILES[level]).rename(columns={"shapeName": "shape_name"})


def district_lookup() -> pd.DataFrame:
    """Authoritative district -> province -> area table (91 rows).

    Built from the ADM2 polygons (area, centroid) joined to ADM1 by point-in-polygon.
    Verified: the resulting province assignment matches the UNFPA file's own
    `admin1_name` for 91/91 districts, and areas sum to 390,772 km2 vs the official
    390,757 km2.
    """
    import geopandas as gpd

    cache = C.DATA_PROC / "_district_lookup.parquet"
    if cache.exists():
        return pd.read_parquet(cache)

    adm1, adm2 = load_boundaries("adm1"), load_boundaries("adm2")

    # equal-area projection -> trustworthy km2
    adm2_eq = adm2.to_crs(C.EQUAL_AREA_CRS)
    area = adm2_eq.geometry.area / 1e6

    centroids = adm2.geometry.centroid
    cx = np.asarray(centroids.x, dtype="float64")
    cy = np.asarray(centroids.y, dtype="float64")
    pts = gpd.GeoDataFrame(
        {"district": adm2["shape_name"].astype(str).values, "cx": cx, "cy": cy},
        geometry=gpd.points_from_xy(cx, cy), crs=adm2.crs)
    prov = gpd.GeoDataFrame(adm1[["shape_name"]].rename(columns={"shape_name": "province_geo"}),
                            geometry=adm1.geometry.values, crs=adm1.crs)
    sj = gpd.sjoin(pts, prov, how="left", predicate="within")

    out = pd.DataFrame({
        "district": sj["district"].values,
        "district_key": [canon(d) for d in sj["district"]],
        "province_geo": sj["province_geo"].values,
        "lon": cx, "lat": cy,
        "area_km2": area.values,
    }).sort_values("district_key").reset_index(drop=True)
    out["province_key"] = out["province_geo"].map(canon)
    out.to_parquet(cache, index=False)
    return out


def save_fig(fig, name: str, subdir: Path | None = None) -> Path:
    """Save a matplotlib figure to outputs/figures and close it."""
    d = subdir or C.OUT_FIG
    d.mkdir(parents=True, exist_ok=True)
    p = d / (name if name.endswith(".png") else f"{name}.png")
    fig.savefig(p)
    plt.close(fig)
    print(f"    [figure] {p.relative_to(C.ROOT)}")
    return p


def banner(step: str, title: str) -> None:
    print("\n" + "=" * 96)
    print(f"  {step}  {title}")
    print("=" * 96)


def save_df(df: pd.DataFrame, name: str, subdir: Path | None = None) -> Path:
    d = subdir or C.OUT_RES
    d.mkdir(parents=True, exist_ok=True)
    p = d / (name if name.endswith(".csv") else f"{name}.csv")
    df.to_csv(p, index=False)
    print(f"    [result ] {p.relative_to(C.ROOT)}  shape={df.shape}")
    return p


def write_text(text: str, name: str, subdir: Path | None = None) -> Path:
    d = subdir or C.REPORTS
    d.mkdir(parents=True, exist_ok=True)
    p = d / (name if name.endswith(".md") else f"{name}.md")
    p.write_text(text, encoding="utf-8")
    print(f"    [report ] {p.relative_to(C.ROOT)}")
    return p


def inspect_columns(df: pd.DataFrame) -> dict:
    """Classify every column as geographic / temporal / numeric / categorical / constant."""
    out = {"geo": [], "time": [], "numeric": [], "categorical": [], "constant": [], "id_like": []}
    n = len(df)
    for c in df.columns:
        nun = df[c].nunique(dropna=True)
        if c in C.GEO_COLS or c.startswith(("admin", "provider_admin")):
            out["geo"].append(c)
        elif c in C.TIME_COLS or c.endswith(("_start", "_end")) or c in ("month", "year", "month_num"):
            out["time"].append(c)
        elif pd.api.types.is_numeric_dtype(df[c]):
            (out["constant"] if nun <= 1 else out["numeric"]).append(c)
        else:
            (out["constant"] if nun <= 1 else out["categorical"]).append(c)
    return out


# ======================================================================================
# SECTION 3 - MISSING-VALUE STRATEGY  (documented, not improvised)
# ======================================================================================
def missing_report(df: pd.DataFrame, name: str, top: int | None = None) -> pd.DataFrame:
    r = pd.DataFrame({"n_missing": df.isna().sum(),
                      "pct_missing": (df.isna().mean() * 100).round(2),
                      "n_unique": df.nunique(dropna=True),
                      "dtype": [str(t) for t in df.dtypes]})
    r = r[r.n_missing > 0].sort_values("pct_missing", ascending=False)
    if top:
        r = r.head(top)
    print(f"\n  -- {name}: missing values in {int((df.isna().sum() > 0).sum())} columns "
          f"({int(df.isna().sum().sum()):,} cells of {df.size:,} = "
          f"{100 * df.isna().sum().sum() / df.size:.2f}%) --")
    print(r.to_string() if len(r) else "     none")
    return r


# ======================================================================================
# SECTION 4 - OUTLIER DIAGNOSTICS (IQR)
# ======================================================================================
def iqr_outliers(s: pd.Series, k: float = 1.5) -> pd.DataFrame:
    """IQR outlier bounds and count for one numeric series.

    RETENTION POLICY (see assumption A11): outliers are reported, never silently deleted.
    Extreme ZWL prices are genuine hyperinflation artefacts of the measurement system and
    seasonal rainfall extremes are physically real. The tree-based models are robust to
    them, and every price-derived feature is either a within-month ratio (SPI) or a
    rank/robust statistic, which already neutralises the influence of extreme levels.
    """
    s = pd.to_numeric(s, errors="coerce").dropna()
    if s.empty:
        return pd.DataFrame()
    q1, q3 = s.quantile(0.25), s.quantile(0.75)
    iqr = q3 - q1
    lo, hi = q1 - k * iqr, q3 + k * iqr
    n_out = int(((s < lo) | (s > hi)).sum())
    return pd.DataFrame([{"variable": s.name, "n": len(s), "q1": q1, "q3": q3, "iqr": iqr,
                          "lower_bound": lo, "upper_bound": hi,
                          "n_outliers": n_out, "pct_outliers": 100 * n_out / len(s),
                          "min": s.min(), "max": s.max(),
                          "skew": s.skew(), "kurtosis": s.kurtosis(),
                          "decision": "RETAINED (see assumption A11)"}])


# ======================================================================================
# SECTION 5 - THE SPATIAL PRICE INDEX  (core methodological safeguard, see A5)
# ======================================================================================
def spatial_price_index(prices: pd.DataFrame, by: str = "market",
                        winsor: tuple[float, float] = (0.01, 0.99)) -> pd.DataFrame:
    """Attach a currency- and inflation-safe Spatial Price Index (SPI) to price rows.

    Definition
    ----------
        SPI(i, c, m) = price(i, c, m) / median( price(j, c, m) : j in districts )

    where the median is taken over districts *within the same commodity, the same calendar
    month and the same currency*.

    Why this works
    --------------
    Both the numerator and the denominator are prices for the *same commodity* in the
    *same month* denominated in the *same currency*. Hyperinflation and the April-2024
    redenomination therefore cancel exactly, leaving a pure spatial signal:

        SPI = 1.00  ->  this district is at the national median price
        SPI = 1.25  ->  25% more expensive than the national median
        SPI = 0.80  ->  20% cheaper than the national median

    Aggregating SPI across commodities gives the **Staple Basket Price Index (SBPI)**,
    the district's cost-of-living pressure relative to the rest of Zimbabwe, which is the
    economically correct quantity for a food-insecurity risk model.

    Two safeguards, both necessary on this dataset
    ----------------------------------------------
    1. THIN-CELL GUARD - if fewer than `SPI_MIN_DISTRICTS` districts report a given
       (commodity, month, currency) cell, the median is not a meaningful national reference
       and the SPI is set to NaN rather than defaulting to 1.0 (which it would be by
       construction for a single reporting district - a silent artefact).

    2. WINSORISATION at the pooled [1%, 99%] quantiles of the SPI. A small number of
       `price_flag == 'actual'` USD quotes collected in 2024 at the border districts
       Beitbridge and Mangwe are implausible by an order of magnitude (e.g. sugar quoted at
       USD 25.0/kg against a national median of USD 1.50/kg; dried kapenta at USD 300/kg).
       Without winsorisation the SPI max is 30 and its 2024 standard deviation is 2.25
       versus 0.14-0.59 in every other year. With winsorisation 95% of raw SPI values
       already lie in [1/3, 3] and the remaining tail is clipped rather than driving
       district rankings. The number of winsorised rows is reported by the caller.
    """
    d = prices.copy()
    if by == "district":
        # collapse markets -> district x month x commodity x currency using the MEDIAN
        key = ["district_key", "month", "commodity_name", "currency_code"]
        if "market_name" in d.columns:
            d = (d.groupby(key, as_index=False)
                   .agg(price=("price", "median"),
                        admin1_name=("admin1_name", "first"),
                        commodity_category=("commodity_category", "first"),
                        is_food=("is_food", "first"), unit=("unit", "first"),
                        price_flag=("price_flag", "first"),
                        n_markets=("market_name", "nunique"),
                        n_price_obs=("price", "size")))
    else:
        # `d` is already at the intended analysis grain (e.g. district-month-commodity)
        key = ["month", "commodity_name", "currency_code"]

    # The national reference must be the median over DISTRICTS, so `district_key` must NOT
    # be part of the reference-grouping key even when it is part of the output grain.
    ref_key = [k for k in key if k != "district_key"]
    grp = d.groupby(ref_key, observed=True)["price"]
    d["country_median_price"] = grp.transform("median")
    if "district_key" in d.columns:
        d["n_districts_reporting"] = d.groupby(ref_key, observed=True)["district_key"] \
                                       .transform("nunique")
    else:
        d["n_districts_reporting"] = grp.transform("size")

    too_thin = d["n_districts_reporting"] < C.SPI_MIN_DISTRICTS
    d.loc[too_thin, "country_median_price"] = np.nan
    d["price_spi_raw"] = d["price"] / d["country_median_price"]
    d["spi_pct_dev"] = (d["price_spi_raw"] - 1.0) * 100.0

    lo, hi = d["price_spi_raw"].quantile([winsor[0], winsor[1]])
    d["price_spi"] = d["price_spi_raw"].clip(lower=lo, upper=hi)
    d["spi_winsorised"] = (d["price_spi_raw"] != d["price_spi"]).fillna(False)
    d.attrs["winsor_bounds"] = (float(lo), float(hi))
    return d


def build_basket_index(prices_spi: pd.DataFrame,
                       commodities: Iterable[str] | None = None) -> pd.DataFrame:
    """District-month Staple Basket Price Index, averaged over the food commodities.

    Returns one row per (district, month) with:
        sbpi          mean SPI across available food commodities
        sbpi_core     mean SPI across the CORE_COMMODITIES subset (falls back to sbpi)
        sbpi_max      worst (most expensive) food commodity that month
        n_commodities how many food commodities actually contributed
    """
    d = prices_spi[prices_spi["is_food"] & prices_spi["price_spi"].notna()].copy()
    if commodities:
        d = d[d["commodity_name"].isin(list(commodities))]
    g = d.groupby(["district_key", "admin1_name", "month"], observed=True)
    out = g["price_spi"].agg(sbpi="mean", sbpi_max="max", n_commodities="count").reset_index()

    core = prices_spi[prices_spi["commodity_name"].isin(C.CORE_COMMODITIES)
                      & prices_spi["price_spi"].notna()]
    cb = core.groupby(["district_key", "month"], observed=True)["price_spi"].mean()
    out = out.merge(cb.rename("sbpi_core").reset_index(),
                    on=["district_key", "month"], how="left")
    out["sbpi_core"] = out["sbpi_core"].fillna(out["sbpi"])
    return out


# ======================================================================================
# SECTION 6 - RAINFALL -> CALENDAR MONTH
# ======================================================================================
def rainfall_calendar_monthly(rf: pd.DataFrame) -> pd.DataFrame:
    """Convert the dekad-anchored '1-month' rainfall series into a clean province-month panel.

    The WFP product publishes three windows on every dekad (1st, 11th, 21st):
    `dekad` (10 days), `1-month` (30-day look-back) and `3-month` (90-day look-back), all
    ending on the dekad end date (assumption A7). Three `1-month` windows therefore end
    inside each calendar month; taking their mean gives a calendar-month rainfall depth
    that is an average of three overlapping 30-day windows - the best available estimate
    and one that avoids summing overlapping windows (which would triple-count).

    Validated: the resulting 2022-2026 climatology reproduces the documented Zimbabwe
    rainfall regime (wet season Nov-Mar, dry season Jun-Sep).
    """
    m = rf[rf["aggregation_period"] == "1-month"].copy()
    m["month"] = m["dekad_end"].dt.to_period("M").dt.to_timestamp()
    out = (m.groupby(["province_key", "admin1_name", "month"], observed=True)
             .agg(rainfall=("rainfall", "mean"),
                  rain_lta=("rainfall_long_term_average", "mean"),
                  rain_anom_pct=("rainfall_anomaly_pct", "mean"),
                  n_dekad=("rainfall", "size"))
             .reset_index())
    # tidy rounded public-facing values
    out["rainfall"] = out["rainfall"].round(4)
    out["rain_lta"] = out["rain_lta"].round(4)
    out["rain_anom_pct"] = out["rain_anom_pct"].round(4)
    return out.sort_values(["province_key", "month"]).reset_index(drop=True)


def add_rolling(panel: pd.DataFrame, value: str, group: str,
                windows: Iterable[int], suffix_fmt: str = "{v}_{w}m") -> pd.DataFrame:
    """Rolling SUM over calendar-month windows, per group, sorted by month."""
    p = panel.sort_values([group, "month"]).copy()
    for w in windows:
        p[suffix_fmt.format(v=value, w=w)] = (p.groupby(group, observed=True)[value]
                                              .rolling(w, min_periods=w).sum()
                                              .reset_index(level=0, drop=True))
    return p


def add_lags(panel: pd.DataFrame, value: str, group: str,
             lags: Iterable[int], suffix_fmt: str = "{v}_lag{l}") -> pd.DataFrame:
    """Lag features (value at T-k), per group, sorted by month."""
    p = panel.sort_values([group, "month"]).copy()
    for k in lags:
        p[suffix_fmt.format(v=value, l=k)] = p.groupby(group, observed=True)[value].shift(k)
    return p


def rolling_stats(panel: pd.DataFrame, group: str, value: str, window: int,
                  pcts=(0.25, 0.75)) -> pd.DataFrame:
    """Rolling mean / median / std / cv / range / pct_change for one value."""
    g = panel.groupby(group, observed=True)[value]
    r = pd.DataFrame(index=panel.index)
    s = panel[value]
    r[f"{value}_mean{window}m"] = g.rolling(window, min_periods=max(2, window // 2)).mean()
    r[f"{value}_std{window}m"] = g.rolling(window, min_periods=max(2, window // 2)).std()
    r[f"{value}_cv{window}m"] = (r[f"{value}_std{window}m"] / r[f"{value}_mean{window}m"]).abs()
    r[f"{value}_min{window}m"] = g.rolling(window, min_periods=max(2, window // 2)).min()
    r[f"{value}_max{window}m"] = g.rolling(window, min_periods=max(2, window // 2)).max()
    r[f"{value}_range{window}m"] = r[f"{value}_max{window}m"] - r[f"{value}_min{window}m"]
    # percentage change over the window vs the value one window earlier
    prev = g.shift(window)
    r[f"{value}_pctchg{window}m"] = np.where(
        (prev.abs() > 1e-9) & prev.notna(), (s - prev) / prev * 100.0, np.nan)
    lo, hi = pcts
    r[f"{value}_iqr{window}m"] = (g.rolling(window, min_periods=max(2, window // 2))
                                  .quantile(hi) - g.rolling(window, min_periods=max(2, window // 2)).quantile(lo))
    return r


# ======================================================================================
# SECTION 7 - MISC
# ======================================================================================
def describe_full(s: pd.Series) -> dict:
    """Full descriptive statistics for one numeric series."""
    s = pd.to_numeric(s, errors="coerce").dropna()
    if s.empty:
        return {}
    modes = s.mode()
    return {
        "n": int(s.size), "mean": s.mean(), "median": s.median(),
        "mode": float(modes.iloc[0]) if len(modes) else np.nan,
        "n_modes": int(len(modes)),
        "std": s.std(ddof=1), "variance": s.var(ddof=1),
        "min": s.min(), "q1": s.quantile(.25), "q3": s.quantile(.75),
        "max": s.max(), "range": s.max() - s.min(), "iqr": s.quantile(.75) - s.quantile(.25),
        "skewness": s.skew(), "kurtosis": s.kurtosis(),
        "cv": s.std(ddof=1) / s.mean() if s.mean() else np.nan,
    }


def describe_table(df: pd.DataFrame, cols: Iterable[str] | None = None, round_to: int = 4) -> pd.DataFrame:
    cols = list(cols) if cols else [c for c in df.columns
                                     if pd.api.types.is_numeric_dtype(df[c]) and df[c].nunique() > 1]
    rows = {c: describe_full(df[c]) for c in cols if df[c].notna().any()}
    return pd.DataFrame(rows).T.round(round_to)


def metric_block(y_true, y_pred, y_proba=None) -> dict:
    """All Step-10 metrics for the positive (high-risk) class, computed consistently."""
    from sklearn.metrics import (accuracy_score, average_precision_score, balanced_accuracy_score,
                                 brier_score_loss, confusion_matrix, f1_score, precision_score,
                                 recall_score, roc_auc_score)
    out = {
        "accuracy": accuracy_score(y_true, y_pred),
        "balanced_accuracy": balanced_accuracy_score(y_true, y_pred),
        "precision_high_risk": precision_score(y_true, y_pred, zero_division=0),
        "recall_high_risk": recall_score(y_true, y_pred, zero_division=0),
        "f1_high_risk": f1_score(y_true, y_pred, zero_division=0),
        "macro_f1": f1_score(y_true, y_pred, average="macro", zero_division=0),
    }
    if y_proba is not None and len(np.unique(y_true)) > 1:
        out["roc_auc"] = roc_auc_score(y_true, y_proba)
        out["pr_auc"] = average_precision_score(y_true, y_proba)
        out["brier"] = brier_score_loss(y_true, y_proba)
    else:
        out["roc_auc"] = out["pr_auc"] = out["brier"] = np.nan
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    out.update({"TN": int(tn), "FP": int(fp), "FN": int(fn), "TP": int(tp)})
    return out