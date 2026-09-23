# Scrap.io — Verification

Verification date: 2026-09-23

## 1. Google Maps product
- Yes. Scrap.io extracts business data from "the three largest maps platforms": Google Maps, Apple Maps, Bing Maps (source: https://scrap.io/, fetched 2026-09-23). Google Maps is the primary dataset (Gmap Search API in docs).

## 2. API
- Real API: yes. "Automate your lead generation with the Scrap.io REST API. Search, filter and export business data programmatically." (source: https://scrap.io/).
- Product URL: https://scrap.io/
- API documentation URL: https://apidoc.scrap.io/ (fetched 2026-09-23). Base URL per docs: `https://scrap.io/api/v1/`. Endpoints: `GET /gmap/search`, `GET /gmap/place`, `GET /gmap/enrich`, `GET /gmap/types`, `GET /gmap/locations`. (Homepage marketing shows an example `GET /api/v2/map/search?...`; docs page documents v1 — version discrepancy noted, not reconciled.)

## 3. Authentication
- Bearer token in header: `Authorization: Bearer xxxxxxxxxx`; keys obtained via the account security dashboard (source: https://apidoc.scrap.io/).
- Rate limit: "The rate limit is 120 requests per minute." (source: https://apidoc.scrap.io/).
- Self-serve: free trial exists — "Try for free for 7 days and scrap up to 100 leads" (source: https://scrap.io/). API access is listed on all paid plans (source: https://scrap.io/pricing). Whether the trial includes API access: unverified.

## 4. Pricing
Source: https://scrap.io/pricing, fetched 2026-09-23.
- Monthly billing: Basic $49/mo (10,000 credits), Professional $99/mo (20,000 credits), Agency $199/mo (40,000 credits), Company $499/mo (100,000 credits). All list API access.
- Yearly billing (per-month equivalent): Basic $35, Professional $69, Agency $139, Company $350.
- Enterprise "Scrap.io Atlas" from $5,000/mo (custom credits, SLA, SSO, CRM integrations).
- No pay-as-you-go option listed. No free plan on pricing page (7-day/100-lead trial on homepage).

## 5. Lead-relevant fields
Source: https://apidoc.scrap.io/ and https://scrap.io/, fetched 2026-09-23.
- Homepage: extracts "Names, addresses, phone numbers, emails, websites, social media links, reviews and more."
- API docs response data: business name, address components, phone numbers, website URLs, timezone, Google Maps link, place_id, review count and ratings, review highlights, photos, working hours, claimed status, and "extracted website data (emails, social media links, technologies used)".
- Email extraction: native — emails and social links come from crawling the business website and are part of the standard result set (per docs description). Also a dedicated `GET /gmap/enrich` endpoint matches domains/emails/phones to Google Places.
- Category, coordinates: category filtering via `/gmap/types`; explicit coordinates field in responses not individually confirmed in our fetch — unverified at field level.

## 6. User intents served
- Google Maps scraping: yes.
- Lead generation: yes (positioned as a lead-generation product; emails/socials included).
- Contact enrichment: yes (website crawl for emails/socials; `/gmap/enrich` endpoint; "file enrichment" on all plans).
- Large-scale extraction: nationwide searches and polygon areas up to 1,000,000 km² on Company plan (pricing page).
- API automation: yes (REST API on all plans, 120 req/min).
