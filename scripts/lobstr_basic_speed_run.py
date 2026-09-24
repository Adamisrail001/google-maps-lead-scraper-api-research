"""Lobstr enrichment-OFF speed run — fair basic-workload wall-clock.

Purpose: the benchmark's Lobstr Run-1 wall-clock (1,711s) includes per-row
website visits for email/social/image enrichment; Bright Data's 365s is bare
listings. This run repeats the EXACT Run-1 workload (same 10 agency sub-area
task URLs at 14z, max_results 200, concurrency 20) with all three enrichment
functions OFF, so the Speed criterion can compare the same basic work.

Guard: aborts before launching if the squid's accepted concurrency != 20
(the benchmark value) — a 1-slot run would not be comparable.

Raw evidence -> data/lobstr/raw/speed-basic/ (squid, tasks, run polls, final).
"""
import json
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.env import load_env, require_env  # noqa: E402
from lib.config import RUN_1  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "lobstr" / "raw" / "speed-basic"
OUT.mkdir(parents=True, exist_ok=True)
CRAWLER = "4734d096159ef05210e0e1677e8be823"  # Google Maps Leads Scraper

load_env()
KEY = require_env("LOBSTR_API_KEY")
H = {"Authorization": f"Token {KEY}", "Content-Type": "application/json"}
API = "https://api.lobstr.io/v1"


def call(method, path, body=None):
    req = urllib.request.Request(API + path, headers=H, method=method,
                                 data=json.dumps(body).encode() if body is not None else None)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, json.load(r)
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode(errors="replace")[:800]}


log = {"started": datetime.now(timezone.utc).isoformat()}

# 1. create squid (or reuse one passed as argv[1] after a partial earlier attempt)
if len(sys.argv) > 1:
    sid = sys.argv[1]
    print("reusing squid:", sid)
else:
    st, squid = call("POST", "/squids", {"crawler": CRAWLER, "name": "Speed Test - Basic (no enrichment)"})
    print("create squid:", st, squid.get("id") or squid)
    assert st in (200, 201), squid
    sid = squid["id"]
log["squid_id"] = sid

# 2. configure: benchmark params minus enrichment, concurrency 20
st, upd = call("POST", f"/squids/{sid}", {
    "concurrency": 20,
    "params": {
        "country": "United States",
        "ratings": "Any rating",
        "language": "English (United States)",
        "functions": {
            "fetch_business_images": False,
            "collect_business_details": False,
            "extract_emails_from_website": False,
        },
        "geo_match": True,
        "max_results": 200,
        "skip_closed": False,
        "category_match": True,
        "website_filter": "all",
        "skip_without_email": False,
        "max_unique_results_per_run": None,
    }})
print("configure squid:", st)
(OUT / "squid.json").write_text(json.dumps(upd, indent=2), encoding="utf-8")
assert st in (200, 201), upd
st, cur = call("GET", f"/squids/{sid}")   # update echo omits concurrency - read back
assert st == 200, cur
acc_conc = cur.get("concurrency")
funcs = (cur.get("params") or {}).get("functions")
print("accepted concurrency:", acc_conc, "| functions:", funcs)
if acc_conc != 20:
    print(f"ABORT: server accepted concurrency {acc_conc}, benchmark used 20 — "
          "run would not be comparable. No run launched, nothing billed.")
    sys.exit(1)

# 3. add the exact Run-1 task URLs
tasks = [{"url": t["lobstr_task_url"]} for t in RUN_1["targets"]]
st, tr = call("POST", "/tasks", {"squid": sid, "tasks": tasks})
print("add tasks:", st, "count:", len(tr.get("tasks", [])) if st in (200, 201) else tr)
(OUT / "tasks.json").write_text(json.dumps(tr, indent=2), encoding="utf-8")
assert st in (200, 201) and len(tr.get("tasks", [])) == 10, tr

# 4. launch
st, run = call("POST", "/runs", {"squid": sid})
print("launch run:", st, run.get("id") or run)
(OUT / "run-launch.json").write_text(json.dumps(run, indent=2), encoding="utf-8")
assert st in (200, 201), run
rid = run["id"]
log["run_id"] = rid

# 5. poll
t0 = time.time()
final = None
while time.time() - t0 < 3600:
    time.sleep(20)
    st, r = call("GET", f"/runs/{rid}")
    if st != 200:
        print("poll err:", st, str(r)[:120])
        continue
    print(f"{time.time()-t0:.0f}s: status={r.get('status')} results={r.get('total_results')} "
          f"unique={r.get('total_unique_results')} credits={r.get('credit_used')}")
    if r.get("is_done") or r.get("status") in ("done", "failed", "error"):
        final = r
        break
assert final, "run did not finish within 60 min"
(OUT / "run-final.json").write_text(json.dumps(final, indent=2), encoding="utf-8")

fmt = "%Y-%m-%dT%H:%M:%S.%f"
wall = (datetime.strptime(final["ended_at"][:26], fmt)
        - datetime.strptime(final["started_at"][:26], fmt)).total_seconds()
log.update(wall_clock_s=round(wall, 1), status=final.get("status"),
           total_results=final.get("total_results"),
           total_unique=final.get("total_unique_results"),
           credit_used=final.get("credit_used"),
           done_reason=final.get("done_reason"),
           finished=datetime.now(timezone.utc).isoformat())
(OUT / "speed-basic-log.json").write_text(json.dumps(log, indent=2), encoding="utf-8")
print(json.dumps(log, indent=1))
