---
id: M-skills-map
lang: en
title: Method map: the product lead's question → which cards and in what order
course: skills
sources: ["EN mirror of the RU methodology card M-skills-map (knowledge/methods/skills-map.md); original sources are listed in the RU card"]
stages: [intake, research, options, strategy, validation, after-decision]
tags: [navigation, route, skills-map, card-order, typical-tasks]
related: [M-strategy-growth, M-external-environment, M-customers, M-competitors, M-goals-drivers-bets, M-landscapes, M-risks, M-outcome-roadmap, M-success-metrics, M-team, M-product-context, M-jtbd, M-problem-design, M-solution-design, M-roadmap, M-mvp-pilots, M-pmf-scaling, M-product-communication, M-product-metrics, M-decision-daci, M-delivery, M-research-types, M-audience-research, M-brief-hypotheses, M-loyalty-metrics, M-in-depth-interviews, M-interview-analysis, M-quant-methods, M-usp, M-marketing-research, M-ux-frameworks, M-cjm, M-usability-testing, M-ux-heuristics, M-dogfooding, M-ux-backlog, M-workshops, M-ai-in-research, M-synthetic-respondents, M-design-thinking, M-market-sizing, M-unit-economics, M-traction-model, M-cannibalization, M-monetization, M-growth-frameworks, M-business-models, M-benchmarking, M-source-criticism, M-trends-scenarios]
---

# Method map: question → cards → order

## When to apply
A product lead asks a vague question ("the product is not growing", "the project needs defending", "should we enter the market"), and the agent must pick which cards to read and in what order. Start here if the route is not obvious; if the task is precise ("compute the TAM", "build the traction model") — go straight to the right card.

## Essence
Three principles of the route (from the product-navigator skills map):
1. First context and stage, then market and environment, then problem/solution, then goals and metrics, then modeling and economics, then plan and launch, then scaling; each topic can be revisited at any phase.
2. Market analysis and modeling apply at any stage of the product lifecycle; what changes is the depth (IDEA — top-down estimates, SCALE — full validation).
3. Every external number entering a calculation passes [[M-source-criticism]] and gets a grade of A–D; assumptions without a source are flagged explicitly.

The purpose of other cards is indicated by their id in the name; in case of divergence `knowledge/INDEX.md` takes priority.

### product-skills skills → cards
| Skill | Card |
|---|---|
| product-context-strategy | [[M-product-context]], [[M-strategy-growth]] |
| business-models | [[M-business-models]] |
| risk-management | [[M-risks]] |
| growth-frameworks | [[M-growth-frameworks]] |
| market-sizing | [[M-market-sizing]] |
| competitor-analysis | [[M-competitors]] |
| pestle-analysis | [[M-external-environment]] |
| benchmarking | [[M-benchmarking]] |
| trend-analysis | [[M-trends-scenarios]] |
| analytical-reports | [[M-source-criticism]] |
| problem-design | [[M-problem-design]] (+ [[M-research-types]], [[M-jtbd]]) |
| solution-design | [[M-solution-design]] |
| product-metrics | [[M-product-metrics]], [[M-success-metrics]] |
| growth-drivers, product-bets | [[M-goals-drivers-bets]] |
| traction-modeling, growth-effects, model-validation | [[M-traction-model]] |
| unit-economics | [[M-unit-economics]] |
| cannibalization | [[M-cannibalization]] |
| monetization-models, auction-monetization | [[M-monetization]] |
| roadmap-okr | [[M-outcome-roadmap]], [[M-roadmap]] |
| mvp-pilot-launch | [[M-mvp-pilots]] |
| team-org-structure | [[M-team]] |
| scaling-communication | [[M-pmf-scaling]], [[M-product-communication]] |

### The PM competency set (curriculum) → cards
The program's official competency matrix: 9 categories, each a set of behavioral indicators; self-assessment on a 0–5 scale (0 — cannot do it … 5 — can teach others) against the desired score and external assessment. Use as a second routing input: if the lead phrases the request through a competency ("learn to plan", "sharpen analytics") — follow the table row.

| Competency category | What the indicators are about | Cards |
|---|---|---|
| Structure, turning "the complex into the simple" | Structuring into tables/diagrams, task decomposition, a laconic status and risks, highlighting important facts, top-down vision | [[M-source-criticism]], [[M-product-communication]], [[M-problem-design]], [[M-solution-design]] |
| Management and communications | Well-argued positions, pausing in conflict, active listening, presenting with ideas/documents/prototypes, choosing the channel (meeting/email/chat) | [[M-product-communication]], [[M-decision-daci]], [[M-workshops]] |
| Planning and organizing work | Estimating resources/dependencies/risks, tracking the roadmap, handling change and escalation, organizing the team | [[M-roadmap]], [[M-delivery]], [[M-team]], [[M-risks]] |
| Discovery quality and speed | Decisions based on discovery data, reacting to the market, JTBD / User Story Mapping / CJM, research and innovation | [[M-research-types]], [[M-jtbd]], [[M-cjm]], [[M-problem-design]] |
| Analytics and metrics | Input→output, the physical meaning of data and its business impact, traction model, accounting for noise/seasonality, metric tree, dashboards and SQL | [[M-product-metrics]], [[M-traction-model]], [[M-quant-methods]] |
| Building and managing PnL | Product economics, LTV/CAC, payback, monetization decisions | [[M-unit-economics]], [[M-monetization]] |
| Improving customer experience | User first, collecting feedback, touchpoints and UX, CX indicators (CSAT, support tickets, churn), a deliberate MLP scope | [[M-cjm]], [[M-usability-testing]], [[M-loyalty-metrics]], [[M-ux-backlog]], [[M-mvp-pilots]] |
| Product management and strategy | Competitor analysis, the sprint backlog, presenting the vision, quarterly plans and the roadmap, end vision and USP, market analysis | [[M-competitors]], [[M-product-context]], [[M-strategy-growth]], [[M-outcome-roadmap]], [[M-usp]], [[M-market-sizing]] |
| ML models and AI in products | Launching products with ML/DS, communicating technical complexity to leadership, understanding programming principles and constraints, speaking the language of tech experts | Knowledge-base gap: no dedicated card; partially [[M-solution-design]] (feasibility, TDR questions) and [[M-ai-in-research]] (AI in research). On request — name the gap honestly and assemble hypotheses from adjacent cards |

The program's discipline map (context, not a route): module 1 — product management, data analysis, communications, CX; module 2 — corporate finance (for PnL); module 3 — growth strategies, business models and unit economics, market analysis, project management; year 2 — ML/AI in products, platform solutions. Competency goals follow the structure "competency → goal → what I will do → how I will know it is done → deadline".

## Procedure
1. Phrase the lead's question in one sentence and find the closest row in the table below; if none — assemble the route by process stages.
2. Ask 3–5 context questions (product and domain; the current task; what has been done; which data exists; B2B/B2C, market stage) — skip what is already known. This is [[M-product-context]] / [[M-brief-hypotheses]].
3. Walk the route's cards in order; each card yields an artifact that feeds the next one.
4. At each step record: input (data and their grade), output (artifact), open questions.
5. Before the conclusion — a verification step (sources, model, risks) and an explicit list of assumptions.
6. The criterion for moving to the next phase: the current phase's artifact is ready, key assumptions have a validation plan.

### Typical questions → route
| The lead's question | Cards in order |
|---|---|
| I want to launch a new product | [[M-product-context]] → [[M-market-sizing]] → [[M-competitors]] → [[M-business-models]] → [[M-growth-frameworks]] → [[M-problem-design]] → [[M-solution-design]] → [[M-mvp-pilots]] |
| Should we enter a market / segment | [[M-market-sizing]] → [[M-source-criticism]] → [[M-competitors]] → [[M-external-environment]] → [[M-business-models]] (Viability) → [[M-unit-economics]] → [[M-risks]] |
| A strategy for the year | [[M-product-context]] → [[M-strategy-growth]] → [[M-market-sizing]] → [[M-competitors]] → [[M-goals-drivers-bets]] → [[M-outcome-roadmap]] → [[M-risks]] |
| The product is not growing | [[M-product-metrics]] → [[M-goals-drivers-bets]] → [[M-problem-design]] → [[M-benchmarking]] → [[M-goals-drivers-bets]] (bets) → [[M-growth-frameworks]] |
| Defend a project before leadership | [[M-product-context]] → [[M-business-models]] → [[M-market-sizing]] → [[M-traction-model]] (with validation) → [[M-risks]] → [[M-product-communication]] |
| Planning the quarter | [[M-goals-drivers-bets]] → [[M-outcome-roadmap]] → [[M-team]] → [[M-risks]] |
| Understand competitors | [[M-competitors]] → [[M-landscapes]] → [[M-benchmarking]] → [[M-market-sizing]] |
| Choose metrics / NSM | [[M-product-metrics]] → [[M-success-metrics]] → [[M-goals-drivers-bets]] → [[M-benchmarking]] |
| Choose a growth framework | [[M-growth-frameworks]] → [[M-product-metrics]] → [[M-goals-drivers-bets]] |
| Preparing to scale | [[M-pmf-scaling]] → [[M-market-sizing]] → [[M-team]] → [[M-risks]] → [[M-outcome-roadmap]] |
| Build a traction model | [[M-traction-model]] → [[M-unit-economics]] → [[M-monetization]] → [[M-cannibalization]] (if there is a base) → [[M-benchmarking]] → [[M-source-criticism]] |
| Check / validate a model | [[M-traction-model]] (validation and effects sections) → [[M-benchmarking]] → [[M-source-criticism]] → [[M-cannibalization]] |
| Choose a monetization model or a price | [[M-monetization]] → [[M-unit-economics]] → [[M-traction-model]] → (competition for a resource) auction in [[M-monetization]] |
| Compute unit economics | [[M-unit-economics]] → [[M-benchmarking]] → [[M-traction-model]] |
| Launching a new product/plan on the existing base | [[M-cannibalization]] → [[M-unit-economics]] → [[M-traction-model]] → [[M-benchmarking]] |
| Business model: PLG or SLG, subscription or commission | [[M-business-models]] → [[M-monetization]] → [[M-growth-frameworks]] |
| Verify a number or an analytical report | [[M-source-criticism]] → [[M-benchmarking]] |
| Where is the market heading, which scenarios | [[M-external-environment]] → [[M-trends-scenarios]] → [[M-source-criticism]] → [[M-risks]] |
| Understand users and the problem (Discover) | [[M-research-types]] → [[M-audience-research]] / [[M-in-depth-interviews]] → [[M-interview-analysis]] → [[M-jtbd]] → [[M-problem-design]] |
| Choose and validate a solution (Define) | [[M-solution-design]] → [[M-mvp-pilots]] → [[M-success-metrics]] → [[M-risks]] |
| Improve UX | [[M-ux-frameworks]] → [[M-cjm]] → [[M-usability-testing]] / [[M-ux-heuristics]] → [[M-ux-backlog]] |
| Positioning and communication | [[M-usp]] → [[M-marketing-research]] → [[M-product-communication]] |
| Loyalty, NPS | [[M-loyalty-metrics]] → [[M-success-metrics]] |
| A dispute between stakeholders, a decision | [[M-decision-daci]] → [[M-workshops]] → [[M-risks]] |

### By the agent's process stages
| Stage | Cards |
|---|---|
| intake (briefing) | [[M-product-context]], [[M-brief-hypotheses]], [[M-strategy-growth]] |
| research | [[M-external-environment]], [[M-market-sizing]], [[M-competitors]], [[M-customers]], [[M-benchmarking]], [[M-source-criticism]], [[M-trends-scenarios]], [[M-research-types]] |
| options | [[M-problem-design]], [[M-solution-design]], [[M-business-models]], [[M-growth-frameworks]], [[M-monetization]], [[M-unit-economics]] |
| strategy | [[M-strategy-growth]], [[M-goals-drivers-bets]], [[M-traction-model]], [[M-outcome-roadmap]], [[M-cannibalization]] |
| validation | [[M-traction-model]] (validation), [[M-source-criticism]], [[M-benchmarking]], [[M-risks]], [[M-mvp-pilots]] |
| after-decision | [[M-roadmap]], [[M-delivery]], [[M-success-metrics]], [[M-product-metrics]], [[M-pmf-scaling]], [[M-product-communication]] |

### By product stage: what to analyze and model
| Stage | Market and environment | Modeling and economics |
|---|---|---|
| IDEA | [[M-market-sizing]], [[M-external-environment]], [[M-competitors]], [[M-business-models]], [[M-growth-frameworks]] | top-down from [[M-traction-model]], a first sketch of [[M-unit-economics]] |
| DISCOVERY | [[M-competitors]] (dogfooding), [[M-benchmarking]], [[M-trends-scenarios]] | [[M-unit-economics]] |
| MVP | [[M-benchmarking]] (goals), [[M-competitors]], [[M-risks]] | bottom-up from [[M-traction-model]], [[M-unit-economics]], [[M-monetization]] |
| GROWTH | [[M-market-sizing]] (the next segment), [[M-trends-scenarios]], [[M-goals-drivers-bets]] | the full [[M-traction-model]], effects, [[M-cannibalization]] |
| SCALE | [[M-market-sizing]] (new markets), [[M-external-environment]], [[M-pmf-scaling]] | model validation, [[M-monetization]] (including auction), [[M-unit-economics]] |

## Template / checklist
A route for answering the lead:
| # | Card | Why (question) | Input (data, grade A–D) | Output (artifact) | Status |
|---|---|---|---|---|---|
Pre-delivery checklist: the goal and horizon are fixed · the route explained to the user in 2–3 sentences · every external number with a source and grade · assumptions listed explicitly · at least one independent verification step (benchmark, triangulation, model validation, risks) · open questions that could change the conclusion are stated.

## Common mistakes
- Starting with modeling without the market and sources; or endlessly collecting market data without a decision.
- Taking all the cards in a row instead of the minimal route for the question.
- Not returning to an early card when the conclusion refutes the initial assumptions (the route is iterative).
- Mixing the growth model and the metrics framework: see [[M-growth-frameworks]] and [[M-product-metrics]].
- Computing UE and the model before choosing the business model and monetization ([[M-business-models]], [[M-monetization]]).

## Questions that can change the decision
- Which decision will the lead make at the end, and by what deadline?
- What is the product's stage (IDEA…SCALE) and is there operational data?
- Does the user have data that would replace external sources?
- Which assumptions are expensive to test, and is launching a pilot instead worthwhile ([[M-mvp-pilots]])?
- Is a defense before investors or an internal committee needed (then add [[M-source-criticism]] and model validation)?

## Related cards
[[M-product-context]], [[M-strategy-growth]], [[M-market-sizing]], [[M-traction-model]], [[M-unit-economics]], [[M-monetization]], [[M-business-models]], [[M-growth-frameworks]], [[M-benchmarking]], [[M-source-criticism]], [[M-trends-scenarios]], [[M-cannibalization]], [[M-risks]]
