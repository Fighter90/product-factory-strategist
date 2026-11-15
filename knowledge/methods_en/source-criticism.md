---
id: M-source-criticism
lang: en
title: Critique of sources and analytical reports, evidence grading scale, provenance recording
course: skills
sources: ["EN mirror of the RU methodology card M-source-criticism (knowledge/methods/source-criticism.md); original sources are listed in the RU card"]
stages: [research, options, strategy, validation]
tags: [sources, credibility, triangulation, red-flags, evidence-log, provenance, reports, bias]
related: [M-benchmarking, M-market-sizing, M-trends-scenarios, M-external-environment, M-marketing-research, M-ai-in-research, M-traction-model]
---

# Critique of sources and analytical reports

## When to apply
Every external number, forecast or thesis enters a conclusion, model or recommendation: a consulting/vendor/government report, a benchmark, a market size, a trend, an LLM answer, a user's words about their own metrics. The rule: **a report is a hypothesis, not a fact**, until it is verified and triangulated.

## Essence
### Evidence grade scale
| Grade | Criteria | Confidence | How to use |
|---|---|---|---|
| **A** | A primary source or project data with a disclosed methodology; confirmed by at least 2 independent sources (triangulation); age within tolerance; comparable by segment, period, definition | High | The backbone of the decision |
| **B** | An authoritative secondary source with methodology (Tier-1 consulting, a regulator, a report with a disclosed methodology); partially confirmed or with comparability caveats | Medium | A support with a range and a caveat |
| **C** | A single source, a retelling, no methodology, sponsor interest, age at the edge of tolerance, an expert estimate without verification | Low | Only a hypothesis/orientation point; sensitivity analysis and a validation plan are mandatory |
| **D** | Not verifiable or has red flags (no primary source/definitions, "internal analysis", too-precise or too-round numbers without an interval), or an agent assumption without a source | Very low | Not a basis for a decision; only an explicitly flagged assumption |

**The weakest-link rule:** the grade of a conclusion is no higher than the grade of its weakest critical input. If the decision is sensitive to a C/D input — verification or data collection first.

### Source types and the main risk
| Type | Pros | What to check first |
|---|---|---|
| Government/international (OECD, UNCTAD, national statistics offices) | neutrality, described methodology, cross-country comparability | data lag (6–12 months), political optics |
| IT company reports | signals earlier than anyone (telemetry) | no methodology; product changes create a "trend"; interest in favorable interpretation |
| Consulting (McKinsey, BCG, Deloitte, PwC) | Tier-1 discloses the method | a layer of interpretations; hidden client/sponsor; niche consulting is weaker |
| Solo analysts | a personal vision | cherry-picking, conflict of interest |
| Bank research, regulators (SEC, ECB, central banks) | transaction/regulatory base | financial optics |
| Public filings (10-K, quarterly) | financially audited | may hide inconvenient facts; their own metric definitions |
| VC/investor reports | fast market signals | a narrow venture focus, the fund's interest |

## Procedure
Verification in five levels (for each report/source):
1. **Purpose.** Why we analyze (choosing a segment, market forecast, testing a hypothesis), for whom the conclusion, the horizon, the geography.
2. **Type and author.** Determine the type by the table and the author's interest; bring the corresponding checks to the front.
3. **Source integrity:** author and competencies; a one-off or a series; sponsor and beneficiary; conflict of interest (vendor affiliation, partnerships).
4. **Method integrity:** definitions of terms ("user", "active", "the AI market"); data type — a survey (sample bias, social desirability), a statistical model (assumptions, extrapolation), transactions/telemetry (incompleteness), desk research (secondary sources), mixed (the best); the sample (geography, industries, respondent roles, weights, collection period); Accuracy/Credibility/Timeliness/Coherence indicators.
5. **Claim integrity:** pick 3–7 key theses/numbers; confirm with a second independent source; sanity checks:
   - shares ≤ 100%, parts sum into a whole;
   - currency and year match;
   - order of magnitude (a $5 billion market vs $5 trillion);
   - implied growth: `CAGR = (V_end / V_start)^(1/n) − 1` — is it realistic;
   - "a 2026 report" ≠ "2026 data": check the collection date.
6. **Assign a grade A–D** by the scale; align with age: fast-moving quantities (CAC, CPI, retention) — no older than 24 months; stable ones (margin, long-term LTV) — 3–5 years; market data for market sizing — no older than 2–3 years (the skills' rules).
7. **Triangulation:** at least 2–3 independent sources of different types (official statistics + a report + primary data); for benchmarks — 3, a spread over 30% requires caution. Dependent sources (retellings of one report) count as one.
8. **Record provenance** (below) and make the decision by grade.
9. **Hand over the conclusion** with caveats: what is confirmed, what is a hypothesis, what needs checking.

### Red flags and green flags
| Red flags | Green flags |
|---|---|
| no market/category definition | a Methodology/Appendix section |
| numbers without a link to the primary source | a glossary of terms |
| an overly precise forecast ("+14.7%") without a confidence interval | a Limitations section |
| a vendor report posing as independent | an update history describing revisions |
| no geography or respondent profile | weighting and data cleaning described |
| "internal analysis" as the only source | for forecasts — scenarios, ranges, drivers |
| updates without noting a methodology change | sponsorship disclosed |
Additionally: narrative fallacy (conclusions stitched into one story, no scenarios or uncertainty); sponsor bias; terminological ambiguity; suspiciously round numbers.

The analyst's cognitive traps: confirmation bias, overconfidence, survivorship bias, authority bias (faith in a guru); anchoring and the curse of knowledge when reviewing one's own work.

## Template / checklist
**Source passport:** author · type · series (one-off/serial) · sponsor · publication year · data collection date · geography · definition of key terms.

**A provenance record (Evidence Log) — one row per claim:**
| Field | What to record |
|---|---|
| ID | E-001… |
| Claim | value, unit, period, segment/geography, definition |
| Source | publisher, title, year, page/section, URL; primary or secondary |
| Method and sponsor | how it was obtained, who funded it |
| Dates | publication · data collection · when we read it |
| Triangulation | IDs of confirming records or "none" |
| Grade A–D and Confidence | + why |
| Usage | where in the conclusion/model; sensitivity of the result |
| Next verification | what and who will do it before the decision |
Special cases: **an agent's calculation** — record the formula, the inputs with their IDs and the grade by the weakest-link rule; **a user's words about metrics** — "user data", graded by whether it can be verified (an export, a dashboard); **an LLM answer without a source** — grade D; do not invent a link, state that a search is needed.

In the conclusion text: the link goes directly on the number (a hyperlink or record ID), not in a list at the end; next to it — the year and the grade.

A table of the report's key theses: thesis · status (confirmed/not) · confirmation · grade · note.
Checklist: the source verified · the method understood · key numbers triangulated · no evident conflict of interest · limitations disclosed · definitions match ours.

## Common mistakes
- Taking a number from a report's headline and not looking at the methodology.
- Comparing numbers from different reports with different market definitions.
- Counting three retellings of one report as three sources.
- Not checking the collection date, confusing it with the publication date.
- Taking a vendor report as neutral and precise forecasts without an interval.
- Entering an assumption into a model without flagging it as an assumption.
- Leaving a conclusion at grade A while the inputs are grade C.

## Questions that can change the decision
- Is the final conclusion sensitive to this number? If not — do not spend time digging deeper.
- Who wins if this number is true (a sponsor, a vendor, the author)?
- Do we or the user have primary data that would replace the secondary source?
- Does the source's definition of the metric/market match ours?
- How many independent confirmations are achievable within time and budget?

## Related cards
[[M-benchmarking]], [[M-market-sizing]], [[M-trends-scenarios]], [[M-external-environment]], [[M-marketing-research]], [[M-ai-in-research]], [[M-traction-model]]
