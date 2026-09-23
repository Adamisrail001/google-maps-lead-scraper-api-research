# LLM Answer — Prompt L1

- **Prompt ID:** L1
- **Date:** 2026-09-23
- **Question (exact):** "What are the best APIs to scrape business leads from Google Maps?"
- **Model:** Claude Fable 5 (claude-fable-5, Anthropic Claude family) — answered purely from model knowledge, no web search or external tools used.

---

**What are the best APIs to scrape business leads from Google Maps?**

Here are the services I'd recommend from memory:

1. **Google Places API (official)** – Google's official API for place/business data; reliable and compliant, but limited to ~20 results per query (60 with pagination), restrictive terms, and no emails — not built for bulk lead scraping.
2. **Outscraper** – A popular Google Maps scraping API purpose-built for lead generation; returns businesses at scale with phone, website, ratings, and offers email/contact enrichment.
3. **Apify (Google Maps Scraper actor)** – A marketplace-based scraping platform whose Google Maps actors extract thousands of listings with reviews, photos, and contact details via API.
4. **SerpApi (Google Maps API)** – A SERP-scraping API with dedicated Google Maps and Local Results endpoints; fast, structured JSON, good for search-style extraction rather than deep enrichment.
5. **ScrapingBee / Scrapingdog / ScraperAPI (Google Maps endpoints)** – General-purpose scraping APIs offering Google Maps endpoints; handle proxies and rendering, useful if you're already in their ecosystem.
6. **DataForSEO (Google Maps / Business Data API)** – SEO-data provider with Business Data endpoints returning Google Maps listings and reviews at competitive per-request pricing.
7. **Bright Data** – Enterprise-grade data collection platform with a Google Maps dataset/scraper API; strong at very large scale but more complex and pricier to start.
8. **Oxylabs** – Enterprise proxy/scraper provider whose SERP Scraper API can target Google Maps results; suited to high-volume, compliance-conscious teams.
9. **Lobstr.io (Google Maps Search Export)** – A cloud scraper with an API that extracts Google Maps business listings (name, phone, website, ratings, etc.) in bulk from search URLs.
10. **PhantomBuster** – Automation platform with Google Maps "phantoms" that extract search results and contact info; more of a growth-hacking tool with API access than a raw data API.
11. **HasData (formerly ScrapeIt)** – Offers a dedicated Google Maps scraper API returning structured listing data as JSON.
12. **Piloterr / Scrap.io** – Newer players: Piloterr provides Google Maps endpoints among many APIs; Scrap.io focuses specifically on exporting Google Maps leads with email/social enrichment.

Notes I'd give a user: the official Places API is the only ToS-compliant option but is poorly suited to lead-gen (no emails, result caps); dedicated scrapers like Outscraper, Apify, and SerpApi are the most commonly used for actual lead lists; enrichment (emails/social) usually requires Outscraper, Scrap.io, or a second-step website scrape.
