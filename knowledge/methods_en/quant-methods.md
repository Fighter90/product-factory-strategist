---
id: M-quant-methods
lang: en
title: Quantitative methods: survey, sampling, data analysis
course: ux
sources: ["EN mirror of the RU methodology card M-quant-methods (knowledge/methods/quant-methods.md); original sources are listed in the RU card"]
stages: [research, validation, after-decision]
tags: [survey, questionnaire, sampling, sample-size, representativeness, scales, statistics, significance, validity, operationalization]
related: [M-research-types, M-brief-hypotheses, M-audience-research, M-loyalty-metrics, M-marketing-research, M-in-depth-interviews, M-interview-analysis, M-market-sizing, M-product-metrics, M-source-criticism, M-usp]
---

# Quantitative methods: survey, sampling, data analysis

## When to apply
You need to measure "how many", "how often", "among whom": share of a segment, prevalence of a barrier, difference between groups, effect of a change, feature priority. The card covers the full path: hypotheses → operationalization → questionnaire → sampling → field work and quality control → analysis → interpretation.

## Essence
**Qualitative and quantitative.** Qualitative methods explain *why and how* and give depth; quantitative ones show *how much and how widespread*. Couplings: *top-down* (numbers → interviews explain) and *bottom-up* (interviews → a survey checks frequencies and the weight of options). Peculiarities of quantitative methods: hypotheses are mandatory; a clear plan before launch; we research indirectly and cannot fix a question mid-field — so we need confidence in the clarity of the questions and in the validity of the data (we measured what we intended; nothing else influenced the result).

**Types of hypotheses.**
- *Descriptive* (about the existence of a link/distribution): "A is related to B". Any explanation of behavior given by a person themselves is also a descriptive hypothesis.
- *Causal* ("A influences B"): reliably tested by an experiment with a control group (A/B), not by an ordinary survey. Be careful with "because", "since", "influences"; the question "why?" in a questionnaire is treacherous.
- *Three levels:* theoretical ("users prefer to buy from legal entities"), empirical ("under equal conditions they will choose a professional seller"), statistical ("there is a significant difference in clicks between a legal entity and an individual"). A strong hypothesis is not one question but several questions together.

**Operationalization of concepts:** write down precisely what we measure, how we understand it ourselves, and how exactly we will measure it; avoid wordings that can be understood in different ways ("do you trust the service?" — trust in what: security, price, quality?). Example: "zoomers avoid extra communication" → measurable behavior ("under equal conditions chooses the option without communication"), not a trait assessment.

**Validity — three control questions before launch:**
| Question | Type of validity | How to check |
|---|---|---|
| Do we know exactly what we want to test? | construct (the question measures the construct we need) | hypotheses formulated in testable form; matrix "question ↔ hypothesis" |
| Will respondents understand the question the same way we do? | content/face (the wording is unambiguous, terms are interpreted identically) | cognitive testing and pilot: people rephrase the question in their own words |
| Are answers free of extraneous influences? | internal (question order, social desirability, momentary context excluded) | wording rules, order randomization, context control |

**Transformations and codings (when analysis requires a different data shape).** Collapsing an interval scale into an ordinal one (NPS 0–10 → "critic/neutral/promoter" for χ²) — an acceptable simplification if the goal is a signal, not an exact value. Ordinal → interval ("pseudometrization") — only for scales with N ≥ 7 and a symmetric wording, with a footnote "under the assumption of equal intervals"; otherwise median + IQR. Nominal → binary dummy variables (k−1 columns for regression); for ANOVA — effect-coding (−1, 0, +1); for ordinal variables in correlations — rank coding (Spearman). Zeros on a ratio scale under log transformation: +1 or separate handling of zeros. Record the scale type and coding in the metric passport (scale_type, coding), otherwise the next analyst will not know what "code = 3" means.

**Baseline measurement:** a hypothesis about a difference or preference is tested against something (before/after, control, competitor, previous wave). There must always be an object of comparison.

**Scales and allowed operations (4 data types).**
| Type | What is allowed | Example | Analysis |
|---|---|---|---|
| Nominal (=) | membership in a group | gender, city, choice of service | shares, mode, contingency tables; the mean is meaningless |
| Ordinal (=, >, <) | order, but not distance | "strongly disagree … strongly agree" | median, "top-2" shares, non-parametric tests, correlations |
| Interval (by how much more) | equal distances (an assumption) | probability scores, ratings 1–5 under the equal-intervals assumption | mean, strict tests (with caveats) |
| Ratio (how many times) | absolute zero | average order value, number of orders | the same + ratios of indicators |
Any answer can be coded as a number, but the number remembers its original meaning: "average age 2.5" from age-group codes is absurd.

## Procedure
### 1. Planning
1. Goal, decision, hypotheses ([[M-brief-hypotheses]]); for each — type (descriptive/causal), variables, measurement method, comparison criterion, statistical test (chosen in advance).
2. Define the population and the inference scope: on whom we want to generalize the result. If conclusions are needed by subgroups, compute the sample for each subgroup.
3. Choose a recruitment strategy (see "Sampling"), calculate the size, add a buffer.
4. Write the questionnaire, run cognitive testing (3–5 people rephrase the questions in their own words) and a pilot.

### 2. Questionnaire
**Structure:** screening and legend (who qualifies, why the survey, how long it takes, what happens to the data) → main part → closing (open question, thanks, reward terms, contacts). Branching (forks) planned in advance.

**Question types:** single choice (options mutually exclusive); multiple choice; scale (not only numeric: "agree—disagree", "likelihood", "basis of decision"); open (replace with closed where possible, limit the count). For scales, replace digits with understandable words; scales 0–10 and −5…+5 are perceived differently although computed identically.

**9 wording rules.** (1) The question is terminologically clear; you and respondents understand it the same way. (2) No negations ("which service have you rarely not used?"). (3) Does not imply a single answer. (4) No multiple questions in one ("how often do you visit and buy?"). (5) Does not provoke a socially desirable answer ("do you know that we have post-payment?"). (6) Closed questions are better than open ones. (7) Anchoring to a concrete situation (the last purchase). (8) Accounting for the survey context: right after the order or a week later. (9) Accounting for forks and logic.

### 3. Sampling
**Representativeness:** before launching, decide which conclusions you want to generalize and to whom. Example: surveying 100 first- and second-year students of university N does not allow conclusions about "students of technical majors", "the physics faculty", or "students in general".
| Strategy | Essence | When | Risk |
|---|---|---|---|
| Random | every element has an equal chance (fixed a place/event and survey everyone) | full list or event stream exists (survey after a search) | expensive, needs a list |
| Quota | artificial quotas by gender/age/region | group comparison, online panels | not random, "first come first served" |
| Stratified | split into strata, random within each | heterogeneous population, share control | need to know the distribution |
| Cluster | choose clusters (cities, branches) and survey inside | dispersed audience, savings | higher error (account for design effect) |
| "Snowball" | respondent brings the next ones | rare and closed groups, B2B | strong bias, "bubble" |

**Sample size for a share (binary question).** n = z² · p · (1 − p) / e², where z = 1.96 at a 95% confidence level, p — expected share (if unknown — 0.5, the maximum), e — allowed error as a share. The result is the number of complete, quality-passing questionnaires.
| Error e (at 95%, p = 0.5) | Responses needed n |
|---|---|
| ±10 p.p. | ≈ 96 |
| ±5 p.p. | ≈ 385 (rounded in the course to ≈ 400) |
| ±3 p.p. | ≈ 1067 |
Finite population: n_corr = n / (1 + (n − 1) / N). With N=2000 and ±5 p.p. ≈ 322 responses suffice; with N=10,000 ≈ 370; with N > 20,000 the correction barely works ("the larger the population, the fewer people are needed relative to *the share of* the population"). If the share differs noticeably from 0.5 (a rare/frequent phenomenon), n decreases: with expected p ≈ 0.1 — almost twice; a course example for a rare event (conversion ~2%, precision ±1 p.p.): p = 0.02, e = 0.01 → n ≈ 750. The mistake "plugging p = 0.5 for a phenomenon with a 1% share" inflates the budget.

**Design effect (DEFF) and weights.** Final field size: n_final = n_calc × DEFF × buffer 1.1–1.2. Course values: simple random and proportional stratification DEFF ≈ 1.0–1.1; clusters (cities, branches, homogeneous inside) ≈ 1.5–2.0; non-random online panel ≈ 1.3–1.5 ("better to overshoot than fall short"). After fielding, actual shares do not match targets — post-stratification weights are applied: `w_i = strata share in population / strata share in sample` (example: target 12%, recruited 9% → w = 1.33); weights are normalized so that Σw = n and applied **only to rows that passed quality control**. Keep "raw" and "weighted" versions in the report. If a quota has a "hole" (no observations in a segment), weights cannot save it — order more completes.

**Comparing two groups (shares).** Required size *per group* at α = 0.05 (two-sided), power 80%: n ≈ 7.85 · [p₁(1−p₁) + p₂(1−p₂)] / (p₁ − p₂)². Examples: 40% vs 50% → ≈ 385 per group; 40% vs 55% → ≈ 170; 30% vs 40% → ≈ 353; 5% vs 6% → ≈ 8000. The smaller the effect, the faster n grows. For comparing means, compute power from the expected effect size (d) and SD; without statistics literacy, bring in an analyst.

Practical course guidelines by method: feature-choice surveys (Kano), SBS and CJM validation — from ≈300; segmentation surveys — from several hundred (a long questionnaire reduces completion).

### 4. Field work and quality control
Soft launch (pilot of 30–50 questionnaires): check timing, drop-outs, logic; if the share failing a trap question or the median time differs sharply from expectations — fix the question and the interface before the mass launch. Controls: 1–2 trap questions (attention), timer (rejecting too-fast completes — under a third of the pilot's median time), straight-lining (SD = 0 across scales), limiting repeats (IP/cookie/device-fingerprint), meaningfulness of open answers (minimum length, nonsense detector), drop-out monitoring by screen (a sharp dip on one screen — a question or interface error). An end-to-end QC pipeline: flags on the questionnaire (time, trap, variability, open answer) → quality score `QScore = 0.3×time + 0.4×attention + 0.3×meaningfulness` (0–100, cut below ~70) → weights on cleaned rows → loss report (N raw / N clean / reasons). Field stop-triggers: trap failures > 25% in a row → suspend delivery; median time dropped sharply within a short window → check for bot traffic; drop-out on a screen > 30–35% → fix and restart; rejected share > 15% of plan → reorder with a loss coefficient. Fix rejection rules and stops before the start; the field log matters more than the presentation (an audit believes the log).

Reducing drop-out (order of techniques from the course): a progress bar "step X of N" (−10 p.p.), splitting one big matrix into separate screens (−8), mobile layout with autosave (−6…−8), time indication "about 3 min left" (−5), branching/skip-logic — show only relevant questions (up to −15). Loss report (why questionnaires were removed) and a check that the final n is not below the planned one and quotas are closed. Clean the data before analysis, fix exclusion criteria in advance.

Tools: Google Forms (simple, no complex logic), Typeform, Toloka, Fabula, Pathway (panels and surveys), analytics platforms.

### 5. Data analysis
**The idea of mathematical statistics:** answer whether a difference is natural sampling noise or a significant difference. You cannot compare "3.7 vs 4.2" or "43% vs 50%" without a test and an interval.

**Choosing an approach (course decision tree, with explanations).**
- Can answers be ordered ascending? *No* (nominal): shares and mode; to understand that 48/52% is statistically equal to 50/50, use contingency tables (χ²; for small cells — Fisher's exact test).
- *Yes* (ordinal/interval): correlation analysis — a link between indicators (A changes — B changes; does not prove the cause); regression — only if there are grounds to believe A precedes B.
- Was one indicator measured several times in the same group (before/after)? *Yes* — tests for paired samples (paired t-test or Wilcoxon), the difference is computed per respondent (subtract "after − before" and test Δ, not compare columns). *No* — tests for unpaired samples (t-test, Mann—Whitney for ordinal data, ANOVA/Kruskal—Wallis for three or more groups).
- Comparing more than two groups and multiple comparisons: corrections (Bonferroni, Holm), otherwise false "wins".

**Normality check before parametric tests (course algorithm):** n < 50 → Shapiro—Wilk test; 50 ≤ n ≤ 300 → Kolmogorov—Smirnov (with Lilliefors correction); n > 300 → by CLT a chart and skewness suffice (|skewness| < 1 — "normal"). Non-normality or outliers → non-parametric analogs (Wilcoxon instead of paired t, Mann—Whitney instead of t, Kruskal—Wallis instead of ANOVA).

**Power and errors.** α = 0.05 is a 5% risk of a false alarm; the β-error (power) covers "missed" effects: aim for 1 − β ≥ 0.8. "p = 0.051, almost significant" is not an argument: either recompute the required minimum detectable effect (MDE), or collect more data, or admit there is no conclusion.

**Effect size is mandatory (course table):**
| Comparison | Metric | Interpretation scale |
|---|---|---|
| Two means | Cohen's d | 0.2 small / 0.5 medium / 0.8 large |
| Shares | OR (odds ratio), RR | > 1 — the odds/risk are higher by that factor |
| Categories (tables) | Cramér's V | 0–1, strength of association |
Course example: n = 10,000, a difference of 0.1 p.p., p < 0.001, d = 0.05 — statistically "significant", gives business nothing.

Always report: the test, p-value, **effect size** and **confidence interval** (for a share ±1.96·SE, "whiskers" on the chart). A p-value without an effect size is a half-truth: on large samples even negligible differences are significant; on small ones, significance is absent.

**Three steps of processing:** state the fact ("80% of zoomers chose the option without communication"); interpret ("what it means"); discuss (link to other data, propose new hypotheses). Example: if 80% do not want to communicate, but those who did communicate give high ratings — the problem may be at the *start* of the dialogue, not in communication itself. The success of research is not only describing percentages and means, but also explanation and new hypotheses.

**Causality:** an ordinary one-off survey does not prove "A influences B". For the effect of a feature you need an experiment (A/B with control) or comparison with a control group; a "before and after" comparison without control mixes effect and time (season, promos). Example of faulty logic: comparing satisfaction "before" and "after" without accounting for changes in the group.

### 6. Visualizing results
**The "3-B" rule: Bold** (one accent color for the key series, the rest muted), **Brief** (one chart — one thought, ≤ 5–7 series), **Beautiful** (even labels, CVD-safe colors, no 3D or shadows — cleanliness = trust).

| Data | Chart |
|---|---|
| Shares (yes/no, top-2) | 100% stacked bar + confidence-interval "whiskers" (±1.96·SE) |
| 3–7 categories | horizontal bar, sorted descending, numbers right on the bars |
| 8+ categories | Pareto (bars + cumulative % line): focus on the "top-80%" |
| Likert scales | 100% stacked bar (polarization visible); heatmap at 5+ questions |
| Means | box-plot or error-bar with CI |
| Cohorts/dynamics | heatmap sorted by date; a chaos of colors kills the insight |

Anti-patterns: a pie chart with > 5 sectors; 3D and "donuts"; two Y axes with different scales; a red-green palette (inaccessible to color-blind people); a heatmap without a legend. The chart title states the conclusion ("67% choose delivery — +6 p.p. versus last year"), not a description ("a chart of shares").

**Story dashboard: Headline → Context (method, sample, date) → Main chart → Support (segments, details) → Action** ("we are rebuilding step 3 of onboarding").

## Template / checklist

**Survey specification:**
| Field | Fill in |
|---|---|
| Decision and business metric | |
| Hypotheses (type; theoretical → empirical → statistical) | |
| Population and on whom we generalize conclusions | |
| Variables, scales, operationalization | |
| Object of comparison (baseline, control) | |
| Sampling strategy, n, error, buffer, quotas | |
| Recruitment channel and incentive | |
| Quality control (pilot, traps, timer) | |
| Analysis plan: tests, effect, intervals | |
| Decision criterion (threshold) and next step | |

**Launch checklist:** hypotheses tied to the goal; questions tested for clarity and absence of leading; scales labeled; pilot run; n computed for the needed precision *per each subgroup*; data exclusion plan fixed; analysis method specified; consent and personal-data protection ensured.

## Common mistakes
- Causal conclusion from a correlation or from a single survey; trusting the "why?" question.
- Non-operationalized concepts; double-barreled and leading questions; questions with negations; provoking the "right" answer.
- The mean of an ordinal scale as an "exact number"; a mean without a distribution; comparing means without a test.
- No baseline measurement: "NPS became 40" without a base for comparison.
- Conclusions about "everyone" from a single-channel sample; self-selection bias; ignoring those who *did not* answer.
- The sample computed, but subgroups, design effect and rejection losses not accounted for.
- Skipping the pilot; a questionnaire too long — low completion and fatigue.
- Multiple comparisons without corrections; searching for significance after collection.
- Statistical significance taken as practical importance; ignoring confidence intervals.
- "Paired" data analyzed as independent (power is lost).

## Questions that can change the decision
- What do we want to prove: the existence of a link, a difference, or a causal influence (an experiment is needed)?
- What precision does the decision need (±5 p.p. or is ±10 enough) and what does extra precision cost?
- Are conclusions needed by segments (each segment gets its own sample)?
- Is there an external source of truth to cross-check (analytics, sales)?
- Can we run an A/B instead of a survey to measure behavior rather than declarations?
- Are analytical skills sufficient in the team or is a statistician needed?

## Related cards
[[M-research-types]], [[M-brief-hypotheses]], [[M-audience-research]], [[M-loyalty-metrics]], [[M-marketing-research]], [[M-in-depth-interviews]], [[M-interview-analysis]], [[M-market-sizing]], [[M-product-metrics]], [[M-source-criticism]], [[M-usp]]
