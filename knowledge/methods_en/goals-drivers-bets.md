---
id: M-goals-drivers-bets
lang: en
title: Goals, growth drivers, streams, focus areas, product bets and the initiative portfolio
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [options, strategy, validation]
tags: [goals, smart, growth-drivers, streams, focus-areas, bets, big-bets, portfolio, impact-effort, pain-validation]
related: [M-strategy-growth, M-customers, M-competitors, M-success-metrics, M-outcome-roadmap, M-risks, M-jtbd, M-problem-design, M-solution-design, M-mvp-pilots, M-brief-hypotheses, M-quant-methods]
---

# Goals, growth drivers, streams, focus areas, product bets and the initiative portfolio

## When to apply
Use this when "we want to grow" has to be turned into a concrete hierarchy: what exactly we change (the goal), through which levers (drivers), in which large direction (stream), what we concentrate on in this period (focus), which large hypothesis we back (bet), and with which actions (initiatives) we verify it. The card protects against the frequent mistake of jumping straight to features.

## Core idea
**The decision hierarchy** (from strategy to operations): goal → streams → drivers → focus areas → bets → initiatives → experiments. The strategic level is the goal, streams and drivers; the tactical level is focus areas and bets; the operational level is initiatives and experiments.

**A goal ≠ a metric ≠ an initiative.** The goal is what changes in the system (D7 retention +5 pp); the metric is how we measure it; the initiative is what we do. "Launch a referral program" is an initiative, not a goal.

**Six types of goals**
| Type | Example | Key question |
|---|---|---|
| Growth | registrations +25% | how to bring in more people |
| Activation & Retention | activation 40% → 55%; D30 12% → 18% | how to get users to value and keep them |
| Monetization | ARPU +15% | how to earn more from current users |
| Cost & Efficiency | cost-to-serve −12% | how to spend less |
| Supply / Quality / Trust | active sellers +20% | how to improve supply and trust |
| Strategic Expansion | a new SMB segment, 10% of revenue | where to expand |

A technical "goal" (upgrade the system version) is a task; the real goal is to protect retention while reducing downtime risk.

**How to choose a goal**: *Strategy × System constraint × Controllability = the priority goal.*
- Strategy context and lifecycle stage: PMF → activation/retention; growth → growth/supply; maturity → monetization/efficiency; decline → harvest (profit), keeping the core, or pivot.
- Diagnostics on data: where the funnel bottleneck is, which metric limits growth, whether there is headroom (benchmarks, market, competitors).
- Controllability: can we influence it, and will the effect be visible within the period's horizon.
If one factor is missing: no controllability → the goal is unreachable; no constraint → it is unclear what to optimize (fix the diagnostics); no link to strategy → we are optimizing the wrong thing. Scaling with low retention is "pouring water into a leaky bucket".

**SMART for product goals**: specific, measurable (metric, baseline, target value), achievable, relevant to the strategy, time-bound. Example: "Raise D7 retention from 22% to 30% within 3 months".

**A growth driver** is a source of change in a key metric, not a feature. It is phrased through change: "cut drop-off at the payment step by 20 pp" is a driver; "add Apple Pay" is an initiative; "a redesign" is a tool, not a driver. Wording tests: if you can ask "why?" — it is an initiative; if there is only one way to implement it — it is an initiative (a real driver has at least two paths).
- Product drivers: activation and key scenarios, search and recommendations, data and content quality, removing friction.
- Business drivers: prices, promotions, acquisition channels, partnerships.
- Antipattern: treating a supply shortage with a redesign.

**A metric decomposes into a product of drivers.** To find the levers, the outcome/output is broken down into multipliers: `orders = active users × conversion to order × order frequency per user`; each multiplier is its own output/input driver with its own way of being influenced. The search logic: pick the multiplier with the biggest gap against a benchmark or a competitor → for that multiplier, find the segment and the point of failure → formulate 2–3 drivers. As a rule, a driver lives at the output or input level of the pyramid: outcome and the NSM cannot be moved "with a button".

**Three levels that get confused** (each next one is more concrete):
| Level | Wording | Example |
|---|---|---|
| Driver | a change in a metric | "conversion to first order 15% → 25%" |
| Bet | an "if… then…" hypothesis about the mechanism | "if we simplify the order form, conversion will rise" |
| Initiative | a concrete action with a deadline | "cut the form from 5 fields to 2" |

**The driver search algorithm (5 steps)**: goal → decompose the funnel and segment it (new/returning, paying/not paying, devices) → quantitative data in the problem segment (conversions, points of failure, time to the key event) → qualitative research (interviews, complaints, session recordings, usability tests) → 2–3 drivers. Drivers are grounded in facts, not in "it seems". A driver sits at the output or input level of the pyramid (`M-success-metrics`); retention cannot be steered directly.

**A growth stream** is a systemic direction that unites several drivers around one large goal ("Improving activation": the first step, guided actions, a simpler sign-up). A stream gives teams focus for at least a quarter and gives the future roadmap its structure.

**Focus** is the direction in which effort is concentrated inside a stream during a period ("cut time-to-first-value"). Five types: growth (acquisition, activation, viral loop), retention, monetization, UX improvements, platform/technical. Choosing 3–5 focus areas: build on the goals; look at funnels and segments; find the bottleneck (the biggest failure, not the most interesting); check the resources; estimate the impact on metrics. There should be no more focus areas than teams (1–2 per team); the same rule applies to streams — the number of streams ≤ the number of teams, and resources are allocated to each stream immediately (how many developers/analysts), otherwise "3 streams" turn into a wish list. The justification of a focus to leadership is built from data ("drop-off is 40% at step 3; if we cut it to 20% — +X conversions"), not from fashion. A focus is not forever: it is revised every quarter; a stream may stay while the focus inside it changes. The antipattern is the "beautiful focus" (AI recommendations with no bottleneck behind them).

**A bet** is a large hypothesis that would substantially change a key metric if it succeeds. It is always: tied to a focus, backed by confirmed pain, describing the mechanism of influence, measurable. Wording: "if we do X (the change), then metric Y changes by Z within period T". Six questions for a bet: is it inside the focus? is there a concrete pain? is the pain confirmed by data? is the cause-and-effect chain clear? is there a measurable target effect? are the constraints and resources clear?

**Pain validation** (otherwise the hypothesis is an illusion)
| Tool | What it checks | Signals |
|---|---|---|
| JTBD | what the person is trying to do, what gets in the way, what progress they want | the product is "not hired" → there is unresolved pain |
| CustDev | the reality of the pain | how often the situation happens, the emotion, the high cost of inaction, the existence of a workaround (a crutch, Excel, YouTube instead of an app) |
| Behavioral data | scale | long time on a step, high drop-off, repeated actions (click → cancel → again), attempts to bypass limits |
| Monetary confirmation | the strongest one | pays or is ready to pay |

The pain pyramid: blocking > significant > annoyance > wish list. Work with the first two. Rule: if ≥3 of the 5 indicators are confirmed (frequency, scale, emotion, workaround, willingness to pay), the pain is real; otherwise it is most likely a wish. False signals: "if you add X, I would definitely use it", a single loud complaint, a request from one large client, correlation instead of causation (projects that were created are retained better — reverse causation is possible).

**The initiative portfolio**: a system of big, mid and small bets. The target balance: 1–2 big bets, 3–5 mid bets, 5–10 small bets. The Impact/Effort matrix: high effect at low effort — do it right away (rare); high/high — a big bet; low/low — quick checks; low/high — decline. Estimate Impact from data and Effort with engineers (t-shirt sizes, planning poker); add confidence (ICE = Impact × Confidence × Ease); at low confidence, run research first. Signs that the matrix is not working: every initiative is "high effect, low effort" (the scoring is poor), there is no data for impact (a discovery phase is needed), the team cannot estimate effort (a technical spike is needed), all initiatives are of the same type. Antipatterns: only small tweaks, only big bets, only UX, only monetization. Revision — once a quarter: what was confirmed (scale it), what failed (drop it or reformulate it), whether new data has appeared (update the estimates), whether the strategy has changed (then the portfolio is rebuilt).

## Procedure
1. **Determine the lifecycle stage** and the business's strategic priorities (`M-strategy-growth`).
2. **Formulate 1–2 goals** in SMART form with a baseline and benchmarks; check them against "Strategy × Constraint × Controllability" and discard tasks disguised as goals.
3. **Find the drivers** using the 5 steps; write each one as a change in a metric; run the "why?" and "only way?" tests; note the type (product/business).
4. **Bundle the drivers into streams**; set an Objective and measurable Key Results for each stream (`M-success-metrics`).
5. **Choose 3–5 focus areas** against the criteria; for each one, specify the bottleneck data, the expected effect, the resource needs, and the alternative ("if we work on Y instead — effect Z").
6. **Formulate 1–2 bets per focus** and check them against the six questions and the pain indicators; mark what is proven by data and what is an assumption.
7. **For each bet, describe the alternatives**: a different mechanism, a cheaper check, "do nothing" (what the metric will look like under inertia), and the condition for closing the bet. Write down the strongest objection to the bet and answer it before making the decision.
8. **Assemble the portfolio** and check it for balance and skew; score Impact (with data) and Effort (with engineers).
9. Pass the bets to `M-risks` and `M-outcome-roadmap` (phases, gate criteria, stop signals).

## Template / checklist
**Goal card**
| Goal (SMART) | Type | Metric | Baseline | Target | Deadline | Owner | Link to strategy | Controllability |
|---|---|---|---|---|---|---|---|---|

**Driver card**: phrased as a change; the segment where it underperforms; quantitative confirmation (funnel, numbers); qualitative confirmation (interviews, complaints); type; level in the pyramid.

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
| Closing condition (stop signal) | |
| Weak point / strongest objection | |

**Checklist**
- [ ] The goal is not an initiative and has a baseline and a deadline
- [ ] The goal type matches the product's stage
- [ ] Every driver is phrased as a change and confirmed with data
- [ ] The number of focus areas does not exceed the number of teams
- [ ] Every bet has passed the six questions and the pain check
- [ ] The portfolio is balanced (not only small items, not only big bets, not only UX/monetization)
- [ ] A portfolio revision date is set

## Typical mistakes
- Goal = initiative ("launch a referral program"), no baseline, no deadline, an unrealistic goal, goals that do not match the stage (monetization at D30=5%), several goals at once.
- Confused levels: retention treated as an input; NSM = revenue; a broken pyramid (loading speed does not affect payment conversion if users drop off at another step); a "hospital average" without segmentation.
- Driver = initiative ("add Apple Pay"); interviews without quantitative data; only business drivers instead of improving value.
- A "beautiful focus" chosen for fashion; a bet without confirmed pain ("it feels like it would help"); the user "is always right" (they propose solutions instead of describing the problem); socially desirable answers instead of observed behavior.
- A static portfolio without revision; Impact estimated without data; every initiative scored "high effect, low effort" (poor-quality estimation).

## Questions that can change the decision
- Which funnel bottleneck is the biggest, and in which segment does it show up?
- What happens without intervention: what will the metric equal after the period if we do nothing?
- Is the cause of the problem a product one or an operational one (slow delivery and few restaurants are not fixed by a redesign)?
- Is the pain confirmed by behavior and money, not just by words?
- Does the team have the resources and competencies for a big bet; would a small check first be better?
- Do the bets compete for the same resource, and how are priorities set between them?
- Which condition for closing the direction will we choose in advance?

## Related maps
[[M-strategy-growth]], [[M-customers]], [[M-competitors]], [[M-success-metrics]], [[M-outcome-roadmap]], [[M-risks]], [[M-jtbd]], [[M-problem-design]], [[M-solution-design]], [[M-mvp-pilots]], [[M-brief-hypotheses]], [[M-quant-methods]]
