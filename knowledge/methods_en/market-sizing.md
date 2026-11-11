---
id: M-market-sizing
lang: en
title: Market sizing (PAM / TAM / SAM / SOM) — a reproducible market funnel with sources and sanity checks
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [research, options, strategy, validation]
tags: [market-sizing, tam, sam, som, top-down, bottom-up, market-funnel, market-units]
related: [M-traction-model, M-unit-economics, M-benchmarking, M-source-criticism, M-competitors, M-external-environment, M-business-models]
---

# Market sizing (PAM / TAM / SAM / SOM)

## When to apply
Product leader questions: "how big is the potential?", "is it worth entering the segment / investing?", "is the market big enough to support the traction-model goals?". The card gives a reproducible calculation of the market funnel and the "top-down check" (a growth model cannot promise more than SOM).

## Core idea
**Market volume** — a quantitative estimate of actual or potential sales (money, people, or product units) obtained by calculation from data, not by assumption.

| Level | What it is | Horizon | Role |
|---|---|---|---|
| PAM (Potential Available Market) | the theoretical maximum without constraints; not used in calculations | — | an optional "ceiling" |
| TAM (Total Addressable Market) | the entire market under full coverage of all segments, with no geographic/technological limits | an aspirational target, on the order of 10 years | the headline metric for venture investors |
| SAM (Serviceable Available Market) | the part of TAM that can realistically be served given the business model, geography, technology, competitors | 3–5 years | the long-term goal |
| SOM (Serviceable Obtainable Market) | the part of SAM reachable in the near term given growth, pricing, resources | 1–3 years | the most conservative metric; the one a business plan is judged by |

**Market units** — count in whatever is closest to the business model, and show the conversion into the others:
| Unit | When | Example |
|---|---|---|
| People | audience, marketing | 15 million potential users |
| Money | investment decisions, business valuation | 2.5 bn RUB/year |
| Product units | production, logistics | 50 million orders/year |

By model: subscription = users × ARPU; e-commerce = orders × average check; marketplace = deals × commission (or GMV × take rate); B2B SaaS = companies × license price.

**Two estimation approaches**
- Top-down: world → region → country → city → segment; fast, less precise.
- Bottom-up: units (users/companies) × average price/frequency; more precise, requires data.
- Compute both and compare. The skill's rule: a divergence of more than 3× means look for an error (definitions, units, period, geography).

**Top-down formulas by funnel level** (as in the course's calculation sheets):
- `PAM = potential users × ARPU` (the global ceiling).
- `TAM = region population × % target audience × % ready to pay × ARPU`.
- `SAM = TAM × % accessible under the business model × (1 − % held by inaccessible competitors) × Adoption rate`.
- `SOM = SAM × target market share` or `SOM = current base × (1 + growth coefficient)^period`.
- An alternative "physical" formula (rental, hotels, parking): `Market volume = number of units (objects) × occupancy × period × price per unit`.
- In money and in people, the levels are defined in words through segments, for example: PAM — the entire tourism market (lodging + transport + food + leisure); TAM — the "lodging" segment in its entirety, including offline; SAM — only the same segments in the online channel (OTA); SOM — the product's estimated GMV: `SOM = booked nights × average check`, users = `nights / trip duration / trips per year`.

**The calculation is always presented together with market dynamics**: the CAGR of the base market and the forecast share of the channel (for example, the online channel's share grows from X% to Y% by the horizon) — "the market will grow N-fold, and the online channel will capture most of that growth" is a separate argument for or against entry, not just the current volume.

**Two ways to compute SOM**
| Situation | Approach |
|---|---|
| Digital scalable product | via conversions (the acquisition funnel) |
| Physical goods, manual production | via production constraints |
| A service with limited capacity | via production constraints |
| Marketplace | conversions + supply constraints (the smaller of the two is taken) |

## Procedure
1. **Research passport:** product/company, purpose ("the market potential for X in segment Y"), date, geo, horizon, main unit.
2. **Market boundaries.** Define in writing what belongs to the category and what does not ("the AI market" = software? services? chips?). Without the definition, numbers from different sources are not comparable (see [[M-source-criticism]]).
3. **Top-down:** `Segment market = Higher-level market × Geo share × Segment share` (the same units and year at every step). For each number — source, year, evidence class.
4. **Bottom-up:**
   - B2C: `TAM = N_segment × Access (%) × Frequency (times/year) × Average check (RUB/time)` → RUB/year.
   - B2B: `TAM = N_companies_in_segment × Contract value (RUB/year)`; the number of decision-makers and the sales cycle are needed for SOM.
5. **SAM** = TAM × sequential constraints (geo, channel, platform, price segment, legal). Write out each multiplier on a separate line with its source.
6. **SOM via conversions:** `Downloads/leads × CR1 × CR2 × … = active buyers`; `SOM = active buyers × Average check × Frequency (times/year)`.
7. **SOM via constraints:** `SOM = Capacity units/day × Working days × Price`.
8. **Reconciliation and sanity checks:**
   - `TAM ≥ SAM ≥ SOM`; the skill's guideline: TAM is 5–10 times larger than SAM — if the ratio is close to 1, TAM and SAM were probably confused.
   - The product of the conversions ≤ 1; the number of active buyers ≤ SAM in people.
   - The divergence between top-down and bottom-up ≤ 3×; otherwise revisit the definitions.
   - Units: RUB/year ≠ RUB/month; users ≠ orders.
   - The traction model does not exceed SOM ([[M-traction-model]]).
9. **Three scenarios** (pessimistic/base/optimistic) for the most uncertain multipliers.
10. **Visualization first:** concentric circles PAM→TAM→SAM→SOM or a waterfall (how TAM narrows down to SOM); then tables with the calculation logic.

### Examples from the skill (the numbers are illustrative)
- A clothing app: 50,000 downloads/year × 40% register × 10% first order × 50% repeat = 1,000 active users; × 3,000 RUB × 4 times/year = **12 million RUB/year**.
- Handmade bags: 2 artisans × 1 item/day × 365 days × 15,000 RUB = **10.95 million RUB/year** (check the actual number of working days: 365 is a simplification of the example).
- Top-down (traction-modeling): the Russian pharmaceutical market ~3 trillion RUB → Moscow + Moscow region 21% × diabetes 2.3% ≈ 15 bn RUB (SAM) → SOM: the leader's 10% of SAM = 1.5 bn RUB — the ceiling of a realistic goal. The numbers have no source; they are taken to demonstrate the logic.

## Template / checklist
**Calculation file format (as in the course practice)** — one sheet, two parts:
1. Research passport: the product, the purpose of the research (which decision it is computed for), the date, the list of sources, **the research conclusions** — a concluding paragraph: what market share the product has by segment, whether the market is growing (CAGR), whether the channel's share is growing, and what this means for the "invest / don't invest" decision.
2. The funnel table (each level is a row):
| Stage | Calculation logic (in words, via segments and cuts) | Volume in money | Volume in users | Sources (for each number) |
|---|---|---|---|---|
| PAM (opt.) | | | | |
| TAM | | | | |
| SAM | | | | |
| SOM | | | | |

The bottom-up check: SOM is computed from the product's own data or the closest competitor (events × conversions × check), then compared with SAM — this yields an estimated market share; it must be plausible (not "22% for a player nobody has heard of") and consistent with the capacities. In the "users" column a level may be `n/a` if the source counts transactions (travel), not unique people — this is recorded explicitly rather than glossed over.

A table for every funnel level (the minimal version):
| Stage | Calculation logic | Money | Users/units | Source (year, grade A–D) |
|---|---|---|---|---|
| PAM (opt.) | | | | |
| TAM top-down | | | | |
| TAM bottom-up | | | | |
| SAM | | | | |
| SOM | | | | |

B2C parameters: the segment's population; internet penetration/access; purchase frequency; average check; funnel conversions (benchmarks via [[M-benchmarking]] or your own data).
B2B parameters: the number of companies in the segment; the number of decision-makers; contract value; sales cycle; win rate.

Investor guidelines from the skill (**no source — grade D; verify before use**):
| Parameter | Russia, Series A | International, Series A |
|---|---|---|
| Investment | $1M–$5M | $5M–$20M |
| TAM | $100M–$1B | from $1B |
| SAM | $50M–$200M | $200M–$1B |
| Revenue/MRR | $10K–$50K/month | $50K–$200K/month |

The exit checklist: the passport; the visualization; the TAM tables (both methods), SAM, SOM; the comparison against the thresholds; the conclusions; every number with a reference to its source right in the text.

## Typical mistakes
- Confusing TAM and SAM; presenting "TAM" as a goal for 1–3 years.
- SAM without accounting for the real competitive landscape and channel constraints.
- An inflated SOM: taking "at least 1% of the market" instead of calculating it via conversions/capacity.
- Sources older than 2–3 years; numbers without references; different market definitions in the numerator and the denominator.
- Counting only in money without showing people and product units.
- Starting with tables instead of the visualization.
- A static "freeze-frame": today's volume without the market's CAGR and the forecast of the channel's share — the entry decision depends on the future market, not only on the current one.
- Market share as an input parameter of the model (see [[M-traction-model]]): share is an outcome, not an input.

## Questions that can change the decision
- What is the unit that constrains the business: demand (the funnel) or capacity?
- Does the product create a new category (no market statistics → only bottom-up and analogs)?
- Which segments are inaccessible due to geography/regulation/platform?
- What horizon does the decision need: 1–3 years (SOM) or 3–5 years (SAM)?
- Which multipliers contribute >50% of the uncertainty in the result (in the scenarios they come first)?

## Related maps
[[M-traction-model]], [[M-unit-economics]], [[M-benchmarking]], [[M-source-criticism]], [[M-competitors]], [[M-external-environment]], [[M-business-models]]
