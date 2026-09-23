# Scrapingdog Google Maps API — Free-Plan Smoke Test Findings

**Date:** 2026-09-23 · **Script:** `scripts/scrapingdog_smoke.py` + inline depth probes · **Raw evidence:** `data/scrapingdog/raw/smoke/` (API key scrubbed from saved responses — their response embeds it in reviews/photos/posts links) · **Spend:** 70 of the account's 100 free credits (14 successful requests × 5 credits; pricing page advertises 200 free credits, account API reported `requestLimit: 100` — 🔴 discrepancy, not resolved).

## Verdict: PASS — deserves a scale test, with one production-critical caveat

## What was verified

1. **Endpoint works as documented.** `GET api.scrapingdog.com/google_maps?api_key&query[&start]` → HTTP 200, 20 results/request. Latency 1.38–2.40s (median ~1.5s) — sync API, Google-like speed.
2. **Field fills excellent on the core set** (80 uniques across 4 benchmark queries): title 100%, address 95%, phone 96%, website 96%, rating 99%, review count 99%, hours 95%, coordinates 100%, place_id 100%. **No email or social fields (confirmed absent)** — competes only on the business-data intent.
3. **"Failed requests never charged" claim: TRUE, verified empirically.** 4 × HTTP 400 responses consumed zero credits (account API before/after: 25 → 25 across the failures, 5 credits per success only).
4. **Pagination mechanics:** `page` param requires an `ll` coordinates argument (400 without it); `start` offset (0/20/40…) works standalone.
5. **Account/credits endpoint exists:** `GET /account?api_key=` (free) — usable for live cost measurement in a scale test.

## 🔴 Production-critical caveat: paid duplicate pages past the depth ceiling

Deep pagination on "restaurants in Manhattan, New York" (`start=40…200`, 9 requests, 180 raw rows) returned **HTTP 200 with a full 20 results every time — but only 35 new unique places**; most pages were 100% repeats of earlier pages. Combined with pages 0–1, the query's effective ceiling is ~75 uniques (Google's familiar wall), and **beyond it the API keeps serving full-looking, fully-billed duplicate pages with no signal that depth is exhausted**. Same finding class as Apify's silent truncation, but inverted: Apify silently under-delivers, Scrapingdog silently over-bills. A scale run must cap `start` ≤ 40–60 per query and dedupe by place_id, or per-unique cost inflates unnoticed.

## Cost outlook for the scale test (rate-card, to verify live)

Lite $40/mo = 200,000 credits = 40,000 requests. At the measured ~75 uniques per 11-request query: ≈ 0.73 credits/unique → **≈ $0.15 per 1,000 unique businesses** — an order of magnitude below every provider measured so far (Apify $0.54, Google $2.30, Outscraper $3.69, Lobstr $5.82) — for listings **without** email/social enrichment. With `start` capped at 40 (3 requests/query, ~65–75 uniques): ≈ 0.2 credits/unique → ≈ $0.04/1K. These are rate-card projections; the scale test should measure billed credits via the `/account` endpoint.

## Recommended scale-test design (pending credits purchase)

Same 2 runs × 10 sub-areas as the benchmark, 3 requests/query (`start` 0/20/40 — inside the measured ceiling), ~60 requests/run = 300 credits/run — trivially cheap even on Lite. Compare volume/fill/cost against the four tested providers; expect it to slot into the "bulk business data, no contacts" intent alongside Google, competing on price and no volume cap per month.
