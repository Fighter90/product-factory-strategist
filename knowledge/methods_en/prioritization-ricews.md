---
id: M-prioritization-ricews
lang: en
title: Backlog prioritization — RICE, ICE, WSJF and Kano: formulas and which method to use when
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [options, validation]
tags: [prioritization, rice, ice, wsjf, kano, backlog, cost-of-delay]
related: [M-solution-design, M-unit-economics, M-lean-canvas]
---

# Prioritization: RICE, ICE, WSJF, Kano — which to choose and how to score

## When to apply
The backlog exceeds team capacity and the disputes about order come not from data but from taste; you need to compare heterogeneous initiatives (features, experiments, debt) and explain the choice to stakeholders; before quarterly planning or when trimming the roadmap.

## Core idea
- **RICE** (Intercom): `(Reach × Impact × Confidence) ÷ Effort`. Reach — users/events per period (share of the audience × the base); Impact on the target metric: 3 massive / 2 high / 1 medium / 0.5 low / 0.25 minimal; Confidence: 100% (data is available) / 80% (partial) / 50% (intuition); Effort — person-months. Plus: comparability of heterogeneous work in a product with a measurable funnel.
- **ICE** (Sean Ellis): `Impact × Confidence × Ease`, each scale 1–10. Fast triage of growth hypotheses when data is scarce and speed matters more than accuracy.
- **WSJF** (Reinertsen / SAFe): `Cost of Delay ÷ Job Size (duration)`; CoD = value for the user/business + time criticality + risk reduction/opportunity enablement; the estimates are relative (a Fibonacci scale) within a single batch of work. Plus: the economics of delay for a queue of large initiatives and for the portfolio.
- **Kano**: a classification of the reaction to a feature, not a ranking. Pairs of questions "functional / dysfunctional" yield 5 categories: must-be (the basics — their absence is intolerable), performance (the more, the better), attractive (delighters), indifferent, reverse.
- The methods answer different questions: Kano — "what moves satisfaction", RICE/ICE/WSJF — "in what order to build".
- Practical combination: Kano — for the release scope; RICE — for the product backlog; WSJF — for the portfolio and large projects; ICE — for quick growth experiments.

## How to do it
1. Pick the method for the task: a measurable funnel → RICE; a queue of large projects → WSJF; triage of hypotheses → ICE; the release scope → Kano.
2. Fix the scales and definitions in advance (what counts as Impact=3, what goes into Effort) — otherwise the estimates are not comparable between people.
3. Have 3+ participants estimate independently and take the median; mark contested items with low Confidence (RICE) or with a coarser scale.
4. Score within a single batch: estimates from different sessions and batches are not comparable (critical for WSJF).
5. Hand-check the top of the list: strategic commitments, dependencies, tech debt and infrastructure are run on a separate track with a capacity quota.
6. After release, return to the actual Reach/Impact/durations and calibrate the scales against history.

## Pitfalls
- Precision theater: scores create the appearance of objectivity but remain expert guesses; a score is a tool for structuring the argument, not a replacement for judgment.
- RICE punishes infrastructure and tech debt: such work has no user Reach — it needs a separate capacity quota, not a place in the general ranking.
- Typical estimation errors: inflated Reach, underestimated Effort; take Effort with a buffer and check it against the team's historical velocity.
- Kano: the categories drift over time — yesterday's delighters turn into must-be; the survey needs to be refreshed, not its conclusions inherited.

## Connections
The scores feed option choice in `M-solution-design`; Cost of Delay in WSJF is the forgone cash flow from `M-unit-economics`; the place of an initiative in the business model is checked on `M-lean-canvas`.
