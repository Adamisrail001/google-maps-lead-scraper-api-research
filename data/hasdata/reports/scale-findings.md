# HasData Google Maps Scraper — Stage-2 Scale Test Findings

**Date:** 2026-09-23 · **Plan:** Startup ($49/mo, 200K credits) · **Design:** benchmark-standard 2 runs × 10 sub-areas, limit 200/job, `extractEmails: true` · **Raw:** `data/hasdata/raw/run1/`, `run2/` (submit/final/results pages per job + run logs) · **Script:** `scripts/hasdata_scale_run.py`

## Results

| | Run 1 (agencies) | Run 2 (restaurants) | Both |
|---|---:|---:|---:|
| Raw rows | 1,634 | 1,312 | 2,946 |
| Unique (placeId dedupe) | 1,204 | 1,252 | **2,456** |
| **Email fill (unique)** | **46%** | **37%** | **42% (1,025 emails)** |
| Credits (measured, per-job `creditsSpent`) | 10,110 | 7,408 | 17,518 |
| Cost @ Startup rate | $2.48 | $1.81 | **$4.29** |
| Wall-clock | ~4 min | ~5 min | — |

**Cost per 1,000: $1.75/1K unique (email-enriched) · $4.19/1K emails obtained.** Versus Lobstr measured: $5.82/1K unique · $6.20/1K emails — **~3.3× cheaper on both axes** (both providers' emails are extraction-only, unverified — comparable class).

## Head-to-head vs the ranked scrapers (same queries, both runs)

| | HasData | Lobstr | Apify |
|---|---:|---:|---:|
| Unique | 2,456 | 2,567 | 2,523 |
| Email fill | 42% | 47% blended (59%/37%) | 28% (verified) |
| $/1K unique | **$1.75** | $5.82 | $0.54 (but 28% enrichment) |
| Wall-clock/run | **~4–5 min** | ~29 min | ~22–37 min cumulative |
| Socials/images/owner | ✗ (socials = separate 5-credit enrichments, untested) | ✓ | ✗ |

Restaurants email fill was **identical to Lobstr's (37%)** — reinforcing the "email yield is a property of the vertical" finding. Agencies: Lobstr 59% vs HasData 46%.

## Caveats (attach to any published numbers)

1. **The smoke's 70% email fill did not hold at scale** (46% agencies) — single-query smoke samples overestimate; scale numbers are the citable ones.
2. **Schema variance again (run 1):** rating/reviews filled only 73% and address 82% on the agencies run, while run 2 was 97–100% on everything — field completeness fluctuates by run/vertical in email mode. Not observed in run 2; unexplained, preserved as-is.
3. Delivery vs requested: 2,946/4,000 = 74% (Lobstr 85%, Apify 68%) — under-delivery concentrated in LA sub-areas (Koreatown 69–81, Hollywood 97) consistent with supply, and restaurants capped well below 200/job (max 182) — no guard messages observed; no evidence of Apify-style economic truncation.
4. Concurrency 5 on Startup — the 429-then-retry submit pattern is required for 10-job runs (handled in script).
5. Status field never reaches `finished` (sticks at `exporting_data`) — completion detected via results endpoint (smoke lesson, held at scale).

## Bottom line for the per-persona scoring

Persona 2 (lead-gen): a genuine challenger — ~3× cheaper than Lobstr per email with 5–13pt lower email fill and materially poorer record richness (no socials/images/owner). Persona 1: viable but unremarkable — $1.75/1K with emails wasted; base mode ($0.74/1K equivalent at 3 credits/row) would compete with Scrapingdog's projected pricing. Persona 3: async jobs + webhooks + clean docs, 5-concurrency cap on entry plan.
