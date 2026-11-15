---
id: M-delivery
lang: en
title: Delivery — from scope to release: what to account for when committing to a plan
course: pm
sources: ["EN mirror of the RU methodology card M-delivery (knowledge/methods/delivery.md); original sources are listed in the RU card"]
stages: [strategy, validation, after-decision]
tags: [delivery, scope, moscow, rice, acceptance-criteria, release, a-b-test, dora, feature-flags, canary, release-train, alerts, dependencies, capacity, security]
related: [M-roadmap, M-mvp-pilots, M-solution-design, M-product-metrics, M-decision-daci, M-risks, M-team, M-product-communication]
---

# Delivery: what you need to know when committing to a plan

## When to use
When a strategy or roadmap includes deadlines and effects: to assess realism, to understand which roles and stages sit between "the hypothesis is validated" and "the value metric changed in production," and not to promise more than the process can sustain. A short map: without the details of Scrum/DevOps.

## Core idea
- **Delivery** — the process of building and shipping the product: it starts when, after Discovery, the feature scope has been formed, and it ends when the value metric "moves" in production. Discovery answers "why and what," Delivery — "how, when, and with what risk" — and verifies that the "why" actually happened. The whole team participates in Delivery, including the PM; business analysis is the seam between Discovery and Delivery.
- **Stages and time benchmarks (from the lecture):**
| Stage | Output | Time benchmark |
|---|---|---|
| Prioritization and scope estimation (MoSCoW, RICE) | The scope split into iterations, the MVP/MLP identified, a target deadline set | 2 days – 1 week |
| Documentation and design | Requirements in the form of user stories, the technical approach agreed, handed to engineering | 2 days – 1.5 months |
| Development and testing | Part/all of the feature built, reviewed, tested | from 1 week, no upper bound |
| Release | The feature in production behind a flag/an A/B or at 100% | ~1 day |
- At the prioritization stage, 30–70% of the functionality from Discovery may be cut off. **MoSCoW:** Must (the first queue, "would the business collapse without this in the next ~6 weeks?"), Should, Could, Won't. The rule of thumb from the notes: Must — no more than ~40% of what the team can physically build in 1–2 sprints. **RICE** = Reach × Impact × Confidence / Effort; Effort is estimated only by engineering and QA, not the PM. The cut-line: past it, nothing is added without recomputing value; a new "urgent" idea is compared through RICE and the Cost of Delay.
- **Documentation:** a user story ("As a [who], I want [action] so that [outcome]") + acceptance criteria (Given-When-Then / "condition → action → result"), each verifiable with only a yes/no answer; exceptions and corner cases described; **the analytics event is part of the specification** — otherwise the feature is "blind." "Ready for Dev": the story and criteria final, the mockups, the API specs, the events and the dashboard, the PM's sign-off.
- **Development:** the team works in sprints (Scrum, 1–2 weeks) or in flow (Kanban, releases every 3–5 days); the dependency chain: without business requirements there are no test cases, without test cases you cannot develop, without tests you cannot release; complex products coordinate releases with adjacent teams and release windows. The release is not "every day" if the product spans several services.
- **Release:** the artifacts — release notes/the release ticket, the design of the A/B test (conditions and expected effect), ready dashboards. 5 rules: do not ship a large release on Friday; everything in production is instrumented with events and covered by alerts; separate the releases of large features so that effects do not mix; risky features only behind an A/B, non-risky ones also behind an A/B to measure the effect; not all bugs are critical, whatever the team says — verify yourself.
- **Feature flags (three types):** a release flag (hides unfinished work, TTL 1–2 sprints, otherwise it becomes tech debt), an experiment flag (splits traffic for an A/B, lives until the test ends), an operational flag (the "red button" — instantly turn off part of the system during an incident). The flag key lives in a config table and is switched without a code revert. **Canary rollout:** 5% → 20% → 100% at ~30 minutes per step; on a latency/5xx alert — automatic rollback; 100% of traffic — during the day, not on Friday evening. After 24 hours without red alerts the flag is turned on for everyone. With a flag, rollback is a button, not an overnight git rollback.
- **When to A/B and when to ship right away (the price of a minute against the price of an error):** a small UX tweak — deserves an A/B (the risks are small, but a p-value is needed); a fix for a critical bug — shipped immediately (the damage from downtime exceeds the cost of a possible rollback); a pricing change — checked carefully and longer (you need to see the LTV and the customers' reaction). The PM decides.
- **An alert is a language of actions, not a red light:** every alert has an owner (an owner:@name field, with auto-escalation during vacations); an ownerless alert is closed after 30 days ("if the metric matters — assign someone responsible"); alerts are grouped by type (latency, financial, UX) and false positives are muted. NPS dropped overnight, the alert went into a dev channel and nobody pinged the PM — a typical failure when there is no owner field.
- **The first 24 hours — four segments:** the first 30 minutes — smoke-test the main scenarios in production; the first hour — a quick cut of the funnel, the PM watches GMV-per-minute, flag to OFF on any anomaly; up to 6 hours — the automated alerts do the work, on-call answers only the question "rollback or fix?"; by 24 hours — a 5-minute "micro-retro" (what to improve in the process before the next release). Watch three groups of signals: technical (latency, CPU, 5xx), product (conversion, clicks), and business metrics (GMV, NPS). "Release isn't done until numbers sing" — Delivery ends when one of three things is clear: the value is proven → scale it; it is doubtful → iterate; it is negative → roll back and form a new hypothesis. Then — a post-release review with action items; in the review — "five whys" down to a system error, not to a culprit (the photo did not upload → the validator let 0 bytes through → the test case did not check an empty file → the AC had no item about size → it slipped through spec review → add a checklist item and an automated test).
- **Delivery health metrics:** Lead Time for Changes, Deployment Frequency, Change Failure Rate, MTTR (DORA); the business layer — On-Time Delivery %, Escaped Defect %, Cost of Delay Saved. Collected automatically; "false improvements" — splitting releases to boost frequency, rollbacks without a tag, bugs hidden behind flags. Answers to 4 questions: how fast an idea becomes value; how many bugs reach the user; how fast we react to a breakage; how many releases land on time.
- **Metrics into actions ("metric → diagnosis → prescription"):** an indicator in the yellow zone for two sprints in a row → in the next sprint, 10% of capacity goes to fixing the process. Once a quarter — Delivery planning: trends → bottlenecks → a goal of the form "raise API coverage from 55 to 75%" → story-points for infrastructure in the capacity. ~10% of velocity is reserved for process tasks permanently, otherwise the metrics are decoration. The boundary of optimization: if the Change Failure Rate grows faster than the Lead Time falls — stop (tests and reviews are being bypassed). Infrastructure investment is sold to the CFO through ROI: "an automated-test cluster at 200K RUB/month saves 1.3M RUB of GMV losses from rollbacks".
- **Delivery Health Index (DHI)** — an aggregate: the share of on-time releases, escaped defects, the reaction speed to alerts, the share of regression checks without issues. The yellow zone for 3 months → a process program; red at the MBR → a "red card" for the cluster and a "freeze" on non-market experiments until it is back in the yellow.
- **Several teams:** the "between-features" problem — five teams independently ship a small improvement each, totaling +12% latency and −8% GMV. Three models: **Release Train** (a shared "train" — predictable for regulators and the CFO, but "did not make it" = a week of waiting), **pure Continuous** (value lands instantly, but one conflict wrecks the portfolio), **the platform hybrid** — the core (billing, authorization, search) rides the train, the frontends and ML services live in continuous flow. Rituals: a shared release calendar (everyone books a "want on the train" slot, everyone sees when the "tracks are occupied"); a dependency matrix as a "metro map" (lines — services, stations — API versions: the switch to v3 is flagged in advance, before date X); the regulatory gate Reg-Gate before the train (PAN masking, audit logs, dependency licenses — one "no" and the train stands); a release readiness meeting (R²M) two days ahead — the PM says Go/No Go, because their metrics are on the line; follow-the-sun on-call for distributed teams. The PM books the slot in the calendar, removes the release-blocker tag, brings the regulatory documents, and watches the business alerts in their own time zone.
- **Security as a Delivery customer ("security left"):** security requirements are placed into the specification next to the design checklists (data masking in the AC, a negative test "unauthorized request → 401"), automation in CI (a secret scanner, dependency analysis, static analysis), a permanent security backlog of 10–15% capacity on the shared board with the same DoD. The PM is the translator between "expensive and slow" and "how much a breach costs" (Cost of Delay × fine).
- **Roles:** the PM — priority, metric, the answer "rollback or wait"; the business/systems analyst — requirements, API, events; the designer — mockups/the design system; the team lead/delivery manager — time estimates, the backlog, dependencies; QA — test cases; the team — development and testing. Role allocation — [[M-decision-daci]].

## Procedure (how to use it when building a commitment)
1. Take the prioritized hypothesis and the MVP/MLP scope ([[M-mvp-pilots]]). Separate Must from the rest; cross out anything that does not affect the metric being tested.
2. Request an **estimate** from engineering and analytics (Effort, time, dependencies, blockers); do not substitute the PM's own estimate. If there is no estimate — write a range and a note "forecast, not confirmed by the team".
3. Match against capacity (sprints, holidays, release windows, feature freeze, time for the A/B) and cross-team dependencies (legal, security, adjacent APIs). Account for the fact that an A/B requires sample-collection time beyond development.
4. Make sure the scope includes: the analytics events and the dashboard, the design of the A/B, the approvals (legal, security, support), the rollback criteria, the launch behind a flag.
5. Set the **post-release decision criteria**: the success threshold, counter-metrics, the observation window (e.g., the first 24 hours for technicals and weeks for the A/B), what counts as a rollback.
6. Record in the roadmap: the stage, the owner, the dependency, the deadline, the milestone, the decision at the milestone ([[M-roadmap]]); mark estimates and assumptions as forecasts.
7. After the release — reconcile fact with plan: time, effect, counter-metrics; action items into the process.

## Template / checklist
```
Feature / hypothesis: ___   Scope: Must ___ | Should ___ | Won't ___ (cut-line)
Estimate (dev+QA): ___ person-weeks, range ___ ; source of the estimate: ___ ; status: forecast|confirmed by the team
Dependencies/approvals: ___ ETA ___   Release window / feature freeze: ___
Analytics events and dashboard: ready? yes|no   A/B design (metric, period, control): ___
Success criterion: ___ ; counter-metrics and thresholds: ___ ; rollback conditions: ___
Post-observation decision: scale | iterate | roll back — by whom and when: ___
```
Checklist: the scope is cut down to MVP/MLP · the estimate comes from the implementers · dependencies and windows are accounted for · analytics and alerts are in the specification · acceptance criteria are verifiable yes/no · the A/B is budgeted · the owner of the rollout/rollback decision is known.

## Typical mistakes
- Shipping a "blind" feature without analytics events; launching on Friday evening without alerts.
- Stuffing "nice-to-haves" into the sprint ("we will be doing this for two years"); Must = "everything"; floating acceptance criteria.
- The PM estimates the effort themselves; the roadmap is built without estimates and without release windows.
- Mixing the releases of large features, so that the effects cannot be separated.
- Believing Delivery is not the PM's concern; stopping at deploy instead of waiting "for the numbers to sing".
- Not budgeting time for the A/B, approvals, support, and rollback.
- Taking speed (release frequency) as the goal instead of value (On-Time, Escaped Defects).
- An alert without an owner and an action — the signal is seen but nobody responds; a release flag lives forever and turns into tech debt.
- An indicator in the yellow zone for two sprints — and "we will fix it someday"; process tasks never make it into the sprint backlog.
- Each team separately ships "green" releases, but the aggregate effect hits latency and GMV — there is no shared calendar and dependency map.

## Questions that can change the decision
- Who from engineering/analytics confirmed the time and scope? Which blockers and external dependencies remain?
- Are there release windows, feature freezes, or regulatory gates that constrain the date?
- Is there enough traffic and time for the A/B to decide on the effect before the next milestone?
- What does the team roll back, and who makes that call at night?
- What is the cost of delay compared to the cost of an error: is it worth shipping without an experiment (a critical bug) or mandatory with one (pricing)?

## Related cards
[[M-roadmap]], [[M-mvp-pilots]], [[M-solution-design]], [[M-product-metrics]], [[M-decision-daci]], [[M-risks]], [[M-team]], [[M-product-communication]]
