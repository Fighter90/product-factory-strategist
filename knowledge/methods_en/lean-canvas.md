---
id: M-lean-canvas
lang: en
title: Lean Canvas — business hypotheses on a single page
course: strategy
sources: ["EN mirror of the RU methodology card M-lean-canvas (knowledge/methods/lean-canvas.md); original sources are listed in the RU card"]
stages: [intake, discovery, options, strategy, validation]
tags: [business-model, frameworks, lean]
related: [M-business-models, M-unit-economics, M-product-frameworks, M-goals-drivers-bets]
---

# Lean Canvas

## When to apply
A new product/direction or a model rebuild: you need to capture the business hypotheses on one screen —
problem, customer, value, channels, monetization, costs, metrics — and understand which box is the most
risky one. In the agent it is filled in at the intake/discovery/strategy steps from the claims registry.

## Essence — 9 blocks, the fill order matters
1. **Problem** — 1–3 real pains; for each one, the existing alternatives.
2. **Customer segments** — early adopters, not "everyone".
3. **USP** — one clear message about value; it differentiates from the alternatives.
4. **Solution** — the 3 most important capabilities (after the problem!).
5. **Channels** — how to reach customers: scalable and not.
6. **Revenue streams** — the monetization model, price, value metric.
7. **Cost structure** — fixed/variable, what dominates.
8. **Key metrics** — the activity funnel (an AARRR slice): what proves progress.
9. **An advantage that is hard to copy** — data, network, contracts, brand.

Link to unit economics: boxes 6–8 are the inputs of `pfs calc` (ARPU, CAC, churn); a Lean Canvas without
a calculation is a declaration, not a hypothesis.

## Procedure (agent)
1. Fill boxes 1–2 from situation/discovery; every pain and segment carries a C###/S###.
2. USP and solution (3–4) — from the chosen option; check the "promise ↔ confirmation" pair.
3. Channels/revenue/costs (5–7) — with numbers from `calcs.json`/`unit_economics.xlsx`.
4. Metrics (8) — align with 06_validation_plan (one primary metric + a guardrail).
5. Mark the **riskiest box** and add its validation to the plan (that is the next experiment).

## Template (checklist)
Problem: … [C###] · Alternatives: … [C###] · Segment: … [C###] · USP: … · Solution: … · Channels: … ·
Revenue: … [C###] · Costs: … [C###] · Metrics: … · Uncopyable advantage: …

## Template (table: block → hypothesis → source → validation)
| # | Block | What we capture | Source | How we validate |
|---|---|---|---|---|
| 1 | Problem | top-3 pains of the segment | situation + discovery | in-depth interviews, C### |
| 2 | Segment | early adopters | audience/customers | quant survey on a representative sample |
| 3 | USP | one value message | VPC/Job Story [[M-usp]] | BHT, message test |
| 4 | Solution | 3 key capabilities | the chosen option | fake-door, MVP [[M-mvp-pilots]] |
| 5 | Channels | 2–3 channels with a cost per contact | landscapes [[M-landscapes]] | CPL from a pilot |
| 6 | Revenue | model, value metric, price | monetization [[M-monetization]] | willingness to pay (Van Westendorp/survey) |
| 7 | Costs | fixed/variable, drivers | unit economics [[M-unit-economics]] | `pfs calc unit-econ` |
| 8 | Metrics | one primary + guardrail | [[M-success-metrics]] | 06_validation_plan |
| 9 | Moat | structure (data, network, contracts) | [[M-business-models]] | the question "why won't it be copied within 3 months" |

## Typical mistakes
- "Everyone" as a segment; a USP made of adjectives ("convenient, reliable"); solution before problem.
- "Social networks" as channels without a channel price; vanity metrics (downloads instead of repeat purchases).
- "We do X better" as the advantage — that is not a moat; look for structure (data, network, contracts).

## Questions that can change the decision
- Which box dies first if the main forecast fails?
- What is the cheapest test of the riskiest box this week?

## Related maps
[[M-business-models]], [[M-unit-economics]], [[M-product-frameworks]], [[M-goals-drivers-bets]]
