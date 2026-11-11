---
id: M-platform-economics
lang: en
title: Platform economics: TCO, effects, financial model, metrics
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [options, strategy, validation]
tags: [platforms, tco, financial-model, dcf, irr, npv, break-even, scenarios, increment, adoption]
related: [M-platforms-types-criteria, M-platform-case-concept, M-platform-risks-rollout, M-unit-economics, M-market-sizing, M-success-metrics, M-source-criticism]
---

# Platform economics: TCO, effects, financial model, metrics

## When to apply
"Does the platform's economics close, and how do we prove it to the committee?", "what do we compare the platform against and how do we count the effect?", "when will it pay back and at what number of connections?", "which assumptions are critical and how do we verify them?" Taken after the concept ([[M-platform-case-concept]]); linked to unit economics ([[M-unit-economics]]).

## Core idea
Platform economics = three parts: **TCO** (the costs of development, support and integrations) + **business effect** (what becomes faster, bigger, better — converted into money) + **comparison with alternatives** (As Is without the platform vs To Be with it). A direct "business effect of the platform as a product" is hard to defend — the usual route is a comparison of the TCO of the platform and the alternatives.

### Cost structure
| Local solutions | Platform |
|---|---|
| Development in every team | Core and launch |
| Repeated rework | Client integrations |
| Support and infrastructure | Migration and launches on the client side; infrastructure |

Costs are divided into **one-off** (building the core, architectural changes, migration and transition tooling) and **recurring** (the platform team, client support, documentation). For an external market, CAPEX (material assets, for example servers) with depreciation (non-cash, not part of cash costs) and OPEX (operations) are added. The unit of labor costs is the FTE-month at the organization's average employee cost; the full financial model is finalized by finance.

### Six sources of effect
1. Additional revenue or growth of other user metrics. 2. Infrastructure savings. 3. Faster launches (TTM). 4. Lower run costs. 5. Development savings (teams and solutions never created). 6. Prevented losses.

### Key formulas
- **Base comparison:** `ΔFCF = FCF_ToBe − FCF_AsIs` by year; `Cumulative ΔFCF = Σ ΔFCF`; **break-even** — the first year where the cumulative ΔFCF ≥ 0.
- **Payback threshold (break-even by the number of clients):** `Number of launches = (Build + Run over the horizon) / Saving per launch`, where the saving per launch = (local development + local support − platform onboarding).
- **ROI** = (benefit − cost) / cost; **IRR** — the discount rate at which the NPV of the ΔFCF stream = 0 (more important than ROI for the committee).
- **WACC** — the weighted average cost of capital; higher risk → higher rate. **Discounting:** `PV = ΔFCF_t / (1+WACC)^t`.
- **Terminal value:** `TV_T = FCF_T_sustainable / WACC` (only the sustainable annual FCF after the horizon); `NPV = Σ PV ΔFCF + PV TV`.
- **Incremental effect (CRM-type):** `Audience → Coverage (the share reached) → Conversion (the share of the target action) → Increment (the difference with control, A/B) → Value (increment × value of the action → revenue, EBITDA, FCF)`. The increment is counted from **company revenue**, not from GMV and not directly from the take rate; revenue ≠ margin (an increment in sales volume at a tiny margin is worth almost nothing in money).
- **TTM effect:** `Saving/effect = (Local launch time − launch time with the platform) × marginal effect per month × number of launches`.
- **For ecosystem (market) platforms:** `Platform revenue = GMV × take rate`; the take rate can be differentiated by side; the deficient side is subsidized (free/negative price), and the side whose value grows with liquidity is monetized; unit economics are counted by sides and cohorts ([[M-unit-economics]]); liquidity (the share of successfully completed search→deal journeys) is the main health indicator; network effects and multi-homing affect the sustainability of the take rate ([[M-platforms-types-criteria]]).

### Platform metrics
The number of client teams; the number of platform usages; the TTM of connecting to the platform; the incremental effect on users "with the platform / without". Platform adoption separately ([[M-platform-risks-rollout]]): by clients (the width of the base), by places/components (the depth of replacement), by volume (the share of traffic/impressions through the platform).

## Procedure
1. **Fix the management decision** the model must support: launch / narrow the scope / postpone / reject / name the critical condition / schedule the next check.
2. **Assemble the 10-block business case:** part 1 — problem, solution, clients, alternative, adoption (who connects and when); part 2 — effect (through what), costs, the payback period, scenarios, recommendation.
3. **Build the As Is / To Be model** (a teaching scaffold):
   - Assumptions: the horizon (for example 3–4 years), the onboarding schedule by year, the cost of an FTE-month, local costs (development + support per launch), the platform build, the run per year, the onboarding cost.
   - As Is: `FCF_AsIs = −(local costs × N_launches)`.
   - To Be: `FCF_ToBe = −Build − Run − (onboarding × N)`.
   - ΔFCF, the cumulative flow, break-even. Then — a row of effects (savings on payments/infrastructure, an earlier launch) on top of the base ΔFCF.
4. **Compute ROI, IRR, payback, break-even by the number of clients**; where needed, WACC, TV, NPV.
5. **Run the scenarios** (conservative / base / optimistic) on the sensitive parameters: the number of connections, local costs, the build and run cost, the onboarding cost, the adoption pace. The honesty rule: take the numbers from approved plans and the actual costs of your own and neighboring teams, not from industry benchmarks — any line must be checkable.
6. **Register the assumptions** according to the scheme: parameter and value → source (expert estimate / past products / benchmark) → allowed range → owner of the assumption → how and when to verify.
7. **Link the model to the roadmap** — the economics change across stages, and at each stage its own decision is taken: Discovery (estimate the range) → Build (invest in the core) → Pilot (verify with a client) → Scale (onboard the next) → Close (switch off the legacy solution).
8. **Formulate the management conclusion:** decision, constraints, next step. For a PR-level deliverable: three pages — decision and alternative, economics, result and recommendation.

### Example (illustrative numbers, a teaching financial model)
A payment acceptance platform: local — 15 FTE-months of development (4.5M ₽) + 24 FTE-months of support (7.2M ₽/year) per launch; platform — build 30M ₽, run 12M ₽/year, onboarding 2 FTE-months (0.6M ₽); launches by year 0/2/3/4; the horizon is 3 years.
- TCO only: ΔFCF = −30 / +10.2 / +21.3 / +32.4; cumulative: −30 / −19.8 / +1.5 / +33.9 → payback in year 2; IRR ≈ 40%.
- The break-even threshold: the saving per launch = 4.5 + 7.2 − 0.6 = 11.1; costs = 30 + 12×3 = 66 → 66 / 11.1 ≈ 6 launches. Fewer than six — no payback; the decision depends on the launch plan.
- With effects (acquiring savings of +2M ₽/month, an earlier launch of 3 months × 2M ₽ × N): ΔFCF = −30 / +46.2 / +63.3 / +80.4 → payback ~8 months into year 1; the conservative scenario (5 launches) is still positive only with the effects — the dependence on adoption is critical.

## Template / checklist
| Parameter | Value | Unit | Source | Class | Check |
|---|---|---|---|---|---|
| Horizon, WACC | | years / % | | | |
| Launches/onboardings by year | | pcs | the company plan | | |
| Local: development + support per 1 launch | | FTE-months / ₽ | team facts | | |
| Platform build / run | | ₽ | | | |
| Onboarding to the platform | | FTE-months / client days | pilot | | |
| Effects: savings, TTM, increment | | ₽/year | A/B / case | | |
| ΔFCF by year, Cumulative, Break-even | | ₽ | calculation | | |
| ROI, IRR, Payback, NPV(+TV) | | % / months / ₽ | calculation | | |

Auto-checks:
- Revenue ≠ margin; the increment is counted from revenue, not from GMV; the margin is stated separately.
- The same units and periods across FTE-months, years and rubles; dual run (the parallel operation of two systems) and migration are included in the platform's costs, not lost.
- The effect is counted only on the products from the approved plan; "products that could have appeared" do not enter the model.
- Cumulative ΔFCF ≥ 0 in some year → the payback year is named; if it does not close in the conservative scenario — that is the conclusion.
- The model is recalculated at every review; the changed numbers are explained.

## Typical mistakes
- Booking all GMV through the platform as its incremental revenue — the effect is counted as the ΔFCF of two scenarios, "with the platform" and "without".
- Ignoring migration, dual run and client support — the platform TCO is understated.
- Booking FTE savings as a cash effect when the people stay in the company and are not laid off.
- A single point estimate instead of a range and scenarios; a benchmark instead of the actual costs of your own teams.
- ROI instead of IRR as the only argument; a forgotten TV with a sustainable flow (or the opposite — a TV with an unsustainable flow).
- A static model: not recalculated after the pilot, although the economics must be refined together with the roadmap.

## Questions that can change the decision
- How many launches are really in the approved plan for 3–4 years (does the conservative scenario pay back)?
- Which parameter in the model is the most sensitive, and who owns its verification?
- Is the saving monetary or "freed people"? What will happen to them?
- How many days of client work does onboarding cost — and what can reduce it?
- Will the cross-product effect (a single perimeter, end-to-end loyalty, anti-fraud) appear only above a threshold share — and is it in the model?
- For a market platform: what take rate per side will competition and multi-homing sustain?

## Related maps
[[M-platforms-types-criteria]], [[M-platform-case-concept]], [[M-platform-risks-rollout]], [[M-unit-economics]], [[M-market-sizing]], [[M-success-metrics]], [[M-source-criticism]]
