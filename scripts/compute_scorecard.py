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

P = ["Lobstr", "Apify", "Outscraper", "Google"]

# (criterion, sub, max, {provider: (points, basis)}) — basis strings cite evidence
S = []

def add(crit, sub, mx, scores):
    S.append((crit, sub, mx, scores))

# ---- 2.1 Reliability (2.0)
add("Reliability", "Success rate (returned/requested, ratio vs best 93.5%)", 1.0, {
    "Lobstr": (0.85, "1,594/2,000 raw returned = 79.7% (run e57af71d)"),
    "Apify": (0.86, "1,608/2,000 = 80.4% (run1 datasets)"),
    "Outscraper": (1.0, "748/800 = 93.5% (512 unique + 236 dups)"),
    "Google": (1.0, "1,120/1,200 page-slots = 93.3% (run-log.json)")})
add("Reliability", "Empty/partial responses (anchor)", 0.4, {
    "Lobstr": (0.4, "Full - none observed"),
    "Apify": (0.08, "Weak - 4/20 queries silently truncated by profit guards; business_status broken on 100% of records"),
    "Outscraper": (0.4, "Full - none observed"),
    "Google": (0.4, "Full - none; sub-60 pages traced to data scarcity, documented")})
add("Reliability", "Error handling quality (anchor)", 0.3, {
    "Lobstr": (0.3, "Full - live 400 AttributeLimitExceeded was precise, actionable"),
    "Apify": (0.06, "Weak - top-level SUCCEEDED masks truncation; only raw log reveals it"),
    "Outscraper": (0.18, "Partial - no errors encountered, quality unassessed (flag: thin evidence)"),
    "Google": (0.3, "Full - structured google.rpc errors, clean retry semantics")})
add("Reliability", "Stability during window (anchor)", 0.3, {
    "Lobstr": (0.3, "Full - both runs completed, no degradation"),
    "Apify": (0.06, "Weak - profitability breaker cut queries mid-processing (Van Nuys 20/200; 3 more in run2)"),
    "Outscraper": (0.3, "Full - completed normally"),
    "Google": (0.3, "Full - 60/60 HTTP 200, latency stable (p95 2.26s)")})

# ---- 2.2 Data Quality (2.0)
add("Data Quality", "Field coverage, 10 lead fields, measured fill-rate proxy (ratio vs best 85.6) - GROUND TRUTH NOT BUILT, proxy flagged", 0.8, {
    "Lobstr": (0.80, "85.6 (core-8 93.3 + email 59 + socials 51)"),
    "Apify": (0.61, "65.3 (core-8 77.9 + email 32 + 0; no review-count field)"),
    "Outscraper": (0.66, "70.7 (core-8 88.4, category only 48%; no email/socials in base scope)"),
    "Google": (0.73, "78.2 (core-8 97.75 - best core fill - + email 0 + socials 0, fields absent from API)")})
add("Data Quality", "Accuracy vs ground truth - NOT MEASURED (sample never built)", 0.5, {
    p: (0.0, "not measurable - scored 0 for all, per plan rule") for p in P})
add("Data Quality", "Schema consistency (anchor)", 0.4, {
    "Lobstr": (0.4, "Full - consistent 90+ field schema"),
    "Apify": (0.24, "Partial - business_status returns UNKNOWN universally (confirmed live)"),
    "Outscraper": (0.4, "Full - consistent"),
    "Google": (0.4, "Full - typed, versioned schema")})
add("Data Quality", "Freshness - NOT MEASURED (no signal collected)", 0.3, {
    p: (0.0, "not measurable - scored 0 for all, per plan rule") for p in P})

# ---- 2.3 Cost (1.5)
add("Cost", "Cost per 1K unique (ratio vs cheapest $0.64)", 0.8, {
    "Lobstr": (0.085, "$6.05/1K measured credits x Growth rate"),
    "Apify": (0.8, "$0.64/1K - billed $0.8932 via billing API"),
    "Outscraper": (0.11, "$4.69/1K rate-card, base only"),
    "Google": (0.19, "$2.70/1K rate-card (run billed $0 in free tier - scored on rate card for comparability, flagged)")})
add("Cost", "Billing fairness (anchor)", 0.3, {
    "Lobstr": (0.3, "Full - pays per delivered row/email only"),
    "Apify": (0.3, "Full - only verified-email leads charged, proven per-record via charged field"),
    "Outscraper": (0.18, "Partial - per-record pricing, post-run billing reconciliation not captured"),
    "Google": (0.18, "Partial - billed per request regardless of yield (18.7 avg places on 20 requested)")})
add("Cost", "Free tier / trial (anchor)", 0.2, {
    "Lobstr": (0.12, "Partial - free plan capped at 30 rows/export"),
    "Apify": (0.12, "Partial - $5/mo platform free credit"),
    "Outscraper": (0.2, "Full - 500 free records/mo"),
    "Google": (0.2, "Full - 1,000 Enterprise+Atmosphere requests/mo (~18.7K places)")})
add("Cost", "Pricing transparency (anchor)", 0.2, {
    "Lobstr": (0.12, "Partial - credit rates public but row+email credit math needs docs digging; pricing page JS-only"),
    "Apify": (0.12, "Partial - event prices published, but two spend-guards undocumented"),
    "Outscraper": (0.2, "Full - flat $3/1K published"),
    "Google": (0.2, "Full - published SKU table, computable to the cent")})

# ---- 2.4 Speed (1.5)
add("Speed", "Median latency (only measurable for sync API; N/A batch = 0 per plan §9.2)", 0.5, {
    "Lobstr": (0.0, "N/A - batch architecture"),
    "Apify": (0.0, "N/A - batch architecture"),
    "Outscraper": (0.0, "N/A - async request architecture"),
    "Google": (0.5, "1.54s median, measured on 60 requests")})
add("Speed", "Wall-clock, Run-1 batch (ratio vs fastest 46s; NOTE: scrapers do website-visit enrichment per row - architecture caveat per plan §5)", 0.5, {
    "Lobstr": (0.013, "1,711s (28m31s, squid run)"),
    "Apify": (0.010, "2,195s cumulative across 10 actor runs (parallelizable)"),
    "Outscraper": (0.0, "not aggregated from raw evidence - unscored, flagged"),
    "Google": (0.5, "~46s for Run 1 (30 requests)")})
add("Speed", "p95 latency (N/A batch = 0)", 0.3, {
    "Lobstr": (0.0, "N/A"), "Apify": (0.0, "N/A"), "Outscraper": (0.0, "N/A"),
    "Google": (0.3, "2.26s p95 measured")})
add("Speed", "Async/batch endpoint availability (anchor)", 0.2, {
    "Lobstr": (0.2, "Full - squid submit/poll"),
    "Apify": (0.2, "Full - actor run/dataset"),
    "Outscraper": (0.2, "Full - async requests"),
    "Google": (0.04, "Weak - synchronous only, no batch/export endpoint")})

# ---- 2.5 Scalability (1.2)
add("Scalability", "Rate limits & max concurrency (anchor)", 0.5, {
    "Lobstr": (0.5, "Full - documented user-set concurrency, 20 slots"),
    "Apify": (0.3, "Partial - internal parallelism, no user control, spend-guarded"),
    "Outscraper": (0.3, "Partial - sequential 3-stage, no knob"),
    "Google": (0.5, "Full - generous documented QPS quotas")})
add("Scalability", "Stability/degradation at tested volume (anchor)", 0.4, {
    "Lobstr": (0.4, "Full"), "Apify": (0.08, "Weak - guard-driven early exits on 4/20 queries"),
    "Outscraper": (0.4, "Full"), "Google": (0.4, "Full")})
add("Scalability", "Volume caps blocking production (anchor)", 0.3, {
    "Lobstr": (0.3, "Full - 200/task, subdividable, no run cap (max_unique null)"),
    "Apify": (0.06, "Weak - profitability breaker structurally under-delivers low-email verticals (restaurants: 264 vs 527 charged)"),
    "Outscraper": (0.18, "Partial - balance-driven ceiling; single-query max unconfirmed"),
    "Google": (0.06, "Weak - hard 60/query cap, hit on 10/10 restaurant queries")})

# ---- 2.6 Usability (1.8)
add("Usability", "Input flexibility (anchor)", 0.3, {
    "Lobstr": (0.3, "Full - coords+zoom, category match, rating/website/closed filters"),
    "Apify": (0.18, "Partial - text queries + few booleans"),
    "Outscraper": (0.3, "Full - query/region/limit/status/dedup"),
    "Google": (0.18, "Partial - text query + location bias; no lead-oriented filters")})
add("Usability", "Endpoint/platform coverage (anchor)", 0.3, {
    "Lobstr": (0.18, "Partial - single crawler data flow (other crawlers separate)"),
    "Apify": (0.18, "Partial - this actor single-purpose (marketplace separate)"),
    "Outscraper": (0.3, "Full - search, reviews, photos, enrichment endpoints"),
    "Google": (0.3, "Full - text/nearby/details/photos/autocomplete")})
add("Usability", "Enrichment endpoints (anchor)", 0.2, {
    "Lobstr": (0.12, "Partial - email extraction native, but verification dashboard-only (no API)"),
    "Apify": (0.12, "Partial - inline verify only, no standalone enrichment"),
    "Outscraper": (0.2, "Full - separate extraction + verification services"),
    "Google": (0.02, "Weak - none")})
add("Usability", "Time-to-first-successful-request (anchor)", 0.3, {
    "Lobstr": (0.18, "Partial - squid+tasks setup; zoom needed live tuning (12z failed, 14z passed)"),
    "Apify": (0.3, "Full - console + one actor call; smoke succeeded in 10.3s"),
    "Outscraper": (0.18, "Partial - not timed this project (flag: thin evidence)"),
    "Google": (0.3, "Full - key to first data in minutes, single endpoint")})
add("Usability", "Documentation quality (anchor)", 0.3, {
    "Lobstr": (0.18, "Partial - working page_size param undocumented; task URL format documented"),
    "Apify": (0.18, "Partial - actor docs fine; guards & status masking undocumented"),
    "Outscraper": (0.18, "Partial - docs exist but site unreachable from test env; schema verified via mirrors"),
    "Google": (0.3, "Full - complete, versioned, searchable")})
add("Usability", "SDKs & examples (anchor)", 0.2, {
    "Lobstr": (0.2, "Full - Python SDK, CLI, MCP"),
    "Apify": (0.2, "Full - JS/Python clients"),
    "Outscraper": (0.2, "Full - official Python client"),
    "Google": (0.2, "Full - official client libraries")})
add("Usability", "Error clarity + support (anchor)", 0.2, {
    "Lobstr": (0.2, "Full - precise live validation errors"),
    "Apify": (0.04, "Weak - SUCCEEDED status masks truncation"),
    "Outscraper": (0.12, "Partial - untested"),
    "Google": (0.2, "Full - structured errors")})

# totals
crits = []
for c in ["Reliability", "Data Quality", "Cost", "Speed", "Scalability", "Usability"]:
    rows = [s for s in S if s[0] == c]
    crits.append((c, sum(r[2] for r in rows), {p: round(sum(r[3][p][0] for r in rows), 2) for p in P}))

totals = {p: round(sum(ct[2][p] for ct in crits), 2) for p in P}

lines = ["# Benchmark Scorecard — 10-Point Rubric (testing-plan §2, method §13)", "",
         "**Computed:** 2026-09-23 by `scripts/compute_scorecard.py` (rerun it to regenerate; every sub-score carries its basis + evidence).",
         "",
         "> **Unscoreable on existing evidence, zeroed for ALL providers equally (0.8 pts):** Accuracy-vs-ground-truth (0.5 — sample never built, testing-plan §10 open item) and Freshness (0.3 — no signal collected). Max attainable = 9.2.",
         "> **Rubric artifacts to keep in mind:** wall-clock ratio scoring severely penalizes batch scrapers that do per-row website-visit enrichment vs a sync API returning 20 records/call (§5 reporting rule caveat applies); Outscraper scored on its reduced budget scope (base scrape, 80/query); Google's cost scored on rate-card since its run billed $0 in free tier.",
         "> **Disclosure:** Lobstr.io is the house product. Per criteria.md writer rules, the aggregate winner is whoever scores highest — no predetermined outcome.",
         ""]
lines.append("## Criterion scores")
lines.append("")
lines.append("| Criterion | Max | " + " | ".join(P) + " |")
lines.append("|---|---:|" + "---:|" * len(P))
for c, mx, sc in crits:
    lines.append(f"| {c} | {mx:.1f} | " + " | ".join(f"{sc[p]:.2f}" for p in P) + " |")
lines.append(f"| **TOTAL /10** | 10.0 | " + " | ".join(f"**{totals[p]:.2f}**" for p in P) + " |")
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
