---
id: M-forecasting-product
lang: en
title: Forecasting and traction analytics — baseline, seasonality, driver model, forecast accuracy and limits
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [options, strategy, validation, after-decision]
tags: [forecast, baseline, seasonality, time-series, drivers, uplift, trend, mape, forecast-validation, scenarios]
related: [M-traction-model, M-model-validation, M-product-metrics, M-ab-testing, M-dashboards-visualization]
---

# Forecasting and traction analytics for a product

## When to apply
When you need to decide "is the idea worth investing in", set goals for a period, plan budget/load, or honestly answer "what
happens to the metric if we do nothing" — that is the baseline, without which an initiative's effect cannot be computed.
A forecast is not a promise but a scenario with assumptions; it is always checkable and always shown with an interval.

## Core idea

### Forecast vs driver model
- **Extrapolation (time series)** — "extend the history": trend + seasonality + noise. Works when there is a deep stable
  history (12–24 months) and the market rules are not breaking. This is the basis for the baseline.
- **Driver model (traction)** — "assemble the metric from parts": e.g., Revenue = PU × TPU × AOV, where each part is a driver
  with a premise and a source. Works when the history is short / the rules of the game change, or when the effect of a specific
  initiative is needed.
- The right practice is a hybrid: a baseline from the time series, the initiative's drivers on top. Pure "as-is" extrapolation
  across horizons with product/market changes is a typical error.

### Time-series components
1. **Trend** — the long-term direction (the category grows 15% year over year).
2. **Seasonality** — a repeating pattern with a known period: daily (day/night), weekly (weekdays/weekends), monthly (salary
   peaks), annual (a December surge, a January dip). Recognizable seasonality ≠ a product problem.
3. **Noise** — random fluctuation; it is exactly why a "+3" week against an average of 20 can be chance.
4. **Anomalies** — one-off spikes: promotions, outages, campaigns, A/B tests, external events. They are excluded or replaced
   before modeling; otherwise the model "learns" the anomaly as a law.

### Baseline: the "if we do nothing" forecast
**The baseline is the forecast of how the metrics will behave without the initiative's launch.** It is the foundation of
traction: a bad baseline = a wrong uplift = a wrong decision. The baseline is NOT a forecast with the feature, NOT the product
manager's opinion and NOT last year's analytics; it is a pure forecast built on historical data.
Why: without a baseline you cannot separate a feature's effect from seasonality ("PU falls 20% every February, and with the
feature it fell 15% — that is success, not failure"), you cannot compute uplift or compare "growth/decline against the norm".
Step-by-step construction:
1. Collect 12–24 months of history, day/week granularity, cuts by segments.
2. Remove anomalies: promotions, large A/B tests, one-off campaigns, spikes.
3. Apply a time-series model, in order of increasing complexity: a moving average / seasonal naive forecast (value = last
   period's value × seasonal factor), then Prophet/ARIMA/ETS, then gradient boosting with features — when there are many
   external factors. The model is built **for each segment separately**.
4. Force last year's seasonality where the model underestimates it: `baseline[t] = trend + last year's seasonality +
   adjustments for other products`.
5. Check that the baseline "holds together": visually, by comparing against the facts of recent months (backtest), by residual
   analysis (errors without systematic bias), by prediction intervals. If it "jumps" — redo it.
6. Segment always: new/returning users, categories, platforms, tariff types — initiatives affect segments differently, and an
   aggregate baseline says nothing about it.

### Traction (driver model) at the entry to an investment decision
The "gates" process (gate model): Gate 0 — idea (days), Gate 1 — "back-of-envelope traction" (a sanity check of the logic:
drivers, orders of magnitude; accuracy not required), Gate 2 — a detailed model (analyst + product manager, days-weeks),
Gate 3 — verification against the facts of an A/B test after the pilot.
Composition of the detailed model:
1. **Target metric** (Revenue/PU/ARPPU/GMV/retention — for the feature).
2. **Baseline** (see above).
3. **Segmentation** (mandatory: the same initiative can raise PU in one segment and crush ARPPU in another).
4. **Drivers** of metric change: decomposing the target into multipliers (Revenue = PU × TPU × AOV; ARPPU = TPU × AOV) and a
   forecast of each driver with a rationale.
5. **Uplift** — the initiative's effect per driver; sources: past launches, other teams' A/B tests, market benchmarks,
   UX research, expert judgment; every premise carries a **confidence level (e.g., 50–100%)** and a status (proven/hypothesis).
6. **Rollout** — the schedule of audience shares by month (10% → 30% → 60% → 100%): the effect stretches over time,
   "January's profit ≠ June's profit"; shifting the timeline shifts the whole forecast.
7. **Final forecast** = baseline + uplift × rollout %, month by month, with cannibalization and intersections with other
   launches ([[M-traction-model]]).
Don't forget: logical checks (the bottom-up forecast must not break through the top-down market cap), sensitivity on 2–3 main
assumptions, base/optimistic/pessimistic scenarios.

### Checking forecast accuracy
- **Backtest:** train on history up to moment T, predict after T, compare with the facts. Errors: MAE — the mean absolute error
  (in the metric's units); **MAPE** — the mean absolute percentage error, `mean(|fact − forecast| / fact) × 100%`, applicable to
  positive metrics; RMSE — quadratic, penalizes large misses. A benchmark for business forecasts is MAPE < 20% (better — <10%);
  the main thing is an error below the "economically meaningful" effect the forecast is supposed to catch.
- Residuals (fact − forecast) must have no trend/seasonality — otherwise the model missed something.
- Always show a forecast with an interval (pessimistic/optimistic), not as a point.
- After launch: fact vs baseline vs forecast — regular reconciliation ([[M-model-validation]]).

### When a forecast "cannot lie" and when it is meaningless
- **A history-based baseline cannot "lie" as an opinion:** it is a checkable statement ("what would have happened without us") —
  it can be reconciled with the facts and improved; in this sense it is objective by construction (pure historical data, no wishes).
- **Not a forecast but planning:** for a new product without history, extrapolation is impossible — the "forecast" turns into
  scenarios with assumptions (top-down from the market, bottom-up from unit economics, three scenarios instead of a baseline).
  Passing them off as a forecast is an error.
- **A forecast is useless/harmful** if: the horizon goes beyond the assumptions' stability (the rules of the game change); the
  main premise is single and unverified; accuracy is not measured; intervals are not shown. A long horizon = a wide interval —
  show the narrowing of confidence toward the horizon honestly.
- **A forecast without an owner, assumptions and fact-vs-plan check dates is not a tool but a picture:** assumptions are placed
  in a prominent position, a specific person is responsible for each, and the reconciliation is scheduled with dates.

### Typical forecasting mistakes
1. Linear "as-is" extrapolation — skipping seasonality and saturation.
2. Ignoring seasonality: the January dip taken as "the feature killed the product" (or vice versa, the December peak taken as
   the feature's success).
3. Poor data cleaning: anomalies/duplicates/outages entered the model.
4. Future data leakage: information "from the future" relative to the forecast moment got into the features.
5. One scenario instead of three; intervals not shown; a point passed off as a fact.
6. Blind trust in the model: without business logic and sanity checks (a model can "predict" the physically impossible).
7. An unsegmented baseline — the uplift is averaged and wrong for every segment.
8. Rollout not accounted for: a 100%-audience effect attributed to the first month.

### Baseline models in order of increasing complexity
| Situation | Model | When it is enough |
|---|---|---|
| Stable seasonality, short history | seasonal naive forecast: value = last period × seasonal factor | a first estimate, Gate 1 |
| Trend + seasonality, one metric | Prophet/ETS/ARIMA (series decomposition) | the basic working baseline |
| Many external factors, many segments | gradient boosting with features (calendar, promotions, weather) | large metrics, features available |
| A new product without history | not a forecast but scenarios: top-down from the market + bottom-up from unit economics | three scenarios instead of a baseline |
The ML forecast construction scheme (briefly): data cleaning → checking/setting seasonality → a baseline model → adding
features → the model → interpretation and a sanity check. Add complexity only if the simpler option fails the backtest.

## Procedure
1. Define the question and the forecast horizon; is there history (≥12 months) and are the rules of the game stable — this
   determines the choice of approach ([[M-traction-model]]).
2. Collect and clean the history (anomalies, duplicates, outages), choose granularity and segments.
3. Build the baseline: seasonal naive forecast → time-series model → impose last year's seasonality; verify with a backtest and
   residuals; compute MAPE/MAE.
4. Decompose the target metric into drivers; for each driver state the uplift, the source and the confidence level.
5. Overlay the uplift on the baseline with the rollout curve; account for cannibalization and intersections; reconcile against
   the market cap.
6. Assemble base/optimistic/pessimistic scenarios and sensitivity on the 2–3 main assumptions.
7. Present the forecast with intervals and assumptions; agree on control: dates for reconciling fact vs baseline vs forecast
   and a revision trigger.

## Template / checklist
```
Question: ___  Horizon: ___  Metric: ___ (units, period)
History: ___ months, segments: ___  Anomalies removed: yes/no
Baseline: method ___  Backtest MAPE = ___%  Residuals without trend: yes/no
Drivers: PU=___ TPU=___ AOV=___  Uplift: ___ (source, confidence ___%)
Rollout: month 1 ___% … month N ___%   Cannibalization: ___
Scenarios: base ___ / optim ___ / pess ___   Fact control: ___ (reconciliation dates)
```
Checklist: there is a baseline, not only a "feature effect" · last year's seasonality is accounted for · accuracy is measured
(MAPE) and below the meaningful effect · every uplift has a source and a confidence level · the rollout is monthly · scenarios
and intervals are shown · fact-vs-baseline reconciliation dates are assigned.

## Typical mistakes
- "Extending the line" instead of a seasonality-aware baseline; booking December's peak as the initiative's success.
- Anomalies and promotions not cleaned out — the model learned them.
- A point forecast without an interval; scenarios replaced by a "most likely" number.
- Uplift out of thin air: no source, no confidence level, no cannibalization.
- One aggregate baseline instead of segmented; the rollout not reflected.
- No backtest; MAPE not computed; nobody ever reconciles fact with forecast.
- For a new product, extrapolation "by analogy" passed off as a forecast.

## Questions that can change the decision
- Is there enough history, and are the rules of the game stable across the whole horizon?
- What happens to the metric without our initiative (the baseline), and how accurate is that baseline (MAPE)?
- Which driver contributes >50% of the result, and where does its uplift come from?
- Does the bottom-up forecast break through the market cap, and does it intersect with other teams' launches?
- What will the facts show in 3 months if the forecast misses by the interval's width — and who reconciles it, and when?

## Related maps
[[M-traction-model]], [[M-model-validation]], [[M-product-metrics]], [[M-ab-testing]], [[M-dashboards-visualization]]
