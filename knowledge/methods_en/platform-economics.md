---
id: M-platform-economics
lang: en
title: Platform economics: TCO, effects, financial model, metrics
course: strategy
sources: ["EN mirror of the RU methodology card M-platform-economics (knowledge/methods/platform-economics.md); original sources are listed in the RU card"]
stages: [options, strategy, validation]
tags: [platforms, tco, financial-model, dcf, irr, npv, break-even, scenarios, increment, adoption, liquidity]
related: [M-platforms-types-criteria, M-platform-case-concept, M-platform-risks-rollout, M-unit-economics, M-market-sizing, M-success-metrics, M-source-criticism]
---

# Platform Economics: TCO, Effects, Financial Model, Metrics

## When to apply
"Does the platform's economics add up and how do we prove it to the committee?", "what to compare the platform against and how to compute the effect?", "when does it pay back and at what number of onboardings?", "which assumptions are critical and how do we verify them?". Taken after the concept ([[M-platform-case-concept]]); linked to unit economics ([[M-unit-economics]]).

## Essence
Platform economics = three parts: **TCO** (the costs of development, support and integrations) + **the business effect** (what becomes faster, bigger, better — translated into money) + **a comparison with alternatives** (As Is without the platform vs To Be with it). A direct "business effect of the platform as a product" is hard to defend — the usual route is a comparison of the TCO of the platform and the alternatives.

### The cost structure
| Local solutions | Platform |
|---|---|
| Development in every team | The core and the launch |
| Repeated rework | Client integrations |
| Support and infrastructure | Migration and launches on the clients' side; infrastructure |

Costs split into **one-off** (building the core, architectural changes, migration and transition tooling) and **recurring** (the platform team, client support, documentation). For an external market add CAPEX (material assets, e.g., servers) with depreciation (non-cash, not part of cash costs) and OPEX (operations). The unit of labor costs is an FTE-month at the organization's average employee cost; the full financial model is refined by finance.

### The six sources of effect
1. Additional revenue or growth of other user metrics. 2. Infrastructure savings. 3. Faster launches (TTM). 4. Lower run costs. 5. Development savings (teams and solutions never built). 6. Prevented losses.

### Key formulas
- **The basic comparison:** `ΔFCF = FCF_ToBe − FCF_AsIs` by year; `Cumulative ΔFCF = Σ ΔFCF`; **break-even** — the first year where the cumulative ΔFCF ≥ 0.
- **The payback threshold (break-even by the number of clients):** `Number of launches = (Build + Run over the horizon) / Savings per launch`, where savings per launch = (local development + local support − platform onboarding).
- **ROI** = (benefit − costs) / costs; **IRR** — the discount rate at which the NPV of the ΔFCF stream = 0 (more important than ROI for the committee).
- **WACC** — the weighted average cost of capital; higher risk → a higher rate. **Discounting:** `PV = ΔFCF_t / (1+WACC)^t`.
- **Terminal value:** `TV_T = FCF_T_sustainable / WACC` (only the sustainable annual FCF after the horizon); `NPV = Σ PV ΔFCF + PV TV`.
- **The incremental effect (the CRM type):** `Audience → Coverage (the share reached) → Conversion (the share performing the target action) → Increment (the difference vs control, an A/B) → Value (increment × the value of the action → revenue, EBITDA, FCF)`. The increment is computed on **company revenue**, not on GMV and not directly on the take rate; revenue ≠ margin (an increment in sales volume at a tiny margin is worth almost nothing in money).
- **The TTM effect:** `Savings/effect = (local launch time − launch time with the platform) × the monthly marginal effect × the number of launches`.
- **For ecosystem (market) platforms:** `Platform revenue = GMV × take rate`; the take rate can be differentiated by side; the deficient side is subsidized (free/negative price), and you monetize the side whose value grows with liquidity; unit economics are computed by side and by cohort ([[M-unit-economics]]); liquidity (the share of successfully completed search→deal) is the main health indicator; network effects and multi-homing affect the sustainability of the take rate ([[M-platforms-types-criteria]]).

### Platform metrics
The number of client teams; the number of platform usages; the TTM of onboarding to the platform; the incremental effect on users "with the platform / without". Platform adoption separately ([[M-platform-risks-rollout]]): by clients (the breadth of the base), by places/components (the depth of replacement), by volume (the share of traffic/impressions through the platform).

## Procedure
1. **Fix the management decision** the model must support: launch / narrow the scope / postpone / reject / name a critical condition / schedule the next check.
2. **Assemble the business case in 10 blocks:** part 1 — the problem, the solution, the clients, the alternative, adoption (who connects and when); part 2 — the effect (what drives it), the costs, the payback period, scenarios, the recommendation.
3. **Build the As Is / To Be model** (the educational frame):
   - Assumptions: the horizon (e.g., 3–4 years), the schedule of onboardings by year, the cost of an FTE-month, local costs (development + support per launch), the platform's build, the annual run, the cost of onboarding.
   - As Is: `FCF_AsIs = −(local costs × N_launches)`.
   - To Be: `FCF_ToBe = −Build − Run − (onboarding × N)`.
   - ΔFCF, the cumulative stream, break-even. Then — a line of effects (savings on payments/infrastructure, an early launch) on top of the base ΔFCF.
4. **Compute ROI, IRR, payback, break-even by the number of clients**; where needed — WACC, TV, NPV.
5. **Check the scenarios** (conservative / base / optimistic) on the sensitive parameters: the number of onboardings, local costs, the cost of build and run, the cost of onboarding, the pace of adoption. The honesty rule: take the numbers from approved plans and actual costs of your own and neighboring teams, not from industry benchmarks — every line must be verifiable.
6. **Register the assumptions** per the scheme: the parameter and value → a source (expert judgment / past products / a benchmark) → an acceptable range → the assumption's owner → how and when to verify.
7. **Link the model to the roadmap** — the economics change by stage and a different decision is made at each: Discovery (estimate the range) → Build (invest in the core) → Pilot (test the client) → Scale (onboard the next) → Close (switch off the legacy solution).
8. **Formulate the management conclusion:** the decision, the constraints, the next step. For a board-level delivery: three pages — the decision and the alternative, the economics, the result and the recommendation.

### An example (illustrative numbers, an educational financial model)
A payments acceptance platform: local — 15 FTE-months of development (4.5M ₽) + 24 FTE-months of support (7.2M ₽/year) per launch; the platform — build 30M ₽, run 12M ₽/year, onboarding 2 FTE-months (0.6M ₽); launches by year 0/2/3/4; a 3-year horizon.
- TCO only: ΔFCF = −30 / +10.2 / +21.3 / +32.4; cumulative: −30 / −19.8 / +1.5 / +33.9 → payback in year 2; IRR ≈ 40%.
- The break-even threshold: savings per launch = 4.5 + 7.2 − 0.6 = 11.1; costs = 30 + 12×3 = 66 → 66 / 11.1 ≈ 6 launches. Fewer than six — it does not pay back; the decision depends on the launch plan.
- With effects (acquiring savings of +2M ₽/month, an early launch of 3 months × 2M ₽ × N): ΔFCF = −30 / +46.2 / +63.3 / +80.4 → payback ~8 months into year 1; the conservative scenario (5 launches) is positive only with effects — the dependence on adoption is critical.

## Template / checklist
| Parameter | Value | Unit | Source | Class | Check |
|---|---|---|---|---|---|
| Horizon, WACC | | years / % | | | |
| Launches/onboardings by year | | pcs | the company's plan | | |
| Local: development + support per launch | | FTE-months / ₽ | teams' facts | | |
| Platform Build / Run | | ₽ | | | |
| Platform onboarding | | FTE-months / days of client work | pilot | | |
| Effects: savings, TTM, increment | | ₽/year | A/B / case | | |
| ΔFCF by year, Cumulative, Break-even | | ₽ | calculation | | |
| ROI, IRR, Payback, NPV(+TV) | | % / months / ₽ | calculation | | |

Auto-checks:
- Revenue ≠ margin; the increment from revenue, not from GMV; margin stated separately.
- Consistent units and periods in FTE-months, years and rubles; dual run (two systems in parallel) and migration are included in the platform's costs, not lost.
- The effect is computed only on products from the approved plan; "products that could have appeared" do not enter the model.
- Cumulative ΔFCF ≥ 0 in some year → the payback year is named; if it fails to converge in the conservative scenario — that is the conclusion.
- The model is recomputed at every review; changed numbers are explained.

## Typical mistakes
- Booking all GMV through the platform as its additional revenue — the effect is computed as the ΔFCF of two scenarios, "with the platform" and "without".
- Ignoring migration, dual run and client support — the platform's TCO is understated.
- Booking FTE savings as a monetary effect while the people stay in the company and are not laid off.
- A single point estimate instead of a range and scenarios; a benchmark instead of the actual costs of your own teams.
- ROI instead of IRR as the only argument; a forgotten TV with a sustainable stream (or the reverse — a TV on an unsustainable one).
- A static model: not recomputed after the pilot, although the economics must be refined together with the roadmap.

## Questions that can change the decision
- How many launches are realistic in the approved 3–4 year plan (does the conservative scenario pay back)?
- Which parameter in the model is the most sensitive, and who owns its verification?
- Are the savings monetary or "freed people"? What happens to them?
- How many days of client work does onboarding cost — and what can reduce it?
- Will the cross-product effect (a unified loop, end-to-end loyalty, anti-fraud) appear only above a threshold share — and is it in the model?
- For a market platform: which take rate by side can competition and multi-homing sustain?

## Related cards
[[M-platforms-types-criteria]], [[M-platform-case-concept]], [[M-platform-risks-rollout]], [[M-unit-economics]], [[M-market-sizing]], [[M-success-metrics]], [[M-source-criticism]]
