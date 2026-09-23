# Google Maps Business Data: Official Places API vs Scraper APIs — Research Report

**Research dates:** discovery 2026-09-23 · benchmark runs 2026-09-22/23
**Disclosure:** this research is owned by Lobstr.io, whose Google Maps Leads Scraper is one of the evaluated products. All measurements are reproducible from the raw evidence in this repository.

---

## 1. The decision this report answers

You want business data out of Google Maps — for a lead list, a dataset, or a product. The real question is not "which tool is best" but **"should I use Google's official Places API or a scraper API — and which one for my job?"**

Short answer, from measured runs on identical workloads (20 sub-area queries, 2 industries, NYC + LA):

- **If you need emails or social profiles, the official API is out** — those fields do not exist in its response surface at any price. Scrapers with contact enrichment (Lobstr, Apify, Outscraper's add-on stage) are the only API route.
- **If you need thousands of records per search area, the official API fights you** — a hard 60-results-per-query cap (measured: all 10 restaurant queries stopped at exactly 60) vs 998–1,405 uniques the scrapers pulled from the same 10 queries.
- **If you need accurate core business data (phone, website, rating, hours) in modest volumes, the official API is excellent** — highest fill-rates we measured (94–98%), fastest responses (median 1.54s), 1,000 free enterprise-tier calls/month, zero ToS ambiguity.

The rest of this report is the evidence: who the real contenders are (§2), what we measured (§3), which tool fits which job (§4), where the official API wins and loses (§5), why other tools were set aside (§6), and how the research was done (§7).

## 2. The contenders

**Tested with live runs on the identical workload** (2 runs × 10 sub-area queries; raw outputs in `data/` and `research/raw/google-places-api/`):

| Provider | Product | Run evidence |
|---|---|---|
| **Google Places API (New)** | Text Search, Enterprise+Atmosphere field mask | 60 requests, 1,044 uniques, $0 billed (free tier) |
| **Lobstr.io** (house product) | Google Maps Leads Scraper | 998 uniques (Run 1), emails + socials native |
| **Apify** | `themineworks/maps-leads` actor | 1,405 uniques (Run 1), pay-per-verified-email-lead |
| **Outscraper** | Google Maps Scraper (base stage) | 512 uniques (Run 1, 80/query budget cap) |

**Verified but not yet run** (API, auth, pricing and fields confirmed against vendor docs — `research/providers/`): **Scrapingdog** (Maps API, from $40/mo, no email fields) and **Bright Data** (Maps scraper API, ~$0.75–1.50/1K records per third-party sources; its site was unreachable from our test network on 2026-09-23, so pricing and a live run are unconfirmed). Both earned their slot through discovery frequency (§7); their rows in the matrix below are docs-based and labeled.

These six were selected by measured user-discovery frequency across 31 search/community/LLM probes — not by feature similarity (method and full numbers in §7).

## 3. What we measured

### 3.1 Field coverage (measured fill-rates on unique results; docs-verified where marked)

| Field | Google (1,044) | Lobstr (998) | Apify (1,405) | Outscraper (512) | Scrapingdog* | Bright Data* |
|---|---:|---:|---:|---:|---|---|
| Name / address / coordinates | 100% | 100% | 100% | 100% | ✓ | ✓ |
| Phone | **95%** | 91% | 90% | 91% | ✓ | ✓ |
| Website | 94% | 93% | 83% | 94% | ✓ | ✓ |
| Rating + review count | **98%** | 86% | 67% | ✓ | ✓ | ✓ |
| Opening hours | **98%** | 90% | 83% | ✓ | ✓ | ✓ |
| Photos/images | 95% (refs, media billed separately) | 81% | — (absent) | **99%** | ✗ | ✓ |
| **Email** | **— absent from API** | **59%** | 32% (verified, only these billed) | paid add-on stage ($3/1K), not run | ✗ | not indicated |
| **Social profiles** | **— absent from API** | ~48–54% (FB/IG/LinkedIn/…) | — | via add-on stage | ✗ | unverified |
| Review texts | max 5/place (hard cap) | score histograms + tags | — | ✓ (histograms, posts) | ✓ | ✓ |
| Owner info / popular times | — absent | ✓ | — | ✓ | ✗ | unverified |

\* docs-verified only, not tested. Full per-provider records: `research/providers/`.

### 3.2 Volume (same 10 Run-1 queries, unique results)

Google 444 · Lobstr 998 · Apify 1,405 · Outscraper 512 (80/query budget cap). Google's ceiling is structural: 20 results/page, 3 pages max per text query — reaching scraper-scale volume requires ~3–4× more, finer-grained queries (~90–120 billed requests for ~1,400 uniques), with rising cross-query overlap (6.8% dupes already at 10 sub-areas).

### 3.3 Speed (Google, measured; both runs)

97.0s wall-clock for 60 requests / 1,120 raw places; latency median 1.54s, p95 2.26s, max 2.67s, zero errors. Scraper wall-clocks are async batch runs measured separately in the benchmark analysis phase (`data/<provider>/`); they trade latency for volume and enrichment.

### 3.4 Cost per 1,000 unique businesses (calculations in `research/analysis/google-places-api-cost-speed.md`)

| Provider | Measured basis | Effective cost |
|---|---|---|
| Google Places API | 60 req × $40/1K (Enterprise+Atmosphere, live rate) → 1,044 uniques | **$0 within 1,000 free req/mo (~18.7K places); $2.30/1K after** — no emails/socials at any price |
| Apify | 451 verified-email leads billed × $0.0016 + starts | ~$0.65/1K uniques returned — but you pay per *verified email*, so cost concentrates on the 32% enriched |
| Outscraper | $3/1K base records, 800 requested → 512 uniques | ~$4.69/1K uniques (listings only; email stage +$3/1K, verification +$3/1K) |
| Lobstr | 1 credit/row + 2 credits/extracted email | credit→$ conversion at plan rate — pending in benchmark analysis |

## 4. Which tool for which job

**Intent 1 — Build a B2B lead list with contact details for outreach.**
The official API cannot do this job: no email, no social fields (§3.1). On measured data: **Lobstr** delivered contacts broadest (59% emails, ~50% socials, in one pass); **Apify** delivered fewer emails (32%) but DNS/MX-verified and only charges for those — attractive when you pay strictly for usable outreach rows; **Outscraper** needs its extra $3/1K stages (untested here). Docs-verified alternative with native emails: Scrap.io (`research/providers/scrap-io.md`).

**Intent 2 — Bulk-extract thousands of businesses for a dataset.**
**Apify** produced the most uniques on the same queries (1,405); **Outscraper** has the richest default listing schema (photos 99%, popular times, histograms); **Google** is viable only if you accept query-engineering against the 60-cap — its per-record rate ($2.30/1K, or $0 inside the free ~18.7K places/mo) is actually competitive, but each extra query buys ≤60 records with growing overlap.

**Intent 3 — Replace or cut the cost of the Places API inside a product.**
Stay on **Google** if your product needs phone/website/rating/hours at ≤1,000 enterprise calls/mo — that's now free, fresh, and fastest (1.54s median). Beyond it, per-request pricing is the pain scrapers exploit: **Scrapingdog** (real-time API, from $40/mo) and SerpApi-style per-search products are the drop-in-shaped alternatives, but check §3.1 — neither adds fields Google lacks; they compete on price and caps, not data depth.

**Intent 4 — Enrich existing records (emails, socials, reviews).**
**Lobstr** (emails+socials in-run) and **Outscraper** (dedicated enrichment/verification services) are built for this; **Apify** verifies inline. **Google** enriches only its own field set — good for refreshing phone/hours/rating (94–98% fill), a dead end for contacts, and reviews are capped at 5/place.

**Intent 5 — Monitor a category or competitors over time.**
Recurring cost dominates. **Google's** 1,000 free enterprise calls/mo cover a ~300-listing watchlist re-checked monthly at $0 with first-party freshness. At larger scale, per-record scrapers win: Apify's pay-per-verified-lead suits contact monitoring; Lobstr squids and Outscraper requests can be scheduled. (No provider was tested for longitudinal reliability — single-window runs only.)

## 5. Official Google Places API — where it wins and loses (measured)

**Wins:** best fill-rates of anything tested for phone (95%), website (94%), rating and hours (98%); fastest responses in the project; 1,000 free Enterprise+Atmosphere requests/month (≈18,700 places); structured, stable schema; no ToS ambiguity.
**Loses:** emails, social profiles, contact forms, owner data, popular times — **absent from the API surface entirely**, which disqualifies it from outreach lead generation, the highest-intent job in this market; hard 60-results-per-query cap (measured at the ceiling on 10/10 restaurant queries); 5-review cap; photo media billed separately; volume beyond the free tier costs per-request, and the request count — not the record count — is what the 60-cap inflates.

## 6. Tools considered and set aside — in terms that matter to a buyer

- **SerpApi** — no email/social fields, and ~20 results per billed search makes list-building cost balloon with volume; strong choice only for SERP-style position data. Reconsidered rather than category-excluded: it lost on missing contact fields and per-search economics, not on being "a SERP API".
- **Oxylabs / ScraperAPI** — usable Maps coverage inside general scraping platforms, but no contact enrichment and no lead-list tooling; ScraperAPI's site was also unreachable from our network during verification (access risk we could not clear).
- **PhantomBuster** — has Maps + email phantoms, but execution-time pricing means the cost of 1,000 records cannot be computed before running — disqualifying for budget-planned extraction.
- **Octoparse** — real Maps + email templates at low prices, but a desktop/no-code workflow; its API orchestrates the UI product rather than returning Maps data directly.
- **DataForSEO** — clean business-data API at $1.50/1K profiles, but no email/social fields; fits SEO/reputation pipelines, not outreach.
- **HasData, G Maps Extractor, Scrap.io** — verified as real email-capable Maps APIs (`research/providers/`); not yet run. Strongest candidates for the next benchmark round.
- **Geoapify, SafeGraph, TravelTime, Radar** — POI/geodata for mapping features, no business-contact data.
- **gosom, Omkar Cloud (open source)** — free self-hosted scrapers for engineering teams; no SLA, you operate the proxies — out of scope for a managed-API comparison.
- **~25 tools surfaced only via flagged Reddit self-promo** (G-Business Extractor, LeadStal, LocalProspects, …) — no independent evidence a real buyer uses them; several have no API at all. Full list: `research/analysis/categorization.md`.
- **OpenWeb Ninja / QuantumProxies** — key-subscription failure (live 403) / 500-lead-per-run technical cap, respectively.

## 7. How the providers were chosen (discovery evidence)

31 probes on 2026-09-23 — 21 web queries across 4 intent groups, 5 Reddit queries, 5 LLM prompts — against 6 source types (Ahrefs stored Google SERPs, live web search, 8 fetched comparison articles, 8 fully-read Reddit threads with self-promo flagging, LLM sampling on 4 models, Ahrefs domain/keyword data). Appearance counts (of 21 web queries): Apify 18, Outscraper 16, gosom 8, G Maps Extractor 8, Bright Data 5, Scrapingdog 5, Scrap.io 5; LLM samples (of 5): Apify/SerpApi/Bright Data 5, Outscraper/DataForSEO/Scrapingdog/Lobstr 4. The official Places API appeared in 8/8 Reddit threads — recommended for small jobs, criticized on cost and caps at scale, which is precisely what §3 quantified. Roughly half of all Reddit mentions were flagged self-promo. Full tables: `research/analysis/provider-frequency.md`; raw evidence: `research/discovery/`, `research/reddit/`, `research/llm/`, `research/ahrefs/`.

**Wording discipline:** "most frequently surfaced across our probes" — not "most popular globally". Frequency shows what buyers encounter; §3's measurements show what the products deliver. The two are kept separate throughout.
