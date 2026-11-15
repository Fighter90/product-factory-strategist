---
id: M-retention-curves
lang: en
title: Retention curves — shapes (smile curve, plateau, decline), how to read them, cohort curves and benchmarks by industry
course: data
sources: ["EN mirror of the RU methodology card M-retention-curves (knowledge/methods/retention-curves.md); original sources are listed in the RU card"]
stages: [validation]
tags: [retention, retention-curves, cohorts, smile-curve, plateau, benchmarks, churn]
related: [M-product-metrics, M-basic-statistics-pm, M-cjm]
---

# Retention curves: smile, plateau, decline — how to read them and what to compare against

## When to apply
You are assessing whether the product "retains" (a PMF check), preparing data for the traction model and unit economics, comparing cohorts after releases, or choosing the retention measurement window for a report.

## Essence
- **A retention curve** — the % of a cohort (e.g., new users of a week) active on day/week/month N after the first event: the X axis — time since entry, the Y axis — % active. It is computed by cohorts, not over the sum of all users.
- **Three curve shapes**: decline without a plateau (the product does not form a habit — a straight line to zero), a plateau (part of the users has stuck — the target shape: company growth = inflow × plateau level), a smile curve (a dip with a rise — reactivation mechanics, seasonality/usage cycles, or an artifact of the calculation method).
- **The plateau is the main question to a curve.** No plateau — user acquisition is a "leaky bucket": an average mobile app loses ~77% of DAU within 3 days and ~90% within 30 days (Andrew Chen, Quettra data).
- **The definition of "activity" is critical.** Opening the app flatters; count a value event. Different methods (Return On — returned exactly on day N; Return On or After — returned on day N or later) give different curves — fix the method and do not change it between comparisons.
- **Benchmarks depend on the category** (Lenny, retention at ~6 months): consumer social — good ~25% / great ~45%; consumer subscription — ~40% / ~70%; enterprise SaaS — ~70% / ~90%. Compare only against your own type of business: a social network and SaaS live on different planets.
- **The horizon is set by the product's frequency**: a daily product — D-metrics, weekly — W, episodic (marketplace, tours) — M-metrics; otherwise the curve looks dead simply because of the natural usage cycle.
- **Comparing cohorts with each other matters more than the absolute level**: if the newer week's cohorts retain better than older ones — the product is improving; that is the signal for iterations.
- The plateau level is an input for LTV and the growth ceiling in the traction model: it also determines how much you can pay for acquisition.

## How to do it
1. Choose events: cohort start (the first meaningful action) and return event (a value action); fix the method (On / On-or-After) and the granularity per the product's natural frequency.
2. Build cohort curves by entry week; assemble a horizon of at least 8–12 weeks (or months for slow products).
3. Read the shape: where the plateau is, whether there is a smile; check what explains the rise (reactivation e-mails, seasonality, the "incomplete periods" artifact).
4. Compare the plateau level with the benchmark of your category; fix D30/W4/M3/M6 values as reference points.
5. Compare cohorts against each other after every significant change (onboarding, a release, a frequency change) — the plateau shift is the result.
6. Enter the plateau into unit economics and the traction model; revisit it as new cohorts appear.

## Pitfalls
- A "Return On or After" curve over a short horizon rises toward 100% — that is not a plateau, it is the method: read only fully completed periods.
- Activity = "opened the app" — the curve flatters and the plateau is fake; enter through a value event.
- Mixed cohorts (all users at once) average and hide improvements — only separate entry cohorts.
- Comparing against someone else's category: 20% M1 is excellent for a social network, a disaster for enterprise SaaS; a benchmark without context is useless.

## Connections
Builds on `M-product-metrics` (funnels, cohorts, metric tree) and `M-basic-statistics-pm` (noise, intervals, period completeness); the behavioral causes of a curve's shape are sought through `M-cjm`.
