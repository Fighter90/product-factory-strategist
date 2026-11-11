---
id: M-six-pager-etalon
lang: en
title: Six-pager etalon — structure walkthrough with "good and bad" for every FAQ
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [review, options]
tags: [six-pager, committee, document-structure, report, quality]
related: [M-six-pager, M-committee-style, M-market-sizing, M-unit-economics, M-outcome-roadmap, M-success-metrics]
---

# Six-pager etalon: structure and "good and bad"

## When to apply
Before assembling or reviewing a six-pager: you need a reference point for "what a correct document for the committee looks like" — section by section, not "on average". The card is a summary of the etalon's structure and the typical mistakes of each FAQ; the full reference case is never copied — the text is always written anew for the specific decision (PRO-46, PRO-60).

## Core idea
The etalon is a fixed structure made of a header, six FAQ sections, and an attachments row, where every section answers one question of the decision maker and has its own "etalon level" of quality.

| Section | Etalon level ("good") | Anti-etalon ("bad") |
|---|---|---|
| Header | the request verbatim, the decision, the recipient, the date and the process step | a header with a "topic" instead of a decision ("product update") |
| FAQ-1 Situation analysis | 3–5 market facts with [C###]/[S###], a competitor table "player → advantage → risk for us", and a conclusion "what this changes for the decision" | a page-long market history, competitors "in general", conclusions without numbers |
| FAQ-2 Users | 2–4 segments with pains by journey stage and "what holds them back", a target focus with a conversion number | personas like "all users 18–65", pains without a journey stage |
| FAQ-3 Initiatives | ≥3 substantively different options, including "keep as is" and "shut down", strong objections, contribution to the result (summing to 100%) | one "favorite" initiative, objections like "not enough resources", a contribution of "roughly half" |
| FAQ-4 Tactics | a Focus → Needs & desires → Solutions table, every tactic tied to a need and an expected effect | a list of features without needs, "we will build an app" |
| FAQ-5 Plan and validation | owners and teams per initiative, seasonality, a validation card: comparison base, deadline, countermetrics, criteria | a plan of "we start in January", validation of "we'll watch the metrics" |
| FAQ-6 Metrics | business and product metrics with formulas, units, period, target value and an A/B plan | "we will grow retention and loyalty" without formulas and targets |
| Attachments | Excel with an "Input" sheet: parameters are editable, calculations run on formulas | "dead" numbers in cells, an assumption you cannot touch |

Substantive rules of the etalon: numbers only with [C###]/[S###] tags and reconciled against Excel; every initiative has objections and a measurable contribution; an objection is strong (it can kill the initiative), not a formality; a section does not retell its neighbor; length ≈6 substantive pages, one screen — one idea.

## Procedure
1. Open the template `knowledge/templates/six_pager.md` and the prompt `SIX_PAGER_PROMPT.md` — the structure and the rules are already there.
2. For each FAQ, check the draft against the "good" column of the table above: does the section answer its own question?
3. Go through the "bad" column as a checklist of antipatterns: if you find one — rewrite the section, don't "polish it up".
4. Reconcile the numbers in the text with the Excel attachments and the claims registry (every value → C###).
5. Read the document through the eyes of a committee member: could they raise an objection on every section — and is there an answer in the text?

## Template / checklist
- [ ] header: the request verbatim, the decision, the recipient, the date;
- [ ] FAQ-1: facts with [C###]/[S###] + a competitor table + a conclusion for the decision;
- [ ] FAQ-2: segments with pains by journey stage + a target focus with a number;
- [ ] FAQ-3: ≥3 options, including "keep as is" and "shut down", objections, contribution = 100%;
- [ ] FAQ-4: tactics through Focus → Needs & desires → Solutions;
- [ ] FAQ-5: owners, seasonality, a validation card (base, deadline, countermetrics, criteria);
- [ ] FAQ-6: metrics with formulas, units, period, targets;
- [ ] attachments: an "Input" sheet, calculations on formulas, numbers match the text.

## Typical mistakes
- "Assembling" the document by pasting in pieces of 02/03/04/06: the text does not answer the committee's questions, it retells the process steps (PRO-46).
- FAQ-1 as a "market history": looks nice, but it does not change the decision.
- Objections for show: "there may not be enough resources" neither kills the initiative nor requires an answer.
- Initiative contributions "summing to 130%": shares are not normalized, prioritization is impossible.
- Metrics without a comparison base and a deadline — they cannot be checked.
- Excel without formulas: assumptions are not editable, trust in the numbers falls.

## Questions that can change the decision
- Which FAQ section is our weakest right now, and what would strengthen it most cheaply?
- Which committee objection could we not defuse with today's text?
- Which number in the document is the most fragile, and where is its confirmation in the attachments?

## Related maps
[[M-six-pager]], [[M-committee-style]], [[M-market-sizing]], [[M-unit-economics]], [[M-outcome-roadmap]], [[M-success-metrics]]
