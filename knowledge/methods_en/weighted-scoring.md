---
id: M-weighted-scoring
lang: en
title: Weighted scoring of options and filters — criteria, weights, go/no-go before scoring
course: strategy
sources: ["EN mirror of the RU methodology card M-weighted-scoring (knowledge/methods/weighted-scoring.md); original sources are listed in the RU card"]
stages: [options, choice]
tags: [scoring, prioritization, criteria, weights, filters, decision-matrix, calibration]
related: [M-prioritization-ricews, M-goals-drivers-bets, M-decision-daci, M-solution-design, M-problem-design, M-product-frameworks]
---

# Weighted scoring of options and filters

## When to apply
When you need to compare **substantively different options** (product bets, entry countries, vendors, quarter
focuses) against shared criteria and get a transparent basis for the discussion. Scoring does not make the
decision — it structures it; the choice stays with the human (the `choice` step, [[M-decision-daci]]).

## Core: filters before scoring, scoring after
Scoring is expensive — do not spend it on options that drop out on thresholds.

**Step 1 — go/no-go filters (before the table).** Hard thresholds that need no weights: legally permissible?
technically feasible in our timeline? not contradicting the strategy? passing minimal economics (for example,
UE > 0 under the pessimistic scenario)? An option that fails a filter drops out — or gets the condition
"valid if the threshold is closed", and that condition is written down explicitly.

**Step 2 — criteria and weights.** Criteria are derived from the strategy and the decision's task, not a
"standard set": impact on the target metric/NSM, confidence in the effect estimate (is there data), cost and
timeline, risk and reversibility (can it be rolled back), strategic synergy. Weights are set before the
scores — otherwise it is tuning for the favorite option. The weights sum to 100%; keep no more than 5–6
weights: discriminability degrades.

**Step 3 — scores with anchors.** A 1–5 scale with written anchors for each criterion ("5 = confirmed by
A/B data; 3 = a retrospective analog; 1 = expert opinion only"). Scores come from 2+ people independently;
gaps larger than 2 points are discussed, not averaged: behind a gap there is usually a different understanding
of the option.

**Step 4 — the total and the robustness check.** `Total = Σ(weight × score)`. Then a sensitivity check:
does shifting a weight by ±5–10 pp change the winner? If yes — the decision is not robust, and that is an
important result: the argument should be about the weights (that is, about strategy), not about the table.

**Interpretation.** A 0.1-point gap between options is not a "winner" but a "statistical tie": the decision
is made on qualitative grounds, and the table is used as background. Scoring must coexist with the "strong
objections" of each option and the conditions under which the option is valid (the `options` step); an option
with the best score and an unanswered killer objection is not chosen.

## Procedure (agent)
1. Fix the decision's task and the criteria from the strategy; agree the weights with the lead before any
   scores.
2. Run the go/no-go filters; for dropped options, write the condition for returning to consideration.
3. Assemble the table: options × criteria; scores independently from 2+ scorers with anchors.
4. Compute the totals; run the weight sensitivity; mark the non-robust spots.
5. Present the table with conclusions and a recommendation at the `choice` step (`pfs ask`); the decision and
   its grounds go into the [[M-decision-daci]] journal.
6. Revision: with new data, rescore only the affected criteria, not the whole table.

## Template / checklist
- [ ] filters applied before scoring; dropped options have a return condition recorded;
- [ ] criteria derived from the strategy; ≤ 6 weights summing to 100%;
- [ ] weights agreed before scores are given;
- [ ] every scale has written anchors; scores are independent, gaps were discussed;
- [ ] weight sensitivity checked; non-robustness recorded as a result;
- [ ] every option keeps its "strong objections" and validity conditions alive.

## Typical mistakes
- Weights after the scores: the table retroactively proves the preselected favorite.
- False precision: "7.4 vs 7.2" as the basis of a decision on expert scales.
- Scoring instead of discussion: the table does not replace red team and objections — it structures them.
- Filler criteria: "innovativeness" without a definition and anchors wobbles the total.
- One scorer: correlated errors and blind spots; a minimum of two views on doubtful cells.

## Questions that could change the decision
- Which criterion is actually decisive — and is it diluted among five equal weights?
- If the winner is not robust to weights, what are the parties really arguing about (about the weights =
  about strategy)?
- Did all options pass the filters honestly, or was a strong option "rescued" from a threshold?

## Related cards
[[M-prioritization-ricews]] — scoring tasks within a backlog; [[M-goals-drivers-bets]] — bets and portfolio;
[[M-solution-design]] — solution hypotheses and validation; [[M-decision-daci]] — recording the decision;
[[M-scenario-modeling]] — option economics across scenarios; [[M-problem-design]] — problem prioritization.
