---
id: M-product-context
lang: en
title: Product Context — the PM role, the product cycle, the perimeter, and the strategic snapshot
course: pm
sources: ["EN mirror of the RU methodology card M-product-context (knowledge/methods/product-context.md); original sources are listed in the RU card"]
stages: [intake, research, strategy]
tags: [context, stage, lifecycle, perimeter, double-diamond, market, strategy, pivot]
related: [M-strategy-growth, M-external-environment, M-customers, M-competitors, M-goals-drivers-bets, M-landscapes, M-jtbd, M-product-metrics, M-market-sizing, M-decision-daci, M-problem-design]
---

# Product context: the PM role, the product cycle, the perimeter, the strategic snapshot

## When to apply
At the start of any task ("our metric dropped", "we need a strategy", "what to do with the product"): before advising, you must fix where the product is right now — stage, audience, market, goals, metrics, constraints, resources, area of responsibility. The map defines the minimal set of inputs and the rule "strategy = stage × context".

## Essence

### 1. The PM role and the boundary of responsibility
- The PM is the link between strategy/business goals, technology, and user problems; defines the strategy, formulates the value, works at the junction of business, UX, and technology.
- Two model modes: (a) "product leader" (large companies) — manages the process, not the execution, "I don't do it, but I answer for it"; (b) "universal doer" (startups, part of the local market) — does analytics, prototypes, copy, and launches personally; the boundaries are blurred.
- Product ≠ project: a product manager manages the product lifecycle and value (retention, conversion, LTV, ARPU, NPS, DAU/MAU, the delivery of product hypotheses); a project manager — deadlines, budget, resources, scope (on-time delivery, budget adherence). The image of the result: a product that solves a real problem and grows, versus a project closed "on schedule".
- Product manager types with different emphases: B2C (funnels, UX, retention), B2B (customization, long sales cycles, communication), monetization (multi-monetization, business models), DS/ML (uncertainty, model metrics), Platform/SaaS (APIs, scale, internal clients).
- Org structures: the product-team lead (clear accountability, but the risk of isolation), a cross-functional team (speed, but complex processes and role conflicts), a matrix (resource flexibility, but dual subordination and slow decisions). It affects who really makes the decision — see [[M-decision-daci]].

### 2. The product lifecycle
IDEA → DISCOVERY (only hypotheses exist, many interviews) → MVP (a minimal product, testing the core value and the riskiest hypotheses) → GROWTH/SCALE (value confirmed, user and revenue growth, focus on unit economics, channels, automation) → MAINTENANCE (growth slowed, stability, retention, cost reduction) → DECLINE (churn, the niche burning out, replacement by a competitor).
- **Pivot** — a deliberate change of a key hypothesis while preserving part of the accumulated assets (team, technology, audience); one or several of these change: audience, problem/value, monetization, functionality. It is based on metrics and feedback, not "a restart from scratch". Examples from the lecture: Burbn → Instagram (kept only photos — what people actually used), Tiny Speck → Slack (an internal tool became the product), a snowboard shop → Shopify (built their own CMS — and realized that was the product), the video-dating "Tune In, Hook Up" → YouTube (users uploaded ordinary videos, and the team did not interfere).
- **Shutting a product down** — not a failure but a deliberate exit, when the hypothesis is not confirmed and the outlook is murky, the market has changed and the value is obsolete, there is no growth trajectory. Knowing how to say "stop" is a PM skill (examples: Google Stadia — never reached critical mass, Apple Newton — technology ahead of its time, Amazon Dash Buttons — smartphones replaced them, ICQ — format obsolescence after ~30 years of life).
- The Double Diamond (Discover → Define → Develop → Deliver) and HADI cycles (Hypothesis, Action, Data, Insights) are thinking frames, not instructions: a framework is a simplified model that helps keep structure when drowning in uncertainty. Product thinking = common sense + structure + a critical perception of patterns. Four things must be checked: the context (what is happening now with the product, team, market), the soundness (are the conclusions justified and the actions feasible), the meaning (why this step, what goal), the responsibility (you can follow the template and still ruin the product).

### 3. The product perimeter (constraints and dependencies)
A perimeter can be: one screen/feature; the whole funnel or part of it; a module inside an ecosystem (e.g., ranking in search results); a separate line of business. **Responsibility ≠ control**: the PM influences but does not command all the parts; in ~98% of cases the product depends on other teams.
Perimeter artifacts: the basic context (goal, segment, problems), a stakeholder map and a decision matrix (DACI), a dependency list (teams, APIs, backends), target metrics, a CJM, an impact map / value stream.

### 4. The product's basic context (the minimal set of inputs)
| Component | What we record |
|---|---|
| Stage | Idea / Discovery / MVP / Growth / Scale / Maintenance / Decline |
| Audience | Segments, roles (user / buyer / decision maker; buyer / seller; courier/driver/partner; admin/moderator) |
| Market and segment | The overall market, the niche, competitors and "non-competitors" (habit, Excel, "do nothing", the user's time) |
| Goals | The business and product goals for the period |
| Key metrics | NSM, growth, LTV, retention, etc. |
| Constraints | Technical, resource, legal |
| Resources | Team, budget, infrastructure |
| Main hypotheses | What the product's development rests on (mark them as hypotheses) |

### 5. How to determine the stage
Four signals: PMF (see [[M-pmf-scaling]]), the regularity of use, unit economics, the base-growth velocity and feedback. Metrics by stage (from the lecture):
| Metric | What it shows | Typical stage |
|---|---|---|
| Task Success Rate | Does the user accomplish their task | Discovery / MVP |
| Activation rate | Did they get the value | MVP |
| Retention D1/D7/D30 | Do they come back | MVP → Growth |
| DAU/MAU (stickiness) | Habit strength, frequency | Growth / Scale |
| NPS / CSAT | Loyalty | Growth / Maintenance |
| LTV/CAC, ROMI | Economics sustainability, marketing efficiency | Growth / Scale |
| ARPU/ARPPU, GMV/revenue | The scale of monetization | Scale |
| Churn | Retention problems | Growth / Maintenance |
| % organic vs paid channel | Dependence on paid traffic | MVP / Growth |
| Bugs / release velocity | Engineering maturity | MVP / Maintenance |

Reading examples (lecture teaching cases, interpretation):
- D30 retention 22%, DAU/MAU 35%, LTV/CAC 2.5, NPS 52, MRR growing, churn 3%, releases every 2 weeks → Growth: value exists, the economics are on the edge (LTV/CAC < 3 by the common benchmark), not yet Scale.
- D7 retention 6%, activation 25%, DAU/MAU 5%, CAC high and rising, organic ≈ 0, NPS 15, no revenue → MVP/Discovery without PMF; too early to scale.
- D30 40%, NPS 60, revenue stable and growing slowly, the roadmap is about resilience and tech debt, MAU barely grows → Maintenance.

### 6. Market context and strategy
- Competitors ≠ analogs: the user compares against habit ("Excel", "do nothing") and competes for time (TikTok, YouTube).
- TAM/SAM/SOM: the typical mistake is counting "every iPhone owner" as the market; SOM is the opening battle; TAM without go-to-market is a number for investors ([[M-market-sizing]]).
- SWOT — not a checkbox ("the product is convenient") but a tie to the market, the stage, and the risks. The BCG matrix — for a product portfolio ("question marks" — grow or kill, "cash cows" are not forever, "stars" need investment). Porter's five forces — for B2B/SaaS/platforms (competitors, entrants, substitutes, suppliers, buyers).
- **Strategy = Stage × Context**; also Strategy = [Goals] + [Opportunities] − [Constraints]. The functions of strategy: perspective, team alignment, focus (against the "feature factory"). A good strategy builds on strengths, is framed as a set of consecutive choices, is agreed, and is logical. Models from the lecture: DHM (Gibson Biddle: Delight, Hard-to-copy, Margin), ecosystem strategy, Blue Ocean (differentiation and lower costs at once).

| Stage | Market | Strategy focus |
|---|---|---|
| MVP | An empty market | Testing value, collecting signals |
| MVP | An occupied market | A niche, early users, a unique USP |
| Growth | Growing | Retention, scaling channels, unit economics |
| Growth | Competitive | Advantages, retention, NPS, positioning |
| Scale | Stable | Process optimization, LTV growth, new segments |
| Decline | Shrinking | A sunset plan, resource transfer, niche search |
| Decline | Transitional | Pivot: audience, monetization model, channel |

## Procedure
1. Write down **what is known** about the product using the "Basic context" table. Mark each cell: a fact (source + date + period), a hypothesis, or a forecast. Empty cells go to the open-questions list.
2. Define the perimeter: what the product controls, what it only influences, which teams it depends on. Build the dependency list and the decision owners.
3. Determine the stage from ≥ 3 independent signals (retention, regularity, unit economics, base dynamics). If the signals contradict each other — say so explicitly and name which data will resolve the contradiction.
4. Describe the market context: direct competitors, substitutes, habit/"do nothing", competitors for time; a rough TAM/SAM/SOM; the market type (empty / occupied / growing / competitive / stable / shrinking / transitional).
5. Formulate the strategic focus from the "stage × market" pair (the table above) and list the constraints.
6. Extract the 3–5 key hypotheses the development rests on and, for each, how to test it (hand over to [[M-problem-design]], [[M-solution-design]]).
7. Explicitly record what is NOT decided and which input data would change the stage/focus.

## Template / checklist
```
Product / perimeter: ___ (screen | funnel | module | line of business)   Dependencies: ___
Stage: ___ (basis: metric → value, period, source)   Confidence: high | medium | low
Audience and roles: ___   Market/competitors (incl. habit, "do nothing"): ___
Goals of the period: ___   NSM/key metrics: ___   Constraints: ___   Resources: ___
Strategic focus (stage × market): ___
Hypotheses (not facts): 1) ___ — verification: ___
Open questions / missing data: ___
```
Checklist: the stage is justified by metrics, not by the product's name · the period of each metric is stated · competitors include habit · SOM, not TAM, is used as the starting target · the dependencies are named by name.

## Typical mistakes
- Determining the stage "by feel" or by company size, not by metrics (retention/activation/unit economics).
- One signal instead of a set: GMV growth with falling retention masks the absence of PMF ([[M-pmf-scaling]]).
- Counting "all potential users" (TAM) as the market and not linking it to channels and monetization.
- SWOT without a tie to the stage and the market; strategy as a feature list ("feature factory").
- Confusing the zone of responsibility and the zone of control: promising a metric outcome that other teams manage.
- Applying a framework (Double Diamond, HADI) as a ritual without checking whether the conclusions fit the context.
- Ignoring the "shut down / pivot" option: every product strategy must answer under what conditions this is discussed.

## Questions that could change the decision
- On which metric and over which period is the stage confirmed? Is there seasonality or subsidies distorting it?
- Who makes the decision, and which dependencies (teams, APIs) can block the plan?
- Which competitors for time/habit are not accounted for? What does the user do "now" without the product?
- Which constraints (legal, technical, resource) are hard, and which are negotiable?
- Is there a portfolio context (BCG): is the product a "star", a "cash cow", a "question mark"?

## Related maps
[[M-strategy-growth]], [[M-external-environment]], [[M-customers]], [[M-competitors]], [[M-goals-drivers-bets]], [[M-landscapes]], [[M-jtbd]], [[M-product-metrics]], [[M-market-sizing]], [[M-decision-daci]], [[M-problem-design]], [[M-pmf-scaling]]
