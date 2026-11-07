---
id: M-benchmarking-en
title: Benchmarking — reference values for retention, conversion, churn, CAC; P25–P50–P95 ranges, comparability checks, biases, triangulation
course: pm-approaches-en
sources: ["EN summary of the RU methodology card; original sources listed in the RU card"]
stages: [research, options, validation, after-decision]
tags: [en, summary]
related: []
---

# Benchmarking (EN summary)

**When:** "what retention/conversion/churn/CAC is considered normal?"; "are our metrics better or worse than the market?"; "where do I get an assumption for a model with no data?"; "can I trust this number from an article?"; "which best practices should we adopt?" The card teaches how to find and verify benchmarks — the numbers themselves come from sources with a confidence grade.

**Core:** a benchmark is a reference value of a metric for comparison. What counts as "reference" depends on the goal: best (P95/P99) — aspiration; median (P50) — realistic industry level; minimum (P25) — below is dangerous. Always use a **P25–P50–P95 range**, never one number; a benchmark is a compass, not a law.

Uses: feature prioritization, finding weak spots, setting KPI/OKR, calibrating models (sanity check, calibration, explaining deviations). Required cuts by metric type: funnels (new/returning, channel cold/warm or organic/paid, platform web/mobile iOS/Android, region and language, client type SMB/Mid-Market/Enterprise); retention (paying vs free, cohorts by launch period, window D1/D7/D30 for consumer apps vs M1/M3/M12 for B2B SaaS, activity criterion); churn (logo churn % of clients vs revenue churn % of revenue, gross vs net, new vs old clients separately); monetization UE/LTV/CAC/ARPU (new vs existing payers, currency and taxes gross/net, fixed costs outside UE, regional purchasing power — CTR/CPC differ 5+× between countries, core vs casual).

Biases that distort published numbers: survivorship bias (the worst are silent — the visible average is too high); vendor bias (a platform exaggerates the problem to sell its solution); startups publish flattering metrics (LTV/CAC = 5 measured on the best segment); suspiciously round numbers (10%, 50% — probably an estimate); missing context ("25% of what: D30? D90? payers?"); stale data.

Freshness: fast-moving metrics (CAC, CPI, retention) no older than 24 months; stable ones (gross margin, long-term LTV) up to 3–5 years acceptable. Comparability heuristic — five axes: metric definition; segment/client; period and season; business model and channel; stage and geography. 5/5 match → use as-is; 3–4 → adjust and explain the correction; ≤2 → use only as order of magnitude and a hypothesis to test. Triangulation: minimum 3 independent confirmations; spread over 30% — caution.

**How:** 1) define the metric precisely: formula, units, period, cohort, activity criterion (e.g. "share of the cohort active on day N by criterion Z"); 2) find sources: search with date/type filters; experts (investors, angels, niche peers, consultants); reports from Sequoia, Y Combinator, Greylock, Reforge, Mixpanel, Amplitude, First Round Review; public filings; own A/B history; 3) check each benchmark in 7 steps — origin (primary or retelling, author); methodology (sample, segments, collection period, metric definition); freshness; comparability; triangulation ≥3; biases; range + confidence level (P25/P50/P95 + High/Medium/Low, mapped to A–D source grades); 4) score comparability on the five axes; 5) compare your value with the range (below P25 / P25–P50 / above P50 / above P95 — suspect measurement error) and explain the deviation (channel, model, segment, product age); 6) use in decisions: OKR target, model assumption (with a discount for weak sources), sensitivity around the range; 7) collect top-3 best practices (UX, onboarding, legal, logistics, monetization, notifications) via competitor observation, search, expert interviews, conferences — each with expected effect, complexity, source; a "+X% retention" from someone else's case is a hypothesis, not a forecast.

**Pitfalls:** taking a single "average" from one article; comparing a B2C app with B2B SaaS, SMB with Enterprise, one country with another without adjustment; comparing day-1 retention with 30-day retention; accepting a vendor's number as independent (the retention vendor will say bad retention is a catastrophe); using a 3-year-old benchmark for fast-moving metrics; setting a P95 goal with no plan for reaching it; copying a best practice without checking segment and channel.

**RU-версия:** `knowledge/methods/benchmarking.md` (полная методика).
