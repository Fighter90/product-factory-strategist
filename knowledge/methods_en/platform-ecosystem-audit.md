---
id: M-platform-ecosystem-audit
lang: en
title: Product ecosystem audit for finding platform opportunities
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [research, options]
tags: [platforms, audit, ecosystem, product-domain, scenarios, platformization-candidates]
related: [M-platforms-types-criteria, M-platform-case-concept, M-platform-economics, M-platform-risks-rollout, M-source-criticism, M-unit-economics]
---

# Product ecosystem audit for finding platform opportunities

## When to apply
"Where and why in our product portfolio should we build a platform?", "which functions are duplicated across teams and is there a common core there?", "what to propose for platformization and how to justify it to stakeholders?". The first step of the platform track after the basic concepts ([[M-platforms-types-criteria]]).

## Core idea
The audit answers three questions: **where** to build a platform, **why a platform specifically** (and not another solution) and **why stakeholders will "buy" it**.

### Start from the problem, not the solution
| Started from a solution (bad) | Started from a problem (right) |
|---|---|
| "Let's create platform X" | Several teams solve a similar task in different ways |
| The architecture is designed before the problem and the composition of the core | There is a confirmed problem of clients or stakeholders — now the form of the shared solution is chosen |

### Four sources of opportunities (found in regular work)
1. **Extending the product** — a mechanic is carried over into a new scenario or vertical.
2. **A shared CJM** — similar user-journey steps are built differently in different places of the product.
3. **Team requests** — several teams request similar capabilities.
4. **Identical changes** — the same change repeats across several products (for example, a migration to a new monetization model across all directions).

### Four lenses on a product domain: scenarios → interfaces → implementations → clients
- **Scenarios** — what the user does (viewing a card, trust in a purchase, profile, communication, transaction…).
- **Interfaces** — where in the product the scenario is implemented (the main page, vertical homepages, the account, the cart…).
- **Implementations** — what in them is shared and what differs (shared logic and elements vs different fields, conditions, behavior).
- **Clients** — who owns the current solutions and who uses them.

If the implementations contain material for something shared (a core) plus differences that clients will refine themselves (customization) — we are looking at a **platformization candidate**.

Additionally, record the **contracts and rules** that have already de facto appeared around the shared part: data formats, serving rules, access rights. If shared rules exist informally ("that's how we agreed"), this confirms that the common core is genuinely in demand — and that it needs an owner.

## Procedure
1. **Pick a domain** and write out 3–5 user scenarios in it (not features — user scenarios).
2. **Fill in the scenario map** for each: where it occurs in the product → implementation examples across verticals/places → what is shared and what differs. In the "shared and differences" column, separate: (a) what is identical and standardizable — material for the core; (b) what differs meaningfully and will be refined by the clients — material for customizations; (c) what is still unknown — mark it as a hypothesis (not a fact).
3. **Fix the owners**: for each current solution — the owning team and the user teams. Candidates for platform clients = the owners of similar solutions + teams without a solution who will need one soon.
4. **Build the candidate shortlist** (2–3): for each — what repeats, what the clients refine, who owns the core, who the clients are.
5. **Run the platformization criteria** for each candidate ([[M-platforms-types-criteria]]): scale, repeatability and a common core, the economics of `N × LOCAL > CORE + N × INTEGRATION`, standardization, client readiness.
6. **Check the alternatives** — explain why a simpler solution won't do: keep it local; agree on rules (without shared code); make a library/design components; make a service or an API; extract a minimal core.
7. **Assess stakeholder adoption**: the candidate must have value for the owner, the clients and the sponsor — otherwise the audit is not finished ([[M-platform-case-concept]]).
8. **Frame the hypothesis**: the platform solution will have users, and its economics will be justified. This is verified by an MVP and a calculation ([[M-platform-economics]]) — after the audit these are hypotheses, not facts.

### Example scenario breakdown (illustrative)
The scenario "trust in a purchase" (a trust badge on the offer card):
- where it occurs: the offer card, the vertical's main page, the results listing;
- shared: the presence of a visual element, a details window on click, the design code, mandatory attributes (image, title, text, button), the fact and the history of issuance;
- differences: the texts and images, the button's action, the issuance conditions, additional attributes (for example, the year of the award);
- conclusion: the element, the window and the design code are candidates for the core; the texts, the issuance conditions and the extra attributes go to adaptation; the differences are meaningful, which means the core must be narrow with settings, not a "universal badge".

### Typical domains for an audit (where to start looking)
- **User profile** — including the public profile.
- **Offer viewing** — cards, listings, recommendations.
- **Rating of participants** — ratings, reviews, complaints.
- **Communication** — notifications, messenger, calls.
- **Purchase with a transaction** — payment, delivery, statuses, delivery services.

For every domain the audit runs with the same scenario map — this makes the candidates comparable with each other.

## Template / checklist
**Product domain map** (for each scenario):
| Scenario | Where it is implemented in the product | Examples across verticals/products | Shared (→ core) | Differences (→ customization) | Solution owner | Clients/users | Fact/hypothesis |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

**Platformization candidate table**:
| Candidate | What repeats | What the clients refine | Core owner | Clients | Passed the 4 criteria? | Why the alternative does not fit |
|---|---|---|---|---|---|---|
| | | | | | | |

Self-checks:
- Each row of the map marks what is a fact and what is a hypothesis, and the evidence class ([[M-source-criticism]]).
- "Owner" is filled in for all current implementations; "clients" — not only the vertical teams (support and marketing too).
- For each candidate a specific alternative is named and the reason for rejecting it.
- The signals from [[M-platforms-types-criteria]] are sufficient (≥3) — otherwise the audit found "shared" things but did not show that the local solutions are exhausted.

## Typical mistakes
- Starting with "let's build platform X" and fitting the problem to the architecture.
- Confusing a feature and a scenario: an audit over a feature list does not find the common core of the user journey.
- Writing the differences between implementations off as "everyone does it their own way, so we need one wide universal standard" — the differences can be meaningful and stay in customizations.
- Counting only the product verticals and missing the horizontal clients (support, marketing, analytics).
- Not marking the gaps: "unknown" in the map must stay visible and go into the validation plan, not be erased when the document is re-formatted.
- Not marking the unknown: a map without a "hypothesis" flag turns assumptions into "facts" at the defense.

## Questions that can change the decision
- What share of the "differences" between implementations is genuinely meaningful scenario specifics, rather than accumulated crutches?
- How much does the support of all the local solutions cost now (FTE per quarter), and how much does "doing nothing" for another year cost?
- Is there a team whose solution is mature enough that it makes sense to take it as the basis of the core?
- Which owners of similar solutions will feel the pain of losing control, and how do we close it?
- Which change in one scenario repeats the most in the others (a shared CJM)?
- Which of the 2–3 candidates will produce the first verifiable result fastest — start the assessment with that one ([[M-platform-case-concept]])?

## Related maps
[[M-platforms-types-criteria]], [[M-platform-case-concept]], [[M-platform-economics]], [[M-platform-risks-rollout]], [[M-source-criticism]], [[M-unit-economics]]
