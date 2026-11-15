---
id: M-pmf-scaling
lang: en
title: Scaling and Product-Market Fit — when to grow, how to measure PMF (the Superhuman engine)
course: pm
sources: ["EN mirror of the RU methodology card M-pmf-scaling (knowledge/methods/pmf-scaling.md); original sources are listed in the RU card"]
stages: [validation, strategy, after-decision]
tags: [pmf, scaling, unit-economics, retention, nps, superhuman, 40-percent-survey, traffic-light, premature-growth]
related: [M-traction-model, M-unit-economics, M-loyalty-metrics, M-product-metrics, M-mvp-pilots, M-jtbd, M-roadmap, M-risks, M-product-context, M-product-communication, M-strategy-growth, M-monetization]
---

# Scaling and PMF

## When to apply
The question "is it time to scale / invest in marketing / enter a new segment or region" and "does the product have PMF, how strong is it, and how to strengthen it". The outcome is a verifiable go / wait / fix decision with thresholds, an observation period, and stop conditions.

## Essence

### Scaling
- **Scaling** — growing the volume of the business (clients, operations) without a proportional growth in expenses; measured by revenue growth, users, and infrastructure resilience. Strategy types: geographic expansion (new markets), entering new segments (new user types, addressing new pains), platform models/ecosystems.
- **Start conditions (in descending order of importance):**
  1. **PMF achieved** — understanding of needs, confirmed by metrics and continuous feedback.
  2. **Confirmed demand and positive dynamics for ≥ 2 quarters** across qualitative and quantitative data (the "two-quarter rule").
  3. **Unit economics** — LTV and CAC calculated, a clear path to profitability ([[M-unit-economics]]).
  4. **Team and infrastructure readiness** — scalable architecture, a hiring plan, specialist availability on the market.
- **Threshold benchmarks from lecture notes** (not universal — validate on product data): LTV/CAC ≥ 3; payback/BEP ≤ 9–18 months (different notes say 9 and 18 months); high and stable NPS/CSAT (the notes use NPS ≥ 70 for two quarters as a "bell" that PMF is near); ~80% of key vacancies closed; no deteriorating trend for 2 quarters. If a threshold is not confirmed by project data — write "benchmark, not fact".
- **The scaling plan (4 directions):** channels (integrations, partnerships, social media); marketing (budget, diversification, personalization); technical (scalable architecture, cloud, automation); people (hiring, culture). What changes is not "more of the same" but the whole system.
- **Scaling metrics:** CAC, LTV, Retention Rate, ROMI, NPS/CSAT, Contact Rate (the share of support requests), the share of paying users. Pick 2–3 as "stop signals" and monitor the rest.
- **Signs of premature/failed scaling:** (1) no growth in sales/users; (2) CAC rises above LTV or is unstable; (3) metrics deteriorate (retention falls, churn grows); (4) organizational failure (the team cannot handle the volume). Lecturer's note: one yellow signal is still treatable, two in a row are red.
- **Typical mistakes:** launching without confirmed PMF; underestimating marketing and support costs.
- **Exceptions (scaling without PMF):** innovation/early market and a "window of opportunity" — acceptable only with a financial cushion and reinforced control of CAC, NPS, and unit economics.
- **False PMF:** (a) subsidized growth (sales grow only on bonuses/cashback); (b) falling retention/NPS hidden behind aggregate GMV ("revenue ↑, transactions per user ↓"). Countermeasures: share of paying users, Contact Rate, LTV/CAC, cohorts.
- **"Traffic lights":** for each metric — a 🟢/🟡/🔴 threshold, an owner, and a pre-agreed action. Examples from the notes: CAC/LTV rising for 3 months → review the offer and targeting; retention D30 below the segment threshold → stop paid traffic, strengthen onboarding; NPS −5 pp in a quarter → reinforce support. On red: freeze expansion, root cause within 48 h, a recovery plan (metric, owner, deadline), a re-check before continuing.
- **PMF signals (6 groups from session 10):** feedback (reviews, NPS); market dynamics ("the market pulls the product", high sales velocity); satisfaction surveys; usage metrics (retention, DAU/MAU); financials (steady revenue growth, positive unit-economics dynamics); growth indicators (viral effect). For final PMF confirmation, quantitative data is combined with qualitative research; PMF is not forever — when the market/expectations change, the product can lose it, so constant monitoring is needed.
- **Course Gate logic:** Gate 1 — the pain is confirmed (Problem fit); Gate 2 — the solution removes the pain (Solution fit, MLP, TDR, feature readiness OK); Gate 3 — sustainable growth and economics (Traction fit, PMF achieved, a scaling plan ready); Gate 4 — goals achieved (the product becomes part of the business / pivot / shutdown); at the scaling stage — quarterly deep dives on tracking against the traction plan. See [[M-product-communication]].
- **Scaling artifacts (the "10×10" from the session 10 notes):** the scale-hypothesis statement (a design doc) · PMF evidence (an evidence table: NPS, stable retention) · the Gate decision protocol for "go to scale" · a 12-month roadmap · channel/marketing/technology/people plans · quarterly OKRs · a metric traffic light (CAC, LTV, NPS) with alerts · a risk register (probability × impact, owner, SLA) · a financial balcony (an at-a-glance financial view: LTV/CAC, BEP, CAPEX, base/pess/opt scenarios) · post-mortems and a knowledge base. Checks before each wave: two quarters of green metrics; the traffic light green; every High×High risk has a mitigator and a "red button"; BEP ≤ threshold and LTV/CAC ≥ 3; roadmap dependencies intact (a tech feature never precedes its channel); ~80% of offers signed; load test and the predictive Contact Rate model passed; legal/compliance checklist green; documents accessible without access requests. Start with the first four artifacts (hypothesis, PMF evidence, Gate protocol, roadmap), each with an owner.

### Measuring PMF: the Superhuman engine
The idea: PMF can be **measured and optimized**, not only recognized by lagging signs (customer waiting lists, growth, press coverage).
- **The leading indicator (Sean Ellis):** the share of users who would be "very disappointed" if they could no longer use the product. The empirical threshold is **40%**; below it, growth usually does not happen. Example: a survey of 731 Slack users — 51% "very disappointed".
- **The 4-question survey:** (1) how would you feel if you could no longer use it: very / somewhat disappointed / not disappointed; (2) which people, in your view, benefit the most; (3) the main benefit for you; (4) how can we improve the product for you.
- **The sample:** users who recently experienced the core value (in the source — at least two uses within two weeks); ~40 respondents is enough (100–200 in the case); survey each person once; repeat on new cohorts.
- **The steps of the engine:**
  1. **Segment** the "very disappointed" respondents by persona/type of work and narrow the market to the segments where PMF is strongest; this often reveals non-obvious segments. Build the "ideal target customer" profile (HXC — the most discerning and most helpful customer, who helps spread the product) from the answers to question 2, using the respondents' own words. Recomputing PMF on this subset raised the score by roughly 10 pp in the case (22% → 33%).
  2. **Analyze the feedback:** what the "very disappointed" love (question 3: themes such as speed, focus, keyboard shortcuts); **ignore** the feedback of those who are "not disappointed" (requests for distracting features, unsuitable use cases). Split the "somewhat disappointed" group with a filter on the main source of value: ignore those for whom it does not matter; study closely those for whom it does — they are held back by a concrete barrier (in the case: no mobile app, then calendar, integrations, attachments, a unified inbox, search, read receipts).
  3. **Split the roadmap in half:** ~50% — strengthening what users love (more speed, shortcuts, automation, design detail); ~50% — removing the barriers for the "somewhat disappointed". Strengthening only → PMF does not grow; removing barriers only → competitors overtake. Prioritization: cost (cheap/moderate/expensive) × impact (weak/medium/strong); for barriers, impact is estimated by the number of requests; start with the "low-hanging fruit".
  4. **Repeat** on new cohorts and make the share of "very disappointed" the key metric (weekly/monthly/quarterly; an OKR with a single KR). The case's trajectory: 22% (start) → 33% (after segmentation) → 58% over three quarters; NPS grew at the pace of the PMF metric.
- **Caveats:** as you move beyond early adopters the PMF score can fall (users are more demanding) — rebuild the roadmap quarterly; with strong network effects value grows with scale; narrowing to a narrow segment that badly needs the product beats being "slightly useful to many". The survey measures the reaction to the product but does not replace behavioral metrics (retention, economics).

## Procedure
1. Confirm the stage (MVP/Growth) and the goal of the decision: grow now or strengthen the core ([[M-product-context]]).
2. Assemble the **PMF signal complex**: (a) a "very disappointed" survey ≥ 40% on a suitable sample (≥ ~40 responses; state the period and cohort); (b) retention D30 or a proxy (for infrequent purchases — a proxy such as the share of active listings) is stable; (c) NPS/CSAT; (d) the market "pulls" (organic, feature requests); (e) finances: revenue grows faster than costs, positive unit-economics dynamics. Do not make the decision on a single signal.
3. Check for **false PMF**: share of organic, subsidies/promotions, retention by cohort, GMV per user.
4. Check stability: the metrics hold for ≥ 2 quarters; seasonality accounted for.
5. If the threshold is not met — run the Superhuman engine (segments → loves/barriers → a 50/50 roadmap → re-measure) instead of scaling; fix a target value and the date of the next measurement.
6. If PMF is confirmed — draft the scaling plan across the 4 directions and a 12-month roadmap ([[M-roadmap]]); test the Gate questions: how will LTV/CAC change if the budget doubles? will the infrastructure survive the peak? who will serve the flow? will NPS/retention hold at base-segment levels? If two questions have no confident answer — postpone.
7. Set the traffic light: metrics, thresholds, owner, action on red, a "red button" (a feature flag / marketing freeze). Schedule a re-check of the conditions.

## Template / checklist
```
Decision: scale | wait | strengthen PMF.   Observation period: ___ quarters
PMF complex: % "very disappointed" = ___ (n=___, cohort ___) | Retention Dxx = ___ | NPS = ___ | organic = ___% | unit economics: LTV/CAC = ___, payback = ___ months
False PMF ruled out? (subsidies | GMV masks retention | segment)
Readiness: architecture | hiring | support | legal
Traffic light: metric → threshold 🟡/🔴 → owner → action
Stop criterion (kill / freeze): ___   What is NOT confirmed: ___
```
The "PMF proven" checklist (from the notes): high NPS/CSAT for 2 quarters · retention or a proxy stable · LTV/CAC and payback in range · Contact Rate not growing · revenue grows faster than costs · tech debt does not block shipping fixes. With fewer than ~5 items met — continue Customer Development.

## Typical mistakes
- Scaling on GMV/traffic growth without looking at retention and cohorts; "flooding the market with money" without PMF.
- Treating 22–39% "very disappointed" as sufficient PMF and accelerating; conversely, not segmenting and ignoring that the score is already higher in a narrow segment.
- Listening to the feedback of the "not disappointed" and spending the roadmap on distracting features.
- Only strengthening what is loved or only fixing barriers (a 100/0 skew instead of ~50/50).
- Underestimating CAC, support costs, infrastructure; computing CAC once a month and without segments.
- Applying the benchmarks (LTV/CAC ≥ 3, NPS ≥ 70) without checking whether they fit the industry and the model.
- Surveying users who have not experienced the core value, or surveying the same people several times.

## Questions that could change the decision
- What is the share of "very disappointed" in the target segment versus the whole base? Is it not averaged away?
- Do the metrics hold for ≥ 2 quarters, and is there seasonality/promotions that explain the growth?
- How will CAC behave if the budget doubles, and what happens to paid-traffic retention versus organic?
- Can the team, support, and architecture withstand double the load?
- Are we in an innovation niche with a "window of opportunity" (the exception) — is there a cushion and reinforced control?

## Related maps
[[M-traction-model]], [[M-unit-economics]], [[M-loyalty-metrics]], [[M-product-metrics]], [[M-mvp-pilots]], [[M-jtbd]], [[M-roadmap]], [[M-risks]], [[M-product-context]], [[M-product-communication]], [[M-strategy-growth]], [[M-monetization]]
