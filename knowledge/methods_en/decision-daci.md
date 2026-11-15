---
id: M-decision-daci
lang: en
title: DACI and the decision log — roles, owners, revisit conditions
course: pm
sources: ["EN mirror of the RU methodology card M-decision-daci (knowledge/methods/decision-daci.md); original sources are listed in the RU card"]
stages: [strategy, validation, after-decision]
tags: [daci, decision, roles, accountability, decision-log, stakeholders, revisit, revisit-criteria]
related: [M-product-communication, M-roadmap, M-team, M-risks, M-solution-design, M-mvp-pilots, M-pmf-scaling, M-delivery, M-goals-drivers-bets]
---

# DACI and the decision log

## When to use
You need to assign who on and around the team does what, and who makes the decision at each stage of the product; and to record a specific decision so that a quarter later it is possible to understand why it was made, who is accountable, and under what conditions it should be revisited.

## Core idea
**DACI** — a role matrix for decisions and activities:
| Role | Meaning |
|---|---|
| **D — Driver** | Drives the activity/decision to a result, gathers the inputs, pushes for deadlines |
| **A — Approver** | Approves; the final word. Ideally one person |
| **C — Contributor** | Provides expertise and work, influences the content |
| **I — Informed** | Learns of the result, no influence |

The decision matrix is part of the product perimeter artifacts (alongside the stakeholder map and the dependency list). Accountability ≠ control: some decisions are made outside the perimeter, and the Approver may sit outside the team.

**Role allocation in a product team (the Avito Design template):** rows — stages and activities, columns — D/A/C/I. Typical Drivers:
- **Search for problem hypotheses:** research on the market and competitors, reviewing studies, talking to stakeholders, user interviews, formulating hypotheses — Driver: the PM (Contributors: researcher, designer, analyst); analysis of current CJM and flows — Driver: the designer (Informed — PM).
- **Problem validation:** synchronization with other teams — PM; Voice of the Customer analysis (support, channels) — researcher (Contributors: PM, analyst); qualitative studies, quantitative surveys, hybrid (unmoderated) ones — researcher; the analytical calculation for problem validation — analyst; sizing the problem, prioritizing problems, defining metrics (primary, proxy, counter) — PM.
- **Solution design:** generating solution hypotheses — designer (Contributors: PM, researcher); assessing feature potential (Contributor: analyst), prioritizing solutions (analyst, designer, researcher, engineer — Informed), formulating user value (Contributors: analyst, designer, editor, researcher) — Driver everywhere: the PM; the final description of scenarios and corner cases — PM; draft mockups — designer; preparing prototypes for studies and UX tests — researcher; finalizing mockups and copy — designer; sign-off with legal — PM; event logging scenarios and the experiment design (A/B) — analyst; the launch plan with marketing — PM.
- **Solution implementation:** diving into the task, grooming, decomposition, kick-off with verticals/horizontals, roadmap refinement, support policies and articles, sign-off with engineering/legal, review — PM/designer; developing and shipping the feature to production, test checklists, rollout — engineer; running the experiment and interpreting A/B results — **analyst** (Contributor: PM); rollout approval — PM; feedback collection and analysis — researcher; discovery/delivery demos — PM.
Conclusion: the PM is the Driver of prioritization, metrics, sign-offs, and the rollout decision, but not of A/B interpretation (the analyst) and not of development. The Approver column in the template is often left empty — a signal that an Approver must be assigned explicitly for every decision.

**The decision log (decision record)** — the unit of product memory. The course's foundation: the decision memo (goal/ask, problem, solution, PMF criteria, risks, resources, "what decision is needed"), the risk log (probability/impact, owner, SLA, mitigator), the post-mortem (hypothesis → metric/MDE → fact → causes → actions). The principle: a post-mortem without action items is a diary; a decision without an owner and a revisit condition is an opinion.

## Procedure
1. Define the **decision** in one phrase (what we choose between what) and its type: reversible/irreversible, cost of error, timeframe.
2. Assign the roles: one Driver, one Approver, a list of Contributors (who provides data and expertise), the Informed. Check: are there two Drivers, do D and A overlap, does the Approver have authority over budget/priority.
3. Gather the inputs and **separate**: facts (source, date, period), assumptions/hypotheses, forecasts (scenarios). State the alternatives, including "do nothing."
4. Fix the **decision criteria** (metrics, thresholds, budget, deadline) and the **counter-metrics** before the choice.
5. The Approver makes the decision; record the chosen option, the rejected options, and the reasons.
6. Record the **revisit conditions**: which metric values, events (a missed TTM corridor, a red risk, a change in the market/constraints) or date bring the decision back for discussion; who initiates the revisit.
7. Assign the actions: owner, deadline, definition of done; update the roadmap ([[M-roadmap]]) and the risk log.
8. Notify the Informed; on the scheduled date — compare fact with expectation (post-mortem), update the record: confirmed / not confirmed / revisited.

## Template / checklist
```
ID and date: ___   Decision (one phrase): ___   Status: proposed | made | revisited | cancelled
Driver: ___   Approver: ___   Contributors: ___   Informed: ___
Context and goal (metric, baseline, period): ___
Options (including "do nothing"): A ___ | B ___ | C ___ ; selection criteria: ___
What is known (facts + source/period): ___   Assumptions/hypotheses: ___   Forecasts and forecast assumptions: ___
Decision and rationale; rejected options and why: ___
Expected change (metric, magnitude, observation period) and success criteria: ___
Failure / kill criterion and plan B: ___   Counter-metrics and thresholds: ___   Side effects we look for: ___
Risks (probability × impact, owner, SLA): ___
Revisit conditions (metric/event/date) and who initiates: ___
Actions: what — who — by when — how we know it is "done": ___
Fact-check date / post-mortem: ___
```
Checklist: there is one Approver · the Driver does not coincide with the Approver without reason · facts/hypotheses/forecasts are distinguished · the "do nothing" alternative is present · criteria and thresholds are set before the decision · revisit conditions are specified · actions have owners and deadlines · the Informed received the record.

## Typical mistakes
- No Approver assigned (the column is empty) or the Approver is "everyone"; two Drivers on one activity.
- Roles tied to job titles rather than decisions: for different decisions the Approver is different.
- The decision recorded without alternatives and reasons for rejection; a quarter later the logic cannot be reconstructed.
- The record has no revisit condition: the decision becomes dogma or, conversely, is revisited on a whim.
- The PM interprets the A/B result instead of the analyst (or the analyst approves the product decision).
- Contributors added "just in case"; the Informed substitute for sign-off.
- A post-mortem as a blame hunt, without action items and without updating assumptions.
- The decision made verbally at a meeting and not recorded ("everyone remembers it anyway").

## Questions that can change the decision
- Who has authority over budget/priority and can actually be the Approver?
- Which dependent teams must be Contributors, otherwise the decision will not be implemented?
- Is the decision reversible (feature flag, pilot) — can it be made faster and revisited later?
- Which events (metrics, a missed deadline, a risk) should automatically send the decision back for revisit?
- What would we need to know to change the decision — and who is responsible for that?

## Related cards
[[M-product-communication]], [[M-roadmap]], [[M-team]], [[M-risks]], [[M-solution-design]], [[M-mvp-pilots]], [[M-pmf-scaling]], [[M-delivery]], [[M-goals-drivers-bets]]
