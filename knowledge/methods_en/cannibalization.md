---
id: M-cannibalization
lang: en
title: Cannibalization of products, features, plans and channels
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [options, strategy, validation, after-decision]
tags: [cannibalization, flow-over, increment, metric-tradeoffs, plans, price, ab-testing, marketplace, baseline]
related: [M-traction-model, M-unit-economics, M-monetization, M-cjm, M-jtbd, M-quant-methods, M-product-metrics]
---

# Cannibalization of products, features, plans and channels

## When to apply
A new product, feature, plan or channel is being launched onto an existing base; prices or free-version limits are changing; you need to say how much of the "growth" is net increment and how much is flow over from a neighboring product.

## Core idea
**Cannibalization** is the effect where a change (a new product, feature, channel) pulls users, revenue or metrics away from an existing product instead of adding pure growth. Causes: the same or an adjacent user job gets solved in a different way; a shared base; limited demand/attention; positioning mistakes. Principle: **count the increment, not the gross effect:** `Launch effect = New growth − Cannibalization losses`.

**Conditions under which it is likely:** a saturated mature market (a telco launches new plans — clients move to a cheaper one); fast technological progress; price differentiation (a luxury sub-brand takes buyers from the top models); a shift in preferences (a non-alcoholic line takes share from the regular one); competitive pressure (a discount to clients who would have renewed anyway); channel expansion (an online store for an offline chain).

**Good and bad:**
| Bad | Good |
|---|---|
| flow over with no total growth | new customers arrive, some flow in, total revenue grows |
| the new item's margin is lower than the old one's | migration "upward" to a more expensive product |
| migration "down" to cheaper plans | we cannibalize our own obsolete offering before competitors do (strategically) |
| positioning gets blurred | |
Criterion: the sign of the net increment (in revenue and in margin alike).

**Types:** product (a new plan takes share from the old one); price (a discount raises volume and cuts margin); channel (a new channel takes from the old one); feature (free delivery devalues paid express); segment (an economy line attracts the mid segment). The course's parallel taxonomy (session 7): **direct** (a product replaces a product: a new smartphone version — easy to model), **indirect** (partially solves the functions of several: a smartphone vs cameras/navigators — hard), **horizontal** (competition between products of the same level: Coca-Cola vs Cherry Coke), **vertical** (migration along a price/feature "funnel": budget → premium).

### Two-sided (cascading) cannibalization in a marketplace
When the business model changes (listing → a transactional "done-for-you deal"), cannibalization runs **on both sides at once** and reinforces itself: the seller stops paying for the listing → there is less content → the buyer, too, moves to the new format → the transaction becomes even more attractive to the seller. Model both sides.
- **The "one budget" principle:** the client has one wallet for one job — "you cannot take it twice": the dealer pays either for the listing or the deal commission, but not both. A new monetization product always competes with the old one for the same budget.
- **The cascade through the interface:** showing both options on one card ("done-for-you deal" next to "message the seller") steers the flow balance by itself — button placement, the description of the benefits, the visibility of the commission. This is a control lever for cannibalization, not an accident.
- **Does the commission replace the listing completely?** No — it is "either-or" at the level of each individual deal, but in total the old revenue falls: plan the listing revenue decline as a separate block in the model.

### Baseline calculation method ("look at the total")
```
Baseline (listing):         1000 ₽/mo
After launch:               800 ₽ (listing) + 300 ₽ (transaction)
Cannibalization:            200 ₽ (listing decline)
Net effect:                 +100 ₽ — and only because the baseline was computed
```
Build the baseline in one of these ways: extrapolation of the trend; YoY against an analogous period; a control group without the launch (A/B); a market benchmark of a competitor without the new model. Looking only at the new product (+300) is the mistake: the total revenue is evaluated against the baseline. Strategic choice: not launch (keep the revenue), launch (lose a part, earn on the commission), launch both and steer the balance with the interface and prices (the hardest path; barrier pricing on the old model — see [[M-monetization]]).

**Risks of ignoring it:** loss of revenue, margin, clients; brand dilution; growing operational complexity of the portfolio; internal competition for resources; channel conflict (several managers approaching one client).

## Procedure
1. **Diagnostics:** are the conditions present (the list above), which type is likely, do the users' jobs overlap (JTBD, CJM — [[M-jtbd]], [[M-cjm]]).
2. **Estimate the scale before launch:** CJM/JTBD analysis; quantitative research on the probability of switching (surveys, conjoint); "new versus current" concept tests; a survey of current clients about their willingness to switch products; a portfolio map by criteria; each product's contribution to revenue and costs ([[M-quant-methods]]).
3. **Transfer matrix** (for plans/a portfolio): rows — from where, columns — to where, cells — share of clients; add a "churn" column and a "new clients" row.
4. **Increment calculation** (a derivative form of the definition):
   - `ΔRevenue = N_new × ARPU_new + Σ M_ij × (ARPU_j − ARPU_i)`, where `M_ij` is the number who migrated from i to j;
   - `ΔMargin` — the same with per-client margin instead of ARPU;
   - plan ladder: `Net effect = Revenue(TO BE) − Revenue(AS IS)`; check whether the margin grew.
5. **Price/base trade:** `Revenue = ARPPU × PU`. If ARPPU grows by p, the share of payers may fall by no more than `d = p / (1 + p)` without losing revenue (p = 10% → d ≈ 9.1%). You need to plan retention and the rollout mechanics for the price increase.
6. **Embedding in the traction model** ([[M-traction-model]]): as a separate explicit block; by segments; onto **all** the model's metrics, not only the top level; account for the indirect trade (a product "sell without publishing a listing" reduces content → the number of orders falls). Two ways: before the hypotheses `(Was − Cann) × K_growth`; after the total effect `(Was × K_growth) × (1 − K_cann)`; the formulas are equivalent at `K_cann = Cann/Was`.
7. **Monitoring after launch:** A/B with measurements in the cuts (old and new base separately); pre/post; cohort analysis of old versus new; group isolation (geo/segment), switchback, a spillover check — the test and control groups may compete for the same buyers and produce a false effect.
8. **Mitigation:** positioning and value boundaries between the plans; retention; special mechanics for price increases; disabling a feature in the paid version is to be evaluated as a churn risk.

### Should cannibalization be modeled in?
| Question | If "yes" |
|---|---|
| Raising prices / changing monetization? | the paying base shrinks, possibly an inflow of new clients |
| Limiting the paid version's functionality? | some users churn |
| A new product on the current base for the same job? | flow over, the "old" product's metrics fall |
| Can the trade be indirect? | model the chain of effects |

### Case (skill): a telco's plan ladder
The goal — how much value to put into each plan so as to minimize churn and downward flow and grow the margin: AS IS (revenue, markup by plans) → TO BE → flow up/down → net effect → margin check. The key: plan not only ARPPU growth but also the decline of the paying base.

## Template / checklist
| Field | Fill in |
|---|---|
| Change (what we launch) | |
| Cannibalization type | product / price / channel / feature / segment |
| Victim (product/segment/metric) | |
| Scale estimation method, confidence class | |
| Transfer matrix (min/base/max) | |
| Increment: revenue, margin | |
| Where in the model (block, formula, K_cann) | |
| Monitoring metrics, reaction thresholds | |
Verification questions: what would have happened without the launch? where did the users/revenue come from? how did the total result change?
Exit path: diagnostics → scale estimation → increment calculation → a block in the model → mitigation → monitoring.

## Typical mistakes
- "We'll look at it later, when we scale" — inflated expectations.
- Showing the gross launch effect instead of the increment.
- Estimating cannibalization only at the top level of the metrics.
- Forgetting that downward flow cuts the margin even when the client count grows.
- Reading an A/B result without a spillover check.
- Summing the new product's effect with the effects of other hypotheses on the same base without a discount ([[M-traction-model]]).

## Questions that can change the decision
- Does the new one solve the same JTBD as the existing one?
- Is there data on the base's willingness to switch products (a survey, the history of migrations)?
- Is the new product's margin higher or lower?
- Can the groups be isolated for an honest test?
- What happens if we don't launch but a competitor does (strategic cannibalization)?

## Related maps
[[M-traction-model]], [[M-unit-economics]], [[M-monetization]], [[M-cjm]], [[M-jtbd]], [[M-quant-methods]], [[M-product-metrics]]
