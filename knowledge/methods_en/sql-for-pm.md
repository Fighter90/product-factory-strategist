---
id: M-sql-for-pm
lang: en
title: SQL for product analytics — standard queries (funnel, cohorts, ARPU), joins and window functions, data quality
course: data
sources: ["EN mirror of the RU methodology card M-sql-for-pm (knowledge/methods/sql-for-pm.md); original sources are listed in the RU card"]
stages: [research, validation, after-decision]
tags: [sql, funnel, retention, cohorts, arpu, arppu, frequency, join, cte, window-functions, lag, row-number, data-quality]
related: [M-product-metrics, M-ab-testing, M-quant-methods, M-dashboards-visualization, M-traction-model]
---

# SQL for product analytics

## When to apply
You need to verify a hypothesis on data yourself: where the funnel leaks, how cohorts behave, what ARPU/ARPPU and frequency are, why a metric dropped. A quick query of your own instead of filing a ticket to an analyst — plus a data quality check before any calculation.

## Essence

### Basic principles
- Every product metric is an aggregate: `COUNT`, `SUM`, `AVG` + `GROUP BY`; every hypothesis is a filter (`WHERE` before aggregation, `HAVING` — a filter on the aggregate after `GROUP BY`).
- Everything that is not aggregated must be in `GROUP BY`; `COUNT(DISTINCT …)` — for users/orders (deduplication); `NULL` in `GROUP BY` forms a separate group and is ignored inside aggregates (`SUM` over NULL rows does not fail, division by zero — treat with `NULLIF`).
- Aggregation on top of aggregation (subquery/CTE): first orders per user, then the average per region — this is how complex metrics like "retention by cohort and region" are built.
- Safety: work with a read-only replica/data marts, don't run heavy queries against the production database, limit the sample (`LIMIT` during exploration), never publish credentials.

### Typical product queries

**DAU/WAU/MAU (activity):**
```sql
SELECT DATE(submitted_at_dttm) AS day,
       COUNT(DISTINCT customer_id) AS dau
FROM orders_delivery
GROUP BY day ORDER BY day;         -- WAU: DATE_TRUNC('week', …), MAU: 'month'
```

**Funnel (unique users at each step):**
```sql
SELECT
  COUNT(DISTINCT CASE WHEN event_type = 'registration' THEN user_id END) AS step1,
  COUNT(DISTINCT CASE WHEN event_type = 'add_to_cart'  THEN user_id END) AS step2,
  COUNT(DISTINCT CASE WHEN event_type = 'checkout'     THEN user_id END) AS step3,
  COUNT(DISTINCT CASE WHEN event_type = 'payment'      THEN user_id END) AS step4
FROM events
WHERE event_time >= '2025-10-01';
-- step CR = step(n)/step(n−1); end-to-end = step4/step1; the gap between steps = the "drop"
```
For an honest funnel, add a sequence window: a step counts only if the user reached it after the previous one (see window functions below).

**Cohort retention (first action → returns):**
```sql
WITH first_orders AS (
  SELECT customer_id, MIN(DATE(submitted_at_dttm)) AS first_day
  FROM orders_delivery GROUP BY customer_id
),
activity AS (
  SELECT DISTINCT customer_id, DATE(submitted_at_dttm) AS activity_day
  FROM orders_delivery
)
SELECT f.first_day, a.activity_day,
       COUNT(DISTINCT a.customer_id) AS active_users,
       ROUND(100.0 * COUNT(DISTINCT a.customer_id)
             / COUNT(DISTINCT f.customer_id), 2) AS retention_rate
FROM first_orders f
JOIN activity a ON f.customer_id = a.customer_id
GROUP BY f.first_day, a.activity_day
ORDER BY f.first_day, a.activity_day;
-- the result = a cohort matrix; for D7 filter a.activity_day = f.first_day + INTERVAL '7 days'
```
The zero point (the first event) must be defined unambiguously — shifting the zero point inflates retention.

**Revenue, average order value, ARPU/ARPPU:**
```sql
-- revenue and average order value by day
SELECT DATE(o.submitted_at_dttm) AS day,
       SUM(i.price * i.quantity) AS revenue,
       SUM(i.price * i.quantity) / COUNT(DISTINCT o.order_id) AS avg_check
FROM order_items i
JOIN orders_delivery o USING (order_id)
GROUP BY day ORDER BY day;

-- ARPU and ARPPU for a period (a users/activity table is required)
-- ARPU  = SUM(period revenue) / COUNT(DISTINCT active users of the period)
-- ARPPU = SUM(period revenue) / COUNT(DISTINCT paying users of the period)
```
Checks: numerator and denominator — the same period and the same cohort; ARPU over actives, ARPPU over payers — do not swap them; an order can contain many items → deduplicate the order when dividing.

**Repeat orders and frequency:**
```sql
-- share of customers with >1 order (repeat rate)
SELECT ROUND(100.0 * COUNT(DISTINCT CASE WHEN orders_count > 1 THEN customer_id END)
             / COUNT(DISTINCT customer_id), 2) AS repeat_rate
FROM (SELECT customer_id, COUNT(order_id) AS orders_count
      FROM orders_delivery GROUP BY customer_id) t;

-- frequency: orders per customer per day of their "life"
SELECT customer_id, COUNT(order_id) AS order_count,
       ROUND(COUNT(order_id)::NUMERIC /
             (DATE_PART('day', MAX(submitted_at_dttm) - MIN(submitted_at_dttm)) + 1), 2)
       AS orders_per_day
FROM orders_delivery GROUP BY customer_id;
```
Frequency + Recency + Monetary (sum) = the basis of RFM segmentation (`CASE WHEN` over thresholds → New/Active/Loyal segments).

**Diagnosing a metric drop:** cuts by region/category/platform for two periods and a comparison (`WHERE DATE BETWEEN … GROUP BY region`), then narrowing down to the segment where the drop is concentrated; cross-check against last year for seasonality.

### JOIN and UNION
- **INNER JOIN** — only matches (both sides); **LEFT JOIN** — all rows of the left side + matches of the right (NULL where there is none): the standard "orders + deliveries", "users + actions" pattern; **RIGHT JOIN** — the mirror image; **FULL JOIN** — everything from both sides (finding discrepancies between systems).
- After a LEFT JOIN the right table can duplicate rows of the left (a 1:N relationship, e.g. order → items): compute aggregates over the left table before or after — duplication distorts sums.
- **UNION ALL** — simply glues results (fast, duplicates remain); **UNION** — glues and deduplicates (more expensive). A typical use — gluing periods/sources of identical structure.
- A join condition with a range (`BETWEEN first_day AND first_day + INTERVAL '7 days'`) — the basis of retention calculations.

### CTE (WITH … AS) and subqueries
A CTE is a named subquery inside a single SELECT: it makes large queries readable, allows reusing the result (e.g. `first_orders`), simplifies step-by-step debugging, and replaces temporary tables. Limitations: it lives only inside one query, must be declared before use, and by itself does not speed up execution (the optimizer may compute it multiple times — for heavy cases, materialize it into a table).

### Window functions
They compute an aggregate over a group of rows **without collapsing them** (unlike `GROUP BY`) and attach the value to each row:
```sql
<function>() OVER (PARTITION BY key   -- independent groups (user/region)
                   ORDER BY column)   -- order inside the group
```
- `ROW_NUMBER()` — a unique row number within the window: numbering a customer's orders, deduplication (`WHERE rn = 1`), "first/last event".
- `RANK()` / `DENSE_RANK()` — ranking with equal values: RANK skips numbers (1,2,2,4), DENSE_RANK does not (1,2,2,3). Tops by revenue/categories.
- `LAG(col, 1)` / `LEAD(col, 1)` — the previous/next value in the window: intervals between orders, delta versus the previous period, checking the sequence of funnel steps.
```sql
-- days between a customer's orders (frequency and return patterns)
SELECT customer_id, submitted_at_dttm,
       submitted_at_dttm - LAG(submitted_at_dttm) OVER (
         PARTITION BY customer_id ORDER BY submitted_at_dttm) AS days_between
FROM orders_delivery;
```
- A window without `PARTITION BY` — over the whole table (an overall rating). `ORDER BY` inside a window is almost always required. Typical tasks: ranking, event sequences, comparing adjacent values, cumulative metrics, cohort analysis.

### Data quality checklist before calculation
1. **Completeness:** DWH sources have been recalculated; no "holes" across dates; data freshness (up to what date events exist at all).
2. **Duplicates:** no doubled rows for a day (a classic: a sharp "spike and rollback" on a chart is almost always a duplicate in the data, not user behavior); `COUNT(*)` vs `COUNT(DISTINCT id)`.
3. **Definitions:** the cohort's zero point, the funnel window, what counts as "activity" and "payment" — fixed and matching the metric passport; events were not renamed.
4. **Segments and filters:** test users/internal accounts excluded; platform/region filters applied deliberately.
5. **Types and NULL:** dates are dates (not strings); division protected with `NULLIF(...,0)`; the share of returns via `CASE WHEN flag THEN 1 ELSE 0 END`.
6. **Joins:** after a JOIN the row count has not "exploded" (1:N); the LEFT JOIN has not lost control users.
7. **Sanity-check:** the metric of at least one day recalculated by hand; totals matched against a dashboard/a known fact.

## Procedure
1. Formulate the question in terms of a metric, a period and a segment (the metric passport from [[M-product-metrics]]).
2. Check data quality against the checklist above.
3. Start with exploration: table structure, `LIMIT`, row counts; then step-by-step CTEs (first event → activity → aggregate).
4. Compute the basic aggregates (DAU/revenue/funnel), then make them more complex: cohorts, ratio metrics, window functions.
5. Make cuts (segment/period/platform) and period comparisons; check seasonality against last year.
6. Recalculate a control point manually and only then draw a conclusion or hand off the result (to a dashboard, [[M-ab-testing]], [[M-traction-model]]).

## Template / checklist (query card)
```
Question/metric: ___  Period: ___  Granularity: day/week/cohort
Tables and keys: ___ (join type: INNER/LEFT, 1:N risk: ___)
Zero point/window: ___  Filters (test users, platforms): ___
Deduplication: COUNT(DISTINCT ___)   Division guard: NULLIF ___
Cross-check against fact: ___ (source/value)
```

## Typical mistakes
- `WHERE` and `HAVING` swapped; columns outside aggregates forgotten in `GROUP BY`.
- A 1:N JOIN doubles revenue/users; a LEFT JOIN silently turns into INNER because of a filter on the right table in `WHERE`.
- UNION instead of UNION ALL where duplicates are needed (or vice versa — hidden duplicates).
- NULL gets lost: `SUM` ignores NULL, but `COUNT(col) ≠ COUNT(*)`; division by zero without `NULLIF`.
- A shifted cohort zero point or a floating funnel window — retention "improves" because of redefinition, not because of the product.
- End-to-end conversion compared with step conversion; ARPU computed over everyone and ARPPU over actives.
- A heavy query on the production database; no `LIMIT` during exploration; "a sharp spike and rollback" taken for user behavior without checking duplicates.

## Questions that can change the decision
- Are all events logged from the needed date, and were events ever renamed?
- What is the relationship between the tables (1:1/1:N), and does the join double the numerator or the denominator?
- What is the zero point and the window here — and do they match the metric passport?
- Is the "drop" concentrated entirely within one segment/platform/region?
- Is the result reproducible: does a manual recount match the dashboard and the previous period?

## Related cards
[[M-product-metrics]], [[M-ab-testing]], [[M-quant-methods]], [[M-dashboards-visualization]], [[M-traction-model]]
