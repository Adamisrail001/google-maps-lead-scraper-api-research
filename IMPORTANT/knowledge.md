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
| {X} Official API | [E1–E6 or PASS] | [reason] | [evidence link] |

**All benchmarked providers — elimination status (sourced, per-provider `elimination-assessment.md` files):**

| Provider | E1 | E2 | E3 | E4 | E5 | E6 | Evidence |
|---|---|---|---|---|---|---|---|
| [Provider 1] | | | | | | | |
| [Provider 2] | | | | | | | |
| [Provider 3] | | | | | | | |

---

## Official API Deep-Dive ({X})

- **What it actually offers:** [TBD]
- **Access model:** [self-serve / waitlist / sales-gated]
- **Pricing:** [TBD or MISSING]
- **THE wall:** [the specific reason this fails E1, if it does]
- **Live access / code example:** [obtained / not obtained]

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
