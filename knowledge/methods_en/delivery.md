---
id: M-delivery
lang: en
title: Delivery — from scope to release: what to account for when committing to a plan
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [strategy, validation, after-decision]
tags: [delivery, scope, moscow, rice, acceptance-criteria, release, dora, feature-flags, canary, alerts]
related: [M-roadmap, M-mvp-pilots, M-solution-design, M-product-metrics, M-decision-daci, M-risks, M-team, M-product-communication]
---

# Delivery: what to know when committing to a plan

## When to apply
When the strategy or roadmap includes dates and effects: to assess realism, to understand which roles and stages stand between "the hypothesis is validated" and "the value metric moved in production", and to avoid promising more than the process can bear. A short card: without Scrum/DevOps detail.

## Core idea
- **Delivery** is the process of building and shipping the product: it starts when Discovery has produced the feature scope and ends when the value metric "moves" in production. Discovery answers "why and what"; Delivery answers "how, when and with what risk" and verifies that the "why" actually happened. The whole team takes part in Delivery, including the PM; business analysis is the seam between Discovery and Delivery.
- **Stages and rough timelines (from the lecture):**
| Stage | Result | Rough timeline |
|---|---|---|
| Prioritization and scope estimation (MoSCoW, RICE) | Scope split into iterations, MVP/MLP identified, a deadline goal set | 2 days – 1 week |
| Documentation and design | Requirements as user stories, technical approach agreed, handed over to development | 2 days – 1.5 months |
| Development and testing | Part or all of the feature built, reviewed, tested | from 1 week, no upper bound |
| Release | The feature live behind a flag/in A/B or at 100% | ~1 day |
- At the prioritization stage, 30–70% of the functionality from Discovery can be cut. **MoSCoW:** Must (first queue, "would the business collapse without it in the next ~6 weeks?"), Should, Could, Won't. Rule of thumb from the notes: Must — no more than ~40% of what the team can physically build in 1–2 sprints. **RICE** = Reach × Impact × Confidence / Effort; Effort is estimated only by development and QA, not the PM. The cut-line: past it, nothing is added without recalculating value; a new "urgent" idea is compared via RICE and Cost of Delay.
- **Documentation:** a user story ("As a [who], I want [action], so that [result]") + acceptance criteria (Given-When-Then / "condition → action → result"), each checkable with a yes/no answer only; exceptions and corner cases described; **the analytics event is part of the specification** — otherwise the feature is "blind". "Ready for Dev": story and acceptance criteria final, mockups, API specs, events and dashboard, PM sign-off.
- **Development:** the team works in sprints (Scrum, 1–2 weeks) or in flow (Kanban, releases every 3–5 days); the dependency chain: without business requirements there are no test cases, without test cases you cannot develop, without tests you cannot release; complex products coordinate releases with adjacent teams and release windows. Release is not "every day" if the product spans several services.
- **Release:** artifacts — release notes / a release ticket, the A/B test design (conditions and expected effect), ready dashboards. 5 rules: don't ship a major release on Friday; everything on prod is instrumented with events and covered by alerts; separate the releases of large features so their effects don't mix; risky features only behind A/B, non-risky ones also behind A/B to measure the effect; not all bugs are critical — verify it yourself, whatever the team says.
- **Feature flags (three types):** a release flag (hides unfinished work, TTL 1–2 sprints, otherwise it becomes tech debt), an experiment flag (splits traffic for A/B, lives until the test ends), an operational flag (the "red button" — instantly switch off part of the system in an incident). The flag key lives in a config table and is flipped without a code revert. **Canary rollout:** 5% → 20% → 100% with ~30 minutes per step; automatic rollback on a latency/5xx alert; 100% of traffic during the day, not on Friday evening. After 24 hours without red alerts the flag is turned on for everyone. With a flag, rollback is a button, not an overnight git rollback.
- **When to A/B and when to ship right away (the cost of a minute vs the cost of an error):** a minor UX tweak deserves an A/B (the risks are small, but you need a p-value); a bugfix for a critical error ships immediately (the damage from downtime exceeds the cost of a possible rollback); a pricing change is verified precisely and longer (you need to see LTV and customer reaction). The PM decides.
- **An alert is a language of actions, not a red lamp:** every alert has an owner (an owner:@name field, auto-escalation during vacation); an alert without an owner is closed after 30 days ("if the metric matters — assign someone responsible"); alerts are grouped by type (latency, financial, UX) and false positives are muted. NPS dropped overnight, the alert went to a dev channel and nobody pinged the PM — a typical failure when there is no owner field.
- **The first 24 hours — four segments:** the first 30 minutes — a smoke test of the main scenarios in prod; the first hour — a quick funnel cut, the PM watches GMV per minute, and on an anomaly the flag goes OFF; up to 6 hours — automatic alerts are running, on-call answers only one question: "rollback or fix?"; by 24 hours — a 5-minute "micro-retro" (what to improve in the process before the next release). Watch three groups of signals: technical (latency, CPU, 5xx), product (conversion, clicks) and business metrics (GMV, NPS). "Release isn't done until numbers sing" — Delivery ends when one of three things is clear: value proven → scale it; doubtful → keep iterating; negative → roll back and start a new hypothesis. Then — a post-release review with action items; in the review, run "five whys" down to the systemic error, not the culprit (the photo didn't send → the validator let 0 bytes through → no test case checked an empty file → the AC had no item about size → missed at spec review → add a checklist item and an automated test).
- **Delivery health metrics:** Lead Time for Changes, Deployment Frequency, Change Failure Rate, MTTR (DORA); the business layer — On-Time Delivery %, Escaped Defect %, Cost of Delay Saved. Collected automatically; "fake improvements" — splitting releases to pump up frequency, rollbacks without a tag, bugs hidden under flags. Answers to 4 questions: how fast an idea becomes value; how many bugs reach the user; how fast we react to a breakage; how many releases land on time.
- **Metrics into action ("metric → diagnosis → prescription"):** a metric in the yellow zone for two sprints in a row → the next sprint allocates 10% of capacity to fixing the process. Once a quarter — Delivery planning: trends → bottlenecks → a goal of the form "raise API coverage from 55 to 75%" → story points for infrastructure in capacity. ~10% of velocity is permanently reserved for process tasks, otherwise the metrics are just decoration. The limit of optimization: if Change Failure Rate grows faster than Lead Time falls — stop (tests and reviews are being bypassed). Infrastructure investment is sold to the CFO via ROI: "an automated test cluster at 200k ₽/month saves 1.3M ₽ of GMV lost to rollbacks".
- **Delivery Health Index (DHI)** — an aggregate: share of on-time releases, escaped defects, speed of reaction to alerts, share of regression checks without findings. Yellow zone for 3 months → a process improvement program; red at MBR → the cluster's "red card" and a freeze on non-market experiments until it returns to yellow.
- **Multiple teams:** the "between features" problem — five teams each ship a small improvement independently, and the sum is +12% latency and −8% GMV. Three models: **Release Train** (a shared "train" — predictable for regulators and the CFO, but "missed it" = a week's wait), **pure Continuous** (value instantly, but one conflict wrecks the portfolio), **platform hybrid** — the core (billing, authorization, search) rides the train, while frontends and ML services live in continuous mode. Rituals: a shared release calendar (everyone books a slot "I want on the train", and everyone can see when "the rails are occupied"); a dependency matrix as a "metro map" (lines — services, stations — API versions: the move to v3 is marked in advance, before date X); the Reg-Gate regulatory gateway before the train (PAN masking, audit logs, dependency licenses — one "no" and the train stands still); a release-readiness meeting (R²M) two days ahead — the PM says Go/No Go, because their metrics are on the line; follow-the-sun on-call for distributed teams. The PM books a slot in the calendar, removes the release-blocker tag, brings the regulatory documents and watches business alerts in their own time zone.
- **Security as a client of Delivery ("security left"):** security requirements go into the specification next to the design checklists (data masking in the AC, a negative test "unauthorized request → 401"), automation in CI (secret scanner, dependency analysis, static analysis), a permanent security backlog at 10–15% of capacity in the shared board with the same DoD. The PM is the translator between "expensive and slow" and "how much a leak costs" (Cost of Delay × fine).
- **Roles:** the PM — priority, metric, the answer to "roll back or wait"; business/system analyst — requirements, APIs, events; designer — mockups/design system; team lead/delivery — date estimates, backlog, dependencies; QA — test cases; the team — development and testing. Role allocation — [[M-decision-daci]].

## Procedure (use when building a commitment)
1. Take the prioritized hypothesis and the MVP/MLP scope ([[M-mvp-pilots]]). Separate Must from the rest; strike out whatever doesn't affect the measurable metric.
2. Request an **estimate** from development and the analyst (Effort, dates, dependencies, blockers); never plug in the PM's own estimate. If there is no estimate — write a range and mark it "forecast, not confirmed by the team".
3. Map against capacity (sprints, holidays, release windows, feature freeze, time for A/B) and cross-team dependencies (legal, security, adjacent APIs). Keep in mind that A/B requires sampling time beyond development.
4. Make sure the scope includes: analytics events and a dashboard, the A/B design, approvals (legal, security, support), rollback criteria, launch behind a flag.
5. Set the **post-release decision criteria**: success threshold, counter-metrics, observation window (e.g., the first 24 hours for tech, weeks for A/B), what counts as a rollback.
6. Record in the roadmap: stage, owner, dependency, date, milestone, decision at the milestone ([[M-roadmap]]); mark estimates and assumptions as forecasts.
7. After the release — reconcile fact against plan: dates, effect, counter-metrics; feed the action items back into the process.

## Template / checklist
```
Feature / hypothesis: ___   Scope: Must ___ | Should ___ | Won't ___ (cut-line)
Estimate (dev+QA): ___ person-weeks, range ___ ; estimate source: ___ ; status: forecast|confirmed by the team
Dependencies/approvals: ___ ETA ___   Release window / feature freeze: ___
Analytics events and dashboard: ready? yes|no   A/B design (metric, period, control): ___
Success criterion: ___ ; counter-metrics and thresholds: ___ ; rollback conditions: ___
Decision after observation: scale | iterate | roll back — who and when: ___
```
Checklist: the scope has been cut down to MVP/MLP · the estimate comes from the executors · dependencies and windows accounted for · analytics and alerts are in the specification · acceptance criteria checkable with yes/no · A/B budgeted · the owner of the roll-out/rollback decision is known.

## Typical mistakes
- Shipping a "blind" feature without analytics events; launching on Friday evening without alerts.
- Stuffing "nice-to-haves" into the sprint ("we'll be building this for two years"); Must = "everything"; floating acceptance criteria.
- The PM estimates effort themselves; the roadmap is built without estimates and without accounting for release windows.
- Mixing the releases of large features, so their effects cannot be separated.
- Assuming Delivery is not the PM's job; stopping at deploy instead of waiting for "the numbers to sing".
- Not reserving time for A/B, approvals, support and rollback.
- Taking speed (release frequency) as the goal instead of value (On-Time, Escaped Defects).
- An alert without an owner or an action — the signal is seen, but nobody responds; a release flag lives forever and turns into tech debt.
- A metric in the yellow zone for two sprints in a row — and "we'll fix it someday"; process tasks never make it into the sprint backlog.
- Each team separately ships "green" releases, but the summed effect hits latency and GMV — there is no shared calendar or dependency map.

## Questions that can change the decision
- Who from development/the analyst confirmed the date and volume? Which blockers and external dependencies remain?
- Are there release windows, feature freezes or regulatory gates that limit the date?
- Is there enough traffic and time for the A/B to decide on the effect before the next milestone?
- What does the team roll back, and who makes that decision at night?
- What is the cost of delay compared with the cost of an error: is it worth shipping without an experiment (a critical bug) or necessarily with one (pricing)?

## Related maps
[[M-roadmap]], [[M-mvp-pilots]], [[M-solution-design]], [[M-product-metrics]], [[M-decision-daci]], [[M-risks]], [[M-team]], [[M-product-communication]]
