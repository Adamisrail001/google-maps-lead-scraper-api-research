# Sum-up — Google Maps scraper API benchmark (2026-09-23)

1. Tested on identical workloads (2 industries × 10 NYC/LA areas): Lobstr, Apify, Outscraper, Google Places API (New), HasData (scale), Bright Data (scale), ScrapingDog (stage-1 smoke; scale needs $40 plan).
2. Personas defined from real evidence (`user-intent.md`): local-data extractor, lead-gen/outreach, developer — all roster decisions and verdicts are per persona.
3. ScrapingDog & Bright Data reinstated: no emails/socials (measured 0), but that's a persona-2-only need — both are strong persona-1 options (fills 89–100%).
4. Persona 2 (leads): **Lobstr leads on fill+richness** (59%/37% emails + socials, $5.82/1K); **HasData is the value challenger** — 42% emails at **$1.75/1K ($4.19/1K emails, ~3.3× cheaper)**, fastest scraper (~4–5 min/run), but no socials and some field wobble.
5. Persona 1 (listings): Bright Data (1,738 uniques, 0.2% errors, ~$1.50/1K est.) and Outscraper ($3.69/1K measured, richest schema) lead; ScrapingDog projects cheapest ($0.04–0.15/1K) pending scale run.
6. Apify: cheapest per row ($0.54/1K, verified-emails-only billing — proven) but silently truncated 4/20 queries via undocumented profit-guards; below our "recommend at scale" line.
7. **Persona-1 answer on the official API: NO, despite fine pricing (~$1.75/1K, $0 in free tier)** — 60-results/query hard cap (hit 10/10 restaurant queries) and Maps ToS §3.2.3 prohibits storing/copying business names & addresses (only place IDs storable). Compliant use = real-time in-app display only.
8. Google: best-engineered API tested (7.66/10 reference score, 1.54s median, 60/60 clean) — but formally **disqualified**: its own customer terms (§3.2.3) bar storing/exporting the data, on top of the 60/query cap and zero contact fields. Headline: "the best API in the test is disqualified by its own contract."
9. Total new spend today: HasData $4.29 (measured), Bright Data ~$2.61 (rate-card est., verify dashboard), Google $0 (free tier), ScrapingDog $0.
10. Deliverables in repo: `final-report.md`, `user-intent.md`, `knowledge.md` (updated), raw runs under `data/<tool>/` — github.com/Adamisrail001/google-maps-lead-scraper-api-research.
