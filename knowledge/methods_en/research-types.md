---
id: M-research-types
lang: en
title: Research types and choosing a method per question
course: ux
sources: ["EN mirror of the RU methodology card M-research-types (knowledge/methods/research-types.md); original sources are listed in the RU card"]
stages: [intake, research, options, validation]
tags: [research, qualitative, quantitative, desk-research, benchmark, double-diamond, custdev, method-selection]
related: [M-brief-hypotheses, M-audience-research, M-in-depth-interviews, M-interview-analysis, M-quant-methods, M-marketing-research, M-competitors, M-external-environment, M-market-sizing, M-source-criticism, M-usability-testing, M-ai-in-research, M-synthetic-respondents, M-jtbd]
---

# Research types and choosing a method per question

## When to apply
A product lead arrives with a vague request ("understand users", "validate the idea", "learn the market"). The card helps determine in one pass: what type of question this is, which method will answer it, with what strength of evidence, and in what sequence (desk research, qualitative stage, quantitative stage, experiment).

## Essence
**Research is needed for a decision, not for a report.** A product team gets pains and needs, design — an understanding of interface perception, marketing — precise targeting and positioning, business — a basis for strategic decisions. If no action follows from the result, the method was chosen wrongly.

**Two process frames from the course.**
- **Double Diamond** (Design Council): four phases — Discover (explore the problem), Define (synthesis, one clearly formulated problem), Develop (searching and testing solutions), Deliver (implementation and launch). The first two phases are the "right problem" diamond, the second two — the "right solution" diamond. The idea: first widen the horizon, then focus; the path is not linear, ideas are constantly tested on people. This is a *mode of thinking*: it answers the question "expand or narrow right now?".
- **Customer Development** (Blank; Lean Startup): Customer Discovery (find and validate the problem, including willingness to pay) → Customer Validation (a repeatable sales model, first deals) → Customer Creation (positioning, demand generation) → Company Building (scale). This is a *checklist of actions*: "what exactly to do to check a guess and not go broke". Pros: fewer unnecessary features, data-based decisions, faster to product-market fit. Cons: slower, the process is endless. In Russian practice "custdev" is often reduced only to in-depth interviews — that is only part of Discovery.
- Alignment: Discover ≈ Customer Discovery; Define = synthesizing insights into a problem statement; Develop ≈ Customer Validation (MVP, hypothesis testing); Deliver ≈ Creation/Building.

**Classifications of research.**
| Axis | Options | Meaning |
|---|---|---|
| Data source | desk research (secondary data) / field research (new data) / benchmark (a subtype of desk research: how competitors solve the same task) | desk answers "general tendencies", field — the concrete task of the product |
| Nature of data | qualitative / quantitative | "why, how, what for" vs "who, how many, how often" |
| Purpose | generative (building the picture, searching for problems: discovery, ethnography, diaries) / evaluative (testing a solution: usability test, A/B, solution interview) | in DD terms: Discover-Define vs Develop-Deliver (the terms generative/evaluative are standard practice; the course expresses them through DD) |
| What we record | what people *say* (interviews, surveys) / what they *do* (analytics, observation, tests) | pairs "survey + behavioral data" give both opinion and fact |

**Qualitative vs quantitative (comparison).**
| Criterion | Qualitative | Quantitative |
|---|---|---|
| Sample | from a few people to a few dozen | hundreds–thousands |
| Collection | unstructured / semi-structured (guide) | a rigidly structured questionnaire |
| Questions | deep, contextual | simple, understandable out of context |
| Skill | moderation | correct wording and validity |
| Analysis | descriptive, slow (coding) | statistical, often fast |
| Hypotheses | you can start without a precise hypothesis | mandatory, the plan is fixed before launch |
| What it proves | **generates hypotheses**, explains the mechanism and the customer's language | **measures prevalence** and significance of differences |

**The main principle of evidence strength.** Qualitative data finds and explains hypotheses but does *not prove* magnitude ("how many") and does not allow extrapolating a share from a sample to the market. Quantitative data proves magnitude and differences, but indirectly, and does not explain "why". Desk data is a starting point, not a basis for a decision.

## Procedure
1. **Formulate the decision** to be made (launch / not launch, what to prioritize, whom to target). Without a decision — return to [[M-brief-hypotheses]].
2. **Classify the question**: "what/how many/how often/who" → quant; "why/what for/how exactly/what gets in the way" → qual; "how is the market and competition structured" → desk; "does a specific solution work" → an evaluative method.
3. **Start with desk research and internal data** (analytics, support, reviews, past studies): it is cheaper and often more accurate than external reports. Record what is *missing*.
4. **Determine the DD/CustDev phase**: the problem is unclear — generative methods; the problem is clear — evaluative; the solution is validated — scaling and tracking.
5. **Choose a method using the table below**, accounting for constraints (time, budget, audience availability, number of segments).
6. **Build a chain**, not a single method. Two funnels: *top-down* (quant → qual: numbers showed an attitude, interviews explain why) and *bottom-up* (qual → quant: interviews produced behavior options, the survey shows which is more frequent and weightier). A typical cycle: a signal (metric drop, spike in complaints) → qual diagnosis → quant check of magnitude → experiment (A/B on part of the traffic) → rollout or return to diagnostics.
7. **Write into the brief**: method, justification, expected strength of evidence, next step on confirmation and refutation.

### Choosing a method per question
| Question | Method | Volume guideline (course rules) | What must not be claimed from it |
|---|---|---|---|
| There is an idea, no data; need needs, motives, language | in-depth interviews ([[M-in-depth-interviews]]) | 40–60 min; 5–15 respondents, informally ≥10 per audience | shares, segment size, "majority" as a number |
| Confirm the magnitude of a problem / share of a segment | online survey ([[M-quant-methods]]) | no fewer than ~300–400 at ±5 p.p. (computed by formula) | causes of behavior |
| Understand the real context, micro-frustrations | field observation (ethnography, dogfooding) | visits into the environment; roles from different functions | "representativeness" |
| Everyday and long-term use, seasonality | diary study | 10–12 participants, 7–10 days | market-level frequencies |
| Test a prototype before release | usability test, series of ~5 participants ([[M-usability-testing]]) | up to ~80% of critical issues per series — an empirical guideline | predicting conversion |
| Choose between two design options | SBS / A/B test | SBS ≈300+; A/B — by power calculation | "why" one variant won |
| Prioritize features | Kano, MaxDiff, TURF ([[M-marketing-research]]) | ≥300 for Kano; ≥200 MaxDiff | willingness to pay |
| Find segments, estimate their shares | interviews → survey + clustering ([[M-audience-research]]) | quant stage of hundreds of respondents | stability over time without a re-measurement |
| Understand the market, size, competitors | desk + benchmark ([[M-market-sizing]], [[M-competitors]]) | — | your customers' behavior |
| Learn loyalty and satisfaction | CSAT/CES/NPS/SUS ([[M-loyalty-metrics]]) | by calculation | causes of the scores without open questions |
| Test a promise/USP | A/B listing, concept interview ([[M-usp]]) | n and effect threshold computed | demand and money (a click ≠ a purchase) |

## Desk research and benchmark (session 2)
**Desk research**: analysis of already existing data; fast and cheap, but the question cannot be refined, the data may be outdated, and it does not answer a narrow product task. Well suited for *forming hypotheses*, defining the USP (competitive analysis + trends) and finding the target audience. Not fit as the sole basis of a decision.

**Sources by goal.**
| Goal | Source | Example |
|---|---|---|
| The big picture of the market and trends | industry reports | the private construction market in a given country |
| Size, demographics, potential | statistics (national statistics office, Statista, Google Trends, OECD / World Bank data) | residents of million-plus cities |
| Competitive landscape | research and reports of competitors in open access | fintech trend reports |
| Fresh niches | business press | the mobile tipping and bookings market |
| "Inside" depth | conference talks, expert and competitor blogs | food delivery in other countries |

**How to choose a source (4 questions).** How much do you already know? (little — broad independent reports and statistics). Do you need general information or an assessment of competitors? Do you need an assessment of the competitive landscape? Are competitors' advantages known? (known, but "how do they solve the task" remains — competitors' studies, conferences, blogs, a benchmark of interfaces).

**Benchmark (5 steps).**
1. Formulate why: which decision depends on the result.
2. Assemble a pool of competitors: direct (the same need), indirect (another way to close the need), non-standard (adjacent industries).
3. Choose criteria: features and UX patterns, price and monetization model, channels and positioning, operational processes.
4. Collect data: public materials, the "field" (register and walk the journey), expert contacts. Record the source and date for every number.
5. Structure it: a matrix "players × criteria" (market standard = cells filled by almost everyone; white-space = empty cells), a feature count as a quick cut, SWOT only with objective data. Turn the conclusion into a hypothesis and test it on people.

**The "data → decision" table** (desk research): attach the source and date to every number → flag data older than ~12 months as needing verification → find patterns and gaps → write hypotheses in the "if… then…" format → cross-check with demographics and segments → formulate 1–2 promises (USP) and hand them to the field.

**A chain example from the course:** entering another country with a banking service for business. Reports → the market is conservative, digital services are fragmented (hypothesis). Competitors → nobody aggregates financial services for business in one place (USP candidate). Statistics → the large-business market is saturated, SMB is not (target-audience candidate). Then field validation.

## Template / checklist

**Method selection card** (fill in for every hypothesis):
| Field | What to record |
|---|---|
| Decision | what changes after the answer |
| Question type | who/how many ↔ why/how ↔ does it work |
| Already known | internal data, past studies |
| Phase | Discover / Define / Develop / Deliver |
| Method and justification | why not the neighboring methods |
| Strength of evidence | what the method can and cannot prove |
| Next step on "yes" / "no" | an action, not "let's discuss" |
| Constraints | time, budget, access to the audience |

**A "desk + field" plan (time guidelines):** desk screening 3–5 days; benchmark 5–7 days; field validation 7–10 days; iteration and prioritization 2–3 days.

**Benchmark checklist:** the task is written down; the competitor pool is complete but manageable; criteria measured identically; data verified; the matrix and conclusions tied to the business goal; hypotheses fixed.

## Common mistakes
- Choosing a method "by habit" (always interviews or always a survey) without linking to the question type.
- Trying to get "how many" from 8 interviews or "why" from a survey with closed options.
- Desk research as the only source: an outdated report, transferring numbers from another country, a trend taken as a cause, ignoring internal data.
- Blind faith in SWOT and "feature counts" without meaning for the user.
- Research without a next step — "research for research's sake".
- Dogfooding as the only source of hypotheses: employees are not the target segment.
- Full trust in what people *say* without behavioral verification (analytics, observation).
- Ignoring DD non-linearity: returning to Define after tests is normal.

## Questions that can change the decision
- Which decision will be made and by whom; what happens if the answer is "no"?
- What do we already know from internal data (analytics, tickets, reviews, past studies)?
- Can respondents of the required profile be sourced (rare, expensive, B2B), and within what time?
- Is a magnitude estimate needed, or is direction enough (a hypothesis for the next step)?
- Is error tolerable: is the decision reversible (a quick pilot) or expensive (a launch, investment)?
- Is there an analyst/statistician for sample size and power calculations?

## Related cards
[[M-brief-hypotheses]], [[M-audience-research]], [[M-in-depth-interviews]], [[M-interview-analysis]], [[M-quant-methods]], [[M-marketing-research]], [[M-competitors]], [[M-market-sizing]], [[M-source-criticism]], [[M-usability-testing]], [[M-ai-in-research]], [[M-synthetic-respondents]]
