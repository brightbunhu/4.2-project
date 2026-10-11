"""Rebuild Option B stage counts and row-level reporting-gap attrition.

Uses only Python's standard library and the project's existing raw food-price
CSV. The rules mirror src/run_option_b_pipeline.py through its reporting-gap
filter; this script never writes to the project tree outside last/.
"""
from __future__ import annotations

import csv
import json
import math
import re
from collections import defaultdict
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw/hdx_hapi_food_price_zwe.csv"
FINAL = ROOT / "outputs/option_b/data/option_b_modelling_table.csv"
APRIL_ZWL = "2024-04"

WS = re.compile(r"\s+")
DASH = re.compile(r"\s*[-/]\s*")


def canon(value: str | None) -> str:
    """Match src/utils.py canon() for text fields from csv.DictReader."""
    if value is None or value.strip().lower() in {"", "nan", "none"}:
        return ""
    return DASH.sub(" ", WS.sub(" ", value.strip())).upper()


def month(value: str) -> date:
    y, m, _ = map(int, value[:10].split("-"))
    return date(y, m, 1)


def next_month(d: date) -> date:
    return date(d.year + (d.month == 12), 1 if d.month == 12 else d.month + 1, 1)


def median(values: list[float]) -> float:
    values = sorted(values)
    n = len(values)
    if n == 0:
        return math.nan
    mid = n // 2
    return values[mid] if n % 2 else (values[mid - 1] + values[mid]) / 2


def quantile_linear(values: list[float], q: float) -> float:
    """NumPy/pandas default linear quantile interpolation (method='linear')."""
    xs = sorted(values)
    pos = (len(xs) - 1) * q
    lo = math.floor(pos)
    hi = math.ceil(pos)
    return xs[lo] + (xs[hi] - xs[lo]) * (pos - lo)


def key_text(parts: tuple[str, ...]) -> str:
    return "|".join(parts)


def main() -> None:
    groups: dict[tuple[str, date, str, str], dict] = {}
    raw_quotes = april_removed = raw_district_blanks = 0
    raw_min_date = raw_max_date = None
    raw_unit_values: set[str] = set()
    raw_flag_values: set[str] = set()
    raw_type_values: set[str] = set()
    raw_currency_values: set[str] = set()
    group_units: dict[tuple, set[str]] = defaultdict(set)
    group_flags: dict[tuple, set[str]] = defaultdict(set)
    group_types: dict[tuple, set[str]] = defaultdict(set)

    with RAW.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            raw_quotes += 1
            observed_day = date.fromisoformat(row["reference_period_start"][:10])
            raw_min_date = observed_day if raw_min_date is None else min(raw_min_date, observed_day)
            raw_max_date = observed_day if raw_max_date is None else max(raw_max_date, observed_day)
            d = month(row["reference_period_start"])
            currency = row.get("currency_code", "") or ""
            if d.strftime("%Y-%m") == APRIL_ZWL and currency == "ZWL":
                april_removed += 1
                continue
            district = canon(row.get("admin2_name"))
            if not district:
                raw_district_blanks += 1
            commodity = row.get("commodity_name", "") or ""
            # pandas groupby(dropna=True) drops null values; blank strings remain keys.
            if not commodity or not currency:
                continue
            key = (district, d, commodity, currency)
            g = groups.setdefault(key, {"prices": [], "first": row, "n_markets": set(), "n_quotes": 0})
            try:
                price = float(row["price"])
            except (TypeError, ValueError):
                price = math.nan
            if math.isfinite(price):
                g["prices"].append(price)
                g["n_quotes"] += 1
            market = row.get("market_name", "") or ""
            if market:
                g["n_markets"].add(market)
            raw_unit_values.add(row.get("unit", "") or "")
            raw_flag_values.add(row.get("price_flag", "") or "")
            raw_type_values.add(row.get("price_type", "") or "")
            raw_currency_values.add(currency)
            if row.get("unit"):
                group_units[key].add(row["unit"])
            if row.get("price_flag"):
                group_flags[key].add(row["price_flag"])
            if row.get("price_type"):
                group_types[key].add(row["price_type"])

    # Market quotes -> district x month x commodity x currency median-price cells.
    agg = []
    for key, g in groups.items():
        if not g["prices"]:
            continue
        district, m, commodity, currency = key
        agg.append({"key": key, "district": district, "month": m,
                    "commodity": commodity, "currency": currency,
                    "price": median(g["prices"]), "n_markets": len(g["n_markets"]),
                    "n_quotes": g["n_quotes"], "unit": g["first"].get("unit", ""),
                    "price_flag": g["first"].get("price_flag", ""),
                    "price_type": g["first"].get("price_type", "")})

    # Within-month, commodity and currency peer median; exclude cells with <8 districts.
    refs: dict[tuple[date, str, str], list[dict]] = defaultdict(list)
    for row in agg:
        refs[(row["month"], row["commodity"], row["currency"])].append(row)
    valid = []
    price_audit_rows = []
    for ref_rows in refs.values():
        district_count = len({r["district"] for r in ref_rows})
        peer = median([r["price"] for r in ref_rows])
        units = sorted({r["unit"] for r in ref_rows if r["unit"]})
        flags = sorted({r["price_flag"] for r in ref_rows if r["price_flag"]})
        types = sorted({r["price_type"] for r in ref_rows if r["price_type"]})
        first = ref_rows[0]
        price_audit_rows.append({
            "month": first["month"].isoformat(), "commodity_name": first["commodity"],
            "currency_code": first["currency"], "n_reporting_districts": district_count,
            "peer_group_eligible_ge_8": int(district_count >= 8),
            "units_seen_after_cell_first_rule": json.dumps(units),
            "price_flags_seen_after_cell_first_rule": json.dumps(flags),
            "price_types_seen_after_cell_first_rule": json.dumps(types),
            "unit_comparable": "PASS" if len(units) <= 1 else "MIXED_UNITS",
            "price_flag_homogeneous": "PASS" if len(flags) <= 1 else "MIXED_FLAGS",
            "price_type_homogeneous": "PASS" if len(types) <= 1 else "MIXED_TYPES",
            "source_aggregation_rule": "median price per district/month/commodity/currency; unit and price_flag first; price_type not retained",
        })
        if district_count < 8 or not math.isfinite(peer) or peer == 0:
            continue
        for row in ref_rows:
            row["spi_raw"] = row["price"] / peer
            valid.append(row)

    lo = quantile_linear([r["spi_raw"] for r in valid], 0.01)
    hi = quantile_linear([r["spi_raw"] for r in valid], 0.99)
    for row in valid:
        row["spi"] = min(max(row["spi_raw"], lo), hi)
        row["stress"] = int(row["spi"] > 1.25)

    # T+1 pairs within district x commodity x currency; retain exact calendar month only.
    by_series: dict[tuple[str, str, str], list[dict]] = defaultdict(list)
    for row in valid:
        by_series[(row["district"], row["commodity"], row["currency"])].append(row)
    candidates = []
    for series, rows in by_series.items():
        rows.sort(key=lambda r: r["month"])
        for current, target in zip(rows, rows[1:]):
            if target["month"] == next_month(current["month"]):
                candidates.append({
                    "district_key": series[0], "commodity_name": series[1],
                    "currency_code": series[2], "prediction_month": current["month"],
                    "target_month": target["month"], "spi_at_t": current["spi"],
                    "spi_at_t_plus_1": target["spi"], "y_true": target["stress"],
                    "n_districts_reporting": len({r["district"] for r in refs[(current["month"], current["commodity"], current["currency"])]}),
                })

    candidates.sort(key=lambda r: (r["district_key"], r["commodity_name"],
                                   r["currency_code"], r["prediction_month"]))
    previous: dict[tuple[str, str, str], date] = {}
    for i, row in enumerate(candidates, 1):
        series = (row["district_key"], row["commodity_name"], row["currency_code"])
        prev = previous.get(series)
        gap_days = (row["prediction_month"] - prev).days if prev else None
        gap_months = round(gap_days / 30.44, 2) if gap_days is not None else None
        keep = gap_months is None or gap_months <= 2.0
        row["previous_candidate_prediction_month"] = prev.isoformat() if prev else ""
        row["months_since_previous_candidate"] = gap_months if gap_months is not None else ""
        row["candidate_natural_key"] = key_text((row["district_key"], row["commodity_name"],
                                                  row["prediction_month"].isoformat(), row["currency_code"]))
        row["observation_id_source_order"] = f"OBS_OPTB_{i:06d}"
        row["stage_aggregated_cell"] = 1
        row["stage_valid_spi"] = 1
        row["stage_exact_t_plus_1"] = 1
        row["stage_final_model_row_by_source_rule"] = int(keep)
        row["exclusion_reason"] = "" if keep else "months_since_last_reported_price > 2.0 (pipeline rule)"
        previous[series] = row["prediction_month"]

    # Compare keys retained by the source rule to the existing final Option B table.
    final_keys: set[tuple[str, str, date, str]] = set()
    final_rows = 0
    with FINAL.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            final_rows += 1
            final_keys.add((row.get("district_key", ""), row.get("commodity_name", ""),
                            month(row["prediction_month"]), row.get("currency_code", "")))
    for row in candidates:
        k = (row["district_key"], row["commodity_name"], row["prediction_month"], row["currency_code"])
        row["present_in_existing_final_table"] = int(k in final_keys)

    ledger_path = OUT / "attrition_ledger.csv"
    fieldnames = ["candidate_natural_key", "district_key", "commodity_name", "currency_code",
                  "prediction_month", "target_month", "spi_at_t", "spi_at_t_plus_1", "y_true",
                  "n_districts_reporting", "previous_candidate_prediction_month",
                  "months_since_previous_candidate", "stage_aggregated_cell", "stage_valid_spi",
                  "stage_exact_t_plus_1", "stage_final_model_row_by_source_rule",
                  "present_in_existing_final_table", "exclusion_reason"]
    with ledger_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in candidates:
            out = dict(row)
            out["prediction_month"] = out["prediction_month"].isoformat()
            out["target_month"] = out["target_month"].isoformat()
            writer.writerow({k: out.get(k, "") for k in fieldnames})

    with (OUT / "price_comparability_audit.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(price_audit_rows[0]))
        w.writeheader()
        w.writerows(price_audit_rows)

    # Report named market areas against the exact ADM2 names used by the rainfall
    # point-in-polygon code. Market rows themselves are name-coded; they are not
    # spatially joined to these polygons in the Option B pipeline.
    boundary_path = ROOT / "data/raw/geo/zwe_adm2_geoboundaries.geojson"
    with boundary_path.open(encoding="utf-8-sig") as f:
        boundary_doc = json.load(f)
    boundary_names = [canon(feature.get("properties", {}).get("shapeName"))
                      for feature in boundary_doc.get("features", [])]
    boundary_counts = defaultdict(int)
    for name in boundary_names:
        boundary_counts[name] += 1
    raw_counts = defaultdict(int)
    raw_admin1_names = defaultdict(set)
    raw_admin2_names = defaultdict(set)
    with RAW.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            d = month(row["reference_period_start"])
            if d.strftime("%Y-%m") == APRIL_ZWL and (row.get("currency_code") or "") == "ZWL":
                continue
            district_key = canon(row.get("admin2_name"))
            raw_counts[district_key] += 1
            if row.get("admin1_name"):
                raw_admin1_names[district_key].add(row["admin1_name"].strip())
            if row.get("admin2_name"):
                raw_admin2_names[district_key].add(row["admin2_name"].strip())
    pair_counts = defaultdict(int)
    for row in candidates:
        pair_counts[row["district_key"]] += 1
    final_counts = defaultdict(int)
    with FINAL.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            final_counts[row.get("district_key", "")] += 1
    spatial_rows = []
    all_names = set(boundary_counts) | set(raw_counts) | set(pair_counts) | set(final_counts)
    for name in sorted(all_names):
        if not name:
            status = "BLANK_ADMIN2_IN_SOURCE"
        elif boundary_counts[name] == 1:
            status = "EXACT_CANONICAL_NAME_MATCH"
        elif boundary_counts[name] > 1:
            status = "AMBIGUOUS_DUPLICATE_BOUNDARY_NAME"
        else:
            status = "NO_EXACT_BOUNDARY_NAME_MATCH"
        spatial_rows.append({
            "district_key": name, "boundary_name_match_count": boundary_counts[name],
            "raw_quotes_after_april_exclusion": raw_counts[name],
            "exact_t_plus_1_pairs": pair_counts[name], "final_model_rows": final_counts[name],
            "match_status": status,
            "price_mapping_method": "HDX admin2_name text canonicalization; no market point-in-polygon in Option B",
            "rainfall_mapping_method": "CHIRPS grid-cell centres within ADM2 polygons; nearest representative-point cell fallback for unrepresented districts",
            "grid_cells_in_subset": "", "grid_cells_matched_to_any_district": "",
            "rainfall_districts_receiving_cells": "", "rainfall_fallback_districts": "",
            "rainfall_output_districts": "", "rainfall_output_rows": "",
            "source_admin1_names": json.dumps(sorted(raw_admin1_names[name])),
            "source_admin2_name_variants": json.dumps(sorted(raw_admin2_names[name])),
            "source_admin1_ambiguous": int(len(raw_admin1_names[name]) > 1),
            "cell_overlap_ambiguity_audit": "NOT RECORDED per grid cell in saved processing outputs",
        })
    rain_log_path = ROOT / "outputs/_step03_log.txt"
    rain_log = rain_log_path.read_text(encoding="utf-8-sig", errors="replace")
    grid_match = re.search(r"grid cells:\s*(\d+);\s*matched to a district:\s*(\d+)", rain_log)
    rain_districts_match = re.search(r"districts receiving cells:\s*(\d+)", rain_log)
    fallback_match = re.search(r"districts with no cell \(nearest-cell fallback\):\s*\[([^\]]*)\]", rain_log)
    output_match = re.search(r"rows:\s*([\d,]+)\s+districts:\s*(\d+)\s+months:\s*(\d+)", rain_log)
    grid_total = grid_match.group(1) if grid_match else "UNKNOWN"
    grid_matched = grid_match.group(2) if grid_match else "UNKNOWN"
    rain_receiving = rain_districts_match.group(1) if rain_districts_match else "UNKNOWN"
    fallback_names = fallback_match.group(1).strip() if fallback_match else "UNKNOWN"
    rain_output_rows = output_match.group(1).replace(",", "") if output_match else "UNKNOWN"
    rain_output_districts = output_match.group(2) if output_match else "UNKNOWN"
    spatial_rows.append({
        "district_key": "__CHIRPS_GRID_JOIN_RUN_SUMMARY__", "boundary_name_match_count": "",
        "raw_quotes_after_april_exclusion": "", "exact_t_plus_1_pairs": "", "final_model_rows": "",
        "match_status": "RUN_LOG_SUMMARY",
        "price_mapping_method": "Market names are not spatially joined in Option B.",
        "rainfall_mapping_method": "See outputs/_step03_log.txt; fallback areas are reported in rainfall_fallback_districts.",
        "grid_cells_in_subset": grid_total, "grid_cells_matched_to_any_district": grid_matched,
        "rainfall_districts_receiving_cells": rain_receiving, "rainfall_fallback_districts": fallback_names,
        "rainfall_output_districts": rain_output_districts, "rainfall_output_rows": rain_output_rows,
        "source_admin1_names": "", "source_admin2_name_variants": "",
        "source_admin1_ambiguous": "", "cell_overlap_ambiguity_audit": "UNKNOWN; only aggregate grid match counts are logged",
    })
    with (OUT / "spatial_join_audit.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(spatial_rows[0]))
        w.writeheader()
        w.writerows(spatial_rows)

    final_by_rule = sum(r["stage_final_model_row_by_source_rule"] for r in candidates)
    excluded_gap = len(candidates) - final_by_rule
    exact_positive = sum(r["y_true"] for r in candidates)
    final_table_positive = 0
    with FINAL.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            final_table_positive += int(float(row["target_next_month"]))
    summary = [
        ("raw_market_quotes", raw_quotes, "source CSV rows"),
        ("quotes_after_april_2024_zwl_exclusion", raw_quotes - april_removed, f"excluded {april_removed} raw quotes"),
        ("aggregated_market_to_district_cells", len(agg), "pipeline group keys; median price"),
        ("valid_spi_cells", len(valid), "same commodity/month/currency peer group >=8 districts"),
        ("exact_t_plus_1_pairs", len(candidates), "next valid observation exactly one calendar month later"),
        ("excluded_after_exact_pairs", excluded_gap, "source continuity rule >2.0 months since previous candidate pair"),
        ("final_model_rows_by_source_rule", final_by_rule, "exact pairs retained by source continuity rule"),
        ("existing_final_table_rows", final_rows, "outputs/option_b/data/option_b_modelling_table.csv"),
        ("exact_pair_positive_labels", exact_positive, "SPI(T+1)>1.25, denominator exact pairs"),
        ("existing_final_table_positive_labels", final_table_positive, "target_next_month sum, denominator existing final table"),
    ]
    with (OUT / "attrition_summary.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["stage_or_check", "count", "definition"])
        w.writerows(summary)

    with (OUT / "target_threshold_sensitivity.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["population_stage", "spi_threshold", "positive_count", "denominator", "prevalence", "interpretation"])
        for stage_name, rs in (("exact_t_plus_1_pairs", candidates),
                               ("final_model_rows", [r for r in candidates if r["stage_final_model_row_by_source_rule"]])):
            for threshold in (1.20, 1.25, 1.30):
                positives = sum(float(r["spi_at_t_plus_1"]) > threshold for r in rs)
                w.writerow([stage_name, f"{threshold:.2f}", positives, len(rs), f"{positives / len(rs):.8f}",
                            "label prevalence only; no model retrained under this threshold"])

    source_rule_keys = {(r["district_key"], r["commodity_name"], r["prediction_month"], r["currency_code"])
                        for r in candidates if r["stage_final_model_row_by_source_rule"]}
    print(json.dumps({
        "raw_quotes": raw_quotes, "april_2024_zwl_removed": april_removed,
        "raw_reference_period_start_min": raw_min_date.isoformat() if raw_min_date else None,
        "raw_reference_period_start_max": raw_max_date.isoformat() if raw_max_date else None,
        "blank_admin2_quotes_after_exclusion": raw_district_blanks,
        "aggregated_cells": len(agg), "valid_spi_cells": len(valid),
        "exact_t_plus_1_pairs": len(candidates), "exact_pair_positives": exact_positive,
        "final_by_source_rule": final_by_rule, "excluded_gap_gt_2": excluded_gap,
        "existing_final_rows": final_rows, "existing_final_positives": final_table_positive,
        "retained_keys_match_existing_table": source_rule_keys == final_keys,
        "retained_missing_from_existing_table": len(source_rule_keys - final_keys),
        "existing_table_extra_keys": len(final_keys - source_rule_keys),
        "raw_units": sorted(raw_unit_values), "raw_price_flags": sorted(raw_flag_values),
        "raw_price_types": sorted(raw_type_values), "raw_currencies": sorted(raw_currency_values),
        "mixed_unit_groups": sum(len(v) > 1 for v in group_units.values()),
        "mixed_flag_groups": sum(len(v) > 1 for v in group_flags.values()),
        "mixed_price_type_groups": sum(len(v) > 1 for v in group_types.values()),
        "price_peer_groups_mixed_units": sum(r["unit_comparable"] != "PASS" for r in price_audit_rows),
        "price_peer_groups_mixed_flags": sum(r["price_flag_homogeneous"] != "PASS" for r in price_audit_rows),
        "price_peer_groups_mixed_types": sum(r["price_type_homogeneous"] != "PASS" for r in price_audit_rows),
        "raw_blank_admin2_quotes_after_april_exclusion": raw_counts[""],
        "source_market_names_without_exact_boundary_match": sorted(n for n in raw_counts if n and not boundary_counts[n]),
        "outputs": [str(ledger_path), str(OUT / "attrition_summary.csv"), str(OUT / "target_threshold_sensitivity.csv"),
                    str(OUT / "price_comparability_audit.csv"), str(OUT / "spatial_join_audit.csv")],
    }, indent=2))


if __name__ == "__main__":
    main()
