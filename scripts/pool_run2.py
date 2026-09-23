"""Pool + dedupe Run 2 (restaurants) raw scraper outputs into unique-lead
exports — the exact same logic as Run 1 (outputs/pool_run1.py, preserved) so
the two runs are comparable: lib.dedupe.build_lead_key (place_id -> URL ->
name+address hash).

Also prints raw/unique counts and lead-field fill-rates per provider.
Outputs: data/<provider>/exports/run2-unique.json +
         data/<provider>/analysis/run2-duplicate-report.json
"""
import json, glob, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.dedupe import dedupe, build_lead_key  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def save(path, obj):
    with open(ROOT / path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def fill(recs, names):
    return {n: f"{100*sum(1 for r in recs if r.get(n) not in (None,'',[],{}))/len(recs):.0f}%" for n in names}


# --- Lobstr ---
lobstr_doc = json.load(open(ROOT / "data/lobstr/raw/results/run2-page1.json", encoding="utf-8"))
lobstr_raw = lobstr_doc["data"]
meta = {k: v for k, v in lobstr_doc.items() if k != "data" and not isinstance(v, (list, dict))}
print("LOBSTR run2 page meta:", meta)
lobstr_result = dedupe([{"domain": "lobstr-run2", "review": r} for r in lobstr_raw], key_fn=build_lead_key)
lu = [e["review"] for e in lobstr_result["unique"]]
print(f"LOBSTR: raw={len(lobstr_raw)} unique={len(lu)} duplicates={len(lobstr_result['duplicates'])}")
print("  fill:", fill(lu, ["phone", "website", "email", "facebook", "instagram", "linkedin", "opening_hours", "ratings", "images"]))

# --- Apify ---
apify_raw = []
for f in glob.glob(str(ROOT / "data/apify/raw/datasets/run2-*.json")):
    items = json.load(open(f, encoding="utf-8"))
    apify_raw.extend([i for i in items if i.get("name")])
apify_result = dedupe([{"domain": "apify-run2", "review": r} for r in apify_raw], key_fn=build_lead_key)
au = [e["review"] for e in apify_result["unique"]]
print(f"APIFY: raw={len(apify_raw)} unique={len(au)} duplicates={len(apify_result['duplicates'])}")
print("  fill:", fill(au, ["phone", "website", "email", "hours", "rating"]))
print("  charged=true:", sum(1 for r in au if r.get("charged")))

# --- Outscraper ---
outscraper_raw = []
for f in glob.glob(str(ROOT / "data/outscraper/raw/scrape/run2-*.json")):
    d = json.load(open(f, encoding="utf-8"))
    outscraper_raw.extend(d.get("data", []))
outscraper_result = dedupe([{"domain": "outscraper-run2", "review": r} for r in outscraper_raw], key_fn=build_lead_key)
ou = [e["review"] for e in outscraper_result["unique"]]
print(f"OUTSCRAPER: raw={len(outscraper_raw)} unique={len(ou)} duplicates={len(outscraper_result['duplicates'])}")
print("  fill:", fill(ou, ["phone", "website", "category", "rating", "reviews", "working_hours", "photo"]))

save("data/lobstr/exports/run2-unique.json", lu)
save("data/lobstr/analysis/run2-duplicate-report.json", lobstr_result["duplicates"])
save("data/apify/exports/run2-unique.json", au)
save("data/apify/analysis/run2-duplicate-report.json", apify_result["duplicates"])
save("data/outscraper/exports/run2-unique.json", ou)
save("data/outscraper/analysis/run2-duplicate-report.json", outscraper_result["duplicates"])
print("\nSaved run2 exports + duplicate reports for all 3 providers.")
