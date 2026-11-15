---
id: M-platform-ecosystem-audit
lang: en
title: Product ecosystem audit for finding platform opportunities
course: strategy
sources: ["EN mirror of the RU methodology card M-platform-ecosystem-audit (knowledge/methods/platform-ecosystem-audit.md); original sources are listed in the RU card"]
stages: [research, options]
tags: [platforms, audit, ecosystem, domain, scenarios, platformization-candidates]
related: [M-platforms-types-criteria, M-platform-case-concept, M-platform-economics, M-platform-risks-rollout, M-source-criticism, M-unit-economics]
---

# Product Ecosystem Audit for Finding Platform Opportunities

## When to apply
"Where and why in our product portfolio is it worth building a platform?", "which functions are duplicated across teams and is there a shared core there?", "what to propose for platformization and how to justify it to stakeholders?". The first step of the platform track after the basic concepts ([[M-platforms-types-criteria]]).

## Essence
The audit answers three questions: **where** a platform should be built, **why a platform** (and not some other solution) and **why stakeholders will "buy" it**.

### Start from the problem, not the solution
| Started from a solution (bad) | Started from a problem (right) |
|---|---|
| "Let's build platform X" | Several teams solve a similar task in different ways |
| The architecture thought through before the problem and the core's composition | There is a confirmed problem of clients or stakeholders — now the form of the shared solution is chosen |

### The four sources of opportunities (found in regular work)
1. **Extending the product** — a mechanic is carried into a new scenario or vertical.
2. **A shared CJM** — similar steps of the user journey are built differently in different places of the product.
3. **Team requests** — several teams request similar capabilities.
4. **Identical changes** — the same change repeats across several products (e.g., a switch to a new monetization model in every direction).

### Four lenses on a product domain: scenarios → interfaces → implementations → clients
- **Scenarios** — what the user does (viewing an item page, trust in a purchase, profile, communication, transaction…).
- **Interfaces** — where in the product the scenario is implemented (the home page, vertical home pages, the account, the cart…).
- **Implementations** — what is shared in them and what differs (shared logic and elements vs different fields, conditions, behavior).
- **Clients** — who owns the current solutions and who uses them.

If the implementations contain material for something shared (a core) and differences that clients will customize themselves (customization) — this is a **platformization candidate**.

Additionally, register the **contracts and rules** that have already de facto emerged around the shared part: data formats, listing rules, access rights. If the shared rules exist informally ("that's what we agreed on"), it confirms that the shared core is genuinely in demand — and needs an owner.

## Procedure
1. **Choose a domain** and write out 3–5 user scenarios in it (not functions — user scenarios).
2. **Fill in the scenario map** for each: where it occurs in the product → examples of implementations in different verticals/places → what is shared and what differs. In the "shared and differences" column, separate: (a) what is identical and standardizable — material for the core; (b) what meaningfully differs and will be refined by clients — material for customizations; (c) what is still unknown — flag as a hypothesis (not a fact).
3. **Register the owners**: for every current solution — the owning team and the using teams. Candidates for the platform's clients = owners of similar solutions + teams without a solution that will soon need one.
4. **Form the shortlist of candidates** (2–3): for each — what repeats, what gets customized by clients, who owns the core, who the clients are.
5. **Run the platformization criteria** on each candidate ([[M-platforms-types-criteria]]): scale, repeatability and a shared core, the economics `N × LOCAL > CORE + N × INTEGRATION`, standardization, client readiness.
6. **Check the alternatives** — explain why a simpler solution will not do: keep it local; agree on rules (without shared code); build a library/design components; build a service or an API; carve out a minimal core.
7. **Assess stakeholder acceptance**: the candidate must have value for the owner, the clients and the sponsor — otherwise the audit is not finished ([[M-platform-case-concept]]).
8. **Frame the hypothesis**: the platform solution will have users, and its economics will be justified. This is verified by an MVP and a calculation ([[M-platform-economics]]) — after the audit these are hypotheses, not facts.

### An example scenario analysis (illustrative)
The scenario "trust in a purchase" (a trust badge/emblem on the offer card):
- where it occurs: the offer card, the vertical's home page, the results listing;
- shared: the presence of a visual element, a details window on click, the design code, mandatory attributes (an image, a title, text, a button), the fact and history of granting;
- differences: texts and images, the button's action, granting conditions, additional attributes (e.g., the year of the nomination);
- conclusion: the element, the window and the design code are core candidates; the texts, granting conditions and extra attributes go to adaptations; the differences are meaningful, so the core must be narrow with settings, not a "universal badge".

### Typical domains for an audit (where to start looking)
- **The user profile** — including the public profile.
- **Viewing an offer** — cards, listings, recommendations.
- **Rating participants** — ratings, reviews, complaints.
- **Communication** — notifications, messenger, calls.
- **A purchase with a transaction** — payment, delivery, statuses, delivery services.

For every domain the audit follows the same scenario map — this makes the candidates comparable with each other.

## Template / checklist
**The product domain map** (for each scenario):
| Scenario | Where in the product it is implemented | Examples in different verticals/products | Shared (→ core) | Differences (→ customization) | Solution owner | Clients/users | Fact/hypothesis |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

**The platformization candidates table**:
| Candidate | What repeats | What gets customized by clients | Core owner | Clients | Passed the 4 criteria? | Why the alternative does not fit |
|---|---|---|---|---|---|---|
| | | | | | | |

Auto-checks:
- In every row of the map it is marked what is fact and what is hypothesis, and with which confidence class ([[M-source-criticism]]).
- "Owner" is filled in for all current implementations; "clients" — not only vertical teams (support and marketing too).
- For each candidate a concrete alternative is named and the reason for rejecting it.
- The signals from [[M-platforms-types-criteria]] are sufficient (≥3) — otherwise the audit found "shared things" but did not show that the local solutions are exhausted.

## Typical mistakes
- Starting with "let's build platform X" and fitting the problem to the architecture.
- Confusing a function with a scenario: an audit over a feature list does not find the shared core of the user journey.
- Recording implementation differences as "everyone does it their own way, so we need a wide universal standard" — the differences may be meaningful and stay in customizations.
- Accounting only for product verticals and missing horizontal clients (support, marketing, analytics).
- Not flagging the gaps: "unknown" in the map must stay visible and go into the verification plan, not be erased when the document is reworked.
- Not flagging the unknown: a map without a "hypothesis" flag turns assumptions into "facts" at the defense.

## Questions that can change the decision
- Which share of the "differences" between implementations is genuinely meaningful scenario specifics, and not accumulated crutches?
- What does it cost now to support all local solutions (FTE per quarter), and what does "doing nothing" for another year cost?
- Is there a team whose solution is mature enough to become the basis of the core?
- Which owners of similar solutions will feel pain from losing control, and how do we cover it?
- Which change in one scenario repeats the most in others (a shared CJM)?
- Which of the 2–3 candidates will produce the first verifiable result fastest — start the assessment with it ([[M-platform-case-concept]])?

## Related cards
[[M-platforms-types-criteria]], [[M-platform-case-concept]], [[M-platform-economics]], [[M-platform-risks-rollout]], [[M-source-criticism]], [[M-unit-economics]]
