# Google Maps Leads API Benchmark — Testing Plan (FINAL)

> Companion to `IMPORTANT/criteria.md` for **elimination criteria (E1–E6) only** — those are reused as-is.
> The **scoring rubric** below supersedes `criteria.md`'s rubric for this article (rebalanced per final decision,
> see Section 2). `IMPORTANT/knowledge.md` is where findings get logged once testing starts.
>
> **No live test has been run yet — this is the plan, not the results.** Follow this document step by step;
> it is written so no methodology decisions need to be made during execution. If something in here turns out
> to be factually wrong once you touch the live API, correct it in place and note the correction — don't work
> around it silently.
>
> **Disclosed conflict of interest:** Lobstr.io owns this article, this testing plan, and the scoring rubric
> (`criteria.md`) it's built on, and Lobstr is also one of the three products being evaluated. This should
> temper confidence in any ranking derived from this rubric, even where the underlying measurements are
> independently verifiable. Per `criteria.md`'s own writer notes: if Lobstr doesn't win the aggregate score,
> it does not get crowned — place it in whatever use-case section it genuinely fits. This disclosure must
> appear in the published article, not just this internal doc.

---

## 1. Final provider list

| Provider | Product | Access model |
|---|---|---|
| **Lobstr.io** | Google Maps Leads Scraper | CLI / Python SDK / dashboard / MCP, API key |
| **Apify** | `themineworks/maps-leads` actor | Console / REST / MCP |
| **Outscraper** | Google Maps Scraper (+ separate email extraction/verification) | REST, `X-API-KEY` header |

**Excluded from this comparison, with the existing factual reason preserved (not re-litigated):**

| Provider | Why excluded |
|---|---|
| OpenWeb Ninja | Key exists but confirmed **not subscribed** to the Local Business Data plan (`403 "You are not subscribed to this API"`, live-checked 2026-09-21). Their platform bundles many APIs under one key; each needs its own subscription. Could re-enter scope later if subscribed — not attempted for this run. |
| QuantumProxies | 500-lead cap is a per-run technical limit (each lead needs 3 fetches: maps search + homepage + contact page), not a tier restriction that paying lifts — confirmed via their own docs. Free credit only covers ~200 leads. A 1,000-lead run would always need 2+ calls regardless of spend. |

### Account/key status (verified live 2026-09-21 — recheck before the real run, this goes stale fast)

| Provider | Status | How it was confirmed |
|---|---|---|
| Lobstr.io | ✅ Paid, active | `GET /v1/squids` returned 93 existing crawlers on the account |
| Apify | ✅ Paid (STARTER, $29/mo) | `GET /v2/users/me` → `"isPaying": true` |
| Outscraper | ✅ Paid, balance $6.51 at last check | `GET /profile` → `"account_status": "valid"` |

**Fixed this session:** `.env`'s `LOBSTR_CRAWLER_ID` originally pointed at the Trustpilot Reviews Scraper crawler (copy-paste from the old project). Corrected to the actual Maps Leads crawler: `4734d096159ef05210e0e1677e8be823` (confirmed via the account's own squid list, `crawler_name: "Google Maps Leads Scraper"`). The old `LOBSTR_SQUID_ID` was removed for the same reason — a fresh squid must be created against the corrected crawler ID before any run.

**Still open, blocking a real Outscraper call:** `OUTSCRAPER_API_KEY` is **not present in `.env`** — add it before Outscraper's setup step in the checklist below.

---

## 2. Final scoring rubric — 10 points total

This is the final rubric for the article. It supersedes `criteria.md`'s point breakdown (elimination criteria E1–E6 in `criteria.md` are still used as-is).

### 2.1 Success Rate & Reliability — 2.0 pts
| Sub-criterion | Points |
|---|---|
| Success rate on 1K-request benchmark | 1.0 |
| Empty/partial response rate | 0.4 |
| Error handling quality | 0.3 |
| Stability during test window | 0.3 |

### 2.2 Data Quality & Completeness — 2.0 pts
| Sub-criterion | Points |
|---|---|
| Field coverage vs ground truth | 0.8 |
| Data accuracy | 0.5 |
| Schema consistency | 0.4 |
| Freshness | 0.3 |

### 2.3 Cost Efficiency — 1.5 pts
| Sub-criterion | Points |
|---|---|
| Cost per 1K successful records | 0.8 |
| Billing fairness | 0.3 |
| Free tier / trial credits | 0.2 |
| Pricing transparency | 0.2 |

### 2.4 Speed & Throughput — 1.5 pts
| Sub-criterion | Points |
|---|---|
| Median latency per request, **if measurable** | 0.5 |
| Wall-clock time for 1K-record batch | 0.5 |
| p95 latency, **if measurable** | 0.3 |
| Async/batch endpoint availability | 0.2 |

### 2.5 Scalability — 1.2 pts
No separate 10×/10K run exists or is claimed. Everything here is supported only by the two 1K runs plus provider documentation.
| Sub-criterion | Points |
|---|---|
| Rate limits & maximum concurrency allowed | 0.5 |
| Stability/degradation at tested 1K volume | 0.4 |
| Volume caps / documented ceilings that could block production use | 0.3 |

### 2.6 Usability — 1.8 pts
Merges the old "Developer Experience" and "Input Flexibility" criteria.
| Sub-criterion | Points |
|---|---|
| Input flexibility (search queries, URLs/IDs, geo/location, filters) | 0.3 |
| Endpoint/platform coverage | 0.3 |
| Enrichment/related endpoints | 0.2 |
| Time-to-first-successful-request | 0.3 |
| Documentation quality | 0.3 |
| SDKs and working examples | 0.2 |
| Error clarity + support responsiveness | 0.2 |

**TOTAL = 2.0 + 2.0 + 1.5 + 1.5 + 1.2 + 1.8 = 10.0**

A provider-specific capability that another provider lacks is **never** scored as a failure for the other provider — it's documented under Usability/Input Flexibility as a differentiator, not penalized elsewhere.

---

## 3. Run design — exactly two runs per provider

**No concurrency A/B test.** (Superseded design note: an earlier draft of this plan ran Lobstr twice at `concurrency: 1` vs `concurrency: 10` and treated the other providers' second run as a repeatability test. That design is dropped — see Section 5 for the replacement.) The two runs now differ **only by industry**, and every other parameter — including concurrency, which is fixed at each provider's max sensible/documented level for both runs — stays identical between them.

### Superseded: single query-per-city design

An earlier draft of this section specified one search per city ("marketing agencies in New York", limit 500) and treated any provider that couldn't hit an exact 500/500 split as an edge case to document. **Live testing found this isn't an edge case — it's universal.** Google Maps caps any single search view at roughly 120–200 results, confirmed three ways before any paid run was fired:
- **Lobstr rejects it outright, server-side:** live `POST /v1/squids/{id}` with `max_results: 1000` returned `400 AttributeLimitExceeded — "The max_results should be lower than the maximum value of 200"`. This is a **per-task** limit (confirmed both by the error and Lobstr's own docs describing "Max Results Per Task" as capped at 200 — Google's own ceiling, not a Lobstr-specific one).
- **Apify's `themineworks/maps-leads` has no internal grid/tile subdivision** (confirmed via the actor's own docs/FAQ) — a single query is capped at ~120 results no matter what `maxLeadsPerQuery` is set to. Their documented way to add volume is more independent query strings, not a higher per-query number.
- **Outscraper's real single-query ceiling is unconfirmed** (community sources suggest up to ~400–500 natively, but this is not vendor-confirmed and must not be assumed without a live check).

Requesting "500 per city" as one query per city would have silently under-delivered for at least 2 of the 3 providers while looking like a normal successful call — exactly the "hidden cap shows up mid-run" failure mode from Section 12's Trustpilot lessons. Caught before any paid request was sent.

### Sub-area design (replaces the single-query-per-city design above)

Each city is split into 5 borough/district sub-areas, each queried independently and capped at **200 requested results** (`PER_SUBAREA_CAP` in `scripts/lib/config.py`) — standardized across all 3 providers so every provider faces the same per-request ceiling, not just whatever its own natural limit happens to be. Results are pooled and deduped (`scripts/lib/dedupe.py`) afterward to compute the real per-city and per-run totals. **No exact 500/500 or 1,000 figure is enforced up front** — Google's own per-search ceiling makes that unenforceable at the request level; the actual achieved totals are what get reported, honestly, per sub-area and per city.

- **New York** (5 official boroughs, no arbitrary cutoff): Manhattan, Brooklyn, Queens, Bronx, Staten Island.
- **Los Angeles** (5 well-known major districts — LA has no formal borough system, so 5 is chosen to match NYC's count for comparable sub-area density): Downtown LA, Hollywood, Santa Monica, Koreatown, San Fernando Valley (Van Nuys).
- **10 sub-area queries per run** (5 per city), each requesting up to 200 results.

### Run 1 — Marketing agencies
- **Industry:** Marketing agencies
- **Search inputs:** `"marketing agencies in <sub-area>, <city>"` for each of the 10 sub-areas above (exact list in `scripts/lib/config.py` → `RUN_1`).
- **Target:** no fixed number enforced — the realistic ceiling is 10 × 200 = 2,000 requested before dedup; report the actual unique total per city and per run.

### Run 2 — Restaurants
- **Industry:** Restaurants
- **Search inputs:** same 10 sub-areas, `"restaurants in <sub-area>, <city>"` (exact list in `scripts/lib/config.py` → `RUN_2`).
- **Target:** same as Run 1 — report the actual achieved total, don't force a number.

### Per provider
- Run 1 = up to 2,000 requested (10 sub-areas × 200), real total reported after dedup.
- Run 2 = same structure, different industry.
- **Total requested ceiling = up to 4,000 per provider** (was 2,000 under the old single-query-per-city design) — this is a request ceiling, not a promise of that many real unique leads; report what's actually returned.

No additional industries, cities, or sub-area counts beyond this unless a provider technically forces it — and if so, document the limitation, don't silently absorb it.

No 10K/10× scalability run. No separate email-only test. No separate speed-only test. No smoke test beyond what's strictly required to confirm a provider's setup actually works (Section 9, Apify) — everything else rides on these same two runs.

---

## 4. Common input requirements (every provider, both runs)

Request/enable these wherever the provider supports it. Never force an unsupported field or pretend two providers are equivalent when they aren't — document the gap instead (see Section 6).

- Business name
- Category
- Address
- Phone
- Website
- Rating
- Review count
- Google Maps URL / place identifier
- Coordinates
- Opening hours
- Business status
- Business details (richer fields beyond the bare listing, where the provider distinguishes this)
- Email extraction
- Images, where available

---

## 5. Concurrency

**Rule:** use the maximum sensible/documented concurrency each provider actually offers, for **both** runs. Do not artificially throttle Lobstr's concurrency down to `1` just because Apify and Outscraper don't expose an equivalent user-facing control — that would be handicapping the one provider that has a real concurrency feature.

- **Lobstr:** has a native `concurrency` (Slots) setting on the squid. Before Run 1, confirm the account's actual maximum entitled concurrency (plan-dependent) and set the squid to that maximum for both runs. Record the exact value used.
- **Apify:** no user-facing concurrency parameter. The actor parallelizes `searchQueries` internally — document this as its concurrency *capability*, not a number we set.
- **Outscraper:** no concurrency knob; the 3-stage pipeline (scrape → extract → verify) is sequential by design. Document this architecture as its concurrency *capability*.

**Reporting rule:** always separate **raw runtime/throughput** from **concurrency capability** in the writeup. Never describe one provider as "faster scraping" without noting that the providers' concurrency settings/architectures differ — a faster wall-clock time might just mean higher concurrency was available, not that the underlying per-request performance was better.

---

## 6. Provider-specific parameters (fixed for both runs, values below reflect the 500/500 split)

### Lobstr.io — squid `params` (crawler `4734d096159ef05210e0e1677e8be823`)

```json
{
  "country": "United States",
  "ratings": "Any rating",
  "language": "English (United States)",
  "functions": {
    "fetch_business_images": true,
    "collect_business_details": true,
    "extract_emails_from_website": true
  },
  "geo_match": true,
  "max_results": 200,
  "skip_closed": false,
  "category_match": true,
  "website_filter": "all",
  "skip_without_email": false,
  "max_unique_results_per_run": null,
  "concurrency": 20
}
```
- **Corrected 2026-09-22 (supersedes the previous entry in this section):** `max_results` is a **per-task** cap, not per-squid-total — confirmed live when `max_results: 1000` was rejected server-side with `400 AttributeLimitExceeded — "The max_results should be lower than the maximum value of 200"`. 200 is Google's own real per-search ceiling (see Section 3's sub-area design), not an arbitrary Lobstr number. Set to the max allowed, `200`, applied uniformly to every task in the squid. `max_unique_results_per_run` stays `null` (uncapped) so the 10 sub-area tasks' unique results all accumulate into one run total rather than being artificially capped.
- **Concurrency `20`** — the documented maximum slots per squid across all plans (confirmed via Lobstr's own knowledge base), set live 2026-09-22.
- **Task format is a Google Maps search URL with embedded coordinates, not a text query string:** `https://www.google.com/maps/search/<url-encoded query>/@<lat>,<lng>,<zoom>z`. Example from Lobstr's own docs: `https://www.google.com/maps/search/restaurant/@43.3928346,5.2662584,14z`. Add tasks via `POST https://api.lobstr.io/v1/tasks` with body `{"squid": "<squid_id>", "tasks": [{"url": "..."}, ...]}`.
  - **10 tasks per run** — one per borough/district sub-area from Section 3 (5 NYC boroughs + 5 LA districts), each at **zoom `14z`** (Lobstr's own documented example zoom).
  - **Zoom live-tested 2026-09-22, two rounds, real evidence in `outputs/lobstr/`:**
    - `12z` (initial choice) **failed** — a 50-result/5-per-task smoke run returned businesses in Palisades Park NJ, Paramus NJ, and near Long Island for NYC sub-areas, and Glendale CA for an LA sub-area — far outside the intended borough/district. Only 16/50 (32%) unique after dedup, meaning adjacent sub-areas' search radii overlapped so heavily they weren't meaningfully distinct searches.
    - `14z` (corrected) **passed** — same smoke test shape, 43/50 (86%) unique, and addresses landed in genuine borough/district neighborhoods (Queens sub-area → Jamaica/Woodhaven/Flushing/Glendale-Queens/South Richmond Hill; Van Nuys sub-area → Encino/Van Nuys/Sherman Oaks). Minor residual cross-border bleed remains (one Hoboken NJ result for the Manhattan query, one Glendale CA result for an LA-core query) — acceptable and documented, not treated as disqualifying.
    - Both smoke runs cost real credits (127 + 150 = 277 credits total) — a real, small spend, logged here for the record.
    - The old `12z` tasks were deleted (`DELETE /v1/tasks/{id}`, confirmed working despite not being in the docs) and replaced with the `14z` set before any real (200/sub-area) run was fired.
  - Exact URLs generated in `scripts/lib/config.py` (`RUN_1`/`RUN_2`, `lobstr_task_url` per target) — e.g. `https://www.google.com/maps/search/marketing+agencies/@40.7831,-73.9712,12z` (Manhattan).
  - This is a real asymmetry vs. Apify/Outscraper's plain text `"<query> in <sub-area>, <city>"` inputs — Lobstr's input is coordinate-anchored, theirs is name-anchored. Document this difference in the Usability/Input Flexibility writeup (Section 11) rather than treating the three as identical inputs.
- `fetch_business_images: true` and `collect_business_details: true` — corrected from the account's live-squid defaults (both were `false`, a leftover from an unrelated squid, not a deliberate choice). Left off, Lobstr's own field coverage vs ground truth (Section 2.2, 0.8 pts) would be artificially depressed relative to competitors that return these fields by default — a real fairness risk given Lobstr is the house product being evaluated.
- `extract_emails_from_website: true` performs **extraction only** — see Section 8, the email rule is load-bearing for scoring and must not be glossed over.
- No `fetch_since` — that's a Trustpilot-reviews-only param, doesn't apply to Maps Leads.
- **Carried over from the Trustpilot benchmark, confirmed live on that project (2026-09-01), re-verify here before trusting it:** `GET /v1/results` accepts a `limit` query param but **silently ignores it** — the server always returns exactly 10 items/page regardless. The real, working (and undocumented) parameter is `page_size` (e.g. `page_size=1000`). Any results-fetching script for this benchmark must use `page_size`, not `limit`, or pagination will look 10x slower/more error-prone than it actually is. Confirm this still holds for the Maps Leads crawler specifically — the earlier finding was on the Trustpilot crawler.
- **Cost measurement endpoint:** `GET /v1/user/balance` (confirmed working in the Trustpilot client, `scripts/lib/lobstr_client.py`) — this is Lobstr's equivalent of Apify's `/v2/users/me` and Outscraper's `/profile`. Lobstr bills in credits, not dollars directly (e.g. email verification is "100 credits/email" per Section 7) — convert credits to dollars using the account's actual plan rate (confirm the current $/credit rate live, don't assume the Trustpilot project's old rate still applies) before comparing cost-per-1K against Apify/Outscraper's dollar-denominated billing.

### Apify — `themineworks/maps-leads` actor input

```json
{
  "searchQueries": ["marketing agencies in Manhattan, New York"],
  "maxLeadsPerQuery": 200,
  "language": "en",
  "verifyEmails": true,
  "skipClosedBusinesses": true,
  "deduplicateAcrossRuns": false,
  "includeFields": [],
  "proxyConfig": { "useApifyProxy": true }
}
```
**One actor invocation per sub-area query — not one call with all 10 queries** (see the "hidden-cap finding" below: bundling all 10 into one call trips an undocumented $0.25/run spend ceiling after the first query and silently drops the rest). Fire this same shape 10 times per benchmark run, once per sub-area, with `searchQueries` set to that single sub-area's string each time — full list in `scripts/lib/config.py` (`RUN_1`/`RUN_2`).
- **Superseded 2026-09-22:** the previous version of this block used one query per city with `maxLeadsPerQuery: 500`, on the assumption this actor natively supports an exact 500/city split. Confirmed via the actor's own docs this is wrong — `maxLeadsPerQuery` caps *per query*, but a single query is itself capped around ~120 results by Google's own ceiling regardless of the number requested (this actor has no internal grid/tile subdivision). `maxLeadsPerQuery: 200` now matches Lobstr's confirmed hard per-task ceiling (Section 3's sub-area design) so every provider faces the same per-request cap.
- `deduplicateAcrossRuns: false` — set this way from the start for both runs. (Superseded note: an earlier draft only turned this off for a "Run 2 repeatability check"; since Run 2 is now a different industry with a fresh, non-overlapping search, there's no cross-run dedup risk to guard against, but keeping it off avoids any silent interaction with unrelated past runs on the same actor/account.)
- `verifyEmails: true` performs extraction **+ DNS/MX verification inline** — this is a materially different guarantee than Lobstr's extraction-only default; see Section 8.
- No concurrency parameter exposed — parallelizes `searchQueries` internally (Section 5).
- **Capability gap, confirmed via vendor docs (2026-09-22), not a config choice:** this actor returns `category` and `hours` but has **no field or parameter for photos/images at all**. Nothing to turn on here — document as a structural gap in Section 2.2 scoring, not a misconfiguration.
- **Known output bug, confirmed LIVE 2026-09-22 (smoke test, not just vendor docs):** `business_status` was `"UNKNOWN"` on all 5/5 records returned. `skipClosedBusinesses` filtering cannot be verified as functional given the underlying field is broken — treat any "closed businesses filtered" claim for Apify as unconfirmed.
- Do not reuse any stored `APIFY_ACTOR_ID` value from the old Trustpilot project — point explicitly at `themineworks/maps-leads` (resolved actor ID: `B1byySkFdoSQ2DlW3`).
- **Smoke test passed (2026-09-22, `outputs/apify/smoke-test-2026-09-22/`):** 1 sub-area query ("marketing agencies in Manhattan, New York"), `maxLeadsPerQuery: 5` → run `kllyS2JM3E1o2rhmU` SUCCEEDED in 10.3s, 5 places found, all expected fields present (`name`, `category`, `address`, `phone`, `website`, `rating`, `hours`, `coordinates`, `google_maps_url`, `email`, `email_status`, `all_emails`), confirming the actor behaves as documented. Actual cost: $0.0082.
- **Major billing-fairness finding, confirmed live (Section 12, lesson 5 — don't take vendor claims on faith):** Apify's real pricing model is **`PAY_PER_EVENT`** — `lead-verified` events at **$0.0016/lead**, plus a one-time `apify-actor-start` fee of **$0.005/run** (memory-scaled). Critically, **only leads with a verified email are billed** — of the 5 smoke-test results, the 2 with a found+verified email show `"charged": true`, the 3 with `"enrichment_status": "no_email"` show `"charged": false` and were not billed. This is a direct, empirical confirmation of Apify's "you only pay for delivered/verified leads" marketing claim — genuinely true for this actor, not just copy. Use this exact mechanism (`charged` field per record) to compute Section 2.3's billing-fairness sub-criterion during the real run — don't estimate it.
- **Cost model implication for Section 9.4:** "cost per 1K successful records" for Apify must be computed as `count(charged=true) × $0.0016 + $0.005` per run, not a flat per-record-returned rate — a provider returning many places but few verified emails will look cheap per-record-returned but is really being billed per verified lead.
- **Major hidden-cap finding, confirmed live 2026-09-22 during the real Run 1 attempt — this is the Trustpilot "hidden cap shows up mid-run" lesson recurring in a new provider:** this actor has an **undocumented $0.25-per-run internal spend ceiling** ("profit guard"). Submitting all 10 sub-area queries in a single actor call ran only the first (Manhattan: 200 found, 80 charged, spend $0.2504) then **silently refused to start the remaining 9 queries** — confirmed via the run's own log: `[profit-guard] spend ~$0.2504 passed the $0.25 ceiling — stopping to bound cost.` The overall run still reported `status: SUCCEEDED` with a generic "80 leads delivered" message — nothing in the top-level run object flags the truncation; it's only visible in the dataset's own `_type: "summary"` row (`queries_run: 1` instead of 10) or the raw log.
- **Fix, adopted going forward:** run **each sub-area query as its own separate actor invocation** (`searchQueries: [<single query>]` per call), not one call with all 10 queries. Manhattan completed cleanly within its own $0.25 budget when run alone, so one-query-per-run avoids the guard. This means **10 separate Apify runs per benchmark run** (20 total across Run 1 + Run 2), each polled and logged independently — more orchestration overhead, but the only way to get complete, untruncated data from this actor.
- **Standing verification rule for every Apify run, not just this one:** always check the dataset's `_type: "summary"` row's `profit_guard_tripped` field and compare `places_found` against the requested `maxLeadsPerQuery` — never trust the top-level `status: SUCCEEDED` alone as proof the full request was honored.
- **Refined 2026-09-22, after running all 10 sub-areas as separate invocations — there are TWO distinct guard mechanisms, confirmed via raw run logs, not one:**
  1. **Run-level $0.25 ceiling** (`"spend ~$0.25 passed the $0.25 ceiling — stopping to bound cost"`) — fires *after* a query completes fully, and only blocks *additional* queries in the same run from starting. Harmless once each sub-area is its own run (Manhattan, Brooklyn, Downtown LA, Hollywood, Santa Monica all tripped this but still returned their full ~200-cap result count).
  2. **Real-time per-query profitability breaker** (`"spend ~$X exceeds revenue ~$Y + $0.02 allowance — stopping (run would lose money)"`) — can cut a **single query short mid-processing** if the running spend-to-charged-lead-revenue ratio turns unfavorable, independent of the $0.25 ceiling. Confirmed on the San Fernando Valley (Van Nuys) sub-area: cut off at just 20 places found (vs. the 200 requested) with 0 charged, because no chargeable emails were turning up relative to spend.
- **Practical implication — a real comparability risk, not just a curiosity:** a sub-200 result count for an Apify sub-area can mean *either* (a) genuine Google Maps data scarcity in that area (confirmed for Bronx: 187, Staten Island: 87, Koreatown: 150 — no guard warning appeared in any of their logs at all) *or* (b) Apify's own internal profitability logic giving up early on a low-email-yield area (confirmed only for Van Nuys in Run 1). These must be told apart per sub-area by checking the raw log for the profitability-breaker message — a low count is not automatically "this area has few businesses."
- **Confirmed as an industry-driven pattern, not a one-off, from Run 2 (restaurants) live data (2026-09-22):** the real-time profitability breaker tripped on **3 of 10** restaurant sub-areas (Manhattan: cut to 20/200 found, Bronx: 126/200, Staten Island: 57/200 — all confirmed via raw log message `"spend exceeds revenue + $0.02 allowance"`), versus only **1 of 10** for marketing agencies in Run 1 (Van Nuys). Total Run 2 places_charged across all 10 sub-areas was **264**, barely half of Run 1's **527** for the same 200-per-sub-area request. This strongly suggests **restaurants have a structurally lower email-yield rate than marketing agencies**, and Apify's own cost-protection logic — not Google Maps' actual restaurant listing volume — is the reason this actor under-delivers for this industry. This is a genuine, article-worthy finding for Section 2.1 (Reliability) and Section 2.5 (Scalability: "volume caps... that could block production use") — a real production risk for anyone using this actor on low-email-yield verticals, not a data-availability limitation of Google Maps itself.

### Outscraper — reduced scope, decided 2026-09-22 (budget constraint, documented not silently absorbed)

**Confirmed live:** account balance is **$6.51**, and Outscraper's real pricing is $3/1,000 for each of base scrape, email extraction (`domains_service`), and email verification (`emails_validator_service`) — up to $9/1,000 for the full 3-stage pipeline. The full design (2 runs × 10 sub-areas × 200 leads = 4,000 requested through all 3 stages) would cost an estimated ~$18–36, far beyond the balance, and a top-up isn't available. Decision: **Outscraper runs base scrape only, no email extraction or verification stages**, at a reduced per-sub-area cap so even base-only fits the budget (base-only at full 200/sub-area would still cost ~$12, over budget).

- **Scope:** both runs (marketing agencies + restaurants), all 10 borough/district sub-areas — breadth preserved, only depth reduced.
- **Per-sub-area cap: 80 leads** (not 200 — Lobstr and Apify keep 200). 2 runs × 10 sub-areas × 80 = 1,600 requested × $3/1,000 = **~$4.80**, leaving a margin under the $6.51 balance.
- **Email extraction/verification: not tested for Outscraper this round.** Its Section 2.2/2.3 email-related sub-scores must be marked "not tested (budget constraint)," never silently left blank or estimated.
- **Cost-comparison caveat, must appear in the article wherever cost is compared:** Outscraper's cost-per-1K reflects **bare listings only** (no contact enrichment), while Lobstr's and Apify's reflect contact-enriched data. A direct "$/1,000 leads" ranking across all 3 would be misleading without this caveat attached every time it's shown.

### Outscraper — three separate billed calls per run

1. **Base scrape** — one call per sub-area (10 calls per run, same sub-areas as Lobstr/Apify above):
   - `GET /maps/search-v3?query=marketing agencies in Manhattan, New York&limit=200&language=en&region=US&drop_duplicates=true`
   - ...repeated for all 10 sub-areas (exact list in `scripts/lib/config.py`).
   - (Run 2: same 10 sub-areas, `restaurants` in place of `marketing agencies`.)
2. **Email extraction** — `domains_service` enrichment against the returned website URLs, run once against the pooled result (or per-sub-area, doesn't matter — cost is billed per domain either way, just track it per Section 12).
3. **Email verification** — `emails_validator_service` enrichment, same pooling approach.
- **Superseded 2026-09-22:** the previous version of this block used one call per city with `limit=500`, treating Outscraper's per-query ceiling as high enough to hit an exact 500/city split directly. Outscraper's real single-query ceiling was never vendor-confirmed (community sources suggest up to ~400–500, not documented) — standardized to `limit=200` per sub-area instead, matching Lobstr's confirmed hard cap, so no provider gets a request-level advantage from an unverified higher ceiling.
- `drop_duplicates=true` on each base call only dedupes within that single call — still run everything through `scripts/lib/dedupe.py` afterward across all 10 sub-area calls for cross-provider consistency.
- **Confirmed via vendor docs (2026-09-22):** the base `search-v3` call already returns full business details and photo data standard — no extra parameter needed (`category`, `working_hours`, `photos_count`, `photo`, `street_view`, `popular_times`, `reviews_per_score_1..5`, plus `place_id`/`google_id`/`cid`/`kgmid`). This is the richest default field set of the three providers.
- No concurrency knob; each of the 3 stages is billed and timed independently — never collapse them into one "per lead" number until verification has actually run (Section 12).
- **Watch the balance.** $6.51 confirmed live 2026-09-22 — this must now cover 2 runs × 10 sub-area calls × up to 200 leads × 3 billed stages each, a larger ceiling than the earlier 1,000-lead framing assumed. Recheck `/profile` immediately before committing to the full run; if the balance is insufficient, that's a blocker to resolve before spending, not to silently shrink the workload around.

---

## 7. Email extraction vs. verification — do not conflate these

This finding is load-bearing for Section 2.2 and 2.3 scoring and must be preserved exactly:

- **Lobstr:** `extract_emails_from_website: true` performs extraction **only**. Verification is a **separate, dashboard-only manual action** (click "Verify" on the completed run in the Runs tab), billed separately (100 credits per valid-or-unknown email). **No documented API endpoint for triggering verification was found.** If this holds true live, Lobstr's result for this benchmark must be explicitly labeled **"extraction-only"** for the email metric.
- **Apify:** `verifyEmails: true` performs extraction **+ DNS/MX verification inline**, in the same call.
- **Outscraper:** extraction and verification are two separate enrichment stages (`domains_service`, `emails_validator_service`) — see Section 6.

**Reporting rule, no exceptions:**
- Report separately, per provider: website found → email extracted → email verified → verification status (valid/risky/unverified/unknown, using whatever categories the provider actually exposes).
- **Never** compare Lobstr's extracted-only emails directly against Apify's or Outscraper's verified emails as if they measure the same thing.
- If Lobstr cannot verify via API during the actual test, its number goes in the results table as "extraction-only, verification not tested via API" — not silently upgraded to look equivalent to a verified count.

---

## 8. What raw data/logs to save

Folder structure already created under `data/<provider>/`, mirroring the Trustpilot benchmark:

```
data/<provider>/
  raw/          every request payload and every raw response page/dataset, unmodified
  exports/      the pooled, deduped lead list — all-leads.csv + all-leads.json
  logs/         run.log (chronological narrative) + errors/ (structured error events, if any)
  analysis/     computed reports — see Section 9 for exactly what goes in each file
  reports/      human-readable .md writeups per finding (cost, field-coverage, scorecard, etc.)
```

`outputs/<provider>/` exists as scratch space for the one-off setup/smoke check Apify needs (Section 9) — anything validated there gets promoted into `data/<provider>/` once trusted, not left duplicated.

Nothing goes into `knowledge.md` or the article that doesn't trace back to a file under `data/`.

---

## 9. Metrics to calculate from the same two runs

No separate experiments per criterion — every number below comes out of the same Run 1 + Run 2 data already being captured.

### 9.1 Reliability (→ Section 2.1)
Per run, per provider, capture: requested records, returned records, successful records, failed records, empty/partial responses, errors (with codes/messages), duplicate records (via `dedupe.py`), and whether the run completed successfully end-to-end. Save as `analysis/run-state.json` + `analysis/error-log.json`.

**Scoring:** success rate = successful ÷ requested, scored relative to the best performer in this test (best gets full 1.0, others scaled proportionally). Empty/partial rate, error handling quality, and stability are scored against the qualitative anchors in Section 13.

### 9.2 Speed (→ Section 2.4)
Capture: start timestamp, completion timestamp, wall-clock runtime, records/minute, and request-level latency **only if the provider actually exposes per-request timestamps** (e.g. Outscraper's 3 discrete calls have real per-call timing; Lobstr's squid→poll and Apify's actor→dataset are batch models where only total wall-clock is meaningful — do not invent a median/p95 for a batch architecture that doesn't expose it). Save as `analysis/timings.json`.

**Scoring:** wall-clock time for the 1K batch scored relative to the fastest provider. Median/p95 latency sub-criteria score **0 and are marked "not applicable"** for any provider whose architecture doesn't expose per-request timing — don't force a number. Async/batch endpoint availability scored on whether the provider offers a submit-then-poll pattern vs. synchronous-only.

### 9.3 Data quality & completeness (→ Section 2.2)
For returned records, check: field presence, field completeness, accuracy against source data (see Section 10, ground truth), schema consistency across records, freshness, duplicate rate, and irrelevant/wrong businesses returned for the query. Save as `analysis/domain-summary.json` + `analysis/duplicate-report.json` + `analysis/ground-truth-match.json`.

A field only counts toward "coverage" if **the ground-truth source actually has that information for that business** — a missing field is not a provider failure if Google Maps itself doesn't expose it for that listing. Do not assume "more fields returned = better" without checking this.

**Freshness is not concretely defined yet — decide this before scoring, not while writing the article.** None of the 3 providers is confirmed to expose an explicit "last crawled"/"last updated" timestamp. The practical proxy: compare a handful of ground-truth sample businesses' live Google Maps state (rating, review count, hours) against each provider's returned values at time of test — a mismatch suggests cached/stale data, a match doesn't prove freshness but is the best available signal. If no usable signal exists for a provider, score that sub-criterion 0 and mark "not measurable" rather than guessing.

**Lead usability is folded into this criterion, not a separate score.** Capture, per provider: website availability rate, phone availability rate, email availability rate (extracted vs. verified per Section 7), relevant-business rate, duplicate-free rate, and presence of useful business details (category, hours). These roll into the Data Quality sub-criteria above rather than getting their own line item.

### 9.4 Cost (→ Section 2.3)
Capture: actual run cost (measured via each provider's live billing endpoint — Outscraper `/profile`, Apify `/v2/users/me` — never estimated from a rate card unless a provider genuinely has no billing endpoint, and if so flag it explicitly as *estimated*), cost per 1K successful records, whether failed/empty results were actually billed (billing fairness), free/trial credits available, pricing transparency, and — specifically for Outscraper — the cost of each of the 3 stages tracked independently before being summed into one per-lead figure. Save as `analysis/cost-report.json`.

**Scoring:** cost-per-1K scored relative to the cheapest provider (cheapest gets full 0.8, others scaled by ratio). Billing fairness, free tier, and pricing transparency scored against Section 13's anchors.

### 9.5 Scalability (→ Section 2.5)
From the same two runs plus provider documentation (no separate 10×/10K run, none is claimed): rate limits, maximum concurrency actually available (Section 5), volume limits, pagination/result caps encountered, whether the 1K run degraded/failed/completed normally, and any documented daily/monthly ceiling that could affect production use (e.g. Outscraper's balance-driven ceiling). Save as `analysis/pagination-report.json` + notes in `reports/scorecard.md`.

### 9.6 Usability (→ Section 2.6)
During setup and execution, capture: time to first successful request, setup complexity, documentation quality, SDKs/examples, API workflow (auth, request shape, polling/result retrieval), error clarity, support experience (only if actually contacted/tested — don't fabricate this), input options actually available (search/location controls, filters), enrichment endpoints, and output richness. This is mostly qualitative — log concrete evidence (screenshots, doc links, timestamps) as you go rather than reconstructing it after the fact.

---

## 10. Ground-truth / data-quality procedure

- Pull a **consistent sample of real businesses actually returned by the same search targets used in Run 1/Run 2** (not a separately invented list) — spread across both industries and both cities so every sub-group (marketing agencies × NY, marketing agencies × LA, restaurants × NY, restaurants × LA) has at least a handful of sampled businesses. A manageable total is ~20–30 businesses across all four sub-groups (roughly 5–8 each), not the full 2,000.
- For each sampled business, manually inspect the actual Google Maps listing and record: name, address, phone, website, category, rating, hours — by hand, independent of any provider's output.
- Compare each provider's returned record for that same business against this hand-verified sample to compute field coverage and accuracy (Section 9.3). A field only counts as "missing" if the ground truth actually has a value for it.
- If a working accuracy/completeness comparison script already exists (none does yet in this project's `scripts/` — Trustpilot's `ground_truth_compare.py` per provider is the pattern to adapt), build a thin equivalent rather than checking by hand at scale; do not require manually checking every field of all 2,000 records.
- Save the hand-verified sample under `ground-truth/`, one file per sub-group, and the comparison output under each provider's `analysis/ground-truth-match.json`.

---

## 11. Provider-specific input functionality (Usability/Input Flexibility evidence — preserved)

Documented as differentiators, never as a penalty against a provider lacking another's capability.

**Lobstr:** squid + task list/search terms · `country` · `geo_match` · `max_results` · `ratings` · `category_match` · `website_filter` · `skip_closed` · `collect_business_details` · `fetch_business_images` · `extract_emails_from_website` · Slots/`concurrency` · `max_unique_results_per_run` · async squid → poll/results architecture.

**Apify:** `searchQueries` · `maxLeadsPerQuery` · `skipClosedBusinesses` (note: `business_status` bug, Section 6) · `verifyEmails` · `deduplicateAcrossRuns` · actor run → dataset architecture.

**Outscraper:** `query` · `region` · `limit` · `business_status` · `drop_duplicates` · separate enrichment/verification stages · three-stage architecture.

---

## 12. Lessons from the Trustpilot benchmark — still applied

1. **A provider that works once can fail completely on the next run.** OpenWeb Ninja went 1,000/1,000 → 0/1,000 with 75× HTTP 429s on the same account across two Trustpilot runs. → Treat any single-run success as unconfirmed; both Run 1 and Run 2 here are real, separately-executed runs, not one run reported twice.
2. **Verify subscription/billing status before spending a single request.** Already applied — this is exactly how OpenWeb Ninja got excluded in Section 1.
3. **Don't blend measured cost with estimated cost.** Outscraper and Apify both expose live billing endpoints — use them; never fall back to rate-card math unless a provider genuinely has nothing better, and flag it explicitly if so.
4. **The default/most-popular option on a platform isn't always the one that works.** → Run a small setup/smoke check on `themineworks/maps-leads` (Section 9's Apify open item) before trusting it as the actor of record — don't assume the marketing copy holds. This is the one exception to "no smoke tests" in Section 3, because it's a correctness check, not a separate benchmark run.
5. **Check billing-fairness claims empirically.** Confirm "you only pay for delivered/verified leads" style claims by comparing requested-vs-billed counts against the provider's own billing endpoint, not the pricing page.
6. **Hidden caps show up mid-run, not in the docs.** Watch every provider's response for quiet truncation (requested count vs. actually-returned count) rather than trusting a success status alone. (Apify's `business_status: UNKNOWN` bug, found this session, is exactly this kind of hidden defect — found in docs this time, but confirm live.)
7. **Reproducibility is the differentiator.** Everything under `data/` should let someone else rerun the exact script and get the same evidence.

---

## 13. Qualitative scoring anchors

For sub-criteria that aren't a direct ratio calculation (error handling quality, stability, billing fairness, free tier, pricing transparency, docs quality, SDKs, error clarity/support, input flexibility, endpoint coverage, enrichment endpoints), score each on a 3-point anchor scale and convert to the sub-criterion's point value:

| Anchor | Meaning | Fraction of sub-criterion points |
|---|---|---|
| Full | Clearly best-in-class, no meaningful gap found during testing | 100% |
| Partial | Present and usable, but with a documented gap, bug, or friction point | 60% |
| Weak/Missing | Not present, broken, or contradicted by live evidence | 0–20% |

Every anchor assignment must cite the specific evidence file (`data/<provider>/...` or a doc URL) it's based on — no anchor gets assigned from memory or vendor marketing copy.

For direct ratio sub-criteria (success rate, cost per 1K, wall-clock time), use relative scoring: the best performer in this specific test gets full points for that sub-criterion, others scored as `points × (their_value / best_value)` for "higher is better" metrics, or `points × (best_value / their_value)` for "lower is better" metrics (cost, latency), floored at 0.

---

## 14. Final results table (template — fill in after testing)

### Reliability
| Provider | Requested | Returned | Successful | Failed | Empty/Partial | Duplicates | Errors | Completed OK? |
|---|---:|---:|---:|---:|---:|---:|---|---|
| Lobstr | | | | | | | | |
| Apify | | | | | | | | |
| Outscraper | | | | | | | | |

### Speed
| Provider | Start | End | Wall-clock | Records/min | Median latency | p95 latency | Architecture |
|---|---|---|---:|---:|---|---|---|
| Lobstr | | | | | N/A (batch) | N/A (batch) | squid → poll |
| Apify | | | | | N/A (batch) | N/A (batch) | actor → dataset |
| Outscraper | | | | | | | 3-stage sequential |

### Data Quality
| Provider | Field coverage | Accuracy | Schema consistency | Freshness | Website % | Phone % | Email extracted % | Email verified % |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Lobstr | | | | | | | | extraction-only |
| Apify | | | | | | | | |
| Outscraper | | | | | | | | |

### Cost
| Provider | Measured cost (Run 1) | Measured cost (Run 2) | Cost / 1K successful | Billing fairness | Free credits | Pricing transparency |
|---|---:|---:|---:|---|---|---|
| Lobstr | | | | | | |
| Apify | | | | | | |
| Outscraper | | | | | | |

### Scalability
| Provider | Rate limit / max concurrency | Degradation at 1K? | Volume caps / ceilings |
|---|---|---|---|
| Lobstr | | | |
| Apify | | | |
| Outscraper | | | |

### Usability
| Provider | Time to first success | Docs quality | SDKs | Error clarity | Input flexibility | Endpoint coverage | Enrichment endpoints |
|---|---|---|---|---|---|---|---|
| Lobstr | | | | | | | |
| Apify | | | | | | | |
| Outscraper | | | | | | | |

### Final scores (/10)
| Provider | Reliability /2.0 | Data Quality /2.0 | Cost /1.5 | Speed /1.5 | Scalability /1.2 | Usability /1.8 | **Total /10** |
|---|---:|---:|---:|---:|---:|---:|---:|
| Lobstr | | | | | | | |
| Apify | | | | | | | |
| Outscraper | | | | | | | |

---

## 15. Open items before the first real test

- [x] Add `OUTSCRAPER_API_KEY` to `.env` — done 2026-09-22, reused from the trustpilot-api-benchmark project's `.env` (same Outscraper account). Confirmed live via `GET /profile`: `account_status: "valid"`, balance $6.51.
- [x] Create a fresh Lobstr squid against the corrected crawler ID (`4734d096159ef05210e0e1677e8be823`) — done live 2026-09-22, squid `6afddf2feb67428f8bed0c383ff10380`, saved to `.env` as `LOBSTR_SQUID_ID`.
- [x] Confirm whether Lobstr's `max_results` applies per-task or per-squid — resolved live 2026-09-22: **per-task**, hard-capped at 200 (a live `400 AttributeLimitExceeded` at 1000 proved it, corrects the earlier "squid-level only" conclusion). See Section 3/6.
- [x] Configure the Lobstr squid with Section 6's params — done live 2026-09-22: `max_results: 200`, `concurrency: 20`, `fetch_business_images: true`, `collect_business_details: true`, `extract_emails_from_website: true`.
- [x] Discovered and resolved: Google's own ~120–200-per-search ceiling meant the original single-query-per-city design would have silently under-delivered for Lobstr and Apify. Replaced with the 10-sub-area borough/district design (Section 3).
- [x] Put the finalized sub-area `TARGETS` into `scripts/lib/config.py` — done, includes Lobstr's coordinate-based task URLs, generated and verified live.
- [x] Add the 10 Run 1 task URLs to the Lobstr squid via `POST /v1/tasks` — done live 2026-09-22, confirmed via `GET /v1/tasks?squid=...`: exactly 10 tasks, no duplicates.
- [x] Confirm Apify's `themineworks/maps-leads` behaves as advertised with a small setup/smoke check before trusting it for Run 1 (Section 12, lesson 4) — done live 2026-09-22 (`outputs/apify/smoke-test-2026-09-22/`), passed, plus confirmed the `business_status: UNKNOWN` bug live and a major billing-fairness finding (Section 6): only verified-email leads are actually charged.
- [x] Outscraper budget decision made 2026-09-22: balance ($6.51) confirmed insufficient for the full design (~$18–36 estimated) and a top-up isn't available. Reduced to base-scrape-only (no email extraction/verification), 80 leads/sub-area instead of 200, ~$4.80 estimated worst-case. See Section 6 "Outscraper — reduced scope" and `scripts/lib/config.py` (`OUTSCRAPER_PER_SUBAREA_CAP`, `OUTSCRAPER_SKIP_ENRICHMENT`).
- [x] Sanity-check Lobstr's zoom choice (Section 6) — done live 2026-09-22 in two rounds: `12z` failed (leaked into NJ/Long Island/Glendale, only 32% unique), `14z` passed (86% unique, genuine borough/district neighborhoods). Squid's tasks rebuilt at `14z`, `max_results` restored to 200 after the test.
- [ ] Build the ~20–30-business hand-verified ground-truth sample across both industries and both cities (Section 10).

---

## EXECUTION CHECKLIST

1. **Setup**
   - [x] Add `OUTSCRAPER_API_KEY` to `.env`.
   - [x] Create a fresh Lobstr squid against crawler `4734d096159ef05210e0e1677e8be823` (`6afddf2feb67428f8bed0c383ff10380`); confirmed live `max_results` is per-task, capped at 200.
   - [x] Set Lobstr's squid concurrency to its documented max (20) and configure its full params block.
   - [x] Put the finalized sub-area `TARGETS` into `scripts/lib/config.py`.
   - [x] Add the 10 Run 1 task URLs to the Lobstr squid (`POST /v1/tasks`) — confirmed 10/10, no duplicates.
   - [ ] Recheck Apify's and Outscraper's live billing/account status — confirm nothing has changed since 2026-09-21/22.
   - [ ] Point Apify at `themineworks/maps-leads` explicitly (do not reuse any old actor ID); run one tiny setup/smoke check to confirm it behaves as documented.
   - [ ] Build the ground-truth sample (Section 10) before or in parallel with Run 1 — it doesn't depend on the runs finishing.

2. **Run 1 — Marketing agencies (10 borough/district sub-areas, up to 200 each)**
   - [ ] Fire the Run 1 request for all 3 providers, with the exact params and sub-area lists from Section 3/6.
   - [ ] Save every raw request/response under `data/<provider>/raw/`.
   - [ ] Record start/end timestamps and poll history for async providers.
   - [ ] Pull each provider's post-run billing balance immediately after completion.

3. **Run 2 — Restaurants (same 10 sub-areas, up to 200 each)**
   - [ ] Same as Run 1, with the restaurant search inputs. Keep every other parameter identical to Run 1 (Section 3).
   - [ ] Save raw evidence and post-run billing the same way.

4. **Analysis**
   - [ ] Pool and dedupe each provider's combined Run 1 + Run 2 output via `scripts/lib/dedupe.py`; export to `data/<provider>/exports/`.
   - [ ] Compute reliability, speed, cost, and scalability metrics per Section 9; write to `data/<provider>/analysis/`.
   - [ ] Run the ground-truth comparison (Section 10) against the hand-verified sample; write `ground-truth-match.json`.
   - [ ] Fill in Section 14's results table with real numbers.

5. **Scoring**
   - [ ] Walk each provider through elimination criteria E1–E6 (`criteria.md`) using the actual Run 1 + Run 2 data (e.g. E2's <50%-success-rate threshold is checked against the real reliability numbers, not assumed in advance).
   - [ ] Apply Section 13's scoring method (relative scoring for ratio metrics, anchor scale for qualitative ones) to every sub-criterion.
   - [ ] Total each provider's score out of 10.
   - [ ] Log every scored claim in `knowledge.md` with a pointer to the evidence file it traces back to, including the disclosed conflict of interest from the top of this document.
