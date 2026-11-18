# Maintenance Documentation — Product Factory Strategist

> Maintenance, operations and evolution of the project. For users: [USER_GUIDE_EN.md](USER_GUIDE_EN.md).
> For admins: [ADMIN_GUIDE_EN.md](ADMIN_GUIDE_EN.md).

## 1. Versioning and releases

- Scheme: `vMAJOR.MINOR.PATCH` (v1.2.x — the current line).
- Releases are shipped by the swarm's release manager: squash-merge into main, a CHANGELOG
  entry, counters via `scripts/update_skill_counts.py --write`, docx rebuild.
- v1.2.x tags point at the release commit (rewritten during filter-repo — neutral authorship).

## 2. Regular maintenance

| Cadence | Action | Command |
|---|---|---|
| Before every push | gates: suite + doctor + strict | `python3 -m unittest discover -s tests && pfs check --strict` |
| After adding/removing a test | counters | `python3 scripts/update_skill_counts.py --write` |
| After editing README/HELP/SUBMISSION | docx versions | `python3 -m tools.pfs docx <md> --out docs/docx/<name>.docx` |
| Weekly | base update: fetch + lint | `git -C knowledge pull && pfs kb lint` |
| After source changes | quote verification | `pfs check --strict` (numeric cross-check) |

## 3. Updating the knowledge base

The distillation process (details in `knowledge/inbox/external-methodology/README.md`):

1. External methodological materials land in the inbox (raw files are not published).
2. A methodologist extracts a method into a `methods/<id>.md` map + the `methods_en/<id>.md`
   mirror (frontmatter: id, lang, tags, related; method sections and quality criteria).
3. RU/EN parity is checked by `pfs kb lint` (sections and volume).
4. `INDEX.md`/`INDEX_EN.md` are updated by `pfs kb index`.

Current state: 111 RU maps + 111 EN maps, templates (including the six-pager PROMPT and
the reference outline), rubrics. Institutional terms, brands and personal data — 0.

## 4. The Swarm: pipeline maintenance

| Aspect | Details |
|---|---|
| Start | supervisor (launchd) or `bash scripts/swarm/run.sh` |
| Queue | Linear: Todo + the `swarm` label (pick — first in line) |
| Attempts | 2; after that — parked (does not block the queue) |
| Stuck | an In Progress claim > 90 min → requeue |
| Crash tails | `blocked executor leftovers` in the stash — apply or discard |
| Lost commits | `git reflog` → cherry-pick (harsh authorship is reset by the orchestrator) |
| Release | gh pr create; fallback — local squash-merge |
| Logs | `.task-board/*.log`, `/tmp/swarm-watchdog-run.log` |

Common failures: an executor exceeded 25 min (no commits — the attempt is not burned);
red gates → feedback to the worker (up to 3 rounds); an issue in Backlog is not picked —
move it to Todo.

## 5. Known limitations

- **docx**: the generator has no complex-level table styles — complex tables are edited manually.
- **PDF**: not built by the agent (read-only via pdftotext/pypdf); the six-pager PDF is manual.
- **gh pr create** crashes after a repository rename (redirect) — the release manager
  automatically falls back to a local squash-merge.
- **uv-tool environment without pip**: `python -m pip install` does not work — use
  `uv tool install --force --with certifi …` (PRO-82).
- **filter-repo and GitHub**: pre-rewrite commits may remain accessible by SHA until GC.
- **EN six-pager**: written manually by the writer; the skeleton draft contains the EN draft marker.

## 6. Diagnostics

```bash
pfs doctor                        # environment: PATH, python, TLS chain, base, projects
python3 -m unittest discover -s tests   # suite
python3 scripts/update_skill_counts.py --check  # counters without writing
pfs kb lint                       # knowledge base integrity
git log --all --oneline | head    # history (rewritten: neutral authorship)
git stash list                    # tails of interrupted executors
```

Logs: `.task-board/*.log` (swarm), `~/.local/share/opencode/log/` (workers),
`/tmp/swarm-watchdog-run.log` (supervisor).

## 7. Maintained artifacts structure

| Artifact | Where | Update |
|---|---|---|
| Project documents 00–07 | `projects/<slug>/outputs/` | process steps + pfs export |
| Six-pager RU/EN | `projects/<slug>/outputs/SIX_PAGER*.md` | writer loop + finish |
| Excel appendices | `outputs/attachments/*.xlsx` | `pfs calc all` |
| Deck | `outputs/presentations/deck.html` | `pfs export --deck` |
| docx documentation | `docs/docx/` | rebuilt from md |
| Site | a separate repository → strategyproduct.ru | push → Pages |

## 8. Channels

- Tasks and status: Linear (the PRO team), the `swarm` label — via the swarm.
- Code and releases: GitHub — three repositories (agent, base, site).
- Site: strategyproduct.ru (GitHub Pages).
