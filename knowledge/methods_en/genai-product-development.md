---
id: M-genai-product-development
lang: en
title: A GenAI product — expediency, lifecycle, LLM fundamentals and model selection
course: ai
sources: ["EN mirror of the RU methodology card M-genai-product-development (knowledge/methods/genai-product-development.md); original sources are listed in the RU card"]
stages: [intake, research, options, validation]
tags: [ai, llm, genai, expediency, lifecycle, model-selection, token-cost, context-window, nondeterminism]
related: [M-genai-assistant-architecture, M-genai-prototyping, M-ai-in-research, M-mvp-pilots, M-unit-economics, M-risks, M-problem-design, M-source-criticism, M-trends-scenarios]
---

# A GenAI product: when it is justified and how it is developed

## When to apply
When a product leader decides: whether to build GenAI/LLM into a product or process, how to plan such a project (timeline, budget, stages) and which model to pick for a specific scenario. The course's main conclusion: generative-AI projects fail not because of the models — there are plenty of models — but because teams cannot formulate the task, build a measurement, reach quality and make the economics work.

## Essence

**Three forms of GenAI in a product** (from the simplest to the most valuable): a standalone GenAI product (without the technology it would not exist); a feature inside a product (speeds up an existing scenario or opens a new way to solve a task); an internal process (the user never talks to the model but sees the result: moderation, card enrichment, routing, data extraction).

**Three autonomy modes** — value and requirements grow on the same scale:
| Mode | What the system does | Minimal mandatory elements |
|---|---|---|
| Answers | gives an answer, the decision stays with the human | quality |
| Helps | proposes an option, the human accepts/edits | quality + economics |
| Acts | performs steps and changes data in systems | quality + economics + safety |

**How a GenAI product differs from a classical one:** the unit of work is a task, not an operation; the interface has open input, boundaries are set by instructions and checks; the cost is variable and grows with usage; the product formulates by itself the claims the company is answerable for (a classical product only shows what was put into it). Hence the three mandatory elements of any solution — quality, economics, safety; none can be skipped.

**The technical basis of LLMs** (what affects product decisions):
- **Token** — a fragment of text (usually a subword); billing and speed are counted in tokens. A non-native language for the model (e.g. Cyrillic in a tokenizer without it) is "thicker" in tokens → more expensive and slower.
- **Generation** — autoregression: the model predicts the next token from the context. Sampling (choosing a token among the probable ones; controlled by the "temperature" parameter and related settings) makes answers diverse but **nondeterministic**: the same request can yield different answers.
- **Context window** — everything the model sees at a step: system prompt, tool descriptions, conversation history, retrieved documents, the user's query, a reserve for the answer. The user's query is often the smallest part.
- **Latency** decomposes into TTFT (time to first token, grows with input length) and TPOT (time per generated token, grows under load): latency ≈ TTFT + TPOT × answer length. It can be hidden (streaming, cache, preloading), not removed.
- **Cost of a request** ≈ input tokens × input price + output tokens × output price, multiplied by the number of calls; processing a cached prefix is cheaper.
- **The stages of model training explain its defects:** pretraining gives plausibility, not truth → hallucinations and stale knowledge; fine-tuning on prompt–answer pairs → format and instruction following; reinforcement learning (rewarding "good" answers) → verbosity, sycophancy, false refusals, behavior change between versions.

## Procedure

### 1. Check whether GenAI is needed here (the expediency algorithm)
1. **The policy test:** describe the process in four questions — what must be done, where information is taken from, how the decision is made, what a good result looks like. If the description came out → the process is automatable. If not → the process is not structured or an expert judge is needed; GenAI will not replace it on its own.
2. **Choose the technology for the task:** ordinary code — if the rules can be described exactly (calculation, conversion, format check); classical ML — if the answer is chosen from a closed list and there are labeled data and a large flow (anti-fraud, ranking, forecasting); GenAI — if unstructured content must be understood or created (answering a question, summarizing, describing from a photo, comparing products in words).
3. **Check the five expediency criteria:** value (how many decisions and actions are taken off the human); data (access, completeness, rights); expertise (is there anyone to lead the project); economics (does the effect cover the cost per request on a rough estimate — the exact price is only revealed by a prototype); risk (is the cost of error acceptable and is the decision explainable). **Any criterion can become a stop factor** — no rights to the data, no project.
4. **Check the scale:** fixed costs (measurement, the control loop, operations) pay off only with volume. Hundreds of requests a day is usually "a working idea but a small project"; tens of thousands — already yes.
5. Record the list of unknowns (data, economics, constraints) and whom to ask for answers.

### 2. Plan by the six-stage lifecycle
1. **Task setting:** the formulation and target business metric; justification of GenAI; a description of the expected behavior. Transition: the task is clear, GenAI is justified, behavior described.
2. **Data and knowledge:** sources, rights, constraints. The key difference from ML — this is not a training set but knowledge supplied at the moment of the request. Stale and contradictory knowledge is cleaned/annotated BEFORE assembly, not after.
   Transition: sources described, access obtained, constraints known.
3. **Prototype:** a working solution without optimizations, on the strongest model, expensive and slow — solely to remove the uncertainty about quality (see [[M-genai-prototyping]]). Transition: the customer confirms the result on the merits.
4. **Quality evaluation:** take apart where the prototype errs; agree on what a "good answer" is (good = moved the human closer to solving the task, not "more facts"); assemble a test sample and a reproducible measurement.
5. **Refinement:** raise quality (prompt, context, external knowledge, architecture), lower cost and time, build the control loop. The first cost lever is the cache (does not change quality), then a smaller model and context compression (they do → a re-measurement is required). Transition: cost and speed within bounds, quality has not sagged.
6. **Operations:** quality control on live traffic, error analysis; the data return into task setting.

Management consequences: a readiness date cannot be named — a hypothesis-check deadline can; the budget is allocated by stages, not as a whole; the decision to continue is made by measurement, not by plan. After the prototype there are three honest outcomes: develop / refine (it is clear which lever to try) / shut down — shutting down before major investment is a success.

### 3. Choose the model by the algorithm "criteria → matrix → cascade"
1. **Set the five product criteria and their weights for the scenario:** quality (the share of acceptable answers on your task); cost (the price per 1 thousand input and output tokens × volume); latency (TTFT/TPOT and the scenario's requirement — moderation and in-interface suggestions cannot wait seconds); privacy (may data be passed to an external provider — personal and sensitive data stay in your own perimeter); stability (version control, degradation, rotation; determinism of critical parts).
2. **Fill the matrix of four axes:** modality (what goes in/out; understanding and generation are different capabilities); specialization (retriever/embedder, reranker, classifier-moderator, generative answer — a pipeline is almost always several models); architecture (encoder — "read it whole and issued a verdict": classification, retrieval, reranking, embeddings; decoder — text generation; MoE and reasoning mode change price/speed at the same "size", so the raw parameter count is a poor proxy); openness (closed via API — usually stronger, but data goes to the vendor and there is no version control; open weights — your own perimeter, fine-tuning, control, but you need your own hosting and attention to the license).
3. **Take the fast→strong cascade:** on small models (tens of milliseconds, cheap) — classification, routing, primary filtering; on medium ones — knowledge-base answers, summarization; on large ones (seconds, expensive) — complex reasoning, multi-step scenarios, dispute resolution. Rule: "not solvable" is concluded only on the strongest available model — otherwise two questions are mixed (the task is unsolvable or the model was not enough).
4. **Do not fine-tune until proven:** the basic path — a ready model + instructions + knowledge in context. Fine-tuning is justified when: there is a stable narrow format/domain, the contextual approach consistently fails to deliver the needed quality with the context squeezed, there are training data and a team for maintenance. A fine-tuned small model can beat a larger one on a narrow task — it is a way to cut costs, not a first step.

## Template / checklist

**Model selection matrix:**
| Scenario | Modality (input→output) | Specialization | Architecture | Open/closed | Criteria: quality / price / latency / privacy / stability |
|---|---|---|---|---|---|
| … | … | classifier / embedder / reranker / generation | encoder / decoder / MoE / reasoning | … | … |

**Expediency checklist:** the policy is described; the task requires unstructured input/output; the five criteria are checked and none is a stop; the volume covers the fixed costs; the deadline is formulated as a "hypothesis-check deadline"; the budget is stage-based; the transition criteria of each stage are written down.

**Feature economics (order of magnitude before the prototype):** `request price ≈ (input_tokens × input_price + output_tokens × output_price)`; `month = request price × volume × 30`; then scenarios "+4k tokens of retrieved fragments", "a bigger model", "prefix cache" — to see a range, not a single number.

## Typical mistakes
| Mistake | Why it is bad | How to avoid |
|---|---|---|
| Taking GenAI where code or classical ML suffices | More expensive, slower, nondeterministic without need | Step 1 of the algorithm: technology choice by task type |
| Planning a readiness date before the experiment | Quality achievability is unknown until checked on your own data | A hypothesis-check deadline; a stage-based budget |
| Optimizing cost before quality is confirmed | Optimizing an unproven approach is a double risk | The strongest model on the prototype, cost cutting during refinement |
| Starting cost cutting with "a smaller model" | It changes quality → a full re-measurement is needed | Cache and context compression first |
| Choosing a model by parameter count or leaderboard | Parameters ≠ speed/price/quality on your task | The matrix + measurement on your own sample |
| Passing personal and sensitive data to an external API | A leak, rights violations | Privacy as a criterion: your own perimeter or masking before sending |
| Concluding "the task is unsolvable" from a weak model | Unachievability is not proven | The cascade: a verdict only on the strongest model |
| Giving a deterministic verdict (reliability, admission) to the model | The answer "flickers" between runs | Verdicts — to rules; the model — wording and explanations |

## Questions that can change the decision
- What is the cost of one wrong answer, and who is answerable for a claim generated by the product?
- May the data (personal data, documents, photos) be passed to an external provider — or is your own perimeter needed?
- What is the daily volume of requests: will it cover measurement, control and operations?
- Does the scenario have an instant-response requirement? If yes — GenAI either does not fit, or an architecture with precomputation is needed.
- Which parts of behavior must be deterministic, and which may vary?

## Related maps
[[M-genai-assistant-architecture]], [[M-genai-prototyping]], [[M-ai-in-research]], [[M-mvp-pilots]], [[M-unit-economics]], [[M-risks]], [[M-problem-design]], [[M-source-criticism]], [[M-trends-scenarios]]
