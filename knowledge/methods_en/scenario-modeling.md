---
id: M-scenario-modeling
lang: en
title: Scenario modeling of the effect — pessimistic, base, and optimistic scenarios, sensitivity
course: strategy
sources: ["EN mirror of the RU methodology card M-scenario-modeling (knowledge/methods/scenario-modeling.md); original sources are listed in the RU card"]
stages: [options, validation, decision]
tags: [scenarios, model, forecast, sensitivity, drivers, assumptions, tornado]
related: [M-traction-model, M-model-validation, M-forecasting-product, M-model-topdown-bottomup, M-risks, M-cannibalization]
---

# Scenario modeling of the effect

## When to apply
When the effect of an initiative or a growth plan is computed in a model ([[M-traction-model]]): so that the
decision rests on a range, not a point; when defending before a committee ("what if conversion is twice
worse?"); when choosing between initiatives with different risk profiles.

## Core
One scenario is a hidden assumption that "everything will go as in the model". Three scenarios make the
assumptions explicit and give the **bounds within which the decision stays right**.

| Scenario | Assumptions | The question it answers |
|---|---|---|
| Pessimistic | conversion below the retro, timelines longer, cannibalization higher, price lower | "what must go wrong for the effect not to pay back"; where the stop criteria are |
| Base | drivers from retro data and confirmed hypotheses | "what we expect if things develop as usual" |
| Optimistic | hypotheses confirmed at the upper bound of the retro | "what scaling is worth if the hypotheses fire" |

Assembly rules:

1. **Assumptions change, not the result.** A scenario = a full run of the model with a different set of
   drivers (conversion, frequency, price, retention, CAC, cannibalization). "Base × 0.7" is not a scenario
   but a label for not knowing the model.
2. **Every scenario is described in words.** "What must be true for this scenario to materialize" —
   2–4 conditions with sources or hypothesis status. A scenario without conditions is unreadable.
3. **Sensitivity (tornado).** On the base scenario: each driver ±10–20% → the change in the target metric.
   The tornado chart shows which 2–3 drivers decide the outcome — they go first into the validation plan
   (the agent's `validation` step).
4. **Expected value — with explicit weights.** If one number is needed: `EV = Σ(scenario × weight)` with
   weights that are explainable (for example, 25/50/25). Do not tune the weights to the desired answer.
5. **Decide by the bounds.** Under the pessimistic scenario the economics must either survive (then the risk
   is acceptable) or have pre-written stop criteria. The optimistic scenario is a scaling plan, not "the one
   that will happen".

## Procedure (agent)
1. Assemble the model: a base run from retro data ([[M-model-topdown-bottomup]], [[M-traction-model]]).
2. List the drivers and their sources; mark each: fact / hypothesis / assumption — its strength.
3. Build the pessimistic and optimistic ones: vary 2–4 drivers within bounds supported by data or analogs;
   do not exceed physical limits (market share, channel capacity).
4. Run the sensitivity: a table "driver ±10% → Δ of the metric"; sort by impact.
   The deciding drivers go first into the validation plan (the agent's `validation` step).
5. Write down each scenario's conditions and plan: stop criteria (pessimistic), validation hypotheses
   (base), scaling triggers (optimistic).
6. Run the auto-check [[M-model-validation]]: period units, the sum of drivers, formula contradictions.

## Template / checklist
- [ ] three scenarios — three different assumption sets, each fully run;
- [ ] every scenario has "what must be true" written down;
- [ ] the tornado is ready: the deciding drivers are visible and they are in the validation plan;
- [ ] EV weights are explainable and not tuned;
- [ ] the pessimistic scenario does not kill the economics without written stop criteria;
- [ ] cannibalization is included in every scenario, not only the base one.

## Typical mistakes
- Three numbers instead of three models: "minus 20%, base, plus 20%" without different assumptions.
- The optimistic one as the target: the plan is written from the best scenario — a "hockey stick" by habit.
- No sensitivity: every hypothesis goes into validation at once instead of the two deciding ones.
- A point forecast as a promise: "we will grow 2.3×" without a range — a commitment that cannot be met.
- A driver outside bounds: conversion higher than ever seen in the retro or in analogs.

## Questions that could change the decision
- At what value of the deciding driver does the initiative stop paying back (the break-even scenario)?
- What is cheaper: narrowing the range with validation or accepting the risk with a stop criterion?
- Does driver correlation change the picture (CAC grows together with scale, not independently)?

## Related cards
[[M-traction-model]] — the growth model and hypothesis layers; [[M-model-validation]] — the model auto-check;
[[M-forecasting-product]] — forecasting; [[M-risks]] — the scenario risk register;
[[M-cannibalization]] — increment with flows; [[M-ab-testing]] — narrowing the driver range.
