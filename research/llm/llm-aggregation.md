# LLM Recommendation Sampling — Aggregation

**Method:** 5 fresh LLM agents (no conversation context, explicitly barred from web/tool research — answers from model knowledge only), each asked one of the L1–L5 prompts from `research/queries/queries.md`. Models deliberately varied across the Claude family. Full verbatim answers: `L1-answer.md` … `L5-answer.md` in this folder.
**Date:** 2026-09-23
**Caveat:** this measures *LLM visibility* (what an AI assistant recommends when a user asks), sampled from one model family only (Claude). It is not a claim about ChatGPT/Gemini/Perplexity behavior, nor about product quality.

| Sample | Model | Prompt intent |
|---|---|---|
| L1 | Fable 5 | best APIs to scrape business leads from Google Maps |
| L2 | Sonnet | extract thousands of listings programmatically |
| L3 | Haiku 4.5 | alternatives to Google Places API at scale |
| L4 | Opus | commonly used Google Maps scraper APIs for B2B lead gen |
| L5 | Sonnet | API returning Maps businesses with contact details |

## Provider appearance counts (out of 5 samples)

| Provider | L1 | L2 | L3 | L4 | L5 | Total |
|---|:-:|:-:|:-:|:-:|:-:|---:|
| Apify | ✓ | ✓ | ✓ | ✓ | ✓ | **5** |
| SerpApi | ✓ | ✓ | ✓ | ✓ | ✓ | **5** |
| Bright Data | ✓ | ✓ | ✓ | ✓ | ✓ | **5** |
| Outscraper | ✓ | ✓ | – | ✓ | ✓ | **4** |
| DataForSEO | ✓ | ✓ | – | ✓ | ✓ | **4** |
| Lobstr.io (house product) | ✓ | ✓ | – | ✓ | ✓ | **4** |
| Scrapingdog | ✓ | ✓ | – | ✓ | ✓ | **4** |
| Google Places API (official, baseline) | ✓ | ✓ | – | ✓ | ✓ | **4** |
| Oxylabs | ✓ | ✓ | – | ✓ | – | **3** |
| PhantomBuster | ✓ | ✓ | – | ✓ | – | **3** |
| ScraperAPI | ✓ | – | – | ✓ | – | **2** |
| ScrapingBee | ✓ | – | – | ✓ | – | **2** |
| Crawlbase | – | ✓ | – | ✓ | – | **2** |
| Scrap.io | ✓ | – | – | ✓ | – | **2** |
| Octoparse | – | ✓ | – | ✓ | – | **2** |
| Clearbit (enrichment, adjacent) | – | – | ✓ | – | ✓ | **2** |
| Apollo.io (enrichment, adjacent) | – | – | ✓ | – | ✓ | **2** |
| Single mentions | HasData, Piloterr (L1); SearchAPI.io, Traject Data, ScrapeHero, Clay, LeadStal, GMapsExtractor, Lead Scrape, Decodo (L4); Yelp, Foursquare, HERE, TomTom, OSM/Nominatim, Mapbox, Diffbot, Crunchbase, ZoomInfo (L3); Hunter.io (L5) | | | | | 1 each |

## Observations (evidence-bounded)

- The scraping-API intent prompts (L1, L2, L4, L5) consistently surface the same core set: **Apify, SerpApi, Bright Data, Outscraper, DataForSEO, Scrapingdog, Lobstr.io**.
- **Lobstr.io appeared unprompted in 4 of 5 samples** — the agents were not told this research is for Lobstr.
- The Haiku sample (L3, "Places API alternative" phrasing) drifted to POI/mapping APIs (Yelp, Foursquare, HERE, TomTom, Mapbox) and B2B enrichment databases — mirroring the same intent-drift seen in the Ahrefs SERP for "google places api alternative". The "alternative" phrasing attracts mapping-data products, not lead scrapers.
