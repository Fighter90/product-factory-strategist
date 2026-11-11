---
id: M-paid-retention
lang: en
title: Paid subscription retention and win-back — renewals, dunning, save offers, winning back churned users
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [validation, after-decision, monitoring]
tags: [retention, subscriptions, churn, win-back, dunning, renewals, cohorts]
related: [M-loyalty-metrics, M-unit-economics, M-product-metrics, M-cannibalization, M-ab-testing, M-retention-curves]
---

# Paid subscription retention and win-back

## When to apply
When paying subscribers churn out: they don't renew the subscription, turn off auto-renewal, or leave after a
promotional period. The goal is to manage the "three leaks" of the paying base: voluntary churn, involuntary churn
(payments), and the dormant churned users who can be won back. The retention scenario appears in the Megafon demo
task — the map describes the general methodology without any closed data.

## Core idea
Retaining payers is work with a cohort's survival curve by churn reason, where each reason has its own tool:

| Churn reason | What it looks like | Tool |
|---|---|---|
| No value received | cancellation in the first 1–2 periods | onboarding up to the "first result", triggered emails/pushes based on usage |
| Didn't understand the charge | "why was I charged?" | a transparent notification before the charge, a clear statement |
| Involuntary churn | the card expired, insufficient funds | dunning: charge retries, notifications, alternative payment methods |
| Price vs value | "too expensive for how I use it" | a downgrade path to a cheaper tier instead of cancellation ([[M-cannibalization]] — count the effect) |
| Seasonality | it was needed for a month | a subscription pause instead of cancellation |
| Life event | changed jobs/city | a win-back segment with a delayed offer |

Rules for working with the metrics:
- compute on subscription cohorts (the month of the first payment), not the "average churn across the base";
- separate **logo churn** (cancellations) and **revenue churn** (money): a downgrade and a pause reduce revenue
  but keep the payer;
- gross retention (retention of the base) and net revenue retention (with upgrades counted in) are different
  metrics; NRR growing while GR falls is "squeezing" the base;
- cohort payback ([[M-unit-economics]]): retaining payers is the main payback lever, sometimes cheaper than
  acquisition.

Win-back: churned users are segmented by the reason for leaving and by recency; the offer is built from the reason
("update your card" ≠ "here's a discount"); cannibalization — part of the win-back audience would have returned
even without an offer, so the effect is counted only against a control group.

## Procedure
1. Break down the churn of the last 3 months by reason (a survey at cancellation + payment data + interviews with
   churned users).
2. Estimate each reason's contribution to churn (the share of cancellations and the share of revenue) —
   prioritize by revenue, not by the number of cancellations.
3. For involuntary churn: audit the dunning sequence (charge retries, intervals, notification texts, payment
   methods).
4. For voluntary churn: an intervention card for each reason (mechanics, expected effect on churn, cannibalization
   risk).
5. Win-back: define the segments (reason × recency), the offer and a control group; count the increment, not
   "returns".
6. Validate the interventions with an A/B test ([[M-ab-testing]]): the metric is cohort survival and NRR, the
   horizon is at least 1–2 billing cycles.
7. Institutionalize: a churn-by-reason dashboard, cohort curves, alerts on renewal anomalies
   ([[M-loyalty-metrics]]).

## Template / checklist
| Reason | Share of cancellations | Share of revenue | Tool | Expected effect | Check |
|---|---|---|---|---|---|
| no value | | | | | A/B |
| didn't understand the charge | | | | | A/B |
| payments (dunning) | | | | | A/B |
| price | | | downgrade/pause | | A/B |
| other | | | | | |

- [ ] churn is counted by cohorts and in money, not only by the number of cancellations;
- [ ] the dunning sequence is described and tested;
- [ ] every tier has a downgrade path and a pause;
- [ ] win-back is measured against a control group (increment);
- [ ] the validation horizon is ≥ 1–2 billing cycles.

## Typical mistakes
- A discount for everyone who leaves as "retention": cannibalizing the loyal base and teaching users to cancel in
  order to get a discount.
- Churn "across the base" instead of by cohorts: the effect of interventions is invisible.
- Logo churn only: downgrades and pauses look like "success" while revenue falls.
- Dunning as a single charge retry "at the end of the month": most involuntary churn is unrecoverable after that.
- Win-back without a control group: "returns" include those who would have come back on their own.
- An offer based on recency instead of the reason for leaving: a discount for "too expensive" doesn't help
  "didn't understand the value".

## Questions that can change the decision
- Which churn reason drives the main revenue loss (not the number of cancellations)?
- How much money does +1 p.p. of retention bring over a year — and is work on it comparable to acquisition?
- What share of the win-back audience would have returned without an offer?
- Doesn't a pause/downgrade dilute the paying base so much that NRR falls even as logo churn drops?

## Related maps
[[M-loyalty-metrics]], [[M-unit-economics]], [[M-product-metrics]], [[M-cannibalization]], [[M-ab-testing]], [[M-retention-curves]]
