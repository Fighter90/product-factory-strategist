---
id: M-ab-testing
lang: en
title: A/B testing — the full cycle from hypothesis to decision, and alternatives when a classic test is impossible
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [options, strategy, validation]
tags: [ab-testing, experiment-design, mde, sample-size, p-value, confidence-interval, sequential-testing, srm, switchback, diff-in-diff]
related: [M-basic-statistics-pm, M-product-metrics, M-goals-drivers-bets, M-quant-methods, M-mvp-pilots, M-solution-design, M-traction-model]
---

# A/B Testing: the Full Cycle and Alternatives

## When to apply
You need to prove a cause-and-effect link "change X → metric Y moves" before rolling out to everyone, estimate up front how much traffic and how many weeks this will take, and interpret the result honestly. The alternatives are for when randomly splitting users is impossible (network effects, offline, "already shipped to everyone").

## Core idea

### Definition and place among methods
An A/B test (split test) is a random division of users into groups, each group shown its own version, and a comparison of the metrics. It is the gold standard because external factors (season, competitors, marketing) hit both groups equally. Evidence hierarchy: survey (opinion, self-selection error) → matching similar users (matching, residual bias) → before/after comparison (trends and external events) → A/B (causality). The classic design fails when: there is a network effect (one side's behavior changes the other side's conditions), randomization is impossible (offline campaigns, the law), or the change is "already shipped to everyone."
- **H₀** — there is no effect; **H₁** — there is an effect. The decision is made only by rules fixed in advance.
- The expected share of "green" tests in a mature team is small (~20%), and even fewer get rolled out — that is the norm, not a failure.
- **When A/B is not needed at all:** (1) the question is "why," not "how much" — interviews and UX research; (2) there are no alternatives (a legal requirement, a critical bug — just ship); (3) the expected effect is huge and obvious — rare; check it with suspicion toward randomness; (4) physical/ethical impossibility of splitting (you cannot "raise the salary of half the people"). In these cases use the alternatives from the last section.

### Metrics and criteria
- Metric config: 1–2 **target** metrics (what the test exists for), 1–3 **proxy** metrics (more sensitive, earlier signal), ≥2 **guardrails** (risk counter-metrics: conversion, NPS/complaints, churn, fraud, latency). More metrics = loss of power.
- Hypothesis by template: "Variant B (change X) will significantly change metric M for segment S by ≥ Z% relative to A, at α and β, provided the guardrails are no worse than the threshold." Plus a written H₀.
- Choose the criterion to fit the nature of the metric: averages (average check, revenue per user) → the classic t-test (relies on the central limit theorem); shares and ratios (conversion, CTR, ARPU = sum over counter) → the linearized t-test (the per-user "contribution" reduces variance); percentiles and heavy tails (p95 response time) → a quantile t-test on the bootstrap; several groups → ANOVA + post-hoc (Tukey) with a correction.

### Calculating sample size, MDE and duration
Parameters: α (type I error — "seeing an effect that is not there," usually 0.01–0.05), β (type II error — "sleeping through an effect," usually 0.1–0.2; power = 1−β ≥ 0.8), and MDE — the minimum effect the test must be able to catch. For shares: baseline p, variance σ² = p·(1−p). Two-sided test:
- z_α = the quantile of the normal distribution at level 1−α/2 (for α=5% ≈ 1.96); z_β — at level 1−β (for β=20% ≈ 0.84).
- **Sample size per group:** n = (z_α + z_β)² · 2·σ² / MDE² (MDE in absolute fractions; round up as the task logic dictates — rounding down favors missing the effect). At α=5%, β=20% the rule of thumb n ≈ 16·σ²/MDE² works.
- **Duration:** n_days = n / (daily traffic × traffic share per group). Mini-example: p=1.8% (4.1/230 contacts per view), σ²≈0.0177, MDE=1 pp → n ≈ (1.96+0.84)²·2·0.0177/0.0001 ≈ 2,770 per group; at 115,000 views/day per group that is ≈ 0.02 days' worth of traffic — but the test is still held for 7–14 days, to cover a full weekly cycle.
- **Reverse calculation** (fixed traffic/duration): MDE = (z_α + z_β)·√(2σ²/n). If the computed MDE is larger than the economically meaningful effect — do not run the test (it will not catch it) or change the design.
- Levers for reducing MDE/duration: more traffic or a longer test; lower variance (linearization of ratio metrics, stratification, CUPED/ML-CUPED, a more sensitive proxy); a conscious trade-off on α/β (deliberately, before the start). An MDE "pulled out of thin air" and fitting numbers after the fact are forbidden.

### Design: splitting, layers, exposure
- **Randomization and sticky assignment:** a user is pinned to a group by a constant key (user_id / seller_id / region_id) — "first contact → forever"; landing in test and control alternately distorts the metrics (the habituation effect).
- **Layers (bucketing):** independent experiments live in different layers with different hash keys; within a layer there are 100 buckets. This keeps hundreds of parallel tests apart without "stealing" traffic from each other.
- The **exposure flag** is set as close as possible to the moment the UX changes and before the measured action: later — part of those who saw the change remain "outside the test"; earlier — outsiders leak into the groups.
- **A/A test** before the A/B (≥24 h, better a full weekly cycle): both groups unchanged; raise an alarm if p<0.1 on any metric or the group sizes are imbalanced. It catches broken randomization, caches, late exposure. Additionally: a "dark launch" (the code is rolled out to 100%, the feature is off behind a flag) — latency warmup and instant rollback.

### Multiple comparisons
With m checks, the probability of at least one false "win" (FWER) grows; at 10+ metrics a raw p<0.05 means little.
- **Bonferroni:** α′ = α/m. Simple and conservative; fine for 1 target + 2–3 guardrails.
- **Holm (step-down):** sort the p-values ascending; p₁ ≤ α/m, the next ≤ α/(m−1), and so on; stop at the first violation. Controls FWER, more powerful than Bonferroni; for 4–8 checks where an error is expensive.
- **Benjamini–Hochberg (FDR):** find the maximum k where p₍ₖ₎ ≤ (k/m)·Q; all p ≤ p₍ₖ₎ are significant. Controls the expected share of false wins among those "lit up" (e.g., Q=5%); for 10–30 secondary checks where a miss is cheaper than missed growth.
- The correction is fixed **before** the start; choosing it "based on the final p" is p-hacking.
- **Peeking:** every mid-flight check inflates α (10 daily looks raise the real α from 5% to ~19%). Options: prohibition — the decision happens exactly at the end; sequential testing with α-spending (e.g., Pocock bounds); the Bayesian approach — the stopping rule is fixed at the start ("stop if P(Δ>0) ≥ 0.95 or P(Δ<0) ≥ 0.95").

### Running the test and monitoring
- **SRM / traffic health:** actual vs planned group sizes (e.g., 50%±0.5 pp); expected vs actual exposures (±3%); a covariate balance test by device/age (p>0.3); the traffic share per group matches the plan. Any violation — stop and debug: an abnormally large effect is almost always a technical error, not a success.
- **Guardrail metrics** with thresholds set before the start; a critical worsening = early stop (the only legal reason to look at the process before the end, apart from a sequential scheme).
- Do not launch in the evening or overnight without an on-call team; keep a unified experiment registry and coordinate overlaps.

### Interpretation
- Compute only after the end: effect, p-value, 95% CI. For a mean: CI = x̄ ± z·σ/√n; the width grows with σ and z, falls with n.
- **The CI excludes 0 ⇔ p < α** (two-sided). The p-value is the probability of a result this extreme or more extreme given a true H₀, NOT the effect size. Significance ≠ business significance: +0.2% can be significant and useless.
- Build the effect report by segments (forest plot: an effect point + 95% CI per segment, a vertical zero line) — but declare the compared segments in advance.
- Scenarios and actions: **green** (target ↑ significant, guardrails within limits) → check the cuts and dynamics, then roll out; **green with nuances** (a guardrail dipped slightly, net increment > 0) → roll out with monitoring/rework; **red** (a guardrail dropped more than the gain, or target ↓) → do not roll out, look for the cause; **gray** (nothing significant) → do not "extend it for luck," but check for bugs and power (CUPED, proxy) and rebuild the hypothesis. Each case gets a knowledge-base entry; the decision: Scale / Iterate / Drop.
- Frequentist vs Bayesian: the frequentist answers "is there a significant difference," the Bayesian answers "with what probability is B better than A, and how large might the effect be" (posterior from Beta/Binomial for shares: posterior = Beta(α₀+successes, β₀+failures), P(Δ>0) via Monte Carlo). The Bayesian approach is convenient for low traffic and for communication; the decision rule (P threshold, expected loss) is fixed in advance.

### Typical interpretation mistakes
- **Peeking** — stopping at the first lit-up result → α inflation (see above).
- **The survivorship error** — drawing conclusions from metrics that lit up by chance and lie outside the hypothesis (with m metrics, ~α·m will light up by chance).
- **Simpson's paradox** — growth in every segment while the total falls due to a change in the traffic mix. Example: two channels with CTR 10% and 90% split 50/50 give 50%; after redistributing to 90%/10% at CTR 11%/91% the total = 0.11·0.9 + 0.91·0.1 ≈ 19% — "growth everywhere," a fall in the total. Check the structure and the total.
- **The novelty/habituation effect** — the first-days effect fades; check the weekly dynamics and keep a subsample of "old" users.
- **Access bias** — the test contains only "app updaters" while the control has everyone: compare comparable subgroups.
- **Experiment interference** — someone else's test inside your control group; cured by layers and a registry.
- Ignoring seasonality — an "effect" caused by a seasonal peak; run the test for at least 1–2 full weeks.

## Procedure (golden design steps)
1. Formulate the problem and the hypothesis by template (X → M → Z%, segment, α/β) + H₀.
2. Choose the metrics: 1–2 target, 1–3 proxy, ≥2 guardrails with thresholds; choose the criterion to fit the nature of the metric.
3. Justify the MDE with economics (which minimum effect pays for the change); compute n and the duration; check that it "fits" into the traffic. Justify why a classic A/B specifically.
4. Define the split: key, layer, sticky assignment, traffic share; plan the dark launch and the A/A.
5. Launch: A/A → A/B; watch only the health metrics and the guardrails; do not peek at the targets.
6. Analyze according to plan: effect + p-value + 95% CI (with correction), cuts and dynamics, Simpson and novelty checks.
7. Make the decision Scale / Iterate / Drop; record the result with its conclusions in the knowledge base.

## Template / checklist (experiment plan)
```
Hypothesis: if [X], then [M] changes by [Z%] for [S]; H0: no effect
Target: ___ (criterion: t-test | linearized | quantile | ANOVA | Bayesian)
Proxy: ___   Guardrail: ___ with thresholds ___
α=___  β=___  MDE=___  baseline p/σ²=___  n per group=___  duration=___ days
Split: key ___ layer ___ traffic share ___ sticky=yes   A/A: plan ___
Correction (Bonferroni/Holm/BH): ___   Stopping rule: until the end | sequential | Bayesian threshold ___
Risks and Plan B: rollback button, guardrail stop conditions ___
```
Pre-launch checklist: A/A passed (p>0.1) · group sizes match the plan · exposure before the action · correction and decision rule documented · MDE justified with economics · a decision date and owner exist.

## Typical mistakes
- MDE "pulled out of thin air" or fitted after the start; α/β changed "on the fly."
- 10+ metrics without a correction; conclusions drawn from metrics outside the hypothesis.
- Extending a gray test "one more week"; stopping at the first lit-up result.
- No A/A or health dashboard — the "victory" turns out to be a cache bug or late exposure.
- Comparing non-equivalent subgroups (updaters vs everyone); ignoring the traffic structure (Simpson).
- Launching without a rollback plan; conflict with a parallel test run by another team.

## Questions that can change the decision
- Which minimum effect is economically justified, and which MDE is actually achievable with our traffic?
- Is there a network effect, or an overlap with someone else's experiments, that breaks randomization?
- Is the power sufficient to catch the effect at all; is a different criterion or a proxy needed?
- What is the stopping rule, and what do we do with a gray result?
- Is the effect stable across weeks and segments, or is it novelty/seasonality/a single segment?

## Alternatives when a classic A/B is impossible
- **Regional test** — the unit of randomization is a city/store: match "twin pairs" by historical metrics (GMV, orders), then assign the pairs randomly. Preserves the network balance within a region; the downside is few units (below 30 regions — Welch/bootstrap, a higher MDE).
- **Switch-back (alternating in time / geo-blocks)** — the same region alternates between test and control (a block = hour/day/shift, ≥ a full user cycle; ABBA/BAAB order to guard against trend; cluster t-test, the cluster = region×period). For strong network effects (pricing, matching); not for long, noticeable changes — the effect "flows" between blocks.
- **Before/after with a control — Diff-in-Diff:** effect = Δ(test: after−before) − Δ(control: after−before). The key assumption is parallel trends before the intervention; verified on pre-history.
- **Synthetic control** — a "synthetic" control built as a weighted combination of similar objects that match the test object before the intervention; for a single unique region/channel; requires a long history.
- **PSM (propensity score matching)** — retrospectively match "similar" users to those who used the feature and compare; the risk is residual bias and sensitivity to the feature set.
- **Interleaving** — both versions (e.g., ranking algorithms) are shown in one mixed feed to the same user; the comparison is by clicks/actions on pairs of positions. Far more sensitive than the classic design at low traffic; suitable for the relative order of algorithms, but not for the absolute effect on business metrics.
- **Multi-arm/bandit** (epsilon-greedy, Thompson sampling) — traffic flows to the leader, less "cost of foregone success"; the strict p-value interpretation is lost.
- **Fake door** — demand is measured with a "coming soon" button before development.
Selection rule: you can split users in advance → classic; geo only → regional; network effect → switch-back/geo-split; shipped to everyone, history exists → DiD/synthetic control/PSM; comparing the algorithms of one feed → interleaving; little data → Bayesian or an honest admission that "there is no answer." The method's assumptions and limitations are documented in the report.

## Related maps
[[M-basic-statistics-pm]], [[M-product-metrics]], [[M-goals-drivers-bets]], [[M-quant-methods]], [[M-mvp-pilots]], [[M-traction-model]]
