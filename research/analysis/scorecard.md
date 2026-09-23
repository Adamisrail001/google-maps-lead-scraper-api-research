# Benchmark Scorecard — 10-Point Rubric (testing-plan §2, method §13)

**Computed:** 2026-09-23 by `scripts/compute_scorecard.py` (rerun it to regenerate; every sub-score carries its basis + evidence).

> **Disqualification note:** Google Places API (New) is scored below for reference but DISQUALIFIED from the rankings — its own customer agreement (Maps Platform Terms §3.2.3) prohibits storing/exporting the data (the article's deliverable), on top of the measured 60/query ceiling and absent contact fields. Full grounds: knowledge.md eliminations table.
> **Comparability note:** HasData and Bright Data scored from their 2026-09-23 stage-2 runs (HasData: benchmark-standard 200/sub-area; Bright Data: 2x1,000 brief design, 100/input) - identical query set, different volume ceilings, flagged where it matters. Bright Data cost is a rate-card ESTIMATE (no billing visibility).
> **Unscoreable on existing evidence, zeroed for ALL providers equally (0.8 pts):** Accuracy-vs-ground-truth (0.5 — sample never built, testing-plan §10 open item) and Freshness (0.3 — no signal collected). Max attainable = 9.2.
> **Rubric artifacts to keep in mind:** wall-clock ratio scoring severely penalizes batch scrapers that do per-row website-visit enrichment vs a sync API returning 20 records/call (§5 reporting rule caveat applies); Outscraper scored on its reduced budget scope (base scrape, 80/query); Google's cost scored on rate-card since its run billed $0 in free tier.
> **Disclosure:** Lobstr.io is the house product. Per criteria.md writer rules, the aggregate winner is whoever scores highest — no predetermined outcome.

## Criterion scores

| Criterion | Max | Lobstr | Apify | Outscraper | Google | HasData | BrightData |
|---|---:|---:|---:|---:|---:|---:|---:|
| Reliability | 2.0 | 1.88 | 0.91 | 1.88 | 1.96 | 1.48 | 1.78 |
| Data Quality | 2.0 | 1.20 | 0.87 | 1.08 | 1.13 | 0.98 | 1.13 |
| Cost | 1.5 | 0.61 | 1.34 | 0.70 | 0.77 | 0.87 | 0.51 |
| Speed | 1.5 | 0.21 | 0.21 | 0.20 | 1.34 | 0.26 | 0.26 |
| Scalability | 1.2 | 1.20 | 0.44 | 0.88 | 0.96 | 1.00 | 0.88 |
| Usability | 1.8 | 1.36 | 1.20 | 1.48 | 1.50 | 1.40 | 0.74 |
| **TOTAL /10** | 10.0 | **6.46** | **4.97** | **6.22** (ref — DQ) | **7.66** (ref — DQ) | **5.99** | **5.30** |

**Ranking (disqualified providers excluded):** 1. Lobstr 6.46 · 2. HasData 5.99 · 3. BrightData 5.30 · 4. Apify 4.97

**Google: DISQUALIFIED (E5): customer agreement §3.2.3 bars storing/exporting business names/addresses; 60/query ceiling (measured 10/10 at cap); zero contact fields. Scored for reference only — see knowledge.md eliminations.**

**Outscraper: DISQUALIFIED on cost/testability (2026-09-23): the full email-enriched workload every ranked provider ran projects to $7–11/1K uniques by its own rate card (up to $9/1K records across 3 stages) — most expensive in test, ~4–6× HasData — so the full-scope run was declined and its email metrics remain untested. Its 6.22 rests on a reduced-scope run (80/query, base-only, easiest workload) and is kept for reference only.**

## Sub-criterion detail

### Reliability

**Success rate, BOTH runs (returned/requested, ratio vs best 96.8%)** (1.0 pts)
- Lobstr: **0.88** — (1,594+1,809)/4,000 = 85.1% (runs e57af71d + run2 pooled)
- Apify: **0.71** — (1,608+1,122)/4,000 = 68.3% - run2 restaurants collapsed to 56.1% via profit-breaker
- Outscraper: **1.0** — (748+800)/1,600 = 96.8%
- Google: **0.96** — 1,120/1,200 page-slots = 93.3% (run-log.json)
- HasData: **0.76** — 2,946/4,000 = 73.7% (scale runs, per-job logs)
- BrightData: **0.9** — 1,741/2,000 = 87.1% (2x1,000 design, snapshots)

**Empty/partial responses (anchor)** (0.4 pts)
- Lobstr: **0.4** — Full - none observed
- Apify: **0.08** — Weak - 4/20 queries silently truncated by profit guards; business_status broken on 100% of records
- Outscraper: **0.4** — Full - none observed
- Google: **0.4** — Full - none; sub-60 pages traced to data scarcity, documented
- HasData: **0.24** — Partial - run1 rating/reviews filled only 73% vs run2 100% (email-mode field wobble, measured)
- BrightData: **0.4** — Full - 3 marked error rows in 1,741 (0.2%), no silent gaps

**Error handling quality (anchor)** (0.3 pts)
- Lobstr: **0.3** — Full - live 400 AttributeLimitExceeded was precise, actionable
- Apify: **0.06** — Weak - top-level SUCCEEDED masks truncation; only raw log reveals it
- Outscraper: **0.18** — Partial - no errors encountered, quality unassessed (flag: thin evidence)
- Google: **0.3** — Full - structured google.rpc errors, clean retry semantics
- HasData: **0.18** — Partial - excellent 422 validation, but status never reaches finished (misleading)
- BrightData: **0.18** — Partial - precise validation errors, but progress ready != snapshot downloadable

**Stability during window (anchor)** (0.3 pts)
- Lobstr: **0.3** — Full - both runs completed, no degradation
- Apify: **0.06** — Weak - profitability breaker cut queries mid-processing (Van Nuys 20/200; 3 more in run2)
- Outscraper: **0.3** — Full - completed normally
- Google: **0.3** — Full - 60/60 HTTP 200, latency stable (p95 2.26s)
- HasData: **0.3** — Full - 20/20 jobs completed, no degradation
- BrightData: **0.3** — Full - both snapshots completed normally

### Data Quality

**Field coverage, 10 lead fields, BOTH-run measured fill-rate proxy (ratio vs best 85.8) - GROUND TRUTH NOT BUILT, proxy flagged** (0.8 pts)
- Lobstr: **0.8** — 85.8 (core-8 95.7 weighted both runs + email 45.6 + socials ~47)
- Apify: **0.63** — 67.7 (core-8 81.1 + email 28.3 verified + 0; no review-count field)
- Outscraper: **0.68** — 73.0 (core-8 91.2, category weak 48-55%; no email/socials in base scope)
- Google: **0.73** — 78.2 (core-8 97.75 - best core fill - + email 0 + socials 0, fields absent from API)
- HasData: **0.74** — 79.2 (core-8 93.8 + email 42 + socials 0 - separate enrichments untested)
- BrightData: **0.73** — 77.8 (core-8 97.2, second-best core fill + email 0 + socials 0, fields absent)

**Accuracy vs ground truth - NOT MEASURED (sample never built)** (0.5 pts)
- Lobstr: **0.0** — not measurable - scored 0 for all, per plan rule
- Apify: **0.0** — not measurable - scored 0 for all, per plan rule
- Outscraper: **0.0** — not measurable - scored 0 for all, per plan rule
- Google: **0.0** — not measurable - scored 0 for all, per plan rule
- HasData: **0.0** — not measurable - scored 0 for all, per plan rule
- BrightData: **0.0** — not measurable - scored 0 for all, per plan rule

**Schema consistency (anchor)** (0.4 pts)
- Lobstr: **0.4** — Full - consistent 90+ field schema
- Apify: **0.24** — Partial - business_status returns UNKNOWN universally (confirmed live)
- Outscraper: **0.4** — Full - consistent
- Google: **0.4** — Full - typed, versioned schema
- HasData: **0.24** — Partial - field set varies by run/options (measured run1 vs run2 wobble)
- BrightData: **0.4** — Full - consistent 39-field schema across 1,738 records

**Freshness - NOT MEASURED (no signal collected)** (0.3 pts)
- Lobstr: **0.0** — not measurable - scored 0 for all, per plan rule
- Apify: **0.0** — not measurable - scored 0 for all, per plan rule
- Outscraper: **0.0** — not measurable - scored 0 for all, per plan rule
- Google: **0.0** — not measurable - scored 0 for all, per plan rule
- HasData: **0.0** — not measurable - scored 0 for all, per plan rule
- BrightData: **0.0** — not measurable - scored 0 for all, per plan rule

### Cost

**Cost per 1K unique, BOTH runs (ratio vs cheapest $0.54)** (0.8 pts)
- Lobstr: **0.07** — $5.82/1K - 8,968 credits measured (3,626 + 5,342, runs e57af71d + 6b7150f5) x Growth rate / 2,567 uniques
- Apify: **0.8** — $0.54/1K - billed $1.3656 total via billing API / 2,523 uniques
- Outscraper: **0.12** — $3.69/1K rate-card - $4.80 for 1,600 requested / 1,300 uniques, base only
- Google: **0.19** — $2.30/1K rate-card - $2.40 / 1,044 uniques (billed $0 in free tier - scored on rate card for comparability, flagged)
- HasData: **0.25** — $1.75/1K measured (17,518 credits x Startup rate / 2,456 uniques)
- BrightData: **0.29** — ~$1.50/1K RATE-CARD ESTIMATE - no billing field in API, unverified, flagged

**Billing fairness (anchor)** (0.3 pts)
- Lobstr: **0.3** — Full - pays per delivered row/email only
- Apify: **0.3** — Full - only verified-email leads charged, proven per-record via charged field
- Outscraper: **0.18** — Partial - per-record pricing, post-run billing reconciliation not captured
- Google: **0.18** — Partial - billed per request regardless of yield (18.7 avg places on 20 requested)
- HasData: **0.3** — Full - per-row billing exact; email surcharge billed BELOW documented rate (158 vs 200)
- BrightData: **0.06** — Weak - no billing visibility through the API at all; fairness unverifiable

**Free tier / trial (anchor)** (0.2 pts)
- Lobstr: **0.12** — Partial - free plan capped at 30 rows/export
- Apify: **0.12** — Partial - $5/mo platform free credit
- Outscraper: **0.2** — Full - 500 free records/mo
- Google: **0.2** — Full - 1,000 Enterprise+Atmosphere requests/mo (~18.7K places)
- HasData: **0.2** — Full - 1,000 credits/mo, no card (covered the whole smoke)
- BrightData: **0.12** — Partial - free monthly credits reported third-party; account required activation + geo friction

**Pricing transparency (anchor)** (0.2 pts)
- Lobstr: **0.12** — Partial - credit rates public but row+email credit math needs docs digging; pricing page JS-only
- Apify: **0.12** — Partial - event prices published, but two spend-guards undocumented
- Outscraper: **0.2** — Full - flat $3/1K published
- Google: **0.2** — Full - published SKU table, computable to the cent
- HasData: **0.12** — Partial - credit rates published but observed billing deviates (favorably) undocumented
- BrightData: **0.04** — Weak - conflicting third-party prices ($0.75-1.50/1K), own pricing unverifiable from env

### Speed

**Median latency (only measurable for sync API; N/A batch = 0 per plan §9.2)** (0.5 pts)
- Lobstr: **0.0** — N/A - batch architecture
- Apify: **0.0** — N/A - batch architecture
- Outscraper: **0.0** — N/A - async request architecture
- Google: **0.5** — 1.54s median, measured on 60 requests
- HasData: **0.0** — N/A - async jobs
- BrightData: **0.0** — N/A - async snapshots

**Wall-clock, Run-1 batch (ratio vs fastest 46s; NOTE: scrapers do website-visit enrichment per row - architecture caveat per plan §5)** (0.5 pts)
- Lobstr: **0.013** — 1,711s (28m31s, squid run)
- Apify: **0.01** — 2,195s cumulative across 10 actor runs (parallelizable)
- Outscraper: **0.0** — not aggregated from raw evidence - unscored, flagged
- Google: **0.5** — ~46s for Run 1 (30 requests)
- HasData: **0.06** — ~367s avg per run (logs; fastest scraper tested)
- BrightData: **0.06** — ~365s avg per run (progress logs)

**p95 latency (N/A batch = 0)** (0.3 pts)
- Lobstr: **0.0** — N/A
- Apify: **0.0** — N/A
- Outscraper: **0.0** — N/A
- Google: **0.3** — 2.26s p95 measured
- HasData: **0.0** — N/A
- BrightData: **0.0** — N/A

**Async/batch endpoint availability (anchor)** (0.2 pts)
- Lobstr: **0.2** — Full - squid submit/poll
- Apify: **0.2** — Full - actor run/dataset
- Outscraper: **0.2** — Full - async requests
- Google: **0.04** — Weak - synchronous only, no batch/export endpoint
- HasData: **0.2** — Full - async jobs + webhooks + paginated results
- BrightData: **0.2** — Full - trigger/progress/snapshot + webhook delivery

### Scalability

**Rate limits & max concurrency (anchor)** (0.5 pts)
- Lobstr: **0.5** — Full - documented user-set concurrency, 20 slots
- Apify: **0.3** — Partial - internal parallelism, no user control, spend-guarded
- Outscraper: **0.3** — Partial - sequential 3-stage, no knob
- Google: **0.5** — Full - generous documented QPS quotas
- HasData: **0.3** — Partial - 5 concurrent on Startup (429s measured), plan-scaled
- BrightData: **0.3** — Partial - batch inputs parallelized internally, no user control

**Stability/degradation at tested volume (anchor)** (0.4 pts)
- Lobstr: **0.4** — Full
- Apify: **0.08** — Weak - guard-driven early exits on 4/20 queries
- Outscraper: **0.4** — Full
- Google: **0.4** — Full
- HasData: **0.4** — Full - no degradation across 20 jobs
- BrightData: **0.4** — Full

**Volume caps blocking production (anchor)** (0.3 pts)
- Lobstr: **0.3** — Full - 200/task, subdividable, no run cap (max_unique null)
- Apify: **0.06** — Weak - profitability breaker structurally under-delivers low-email verticals (restaurants: 264 vs 527 charged)
- Outscraper: **0.18** — Partial - balance-driven ceiling; single-query max unconfirmed
- Google: **0.06** — Weak - hard 60/query cap, hit on 10/10 restaurant queries
- HasData: **0.3** — Full - user-set limits honored, no hidden ceilings observed
- BrightData: **0.18** — Partial - tested at 100/input by design; higher per-input volumes unprobed

### Usability

**Input flexibility (anchor)** (0.3 pts)
- Lobstr: **0.3** — Full - coords+zoom, category match, rating/website/closed filters
- Apify: **0.18** — Partial - text queries + few booleans
- Outscraper: **0.3** — Full - query/region/limit/status/dedup
- Google: **0.18** — Partial - text query + location bias; no lead-oriented filters
- HasData: **0.18** — Partial - keywords+locations+limit+extractEmails; no coords/filters
- BrightData: **0.06** — Weak - country+keyword discovery only; no text-query or location params

**Endpoint/platform coverage (anchor)** (0.3 pts)
- Lobstr: **0.18** — Partial - single crawler data flow (other crawlers separate)
- Apify: **0.18** — Partial - this actor single-purpose (marketplace separate)
- Outscraper: **0.3** — Full - search, reviews, photos, enrichment endpoints
- Google: **0.3** — Full - text/nearby/details/photos/autocomplete
- HasData: **0.3** — Full - scraper jobs + real-time SERP APIs + reviews/photos
- BrightData: **0.3** — Full - large scraper/dataset catalog (1,763 datasets listed)

**Enrichment endpoints (anchor)** (0.2 pts)
- Lobstr: **0.12** — Partial - email extraction native, but verification dashboard-only (no API)
- Apify: **0.12** — Partial - inline verify only, no standalone enrichment
- Outscraper: **0.2** — Full - separate extraction + verification services
- Google: **0.02** — Weak - none
- HasData: **0.2** — Full - native extractEmails + per-field enrichments (LinkedIn/socials, 5 cr)
- BrightData: **0.02** — Weak - none

**Time-to-first-successful-request (anchor)** (0.3 pts)
- Lobstr: **0.18** — Partial - squid+tasks setup; zoom needed live tuning (12z failed, 14z passed)
- Apify: **0.3** — Full - console + one actor call; smoke succeeded in 10.3s
- Outscraper: **0.18** — Partial - not timed this project (flag: thin evidence)
- Google: **0.3** — Full - key to first data in minutes, single endpoint
- HasData: **0.3** — Full - first job in minutes; 422 errors self-document the schema
- BrightData: **0.06** — Weak - first key blocked (Customer is not active), activation + geo friction, DNS-blocked domains

**Documentation quality (anchor)** (0.3 pts)
- Lobstr: **0.18** — Partial - working page_size param undocumented; task URL format documented
- Apify: **0.18** — Partial - actor docs fine; guards & status masking undocumented
- Outscraper: **0.18** — Partial - docs exist but site unreachable from test env; schema verified via mirrors
- Google: **0.3** — Full - complete, versioned, searchable
- HasData: **0.18** — Partial - good docs; status semantics wrong; billing discount undocumented
- BrightData: **0.06** — Weak - docs unreachable from test env; schema discovered by probing

**SDKs & examples (anchor)** (0.2 pts)
- Lobstr: **0.2** — Full - Python SDK, CLI, MCP
- Apify: **0.2** — Full - JS/Python clients
- Outscraper: **0.2** — Full - official Python client
- Google: **0.2** — Full - official client libraries
- HasData: **0.12** — Partial - clean REST + examples; official SDK not verified
- BrightData: **0.12** — Partial - SDKs exist per ecosystem; not verified from this env

**Error clarity + support (anchor)** (0.2 pts)
- Lobstr: **0.2** — Full - precise live validation errors
- Apify: **0.04** — Weak - SUCCEEDED status masks truncation
- Outscraper: **0.12** — Partial - untested
- Google: **0.2** — Full - structured errors
- HasData: **0.12** — Partial - great validation errors, misleading status field
- BrightData: **0.12** — Partial - good errors; ready/building mismatch
