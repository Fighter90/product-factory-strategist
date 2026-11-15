---
id: M-goals-drivers-bets
lang: en
title: Goals, growth drivers, streams, focus areas, product bets and the initiative portfolio
course: strategy
sources: ["EN mirror of the RU methodology card M-goals-drivers-bets (knowledge/methods/goals-drivers-bets.md); original sources are listed in the RU card"]
stages: [options, strategy, validation]
tags: [goals, smart, growth-drivers, streams, focus-areas, bets, big-bets, portfolio, impact-effort, pain, jtbd, custdev]
related: [M-strategy-growth, M-customers, M-competitors, M-success-metrics, M-outcome-roadmap, M-risks, M-jtbd, M-problem-design, M-solution-design, M-mvp-pilots, M-brief-hypotheses, M-quant-methods]
---

# Goals, growth drivers, streams, focus areas, product bets and the initiative portfolio

## When to apply
When "we want to grow" must become a concrete hierarchy: what exactly we change (the goal), through which levers (drivers), in which large direction (a stream), what we concentrate on this period (focus), which big hypothesis we bet on (a bet) and by which actions (initiatives) we check it. The map protects against the frequent mistake — jumping straight to features.

## Essence
**The hierarchy of decisions** (from strategy to operations): goal → streams → drivers → focuses → bets → initiatives → experiments. Strategic level: goal, streams, drivers; tactical: focuses and bets; operational: initiatives and experiments.

**A goal is not a metric and not an initiative.** The goal — what changes in the system (D7 retention +5 pp); the metric — how we measure; the initiative — what we do. "Launch a referral program" is an initiative, not a goal.

**Six types of goals**
| Type | Example | Key question |
|---|---|---|
| Growth | registrations +25% | how to attract more people |
| Activation & Retention | activation 40% → 55%; D30 12% → 18% | how to bring users to value and keep them |
| Monetization | ARPU +15% | how to earn more from current users |
| Cost & Efficiency | cost-to-serve −12% | how to spend less |
| Supply / Quality / Trust | active sellers +20% | how to improve the offer and trust |
| Strategic Expansion | a new SMB segment, 10% of revenue | where to expand |
A technical "goal" (upgrade the system version) is a task; the real goal is to preserve retention while reducing downtime risk.

**How to choose a goal**: *Strategy × System constraint × Controllability = the priority goal.*
- Strategy context and lifecycle stage: PMF → activation/retention; growth → growth/supply; maturity → monetization/efficiency; decline → harvest (profit), retaining the core or a pivot.
- Diagnosis on data: where is the funnel's bottleneck, which metric limits growth, is there potential (benchmarks, market, competitors).
- Controllability: can we influence it and is the effect visible within the period's horizon.
If one factor is missing: no controllability → the goal is unreachable; no constraint → it is unclear what to optimize (redo the diagnosis); no link to strategy → we are optimizing the wrong thing. Scaling with low retention is "pouring water into a leaky bucket".

**SMART for product goals**: specificity, measurability (metric, baseline, target value), attainability, relevance to strategy, a deadline. Example: "Raise D7 retention from 22% to 30% within 3 months".

**A growth driver** — a source of change in the key metric, not a feature. It is worded as a change: "cut drop-off at the payment step by 20 pp" — a driver; "add Apple Pay" — an initiative; "a redesign" — a tool, not a driver. Wording tests: if you can ask "why?" — it is an initiative; if the implementation method is the only one — it is an initiative (a real driver has at least two paths).
- Product drivers: activation and key scenarios, search and recommendations, data and content quality, friction removal.
- Business drivers: prices, promotions, acquisition channels, partnerships.
- Antipattern: treating a supply shortage with a redesign.

**A metric decomposes into a product of drivers.** To find the levers, outcome/output is factored into multipliers: `orders = active users × conversion to order × order frequency per user`; each multiplier is its own output/input driver with its own way of influence. The search logic: pick the multiplier with the biggest gap against a benchmark or competitor → for that multiplier find the segment and the point of failure → formulate 2–3 drivers. A driver usually lives at the output or input level of the pyramid: outcome and NSM are not moved "with a button".

**Three levels that get confused** (each next one is more concrete):
| Level | Wording | Example |
|---|---|---|
| Driver | a change in a metric | "conversion to first order 15% → 25%" |
| Bet | an "if… then…" hypothesis about a mechanism | "if we simplify the order form, conversion will rise" |
| Initiative | a concrete action with a deadline | "cut the form from 5 fields to 2" |

**The driver search algorithm (5 steps)**: goal → decompose the funnel and segment (new/returning, paying/not, devices) → quantitative data in the problem segment (conversions, failure points, time to the key event) → qualitative research (interviews, complaints, session recordings, usability tests) → 2–3 drivers. Drivers are based on facts, not on "it seems". A driver sits at the output or input level of the pyramid (`M-success-metrics`); retention cannot be managed directly.

**A growth stream** — a systemic direction uniting several drivers around one large goal ("Improving activation": the first step, guided actions, simpler sign-up). A stream gives teams focus for at least a quarter and gives the future roadmap its structure.

**A focus** — the direction of effort concentration inside a stream for a period ("cut time-to-first-value"). Five types: growth (acquisition, activation, viral loop), retention, monetization, UX improvements, platform/technical. Choosing 3–5 focuses: rely on goals; look at funnels and segments; look for the bottleneck (the biggest drop, not the most interesting thing); check resources; estimate the impact on metrics. No more focuses than teams (1–2 per team); the same rule for streams — the number of streams ≤ the number of teams, and resources are allocated per stream immediately (how many developers/analysts), otherwise "3 streams" become a wish-list. The focus's justification to leadership is built from data ("drop-off is 40% at step 3; if we cut it to 20% — +X conversions"), not from fashion. A focus is not forever: a review each quarter; a stream may stay, the focus within it changes. The antipattern is a "pretty focus" (AI recommendations with no bottleneck).

**A bet** — a large hypothesis that substantially moves the key metric if it succeeds. Always: linked to a focus, has a confirmed pain, describes the mechanism of influence, is measurable. Wording: "if we do X (a change), then metric Y will change by Z within period T". Six questions of a bet: inside the focus? is there a concrete pain? is the pain confirmed by data? is the cause-effect link clear? is there a measurable target effect? are constraints and resources clear?

**Pain validation** (otherwise the hypothesis is an illusion)
| Tool | What it checks | Signals |
|---|---|---|
| JTBD | what the person is trying to do, what gets in the way, what progress they want | the product is "not hired" → there is unaddressed pain |
| CustDev | the reality of the pain | frequency of the situation, emotion, a high cost of inaction, the presence of a workaround (a crutch, Excel, YouTube instead of the app) |
| Behavioral data | scale | long time on a step, high drop-off, repeated actions (click → cancel → again), attempts to bypass limits |
| Monetary confirmation | the strongest | pays or is ready to pay |
The pain pyramid: blocking > significant > irritation > wish list. Work with the first two. Rule: confirmed ≥3 of 5 indicators (frequency, scale, emotion, workaround, willingness to pay) — the pain is real, otherwise it is more likely a wish. False signals: "if you add X, I would definitely use it", one loud complaint, a request from a single large client, correlation instead of causality (those who created a project retain better — reverse causality is possible).

**The initiative portfolio**: a system of big, mid and small bets. The target balance: 1–2 big bets, 3–5 mid bets, 5–10 small bets. The Impact/Effort matrix: high impact at low effort — do immediately (rare); high/high — a big bet; low/low — quick checks; low/high — decline. Score impact with data, effort with engineers (t-shirt, planning poker); add confidence (ICE = Impact × Confidence × Ease); at low confidence — research first. Signs the matrix is not working: every initiative is "high impact, low effort" (the scoring is poor), no data for impact (a discovery phase is needed), the team cannot estimate effort (a technical spike is needed), all initiatives are of one type. Antipatterns: only small tweaks, only big bets, only UX, only monetization. The review — once a quarter: what was confirmed (scale), what failed (drop or reframe), did new data appear (update the estimates), has the strategy changed (then the portfolio is reassembled).

## Procedure
1. **Determine the lifecycle stage** and the business's strategic priorities (`M-strategy-growth`).
2. **Formulate 1–2 goals** per SMART with a baseline and benchmarks; check with the formula "Strategy × Constraint × Controllability" and discard tasks disguised as goals.
3. **Find drivers** by the 5 steps; word each as a metric change; run the "why?" and "only one way?" tests; mark the type (product/business).
4. **Assemble drivers into streams**; for each stream set an Objective and measurable Key Results (`M-success-metrics`).
5. **Choose 3–5 focuses** by the criteria; for each specify the bottleneck data, the expected effect, the resource need and the alternative ("if instead we do Y — effect Z").
6. **Formulate 1–2 bets per focus** and check them by the six questions and the pain indicators; mark what is proven by data and what is an assumption.
7. **For each bet describe the alternatives**: a different mechanism, a cheaper check, "do nothing" (which metric results from inertia) and the bet's shutdown condition. Write down the strong objection to the bet and answer it before the decision.
8. **Assemble the portfolio** and check balance and skews; score Impact (data) and Effort (engineers).
9. Pass the bets to `M-risks` and `M-outcome-roadmap` (phases, transition criteria, stop signal).

## Template / checklist
**Goal card**
| Goal (SMART) | Type | Metric | Baseline | Target | Deadline | Owner | Link to strategy | Controllability |
|---|---|---|---|---|---|---|---|---|

**Driver card**: wording as a change; the segment where it sags; quantitative confirmation (funnel, numbers); qualitative confirmation (interviews, complaints); type; level in the pyramid.

**Bet card**
| Field | Content |
|---|---|
| Focus / stream | |
| Bet ("if… then…") | |
| Pain and its confirmation (which of the 5 indicators) | |
| Mechanism (the causal chain) | |
| Target effect and metric | |
| Resources and constraints | |
| Alternatives, including "do nothing" | |
| Shutdown condition (stop signal) | |
| Weak spot / strong objection | |

**Checklist**
- [ ] The goal is not an initiative and has a baseline and a deadline
- [ ] The goal type matches the product stage
- [ ] Every driver is worded as a change and confirmed by data
- [ ] The number of focuses does not exceed the number of teams
- [ ] Every bet passed the six questions and the pain check
- [ ] The portfolio is balanced (not only small things, not only big bets, not only UX/monetization)
- [ ] A portfolio review date is assigned

## Typical mistakes
- A goal = an initiative ("launch a referral program"), no baseline, no deadline, an unrealistic goal, goals not matching the stage (monetization at D30=5%), several goals at once.
- Confusion of levels: retention treated as input; NSM = revenue; a broken pyramid (page load speed does not affect payment conversion if users drop at another step); "the hospital average" without segmentation.
- A driver = an initiative ("add Apple Pay"); interviews without quantitative data; only business drivers instead of improving value.
- A "pretty focus" by fashion; a bet without confirmed pain ("it seems it will help"); "the user is always right" (they request a solution instead of describing the problem); socially desirable answers instead of behavior.
- A static portfolio without review; scoring Impact without data; every initiative "high impact, low effort" (poor scoring).

## Questions that can change the decision
- Which funnel bottleneck is the biggest and in which segment does it show?
- What happens without intervention: what will the metric equal after the period under inertia?
- Is the cause of the problem product-side or operational (slow delivery and few restaurants — not fixed by a redesign)?
- Is the pain confirmed by behavior and money, not only by words?
- Does the team have the resources and competencies for a big bet; would a small check be better first?
- Do the bets compete for one resource, and how are priorities set between them?
- Which shutdown condition for the direction will we choose in advance?

## Related maps
[[M-strategy-growth]], [[M-customers]], [[M-competitors]], [[M-success-metrics]], [[M-outcome-roadmap]], [[M-risks]], [[M-jtbd]], [[M-problem-design]], [[M-solution-design]], [[M-mvp-pilots]], [[M-brief-hypotheses]], [[M-quant-methods]]
