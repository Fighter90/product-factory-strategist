---
id: M-benchmarking
lang: en
title: Benchmarking — reference values for metrics and checking whether they apply
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [research, options, validation, after-decision]
tags: [benchmarking, retention, churn, conversion, comparability, survivorship-bias, triangulation, best-practices]
related: [M-source-criticism, M-unit-economics, M-traction-model, M-product-metrics, M-market-sizing, M-competitors]
---

# Benchmarking: reference values for metrics and checking whether they apply

## When to apply
"What retention/conversion/churn/CAC is considered normal?", "are our metrics better or worse than the market's?", "where do I get an assumption for a model when there is no data?", "can this number from an article be trusted?", "which best practices should we take?". The card contains no ready-made numerical benchmarks — it describes how to find and verify them; the numbers are taken from sources with a stated confidence grade ([[M-source-criticism]]).

## Core idea
**A benchmark** — a reference value of a metric used for comparison. What counts as "reference" depends on the goal: the best (P95/P99) — an aspiration level; the median (P50) — a realistic industry level; the minimum (P25) — below it is dangerous. Always use a **P25–P50–P95 range**, not a single number; a benchmark is a compass, not a law.

Why it is needed: to prioritize features, find weak spots, set KPI/OKR, calibrate the model (sanity check, calibration, explaining deviations — [[M-traction-model]]).

**Metric types and mandatory cuts**
| Type | What to clarify |
|---|---|
| Funnel (visit → registration → activation → purchase) | new/returning; channel (cold/warm, organic/paid); platform (web/mobile, iOS/Android); region, language; client type (SMB, Mid-Market, Enterprise) |
| Retention | paying/free; cohorts by launch period; window: D1/D7/D30 for consumer apps, M1/M3/M12 for B2B SaaS; the criterion (any action or a paying one) |
| Churn | logo churn (% of clients), revenue churn (% of revenue), gross vs net (minus expansion among those who stayed); new and old clients separately |
| Monetization (UE, LTV, CAC, ARPU) | new/existing payers; currency and taxes (gross/net revenue); fixed costs are outside UE; the region's purchasing power (CTR/CPC differ 5+× between countries per the skill's estimate); core vs casual |

**Biases:** survivorship bias (the worst ones are silent — the visible average is higher than the real one); vendor bias (a platform exaggerates the problem in order to sell a solution); startups publish flattering metrics (LTV/CAC = 5 measured on the best segment); suspiciously round numbers (10%, 50%) — probably an estimate; the context-killer (25% of what: D30? D90? paying users?); stale data.

## Procedure
1. **Define the metric:** formula, units, period, cohort, activity criterion. An example definition from the skill's template — D30 retention; in the template the formula is written as `DAU[Day30]/DAU[Day1]`, and this is a filled-in sample: fix your own metric as "the share of the cohort's users active on day N by criterion Z".
2. **Find sources:** search (with a filter by date and source type); experts (investors, angels, peers in the niche, consultants); reports from Sequoia, Y Combinator, Greylock, Reforge, Mixpanel, Amplitude, First Round Review; companies' public filings; your own A/B tests and history.
3. **Verify each benchmark (7 steps):**
   1. Origin: primary or a retelling; the author.
   2. Methodology: the sample, the segments, the collection period, the metric definition.
   3. Freshness: fast-moving metrics (CAC, CPI, retention) — no older than 24 months; stable ones (gross margin, long-term LTV) — up to 3–5 years is acceptable.
   4. Comparability: vertical/product, business model, geography and language, target segment, company stage, channel, seasonality, product age.
   5. Triangulation: at least 3 independent confirmations; a spread of more than 30% — caution.
   6. Biases: survivorship, vendor, flattery, "round numbers".
   7. Range and confidence level: P25/P50/P95 + High/Medium/Low (it maps onto the A–D grades in [[M-source-criticism]]).
4. **Score comparability on five axes** (the card's heuristic): the metric definition, the segment/client, the period and the season, the business model and the channel, the stage and the geography. All 5 match — use as is; 3–4 — adjust and explain the correction; 2 or fewer — only as an order of magnitude and a hypothesis to test.
5. **Compare your value with the range:** below P25 / between P25–P50 / above P50 / above P95 (a suspicion of a measurement error); explain the deviation (channel, model, segment, product age).
6. **Use it in the decision:** an OKR goal, a model assumption (with a discount if the source is weak), sensitivity around the range.
7. **Best practices:** collect 3 priority practices (UX/UI, onboarding, legal, logistics, monetization, notifications) through close study of competitors, search, expert interviews, conferences; for each one — the expected effect, the complexity, the source. An effect of "+X% retention" from someone else's case is a hypothesis, not a forecast.

## Template / checklist
Passport: metric · research period · segments · sources · author · date of last update.
The benchmark table:
| Metric | Definition / formula | P25 / P50 / P95 | Sources (a reference in the text) | Data age | Comparability (1–5) | Notes | Confidence |
|---|---|---|---|---|---|---|---|
The practices table: practice · area · description · expected result · complexity · source.
Conclusions: where we are below the benchmark and why; which practices come first; which KPIs for the quarter.

Checklist:
- [ ] The metric and the measurement method are defined
- [ ] At least 3 sources found
- [ ] For every number the origin is known (primary/secondary)
- [ ] The age is within tolerance (24 months for fast-moving ones; 3–5 years for stable ones)
- [ ] Comparability across vertical, model, geo, segment, stage
- [ ] A range built and a confidence level stated
- [ ] Survivorship bias accounted for
- [ ] The top-3 practices selected; KPIs set based on the range

## Typical mistakes
- Taking a single "average" number from a single article.
- Comparing a B2C app with B2B SaaS, SMB with Enterprise, Russia with the US without an adjustment.
- Taking retention for one day and comparing it with retention for 30 days.
- Accepting a vendor's number as independent (Amplitude will say that poor retention is a catastrophe).
- Using a three-year-old benchmark for fast-moving metrics.
- Setting a goal at P95 with no plan for how to reach it.
- Copying a best practice without checking the segment and the channel.

## Questions that can change the decision
- Whose metric is being compared: paying users' or everyone's, new or returning?
- Which channel brings in most of the traffic (SMM — low retention, partners — high)?
- What is the product's age (young apps sometimes see a jump in retention in months 2–6)?
- Is the decision sensitive to this assumption? If yes — spend the time collecting your own data or running a mini-experiment instead of a benchmark.
- Can retro-data or proxy metrics be obtained (a similar region, segment, product)?

## Related maps
[[M-source-criticism]], [[M-unit-economics]], [[M-traction-model]], [[M-product-metrics]], [[M-market-sizing]], [[M-competitors]]
