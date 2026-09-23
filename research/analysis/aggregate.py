"""Provider frequency aggregation across discovery sources.

Inputs:
  ../discovery/websearch-q01-q10.csv, ../discovery/websearch-q11-q21.csv (agent-collected)
  Ahrefs SERP appearances (encoded below from ../discovery/ahrefs-serp-raw.md)
  LLM sample appearances (encoded below from ../llm/llm-aggregation.md)
  Reddit thread appearances (../reddit/reddit-mentions.csv if present)

Output: provider-frequency.csv + provider-frequency.md (this folder)

Counting rules:
  - websearch: number of DISTINCT queries (of 21) where the provider appeared as a result
  - listicle: number of DISTINCT listicle articles mentioning the provider
  - ahrefs_serp: number of DISTINCT Ahrefs-stored SERPs (of 5) where provider appeared organically
  - llm: number of LLM samples (of 5) recommending the provider
  - reddit: number of distinct reddit threads mentioning the provider
No weighting, no invented score - raw counts only.
"""
import csv, re, json, os
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
DISC = os.path.join(HERE, "..", "discovery")
REDDIT = os.path.join(HERE, "..", "reddit", "reddit-mentions.csv")

# canonicalization: regex (case-insensitive) -> canonical provider name
CANON = [
    (r"apify", "Apify"),
    (r"outscraper", "Outscraper"),
    (r"bright ?data", "Bright Data"),
    (r"scrapingdog", "Scrapingdog"),
    (r"scraper ?api\b|scraperapi", "ScraperAPI"),
    (r"serpapi|serp api\b", "SerpApi"),
    (r"dataforseo|data for seo", "DataForSEO"),
    (r"lobstr", "Lobstr.io"),
    (r"scrap\.io", "Scrap.io"),
    (r"oxylabs", "Oxylabs"),
    (r"scrapingbee", "ScrapingBee"),
    (r"octoparse", "Octoparse"),
    (r"phantombuster", "PhantomBuster"),
    (r"gosom", "gosom (open source)"),
    (r"omkar", "Omkar Cloud (open source)"),
    (r"g ?maps ?extractor", "G Maps Extractor"),
    (r"map lead scraper|maplead", "Map Lead Scraper"),
    (r"leads[- ]sniper", "Leads Sniper"),
    (r"\bn8n\b", "n8n (workflow)"),
    (r"geoapify", "Geoapify"),
    (r"safegraph", "SafeGraph"),
    (r"traveltime", "TravelTime"),
    (r"hasdata", "HasData"),
    (r"crawlbase", "Crawlbase"),
    (r"zyla", "Zyla API Hub"),
    (r"scrapehero", "ScrapeHero"),
    (r"local ?prospects", "LocalProspects"),
    (r"nodatanobusiness", "NoDataNoBusiness"),
    (r"openmart", "Openmart"),
    (r"livescraper", "Livescraper"),
    (r"botsol", "Botsol"),
    (r"datablist", "Datablist"),
    (r"artisan", "Artisan"),
    (r"oppora", "Oppora"),
    (r"tendem", "Tendem"),
    (r"traject", "Traject Data"),
    (r"maps ?scraper & ?leads|mapsleads", "MapsLeads.net (extension)"),
    (r"maps scraper & map data|chrome ?web ?store|chrome extension", "Chrome extension (various)"),
    (r"mappr", "Mappr"),
    (r"bizdata", "BizData"),
]

def canon(name, url=""):
    s = (name or "") + " " + (url or "")
    for pat, c in CANON:
        if re.search(pat, s, re.I):
            return c
    return None  # non-provider rows (blogs, SO, reddit threads, generic tutorials)

# distinct-query websearch appearances + distinct-listicle mentions
ws_queries = defaultdict(set)
listicle_arts = defaultdict(set)
all_queries = set()
for f in ("websearch-q01-q10.csv", "websearch-q11-q21.csv"):
    with open(os.path.join(DISC, f), encoding="utf-8-sig") as fh:
        for row in csv.DictReader(fh):
            c = canon(row["provider"], row["url"])
            if not c:
                continue
            if row["source"].strip().lower() == "websearch":
                all_queries.add(row["query_id"])
                ws_queries[c].add(row["query_id"])
            elif row["source"].startswith("listicle"):
                listicle_arts[c].add(row["source"])

# Ahrefs stored SERPs (from ahrefs-serp-raw.md, organic positions only)
AHREFS_SERPS = {
    "Q06": ["Apify", "gosom (open source)", "Outscraper", "Bright Data", "Scrapingdog",
            "ScraperAPI", "Chrome extension (various)", "n8n (workflow)"],
    "Q02": ["MapsLeads.net (extension)", "Outscraper", "Apify", "Scrap.io",
            "gosom (open source)", "Octoparse", "G Maps Extractor"],
    "Q12": ["Geoapify", "TravelTime", "SafeGraph"],  # provider results only; blogs/SO excluded
    "Q21": ["Artisan", "gosom (open source)", "Leads Sniper"],
    "Q01_noserp": [],
}
ah = defaultdict(set)
for q, provs in AHREFS_SERPS.items():
    for p in provs:
        ah[p].add(q)

# LLM samples (from llm-aggregation.md)
LLM = {
    "Apify": 5, "SerpApi": 5, "Bright Data": 5, "Outscraper": 4, "DataForSEO": 4,
    "Lobstr.io": 4, "Scrapingdog": 4, "Oxylabs": 3, "PhantomBuster": 3,
    "ScraperAPI": 2, "ScrapingBee": 2, "Crawlbase": 2, "Scrap.io": 2, "Octoparse": 2,
    "HasData": 1, "ScrapeHero": 1, "Traject Data": 1, "G Maps Extractor": 1,
}

# Reddit (optional, filled when agent completes)
reddit = defaultdict(set)
if os.path.exists(REDDIT):
    with open(REDDIT, encoding="utf-8-sig") as fh:
        for row in csv.DictReader(fh):
            c = canon(row["provider"], row.get("thread_url", ""))
            if c:
                reddit[c].add(row["thread_url"])

provs = set(ws_queries) | set(listicle_arts) | set(ah) | set(LLM) | set(reddit)
rows = []
for p in sorted(provs):
    w, l, a, m, r = (len(ws_queries[p]), len(listicle_arts[p]), len(ah[p]),
                     LLM.get(p, 0), len(reddit[p]))
    rows.append({"provider": p, "websearch_queries": w, "websearch_pct": round(100*w/21),
                 "ahrefs_serps": a, "listicles": l, "llm_samples": m, "reddit_threads": r,
                 "total_signals": w + a + l + m + r})
rows.sort(key=lambda x: -x["total_signals"])

out = os.path.join(HERE, "provider-frequency.csv")
with open(out, "w", newline="", encoding="utf-8") as fh:
    wtr = csv.DictWriter(fh, fieldnames=rows[0].keys())
    wtr.writeheader(); wtr.writerows(rows)
print(f"queries covered by websearch CSVs: {sorted(all_queries)} ({len(all_queries)})")
print(f"reddit csv present: {os.path.exists(REDDIT)}")
for r in rows[:25]:
    print(r)
