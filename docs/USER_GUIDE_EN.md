# User Guide — Product Factory Strategist

> For a product lead using the agent for product decisions.
> Companion docs: [SUPPORT_EN.md](SUPPORT_EN.md). Administrator guide: [ADMIN_GUIDE_EN.md](ADMIN_GUIDE_EN.md).

## 1. What the agent is

Product Factory Strategist is a CLI agent for digital product leads.
You state a product question ("Why is conversion dropping?", "Should we introduce tiered pricing?"),
and the agent walks you through a 12-step process: from clarifying the brief to a
committee-ready document (six-pager) with an evidence base.

Key properties:

- **Verifiability.** Every material claim has a source ([S###]) and a claim tag ([C###]);
  numeric cross-checks catch mismatches against the source.
- **12 steps.** A fixed process: intake → sources → research → discovery → situation →
  options → choice → strategy → validation → review → decision → monitoring.
- **Pauses only on decisions.** The agent stops at intake, choice, decision and finish;
  in between it moves without unnecessary questions.
- **Two languages.** EN projects via `--lang en`; RU is the default.
- **Nothing leaves the machine.** Registries and documents live in the project folder;
  registries are edited only through `pfs`.

## 2. Installation (5 minutes)

```bash
git clone https://github.com/Fighter90/product-factory-strategist-agent.git
cd product-factory-strategist-agent
bash scripts/install.sh
```

The script clones three repositories (agent, knowledge base `knowledge/`, site), installs
`pfs` globally and runs a self-check (`pfs doctor`). Details: [INSTALL_EN.md](INSTALL_EN.md).

Environment check:

```bash
pfs doctor   # PATH, python, pdftotext/pypdf, TLS chain, KB map count, active project
```

## 3. First run

```bash
pfs new "Project title" "Your product question verbatim"
```

The agent creates the project in `projects/<slug>/`, asks clarifying questions (intake step)
and walks you through the steps. Orientation helpers:

```bash
pfs status   # where you stopped, what's next
pfs next     # "what to decide now": step, commitments, revisions
```

## 4. The 12 steps — what to do at each

### Step 1 · intake — clarify the brief
Answer the agent's questions: decision, goal, audience, constraints, data.
Output: `00_brief.md`.

### Step 2 · sources — collect materials
```bash
pfs source add <file.md|pdf|csv> --origin public   # your materials
pfs source add https://example.com/report          # web page (fetched, URL-deduped)
pfs source fetch https://blocked.example.com --title "…"  # unreachable URL: retries and fallbacks
pfs source list                                    # the S### source registry
```
Rule: data not obtained from external sources is honestly marked as a hypothesis.
Blocked domains are configured in `quality_gate.json`.

### Step 3 · research — the study
Register claims with evidence strength:

```bash
pfs claim add "Statement" --kind fact --source S001 --grade B --quote "verbatim quote"
pfs claim add "Hypothesis" --kind hypothesis --source S001
pfs claim add "Conclusion" --kind inference --from C001,C002
```

The gate watches quotes: numbers in a quote must appear in the source text.
If the quote doesn't match — `pfs claim fix-source --id C001 --source S002` (with re-verification).

### Step 4 · discovery — users and alternatives
Personas, JTBD, competitors. The step maps suggest methods (`pfs step` prints them).

### Step 5 · situation — the situation picture
`02_situation.md`: what's known, what's not (a gap table), contradictions,
questions that could change the decision.

### Step 6 · options — options
`03_options.md`: at least three substantively different options, including "keep as is"
and "shut down". Each option has an "Objections" section with counter-arguments.

### Step 7 · choice — the lead's decision
The agent shows the comparison and a recommendation, pauses with `pfs ask` → you answer `pfs answer "B"`.

### Step 8 · strategy — strategies
`04_product_strategy.md` (audience, chosen direction, economics, roadmap stages)
and `05_comms_strategy.md` (audience, barrier, message, "promise → proof" table).

### Step 9 · validation — the validation plan
`06_validation_plan.md`: expected change, comparison base, duration, counter-metrics,
two-plane KPIs (business/product) as an explicit table.

### Step 10 · review — quality control
```bash
pfs check --strict      # blocking errors stop the run
pfs review lock         # lock the verdict after the revision
```

### Step 11 · decision — the decision
```bash
pfs decision add --title "…" --decision "…" --owner PM --grounds C001,C003 \
  --review "2027-02-01" --trigger "metric < X" --commit "what | who | when"
pfs decision due      # what to decide now
```

### Step 12 · monitoring — on request
A separate mode: `pfs decision due`, `pfs next`. It does not start automatically.

## 5. The final package: six-pager

A two-step workflow:

```bash
pfs export --six-pager    # step 1: data pack + FAQ-1…6 skeleton with slots
pfs check --six-pager     # step 2: committee-document linter; loop "fix → 0 errors"
pfs finish                # final package: 4 Excel + REPORT + six-pager RU/EN + DOCX + deck
```

The linter checks: reference structure, word budget ≤ 3500, template leftovers, empty tables,
service IDs without decoding, arithmetic (contributions 100%, metrics match), footnotes,
language (EN without Cyrillic). The six-pager is not rebuilt over written text.

## 6. Skills and subagents

101 skills in `.claude/skills/` (13 core + 27 product + 57 personal library + 4 integrations).
Invoke: `pfs kb show <map>` for the method; a skill connects automatically by step context.
10 subagents (`.claude/agents/`): researcher, red-team, evidence-auditor, synthetic-respondent,
data-analyst, ux-analyst, comms-strategist, router, six-pager-writer, editor.

## 7. User FAQ

| Symptom | Action |
|---|---|
| "Task 'X' is not described in models.json" | `pfs models` — the list of available tasks; use real tasks (`judge`) in cheat sheets |
| A number without a C###/S### tag | add a claim tag or mark it as a "product assumption" |
| Linter: "KPI/CAC undecoded" | decode the abbreviation at first mention |
| "document not written yet" | the working document doesn't exist yet — fill it or remove the link |
| finish rejects the package | `pfs check --strict` shows the list: fix and retry |
