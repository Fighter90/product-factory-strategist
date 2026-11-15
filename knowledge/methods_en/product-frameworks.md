---
id: M-product-frameworks
lang: en
title: Product Frameworks — what, when, and why
course: synthesis
sources: ["EN mirror of the RU methodology card M-product-frameworks (knowledge/methods/product-frameworks.md); original sources are listed in the RU card"]
stages: [intake, research, discovery, situation, options, choice, strategy, validation, review, after-decision]
tags: [frameworks, prioritization, metrics, process, hadi, hypotheses]
related: [M-double-diamond, M-lean-canvas, M-goals-drivers-bets, M-success-metrics, M-product-metrics, M-monetization]
---

# Overview of product frameworks

## When to apply
Choosing the tool for the phase and the question. The agent's rule: a framework is a checklist and a vocabulary, not "the right answer"; every framework is filled with data from the C###/S### registry and the calculations, otherwise it is useless.

## The "phase → frameworks" map
| Phase (double diamond) | Question | Frameworks (maps) |
|---|---|---|
| Discover | What is happening? who is the user? | JTBD [[M-jtbd]], Audience [[M-audience-research]], PESTEL [[M-external-environment]], Trends [[M-trends-scenarios]], Double Diamond [[M-double-diamond]] |
| Define | Which problem do we solve? what is true? | Problem Design [[M-problem-design]], Competitors [[M-competitors]], the Situation framework, Lean Canvas [[M-lean-canvas]] |
| Develop | How do we solve it? what has priority? | Drivers and bets [[M-goals-drivers-bets]], RICE/ICE/WSJF (below), Kano [[M-marketing-research]], Cannibalization [[M-cannibalization]], Platforms [[M-platforms-types-criteria]] |
| Deliver | How do we verify and record it? | A/B [[M-ab-testing]], NSM/OKR [[M-success-metrics]], Product metrics [[M-product-metrics]], Six-pager [[M-six-pager]], DACI [[M-decision-daci]] |

## Prioritization — a quick method choice
- **RICE** (Reach × Impact × Confidence / Effort) — when there is a countable reach and confidence estimates; for the quarterly backlog.
- **ICE** (Impact × Confidence × Ease) — a quick estimate at the sprint horizon; less data, more argument.
- **WSJF** (weight/duration) — when the cost of delay differs across initiatives (seasonality, regulation).
- The discipline is the same: the criteria are fixed **before** the estimates, and Confidence references a C###.

## Metric families
- **AARRR** — the growth funnel (acquisition→activation→retention→revenue→referral): where the bottleneck is.
- **HEART** — product quality: Happiness/Engagement/Adoption/Retention/Task success.
- **Kano** — which features are basic/performance/delighters — for surveys and the roadmap.
- **NSM + a metric tree** — one north star and its drivers; the input for OKR [[M-success-metrics]].

## Hypothesis-testing cycles
- **HADI** (Hypothesis→Action→Data→Insight) — the micro-cycle of every bet: a hypothesis from a C###, an action, data, a conclusion → update the claim (supersede) — and again.
- **MVP/pilot** [[M-mvp-pilots]] — choosing the type of test to match the risk; **backtest** [[M-model-validation]] — for models/forecasts.

## Procedure (agent)
1. Determine the double-diamond phase and the question — pick 1–2 frameworks from the map, no more.
2. Fill the framework with registry data: every cell/score is a C###/S### or an "EXAMPLE" mark.
3. Derive a testable consequence from the framework → add it to the validation plan (06) or a forecast (a C###-forecast).

## Typical mistakes
- A framework for the framework's sake: filling in everything in a row instead of the one needed.
- Estimates without confidence grounding: a RICE with Confidence=100% despite unverified data.
- Fitting the result: the prioritization criteria are changed after the estimates have been seen.
- Collecting: 6 frameworks for one question — zero new knowledge after the third.

## Questions that could change the decision
- Which single framework answers the current question at the lowest cost?
- What would have to happen for us to switch the diamond phase right now?

## Related maps
[[M-double-diamond]], [[M-lean-canvas]], [[M-goals-drivers-bets]], [[M-success-metrics]], [[M-ab-testing]]
