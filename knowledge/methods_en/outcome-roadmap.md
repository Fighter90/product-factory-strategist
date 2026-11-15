---
id: M-outcome-roadmap
lang: en
title: Strategy timelines and the Outcome Roadmap — phases, transition criteria, stop signals
course: strategy
sources: ["EN mirror of the RU methodology card M-outcome-roadmap (knowledge/methods/outcome-roadmap.md); original sources are listed in the RU card"]
stages: [strategy, validation, after-decision]
tags: [roadmap, outcome-roadmap, phases, pilot, validation, scaling, transition-criteria, stop-signal, time-box, dependencies, right-to-fail]
related: [M-strategy-growth, M-goals-drivers-bets, M-risks, M-success-metrics, M-team, M-mvp-pilots, M-pmf-scaling, M-traction-model, M-decision-daci]
---

# Strategy Timelines and the Outcome Roadmap — Phases, Transition Criteria, Stop Signals

## When to apply
When the bets are chosen and you must answer: "what do we do in Q1, what do we postpone, what happens if resources run short or the hypothesis fails". A roadmap here is not a promise to stakeholders but a decision-making tool under constraints: it shows the choices, fixes the trade-offs and leaves room for change. The result is a roadmap that reads like a management document and admits challenge.

## Essence
**A strategy without timelines remains an intention.** The typical picture: the logic exists, the bets and metrics are chosen, but nobody can answer "what is in Q1", "what do we postpone", "what if resources run short".

**Feature-roadmap and outcome-roadmap.** A feature-roadmap lists what will be built ("launched onboarding, a filter, a page") and creates an illusion of control: it substitutes activity for the result. An outcome-roadmap answers which result you want to achieve and verify ("cut time-to-value", "raised activation", "reduced drop-off at a critical step"). A feature-roadmap is acceptable as an internal delivery plan layered on top of the outcome-roadmap.

**The eight elements of an outcome-roadmap**
| # | Element | What it must contain |
|---|---|---|
| 1 | Strategic bet | a large hypothesis tied to an outcome; the number of bets is limited by resources |
| 2 | Phases | pilot → validation → scaling (the number of stages can vary; a pilot always starts with minimal investment) |
| 3 | Outcome metric | a specific change in a specific metric — the goal of the whole bet, not just a phase |
| 4 | Output metric | a fast proxy for the early phases |
| 5 | Timelines | a time-box for each phase |
| 6 | Dependencies | whom we depend on, whether priorities are agreed, whether there are blockers |
| 7 | Transition criteria | numeric thresholds for the next phase ("CTR > N% → validation") |
| 8 | Stop signal | a condition for closing the bet, defined in advance |

**Phases — a way of buying knowledge sequentially**
| Phase | What we "buy" | What we verify | Means | Duration | Metric |
|---|---|---|---|---|---|
| Pilot (discovery) | a signal: does the idea work at all? | the presence of a qualitative signal, not statistical significance | simple ones: a simplified scenario, pre-filling, rule-based instead of ML | days–weeks (if it is 3 months and serious development, it is already a mini-MVP) | output |
| Validation (MVP) | proof: does it affect the outcome, are there side effects | a statistically significant effect | a working version, an A/B test | weeks–months | outcome |
| Scaling | scale: is the effect stable, does it pay off | economic efficiency | a full rollout, connecting marketing | months–quarters | outcome + ROI |
The absence of phases is a signal of weak planning: without them "six months of development → the wrong effect → restructuring".

**Output and outcome.** The outcome (retention, revenue, LTV) lags: an action → after 1–2 weeks you see output (the block's CTR) → after 1–2 months retention moves → after 3–6 months the business. Output is a fast proxy; it shows direction but does not prove impact on the outcome, so at validation the goal is the outcome. The outcome metric does not disappear: it is the "contract" with stakeholders; at the pilot the goal is output, at validation — outcome, at scaling — outcome + ROI.

**The right to fail is planned, not requested.** A buffer for errors is built into the roadmap, agreed with leadership in advance, has a time-box and a resource cap, and there are failure criteria and a plan B. A hypothesis failing is a planned outcome, not a catastrophe.

**A management contract (an example from the course).** The bet: personalization of recommendations for a marketplace. Metric: the share of repeat purchases within 15 days from 22% → 27% over 6 months. Ambition — 27%; acceptable — 25% (the economics add up, fewer resources allocated); below 25% — the bet is closed and resources are reallocated. A pilot of 2–4 weeks on the current team: rule-based recommendations, output — the block's CTR above the threshold; if lower — plan B (CRM triggers, a new pilot). Validation 2–3 months: a full system, an A/B test, an outcome of +2 pp significant; if not — closure. Scaling 2–3 months: a full rollout, marketing, ROI, 27% (25% acceptable).

**The "bets × phases × months" format** (a grid from the course's practice) — each bet occupies a block of rows:
| Column | What is written |
|---|---|
| Bet / Phase / Milestone | the bet's row and nested phase rows (Pilot → MVP → Scale or Discovery → MVP → Scale) |
| Resource | a concrete staffing and loading per phase ("2 BE, 1 FE, analyst 50%, designer — outsourced"), not "the development team" |
| Outcome metric | baseline → target + a revision threshold ("if after 3 months <+10% → adjustment") |
| Output metric | a threshold for moving to the next phase + plan B ("CTR <1% → a UX revision", "<+3% CR → simplification (plan B)") |
| Dependencies / hiring | neighboring teams and vacancies with months ("3 dev: hiring M2→M5") |
| Comment | the bet's type (quick win / big bet) and horizon, parallelism with other bets |
| Months 1–12 | fortnight strips marking the active phase |

Bets of different scale coexist in one plan: quick wins (a horizon of ~3 months, a visible contribution to the current quarter) and big bets (6–12 months, a Discovery phase on thin resources until confirmation). Shared resources are visible in the grid: two bets share one backend — the loading is split explicitly ("BE: 30% capacity, 70% — on bet 2"). A separate row tracks **hiring**: search → offer → onboarding for each vacancy with months; phases that depend on hiring shift with it, rather than "believing" in the ideal date.

**The contribution of initiatives to the overall result.** In a strategy implementation plan, every initiative carries an expected contribution to the target metrics in percent (the sum ≈ 100%) — this makes priorities measurable and allows an honest answer to "which stream delivers the growth". In parallel with product initiatives, separate tracks run (partnerships, BD, marketing) which must not "fall out" of the roadmap.

**Seasonality in the plan.** Three rules: (1) mass launches and effect measurements happen in the peak season of demand; outside the season do preparation, integrations and retention of the offer; (2) promo and growth mechanics launch **before** the trading season starts (sellers must have time to connect: in the course's example — weeks before the season starts); (3) in each bet's card, mark the season into which the outcome measurement falls, and do not make decisions on a "dead" season without an adjustment. More on seasonality risks — [[M-risks]].

**Resources are part of strategy.** With 2 developers and 1 designer you cannot run four strategies in parallel. Resource constraints: the team, hiring, dependencies, technology, competencies.
- Hiring is a long chain (vacancy → search → interviews → offer → start → onboarding); the course's reference points: 3–6 months of hiring and 1–3 months of onboarding (in the notes — "6 or more"), not an SLA; for a resource needed in Q3, start thinking in Q1.
- A mature approach: a pilot on current resources; expansion — after confirmation; a parallel search; alternatives — reducing the scope, outsourcing, moving a phase. Two extremes: "freeze everything until the hire" and "plan as if already hired".
- Dependencies: platform, technological, organizational (marketing, legal, support), human. Keep a register: bet, dependency, team, approval status, risk, mitigation.
- Bets compete (short-term revenue vs retention and infrastructure); the company's context affects priority (if the company is "pushing" revenue, long-term bets get de-prioritized). Choosing one bet = giving up another; the roadmap shows which bet is #1 and what is postponed.

## Procedure
1. **Take the bets** from `M-goals-drivers-bets` with effect and effort estimates.
2. **For each bet set an outcome metric** (baseline → target → deadline), an "acceptable" level and a closure threshold.
3. **Split into phases**: at the pilot choose an output proxy and minimal means; specify what counts as a qualitative signal.
4. **Set the time-boxes** and **numeric transition criteria** for each phase; for each — a stop signal and plan B.
5. **Build the dependency register** and agree priorities with the owners; dependent teams go into the agreements table (`M-risks`).
6. **Define resources and hiring**: who is available now, what is needed later, which alternatives exist if hiring fails; account for hiring in the timelines and the traction model (`M-team`).
7. **Set priorities and trade-offs**: which bet is #1 and why, which are postponed and why, how the company's context changes the order.
8. **Lay it out by quarters**: what is in Q1, Q2…, what is postponed; the scenarios "if it does not work", "if the resource is not hired".
9. **Run the completeness checklist** and agree with stakeholders (DACI); set a review date.

## Template / checklist
**A bet's card in the roadmap**
| Field | Example |
|---|---|
| Bet | improve retention through personalization of recommendations |
| Phase | pilot |
| Outcome metric | share of repeat purchases within 15 days: 22% → 27% (acceptable ≥25%) |
| Output metric | the recommendations block's CTR above a set threshold |
| Duration (time-box) | 4 weeks |
| Dependencies | data preparation from the platform team (agreed / not) |
| Transition criterion | CTR > threshold → validation; not → plan B (CRM triggers) |
| Stop signal | after 6 months < 25% → the bet closes, resources reallocated |
| Resources | the current team; expansion after validation |

**The completeness checklist** (must answer "yes" to every question)
- [ ] The bet is tied to an outcome
- [ ] Phases are defined, each with its own metric (early ones — output proxies)
- [ ] Every phase has a time-box
- [ ] Dependencies identified and agreed
- [ ] Transition criteria are numeric; a stop signal is defined; an error buffer and plan B are built in
- [ ] It is stated who makes the transition decision
- [ ] It is shown what is postponed and why
- [ ] Hiring and alternatives are accounted for in the timelines
- [ ] Stakeholders agreed the elements

## Typical mistakes
- Roadmap = a list of features; no phases; no dependencies; output not linked to outcome; no gates and stop conditions.
- Endless testing: "we need more data" without a stop criterion.
- A 3-month pilot with serious development (that is not a pilot).
- One outcome metric for all phases: waiting months for feedback.
- "First we invent the strategy, we'll find resources later"; a strategy requiring 20 developers who do not exist.
- A single region for a regional pilot; a pilot without a criterion of "what counts as a signal".
- A roadmap as a promise, not a tool of choice: no room for change; the "right to fail" is requested after the failure.
- Nobody can see what was de-prioritized, and nobody explained why.

## Questions that can change the decision
- Which minimal signal in 2–4 weeks will show whether to continue (which output proxy and threshold)?
- Does a proven output → outcome link exist, or is it a hypothesis?
- What does an error cost at each phase, and how much buffer is agreed?
- What happens if the key dependency does not get priority in time?
- Which resource is key and will it start by the phase's beginning; what do we do if it does not?
- At which result is the bet considered closed, and who approved that threshold?
- Which demand season does the outcome measurement fall into, and might the season force moving phases or validation?
- What happens if we do nothing (the inertial scenario of the metric)?

## Related cards
[[M-strategy-growth]], [[M-goals-drivers-bets]], [[M-risks]], [[M-success-metrics]], [[M-team]], [[M-mvp-pilots]], [[M-pmf-scaling]], [[M-traction-model]], [[M-decision-daci]]
