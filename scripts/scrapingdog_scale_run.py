"""Scrapingdog Google Maps API - full-scale benchmark run (Lite plan, 2026-09-24).

Benchmark-standard workload (testing-plan Section 3): 2 runs (marketing
agencies, restaurants) x 10 NYC/LA borough/district sub-areas, up to 200
requested results per query - Scrapingdog serves 20/request via the `start`
offset (0,20,...,180 = 10 pages = the same 200/query ceiling every other
provider faced).

Smoke-test caveat applied (data/scrapingdog/reports/smoke-findings.md): past
~75 uniques/query the API serves fully-billed HTTP-200 duplicate pages with
no exhaustion signal. Pagination therefore EARLY-STOPS after the first page
that yields 0 new unique place_ids for that query - that dead page is still
billed and is recorded as measured overhead, never hidden.

Cost is measured live via GET /account before/after each run (5 credits per
successful request, failures not billed - verified in smoke). The API key is
scrubbed from saved responses (their payload embeds it in reviews/photos
links).

Usage: python scripts/scrapingdog_scale_run.py  (does run1 then run2)
Raw: data/scrapingdog/raw/run1/ and run2/ (every page + per-run log).
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
from lib.config import RUNS  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
MAX_PAGES = 10          # start 0..180 -> 200 requested/query, benchmark ceiling
API = "https://api.scrapingdog.com/google_maps"

load_env()
KEY = require_env("SCRAPINGDOG_API_KEY")


def account():
    with urllib.request.urlopen(
            f"https://api.scrapingdog.com/account?api_key={KEY}", timeout=30) as r:
        return json.load(r)


def fetch(query, start):
    url = API + "?" + urllib.parse.urlencode(
        {"api_key": KEY, "query": query, "start": start})
    t0 = time.perf_counter()
    try:
        with urllib.request.urlopen(url, timeout=90) as r:
            body = r.read().decode("utf-8", errors="replace")
            status = r.status
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")[:1000]
        status = e.code
    return status, body, round(time.perf_counter() - t0, 2)


def do_run(run_label, run):
    out = ROOT / "data" / "scrapingdog" / "raw" / run_label
    out.mkdir(parents=True, exist_ok=True)
    acct0 = account()
    log = {"run": run_label, "industry": run["industry"], "max_pages": MAX_PAGES,
           "credits_used_before": acct0["requestUsed"], "pack": acct0["pack"],
           "started": datetime.now(timezone.utc).isoformat(), "requests": []}
    run_uniques = {}
    t_run = time.perf_counter()
    for t in run["targets"]:
        query = t["query"]
        slug = query.lower().replace(",", "").replace(" ", "_")[:60]
        q_seen = {}
        dead_page_billed = 0
        for page in range(MAX_PAGES):
            start = page * 20
            status, body, lat = fetch(query, start)
            n_results, new = 0, 0
            if status == 200:
                try:
                    d = json.loads(body)
                except json.JSONDecodeError:
                    d = {}
                results = d.get("search_results", [])
                n_results = len(results)
                for rec in results:
                    pid = rec.get("place_id") or rec.get("data_id")
                    if pid not in q_seen:
                        q_seen[pid] = rec
                        new += 1
                (out / f"{slug}-start{start}.json").write_text(
                    body.replace(KEY, "SCRAPINGDOG_API_KEY"), encoding="utf-8")
            log["requests"].append({"query": query, "start": start, "http": status,
                                    "latency_s": lat, "results": n_results, "new_unique": new})
            print(f"  {slug} start={start}: HTTP {status}, {n_results} results, "
                  f"{new} new, {lat}s", flush=True)
            if status != 200 or n_results == 0:
                break
            if new == 0:
                dead_page_billed += 1
                break  # depth ceiling reached - this page was billed, recorded
        run_uniques.update(q_seen)
        log.setdefault("per_query", {})[query] = {
            "unique": len(q_seen), "pages_fetched": len([r for r in log["requests"] if r["query"] == query]),
            "dead_pages_billed": dead_page_billed}
    log["wall_clock_s"] = round(time.perf_counter() - t_run, 1)
    acct1 = account()
    log["credits_used_after"] = acct1["requestUsed"]
    log["credits_this_run"] = acct1["requestUsed"] - acct0["requestUsed"]
    log["unique_places_run"] = len(run_uniques)
    log["finished"] = datetime.now(timezone.utc).isoformat()
    (out / f"{run_label}-log.json").write_text(json.dumps(log, indent=2), encoding="utf-8")
    print(f"{run_label} DONE: {len(run_uniques)} unique, "
          f"{log['credits_this_run']} credits, {log['wall_clock_s']}s wall")
    return log


if __name__ == "__main__":
    a = account()
    assert a["pack"] == "lite", f"expected lite plan, got {a['pack']} - aborting before spend"
    print(f"account OK: pack={a['pack']}, used {a['requestUsed']}/{a['requestLimit']}")
    summary = {}
    for label, run in (("run1", RUNS[0]), ("run2", RUNS[1])):
        lg = do_run(label, run)
        summary[label] = {k: lg[k] for k in ("unique_places_run", "credits_this_run", "wall_clock_s")}
    print(json.dumps(summary, indent=1))
