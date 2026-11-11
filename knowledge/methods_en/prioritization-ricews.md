---
id: M-prioritization-ricews
lang: en
title: Backlog prioritization — RICE, ICE, WSJF, and Kano: formulas and when to use which
course: pm-approaches-en
sources: ["EN summary of the RU methodology card; original sources listed in the RU card"]
stages: [options, validation]
tags: [en, summary]
related: [M-solution-design, M-unit-economics, M-lean-canvas]
---

# Prioritization: RICE, ICE, WSJF, Kano (EN summary)

**When:** the backlog exceeds team capacity and order disputes come from taste, not data; you need to compare heterogeneous work (features, experiments, debt) and explain the choice to stakeholders.

**Core:** **RICE** (Intercom): `(Reach × Impact × Confidence) ÷ Effort` — Reach is users/events per period, Impact ∈ {3, 2, 1, 0.5, 0.25}, Confidence ∈ {100%, 80%, 50%}, Effort in person-months. **ICE** (Sean Ellis): `Impact × Confidence × Ease`, each 1–10 — fast triage when data is scarce. **WSJF** (Reinertsen/SAFe): `Cost of Delay ÷ Job Size`, where CoD = user-business value + time criticality + risk reduction/opportunity enablement, estimated relatively (Fibonacci) within one batch. **Kano** classifies reactions rather than ranks: must-be, performance, attractive (delighters), indifferent, reverse — via functional/dysfunctional question pairs. Kano answers "what drives satisfaction"; RICE/ICE/WSJF answer "in what order to build". Typical combo: Kano for release scope, RICE for the product backlog, WSJF for the portfolio, ICE for growth experiments.

**How:** pick the method per task → fix scales and definitions up front → 3+ independent estimators, take the median, mark low-confidence items → score within a single batch (batches are not comparable, especially WSJF) → hand-check the top list for strategy, dependencies, and a separate track/quota for tech debt → recalibrate scales against actuals after release.

**Pitfalls:** scoring theater (numbers are expert guesses, not objectivity); RICE punishes infrastructure/debt with no user Reach — give it a separate quota; inflated Reach and lowballed Effort are the classic errors; Kano categories drift over time as delighters become must-be.
