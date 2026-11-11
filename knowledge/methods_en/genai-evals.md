---
id: M-genai-evals
lang: en
title: LLM Evals — golden sets, LLM-as-judge, guardrails, degradation monitoring
course: pm-approaches-en
sources: ["EN summary of the RU methodology card; original sources listed in the RU card"]
stages: [options, validation]
tags: [en, summary]
related: [M-genai-prototyping, M-genai-product-development, M-ab-testing, M-product-metrics]
---

# LLM Evals (EN summary)

**When:** an LLM feature is designed and possibly prototyped — you need a repeatable way to measure quality on every change (prompt, model, RAG, cascade) before release and on live traffic after release. The prototype answers "is the quality achievable at all"; evals are the permanent quality-control loop. LLMs are non-deterministic and degrade silently (API model version rotation, traffic drift); "I skimmed a few answers, it looks better" is not a measurement.

**Core:** Trust hierarchy: human annotation > calibrated LLM-as-judge > auto-computed proxies. Golden set — a fixed, random, uncleaned sample of real examples (hundreds, not a handful) including hard cases (missing data, contradictions, rare formats) and unacceptable cases (injection attempts); version it and never change it between runs. Regression suite — every prompt/model/architecture change = a full run of the same set with inputs/outputs/step history saved, compared to the previous run; a change without a regression run is degradation without a witness. Human annotation defines quality: free-text notes ("what's wrong, in your own words") → yes/no checklist derived from the notes → binary acceptable/not with a threshold named before the run; blind pairwise comparison for version-vs-version (the better of two may still be bad). LLM-as-judge scales annotation between human rounds but must be calibrated against human labels: measure agreement, randomize comparison order, test known biases (length preference, self-preference). Guardrails: input checks (injections, forbidden topics, format) and output checks (schema, forbidden content, facts-vs-data); unacceptable errors = zero in the run plus hard filters/refusals at runtime; high-stakes verdicts go to rules, not the model. Online A/B against the old path on the target metric plus counter-metrics (complaints, manual edits, refunds, refusal rate). Degradation monitoring: canary examples on live traffic, logged answers with sampled judge/human review, alerts on acceptance-rate drops, refusals, cost and latency growth; complaints feed the next golden-set release.

**How:** fix the verbal acceptance criterion, the unacceptable-error list, and the threshold before the first run → assemble and version the golden set (random + hard + unacceptable cases) → wire the regression run into the process with an error-source breakdown (assembly/data/spec/model) → human annotation on run samples, then calibrate the judge against it (judge for intermediate runs, humans for releases) → build guardrails on unacceptable cases (filters in/out, refusals on missing data) → after release: A/B vs the old path, monitoring with alerts, and feed new errors from logs and complaints back into the golden set.

**Pitfalls:** an uncalibrated judge (you optimize the judge model's taste, not product quality); a gamed golden set or a threshold named after the results; a single number without breakdown ("87% acceptable" says nothing about what to fix); silent post-release degradation (version rotation, traffic drift — canaries + alerts + logs are the minimum); eval cost and privacy (strong-model runs over hundreds of examples cost money — count the price; logged conversations are personal data — masking, rights, retention); guardrails hide symptoms instead of fixing generation quality — they are the last line, not a replacement for measurement.
