---
id: M-product-communication
lang: en
title: Product Communication and Defense — from roadmap to stakeholder decisions
course: pm
sources: ["EN mirror of the RU methodology card M-product-communication (knowledge/methods/product-communication.md); original sources are listed in the RU card"]
stages: [strategy, validation, after-decision]
tags: [product-defense, decision-memo, one-pager, stakeholders, gates, traction-doc, mece, traffic-light, pitch, post-mortem]
related: [M-roadmap, M-decision-daci, M-pmf-scaling, M-mvp-pilots, M-traction-model, M-risks, M-team, M-goals-drivers-bets, M-success-metrics, M-product-metrics]
---

# Product communication and defense

## When to apply
You need to turn the analysis and the roadmap into a decision by the people who allocate money, people, and priority: prepare the document (one-pager / decision memo / traction doc), the presentation, the stakeholder map, and the communication channel; then preserve the decision's memory and review the outcome.

## Essence
- **Why documents** (three jobs): align the context across a large organization; make the decision on facts, not charisma; preserve the product's memory (a different team arrives tomorrow). The principle "1 page → one decision". A good document is not one with nothing left to add, but one with nothing left to remove.
- **Portfolio context (a large product company):** 200+ initiatives at once, 3K+ people in P&T. Problems without a portfolio: budgets built on assumptions, an unclear link between products and strategy, opaque economics, few breakthrough products, market entry detached from success criteria, hiring hard to justify, conflicts between verticals and horizontals hard to resolve. Portfolio goals: align the portfolio and the strategy, raise the share of innovative products, increase the deliberateness of decisions and budget execution, speed up time-to-market (from idea to production and to PMF). Tasks: potential assessment, end-to-end prioritization criteria, investment rules, team reallocation, portfolio balance, aligning the efforts of verticals/horizontals/functions.
- **6 types of initiatives:** New Big Bet (high risk, a potential on the order of 1 bn of additional revenue or savings by year 5); Business as Usual bet (organic development, low risk); Product (a coherent feature set for a new need); Stream (a series of interconnected small improvements — a set of mini-products); Enabler (a "foundation" for other products, often not a product itself); Other (non-product initiatives of P&T). For enablers and streams, the classic gates apply differently (stream — a Stream-review and a single headline metric; enabler — demand from the consuming products).
- **Product stages and the outcome of each:** New idea (an idea selected, a frontend/timeline defined, Gate 1) → Opportunity Discovery (needs, 3-year traction, verification methods and success criteria; the transition criterion is Gate 1) → Solution Discovery (hypotheses tested, an end-state, an MLP, and PMF criteria defined, the TDR passed, feature readiness OK; Gate 2) → Development (the MLP launched, PMF achieved, a marketing plan and scaling goals ready; Gate 3) → Scaling (goals achieved; the product becomes part of the company, pivots, or shuts down; Gate 4; a quarterly deep dive on tracking against the traction plan) → Baseline (quality maintenance: keeps living as it lived / pivot / shutdown).
- **Time-to-market:** the interval from an idea entering the portfolio to passing Gate 3; it includes the "useful" (work, experiments, development) and the "useless" (waiting for other teams/partners/resources). Benchmarks from the lecture: kick-off → Gate 2 ≈ 120 days, Gate 2 → Gate 3 ≈ 6 months, Gate 3 → Gate 4 ≥ 1 year. Missing the corridor is treated as a communication failure.
- **The traction model:** it must show which drivers produce the result and how to influence them; it is based on a credible long-term forecast (in the lecture — LTM) and links input and output metrics ([[M-traction-model]]).
- **The pilot hypothesis list:** only the base (without which there is no point in going further); the input → output link; the values that will be tested in the pilot. Example (phone buyback): connect 4 federal retailers, 8% conversion across 200 partners, a fulfillment SLA ≤ 7 days.
- **MECE** (mutually exclusive, collectively exhaustive): structure the problem so that the options do not overlap and cover everything; usually ≤ 5 items per level. Test: more than 5 items → a layer is missing; two items merge into one phrase → not mutually exclusive; there is a "remainder" (e.g., besides iOS/Android another 15% of smartphones) → not exhaustive. Teaching errors: "order food" and "eat at a café" overlap; a list of punishments omits "change the schedule".

### Working-group composition and milestones
Mandatory: the product manager, the tech lead, a UX researcher, a designer, an analyst; as needed — an editor, a business leader, a PMM. A weekly sync (progress, insights, next steps). Defense preparation: record the outcomes after the previous defense (Jira, sprint review); book the date in advance and give advance notice to the critical participants; keep the team continuously engaged with decisions and risks; align decisions with the key functions throughout the quarter; 2–3 read-throughs from a narrow circle to a wide one; before the defense, align contested points with the critical participants.

### Documents
- **One-pager (Gate 1/2):** (1) the problem (a paragraph); (2) insights; (3) the solution (an MLP sketch); (4) metrics and the MDE; (5) risks and plan B.
- **Decision memo (up to 4 pages, Gate 2→3):** (1) the goal and the ask; (2) a recap of the problem with numbers; (3) the solution and the end-state, what is cut off; (4) the MLP/MVP and why this one; (5) the PMF criteria in numbers; (6) the TDR summary (feasible / constrained / impossible); (7) resources and budget; (8) the Top-5 risks (probability × impact, owner, SLA, plan B); (9) the timeline / TTM; (10) which decision is requested (money, people, quota).
- **The traction doc** (≤ 5 slides or 2 pages): MECE segmentation (2–5 blocks), output metrics with a 3-year target, input drivers with causal links, the pilot hypotheses (with the MDE), a 0–36-month growth timeline, risks and plan B.
- **A traffic-light dashboard (3 layers):** the business outcome (GMV, revenue), the user/PMF (NPS, retention D30, LTV/CAC), technology/operations (SLA, latency, Contact Rate). The 🟡/🔴 thresholds come from the memo; the color is computed by rules, not by hand; 1–2 core metrics + 3–5 proxies + counter-metrics; ≤ ~5 on screen. Threshold examples from the lecture: GMV −5% vs plan → 🟡, −10% → 🔴; NPS < 70 → 🟡, < 65 → 🔴; Contact Rate +30% vs baseline → 🟡, +50% → 🔴 (an illustration, not a norm).
- **A risk heatmap 3×3:** High-Impact × High-Prob = red before launch; without a "red button" (a feature flag, a marketing freeze) do not allow a rollout. Register fields: ID/category, description, probability/impact, mitigator, owner and a response SLA.
- **TDR (Technical Decision Review):** a mini-gate of the tech team before Gate 2 — load, server costs, latency, bus-factor; the summary goes into the memo.
- **A post-mortem (up to 2 pages):** context/goal; the hypothesis and metric (MDE); actions and chronology; fact versus target and the root cause; what worked/did not (3–5 items); next steps/lessons with owners; links (memo, TDR, dashboards). Without an action it is a "diary", not a tool.

### The "10 slides × 10 minutes" presentation
0 title + the ask (1 phrase, 1 number, 1 decision) · 1 pain · 2 proof of pain (≤ 3 facts) · 3 solution / end-state · 4 MLP and the PMF criteria · 5 traction · 6 unit economics (LTV/CAC, payback) · 7 resources · 8 risks and plan B · 9 the decision we ask for. Narrative: problem → dream → road → price → fears → action. Q&A by the "yes / and" rule ("yes, the number is bold, and there is a review every 3 months"). Dry run: read aloud, colleagues' hard questions, a stopwatch, a tech check. Tables go into the memo; a graph goes on the slide.

### FAQ for the defense and the "anti-f-up" check
The document has an FAQ section: write down the stakeholder-specific questions in advance, keyed to the stakeholder's profile, the date/time of the defense, and the context; discuss the contested questions with the key stakeholders before the defense. The self-check before sending (5 questions): why am I writing this / is it current · what do I lose if I delete this sentence · are there enough details · what conclusion follows from the sentence · does it explain the previous statement (if so — why was the previous one not enough). The "anti-f-up" checklist before the pitch: the punchline contains market share and payback, not only an absolute ("1 bn GMV = 5% of the P2P market, payback 7 months") · the core metric is expressed as a number and a unit ("Contact Rate −30% in 6 months", not "improve safety") · BEP in the base and pessimistic scenarios is below the board's threshold · bus-factor ≥ 2 for every critical service/role · every High×High risk has a Plan B (a feature flag, a backup channel, a manual process) · a dry run with a "devil's advocate" playing CFO/CTO/CMO.

### Typical failures and repackaging
Five categories that kill even a perfect pitch: (1) the hollow punchline — a loud absolute without a share and pay-back; (2) the ghost metric — a goal without a unit of measurement; (3) the tech blind spot — TDR green but bus-factor = 1; (4) "red pessimism" — the base scenario is fine, but the pessimistic one breaches the payback threshold (treated with: a phased rollout, lower CAPEX, CAC); (5) a risk without a Plan B — the risk map shows "how we die" but not "how we do not die". The repackaging principle: not "redo the design" but close the hole with a fact, a number, a plan, or a resource — a quarter later the same slide deck with the patched hole passes without questions.

### Stakeholders
Channels: chats, meetings, reports, internal mailings, a single portfolio feed (a board showing at which stage each initiative is and which document is needed next). Types (from the lecture): approvers, worriers, dominants, demanders, the indifferent, initiators, silent experts, politicians, optimists, skeptics. Working moves (reading the map): worriers — risks and plan B in advance; dominants and demanders — preliminary 1-on-1s and clear boundaries of the ask; silent experts — personal questions outside the meeting; skeptics — data and a failure criterion; approvers — a checklist ready for signature. For role allocation use [[M-decision-daci]].

## Procedure
1. Define **the decision you are asking for** and who makes it (Driver / Approver); the deadline and format (a Gate, a deep dive, a QBR).
2. Choose the document by gate: Gate 1 → a one-pager; Gate 2/3 → a decision memo + TDR + a risk log; a quarter → a deep dive with the traffic light.
3. Collect the facts and separate them in the document: **facts** (with a source, period, n), **hypotheses** (how they are tested, the criterion), **forecasts** (assumptions, scenarios). Numbers instead of adjectives; replace "we want to improve loyalty" with "NPS +7 pp over 2 quarters".
4. Fix the PMF/success criteria and the traffic-light thresholds **in the document before launch**; the Top-5 risks with owners, SLA, and a plan B.
5. Structure with MECE (no more than 5 items per level); verify the input → output link.
6. Run 2–3 read-throughs (D-7 a draft, D-4 cuts and number checks, D-2 a dry run); align the contested points with the critical participants; send the memo no later than 48 hours before the board.
7. At the defense: first the ask and the key number, then the pain, solution, price, risks; to objections — "yes / and" with a plan.
8. After the decision: record the outcome in the decision log ([[M-decision-daci]]), update the roadmap, assign the action owners; plan the post-mortem (date, metric, MDE).

## Template / checklist
The defense-readiness checklist: the goal and the ask in the first paragraph · one thought per slide/paragraph · a summary at the top · numbers instead of adjectives (N interviews, +x pp) · the PMF criteria in numbers · a TDR summary · budget and resources · the Top-5 risks with an owner and SLA · a plan B for every red risk · the timeline fits the TTM corridors · the document is 1–4 pages · sent 48 h ahead · a dry run done · a punchline with share and payback, the core metric with a unit · bus-factor ≥ 2 · the FAQ anticipated · the questions "expensive?", "how many people?", "why now?" anticipated.
Writing rules: write short and simple; one idea per sentence; do not write about what you are unsure of; share results, not process; give answers, not questions; back "it rose/fell" with numbers and significance; the self-check: why am I writing this, what do I lose by deleting it, are there enough details, what is the conclusion, does it explain the previous statement.

## Typical mistakes
- "We'll do it because the competitors did" — no numbers and no impact on the key metric.
- "We need 3 more months of research" with an overdue corridor; Discovery without stop criteria.
- "Users will like it" without an MDE and an NPS target.
- A 30-slide document; two levels (strategy and a feature) on one slide; a copy-pasted backlog instead of 3 drivers.
- A dashboard metric without a threshold, 10+ metrics, a red risk without an owner and SLA.
- No plan B / "red button"; the risks discussed for the first time at the board ("executives fear a risk they learned about by accident").
- Approvals "at the last moment"; never clarified in advance who is against.
- A post-mortem without causes and actions, or with a search for the guilty.

## Questions that could change the decision
- Which exact decision is needed and who makes it? Are we asking for something outside the audience's authority?
- Which 1–2 numbers will the board see and remember, and are they confirmed?
- Which stakeholders are against, and what do they fear (risk, cost, speed, a priority conflict)?
- What happens if the TTM corridor is broken?
- What will be the "red button", and who has the right to press it without additional approval?

## Related maps
[[M-roadmap]], [[M-decision-daci]], [[M-pmf-scaling]], [[M-mvp-pilots]], [[M-traction-model]], [[M-risks]], [[M-team]], [[M-goals-drivers-bets]], [[M-success-metrics]], [[M-product-metrics]]
