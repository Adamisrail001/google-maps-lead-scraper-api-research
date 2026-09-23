# HasData — Verification

Verification date: 2026-09-23

**Access note:** hasdata.com apex domain timed out (DNS) from our research environment on 2026-09-23; docs.hasdata.com and the pricing page fetched successfully. Product-page facts marked accordingly.

## 1. Google Maps product
- Yes. Two relevant products: "Google Maps Scraper" (no-code + async jobs API, https://hasdata.com/scrapers/google-maps) and "Google Maps Search API" (real-time JSON API, https://hasdata.com/apis/google-maps-search-api). Also Google Maps Reviews API and Photos API. (Sources: domain-restricted search results listing these hasdata.com pages, 2026-09-23; docs fetched directly.)

## 2. API
- Real API: yes.
  - Scraper jobs API: `POST https://api.hasdata.com/scrapers/google-maps/jobs` — async, returns `jobId`, results polled or delivered by webhook (source: https://docs.hasdata.com/scrapers/google-maps, fetched 2026-09-23).
  - Product URL: https://hasdata.com/apis/google-maps-search-api (direct fetch failed; page existence verified via domain-restricted search).
  - API documentation URL: https://docs.hasdata.com/scrapers/google-maps (fetched); docs root https://docs.hasdata.com/.

## 3. Authentication
- API key in `x-api-key` header (source: https://docs.hasdata.com/scrapers/google-maps).
- Self-serve: yes — "1,000 credits every month with access to every tool. No credit card required." (source: https://hasdata.com/pricing, fetched 2026-09-23).

## 4. Pricing
Source: https://hasdata.com/pricing, fetched 2026-09-23.
- Free: $0, 1,000 credits/mo, 1 concurrent request.
- Startup: $49/mo, 200,000 credits, 5 concurrent.
- Basic: $99/mo, 1,000,000 credits, 15 concurrent.
- Growth: $208/mo, 3,000,000 credits, 50 concurrent.
- Enterprise: custom above 20M credits/mo.
- Google Maps APIs: $1.23 per 1,000 requests on Startup; $0.50/1,000 on Basic; $0.35/1,000 on Growth (pricing page table).
- Credit costs (docs, Google Maps scraper): "Each row of data returned consumes 3 credits"; email extraction 10 credits per row; enrichments (email, LinkedIn, social profiles, revenue, traffic, funding, founded year) 5 credits each (source: https://docs.hasdata.com/scrapers/google-maps).
- Free 1,000 credits "equals 333 Google Maps places" (source: hasdata.com Google Maps scraper page via domain-restricted search snippet).

## 5. Lead-relevant fields
Source: https://docs.hasdata.com/scrapers/google-maps, fetched 2026-09-23.
- Name: yes (title). Address: yes. Phone: yes. Website: yes. Category: yes (type). Rating: yes. Review count: yes. Coordinates: yes (latitude/longitude). Hours: yes (working hours). Also description, price level, service options, place/data IDs.
- Email extraction: native option — `extractEmails` boolean parameter on the scraper job; costs 10 credits per row (add-on cost within same API).
- Social/other enrichment: available as enrichments (email, LinkedIn, social profiles, revenue, traffic, funding, founded year) at 5 credits each (docs).
- Note: the real-time Google Maps Search API (SERP-style) field list mirrors the above minus emails; email extraction is documented on the scraper jobs API. Exact Search API sample JSON: unverified (page fetch failed).

## 6. User intents served
- Google Maps scraping: yes (scraper jobs API + real-time search API + no-code UI).
- Lead generation: yes (emails + enrichment fields; lead-gen positioning in their content).
- Contact enrichment: yes (extractEmails, LinkedIn/social enrichments).
- Large-scale extraction: async jobs with `limit: 0 = unlimited`, webhooks, plans to 3M+ credits.
- API automation: yes (REST, x-api-key, webhooks).
