---
id: M-research-types
lang: en
title: Research types and choosing a method for the question
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [intake, research, options, validation]
tags: [research, qualitative, quantitative, desk-research, benchmark, double-diamond, custdev, method-choice]
related: [M-brief-hypotheses, M-audience-research, M-in-depth-interviews, M-interview-analysis, M-quant-methods, M-marketing-research, M-competitors, M-external-environment, M-market-sizing, M-source-criticism, M-usability-testing, M-ai-in-research, M-synthetic-respondents, M-jtbd]
---

# Research types and choosing a method for the question

## When to apply
A product leader arrives with a vague request ("understand our users", "test the idea", "learn the market"). This map helps determine in a single pass: what type of question it is, which method will answer it, with what strength of evidence, and in what sequence (desk research, a qualitative stage, a quantitative stage, an experiment).

## Core idea
**Research exists to serve a decision, not to produce a report.** The product team gets pains and needs, design gets an understanding of how the interface is perceived, marketing gets precise targeting and positioning, the business gets grounds for strategic decisions. If no action follows from the result, the method was chosen wrong.

**The two process frames from the course.**
- **Double Diamond** (Design Council): four phases — Discover (explore the problem), Define (synthesis, one clearly formulated problem), Develop (searching for and testing solutions), Deliver (implementation and launch). The first two phases are the "right problem" diamond, the last two are the "right solution" diamond. The idea: first you widen your view, then you focus; the path is non-linear, and ideas are constantly tested on people. This is a *thinking mode*: it answers the question "expand or narrow right now?".
- **Customer Development** (Blank; Lean Startup): Customer Discovery (find and validate the problem, including willingness to pay) → Customer Validation (a repeatable sales model, first deals) → Customer Creation (positioning, demand generation) → Company Building (scale). This is an *action checklist*: "what exactly to do to test a guess and not go broke". Pros: fewer unnecessary features, decisions based on data, a faster path to product-market fit. Cons: it takes longer, and the process never ends. In Russian practice "custdev" is often reduced to in-depth interviews only — that is merely one part of Discovery.
- How they connect: Discover ≈ Customer Discovery; Define = synthesizing insights into a problem statement; Develop ≈ Customer Validation (MVP, hypothesis testing); Deliver ≈ Creation/Building.

**Classifications of research.**
| Axis | Options | Meaning |
|---|---|---|
| Data source | desk research (secondary data) / field research (new data) / benchmark (a desk subtype: how competitors solve the same job) | desk answers "general trends", field answers the product's specific task |
| Nature of data | qualitative / quantitative | "why, how, what for" vs "who, how many, how often" |
| Purpose | generative (building the picture, looking for problems: discovery, ethnography, diaries) / evaluative (testing a solution: usability test, A/B, solution interview) | in DD terms: Discover–Define vs Develop–Deliver (generative/evaluative is standard practice terminology; the course expresses it through DD) |
| What we capture | what people *say* (interviews, surveys) / what they *do* (analytics, observation, tests) | pairing "survey + behavioral data" gives both opinion and fact |

**Qualitative vs quantitative (comparison).**
| Criterion | Qualitative | Quantitative |
|---|---|---|
| Sample | from a few people to a few dozen | hundreds–thousands |
| Collection | unstructured / semi-structured (an interview guide) | a rigidly structured questionnaire |
| Questions | deep, contextual | simple, understandable out of context |
| Skill | moderation | correct wording and validity |
| Analysis | descriptive, slow (coding) | statistical, often fast |
| Hypotheses | you can start without a precise hypothesis | mandatory, the plan is fixed before launch |
| What it proves | **generates hypotheses**, explains the mechanism and the customer's own language | **measures prevalence** and the significance of differences |

**The main principle of evidence strength.** Qualitative data finds and explains hypotheses, but it does *not prove* scale ("how many") and does not let you transfer a share from a sample to the market. Quantitative data proves scale and differences, but only indirectly, and does not explain "why". Desk data is a starting point, not grounds for a decision.

## Procedure
1. **State the decision** to be made (launch / don't launch, what to prioritize, whom to target). Without a decision — go back to [[M-brief-hypotheses]].
2. **Classify the question**: "what / how many / how often / who" → quant; "why / what for / how exactly / what gets in the way" → qual; "how is the market and the competition structured" → desk; "does this specific solution work" → an evaluative method.
3. **Start with desk research and internal data** (analytics, support, reviews, past research): it is cheaper and often more accurate than external reports. Record what is *missing*.
4. **Determine the DD/CustDev phase**: the problem is unclear — generative methods; the problem is clear — evaluative; the solution has been validated — scaling and tracking.
5. **Choose the method from the table below**, taking constraints into account (timeline, budget, audience availability, number of segments).
6. **Build a chain**, not a single method. Two funnels: *descending* (quant → qual: the numbers showed the attitude, the interviews explain why) and *ascending* (qual → quant: the interviews produced behavior options, a survey shows which one is more frequent and weightier). The typical cycle: a signal (a metric drops, a spike of complaints) → a qual diagnosis → a quant check of the scale → an experiment (A/B on part of the traffic) → rollout or back to diagnostics.
7. **Write it into the brief**: method, rationale, expected strength of evidence, the next step on confirmation and on refutation.

### Choosing a method for the question
| Question | Method | Volume guideline (course rules) | What you cannot claim from the results |
|---|---|---|---|
| The idea exists, there is no data; you need needs, motives, language | in-depth interviews ([[M-in-depth-interviews]]) | 40–60 min; 5–15 respondents, informally ≥10 per audience | shares, segment size, "the majority" as a number |
| Confirm the scale of the problem / a segment's share | online survey ([[M-quant-methods]]) | at least ~300–400 at ±5 pp (calculated by formula) | the causes of behavior |
| Understand the real context, micro-frustrations | field observation (ethnography, dogfooding) | visits into the environment; roles from different functions | "representativeness" |
| Everyday and long-term use, seasonality | diary study | 10–12 participants, 7–10 days | market-level frequencies |
| Test a prototype before release | usability test, series of ~5 participants ([[M-usability-testing]]) | up to ~80% of critical problems per series — an empirical guideline | a conversion prediction |
| Choose between two design options | SBS / A/B test | SBS ≈300+; A/B — by power calculation | "why" one variant won |
| Prioritize features | Kano, MaxDiff, TURF ([[M-marketing-research]]) | ≥300 for Kano; ≥200 MaxDiff | willingness to pay |
| Find segments and estimate their shares | interviews → survey + clustering ([[M-audience-research]]) | quant stage: hundreds of respondents | stability over time without a re-measurement |
| Understand the market, its size, competitors | desk + benchmark ([[M-market-sizing]], [[M-competitors]]) | — | the behavior of your own customers |
| Learn loyalty and satisfaction | CSAT/CES/NPS/SUS ([[M-loyalty-metrics]]) | by calculation | the reasons behind scores without open questions |
| Test a promise/USP | A/B listing, concept interviews ([[M-usp]]) | n and effect-threshold calculation | demand and money (a click ≠ a purchase) |

## Desk research and benchmark (session 2)
**Desk research**: the analysis of data that already exists; fast and cheap, but you cannot refine the question, the data may be outdated, and it does not answer a narrow product task. It works well for *forming hypotheses*, defining a USP (competitive analysis + trends) and finding the target audience. It cannot serve as the only basis for a decision.

**Sources by goal.**
| Goal | Source | Example |
|---|---|---|
| The overall market picture and trends | industry reports | the private-construction market in Russia |
| Market size, demographics, potential | statistics (Rosstat, Statista, Google Trends, OECD / World Bank data) | residents of million-plus cities |
| The competitive environment | competitors' research and reports published openly | fintech trend reports |
| Fresh niches | the business press | the mobile tipping and bookings market |
| "Inside" depth | conference talks, blogs of experts and competitors | food ordering in other countries |

**How to choose a source (4 questions).** How much do you already know? (little — broad independent reports and statistics). Do you need general information or an assessment of competitors? Do you need an assessment of the competitive environment? Are competitors' advantages known? (known, but the question "how do they solve the job" remains — competitors' research, conferences, blogs, interface benchmarks).

**Benchmark (5 steps).**
1. State why: which decision depends on the result.
2. Assemble a pool of competitors: direct (the same need), indirect (a different way to meet the need), non-standard (adjacent industries).
3. Choose criteria: features and UX patterns, price and monetization model, channels and positioning, operational processes.
4. Collect the data: public materials, the "field" (register and walk the journey yourself), expert contacts. Record the source and the date next to every figure.
5. Structure it: a "players × criteria" matrix (the market standard = cells filled by almost everyone; white space = empty cells), a feature count as a quick slice, SWOT only with objective data. Turn the conclusion into a hypothesis and test it on people.

**The "data → decision" table** (desk research): attach a source and a date to every figure → mark data older than ~12 months as requiring verification → look for patterns and gaps → write hypotheses in the "if… then…" format → cross-check against demographics and segments → formulate 1–2 promises (a USP) and hand them over to the field stage.

**A course example of the chain:** entering another country with a banking service for businesses. Reports → the market is conservative, digital services are fragmented (a hypothesis). Competitors → nobody assembles financial services for businesses in one place (a USP candidate). Statistics → the large-business market is saturated, SMB is not (a target-audience candidate). Then field validation.

## Template / checklist

**Method-choice card** (fill in for every hypothesis):
| Field | What to write |
|---|---|
| Decision | what changes after the answer |
| Question type | who/how many ↔ why/how ↔ does it work |
| Already known | internal data, past research |
| Phase | Discover / Define / Develop / Deliver |
| Method and rationale | why not the neighboring methods |
| Strength of evidence | what the method can and cannot prove |
| Next step on "yes" / "no" | an action, not "let's discuss" |
| Constraints | timeline, budget, access to the audience |

**A "desk + field" plan (timeline guidelines):** desk screening 3–5 days; benchmark 5–7 days; field validation 7–10 days; iteration and prioritization 2–3 days.

**Benchmark checklist:** the job is written down; the competitor pool is complete but manageable; the criteria are measured the same way; the data is verified; the matrix and the conclusions are tied to the business goal; the hypotheses are recorded.

## Typical mistakes
- Choosing a method "out of habit" (always interviews or always surveys) without linking it to the question type.
- Trying to get "how many" from 8 interviews, or "why" from a survey with closed answer options.
- Desk research as the only source: an outdated report, numbers transferred from another country, a trend taken for a cause, internal data ignored.
- Blind faith in SWOT and in "feature counts" without meaning for the user.
- Research without a next step — "research for research's sake".
- Dogfooding as the only source of hypotheses: employees are not the same as the target segment.
- Full trust in what people *say* without behavioral verification (analytics, observation).
- Ignoring the non-linearity of DD: returning to Define after tests is normal.

## Questions that can change the decision
- Which decision will be made, and by whom; what happens if the answer is "no"?
- What do we already know from internal data (analytics, tickets, reviews, past research)?
- Can we get respondents of the required profile (rare, expensive, B2B), and within what time frame?
- Is a scale estimate needed, or is a direction enough (a hypothesis for the next step)?
- Is an error acceptable: is the decision reversible (a quick pilot) or expensive (a launch, investments)?
- Is there an analyst/statistician available for sample-size and power calculations?

## Related maps
[[M-brief-hypotheses]], [[M-audience-research]], [[M-in-depth-interviews]], [[M-interview-analysis]], [[M-quant-methods]], [[M-marketing-research]], [[M-competitors]], [[M-market-sizing]], [[M-source-criticism]], [[M-usability-testing]], [[M-ai-in-research]], [[M-synthetic-respondents]]
