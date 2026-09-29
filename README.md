# Google Maps Lead Scraper API Benchmark — Raw Evidence

Public evidence repository for a benchmark of Google Maps scraper APIs run 2026-09-22 → 2026-09-24.

**Providers tested:** lobstr.io, HasData, Bright Data, Apify (`themineworks/maps-leads`), Outscraper, ScrapingDog, and the official Google Places API (New) as baseline.

**Workload:** identical for every provider — 20 searches (marketing agencies + restaurants) across 10 NYC/LA borough/district sub-areas, up to 200 results each (4,000 requested per provider), graded against a 24-business live ground truth.

**Disclosure:** lobstr.io runs this benchmark and is one of the evaluated providers. That is exactly why every raw request, response, run log and credit snapshot is published here. If you distrust a number, re-derive it.

## Repository layout

```text
data/<provider>/raw/        every raw request & response, run logs, credit snapshots
data/<provider>/analysis/   per-provider analyses incl. ground-truth comparison
data/google-places-api/raw/ the official-API baseline runs
ground-truth/               the 24-business live sample (sample-24.json) + checklist
scripts/                    runners and analyzers for every provider
SCORING-REPORT.md           every criterion, formula, and fairness measure
scoring.md                  generated ranking table (regenerate: see below)
```

## Reproduce it

```bash
python scripts/compute_final_scorecard.py   # regenerates scoring.md from the raw files in data/
python scripts/ground_truth_compare.py      # regrades all four ranked providers against the truth
```

Field fills, unique counts and ground-truth scores are recomputed live from `data/` on every run — nothing in the ranking table is hand-typed.

To rerun a provider against the live APIs, put your own keys in `.env` (see `.env.example`; keys are never committed) and use the matching `scripts/<provider>_*.py` runner. Fairness re-runs (enrichment-off timing twins for lobstr.io and HasData) are `scripts/lobstr_basic_speed_run.py` and `scripts/hasdata_basic_speed_run.py`.

## Headline findings

See `SCORING-REPORT.md` for the full method and every number. Short version: no tool beats Google's ~200-per-search ceiling; what separates them is delivery honesty (one provider's undocumented profit-guard truncates low-yield queries while reporting success), billing visibility (one exposes no billing data at all), fills, accuracy against the live listing, and cost per 1K listings.
