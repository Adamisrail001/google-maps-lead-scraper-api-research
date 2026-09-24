"""Compute the 10-point benchmark scorecard (testing-plan §2 rubric, §13 method).

Every sub-score below is either a RATIO (relative to the best measured value,
per §13) or an ANCHOR (Full=100%, Partial=60%, Weak=0-20% of sub-criterion
points), each with its rationale and evidence pointer. Accuracy and Freshness
are scored 0 for ALL providers (ground-truth sample never built; no freshness
signal collected) and flagged — 0.8 of the 10 points are unscoreable on
existing evidence for every provider equally.

Outputs research/analysis/scorecard.md.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "research" / "analysis" / "scorecard.md"

P = ["Lobstr", "Apify", "HasData", "BrightData"]  # scored providers ONLY
# Google Places and Outscraper are DISQUALIFIED (core requirements) and receive
# NO score - their measured results stay in knowledge.md and data/, never as points.

# (criterion, sub, max, {provider: (points, basis)}) — basis strings cite evidence
S = []

def add(crit, sub, mx, scores):
    S.append((crit, sub, mx, scores))

# ---- 2.1 Reliability (2.0)
add("Reliability", "Success rate, BOTH runs (returned/requested, ratio vs best 96.8%)", 1.0, {
    "Lobstr": (0.88, "(1,594+1,809)/4,000 = 85.1% (runs e57af71d + run2 pooled)"),
    "Apify": (0.71, "(1,608+1,122)/4,000 = 68.3% - run2 restaurants collapsed to 56.1% via profit-breaker"),
    "HasData": (0.76, "2,946/4,000 = 73.7% (scale runs, per-job logs)"),
    "BrightData": (0.90, "1,741/2,000 = 87.1% (2x1,000 design, snapshots)")})
add("Reliability", "Empty/partial responses (anchor)", 0.4, {
    "Lobstr": (0.4, "Full - none observed"),
    "Apify": (0.08, "Weak - 4/20 queries silently truncated by profit guards; business_status broken on 100% of records"),
    "HasData": (0.24, "Partial - run1 rating/reviews filled only 73% vs run2 100% (email-mode field wobble, measured)"),
    "BrightData": (0.4, "Full - 3 marked error rows in 1,741 (0.2%), no silent gaps")})
add("Reliability", "Error handling quality (anchor)", 0.3, {
    "Lobstr": (0.3, "Full - live 400 AttributeLimitExceeded was precise, actionable"),
    "Apify": (0.06, "Weak - top-level SUCCEEDED masks truncation; only raw log reveals it"),
    "HasData": (0.18, "Partial - excellent 422 validation, but status never reaches finished (misleading)"),
    "BrightData": (0.18, "Partial - precise validation errors, but progress ready != snapshot downloadable")})
add("Reliability", "Stability during window (anchor)", 0.3, {
    "Lobstr": (0.3, "Full - both runs completed, no degradation"),
    "Apify": (0.06, "Weak - profitability breaker cut queries mid-processing (Van Nuys 20/200; 3 more in run2)"),
    "HasData": (0.3, "Full - 20/20 jobs completed, no degradation"),
    "BrightData": (0.3, "Full - both snapshots completed normally")})

# ---- 2.2 Data Quality (2.0)
add("Data Quality", "Field coverage, 10 lead fields, BOTH-run measured fill-rate proxy (ratio vs best 85.8) - GROUND TRUTH NOT BUILT, proxy flagged", 0.8, {
    "Lobstr": (0.80, "85.8 (core-8 95.7 weighted both runs + email 45.6 + socials ~47)"),
    "Apify": (0.63, "67.7 (core-8 81.1 + email 28.3 verified + 0; no review-count field)"),
    "HasData": (0.74, "79.2 (core-8 93.8 + email 42 + socials 0 - separate enrichments untested)"),
    "BrightData": (0.73, "77.8 (core-8 97.2, second-best core fill + email 0 + socials 0, fields absent)")})
add("Data Quality", "Accuracy vs ground truth - NOT MEASURED (sample never built)", 0.5, {
    p: (0.0, "not measurable - scored 0 for all, per plan rule") for p in P})
add("Data Quality", "Schema consistency (anchor)", 0.4, {
    "Lobstr": (0.4, "Full - consistent 90+ field schema"),
    "Apify": (0.24, "Partial - business_status returns UNKNOWN universally (confirmed live)"),
    "HasData": (0.24, "Partial - field set varies by run/options (measured run1 vs run2 wobble)"),
    "BrightData": (0.4, "Full - consistent 39-field schema across 1,738 records")})
add("Data Quality", "Freshness - NOT MEASURED (no signal collected)", 0.3, {
    p: (0.0, "not measurable - scored 0 for all, per plan rule") for p in P})

# ---- 2.3 Cost (1.5)
add("Cost", "Cost per 1K unique, BOTH runs (ratio vs cheapest $0.54)", 0.8, {
    "Lobstr": (0.07, "$5.82/1K - 8,968 credits measured (3,626 + 5,342, runs e57af71d + 6b7150f5) x Growth rate / 2,567 uniques"),
    "Apify": (0.8, "$0.54/1K - billed $1.3656 total via billing API / 2,523 uniques"),
    "HasData": (0.25, "$1.75/1K measured (17,518 credits x Startup rate / 2,456 uniques)"),
    "BrightData": (0.29, "~$1.50/1K RATE-CARD ESTIMATE - no billing field in API, unverified, flagged")})
add("Cost", "Billing fairness (anchor)", 0.3, {
    "Lobstr": (0.3, "Full - pays per delivered row/email only"),
    "Apify": (0.3, "Full - only verified-email leads charged, proven per-record via charged field"),
    "HasData": (0.3, "Full - per-row billing exact; email surcharge billed BELOW documented rate (158 vs 200)"),
    "BrightData": (0.06, "Weak - no billing visibility through the API at all; fairness unverifiable")})
add("Cost", "Free tier / trial (anchor)", 0.2, {
    "Lobstr": (0.12, "Partial - free plan capped at 30 rows/export"),
    "Apify": (0.12, "Partial - $5/mo platform free credit"),
    "HasData": (0.2, "Full - 1,000 credits/mo, no card (covered the whole smoke)"),
    "BrightData": (0.12, "Partial - free monthly credits reported third-party; account required activation + geo friction")})
add("Cost", "Pricing transparency (anchor)", 0.2, {
    "Lobstr": (0.12, "Partial - credit rates public but row+email credit math needs docs digging; pricing page JS-only"),
    "Apify": (0.12, "Partial - event prices published, but two spend-guards undocumented"),
    "HasData": (0.12, "Partial - credit rates published but observed billing deviates (favorably) undocumented"),
    "BrightData": (0.04, "Weak - conflicting third-party prices ($0.75-1.50/1K), own pricing unverifiable from env")})

# ---- 2.4 Speed (1.5)
add("Speed", "Median latency (only measurable for sync API; N/A batch = 0 per plan §9.2)", 0.5, {
    "Lobstr": (0.0, "N/A - batch architecture"),
    "Apify": (0.0, "N/A - batch architecture"),
    "HasData": (0.0, "N/A - async jobs"),
    "BrightData": (0.0, "N/A - async snapshots")})
add("Speed", "Wall-clock, Run-1 batch (ratio vs fastest 46s; NOTE: scrapers do website-visit enrichment per row - architecture caveat per plan §5)", 0.5, {
    "Lobstr": (0.013, "1,711s (28m31s, squid run)"),
    "Apify": (0.010, "2,195s cumulative across 10 actor runs (parallelizable)"),
    "HasData": (0.06, "~367s avg per run (logs; fastest scraper tested)"),
    "BrightData": (0.06, "~365s avg per run (progress logs)")})
add("Speed", "p95 latency (N/A batch = 0)", 0.3, {
    "Lobstr": (0.0, "N/A"), "Apify": (0.0, "N/A"), "Outscraper": (0.0, "N/A"),
    "HasData": (0.0, "N/A"),
    "BrightData": (0.0, "N/A")})
add("Speed", "Async/batch endpoint availability (anchor)", 0.2, {
    "Lobstr": (0.2, "Full - squid submit/poll"),
    "Apify": (0.2, "Full - actor run/dataset"),
    "HasData": (0.2, "Full - async jobs + webhooks + paginated results"),
    "BrightData": (0.2, "Full - trigger/progress/snapshot + webhook delivery")})

# ---- 2.5 Scalability (1.2)
add("Scalability", "Rate limits & max concurrency (anchor)", 0.5, {
    "Lobstr": (0.5, "Full - documented user-set concurrency, 20 slots"),
    "Apify": (0.3, "Partial - internal parallelism, no user control, spend-guarded"),
    "HasData": (0.3, "Partial - 5 concurrent on Startup (429s measured), plan-scaled"),
    "BrightData": (0.3, "Partial - batch inputs parallelized internally, no user control")})
add("Scalability", "Stability/degradation at tested volume (anchor)", 0.4, {
    "Lobstr": (0.4, "Full"), "Apify": (0.08, "Weak - guard-driven early exits on 4/20 queries"),
    "HasData": (0.4, "Full - no degradation across 20 jobs"), "BrightData": (0.4, "Full")})
add("Scalability", "Volume caps blocking production (anchor)", 0.3, {
    "Lobstr": (0.3, "Full - 200/task, subdividable, no run cap (max_unique null)"),
    "Apify": (0.06, "Weak - profitability breaker structurally under-delivers low-email verticals (restaurants: 264 vs 527 charged)"),
    "HasData": (0.3, "Full - user-set limits honored, no hidden ceilings observed"),
    "BrightData": (0.18, "Partial - tested at 100/input by design; higher per-input volumes unprobed")})

# ---- 2.6 Usability (1.8)
add("Usability", "Input flexibility (anchor)", 0.3, {
    "Lobstr": (0.3, "Full - coords+zoom, category match, rating/website/closed filters"),
    "Apify": (0.18, "Partial - text queries + few booleans"),
    "HasData": (0.18, "Partial - keywords+locations+limit+extractEmails; no coords/filters"),
    "BrightData": (0.06, "Weak - country+keyword discovery only; no text-query or location params")})
add("Usability", "Endpoint/platform coverage (anchor)", 0.3, {
    "Lobstr": (0.18, "Partial - single crawler data flow (other crawlers separate)"),
    "Apify": (0.18, "Partial - this actor single-purpose (marketplace separate)"),
    "HasData": (0.3, "Full - scraper jobs + real-time SERP APIs + reviews/photos"),
    "BrightData": (0.3, "Full - large scraper/dataset catalog (1,763 datasets listed)")})
add("Usability", "Enrichment endpoints (anchor)", 0.2, {
    "Lobstr": (0.12, "Partial - email extraction native, but verification dashboard-only (no API)"),
    "Apify": (0.12, "Partial - inline verify only, no standalone enrichment"),
    "HasData": (0.2, "Full - native extractEmails + per-field enrichments (LinkedIn/socials, 5 cr)"),
    "BrightData": (0.02, "Weak - none")})
add("Usability", "Time-to-first-successful-request (anchor)", 0.3, {
    "Lobstr": (0.18, "Partial - squid+tasks setup; zoom needed live tuning (12z failed, 14z passed)"),
    "Apify": (0.3, "Full - console + one actor call; smoke succeeded in 10.3s"),
    "HasData": (0.3, "Full - first job in minutes; 422 errors self-document the schema"),
    "BrightData": (0.06, "Weak - first key blocked (Customer is not active), activation + geo friction, DNS-blocked domains")})
add("Usability", "Documentation quality (anchor)", 0.3, {
    "Lobstr": (0.18, "Partial - working page_size param undocumented; task URL format documented"),
    "Apify": (0.18, "Partial - actor docs fine; guards & status masking undocumented"),
    "HasData": (0.18, "Partial - good docs; status semantics wrong; billing discount undocumented"),
    "BrightData": (0.06, "Weak - docs unreachable from test env; schema discovered by probing")})
add("Usability", "SDKs & examples (anchor)", 0.2, {
    "Lobstr": (0.2, "Full - Python SDK, CLI, MCP"),
    "Apify": (0.2, "Full - JS/Python clients"),
    "HasData": (0.12, "Partial - clean REST + examples; official SDK not verified"),
    "BrightData": (0.12, "Partial - SDKs exist per ecosystem; not verified from this env")})
add("Usability", "Error clarity + support (anchor)", 0.2, {
    "Lobstr": (0.2, "Full - precise live validation errors"),
    "Apify": (0.04, "Weak - SUCCEEDED status masks truncation"),
    "HasData": (0.12, "Partial - great validation errors, misleading status field"),
    "BrightData": (0.12, "Partial - good errors; ready/building mismatch")})

# totals
crits = []
for c in ["Reliability", "Data Quality", "Cost", "Speed", "Scalability", "Usability"]:
    rows = [s for s in S if s[0] == c]
    crits.append((c, sum(r[2] for r in rows), {p: round(sum(r[3][p][0] for r in rows), 2) for p in P}))

totals = {p: round(sum(ct[2][p] for ct in crits), 2) for p in P}

DQ = {"Google Places API (New)": "DISQUALIFIED — NOT SCORED. Hard 60-results/query cap (measured at cap on 10/10 restaurant queries) and Maps Platform Terms §3.2.3 storage restrictions conflict with the core requirement of extracting and keeping all available listings. Measured results shown in knowledge.md / research/raw/google-places-api/ as findings, never as points.",
      "Outscraper": "DISQUALIFIED — NOT SCORED. Most expensive basic extraction measured in the test ($3.69/1K unique, base scrape only, vs $0.54–2.66 for scored providers) — fails the affordable-basic-extraction core requirement. Measured results (97.5% core-4 fills, 96.8% delivery on its budget-reduced 80/query batch) shown in data/outscraper/ and knowledge.md as findings, never as points."}

lines = ["# Benchmark Scorecard — 10-Point Rubric (testing-plan §2, method §13)", "",
         "**Computed:** 2026-09-23 by `scripts/compute_scorecard.py` (rerun it to regenerate; every sub-score carries its basis + evidence).",
         "",
         "> **Disqualification rule (corrected 2026-09-24): disqualified providers receive NO score.** Google Places API (New) and Outscraper are disqualified on core requirements (see the Disqualified section below) and do not appear in any score table. Earlier versions of this file showed them with \"reference\" scores — that display is retired; git history preserves it.",
         "> **Comparability note:** HasData and Bright Data scored from their 2026-09-23 stage-2 runs (HasData: benchmark-standard 200/sub-area; Bright Data: 2x1,000 brief design, 100/input) - identical query set, different volume ceilings, flagged where it matters. Bright Data cost is a rate-card ESTIMATE (no billing visibility).",
         "> **Unscoreable on existing evidence, zeroed for ALL providers equally (0.8 pts):** Accuracy-vs-ground-truth (0.5 — sample never built, testing-plan §10 open item) and Freshness (0.3 — no signal collected). Max attainable = 9.2.",
         "> **Rubric artifacts to keep in mind:** wall-clock ratio scoring severely penalizes batch scrapers that do per-row website-visit enrichment (§5 reporting rule caveat applies). NOTE: this file is the superseded v1 rubric — the scoring of record is scoring.md (scripts/compute_final_scorecard.py).",
         "> **Disclosure:** Lobstr.io is the house product. Per criteria.md writer rules, the aggregate winner is whoever scores highest — no predetermined outcome.",
         ""]
lines.append("## Criterion scores")
lines.append("")
lines.append("| Criterion | Max | " + " | ".join(P) + " |")
lines.append("|---|---:|" + "---:|" * len(P))
for c, mx, sc in crits:
    lines.append(f"| {c} | {mx:.1f} | " + " | ".join(f"{sc[p]:.2f}" for p in P) + " |")
lines.append(f"| **TOTAL /10** | 10.0 | " + " | ".join(
    f"**{totals[p]:.2f}**" + (" (ref — DQ)" if p in DQ else "") for p in P) + " |")
lines.append("")
ranked = sorted((p for p in P if p not in DQ), key=lambda p: -totals[p])
lines.append("**Ranking (scored providers only):** " +
             " · ".join(f"{i+1}. {p} {totals[p]:.2f}" for i, p in enumerate(ranked)))
lines.append("")
lines.append("## Disqualified — not scored")
for p, why in DQ.items():
    lines.append("")
    lines.append(f"**{p}:** {why}")
lines.append("")
lines.append("## Sub-criterion detail")
lines.append("")
for c, mx, _ in crits:
    lines.append(f"### {c}")
    lines.append("")
    for crit, sub, m, scores in S:
        if crit != c:
            continue
        lines.append(f"**{sub}** ({m} pts)")
        for p in P:
            pts, basis = scores[p]
            lines.append(f"- {p}: **{pts}** — {basis}")
        lines.append("")
OUT.write_text("\n".join(lines), encoding="utf-8")
print(json.dumps({"criterion_scores": {c: sc for c, _, sc in crits}, "totals": totals}, indent=1))
