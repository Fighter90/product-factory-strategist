---
id: M-brief-hypotheses
lang: en
title: Research brief and hypothesis formulation
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [intake, research, validation]
tags: [brief, hypotheses, research-goal, business-goal, ice, discovery-plan, decision-log]
related: [M-research-types, M-audience-research, M-in-depth-interviews, M-quant-methods, M-goals-drivers-bets, M-success-metrics, M-product-context, M-problem-design, M-mvp-pilots, M-decision-daci, M-product-metrics]
---

# Research brief and hypothesis formulation

## When to apply
The original request is vague ("we need to research…"), or the research is already underway without an agreement on why it is being done and what will happen to the result. The card turns a request into a brief (a contract of meaning between the product and the researcher) and into testable hypotheses with a PASS/FAIL criterion.

## Core idea
**UX and research sit at the intersection of people, business and technology.** The researcher defines goals and questions, picks the method, prepares and runs fieldwork, analyzes, presents and supports the rollout. The brief is the first page of this cycle: without it, the timeline stretches and the result never reaches decisions.

**The business goal and the research goal are different things.**
| | Business goal | Research goal |
|---|---|---|
| Question | How to earn more / cut losses? | How does this work? Why does it happen? What follows from it? |
| Metrics | revenue, conversion, acquisition cost, NPS | satisfaction, task completion time, error share, causes of behavior |
| Horizon | a quarter, a year | from 2 weeks to several months |
| Result | sales growth, cost reduction | insights and product recommendations |
| Risk if forgotten | decisions made "blind" (features nobody uses) | "research for research's sake": a beautiful report with no impact on money |

The chain: business goal "raise purchase conversion by 10%" → research goal "find out why users don't reach payment" → action (we simplified the payment form) → metric check.

**A hypothesis** — a testable assumption about user behavior, motives or problems (a research hypothesis), or about the effect of a product change on value and the metric (a product hypothesis). It contains a segment, an observed problem/opportunity and an expected measurable effect. The difference from an idea is the presence of these three parts and a test criterion.
- *A problem hypothesis* — about understanding (why they behave this way); Discovery.
- *A solution hypothesis* — about the outcome (will the change work); Delivery and A/B.
- *Bad:* "people don't like our pickup points" (generic, no segment or cause, seeks confirmation). *Good:* "new users who chose a pickup point for the first time don't place a repeat order because of a negative experience: the point was hard to find and expectations didn't match the actual location" (specific, testable, splits into sub-hypotheses, shows next steps).

**Sources of hypotheses:** analytics (dashboards, funnels, dips); research (any, desk and field); support data (a spike in the causes of tickets); reviews and social media; plus benchmark and dogfooding (additional channels: dogfooding does not replace validation on a real segment).

**Evidence strength of a hypothesis.** A hypothesis stays a hypothesis until it passes a check with a method suited to the question type ([[M-research-types]]). Interviews give a plausible explanation but don't confirm scale; desk data gives direction; only a measurement with a threshold set in advance allows you to say PASS/FAIL.

## Procedure
1. **Run a brief session with the product.** Put yourself in the CEO's shoes: what will this research give — is it value or a waste of resources?
2. **Fill the brief** across the 10 fields (below). No answer — don't launch fieldwork; gather the data instead.
3. **Separate the goals:** write down the business goal with its metric (and baseline), separately the research goal (what we want to learn/test), and the next step after the result.
4. **Collect hypotheses** from the sources (analytics, research, support, reviews, benchmark); in ~60 minutes: open 4–5 dashboards and note anomalies, read the top tickets and fresh reviews, look through the latest UX report, do a quick benchmark.
5. **Formulate each hypothesis** in the format: *If [segment] faces [X / does Y], then because of [cause] [a measurable effect: metric, baseline, magnitude] will happen within [timeframe / scenario].*
6. **Filter and prioritize.** Simple ICE scoring: Impact (effect on the main metric), Confidence (is there enough data to believe it), Ease (cost and time), each on 1–10; only the selected ones go into the brief. ICE scores are subjective — record what they are based on.
7. **Choose a method and audience** for each hypothesis ([[M-research-types]], [[M-audience-research]]); specify topics/questions for discussion or scenarios to test.
8. **Describe a Discovery plan** for the main hypothesis: target metric (baseline, target change), audience (IN/OUT), method and volume, data sources, a PASS/FAIL criterion as a number (before start), owners and dates.
9. **The ladder of working with a hypothesis:** formulation → Discovery (with what and how we'll check) → elaboration (bring in the right people) → solution (final elaboration for development) → Delivery (launch) → feedback (the first data cut, test results).
10. **After the check** — record the result in the decision journal: "hypothesis → outcome (PASS / FAIL / PARTIAL) → metric change → decision (roll out / rework / kill) → next step". Failures must be recorded: otherwise ideas repeat.

**A quick "hypothesis sprint" (15 minutes, when an idea needs to be warmed up cheaply):** 10 minutes analyzing the case from data (logs, support, benchmark) → 5 minutes of ICE-scoring 1–2 hypotheses → one top hypothesis goes into a Discovery plan. Quality check of the exercise: every hypothesis is immediately "stitched" to a metric and a validation plan, not just written down.

**Portfolio health metrics for hypotheses (computed from the decision journal per quarter):**
| Metric | How to compute | Benchmark |
|---|---|---|
| Validation rate | (PASS + PARTIAL) / all closed | ≥ 40% |
| Speed to verdict | average days "start → outcome" | ≤ 20 days |
| 90-day ROI | Σ(ΔGMV or ΔLTV) / Σ validation costs | > 3× |
| Kill early rate | killed before development / all | ≥ 25% (we cut the "junk" early) |

## Template / checklist

### Research brief (all fields of the course template)
| # | Field | What should be written |
|---|---|---|
| 1 | Context | what we already know, including past research; why now; how high a priority it is |
| 2 | Business goal in the task | what the business wants to achieve; why the research; the metrics the results will affect |
| 3 | Research goals and objectives | what we run it for; what we test; what we'll get an answer to or be able to solve |
| 4 | What the next step will be | which decisions depend on the result; what we do on confirmation and on refutation |
| 5 | Our hypotheses and questions | which assumptions we test; what we want to clarify; which questions have no answer; what to confirm or refute |
| 6 | Which method we want to test the hypothesis with | the method; high-level interview topics / user flows of the test; why exactly this one |
| 7 | Audience | who the target audience of the research is; which segments answer the questions most fully; experience, vertical, category, activity volume; how to find the right people; whom we exclude |
| 8 | Timing and resources | when to start; priority; hard and soft deadlines |
| 9 | Image of the result | what the final report must contain; in what format conclusions are needed for further work |
| 10 | Related research | links to sources of context, to subsequent iterations, marketing and analytics research |

The lecture presents the structure as "context → business goal → goals and objectives → hypotheses and questions → next steps → method → target audience → timing and agreements → image of the result"; the template adds a "Related research" field.

**Example (short):** context — handling claims with partners goes over email, the project is scaling; business goal — a product vision for claims, impact on the share of claims, the share of compensations, processing time; goals — how competitors structured claims handling, how pickup points work with claims, which pains exist with us and with the anchor brand, best practices; hypothesis — "if we give pickup points a claims-handling tool (a section in the cabinet), the time to close a claim and the number of erroneous claims will shrink"; next step — a product vision; method — in-depth interviews; audience — pickup point owners with different anchor brands and scales; result — a document with conclusions + recordings.

### Hypothesis card
| Field | Example of filling |
|---|---|
| ID, date, owner | HYP-YYMM-###; @product manager/researcher |
| Formulation ("if… then… because of… within…") | ≤ 140 characters for the journal |
| Type | problem / solution |
| Segment (IN/OUT) | |
| Target metric: baseline → target | the metric is tied to a business KPI/North Star |
| Method and volume | |
| PASS / FAIL criterion (a number, a significance threshold) | PASS — Δ ≥ X at p < 0.05; FAIL — otherwise |
| ICE: I / C / E | scores with a note of what they are based on |
| Validation cost (Discovery cost) | hours / money |
| Outcome, metric change, decision, next step | PASS/FAIL/PARTIAL → roll-out / re-work / kill → a link to the task/epic |

**Decision journal (one line per hypothesis):** ID and date · hypothesis · owner · validation cost · outcome · metric Δ (preferably translated into ΔGMV/ΔLTV — otherwise the value cannot be computed) · decision · a link to the next step and the raw data. The metric Δ is confirmed by a dashboard before the card closes; the owner's final comment explains the choice of decision. The log is exported to a shared place (read-only): six months later it answers "what we already tried and why we dropped it".

### Brief and hypothesis checklist
- The business goal and the research goal are separated and linked.
- There is a next step for both the "yes" and the "no" outcome.
- Hypothesis: segment, cause, measurable effect, timeframe/scenario, baseline, validation method.
- PASS/FAIL is expressed as a number, not "it will get better".
- Audience and exclusions are set; the recruiting method is clear.
- The image of the result is agreed with the recipient (format, depth, deadline).
- Baseline data is fixed before launch.

## Typical mistakes
- Mixing business and research goals: unmeasurable conclusions or a report "into a drawer".
- No image of the result and no next steps: conclusions settle into storage.
- A slogan hypothesis ("people dislike the site") or a hypothesis that already contains the answer.
- The method chosen before the question is formulated; the brief filled "for the record".
- Skipping the audience definition → recruiting the "wrong" people → irrelevant data.
- A list of "wishes" without splitting into must-have and nice-to-have.
- "We'll measure after release" without a baseline; PASS described in words.
- FAILs are not recorded: the team repeats the same ideas.
- Dogfooding and colleagues' opinions taken as hypothesis validation.
- A causal formulation ("because") in a hypothesis that will be checked only by descriptive methods: see [[M-quant-methods]].

## Questions that can change the decision
- Which single decision will change based on the result (and what happens if the answer turns out unexpected)?
- Which business metric moves first, and what is its baseline?
- What is already known from analytics, support, reviews, past research?
- Who definitely should not be in the sample; which hard constraints exist on timing, budget, legal limits?
- Which result format will actually reach the backlog and be read?
- Is there enough analytical support (baseline, A/B power) for the PASS/FAIL to be honest?

## Related maps
[[M-research-types]], [[M-audience-research]], [[M-in-depth-interviews]], [[M-quant-methods]], [[M-goals-drivers-bets]], [[M-success-metrics]], [[M-problem-design]], [[M-mvp-pilots]], [[M-decision-daci]]
