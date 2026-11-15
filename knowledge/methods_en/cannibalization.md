---
id: M-cannibalization
lang: en
title: Cannibalization of products, features, pricing tiers, and channels
course: skills
sources: ["EN mirror of the RU methodology card M-cannibalization (knowledge/methods/cannibalization.md); original sources are listed in the RU card"]
stages: [options, strategy, validation, after-decision]
tags: [cannibalization, substitution-flow, increment, metric-tradeoff, pricing-tiers, price, a-b, marketplace, baseline]
related: [M-traction-model, M-unit-economics, M-monetization, M-cjm, M-jtbd, M-quant-methods, M-product-metrics]
---

# Cannibalization of products, features, pricing tiers, and channels

## When to use
A new product, feature, pricing tier, or channel is being launched on an existing base; prices or free-version limits are changing; you need to say how much of the "growth" is pure increment and how much is substitution-flow from the neighboring product.

## Core idea
**Cannibalization** — the effect where a change (new product, feature, channel) pulls users, revenue, or metrics away from an existing product instead of adding pure growth. Causes: the same or an adjacent user job is solved in another way; a shared base; limited demand/attention; positioning errors. Principle: **count the increment, not the total effect:** `Launch effect = New growth − Losses from cannibalization`.

**Conditions making it likely:** a saturated mature market (an operator's new tariffs — clients move to the cheaper one); fast technological progress; price differentiation (a luxury sub-brand pulls buyers from top models); shifting preferences (a non-alcoholic line takes share from the regular one); competitive pressure (a discount for clients who would have renewed anyway); channel expansion (an online store for an offline chain).

**Good and bad:**
| Bad | Good |
|---|---|
| substitution-flow without total growth | new clients arrive, part flows over, total revenue grows |
| new margin lower than the old one | migration "up" to a more expensive product |
| migration "down" to cheap tiers | we cannibalize our own outdated offering before competitors do (strategically) |
| positioning gets diluted | |
The criterion: the sign of the net increment (in both revenue and margin).

**Types:** product-based (a new tier takes share from the old one); price-based (a discount lifts volume, cuts margin); channel-based (a new channel takes from the old one); feature-based (free delivery devalues paid express); segment-based (an economy line attracts the mid segment). The course's parallel taxonomy (lesson 7): **direct** (a product replaces a product: a new smartphone version — easy to model), **indirect** (partially solves the functions of several: a smartphone vs cameras/navigators — hard), **horizontal** (competition between products of the same level: Coca-Cola vs Cherry Coke), **vertical** (migration along a price/feature "funnel": budget → premium).

### Two-sided (cascading) cannibalization on a marketplace
When the business model changes (listing → transactional "turnkey deal"), cannibalization runs **on both sides simultaneously** and reinforces itself: the seller stops paying for listings → less content → the buyer also moves to the new format → the transaction is even more profitable for the seller. Model both sides.
- **The "one budget" principle:** a client has one wallet per job — "you can't take it twice": a dealer pays either for the listing or a commission per deal, not both. A new monetization product always competes with the old one for the same budget.
- **Cascade through the interface:** showing both options on one card ("turnkey deal" next to "message the seller") itself steers the balance of the flow — button placement, benefit descriptions, the visibility of the commission. This is a control lever for cannibalization, not an accident.
- **Does the commission fully replace the listing?** No — it is "either-or" at the level of each deal, but in total the old revenue falls: book the fall of listing revenue as a separate block in the model.

### Calculation method with a baseline ("look at the sum")
```
Baseline (listing):        1000 ₽/mo
After launch:              800 ₽ (listing) + 300 ₽ (transaction)
Cannibalization:           200 ₽ (listing decline)
Net effect:                +100 ₽ — and only if the baseline was computed
```
Build the baseline one of these ways: extrapolating the trend; YoY against a comparable period; a control group without the launch (A/B); a market benchmark of a competitor without the new model. Looking only at the new product (+300) is an error: total revenue must be evaluated against the baseline. The strategic choice: not to launch (keep the revenue), launch (lose part, earn on commission), or launch both and manage the balance through interface and pricing (the hardest path; gate pricing on the old model — see [[M-monetization]]).

**Risks without accounting for it:** loss of revenue, margin, customers; brand dilution; growing operational complexity of the portfolio; internal competition for resources; channel conflict (several managers reaching one client).

## Procedure
1. **Diagnostics:** are the conditions present (list above), which type is likely, do users' jobs overlap (JTBD, CJM — [[M-jtbd]], [[M-cjm]]).
2. **Estimating the scale before launch:** CJM/JTBD analysis; quantitative research on switching probability (surveys, conjoint); concept tests "new vs current"; surveying current clients on their willingness to switch; a portfolio map by criteria; each product's contribution to revenue and costs ([[M-quant-methods]]).
3. **Flow matrix** (for tiers/portfolio): rows — from where, columns — to where, cells — share of clients; add a "churn" column and a "new clients" row.
4. **Increment calculation** (a derived form of the definition):
   - `ΔRevenue = N_new × ARPU_new + Σ M_ij × (ARPU_j − ARPU_i)`, where `M_ij` is the number who migrated from i to j;
   - `ΔMargin` — the same with per-customer margin instead of ARPU;
   - tier line-up: `Net effect = Revenue(TO BE) − Revenue(AS IS)`; check whether margin grew.
5. **The price/base trade-off:** `Revenue = ARPPU × PU`. If ARPPU grows by p, the share of payers may fall by no more than `d = p / (1 + p)` without losing revenue (p = 10% → d ≈ 9.1%). Retention and the mechanics of rolling out price increases must be planned.
6. **Booking into the traction model** ([[M-traction-model]]): as a separate explicit block; by segments; onto **all** model metrics, not only the top level; account for the mediated trade-off (a product that lets you "sell without publishing a listing" reduces content → the number of orders). Two ways: before hypotheses `(Was − Cann.) × K_growth`; after the total effect `(Was × K_growth) × (1 − K_cann)`; the formulas are equivalent at `K_cann = Cann./Was`.
7. **Monitoring after launch:** A/B with measurements in cuts (old and new base separately); pre/post; cohort analysis of old vs new; group isolation (geo/segment), switchback, spillover checks — test and control groups may compete for the same buyers and produce a false effect.
8. **Mitigation:** positioning and value boundaries of the tiers; retention; special mechanics for price increases; disabling a feature in the paid version must be assessed as a churn risk.

### Should cannibalization be booked?
| Question | If "yes" |
|---|---|
| Raising prices / changing monetization? | the paying base shrinks, possibly an inflow of new users |
| Limiting the paid version's functionality? | part of the users churn |
| A new product on the current base for the same job? | substitution-flow, the "old" metrics fall |
| The trade-off could be mediated? | model the chain of effects |

### Case (skill): an operator's tier line-up
Goal — how much value to put into each tier to minimize churn and downward flow and grow margin: AS IS (Revenue, markup by tier) → TO BE → upward/downward flow → net effect → margin check. The key: book not only ARPPU growth but also the shrinking paying base.

## Template / checklist
| Field | Fill in |
|---|---|
| The change (what we launch) | |
| Cannibalization type | product / price / channel / feature / segment |
| Victim (product/segment/metric) | |
| Scale estimation method, evidence class | |
| Flow matrix (min/base/max) | |
| Increment: revenue, margin | |
| Where in the model (block, formula, K_cann) | |
| Monitoring metrics, reaction thresholds | |
Verification questions: what would happen without the launch? where did users/revenue come from? how did the total result change?
Exit: diagnostics → scale estimation → increment calculation → a block in the model → mitigation → monitoring.

## Common mistakes
- "We'll see later, when we scale" — inflated expectations.
- Showing the total launch effect instead of the increment.
- Estimating cannibalization only at the top level of metrics.
- Forgetting that downward flow cuts margin even when clients grow.
- Reading an A/B result without a spillover check.
- Adding the new product's effect to the effects of other hypotheses on the same base without a discount ([[M-traction-model]]).

## Questions that can change the decision
- Does the new product solve the same JTBD as the existing one?
- Is there data on the base's willingness to switch (a survey, migration history)?
- Is the new product's margin higher or lower?
- Can groups be isolated for an honest test?
- What happens if we don't launch and a competitor does (strategic cannibalization)?

## Related maps
[[M-traction-model]], [[M-unit-economics]], [[M-monetization]], [[M-cjm]], [[M-jtbd]], [[M-quant-methods]], [[M-product-metrics]]
