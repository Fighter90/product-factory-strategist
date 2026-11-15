---
id: M-prioritization-ricews
lang: en
title: Backlog Prioritization — RICE, ICE, WSJF, and Kano: formulas and when to use which method
course: strategy
sources: ["EN mirror of the RU methodology card M-prioritization-ricews (knowledge/methods/prioritization-ricews.md); original sources are listed in the RU card"]
stages: [options, validation]
tags: [prioritization, rice, ice, wsjf, kano, backlog, cost-of-delay]
related: [M-solution-design, M-unit-economics, M-lean-canvas]
---

# Prioritization: RICE, ICE, WSJF, Kano — which to choose and how to compute

## When to apply
The backlog exceeds team capacity, and arguments about order come from tastes rather than data; you need to compare heterogeneous initiatives (features, experiments, debt) and explain the choice to stakeholders; before quarterly planning or when cutting the roadmap.

## Essence
- **RICE** (Intercom): `(Reach × Impact × Confidence) ÷ Effort`. Reach — users/events per period (audience share × base); Impact on the target metric: 3 massive / 2 high / 1 medium / 0.5 low / 0.25 minimal; Confidence: 100% (data exists) / 80% (partial) / 50% (intuition); Effort — person-months. Plus: comparability of heterogeneous work in a product with a measurable funnel.
- **ICE** (Sean Ellis): `Impact × Confidence × Ease`, each scale 1–10. A quick triage of growth hypotheses when data is scarce and speed matters more than precision.
- **WSJF** (Reinertsen / SAFe): `Cost of Delay ÷ Job Size (duration)`; CoD = user/business value + time criticality + risk reduction/opportunity enablement; estimates are relative (the Fibonacci scale) within a single batch of work. Plus: the economics of delay for a queue of large initiatives and the portfolio.
- **Kano**: classifying the reaction to a feature, not ranking it. Pairs of questions "functional / dysfunctional" yield 5 categories: must-be (the basics — their absence is intolerable), performance (the more, the better), attractive (delighters), indifferent, reverse.
- The methods answer different questions: Kano — "what moves satisfaction", RICE/ICE/WSJF — "in what order to build".
- A practical pairing: Kano — for the release composition; RICE — for the product backlog; WSJF — for the portfolio and large projects; ICE — for fast growth experiments.

## How to do it
1. Pick the method for the task: a measurable funnel → RICE; a queue of large projects → WSJF; hypothesis triage → ICE; release composition → Kano.
2. Fix the scales and definitions up front (what Impact=3 means, what is included in Effort) — otherwise estimates are not comparable between people.
3. Have 3+ participants estimate independently and take the median; flag contested items with low Confidence (RICE) or a coarser scale.
4. Compute the scores in one batch: estimates from different sessions and batches are not comparable (critical for WSJF).
5. Manually review the top of the list: strategic commitments, dependencies, tech debt, and infrastructure are run as a separate track with a capacity quota.
6. After release, return to the actual Reach/Impact/durations and calibrate the scales against history.

## Pitfalls
- Precision theater: scores create the appearance of objectivity but remain expert guesses; a score is a tool for structuring the argument, not a replacement for judgment.
- RICE punishes infrastructure and tech debt: such work has no Reach on users — it needs a separate capacity quota, not a place in the general ranking.
- Typical estimation errors: inflated Reach, underestimated Effort; pad the Effort and check it against the team's historical velocity.
- Kano: categories drift over time — yesterday's delighters become must-be; refresh the survey rather than inheriting the conclusions.

## Links
The scores feed option selection in `M-solution-design`; the Cost of Delay in WSJF is the forgone cash flow from `M-unit-economics`; an initiative's place in the business model is checked on `M-lean-canvas`.
