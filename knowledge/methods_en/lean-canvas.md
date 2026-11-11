---
id: M-lean-canvas
lang: en
title: Lean Canvas — business hypotheses on one page
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [intake, discovery, options, strategy, validation]
tags: [business-model, lean-canvas, hypotheses, value-proposition, early-adopters, moat, validation]
related: [M-business-models, M-unit-economics, M-product-frameworks, M-goals-drivers-bets]
---

# Lean Canvas

## When to apply
A new product/direction or a rebuild of the model: you need to capture the business's hypotheses on one screen — problem, customer, value, channels, monetization, costs, metrics — and understand which cell is the riskiest. In the agent it is filled at the intake/discovery/strategy steps from the claims registry.

## Core idea — 9 blocks, fill-in order matters
1. **Problem** — 1–3 real pains; for each one, the existing alternatives.
2. **Customer segments** — early adopters, not "everyone".
3. **UVP** — one clear message about the value; it distinguishes you from the alternatives.
4. **Solution** — the 3 most important capabilities (after the problem!).
5. **Channels** — how to reach customers: scalable and non-scalable.
6. **Revenue streams** — the monetization model, the price, the value metric.
7. **Cost structure** — fixed/variable, and what dominates.
8. **Key metrics** — the activity funnel (an AARRR slice): what proves progress.
9. **An advantage that is hard to copy** — data, network, contracts, brand.

Link to unit economics: cells 6–8 are the inputs of `pfs calc` (ARPU, CAC, churn); a Lean Canvas without the calculation is a declaration, not a hypothesis.

## Procedure (agent)
1. Fill cells 1–2 from the situation/discovery documents; every pain and segment backed by C###/S###.
2. UVP and solution (3–4) — from the chosen option; run the "promise ↔ proof" check.
3. Channels/revenue/costs (5–7) — with numbers from `calcs.json`/`unit_economics.xlsx`.
4. Metrics (8) — align with 06_validation_plan (one headline metric + a guardrail).
5. Mark the **riskiest cell** and add its test to the plan (that test is the next experiment).

## Template (checklist)
Problem: … [C###] · Alternatives: … [C###] · Segment: … [C###] · UVP: … · Solution: … · Channels: … · Revenue: … [C###] · Costs: … [C###] · Metrics: … · Uncopyable advantage: …

## Template (table: block → hypothesis → source → check)
| # | Block | What we capture | Where from | How we check |
|---|---|---|---|---|
| 1 | Problem | the segment's top-3 pains | situation + discovery | depth interviews, C### |
| 2 | Segment | early adopters | audience/clients | a quantitative survey on a representative sample |
| 3 | UVP | one value message | VPC/Job Story [[M-usp]] | BHT, a message test |
| 4 | Solution | 3 key capabilities | the chosen option | fake-door, MVP [[M-mvp-pilots]] |
| 5 | Channels | 2–3 channels with a cost per contact | landscapes [[M-landscapes]] | CPL from the pilot |
| 6 | Revenue | the model, the value metric, the price | monetization [[M-monetization]] | willingness to pay (Van Westendorp/survey) |
| 7 | Costs | fixed/variable, drivers | unit economics [[M-unit-economics]] | `pfs calc unit-econ` |
| 8 | Metrics | one headline + a guardrail | [[M-success-metrics]] | 06_validation_plan |
| 9 | Moat | structure (data, network, contracts) | [[M-business-models]] | the question "why won't they copy it within 3 months" |

## Typical mistakes
- "Everyone" as the segment; a UVP made of adjectives ("convenient, reliable"); the solution before the problem.
- Channels as "social media" without a channel cost; vanity metrics (downloads instead of repeat purchases).
- The advantage "we do X better" — that is not a moat; look for structure (data, network, contracts).

## Questions that can change the decision
- Which cell dies first if the main forecast does not come true?
- What is the cheapest test of the riskiest cell that can run this week?

## Related maps
[[M-business-models]], [[M-unit-economics]], [[M-product-frameworks]], [[M-goals-drivers-bets]]
