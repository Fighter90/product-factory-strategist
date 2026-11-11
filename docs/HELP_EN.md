# Help: How to use the Product Factory Strategist agent

**[RU](HELP.md) · [EN](HELP_EN.md)**

> Full user guide.

---

## 1. What it is and how it is organized

The agent is not a program and not a bot — it is a **repository folder** that you open in an LLM environment
(Claude Code, Cursor, Codex, OpenCode, Windsurf, Copilot). The environment reads `AGENTS.md` (rules and process),
`knowledge/` (knowledge sets by category: strategy · economics · product · UX · data · platforms · Gen AI;
techniques only — no brands), while the tool `pfs` keeps
the research "bookkeeping": sources, claims, checks, decisions, cost.

Four layers to distinguish:

| Layer | Where | What is inside |
|---|---|---|
| Rules and process | `AGENTS.md` | 12-step process, evidence rules, command cheat sheet |
| Methods | `knowledge/methods/` | 89 method cards (RU) + 89 EN mirrors (full bilingual base): unit economics, A/B testing, platforms, GenAI, etc. |
| Task materials | `projects/<slug>/` | sources, claim registry, documents, Excel models, state |
| Tools | `python3 -m tools.pfs …` | CLI and MCP server with guarantees: no fact without a source |

The agent drives the process and calls `pfs` itself. Your job: answer questions and decide at three checkpoints —
**brief** (step 0), **option choice** (step 6), **decision approval** (step 10).

---

## 2. Requirements and setup

You need: Python 3.9+ (no packages), git, any environment above. Optional: `pdftotext` (poppler) or
`pip install pypdf` for PDF sources.

```bash
git clone https://github.com/Fighter90/product-factory-strategist.git
cd product-factory-strategist
python3 -m tools.pfs doctor                    # environment check
python3 -m unittest discover -s tests          # self-check (411 tests)
```

`doctor` reports install mode (editable/venv/source), package version, `pfs` path (which), PATH health, projects dir location, Python version, pdftotext/pypdf availability, number of knowledge cards, active project.
CLI needs no API keys. Keys (e.g., Linear API) go into `.env` — it is git-ignored.

---

## 3. Quick start: your first task

1. Open the repo folder in your environment (in Claude Code: run `claude` inside the folder).
2. Write the task in plain language, like a product director would:

   > Our paid anti-spam service is losing subscribers. What do we do with the product, and what do we tell customers?

3. The agent will: create a project, ask 1–3 clarifying questions, build a research plan, collect sources,
   propose options and attack them with a red team, synthesize strategies, and show progress as:

   `Step 2/12 · research · sources S001–S009 collected · next: discovery`

4. At any moment you can say: **"stop"** — pause; **"clarify: …"** — adjust the task; **"redo section X"** —
   rework only the affected part; **"build the six-pager"** — get the committee report.
5. Break / new chat: open a new chat in the same folder — the SessionStart hook feeds the agent its state
   (`pfs status` does the same manually). Finished steps are never repeated.

---

## 4. The 12-step process

| # | Step | What happens | Your role |
|---|---|---|---|
| 0 | intake | Clarify question, goal, constraints, data → `00_brief.md` | **approve the brief** |
| 1 | sources | Register your files and public sources → `sources/S###.md` | provide materials |
| 2 | research | Plan from decision-changing questions; search; calculations; interviews | answer questions |
| 3 | discovery | Personas, JTBD, user alternatives → "Segments" section in 02 | answer discovery block |
| 4 | situation | Known/unknown, contradictions → `02_situation.md` | — |
| 5 | options | ≥3 distinct options + objections (red team) → `03_options.md` | — |
| 6 | choice | Comparison and recommendation | **you pick** |
| 7 | strategy | Product + communication strategies → `04/05_*.md` | — |
| 8 | validation | Test plan: metric, baseline, duration, counter-metrics → `06_validation_plan.md` | — |
| 9 | review | `pfs check` + rubric review → `07_quality_review.md`; lock the verdict: `pfs review lock` | — |
| 10 | decision | Grounds, owners, metrics, commitments → `decisions.jsonl` | **you approve** |
| 11 | monitoring | Deadlines, new data, revision of affected conclusions | receive reminders |

After step 9 (review) you can build the **six-pager with Excel attachments** (section 7) — a committee-ready report
in the FAQ-1…FAQ-6 growth-strategy reference structure (detailed format spec — knowledge/templates/SIX_PAGER_PROMPT.md).

---

## 5. All `pfs` commands

Full list: `python3 -m tools.pfs --help`. The agent runs most of this itself — the commands are here to check
state or act manually.

### Projects
```bash
pfs new "Title" "Request verbatim"     # create a project
pfs list                               # list projects
pfs use <slug>                         # make a project active
pfs status [--brief]                   # where we stopped, what's next, cost
```
The active project is stored in `projects/.active`: switch with `pfs use <slug>` before working on another
project — no need to export environment variables (the env override exists for tests only, via `PFS_PROJECTS_DIR`).
File paths in `source add`, `docx` and `media add` resolve first against the project directory
(`projects/<slug>/…`), falling back to the current directory; the resolved path is printed in the output.

### Steps and questions
```bash
pfs next                                # "what to decide now": current step, human checkpoint,
                                        # overdue commitments, grounds sources unchecked for 180+ days
                                        # (with a ready `pfs source refresh S###` command), reviews due
                                        # (past and within 14 days), open questions;
                                        # after review without SIX_PAGER.md — committee package
                                        # build first (calc scaffold → calc all → export --six-pager)
pfs step <step> in_progress|done --note "…" --next "…"
pfs ask "Question?" --options "A,B,C"  # pause: agent waits for your answer
pfs answer "Option B"
pfs question "Open question" [--close]
pfs questions <step|block>             # question blocks per step for strategy tuning (config/question_blocks.json); use `pfs ask` to pose to the director
```

### Sources (S###)
```bash
pfs source add https://example.com/report            # web page: fetched, cleaned, deduped by URL/SHA-256
pfs source add ~/Downloads/report.pdf                # PDF/DOCX/XLSX/CSV/image
pfs source add sources/raw/report.md                 # relative path: project directory first
                                                     # (projects/<slug>/…), then cwd; resolved path is printed
pfs source add --text-file doc.md --url <url> --title "…"   # if a site blocks automated fetching
pfs source fetch <url> --title "…"                   # unreachable URL (403/SSL/JS/timeout) in one call:
                                                     # direct request → r.jina.ai → web.archive.org;
                                                     # origin: public on direct success, excerpt on fallback
pfs source add interview.md --origin interview       # your interview (no personal data)
pfs source add transcript.md --origin synthetic      # AI respondent: hypotheses only
pfs source list | pfs source show S003
pfs source refresh S003                 # refresh a web source: sha256 delta → old version backed up
                                        # to raw/<S###>_old_<sha8>.txt → impact on claims built on it
```
Rules: project domains (`project.json → allowed_sources`) are checked before the request; secret files
(`.ssh`, keys, `.env`) are rejected; instruction-like phrases in texts are flagged and never executed.

### Claims (C###) — the heart of the agent
```bash
pfs claim add "Market is 40 B RUB" --kind fact --source S002 --grade B
pfs claim add "People will pay for family protection" --kind hypothesis --source S005
pfs claim add "Therefore focus on families" --kind inference --from C003,C010
pfs claim add-batch claims.jsonl        # register a batch from JSONL (text/kind/source/grade/quote/from):
                                        # one line = one claim; an invalid line cancels the whole
                                        # batch; duplicates by text are skipped
pfs claim list [--kind fact] [--all]
pfs claim retract --id C005 --reason "methodology error"
pfs claim supersede "Market is 45 B RUB" --id C005 --reason "new report" [--source S009]
pfs claim rebase [--id C012]            # redirect conclusions to the replacements of their grounds
```
Kinds: `fact` (needs a source; synthetic material never counts as one), `hypothesis`, `forecast`,
`assumption`, `inference` (only from other C###). Evidence strength: `--grade A…D`.

### Checks and impact
```bash
pfs check [--strict] [--json]   # quality gate: untagged numbers, dead links, document structure
                                # numeric cross-check (PRO-26): numbers of active claims vs numbers in the
                                # titles of their sources, and quote numbers vs sources/S###.md text —
                                # a mismatch ("claim says 19, title says 17") adds a warning with the C###/S### pair
pfs review lock                 # lock the review verdict: registry snapshot (sha256 of claims/sources and docs 00–07)
                                # into outputs/.review_state.json; registry edits after the lock add a
                                # "review verdict stale — the registry changed after the review; re-run evidence-auditor"
                                # warning to check/status/export; re-lock after the re-review
pfs gap list                    # research gaps from 02 "What we don't know": numbers and status (open/partial/closed)
pfs gap close 3 --claim C069 --note "how it was closed"
                                # mark a gap closed SYNCHRONOUSLY: the 02 row + the 01 item / question status;
                                # pfs check warns if 02 says "closed" but the 01 line still says "open"
pfs impact C005                 # what a change affects: conclusions → document lines → decisions
```

### Decisions (D###) and monitoring
```bash
pfs decision add --title "…" --decision "…" --owner "CPO" --grounds C001,C007 \
  --metric "M1 retention: 38% -> 45% @2027-01-01" --review 2027-01-01 \
  --trigger "M1 < 40% for two months" --commit "Launch pilot|PM|2026-12-01"
pfs decision due          # what to decide now: overdue commitments, stale grounds, sources
                          # unchecked for 180+ days — with a ready `pfs source refresh S###` command
pfs decision done --id D001 --commitment K1
pfs decision list | status | rebase
```

### Data
```bash
pfs data profile events.csv [--sheet Sheet1] --save profile      # table profile: types, gaps, dupes, periods
pfs data cohort events.csv --user user_id --date dt --save cohorts   # cohort retention
pfs data funnel events.csv --steps visit,signup,pay --user user_id   # funnel over an event log
                                                  # or per-step flag columns; --date validates step order
pfs data stats events.csv --col revenue [--group segment]       # descriptive stats for a column
                                                  # (n, mean, median, percentiles, 95% CI), optionally per group
```

### Interviews, media and UX
```bash
pfs interview guide --persona "Parent of 7–12" [--topic "…"]   # interview question outline in interviews/
pfs interview save transcript.md --persona "…" --title "…"     # AI-respondent transcript/summary
                                        # → source with origin synthetic (hypotheses only)
pfs media add screenshot.png --desc "what is visible"          # media within declared limits: the file is copied
                                        # to sources/raw and its description — "only what is visible/audible" —
                                        # becomes a source; interpretations are separate claims
                                        # (path: project directory → cwd)
pfs ux scaffold S003 --focus "onboarding"                      # UX scaffold of 10 heuristics in analysis/ux_<S###>.md
                                        # with the rule "conclusions only from the source material"
```

### Excel models (six-pager attachments)
```bash
pfs calc scaffold                      # calcs.json skeleton from 02/04/06/07: numbers carry
                                       # C/S tags in _notes; misses become null + _hints
pfs calc all                          # 4 workbooks → projects/<slug>/outputs/attachments/
pfs calc unit-econ | growth | cohort | market
```
Each workbook: an **Input** sheet (editable parameters) + calculation sheets **built on formulas** — Excel
recalculates on open. Parameters come from `projects/<slug>/calcs.json`; the skeleton is generated
by `pfs calc scaffold` (manual filling — only the null fields):

```json
{
  "unit_econ": {"arpu": 199, "vc_share": 0.2, "cac": 600, "churn_month": 0.08,
                "note": "values from C010, C014; replace modeled ones — see open questions"},
  "growth": {"mau_start": 100000, "mau_growth_month": 0.05, "conv_order": 0.02,
             "orders_per_active": 1.5, "aov": 3500, "take_rate": 0.08, "margin": 0.6},
  "cohort": {"sizes": [5000, 6000], "retention": [1.0, 0.55, 0.42]},
  "market": {"pam": 120000000000, "tam_share": 0.6, "sam_share": 0.3, "som_share": 0.05}
}
```
Anything missing falls back to the example in `tools/pfs/calc.py: DEFAULTS` marked "EXAMPLE"
(null fields from the skeleton too). Number ranges ("60–70%") are taken as the midpoint by the
skeleton; a null inside lists (sizes/retention) is filled from the example at its own position,
while a null in the tail beyond the example truncates the list right there — positions never
shift, cohort 8's size never becomes cohort 7's. Trace every value to C###/S###: the source lives
in the registry, the link goes into `note`; numbers found by the scaffold carry their tag in the
section's `_notes`, and a re-run preserves `_notes`/`_hints` of values already set.

### Reports
```bash
pfs finish                      # full package in one chain: pfs check → calc all → REPORT →
                                # SIX_PAGER → registry snapshot → DOCX → deck → "built + stale" summary;
                                # any check error stops the build (same as pfs check --strict); re-running is idempotent
pfs finish --no-deck            # same without the HTML deck
pfs finish --en                 # + EN draft of the six-pager: SIX_PAGER_EN.md + DOCX (tool skeleton in
                                # English; document sections are marked "[RU source — translate]"; check
                                # compares RU↔EN tags and warns when the EN draft lags behind RU)
pfs export                     # REPORT.md: all documents + appendices A–E
                               # registry snapshot in outputs/.export_state.json; if claims/sources/Excel changed after the build — ⚠ on `pfs status` and on the next export
pfs export --six-pager         # SIX_PAGER.md (FAQ-1…6) + Excel rebuild
pfs export --six-pager --en    # + EN skeleton: SIX_PAGER_EN.md — same structure/numbers/tags, English skeleton,
                               # document sections marked "[RU source — translate]" (translation is the agent's job)
pfs export --six-pager --no-calcs   # rebuild text without regenerating workbooks
pfs export --deck                   # 16:9 HTML deck from SIX_PAGER.md
pfs docx <file.md> [--out]          # Markdown → Word, dependency-free (path: project directory → cwd; docx versions of HELP/README live in docs/docx/)
```
Six-pager structure: FAQ-1 market & competitors · FAQ-2 segments & personas · FAQ-3 initiatives & objections ·
FAQ-4 tactics · FAQ-5 plan & validation · FAQ-6 success metrics · Excel attachments table.
Full evidence — REPORT.md.

### Knowledge base
```bash
pfs kb search "cohort retention analysis"      # BM25 search over method cards
pfs kb show M-unit-economics                   # show a card
pfs kb index                                   # rebuild INDEX.md, validate links
```

### Models and cost
```bash
pfs models                     # which model solves which task (config/models.json)
pfs models pick red_team       # plan for a task
pfs models use cursor-mixed    # profile for another environment
pfs models sync                # write models into Claude Code subagents
pfs cost [--transcript session.jsonl] [--session ses_e43_session.json] [--window]   # cost from Claude Code transcripts or an OpenCode session (session.json; plan providers like zai-coding-plan get $0 tokens marked «plan»); --session <file> without --transcript is an alias with auto-detection in the project root (*_session.json / *.jsonl; no value — the newest one; registry claims/sources/decisions/log.jsonl are not treated as transcripts); elsewhere:
pfs log "Manual edit" --usd 0.8 --human-minutes 15
```

### Diagnostics
```bash
pfs doctor      # environment + source registry integrity: duplicate IDs/URLs, record without file, orphan file (PRO-34)
```

---

## 6. Background work (subagents)

The agent offloads the main dialogue to subagents: `researcher` (reading long sources), `red-team`
(attacking options), `evidence-auditor` (rubric review), `data-analyst` (calculations, including `pfs calc`),
`synthetic-respondent` (AI respondents — hypotheses only), `comms-strategist`, `ux-analyst`, `router`.
Six-pager Excel models are built **in the background**: while `pfs calc` runs, you can keep chatting.
The model per task is selected via `config/models.json` (cheap models for classification and extraction,
strong ones for synthesis and strategy); escalation — `pfs models escalate`.

Deep research — Feynman (feynman.is, skill `deep-research`): `feynman deepresearch/lit/compare` with a provenance
file. Transfer rules: provenance → primary sources registered as S###; numbers are facts only from primary sources;
the report itself is origin agent — hypotheses only. Telemetry: `FEYNMAN_TELEMETRY=off`;
`OPENALEX`/`SEMANTIC_SCHOLAR_API_KEY` in `.env`.

---

## Skills: structure and invocation

Alongside the process the environment loads **skills** — packaged instruction sets (100 in total, in three
groups plus integrations):

- **Base (13)** — one per process step: `intake`, `research`, `situation`, `options`, `strategy`,
  `validation-plan`, `decision-support`, `six-pager`, `deck`, etc.
- **Product-skills (27)** — domain packs around the process: segments, JTBD, unit economics, growth, risks.
- **Personal library (57)** — domain expertise:
  - **Design** — `design-ui`, `refero-design`, `frontend-design`, `claudable-landing`, `make-interfaces-feel-better`,
    `emil-design-eng`, `web-design-guidelines`;
  - **Marketing & comms** — `ads`, `ad-creative`, `seo-audit`, `ai-seo`, `cro`, `pricing`, `offers`, `emails`,
    `launch`, `content-strategy`, `competitors`, `analytics`, `programmatic-seo`, `customer-research`,
    `marketing-psychology`, `prospecting`…;
  - **Research & science** — `research-lookup`, `literature-review`, `scientific-writing`,
    `scientific-critical-thinking`, `peer-review`, `hypothesis-generation`, `defuddle`;
  - **Data** — `statistical-analysis`, `exploratory-data-analysis`, `matplotlib`, `scientific-visualization`;
  - **Docs/media** — `pdf`, `docx`, `pptx`, `xlsx`, `markitdown`, `officecli`, `generate-image`, `video`,
    `infographics`, `watch`, `transcribe`;
  - **Thinking modes/meta** — `balanced`, `find-skills`.
- **Integrations** — cross-process behaviors: `premortem` (failure pre-mortem), `sdd` (development
  discipline), `deck` (six-pager presentation).

How skills are invoked:

- **Automatically** — by description trigger: the task matches, the skill loads.
- **Explicitly** — say `use skill <name>: <task>` (example: `use skill design-ui: build the landing`).
- **In-process, by step** — `pfs step` prints the step's knowledge cards; at `options` the `red-team`
  subagent attacks each variant; at `decision` — `decision-support` plus `premortem` AFTER the D###
  draft and BEFORE your approval; at `research` — `deep-research` for literature reviews.

Examples of requests: "run a premortem on D001", "use skill design-ui: build the landing".

Precedence rule: on conflict, the `knowledge/` methodology wins over a skill's own procedure.
Full registry of skills — [`SKILLS.md`](SKILLS.md).

---

## 7. Six-pager in 5 steps (scenario)

1. Wait until documents 02/03/04/06 exist (steps situation…validation).
2. Tell the agent "build the six-pager" — it fills `calcs.json` from the claim registry
   (every value tied to a C###), runs calculations in a background subagent, and assembles the report.
3. You get: `outputs/SIX_PAGER.md` + `outputs/attachments/*.xlsx` (4 workbooks).
4. Open Excel: the Input sheet — replace assumptions with actual figures; formulas recalculate.
5. Numbers in text and Excel must match: after editing `calcs.json`, rerun `pfs calc all` and `pfs export --six-pager`.

---

## 8. Hooks and automation

| Event | What happens automatically |
|---|---|
| Chat start | feeds the agent project state and "what to decide now" |
| WebFetch | blocks domains outside project `allowed_sources` **before** the request |
| After tools | writes the log, scans web answers for instruction-like phrases, auto-checks edited documents |
| Answer end | counts session cost (idempotent) |

Hooks never crash the session: errors go to `.claude/hooks/hook_errors.log`.

### End-to-end QA run (PRO-64)

To check that "the agent handles new tasks", run the whole 12-step chain on a fresh clone:

```bash
scripts/e2e_opencode.sh en qa/tasks/antispam-en.md    # 3 tasks × ru/en in qa/tasks/
# in OpenCode the same: the /pfs-e2e command — ru | en | all
```

The script does everything itself: a fresh clone into a temp directory → `opencode run --auto
--format json` in autopilot mode (the agent answers its own `pfs ask` questions, works until
`pfs finish`, no "continue" nudges) → log parsing → report `qa/E2E-<date>-<task>-<lang>.md`: steps,
tool calls, errors, tokens and cost, time, `pfs check --strict` and six-pager build results,
number of stops, reply language consistency ("Язык реплик" row with ⚠️ when a noticeable share
of the agent's replies is not in the run language). A run takes 20–40 minutes.
Comparison with plain chat and sample-size caveats: `docs/demo/comparison.md`.

---

## 9. Revising after new data

1. Add the source: `pfs source add <url|file>`.
2. If it changes a claim: `pfs claim supersede "…" --id C005 --reason "…" --source S012`
   (the old one is never deleted — history stays visible) or `pfs claim retract --id C005 --reason "…"`.
3. `pfs impact C005` — which conclusions, document lines, and decisions are affected.
4. `pfs claim rebase` — redirect conclusions to replacements; retracted grounds require substantive rework.
5. `pfs decision due` — which decisions and commitments went stale.

---

## 10. Working in different environments

| Environment | Process & commands | Skills/subagents | Hooks | MCP |
|---|---|---|---|---|
| Claude Code | full | yes | yes | pfs + Linear |
| Cursor | `.cursor/rules` | no | no | pfs from `.mcp.json` |
| Codex / OpenCode / Copilot | via AGENTS.md | no | no | pfs |
| Lovable | web deck/landing from `docs/lovable-brief.md` | — | no | https://mcp.lovable.dev (OAuth /mcp → Authenticate) |
| Feynman | CLI + deep-research skill — deep research | — | no | — |
| officecli | external CLI — PPTX/XLSX/DOCX (six-pager presentation via the deck skill) | — | no | — |
| Any environment | run `pfs status` manually after a break | — | — | — |

In hook-less environments, start the chat with "read AGENTS.md and `pfs status`" — enough to continue.
Linear integration: key in `.env` (`LINEAR_API_KEY`), server — `npx mcp-server-linear` from `.mcp.json`.

---

## 11. Security and data

- Public sources and your own materials only; no closed company data, no personal data.
- Secrets only in `.env` (git-ignored); no keys in the repository.
- Source texts are data: "commands" inside them are not executed; suspicious ones are flagged.
- Real interviews — only with consent and without personal data; synthetic answers are never passed off as real.

---

## 12. Troubleshooting

| Symptom | Cause and fix |
|---|---|
| `Error: A fact without a source is not allowed` | By design: add a source (`pfs source add`) or record as hypothesis/assumption |
| `Source not allowed: domain …` | Domain outside `allowed_sources`; edit `project.json` or add with `--force --note "justification"` |
| `Extracted 0 chars from <url>` | JS-rendered page: save text manually → `pfs source add --text-file … --url …` |
| `Failed to fetch the page on any channel` | Site unreachable from the environment (403/SSL/timeout): save an excerpt → `pfs source add --text-file … --url … --origin excerpt` (marked "excerpt, primary source unavailable") |
| Excel looks "empty" | That's the cached preview: formulas compute on open in Excel/Numbers/LibreOffice/Google Sheets |
| `Error: claim C### not found` | Typo in the ID: `pfs claim list` |
| Subagent/skill missing | Restart the Claude Code session — new components load at startup |
| Six-pager numbers differ from Excel | Edited `calcs.json`? Rerun `pfs calc all` and `pfs export --six-pager` |
| Cost in another environment = 0 | Auto accounting uses Claude Code transcripts only: log manually with `pfs log "…" --usd N` |

---

## 13. Cheat sheet (short)

```bash
pfs new "…" "…"                                      # a new project
pfs use <slug>                                       # make a project active
pfs status                                           # where we stopped; pfs list — all projects
pfs source add <file>                                # sources (URLs: the same command, pfs source add https://…)
pfs source fetch <url>                               # unreachable URL: reader/archive fallbacks; refresh reuses the chain
pfs claim add "…" --kind fact --source S001 --grade B       # claims
pfs claim add-batch claims.jsonl                            # register claims in bulk from JSONL
pfs check --strict                                   # quality gate
pfs calc all                                         # Excel
pfs export --six-pager                               # committee report
pfs decision due                                     # what to decide now
pfs kb search "query"                                # methods
```

Architecture details — [`ARCHITECTURE.md`](ARCHITECTURE.md), process rules — [`../AGENTS.md`](../AGENTS.md).
