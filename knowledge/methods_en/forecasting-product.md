---
id: M-forecasting-product
lang: en
title: Forecasting and traction analytics — baseline, seasonality, a driver model, accuracy and the limits of a forecast
course: data
sources: ["EN mirror of the RU methodology card M-forecasting-product (knowledge/methods/forecasting-product.md); original sources are listed in the RU card"]
stages: [options, strategy, validation, after-decision]
tags: [forecast, baseline, seasonality, time-series, drivers, uplift, trend, mape, forecast-validation, scenarios]
related: [M-traction-model, M-model-validation, M-product-metrics, M-ab-testing, M-dashboards-visualization]
---

# Forecasting and traction analytics for a product

## When to apply
You need to decide "is it worth investing in the idea", set goals for a period, plan budget/workload, or honestly answer "what happens to the metric if we do nothing" — that is the baseline, without which the effect of an initiative cannot be counted. A forecast is not a promise but a scenario with assumptions; it is always verifiable and always comes with an interval.

## Essence

### Forecast vs driver model
- **Extrapolation (time series)** — "extend the history": trend + seasonality + noise. Works when there is a deep stable history (12–24 months) and the market is not being disrupted. This is the base for the baseline.
- **Driver model (traction)** — "assemble the metric from parts": e.g. Revenue = PU × TPU × AOV, each part a driver with its assumption and source. Works when history is short / the rules of the game change or you need the effect of a specific initiative.
- The right practice is a hybrid: a baseline from the time series, with initiative drivers on top. Pure "as is" extrapolation over horizons with product/market changes is a typical mistake.

### Components of a time series
1. **Trend** — the long-term direction (the category grows 15% year over year).
2. **Seasonality** — a repeating pattern with a known period: daily (day/night), weekly (weekdays/weekends), monthly (payday peaks), yearly (December upswing, January dip). Recognizable seasonality is not a product problem.
3. **Noise** — random fluctuations; it is exactly because of noise that a week of "+3" against an average of 20 can be a fluke.
4. **Anomalies** — one-off spikes: promotions, outages, campaigns, A/B tests, external events. Before modeling they are excluded or replaced; otherwise the model "learns" the anomaly as a pattern.

### Baseline: the "if we do nothing" forecast
**The baseline is a forecast of how the metrics will behave without the initiative launch.** It is the foundation of traction: a bad baseline = wrong uplift = wrong decision. The baseline is NOT a forecast with a feature, NOT a product manager's opinion and NOT last year's analytics; it is a clean forecast built on historical data.
Why: without a baseline you cannot tell a feature's effect from seasonality ("every February PU drops by 20%, and with the feature it dropped by 15% — that is a success, not a failure"), you cannot compute uplift or compare "growth/decline against the norm".
Step-by-step construction:
1. Collect 12–24 months of history, day/week granularity, cuts by segments.
2. Remove anomalies: promotions, large A/B tests, one-off campaigns, outliers.
3. Apply a time-series model: in ascending complexity — moving average / naive seasonal forecast (value = last period's value × seasonal coefficient), then Prophet/ARIMA/ETS, then gradient boosting with features — when there are many external factors. The model is built **for each segment separately**.
4. Force-impose last year's seasonality where the model under-captures it: `baseline[t] = trend + last year's seasonality + adjustments for other products`.
5. Check that the baseline "does not fall apart": visually, by backtesting against recent months' facts, by residual analysis (errors without systematic bias), by prediction intervals. If it "jumps" — redo it.
6. Always segment: new/existing users, categories, platforms, plan types — initiatives affect segments differently, and an aggregate baseline is silent about it.

### Traction (driver model) at the entry to an investment decision
The process of "gates" (a gate model): Gate 0 — idea (days), Gate 1 — "traction on a napkin" (an estimate of the logic: drivers, orders of magnitude; accuracy not required), Gate 2 — a detailed model (analyst + product manager, days-weeks), Gate 3 — verification by the facts of an A/B test after the pilot.
Composition of the detailed model:
1. **Target metric** (Revenue/PU/ARPPU/GMV/retention — per feature).
2. **Baseline** (see above).
3. **Segmentation** (mandatory: the same initiative can raise PU in one segment and crush ARPPU in another).
4. **Drivers** of metric changes: decompose the target into multipliers (Revenue = PU × TPU × AOV; ARPPU = TPU × AOV) and forecast each driver with justification.
5. **Uplift** — the initiative's effect by driver; sources: past launches, other teams' A/B tests, market benchmarks, UX research, expert judgment; each assumption carries a **confidence level (e.g. 50–100%)** and a status (proven/hypothesis).
6. **Rollout** — a schedule of audience shares by month (10% → 30% → 60% → 100%): the effect stretches over time, "January's profit is not June's profit"; a schedule shift moves the whole forecast.
7. **Final forecast** = baseline + uplift × % rollout, month by month, with cannibalization and overlaps with other launches ([[M-traction-model]]).
Do not forget: logic checks (bottom-up does not punch through the top-down market ceiling), sensitivity on the 2–3 main assumptions, base/optimistic/pessimistic scenarios.

### Checking forecast accuracy
- **Backtest:** train on history up to moment T, predict after T, compare with the fact. Errors: MAE — mean absolute error (in metric units); **MAPE** — mean absolute percentage error, `mean(|fact − forecast| / fact) × 100%`, applicable to positive metrics; RMSE — quadratic, penalizes large misses. A benchmark for business forecasts is MAPE < 20% (stronger — <10%); the main thing is that the error be below the "economically meaningful" effect the forecast is supposed to catch.
- Residuals (fact − forecast) must have no trend/seasonality — otherwise the model missed something.
- Always show the forecast with an interval (pessimistic/optimistic), not as a point.
- After launch: fact vs baseline vs forecast — regular reconciliation ([[M-model-validation]]).

### When a forecast "cannot lie" and when it makes no sense
- **A baseline built on history cannot "lie" as an opinion:** it is a checkable statement ("what would have happened without us") — it can be reconciled with facts and improved; in this sense it is objective by construction (pure historical data, no wishes).
- **Not a forecast but planning:** for a new product without history extrapolation is impossible — the "forecast" becomes scenarios with assumptions (top-down from the market, bottom-up from unit economics, three scenarios instead of a baseline). Passing them off as a forecast is a mistake.
- **A forecast is useless/harmful** if: the horizon is beyond the stability of the assumptions (the rules of the game change); the main assumption is singular and unverified; accuracy is not measured; intervals are not shown. A long horizon = a wide interval — show the narrowing of confidence toward the horizon honestly.
- **A forecast without an owner, assumptions and fact-vs-plan reconciliation dates is not a tool but a picture:** assumptions are put in a prominent place, a specific person is responsible for each, reconciliation is scheduled with dates.

### Typical forecasting mistakes
1. Linear "as is" extrapolation — missing seasonality and saturation.
2. Ignoring seasonality: the January dip is taken as "the feature killed the product" (or conversely, the December peak as the feature's success).
3. Poor data cleaning: anomalies/duplicates/outages entered the model.
4. Future-data leakage: information "from the future" relative to the forecast moment got into the features.
5. One scenario instead of three; intervals not shown; a point passed off as a fact.
6. Blind trust in the model: no business logic or sanity-check (a model can "predict" the physically impossible).
7. An unsegmented baseline — uplift is averaged and wrong for every segment.
8. Rollout not accounted: the effect of 100% of the audience is attributed to the first month.

### Baseline models in ascending complexity
| Situation | Model | When it is enough |
|---|---|---|
| Stable seasonality, short history | naive seasonal forecast: value = last period × seasonal coefficient | a first estimate, Gate 1 |
| Trend + seasonality, one metric | Prophet/ETS/ARIMA (decomposition of the series) | the basic working baseline |
| Many external factors, many segments | gradient boosting with features (calendar, promotions, weather) | large metrics, features available |
| New product without history | not a forecast but scenarios: top-down from the market + bottom-up from unit economics | three scenarios instead of a baseline |
The scheme of building an ML forecast (briefly): data cleaning → check/set seasonality → a baseline model → adding features → the model → interpretation and sanity-check. Add complexity only if the simpler option fails the backtest.

## Procedure
1. Define the question and the forecast horizon; is there history (≥12 months) and are the rules of the game stable — this determines the choice of approach ([[M-traction-model]]).
2. Collect and clean the history (anomalies, duplicates, outages), choose granularity and segments.
3. Build the baseline: naive seasonal forecast → a time-series model → impose last year's seasonality; verify with a backtest and residuals; compute MAPE/MAE.
4. Decompose the target metric into drivers; for each driver specify uplift, source and confidence level.
5. Overlay uplift on the baseline with a rollout schedule; account for cannibalization and overlaps; check against the market ceiling.
6. Assemble base/optimistic/pessimistic scenarios and sensitivity on the 2–3 main assumptions.
7. Present the forecast with intervals and assumptions; agree on control: fact vs baseline vs forecast reconciliation dates and the condition for revision.

## Template / checklist
```
Question: ___  Horizon: ___  Metric: ___ (units, period)
History: ___ months, segments: ___  Anomalies excluded: yes/no
Baseline: method ___  Backtest MAPE = ___%  Residuals without trend: yes/no
Drivers: PU=___ TPU=___ AOV=___  Uplift: ___ (source, confidence ___%)
Rollout: month 1 ___% … month N ___%   Cannibalization: ___
Scenarios: base ___ / optim ___ / pess ___   Fact control: ___ (reconciliation dates)
```
Checklist: there is a baseline, not only "the feature's effect" · last year's seasonality is accounted · accuracy is measured (MAPE) and below the meaningful effect · every uplift has a source and confidence · rollout is month by month · scenarios and intervals are shown · fact vs baseline reconciliation dates are assigned.

## Typical mistakes
- "Extending the line" instead of a baseline with seasonality; recording the December peak as the initiative's success.
- Anomalies and promotions are not cleaned out — the model learned them.
- A point forecast without an interval; scenarios replaced by a "most likely" number.
- Uplift out of thin air: no source, no confidence level, no cannibalization.
- One aggregate baseline instead of a segmented one; rollout not reflected.
- No backtest; MAPE not computed; fact vs forecast never reconciled by anyone.
- For a new product, extrapolation "by analogy" passed off as a forecast.

## Questions that can change the decision
- Is there enough history, and are the rules of the game stable across the whole horizon?
- What happens to the metric without our initiative (the baseline) and how accurate is that baseline (MAPE)?
- Which driver contributes >50% of the result, and where is its uplift taken from?
- Does the bottom-up forecast punch through the market ceiling, and does it overlap with other teams' launches?
- What will the fact show in 3 months if the forecast is off by the size of the interval, and who reconciles it and when?

## Related maps
[[M-traction-model]], [[M-model-validation]], [[M-product-metrics]], [[M-ab-testing]], [[M-dashboards-visualization]]
