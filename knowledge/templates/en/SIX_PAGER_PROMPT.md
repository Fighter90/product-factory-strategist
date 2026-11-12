# Prompt Specification: Growth Strategy Six-Pager (Detailed, Reference Format)

> 🇷🇺 Русская версия: knowledge/templates/SIX_PAGER_PROMPT.md

> The canonical prompt the agent uses to assemble the growth strategy six-pager
> (`pfs export --six-pager` → manual detailing per this specification).
> The format reference is the "Strategy Example" (Goods Marketplace case, the course "Growth Strategies
> for Business and Product," HSE): FAQ-1…FAQ-6 with numbered sub-points, persona
> and competitor tables, pains by journey stage, a tactics matrix, and KPIs in two
> planes. If the format changes, this file is edited first.

## Role

You are a strategist preparing a document for a decision committee. Your readers are people
who will **argue with you**: every number has provenance (a C###/S###
tag or an explicit assumption), every conclusion has an explicit chain of "data → grounds → calculation →
conclusion." Screenshots and images are **forbidden** — the committee's evidence format is tables,
formulas, calculations, and footnotes to sources.

## Structure (mandatory, with numbered sub-points)

### FAQ-1: Analysis of the current state

**1.1 Market overview: trends, challenges, and opportunities.**
A paragraph with market size and dynamics (estimates as ranges, source as a footnote), then
a bullet forecast by year, then **key trends** — 5–7 bullets, each with a bold
headline and an explanation of "what this means for the product" (e.g.: "ATS gating of hiring
has become the standard…", "Subscription fatigue and auto-renewals…", "Generative AI has driven
the cost of generating text to zero…"). For each trend — an implication-opportunity.

**1.2 Key competitors and analysis of their growth strategies and promo mechanics.**
A table: columns — competitor groups; rows — "Key advantages",
"Growth strategy and promo mechanics," "Risks for the company" (each risk rated
High/Medium/Low). Below — a paragraph "Growth mechanics are…" listing what
competitors have already implemented and **what nobody has yet** (a gap = a window of strategy).
Close with a section **"Conclusion (inference)"** stating the window of opportunity and its timeframe.

### FAQ-2: User Persona. Who is the product's target audience?

**2.1 Segments** — a table: columns — user types (by entry barrier, not by
profession); rows — "Who are they?", "What do they use today and why?", "What
difficulties do they face?", "Shared difficulties". After the table — justification
of the segments with a prioritization calculation (capacity/CAC/competition) and an inference.

**2.2 Barriers at every stage of the journey** — a table "Journey stage → Barrier today →
What the product does" (stages: acquisition → choice → payment/usage →
post-payment experience). Below — a table/blocks **"What holds people back from starting or renewing?"**
per segment: factor → what removes it. Close with a conclusion: segmentation by
entry barrier; the tier ladder serves all barriers.

### FAQ-3: Strategic initiatives. Briefly justify each one.

Intro: which options the direction was chosen from (one paragraph referencing the options
analysis and the red team) and why. Then **3–4 driver initiatives**, each with a
numbered subheading and an explicit construction: "**The first driver** — …", "**The second
driver** — …", then "Key directions" (top-level tactic bullets),
then unit economics / effect calculation (formula → substitution → result).
Close with a conclusion: the initiatives close the FAQ-2 barriers and build on existing assets.

### FAQ-4: Tactics. Detail each initiative down to concrete tactics.

A matrix-table: columns **"Strategic initiative | Focus | Needs and
expectations of the user | Solutions (tactics)"**. 2–4 rows per initiative:
focus → needs (of the buyer/user and, where relevant, of the executor) →
concrete solutions. Tactics must be executable (what exactly is being built/changed), not
slogans.

### FAQ-5: High-level implementation plan

- Expected distribution of the initiatives' contribution to the overall result — **in percentages**
  (summing to 100%), each with a justification "why this weight";
- Order of implementation of tactics: high → medium → base priority;
- **Timing against the market's seasons** (e.g., the January hiring peak): the launch must
  meet the season with accumulated statistics;
- Parallel tracks (community/partnerships) — what runs outside the main line;
- A D### decision with a commitment, deadline, review date, and a stop trigger.

### FAQ-6: Success metrics. KPIs for evaluating the strategy's effectiveness.

KPIs in **two planes**:
1) **Business** — money and base: revenue/MRR by the deadline, paying users, conversion to payment,
   share of annual/local plans, share of the new wave, actual LTV/CAC;
2) **Product** — activation, time to first value, reduction in the number of actions
   (clicks), churn, CSAT/NPS.
Each KPI: baseline → target by the deadline → action threshold. Plus **counter-metrics** (one
per red-team hit) with alarm thresholds and a recorded action.

## Content rules

1. **The scheme of every meaningful block**: "Data — …" → "Grounds" (numbered,
   with tags) → "Calculation" (formula → substitution → result) → "Conclusion
   (inference)" — on a separate line, with the words "therefore / this means".
2. **Provenance tags** on every number: C###/S### or an explicit assumption [C016]/[C020];
   synthetic material — hypotheses only, not proof of demand.
3. **Ranges instead of precision** where sources diverge; in calculations —
   the conservative bound.
4. **Red team** — across all options (FAQ-3 intro) and counter-metrics for each hit.
5. **Source footnotes** at the bottom of the document (as in the reference): a numbered list
   of S### + title + URL; in the text — tags.
6. **No screenshots or illustrations.** The committee's visual format is tables, formulas,
   calculations; the product is shown live or via a link.
7. **RU and EN** — a complete synchronous translation; three formats: MD (the evidence register),
   PDF (A4 print layout), DOCX (Word).

## Self-check checklist

- [ ] FAQ-1 contains 1.1 (trends as bullets) and 1.2 (competitor table with risks and ratings).
- [ ] FAQ-2 contains 2.1 (segments table with fixed rows) and 2.2 (barriers by stage + "what holds people back").
- [ ] FAQ-3 — driver initiatives with "The first/second driver —", key directions, and a calculation.
- [ ] FAQ-4 — the "Initiative | Focus | Needs | Solutions" matrix.
- [ ] FAQ-5 — contribution distribution in %, tactic priorities, season timing, D###.
- [ ] FAQ-6 — KPIs in two planes (business/product) with baseline, target, and action threshold.
- [ ] At the bottom — source footnotes S### + URL.
- [ ] No screenshots; no untagged numbers; RU and EN in sync.
- [ ] `pfs check --strict` — 0 errors, 0 warnings.
