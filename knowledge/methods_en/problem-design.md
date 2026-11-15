---
id: M-problem-design
lang: en
title: Problem Design — problem vs symptom, root cause, research selection, prioritization
course: pm
sources: ["EN mirror of the RU methodology card M-problem-design (knowledge/methods/problem-design.md); original sources are listed in the RU card"]
stages: [intake, research, options]
tags: [problem, symptom, root-cause, 5-whys, problem-hypothesis, rice, ice, kano, research]
related: [M-jtbd, M-research-types, M-brief-hypotheses, M-in-depth-interviews, M-interview-analysis, M-quant-methods, M-product-context, M-solution-design, M-roadmap, M-product-metrics]
---

# Problem Design

## When to apply
A leader brings a vague request ("conversion dropped", "customers complain", "we want feature X"). The method turns it into testable problem hypotheses with a root cause, a segment, and a metric, selects the way to research them, and ranks the problems so that resources go to what matters most.

## Essence
- **Problem** — an unmet user need that prevents reaching the desired outcome. It exists for the user, not for the product or the team.
- Signs of a problem: (1) belongs to the user, not the team; (2) prevents reaching the outcome; (3) systemic — repeats across many users; (4) has context (where, when, in which scenario); (5) triggers a reaction — anger, distrust, workarounds ("crutches").
- **Symptom** — the external manifestation of a hidden problem (a metric, a behavior, a complaint); it answers "what is happening" but does not explain the cause. The problem answers "why".

| Symptom (what) | Problem (why) |
|---|---|
| Conversion to order is falling | The user cannot understand how to find the right product |
| The complaint "the filter does not work" | There is no way to filter by the needed criterion |
| Refusals at pickup points are growing | The user cannot judge the real size/color/quality: too few photos and description |

- **Formulas** (use literally):
  - Problem: `[Typical user] experiences [a specific difficulty] when [action/goal], because [something blocks them]`.
  - Problem hypothesis: `We believe that [segment] has the problem [essence], because [cause/context], which leads to [a negative consequence/metric]`. Example from the lecture: 60% of professional sellers do not know their listing's position in search, because the statistics do not include this data, and cannot manage their promotion bid.
- Signal sources: **internal** ("what is happening?") — metrics/analytics, support tickets, feedback from sales/marketing/PR (especially B2B); **external** ("why?") — interviews and surveys, the market and competitors, public reviews (the users' dictionary). Real problems "seep" simultaneously from analytics, support, and the users' own words.
- Research: **qualitative** (interviews, ethnography/observation, a diary study) reveals the essence; **quantitative** (analytics, surveys) confirms the scale; the **hybrid** "analytics/support → interviews → survey" creates a grounded decision (signal → cause → ranking by importance).

| Stage | Research goal | Methods |
|---|---|---|
| Discovery / Idea | Is there a pain | In-depth interviews, ethnography, diary study |
| Problem/Solution Fit | Why it arises | Qualitative + the first surveys for a rough estimate |
| PMF | How many people suffer | Analytics, large-scale surveys, A/B |
| Scale | Growth bottlenecks | End-to-end analytics, logs, NPS |

Method choice: a new idea, unclear who hurts → interviews/observation; the symptom is already in the metrics → qualitative sessions for the cause; a list of pains exists → a survey/segment analytics for reach and priority.

## Procedure
1. **Record the symptom** with a metric, period, segment, and baseline. Without a metric it is a "complaint", not a fact; mark it as a hypothesis.
2. **Collect signals from ≥ 2 independent sources** (internal + external). One source = a hypothesis, not a conclusion.
3. **Interpret**: signal → interpretation → hypothesis (e.g., "users do not reach the CTA" → "the button is below the first screen"). The alternative is JTBD ("When I…, I want…, so that…" → what blocks it? which crutch do they use?), see [[M-jtbd]].
4. **Dig to the root cause with "5 whys"**: each answer points to a barrier in the product or behavior, until you reach a cause the product can influence. Example: 30% of returns ← the item does not match expectations ← the color/size differ from the photo ← too few photos and details ← sellers are not required to fill them in ← uploading content is slow and cumbersome. Stop at the level where there is an action and an owner; verify every link with data.
5. **Write the problem hypothesis using the formula** and add: the symptom metric (baseline), the segment, the verification signal (a specific answer/behavior), the confirmation criterion (what share of respondents / what metric shift will confirm the hypothesis).
6. **Choose the verification method** (the table above), define the sample and the deadline.
7. **Prioritize** the problems (ICE/RICE/Kano), each score with a data source (see below).
8. **Record them in the problem backlog**: segment → wording → metrics → confirmed reach → next step → owner. Hand over to [[M-roadmap]] (the problem roadmap) and [[M-solution-design]].

### Prioritization
- **ICE** = Impact × Confidence × Ease (a 1–5 or 1–10 scale). Fast, with minimal data. Example (low "buy with delivery" conversion): distrust of sellers 3×4×3 = 36; not understanding the benefits of delivery 2×3×5 = 30; fear of damage 4×3×2 = 24.
- **RICE** = (Reach × Impact × Confidence) / Effort. Example (refusal over the delivery price at the last moment): 4×3×4/3 = 16; no "free delivery" filter 2×4×3/2 = 12; not understanding the price increase 2×2×3/5 = 2.4. For decisions, Impact is often set on a 0.5–3 scale; Effort — person-weeks.
- **Kano** (a survey: "How would you feel if the problem were fixed / remained?", answers from "delighted" to "very annoyed"): must-be (critical to fix first), performance (the better, the higher the satisfaction), delighters (when there are resources), indifferent (do not spend resources), reverse (do not "fix" it — possibly a false hypothesis).
- Scoring is a ranking tool, not truth: scores are ordinal; business goals also set the priority (if the strategy trades GMV for margin, the "high commission" problem falls down the list).
- The verification rule: Impact — anchored on the baseline metric and the share affected; Reach — from analytics/survey; Confidence: analytics+support+interviews = high, interviews/survey = medium, the team's guess = low; Effort — estimated by the development team, not the PM.

## Template / checklist
```
ID | Segment | Problem hypothesis (per the formula) | Symptom: metric, baseline, period
Signal sources (≥2): ___ | Root cause ("5 whys"): ___ | Verification method + sample: ___
Confirmation criterion: ___ | Reach/Impact/Confidence/Effort (with sources): ___ → RICE = ___
Kano type: ___ | Owner: ___ | Status: hypothesis | confirmed | refuted
```
The hypothesis checklist: describes the problem, not the solution · specific and testable · tied to a metric/goal · states exactly who has the problem · has a cause ("because") · states how it will be confirmed (a metric, interviews, the sample size).

## Typical mistakes
- A solution hypothesis: "we need a fast review filter" instead of "the user cannot choose a product because the reviews are overwhelming".
- Too generic and unvalidated: "users do not like the product" (needed: they leave after the first screen because they do not understand the product's task — confirmed by interviews).
- No link to a metric: "sometimes confusion when ordering" instead of "up to 15% of paid orders are lost at the last step".
- Unclear who has it: "users do not understand how to find housing in the right district" instead of "new mobile users do not see the map entry point".
- Treating a symptom as the problem and jumping straight to solutions; stopping "5 whys" at the first answer.
- A survey instead of interviews at the "is there a pain" stage (a survey confirms scale but does not reveal causes); or interviews instead of numbers to estimate reach.
- RICE scores "by eye" without sources; Effort estimated by the product manager; tuning the scores toward the desired conclusion.
- Solving all the problems: resources are always fewer than tasks, and not every problem needs solving at all.

## Questions that could change the decision
- Is the symptom confirmed by data (period, segment, baseline), or is it isolated complaints?
- What share of the segment is really affected (Reach), and is that confirmed by a second source?
- Do users have workarounds — a signal of significance, or a sign that the problem is tolerable?
- Does the found root cause fall within the product's zone of control, or is it in someone else's perimeter?
- Does the strategic goal of the period change the priority (margin vs growth vs retention)?

## Related maps
[[M-jtbd]], [[M-research-types]], [[M-brief-hypotheses]], [[M-in-depth-interviews]], [[M-interview-analysis]], [[M-quant-methods]], [[M-product-context]], [[M-solution-design]], [[M-roadmap]], [[M-product-metrics]]
