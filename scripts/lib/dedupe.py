"""Generic record deduper, shared by every provider's benchmark script.

Pattern module — the field names below (id/review_id/hash_id, url,
author_name/user_profile.name, timestamp/datetime, rating, title,
review_text) match a review/listing-style record shape. When adapting this
template to a new API comparison whose records look different, edit
build_review_key() to pull from that API's actual field names; dedupe()
itself never needs to change."""
import hashlib


def _normalize(value):
    if value is None:
        return ""
    return str(value).strip().lower()


def build_review_key(domain, review):
    """Three-tier dedupe key, in priority order:
    1. Native record ID (review['id'] / review['review_id'] / review['hash_id'])
    2. Record URL (review['url'])
    3. Deterministic hash of domain+author+timestamp+rating+title+text
    """
    native_id = _normalize(
        review.get("id") or review.get("review_id") or review.get("hash_id")
    )
    if native_id:
        return {"key": f"id:{native_id}", "keyType": "native_id"}

    url = _normalize(review.get("url"))
    if url:
        return {"key": f"url:{url}", "keyType": "url"}

    user_profile = review.get("user_profile") or {}
    author = _normalize(review.get("author_name") or user_profile.get("name"))
    timestamp = _normalize(review.get("timestamp") or review.get("datetime"))
    rating = review.get("rating")
    if isinstance(rating, dict):
        rating = rating.get("value")
    rating = _normalize(rating)
    title = _normalize(review.get("title"))
    text = _normalize(review.get("review_text"))

    hash_input = "|".join([_normalize(domain), author, timestamp, rating, title, text])
    digest = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()
    return {"key": f"hash:{digest}", "keyType": "hash"}


def build_lead_key(domain, lead):
    """Three-tier dedupe key for lead/listing-shaped records (Google Maps
    Leads benchmark), in priority order:
    1. Native place ID (lead['place_id'] / lead['google_id'])
    2. Record URL (lead['google_maps_url'] / lead['location_link'] / lead['url'])
    3. Deterministic hash of domain+name+address
    """
    native_id = _normalize(lead.get("place_id") or lead.get("google_id"))
    if native_id:
        return {"key": f"id:{native_id}", "keyType": "native_id"}

    url = _normalize(
        lead.get("google_maps_url") or lead.get("location_link") or lead.get("url")
    )
    if url:
        return {"key": f"url:{url}", "keyType": "url"}

    name = _normalize(lead.get("name"))
    address = _normalize(lead.get("address") or lead.get("full_address"))

    hash_input = "|".join([_normalize(domain), name, address])
    digest = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()
    return {"key": f"hash:{digest}", "keyType": "hash"}


def dedupe(entries, key_fn=build_review_key):
    """Dedupes a flat list of {domain, review} dict entries.
    Pass key_fn=build_lead_key for lead/listing-shaped records instead of
    review-shaped ones (testing-plan.md Section 4).
    Returns {"unique": [...], "duplicates": [...]}, each duplicate entry
    recording which key/original it collided with.
    """
    seen = {}
    unique = []
    duplicates = []

    for entry in entries:
        result = key_fn(entry["domain"], entry["review"])
        key, key_type = result["key"], result["keyType"]
        if key in seen:
            review = entry["review"]
            duplicates.append(
                {
                    "domain": entry["domain"],
                    "key": key,
                    "keyType": key_type,
                    "firstSeenDomain": seen[key]["domain"],
                    "review_title": review.get("title") or review.get("name"),
                    "timestamp": review.get("timestamp") or review.get("datetime"),
                }
            )
            continue
        seen[key] = entry
        unique_entry = dict(entry)
        unique_entry["dedupeKey"] = key
        unique_entry["dedupeKeyType"] = key_type
        unique.append(unique_entry)

    return {"unique": unique, "duplicates": duplicates}
