---
id: M-basic-statistics-pm
lang: en
title: Basic statistics for product decisions — means, spread, confidence intervals, type I/II errors, power
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [research, validation, after-decision]
tags: [statistics, mean, median, percentile, variance, confidence-interval, p-value, type-i-error, type-ii-error, statistical-power]
related: [M-ab-testing, M-product-metrics, M-quant-methods, M-source-criticism, M-traction-model]
---

# Basic statistics for product decisions

## When to apply
You need to judge whether a "successful" week is a fluke, how much an average can be trusted, what range of effect to promise the business, and what "scale / don't scale" decisions risk. This is the foundation under [[M-ab-testing]] and under the reading of any metric.

## Core idea

### Why a product needs statistics
One lucky result (say, 23 sales in a week against a breakeven point of 20) can be pure chance: with a true mean of 20, the probability of such a week is ≈ one third of all weeks, and with a mean of 19 such a "lucky" week happens in about 27% of cases. Statistics turns the "lucky/unlucky" intuition into managed risk: it gives no guarantees — it gives probabilities and lets you agree in advance on how much risk you are prepared to live with.

### Descriptive statistics: mean, median, percentiles
- **Mean** — the sum of values / the number of observations; sensitive to outliers (a single large order shifts the "average check"). Stable at large n thanks to the CLT: the mean of a large sample is distributed almost normally, even when the values themselves are not.
- **Median** — the value that splits the sample in half; robust to outliers and heavy tails; it describes the "typical" user better (median session time, median check).
- **Percentile pN** — the value below which N% of the observations lie. p90/p95/p99 of response time are the SLA standard: the mean can look fine while the tails are terrible. For medians and percentiles a plain t-test on "raw" values does not work — the bootstrap distribution of the quantile is used instead.
- Rule: for money and time, always look at the median/percentiles next to the mean; a divergence is a sign of asymmetry.

### Spread: variance and standard deviation
- **Variance σ²** — the mean squared deviation from the mean; **σ** is its square root, in the same units as the metric. For a share (conversion) σ² = p·(1−p), where p is the baseline conversion.
- Spread defines the metric's "corridor of normal values" and the required sample size: the larger σ, the wider the CI and the longer any test. Variance can be reduced by linearizing ratio metrics, stratification, and CUPED ([[M-ab-testing]]).

### Distributions
- **Normal ("bell")** around the true mean: most values sit near the center, with rare deviations at the edges. This is where the danger of "one success" comes from: a value from the right tail is a normal event, not a pattern.
- Product metrics are often **asymmetric with a heavy right tail** (checks, session time, response time): the mean > the median, and individual outliers dominate. Then: log transformation, comparison by medians/percentiles, nonparametric tests.
- Binary outcomes (bought / did not buy) at large n give a normally distributed share — this makes it possible to compute CIs and sample sizes with the p(1−p) formulas.

### Hypotheses and p-value
- **H₀** ("there is no effect", the status quo) and **H₁** ("there is an effect") are formulated before the analysis. By default we treat H₀ as true until the data gives grounds to reject it.
- **p-value** — the probability of observing a difference this extreme or more extreme if in fact there is no effect (H₀ holds). A small p-value ≠ a large effect: it speaks about the strength of the evidence against H₀, not about the size of the effect or the probability of success.
- Decision rule: p < α → we reject H₀ (the effect is significant); p ≥ α → there are no grounds to reject it (this is not "the effect is absent", it is "we have not proven it").

### Confidence interval (CI)
The range that with a given probability (usually 95%) "covers" the true value. For the mean:
```
CI = x̄ ± z · σ / √n
where x̄ is the sample mean; z is the quantile of the normal distribution
(1.96 for 95%, ≈2.58 for 99%); σ is the standard deviation; n is the sample size.
```
Reference z-quantiles for two-sided intervals: 90% → z ≈ 1.64; 95% → 1.96; 99% → 2.58. For shares, replace σ/√n with √(p·(1−p)/n).
A mini-example: sample {15, 17, 19}, σ=5, n=3 → x̄=17, CI = 17 ± 1.96·5/√3 ≈ 17 ± 5.66 = [11.3; 22.7].
- The CI widens with: a larger spread σ, a stricter z level; it narrows with: a larger sample n. The mean only shifts the interval and does not affect its width.
- For an A/B effect (the difference between groups) the interval is built around the difference; comparing effects across segments is conveniently drawn as a forest plot: a point = the effect estimate, a line = the 95% CI, a vertical line at 0.
- Practice: **if the lower bound of the CI is below the payback point (or the CI covers 0) — there is no durable success**, even if the mean looks good. Decide by the CI, not by the point.
- Connection with p-value: a 95% CI that does not include 0 ⇔ p < 0.05. The p-value answers "how strong is the evidence against H₀", the CI answers "within what range can the real effect lie". Show both to the business.

### Two patterns for interpreting a result (for communication)
- "Growth +6%, p-value = 0.10, 95% CI [−1%; +13%]" → the CI covers zero: the real effect may even be negative; there are no grounds for scaling, a retest with more power is possible.
- "Payers +10%, p-value = 0.04, 95% CI [+3%; +17%]" → significant; even the worst CI bound (+3%) is above the business threshold → we scale, having separately checked the segments where the effect did not hold (a bug or a small segment sample is possible).

### Type I and II errors, α, β, power
- **Type I error (α, false positive):** we "saw" an effect that does not exist → we scaled randomness. The costs: spent resources, reputation, a rollback.
- **Type II error (β, false negative):** we missed a real effect → growth not captured, a good feature "buried".
- **α** — the tolerated share of false alarms, fixed before the test: 5% is the standard; 1% — when the price of a false release is high (payments, security); up to 10% — for MVPs and "improvements", where not missing an effect matters more.
- **β** — the probability of a miss; usually ≤ 0.2. **Power = 1 − β** — the probability of catching the effect if it exists; the standard is ≥ 0.8.
- The balance depends on the context: where a miss is costlier than a false alarm (safety, critical features) — tighten β and raise power; where a rollback/risk is expensive (payment features) — tighten α. The choice of α/β is a business decision, agreed upon before the test.
- Raising power: a larger sample, a longer test, lower variance (aggregation, linearization, CUPED), a more sensitive proxy metric.

### Practical benchmarks for data volume
- The accuracy of a mean estimate grows as √n: to halve the CI you need four times the data; at n ≈ 100 observations only large effects (of the order of tens of percent) are visible, and small shifts "drown" in the noise.
- A larger sample does not cure bias: if the data was collected non-representatively (only loyal or only disgruntled people respond), growing n will not fix the conclusion.
- A minimum for a series of observations: any conclusion from one week / one launch is preceded by the question "how often does this happen by chance".
- Asymmetry is a reason to change the headline statistic: if the mean is noticeably above the median, the median becomes the headline number for the "typical user", and the mean is kept for total effects (revenue).

### Correlation ≠ causation
- Metrics moving together (or a link in a metrics-tree node) can be: a coincidence, a common cause (a season, traffic), reverse causality (not "those who created projects retain better" but "those who retain create projects"), or sample bias.
- Causality is proven by an experiment ([[M-ab-testing]]) or a quasi-experiment (Diff-in-Diff, matching, synthetic control). A regression with controls shows an "adjusted correlation" but does not prove causality.
- Rule for the metrics tree: an "influences" arrow is either a proven A/B or a hypothesis with a check plan; the coefficients of links are measured, not assumed.

### Communicating with the business
- Speak in ranges: "with 95% confidence the effect lies within [X; Y]", not "it grew by exactly 7%".
- Always state: the significance level, the CI width, the power, the limitations ("significant only on Android", "the power was insufficient — a retest is needed").
- Anti-patterns: "tuning" a test until it produces a pretty result; selling a significant but tiny effect; promising guarantees instead of probabilities; ignoring gray results.

## Procedure
1. Formulate H₀/H₁ and the decision rule (which result we count as success) before the analysis.
2. Choose descriptive statistics to match the nature of the metric (mean + median/percentiles for asymmetric ones).
3. Estimate the spread and the "corridor of normal values" on 3–6 months of history: a deviation inside the corridor is not a reason for an investigation.
4. Compute the CI (and the p-value if there is a comparison); check whether the CI crosses 0 or the business threshold.
5. For tests: fix α/β/MDE, compute the sample size ([[M-ab-testing]]); check that the power is sufficient.
6. Phrase the conclusion in terms of risk: which type of error is possible, and what we lose in each decision scenario.
7. Rule out alternative explanations (a season, the base structure, external events) before a causal reading of a correlation.

## Template / checklist
```
Metric: ___  Period: ___  n = ___   x̄ = ___   median = ___   p90 = ___   σ = ___
Normal corridor (3–6 months of history): [___; ___]   Is the current value inside? yes/no
H0: ___   H1: ___   α = ___   β = ___   Power = ___
95% CI: [___; ___]   p-value = ___   Business threshold: ___   Verdict: significant / not significant / underpowered
Alternative explanations: season ___ base structure ___ events ___
```
Checklist: the mean and the median do not contradict each other · the period and window are stated · a CI is given, not a point · α/β declared in advance · a correlation not called a cause without an experiment · statistical significance separated from business significance.

## Typical mistakes
- Deciding on a single point/week without the spread or a corridor of normal values.
- The mean without the median on an asymmetric metric; p90 ignored when an SLA question is at stake.
- "A small p → a big effect"; "a big p → definitely no effect" (instead of "not proven").
- The CI covers the payback threshold, but the decision was made on the mean.
- α chosen post hoc "so that it turns green"; extending a test for the sake of significance.
- A correlation in a report turns into "therefore we will do X" without checking causality.
- Comparing shares with different denominators/windows; percentage points confused with percent.
- "Tuning" the sample after the result (picking a luckier window/segment post hoc) — the same p-hacking as extending a test.

## Questions that can change the decision
- What is the probability of seeing such a result if H₀ is true, and what power does the comparison have?
- Is the current deviation inside the corridor of normal values, and is there a seasonal coincidence?
- What is the price of a type I error vs a type II error for this particular decision?
- Is the lower bound of the CI above the breakeven point / quality threshold?
- What explains the link besides the assumed cause, and how could it be checked more cheaply than an experiment?

## Related maps
[[M-ab-testing]], [[M-product-metrics]], [[M-quant-methods]], [[M-source-criticism]], [[M-traction-model]]
