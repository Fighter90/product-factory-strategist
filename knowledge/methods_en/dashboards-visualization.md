---
id: M-dashboards-visualization
lang: en
title: Visualization and dashboards for a PM — purpose, a 4-level structure, chart rules, and a checklist
course: data
sources: ["EN mirror of the RU methodology card M-dashboards-visualization (knowledge/methods/dashboards-visualization.md); original sources are listed in the RU card"]
stages: [research, after-decision]
tags: [visualization, dashboard, hero-kpi, funnel-on-chart, annotations, palette, checklist, monitoring]
related: [M-product-metrics, M-sql-for-pm, M-ab-testing, M-traction-model, M-quant-methods]
---

# Visualization and dashboards for a PM

## When to use
You need to speed up decisions and the search for hypotheses on metrics, assemble a dashboard from which the team understands within a minute "are we OK or not," or check an existing dashboard/chart for typical mistakes. Visualization is not decoration but a way to think faster: a table of a thousand rows hides an anomaly, a chart shows it in seconds.

## Core idea

### Why a PM needs visualization
1. **Faster decisions:** trends, spikes, seasonality, drops, and incidents are visible as patterns, not as numbers.
2. **Hypotheses:** a collapse at the onboarding step, seasonal growth, a conversion drop after a release — sources of product hypotheses; a funnel on a chart "screams" about the problem.
3. **A shared language:** engineers, designers, marketing, and top management read the same charts; annotations "release," "incident" remove unnecessary calls.
4. **Monitoring and prioritization:** the dashboard highlights KPI deviations and signals when "something went wrong."
The flip side: **wrong visualization = wrong decision** — a truncated axis hides a drop, an extra series makes the chart unreadable.

### Visualization ≠ dashboard
- **Visualization (chart)** — one object: a line, bars, a funnel. Answers one question.
- **A dashboard** — a composition of charts assembled for decision-making, with context, hierarchy, and filters. The dashboard question: "what is happening with the product and why."

### When visualization does not help
The chart answers the wrong question; too many series/colors; no labels or units; a decorative style instead of data; a scale chosen so that changes are invisible; the data is chaotic and is better summarized in a small table. Then the answer is not "re-styling" but changing the chart itself or the question.

### The reference dashboard structure: 4 levels
| Level | Question | Content |
|---|---|---|
| 1. Intro | "Where am I, what data is this?" | Title, period, active filters (platform, geo, segment), a description "what the dashboard is for," the date of the last data refresh |
| 2. Hero KPI | "Are we OK?" | 3–6 key metrics as large cards: value + arrow + comparison with the previous period (WoW/MoM/YoY) |
| 3. Diagnostics | "Why is it so?" | Dynamics of the key metrics with release/incident annotations; cuts by segment (bar); a funnel; distributions/heatmap; cohorts when needed |
| 4. Detail | "Where to dig?" | Tables by campaign/category/segment, anomaly lists, data export |
Reading logic top-down: "are we OK?" → "why?" → "where to dig?". The levels must not be mixed: a KPI card at the bottom of the page and a table on top break the movement of the eye and of decisions. The quality rule: **the state of the product is readable from the top block in 5 seconds, the whole dashboard in 60 seconds**. The Intro is insurance against wrong decisions: without it, people read the wrong period/platform and argue about numbers.

### "One panel = one thought"
Each panel answers exactly one question and sits at its own level: Hero KPI — large values; diagnostics — a line chart of dynamics, cuts, a funnel; detail — tables. A chaotic "everything at once" grid without hierarchy is the main sign of a bad dashboard.

### Choosing the chart type for the question
| Question | Type | Notes |
|---|---|---|
| How does a metric change over time? | line chart | with release/incident annotations, no axis truncation |
| What is bigger/smaller across categories? | bar chart | mandatory sorting by value, axis from zero |
| Where does the user's path "break"? | funnel | steps in the user's language, the path window specified |
| How are values distributed / where are the anomalies? | histogram, heatmap | instead of "the average across everyone" |
| How do cohorts behave? | cohort heatmap | acquisition period × lifetime |
| What makes up a whole? | stack/shares — only 3–5 parts | avoid pie above 5 shares and with close values |
| Plan vs actual dynamics? | two lines/bars + the difference | the comparison baseline is stated ([[M-forecasting-product]]) |

### How to read someone else's dashboard in 60 seconds
1. Intro: which period, which filters, how fresh the data is (otherwise do not look further).
2. Hero KPI: which metrics are "red" and by how much they deviated from the previous period.
3. Diagnostics: for the deviating metric — dynamics with annotations and a cut; what changed before the metric did (a leading signal).
4. Detail: who specifically/which segment/which category; formulate one next verification step.
If steps 2–3 do not answer "what is happening" — the dashboard was assembled incorrectly, not "there is too little data."

### Chart rules inside a dashboard
1. **One question per chart**; the chart type follows the question: dynamics — line; category comparison — sorted bar; part of a whole — only if ≤ 4–5 shares (pie is best avoided in general); funnel — funnel; density/distribution — heatmap/histogram.
2. **Minimalism:** clean axes, no 3D, shadows, or decor; much data means information density, but without visual noise.
3. **A unified palette and style** across the whole dashboard: at most 4–5 colors; gray for secondary series; red only for bad values, green only for good ones; color as an accent only where the message is.
4. **Honest axes:** a bar chart always from zero; a line chart without truncation that hides the amplitude (or with an explicit note); the same scale for comparable panels.
5. **Labels:** axis names, units of measure (RUB, %, count), period, granularity (day/week), a legend wherever there is more than one series.
6. **Annotations are mandatory:** releases, incidents, marketing campaigns right on the dynamics line — otherwise the team hunts for the "cause" in the product when it was a competitor's release or an outage.
7. **Filters and parameters:** platform/segment/period are switched at the Intro level and apply to the whole dashboard.
8. **Match with the level:** on Hero — values and arrows; on Diagnostics — cuts and funnels; on Detail — tables with export.

### Typical dashboard mistakes (anti-patterns)
1. No Intro — the reader does not know the period/filters/data freshness.
2. No Hero KPI — the state of the product is not readable; all charts are "equal."
3. Too many charts and fine details at one scale; no sorting in the bar chart (the most important should be on top).
4. Unrelated charts — a panel leads nowhere and depends on nothing.
5. Too many colors and different styles (fonts, line weights, palettes) — visual noise.
6. A pie chart for comparing many shares; a truncated Y axis on bars.
7. No release/incident annotations — the cause of the metric's movement is sought in the wrong place.
8. Overloaded tables without sorting or highlighted deviations.
9. No filters — a new dashboard is built for every question.
10. The dashboard "explains" but does not help decide: no cuts, detail, or export.
11. No period/units specified — numbers are interpreted arbitrarily.

## Procedure (assembling a dashboard)
1. Define the dashboard's **one main question** and its consumer (who looks at it and how often, what decision they make).
2. Choose the metrics by the pyramid: 3–6 "product health" metrics (Hero), drivers for diagnostics, detailed tables ([[M-product-metrics]] — a passport for each metric: formula, units, period).
3. Design top-down: Intro → Hero → Diagnostics → Detail; check that each level answers its own question.
4. Select the charts: one question per panel, the right type, a unified palette, honest axes, labels and units.
5. Add annotations for releases/campaigns/incidents and a filter system.
6. Run the "60 seconds" test: an outside person names the state of the product and one suspicious spot.
7. Agree on the data refresh (frequency, last-updated date) and the dashboard owner.

## Template / checklist
```
Title: ___  Consumer and decision: ___  Refresh: ___
Intro: period ___ filters ___ description ___ data-freshness date ___
Hero KPI (3–6): ___ each with Δ vs the previous period
Diagnostics: dynamics with annotations ___ cuts ___ funnel ___ distributions ___
Detail: tables ___ anomalies ___ export ___
```
Checklist: the Intro is filled in · Hero answers "are we OK?" in 5 seconds · one question per panel · ≤4–5 colors, a unified style · honest axes (bar from zero) · labels and units everywhere · releases/incidents annotated · bar charts sorted · filters and detail present · the state is readable in 60 seconds.

## Typical mistakes
- A dashboard as "a pretty picture": no decision it was assembled for, and no consumer.
- No hierarchy: 20 charts in a single grid, KPI at the bottom, the dashboard's question unclear.
- A truncated Y axis on bars turns ±1% into "drama" (and vice versa — hides a drop).
- A neutral row highlighted in bright red, a bad one in green: color stops carrying meaning.
- A metric on a chart without period/units; two charts with different scales compared "by eye."
- No annotations — the team ties the drop to a feature when it was an incident or a campaign.
- The dashboard is not refreshed (the freshness date is not visible), and decisions are made on stale data.

## Questions that can change the decision
- Which decision should this dashboard speed up, and who is its consumer?
- Is "are we OK or not" readable in 5 seconds from the top block, without explanations?
- Is every movement of a key metric annotated (release/campaign/incident), or will the cause be hunted blindly?
- Do the axes, sorting, and palette distort the perception of the size of the changes?
- Is the data fresh at the moment of the decision, and is the last-updated date visible?

## Related cards
[[M-product-metrics]], [[M-sql-for-pm]], [[M-ab-testing]], [[M-traction-model]], [[M-quant-methods]]
