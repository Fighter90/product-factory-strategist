---
id: M-unit-economics
lang: en
title: Unit economics (LTV, CAC, payback)
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [options, strategy, validation, after-decision]
tags: [unit-economics, ltv, cac, payback, margin, cohorts, arppu, gmv, contribution-margin, freemium]
related: [M-traction-model, M-monetization, M-benchmarking, M-cannibalization, M-market-sizing, M-product-metrics, M-loyalty-metrics, M-model-validation, M-auctions-marketplaces]
---

# Unit economics (LTV, CAC, payback)

## When to apply
"Does the economics converge?", "Is it worth scaling acquisition?", "Which channel pays back?", "How do we test the price / monetization model per unit?" This is the entry block of the traction model and the cross-check point for monetization.

## Core idea
A **unit** is the basic revenue-bearing unit: an order, a client, a deal, a ride, an event. Unit economics compares the revenue and the costs of one such unit.

The main rule: `UE = LTV − CAC`, the economics converge when `LTV > CAC`.
Expanded form: `UE = (Unit revenue − Unit cost) × Number of lifetime periods − CAC`.
- **LTV** — the money (margin) a client brings over their entire lifetime. **CAC** = acquisition spend / number of clients acquired (always compute per channel).
- **CM (contribution margin)** — the P&L level between revenue and fixed costs: `CM = Revenue − Variable costs`; per unit: **`CM_unit = ARPU − unit VC`** (variable costs per unit). The share of marketing in revenue (`Marketing / Revenue`) is the controlled "advertising" slice of variable costs.
- **GM%** = GM1 / Revenue, where GM1 is profit after variable costs and before fixed costs (first-level margin).
- Positive UE does not prove that the product is profitable (fixed and indirect costs are not counted); **negative UE means the product is definitely loss-making.**
- Compute by **cohorts**: an average over the whole base hides loss-making new cohorts behind profitable old ones.
- Five levers of improvement: price (ARPU); frequency/retention; variable costs per order; CAC (efficient channels); operational efficiency (call center, automation).

### Cost classification and the place of unit economics in the P&L (sessions 1–2, 8)
Unit economics counts only **variable** costs per unit; fixed, indirect costs and capex already belong to the financial model and the P&L.
- Two typical P&L structures: (1) `Revenue − COGS = Gross Profit → − Selling − G&A = Operating Profit`; (2) `Revenue − Variable costs = Contribution Margin → − Fixed costs = EBITDA`. Unit economics lives in the second one: **UE = `CM_unit × Lifetime − CAC`**.
- Cost hierarchy: Variable (unit economics) → Direct → Indirect → Administration → Net profit. "Unit economics breaks long before trouble" — it is the earliest indicator: positive UE only means "the first line of defense has held", negative UE means a guaranteed loss at any scale.
- Attribution rule: a cost that arises with every unit is variable (order logistics, acquiring at 1.5–3% of a transaction, packaging, a manager's per-deal bonus, SMS); a cost that does not depend on volume is fixed (rent, salaries, depreciation, a software license not tied to users). If a cost scales with volume (cleaners, support, hosting) it is a gray zone: the fixed share of such a cost is booked into unit economics as a percentage.
- Mixed cost: `Y = a + bX` (salary + % of sales; electricity with a base fee) — split it into the fixed part a and the rate b. Stepped cost — a step function (hosting, call center): when crossing a step, account for the jump.
- Business-level summary metrics: **breakeven point** `BEP_units = Fixed / CM_unit`; **operating leverage** `DOL = CM / EBITDA` (sales +10% → profit +DOL×10%); **safety margin** `(Sales − BEP) / Sales`; **volume for a target profit** `(Fixed + Target profit) / CM_unit`.
- Lifecycle phases: at creation UE is not computed (too early), once hypotheses are validated it is booked into the model, at scaling UE is critical (a line in the traction model), at maturity it is a prioritization tool. Exception — "investment holidays": consciously operating at a loss with a plan to become profitable (plans B and C are required).

### Choosing the unit and the two "flips" (session 8)
- Unit by business model: subscription → user; transactions/marketplace → order/deal; retail → order or SKU; high-frequency business (scooters, rentals) → client; advertising → impression.
- Two "flips" of the same business: **per transaction** (booking) — a new business where you don't know yet whether the client will return; **per client** — a mature base with a well-understood return pattern ("a business traveler comes 3 times a year — spread acquisition over 3 trips"). It is useful to compute both: per client and per product/course/SKU.
- Cohort data is missing — it does NOT follow that you should "count per product" (a causality trap); the choice of unit is determined by the business model, not by data availability.
- CLTV — the value of a client across all of the company's products; terminology differs between companies ("catch the meaning, not the letters").

### Seven LTV methods and choosing one
| # | Method | LTV formula | When it fits | Typical products |
|---|---|---|---|---|
| 1 | Classic | `ARPU × Lifetime × GM%` | subscription, stable ARPU and margin, predictable churn | SaaS, streaming, fitness apps |
| 2 | Retention / cohorts | `Σ_t (ARPU_t × GM% × Retention_t)` | cohort data available, ARPU and margin change from month to month, uneven retention | mobile games, e-com with unpredictable behavior, EdTech |
| 3 | Via churn | `ARPU × (1/Churn) × GM%` | stable ARPU and GM%, predictable churn, a long retention "tail" (a plateau) | telecom, banks, B2B SaaS with a stable base |
| 4 | Gross margin per order | `GM1_order × Orders_per_user × Lifetime`, `GM1_order = Order revenue − Order variable costs` | a high share of variable costs per order, logistics | e-grocery, food delivery, DTC brands |
| 5 | ARPPU | `ARPPU = Revenue/Paying users`; `ARPU = ARPPU × CR_to_paying`; `LTV = ARPU × Lifetime × GM%` | freemium, a small share of paying users, marketing payback | Telegram Premium, mobile games with IAP, Duolingo |
| 6 | GMV | `GMV_per_user = GMV/Active users`; `Revenue_per_user = GMV_per_user × Commission%`; `GM1_per_user = Revenue_per_user − Variable costs`; `LTV = GM1_per_user × Lifetime` | marketplaces and platforms earning a commission | Ozon Marketplace, Airbnb, Uber |
| 7 | AOV × frequency | `ARPU = AOV × F`; `LTV = AOV × F × Lifetime × GM%` | transactional models with repeat purchases; check size and frequency are managed separately | e-commerce, food delivery, retail |

Choice matrix: a subscription with stable ARPU and churn → 1 or 3; cohorts and a changing ARPU → 2; heavy logistics → 4; freemium → 5; a commission on GMV → 6; repeat purchases → 7. Start with the simple method and add complexity only when there are clear distortions. If two methods give a very different LTV — one of them is inaccurate; find the cause.

### Practical rules from the course (session 8)
- **Lifetime:** the most unstable parameter. Estimation methods: retrospective cohort data (high accuracy), churn (medium), an industry benchmark, expert judgment (low). Rule: **at the start, do not set Lifetime above 3 years**, even if "the client will stay forever". `Lifetime = 1/Churn` is valid only with constant churn.
- **ARPU across tariffs** — weighted by the shares of the base: `ARPU = Σ(Tariff price × Tariff share)`, not the arithmetic mean of the tariffs. UE may differ by geo/city — compute separately or average explicitly.
- **Median instead of mean** for transactional businesses: if the spread of check sizes is > 3×, use the median; > 10× — the median is mandatory. "95 orders of 500 ₽ and 5 of 50 000 ₽: an average check of 3 000 ₽ is a lie — the typical order is 500 ₽". Cross-margin matters more than the margin on a single item (frequent items with a 2% margin are an acquisition tool; a robot vacuum with an 8% margin goes into the same basket).
- **Freemium:** costs are borne by everyone, revenue comes from payers. `Payer CAC = Acquisition CAC / CR_free→paid` (marketing shows a CAC of 100 ₽; at a 5% conversion the real price of a payer is 2 000 ₽). The minimum share of paying users `≈ Cost per user / Payer ARPU`; the "tasty metric" is growth in the share of paying users. Shifting part of the cost onto the buyer (a service fee, as at Airbnb) improves margin as long as buyer churn does not grow.
- **Cohort breakeven:** a cohort's cumulative revenue crosses CAC after N months (payback). Until then — an "investment cycle": either keep acquiring consciously (a breakeven plan plus the money to fund it) or stop. With positive UE, acquisition can be "paused" and the accumulated margin reinvested (bootstrap) — marketing spend does not have to be spread evenly over time.

## Procedure
1. **Define the unit** and the period (month/order); fix the units of all quantities.
2. **Choose the LTV method** from the table; record the reason for the choice and the list of missing data.
3. **Gather the inputs** (ARPU/AOV/F/churn/retention/GM1) separately by cohort and channel; each input carries a source and an evidence class ([[M-source-criticism]]).
4. **Compute LTV** with the numbers substituted; Lifetime = `1/Churn` or the sum over the retention curve; cap Lifetime at the model horizon (as churn → 0 the 1/churn formula gives an unrealistically large value).
5. **Compute CAC per channel:** `CAC_channel = Channel spend / Channel new clients`; show the blended figure too, but make decisions per channel.
6. **UE** = LTV − CAC and `LTV/CAC`; **payback:** `Payback (periods) = CAC / (ARPU_per_period × GM%)`; per cohort — the minimal T at which `Σ_{t≤T}(ARPU_t × GM% × Retention_t) ≥ CAC`.
7. **Cross-check:** a second LTV method; compare against a benchmark ([[M-benchmarking]]) — take LTV/CAC and payback thresholds only from class A–B sources; in this skill the threshold is the condition `LTV > CAC`.
8. **Levers:** the sensitivity of UE to check size, margin, retention, CAC (±10% of each) → which lever yields the maximum.
9. **Pass the result** to the traction model ([[M-traction-model]]) and to monetization ([[M-monetization]]).

### Example (illustrative numbers)
A subscription: ARPU 500 RUB/mo, churn 5%/mo, GM% 70%, CAC 3 000 RUB.
`Lifetime = 1/0.05 = 20 mo`; `LTV = 500 × 20 × 0.7 = 7 000 RUB`; `UE = 7 000 − 3 000 = 4 000 RUB`; `LTV/CAC ≈ 2.3`; `Payback = 3 000 / (500 × 0.7) ≈ 8.6 mo`. If the real Lifetime is capped at a 12-month horizon — `LTV = 500 × 12 × 0.7 = 4 200`, UE = 1 200: the conclusion is sensitive to the horizon assumption.

### CPA model (a booking platform for masters, the skill's example)
`CPA = AVO × TR × CR_ap` (AVO — average order value, TR — take rate, CR_ap — conversion from a booking to payment);
`Revenue = 365 × DAU × OrderRate × CPA` (RUB/year); `clientLTV = LifetimeSessions × OrderRate × CPA`;
`LifetimeSessions ≈ (1 + MRR + MRR² + …) × Stickiness`, MRR — monthly retention.
Two cross-check points: Revenue vs Expenses (is the business profitable as a whole) and clientLTV vs CAC (does acquisition pay back). Compute for the cohort acquired by marketing.
Caution: in the unit-economics skill Stickiness is written as MAU/DAU, in monetization-models as DAU/MAU; the accepted value is DAU/MAU (a 0–1 share), and converting it into sessions requires a multiplier of days and sessions per active day — check the dimensions (see [[M-monetization]]).

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

Exit artifact: the unit definition → method and rationale → LTV calculation → CAC per channel → UE → cohort breakdown → recommendations on levers.

Automated checks (reproducible):
- Retention and churn ∈ [0; 1]; Retention_t does not grow without reactivation.
- The period units are the same across ARPU, Lifetime, churn and payback.
- GM% is computed after variable costs (not revenue and not net profit).
- The sum over cohorts ≈ the overall result; the difference between the methods is explained.
- Acquisition costs and revenue belong to the same cohort and comparable periods.

## Typical mistakes
- An average LTV over the whole base instead of cohort LTV; old and new cohorts mixed.
- Revenue instead of margin (GM% forgotten); fixed costs counted in UE — or, on the contrary, variable costs (logistics, payment acquiring) ignored entirely.
- Mismatched periods: costs from a single moment set against revenue accumulated over years.
- Lifetime = 1/churn at a very low churn → LTV is overstated.
- Blended CAC hides loss-making channels.
- The conclusion "UE > 0, therefore we are profitable" without fixed costs.
- An LTV/CAC benchmark without a comparability check (see [[M-benchmarking]]).
- The "marketing" CAC instead of the payer CAC in freemium; a plain average ARPU instead of the tariff-weighted one.
- A hardcoded Lifetime > 3 years, or 1/churn with negligible churn.
- Mixing up Gross and Net margin: salaries, rent, development and marketing itself are not part of CM/Gross Margin (marketing sits in CAC).

## Questions that can change the decision
- What share of revenue comes from repeat purchases, and what share from the first one?
- Does ARPU/margin change with the age of the cohort (then method 2 is needed)?
- Are there significant variable costs per unit (logistics, support, payment acquiring)?
- How sensitive is CAC to scale (a larger budget → a higher price of a client)?
- Does the new unit cannibalize the revenue of existing ones ([[M-cannibalization]])?

## Related maps
[[M-traction-model]], [[M-monetization]], [[M-benchmarking]], [[M-cannibalization]], [[M-market-sizing]], [[M-product-metrics]], [[M-loyalty-metrics]], [[M-model-validation]], [[M-model-topdown-bottomup]]
