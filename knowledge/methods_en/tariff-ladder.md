---
id: M-tariff-ladder
lang: en
title: Tariff ladder pricing — ARPU mix, freemium, paying-user CAC, annual plans
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [strategy, validation, after-decision]
tags: [pricing, tariff-plans, arpu, freemium, cac, annual-plans, ladder]
related: [M-monetization, M-unit-economics, M-van-westendorp, M-cannibalization, M-traction-model, M-benchmarking]
---

# Tariff ladder: ARPU mix, freemium, annual plans

## When to apply
When a product is sold through several tiers (a "ladder"): choose the number and boundaries of the tiers, the
price of each one, the share of free, the size of the annual discount — and check whether the economics add up
not "on the top tier" but on the real mix (PRO-51: a typical calculation mistake is using the ARPU of the most
expensive tier).

## Core idea
A ladder is a managed mix: revenue is computed not from a tier's price but from the weighted-average ARPU across
the shares of the base.

Key formulas:
- `ARPU = Σ(Tier_price × Tier_share)` — a weighted average, not the arithmetic mean of tier prices;
- `LTV = ARPU × Lifetime × GM%` (or the cohort method, if the mix changes as the cohort ages);
- `CAC_payer = CAC_acquisition / CR_free→paid` — the freemium conversion multiplies the per-user cost;
- minimum share of payers `≈ User_cost / Paying_ARPU`;
- annual plan: `Annual_ARPU = Monthly_price × 12 × (1 − Discount)`; the effect is a lump of cash upfront and a
  lifetime mix.

Ladder design:
- 3–4 steps: free (or trial) → basic → core (the sales anchor) → premium (the price anchor; it raises the
  perceived value of the core tier);
- the steps differ by **value metric** — a parameter that grows with the value to the customer (storage, users,
  requests, deals), not by "stars" and support;
- the core tier is the one the target mix is designed around; its price is validated with the Van Westendorp range;
- the annual plan is a retention tool, not just a cash tool: the discount pays off if it is smaller than the churn
  it saves (an annual plan "freezes" 12 months of payment);
- transitions between steps: upgrade triggers (hitting a limit) and downgrade paths (keep the payer on a lower
  step instead of losing them).

Checking the ladder's economics: UE is computed on cohorts and the mix. If `UE > 0` only under "everyone is on
premium" — the mix is unrealistic. Cannibalization: premium must not eat the core tier (see
[[M-cannibalization]]), and free must not eat the core tier either (freemium cannibalization is checked via
conversion and the share of "eternal free" users).

## Procedure
1. Fix the value metric and the steps; for each step set the target share of the base and the justification for
   that share (benchmark or data).
2. Compute the target ARPU on the mix; compare it with the ARPU needed for `LTV > CAC` — the gap is the mix risk.
3. For freemium: compute the paying-user CAC at the current and the target conversion; check the minimum share of
   payers.
4. For the annual plan: compute the price, the payback threshold of the discount
   (`Discount < Annual_churn × 12`) and the impact on cash.
5. Check the ladder for cannibalization between steps; redistribute features between steps if needed.
6. Validate prices with the Van Westendorp range ([[M-van-westendorp]]) and a benchmark ([[M-benchmarking]]).
7. Plan an A/B test or a rollout with a control group and metrics: mix, ARPU, conversion, churn per step.

## Template / checklist
| Parameter | Free | Basic | Core | Premium | Annual |
|---|---|---|---|---|---|
| Price (month) | | | | | |
| Target share of the base | | | | | |
| Contribution to ARPU (price × share) | | | | | |
| Limit (value metric) | | | | | |
| Step churn | | | | | |

- [ ] ARPU is computed on the mix, not on the top tier;
- [ ] paying-user CAC = CAC / free→paid conversion (freemium);
- [ ] the annual-plan discount is smaller than the churn saved over 12 months;
- [ ] the steps differ by value metric, not by cosmetics;
- [ ] cannibalization between steps has been checked.

## Typical mistakes
- ARPU from the top tier or the arithmetic mean of prices — the mix is inflated and UE "adds up" on paper (PRO-51).
- The CAC of "marketing" instead of the paying-user CAC in freemium: the real cost of a payer is 10–20 times higher.
- A ladder built "from features we didn't mind giving away": the steps don't differ in value → everyone sits on
  basic.
- A 50% annual discount "to attract users" without computing the payback through churn.
- The premium tier as a feature dump: it cannibalizes the core tier.
- Comparing tier ARPU without the shares of the base: the "average tier" of three prices ≠ ARPU.

## Questions that can change the decision
- What share of the base will actually land on each step (and where does that knowledge come from)?
- Won't the free tier eat the paying conversion, and premium eat the core tier?
- Will the annual discount pay off through churn savings at our churn rate?
- How does ARPU change if the mix shifts by 10 p.p. toward the basic tier?

## Related maps
[[M-monetization]], [[M-unit-economics]], [[M-van-westendorp]], [[M-cannibalization]], [[M-traction-model]], [[M-benchmarking]]
