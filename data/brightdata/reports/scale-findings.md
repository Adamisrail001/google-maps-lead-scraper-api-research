# Bright Data "Google Maps full information" — Stage-2 Scale Test Findings

**Date:** 2026-09-23 · **Design:** 2 runs × 10 sub-area inputs × limit_per_input 100 (2 × 1,000 ceiling, per completion brief) · discovery by location (`country`+`keyword`) · **Raw:** `data/brightdata/raw/run1|run2/snapshot.json` + logs · **Script:** `scripts/brightdata_scale_run.py`

| | Run 1 (agencies) | Run 2 (restaurants) | Both |
|---|---:|---:|---:|
| Rows / unique (place_id) | 756 / 753 | 985 / 985 | **1,738 unique** |
| Errors | 3 | 0 | 3 (0.2%) |
| Delivery vs 1,000 ceiling | 75.6% | 98.5% | 87% |
| Wall-clock | 389 s | 340 s | ~6 min/run |

**Field fills (unique rows):** name/category/rating/review-count 100%; phone 93–98%; address 92–100%; website 89–92%; hours 89–98%. Duplicate rate near zero (batch discovery dedupes internally).

**Emails/socials at scale: confirmed ZERO** — no fields, 2 incidental @-strings in review text across 1,738 records. The smoke conclusion holds at volume.

**Cost: not measurable via this API flow** (no billing field in trigger/progress/snapshot responses). Rate-card estimate: ~1,741 records ≈ **$2.61 at the third-party-reported $1.50/1K** (range $0.75–1.50 unconfirmed) → ≈ **$1.50/1K unique, estimate flagged** — verify in the dashboard's billing screen before publishing any Bright Data cost figure.

**Persona placement:** persona 1 (local-data extractor) — a serious contender: near-perfect core fills at the lowest at-scale price verified-ish so far, async batch model, ~6 min/1K. Persona 2 — not eligible (no contacts). Persona 3 — capable (snapshot/webhook delivery), with two frictions: no text-query input mode (`country`+`keyword` discovery only), and account onboarding (geo-blocks, dashboard activation, DNS-blocked domains on some networks — all documented findings).
**Run-2 download quirk:** progress `ready` ≠ snapshot downloadable — first fetch returned `{"status":"building"}`; needed retry ~30s later. Scale scripts must handle this.
