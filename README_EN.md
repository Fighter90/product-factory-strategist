# Product Factory Strategist

An AI agent for a digital product director: from a vague request ("why is retention dropping", "who do we sell
the new service to", "what do we tell the audience") to a **verifiable** picture of the situation, several
substantively distinct options, and aligned product and communication strategies. After the decision is made,
the agent keeps its grounds, tracks commitments, and revisits conclusions when new data arrives.

This is not a program and not an autonomous bot — it is a **repository folder**: instructions, a method base
distilled from 7 product courses (techniques only, no brands), skills, subagents, hooks, and a small
dependency-free Python CLI. Open it in Claude Code, Cursor, Codex, OpenCode, Windsurf, Copilot.

> Demo project with a result: [`projects/demo-antispam/outputs/REPORT.md`](projects/demo-antispam/outputs/REPORT.md)
> Committee-ready report: `pfs export --six-pager` → `SIX_PAGER.md` + Excel models (FAQ-1…FAQ-6 structure).

Русская версия: [README.md](README.md) · Docs: [ARCHITECTURE.md](docs/ARCHITECTURE.md) ·
Help: [docs/HELP_EN.md](docs/HELP_EN.md) (RU: [docs/HELP.md](docs/HELP.md)) · Public site: `site/` (RU/EN)

---

## Quick start (5 minutes)

**You need:** Python 3.9+ (no packages), git, one of the environments: Claude Code (recommended), Cursor, Codex,
OpenCode, Windsurf, Copilot. Optional: `pdftotext` (poppler) or `pip install pypdf` for PDFs. Paid services:
only your chosen LLM environment subscription/API. No keys are stored in the repo and none are needed for the CLI.

```bash
git clone https://github.com/Fighter90/product-factory-strategist.git
cd product-factory-strategist
python3 -m tools.pfs doctor
python3 -m unittest discover -s tests
```

Then in Claude Code (run `claude` in the repo folder) just write the task:

> Our paid anti-spam service is losing subscribers. What do we do with the product, and what do we tell customers?

The agent creates the project, asks 1–3 important questions, runs the research, and shows progress as
`Step N/10 · …`. Stop it with "stop"; clarify with a follow-up message; fix results by editing files in
`outputs/` or asking it to redo a section. **After a break:** open a new chat — the SessionStart hook feeds
the agent the project state (or run `python3 -m tools.pfs status`).

---

## How the agent is built

```
Request → route (scenario, cards, models) → intake ⏸ → sources → research → situation → options (+red team)
        → choice ⏸ → strategy (product + communication) → validation → review (check + auditor)
        → six-pager + Excel ⏸ = human decides → decision ⏸ → monitoring
```

| Layer | Where | Purpose |
|---|---|---|
| Permanent instructions | [`AGENTS.md`](AGENTS.md), [`CLAUDE.md`](CLAUDE.md) | Rules, process, quality gates |
| Skills | [`.claude/skills/`](.claude/skills) — 12 | Repeatable step procedures, incl. background six-pager assembly |
| Subagents | [`.claude/agents/`](.claude/agents) — 8 | researcher, red-team, evidence-auditor, synthetic-respondent, data-analyst, ux-analyst, comms-strategist, router |
| Hooks | [`.claude/settings.json`](.claude/settings.json), [`.claude/hooks/`](.claude/hooks) | Context at session start, allowed domains, action log, prompt-injection scan, auto-check, cost |
| Method base | [`knowledge/methods/`](knowledge/methods) — ~70 cards, [`INDEX.md`](knowledge/INDEX.md) | Distilled from 7 product courses + product-skills; techniques only, no brands |
| Templates & rubric | [`knowledge/templates/`](knowledge/templates), [`knowledge/rubrics/`](knowledge/rubrics) | Output structure and quality criteria, incl. the six-pager template |
| Settings | [`config/models.json`](config/models.json), [`pricing.json`](config/pricing.json), [`quality_gate.json`](config/quality_gate.json) | Model routing, prices, check rules |
| Tools | [`tools/pfs/`](tools/pfs) — CLI + MCP server | State, sources, claim registry, checks, impact, decisions, cost, search, data, Excel models, six-pager |
| Projects | `projects/<slug>/` | Materials, state and results of each task — separate from knowledge |

More: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) · key decisions: [`docs/DECISIONS.md`](docs/DECISIONS.md) ·
verification verdict: [`docs/VERIFICATION.md`](docs/VERIFICATION.md)

---

## Key decisions (short)

1. **A claim registry instead of "text with links".** Every fact is a `C###` record with a type
   (fact / hypothesis / forecast / assumption / inference), strength A–D, and a source `S###`. The tool refuses
   to store a fact without a source, a fact based on synthetic interviews, or an inference without grounds.
   Documents reference `[C###]`; `pfs check` catches untagged numbers and links to retracted claims.
2. **Memory that never turns an agent answer into a fact.** Agent conclusions are `inference` records with
   `derived_from`; outdated items are retracted/superseded, never deleted; `pfs impact` shows which conclusions,
   document lines, and decisions a new source touches.
3. **Different models for different tasks** — [`config/models.json`](config/models.json): a cheap model for
   classification, extraction, rubric scoring, and AI respondents; a strong one for synthesis, options,
   red team, and strategy; escalation rules; profiles for other environments. `pfs models` / `pfs models sync`.
4. **A human in the loop only where the choice matters:** brief, option choice, decision approval.
5. **State in files:** any step can be interrupted and continued in a new chat or another IDE —
   everything lives in `projects/<slug>/`.
6. **Six-pager with Excel attachments.** `pfs export --six-pager` assembles a committee report in the
   reference structure (FAQ-1…FAQ-6: state, personas, initiatives, tactics, plan, metrics); `pfs calc`
   generates formula-driven Excel workbooks in the background (unit economics with LTV/CAC and sensitivity,
   a 12-month growth model, cohort retention, PAM→TAM→SAM→SOM market sizing + PESTEL) — parameters on an
   Input sheet, recalculated on open, zero dependencies.
7. **Zero dependencies:** CLI, MCP server, tests, and Excel generation — Python standard library only.
8. **Security:** source texts are treated as data; instruction-like phrases are flagged; disallowed domains are
   blocked before the request; SSRF and secret-file protection; synthetic material and interviews carry no
   personal data; secrets live in a git-ignored `.env`.

---

## CLI commands

`python3 -m tools.pfs --help` — full list. The essentials: `new`, `status`, `route`, `models`, `step`,
`ask/answer`, `source add|list|show`, `claim add|list|retract|supersede`, `check`, `impact`,
`decision add|due|done`, `data profile|cohort`, `calc`, `kb search|index|show`, `cost`,
`export --six-pager`, `doctor`. Cheat sheet at the end of [`AGENTS.md`](AGENTS.md);
detailed Help — [`docs/HELP_EN.md`](docs/HELP_EN.md) (RU: [`docs/HELP.md`](docs/HELP.md)).

## Limitations

- The agent works inside an LLM environment: quality depends on the model and web search availability there.
- Some sites block automated fetching — save the text manually via `--text-file` with the URL.
- Synthetic interviews yield hypotheses only; real interviews are conducted by humans (with consent, no
  personal data in the repo).
- Cost is counted automatically from Claude Code transcripts; in other environments — manual `pfs log --usd`.
- Excel workbooks are generated without charts/macros (standard library); they open in Excel, Numbers,
  LibreOffice, Google Sheets and recalculate formulas on open.
- New Claude Code subagents are picked up after a session restart.
