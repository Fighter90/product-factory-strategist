---
id: M-success-metrics
lang: en
title: Success metrics — North Star Metric, metrics tree, AARRR and OKR
course: strategy
sources: ["EN mirror of the RU methodology card M-success-metrics (knowledge/methods/success-metrics.md); original sources are listed in the RU card"]
stages: [strategy, validation, after-decision]
tags: [nsm, north-star-metric, metrics-tree, aarrr, okr, leading-metrics, proxy-metrics, impact-outcome-output-input, key-results, leading-lagging]
related: [M-strategy-growth, M-goals-drivers-bets, M-outcome-roadmap, M-loyalty-metrics, M-unit-economics, M-traction-model, M-quant-methods, M-pmf-scaling, M-ab-testing, M-product-metrics]
---

# Success metrics — North Star Metric, metrics tree, AARRR and OKR

## When to apply
When you need to answer the questions "how will we know the strategy works", "which single metric all teams subordinate to", "how the quarter's goals relate to the long-term result". The output — an NSM checked against criteria, a metrics tree with owners and proven links, the period's objectives and key results, and a list of metrics with formulas, units and horizons.

## Essence
**Four levels of strategy metrics** (session 1) and the **pyramid** (session 5) describe one idea: from the long-term result down to what the team influences directly.
| Level | What it is | Horizon | Examples |
|---|---|---|---|
| NSM / Impact | long-term value and growth | years | EBITDA, ROI, LTV/CAC; the product's NSM |
| Outcome | the result of the goal-setting period (team goals) | quarter–year | revenue, deals, retention |
| Output | an intermediate result, a proxy | sprint–quarter | conversion, share of fulfilled orders, response speed |
| Input | what the team influences directly | day–sprint | adoption, number of pushes, AOV |
The team manages bottom-up: input and output → outcome → NSM. Relative metrics (percentages, conversions) are dangerous as goals: at scale, conversion falls (cold traffic) while deals grow. What you can "touch" is money, deals, GMV — conversion and average order value are merely attributes. NPS as a product metric is unreliable: it can decrease while the product improves (price increases).

**North Star Metric** — the key indicator that best predicts long-term success: it leads to revenue growth, reflects customer value, and measures real progress. Why it matters: it aligns teams around one goal, brings transparency to results, and supports customer-centricity. **Revenue is a bad NSM**: it pushes toward short-term squeezing, user burnout and churn.

**Eight NSM criteria**
| # | Question | Example / explanation |
|---|---|---|
| 1 | Matches the customer's moment of "success"? | a booking service — a booked trip; not "registrations" |
| 2 | Expresses value, not just sales? | "orders without complaints", "delivered in 15 minutes" is more precise than "orders" |
| 3 | Quantitatively measurable? | not "satisfaction" but the number of operations, frequency, time saved |
| 4 | Tied to time? | day/week/month; avoid annual intervals |
| 5 | Under control (minimal external factors)? | depends on the actions of the team and customers |
| 6 | NSM growth = business growth? | "number of downloaded reports" is bad (downloaded ten times because of errors); better "successfully downloaded reports per week" |
| 7 | Tied to the AARRR funnel (every team has an influence)? | growth of any stage moves the NSM |
| 8 | Changes often enough? | daily/weekly; the action repeats ≈3–4 times a month per user |
Examples of good NSMs from the course: MAU, listening time (an audio service), purchases per month, booked nights (accommodation booking), messages sent, answers to questions, rides per user per week (taxi), weekly active teams, DAU. For a delivery marketplace in the course: successful delivery deals.

**Metrics tree** — a logical hierarchy: input metrics (Layer 2 and below) influence focus metrics (Layer 1), and those influence the NSM. Rules:
- Layer 1 — 3–5 metrics that directly influence the NSM; each has an **owner** (a team or function). A metric without an owner degrades. A typical distribution: 3–5 teams per business, each "owning" its Layer 1 and formulating goals relative to its metric.
- **Two-sided marketplace: a deal requires all conditions simultaneously.** A successful delivery/booking happens only if (1) the buyer chose the service, (2) the seller connected it, (3) the listing/property has the service activated. Therefore Layer 1 must cover both sides of the market and the product — measuring only demand is not enough: demand without supply produces no deals.
- Links between levels are **proven** (A/B test, correlation, retrospective), not assumed: a 10% growth in sellers may yield +1–2% in deals — the link exists, the coefficient is low; links are not a simple sum/product but coefficients.
- Acquisition growth does not equal deal growth (irrelevant traffic is possible): quality metrics must grow along with it.
- The tree changes with the stage: launch — acquisition and activation; growth — scale; maturity — retention and revenue; optimization — efficiency. Two or three levels of depth is enough.
- Purpose: visualization, prioritization, monitoring. The tree is a map of levers; ranking is an example of a controllable lever (more traffic to listings with delivery).

**AARRR** — a frame for the blocks of the tree: Acquisition (registrations), Activation (aha-moment, free→paid conversion), Retention (retention, DAU/MAU), Referral (NPS, share the link), Revenue (LTV, AOV, CAC). An example Layer 2 for "buyers who chose delivery": share of listings with delivery, traffic to those listings, CTR in the delivery block, share of sellers who completed onboarding.

**OKR**: Objective (where we want to arrive, an outcome) + Key Results (how we will know we are moving) + scoring. Objective — verb + what we want + "so that" + what value we create; it sets direction, answers "why", follows from the team's mission, motivates, is understandable and memorable, and is tied to the company's strategy. Key Result — verb + value + "from X to Z"; achievable, ambitious, measurable, **sensitive** within the period (usually a quarter). KRs are formulated through **leading** metrics (an action, a process), not **lagging** ones (a result): "reduce calorie intake to X per day", not "reduce weight". **KRs sit one Layer below the Objective** (Objective on Layer 1 → KRs on Layer 2). The format is uniform across the company so anyone can read another team's goals.

Example: Objective — "increase the number of buyers who prefer delivery, so that the number of successful deals grows"; KR1 — the number of delivery categories from 3 to 6; KR2 — the share of traffic to delivery listings in ranking from 10% to 15%. An example KR on quality: "start factoring the seller's rating into recommendations, so that the CTR of the first five positions grows from 10% to 20%". The selection paradox: more recommendations may lower conversion — set a compound KR ("clicks grow, conversion to deal does not fall") or a KR on conversion.

**Proving the KR → Objective link** — the hardest part of OKR; four mechanisms in descending strength: an A/B test (the gold standard), correlation analysis on history, a counterfactual "before/after" comparison with a control group, a logical chain (allowed only for obvious links — "more categories → more choice → more buyers" — and still confirmed with data). Without a proven link, the KR may be fulfilled while the Objective is not. **Technical teams** set infrastructure KRs (e.g., "make parallel A/B tests possible", "start factoring the rating into recommendations") — their link to a business metric goes through enabling capabilities for product teams, and it must be stated explicitly.

### From goal to metrics: bets-as-evidence and the "expectation → fact" cycle (distilled from the data analysis course, sessions 2 and 4)
- **How metrics are "born":** goal → strategy and bets (how we will reach the goal) → data and metrics. Every bet must have its own **driver metric** with an obvious link to the goal's target metric; teams' target metrics are linked to the strategy's target metric. If the chosen metric does not explain movement toward the goal — the bet is revised, not the data. Prioritization of bets — RICE (Reach, Impact, Confidence, Effort).
- **The Leading / Lagging split** (a framework, session 4): leading metrics (input/output: an action and its proxy) are manageable and show progress quickly; lagging ones (outcome/NSM) confirm the result. KRs are formulated on leading metrics; NSM and period goals — on lagging ones. The mistake — ignoring leading metrics and "managing" only the outcome.
- **The trio for any scale:** target (the main criterion) + proxy (moves earlier, predicts the target) + counter (what must not be allowed). It works identically at the stream/strategy level, the product/project level and the initiative/feature level — only the horizon changes.
- **The expectation is fixed before launch:** for every initiative, "which metric will change and by how much" (magnitude + period) is written down in advance. After the experiment, fact is compared with expectation: a discrepancy is decomposed by drivers; "the metric is dancing" — first check the stability and seasonality of the metric itself ([[M-product-metrics]]: a drop can be normal).
- **The decision on the outcome — Scale / Iterate / Drop:** roll out with a confirmed effect and no harm to counter-metrics; refine and retest with a partial effect; abandon with no effect — always recording the conclusion in the knowledge base. Risks are checked with counter-metrics before scaling ("don't fix one thing by breaking another": liquidity redistribution, churn of payers).
- **Frameworks as scaffolding, not dogma:** AARRR sets the blocks of the tree (each team owns its stage), HEART — a slice of experience quality (Happiness/Engagement/Adoption/Retention/Task Success), One Metric That Matters — the focus of the period. A framework is adapted to the product, not copied.

## Procedure
1. **Define the product stage** and the business/product NSM (2–3 candidates); check each against the eight criteria; reject revenue.
2. **Build the tree** top-down: NSM → 3–5 Layer 1 metrics (by AARRR blocks or another logic) → Layer 2 → if needed Layer 3. Assign an owner to each Layer 1 metric.
3. **For each link, record the proof status**: proven by A/B / correlation / retrospective / hypothesis. Put hypotheses into the verification plan (`M-goals-drivers-bets`).
4. **Choose goal metrics** so the team can "move" them (measure them with statistical significance) within the period: if the outcome is too large (company revenue), pick an output/input with a proven link.
5. **Formulate the quarterly OKR**: first the team's NSM and its tree, then the drivers, then the Objective; KRs are leading, one layer below, "from X to Z".
6. **Fill in the passport of each metric**: definition, formula, unit, period, data source, owner, baseline, target, sensitivity horizon.
7. **Set up a review** (once a quarter, and off-schedule when the strategy changes): are the links confirmed, is any metric left without an owner.
8. Hand the metrics to `M-outcome-roadmap` (output for a pilot, outcome for validation and scaling).

## Template / checklist
**Metric passport**
| Field | Example |
|---|---|
| Name and level | share of orders delivered within ≤15 minutes (a team outcome) |
| Formula, units, period | orders delivered within ≤15 minutes / all orders, %, week |
| Source | delivery event in the warehouse |
| Owner | team X |
| Baseline → target → deadline | 62% → 70% in a quarter |
| Link type to the upper level | proven by A/B (effect on repeat orders) |
| Sensitivity horizon | 2–4 weeks |

**Metrics tree**
| Level | Metric | AARRR block | Owner | Link to the upper level | Proof status |
|---|---|---|---|---|---|

**OKR template**: Objective: [verb] + [what] + "so that" + [value]. KR1: [verb] [metric] from X to Z (Layer 2, leading, a quarter). KR2 … Scoring: how the achievement of each KR is counted.

**Checklist**
- [ ] The NSM passes the eight criteria and is not revenue
- [ ] Every Layer 1 metric has an owner
- [ ] For a two-sided market, Layer 1 covers both sides and the "product" condition of a deal
- [ ] Links between levels have a proof status
- [ ] Team goals sit in metrics the team can measure within the period
- [ ] KRs are leading, sensitive, one layer below the Objective, with "from X to Z"
- [ ] For every metric, the formula, unit, period and source are specified

## Typical mistakes
- NSM = revenue; an NSM not tied to the moment of value; an NSM with an annual cycle.
- Too many metrics; broken links; confusion of levels (retention as an input).
- A proxy as an end in itself (average order value, conversion, time-to-market).
- Metrics without owners; links "by feel"; "two hits" taken for a correlation.
- Goals in absolute and relative metrics mixed without explanation; a relative metric worsens at scale and the team gets "punished".
- KRs without "from-to", on a lagging metric, unmanageable (MAU instead of campaign launches), too ambitious ("double revenue in a quarter"), not tied to the tree ("improve the design"), insensitive to the period (LTV).
- OKR formats differ between teams — no one can read other teams' goals.

## Questions that can change the decision
- Which user action means the user received value, and how often does it repeat?
- Do the interests of different market sides (buyers and sellers) align in one NSM, or is a balance of metrics needed?
- Which links in the tree are proven, and which are hypotheses that can be tested within a quarter?
- Which Layer 1 metric currently has no owner?
- Will the goal shift if the company's strategy changes (the NSM may change)?
- Does the chosen metric reward behavior that harms long-term value?

## Related cards
[[M-strategy-growth]], [[M-goals-drivers-bets]], [[M-outcome-roadmap]], [[M-loyalty-metrics]], [[M-unit-economics]], [[M-traction-model]], [[M-quant-methods]], [[M-pmf-scaling]], [[M-ab-testing]], [[M-product-metrics]]
