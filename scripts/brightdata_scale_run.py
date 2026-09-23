"""Bright Data Web Scraper API - SCALE run (Google Maps full information).

Per completion brief: stage 2 = 1,000 results x 2 runs. One trigger per run
with all 10 sub-area inputs, limit_per_input=100 (10 x 100 = 1,000 ceiling).
Discovery mode: discover_by=location, inputs {country, keyword} - keyword
embeds the sub-area text (validated in smoke: returned correct-area results).

Usage: python scripts/brightdata_scale_run.py run1|run2
Outputs: data/brightdata/raw/<run>/ (snapshot JSON + progress log).
brightdata.com zone is blocked by local DNS -> DoH-resolved pinned IP.
"""
import json
import socket
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

DATASET = "gd_m8ebnr0q2qlklc02fz"
LIMIT_PER_INPUT = 100
API = "https://api.brightdata.com"

load_env()
KEY = require_env("BRIGHTDATA_API_KEY_2")
H = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}


def main():
    run_label = sys.argv[1]
    run = RUNS[0] if run_label == "run1" else RUNS[1]
    out = Path(__file__).resolve().parent.parent / "data" / "brightdata" / "raw" / run_label
    out.mkdir(parents=True, exist_ok=True)

    inputs = [{"country": "US", "keyword": f"{run['industry']} in {t['subarea']}, {t['city']}"}
              for t in run["targets"]]
    params = urllib.parse.urlencode({
        "dataset_id": DATASET, "include_errors": "true",
        "type": "discover_new", "discover_by": "location",
        "limit_per_input": str(LIMIT_PER_INPUT)})
    log = {"run": run_label, "inputs": inputs, "limit_per_input": LIMIT_PER_INPUT,
           "started": datetime.now(timezone.utc).isoformat()}
    req = urllib.request.Request(f"{API}/datasets/v3/trigger?{params}",
                                 data=json.dumps(inputs).encode(), headers=H)
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=120) as r:
        trig = json.loads(r.read())
    sid = trig["snapshot_id"]
    log["snapshot_id"] = sid
    print(f"{run_label} triggered: {sid}")

    while time.time() - t0 < 5400:
        time.sleep(30)
        try:
            req = urllib.request.Request(f"{API}/datasets/v3/progress/{sid}", headers=H)
            with urllib.request.urlopen(req, timeout=60) as r:
                p = json.loads(r.read())
        except Exception as e:
            print("poll err:", str(e)[:100])
            continue
        print(f"{time.time()-t0:.0f}s: {p.get('status')} records={p.get('records')}")
        if p.get("status") in ("ready", "failed"):
            log["progress_final"] = p
            break
    log["wall_clock_s"] = round(time.time() - t0, 1)

    if log.get("progress_final", {}).get("status") == "ready":
        req = urllib.request.Request(f"{API}/datasets/v3/snapshot/{sid}?format=json", headers=H)
        with urllib.request.urlopen(req, timeout=600) as r:
            rows = json.loads(r.read())
        (out / "snapshot.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2),
                                           encoding="utf-8")
        log["rows_downloaded"] = len(rows)
        print(f"{run_label} DONE: {len(rows)} rows, wall {log['wall_clock_s']}s")
    log["finished"] = datetime.now(timezone.utc).isoformat()
    (out / f"{run_label}-log.json").write_text(json.dumps(log, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
