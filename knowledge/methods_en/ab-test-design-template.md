---
id: M-ab-test-design-template
lang: en
title: A/B test design template — a one-pager from business context to conclusions and call to action
course: pm-approaches-en
stages: [strategy, validation]
tags: [ab-testing, experiment, template, experiment-design, target-metric, guardrail-metric, mde, split]
related: [M-ab-testing, M-ab-test-checklist, M-ai-experiment-review-context, M-product-metrics, M-success-metrics, M-quant-methods, M-mvp-pilots, M-basic-statistics-pm, M-pmf-scaling]
---

# A/B Test Design Template

## When to apply
Before launching any A/B test, when you need to turn a vague "let's try this" idea into a reviewable document with metrics, decision thresholds, and a sample-size calculation. The template is a contract the team signs with itself: all decisions about thresholds, duration, and actions are fixed **before** launch, so that after the data is collected nobody adjusts the criteria to fit the result. The methodology base (statistics, criteria, traps) lives in the `M-ab-testing` card; this template is the working skeleton of a specific experiment, filled in section by section top-down and living as a single document.

## How to use the template
Fill in the sections in order: Business → Metrics → Decision mechanism → Implementation → Hypothesis testing. The "Results" section is filled only after the data is collected — in advance you write only its structure. Maturity rule: if some section cannot be filled without "we'll clarify later", the experiment is not ready to launch. Square brackets are substitution slots; the text inside brackets is a hint on what and in what form to write. The finished document is reviewed by an analyst + a product manager: the analyst checks the statistics (MDE, sample size, criteria), the product manager checks the business logic and the cost of a mistake.

## Business
**Product:** [briefly: the product, who it is for, which scenario we are changing — 2–3 sentences, enough for a stranger].

**Problem:** [what is unsatisfactory now? show with data or observations why this is a problem: a funnel number, complaints, user behavior].

**Experiment goal:** [which question will the experiment answer? tie it to the product goal or the team's quarterly goal].

**Hypothesis:** [for each target metric: "If we make <change> for <segment>, then <metric> will grow/drop by <X>, because <reason>"].

**Estimated impact:** [estimate the effect in metric terms, orders, or money. State the assumptions and attach a calculation or research — even a rough range beats "it will get better"].

## Metrics

### Target
**Name:** [what do we count? for shares and ratios state the numerator and the denominator].
**Metric type:** [conversion, continuous, or ratio].
**Calculation period:** [until the end of the test, or N days from entering the sample].
**Stat. test:** [e.g., z-test, t-test, or bucketed t-test].
**Why does this metric matter?** [which change in this metric affects the decision?].

### Proxy
**Name:** [what do we count? for shares and ratios state the numerator and the denominator].
**Metric type:** [conversion, continuous, or ratio].
**Calculation period:** [until the end of the test, or N days from entering the sample].
**Stat. test:** [e.g., z-test, t-test, or bucketed t-test].
**Why does this metric matter?** [how will it help notice the effect earlier or explain it?].

### Guardrail
**Name:** [what do we count? for shares and ratios state the numerator and the denominator].
**Metric type:** [conversion, continuous, or ratio].
**Calculation period:** [until the end of the test, or N days from entering the sample].
**Stat. test:** [e.g., z-test, t-test, or bucketed t-test].
**Why does this metric matter?** [what could get worse because of the test, and which drop is unacceptable?].

## Decision mechanism
**Which decisions will be made?** [set thresholds for target and guardrail metrics. What do we do on success, on degradation, or on an ambiguous result? For example: "roll out to 100% on a conversion lift ≥ X pp with guardrail degradation ≤ Y"; "on an ambiguous result — record the conclusion and do not roll out"; "if the guardrail drops below Y — roll back immediately, without waiting for the end"].

## Implementation
**Splitting system:** [name the system and attach a link to the configuration. For a custom split, attach the verification results].

**Splitting identifier:** [which ID do you split by? if the split is not by user, explain why and how you will compute the metrics].

**Splitting mechanics:** [state the audience, platforms, versions, and exclusions. Describe when you assign the group and from which event a person enters the test].

**Differences between variants:** [describe what happens in control and in each test group. Attach screenshots or mockups].

**Script:** [before launch, save the SQL or code that can restore the participants, groups, and the moment of entering the test].

## Hypothesis testing
**Null and alternative hypotheses:** [write H₀ and H₁ for each target metric. If there are several test groups, state which groups you compare].

**Significance level:** [state α (usually 5%). If the decision depends on several checks, describe the correction — e.g., Bonferroni].

**Power:** [state the power for the chosen MDE. Usually 80%].

**MDE:** [state the baseline value of the metric and the MDE. Label the units (pp, %, absolute) and explain why an effect of this size matters — it must be tied to the cost of the decision, not to a wish].

**Sample size:** [state the number of participants and the share of traffic for each group. Attach the calculation for the same audience and split — the formula and the check are in `M-ab-testing` and `M-quant-methods`].

**Test duration:** [state how long the collection will take given the participant flow, and how long you must wait for the target action. Keep the test a whole number of weeks to cover the weekly behavior cycle].

## Experiment results
### Row 1
**Name:** [metric, actual group sizes, values, and the effect. Attach the calculation].
**p-val:** [state the p-value with the correction if one was needed].
**CI:** [state the level and both bounds of the interval for the effect].

### Row 2
**Name:** [metric, actual group sizes, values, and the effect. Attach the calculation].
**p-val:** [state the p-value with the correction if one was needed].
**CI:** [state the level and both bounds of the interval for the effect].

## Conclusions
**Conclusion:** [what did the test show and which decision was made? Check it against the rules from the "Decision mechanism" section — the decision must match the pre-registered rule, not be fitted to the result].

**Call to action:** [who will do what after the test? State the deadlines and the next checks — what we measure after the rollout to confirm the effect on the whole base].

## Connection to the pfs process
The template is the core artifact of the `validation` step (pfs step 9): the "Business" section grows out of the hypotheses of the `options` step, the metrics — out of `M-success-metrics`, the sample-size calculation — out of `M-quant-methods`, and the "Conclusions" section is recorded in `pfs validation` and in the decision journal (`pfs decision add`). For non-classic cases (network effects, offline, "already shipped") — alternatives in `M-ab-testing`, the section "when the classic approach is impossible".
