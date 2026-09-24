"""Compare each ranked provider's benchmark records against the live Google
Maps ground truth (ground-truth/sample-24.json, captured via Places API).

Accuracy (testing-plan §9.3 / criteria.md Data Quality 'accuracy' 0.5):
per field, a provider is only graded where BOTH it and the truth have a value.
accuracy% = matched comparable fields / total comparable fields, all records.

Freshness (criteria.md Data Quality 'freshness' 0.3): volatile-field currency —
a record is 'fresh' if rating within ±0.1 AND review count within max(5%, 5)
of the live value (runs were 1-2 days before capture; a live scraper drifts
by at most a few reviews). Providers without a review-count field (Apify) are
graded on rating only, flagged.

Outputs: data/<provider>/analysis/ground-truth-match.json + printed summary.
Does NOT touch any scoring file - review step happens first.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
gt = json.loads((ROOT / "ground-truth/sample-24.json").read_text(encoding="utf-8"))
pr = json.loads((ROOT / "ground-truth/provider-records.json").read_text(encoding="utf-8"))

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def norm_phone(v):
    d = re.sub(r"\D", "", str(v or ""))
    return d[-10:] if len(d) >= 10 else d


def norm_domain(v):
    v = str(v or "").lower()
    v = re.sub(r"^https?://", "", v).replace("www.", "")
    return v.split("/")[0].split("?")[0]


def norm_name(v):
    return re.sub(r"[^a-z0-9]", "", str(v or "").lower())


def addr_key(v):
    """street number + 5-digit zip - robust to abbreviation differences."""
    v = str(v or "")
    num = re.match(r"\s*(\d+)", v)
    zips = re.findall(r"\b(\d{5})\b", v)
    return (num.group(1) if num else "", zips[-1] if zips else "")


def norm_time(v):
    v = str(v or "").lower()
    v = re.sub(r"[\s  –—]+", "", v).replace("--", "-")
    v = re.sub(r"[,/\n]+", "", v)
    v = v.replace(":00", "").replace("–", "-").replace("—", "-")
    v = v.replace("open24hours", "24h").replace("24hours", "24h")
    return v


def hours_map(provider, rec):
    if provider == "Lobstr":
        s = rec.get("opening_hours") or ""
        out = {}
        for day in DAYS:
            m = re.search(day + r": ([^,]+(?:, (?!(?:" + "|".join(DAYS) + r"):)[^,]+)*)", s)
            if m:
                out[day] = m.group(1)
        return out
    if provider == "HasData":
        wh = rec.get("workingHours") or {}
        return {d.get("day"): d.get("time") for d in wh.get("days", []) if d.get("day")}
    if provider == "Apify":
        return rec.get("hours") or {}
    if provider == "BrightData":
        return rec.get("open_hours") or {}
    return {}


def truth_hours_map(t):
    out = {}
    for line in t.get("hours") or []:
        day, _, rest = line.partition(":")
        out[day.strip()] = rest.strip()
    return out


FIELD_GETTERS = {
    "Lobstr": dict(name="name", address="address", phone="phone", website="website",
                   category="category", rating="score", review_count="ratings"),
    "HasData": dict(name="title", address="address", phone="phone", website="website",
                    category="type", rating="rating", review_count="reviews"),
    "Apify": dict(name="name", address="address", phone="phone", website="website",
                  category="category", rating="rating", review_count=None),
    "BrightData": dict(name="name", address="address", phone="phone_number",
                       website="open_website", category="category", rating="rating",
                       review_count="reviews_count"),
}


def fnum(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


summary = {}
for prov, getters in FIELD_GETTERS.items():
    per_field = {f: {"comparable": 0, "matched": 0} for f in
                 ["name", "address", "phone", "website", "category", "rating", "review_count", "hours"]}
    fresh_ok, fresh_n = 0, 0
    details = []
    for g in gt:
        rec = pr[prov][g["cid"]]
        t = g["truth"]
        row = {"cid": g["cid"], "name": t["name"], "mismatches": []}

        def grade(field, tv, pv, match):
            if tv in (None, "", []) or pv in (None, "", []):
                return
            per_field[field]["comparable"] += 1
            if match:
                per_field[field]["matched"] += 1
            else:
                row["mismatches"].append({"field": field, "truth": tv, "provider": pv})

        pv = rec.get(getters["name"])
        n_t, n_p = norm_name(t["name"]), norm_name(pv)
        grade("name", t["name"], pv, bool(n_t and n_p) and (n_t in n_p or n_p in n_t))
        pv = rec.get(getters["address"])
        grade("address", t["address"], pv, addr_key(t["address"]) == addr_key(pv) and addr_key(pv) != ("", ""))
        pv = rec.get(getters["phone"])
        grade("phone", t["phone"], pv, norm_phone(t["phone"]) == norm_phone(pv))
        pv = rec.get(getters["website"])
        grade("website", t["website"], pv, norm_domain(t["website"]) == norm_domain(pv))
        pv = rec.get(getters["category"])
        # truth category = primary type display OR any of the Places `types`
        # (primaryTypeDisplayName is often a generic bucket like "Services" -
        # confirmed on 12/12 agencies - while `types` carries the real
        # listing categories; generic-only truths are not comparable)
        GENERIC = {"services", "service", "pointofinterest", "establishment", "food", "store"}
        t_cats = [norm_name(t["category"])] + [norm_name(x.replace("_", "")) for x in (t.get("types") or [])]
        t_cats = [c for c in t_cats if c and c not in GENERIC]
        if t_cats and pv:
            pp = norm_name(pv)
            grade("category", (t["category"], t.get("types")), pv,
                  any(c in pp or pp in c for c in t_cats))
        tr, prv = fnum(t["rating"]), fnum(rec.get(getters["rating"]))
        if tr is not None and prv is not None:
            grade("rating", tr, prv, abs(tr - prv) <= 0.1)
        tc = fnum(t["review_count"])
        pc = fnum(rec.get(getters["review_count"])) if getters["review_count"] else None
        if tc is not None and pc is not None:
            grade("review_count", tc, pc, abs(tc - pc) <= max(5, 0.05 * tc))
        th, ph = truth_hours_map(t), hours_map(prov, rec)
        common = [d for d in DAYS if d in th and d in ph]
        if common:
            day_match = sum(1 for d in common if norm_time(th[d]) == norm_time(ph[d]))
            grade("hours", f"{len(common)} days", f"{day_match} match",
                  day_match >= max(1, round(0.8 * len(common))))

        # freshness: volatile fields current vs live
        f_ok = True
        f_seen = False
        if tr is not None and prv is not None:
            f_seen = True
            f_ok &= abs(tr - prv) <= 0.1
        if tc is not None and pc is not None:
            f_seen = True
            f_ok &= abs(tc - pc) <= max(5, 0.05 * tc)
        if f_seen:
            fresh_n += 1
            fresh_ok += 1 if f_ok else 0
            row["fresh"] = f_ok
        details.append(row)

    comparable = sum(v["comparable"] for v in per_field.values())
    matched = sum(v["matched"] for v in per_field.values())
    summary[prov] = {
        "accuracy_pct": round(100 * matched / comparable, 1),
        "fields_compared": comparable, "fields_matched": matched,
        "per_field": {f: (f"{v['matched']}/{v['comparable']}" if v["comparable"] else "n/a")
                      for f, v in per_field.items()},
        "freshness_pct": round(100 * fresh_ok / fresh_n, 1) if fresh_n else None,
        "freshness_records": f"{fresh_ok}/{fresh_n}",
        "freshness_basis": "rating only (no review-count field)" if not getters["review_count"] else "rating + review count",
    }
    outd = ROOT / "data" / ("brightdata" if prov == "BrightData" else prov.lower()) / "analysis"
    outd.mkdir(parents=True, exist_ok=True)
    (outd / "ground-truth-match.json").write_text(json.dumps(
        {"method": "ground-truth/sample-24.json (Places API live capture 2026-09-24) vs benchmark records",
         "summary": summary[prov], "records": details}, indent=2, ensure_ascii=False), encoding="utf-8")

print(json.dumps(summary, indent=1))
