"""Analyze the Google Places API (New) benchmark run.

Reads research/raw/google-places-api/*.json, computes unique counts (by place
id), per-field coverage, latency stats, and the cost calculation. Prints a
JSON summary consumed by research/analysis/google-places-api-cost-speed.md.
"""
import json
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "research" / "raw" / "google-places-api"

FIELDS = [
    "id", "displayName", "formattedAddress", "addressComponents", "location",
    "types", "primaryType", "googleMapsUri", "businessStatus", "photos",
    "nationalPhoneNumber", "internationalPhoneNumber", "websiteUri", "rating",
    "userRatingCount", "regularOpeningHours", "priceLevel", "reviews",
    "editorialSummary",
]

runs = {"run1": {}, "run2": {}}  # run -> id -> place
per_query_raw = {}
for f in sorted(RAW.glob("run*-page*.json")):
    run = f.name.split("-")[0]
    qkey = f.name.rsplit("-page", 1)[0]
    data = json.loads(f.read_text(encoding="utf-8"))
    for p in data.get("places", []):
        runs[run][p["id"]] = p
        per_query_raw.setdefault(qkey, set()).add(p["id"])

log = json.loads((RAW / "run-log.json").read_text(encoding="utf-8"))
lat = [r["latency_s"] for r in log["requests"]]
raw_total = sum(r["places_returned"] for r in log["requests"])

all_places = {**runs["run1"], **runs["run2"]}
coverage = {}
for fld in FIELDS:
    have = sum(1 for p in all_places.values() if p.get(fld) not in (None, "", [], {}))
    coverage[fld] = round(100 * have / len(all_places), 1)

# reviews depth: Places API returns max 5 reviews per place
rev_counts = [len(p.get("reviews", [])) for p in all_places.values() if p.get("reviews")]

summary = {
    "requests_benchmark": len(log["requests"]),
    "raw_places": raw_total,
    "run1_unique": len(runs["run1"]),
    "run2_unique": len(runs["run2"]),
    "total_unique": len(all_places),
    "dup_rate_pct": round(100 * (1 - len(all_places) / raw_total), 1),
    "per_query_unique": {k: len(v) for k, v in sorted(per_query_raw.items())},
    "wall_clock_s": log["totals"]["wall_clock_s"],
    "latency_median_s": round(statistics.median(lat), 2),
    "latency_p95_s": round(sorted(lat)[int(len(lat) * 0.95) - 1], 2),
    "latency_max_s": round(max(lat), 2),
    "places_per_request_avg": round(raw_total / len(log["requests"]), 1),
    "field_coverage_pct": coverage,
    "reviews_max_per_place": max(rev_counts) if rev_counts else 0,
    "reviews_avg_per_place_with_reviews": round(statistics.mean(rev_counts), 1) if rev_counts else 0,
}
print(json.dumps(summary, indent=2))
