# G Maps Extractor — Verification

Verification date: 2026-09-23

## 1. Google Maps product
- Yes. G Maps Extractor collects "publicly available business listing data" from Google Maps in three forms: Chrome extension, cloud web app, and API (source: https://gmapsextractor.com/, fetched 2026-09-23).

## 2. API
- Real API: yes — "Google Maps Scraper API" plus "Google Maps Reviews Scraper API" and "Google Maps Photos Scraper API" (source: https://gmapsextractor.com/).
- Product URL: https://gmapsextractor.com/google-maps-scraper-api
- API documentation URL: https://documenter.getpostman.com/view/2218135/2s9YymJRMi (linked from the product page as the API reference). The Postman page did not render in our fetch (JavaScript-heavy), so endpoint paths, base URL, and request schemas are unverified from this environment.

## 3. Authentication
- Method: unverified. The product page references the dashboard (/dashboard/api) for getting started but does not state the auth scheme; the Postman documentation could not be rendered.
- Self-serve: yes — "1,000 free credits/month", "No credit card required" (homepage); API Free plan of 20 requests/month exists on the pricing page.

## 4. Pricing
Source: https://gmapsextractor.com/pricing, fetched 2026-09-23.
- API plans: Free $0 (20 requests/mo); Basic $15/mo (1,000 requests, $0.014/req); Professional $65/mo (5,000, $0.012/req); Business $115/mo (10,000, $0.011/req); Scale $365/mo (50,000, $0.009/req); Enterprise custom.
- Online (cloud) scraper plans: Free $0 (1,000 records/mo); Lite $19/mo (20,000); Basic $49/mo (80,000); Growth $99/mo (250,000); Professional $149/mo (500,000); Enterprise custom.
- Chrome extension plans: Free $0 (1,000 records/mo); Professional $39/mo (100,000); Business $99/mo (500,000).
- "No separate charges" for email/social extraction — included in all subscription tiers (pricing page).

## 5. Lead-relevant fields
Source: https://gmapsextractor.com/ and /google-maps-scraper-api, fetched 2026-09-23.
- Homepage: business names, addresses, phone numbers, websites, categories, ratings, reviews, photos, coordinates, opening hours, emails, and "social media profile URLs found from the internet (Facebook, Instagram, LinkedIn, Youtube, Yelp, Twitter/X, TikTok, and so on)".
- API page: results include "name, phone, domain, categories, reviews count, emails, social medias, place id, rating, addresses, and more".
- Email extraction: native — emails and socials are part of standard output at no extra charge (pricing page: included in all tiers).
- Field-level sample JSON: unverified (Postman docs not renderable here).

## 6. User intents served
- Google Maps scraping: yes (extension, cloud app, API).
- Lead generation: yes (emails + socials in output).
- Contact enrichment: yes, bundled (socials "found from the internet").
- Large-scale extraction: cloud plans to 500,000 records/mo; API plans to 50,000 requests/mo.
- API automation: yes, though API request volumes are lower-tiered than the cloud app record volumes.
