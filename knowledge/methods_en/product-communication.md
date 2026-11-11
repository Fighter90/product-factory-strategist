---
id: M-product-communication
lang: en
title: Product communication and defense — from roadmap to stakeholder decision
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [strategy, validation, after-decision]
tags: [product-defense, decision-memo, one-pager, stakeholders, gates, traction-doc, mece, traffic-light, pitch, post-mortem]
related: [M-roadmap, M-decision-daci, M-pmf-scaling, M-mvp-pilots, M-traction-model, M-risks, M-team, M-goals-drivers-bets, M-success-metrics, M-product-metrics]
---

# Product communication and defense

## When to apply
You need to turn analysis and a roadmap into the decision of the people who provide money, headcount and priority: prepare the document (one-pager / decision memo / traction doc), the presentation, the stakeholder map and the communication channel; then preserve the memory of the decision and review the outcome.

## Core idea
- **Why documents** (three tasks): align context across a large organization; make the decision on facts rather than charisma; preserve the product's memory (another team arrives tomorrow). The principle "1 page → one decision". A good document is not one to which nothing can be added, but one from which nothing can be removed.
- **Portfolio context (a large product company):** 200+ initiatives running simultaneously, 3K+ people in P&T. Problems without a portfolio: budgets built on assumptions, an unclear link between products and strategy, opaque economics, few breakthrough products, market entry disconnected from success criteria, difficulty justifying hiring and resolving conflicts between verticals and horizontals. Portfolio goals: align the portfolio with the strategy, raise the share of innovative products, make decisions and budget execution more deliberate, speed up time-to-market (from idea to production and on to PMF). Tasks: assessing potential, cross-cutting prioritization criteria, investment rules, reallocating teams, balancing the portfolio, coordinating the effort of verticals/horizontals/functions.
- **6 types of initiatives:** New Big Bet (high risk, potential of roughly 1B in incremental revenue or savings by year 5); Business as Usual bet (organic development, low risk); Product (a coherent feature set for a new need); Stream (a series of interconnected small improvements — a collection of mini-products); Enabler (a "foundation" for other products, often not a product itself); Other (non-product P&T initiatives). For enablers and streams, the classic gates are applied differently (stream — Stream-review and one headline metric; enabler — demand from the products that consume it).
- **Product stages and the outcome of each:** New idea (an idea selected, the frontend and timing defined, Gate 1) → Opportunity Discovery (needs, 3-year traction, validation methods and success criteria; the transition criterion is Gate 1) → Solution Discovery (hypotheses tested, end-state, MLP and PMF criteria defined, TDR passed, functions' OK; Gate 2) → Development (MLP launched, PMF achieved, marketing plan and scaling targets ready; Gate 3) → Scaling (targets achieved; the product becomes part of the company, pivots or shuts down; Gate 4; a quarterly deep dive on hitting the traction) → Baseline (quality support: stays as it is / pivot / closure).
- **Time-to-market:** the interval from an idea entering the portfolio to successfully passing Gate 3; it includes "useful" time (work, experiments, development) and "useless" time (waiting for other teams/partners/resources). Reference points from the lecture: kick-off → Gate 2 ≈ 120 days, Gate 2 → Gate 3 ≈ 6 months, Gate 3 → Gate 4 ≥ 1 year. Breaking the corridor is treated as a communication failure.
- **Traction model:** it must show which drivers deliver the result and how to influence them; it is built on a credible long-term forecast (LTM in the lecture) and links input and output metrics ([[M-traction-model]]).
- **Pilot hypothesis list:** only the base (that without which there is no point in moving on); the input → output link; the values that will be tested in the pilot. Example (phone buyback): onboard 4 federal retailers, 8% conversion across 200 partners, delivery SLA ≤ 7 days.
- **MECE** (mutually exclusive, collectively exhaustive): structure the problem so that the options do not overlap and cover everything; at the top level usually ≤ 5 items. Tests: more than 5 items → a layer is missing; two items can be merged into one phrase → not mutually exclusive; there is a "leftover" (e.g., besides iOS/Android another 15% of smartphones) → not exhaustive. Classroom errors: "order food" and "eat at a cafe" overlap; a list of remedies does not include "change the schedule".

### Working group composition and milestones
Mandatory: product manager, tech lead, UX researcher, designer, analyst; as needed — editor, business leader, PMM. A weekly sync (progress, insights, next steps). Preparing for the defense: record the outcomes after the previous defense (Jira, sprint review); book the date in advance and set pre-reads for critical participants; keep the team continuously engaged in decisions and risks; align decisions with key functions throughout the quarter; run 2–3 proofreads from a narrow circle to a wide one; before the defense, settle contentious points with the critical participants.

### Documents
- **One-pager (Gate 1/2):** (1) the problem (a paragraph); (2) insights; (3) the solution (an MLP sketch); (4) metrics and MDE; (5) risks and plan B.
- **Decision memo (up to 4 pages, Gate 2→3):** (1) goal and ask; (2) a recap of the problem with numbers; (3) the solution and end-state, what is cut off; (4) the MLP/MVP and why this one; (5) PMF criteria in numbers; (6) a TDR summary (feasible / feasible with limits / infeasible); (7) resources and budget; (8) Top-5 risks (probability × impact, owner, SLA, plan B); (9) timeline / TTM; (10) which decision is requested (money, people, quota).
- **Traction doc** (≤ 5 slides or 2 pages): MECE segmentation (2–5 blocks), output metrics with a 3-year target, input drivers with a causal link, pilot hypotheses (with an MDE), a 0–36-month growth timeline, risks and plan B.
- **Traffic-light dashboard (3 layers):** business result (GMV, revenue), user/PMF (NPS, D30 retention, LTV/CAC), technology/operations (SLA, latency, Contact Rate). The 🟡/🔴 thresholds are taken from the memo, the color is computed by rules, not manually; 1–2 core metrics + 3–5 proxies + counter-metrics; ≤ ~5 on screen. Threshold examples from the lecture: GMV −5% vs plan → 🟡, −10% → 🔴; NPS < 70 → 🟡, < 65 → 🔴; Contact Rate +30% vs base → 🟡, +50% → 🔴 (an illustration, not a norm).
- **Risk heatmap 3×3:** High-Impact × High-Prob = red before the launch; without a "red button" (feature flag, marketing freeze) do not allow a rollout. Registry fields: ID/category, description, probability/impact, mitigator, owner and response SLA.
- **TDR (Technical Decision Review):** the tech team's mini-gate before Gate 2 — load, server cost, latency, bus-factor; the result goes into the memo.
- **Post-mortem (up to 2 pages):** context/goal; hypothesis and metric (MDE); actions and chronology; fact vs target and root cause; what worked / what didn't (3–5 items); next steps/lessons with owners; links (memo, TDR, dashboards). Without action it is a "diary", not a tool.

### The "10 slides × 10 minutes" presentation
0 title + ask (1 phrase, 1 number, 1 decision) · 1 pain · 2 proof of pain (≤ 3 facts) · 3 solution / end-state · 4 MLP and PMF criteria · 5 traction · 6 unit economics (LTV/CAC, payback) · 7 resources · 8 risks and plan B · 9 the decision we are asking for. Storyline: problem → dream → road → price → fears → action. Q&A follows the "yes / and" rule ("yes, the number is bold, and there is a review every 3 months"). Dry run: reading aloud, colleagues' tough questions, a stopwatch, a tech check. Tables go into the memo; a chart goes on the slide.

### FAQ for the defense and "anti-fumbling"
The document contains an FAQ section: write out in advance the questions specific to the stakeholder, to the date/time of the defense and to the context; discuss contentious questions with key stakeholders before the defense. Self-check before sending (5 questions): why am I writing this / is it still relevant · what will I lose if I delete this sentence · are there enough details · what conclusion follows from the sentence · does it explain the previous statement (if so — why is the previous one not enough). The "anti-fumbling" checklist before the pitch: the punchline contains market share and payback period, not just an absolute ("1B GMV = 5% of the P2P market, 7-month payback") · the core metric is expressed as a number and a unit ("Contact Rate −30% in 6 months", not "improve safety") · the BEP in the base and pessimistic scenarios is below the board's threshold · bus-factor ≥ 2 for every critical service/role · every High×High risk comes with a Plan B (feature flag, backup channel, manual process) · a dry run with a "devil's advocate" in the role of CFO/CTO/CMO.

### Typical failures and repackaging
Five categories that kill even a perfect pitch: (1) an "empty" punchline — a loud absolute without share and pay-back; (2) a ghost metric — a goal without a unit of measurement; (3) a tech blind spot — the TDR is green but bus-factor = 1; (4) the "red pessimist" — the base scenario is fine while the pessimistic one breaks the payback threshold (the cure: a phased rollout, lower CAPEX, CAC); (5) a risk without a Plan B — the risk map shows "how we die" but not "how we don't die". The repackaging principle: not "redo the design" but close the hole with a fact, a number, a plan or a resource — a quarter later the same deck with the patched hole passes without questions.

### Stakeholders
Channels: chats, meetings, reports, internal mailings, a single portfolio feed (the board shows which stage each initiative is at and which document is needed next). Types (from the lecture): approvers, the anxious, dominants, the demanding, the indifferent, initiators, silent experts, politicians, optimists, skeptics. Working tactics (an interpretation of the map): for the anxious — risks and plan B in advance; for dominants and the demanding — preliminary 1-on-1s and clear boundaries of the ask; for silent experts — personal questions outside the meeting; for skeptics — data and a failure criterion; for approvers — a checklist to sign off. To distribute roles, use [[M-decision-daci]].

## Procedure
1. Define the **decision we are asking for** and who makes it (Driver / Approver); the deadline and format (Gate, deep dive, QBR).
2. Choose the document by gate: Gate 1 → one-pager; Gate 2/3 → decision memo + TDR + risk log; quarter → deep dive with the traffic light.
3. Assemble the facts and separate them in the document: **facts** (with source, period, n), **hypotheses** (how they are tested, criterion), **forecasts** (assumptions, scenarios). Numbers instead of adjectives; replace "we want to improve loyalty" with "NPS +7 pp over 2 quarters".
4. Fix the PMF/success criteria and the traffic-light thresholds **in the document before the launch**; Top-5 risks with owners, SLA and plan B.
5. Structure through MECE (no more than 5 items per level); check the input → output link.
6. Run 2–3 proofreads (D-7 draft, D-4 cuts and a number check, D-2 dry run); settle contentious points with the critical participants; send the memo no later than 48 hours before the board.
7. At the defense: the ask and the key number first, then pain, solution, price, risks; on objections — "yes / and" with a plan.
8. After the decision: record the outcome in the decision journal ([[M-decision-daci]]), update the roadmap, assign the owners of actions; plan the post-mortem (date, metric, MDE).

## Template / checklist
Readiness-for-defense checklist: goal and ask in the first paragraph · one thought — one slide/paragraph · an executive summary at the start · numbers instead of adjectives (N interviews, +x pp) · numerical PMF criteria · a TDR summary · budget and resources · Top-5 risks with an owner and SLA · a plan B for every red risk · the timeline fits the TTM corridors · the document is 1–4 pages · sent 48 h ahead · a dry run held · a punchline with share and payback, a core metric with a unit · bus-factor ≥ 2 · the FAQ anticipated · the questions "expensive?", "how many people?", "why now?" anticipated.
Writing rules: write briefly and simply; one idea — one sentence; do not write about what you are not sure of; share results, not process; give answers, not questions; back up "grew/fell" with numbers and significance; the self-check: why am I writing this, what do I lose by deleting, are there enough details, what is the conclusion, does it explain the previous statement.

## Typical mistakes
- "We'll do it because competitors did" — no numbers and no impact on the key metric.
- "We need 3 more months of research" when the corridor is already overdue; Discovery without stop criteria.
- "Users will like it" without an MDE and an NPS target.
- A 30-slide document; two levels (strategy and feature) on one slide; a copy-pasted backlog instead of 3 drivers.
- A dashboard metric without a threshold, 10+ metrics, a red risk without an owner and SLA.
- No plan B / "red button"; risks discussed for the first time at the board ("directors fear a risk they learned about by accident").
- Approval "at the last moment"; it was not found out in advance who is against.
- A post-mortem without causes and actions, or turned into a hunt for the guilty.

## Questions that can change the decision
- Which exact decision is needed and who makes it? Are we asking for something outside the audience's authority?
- Which 1–2 numbers will the board see and remember, and are they confirmed?
- Which stakeholders are against, and what do they fear (risk, cost, speed, a conflict of priorities)?
- What happens if the TTM corridor is broken?
- What will be the "red button", and who has the right to press it without an additional approval?

## Related maps
[[M-roadmap]], [[M-decision-daci]], [[M-pmf-scaling]], [[M-mvp-pilots]], [[M-traction-model]], [[M-risks]], [[M-team]], [[M-goals-drivers-bets]], [[M-success-metrics]], [[M-product-metrics]]
