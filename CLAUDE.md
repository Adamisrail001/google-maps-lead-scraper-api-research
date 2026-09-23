# Lobstr API Research Workflow

## Purpose

This project is used to research and compare APIs for Lobstr articles.

The research must be:

- User-centric
- Evidence-based
- Reproducible
- Practical
- Focused on real API capabilities
- Free from unsupported popularity claims

Do not select competitors simply because they have similar technical features.

---

# 1. Start With User Intent

Before selecting competitors, identify what users are actually trying to accomplish.

For each Lobstr product, create 10–25 realistic search intents.

For Google Maps Leads Scraper, consider intents such as:

- Google Maps lead scraper
- Google Maps business leads API
- Google Maps scraper API
- Google Maps business data API
- Google Maps lead generation API
- Google Places API alternative
- Google Maps scraper for thousands of businesses
- Google Maps business data at scale
- scrape Google Maps businesses
- Google Maps data extraction API

Expand the query set based on actual user language discovered during research.

---

# 2. Competitor Discovery

Search multiple sources where available:

- Google/web search
- Reddit
- LLM recommendations
- Relevant directories
- Comparison pages
- Ahrefs
- Other available research tools

Do not rely on a single search result, screenshot, article, or personal memory.

For every provider discovered, record:

- Provider
- Query
- Source
- URL
- Search position when available
- User intent
- Relevant product/API
- Evidence

Example:

| Query | Source | Provider | Position | URL | Intent |
|---|---|---|---:|---|---|
| Google Maps lead scraper | Google | Provider X | 3 | URL | Lead generation |

---

# 3. Evidence Before Conclusions

Never start with:

> "These are the top competitors."

Instead:

1. Collect raw discovery data.
2. Measure provider frequency.
3. Verify product relevance.
4. Check API availability.
5. Collect supporting traffic/SEO/community signals.
6. Then identify candidate competitors.

A single SERP screenshot is not enough to establish popularity.

Do not claim global popularity from our research.

Use precise wording such as:

> "Frequently surfaced across our research queries."

rather than:

> "Most popular."

unless there is sufficient evidence for the stronger claim.

---

# 4. Provider Frequency

Calculate measurable discovery signals.

Where possible record:

- Google appearances
- Reddit appearances
- LLM appearances
- Relevant pages
- Search position
- Appearance percentage

Example:

| Provider | Google | Reddit | LLM | Total |
|---|---:|---:|---:|---:|
| Provider A | 12 | 6 | 5 | 23 |
| Provider B | 10 | 8 | 4 | 22 |

Do not create arbitrary scores.

Frequency is a research signal, not proof of product quality.

---

# 5. Ahrefs

When Ahrefs access is available, collect relevant measurable signals.

Possible metrics:

- Domain Rating
- Organic traffic
- Organic keywords
- Referring domains
- Relevant search visibility

Record the date of the metric.

Do not treat total website traffic as direct proof of popularity for a particular API.

Use Ahrefs as one supporting signal among several.

---

# 6. Verify Every Candidate

For every candidate provider, verify:

### Product

- Does it actually provide Google Maps/business data?
- Does it solve the user's intended problem?
- Is it relevant to lead generation?

### API

- Is there a real API?
- Exact API URL
- Exact documentation URL
- Authentication method
- API key availability
- Pricing/access requirements
- Relevant endpoints

### Capability

Check relevant lead fields such as:

- Business name
- Address
- Phone
- Website
- Category
- Rating
- Review count
- Coordinates
- Opening hours
- Social profiles
- Business identifiers
- Other enrichment fields

Only record fields that are actually verified.

---

# 7. Categorise Providers

Use:

### Direct competitors

Providers offering a directly relevant Google Maps/business data API or equivalent programmatic product.

### Adjacent competitors

Providers capable of Google Maps scraping but whose primary product/use case is broader or different.

### Excluded

Providers that:

- Do not provide the required API
- Do not actually provide Google Maps/business data
- Cannot reasonably be tested
- Are irrelevant to the user intent
- Duplicate another product/provider
- Require inaccessible enterprise-only access

Always give a concrete exclusion reason.

---

# 8. Testing

After competitor discovery, test the selected APIs against the same realistic workloads.

Prioritise:

1. Required user-facing features
2. Data coverage
3. Reliability
4. Scalability
5. Speed
6. Cost
7. Ease of use

Do not force a numerical score unless the article methodology specifically requires it.

Record:

- Input
- Request
- Response
- Number of results
- Fields returned
- Errors
- Duplicates
- Runtime
- Cost
- Limitations

Preserve raw outputs whenever possible.

---

# 9. Research Artifacts

Every research project should preserve:

```text
research/
├── queries/
├── discovery/
├── reddit/
├── llm/
├── ahrefs/
├── providers/
├── raw/
├── analysis/
└── final/
```

The exact structure can change depending on the project.

Never throw away the evidence used to reach the final competitor selection.

---

# 10. Writing Principles

The article should address user needs rather than simply compare technical specifications.

Frame comparisons around questions such as:

- Which API handles this use case?
- Which API provides the required data?
- Which API works at this scale?
- What does the user have to configure?
- What limitations will the user encounter?
- What does it cost for the user's workload?
- What happens when the user needs enrichment?

Avoid unsupported claims.

Avoid calling something:

- Best
- Top
- Most popular
- Winner
- Worst

unless the methodology and evidence clearly justify the wording.

Prefer factual language:

> "In our testing..."

> "Across X discovery queries..."

> "Returned X results..."

> "We excluded Provider X because..."

> "Provider X appeared in X of Y searches..."

---

# 11. Reproducibility

Another engineer should be able to understand how the competitor list was produced.

For every important conclusion, ask:

> "What is the evidence?"

If evidence is unavailable, explicitly state that it is unavailable.

Do not fill gaps with assumptions.

---

# 12. Standard Workflow

For every new Lobstr API article:

```text
1. Understand Lobstr product
2. Define user intents
3. Generate search queries
4. Search multiple discovery sources
5. Save raw results
6. Measure provider frequency
7. Collect Ahrefs signals
8. Verify candidate APIs
9. Categorise direct/adjacent/excluded
10. Select candidates for testing
11. Test APIs
12. Save raw test results
13. Analyse results
14. Write article
```

This workflow should be reused for future Lobstr API comparison articles.