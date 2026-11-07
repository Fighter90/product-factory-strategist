---
id: M-six-pager-en
title: Six-pager — six-FAQ strategic report with Excel appendices for committee defense
course: pm-approaches-en
sources: ["EN summary of the RU methodology card; original sources listed in the RU card"]
stages: [options, strategy, validation, review]
tags: [en, summary]
related: []
---

# Six-pager (EN summary)

**When:** a recommendation is defended before a committee/leadership: a compact (~6 meaningful pages) document in a fixed structure where each section answers a known question and the numbers are computed in Excel appendices, not "in the air". In the agent it is assembled by `pfs export --six-pager`.

**Core:** six FAQ sections, each answering the decision-maker's question: **FAQ-1** — what's happening in the market, who are the competitors, what's the challenge (from the situation document: a short answer, what's known, contradictions); **FAQ-2** — who are the users and what are their pains along the journey (segments/personas from the situation or strategy); **FAQ-3** — which initiatives are proposed and why exactly these (options + strong objections + recommendation); **FAQ-4** — what each initiative concretely consists of (tactics: Focus → Needs & desires → Solutions); **FAQ-5** — how it will be implemented and how success will be recognized (validation plan + plan/initiative contributions); **FAQ-6** — which metrics measure success (business and product metrics with formulas). Structure rules: initiative contributions to the result sum to 100%; every initiative carries strong objections; "keep as is" and "shut the direction down" are present as full alternatives; the competitor table is "advantage → risk for us"; tactics are tied to needs, not features.

**How:** (1) wait for documents 02/03/04/06 to be ready; (2) collect parameters from the claims registry into the project's calcs file (every value → a C### claim); (3) a background subagent runs the full calculation set → Excel appendices (unit economics, growth model, cohorts, market size; an "Inputs" sheet with editable parameters, calculations as live formulas); (4) run the six-pager export → `outputs/SIX_PAGER.md`; check every FAQ section is filled; (5) run the quality check with no new errors; show the owner the appendix list and what is editable in each.

**Pitfalls:** beautiful text without calculations — numbers without a model and source can't be verified by the reader; tactics without needs — a feature list instead of "pain → mechanic → expected effect"; an overflowing FAQ-1 — market history instead of answering "what does this change for the decision"; metrics without a comparison base and deadline ("we'll grow loyalty" is untestable); Excel with dead numbers instead of formulas — assumptions can't be probed.

**RU-версия:** `knowledge/methods/six-pager-report.md` (полная методика).
