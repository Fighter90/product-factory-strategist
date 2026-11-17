# Six-pager (EN)

> EN draft — pending the EN six-pager is written in plain English by the six-pager-writer from the SAME data package outputs/six_pager_pack.md (claims, sources, calculations; documents 00–07 are RU inputs — never pasted verbatim), per the spec `knowledge/templates/SIX_PAGER_PROMPT_EN.md`, style guide `knowledge/templates/STYLE_EN.md` (plain English, numbers 1,234.5, no calque). Restate the project title and question in English (project.json: title, question). Mandatory loop: write → `pfs check --six-pager` → fix until 0 errors. Assembled 2026-11-17T07:38 by `pfs export --six-pager`. Numbers carry sequential footnotes in the same order and numbering as RU SIX_PAGER.md; each footnote names its source ID: S### — publisher — title — date — URL — grade A–D. Raw C###/S### tags stay out of the six-pager; the full evidence registry lives in REPORT.md.

**Request:** — write in English; RU source: project.json → question.

## FAQ-1. Current state analysis

### 1.1 Market overview: trends, challenges and opportunities

> EN draft — pending: write this section in English from the data package outputs/six_pager_pack.md (pack sections: situation (market, known facts, contradictions, unknowns) plus the claims and sources lists); spec: knowledge/templates/SIX_PAGER_PROMPT_EN.md, style: knowledge/templates/STYLE_EN.md.

### 1.2 Key competitors: growth and promo mechanics

> EN draft — pending: write this section in English from the data package outputs/six_pager_pack.md (pack situation — competitor groups; risks rated High/Medium/Low); spec: knowledge/templates/SIX_PAGER_PROMPT_EN.md, style: knowledge/templates/STYLE_EN.md.

Comparative table of competitor groups (fill in after competitive analysis):

| | Group 1 | Group 2 | Group 3 |
|---|---|---|---|
| **Key advantages** | … | … | … |
| **Growth and promo mechanics** | … | … | … |
| **Risks for the company** | … — High/Medium/Low | … | … |

> **Conclusion (inference):** the opportunity window and its horizon — fill from 1.1–1.2.

## FAQ-2. User Persona. Who is the target audience?

### 2.1 Segments

> EN draft — pending: write this section in English from the data package outputs/six_pager_pack.md (pack situation — segments/personas and the JTBD user barrier); spec: knowledge/templates/SIX_PAGER_PROMPT_EN.md, style: knowledge/templates/STYLE_EN.md.

Persona table (fill in):

| | Segment 1 | Segment 2 | Segment 3 |
|---|---|---|---|
| **Who are they?** | … | … | … |
| **What do they use today and why?** | … | … | … |
| **What difficulties do they face?** | … | … | … |
| **Common difficulties** | … | … |

### 2.2 Barriers at each journey stage

> EN draft — pending: write this section in English from the data package outputs/six_pager_pack.md (pack situation — barriers per journey stage, hold-backs per segment); spec: knowledge/templates/SIX_PAGER_PROMPT_EN.md, style: knowledge/templates/STYLE_EN.md.

| Journey stage | Barrier today | What the product does |
|---|---|---|
| Acquisition | … | … |
| Choice / usage | … | … |
| Payment | … | … |
| Post-payment experience | … | … |

What holds back signup or renewal? (fill in per segment):

| Segment | Blocking factor | How it is removed |
|---|---|---|
| Segment 1 | … | … |

> **Conclusion (inference):** segment by the entry barrier; the tier ladder serves all barriers; prioritize by capacity/CAC/competition (calculation above).

## FAQ-3. Strategic initiatives. Justify each one briefly.

> EN draft — pending: write this section in English from the data package outputs/six_pager_pack.md (pack sections options, leader's choice and initiatives: chosen direction, red-team objections, 3–4 driver initiatives); spec: knowledge/templates/SIX_PAGER_PROMPT_EN.md, style: knowledge/templates/STYLE_EN.md.

### Initiatives of the chosen direction (drivers)

Formulate 3–4 initiatives as: «**First driver** — …», «**Second driver** — …», then «Key directions» (bullets) and a step-by-step effect calculation. Data — the pack sections options, leader's choice and initiatives. Close with an inference-conclusion.

Unit economics — step-by-step:

Assumptions: Юнит-допущения [C057]: ARPU €25 (Unlimited; коридор CVDesignR €9,99 [C023] ↔ resume.io €24,95 [C026]); переменные 25%; churn 8%/мес. CAC €30 — допущение для чувствительности платного сценария; денежный CAC органики ≈ 0 [04_product_strategy]. Для ЕС не подтверждены — проверка на валидации [06_validation_plan]

| Formula | Calculation | Result |
|---|---|---|
| CM = ARPU × (1 − variable share) | 25.00 × (1 − 0.25) = 25.00 × 0.75 | **CM = 18.75** |
| Average paying lifetime = 1 / churn | 1 / 0.08 | **12.50 mo** |
| LTV = CM / churn | 18.75 / 0.08 | **LTV = 234.38** |
| LTV/CAC | 234.38 / 30.00 | **7.81** (target ≥ 3) |
| CAC payback = CAC / CM | 30.00 / 18.75 | **1.60 mo** |

**Conclusion (inference):** LTV/CAC ≥ 3 holds up to churn ≈ 20.83 %/mo, CAC ≈ €78.12, variable-cost share ≈ 61.60 % (each threshold — all else equal; grid — the sensitivity sheet).

## FAQ-4. Tactics. Detail each initiative into concrete tactics.

> EN draft — pending: write this section in English from the data package outputs/six_pager_pack.md (pack initiatives (focus, tactics, gates) — the tactics matrix); spec: knowledge/templates/SIX_PAGER_PROMPT_EN.md, style: knowledge/templates/STYLE_EN.md.

Tactics matrix (fill in):

| Strategic initiative | Focus | User needs and expectations | Solutions (tactics) |
|---|---|---|---|
| Initiative 1 | … | … | … |
| Initiative 2 | … | … | … |

## FAQ-5. High-level implementation plan

> EN draft — pending: write this section in English from the data package outputs/six_pager_pack.md (pack sections decisions, leader's choice and initiatives — order, season timing, parallel tracks); spec: knowledge/templates/SIX_PAGER_PROMPT_EN.md, style: knowledge/templates/STYLE_EN.md.

Expected contribution of initiatives to the outcome (must sum to 100%):

- __% — Initiative 1;
- __% — Initiative 2;
- __% — Initiative 3.

Tactic order: high → medium → base priority. Timing follows market seasons. Parallel tracks: community/partnerships — off the main line.

## FAQ-6. Success metrics. KPIs in two dimensions

> EN draft — pending: write this section in English from the data package outputs/six_pager_pack.md (pack sections KPI and calculations — business and product planes, counter-metrics per red-team hit); spec: knowledge/templates/SIX_PAGER_PROMPT_EN.md, style: knowledge/templates/STYLE_EN.md.


## Sources (footnotes)

> EN draft — pending: write this section in English from the data package outputs/six_pager_pack.md (source footnotes by first mention: publisher, title, date, URL, grade A–D; cited sources only; synthetic listed separately (hypotheses, not evidence)); spec: knowledge/templates/SIX_PAGER_PROMPT_EN.md, style: knowledge/templates/STYLE_EN.md.

## Appendices (Excel)

> Appendices are built by `pfs calc all` into outputs/attachments/: unit_economics.xlsx, growth_model.xlsx, cohort_retention.xlsx, market_sizing.xlsx. Formulas recalculate on open (Excel / Numbers / LibreOffice); the input sheet inside each workbook carries RU labels — edit the values there.


> Formulas recalculate on open (Excel / Numbers / LibreOffice). Detailing per the spec: knowledge/templates/SIX_PAGER_PROMPT_EN.md. Full evidence version — REPORT.md.
