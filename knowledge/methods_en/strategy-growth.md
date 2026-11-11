---
id: M-strategy-growth
lang: en
title: Product strategy, growth types and the structure of a strategy document
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [intake, options, strategy, validation]
tags: [product-strategy, growth, ansoff, cascading, unfair-advantage, product-led, sales-led, marketing-led, document-structure]
related: [M-external-environment, M-customers, M-competitors, M-goals-drivers-bets, M-landscapes, M-risks, M-outcome-roadmap, M-success-metrics, M-team, M-monetization, M-pmf-scaling]
---

# Product strategy, growth types and the structure of a strategy document

## When to apply
When a product lead arrives with a vague request ("we need a growth strategy", "we must grow faster", "what to do with the product for the next 2–3 years") and the agent needs to understand what exactly counts as a strategy, which mandatory parts it consists of, and how to link it to the company's business strategy. The card sets the frame for the whole final document: the other course cards (`M-external-environment` … `M-team`) fill in its sections.

## Core idea
**Strategy** — a long-term plan for moving from state A (where we are now) to state B (where we want to arrive). It is not a vision, not a roadmap and not a backlog: a vision describes only point B without a plan; a roadmap and a backlog are tactical instruments derived from the strategy.

**Five mandatory components of a product strategy**
| Component | What must be written | Check |
|---|---|---|
| Current state (A) | Key metrics right now, market position, strengths and weaknesses | Every claim is a number with a source and a date |
| Target state (B) | Target metrics, a horizon (usually 2–3 years), the vision | The goal is expressed in metrics; for an early startup a "first sales" milestone is acceptable |
| External context | Market, trends, clients, competitors, opportunities and threats | Every threat/opportunity is scored by importance and probability |
| Internal context | Unfair advantage, resources, constraints | An advantage is something a competitor cannot copy quickly |
| Plan of achievement | Streams, drivers, bets, phases, risks, team | The chain "goal → driver → bet → metric" is not broken |

**Unfair advantage** — something you have that is unavailable to competitors: an audience on which new launches can run at minimal acquisition cost; a culture of quality; distribution; unique data or technology; partnerships a startup cannot get. To check the resource's durability — VRIO: value for the client, rarity, difficulty of copying, and the organization's ability to exploit the resource. Only "yes" on all four points gives a realized, durable advantage.

**Four types of strategy metrics** (details in `M-success-metrics`)
| Type | What it shows | Examples | Who owns it |
|---|---|---|---|
| Impact (business) | Company/direction efficiency, a long horizon (3–5 years) | EBITDA, ROI, LTV/CAC, revenue per employee | top management |
| Outcome (business) | The result for the business and the user over the goal-setting period | revenue, deals/purchases, retention | product lead, team goals |
| Output (product) | An intermediate result, often a proxy for outcome | purchase conversion, share of bought-out orders, response speed | product manager |
| Input (product) | What the team influences directly | feature adoption, AOV, pushes per user | product manager, analyst |
A strategy that does not move business metrics (impact/outcome) is useless; product metrics (output/input) are needed so that the team can steer.

**Cascading goals**: a top-level goal (for example, revenue) decomposes into direction goals (marketing: DAU; product: retention; partners: new channels), then into clusters and teams. Business and product are entitled to choose different paths, but they must converge in the top-level metric. Without a cascade a desync is possible: the business buys traffic while the product is not ready to convert it, or vice versa. Cascading is a **process, not a document**: in mature companies goals live in a shared tool, where the link "company → direction → cluster → team" is visible top-down rather than smeared across spreadsheets. A team's local goal may sit one level higher than usual (Outcome, not Input) if the team can prove the link in an A/B test — that is how the messenger team held its goal directly in deals. The linkage of metrics across cascade levels: company — Impact; direction — Outcome; cluster — Outcome/Output; team — Output/Input.

**Product types by relation to earning money** — not every product must earn money directly, but every one must bring the business value:
| Type | Purpose | Examples |
|---|---|---|
| Monetizable | direct earning | subscriptions, transactions, advertising |
| Lead-generating | attracting users for other products | free tools, freemium |
| Brand-building | brand, HR brand, lobbying | corporate LLMs, social-impact projects |
Hence a strategy check: for a non-monetizable product the goal is formulated not in revenue but in contribution to the business (leads, brand metrics, ecosystem retention).

**Business growth models around the product** — they define the product's role and the admissible hypotheses
| Model | Acquisition | Conversion | Retention | Product manager's focus | Course examples |
|---|---|---|---|---|---|
| Product-led | the product, virality, organic traffic | fast time-to-value, "try first" | the user's "collection" (contacts, boards, data) | needs research, value, retention | Miro, messengers |
| Marketing-led | advertising, triggers, promotions | discounts, funnel conversion | CRM reminders | purchase conversion, tools for marketing | marketplaces, e-commerce |
| Sales-led | a sales team hunting for decision makers (DMs) | demo, pilot, negotiations | a success manager, regular value reports | features considered mandatory for a deal; working off sales signals | B2B enterprise, 2GIS |
Most companies combine models (a classifieds site: private users — product-led, sellers — marketing-led, car dealers — sales-led). The myth "real product managers exist only in product-led" is false.

**Linking business strategy and product strategy** — three variants: the business inherits the product's strategy (product-led, technology companies); the product inherits and refines the business's strategy (sales/marketing-led); a single shared strategy with a mature cascading culture. Good synergy: the business bets on product-led + a product with virality tools (Miro). Bad: a bold business move (a free browser bundled with the OS) + a product violating platform standards (Internet Explorer 6).

**Growth types (optional, reference from the extended notes of session 2)** — the Ansoff matrix:
| Strategy | Product / market | Risk | Resources | Timeline benchmark |
|---|---|---|---|---|
| Penetration | existing / existing | low | low | 6–12 months |
| Market development | existing / new | medium | medium | 12–24 months |
| Product development | new / existing | medium | high | 12–18 months |
| Diversification | new / new | high | very high | 24–36 months |
The timelines and risk levels in the table are benchmarks from the notes, not measurements; in a strategy, confirm them with the project's own data. Link to the course's goal types (`M-goals-drivers-bets`): Growth/Activation/Monetization goals usually fall in the "penetration" zone; Strategic Expansion — "market development" or "diversification".

## Procedure
1. **Determine the business's growth model** (sales/marketing/product-led, or a mix by segments) and the product's lifecycle stage (PMF search, growth, maturity, decline) — the admissible goal type depends on them.
2. **Fix A**: 5–10 metrics with a period and a source. Whatever cannot be measured right now — mark as a gap and add to the validation plan.
3. **Fix B**: target metrics on a 2–3 year horizon and intermediate checkpoints; specify which of them are business (impact/outcome) and which are product (output/input).
4. **Find out the goal of the level above** (a director, a cluster) and build the cascade: how the product's goal contributes to it. If the higher-level goal is unknown — that is a question for the product lead, not a reason to invent one.
5. **Collect the external context** using the cards `M-external-environment`, `M-customers`, `M-competitors`; the **internal** one — using `M-landscapes` (marketing, technology, business model) and VRIO.
6. **Formulate growth options** (at least three, including "change nothing" and "close the direction / narrow the focus"); compare them by effect on the B metrics, resources, risk, and reversibility.
7. **Choose the strategy**: goals → streams → drivers → bets (`M-goals-drivers-bets`), then risks (`M-risks`), metrics (`M-success-metrics`), phases and timing (`M-outcome-roadmap`), team (`M-team`).
8. **Make the strategy checkable**: for every key claim specify its type (fact with a source / assumption / forecast), for every bet — a success criterion and a stop condition, for the strategy as a whole — a review date.

## Template / checklist
**Strategy document skeleton** (after the course example and the final-work structure):
| # | Section | Content | Card |
|---|---|---|---|
| 1 | Current-state analysis | Market: size, dynamics, trends, challenges, opportunities (with numbers and footnotes to sources) | `M-external-environment` |
| 1a | Competitors | Competitor groups, their advantages, growth strategy and promo mechanics, risks to us with a level (high/low) | `M-competitors` |
| 2 | Clients | Client types by market side (sellers / buyers): who they are, why they come, what difficulties they face, what holds them back from acting more often | `M-customers` |
| 3 | Strategic initiatives | 2–4 directions with brief rationale derived from sections 1–2 (e.g.: the market is concentrated → not a frontal battle but a defensible niche; traffic is comparable → grow through frequency on the current base) | `M-goals-drivers-bets` |
| 4 | Tactics | A table "initiative / focus / user needs / solutions" | `M-goals-drivers-bets` |
| 5 | Implementation plan | Teams per initiative, each one's expected contribution to the result, priority order, ties to seasons and dates | `M-outcome-roadmap`, `M-team` |
| 6 | Success metrics | KPIs in two blocks: business (sales volume, number of orders, transactions per user, active sellers) and product (conversion per A/B, number of actions to an order, CSAT) | `M-success-metrics` |
| 7 | Risks and mitigation | 8 types, matrix, AATM, plan B | `M-risks` |
| 8 | Team and resources | Roles, hiring, stakeholders, dependencies | `M-team` |

In the course example the numbers are replaced with "X" and supplied with footnotes: in a working version every "X" must have a source; the agent does not insert made-up values but marks gaps.

**Document maturity checklist**
- [ ] A and B are expressed in metrics with a period and a source
- [ ] The cascade from the business goal to the product goal is shown
- [ ] The unfair advantage is named and checked for copyability
- [ ] At least three options are analyzed, including doing nothing and closing the direction
- [ ] Every bet has a pain backed by data, a transition criterion and a stop signal
- [ ] Risks are described; the red zone has a plan B
- [ ] Resources and hiring are built into the timelines
- [ ] The review date and triggers for revisiting the strategy are specified

## Typical mistakes
- **Growth for growth's sake**: vanity metrics, "grow first, earn later", ignoring unit economics; cured by LTV > CAC and a path to profitability (`M-unit-economics`).
- **A roadmap or a vision instead of a strategy**: no current state in metrics and no transition path.
- **Underestimating competitors** ("we have no competitors"), ignoring indirect competitors and substitutes.
- **Premature scaling**: costs grow faster than revenue, hiring before PMF, expansion without a model.
- **A goal in a proxy metric** (average order value, conversion as an end in itself): proxies are convenient to measure, but at scale they diverge from money and deals.
- **A strategy without a cascade**: the product optimizes a metric the business does not count as a goal (the team develops reviews while the company moves to a sales model without showing the item).
- **A strategy as a one-off document**: no "hypothesis → test → result → confirmed / revised (recast)" cycle. Two random hits are taken for a correlation.
- **Misplaced responsibility**: a product manager picks metrics the team cannot statistically "light up" (a small team cannot measure the effect on the whole company's revenue) — choose proxies whose link to outcome has been proven.

## Questions that can change the decision
- What is the business's growth model (sales/marketing/product-led), and does it match what the product wants to do?
- What is the goal of the level above, and on which metric is it measured?
- What stage is the product at (PMF search, growth, maturity, decline)? If retention is low, scaling is "pouring water into a leaky bucket".
- Is there an unfair advantage that can be used quickly, or does it need to be built first?
- What horizon and which constraints on resources, hiring and legal boundaries are already set?
- What happens if we do nothing: what value of the B metric results from the inertial scenario?
- Which assumptions of the strategy can be validated within a single quarter, and which only within a year?

## Related maps
[[M-external-environment]], [[M-customers]], [[M-competitors]], [[M-goals-drivers-bets]], [[M-landscapes]], [[M-risks]], [[M-outcome-roadmap]], [[M-success-metrics]], [[M-team]], [[M-pmf-scaling]], [[M-unit-economics]]
