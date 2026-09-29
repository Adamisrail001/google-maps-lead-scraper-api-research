# Final Scoring — 7-criterion rubric (methodology §4, unchanged), core-requirement check applied

**Computed:** 2026-09-28 (cost basis revised to lobstr.io's current Team plan rate; first computed 2026-09-24) by `scripts/compute_final_scorecard.py` (core-field/enrichment fills and uniques recomputed live from `data/` on every run). Model: Step 0 core-requirement check (lead decision 2026-09-24) + the Section 4 rubric. Supersedes all earlier gate/persona drafts.

**The user and the job:** extract all available Google Maps business listings from a search, reliably and affordably, with **name, address, phone, opening hours**. Enrichment (email/socials/images/verification) is bonus value only — it improves Data Quality/Coverage and is never a requirement (demand evidence: a 31-probe user-intent study and an independent 12-voice confirmation sweep, run 2026-09-21/23).

**Disclosure:** lobstr.io runs this benchmark and is one of the evaluated providers. All raw evidence is in the public repo; every number traces to a repo file.

**Ground truth built 2026-09-24** (24-business live sample via Places API Details, `ground-truth/`; manual browser spot-check pending on 3 flagged businesses) — accuracy (0.5) and freshness (0.3) are now MEASURED for all four providers. The only sub-criteria zeroed for all remain median/p95 latency (0.8, N/A for batch/async architectures) — **effective ceiling 9.2/10**; compare scores against 9.2, not 10.

## Ranked table

| Rank | Provider | Reliability /2.0 | Data Quality /2.0 | Cost /1.5 | Speed /1.5 | Scalability /1.2 | DevEx /1.0 | Input Flex /0.8 | **Total /10** |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | **lobstr.io (house — disclosed)** | 1.98 | 2.00 | 1.34 | 0.70 | 1.20 | 0.76 | 0.60 | **8.58** |
| 2 | **HasData** | 1.57 | 1.69 | 1.03 | 0.35 | 1.00 | 0.72 | 0.68 | **7.04** |
| 3 | **Bright Data** | 1.88 | 1.79 | 0.49 | 0.26 | 0.88 | 0.36 | 0.38 | **6.04** |
| 4 | **Apify (themineworks/maps-leads)** | 0.98 | 1.66 | 1.28 | 0.21 | 0.44 | 0.72 | 0.48 | **5.77** |

**Ranking:** 1. lobstr.io 8.58 · 2. HasData 7.04 · 3. Bright Data 6.04 · 4. Apify 5.77

### Why each provider scored what it scored (criterion by criterion, prompt closing rule)

- **lobstr.io (house — disclosed) — 8.58:** wins Reliability (85.1% delivery, zero silent truncation, clean errors), Data Quality with a perfect 2.0/2.0 (best core-4 fill 97.1%, the enrichment reference point — 45.3% email + 56.8% socials — plus 100% ground-truth accuracy — all 180 checkable data points — and 100% freshness), and Scalability (only user-controlled concurrency, no hidden caps). Also the fastest on the basic workload — 45.3s for the full Run-1 batch with enrichment off (measured 2026-09-24), revealing that ~97% of its 28m31s as-tested wall-clock was enrichment work. At the Team plan rate ($500/mo, 1M credits) its measured basic cost is $0.50/1K — the cheapest in the ranked set ($1.67/1K at the legacy Growth rate the test account is on; plan-tier caveat in the sensitivity check below).
- **HasData — 7.04:** second on core fills (94.2%), $0.98/1K measured basic cost at its entry Startup plan ($0.28/1K at its own volume tier — see sensitivity check), and 146.6s measured basic wall-clock (2nd fastest); enrichment bonus from 41.7% email fill; 98.9% ground-truth accuracy and 100% freshness. Held back by 73.7% delivery, run-to-run field wobble, and a 5-concurrency entry-plan cap.
- **Bright Data — 6.04:** near-perfect core fills (96.4%) and clean 87.1% delivery — but the 2026-09-24 basic-mode twins revealed it is NOT the fastest bare-listings tool (365s vs Lobstr 45.3s / HasData 146.6s on the same work). Held back everywhere else by opacity and friction: cost is an unverifiable rate-card estimate (no billing API), docs unreachable, onboarding blocked initially, keyword-only inputs.
- **Apify (themineworks/maps-leads) — 5.77:** cheapest BILLED figure ($0.54/1K via its billing API — the strongest cost-evidence tier in the test, though second to Lobstr's Team-rate $0.50 measured-credits figure; inseparable from its pay-per-verified-email model) and good DevEx (fastest time-to-first-request). Sunk by the trust findings, which hit this user's 'reliably' requirement hardest: 4/20 queries silently truncated by undocumented profit-guards while reporting SUCCEEDED, business_status broken on all records, and structural under-delivery on low-email verticals — a listings user pays in missing listings for an economics model built around emails they don't need.

### Sensitivity checks on the #1 spot (cost-basis framings — read before questioning the Team-rate basis)

The table prices lobstr.io's measured credits at its **Team plan** ($500/mo, 1M credits — current lineup verified on lobstr.io/pricing 2026-09-28; basis revised 2026-09-28, previously the legacy $50/30K Growth rate). Because plan choice moves the $ figure, the ranking was recomputed under every framing:

1. **Volume-tier symmetry** (both top providers at their own volume tier): HasData's Growth plan ($208/mo, 3M credits) prices its measured basic twin at **$0.28/1K** (5,121 credits = $0.36 / 1,276 uniques) — HasData becomes the cheapest and takes the full cost sub. Result: Lobstr 8.23 vs HasData 7.43 — **stable**.
2. **Legacy/entry-plan framing** (the pre-2026-09-28 basis: Lobstr at Growth $1.67/1K vs HasData at Startup $0.98/1K, both measured 2026-09-24 enrichment-off twins): Lobstr 8.04 vs HasData 7.07 — **stable**.
3. **As-tested enriched spend** (Lobstr $1.75/1K at Team rate — 8,968 credits / 2,567 uniques; HasData $1.75/1K email-mode): Cost 0.79 vs 0.87, totals Lobstr 8.03 vs HasData 6.88 — **stable**.

The #1 spot holds under all framings. The Speed criterion likewise uses like-for-like basic timings for the top three (Lobstr 45.3s / HasData 146.6s / Bright Data 365s); Apify has no separable basic mode, flagged. Per the disclosure: if any framing had flipped the ranking, this table would say so.

## Disqualified Providers (core-requirement failures — results and cost shown, never ranked)

| Provider | Core requirement failed | Its test results (shown, not scored) |
|---|---|---|
| **Google Places API (New)** | Required volume + usable results/storage: hard 60-results/query cap (measured at cap on 10/10 restaurant queries — 444 uniques vs 998–1,405 for scrapers on identical queries) and Maps Platform Terms §3.2.3 bars copying/saving business names & addresses — the user cannot extract *all* listings nor *keep* them | Best-engineered API tested: 60/60 HTTP 200, 1.54s median / 2.26s p95, best per-field fills (phone 95.4%, website 94.3%, hours 97.9%), 1,044 uniques, $0 billed in free tier / $2.30/1K rate-card. Compliant use: real-time in-app display. Evidence: `data/google-places-api/raw/`, knowledge.md |
| **Outscraper** | Affordable basic extraction: $3.69/1K unique measured-per-unique on base scrape alone ($4.80 for 1,300 uniques, rate-card $3/1K requested) — the most expensive basic extraction in the test vs $0.50–0.98 measured (Bright Data ~$1.50 rate-card) for ranked providers | Otherwise strong on this user's job: best core-4 fills measured (name 100% · address 100% · phone 94.7% · hours 95.3%, avg 97.5%), 96.8% delivery (on a budget-reduced 80/query batch, flagged), richest default listing schema. Evidence: `data/outscraper/` |
| **ScrapingDog** | Required volume: full-scale run on the paid Lite plan (2026-09-24, same 2×10×200 workload) measured a hard **~49-unique/query depth ceiling** (range 39–57 vs 200 requested) — *below the 60/query cap that disqualified Google* — where the four ranked scrapers found 120–200 on identical queries; 862 uniques total vs 1,739–2,567. Compounding: past the ceiling it keeps serving HTTP-200, **fully-billed, 100%-duplicate pages with no exhaustion signal** — 44 such pages billed in this benchmark (22% of spend bought pure duplicates) | Everything else was excellent: **$0.23/1K unique measured** (cheapest in test by 2×+), core-4 fill 97.4% (best measured), ~1.0s median latency, ~2 min/run. A strong shallow-lookup tool (top ~40–50 results per area), not a full-extraction tool. Both pagination modes tested — `start` offsets barely paginate (~22 uniques/query), `ll`+`page` used for the benchmark. Evidence: `data/scrapingdog/raw/run*-llpage/`, `data/scrapingdog/reports/scale-findings.md` |

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
- Lobstr: **0.8** — core-4 (name/address/phone/hours) 97.1% (0.6 x ratio vs best 97.1) + enrichment bonus 51.0 avg email/social fill (0.2 x ratio vs best enricher lobstr.io 51.0) — email 45.3%, socials 56.8%, computed live on 2,567 uniques
- HasData: **0.66** — core-4 (name/address/phone/hours) 94.2% (0.6 x ratio vs best 97.1) + enrichment bonus 20.9 avg email/social fill (0.2 x ratio vs best enricher lobstr.io 51.0) — email 41.7%, socials 0.0%, computed live on 2,456 uniques
- Apify: **0.63** — core-4 (name/address/phone/hours) 92.8% (0.6 x ratio vs best 97.1) + enrichment bonus 14.1 avg email/social fill (0.2 x ratio vs best enricher lobstr.io 51.0) — email 28.3%, socials 0.0%, computed live on 2,523 uniques
- BrightData: **0.6** — core-4 (name/address/phone/hours) 96.4% (0.6 x ratio vs best 97.1) + enrichment bonus 0.0 avg email/social fill (0.2 x ratio vs best enricher lobstr.io 51.0) — email 0.0%, socials 0.0%, computed live on 1,739 uniques

**Data accuracy vs ground truth (24-business live sample; a data point = one business x field pair, graded only where both truth and provider have a value; ratio vs best)** (0.5 pts)
- Lobstr: **0.5** — 100.0% (180/180 checkable data points (business × field pairs)) — data/lobstr/analysis/ground-truth-match.json
- HasData: **0.49** — 98.9% (178/180 checkable data points (business × field pairs)) — data/hasdata/analysis/ground-truth-match.json
- Apify: **0.49** — 98.7% (155/157 checkable data points (business × field pairs)) — data/apify/analysis/ground-truth-match.json
- BrightData: **0.49** — 98.3% (177/180 checkable data points (business × field pairs)) — data/brightdata/analysis/ground-truth-match.json

**Schema consistency (anchor)** (0.4 pts)
- Lobstr: **0.4** — Full - consistent 90+ field schema
- HasData: **0.24** — Partial - field set varies by run/options (measured run1 vs run2 wobble)
- Apify: **0.24** — Partial - business_status UNKNOWN universally (confirmed live)
- BrightData: **0.4** — Full - consistent 39-field schema across 1,738 records

**Freshness (volatile fields — rating/review count — vs same-day live values on the 24-business sample, ratio vs best)** (0.3 pts)
- Lobstr: **0.3** — 100.0% fresh (23/23 records; basis: rating + review count)
- HasData: **0.3** — 100.0% fresh (23/23 records; basis: rating + review count)
- Apify: **0.3** — 100.0% fresh (23/23 records; basis: rating only (no review-count field))
- BrightData: **0.3** — 100.0% fresh (23/23 records; basis: rating + review count)

### Cost

**Cost per 1K unique, BASIC extraction workload (ratio vs cheapest; enrichment priced separately)** (0.8 pts)
- Lobstr: **0.8** — $0.50/1K — MEASURED 2026-09-24: enrichment-off run of the same Run-1 workload billed 926 credits for 926 uniques (exactly 1 credit/unique) x Team plan rate $500/mo / 1M credits = $0.0005/credit (current plan lineup verified on lobstr.io/pricing 2026-09-28) — data/lobstr/raw/speed-basic/speed-basic-log.json. Same credits at the legacy $50/30K Growth rate the test account is on = $1.67/1K (basis until 2026-09-28); supersedes the earlier $2.66 derived estimate
- HasData: **0.41** — $0.98/1K — MEASURED 2026-09-24: basic-mode twin run billed 5,121 credits (exactly 3/row) = $1.25 for 1,276 uniques — data/hasdata/raw/speed-basic/. Supersedes the $0.74/1K-ROW rate-card (this figure is per 1K UNIQUE, same basis as all providers); email-mode measured $1.75/1K (scale-findings.md)
- Apify: **0.74** — $0.54/1K — billed via billing API on the full workload ($1.3656 / 2,523 uniques). FLAG: no basic-only price exists — this actor bills per VERIFIED-EMAIL lead, so basic extraction is inseparable from its enrichment economics
- BrightData: **0.27** — $1.50/1K — rate-card ESTIMATE ~$0.75-1.50/1K, upper bound used; NO billing visibility in the API — unverified

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

**Wall-clock, Run-1 batch, BASIC workload (ratio vs fastest; Lobstr and HasData re-timed with enrichment off 2026-09-24, Bright Data bare by design; Apify flagged — enrichment inseparable)** (0.5 pts)
- Lobstr: **0.5** — 45s — MEASURED basic-mode (all 3 enrichment functions off), identical Run-1 workload/concurrency-20 — data/lobstr/raw/speed-basic/. As-tested enriched run was 1,711s (28m31s): ~97% of that wall-clock was website-visit enrichment work
- HasData: **0.15** — 147s — MEASURED basic-mode twin (extractEmails off), identical Run-1 pipeline/timing method — data/hasdata/raw/speed-basic/. Email-mode benchmark run was 431.3s
- Apify: **0.01** — 2,194s — cumulative runTimeSecs across 10 actor runs (knowledge.md; parallelizable). FLAG: enrichment is inseparable from this actor's billing model — no basic-mode timing exists; only available figure used
- BrightData: **0.06** — 365s — data/brightdata/raw/run*/ progress logs (~6 min/run, bare listings by design — already a basic timing)

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
