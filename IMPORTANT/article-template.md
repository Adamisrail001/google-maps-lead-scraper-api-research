<!--
This is a fill-in-the-blanks clone of the actual published Trustpilot reviews API
article's structure, wording rhythm, and voice. Nothing here is abstracted or
reworded into generic instructions - it is the same article, same order, same
sentence shapes, with the Trustpilot-specific facts swapped for {placeholders}
and one addition: a scoring layer (Benchmark score / verdict band / scorecard
table), pulled from IMPORTANT/criteria.md, inserted at the same points a
numeric score would naturally sit.

Every image from the original article is replaced with an HTML comment in the
form: SCREENSHOT colon what to capture, then a "why" clause explaining what it
proves to the reader (see the comments throughout this file for the exact
syntax). Keep that comment in the draft until the real screenshot/gif
replaces it - never delete it and leave a blank gap; if you skip a
screenshot, say why.

Do not add sections that were not in the original article. Do not remove
sections that were. The multiple-full-winner-sections pattern (three deep
dives, not one winner + a flat table) is real and intentional - keep it.
-->

> **{WINNER} is the best {X} API for {core job, e.g. "collecting reviews at scale"}.** I asked it for {N} {records} from each of {M} {targets} and it returned all **{total}, with {0 duplicates / other headline reliability stat}**. Scored **{score}/10** on the benchmark. {Runner-up} is the only other API that {cleared the same wall / came close} in my tests.

## ⚡ 15-Second Summary

1. **The problem:** {X} locks {anonymous visitors / free-tier users} out after {the specific limit, e.g. "page 10 of reviews, 20 reviews a page"}. Most APIs stop at exactly **{N} {records} per {target}** because of it.
2. **How I tested:** **{N} APIs, {M} {targets}, {baseline size} each** as the baseline ({total} total), then **{depth size} per {target} ({depth total} total)** for the APIs that cleared the wall. Every raw run is in a [public repo]({repo_url}).
3. **{WINNER}:** **{result}**, {0 duplicates}, {100%} field coverage, {N} fields per {record}. Scored **{score}/10**. **${n} per 1K {records}** on the {plan} plan, **${n} per 1K** at volume. {One line on the one real trade-off, e.g. async workflow / no filters.}
4. **{PROVIDER_2}:** **{result}**, {0 duplicates}, **${n} to ${n} per 1K** measured. Scored **{score}/10**. {One line on its edge over the winner and its gap.}
5. **{PROVIDER_3}:** **${n} per 1K**, the cheapest by a mile, but {hard-capped at N / other structural limitation}.

<!-- SCREENSHOT: full comparison chart, all tested APIs side by side -- why: gives above-the-fold scanners (and LLM crawlers lifting just this section) one glanceable visual proof before they read a word of prose -->

Every {X} scraping project I've seen runs into the same wall. You ask for all the {records} and you get exactly {N}. No error, no warning, just {N} and a `{SUCCESS_STATUS}` status.

The official API is worse in a different way: {the access problem, e.g. "you can't even start without a waitlist approval"}. And the third-party APIs that promise "{marketing claim, e.g. all reviews}" mostly don't deliver them.

<!-- SCREENSHOT: the 15-second summary graphic itself, rendered as a branded image -- why: gives readers who skim past the text block a second, faster pass at the same verdict -->

So I tested the main {X} APIs side by side, same {targets}, same request shape, same day where possible.

For reproducibility, everything is in a public repo, down to the raw responses and the {credit/cost} snapshots.

[{X} API benchmark]({repo_url}#cta-link)

But first, the question everyone asks... **why not just use the official {X} API?**

## Does {X} have an official {record type} API?

{Yes/No}. {X} offers {list of official APIs/products}, but {the limitation, e.g. "most of them only let you read and reply to your own reviews"}.

👉 [Check {X} API documentation]({official_docs_url})

For collecting {records} of **other {entities}**, the only relevant one is the [{Official Cross-Business API name}]({url}). It exposes {what it exposes}, with the key endpoints being **{endpoint 1}** and **{endpoint 2}**, and {pagination mechanism, e.g. "the latter paginates with a token"}.

```bash
curl -X GET "{official_api_endpoint_example}" \
  -H "apikey: YOUR-API-KEY"
```

A sample response from the official docs:

```json
{
  "records": [
    {
      "id": "{sample_id}",
      "...": "..."
    }
  ],
  "nextToken": "..."
}
```

<!-- SCREENSHOT: the official API's data-access product page or endpoint list -- why: proves the endpoint and shape above are real, not paraphrased from memory -->

The catch is access. {State the exact friction: no sign-up / waitlist / sales call / approval tier.}

{Describe the waitlist/approval flow in one or two sentences, plainly, no editorializing.}

<!-- SCREENSHOT: the waitlist/access-request form or approval-gate screen -- why: the access-friction claim needs to be seen, not just asserted -->

Unless you're {the narrow segment that gets approved, e.g. enterprise or non-profit}, your chances are thin. So I excluded it from the comparison on **accessibility**, not capability.

{Optional: link to a fuller standalone official-API guide if one exists.}

## What about {X}'s internal API?

{X}'s own {page type} fetch their data from an internal {tech stack, e.g. Next.js} endpoint.

Open DevTools, switch to the **Network** tab, {the specific interaction that triggers it, e.g. "click to page 2 of any listing"}, and you'll see a request like this one for {example target}:

```text
{internal_endpoint_path_example}
```

<!-- SCREENSHOT: DevTools Network tab showing the real internal endpoint URL -- why: this is the "aha" discovery moment of the section, it has to be a real capture, not a description -->

The response is clean JSON with everything the page renders.

<!-- SCREENSHOT: the internal endpoint's raw JSON response -- why: proves the "clean JSON" claim and sets up the two problems named next -->

Tempting, but two problems.

It's an **undocumented internal endpoint**, so {the specific instability, e.g. "the build number in the path and the response shape can change without notice"}.

And it hits the same wall as your browser does: **{X} forces {the same block, e.g. a login} after {the same limit}**, so the internal API gives you a nicer JSON shape and the same {N} {records}.

<!-- SCREENSHOT: the login/paywall redirect that fires past the limit -- why: shows the ceiling is the same one third-party APIs hit, not a separate, worse problem -->

Good for understanding how {X} loads {records}. Not something I'd build a production pipeline on.

That leaves two routes: build your own scraper, or use a third-party {X} {record type} API.

Building your own works for the first scrape. Keeping it alive against {X}'s page changes, anti-bot measures and that {login/access} wall is where it turns into a maintenance job.
For this article I went with third-party APIs.

## How I picked and tested the APIs

I went through vendor docs, developer forums, Reddit threads and GitHub issues to build the long list, then cut it with six elimination rules:

1. **No self-serve access:** waitlist, sales call or no trial
2. **Run failure:** below 50% success rate, or breaks mid-run
3. **No usable docs:** you can't build a working request from the documentation alone
4. **Unclear pricing:** cost per 1K {records} can't be calculated
5. **Wrong data:** doesn't return {record}-level data
6. **Dead or abandoned:** no response, broken infrastructure, no maintenance

👉 [See the full elimination criteria]({repo_url}/blob/main/IMPORTANT/criteria.md#3-elimination-criteria)

{N} APIs survived: **{WINNER}, {PROVIDER_2}, {PROVIDER_3}, {PROVIDER_4} and {PROVIDER_5}**.

{Optional footnote for any provider-specific choice that needs explaining up front, e.g. "For {PROVIDER_2}, the {sub-product} in this comparison is X, not the more popular Y. I explain why in the {PROVIDER_2} section."}

<!-- SCREENSHOT/GIF: the research process itself (vendor docs / forum threads / GitHub issues open side by side) -- why: makes the sourcing claim feel lived-in, not asserted after the fact -->

### How I tested the APIs

Every API got the same {M} {targets}: **{target 1}, {target 2}, {target 3}, {target 4} and {target 5}**.

The baseline run asked for **{N} {records} per {target}, {total} in total**.

Any API that cleared the baseline without hitting a ceiling then got a depth run at **{depth N} {records} per {target}, {depth total} in total**.

<!-- SCREENSHOT/GIF: the fixed set of targets used across every provider -- why: proves every API was tested against the identical input, the core fairness claim of the whole benchmark -->

I judged each API on {N} things:

1. **Reliability:** did it return what I asked for, every time?
2. **Data quality:** was the data accurate and complete?
3. **Cost:** what did 1K {records} cost?
4. **Speed:** how fast did the run complete?
5. **Scalability:** could it collect more than {N} {records} from one {target}?
6. **Usability:** how much work is the integration?

For data quality, I hand-checked a [{N}-{record} sample from {target}]({ground_truth_url}) across {N} fields and used it as the ground truth for every API.

<!-- SCREENSHOT/GIF: the ground-truth sample being built/verified by hand -- why: shows the accuracy numbers later in the article trace to a real manual check, not the vendor's own claims -->

Here is how the {N} stacked up:

| | {WINNER} | {PROVIDER_2} | {PROVIDER_3} | {PROVIDER_4} | {PROVIDER_5} |
| --- | --- | --- | --- | --- | --- |
| **{Records} returned / requested** | | | | | |
| **Benchmark score** | {n}/10 | {n}/10 | {n}/10 | {n}/10 | {n}/10 |
| **Cost per 1K {records}** | | | | | |
| **Speed ({records}/min)** | | | | | |
| **Past {N} {records} per {target}?** | | | | | |
| **Data quality ({N} ground-truth fields)** | | | | | |
| **Input** | | | | | |

## Best {X} {record type} API: {WINNER}

- **User rating: {n}/5 ([{Source}]({review_source_url}), {N} reviews, as of {date})**
- **API type: {Sync/Async}**
- **Best for: {one line}**
- **Benchmark score: {n}/10 ({verdict band, e.g. "Best-in-class"})**

| Criterion | Score |
| --- | --- |
| Success Rate & Reliability | {n}/2.0 |
| Data Quality & Completeness | {n}/2.0 |
| Cost Efficiency | {n}/1.5 |
| Speed & Throughput | {n}/1.5 |
| Scalability | {n}/1.2 |
| Developer Experience | {n}/1.0 |
| Input Flexibility & Coverage | {n}/0.8 |

| **Pros** | **Cons** |
| --- | --- |
| {pro, with the number that backs it} | {con, stated plainly, never softened} |
| {pro} | |
| {pro} | |
| {pro} | |

### What is {WINNER}?

[{WINNER}]({product_url}) is {one-line description of the platform}. The one that matters here is the **{specific scraper/product name}**.

<!-- SCREENSHOT: the specific scraper/product's store or landing page -- why: orients a reader who's never heard of this specific product before pricing/data claims start -->

[{Store CTA line, e.g. "Scrape all {X} {records} from any {target}"}]({store_url}#cta-link)

### Pricing

{WINNER} is a {billing model} with [plans]({pricing_url}) from **${n} to ${n}**.

{Explain the unit economics in one line, e.g. "1 credit = 1 unique record."}

<!-- SCREENSHOT: the pricing page's plan table -- why: backs the exact dollar figures cited, a reader should be able to verify them in one click -->

**Cost per 1K {records}**

- **${n} per 1K** on the {entry plan}
- **${n} per 1K** at volume

<!-- SCREENSHOT/GIF (optional): a pricing/cost simulator or calculator, if the provider has one -- why: lets the reader plug in their own volume instead of trusting the article's numbers alone -->

### Data

One {record} object from a live run:

```json
{
  "...": "real, sanitized response object"
}
```

It gives you **{N} meaningful data points per {record}**: {summarize the categories of fields}.

{N} of those weren't available in every API I tested: **`{field_a}`**, **`{field_b}`** and **`{field_c}`**.

**Data quality**

- **Field coverage:** {n}/{total} ground-truth fields
- **Accuracy:** {n}/{total} {records} matched
- **Schema consistency:** {finding, e.g. "0 missing fields across N records"}
- **Freshness:** {finding}

### Speed

{N} runs, same {config}:

| **Run** | **{Records} collected** | **Completion time** | **{Records}/min** |
| --- | --- | --- | --- |
| Run 1 | | | |
| Run 2 | | | |

That's a range of **{n} to {n} {records} per minute**, averaging about **{n}**.

{Optional: concurrency test if one was run, same table shape, one line of interpretation.}

### Usability

{WINNER} runs on {a sync/async} model: **{name the model, e.g. "Squid -> Task -> Run -> Results"}**.

> {One-sentence plain-language definition of each unfamiliar term in the model name, e.g. "A Squid is the scraper instance, Tasks are the input URLs, a Run executes them, and you fetch results by polling the Run ID."}

The base URL is `{base_url}` and every request carries `{auth header pattern}`. {Note the auth mechanism, e.g. "Static token, no OAuth."}

<!-- SCREENSHOT/GIF: the API reference docs landing page -- why: shows a first-time reader what they'll actually land on when they go set this up themselves -->

[Check {WINNER} Documentation]({docs_url}#cta-link)

Here's the walkthrough, with the requests I actually ran.

### 1. {First step name}

```bash
curl --request POST \
  --url "{endpoint}" \
  --header "Authorization: {auth}" \
  --header "Content-Type: application/json" \
  --data '{ "...": "real request body" }'
```

Response, trimmed to the fields that matter:

```json
{ "...": "real, sanitized response" }
```

{One or two sentences explaining what this response's key fields mean for the next step.}

### 2. {Second step name}

{...repeat the same request/response/explanation shape for each remaining step, 3-5 steps total...}

<!-- SCREENSHOT/GIF: the final API reference page for the results/retrieval endpoint -- why: closes the walkthrough by showing where a reader lands once they've followed every step above -->

For the long version of this walkthrough, with {advanced options}, see the [{WINNER} {record type} API guide]({guide_url}).

### Verdict

{WINNER} is the pick when **{the one condition that matters}**. It was one of only {N} APIs to {the differentiator}, and the only one to do it with {the extra edge, e.g. a perfect ground-truth match}.

## {PROVIDER_2} via {sub-product}: {the other API that clears the same bar}

- **User rating: {n}/5 ({Source}, {N} reviews, as of {date}), for {the platform, not the sub-product} if that distinction matters**
- **API type: {Sync/Async}**
- **Best for: {one line}**
- **Benchmark score: {n}/10 ({verdict band})**

| Criterion | Score |
| --- | --- |
| Success Rate & Reliability | {n}/2.0 |
| Data Quality & Completeness | {n}/2.0 |
| Cost Efficiency | {n}/1.5 |
| Speed & Throughput | {n}/1.5 |
| Scalability | {n}/1.2 |
| Developer Experience | {n}/1.0 |
| Input Flexibility & Coverage | {n}/0.8 |

| **Pros** | **Cons** |
| --- | --- |
| {pro, matched {WINNER}'s headline result} | {con, plainly stated} |

### What is {PROVIDER_2}?

[{PROVIDER_2}]({url}) is {one-line description}.

{If applicable: name the specific sub-product/actor/plugin used, and explicitly call out that it's NOT the platform's most popular/default option, with the one-line reason why (e.g. the default one hard-caps or silently fails).}

<!-- SCREENSHOT: the specific sub-product's store/marketplace listing -- why: proves this exact one exists and was chosen deliberately, not the platform's generic default -->

{One line confirming it delivers the depth-run result: e.g. "It returned {depth total} {records} from {M} {targets}, {depth total} in total, 0 duplicates."}

### Pricing

{Billing model}, plans from **${n}** to **${n}**.

<!-- SCREENSHOT: the pricing page -- why: backs the published rate cited below -->

**Cost per 1K {records}** ({sub-product}):

- **Published rate:** from ${n} per 1K
- **Measured:** **${n} per 1K** for {config A}, **${n} per 1K** for {config B}

### Data

One {record} object from the live response:

```json
{ "...": "real, sanitized response object" }
```

{One or two sentences on what's structured differently here vs. {WINNER}, and what's missing at the company/entity level if anything.}

**Data quality**

- **Field coverage:** {n}/{total} ground-truth fields. {Note what's missing and whether it can be reconstructed from other fields.}
- **Accuracy:** {n}/{total} matched

### Speed

{N} configurations, same {M} {targets}, {depth N} {records} each:

| **Config** | **{Records} collected** | **Completion time** | **Measured cost** |
| --- | --- | --- | --- |
| {Config A} | | | |
| {Config B} | | | |

{One line comparing this to {WINNER}'s equivalent run, naming the fair comparison point (e.g. same concurrency setting) rather than the flattering one.}

### Usability

{PROVIDER_2}'s model is **{execution model name}**. You {start/trigger}, poll until done, then read the output.

<!-- SCREENSHOT/GIF: the API reference docs -- why: same purpose as the winner's docs screenshot, consistency lets readers compare integration effort at a glance -->

[Check {PROVIDER_2} Documentation]({docs_url}#cta-link)

The base URL is `{base_url}` and auth is `{auth mechanism}`.

### 1. {First step name}

```bash
{real curl request}
```

Response:

```json
{ "...": "real, sanitized response" }
```

{Explain the one non-obvious parameter or field here, e.g. per-input vs. shared caps.}

### 2. {Second step name}

{...repeat for remaining steps...}

{One line on documentation quality/gaps and whether official SDKs/CLI/MCP apply.}

### Verdict

{If you're already invested in {PROVIDER_2}'s ecosystem}, `{sub-product}` gets you {the same/comparable} depth, {the one real edge it has over {WINNER}}. You trade away {the one real thing you lose}.

## {PROVIDER_3}: {the other angle, e.g. "the cheapest {X} API"}

- **User rating: {n}/5 ({Source}, {N} reviews, as of {date})**
- **API type: {Sync/Async}**
- **Best for: {one line}**
- **Benchmark score: {n}/10 ({verdict band})**

| Criterion | Score |
| --- | --- |
| Success Rate & Reliability | {n}/2.0 |
| Data Quality & Completeness | {n}/2.0 |
| Cost Efficiency | {n}/1.5 |
| Speed & Throughput | {n}/1.5 |
| Scalability | {n}/1.2 |
| Developer Experience | {n}/1.0 |
| Input Flexibility & Coverage | {n}/0.8 |

| **Pros** | **Cons** |
| --- | --- |
| **${n} per 1K {records}** measured, {n}x cheaper than {WINNER}'s entry rate | {The one hard structural limitation, stated plainly} |
| {pro} | {con} |

### What is {PROVIDER_3}?

[{PROVIDER_3}]({url}) {one-line description, e.g. "sells {category} data over APIs, and one of them is a dedicated {X} {record type} API"}.

<!-- SCREENSHOT: the specific product page -- why: shows the exact product being tested exists as a named, dedicated offering -->

### Pricing

{Billing model}. The published rate is **${n} per {unit}**, which is **${n} per 1K**. I measured **${n} per 1K** on the actual runs.

<!-- SCREENSHOT: the pricing page -- why: backs the exact published-vs-measured comparison -->

### Data

One {record} object from the live response:

```json
{ "...": "real, sanitized response object" }
```

{One or two sentences on what fields this provider adds that others don't, and what came back null/unused.}

**Data quality**

- **Field coverage:** {n}/{total} ground-truth fields, {note if it's the narrowest of the set}. Missing: {list}
- **Accuracy:** {n}/{total} matched
- **Schema consistency:** {finding}

### Speed

| **Run** | **{Records} collected** | **Completion time** | **{Records}/min** |
| --- | --- | --- | --- |
| Run 1 | | | |
| Run 2 | | | |

A range of **{n} to {n} {records} per minute**. {One line on why the range exists, e.g. queue variance, and whether it's within the documented worst case.}

### Usability

{PROVIDER_3}'s model is **{execution model name}**.

<!-- SCREENSHOT/GIF: the API reference docs -- why: same consistency purpose as the other two providers' docs screenshots -->

[Check {PROVIDER_3} Documentation]({docs_url}#cta-link)

The base URL is `{base_url}` and auth is `{auth mechanism}`. {Note if there's no official SDK, meaning raw HTTP calls.}

### 1. {First step name}

```bash
{real curl request}
```

Response:

```json
{ "...": "real, sanitized response" }
```

{Explain the key inputs available here, e.g. depth/sort/priority, and explicitly note what's NOT available (filters others have) if relevant.}

### 2. {Second step name}

{...repeat for remaining steps...}

{Note the one field that tells "the whole story" of this provider's limitation, e.g. requested-total vs. returned-total shown side by side in the response.}

### Verdict

{PROVIDER_3} is the pick when **{cost and simplicity, or whatever the real angle is} matter more than {depth/coverage/whatever it trades off}**. {One sentence stating the hard ceiling plainly.}

## Also tested: {PROVIDER_4} and {PROVIDER_5}

Both made the shortlist. Neither made the recommendations.

### {PROVIDER_4}

<!-- SCREENSHOT: the provider's product/homepage -- why: gives this shorter section the same one-glance orientation the full deep dives get -->

**{PROVIDER_4}** was {the headline positive}: **{result}, {0 errors}, {n}/{total} ground-truth fields, {n}/{total} matched**, scoring **{n}/10**, and {one structural strength, e.g. "accepts up to N inputs in one call, the widest batch input of the set"}.

{Optional: one line on a docs quality note, positive or negative.}

> The problem is {the one disqualifying flaw, e.g. price}: **${n} to ${n} per 1K {records}** {basis, e.g. "estimated from the rate card, since there's no billing endpoint"} for the same **{N}-{record} cap** {PROVIDER_3} gives you at ${n}. You're paying {n}x for {what you're not actually getting more of}.

### {PROVIDER_5}

<!-- SCREENSHOT: the provider's product/homepage -- why: same orientation purpose as above -->

**{PROVIDER_5}** has {a genuine strength, e.g. "the broadest SDK coverage of the set"} and its first run returned {early result}. Scored **{n}/10**.

> A later run on the same account returned **{degraded result}**.

{One closing sentence stating why this disqualifies it from a recommendation, plainly, not as a pile-on.}

## Which {X} {record type} API should you pick?

### {WINNER}: {the one-line framing, e.g. "every {record}, every {target}"}

{One paragraph: who needs this, the headline number, the score, the price.} [Start here]({store_url}#cta-link) if {the requirement} is the requirement.

### {PROVIDER_2}: {the one-line framing}

{Same result, the one real edge, the price, the score.} Worth it if {the specific precondition}. Not worth {the thing you shouldn't do just for this}.

### {PROVIDER_3}: {the one-line framing}

{The price, the workflow simplicity, the score.} If {the precondition} tells you what you need to know, nothing else comes close on {the dimension it wins}.

{Optional bridge line to a matching no-code roundup if one exists.}

## FAQ

### Why do most {X} APIs stop at {N} {records}?

Because {X} does. {Explain the underlying mechanism in one or two sentences.} {WINNER} and {PROVIDER_2} were the only {N} APIs in my test that got past it.

### Is scraping {X} {record type} data legal?

There's no universal yes or no. {X}'s terms {state the relevant restriction}, and legality depends on your jurisdiction and what you do with the data. This article tested whether APIs can technically collect this data; whether your use is permitted is a separate question. Check {X}'s terms and applicable law before using the data commercially, and read the [legal series on scraping]({legal_url}) for the background. This is not legal advice.

### Is the {X} API free?

{Direct answer.} {One or two sentences on the tier/pricing structure for the official route.}

### Why isn't {PROVIDER_4} recommended?

{The one disqualifying reason.} It delivered {the good result} with {the good stat}, but at {the bad number} it's {the comparative framing against a cheaper/better alternative that does the same job}.

### Can I reproduce these results?

Yes. Every run, with raw requests, responses, timings, cost and error reports, is in the [research repository]({repo_url}) under `{data_dir}/` and `{scripts_dir}/`. Swap in your own API keys and run the provider script you want to check, for example `{example_script_path}`.

## Conclusion

I tested {N} {X} {record type} APIs under the same conditions. {N} got past {the wall}: **{WINNER} and {PROVIDER_2}**.

**{WINNER} is my recommendation** for a {X} {record type} API, scoring **{n}/10**. {One sentence on why: purpose-built, returned everything asked, widest schema, ground-truth match, no tier surprises, or whatever the real reasons are.}

If {the precondition for {PROVIDER_2}}, {PROVIDER_2} is a legitimate alternative, scoring {n}/10. If {the precondition for {PROVIDER_3}}, {PROVIDER_3} at ${n} per 1K is the obvious choice.

Want to check the {headline claim} yourself? [**Try the {X} {record type} API**]({store_url}#cta-link).

**Have you tested any of these APIs? What was your experience?** [Connect with me on LinkedIn]({linkedin_url}).
