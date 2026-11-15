---
id: M-ab-testing
lang: en
title: A/B testing — the full cycle from hypothesis to decision, and alternatives when the classic approach is impossible
course: data
sources: ["EN mirror of the RU methodology card M-ab-testing (knowledge/methods/ab-testing.md); original sources are listed in the RU card"]
stages: [options, strategy, validation]
tags: [ab-test, experiment, mde, sample-size, p-value, confidence-interval, bonferroni, sequential, srm, aa-test, switchback, diff-in-diff, synthetic-control, uplift, bayesian]
related: [M-basic-statistics-pm, M-product-metrics, M-goals-drivers-bets, M-quant-methods, M-mvp-pilots, M-solution-design, M-traction-model]
---

# A/B testing: the full cycle and alternatives

## When to use
You need to prove a causal link "change X → shift in metric Y" before rolling out to all users, estimate how much traffic and how many weeks this will take, and interpret the result honestly. Alternatives apply when random user assignment is impossible (network effects, offline, "already rolled out to everyone").

## Core idea

### Definition and place among methods
An A/B test (split test) is random assignment of users into groups, showing each group its own version, and comparing the metrics. It is the gold standard because external factors (season, competitors, marketing) hit both groups equally. Hierarchy of evidence: survey (opinion, self-selection error) → look-alike matching (residual bias) → before/after comparison (trends and external events) → A/B (causality). The classic approach fails when: network effect (one side's behavior changes another side's conditions), randomization is impossible (offline campaigns, law), "already rolled out to everyone."
- **H₀** — no effect; **H₁** — there is an effect. The decision is made only by rules fixed in advance.
- The expected share of "green" tests in a mature team is small (~20%), and even fewer get rolled out — this is the norm, not failure.
- **When an A/B test is not needed at all:** (1) the question is "why," not "how much" — interviews and UX research; (2) there are no alternatives (a legal requirement, a critical bug — just ship it); (3) the expected effect is huge and obvious — rare, and it should be checked with suspicion of randomness; (4) physical/ethical impossibility of splitting (you cannot "raise salaries for half the staff"). In these cases — the alternatives from the last section.

### Metrics and criteria
- Metric config: 1–2 **target** metrics (the reason the test exists), 1–3 **proxy** metrics (more sensitive, earlier signal), ≥2 **guardrails** (risk counter-metrics: conversion, NPS/complaints, churn, fraud, latency). More metrics = power loss.
- Hypothesis by template: "Variant B (change X) will significantly change metric M in segment S by ≥ Z% relative to A, at α, β, and provided the guardrails are not worse than the threshold." Plus a written H₀.
- Choosing the criterion to match the nature of the metric: means (order value, revenue/user) → classic t-test (relies on the CLT); proportions and ratios (conversion, CTR, ARPU = sum/counter) → linearized t-test (the per-user "contribution" reduces variance); percentiles and heavy tails (p95 response time) → quantile t-test on the bootstrap; several groups → ANOVA + post-hoc (Tukey) with a correction.

### Sample size, MDE, and duration calculation
Parameters: α (type I error — "seeing an effect that does not exist," usually 0.01–0.05), β (type II error — "sleeping through an effect," usually 0.1–0.2; power = 1−β ≥ 0.8), MDE — the minimum effect the test must be able to catch. For proportions: baseline p, variance σ² = p·(1−p). Two-sided test:
- z_α = normal distribution quantile at level 1−α/2 (for α=5% ≈ 1.96); z_β — at level 1−β (for β=20% ≈ 0.84).
- **Sample size per group:** n = (z_α + z_β)² · 2·σ² / MDE² (MDE in absolute proportion terms; round up in line with the meaning of the task — rounding down favors missing the effect). At α=5%, β=20% the rule of thumb n ≈ 16·σ²/MDE² works.
- **Duration:** n_days = n / (daily traffic × share of traffic per group). Mini-example: p=1.8% (4.1/230 contacts per view), σ²≈0.0177, MDE=1 p.p. → n ≈ (1.96+0.84)²·2·0.0177/0.0001 ≈ 2,770 per group; at 115,000 views/day per group ≈ 0.02 days by traffic — yet the test is still kept running 7–14 days to cover a full weekly cycle.
- **Reverse calculation** (fixed traffic/duration): MDE = (z_α + z_β)·√(2σ²/n). If the computed MDE is larger than the economically meaningful effect — do not run the test (it will not catch it) or change the design.
- Levers for lowering MDE/duration: more traffic or a longer test; lower variance (linearization of ratio metrics, stratification, CUPED/ML-CUPED, a sensitive proxy); a conscious compromise on α/β (decided before the start). MDE "off the top of the head" and post-hoc fitting are forbidden.

### Design: splitting, layers, exposure
- **Randomization and sticky assignment:** a user is pinned to a group by a permanent key (user_id / seller_id / region_id) — "first contact → forever"; falling into test, then into control, distorts the metrics (habituation effect).
- **Layers (bucketing):** independent experiments live in different layers with different hashing keys; within a layer — 100 buckets. This separates hundreds of parallel tests without "stealing" traffic.
- The **exposure flag** is set as close as possible to the moment of the UX change and before the measurable action: later — part of those who saw the change stay "outside the test"; earlier — outsiders leak into the groups.
- **A/A test** before A/B (≥24 h, better a full weekly cycle): both groups unchanged; an alarm if p<0.1 on any metric or an imbalance in group sizes. Catches broken randomization, caches, late-exposure. Additionally: a "dark patch" (code rolled out to 100%, feature switched off behind a flag) — latency warm-up and instant rollback.

### Multiple comparisons
With m checks the probability of at least one false "significance flag" (FWER) grows; with 10+ metrics a raw p<0.05 means almost nothing.
- **Bonferroni:** α′ = α/m. Simple and conservative; fine for 1 target + 2–3 guardrails.
- **Holm (step-down):** sort p ascending; p₁ ≤ α/m, the next ≤ α/(m−1), and so on; stop at the first violation. Controls the FWER, more powerful than Bonferroni; for 4–8 checks with an expensive error.
- **Benjamini–Hochberg (FDR):** find the largest k where p₍ₖ₎ ≤ (k/m)·Q; all p ≤ p₍ₖ₎ are significant. Controls the expected share of false flags among the flagged ones (e.g., Q=5%); for 10–30 secondary checks where a miss is cheaper than missed growth.
- The correction is fixed **before** the start; choosing it "based on the final p" is p-hacking.
- **Peeking:** every interim check inflates α (10 daily looks raise the real α from 5% to ~19%). Options: a ban — the decision comes exactly at the end; sequential testing with α-spending (e.g., Pocock boundaries); the Bayesian approach — the stopping rule is fixed at the start ("stop if P(Δ>0) ≥ 0.95 or P(Δ<0) ≥ 0.95").

### Running and monitoring
- **SRM / traffic health:** actual vs planned group sizes (e.g., 50%±0.5 p.p.); expected vs actual exposures (±3%); covariate test by device/age (p>0.3); the traffic share per group matches the plan. Any violation — stop and debug: an abnormally large effect is almost always a technical error, not a success.
- **Guardrail metrics** with thresholds fixed before the start; a critical degradation = early stop (the only legal reason to look into the process before the end, besides a sequential scheme).
- Do not launch in the evening/at night without an on-call team; keep a single experiment registry and coordinate overlaps.

### Interpretation
- Compute only after the end: effect, p-value, 95% CI. For a mean: CI = x̄ ± z·σ/√n; the width grows with σ and z and falls with n.
- **CI does not include 0 ⇔ p < α** (two-sided). p-value is the probability of such or a more extreme result if H₀ is true, NOT the effect size. Statistical significance ≠ business significance: +0.2% can be significant and useless.
- Build the report of effects by segments (forest plot: effect point + 95% CI per segment, a vertical zero line) — but declare the compared segments in advance.
- Scenarios and actions: **green** (target ↑ significant, guardrails fine) → check the cuts and dynamics, then roll out; **green with nuances** (a guardrail dipped slightly, the total increment > 0) → ship with monitoring/refinement; **red** (a guardrail dropped more than the gain, or target ↓) → do not ship, find the cause; **gray** (nothing is significant) → not "extend it for luck," but check for bugs and power (CUPED, proxy), rebuild the hypothesis. Each case gets an entry in the knowledge base; the decision: Scale / Iterate / Drop.
- Frequentist vs Bayesian: the frequentist answers "is there a significant difference," the Bayesian — "with what probability is B better than A, and what effect can be expected" (posterior from Beta/Binomial for proportions: posterior = Beta(α₀+successes, β₀+failures), P(Δ>0) via Monte Carlo). The Bayesian approach is convenient for low traffic and for communication; the decision rule (the P threshold, expected loss) is fixed in advance.

### Typical interpretation errors
- **Peeking** — stopping at the first flag → α inflation (see above).
- **Survivorship error** — drawing conclusions from randomly flagged metrics outside the hypothesis (with m metrics, ~α·m flag by chance).
- **Simpson's paradox** — growth in every segment with a falling total due to a change in traffic structure. Example: channels with CTR 10% and 90% split 50/50 give 50%; after redistribution to 90%/10% at CTR 11%/91% the total = 0.11·0.9 + 0.91·0.1 ≈ 19% — "growth everywhere," a fall in the total. Check the structure and the total.
- **Novelty/habituation effect** — the first-days effect disappears; check the weekly dynamics and keep a subsample of "old" users.
- **Access bias** — the test contains only "those who updated the app," the control everyone else: compare comparable subgroups.
- **Experiment overlap** — someone else's test inside your control group; cured by layers and a registry.
- Ignoring seasonality — an "effect" from a seasonal peak; run the test for at least 1–2 full weeks.

## Procedure ("golden" design steps)
1. State the problem and the hypothesis by template (X → M → Z%, segment, α/β) + H₀.
2. Choose metrics: 1–2 targets, 1–3 proxies, ≥2 guardrails with thresholds; choose the criterion matching the metric's nature.
3. Justify the MDE with economics (which minimum effect pays for the change); compute n and the duration; verify that it "fits" the traffic. Justify why the classic A/B design specifically.
4. Define the split: key, layer, stickiness, traffic share; plan the dark patch and the A/A.
5. Launch: A/A → A/B; watch only health metrics and guardrails; do not peek at the targets.
6. Analyze according to the plan: effect + p-value + 95% CI (with the correction), cuts and dynamics, checks for Simpson's paradox and novelty.
7. Make the decision Scale / Iterate / Drop; write the result into the knowledge base with a conclusion.

## Template / checklist (experiment plan)
```
Hypothesis: if [X], then [M] changes by [Z%] in [S]; H0: no effect
Target: ___ (criterion: t-test | linearized | quantile | ANOVA | bayesian)
Proxy: ___   Guardrail: ___ with thresholds ___
α=___  β=___  MDE=___  baseline p/σ²=___  n per group=___  duration=___ days
Split: key ___ layer ___ traffic share ___ sticky=yes   A/A: plan ___
Correction (Bonferroni/Holm/BH): ___   Stopping rule: until the end | sequential | bayesian threshold ___
Risks and Plan B: rollback button, guardrail stop-conditions ___
```
Pre-launch checklist: A/A passed (p>0.1) · group sizes as planned · exposure before the action · correction and decision rule documented · MDE justified by economics · a decision date and owner exist.

## Common mistakes
- MDE "taken off the top of the head" or fitted after the start; α/β changed "on the fly."
- 10+ metrics without a correction; conclusions drawn from metrics outside the hypothesis.
- Extending a gray test "for one more week"; stopping at the first flag.
- No A/A or health dashboard — the "victory" turns out to be a cache bug or late-exposure.
- Comparing non-equivalent subgroups (updaters vs everyone); ignoring traffic structure (Simpson).
- Launching without a rollback plan; conflict with another team's parallel test.

## Questions that can change the decision
- Which minimum effect is economically justified, and which MDE is realistically achievable with our traffic?
- Is there a network effect or an overlap with other teams' experiments that breaks randomization?
- Is the power sufficient to catch the effect at all; is a different criterion or proxy needed?
- What is the stopping rule, and what do we do with a gray result?
- Is the effect stable across weeks and segments, or is it novelty/season/one segment?

## Alternatives when the classic A/B is impossible
- **Regional test** — the randomization unit is a city/store: matching of "twin pairs" by historical metrics (GMV, orders), then random distribution of the pairs. Preserves network balance inside a region; downside — few units (with <30 regions — Welch/bootstrap, higher MDE).
- **Switch-back (switching over time / geo-blocks)** — the same region alternates between test and control (block = hour/day/shift ≥ a full user cycle; ABBA/BAAB order against the trend; cluster t-test, cluster = region×period). For strong network effects (pricing, matching); not for long and noticeable changes — the effect "flows" between blocks.
- **Before/after with a control — Diff-in-Diff:** effect = Δ(test: after−before) − Δ(control: after−before). The key assumption — parallel trends before the intervention; verified on pre-history.
- **Synthetic control** — a "synthetic" control built as a weighted combination of similar objects that match the test before the intervention; for a single unique region/channel; requires a long history.
- **PSM (propensity score matching)** — retrospectively match "similar" users to those who adopted the feature and compare; risk of residual bias and sensitivity to the feature set.
- **Interleaving** — both versions (e.g., ranking algorithms) are shown in one mixed feed to the same user; comparison by clicks/actions on position pairs. Far more sensitive than the classic approach at low traffic; suitable for the relative order of algorithms, but not for the absolute effect on business metrics.
- **Multi-armed bandit** (epsilon-greedy, Thompson sampling) — traffic flows to the leader, less "cost of foregone success"; the strict p-value interpretation is lost.
- **Fake door** — measuring demand with a "coming soon" button before development.
Choice rule: can split in advance by user → classic; only by geo → regional; network effect → switch-back/geo-split; rolled out to everyone with history → DiD/synthetic control/PSM; comparing the algorithms of one feed → interleaving; little data → Bayesian or honestly admit "there is no answer." The method's assumptions and limitations are documented in the report.

## Related maps
[[M-basic-statistics-pm]], [[M-product-metrics]], [[M-goals-drivers-bets]], [[M-quant-methods]], [[M-mvp-pilots]], [[M-traction-model]]
