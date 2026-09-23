# Google Places API (New) — Benchmark Run: Cost, Speed, Volume, Field Coverage

**Run date:** 2026-09-23 · **Script:** `scripts/google_places_run.py` · **Analysis:** `scripts/google_places_analyze.py` · **Raw evidence:** `research/raw/google-places-api/` (60 response files + `run-log.json`, unmodified)
**Workload:** identical to the scraper benchmark (`scripts/lib/config.py`) — Run 1 "marketing agencies in <sub-area>" and Run 2 "restaurants in <sub-area>" across the same 10 NYC/LA sub-areas.
**Endpoint:** Text Search (New) `places:searchText`, pageSize 20, paginated to Google's documented 60-results-per-query maximum. Field mask spans all four SKU tiers, so every request billed as **Text Search Enterprise + Atmosphere** (SKU 120C-BEC3-B48F).

## Results

| Metric | Value |
|---|---|
| Requests (benchmark) | 60 (+2 smoke) — 0 errors, 60/60 HTTP 200 |
| Raw places returned | 1,120 |
| Unique places (by place id) | **1,044** (Run 1: 444 · Run 2: 600) — 6.8% cross-sub-area duplicate rate |
| Wall-clock, both runs | **97.0 s** |
| Latency median / p95 / max | **1.54 s / 2.26 s / 2.67 s** per request |
| Avg places per billed request | 18.7 |

**The 60-per-query wall, measured:** all 10 restaurant queries returned exactly 60 (ceiling hit — real supply is far larger); marketing-agency queries returned 35–60 (Queens 42, Van Nuys 35 = genuine local scarcity; the same areas under-delivered for the scrapers too). The same 10 Run-1 queries produced **444 unique places from Google vs 998 (Lobstr), 1,405 (Apify), 512 (Outscraper, 80/query budget cap)**. Volume scales only by adding more, finer-grained queries: matching a scraper's ~1,400 uniques would need roughly 3–4× more distinct sub-area queries (~30–40 queries → ~90–120 billed requests), with rising overlap.

## Cost — shown calculation

Pricing fetched live 2026-09-23 from developers.google.com/maps/billing-and-pricing/pricing:
Text Search Enterprise + Atmosphere = **$40 / 1,000 requests** (tier 1,001–100,000), **first 1,000 requests/month free**. (Pro tier without phone/website/reviews: $32/1K, 5,000 free/mo — insufficient fields for lead use.)

- **This benchmark, actually billed: $0.00** — 62 total requests, inside the 1,000-free-events allowance. (To cross-check on your side: Cloud Console → Billing report, SKU 120C-BEC3-B48F.)
- **Rate-card cost had free tier been exhausted:** 60 req × $0.040 = **$2.40** → 1,044 unique places → **$2.30 per 1,000 unique businesses** (fields at scraper parity minus email/socials).
- **Comparators (Run 1, same queries):** Apify measured $0.0016/verified-email lead + $0.005/run (451 of 1,405 uniques billed); Outscraper $3.00/1K base records ($2.40 for 800 requested → 512 unique ≈ **$4.69/1K unique**, listings only); Lobstr 1 credit/row + 2/email extracted (credit→$ conversion at plan rate — pending, tracked in testing plan §9.4).
- **Free-tier reality:** 1,000 Enterprise+Atmosphere requests/mo ≈ ~18,700 raw places/month at zero cost — a genuinely large free allowance, but per-month, per-project, and email-less.

## Field coverage — measured on all 1,044 unique places

| Field | Coverage | Field | Coverage |
|---|---:|---|---:|
| id / name / address / coordinates / types / Google Maps URL / businessStatus | 100% | rating + review count | 97.7% |
| addressComponents (structured) | 100% | regularOpeningHours | 97.9% |
| nationalPhoneNumber | 95.4% | reviews (**max 5 per place**, avg 4.7) | 97.7% |
| websiteUri | 94.3% | photos (refs; media fetch billed separately) | 94.7% |
| primaryType | 99.4% | priceLevel | 50.4% |
| | | editorialSummary | 37.5% |

**Fields the official API cannot return at any price** (confirmed absent from the API surface, not just empty): **email addresses, social profiles (Facebook/Instagram/LinkedIn/etc.), contact-form URLs, owner name/link, full review corpus (hard 5-review cap), popular-times data, review-score histograms.** For comparison on the same Run-1 workload: Lobstr returned emails for 59% and 2–3 social links for ~50% of its 998 uniques; Apify verified emails for 32% of 1,405; Outscraper offers email extraction as a separately billed service (not run, budget).

## Where the official API wins / loses (evidence-based)

**Wins:** fastest per-request latency measured in the project (median 1.54s, 97s for the full dual-run); highest phone/website/rating/hours fill-rates of the four tested (94–98%); first-party freshness; 1,000 free enterprise-tier calls/mo; zero ToS ambiguity; clean structured schema.
**Loses:** no email/social/contact-enrichment fields at any price — the decisive gap for outreach lead lists; 60-results-per-query hard cap makes bulk extraction a query-engineering exercise (3–4× more queries for scraper-scale volume); 5-review cap; photos/media billed separately; costs scale per-request, so the effective $/1K businesses rises with the extra queries volume requires.
