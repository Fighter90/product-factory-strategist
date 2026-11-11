---
id: M-model-topdown-bottomup
lang: en
title: Top-Down and Bottom-up business modeling
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [options, strategy, validation]
tags: [top-down, bottom-up, market-sizing, cagr, seasonality, drivers, cohorts, baseline, gap, traction-model]
related: [M-traction-model, M-market-sizing, M-model-validation, M-unit-economics, M-monetization, M-source-criticism, M-benchmarking]
---

# Top-Down and Bottom-up business modeling

## When to apply
"What revenue and growth should we expect from the product?", "what should the forecast lean on — the market or our own data?", "how do we explain a divergence between two estimates?", "a quick potential estimate for an investor, or a detailed model for the budget?". The two approaches are used as a pair: top-down sets the frame, bottom-up does the counting, and the two are cross-checked against each other.

## Core idea
**Top-Down** goes from the market down: a known money volume of the industry becomes a ceiling, and you descend to the company through successive filters. **Bottom-up** goes from operational metrics up: real users, conversions, checks and cohorts are aggregated into revenue.

Three Top-Down projections (not alternatives but three cameras on one object — a divergence is information):
| Approach | Input | Mechanics | Role |
|---|---|---|---|
| Market/Money | market volume + share | `TAM → SAM → SOM = Market × Share` | the frame and the ceiling |
| Demand-side | clients, conversions, checks | `Revenue = Clients × Lead CR × Paying CR × Average check` | who brings the money |
| Supply-side | a resource (a limit) | `Page views × slots × fill rate × viewability × CTR × CPC/CPM` | "can we serve the demand" |

Concepts:
- **TAM** — the whole market; **SAM** — the reachable part (geo/segment/online); **SOM** — the company's real share.
- **CAGR** — the annual growth of the market; monthly: `(1 + CAGR_year)^(1/12) − 1` (simplified: CAGR/12).
- **Seasonal coefficient** — a month's multiplier (January ~0.6, November ~1.8 on the ad market); the base the percentages are taken against is fixed explicitly. The 12 coefficients sum to 12.0.
- **Baseline** — "what happens if we do nothing". Without investment the business loses share (a typical multiplier of −0.1 pp/month): competitors fight for the same market. The difference between baseline and growth = "the cost of inaction" = the value of the investment.
- **Retention** is ambiguous: by users, by transactions, by payments (a 3-month subscription = 100% payment retention while usage falls). The typical curve: M1 55% → M2 26% → M3 16% → a plateau; a plateau ≠ zero — a sign of PMF.
- **Input vs output:** assumptions are set only for input metrics (new users, conversions, check); output (revenue, P&L) is computed by formulas. "You cannot forecast an outcome — you forecast changes": growth must be explained by a driver.

The "baseline or traction" boundary ([[M-traction-model]]): can I get the effect without additional development/budget resources? Yes — baseline (always-on marketing, regular price raises, an organic network effect). No — traction (a feature, a new channel, a new geo). A feature retains and engages, marketing attracts — do not attribute acquisition to a feature. A network effect is a "bonus" that shows itself after 2–3 months.

### Approach selection matrix
| Situation | Bottom-up | Top-down | Recommendation |
|---|---|---|---|
| There is an MVP + 3 months of data | ✅ the main one | ⚠️ for cross-checking | bottom-up as the base |
| An absolute start, no data | ❌ impossible | ✅ the main one | top-down + benchmarks |
| A mature product, a new market | ✅ on the current market | ✅ on the new one | both in parallel |
| A 3+ year strategy | ⚠️ for the first year | ✅ over the horizon | top-down frame, bottom-up details |
| Launching a feature inside an existing product | ✅ the main one | ❌ not needed | bottom-up from cohorts |
| A quick estimate for an investor/pitch | ⚠️ | ✅ | top-down in one or two nights |

### Growth drivers and metrics
- **A driver** is a factor you can "turn" to get growth: product ones (features, engagement), marketing ones (acquisition), network effects (they strengthen both sides of a marketplace over time).
- The influence matrix: DAU — strongly product, weakly marketing; acquisition — strongly marketing; retention — strongly product and network effects; ARPU — moderately product.
- The driver test: "can I do this without spending additional resources?" If yes — it is baseline, not traction.
- A numerical illustration of the trap of averages: cohort A (500 people, retention 60%, ARPU 2000) + cohort B (500 people, retention 15%, ARPU 500): "by the averages" 468,750 ₽, by cohorts 637,500 ₽ — a 36% divergence.

## Procedure
1. **Determine the business's Supply** — the limiting resource: ad inventory, couriers, hotel rooms, SKUs, servers. It is also the model's upper limit.
2. **Collect Market Assumptions** (a separate sheet, every parameter with a source and an evidence class, [[M-source-criticism]]):
   - the market volume per month — start flat, and check that "month × 12" matches public data;
   - CAGR (annual) → the monthly rate; seasonal coefficients (the sum = 12.0, the base for the percentages stated explicitly);
   - the market share and its dynamics. Sources: agency reports, associations, company dashboards, expert estimates (labeled as such).
3. **Decompose Demand by segment** (segments have different checks and conversions, e.g. performance SMB vs branding enterprise): the number in the market → CR to lead → CR to payer → the check (low/high season). A reverse calculation is possible: from known payers up to leads and the market share.
4. **Build the Supply funnel:** resource → × conversions (fill rate, viewability) → × monetization (CTR × CPC or impressions/1000 × CPM). Compute RPMI = revenue / inventory × 1000 — the end-to-end efficiency.
5. **Bring the three figures to the summary sheet** (by year) and compare them. The comparability band is ±10–20%.
6. **Interpret the divergences** (the table below) — every divergence is a hypothesis to check, not an error.
7. **Build the baseline separately from growth:** the base share dynamics (often a negative multiplier of −0.1 pp/month), the retro-fact from dashboards up to the "fact/forecast" boundary, then an extension by formulas.
8. **Bottom-up on top of the baseline ([[M-traction-model]]):** driver hypotheses with an uplift on specific input metrics, computed by cohorts (never aggregated), with cohort decay and phased retention (D1/D7/D30, M1/M2/M3).
9. **Cross-check bottom-up against top-down:** a gap < 15% — the green zone; the remainder is closed with explicit hypotheses; a gap > 30% — an error in the assumptions of one of the models; bottom-up above top-down — inflated assumptions.
10. **Model hygiene:** hardcoded values (assumptions) are moved to a separate sheet, highlighted with color and labeled with a source; everything else is formulas ("extension by formulas"); not a single constant embedded inside a formula.

### Interpreting the divergences between the three approaches
| Ratio | Interpretation | Action |
|---|---|---|
| SOM < Demand < Supply | underutilization | attract demand, do not expand the resource |
| SOM < Supply < Demand | limited by the resource | grow the Supply |
| Demand < SOM | the share is inflated or the checks are understated | re-check the data and the conversions |
| Everything matches within ±10–20% | the model is consistent | fix it as the working frame |

### Sheet structure (the course reference)
`Assumptions` (the M/D/S/SS parameters with sources and confidence — see [[M-traction-model]]) → `Traction model` (metric rows × months, a year marker, annual totals via SUMIF) → `Costs assumptions` → `Checks` (GMV < the SOM cap, and others, [[M-model-validation]]).

## Template / checklist
| Parameter | Fill in |
|---|---|
| The business's Supply limit | inventory / couriers / rooms / SKUs / capacity |
| TAM, SAM, SOM + a source for each | |
| CAGR (annual) and the monthly rate | |
| Seasonal coefficients (the sum = 12.0), and which base the percentages are taken against | |
| Demand segments: volume, CR, check (low/high season) | |
| Supply funnel: fill rate, viewability, CTR, CPC/CPM, RPMI | |
| Baseline share multiplier (pp/month) | |
| Bottom-up: input metrics, cohorts, decay | |
| The gap between bottom-up and top-down | <15% green / 15–30% yellow / >30% red |
| "The cost of inaction": growth − baseline | |

The exit artifact: a summary sheet with the three top-down estimates → a bottom-up model with drivers → a divergence table with hypotheses about the causes → baseline/growth.

## Typical mistakes
- The "dream model": a 100 bn market × 1% = 1 bn with no answer to where the users come from and at what CAC/retention.
- Bottom-up without top-down (no ceiling: the model pierces through the market) and top-down without bottom-up (no mechanics: it does not explain where the money comes from).
- Flat where there is seasonality, or seasonality not correlated across parameters (the market share must not "breathe" together with the season).
- Confusing percentages and absolute values; CPM without dividing impressions by 1000.
- Averages over the whole base instead of cohorts (segments with 80% and 20% retention produce an "average" of 50% and a calculation error of tens of percent); ignoring cohort decay inflates ARPU/LTV by 30–40%.
- A "flat" baseline instead of a decaying one: without investment the share does not stand still — it declines.
- Linear growth, a "hockey stick" without an explanation ([[M-model-validation]]).

## Questions that can change the decision
- What is the Supply limit in this business, and what is its utilization right now?
- Does the annual market volume multiplied over the horizon match public data?
- Which 2–3 assumptions produce >50% of the result, and where do they come from?
- Have we computed the "no investment" baseline — and is it not a quiet loss of share?
- Do the bottom-up hypotheses close the gap to top-down, or is the gap a signal to rework both models?

## Related maps
[[M-traction-model]], [[M-market-sizing]], [[M-model-validation]], [[M-unit-economics]], [[M-monetization]], [[M-source-criticism]], [[M-benchmarking]], [[M-trends-scenarios]]
