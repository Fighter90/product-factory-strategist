---
id: M-model-topdown-bottomup
lang: en
title: Top-Down and Bottom-Up business modeling
course: strategy
sources: ["EN mirror of the RU methodology card M-model-topdown-bottomup (knowledge/methods/model-topdown-bottomup.md); original sources are listed in the RU card"]
stages: [options, strategy, validation]
tags: [top-down, bottom-up, tam, sam, som, cagr, seasonality, drivers, cohorts, baseline, gap, funnel]
related: [M-traction-model, M-market-sizing, M-model-validation, M-unit-economics, M-monetization, M-source-criticism, M-benchmarking]
---

# Top-Down and Bottom-Up Business Modeling

## When to apply
"What revenue and growth to expect from the product?", "what to base the forecast on — the market or our own data?", "how to explain a divergence between two estimates?", "quickly sketch the potential for an investor or build a detailed model for the budget". The two approaches are used as a pair: bottom-up computes, and bottom-up is cross-checked against top-down.

## Essence
**Top-Down** — from the market down: the known volume of industry money becomes a ceiling and descends to the company through successive filters. **Bottom-Up** — from operating metrics up: real users, conversions, order values and cohorts are aggregated into revenue.

Three Top-Down projections (not alternatives, but three cameras on one object — divergence = information):
| Approach | Input | Mechanics | Role |
|---|---|---|---|
| Market/Money | market size + share | `TAM → SAM → SOM = Market × Share` | frame and ceiling |
| Demand-side | clients, conversions, order values | `Revenue = Clients × CR_lead × CR_paying × Avg order value` | who brings the money |
| Supply-side | resource (limit) | `Page views × slots × fill rate × viewability × CTR × CPC/CPM` | "can we serve the demand" |

Concepts:
- **TAM** — the whole market; **SAM** — the reachable part (geo/segment/online); **SOM** — the company's realistic share.
- **CAGR** — annual market growth; monthly: `(1 + CAGR_year)^(1/12) − 1` (simplified: CAGR/12).
- **Seasonal coefficient** — a multiplier for the month (January ~0.6, November ~1.8 in the ad market); the base for percentages is fixed explicitly. The sum of the 12 coefficients = 12.0.
- **Baseline** — "what happens if we do nothing". Without investment a business loses share (a typical multiplier is −0.1 pp/month): competitors fight for the same market. The difference between baseline and growth = "the cost of inaction" = the value of the investment.
- **Retention** is ambiguous: by users, by transactions, by payments (a 3-month subscription = 100% payment retention while usage declines). A typical curve: M1 55% → M2 26% → M3 16% → stabilization; stabilization ≠ zero — a sign of PMF.
- **Input vs output:** assumptions are set only for input metrics (new users, conversions, order value); output (revenue, P&L) is computed by formulas. "You cannot forecast the result — you must forecast the changes": growth has to be explained by a driver.

The "baseline or traction" boundary ([[M-traction-model]]): can I get the effect without extra development/budget resources? Yes — baseline (ongoing marketing, regular price increases, organic network effect). No — traction (a feature, a new channel, a new geo). A feature retains and engages, marketing acquires — do not attribute acquisition to a feature. The network effect is a "bonus" that shows up after 2–3 months.

### Matrix for choosing the approach
| Situation | Bottom-up | Top-down | Recommendation |
|---|---|---|---|
| MVP + 3 months of data | ✅ primary | ⚠️ for cross-check | bottom-up as the base |
| Absolute start, no data | ❌ impossible | ✅ primary | top-down + benchmarks |
| Mature product, new market | ✅ for the current market | ✅ for the new one | both in parallel |
| A 3+ year strategy | ⚠️ for the first year | ✅ for the horizon | top-down frame, bottom-up details |
| Feature launch in an existing product | ✅ primary | ❌ not needed | bottom-up from cohorts |
| A quick estimate for an investor/pitch | ⚠️ | ✅ | top-down in one or two nights |

### Growth drivers and metrics
- **A driver** — a factor you can "tune" and get growth: product (features, engagement), marketing (acquisition), network effects (they strengthen both sides of a marketplace over time).
- Influence matrix: DAU — strongly product, weakly marketing; acquisition — strongly marketing; retention — strongly product and network effects; ARPU — moderately product.
- Driver test: "can I do this without spending additional resources?" If yes — it is baseline, not traction.
- A numeric illustration of the trap of averages: cohort A (500 people, retention 60%, ARPU 2000) + cohort B (500 people, retention 15%, ARPU 500): "by averages" 468,750 ₽, by cohorts 637,500 ₽ — a 36% divergence.

## Procedure
1. **Define the business's Supply** — the limiting resource: ad inventory, couriers, hotel rooms, SKUs, servers. It is also the model's upper limit.
2. **Assemble Market Assumptions** (a separate sheet, every parameter with a source and a confidence class, [[M-source-criticism]]):
   - market size per month — start flat, and check that "month × 12" matches public data;
   - CAGR (annual) → the monthly rate; seasonal coefficients (sum = 12.0, the percentage base explicit);
   - market share and its dynamics. Sources: agency reports, associations, company dashboards, expert judgment (flag it as such).
3. **Split Demand into segments** (segments have different order values and conversions, e.g., performance SMB vs branding enterprise): market count → CR to lead → CR to paying → order value (low/high season). A "reverse" computation is possible: from known payers upward to leads and market share.
4. **Build the Supply funnel:** resource → × conversions (fill rate, viewability) → × monetization (CTR × CPC or impressions/1000 × CPM). Compute RPMI = revenue / inventory × 1000 — the end-to-end efficiency.
5. **Bring the three figures onto the summary sheet** (by year) and compare. Comparability threshold ±10–20%.
6. **Interpret the divergences** (table below) — every divergence is a hypothesis to test, not an error.
7. **Build the baseline separately from growth:** the base share dynamics (often a negative multiplier −0.1 pp/month), the retro fact from dashboards up to the "fact/forecast" boundary, beyond it — extension with formulas.
8. **Bottom-up on top of the baseline ([[M-traction-model]]):** driver hypotheses with uplift on specific input metrics, by cohorts (do not aggregate), with cohort decay and phased retention (D1/D7/D30, M1/M2/M3).
9. **Cross-check bottom-up against top-down:** a gap < 15% — the green zone; the remainder is covered by explicit hypotheses; a gap > 30% — an error in the assumptions of one of the models; bottom-up above top-down — inflated assumptions.
10. **Model hygiene:** hardcoded values (assumptions) are moved to a separate sheet, color-highlighted and labeled with a source; everything else is formulas ("extension with formulas"); not a single constant embedded inside formulas.

### Interpreting divergences between the three approaches
| Relationship | Interpretation | Action |
|---|---|---|
| SOM < Demand < Supply | underutilization | attract demand, do not expand the resource |
| SOM < Supply < Demand | limited by the resource | grow Supply |
| Demand < SOM | share inflated or order values deflated | re-check the data and conversions |
| Everything matches ±10–20% | the model is consistent | fix it as the working frame |

### Sheet structure (the course's reference)
`Assumptions` (M/D/S/SS parameters with sources and confidence — see [[M-traction-model]]) → `Traction model` (metric rows × months, a year marker, annual totals via SUMIF) → `Costs assumptions` → `Checks` (GMV < SOM cap, etc., [[M-model-validation]]).

## Template / checklist
| Parameter | To fill in |
|---|---|
| Business Supply limit | inventory / couriers / rooms / SKUs / capacity |
| TAM, SAM, SOM + a source for each | |
| CAGR (annual) and the monthly rate | |
| Seasonal coefficients (sum = 12.0), which base the percentages use | |
| Demand segments: volume, CR, order value (low/high season) | |
| Supply funnel: fill rate, viewability, CTR, CPC/CPM, RPMI | |
| Baseline share multiplier (pp/month) | |
| Bottom-up: input metrics, cohorts, decay | |
| Gap bottom-up vs top-down | <15% green / 15–30% yellow / >30% red |
| "Cost of inaction": growth − baseline | |

Exit artifact: a summary sheet with three top-down estimates → a bottom-up model with drivers → a divergence table with hypotheses about causes → baseline/growth.

## Typical mistakes
- A "dream model": a 100B market × 1% = 1B with no answer to where users come from and what the CAC/retention will be.
- Bottom-up without top-down (no ceiling: the model punches through the market) and top-down without bottom-up (no mechanics: it does not explain where the money comes from).
- Flat where there is seasonality, or seasonality not correlated across parameters (market share must not "breathe" with the season).
- Confusing percentages and absolute values; CPM without dividing impressions by 1000.
- Averages over the whole base instead of cohorts (segments with retention 80% and 20% give an "average" of 50% and calculation errors of tens of percent); ignoring cohort decay inflates ARPU/LTV by 30–40%.
- A "flat" baseline instead of a decaying one: without investment share does not stand still — it declines.
- Linear growth, a "hockey stick" without explanation ([[M-model-validation]]).

## Questions that can change the decision
- What is the Supply limit in this business, and what is its utilization now?
- Does the annual market size multiplied over the horizon match public data?
- Which 2–3 assumptions deliver >50% of the result, and where do they come from?
- Did we compute the "no investment" baseline — and is it not just a quiet loss of share?
- Do the bottom-up hypotheses close the gap to top-down, or is the gap a signal to revise both models?

## Related cards
[[M-traction-model]], [[M-market-sizing]], [[M-model-validation]], [[M-unit-economics]], [[M-monetization]], [[M-source-criticism]], [[M-benchmarking]], [[M-trends-scenarios]]
