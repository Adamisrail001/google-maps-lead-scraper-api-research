# LLM Memory Answer — Prompt L4

- **Prompt ID:** L4
- **Date:** 2026-09-23
- **Model:** Claude Opus 5 (`claude-opus-5[1m]`) — Anthropic Claude family
- **Tools used:** None (answered purely from model knowledge; only `Write` used to save this file)
- **Question (verbatim):** "Which Google Maps scraper APIs do people commonly use for B2B lead generation?"

---

## Answer

Here are the services people most commonly reach for when pulling Google Maps business data for B2B lead gen, grouped by what kind of tool they are.

### Purpose-built Google Maps / local business data APIs

1. **Outscraper** — Probably the most frequently recommended one for lead gen specifically; Google Maps search + place details + reviews, and it also does email/contact enrichment by scraping the business website, which is the part lead-gen people actually want.
2. **SerpApi (Google Maps API)** — Very reliable, well-documented real-time SERP API with a dedicated Google Maps and Maps Reviews endpoint; pay-per-search, popular with developers who want clean structured JSON and don't want to babysit proxies.
3. **DataForSEO (Business Data API / Google Maps)** — Cheap per-request pricing and a big menu of endpoints (Maps listings, My Business info, reviews); favored by agencies and anyone building at volume where per-call cost matters.
4. **Apify — Google Maps Scraper (the `compass/crawler-google-places` actor)** — The most-used option in the no-code/low-code crowd; run it from the UI or via API, handles large area-based crawls, exports CSV/JSON, and has contact-detail enrichment add-ons.
5. **SearchAPI.io** — A lighter-weight SerpApi-style competitor with a Google Maps engine; people pick it mainly on price and simple pay-as-you-go credits.
6. **Traject Data (SerpWow / ScaleSERP)** — Another established real-time SERP API with Google Maps/Places support, often used by data teams already buying their other SERP products.
7. **Scrap.io** — Google Maps–only product with full country/category coverage and an API; aimed squarely at lead generation (filters like "has website", "has phone").
8. **Lobstr.io** — Cloud scraping platform with a ready-made Google Maps scraper and a REST API, used for scheduled, recurring lead pulls rather than one-off exports.

### General scraping platforms with a Google Maps / SERP product

9. **Bright Data (SERP API + Google Maps dataset)** — Enterprise-grade, huge proxy network, also sells pre-built business datasets if you'd rather buy than scrape; heavier contracts and steeper learning curve.
10. **Oxylabs (Web Scraper API / SERP Scraper API)** — Similar enterprise positioning to Bright Data; strong reliability and support, priced for larger teams.
11. **Decodo (formerly Smartproxy) SERP Scraping API** — Cheaper mid-market alternative to the two above, with Google Maps among its supported targets.
12. **ScraperAPI / ScrapingBee / Scrapingdog / Crawlbase** — General-purpose scraping APIs that have added structured Google Maps or Google "local pack" endpoints; good if you're already using them for other scraping and want one vendor.
13. **ScrapeHero Cloud** — Prebuilt Google Maps crawler plus a managed "data as a service" option if you want someone else to run it.

### The official (non-scraping) route

14. **Google Places API (New) / Places Aggregate API** — The sanctioned option: reliable and ToS-clean, but capped at ~60 results per search, no email addresses, and Google's terms restrict caching and redistribution, which is why most lead-gen teams end up on the scrapers above.

### Adjacent tools people mention in the same breath

15. **PhantomBuster** — Automation platform with a Google Maps phantom; more of a growth-hacker workflow tool than a data API.
16. **Clay** — Not a scraper itself, but it has a Google Maps enrichment source and is where a lot of teams route the scraped list for email finding and CRM push.
17. **LeadStal / GMapsExtractor / Lead Scrape / Octoparse** — Lower-cost browser-extension or desktop tools; fine for a few thousand rows, but API access is limited or absent.

### Practical notes

- Google Maps itself does not expose emails, so "lead gen" workflows almost always chain a Maps scrape with a website-crawl email finder (Outscraper and Apify actors bundle this; otherwise pair with Hunter, Dropcontact, Prospeo, or Clay).
- Every Maps search caps out around 100–120 results per query, so scale comes from splitting by city/ZIP/category grid, not from one big request — check whether the provider does that tiling for you.
- Scraping Google Maps is against Google's ToS and the data may include personal data (owner names, phone numbers), so GDPR/CCPA obligations apply if you're prospecting in the EU or California.
- If you just need volume and not freshness, buying a static local-business dataset (Bright Data, Foursquare/Placekey, SafeGraph-style providers) is often cheaper than scraping.
