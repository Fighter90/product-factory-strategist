---
id: M-ml-for-product
lang: en
title: ML for product managers — where ML is justified, hypotheses and validation, model quality metrics vs business metrics, ML in A/B tests, risks
course: data
sources: ["EN mirror of the RU methodology card M-ml-for-product (knowledge/methods/ml-for-product.md); original sources are listed in the RU card"]
stages: [options, strategy, validation]
tags: [ml, machine-learning, regression, classification, ranking, precision, recall, ndcg, ml-cuped, uplift, leakage, data-driven]
related: [M-ab-testing, M-product-metrics, M-quant-methods, M-forecasting-product, M-genai-product-development, M-solution-design]
---

# ML for Product Managers

## When to apply
The team thinks "we need ML here": price suggestions, anti-fraud, recommendations, demand forecasting. You need to decide whether ML is justified, turn the idea into a testable ML hypothesis, agree on model quality metrics and business metrics, and verify the effect in the product — including boosting A/B tests with ML methods.

## Essence

### Where ML is justified (and where it is not)
ML is justified when the pattern is complex/multidimensional and cannot be expressed as rules:
- **Search and ranking** — query semantics, user behavior, item quality; without ML marketplaces and content services do not scale.
- **Recommendations** — personalized "similar items" blocks, feeds; they grow engagement and conversion.
- **Risk classification** — anti-fraud, content moderation, scoring (Recall is critical).
- **Regression/forecasting** — price, time to transaction, demand, load, fraud spikes.
- **Clustering** — finding segments and generating hypotheses.
- **Pricing and auto-bidding** — dynamic prices and bids.
ML is NOT needed when: data is absent (no data, no ML), the dependency is simple and well captured by rules/SQL, a human makes the decision on qualitative data, and model accuracy does not pay back its complexity and risks. Rule of thumb: first a simple model/rule as the baseline, ML — only when it provably beats the baseline on the business metric.

### ML task types through a product manager's eyes
| Task | Question | Product examples | Metrics |
|---|---|---|---|
| Regression | predict a number | price, time to transaction, demand | MAE, MAPE, RMSE |
| Classification | predict a probability/class | fraud, rule violations, "will buy / won't buy" | Precision, Recall, ROC-AUC |
| Clustering | find segments | employer/buyer segments | silhouette + interpretability of segments |
| Ranking | order of items | search, recommendations, feed | NDCG, MRR, Recall@k, Precision@k |
Notes: Precision — the share of correct items among those the model flagged; Recall — the share of found items among all real ones (for fraud/moderation ≥90% is a typical bar); ROC-AUC — quality of class separation; NDCG/MRR — quality of the ordering of results. An error like "precision for regression" is a sign of a wrong problem setup.

### ML hypothesis template (7 steps)
1. **Problem/business context with numbers**: "in category X sellers underprice by 20–30%, which lowers GMV and margin".
2. **Narrow ML task**: extract a subtask from the problem — classification "good/bad price", regression "optimal price", ranking "which price to show".
3. **Data**: are there historical examples, labels, behavioral data; will they be available in the future at the moment of application. No data → the hypothesis is dead on arrival.
4. **Decision point** — where the model's output "sits" in the product: at ad creation, in the feed, at checkout. ML without a place of application is meaningless.
5. **Business metric** — the KPI of the hypothesis: GMV, CR, retention, transaction time, fraud share.
6. **Model quality metrics** — the second level of KPIs by task type (table above).
7. **Success criteria along all three axes**: business (e.g., +4% GMV in the category), model (e.g., MAE < 12%), UX (e.g., ≤10% of users reject the suggestion).
Examples of "business ↔ model" pairs: moderation — reduced risk / growing trust ↔ Recall > 90%; time-to-transaction forecast — growing salability CR ↔ MAPE < 20%; recommendations — GMV growth ↔ NDCG > 0.25. When planning, verify the thresholds are achievable (is AUC > 0.75 / MAPE < 20% achievable on this data?).

### Model quality metrics vs product metrics
- Model metrics are a development tool; the business metric is the success criterion. High model accuracy guarantees the product nothing: AUC 0.95 with zero impact on CR is a useless model.
- Class balance and the cost of errors: the classification threshold is chosen for the product (anti-fraud — sacrifice Precision for Recall; price suggestions — the opposite).
- Offline metrics ≠ online effect: roll out only after validation on live users (A/B). Offline/online divergence is a normal reason for research, not for "tuning the threshold".
- Ranking is validated on complex metrics (NDCG/MRR/Recall@k), because plain CTR is not enough.

### ML as an analytics and hypothesis-generation tool
- **Factor analysis:** a model (e.g., gradient boosting) shows which features actually influence the target metric (feature importances/SHAP) — a source of hypotheses ("what drives subscription purchases / item pricing").
- **Clustering:** finding segments invisible in reports → personalized hypotheses and campaigns.
- **Forecasting:** time-series components and models — see [[M-forecasting-product]]; typical mistakes: ignoring seasonality, poor cleaning, leakage, blind trust, missing business logic.
- **ML in A/B tests** ([[M-ab-testing]]):
  - **CUPED / ML-CUPED** — variance reduction: the covariate X = the pre-test value of the metric (classic) or an ML model's prediction of "what the metric would have been without the feature" (the ML version uses more data and dynamics). Adjusted metric = Y − θ·(X − E[X]); θ is estimated on the pre-period. The effect — up to 2–3x faster tests (21 days → 7–10).
  - **Propensity score / stratification** — aligning heterogeneous groups when the split turned out unequal in "strong" users: the model estimates the probability of landing in a group, and weighting removes the bias.
  - **Uplift modeling** — when the average effect ≈ 0 but segments show an effect: the model predicts the individual effect (T/S/X-learner, causal forests, uplift trees); the PM picks the segment with the strongest effect and rolls out selectively.
  - **Complex metrics** (search, recommendations) — tests on NDCG/MRR/Recall@k with ML variance-reduction methods.
  - Risks: ML without bias checks, a poor covariate (includes the post-test period = leakage), applying it without business understanding.

### Validating ML solutions
1. **Offline:** labeling/retrospective, quality metrics by task type, comparison against a simple baseline (rules, mean, naive forecast).
2. **Online:** an A/B test of the business metric with guardrails (conversion, complaints, latency) — an ML feature proves itself like any product.
3. **Post-launch:** monitoring data drift and model quality (feature distributions drift — accuracy falls), a retraining loop, fallback logic when the model fails.
4. Slices: check whether the experience degraded in minority segments (the model optimizes the average).

### Three pairs "task → mechanics in the product → criteria" (templates)
| Task | Mechanics (decision point) | Business metric | Model metric |
|---|---|---|---|
| Ad moderation (classification) | stopping publication + manual review | reduced risk, growing trust | Recall > 90% |
| "Time to transaction" suggestion (regression) | suggestion at ad creation | growing salability CR | MAPE < 20% |
| Similar items (ranking) | "Similar" block on the item page | GMV | NDCG > 0.25 |
The pattern in all three: a narrow task at the point of contact + a "business metric / model metric" pair + online validation. A model without a decision point is not built.

## Procedure
1. Check whether ML is needed: is there data, can the task be solved with rules, does the effect pay back the complexity.
2. Fill in the hypothesis template (7 steps): problem with numbers → narrow ML task → data → decision point → business metric → model metric → success criteria along three axes.
3. Fix a simple baseline solution to compare against.
4. Offline training and validation: the right metrics for the task, a leakage check (no data "from the future"), a Precision/Recall balance that matches the cost of errors.
5. Design the online validation: A/B with CUPED/ML-CUPED under high variance, uplift analysis when the average effect ≈ 0; guardrail metrics and thresholds.
6. Decide on the business metric (not the model one), set up drift monitoring and a retraining plan.
7. Write the conclusions into the knowledge base: what worked, which data/features were decisive.

## Template / checklist (ML hypothesis card)
```
Problem (with numbers): ___
ML task: regression | classification | clustering | ranking: ___
Data: history ___ labels ___ features ___ (leakage checked: yes/no)
Decision point: ___ (where the model meets the user)
Business metric and criterion: ___  Model metric and threshold: ___
UX/safety criterion: ___
Baseline (without ML): ___  Online validation plan: A/B + guardrails ___
Post-launch monitoring: drift ___ retraining ___ fallback ___
```
Checklist: data exists and will exist at the moment of application · the task is narrow · the business metric outranks the model metric · the model threshold is achievable and justified by the cost of errors · comparison against a baseline · an online validation is planned · leakage excluded · a monitoring and rollback plan exists.

## Typical mistakes
- "Improve search/recommendations" instead of a narrow task with a metric — not a hypothesis.
- No business metric: model accuracy as the goal; AUC for AUC's sake.
- No data (or data will not be available at the moment of application) — yet the hypothesis goes into development anyway.
- Leakage: features containing target information or "the future"; offline metrics inflated.
- Blind trust in the model: no baseline, no sanity-check, no business logic in validation.
- The wrong error balance: for fraud they optimize Precision and lose violators (or the reverse — block normal users).
- The CUPED covariate is taken from the post-test period; the group split is not checked for homogeneity.
- Data drift is not monitored: the model "quietly" degrades after launch.
- Explainability: wherever the model affects users directly (moderation, prices, scoring), a black box without explanations and selective decision audits is a trust risk and a regulatory risk.
- ML for ML's sake where a rule/SQL is cheaper, clearer and more reliable.

## Questions that can change the decision
- Is there data with history and labels — and will it be available at the moment the model is applied?
- What is the simple alternative (rules, mean, naive forecast), and by how much must ML beat it on the business metric?
- What is the cost of model errors in both directions, and which Precision/Recall threshold corresponds to it?
- How will the effect be validated online, and which guardrail metrics could suffer?
- What happens to model quality in 3–6 months (data drift), and who is responsible for retraining?

## Related cards
[[M-ab-testing]], [[M-product-metrics]], [[M-quant-methods]], [[M-forecasting-product]], [[M-genai-product-development]], [[M-solution-design]]
