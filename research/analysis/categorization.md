# Provider Categorization — Direct / Adjacent / Excluded

**Date:** 2026-09-23. Categories per CLAUDE.md §7 and prompt.txt §7. Every provider that surfaced in discovery is accounted for. Verification evidence: `../providers/*.md`.

## Direct competitors
Directly consumable Google Maps business/lead data API, self-serve or near-self-serve.

| Provider | API | Email extraction | Key evidence | Notes |
|---|---|---|---|---|
| Apify | REST v2, actor marketplace | Yes + verification (actor-dependent) | 18/21 web queries, 5/5 LLM, 3/8 Reddit — highest discovery frequency | Already in benchmark; live-tested |
| Outscraper | REST + Python client | Yes (separate billed service, $3/1K) | 16/21 web queries, 4/5 LLM, best genuine Reddit evidence ($50/20K listings user test) | Already in benchmark; live-tested |
| Lobstr.io (house) | REST v1 + SDK/CLI/MCP | Yes (extraction; verification dashboard-only) | 4/5 LLM unprompted, Q20 position 2, 1 listicle | House product — conflict disclosed |
| Scrap.io | REST v1 (/gmap/search, /gmap/place, /gmap/enrich) | Yes — emails + socials native | 5/21 web queries, 2 listicles, 2/5 LLM, 1 Ahrefs SERP | Lead-gen positioned; paid-only from $49/mo, no PAYG; trial API access unverified |
| HasData | Async jobs API + real-time API | Yes — `extractEmails` (10 credits/row vs 3 base) | 1 web query, 1/5 LLM; Reddit presence mostly vendor self-promo | Free tier 1K credits/mo no card; apex domain unreachable from env (docs reachable) |
| Scrapingdog | REST `/google_maps` | **No** | 5/21 web queries, 4/5 LLM, Ahrefs SERP pos 5 | Cheap entry ($40/mo, 200 free credits); business data only |
| SerpApi | Google Maps API (search) | **No** | 5/5 LLM, 3/8 Reddit (2 via employee accounts), 2 listicles — LLM-visibility leader | Per-search pricing (~20 results/search) makes per-record cost query-dependent |
| DataForSEO | Business Data API (GBP info $1.50/1K) | **No** | 4/5 LLM, 1 listicle, 0/21 web queries | SEO-data positioning; strong LLM-only visibility |
| G Maps Extractor | API (Postman-documented) | Yes — emails + socials all tiers | 8/21 web queries, DR 36 | Small footprint; auth method unverified; API tier caps 50K req/mo |
| Bright Data | Web Scraper API + SERP API maps | Not indicated | 5/21 web queries, 5/8 listicles, 5/5 LLM | **Testability flag:** brightdata.com + docs unreachable from research env (DNS, 4 attempts 2026-09-23); pricing unconfirmed ($0.75–1.50/1K, third-party) |

## Adjacent competitors
Can scrape Google Maps but primary product/positioning is broader or different.

| Provider | Why adjacent |
|---|---|
| Oxylabs | General SERP/Web Scraper API (user:pass auth, from $49/mo); no lead enrichment; 0/21 web queries on lead intents — listicle/LLM visibility only |
| ScraperAPI | General scraping API with a structured Maps-search endpoint; no email; site unreachable from env (testability flag) |
| PhantomBuster | Automation platform (Phantoms) with Maps + contact-data phantoms incl. email verification; execution-time pricing → per-record cost not computable in advance (E4 risk); dev API unverified |
| Octoparse | No-code UI templates (incl. Email Finder $0.5/1K lines); Open API is task orchestration, not a data API |
| gosom / Omkar Cloud (open source) | Self-hosted scrapers (8 and 6 web queries respectively, gosom in 3/5 Ahrefs SERPs) — real user option but not a managed API service; can't be benchmarked as a provider SLA product |
| n8n | Workflow templates that wrap other scrapers (7/21 queries) — a channel, not a data provider |
| TexAu, Clay | Automation/enrichment platforms recommended on Reddit; Maps scraping is incidental |
| Chrome/Firefox extensions (MapsLeads.net, Maps Scraper & Map Data Extractor, Scraperz, etc.) | Browser extensions, no API |

## Excluded

| Provider | Concrete reason |
|---|---|
| Google Places API (official) | The baseline product users are trying to replace (appeared in 8/8 Reddit threads with recurring cost complaints) — covered as the article's "official API" section, not a competitor |
| Geoapify, SafeGraph, TravelTime, Radar, Mappr, BizData | POI/geocoding/mapping-data products — serve the "Places API alternative for maps/POI" intent, not lead generation from Google Maps listings |
| G-Business Extractor | All 4 Reddit appearances traced to one repeat-promoter account (coordinated self-promo); desktop tool, no verified API |
| LocalProspects, ScraperCity, LeadStal, MapsHunt, CoreClaw, Leads-Extractor.com, dnleads.co, gmapsscout.com, mapsleadextractor.com, themapgopher.com, Qoest, Ritchy, PandaExtract, WebLeads, BrowserAct, QuickScraper, ig-leads, SmythOS, BlueAcquire, forage.ai, LetsScrapeData, webautomation.io | Surfaced only/mainly as flagged Reddit self-promo; no independent discovery signal; API existence unverified — cannot reasonably be tested |
| Map Lead Scraper, Leads Sniper, Botsol, G Maps Extractor-like desktop tools without APIs, D7 Lead Finder | UI/desktop/extension tools; no directly consumable Maps data API found (Map Lead Scraper: 5 web queries but extension-only) |
| Zyla API Hub | API marketplace aggregator (1 query) — duplicates underlying providers |
| Openmart, Livescraper, Datablist, Oppora, Tendem, Artisan, NoDataNoBusiness | 1–2 total signals each, mostly their own blog/listicle content; insufficient discovery evidence of user consideration |
| OpenWeb Ninja | Preserved from testing phase: key not subscribed to Local Business Data plan (live 403, 2026-09-21) |
| QuantumProxies | Preserved from testing phase: 500-lead per-run technical cap (vendor-doc-confirmed) |
| Yelp / Foursquare / HERE / TomTom / Mapbox / OSM-Nominatim (from LLM sample L3) | Different data source or mapping platform — not Google Maps business data |
