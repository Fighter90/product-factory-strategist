---
id: M-double-diamond
lang: en
title: Double Diamond — a process framework from problem to solution
course: synthesis
sources: ["EN mirror of the RU methodology card M-double-diamond (knowledge/methods/double-diamond.md); original sources are listed in the RU card"]
stages: [intake, research, discovery, situation, options, choice, strategy, validation, review]
tags: [process, frameworks, double-diamond]
related: [M-product-frameworks, M-jtbd, M-problem-design, M-solution-design]
---

# Double Diamond

## When to use
When you need to explain and control which stage of thinking the work is at: diverging (ideas, data) or converging (solutions, choices). In the agent it maps onto the 11 process steps and the question blocks.

## Core idea
Two diamond phases; in each one we diverge first, then converge:
1. **Discover** — gather as much as possible about the problem: data, interviews, context. Do not propose solutions.
2. **Define** — narrow down to a properly framed problem/point of view (insight).
3. **Develop** — generate many meaningfully different solutions and attack them.
4. **Deliver** — choose, validate at small scale, record the decision and the metrics.
The classic process mistake is "collapsing the diamond": starting the solution before the problem is understood, or iterating over solutions without selection criteria.

## Mapping onto the agent process
| Phase | Agent steps | Gate | Question block (pfs questions) |
|---|---|---|---|
| Discover | intake → sources → research → discovery | a plan driven by decision-changing questions; personas/JTBD | intake-*, discovery-* |
| Define | situation → options → choice | contradictions named; ≥3 options; the human chooses | situation-*, options-* |
| Develop | strategy → validation | promises ↔ product; metric+baseline+window | strategy-*, validation-* |
| Deliver | review → decision → monitoring | check/rubric; decision record; commitments | decision-* |

## Procedure (agent)
1. At every step, declare the phase ("we are in Define — we are narrowing") — the lead sees the thinking mode.
2. In the Discover/Develop phases, explicitly accumulate options (C### hypotheses, options A–D) instead of cutting early.
3. In the Define/Deliver phases, apply the criteria from the question blocks (options-criteria, choice-reversibility).
4. Never move into the next diamond without its gate: Define closes with a human choice, Deliver with a recorded decision.

## Template / phase-gate checklist
| Transition | What must be ready | Pass criterion |
|---|---|---|
| Discover → Define | a claim registry with sources; a plan driven by decision-changing questions | every key question answered with a C### or a named gap |
| Define → Develop | 02_situation with contradictions; ≥3 meaningfully different options | the red team has responded; the human picked an option |
| Develop → Deliver | 04/05 strategies; 06 validation plan (metric, baseline, window, counter-metrics) | every promise backed by the product map |
| Deliver → next cycle | a decision in decisions.jsonl; commitments with owners and dates | `pfs decision due` empty; monitoring set up |

## Typical mistakes
- Deciding in Discover: "let's just build X" before situation/options.
- An endless Define: data is collected without asking "what would change the decision."
- Deliver without metrics: "launched" = "done."
- One diamond instead of two: no separate work on the problem and on the solution.

## Questions that can change the decision
- Are we currently diverging or converging? What is needed to close the current phase?
- Which fact would send us back to Discover?
- Where did we cut the Define phase short — and what will that cost us in Deliver?

## Related cards
[[M-product-frameworks]], [[M-jtbd]], [[M-problem-design]], [[M-solution-design]]
