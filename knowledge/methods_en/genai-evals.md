---
id: M-genai-evals
lang: en
title: Evaluating the quality of LLM features (LLM evals) — golden set, LLM-as-judge, guardrails and degradation monitoring
course: pm-approaches-en
sources: ["Hamel Husain — Your AI Product Needs Evals (https://hamel.dev/blog/posts/eval/)", "Zheng et al. — Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena (https://arxiv.org/abs/2306.05685)", "Shankar et al. — Who Validates the Validators? (https://arxiv.org/abs/2404.12272)", "Eugene Yan — Patterns for Building LLM-based Systems & Products, the Evals section (https://eugeneyan.com/writing/llm-patterns/)"]
stages: [options, validation]
tags: [ai, llm, evals, golden-set, llm-as-judge, guardrails, degradation, regression-suite, human-annotation]
related: [M-genai-prototyping, M-genai-product-development, M-ab-testing, M-product-metrics]
---

# LLM evals: measuring the quality of an LLM feature before and after release

## When to apply
An LLM feature is designed ([[M-genai-feature-patterns]]) and possibly verified on a prototype ([[M-genai-prototyping]]) —
you need a repeatable way to measure quality on every change (prompt, model, RAG, cascade) before release and on live
traffic after release. The prototype answers "is the quality achievable at all"; evals are the permanent control loop: the LLM
is non-deterministic and degrades unnoticed (rotation of API model versions, traffic drift). "I looked at a few answers —
it got better" is not a measurement; without evals the feature is unmanageable.

## Core idea

**Trust hierarchy: human annotation > a calibrated LLM-as-judge > automatically computed proxies.**

1. **Golden set.** A fixed sample of real examples — random, without cleaning, with hard cases (missing data,
   contradictions, rare formats) and unacceptable cases (injection attempts, provocations). Hundreds, not
   a handful; the version of the set is fixed; it does not change between runs — otherwise the comparison of runs is meaningless.
2. **Regression suite.** Every change of prompt, model or architecture = a full run of the golden
   set with the inputs, outputs and step history saved; a comparison with the previous run. A change without a regression run
   is degradation without witnesses.
3. **Human annotation.** People define what quality is; everything else is an approximation.
   The order: reading and notes in free text ("what is wrong", in your own words) → a yes/no checklist derived from the notes → a binary
   "acceptable / not acceptable" with a threshold named before the run; for comparing versions — a blind pairwise comparison ("did it get better";
   the better of two may still be bad).
4. **LLM-as-judge.** A strong model grades the answers of the feature against a rubric — it scales the grading between human
   rounds. Mandatory calibration: on a sample with human annotation, measure the agreement with humans;
   randomize the order in pairwise comparisons; check the known biases — a preference for long answers,
   self-preference (the judge prefers answers produced by the same model), position effects.
5. **Guardrails.** Checks on input (injections, forbidden topics, format validation) and on output
   (structure per schema, forbidden content, fact-checking against product data). Unacceptable errors: zero in the run and
   a hard filter/refusal at runtime; verdicts with a high cost of error go to rules, not to the model.
6. **A/B against regression (the online check).** The old path vs the LLM feature on live traffic: the target metric +
   counter-metrics (complaints, manual edits, returns, the share of refusals). An LLM feature is not an improvement by default — it
   must win the measurement ([[M-ab-testing]]).
7. **Degradation monitoring.** Canary examples on live traffic; answer logging with sampled grading (judge or
   human); alerts on the fall of the acceptable share, the growth of refusals, cost and latency; complaints and the "thumbs down"
   of the user are a source of new errors for the next version of the golden set.

## How to do it
1. Fix the verbal acceptance criterion ("a good answer = …"), the list of unacceptable errors and the threshold of the acceptable share —
   everything before the first run.
2. Assemble the golden set: a random sample of real inputs + hard + unacceptable cases; fix the version;
   do not change it between runs.
3. Wire the regression run into the process: any change = a run + a comparison with the previous one; an error breakdown by sources
   (assembly / data / specification / model).
4. Set up the annotation: a human reads a sample of the run and fills the checklist; then calibrate the LLM-as-judge against
   the human annotation (agreement, order randomization, a self-preference test); the judge is for intermediate
   runs, a human — for release ones.
5. Build the guardrails: unacceptable cases in a separate run; input and output filters; verdicts go to rules; refusal
   when data is missing.
6. After release: an A/B against the old path on the metric and counter-metrics; monitoring (canary, logs, sampled grading,
   alerts); new errors from logs and complaints go back into the next version of the golden set.

## Pitfalls
- **An uncalibrated judge.** The judge model is biased: long answers seem better, its own seem better, the order in a pair matters.
  A judge without comparison against human annotation — you are optimizing the taste of the model, not the quality of the product.
- **Gaming the set and the threshold.** "Typical cases", data cleaning and a threshold named after looking at the results
  inflate the score. A random sample, the threshold — before the run.
- **A single number without a breakdown.** "87% acceptable" does not say what to fix: you need a breakdown by the checklist items and
  a classification of the error sources.
- **Degradation after release.** Model version rotation and traffic drift change behavior unnoticed; without monitoring
  you will learn about it from the users. Canary + alerts + logs with sampled grading — the mandatory minimum.
- **The cost and privacy of evals.** A run of hundreds of examples on a strong model costs money — count the price of a run; a judge
  makes the annotation cheaper. Logging real conversations for grading — personal data: masking, rights, retention
  periods. Guardrails do not replace the measurement: a filter hides the symptom but does not fix the generation.

## Connections
The methods are born in the prototype — [[M-genai-prototyping]]; what to measure and the cost of error — [[M-genai-feature-patterns]]; the
"Quality evaluation" stage of the life cycle — [[M-genai-product-development]]; the online check — [[M-ab-testing]]; product
metrics and counter-metrics — [[M-product-metrics]].
