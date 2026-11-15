---
id: M-monetization
lang: en
title: Monetization models, value metric and pricing (with an auctions section)
course: skills
sources: ["EN mirror of the RU methodology card M-monetization (knowledge/methods/monetization.md); original sources are listed in the RU card"]
stages: [options, strategy, validation, after-decision]
tags: [monetization, pricing, value-metric, take-rate, cpa, arppu, subscription, auction, vcg, bundling, pricing-tactics, loyalty]
related: [M-unit-economics, M-traction-model, M-business-models, M-cannibalization, M-benchmarking, M-market-sizing, M-auctions-marketplaces, M-loyalty-metrics]
---

# Monetization Models, Value Metric and Pricing

## When to apply
"How do we make money?", "which model to choose and how to compute revenue?", "what does the client pay for and how much?", "does monetization line up with the channel and the economics?", "do we need an auction?". Monetization is a layer of the traction model, not an isolated choice.

## Essence
### The maturity scale of models
Mature models tie payment to value more precisely, give predictable revenue, lower the entry barrier (paying for the result) and raise WTP (willingness to pay).
| Level | Model | What the client pays for | Revenue |
|---|---|---|---|
| 1 | Pay-and-Pray | placement/access, no guarantee of results | `Placements × Placement price` |
| 2 | CPV | a view (attention) | `Σ Views_i × CPV_i` |
| 3 | TRX (commission) | a completed deal | `GMV × Take_Rate`, `GMV = Deals × AVO` |
| 4 | CPA | a target action (application, booking, lead) | `CPA = AOV × TR × CR_action→payment` |
| 5 | Subscription | ongoing access | `Subscribers × ARPU`; `MRR = Payers × Price`; `ARR = MRR × 12` |
| 6 | Auction | a resource at the market price | see the auctions section |

**The "Chairs" case from the course — the same amount three ways:** Pay-and-Pray: 1,000 RUB/month for placement; CPV: 100 views × 10 RUB = 1,000 RUB; TRX: 10 deals × 5,000 RUB × 2% = 1,000 RUB. The amounts are equal, but under TRX the client does not pay if there are no sales — a lower entry barrier, higher loyalty. Technique: compare models on the same client scenario (equivalent revenue → the difference lies in fairness and risk).
Why a transaction is "fairer" — **distributions, not averages** ("it is never an average, it is always a distribution"): Pay-and-Pray gives a wide distribution — a left tail (paid, got few deals → leaves → retention falls) and a right tail (got many deals for a fixed fee → the platform undercharged; because of it the left tail pays "dearly"). CPC narrows the distribution; a transaction almost removes the tails: paid the commission = got the deal. A check: plot the distribution of client outcomes, estimate the share of loss-makers and "underpayers", compute the losses of the left tail (`N_lossmakers × (1 − retention) × ARPU`).

**Four types of value people pay for (where to start):** goods/services (a one-off purchase); access for a period (subscription: ChatGPT, streaming); leads/deals (the seller pays for clients: classifieds, CPA networks); managing money (fintech, insurance, lotteries). The algorithm: what does the client get → which category does it fall into → can it fall into 2+ (normal) → which value is primary for the payer → the base model; secondary values — upsell and "extras". A company's positioning ("we are a bank") does not define the model: a bank in a side-gig service sells leads. The need sits in deals, not in clicks: monetizing intermediate actions should be a deliberate choice.

**Implicit take rate — TR exists in any model, not only in a transaction:** `implicit TR = payment to the platform / the client's revenue for the period`. A master's subscription of 10,000 ₽/month with a revenue of 200,000 ₽/month → TR 5%. An auto-lead-generation benchmark: a commission of ~10% of the dealer's margin (~10% of the price) ≈ 1% of the car's full cost. Course formulas: `CPA = AOV × Take Rate × CR_booking→payment`; `Revenue = 365 × DAU_target × OrderRate × CPA`; `LTV = Sessions_lifetime × OrderRate × CPA`, where `Sessions_lifetime = Σ Retention^n × Stickiness` (the number of sessions per lifetime; a rough estimate — 2–3 sessions/month × lifetime). Sensitivity: CPA and LTV are linear in AOV and Sessions; Sessions (retention) is the main lever. The least reliable input is CR_booking→payment (only MVP data), the most reliable — AOV (a survey of sellers).

**Take rate** (a skill, without a source, grade D — use as a hypothesis and verify): marketplaces 5–20%, fintech 1–3%, ride-hailing 20–30%.

### Value metric
The unit of value the client pays for; it affects WTP, the perceived fairness of the price and scalability.
| Product | Value metric | Model |
|---|---|---|
| Marketplace | deal / GMV | TRX |
| SaaS | user/month | subscription |
| Ad platform | click / impression / action | CPC / CPM / CPA |
| Cloud | resource consumption | pay-per-use |
| Booking bot assistant | a booking with a master | CPA |
Key indicators: `ARPU = Revenue / All_users`; `ARPPU = Revenue / Payers`; `ARPU = ARPPU × CR_free→paid`; Take Rate; CR free→paid.

### Choosing a model by category (the course's decision tree)
```
Does the transaction pass through the platform? (delivery, booking, escrow)
  ├── yes → transactional (Travel with a booking calendar, goods with delivery, credit via a partner)
  └── no → one listing = one item?
        ├── yes → Pay-and-Pray (used cars, secondary real estate)
        └── no (1 listing = many units) → is there a clear action before the deal?
             ├── yes → CPA (new-build/new cars — a call; jobs — an employee's first day)
             └── no → CPC (goods, services: the click self-calibrates the price to demand/geo)
```
Freemium is a risky strategy for small products: "giving away for free — you devalue"; it works for platforms with network effects and ecosystems (the free part leads to a sale elsewhere). Check the funnel: free 100,000 → trial 3,000 → pay 900 — do the 900 payers cover the costs of acquiring the 100,000?

### Pricing: three types and "extras"
| Type | When | Goal |
|---|---|---|
| Sub-optimal (below the optimum) | startup and growth; insurance | a base and room to "raise" the price in a bad scenario (meet the revenue plan) |
| Optimal (the revenue maximum on the "price×demand" curve) | a mature product, #1 on the market | monetization |
| Deterring (above the optimum) | migrating from an old model to a new one; winding a direction down | gently squeezing users out ("we are not switching it off, it is just expensive") |
Raising the price without creating value is a trap ("clever finance people do the math"); price as a driver — only together with new value. Extras on top of the base model: **bundling** (hard/soft/status: a logo in search results + bonuses — billion-scale amounts; an annual fitness card), **companion goods** (an apartment + insurance), **promo mechanics** (an ML willingness-to-pay model: discounts for those for whom it is "a bit pricey"; be careful with the antitrust authority; professionals are rational — promos work on individuals), **prepayment** (money upfront, no missing demand) vs **post-payment** (don't miss sudden demand, but with a debt risk — you need scoring and limits).

### Loyalty programs (lesson 5)
The task is **retention, not acquisition**. Mechanics: cashback (delayed accrual + point expiration = a return loop and higher frequency), points restricted to a spending category (indirect monetization via commission), status tiers, a paid subscription-bundle of the ecosystem. A constraint: cashback cannot exceed the platform's margin (for a low-take-rate classifieds, cashback > 10% = a loss). A cautionary case: subsidizing with cashback as an acquisition "bait" breaks the economics (arbitrage: a purchase with a giant cashback → resale). Measure the loyalty effect in isolation: a test group with points vs a control group without "contamination".

## Procedure
1. **Value:** what the client is really willing to pay for; who pays (the user, the master, the advertiser).
2. **Choice questions:** (a) how easily measurable is the value — obvious → CPA/TRX, subjective → subscription; (b) what risk is the client willing to bear — a low barrier → paying for the result, high trust → a fixed fee; (c) is there competition for a resource → an auction; (d) the product's stage → early means simpler.
3. **Choosing by lifecycle:**
   | Stage | Approach | Metrics |
   |---|---|---|
   | Value validation | free/freemium, a focus on activation | the share of new users in the base, new buyers, deals per buyer |
   | Demand validation | the first monetization — a test of willingness to pay | the share of payers among newcomers, the average order value, retention to a repeat order, GMV |
   | Scale validation | the chosen model, the UE adds up | ROMI, UE, CAC by channel, base growth, LTV, DAU/MAU, GMV |
   | Regular business | margin optimization, a transition to mature models | ROMI, UE, LTV, Revenue/GMV, churn, frequency, cost per deal |
4. **Value metric:** candidates → check that the metric is measurable, grows together with the value received, and is understandable to the client (otherwise WTP falls).
5. **The revenue formula** in variables with units and a period; every input — with a source and a class ([[M-source-criticism]]).
6. **Price:** a WTP range by segments (research — [[M-quant-methods]]); for a price change, check the trade-off `ARPPU × PU` ([[M-cannibalization]]): revenue grows if `(1+Δ ARPPU)(1−Δ PU) > 1`.
7. **Cross-check points:** `Revenue vs Expenses` (infrastructure, AI tokens, the team) and `clientLTV vs CAC` for the cohort acquired by marketing ([[M-unit-economics]]).
8. **Build it into the traction model:** layers 5–8 — monetization (subscription and payer share, add-on services, take rate, AVO), the revenue forecast (a comparison with the market), costs (fixed and driver-based), efficiency (UE, the payback period, NPV, IRR, EBITDA) — see [[M-traction-model]].

### The CPA model (the skill's formulas)
`Revenue = 365 × DAU × OrderRate × CPA` (RUB/year; OrderRate — orders per active user per day); `clientLTV = LifetimeSessions × OrderRate × CPA`; `LifetimeSessions ≈ (1 + MRR_ret + MRR_ret² + …) × Stickiness`, where `MRR_ret` is the monthly retention.
A note: skills disagree (Stickiness = DAU/MAU or MAU/DAU). The accepted definition is DAU/MAU; the series `1 + r + r² + …` gives the expected number of life months `1/(1−r)`, so for sessions add the days in a month and the sessions per active day, and check the dimensionality.

## Auctions (a short section)
**When to introduce — all three conditions:** the resource is limited (places, positions, slots); demand > supply; willingness to pay differs. Not suitable: a single buyer, user intolerance of ads, no real-time infrastructure, too small a market.
**Types:** open (English), closed (sealed-bid), Dutch (the price falls). For several lots: sealed bids → places by descending bids → payment by the rule: **first-price** (pays its own bid), **second-price/GSP** (pays the next bid), **VCG** (pays the marginal value of the place: the losses of the others caused by its presence).
**A VCG example (skill):** places: P1 — 100 clicks, P2 — 60; bids: A 5, B 4, C 3 RUB/click. The optimum: A→P1 (500), B→P2 (240), C without a place; the total is 740 RUB. A's payment = (B on P1 400 + C on P2 180) − 240 = 580 − 240 = **340 RUB.** B's payment (a counterfactual calculation) = (A 500 + C 180) − 500 = **180 RUB.**; C pays 0. For comparison, under GSP: A pays 4×100 = 400, B — 3×60 = 180. VCG makes honest bidding profitable, because the price depends on the impact on others, not on your own bid.
**Metrics:** monetary (Revenue per auction, eCPM/eCPC/eCPA, fill rate, the average bid, win rate); market (liquidity, the bid-ask spread, the number of participants per auction); behavior (advertiser churn, bid frequency, price elasticity, a concentration index).
**Net income** = auction revenue − refunds and fraud − taxes − bonuses and discounts − infrastructure − support and sales.
**Toxic revenue (bad revenue)** — income growth at the cost of deteriorating liquidity, competition and trust. Signs: revenue grows while the number of active participants falls; dependence on 1–2 large buyers; the falling quality of the resource for users; "gaming" the system; growth while the fill rate or bid frequency falls. Protection: market-health metrics on par with Revenue; floor/reserve prices without abuse; a diversity of participants.
**Implementation stages:** demand validation → mechanism choice → an MVP on a limited inventory → calibration (floor, quality score, reserve) → scaling → toxicity monitoring.

## Template / checklist
| Field | To fill in |
|---|---|
| Who pays, for what (value metric) | |
| The model and maturity level | |
| A revenue formula with units/period | |
| Parameters: ARPPU, ARPU, Take Rate, AVO, CR, OrderRate | |
| Cross-check points: Revenue vs Expenses; LTV vs CAC | |
| The product's stage and stage metrics | |
| The impact on the base (price cannibalization) | |
| For an auction: the three conditions, the mechanism, health metrics | |
Exit artifact: a value analysis → a model choice → a formula → key metrics → cross-check points → integration into layers 5–8.

## Typical mistakes
- Choosing a model by fashion without checking whether the value is measurable.
- Computing revenue without accounting for the shrinking paying base at a higher price.
- Not cross-checking LTV against CAC and Revenue against expenses.
- Mixing cohorts (marketing-acquired and organic).
- Confusing ARPU and ARPPU; taking a take rate "from the market" without a source.
- Chasing auction revenue against market-health metrics.

## Questions that can change the decision
- Does the same party pay who receives the value, or a third party?
- Is the value measurable at the moment of payment (a result or access)?
- Is there real competition for the resource (an auction), or is a fixed price enough?
- Is the model compatible with the acquisition channel (viral freemium or direct sales)?
- What share of the base will we lose when changing the model or the price?

## Related cards
[[M-unit-economics]], [[M-traction-model]], [[M-business-models]], [[M-cannibalization]], [[M-benchmarking]], [[M-market-sizing]], [[M-quant-methods]], [[M-source-criticism]], [[M-auctions-marketplaces]], [[M-loyalty-metrics]]
