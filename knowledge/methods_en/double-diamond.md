---
id: M-double-diamond
lang: en
title: Double Diamond — the process frame from problem to solution
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [intake, research, discovery, situation, options, choice, strategy, validation, review]
tags: [process, frameworks, double-diamond, diverge-converge, phase-gates]
related: [M-product-frameworks, M-jtbd, M-problem-design, M-solution-design]
---

# Double Diamond

## When to apply
When you need to explain and control which thinking stage the work is in: are we diverging (ideas, data) or converging (solutions, choice). In the agent it maps onto the 11 process steps and onto the question blocks.

## Core idea
Two "diamond" phases; in each one you diverge first, then converge:
1. **Discover** — gather as much as possible about the problem: data, interviews, context. Do not propose solutions.
2. **Define** — narrow it down to a correctly posed problem / point of view (an insight).
3. **Develop** — generate many meaningfully different solutions and attack them.
4. **Deliver** — choose, verify at a small scale, record the decision and the metrics.
The classic process failure is "collapsing the diamond": starting on a solution before the problem is understood, or iterating over solutions with no choice criteria.

## Mapping to the agent workflow
| Phase | Agent steps | Gate | Question block (pfs questions) |
|---|---|---|---|
| Discover | intake → sources → research → discovery | a plan built from decision-changing questions; personas/JTBD | intake-*, discovery-* |
| Define | situation → options → choice | contradictions named; ≥3 options; the human chooses | situation-*, options-* |
| Develop | strategy → validation | promises ↔ product; metric + baseline + timeframe | strategy-*, validation-* |
| Deliver | review → decision → monitoring | check/rubric; the decision recorded; commitments | decision-* |

## Procedure (agent)
1. At every step, announce the phase ("we are in Define — we are narrowing down") — the lead sees the thinking mode.
2. In the Discover/Develop phases, explicitly accumulate options (C### hypotheses, variants A–D) instead of pruning early.
3. In the Define/Deliver phases, apply the criteria from the question blocks (options-criteria, choice-reversibility).
4. Never move into the next diamond without the gate: Define closes with the human's choice, Deliver with the recorded decision.

## Template / checklist of phase gates
| Transition | What must be ready | Pass criterion |
|---|---|---|
| Discover → Define | a claim registry with sources; a plan built from decision-changing questions | every key question answered with a C### or a named gap |
| Define → Develop | 02_situation with contradictions; ≥3 meaningfully different options | the red team has answered; the human has chosen an option |
| Develop → Deliver | 04/05 strategies; the 06 validation plan (metric, baseline, timeframe, counter-metrics) | every promise backed by the product map |
| Deliver → next cycle | the decision in decisions.jsonl; commitments with owners and dates | `pfs decision due` is empty; monitoring is set up |

## Typical mistakes
- Deciding during Discover: "let's just do X right away" before situation/options.
- An endless Define: data is collected without the question "what will change the decision".
- Deliver without metrics: "we launched" = "we are done".
- One diamond instead of two: no separate work on the problem and on the solution.

## Questions that can change the decision
- Are we diverging or converging right now? What is needed to close the current phase?
- What fact would send us back to Discover?
- Where did we cut the Define phase short — and what will it cost us in Deliver?

## Related maps
[[M-product-frameworks]], [[M-jtbd]], [[M-problem-design]], [[M-solution-design]]
