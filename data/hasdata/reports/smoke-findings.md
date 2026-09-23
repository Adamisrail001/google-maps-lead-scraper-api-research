# HasData Google Maps Scraper — Free-Plan Smoke Test Findings

**Date:** 2026-09-23 · **Raw evidence:** `data/hasdata/raw/smoke/` · **Spend:** 278 of 1,000 free monthly credits (no card) — job 515783 base (40 rows, 120 credits) + job 515784 with `extractEmails` (20 rows, 158 credits).

## Verdict: PASS — strongest new lead-gen candidate; deserves the scale test

Unlike Scrapingdog and Google, HasData delivers the defining lead field: **real email extraction via API**, and its measured email fill on this (small) sample beat every provider in the benchmark.

## What was verified

1. **API mechanics:** `POST api.hasdata.com/scrapers/google-maps/jobs` (x-api-key), body `{keywords: [...], locations: [...], limit, extractEmails}` — async job → `GET /scrapers/jobs/{id}/results` (paginated, ≤100/page). Precise 422 validation errors made the schema self-discoverable.
2. **Speed:** email job created→data-complete in **~18s for 20 rows incl. website-visit email extraction**; base job ~5min for 40 rows (queue variance; n=2 jobs, not conclusive).
3. **Field fills** — base job (40 Manhattan agencies): title/website/rating/reviews/coords/place_id 100%, phone 85%, hours 93%. Email job (20 Van Nuys agencies): website 100%, phone 95%, **emails 14/20 = 70%** (vs Lobstr 59%, Apify 32% on the same vertical in the benchmark — small-sample caveat, n=20).
4. **Billing observed:** base exactly 3 credits/row (120/40 ✓). Email job billed **158 credits, not the naive 20×10=200** — effective 7.9 credits/row all-in; the discount pattern (charged only for crawled/found?) is undocumented — measure precisely in the scale test.
5. **Cost projection (rate-card, Startup $49/mo = 200K credits):** all-in email rows at 7.9 credits ≈ **$1.94/1K rows with ~70% emails** — roughly 3× cheaper than Lobstr's measured $5.82/1K (59% emails), if it holds at scale.

## Caveats / open items for the scale test

- **Status quirk:** both jobs stuck at `exporting_data` indefinitely (never reached `finished` in 5+ min of polling) while results were fully retrievable — scale scripts must poll the results endpoint, not trust the status field. Same "don't trust top-level status" lesson class as Apify.
- **Field-set inconsistency:** the `extractEmails` job's rows lacked `workingHours`/`openState` columns that the base job returned — schema varies by job options; verify at scale.
- **No social profiles in results** — docs list LinkedIn/social as separate per-field enrichments (5 credits each), untested this round.
- Address fill dipped to 15/20 on the email job (75%) vs 100% base — small sample, recheck.
- hasdata.com apex domain unreachable from this network (docs + API reachable; local DNS flakiness required DoH-pin fallback mid-test).

## Recommended scale test

Same 2 runs × 10 sub-areas, `extractEmails: true`, limit 200/sub-area: ~4,000 rows × ~8 credits ≈ 32,000 credits — needs the **Startup plan ($49)**; free tier (1,000) covers only a ~125-row mini-run. Direct head-to-head vs Lobstr on the email-fill and cost-per-contact axes.
