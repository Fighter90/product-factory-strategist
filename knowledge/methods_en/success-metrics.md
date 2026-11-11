---
id: M-success-metrics
lang: en
title: Success metrics — North Star Metric, metric tree, AARRR and OKR
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [strategy, validation, after-decision]
tags: [nsm, north-star-metric, metric-tree, aarrr, okr, leading-metrics, proxy-metrics, key-results, leading-lagging, impact-outcome-output-input]
related: [M-strategy-growth, M-goals-drivers-bets, M-outcome-roadmap, M-loyalty-metrics, M-unit-economics, M-traction-model, M-quant-methods, M-pmf-scaling, M-ab-testing, M-product-metrics]
---

# Success metrics — North Star Metric, metric tree, AARRR and OKR

## When to apply
When you need to answer the questions "how will we know that the strategy works", "which single metric do all teams subordinate to", "how are the goals of the quarter connected to the long-term result". The outcome is an NSM checked against the criteria, a metric tree with owners and proven links, the period's objectives and key results, and a list of metrics with formulas, units and horizons.

## Core idea
**Four levels of strategy metrics** (session 1) and the **pyramid** (session 5) describe one idea: from the long-term result down to what the team influences directly.
| Level | What it is | Horizon | Examples |
|---|---|---|---|
| NSM / Impact | long-term value and growth | years | EBITDA, ROI, LTV/CAC; the product's NSM |
| Outcome | the result of the goal-setting period (team goals) | quarter–year | revenue, deals, retention |
| Output | an intermediate result, a proxy | sprint–quarter | conversion, buyout share, response speed |
| Input | what the team influences directly | day–sprint | adoption, the number of pushes, AOV |
The team manages bottom-up: input and output → outcome → NSM. Relative metrics (percentages, conversions) are dangerous as goals: when scaling, conversion falls (cold traffic) while deals grow. What you can "touch" is money, deals, GMV — conversion and average order value are merely attributes. NPS as a product metric is unreliable: it can fall while the product improves (tariff increases).

**North Star Metric** — the key indicator that best predicts long-term success: it leads to revenue growth, reflects customer value, measures real progress. Why it matters: it aligns teams around one goal, gives transparency of the result, supports customer focus. **Revenue is a bad NSM**: it pushes toward short-term squeezing, user burnout and churn.

**Eight NSM criteria**
| # | Question | Example / explanation |
|---|---|---|
| 1 | Does it coincide with the customer's moment of "success"? | a booking service — a booked trip; not "registrations" |
| 2 | Does it express value, not only sales? | "orders without complaints", "delivered in 15 minutes" are more precise than "orders" |
| 3 | Is it quantitatively measurable? | not "satisfaction", but the number of operations, frequency, time saved |
| 4 | Is it time-bound? | day/week/month; avoid annual intervals |
| 5 | Is it under control (minimum of external factors)? | depends on the actions of the team and the customers |
| 6 | NSM growth = business growth? | "the number of downloaded reports" is bad (they downloaded ten times because of errors); better "successfully downloaded reports per week" |
| 7 | Is it linked to the AARRR funnel (does every team influence it)? | growth of any stage shifts the NSM |
| 8 | Does it change often enough? | daily/weekly; the action repeats ≈3–4 times a month per user |
Examples of good NSMs from the course: MAU, listening time (an audio service), the number of purchases per month, booked nights (accommodation booking), the number of sent messages, the number of answers to questions, trips per user per week (taxi), weekly active teams, DAU. For a delivery marketplace in the course: successful deals with delivery.

**Metric tree** — a logical hierarchy: input metrics (Layer 2 and below) influence the focus metrics (Layer 1), and those influence the NSM. Rules:
- Layer 1 — 3–5 metrics that directly influence the NSM; each has an **owner** (a team or a function). A metric without an owner degrades. A typical distribution: 3–5 teams per business, each "owning" its Layer 1 and formulating goals relative to its metric.
- **A two-sided marketplace: a deal requires all conditions simultaneously.** A successful delivery/booking happens only if (1) the buyer chose the service, (2) the seller connected it, (3) the listing/property has the activated service. Therefore Layer 1 must cover both sides of the market and the product — measuring only demand is not enough: demand without supply yields no deals.
- Links between levels are **proven** (an A/B test, correlation, a retrospective), not assumed: growing the number of sellers by 10% may add 1–2% of deals — the link exists, the coefficient is low; links are not a simple sum/product but coefficients.
- Acquisition growth does not equal deal growth (irrelevant traffic is possible): quality metrics must grow along with it.
- The tree changes with the stage: launch — acquisition and activation; growth — scale; maturity — retention and income; optimization — efficiency. Two or three depths are enough.
- Purpose: visualization, prioritization, monitoring. The tree is a map of levers; ranking is an example of a controllable lever (more traffic to listings with delivery).

**AARRR** — the frame of the tree's blocks: Acquisition (signups), Activation (aha-moment, free→paid conversion), Retention (retention, DAU/MAU), Referral (NPS, share the link), Revenue (LTV, AOV, CAC). An example of Layer 2 for "buyers who chose delivery": the share of listings with delivery, traffic to those listings, the CTR into the delivery block, the share of sellers who passed onboarding.

**OKR**: Objective (where we want to arrive, an outcome) + Key Results (how we will know we are moving) + scoring. An Objective is a verb + what we want + "so that" + which value we create; it sets direction, answers "why", follows from the team's mission, motivates, is understandable and memorable, and is tied to the company's strategy. A Key Result is a verb + value + "from X to Z"; achievable, ambitious, measurable, **sensitive** within the period (usually a quarter). KRs are formulated through **leading** metrics (action, process), not **lagging** ones (result): "reduce daily calories to X", not "reduce weight". **A KR sits one Layer below the Objective** (Objective on Layer 1 → KR on Layer 2). The format is uniform across the company, so that anyone can read the neighboring team's goals.

Example: Objective — "grow the number of buyers who prefer delivery, to raise the number of successful deals"; KR1 — the number of categories with delivery from 3 to 6; KR2 — the share of traffic to delivery-enabled listings in ranking from 10% to 15%. An example of a KR on quality: "start accounting for the seller rating in recommendations, so that the CTR of the first five positions grows from 10% to 20%". The selection paradox: more recommendations may lower conversion — set a composite KR ("clicks grow, conversion into a deal does not fall") or a KR on conversion.

**Proving the KR → Objective link** is the hardest part of OKR; four mechanisms in decreasing strength: an A/B test (the gold standard), correlation analysis on history, a counterfactual "before/after" comparison with a control group, a logical chain (allowed only for obvious links — "more categories → more choice → more buyers" — and even then confirmed with data). Without a proven link the KR can be met while the Objective is not. **Technical teams** set infrastructure KRs (for example, "make parallel A/B tests possible", "start accounting for the rating in recommendations") — their link to the business metric goes through enabling the product teams, and it must be named explicitly.

### From goals to metrics: bets as evidence and the "expectation → fact" loop (a distillation of "Data Analysis", sessions 2 and 4)
- **How metrics are "born":** a goal → strategy and bets (how we will reach the goal) → data and metrics. Every bet must have its own **driver metric** with an obvious link to the goal's target metric; the target metrics of teams are linked to the target metric of the strategy. If the chosen metric does not explain the movement toward the goal, the bet is revised, not the data. Bet prioritization — RICE (Reach, Impact, Confidence, Effort).
- **The Leading / Lagging division** (a framework, session 4): leading metrics (input/output: the action and its proxy) are managed and show progress fast; lagging ones (outcome/NSM) confirm the result. KRs are formulated on leading metrics; the NSM and the goals of the period — on lagging ones. The mistake is to ignore the leading metrics and "manage" only the outcome.
- **The trio for any scale:** target (the main criterion) + proxy (moves earlier, predicts the target) + counter (what must not be allowed). It works identically at the level of a stream/strategy, a product/project and an initiative/feature — only the horizon changes.
- **The expectation is fixed before the launch:** for every initiative, in advance, "which metric will change and by how much" is written down (magnitude + period). After the experiment the fact is compared with the expectation: a divergence is analyzed through the drivers; if "the metric dances", first check the stability and seasonality of the metric itself ([[M-product-metrics]]: a drop can be normal).
- **The decision on the result — Scale / Iterate / Drop:** rollout with a confirmed effect and no harm to the counter-metrics; rework and a repeat test with a partial effect; abandonment with no effect — with the conclusion necessarily written into the knowledge base. Risks are checked with counter-metrics before scaling ("don't fix one thing by breaking another": liquidity redistribution, churn of payers).
- **Frameworks as a frame, not as dogma:** AARRR sets the blocks of the tree (each team gets its own stage), HEART — a cut of experience quality (Happiness/Engagement/Adoption/Retention/Task Success), One Metric That Matters — the focus of the period. A framework is adapted to the product, not copied.

## Procedure
1. **Define the product stage** and the business/product NSM (2–3 candidates); check each against the eight criteria; reject revenue.
2. **Build the tree top-down**: NSM → 3–5 Layer 1 metrics (by AARRR blocks or another logic) → Layer 2 → Layer 3 if needed. Assign an owner to each Layer 1 metric.
3. **State the proof status for each link**: proven by A/B / correlation / retrospective / hypothesis. Put the hypotheses into the validation plan (`M-goals-drivers-bets`).
4. **Choose the target metrics** so that the team can "paint" them (measure them with statistical significance) within the period: if the outcome is too coarse (company revenue), choose an output/input with a proven link.
5. **Formulate the quarterly OKR**: first the team's NSM and its tree, then the drivers, then the Objective; KRs are leading, one layer below, "from X to Z".
6. **Fill in the passport of each metric**: definition, formula, unit, period, data source, owner, baseline, target, sensitivity horizon.
7. **Set up a review** (once a quarter, and off-schedule when the strategy changes): are the links confirmed, has a metric lost its owner.
8. Pass the metrics to `M-outcome-roadmap` (output for the pilot, outcome for validation and scaling).

## Template / checklist
**Metric passport**
| Field | Example |
|---|---|
| Name and level | the share of orders delivered within ≤15 minutes (a team outcome) |
| Formula, units, period | orders delivered within ≤15 minutes / all orders, %, week |
| Source | the delivery event in the data warehouse |
| Owner | team X |
| Baseline → target → deadline | 62% → 70% within a quarter |
| Type of link to the upper level | proven by A/B (the effect on repeat orders) |
| Sensitivity horizon | 2–4 weeks |

**Metric tree**
| Level | Metric | AARRR block | Owner | Link to the upper level | Proof status |
|---|---|---|---|---|---|

**OKR template**: Objective: [verb] + [what] + "so that" + [value]. KR1: [verb] [metric] from X to Z (Layer 2, leading, quarter). KR2 … Scoring: how the achievement of each KR is counted.

**Checklist**
- [ ] The NSM passes the eight criteria and is not revenue
- [ ] Every Layer 1 metric has an owner
- [ ] For a two-sided market, Layer 1 covers both sides and the "product" condition of the deal
- [ ] Links between levels have a proof status
- [ ] Team goals sit in metrics the team is able to measure within the period
- [ ] KRs are leading, sensitive, one layer below the Objective, with "from X to Z"
- [ ] For every metric, the formula, unit, period and source are specified

## Typical mistakes
- NSM = revenue; an NSM not linked to the moment of value; an NSM with an annual cycle.
- Too many metrics; broken links; confusion of levels (retention as an input).
- A proxy as an end in itself (average order value, conversion, time-to-market).
- Metrics without owners; links "by feel"; "two hits" taken for a correlation.
- Absolute and relative goals mixed without explanation; a relative metric degrades at scale, and the team is "punished".
- KRs without "from and to", on a lagging metric, unmanageable (MAU instead of campaign launches), too ambitious ("double revenue within a quarter"), not tied to the tree ("improve the design"), insensitive to the period (LTV).
- OKR formats differ between teams — nobody can read the other teams' goals.

## Questions that can change the decision
- Which user action means that they received value, and how often does it repeat?
- Do the interests of the different sides of the market (buyers and sellers) coincide in one NSM, or is a balance of metrics needed?
- Which links in the tree are proven, and which are a hypothesis that can be tested within a quarter?
- Which Layer 1 metric currently has no owner?
- Will the goal shift if the company's strategy changes (the NSM may change)?
- Does the chosen metric encourage behavior that harms long-term value?

## Related maps
[[M-strategy-growth]], [[M-goals-drivers-bets]], [[M-outcome-roadmap]], [[M-loyalty-metrics]], [[M-unit-economics]], [[M-traction-model]], [[M-quant-methods]], [[M-pmf-scaling]], [[M-ab-testing]], [[M-product-metrics]]
