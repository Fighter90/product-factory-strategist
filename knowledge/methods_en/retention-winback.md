---
id: M-retention-winback
lang: en
title: Paid subscription retention and win-back — dunning, save flows, cancellation reasons, winning customers back
course: strategy
sources: ["EN mirror of the RU methodology card M-retention-winback (knowledge/methods/retention-winback.md); original sources are listed in the RU card"]
stages: [validation, after-decision, monitoring]
tags: [retention, subscriptions, churn, dunning, save-offer, win-back, gross-retention, resurrection]
related: [M-retention-curves, M-product-metrics, M-loyalty-metrics, M-unit-economics, M-cannibalization, M-ab-testing]
---

# Paid subscription retention and win-back

## When to apply
When the product lives on paid subscriptions: payers are leaving, payments are failing, cancellations are
growing; when designing cancellation save flows and win-back campaigns. The card closes the gap between
product retention ([[M-retention-curves]]) and money: a subscription is lost not only when the customer
"leaves" but also when the payment fails.

## Core
**Payer churn ≠ product churn.** Cancellation splits into voluntary (the customer decided) and involuntary
(a failed payment: an expired card, insufficient funds, a bank block). In subscription products the
involuntary part reaches a noticeable share of total churn, and it is treated with mechanics, not with
product work:

1. **Dunning** — payment recovery: scheduled retry charges (for example, on day 3, 5, and 7), card-update
   reminders, bank account updater, pausing instead of instantly cutting off access.
2. **Save flow at cancellation** — a cascade before the cancellation is confirmed: pause the subscription,
   downgrade to a cheaper tier, an offer (discount/plan change), move the billing date. Each step addresses
   its own cancellation reason.
3. **Cancellation reasons** — categorize with a survey at cancellation: price, value (not using it), the need
   has passed, an accidental subscription, technical problems. Each category calls for different
   countermeasures: price → the tier ladder ([[M-pricing-ladder]]), value → activation and habit formation,
   accident → make cancellation easier at purchase.

**Win-back is a separate product, not a mailing.** Win-back works when something **has changed**: new
content/a feature, a pain from the cancellation reason that is now solved, a change in the customer's life
situation. The scheme: to whom (churned users with high past value and a "natural" return cycle), when
(30/60/90 days after cancellation — tuned from data), with what (a product change or a targeted offer),
channel (email/push). Without "what changed", win-back trains customers to wait for a discount — that is
learnable cannibalization ([[M-cannibalization]]): buyers meet the next offer expecting an even bigger
discount.

**Metrics.** Gross retention (how many payers were kept) versus net retention (with upgrades/downgrades);
resurrection rate (the share of churned users who returned in the period); LTV with the win-back effect;
involuntary churn as a separate line. Retaining existing users is cheaper than acquiring new ones: check that
the win-back budget is not taken away from channels with better CAC without a calculation.

## Procedure (agent)
1. Decompose churn: voluntary / involuntary, by tier and cohort — as a fact from payment data.
2. Cancellation reasons: run a cancellation survey, categorize, compute shares — countermeasure hypotheses for
   every major category.
3. Design dunning and save flows: a map of cancellation steps with copy; what is offered to whom.
4. Win-back: segment, the "what changed" trigger, channel, offer, success metric and counter-metric (the share
   of "discount-driven" re-cancellations).
5. Validation: A/B each mechanic ([[M-ab-testing]]) — save flow vs a straightforward cancellation, the dunning
   schedule, win-back with an offer vs without; the evaluation horizon ≥ 2 billing cycles.
6. In the model ([[M-traction-model]]): retention as an LTV driver; the sensitivity of ARPU and churn to
   save/win-back.

## Template / checklist
- [ ] churn split into voluntary/involuntary, by tier;
- [ ] cancellation reasons are collected and categorized, shares computed;
- [ ] every major reason has a countermeasure and its metric;
- [ ] dunning: a retry schedule, a card-update reminder, paused access;
- [ ] save flow: a "pause → downgrade → offer" cascade, without dark patterns of hiding the cancellation;
- [ ] win-back launches only with "what changed" and with a counter-metric for discount dependency;
- [ ] gross and net retention are computed separately; involuntary churn is visible as a separate line.

## Typical mistakes
- "The customer cancelled = the customer left": involuntary churn is fixed with payment mechanics, not
  features.
- A save offer for everyone: a discount for those who would have stayed anyway is a direct margin loss.
- Win-back "we miss you" without change: training the base to wait for discounts.
- Cancellation in two clicks, coming back in five: it retains short-term and destroys trust and NPS
  long-term.
- Average churn across the base: first-year payers and veterans leave differently; compute by cohort.

## Questions that could change the decision
- What share of churn is actually involuntary (a fast win without product work)?
- Will the save offer cost more margin than it saves in subscriptions?
- Do churned users have a "natural" return cycle (seasonality, events) to lean on?

## Related cards
[[M-retention-curves]] — curves and cohorts; [[M-product-metrics]] — the retention metrics tree;
[[M-loyalty-metrics]] — NPS/CSAT as early signals; [[M-pricing-ladder]] — downgrade instead of cancellation;
[[M-ab-testing]] — validating the mechanics; [[M-cannibalization]] — discount cannibalization.
