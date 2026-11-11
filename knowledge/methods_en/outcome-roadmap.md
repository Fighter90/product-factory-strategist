---
id: M-outcome-roadmap
lang: en
title: Strategy timing and the outcome roadmap — phases, gate criteria, stop signals
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [strategy, validation, after-decision]
tags: [roadmap, outcome-roadmap, phases, pilot, validation, scaling, gate-criteria, stop-signal, time-box, dependencies]
related: [M-strategy-growth, M-goals-drivers-bets, M-risks, M-success-metrics, M-team, M-mvp-pilots, M-pmf-scaling, M-traction-model, M-decision-daci]
---

# Strategy timing and the outcome roadmap — phases, gate criteria, stop signals

## When to apply
When the bets are already chosen and you have to answer: "what do we do in Q1, what do we put off, and what happens if resources run short or the hypothesis is not confirmed". A roadmap here is not a promise to stakeholders but a decision-making tool under constraints: it surfaces the choices, fixes the trade-offs, and leaves room for change. The result is a roadmap that reads like a management document and can be openly challenged.

## Core idea
**A strategy without timing stays an intention.** The typical picture: the logic is there, the bets and metrics are chosen, but nobody can answer the questions "what is in Q1", "what do we defer", "what do we do if resources run short".

**Feature roadmap vs outcome roadmap.** A feature roadmap lists what will be built ("we launched onboarding, a filter, a page") and creates an illusion of control: it substitutes activity for results. An outcome roadmap states what result you want to get and verify ("cut time-to-value", "raise activation", "reduce drop-off at the critical step"). A feature roadmap is acceptable as an internal delivery plan layered on top of an outcome roadmap.

**Eight elements of an outcome roadmap**
| # | Element | What it must contain |
|---|---|---|
| 1 | Strategic bet | a large hypothesis tied to an outcome; the number of bets is limited by resources |
| 2 | Phases | pilot → validation → scaling (the number of stages may vary; a pilot always starts with the minimum investment) |
| 3 | Outcome metric | a specific change in a specific metric — the goal of the whole bet, not just of a phase |
| 4 | Output metric | a fast proxy for the early phases |
| 5 | Timing | a time-box for every phase |
| 6 | Dependencies | who we depend on, whether priorities are agreed, whether there are blockers |
| 7 | Gate criteria | numeric thresholds for moving to the next phase ("CTR > N% → validation") |
| 8 | Stop signal | a condition for closing the bet, defined in advance |

**Phases are a way of buying knowledge sequentially**
| Phase | What you "buy" | What you verify | Means | Duration | Metric |
|---|---|---|---|---|---|
| Pilot (discovery) | a signal: does the idea work at all? | the presence of a qualitative signal, not statistical significance | simple means: simplifying the scenario, pre-filling, rule-based instead of ML | days–weeks (if it is 3 months with serious development, that is already a mini-MVP) | output |
| Validation (MVP) | proof: does it affect the outcome, are there side effects | a statistically significant effect | a working version, an A/B test | weeks–months | outcome |
| Scaling | scale: is the effect stable, does it pay off | economic efficiency | full rollout, marketing switched on | months–quarters | outcome + ROI |
The absence of phases is a signal of weak planning: without them you get "half a year of development → the wrong effect → restructuring".

**Output and outcome.** The outcome (retention, revenue, LTV) lags behind: an action → in 1–2 weeks you see the output (CTR of the block) → in 1–2 months retention starts moving → in 3–6 months the business. Output is a fast proxy: it shows the direction but does not prove impact on the outcome, which is why at validation the goal is the outcome. The outcome metric never disappears: it is the "contract" with stakeholders; at the pilot the goal is output, at validation it is the outcome, at scaling it is outcome + ROI.

**The right to fail is planned, not requested.** The buffer for mistakes is built into the roadmap itself, agreed with leadership in advance, has a time-box and a cap on resources; failure criteria and a plan B exist. A hypothesis failing is a planned outcome, not a catastrophe.

**The management contract (a course example).** Bet: personalizing recommendations for a marketplace. Metric: share of repeat purchases within 15 days 22% → 27% over 6 months. The ambition is 27%; acceptable is 25% (the economics still converge, so fewer resources are allocated); below 25% — the bet is closed and the resource is reallocated. Pilot of 2–4 weeks with the current team: rule-based recommendations, output — CTR of the block above a threshold; if below, plan B (CRM triggers, a new pilot). Validation of 2–3 months: a full system, an A/B test, outcome +2 pp significant; if not — closure. Scaling of 2–3 months: full rollout, marketing, ROI, 27% (25% acceptable).

**The "bets × phases × months" format** (the grid from the course practice) — each bet occupies a block of rows:
| Column | What is written there |
|---|---|
| Bet / Phase / Milestone | the bet's row and the nested rows of its phases (Pilot → MVP → Scale or Discovery → MVP → Scale) |
| Resource | the concrete staffing and load per phase ("2 BE, 1 FE, analyst 50%, designer outsourced"), not "the development team" |
| Outcome metric | baseline → goal + a review threshold ("if after 3 months <+10% → adjust") |
| Output metric | the threshold for the phase gate + plan B ("CTR <1% → rethink the UX", "<+3% CR → simplify (plan B)") |
| Dependencies / hiring | counterparts and vacancies with months ("3 devs: hiring M2→M5") |
| Comment | the bet's type (quick win / big bet) and horizon, parallelism with other bets |
| Months 1–12 | two-week bars marking the active phase |

Bets of different scale coexist in a single plan: quick wins (a horizon of ~3 months, a visible contribution to the current quarter) and big bets (6–12 months, a Discovery phase kept on thin resources until confirmed). Shared resources are visible in the grid: if two bets share one backend, the load is split explicitly ("BE: 30% capacity, 70% — on bet 2"). **Hiring tracking** is kept on a separate row: search → offer → onboarding for every vacancy, with months; phases that depend on a hire shift together with it instead of "believing" in the ideal date.

**The contribution of initiatives to the overall result.** In the strategy implementation plan, every initiative carries an expected contribution to the target metrics in percent (the sum ≈ 100%) — this makes priorities measurable and lets you answer honestly the question "which stream drives growth". Alongside the product initiatives, separate tracks run in parallel (partnerships, BD, marketing), and these must not "fall out" of the roadmap.

**Seasonality in the plan.** Three rules: (1) mass launches and effect measurements happen in the peak demand season; out of season you do preparation, integrations, and keeping the offer visible; (2) promo and growth mechanics are launched **before** the trading season starts (sellers must have time to join: in the course example, weeks before the season begins); (3) in the card of every bet, mark the season into which the outcome measurement falls, and do not make decisions based on a "dead" season without an adjustment. More on seasonality risks — [[M-risks]].

**Resources are part of the strategy.** If you have 2 developers and 1 designer, you cannot run four strategies in parallel. Resource constraints: the team, hiring, dependencies, technology, competencies.
- Hiring is a long chain (vacancy → search → interviews → offer → start date → onboarding); the course benchmarks are 3–6 months to hire and 1–3 months of onboarding (in the lecture notes — "6 or more"), not an SLA; for a resource needed in Q3, start thinking in Q1.
- The mature approach: run the pilot on current resources; expand only after confirmation; search for people in parallel; alternatives — cut the scope, outsource, move the phase. Two extremes to avoid: "freeze everything until we hire" and "plan as if people were already hired".
- Dependencies: platform, technology, organizational (marketing, legal, support), human. Keep a registry: bet, dependency, team, approval status, risk, mitigation.
- Bets compete with each other (short-term revenue vs retention and infrastructure); company context affects priority (if the company is "chasing" revenue, long-term bets get de-prioritized). Choosing one bet means giving up another; the roadmap shows which bet is #1 and what has been deferred.

## Procedure
1. **Take the bets** from `M-goals-drivers-bets` with their effect and effort estimates.
2. **For each bet set the outcome metric** (baseline → goal → deadline), an "acceptable" level, and the closing threshold.
3. **Split it into phases**: for the pilot choose an output proxy and the minimal means; state what counts as a qualitative signal.
4. **Set the time-boxes** and the **numeric gate criteria** for every phase; for each phase — a stop signal and a plan B.
5. **Build the dependency registry** and agree priorities with the owners; dependent teams go into the agreements table (`M-risks`).
6. **Determine the resources and hiring**: who is here now, what will be needed later, which alternatives exist if a hire falls through; fold hiring into the timelines and the traction model (`M-team`).
7. **Set the priorities and the trade-offs**: which bet is #1 and why, which ones we defer and why, how company context changes the order.
8. **Lay it out by quarters**: what is in Q1, Q2…, what is deferred; scenarios "if it doesn't work" and "if the resource is not hired".
9. **Run the completeness checklist** and align it with stakeholders (DACI); set a review date.

## Template / checklist
**A bet card in the roadmap**
| Field | Example |
|---|---|
| Bet | improve retention through recommendation personalization |
| Phase | pilot |
| Outcome metric | share of repeat purchases within 15 days: 22% → 27% (acceptable ≥25%) |
| Output metric | CTR of the recommendations block above a set threshold |
| Timing (time-box) | 4 weeks |
| Dependencies | data preparation by the platform team (agreed / not agreed) |
| Gate criterion | CTR above the threshold → validation; not → plan B (CRM triggers) |
| Stop signal | after 6 months < 25% → the bet is closed, the resource is reallocated |
| Resources | the current team; expansion after validation |

**Completeness checklist** (must answer "yes" to every question)
- [ ] The bet is tied to an outcome
- [ ] The phases are defined, and each phase has its own metric (output proxies in the early ones)
- [ ] Every phase has a time-box
- [ ] Dependencies are identified and agreed
- [ ] The gate criteria are numeric; a stop signal is defined; a buffer for failure and a plan B are built in
- [ ] It is stated who makes the gate decision
- [ ] It is shown what has been deferred and why
- [ ] Hiring and alternatives are accounted for in the timelines
- [ ] The stakeholders have agreed on the elements

## Typical mistakes
- A roadmap that is a feature list; no phases; no dependencies; output not linked to outcome; no gates and no stop conditions.
- Endless testing: "we need more data" without a stop criterion.
- A pilot three months long that involves serious development (that is not a pilot).
- One outcome metric shared by all phases: you wait months for the feedback.
- "First we'll come up with the strategy, find the resources later"; a strategy that requires 20 developers who do not exist.
- A single region for a regional pilot; a pilot without a criterion for "what counts as a signal".
- A roadmap used as a promise rather than a tool of choice: no room left for change; the "right to fail" is requested only after the failure.
- It is invisible what has been de-prioritized, and nobody explained why.

## Questions that can change the decision
- What minimal signal within 2–4 weeks will show whether it is worth continuing (which output proxy and threshold)?
- Is there a proven output → outcome link, or is that link itself a hypothesis?
- How much does a mistake cost at each phase, and how much buffer is agreed?
- What happens if a key dependency does not get priority in time?
- Which resource is the key one, will it be in place by the start of the phase, and what do we do if it is not?
- At what result is the bet considered closed, and who approved that threshold?
- Which demand season does the outcome measurement fall into, and could the season force the phases or the validation to move?
- What happens if we do nothing (the inertial scenario for the metric)?

## Related maps
[[M-strategy-growth]], [[M-goals-drivers-bets]], [[M-risks]], [[M-success-metrics]], [[M-team]], [[M-mvp-pilots]], [[M-pmf-scaling]], [[M-traction-model]], [[M-decision-daci]]
