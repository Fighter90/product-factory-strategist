---
id: M-risks
lang: en
title: Strategy risks — identification, assessment, AATM, mitigation and plan B
course: strategy
sources: ["EN mirror of the RU methodology card M-risks (knowledge/methods/risks.md); original sources are listed in the RU card"]
stages: [options, strategy, validation, after-decision]
tags: [risks, risk-matrix, accept-avoid-transfer-mitigate, plan-b, trigger-metric, daci, mitigation, stakeholders]
related: [M-strategy-growth, M-external-environment, M-goals-drivers-bets, M-outcome-roadmap, M-team, M-decision-daci, M-mvp-pilots, M-landscapes, M-unit-economics]
---

# Strategy risks — identification, assessment, AATM, mitigation and plan B

## When to apply
For any strategy and any major bet, especially when resources are requested for it. The risks section is a mandatory item of a defense: without it the investment decision cannot be made. The card gives a procedure from a list of threats to an action plan with triggers and owners, plus update rituals.

## Essence
**Product risk** — everything that can go wrong while building, launching and operating the product and prevent reaching goals, succeeding on the market and solving users' tasks.

**Why risks matter**: for the business — controllability of the outcome, a budget for the worst case, quality of decisions, synchronization of vision and investor trust. For the product manager — managing expectations (a sign of maturity), the ability to request resources with risks factored in advance (asking for "another 20%" after the fact is far harder), readiness to maneuver instead of firefighting. "Everything always goes off plan" — the question is not whether a risk will materialize, but whether the product manager is ready. If a risk materializes, accountability will fall on the product manager — so they must speak up in time.

**Eight types of risks** (example: turning a booking service from a classifieds into a transaction model)
| Type | Essence | Example |
|---|---|---|
| Product | users do not understand the value, metrics fall | conversion drop due to unfamiliar search and booking UX |
| Technical | incidents, bugs, integrations | architecture complexity, payment integrations via partners |
| Business | the model does not converge, monetization does not cover costs | seller churn due to new rules, loss of content and USP |
| Market | overestimated demand, competition, seasonality | high competition among travel services |
| Legal | laws, licenses, fines, liability | the platform held liable in disputes |
| Fraud | user and partner fraud, leaks | steering buyers off-platform to avoid commission |
| Operational | load on support, SLA | growth of tickets from new functionality |
| Marketing | channels do not work, value is not communicated | low trust in the brand as a travel service |

**Assessment**: Risk = Probability × Impact. Probability — from 0 to 100% (or a 1–5 scale); impact — on key metrics (revenue, users, timelines, reputation). To compare heterogeneous risks, convert damage into one metric — usually revenue (conversion → via traffic × average order value × take rate; seller churn → via lost bookings; reputation → via churn × LTV; operational → via staff and compensation costs). If all initiatives affect one metric (e.g., conversion), that one can be used. The assessment is subjective — recording the assumptions matters.

Matrix zones: **red** (high probability × high damage) — immediate attention, usually avoid or mitigate with a mandatory plan B; **orange** — mitigate or transfer; **yellow/green** — accept or minimal mitigation. Course example: red — churn of top sellers; orange — conversion drop, competition, liability in disputes, brand trust, fraud; green — technical (ready fintech is reused).

**Four reactions (AATM)**
| Reaction | When | Example |
|---|---|---|
| Accept | mitigation costs more than the risk; usually low probability and modest damage; a conscious acceptance, not "whatever" | support load growing with the business — add resources in advance |
| Avoid | red zone: very expensive and very likely — better not to do it | drop part of the functionality |
| Transfer | a third party able to carry the risk exists | an insurance partner covers damage in disputes; in installments the bank carries the default risk |
| Mitigate | reduce probability or damage with concrete measures | tests, pilot, plan B |

**Mitigation methods**: minimal hypothesis testing (MVP, A/B, fake door — showing a non-existent feature and measuring interest, focus group; remember that surveys and focus groups often diverge from reality); pilot launch (region/segment; regional tests — at least two regions, otherwise the sample is too small); resource reservation (the "+20% to the estimate" rule); agreements with teams (priority, resources, fixing dependencies); **plan B** — a trigger metric with a justified threshold, action scenarios, owners. The threshold is not taken "off the ceiling" but from the economics (the traction model shows what churn is tolerable at the project's minimum revenue). Example: "if seller churn exceeds 40% — do not win old ones back, acquire new ones via partners; at more than 3 violations — blocking".

**The choice of validation method depends on the product stage** (the earlier — the cheaper the method):
| Method | Discovery | MVP | Growth | Maturity |
|---|---|---|---|---|
| Focus group | primary | with caution | — | — |
| Fake door | primary | appropriate | — | — |
| MVP | with caution | primary | — | — |
| A/B test | — | with caution | primary | primary |
| Pilot launch | — | appropriate | appropriate | with caution |
| +20% reserve, fixing dependencies, plan B | always | always | always | always |

**Fake door** (in detail): a button/banner for a non-existent feature → a "Coming soon, leave your e-mail" page; CTR is measured. The guideline for confirming demand — CTR above ~3–5%; cost — days of work. Limitation: it shows interest, not willingness to pay; it differs from an MVP in that nothing works behind the button. The "+20%" rule applies to timelines, budget and headcount ("the tech lead said 2 sprints — count 2 + 20%: in reality everything slips"), and conservatively to conversions in the traction model.

**Seasonality is part of risk assessment** (travel vertical example): peak demand Q3, growth Q2, decline Q4, low Q1. Consequences: mass launches and metric measurements — only in the peak season (off-season, the effect will drown in seasonal noise and not be proven); off-season — preparation, integrations, seller retention; an off-season launch requires separate justification. When assessing market demand risk always ask: "on which season are we measuring this?"

**Legal risk — a decision tree instead of "let's mitigate just in case"**: if probability > 50% and damage > threshold — avoid (do not do it or change the model); probability < 50% but damage is very large — mitigate (lawyer + plan B); otherwise — transfer (insurance, contract) or accept + monitoring legislation. Damage thresholds are set in money per year and fixed.

**Anti-fraud — a pyramid by rising cost**: (1) basic content moderation; (2) behavioral detection (going around the platform, exchanging contacts in chat); (3) a penalty system (strikes, warnings); (4) restricting the workaround channel (closing communication until payment); (5) proactive ML detection of anomalies. Measures are introduced in phases as the transactional share grows — building everything at once is expensive and hurts conversion. Risk classification is conditional: one risk can be both fraud and business (buyers leave because of seller scams) — the type of measure matters more than the label.

**Stakeholders and DACI**: Driver (the product manager, accountable for the result), Approver (approve the decision), Contributor (marketing, legal, business development, teams), Informed (kept informed). Do not forget peer colleagues and those you report to. Agreements are fixed in a table: stakeholder, agreement, status, owner (one contact person), deadline.

**Rituals**: threat modeling (what can go wrong in a sprint), post-mortems, a single risk map, a "three amigos" assessment (PM, developer/tester, designer — reviewing mockups as early as possible), a quarterly dive-in with stakeholders. A new risk — update the strategy (do not change goals, but the risks section); a materialized one — socialize and act on the new data.

**Maturity of risk practice**: 0 — chaos; 1 — reactive (post-mortems); 2 — a risk list exists but is not updated; 3 — proactive (matrix, AATM, plan B, triggers, review); 4 — systemic (a map in rituals, threat modeling, alerts). The goal — at least level 3.

## Procedure
1. **List risks across all eight types**: at least one per type; sources — research, interviews, experience of similar launches, technical reviews, legal, support. For each specify: what will happen, how we will notice (indicator), which strategy assumption it depends on.
2. **Mark cascades**: a risk triggering another (seller churn → falling supply → falling conversion).
3. **Assess probability and impact**; convert impact into revenue; indicate the source of the estimate and its type (fact / assumption).
4. **Place on the matrix**, determine the zone.
5. **Choose the AATM reaction**; for accept — justify (cost of mitigation > the risk); for transfer — name the counterparty and the terms.
6. **Describe mitigation for red and orange**: method, cost, time, owner, residual risk.
7. **Plan B for the red zone**: trigger metric, threshold and its justification, action, decision owner, reaction time.
8. **Agree the agreements** (DACI + table); enter dependencies into the roadmap.
9. **Set rituals and a revision date** (at least once a quarter); link the materialization of a risk to the buffer and the bet-closing conditions in `M-outcome-roadmap`.

## Template / checklist
**Risk register**
| ID | Type | Risk | Strategy assumption | Indicator | Probability | Damage (₽/month or metric) | Zone | Reaction | Mitigation / plan B | Trigger and threshold | Owner | Deadline |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

**Agreements table**
| Stakeholder | Agreement | Status (agreed / in progress) | Owner | Deadline |
|---|---|---|---|---|
Example: the tech team — adopt another vertical's payments experience and set up alerts (Q1); support — +50% capacity for calls (Q1–Q2); legal — update the seller contract because of the new offer terms; business — connect two insurance partners (Q2); marketing — a campaign emphasizing safety and choice (Q3).

**Checklist**
- [ ] All 8 risk types covered; no "there are no risks" wording
- [ ] Every risk assessed by probability and damage, in a single metric
- [ ] Every red risk has a plan B with a trigger and a justified threshold
- [ ] An AATM reaction chosen and justified for each risk
- [ ] Agreements fixed with an owner and a deadline
- [ ] A revision date and rituals planned

## Common mistakes
- "There are no risks" or "everything is average" — no focus and no trust.
- Risks without assessment and without plan B; risks written but not updated.
- Treating mitigation as mandatory: some risks are cheaper to accept.
- A trigger threshold "off the ceiling" (30%/40%) without economics.
- A regional pilot in one region.
- Damage assessed in different units (reputation, conversion, money) without converting to a common metric.
- Requesting resources without a reserve; stakeholders learn of the risk when it materializes.
- A list of only internal risks (legal, market, fraud forgotten).

## Questions that can change the decision
- Which risk is in the red zone, and is the pilot cheap enough to test it before major investment?
- Which strategy assumption, if false, kills the whole bet (pre-mortem: "in a year the bet failed — why")?
- Is there a party to transfer the risk to (insurance, partner, contract) and what does it cost?
- At which value of the trigger metric is closing the direction more profitable than continuing?
- Who decides on switching to plan B, and within what time?
- Which risks depend on stakeholders with whom there are no agreements?

## Related cards
[[M-strategy-growth]], [[M-external-environment]], [[M-goals-drivers-bets]], [[M-outcome-roadmap]], [[M-team]], [[M-decision-daci]], [[M-mvp-pilots]], [[M-landscapes]], [[M-unit-economics]]
