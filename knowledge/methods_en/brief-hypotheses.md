---
id: M-brief-hypotheses
lang: en
title: Research brief and hypothesis formulation
course: ux
sources: ["EN mirror of the RU methodology card M-brief-hypotheses (knowledge/methods/brief-hypotheses.md); original sources are listed in the RU card"]
stages: [intake, research, validation]
tags: [brief, hypotheses, research-goal, business-goal, ice, discovery-plan, decision-log]
related: [M-research-types, M-audience-research, M-in-depth-interviews, M-quant-methods, M-goals-drivers-bets, M-success-metrics, M-product-context, M-problem-design, M-mvp-pilots, M-decision-daci, M-product-metrics]
---

# Research brief and hypothesis formulation

## When to use
The initial request is vague ("we need to research…"), or the research has already been started without an agreement on why it exists and what will happen to the result. The card turns a request into a brief (an agreement on meaning between product and researcher) and into testable hypotheses with a PASS/FAIL criterion.

## Core idea
**UX and research sit at the intersection of people, business, and technology.** The researcher defines goals and questions, chooses the method, prepares and runs the fieldwork, analyzes, presents, and supports implementation. The brief is the first page of that cycle: without it the timeline stretches and the result never lands in decisions.

**A business goal and a research goal are different things.**
| | Business goal | Research goal |
|---|---|---|
| Question | How to earn more / cut losses? | How does this work? Why does it happen? What follows from it? |
| Metrics | revenue, conversion, acquisition cost, NPS | satisfaction, task completion time, error rate, reasons for behavior |
| Horizon | quarter, year | from 2 weeks to several months |
| Result | sales growth, cost reduction | insights and product recommendations |
| Risk if forgotten | decisions "blind" (features nobody uses) | "research for research's sake": a beautiful report with no effect on money |
The chain: business goal "raise purchase conversion by 10%" → research goal "find out why users don't reach payment" → action (simplified the payment form) → metric check.

**A hypothesis** — a testable assumption about user behavior, motives, or problems (research hypothesis) or about the effect of a product change on value and a metric (product hypothesis). It contains a segment, an observable problem/opportunity, and an expected measurable effect. The difference from an idea is the presence of these three parts and a verification criterion.
- *Problem hypothesis* — about understanding (why people behave this way); Discovery.
- *Solution hypothesis* — about the outcome (will the change work); Delivery and A/B.
- *Bad:* "people don't like our pickup points" (generic, no segment or cause, seeks confirmation). *Good:* "new users choosing a pickup point for the first time do not place a repeat order because of a negative experience: the point is hard to find and expectations did not match the actual place" (specific, testable, decomposes into sub-hypotheses, shows next steps).

**Sources of hypotheses:** analytics (dashboards, funnels, dips); research (any, desk and field); support data (a spike in ticket causes); reviews and social media; plus benchmarking and dogfooding (additional channels: dogfooding does not replace verification on a real segment).

**Strength of evidence for a hypothesis.** A hypothesis stays a hypothesis until it passes a check by a method appropriate to the question type ([[M-research-types]]). Interviews give a plausible explanation but not the scale; desk data gives direction; only measurement with a threshold fixed in advance allows saying PASS/FAIL.

## Procedure
1. **Hold a brief session with the product.** Put yourself in the CEO's shoes: what will this research give, is it useful or a waste of resources?
2. **Fill in the brief** across the 10 fields (below). No answer — do not launch fieldwork, collect more data instead.
3. **Separate the goals:** write down the business goal with a metric (and baseline), separately the research goal (what we want to learn/verify), and the next step after the result.
4. **Collect hypotheses** from the sources (analytics, research, support, reviews, benchmarks); in ~60 minutes: open 4–5 dashboards and note anomalies, read the top tickets and fresh reviews, look at the latest UX report, do a quick benchmark.
5. **Phrase each hypothesis** in the format: *If [segment] faces [X / does Y], then because of [cause] [measurable effect: metric, baseline, magnitude] will happen within [timeframe / scenario].*
6. **Filter and prioritize.** Simple ICE scoring: Impact (effect on the main metric), Confidence (is there enough data to believe), Ease (cost and time), each 1–10; only the selected ones go into the brief. ICE scores are subjective — record what they are based on.
7. **Choose the method and audience** for each hypothesis ([[M-research-types]], [[M-audience-research]]); state the topics/questions for discussion or the scenarios to test.
8. **Describe the Discovery plan** for the main hypothesis: target metric (baseline, target change), audience (IN/OUT), method and volume, data sources, a numeric PASS/FAIL criterion (before the start), owners and dates.
9. **The ladder of working with a hypothesis:** formulation → Discovery (how and with what we verify) → elaboration (bring in the right people) → decision (final elaboration for development) → Delivery (launch) → feedback (first data cut, test results).
10. **After verification** — write the result into the decision log: "hypothesis → outcome (PASS / FAIL / PARTIAL) → metric change → decision (roll out / rework / close) → next step." Failures must be recorded: otherwise ideas repeat.

**A quick "hypothesis sprint" (15 minutes, when you need to warm up an idea cheaply):** 10 minutes analyzing the case from data (logs, support, benchmark) → 5 minutes ICE-scoring 1–2 hypotheses → the one top hypothesis goes into a Discovery plan. Quality check of the exercise: every hypothesis is immediately "stitched" to a metric and a verification plan, not just written down.

**Health metrics of the hypothesis portfolio (computed from the decision log per quarter):**
| Metric | How to compute | Reference point |
|---|---|---|
| Validation rate | (PASS + PARTIAL) / all closed | ≥ 40% |
| Speed to verdict | average days "start → outcome" | ≤ 20 days |
| ROI 90 days | Σ(ΔGMV or ΔLTV) / Σ verification costs | > 3× |
| Kill early rate | closed before development / all | ≥ 25% (cutting "junk" early) |

## Template / checklist

### Research brief (all fields of the course template)
| No | Field | What should be written |
|---|---|---|
| 1 | Context | what we already know, including past research; why now; how much of a priority |
| 2 | Business goal in this task | what the business wants to achieve; why the research; which metrics the results will affect |
| 3 | Research goals and objectives | what we run it for; what we verify; what we will get an answer to or be able to decide |
| 4 | What the next step will be | which decisions depend on the result; what we do on confirmation and on refutation |
| 5 | Our hypotheses and questions | which assumptions we verify; what we want to clarify; which questions are unanswered; what to confirm or refute |
| 6 | Which method we want to verify the hypothesis with | method; high-level interview topics / test user flows; why exactly this one |
| 7 | Audience | who the research TA is; which segments answer the questions best; experience, vertical, category, activity volume; how to find the right people; whom we exclude |
| 8 | Timing and resources | when to start; priority; hard and soft deadlines |
| 9 | Image of the result | what must be in the final report; in which format conclusions are needed for further work |
| 10 | Related research | links to context sources, to subsequent iterations, marketing and analytics studies |
In the lecture the structure is given as "context → business goal → goals and objectives → hypotheses and questions → next steps → method → TA → timing and agreements → image of the result"; the template adds the "Related research" field.

**Example (briefly):** context — claims handling with partners runs over email, the project is scaling; business goal — product vision reflected in claims, impact on the share of claims, share of compensations, processing time; goals — how competitors organized claims handling, how pickup points work with claims, which pains exist with us and with the anchor brand, best practices; hypothesis — "if we give pickup points a claims-handling tool (a section in the dashboard), the closing time and the number of erroneous claims will shrink"; next step — product vision; method — in-depth interviews; audience — pickup point owners with different anchor brands and scales; result — a document with conclusions + recordings.

### Hypothesis card
| Field | Example entry |
|---|---|
| ID, date, owner | HYP-YYMM-###; @product-manager/researcher |
| Wording ("if… then… because… within…") | ≤ 140 characters for the log |
| Type | problem / solution |
| Segment (IN/OUT) | |
| Target metric: baseline → goal | the metric is tied to a business KPI/North Star |
| Method and volume | |
| PASS / FAIL criterion (a number, significance threshold) | PASS — Δ ≥ X at p < 0.05; FAIL — otherwise |
| ICE: I / C / E | scores with a note on what they are based on |
| Verification cost (Discovery cost) | hours / money |
| Outcome, metric change, decision, next step | PASS/FAIL/PARTIAL → roll-out / re-work / kill → link to the ticket/epic |

**Decision log (one row per hypothesis):** ID and date · hypothesis · owner · verification cost · outcome · Δ of the metric (preferably converted into ΔGMV/ΔLTV — otherwise value cannot be computed) · decision · link to the next step and raw data. The metric Δ is confirmed by a dashboard before closing the card; the owner's final comment explains the choice of decision. The log is exported to a shared place (read-only): six months later it answers "what we already tried and why we abandoned it."

### Brief and hypothesis checklist
- Business goal and research goal are separated and connected.
- There is a next step for both "yes" and "no" outcomes.
- Hypothesis: segment, cause, measurable effect, timeframe/scenario, baseline, verification method.
- PASS/FAIL is expressed as a number, not "it will get better."
- Audience and exclusions defined; the recruiting approach is clear.
- The image of the result is agreed with the recipient (format, depth, deadline).
- Baseline data fixed before launch.

## Common mistakes
- Mixing business and research goals: unmeasurable conclusions or a report "into the void."
- No image of the result and next steps: conclusions settle into storage.
- A slogan hypothesis ("the site is disliked") or a hypothesis that already contains the answer.
- Method chosen before the question is phrased; the brief filled in "for the record."
- Skipping the audience → recruiting the "wrong people" → irrelevant data.
- A list of "wishes" without dividing into mandatory and desirable.
- "Measurable after release" without a baseline; PASS described in words.
- Not recording FAIL: the team repeats the same ideas.
- Dogfooding and colleagues' opinions accepted as hypothesis verification.
- A causal wording ("because") in a hypothesis that will only be checked with descriptive methods: see [[M-quant-methods]].

## Questions that can change the decision
- Which one decision will change based on the result (and what happens if the answer is unexpected)?
- Which business metric will move first and what is its baseline?
- What is already known from analytics, support, reviews, past research?
- Who definitely should not be in the sample; what are the hard constraints on time, budget, legal boundaries?
- Which result format will actually land in the backlog and be read?
- Is there enough analytical support (baseline, A/B power) for PASS/FAIL to be honest?

## Related maps
[[M-research-types]], [[M-audience-research]], [[M-in-depth-interviews]], [[M-quant-methods]], [[M-goals-drivers-bets]], [[M-success-metrics]], [[M-problem-design]], [[M-mvp-pilots]], [[M-decision-daci]]
