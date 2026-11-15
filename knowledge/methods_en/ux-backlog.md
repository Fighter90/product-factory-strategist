---
id: M-ux-backlog
lang: en
title: UX backlog, research knowledge base, and big picture — how to store insights so they can be reused and retracted
course: ux
sources: ["EN mirror of the RU methodology card M-ux-backlog (knowledge/methods/ux-backlog.md); original sources are listed in the RU card"]
stages: [research, strategy, validation, after-decision]
tags: [ux-backlog, atomic-research, big-picture, knowledge-base, insights, versioning, triage, metric-linkage]
related: [M-cjm, M-usability-testing, M-ux-heuristics, M-dogfooding, M-workshops, M-ai-in-research, M-product-metrics, M-interview-analysis, M-source-criticism, M-decision-daci]
---

# UX backlog, knowledge base, and big picture

## When to apply
When there are already many studies (or there will be) and knowledge gets lost, duplicated, becomes outdated: you need the problem found in an interview or a test
to reach a decision without losing its evidence, and afterwards to remain findable, reviewable and — if it turns out to be wrong — **retractable**.
Also for onboarding new people and for materials for workshops and strategy sessions.

## Essence
Three related constructs:
1. **Atomic research (D. Pidcock):** knowledge is stored as "atoms" — one insight, one card. The chain: experiment ("we did this") →
   fact ("we saw this") → insight ("this made us think that…") → conclusion ("therefore we will do this"). The unit (nugget): a brief
   observation (what and why) + evidence (video, audio, photo, screenshot) + tags for search (method, segment, business structure, experience).
2. **UX backlog:** a shared open table of problems and insights. It answers "why this matters" (context, evidence, impact estimate),
   whereas the product backlog answers "what to do". Filled in by researchers, designers, product managers, editors; reviewed by the business.
3. **Big picture:** a large file/board about the product for knowledge transfer, quick access and workshops: date of the last update,
   baseline research (drivers/barriers), team ownership zones, CJM, the main CSAT/CES measurements, workshop boards, interesting
   external research, segments, useful links (dashboards, documents). Risk: too much information, hard to keep it up to date.
4. **UJM as a repository:** the user path across screens with the fields "steps → frustrations/obstacles/errors → metrics and description →
   proposals → links to other departments' design". Shows problems strictly against specific screens.

Comparison (from the course): UX backlog — easy to filter, anyone can edit; downside — not everyone remembers the file exists, it is hard to enter all the data.
Big picture — visual, attracts attention; downside — overload and maintenance. Jira/Confluence — convenient for the business and for moving tasks; downside — not everyone has access,
the structure is hard to change. The best combination: the UX backlog as the "why", the tracker as the "what to do".

Record types: **UX problem** (an interface deficiency affecting task completion/speed/satisfaction); **CX problem** (outside the interface:
packaging at the pickup point); **feature request**; **bug** (works differently from intended); **Look&Feel** (minor visual flaws). The type determines the owner (design, support/business, dev, product, front-end + design system).

Principle: **a card without a link to a metric is an opinion; a card plus a metric is an argument.**

## Procedure

### A. Capture the finding (capture)
1. Split the layers: **fact** (observation/quote/number with a timecode and a link) → **insight** (the explanation of "why") → **hypothesis** (what to change and what
   to measure) → **conclusion/decision**. An insight without a link to a fact is not accepted.
2. Fill in the atom fields (below), assign the status `raw`.
3. Assign no more than 3–4 tags across the "three planes": segment × journey stage (CJM) × problem type. More than that is "filter hell".

### B. Triage (once a week: product manager + UX lead + development)
1. Deduplication by the pair "fact + segment".
2. Estimate impact, cost, weight of the evidence; assign the status `confirmed` or `needs-evidence`.
3. Scoring (from the lecture, a simplified formula): `Score = (10 − Cost) × Impact × EvidenceWeight`, where Impact is 1–5, Cost is 1–10,
   EvidenceWeight: 1 — one respondent, 2 — several, 3 — confirmed by a metric. The threshold for entering the nearest sprint is tuned per team (in the lecture, 70+).
   An alternative for money: `ROI = (ΔMetric × LTV × Users_affected) / DevCost`; course guidance: ROI > 1 — into the sprint, 0.3–1 — discuss, < 0.3 — defer.
   All input numbers have a source and a date; estimates made before measurement are hypotheses.
4. Assign an owner and a type; create/link a task in the tracker (the research-link field is mandatory).

### C. Validation and closure
1. After the release, compare the metric against the baseline in the same window and segment (for example, 14 days before/after, a statistical test).
2. Status: `done` (the metric was achieved), `reopen` (not achieved), `dropped` (the insight was retracted).

### D. How to store so that an insight can be retracted (extension for the agent)
- Never delete — change the status and leave a trace: `superseded_by`, `invalidated_reason`, `invalidated_date`.
- Every claim carries: `evidence_ref` (link/file/timecode), `method`, `n`/sample, `date`, `segment`, `confidence` (low/medium/high),
  `source_type` (interview, test, analytics, observation, **team hypothesis**, **synthetic/AI** — see [[M-synthetic-respondents]]).
- Shelf life: a review date; items outdated by age or after a major release → status `stale`, revalidation.
- With contradictory data: both atoms remain, with a `conflicts_with` link between them; the decision is recorded as a separate entry ([[M-decision-daci]]).
- If a fact is disproven — cascade-flag the derived insights and hypotheses as `needs-revalidation`.
- Do not mix criticality/frequency with credibility: "serious but weakly evidenced" is a separate category.

### E. Maintenance rituals
A weekly digest of new entries; a quarterly cleanup of "dead" links and a review of versions; once or twice a year a review of outdated
insights; a "Paint it red" workshop (on the big picture — pick the red zones and turn them into an action plan, see [[M-workshops]]).
Roles: the researcher updates statuses and enters insights; the designer — problems found in the interface; the product manager looks for ideas; the business tracks
execution; everyone else reads. The lead researcher moderates the process and develops the big picture; the others work in their own areas.

## Template / checklist

**UX backlog row (lecture fields):** Platform | Target-audience segment | Product category | Source of knowledge | Rough estimate of the impact on the product |
Criticality | Comments | Status | Entered by | Impact on metrics.

**Atom (minimum):**
`atom_id | research_type | segment | product_area | fact (quote/number + timecode) | insight (one "why" phrase) | evidence (link) | tags (≤4) | status (raw/confirmed/used/stale/dropped) | backlog_ref | metric_id + baseline | confidence | date | superseded_by`

**Readiness for quantitative validation:** a metric_id is set; the baseline (window) is fixed; the target delta in percentage points/seconds is stated; the affected
users are estimated; the engineers have given a realistic cost estimate; the ROI is calculated.

**Layered repository** (each layer references the one below it: report → transcript → video): raw data (audio, video, logs) → facts/codes →
artifacts (CJM, prototypes, reports) → metrics (dashboards) → decisions (epics). Document versioning: major — restructuring of the stages, minor —
new pains/metrics, patch — edits; the change date in the name/properties.

## Typical mistakes
| Mistake | Consequence | Antidote |
|---|---|---|
| Insight without a fact | "Hot air", impossible to prove | A mandatory evidence field |
| 10+ tags | Noise in search | ≤3–4 tags across the three planes |
| No owner and no status | Hanging entries | Auto-fill the author, weekly triage |
| Duplicates | Bloat of the database | A check on fact + segment |
| Card without a metric | An opinion, not an argument | metric_id is required for prioritization |
| Baseline from different windows | A false win/failure | A fixed before/after window |
| Underestimated DevCost | Inflated ROI | A post-mortem on actual hours |
| The file exists but nobody uses it | Knowledge never reaches decisions | Rituals, the research-link field in tasks, the digest |
| CX and UX mixed | Tasks go to the wrong people | Typing of records |
| Old insights are never retracted | Decisions on outdated data | Shelf life, the stale status, re-evaluation |

## Questions that can change the decision
- Who will maintain the knowledge base (owner and ritual)? Without this, a simple table is better than a complex system.
- Do all the people who need the knowledge have access to the tracker? Otherwise, an open table.
- Which metrics and baselines are available? Without them the cards remain opinions.
- How many studies per quarter: with single-digit counts a table is enough, with hundreds you need an Ops role and tags.
- Which data must not go into external services (personal data, trade secrets)?

## Related cards
[[M-cjm]], [[M-usability-testing]], [[M-ux-heuristics]], [[M-dogfooding]], [[M-workshops]], [[M-ai-in-research]], [[M-synthetic-respondents]], [[M-product-metrics]], [[M-interview-analysis]], [[M-source-criticism]], [[M-decision-daci]]
