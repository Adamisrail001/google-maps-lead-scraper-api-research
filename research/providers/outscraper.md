# Outscraper — Verification

Verification date: 2026-09-23

**Access note:** outscraper.com and app.outscraper.com were unreachable from our research environment on 2026-09-23 (connection refused / DNS timeout on repeated attempts). Facts below were verified via Outscraper's own official PyPI package page and Google-indexed snippets of outscraper.com pages restricted to their domain. Items that required loading the live site directly are marked unverified.

## 1. Google Maps product
- Yes. Products: "Google Maps Scraper" (https://outscraper.com/google-maps-scraper/) and "Google Maps Places API" (https://outscraper.com/google-maps-api/). Both pages surfaced in domain-restricted search on 2026-09-23; page bodies not directly fetched (site unreachable).

## 2. API
- Real API: yes. Official Python client `outscraper` on PyPI wraps the Outscraper API with methods `google_maps_search()`, `google_maps_reviews()`, `emails_and_contacts()` (source: https://pypi.org/project/outscraper/, fetched 2026-09-23).
- Product URL: https://outscraper.com/google-maps-api/
- API documentation URL: https://app.outscraper.com/api-docs (referenced from the PyPI page; direct fetch failed — content unverified from this environment).

## 3. Authentication
- API key: `OutscraperClient(api_key='SECRET_API_KEY')`; keys created at https://app.outscraper.com/profile (source: https://pypi.org/project/outscraper/).
- Self-serve: key creation is via the app profile page per PyPI docs. Free-tier records suggest self-serve access ("Google Maps Scraper - Free Tier" page title, https://outscraper.com/google-maps-scraper/). Exact signup flow unverified (site unreachable).

## 4. Pricing
- Pay-as-you-go, tiered (source: Google-indexed snippets of https://outscraper.com/pricing/ and https://outscraper.com/outscraper-pricing-explained/, retrieved 2026-09-23):
  - Google Maps data: first 500 records free; then $3 per 1,000 records ("Medium Tier", next 99,500); $1 per 1,000 above 100,000 records ("Business Tier").
  - Emails & Contacts Scraper: $0.003 per record ($3 per 1,000).
  - Enrichment is optional and billed separately from the base Google Maps scrape (source snippet: https://outscraper.com/google-maps-scraper-pricing-enrichment-cost/).
- Exact current pricing page contents unverified directly (https://outscraper.com/pricing/ unreachable).

## 5. Lead-relevant fields
- Emails/socials: `emails_and_contacts()` method returns "emails, phones, socials" (source: https://pypi.org/project/outscraper/). Email extraction is a separate, natively offered enrichment service (Emails & Contacts Scraper), billed separately from the Maps scrape.
- Business name, address, phone, website, category, rating, review count, coordinates, hours: unverified field-by-field from this environment (API docs unreachable). The products are described as Google Maps business data extraction; exact response schema not captured.

## 6. User intents served
- Google Maps scraping: yes (product pages).
- Lead generation: yes (Emails & Contacts enrichment; "Boost Your Leads" content on their domain).
- Large-scale extraction: pricing tiers up to and beyond 100,000 records indicate volume use (pricing snippets).
- API automation: yes (REST API + official Python client).
- Contact enrichment: yes (Emails & Contacts Scraper, $3/1,000).
