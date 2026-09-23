# Bright Data "Google Maps full information" — Smoke Test Findings

**Date:** 2026-09-23 · **Scraper:** Web Scraper API dataset `gd_m8ebnr0q2qlklc02fz` (the only triggerable Maps scraper on the account; "Google Maps businesses" entries are pre-collected marketplace datasets) · **Raw evidence:** `data/brightdata/raw/smoke/smoke1-snapshot.json` · **Job:** discovery by location, `{country: US, keyword: "marketing agencies in Manhattan, New York"}`, `limit_per_input=10` → snapshot `sd_mue0hlp9x3r40f9xx`.

## Result: API works well — but ZERO contact fields → recommend E5 elimination, no scale test

### What passed
- **Reliability:** 10/10 records, 0 errors; trigger → ready in 130s (discovery jobs carry fixed overhead; not comparable per-record at n=10).
- **Field fills (n=10):** name, address, phone, website (`open_website`), category, rating, reviews_count, hours, coordinates, place_id, main_image, top_reviews — **all 10/10**. Rich extras: review_distribution, reviews_snippets, business_details, people_also_search, is_claimed. popular_times present in schema but empty (0/10).
- **Mechanics:** clean async model (trigger → progress → snapshot), precise validation errors, Bearer auth.
- **Network workaround proven again:** brightdata.com zone is blocked by local DNS; DoH-resolved pinned IP works reliably.

### The decisive finding
**No email addresses and no social profiles anywhere in the output** — no email/social fields in the 39-field schema, zero `@`-pattern strings in the full payload, zero facebook/instagram/linkedin/twitter occurrences. This resolves the question left open by the unreachable docs ("not indicated"): **confirmed absent.**

Per the lead's filter (article intent = lead generation) and the precedent set for Scrapingdog the same day: a contact-less provider repeats Google's "not eligible" verdict, and a scale test cannot change that — **the scale-test budget is better spent on HasData.**

### Retained value for the article
- One line in the bulk-business-data use-case section: excellent core-field completeness (10/10 across the board on this sample), rate-card ~$0.75–1.50/1K records (still unconfirmed by a billed run — measured cost not captured at n=10; no cost field in the progress/snapshot response).
- Discovery inputs are `country`+`keyword` (or place_id/cid) — **no text-query-with-location mode**, an input-comparability caveat had it been benchmarked.

### If a scale test is ever wanted anyway (bulk-data angle only)
Trigger shape is proven; 20 inputs (2 runs × 10 sub-areas as keywords) with `limit_per_input=200` would mirror the benchmark; measure billed cost via the dashboard (no billing figure surfaced through this API flow).
