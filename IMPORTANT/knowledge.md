# {X} {Data Type} Scraping API Benchmark — Knowledge Base

> This document is the verified factual record for the {X} API benchmark and the article built on it. Every claim and figure below must trace to logged benchmark evidence — nothing is inferred, estimated, or assumed. Evidence status is marked throughout: ✅ **CAPTURED** (complete, traceable evidence), ⚠️ **PARTIAL** (incomplete validation), ❌ **MISSING** / **Not tested** (no evidence — never softened into an estimate), ❓ **UNCLEAR** (provenance or interpretation unconfirmed), 🔴 **DISCREPANCY** (sources conflict, not silently resolved).
>
> Corrections to earlier entries in this document are never silently overwritten — mark the correction inline (🔴), state what changed and why, and leave the superseded text in place for provenance unless explicitly told to remove it.
>
> **Scope of the benchmark:** [list every provider tested] were each run once, on the same fixed set of {X} targets — [list targets] — each targeting [N] records ([total] requested per provider). Fill in once the target list and run design are decided (see `scripts/lib/config.py`).

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
| [Provider 1] | | | | | | | |
| [Provider 2] | | | | | | | |
| [Provider 3] | | | | | | | |

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

**Cross-provider reliability summary**

| Provider | Requested | Raw / Unique returned | Success rate | Real errors this run |
|---|---:|---|---:|---|
| | | | | |

---

## 2. Cost Effectiveness

> Strict distinction maintained throughout: **confirmed billed cost** (from the provider's own billing field) vs. **API usage field** vs. **published rate-card calculation** vs. **credit count with no monetary conversion** vs. **no direct charge observed during the test.** These are never conflated.

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

**Cross-provider speed summary**

| Provider | Total wall-clock | Median latency | p95 latency | Execution model |
|---|---:|---:|---:|---|
| | | | | |

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

### [Provider 1]

- **Field coverage vs ground truth:**
- **Data accuracy:**
- **Schema consistency:**
- **Freshness:**

---

## Final Summary — which platform looks strongest

### 1. [Provider] — [one-line verdict]

### 2. [Provider] — [one-line verdict]

### 3. [Provider] — [one-line verdict]

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
