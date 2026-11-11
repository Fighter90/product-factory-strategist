---
id: M-dashboards-visualization
lang: en
title: Visualization and dashboards for product managers — purpose, a 4-level structure, chart rules and a checklist
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [research, after-decision]
tags: [visualization, dashboards, hero-kpi, funnel-chart, annotations, palette, checklist, monitoring]
related: [M-product-metrics, M-sql-for-pm, M-ab-testing, M-traction-model, M-quant-methods]
---

# Visualization and dashboards for product managers

## When to apply
You need to speed up decisions and the search for hypotheses about metrics, assemble a dashboard from which the team understands within a minute "are we OK or not", or check an existing dashboard/chart for typical mistakes. Visualization is not decoration but a way to think faster: a table of a thousand rows hides an anomaly, a chart shows it in seconds.

## Core idea

### Why a product manager needs visualization
1. **Faster decisions:** trends, spikes, seasonality, failures and incidents are visible as patterns, not as numbers.
2. **Hypotheses:** a collapse at the onboarding step, seasonal growth, a conversion drop after a release — a source of product hypotheses; a funnel on a chart "screams" about the problem.
3. **A common language:** developers, designers, marketing and top management read the same charts; "release" and "incident" annotations remove unnecessary calls.
4. **Monitoring and prioritization:** the dashboard highlights KPI deviations and signals when "something went wrong".
The flip side: **wrong visualization = wrong decision** — a cropped axis hides a failure, an extra series makes the chart unreadable.

### Visualization ≠ dashboard
- **Visualization (chart)** — a single object: a line, bars, a funnel. It answers one question.
- **A dashboard** — a composition of charts assembled for a decision, with context, hierarchy and filters. The dashboard's question: "what is happening with the product and why".

### When visualization doesn't help
The chart answers the wrong question; too many series/colors; no labels or units; a decorative style instead of data; a scale chosen so that the changes are invisible; chaotic data that is better summarized in a small table. Then don't "touch up" — change the chart itself or the question.

### Reference dashboard structure: 4 levels
| Level | Question | Content |
|---|---|---|
| 1. Intro | "Where am I, what is this data?" | Name, period, active filters (platform, geo, segment), a description "what the dashboard is for", the date of the last data refresh |
| 2. Hero KPI | "Are we OK?" | 3–6 main metrics as large cards: value + arrow + comparison with the previous period (WoW/MoM/YoY) |
| 3. Diagnostics | "Why is that?" | Dynamics of the key metrics with release/incident annotations; breakdowns by segment (bar); a funnel; distributions/heatmap; cohorts where needed |
| 4. Detail | "Where to dig?" | Tables by campaign/category/segment, lists of anomalies, data export |
The reading logic is top-down: "are we OK?" → "why?" → "where to dig?". The levels must not be mixed: a KPI card at the bottom of the page and a table at the top break the movement of the gaze and of decisions. Quality rule: **the state of the product is clear from the top block in 5 seconds, the whole dashboard in 60 seconds**. The Intro is insurance against wrong decisions: without it people read the wrong period/platform and argue about numbers.

### "One panel = one thought"
Each panel answers exactly one question and sits at its own level: Hero KPI — large values; diagnostics — a line chart of dynamics, breakdowns, a funnel; detail — tables. A chaotic grid of "everything at once" without hierarchy is the main sign of a bad dashboard.

### Choosing a chart type per question
| Question | Type | Notes |
|---|---|---|
| How does a metric change over time? | line chart | with release/incident annotations, without cropping the axis |
| What is bigger/smaller across categories? | bar chart | mandatory sorting by value, axis from zero |
| Where does the user path "fail"? | funnel | steps in the user's language, the window of the path is stated |
| How are values distributed / where are the anomalies? | histogram, heatmap | instead of "the average across the hospital" |
| How do cohorts behave? | cohort heatmap | arrival period × lifetime |
| What is a whole made of? | stack/shares — only 3–5 parts | avoid a pie with >5 shares and close values |
| Plan vs fact dynamics? | two lines/bars + the difference | the comparison base is stated ([[M-forecasting-product]]) |

### How to read someone else's dashboard in 60 seconds
1. Intro: which period, which filters, how fresh the data is (otherwise there is nothing to look at further).
2. Hero KPI: which metrics are "red" and by how much they deviated from the previous period.
3. Diagnostics: for the deviated metric — the dynamics with annotations and a breakdown; what changed earlier than the metric (a leading signal).
4. Detail: who exactly / which segment / which category; formulate one next verification step.
If steps 2–3 do not give an answer to "what is happening" — the dashboard was assembled incorrectly, not "there is too little data".

### Chart rules inside a dashboard
1. **One question per chart**; the chart type per question: dynamics — a line; comparing categories — a sorted bar; a part of a whole — only if ≤ 4–5 shares (a pie is better avoided in general); a funnel — a funnel chart; density/distribution — a heatmap/histogram.
2. **Minimalism:** clean axes, no 3D, shadows or decor; a lot of data — information density, but no visual noise.
3. **A single palette and styling** across the whole dashboard: at most 4–5 colors; gray for secondary series; red only for bad values, green only for good ones; a color accent only where the message is.
4. **Honest axes:** a bar chart is always from zero; a line chart — without cropping that hides the amplitude (or with an explicit note); the same scale for comparable panels.
5. **Labels:** axis names, units of measurement (₽, %, items), period, granularity (day/week), a legend where there is more than one series.
6. **Annotations are mandatory:** releases, incidents, marketing campaigns right on the dynamics line — otherwise the team looks for the "cause" in the product when it was a competitor's release or an outage.
7. **Filters and parameters:** platform/segment/period are switched at the Intro level and apply to the whole dashboard.
8. **The link to the level:** on Hero — values and arrows; on Diagnostics — breakdowns and funnels; on Detail — tables with export.

### Typical dashboard mistakes (anti-patterns)
1. No Intro — the reader doesn't know the period/filters/freshness of the data.
2. No Hero KPI — the state of the product is not readable; all charts are "equal".
3. Too many charts and fine details of the same scale; no sorting in the bar chart (the most important must be on top).
4. Unrelated charts — a panel leads nowhere and depends on nothing.
5. Too many colors and different styles (fonts, line thickness, palettes) — visual noise.
6. A pie chart for comparing many shares; a cropped Y-axis on the bars.
7. No release/incident annotations — the cause of a metric's movement is searched for in the wrong place.
8. Overloaded tables without sorting or highlighted deviations.
9. No filters — a new dashboard is built for every question.
10. The dashboard "explains" but does not help act: no breakdowns, detail or export.
11. The period/units are not stated — numbers are interpreted arbitrarily.

## Procedure (dashboard assembly)
1. Define the **one main question** of the dashboard and its consumer (who looks at it and how often, which decision they make).
2. Pick the metrics by the pyramid: 3–6 "product health" (Hero), drivers for diagnostics, detail tables ([[M-product-metrics]] — a passport for each metric: formula, units, period).
3. Design top-down: Intro → Hero → Diagnostics → Detail; check that each level answers its own question.
4. Select the charts: one question per panel, the right type, a single palette, honest axes, labels and units.
5. Add annotations of releases/promotions/incidents and a filter system.
6. Check with the "60-second" test: an outside person names the state of the product and one suspicious spot.
7. Agree on the data updates (frequency, the date of the last refresh) and the owner of the dashboard.

## Template / checklist
```
Name: ___  Consumer and decision: ___  Updates: ___
Intro: period ___ filters ___ description ___ data-freshness date ___
Hero KPI (3–6): ___ each with Δ vs the previous period
Diagnostics: dynamics with annotations ___ breakdowns ___ funnel ___ distributions ___
Detail: tables ___ anomalies ___ export ___
```
Checklist: the Intro is filled in · the Hero answers "are we OK?" in 5 seconds · one question per panel · ≤4–5 colors, a single style · the axes are honest (bars from zero) · labels and units everywhere · releases/incidents are annotated · bar charts are sorted · there are filters and detail · the state is clear in 60 seconds.

## Typical mistakes
- A dashboard as a "pretty picture": no decision it was assembled for, and no consumer.
- No hierarchy: 20 charts in a single grid, the KPI at the bottom, the dashboard's question unclear.
- A cropped Y-axis on bars turns ±1% into "drama" (and vice versa — hides a drop).
- A neutral series highlighted in bright red, a bad one in green: color stops carrying meaning.
- A metric on a chart without a period/units; two charts with different scales compared "by eye".
- No annotations — the team ties a drop to a feature when it was an incident or a campaign.
- The dashboard is not updated (the freshness date is not visible), and decisions are made on stale data.

## Questions that can change the decision
- Which decision should this dashboard speed up, and who is its consumer?
- Is "are we OK or not" readable in 5 seconds from the top block without explanations?
- Is every movement of a key metric annotated (release/campaign/incident), or will the cause be searched for blindly?
- Do the axes, sorting and palette distort the perception of the size of changes?
- Is the data fresh at the moment of the decision, and is the date of the last refresh visible?

## Related maps
[[M-product-metrics]], [[M-sql-for-pm]], [[M-ab-testing]], [[M-traction-model]], [[M-quant-methods]]
