---
id: M-quant-methods
lang: en
title: Quantitative methods: survey, sampling, data analysis
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [research, validation, after-decision]
tags: [survey, questionnaire, sampling, sample-size, representativeness, scales, statistics, significance, validity, operationalization]
related: [M-research-types, M-brief-hypotheses, M-audience-research, M-loyalty-metrics, M-marketing-research, M-in-depth-interviews, M-interview-analysis, M-market-sizing, M-product-metrics, M-source-criticism, M-usp]
---

# Quantitative methods: survey, sampling, data analysis

## When to apply
You need to measure "how much", "how often", "in whom": a segment share, the prevalence of a barrier, a difference between groups, the effect of a change, the priority of a feature. The card covers the full path: hypotheses → operationalization → questionnaire → sampling → fieldwork and quality control → analysis → interpretation.

## Core idea
**Quality and quantity.** Qualitative methods explain *why and how* and give depth; quantitative methods show *how much and how widespread*. Combinations: *top-down* (numbers → interviews explain them) and *bottom-up* (interviews → a survey checks frequencies and the weight of answer options). Specifics of quantitative methods: hypotheses are mandatory; a firm plan before launch; we measure indirectly and cannot fix a question mid-field — which means we need confidence in the clarity of the questions and in the validity of the data (we measured what we intended to; nothing else interfered).

**Types of hypotheses.**
- *Descriptive* (about the existence of a relationship/distribution): "A is related to B". Any explanation of behavior given by the person themselves is also a descriptive hypothesis.
- *Causal* ("A influences B"): reliably tested by an experiment with a control group (A/B), not by a regular survey. Be careful with "because", "since", "influences"; the "why?" question in a questionnaire is treacherous.
- *Three levels:* theoretical ("users prefer buying from business sellers"), empirical ("under equal conditions they will choose a professional seller"), statistical ("there is a significant difference in clicks between business and private accounts"). A strong hypothesis is not one question but several questions together.

**Operationalization of concepts:** write down exactly what you measure, how you yourselves understand it, and how exactly you will measure it; avoid wording that can be understood in different ways ("do you trust the service?" — trust in what: safety, price, quality?). Example: "zoomers avoid unnecessary communication" → measurable behavior ("under equal conditions they choose the option without communication"), not an assessment of a trait.

**Validity — three control questions before launch:**
| Question | Type of validity | How to check |
|---|---|---|
| Do we know exactly what we want to test? | construct (the question measures the construct we need) | hypotheses are formulated testably; a "question ↔ hypothesis" matrix |
| Will respondents understand the question the same way we do? | content/face (the wording is unambiguous, terms are interpreted the same way) | cognitive probing and a pilot: people retell the questions in their own words |
| Do extraneous factors influence the answer? | internal (question order, social desirability, momentary context are excluded) | wording rules, randomization of order, context control |

**Transformations and encodings (when the analysis requires a different shape of data).** Collapsing interval into ordinal (NPS 0–10 → "detractor/passive/promoter" for χ²) is an acceptable simplification if the goal is a signal, not an exact value. Ordinal → interval ("pseudometrization") — only for scales with N ≥ 7 and a symmetric wording, with a footnote "under the assumption of equal intervals"; otherwise the median + IQR. Nominal → binary dummy variables (k−1 columns for regression); for ANOVA — effect coding (−1, 0, +1); for ordinal variables in correlations — rank encoding (Spearman). Zeros on a ratio scale under log transformation: +1 or separate handling of zeros. Record the scale type and the encoding in the metric passport (scale_type, coding), otherwise the next analyst will not understand what "code = 3" means.

**Null measurement:** a hypothesis about a difference or a preference is tested against something (before/after, control, a competitor, the previous wave). There must always be an object of comparison.

**Scales and allowed operations (4 data types).**
| Type | What is allowed | Example | Analysis |
|---|---|---|---|
| Nominal (=) | membership in a group | gender, city, choice of a service | shares, mode, contingency tables; the mean is meaningless |
| Ordinal (=, >, <) | order, but not distance | "strongly disagree … strongly agree" | median, "top-2" shares, nonparametric tests, rank correlations |
| Interval (by how much more) | equal distances (an assumption) | probability scores, 1–5 ratings under the assumption of equal intervals | mean, stricter tests (with caveats) |
| Ratio (by how many times) | absolute zero | average order value, number of orders | the same + ratios of indicators |

Any answer can be encoded as a number, but the number remembers its original meaning: "average age 2.5" computed from age-group codes is absurd.

## Procedure
### 1. Planning
1. Goal, decision, hypotheses ([[M-brief-hypotheses]]); for each — the type (descriptive/causal), variables, method of measurement, comparison criterion, statistical test (choose in advance).
2. Define the population and the conclusions: on whom we want to extend the result. If conclusions are needed for subgroups, compute the sample for each subgroup.
3. Choose a recruiting strategy (see "Sampling"), compute the size, add a buffer.
4. Write the questionnaire, run cognitive probing (3–5 people retell the questions in their own words) and a pilot.

### 2. Questionnaire
**Structure:** screening and legend (who fits, what the survey is for, how long it takes, what happens to the data) → the main part → the closing (an open question, thanks, reward terms, contacts). Branching (forks) planned in advance.

**Question types:** single choice (options are mutually exclusive); multiple choice; scale (not only numeric: "agree—disagree", "likelihood", "basis of the decision"); open-ended (replace with a closed question where possible, limit the number). For scales, replace digits with understandable words; 0–10 and −5…+5 scales are perceived differently even though they are computed the same way.

**9 wording rules.** (1) The question is terminologically clear; you and the respondents understand it identically. (2) No negations ("which service have you rarely not used?"). (3) Does not imply a single answer. (4) Contains no several questions in one ("how often do you visit and buy?"). (5) Does not provoke a socially desirable answer ("you know we have postpayment, right?"). (6) Closed questions are better than open ones. (7) Anchoring to a specific situation (the last purchase). (8) Accounting for the survey context: right after the order or a week later. (9) Accounting for branches and logic.

### 3. Sampling
**Representativeness:** before launching, decide which conclusions you want to extend and to whom. Example: surveying 100 first- and second-year students of university N does not allow conclusions about "students of technical majors", about "the physics department", or about "students in general".
| Strategy | Essence | When | Risk |
|---|---|---|---|
| Random | every element has an equal chance (you fixed a place/event and survey everyone) | a full list or an event stream exists (a survey after a search) | expensive, a list is needed |
| Quota | artificial quotas by gender/age/region | comparing groups, online panels | not random, "first come first served" |
| Stratified | we split into strata, random within each | heterogeneous population, control of shares | you need to know the distribution |
| Cluster | we pick clusters (cities, branches) and survey inside them | a dispersed audience, savings | higher error (account for the design effect) |
| "Snowball" | a respondent brings in the next ones | rare and closed groups, B2B | strong bias, a "bubble" |

**Sample size for a share (a binary question).** n = z² · p · (1 − p) / e², where z = 1.96 at a 95% confidence level, p — the expected share (if unknown — 0.5, the maximum), e — the acceptable error in shares. The result is the number of complete, quality questionnaires.
| Error e (at 95%, p = 0.5) | Responses needed n |
|---|---|
| ±10 pp | ≈ 96 |
| ±5 pp | ≈ 385 (rounded to ≈ 400 in the course) |
| ±3 pp | ≈ 1067 |

Finite population: n_corrected = n / (1 + (n − 1) / N). With N=2000 and ±5 pp, ≈ 322 responses are enough; with N=10,000 ≈ 370; with N > 20,000 the correction barely works ("the larger the population, the fewer people you need *as a share of the population*"). If the share differs noticeably from 0.5 (a rare/frequent phenomenon), n decreases: at an expected p ≈ 0.1 — almost in half; an example from the course for a rare event (conversion ~2%, precision ±1 pp): p = 0.02, e = 0.01 → n ≈ 750. The mistake of "plugging in p = 0.5 for a phenomenon with a 1% share" inflates the budget.

**Design effect (DEFF) and weights.** The final fieldwork number: n_final = n_calculated × DEFF × a buffer of 1.1–1.2. Values from the course: simple random and proportional stratification DEFF ≈ 1.0–1.1; clusters (cities, branches, homogeneous inside) ≈ 1.5–2.0; a non-random online panel ≈ 1.3–1.5 ("better to overestimate than to fall short"). After fieldwork the actual shares do not match the targets — post-stratification weights are applied: `w_i = stratum share in the population / stratum share in the sample` (example: target 12%, recruited 9% → w = 1.33); the weights are normalized so that Σw = n and applied **only to rows that passed quality control**. Keep both "raw" and "weighted" versions in the report. If a quota has a "hole" (no observations in a segment), weights cannot save it — order more respondents.

**Comparing two groups (shares).** The required size *per group* at α = 0.05 (two-sided), power 80%: n ≈ 7.85 · [p₁(1−p₁) + p₂(1−p₂)] / (p₁ − p₂)². Examples: 40% vs 50% → ≈ 385 per group; 40% vs 55% → ≈ 170; 30% vs 40% → ≈ 353; 5% vs 6% → ≈ 8000. The smaller the effect, the faster n grows. For comparing means, compute the power from the expected effect size (d) and the SD; without a grasp of statistics, bring in an analyst.

Practical course guidelines by method: feature-choice surveys (Kano), SBS and CJM validation — from ≈300; segmentation surveys — from several hundred (a long questionnaire lowers completion).

### 4. Fieldwork and quality control
A soft launch (a pilot of 30–50 questionnaires): check the timing, dropouts, logic; if the share failing the trap question or the median time differ sharply from expectations — fix the question and the interface before the mass launch. Controls: 1–2 trap questions (attention), a timer (rejecting too-fast responses — less than a third of the pilot's median time), straight-lining (SD = 0 across scales), limitation of repeats (IP/cookie/device fingerprint), meaningfulness of open answers (minimum length, a nonsense detector), dropout monitoring by screen (a sharp fall on one screen — an error in a question or the interface). An end-to-end QC pipeline: flags on the questionnaire (time, trap, variability, open answer) → a quality score `QScore = 0.3×time + 0.4×attention + 0.3×meaningfulness` (0–100, cut off below ~70) → weights on the cleaned rows → a loss report (N raw / N clean / reasons). Field stop-triggers: trap failures > 25% in a row → suspend delivery; the median time fell sharply within a short window → check for bot traffic; dropout on a screen > 30–35% → fix and restart; the rejected share > 15% of the plan → order more with a loss coefficient. Fix the exclusion rules and the stops before the start; the field log matters more than the presentation (an audit believes the log).

Reducing dropout (the order of techniques from the course): a "step X of N" progress bar (−10 pp), splitting one big matrix into separate screens (−8), a mobile layout with autosave (−6…−8), a time indicator "about 3 min left" (−5), branching/skip-logic — show only relevant questions (up to −15). A loss report (why questionnaires were removed) and a check that the final n is not below the calculated one and the quotas are closed. Clean the data before the analysis, fix the exclusion criteria in advance.

Tools: Google Forms (simple, no complex logic), Typeform, Toloka, Fabula, Pathway (panels and surveys), analytics platforms.

### 5. Data analysis
**The idea of mathematical statistics:** to answer whether a difference is the natural noise of the sample or a significant difference. You cannot compare "3.7 vs 4.2" or "43% vs 50%" without a test and an interval.

**Choosing an approach (the course's decision tree, with explanations).**
- Can the answers be ordered ascending? *No* (nominal): shares and the mode; to see that 48/52% are statistically equal to 50/50, use contingency tables (χ²; Fisher's exact test for small cells).
- *Yes* (ordinal/interval): correlation analysis — a relationship between indicators (A changes — B changes; it does not prove cause); regression — only if there are grounds to believe that A precedes B.
- Did you measure one indicator several times in the same group (before/after)? *Yes* — tests for paired samples (the paired t-test or Wilcoxon); the difference is computed per respondent (subtract "after − before" and test Δ, not compare columns). *No* — tests for independent samples (the t-test, Mann–Whitney for ordinal data, ANOVA/Kruskal–Wallis for three or more groups).
- Comparing more than two groups and multiple comparisons: corrections (Bonferroni, Holm), otherwise false "wins".

**Checking normality before parametric tests (the course's algorithm):** n < 50 → Shapiro–Wilk; 50 ≤ n ≤ 300 → Kolmogorov–Smirnov (with the Lilliefors correction); n > 300 → by the CLT a plot and skewness are enough (|skewness| < 1 — "normal"). Non-normality or outliers → nonparametric analogs (Wilcoxon instead of the paired t, Mann–Whitney instead of t, Kruskal–Wallis instead of ANOVA).

**Power and errors.** α = 0.05 is a 5% risk of a false alarm; the β-error (power) accounts for "missed" effects: aim for 1 − β ≥ 0.8. "p = 0.051, almost significant" is not an argument: either recompute the required minimum detectable effect (MDE), or collect more data, or admit there is no conclusion.

**Effect size is mandatory (the course's table):**
| Comparison | Metric | Interpretation scale |
|---|---|---|
| Two means | Cohen's d | 0.2 small / 0.5 medium / 0.8 large |
| Shares | OR (odds ratio), RR | > 1 — the odds/risk is higher by that many times |
| Categories (tables) | Cramér's V | 0–1, the strength of the association |

A course example: n = 10,000, a difference of 0.1 pp, p < 0.001, d = 0.05 — statistically "significant", gives the business nothing.

Always report: the test, the p-value, the **effect size** and the **confidence interval** (for a share ±1.96·SE, "whiskers" on the chart). A p-value without an effect size is half the truth: on large samples even a negligible difference is significant; on small ones, a significant one is absent.

**Three steps of processing:** present the fact ("80% of zoomers chose the option without communication"); interpret ("what it means"); discuss (link it with other data, propose new hypotheses). Example: if 80% don't want to communicate, but those who did communicate give high ratings — the problem is probably in the *beginning* of the dialogue, not in communication itself. The success of a study is not only a description of percentages and means but also explanation and new hypotheses.

**Causality:** a regular one-off survey does not prove "A influences B". For the effect of a feature you need an experiment (an A/B with a control) or a comparison with a control group; a "before and after" comparison without a control mixes effect and time (season, promotions). An example of faulty logic: comparing satisfaction "before" and "after" without accounting for changes in the group.

### 6. Visualizing results
**The "3-B" rule: Bold** (one accent color for the key series, the rest muted), **Brief** (one chart — one message, ≤ 5–7 series), **Beautiful** (even labels, CVD-safe colors, no 3D or shadows — cleanliness = trust).

| Data | Chart |
|---|---|
| Shares (yes/no, top-2) | a 100% stacked bar + a confidence interval with "whiskers" (±1.96·SE) |
| 3–7 categories | a horizontal bar, sorted descending, numbers right on the bars |
| 8+ categories | a Pareto (bars + a cumulative % line): focus on the "top 80%" |
| Likert scales | a 100% stacked bar (polarization is visible); a heatmap at 5+ questions |
| Means | a box-plot or error-bar with a CI |
| Cohorts/dynamics | a heatmap sorted by date; color chaos kills the insight |

Anti-patterns: a pie chart with > 5 sectors; 3D and "donuts"; two Y axes with different scales; a red-green palette (inaccessible to colorblind people); a heatmap without a legend. The chart title states the conclusion ("67% choose delivery — +6 pp vs last year"), not a description ("a chart of shares").

**Story dashboard: Headline → Context (method, sample, date) → Main chart → Support (segments, details) → Action** ("we are rebuilding the onboarding of step 3").

## Template / checklist

**Survey specification:**
| Field | Fill in |
|---|---|
| Decision and business metric | |
| Hypotheses (type; theoretical → empirical → statistical) | |
| Population and on whom we extend the conclusions | |
| Variables, scales, operationalization | |
| Object of comparison (null measurement, control) | |
| Sampling strategy, n, error, buffer, quotas | |
| Recruiting channel and incentive | |
| Quality control (pilot, traps, timer) | |
| Analysis plan: tests, effect, intervals | |
| Decision criterion (threshold) and next step | |

**Launch checklist:** hypotheses are linked to the goal; questions are checked for clarity and the absence of leading; scales are labeled; a pilot has been run; n is computed for the required precision *per each subgroup*; the data exclusion plan is fixed; the method of analysis is specified; consent and personal data protection are ensured.

## Typical mistakes
- A causal conclusion from a correlation or from a single survey; trusting the "why?" question.
- Unoperationalized concepts; double-barreled and leading questions; questions with negations; provoking the "right" answer.
- The mean of an ordinal scale taken as an "exact number"; a mean without a distribution; comparing means without a test.
- No null measurement: "NPS became 40" without a base for comparison.
- Conclusions about "everyone" from a sample of one channel; self-selection bias; ignoring those who did *not* answer.
- The sample is computed but subgroups, the design effect and the losses to rejection are not accounted for.
- Skipping the pilot; a questionnaire that is too long — low completion and fatigue.
- Multiple comparisons without corrections; hunting for significance after collection.
- Statistical significance mistaken for practical importance; ignoring confidence intervals.
- "Paired" data analyzed as independent (power is lost).

## Questions that can change the decision
- What do we want to prove: the existence of a relationship, a difference, or a causal effect (an experiment is needed)?
- What precision does the decision need (±5 pp or is ±10 enough) and what does the extra precision cost?
- Are conclusions by segments needed (each segment is its own sample)?
- Is there an external source of truth to cross-check against (analytics, sales)?
- Can we run an A/B instead of a survey, to measure behavior rather than declarations?
- Are the analytical skills in the team sufficient, or is a statistician needed?

## Related maps
[[M-research-types]], [[M-brief-hypotheses]], [[M-audience-research]], [[M-loyalty-metrics]], [[M-marketing-research]], [[M-in-depth-interviews]], [[M-interview-analysis]], [[M-market-sizing]], [[M-product-metrics]], [[M-source-criticism]], [[M-usp]]
