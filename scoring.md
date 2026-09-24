# Final Scoring — 7-criterion rubric (criteria.md §4, unchanged), core-requirement check applied

**Computed:** 2026-09-24 by `scripts/compute_final_scorecard.py` (core-field/enrichment fills and uniques recomputed live from `data/` on every run). Model: `IMPORTANT/criteria.md` Step 0 (core-requirement check, lead decision 2026-09-24) + Section 4 rubric + `prompt.txt` scoring rules. Supersedes `research/analysis/scorecard.md` totals (kept as sub-score provenance for the old framing) and all earlier gate/persona drafts.

**The user and the job:** extract all available Google Maps business listings from a search, reliably and affordably, with **name, address, phone, opening hours**. Enrichment (email/socials/images/verification) is bonus value only — it improves Data Quality/Coverage and is never a requirement (`prompt.txt`; demand evidence: `user-intent.md`, `research/analysis/who-why-research.md`).

**Disclosure:** Lobstr.io is the house product and owns this methodology. All raw evidence is in the public repo; every number traces to a repo file.

**Unscoreable, zeroed for all equally:** accuracy-vs-ground-truth (0.5) and freshness (0.3) — max attainable 9.2. Median/p95 latency (0.8) also scores 0 for all four ranked providers (all batch/async) — architecture-neutral this time.

## Ranked table

| Rank | Provider | Reliability /2.0 | Data Quality /2.0 | Cost /1.5 | Speed /1.5 | Scalability /1.2 | DevEx /1.0 | Input Flex /0.8 | **Total /10** |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | **Lobstr.io (house — disclosed)** | 1.98 | 1.20 | 0.70 | 0.31 | 1.20 | 0.76 | 0.60 | **6.75** |
| 2 | **HasData** | 1.57 | 0.90 | 1.20 | 0.62 | 1.00 | 0.72 | 0.68 | **6.69** |
| 3 | **Bright Data** | 1.88 | 1.00 | 0.51 | 0.70 | 0.88 | 0.36 | 0.38 | **5.71** |
| 4 | **Apify (themineworks/maps-leads)** | 0.98 | 0.87 | 1.34 | 0.28 | 0.44 | 0.72 | 0.48 | **5.11** |

**Ranking:** 1. Lobstr 6.75 · 2. HasData 6.69 · 3. BrightData 5.71 · 4. Apify 5.11

### Why each provider scored what it scored (criterion by criterion, prompt closing rule)

- **Lobstr.io (house — disclosed) — 6.75:** wins Reliability (85.1% delivery, zero silent truncation, clean errors), Data Quality (best core-4 fill 97.1% AND the enrichment reference point: 45.3% email + 56.8% socials), and Scalability (only user-controlled concurrency, no hidden caps). Loses ground on Cost (basic ~$2.66/1K — derived, 5x the cheapest) and Speed (28m31s Run 1, which includes per-row website visits for enrichment — caveat attached).
- **HasData — 6.69:** second on core fills (94.2%) and the cheapest measured-plan basic rate (~$0.74/1K base mode); fastest full-batch scraper among enrichment-capable tools (7m11s email-mode Run 1); enrichment bonus from 41.7% email fill. Held back by 73.7% delivery, run-to-run field wobble, and a 5-concurrency entry-plan cap.
- **Bright Data — 5.71:** near-perfect core fills (96.4%) and clean 87.1% delivery — the best pure-listings executor tested. Held back everywhere else by opacity and friction: cost is an unverifiable rate-card estimate (no billing API), docs unreachable, onboarding blocked initially, keyword-only inputs.
- **Apify (themineworks/maps-leads) — 5.11:** cheapest billed figure ($0.54/1K — but inseparable from its pay-per-verified-email model) and good DevEx (fastest time-to-first-request). Sunk by the trust findings, which hit this user's 'reliably' requirement hardest: 4/20 queries silently truncated by undocumented profit-guards while reporting SUCCEEDED, business_status broken on all records, and structural under-delivery on low-email verticals — a listings user pays in missing listings for an economics model built around emails they don't need.

### Sensitivity check on the #1 spot (house-product margin is thin — 0.06)

The Lobstr–HasData gap under the basic-workload cost framing is 6.75 vs 6.69. Recomputing the Cost criterion with **as-tested measured costs** instead (Lobstr $5.82/1K incl. enrichment → Cost 0.61; HasData $1.75/1K email mode → Cost 0.87) gives Lobstr 6.66 vs HasData 6.36 — the #1 spot is **stable under both consistent cost framings**; the near-tie is an artifact of the basic-mode framing, which favors HasData (its $0.74 is a rate-card figure, Lobstr's $2.66 a measured-credit derivation). Flagged per the disclosure: if any framing had flipped the ranking, this table would say so.

## Disqualified Providers (core-requirement failures — results and cost shown, never ranked)

| Provider | Core requirement failed | Its test results (shown, not scored) |
|---|---|---|
| **Google Places API (New)** | Required volume + usable results/storage: hard 60-results/query cap (measured at cap on 10/10 restaurant queries — 444 uniques vs 998–1,405 for scrapers on identical queries) and Maps Platform Terms §3.2.3 bars copying/saving business names & addresses — the user cannot extract *all* listings nor *keep* them | Best-engineered API tested: 60/60 HTTP 200, 1.54s median / 2.26s p95, best per-field fills (phone 95.4%, website 94.3%, hours 97.9%), 1,044 uniques, $0 billed in free tier / $2.30/1K rate-card. Compliant use: real-time in-app display. Evidence: `research/raw/google-places-api/`, knowledge.md |
| **Outscraper** | Affordable basic extraction: $3.69/1K unique measured-per-unique on base scrape alone ($4.80 for 1,300 uniques, rate-card $3/1K requested) — the most expensive basic extraction in the test vs $0.54–2.66 for ranked providers | Otherwise strong on this user's job: best core-4 fills measured (name 100% · address 100% · phone 94.7% · hours 95.3%, avg 97.5%), 96.8% delivery (on a budget-reduced 80/query batch, flagged), richest default listing schema. Evidence: `data/outscraper/` |

## Pending — not scored, no core-requirement failure on evidence

**ScrapingDog:** profile fits this user exactly (smoke: core fills 95–100%, ~1.5s median, projected $0.04–0.15/1K — cheapest in test by an order of magnitude) but the standard full-scale batch has not run: the supplied key is on the free 100-credit plan (verified live via `/account`, 2026-09-24). Enters the ranking only after running the same workload. Smoke also flagged a real risk to verify at scale: past ~75 uniques/query it serves fully-billed duplicate pages with no exhaustion signal (`data/scrapingdog/reports/smoke-findings.md`).

## Sub-criterion detail (every score's basis and evidence)

### Reliability

**Success rate on the core-workload benchmark (returned/requested, ratio vs best)** (1.0 pts)
- Lobstr: **0.98** — 3,403/4,000 = 85.1% — data/lobstr/raw/run1-final.json (1,594) + knowledge.md Run-2 pooled (1,809)
- HasData: **0.85** — 2,946/4,000 = 73.7% — data/hasdata/raw/run*/ per-job logs
- Apify: **0.78** — 2,730/4,000 = 68.2% — data/apify/raw/datasets/ row counts; 4/20 queries silently truncated (raw logs)
- BrightData: **1.0** — 1,741/2,000 = 87.1% — data/brightdata/raw/run*/snapshot.json (2x1,000 design)

**Empty/partial responses (anchor)** (0.4 pts)
- Lobstr: **0.4** — Full - none observed
- HasData: **0.24** — Partial - run1 rating/reviews filled 73% vs run2 100% (email-mode field wobble, measured)
- Apify: **0.08** — Weak - 4/20 queries silently truncated by profit guards; business_status broken on 100% of records
- BrightData: **0.4** — Full - 3 marked error rows in 1,741 (0.2%), no silent gaps

**Error handling quality (anchor)** (0.3 pts)
- Lobstr: **0.3** — Full - live 400 AttributeLimitExceeded precise, actionable
- HasData: **0.18** — Partial - excellent 422 validation, but status never reaches finished
- Apify: **0.06** — Weak - top-level SUCCEEDED masks truncation; only raw log reveals it
- BrightData: **0.18** — Partial - precise validation errors, but progress ready != snapshot downloadable

**Stability during test window (anchor)** (0.3 pts)
- Lobstr: **0.3** — Full - both runs completed, no degradation
- HasData: **0.3** — Full - 20/20 jobs completed
- Apify: **0.06** — Weak - profitability breaker cut queries mid-processing (Van Nuys 20/200; 3 more in run2)
- BrightData: **0.3** — Full - both snapshots completed normally

### Data Quality

**Field coverage: core fields FIRST (0.6), enrichment as BONUS (0.2) — prompt rules 1-2; ground truth not built, fills are a coverage proxy** (0.8 pts)
- Lobstr: **0.8** — core-4 (name/address/phone/hours) 97.1% (0.6 x ratio vs best 97.1) + enrichment bonus 51.0 avg email/social fill (0.2 x ratio vs best enricher Lobstr 51.0) — email 45.3%, socials 56.8%, computed live on 2,567 uniques
- HasData: **0.66** — core-4 (name/address/phone/hours) 94.2% (0.6 x ratio vs best 97.1) + enrichment bonus 20.9 avg email/social fill (0.2 x ratio vs best enricher Lobstr 51.0) — email 41.7%, socials 0.0%, computed live on 2,456 uniques
- Apify: **0.63** — core-4 (name/address/phone/hours) 92.8% (0.6 x ratio vs best 97.1) + enrichment bonus 14.1 avg email/social fill (0.2 x ratio vs best enricher Lobstr 51.0) — email 28.3%, socials 0.0%, computed live on 2,523 uniques
- BrightData: **0.6** — core-4 (name/address/phone/hours) 96.4% (0.6 x ratio vs best 97.1) + enrichment bonus 0.0 avg email/social fill (0.2 x ratio vs best enricher Lobstr 51.0) — email 0.0%, socials 0.0%, computed live on 1,739 uniques

**Data accuracy vs ground truth — NOT MEASURED (sample never built)** (0.5 pts)
- Lobstr: **0.0** — not measurable - 0 for all, flagged
- HasData: **0.0** — not measurable - 0 for all, flagged
- Apify: **0.0** — not measurable - 0 for all, flagged
- BrightData: **0.0** — not measurable - 0 for all, flagged

**Schema consistency (anchor)** (0.4 pts)
- Lobstr: **0.4** — Full - consistent 90+ field schema
- HasData: **0.24** — Partial - field set varies by run/options (measured run1 vs run2 wobble)
- Apify: **0.24** — Partial - business_status UNKNOWN universally (confirmed live)
- BrightData: **0.4** — Full - consistent 39-field schema across 1,738 records

**Freshness — NOT MEASURED (no signal collected)** (0.3 pts)
- Lobstr: **0.0** — not measurable - 0 for all, flagged
- HasData: **0.0** — not measurable - 0 for all, flagged
- Apify: **0.0** — not measurable - 0 for all, flagged
- BrightData: **0.0** — not measurable - 0 for all, flagged

### Cost

**Cost per 1K unique, BASIC extraction workload (ratio vs cheapest; enrichment priced separately)** (0.8 pts)
- Lobstr: **0.16** — $2.66/1K — derived from measured credits with the email-extraction credit share removed (knowledge.md: $6.05/1K as-tested incl. enrichment -> ~$2.66/1K without) — derived, flagged
- HasData: **0.58** — $0.74/1K — base mode 3 credits/row x Startup rate ($49/200K credits) — rate-card; measured email-mode run was $1.75/1K (scale-findings.md)
- Apify: **0.8** — $0.54/1K — billed via billing API on the full workload ($1.3656 / 2,523 uniques). FLAG: no basic-only price exists — this actor bills per VERIFIED-EMAIL lead, so basic extraction is inseparable from its enrichment economics
- BrightData: **0.29** — $1.50/1K — rate-card ESTIMATE ~$0.75-1.50/1K, upper bound used; NO billing visibility in the API — unverified

**Billing fairness (anchor)** (0.3 pts)
- Lobstr: **0.3** — Full - pays per delivered row/email only
- HasData: **0.3** — Full - per-row billing exact; email surcharge billed BELOW documented rate
- Apify: **0.3** — Full - only verified-email leads charged, proven per-record via charged field
- BrightData: **0.06** — Weak - no billing visibility through the API; fairness unverifiable

**Free tier / trial (anchor)** (0.2 pts)
- Lobstr: **0.12** — Partial - free plan capped at 30 rows/export
- HasData: **0.2** — Full - 1,000 credits/mo, no card
- Apify: **0.12** — Partial - $5/mo platform free credit
- BrightData: **0.12** — Partial - free credits reported third-party; activation + geo friction

**Pricing transparency (anchor)** (0.2 pts)
- Lobstr: **0.12** — Partial - credit rates public but row+email math needs docs digging
- HasData: **0.12** — Partial - rates published but observed billing deviates (favorably), undocumented
- Apify: **0.12** — Partial - event prices published, two spend-guards undocumented
- BrightData: **0.04** — Weak - conflicting third-party prices, own pricing unverifiable from env

### Speed

**Median latency per request (N/A for batch/async architectures = 0, all four)** (0.5 pts)
- Lobstr: **0.0** — N/A - batch/async architecture, no per-request timing
- HasData: **0.0** — N/A - batch/async architecture, no per-request timing
- Apify: **0.0** — N/A - batch/async architecture, no per-request timing
- BrightData: **0.0** — N/A - batch/async architecture, no per-request timing

**Wall-clock, Run-1 batch (ratio vs fastest; Lobstr/Apify/HasData timings include enrichment work — caveat attached, no unenriched timing exists to substitute)** (0.5 pts)
- Lobstr: **0.11** — 1,711s — data/lobstr/raw/run1-final.json (28m31s). Caveat: includes per-row website-visit email extraction (prompt rule 6)
- HasData: **0.42** — 431s — data/hasdata/raw/run1/run1-log.json (email mode — also doing enrichment work)
- Apify: **0.08** — 2,194s — cumulative runTimeSecs across 10 actor runs (knowledge.md; parallelizable). Caveat: includes email extraction + DNS/MX verification
- BrightData: **0.5** — 365s — data/brightdata/raw/run*/ progress logs (~6 min/run, no enrichment work)

**p95 latency (N/A batch = 0)** (0.3 pts)
- Lobstr: **0.0** — N/A
- HasData: **0.0** — N/A
- Apify: **0.0** — N/A
- BrightData: **0.0** — N/A

**Async/batch endpoint availability (anchor)** (0.2 pts)
- Lobstr: **0.2** — Full - squid submit/poll
- HasData: **0.2** — Full - async jobs + webhooks
- Apify: **0.2** — Full - actor run/dataset
- BrightData: **0.2** — Full - trigger/progress/snapshot + webhooks

### Scalability

**Rate limits & max concurrency (anchor)** (0.5 pts)
- Lobstr: **0.5** — Full - documented user-set concurrency, 20 slots
- HasData: **0.3** — Partial - 5 concurrent on Startup (429s measured), plan-scaled
- Apify: **0.3** — Partial - internal parallelism, no user control, spend-guarded
- BrightData: **0.3** — Partial - batch inputs parallelized internally, no user control

**Degradation at tested volume (anchor)** (0.4 pts)
- Lobstr: **0.4** — Full
- HasData: **0.4** — Full - no degradation across 20 jobs
- Apify: **0.08** — Weak - guard-driven early exits on 4/20 queries (counted once here at reduced weight; primary hit taken in Reliability - prompt rule 5, no double-counting)
- BrightData: **0.4** — Full

**Volume caps blocking production (anchor)** (0.3 pts)
- Lobstr: **0.3** — Full - 200/task = Google's own ceiling, subdividable, no run cap
- HasData: **0.3** — Full - user-set limits honored, no hidden ceilings observed
- Apify: **0.06** — Weak - profitability breaker structurally under-delivers low-email verticals (restaurants 264 vs 527 charged)
- BrightData: **0.18** — Partial - tested at 100/input by design; higher per-input volumes unprobed

### DevEx

**Time-to-first-successful-request (anchor)** (0.3 pts)
- Lobstr: **0.18** — Partial - squid+tasks setup; zoom needed live tuning
- HasData: **0.3** — Full - first job in minutes; 422 errors self-document schema
- Apify: **0.3** — Full - console + one actor call; smoke succeeded in 10.3s
- BrightData: **0.06** — Weak - first key blocked, activation + geo friction, DNS-blocked domains

**Docs quality (anchor)** (0.3 pts)
- Lobstr: **0.18** — Partial - working page_size param undocumented
- HasData: **0.18** — Partial - good docs; status semantics wrong
- Apify: **0.18** — Partial - actor docs fine; guards & status masking undocumented
- BrightData: **0.06** — Weak - docs unreachable from test env; schema discovered by probing

**SDKs & examples (anchor)** (0.2 pts)
- Lobstr: **0.2** — Full - Python SDK, CLI, MCP
- HasData: **0.12** — Partial - clean REST; official SDK not verified
- Apify: **0.2** — Full - JS/Python clients
- BrightData: **0.12** — Partial - SDKs exist; not verified from env

**Error clarity + support (anchor)** (0.2 pts)
- Lobstr: **0.2** — Full - precise live validation errors
- HasData: **0.12** — Partial - great validation errors, misleading status field
- Apify: **0.04** — Weak - SUCCEEDED masks truncation
- BrightData: **0.12** — Partial - good errors; ready/building mismatch

### Input Flexibility

**Accepted input types (anchor)** (0.3 pts)
- Lobstr: **0.3** — Full - coords+zoom, category match, rating/website/closed filters
- HasData: **0.18** — Partial - keywords+locations+limit+extractEmails; no coords/filters
- Apify: **0.18** — Partial - text queries + few booleans
- BrightData: **0.06** — Weak - country+keyword discovery only

**Endpoint breadth (anchor)** (0.3 pts)
- Lobstr: **0.18** — Partial - single crawler data flow
- HasData: **0.3** — Full - scraper jobs + real-time SERP APIs + reviews/photos
- Apify: **0.18** — Partial - this actor single-purpose
- BrightData: **0.3** — Full - large scraper/dataset catalog

**Enrichment endpoints (BONUS capability, per prompt rule 2)** (0.2 pts)
- Lobstr: **0.12** — Partial - email extraction native; verification dashboard-only
- HasData: **0.2** — Full - native extractEmails + per-field enrichments (LinkedIn/socials)
- Apify: **0.12** — Partial - inline verify only, no standalone enrichment
- BrightData: **0.02** — Weak - none
