---
id: M-six-pager-etalon
lang: en
title: Six-pager benchmark — structure walkthrough, good vs bad for every FAQ, typical mistakes
course: strategy
sources: ["EN mirror of the RU methodology card M-six-pager-etalon (knowledge/methods/six-pager-etalon.md); original sources are listed in the RU card"]
stages: [options, strategy, review]
tags: [six-pager, committee, structure, benchmark, faq, tables, inference, evidence]
related: [M-six-pager, M-committee-doc-style, M-source-criticism, M-decision-daci, M-success-metrics, M-strategy-growth]
---

# Six-pager benchmark: how the committee document is built

## When to apply
When a six-pager is assembled or reviewed: before writing a section — to know the benchmark structure
"as it should be"; after writing — as a checklist against typical deviations. The card is a summary of the
benchmark structure of `knowledge/templates/SIX_PAGER_PROMPT.md` with a good/bad walkthrough; the benchmark
itself is the canonical prompt and its text is not duplicated here.

## Core: the document skeleton
Six FAQ sections, each answering a question from the committee reader; inside — numbered sub-items 1.1, 2.1…,
mandatory tables, and a "Conclusion (inference)" line at the end of every substantive block.

| FAQ | The reader's question | Mandatory elements per the benchmark |
|---|---|---|
| FAQ-1 Current state analysis | What is happening in the market, who are the competitors, what is the challenge? | 1.1 market overview: dynamics as ranges, a bullet forecast by year, 5–7 trends, each with "what this means for the product"; 1.2 competitor table: advantages / growth mechanics / risks (High–Low); "what nobody offers" = the strategy window |
| FAQ-2 User Persona | Who is the target audience and what are the barriers? | 2.1 segment table with fixed rows ("Who are they?", "What do they use today?", "What difficulties do they face?"), segmentation by entry barrier, not by profession; 2.2 barriers by journey stage (acquisition → choice → payment → post-payment experience) + "what holds them back from starting" |
| FAQ-3 Strategic initiatives | What do we propose and why exactly this? | an introduction: which options it was chosen from (a reference to red team); 3–4 driver-initiatives with the construction "First/Second driver — …", "Key directions", and an effect calculation (formula → substitution → result) |
| FAQ-4 Tactics | What exactly does each initiative consist of? | matrix "Initiative | Focus | User needs and expectations | Solutions (tactics)": 2–4 rows per initiative; tactics are executable, not slogans |
| FAQ-5 Implementation plan | How do we implement it and in what order? | each initiative's contribution to the result in % (summing to 100%) with justification of the weights; tactic priorities (high → baseline); timing to market seasons; parallel tracks; a D### decision with a stop trigger |
| FAQ-6 Success metrics | What do we measure success by? | KPIs in two planes: business (revenue/MRR, paying users, conversion, LTV/CAC) and product (activation, time-to-value, churn, CSAT/NPS); each KPI: baseline → target by deadline → action threshold; counter-metrics per red-team hits |

## Good vs bad for every FAQ

| FAQ | Good | Bad |
|---|---|---|
| FAQ-1 | a trend leads to a consequence-opportunity: "the ATS gate has become the standard → for us that is an entry barrier, which means…"; competitors in a table with a risk rating; the strategy window is named | a three-page market history; trends without "what this means for us"; competitors as a list without risks and without a conclusion |
| FAQ-2 | segments by entry barrier ("does not know this is possible" vs "knows but fears the payment"); for each barrier — what removes it in the product | portraits like "a 35-year-old housewife"; segments by profession/age; barriers unconnected to product mechanics |
| FAQ-3 | a driver with a calculation: "conversion 2.0→2.6% × traffic × ARPU = +X [C016]"; an explicit reference "option B was rejected because…" | "we will improve retention" without a formula; initiatives without alternatives and objections; an effect "in the air" |
| FAQ-4 | a tactic: "the Start tier at 199 ₽: a landing page with a savings calculator, card and instant-payment (SBP) checkout" | a slogan tactic: "brand development", "UX improvement"; a matrix without needs |
| FAQ-5 | contribution: "the tier ladder at 45%, because it closes two barriers from 2.2 and delivers X ₽ [C020]"; timing to the season | contributions "roughly equal"; a plan without dates and without a D### decision; the 100% does not add up |
| FAQ-6 | "payment conversion: baseline 1.8% → target 2.4% by 01 June → action threshold 2.0%" | "we will grow revenue and loyalty"; KPIs without a baseline and a deadline; no counter-metrics |

## Typical mistakes
- Pasting instead of writing: the text of `02_situation.md` is inserted into FAQ-1 without transitioning to the
  benchmark sub-items 1.1/1.2 — the document does not answer the committee's questions in their order.
- Numbers without provenance: "a 120 billion market" without [S###]/a range — the reader cannot verify it.
- The conclusion is not separated: data, justification, and conclusion are mixed — the committee argues with a
  paragraph instead of the line "therefore…".
- Screenshots and pictures instead of tables — forbidden by the benchmark: the committee's evidentiary form is
  tables and formulas.
- Initiative contributions do not sum to 100%, or weights without justification.
- Metrics without an action threshold: it is not recorded at which value we change the plan.
- The RU and EN versions diverge: the translation is done "by the meaning of the section", the numbers do not
  match — the EN version loses trust.

## Procedure (agent)
1. Before writing: read the benchmark `knowledge/templates/SIX_PAGER_PROMPT.md` and this card; the list of
   mandatory elements for each FAQ comes from the "Core" table.
2. Take the data from 02/03/04/06 and the claim registry (every number → C###/S###), but write the sections anew
   along the benchmark skeleton rather than pasting documents.
3. Close every substantive block with a "Conclusion (inference)" line using the words "therefore / this means".
4. After assembly: walk through the benchmark's "Self-check checklist" and the good/bad table above for every FAQ.
5. `pfs check --strict` — 0 errors; the RU and EN versions are in sync (a full translation, identical numbers).

## Questions that could change the decision
- Which FAQ is the weakest in the current draft — where will the committee ask a question that has no
  "therefore" line?
- Which table is missing (competitors, segments, tactics matrix) and what would it change in the argument?
- Which number without a provenance tag is the most vulnerable, and what is the cheapest way to back it up?

## Related cards
[[M-six-pager]], [[M-committee-doc-style]], [[M-strategy-growth]], [[M-source-criticism]], [[M-decision-daci]]
