---
id: M-pmf-scaling
lang: en
title: Scaling and Product-Market Fit — when to grow, how to measure PMF (the Superhuman engine)
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [validation, strategy, after-decision]
tags: [pmf, scaling, unit-economics, retention, nps, superhuman, 40-percent-survey, traffic-light, premature-scaling]
related: [M-traction-model, M-unit-economics, M-loyalty-metrics, M-product-metrics, M-mvp-pilots, M-jtbd, M-roadmap, M-risks, M-product-context, M-product-communication, M-strategy-growth, M-monetization]
---

# Scaling and PMF

## When to apply
The question "is it time to scale / invest in marketing / enter a new segment or region?" and "does the product have PMF, how strong is it, and how can it be strengthened?" The output is a verifiable go / wait / fix decision with thresholds, an observation period, and stop conditions.

## Core idea

### Scaling
- **Scaling** — growing the volume of the business (customers, operations) without a proportional growth in expenses; it is measured by revenue growth, user growth, and whether the infrastructure holds up. Strategy types: geographic expansion (new markets), entering new segments (new types of users, addressing new pains), platform models/ecosystems.
- **Start conditions (in descending order of importance):**
  1. **PMF achieved** — an understanding of the needs, confirmed by metrics and continuous feedback.
  2. **Confirmed demand and positive dynamics for ≥ 2 quarters** based on qualitative and quantitative data (the "two-quarter rule").
  3. **Unit economics** — LTV and CAC computed, and the path to profit is clear ([[M-unit-economics]]).
  4. **Team and infrastructure readiness** — scalable architecture, a hiring plan, availability of specialists on the market.
- **Guideline thresholds from the lecture notes** (not universal — validate on the product's own data): LTV/CAC ≥ 3; payback/BEP ≤ 9–18 months (different notes give 9 and 18 months); NPS/CSAT high and stable (in the notes, NPS ≥ 70 for two quarters is the "bell" that PMF is close); ~80% of key vacancies closed; no worsening trend for 2 quarters. If a threshold is not confirmed by the project's data — write "a guideline, not a fact".
- **Scaling plan (4 directions):** channels (integrations, partnerships, social media); marketing (budget, diversification, personalization); technical (scalable architecture, cloud, automation); people (hiring, culture). What changes is not "more of the same" but the system as a whole.
- **Scaling metrics:** CAC, LTV, retention rate, ROMI, NPS/CSAT, Contact Rate (the share of support tickets), the share of paying users. Choose 2–3 as "stop signals" and monitor the rest.
- **Signs of premature/unsuccessful scaling:** (1) no growth in sales/users; (2) CAC rises above LTV or is unstable; (3) metrics worsen (retention falls, churn grows); (4) organizational breakdown (the team cannot handle the volume). Lecturer's note: one yellow signal can still be treated; two in a row is red.
- **Typical mistakes:** launching without confirmed PMF; underestimating marketing and support costs.
- **Exceptions (scaling without PMF):** innovation/early market and a "window of opportunity" — allowed only with a financial cushion and reinforced control of CAC, NPS, and unit economics.
- **Fake PMF:** (a) subsidized growth (sales grow only on bonuses/cashback); (b) falling retention/NPS hidden behind total GMV ("revenue ↑, deals per user ↓"). Countermeasures: the share of paying users, Contact Rate, LTV/CAC, cohorts.
- **"Traffic light":** for each metric — a 🟢/🟡/🔴 threshold, an owner, and a pre-agreed action. Examples from the notes: CAC/LTV rising for 3 months → rework the offer and targeting; retention D30 below the segment threshold → stop paid traffic, strengthen onboarding; NPS down 5 p.p. in a quarter → reinforce support. On red: freeze expansion, find the root cause within 48 hours, a recovery plan (metric, owner, deadline), and a re-check before continuing.
- **PMF signals (6 groups from session 10):** feedback (reviews, NPS); market dynamics ("the market pulls the product", high sales velocity); satisfaction surveys; usage metrics (retention, DAU/MAU); financial (stable revenue growth, positive unit-economics dynamics); growth indicators (viral effect). For final confirmation of PMF, quantitative data is combined with qualitative research; PMF is not forever — when the market or expectations change, the product can lose it, so continuous monitoring is needed.
- **Course gate logic:** Gate 1 — the pain is confirmed (Problem fit); Gate 2 — the solution relieves the pain (Solution fit, MLP, TDR, feature sign-off); Gate 3 — sustainable growth and economics (Traction fit, PMF achieved, a scaling plan is ready); Gate 4 — the goals are achieved (becomes part of the business / pivot / shutdown); at the scaling stage — quarterly deep dives on adherence to traction. See [[M-product-communication]].
- **Scaling artifacts (the "10×10" from the session 10 notes):** a scale hypothesis (design doc) · PMF evidence (an evidence table: NPS, stable retention) · a "go to scale" Gate decision protocol · a 12-month roadmap · channel/marketing/technology/people plans · quarterly OKRs · a metric traffic light (CAC, LTV, NPS) with alerts · a risk register (probability × impact, owner, SLA) · a financial balcony (LTV/CAC, BEP, CAPEX, base/pess/opt scenarios) · post-mortems and a knowledge base. Checks before each wave: two quarters of green metrics; the traffic light is green; every High×High risk has a mitigator and a "red button"; BEP ≤ threshold and LTV/CAC ≥ 3; roadmap dependencies not violated (a tech feature no earlier than its channel); ~80% of offers signed; load test and a predictive Contact Rate model passed; the legal/compliance checklist green; documents available without requesting access. Start with the first four artifacts (hypothesis, PMF evidence, Gate protocol, roadmap), each with an owner.

### Measuring PMF: the Superhuman engine
The idea: PMF can be **measured and optimized**, not only recognized by lagging signs (customer queues, growth, press coverage).
- **Leading indicator (Sean Ellis):** the share of users who would be "very disappointed" if they could no longer use the product. The empirical threshold is **40%**; below it, growth usually does not happen. Example: a survey of 731 Slack users — 51% "very disappointed".
- **A four-question survey:** (1) how would you feel if you could no longer use it: very / somewhat / not disappointed; (2) which people, in your opinion, benefit the most; (3) the main benefit for you; (4) how to improve the product for you.
- **Sample:** users who recently experienced the core value (in the source — at least two uses within two weeks); ~40 respondents is enough (in the case, 100–200); survey each person once; repeat on new cohorts.
- **Steps of the engine:**
  1. **Segment** the "very disappointed" respondents by personas/types of activity and narrow the market to the segments where PMF is stronger; this often reveals non-obvious segments. Build the profile of the "ideal target customer" (HXC — the most demanding and most useful customer, who helps spread the product) from the answers to question 2, using the respondents' own language. In the case, recomputing PMF on this subset raised the score by roughly 10 p.p. (22% → 33%).
  2. **Analyze the feedback:** what the "very disappointed" love (question 3: themes, e.g. speed, focus, keyboard shortcuts); **ignore** the feedback of those who are "not disappointed" (requests for distracting features, unsuitable use cases). Split the "somewhat disappointed" group with a filter on the main source of value: ignore those for whom it does not matter; study closely those for whom it does — a specific barrier holds them back (in the case: the lack of a mobile app, then calendar, integrations, attachments, a unified inbox, search, read receipts).
  3. **Split the roadmap in half:** ~50% — strengthening what users love (more speed, shortcuts, automation, design detail); ~50% — removing the barriers of the "somewhat disappointed". Strengthening only → PMF does not grow; barrier removal only → competitors get ahead. Prioritization: cost (cheap/moderate/expensive) × impact (weak/medium/strong); for barriers, impact is estimated by the number of requests; start with the "low-hanging fruit".
  4. **Repeat** on new cohorts and make the share of "very disappointed" users the key metric (weekly/monthly/quarterly; an OKR with a single KR). The case's dynamics: 22% (start) → 33% (after segmentation) → 58% over three quarters; NPS grew at the pace of the PMF metric.
- **Caveats:** as you move beyond early adopters the PMF score can fall (users are more demanding) — rebuild the roadmap quarterly; with strong network effects, value grows with scale; narrowing to a small segment that badly needs the product beats being "somewhat needed by many". The survey measures the reaction to the product but does not replace behavioral metrics (retention, economics).

## Procedure
1. Confirm the stage (MVP/Growth) and the goal of the decision: grow now or strengthen the core ([[M-product-context]]).
2. Assemble the **PMF signal complex**: (a) a "very disappointed" survey ≥ 40% on a suitable sample (≥ ~40 responses; state the period and cohort); (b) stable retention D30 or a proxy (for infrequent purchases — a proxy, e.g. the share of active listings); (c) NPS/CSAT; (d) the market "pulls" (organic traffic, feature requests); (e) finances: revenue growing faster than costs, positive unit-economics dynamics. Never decide on a single signal.
3. Check for **fake PMF**: the organic share, subsidies/promotions, retention by cohorts, GMV per user.
4. Check stability: the figures hold for ≥ 2 quarters; seasonality is accounted for.
5. If the threshold is not reached — run the Superhuman engine (segments → loved features/barriers → a 50/50 roadmap → re-measure) instead of scaling; fix a target value and the date of the next measurement.
6. If PMF is confirmed — build the scaling plan across the 4 directions and a 12-month roadmap ([[M-roadmap]]); test the Gate questions: how will LTV/CAC change if the budget doubles? will the infrastructure hold the peak? who will serve the flow? will NPS/retention stay at the level of the base segments? If two questions have no confident answer — postpone.
7. Set the traffic light: metrics, thresholds, an owner, an action on red, a "red button" (a feature flag / a marketing freeze). Schedule a re-check of the conditions.

## Template / checklist
```
Decision: scale | wait | strengthen PMF.   Observation period: ___ quarters
PMF complex: % "very disappointed" = ___ (n=___, cohort ___) | Retention Dxx = ___ | NPS = ___ | organic = ___% | unit economics: LTV/CAC = ___, payback = ___ months
Fake PMF ruled out? (subsidies | GMV masks retention | segment)
Readiness: architecture | hiring | support | legal
Traffic light: metric → threshold 🟡/🔴 → owner → action
Stop criterion (kill / freeze): ___   What is NOT confirmed: ___
```
The "PMF proven" checklist (from the notes): high NPS/CSAT for 2 quarters · stable retention or proxy · LTV/CAC and payback within norms · Contact Rate not growing · revenue growing faster than costs · tech debt not blocking the release of fixes. If fewer than ~5 items hold — continue Customer Development.

## Typical mistakes
- Scaling on GMV/traffic growth without looking at retention and cohorts; "flooding the market with money" without PMF.
- Treating 22–39% "very disappointed" as sufficient PMF and accelerating; conversely, failing to segment and ignoring that the score in a narrow segment is already higher.
- Listening to "not disappointed" feedback and spending the roadmap on distracting features.
- Strengthening only what is loved or only fixing barriers (a 100/0 skew instead of ~50/50).
- Underestimating CAC, support costs, and infrastructure; computing CAC once a month and without segments.
- Applying the guidelines (LTV/CAC ≥ 3, NPS ≥ 70) without checking their applicability to the industry and the model.
- Surveying users who have not experienced the core value, or the same people several times.

## Questions that can change the decision
- What is the share of "very disappointed" users in the target segment versus the whole base? Has it been averaged away?
- Do the metrics hold for ≥ 2 quarters, and is there no seasonality/promotions that would explain the growth?
- How will CAC behave when the budget doubles, and what happens to paid-traffic retention versus organic?
- Will the team, support, and architecture hold up under twice the load?
- Are we in an innovative niche with a "window of opportunity" (the exception) — is there a cushion and reinforced control?

## Related maps
[[M-traction-model]], [[M-unit-economics]], [[M-loyalty-metrics]], [[M-product-metrics]], [[M-mvp-pilots]], [[M-jtbd]], [[M-roadmap]], [[M-risks]], [[M-product-context]], [[M-product-communication]], [[M-strategy-growth]], [[M-monetization]]
