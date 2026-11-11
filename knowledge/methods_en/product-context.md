---
id: M-product-context
lang: en
title: Product context — PM role, product lifecycle, perimeter and the strategic slice
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [intake, research, strategy]
tags: [product-context, pm-role, lifecycle, perimeter, stage-detection, strategy, pivot, market]
related: [M-strategy-growth, M-external-environment, M-customers, M-competitors, M-goals-drivers-bets, M-landscapes, M-jtbd, M-product-metrics, M-market-sizing, M-decision-daci, M-problem-design]
---

# Product context: PM role, product lifecycle, perimeter, strategic slice

## When to apply
At the start of any task ("our metric dropped", "we need a strategy", "what to do with the product"): before advising, you must pin down where the product is right now — stage, audience, market, goals, metrics, constraints, resources, responsibility perimeter. The card defines a minimal set of inputs and the rule "strategy = stage × context".

## Core idea

### 1. The PM role and the boundary of responsibility
- The PM is the link between strategy/business goals, technology and user problems; they define the strategy, formulate the value and work at the intersection of business, UX and technology.
- Two model modes: (a) "product leader" (large companies) — manages the process, not the execution: "I don't do it myself, but I am accountable"; (b) "generalist doer" (startups, part of the Russian market) — personally does analytics, prototypes, copy, launch; the boundaries are blurred.
- Product ≠ project: a product manager owns the product's lifecycle and value (retention, conversion, LTV, ARPU, NPS, DAU/MAU, delivery of product hypotheses); a project manager owns deadlines, budget, resources and scope (on-time delivery, budget adherence). The image of the outcome: a product that solves a real problem and grows, versus a project closed "on schedule".
- Product manager types with different emphases: B2C (funnels, UX, retention), B2B (customization, long sales cycles, communication), monetization (multi-monetization, business models), DS/ML (uncertainty, model metrics), Platform/SaaS (APIs, scale, internal clients).
- Org structures: product team leader (clear accountability, but the risk of isolation), cross-functional team (speed, but complex processes and role conflicts), matrix (resource flexibility, but dual reporting and slow decisions). It affects who actually makes the decision — see [[M-decision-daci]].

### 2. Product lifecycle
IDEA → DISCOVERY (only hypotheses exist, many interviews) → MVP (a minimal product; testing the core value and the risky hypotheses) → GROWTH/SCALE (value confirmed, users and revenue grow, focus on unit economics, channels, automation) → MAINTENANCE (growth has slowed, stability, retention, cost reduction) → DECLINE (churn, the niche burns out, replacement by a competitor).
- **Pivot** — a deliberate change of a key hypothesis while keeping part of the assets (team, technology, audience); one or several of the following change: audience, problem/value, monetization, functionality. It is based on metrics and feedback, not a "restart from scratch". Examples from the lecture: Burbn → Instagram (kept only photos — the thing people actually used), Tiny Speck → Slack (an internal tool became the product), a snowboard shop → Shopify (they built their own CMS — and realized that this was the product), the video-dating site "Tune In, Hook Up" → YouTube (users uploaded ordinary video, and the team didn't get in the way).
- **Closing a product** — not a failure but a deliberate exit when the hypothesis is not confirmed and the prospects are murky, when the market has changed and the value is outdated, when there is no growth trajectory. Knowing how to say "stop" is a PM skill (examples: Google Stadia — never reached critical mass, Apple Newton — the technology was ahead of its time, Amazon Dash Buttons — replaced by smartphones, ICQ — the format went stale after ~30 years of life).
- Double Diamond (Discover → Define → Develop → Deliver) and HADI cycles (Hypothesis, Action, Data, Insights) are frames for thinking, not instructions: a framework is a simplified model that helps you keep structure when you are drowning in uncertainty. Product thinking = common sense + structure + a critical perception of patterns. Four things must be checked: context (what is happening now with the product, the team, the market), adequacy (are the conclusions justified and the actions feasible), meaning (why this step, what is the goal), accountability (you can follow the template and still ruin the product).

### 3. Product perimeter (constraints and dependencies)
The perimeter can be: a single screen/feature; the whole funnel or part of it; a module inside an ecosystem (for example, ranking in search results); a separate business line. **Responsibility ≠ control**: the PM influences but does not manage every part; in ~98% of cases the product depends on other teams.
Perimeter artifacts: the base context (goal, segment, problems), a stakeholder map and a decision matrix (DACI), a list of dependencies (teams, APIs, backends), target metrics, a CJM, an impact map / value stream.

### 4. Base product context (minimal set of inputs)
| Component | What we record |
|---|---|
| Stage | Idea / Discovery / MVP / Growth / Scale / Maintenance / Decline |
| Audience | Segments, roles (user / buyer / decision maker; buyer / seller; courier/driver/partner; admin/moderator) |
| Market and segment | The overall market, the niche, competitors and "non-competitors" (habit, Excel, "doing nothing", the user's time) |
| Goals | Business and product goals for the period |
| Key metrics | NSM, growth, LTV, retention, etc. |
| Constraints | Technical, resource, legal |
| Resources | Team, budget, infrastructure |
| Key hypotheses | What the product's development rests on (mark them as hypotheses) |

### 5. How to determine the stage
Four signals: PMF (see [[M-pmf-scaling]]), regularity of use, unit economics, growth rate of the user base and feedback. Metrics by stage (from the lecture):
| Metric | What it shows | Typical stage |
|---|---|---|
| Task Success Rate | Does the user get their task done | Discovery / MVP |
| Activation rate | Did the user get the value | MVP |
| Retention D1/D7/D30 | Do users come back | MVP → Growth |
| DAU/MAU (stickiness) | Habit-forming, frequency | Growth / Scale |
| NPS / CSAT | Loyalty | Growth / Maintenance |
| LTV/CAC, ROMI | Sustainability of the economics, marketing efficiency | Growth / Scale |
| ARPU/ARPPU, GMV/revenue | Scale of monetization | Scale |
| Churn | Retention problems | Growth / Maintenance |
| % organic vs paid channel | Dependence on paid traffic | MVP / Growth |
| Bugs / release speed | Engineering maturity | MVP / Maintenance |

Example readings (training cases from the lecture, interpretation):
- D30 retention 22%, DAU/MAU 35%, LTV/CAC 2.5, NPS 52, MRR growing, churn 3%, releases every 2 weeks → Growth: the value exists, the economics are on the edge (LTV/CAC < 3 by the common benchmark), it doesn't quite reach Scale.
- D7 retention 6%, activation 25%, DAU/MAU 5%, CAC high and rising, organic ≈ 0, NPS 15, no revenue → MVP/Discovery without PMF; scaling is premature.
- D30 40%, NPS 60, revenue stable and growing slowly, the roadmap is about resilience and tech debt, MAU barely grows → Maintenance.

### 6. Market context and strategy
- Competitors ≠ analogues: the user compares you with a habit ("Excel", "doing nothing") and you compete for time (TikTok, YouTube).
- TAM/SAM/SOM: the typical mistake is counting "every iPhone owner" as the market; SOM is the opening battle; TAM without a go-to-market is a number for investors ([[M-market-sizing]]).
- SWOT is not a checkbox ("the product is convenient") but a tie to the market, the stage and the risks. The BCG matrix is for a portfolio of products ("question marks" — grow them or drop them, "cash cows" are not forever, "stars" require investment). Porter's five forces — for B2B/SaaS/platforms (competitors, new entrants, substitutes, suppliers, buyers).
- **Strategy = Stage × Context**; also Strategy = [Goals] + [Opportunities] − [Constraints]. The functions of strategy: perspective, team synchronicity, focus (against the "feature factory"). A good strategy builds on strengths, is framed as a set of sequential choices, and is coherent and logical. Models from the lecture: DHM (Gibson Biddle: Delight, Hard-to-copy, Margin), ecosystem strategy, Blue Ocean (differentiation and cost reduction at the same time).

| Stage | Market | Strategy focus |
|---|---|---|
| MVP | Empty market | Testing value, collecting signals |
| MVP | Occupied market | A niche, early users, a unique USP |
| Growth | Growing | Retention, scaling channels, unit economics |
| Growth | Competitive | Advantages, retention, NPS, positioning |
| Scale | Stable | Optimizing processes, growing LTV, new segments |
| Decline | Shrinking | A sunset plan, moving resources, finding niches |
| Decline | Transitional | Pivot: audience, monetization model, channel |

## Procedure
1. Write down **what is known** about the product per the "Base context" table. Mark every cell as: fact (source + date + period), hypothesis or forecast. Empty cells go to the list of questions.
2. Define the perimeter: what the product controls, what it only influences, which teams it depends on. Compile a list of dependencies and decision owners.
3. Determine the stage from ≥ 3 independent signals (retention, regularity, unit economics, base dynamics). If the signals contradict each other — state this explicitly and name the data that would resolve the contradiction.
4. Describe the market context: direct competitors, substitutes, habit/"doing nothing", competitors for time; a rough TAM/SAM/SOM; the market type (empty / occupied / growing / competitive / stable / shrinking / transitional).
5. Formulate the strategic focus from the "stage × market" pair (the table above) and list the constraints.
6. Extract the 3–5 key hypotheses the product's development rests on and, for each one, how to test it (hand it over to [[M-problem-design]], [[M-solution-design]]).
7. Explicitly write down what is NOT resolved and which inputs would change the stage/focus.

## Template / checklist
```
Product / perimeter: ___ (screen | funnel | module | business line)   Dependencies: ___
Stage: ___ (grounds: metric → value, period, source)   Confidence: high | medium | low
Audience and roles: ___   Market/competitors (incl. habit, "doing nothing"): ___
Goals of the period: ___   NSM/key metrics: ___   Constraints: ___   Resources: ___
Strategic focus (stage × market): ___
Hypotheses (not facts): 1) ___ — test: ___
Open questions / missing data: ___
```
Checklist: the stage is justified by metrics, not by the product's name · the period of every metric is stated · competitors include habit · SOM, not TAM, is used as the starting target · dependencies are named individually.

## Typical mistakes
- Determining the stage "by feel" or by the size of the company instead of by metrics (retention/activation/unit economics).
- One signal instead of a set: growing GMV with falling retention masks the absence of PMF ([[M-pmf-scaling]]).
- Counting "everyone potentially reachable" (TAM) as the market without linking it to channels and monetization.
- SWOT with no tie to the stage and the market; strategy as a list of features ("feature factory").
- Confusing the zone of responsibility with the zone of control: promising a metric outcome that other teams manage.
- Applying a framework (Double Diamond, HADI) as a ritual without checking whether the conclusions are adequate to the context.
- Ignoring the "close/pivot" option: every product strategy must contain an answer to when this is discussed.

## Questions that can change the decision
- On which metric and for which period is the stage confirmed? Is there seasonality or subsidies distorting it?
- Who makes the decision, and which dependencies (teams, APIs) could block the plan?
- Which competitors for time/habit are not accounted for? What does the user do "now" without the product?
- Which constraints (legal, technical, resource) are hard, and which are negotiable?
- Is there a portfolio context (BCG): is the product a "star", a "cash cow", a "question mark"?

## Related maps
[[M-strategy-growth]], [[M-external-environment]], [[M-customers]], [[M-competitors]], [[M-goals-drivers-bets]], [[M-landscapes]], [[M-jtbd]], [[M-product-metrics]], [[M-market-sizing]], [[M-decision-daci]], [[M-problem-design]], [[M-pmf-scaling]]
