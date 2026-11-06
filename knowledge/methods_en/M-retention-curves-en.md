---
id: M-retention-curves-en
title: Retention curves — smile curve, plateau, decay; how to read them, cohort curves and industry benchmarks
course: pm-approaches-en
sources: ["EN summary of the RU methodology card; original sources listed in the RU card"]
stages: [validation]
tags: [en, summary]
related: []
---

# Retention Curves (EN summary)

**When:** assessing whether the product "sticks" (PMF check), feeding retention data into the traction model and unit economics, comparing cohorts after releases, or choosing the measurement window for retention reporting.

**Core:** a retention curve plots the % of a cohort (e.g., weekly new users) active at day/week/month N after their first event. Three shapes: continuous decay (no habit — straight to zero), plateau (a stable core — the target shape; growth = inflow × plateau level), smile curve (dip and rise — reactivation mechanics, usage cycles, or a measurement artifact). No plateau means acquisition is a leaky bucket: the average mobile app loses ~77% of DAU in 3 days and ~90% in 30 days (Andrew Chen, Quettra data). "Active" must mean a value event, not app opens; fix the counting method (Return On vs Return On or After) and never change it between comparisons. Benchmarks are category-specific (Lenny, ~6-month retention): consumer social good ~25% / great ~45%; consumer subscription ~40% / ~70%; enterprise SaaS ~70% / ~90%. Measurement granularity follows natural usage frequency (daily → D-metrics, weekly → W, episodic → M). Cohort-to-cohort comparison matters more than the absolute level: improving younger cohorts = improving product. The plateau level feeds LTV and the growth ceiling in the traction model.

**How:** pick start and return events (value action), fix method and granularity → build cohort curves over 8–12 weeks/months → read the shape (plateau? smile? artifact?) → benchmark against your own category, record D30/W4/M3/M6 → compare cohorts after every significant change → feed the plateau into unit economics and the traction model.

**Pitfalls:** "On-or-After" curves rise toward 100% on short horizons — method artifact, not a plateau; activity defined as app opens flatters the curve; merged (non-cohort) data hides improvements; benchmarking against a foreign category (social vs SaaS) is meaningless.

**RU-версия:** `knowledge/methods/M-retention-curves.md` (полная методика).
