---
id: M-product-metrics
lang: en
title: Product metrics — types, funnels, retention and cohorts, metric tree, NSM, counter-metrics
course: pm
sources: ["EN mirror of the RU methodology card M-product-metrics (knowledge/methods/product-metrics.md); original sources are listed in the RU card"]
stages: [intake, research, validation, strategy, after-decision]
tags: [metrics, funnel, retention, cohorts, nsm, metric-tree, counter-metrics, cac, ltv, arpu, units-of-measure, proxy-metrics, seasonality, volatility, decomposition]
related: [M-success-metrics, M-loyalty-metrics, M-unit-economics, M-traction-model, M-quant-methods, M-cjm, M-mvp-pilots, M-pmf-scaling, M-solution-design, M-product-context, M-goals-drivers-bets, M-ab-testing, M-basic-statistics-pm, M-sql-for-pm, M-dashboards-visualization, M-forecasting-product]
---

# Product metrics

## When to apply
You need to choose/validate a goal metric, build a funnel and a metric tree, estimate the effect of an initiative, find the bottleneck, formulate a success criterion and a counter-metric. Especially — verifying that formulas, units and periods are consistent before drawing a conclusion.

## Essence

### What a metric is and when it is fit for use
A metric is a measurable indicator you define yourself in order to see and change the reality of the product. It is needed for: setting and tracking goals, prioritizing initiatives, justifying resources, designing tests, decisions about changes. **A metric is fit for use only if the answer is "yes" on every point:** it can be computed · data exists and is logged correctly · everyone understands and computes it the same way · it reflects a specific goal · it can be influenced by concrete actions · its dynamics can be tracked (chart, alert). The beginner's mistake is measuring "what is convenient" instead of "what matters". Metric lifecycle: choose → agree on the formula → get the data → compute → visualize → test and track → change goals and the metric when the goal changes.
**Metric passport:** what it measures · formula (numerator/denominator, units) · period and window · event source · owner · lever of influence · link to the goal.

### Classifications
- Product metrics (engagement, quality, usefulness: DAU/MAU, retention D1/D7/D30, Task Success, NPS, CSAT) vs business metrics (money, growth, economics: revenue/GMV, LTV, CAC, ARPU/ARPPU, ROI, Net Profit).
- Input (controllable, leading) vs output (results, lagging); growth metrics vs product metrics.
- Segments: audience (MAU, DAU, retention); finance; quality/value (Task Success, NPS, errors); conversion/funnel (AARRR); service (CSAT, SLA, response time); product steps (feature adoption, engagement); experiments (win rate, effect).
- Frameworks: AARRR (Acquisition, Activation, Retention, Referral, Revenue — e.g., for a music service: CR to install, CPA/CPC, sharing, activation by number of tracks played/likes, subscription, D1/D7/D30), HEART (focus on CX quality), One Metric That Matters (one metric per period), NSM (one for all the time), AIDA. A framework is adapted, not copied.

### Funnel
- **Conversion Rate (CR)** = users moving from step A to step B / users at step A, for the specified period. The funnel is built on the CJM; steps must be understood and counted identically by everyone.
- Rules: events phrased in the user's language; one path to the goal = one funnel (otherwise steps "get skipped" and percentages get distorted); funnel window = the real cycle of the action (e-commerce — minutes to days, SaaS — a week to a month); the first version of the funnel may be imperfect — what matters is seeing the drop-off quickly.
- **Reading the funnel:** (1) where is the sharpest collapse; (2) why exactly there — compare against benchmarks and unit economics ("very low"), hypothesize and test causes: high prices, slow delivery, technical errors, out-of-stock items, irrelevant search results; slice by segments (device, source, hour, age); (3) how much money we lose = lost users × average order value × period. Example: 10,000 people × 250 ₽ = 2.5M ₽ per day.
- **Unit check:** step conversion ≠ end-to-end. Example: search 100% → product page view 70% → cart 15% → payment 5%; step CRs: 70/100 = 70%; 15/70 = 21.4% (CR2Cart); 5/15 = 33.3%; end-to-end to payment — 5%. You cannot compare the step-level 21.4% and the end-to-end 15% as if they were the same kind of number; a gap in percentage points ≠ in percent (62% → 15% = −47 p.p. and −76% relative).
- A micro-funnel inside the step with the biggest loss; errors: non-exclusive steps, renamed events ("the funnel reset to zero"), floating window. Fixed by an "event passport" (entity, format, author, change date). The funnel is diagnostics; KPIs are phrased differently: "raise checkout CR from 15% to 25% by the end of the quarter".

### Retention, activity, cohorts
- **Retention Dn** = share of the cohort (users who arrived on day 0) that returned and performed the target action on day n. The zero point must be defined unambiguously (registration, first activity, e-mail confirmation) — shifting the zero point inflates retention.
- Models: classic cohort (D0-D1-D7-D30; e-commerce, fintech), N-day rolling (7-/28-day; social networks, content), product return rate ("returned and performed the target action"; B2B SaaS).
- **Cohorts**: by device, traffic source, first feature/scenario, acquisition period. Average retention without cohorts hides the problem. Reading the plateau of the curve — the higher it is, the more loyal the users.
- DAU/WAU/MAU; **Stickiness = DAU/MAU** (notes: 0.2–0.3 is typical for utilities, 0.5+ for top social networks — a reference point, depends on usage frequency); a drop with stable MAU means "users come but don't live there".
- Reading mistakes: artificial growth from a 90% discount (kills unit economics); mixing seasons; comparing cohorts of different ages without alignment.
- For rare transactions, retention is replaced by a proxy (share of active listings, etc.).

### Satisfaction
- **CSAT** — rating of a specific interaction (1–5), ask immediately. **CES** — user effort (scale 1–7), after complex/rare scenarios (return, cancellation, chat). **NPS** — willingness to recommend, 0–10; NPS = % promoters (9–10) − % critics (0–6), periodically (once a quarter/after accumulated experience), by segments. One question per interaction. Mistakes: surveying too late, mixing scales, long questionnaires, ignoring segments (NPS of old customers is usually higher than of new ones). Link to money: CSAT → repeat purchases/cross-sell; CES → support operating costs; NPS → organic growth/CAC. Specific numbers for the links come only from the product's own data.

### Money and growth (formulas with units)
| Metric | Formula | Units / period |
|---|---|---|
| ARPU | period revenue / active users of the period | ₽ per user per period |
| ARPPU | period revenue / paying users of the period | ₽ per paying user per period |
| GMV | sum of prices of all orders (before costs deducted) | ₽ per period |
| AOV | GMV / number of orders | ₽ per order |
| CAC | marketing spend of the period (full composition: bonuses, store commissions, referral payouts, part of payroll) / new customers of the same period | ₽ per customer |
| ROAS | campaign revenue / campaign spend | unitless; windows of 24 h and 7 days |
| ROMI | (revenue − marketing spend) / spend | % or fraction |
| Payback | CAC / (contribution margin per user per period) | periods (months) |
| LTV | in the simplest model ARPU × expected number of active periods; with constant retention r per period ≈ ARPU / (1 − r) | ₽; periods consistent with r |
Checks: an ARPU "per day" cannot be divided by a "per week" retention; LTV and CAC must be compared in the same currency and on comparable margin (marginal LTV, not revenue, is better); CAC and revenue — for the same period and the same cohort; separate promo revenue from organic revenue; convert multi-currency GMV at the exchange rate of the transaction date; ARPU is computed over actives, ARPPU over payers — do not substitute one for the other. The notes sometimes show "CM = ARPU − CAC − Cvar": this mixes a periodic income with a one-off acquisition cost — it is more correct to compare the accumulated lifetime contribution (LTV by margin) with CAC ([[M-unit-economics]]).
Reference points from the notes (verify, do not accept as norms): CAC ≤ ~30% of LTV; 7-day ROAS ≥ 1.2; Payback ≤ 3 months for a mature business (up to 6 for a startup); paid-channel retention no lower than organic by more than ~5 p.p.

### NSM and the metric tree
- **NSM** — the main metric reflecting value for the user and linked to revenue/LTV. Selection: (1) what is the core value? (2) which unit of outcome can be measured? (3) is it scalable and does it influence growth? Criteria: clear link to value; correlation with revenue/LTV (verify on history); sufficient frequency of change (weeks/months); several functions influence it; explainable in simple words. Examples: listening minutes by a paying user; number of successful transactions per day; deals won per month. Mistakes: changing the NSM every quarter (the rule is it lives about a year and changes when strategy changes); too distant from executors (then driver proxies closer to actions are used). Hierarchy: NSM → drivers (2–4) → operational metrics → process ones (Lead Time, Change Failure Rate).
- **Metric tree:** links local changes to the business goal. Example: GMV = number of orders × average order value; orders = users × CR to purchase; average order value = average number of items × average price. Rules: decompose mathematically everything that can be decomposed, the rest by meaning; keep the levels connected; descend to the level where you can actually influence; every "arrow" has an owner and a verified link (correlation/experiment, not an assumption).
- **Choosing the key metric:** stage of the business → which problem the product solves for the business → what we want from users → what we can actually influence → proxy metrics for reaching the goal from several sides.

### Counter-metrics (guardrails)
Metrics that must not deteriorate while the target metric grows: NPS/CSAT/CES, SLA and response time, Contact Rate, refunds, complaints, retention, CAC, metrics of adjacent products (cannibalization), latency. For each — a threshold set before the start. Example: "fast delivery" raised GMV by 6%, but CES showed growing effort and NPS a month later dropped by 4 p.p. — "a short-lived success without effort control gets rolled back through retention".

### Metric trio: target → proxy → counter (levels of application)
For any task — from a yearly strategy to a single feature/A/B test — metrics are assembled into a trio:
| Role | Question | Property |
|---|---|---|
| Target | what counts as success? | the main criterion, may change slowly |
| Proxy (1–3) | what moves earlier and predicts the target? | sensitivity + proven correlation with the target |
| Counter (2–3) | what must not be allowed? | thresholds set before the start (see guardrails above) |
Selection starts with three questions: the goal ("what we want to achieve"), the moving factors ("thanks to what"), the risks ("which side effects are possible"). If the target metric is hard to measure within the period, an earlier funnel stage is taken (contacts, views) and its correlation with the main metric is proven. After the experiment the decision: **Scale** (rollout) / **Iterate** (refine and retest) / **Drop** (abandon and record in the knowledge base).

### A good metric: sensitivity × stability × simplicity
| Criterion | Meaning | How to verify |
|---|---|---|
| Sensitivity | reacts to a product change within days, not months | will it "catch" the effect of a test; CTR — yes, retention — no for a button |
| Stability | changes only from the product, not from external noise | history chart without chaotic "spikes"; weak seasonality |
| Simplicity | the formula and the link to the goal are explainable without an analyst | "what-if": if the metric grows by 10% — is it clear what to do? |
Balance is achieved by choosing the level of aggregation and accounting for seasonality (moving average, ratios instead of absolutes). Before inclusion in OKR the metric is "broken in" on history. Bad signs: a noisy metric (increase the window or switch to a share), an opaque composite index (split it or replace it with a component closer to the goal), manipulative ambiguity ("time on page" is interpreted both ways — unfit as a final criterion).

### A metric drop can be normal: a triage algorithm
Before "rescuing the product", go through the steps in order — the analysis may stop at any of them:
1. **Context and magnitude — three questions:** how strongly did it drop (magnitude versus usual spread), when exactly (link to a release/campaign/date), for whom (everyone or one segment: new users, region, platform). Coin analogy: 4–6 "heads" out of 10 — normal, 10 in a row — an anomaly.
2. **Volatility vs trend:** outline a "corridor of normal values" on 3–6 months of history; a deviation inside the corridor — natural fluctuation, no analysis needed. A sharp drop over a short time → bug/release/campaign/external event; a gradual decline over weeks → a systemic cause. Growth is checked with the same algorithm: growth can also be random or external.
3. **Data verification:** the most common cause of "drops" is technical failures. Check: did the sources recalculate in the DWH; were there collection failures (test users in production); did the computation code of the data mart change; are there duplicate rows (doubling for one day gives "a sharp rise and a roll back" — almost always data, not behavior); has someone already analyzed this metric.
4. **Seasonality:** compare year over year (YoY) — if the drop repeats in the same period every year, it is seasonality; week over week (WoW) — for weekdays/weekends; check against the forecast — a strong deviation of actuals from the baseline is a reason to dig ([[M-forecasting-product]]).
5. **Decomposition (metric tree):** break the target metric into components and find the branch that fell the most (revenue = purchases × order value; purchases = users × conversion × frequency). The tree may be partly multiplicative, partly additive — the point is that it localizes the problem.
6. **Segmentation and cohorts:** segmentation — groups by characteristics (category, city, source, platform) — finds a local problem ("drops only on iOS"); cohorts — groups by arrival time — show that the new cohort behaves worse than older ones. A retention heatmap with a diagonal reveals seasonal cohorts.
7. **Presentation:** at the top — conclusion and recommendation, below — the numbers and cuts; not a "waterfall of screenshots".

### Product problem-solving cycle (case approach)
An iterative cycle (an analog of the double diamond): **problem → problem validation → hypotheses → hypothesis validation → solutions → solution verification → a new iteration.**
1. **Sources of problems:** data analysis (anomalies, funnel drop-off points), UX research (interviews, usability), feedback (reviews, support), market benchmarks, working with the team/dogfooding. The mistake is relying on a noisy, non-representative subset of users.
2. **Problem validation:** data on magnitude (% affected, losses in money), quantitative checks (surveys, A/B of mockups). Prioritization: frequency × user pain × business impact.
3. **Hypotheses about the cause:** the "5 whys" method, correlations by dates/segments, qualitative research, discussion with the team. The hypothesis is concrete and testable ("new users don't complete payment because they don't see the plan's benefits", not "they dislike the product"). Types: external (competitors, season, macro — not directly controllable) and internal (UX, bugs, segments).
4. **Hypothesis validation** before building the solution: data slices, UX tests with numbers ("30% can't find the button"), analysis of support tickets, A/B of mockups. The match "hypothesis ↔ verification method" is fixed in advance.
5. **Solutions:** generation (brainstorm, analogs, inversion), types (product/process/communication), quick checks of potential before launch: fake door, prototype, pilot on part of the audience.
6. **Solution verification:** comparison with the expectation fixed before launch; quantification of the effect (metric, magnitude, period); monitoring counter-metrics. Then — Scale/Iterate/Drop and recording the insight in the knowledge base.
Anti-fails: a decision without validating the problem/hypothesis; costs higher than the effect; a chain of reasoning not carried to the end; a solution impossible to test; non-representative feedback; fear of quick MVPs and fake doors; constraints and risks not fixed.

## Procedure
1. Write down the goal and the stage; choose **one target metric** (output), 1–3 drivers (input), 2–3 counter-metrics.
2. For each, compose a metric passport (formula, units, period, window, source, owner) and run the 6-point fitness check.
3. Build the funnel (from the CJM), compute step and end-to-end conversions, find the biggest loss, estimate it in money, slice by segments and cohorts.
4. If a retention estimate is needed — define an unambiguous zero point and target action, build cohorts at least by source and period.
5. Build the metric tree from the monetary/NSM goal down to controllable drivers; remove nodes without an owner and a link.
6. For the initiative write down: **expected change** (metric, magnitude, units), baseline (value, period), comparison (control/before-after/cohort), **observation period**, success and failure criteria, counter-metrics with thresholds, expected side effects. Statuses: fact / hypothesis / forecast ([[M-solution-design]], [[M-mvp-pilots]]).
7. Before the conclusion run the **units and periods check**: p.p. vs %, step-level vs end-to-end, actives vs payers vs new users, day vs week vs month, revenue vs margin, currency, seasonality, cohort age, identical windows for numerator and denominator.
8. Fix the formula, the owner and the revision date.

## Template / checklist
```
Metric: ___  Type: input|output|counter   Formula: numerator ___ / denominator ___   Units: ___
Period and window: ___ (cohort: ___)   Source/event: ___   Owner: ___   Lever: ___
Baseline: ___ (period ___)   Target: ___ by ___   Threshold 🟡/🔴: ___
Link to goal (tree): ___   Counter-metrics and thresholds: ___   Data status: fact|hypothesis|forecast
```
Conclusion checklist: p.p. and % not mixed · identical periods and cohorts · numerator and denominator from one system · segment specified · seasonality accounted for · the effect is not a consequence of a promo/subsidy · significance/sample size stated · counter-metrics did not deteriorate.

## Common mistakes
- A metric "for a pretty chart" not tied to the business goal; dozens of metrics without hierarchy.
- No passport: teams compute differently; events were renamed — the funnel "reset to zero".
- Hospital-wide average instead of cohorts/segments; overall CAC without channels.
- Comparing ARPU and retention of different periods; dividing revenue by users of another period.
- Counting success by growth of the numerator while the denominator of quality falls (GMV grows, retention falls).
- Changing the zero point or the window mid-test; a "sliding range".
- Not defining the counter-metric and threshold in advance; showing an honest chart only if it looks nice.
- Accepting a correlation (in a tree arrow) as causality without verification.

## Questions that can change the decision
- How exactly is the metric defined in this project's data (event, window, deduplication), and do all teams count it the same way?
- Which period and which cohort underlie the number? Is there seasonality/a promo?
- Which driver metric is actually controllable by the team, and which belongs to someone else's zone?
- Which counter-metrics and thresholds are needed so growth is not bought at the cost of loyalty or economics?
- Is the data sufficient (sample size, length of history) for a conclusion about significance?

## Related cards
[[M-success-metrics]], [[M-loyalty-metrics]], [[M-unit-economics]], [[M-traction-model]], [[M-quant-methods]], [[M-cjm]], [[M-mvp-pilots]], [[M-pmf-scaling]], [[M-solution-design]], [[M-product-context]], [[M-goals-drivers-bets]], [[M-ab-testing]], [[M-basic-statistics-pm]], [[M-sql-for-pm]], [[M-dashboards-visualization]], [[M-forecasting-product]]
