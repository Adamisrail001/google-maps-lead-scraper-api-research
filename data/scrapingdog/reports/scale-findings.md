# Scrapingdog Google Maps API — Full-Scale Benchmark Findings (Lite plan)

**Date:** 2026-09-24 · **Plan:** Lite ($40/mo, 200K credits, verified live via `/account`) · **Script:** `scripts/scrapingdog_scale_run2.py` (ll+page mode) · **Raw:** `data/scrapingdog/raw/run1-llpage/`, `run2-llpage/` (every page + logs; API key scrubbed) · **Analysis:** `scripts/scrapingdog_scale_analyze.py` (rerun to regenerate).

## Design — benchmark-standard workload, correctly-configured pagination

Same 2 runs × 10 sub-areas as every provider; input = industry term + `ll=@lat,lng,14z` (the exact coordinate-anchored shape Lobstr's tasks used); **all 10 pages fetched per query** (200 requested = the benchmark ceiling), no early stop, so billed duplicate pages are measured, not estimated.

**Pagination mode A/B (live, same query):** the `start` offset barely paginates — page 2 ~90% repeats, page 3 zero new (~22 uniques/query; first attempt preserved in `raw/run1/`, `raw/run2/`). The documented `ll`+`page` mode goes deeper and is what this benchmark uses.

## Results

| | Run 1 (agencies) | Run 2 (restaurants) | Both |
|---|---:|---:|---:|
| Requested (10 pages × 20 × 10 queries) | 2,000 | 2,000 | 4,000 |
| HTTP 200 requests | 100 | 100 | 200 |
| Unique places (place_id dedupe) | 382 | 480 | **862** |
| Credits (measured, /account before/after) | 500 | 500 | 1000 |
| Cost @ Lite rate | $0.10 | $0.10 | **$0.20** |
| Wall-clock | 115.1s | 118.7s | — |
| Latency median / p95 (s) | 0.91 / 2.01 | 1.08 / 1.94 | — |
| Fully-billed all-duplicate pages | 23 | 21 | 44 |

**Cost per 1K unique: $0.23** — cheapest raw rate in the test. **Field fills on 862 uniques:** name 100.0% · address 98.0% · phone 95.4% · hours 96.3% (core-4 avg 97.4%) · website 92.5% · rating 96.2%.

## The finding that decides its ranking status: a hard ~2-page depth ceiling

Per-query uniques ranged **39–57** (mean 49) against 200 requested — every query effectively exhausted by page 2–3, after which the API keeps serving **HTTP-200, fully-billed, 100%-duplicate pages with no exhaustion signal** (44 such pages billed in this benchmark alone; confirms the smoke finding at scale). Identical queries yielded 120–200 uniques on Lobstr/HasData/Apify/Bright Data.

## Head-to-head (same queries, both runs)

| | Scrapingdog | Lobstr | HasData | BrightData | Apify |
|---|---:|---:|---:|---:|---:|
| Unique places | **862** | 2,567 | 2,456 | 1,739 | 2,523 |
| Delivery vs 4,000 requested | 22%* | 85.1% | 73.7% | 87.1% (of 2,000) | 68.3% |
| Core-4 fill | 97.4% | 97.1% | 94.2% | 96.4% | 92.8% |
| $/1K unique (basic) | **$0.23** | $2.66 | $0.74 | ~$1.50 | $0.54 |

*Delivery measured against the same 200/query ceiling all providers faced; the shortfall is the API's own depth ceiling, not data scarcity — the other four found 3–5× more places on identical queries.

## Verdict for the core-requirement check (Step 0)

**Fails the required-volume core requirement.** The measured ~49-unique/query ceiling is *below Google Places API's 60/query cap that disqualified Google*, and it cannot extract 'all available listings from a search' when 120–200 demonstrably exist. Compounding it, depth exhaustion is invisible: past the ceiling you pay full price for duplicate pages. Everything else is genuinely strong — cheapest cost, ~1.3s median latency, high fills on what it does return — so it stays valuable for the shallow-lookup use case (top ~40 results per area), documented under Disqualified Providers with these numbers.