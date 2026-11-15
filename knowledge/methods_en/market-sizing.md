---
id: M-market-sizing
lang: en
title: Market sizing (PAM / TAM / SAM / SOM)
course: skills
sources: ["EN mirror of the RU methodology card M-market-sizing (knowledge/methods/market-sizing.md); original sources are listed in the RU card"]
stages: [research, options, strategy, validation]
tags: [market, tam, sam, som, top-down, bottom-up, market-units, market-funnel]
related: [M-traction-model, M-unit-economics, M-benchmarking, M-source-criticism, M-competitors, M-external-environment, M-business-models]
---

# Market sizing (PAM / TAM / SAM / SOM)

## When to apply
The product leader's questions: "how big is the potential?", "is it worth entering the segment / investing?", "is the market big enough for the traction model's goals?". The map gives a reproducible calculation of the market funnel and the "top-down check" (a growth model cannot promise more than SOM).

## Essence
**Market volume** — a quantitative estimate of real or potential sales (money, people or product units), obtained by calculation from data, not by assumption.

| Level | What it is | Horizon | Role |
|---|---|---|---|
| PAM (Potential Available Market) | the theoretical maximum without constraints; not used in calculations | — | an optional "ceiling" |
| TAM (Total Addressable Market) | the whole market with all segments covered and no geo/technology constraints | a stretch goal, on the order of 10 years | the headline figure for venture investors |
| SAM (Serviceable Available Market) | the part of TAM actually serviceable given the business model, geography, technology, competitors | 3–5 years | the long-term goal |
| SOM (Serviceable Obtainable Market) | the part of SAM achievable in the near term given growth, price, resources | 1–3 years | the most conservative metric, the one expected in a business plan |

**Market units** — count in what is closest to the business model and show the conversion into the others:
| Unit | When | Example |
|---|---|---|
| People | audience, marketing | 15M potential users |
| Money | investment decisions, business valuation | 2.5B ₽/year |
| Product units | production, logistics | 50M orders/year |

By model: subscription = users × ARPU; e-commerce = orders × average order value; marketplace = deals × commission (or GMV × take rate); B2B SaaS = companies × licence price.

**Two ways to estimate**
- Top-down: world → region → country → city → segment; fast, less precise.
- Bottom-up: units (users/companies) × average price/frequency; more precise, requires data.
- Calculate both and compare. The skill's rule: a divergence of more than 3x means looking for an error (definitions, units, period, geography).

**Top-down formulas by funnel level** (as in the course's calculation sheets):
- `PAM = potential users × ARPU` (the global ceiling).
- `TAM = region population × % target audience × % willing to pay × ARPU`.
- `SAM = TAM × % reachable by the business model × (1 − % held by unreachable competitors) × Adoption rate`.
- `SOM = SAM × target market share` or `SOM = current base × (1 + growth coefficient)^period`.
- An alternative "physical" formula (rental, hotels, parking): `Market volume = number of units (objects) × occupancy × period × price per unit`.
- In money and in people, the levels are defined in words through segments, e.g.: PAM — the entire tourism market (accommodation + transport + food + leisure); TAM — the "accommodation" segment as a whole, including offline; SAM — only the same segments in the online channel (OTA); SOM — the product's estimated GMV: `SOM = booked nights × average order value`, users = `nights / trip duration / trips per year`.

**The calculation is always shown together with market dynamics**: the base market's CAGR and the forecast channel share (e.g., the online channel's share grows from X% to Y% by the horizon) — "the market will grow N-fold, and the online channel will capture most of that growth" is a separate argument for/against entry, not just the current volume.

**Two ways to SOM**
| Situation | Approach |
|---|---|
| Digital scalable product | through conversions (the acquisition funnel) |
| Physical goods, manual production | through production constraints |
| A service with limited capacity | through production constraints |
| Marketplace | conversions + supply constraints (the smaller one is taken) |

## Procedure
1. **The research passport:** product/company, the goal ("market potential for X in segment Y"), date, geography, horizon, the primary unit.
2. **Market boundaries.** Define in writing what belongs to the category and what does not (is the "AI market" software? services? chips?). Without a definition, figures from different sources are not comparable (see [[M-source-criticism]]).
3. **Top-down:** `Segment_market = Upper_level_market × Geo_share × Segment_share` (the same units and year at every step). For every figure — source, year, credibility grade.
4. **Bottom-up:**
   - B2C: `TAM = Segment_N × Access(%) × Frequency (times/year) × Average order value (₽/time)` → ₽/year.
   - B2B: `TAM = Segment_company_count × Contract value (₽/year)`; the number of decision-makers and the sales cycle are needed for SOM.
5. **SAM** = TAM × sequential constraints (geo, channel, platform, price segment, legal). Write out every multiplier on its own line with a source.
6. **SOM through conversions:** `Downloads/leads × CR1 × CR2 × … = active buyers`; `SOM = active × Average order value × Frequency (times/year)`.
7. **SOM through constraints:** `SOM = Capacity units/day × Working days × Price`.
8. **Reconciliation and sanity-checks:**
   - `TAM ≥ SAM ≥ SOM`; the skill's benchmark: TAM is 5–10x bigger than SAM — if the ratio is close to 1, TAM and SAM have probably been confused.
   - The product of conversions ≤ 1; the number of active buyers ≤ SAM in people.
   - The top-down vs bottom-up divergence ≤ 3x; otherwise revise the definitions.
   - Units: ₽/year ≠ ₽/month; users ≠ orders.
   - The traction model does not exceed SOM ([[M-traction-model]]).
9. **Three scenarios** (pessimistic/base/optimistic) for the most uncertain multipliers.
10. **Visualization first:** concentric circles PAM→TAM→SAM→SOM or a waterfall (how TAM narrows to SOM); then tables with the calculation logic.

### Examples from the skill (figures are illustrative)
- A clothing app: 50,000 downloads/year × 40% signup × 10% first order × 50% repeat = 1,000 active users; × 3,000 ₽ × 4 times/year = **12M ₽/year**.
- Handmade bags: 2 makers × 1 unit/day × 365 days × 15,000 ₽ = **10.95M ₽/year** (check the real working days: 365 is a simplification of the example).
- Top-down (traction-modeling): the Russian pharmaceutical market ~3T ₽ → Moscow+region 21% × diabetes 2.3% ≈ 15B ₽ (SAM) → SOM: the leader's 10% of SAM = 1.5B ₽ — the ceiling of a realistic goal. Figures without a source, taken to demonstrate the logic.

## Template / checklist
**The calculation file format (as in the course practice)** — one sheet, two parts:
1. The research passport: product, the research goal (which decision this is calculated for), date, the list of sources, **the research summary** — a concluding paragraph: what market share the product has by segments, whether the market is growing (CAGR), whether the channel share is growing, and what that means for the "invest / don't invest" decision.
2. The funnel table (each level is a row):
| Stage | Calculation logic (in words, through segments and slices) | Volume in money | Volume in users | Sources (for every figure) |
|---|---|---|---|---|
| PAM (opt.) | | | | |
| TAM | | | | |
| SAM | | | | |
| SOM | | | | |

The bottom-up check: SOM is calculated from the product's data or the nearest competitor's (events × conversions × order value), then compared with SAM — yielding the implied market share; it must be plausible (not "22% for a player nobody knows") and consistent with the capacities. In "users", a level may be `n/a` if the source counts transactions (travel), not unique people — this is stated explicitly, not glossed over.

A table per funnel level (the minimal version):
| Stage | Calculation logic | Money | Users/units | Source (year, grade A–D) |
|---|---|---|---|---|
| PAM (opt.) | | | | |
| TAM top-down | | | | |
| TAM bottom-up | | | | |
| SAM | | | | |
| SOM | | | | |

B2C parameters: segment population; internet penetration/access; purchase frequency; average order value; funnel conversions (benchmarks via [[M-benchmarking]] or own data).
B2B parameters: the number of companies in the segment; the number of decision-makers; contract value; the sales cycle; win rate.

Investor benchmarks from the skill (**no source — grade D, verify before use**):
| Parameter | Russia, Series A | International, Series A |
|---|---|---|
| Investment | $1M–$5M | $5M–$20M |
| TAM | $100M–$1B | from $1B |
| SAM | $50M–$200M | $200M–$1B |
| Revenue/MRR | $10K–$50K/mo | $50K–$200K/mo |

The exit checklist: the passport; the visualization; the TAM tables (both methods), SAM, SOM; comparison with the thresholds; conclusions; every number with a source reference right in the text.

## Typical mistakes
- Confusing TAM and SAM; presenting "TAM" as a goal for 1–3 years.
- SAM without accounting for the real competitive landscape and channel constraints.
- An inflated SOM: taking "at least 1% market share" instead of calculating from conversions/capacity.
- Sources older than 2–3 years; figures without references; different market definitions in numerator and denominator.
- Counting only in money without showing people and product units.
- Starting with tables instead of the visualization.
- A static "snapshot": today's volume without the market CAGR and the channel-share forecast — the entry decision depends on the future market, not only the current one.
- Market share as an input parameter of the model (see [[M-traction-model]]): share is an outcome, not an input.

## Questions that can change the decision
- Which unit constrains the business: demand (the funnel) or capacity?
- Does the product create a new category (no market statistics → only bottom-up and analogues)?
- Which segments are unreachable by geo/regulation/platform?
- What horizon does the decision need: 1–3 years (SOM) or 3–5 years (SAM)?
- Which multipliers contribute >50% of the result's uncertainty (in the scenarios they go first)?

## Related maps
[[M-traction-model]], [[M-unit-economics]], [[M-benchmarking]], [[M-source-criticism]], [[M-competitors]], [[M-external-environment]], [[M-business-models]]
