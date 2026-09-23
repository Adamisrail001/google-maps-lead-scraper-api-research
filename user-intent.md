# Who Uses a Google Maps Scraper API — and Why

**Date:** 2026-09-23. Evidence sources: 31-probe discovery research (`research/`) — 21 Google-intent queries with Ahrefs volumes and stored SERPs, 8 fully-read Reddit threads (self-promo flagged per mention), 5 LLM-recommendation samples, 8 comparison listicles — plus Google's own Maps Platform terms. Signals not available in this environment: Search Console for the site, serper.dev (recorded as unavailable, not substituted with guesses).

## The demand picture

US search demand concentrates on generic extraction terms, not lead terms: "google maps scraper" 1,800/mo vs "google maps lead scraper" 80/mo (Ahrefs, 2026-09-23). But community evidence splits clearly into distinct jobs — and in 8 of 8 Reddit threads read, the trigger for the search was the official Places API's limits (cost at scale, missing fields, result caps). Personas below are ordered by strength of *genuine* (non-self-promo) evidence.

## Persona 1 — Local-data extractor

**Who:** analyst, agency producing local-market datasets, SMB owner mapping a territory, local-SEO/GBP auditor.
**Job:** *every* listing matching "«category» in «area»" — complete, exportable, repeatable.
**Needs:** name, address, phone, website, opening hours, rating + review count, category, coordinates. **Does NOT need emails or socials.**
**Volume:** hundreds–20,000 listings per project. **Budget: highly price-sensitive** — this buyer compares $/1,000 listings directly.
**Best evidence in our data:** the r/webscraping user who scraped an entire town — paid Outscraper $50 for 20,000 listings, wanted listings not contacts, still recommending it two years later. The recurring Places-API cost complaints (8/8 threads) are mostly this persona.
**Why not the official API:** 60-results/query ceiling (measured: 10/10 restaurant queries capped), grid-engineering burden for coverage, and — decisive — Maps Platform Terms §3.2.3 prohibits "copying and saving business names, addresses, or user reviews": the *stored, exportable list* this persona exists to produce is contractually disallowed.

## Persona 2 — Lead-gen / outreach builder

**Who:** agency owner, SDR, growth freelancer building cold-outreach lists.
**Job:** contactable leads from Maps categories.
**Needs:** persona-1 fields **plus emails (first), social profiles, decision-maker hints**. Enrichment fill-rate is the KPI; willing to pay multiples more per lead.
**Volume:** 500–10,000 leads/campaign. **Budget: moderate sensitivity** — judged in $/qualified lead, not $/listing.
**Evidence:** the "lead scraper"/"extract emails from google maps" query cluster (real but smaller volume); r/Entrepreneur's tool thread (145 answers — heavily astroturfed, itself evidence of commercial demand); every LLM sample for lead-phrased prompts recommends email-capable tools.
**Key technical fact this persona must understand:** emails/socials are NOT Google Maps listing data — every provider that returns them crawls the business's *website* as an enrichment step. This is a different product layer, priced accordingly (Lobstr 2 credits/email; HasData ~2.6× base row cost; Outscraper +$3/1K stage; Apify bills only verified-email rows).

## Persona 3 — Developer building a product

**Who:** engineer embedding local-business data in an app/SaaS.
**Job:** programmatic, stable access at 10k–100k listings/month.
**Needs:** stable schema, pagination, documented rate limits, SDKs, async/webhooks, predictable pricing; fields per their app (usually persona-1 set).
**Budget:** predictability > absolute price.
**Evidence:** r/reactnative "free alternative to google places api" thread (the #1 Ahrefs result for that query); the POI-API cluster (Geoapify/Radar/SafeGraph) surfacing on "alternative" phrasing — different products competing for this persona's *display* use case.
**Split decision:** if data is displayed live in-app → the official API is the compliant, well-engineered answer (7.66/10 as an API in our test; 1.54s median). If data is stored/served from their own DB → same §3.2.3 wall as persona 1, and scraper APIs with stable schemas + async patterns compete.

## Consequences for the tool roster (the rule)

**No tool is disqualified for lacking a field a persona doesn't need.** Concretely: ScrapingDog and Bright Data — eliminated earlier for lacking emails/socials — are reinstated as persona-1/3 contenders (their smoke tests showed exactly persona-1 strengths: 95–100% NAP fills). Contact-capable tools (Lobstr, HasData, Apify, Outscraper+enrichment, Scrap.io) compete for persona 2. The official API competes for persona 3's display case and is scored, with the ToS finding attached, for personas 1–2. Every scoring table in the final report is broken down by persona.
