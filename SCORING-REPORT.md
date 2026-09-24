# Google Maps Lead Scraper APIs — Detailed Scoring Report

**Date of record:** 2026-09-24 · **Benchmark window:** 2026-09-22 → 2026-09-24
**Generated ranking table:** [`scoring.md`](scoring.md) (regenerate any time with `python scripts/compute_final_scorecard.py` — field fills, unique counts and ground-truth scores are recomputed live from the raw files in `data/` on every run)
**Factual record:** [`IMPORTANT/knowledge.md`](IMPORTANT/knowledge.md) · **Methodology:** [`IMPORTANT/criteria.md`](IMPORTANT/criteria.md)

**Disclosure:** Lobstr.io owns this methodology and is one of the evaluated providers. Every number in this report traces to a raw file in this repository, every formula is written down below, and the fairness measures in §7 were applied symmetrically — including re-running the closest rival under the same favorable conditions as the house product. If you distrust any figure, §9 tells you how to re-derive it yourself.

---

## 1. The user this ranking serves

The score answers one question: **"Which API best extracts all available Google Maps business listings from a search — name, address, phone number, opening hours — reliably and affordably?"**

That user definition is evidence, not assumption: a 31-probe discovery study (`user-intent.md`) and an independent 12-voice confirmation sweep (`research/analysis/who-why-research.md`) both found ~60–70% of real demand is exactly this listings-extraction job. Enrichment (emails, social profiles, images, verification) is **bonus value** — it improves the Data Quality criterion but is never a requirement and never a disqualifier.

## 2. The workload every provider ran

Identical for all: **2 runs** (marketing agencies, restaurants) × **10 NYC/LA borough/district sub-areas** (5 NYC boroughs + 5 LA districts, `scripts/lib/config.py`) × up to **200 results per query** = 4,000 requested per provider. 200/query is Google Maps' own per-search ceiling, verified server-side (Lobstr rejects >200 with a live `400 AttributeLimitExceeded`). Every raw request and response is preserved under `data/<provider>/`.

## 3. Step 0 — core-requirement screen (who gets scored at all)

A provider is disqualified **only** for failing a core requirement: reliable listing extraction, required volume, usable/storable results, or affordable basic extraction. Missing optional features never disqualify. Disqualified providers get **no score** — their measured results are shown as findings.

| Provider | Verdict | Ground (all measured) | Evidence |
|---|---|---|---|
| Lobstr, HasData, Apify, Bright Data | **SCORED** | Pass all four core requirements | §5 below |
| Google Places API (New) | **DISQUALIFIED** | Hard 60-results/query cap (hit on 10/10 restaurant queries: 444 uniques vs scrapers' 998–1,405 on identical queries) + its own Terms §3.2.3 bar storing/exporting the extracted list — the user can neither get *all* listings nor *keep* them. Otherwise the best-engineered API tested (60/60 requests, 1.54s median, phone 95.4% / hours 97.9% fills) | `research/raw/google-places-api/`, terms fetched 2026-09-23 |
| Outscraper | **DISQUALIFIED** | Affordability: $3.69/1K unique measured on base scrape alone — most expensive basic extraction vs $0.54–1.67 measured for scored providers. Otherwise strong (97.5% core-4 fills, 96.8% delivery on its budget-reduced 80/query batch) | `data/outscraper/` |
| ScrapingDog | **DISQUALIFIED** | Required volume: full-scale run on a paid Lite key measured a hard ~49-unique/query depth ceiling (range 39–57 — below Google's disqualifying 60), 862 uniques vs 1,739–2,567 for scored providers, and it keeps serving fully-billed 100%-duplicate pages past the ceiling with no signal (44 billed = 22% of spend). Otherwise excellent: $0.23/1K measured, 97.4% core-4 fill, ~1.0s median | `data/scrapingdog/raw/run*-llpage/`, `data/scrapingdog/reports/scale-findings.md` |

## 4. Scoring method (criteria.md §4, unchanged)

Seven criteria, 10 points total: **Reliability 2.0 · Data Quality 2.0 · Cost 1.5 · Speed 1.5 · Scalability 1.2 · Developer Experience 1.0 · Input Flexibility 0.8.** Two scoring modes:

- **Ratio sub-criteria** (anything directly measurable): the best measured value gets full points, others scaled proportionally — `points × (value ÷ best)` for higher-is-better, `points × (best ÷ value)` for lower-is-better (cost, time).
- **Anchor sub-criteria** (qualitative): Full = 100%, Partial = 60%, Weak = 0–20% of the sub-criterion's points — every anchor cites the specific evidence it rests on (all listed in `scoring.md`'s sub-criterion detail).

Median and p95 latency (0.8 pts combined) score 0 for all four providers equally — all are batch/async architectures with no per-request timing to measure, so the **effective ceiling is 9.2/10**, not 10.

## 5. How each criterion was calculated, with the evidence

### 5.1 Reliability (2.0) — did the listings actually arrive?

`success = returned ÷ requested`, ratio vs best; plus anchors for empty/partial responses, error handling, stability.

| | Returned/requested | Success sub (1.0) | Anchors (1.0) | Total | Key evidence |
|---|---|---:|---:|---:|---|
| Lobstr | 3,403/4,000 = 85.1% | 0.98 | 1.00 (no empty/partial, precise errors, stable) | **1.98** | `data/lobstr/raw/run1-final.json` + pooled Run 2 |
| Bright Data | 1,741/2,000 = 87.1% (best) | 1.00 | 0.88 | **1.88** | `data/brightdata/raw/run*/snapshot.json` |
| HasData | 2,946/4,000 = 73.7% | 0.85 | 0.72 (field wobble run1 vs run2; status field never reaches `finished`) | **1.57** | `data/hasdata/raw/run*/` per-job logs |
| Apify | 2,730/4,000 = 68.3% | 0.78 | 0.20 (4/20 queries silently truncated by undocumented profit-guards while reporting SUCCEEDED; `business_status` broken on 100% of records — raw run logs) | **0.98** | `data/apify/raw/` |

### 5.2 Data Quality (2.0) — core fields first, enrichment as bonus, accuracy against reality

Four sub-criteria: **field coverage 0.8** = `0.6 × (core-4 fill ÷ best) + 0.2 × (enrichment fill ÷ best enricher)` — core-4 = mean fill of name/address/phone/hours on all uniques, computed live from raw files; enrichment = mean of email% and social%. **Accuracy 0.5** and **freshness 0.3**: measured against a live ground truth (§6). **Schema consistency 0.4**: anchors.

| | Core-4 fill | Enrichment | Accuracy | Freshness | Schema | Total |
|---|---:|---:|---:|---:|---:|---:|
| Lobstr | 97.1% (best) | 45.3% email + 56.8% social (reference) | **100%** (180/180) | 100% | Full | **2.00** |
| Bright Data | 96.4% | 0% | 98.3% | 100% | Full | **1.79** |
| HasData | 94.2% | 41.7% email | 98.9% | 100% | Partial (run-to-run field wobble) | **1.69** |
| Apify | 92.8% | 28.3% verified email | 98.7% | 100% (rating-only basis — no review-count field, flagged) | Partial (broken business_status) | **1.66** |

### 5.3 Cost (1.5) — basic workload first, measured wherever possible

`cost sub (0.8) = 0.8 × (cheapest ÷ provider's basic $/1K unique)`; plus anchors for billing fairness, free tier, pricing transparency. **Evidence tiers are never mixed silently**: billed-API figure > measured credits × plan rate > rate-card estimate.

| | Basic $/1K unique | Evidence tier | Cost sub | Anchors | Total |
|---|---:|---|---:|---:|---:|
| Apify | $0.54 (cheapest) | **Billed** via its billing API — flagged: it bills per verified-email lead, no basic-only mode exists | 0.80 | 0.54 | **1.34** |
| HasData | $0.98 | **Measured** 2026-09-24: basic twin billed 5,121 credits (exactly 3/row) = $1.25 / 1,276 uniques | 0.44 | 0.62 | **1.06** |
| Lobstr | $1.67 | **Measured** 2026-09-24: enrichment-off run billed 926 credits for 926 uniques (exactly 1/unique) × Growth rate | 0.26 | 0.54 | **0.80** |
| Bright Data | ~$1.50 | **Rate-card estimate, unverified** — its API exposes no billing at all (also why its fairness/transparency anchors are Weak) | 0.29 | 0.22 | **0.51** |

### 5.4 Speed (1.5) — same basic workload, timed like-for-like

`wall-clock sub (0.5) = 0.5 × (fastest ÷ provider)` on the Run-1 batch; async-endpoint anchor 0.2 (all Full); median/p95 latency 0.8 = N/A for all (batch/async).

The wall-clocks are **basic-workload timings**: Lobstr and HasData were both re-run 2026-09-24 with enrichment off on the identical workload (§7); Bright Data's benchmark timing was already bare-listings; Apify's enrichment is inseparable from its billing model, so its as-tested figure is used, flagged.

| | Basic wall-clock | Wall sub | Total | Evidence |
|---|---:|---:|---:|---|
| Lobstr | **45.3s** (fastest; as-tested enriched run was 1,711s — ~97% of it was website-visit enrichment work) | 0.50 | **0.70** | `data/lobstr/raw/speed-basic/` |
| HasData | 146.6s (431.3s in email mode) | 0.15 | **0.35** | `data/hasdata/raw/speed-basic/` |
| Bright Data | 365.0s | 0.06 | **0.26** | `data/brightdata/raw/run*/` progress logs |
| Apify | 2,194.5s cumulative (flagged: only available timing) | 0.01 | **0.21** | knowledge.md speed table |

### 5.5 Scalability (1.2), 5.6 Developer Experience (1.0), 5.7 Input Flexibility (0.8)

Anchor-scored with cited evidence per line (full detail in `scoring.md`). Highlights: Lobstr is the only provider with user-controlled concurrency (20 slots) and no hidden caps found (Scalability 1.20); Apify's profit-guards make its volume behavior vertical-dependent (0.44); Bright Data's onboarding friction, unreachable docs and keyword-only inputs cost it DevEx (0.36) and Input Flexibility (0.38); HasData's endpoint breadth and enrichment endpoints lead Input Flexibility (0.68).

## 6. The ground truth behind accuracy and freshness

Built 2026-09-24 per testing-plan §10. **Sample selection:** 24 businesses returned by **all four providers** (joined on Google CID — 6 per industry×city sub-group, deterministic pick), so every provider is graded on the same records. **Truth values:** captured live from **Google Maps itself** (Places API Details, full field mask, per-record timestamps — `ground-truth/sample-24.json`); provider records only decided *which* businesses to check, never what counts as correct. **Grading:** per field, a provider is graded only where both it and the truth have a value; normalization handles format noise (phone digits, website domains, hours separators), and two oracle artifacts were excluded transparently (Google's `primaryTypeDisplayName` returns a generic "Services" bucket for agencies; category is graded against the full `types` list, with generic-only truths marked not-comparable). **Freshness:** a record is fresh if its rating (±0.1) and review count (±max(5%, 5)) match the same-day live values. Comparison outputs: `data/<provider>/analysis/ground-truth-match.json`. A manual browser spot-check of 3 flagged businesses (`ground-truth/manual-checklist.md`) is pending; until it's done, the claim is "verified against live Places data," not "hand-verified."

## 7. Fairness measures (read this before questioning the house product's win)

1. **Enrichment-off twins, run on both sides.** Lobstr's as-tested wall-clock (28m31s) included website-visit enrichment that bare-listings providers never do. Rather than compare unlike work, the identical Run-1 workload was re-run with enrichment off — **for Lobstr (45.3s, $1.67/1K) AND for its closest rival HasData (146.6s, $0.98/1K)**. Nobody can say only the house product got the favorable re-timing. Apify has no separable basic mode (flagged); Bright Data was already basic.
2. **Cost-framing sensitivity check.** Recomputing the Cost criterion with fully-enriched as-tested spend instead (Lobstr $5.82/1K, HasData $1.75/1K) gives Lobstr 7.85 vs HasData 6.88 — **the #1 spot is stable under both framings.** If any framing had flipped the ranking, this report would say so.
3. **Enrichment never punishes rivals.** Providers without emails/socials lose nothing outside the explicit 0.2-point enrichment bonus inside field coverage; the DQ screen ignores optional features entirely.
4. **Every anchor cites evidence; every ratio is a written formula.** No sub-score exists that cannot be traced to a raw file and re-derived by hand.
5. **Evidence tiers are labeled** wherever cost appears — a billed figure, a measured-credits figure, and a rate-card estimate are never presented as equivalent.

## 8. Final result

| Rank | Provider | Reliability /2.0 | Data Quality /2.0 | Cost /1.5 | Speed /1.5 | Scalability /1.2 | DevEx /1.0 | Input Flex /0.8 | **Total /10** (ceiling 9.2) |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | **Lobstr.io** (house — disclosed) | 1.98 | 2.00 | 0.80 | 0.70 | 1.20 | 0.76 | 0.60 | **8.04** |
| 2 | **HasData** | 1.57 | 1.69 | 1.06 | 0.35 | 1.00 | 0.72 | 0.68 | **7.07** |
| 3 | **Bright Data** | 1.88 | 1.79 | 0.51 | 0.26 | 0.88 | 0.36 | 0.38 | **6.06** |
| 4 | **Apify** (themineworks/maps-leads) | 0.98 | 1.66 | 1.34 | 0.21 | 0.44 | 0.72 | 0.48 | **5.83** |

Not scored (core-requirement failures, results shown in §3): Google Places API, Outscraper, ScrapingDog.

## 9. Reproduce it yourself

```
scripts/compute_final_scorecard.py   # regenerates scoring.md; fills/uniques/GT scores recomputed live
scripts/ground_truth_build.py        # rebuilds the 24-business sample + captures live truth (needs GOOGLE_PLACES_API_KEY)
scripts/ground_truth_compare.py      # regrades all four providers against the truth
scripts/lobstr_basic_speed_run.py    # the Lobstr enrichment-off twin (needs LOBSTR_API_KEY)
scripts/hasdata_basic_speed_run.py   # the HasData basic-mode twin (needs HASDATA_API_KEY_SCALE)
scripts/scrapingdog_scale_run2.py    # ScrapingDog full-scale run (ll+page mode)
scripts/hasdata_scale_run.py, brightdata_scale_run.py, google_places_run.py ...
```

Raw evidence lives under `data/<provider>/raw/` (every request/response), analyses under `data/<provider>/analysis/`, ground truth under `ground-truth/`, and the discovery research that chose the candidate set under `research/`. Keys go in `.env` (never committed). Swap in your own keys, rerun any script, and compare against the committed raw files.
