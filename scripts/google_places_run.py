"""Google Places API (New) benchmark run - the official-API contender.

Same workload as the scraper benchmark (scripts/lib/config.py RUNS): 2 runs x
10 sub-area text queries. Google's Text Search hard-caps each query at 60
results (20/page x 3 pages via nextPageToken), so per-query volume is expected
to fall short of the scrapers' 200-cap - that gap is a measured finding, not
an error.

Field mask requests the maximal lead-relevant set; phone/website/hours/rating
sit in the Enterprise tier and reviews/editorialSummary in Enterprise +
Atmosphere, so every request bills as Text Search Enterprise + Atmosphere
(SKU 120C-BEC3-B48F, $40/1K after 1,000 free events/mo - pricing fetched live
2026-09-23). Full run = ~60 requests, inside the free tier.

Usage:
  python scripts/google_places_run.py --smoke   # 1 query, 1 page
  python scripts/google_places_run.py           # full 2-run benchmark

Outputs under research/raw/google-places-api/:
  run{n}-{subarea-slug}-page{p}.json   raw response, unmodified
  run-log.json                         per-request timings, counts, errors
API key comes from .env (GOOGLE_PLACES_API_KEY) and is never written to disk.
"""
import json
import re
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.env import load_env, require_env  # noqa: E402
from lib.config import RUNS  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "research" / "raw" / "google-places-api"
ENDPOINT = "https://places.googleapis.com/v1/places:searchText"

FIELD_MASK = ",".join([
    # Essentials
    "places.id", "nextPageToken",
    # Pro
    "places.displayName", "places.formattedAddress", "places.addressComponents",
    "places.location", "places.types", "places.primaryType", "places.googleMapsUri",
    "places.businessStatus", "places.photos",
    # Enterprise
    "places.nationalPhoneNumber", "places.internationalPhoneNumber",
    "places.websiteUri", "places.rating", "places.userRatingCount",
    "places.regularOpeningHours", "places.priceLevel",
    # Enterprise + Atmosphere
    "places.reviews", "places.editorialSummary",
])

PAGE_SIZE = 20
MAX_PAGES = 3  # 60-result documented ceiling per text query


def slug(text):
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


def search_page(api_key, query, page_token=None):
    body = {"textQuery": query, "pageSize": PAGE_SIZE}
    if page_token:
        body["pageToken"] = page_token
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(body).encode(),
        headers={
            "Content-Type": "application/json",
            "X-Goog-Api-Key": api_key,
            "X-Goog-FieldMask": FIELD_MASK,
        },
    )
    t0 = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read())
            status = resp.status
    except urllib.error.HTTPError as e:
        data = json.loads(e.read() or b"{}")
        status = e.code
    elapsed = time.perf_counter() - t0
    return status, data, elapsed


def run_query(api_key, run_label, target, log):
    query = target["query"]
    qslug = slug(f"{target['subarea']}_{target['city']}")
    places_total = 0
    token = None
    for page in range(1, MAX_PAGES + 1):
        # nextPageToken can need a moment to become valid; retry briefly
        for attempt in range(4):
            status, data, elapsed = search_page(api_key, query, token)
            if status == 200 or attempt == 3:
                break
            time.sleep(1.5 * (attempt + 1))
        raw_path = OUT / f"{run_label}-{qslug}-page{page}.json"
        raw_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        n = len(data.get("places", []))
        places_total += n
        log["requests"].append({
            "run": run_label, "query": query, "page": page, "http_status": status,
            "latency_s": round(elapsed, 3), "places_returned": n,
            "has_next_page": bool(data.get("nextPageToken")),
            "error": data.get("error", {}).get("message") if status != 200 else None,
            "ts": datetime.now(timezone.utc).isoformat(),
        })
        print(f"  {query} page {page}: HTTP {status}, {n} places, {elapsed:.2f}s")
        token = data.get("nextPageToken")
        if status != 200 or not token:
            break
    return places_total


def main():
    load_env()
    api_key = require_env("GOOGLE_PLACES_API_KEY")
    OUT.mkdir(parents=True, exist_ok=True)
    smoke = "--smoke" in sys.argv

    log = {"started": datetime.now(timezone.utc).isoformat(),
           "field_mask": FIELD_MASK, "page_size": PAGE_SIZE, "max_pages": MAX_PAGES,
           "requests": [], "totals": {}}

    if smoke:
        target = RUNS[0]["targets"][0]
        status, data, elapsed = search_page(api_key, target["query"])
        n = len(data.get("places", []))
        print(f"SMOKE: HTTP {status}, {n} places, {elapsed:.2f}s")
        if status != 200:
            print(json.dumps(data.get("error", data), indent=2)[:2000])
            sys.exit(1)
        (OUT / "smoke-test.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
        first = data["places"][0]
        print("fields on first place:", sorted(first.keys()))
        return

    grand_total = 0
    t_start = time.perf_counter()
    for run in RUNS:
        run_label = "run1" if run is RUNS[0] else "run2"
        print(f"== {run_label}: {run['industry']} ==")
        run_total = 0
        for target in run["targets"]:
            run_total += run_query(api_key, run_label, target, log)
        log["totals"][run_label] = run_total
        grand_total += run_total
    log["totals"]["grand_total_places_raw"] = grand_total
    log["totals"]["total_requests"] = len(log["requests"])
    log["totals"]["wall_clock_s"] = round(time.perf_counter() - t_start, 1)
    log["finished"] = datetime.now(timezone.utc).isoformat()
    (OUT / "run-log.json").write_text(json.dumps(log, indent=2), encoding="utf-8")
    print(f"TOTAL: {grand_total} places in {log['totals']['total_requests']} requests, "
          f"{log['totals']['wall_clock_s']}s wall-clock")


if __name__ == "__main__":
    main()
