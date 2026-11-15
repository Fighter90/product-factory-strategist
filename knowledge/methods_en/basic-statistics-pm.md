---
id: M-basic-statistics-pm
lang: en
title: Basic statistics for product decisions — means, dispersion, confidence intervals, type I/II errors, power
course: data
sources: ["EN mirror of the RU methodology card M-basic-statistics-pm (knowledge/methods/basic-statistics-pm.md); original sources are listed in the RU card"]
stages: [research, validation, after-decision]
tags: [statistics, mean, median, percentile, variance, confidence-interval, p-value, type-i-error, type-ii-error, power, correlation, distribution]
related: [M-ab-testing, M-product-metrics, M-quant-methods, M-source-criticism, M-traction-model]
---

# Basic statistics for product decisions

## When to use
You need to assess whether a week of "success" is random, how much to trust the mean, which range of effect to promise the business, and what "scale / don't scale" decisions risk. This is the foundation under [[M-ab-testing]] and the reading of any metrics.

## Core idea

### Why a product needs statistics
One lucky result (e.g., 23 sales in a week with a break-even point of 20) can be pure chance: with a true mean of 20 the probability of such a week is ≈ one third of all weeks, and with a mean of 19 such a "lucky" week happens in about 27% of cases. Statistics turns the intuition of "lucky/unlucky" into managed risk: it gives no guarantees — it gives probabilities and lets you agree in advance on which risk you are willing to live with.

### Descriptive statistics: mean, median, percentiles
- **Mean** — sum of values / number of observations; sensitive to outliers (one large order shifts the "average order"). Stable at large n thanks to the CLT: the mean of a large sample is distributed almost normally, even if the values themselves are not.
- **Median** — the value splitting the sample in half; robust to outliers and heavy tails; better describes the "typical" user (median session time, median order).
- **Percentile pN** — the value below which N% of observations lie. p90/p95/p99 of response time are the SLA standard: the mean can look fine with terrible tails. For medians and percentiles the ordinary t-test on "raw" values does not work — use the bootstrap distribution of the quantile.
- Rule: for money and time, always look at the median/percentiles next to the mean; a discrepancy signals asymmetry.

### Dispersion: variance and standard deviation
- **Variance σ²** — the mean squared deviation from the mean; **σ** is its square root, in the same units as the metric. For a proportion (conversion) σ² = p·(1−p), where p is the baseline conversion.
- Dispersion defines the "corridor of normal values" of a metric and the required sample: the larger σ, the wider the CI and the longer any test. Variance can be reduced by linearizing ratio metrics, stratification, CUPED ([[M-ab-testing]]).

### Distributions
- **Normal ("bell")** around the true mean: most values near the center, rare deviations at the edges. Hence the danger of "one success": a value from the right tail is a normal event, not a pattern.
- Product metrics are often **asymmetric with a heavy right tail** (order values, session time, response time): mean > median, individual outliers dominate. Then: log transformation, comparison by medians/percentiles, nonparametric tests.
- Binary outcomes (bought / did not buy) at large n give a normal distribution of the proportion — this lets you compute the CI and sample size with the p(1−p) formulas.

### Hypotheses and p-value
- **H₀** ("no effect," the status quo) and **H₁** ("there is an effect") are formulated before the analysis. By default we treat H₀ as true until the data gives grounds to reject it.
- **p-value** — the probability of obtaining the observed or a more extreme difference if in fact there is no effect (H₀ is true). A small p-value ≠ a large effect: it speaks to the strength of evidence against H₀, not to the size or the probability of success.
- Decision rule: p < α → reject H₀ (the effect is significant); p ≥ α → no grounds to reject (this is not "the effect is absent," but "we have not proven it").

### Confidence interval (CI)
A range that with a given probability (usually 95%) "covers" the true value. For a mean:
```
CI = x̄ ± z · σ / √n
where x̄ — sample mean; z — normal distribution quantile
(1.96 for 95%, ≈2.58 for 99%); σ — standard deviation; n — sample size.
```
Reference points for two-sided z-quantiles: 90% → z ≈ 1.64; 95% → 1.96; 99% → 2.58. For proportions, substitute √(p·(1−p)/n) for σ/√n.
Mini-example: sample {15, 17, 19}, σ=5, n=3 → x̄=17, CI = 17 ± 1.96·5/√3 ≈ 17 ± 5.66 = [11.3; 22.7].
- The CI width grows with: greater dispersion σ, a stricter z level; it shrinks with: a larger sample n. The mean only shifts the interval and does not affect the width.
- For an A/B effect (the group difference) the interval is built around the difference; comparing effects across segments is conveniently drawn as a forest plot: point = effect estimate, line = 95% CI, a vertical zero line.
- Practice: **if the lower bound of the CI is below the break-even point (or the CI covers 0) — there is no sustainable success**, even if the mean looks good. Decide by the CI, not by the point.
- Connection with p-value: a 95% CI not including 0 ⇔ p < 0.05. p-value answers "how strong is the evidence against H₀," the CI — "in which range can the real effect lie." Show the business both.

### Two templates for interpreting a result (for communication)
- "Growth +6%, p-value = 0.10, 95% CI [−1%; +13%]" → the CI covers zero: the real effect may be negative; no grounds for scaling, a repeat test with more power is possible.
- "Payers +10%, p-value = 0.04, 95% CI [+3%; +17%]" → significant; even the worst CI bound (+3%) is above the business threshold → we scale, separately checking the segments where the effect was not confirmed (a bug or a small segment sample is possible).

### Type I and II errors, α, β, power
- **Type I error (α, false positive):** we "saw" an effect that does not exist → we scaled randomness. Costs: spent resources, reputation, rollback.
- **Type II error (β, false negative):** we missed a real effect → forgone growth, a good feature "buried."
- **α** — the tolerated share of false alarms, fixed before the test: 5% is the standard; 1% when the price of a false release is high (payments, security); up to 10% for MVPs and "improvers," where not missing matters more.
- **β** — the probability of a miss; usually ≤ 0.2. **Power = 1 − β** — the probability of catching the effect if it exists; the standard is ≥ 0.8.
- The balance depends on context: where a miss is costlier than a false alarm (safety, critical features) — stricter β and higher power; where rollback/risk is expensive (payment features) — stricter α. Choosing α/β is a business decision, spelled out before the test.
- Raising power: a larger sample, a longer test, lower variance (aggregation, linearization, CUPED), a more sensitive proxy metric.

### Practical guidelines on data volume
- The accuracy of a mean estimate grows as √n: to halve the CI you need four times the data; at n ≈ 100 observations only large effects (tens of percent) are visible, small shifts "drown" in noise.
- A sample does not cure bias: if the data was collected unrepresentatively (only loyal or only dissatisfied people respond), more n will not fix the conclusion.
- Minimum series of observations: any conclusion from one week/one launch is preceded by the question "how often does this happen by chance."
- Asymmetry is a reason to switch the headline statistic: if the mean is noticeably above the median, the median becomes the headline number for the "typical user," and the mean is kept for total effects (revenue).

### Correlation ≠ causation
- Metrics moving together (or a link in a metric-tree node) can be: coincidence, a common cause (season, traffic), reverse causality (not "those who created projects are retained better," but "those who are retained create projects"), sample bias.
- Causality is proven by an experiment ([[M-ab-testing]]) or a quasi-experiment (Diff-in-Diff, matching, synthetic control). Regression with controls shows "adjusted correlation" but does not prove causality.
- Rule for the metric tree: an "influences" arrow is either a proven A/B test or a hypothesis with a verification plan; link coefficients are measured, not assumed.

### Communicating with the business
- Speak in ranges: "with 95% confidence the effect lies in [X; Y]," not "it grew by exactly 7%."
- Always name: the significance level, the CI width, the power, the limitations ("significant only on Android," "not enough power — a retest is needed").
- Anti-patterns: "polishing" a test until a pretty result; selling a significant but tiny effect; promising guarantees instead of probabilities; ignoring gray results.

## Procedure
1. State H₀/H₁ and the decision criterion (which result counts as success) before the analysis.
2. Choose descriptive statistics to match the metric's nature (mean + median/percentiles for asymmetric ones).
3. Estimate the dispersion and the "corridor of normal values" on 3–6 months of history: a current deviation inside the corridor is not a reason for an investigation.
4. Compute the CI (and the p-value if there is a comparison); check whether the CI crosses 0 or the business threshold.
5. For tests: fix α/β/MDE, compute the sample ([[M-ab-testing]]); verify the power is sufficient.
6. Formulate the conclusion in terms of risk: which error type is possible, what we lose in each decision scenario.
7. Check alternative explanations (season, base structure, external events) before a causal reading of a correlation.

## Template / checklist
```
Metric: ___  Period: ___  n = ___   x̄ = ___   median = ___   p90 = ___   σ = ___
Corridor of normal (history 3–6 mo): [___; ___]   Current value inside? yes/no
H0: ___   H1: ___   α = ___   β = ___   Power = ___
CI 95%: [___; ___]   p-value = ___   Business threshold: ___   Verdict: significant / not significant / not enough power
Alternative explanations: season ___ base structure ___ events ___
```
Checklist: mean and median do not contradict · period and window stated · the CI is given, not a point · α/β declared in advance · correlation not called a cause without an experiment · statistical significance separated from business significance.

## Common mistakes
- Deciding on one point/week without dispersion and the corridor of norms.
- Mean without median on an asymmetric metric; p90 ignored in an SLA question.
- "Small p → large effect"; "large p → the effect definitely does not exist" (instead of "not proven").
- The CI covers the break-even threshold, but the decision was made by the mean.
- α chosen post-hoc "so that something flags"; extending a test for significance.
- A correlation in the report turns into "therefore we will do X" without a causality check.
- Comparing proportions with different denominators/windows; confusing p.p. with %.
- "Polishing" the sample after the result (choosing a luckier window/segment post-hoc) — the same p-hacking as extending a test.

## Questions that can change the decision
- What is the probability of seeing such a result if H₀ is true, and what power does the comparison have?
- Is the current deviation inside the corridor of normal values, and is there no seasonal coincidence?
- What is the cost of a type I error vs a type II error for this specific decision?
- Is the lower bound of the CI above the break-even point/quality threshold?
- What else explains the link besides the assumed cause, and how can it be checked cheaper than an experiment?

## Related maps
[[M-ab-testing]], [[M-product-metrics]], [[M-quant-methods]], [[M-source-criticism]], [[M-traction-model]]
