---
id: M-platform-case-concept
lang: en
title: Platform concept — justification, boundaries, MVP, patterns, defense
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [options, strategy]
tags: [platforms, platform-concept, platform-boundary, platform-mvp, integration-patterns, defense, stakeholders]
related: [M-platforms-types-criteria, M-platform-ecosystem-audit, M-platform-economics, M-platform-risks-rollout, M-mvp-pilots, M-product-communication, M-risks]
---

# Platform concept: justification, boundaries, MVP, patterns, defense

## When to apply
"How do you justify a platform opportunity to internal clients and the sponsor?", "what goes into the core and what stays with the client?", "which client to start with and what counts as the platform's MVP?", "which integration pattern to choose and how to defend the concept so that resources are granted?". This map is taken after the audit ([[M-platform-ecosystem-audit]]) and before economics/risks ([[M-platform-economics]], [[M-platform-risks-rollout]]).

## Core idea
A platform is not a technology but a **contract**: an ownership boundary + the price and rules of transition + trust.

### Participants and value
| Role | Responsible for |
|---|---|
| Platform owner | The product and its development |
| Sponsor | Investment, conflict resolution, enforcement of the rules, the first clients |
| Internal clients | Migration to the platform, their own scenarios |
| Teams affected by the migration | Moving their existing solutions over |
| Engineering and other functions (design, legal, etc.) | Building and maintaining |

Value has two levels: **for the company** (less duplication, standardization, economies of scale, quality and risk management) and **for the client** (a faster launch, less in-house development, ready-made data and capabilities, customization to their needs). Conflicts are typical: the platform wants standardization / a long roadmap / fewer exceptions — the client wants specifics / a quick fix / customization and carries the migration costs. Resolution goes through the sponsor and explicit rules.

### Boundaries: three layers and the core test
- **Core** — common to all clients, fully managed by the platform; by placing an element here, the platform takes away the client's right to decide.
- **Adaptations** — client settings within pre-defined frames.
- **Exceptions** — the client builds them themselves outside the platform; the platform is not responsible for the result.

**The core test (3 questions; any "no" → adaptation):** 1) is it identical across all the first clients (not "in theory"); 2) are you ready to answer for it to everyone at once (a core failure breaks everyone); 3) would it hurt to take this element away in a year (narrowing the core is more expensive than widening it: widening costs a sprint, narrowing costs trust). Symmetric risks: a **wide core** — slow onboarding, "half a year spent studying the documentation", the platform gets bypassed; a **narrow core** — "we build everything ourselves anyway", the same code written three times, a service with forks instead of a platform.

**Boundary principles** (from the educational case of a transaction platform): modularity (the client takes part of the core, not all of it); a constructor instead of a finished product (the scenario moves out to the client); flexible participants (roles and their number are a parameter, not a core constant); priorities driven by client requests (the boundary is drawn by the clients, not by the platform team); no business logic in the core.

**The interface as a contract (4 questions):** what the platform guarantees, and at what level (an SLA is a promise, not a metric on a dashboard); what it does NOT guarantee and hands over to the client (an explicit list, otherwise there will be boundary disputes); how the client learns about changes (versions, backward compatibility, the lifetime of the old version); what the first integration costs — in days of the client's work (the comparison is "platform vs doing it yourself in a month", not "platform vs nothing").

### Launch and the platform MVP
- **Top-down (mandate)** — fast rollout and a single standard, but the core is designed without feedback; it works when the benefit is obvious and the directive rests on a strategic choice of the company (the classic example is a large cloud business's mandate for service interfaces). **Bottom-up (voluntary)** — the core is tested on real tasks from day one, but you have to negotiate with every team (an example is an internal development portal that grew out of the needs of its own teams).
- Choosing the first client: top-down — whoever is easiest to onboard (risk: picking the convenient one and never learning about the inconvenient ones); bottom-up — the one whose mechanics look least like yours (risk: tuning the core to exotic cases; discuss the boundary between "the common case vs a special case").
- **A platform MVP = a minimal core + the first client + a testable value hypothesis.** The minimal core is not a stripped-down version of everything: only what the first client cannot get value without (more than three components and it is no longer minimal). The hypothesis is falsifiable: "the client will launch a product in N weeks instead of M months", not "the platform will speed up development". The difference from a product MVP: you prove to an internal team that building on your core is cheaper than building by hand; the price of an error is higher — the client has spent sprints, so the right to be wrong is smaller; a platform has no cheap experiment.
- **MVP ≠ PoC**: a PoC proves feasibility to yourself and to those who give resources (technical in nature; it opens the right to ask for resources); an MVP proves value to the first client (product in nature; it opens the right to go to the next clients). Mixing them up = losing trust at the first bug, or not getting resources.
- **The "point solution → platform" path** consistently beats "platform from day one": generalization based on facts (you know what worked for the first client and what they worked around); a working result within a quarter is itself the argument for resources; the "platform from day one" path without real integrations rests on assumptions. "Platform from day one" is justified only when there is a top-down standard and the variability is known to be small.

### The seven blocks of the concept
1. Problem — what hurts and for whom, in measurable terms. 2. Clients — 2–3 specific teams from the first launches. 3. Core — what is identical across the first clients. 4. Adaptations — what the client configures. 5. Integration — what the client has to do and how many days it will take. 6. Risks — what will kill the endeavor, and the plan ([[M-risks]]). 7. Success criteria — by which metrics the result will be judged in six months.

### Seven integration patterns (the choice — trading flexibility for support cost)
| Pattern | What it gives the client | What you pay |
|---|---|---|
| Shared service | A ready screen/feature "as is", cheap to plug in | The client changes nothing; the owner updates without sign-off |
| Core + adapters | Maximum flexibility: the core + your own case on top | Every client gets their own adapter, which someone maintains for years |
| Design system | A single language, fast assembly of the typical | Non-standard things assemble slower; it speeds up the typical and penalizes the original |
| Event-driven | Loose coupling: a new consumer is added cheaply | When data diverges there is no guilty party — you investigate through the logs of several systems |
| Rules engine | Rules change without a release, experiments run faster | Configuration becomes a second product; nobody will remember "why is the price like this" |
| API-first | Full freedom of interface and scenario | Quality and a consistent experience are controlled by the client, not the platform |
| Boilerplate | Instant start: a copy of the code/a template, full freedom | The connection breaks: versions diverge, one bug gets fixed ten times |

**How to choose (4 questions):** how different the clients are (different → core+adapters / rules engine; similar → shared service); who owns the experience/UX (the client → API-first; the platform → a design system; the choice is irreversible); whether a real-time response is needed (yes → a synchronous call; the fact is enough → event-driven); how often the rules change (often → move them into configuration). The pattern defines **who pays for a change**: core+adapters — the platform; API-first — the client.

### Resources for the prototype
Three options: a dedicated team (it needs goal-setting and a stream), a share of the neighbors' time (hard to coordinate), a feature team inside a unit (self-sufficient, requires no formal goals). Resources are often obtained through a **deal**: trading measurable value "now" (for example, taking on the cluster's tech debt) for team time for the prototype — the exchange must be visible to both sides, otherwise it is a hope, not a plan.

### Defending the concept
Three mandatory parts: **architecture** (the boundary, the pattern, the constraints) + **integration** (onboarding rules and the price in client-days) + **economics** ([[M-platform-economics]]). Scenarios: **defense from the top** — early and upward, defending the idea and its technical validity; **defense from the bottom** — through buy-in: by the time of the defense there are live clients and collected demand (someone who took part in prioritization with clients = an ally). **Client commitment** vs politeness: "interesting, tell us when it's ready" is worth nothing; commitments are: the client put the integration into their quarterly plan, named the pain in numbers, is ready to say it out loud at the defense, confirmed the integration in writing subject to a specific and verifiable deadline. **Turning a limitation into a risk (3 steps):** what will break for the client (not for us) → how we compensate → if it cannot be compensated, say so anyway — the stakeholders must understand what they are agreeing to. A strong defense answers: what exactly we are asking for (people/money/time in numbers); what will count as failure (otherwise any result will be declared a success and the resources cut); the limitations are named honestly, with plans; the need is confirmed by clients, not only by the platform team.

## Procedure
1. **Describe the participants** using the "participants and value" template; for every stakeholder — 5 questions: value (what they gain), risk (what they lose), changes (what they will have to do), success (how they will judge the result), buy-in (under what condition they will agree).
2. **Formulate the value proposition**: "For [internal clients] who [try to get the job done], the solution creates [value] through [a shared capability]. The alternative of [option] is impractical because [argument]".
3. **Draw the boundary**: break the capability down into core/adaptations/exceptions (a table: what · basket · why here · cost of error; at least 2 rows per basket), run the core test on every core row; peer-review someone else's allocation: is it a set of ownership decisions or a feature list; will it answer the client's question "what do I do myself"; is there anything in the core that differs between clients (a wide-core symptom); is there anything in the exceptions that will repeat for everyone (a narrow-core symptom).
4. **Choose the launch** (top-down/bottom-up/hybrid) and the first client against 4 criteria: high motivation (the solution is needed now); a clear and measurable pain that the client names themselves (otherwise it is not a pilot, it is a sale); readiness to integrate (resources in the coming quarter); an influential sponsor (without one, the first priority conflict kills the pilot). Zero on any criterion — do not take them. Score the candidates on a 0–2 scale and justify the choice — "they agreed" is not an answer.
5. **Assemble the MVP**: a minimal core (≤3 components), a testable hypothesis, a failure criterion. Check: is the MVP enough to prove value; what will count as failure.
6. **Choose the pattern** using the 4 questions; fix the integration rules (5 points: guarantees/SLA, what stays with the client, behavior when the platform fails — degradation or a full stop, versioning, the integration cost in client-days).
7. **Plan the resources**: one of the three options, a concrete exchange (what we give today / what we get in return / what the party giving the people receives).
8. **Assemble the 7 blocks of the concept** and prepare the defense: 4 parts of the presentation — problem and clients (who confirmed it and in what form) → the core boundary and the MVP with the first pilot → the integration rules and the integration cost → what we ask for and what we promise in return. Rehearse the stakeholder questions by role (the finance partner, the client's commercial sponsor, the vertical's product leader, the CTO).

## Template / checklist
| Concept section | Content | Check |
|---|---|---|
| Problem | the pain, whose it is, in numbers | the client names it themselves |
| Clients | 2–3 teams, the onboarding order | the 4 pilot criteria, no zeros |
| Core | rows of "what · why · cost of error" | the core test passed |
| Adaptations/exceptions | an explicit list | the client understands what to do themselves |
| Pattern and contract | 7 patterns → the choice; 5 integration rules | the integration cost in client-days |
| MVP and hypothesis | core ≤3, a falsifiable hypothesis | a failure criterion defined |
| Risks | top risks + mitigations | [[M-risks]] |
| Success criteria | metrics in six months | [[M-success-metrics]] |
| Resource request | people/deadline, concretely | the deal is visible to both sides |

Exit artifact: a concept in 7 blocks + the boundary allocation + the integration rules + a defense plan with answers to the stakeholder questions.

## Typical mistakes
- A concept with no owner after launch, no migration rules for the teams with their own solutions (the majority), and no measurable effect — in six months it is cut at the first reprioritization.
- You showed a client a PoC as an MVP (they expect a finished product and lose trust), or showed leadership an MVP instead of a PoC (the question "will it work technically" is unanswered — no resources will be given).
- A core shaped around one strong client's private need; the client's business logic inside the core.
- An SLA "as a metric on a dashboard", with no obligation and no consequences.
- The integration cost estimated in your own estimates, not in days of the client's work.
- "We need leadership support" as the ask, instead of specifics: people, money, time.

## Questions that can change the decision
- What in the client's current solution is expensive, slow or risky — and which part is the platform ready to take over?
- What does the client want to keep under their own control?
- If in a year it turns out that a core element is unnecessary — what will we pay for taking it out?
- Who will become the first client, and why exactly do they give the most learning, rather than just "they agreed"?
- When the platform fails, does the client degrade or stop completely — and will they agree to such a dependency at all?
- Which change will the client pay for, and which will the platform pay for (the pattern)?

## Related maps
[[M-platforms-types-criteria]], [[M-platform-ecosystem-audit]], [[M-platform-economics]], [[M-platform-risks-rollout]], [[M-mvp-pilots]], [[M-product-communication]], [[M-risks]], [[M-success-metrics]]
