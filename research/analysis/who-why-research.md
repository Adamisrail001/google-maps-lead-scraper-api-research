# Who uses a Google Maps scraper, and why — fresh confirmation sweep (2026-09-24)

**Method:** independent web sample of real user voices (Hacker News, BlackHatWorld, IndieHackers, OSS tool issues/READMEs), collected 2026-09-24 to validate `user-intent.md`'s persona split after the lead's review. Reddit was unreachable from this environment (blocked; pullpush/arctic-shift rate-limited) — sample skews HN/forums, which likely *understates* the email-leads share somewhat.

## Users found

| Who (role/business) | Job | Fields explicitly needed | Price sensitivity | Source |
|---|---|---|---|---|
| Builder of a diaspora-owned business directory | Populate a community directory | ratings, phone, hours (NAP-type) | Expected ~$89, billed **$504** by Places API (20k businesses) | news.ycombinator.com/item?id=46953870 |
| Solo dev running a web agency | Outbound sales leads | websites, phones, addresses ("a ton of listings are missing websites") | Built own free scraper | news.ycombinator.com/item?id=44555519 |
| IT services company operator | Find SMBs needing IT upgrades | locations + phone | — | news.ycombinator.com/item?id=42551941 |
| Website-redesign service (Pitchkit) | Pitch businesses with no/poor website | name, category, photos, reviews, phone | — | news.ycombinator.com/item?id=47298481 |
| Lead-gen tool founder (Potarix) | Maps data at scale for SMB leads | names, locations, contact details | Apify pricing a blocker at scale | news.ycombinator.com/item?id=42462198 |
| Developer, places app | Place search | POI | "Places API is ludicrously expensive" → Foursquare free tier | news.ycombinator.com/item?id=20632041 |
| Pub-crawl map builder | Map of bars/pubs | locations | avoided "very expensive" Places API | news.ycombinator.com/item?id=48204071 |
| Location-service dev | Business search | POI | "WAAAYYY TOO EXPENSIVE" → TomTom | news.ycombinator.com/item?id=30558381 |
| Location comments app (Gridtalk) | Business data by coordinates | POI/NAP | paid APIs "quite expensive" | news.ycombinator.com/item?id=41636114 |
| Analyst | Map competition eliminated by a merger | store names, addresses, coordinates | — | news.ycombinator.com/item?id=33233693 |
| OSS scraper author (proxy for his users) | Business lists to CSV | names, addresses, ratings, review counts, phones | free | news.ycombinator.com/item?id=44786181 |
| BHW SEO/agency users (via search snippets; site unreachable from env) | Cold email/SEO outreach | **emails on top of Maps data**; workflow: "scrape Maps and crawl business websites to get emails" | prefer free/cheap | blackhatworld.com threads 1182586, 1594120, 1581675 |

## Synthesis

Two populations. **(a) Builders/analysts/agencies prospecting by phone or website** need the listing itself — name, address, phone, website, hours, ratings — at scale and cheap; nearly all arrived at scrapers after a Places-API cost shock (the $504-bill directory builder is archetypal). **(b) Cold-outreach lead generators** (SEO/web-design agencies, freelancers — concentrated on BHW/IndieHackers, not HN) explicitly want emails/socials on top. In this sample, roughly **60–70% of voiced demand is listing-fields-only; ~30–40% wants email-enriched leads**. The email-seekers largely understand that emails are not listing data — multiple sources state emails come from crawling the business's website (e.g. gosom/google-maps-scraper README), and one lead-gen pattern even filters "has website but no email listed" as the pitch signal.

**Implication used in this benchmark (lead decision 2026-09-24):** the ranking's user is the listings extractor (name, address, phone, hours, all listings, affordable + reliable); enrichment is bonus value, never a disqualifier. Consistent with `user-intent.md`'s persona evidence and this fresh sample.

Other sources checked: news.ycombinator.com/item?id=42516229, ?id=46305413; github.com/gosom/google-maps-scraper; indiehackers.com/post/best-google-maps-scrapers-top-5-for-email-phone-list-building-a187a18972
