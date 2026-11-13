---
id: M-ab-test-checklist
lang: en
title: A/B test checklist — 7 blocks of checks before launch and before the decision on results
course: pm-approaches-en
stages: [strategy, validation]
tags: [ab-testing, checklist, experiment, srm, multiple-comparisons, guardrail-metric]
related: [M-ab-test-design-template, M-ai-experiment-review-context, M-ab-testing, M-success-metrics, M-product-metrics, M-quant-methods]
---

# A/B Test Checklist

## When to apply
Walk through the first part (blocks 1–4) before launching the test, and the second part (blocks 5–7) before making the decision on the results. If an item is not closed, write down what needs to be checked, who will do it, and by when. The checklist is a companion document to the design template `M-ab-test-design-template`: the template is filled in during design, the checklist is verified before launch and before interpretation. It catches typical omissions: unrecorded decision rules, SRM (unequal group shares), unaccounted multiple comparisons, and the substitution of "click growth = purchase growth".

## Before launch

### 1. Problem, hypothesis, and benefit
- [ ] Described what is happening now, who it affects, and which data the conclusion is based on. It is clear why the experiment is needed.
- [ ] Wrote down the question the test answers and the decision that depends on the answer. Tied it to the product goal.
- [ ] Named the audience, the change, the mechanism, and the expected effect. It is clear why the behavior should change.
- [ ] Estimated the benefit: in money, orders, or another unit that matters to the product. If using an indirect metric, explained its connection to the goal. For a non-financial task, stated which benefit you are verifying.

**Example.** Over two months, the share of new users who paid for an order after opening the form dropped from 42% to 36%. If we remove two required fields, the form will be easier to complete. We expect the checkout conversion to grow by 5% relative to control without an increase in payment errors. With 10,000 new users per month, that is about 180 additional orders, if each has at most one. This is a forecast. Based on the results, we will decide whether to keep the short form.

### 2. Metrics and decision rules
- [ ] Chose the target metric for the main decision. Set acceptable-harm boundaries for guardrails. Added indirect metrics where they will help understand the cause of the effect.
- [ ] For each key metric, recorded the role, type, formula, source, baseline value, unit of analysis, observation window, and comparison method. For shares and ratios, stated the numerator and the denominator.
- [ ] Before launch, agreed on what result is sufficient, when to abandon the change, and what to do if there is not enough data. Separately recorded what to do when only an indirect metric grows or a guardrail degrades. A violation of the agreed harm boundary blocks the rollout.

### 3. Groups, audience, and exposure
- [ ] Described control and each test variant. Attached screens or a description of the changes.
- [ ] Saved a link to the allocation settings, the experiment ID, the assignment key, and the group shares. If the units of analysis and allocation differ, described how the dependence of observations will be accounted for.
- [ ] Stated who and when enters the test, when assignment happens, and what counts as an actual exposure. Checked the available traffic and explained whether this audience is suitable for a conclusion about a future rollout.
- [ ] Checked overlaps with other tests. Saved the sources, the query, or the code that can restore the groups, exclusions, and calculations. The selection rules were fixed before launch.

### 4. Sample and duration
- [ ] Stated the sample size per group, the shares, the duration, and the stopping rule. Accounted for the inflow of suitable users, seasonality, and the time to the target action.
- [ ] Saved the baseline data, the period, and the calculation. Recorded the significance level and power: e.g., 5% and 80%. Explained the choice if using other values.
- [ ] Separated the expected effect, the minimally useful effect, and the MDE. The MDE shows which effect size the test is designed to detect with the given power. Checked whether this sensitivity is enough for the decision.
- [ ] If several hypotheses are part of the decision, described in advance how multiple comparisons will be accounted for: across metrics, variants, and segments that affect the decision.

## After the test

### 5. What was actually launched
- [ ] Saved a link to the card and the results. Compared actual dates, variants, and group sizes with the design. Explained deviations, condition changes, and restarts.
- [ ] Checked group shares against the plan (SRM), baseline characteristics, and event quality. Analyzed anomalies before interpreting the effect.

### 6. How the result was computed
- [ ] Restored the groups by the assignment key. Used the agreed unit of analysis, windows, and metric definitions. Recorded deduplication, exclusions, and filters with reasons.
- [ ] For each key metric, showed group values, absolute and relative effect, confidence interval, and p-value if used. Provided the spread where necessary. Applied the correction planned in the design.
- [ ] Separated planned comparisons from exploratory analysis. Saved the code or report that can reproduce the calculation.

### 7. What we learned and what we do
- [ ] Analyzed the target, guardrail, and indirect metrics separately. If the change was not confirmed, looked at which effects are still compatible with the data. Click growth by itself does not prove purchase growth.
- [ ] Checked possible flow between scenarios if it matters for the decision. Explained what is confirmed by data and where the mechanism remains an assumption.
- [ ] Applied the pre-agreed rules. Recorded the decision: roll out, abandon, change the variant, or test again. Named the next step, the owner, and the deadline. For a rollout, stated what we will monitor.

## Connection to the pfs process
The checklist completes the `validation` step (pfs step 9) together with the design template `M-ab-test-design-template`: blocks 1–4 are checked when filling the template and before launch (their results are the "Business", "Metrics", "Implementation", and "Hypothesis testing" sections), blocks 5–7 — when filling the "Results" and "Conclusions" sections before `pfs validation` and recording the decision in `pfs decision add`. The statistical base — `M-ab-testing`; metric selection — `M-success-metrics` and `M-product-metrics`.
