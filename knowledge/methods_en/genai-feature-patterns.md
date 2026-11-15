---
id: M-genai-feature-patterns
lang: en
title: AI feature patterns in products — a taxonomy (autocorrection → generation → classification → chat → copilot → agent), the cost of error and UX mitigations
course: ai
sources: ["EN mirror of the RU methodology card M-genai-feature-patterns (knowledge/methods/genai-feature-patterns.md); original sources are listed in the RU card"]
stages: [options, validation]
tags: [ai, llm, feature-patterns, copilot, agent, ux-patterns, error-cost]
related: [M-genai-product-development, M-genai-prototyping, M-ab-testing, M-product-metrics]
---

# AI feature patterns: which pattern fits which task and error cost

## When to apply
GenAI in the feature is already justified (checked via [[M-genai-product-development]]) and you need to choose the form of embedding into the product: what the system does by itself, what together with a human, what the cost of error is and which UX patterns reduce it. The question of autonomy is also decided here: the modes "Answers / Helps / Acts" from the expediency map are made concrete as one of six patterns. The central rule: **the pattern is chosen from the task and the cost of error, not from fashion for agents**; each next level of autonomy multiplies both value and the requirements for control.

## Essence

**The taxonomy — six patterns** in ascending autonomy, value and requirements for control:

| Pattern | What it does | Where it fits | Cost of error |
|---|---|---|---|
| **Autocorrection (background)** | Silently improves what the user has done: typos, wording, auto-tags, smart completion | Mass repeated actions where the result is visible before saving | Low: the result is on screen, reverted in one action; intrusiveness is inadmissible |
| **Generation (draft-first)** | Creates content on request: an email, a description, an image, a summary | Creating content from scratch; the user reads and edits anyway | Low-medium: time lost on editing; fabricated facts are inadmissible |
| **Classification / extraction** | Unstructured → a label or structure: moderation, ticket categories, card enrichment, field extraction | A large flow; the user may never see the system at all | Medium-high: systemic noise (false positives) shows in metrics, not in a single answer |
| **Chat assistant (Q&A)** | Answers free-form questions: support, knowledge base | Many question variants; a short answer is cheaper than manual search | Medium-high: a confidently worded wrong answer is worse than a refusal; grounding is mandatory |
| **Copilot** | Proposes steps, edits and decisions inside the workflow; the human accepts | Expert processes: code, documents, analysis; the expert's speed matters more than saving their labor | Medium: the error is visible and fixable, but undermines trust; review is mandatory |
| **Agent** | Performs multi-step work with tools by itself and changes data | Tasks where a human cannot sit in every step: routine operations under control | High and irreversible (money, emails, publications): limits, confirmations, stop button |

**Three rules for choosing a pattern:**
- **Minimal sufficient.** Almost any "agent" task can first be given as draft generation or a copilot; an agent is the last choice, when the work is multi-step and a human physically cannot be present at every step.
- **Cost of error × reversibility.** The error is cheaply fixed by the user → draft-first is enough. The error is expensive but visible → review is mandatory (copilot). The error is irreversible (sent outward, money spent) → autonomous action is forbidden without human confirmation at critical steps.
- **The pattern defines the requirements.** Interactive patterns (autocorrection, inline suggestions) do not tolerate seconds of latency; agent ones — require logs, limits and control; Q&A — grounding and an honest refusal on missing data.

**UX patterns for risk reduction** (the set of mitigations is matched to the cost of error):
1. **Draft → review**: everything generated is a draft by default; the user edits and confirms. Nothing generated leaves to the outside world without a human until a low error cost is proven by measurement.
2. **Confidence display / transparency**: show that this is AI; show the grounds ("based on these documents", links to sources); at low confidence — a "check this" signal and hand-off to a human.
3. **Fallback / escalation to a human**: on missing data, conflicting sources or low confidence, do not invent — hand off to a human or a human process. A refusal is also an answer.
4. **Undo and history**: undo, versions, "restore as it was" — lowers the cost of error for autocorrection and generation.
5. **Streaming and progress**: for generation and agents show the steps and allow stopping at any moment.

## How to do it
1. Measure the cost of error: what happens on error — who notices, how to fix, is it reversible; list the inadmissible errors (a fabricated fact, an email sent to a client, money charged).
2. Choose the minimal sufficient pattern from the table; check whether autonomy can be lowered without losing value (agent → copilot → draft).
3. Design UX mitigations for the cost of error: draft→review, showing grounds, refusal/escalation, undo; critical steps behind human confirmation.
4. Draw the boundaries: what the system does by itself, what with confirmation, what it never does; verdicts with a high error cost go to rules and humans, the model gets wording.
5. Measure before release: a regression run on the golden set ([[M-genai-prototyping]], [[M-genai-evals]]) + feature metrics (share of accepted drafts, manual edits after AI, time to result).
6. Verify in production with an A/B against the old path ([[M-ab-testing]]) on the target metric and counter-metrics: complaints, returns, manual edits.

## Pitfalls
- **An agent for the sake of an agent.** Multi-step autonomy where a draft would do: latency, cost and failure points grow multiplicatively. Start with the minimal pattern; add autonomy when the need is proven.
- **Hallucinations in "responsible" places.** Generation without grounding in product data and Q&A without sources produce confident fabrications. Mitigations: supply data, show grounds, refuse on missing data — draft→review as the norm.
- **Inference cost not counted.** An LLM call on every action (let alone every keystroke) multiplies the bill; caching, a smaller model, a cascade and event-based triggers are part of choosing the pattern, not an optimization "for later".
- **Latency not hidden.** Interactive patterns break on seconds of waiting; if the model is slow — it is the wrong pattern, or streaming, caching and precomputation are needed.
- **Privacy and degradation.** Agent patterns see more user context — check permissions and mask data before sending to an external API; a model version change alters the pattern's behavior — repeat the measurement on rotation.

## Connections
Expediency and autonomy modes — [[M-genai-product-development]]; checking quality achievability — [[M-genai-prototyping]]; measuring quality and degradation — [[M-genai-evals]]; the agent's architecture as a system — [[M-genai-assistant-architecture]]; the online check — [[M-ab-testing]]; feature metrics — [[M-product-metrics]].
