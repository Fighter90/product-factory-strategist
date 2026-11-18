# Administrator Guide — Product Factory Strategist

> For the admin/devops who deploys, configures and maintains the agent.
> For users: [USER_GUIDE_EN.md](USER_GUIDE_EN.md). Maintenance: [SUPPORT_EN.md](SUPPORT_EN.md).

## 1. Deployment architecture

Three repositories:

| Repository | Visibility | Contents | Folder after install |
|---|---|---|---|
| `product-factory-strategist-agent` | public | CLI `pfs`, skills, subagents, hooks, tests | root |
| `product-factory-strategist-base` | public | 111 method maps RU/EN, templates, rubrics, distillation inbox | `knowledge/` |
| `product-factory-strategist-site` | public | landing, demo, help — strategyproduct.ru | deployed to GitHub Pages |

`knowledge/` inside the agent repository is a clone of the base, gitignored (the content lives in the base).

## 2. Installation

```bash
git clone https://github.com/Fighter90/product-factory-strategist-agent.git
cd product-factory-strategist-agent
bash scripts/install.sh
```

The script: clones all three repositories, installs `pfs` globally (uv tool → venv+symlink
fallback), verifies the base and the environment (`pfs doctor`). No tokens needed —
all repositories are public.

Requirements: Python 3.9+ (uv recommended), git, network access to github.com.
Optional: pdftotext (poppler) for PDF reading, pypdf.

Doctor composition: install mode (editable/venv/source), package version, `pfs` path,
PATH health, projects dir, Python version, pdftotext/pypdf, certifi/TLS chain
(certifi → truststore → `SSL_CERT_FILE`), KB map count, active project.

## 3. Configuration

| File | Purpose |
|---|---|
| `config/quality_gate.json` | gate rules: required document sections, banned terms, word budget, KPI columns |
| `config/models.json` | LLM tasks (route, extract, judge, editor…) and their models; `pfs models` |
| `.env` (not committed) | `LINEAR_API_KEY` (MCP), optional OpenAlex/SemanticScholar keys |
| `.env.example` | placeholders — copy to `.env` |

Secrets are NOT committed: `.env` is in `.gitignore`, `.env.example` has placeholders only.
An end-to-end agent run confirms zero real keys in the tree and the history.

## 4. Quality gates

```bash
python3 -m unittest discover -s tests   # suite (874+ tests)
python3 -m tools.pfs doctor             # environment
pfs check --strict                      # documents: errors stop the run
pfs check --six-pager                   # committee-document linter
```

The strict gate checks: C###/S### tags on numbers, document sections (Objections per option,
Alternatives, Proof + Promise-match, two-plane KPI table), claim quotes against source text,
gap sync 01↔02, six-pager EN style.

Counters (tests, skills, maps) are updated by the script:

```bash
python3 scripts/update_skill_counts.py --write
```

## 5. The Swarm: the development pipeline

The project develops itself. Pipeline: Linear (Todo + `swarm` label) → Orchestrator
→ Executor (GLM worker, worktree, up to 3 rounds with gate feedback) → Tester (deterministic
gates) → Reviewer (GLM, ACCEPT/RETURN) → Documenter → Release Manager → Linear Done.

Swarm files:

| Path | Purpose |
|---|---|
| `scripts/swarm/orchestrator.mjs` | the task pipeline: pick → develop → gates → review → release |
| `scripts/swarm/roles/*.md` | role prompts |
| `.task-board/attempts.json` | attempt counter (2, then parked) |
| `.task-board/claimed.json` | active claims; a claim > 90 min → requeue |
| `.task-board/wt-pro-XX/` | isolated task worktrees |
| `.task-board/lock` | orchestrator single-instance lock |

Reliability infrastructure: supervisor (launchd) restarts the orchestrator; blocked executors
are packed into a stash; lost commits — reflog-rescue with neutral authorship; red gates →
output is fed back to the worker.

## 6. Releases

- Main is always green: gates are mandatory before push.
- CHANGELOG.md is updated by the swarm's documenter.
- Counters (`tests/ (N)`, skills, maps) — only `scripts/update_skill_counts.py --write`.
- docx versions of the docs: `python3 -m tools.pfs docx <md> --out docs/docx/<name>.docx`.
- Site: push to `product-factory-strategist-site` → GitHub Pages deploys automatically
  (strategyproduct.ru: 8 pages × RU/EN).

## 7. Security

- Registries (`claims.jsonl`, `sources/`, `decisions.jsonl`) — CLI only; the `pre_guard` hook
  blocks direct edits, reads outside the repository are ask-gated.
- Data never leaves the machine: network calls are only source fetch/add by URL and the LLM provider.
- No institutional terms, brands or personal data: "external sources" only.
- Secret scan: `lin_api_*`, `sk-*`, `ghp_*`, passwords, `.env` — 0 in the tree and the full history.
- History rewrite (filter-repo) done; pre-rewrite commits may remain accessible by SHA
  on GitHub's side until garbage collection.

## 8. Diagnostics and repair

| Symptom | Action |
|---|---|
| `pfs` not found | `./scripts/install.sh`; PATH: `~/.local/bin` or uv tool |
| SSL: CERTIFICATE_VERIFY_FAILED | doctor shows the TLS chain; macOS: Install Certificates.command; uv tool: `uv tool install --force --with certifi …` |
| Global pfs points to a foreign checkout | reinstall from the actual checkout; doctor prints the agent code path |
| Orchestrator dead | supervisor restarts it; manually: `bash scripts/swarm/run.sh` |
| Queue empty | no Todo+swarm issues in Linear — create one |
| A task sits in Backlog | the picker takes Todo — move the status |
