"""Scrapingdog Google Maps API - full-scale benchmark, ll+page mode (2026-09-24).

Supersedes the start-offset attempt (scripts/scrapingdog_scale_run.py, raw in
data/scrapingdog/raw/run1|run2/): live A/B on the same query showed `start`
offsets barely advance results (~22 uniques/query) while the documented
`ll`+`page` pagination reaches deeper (43 uniques on the probe). This run uses
the correctly-configured mode: query = industry term, ll = sub-area center at
14z - the exact coordinate-anchored input shape Lobstr's tasks used, so the
comparison is like-for-like.

Full 10 pages per query (200 requested = the benchmark ceiling), NO early
stop: duplicate pages are fully billed by Scrapingdog with no exhaustion
signal (smoke finding), so fetching the whole ceiling measures that overbilling
exactly instead of estimating it. Stop only on HTTP error or an empty page.

Raw: data/scrapingdog/raw/run1-llpage/, run2-llpage/. Credits measured live
via /account before/after each run. API key scrubbed from saved responses.
"""
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.env import load_env, require_env  # noqa: E402
from lib.config import SUBAREAS  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
MAX_PAGES = 10
ZOOM = "14z"  # matches Lobstr's live-validated sub-area zoom (config.py)

load_env()
KEY = require_env("SCRAPINGDOG_API_KEY")

RUNS = [("run1", "marketing agencies"), ("run2", "restaurants")]
TARGETS = [(sub["name"], city, sub["lat"], sub["lng"])
           for city, subs in SUBAREAS.items() for sub in subs]


def account():
    with urllib.request.urlopen(
            f"https://api.scrapingdog.com/account?api_key={KEY}", timeout=30) as r:
        return json.load(r)


def fetch(term, ll, page):
    url = "https://api.scrapingdog.com/google_maps?" + urllib.parse.urlencode(
        {"api_key": KEY, "query": term, "ll": ll, "page": page})
    t0 = time.perf_counter()
    try:
        with urllib.request.urlopen(url, timeout=90) as r:
            return r.status, r.read().decode("utf-8", errors="replace"), round(time.perf_counter() - t0, 2)
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode(errors="replace")[:1000], round(time.perf_counter() - t0, 2)


def do_run(label, term):
    out = ROOT / "data" / "scrapingdog" / "raw" / f"{label}-llpage"
    out.mkdir(parents=True, exist_ok=True)
    a0 = account()
    log = {"run": label, "industry": term, "mode": "ll+page", "zoom": ZOOM,
           "max_pages": MAX_PAGES, "credits_used_before": a0["requestUsed"],
           "pack": a0["pack"], "started": datetime.now(timezone.utc).isoformat(),
           "requests": [], "per_query": {}}
    run_uniques = {}
    t_run = time.perf_counter()
    for sub, city, lat, lng in TARGETS:
        ll = f"@{lat},{lng},{ZOOM}"
        slug = f"{term}_{sub}_{city}".lower().replace(",", "").replace(" ", "_")[:70]
        q_seen = {}
        billed_dup_pages = 0
        for page in range(MAX_PAGES):
            status, body, lat_s = fetch(term, ll, page)
            n, new = 0, 0
            if status == 200:
                try:
                    d = json.loads(body)
                except json.JSONDecodeError:
                    d = {}
                results = d.get("search_results", [])
                n = len(results)
                for rec in results:
                    pid = rec.get("place_id") or rec.get("data_id")
                    if pid not in q_seen:
                        q_seen[pid] = rec
                        new += 1
                (out / f"{slug}-page{page}.json").write_text(
                    body.replace(KEY, "SCRAPINGDOG_API_KEY"), encoding="utf-8")
                if n > 0 and new == 0:
                    billed_dup_pages += 1
            log["requests"].append({"subarea": sub, "city": city, "page": page,
                                    "http": status, "latency_s": lat_s,
                                    "results": n, "new_unique": new})
            print(f"  {slug} p{page}: HTTP {status}, {n} res, {new} new, {lat_s}s", flush=True)
            if status != 200 or n == 0:
                break
        run_uniques.update(q_seen)
        log["per_query"][f"{sub}, {city}"] = {
            "unique": len(q_seen), "billed_all_duplicate_pages": billed_dup_pages}
    log["wall_clock_s"] = round(time.perf_counter() - t_run, 1)
    a1 = account()
    log["credits_used_after"] = a1["requestUsed"]
    log["credits_this_run"] = a1["requestUsed"] - a0["requestUsed"]
    log["unique_places_run"] = len(run_uniques)
    log["finished"] = datetime.now(timezone.utc).isoformat()
    (out / f"{label}-log.json").write_text(json.dumps(log, indent=2), encoding="utf-8")
    print(f"{label} DONE: {len(run_uniques)} unique, {log['credits_this_run']} credits, "
          f"{log['wall_clock_s']}s wall")
    return log


if __name__ == "__main__":
    a = account()
    assert a["pack"] == "lite", f"expected lite plan, got {a['pack']}"
    print(f"account OK: {a['pack']}, used {a['requestUsed']}/{a['requestLimit']}")
    summary = {}
    for label, term in RUNS:
        lg = do_run(label, term)
        summary[label] = {k: lg[k] for k in ("unique_places_run", "credits_this_run", "wall_clock_s")}
    print(json.dumps(summary, indent=1))
