---
id: M-strategy-growth
lang: en
title: Product strategy, growth types, and the structure of a strategy document
course: strategy
sources: ["EN mirror of the RU methodology card M-strategy-growth (knowledge/methods/strategy-growth.md); original sources are listed in the RU card"]
stages: [intake, options, strategy, validation]
tags: [strategy, growth, ansoff, cascading, unfair-advantage, product-led, sales-led, marketing-led, document-structure]
related: [M-external-environment, M-customers, M-competitors, M-goals-drivers-bets, M-landscapes, M-risks, M-outcome-roadmap, M-success-metrics, M-team, M-monetization, M-pmf-scaling]
---

# Product strategy, growth types, and the structure of a strategy document

## When to apply
When a product leader arrives with a vague request ("we need a growth strategy", "we need to grow faster", "what to do with the product for the next 2–3 years") and the agent needs to understand what exactly counts as strategy, which mandatory parts it consists of, and how to connect it to the company's business strategy. This card sets the frame for the whole final document: the other cards of the course (`M-external-environment` … `M-team`) fill in its sections.

## Essence
**Strategy** — a long-term plan for moving from state A (where we are now) to state B (where we want to arrive). It is not a vision, not a roadmap and not a backlog: a vision describes only point B without a plan; a roadmap and a backlog are tactical tools derived from the strategy.

**Five mandatory components of a product strategy**
| Component | What must be written | Check |
|---|---|---|
| Current state (A) | Key metrics now, market position, strengths and weaknesses | Every statement is a number with a source and a date |
| Target state (B) | Target metrics, horizon (usually 2–3 years), vision | The goal is expressed in metrics; for an early startup a "first sales" milestone is acceptable |
| External context | Market, trends, customers, competitors, opportunities and threats | Every threat/opportunity is rated by importance and probability |
| Internal context | Unfair advantage, resources, constraints | An advantage is something a competitor cannot copy quickly |
| Achievement plan | Streams, drivers, bets, phases, risks, team | The chain "goal → driver → bet → metric" is unbroken |

**Unfair advantage** — something you have that competitors cannot access: an audience on which you can launch new things at minimal acquisition cost; a culture of quality; distribution; unique data or technology; partnerships unavailable to a startup. To check a resource's durability — VRIO: value for the customer, rarity, difficulty of copying, the organization's ability to exploit the resource. Only "yes" on all four points yields a realized sustainable advantage.

**Four types of strategy metrics** (more detail — `M-success-metrics`)
| Type | What it shows | Examples | Who is accountable |
|---|---|---|---|
| Impact (business) | Efficiency of the company/direction, long horizon (3–5 years) | EBITDA, ROI, LTV/CAC, revenue per employee | top management |
| Outcome (business) | The result for the business and the user over the goal-setting period | revenue, deals/purchases, retention | product leader, team goals |
| Output (product) | An intermediate result, often a proxy for outcome | conversion to purchase, share of fulfilled orders, response speed | product manager |
| Input (product) | What the team influences directly | feature adoption, AOV, number of pushes per user | product manager, analyst |
A strategy that does not influence business metrics (impact/outcome) is useless; product metrics (output/input) are needed so the team can actually manage something.

**Cascading goals**: a top-level goal (e.g., revenue) is decomposed into goals of directions (marketing: DAU; product: retention; partners: new channels), then into clusters and teams. Business and product may choose different paths, but they must converge on the top-level metric. Without a cascade, desynchronization is possible: the business buys traffic while the product is not ready to convert it, or vice versa. Cascading is a **process, not a document**: in mature companies goals live in a shared tool where the link "company → direction → cluster → team" is visible top-down, rather than smeared across spreadsheets. A team's local goal may sit one level higher than usual (Outcome, not Input) if the team can prove the link in an A/B test — this is how the messenger team held its goal directly in deals. The link between metrics across cascade levels: company — Impact; direction — Outcome; cluster — Outcome/Output; team — Output/Input.

**Product types by their relation to earning money** — not every product must earn money directly, but every one must bring value to the business:
| Type | Purpose | Examples |
|---|---|---|
| Monetizable | direct earning | subscriptions, transactions, advertising |
| Lead-generating | attracting users for other products | free tools, freemium |
| Image-building | brand, employer brand, lobbying | corporate LLMs, social projects |
Hence a strategy check: for a non-monetizable product the goal is formulated not in revenue but in contribution to the business (leads, brand metrics, ecosystem retention).

**Business growth models around the product** — they define the product's role and the admissible hypotheses
| Model | Acquisition | Conversion | Retention | Product manager's focus | Examples from the course |
|---|---|---|---|---|---|
| Product-led | the product, virality, organic | fast time-to-value, "try first" | the user's "collection" (contacts, boards, data) | needs research, value, retention | Miro, messengers |
| Marketing-led | advertising, triggers, promotions | discounts, funnel conversion | CRM reminders | conversion to purchase, tools for marketing | marketplaces, e-commerce |
| Sales-led | a sales team hunting decision-makers (DMs) | demo, pilot, negotiations | success manager, regular value reports | features counted as mandatory for a deal; working from sales signals | B2B enterprise, 2GIS |
Most companies combine models (a classified-ads service: private users — product-led, sellers — marketing-led, car dealers — sales-led). The myth "real product managers exist only in product-led" is false.

**The link between business strategy and product strategy** — three options: the business inherits the product's strategy (product-led, technology companies); the product inherits and refines the business strategy (sales/marketing-led); a single strategy with a mature cascading culture. Good synergy: the business bets on product-led + a product with virality tooling (Miro). Bad: a bold business move (a free browser bundled with the OS) + a product violating platform standards (Internet Explorer 6).

**Growth types (optional, reference from the extended notes of session 2)** — the Ansoff matrix:
| Strategy | Product / market | Risk | Resources | Timeline benchmark |
|---|---|---|---|---|
| Penetration | existing / existing | low | low | 6–12 months |
| Market development | existing / new | medium | medium | 12–24 months |
| Product development | new / existing | medium | high | 12–18 months |
| Diversification | new / new | high | very high | 24–36 months |
The timelines and risk levels in the table are benchmarks from the notes, not measurements; in a strategy, confirm them with project data. Connection to the course's goal types (`M-goals-drivers-bets`): Growth/Activation/Monetization goals usually sit in the "penetration" zone; Strategic Expansion — "market development" or "diversification".

## Procedure
1. **Define the business growth model** (sales/marketing/product-led or a mix by segment) and the product lifecycle stage (PMF, growth, maturity, decline) — the admissible goal type depends on them.
2. **Fix A**: 5–10 metrics with a period and a source. What cannot be measured now — mark as a gap and add to the verification plan.
3. **Fix B**: target metrics over a 2–3 year horizon and intermediate points; specify which of them are business (impact/outcome) and which are product (output/input).
4. **Find out the goal of the level above** (director, cluster) and build the cascade: how the product's goal contributes to it. If the higher-level goal is unknown — that is a question for the product leader, not a reason to invent one.
5. **Assemble the external context** using the cards `M-external-environment`, `M-customers`, `M-competitors`; the **internal** one — via `M-landscapes` (marketing, technology, business model) and VRIO.
6. **Formulate growth options** (at least three, including "change nothing" and "close the direction/narrow the focus"); compare them by effect on B metrics, resources, risk, reversibility.
7. **Choose the strategy**: goals → streams → drivers → bets (`M-goals-drivers-bets`), then risks (`M-risks`), metrics (`M-success-metrics`), phases and timelines (`M-outcome-roadmap`), team (`M-team`).
8. **Make the strategy verifiable**: for every key statement, specify its type (fact with source / assumption / forecast); for every bet — a success criterion and a stop condition; for the whole strategy — a review date.

## Template / checklist
**Frame of the strategy document** (following the course example and the structure of the final work):
| # | Section | Content | Card |
|---|---|---|---|
| 1 | Current state analysis | Market: size, dynamics, trends, challenges, opportunities (with numbers and footnotes to sources) | `M-external-environment` |
| 1a | Competitors | Competitor groups, their advantages, growth strategy and promo mechanics, risks for us with a level (high/low) | `M-competitors` |
| 2 | Customers | Customer types by market sides (sellers / buyers): who they are, why they come, what difficulties they face, what holds them back from acting more often | `M-customers` |
| 3 | Strategic initiatives | 2–4 directions with a brief rationale derived from sections 1–2 (e.g.: the market is concentrated → not a head-on battle but a sustainable niche; traffic is comparable → grow via frequency with the current base) | `M-goals-drivers-bets` |
| 4 | Tactics | A table "initiative / focus / user needs / solutions" | `M-goals-drivers-bets` |
| 5 | Implementation plan | Teams per initiative, each one's expected contribution to the result, priority order, tie-in to seasons and dates | `M-outcome-roadmap`, `M-team` |
| 6 | Success metrics | KPIs in two blocks: business (sales volume, number of orders, transactions per user, active sellers) and product (A/B conversion, number of actions before an order, CSAT) | `M-success-metrics` |
| 7 | Risks and mitigation | 8 types, matrix, AATM, plan B | `M-risks` |
| 8 | Team and resources | Roles, hiring, stakeholders, dependencies | `M-team` |

In the course example the numbers are replaced with "X" and supplied with footnotes: in a working version every "X" must have a source; the agent does not insert invented values but marks gaps.

**Document maturity checklist**
- [ ] A and B are expressed in metrics with a period and a source
- [ ] The cascade from the business goal to the product goal is shown
- [ ] The unfair advantage is named and checked for copyability
- [ ] At least three options are analyzed, including doing nothing and closing the direction
- [ ] Every bet has a pain confirmed by data, a transition criterion and a stop signal
- [ ] Risks are described; the red zone has a plan B
- [ ] Resources and hiring are embedded in the timelines
- [ ] The review date and triggers for revisiting the strategy are specified

## Typical mistakes
- **Growth for growth's sake**: vanity metrics, "grow first, earn later", ignoring unit economics; treated by LTV > CAC and a path to profitability (`M-unit-economics`).
- **A roadmap or vision instead of strategy**: no current state in metrics and no path of transition.
- **Underestimating competitors** ("we have no competitors"), ignoring indirect ones and substitutes.
- **Premature scaling**: expenses grow faster than revenue, hiring before PMF, expansion without a model.
- **A goal in a proxy metric** (average order value, conversion as an end in itself): proxies are convenient to measure, but at scale they diverge from money and deals.
- **Strategy without a cascade**: the product optimizes a metric the business does not consider a goal (the team develops reviews while the company moves to a sales model without product display).
- **Strategy as a one-off document**: no cycle of "hypothesis → test → result → confirmed / revised (recast)". Two random hits are taken for a correlation.
- **Misplaced accountability**: the product manager picks metrics the team cannot statistically "move" (a small team cannot measure its impact on the whole company's revenue) — pick proxies whose link to outcome is proven.

## Questions that can change the decision
- What growth model does the business have (sales/marketing/product-led), and does it match what the product wants to do?
- What is the goal of the level above, and on which metric is it measured?
- What stage is the product at (searching for PMF, growth, maturity, decline)? If retention is low, scaling is "pouring water into a leaky bucket".
- Is there an unfair advantage that can be used quickly, or does it need to be built?
- What horizon and what constraints on resources, hiring and legal boundaries are already set?
- What happens if we do nothing: what value of the B metric results under the inertial scenario?
- Which assumptions of the strategy are testable within one quarter, and which only within a year?

## Related cards
[[M-external-environment]], [[M-customers]], [[M-competitors]], [[M-goals-drivers-bets]], [[M-landscapes]], [[M-risks]], [[M-outcome-roadmap]], [[M-success-metrics]], [[M-team]], [[M-pmf-scaling]], [[M-unit-economics]]
