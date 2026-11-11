---
id: M-decision-daci
lang: en
title: DACI and the decision journal — roles, owners, revision conditions
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [strategy, validation, after-decision]
tags: [daci, decisions, roles, accountability, decision-journal, stakeholders, revision, revision-criteria]
related: [M-product-communication, M-roadmap, M-team, M-risks, M-solution-design, M-mvp-pilots, M-pmf-scaling, M-delivery, M-goals-drivers-bets]
---

# DACI and the decision journal

## When to apply
You need to assign who on and around the team does what, and who makes the decision at each stage of the product; and to record a concrete decision so that a quarter later it is still possible to understand why it was made, who is accountable, and under which conditions it should be revisited.

## Core idea
**DACI** — a role matrix for decisions and activities:
| Role | Meaning |
|---|---|
| **D — Driver** (the person responsible) | Drives the activity/decision to a result, gathers the inputs, pushes for deadlines |
| **A — Approver** (the customer) | Approves; has the last word. Ideally one person |
| **C — Contributor** (executor/consultant) | Brings expertise and work, influences the content |
| **I — Informed** (kept informed) | Learns about the result, has no influence |

The decision-making matrix is part of the product perimeter artifacts (alongside the stakeholder map and the list of dependencies). Accountability ≠ control: some decisions are made outside the perimeter, and the Approver may sit outside the team.

**Role distribution in a product team (Avito Design template):** rows are stages and activities, columns are D/A/C/I. Typical Drivers:
- **Search for problem hypotheses:** market and competitor research, studying research reports, talking to stakeholders, user interviews, formulating hypotheses — Driver: the product manager (Contributors: researcher, designer, analyst); analyzing the current CJM and flows — Driver: the designer (Informed: the product manager).
- **Problem validation:** synchronization with other teams — product manager; Voice of the Customer analysis (support, channels) — researcher (Contributors: product manager, analyst); qualitative research, quantitative surveys, hybrid (unmoderated) studies — researcher; analytical calculation for problem validation — analyst; estimating the scale of the problem, problem prioritization, defining metrics (primary, proxy, counter) — product manager.
- **Solution design:** generating solution hypotheses — designer (Contributors: product manager, researcher); estimating feature potential (Contributor: analyst), prioritizing solutions (analyst, designer, researcher, developer — Informed), formulating user value (Contributors: analyst, designer, editor, researcher) — Driver everywhere: the product manager; the final description of scenarios and corner cases — product manager; draft mockups — designer; preparing prototypes for studies and UX tests — researcher; finalizing mockups and copy — designer; sign-off with legal — product manager; logging scenarios and experiment (A/B) design — analyst; the launch plan with marketing — product manager.
- **Solution implementation:** diving into the task, grooming, decomposition, kick-off with verticals/horizontals, refining the roadmap, support regulations and articles, sign-off with tech/legal, review — product manager/designer; developing and delivering the feature to production, testing checklists, rollout — developer; running the experiment and interpreting A/B results — **the analyst** (Contributor: product manager); approving the rollout — product manager; collecting and analyzing feedback — researcher; disco/delivery demos — product manager.
Takeaway: the product manager is the Driver of prioritization, metrics, approvals and the rollout decision — but not of A/B interpretation (that's the analyst) and not of development. The Approver column in the template is often left empty — a signal that an Approver must be assigned explicitly for each decision.

**The decision journal (decision record)** — the product's unit of memory. The course foundation: a decision memo (goal/ask, problem, solution, PMF criteria, risks, resources, "which decision is needed"), a risk log (probability/impact, owner, SLA, mitigator), a post-mortem (hypothesis → metric/MDE → fact → causes → actions). The principle: a post-mortem without action items is a diary; a decision without an owner and a revision condition is an opinion.

## Procedure
1. State the **decision** in one sentence (choosing what between what) and classify it: reversible/irreversible, cost of error, deadline.
2. Assign roles: one Driver, one Approver, a list of Contributors (who brings data and expertise), Informed. Check: is there a second Driver, do D and A overlap, does the Approver have authority over budget/priority.
3. Gather the inputs and **separate** them: facts (source, date, period), assumptions/hypotheses, forecasts (scenarios). List the alternatives, including "do nothing".
4. Fix the **decision criteria** (metrics, thresholds, budget, deadline) and the **counter-metrics** before the choice is made.
5. The Approver makes the decision; record the chosen option, the rejected options and the reasons.
6. Write down the **revision conditions**: which metric values, events (a missed TTM corridor, a red risk, a change in the market or constraints) or date will return the decision to discussion; who initiates the revisit.
7. Assign actions: owner, deadline, definition of done; update the roadmap ([[M-roadmap]]) and the risk log.
8. Notify the Informed; on the appointed date compare the fact with the expectation (post-mortem), update the record: confirmed / not confirmed / revised.

## Template / checklist
```
ID and date: ___   Decision (one sentence): ___   Status: proposed | accepted | revised | cancelled
Driver: ___   Approver: ___   Contributors: ___   Informed: ___
Context and goal (metric, baseline, period): ___
Options (including "do nothing"): A ___ | B ___ | C ___ ; choice criteria: ___
What is known (facts + source/period): ___   Assumptions/hypotheses: ___   Forecasts and the forecast's assumptions: ___
The decision and its justification; rejected options and why: ___
Expected change (metric, magnitude, observation period) and success criteria: ___
Failure criterion / kill and plan B: ___   Counter-metrics and thresholds: ___   Side effects we look for: ___
Risks (probability × impact, owner, SLA): ___
Revision conditions (metric/event/date) and who initiates: ___
Actions: what — who — by when — how we know it's "done": ___
Result check-in date / post-mortem: ___
```
Checklist: there is one Approver · the Driver is not also the Approver without a reason · facts/hypotheses/forecasts are distinguished · the "do nothing" alternative is present · criteria and thresholds are set before the decision · revision conditions are stated · actions have owners and deadlines · the Informed have received the record.

## Typical mistakes
- No Approver assigned (the column is empty) or the Approver is "everyone"; two Drivers on one activity.
- Roles tied to job titles rather than to decisions: for different decisions the Approver is different.
- The decision recorded without alternatives and reasons for rejection; a quarter later the logic cannot be reconstructed.
- The record has no revision condition: the decision turns into dogma or, conversely, gets revisited on a mood.
- The product manager interprets the A/B result instead of the analyst (or the analyst approves a product decision).
- Contributors added "just in case"; the Informed substitute for real approval.
- A post-mortem as blame-hunting, without action items and without updating the assumptions.
- The decision is made verbally in a meeting and never recorded ("everyone remembers it anyway").

## Questions that can change the decision
- Who has authority over budget/priority and can genuinely act as the Approver?
- Which dependent teams must be Contributors, otherwise the decision cannot be implemented?
- Is the decision reversible (a feature flag, a pilot) — can it be accepted faster and revisited later?
- Which events (metrics, a missed deadline, a risk) should automatically return the decision for revision?
- What would we need to know to change the decision — and who is responsible for finding it out?

## Related maps
[[M-product-communication]], [[M-roadmap]], [[M-team]], [[M-risks]], [[M-solution-design]], [[M-mvp-pilots]], [[M-pmf-scaling]], [[M-delivery]], [[M-goals-drivers-bets]]
