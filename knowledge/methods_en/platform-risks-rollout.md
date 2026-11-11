---
id: M-platform-risks-rollout
title: Platform risks, concept evaluation, pilot, scaling and defense
course: pm-approaches-en
sources: ["EN mirror of RU card M-platform-risks-rollout (knowledge/methods/platform-risks-rollout.md); original sources are listed in the RU card"]
stages: [options, validation, after-decision]
tags: [platforms, risks, risk-register, pilot, adoption, gtm, investment-case, review, traffic-lights]
related: [M-platforms-types-criteria, M-platform-case-concept, M-platform-economics, M-risks, M-mvp-pilots, M-pmf-scaling, M-product-metrics, M-traction-model]
lang: en
---

# Platform risks, concept evaluation, pilot, scaling and defense

## When to use
"What could revise the platform decision, and how do we prepare for it?", "how do we write up and defend the final document?", "how do we pick the pilot project and decide based on its results?", "how do we scale the platform and raise customer adoption?", "how do we assemble the investment case for the committee?". The closing loop of the platform track, after the concept ([[M-platform-case-concept]]) and the economics ([[M-platform-economics]]).

## Core
A positive ROI shows the platform's potential, but not the probability of realizing it. That is why the case is stress-tested through risks, a pilot, and regular reviews.

### Risk vs issue vs constraint vs assumption
| Category | Signature |
|---|---|
| Risk | The event has not happened yet, but could change the outcome |
| Issue | The event has already happened and demands a response |
| Constraint | A known condition within which we operate |
| Assumption | A statement accepted in the model but not confirmed |

Categories of platform risks: product and value / adoption; technology and data; economics; organization; legal and compliance; PR. Adoption is a risk in its own right: "four customers will onboard, migration will take a quarter, savings in year 2" can turn into a delayed migration, an expensive transition, and a shifted or vanished break-even.

### Prioritization and the register
The `probability × impact` matrix yields P0–P3: **P0** blocking (can stop the launch or make the platform unviable); **P1** critical (changes scope, economics, architecture, roadmap); **P2** significant (requires action but does not change the decision as a whole); **P3** local (monitored inside the team). Risk statement format: **cause → event → consequences**.

### Concept evaluation: the document and its verification
The skeleton of the defense document: 1) case passport + traffic lights (traction model, investment control) on the first page; 2) executive summary and decision ask; 3–4) FAQ by blocks: product idea, segments, embedding into strategy; tasks, GTM; 5) traction and financial summary; 6) concerns and risks; 7) success criteria and the date of the next review; 8) appendices and sources. Every key claim follows the chain **claim → source → calculation → decision** (what we assert; whose plan/measurement; how the data leads to the conclusion; what changes in the request, roadmap, or risk). Cross-check by the team: USP, validation of problem hypotheses, MLP description, connection of input metrics to the essence of the product, traction model and IRR, criteria for the next review and stop criteria.

### Pilot
- **Criteria for choosing a pilot project (rated "poor / average / good" + why):** 1) learning value — which hypotheses about the platform will we test; 2) customer readiness — there is an owner and resources; 3) an influential sponsor; 4) impact / clear value; 5) risk — a mistake is contained, reversible, not critical for the business; 6) effort — cost of development and integration.
- **What is measured in the pilot:** before — Easy Start (how easily the project got launched); during — functionality and stability; after — results and the decision.
  - Easy Start qualitatively: interviews with users of the platform (what was easy/hard, what was missing in the documentation, which constraints got in the way, what to change so the next team launches without support, whether there were doubts about correctness). Quantitatively: number of requests to the platform team; time from the start of integration to launch; effort of both sides in person-sprints; number of changes made specifically for the pilot.
  - Functionality: triggers/rules work, the audience is respected, data is correct, behavior on failures is defined, analytics are counted.
  - Stability: critical incidents; downtime ≤ 0.5%; ≥ 99% of events processed successfully; monitoring and alerts help find the cause.
- **The decision after the pilot: change / scale / stop.** Change — finish the work before scaling (poor integration estimate by the team). Scale — grow the number of customers while watching every launch (quality metrics are normal). Stop — the effect was not confirmed (statistically significantly negative) or a blocker was found. Separate cases: the effect was not measured because of a narrow launch audience → another pilot is needed; a top manager doubts the whole direction → work on the opinion, not "scale".

### Scaling and adoption
- **Usage ≠ adoption**: usage — the action happened; adoption — the behavior has taken hold: the user came back, uses it regularly, the product became part of the routine. Granted access ≠ adoption: a link/demo/account do not count; we count a change in working behavior — assigned an owner, launched, came back.
- **Adoption is counted three ways:** by customers (`teams with a launch within N days / all eligible teams` — width of the base), by places/components (`places through the platform / all eligible` — depth of replacement), by volume (`impressions/transactions through the platform / all eligible` — the actual scale).
- **The adoption funnel of a customer team:** fits (has a real task the platform solves) → knows (about the platform and its tasks) → requirements finalized → ready (owner, deadlines, roles, no obstacles) → launched → repeats/expands. Each transition has its own barriers and solutions:
  - top of the funnel: the task was mistakenly judged unsuitable → simple eligibility criteria + a short consultation; the platform does not know about customers → a registry of scenarios, studying team plans, regular collection of requests.
  - knows: does not see the connection to their own task, does not know where to start → an offer in the team's language ("launch X with ready-made analytics", not "connect to the platform"); the platform's GTM.
  - requirements: the customer is not interested → value, a change agent, a step-by-step migration of the existing solution; cannot formulate requirements → a questionnaire template; rejects common rules → show the consequences for other teams, an experiment with guaranteed test traffic and completion criteria (not switching off the rules — a dangerous precedent).
  - ready: the task is not a priority, no resources → show the customer's scope of work in advance, a readiness checklist, joint OKRs, a sponsor; dependencies on other teams → a dependency map.
  - launched: new requirements appear mid-flight → fix the MVP scope, new items go into the next iterations; underestimation → cut the scope / recalculate the deadline; slow development → documentation, integration templates, regular blocker meetings.
  - repeats: the first experience failed → growth points for self-service, news about improvements; no next scenario → show cases of other customers.
- **Platform GTM:** a landing page (value, scenarios, the path to launch, successful cases, a "discuss your task" button); internal PR (talks, demos, digests); work with teams (collecting requests, quarterly planning, change agents in every vertical). Scaling forks are resolved on the principle "an exception = a dangerous precedent": first look for a platform solution, do migration in stages starting from the simplest segment, fix tech debt with a deadline.

### The investment case (defense before the committee)
Composition per the defense template: case passport (class, level, type of effect) + traffic lights for traction-model validation and investment control + support of the verticals; executive summary of past reviews and the current one (platform boundary, commitments, actuals); executive summary (problem, traction goal, sources of the effect — "teams not created" and "a single loop", financial summary); FAQ 1 idea and strategy; FAQ 2 tasks, success criteria, roadmap, progress ("done / success criterion" tables); FAQ 3 traction — input/output metrics, "old/new version" columns with explanations of the changes; FAQ 5 financial summary (ΔFCF of the two scenarios "without the platform" and "with the platform" minus the platform team; IRR; signs that a top-level approval request is triggered: negative flow above the threshold, costs above the threshold within 12 months, M&A); FAQ 6 traffic lights (analytics yellow while the effect is measured on one customer — until the second/third measurement; investment-control green — costs are limited to one team, the model is conservative, and if funding stops the platform is handed to the first customer as a service); FAQ 7 success criteria and commitments to the next review; appendices (P&L against the previous committee, cost detail, incremental P&L, scenarios, measurement methodology, the core's composition component by component, integration rules, the onboarding queue). The strength of the case is in its sources: the number of future products comes from the company's approved plan; the costs "without the platform" come from the actual costs of one's own and neighboring teams; the speedup comes from the pilot measurement; the onboarding cost is in customer person-days.

## Procedure
1. **Build the risk register (5–7 risks):** priority P0–P3 by the matrix; cause → event → consequences; a mitigation plan (we reduce probability or damage; what we do before it happens; how we will know the risk is approaching; what to do after); owner and participants (platform PM, vertical owners, tech/architecture, finance, legal, operations). For the three top-priority ones — a detailed plan.
2. **Run the concept's constraints** through translation into risk: what will break for the customer → how we compensate → if we cannot — warn honestly.
3. **Assemble the defense document** per the skeleton; check the chain "claim → source → calculation → decision" in every section; cross-check for contradictions between sections and metrics; mark gaps rather than hushing them up.
4. **Choose the pilot project:** rate the candidates on the 6 criteria in a summary table; fix each one's expected effect.
5. **Run the pilot and measure** Easy Start (interviews + 4 metrics), functionality, stability; handle incidents by protocol (check the scale → switch off the problematic part → fix it → resume on a small audience → extend the pilot if data is insufficient; support goes through a process, not personal chats).
6. **Decide change / scale / stop** on actual metrics; fix the platform's growth points and the improvement plan.
7. **Design the scaling:** an onboarding queue in waves; the adoption funnel and its bottleneck (the biggest gap between stages); a plan to lower the barriers of each transition; a GTM plan; resolving conflicts through platform solutions, not exceptions.
8. **Assemble the investment case** per the template and go to the review: a concrete request (a team and a deadline), commitments to the next review (what you undertake to show), an explanation of the changed numbers, status traffic lights with justification.

## Template / checklist
**Risk register:**
| Priority | Risk: cause → event → consequences | Mitigation plan (before/after, early signals) | Owner | Participants |
|---|---|---|---|---|
| P0–P3 | | | | |

**Pilot summary scorecard:**
| Candidate | Learning | Customer readiness | Sponsor | Impact | Risk | Effort | Expected effect |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

**Adoption funnel:**
| Stage | Teams at the stage | Transition to the next | Barriers | Solutions |
|---|---|---|---|---|
| fits | | | | |
| knows | | | | |
| requirements | | | | |
| ready | | | | |
| launched | | | | |
| repeats | | | | |

Exit artifacts: risk register → defense document per the skeleton → pilot protocol with the change/scale/stop decision → scaling plan with the funnel and GTM → investment case with commitments.

## Typical mistakes
- Confusing a risk with an issue/constraint/assumption; stating a risk without cause and consequences ("there are always risks").
- Hiding yellow/red traffic lights or setting them without a methodology; traffic lights must come before the executive summary, with an explanation.
- Transferring an effect measured on one customer to everyone without a second/third measurement.
- Counting access, demos, and account creation as adoption; the adoption funnel is drawn, but the barriers are not named and not removed.
- Making exceptions for strong customers (switch off common rules for one) — the precedent destroys the platform.
- A pilot without a defined failure criterion → any result will be declared a success.
- "We need management support" instead of specifics; investment-case figures from a guess instead of plans and facts.

## Questions that can change the decision
- Which P0 risk can stop the initiative, and when will we learn about it the earliest?
- Which transition of the adoption funnel is the narrowest, and is removing its barrier cheaper than building new features?
- Are two measurements of the effect enough to remove the analytics yellow light?
- What happens to the platform if funding stops (handover to a customer, support, archive)?
- What will the next commitment before the committee be, and is it doable without extra people?
- Could the first customer's failure turn into a vertical's long-term rejection of the platform?

## Related cards
[[M-platforms-types-criteria]], [[M-platform-case-concept]], [[M-platform-economics]], [[M-risks]], [[M-mvp-pilots]], [[M-pmf-scaling]], [[M-product-metrics]], [[M-traction-model]]
