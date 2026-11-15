---
id: M-genai-assistant-architecture
lang: en
title: A GenAI assistant as a product system — components, mitigations of limitations, orchestration and agent patterns
course: ai
sources: ["EN mirror of the RU methodology card M-genai-assistant-architecture (knowledge/methods/genai-assistant-architecture.md); original sources are listed in the RU card"]
stages: [research, options, strategy, validation]
tags: [ai, llm, assistant, agent, orchestration, guardrails, rag, structured-output, memory, tools, agent-patterns]
related: [M-genai-product-development, M-genai-prototyping, M-ai-in-research, M-risks, M-solution-design, M-delivery, M-decision-daci, M-team]
---

# A GenAI assistant as a product system

## When to apply
When you need to design not "a single prompt" but a working assistant or agent inside a product: which components make up the system, how to neutralize LLM limitations, when a fixed scenario (workflow) is enough and when an autonomous agent is justified. The course's main conclusion: the model is responsible for reasoning; the result is determined by what is built around it; an assistant is a managed product system, not a prompt.

## Essence

**A single model call** — stateless: it does not act (text remains text), does not remember (every call starts from scratch), does not know your product. **An agent** — a system of an LLM and surrounding machinery able to solve a task with a high degree of autonomy: multiple steps and calls, session state and memory, tool calls, cost not known in advance.

**Delineating concepts:** *context* — what goes into the model right now (instruction, tools, recent messages, retrieved documents, call results); *memory* — what persists between steps and sessions (task state, facts about the user, actions taken) and is stored outside the model, in the service's database; *knowledge* — information shared by all users about the domain (policies, catalog), with an owner and an update process. Knowledge and memory are delivered to the model by placing the needed information into the context.

**System components** (the scenario dictates the composition: the more autonomous the agent, the more expensive the machinery): the model; the system prompt (role, rules, format, a ban on leaving the data); software plumbing (calls, retries, limits, error handling, the agent loop); the orchestrator (decomposition, routing, step order, assembling the result); tools (reading — safe; retrieval — quality depends on the knowledge base; action — needs limits and confirmation); structured output per schema (structured output: the answer becomes data → branching, metrics, validation, less room for fabrication); the interface (you can see what the system does and at which step; you can stop it or ask again); control (limits on amounts and number of actions, human confirmation on expensive steps, logs and incident review).

**LLM limitations and their origins:** the model generates plausible text, not truth → hallucinations; knowledge is frozen at the training date → staleness; sampling during generation → nondeterminism and sensitivity to wording; an instruction lowers the probability of an unwanted answer but does not exclude it → behavior is checked at the output, not only set at the input; rewarding "agreeable" answers during training → verbosity and sycophancy; a model version change → behavior drift.

## Procedure

### 1. Fill in the assistant canvas (top to bottom, model last)
| # | Field | Question |
|---|---|---|
| 01 | Task | What work does the system take away from a human? |
| 02 | Boundaries | What does it do on its own and what only with a human (amounts, topics, cases)? |
| 03 | Orchestrator | Of which steps does the work consist, when to stop and escalate (a step limit)? |
| 04 | Tools | What does it read and what does it change in systems? |
| 05 | Knowledge | Which domain knowledge is needed, who owns it and updates it? |
| 06 | Memory | What to remember between steps and sessions? |
| 07 | Interface | Where can a human see the work and intervene? |
| 08 | Control | Limits, metrics, cost of error, stop conditions? |
| 09 | Model | What is required of the model for all of this to work? |
Record missing data in a field as an assumption rather than silently assuming.

### 2. Close every limitation with a concrete mitigation
| Limitation | How it manifests for the user | Mitigations |
|---|---|---|
| Hallucinations | a confident fact that does not exist | grounding: retrieval over the knowledge base (RAG) and passing fragments into context; requiring quotes/links to the source; structured output with validation; the rule "no data in the source — say so or refuse"; automatic answer check before delivery; escalation to a human in complex cases |
| Limited knowledge | it does not know your data or events after training | knowledge via context/tools; an owner and refresh of the knowledge base before assembly |
| Nondeterminism | "flickering" verdicts, different selections | verdicts and sensitive decisions — deterministic rules; the model — wording; re-run on the regression set at every change |
| Sensitivity to wording / version drift | after a model update the behavior changed | a regression set: a fixed sample, the same evaluation method, a run at every model/prompt change; comparison with the previous version (paired, blind) |
| Injections through data | external content (a web page, a document, a message) tries to change the instructions | separating instructions and data (marking blocks, system prompt separate); treat data from external sources as data, not commands; restrict the list of available actions |
| Latency | "it hangs", repeated presses, chat abandonment | streaming; short input; a reranker selects 3–5 snippets of 200–400 tokens instead of whole documents; compressing conversation history instead of trimming from the start; the key content — at the beginning and end of the context |
| Cost | the feature fails the economics after the pilot | caching of repeats and the stable prefix; fewer calls per step; a fast→strong model cascade ([[M-genai-product-development]]); per-user limits |

### 3. Design the scenario: workflow or agent
**Workflow** — a pre-described order of a multi-step scenario (the orchestrator holds state and transitions; nodes perform operations). **An agent** — plans the next step itself as work proceeds. Workflow for tasks decomposable into understandable stages: predictable, controllable, debuggable. Agent for open-ended tasks where the steps and their number are unknown in advance: flexible, but more expensive, slower, errors accumulate — needs limits and thorough testing.

**Five workflow patterns (and when each is appropriate):**
| Pattern | When to choose | Costs / risks |
|---|---|---|
| Chain | sequential dependent steps with a known order | each step is a call and a wait; an early error propagates onward |
| Routing | different input types require different branches; simple queries go to a cheap fast branch | a classification error sends to the wrong branch; branches must be maintained |
| Parallelization | independent subtasks or several independent attempts | all branches are paid for; results may contradict — reconciliation is needed |
| Orchestrator-workers | the composition of subtasks is determined dynamically per request | the result depends on the quality of decomposition; the volume of work is unpredictable; if subtasks are known in advance — a fixed workflow is simpler |
| Evaluator-optimizer | the result can be improved by understandable criteria | each iteration is calls, delay, money; stop conditions are mandatory |

The patterns do not exclude each other: different parts of one scenario can be built differently. Rule: if one prompt solves the task — do not complicate; task first, patterns second.

**Four agent patterns (and when they are justified):**
| Pattern | Mechanics | When justified |
|---|---|---|
| ReAct (reasoning + acting) | alternating "thought → action → observation"; the result of each step determines the next | search and diagnostics: the path to the answer is unknown in advance |
| Reflection (+ Reflexion with an error memory) | draft → check against criteria (the same model / a separate judge / an external tool) → refinement up to an attempt limit | the answer is checkable and improvable by explicit criteria |
| Plan-and-Execute | a planner builds a multi-step plan, an executor performs it, the plan is revised | the task can be pre-split into subtasks |
| Multi-agent | a lead agent delegates subtasks to specialized agents and assembles the result | several independent subtasks with different data/tools |

### 4. Set the boundaries of autonomy
1. Separate: developer-defined rules / model decisions / human actions.
2. For system actions — limits (amounts, number of operations, available tools) and human confirmation on expensive steps. A normal healthy boundary: part of the cases closes automatically, the rest go to a human with a prepared breakdown — there is no need to strive for 100% automation.
3. For loops — completion conditions and an attempt limit, otherwise refinement can continue forever.
4. Define control metrics: share of auto-closures, escalations, repeat contacts, complaints after an answer, cost per answer.

## Template / checklist

**Checklist "is an agent needed":** are steps and transitions known in advance? → workflow. Does the result depend on data that must be retrieved along the way? → ReAct. Are there explicit criteria of answer quality? → Reflection. Does the task split into sequential subtasks? → Plan-and-Execute. Are there several large independent subtasks? → multi-agent. None of these — a single prompt.

**Assembly checklist:** every canvas field has content or an assumption; verdicts are deterministic; hallucination protection exists (grounding/quotes/validation); retries and limits exist; structured output is validated; the interface shows the steps; human confirmation on expensive actions; logs are kept for incident review; a regression set exists and is run on every model/prompt change.

## Typical mistakes
| Mistake | Why it is bad | How to avoid |
|---|---|---|
| Treating a prompt as the product | The plumbing is responsible for the result, not the model | The 9-field canvas + components |
| Believing an instruction will exclude an unwanted answer | A ban lowers probability but does not exclude | Output checks: validation, filters, escalation |
| Giving the model verdicts and sensitive decisions | "Flickering" behavior undermines trust | Rules for verdicts, the model for wording |
| Putting everything into context (the whole policy, the whole correspondence) | Cost and TTFT grow, the important gets lost in the middle | Snippets, reranking, history compression, key content at the edges |
| A single call where a scenario is needed; an agent where a workflow suffices | Either the task is not solved, or needless cost and risks | The "workflow vs agent" algorithm above |
| Evaluator-optimizer without criteria and an attempt limit | Iterations without improvement, an endless loop | Criteria before launch; stop conditions |
| No regression set on a model version change | Users notice the behavior drift | A fixed sample + the same measurement at every change |
| Action tools without limits and confirmations | The system performs irreversible actions on its own | Limits, human confirmation, logs |
| Letting knowledge go stale in the base | The model confidently answers per a dead policy | A knowledge owner, an update process |

## Questions that can change the decision
- What is the cost of one error, and which system actions are irreversible? This sets the boundaries of autonomy and the mandatory controls.
- Are the policy/knowledge base the assistant is built on correct and current, and is there an owner?
- Can users try to "re-educate" the system via messages (injections) — and which actions are allowed to it?
- Is a fixed workflow enough? Every extra step is time, money and a new source of error.
- What must stay stable between runs (verdicts, amounts, references) and how is that checked?

## Related maps
[[M-genai-product-development]], [[M-genai-prototyping]], [[M-ai-in-research]], [[M-risks]], [[M-solution-design]], [[M-delivery]], [[M-decision-daci]], [[M-team]]
