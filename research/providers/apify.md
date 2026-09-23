# Apify — Verification Record

**Verified:** live, 2026-09-21/22 (this project's testing phase — see `IMPORTANT/testing-plan.md`), re-confirmed in discovery 2026-09-23.

- **Google Maps product:** yes — marketplace of actors; most-surfaced in discovery: `compass/crawler-google-places` (appeared in 18/21 web queries and 2/5 Ahrefs SERPs); lead-gen-specific actor used in our benchmark: `themineworks/maps-leads` (resolved actor ID `B1byySkFdoSQ2DlW3`). Q03 ("google maps business leads api") returned 9/9 Apify actor results — the marketplace saturates lead-intent SERPs with many actors by different authors.
- **Real API:** yes — REST API v2 (`api.apify.com/v2`), runs + datasets endpoints. Docs: https://docs.apify.com/api/v2
- **Auth:** API token; self-serve. Account live-verified: `GET /v2/users/me` → `isPaying: true` (STARTER $29/mo).
- **Pricing (live-measured on themineworks/maps-leads):** PAY_PER_EVENT — $0.0016 per verified-email lead + $0.005 actor start. Only leads with verified email are billed (confirmed via per-record `charged` field). Known issues confirmed live: undocumented $0.25/run spend ceiling ("profit guard") and a per-query profitability breaker that can truncate low-email-yield queries; `business_status` returns "UNKNOWN" (bug).
- **Lead fields (smoke-tested live):** name, category, address, phone, website, rating, hours, coordinates, google_maps_url, email + email_status + all_emails. No photos/images field on this actor.
- **Intents served:** Google Maps scraping, lead generation, business data extraction, large-scale extraction, API automation, email extraction+verification.
- **Category: DIRECT competitor** (already in the benchmark).
