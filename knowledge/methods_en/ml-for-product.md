---
id: M-ml-for-product
lang: en
title: ML for product managers — where ML is justified, hypothesis validation, model quality metrics vs business metrics, ML in A/B tests, risks
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [options, strategy, validation]
tags: [ml, machine-learning, regression, classification, ranking, precision-recall, ndcg, ml-cuped, uplift, data-leakage]
related: [M-ab-testing, M-product-metrics, M-quant-methods, M-forecasting-product, M-genai-product-development, M-solution-design]
---

# ML for the Product Manager

## When to apply
The team is thinking "we need ML here": a price hint, antifraud, recommendations, a demand forecast. You need to decide whether ML is justified, turn the idea into a testable ML hypothesis, agree on the model-quality metrics and the business metrics, and check the effect in the product — including strengthening A/B tests with ML methods.

## Core idea

### Where ML is justified (and where it is not)
ML is justified when the pattern is complex/multidimensional and cannot be expressed as rules:
- **Search and ranking** — query semantics, user behavior, item quality; without ML marketplaces and content services do not scale.
- **Recommendations** — personalized "similar items" blocks, feeds; they grow engagement and conversion.
- **Risk classification** — antifraud, content moderation, scoring (Recall is critical).
- **Regression/forecast** — price, time to deal, demand, load, fraud spikes.
- **Clustering** — finding segments and generating hypotheses.
- **Pricing and autobidding** — dynamic prices and bids.
ML is NOT needed when: there is no data (no data, no ML), the dependency is simple and is well captured by rules/SQL, a human makes the decision on qualitative data, and the model's accuracy does not pay for the complexity and risks. Rule: start with a simple model/rule as the baseline; ML only when it demonstrably beats the baseline on a business metric.

### ML task types through a PM's eyes
| Task | Question | Product examples | Metrics |
|---|---|---|---|
| Regression | predict a number | price, time to deal, demand | MAE, MAPE, RMSE |
| Classification | predict a probability/class | fraud, rule violations, "will buy / won't buy" | Precision, Recall, ROC-AUC |
| Clustering | find segments | employer/buyer segments | silhouette + interpretability of the segments |
| Ranking | the order of objects | search, recommendations, feed | NDCG, MRR, Recall@k, Precision@k |
Clarifications: Precision — the share of correct items among those the model "flagged"; Recall — the share found among all real cases (for fraud/moderation ≥90% is a typical bar); ROC-AUC — the quality of class separation; NDCG/MRR — the quality of the output ordering. A mistake like "precision for a regression" is a sign of a wrong problem statement.

### The ML hypothesis template (7 steps)
1. **Problem/business context** with numbers: "in category X sellers underprice by 20–30%, which hurts GMV and margin."
2. **A narrow ML task**: carve a subtask out of the problem — classification "good/bad price," regression "the optimal price," ranking "which price to show."
3. **Data**: are there historical examples, labels, behavioral data; could they exist at the moment of application in the future. No data → the hypothesis is dead.
4. **The decision point** — where the model's output "slots into" the product: at listing creation, in the feed, at payment. ML with no place of application is meaningless.
5. **The business metric** — the hypothesis KPI: GMV, CR, retention, deal time, the share of fraud.
6. **Model-quality metrics** — the second level of the KPI, by task type (the table above).
7. **Success criteria on all three axes**: business (e.g., +4% GMV in the category), model (e.g., MAE < 12%), UX (e.g., ≤10% of users reject the hint).
Examples of "business ↔ model" pairs: moderation — lower risk / more trust ↔ Recall > 90%; a time-to-deal forecast — a higher sellability CR ↔ MAPE < 20%; recommendations — GMV growth ↔ NDCG > 0.25. When planning, check that the thresholds are attainable (is AUC > 0.75 / MAPE < 20% attainable on this data?).

### Model-quality metrics vs product metrics
- Model metrics are a development tool; the business metric is the success criterion. High model accuracy guarantees nothing for the product: AUC 0.95 with zero impact on CR is a useless model.
- Class balance and the cost of errors: the classification threshold is chosen to fit the product (antifraud sacrifices Precision for Recall; price hints — the other way around).
- Offline metrics ≠ the online effect: roll out only after validation on live users (A/B). Offline/online divergence is a normal reason to investigate, not to "tune the threshold."
- Ranking is validated on complex metrics (NDCG/MRR/Recall@k), because plain CTR is not enough.

### ML as an analytics and hypothesis-generation tool
- **Factor analysis:** a model (e.g., gradient boosting) shows which features actually affect the target metric (feature importances/SHAP) — a source of hypotheses ("what drives a subscription purchase / the price of an item").
- **Clustering:** finding segments that are invisible in reports → personalized hypotheses and campaigns.
- **Forecasting:** time-series components and models — see [[M-forecasting-product]]; typical mistakes: ignoring seasonality, poor cleaning, leakage, blind trust, the absence of business logic.
- **ML in A/B tests** ([[M-ab-testing]]):
  - **CUPED / ML-CUPED** — variance reduction: the covariate X = the metric's pre-test value (classic) or an ML model's prediction of "what the metric would have been without the feature" (the ML version uses more data and the dynamics). Adjusted metric = Y − θ·(X − E[X]); θ is estimated on the pre-period. The effect — up to a 2–3× speedup of the test (21 days → 7–10).
  - **Propensity score / stratification** — leveling heterogeneous groups when the split came out unequal on "strong" users: the model estimates the probability of landing in a group, and the weighting removes the bias.
  - **Uplift modeling** — when the average effect ≈ 0 but there is an effect inside segments: the model predicts the individual effect (T/S/X-learners, causal forests, uplift trees); the PM picks the segment with the strongest effect and rolls out in a targeted way.
  - **Complex metrics** (search, recommendations) — tests on NDCG/MRR/Recall@k with ML variance-reduction methods.
  - Risks: ML without a bias check, a poor covariate (it uses the post-test period = leakage), applying it without business understanding.

### Validating ML solutions
1. **Offline:** labels/retrospective, quality metrics by task type, comparison against a simple baseline (rules, the mean, a naive forecast).
2. **Online:** an A/B test of the business metric with guardrails (conversion, complaints, latency) — an ML feature proves itself like any other product.
3. **Post-launch:** monitoring data drift and model quality (feature distributions drift — accuracy falls), a retraining cycle, fallback logic when the model fails.
4. Cuts: has the experience worsened for minority segments (a model optimizes the average)?

### Three pairs of "task → mechanism in the product → criteria" (templates)
| Task | Mechanism (decision point) | Business metric | Model metric |
|---|---|---|---|
| Listing moderation (classification) | stop the publication + manual review | lower risks, more trust | Recall > 90% |
| A "time to deal" hint (regression) | a hint at listing creation | a higher sellability CR | MAPE < 20% |
| Similar items (ranking) | a "Similar" block on the item page | GMV | NDCG > 0.25 |
The pattern in all of them: a narrow task at the point of contact + a "business metric / model metric" pair + an online check. A model without a decision point is not built.

## Procedure
1. Check whether ML is needed: is there data, can the task be solved with rules, does the effect pay for the complexity.
2. Fill in the hypothesis template (7 steps): the problem with numbers → the narrow ML task → data → the decision point → the business metric → the model metric → success criteria on the three axes.
3. Fix a simple baseline solution to compare against.
4. Offline training and validation: the right metrics for the task, a leakage check (no data "from the future"), the Precision/Recall balance matched to the cost of errors.
5. Design the online check: A/B with CUPED/ML-CUPED under high variance, uplift analysis when the average effect ≈ 0; guardrail metrics and thresholds.
6. Make the decision on the business metric (not the model one); fix drift monitoring and a retraining plan.
7. Write the conclusions into the knowledge base: what worked, which data/features were decisive.

## Template / checklist (ML hypothesis card)
```
Problem (with numbers): ___
ML task: regression | classification | clustering | ranking: ___
Data: history ___ labels ___ features ___ (leakage checked: yes/no)
Decision point: ___ (where the model meets the user)
Business metric and criterion: ___  Model metric and threshold: ___
UX/safety criterion: ___
Baseline (without ML): ___  Online check plan: A/B + guardrail ___
Post-launch monitoring: drift ___ retraining ___ fallback ___
```
Checklist: the data exists and will exist at the moment of application · the task is narrow · the business metric outranks the model metric · the model threshold is attainable and justified by the cost of errors · a comparison against a baseline exists · an online check is planned · leakage is excluded · a monitoring and rollback plan exists.

## Typical mistakes
- "Improve search/recommendations" instead of a narrow task with a metric — not a hypothesis.
- No business metric: model accuracy as the goal; AUC for AUC's sake.
- No data (or the data will not be available at the moment of application) — yet the hypothesis is handed to development anyway.
- Leakage: features containing target information or "the future"; inflated offline metrics.
- Blind trust in the model: no baseline, no sanity check, no business logic in the validation.
- The wrong error balance: for fraud they optimize Precision and lose the violators (or the reverse — block normal users).
- The CUPED covariate is taken from the post-test period; the group split is not checked for homogeneity.
- Data drift is not monitored: the model "quietly" degrades after launch.
- Explainability: where the model touches users directly (moderation, prices, scoring), a black box without explanations and sampled audits of decisions is a trust risk and a regulatory risk.
- ML for ML's sake where a rule/SQL is cheaper, clearer and more reliable.

## Questions that can change the decision
- Is there data with history and labels — and will it be available at the moment the model runs?
- What is the simple alternative (rules, the mean, a naive forecast), and by how much must ML beat it on the business metric?
- What is the cost of the model's error in both directions, and which Precision/Recall threshold corresponds to it?
- How will the effect be verified online, and which guardrail metrics might suffer?
- What happens to the model's quality in 3–6 months (data drift), and who is responsible for retraining?

## Related maps
[[M-ab-testing]], [[M-product-metrics]], [[M-quant-methods]], [[M-forecasting-product]], [[M-genai-product-development]], [[M-solution-design]]
