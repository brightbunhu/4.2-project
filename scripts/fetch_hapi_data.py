"""Fetch the raw HDX HAPI datasets used by the ZCPSC pipeline.

Downloads the four keyless HDX HAPI sources (food prices, poverty rate, rainfall,
baseline population) for Zimbabwe into a timestamped staging folder and writes a
fetch manifest (row counts, params, sha256). Optionally installs them over the
canonical data/raw files (with a timestamped backup).

Usage:
    python scripts/fetch_hapi_data.py --start-date 2017-01-01 --end-date 2026-05-31
    python scripts/fetch_hapi_data.py --install
    python scripts/fetch_hapi_data.py --datasets food_price rainfall
"""
from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
try:
    import config as C

    CANON = {k: Path(v) for k, v in C.RAW_FILES.items()}
except Exception:
    CANON = {}

HAPI_BASE = "https://hapi.humdata.org/api/v2"
PAGE_LIMIT = 10000

DATASETS = {
    "food_price": ("food-security-nutrition-poverty/food-prices-market-monitor", "hdx_hapi_food_price_zwe.csv"),
    "poverty": ("food-security-nutrition-poverty/poverty-rate", "hdx_hapi_poverty_rate_zwe.csv"),
    "rainfall": ("climate/rainfall", "hdx_hapi_rainfall_zwe.csv"),
    "population": ("geography-infrastructure/baseline-population", "hdx_hapi_population_zwe.csv"),
}


def build_identifier(app_name: str, app_email: str) -> str:
    env = os.environ.get("HAPI_APP_IDENTIFIER")
    if env:
        return env
    return base64.b64encode(f"{app_name}:{app_email}".encode("utf-8")).decode("ascii")


def fetch_page(endpoint: str, params: dict) -> dict:
    url = f"{HAPI_BASE}/{endpoint}?" + urlencode(params)
    req = Request(
        url,
        headers={
            "X-HDX-HAPI-APP-IDENTIFIER": params["app_identifier"],
            "Accept": "application/json",
            "User-Agent": "ZCPSC-data-fetch/1.0",
        },
    )
    with urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_dataset(endpoint: str, app_id: str, start: str | None, end: str | None, max_rows: int) -> list:
    rows: list = []
    offset = 0
    while True:
        params = {
            "app_identifier": app_id,
            "location_code": "ZWE",
            "output_format": "json",
            "limit": PAGE_LIMIT,
            "offset": offset,
        }
        if start:
            params["start_date"] = start
        if end:
            params["end_date"] = end
        payload = fetch_page(endpoint, params)
        data = payload.get("data", []) or []
        rows.extend(data)
        if len(data) < PAGE_LIMIT or len(rows) >= max_rows:
            break
        offset += PAGE_LIMIT
    return rows[:max_rows]


def write_csv(path: Path, rows: list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    seen = set(fieldnames)
    for r in rows:
        for k in r.keys():
            if k not in seen:
                seen.add(k)
                fieldnames.append(k)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser(description="Fetch HDX HAPI raw data for ZCPSC.")
    ap.add_argument("--datasets", nargs="+", choices=list(DATASETS), default=list(DATASETS))
    ap.add_argument("--start-date", default="2017-01-01")
    ap.add_argument("--end-date", default=None)
    ap.add_argument("--out-dir", default=str(ROOT / "data" / "raw" / "hapi_live"))
    ap.add_argument("--max-rows", type=int, default=500000)
    ap.add_argument("--app-name", default="ZCPSC-dashboard")
    ap.add_argument("--app-email", default="zcpsc@example.com")
    ap.add_argument("--install", action="store_true", help="copy results over data/raw canonical files (with backup)")
    ap.add_argument("--dry-run", action="store_true", help="print request targets without downloading")
    args = ap.parse_args()

    app_id = build_identifier(args.app_name, args.app_email)
    run_stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    staging = Path(args.out_dir) / run_stamp

    if args.dry_run:
        for key in args.datasets:
            endpoint, name = DATASETS[key]
            print(f"[dry-run] {key:11s} -> {HAPI_BASE}/{endpoint} -> {staging / name}")
        return 0

    manifest = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "location_code": "ZWE",
        "start_date": args.start_date,
        "end_date": args.end_date,
        "staging_dir": str(staging),
        "datasets": {},
    }

    failures = 0
    for key in args.datasets:
        endpoint, name = DATASETS[key]
        print(f"fetching {key} ({endpoint}) ...", flush=True)
        try:
            rows = fetch_dataset(endpoint, app_id, args.start_date, args.end_date, args.max_rows)
            out = staging / name
            write_csv(out, rows)
            manifest["datasets"][key] = {
                "endpoint": f"{HAPI_BASE}/{endpoint}",
                "file": str(out),
                "rows": len(rows),
                "sha256": sha256(out),
                "columns": list(rows[0].keys()) if rows else [],
            }
            print(f"  {len(rows):>7,} rows -> {out}")
            if len(rows) == 0:
                print("  WARNING: zero rows returned")
        except (HTTPError, URLError, TimeoutError) as exc:
            failures += 1
            manifest["datasets"][key] = {"endpoint": f"{HAPI_BASE}/{endpoint}", "error": str(exc)}
            print(f"  ERROR: {exc}")

    staging.mkdir(parents=True, exist_ok=True)
    manifest_path = staging / "fetch_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"manifest -> {manifest_path}")

    if args.install:
        install_stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        for key, meta in manifest["datasets"].items():
            if "file" not in meta:
                continue
            src = Path(meta["file"])
            dst = CANON.get(key, ROOT / "data" / "raw" / DATASETS[key][1])
            if dst.exists():
                shutil.copy2(dst, dst.with_suffix(dst.suffix + f".bak_{install_stamp}"))
            shutil.copy2(src, dst)
            print(f"installed {src.name} -> {dst}")

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
