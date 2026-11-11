---
id: M-genai-feature-patterns
lang: en
title: AI feature patterns in products — a taxonomy (autocorrect → generation → classification → chat → copilot → agent), the error cost and UX mitigations
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [options, validation]
tags: [ai, llm, feature-patterns, copilot, agent, ux-patterns, error-cost]
related: [M-genai-product-development, M-genai-prototyping, M-ab-testing, M-product-metrics]
---

# AI feature patterns: which pattern fits which task and which error cost

## When to apply
GenAI in the feature is already justified (verified via [[M-genai-product-development]]) and you need to choose the form of embedding into the product: what the system does on its own, what it does together with a human, what the error cost is, and which UX patterns reduce it. This is also where the autonomy question is settled: the "Answers / Assists / Acts" modes from the justification card are made concrete as one of the six patterns. The central rule: **the pattern is chosen from the task and the error cost, not from the fashion for agents**; every next level of autonomy multiplies both the value and the requirements for control.

## Core idea

**The taxonomy — six patterns**, in rising order of autonomy, value and control requirements:

| Pattern | What it does | Where it fits | Error cost |
|---|---|---|---|
| **Autocorrect (background)** | Silently improves what the user has made: typos, wording, auto-tags, smart completion | Mass repeated actions where the result is visible before saving | Low: the result is on screen and can be rejected with one action; intrusiveness is unacceptable |
| **Generation (draft-first)** | Creates content on request: an email, a description, an image, a summary | Creating content from scratch; the user reads and edits it anyway | Low–medium: lost time on editing; invented facts are unacceptable |
| **Classification / extraction** | Unstructured → a label or structure: moderation, ticket categories, card enrichment, field extraction | A large flow; the user may never see the system at all | Medium–high: systemic noise (false positives) shows up in the metrics, not in a single answer |
| **Chat assistant (Q&A)** | Answers free-form questions: support, a knowledge base | Many possible phrasings of the question; a short answer is cheaper than manual search | Medium–high: a confidently worded wrong answer is worse than a refusal; grounding is mandatory |
| **Copilot** | Proposes steps, edits and decisions inside the workflow; the human accepts | Expert processes: code, documents, analysis; the expert's speed matters more than saving their effort | Medium: the error is visible and fixable, but it undermines trust; review is mandatory |
| **Agent** | Performs multi-step work with tools on its own and changes data | Tasks where a human cannot sit inside every step: routine operations under control | High and irreversible (money, emails, publications): limits, confirmations, a stop control |

**Three rules for choosing a pattern:**
- **Minimal sufficient.** Almost any "agent" task can be delivered first as a draft generation or a copilot; the agent is the last-resort choice, made when the work is multi-step and a human physically cannot be present in every step.
- **Error cost × reversibility.** The error is cheaply fixed by the user → draft-first is enough. The error is costly but visible → review is mandatory (copilot). The error is irreversible (something was sent out, money was spent) → autonomous action is forbidden without human confirmation on the critical steps.
- **The pattern defines the requirements.** Interactive patterns (autocorrect, inline suggestions) cannot tolerate seconds of latency; agent ones require logs, limits and control; Q&A requires grounding and an honest refusal when data is missing.

**UX patterns for reducing risk** (the set of mitigations is matched to the error cost):
1. **Draft → review**: everything generated is a draft by default; the user edits and confirms. Nothing generated leaves for the outside world without a human, until the low error cost has been proven by measurement.
2. **Confidence display / transparency**: show that this is AI; show the grounds ("based on these documents", links to the sources); at low confidence — a "check this" signal and a hand-off to a human.
3. **Fallback / escalation to a human**: when data is missing, sources conflict, or confidence is low, do not invent — hand off to a human or a human process. A refusal is also an answer.
4. **Undo and history**: undo, versions, "restore as it was" — it lowers the error cost of autocorrect and generation.
5. **Streaming and progress**: for generation and agents, show the steps and allow the user to stop at any moment.

## How to do it
1. Measure the error cost: what happens when an error occurs — who will notice, how it can be fixed, whether it is reversible; list the unacceptable errors (an invented fact, an email sent to a client, money charged).
2. Choose the minimal sufficient pattern using the table; check whether autonomy can be lowered without losing value (agent → copilot → draft).
3. Design the UX mitigations for the error cost: draft→review, showing the grounds, refusal/escalation, undo; the critical steps go behind human confirmation.
4. Draw the boundaries: what the system does on its own, what it does with confirmation, what it never does; verdicts with a high error cost go to rules and humans — the model handles the wording.
5. Measure before release: a regression run on the golden set ([[M-genai-prototyping]], [[M-genai-evals]]) + the feature's metrics (the share of accepted drafts, manual edits after the AI, time to result).
6. Check in production with an A/B test against the old path ([[M-ab-testing]]) on the target metric and counter-metrics: complaints, returns, manual edits.

## Pitfalls
- **An agent for the agent's sake.** Multi-step autonomy where a draft would have sufficed: latency, cost and failure points grow by multiples. Start with the minimal pattern; add autonomy once the need has been proven.
- **Hallucinations in "high-stakes" places.** Generation without grounding in product data, and Q&A without sources, produce confident fabrications. Mitigations: supply the data, show the grounds, refuse when data is missing — draft→review as the norm.
- **The inference cost was not counted.** An LLM call on every action (all the more on every keystroke) multiplies the bill; caching, a smaller model, a cascade and event-based triggers are part of choosing the pattern, not an optimization "for later".
- **The latency is not hidden.** Interactive patterns break under seconds of waiting; if the model is slow, either the pattern is the wrong one, or you need streaming, caching and precomputation.
- **Privacy and degradation.** Agent patterns see more of the user's context — check permissions and mask the data before sending it to an external API; a model version change alters the pattern's behavior — repeat the measurement at every rotation.

## Connections
Justification and autonomy modes — [[M-genai-product-development]]; checking that quality is achievable — [[M-genai-prototyping]]; measuring quality and degradation — [[M-genai-evals]]; the architecture of an agent as a system — [[M-genai-assistant-architecture]]; the online check — [[M-ab-testing]]; feature metrics — [[M-product-metrics]].
