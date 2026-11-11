---
id: M-source-criticism
lang: en
title: Source criticism and analytical reports — the evidence scale, provenance tracking
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [research, options, strategy, validation]
tags: [sources, credibility, triangulation, red-flags, evidence-log, provenance, reports, bias]
related: [M-benchmarking, M-market-sizing, M-trends-scenarios, M-external-environment, M-marketing-research, M-ai-in-research, M-traction-model]
---

# Source Criticism and Analytical Reports

## When to apply
Any external figure, forecast or claim that goes into a conclusion, a model or a recommendation: a consulting/vendor/government report, a benchmark, a market size, a trend, an LLM answer, a user's words about their own metrics. The rule: **a report is a hypothesis, not a fact**, until it has been verified and triangulated.

## Core idea
### The evidence scale (evidence grade)
| Grade | Criteria | Confidence | How to use it |
|---|---|---|---|
| **A** | A primary source or project data with a disclosed methodology; confirmed by at least 2 independent sources (triangulation); the age is within the tolerance; comparable by segment, period and definition | High | The backbone of the decision |
| **B** | An authoritative secondary source with a methodology (Tier-1 consulting, a regulator, a report with a disclosed method); partially confirmed, or there are caveats about comparability | Medium | A backbone with a range and a caveat |
| **C** | A single source, a retelling, no methodology, a sponsor's interest, the age at the edge of the tolerance, an expert estimate without verification | Low | Only a hypothesis/landmark; sensitivity analysis and a verification plan are mandatory |
| **D** | It is not verified, or there are red flags (no primary source/definitions, "internal analysis", figures that are too precise or too round without an interval), or an agent's assumption without a source | Very low | Not a basis for a decision; only an explicitly labeled assumption |

**The weak-link rule:** the grade of a conclusion is never higher than the grade of its weakest critical input. If the decision is sensitive to an input of grade C/D — verification or data collection comes first.

### Types of sources and the main risk
| Type | Pros | What to check first of all |
|---|---|---|
| Government/international (OECD, UNCTAD, Rosstat, national statistics institutes) | neutrality, a described methodology, cross-country comparability | the data lag (6–12 months), the political optic |
| Reports of IT companies | signals earlier than anyone (telemetry) | no methodology; product changes create a "trend"; an interest in a favorable reading |
| Consulting (McKinsey, BCG, Deloitte, PwC) | Tier-1 discloses its method | a layer of interpretations; a hidden customer/sponsor; niche consulting is weaker |
| Solo analysts | a personal vision | cherry-picking, a conflict of interest |
| Bank research, regulators (SEC, ECB, the Central Bank of Russia) | a deal/regulatory base | the financial optic |
| Public filings (10-K, quarterly) | financially audited | they may hide the inconvenient; the definitions of metrics are their own |
| VC/investor reports | fast signals of the market | a narrow venture focus, the interest of the fund |

## Procedure
A check in nine levels (for each report/source):
1. **The purpose.** Why are we analyzing this (choosing a segment, forecasting a market, testing a hypothesis), for whom is the conclusion, what horizon, what geography.
2. **The type and the author.** Determine the type from the table and the author's interest; bring the corresponding checks to the front.
3. **Source integrity:** the author and their competence; a one-off or a serial report; the sponsor and the beneficiary; conflicts of interest (a vendor affiliation, partnerships).
4. **Method integrity:** the definitions of the terms ("a user", "active", "the AI market"); the type of data — a survey (a sample bias, social desirability), a statistical model (assumptions, extrapolation), transactions/telemetry (incompleteness), desk research (secondary sources), mixed (the best of all); the sample (geography, industries, the roles of the respondents, weights, the collection period); the Accuracy/Credibility/Timeliness/Coherence indicators.
5. **Claim integrity:** pick 3–7 key claims/figures; confirm each with a second independent source; sanity checks:
   - the shares are ≤ 100%, the parts sum up into the whole;
   - the currency and the year match;
   - the order of magnitude (a market of $5 billion against $5 trillion);
   - the implied growth: `CAGR = (V_end / V_start)^(1/n) − 1` — is it realistic;
   - "a report of 2026" ≠ "data of 2026": check the date of collection.
6. **Assign a grade A–D** on the scale; match it against the age: fast-changing quantities (CAC, CPI, retention) — no older than 24 months; stable ones (margin, a long-term LTV) — 3–5 years; market data for market sizing — no older than 2–3 years (the rules of the skills).
7. **Triangulation:** at least 2–3 independent sources of different types (government statistics + a report + primary data); for benchmarks — 3, and a spread of more than 30% calls for caution. Dependent sources (retellings of one report) count as one.
8. **Record the provenance** (below) and make the decision according to the grade.
9. **Hand over the conclusion** with the caveats: what is confirmed, what is a hypothesis, what still needs to be checked.

### Red flags and green flags
| Red flags | Green flags |
|---|---|
| no definition of the market/category | a Methodology/Appendix section |
| figures without a link to the primary source | a glossary of terms |
| a too-precise forecast ("+14.7%") without a confidence interval | a Limitations section |
| a vendor report disguised as an independent one | a history of updates with a description of the changes |
| no geography and no profile of the respondents | the weighting and the cleaning of the data are described |
| "internal analysis" as the only source | for forecasts — scenarios, ranges, drivers |
| updates without a note on a change of methodology | the sponsorship is disclosed |
In addition: the narrative fallacy (the conclusions are stitched together under one story, there are no scenarios and no uncertainty); sponsor bias; terminological uncertainty; suspiciously round numbers.

The cognitive traps of the analyst: confirmation bias, overconfidence, survivorship bias, authority bias (faith in the guru); anchoring and the curse of knowledge when reviewing one's own work.

## Template / checklist
**The source passport:** the author · the type · the series (one-off/serial) · the sponsor · the year of publication · the date of the data collection · the geography · the definition of the key terms.

**The provenance record (Evidence Log) — one line per claim:**
| Field | What to record |
|---|---|
| ID | E-001… |
| Claim | the value, the unit, the period, the segment/geography, the definition |
| Source | the publisher, the title, the year, the page/section, the URL; primary or secondary |
| Method and sponsor | how it was obtained, who financed it |
| Dates | of publication · of the data collection · of when we read it |
| Triangulation | the IDs of the confirming records, or "none" |
| Grade A–D and Confidence | + why |
| Usage | where in the conclusion/model; the sensitivity of the result |
| The next check | what will be done, and by whom, before the decision |
Special cases: **a calculation by the agent** — record the formula, the inputs with their IDs, and the grade by the weak-link rule; **a user's words about their metrics** — "user data", graded by whether it can be verified (an export, a dashboard); **an LLM answer without a source** — grade D; do not invent a link, state that a search is needed.

In the text of the conclusion: the citation is placed right at the number (a hyperlink or the ID of the record), and not as a list at the end; next to it — the year and the grade.

A table of the key claims of the report: the claim · the status (confirmed/not) · the confirmation · the grade · the note.
Checklist: the source has been verified · the method is understood · the key figures are triangulated · there is no obvious conflict of interest · the limitations are disclosed · the definitions match ours.

## Typical mistakes
- Taking a figure from the headline of a report and not looking at the methodology.
- Comparing figures from different reports with different definitions of the market.
- Counting three retellings of one report as three sources.
- Not checking the date of the collection, confusing it with the date of publication.
- Taking a vendor report as neutral, and precise forecasts without an interval.
- Writing an assumption into a model without marking it as an assumption.
- Leaving a conclusion of grade A standing on inputs of grade C.

## Questions that can change the decision
- Is the final conclusion sensitive to this figure? If not — do not spend the time on digging deeper.
- Who wins if this number is true (the sponsor, the vendor, the author)?
- Do we or the user hold primary data that would replace the secondary source?
- Does the definition of the metric/market in the source match ours?
- How many independent confirmations are achievable within the time and the budget?

## Related maps
[[M-benchmarking]], [[M-market-sizing]], [[M-trends-scenarios]], [[M-external-environment]], [[M-marketing-research]], [[M-ai-in-research]], [[M-traction-model]]
