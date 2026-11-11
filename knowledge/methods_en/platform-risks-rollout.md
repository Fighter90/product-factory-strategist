---
id: M-platform-risks-rollout
lang: en
title: Platform risks, concept review, pilot, scaling and adoption, investor case
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [options, validation, after-decision]
tags: [platforms, risks, risk-register, pilot, adoption, gtm, investor-case, review, traffic-lights]
related: [M-platforms-types-criteria, M-platform-case-concept, M-platform-economics, M-risks, M-mvp-pilots, M-pmf-scaling, M-product-metrics, M-traction-model]
---

# Platform risks, concept review, pilot, scaling and defense

## When to apply
"What could revise the platform decision, and how do we prepare for it?", "how do we package and defend the final document?", "how do we choose the pilot project and decide on its outcome?", "how do we scale the platform and raise client adoption?", "how do we assemble the investment case for the committee?". This is the closing loop of the platform track, following the concept ([[M-platform-case-concept]]) and the economics ([[M-platform-economics]]).

## Core idea
A positive ROI shows the platform's potential, but not the probability of realizing it. That is why the case is stress-tested through risks, a pilot, and regular reviews.

### Risk vs problem vs constraint vs assumption
| Category | Sign |
|---|---|
| Risk | The event has not happened yet, but may change the outcome |
| Problem | The event has already happened; it requires a response |
| Constraint | A known condition we work within |
| Assumption | A statement accepted in the model but not yet confirmed |

Categories of platform risks: product and value / adoption; technology and data; economics; organization; legal and compliance; PR. Adoption is a risk category in its own right: "four clients will connect, migration takes a quarter, savings land in year two" can turn into a delayed migration, an expensive transition, and a shifted — or vanished — break-even.

### Prioritization and the register
The `probability × impact` matrix yields P0–P3: **P0** blocking (can stop the launch or make the platform unviable); **P1** critical (changes scope, economics, architecture, roadmap); **P2** significant (requires action but does not change the decision as a whole); **P3** local (monitored inside the team). A risk is phrased as **cause → event → consequences**.

### Concept review: the document and the check
Skeleton of the defense document: 1) case passport + traffic lights (traction model, investment control) on the first page; 2) executive summary and the decision ask; 3–4) FAQ by blocks: product idea, segments, fit with the strategy; tasks, GTM; 5) traction and financial summary; 6) concerns and risks; 7) success criteria and the date of the next review; 8) appendices and sources. Every key claim follows the chain **thesis → source → calculation → decision** (what we assert; whose plan/measurement; how the data lead to the conclusion; what changes in the ask, the roadmap, or the risk register). Team cross-check: the USP, the problem-hypothesis checks, the MLP description, the linkage of input metrics to the product's essence, the traction model and IRR, the criteria for the next review and the stop criteria.

### Pilot
- **Criteria for choosing the pilot project (score "poor / medium / good" + why):** 1) learning value — which hypotheses about the platform it tests; 2) client readiness — there is an owner and resources; 3) an influential sponsor; 4) impact / clear value; 5) risk — the failure is bounded, reversible, and not critical for the business; 6) effort — the cost of development and integration.
- **What is measured in the pilot:** before — Easy Start (how easily the project got launched); during — functionality and stability; after — the result and the decision.
  - Easy Start, qualitative: interviews with the platform's users (what was easy/hard, what was missing in the documentation, which constraints got in the way, what to change so the next team can launch without support, whether there were doubts about correctness). Quantitative: the number of requests to the platform team; the time from the start of integration to launch; the effort of both sides in person-sprints; the number of changes made specifically for the pilot.
  - Functionality: triggers/rules work, the audience is respected, the data are correct, behavior under failure is defined, the analytics is computed.
  - Stability: critical incidents; downtime ≤ 0.5%; ≥ 99% of events processed successfully; monitoring and alerts help find the cause.
- **The decision on the results: change / scale / stop.** Change — fix before scaling (the team's integration estimate was poor). Scale — increase the number of clients while watching every launch (quality metrics are within norms). Stop — the effect was not confirmed (statistically significantly negative) or a blocker was found. Separate cases: the effect could not be measured because the launch audience was too narrow → another pilot is needed; a top manager doubts the direction itself → work on their opinion, do not "scale".

### Scaling and adoption
- **Usage ≠ adoption**: usage — the action happened; adoption — the behavior has stuck (the person returns, uses it regularly, the product has become part of the routine). Granted access ≠ adoption: a link/demo/account do not count; what counts is a change in working behavior — assigned an owner, launched, came back.
- **Adoption is counted three ways:** by clients (`teams with a launch within N days / all eligible teams` — the breadth of the base), by places/components (`places going through the platform / all eligible` — the depth of replacement), by volume (`impressions/transactions through the platform / all eligible` — the actual scale).
- **The adoption funnel of a client team:** eligible (has a real task the platform solves) → aware (of the platform and what it is for) → requirements finalized → ready (owner, deadlines, roles, no obstacles) → launched → repeats/expands. Every transition has its own barriers and remedies:
  - top of the funnel: the task was mistakenly deemed ineligible → simple eligibility criteria + a short consultation; the platform knows nothing about the clients → a registry of scenarios, studying teams' plans, a regular collection of requests.
  - aware: does not see the connection to their task, does not know where to start → an offer in the team's own language ("launch X with ready-made analytics", not "connect to the platform"); platform GTM.
  - requirements: the client is not interested → value, a change agent, a step-by-step migration of the existing solution; cannot formulate requirements → a questionnaire template; rejects the common rules → show the consequences for other teams, an experiment with guaranteed test traffic and completion criteria (rather than disabling the rules — a dangerous precedent).
  - ready: the task is not in the priorities, there are no resources → show the client's scope of work in advance, a readiness checklist, shared OKRs, a sponsor; dependencies on other teams → a dependency map.
  - launched: new requirements mid-flight → fix the MVP scope; the new items go into the next iterations; underestimated → cut the scope / recalculate the deadline; slow development → documentation, integration templates, regular blocker meetings.
  - repeats: the first experience failed → self-service growth points, news about improvements; no next scenario → show cases from other clients.
- **Platform GTM:** a landing page (value, scenarios, the launch path, success cases, a "discuss your task" button); internal PR (talks, demos, digests); working with teams (collecting requests, quarterly planning, change agents in every vertical). Scaling forks are resolved by the principle "an exception = a dangerous precedent": first look for a platform solution; migrate in stages, starting from the simplest segment; fix tech debt with a deadline.

### Investment case (defense before the committee)
Composition per the defense template: the case passport (class, level, type of effect) + the traffic lights of traction-model validation and investment control + the support of the verticals; the executive summary of past reviews and the current one (the platform boundary, commitments, facts); the executive summary (the problem, the traction goal, the sources of the effect — "teams not created" and "a single loop", the financial summary); FAQ 1 idea and strategy; FAQ 2 tasks, success criteria, roadmap, progress ("done / success criterion" tables); FAQ 3 traction — input/output metrics with "old / new version" columns and explanations of the changes; FAQ 5 financial summary (ΔFCF of the two scenarios "without the platform" and "with the platform" minus the platform team; IRR; the signs that a top-level approval is required: negative flow above a threshold, costs above a threshold over 12 months, M&A); FAQ 6 traffic lights (yellow for analytics while the effect is measured on a single client — until a second/third measurement; green for investment control — costs are limited to one team, the model is conservative, and if funding stops the platform is handed to the first client as a service); FAQ 7 success criteria and commitments to the next review; appendices (P&L versus the previous committee, a breakdown of costs, the incremental P&L, scenarios, the measurement methodology, the core composition component by component, integration rules, the onboarding queue). The strength of the case lies in its sources: the number of future products comes from the company's approved plan; the "without platform" costs come from the actual costs of one's own and neighboring teams; the acceleration comes from the pilot measurement; the onboarding cost is in client person-days.

## Procedure
1. **Build a risk register (5–7 risks):** priority P0–P3 per the matrix; cause → event → consequences; a mitigation plan (reduce probability or damage; what we do before it materializes; how we will recognize that the risk is approaching; what to do afterwards); the owner and the involved parties (platform PM, vertical owners, tech/architecture, finance, legal, operations). For the three top-priority risks — a detailed plan.
2. **Run the concept constraints** through a translation into risks: what breaks at the client → how we compensate → if we cannot, warn honestly.
3. **Assemble the defense document** per the skeleton; check the "thesis → source → calculation → decision" chain in every section; cross-check for contradictions between sections and between metrics; mark the gaps rather than hide them.
4. **Choose the pilot project:** score the candidates against the 6 criteria in a summary table; record the expected effect of each.
5. **Run the pilot and measure** Easy Start (interviews + 4 metrics), functionality, stability; handle incidents per the protocol (check the scale → disable the faulty part → fix → resume on a small audience → extend the pilot if the data are insufficient; support goes through a process, not personal chats).
6. **Decide change / scale / stop** based on the actual metrics; record the platform's growth points and the improvement plan.
7. **Design the scaling:** an onboarding queue in waves; the adoption funnel and its bottleneck (the biggest gap between stages); a plan to lower the barriers of every transition; the GTM plan; resolving conflicts through platform solutions rather than exceptions.
8. **Assemble the investor case** per the template and go to the review: a concrete ask (team and deadline), commitments to the next review (what you undertake to show), explanations of the changed figures, status traffic lights with their rationale.

## Template / checklist
**Risk register:**
| Priority | Risk: cause → event → consequences | Mitigation plan (before/after, early signals) | Owner | Who is involved |
|---|---|---|---|---|
| P0–P3 | | | | |

**Summary pilot assessment:**
| Candidate | Learning | Client readiness | Sponsor | Impact | Risk | Effort | Expected effect |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

**Adoption funnel:**
| Stage | Teams at the stage | Transition to the next | Barriers | Remedies |
|---|---|---|---|---|
| eligible | | | | |
| aware | | | | |
| requirements | | | | |
| ready | | | | |
| launched | | | | |
| repeats | | | | |

Exit artifacts: a risk register → a defense document per the skeleton → a pilot protocol with a change/scale/stop decision → a scaling plan with the funnel and GTM → an investor case with commitments.

## Typical mistakes
- Confusing a risk with a problem/constraint/assumption; phrasing a risk without a cause and consequences ("risks always exist").
- Hiding yellow/red traffic lights or setting them without a methodology; traffic lights must come before the executive summary, with an explanation.
- Transferring an effect measured on one client to everyone without a second/third measurement.
- Counting access, demos, and account creation as adoption; the adoption funnel has been built, but its barriers are never named or removed.
- Making exceptions for strong clients (disabling the common rules for one client) — the precedent destroys the platform.
- A pilot without a defined failure criterion → any result will be declared a success.
- "We need leadership support" instead of specifics; in the investor case, figures taken from guesses rather than from plans and facts.

## Questions that can change the decision
- Which P0 risk could stop the initiative, and when would we learn about it earliest?
- Which adoption-funnel transition is the narrowest, and is removing its barrier cheaper than building new features?
- Are two effect measurements enough to remove the yellow analytics traffic light?
- What happens to the platform if the funding stops (handover to a client, support, archive)?
- What will the next commitment before the committee be, and is it achievable without additional people?
- Won't a client's first failure turn into a vertical's long-term refusal of the platform?

## Related maps
[[M-platforms-types-criteria]], [[M-platform-case-concept]], [[M-platform-economics]], [[M-risks]], [[M-mvp-pilots]], [[M-pmf-scaling]], [[M-product-metrics]], [[M-traction-model]]
