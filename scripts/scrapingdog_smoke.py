"""Scrapingdog Google Maps API - free-plan smoke test (2026-09-23).

Goal: decide whether Scrapingdog deserves a paid scale test. 4 queries from
the benchmark target set (data-rich vs data-scarce area x high- vs low-email
vertical), paginated until an empty page or MAX_PAGES. Free plan = 200
credits, 5 credits/request -> hard budget of 36 requests total including the
already-spent probe (saved as raw/smoke/probe-*.json, counted as page 0 of
Manhattan agencies).

Answers: per-query depth ceiling (past Google's ~60?), latency, field fills,
delivery consistency. Raw pages -> data/scrapingdog/raw/smoke/.
"""
import json
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.env import load_env, require_env  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "scrapingdog" / "raw" / "smoke"
MAX_PAGES = 8          # pages 0..7 per query
MAX_REQUESTS = 35      # incl. the 1 probe already spent -> <=180 credits total

QUERIES = [
    ("manhattan-agencies", "marketing agencies in Manhattan, New York", 1),   # probe covered page 0
    ("vannuys-agencies", "marketing agencies in San Fernando Valley (Van Nuys), Los Angeles", 0),
    ("manhattan-restaurants", "restaurants in Manhattan, New York", 0),
    ("vannuys-restaurants", "restaurants in San Fernando Valley (Van Nuys), Los Angeles", 0),
]

load_env()
KEY = require_env("SCRAPINGDOG_API_KEY")
OUT.mkdir(parents=True, exist_ok=True)

log = {"started": datetime.now(timezone.utc).isoformat(), "requests": []}
made = 1  # probe already spent
for slug, query, start_page in QUERIES:
    for page in range(start_page, MAX_PAGES):
        if made >= MAX_REQUESTS:
            print("request budget reached, stopping")
            break
        url = "https://api.scrapingdog.com/google_maps?" + urllib.parse.urlencode(
            {"api_key": KEY, "query": query, "page": page})
        t0 = time.perf_counter()
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                d = json.load(r)
                status = r.status
        except urllib.error.HTTPError as e:
            d = {"error": e.read().decode(errors="replace")[:500]}
            status = e.code
        el = time.perf_counter() - t0
        made += 1
        n = len(d.get("search_results", []))
        (OUT / f"{slug}-page{page}.json").write_text(
            json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
        log["requests"].append({"query": query, "page": page, "http": status,
                                "latency_s": round(el, 2), "results": n})
        print(f"  {slug} p{page}: HTTP {status}, {n} results, {el:.2f}s")
        if status != 200 or n == 0:
            break
    else:
        continue
    if made >= MAX_REQUESTS:
        break

log["total_requests_incl_probe"] = made
log["finished"] = datetime.now(timezone.utc).isoformat()
(OUT / "smoke-log.json").write_text(json.dumps(log, indent=2), encoding="utf-8")

# per-query totals + dedupe + field fill across all fetched pages
from collections import defaultdict  # noqa: E402
per_q = defaultdict(dict)
for f in OUT.glob("*page*.json"):
    name = f.name.replace("probe-manhattan-agencies-page0", "manhattan-agencies-page0")
    slug = name.rsplit("-page", 1)[0]
    d = json.loads(f.read_text(encoding="utf-8"))
    for rec in d.get("search_results", []):
        per_q[slug][rec.get("place_id") or rec.get("data_id")] = rec
allrec = {}
for slug, recs in sorted(per_q.items()):
    print(f"{slug}: {len(recs)} unique")
    allrec.update(recs)
vals = list(allrec.values())
fill = {f: round(100 * sum(1 for r in vals if r.get(f) not in (None, "", [], {})) / len(vals))
        for f in ["title", "address", "phone", "website", "rating", "reviews", "operating_hours", "gps_coordinates", "place_id"]}
print("TOTAL unique:", len(allrec), "| fill:", fill)
lat = [r["latency_s"] for r in log["requests"] if r["http"] == 200]
print("latency median:", sorted(lat)[len(lat)//2], "max:", max(lat), "| requests incl probe:", made, "=> credits ~", made * 5)
