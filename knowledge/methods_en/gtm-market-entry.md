---
id: M-gtm-market-entry
lang: en
title: Entering a new market (GTM by country) — localization, taxes and payments, data regulation
course: strategy
sources: ["EN mirror of the RU methodology card M-gtm-market-entry (knowledge/methods/gtm-market-entry.md); original sources are listed in the RU card"]
stages: [situation, strategy, validation]
tags: [gtm, market, countries, localization, vat, payments, mor, regulation, checklist]
related: [M-gtm-launch, M-market-sizing, M-external-environment, M-competitors, M-unit-economics, M-risks]
---

# Entering a new market (GTM by country)

## When to apply
When the product enters a new country or region: market selection, entry preparation, a country pilot.
The card is a **checklist of questions**, not legal conclusions: on taxes and regulation it names what to
check and with whom (MoR, a tax advisor, a data lawyer) but does not decide for them.

## Core: five entry loops
Entering a country is five parallel loops; the failure of any one nullifies the others.

| Loop | Key questions | Where to verify |
|---|---|---|
| Demand and size | TAM/SAM for the country, willingness to pay, local competitors and alternatives, "why now" | [[M-market-sizing]], [[M-competitors]], open statistics |
| Localization | The language of product, onboarding, support, and marketing; local use cases and currencies; cultural expectations (date, address, and payment formats) | dogfooding with locals, interviews with diaspora/expats |
| Payments and taxes | Local payment methods (iDEAL, PIX, Bancontact…), who is the merchant of record (you yourselves or a MoR), VAT/GST: rates, registration thresholds, prices with or without tax, invoicing | payment providers, MoR services, a tax advisor |
| Data regulation | Personal data law (GDPR and local analogs), consents and cookies, data localization, cross-border transfer | a data lawyer, the regulator's official guides |
| Operations and channel | Support across time zones and languages, pricing in the local currency, the country's GTM channels (SEO, marketplaces, partners), channel cost | [[M-gtm-launch]], pilot campaigns |

**Price and tax are part of the product.** In the EU the price shown to an individual consumer includes VAT;
a "price without tax" reads as deception. VAT registration thresholds and one-stop-shop schemes (OSS/IOSS)
change the economics of low order values: compute revenue net of tax before setting prices, not after the
first invoices.

**MoR vs own registration.** A merchant of record (a provider who acts as the seller and carries the tax
reporting) speeds up entry and removes the tax routine for a fee; registering yourself preserves margin and
control but requires accounting in every jurisdiction. For a country pilot a MoR is usually faster; at scale
the decision is recalculated.

**A country pilot, not a "country launch".** Entry is validated as a hypothesis: a narrow segment, one
channel, one language, entry metrics (CR, CAC, churn, ARPU — local, not global averages) and the
"expand / change the entry / exit" criteria written before the start.

## Procedure (agent)
1. Pick 2–3 candidate countries: size ([[M-market-sizing]]), competition, ease of payments and data —
   weighted scoring ([[M-weighted-scoring]]).
2. For the chosen country, fill in the five-loop checklist: every answer with a source (fact) or as a
   hypothesis with a validation plan.
3. Taxes and payments: draft the questions for the MoR/tax advisor; build two scenarios into the model
   (MoR / own registration) with their fees.
4. Localization: scope (product + support + marketing), who translates and reviews, local use cases.
5. Pilot: segment, channel, budget, duration, metrics, and decision criteria — in the format of the
   validation plan 06 (see [[M-ab-test-design-template]], [[M-success-metrics]]).
6. Country risks (regulatory changes, payment blocks, exchange rate) — into the [[M-risks]] register.

## Template / checklist
- [ ] The country's TAM/SAM computed separately, not as "a share of the global market";
- [ ] local competitors and "how it is solved today" analyzed;
- [ ] language: product, support, marketing — what is translated in the pilot, what is not (and why);
- [ ] payment methods cover ≥80% of the target segment's preferences;
- [ ] the tax scheme is clear: who is the seller of record, the VAT rate, price with or without tax;
- [ ] data: which consents, where it is stored, whether it can be transferred abroad — questions for the
      lawyer drafted;
- [ ] pilot metrics are local (the country's CR/CAC/churn/ARPU), decision criteria written before the start.

## Typical mistakes
- Copying the US price: without VAT, purchasing power, and local alternatives.
- "We will translate later": an English-only product on a non-English-speaking market converts two to three
  times worse.
- Taxes after the start: penalties and retrospective registrations eat the pilot's margin.
- One market "for all of Europe": countries differ in payments, languages, and laws — "Europe" is not a market.
- Legal conclusions from this card: the checklist names the questions; a consultant makes the decisions.

## Questions that could change the decision
- Is the niche already taken by a local player who is cheaper and "one of their own"?
- Does the country's CAC pay back at local conversion and VAT-inclusive prices?
- In which country will data regulation not require local infrastructure (entry cost ×2)?

## Related cards
[[M-gtm-launch]] — launch and channels; [[M-market-sizing]] — the size of the country's market;
[[M-external-environment]] — PESTEL and the macro environment; [[M-unit-economics]] — the unit economics of
the country; [[M-risks]] — the entry risk register.
