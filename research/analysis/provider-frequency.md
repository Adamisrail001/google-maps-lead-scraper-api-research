# Provider Frequency Analysis

**Date:** 2026-09-23
**Computed by:** `aggregate.py` (this folder) from `../discovery/websearch-q01-q10.csv`, `../discovery/websearch-q11-q21.csv`, `../discovery/ahrefs-serp-raw.md`, `../llm/llm-aggregation.md`, `../reddit/reddit-mentions.csv`. Machine-readable output: `provider-frequency.csv`.

**Counting rules (raw counts, no invented weighting):**
- **Web queries** — distinct web-search queries (of 21) where the provider appeared as a result
- **Ahrefs SERPs** — distinct Ahrefs-stored Google SERPs (of the 5 available) with an organic appearance
- **Listicles** — distinct comparison/roundup articles (8 fetched) mentioning the provider
- **LLM** — LLM samples (of 5) recommending the provider
- **Reddit** — distinct Reddit threads (of 8 read) mentioning the provider

"Total signals" is a simple sum for sorting only — it is NOT a quality score.

| Provider | Web queries (of 21) | % | Ahrefs SERPs (of 5) | Listicles (of 8) | LLM (of 5) | Reddit (of 8) | Total |
|---|---:|---:|---:|---:|---:|---:|---:|
| Apify | 18 | 86% | 2 | 4 | 5 | 3 | **32** |
| Outscraper | 16 | 76% | 2 | 3 | 4 | 2 | **27** |
| Bright Data | 5 | 24% | 1 | 5 | 5 | 1 | **17** |
| Scrapingdog | 5 | 24% | 1 | 1 | 4 | 1 | **12** |
| gosom (open source) | 8 | 38% | 3 | 0 | 0 | 1 | **12** |
| G Maps Extractor | 8 | 38% | 1 | 0 | 1 | 1 | **11** |
| Octoparse | 3 | 14% | 1 | 2 | 2 | 3 | **11** |
| Scrap.io | 5 | 24% | 1 | 2 | 2 | 1 | **11** |
| SerpApi | 1 | 5% | 0 | 2 | 5 | 3 | **11** |
| Oxylabs | 0 | 0% | 0 | 4 | 3 | 1 | **8** |
| n8n (workflow templates) | 7 | 33% | 1 | 0 | 0 | 0 | **8** |
| Omkar Cloud (open source) | 6 | 29% | 0 | 0 | 0 | 1 | **7** |
| PhantomBuster | 2 | 10% | 0 | 1 | 3 | 1 | **7** |
| ScrapingBee | 3 | 14% | 0 | 1 | 2 | 1 | **7** |
| Lobstr.io (house product) | 1 | 5% | 0 | 1 | 4 | 0 | **6** |
| ScraperAPI | 3 | 14% | 1 | 0 | 2 | 0 | **6** |
| DataForSEO | 0 | 0% | 0 | 1 | 4 | 0 | **5** |
| Map Lead Scraper | 5 | 24% | 0 | 0 | 0 | 0 | **5** |
| SafeGraph (POI) | 3 | 14% | 1 | 1 | 0 | 0 | **5** |
| TravelTime (POI) | 3 | 14% | 1 | 1 | 0 | 0 | **5** |
| Chrome extensions (various) | 4 | 19% | 1 | 0 | 0 | 0 | 5 |
| Leads Sniper | 2 | 10% | 1 | 0 | 0 | 1 | 4 |
| Others (≤3 signals) | Artisan, LocalProspects, Botsol, HasData*, Crawlbase, ScrapeHero, Traject Data, Geoapify, Mappr, BizData, Openmart, Livescraper, Datablist, Oppora, Tendem, NoDataNoBusiness, Zyla, TexAu, Clay… | | | | | | |

\* HasData: 1 web query + 1 LLM + 1 Reddit thread (Reddit mentions were mostly vendor self-promo — see caveat below).

## Baseline (not a competitor)

**Google Places API (official)** appeared in all 8 Reddit threads and 4/5 LLM samples — consistently recommended for small jobs and consistently criticized on cost/limits for lead-gen scale. This is the "alternative to what" baseline for the article, not a candidate.

## Important caveats on the evidence

1. **Reddit is heavily astroturfed for this topic.** Roughly half of all Reddit provider mentions carried self-promo or suspected-self-promo flags (per-mention flags in `../reddit/reddit-mentions.csv`). The most credible non-promotional Reddit support: **Outscraper** (an OP live-tested $50/20,000 listings and recommended it 2 years running), **Apify**, **TexAu**. SerpApi's 3 threads include employee/founder accounts in 2 of them (disclosed). G-Business Extractor's 4 threads are all one repeat-promoter account — treated as coordinated promo, not organic signal.
2. **Reddit SERP positions unavailable for QR2–QR5** — WebSearch cannot return reddit.com results (Reddit blocks the crawler); fallback was DuckDuckGo (QR1 only) + pullpush.io archive full-text search. Documented in `../reddit/reddit-discovery.md`.
3. **The "Places API alternative" intent cluster (Q12/Q14/Q15) surfaces a different market** — POI/geodata providers (Geoapify, SafeGraph, TravelTime, Mappr, BizData). These serve map/POI data needs, not lead generation, and are categorized adjacent/excluded.
4. **LLM sampling is Claude-family only** (5 samples, 4 models) — an LLM-visibility signal, not a cross-assistant measurement.
5. **Web-search positions are order-of-appearance in the search tool, not exact Google ranks.** Exact Google positions exist for the 5 queries with Ahrefs stored SERPs.
6. **Lobstr.io (the house product)** shows strong LLM visibility (4/5 samples, unprompted) but low SERP visibility (1/21 web queries, 0/5 Ahrefs SERPs, 0/8 Reddit threads). Recorded as-is; conflict of interest disclosed in the final report.
