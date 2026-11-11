---
id: M-ux-backlog
lang: en
title: UX backlog, research knowledge base and big picture — how to store insights so they can be reused and retracted
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [research, strategy, validation, after-decision]
tags: [ux-backlog, atomic-research, big-picture, knowledge-base, insights, versioning, triage, metric-links]
related: [M-cjm, M-usability-testing, M-ux-heuristics, M-dogfooding, M-workshops, M-ai-in-research, M-product-metrics, M-interview-analysis, M-source-criticism, M-decision-daci]
---

# UX backlog, knowledge base and big picture

## When to apply
When there is already a lot of research (or there will be) and knowledge gets lost, duplicated, goes stale: a problem found in an interview or a test must reach a solution without losing its evidence, and afterwards stay findable, revisable and — if it turns out to be wrong — **retractable**. Also for onboarding new people and for material for workshops and strategy sessions.

## Core idea
Three connected constructs:
1. **Atomic research (D. Pidcock):** knowledge is stored as "atoms" — one insight, one card. The chain: experiment ("we did this") → fact ("we saw this") → insight ("this made us think that…") → conclusion ("therefore we will do this"). The unit (nugget): a short observation (what and why) + evidence (video, audio, photo, screenshot) + tags for search (method, segment, business structure, experience).
2. **UX backlog:** a common open table of problems and insights. It answers "why this matters" (context, evidence, impact estimate), whereas the product backlog answers "what to do". It is filled in by researchers, designers, PMs, editors; the business looks at it.
3. **Big picture:** a large file/board about the product for knowledge transfer, quick access and workshops: date of the last update, base research (drivers/barriers), team ownership zones, CJM, the main CSAT/CES measurements, workshop boards, notable external research, segments, useful links (dashboards, documents). Risk: too much information, hard to keep up to date.
4. **UJM as storage:** the user journey by screens with the fields "steps → frustrations/obstacles/errors → metrics and description → suggestions → links to other departments' designs". Shows problems strictly at specific screens.

Comparison (from the course): UX backlog — easy to filter, anyone can edit it; minus — not everyone remembers the file exists, and entering all the data is laborious. Big picture — visual, attracts attention; minus — overload and upkeep. Jira/Confluence — convenient for the business and for moving tasks; minus — not everyone has access, and the structure is hard to change. The best combination: the UX backlog as "why", the tracker as "what to do".

Record types: **UX problem** (an interface deficiency affecting completion/speed/satisfaction); **CX problem** (outside the interface: packaging at the pickup point); **feature request**; **bug** (works differently from the design); **Look&Feel** (minor visual flaws). The type determines the owner (design, support/business, dev, PM, front-end + design system).

Principle: **a card without a link to a metric is an opinion; a card plus a metric is an argument.**

## Procedure

### A. Capture the finding (capture)
1. Separate the layers: **fact** (observation/quote/number with timecode and link) → **insight** (the explanation of "why") → **hypothesis** (what to change and what to measure) → **conclusion/decision**. An insight without a link to a fact is not accepted.
2. Fill in the atom fields (below), assign the status `raw`.
3. Add no more than 3–4 tags across "three planes": segment × journey stage (CJM) × problem type. More is "filter hell".

### B. Triage (once a week: PM + UX lead + engineering)
1. Deduplicate on the "fact + segment" pair.
2. Assess impact, cost and the weight of evidence; assign the status `confirmed` or `needs-evidence`.
3. Scoring (from the lecture, a simplified formula): `Score = (10 − Cost) × Impact × EvidenceWeight`, where Impact 1–5, Cost 1–10, EvidenceWeight: 1 — one respondent, 2 — several, 3 — confirmed by a metric. The threshold for entering the nearest sprint is calibrated on the team (70+ in the lecture). A money alternative: `ROI = (ΔMetric × LTV × Users_affected) / DevCost`; course benchmark: ROI > 1 — into the sprint, 0.3–1 — discuss, < 0.3 — defer. Every input number has a source and a date; estimates made before measurement are hypotheses.
4. Assign the owner and the type; create/link the task in the tracker (the research-link field is mandatory).

### C. Validation and closure
1. After release, compare the metric against the baseline in the same window and segment (e.g. 14 days before/after, a statistical test).
2. Status: `done` (the metric was reached), `reopen` (not reached), `dropped` (the insight was retracted).

### D. How to store so an insight can be retracted (extension for the agent)
- Never delete — change the status and leave a trail: `superseded_by`, `invalidated_reason`, `invalidated_date`.
- Every claim carries: `evidence_ref` (link/file/timecode), `method`, `n`/sample, `date`, `segment`, `confidence` (low/medium/high), `source_type` (interview, test, analytics, observation, **team hypothesis**, **synthetic/AI** — see [[M-synthetic-respondents]]).
- Expiry date: a review date; records past their deadline or a major release → status `stale`, re-validation.
- With conflicting data: both atoms remain, with a `conflicts_with` link between them; the decision is recorded as a separate entry ([[M-decision-daci]]).
- If a fact is refuted, cascade-mark the derived insights and hypotheses `needs-revalidation`.
- Do not mix severity/frequency with confidence: "serious but weakly evidenced" is a separate category.

### E. Upkeep rituals
A weekly digest of new records; a quarterly cleanup of "dead" links and a review of versions; once or twice a year a review of stale insights; the workshop "Paint over the red" (on the big picture — pick the red zones and turn them into an action plan, see [[M-workshops]]).
Roles: the researcher updates statuses and adds insights; the designer — problems found in the interface; the PM looks for ideas; the business watches execution; everyone else reads. The lead researcher moderates the process and develops the big picture; the others work in their own areas.

## Template / checklist

**UX backlog row (fields from the lecture):** Platform | Target-audience segment | Product category | Source of knowledge | Rough estimate of impact on the product | Severity | Comments | Status | Entered by | Impact on metrics.

**Atom (minimum):**
`atom_id | research_type | segment | product_area | fact (quote/number + timecode) | insight (one phrase "why") | evidence (link) | tags (≤4) | status (raw/confirmed/used/stale/dropped) | backlog_ref | metric_id + baseline | confidence | date | superseded_by`

**Readiness for quantitative validation:** a metric_id is set; a baseline is fixed (window); the target delta in percentage points/seconds; the affected users are estimated; engineers have given a realistic cost estimate; ROI is calculated.

**Layered storage** (each layer links to the one below: report → transcript → video): raw data (audio, video, logs) → facts/codes → artifacts (CJM, prototypes, reports) → metrics (dashboards) → decisions (epics). Document versioning: major — restructuring of the stages, minor — new pains/metrics, patch — edits; the change date in the title/properties.

## Typical mistakes
| Mistake | Consequence | Antidote |
|---|---|---|
| Insight without a fact | "Air", impossible to prove | The evidence field is mandatory |
| 10+ tags | Noise in search | ≤3–4 tags across the three planes |
| No owner or status | Hanging records | Auto-filled author, weekly triage |
| Duplicates | Bloat of the base | A check on fact + segment |
| Card without a metric | An opinion, not an argument | metric_id required for prioritization |
| Baseline from different windows | A false win/loss | A fixed before/after window |
| Underestimated DevCost | Inflated ROI | A post-mortem on actual hours |
| The file exists but nobody uses it | Knowledge never reaches decisions | Rituals, a research-link field in tasks, the digest |
| CX and UX mixed | Tasks routed to the wrong people | Typing of records |
| Old insights are never retracted | Decisions on stale data | Expiry dates, the stale status, re-assessment |

## Questions that can change the decision
- Who will maintain the base (owner and ritual)? Without that, a simple table beats a complex system.
- Does everyone who needs the knowledge have access to the tracker? Otherwise an open table.
- Which metrics and baselines are available? Without them the cards remain opinions.
- How much research per quarter: with single units a table is enough, with hundreds you need an Ops role and tags.
- Which data must not be put into external services (personal data, trade secrets)?

## Related maps
[[M-cjm]], [[M-usability-testing]], [[M-ux-heuristics]], [[M-dogfooding]], [[M-workshops]], [[M-ai-in-research]], [[M-synthetic-respondents]], [[M-product-metrics]], [[M-interview-analysis]], [[M-source-criticism]], [[M-decision-daci]]
