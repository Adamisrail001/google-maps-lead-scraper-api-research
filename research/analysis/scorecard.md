# Benchmark Scorecard — 10-Point Rubric (testing-plan §2, method §13)

**Computed:** 2026-09-23 by `scripts/compute_scorecard.py` (rerun it to regenerate; every sub-score carries its basis + evidence).

> **Unscoreable on existing evidence, zeroed for ALL providers equally (0.8 pts):** Accuracy-vs-ground-truth (0.5 — sample never built, testing-plan §10 open item) and Freshness (0.3 — no signal collected). Max attainable = 9.2.
> **Rubric artifacts to keep in mind:** wall-clock ratio scoring severely penalizes batch scrapers that do per-row website-visit enrichment vs a sync API returning 20 records/call (§5 reporting rule caveat applies); Outscraper scored on its reduced budget scope (base scrape, 80/query); Google's cost scored on rate-card since its run billed $0 in free tier.
> **Disclosure:** Lobstr.io is the house product. Per criteria.md writer rules, the aggregate winner is whoever scores highest — no predetermined outcome.

## Criterion scores

| Criterion | Max | Lobstr | Apify | Outscraper | Google |
|---|---:|---:|---:|---:|---:|
| Reliability | 2.0 | 1.85 | 1.06 | 1.88 | 2.00 |
| Data Quality | 2.0 | 1.20 | 0.85 | 1.06 | 1.13 |
| Cost | 1.5 | 0.62 | 1.34 | 0.69 | 0.77 |
| Speed | 1.5 | 0.21 | 0.21 | 0.20 | 1.34 |
| Scalability | 1.2 | 1.20 | 0.44 | 0.88 | 0.96 |
| Usability | 1.8 | 1.36 | 1.20 | 1.48 | 1.50 |
| **TOTAL /10** | 10.0 | **6.44** | **5.10** | **6.19** | **7.70** |

## Sub-criterion detail

### Reliability

**Success rate (returned/requested, ratio vs best 93.5%)** (1.0 pts)
- Lobstr: **0.85** — 1,594/2,000 raw returned = 79.7% (run e57af71d)
- Apify: **0.86** — 1,608/2,000 = 80.4% (run1 datasets)
- Outscraper: **1.0** — 748/800 = 93.5% (512 unique + 236 dups)
- Google: **1.0** — 1,120/1,200 page-slots = 93.3% (run-log.json)

**Empty/partial responses (anchor)** (0.4 pts)
- Lobstr: **0.4** — Full - none observed
- Apify: **0.08** — Weak - 4/20 queries silently truncated by profit guards; business_status broken on 100% of records
- Outscraper: **0.4** — Full - none observed
- Google: **0.4** — Full - none; sub-60 pages traced to data scarcity, documented

**Error handling quality (anchor)** (0.3 pts)
- Lobstr: **0.3** — Full - live 400 AttributeLimitExceeded was precise, actionable
- Apify: **0.06** — Weak - top-level SUCCEEDED masks truncation; only raw log reveals it
- Outscraper: **0.18** — Partial - no errors encountered, quality unassessed (flag: thin evidence)
- Google: **0.3** — Full - structured google.rpc errors, clean retry semantics

**Stability during window (anchor)** (0.3 pts)
- Lobstr: **0.3** — Full - both runs completed, no degradation
- Apify: **0.06** — Weak - profitability breaker cut queries mid-processing (Van Nuys 20/200; 3 more in run2)
- Outscraper: **0.3** — Full - completed normally
- Google: **0.3** — Full - 60/60 HTTP 200, latency stable (p95 2.26s)

### Data Quality

**Field coverage, 10 lead fields, measured fill-rate proxy (ratio vs best 85.6) - GROUND TRUTH NOT BUILT, proxy flagged** (0.8 pts)
- Lobstr: **0.8** — 85.6 (core-8 93.3 + email 59 + socials 51)
- Apify: **0.61** — 65.3 (core-8 77.9 + email 32 + 0; no review-count field)
- Outscraper: **0.66** — 70.7 (core-8 88.4, category only 48%; no email/socials in base scope)
- Google: **0.73** — 78.2 (core-8 97.75 - best core fill - + email 0 + socials 0, fields absent from API)

**Accuracy vs ground truth - NOT MEASURED (sample never built)** (0.5 pts)
- Lobstr: **0.0** — not measurable - scored 0 for all, per plan rule
- Apify: **0.0** — not measurable - scored 0 for all, per plan rule
- Outscraper: **0.0** — not measurable - scored 0 for all, per plan rule
- Google: **0.0** — not measurable - scored 0 for all, per plan rule

**Schema consistency (anchor)** (0.4 pts)
- Lobstr: **0.4** — Full - consistent 90+ field schema
- Apify: **0.24** — Partial - business_status returns UNKNOWN universally (confirmed live)
- Outscraper: **0.4** — Full - consistent
- Google: **0.4** — Full - typed, versioned schema

**Freshness - NOT MEASURED (no signal collected)** (0.3 pts)
- Lobstr: **0.0** — not measurable - scored 0 for all, per plan rule
- Apify: **0.0** — not measurable - scored 0 for all, per plan rule
- Outscraper: **0.0** — not measurable - scored 0 for all, per plan rule
- Google: **0.0** — not measurable - scored 0 for all, per plan rule

### Cost

**Cost per 1K unique (ratio vs cheapest $0.64)** (0.8 pts)
- Lobstr: **0.085** — $6.05/1K measured credits x Growth rate
- Apify: **0.8** — $0.64/1K - billed $0.8932 via billing API
- Outscraper: **0.11** — $4.69/1K rate-card, base only
- Google: **0.19** — $2.70/1K rate-card (run billed $0 in free tier - scored on rate card for comparability, flagged)

**Billing fairness (anchor)** (0.3 pts)
- Lobstr: **0.3** — Full - pays per delivered row/email only
- Apify: **0.3** — Full - only verified-email leads charged, proven per-record via charged field
- Outscraper: **0.18** — Partial - per-record pricing, post-run billing reconciliation not captured
- Google: **0.18** — Partial - billed per request regardless of yield (18.7 avg places on 20 requested)

**Free tier / trial (anchor)** (0.2 pts)
- Lobstr: **0.12** — Partial - free plan capped at 30 rows/export
- Apify: **0.12** — Partial - $5/mo platform free credit
- Outscraper: **0.2** — Full - 500 free records/mo
- Google: **0.2** — Full - 1,000 Enterprise+Atmosphere requests/mo (~18.7K places)

**Pricing transparency (anchor)** (0.2 pts)
- Lobstr: **0.12** — Partial - credit rates public but row+email credit math needs docs digging; pricing page JS-only
- Apify: **0.12** — Partial - event prices published, but two spend-guards undocumented
- Outscraper: **0.2** — Full - flat $3/1K published
- Google: **0.2** — Full - published SKU table, computable to the cent

### Speed

**Median latency (only measurable for sync API; N/A batch = 0 per plan §9.2)** (0.5 pts)
- Lobstr: **0.0** — N/A - batch architecture
- Apify: **0.0** — N/A - batch architecture
- Outscraper: **0.0** — N/A - async request architecture
- Google: **0.5** — 1.54s median, measured on 60 requests

**Wall-clock, Run-1 batch (ratio vs fastest 46s; NOTE: scrapers do website-visit enrichment per row - architecture caveat per plan §5)** (0.5 pts)
- Lobstr: **0.013** — 1,711s (28m31s, squid run)
- Apify: **0.01** — 2,195s cumulative across 10 actor runs (parallelizable)
- Outscraper: **0.0** — not aggregated from raw evidence - unscored, flagged
- Google: **0.5** — ~46s for Run 1 (30 requests)

**p95 latency (N/A batch = 0)** (0.3 pts)
- Lobstr: **0.0** — N/A
- Apify: **0.0** — N/A
- Outscraper: **0.0** — N/A
- Google: **0.3** — 2.26s p95 measured

**Async/batch endpoint availability (anchor)** (0.2 pts)
- Lobstr: **0.2** — Full - squid submit/poll
- Apify: **0.2** — Full - actor run/dataset
- Outscraper: **0.2** — Full - async requests
- Google: **0.04** — Weak - synchronous only, no batch/export endpoint

### Scalability

**Rate limits & max concurrency (anchor)** (0.5 pts)
- Lobstr: **0.5** — Full - documented user-set concurrency, 20 slots
- Apify: **0.3** — Partial - internal parallelism, no user control, spend-guarded
- Outscraper: **0.3** — Partial - sequential 3-stage, no knob
- Google: **0.5** — Full - generous documented QPS quotas

**Stability/degradation at tested volume (anchor)** (0.4 pts)
- Lobstr: **0.4** — Full
- Apify: **0.08** — Weak - guard-driven early exits on 4/20 queries
- Outscraper: **0.4** — Full
- Google: **0.4** — Full

**Volume caps blocking production (anchor)** (0.3 pts)
- Lobstr: **0.3** — Full - 200/task, subdividable, no run cap (max_unique null)
- Apify: **0.06** — Weak - profitability breaker structurally under-delivers low-email verticals (restaurants: 264 vs 527 charged)
- Outscraper: **0.18** — Partial - balance-driven ceiling; single-query max unconfirmed
- Google: **0.06** — Weak - hard 60/query cap, hit on 10/10 restaurant queries

### Usability

**Input flexibility (anchor)** (0.3 pts)
- Lobstr: **0.3** — Full - coords+zoom, category match, rating/website/closed filters
- Apify: **0.18** — Partial - text queries + few booleans
- Outscraper: **0.3** — Full - query/region/limit/status/dedup
- Google: **0.18** — Partial - text query + location bias; no lead-oriented filters

**Endpoint/platform coverage (anchor)** (0.3 pts)
- Lobstr: **0.18** — Partial - single crawler data flow (other crawlers separate)
- Apify: **0.18** — Partial - this actor single-purpose (marketplace separate)
- Outscraper: **0.3** — Full - search, reviews, photos, enrichment endpoints
- Google: **0.3** — Full - text/nearby/details/photos/autocomplete

**Enrichment endpoints (anchor)** (0.2 pts)
- Lobstr: **0.12** — Partial - email extraction native, but verification dashboard-only (no API)
- Apify: **0.12** — Partial - inline verify only, no standalone enrichment
- Outscraper: **0.2** — Full - separate extraction + verification services
- Google: **0.02** — Weak - none

**Time-to-first-successful-request (anchor)** (0.3 pts)
- Lobstr: **0.18** — Partial - squid+tasks setup; zoom needed live tuning (12z failed, 14z passed)
- Apify: **0.3** — Full - console + one actor call; smoke succeeded in 10.3s
- Outscraper: **0.18** — Partial - not timed this project (flag: thin evidence)
- Google: **0.3** — Full - key to first data in minutes, single endpoint

**Documentation quality (anchor)** (0.3 pts)
- Lobstr: **0.18** — Partial - working page_size param undocumented; task URL format documented
- Apify: **0.18** — Partial - actor docs fine; guards & status masking undocumented
- Outscraper: **0.18** — Partial - docs exist but site unreachable from test env; schema verified via mirrors
- Google: **0.3** — Full - complete, versioned, searchable

**SDKs & examples (anchor)** (0.2 pts)
- Lobstr: **0.2** — Full - Python SDK, CLI, MCP
- Apify: **0.2** — Full - JS/Python clients
- Outscraper: **0.2** — Full - official Python client
- Google: **0.2** — Full - official client libraries

**Error clarity + support (anchor)** (0.2 pts)
- Lobstr: **0.2** — Full - precise live validation errors
- Apify: **0.04** — Weak - SUCCEEDED status masks truncation
- Outscraper: **0.12** — Partial - untested
- Google: **0.2** — Full - structured errors
