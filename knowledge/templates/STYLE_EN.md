# English Style Guide for Executive Output (STYLE_EN.md)

> Binding for every English document the agent writes for a human reader:
> `SIX_PAGER_EN.md`, EN versions of REPORT/strategy documents, cover letters.
> Used by the six-pager-writer (authoring) and the editor (proofreading pass).
> Russian counterpart: `knowledge/methods/committee-doc-style.md` (RU style).
> Introduced by PRO-53: the EN output must read like English, not like
> translated Russian.

## Core principle: write, don't translate

1. The EN version is **written in English from the same data package** (claims,
   sources, calculations; documents 00–07 are RU *inputs*, never pasted verbatim).
   The old marker `[RU source — translate]` is a banned artifact: if it survives in
   `outputs/SIX_PAGER_EN.md`, the document is unfinished and `pfs check` flags it.
2. Formulate the thought in English; do not render Russian syntax. Long Russian
   genitive chains ("модель роста базы пользователей сервиса") become two English
   sentences ("a growth model for the service's user base. It drives…" or similar).
3. The evidence contract is language-neutral: every number keeps its C###/S### tag,
   every conclusion keeps the chain "data → grounds → calculation → conclusion",
   and figures match the RU registry to the sign.

## Plain English for the executive reader

- Short sentences (average 12–20 words), one thesis per paragraph; put the
  conclusion before the grounds where the reader is in a hurry.
- Active voice and concrete verbs over nominal style: "the committee decided",
  not "a decision was made"; "churn falls to 3%", not "a reduction in churn is
  observed".
- One term — one word across the document (glossary at the first mention).
  Do not alternate synonyms: "plan" does not become "tariff/package" mid-text.
- Headings read like English headings (established wording: "Market overview",
  "Key competitors", "High-level implementation plan"). Bullets do not all start
  with the same verb.

## Numbers, units, dates

- Numbers: **1,234.5** — the comma separates thousands, the dot is the decimal
  separator. Never `8,5` or `1,234,5`; `42,635` (thousands) and `1,234.5` are correct.
- Currency: **€24.95**, €9–12; keep the currency with every amount in tables.
- Growth rates: **y/y** (year over year), m/m (month over month): "+44% tech
  vacancies y/y (2025)".
- Dates: **1 June 2026** or **2026-06-01**; never `01.06.26`.
- Every number carries units, period, and comparison base: "109,000 unfilled IT
  vacancies (DE, 2025)"; "CVR 2.3% month over month".

## Terminology (unified)

| Write | Not (calque) |
|---|---|
| KPIs in two dimensions (business and product) | «KPIs in two planes» |
| Solutions (tactics) — the tactics-matrix column | «Decisions (tactics)» |
| launch the hosted version / the hosted version's launch | «the hosted launch» |
| fall back to option B/E | «a fallback to B/E» (verb) |
| shift the focus to community and PR | «a pivot to community/PR» |
| the Domain Rating is too low to rank | «the DR does not carry» |
| a shortage indicator of 1.1 for "IT engineers" | «…for "IT engineers" of 1.1» |

- Artifact names stay as-is with an explanation at first mention:
  `02_situation.md`, tags C###/S###/D###, Excel sheet labels, product and plan names.

## False friends and traps

- **actual** = "current/real", not "relevant/up-to-date"; use "current" or "up-to-date".
- **momentary** = "lasting a moment", not "instant"; **perspective** = "viewpoint",
  not "promising" (use "promising", "outlook").
- Drop empty articles on process nouns: "fall back to option B/E", not "a fallback
  to B/E" when the sentence needs a verb.
- No Russian connective calques: "on the basis of the data" → "based on the data";
  "in the framework of this step" → "at this step"; "it is necessary to note" →
  "note that" (or delete).

## Editor pass (proofreading)

1. After writing, run a dedicated editor pass with this guide: read **for language
   only**, not for meaning; C###/S### tags, numbers, units, and table structure are
   untouchable.
2. Rubric — sample 3 sections and score each 1–5 on "reads like it was written in
   English by a native speaker"; the document is accepted at **≥ 4/5 on every
   sampled section**, otherwise rewrite the weak sections (not word-by-word patching).
3. Linter (`pfs check`): `SIX_PAGER_EN.md` must contain no Cyrillic, no Russian
   decimal commas (`8,5`), and no `[RU source — translate]` marker; warnings name
   the offending lines.

## Checklist

- [ ] Sentences ≤ 20 words on average; no wall paragraphs; conclusions read on their own.
- [ ] No calques from the trap tables; headings and bullets read like English.
- [ ] Numbers `1,234.5`; currency `€24.95`; growth `y/y`; dates `1 June 2026`.
- [ ] One term per concept; artifact names preserved and explained at first mention.
- [ ] Tags C###/S###/D### intact; figures match the RU registry to the sign.
- [ ] `pfs check` — no `SIX_PAGER_EN.md` warnings.
