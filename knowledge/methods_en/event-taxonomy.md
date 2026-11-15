---
id: M-event-taxonomy
lang: en
title: Event taxonomy for product analytics — naming conventions (object-action), the event plan, properties and antipatterns
course: data
sources: ["EN mirror of the RU methodology card M-event-taxonomy (knowledge/methods/event-taxonomy.md); original sources are listed in the RU card"]
stages: [validation]
tags: [event-taxonomy, analytics, events, tracking-plan, naming, properties, antipatterns]
related: [M-product-metrics, M-cjm, M-roadmap]
---

# Event taxonomy: the analytics dictionary before the first line of code

## When to apply
You are rolling out product analytics from scratch; events have grown into a "zoo" and reports do not reconcile; you are preparing hypothesis validation or A/B tests; you are migrating between analytics tools.

## Essence
- **Taxonomy = an agreed data dictionary**: which events and properties are tracked, how they are named, who owns each one, where the plan lives. Without it every analyst invents their own names, and one and the same metric sprawls into duplicates.
- **Object-action naming convention**: `[object]_[action]` in the past tense and a single style across the whole project — `song_played`, `signup_completed`, `checkout_initiated`. Case matters: `Song Played` and `song played` are two different events. The specific style (snake_case/PascalCase) matters less than having one style: the key thing is a single style without exceptions.
- **An event is an action, a property is context.** Do not spawn an event per variant: one `order_completed` event plus properties (`plan`, `payment_method`, `platform`) instead of ten "versions" of the event. Property values are fixed as an enum list.
- **Three layers of properties**: event properties (what happened), user properties (profile: plan, role, segment), environment properties (platform, app version, locale) — filled in automatically by the SDK, not by hand.
- **The event plan (tracking plan)** is a table: name → description (when it fires) → trigger (the point in the flow) → required properties and types → owner. Review the plan before implementation, not after.
- **The taxonomy is derived from metrics, not the other way around**: from the metric tree and questions ("what share of new users reaches value?") to the events that answer them; the event hierarchy mirrors product sections (Account > Authentication > password_reset).
- Hygiene: one stable user identifier, required fields (timestamp, user_id), versioning on schema changes, a single timezone.

## How to do it
1. Write down 5–10 questions analytics must answer (from the metric tree / NSM / the roadmap's validation plan).
2. Draft the event plan: for each question — events and properties; names per the convention, descriptions in one sentence, an owner for every event.
3. Cross-check against the CJM: every key point of the user journey is covered by an event; redundant and "just in case" events are crossed out.
4. Agree the schema with engineering (types, required properties, triggers), implement and verify event by event in a staging environment.
5. Validate the data after release: event volumes vs backend numbers, funnel steps not "wider" than the previous one, properties populated.
6. Governance: any change goes only through the event plan; a quarterly audit for duplicates, dead events and gaps.

## Pitfalls
- A zoo of styles and twins (`signup`, `Signup`, `sign_up`) — one metric lives in three rows of a report and nobody notices.
- Information in the name instead of properties (`order_completed_premium_card_mobile`) — a combinatorial explosion of events; context belongs in properties.
- "Track everything" with auto-tracking: thousands of events, nothing is analyzed, you pay for volume and noise.
- No owner and no descriptions — six months later nobody remembers what `exp_file_ok` means; renaming live events without a migration plan breaks every report.

## Connections
Events feed `M-product-metrics` (funnels, retention, the metric tree), cover the journey points from `M-cjm` and provide the data for checking hypotheses and validation from `M-roadmap`.
