---
id: M-solution-design
lang: en
title: Solution design — solution hypotheses, scoring, risks, validation and post-mortem
course: pm
sources: ["EN mirror of the RU methodology card M-solution-design (knowledge/methods/solution-design.md); original sources are listed in the RU card"]
stages: [options, validation, after-decision]
tags: [solution-hypothesis, rice, solution-risks, fake-door, ab-test, counter-metrics, pivot, kill]
related: [M-problem-design, M-mvp-pilots, M-roadmap, M-risks, M-usability-testing, M-quant-methods, M-product-metrics, M-usp, M-decision-daci]
---

# Solution design: generation and validation

## When to apply
The problem is already formulated and prioritized ([[M-problem-design]]); solution options must be proposed, the best one chosen, and the test planned so that the "confirmed / refuted" verdict is unambiguous and fixed in advance.

## Essence
- **A solution hypothesis** — an assumption that a specific action (feature, service, change) will improve the user experience and lead to a business result. We do not know in advance whether it will work, so we test it.
- Formula: `If [we do ___], then [users will be able to ___], which will lead to [a business result]` (with a metric and an effect size). Example: a chatbot for order status → users resolve the issue without a seller/support (y% of tickets) → a faster answer → we close the information gap → conversion to order +x%.
- **Checklist of a good hypothesis (7 points):** an explicit link to the user problem · specific ("support response time from 2 min to 30 sec", not "improve the service") · contains an assumption about the impact on user experience · the expected business effect stated as a metric · testable (one can measure "confirmed/refuted") · contains success criteria (a guideline: +10% clicks, −5% churn) · focused (one idea = one hypothesis).
- **Generation:** benchmarking/competitive analysis; brainstorming with cross-functional colleagues (sales, marketing, support, engineering); customer co-design. Usually combined. If the problem is concrete and the solution lies on the surface (no Apple Pay for iOS users) — do not spend resources on "originality".
- **Prioritization:** ICE = I×C×E; RICE = (Reach × Impact × Confidence) / Effort. Example for the problem "sellers are not trusted": money-back guarantee 4×4×5/4 = 20; seller reviews 3×4×3/3 = 12; a "trusted seller" badge 2×3×3/2 = 9.
- **Where to take assumptions for scoring:** funnel/retention analytics and the share of users with the problem; qualitative and quantitative research; sales/support (number of tickets); benchmarks of competitors and adjacent markets; results of past experiments; the team's expert estimates (engineering cost, UX complexity). Confidence: analytics data — high, user research — medium, the team's guess — low.
- **Solution risks** (assess before choosing; a plan B for every critical one):
  - Value — the user does not need it (push notifications about new listings get disabled as spam).
  - Usability — users cannot operate it (complex filters tank conversion).
  - Feasibility — hard/expensive to build and maintain (AI photo recognition requires servers and experts).
  - Business viability — it does not pay off, harms the model (free delivery raised sales but losses grew).
  - Legal/reputation — paid reviews: slander, loss of trust.
- **What we test:** value (Value), usability (Usability), business effect (Viability), impact on counter-metrics.

| What we test | Methods |
|---|---|
| Value | Qualitative interviews with a prototype ("would you pay?"), landing page/fake door (a button with no implementation, counting clicks), survey/NPS/conjoint |
| Usability | A prototype in Figma, a usability test (task: "find housing near the metro"), A/B with funnel and CES |
| Business effect | A/B test (control vs experiment), cohort analysis (LTV, ARPU, retention of the feature group) |
| Counter-metrics | An A/B test with monitoring of adjacent products/metrics (revenue of other promo tools, NPS, SLA) |

## Procedure
1. Take the priority problem with a baseline and a segment. Generate 3–7 solution hypotheses with at least two methods (benchmark + brainstorm).
2. Write each one in the "If… then… which leads to…" formula and run the 7-point checklist; split glued ideas apart.
3. Score with RICE/ICE; attach a source and a confidence type to every score. Add a risks column (Value/Usability/Feasibility/Business/Legal) and a plan B for the critical ones.
4. Choose 1–2 hypotheses to test; determine **what exactly is unknown** (value, usability, effect, counter-metrics) and take the cheapest method that removes precisely that uncertainty. The chain by rising cost: interviews/fake door → prototype/usability → A/B → pilot ([[M-mvp-pilots]]).
5. **Before launch** fix the test plan (template below): audience, channel, materials, period, success/failure criteria, counter-metrics with thresholds, what we do at each outcome.
6. Run the test; compare facts against the criteria; record insights (confirmed / not / unexpected).
7. **Post-mortem and decision (pivot / persevere / kill):** (1) collect facts — target and guardrail metrics against the criterion; (2) review assumptions, which proved wrong; (3) root cause ("5 whys"); (4) classify risks; (5) make the decision; (6) update the backlog, RICE scores and the wiki. Formats: a 30-minute light retro right after the A/B; a 2–3 h deep review; quarterly learnings.

Sample report: goal +10% conversion to promotion; actual +4%, p = 0.12 (insignificant); the Reach assumption failed (8% instead of 20%); cause — the banner is visible only in "My listings", 60% of sellers go straight to chat; decision — pivot: move the banner into chat and repeat the A/B; plan B — stop the rollout if LTV of adjacent promos falls by more than 5%.

## Template / checklist
**Solution test card (experimental):**
```
Hypothesis: If ___, then ___, which will lead to ___ (metric, magnitude).
What we test: value | usability | business effect | counter-metrics
Method: ___   Audience/segment and acquisition channel: ___
Baseline (value, period, source): ___   Comparison/control group: ___
Expected change (target metric): ___   Minimum significant effect / sample size: ___
Observation period: ___ (we end by data volume, not by date)
Success criterion (fixed before the start): ___   Failure / kill criterion: ___
Counter-metrics and thresholds (guardrails): ___   Side effects we watch for: ___
Decision by outcome: success → ___ ; partial → ___ ; failure → ___
Risks (Value/Usability/Feasibility/Business/Legal) and plan B: ___
```
**A filled example (sellers do not know their position in search):** hypothesis — show the listing's average position → the promotion decision becomes more conscious → conversion to subscribing to promotion +10%. Verify: it solves the need; it is understandable; it helps decide about promotion; it moves the target metric; users are satisfied; counter-metrics do not fall. Methods: a UX test of mockups; an A/B on the target metric, satisfaction and counter-metrics. Criteria: CES "it is easy for me to determine my position" > 80%; conversion to subscribing +10% in the test group; revenue of other promo tools does not fall.

## Common mistakes
- A hypothesis without a metric and effect size ("we will improve the experience"); several ideas inside one hypothesis.
- RICE scores without sources; Impact "by eye" (+5 p.p. of NPS turned out to be +1.5).
- Success criteria formulated after the test or "adjusted" along the way.
- No counter-metrics: the target metric grew while NPS/SLA/revenue of adjacent products fell.
- Choosing the most expensive method (development + A/B) for a question a fake door or an interview would answer.
- A result of "+4%, insignificant" treated as success or as "let's wait another month" without a pre-set plan.
- A post-mortem as blame-seeking or "the numbers are fine, let's move on" without updating assumptions.
- Launching without approvals (legal, security) and without an analytics event: the effect becomes unmeasurable afterwards.

## Questions that can change the decision
- Which uncertainty is the main one — value, usability, economics, or technical feasibility?
- Is there enough traffic/segment for a statistically significant test within an acceptable time?
- What counts as failure, and at which outcome do we kill the idea rather than refine it?
- Which adjacent metrics and teams can the solution affect (cannibalization, support load)?
- Are there legal/reputational constraints that make a pilot impossible?

## Related cards
[[M-problem-design]], [[M-mvp-pilots]], [[M-roadmap]], [[M-risks]], [[M-usability-testing]], [[M-quant-methods]], [[M-product-metrics]], [[M-usp]], [[M-decision-daci]]
