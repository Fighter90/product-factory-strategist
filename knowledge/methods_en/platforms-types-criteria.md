---
id: M-platforms-types-criteria
lang: en
title: Platform types and platformization criteria
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [research, options, strategy]
tags: [platforms, platformization, core, contracts, network-effects, multi-homing, curation, shared-service]
related: [M-platform-ecosystem-audit, M-platform-case-concept, M-platform-economics, M-platform-risks-rollout, M-business-models, M-unit-economics]
---

# Platform types and platformization criteria

## When to apply
"Is there a platform opportunity here, and what should it be?"; "when is a platform justified, and when is a shared service or local solutions enough?"; "what distinguishes a true platform product from a set of duplicate solutions?" Entry point into the platform track: before the ecosystem audit ([[M-platform-ecosystem-audit]]) and before concept design ([[M-platform-case-concept]]).

## Core idea
### Two meanings of the word "platform"
- An **ecosystem platform** organizes the interaction of several groups of participants; value arises in the exchange between them (a marketplace, an app platform, a video platform: creators ↔ viewers ↔ advertisers). Framework: Parker, Van Alstyne, Choudary, "Platform Revolution".
- An **internal platform** gives teams a reusable core and rules so that they can create their own solutions; its "clients" are internal teams.

### Taxonomy by locus of value
| Class | What it provides | Generalized examples |
|---|---|---|
| Transactional (ecosystem) | An exchange venue: the deal happens between the participants, and the platform provides the service and the rules | marketplaces, aggregators of rides and lodging |
| Innovation (ecosystem/technical) | A technology on top of which others build solutions | operating systems, messenger bot platforms, API platforms |
| Integrated | Both the exchange and building solutions on top of the core | an app platform inside a company's ecosystem |

### Types of internal platforms (the course's focus)
1. **Product** — reputation, loyalty, promotion.
2. **Product-tech** — notifications, recommendations, verification.
3. **Technical** — APIs, data platforms, developer tooling.
4. **Infrastructure** — compute, storage, observability.

### Anatomy: core → contracts → customization → client products
- The **core**: shared data, shared logic, a standard product.
- **Contracts**: APIs, formats, access rights — the rules of onboarding.
- **Customization**: settings and extensions within the limits provided by the platform.
- The "already a platform or not yet" test: ≥2 independent clients; the core is separated from extensions (shared code is not edited for every case); onboarding, versioning and support exist. Bottom line: the client builds its own solution on top of the core without the platform being reworked for each scenario.

### Network effects, multi-homing, curation (for ecosystem platforms)
- **Network effect**: the value for a participant grows with the number of participants on the other side (cross-side) or on the same side (same-side). It determines the launch strategy: which side to grow, and when.
- **Multi-homing**: a participant uses several platforms at the same time. The lower the multi-homing costs (moving content, data, habit), the weaker the scale advantage; at the same time it shows where a challenger can catch up with the leader.
- **Curation**: the platform must govern the quality of interactions (rules, verification, ratings) — otherwise a low-quality flow kills the value for the other side. Curation = an instrument of liquidity management ([[M-platform-economics]]).

## Procedure
1. **Classify the situation**: an ecosystem platform or an internal one? If internal — which of the four types. This sets the success metrics (liquidity and side adoption vs team speed and reuse).
2. **Collect the signals that local solutions have stopped being enough** (≥3 from the list is a strong argument): several teams independently build the same function; similar scenarios work under different rules; UX diverges between verticals; supporting local solutions eats ever more time; every connection is done manually; tech debt keeps piling up.
3. **Choose one of the four options** (not everything boils down to "build a platform"):
   - **Keep it local** — one team, a unique scenario, repetition unproven.
   - **Build a shared service** — extract the function with an API, without the platform model (a roadmap, onboarding contracts, support).
   - **Platformize minimally** — extract a small shared core, leave the rest to the teams.
   - **Build the platform** — a separate product for several clients with a development plan, contracts and support.
4. **Run the 4 platformization criteria**:
   - **Scale and repeatability**: ≥ several teams need it now or in the near-term plan; the scenario is recurring; a stable core can be extracted without hurting the teams' goals.
   - **Economics**: `Cost(N × LOCAL) > Cost(CORE + N × INTEGRATION)` — where LOCAL includes development, support, fixes and integrations on each team's side; the platform includes the core, onboarding, compatibility and migrations ([[M-platform-economics]]).
   - **Standardization without losing speed**: the core carries unified entities, rules and quality guarantees; adaptations preserve the differences between scenarios and the teams' pace.
   - **Client readiness**: the value solves the client's problem (rather than only saving the company money); the migration cost has been calculated (integration + data transfer + process changes); a sponsor and an owner exist; the onboarding contract states the constraints, SLA, responsibility and settings.
5. **Check yourself against the anti-patterns**: a platform for the platform's sake (architecture before the shared problem is confirmed); a core that is too wide (the requirements of all possible clients are pre-included in the core); migration without value (moving teams without improving their speed and metrics); universality at any cost (the shared solution breaks important differences between scenarios). First a local MVP and proven repeatability, then the core and contracts.
6. **Choose the level of generalization**: the same capability can be measured at different scales (a private feature → a function → a domain). Run the 4 criteria at each level — the level worth platformizing is the one where all four converge.
7. **Formulate the pros and cons for the defense**: the main change for the business (less duplication, unified UX and rules, economies of scale, the next teams connect faster, lower operating costs) versus the risk (demand unproven, migration expensive, scenarios too divergent, no sponsor, onboarding slows the clients down).

### Example (illustrative numbers, the economics criterion)
The task is needed by 5 teams. Locally: development in each team is 2 months (5 × 2 = 10), repeated rework is 20 × 2 days ≈ 2 months, support is 5 × 0.2 ≈ 1 month → 13 FTE-months. Platform: the core is 3 months + integrations 3 months + client migration and launches 5 months → 11 FTE-months in the first year. The economics close already within the first year; with 6+ clients and zero repeated rework the gap keeps growing. If there were only 2 clients and the scenarios diverged by half, "keep it local" or "a shared service" would win. The conclusion is sensitive to the number of clients and the depth of divergence — calculate over a range.

### Hints for choosing an option
| Situation | The leaning option |
|---|---|
| One team, a unique scenario, repetition unproven | Keep it local |
| Many need the function, but variability is almost zero (we test hypotheses, run A/B) | Shared service |
| The core exists (data, statuses, channels); the differences are in content and rules | Platformize minimally |
| Several independent clients, shared entities exist and new onboarding is expected in the plan | Build the platform |

## Template / checklist
| Check | Yes/No | Comment |
|---|---|---|
| Clients ≥ 2 and they are independent | | |
| The core is separated from extensions | | |
| Onboarding, versions and support exist | | |
| Signals that local solutions are exhausted ≥ 3 | | list which ones |
| `N × LOCAL > CORE + N × INTEGRATION` | | the numbers |
| A sponsor and an owner are appointed | | who |
| Migration cost calculated (in client days) | | |
| Anti-patterns cleared (all 4 items) | | |

Exit artifact: platform type → signals → the chosen option of the four with its justification → scoring against the 4 criteria → the counterargument against platformization.

## Typical mistakes
- Calling shared code with a single real client and no stable contracts a platform.
- Platformizing before value is confirmed on a local MVP (a typical failure: a premature shared reputation/scoring platform — dependencies, migrations and deadlines grow before the demand signal).
- Counting only the reuse benefit and not counting support, compatibility and migrations — a platform's economics don't close right away.
- Building a wide architectural "space shuttle": the system can do everything, but onboarding requires understanding the entire model.
- Ignoring client readiness: "savings for the company" does not motivate the client team that bears the migration costs.

## Questions that can change the decision
- How many teams will face this task next year by plan, rather than "someday"?
- What is the real cost of the core + integrations vs N local solutions over 3–5 years?
- If the core goes down, all clients suffer at once — are you ready to answer for that?
- Are there multi-homing costs for the sides/clients, and can they be raised or lowered in your favor?
- Whom will the platform get in the way of, and how: whose scenario diverges the most ([[M-platform-ecosystem-audit]])?

## Related maps
[[M-platform-ecosystem-audit]], [[M-platform-case-concept]], [[M-platform-economics]], [[M-platform-risks-rollout]], [[M-business-models]], [[M-unit-economics]]
