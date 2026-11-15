---
id: M-traction-model
lang: en
title: Traction model (growth model): building, effects, validation
course: skills
sources: ["EN mirror of the RU methodology card M-traction-model (knowledge/methods/traction-model.md); original sources are listed in the RU card"]
stages: [options, strategy, validation, after-decision]
tags: [traction-model, baseline, top-down, bottom-up, cohorts, effects, elasticity, sensitivity, validation, business-case, assumptions, scenarios]
related: [M-market-sizing, M-unit-economics, M-monetization, M-cannibalization, M-benchmarking, M-source-criticism, M-risks, M-trends-scenarios, M-goals-drivers-bets, M-pmf-scaling, M-product-communication, M-model-topdown-bottomup, M-model-validation]
---

# Traction model (growth model): building, effects, validation

## When to apply
"What growth and revenue will the initiative/product bring?", "which hypotheses to bet on?", "how to defend the forecast before management or an investor?", "can the effects of hypotheses be added up?", "check someone else's model for errors". The model is the basis of the business case, prioritization, and tracking fact against plan.

## Essence
A **traction model** (business case, product model, growth model) — a forecast of the incremental effect of launching a product/initiative: `Acquisition channels + Product value (and value growth) + Monetization = Business result`. It answers: due to what, how, and over what horizon the product grows.

**Layers of hypotheses** (a forecast is a "big hypothesis" made of nested assumptions):
1. Market — TAM/SAM/SOM, average order value, competitor shares, legislation → the "top-down check" ([[M-market-sizing]]).
2. Baseline ("if we do nothing") — the dynamics of the funnel, the base, prices, the influence of other products.
3. Growth drivers ("if we act") — the change in funnel/base/metrics from specific initiatives.
4. Monetization — how revenue changes when the drivers are realized (order value, conversion to payment, pricing).
Extension in the monetization skill: 5 — monetization, 6 — revenue forecast, 7 — costs (fixed and driver-based), 8 — efficiency (UE, payback, NPV, IRR, EBITDA). The numbering differs across skills (in traction-modeling monetization = layer 4); in the cards use the scheme "4 layers of hypotheses + the revenue / costs / efficiency blocks".

Two structure types: **growth** (new users, active base, conversion, ARPU, Revenue) and **efficiency** (cost-to-serve, margin, LTV/CAC, operating expenses).

Metrics by lifecycle stage: MVP/Pilot — retention, activation, NPS; Growth — growth rate, CAC, LTV, funnel conversions; Maturity — ARPU, market share, margin; Decline — churn, cost-to-serve, harvest.

### Choosing the approach
| Situation | Approach |
|---|---|
| There is history; the market and seasonality are stable | baseline from time series (e.g., Prophet) + overlaying drivers |
| No data (a new product) | no baseline; top-down scenarios of varying optimism |
| After an MVP, CAC/LTV/retention exist | bottom-up, conservative estimate; cross-check against top-down |
| The increment from a feature/channel/geo is needed | bottom-up with drivers |
| A strategic frame, investors, a "top-down check" | top-down |

**Top-down:** TAM→SAM → market share → dynamics (CAGR, macro factors) → SOM → internal factors. The weak spot — assumptions: an averaged retention, false seasonality (promo peaks taken for seasonality), underestimating cost-to-serve.
**Bottom-up:** modules (PU, ARPPU, retention, conversions), cohorts (do not aggregate), transparent formulas, built-in sensitivity. Limited when data is scarce and for a "vision" years ahead. **Green zone: the bottom-up vs top-down divergence is < 15%.**

### The course's traction model template (Excel)
The reference sheet structure — the basis for the agent's Excel templates:

**Sheet `Assumptions`** — a parameter table: `# (code) | Parameter | Value | Unit | Source / rationale | Confidence (high/medium/low)`. Code groups:
- `M1–M6` market assumptions (top-down): TAM/SAM, SOM share, market AOV, SAM growth %/month, SOM growth pp/month;
- `D1–D9` demand side (funnel): MAU, CR MAU→search, CR search→request, CR request→confirmation, cancellation share, AOV, AOV growth %/month, take rate, MAU growth %/year;
- `S1–S6` supply side: listings, share of active, share of PRO, seller ARPU/month, ARPU growth %/month, base growth %/year;
- `SS1–SS12` seasonal coefficients by month (control row: the sum = 12.0).
Every parameter — with a source and a confidence class; hardcoded values = editable cells (blue cells), the whole model is formulas (see [[M-model-topdown-bottomup]]).

**Sheet `Traction model (Scenario N)`** — rows = metrics, columns = 60 months (5 years); row 2 = the year marker; annual totals via `SUMIF` on the year marker, averages via `AVERAGEIFS`. Row blocks:
1. MARKET (the ceiling): `SAM_GMV_month = TAM × SAM% × AOV / 12`; MoM growth; `SOM_cap = SAM × SOM%` (grows pp/month); the seasonal coefficient from Assumptions.
2. BASELINE Demand side (a driver tree): `MAU_month = MAU × seasonal coeff.` → `×CR_search` → `×CR_request` → `×CR_confirmation` → `Orders paid` → `×(1 − cancellation share) = Orders fulfilled (NSM)` → `×AOV = GMV` → `×Take rate = Revenue: commissions`.
3. BASELINE Supply side: `Active listings = listings × share of active × seasonal coeff.`; `Revenue: VAS = Active listings × ARPU_month` (grows %/month).
4. TOTAL: `Total Revenue = commissions + VAS`; `Revenue YoY growth`; the check `GMV < SOM cap` (TRUE = OK) — bottom-up must not pierce the top-down ceiling.
Each month is computed from the previous one "extended by formulas": `value_N = value_(N−1) × (1 + growth rate)` + the seasonal coefficient; the first month's start is a reference to Assumptions.

**Hypothesis block** (a table in Assumptions or a separate sheet): `Hypothesis | Metric (what we change) | Status (done/wip/not started) | Confidence | Confidence rate | uplift | % rollout | Source / rationale | Verification method | Cannibalization risk | Comment (scenario 1/2, included/excluded)`. In the model the uplift is applied to the row of a specific metric from the launch month: `value = baseline × (1 + uplift × % rollout)`. The scenario switch (hypotheses included/excluded) — the handle for base/optimistic/pessimistic scenarios: base = hypotheses off or with a base uplift, optimistic = high-confidence hypotheses on, pessimistic = only done-hypotheses/reduced uplifts.

**Sheet `Costs assumptions`**: Cost of Sales (marketing per order, logistics per order — variable, goes into UE), Staff cost (FTE × average salary with taxes), Marketing, IT (licenses, IT for new people), other (travel). Placed above revenue it contributes to the P&L; variable costs per order are an input into UE ([[M-unit-economics]]).

**Template hygiene:** not a single hardcoded number in calculated rows (everything is references to Assumptions); the retrospective (fact from dashboards) is separated from the forecast; an auxiliary coefficients row instead of manually filling months.

## Procedure
1. **Purpose and audience of the model** (a decision, financing, tracking); horizon; stage.
2. **Preconditions:** is the market stable? Is seasonality stable? How deep is the history? Are macro factors known (inflation, taxes, rates)? What is the model for? The answers select the approach.
3. **Target metric** decomposed to atomic drivers: `MRR = Customers × ARPU`; then each component is either a driver or decomposes further. The sufficiency criterion: all components are explained by drivers.
4. **Baseline:** history and trends, seasonality, cohort behavior (new cohorts behave differently), the inertia of past launches, inflation, price increases, the influence of neighboring products. No data — three scenarios instead of a baseline.
5. **Driver hypotheses:** for each — the target metric (activation / acquisition / retention / virality), the formulation "change X → result Y", the effect size, a source/benchmark ([[M-benchmarking]]), a confidence class.
6. **Effects:** timing, addition, decay (see below). Cannibalization — as an explicit block ([[M-cannibalization]]).
7. **Monetization and economics:** revenue (`Revenue = ARPPU × PU` or per the model's formula, [[M-monetization]]), costs, UE ([[M-unit-economics]]).
8. **Sensitivity:** for each key driver three scenarios (pessimistic/base/optimistic); show which 2–3 drivers move the result.
9. **Top-down check:** the model ≤ SOM; divergence from top-down; the sum of channels ≤ TAM.
10. **Validation** (below) and a review by an independent person; document the OK/WARNING/ERROR status.

### Adding effects
The effects of hypotheses are usually **not additive**: you may add only hypotheses on different segments/channels without overlap (a promotion on assortment + a performance channel). They overlap — a partner channel and a mailing over the same base ("double counting").
A 4-question checklist: (1) one driver/metric? (2) one calendar period? (3) total growth > 10% (double-digit)? (4) one segment/channel? **If "yes" on at least two — apply a discount:** `Total = Σ Effect_i × k`, `k` usually 0.5–0.8 (the larger the overlap, the lower).
Example (illustration): two hypotheses on conversion in one segment, +6% and +5% → the sum is 11%, "yes" on all 4 questions → the result is 5.5–8.8% at k 0.5–0.8.

### Elasticity and plateau
Effects are almost always nonlinear: they decay (novelty, habituation) or accumulate. Determine the moment of reaching the plateau from benchmarks and the decay of interest; in early periods lay out the effect by weeks, not quarters; sanity-check the ceiling (a shoe buyer is unlikely to buy more than 12 pairs at once). **A hockey stick is a red flag**; it is acceptable only with rapid physical scaling (entry into a new geography).

### Cannibalization in the model (briefly)
`Growth = (Was − Cannibalization) × K_growth` (before hypotheses) or `Growth = (Was × K_growth) × (1 − K_cann)` (after the total effect). The formulas are equivalent if `K_cann = Cannibalization / Was`; fix which base the coefficient refers to. Price as a driver: `Revenue = ARPPU × PU` — evaluate the trade-off of ARPPU growth against a fall in PU. Details — [[M-cannibalization]].

### External factors (an influence map)
Consumers (behavior, demographics) → the number of buyers, deals, order value; laws and economics (rates, taxes) → market size, order value, cost; competitors → share, CAC; technologies (AI agents, etc.) → market size, search, CAC. Tie them to the scenarios from [[M-trends-scenarios]].

### Link to valuation
The model is an input for DCF (discounted future cash flows; sensitive to WACC and terminal value; later rounds, sustainable projects), CCA (multiples of similar companies; depends on the choice of comparables) and Precedent Transactions (multiples of M&A deals; data may be outdated).

## Template / checklist
Sheet structure: `Assumptions` (all assumptions with a source and a class) → `Baseline` → `Drivers` (hypotheses, effects) → `Monetization` → `Costs/Efficiency` → `Scenarios/Sensitivity` → `CHECKS`.

Hypothesis table:
| Hypothesis | Layer | Metric | Effect (min/base/max) | Segment/channel | Period and curve | Overlaps | Source, class |
|---|---|---|---|---|---|---|---|

### Validation: four types of technical errors
1. **Rounding:** round only the final result; the sum of monthly roundings ≠ the annual sum. Check: `=IF(ABS(SUM(B10:M10)-N10)>0.1;1;0)`.
2. **Time anchoring** (the most common): costs at a moment versus revenue over years; point-in-time and cumulative metrics mixed. `MAU(N) = MAU(N−1) + New(N) − Churned(N)` for base balance.
3. **Formula contradictions:** one quantity is computed in two places differently. The SSOT rule (Single Source of Truth): compute in one place, other sheets reference it; named ranges for key cells.
4. **Logical inconsistency:** the balance `Customers_start + New − Churned = Customers_end`; non-negativity; CR1 85% × CR2 90% = 76.5%, but the model shows 80% — a contradiction.

A `CHECKS` tab, binary (0 — ok, 1 — error), a global status `=IF(SUM(Check_Range)>0;"ERROR";"OK")`:
```
Broken cells:      =IF(SUMPRODUCT(--ISERROR('P&L'!A1:Z1000))>0;1;0)
Negatives:         =IF(MIN(B20:M20)<0;1;0)
Percent bounds:    =IF(OR(MAX(B25:M25)>1;MIN(B25:M25)<0);1;0)
Retention monot.:  =IF(SUMPRODUCT(--(B31:M31>B30:M30))>0;1;0)
Not above TAM:     =IF(SUM(B50:B55)>'Assumptions'!$B$5;"TAM Exceeded";"OK")
```
Benchmarks in validation: sanity check, calibration, explaining deviations; a benchmark is a range, compare with the same stage and segment. No data: proxy metrics (a similar region/segment), expert interviews (ranges), an MVP for 1–2 months with a discounted extrapolation, three scenarios.

Review (the author is blind: confirmation bias, anchoring, the curse of knowledge): an analyst (technique), finance (economics), another product manager (logic), a stakeholder (goals). When to validate: before a presentation, after major changes, before planning based on the model, upon handover to a team.

| Red flags | Green flags |
|---|---|
| unrealistic input metrics or inflated dynamics | growth of input metrics is justified by A/B tests, research, trends |
| a period's underperformance carried over without justification | trends and research are discounted |
| no history and trends in the baseline | "market share" is not used as an input metric |
| cannibalization not accounted for | a fall in one input metric is not offset by growth in another |
| no input metrics ("a commitment without inputs") | cannibalization is accounted for expertly or via A/B |
| one strong assumption holds up all outputs | a small change in an assumption does not produce a disproportionate shift in outputs |

Final checklist: drivers are causally linked; technical errors (hardcode, rounding, broken references); assumptions checked against benchmarks; an independent review; a resolution/"traffic light". Output: the model's status, a list of errors by type, the CHECKS tab, a comparison with benchmarks, recommendations, a filled checklist.

## Typical mistakes
| Mistake | Consequence |
|---|---|
| Ignoring cohort decay | ARPU/LTV overstated by 30–40% (a skill estimate, without a source) |
| Aggregated retention without phasing | wrong budget allocation |
| Linear growth | seasonality and jumps missed |
| An error in the monetization model | wrong ARPU/LTV |
| Weak data hygiene | garbage in — garbage out |
| No sensitivity | false confidence |
| Effects added without a discount | inflated total where overlaps exist |
| A driver is a correlation, not a cause; or the team does not influence it | an unrealizable plan |

## Questions that can change the decision
- Is there data for the baseline, how stable and deep is it?
- Which 2–3 assumptions determine >50% of the result, and what is their confidence class?
- Do the hypotheses overlap across segments, channels, periods?
- Is the product launching onto an existing base (then cannibalization is mandatory)?
- What is the model for: a decision, money, or tracking — the acceptable accuracy depends on it.

## Related cards
[[M-market-sizing]], [[M-unit-economics]], [[M-monetization]], [[M-cannibalization]], [[M-benchmarking]], [[M-source-criticism]], [[M-risks]], [[M-trends-scenarios]], [[M-goals-drivers-bets]], [[M-pmf-scaling]], [[M-product-communication]]
