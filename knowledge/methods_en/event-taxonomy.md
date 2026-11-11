---
id: M-event-taxonomy
lang: en
title: Event taxonomy for product analytics — naming conventions (object-action), tracking plan, properties and anti-patterns
course: pm-approaches-en
sources: ["EN summary of the RU methodology card; original sources listed in the RU card"]
stages: [validation]
tags: [en, summary]
related: [M-product-metrics, M-cjm, M-roadmap]
---

# Event Taxonomy (EN summary)

**When:** introducing product analytics from scratch; events have grown into a "zoo" and reports don't reconcile; preparing hypothesis validation or A/B tests; migrating between analytics tools.

**Core:** taxonomy = an agreed data dictionary (which events and properties, how named, who owns each). Naming convention object-action: `[object]_[action]` past tense, one style project-wide (`song_played`, `signup_completed`); casing matters (`Song Played` ≠ `song played`), and consistency beats the specific style. Events are actions, properties are context: one event + properties (`order_completed` with `plan`, `payment_method`) instead of ten event variants; enum values are fixed. Three property layers: event properties, user properties (plan, role), environment properties (platform, app version). The tracking plan is a table: name → description (when it fires) → trigger (exact flow point) → required properties and types → owner; reviewed before implementation. The taxonomy is derived from metrics, not the reverse: questions from the metrics tree → events that answer them; event hierarchy mirrors product areas (Account > Authentication > password_reset). Hygiene: one stable user ID, mandatory fields (timestamp, user_id), schema versioning, one time zone.

**How:** list 5–10 analytics questions (from NSM / metrics tree / roadmap validation) → draft the tracking plan with convention-compliant names and owners → cross-check against the CJM (every key journey point covered, extras cut) → align the schema with engineering, verify event by event in staging → validate production data (counts vs backend, funnel step monotonicity, property fill rates) → governance: changes only via the plan, quarterly audit for duplicates and dead events.

**Pitfalls:** style zoo and twin events (`signup`/`Signup`/`sign_up`) silently split one metric across three rows; information packed into event names instead of properties (`order_completed_premium_card_mobile`) — combinatorial explosion; auto-track-everything: thousands of events, nothing analyzed; no owner/descriptions — in six months nobody knows what `exp_file_ok` means, and renaming live events without a migration plan breaks every report.
