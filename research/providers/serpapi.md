# SerpApi — Verification

Verification date: 2026-09-23

## 1. Google Maps product
- Yes. "Google Maps API" — "Scrape Google Maps results automatically with SerpApi. Search for businesses and places in locations using GPS coordinates." (source: https://serpapi.com/google-maps-api, fetched 2026-09-23). It scrapes Google Maps SERP/local results, not Google Business Profile backend.

## 2. API
- Real API: yes — SerpApi is API-only (GET search endpoint returning JSON).
- Product URL: https://serpapi.com/google-maps-api
- API documentation URL: https://serpapi.com/google-maps-api (the product page is the API reference, with parameters and example JSON). Related: reviews/photos have separate SerpApi engines (not verified in this pass).

## 3. Authentication
- API key via `api_key` request parameter (source: https://serpapi.com/google-maps-api).
- Self-serve: yes — free plan exists ("Free Plan: 250 searches per month, $0", source: https://serpapi.com/pricing, fetched 2026-09-23).

## 4. Pricing
Source: https://serpapi.com/pricing, fetched 2026-09-23.
- Free: 250 searches/month, $0.
- Starter: $25/mo, 1,000 searches.
- Developer: $75/mo, 5,000 searches.
- Production: $150/mo, 15,000 searches.
- Big Data: $275/mo, 30,000 searches. Higher tiers to $2,750/mo (500,000) and enterprise tiers to $106,050/mo (54M).
- "Only successful searches are counted toward your monthly searches."
- Note: one search returns a page of local results (roughly 20 per page); per-business cost depends on results per search.

## 5. Lead-relevant fields
Source: example JSON on https://serpapi.com/google-maps-api, fetched 2026-09-23.
- Name: yes (`title`). Address: yes (`address`). Phone: yes (`phone`). Category: yes (`type`, `types`). Rating: yes (`rating`). Review count: yes (`reviews`). Coordinates: yes (`gps_coordinates.latitude/longitude`). Hours: yes (`operating_hours`). Also `price`, `open_state`, `service_options`, photo/review links.
- Website: not confirmed in the fetched excerpt (SerpApi local results commonly include a website field, but it was not captured in our fetch — unverified).
- Email extraction: absent — no email field in the documented response; no email enrichment product on the page.
- Social profiles: absent from documented response.

## 6. User intents served
- Google Maps scraping: yes.
- API automation: yes (pure API product).
- Large-scale extraction: plans to 500k+ searches/month.
- Lead generation: partial — business data only, no email/social contact extraction.
- Contact enrichment: no (absent in own docs).
