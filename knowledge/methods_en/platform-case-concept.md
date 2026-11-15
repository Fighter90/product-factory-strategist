---
id: M-platform-case-concept
lang: en
title: Platform concept: justification, boundaries, MVP, patterns, defense
course: strategy
sources: ["EN mirror of the RU methodology card M-platform-case-concept (knowledge/methods/platform-case-concept.md); original sources are listed in the RU card"]
stages: [options, strategy]
tags: [platforms, concept, platform-boundaries, platform-mvp, integration-patterns, defense, stakeholders]
related: [M-platforms-types-criteria, M-platform-ecosystem-audit, M-platform-economics, M-platform-risks-rollout, M-mvp-pilots, M-product-communication, M-risks]
---

# Platform Concept: Justification, Boundaries, MVP, Patterns, Defense

## When to apply
"How do we justify a platform opportunity to internal clients and the sponsor?", "what goes into the core, and what stays with the client?", "which client to start with and what counts as the platform's MVP?", "which integration pattern to choose and how to defend the concept so that resources are granted?". This card is taken after the audit ([[M-platform-ecosystem-audit]]) and before the economics/risks ([[M-platform-economics]], [[M-platform-risks-rollout]]).

## Essence
A platform is not a technology but a **contract**: a boundary of ownership + the price and rules of transition + trust.

### Participants and value
| Role | Responsible for |
|---|---|
| Platform owner | The product and its development |
| Sponsor | Investment, conflict resolution, backing the rules, the first clients |
| Internal clients | Moving onto the platform, their own scenario |
| Teams affected by migration | Carrying over existing solutions |
| Development and other functions (design, legal, etc.) | Creation and support |

The value has two levels: **for the company** (less duplication, standardization, economies of scale, quality and risk management) and **for the client** (a faster launch, less of their own development, ready data and capabilities, customization). Conflicts are typical: the platform wants standardization / a long roadmap / fewer exceptions — the client wants specificity / a fast solution / customization and bears migration costs. The resolution — through the sponsor and explicit rules.

### Boundaries: three layers and the core test
- **Core** — shared by all clients, fully managed by the platform; by placing an element here the platform takes away the client's right to decide.
- **Adaptations** — the client's settings within pre-built frames.
- **Exceptions** — the client does them themselves outside the platform; the platform is not responsible for the result.

**The core test (3 questions; any "no" → adaptation):** 1) is this the same for all first clients (not "in theory"); 2) are we ready to answer for it to everyone at once (a core failure breaks everyone); 3) will it hurt to take it away a year from now (shrinking the core is more expensive than expanding: expansion costs a sprint, shrinking costs trust). Symmetric risks: a **wide core** — long onboarding, "we studied the documentation for half a year", the platform gets bypassed; a **narrow core** — "we'll do it our own way anyway", the same code gets written three times, a service with forks instead of a platform.

**Boundary principles** (from the educational case of a transactional platform): modularity (the client takes part of the core, not all of it); a constructor instead of a finished product (the scenario is pushed out to the client); flexible participants (roles and their number are a parameter, not a constant of the core); priorities set by client requests (the boundary is drawn by the clients, not the platform team); no business logic in the core.

**The interface as a contract (4 questions):** what and at which level the platform guarantees (SLA — a promise, not a metric on a dashboard); what it does NOT guarantee and hands to the client (an explicit list, otherwise boundary disputes); how the client learns about changes (versions, backward compatibility, the lifetime of an old version); how much the first integration costs — in days of client work (a comparison "platform vs doing it yourself in a month", not "platform vs nothing").

### Launch and the platform MVP
- **From the top (a mandate)** — fast spread and a single standard, but the core is designed without feedback; it works if the benefit is obvious and the directive stands on a strategic choice of the company (the classic example — a mandate of a major cloud business for service interfaces). **From the bottom (voluntary)** — the core is tested on real tasks from day one, but you need to negotiate with every team (an example — an internal developer portal that grew out of the needs of its own teams).
- Choosing the first client: from the top — whoever is easier to onboard (the risk: taking the convenient one and not learning about the inconvenient); from the bottom — whoever's mechanics are least like yours (the risk: shaping the core for an exotic case; discuss the boundary "general vs a special case").
- **The platform's MVP = a minimal core + the first client + a testable value hypothesis.** The minimal core is not a cut-down version of everything: only what, without which, the first client gets no value (more than three components is no longer minimal). The hypothesis is falsifiable: "the client will launch a product in N weeks instead of M months", not "the platform will speed up development". The difference from a product's MVP: we prove to an internal team that our core is cheaper than doing it by hand; the price of error is higher — the client spent sprints, the right to error is smaller; the platform has no cheap experiment.
- **An MVP ≠ a PoC**: a PoC proves feasibility to ourselves and to those giving resources (a technical nature, opens the right to ask for resources); an MVP proves value to the first client (a product nature, opens the right to go to the next clients). Confusing them = losing trust at the first bug or not getting resources.
- **The path "point solution → platform"** consistently beats "platform right away": generalization on facts (we know what worked at the first client and what they bypassed); a working result within a quarter is itself the argument for resources; the "platform right away" path without real integrations rests on assumptions. "Platform right away" is justified only with a top-down standard and knowingly low variability.

### The seven blocks of the concept
1. Problem — what hurts and for whom, in measurable quantities. 2. Clients — 2–3 specific teams of the first launches. 3. Core — what is identical across the first clients. 4. Adaptations — what the client configures. 5. Integration — what the client must do and how many days it will take. 6. Risks — what will kill the endeavor, and the plan ([[M-risks]]). 7. Success criteria — by which indicators the result will be judged six months later.

### The seven integration patterns (choosing = trading flexibility for the cost of support)
| Pattern | What it gives the client | What we pay |
|---|---|---|
| Shared service | A ready screen/function "as is", cheap to connect | The client changes nothing; the owner updates without approval |
| Core + adapters | Maximum flexibility: the core + your case on top | Every client has their own adapter, which someone supports for years |
| Design system | A single language, fast assembly of the typical | The non-standard assembles slower; it speeds up the typical, penalizes the original |
| Event-driven | Loose coupling: a new consumer is added cheaply | When data diverges there is no guilty party — you dig through the logs of several systems |
| Rules engine | Rules change without a release, faster experiments | The configuration becomes a second product; nobody will remember "why this price" |
| API-first | Full freedom of interface and scenario | The client, not the platform, controls quality and a unified experience |
| Boilerplate | An instant start: a copy of code/a template, full freedom | The connection breaks: versions diverge, one bug gets fixed ten times |

**How to choose (4 questions):** how different the clients are (different → core+adapters / rules engine; similar → shared service); who owns the experience/UX (the client → API-first; the platform → design system; the choice is irreversible); whether real-time reaction is needed (yes → a synchronous call; the fact is enough → event-driven); how often the rules change (often → move them into configuration). The pattern defines **who pays for a change**: core+adapters — the platform, API-first — the client.

### Resources for the prototype
Three options: a dedicated team (needs goal-setting and a stream), a share of neighbors' time (hard to coordinate), a feature team inside a unit (self-sufficient, needs no formal goals). Resources are often obtained **by a deal**: an exchange of measurable value "now" (for example, taking on the cluster's tech debt) for the team's time for the prototype — the exchange must be visible to both sides, otherwise it is hope, not a plan.

### Defending the concept
Three mandatory parts: **architecture** (the boundary, the pattern, the constraints) + **integration** (the onboarding rules and the price in days of client work) + **economics** ([[M-platform-economics]]). Scenarios: **defense from the top** — early and upward, defending the idea and its technical soundness; **defense from the bottom** — through buy-in, with live clients and collected demand by the time of the defense (a participant in prioritization with clients = an ally). **The client's commitment** vs politeness: "interesting, tell us when it's done" is worth nothing; commitments are: they put the integration into their quarterly plan, named the pain in numbers, are ready to say it out loud at the defense, confirmed the connection in writing subject to a specific and verifiable deadline. **Turning a constraint into a risk (3 steps):** what breaks at the client (not at us) → how we compensate → if it cannot be compensated, name it anyway — stakeholders must understand what they agree to. A strong defense answers: what exactly we ask for (people/money/time in numbers); what will count as failure (otherwise any result will be declared a success and resources will be cut); constraints named honestly with plans; the need confirmed by clients, not only by the platform team.

## Procedure
1. **Describe the participants** using the "participants and value" template; for each stakeholder — 5 questions: value (what they get), risk (what they lose), changes (what they must do), success (how they will judge the result), buy-in (under which condition they will agree).
2. **Formulate the value proposition**: "For [internal clients] who [try to get a job done], the solution creates [value] through [a shared capability]. The alternative of [option] is impractical because [argument]".
3. **Draw the boundary**: decompose the opportunity into core/adaptations/exceptions (a table: what · bucket · why here · the price of error; at least 2 rows per bucket), run the core test on each core row; peer-review someone else's layout: are these decisions about ownership or a list of features; will it answer the client's "what should I do myself"; is there anything in the core that differs across clients (a symptom of a wide core); is there anything in the exceptions that will repeat for everyone (a symptom of a narrow one).
4. **Choose the launch** (top-down/bottom-up/hybrid) and the first client on 4 criteria: high motivation (the solution is needed now); a clear and measurable pain the client names themselves (otherwise it is not a pilot but a sale); readiness for integration (a resource in the nearest quarter); an influential sponsor (without one the first conflict of priorities kills the pilot). Zero on any criterion — we do not take it. Rate candidates on a 0–2 scale and justify the choice — "they agreed" is not an answer.
5. **Assemble the MVP**: a minimal core (≤3 components), a testable hypothesis, a failure criterion. Check: is the MVP enough to prove value; what will count as failure.
6. **Choose the pattern** on the 4 questions; fix the integration rules (5 points: guarantees/SLA, what stays with the client, behavior on platform failure — degradation or stop, versioning, the cost of onboarding in days of client work).
7. **Plan the resources**: one of the three options, a concrete exchange (what we give today / what we take in return / what the party giving people gets).
8. **Assemble the 7 blocks of the concept** and prepare the defense: 4 blocks of the talk — the problem and clients (who confirmed it and in what form) → the core boundary and the MVP with the first pilot → the integration rules and the cost of onboarding → what we ask for and what we promise in return. Rehearse the stakeholders' questions by role (the financial partner, the commercial sponsor of the client, the product leader of the vertical, the CTO).

## Template / checklist
| Section of the concept | Content | Check |
|---|---|---|
| Problem | the pain, for whom, in numbers | the client names it themselves |
| Clients | 2–3 teams, the order of onboarding | the 4 pilot criteria, no zeros |
| Core | rows "what · why · the price of error" | the core test passed |
| Adaptations/exceptions | an explicit list | the client understands what to do themselves |
| Pattern and contract | the 7 patterns → the choice; the 5 integration rules | the cost of onboarding in days of client work |
| MVP and hypothesis | a core ≤3, a falsifiable hypothesis | a failure criterion defined |
| Risks | top risks + mitigations | [[M-risks]] |
| Success criteria | metrics six months later | [[M-success-metrics]] |
| The resource ask | people/dates concretely | the deal visible to both sides |

Exit artifact: a concept in 7 blocks + the boundary layout + the integration rules + a defense plan with answers to stakeholders' questions.

## Typical mistakes
- A concept without an owner after launch, without rules for migrating teams with their own solutions (they are the majority) and without a measurable effect — six months later it gets cut at the first re-prioritization.
- Showing a PoC to the client as an MVP (they expect a finished product and lose trust), or showing leadership an MVP instead of a PoC (the question "will it work technically" unanswered — no resources).
- A core shaped for a strong client's private need; the client's business logic in the core.
- An SLA "as a metric on a dashboard" without an obligation and consequences.
- The cost of onboarding computed in our own estimates, not in days of client work.
- "We need leadership support" as the ask instead of specifics: people, money, time.

## Questions that can change the decision
- What in the client's current solution is expensive, slow or risky — and which part is the platform ready to take?
- What does the client want to keep under their own control?
- If a year from now a core element turns out to be redundant — what will we pay for its removal?
- Who will be the first client, and why exactly do they give the most learning, and not merely "agreed"?
- If the platform fails, does the client degrade or stop entirely — and will they accept such a dependency at all?
- For which change does the client pay, and for which the platform (the pattern)?

## Related cards
[[M-platforms-types-criteria]], [[M-platform-ecosystem-audit]], [[M-platform-economics]], [[M-platform-risks-rollout]], [[M-mvp-pilots]], [[M-product-communication]], [[M-risks]], [[M-success-metrics]]
