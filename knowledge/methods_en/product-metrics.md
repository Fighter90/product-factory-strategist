---
id: M-product-metrics
lang: en
title: Product metrics — types, funnels, retention and cohorts, the metric tree, NSM, counter-metrics
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [intake, research, validation, strategy, after-decision]
tags: [metrics, funnels, retention, cohorts, nsm, metric-tree, guardrails, cac, ltv, arpu]
related: [M-success-metrics, M-loyalty-metrics, M-unit-economics, M-traction-model, M-quant-methods, M-cjm, M-mvp-pilots, M-pmf-scaling, M-solution-design, M-product-context, M-goals-drivers-bets, M-ab-testing, M-basic-statistics-pm, M-sql-for-pm, M-dashboards-visualization, M-forecasting-product]
---

# Product Metrics

## When to apply
You need to choose or validate a goal metric, build a funnel and a metric tree, estimate the effect of an initiative, find the bottleneck, or formulate a success criterion and a counter-metric. Especially — when you must verify that formulas, units and periods are consistent before drawing a conclusion.

## Core idea

### What a metric is and when it is fit for use
A metric is a measurable indicator that you define yourself in order to see and change the reality of the product. You need it for: setting and tracking goals, prioritizing initiatives, justifying resources, designing tests, and making decisions about changes. **A metric is fit for use only if the answer is "yes" on every point:** it can be computed · the data exists and is logged correctly · everyone understands and computes it the same way · it reflects a specific goal · concrete actions can influence it · its dynamics can be tracked (chart, alert). The beginner's mistake is to measure "what is convenient" instead of "what matters". The life cycle of a metric: choose it → agree on the formula → get the data → compute it → visualize it → test and track it → change the goals and the metric when the goal changes.
**Metric passport:** what it measures · formula (numerator/denominator, units) · period and window · source of events · owner · lever of influence · link to the goal.

### Classifications
- Product metrics (engagement, quality, usefulness: DAU/MAU, retention D1/D7/D30, Task Success, NPS, CSAT) vs business metrics (money, growth, economics: revenue/GMV, LTV, CAC, ARPU/ARPPU, ROI, Net Profit).
- Input (controllable, leading) vs output (results, lagging); growth metrics vs product metrics.
- Segments: audience (MAU, DAU, retention); finance; quality/value (Task Success, NPS, errors); conversion/funnel (AARRR); service (CSAT, SLA, response time); product steps (feature adoption, engagement); experiments (win rate, effect).
- Frameworks: AARRR (Acquisition, Activation, Retention, Referral, Revenue — for example, an audio service: CR to install, CPA/CPC, sharing, activation by the number of tracks played or liked, subscription, D1/D7/D30), HEART (the accent on CX quality), One Metric That Matters (one metric per period), NSM (one for all the time), AIDA. A framework is adapted, not copied.

### Funnel
- **Conversion Rate (CR)** = users who moved from step A to step B / users at step A, over the stated period. The funnel is built on the CJM; every step must be understood and computed the same way by everyone.
- Rules: events in the user's language; one path to the goal = one funnel (otherwise steps get "jumped over" and the percentages distort); the funnel window equals the real cycle of the action (e-commerce — minutes to days, SaaS — a week to a month); the first version of the funnel is allowed to be imperfect — what matters is to see the drop-off quickly.
- **Reading the funnel:** (1) find the sharpest collapse; (2) why exactly there — compare with benchmarks and unit economics ("very low"), put forward and test hypotheses about the causes: high prices, slow delivery, technical errors, items out of stock, irrelevant search results; slice by segments (device, source, hour, age); (3) how much money we lose = lost users × average check × period. Example: 10,000 people × 250 ₽ = 2.5 million ₽ per day.
- **Checking the units:** step conversion ≠ through conversion. Example: search 100% → product card 70% → cart 15% → payment 5%; the step CRs are: 70/100 = 70%; 15/70 = 21.4% (CR2Cart); 5/15 = 33.3%; the through conversion to payment is 5%. You must not compare the step 21.4% and the through 15% as if they were the same kind of number; a gap in percentage points ≠ a gap in percent (62% → 15% is −47 pp and −76% in relative terms).
- A micro-funnel inside the step with the biggest loss; mistakes: non-exclusive steps, renamed events ("the funnel reset to zero"), a floating window. The cure is an "event passport" (entity, format, author, date of change). A funnel is a diagnostic tool; KPIs are phrased differently: "raise checkout CR from 15% to 25% by the end of the quarter".

### Retention, activity, cohorts
- **Retention Dn** = the share of the cohort (the users who arrived on day 0) that returned and performed the target action on day n. The zero point must be defined unambiguously (registration, first activity, e-mail confirmation) — shifting the zero point inflates retention.
- Models: classic cohort (D0-D1-D7-D30; e-commerce, fintech), N-day rolling (7-/28-day; social networks, content), product return rate ("came back and did the target action"; B2B SaaS).
- **Cohorts**: by device, traffic source, first feature/scenario, acquisition period. Average retention without cohorts hides problems. Read the plateau of the curve — the higher it is, the more loyal the audience.
- DAU/WAU/MAU; **Stickiness = DAU/MAU** (in the lecture notes: 0.2–0.3 is typical for utilities, 0.5+ for the top social networks — a guideline, it depends on usage frequency); a falling stickiness at a stable MAU means "people come in but don't live here".
- Mistakes in reading: artificial growth driven by a 90% discount (it kills unit economics); mixing seasons; comparing cohorts of different ages without aligning them.
- For rare transactions, retention is replaced with proxies (the share of active listings and the like).

### Satisfaction
- **CSAT** — a rating of a specific interaction (1–5); ask right after it. **CES** — user effort (scale 1–7), after complex/rare scenarios (returns, cancellations, chat). **NPS** — willingness to recommend, 0–10; NPS = % of promoters (9–10) − % of critics (0–6), measured periodically (once a quarter / after accumulated experience), by segments. One question per interaction. Mistakes: surveying too late, mixing scales, long questionnaires, ignoring segments (the NPS of long-standing customers is usually higher than that of new ones). The link to money: CSAT → repeat purchases/cross-selling; CES → operating costs of support; NPS → organic growth/CAC. Concrete numbers for these links come only from the product's own data.

### Money and growth (formulas with units)
| Metric | Formula | Units / period |
|---|---|---|
| ARPU | revenue of the period / active users of the period | ₽ per user per period |
| ARPPU | revenue of the period / paying users of the period | ₽ per paying user per period |
| GMV | the sum of the prices of all orders (before deducting costs) | ₽ per period |
| AOV | GMV / number of orders | ₽ per order |
| CAC | marketing spend of the period (full composition: bonuses, store commissions, referral payouts, part of payroll) / new clients of the same period | ₽ per client |
| ROAS | revenue from the campaign / spend on the campaign | dimensionless; 24 h and 7-day windows |
| ROMI | (income − marketing spend) / spend | % or a fraction |
| Payback | CAC / (marginal income per user per period) | periods (months) |
| LTV | in the simplest model ARPU × the expected number of active periods; at a constant retention r per period ≈ ARPU / (1 − r) | ₽; periods must be consistent with r |
Checks: an ARPU "per day" must not be divided by a retention "per week"; compare LTV and CAC in one currency and on a comparable margin (better marginal LTV than revenue); CAC and revenue — for one period and one cohort; separate promo revenue from organic; convert multi-currency GMV at the exchange rate of the deal date; ARPU is computed over active users and ARPPU over paying ones — do not substitute one for the other. The notes sometimes contain "CM = ARPU − CAC − Cvar": this mixes periodic income with a one-off acquisition cost — it is more correct to compare the contribution accumulated over the lifetime (LTV by margin) with CAC ([[M-unit-economics]]).
Benchmarks from the notes (verify them, do not take them as norms): CAC ≤ ~30% of LTV; 7-day ROAS ≥ 1.2; Payback ≤ 3 months for a mature business (up to 6 for a startup); paid-channel retention no lower than organic by more than ~5 pp.

### NSM and the metric tree
- **NSM** — the main metric that reflects the value for the user and is linked to revenue/LTV. Choosing it: (1) what is the core value? (2) which unit of the result can be measured? (3) does it scale, and does it affect growth? Criteria: a clear link to value; a correlation with revenue/LTV (check it on history); a sufficient frequency of change (weeks/months); several functions influence it; it is explainable in plain words. Examples: minutes of listening by a paying user; the number of successful transactions per day; deals won per month. Mistakes: changing the NSM every quarter (the rule is that it lives for about a year and changes when the strategy changes); too distant for the people doing the work (then driver-proxies are closer to the actions). Hierarchy: NSM → drivers (2–4) → operational metrics → process metrics (Lead Time, Change Failure Rate).
- **The metric tree:** it links local changes to the goal of the business. Example: GMV = number of orders × average check; orders = users × CR to purchase; average check = average number of items × average price. Rules: decompose mathematically everything that can be decomposed, and the rest by meaning; keep the levels connected; descend to the level where you can actually influence things; every "arrow" comes with an owner and a confirmed link (correlation/experiment, not an assumption).
- **Choosing the key metric:** the stage of the business → what problem the product solves for the business → what we want from the users → what we can really influence → proxy metrics for reaching the goal from several sides.

### Counter-metrics (guardrails)
Metrics that must not get worse while the target metric grows: NPS/CSAT/CES, SLA and response time, Contact Rate, returns, complaints, retention, CAC, the metrics of neighboring products (cannibalization), latency. For each one — a threshold set before the start. Example: "fast delivery" raised GMV by 6%, but CES showed a growing effort and NPS sagged by 4 pp a month later — "a short success without monitoring the effort is rolled back through retention".

### The metric trio: target → proxy → counter (levels of application)
For any task — from a yearly strategy to a single feature/A/B test — metrics are assembled into a trio:
| Role | Question | Property |
|---|---|---|
| Target | what do we count as success? | the main criterion, may change slowly |
| Proxy (1–3) | what moves earlier and predicts the target? | sensitivity + a proven correlation with the target |
| Counter (2–3) | what must we not allow? | thresholds set before the start (see the guardrails above) |
The choice starts with three questions: the goal ("what are we trying to achieve"), the driving factors ("thanks to what"), the risks ("which side effects are possible"). If the target metric is hard to measure within the period, take an earlier stage of the funnel (contacts, views) and prove the correlation with the main metric. After the experiment the decision is: **Scale** (roll it out) / **Iterate** (refine and test again) / **Drop** (abandon and record in the knowledge base).

### A good metric: sensitivity × stability × simplicity
| Criterion | Meaning | How to check |
|---|---|---|
| Sensitivity | reacts to a change in the product in days, not months | will it "catch" the effect of the test; CTR — yes, retention — no for a button |
| Stability | changes only from the product, not from external noise | a history chart without chaotic "saw teeth"; weak seasonality |
| Simplicity | the formula and the link to the goal are explainable without an analyst | a "what-if": if the metric grows by 10% — is it clear what to do? |
Balance is achieved by choosing the level of aggregation and accounting for seasonality (a moving average, ratios instead of absolutes). Before a metric enters OKR, it is "run in" on history. Bad signs: a noisy metric (enlarge the window or move to a share), an opaque composite index (split it or replace it with a component closer to the goal), manipulative ambiguity ("time on page" is read both ways — it cannot serve as a final criterion).

### A metric drop can be normal: the triage algorithm
Before "rescuing the product", go through the steps in order — the analysis may stop at any of them:
1. **Context and scale — three questions:** how much did it fall (the magnitude against the usual spread), when exactly (a link to a release/campaign/date), for whom (everyone or one segment: new users, a region, a platform). The coin analogy: 4–6 "heads" out of 10 is normal, 10 in a row is an anomaly.
2. **Volatility vs trend:** outline a "corridor of normal values" over 3–6 months of history; a deviation inside the corridor is a natural fluctuation, no analysis needed. A sharp fall over a short period → a bug/release/campaign/external event; a gradual decline over weeks → a systemic cause. Growth is checked by the same algorithm: growth can also be random or external.
3. **Verification of the data:** the most frequent cause of "drops" is technical failures. Check: did the sources recalculate in the DWH; were there collection failures (test users in production); did the calculation code of the data mart change; are there duplicate rows (doubling one day gives a "sharp spike and rollback" — almost always data, not behavior); has someone already analyzed this metric.
4. **Seasonality:** compare year over year (YoY) — if the drop repeats in the same period every year, it is seasonality; week over week (WoW) — for weekdays/weekends; check against the forecast — a strong deviation of the fact from the baseline is a reason to dig deeper ([[M-forecasting-product]]).
5. **Decomposition (the metric tree):** break the target metric into its components and find the branch that fell the most (revenue = purchases × check; purchases = users × conversion × frequency). The tree can be partly multiplicative and partly additive — the point is that it localizes the problem.
6. **Segmentation and cohorts:** segmentation — groups by characteristics (category, city, source, platform) — finds a local problem ("it falls only on iOS"); cohorts — groups by time of arrival — show that a new cohort behaves worse than the older ones. A retention heatmap with a diagonal reveals seasonal cohorts.
7. **Presentation:** on top — the conclusion and the recommendation, below — the numbers and the cuts; not a "waterfall of screenshots".

### The product problem-solving loop (the case approach)
An iterative loop (an analog of the double diamond): **problem → problem validation → hypotheses → hypothesis validation → solutions → checking the solutions → a new iteration.**
1. **Sources of problems:** data analysis (anomalies, funnel drop-off points), UX research (interviews, usability), feedback (reviews, support), market benchmarks, working with the team/dogfooding. The mistake is to rely on a noisy, unrepresentative subset of users.
2. **Problem validation:** data on the scale (% affected, losses in money), quantitative checks (surveys, A/B mockups). Prioritization: frequency × user pain × impact on the business.
3. **Hypotheses about the cause:** the "5 whys" method, correlations by dates/segments, qualitative research, discussion with the team. A hypothesis is specific and testable ("new users don't complete the payment because they don't see the benefits of the plan", not "they don't like the product"). Types: external (competitors, the season, the macro environment — not directly controllable) and internal (UX, bugs, segments).
4. **Hypothesis validation** before building a solution: slices of the data, UX tests with a number ("30% don't find the button"), analysis of support tickets, A/B mockups. The match "hypothesis ↔ validation method" is fixed in advance.
5. **Solutions:** generation (brainstorming, analogs, inversion), types (product/process/communication), quick checks of the potential before launch: a fake door, a prototype, a pilot on part of the audience.
6. **Checking the solution:** a comparison with the expectation fixed before launch; the quantification of the effect (metric, magnitude, period); the monitoring of the counter-metrics. Then — Scale/Iterate/Drop and writing the insight into the knowledge base.
Anti-fails: a decision without problem/hypothesis validation; the costs above the effect; a chain of reasoning not carried to the end; a solution that cannot be tested; unrepresentative feedback; the fear of fast MVPs and fake doors; constraints and risks not written down.

## Procedure
1. Write down the goal and the stage; choose **one target metric** (output), 1–3 drivers (input), 2–3 counter-metrics.
2. For each one, compose a metric passport (formula, units, period, window, source, owner) and run the 6-point fitness check.
3. Build the funnel (from the CJM), compute the step and through conversions, find the maximum loss, price it in money, slice it by segments and cohorts.
4. If a retention estimate is needed — set an unambiguous zero point and target action, build cohorts at least by source and period.
5. Build the metric tree from the monetary/NSM goal down to the controllable drivers; remove the nodes without an owner and a link.
6. For an initiative write down: the **expected change** (metric, magnitude, units), the baseline (value, period), the comparison (control/before-after/cohort), the **observation period**, the success and failure criteria, the counter-metrics with thresholds, the expected side effects. Statuses: fact / hypothesis / forecast ([[M-solution-design]], [[M-mvp-pilots]]).
7. Before drawing a conclusion, run the **units-and-periods check**: pp vs %, step vs through, active vs paying vs new, day vs week vs month, revenue vs margin, currency, seasonality, the ages of cohorts, matching windows in the numerator and the denominator.
8. Fix the formula, the owner and the review date.

## Template / checklist
```
Metric: ___  Type: input|output|counter   Formula: numerator ___ / denominator ___   Units: ___
Period and window: ___ (cohort: ___)   Source/event: ___   Owner: ___   Lever: ___
Baseline: ___ (period ___)   Target: ___ by ___   Threshold 🟡/🔴: ___
Link to the goal (tree): ___   Counter-metrics and thresholds: ___   Data status: fact|hypothesis|forecast
```
Conclusion checklist: pp and % are not mixed · the same periods and cohorts · numerator and denominator from one system · the segment is stated · seasonality is accounted for · the effect is not a consequence of a promo/subsidy · significance/sample size is stated · the counter-metrics have not degraded.

## Typical mistakes
- A metric "for a pretty chart", not tied to the goal of the business; dozens of metrics without a hierarchy.
- No passport: teams compute differently; the events were renamed — the funnel "reset to zero".
- The hospital average instead of cohorts/segments; an overall CAC without channels.
- Comparing the ARPU and retention of different periods; dividing revenue by the users of another period.
- Counting success by the growth of the numerator while the denominator of quality falls (GMV grows, retention falls).
- Changing the zero point or the window in the middle of a test; a "sliding range".
- Not defining the counter-metric and the threshold in advance; showing the honest chart only when it looks nice.
- Taking a correlation (in an arrow of the tree) for causality without verification.

## Questions that can change the decision
- How exactly is the metric defined in this project's data (event, window, deduplication), and does every team compute it the same way?
- Which period and which cohort underlie the number? Is there any seasonality/promo?
- Which driver metric can the team really control, and which one is someone else's zone?
- Which counter-metrics and thresholds are needed so that growth does not come at the cost of loyalty or economics?
- Is there enough data (sample size, length of history) for a conclusion about significance?

## Related maps
[[M-success-metrics]], [[M-loyalty-metrics]], [[M-unit-economics]], [[M-traction-model]], [[M-quant-methods]], [[M-cjm]], [[M-mvp-pilots]], [[M-pmf-scaling]], [[M-solution-design]], [[M-product-context]], [[M-goals-drivers-bets]], [[M-ab-testing]], [[M-basic-statistics-pm]], [[M-sql-for-pm]], [[M-dashboards-visualization]], [[M-forecasting-product]]
