---
id: M-six-pager
lang: en
title: Six-pager — a six-page strategy report with Excel appendices
course: strategy
sources: ["EN mirror of the RU methodology card M-six-pager (knowledge/methods/six-pager.md); original sources are listed in the RU card"]
stages: [options, strategy, validation, review]
tags: [report, six-pager, committee, excel]
related: [M-market-sizing, M-traction-model, M-unit-economics, M-outcome-roadmap, M-success-metrics]
---

# Six-pager

## When to apply
When a recommendation is defended before a committee/leadership: a compact (≈6 substantive pages) document is needed in a fixed structure, where each section answers a known question and the numbers are computed in Excel appendices rather than "in thin air". In the agent it is assembled by the command `pfs export --six-pager`.

## Essence
Six FAQ sections, each an answer to the decision-maker's question:

| Section | The reader's question | What serves as input (data, not prose) |
|---|---|---|
| FAQ-1 | What is happening on the market, who are the competitors, what is the challenge? | numbers and tensions from `02_situation.md` — written anew per the reference 1.1–1.2, not pasted in |
| FAQ-2 | Who are the users, what are their pains along the journey? | segments/personas from the situation or strategy — tables 2.1–2.2 of the reference |
| FAQ-3 | Which initiatives are proposed and why exactly those? | options, objections and the recommendation from `03_options.md` — rewritten into the "driver → directions → calculation" construction |
| FAQ-4 | What exactly does each initiative consist of? | tactics: Focus → Needs & desires → Solutions — the reference matrix |
| FAQ-5 | How will it be implemented and how will we know it worked? | `06_validation_plan.md` + the initiatives' plan/contribution — sections 5.x of the reference |
| FAQ-6 | By which metrics do we measure success? | business and product metrics with formulas |

The document is **written per the reference** `knowledge/templates/SIX_PAGER_PROMPT.md` (numbered sub-items 1.1, 2.1…, mandatory tables, a "Conclusion (inference)" in every FAQ), not assembled by pasting documents 02/03/04/06 — those serve as sources of data and claims. See the card `M-six-pager-etalon` (a "good/bad" breakdown per FAQ).

Structure rules: the initiatives' contribution to the result sums to 100%; every initiative has strong objections; "keep as is" and "shut the direction down" are present as full-fledged alternatives; a competitor table "advantage → risk for us"; tactics tied to needs, not to features.

## Procedure (agent)
1. Wait for documents 02/03/04/06 to be ready — they are the source of numbers and claims, but not the structure of the document
   (see the skill `six-pager` and the card `M-six-pager-etalon`).
2. Collect parameters from the claims registry in `projects/<slug>/calcs.json` (every value → C###).
3. With a background subagent: `pfs calc all` → `outputs/attachments/*.xlsx` (unit economics, growth model,
   cohorts, market size; an "Input" sheet with editable parameters, calculations as formulas).
4. `pfs export --six-pager` → the skeleton `outputs/SIX_PAGER.md`; elaborate each FAQ per the reference
   `knowledge/templates/SIX_PAGER_PROMPT.md` (numbered sub-items, tables, "Conclusion"), not by pasting 02/03/04/06.
5. `pfs check` with no new errors; show the lead the list of appendices and what can be edited in them.

## Template / checklist
See `knowledge/templates/six_pager.md`. Quality checklist:
- [ ] every section answers "its own" question, not retells the neighboring one;
- [ ] numbers only with [C###]/[S###]; values in the text match the Excel;
- [ ] every initiative has objections and a contribution to the result (the sum = 100%);
- [ ] metrics with formulas, units, period and target value;
- [ ] a validation plan: comparison base, time frame, counter-metrics, criteria to continue/change/stop.

## Common mistakes
- "Nice text without calculations": numbers without a model and a source — the reader cannot verify them.
- Tactics without needs: a feature list instead of "pain → mechanic → expected effect".
- An overfilled FAQ-1: market history instead of answering "what does this change for the decision".
- Metrics without a comparison base and a time frame — "we will grow loyalty" is not testable.
- Excel with "dead" numbers instead of formulas: an assumption cannot be probed.

## Questions that can change the decision
- What is each initiative's contribution to the target metric, and what is it based on?
- What would have to happen for us to abandon the initiative (a stopping criterion)?
- Which number in the model is the most fragile, and what would confirm it most cheaply?

## Related cards
[[M-market-sizing]], [[M-traction-model]], [[M-unit-economics]], [[M-outcome-roadmap]], [[M-success-metrics]]
