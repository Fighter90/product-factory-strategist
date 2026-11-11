---
id: M-event-taxonomy
lang: en
title: Event taxonomy for product analytics — naming conventions (object-action), tracking plan, properties and anti-patterns
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [validation]
tags: [event-taxonomy, analytics, events, tracking-plan, naming, properties, anti-patterns]
related: [M-product-metrics, M-cjm, M-roadmap]
---

# Event taxonomy: the analytics dictionary before the first line of code

## When to apply
You are introducing product analytics from scratch; the events have grown into a "zoo" and the reports do not reconcile; you are preparing hypothesis validation or A/B tests; you are migrating between analytics tools.

## Core idea
- **Taxonomy = an agreed data dictionary**: which events and properties are tracked, how they are named, who the owner is, where the plan lives. Without it every analyst invents their own names, and one and the same metric sprawls into duplicates.
- **Naming convention object-action**: `[object]_[action]` in the past tense and in one style across the whole project — `song_played`, `signup_completed`, `checkout_initiated`. Casing matters: `Song Played` and `song played` are two different events. The specific style (snake_case/PascalCase) matters less than consistency: the main thing is one style, without exceptions.
- **An event is an action, a property is context.** Do not spawn an event for every variant: one event `order_completed` + properties (`plan`, `payment_method`, `platform`) instead of ten "versions" of the event. Property values are fixed as a list (enum).
- **Three layers of properties**: event properties (what happened), user properties (the profile: plan, role, segment), environment properties (platform, app version, locale) — filled in automatically by the SDK, not by hand.
- **The tracking plan** is a table: name → description (when it fires) → trigger (the exact point in the flow) → required properties and types → owner. The plan is reviewed before implementation, not after.
- **The taxonomy is derived from the metrics, not the other way around**: from the metrics tree and the questions ("what share of new users reaches the value?") to the events that answer them; the event hierarchy mirrors the sections of the product (Account > Authentication > password_reset).
- Hygiene: one stable user identifier, mandatory fields (timestamp, user_id), versioning when the schema changes, a single time zone.

## How to do it
1. Write out 5–10 questions that the analytics must answer (from the metrics tree / NSM / the roadmap's validation plan).
2. Draft the tracking plan: for each question — the events and properties; names per the convention, one-sentence descriptions, an owner for every event.
3. Cross-check against the CJM: every key point of the user journey is covered by an event; the extra ones and the "just in case" ones are crossed out.
4. Align the schema with engineering (types, required properties, triggers), implement and verify event by event in the test environment.
5. Validate the data after the release: event volumes vs the backend numbers, funnel steps not "wider" than the previous one, properties filled in.
6. Governance: any change goes through the tracking plan only; a quarterly audit for duplicates, dead events and gaps.

## Pitfalls
- A zoo of styles and twin events (`signup`, `Signup`, `sign_up`) — one metric lives in three rows of a report, and nobody notices.
- Information in the name instead of properties (`order_completed_premium_card_mobile`) — a combinatorial explosion of events; the context goes into properties.
- "Track everything" with auto-tracking: thousands of events, nothing is analyzed, you pay for volume and noise.
- No owner and no descriptions — in six months nobody remembers what `exp_file_ok` means; renaming live events without a migration plan breaks every report.

## Connections
The events feed `M-product-metrics` (funnels, retention, the metrics tree), cover the journey points from `M-cjm`, and provide the data for hypothesis checking and validation from `M-roadmap`.
