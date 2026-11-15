---
id: M-roadmap
lang: en
title: Roadmap — how it is structured, how it is built and how it is quality-checked
course: pm
sources: ["EN mirror of the RU methodology card M-roadmap (knowledge/methods/roadmap.md); original sources are listed in the RU card"]
stages: [strategy, validation, after-decision]
tags: [roadmap, okr, prioritization, dependencies, capacity, milestones, risks, moscow, rice]
related: [M-outcome-roadmap, M-goals-drivers-bets, M-problem-design, M-solution-design, M-mvp-pilots, M-pmf-scaling, M-risks, M-product-communication, M-delivery, M-team, M-decision-daci]
---

# Roadmap

## When to apply
You need to turn the strategy and a set of hypotheses into a plan over time: what, in what order, who, with which metrics and decision points. Also — assessing someone else's roadmap for feasibility, dependencies and measurability. Here a roadmap is treated as a strategic document, not a feature list.

## Essence
- A roadmap aligns the business vision with tactical steps, synchronizes participants and structures key stages and tasks. Two main areas: (1) product and technical development — where and how P&T resources are invested and what effect is expected; (2) synchronization of interdependencies with other teams (marketing, sales, adjacent products).
- Benefits: transparency and fewer delays; prioritization and communication; flexibility under market changes; performance management (minimizing risks, reallocating resources).
- **Elements:** (1) vision and goals; (2) key initiatives/stages; (3) milestones; (4) decomposition into tasks; (5) owners and resources; (6) timelines (quarters, months, sprints); (7) links and dependencies; (8) success metrics / expected result.
- **Types:** thematic (by direction; at high uncertainty), timeline-based (by dates; classic IT), specific (UX/UI, mobile, integrations), cross-functional (several departments), technical (infrastructure, tech debt). The choice depends on the stage (launch — flexibility and fast iterations; maturity — optimization and maintenance), the business model (B2B — more detailed and longer; B2C — more flexible) and the product type (traditional — more linear; technological — frequent revisions).
- **Detail by stage:** idea — high level of abstraction; development — detail and dependencies; pilot — testing tasks and quick fixes; scaling — resource planning, calendaring and team alignment.
- **Frameworks:** Agile roadmapping, OKR, Lean roadmapping, Impact Mapping, Business Model Canvas.
- **OKR:** Objective — an inspiring direction, not a metric, ambitious (a guideline of 50% probability of achievement); Key Result — measurable (SMART), not a feature or a task, shows whether we are moving toward the goal. The chain: long-term strategy → yearly goals → quarterly OKRs → synchronization between units. The lecture cites a headroom rule of "0.9 of the yearly goal = 0.7 of OKR". Goals are transparent to everyone and achieved jointly.
- **Problem-based (outcome-based) roadmap:** rows are problems/outcomes, not features: problem, symptom metric (baseline), status (Discovery / In progress / Done), planned release, owner, links to the dashboard and interviews. A hypothesis confirmed → the status changes; it did not work → the hypothesis is revised.
- **A 12-month scaling roadmap:** a "months × stages" table with quarterly milestones (Discovery → MVP → PMF proof → the "start scaling" Gate → final review); in a cell — hypothesis → validation method → expected metric/threshold; a row of 5 fields: stage, hypothesis/goal, tasks, metric + threshold, owner + date.

## Procedure
1. **Goal.** Write out the product's vision/mission and 1–3 goals for the period (OKR). Check that every KR has a baseline, a threshold and a deadline.
2. **Input.** Collect ideas and requirements from product, engineering, design, analytics, support, marketing and external "bottlenecks" (legal, moderation, DS, infrastructure). The source of every initiative is a problem or hypothesis from [[M-problem-design]]/[[M-solution-design]].
3. **Resources.** Estimate each team's capacity (person-weeks, available days of the quarter, days off/holidays) and historical velocity; effort estimates come from engineering and QA, not from the PM.
4. **Prioritization.** Roughly — MoSCoW (Must/Should/Could/Won't), then RICE; constraint: Must — no more than ~40% of the actual volume for 1–2 sprints. Cut ("No" is a PM tool); record what we do NOT do and why.
5. **Structure.** Choose the roadmap type; plan 1–2 quarters in detail, further out — in large themes. For each initiative specify: hypothesis, validation method, metric+threshold, owner, date, dependencies (including external ones, with ETA), risks and mitigation.
6. **Decision points.** For each milestone record: which decision is made (proceed / refine / stop), by which criterion, who decides ([[M-decision-daci]]). This is what distinguishes a roadmap from a task list.
7. **Buffers and the critical path.** Reserve headroom for force majeure and new Discovery insights (a lecture guideline: 10–15% of time and 1–2 sprints for risks); highlight the critical path and the peak load of roles (QA, backend).
8. **Alignment.** Discuss with the executors and key stakeholders (buy-in); keep a "public" and an "internal" (with risks) version; keep a single master roadmap.
9. **Revision rhythm.** Review once a month/quarter; after a quarter — what succeeded, what did not, why the slips. Change is the norm, not a failure.

### Roadmap evaluation criteria (rubric, 7 criteria)
1. Logic and realism of stages (2 points) — no unexplained pauses, timelines hold against capacity.
2. Clear binding of hypotheses to stages (2) — it is clear which hypothesis is validated when; a problem hypothesis is not validated in parallel with a solution for an as-yet-unconfirmed problem without reason.
3. Dependencies and the critical path (2): 0 — dependencies not specified; 1 — 1–2 without a full picture; 2 — key dependencies within and between teams, the critical path, external factors.
4. Roles, teams, alignment points (1) — not "engineering" in general but concrete roles; at forks it is visible who participates (marketing, support).
5. Risks and measures (1) — 2–3 key risks (product, team, external), blocking/non-blocking, a realistic mitigation plan.
6. Metrics and checkpoints tied to decisions (1) — for each milestone: the metric and the decision made on it.
7. Presentation quality (1) — readable, structure, legend, no overload.
Additionally check: whether specific teams are overloaded in the same weeks; whether there is idle time.

## Template / checklist
```
Initiative / problem: ___   Goal (OKR/KR, baseline → target, deadline): ___
Hypothesis and validation method: ___   Metric + threshold (MDE / success criterion): ___
Owner/teams and roles: ___   Start–finish, milestone: ___
Dependencies (internal/external, ETA): ___   Critical path: yes | no
Risk → mitigation → "red button" trigger: ___
Decision at the milestone: proceed | refine | stop (criterion): ___
Data status: fact | hypothesis | forecast
```
Checklist: linked to the strategy · priorities are clear · milestones, timelines, owners visible · success is measurable · dependencies and risks accounted for · a revision process exists · the format suits the audience · not overloaded · respects capacity · any new hire understands the direction in ~3 minutes.

## Common mistakes
- No link to the strategy: the roadmap is a "wish list".
- Unrealistic timelines (10 releases in a quarter for 3 people); ignoring capacity and seasonality.
- Over-detail: hundreds of tasks, quickly goes stale. Solution: levels of abstraction (leadership — initiatives, the team — tasks).
- Unaccounted dependencies and blockers; no buffers.
- No metrics and decisions at milestones (in final-work reviews this is a typical loss of points).
- Unsynchronized roadmaps of different teams; a roadmap "born in the PM's head" without buy-in.
- No flexibility: frozen, revised only in a crisis.
- Launching "everything at once" without phasing and without an entry point/channel for the user.
- Validating a solution hypothesis in parallel for a problem not yet confirmed.

## Questions that can change the decision
- What is the real capacity of the teams, and which external teams are critical for the path?
- Which milestones are "go/no-go" points, and by which threshold values?
- What happens to the plan if the key hypothesis fails at the first milestone?
- Which stakeholders must approve the forks so the decision does not collapse later?
- Are there urgent leadership "drop-ins", and how are they built in (what exactly do they displace, what is the cost of delay)?

## Related cards
[[M-outcome-roadmap]], [[M-goals-drivers-bets]], [[M-problem-design]], [[M-solution-design]], [[M-mvp-pilots]], [[M-pmf-scaling]], [[M-risks]], [[M-product-communication]], [[M-delivery]], [[M-team]], [[M-decision-daci]]
