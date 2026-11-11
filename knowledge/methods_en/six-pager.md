---
id: M-six-pager
lang: en
title: Six-pager — a six-page strategic report with Excel appendices
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [options, strategy, validation, review]
tags: [six-pager, report, committee, excel-appendices, strategy-review, decision-support]
related: [M-market-sizing, M-traction-model, M-unit-economics, M-outcome-roadmap, M-success-metrics]
---

# Six-pager

## When to apply
When a recommendation is defended before a committee/leadership: you need a compact (~6 meaningful pages) document in a fixed structure, where each section answers a known question and the numbers are computed in Excel appendices, not "in thin air". In the agent it is assembled by `pfs export --six-pager`.

## Core idea
Six FAQ sections, each an answer to the decision-maker's question. The six-pager is **written to the reference** (`knowledge/templates/six_pager.md`, prompt `SIX_PAGER_PROMPT.md`), not stitched together by pasting in from documents 02/03/04/06: those documents are the sources of facts and numbers, and the text of each section is written anew for the reader's question (PRO-46).

| Section | Reader's question | What it is filled with (sources of facts) |
|---|---|---|
| FAQ-1 | What's happening in the market, who are the competitors, what is the challenge? | facts and contradictions from `02_situation.md`, the competitor table "advantage → risk for us" |
| FAQ-2 | Who are the users and what are their pains along the journey? | segments/personas from the situation and research |
| FAQ-3 | Which initiatives do we propose and why exactly these? | options and objections from `03_options.md`, the recommendation |
| FAQ-4 | What does each initiative concretely consist of? | tactics: Focus → Needs & desires → Solutions |
| FAQ-5 | How will it be implemented and how will we know it worked? | the validation plan from `06_validation_plan.md`, the initiatives' contributions |
| FAQ-6 | By which metrics do we measure success? | business and product metrics with formulas (04, the metrics map) |

Structure rules: the initiatives' contributions to the result sum up to 100%; every initiative has strong objections; "keep as is" and "shut the direction down" are present as full-fledged alternatives; a competitor table of "advantage → risk for us"; tactics tied to needs, not to features.

## Procedure (agent)
1. Check that the sources are ready: `02_situation.md`, `03_options.md`, `04_product_strategy.md`, `06_validation_plan.md`. Something is missing — finish that step first; a six-pager is not written without sources of facts.
2. Assemble the parameters from the claims registry into `projects/<slug>/calcs.json` (every value → a C###).
3. With a background subagent: `pfs calc all` → `outputs/attachments/*.xlsx` (unit economics, growth model, cohorts, market size; an "Inputs" sheet with editable parameters, calculations as live formulas).
4. `pfs export --six-pager` → `outputs/SIX_PAGER.md`: the sections are written to the reference (`knowledge/templates/SIX_PAGER_PROMPT.md`), each FAQ answers its own question rather than retelling a document.
5. `pfs check` with no new errors; show the owner the list of appendices and what can be edited in them.

## Template / checklist
See `knowledge/templates/six_pager.md`. Quality checklist:
- [ ] each section answers "its own" question, not a neighboring one;
- [ ] numbers only with [C###]/[S###]; values in the text match the Excel;
- [ ] every initiative has objections and a contribution to the result (sum = 100%);
- [ ] metrics with formulas, units, period and target value;
- [ ] a validation plan: comparison base, duration, counter-metrics, criteria to continue/change/stop.

## Typical mistakes
- "Nice text without calculations": numbers without a model and a source — the reader cannot verify them.
- Tactics without needs: a list of features instead of "pain → mechanic → expected effect".
- An overflowing FAQ-1: the history of the market instead of answering "what does this change for the decision".
- Metrics without a comparison base and a deadline — "we'll grow loyalty" is untestable.
- Excel with "dead" numbers instead of formulas: an assumption you cannot touch.

## Questions that can change the decision
- What is each initiative's contribution to the target metric, and what is it based on?
- What would have to happen for us to abandon the initiative (a stop criterion)?
- Which number in the model is the most fragile, and what would confirm it most cheaply?

## Related maps
[[M-market-sizing]], [[M-traction-model]], [[M-unit-economics]], [[M-outcome-roadmap]], [[M-success-metrics]]
