---
id: M-scenario-modeling
lang: en
title: Scenario modeling of impact — pessimistic, base and optimistic scenarios, sensitivity
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [options, validation, after-decision]
tags: [scenarios, sensitivity, modeling, forecast, risk, traction-model]
related: [M-traction-model, M-model-validation, M-forecasting-product, M-trends-scenarios, M-risks, M-unit-economics]
---

# Scenario modeling: three scenarios and sensitivity

## When to apply
When a decision rests on a growth model or on a calculation of an initiative's impact: instead of one
"point" number — three scenarios (pessimistic, base, optimistic) and an understanding of which inputs the
model is most sensitive to. Needed at the options step (comparing options), validation (expected change)
and decision (grounds for the decision).

## Core idea
A scenario is a coherent set of input values, not "the forecast minus 30%". A point forecast lies twice:
it hides the spread and conceals the dependencies between inputs.

- **Pessimistic:** inputs at "what certainly will not turn out worse" levels — low conversions, slow
  growth, high churn; the model must survive here too (or have a plan B/C).
- **Base:** confirmed data + validated hypotheses; every value with a C###/S### source.
- **Optimistic:** the upper bound of the plausible — taken from benchmarks or the best confirmed
  experiments, not a "dream"; used for capacity planning, not for promises to the committee.

Sensitivity: ±10–20% applied in turn to each key input while the others stay at base — which inputs move
the result the most (a tornado list). Weakly influential inputs do not deserve refinement; strongly
influential ones are candidates for testing by an experiment before the decision.

Rules of honest scenario modeling:
- scenarios differ in **several coherent inputs** (a "bad market" scenario: conversion is lower, CAC is
  higher, growth is slower — they are linked), not in a single number;
- the scenario's assumptions are written down explicitly and stay readable ([[M-model-validation]]: units,
  periods, formulas);
- hypothesis effects are not summed without adjusting for elasticity and plateau ([[M-traction-model]]);
- the result of a scenario is a range plus the conditions under which it materializes, not "a number ±
  vibes";
- every scenario has a consequence for the decision: what we do if exactly that one materializes.

## Procedure
1. Fix the model's output (revenue, paying users, payback) and the horizon; write down the formulas and
   the units.
2. List the key inputs (5–8); for each one — the current value, a source and a confidence class.
3. Assemble the base scenario from the data; mark the inputs that are unconfirmed hypotheses.
4. Build the pessimistic and optimistic scenarios: shift the linked inputs coherently; the source of the
   upper bound is a benchmark/an experiment.
5. Run the sensitivity: ±10–20% for each input; build a tornado list "input → change in output".
6. For the top 2–3 sensitive inputs — a testing plan (an experiment before the decision or monitoring
   after it).
7. Write down the consequences: a continue/change/stop criterion for each scenario
   ([[M-forecasting-product]] for the boundaries of the forecast).

## Template / checklist
| Input | Pessimistic | Base | Optimistic | Source of the base | Class |
|---|---|---|---|---|---|
| | | | | | |

| Scenario | Output (horizon) | Key assumptions | Consequence for the decision |
|---|---|---|---|
| Pessimistic | | | |
| Base | | | |
| Optimistic | | | |

- [ ] three scenarios with coherent sets of inputs, not "one number minus 30%";
- [ ] every input has a source and a confidence class;
- [ ] the sensitivity tornado list is built, the top inputs have a testing plan;
- [ ] every scenario has its consequence for the decision written down;
- [ ] formulas, units and periods are consistent (the auto-checks of [[M-model-validation]]).

## Typical mistakes
- Three scenarios as "×0.8 / ×1.0 / ×1.2" of one number: the spread is fake, the input dependencies are lost.
- An optimistic "dream" scenario with no source: that is what gets promised to the committee as the plan.
- Sensitivity to an input that cannot be changed or tested: knowledge without action.
- Summing hypothesis effects without elasticity: "three initiatives will give +3×10%" — a hockey stick
  ([[M-traction-model]]).
- A scenario without a consequence: "if pessimistic — well, that's bad" instead of a plan written in advance.
- Hidden inconsistency: the base conversion paired with the optimistic scenario's CAC ([[M-model-validation]]).

## Questions that can change the decision
- Which input moves the result the most, and how do we test it in the cheapest way?
- At which values of the inputs does the decision flip to the opposite (a reversal threshold)?
- What do the pessimistic and base scenarios have in common — what is almost certainly true?
- Which scenario makes the initiative unprofitable — and do we have a plan for that case?

## Related maps
[[M-traction-model]], [[M-model-validation]], [[M-forecasting-product]], [[M-trends-scenarios]], [[M-risks]], [[M-unit-economics]]
