---
id: M-unit-economics
lang: en
title: Unit economics (LTV, CAC, payback)
course: skills
sources: ["EN mirror of the RU methodology card M-unit-economics (knowledge/methods/unit-economics.md); original sources are listed in the RU card"]
stages: [options, strategy, validation, after-decision]
tags: [unit-economics, ltv, cac, payback, margin, cohorts, arppu, gmv, contribution-margin, pnl, freemium]
related: [M-traction-model, M-monetization, M-benchmarking, M-cannibalization, M-market-sizing, M-product-metrics, M-loyalty-metrics, M-model-validation, M-auctions-marketplaces]
---

# Unit economics (LTV, CAC, payback)

## When to apply
"Does the economics converge?", "is it worth scaling acquisition?", "which channel pays back?", "how to check the price/monetization model per unit". This is the entry block of the traction model and the cross-check point for monetization.

## Essence
A **unit** — the basic revenue-generating unit: an order, a customer, a deal, a ride, an event. Unit economics compares revenue and costs for one such unit.

The main rule: `UE = LTV − CAC`; the economics converge when `LTV > CAC`.
The extended form: `UE = (Unit revenue − Unit cost) × Number_of_lifetime_periods − CAC`.
- **LTV** — the money (margin) a customer brings over their entire lifetime. **CAC** = acquisition costs / number acquired (compute per channel).
- **CM (contribution margin)** — the P&L level between revenue and fixed costs: `CM = Revenue − Variable costs`; per unit: **`CM_unit = ARPU − VC_unit`** (variable costs per unit). The share of marketing in revenue (`Marketing / Revenue`) — a controllable share of the "advertising" part of variable costs.
- **GM%** = GM1 / Revenue, where GM1 — profit after variable costs and before fixed ones (first-level margin).
- Positive UE does not prove product profitability (fixed and indirect costs are not counted); **negative UE means the product is definitely loss-making.**
- Compute by **cohorts**: an average over the base hides loss-making new cohorts behind profitable old ones.
- Five levers of improvement: price (ARPU); frequency/retention; variable costs per order; CAC (efficient channels); operational efficiency (call center, automation).

### Cost classification and the place of unit economics in the P&L (sessions 1–2, 8)
Unit economics counts only **variable** costs per unit; fixed, indirect ones and capex are already the financial model and the P&L.
- Two typical P&L structures: (1) `Revenue − COGS = Gross Profit → − Selling − G&A = Operating Profit`; (2) `Revenue − Variable costs = Contribution Margin → − Fixed costs = EBITDA`. Unit economics lives in the second one: **UE = `CM_unit × Lifetime − CAC`**.
- The cost hierarchy: Variable (unit economics) → Direct → Indirect → Administration → Net profit. "Unit economics breaks bad news earliest" — it is the earliest indicator: positive UE is only "the first line held", negative means a guaranteed loss at any scale.
- Attribution rule: a cost arises with every unit — variable (order logistics, acquiring at 1.5–3% of the transaction, packaging, a manager's bonus per deal, SMS); independent of volume — fixed (rent, salaries, depreciation, a software license not tied to users). If a cost depends on scale (cleaners, support, hosting) — a gray zone: the fixed part is embedded into UE as a percentage.
- Mixed cost: `Y = a + bX` (a salary + a % of sales; electricity with a base fee) — split into the fixed part a and the rate b. Stepped cost — a step function (hosting, call center): when crossing a step, account for the jump.
- Business-level summary metrics: the **break-even point** `BEP_units = Fixed / CM_unit`; the **operating leverage** `DOL = CM / EBITDA` (sales grow 10% → profit +DOL×10%); the **margin of safety** `(Sales − BEP) / Sales`; the **volume for a target profit** `(Fixed + Target profit) / CM_unit`.
- Lifecycle phases: at creation UE is not computed (too early), when hypotheses are confirmed it is embedded into the model, at scaling UE is critical (a row in the traction model), at maturity — a prioritization tool. The exception — "investment holidays": consciously operating at a loss with a plan to turn positive (plans B and C are needed).

### Choosing the unit and the "pivots" (session 8)
- Unit by business model: subscription → user; transactions/marketplace → order/deal; retail → order or SKU; frequency business (kick scooters, rentals) → customer; advertising → impression.
- Two "pivots" of one business: **per transaction** (a booking) — a new business, you don't know if the customer will return; **per customer** — a mature base with a clear return pattern ("a business traveler comes 3 times a year — attribute acquisition across 3 trips"). It is useful to compute both: per customer and per product/course/SKU.
- No cohort data — it does NOT follow that one should "count per product" (a causality trap); the choice of unit is determined by the business model, not by data availability.
- CLTV — the customer's value across all the company's products; terminology differs between companies ("catch the meaning, not the letters").

### Seven LTV methods and choosing one
| # | Method | LTV formula | When it fits | Typical products |
|---|---|---|---|---|
| 1 | Classic | `ARPU × Lifetime × GM%` | subscription, stable ARPU and margin, predictable churn | SaaS, streaming, fitness apps |
| 2 | Retention / cohorts | `Σ_t (ARPU_t × GM% × Retention_t)` | cohort data exists, ARPU and margin change by month, uneven retention | mobile games, e-com with unpredictable behavior, EdTech |
| 3 | Via churn | `ARPU × (1/Churn) × GM%` | stable ARPU and GM%, predictable churn, a long retention "tail" (a plateau) | telecom, banks, B2B SaaS with a stable base |
| 4 | Gross margin per order | `GM1_order × Orders_per_user × Lifetime`, `GM1_order = Order revenue − Order variable costs` | a high share of variable costs per order, logistics | e-grocery, food delivery, DTC brands |
| 5 | ARPPU | `ARPPU = Revenue/Payers`; `ARPU = ARPPU × CR_to_payers`; `LTV = ARPU × Lifetime × GM%` | freemium, a small share of payers, marketing payback | Telegram Premium, mobile games with IAP, Duolingo |
| 6 | GMV | `GMV_per_user = GMV/Active`; `Revenue_per_user = GMV_per_user × Commission%`; `GM1_per_user = Revenue_per_user − Variable costs`; `LTV = GM1_per_user × Lifetime` | marketplaces and platforms with a commission | Ozon Marketplace, Airbnb, Uber |
| 7 | AOV × frequency | `ARPU = AOV × F`; `LTV = AOV × F × Lifetime × GM%` | transactional models with repeat purchases; order value and frequency are managed separately | e-commerce, food delivery, retail |

The choice matrix: a subscription with stable ARPU and churn → 1 or 3; cohorts and changing ARPU → 2; heavy logistics → 4; freemium → 5; a GMV commission → 6; repeat purchases → 7. Start with the simple method; complicate only with clear distortions. If two methods give very different LTVs — one of them is inaccurate; find the cause.

### Practical rules from the course (session 8)
- **Lifetime:** the most unstable parameter. Estimation methods: retrospective cohort data (high accuracy), churn (medium), an industry benchmark, expert judgment (low). Rule: **at the start do not set Lifetime above 3 years**, even if "the customer will stay forever". `Lifetime = 1/Churn` is valid only with constant churn.
- **ARPU with multiple plans** — weighted by the shares of the base: `ARPU = Σ(Plan price × Plan share)`, not the arithmetic mean of the plans. UE may differ across geos/cities — compute separately or average explicitly.
- **The median instead of the mean** for a transactional business: an order spread > 3x — the median; > 10x — the median is mandatory. "95 orders of 500 RUB and 5 of 50,000 RUB: an average order of 3,000 RUB is a lie; the typical order is 500 RUB". Cross-margin matters more than the margin on a single item (frequent items with a 2% margin are an acquisition tool; a robot vacuum with an 8% margin goes into the same basket).
- **Freemium:** costs are borne for everyone, revenue comes from payers. `CAC_payer = CAC_acquisition / CR_free→paid` (marketing shows a CAC of 100 RUB; at a 5% conversion the real price of a payer is 2,000 RUB). The minimum share of payers `≈ Cost_per_user / ARPU_payer`; the "tasty metric" — growth in the share of payers. Shifting part of the cost to the buyer (a service fee, as Airbnb does) improves the margin if buyer churn does not grow.
- **Cohort breakeven:** a cohort's cumulative revenue crosses CAC after N months (payback). Before that — an "investment cycle": continue acquiring consciously (a breakeven plan + the money for it) or stop. With positive UE, acquisition can be "paused" and accumulated margin reinvested (bootstrap) — marketing spend does not have to be even.

## Procedure
1. **Define the unit** and the period (a month/an order); fix the units of all quantities.
2. **Choose the LTV method** from the table; write down the reason for the choice and the list of missing data.
3. **Assemble the inputs** (ARPU/AOV/F/churn/retention/GM1) separately by cohorts and channels; every input — with a source and a credibility class ([[M-source-criticism]]).
4. **Compute LTV** with the numbers substituted; Lifetime = `1/Churn` or the sum over the retention curve; cap Lifetime at the model's horizon (as churn → 0 the 1/churn formula gives an unrealistically large value).
5. **Compute CAC** by channels: `CAC_channel = Channel spend / Channel new customers`; also show blended (overall), but make decisions per channel.
6. **UE** = LTV − CAC and `LTV/CAC`; **payback:** `Payback (periods) = CAC / (ARPU_per_period × GM%)`; by cohorts — the minimal T at which `Σ_{t≤T}(ARPU_t × GM% × Retention_t) ≥ CAC`.
7. **Cross-check:** a second LTV method; compare with a benchmark ([[M-benchmarking]]) — take LTV/CAC and payback thresholds only from sources of class A–B; in the skill the threshold is the condition `LTV > CAC`.
8. **Levers:** the sensitivity of UE to order value, margin, retention, CAC (±10% of each) → which lever gives the maximum.
9. **Hand the result** to the traction model ([[M-traction-model]]) and to monetization ([[M-monetization]]).

### Example (illustrative numbers)
Subscription: ARPU 500 RUB/month, churn 5%/month, GM% 70%, CAC 3,000 RUB.
`Lifetime = 1/0.05 = 20 months`; `LTV = 500 × 20 × 0.7 = 7,000 RUB`; `UE = 7,000 − 3,000 = 4,000 RUB`; `LTV/CAC ≈ 2.3`; `Payback = 3,000 / (500 × 0.7) ≈ 8.6 months`. If the real Lifetime is capped at a 12-month horizon — `LTV = 500 × 12 × 0.7 = 4,200`, UE = 1,200: the conclusion is sensitive to the horizon assumption.

### The CPA model (a booking platform for masters, a skill example)
`CPA = AVO × TR × CR_ap` (AVO — the average order value, TR — the take rate, CR_ap — the conversion from booking to payment);
`Revenue = 365 × DAU × OrderRate × CPA` (RUB/year); `clientLTV = LifetimeSessions × OrderRate × CPA`;
`LifetimeSessions ≈ (1 + MRR + MRR² + …) × Stickiness`, MRR — the monthly retention.
Two cross-check points: Revenue vs Expenses (is the business profitable overall) and clientLTV vs CAC (does acquisition pay off). Compute for the cohort acquired by marketing.
Caution: in the unit-economics skill Stickiness is written as MAU/DAU, in monetization-models as DAU/MAU; DAU/MAU is adopted (a 0–1 share), and converting it into sessions requires a multiplier of days and sessions per active day — check the dimensionality (see [[M-monetization]]).

## Template / checklist
Calculation table:
| Parameter | Value | Period/unit | Cohort/channel | Source | Class |
|---|---|---|---|---|---|
| ARPU / AOV / F | | | | | |
| GM1, GM% | | | | | |
| Churn / Retention_t | | | | | |
| Lifetime | | | | | |
| CAC | | | | | |
| LTV, UE, LTV/CAC, Payback | | | | | |

Output artifact: the unit definition → the method and rationale → the LTV calculation → CAC by channels → UE → the cohort breakdown → recommendations on levers.

Automated checks (reproducible):
- Retention and churn ∈ [0; 1]; Retention_t does not grow without reactivation.
- The period units are the same in ARPU, Lifetime, churn, payback.
- GM% is computed after variable costs (not revenue and not net profit).
- The sum over cohorts ≈ the overall result; the difference between methods is explained.
- Acquisition costs and revenue refer to the same cohort and comparable periods.

## Typical mistakes
- An average LTV over the whole base instead of cohorts; mixing old and new cohorts.
- Revenue instead of margin (GM% forgotten); fixed costs counted in UE or, conversely, variable costs entirely ignored (logistics, payment processor fees).
- Mismatched periods: costs at one moment against revenue over years.
- Lifetime = 1/churn with a very small churn → LTV overstated.
- Blended CAC hides loss-making channels.
- The conclusion "UE > 0, therefore profitable" without accounting for fixed costs.
- An LTV/CAC benchmark without a comparability check (see [[M-benchmarking]]).
- The "marketing" CAC instead of the payer's CAC in freemium; a plain average ARPU instead of a plan-weighted one.
- A hardcoded Lifetime > 3 years or 1/churn with negligible churn.
- Mixing Gross and Net margin: salaries, rent, development and marketing itself (it is in CAC) are not part of CM/Gross Margin.

## Questions that can change the decision
- What share of revenue comes from repeat purchases, and what from the first one?
- Do ARPU/margin change with cohort age (then method 2 is needed)?
- Are there significant variable costs per unit (logistics, support, payment acquiring)?
- How sensitive is CAC to scale (a growing budget → a rising price of a customer)?
- Does the new unit cannibalize existing revenue ([[M-cannibalization]])?

## Related cards
[[M-traction-model]], [[M-monetization]], [[M-benchmarking]], [[M-cannibalization]], [[M-market-sizing]], [[M-product-metrics]], [[M-loyalty-metrics]], [[M-model-validation]], [[M-model-topdown-bottomup]]
