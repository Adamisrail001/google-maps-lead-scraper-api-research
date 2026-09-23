"""Per-benchmark configuration, shared by every provider's scripts.

See IMPORTANT/testing-plan.md Sections 3 and 6 for the full rationale behind
these values - this file is just the executable form of that decision.

Google Maps caps any single search view at ~120-200 results (confirmed live:
Lobstr's max_results is hard-validated server-side at 200 per task; Apify's
themineworks/maps-leads has no internal grid-splitting and hits the same
wall per query; Outscraper's real per-query ceiling is unconfirmed but not
assumed higher). To reach >=500 unique leads per city, each city is split
into borough/district sub-areas, each queried independently and deduped -
not one whole-city query per city.
"""
import time

# Per-sub-area request cap. 200 for Lobstr/Apify (Lobstr's confirmed hard
# server-side maximum per task, 2026-09-22). Outscraper is reduced to 80 -
# its account balance ($6.51, confirmed live 2026-09-22) can't fund the full
# design even at base-scrape-only pricing ($3/1000); see testing-plan.md
# Section 6 "Outscraper - reduced scope" for the full cost math. This is a
# documented budget constraint, not a provider capability difference - never
# silently equalize it back to 200 in scripts or reporting.
PER_SUBAREA_CAP = 200
OUTSCRAPER_PER_SUBAREA_CAP = 80

# Outscraper runs base scrape only for this benchmark - no domains_service
# (email extraction) or emails_validator_service (verification) stage.
# Its email-related sub-scores must be reported "not tested (budget
# constraint)", never left blank or estimated (testing-plan.md Section 7/6).
OUTSCRAPER_SKIP_ENRICHMENT = True

# Borough/district centers used to build both the search query text
# ("<industry> in <district>") and Lobstr's coordinate-anchored task URLs.
# NYC uses its 5 official boroughs (no arbitrary cutoff). LA has no formal
# borough system, so 5 well-known major districts are used instead, chosen
# to match NYC's count for a comparable sub-area density per city.
SUBAREAS = {
    "New York": [
        {"name": "Manhattan", "lat": 40.7831, "lng": -73.9712},
        {"name": "Brooklyn", "lat": 40.6782, "lng": -73.9442},
        {"name": "Queens", "lat": 40.7282, "lng": -73.7949},
        {"name": "Bronx", "lat": 40.8448, "lng": -73.8648},
        {"name": "Staten Island", "lat": 40.5795, "lng": -74.1502},
    ],
    "Los Angeles": [
        {"name": "Downtown LA", "lat": 34.0407, "lng": -118.2468},
        {"name": "Hollywood", "lat": 34.0928, "lng": -118.3287},
        {"name": "Santa Monica", "lat": 34.0195, "lng": -118.4912},
        {"name": "Koreatown", "lat": 34.0577, "lng": -118.3005},
        {"name": "San Fernando Valley (Van Nuys)", "lat": 34.1867, "lng": -118.4487},
    ],
}

# Zoom level for Lobstr's map URLs. 12z was live-tested 2026-09-22 and
# FAILED - results leaked far outside the intended borough/district (NJ,
# Long Island, Glendale CA all showed up for NYC/LA sub-areas), and adjacent
# sub-areas overlapped so heavily that 50 raw results deduped to just 16
# unique (32%). 14z was tested next and CONFIRMED live 2026-09-22: 43/50
# unique (86%), and returned addresses landed in genuine borough/district
# neighborhoods (Queens: Jamaica/Woodhaven/Flushing; Van Nuys sub-area:
# Encino/Van Nuys/Sherman Oaks). Minor residual cross-border bleed remains
# (one Hoboken NJ result for Manhattan, one Glendale CA for an LA sub-area)
# - acceptable and documented, not a blocker. See testing-plan.md Section 6.
LOBSTR_ZOOM = 14


def _lobstr_task_url(industry_term, lat, lng):
    encoded_query = industry_term.replace(" ", "+")
    return (
        f"https://www.google.com/maps/search/{encoded_query}/"
        f"@{lat},{lng},{LOBSTR_ZOOM}z"
    )


def _build_run(label, industry, industry_term):
    targets = []
    for city, subareas in SUBAREAS.items():
        for sub in subareas:
            targets.append(
                {
                    "query": f"{industry} in {sub['name']}, {city}",
                    "city": city,
                    "subarea": sub["name"],
                    "leads": PER_SUBAREA_CAP,
                    "leads_outscraper": OUTSCRAPER_PER_SUBAREA_CAP,
                    "lobstr_task_url": _lobstr_task_url(industry_term, sub["lat"], sub["lng"]),
                }
            )
    return {"label": label, "industry": industry, "targets": targets}


# Two runs, identical in every parameter except industry (testing-plan.md
# Section 3). Each city is covered by 5 borough/district sub-area queries,
# each capped at PER_SUBAREA_CAP; results are pooled and deduped afterward
# (scripts/lib/dedupe.py) to reach the real per-city and per-run totals -
# not enforced as an exact 500/500 or 1,000 up front, since Google's own
# per-search ceiling makes that unenforceable at the request level.
RUN_1 = _build_run("marketing-agencies", "marketing agencies", "marketing agencies")
RUN_2 = _build_run("restaurants", "restaurants", "restaurants")

RUNS = [RUN_1, RUN_2]


def sleep(seconds):
    time.sleep(seconds)
