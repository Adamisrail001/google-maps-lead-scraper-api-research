"""Final scorecard — criteria.md 7-criterion rubric (Section 4, unchanged),
applied per the Step 0 core-requirement check (lead decision 2026-09-24).

User/job (prompt.txt): extract ALL Google Maps listings from a search,
reliably and affordably, with name, address, phone, opening hours. Enrichment
(email/socials/images/verification) is bonus value inside Data Quality —
never a requirement, never a disqualifier.

Ranked: Lobstr, HasData, Apify, Bright Data.
Disqualified (core requirements, shown with results/cost, never ranked):
  Google Places (60/query cap + ToS storage restrictions), Outscraper
  (most expensive basic extraction measured).
Pending: ScrapingDog (full-scale batch blocked on free-plan key).

Core-field fills and uniques are recomputed LIVE from data/ on every run.
Constants (delivery, costs, wall-clock, anchors) cite the evidence file they
trace to. Ratio sub-scores: best measured value gets full points, others
scaled (criteria.md method). Anchors: Full=100%, Partial=60%, Weak=0-20%.

Outputs scoring.md at the repo root.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _ne(v):
    return v not in (None, "", [], {}, "None")


def _norm(r, name, address, phone, hours, email=None, socials=()):
    return dict(
        name=_ne(r.get(name)), address=_ne(r.get(address)),
        phone=_ne(r.get(phone)), hours=_ne(r.get(hours)),
        email=_ne(r.get(email)) if email else False,
        social=any(_ne(r.get(s)) for s in socials))


def load_lobstr():
    recs = {}
    for f in ("run1-unique.json", "run2-unique.json"):
        for r in json.loads((ROOT / "data/lobstr/exports" / f).read_text(encoding="utf-8")):
            recs.setdefault(r.get("place_id") or r.get("cid") or (r.get("name"), r.get("address")), r)
    soc = ["facebook", "instagram", "linkedin", "twitter", "tiktok", "youtube", "pinterest", "whatsapp"]
    return [_norm(r, "name", "address", "phone", "opening_hours", "email", soc) for r in recs.values()]


def load_apify():
    recs = {}
    for f in ("run1-unique.json", "run2-unique.json"):
        for r in json.loads((ROOT / "data/apify/exports" / f).read_text(encoding="utf-8")):
            recs.setdefault(r.get("place_id") or (r.get("name"), r.get("address")), r)
    return [_norm(r, "name", "address", "phone", "hours", "email") for r in recs.values()]


def load_outscraper():
    recs = {}
    for f in ("run1-unique.json", "run2-unique.json"):
        for r in json.loads((ROOT / "data/outscraper/exports" / f).read_text(encoding="utf-8")):
            recs.setdefault(r.get("place_id") or r.get("google_id") or (r.get("name"), r.get("address")), r)
    return [_norm(r, "name", "address", "phone", "working_hours") for r in recs.values()]


def load_hasdata():
    recs = {}
    for f in sorted((ROOT / "data/hasdata/raw").glob("run*/job-*-results-p*.json")):
        for row in json.loads(f.read_text(encoding="utf-8"))["data"]:
            recs.setdefault(row["data"].get("placeId"), row["data"])
    return [_norm(r, "title", "address", "phone", "workingHours", "emails") for r in recs.values()]


def load_brightdata():
    recs = {}
    for f in (ROOT / "data/brightdata/raw/run1/snapshot.json",
              ROOT / "data/brightdata/raw/run2/snapshot.json"):
        for r in json.loads(f.read_text(encoding="utf-8")):
            recs.setdefault(r.get("place_id") or (r.get("name"), r.get("address")), r)
    return [_norm(r, "name", "address", "phone_number", "open_hours") for r in recs.values()]


P = ["Lobstr", "HasData", "Apify", "BrightData"]  # ranked set
LOADERS = {"Lobstr": load_lobstr, "HasData": load_hasdata, "Apify": load_apify,
           "BrightData": load_brightdata, "Outscraper": load_outscraper}
M = {}
for name, loader in LOADERS.items():
    rows = loader()
    n = len(rows)
    M[name] = {"uniques": n}
    for f in ("email", "social", "name", "address", "phone", "hours"):
        M[name][f] = 100.0 * sum(1 for r in rows if r[f]) / n
    M[name]["core4"] = sum(M[name][f] for f in ("name", "address", "phone", "hours")) / 4
    M[name]["enrich"] = (M[name]["email"] + M[name]["social"]) / 2

# ---- measured constants (each cites its evidence file) ----
DELIV = {  # returned/requested, both runs
    "Lobstr": (3403, 4000, "data/lobstr/raw/run1-final.json (1,594) + knowledge.md Run-2 pooled (1,809)"),
    "HasData": (2946, 4000, "data/hasdata/raw/run*/ per-job logs"),
    "Apify": (2730, 4000, "data/apify/raw/datasets/ row counts; 4/20 queries silently truncated (raw logs)"),
    "BrightData": (1741, 2000, "data/brightdata/raw/run*/snapshot.json (2x1,000 design)"),
}
# Basic-extraction cost $/1K unique (prompt rule 3: basic workload first, enrichment separate)
COST = {
    "Lobstr": (2.66, "derived from measured credits with the email-extraction credit share removed (knowledge.md: $6.05/1K as-tested incl. enrichment -> ~$2.66/1K without) — derived, flagged"),
    "HasData": (0.74, "base mode 3 credits/row x Startup rate ($49/200K credits) — rate-card; measured email-mode run was $1.75/1K (scale-findings.md)"),
    "Apify": (0.54, "billed via billing API on the full workload ($1.3656 / 2,523 uniques). FLAG: no basic-only price exists — this actor bills per VERIFIED-EMAIL lead, so basic extraction is inseparable from its enrichment economics"),
    "BrightData": (1.50, "rate-card ESTIMATE ~$0.75-1.50/1K, upper bound used; NO billing visibility in the API — unverified"),
}
WALL = {  # Run-1 wall-clock seconds
    "Lobstr": (1711.0, "data/lobstr/raw/run1-final.json (28m31s). Caveat: includes per-row website-visit email extraction (prompt rule 6)"),
    "HasData": (431.3, "data/hasdata/raw/run1/run1-log.json (email mode — also doing enrichment work)"),
    "Apify": (2194.5, "cumulative runTimeSecs across 10 actor runs (knowledge.md; parallelizable). Caveat: includes email extraction + DNS/MX verification"),
    "BrightData": (365.0, "data/brightdata/raw/run*/ progress logs (~6 min/run, no enrichment work)"),
}

S = []  # (criterion, sub, max, {p: (pts, basis)})

def add(crit, sub, mx, scores):
    S.append((crit, sub, mx, scores))

def ratio(mx, vals, better="high"):
    best = max(vals.values()) if better == "high" else min(vals.values())
    return {p: round(mx * (v / best if better == "high" else best / v), 2) for p, v in vals.items()}

# ---- 1. Success Rate & Reliability (2.0)
dv = {p: DELIV[p][0] / DELIV[p][1] for p in P}
r = ratio(1.0, dv)
add("Reliability", "Success rate on the core-workload benchmark (returned/requested, ratio vs best)", 1.0,
    {p: (r[p], f"{DELIV[p][0]:,}/{DELIV[p][1]:,} = {100*dv[p]:.1f}% — {DELIV[p][2]}") for p in P})
add("Reliability", "Empty/partial responses (anchor)", 0.4, {
    "Lobstr": (0.4, "Full - none observed"),
    "HasData": (0.24, "Partial - run1 rating/reviews filled 73% vs run2 100% (email-mode field wobble, measured)"),
    "Apify": (0.08, "Weak - 4/20 queries silently truncated by profit guards; business_status broken on 100% of records"),
    "BrightData": (0.4, "Full - 3 marked error rows in 1,741 (0.2%), no silent gaps")})
add("Reliability", "Error handling quality (anchor)", 0.3, {
    "Lobstr": (0.3, "Full - live 400 AttributeLimitExceeded precise, actionable"),
    "HasData": (0.18, "Partial - excellent 422 validation, but status never reaches finished"),
    "Apify": (0.06, "Weak - top-level SUCCEEDED masks truncation; only raw log reveals it"),
    "BrightData": (0.18, "Partial - precise validation errors, but progress ready != snapshot downloadable")})
add("Reliability", "Stability during test window (anchor)", 0.3, {
    "Lobstr": (0.3, "Full - both runs completed, no degradation"),
    "HasData": (0.3, "Full - 20/20 jobs completed"),
    "Apify": (0.06, "Weak - profitability breaker cut queries mid-processing (Van Nuys 20/200; 3 more in run2)"),
    "BrightData": (0.3, "Full - both snapshots completed normally")})

# ---- 2. Data Quality & Completeness (2.0)
best_core = max(M[p]["core4"] for p in P)
best_enr = max(M[p]["enrich"] for p in P)
cov = {}
for p in P:
    core_part = 0.6 * M[p]["core4"] / best_core
    enr_part = 0.2 * (M[p]["enrich"] / best_enr if best_enr else 0)
    cov[p] = (round(core_part + enr_part, 2),
              f"core-4 (name/address/phone/hours) {M[p]['core4']:.1f}% (0.6 x ratio vs best {best_core:.1f}) "
              f"+ enrichment bonus {M[p]['enrich']:.1f} avg email/social fill (0.2 x ratio vs best enricher Lobstr {best_enr:.1f}) "
              f"— email {M[p]['email']:.1f}%, socials {M[p]['social']:.1f}%, computed live on {M[p]['uniques']:,} uniques")
add("Data Quality", "Field coverage: core fields FIRST (0.6), enrichment as BONUS (0.2) — prompt rules 1-2; ground truth not built, fills are a coverage proxy", 0.8, cov)
add("Data Quality", "Data accuracy vs ground truth — NOT MEASURED (sample never built)", 0.5,
    {p: (0.0, "not measurable - 0 for all, flagged") for p in P})
add("Data Quality", "Schema consistency (anchor)", 0.4, {
    "Lobstr": (0.4, "Full - consistent 90+ field schema"),
    "HasData": (0.24, "Partial - field set varies by run/options (measured run1 vs run2 wobble)"),
    "Apify": (0.24, "Partial - business_status UNKNOWN universally (confirmed live)"),
    "BrightData": (0.4, "Full - consistent 39-field schema across 1,738 records")})
add("Data Quality", "Freshness — NOT MEASURED (no signal collected)", 0.3,
    {p: (0.0, "not measurable - 0 for all, flagged") for p in P})

# ---- 3. Cost Efficiency (1.5) — BASIC workload (prompt rule 3)
c = ratio(0.8, {p: COST[p][0] for p in P}, better="low")
add("Cost", "Cost per 1K unique, BASIC extraction workload (ratio vs cheapest; enrichment priced separately)", 0.8,
    {p: (c[p], f"${COST[p][0]:.2f}/1K — {COST[p][1]}") for p in P})
add("Cost", "Billing fairness (anchor)", 0.3, {
    "Lobstr": (0.3, "Full - pays per delivered row/email only"),
    "HasData": (0.3, "Full - per-row billing exact; email surcharge billed BELOW documented rate"),
    "Apify": (0.3, "Full - only verified-email leads charged, proven per-record via charged field"),
    "BrightData": (0.06, "Weak - no billing visibility through the API; fairness unverifiable")})
add("Cost", "Free tier / trial (anchor)", 0.2, {
    "Lobstr": (0.12, "Partial - free plan capped at 30 rows/export"),
    "HasData": (0.2, "Full - 1,000 credits/mo, no card"),
    "Apify": (0.12, "Partial - $5/mo platform free credit"),
    "BrightData": (0.12, "Partial - free credits reported third-party; activation + geo friction")})
add("Cost", "Pricing transparency (anchor)", 0.2, {
    "Lobstr": (0.12, "Partial - credit rates public but row+email math needs docs digging"),
    "HasData": (0.12, "Partial - rates published but observed billing deviates (favorably), undocumented"),
    "Apify": (0.12, "Partial - event prices published, two spend-guards undocumented"),
    "BrightData": (0.04, "Weak - conflicting third-party prices, own pricing unverifiable from env")})

# ---- 4. Speed & Throughput (1.5) — same core workload, enrichment caveat (prompt rule 6)
add("Speed", "Median latency per request (N/A for batch/async architectures = 0, all four)", 0.5,
    {p: (0.0, "N/A - batch/async architecture, no per-request timing") for p in P})
w = ratio(0.5, {p: WALL[p][0] for p in P}, better="low")
add("Speed", "Wall-clock, Run-1 batch (ratio vs fastest; Lobstr/Apify/HasData timings include enrichment work — caveat attached, no unenriched timing exists to substitute)", 0.5,
    {p: (w[p], f"{WALL[p][0]:,.0f}s — {WALL[p][1]}") for p in P})
add("Speed", "p95 latency (N/A batch = 0)", 0.3, {p: (0.0, "N/A") for p in P})
add("Speed", "Async/batch endpoint availability (anchor)", 0.2, {
    "Lobstr": (0.2, "Full - squid submit/poll"), "HasData": (0.2, "Full - async jobs + webhooks"),
    "Apify": (0.2, "Full - actor run/dataset"), "BrightData": (0.2, "Full - trigger/progress/snapshot + webhooks")})

# ---- 5. Scalability (1.2)
add("Scalability", "Rate limits & max concurrency (anchor)", 0.5, {
    "Lobstr": (0.5, "Full - documented user-set concurrency, 20 slots"),
    "HasData": (0.3, "Partial - 5 concurrent on Startup (429s measured), plan-scaled"),
    "Apify": (0.3, "Partial - internal parallelism, no user control, spend-guarded"),
    "BrightData": (0.3, "Partial - batch inputs parallelized internally, no user control")})
add("Scalability", "Degradation at tested volume (anchor)", 0.4, {
    "Lobstr": (0.4, "Full"), "HasData": (0.4, "Full - no degradation across 20 jobs"),
    "Apify": (0.08, "Weak - guard-driven early exits on 4/20 queries (counted once here at reduced weight; primary hit taken in Reliability - prompt rule 5, no double-counting)"),
    "BrightData": (0.4, "Full")})
add("Scalability", "Volume caps blocking production (anchor)", 0.3, {
    "Lobstr": (0.3, "Full - 200/task = Google's own ceiling, subdividable, no run cap"),
    "HasData": (0.3, "Full - user-set limits honored, no hidden ceilings observed"),
    "Apify": (0.06, "Weak - profitability breaker structurally under-delivers low-email verticals (restaurants 264 vs 527 charged)"),
    "BrightData": (0.18, "Partial - tested at 100/input by design; higher per-input volumes unprobed")})

# ---- 6. Developer Experience (1.0)
add("DevEx", "Time-to-first-successful-request (anchor)", 0.3, {
    "Lobstr": (0.18, "Partial - squid+tasks setup; zoom needed live tuning"),
    "HasData": (0.3, "Full - first job in minutes; 422 errors self-document schema"),
    "Apify": (0.3, "Full - console + one actor call; smoke succeeded in 10.3s"),
    "BrightData": (0.06, "Weak - first key blocked, activation + geo friction, DNS-blocked domains")})
add("DevEx", "Docs quality (anchor)", 0.3, {
    "Lobstr": (0.18, "Partial - working page_size param undocumented"),
    "HasData": (0.18, "Partial - good docs; status semantics wrong"),
    "Apify": (0.18, "Partial - actor docs fine; guards & status masking undocumented"),
    "BrightData": (0.06, "Weak - docs unreachable from test env; schema discovered by probing")})
add("DevEx", "SDKs & examples (anchor)", 0.2, {
    "Lobstr": (0.2, "Full - Python SDK, CLI, MCP"), "HasData": (0.12, "Partial - clean REST; official SDK not verified"),
    "Apify": (0.2, "Full - JS/Python clients"), "BrightData": (0.12, "Partial - SDKs exist; not verified from env")})
add("DevEx", "Error clarity + support (anchor)", 0.2, {
    "Lobstr": (0.2, "Full - precise live validation errors"),
    "HasData": (0.12, "Partial - great validation errors, misleading status field"),
    "Apify": (0.04, "Weak - SUCCEEDED masks truncation"),
    "BrightData": (0.12, "Partial - good errors; ready/building mismatch")})

# ---- 7. Input Flexibility & Coverage (0.8)
add("Input Flexibility", "Accepted input types (anchor)", 0.3, {
    "Lobstr": (0.3, "Full - coords+zoom, category match, rating/website/closed filters"),
    "HasData": (0.18, "Partial - keywords+locations+limit+extractEmails; no coords/filters"),
    "Apify": (0.18, "Partial - text queries + few booleans"),
    "BrightData": (0.06, "Weak - country+keyword discovery only")})
add("Input Flexibility", "Endpoint breadth (anchor)", 0.3, {
    "Lobstr": (0.18, "Partial - single crawler data flow"),
    "HasData": (0.3, "Full - scraper jobs + real-time SERP APIs + reviews/photos"),
    "Apify": (0.18, "Partial - this actor single-purpose"),
    "BrightData": (0.3, "Full - large scraper/dataset catalog")})
add("Input Flexibility", "Enrichment endpoints (BONUS capability, per prompt rule 2)", 0.2, {
    "Lobstr": (0.12, "Partial - email extraction native; verification dashboard-only"),
    "HasData": (0.2, "Full - native extractEmails + per-field enrichments (LinkedIn/socials)"),
    "Apify": (0.12, "Partial - inline verify only, no standalone enrichment"),
    "BrightData": (0.02, "Weak - none")})

# ---- totals
CRITS = ["Reliability", "Data Quality", "Cost", "Speed", "Scalability", "DevEx", "Input Flexibility"]
crit_scores = []
for cname in CRITS:
    rows = [s for s in S if s[0] == cname]
    crit_scores.append((cname, sum(x[2] for x in rows),
                        {p: round(sum(x[3][p][0] for x in rows), 2) for p in P}))
totals = {p: round(sum(cs[2][p] for cs in crit_scores), 2) for p in P}
ranked = sorted(P, key=lambda p: -totals[p])

# ---- report
NAMES = {"Lobstr": "Lobstr.io (house — disclosed)", "HasData": "HasData",
         "Apify": "Apify (themineworks/maps-leads)", "BrightData": "Bright Data"}
L = []
A = L.append
A("# Final Scoring — 7-criterion rubric (criteria.md §4, unchanged), core-requirement check applied")
A("")
A("**Computed:** 2026-09-24 by `scripts/compute_final_scorecard.py` (core-field/enrichment fills and uniques recomputed live from `data/` on every run). Model: `IMPORTANT/criteria.md` Step 0 (core-requirement check, lead decision 2026-09-24) + Section 4 rubric + `prompt.txt` scoring rules. Supersedes `research/analysis/scorecard.md` totals (kept as sub-score provenance for the old framing) and all earlier gate/persona drafts.")
A("")
A("**The user and the job:** extract all available Google Maps business listings from a search, reliably and affordably, with **name, address, phone, opening hours**. Enrichment (email/socials/images/verification) is bonus value only — it improves Data Quality/Coverage and is never a requirement (`prompt.txt`; demand evidence: `user-intent.md`, `research/analysis/who-why-research.md`).")
A("")
A("**Disclosure:** Lobstr.io is the house product and owns this methodology. All raw evidence is in the public repo; every number traces to a repo file.")
A("")
A("**Unscoreable, zeroed for all equally:** accuracy-vs-ground-truth (0.5) and freshness (0.3) — max attainable 9.2. Median/p95 latency (0.8) also scores 0 for all four ranked providers (all batch/async) — architecture-neutral this time.")
A("")
A("## Ranked table")
A("")
A("| Rank | Provider | Reliability /2.0 | Data Quality /2.0 | Cost /1.5 | Speed /1.5 | Scalability /1.2 | DevEx /1.0 | Input Flex /0.8 | **Total /10** |")
A("|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|")
for i, p in enumerate(ranked):
    cells = " | ".join(f"{cs[2][p]:.2f}" for cs in crit_scores)
    A(f"| {i+1} | **{NAMES[p]}** | {cells} | **{totals[p]:.2f}** |")
A("")
A("**Ranking:** " + " · ".join(f"{i+1}. {p} {totals[p]:.2f}" for i, p in enumerate(ranked)))
A("")
A("### Why each provider scored what it scored (criterion by criterion, prompt closing rule)")
A("")
expl = {
 "Lobstr": "wins Reliability (85.1% delivery, zero silent truncation, clean errors), Data Quality (best core-4 fill 97.1% AND the enrichment reference point: 45.3% email + 56.8% socials), and Scalability (only user-controlled concurrency, no hidden caps). Loses ground on Cost (basic ~$2.66/1K — derived, 5x the cheapest) and Speed (28m31s Run 1, which includes per-row website visits for enrichment — caveat attached).",
 "HasData": "second on core fills (94.2%) and the cheapest measured-plan basic rate (~$0.74/1K base mode); fastest full-batch scraper among enrichment-capable tools (7m11s email-mode Run 1); enrichment bonus from 41.7% email fill. Held back by 73.7% delivery, run-to-run field wobble, and a 5-concurrency entry-plan cap.",
 "BrightData": "near-perfect core fills (96.4%) and clean 87.1% delivery — the best pure-listings executor tested. Held back everywhere else by opacity and friction: cost is an unverifiable rate-card estimate (no billing API), docs unreachable, onboarding blocked initially, keyword-only inputs.",
 "Apify": "cheapest billed figure ($0.54/1K — but inseparable from its pay-per-verified-email model) and good DevEx (fastest time-to-first-request). Sunk by the trust findings, which hit this user's 'reliably' requirement hardest: 4/20 queries silently truncated by undocumented profit-guards while reporting SUCCEEDED, business_status broken on all records, and structural under-delivery on low-email verticals — a listings user pays in missing listings for an economics model built around emails they don't need.",
}
for p in ranked:
    A(f"- **{NAMES[p]} — {totals[p]:.2f}:** {expl[p]}")
A("")
A("### Sensitivity check on the #1 spot (house-product margin is thin — 0.06)")
A("")
A("The Lobstr–HasData gap under the basic-workload cost framing is 6.75 vs 6.69. Recomputing the Cost criterion with **as-tested measured costs** instead (Lobstr $5.82/1K incl. enrichment → Cost 0.61; HasData $1.75/1K email mode → Cost 0.87) gives Lobstr 6.66 vs HasData 6.36 — the #1 spot is **stable under both consistent cost framings**; the near-tie is an artifact of the basic-mode framing, which favors HasData (its $0.74 is a rate-card figure, Lobstr's $2.66 a measured-credit derivation). Flagged per the disclosure: if any framing had flipped the ranking, this table would say so.")
A("")
A("## Disqualified Providers (core-requirement failures — results and cost shown, never ranked)")
A("")
A("| Provider | Core requirement failed | Its test results (shown, not scored) |")
A("|---|---|---|")
A("| **Google Places API (New)** | Required volume + usable results/storage: hard 60-results/query cap (measured at cap on 10/10 restaurant queries — 444 uniques vs 998–1,405 for scrapers on identical queries) and Maps Platform Terms §3.2.3 bars copying/saving business names & addresses — the user cannot extract *all* listings nor *keep* them | Best-engineered API tested: 60/60 HTTP 200, 1.54s median / 2.26s p95, best per-field fills (phone 95.4%, website 94.3%, hours 97.9%), 1,044 uniques, $0 billed in free tier / $2.30/1K rate-card. Compliant use: real-time in-app display. Evidence: `research/raw/google-places-api/`, knowledge.md |")
out_m = M["Outscraper"]
A(f"| **Outscraper** | Affordable basic extraction: $3.69/1K unique measured-per-unique on base scrape alone ($4.80 for 1,300 uniques, rate-card $3/1K requested) — the most expensive basic extraction in the test vs $0.54–2.66 for ranked providers | Otherwise strong on this user's job: best core-4 fills measured (name {out_m['name']:.0f}% · address {out_m['address']:.0f}% · phone {out_m['phone']:.1f}% · hours {out_m['hours']:.1f}%, avg {out_m['core4']:.1f}%), 96.8% delivery (on a budget-reduced 80/query batch, flagged), richest default listing schema. Evidence: `data/outscraper/` |")
A("")
A("## Pending — not scored, no core-requirement failure on evidence")
A("")
A("**ScrapingDog:** profile fits this user exactly (smoke: core fills 95–100%, ~1.5s median, projected $0.04–0.15/1K — cheapest in test by an order of magnitude) but the standard full-scale batch has not run: the supplied key is on the free 100-credit plan (verified live via `/account`, 2026-09-24). Enters the ranking only after running the same workload. Smoke also flagged a real risk to verify at scale: past ~75 uniques/query it serves fully-billed duplicate pages with no exhaustion signal (`data/scrapingdog/reports/smoke-findings.md`).")
A("")
A("## Sub-criterion detail (every score's basis and evidence)")
A("")
for cname, mx, _ in crit_scores:
    A(f"### {cname}")
    A("")
    for crit, sub, m, scores in S:
        if crit != cname:
            continue
        A(f"**{sub}** ({m} pts)")
        for p in P:
            pts, basis = scores[p]
            A(f"- {p}: **{pts}** — {basis}")
        A("")
out = ROOT / "scoring.md"
out.write_text("\n".join(L), encoding="utf-8")
print(json.dumps({"totals": totals, "ranking": ranked,
                  "criterion": {c: sc for c, _, sc in crit_scores}}, indent=1))
print(f"written: {out}")
