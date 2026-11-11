---
id: M-problem-design
lang: en
title: Problem design — problem vs symptom, root cause, research choice, prioritization
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [intake, research, options]
tags: [problem, symptom, root-cause, five-whys, problem-hypothesis, rice, ice, kano, research]
related: [M-jtbd, M-research-types, M-brief-hypotheses, M-in-depth-interviews, M-interview-analysis, M-quant-methods, M-product-context, M-solution-design, M-roadmap, M-product-metrics]
---

# Problem design

## When to apply
A leader brings a vague request ("conversion dropped", "clients complain", "we want feature X"). The method turns it into testable problem hypotheses with a root cause, a segment and a metric, chooses the research approach, and ranks the problems so that resources go to the most significant ones.

## Core idea
- A **problem** is an unmet user need that prevents the desired result. It exists in the user, not in the product or the team.
- Signs of a problem: (1) it belongs to the user, not to the team; (2) it blocks a result; (3) it is systemic — it recurs for many users; (4) it has context (where, when, in which scenario); (5) it triggers a reaction — anger, distrust, workarounds ("kludges").
- A **symptom** is the external manifestation of a hidden problem (a metric, a behavior, a complaint); it answers "what is happening" but does not explain the cause. A problem answers "why".

| Symptom (what) | Problem (why) |
|---|---|
| Falling conversion to order | The user can't understand how to find the right product |
| Complaint "the filter doesn't work" | You can't filter by the criterion that matters |
| Refusals at pickup points are growing | The user can't judge the real size/color/quality: too few photos and description |

- **Formulas** (use literally):
  - Problem: `[A typical user] experiences [a specific difficulty] when [an action/goal], because [something blocks them]`.
  - Problem hypothesis: `We believe that [segment] has the problem [essence], because [cause/context], which leads to [a negative consequence/metric]`. Example from the lecture: 60% of professional sellers don't know their listing's position in search, because the statistics lack this data, and can't manage their promotion bids.
- Signal sources: **internal** ("what is happening?") — metrics/analytics, support tickets, sales/marketing/PR feedback (especially B2B); **external** ("why?") — interviews and surveys, the market and competitors, open reviews (the users' vocabulary). Real problems "leak through" from analytics, support and user words simultaneously.
- Research: **qualitative** (interviews, ethnography/observation, diary study) reveals the essence; **quantitative** (analytics, surveys) confirms the scale; the hybrid chain "analytics/support → interviews → survey" builds an evidence-based solution (signal → cause → ranking by importance).

| Stage | Research goal | Methods |
|---|---|---|
| Discovery / Idea | Is there pain | In-depth interviews, ethnography, diary study |
| Problem/Solution Fit | Why it arises | Qualitative + first surveys for a rough estimate |
| PMF | How many people suffer | Analytics, large-scale surveys, A/B |
| Scale | Growth bottlenecks | End-to-end analytics, logs, NPS |

Choosing a method: a new idea, unclear who hurts → interviews/observation; the symptom is already in the metrics → qualitative sessions for the cause; a list of pains exists → a survey/segment analytics for reach and priority.

## Procedure
1. **Fix the symptom** with a metric, a period, a segment and a baseline. If there is no metric, it's a "complaint", not a fact; mark it as a hypothesis.
2. **Collect signals from ≥ 2 independent sources** (internal + external). One source = a hypothesis, not a conclusion.
3. **Interpret**: signal → interpretation → hypothesis (e.g., "users don't reach the CTA" → "the button is below the first screen"). An alternative is JTBD ("When I…, I want…, so that…" → what blocks them? which kludge do they use?), see [[M-jtbd]].
4. **Dig to the root cause with the "5 whys" method**: each answer names a barrier in the product or behavior, until you reach a cause the product can influence. Example: 30% returns ← the item doesn't match expectations ← the color/size in the photo differ ← too few photos and details ← sellers aren't required to fill them in ← uploading content is complicated and slow. Stop at the level where there is an action and an owner; verify every link with data.
5. **Write the problem hypothesis by the formula** and add: the symptom metric (baseline), the segment, a verification signal (a specific answer/behavior), a confirmation criterion (what share of respondents / what metric shift will confirm the hypothesis).
6. **Choose the verification method** (the table above), define the sample and the timeline.
7. **Prioritize** the problems (ICE/RICE/Kano), every score with a data source (see below).
8. **Record in the problem backlog**: segment → formulation → metrics → confirmed reach → next step → owner. Hand off to [[M-roadmap]] (the problem roadmap) and [[M-solution-design]].

### Prioritization
- **ICE** = Impact × Confidence × Ease (a 1–5 or 1–10 scale). Fast, with minimal data. Example (low conversion of "buy with delivery"): distrust of sellers 3×4×3 = 36; not understanding the benefits of delivery 2×3×5 = 30; fear of damage 4×3×2 = 24.
- **RICE** = (Reach × Impact × Confidence) / Effort. Example (refusal because of the delivery price at the last moment): 4×3×4/3 = 16; no "free delivery" filter 2×4×3/2 = 12; not understanding the price increase 2×2×3/5 = 2.4. For solutions, Impact is often set on a 0.5–3 scale; Effort is in person-weeks.
- **Kano** (a survey: "How would you feel if the problem were fixed / remained?", answers from "delighted" to "very annoyed"): must-be (critical to close first), performance (the better, the higher the satisfaction), delighters (if resources allow), indifferent (don't spend resources), reverse (don't "fix" — possibly a false hypothesis).
- Scoring is a ranking tool, not the truth: the scores are ordinal; business goals also set the priority (if the strategy sacrifices GMV for margin, the "high commission" problem moves down the list).
- Verification rule: Impact — backed by the baseline metric and the share of affected users; Reach — from analytics/a survey; Confidence: analytics + support + interviews = high, interviews/a survey = medium, the team's guess = low; Effort — estimated by the development team, not the PM.

## Template / checklist
```
ID | Segment | Problem hypothesis (by the formula) | Symptom: metric, baseline, period
Signal sources (≥2): ___ | Root cause ("5 whys"): ___ | Verification method + sample: ___
Confirmation criterion: ___ | Reach/Impact/Confidence/Effort (with sources): ___ → RICE = ___
Kano type: ___ | Owner: ___ | Status: hypothesis | confirmed | refuted
```
Hypothesis checklist: describes a problem, not a solution · specific and testable · tied to a metric/goal · states exactly who has the problem · gives a cause ("because") · states what will confirm it (a metric, interviews, sample size).

## Typical mistakes
- A solution-hypothesis: "we need a fast review filter" instead of "the user can't choose a product because reviews overwhelm them".
- Too generic and unvalidated: "users don't like the product" (needed: they leave after the first screen because they don't understand the product's task — confirmed by interviews).
- No link to a metric: "sometimes confusion at checkout" instead of "up to 15% of paid orders are lost at the last step".
- Unclear who has it: "people don't understand how to find housing in the right district" instead of "new mobile users don't see the map entry".
- Taking the symptom for the problem and jumping straight to solutions; stopping "5 whys" at the first answer.
- A survey instead of interviews at the "is there pain" stage (a survey confirms the scale but doesn't reveal causes); or interviews instead of numbers to estimate reach.
- RICE scores "by eye" without sources; Effort estimated by the product side; fitting the scores to the desired conclusion.
- Trying to solve every problem: resources are always fewer than tasks, and not every problem needs solving at all.

## Questions that can change the decision
- Is the symptom confirmed by data (period, segment, baseline), or are these one-off complaints?
- What share of the segment is actually affected (Reach), and is that confirmed by a second source?
- Do users have workarounds — is that a signal of significance, or a sign that the problem is tolerable?
- Does the found root cause fall within the product's zone of control, or does it lie in someone else's perimeter?
- Does the strategic goal of the period change the priority (margin vs growth vs retention)?

## Related maps
[[M-jtbd]], [[M-research-types]], [[M-brief-hypotheses]], [[M-in-depth-interviews]], [[M-interview-analysis]], [[M-quant-methods]], [[M-product-context]], [[M-solution-design]], [[M-roadmap]], [[M-product-metrics]]
