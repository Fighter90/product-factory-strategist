---
id: M-model-validation
lang: en
title: Model validation (backtest, benchmarks, sensitivity)
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [validation, strategy, after-decision]
tags: [model-validation, backtest, benchmarks, sensitivity, scenarios, cognitive-biases, checks, mape, threshold, red-flags]
related: [M-traction-model, M-model-topdown-bottomup, M-benchmarking, M-source-criticism, M-unit-economics, M-cannibalization]
---

# Model validation (backtest, benchmarks, sensitivity)

## When to apply
Before presenting the model to stakeholders; when the model becomes the budget/plan (a commitment); after major changes to the assumptions; when fact deviates from plan by more than 10–15%. Validation is not "checking the formulas" — it is a process of building agreement (buy-in): an error in a model that has become the plan is very expensive.

## Core idea
**The validation pyramid** — bottom-up, skipping no level:
1. **Mechanical errors** — formulas, references, rounding (the most common layer).
2. **Logical consistency** — contradictions between the assumptions and common sense.
3. **Assumptions and benchmarks** — every assumption with a source.
4. **Backtest** — does the model work on past data.
5. **Conceptual check** — is the modeling logic itself correct.

**The mechanical layer** — the most common and the easiest to fix:
- period balance: `End = Start + inflows − outflows` (a tolerance of ~0.01 for rounding);
- the product of step conversions equals the total conversion (adding instead of multiplying is a classic: 50%×30%×20%×10% = 0.3%, not 110%);
- retention ≤ 100%, conversions ∈ [0;1], users and revenue non-negative;
- a metric computed "two ways" (demand vs supply) reconciles;
- no #REF! after deleting rows; dragged formulas checked in the extreme cells (a shifted relative reference is the typical cause of retention = 120%);
- retro/fact separated from the forecast.

**The logical layer:** metric values match the stage of the business (a startup ≠ mature SaaS); the parts of the model do not contradict each other; seasonality is accounted for. Approximate bands:

| Metric | Startup (0–1 year) | Scaling | Mature (3+ years) |
|---|---|---|---|
| Month-1 retention | 10–30% | 25–50% | 40–70% |
| Payment conversion | 1–5% | 5–15% | 10–30% |
| MoM MAU growth | 10–30% | 5–15% | 1–5% |
| Monthly churn | 5–15% | 3–8% | 1–5% |
| LTV/CAC | 0.5–1.5 | 1.5–3 | 3–5+ |

Red flags: retention > 50% at a startup, a funnel step conversion of 90% ("that never happens"), 3+ metrics in the red zone = revisit the assumptions. The "reverse reading" technique: start from the final revenue and walk up the chain — which assumptions were required, and are they realistic?

**Benchmarks:** reference values from the industry, competitors, or internal data. The golden rule: **every benchmark = a source in the model**; no source — admit it honestly.

| Source | Pros | Cons |
|---|---|---|
| Public reports (IPO, annual) | verifiable | not always detailed |
| The company's A/B test base | the most relevant for feature effects | requires analytics maturity |
| Benchmark agencies | structured | paid |
| Own history | the most relevant | only for existing products |
| Expert estimates | fast and cheap | subjective |

Relevance check on 4 criteria: industry, segment, stage, business model (the "2-of-4 rule" — usable with a caveat). When sources diverge: consistent — the mean, moderately — the median, strongly — **the conservative value** (a dispersion of 10–80% is noise, not information). A healthy proportion: most assumptions within market range, only a few above the benchmark, each with an explanation; >40–50% of assumptions above the benchmark = an unrealistic model.

**Backtest:** feed in past data, compare the model's forecast with the fact, and compute MAPE (the mean absolute percentage error).

| MAPE | Interpretation | Action |
|---|---|---|
| < 5% | an excellent model | plan with confidence |
| 5–15% | good | build in a buffer for deviations |
| 15–30% | satisfactory | revise the key assumptions |
| > 30% | weak | unfit for budgeting |

**Rolling backtest:** every month the fact is loaded → the model re-forecasts → the error must decrease; an unstable forecast = overfitting or a fragile assumption. Traps: "leakage from the future" (the model contains data that was not available at the moment of the forecast), overfitting (split the data into train/test), instability.

## Procedure
1. **Auto-checks (see Template):** a Checks tab with binary formulas and a happy checker `SUM(all checks)`; 0 = a clean model. This removes the cognitive load from the reviewer.
2. **Sanity check of the totals:** are the final Revenue/MAU/Profit realistic for the market and the stage? Reverse reading of the chain of assumptions.
3. **Benchmark check:** every assumption has a source and a reliability class ([[M-source-criticism]]); each deviation from a benchmark is explained in one line.
4. **Fact-vs-plan check:** decompose the deviation into market / product / operational / model factors; check each against benchmarks; update the model with the fact.
5. **Backtest** (if there is history): MAPE over 6+ months, a rolling backtest, a check for leakage from the future.
6. **Sensitivity analysis:** for 2–3 key drivers — ±10/20/30% scenarios; an answer to "what happens if things go wrong". The rule of three questions: which parameter influences the outcome the most; which is known the worst; at what value the project becomes unviable (**threshold** — the level below which it must not fall; understandable to any investor).
7. **bull/base/bear scenarios:** three sets of assumptions → three outcomes; with a large dispersion of values, show a range rather than a "precise" forecast.
8. **Review without a "single pot"** — a diversity of perspectives is mandatory; a feast from the same team is subject to the same biases:

| Reviewer | What they check | Time | Limitation |
|---|---|---|---|
| Business peer | the logic, the "feel" of the numbers | 30 min | the same biases |
| Finance / FP&A | formulas, discounting | 1–2 h | weak product context |
| Data analyst | data quality, benchmarks vs fact | 1–2 days | no business context |
| External auditor | the major assumptions, the market | 3–5 days | expensive, optional |

9. **Cognitive bias control:** confirmation bias ("the arguments support us" rather than us supporting them), anchoring (falling in love with the first option / an authority's opinion), the reluctance to break the "neat picture". Antidotes: a challenger (digs one driver down to the bottom), a search for 3 arguments AGAINST the model, sensitivity analysis, an external reviewer.
10. **Documentation:** a validation report — the happy checker, the problems found and their resolutions, who reviewed it, the buy-in of all participants. Only after that does the model become the plan.

## Template / checklist
The `Checks` tab, binary (0 ok / 1 error), the global status `=IF(SUM(checks)>0;"ERROR";"OK")` — for the formulas see [[M-traction-model]]:
```
Period balance:         =IF(ABS(End−(Start+In−Out))<0.01;0;1)
Non-negativity:         =IF(MIN(range)<0;1;0)
Retention ≤ 100%:       =IF(MAX(range)>1;1;0)
Funnel non-increasing:  =IF(SUMPRODUCT(--(next_step>prev_step))>0;1;0)
Not above market:       =IF(SUM(model)>SOM_cap;1;0)
Demand/supply reconcile:=IF(ABS(path1−path2)>0.01;1;0)
Broken references:      =IF(SUMPRODUCT(--ISERROR(range))>0;1;0)
```
The model readiness checklist: a tab-based structure and clear navigation · the build logic described · assumptions separated from the formulas · every assumption has a source (or an honest "none") · sensitivity and scenarios · a threshold · the review signed off · the results documented · buy-in.

A scenario table: `Parameter (retention, CAC, conversion, ARPU) | Bear (−20%) | Base | Bull (+20%) → Revenue, Profit by year | Threshold: Profit < 0 → red flag`.

## Typical mistakes
| Mistake | How to notice |
|---|---|
| Eyeball validation without a Checks tab | the reviewer hunts mechanics instead of logic |
| A beautiful model without external review | the author's jaded eye does not see retention 120% |
| A benchmark from an irrelevant industry/stage | an apparel conversion of 2–3% applied to grocery delivery with its 15–25% |
| A divergence of the two calculation paths ignored | revenue from demand ≠ revenue from supply — always look for the cause |
| Fitting the assumptions to the desired outcome | "the economics don't converge — let's raise the conversion" instead of an honest conclusion |
| Judging by a single month of backtest | an unstable forecast taken as "normal" |
| One reviewer (or all from one team) | shared cognitive biases go unseen |
| The early months taken as the base | the first 1–2 months are early adopters, unrepresentative; wait for 2–3 months of data |

When there is no data at all (a new business/market): proxy metrics (`target = proxy_1 × proxy_2 × adjustment`, an expected error of 30–60%), expert estimates, a cheap MVP test, an analogy with an adjacent market — and scenario planning instead of a "precise" forecast.

## Questions that can change the decision
- Which single assumption, if it is wrong by 30%, sinks the model — and how fast would we learn it from reality?
- Where is the project's threshold, and what do we do when it is breached?
- Which assumptions do we know the worst (they get sensitivity analysis first)?
- Can the riskiest assumption be tested cheaply and quickly (an MVP; the first marketing campaign yields a real CAC in 1–2 weeks)?
- What in the model appeared "for beauty's sake" and will not survive the question "where does this number come from?"

## Related maps
[[M-traction-model]], [[M-model-topdown-bottomup]], [[M-benchmarking]], [[M-source-criticism]], [[M-unit-economics]], [[M-cannibalization]], [[M-trends-scenarios]], [[M-risks]]
