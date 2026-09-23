# Google Maps Scraper APIs — Final Benchmark Report (by user persona)

**Test window:** 2026-09-22/23 · **Method:** identical workload for every tool — 2 runs (marketing agencies, restaurants) × 10 NYC/LA sub-areas; two-stage testing (free-plan smoke ~100 results → scale run) · **Personas & evidence:** `user-intent.md` · **Raw evidence:** `data/<tool>/`, `research/raw/google-places-api/` · **Disclosure:** Lobstr.io owns this research and is an evaluated provider.

## Verdicts by persona

**Persona 1 — Local-data extractor** (complete NAP+hours+rating sets, price-sensitive):
Use **Bright Data** or **Outscraper**. Bright Data delivered the cleanest at-scale core data of the new candidates (1,738 uniques, 0.2% errors, phone 93–98%, ~6 min/1K, est. ~$1.50/1K — rate-card, unverified billing) with onboarding friction (geo-blocks, no text-query input). Outscraper is the proven all-rounder ($3.69/1K measured, richest default listing schema, 96.8% delivery). **HasData base-mode** (~$0.74/1K at 3 credits/row) and **ScrapingDog** (projected $0.04–0.15/1K, 95–100% fills — smoke-verified only, scale run pending a paid plan; beware its billed-duplicate-pages behavior past ~75 uniques/query) are the budget picks. **The official Google API is NOT the answer here despite ~$1.75–2.30/1K pricing:** 60-results/query ceiling (measured at the cap on 10/10 restaurant queries) and Maps Platform Terms §3.2.3 prohibiting "copying and saving business names, addresses" — a stored, exportable list is contractually barred.

**Persona 2 — Lead-gen / outreach** (emails first, then socials; $/qualified lead):
Use **Lobstr** for the most contactable, richest records — highest email fill measured (59% agencies / 37% restaurants), only provider with social profiles (~50%), plus images/owner data — at the highest price ($5.82/1K unique, $6.20/1K emails). Use **HasData** as the value alternative: 42% blended email fill (46%/37%) at **$1.75/1K unique / $4.19/1K emails — ~3.3× cheaper** — and the fastest scraper tested (~4–5 min/run), but no socials/images and field-fill wobble in email mode (rating/reviews 73% on run 1). Use **Apify** only if verified-emails-only billing fits ($0.54/1K, DNS/MX-verified 28%) and you can tolerate its silent profit-guard truncations (4/20 queries measured). Not eligible: Google, ScrapingDog, Bright Data (no contact fields — measured, not assumed). Note for all: emails come from crawling business websites, not from Maps listings.

**Persona 3 — Developer building a product** (stability, pagination, quotas, predictable pricing at 10k–100k/mo):
Displaying live data in-app → **Google Places API (New)**: best-engineered API tested (60/60 + 3/3 requests clean, 1.54s median, typed schema, per-method quotas, 1,000 free Enterprise calls/mo) and the only fully ToS-compliant option for its intended use. Storing data in your own DB → Google is barred by its own terms; **HasData** (async jobs, webhooks, clean docs, 18s–5min jobs, 5-concurrency on $49 plan) and **Apify** (mature platform/SDKs) lead, with **Outscraper** (official Python client, 3-stage async) close. Watch-outs measured: HasData's status field never reaches `finished` (poll results endpoint); Apify's `SUCCEEDED` can mask truncation; Bright Data's snapshot can report `ready` before it's downloadable.

## Master comparison (measured unless marked)

| Tool | Unique (both runs) | Email fill | Core NAP fills | $/1K unique | Wall-clock/run | Errors/trust findings |
|---|---:|---:|---|---:|---:|---|
| Lobstr | 2,567 | 59%/37% + socials | phone 91–98, web 86–93 | $5.82 | ~29 min | none; verification dashboard-only |
| Apify | 2,523 | 28% verified | phone 90–96, web 83–89 | $0.54 | ~22–37 min cum. | 🔴 silent truncation 4/20; business_status broken |
| HasData | 2,456 | 42% | web 100, phone 89–97 | $1.75 | **~4–5 min** | status never `finished`; email-mode field wobble |
| Outscraper | 1,300 (80/q cap) | not run (+$6/1K stages) | phone 91–97, web 93–94 | $3.69 | not aggregated | none |
| Bright Data | 1,738 (2×1K design) | **0 — no fields** | phone 93–98, web 89–92 | ~$1.50 (rate-card est.) | ~6 min | 3 errors/1,741; `ready`≠downloadable |
| ScrapingDog (stage 1 only) | 80 (smoke) | **0 — no fields** | phone 96, web 96 | $0.04–0.15 (projected) | 1.5s/request | 🔴 billed duplicate pages past depth |
| Google Places (New) | 1,044 (60/query cap) | **0 — no fields** | phone 95, web 94 | $0 free tier / $2.30 | **97 s both runs** | none; §3.2.3 storage prohibition |

**API-quality scorecard (all-persona aggregate, /10, max attainable 9.2):** Google 7.66 · Lobstr 6.46 · Outscraper 6.22 · Apify 4.97 (`research/analysis/scorecard.md`; HasData/Bright Data/ScrapingDog joined after the scored benchmark — their measured axes are in this table, full rubric scoring pending a re-run under identical conditions).

## Google Places API (New) — the direct answer for persona 1

**Is it "enough"? No — but not because of price.** Numbers: ~$1.75/1K businesses at the 4-field Enterprise mask ($2.30 measured at our fuller mask), $0 within 1,000 free calls/mo, 1.54s median, best fill-rates tested. It fails on: (1) **result ceiling** — 60/query hard cap, hit on 10/10 restaurant queries; matching scraper volume takes 3–4× more queries with overlap; ranked-not-complete results; (2) **terms** — §3.2.3 "No Scraping/No Caching/No Creating Content": storing anything beyond place IDs is prohibited, so the persona's deliverable (a saved list) is disallowed; (3) **friction** — billing card required, SKU/field-mask learning curve. Where it wins: real-time in-app display, freshness, reliability, free tier.

## Methodology
Queries: 2 industries × 10 borough/district sub-areas (NYC boroughs; 5 major LA districts), `scripts/lib/config.py`. Volumes: scrapers up to 200/sub-area (Outscraper 80, budget); stage-2 for post-brief candidates 2×1,000 (HasData ran the benchmark-standard 200s: 2,946 rows). Plans tested: Lobstr Growth, Apify Starter, Outscraper PAYG, HasData Startup, Bright Data PAYG key, ScrapingDog free, Google free tier. Dedupe: `scripts/lib/dedupe.py` (place_id → URL → name+address hash). Dates: all runs 2026-09-22/23; pricing pages fetched live 2026-09-23.

## What we changed and why
1. **ScrapingDog and Bright Data reinstated** (were excluded for lacking emails/socials — a persona-2-only need; both are persona-1 contenders on measured fills/price).
2. **Google Places API (New) treated as a full competitor** — tested on the same workload, scored, and answered per persona instead of dismissed as a baseline; its ToS storage prohibition verified from Google's own terms and moved from "win" to the decisive persona-1 blocker.
3. **Two-stage free→scale method adopted** — smokes caught the findings that matter before spend (ScrapingDog's duplicate billing, HasData's status quirk, Bright Data's missing contact fields).
