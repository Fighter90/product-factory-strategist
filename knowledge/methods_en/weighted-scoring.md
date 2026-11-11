---
id: M-weighted-scoring
lang: en
title: Weighted scoring of options and filters — a transparent comparison of alternatives
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [options, choice]
tags: [scoring, prioritization, criteria, weights, filters, options]
related: [M-solution-design, M-prioritization-ricews, M-unit-economics, M-model-validation, M-decision-daci, M-risks]
---

# Weighted scoring: weights, scales, filters

## When to apply
When you need to compare substantively different options (initiatives, decisions, markets) across several
criteria and obtain a transparent basis for the choice. Scoring is a tool for **structuring the argument**,
not an "objective truth": it is useful before the executive makes the choice ([[M-decision-daci]] — the
decision stays with the human anyway).

## Core idea
Weighted scoring = filters (disqualification) + criteria with weights + scales + numbers from calculations
that reconcile with the knowledge base (PRO-51).

The order of application:
1. **Filters before scoring:** hard disqualifying conditions ("no owner", "contradicts the strategy",
   "unit economics negative under a realistic mix", "cannot be tested within a quarter"). An option that
   fails a filter does not take part in the scoring — this keeps the table from bloating and keeps weak
   options from being "pulled up" by weights.
2. **Criteria:** 4–6, each one a question that the option answers with a number or an expert estimate
   carrying a confidence class. Typical ones: contribution to the target metric (from the model
   [[M-traction-model]]), cost/resources, time to impact, risk (reversibility), confidence in the hypothesis.
3. **Weights:** they sum to 100%; the decision-maker (not the author of the calculation) assigns the
   weights before scores are given — this rules out "tuning the weights to a favorite".
4. **Scales:** a single scale for all options (1–5 or 1–10); the scale has anchors ("5 = +5% to NSM under
   the base scenario with class A–B"); scores come with justification, not "just a number".
5. **Calculation:** `Score = Σ(score × weight)`; next to it — always the raw scores per criterion: the
   decision is made on the profile, not on the sum (an option can lose on the sum but win on a critically
   important criterion).

Connection with the calculations (PRO-51): the criteria "contribution to the metric" and "payback" are
filled in from verified calculations ([[M-unit-economics]], [[M-traction-model]]): ARPU — a weighted
average over the tariff mix, CAC ≠ 0, effects — with cannibalization and elasticity taken into account.
If a number in the scoring contradicts the knowledge base, the scoring is invalid: fix the calculation,
not the table.

## Procedure
1. Formulate the comparison question: "what are we choosing and what does 'better' mean" — the criteria
   follow from the target metric.
2. Run the options through the filters; the disqualified ones go with a reason — they remain in the
   document as considered.
3. Assign the weights (by the decision-maker, before the scores); the sum of the weights = 100%.
4. Fill in the scores with anchors and justifications; numbers — only from calculations that reconcile
   with the base ([[M-model-validation]]).
5. Compute the sums; build the profile of the top-2 options: where they are strong, where they are weak.
6. Show the table to the executive together with the strong objections ([[M-solution-design]]); the
   choice belongs to the human.
7. Write the choice into the decision: grounds (criteria, scores, C###), conditions for revision
   ([[M-decision-daci]]).

## Template / checklist
| Criterion | Weight | Option A | Option B | Option C | Justification of the scores |
|---|---|---|---|---|---|
| Contribution to NSM | | | | | a number from the model + C### |
| Resources/cost | | | | | |
| Time to impact | | | | | |
| Risk/reversibility | | | | | |
| Confidence in the hypothesis | | | | | |
| **Sum** | 100% | | | | |

- [ ] filters applied before scoring, disqualifications with reasons;
- [ ] weights assigned by the decision-maker and before the scores are given;
- [ ] the scale has anchors; every score has a justification;
- [ ] the criterion numbers reconcile with the calculations and the knowledge base (PRO-51);
- [ ] the decision is written down with grounds and conditions for revision.

## Typical mistakes
- The weights are "picked" after the scores so that the favorite option wins.
- Scoring without filters: 10 options across 8 criteria — a table for the table's sake.
- Scores without anchors: "risk 3" means "medium" for one person and "high" for another.
- Criterion numbers out of thin air: "revenue contribution 4" instead of a value from the model
  ([[M-traction-model]]).
- Deciding by the sum of points when the profile is contradictory: the option is critically weak on the
  main criterion.
- Scoring as a substitute for the argument: the table must structure the objections, not replace them.

## Questions that can change the decision
- Which criterion is actually the decisive one, and is it dissolved among the weights?
- Which score in the table is the shakiest — and what would confirm it in the cheapest way?
- Would removing one criterion change the order of the options (a robustness check)?
- Which two options are worth combining or testing together?

## Related maps
[[M-solution-design]], [[M-prioritization-ricews]], [[M-unit-economics]], [[M-model-validation]], [[M-decision-daci]], [[M-risks]]
