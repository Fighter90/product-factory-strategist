---
id: M-traction-model
lang: en
title: Traction model (growth model): building, effects, validation
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [options, strategy, validation, after-decision]
tags: [traction-model, growth-model, baseline, top-down, bottom-up, cohorts, elasticity, sensitivity, validation, business-case]
related: [M-market-sizing, M-unit-economics, M-monetization, M-cannibalization, M-benchmarking, M-source-criticism, M-risks, M-trends-scenarios, M-goals-drivers-bets, M-pmf-scaling, M-product-communication, M-model-topdown-bottomup, M-model-validation]
---

# Traction model (growth model): building, effects, validation

## When to apply
"What growth and revenue will this initiative/product deliver?", "which hypotheses should we bet on?", "how do we defend the forecast to leadership or an investor?", "can hypothesis effects be added together?", "check someone else's model for mistakes." The model is the backbone of the business case, of prioritization, and of tracking actuals against plan.

## Core idea
A **traction model** (business case, product model, growth model) is a forecast of the incremental effect of launching a product/initiative: `Acquisition channels + Product value (and value growth) + Monetization = Business result`. It answers: what the product grows by, how, and on what horizon.

**Hypothesis layers** (a forecast is one "big hypothesis" made of nested assumptions):
1. Market — TAM/SAM/SOM, average check, competitor shares, legislation → the "top-down check" ([[M-market-sizing]]).
2. Baseline ("if we do nothing") — dynamics of the funnel, the base, prices, and the influence of other products.
3. Growth drivers ("if we act") — changes in the funnel/base/metrics from specific initiatives.
4. Monetization — how income changes when the drivers land (check, conversion to payment, pricing).
Extension in the monetization skill: 5 — monetization, 6 — revenue forecast, 7 — costs (fixed and driver-based), 8 — efficiency (UE, payback, NPV, IRR, EBITDA). The numbering differs between skills (in traction-modeling monetization = layer 4); in the maps use the scheme "4 hypothesis layers + revenue / costs / efficiency blocks".

Two structure types: **growth** (new users, active base, conversion, ARPU, revenue) and **efficiency** (cost-to-serve, margin, LTV/CAC, operating expenses).

Metrics by life-cycle stage: MVP/Pilot — retention, activation, NPS; Growth — growth rate, CAC, LTV, funnel conversions; Maturity — ARPU, market share, margin; Decline — churn, cost-to-serve, harvest.

### Choosing the approach
| Situation | Approach |
|---|---|
| History exists, market and seasonality are stable | baseline from time series (e.g. Prophet) + drivers overlaid |
| No data (new product) | no baseline; top-down scenarios of varying optimism |
| After MVP, with CAC/LTV/retention | bottom-up, conservative estimate; cross-checked against top-down |
| An increment from a feature/channel/geo is needed | bottom-up with drivers |
| Strategic frame, investors, a "top-down check" | top-down |

**Top-down:** TAM→SAM → market share → dynamics (CAGR, macro factors) → SOM → internal factors. The weak spot is assumptions: averaged retention, false seasonality (promo peaks taken for seasonality), underestimated cost-to-serve.
**Bottom-up:** modules (PU, ARPPU, retention, conversions), cohorts (never aggregated), transparent formulas, built-in sensitivity. Limited when data is scarce and for "vision" years ahead. **Green zone: bottom-up vs top-down divergence < 15%.**

### The course traction-model template (Excel)
The reference sheet structure — the basis for the agent's Excel templates:

**Sheet `Assumptions`** — a parameter table: `# (code) | Parameter | Value | Unit | Source / justification | Confidence (high/medium/low)`. Code groups:
- `M1–M6` market assumptions (top-down): TAM/SAM, SOM share, market AOV, SAM growth %/month, SOM growth pp/month;
- `D1–D9` demand side (funnel): MAU, CR MAU→search, CR search→query, CR query→confirmation, cancel share, AOV, AOV growth %/month, take rate, MAU growth %/year;
- `S1–S6` supply side: listings, active share, PRO share, seller ARPU/month, ARPU growth %/month, base growth %/year;
- `SS1–SS12` seasonal coefficients by month (control row: sum = 12.0).
Every parameter carries a source and a confidence class; hardcoded values = editable cells (blue cells), the whole model is formulas (see [[M-model-topdown-bottomup]]).

**Sheet `Traction model (Scenario N)`** — rows = metrics, columns = 60 months (5 years); row 2 = year marker; annual totals via `SUMIF` on the year marker, averages via `AVERAGEIFS`. Row blocks:
1. MARKET (the ceiling): `SAM_GMV_month = TAM × SAM% × AOV / 12`; MoM growth; `SOM_cap = SAM × SOM%` (grows pp/month); the seasonal coefficient from Assumptions.
2. BASELINE demand side (driver tree): `MAU_month = MAU × seasonal coeff.` → `×CR_search` → `×CR_query` → `×CR_confirmation` → `Orders paid` → `×(1 − cancel share) = Orders fulfilled (NSM)` → `×AOV = GMV` → `×Take rate = Revenue: commissions`.
3. BASELINE supply side: `Active listings = listings × active share × seasonal coeff.`; `Revenue: VAS = Active listings × ARPU_month` (growing %/month).
4. TOTAL: `Total Revenue = commissions + VAS`; `Revenue YoY growth`; the check `GMV < SOM cap` (TRUE = OK) — bottom-up must not pierce the top-down ceiling.
Every month is computed from the previous one, "extended by formulas": `value_N = value_(N−1) × (1 + growth rate)` + the seasonal coefficient; the first month starts from a reference to Assumptions.

**Hypothesis block** (a table in Assumptions or a separate sheet): `Hypothesis | Metric (what we change) | Status (done/wip/not started) | Confidence | Confidence rate | uplift | rollout % | Source / justification | Check method | Cannibalization risk | Comment (scenario 1/2, included/excluded)`. In the model, uplift is applied to the row of the specific metric starting from the launch month: `value = baseline × (1 + uplift × rollout %)`. The scenario switch (hypotheses included/excluded) is the handle for base/optimistic/pessimistic scenarios: base = hypotheses off or with the baseline uplift, optimistic = high-confidence hypotheses on, pessimistic = done hypotheses only / lowered uplift.

**Sheet `Costs assumptions`**: Cost of Sales (marketing spend per order, logistics per order — variable, goes into unit economics), Staff cost (FTE × average salary with taxes), Marketing, IT (licenses, IT for new hires), other (travel). Sitting above revenue, this contributes to P&L; variable costs per order are an input to UE ([[M-unit-economics]]).

**Template hygiene:** not a single hardcoded number in calculated rows (everything references Assumptions); the retrospective (actuals from dashboards) is kept separate from the forecast; a helper row of coefficients instead of manually filling months.

## Procedure
1. **Purpose and audience of the model** (a decision, funding, tracking); horizon; stage.
2. **Preconditions:** is the market stable? is the seasonality sustainable? how deep is the history? are macro factors known (inflation, taxes, rates)? What is the model for? The answers pick the approach.
3. **Target metric** decomposed into atomic drivers: `MRR = Clients × ARPU`, and onward each component is either a driver or decomposes further. Sufficiency criterion: every component is explained by drivers.
4. **Baseline:** history and trends, seasonality, cohort behavior (new cohorts behave differently), inertia of past launches, inflation, price rises, the influence of neighboring products. No data — three scenarios instead of a baseline.
5. **Driver hypotheses:** for each — the target metric (activation / acquisition / retention / virality), the wording "changing X → result Y", the effect size, a source/benchmark ([[M-benchmarking]]), a confidence class.
6. **Effects:** timing, addition, decay (see below). Cannibalization as an explicit block ([[M-cannibalization]]).
7. **Monetization and economics:** revenue (`Revenue = ARPPU × PU` or the model's formula, [[M-monetization]]), costs, UE ([[M-unit-economics]]).
8. **Sensitivity:** for every key driver, three scenarios (pessimistic/base/optimistic); show which 2–3 drivers move the result.
9. **Top-down cross-check:** the model ≤ SOM; the divergence from top-down; the sum of channels ≤ TAM.
10. **Validation** (below) and review by an independent person; document the OK/WARNING/ERROR status.

### Adding effects
Hypothesis effects are usually **not additive**: only hypotheses on different segments/channels with no overlap can be summed (an assortment promo + a performance channel). Overlapping means a partner channel and a mailing to the same base ("double counting").
A 4-question checklist: (1) one driver/metric? (2) one calendar period? (3) combined growth > 10% (double-digit)? (4) one segment/channel? **If "yes" on at least two — apply a discount:** `Total = Σ Effect_i × k`, `k` usually 0.5–0.8 (the larger the overlap, the lower it is).
Example (illustration): two hypotheses on conversion in the same segment, +6% and +5% → 11% summed, "yes" on all 4 questions → a net 5.5–8.8% at k 0.5–0.8.

### Elasticity and plateau
Effects are almost always nonlinear: they decay (novelty, habituation) or accumulate. Set the moment of reaching the plateau from benchmarks and interest decay; lay out the first periods by weeks, not quarters; sanity-check the ceiling (a shoe buyer is unlikely to buy more than 12 pairs at once). **A hockey stick is a red flag**; it is acceptable only with rapid physical scaling (entering a new geography).

### Cannibalization in the model (short)
`Growth = (Was − Cannibalization) × K_growth` (before hypotheses) or `Growth = (Was × K_growth) × (1 − K_cann)` (after the total effect). The formulas are equivalent if `K_cann = Cannibalization / Was`; fix which base the coefficient refers to. Price as a driver: `Revenue = ARPPU × PU` — weigh the growth of ARPPU against the fall in PU. Details — [[M-cannibalization]].

### External factors (influence map)
Consumers (behavior, demography) → the number of buyers, deals, check; laws and the economy (rate, taxes) → market size, check, cost; competitors → share, CAC; technology (AI agents and others) → market size, search, CAC. Tie them to the scenarios from [[M-trends-scenarios]].

### Link to valuation
The model is an input for DCF (discounted future cash flows; sensitive to WACC and terminal value; later rounds, sustainable projects), CCA (multiples of comparable companies; depends on the choice of peers) and Precedent Transactions (multiples of M&A deals; the data may be outdated).

## Template / checklist
Sheet structure: `Assumptions` (all assumptions with a source and a class) → `Baseline` → `Drivers` (hypotheses, effects) → `Monetization` → `Costs/Efficiency` → `Scenarios/Sensitivity` → `CHECKS`.

Hypothesis table:
| Hypothesis | Layer | Metric | Effect (min/base/max) | Segment/channel | Period and curve | Overlaps | Source, class |
|---|---|---|---|---|---|---|---|

### Validation: four types of technical mistakes
1. **Rounding:** round only the final figure; the sum of monthly roundings ≠ the annual total. Check: `=IF(ABS(SUM(B10:M10)-N10)>0.1;1;0)`.
2. **Time anchoring** (the most common): momentary costs against income earned over years; point and cumulative metrics mixed. `MAU(N) = MAU(N−1) + New(N) − Churned(N)` keeps the base in balance.
3. **Formula contradictions:** the same quantity is computed in two places in different ways. The SSOT rule (Single Source of Truth): compute it in one place, and all other sheets reference it; named ranges for the key cells.
4. **Logical inconsistency:** the balance `Clients_start + New − Gone = Clients_end`; non-negativity; CR1 85% × CR2 90% = 76.5%, but the model shows 80% — a contradiction.

A `CHECKS` tab, binary (0 — ok, 1 — error), global status `=IF(SUM(Check_Range)>0;"ERROR";"OK")`:
```
Broken cells:      =IF(SUMPRODUCT(--ISERROR('P&L'!A1:Z1000))>0;1;0)
Negatives:         =IF(MIN(B20:M20)<0;1;0)
Percentage bounds: =IF(OR(MAX(B25:M25)>1;MIN(B25:M25)<0);1;0)
Retention monot.:  =IF(SUMPRODUCT(--(B31:M31>B30:M30))>0;1;0)
Not above TAM:     =IF(SUM(B50:B55)>'Assumptions'!$B$5;"TAM Exceeded";"OK")
```
Benchmarks in validation: a sanity check, calibration, explaining deviations; a benchmark is a range, and it should be compared with the same stage and segment. No data: proxy metrics (a similar region/segment), expert interviews (ranges), a 1–2 month MVP with discounted extrapolation, three scenarios.

Review (the author is blind: confirmation bias, anchoring, the curse of knowledge): an analyst (technique), finance (economics), another product manager (logic), a stakeholder (goals). When to validate: before a presentation, after major changes, before planning based on the model, when handing the model over to a team.

| Red flags | Green flags |
|---|---|
| unrealistic input metrics or inflated dynamics | growth of input metrics is backed by A/B tests, research, trends |
| an unmet period carried over without justification | trends and research are discounted |
| no history and trends in the baseline | "market share" is not used as an input metric |
| cannibalization is not accounted for | a fall in one input metric is not covered by growth in another |
| no input metrics ("a commit without inputs") | cannibalization is accounted for expertly or via an A/B |
| one strong assumption holds up all the outputs | a small change in an assumption does not shift the outputs disproportionately |

The final checklist: drivers are causally linked; technical mistakes (hardcoding, rounding, broken references); assumptions checked against benchmarks; independent review; a resolution/"traffic light". The output: the model status, a list of mistakes by type, the CHECKS tab, a comparison with benchmarks, recommendations, the completed checklist.

## Typical mistakes
| Mistake | Consequence |
|---|---|
| Ignoring cohort decay | ARPU/LTV overstated by 30–40% (the skill's estimate, no source) |
| Aggregate retention without phasing | wrong budget allocation |
| Linear growth | seasonality and jumps missed |
| An error in the monetization model | wrong ARPU/LTV |
| Weak data hygiene | garbage in — garbage out |
| No sensitivity | false confidence |
| Effects summed without a discount | an inflated total where effects overlap |
| A driver that is a correlation, not a cause — or one the team does not influence | an unrealizable plan |

## Questions that can change the decision
- Is there data for a baseline, and how stable and deep is it?
- Which 2–3 assumptions determine >50% of the result, and what confidence class do they have?
- Do the hypotheses overlap by segments, channels, periods?
- Is the product launching onto an existing base (then cannibalization is mandatory)?
- What is the model for: a decision, money, or tracking — the acceptable precision depends on that.

## Related maps
[[M-market-sizing]], [[M-unit-economics]], [[M-monetization]], [[M-cannibalization]], [[M-benchmarking]], [[M-source-criticism]], [[M-risks]], [[M-trends-scenarios]], [[M-goals-drivers-bets]], [[M-pmf-scaling]], [[M-product-communication]]
