# Scrapingdog — Verification

Verification date: 2026-09-23

## 1. Google Maps product
- Yes. "Google Maps Scraper API" / "Google Maps API" — extracts business/location data from Google Maps search results (source: https://www.scrapingdog.com/google-maps-api/, fetched 2026-09-23).
- Related endpoints per docs index: Google Maps Search, Places, Reviews, Photos, Posts APIs (source: docs index at https://docs.scrapingdog.com/, surfaced via domain search 2026-09-23).

## 2. API
- Real API: yes. Endpoint `https://api.scrapingdog.com/google_maps` (source: https://www.scrapingdog.com/documentation/google-maps-api/, fetched 2026-09-23).
- Product URL: https://www.scrapingdog.com/google-maps-api/
- API documentation URL: https://www.scrapingdog.com/documentation/google-maps-api/ (docs.scrapingdog.com/google-maps-scraping-api-documentation 301-redirects here).

## 3. Authentication
- API key passed as `api_key` query parameter; "Your personal API key. Available on your dashboard" (source: documentation page above).
- Self-serve: yes — "Every account starts with 200 free credits and full access to all APIs, no credit card required" (source: https://www.scrapingdog.com/pricing/, fetched 2026-09-23).

## 4. Pricing
- Credit-based subscription (source: https://www.scrapingdog.com/pricing/, fetched 2026-09-23):
  - Free: $0, 200 credits.
  - Lite: $40/mo, 200,000 credits.
  - Standard: $90/mo, 1,000,000 credits.
  - Pro: $200/mo, 3,000,000 credits.
  - Premium: $350/mo, 6,000,000 credits. (Tiers continue up to $30,000/mo.)
- Google Maps API cost: "Google Maps API 5 credits / req" (same pricing page).
- "Failed requests never charged" (same page). Annual billing ≈ two months free.

## 5. Lead-relevant fields
Source: https://www.scrapingdog.com/documentation/google-maps-api/ sample response, fetched 2026-09-23.
- Name: yes (`title`). Address: yes. Phone: yes. Website: yes. Category/type: yes (`type`, `types`). Rating: yes. Review count: yes (`reviews`). Coordinates: yes (`gps_coordinates`). Hours: yes (`operating_hours` by day). Also `place_id`, `data_id`, price range, thumbnail, reviews/photos/posts links.
- Email extraction: absent — no email field in documented response; no email enrichment product found in the Google Maps docs.
- Social profiles: absent from documented response fields.

## 6. User intents served
- Google Maps scraping: yes.
- API automation: yes (single-endpoint REST API, JSON).
- Large-scale extraction: credit plans to millions of requests; pagination by 20 results/page (docs).
- Lead generation: partial — returns phone/website but no email/social extraction.
- Contact enrichment: no (unverified/absent in own docs).
