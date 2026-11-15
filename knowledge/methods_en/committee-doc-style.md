---
id: M-committee-doc-style
lang: en
title: Committee document style — Russian and English output language, grammar, no calquing
course: skills
sources: ["EN mirror of the RU methodology card M-committee-doc-style (knowledge/methods/committee-doc-style.md); original sources are listed in the RU card"]
stages: [strategy, review, decision]
tags: [style, document, committee, language, anglicisms, calque, editing, grammar, terminology]
related: [M-six-pager-etalon, M-six-pager, M-product-communication, M-source-criticism, M-decision-daci]
---

# Committee document style (RU and EN)

## When to apply
When writing and revising any document a human reads: a six-pager, strategies, a validation plan, a decision,
a cover memo. A committee document is argued over line by line — linguistic carelessness reads as careless
thinking and undermines trust in the numbers. The card fixes two loops: RU output without bureaucratese,
jargon, and needless anglicisms; EN output without calques from Russian.

## Core

### General rules (both languages)
1. **The reader is a busy skeptic.** Short sentences (12–20 words on average), one thesis per paragraph,
   the conclusion before the justification where the reader is in a hurry ("Conclusion: … because …").
2. **One term, one word.** "Tier" does not alternate with "plan" and "package"; a glossary of terms lives
   at the start of the project, not in the reader's head.
3. **Numbers are verifiable**: units, period, comparison base ("payment conversion, %, month over month").
4. **No evaluative adverbs in place of an argument**: "significantly", "substantially", "far" — only together
   with a number.
5. **Passive voice is acceptable when the actor does not matter**; otherwise — active: not "a decision was
   made", but "the committee decided".

### Russian output (PRO-52)
- An anglicism only when there is no established Russian equivalent or the term is industry-specific
  (the anglicism for "feature" → the Russian for function/capability; "location" → the Russian for
  place/position; "community" → the Russian for community; "mapping" → the Russian for correspondence;
  the noun "checklist" is acceptable, the slang verb "to check off" is not).
- Jargon and bureaucratese: "we are carrying out a launch" → "we launch"; "within the framework of the given
  step" → "at this step"; "a growth takes place" → "it grows".
- The distinct letter for "yo", dashes, and «guillemet» quotes follow Russian typographic rules; non-breaking
  spaces before units (500 ₽, 12 %) — if the document format supports them.
- A separate editing pass: reread for language only (not for meaning); the edits do not touch C###/S### tags.

### English output (PRO-53)
- Calquing from Russian is the main defect: "make actualization of tariff plan" ← the Russian "to carry out
  an actualization". Rule: restate the thought rather than translate word for word; long Russian genitive
  chains ("the growth model of the service's user base") are split into two sentences.
- The EN version of a document is **written** in English from the same data package (claims, sources,
  calculations), not translated; the RU text of documents 00–07 is the writer's input and is not inserted
  into EN. Style guide: `knowledge/templates/STYLE_EN.md` (plain English, numbers 1,234.5, €24.95, y/y,
  dates "1 June 2026", consistent terminology); the `pfs check` linter catches Cyrillic, Russian decimal
  commas, and the marker "[RU source — translate]" in SIX_PAGER_EN.md.
- EN templates: section headings use established English wording (When to use, Core, Procedure,
  Typical mistakes); bullets start with different words, not the same verb.
- False friends and stylistic traps: "actual" is not "up-to-date" (the Russian look-alike) but "currently
  in effect"; "momentary" is not "instant"; "perspective" is not "promising". Dates in the format
  1 June 2026 or 2026-06-01, not "01.06.26"; the decimal separator is a period.
- Names of tiers, brands, and artifact sections (02_situation.md) stay as they are; an explanation is given
  at first mention.

### Connection to the repository's language rules
Repository pattern: CLI output and help are in Russian; documentation is bilingual where it is bilingual
(rule 9 of AGENTS.md). A project document (six-pager, REPORT) is the RU canon of evidence plus an EN version
written in English from the same data package: identical numbers and C###/S### tags, one structure, with
tag reconciliation RU↔EN in `pfs check`.

## Procedure (agent)
1. Write the draft following the document's card (for example, `M-six-pager-etalon`), without thinking about style.
2. Pass 1 — meaning and evidence: every conclusion is backed, every number has a tag and units.
3. Pass 2 — RU style: anglicisms → Russian equivalents per the list above; bureaucratese → verbs;
   long sentences split.
4. Pass 3 — EN version: write in English from the same data package (not a translation!); check for calques
   against the STYLE_EN.md trap list; synchronize numbers and tags with the RU version.
5. Final: reread the first paragraph of each section — does the conclusion read without the rest of the text?

## Template / checklist
- [ ] Sentences average ≤ 20 words; no wall-of-text paragraphs.
- [ ] One term — one word across the whole document.
- [ ] No "significantly/substantially" without a number next to it.
- [ ] RU: no slang jargon, no bureaucratese ("we are performing"), no needless anglicisms.
- [ ] EN: no calques ("make actualization"), dates and numbers in EN format, headings follow English templates.
- [ ] Numbers in RU and EN match to the digit; C###/S### tags are not lost in translation.
- [ ] Each section's conclusion reads separately from its justification.

## Typical mistakes
- "Pretty" style instead of precise: metaphors and epithets where the committee needs a formula.
- Language mixing in one document: English terms inside the RU text without need (and vice versa).
- A translation of the translation: the EN version carries the Russian syntactic structure verbatim —
  a native speaker spots the calque from the first paragraph.
- Editing erases evidence: a style fix loses a C### tag or units of measure.
- Different terms for one concept in the RU and EN versions — a reader of both languages thinks these are
  different things.

## Questions that could change the decision
- Which sentence of the document will the committee reread twice — and is it clear without context?
- Which term in the document is ambiguous and can be read two ways during an argument?
- Where does the EN version diverge from the RU one in numbers or terms — and which version becomes the
  "canon" in a divergence?

## Related cards
[[M-six-pager-etalon]], [[M-six-pager]], [[M-product-communication]], [[M-source-criticism]], [[M-decision-daci]]
