# Google Maps Leads Scraper API — Competitor Discovery Research Report

**Research date:** 2026-09-23
**Question answered:** *"When users need Google Maps business/lead data through an API, which providers do they actually encounter and consider as solutions?"*
**Conflict of interest (disclosed):** this research is owned by Lobstr.io, whose Google Maps Leads Scraper is one of the evaluated products. Discovery evidence was collected by tools/agents not told to favor Lobstr; Lobstr's weak SERP visibility is reported as-is.

---

## A. Research methodology

- **31 discovery probes:** 21 web-search queries (4 intent categories: lead generation, business data/API, alternatives, scale/automation/enrichment — `../queries/queries.md`), 5 Reddit-focused queries, 5 LLM-recommendation prompts.
- **Sources used:**
  1. **Ahrefs stored Google SERPs** (`serp-overview`, US, organic, top 10) — real Google positions for the 5 queries in Ahrefs' DB; the other 16 recorded as "no Ahrefs SERP data".
  2. **Live web search** (Claude WebSearch, US) — all 21 queries; positions are order-of-appearance, not exact Google ranks.
  3. **Listicle extraction** — 8 comparison/roundup articles fetched, full provider lists recorded.
  4. **Reddit** — 8 threads read in full (via DuckDuckGo + pullpush.io archive; Reddit blocks direct crawling — method + failures documented in `../reddit/reddit-discovery.md`), every mention flagged for self-promo.
  5. **LLM sampling** — 5 fresh agents across 4 Claude models, no web access, answering from model knowledge.
  6. **Ahrefs demand + domain data** — keyword volumes for the query set; DR/traffic/keywords/refdomains for 17 candidate domains.
- **Frequency calculation:** raw counts of distinct queries/SERPs/listicles/LLM-samples/threads per provider (`../analysis/aggregate.py` → `provider-frequency.csv`). No invented weighting.
- **Filtering:** every frequently-surfaced provider verified against its own site/docs (`../providers/*.md` — 14 files), then categorized direct/adjacent/excluded with concrete reasons (`../analysis/categorization.md`).
- **Known gaps (recorded, not filled):** Lobstr's own Google Search Scraper couldn't provide a second live-SERP source (account credits = 0, live-checked); Reddit SERP positions unavailable for 4 of 5 Reddit queries; brightdata.com and scraperapi.com unreachable from the research network (DNS timeouts); LLM sampling is Claude-family only.

## B. Raw evidence

All preserved, reproducible:

```
research/
├── queries/queries.md, keyword-volumes.md
├── discovery/ahrefs-serp-raw.md, websearch-q01-q10.{md,csv}, websearch-q11-q21.{md,csv}
├── reddit/reddit-discovery.md, reddit-mentions.csv
├── raw/reddit/            (per-thread comment JSON, search JSON, DDG HTML)
├── llm/L1..L5-answer.md, llm-aggregation.md
├── ahrefs/domain-metrics.md
├── providers/ (14 verification records)
└── analysis/aggregate.py, provider-frequency.{csv,md}, categorization.md
```

## C. Provider frequency (summary — full table in `../analysis/provider-frequency.md`)

| Provider | Web queries (21) | Ahrefs SERPs (5) | Listicles (8) | LLM (5) | Reddit (8) | Total signals |
|---|---:|---:|---:|---:|---:|---:|
| **Apify** | 18 (86%) | 2 | 4 | 5 | 3 | **32** |
| **Outscraper** | 16 (76%) | 2 | 3 | 4 | 2 | **27** |
| **Bright Data** | 5 | 1 | 5 | 5 | 1 | **17** |
| Scrapingdog | 5 | 1 | 1 | 4 | 1 | 12 |
| gosom (open source) | 8 | 3 | 0 | 0 | 1 | 12 |
| G Maps Extractor | 8 | 1 | 0 | 1 | 1 | 11 |
| Octoparse | 3 | 1 | 2 | 2 | 3 | 11 |
| Scrap.io | 5 | 1 | 2 | 2 | 1 | 11 |
| SerpApi | 1 | 0 | 2 | 5 | 3 | 11 |
| Oxylabs | 0 | 0 | 4 | 3 | 1 | 8 |
| Lobstr.io (house) | 1 | 0 | 1 | 4 | 0 | 6 |
| DataForSEO | 0 | 0 | 1 | 4 | 0 | 5 |

Baseline: **Google Places API (official)** appeared in 8/8 Reddit threads and 4/5 LLM samples — recommended for small jobs, criticized on cost/limits at lead-gen scale. It is the product users are trying to replace.

**Wording note:** these are "most frequently surfaced across our 31 research probes" — not claims of global popularity.

**Reddit caveat:** ~half of all Reddit provider mentions were flagged self-promo/suspected self-promo. Most credible non-promotional Reddit support: Outscraper (a user's live $50/20,000-listings test, recommended 2 years running), Apify, TexAu.

## D. Ahrefs signals (collected 2026-09-23, Ahrefs API v3 — full table in `../ahrefs/domain-metrics.md`)

Domain-level only (supporting signal, not product-level proof): apify.com DR 81 / 476K organic visits/mo · brightdata.com DR 79 / 103K · serpapi.com DR 79 / 105K · oxylabs.io DR 77 / 166K · dataforseo.com DR 76 / 47K · outscraper.com DR 64 / 24K · scrapingdog.com DR 60 / 14K · scrap.io DR 52 / 8.3K · lobstr.io DR 50 / 1.0K · hasdata.com DR 62 / 1.1K · gmapsextractor.com DR 36 / 1.4K.

Demand side: "google maps scraper" 1,800/mo US (7,100 global); "google maps scraper api" 150/mo; "google maps lead scraper" 80/mo; most long-tail lead-API phrasings have no tracked volume (`../queries/keyword-volumes.md`).

## E. Candidate competitors (verification: `../providers/*.md`)

**Already in the benchmark (validated by this discovery):**
1. **Apify** — #1 discovery frequency overall; marketplace saturates lead-intent SERPs (Q03: 9/9 results were Apify actors). API live-tested; known live-confirmed caveats: profit-guard truncation, business_status bug.
2. **Outscraper** — #2 frequency; best genuine Reddit evidence; API live-tested; email extraction is a separately-billed service.
3. **Lobstr.io** (house) — strong LLM visibility (4/5 unprompted), weak SERP visibility (1/21 queries, DR 50, ~1K visits/mo — smallest domain footprint among direct candidates); API live-tested.

**New direct candidates from discovery:**
4. **Scrap.io** — lead-gen-positioned Maps API with native emails+socials and an enrich endpoint; surfaced across 4 source types. Limitations: from $49/mo, no PAYG, trial API access unverified.
5. **HasData** — self-serve jobs API with `extractEmails`; 1K free credits/mo. Limitation: discovery presence partly vendor self-promo on Reddit; email rows cost 3.3× base.
6. **Scrapingdog** — Maps API, cheap entry, 4/5 LLM + SERP presence. Limitation: **no email/contact extraction** — cannot serve the enrichment intent.
7. **SerpApi** — highest LLM/Reddit visibility after Apify; API-only product with free 250 searches/mo. Limitations: no email extraction; per-search (~20 results) pricing; 2 of 3 Reddit threads involved employee accounts.
8. **DataForSEO** — Business Data API, $1.50/1K profiles, self-serve sandbox. Limitations: no email; zero web-SERP presence on lead intents (LLM-only visibility).
9. **G Maps Extractor** — API with emails/socials included; 8/21 web queries. Limitations: small domain (DR 36), auth undocumented publicly, low API caps.
10. **Bright Data** — top-3 aggregate visibility (esp. listicles + LLM). Limitations: site unreachable from the research environment (4 DNS failures, 2026-09-23) → concrete E1 testability risk; pricing unconfirmed ($0.75–1.50/1K, third-party only).

## F. Excluded providers (full list with reasons: `../analysis/categorization.md`)

- **Google Places API (official)** — the baseline being replaced, not a competitor.
- **POI/geodata cluster** (Geoapify, SafeGraph, TravelTime, Radar, Mappr, BizData) — serve mapping/POI needs, not lead generation; they dominate only the "Places API alternative" phrasing.
- **Reddit self-promo cluster** (G-Business Extractor — 4 threads, all one promoter account; LocalProspects, LeadStal, ScraperCity, MapsHunt, +~20 more) — no independent signal, unverifiable APIs.
- **Extensions/desktop tools** (Map Lead Scraper, MapsLeads.net, Leads Sniper, D7 Lead Finder, …) — no API.
- **Open source** (gosom, Omkar Cloud) — real DIY option (gosom: 3/5 Ahrefs SERPs), but self-hosted software, not a testable managed API.
- **Adjacent platforms** (Oxylabs, ScraperAPI, PhantomBuster, Octoparse, n8n, TexAu, Clay) — capable but not positioned/priced as Maps lead-data APIs (details in categorization).
- **Preserved from testing phase:** OpenWeb Ninja (403 not-subscribed, live 2026-09-21), QuantumProxies (500-lead/run cap).

## G. Recommended test set

The current benchmark trio — **Lobstr.io, Apify, Outscraper** — is retroactively validated: the two external providers are exactly the #1 and #2 most frequently surfaced across all 31 probes.

Strongest additional candidates to investigate (evidence-based, in order):

1. **Scrap.io** — should be tested because it is the only new candidate that matches the full lead-gen intent stack (Maps search + native email/social enrichment via API), surfaced in 4 of 5 source types, and directly targets the same user as Lobstr's product.
2. **SerpApi** — should be tested because it has the highest AI-assistant/community visibility of any untested provider (5/5 LLM, 3/8 Reddit) — users asking an LLM "which Maps API?" will hear this name; the article should answer whether it serves lead gen (it lacks email extraction, which testing would make concrete).
3. **Scrapingdog** — should be tested because it combines real SERP presence (5/21 queries + Ahrefs SERP pos 5 on the head API term) with 4/5 LLM visibility and the lowest entry price among API-first candidates; its missing email extraction is a key user-facing limitation to demonstrate.
4. **HasData** — should be tested because it is fully self-serve (1K credits/mo free, no card) with native `extractEmails` — the cheapest way to add a second email-capable competitor; its visibility partly rests on self-promo, which testing would either substantiate or puncture.
5. **Bright Data** — conditional: highest untested aggregate visibility, but only if a key + run are obtainable within 48h (E1) despite the connectivity issues observed today; otherwise document the access failure as the finding.

---

## Final summary

**Research scope:** 31 probes (21 web + 5 Reddit + 5 LLM) across 6 source types, 2026-09-23.

**Most frequently surfaced candidates:**
1. **Apify** — 18/21 web queries, 2/5 Ahrefs SERPs, 4/8 listicles, 5/5 LLM samples, 3/8 Reddit threads
2. **Outscraper** — 16/21 web queries, 2/5 Ahrefs SERPs, 3/8 listicles, 4/5 LLM, 2/8 Reddit (incl. the sample's best genuine user test)
3. **Bright Data** — 5/8 listicles, 5/5 LLM, 5/21 web queries (site unreachable from research env — testability risk)
4. **Scrapingdog** — 5/21 web queries, 4/5 LLM, Ahrefs SERP pos 5 on "google maps scraper api"
5. **SerpApi / Scrap.io / G Maps Extractor / Octoparse / gosom** — 11 signals each, different profiles (LLM+Reddit / lead-gen product / SERP / community / open source)

**Candidates requiring API testing:** Scrap.io · SerpApi · Scrapingdog · HasData · Bright Data (conditional on access)

**Excluded (headline examples):** Google Places API (baseline, not competitor) · Geoapify/SafeGraph/TravelTime (POI data, wrong intent) · G-Business Extractor (coordinated Reddit self-promo, no verified API) · gosom/Omkar Cloud (open-source software, not managed APIs) · PhantomBuster (execution-time pricing, cost-per-record incomputable in advance) · full list with reasons in `../analysis/categorization.md`.
