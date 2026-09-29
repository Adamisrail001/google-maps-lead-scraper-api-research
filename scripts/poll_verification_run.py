"""Poll the auto_verify_emails benchmark run until scrape + mail phase complete.

Writes progress snapshots and the final run object to data/lobstr/raw/verification-run/.
Usage: python scripts/poll_verification_run.py <run_id>
"""
import json
import os
import sys
import time
import urllib.request

RUN_ID = sys.argv[1]
OUT_DIR = os.path.join("data", "lobstr", "raw", "verification-run")
os.makedirs(OUT_DIR, exist_ok=True)


def env_key():
    with open(".env", encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("LOBSTR_API_KEY"):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("LOBSTR_API_KEY not found in .env")


KEY = env_key()


def get_run():
    req = urllib.request.Request(
        f"https://api.lobstr.io/v1/runs/{RUN_ID}",
        headers={"Authorization": f"Token {KEY}"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


start = time.time()
last = None
while time.time() - start < 90 * 60:
    try:
        run = get_run()
    except Exception as e:  # transient network errors: keep polling
        print(f"[{time.strftime('%H:%M:%S')}] poll error: {e}", flush=True)
        time.sleep(60)
        continue
    last = run
    status = run.get("status")
    mail_done = run.get("mail_done")
    print(
        f"[{time.strftime('%H:%M:%S')}] status={status} results={run.get('total_results')} "
        f"unique={run.get('total_unique_results')} credits={run.get('credit_used')} "
        f"mail_done={mail_done} duration={run.get('duration')}",
        flush=True,
    )
    ev = run.get("email_verification") or {}
    if status in ("error", "aborted"):
        break
    if status == "done" and (mail_done is True or ev.get("is_done") is True):
        break
    if status == "done" and not ev and mail_done is None:
        break  # no verification phase attached at all
    time.sleep(60)

with open(os.path.join(OUT_DIR, "run-final.json"), "w", encoding="utf-8") as f:
    json.dump(last, f, indent=1)
print("FINAL:", json.dumps(last, indent=1)[:2000], flush=True)
