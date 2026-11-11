---
id: M-monetization
lang: en
title: Monetization models, value metric and pricing (with an auctions section)
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [options, strategy, validation, after-decision]
tags: [monetization, pricing, value-metric, take-rate, cpa, arppu, subscription, auction, vcg, loyalty]
related: [M-unit-economics, M-traction-model, M-business-models, M-cannibalization, M-benchmarking, M-market-sizing, M-auctions-marketplaces, M-loyalty-metrics]
---

# Monetization models, value metric and pricing

## When to apply
"How do we earn money?", "which model should we choose and how do we compute revenue?", "what does the client pay for, and how much?", "does monetization add up with the channel and the unit economics?", "do we need an auction?". Monetization is a layer of the traction model, not an isolated choice.

## Core idea
### Maturity ladder of models
Mature models tie payment to value more precisely, give predictable revenue, lower the entry threshold (you pay for the result) and raise WTP (willingness to pay).
| Lvl | Model | What the client pays for | Revenue |
|---|---|---|---|
| 1 | Pay-and-Pray | placement/access, with no guarantee of a result | `Placements × Placement_price` |
| 2 | CPV | a view (attention) | `Σ Views_i × CPV_i` |
| 3 | TRX (commission) | a completed deal | `GMV × Take_Rate`, `GMV = Deals × AOV` |
| 4 | CPA | a target action (an application, a booking, a lead) | `CPA = AOV × TR × CR_action→payment` |
| 5 | Subscription | continuous access | `Subscribers × ARPU`; `MRR = Payers × Price`; `ARR = MRR × 12` |
| 6 | Auction | a resource at a market price | see the auctions section |

**The course's "Chairs" case, one and the same amount three ways:** Pay-and-Pray: 1,000 ₽/mo for placement; CPV: 100 views × 10 ₽ = 1,000 ₽; TRX: 10 deals × 5,000 ₽ × 2% = 1,000 ₽. The totals are equal, but under TRX the client pays nothing when there are no sales — a lower entry barrier, higher loyalty. Technique: compare models on the same client scenario (equal revenue → the difference lies in fairness and risk).
Why the transaction is "fairer" — **distributions, not the average** ("it never happens on average; there are distributions"): Pay-and-Pray produces a wide distribution — a left tail (paid, got few deals → leaves → retention falls) and a right tail (got many deals for a fixed fee → the platform under-collected; because of that tail, the left tail pays "dearly"). CPC narrows the distribution; a transaction almost eliminates the tails: you paid the commission = you got the deal. Check: build the distribution of client outcomes, estimate the share of losing and "underpaid" clients, compute the left-tail loss (`N_losing × (1 − retention) × ARPU`).

**Four types of paid-for value (a starting point):** goods/services (a one-off purchase); access for a period (subscription: ChatGPT, streaming); leads/deals (the seller pays for customers: classifieds, CPA networks); money management (fintech, insurance, lotteries). Algorithm: what does the client get → which category does it fall into → can it fall into 2+ (that's normal) → which value is primary for the payer → the base model; secondary values become upsell and "gimmicks". A company's positioning ("we are a bank") does not determine the model: a bank inside a side-gig service sells leads. The need lives in deals, not in clicks: monetizing intermediate actions is a deliberate choice.

**Implicit take rate — a TR exists in every model, not only in transactions:** `implicit TR = payment to the platform / client's revenue for the period`. A master's subscription of 10,000 ₽/mo with a revenue of 200,000 ₽/mo → TR 5%. Auto lead-generation benchmark: a commission of ~10% of the dealer's margin (~10% of the price) ≈ 1% of the car's full price. Course formulas: `CPA = AOV × Take Rate × CR_booking→payment`; `Revenue = 365 × DAU_target × OrderRate × CPA`; `LTV = Sessions_lifetime × OrderRate × CPA`, where `Sessions_lifetime = Σ Retention^n × Stickiness` (the number of sessions over a lifetime; a rough estimate — 2–3 sessions/mo × lifetime). Sensitivity: CPA and LTV are linear in AOV and Sessions; Sessions (retention) is the main lever. The least reliable input is CR_booking→payment (MVP data only), the most reliable is AOV (a survey of sellers).

**Take rate** (from the skill, no source, grade D — use as a hypothesis and test it): marketplaces 5–20%, fintech 1–3%, taxi 20–30%.

### Value metric
The unit of value the client pays for; it affects WTP, the perceived fairness of the price and scalability.
| Product | Value metric | Model |
|---|---|---|
| Marketplace | deal / GMV | TRX |
| SaaS | user/month | subscription |
| Ad platform | click / impression / action | CPC / CPM / CPA |
| Cloud | resource consumption | pay-per-use |
| Assistant bot | a booking with a master | CPA |
Key metrics: `ARPU = Revenue / All_users`; `ARPPU = Revenue / Payers`; `ARPU = ARPPU × CR_free→paid`; Take Rate; CR free→paid.

### Choosing a model by category (the course's tree)
```
Does the transaction pass through the platform? (delivery, booking, escrow)
 ├── yes → transactional (Travel with a booking calendar, goods with delivery, loans via a partner)
 └── no → is one listing one item?
      ├── yes → Pay-and-Pray (used cars, secondary real estate)
      └── no (1 listing = many units) → is there a clear action before the deal?
           ├── yes → CPA (new-builds/new cars — a call; jobs — an employee starting work)
           └── no → CPC (goods, services: the click self-calibrates the price to demand/geo)
```
Freemium is a risky strategy for small products: "by giving away for free you devalue"; it works for platforms with network effects and for ecosystems (the free part leads to a sale somewhere else). Check the funnel: free 100,000 → trial 3,000 → 900 pay — do those 900 payers cover the cost of the 100,000?

### Pricing: three types and "gimmicks"
| Type | When | Goal |
|---|---|---|
| Sub-optimal (below the optimum) | a startup and growth; insurance | a base plus headroom to "crank up" the price in a bad scenario (meet the revenue plan) |
| Optimal (maximum revenue on the "price×demand" curve) | a mature product, #1 in the market | monetization |
| Barrier (above the optimum) | migrating from an old model to a new one; winding a direction down | a soft squeeze on users ("we're not disabling it, it's just expensive") |
Raising the price without creating value is a trap ("smart financiers do the counting"); price works as a growth driver only together with new value. Gimmicks layered on top of the base model: **bundling** (hard/soft/status-based: a logo on the search results page + bonuses — billion-scale sums; an annual gym membership), **adjacent products** (apartment + insurance), **promo mechanics** (an ML willingness-to-pay model: discounts for those for whom it's "a bit too expensive"; be careful with the antitrust authority; professionals are rational — promo works on private sellers), **prepayment** (money up front; you cannot afford to miss demand) vs **postpayment** (never miss sudden demand, but there is a debt risk — you need scoring and limits).

### Loyalty programs (session 5)
The goal is **retention, not acquisition**. Mechanics: cashback (delayed crediting + point expiry = a return cycle and higher purchase frequency), points restricted to certain spending categories (indirect monetization via a commission), status tiers, a paid ecosystem-wide subscription bundle. Constraint: cashback cannot exceed the platform's margin (for a classifieds service with a low take rate, cashback > 10% = a loss). A cautionary case: subsidizing cashback as an acquisition "bait" breaks the economics (arbitrage: buying with a giant cashback → reselling). Measure the loyalty effect in isolation: a test group with points vs a control group without any "contamination".

## Procedure
1. **Value:** what the client is really willing to pay for; who pays (the user, the master, the advertiser).
2. **Choice questions:** (a) how easy is it to measure the value — obvious → CPA/TRX, subjective → subscription; (b) what risk is the client willing to carry — a low threshold → pay for the result, high trust → a fixed fee; (c) is there competition for a resource → an auction; (d) the product's stage → earlier is simpler.
3. **Choosing by life cycle:**
   | Stage | Approach | Metrics |
   |---|---|---|
   | Value check | free/freemium, focus on activation | share of newcomers in the base, new buyers, deals per buyer |
   | Demand check | first monetization — testing willingness to pay | share of payers among newcomers, average check, retention into a repeat order, GMV |
   | Scale check | the chosen model, the UE adds up | ROMI, UE, CAC by channel, base growth, LTV, DAU/MAU, GMV |
   | Regular business | margin optimization, moving to mature models | ROMI, UE, LTV, Revenue/GMV, churn, frequency, cost per deal |
4. **Value metric:** candidates → check that the metric is measurable, grows together with the delivered value, and is understandable to the client (otherwise WTP falls).
5. **Revenue formula** in variables with units and a period; every input comes with a source and an evidence class ([[M-source-criticism]]).
6. **Price:** a WTP range per segment (research — [[M-quant-methods]]); for a price change, check the trade-off `ARPPU × PU` ([[M-cannibalization]]): revenue grows if `(1+Δ ARPPU)(1−Δ PU) > 1`.
7. **Reconciliation points:** `Revenue vs Expenses` (infrastructure, AI tokens, the team) and `clientLTV vs CAC` on the cohort acquired by marketing ([[M-unit-economics]]).
8. **Embed it into the traction model:** layers 5–8 — monetization (subscription and payer share, extra services, take rate, AOV), the revenue forecast (compared with the market), costs (fixed and driver-based), efficiency (UE, payback period, NPV, IRR, EBITDA) — see [[M-traction-model]].

### CPA model (the skill's formulas)
`Revenue = 365 × DAU × OrderRate × CPA` (₽/year; OrderRate — orders per active user per day); `clientLTV = LifetimeSessions × OrderRate × CPA`; `LifetimeSessions ≈ (1 + MRR_ret + MRR_ret² + …) × Stickiness`, where `MRR_ret` is monthly retention.
Note: the skills disagree (Stickiness = DAU/MAU or MAU/DAU). The accepted definition is DAU/MAU; the series `1 + r + r² + …` gives the expected number of months of life `1/(1−r)`, so for sessions add the days in a month and the sessions per active day, and check the dimensionality.

## Auctions (short section)
**When to introduce — all three conditions:** the resource is scarce (places, positions, slots); demand > supply; willingness to pay differs. Not suitable: a single buyer, users intolerant of advertising, no real-time infrastructure, a market that is too small.
**Formats:** open (English), closed (sealed-bid), Dutch (the price falls). For several slots: bids in secret → slots assigned by descending bid → payment by the rule: **first-price** (you pay your own bid), **second-price/GSP** (you pay the next bidder's bid), **VCG** (you pay the marginal value of the slot: the losses the others suffer from your presence).
**VCG example (from the skill):** slots: P1 — 100 clicks, P2 — 60; bids: A 5, B 4, C 3 ₽/click. The optimum: A→P1 (500), B→P2 (240), C gets no slot; total 740 ₽. A's payment = (B at P1 400 + C at P2 180) − 240 = 580 − 240 = **340 ₽**. B's payment (card calculation) = (A 500 + C 180) − 500 = **180 ₽**; C pays 0. For comparison, GSP: A pays 4×100 = 400, B pays 3×60 = 180. VCG makes truthful bidding profitable, because the price depends on your impact on the others, not on your own bid.
**Metrics:** monetary (Revenue per auction, eCPM/eCPC/eCPA, fill rate, average bid, win rate); market (liquidity, bid-ask spread, the number of participants per auction); behavior (advertiser churn, bid frequency, price elasticity, a concentration index).
**Net income** = auction revenue − refunds and fraud − taxes − bonuses and discounts − infrastructure − support and sales.
**Toxic revenue (bad revenue)** — revenue growth achieved by degrading liquidity, competition and trust. Signs: revenue grows while the number of active participants falls; dependence on 1–2 large buyers; falling quality of the resource for users; "gaming" the system; growth while fill rate or bid frequency falls. Defense: market-health metrics on par with Revenue; floor/reserve prices without abuse; diversity of participants.
**Rollout stages:** demand validation → mechanism choice → an MVP on limited inventory → calibration (floor, quality score, reserve) → scaling → toxicity monitoring.

## Template / checklist
| Field | Fill in |
|---|---|
| Who pays, for what (value metric) | |
| Model and maturity level | |
| Revenue formula with units/period | |
| Parameters: ARPPU, ARPU, Take Rate, AOV, CR, OrderRate | |
| Reconciliation points: Revenue vs Expenses; LTV vs CAC | |
| Product stage and stage metrics | |
| Impact on the base (price cannibalization) | |
| For an auction: three conditions, mechanism, health metrics | |
Exit artifact: value analysis → model choice → formula → key metrics → reconciliation points → embedding into layers 5–8.

## Typical mistakes
- Choosing a model by fashion without checking that the value is measurable.
- Computing revenue without accounting for the payer base shrinking when the price rises.
- Not reconciling LTV with CAC and Revenue with Expenses.
- Mixing cohorts (marketing-acquired and organic).
- Confusing ARPU with ARPPU; taking a take rate "from the market" without a source.
- Chasing auction revenue against the market-health metrics.

## Questions that can change the decision
- Does the one who pays coincide with the one who receives the value, or is it a third party?
- Is the value measurable at the moment of payment (a result or access)?
- Is there real competition for the resource (an auction), or does a fixed fee suffice?
- Is the model compatible with the acquisition channel (viral freemium or direct sales)?
- What share of the base will we lose when changing the model or the price?

## Related maps
[[M-unit-economics]], [[M-traction-model]], [[M-business-models]], [[M-cannibalization]], [[M-benchmarking]], [[M-market-sizing]], [[M-quant-methods]], [[M-source-criticism]], [[M-auctions-marketplaces]], [[M-loyalty-metrics]]
