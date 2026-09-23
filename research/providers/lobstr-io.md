# Lobstr.io — Verification Record (house product — conflict of interest disclosed)

**Verified:** live, 2026-09-21/22 (this project's testing phase — see `IMPORTANT/testing-plan.md`).

- **Google Maps product:** yes — Google Maps Leads Scraper (crawler `4734d096159ef05210e0e1677e8be823`), purpose-built for lead generation.
- **Real API:** yes — REST API v1 (`api.lobstr.io/v1`): squids, tasks, runs, results endpoints. Docs: https://docs.lobstr.io — plus Python SDK, CLI, dashboard, MCP server.
- **Auth:** API key; self-serve. Account live-verified (93 crawlers on account).
- **Pricing:** credit-based — 1 credit/row, 2 credits/email (per crawler catalog); email *verification* is a separate dashboard action (100 credits/valid-or-unknown email) with no documented API endpoint (load-bearing distinction — see testing-plan Section 7).
- **Lead fields (live-tested):** name, category, address, phone, website, rating, review count, coordinates, hours, business details, images, email extraction (extraction-only via API). Input is a coordinate-anchored Google Maps search URL (max 200 results/task — Google's own per-search ceiling).
- **Intents served:** Google Maps scraping, lead generation, business data extraction, large-scale extraction, API automation, email extraction.
- **Discovery visibility (2026-09-23):** 4/5 LLM samples recommended it unprompted; appeared on the email-extraction web query (Q20, position 2) and in 1 fetched listicle (LocalProspects' 10-API comparison); 0/5 Ahrefs stored SERPs; 0/8 Reddit threads. Ahrefs domain: DR 50, ~1.0K organic traffic/mo — smallest domain footprint among the direct candidates.
- **Category: DIRECT competitor** (house product — the article's subject; conflict disclosed).
