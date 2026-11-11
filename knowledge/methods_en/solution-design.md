---
id: M-solution-design
lang: en
title: Solution design — solution hypotheses, scoring, risks, validation and post-mortem
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [options, validation, after-decision]
tags: [solution-hypothesis, rice, solution-risks, fake-door, ab-test, counter-metrics, pivot, kill]
related: [M-problem-design, M-mvp-pilots, M-roadmap, M-risks, M-usability-testing, M-quant-methods, M-product-metrics, M-usp, M-decision-daci]
---

# Solution design: generation and validation

## When to apply
The problem is already formulated and prioritized ([[M-problem-design]]); you need to propose solution options, pick the best one, and plan the check so that the verdict "confirmed / refuted" is unambiguous and fixed in advance.

## Core idea
- **A solution hypothesis** — an assumption that a specific action (a feature, a service, a change) will improve the user experience and lead to a business result. We don't know in advance whether it will work, which is why we test it.
- Formula: `If [we make ___], then [users will be able to ___], which leads to [a business result]` (with a metric and an effect magnitude). Example: an order-status chatbot → users resolve their issue without the seller/support (y% of tickets) → a faster answer → the information gap is closed → purchase conversion +x%.
- **Checklist of a good hypothesis (7 points):** an explicit link to the user problem · concrete ("support response time from 2 min to 30 sec", not "we'll improve the service") · contains an assumption about the impact on the user experience · the expected business effect is stated as a metric · testable ("confirmed/refuted" can be measured) · contains success criteria (guideline: +10% clicks, −5% churn) · focused (one idea = one hypothesis).
- **Generation:** benchmarking/competitive analysis; a brainstorm with cross-functional colleagues (sales, marketing, support, engineering); customer co-design. Usually these are combined. If the problem is concrete and the solution is on the surface (iOS users have no Apple Pay) — don't spend resources on "originality".
- **Prioritization:** ICE = I×C×E; RICE = (Reach × Impact × Confidence) / Effort. Example for the problem "sellers are not trusted": a money-back guarantee 4×4×5/4 = 20; seller reviews 3×4×3/3 = 12; a "reliable seller" badge 2×3×3/2 = 9.
- **Where to take assumptions for the scoring:** funnel/retention analytics and the share of users with the problem; qualitative and quantitative research; sales/support (the number of tickets); benchmarks of competitors and adjacent markets; results of past experiments; the team's expert estimates (engineering cost, UX complexity). Confidence levels: analytics data — high, user research — medium, a team guess — low.
- **Solution risks** (assess before choosing; a plan B for every critical one):
  - Value — the user doesn't need it (push notifications about new listings get disabled as spam).
  - Usability — they won't be able to use it (complex filters crash conversion).
  - Feasibility — hard/expensive to build and maintain (AI photo recognition requires servers and experts).
  - Business viability — it doesn't pay off, harms the model (free delivery raised sales but losses grew).
  - Legal/reputation — paid reviews: defamation, loss of trust.
- **What we test:** value, usability, the business effect (viability), the impact on counter-metrics.

| What we test | Methods |
|---|---|
| Value | Qualitative interviews with a prototype ("would you pay?"), a landing page/fake door (a button with no implementation behind it, counting clicks), a survey/NPS/conjoint |
| Usability | A Figma prototype, a usability test (task: "find housing near a metro station"), an A/B with a funnel and CES |
| Business effect | An A/B test (control vs experiment), cohort analysis (LTV, ARPU, retention for the group with the feature) |
| Counter-metrics | An A/B test with monitoring of adjacent products/metrics (revenue of other promo tools, NPS, SLA) |

## Procedure
1. Take the prioritized problem with a baseline and a segment. Generate 3–7 solution hypotheses using at least two methods (benchmark + brainstorm).
2. Write each one in the "If… then… which leads to…" formula and run it through the 7-point checklist; split ideas that are glued together.
3. Score RICE/ICE; attach a source and a confidence type to every score. Add a risk column (Value/Usability/Feasibility/Business/Legal) and a plan B for the critical ones.
4. Pick 1–2 hypotheses to test; determine **what exactly is unknown** (value, usability, effect, counter-metrics) and take the cheapest method that removes exactly that uncertainty. The cost ladder: interviews/fake door → prototype/usability → A/B → pilot ([[M-mvp-pilots]]).
5. **Before launch**, fix the validation plan (template below): audience, channel, materials, period, success/failure criteria, counter-metrics with thresholds, what we do for each outcome.
6. Run the check; compare the facts with the criteria; record insights (confirmed / not confirmed / unexpected).
7. **Post-mortem and decision (pivot / persevere / kill):** (1) collect the facts — target and guardrail metrics against the criterion; (2) check the assumptions — which turned out wrong; (3) root cause ("5 whys"); (4) classify the risks; (5) make the decision; (6) update the backlog, the RICE scores and the wiki. Formats: a 30-min light retro right after the A/B; a 2–3h deep dive; quarterly learnings.

An example report: goal +10% conversion to promotion; fact +4%, p = 0.12 (not significant); the Reach assumption failed (8% instead of 20%); cause — the banner is visible only in "My listings", 60% of sellers go straight to chat; decision — pivot: move the banner into chat and rerun the A/B; plan B — stop the rollout if the LTV of adjacent promos falls more than 5%.

## Template / checklist
**Solution validation card (experimental):**
```
Hypothesis: If ___, then ___, which leads to ___ (metric, magnitude).
What we test: value | usability | business effect | counter-metrics
Method: ___   Audience/segment and acquisition channel: ___
Baseline (value, period, source): ___   Comparison/control group: ___
Expected change (target metric): ___   Minimum detectable effect / sample size: ___
Observation window: ___ (we end by data volume, not by date)
Success criterion (fixed before launch): ___   Failure/kill criterion: ___
Counter-metrics and thresholds (guardrails): ___   Side effects we watch for: ___
Decision per outcome: success → ___ ; partial → ___ ; failure → ___
Risks (Value/Usability/Feasibility/Business/Legal) and plan B: ___
```
**An example of a filled card (sellers don't know their position in search):** hypothesis — show the average position of a listing → more informed decisions about promotion → conversion to promotion activation +10%. Test that it: addresses the need; is understandable; helps decide about promotion; moves the target metric; users are satisfied; counter-metrics don't fall. Methods: a UX test of mockups; an A/B on the target metric, satisfaction and counter-metrics. Criteria: CES "it's easy for me to determine my position" > 80%; conversion to activation +10% in the test group; the revenue of other promo tools doesn't fall.

## Typical mistakes
- A hypothesis without a metric and an effect magnitude ("we'll improve the experience"); several ideas in one hypothesis.
- RICE scores without sources; Impact "by eye" (+5 pp of NPS turned out to be +1.5).
- Success criteria formulated after the test or "adjusted" along the way.
- No counter-metrics: the target metric grew while NPS/SLA/the revenue of adjacent products fell.
- Choosing the most expensive method (development + A/B) for a question that a fake door or interviews would answer.
- "+4%, not significant" treated as success or as "let's wait one more month" without a pre-set plan.
- A post-mortem as a search for the guilty, or "the numbers are fine, moving on" without updating assumptions.
- Launching without approvals (legal, security) and without the analytics event: the effect becomes impossible to measure later.

## Questions that can change the decision
- Which uncertainty is the main one — value, usability, economics, or technical feasibility?
- Is there enough traffic/segment for a statistically significant check within an acceptable time?
- What counts as failure, and for which outcome do we close the idea instead of iterating on it?
- Which adjacent metrics and teams can the solution affect (cannibalization, load on support)?
- Are there legal/reputational constraints that make a pilot impossible?

## Related maps
[[M-problem-design]], [[M-mvp-pilots]], [[M-roadmap]], [[M-risks]], [[M-usability-testing]], [[M-quant-methods]], [[M-product-metrics]], [[M-usp]], [[M-decision-daci]]
