---
id: M-genai-feature-patterns-en
title: AI Feature Patterns — taxonomy, error cost, and UX mitigations
course: pm-approaches-en
sources: ["EN summary of the RU methodology card; original sources listed in the RU card"]
stages: []
tags: [en, summary]
related: []
---

# AI Feature Patterns (EN summary)

**When:** GenAI in a feature is already justified and you must choose how it embeds into the product: what the system does alone vs. with a human, what the error cost is, and which UX patterns reduce that cost. The core rule: the pattern follows the task and the error cost, not the hype around agents — each step up in autonomy multiplies both value and control requirements.

**Core:** Six patterns in rising autonomy/value/control order. (1) Autocorrect/background — silently improves what the user made (typos, wording, tags, smart completions); cheap errors, but no intrusiveness. (2) Generation (draft-first) — creates content the user reads and edits; invented facts are unacceptable. (3) Classification/extraction — unstructured → labels/structure (moderation, ticket routing, enrichment); errors surface as systemic noise in metrics. (4) Chat assistant (Q&A) — open-ended questions; needs grounding (RAG) and honest refusals — a confident wrong answer is worse than "I don't know". (5) Copilot — proposes steps/edits inside an expert workflow, human accepts; review mandatory. (6) Agent — multi-step tool-using work that changes data; highest value and error cost: limits, human confirmation on critical steps, stop control. Three selection rules: start with the minimal sufficient pattern (most "agent" work works as a copilot or draft); error cost × reversibility (reversible → draft-first, costly but visible → review, irreversible → no autonomous action without human confirmation); the pattern dictates requirements (latency for interactive patterns, logs/limits for agents, grounding for Q&A). UX mitigations: draft → review by default (nothing generated leaves the product without a human until the low error cost is proven); confidence display (show it's AI, show sources/basis, flag low confidence to a human); fallback/escalation to a human instead of inventing — refusal is an answer; undo and history; streaming with visible progress and a stop button.

**How:** measure the error cost (who notices, how reversible, list unacceptable errors) → pick the minimal sufficient pattern and check whether autonomy can be lowered (agent → copilot → draft) → design UX mitigations for that cost (review, sources, escalation, undo) → set boundaries (what it never does; high-stakes verdicts go to rules and humans, not the model) → pre-release regression run on a golden set plus feature metrics (accepted drafts, post-AI manual edits, time-to-result) → online A/B against the old path on the target metric and counter-metrics.

**Pitfalls:** an agent for the agent's sake (latency, cost, and failure points multiply); hallucinations in high-stakes spots without grounding; uncounted inference cost (per-action LLM calls — cache, smaller model, cascade, event-based triggers belong to the pattern choice, not "later"); hidden latency breaks interactive patterns; privacy (agents see more user context — mask before external API calls) and silent behavior drift after model version rotation (re-run the regression).

**RU-версия:** `knowledge/methods/M-genai-feature-patterns.md` (полная методика).
