# Prompt ID: L5

**Date:** 2026-09-23
**Model:** Claude Sonnet 5 (Anthropic)
**Exact question asked:** "I want an API that returns Google Maps businesses with contact details for lead gen. What are my options?"

---

## Answer

Here are the main options for pulling Google Maps business data (with contact details like phone/website) via API for lead generation:

**Official / Google-backed**
- **Google Places API (New) / Google Maps Platform** – The official source; returns name, address, phone, website, ratings, hours, and coordinates, but has strict ToS around storage/lead-gen use, per-request pricing, and no bulk "scrape by category+area" search built in.

**Scraping-focused APIs (Google Maps specific)**
- **Outscraper** – Popular dedicated Google Maps Scraper API; returns business name, phone, website, category, rating, reviews, and often emails/social links via enrichment add-ons; pay-as-you-go pricing.
- **SerpApi (Google Maps API / Google Local Results API)** – Structured JSON from Google Maps/Local Pack searches, including phone and website fields; good for smaller-to-medium volume, priced per search.
- **DataForSEO (Business Data API / Google My Business API)** – SEO-data company offering Google Maps/GBP endpoints with contact fields, aimed more at agencies but usable for lead lists.
- **Apify (Google Maps Scraper actor)** – Marketplace "actor" with a REST API wrapper; returns detailed business profiles including phone, website, and sometimes email enrichment; usage-based pricing on the Apify platform.
- **Bright Data (Google Maps Scraper API / Web Scraper IDE)** – Enterprise-grade scraping infrastructure with a Google Maps dataset/API option; robust but pricier and more infra-oriented.
- **Scrapingdog (Google Maps Scraper API)** – Simpler/cheaper alternative returning similar structured fields (name, phone, address, website).
- **Lobstr.io (Google Maps Leads Scraper)** – No-code/API scraper built specifically for Maps lead generation, exporting name, phone, website, category, and address at scale.

**Adjacent / enrichment-oriented (not Maps-native, but often paired for lead gen)**
- **Apollo.io / Clearbit / Hunter.io** – Not Google Maps scrapers themselves, but commonly used afterward to enrich scraped businesses with verified emails and firmographic data.

**Practical note:** Most of these differ mainly in (1) how deep the enrichment goes (does it find emails/socials beyond what Google Maps shows natively), (2) rate limits/scale for bulk area+category searches, and (3) pricing model (per-request vs. per-record vs. subscription). None of them guarantee email addresses since Google Maps listings themselves rarely expose email — that typically requires a secondary enrichment step or website-scraping add-on.

---

*This answer was generated purely from the model's internal knowledge, without any web search, browsing, or external tool use.*
