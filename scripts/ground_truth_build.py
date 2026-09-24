"""Build the hand-verifiable ground-truth sample (testing-plan §10).

Sample selection: businesses returned by ALL FOUR ranked providers (join key =
Google CID, derived per provider), stratified 6 per sub-group (industry x
city), deterministic (sorted by CID). The providers only pick WHICH businesses
are checked - the truth VALUES come exclusively from Google Maps itself,
captured live via Places API (New) Details with a full field mask, timestamped.

Outputs:
  ground-truth/sample-24.json      - ground truth values + capture metadata
  ground-truth/manual-checklist.md - shortlist for human browser verification
  ground-truth/provider-records.json - each provider's benchmark record for
                                       the sampled CIDs (for the comparison step)
"""
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.env import load_env, require_env  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "ground-truth"
OUT.mkdir(exist_ok=True)
PER_SUBGROUP = 6

load_env()
GKEY = require_env("GOOGLE_PLACES_API_KEY")

def cid_lob(r):
    return str(r.get("cid") or "")

def cid_apify(r):
    u = r.get("google_maps_url") or ""
    if "cid=" in u:
        return u.split("cid=")[1].split("&")[0]
    pid = r.get("place_id") or ""
    if ":0x" in pid:
        try:
            return str(int(pid.split(":")[1], 16))
        except ValueError:
            return ""
    return ""

def cid_has(r):
    d = r.get("dataId") or ""
    if ":0x" in d:
        try:
            return str(int(d.split(":")[1], 16))
        except ValueError:
            return ""
    return ""

def cid_bd(r):
    return str(r.get("cid") or "")

P = {}
for run in ("run1", "run2"):
    P.setdefault("Lobstr", {})[run] = {}
    for r in json.loads((ROOT / "data/lobstr/exports" / f"{run}-unique.json").read_text(encoding="utf-8")):
        c = cid_lob(r)
        if c:
            P["Lobstr"][run][c] = r
    P.setdefault("Apify", {})[run] = {}
    for r in json.loads((ROOT / "data/apify/exports" / f"{run}-unique.json").read_text(encoding="utf-8")):
        c = cid_apify(r)
        if c:
            P["Apify"][run][c] = r
for f in sorted((ROOT / "data/hasdata/raw").glob("run*/job-*-results-p*.json")):
    run = f.parent.name
    P.setdefault("HasData", {}).setdefault(run, {})
    for row in json.loads(f.read_text(encoding="utf-8"))["data"]:
        c = cid_has(row["data"])
        if c:
            P["HasData"][run][c] = row["data"]
for run in ("run1", "run2"):
    P.setdefault("BrightData", {})[run] = {}
    for r in json.loads((ROOT / f"data/brightdata/raw/{run}/snapshot.json").read_text(encoding="utf-8")):
        c = cid_bd(r)
        if c:
            P["BrightData"][run][c] = r

INDUSTRY = {"run1": "marketing agencies", "run2": "restaurants"}

def city_of(lob):
    sc = (lob.get("state_code") or "").upper()
    if sc == "NY":
        return "New York"
    if sc == "CA":
        return "Los Angeles"
    addr = lob.get("address") or ""
    return "New York" if " NY " in addr or addr.endswith("NY") else "Los Angeles"

sample = []
for run in ("run1", "run2"):
    inter = sorted(set.intersection(*[set(P[p][run]) for p in P]), key=int)
    buckets = {"New York": [], "Los Angeles": []}
    for c in inter:
        buckets[city_of(P["Lobstr"][run][c])].append(c)
    for city, cids in buckets.items():
        for c in cids[:PER_SUBGROUP]:
            sample.append({"cid": c, "run": run, "industry": INDUSTRY[run], "city": city,
                           "place_id": P["Lobstr"][run][c].get("place_id"),
                           "name_hint": P["Lobstr"][run][c].get("name")})

print(f"sample: {len(sample)} businesses "
      f"({sum(1 for s in sample if s['run']=='run1')} agencies / "
      f"{sum(1 for s in sample if s['run']=='run2')} restaurants)")

# ---- live Google Places Details capture (the truth source) ----
MASK = ("displayName,formattedAddress,nationalPhoneNumber,internationalPhoneNumber,"
        "websiteUri,primaryTypeDisplayName,types,rating,userRatingCount,"
        "regularOpeningHours.weekdayDescriptions,businessStatus,googleMapsUri,id")
gt = []
for s in sample:
    req = urllib.request.Request(
        f"https://places.googleapis.com/v1/places/{s['place_id']}",
        headers={"X-Goog-Api-Key": GKEY, "X-Goog-FieldMask": MASK})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.load(r)
        err = None
    except urllib.error.HTTPError as e:
        d, err = {}, f"HTTP {e.code}: {e.read().decode(errors='replace')[:200]}"
    gt.append({**s,
               "captured_at": datetime.now(timezone.utc).isoformat(),
               "source": "Google Places API (New) Place Details, live",
               "error": err,
               "truth": {
                   "name": (d.get("displayName") or {}).get("text"),
                   "address": d.get("formattedAddress"),
                   "phone": d.get("nationalPhoneNumber") or d.get("internationalPhoneNumber"),
                   "website": d.get("websiteUri"),
                   "category": (d.get("primaryTypeDisplayName") or {}).get("text"),
                   "types": d.get("types"),
                   "rating": d.get("rating"),
                   "review_count": d.get("userRatingCount"),
                   "hours": (d.get("regularOpeningHours") or {}).get("weekdayDescriptions"),
                   "business_status": d.get("businessStatus"),
                   "google_maps_uri": d.get("googleMapsUri"),
               }})
    print(" ", s["name_hint"], "->", err or "OK")

(OUT / "sample-24.json").write_text(json.dumps(gt, indent=2, ensure_ascii=False), encoding="utf-8")

# provider records for the sampled CIDs (comparison inputs, frozen)
prov_records = {p: {s["cid"]: P[p][s["run"]][s["cid"]] for s in sample} for p in P}
(OUT / "provider-records.json").write_text(
    json.dumps(prov_records, indent=2, ensure_ascii=False), encoding="utf-8")

# manual checklist
L = ["# Manual browser verification checklist (ground truth spot-check)",
     "",
     f"Captured via Places API {datetime.now(timezone.utc).date()}. For each row, open the URL in a browser and confirm name, address, phone, website, category, rating, review count, hours match what Google Maps shows. Tick the box; note any mismatch inline.",
     "",
     "| # | Business | Sub-group | Google Maps URL | Verified? |",
     "|---:|---|---|---|---|"]
for i, g in enumerate(gt, 1):
    L.append(f"| {i} | {g['truth']['name'] or g['name_hint']} | {g['industry']} × {g['city']} | {g['truth']['google_maps_uri'] or 'https://www.google.com/maps?cid=' + g['cid']} | ☐ |")
(OUT / "manual-checklist.md").write_text("\n".join(L), encoding="utf-8")
print("written: ground-truth/sample-24.json, provider-records.json, manual-checklist.md")
