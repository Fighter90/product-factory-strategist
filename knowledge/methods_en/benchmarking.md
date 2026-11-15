---
id: M-benchmarking
lang: en
title: Benchmarking: reference values for metrics and verifying their applicability
course: skills
sources: ["EN mirror of the RU methodology card M-benchmarking (knowledge/methods/benchmarking.md); original sources are listed in the RU card"]
stages: [research, options, validation, after-decision]
tags: [benchmark, retention, churn, conversion, comparability, survivorship, triangulation, best-practices]
related: [M-source-criticism, M-unit-economics, M-traction-model, M-product-metrics, M-market-sizing, M-competitors]
---

# Benchmarking: reference values for metrics and verifying their applicability

## When to use
"Which retention/conversion/churn/CAC counts as normal?", "are our metrics worse or better than the market?", "where do I get an assumption for a model when there is no data?", "can I trust this figure from an article?", "which best practices should I take?". The card contains no ready-made numeric benchmarks — it describes how to find and verify them; the numbers come from sources labeled with an evidence class ([[M-source-criticism]]).

## Core idea
A **benchmark** is a reference value of a metric used for comparison. What counts as a "reference" depends on the goal: the best (P95/P99) — an aspiration target; the median (P50) — a realistic industry level; the minimum (P25) — below it is dangerous. Always use the **range P25–P50–P95**, not a single number; a benchmark is a compass, not a law.

Why: to prioritize features, find weak spots, set KPI/OKR, calibrate a model (sanity check, calibration, explaining deviations — [[M-traction-model]]).

**Metric types and mandatory cuts**
| Type | What to specify |
|---|---|
| Funnel (visit → registration → activation → purchase) | new/returning; channel (cold/warm, organic/paid); platform (web/mobile, iOS/Android); region, language; customer type (SMB, Mid-Market, Enterprise) |
| Retention | paying/free; cohorts by launch periods; window: D1/D7/D30 for consumer apps, M1/M3/M12 for B2B SaaS; criterion (any action or paying) |
| Churn | logo churn (% of customers), revenue churn (% of revenue), gross vs net (minus expansion among stayers); new and old customers separately |
| Monetization (UE, LTV, CAC, ARPU) | new/existing payers; currency and taxes (gross/net revenue); fixed costs outside UE; regional purchasing power (CTR/CPC between countries differ 5+ times by the skill's estimate); core vs casual |

**Biases:** survivorship bias (the worst stay silent — the visible average is above the real one); vendor bias (a platform exaggerates the problem to sell the solution); startups publish flattering metrics (LTV/CAC = 5 on their best segment); suspiciously round numbers (10%, 50%) — likely an estimate; context-killer (25% of what: D30? D90? payers?); stale data.

## Procedure
1. **Define the metric:** formula, units, period, cohort, activity criterion. An example definition from the skill's template — D30 retention; in the template the formula is written as `DAU[Day30]/DAU[Day1]`, that is a filled-in specimen: fix your own metric as "the share of the cohort's users active on day N by criterion Z."
2. **Find sources:** search (filtered by date and source type); experts (investors, angels, niche peers, consultants); reports from Sequoia, Y Combinator, Greylock, Reforge, Mixpanel, Amplitude, First Round Review; public company filings; your own A/B tests and history.
3. **Verify each benchmark (7 steps):**
   1. Provenance: primary or retelling; the author.
   2. Methodology: sample, segments, collection period, metric definition.
   3. Freshness: fast-moving ones (CAC, CPI, retention) — no older than 24 months; stable ones (gross margin, long-term LTV) — up to 3–5 years is acceptable.
   4. Comparability: vertical/product, business model, geography and language, target segment, company stage, channel, seasonality, product age.
   5. Triangulation: at least 3 independent confirmations; a spread above 30% — caution.
   6. Biases: survivorship, vendor, flattering numbers, "round numbers."
   7. Range and confidence level: P25/P50/P95 + High/Medium/Low (comparable with the A–D classes in [[M-source-criticism]]).
4. **Assess comparability on five axes** (the card's heuristic): metric definition, segment/customer, period and season, business model and channel, stage and geography. All 5 match — use as is; 3–4 — adjust and explain the correction; 2 or fewer — only as an order of magnitude and a hypothesis to verify.
5. **Compare your value with the range:** below P25 / between P25–P50 / above P50 / above P95 (suspicion of a measurement error); explain the deviation (channel, model, segment, product age).
6. **Use in the decision:** an OKR target, a model assumption (with a discount if the source is weak), sensitivity around the range.
7. **Best practices:** collect 3 priority practices (UX/UI, onboarding, legal, logistics, monetization, notifications) through competitive observation, search, expert interviews, conferences; for each — expected effect, complexity, source. An effect of "+X% retention" from someone else's case is a hypothesis, not a forecast.

## Template / checklist
Passport: metric · research period · segments · sources · author · date of refresh.
Benchmark table:
| Metric | Definition / formula | P25 / P50 / P95 | Sources (linked in text) | Data age | Comparability (1–5) | Remarks | Confidence |
|---|---|---|---|---|---|---|---|
Practices table: practice · area · description · expected result · complexity · source.
Conclusions: where we are below the benchmark and why; which practices come first; which KPIs for the quarter.

Checklist:
- [ ] Metric and measurement method defined
- [ ] At least 3 sources found
- [ ] For every figure the provenance is known (primary/secondary)
- [ ] Age within tolerance (24 months for fast-moving; 3–5 years for stable)
- [ ] Comparability across vertical, model, geography, segment, stage
- [ ] Range built and confidence level stated
- [ ] Survivorship bias accounted for
- [ ] Top-3 practices chosen; KPIs set based on the range

## Common mistakes
- Taking one "average" number from one article.
- Comparing a B2C app with B2B SaaS, SMB with Enterprise, one country with another without a correction.
- Taking retention for one day and comparing it with 30-day retention.
- Accepting a vendor's number as independent (Amplitude will say that poor retention is a disaster).
- Using a three-year-old benchmark for fast-moving metrics.
- Setting a goal at P95 without a plan for how to reach it.
- Copying a best practice without checking the segment and channel.

## Questions that can change the decision
- Whose metric is being compared: payers or everyone, new or returning?
- Which channel brings most of the traffic (SMM — low retention, partners — high)?
- What is the product's age (young apps sometimes show a retention jump in months 2–6)?
- Is the decision sensitive to this assumption? If yes — spend the time collecting your own data or running a mini-experiment instead of a benchmark.
- Can you get retro-data or proxy metrics (a close region, segment, product)?

## Related maps
[[M-source-criticism]], [[M-unit-economics]], [[M-traction-model]], [[M-product-metrics]], [[M-market-sizing]], [[M-competitors]]
