---
id: M-genai-assistant-architecture
lang: en
title: GenAI assistant as a product system — components, LLM-limit mitigations, orchestration and agent patterns
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [research, options, strategy, validation]
tags: [genai, llm, assistant, agent, orchestration, guardrails, rag, structured-output, memory, tools]
related: [M-genai-product-development, M-genai-prototyping, M-ai-in-research, M-risks, M-solution-design, M-delivery, M-decision-daci, M-team]
---

# GenAI assistant as a product system

## When to apply
When you need to design not "a single prompt" but a working assistant or agent inside a product: which components
make up the system, how to neutralize LLM limitations, when a fixed scenario (workflow) is enough and when an
autonomous agent is justified. The course's main takeaway: the model is responsible for reasoning; the result is
decided by what is built around it. An assistant is a managed product system, not a prompt.

## Core idea

**A single model call** is stateless: it does not act (text stays text), does not remember (every call starts from
scratch), does not know your product. An **agent** is a system of an LLM and a harness, able to solve a task with a
high degree of autonomy: multiple steps and calls, session state and memory, tool calls, a cost unknown upfront.

**Separating the terms:** *context* — what goes into the model right now (instructions, tools, recent messages,
retrieved documents, call results); *memory* — what persists between steps and sessions (task state, facts about the
user, actions taken) and is stored outside the model, in the service's database; *knowledge* — information shared by
all users about the domain (regulations, a catalog), with an owner and an update process. Knowledge and memory are
delivered to the model by placing the needed information into the context.

**System components** (the composition is dictated by the scenario: the more autonomous the agent, the costlier the
harness): model; system prompt (role, rules, format, a ban on leaving the data); programmatic harness (calls,
retries, limits, error handling, the agent loop); orchestrator (decomposition, routing, step order, result
assembly); tools (reading — safe; search — quality depends on the knowledge base; action — needs limits and
confirmation); structured output by schema (structured output: the answer becomes data → branching, metrics,
validation, less room for making things up); interface (you can see what the system is doing and at which step; you
can stop it or ask again); control (limits on amounts and the number of actions, human confirmation on expensive
steps, logs and incident review).

**LLM limitations and where they come from:** the model produces plausible text, not truth → hallucinations;
knowledge is frozen at the training date → obsolescence; sampling during generation → nondeterminism and sensitivity
to wording; an instruction lowers the probability of an unwanted answer but does not exclude it → behavior is
checked on the output, not only set on the input; rewarding "agreeable" answers during training → verbosity and
sycophancy; a change of model version → behavior drift.

## Procedure

### 1. Fill in the assistant canvas (top-down, model last)
| # | Field | Question |
|---|---|---|
| 01 | Task | What work does the system take away from a human? |
| 02 | Boundaries | What does it do on its own and what only with a human (amounts, topics, cases)? |
| 03 | Orchestrator | What steps does the work consist of, when to stop and escalate (step limit)? |
| 04 | Tools | What does it read and what does it change in other systems? |
| 05 | Knowledge | What domain knowledge is needed, who owns it and updates it? |
| 06 | Memory | What to remember between steps and sessions? |
| 07 | Interface | Where does the human see the work and can intervene? |
| 08 | Control | Limits, metrics, error cost, stop conditions? |
| 09 | Model | What is required of the model for all of this to work? |
Record missing data in a field as a stated assumption, not a silent guess.

### 2. Close every limitation with a specific mitigation
| Limitation | How it shows up for the user | Mitigations |
|---|---|---|
| Hallucinations | a confident fact that does not exist | grounding: retrieval over a knowledge base (RAG) and passing fragments into the context; requiring quotes/links to a source; structured output with validation; the rule "no data in the source — say so directly or refuse"; automatic check of the answer before it is issued; escalation to a human in complex cases |
| Limited knowledge | does not know your data or events after training | knowledge delivered via context/tools; an owner and a knowledge-base update process before assembly |
| Nondeterminism | "flickering" verdicts, different selections | verdicts and sensitive decisions — with deterministic rules; the model — with wording; rerun on a regression set at every change |
| Wording sensitivity / version drift | after a model update the behavior changed | regression set: a fixed sample, the same evaluation method, a run at every model/prompt change; comparison with the previous version (paired, blind) |
| Injections via data | external content (a web page, a document, a message) tries to change the instructions | separating instructions and data (marking blocks, the system prompt kept apart); content from external sources is processed as data, not as commands; restrict the list of available actions |
| Latency | "it hung", repeated clicks, leaving the chat | streaming; short input; a reranker picks 3–5 snippets of 200–400 tokens instead of whole documents; compressing the dialogue history instead of truncating it from the start; key content at the start and end of the context |
| Cost | the feature fails unit economics after a pilot | caching of repeats and stable prefixes; fewer calls per step; a model cascade fast→strong ([[M-genai-product-development]]); per-user limits |

### 3. Design the scenario: workflow or agent
A **workflow** is a pre-described order of a multi-step scenario (the orchestrator keeps state and transitions,
nodes perform operations). An **agent** plans the next step itself as the work proceeds. Workflow for tasks that
decompose into clear stages: predictable, controllable, debuggable. Agent for open-ended tasks where the steps and
their number are unknown upfront: flexible, but costlier, slower, errors accumulate — needs limits and thorough
testing.

**Five workflow patterns (and when each fits):**
| Pattern | When to choose it | Costs / risks |
|---|---|---|
| Chain | sequential dependent steps with a known order | each step is a call and a wait; an error in an early step propagates further |
| Routing | different input types need different branches; simple requests go to a cheap fast branch | a classification error sends the request to the wrong branch; the branches must be maintained |
| Parallelization | independent subtasks or several independent attempts | all branches are paid for; the results may contradict each other — reconciliation is needed |
| Orchestrator-workers | the subtask set is determined dynamically per request | the result depends on the quality of the decomposition; the amount of work is unpredictable; if the subtasks are known upfront, a fixed workflow is simpler |
| Evaluator-optimizer | the result can be improved by clear criteria | every iteration is calls, latency, money; stop conditions are mandatory |

The patterns do not exclude each other: different parts of one scenario can be built differently. Rule: if the task
is solved by a single prompt — do not complicate; task first, patterns later.

**Four agent patterns (and when they are justified):**
| Pattern | Mechanics | When it is justified |
|---|---|---|
| ReAct (reasoning + acting) | alternating "thought → action → observation", the result of each step determines the next | search and diagnostics: the path to the answer is not known upfront |
| Reflection (+ Reflexion with an error memory) | draft → check against criteria (the same model / a separate evaluator / an external tool) → refinement up to an attempt limit | the answer is verifiable and improvable by explicit criteria |
| Plan-and-Execute | a planner builds a multi-step plan, an executor carries it out, the plan is revised | the task can be split into subtasks upfront |
| Multi-agent | a lead agent delegates subtasks to specialized agents and assembles the result | several independent subtasks with different data/tools |

### 4. Set the boundaries of autonomy
1. Separate: rules set by developers / decisions of the model / actions of a human.
2. For system actions — limits (amount, number of operations, available tools) and human confirmation on expensive
   steps. A common healthy boundary: part of the cases closes automatically, the rest go to a human with a ready
   analysis — there is no need to strive for 100% automation.
3. For loops — completion conditions and an attempt limit, otherwise refinement may continue endlessly.
4. Define control metrics: share of auto-closures, escalations, repeat requests, complaints after an answer, cost
   per answer.

## Template / checklist

**"Do you need an agent" checklist:** are the steps and transitions known upfront? → workflow. Does the result
depend on data that must be searched along the way? → ReAct. Are there explicit quality criteria for the answer? →
Reflection. Does the task split into sequential subtasks? → Plan-and-Execute. Are there several large independent
subtasks? → multi-agent. None of these — a single prompt.

**Assembly checklist:** every canvas field has content or an assumption; verdicts are deterministic; hallucination
defenses are in place (grounding/citations/validation); retries and limits exist; structured output is validated;
the interface shows the steps; human confirmation on expensive actions; logs are saved for incident review; a
regression set exists and is run on every model/prompt change.

## Typical mistakes
| Mistake | Why it is bad | How to avoid it |
|---|---|---|
| Treating the prompt as the product | The harness is responsible for the result, not the model | The 9-field canvas + components |
| Believing an instruction will exclude the unwanted answer | A ban lowers the probability but does not eliminate it | Check the output: validation, filters, escalation |
| Giving verdicts and sensitive decisions to the model | "Flickering" behavior undermines trust | Rules for verdicts, the model for wording |
| Putting everything into the context (the whole regulation, the whole correspondence) | Cost and TTFT grow, the important is lost in the middle | Snippets, rerank, history compression, key content at the edges |
| One call where a scenario is needed; an agent where a workflow suffices | Either it does not solve the task, or extra cost and risk | The "workflow vs agent" algorithm above |
| Evaluator-optimizer without criteria and an attempt limit | Iterations without improvement, an endless loop | Criteria before launch; stop conditions |
| No regression set when the model version changes | Users notice the behavior drift first | A fixed sample + the same measurement at every change |
| Action tools without limits and confirmations | The system performs irreversible actions on its own | Limits, human confirmation, logs |
| Letting it forget: outdated knowledge in the base | The model confidently answers from a dead regulation | Knowledge owner, an update process |

## Questions that can change the decision
- What is the cost of an error and which system actions are irreversible? This sets the boundaries of autonomy and
  how mandatory control is.
- Are the regulation/knowledge base the assistant is built on actually valid, and do they have an owner?
- Can users try to "re-educate" the system via messages (injections) — and which actions are allowed to it?
- Is a fixed workflow enough? Every extra step is time, money and a new source of error.
- What must stay stable between runs (verdicts, amounts, links) and how do you verify that?

## Related maps
[[M-genai-product-development]], [[M-genai-prototyping]], [[M-ai-in-research]], [[M-risks]], [[M-solution-design]], [[M-delivery]], [[M-decision-daci]], [[M-team]]
