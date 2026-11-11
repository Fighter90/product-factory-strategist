---
id: M-risks
lang: en
title: Strategy risks — identification, assessment, AATM, mitigation and plan B
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [options, strategy, validation, after-decision]
tags: [risks, risk-matrix, accept-avoid-transfer-mitigate, plan-b, trigger-metric, daci, mitigation, stakeholders]
related: [M-strategy-growth, M-external-environment, M-goals-drivers-bets, M-outcome-roadmap, M-team, M-decision-daci, M-mvp-pilots, M-landscapes, M-unit-economics]
---

# Strategy risks — identification, assessment, AATM, mitigation and plan B

## When to apply
For any strategy and any major bet, especially when resources are requested for it. The risk section is a mandatory item of the defense: without it no investment decision can be made. The card gives a procedure that goes from a list of threats to an action plan with triggers and owners, plus the rituals for keeping it up to date.

## Core idea
**Product risk** — anything that can go wrong while building, launching and operating the product and prevent it from reaching its goals, succeeding in the market and solving user problems.

**Why risks matter**: for the business — controllability of the outcome, a budget for the worst-case scenario, decision quality, vision synchronization and investor trust. For the product manager — managing expectations (a sign of maturity), the ability to request resources with risks priced in upfront (asking for "another 20%" after the fact is much harder), and readiness to maneuver instead of firefighting. "Everything always goes off plan" — the question is not whether a risk materializes but whether the product manager is ready. If a risk materializes, they will come to the product manager — so they must speak up about it in time.

**Eight risk types** (example: turning a booking service from a classifieds listing into a transaction)
| Type | Essence | Example |
|---|---|---|
| Product | users don't understand the value, metrics fall | conversion drop due to unfamiliar search and booking UX |
| Technical | incidents, bugs, integrations | a more complex architecture, payment integrations through partners |
| Business | the model doesn't close, monetization doesn't cover costs | seller churn due to new rules, loss of content and USP |
| Market | demand overestimated, competition, seasonality | strong competition among travel services |
| Legal | laws, licenses, fines, liability | the platform held liable in disputed situations |
| Fraud | user and partner fraud, leaks | taking buyers off the platform to avoid the commission |
| Operational | support load, SLA | growth of tickets caused by the new functionality |
| Marketing | channels don't work, value isn't communicated | low trust in the brand as a travel service |

**Assessment**: Risk = Probability × Impact. Probability — from 0 to 100% (or a 1–5 scale); impact — on key metrics (revenue, users, deadlines, reputation). To compare heterogeneous risks, convert the damage into one metric — usually revenue (conversion → via traffic × average check × take rate; seller churn → via lost bookings; reputation → via churn × LTV; operational → via staff and compensation cost). If all initiatives affect one metric (for example, conversion), you can use it directly. The assessment is subjective — it is important to record the assumptions.

Matrix zones: **red** (high probability × high damage) — immediate attention, usually avoid or mitigate with a mandatory plan B; **orange** — mitigate or transfer; **yellow/green** — accept or minimal mitigation. Course example: red — churn of top sellers; orange — conversion drop, competition, liability in disputes, trust in the brand, fraud; green — the technical one (a ready fintech solution is reused).

**Four responses (AATM)**
| Response | When | Example |
|---|---|---|
| Accept | mitigating costs more than the risk; usually low probability and moderate damage; conscious acceptance, not neglect | growing support load as the business grows — add resources in advance |
| Avoid | red zone: very expensive and very likely — better not to do it | drop part of the functionality |
| Transfer | there is a third party able to bear the risk | an insurance partner pays damages in disputes; in installments the bank bears the default risk |
| Mitigate | reduce the probability or the damage with concrete measures | tests, a pilot, a plan B |

**Mitigation methods**: minimal hypothesis testing (MVP, A/B, fake door — showing a non-existent feature and measuring interest, a focus group; remember that surveys and focus groups often diverge from reality); a pilot launch (a region/segment; regional tests — in at least two regions, otherwise the sample is too small); resource reservation (the "+20% to the estimate" rule); agreements with teams (priority, resources, fixed dependencies); **plan B** — a trigger metric with a justified threshold, action scenarios, owners. The threshold is not taken "off the ceiling" but derived from economics (the traction model shows what churn is acceptable at the project's minimum revenue). Example: "if seller churn is above 40% — we don't win back the old sellers, we acquire new ones through partners; after more than 3 violations — blocking".

**The choice of validation method depends on the product stage** (the earlier the stage, the cheaper the method):
| Method | Discovery | MVP | Growth | Maturity |
|---|---|---|---|---|
| Focus group | primary | with caution | — | — |
| Fake door | primary | appropriate | — | — |
| MVP | with caution | primary | — | — |
| A/B test | — | with caution | primary | primary |
| Pilot launch | — | appropriate | appropriate | with caution |
| +20% reserve, fixed dependencies, plan B | always | always | always | always |

**Fake door** (in detail): a button/banner for a non-existent feature → a "Coming soon, leave your e-mail" page; the CTR is measured. A reference threshold for confirming demand is a CTR above ~3–5%; the cost is days of work. Limitation: it shows interest but not willingness to pay; it differs from an MVP in that nothing works behind the button. The "+20%" rule applies to timelines, budget and headcount ("the tech lead said 2 sprints — count 2 + 20%: in reality everything slips"), and, conservatively, to conversion rates in the traction model.

**Seasonality is part of risk assessment** (a travel-vertical example): peak demand in Q3, growth in Q2, decline in Q4, low in Q1. Consequences: mass launches and metric reads — only in the peak season (off-season the effect drowns in seasonal noise and cannot be proven); off-season — preparation, integrations, seller retention; a counter-seasonal launch requires separate justification. When assessing the market risk of demand, always ask: "which season are we measuring this on?"

**Legal risk — a decision tree instead of "let's mitigate just in case"**: if probability > 50% and damage > threshold — avoid (don't do it or change the model); probability < 50% but the damage is very large — mitigate (a lawyer + plan B); otherwise — transfer (insurance, contract) or accept + monitoring of legislation. Damage thresholds are set in money per year and fixed.

**Antifraud — a pyramid by rising cost**: (1) basic content moderation; (2) behavioral detection (bypassing the platform, exchanging contacts in chat); (3) a penalty system (strikes, warnings); (4) restricting the bypass channel (closing communication until payment); (5) proactive ML detection of anomalies. The measures are introduced in phases as the transactional share grows — building everything at once is expensive and hurts conversion. Risk classification is conventional: one risk can be both fraud and business at the same time (buyers leave because of seller deception) — the type of measure matters more than the label.

**Stakeholders and DACI**: Driver (the product manager, accountable for the result), Approver (those who approve the decision), Contributor (marketing, lawyers, business development, teams), Informed (kept informed). Don't forget peer colleagues and the people you report to. Agreements are recorded in a table: stakeholder, agreement, status, owner (one contact person), deadline.

**Rituals**: threat modeling (what can go wrong in a sprint), post-mortems, a single risk map, the "three amigos" assessment (PM, developer/tester, designer — review mockups as early as possible), a quarterly dive-in with stakeholders. A new risk — update the strategy (don't change the goals, change the risk section); a materialized risk — socialize it and act on the new data.

**Maturity of risk management**: 0 — chaos; 1 — reactive (post-mortems); 2 — a risk list exists but is not updated; 3 — proactive (matrix, AATM, plan B, triggers, review); 4 — systemic (the map in rituals, threat modeling, alerts). The goal is at least level 3.

## Procedure
1. **List risks across all eight types**: at least one per type; sources — research, interviews, experience of similar launches, technical reviews, lawyers, support. For each one state: what will happen, how we'll notice (an indicator), which strategy assumption it depends on.
2. **Mark the cascades**: one risk causing another (seller churn → supply falls → conversion falls).
3. **Assess probability and impact**; convert the impact into revenue; state the source of the estimate and its type (fact / assumption).
4. **Place the risks in the matrix**, determine the zone.
5. **Choose the AATM response**; for accept — justify it (the cost of mitigation > the risk); for transfer — name the counterparty and the terms.
6. **Describe mitigation for red and orange**: method, cost, deadline, owner, residual risk.
7. **Plan B for the red zone**: trigger metric, threshold and its justification, action, decision owner, reaction time.
8. **Agree on the commitments** (DACI + the table); put the dependencies into the roadmap.
9. **Set up rituals and a review date** (at least once a quarter); link the materialization of a risk to the buffer and the bet-closing conditions in `M-outcome-roadmap`.

## Template / checklist
**Risk register**
| ID | Type | Risk | Strategy assumption | Indicator | Probability | Damage (₽/month or metric) | Zone | Response | Mitigation / plan B | Trigger and threshold | Owner | Deadline |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

**Agreements table**
| Stakeholder | Agreement | Status (agreed / in progress) | Owner | Deadline |
|---|---|---|---|---|
Example: the tech team — adopt another vertical's payment experience and set up alerts (Q1); support — +50% resources for calls (Q1–Q2); lawyers — update the seller contract because of the new offer; business — connect two insurance partners (Q2); marketing — a campaign focused on safety and choice (Q3).

**Checklist**
- [ ] All 8 risk types are covered; no "there are no risks" statement
- [ ] Every risk is scored for probability and damage, in a single metric
- [ ] Every red risk has a plan B with a trigger and a justified threshold
- [ ] Every risk has an AATM response with a justification
- [ ] Agreements are recorded with an owner and a deadline
- [ ] A review date and rituals are scheduled

## Typical mistakes
- "There are no risks" or "everything is average" — no focus and no trust.
- Risks without scores and without a plan B; risks written but never updated.
- Treating mitigation as mandatory: some risks are cheaper to accept.
- A trigger threshold taken "off the ceiling" (30%/40%) without economics.
- A regional pilot on a single region.
- Damage assessed in different units (reputation, conversion, money) without converting to a common metric.
- Requesting resources without a reserve; stakeholders learn of the risk at the moment it materializes.
- A list of only internal risks (legal, market and fraud forgotten).

## Questions that can change the decision
- Which risk is in the red zone, and is the pilot cheap enough to test it before major investment?
- Which strategy assumption, if false, kills the whole bet (pre-mortem: "a year from now the bet failed — why")?
- Is there a party the risk can be transferred to (insurance, partner, contract), and what does it cost?
- At what value of the trigger metric is it better to close the direction than to continue?
- Who makes the decision to switch to plan B, and within what time?
- Which risks depend on stakeholders with whom there are no agreements?

## Related maps
[[M-strategy-growth]], [[M-external-environment]], [[M-goals-drivers-bets]], [[M-outcome-roadmap]], [[M-team]], [[M-decision-daci]], [[M-mvp-pilots]], [[M-landscapes]], [[M-unit-economics]]
