# {X} {Data Type} Scraping API Benchmark — Knowledge Base

> This document is the verified factual record for the {X} API benchmark and the article built on it. Every claim and figure below must trace to logged benchmark evidence — nothing is inferred, estimated, or assumed. Evidence status is marked throughout: ✅ **CAPTURED** (complete, traceable evidence), ⚠️ **PARTIAL** (incomplete validation), ❌ **MISSING** / **Not tested** (no evidence — never softened into an estimate), ❓ **UNCLEAR** (provenance or interpretation unconfirmed), 🔴 **DISCREPANCY** (sources conflict, not silently resolved).
>
> Corrections to earlier entries in this document are never silently overwritten — mark the correction inline (🔴), state what changed and why, and leave the superseded text in place for provenance unless explicitly told to remove it.
>
> **Scope of the benchmark:** Lobstr.io, Apify (`themineworks/maps-leads`), Outscraper (base scrape, reduced budget scope), and Google Places API (New) were each run on the same fixed target set — 2 runs (marketing agencies, restaurants) × 10 NYC/LA borough/district sub-areas (`scripts/lib/config.py`) — scrapers requesting up to 200/sub-area (Outscraper 80, budget-capped; Google hard-capped at 60/query by its own API). HasData and Bright Data ran the same query set in stage-2 (2026-09-23). Run window 2026-09-22/24.
> **Scoring of record (2026-09-24):** `scoring.md` at repo root, computed by `scripts/compute_final_scorecard.py` under the core-requirement check in `IMPORTANT/criteria.md` Step 0 — the user's job is extracting all listings from a search with name/address/phone/hours, affordably and reliably; enrichment is bonus, never a requirement; **disqualified providers receive NO score** (results shown as findings only). `research/analysis/scorecard.md` is the superseded v1 rubric, kept as provenance.

---

## Article Meta

- **Primary SEO keyword:** [TBD — writer-confirmed]
- **Full roster tested:** [Provider 1], [Provider 2], [Provider 3], … ({X}'s own official API [was / was not] tested — see "Eliminations" below).

---

## Benchmark Methodology Record

- **Test window:** [dates the raw evidence spans]
- **Shared script template:** one benchmark script template adapted per provider's auth/request format.
- **What was logged:** raw request/response captures, timings, error/cost/pagination reports per provider.
- **Public repo URL:** https://github.com/Adamisrail001/google-maps-lead-scraper-api-research (made public 2026-09-23; contains `research/` discovery evidence, `data/` benchmark raw evidence, `scripts/`, and this methodology doc — `.env`, `prompt.txt`, and `outputs/` scratch excluded; oversized `data/lobstr/raw/results/run2-page1.json` tracked as `.json.gz` due to GitHub's 100MB limit)

---

## Eliminations (E1–E6)

**{X}'s official API — the elimination check:**

| API | Criterion failed | One-line reason | Evidence |
|---|---|---|---|
| Google Places API (New) | **DISQUALIFIED — NOT SCORED (core-requirement check, final form 2026-09-24)** 🔴 supersedes both the earlier "PASS — full contender" entry below and the 2026-09-23 three-ground E5 framing: under the final core-requirement screen the grounds are TWO, and optional-data absence is never an elimination ground | Two verified grounds: **(1) contractual** — Maps Platform Terms §3.2.3, accepted by every API customer at signup, prohibits "copying and saving business names, addresses, or user reviews" and storing anything beyond place IDs — the extracted, kept list is the user's deliverable (this is the customer's own agreement, NOT the category-wide "scraping violates site ToS" argument criteria.md excludes); **(2) technical** — hard 60-results/query ceiling, measured at the cap on 10/10 restaurant queries (444 vs 998–1,405 scraper uniques on identical Run-1 queries) — blocks "all available listings from a search." 🔴 *Corrected phrasing (2026-09-24, reviewer):* the earlier "zero email/social/contact fields at any price" claim is retired as an elimination ground and restated as a **test-and-docs side finding**: no email or social-profile fields appeared in any of our 60 responses requested with the full Enterprise+Atmosphere field mask, and none are listed in the documented field/SKU tables as fetched 2026-09-23 — a finding about the configurations we verified, not a universal capability claim, and irrelevant to this user's core fields (which Google filled well: phone 95.4%, hours 97.9%). It remains fully covered in the article's "official API" section with all measured numbers, and stays the recommended tool for real-time in-app display — the one use its terms permit. | Terms: cloud.google.com/maps-platform/terms §3.2.3 + developers.google.com/maps/documentation/places/web-service/policies (fetched 2026-09-23); runs: `research/raw/google-places-api/`, `research/analysis/google-places-api-cost-speed.md` |
| *(superseded 2026-09-23)* Google Places API (New) | PASS — tested as full contender | Self-serve key + full run same day (E1 ✓), 60/60 requests succeeded (E2 ✓), docs complete (E3 ✓), cost computable to the cent (E4 ✓), returns core business data (E5 ✓), actively maintained (E6 ✓). Product-fit walls (no email/social fields; 60/query cap) are findings, not eliminations. *(Reversed when §3.2.3 verification established the use case is contractually undeliverable — preserved for provenance.)* | `research/raw/google-places-api/run-log.json` |

**All benchmarked providers — elimination status (sourced, per-provider `elimination-assessment.md` files):**

| Provider | E1 | E2 | E3 | E4 | E5 | E6 | Evidence |
|---|---|---|---|---|---|---|---|
| Lobstr.io | ✓ | ✓ (79.7%) | ✓ (page_size gap noted) | ✓ ($6.05/1K at Growth rate) | ✓ | ✓ | run `e57af71d`, `data/lobstr/` |
| Apify | ✓ | ✓ (80.4% — truncations documented, above 50% floor) | ✓ (guards undocumented, but working request buildable) | ✓ ($0.64/1K, billed API) | ✓ | ✓ | `data/apify/`, billing API |
| Outscraper | ✓ | ✓ (93.5%) | ✓ | ✓ ($4.69/1K rate-card) | ✓ | ✓ | `data/outscraper/` |
| Google Places API (New) | ✓ | ✓ (60/60) | ✓ | ✓ ($2.70/1K rate-card; $0 free tier) | ✓ (returns business data; contact fields absent = finding, not E5) | ✓ | `research/raw/google-places-api/` |

All four pass E1–E6 — no eliminations this benchmark.

**🔴 SUPERSEDED 2026-09-23 (same day, per completion brief + lead feedback in question.txt): the two E5 eliminations below are REVERSED.** The eliminations treated persona-2's needs (emails/socials) as the only user intent; the brief's rule — "no tool is disqualified because it lacks a data point that a persona doesn't need" — reinstates both as **persona-1/persona-3 contenders** (local-data extractor / developer: name, address, phone, website, hours, rating — no contacts needed; see `user-intent.md`). ScrapingDog: scored per persona from stage-1 evidence (stage-2 scale run blocked on paid plan, ~$40 Lite). Bright Data: stage-2 scale run executed 2026-09-23 (2 × 1,000 design). The original elimination entries are preserved below for provenance, per this document's correction rules — their *evidence* remains valid; only the roster *decision* is reversed.

**🔴 FINAL ELIMINATION DECISIONS 2026-09-24 (lead review, prompt.txt final form — core-requirement check, criteria.md Step 0). These are the decisions of record; everything below/above in this section is provenance:**

| Provider | Decision | Ground (core requirement) | Evidence |
|---|---|---|---|
| Google Places API (New) | **DISQUALIFIED — no score** | Required volume (hard 60/query cap, measured 10/10 at cap) + usable results/storage (Terms §3.2.3 bars keeping the extracted list) | row above; `research/raw/google-places-api/` |
| Outscraper | **DISQUALIFIED — no score** | Affordable basic extraction: $3.69/1K unique measured-per-unique on base scrape alone — most expensive basic extraction in test vs $0.54–2.66 for scored providers. Results (97.5% core-4 fills, 96.8% delivery on its budget-reduced 80/query batch) shown as findings only | `data/outscraper/`, scoring.md DQ table |
| ScrapingDog | **PENDING — not disqualified by the core-requirement screen** | No core-requirement failure on evidence (smoke: 95–100% core fills, projected $0.04–0.15/1K); unranked only because the standard full-scale batch hasn't run — supplied key on the free 100-credit plan, verified live via `/account` 2026-09-24 | `data/scrapingdog/reports/smoke-findings.md` |
| Bright Data, HasData, Apify, Lobstr | **SCORED** | Pass all core requirements (missing optional enrichment is never a ground — Bright Data's earlier E5 elimination stays reversed) | scoring.md |

**Candidate eliminations from post-benchmark smoke tests (decision 2026-09-23, per lead's free-test-first policy) — superseded, see above:**

| Provider | Criterion failed | One-line reason | Evidence |
|---|---|---|---|
| Scrapingdog | E5 (article's core data type = lead contact data) | Smoke test PASSED on API quality (fields 95–100%, 1.5s median, "failed requests never charged" verified true) but **0% emails and 0% socials by design — fields don't exist in the response**; same disqualification as Google's API for the lead-gen intent, and a second contact-less provider in the ranking dilutes the piece. Retained for one use-case mention (bulk business data ~$0.04–0.15/1K projected) + the measured 🔴 finding that past ~75 uniques/query it serves fully-billed HTTP-200 duplicate pages with no exhaustion signal. | `data/scrapingdog/reports/smoke-findings.md`, raw in `data/scrapingdog/raw/smoke/` |
| Bright Data | E5 (article's core data type = lead contact data) | Smoke test (Web Scraper API, dataset `gd_m8ebnr0q2qlklc02fz` "Google Maps full information", discovery by location, limit 10) PASSED on API quality — 10/10 records, 0 errors, 130s trigger→ready, **perfect core fills** (name/address/phone/website/category/rating/review count/hours/coords/images all 10/10, plus review distribution/snippets/top reviews) — but **zero email and zero social fields confirmed**: none in the 39-field schema, zero @-pattern strings in the full payload. Resolves the docs-unverifiable "not indicated" to **absent**. Scale test not run — budget redirected to HasData. Retained for one bulk-data use-case mention; rate-card ~$0.75–1.50/1K records still unconfirmed by any billed run. Caveats for any future run: discovery inputs are `country`+`keyword` (or place_id/cid), no text-query mode (input-comparability gap); brightdata.com zone blocked by local DNS — use DoH-resolved pinned IP. | `data/brightdata/reports/smoke-findings.md`, raw in `data/brightdata/raw/smoke/` |

---

## Post-benchmark candidate pipeline (smoke → scale, decisions 2026-09-23)

| Candidate | Smoke result | Decision |
|---|---|---|
| **HasData** | ✅ PASS — **70% email fill (14/20) via API** on the Van Nuys agencies query (vs Lobstr 59% / Apify 32% same vertical — n=20 caveat); base billing exact (3 credits/row), email job billed 158 not the naive 200 (undocumented partial charging, favorable); ~18s for 20 email-enriched rows; 278/1,000 free credits spent | **→ SCALE TEST EXECUTED 2026-09-23 (Startup plan): 2,946 rows → 2,456 unique, email fill 42% blended (46% agencies / 37% restaurants — smoke's 70% did NOT hold at scale), measured $4.29 total → $1.75/1K unique, $4.19/1K emails (~3.3× cheaper than Lobstr on both axes), ~4–5 min/run wall-clock (fastest scraper tested).** Caveats held/new: status never reaches `finished` (poll results 🔴); email-mode field wobble (run1 rating/reviews 73%, address 82%); no socials/images. Full record: `data/hasdata/reports/scale-findings.md` |
| **Scrapingdog** | ✅ API quality / ❌ lead fields (see elimination above) | **→ ELIMINATED from the ranking** (E5, lead-data absence); keep one line in the bulk-data use-case section |
| **Bright Data** | ✅ smoke completed 2026-09-23 (second key, account active): 10/10 records, 0 errors, 130s; **core fills perfect** (name/address/phone/website/rating/hours/reviews/coords all 10/10) — but **ZERO email + ZERO social fields confirmed in the full payload** (no email/social keys in the 39-field schema, zero @-pattern strings). The "not indicated" question is now resolved: absent. | **→ REINSTATED as persona-1/3 contender (roster reversal above) and SCALE TEST EXECUTED 2026-09-23 (2 × 1,000 design): 1,741 rows → 1,738 unique, 3 errors (0.2%), fills phone 93–98% / website 89–92% / rating+reviews 100%, ~6 min/run; zero contacts confirmed at scale (2 incidental @-strings in review text).** Cost NOT measurable via API (no billing field) — rate-card estimate ~$1.50/1K flagged, verify in dashboard. New quirk: progress `ready` ≠ snapshot downloadable (returns `building`, retry ~30s). Full record: `data/brightdata/reports/scale-findings.md` |

---

## Official API Deep-Dive (Google Places API (New)) — ✅ CAPTURED, live-tested 2026-09-23

> Per reviewer direction (2026-09-23), the official API is a **full tested contender**, not a docs-only baseline. Run on the identical workload as the scrapers (2 runs × 10 sub-area Text Search queries). Evidence: `research/raw/google-places-api/` (60 raw responses + run-log.json), `research/analysis/google-places-api-cost-speed.md`, scripts `scripts/google_places_run.py` / `google_places_analyze.py`.

- **What it actually offers:** Text Search (New) `places:searchText` with FieldMask-based SKU billing. Full lead-relevant mask (phone, website, rating, hours, reviews) bills as **Text Search Enterprise + Atmosphere** (SKU 120C-BEC3-B48F). ✅
- **Access model:** fully self-serve — API key, no sales contact. Key obtained and run completed same day (passes E1 by a wide margin). ✅
- **Pricing (fetched live 2026-09-23 from Google's pricing page):** $40/1K requests at Enterprise+Atmosphere tier; **1,000 free events/mo per SKU** (post-March-2025 model; the old $200/mo credit is gone). Pro tier (no phone/website/reviews) $32/1K with 5,000 free/mo — insufficient fields for lead use. ✅
- **Benchmark result:** 60 requests → 1,120 raw / **1,044 unique** places (Run 1: 444, Run 2: 600), 0 errors, 97.0s wall-clock, latency median 1.54s / p95 2.26s. **Measured billed cost: $0.00** (inside free tier); rate-card equivalent $2.40 → **$2.30/1K unique businesses**. ✅
- **Field coverage (measured on 1,044 uniques):** phone 95.4%, website 94.3%, rating+count 97.7%, hours 97.9%, photos-refs 94.7% — the best fill-rates of the four tested providers. ✅
- **THE wall (two, both measured — E-criteria PASS, product-fit walls):**
  1. **No email, social-profile, contact-form, owner, or popular-times fields observed** — 🔴 phrasing corrected 2026-09-24 (reviewer): this is a **test-and-docs finding**, not a universal capability claim — none of these fields appeared in any of our 60 responses requested with the full Enterprise+Atmosphere field mask, and none are listed in the documented field/SKU tables as fetched 2026-09-23. A gap for outreach lead lists (vs Lobstr 59% emails / Apify 32% verified emails on the same queries) — recorded as a finding only, NOT an elimination ground under the final core-requirement screen. Reviews hard-capped at 5/place. ✅
  2. **60-results-per-query hard cap** (20/page × 3 pages) — hit on 10/10 restaurant queries; same 10 Run-1 queries yielded Google 444 uniques vs Lobstr 998 / Apify 1,405 / Outscraper 512. Scraper-scale volume needs ~3–4× more distinct queries with rising overlap (6.8% dupes at 10 sub-areas). ✅
- **Live access / code example:** obtained — reproducible runner in `scripts/google_places_run.py` (key via `.env` `GOOGLE_PLACES_API_KEY`, never committed). ✅
- **THE wall #3 — ToS storage prohibition (✅ verified 2026-09-23 against Google's own terms; supersedes the earlier "zero ToS ambiguity" win claim 🔴):** Maps Platform Terms §3.2.3 (cloud.google.com/maps-platform/terms): **"No Scraping. Customer will not export, extract, or otherwise scrape Google Maps Content for use outside the Services"** — explicitly including **"copying and saving business names, addresses, or user reviews"**; **"No Caching"** except as permitted in the Service Specific Terms; **"No Creating Content From Google Maps Content."** The Places policies page (developers.google.com/maps/documentation/places/web-service/policies, fetched directly) confirms the only durable exception: *"place ID … exempt from the caching restrictions. You can therefore store place ID values indefinitely."* **Implication:** even for the 4-field NAP user at the cheap tier (~$1.75–1.87/1K businesses, pages full), building a stored/exported business list from the official API is contractually prohibited — the compliant use is real-time in-app display. This is a stronger scraper argument than price or the 60-cap, and applies to every user persona in this article. Corrected framing: Google's ToS is unambiguous — but what it unambiguously says is that the article's use cases are not allowed.

---

## 1. Success Rate & Reliability

> Every figure below describes **one benchmark run of [N] requested records per provider**. This is not evidence of reliability under repeated trials, concurrent load, or sustained production use — keep that distinction explicit.

### [Provider 1]

- **Requests attempted:**
- **Successful requests:**
- **Raw / unique records returned:**
- **Retries:**

### [Provider 2]

- (same shape as above)

**Cross-provider reliability summary — ✅ CAPTURED (Run 1, same 10 queries)**

| Provider | Requested | Raw / Unique returned | Success rate | Real errors this run |
|---|---:|---|---:|---|
| Google Places API | 1,200 page-slots (600 doc-max) | 520 / 444 | 93.3% of page-slots, 60/60 HTTP 200 | none |
| Lobstr | 2,000 | 1,594 / 999 | 79.7% returned/requested | none; run `done/tasks_done` |
| Apify | 2,000 | ~1,608 / 1,405 | 80.4% — **but 1/10 queries silently truncated** (Van Nuys 20/200, profit guard; 3/10 in Run 2) | none at HTTP level; top-level SUCCEEDED masks truncation 🔴 |
| Outscraper | 800 (reduced scope) | 748 / 512 | 93.5% | none |

Shortfalls vs requested partly reflect genuine Google Maps data scarcity in some sub-areas (Queens/Bronx/Staten Island/Van Nuys under-filled for every provider) — success rate mixes provider capability with supply; kept explicit, not resolved silently.

**Run 2 (restaurants) — ✅ CAPTURED, pooled 2026-09-23 via `scripts/pool_run2.py` (same dedupe as Run 1):**

| Provider | Requested | Raw / Unique | Delivery | Notes |
|---|---:|---|---:|---|
| Lobstr | 2,000 | 1,809 / 1,569 | 90.5% | server metadata corroborates (total_results 1,570); email fill 37% (vs 59% run1) |
| Apify | 2,000 | 1,122 / 1,118 | **56.1%** 🔴 | profit-breaker on low-email vertical, confirmed pattern (3/10 queries cut; 262 charged vs 527 run1); email 23% |
| Outscraper | 800 | 800 / 788 | 100% of its cap | fill: phone 97%, website 93%, rating 100%, hours 99% |
| Google Places API | 600 doc-max | 600 / 600 | 100% of its cap | all 10 queries hit the 60 ceiling exactly |

**Both-run unique totals:** Lobstr 2,567 · Apify 2,523 · Outscraper 1,300 · Google 1,044.
**Cross-run delivery flip (article-worthy):** Apify out-delivered Lobstr on agencies (80.4% vs 79.7%) but collapsed on restaurants (56.1% vs 90.5%) — its economics-driven early exits make delivery *vertical-dependent*, while Lobstr's delivery tracked data supply. Email yield fell for every provider on restaurants (industry property, not tool property).

---

## 2. Cost Effectiveness

> Strict distinction maintained throughout: **confirmed billed cost** (from the provider's own billing field) vs. **API usage field** vs. **published rate-card calculation** vs. **credit count with no monetary conversion** vs. **no direct charge observed during the test.** These are never conflated.

**Run 1 measured costs (same 10 sub-area queries) — ✅ CAPTURED 2026-09-23:**

| Provider | Evidence tier | Measured basis | Cost / 1K unique results |
|---|---|---|---:|
| Apify | confirmed billed (billing API `usageTotalUsd`) | $0.8932 Run 1 ($0.4724 Run 2) — only 451 verified-email leads charged | **$0.64** |
| Google Places API (New) | $0 billed (free tier) + live rate-card | 30 req × $40/1K Enterprise+Atmosphere → 444 unique | **$0 in free tier; $2.70 after** (no contact fields) |
| Outscraper | published rate-card ($3/1K base) | 800 requested → 512 unique, base scrape only | **$4.69** (listings only; email stages not run) |
| Lobstr | API usage field (`credit_used: 3626`, run `e57af71d…`) × account plan rate (Growth, $50/mo ÷ 30,000 credits, user-confirmed 2026-09-23) | $6.04 Run 1 → 999 unique, incl. 974 extracted emails + details + images | **$6.05** (≈$2.66 without email extraction) |

Caveats that must travel with any cost table: Apify's figure buys 32% verified-email coverage; Lobstr's buys 59% email + ~50% socials coverage (extraction-only); Google's buys zero contact fields; Outscraper's buys bare listings. These are different products per dollar — never rank on price alone.

### [Provider 1]

- **Billing model:**
- **Published pricing:**
- **Measured billed cost:**
- **Cost per 1,000 successful records:**

**Cross-provider cost summary**

| Provider | Cost evidence tier | Cost per 1,000 successful records |
|---|---|---:|
| | | |

---

## 3. Speed

> Timing figures are **not directly comparable** across providers without accounting for differing execution models — note whether each provider is synchronous, async submit-then-poll, or async with a separate paginated retrieval phase.

### [Provider 1]

- **Total wall-clock duration:**
- **Median latency:**
- **p95 latency:**
- **Requests:**

**Cross-provider speed summary — ✅ CAPTURED (Run 1; architectures differ, never rank raw wall-clock without the §5 concurrency caveat)**

| Provider | Total wall-clock | Median latency | p95 latency | Execution model |
|---|---:|---:|---:|---|
| Google Places API | ~46 s (97.0 s both runs) | 1.54 s | 2.26 s | synchronous request/response |
| Lobstr | 28 m 31 s (1,711 s) | N/A (batch) | N/A | squid → poll; concurrency 20; includes per-row website-visit email extraction |
| Apify | 2,194.5 s cumulative across 10 separate actor runs (parallelizable) | N/A (batch) | N/A | actor → dataset; includes email extraction + DNS/MX verification |
| Outscraper | ❌ not aggregated from raw evidence | N/A | N/A | async 3-stage (base only run) |

Scrapers do materially more work per row (website visits for contacts); Google returns 20 records/call with no enrichment. Comparable order-of-magnitude between scrapers only.

---

## 4. Scalability

> Note explicitly whether real concurrency and 10x-volume degradation were tested, or only the standard single-run benchmark.

### [Provider 1]

- **Max records tested from one target:**
- **Concurrency tested:**
- **Volume caps observed:**

---

## 4a. Data Coverage & Collection Depth

> Whether a provider can collect *past* the standard per-target target size — a distinct question from raw success rate at the standard depth.

### [Provider 1]

---

## 5. Developer Experience & Usability

### [Provider 1]

- **Time-to-first-successful-request:**
- **Docs quality:**
- **SDKs / code examples:**
- **Error message clarity + support responsiveness:**

---

## 6. Data Quality & Completeness

> State clearly which target(s) have ground truth available. Any accuracy/field-coverage figure is valid only for targets with ground truth — never generalize to targets without it.

**❌ Ground truth was never built** (testing-plan §10, open item) — the fill-rates below are measured field-presence on Run-1 unique results, a coverage proxy, NOT accuracy. Accuracy and freshness scored 0 for all providers in the scorecard, flagged not-measurable.

| Field (fill-rate, Run 1 uniques) | Google (444) | Lobstr (998) | Apify (1,405) | Outscraper (512) |
|---|---:|---:|---:|---:|
| Name / address / coordinates | 100% | 100% | 100% | 100% |
| Phone | 95% | 91% | 90% | 91% |
| Website | 94% | 93% | 83% | 94% |
| Category | 99% | 100% | 100% | 48% |
| Rating / review count | 98% / 98% | 86% / 86% | 67% / — (no field) | 92% / 92% |
| Opening hours | 98% | 90% | 83% | 90% |
| Photos/images | 95% (refs) | 81% | — (absent) | 99% |
| **Email** | **impossible (no field)** | **59%** (extraction-only; 974 total incl. multiples) | 32% (DNS/MX-verified — never compare 1:1 with extraction-only, §7 rule) | not run (budget) |
| **Socials** | **impossible** | ~48–54% (FB/IG/LinkedIn/TikTok/…) | — | not run |
| Schema consistency | Full | Full | 🔴 business_status "UNKNOWN" on 100% of records | Full |

---

## Final Summary — which platform looks strongest

**🔴 REWRITTEN 2026-09-24 (supersedes the earlier version of this section, which ranked under the v1 rubric and displayed "reference" scores for disqualified providers — retired; git history preserves it).** Scoring of record: `scoring.md`, computed by `scripts/compute_final_scorecard.py` under criteria.md's 7-criterion rubric (§4, unchanged) after the core-requirement check (Step 0). The user's job: **extract all available listings from a search — name, address, phone, opening hours — reliably and affordably.** Enrichment is bonus value inside Data Quality, never a requirement. **Disqualified providers receive no score.** Max attainable 9.2 (accuracy & freshness unscoreable for all, zeroed equally); median/p95 latency also zero for all four (all batch/async — architecture-neutral).

| Rank | Provider | Reliability /2.0 | Data /2.0 | Cost /1.5 | Speed /1.5 | Scale /1.2 | DevEx /1.0 | Input /0.8 | **Total /10** |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | **Lobstr.io** (house — disclosed) | 1.98 | 1.20 | 0.70 | 0.31 | 1.20 | 0.76 | 0.60 | **6.75** |
| 2 | HasData | 1.57 | 0.90 | 1.20 | 0.62 | 1.00 | 0.72 | 0.68 | **6.69** |
| 3 | Bright Data | 1.88 | 1.00 | 0.51 | 0.70 | 0.88 | 0.36 | 0.38 | **5.71** |
| 4 | Apify | 0.98 | 0.87 | 1.34 | 0.28 | 0.44 | 0.72 | 0.48 | **5.11** |

**Sensitivity check on the thin #1 margin (0.06), given the house-product disclosure:** recomputing Cost with as-tested measured spend instead of basic-workload framing (Lobstr $5.82/1K, HasData $1.75/1K) gives Lobstr 6.66 vs HasData 6.36 — the #1 spot is stable under both consistent cost framings (`scoring.md`).

**Basic-extraction costs used for the Cost criterion (prompt rule: basic workload first, enrichment separate):** Apify **$0.54/1K** billed — flagged: no basic-only price exists, it bills per verified-email lead · HasData **~$0.74/1K** base-mode rate-card ($1.75/1K measured in email mode) · Bright Data **~$1.50/1K** rate-card estimate, unverified (no billing visibility) · Lobstr **≈$2.66/1K** derived from measured credits with the email-extraction share removed ($5.82/1K as-tested incl. enrichment).

### 1. Lobstr.io (house — disclosed) — 6.75 — wins Reliability (85.1% delivery, zero silent truncation), Data Quality (best core-4 fill 97.1%, plus the enrichment reference point: 45.3% email + 56.8% socials — bonus, not requirement), and Scalability (user-set concurrency, no hidden caps found). Loses ground on Cost (≈$2.66/1K basic, 5× the cheapest) and Speed (28m31s Run 1, incl. per-row website visits for enrichment — caveat attached). The margin over HasData is 0.06 — disclosed and sensitivity-checked above.

### 2. HasData — 6.69 — the value pick: cheapest measured-plan basic rate (~$0.74/1K base mode), fastest full runs (7m11s email-mode Run 1), 94.2% core fills, 41.7% email fill as bonus. Held back by 73.7% delivery, run-to-run field wobble (run1 rating/reviews 73% vs run2 100%), and a 5-concurrency entry-plan cap.

### 3. Bright Data — 5.71 — the best pure-listings executor tested (96.4% core fills, 87.1% delivery, 0.2% error rows) dragged down by opacity and friction: no billing visibility (cost unverifiable), docs unreachable from the test env, onboarding/geo friction, keyword-only inputs.

### 4. Apify — 5.11 — cheapest billed figure but the benchmark's worst trust findings, which hit this user's "reliably" requirement hardest: two undocumented profit-guards silently truncated 4/20 queries while reporting SUCCEEDED (🔴 worst trust finding), business_status broken on 100% of records, and structural under-delivery on low-email verticals — a listings user pays in missing listings for an economics model built around emails they don't need.

### DISQUALIFIED — no score (results shown as findings; full grounds in the Eliminations decisions table above)

- **Google Places API (New):** hard 60/query cap (measured 10/10 at cap) + Terms §3.2.3 bars keeping the extracted list. Otherwise the best-engineered API tested (60/60 requests, 1.54s median, phone 95.4% / hours 97.9% fills, $2.30/1K rate-card, $0 billed in free tier) — recommended for the one permitted use, real-time in-app display. Side finding (test-and-docs, not universal): no email/social fields in our 60 full-field-mask responses nor in the documented field/SKU tables (fetched 2026-09-23).
- **Outscraper:** fails affordable basic extraction — $3.69/1K unique measured-per-unique on base scrape alone, most expensive in test vs $0.54–2.66 for scored providers (enrichment would add up to +$6/1K by its published stage pricing; email stages remain untested — full-scope re-run declined 2026-09-23 on that projection). Otherwise strong on this user's job: best core-4 fills (97.5%), 96.8% delivery on its budget-reduced 80/query batch (flagged), richest default listing schema.

### PENDING — ScrapingDog (not disqualified by the core-requirement screen)

No core-requirement failure on evidence; smoke fits this user's profile exactly (95–100% core fills, ~1.5s median, projected $0.04–0.15/1K — cheapest in test by an order of magnitude). Unranked only because the standard full-scale batch hasn't run: the supplied key is on the free 100-credit plan (verified live via `/account`, 2026-09-24). Smoke risk to verify at scale: past ~75 uniques/query it serves fully-billed duplicate pages with no exhaustion signal.

---

## FAQ

### Why isn't [Provider] ranked / included?

### Is scraping {X} data legal?

### Is the {X} official API free?

---

## Winner Quickstart Facts

### [Provider]

---

## Concept Explainer Choice

[What background concept the article needs to explain before the comparison, if any.]

---

## Store / Links

- [Standard CTA links, help center, legal disclosures, etc.]

---

## Open Items

- [ ] [Anything genuinely unresolved — list explicitly, never silently drop.]
