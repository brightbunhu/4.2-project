"""
ingest_chirps_district_month.py
===============================
Convert the global CHIRPS v3 monthly NetCDF (`yr.nc`) into a district x month
rainfall table for Zimbabwe.

Method
------
1. Subset the global grid to the Zimbabwe bounding box (lon 25-34, lat -23 - -15).
2. Build a point per grid cell and spatially join each point to an ADM2 district
   polygon (names in the geoBoundaries file match `d_district_base.district` exactly).
3. Area-weight each cell by cos(latitude) and take the weighted mean of `precip`
   per district per month (mm/month).
4. Derive long-term climatology (1991-2020) and % anomaly per district-calendar-month.

Output
------
data/processed/d_rainfall_chirps_district_month.csv  (district x month)
Columns: district_key, district, province, month, rainfall_mm, rain_lta,
         rain_anom_pct, n_cells
"""
import sys
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import xarray as xr

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config as C

NC_PATH = C.CHIRPS_NC
OUT = C.PROC_RAINFALL_DISTRICT

LAT_SLICE = slice(-23.0, -15.0)
LON_SLICE = slice(25.0, 34.0)

# --------------------------------------------------------------------------------------
# 1. Load the subset of CHIRPS (lazy -> only Zimbabwe is read into memory)
# --------------------------------------------------------------------------------------
print("Opening", NC_PATH)
ds = xr.open_dataset(NC_PATH)
sub = ds.sel(latitude=LAT_SLICE, longitude=LON_SLICE)
print("Zimbabwe subset:", dict(sub.sizes))

# Only keep months that align to the first of the month.
times = pd.to_datetime(sub["time"].values).to_period("M").to_timestamp()
if not (times == pd.to_datetime(sub["time"].values)).all():
    print("WARNING: some time steps are not month-aligned.")

lat = sub["latitude"].values
lon = sub["longitude"].values

# --------------------------------------------------------------------------------------
# 2. Spatial join: assign every grid cell to an ADM2 district
# --------------------------------------------------------------------------------------
adm2 = gpd.read_file(C.GEO_FILES["adm2"])[["shapeName", "geometry"]]
adm2 = adm2.rename(columns={"shapeName": "district"})

lon2d, lat2d = np.meshgrid(lon, lat)
pts = gpd.GeoDataFrame(
    {"latitude": lat2d.ravel(), "longitude": lon2d.ravel()},
    geometry=gpd.points_from_xy(lon2d.ravel(), lat2d.ravel()),
    crs="EPSG:4326",
)
pts["cell"] = np.arange(len(pts))  # stable flat grid index for precipitation lookup
joined = gpd.sjoin(pts, adm2, how="inner", predicate="within")
print(f"grid cells: {len(pts)}; matched to a district: {len(joined)}")
print("districts receiving cells:", joined["district"].nunique())

# Fallback: tiny urban districts (e.g. Mvurwi) can contain no grid-cell centre at
# 0.05 deg. Assign the single nearest cell to their polygon centroid so every
# district is represented. Documented limitation: this cell may be shared with a
# neighbouring district.
all_districts = set(adm2["district"])
matched_districts = set(joined["district"])
missing = sorted(all_districts - matched_districts)
if missing:
    print("districts with no cell (nearest-cell fallback):", missing)
    for d in missing:
        poly = adm2.loc[adm2["district"] == d, "geometry"].iloc[0]
        cen = poly.representative_point()
        d2 = (pts.geometry.x - cen.x) ** 2 + (pts.geometry.y - cen.y) ** 2
        nearest = pts.loc[d2.idxmin()]
        row = {"latitude": nearest["latitude"], "longitude": nearest["longitude"],
               "geometry": nearest["geometry"], "district": d,
               "cell": int(nearest["cell"])}
        joined = pd.concat([joined, gpd.GeoDataFrame([row], crs=joined.crs)],
                           ignore_index=True)

# cos(lat) weight per matched cell (equal-area approximation for the small lat span).
joined["weight"] = np.cos(np.deg2rad(joined["latitude"].astype(float)))
# De-duplicate (the fallback cell can collide with an existing cell-district pair).
joined = joined.drop_duplicates(subset=["cell", "district"]).reset_index(drop=True)

# --------------------------------------------------------------------------------------
# 3. Area-weighted district monthly means
# --------------------------------------------------------------------------------------
# precip shape: (time, lat, lon) -> flatten space to (time, n_cells)
precip = sub["precip"].transpose("time", "latitude", "longitude").values
precip = precip.reshape(len(times), -1)

# Each matched row contributes weight `w` of cell `c` to one district.
row_cell = joined["cell"].to_numpy()
row_w = joined["weight"].to_numpy()
districts = sorted(joined["district"].unique())
district_idx = {d: i for i, d in enumerate(districts)}
row_dist = joined["district"].map(district_idx).to_numpy()
D = len(districts)

onehot = np.zeros((len(joined), D), dtype=np.float32)
onehot[np.arange(len(joined)), row_dist] = 1.0
weighted = onehot * row_w[:, None]                  # (rows, districts)
denom = weighted.sum(axis=0)                        # (districts,)
numer = precip[:, row_cell] @ weighted              # (time, districts)
district_monthly = numer / denom[None, :]

# Long-form dataframe.
df = pd.DataFrame(district_monthly, columns=districts)
df.insert(0, "month", times)
long = df.melt(id_vars="month", var_name="district", value_name="rainfall_mm")

# Cell counts per district (quality indicator).
counts = joined.groupby("district").size().rename("n_cells").reset_index()
long = long.merge(counts, on="district", how="left")

# --------------------------------------------------------------------------------------
# 4. Rolling totals, climatology (1991-2020) and % anomalies per district-month
# --------------------------------------------------------------------------------------
long = long.sort_values(["district", "month"]).reset_index(drop=True)

# Rolling totals on the full continuous monthly record (per district).
for w in (3, 6, 12):
    long[f"rainfall_{w}m_total"] = (
        long.groupby("district")["rainfall_mm"]
        .rolling(w, min_periods=w).sum().reset_index(level=0, drop=True)
    )

long["year"] = long["month"].dt.year
long["cal_month"] = long["month"].dt.month
base = long[(long["year"] >= 1991) & (long["year"] <= 2020)]

# Monthly climatology and % anomaly.
lta = (base.groupby(["district", "cal_month"])["rainfall_mm"]
       .mean().rename("rain_lta").reset_index())
long = long.merge(lta, on=["district", "cal_month"], how="left")
long["rain_anom_pct"] = np.where(
    long["rain_lta"] > 0,
    (long["rainfall_mm"] - long["rain_lta"]) / long["rain_lta"] * 100.0, np.nan)

# 3-month-total climatology and % anomaly (the requested rainfall_3m_anomaly).
lta3 = (base.groupby(["district", "cal_month"])["rainfall_3m_total"]
        .mean().rename("rain3m_lta").reset_index())
long = long.merge(lta3, on=["district", "cal_month"], how="left")
long["rainfall_3m_anomaly"] = np.where(
    long["rain3m_lta"] > 0,
    (long["rainfall_3m_total"] - long["rain3m_lta"]) / long["rain3m_lta"] * 100.0,
    np.nan)

# Attach canonical district_key / province.
db = pd.read_csv(C.DATA_PROC / "d_district_base.csv")[
    ["district", "district_key", "province"]
]
long = long.merge(db, on="district", how="left")

out = long[[
    "district_key", "district", "province", "month",
    "rainfall_mm", "rain_lta", "rain_anom_pct",
    "rainfall_3m_total", "rainfall_6m_total", "rainfall_12m_total",
    "rainfall_3m_anomaly", "n_cells",
]].sort_values(["district", "month"]).reset_index(drop=True)

out.to_csv(OUT, index=False)
print(f"\nSaved {OUT}")
print(f"rows: {len(out):,}  districts: {out['district'].nunique()}  "
      f"months: {out['month'].dt.to_period('M').nunique()}")
print(f"date range: {out['month'].min().date()} -> {out['month'].max().date()}")
print("missing rainfall:", out["rainfall_mm"].isna().sum())
print(out.head().to_string())
