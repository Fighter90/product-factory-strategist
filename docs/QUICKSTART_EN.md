# Quick Start: full end-to-end agent testing

A step-by-step guide: how to verify the agent completely — from a clean install to the
final package (six-pager RU/EN, Excel, deck) in both languages. Every step has a command
and a pass criterion.

> Short install version — [INSTALL_EN.md](INSTALL_EN.md). RU version of this guide: [QUICKSTART_RU.md](QUICKSTART_RU.md). All commands — in the cheat sheet in the [README](../README_EN.md).

## Step 0. Clean install (5 minutes)

```bash
rm -rf ~/agent-test && mkdir ~/agent-test && cd ~/agent-test
git clone https://github.com/Fighter90/product-factory-strategist-agent.git agent
cd agent && bash scripts/install.sh    # 3 repos + global pfs + doctor
pfs doctor                             # PATH, Python, TLS, 111 maps, projects
```

✅ criterion: "Installation complete", doctor with no errors, `pfs --help` lists all commands.

## Step 1. RU run: full 12-step cycle with data

```bash
mkdir -p ~/agent-test/projects && export PFS_PROJECTS_DIR=~/agent-test/projects
pfs new "ATS: junior resume passes filters" "Junior resumes fail ATS filters (75% are cut before a recruiter). Build a keyword-match checker and hints to raise the pass rate from 40% to 80%?"
pfs route growth
printf '# Data: ATS and resumes\n\n- ATS is used by 98%% of Fortune 500.\n- The filter cuts 75%% of resumes before a recruiter.\n' > /tmp/src.md
pfs source add /tmp/src.md --origin public
pfs claim add "ATS cuts 75% of resumes before a recruiter" --kind fact --source S001 --grade B --quote "The filter cuts 75% of resumes"
pfs claim add "98% of Fortune 500 use ATS" --kind fact --source S001 --grade B --quote "98% of Fortune 500 use ATS"
pfs claim add "Keyword match improves pass rate 2-3x" --kind fact --source S001 --grade B --quote "Keyword match improves pass rate 2-3x"
pfs claim add "Junior resumes cover 40% of keywords" --kind hypothesis --source S001 --grade B
pfs step intake done --next sources && pfs step sources done --next research
pfs step research done --next discovery && pfs step discovery done --next situation
pfs step situation done --next options && pfs step options done --next choice
pfs ask "Which option?" --options "A: keep as is,B: ATS scan" && pfs answer "B: ATS scan"
pfs step choice done --next strategy && pfs step strategy done --next validation
pfs step validation done --next review && pfs step review done --next decision
pfs decision add --title "ATS scan" --decision "Keyword-match checker module" --owner PM --grounds C001,C003 --review 2027-03-01
pfs step decision done --next finish
```

✅ criterion: each step prints "Step maps", no errors.

## Step 2. Documents 00–07 + the quality gate

Fill 02/03/04/05/06 per the templates in `knowledge/templates/`:
03 — options + "Objections" for each, 04 — "Alternatives", "Chosen direction", "Conscious refusals",
05 — "Proof" table with [C###] tags + "Promise-to-product match",
06 — a two-plane KPI table with the "Plane" column.

```bash
pfs check --strict    # target: 0 errors
```

## Step 3. Two-step six-pager (PRO-46)

```bash
pfs export --six-pager          # step 1: the data pack + FAQ-1…6 skeleton with slots
pfs check --six-pager           # step 2: the committee-document linter; loop "fix → 0 errors"
```

✅ criterion: 0 errors; footnotes [^N] match the sources; word budget ≤ 3500.

## Step 4. The final package

```bash
pfs finish    # REPORT, six-pager RU/EN (md/docx), 4 Excel workbooks, deck
ls projects/*/outputs/   # target: 11 finish artifacts (+ data pack and JSON registries — 18 files)
```

✅ criterion: REPORT.md, SIX_PAGER.md/.docx, SIX_PAGER_EN.md/.docx, 4 Excel workbooks, deck.html — all present.

## Step 5. EN run (alternating with RU)

```bash
pfs new --lang en "ATS resume scanner" "Junior resumes fail ATS filters. Build a keyword-match checker to raise pass rate from 40% to 80%?"
# repeat the steps in English; then verify:
grep -c "[а-яА-Я]" projects/*/outputs/SIX_PAGER_EN.md   # target: 0 Cyrillic characters
```

## Step 6. Smoke every CLI command

Run each command from the cheat sheet (README, HELP) — one line at a time:

```bash
pfs models && pfs kb search "test"
pfs data profile events.csv 2>/dev/null || true   # CSV/XLSX; a non-tabular file gives a clear error, not a Traceback
pfs interview guide --persona "Student"
pfs media add shot.png --desc "test" 2>/dev/null || true
pfs ab --hypothesis "Hypothesis [C001]" --metric "conversion"
pfs roadmap 2>/dev/null || true
pfs cost && pfs doctor
```

✅ criterion: no argparse usage errors, no Tracebacks.

## Step 7. The full test suite

```bash
python3 -m unittest discover -s tests   # target: OK, 874+ tests
python3 scripts/update_skill_counts.py --check  # counters are fresh
```

## Step 8. MCP servers

In OpenCode: `/mcp` — every server shows "connected"
(`linear-pfs` — issue operations, `producthunt`, `context7`, `zai-mcp-server`).

## If something doesn't match

- A mismatch with a "✅ criterion" is a bug: file a Linear issue labeled `swarm` —
  the swarm fixes it and ships a release.
- Common failures and remediation — [ADMIN_GUIDE_EN.md](ADMIN_GUIDE_EN.md), "Diagnostics".
