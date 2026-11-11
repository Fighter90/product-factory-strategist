---
id: M-retention-curves
lang: en
title: Retention curves — shapes (smile curve, plateau, decay), how to read them, cohort curves and industry benchmarks
course: pm-approaches-en
sources: ["Lenny Rachitsky, What is good retention (good/great benchmarks by business type) — https://www.lennysnewsletter.com/p/what-is-good-retention-issue-29", "Andrew Chen, New data shows losing 80% of mobile users is normal (app retention curve data) — https://andrewchen.com/new-data-shows-why-losing-80-of-your-mobile-users-is-normal-and-that-the-best-apps-do-much-better", "Amplitude Docs, Build a retention analysis (Retain On vs Return On or After) — https://www.amplitude.com/docs/analytics/charts/retention-analysis/retention-analysis-build"]
stages: [validation]
tags: [retention, retention-curves, cohorts, smile-curve, plateau, benchmarks, churn]
related: [M-product-metrics, M-basic-statistics-pm, M-cjm]
---

# Retention curves: smile, plateau, decay — how to read them and what to compare against

## When to apply
You are assessing whether the product "sticks" (a PMF check), preparing data for the traction model and unit economics, comparing cohorts after releases, or choosing the measurement period for retention in reports.

## Core idea
- **A retention curve** — the % of a cohort (e.g., the week's new users) that is active on day/week/month N after the first event: the X-axis is time since entry, the Y-axis is % active. It is computed per cohort, not across all users summed together.
- **Three curve shapes**: decay without a plateau (the product does not form a habit — a straight line to zero), a plateau (part of the users has stuck — the target shape: company growth = inflow × plateau level), a smile curve (a dip with a rise — reactivation mechanics, seasonality/usage cycles, or an artifact of the calculation method).
- **The plateau is the main question to ask of the curve.** No plateau — user acquisition is a "leaky bucket": the average mobile app loses ~77% of DAU within 3 days and ~90% within 30 days (Andrew Chen, Quettra data).
- **The definition of "active" is critical.** App opens flatter you; count a value event. Different methods (Return On — returned exactly on day N; Return On or After — returned on day N or later) produce different curves — fix the method and do not change it between comparisons.
- **Benchmarks depend on the category** (Lenny, retention at the ~6-month horizon): consumer social — good ~25% / great ~45%; consumer subscription — ~40% / ~70%; enterprise SaaS — ~70% / ~90%. Compare only with your own type of business: a social network and SaaS live on different planets.
- **The horizon is set by the product's frequency**: a daily product — D-metrics, a weekly one — W, an episodic one (marketplace, travel) — M-metrics; otherwise the curve looks dead simply because of the natural usage cycle.
- **Cohort-to-cohort comparison matters more than the absolute level**: if the newer weeks retain better than the older ones — the product is improving; that is exactly the signal for iteration.
- The plateau level is an input for LTV and the growth ceiling in the traction model: it also determines how much you can pay for acquisition.

## How to do it
1. Choose the events: the cohort start (the first meaningful action) and the return event (a value action); fix the method (On / On-or-After) and the granularity according to the product's natural frequency.
2. Build cohort curves by entry week; collect a horizon of at least 8–12 weeks (or months for slow products).
3. Read the shape: where the plateau is, whether there is a smile; check what explains the rise (reactivation emails, seasonality, the "incomplete periods" artifact).
4. Compare the plateau level with a benchmark for your category; record the D30/W4/M3/M6 values as reference points.
5. Compare cohorts against each other after every significant change (onboarding, a release, a change in frequency) — the shift of the plateau is the result.
6. Put the plateau into unit economics and the traction model; revisit it as new cohorts appear.

## Pitfalls
- A "Return On or After" curve on a short horizon grows toward 100% — this is not a plateau but the method: read only fully completed periods.
- Activity = "opened the app" — the curve flatters you and the plateau is fake; go in through a value event.
- Mixed cohorts (all users at once) average things out and hide improvements — only separate entry cohorts.
- Comparison with someone else's category: 20% M1 is excellent for a social network and a disaster for enterprise SaaS; a benchmark without context is useless.

## Connections
Builds on `M-product-metrics` (funnels, cohorts, the metric tree) and `M-basic-statistics-pm` (noise, intervals, period completeness); the behavioral reasons for a curve's shape are traced through `M-cjm`.
