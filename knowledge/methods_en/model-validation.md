---
id: M-model-validation
lang: en
title: Model validation (backtest, benchmarks, sensitivity)
course: strategy
sources: ["EN mirror of the RU methodology card M-model-validation (knowledge/methods/model-validation.md); original sources are listed in the RU card"]
stages: [validation, strategy, after-decision]
tags: [validation, backtest, benchmarks, sensitivity, scenarios, cognitive-biases, checks, mape, threshold, red-flags]
related: [M-traction-model, M-model-topdown-bottomup, M-benchmarking, M-source-criticism, M-unit-economics, M-cannibalization]
---

# Model Validation (Backtest, Benchmarks, Sensitivity)

## When to apply
Before presenting the model to stakeholders; when the model becomes the budget/plan (a commitment); after major changes to assumptions; when fact deviates from plan by more than 10–15%. Validation is not "checking formulas" but a buy-in process: an error in a model that has become the plan is very expensive.

## Essence
**The validation pyramid** — bottom up, without skipping levels:
1. **Mechanical errors** — formulas, references, rounding (the most frequent layer).
2. **Logical consistency** — contradictions between assumptions and common sense.
3. **Assumptions and benchmarks** — every assumption has a source.
4. **Backtest** — does the model work on past data.
5. **Conceptual check** — is the modeling logic itself correct.

**The mechanical layer** — the most frequent and the easiest to fix:
- period balance: `End = Start + inflows − leavers` (tolerance ~0.01 for rounding);
- the product of step conversions = the total conversion (adding instead of multiplying is a classic: 50%×30%×20%×10% = 0.3%, not 110%);
- retention ≤ 100%, conversions ∈ [0;1], users and revenue non-negative;
- a metric computed "two ways" (demand vs supply) converges;
- no #REF! after deleting rows; dragged formulas checked in the edge cells (a shifted relative reference is a typical cause of retention = 120%);
- retro/fact separated from the forecast.

**The logical layer:** metric values match the business stage (a startup ≠ mature SaaS); parts of the model do not contradict each other; seasonality is accounted for. Approximate frames:

| Metric | Startup (0–1 yr) | Scaling | Mature (3+ yrs) |
|---|---|---|---|
| Month-1 retention | 10–30% | 25–50% | 40–70% |
| Conversion to payment | 1–5% | 5–15% | 10–30% |
| MoM MAU growth | 10–30% | 5–15% | 1–5% |
| Monthly churn | 5–15% | 3–8% | 1–5% |
| LTV/CAC | 0.5–1.5 | 1.5–3 | 3–5+ |

Red flags: retention > 50% in a startup, a 90% conversion at a funnel step ("that doesn't happen"), 3+ metrics in the red zone = a revision of assumptions. The "backward reading" technique: from the final revenue up the chain — which assumptions were required, and are they realistic.

**Benchmarks:** reference values from the industry, competitors, or internal data. The golden rule: **every benchmark = a source in the model**; if there is no source, admit it honestly.

| Source | Pros | Cons |
|---|---|---|
| Public reports (IPO, annual) | verifiable | not always detailed |
| The company's A/B test base | the most relevant for feature effects | requires analytics maturity |
| Benchmarking agencies | structured | paid |
| Your own history | maximally relevant | only for existing products |
| Expert estimates | fast and cheap | subjective |

A relevance check on 4 criteria: industry, segment, stage, business model ("the rule of 2 out of 4" — usable with a caveat). When sources diverge: consistent — the mean; moderately — the median; strongly — **the conservative value** (a 10–80% variance is noise, not information). A healthy proportion: most assumptions within the market range, a few above the benchmark with an explanation; >40–50% of assumptions above the benchmark = an unrealistic model.

**Backtest:** plug in past data, compare the model's forecast with the fact, compute MAPE (the mean absolute percentage error).

| MAPE | Interpretation | Action |
|---|---|---|
| < 5% | an excellent model | plan confidently |
| 5–15% | good | build in a buffer for deviation |
| 15–30% | acceptable | revise the key assumptions |
| > 30% | weak | not fit for budgeting |

**Rolling backtest:** every month the fact is loaded → the model re-forecasts → the error must decrease; an unstable forecast = overfitting or a fragile assumption. Traps: "leakage from the future" (the model uses data unavailable at forecast time), overfitting (split the data train/test), instability.

## Procedure
1. **Auto-checks (see the Template):** a Checks tab with binary formulas and a happy checker `SUM(all checks)`; 0 = a clean model. This removes cognitive load from the reviewer.
2. **A sanity check of the totals:** are the final Revenue/MAU/Profit realistic for the market and stage? Backward reading of the assumption chain.
3. **A benchmark cross-check:** every assumption — a source and a confidence class ([[M-source-criticism]]); a deviation from the benchmark explained in one line.
4. **A fact/plan cross-check:** decompose the deviation into a market / product / operational / model factor; each against a benchmark; the model is updated with the fact.
5. **A backtest** (if there is history): MAPE over 6+ months, a rolling backtest, a check for leakage from the future.
6. **Sensitivity analysis:** for 2–3 key drivers — scenarios of ±10/20/30%; an answer to "what if it goes wrong". The rule of three questions: which parameter influences the most; which is known worst; at which value the project becomes unviable (**threshold** — below it you must not fall; understandable to any investor).
7. **Scenarios bull/base/bear:** three sets of assumptions → three outcomes; with a large variance of values, show a range, not a "precise" forecast.
8. **A review without "one pot"** — a diversity of perspectives is mandatory; a feast from the same team is subject to the same distortions:

| Reviewer | What they check | Time | Limitation |
|---|---|---|---|
| A business peer | logic, the "feel" of the numbers | 30 min | the same biases |
| Finance / FP&A | formulas, discounting | 1–2 h | weak product context |
| A data analyst | data quality, benchmarks vs fact | 1–2 days | no business context |
| An external auditor | major assumptions, the market | 3–5 days | expensive, optional |

9. **Cognitive bias control:** confirmation bias ("the arguments lean on us", rather than us on them), anchoring (falling in love with the first option / an authority's opinion), the reluctance to break a "neat picture". Antidotes: a challenger (drills one driver to the bottom), searching for 3 arguments AGAINST the model, sensitivity analysis, an external reviewer.
10. **Documentation:** a validation report — the happy checker, the problems found and their resolutions, who reviewed it, buy-in from all participants. Only after that does the model become the plan.

## Template / checklist
A `Checks` tab, binary (0 ok / 1 error), a global status `=IF(SUM(checks)>0;"ERROR";"OK")` — formulas in [[M-traction-model]]:
```
Period balance:        =IF(ABS(End−(Start+In−Out))<0.01;0;1)
Non-negativity:        =IF(MIN(range)<0;1;0)
Retention ≤ 100%:      =IF(MAX(range)>1;1;0)
Funnel never grows:    =IF(SUMPRODUCT(--(step_next>step_prev))>0;1;0)
Not above the market:  =IF(SUM(model)>SOM_cap;1;0)
Demand/supply converges:=IF(ABS(path1−path2)>0.01;1;0)
Broken references:     =IF(SUMPRODUCT(--ISERROR(range))>0;1;0)
```
A model readiness checklist: a tabbed structure and clear navigation · the build logic described · assumptions separated from formulas · every assumption has a source (or an honest "none") · sensitivity and scenarios · a threshold · the review signed off · results documented · buy-in.

A scenario table: `Parameter (retention, CAC, conversion, ARPU) | Bear (−20%) | Base | Bull (+20%) → Revenue, Profit by year | Threshold: Profit < 0 → a red flag`.

## Typical mistakes
| Mistake | How to notice |
|---|---|
| Validation "by eye" without a Checks tab | the reviewer hunts mechanics instead of logic |
| A beautiful model without an external review | the author's "blind eye" does not see retention 120% |
| A benchmark from an irrelevant industry/stage | an apparel conversion of 2–3% for food delivery with its 15–25% |
| The divergence of the two calculation paths ignored | revenue from demand ≠ revenue from supply — always look for the cause |
| Fitting assumptions to the desired outcome | "the economics don't add up — let's raise the conversion" instead of an honest conclusion |
| Judging by a single month of backtest | an unstable forecast accepted as "normal" |
| One reviewer (or all from one team) | shared cognitive biases go unseen |
| Early months taken as the base | the first 1–2 months are early adopters, not representative; wait for 2–3 months of data |

When there is no data at all (a new business/market): proxy metrics (`target = proxy_1 × proxy_2 × an adjustment`, an expected error of 30–60%), expert estimates, a cheap MVP test, an analogy from an adjacent market — and scenario planning instead of a "precise" forecast.

## Questions that can change the decision
- Which single assumption, if wrong by 30%, kills the model — and how fast will we learn this from reality?
- Where is the project's threshold, and what do we do when it is breached?
- Which assumptions do we know worst (they get sensitivity analysis first)?
- Can the riskiest assumption be tested cheaply and fast (an MVP, the first marketing campaign yields a real CAC within 1–2 weeks)?
- What appeared in the model "for beauty" and will not survive the question "where is this number from?"

## Related cards
[[M-traction-model]], [[M-model-topdown-bottomup]], [[M-benchmarking]], [[M-source-criticism]], [[M-unit-economics]], [[M-cannibalization]], [[M-trends-scenarios]], [[M-risks]]
