---
id: M-sql-for-pm
lang: en
title: SQL for product analytics — typical queries (funnel, cohorts, ARPU), joins and window functions, data quality
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [research, validation, after-decision]
tags: [sql, funnel, retention, cohorts, arpu, arppu, join, cte, window-functions, data-quality]
related: [M-product-metrics, M-ab-testing, M-quant-methods, M-dashboards-visualization, M-traction-model]
---

# SQL for product analytics

## When to apply
You need to verify a hypothesis on the data yourself: where the funnel leaks, how cohorts behave, what ARPU/ARPPU and frequency are, why a metric fell. A fast query of your own instead of ticketing the analyst — plus a data-quality check before any calculation.

## Core idea

### Basic principles
- Every product metric is an aggregate: `COUNT`, `SUM`, `AVG` + `GROUP BY`; every hypothesis is a filter (`WHERE` before aggregation, `HAVING` — a filter on the aggregate after `GROUP BY`).
- Everything that is not aggregated must appear in `GROUP BY`; `COUNT(DISTINCT …)` is for users/orders (deduplication); `NULL` in `GROUP BY` forms a group of its own and is ignored by aggregates (`SUM` over NULL rows doesn't fail, division by zero is treated with `NULLIF`).
- Aggregation on top of aggregation (subquery/CTE): first orders per user, then the average per region — that is how compound metrics like "retention by cohort and region" are built.
- Safety: work on a read-only replica/data marts, don't run heavy queries against the production database, limit your samples (`LIMIT` during exploration), never publish credentials.

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
-- step CR = step(n)/step(n−1); through conversion = step4/step1; the gap between steps = the "drop"
```
For an honest funnel, a sequence window is added: a step counts only if the user reached it after the previous one (see window functions below).

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
-- the result = a cohort matrix; for D7, filter a.activity_day = f.first_day + INTERVAL '7 days'
```
The zero point (the first event) must be defined unambiguously — a shifted zero point inflates retention.

**Revenue, average check, ARPU/ARPPU:**
```sql
-- revenue and average check by day
SELECT DATE(o.submitted_at_dttm) AS day,
       SUM(i.price * i.quantity) AS revenue,
       SUM(i.price * i.quantity) / COUNT(DISTINCT o.order_id) AS avg_check
FROM order_items i
JOIN orders_delivery o USING (order_id)
GROUP BY day ORDER BY day;

-- ARPU and ARPPU for a period (a users/activity table is required)
-- ARPU  = SUM(revenue of the period) / COUNT(DISTINCT active users of the period)
-- ARPPU = SUM(revenue of the period) / COUNT(DISTINCT paying users of the period)
```
Checks: numerator and denominator must share one period and one cohort; ARPU over active users, ARPPU over paying ones — never swap them; an order can contain many items → deduplicate the order when dividing.

**Repeat orders and frequency:**
```sql
-- share of clients with >1 order (repeat rate)
SELECT ROUND(100.0 * COUNT(DISTINCT CASE WHEN orders_count > 1 THEN customer_id END)
             / COUNT(DISTINCT customer_id), 2) AS repeat_rate
FROM (SELECT customer_id, COUNT(order_id) AS orders_count
      FROM orders_delivery GROUP BY customer_id) t;

-- frequency: orders per client per day of their "life"
SELECT customer_id, COUNT(order_id) AS order_count,
       ROUND(COUNT(order_id)::NUMERIC /
             (DATE_PART('day', MAX(submitted_at_dttm) - MIN(submitted_at_dttm)) + 1), 2)
       AS orders_per_day
FROM orders_delivery GROUP BY customer_id;
```
Frequency + Recency + Monetary (sum) = the basis of RFM segmentation (`CASE WHEN` on thresholds → New/Active/Loyal segments).

**Diagnosing a metric drop:** cuts by region/category/platform for two periods and a comparison (`WHERE DATE BETWEEN … GROUP BY region`), then narrowing down to the segment where the drop is concentrated; a year-over-year check for seasonality.

### JOIN and UNION
- **INNER JOIN** — matches only (both sides); **LEFT JOIN** — all rows of the left table + matches of the right one (NULL where there is none): the standard "orders + deliveries", "users + actions" pattern; **RIGHT JOIN** — the mirror image; **FULL JOIN** — everything from both sides (finding discrepancies between systems).
- After a LEFT JOIN the right table can duplicate rows of the left one (a 1:N relationship, e.g. order → items): count aggregates over the left table before or after consciously — duplication distorts sums.
- **UNION ALL** — simply glues results (fast, duplicates remain); **UNION** — glues and deduplicates (more expensive). Typical use — gluing together periods/sources of identical structure.
- A join condition with a range (`BETWEEN first_day AND first_day + INTERVAL '7 days'`) is the basis of retention calculations.

### CTE (WITH … AS) and subqueries
A CTE is a named subquery inside a single SELECT: it makes large queries readable, allows reusing a result (for example, `first_orders`), simplifies step-by-step debugging, and replaces temporary tables. Limitations: it lives only inside one query, must be declared before use, and does not speed up execution by itself (the optimizer may evaluate it repeatedly — for heavy cases, materialize it into a table).

### Window functions
They compute an aggregate over a group of rows **without collapsing it** (unlike `GROUP BY`) and attach the value to each row:
```sql
<function>() OVER (PARTITION BY key    -- independent groups (user/region)
                   ORDER BY column)    -- the order within the group
```
- `ROW_NUMBER()` — a unique row number within the window: numbering a client's orders, deduplication (`WHERE rn = 1`), "first/last event".
- `RANK()` / `DENSE_RANK()` — ranking with ties: RANK skips numbers (1,2,2,4), DENSE_RANK does not (1,2,2,3). Tops by revenue/categories.
- `LAG(col, 1)` / `LEAD(col, 1)` — the previous/next value within the window: intervals between orders, the delta versus the previous period, checking the sequence of funnel steps.
```sql
-- days between a client's orders (frequency and return patterns)
SELECT customer_id, submitted_at_dttm,
       submitted_at_dttm - LAG(submitted_at_dttm) OVER (
         PARTITION BY customer_id ORDER BY submitted_at_dttm) AS days_between
FROM orders_delivery;
```
- A window without `PARTITION BY` spans the whole table (an overall ranking). `ORDER BY` inside a window is almost always mandatory. Typical tasks: ranking, event sequences, comparing neighboring values, cumulative metrics, cohort analysis.

### Data-quality checklist before calculating
1. **Completeness:** DWH sources have been recalculated; no date "holes"; data freshness known (up to which date events exist at all).
2. **Duplicates:** no doubled rows for a day (a classic: a sharp "growth and rollback" on the chart is almost always a duplicate in the data, not user behavior); `COUNT(*)` vs `COUNT(DISTINCT id)`.
3. **Definitions:** the cohort's zero point, the funnel window, what counts as "activity" and "payment" — fixed and matching the metric passport; events have not been renamed.
4. **Segments and filters:** test users/internal accounts are excluded; platform/region filters applied consciously.
5. **Types and NULL:** dates are dates (not strings); division is protected with `NULLIF(...,0)`; return shares via `CASE WHEN flag THEN 1 ELSE 0 END`.
6. **Relationships:** after a JOIN the row count has not "exploded" (1:N); a LEFT JOIN has not lost the control users.
7. **Sanity-check:** the metric for at least one day has been recomputed by hand; totals reconciled with the dashboard/a known fact.

## Procedure
1. Phrase the question in terms of a metric, a period and a segment (the metric passport from [[M-product-metrics]]).
2. Check data quality against the checklist above.
3. Start with exploration: table structure, `LIMIT`, row counts; then build CTEs step by step (first event → activity → aggregate).
4. Compute the basic aggregates (DAU/revenue/funnel), then complicate: cohorts, ratio metrics, window functions.
5. Make the cuts (segment/period/platform) and compare periods; check seasonality against last year.
6. Recompute a control point by hand and only then draw a conclusion or hand the result over (to a dashboard, [[M-ab-testing]], [[M-traction-model]]).

## Template / checklist (request card)
```
Question/metric: ___  Period: ___  Granularity: day/week/cohort
Tables and keys: ___ (join type: INNER/LEFT, 1:N risk: ___)
Zero point/window: ___  Filters (test users, platforms): ___
Deduplication: COUNT(DISTINCT ___)   Division guard: NULLIF ___
Reconciliation with a known fact: ___ (source/value)
```

## Typical mistakes
- `WHERE` and `HAVING` swapped; columns outside aggregates forgotten in `GROUP BY`.
- A 1:N JOIN doubles revenue/users; a LEFT JOIN silently becomes an INNER because of a right-table filter in `WHERE`.
- UNION instead of UNION ALL where duplicates are needed (or vice versa — hidden duplicates).
- NULL handling slips: `SUM` ignores NULL, but `COUNT(col) ≠ COUNT(*)`; division by zero without `NULLIF`.
- A shifted cohort zero point or a floating funnel window — retention "improves" because of redefinition, not because of the product.
- Through conversion compared with step conversion; ARPU computed over everyone while ARPPU over active users.
- A heavy query on the production database; no `LIMIT` during exploration; a "sharp growth and rollback" taken for user behavior without checking for duplicates.

## Questions that can change the decision
- Are all events logged from the needed date, and have events been renamed along the way?
- What is the relationship between the tables (1:1/1:N), and does the join double the numerator or the denominator?
- What is the zero point and the window here — and do they match the metric passport?
- Is the "drop" concentrated entirely in one segment/platform/region?
- Is the result reproducible: does the recomputation agree with the dashboard and the previous period?

## Related maps
[[M-product-metrics]], [[M-ab-testing]], [[M-quant-methods]], [[M-dashboards-visualization]], [[M-traction-model]]
