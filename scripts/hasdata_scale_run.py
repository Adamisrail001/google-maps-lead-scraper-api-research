"""HasData Google Maps scraper - SCALE benchmark run (Startup plan).

Mirrors the provider benchmark: one job per sub-area (10/run), 200 limit,
extractEmails on, both industries. Usage:
    python scripts/hasdata_scale_run.py run1   # marketing agencies
    python scripts/hasdata_scale_run.py run2   # restaurants

Smoke-test lessons applied (data/hasdata/reports/smoke-findings.md):
- job status sticks at 'exporting_data' while data is complete -> completion
  is detected via the RESULTS endpoint (meta.total == dataRowsCount, stable),
  never via status == 'finished'.
- schema varies with extractEmails; keep raw pages verbatim.
- billing measured from each job's creditsSpent field (no account endpoint).

Outputs: data/hasdata/raw/<run>/job-<slug>-{submit,final}.json + results
pages, plus <run>-log.json with timings.
"""
import json
import socket
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.env import load_env, require_env  # noqa: E402
from lib.config import RUNS  # noqa: E402

# DNS resilience: local resolver intermittently fails; fall back to DoH pin.
_orig = socket.getaddrinfo
_PIN = {}
def _doh(host):
    with urllib.request.urlopen(
            f"https://dns.google/resolve?name={host}&type=A", timeout=30) as r:
        for a in json.load(r).get("Answer", []):
            if a.get("type") == 1:
                return a["data"]
def _patched(host, *a, **kw):
    if host in _PIN:
        return _orig(_PIN[host], *a, **kw)
    try:
        return _orig(host, *a, **kw)
    except socket.gaierror:
        _PIN[host] = _doh(host)
        return _orig(_PIN[host], *a, **kw)
socket.getaddrinfo = _patched

ROOT = Path(__file__).resolve().parent.parent
API = "https://api.hasdata.com"
LIMIT = 200
POLL_S = 20
STABLE_POLLS = 2   # results total must be stable this many polls to call it done
TIMEOUT_S = 3600

load_env()
KEY = require_env("HASDATA_API_KEY_SCALE")
H = {"x-api-key": KEY, "Content-Type": "application/json"}


def req_json(method, path, body=None, tries=4):
    for i in range(tries):
        try:
            r = urllib.request.Request(API + path, headers=H,
                                       data=json.dumps(body).encode() if body else None,
                                       method=method)
            with urllib.request.urlopen(r, timeout=60) as resp:
                return resp.status, json.loads(resp.read())
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read() or b"{}")
        except Exception as e:
            if i == tries - 1:
                raise
            time.sleep(5 * (i + 1))


def slug(t):
    import re
    return re.sub(r"[^a-z0-9]+", "_", t.lower()).strip("_")


def main():
    run_label = sys.argv[1]
    run = RUNS[0] if run_label == "run1" else RUNS[1]
    out = ROOT / "data" / "hasdata" / "raw" / run_label
    out.mkdir(parents=True, exist_ok=True)
    log = {"run": run_label, "industry": run["industry"], "limit": LIMIT,
           "extractEmails": True, "started": datetime.now(timezone.utc).isoformat(),
           "jobs": {}}

    # submit all 10 sub-area jobs; plan allows 5 concurrent -> retry 429s as
    # slots free up. Reuse jobs already submitted by a previous attempt.
    for t in run["targets"]:
        s = slug(f"{t['subarea']}_{t['city']}")
        prior = out / f"job-{s}-submit.json"
        if prior.exists():
            pd = json.loads(prior.read_text(encoding="utf-8"))
            if pd.get("id"):
                log["jobs"][s] = {"id": pd["id"], "submitted": pd.get("createdAt"),
                                  "submit_http": 200, "reused": True}
                print(f"reusing {s} -> job {pd['id']}")
                continue
        body = {"keywords": [run["industry"]],
                "locations": [f"{t['subarea']}, {t['city']}"],
                "limit": LIMIT, "extractEmails": True}
        deadline = time.time() + 1800
        while True:
            st, d = req_json("POST", "/scrapers/google-maps/jobs", body)
            if st == 429 and time.time() < deadline:
                time.sleep(30)
                continue
            break
        (out / f"job-{s}-submit.json").write_text(json.dumps(d, indent=2), encoding="utf-8")
        if st != 200:
            print(f"SUBMIT FAILED {s}: HTTP {st} {json.dumps(d)[:200]}")
            log["jobs"][s] = {"submit_http": st, "error": d}
            continue
        log["jobs"][s] = {"id": d["id"], "submitted": datetime.now(timezone.utc).isoformat(),
                          "submit_http": st}
        print(f"submitted {s} -> job {d['id']}")

    # poll: completion = results total == dataRowsCount, stable for N polls
    t0 = time.time()
    pending = {s: j for s, j in log["jobs"].items() if "id" in j}
    stable = {s: (None, 0) for s in pending}
    while pending and time.time() - t0 < TIMEOUT_S:
        time.sleep(POLL_S)
        for s in list(pending):
            j = pending[s]
            st, d = req_json("GET", f"/scrapers/jobs/{j['id']}")
            if st != 200:
                continue
            rows, status = int(d.get("dataRowsCount") or 0), d.get("status")
            st2, res = req_json("GET", f"/scrapers/jobs/{j['id']}/results?page=1&limit=1")
            total = int(res.get("meta", {}).get("total") or 0) if st2 == 200 else 0
            prev, count = stable[s]
            stable[s] = (total, count + 1 if total == prev else 0)
            fin = status not in ("pending", "in_progress", "running")
            if fin and rows > 0 and total >= rows and stable[s][1] >= STABLE_POLLS:
                j.update({"finished": datetime.now(timezone.utc).isoformat(),
                          "status": status, "rows": rows,
                          "credits": int(d.get("creditsSpent") or 0),
                          "stopReason": d.get("stopReason"),
                          "elapsed_s": round(time.time() - t0, 1)})
                (out / f"job-{s}-final.json").write_text(json.dumps(d, indent=2), encoding="utf-8")
                print(f"done {s}: {rows} rows, {d.get('creditsSpent')} credits, "
                      f"stop={d.get('stopReason')} ({j['elapsed_s']}s)")
                del pending[s]
    for s in pending:
        print(f"TIMEOUT/incomplete: {s}")
        log["jobs"][s]["timeout"] = True

    # fetch all result pages
    for s, j in log["jobs"].items():
        if "id" not in j or j.get("timeout"):
            continue
        page, got = 1, 0
        while True:
            st, res = req_json("GET", f"/scrapers/jobs/{j['id']}/results?page={page}&limit=100")
            if st != 200:
                break
            (out / f"job-{s}-results-p{page}.json").write_text(
                json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
            got += len(res.get("data", []))
            if page >= res.get("meta", {}).get("lastPage", 1):
                break
            page += 1
        j["rows_fetched"] = got
    log["finished"] = datetime.now(timezone.utc).isoformat()
    log["wall_clock_s"] = round(time.time() - t0, 1)
    (out / f"{run_label}-log.json").write_text(json.dumps(log, indent=2), encoding="utf-8")
    total_rows = sum(j.get("rows_fetched", 0) for j in log["jobs"].values())
    total_credits = sum(int(j.get("credits") or 0) for j in log["jobs"].values())
    print(f"== {run_label} DONE: {total_rows} rows fetched, {total_credits} credits, "
          f"wall {log['wall_clock_s']}s")


if __name__ == "__main__":
    main()
