---
id: M-pricing-ladder
lang: en
title: Tier ladder pricing — ARPU mix, freemium conversion, payer CAC, annual plans
course: strategy
sources: ["EN mirror of the RU methodology card M-pricing-ladder (knowledge/methods/pricing-ladder.md); original sources are listed in the RU card"]
stages: [strategy, validation]
tags: [pricing, tiers, ladder, arpu, freemium, payer-cac, annual-plans, value-metric]
related: [M-monetization, M-unit-economics, M-van-westendorp, M-traction-model, M-cannibalization, M-ab-testing]
---

# Tier ladder pricing

## When to apply
When the product has more than one tier or tiers are planned: laying out "Free → Base → Pro → Enterprise",
choosing the value metric, computing the ARPU mix, checking that freemium adds up, and the decision on annual
plans. The card is the bridge between [[M-monetization]] (model choice) and [[M-unit-economics]]
(the viability check).

## Core
A tier ladder is not "several prices" but a mechanism for distributing the base across price points:
**ARPU = Σ(tier price × tier share of the base)**. Three consequences follow.

1. **ARPU is always weighted.** An unweighted average across tiers is a lie: a base of 90% Free and 10% Pro
   does not produce "an average between 0 and 1000". Compute ARPU on the actual mix and watch its drift
   across cohorts.
2. **Each rung of the ladder is bought with value, not features.** Every next tier is justified by a
   qualitative jump: limits that remove a real scale pain (volume, seats, automation, support). Big-step rule:
   price ×2–3 for a noticeably new value; small steps of 10–15% teach the customer to pick the cheapest tier.
3. **The value metric is what people pay for.** The metric must grow with the customer's value (seats, users,
   deals, data volume), be predictable for the buyer, and be easy to measure. A wrong value metric breaks the
   ladder: customers pay for something other than what is actually valuable to them.

**Freemium conversion.** The Free tier is an acquisition channel, not charity: its cost is borne by everyone.
The entry economics only add up if `CR_free→paid` carries the load: `CAC_payer = CAC_acquisition /
CR_free→paid` (acquisition at 300 with a 5% conversion → a paying user costs 6000). The minimum share of
payers at which freemium survives: `min_payer_share ≈ cost_to_serve_user / ARPPU`. Check it on retrospective
cohorts before scaling acquisition.

**Annual plans.** An annual subscription is a prepayment: it reduces churn in the first 12 months and
accelerates cash flow, but it sells at a discount (typically 15–20%, i.e., "2 months free"). The effect on the
economics is double-edged: LTV per user rises (low early churn), monthly ARPU falls (the discount), and the
discount cannibalizes the monthly plan — part of the base that would have stayed anyway pays less. An annual
plan pays off when `discount < churn savings + cost of capital`; verify with an A/B price test and a
comparison of annual vs monthly cohort retention.

## Procedure (agent)
1. Collect the actual mix: tier shares, ARPPU per tier, CR free→paid per cohort — every number with a source
   and a date (`pfs claim add --kind fact`).
2. Compute the ARPU mix and the payer CAC; compare payer payback against the target horizon.
3. Check the value metric: what the best customers actually pay for; does the counter grow with their value.
4. Design the ladder steps: for every transition, "what hurts on the previous tier → what they buy on the
   next one".
5. Model it in [[M-traction-model]]: three mix scenarios (pessimistic / base / optimistic on conversion and
   the annual-plan share) — see [[M-scenario-modeling]].
6. Check cannibalization: who on the new tier would have been a payer on the old one ([[M-cannibalization]]).
7. Validation plan: A/B the price and the annual discount; metrics — CR free→paid, ARPU, payback, churn
   per tier.

## Template / checklist
- [ ] ARPU computed weighted, per cohort, not as an average of the price list;
- [ ] every ladder transition names the pain of the previous tier and the value bought;
- [ ] one value metric, predictable, growing with customer value;
- [ ] payer CAC = CAC / CR free→paid, and it pays back within the target horizon;
- [ ] the annual-plan share and the discount size are a hypothesis with an A/B plan, not "that is what
      competitors do";
- [ ] cannibalization of the monthly plan by the annual plan is estimated in the model.

## Typical mistakes
- "Average ARPU across tiers": averaging the price list instead of weighting by the base.
- CAC without conversion: acquisition costs 300, a paying user costs 6000; LTV is compared against the first
  number.
- A ladder of checkboxes: "Pro differs by support" — not a value jump but a reason to stay on Base.
- An annual discount as a promotion without math: cannibalization of the monthly plan eats the churn win.
- Too many tiers: choice fatigue, an unmanageable ARPU mix; 3–4 rungs is the ceiling for self-serve.

## Questions that could change the decision
- What share of the base is ready to pay at all (the size of the "paying core")?
- Will the annual plan eat the monthly one without a retention win?
- Which value metric will survive two more years of product growth?

## Related cards
[[M-monetization]] — choosing the monetization model; [[M-unit-economics]] — viability and payback checks;
[[M-van-westendorp]] — price sensitivity research; [[M-traction-model]] — the growth model;
[[M-cannibalization]] — flow between tiers and plans.
