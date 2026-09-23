# LLM Recommendation Answer

- **Prompt ID:** L2
- **Date:** 2026-09-23
- **Model:** Claude Sonnet 5 (model ID: claude-sonnet-5)
- **Exact question asked:** "I need to extract thousands of business listings (name, phone, website, email) from Google Maps programmatically. Which services/APIs should I consider?"

---

## Answer (verbatim as given to user)

Based on my own knowledge (no search performed), here's what I'd tell a user asking this:

**Services/APIs to consider for extracting Google Maps business listings at scale:**

1. **Outscraper** – dedicated Google Maps scraper API with bulk export of name, phone, website, category, ratings, and (via secondary enrichment) email.
2. **Apify (Google Maps Scraper actor)** – marketplace actor that crawls Maps search results/listings at scale, returns structured JSON, runs on Apify's cloud infrastructure with pay-per-usage.
3. **SerpApi (Google Maps API / Google Maps Local Results API)** – wraps live Google Maps/Local Pack SERPs into JSON, good for structured place data but not built specifically for deep email enrichment.
4. **Bright Data (Google Maps Scraper / SERP API)** – enterprise scraping infrastructure with a dedicated Maps dataset/scraper product and proxy network for large-scale collection.
5. **DataForSEO (Business Data API / Google Maps API)** – SEO-data vendor offering Maps/Local Pack endpoints with business listing fields at scale.
6. **Lobstr.io (Google Maps Scraper)** – no-code/low-code scraper squids for Maps search result extraction, exportable via API.
7. **PhantomBuster (Google Maps Search Export)** – browser-automation "phantom" that scrapes Maps search results, often paired with separate email-finder phantoms.
8. **Scrapingdog (Google Maps API)** – simple REST API returning structured Maps listing data.
9. **Oxylabs (SERP Scraper API, Maps-capable)** – proxy/scraping infrastructure vendor with Maps/Local support as part of its SERP scraping product.
10. **Crawlbase (Maps Scraper API)** – API-based scraper for Maps listings with pay-as-you-go pricing.
11. **Google Places API / Google My Business API (official)** – the legitimate, ToS-compliant source of business data, but it is rate-limited, priced per field/request, and does not return email addresses (and often not verified phone/website beyond what's public).
12. **Octoparse** – general-purpose no-code scraper with pre-built Google Maps templates, more suited to smaller/manual batch jobs.

**Important caveat I'd flag:** Google Maps listings themselves don't natively include email addresses — any tool claiming to return "email" is doing secondary enrichment (crawling the business's website, WHOIS, or third-party contact databases), which adds a separate accuracy/legality dimension worth testing independently from the core Maps extraction.
</content>
