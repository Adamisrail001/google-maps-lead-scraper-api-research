# {X} {Data Type} Scraping API Benchmark — Knowledge Base

> This document is the verified factual record for the {X} API benchmark and the article built on it. Every claim and figure below must trace to logged benchmark evidence — nothing is inferred, estimated, or assumed. Evidence status is marked throughout: ✅ **CAPTURED** (complete, traceable evidence), ⚠️ **PARTIAL** (incomplete validation), ❌ **MISSING** / **Not tested** (no evidence — never softened into an estimate), ❓ **UNCLEAR** (provenance or interpretation unconfirmed), 🔴 **DISCREPANCY** (sources conflict, not silently resolved).
>
> Corrections to earlier entries in this document are never silently overwritten — mark the correction inline (🔴), state what changed and why, and leave the superseded text in place for provenance unless explicitly told to remove it.
>
> **Scope of the benchmark:** Lobstr.io, Apify (`themineworks/maps-leads`), Outscraper (base scrape, reduced budget scope), and Google Places API (New) were each run on the same fixed target set — 2 runs (marketing agencies, restaurants) × 10 NYC/LA borough/district sub-areas (`scripts/lib/config.py`) — scrapers requesting up to 200/sub-area (Outscraper 80, budget-capped; Google hard-capped at 60/query by its own API). Run window 2026-09-22/23. Scorecard: `research/analysis/scorecard.md` (reproducible via `scripts/compute_scorecard.py`).

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
| Google Places API (New) | **PASS — tested as full contender** | Self-serve key + full run same day (E1 ✓), 60/60 requests succeeded (E2 ✓), docs complete (E3 ✓), cost computable to the cent (E4 ✓), returns core business data (E5 ✓), actively maintained (E6 ✓). Product-fit walls (no email/social fields; 60/query cap) are findings, not eliminations. | `research/raw/google-places-api/run-log.json`, `research/analysis/google-places-api-cost-speed.md` |

**All benchmarked providers — elimination status (sourced, per-provider `elimination-assessment.md` files):**

| Provider | E1 | E2 | E3 | E4 | E5 | E6 | Evidence |
|---|---|---|---|---|---|---|---|
| Lobstr.io | ✓ | ✓ (79.7%) | ✓ (page_size gap noted) | ✓ ($6.05/1K at Growth rate) | ✓ | ✓ | run `e57af71d`, `data/lobstr/` |
| Apify | ✓ | ✓ (80.4% — truncations documented, above 50% floor) | ✓ (guards undocumented, but working request buildable) | ✓ ($0.64/1K, billed API) | ✓ | ✓ | `data/apify/`, billing API |
| Outscraper | ✓ | ✓ (93.5%) | ✓ | ✓ ($4.69/1K rate-card) | ✓ | ✓ | `data/outscraper/` |
| Google Places API (New) | ✓ | ✓ (60/60) | ✓ | ✓ ($2.70/1K rate-card; $0 free tier) | ✓ (returns business data; contact fields absent = finding, not E5) | ✓ | `research/raw/google-places-api/` |

All four pass E1–E6 — no eliminations this benchmark.

**Candidate eliminations from post-benchmark smoke tests (decision 2026-09-23, per lead's free-test-first policy):**

| Provider | Criterion failed | One-line reason | Evidence |
|---|---|---|---|
| Scrapingdog | E5 (article's core data type = lead contact data) | Smoke test PASSED on API quality (fields 95–100%, 1.5s median, "failed requests never charged" verified true) but **0% emails and 0% socials by design — fields don't exist in the response**; same disqualification as Google's API for the lead-gen intent, and a second contact-less provider in the ranking dilutes the piece. Retained for one use-case mention (bulk business data ~$0.04–0.15/1K projected) + the measured 🔴 finding that past ~75 uniques/query it serves fully-billed HTTP-200 duplicate pages with no exhaustion signal. | `data/scrapingdog/reports/smoke-findings.md`, raw in `data/scrapingdog/raw/smoke/` |
| Bright Data | E5 (article's core data type = lead contact data) | Smoke test (Web Scraper API, dataset `gd_m8ebnr0q2qlklc02fz` "Google Maps full information", discovery by location, limit 10) PASSED on API quality — 10/10 records, 0 errors, 130s trigger→ready, **perfect core fills** (name/address/phone/website/category/rating/review count/hours/coords/images all 10/10, plus review distribution/snippets/top reviews) — but **zero email and zero social fields confirmed**: none in the 39-field schema, zero @-pattern strings in the full payload. Resolves the docs-unverifiable "not indicated" to **absent**. Scale test not run — budget redirected to HasData. Retained for one bulk-data use-case mention; rate-card ~$0.75–1.50/1K records still unconfirmed by any billed run. Caveats for any future run: discovery inputs are `country`+`keyword` (or place_id/cid), no text-query mode (input-comparability gap); brightdata.com zone blocked by local DNS — use DoH-resolved pinned IP. | `data/brightdata/reports/smoke-findings.md`, raw in `data/brightdata/raw/smoke/` |

---

## Post-benchmark candidate pipeline (smoke → scale, decisions 2026-09-23)

| Candidate | Smoke result | Decision |
|---|---|---|
| **HasData** | ✅ PASS — **70% email fill (14/20) via API** on the Van Nuys agencies query (vs Lobstr 59% / Apify 32% same vertical — n=20 caveat); base billing exact (3 credits/row), email job billed 158 not the naive 200 (undocumented partial charging, favorable); ~18s for 20 email-enriched rows; 278/1,000 free credits spent | **→ SCALE TEST approved** — full 2-run benchmark ≈ 32K credits, needs Startup plan ($49/mo, 200K credits). Projected ~$1.94/1K email rows ≈ 3× cheaper than Lobstr's measured $5.82 — the only untested provider that can move the lead-gen ranking. Scale-script rules: poll the **results endpoint, not job status** (status sticks at `exporting_data` while data is complete 🔴); schema varies with `extractEmails` (hours/open-state columns dropped); socials = separate 5-credit enrichments, untested. Evidence: `data/hasdata/reports/smoke-findings.md` |
| **Scrapingdog** | ✅ API quality / ❌ lead fields (see elimination above) | **→ ELIMINATED from the ranking** (E5, lead-data absence); keep one line in the bulk-data use-case section |
| **Bright Data** | ✅ smoke completed 2026-09-23 (second key, account active): 10/10 records, 0 errors, 130s; **core fills perfect** (name/address/phone/website/rating/hours/reviews/coords all 10/10) — but **ZERO email + ZERO social fields confirmed in the full payload** (no email/social keys in the 39-field schema, zero @-pattern strings). The "not indicated" question is now resolved: absent. | **→ ELIMINATED from the lead-gen ranking (E5, same path as Scrapingdog); scale test NOT run** — a contact-less provider can't move the lead-gen verdict, budget redirected to HasData. Retained for one bulk-data use-case mention (rate-card ~$0.75–1.50/1K, still unconfirmed by any billed run). Evidence: `data/brightdata/reports/smoke-findings.md` |

---

## Official API Deep-Dive (Google Places API (New)) — ✅ CAPTURED, live-tested 2026-09-23

> Per reviewer direction (2026-09-23), the official API is a **full tested contender**, not a docs-only baseline. Run on the identical workload as the scrapers (2 runs × 10 sub-area Text Search queries). Evidence: `research/raw/google-places-api/` (60 raw responses + run-log.json), `research/analysis/google-places-api-cost-speed.md`, scripts `scripts/google_places_run.py` / `google_places_analyze.py`.

- **What it actually offers:** Text Search (New) `places:searchText` with FieldMask-based SKU billing. Full lead-relevant mask (phone, website, rating, hours, reviews) bills as **Text Search Enterprise + Atmosphere** (SKU 120C-BEC3-B48F). ✅
- **Access model:** fully self-serve — API key, no sales contact. Key obtained and run completed same day (passes E1 by a wide margin). ✅
- **Pricing (fetched live 2026-09-23 from Google's pricing page):** $40/1K requests at Enterprise+Atmosphere tier; **1,000 free events/mo per SKU** (post-March-2025 model; the old $200/mo credit is gone). Pro tier (no phone/website/reviews) $32/1K with 5,000 free/mo — insufficient fields for lead use. ✅
- **Benchmark result:** 60 requests → 1,120 raw / **1,044 unique** places (Run 1: 444, Run 2: 600), 0 errors, 97.0s wall-clock, latency median 1.54s / p95 2.26s. **Measured billed cost: $0.00** (inside free tier); rate-card equivalent $2.40 → **$2.30/1K unique businesses**. ✅
- **Field coverage (measured on 1,044 uniques):** phone 95.4%, website 94.3%, rating+count 97.7%, hours 97.9%, photos-refs 94.7% — the best fill-rates of the four tested providers. ✅
- **THE wall (two, both measured — E-criteria PASS, product-fit walls):**
  1. **No email, social-profile, contact-form, owner, or popular-times fields exist in the API surface at any price** — disqualifying for outreach lead lists (vs Lobstr 59% emails / Apify 32% verified emails on the same queries). Reviews hard-capped at 5/place. ✅
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

**Scorecard totals (max attainable 9.2 — accuracy & freshness unscoreable for all, zeroed equally; full sub-scores with evidence in `research/analysis/scorecard.md`):**

| Provider | Reliability /2.0 | Data /2.0 | Cost /1.5 | Speed /1.5 | Scale /1.2 | Usability /1.8 | **Total /10** |
|---|---:|---:|---:|---:|---:|---:|---:|
| Google Places API (New) | 1.96 | 1.13 | 0.77 | 1.34 | 0.96 | 1.50 | **7.66** |
| Lobstr.io | 1.88 | 1.20 | 0.61 | 0.21 | 1.20 | 1.36 | **6.46** |
| Outscraper | 1.88 | 1.08 | 0.70 | 0.20 | 0.88 | 1.48 | **6.22** |
| Apify | 0.91 | 0.87 | 1.34 | 0.21 | 0.44 | 1.20 | **4.97** |

*(Recomputed 2026-09-23 on BOTH runs after Run-2 pooling — supersedes the Run-1-only totals 7.70/6.44/6.19/5.10 previously recorded here; ranking unchanged, Apify fell further below the 6.0 band on its 68.3% both-run delivery.)*

**Intent rule for the article (load-bearing):** the rubric scores *API quality*. Google tops it while being structurally incapable of the article's core use case — no email/social/contact fields exist in its API at any price — so it is **not eligible for the lead-generation verdict**; its 7.66 answers "how good is this API", not "can it produce leads". Ranked for the lead-gen searcher: **Lobstr 6.46 · Outscraper 6.22 · Apify 4.97**.

**Both-run measured costs (Lobstr Run-2 credits fetched live 2026-09-23, run `6b7150f5`: 5,342 credits):** Apify $1.3656 billed / 2,523 uniques = **$0.54/1K** · Google $2.40 rate-card / 1,044 = **$2.30/1K** ($0 billed, free tier) · Outscraper $4.80 rate-card / 1,300 = **$3.69/1K** (base only) · Lobstr 8,968 credits × Growth rate = $14.95 / 2,567 = **$5.82/1K** (incl. 1,747 extracted emails + socials + images).

### 1. Google Places API (New) — 7.66 — best-engineered API in the test (perfect reliability, 1.54s median, best docs, best core-field fill 94–98%); zero lead capability, 60/query cap. Winner only outside lead gen (core-data accuracy, ≤1K free calls/mo).

### 2. Lobstr.io (house product — disclosed) — 6.46 — top scraper: wins Data Quality (59% emails + ~50% socials, richest lead records) and Scalability (user-set concurrency, no hidden caps found); most expensive at $5.82/1K unique both-run measured (Growth rate) and slow wall-clock. Per criteria.md house rule: did NOT win the aggregate → not crowned; placed where it genuinely wins — contact-complete lead lists.

### 3. Outscraper — 6.22 — solid middle on a budget-reduced test (base scrape, 80/query): 93.5% delivery, richest default listing schema, cheapest full-stack enrichment path on paper; email stages untested (budget), several usability sub-scores on thin evidence.

### 4. Apify — 4.97 — below the 6.0 "recommended at scale" band despite winning Cost ($0.54/1K both-run, only verified-email leads billed, empirically proven): the two undocumented profit-guards silently truncated 4/20 queries (🔴 worst trust finding of the benchmark), business_status broken on 100% of records, and top-level SUCCEEDED masks under-delivery. Cheapness and untrustworthiness share the same mechanism.

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
