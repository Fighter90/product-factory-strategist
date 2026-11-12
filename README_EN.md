# Product Factory Strategist

**[RU](README.md) · [EN](README_EN.md)**

An AI agent for a digital product director: from a vague request ("why is retention dropping", "who do we sell
the new service to", "what do we tell the audience") to a **verifiable** picture of the situation, substantively
distinct options, and aligned product and communication strategies. After the decision, the agent keeps its
grounds, tracks commitments, and revisits conclusions when new data arrives.

This is a repository folder: instructions, knowledge sets organized by category (strategy · economics · product ·
UX · data · platforms · Gen AI), 100 skills, 8 subagents, 6 hooks, and a dependency-free Python CLI/MCP toolset.
Works in Claude Code, Cursor, Codex, OpenCode, Windsurf, Copilot.

**Links:** [Docs site RU/EN](https://strategyproduct.ru) · [HELP (EN)](docs/HELP_EN.md) ·
[HELP (RU)](docs/HELP.md) · [Skills registry](docs/SKILLS.md) · [CHANGELOG](CHANGELOG.md) ·
[Release v1.0.0](https://github.com/Fighter90/product-factory-strategist/releases/tag/v1.0.0)

---

## Quick start (5 minutes)

## Installation

```bash
git clone https://github.com/Fighter90/product-factory-strategist.git
cd product-factory-strategist
./scripts/install.sh          # uv tool install -e . (or venv+symlink)
pfs --help
```

Details, PEP 668, updates, uninstall, testing and troubleshooting — [docs/INSTALL_EN.md](docs/INSTALL_EN.md).

```bash
git clone https://github.com/Fighter90/product-factory-strategist.git
cd product-factory-strategist
python3 -m tools.pfs doctor                    # environment check
python3 -m unittest discover -s tests          # 609 tests
# in Claude Code (run `claude` in the folder) write the task:
# "Our paid anti-spam service is losing subscribers. What do we do and what do we tell customers?"
```

The agent creates the project, runs question blocks, builds the research and shows progress as
`Step N/12 · …`. Say **"stop"** to pause, **"clarify: …"** to adjust, **"build the six-pager in two languages with an Excel model and a committee report"**, **"make the presentation"** for a deck from the six-pager. After a break, open a new
chat — state is restored automatically.

---

## Demo project: CVStart — full walkthrough

A live end-to-end run on a real task: **CVStart** — [cvstart.org](https://cvstart.org/)
([github.com/Fighter90/career-ops-ui](https://github.com/Fighter90/career-ops-ui)), an open (MIT) AI resume
builder and job-search tool: a scan of ~129 job boards, AI scoring 0.0–5.0, CV Studio, PDF/DOCX, cover letters,
a tracker, a job map; 100% local; 18 BYOK LLM providers; 19 languages; ~7,602 automated tests; no monetization yet.

- Task: "Build the commercial version of cvstart.org and a go-to-market strategy for the whole world."
  Comparison axis: paying subscribers and ARR; constraints: the MIT core stays free and open, a solo developer,
  keep the trust of the local/private mode.
- How the agent ran: 12 steps — brief → 10 sources (S001–S011) → research plan → discovery with 2 synthetic
  personas (honestly labeled, hypotheses only) → situation → 5 options + red team (15 objections + 5 hidden
  assumptions = 20 hits) → the director picked **B: hosted freemium SaaS** (Free BYOK / Pro $12 / Unlimited $29,
  opt-in cloud on top of the local MIT core, honest pricing without auto-renewals, locale waves
  EN → DE/ES/PT-BR → JA/ZH) → both strategies → 90-day validation plan (continue ≥40 paying / change 20–40 /
  stop <20 at activation <35%; counter-metrics: GitHub stars, GDPR complaints, NPS ≥30, free-tier inference
  ≤$200/mo) → review `check --strict` **100/100** → decision D001 (beta in 3 EN geos by 2026-12-15,
  review 2027-02-10) → monitoring.
- Evidence: 10 sources, 20 claims with types and grades A–D (12 facts, 4 hypotheses, 4 assumptions); market
  facts: resume builders $1.2–2.4B (aggregators disagree 2×), AI segment CAGR 13.1%, online recruiting $37.97B
  (2025), ATS at 98% of F500, 7 competitors at $8–40/mo with auto-renewals; unit economics [C016]: ARPU $29,
  CM $21.75, LTV ≈ $271.88, LTV/CAC ≈ 4.5, break-even ≈ 69 paying; synthetic funnel [S008] is a method,
  not a forecast. Synthetic material is registered with `origin=synthetic` — the tool refuses to record facts on it.

What to look at: `projects/демо/outputs/` (00_brief…07, REPORT.md, **SIX_PAGER_RU and SIX_PAGER_EN — each as
.md/.pdf/.docx**, attachments/*.xlsx — 4 workbooks, img/ screenshots), `projects/демо/interviews/synthetic/`. The six-pager follows the growth-strategy reference format: subsections 1.1/1.2 and 2.1/2.2, driver initiatives, a tactic matrix, KPIs in two planes, source footnotes; the draft is assembled by `pfs export --six-pager` (spec: `knowledge/templates/SIX_PAGER_PROMPT.md`)
(2 AI personas), `projects/демо/analysis/` (generators + funnel CSV). Product screenshots: `site/assets/`.
Full RU breakdown with a task-requirements mapping table — in
[README.md](README.md#демонстрационный-проект-cvstart--полный-разбор).

How to repeat:

```bash
python3 -m tools.pfs use демо                        # switch to the demo
python3 -m tools.pfs status                          # where we stopped (step: monitoring)
python3 -m tools.pfs next                            # what to decide now
python3 -m tools.pfs --project демо check --strict   # quality gate: 100/100
python3 -m tools.pfs new "Title" "Request verbatim"  # your own task
```

## How the agent works: 12 steps

At every step the agent **reads the mandatory knowledge cards** (printed by `pfs step`), passes a
**question block** (`pfs questions <step>` — at least 1–3 questions to you; skipping requires a log note),
and hits **quality gates**. Double Diamond phases: Discover (0–3) → Define (4–6) → Develop (7–9) →
Deliver (10–11).

```mermaid
flowchart TD
  Q["director's request"] --> R["route: scenario · cards · models"]
  R --> S0["0 intake: brief"] --> S1["1 sources"] --> S2["2 research"] --> S3["3 discovery: personas/JTBD"] --> S4["4 situation"] --> S5["5 options + red team"] --> S6{{"6 choice: HUMAN"}} --> S7["7 strategy"] --> S8["8 validation"] --> S9["9 review: check + rubric + six-pager"] --> S10{{"10 decision: HUMAN"}} --> S11["11 monitoring"]
  S6 -.->|"pfs questions"| QB["question blocks"]
  S9 --> DECK["six-pager + 4 Excel"]
  S11 -->|"new data"| REF["impact → supersede → rebase"]
```

| # | Step | What the agent does | Mandatory cards | Question block | Gate |
|---|---|---|---|---|---|
| 0 | intake | ≤3 questions, brief, assumptions | M-brief-hypotheses, M-customers, M-jtbd | intake-* | **human approves** |
| 1 | sources | Web/PDF/DOCX/XLSX/CSV → S###, dedup, protection | M-source-criticism, M-research-types | intake-constraints | allowed domains |
| 2 | research | Plan from decision-changing questions; calculations; interviews | M-research-types, M-quant-methods, M-ab-testing, M-sql-for-pm | discovery-jtbd | answered or gap named |
| 3 | discovery | Personas, JTBD, user alternatives | M-jtbd, M-audience-research, M-customers | discovery-segment | segment+personas fixed |
| 4 | situation | Known / unknown / contradictions | M-source-criticism, M-external-environment, M-competitors | situation-gaps | `pfs check` |
| 5 | options | ≥3 options + red team + falsifiers | M-goals-drivers-bets, M-risks, M-double-diamond, M-lean-canvas | options-criteria | check + red team |
| 6 | choice | Comparison and recommendation | M-decision-daci | choice-reversibility | **human decides** |
| 7 | strategy | Product + communication | M-usp, M-product-communication, M-monetization, M-unit-economics | strategy-promise | promises ↔ product |
| 8 | validation | Metric, baseline, duration, counter-metrics | M-ab-testing, M-success-metrics | validation-metric | 5 sections |
| 9 | review | check + rubric + six-pager with Excel | M-six-pager, M-source-criticism | — | rubric ≥ threshold |
| 10 | decision | Grounds, owners, commitments | M-decision-daci, M-model-validation | decision-commitments | **human approves** |
| 11 | monitoring | Deadlines, new data, revisions | M-loyalty-metrics | — | `pfs decision due` empty |

---

## Architecture

```mermaid
flowchart TB
  U["Product director"] -->|"request · answers to question blocks"| ENV
  subgraph ENV["LLM environment (Claude Code / Cursor / OpenCode / Codex…)"]
    AG["AGENTS.md — 12-step process, rules"] --> SK["skills: 100<br/>(base + product-skills 27 + integrations: sdd · deck · premortem)"]
    AG --> SUB["subagents: 8<br/>researcher · red-team · evidence-auditor · synthetic-respondent · data-analyst · ux-analyst · comms-strategist · router"]
    AG --> HK["hooks: 6<br/>SessionStart · PreWeb-domains · PreGuard-registries · PostTool-log · Stop-cost (+ shared module)"]
  end
  ENV -->|"CLI: pfs … · MCP: pfs-strategist"| TOOLS
  subgraph TOOLS["tools/pfs — deterministic guarantees (stdlib only)"]
    P["projects/&lt;slug&gt;<br/>state · outputs · calcs.json"] --> S["sources S###<br/>dedup · SSRF · injection scan"]
    S --> CL["claims C###<br/>fact/hypothesis/forecast/assumption/inference · grade A–D"]
    CL --> CH["check --strict<br/>quality gate"]
    CAL["calc → 4 Excel workbooks<br/>Input sheet + formulas"] --> EX["export<br/>REPORT.md · SIX_PAGER.md (FAQ-1…6)"]
    CH --> EX
    DEC["decisions D###<br/>grounds · commitments"] --> MON["decision due<br/>what to decide now"]
  end
  KB["knowledge/ — 89 cards across categories (RU) + 89 EN mirrors (full bilingual base) (methods_en/) + INDEX_EN.md<br/>+ frameworks: Double Diamond · Lean Canvas · RICE/ICE/WSJF · AARRR/HEART/Kano"]
  ENV -->|kb search / route| KB
  FEY["Feynman (feynman.is)<br/>deepresearch · lit · compare"] -->|"provenance → primary sources → S###"| S
  EX --> ATT["outputs/attachments/*.xlsx<br/>recalculated on open"]
```

Four layers you never mix: **instructions** (AGENTS.md, skills) ≠ **knowledge** (knowledge/) ≠
**project materials** (projects/`<slug>`) ≠ **state** (state.json, *.jsonl). A previous agent answer never
becomes a fact: it is stored as `inference` with grounds; when a ground is retracted, `pfs check` flags
every place referencing it.

---

## Skills: structure and how to invoke

```mermaid
flowchart TB
  SK["100 skills"] --> B["Base 13: process steps<br/>intake · research · situation · options · strategy · validation · decision-support · data-analysis · interviews · ux-review · six-pager · deep-research · strategist"]
  SK --> P["Product-skills 27: method procedures<br/>market-sizing · unit-economics · traction-modeling · solution-design · problem-design · …"]
  SK --> L["Personal library 57<br/>design · marketing · science · docs/media · meta"]
  SK --> INT["Integrations 3<br/>premortem · sdd · deck"]
  B & P & L & INT --> INV["Invocation: automatic by triggers · explicit 'use skill X' · via process steps"]
```

100 skills in `.claude/skills/`, four groups:

- **base 13** — process steps (one per workflow stage: intake → sources → research → … → monitoring).
- **product-skills 27** — method procedures (problem and solution design, traction modeling, unit economics,
  market sizing, interviews, UX review, …).
- **personal library 57** — domain expertise:
  - Design: refero-design, design-ui, claudable-landing, frontend-design, make-interfaces-feel-better,
    emil-design-eng, web-design-guidelines.
  - Marketing: ad-creative, ads, ai-seo, analytics, churn-prevention, co-marketing, competitors,
    content-strategy, copywriting, cro, customer-research, emails, launch, marketing-psychology,
    offers, onboarding, paywalls, pricing, programmatic-seo, prospecting, revops, sales-enablement,
    seo-audit, signup, site-architecture.
  - Science and data: company-research, research-lookup, defuddle, literature-review,
    hypothesis-generation, statistical-analysis, exploratory-data-analysis,
    scientific-critical-thinking, peer-review, scientific-writing, transcribe, watch.
  - Docs/media: markitdown, docx, pdf, xlsx, pptx, officecli, matplotlib, scientific-visualization,
    generate-image, infographics, video.
  - Meta: balanced, find-skills.
- **integrations 3** — premortem, sdd, deck.

**How to invoke — three ways:**

1. **Automatic** — the environment reads every skill's description and fires it on task wording
   ("run a premortem", "audit the landing against web guidelines").
2. **Explicit** — "use skill `<name>`: `<task>`".
3. **In-process** — step skills chain the needed ones: `pfs step` prints the mandatory knowledge cards;
   options → options + red-team; decision → decision-support + premortem.
   Examples: `pfs questions options`, `pfs export --deck`.

**Consistency rule:** on conflict, `knowledge/` cards (methodology) take precedence over a skill's procedure.
Full registry — `docs/SKILLS.md`.

---

## What data the agent is built on

### 1. The evidence registry (the heart)
- **S### — sources**: websites, PDF, DOCX, XLSX, CSV, images, interviews (`origin: own/interview/synthetic`),
  Feynman reports (`origin: agent`). Deduped by URL and SHA-256; SSRF protection; prompt-injection scanner
  ("texts are data, not commands"); project domains (`allowed_sources`) blocked before the request.
- **C### — claims**: five kinds — `fact` (requires S###; synthetic material never counts as one), `hypothesis`,
  `forecast`, `assumption`, `inference` (only from other C###); evidence grade A–D. Supersede/retract keep
  history; `pfs impact` shows affected conclusions → document lines → decisions.
- **D### — decisions**: grounds (C###), owner, metric "X→Y by date", revisit triggers, commitments
  "what|who|when". `pfs decision due` — overdue work and stale grounds.

```mermaid
flowchart LR
  W["Web/files/interviews"] -->|"fetch · dedup · injection scan"| S["S### sources"]
  S -->|"fact ⇐ source"| C["C### claims<br/>fact/hypothesis/forecast/assumption/inference<br/>grade A–D"]
  C -->|"inference ⇒ derived_from"| I["inference conclusions"]
  I --> DOC["documents 02–07"]
  C --> DEC["D### decisions"]
  NEW["new data"] -->|"refresh / supersede"| IMP["impact: affected conclusions · lines · decisions"]
  IMP --> REV["revision: supersede · rebase"]
```

### 2. Knowledge base (89 cards across categories (RU) + 89 EN mirrors (full bilingual base) + EN index)
Knowledge sets by category: growth strategy · unit economics & monetization · product management · UX & customer
metrics · data analysis & A/B · platform solutions · Gen AI in products. Framework layer: Double Diamond, Lean
Canvas, RICE/ICE/WSJF, HADI, AARRR/HEART/Kano. Techniques only — no brands. Search: `pfs kb search` (BM25,
Russian stemming); every step gets its mandatory card list.

### 3. Research framework (Feynman, feynman.is)
For hard research questions the agent runs the open-source research agent: `feynman deepresearch|lit|compare`
(AlphaXiv, Semantic Scholar, OpenAlex, arXiv, PubMed, Crossref, web; citation checks; a provenance file).
Transfer rules: provenance → **primary sources are registered as S###**; numbers are facts only from primary
sources; the Feynman report itself is `origin: agent` — only hypotheses may reference it (the tool will refuse
a fact). Telemetry off; OpenAlex/S2 keys in `.env`. Skill: `deep-research`. Plus 27 product-skills procedures
and question blocks in `config/question_blocks.json`.

### 4. Numbers come from calculations, not "from the head"
`pfs calc` builds 4 formula-driven Excel workbooks (unit economics with LTV/CAC/payback + sensitivity,
a 12-month growth model, cohort retention, PAM→TAM→SAM→SOM + PESTEL): the Input sheet holds editable
parameters from `calcs.json` (every value traced to a C###), cached values for preview, recalculation on open.
The `calcs.json` skeleton is generated by `pfs calc scaffold` from the 02/04/06/07 documents: found numbers
carry their C/S tag in `_notes`, misses become null + a hint in `_hints` (manual filling — only the null fields).

---

## Six-pager for the committee

`pfs export --six-pager` assembles the report in the reference structure: FAQ-1 state · FAQ-2 personas ·
FAQ-3 initiatives & objections · FAQ-4 tactics · FAQ-5 plan & validation · FAQ-6 metrics · Excel attachments
table. Numbers in the text match the workbooks; full evidence lives in REPORT.md (appendices A–E: claims,
sources, decisions, cost, Excel). Presentation: the `deck` skill (officecli → PPTX, HTML fallback,
Higgsfield visuals, Lovable web version).

---

## CLI (full list)

| Command | Purpose |
|---|---|
| `pfs new / list / use / status [--brief]` | projects and state |
| `pfs route "<request>" [--override --economy --json]` | scenario, cards, model plan |
| `pfs questions <step\|block>` | question blocks for strategy tuning |
| `pfs next` | "what to decide now": step, commitments, stale sources with a refresh command, reviews |
| `pfs step <step> in_progress\|done [--note --next]` | step mark + mandatory cards |
| `pfs ask / answer / question` | human checkpoints |
| `pfs source add/list/show [--text-file --url --origin --force]` | sources S### |
| `pfs source refresh S###` | refresh a web source: sha256 delta, backup, impact |
| `pfs claim add/list/supersede/retract/rebase/retag [--kind --source --from --grade]` | claims C###; `retag --from C003 --to C059` renumbers claim tags across all outputs in one command |
| `pfs check [--strict --json] · pfs impact C###` | quality and change impact |
| `pfs review lock` | lock the review verdict; registry edits after the lock → "verdict stale" in check/status/export |
| `pfs decision add/list/due/done/status/rebase` | decisions and monitoring |
| `pfs data profile/cohort <csv> [--save]` | table profile, cohorts |
| `pfs data funnel/stats <csv>` | funnel over events/columns; stats with 95% CI |
| `pfs interview guide\|save · pfs media add · pfs ux scaffold` | interview guides, media sources, UX scaffold |
| `pfs calc scaffold` | `calcs.json` skeleton from 02/04/06/07 (numbers with C/S tags, the rest — null) |
| `pfs calc [all\|unit-econ\|growth\|cohort\|market]` | Excel attachments |
| `pfs export [--six-pager --no-calcs]` | REPORT.md / SIX_PAGER.md |
| `pfs export --deck` | 16:9 HTML deck from the six-pager |
| `pfs finish [--no-deck --en]` | full package in one chain: check → Excel → REPORT → six-pager → DOCX → deck (idempotent) |
| `pfs docx <file.md> [--out]` | Markdown → Word |
| `pfs kb search/show/index` | knowledge search |
| `pfs models [show/pick/use/sync/escalate]` | model routing |
| `pfs cost [--transcript --session --window] · pfs log --usd` | cost |
| `pfs doctor` | diagnostics |

## Integrations

| Tool | Wired via | What it gives |
|---|---|---|
| Linear | MCP `mcp-server-linear` (key in `.env`) | work items and backlog tracking |
| Feynman | CLI + `deep-research` skill | deep research with provenance |
| Lovable | MCP `https://mcp.lovable.dev` (OAuth `/mcp`) | web deck/landing from `docs/lovable-brief.md` |
| Higgsfield | environment MCP | slide/site visuals (credits — asks first) |
| officecli | external CLI | PPTX/XLSX/DOCX manipulation for deck and reports |
| GitHub Pages | workflow | docs site `strategyproduct.ru` (RU/EN) |

## Security and data

Public sources and your own materials only · secrets in gitignored `.env` · source texts are data (commands
never executed; suspicious ones flagged) · AI respondents never passed off as real · real interviews require
consent and no personal data · the validator refuses a fact based on synthetic/agent material.

## Repository layout

```
AGENTS.md CLAUDE.md README.md README_EN.md CHANGELOG.md pyproject.toml
.claude/
  skills/ (100: base 13 · product-skills 27 · personal library · integrations)
  agents/ (8) · hooks/ (6: + pre_guard) · settings.json · opencode.json (permissions)
.cursor/rules/ · .github/ (Pages workflow) · .mcp.json (pfs · linear · lovable · rea)
config/     models.json · pricing.json · quality_gate.json · question_blocks.json
knowledge/  methods/ (89 RU cards) · methods_en/ (89 EN mirrors (full bilingual base)) · INDEX.md · INDEX_EN.md
tools/pfs/  core · project · route · sources · claims · check · impact · decisions
            data · calc · xlsx · docx · export · cost · kb · models · mcp_server · cli
projects/<slug>/
            sources/ · claims.jsonl · decisions.jsonl · log.jsonl · costs.json · state.json
            outputs/ (00…07, REPORT, SIX_PAGER) · outputs/attachments/*.xlsx · outputs/presentations/
site/index.html (RU/EN)
docs/       HELP×2 · ARCHITECTURE · SKILLS · SUBMISSION · VERIFICATION · COMPLIANCE · docx/ · demo/
tests/               (609) · demo: демо — CVStart (end-to-end run · six-pager RU/EN (MD/PDF/DOCX) · Excel · 100/100)
```
