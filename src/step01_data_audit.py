"""
step01_data_audit.py
====================
STEP 1 - RAW DATA AUDIT.

Profile every raw source (shape, dtypes, missingness, duplicates, key columns) and write a
machine-readable audit plus a human-readable report. No cleaning is done here; this step only
establishes exactly what we have before any transformation.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config as C  # noqa: E402
from src.utils import banner, inspect_columns, missing_report, save_df, write_text


def audit_table(name: str, df: pd.DataFrame) -> pd.DataFrame:
    """Return a per-column audit frame for one dataset."""
    rows = []
    dup = int(df.duplicated().sum())
    for col in df.columns:
        s = df[col]
        rows.append({
            "dataset": name,
            "column": col,
            "dtype": str(s.dtype),
            "n_missing": int(s.isna().sum()),
            "pct_missing": round(100 * s.isna().mean(), 2),
            "n_unique": int(s.nunique(dropna=True)),
            "duplicate_rows": dup,
        })
    return pd.DataFrame(rows)


def main() -> None:
    banner("1", "RAW DATA AUDIT")

    datasets = {name: pd.read_csv(path) for name, path in C.RAW_FILES.items()}

    print("\noverview")
    for name, df in datasets.items():
        print(f"  {name:12s} rows={len(df):>7,}  cols={df.shape[1]:>3}  "
              f"dupes={df.duplicated().sum():>5}")

    print("\nkey columns")
    for name, df in datasets.items():
        keys = inspect_columns(df)
        print(f"  {name}: {keys}")

    # Combined per-column audit.
    audit = pd.concat([audit_table(n, d) for n, d in datasets.items()], ignore_index=True)
    save_df(audit, "step01_column_audit")

    for name, df in datasets.items():
        missing_report(df, f"step01_missing_{name}")

    # Boundaries summary.
    geo_lines = []
    try:
        import geopandas as gpd
        for lvl, path in C.GEO_FILES.items():
            g = gpd.read_file(path)
            geo_lines.append(f"| {lvl} | {len(g)} | {g.crs} |")
            print(f"  {lvl}: {len(g)} features, CRS={g.crs}")
    except Exception as exc:  # pragma: no cover
        geo_lines.append(f"| (geo) | error | {exc} |")

    # Report.
    lines = ["# Step 1 - Raw Data Audit", ""]
    lines.append("## Source overview")
    lines.append("| Dataset | Rows | Columns | Duplicate rows |")
    lines.append("|---|---|---|---|")
    for name, df in datasets.items():
        lines.append(f"| {name} | {len(df):,} | {df.shape[1]} | {df.duplicated().sum()} |")
    lines.append("")
    lines.append("## Boundary layers")
    lines.append("| Level | Features | CRS |")
    lines.append("|---|---|---|")
    lines.extend(geo_lines)
    lines.append("")
    lines.append("## Missingness (columns with any nulls)")
    for name, df in datasets.items():
        nz = df.isna().sum()
        nz = nz[nz > 0]
        if len(nz):
            lines.append(f"**{name}**: " + ", ".join(f"`{c}`={v}" for c, v in nz.items()))
        else:
            lines.append(f"**{name}**: no missing values.")
        lines.append("")
    write_text("\n".join(lines), "step01_data_audit", C.REPORTS)

    banner("1", "AUDIT COMPLETE -> reports/step01_data_audit.md")


if __name__ == "__main__":
    main()
