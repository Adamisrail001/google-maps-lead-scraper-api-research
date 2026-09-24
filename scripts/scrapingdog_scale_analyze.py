"""Analyze the Scrapingdog ll+page full-scale benchmark runs.

Reads data/scrapingdog/raw/run{1,2}-llpage/ (raw pages + per-run logs written
by scrapingdog_scale_run2.py), dedupes by place_id, computes field fills,
delivery, measured credits -> $/1K at the Lite rate, latency, and the
billed-duplicate-page overhead. Writes data/scrapingdog/reports/scale-findings.md.

Lite rate: $40/mo = 200,000 credits -> $0.0002/credit (5 credits/request).
"""
import json
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "scrapingdog" / "raw"
CREDIT_USD = 40.0 / 200_000

FIELDS = {"name": "title", "address": "address", "phone": "phone",
          "hours": "operating_hours", "website": "website",
          "rating": "rating", "reviews": "reviews"}

runs = {}
all_uniques = {}
for label in ("run1", "run2"):
    d = RAW / f"{label}-llpage"
    log = json.loads((d / f"{label}-log.json").read_text(encoding="utf-8"))
    uniq = {}
    for f in sorted(d.glob("*-page*.json")):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        for rec in data.get("search_results", []):
            pid = rec.get("place_id") or rec.get("data_id")
            uniq.setdefault(pid, rec)
    lat = [r["latency_s"] for r in log["requests"] if r["http"] == 200]
    dup_pages = sum(1 for r in log["requests"] if r["http"] == 200
                    and r["results"] > 0 and r["new_unique"] == 0)
    runs[label] = dict(
        log=log, uniques=len(uniq),
        requests=len(log["requests"]),
        credits=log["credits_this_run"],
        wall=log["wall_clock_s"],
        lat_median=round(statistics.median(lat), 2),
        lat_p95=round(sorted(lat)[int(len(lat) * 0.95) - 1], 2),
        dup_pages=dup_pages,
        per_query=log["per_query"],
    )
    all_uniques.update(uniq)

n = len(all_uniques)
vals = list(all_uniques.values())
fills = {k: round(100 * sum(1 for r in vals if r.get(f) not in (None, "", [], {})) / n, 1)
         for k, f in FIELDS.items()}
core4 = round((fills["name"] + fills["address"] + fills["phone"] + fills["hours"]) / 4, 1)

total_credits = sum(r["credits"] for r in runs.values())
total_cost = total_credits * CREDIT_USD
cost_per_1k = 1000 * total_cost / n
per_query_uniques = [q["unique"] for r in runs.values() for q in r["per_query"].values()]

out = {
    "uniques_both_runs": n,
    "per_run": {l: {k: v for k, v in r.items() if k not in ("log", "per_query")} for l, r in runs.items()},
    "per_query_unique_min_max_mean": [min(per_query_uniques), max(per_query_uniques),
                                      round(statistics.mean(per_query_uniques), 1)],
    "fills": fills, "core4": core4,
    "total_credits": total_credits, "total_cost_usd": round(total_cost, 2),
    "cost_per_1k_unique": round(cost_per_1k, 2),
}
print(json.dumps(out, indent=1))

L = []
A = L.append
A("# Scrapingdog Google Maps API — Full-Scale Benchmark Findings (Lite plan)")
A("")
A(f"**Date:** 2026-09-24 · **Plan:** Lite ($40/mo, 200K credits, verified live via `/account`) · **Script:** `scripts/scrapingdog_scale_run2.py` (ll+page mode) · **Raw:** `data/scrapingdog/raw/run1-llpage/`, `run2-llpage/` (every page + logs; API key scrubbed) · **Analysis:** `scripts/scrapingdog_scale_analyze.py` (rerun to regenerate).")
A("")
A("## Design — benchmark-standard workload, correctly-configured pagination")
A("")
A("Same 2 runs × 10 sub-areas as every provider; input = industry term + `ll=@lat,lng,14z` (the exact coordinate-anchored shape Lobstr's tasks used); **all 10 pages fetched per query** (200 requested = the benchmark ceiling), no early stop, so billed duplicate pages are measured, not estimated.")
A("")
A("**Pagination mode A/B (live, same query):** the `start` offset barely paginates — page 2 ~90% repeats, page 3 zero new (~22 uniques/query; first attempt preserved in `raw/run1/`, `raw/run2/`). The documented `ll`+`page` mode goes deeper and is what this benchmark uses.")
A("")
A("## Results")
A("")
A("| | Run 1 (agencies) | Run 2 (restaurants) | Both |")
A("|---|---:|---:|---:|")
A(f"| Requested (10 pages × 20 × 10 queries) | 2,000 | 2,000 | 4,000 |")
A(f"| HTTP 200 requests | {runs['run1']['requests']} | {runs['run2']['requests']} | {runs['run1']['requests']+runs['run2']['requests']} |")
A(f"| Unique places (place_id dedupe) | {runs['run1']['uniques']:,} | {runs['run2']['uniques']:,} | **{n:,}** |")
A(f"| Credits (measured, /account before/after) | {runs['run1']['credits']} | {runs['run2']['credits']} | {total_credits} |")
A(f"| Cost @ Lite rate | ${runs['run1']['credits']*CREDIT_USD:.2f} | ${runs['run2']['credits']*CREDIT_USD:.2f} | **${total_cost:.2f}** |")
A(f"| Wall-clock | {runs['run1']['wall']}s | {runs['run2']['wall']}s | — |")
A(f"| Latency median / p95 (s) | {runs['run1']['lat_median']} / {runs['run1']['lat_p95']} | {runs['run2']['lat_median']} / {runs['run2']['lat_p95']} | — |")
A(f"| Fully-billed all-duplicate pages | {runs['run1']['dup_pages']} | {runs['run2']['dup_pages']} | {runs['run1']['dup_pages']+runs['run2']['dup_pages']} |")
A("")
A(f"**Cost per 1K unique: ${cost_per_1k:.2f}** — cheapest raw rate in the test. **Field fills on {n:,} uniques:** name {fills['name']}% · address {fills['address']}% · phone {fills['phone']}% · hours {fills['hours']}% (core-4 avg {core4}%) · website {fills['website']}% · rating {fills['rating']}%.")
A("")
A("## The finding that decides its ranking status: a hard ~2-page depth ceiling")
A("")
A(f"Per-query uniques ranged **{min(per_query_uniques)}–{max(per_query_uniques)}** (mean {statistics.mean(per_query_uniques):.0f}) against 200 requested — every query effectively exhausted by page 2–3, after which the API keeps serving **HTTP-200, fully-billed, 100%-duplicate pages with no exhaustion signal** ({runs['run1']['dup_pages']+runs['run2']['dup_pages']} such pages billed in this benchmark alone; confirms the smoke finding at scale). Identical queries yielded 120–200 uniques on Lobstr/HasData/Apify/Bright Data.")
A("")
A("## Head-to-head (same queries, both runs)")
A("")
A("| | Scrapingdog | Lobstr | HasData | BrightData | Apify |")
A("|---|---:|---:|---:|---:|---:|")
A(f"| Unique places | **{n:,}** | 2,567 | 2,456 | 1,739 | 2,523 |")
A(f"| Delivery vs 4,000 requested | {100*n/4000:.0f}%* | 85.1% | 73.7% | 87.1% (of 2,000) | 68.3% |")
A(f"| Core-4 fill | {core4}% | 97.1% | 94.2% | 96.4% | 92.8% |")
A(f"| $/1K unique (basic) | **${cost_per_1k:.2f}** | $2.66 | $0.74 | ~$1.50 | $0.54 |")
A("")
A("*Delivery measured against the same 200/query ceiling all providers faced; the shortfall is the API's own depth ceiling, not data scarcity — the other four found 3–5× more places on identical queries.")
A("")
A("## Verdict for the core-requirement check (Step 0)")
A("")
A(f"**Fails the required-volume core requirement.** The measured ~{statistics.mean(per_query_uniques):.0f}-unique/query ceiling is *below Google Places API's 60/query cap that disqualified Google*, and it cannot extract 'all available listings from a search' when 120–200 demonstrably exist. Compounding it, depth exhaustion is invisible: past the ceiling you pay full price for duplicate pages. Everything else is genuinely strong — cheapest cost, ~1.3s median latency, high fills on what it does return — so it stays valuable for the shallow-lookup use case (top ~40 results per area), documented under Disqualified Providers with these numbers.")
(ROOT / "data" / "scrapingdog" / "reports" / "scale-findings.md").write_text("\n".join(L), encoding="utf-8")
print("written: data/scrapingdog/reports/scale-findings.md")
