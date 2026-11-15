---
id: M-platforms-types-criteria
lang: en
title: Platform Types and Platformization Criteria
course: strategy
sources: ["EN mirror of the RU methodology card M-platforms-types-criteria (knowledge/methods/platforms-types-criteria.md); original sources are listed in the RU card"]
stages: [research, options, strategy]
tags: [platforms, platformization, core, contracts, network-effects, multi-homing, shared-service]
related: [M-platform-ecosystem-audit, M-platform-case-concept, M-platform-economics, M-platform-risks-rollout, M-business-models, M-unit-economics]
---

# Platform Types and Platformization Criteria

## When to apply
"Is there a platform opportunity here, and what should it look like?", "when is a platform justified, and when is a shared service or local solutions enough?", "what distinguishes a real platform product from a set of duplicated solutions?". Entry point into the platform track: before the ecosystem audit ([[M-platform-ecosystem-audit]]) and before designing the concept ([[M-platform-case-concept]]).

## Essence
### Two meanings of the word "platform"
- **Ecosystem platform** — organizes interaction between several groups of participants; value emerges in the exchange between them (a marketplace, an app platform, a video platform: creators ↔ viewers ↔ advertisers). Framework: Parker, Van Alstyne, Choudary "Platform Revolution".
- **Internal platform** — gives teams a reusable core and rules so they can build their own solutions; the "customers" are internal teams.

### Taxonomy by where the value sits
| Class | What it provides | Generalized examples |
|---|---|---|
| Transactional (ecosystem) | An exchange venue: the deal happens between the participants, the platform provides the service and the rules | marketplaces, ride and lodging aggregators |
| Innovation (ecosystem/technical) | A technology on top of which others build solutions | operating systems, messenger bot platforms, API platforms |
| Integrated | Both exchange and solution-building on top of a core | an app platform inside a company's ecosystem |

### Types of internal platforms (course focus)
1. **Product** — reputation, loyalty, promotion.
2. **Product-technical** — notifications, recommendations, verification.
3. **Technical** — APIs, data platforms, developer tooling.
4. **Infrastructure** — compute, storage, observability.

### Anatomy: core → contracts → customization → client products
- **Core**: shared data, shared logic, a standard product.
- **Contracts**: APIs, formats, access rights — the rules of integration.
- **Customization**: settings and extensions within the limits the platform provides.
- The "is it already a platform or not yet" test: ≥2 independent clients; the core is separated from extensions (shared code is not edited per case); there is onboarding, versioning, and support. Bottom line: a client builds its own solution on top of the core without reworking the platform for each scenario.

### Network effects, multi-homing, curatability (for ecosystem platforms)
- **Network effect**: value for a participant grows with the number of participants on the other side (cross-side) or the same side (same-side). It determines the launch strategy: which side to build up, and when.
- **Multi-homing**: a participant uses several platforms at once. The lower the multi-homing costs (moving content, data, habits), the weaker the scale effect; it also shows where the leader can be caught up.
- **Curatability**: the platform must manage the quality of interactions (rules, verification, ratings) — otherwise a low-quality flow kills value for the second side. Curatability = a liquidity management tool ([[M-platform-economics]]).

## Procedure
1. **Classify the situation**: an ecosystem platform or an internal one? If internal — which of the four types. This sets the success metrics (liquidity and side adoption vs team speed and reuse).
2. **Collect the signals that local solutions stopped being enough** (≥3 items from the list is a strong argument): several teams independently build the same feature; similar scenarios run under different rules; UX diverges between verticals; supporting local solutions eats more and more time; every integration is done manually; tech debt accumulates.
3. **Choose one of four options** (not everything reduces to "build a platform"):
   - **Keep it local** — one team, a unique scenario, repetition not proven.
   - **Build a shared service** — extract the function with an API without a platform model (plans, integration contracts, support).
   - **Minimally platformize** — extract a small shared core, leave the rest to the teams.
   - **Build a platform** — a separate product for several clients with a development plan, contracts, and support.
4. **Run the 4 platformization criteria**:
   - **Scale and repeatability**: ≥ several teams need it now or in the near-term plan; the scenario is regular; a stable core can be extracted without hurting the teams' goals.
   - **Economics**: `Cost(N × LOCAL) > Cost(CORE + N × INTEGRATION)` — where LOCAL includes development, maintenance, fixes, and integrations at each team; the platform includes the core, integrations, compatibility, and migrations ([[M-platform-economics]]).
   - **Standardization without losing speed**: the core holds unified entities, rules, quality guarantees; adaptations preserve the differences between scenarios and the teams' pace.
   - **Client readiness**: the value solves the client's problem (not just saves the company money); the migration cost is calculated (integration + data transfer + process change); there is a sponsor and an owner; the integration contract describes constraints, SLA, responsibilities, settings.
5. **Check yourself against the anti-patterns**: a platform for the platform's sake (architecture before the shared problem is confirmed); too broad a core (the requirements of all conceivable clients baked into the core up front); migration without value (moving teams without improving their speed and metrics); universality at any cost (a shared solution breaks important scenario differences). First a local MVP and proven repeatability, then the core and contracts.
6. **Choose the level of generalization**: the same capability can be measured at different scales (a specific feature → a function → a domain). Run the 4 criteria at each level — platformize the level where all four converge.
7. **Formulate pros and cons for the defense**: the main change for the business (less duplication, unified UX and rules, economies of scale, the next teams onboard faster, lower operating costs) against the risk (demand not confirmed, migration expensive, scenarios too different, no sponsor, integration slows clients down).

### Example (illustrative numbers, the economics criterion)
Five teams need the capability. Locally: development in each team 2 mo. (5 × 2 = 10), repeated rework 20 × 2 days ≈ 2 mo., support 5 × 0.2 ≈ 1 mo. → 13 FTE-months. Platform: core 3 mo. + integrations 3 mo. + client migrations and launches 5 mo. → 11 FTE-months in the first year. The economics converge already in the first year; with 6+ clients and zero repeated rework the gap widens. If there were only 2 clients and the scenarios differed by half — "keep it local" or "a shared service" would win. The conclusion is sensitive to the number of clients and the depth of differences — compute over a range.

### Hints on choosing an option
| Situation | The option to lean toward |
|---|---|
| One team, unique scenario, repetition not proven | Keep it local |
| The function is needed by many, but variability is near zero (hypothesis testing, A/B experiments) | Shared service |
| A core exists (data, statuses, channels), the differences are in content and rules | Minimally platformize |
| Several independent clients, shared entities exist, new integrations expected in the plan | Build a platform |

## Template / checklist
| Check | Yes/No | Comment |
|---|---|---|
| Clients ≥ 2 and they are independent | | |
| The core separates from extensions | | |
| Onboarding, versions, support exist | | |
| Local-solution exhaustion signals ≥ 3 | | list which ones |
| `N × LOCAL > CORE + N × INTEGRATION` | | the numbers |
| Sponsor and owner appointed | | who |
| Migration cost estimated (in client-days) | | |
| Anti-patterns cleared (across all 4 items) | | |

Exit artifact: platform type → signals → the chosen option from the four with a rationale → assessment against the 4 criteria → the counterargument against platformization.

## Typical mistakes
- Calling shared code with a single real client and no stable contracts a platform.
- Platformizing before value is confirmed on a local MVP (a typical failure: a premature shared reputation/rating platform — dependencies, migrations, and timelines grow before any demand signal).
- Counting only the reuse benefit and not counting support, compatibility, and migrations — a platform's economics do not converge immediately.
- Building a broad architectural "spaceship": the system can do everything, but integration requires understanding the entire model.
- Ignoring client readiness: "savings for the company" does not motivate the client team that bears the migration cost.

## Questions that could change the decision
- How many teams will face the task next year by plan, not "someday"?
- What is the real cost of core + integrations vs N local solutions over 3–5 years?
- If the core goes down, all clients suffer at once — are you ready to answer for that?
- Do the sides/clients have multi-homing costs, and can they be raised/lowered in your favor?
- Whom and how will the platform get in the way of: whose scenario differs the most ([[M-platform-ecosystem-audit]])?

## Related maps
[[M-platform-ecosystem-audit]], [[M-platform-case-concept]], [[M-platform-economics]], [[M-platform-risks-rollout]], [[M-business-models]], [[M-unit-economics]]
