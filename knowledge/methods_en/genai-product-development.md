---
id: M-genai-product-development
lang: en
title: GenAI product — viability, lifecycle, LLM basics and model selection
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [intake, research, options, validation]
tags: [ai, llm, genai, viability, product-lifecycle, model-selection, token-costs, context-window, nondeterminism]
related: [M-genai-assistant-architecture, M-genai-prototyping, M-ai-in-research, M-mvp-pilots, M-unit-economics, M-risks, M-problem-design, M-source-criticism, M-trends-scenarios]
---

# GenAI product: when it is justified and how it is developed

## When to apply
When a product leader decides whether to build GenAI/LLM into a product or a process, how to plan such a project
(timeline, budget, stages), and which model to choose for a specific scenario. The main takeaway of the course:
generative-AI projects fail not because of models — models are plentiful — but because teams cannot formulate
the task, build a measurement, reach quality and close the economics.

## Core idea

**Three forms of GenAI in a product** (from the simplest to the most valuable): a standalone GenAI product
(without the technology it would not exist); a feature inside a product (speeds up an existing scenario or opens
a new way to solve a task); an internal process (the user never talks to the model but sees the result:
moderation, card enrichment, routing, data extraction).

**Three autonomy modes** — value and requirements grow along one scale:
| Mode | What the system does | Minimum mandatory elements |
|---|---|---|
| Answers | gives an answer; the human makes the decision | quality |
| Assists | proposes an option; the human accepts/edits it | quality + economics |
| Acts | executes steps and changes data in systems | quality + economics + safety |

**How a GenAI product differs from a classic one:** the unit of work is a task, not an operation; the interface
takes open input, with boundaries set by instructions and checks; cost is variable and grows with usage; the
product itself formulates statements the company is accountable for (a classic product only shows what was put
into it). Hence three mandatory elements of any decision — quality, economics, safety; not one of them can be
skipped.

**Technical foundations of LLMs** (the parts that shape product decisions):
- **Token** — a fragment of text (usually a subword); billing and speed are counted in tokens. A language the
  model was not built for natively (for example, Cyrillic in a tokenizer without it) is "thicker" in tokens →
  more expensive and slower.
- **Generation** — autoregression: the model predicts the next token from the context. Sampling (choosing a token
  among the likely ones; controlled by the "temperature" parameter and related settings) makes answers diverse
  but **nondeterministic**: the same query can produce different answers.
- **Context window** — everything the model sees at one step: the system prompt, tool descriptions, dialog
  history, retrieved documents, the user query, and reserve space for the answer. The user query is often the
  smallest part.
- **Latency** decomposes into TTFT (time to first token, grows with input length) and TPOT (time per generated
  token, grows under load): latency ≈ TTFT + TPOT × answer length. It can be hidden (streaming, caching,
  prefetching) but not removed.
- **Cost per query** ≈ input tokens × input price + output tokens × output price, multiplied by the number of
  calls; processing a cached prefix is cheaper.
- **Model training stages explain its defects:** pretraining gives plausibility, not truth → hallucinations and
  stale knowledge; fine-tuning on query–answer pairs → format and instruction-following; reinforcement learning
  (rewarding "good" answers) → verbosity, sycophancy, false refusals, behavior changes between versions.

## Procedure

### 1. Check whether GenAI is needed here (viability algorithm)
1. **Regulation test:** describe the process by answering four questions — what must be done, where the
   information comes from, how the decision is made, what a good result looks like. If the description works,
   the process can be automated. If it does not, the process is not built out or needs expert judgment; GenAI
   will not replace it on its own.
2. **Choose the technology for the task:** plain code — if the rules can be described exactly (a calculation,
   a conversion, format validation); classic ML — if the answer is picked from a closed list and there are
   labeled data and high volume (antifraud, ranking, forecasting); GenAI — if the system must understand or
   create unstructured content (answering a question, retelling, describing from a photo, comparing products
   in words).
3. **Check the five viability criteria:** value (how many decisions and actions are taken off humans); data
   (access, completeness, rights); expertise (is there anyone to lead the project); economics (does the effect
   beat the inference price on a rough estimate — only a prototype will show the exact price); risk (is the
   cost of an error acceptable and is the decision explainable). **Any criterion can become a stop factor** —
   no data rights, no project.
4. **Check the scale:** fixed costs (the measurement, the control loop, operations) pay off only with volume.
   Hundreds of queries per day usually means "the idea is sound, but the project is small"; tens of thousands
   — already yes.
5. Write down the list of unknowns (data, economics, constraints) and who to ask for answers.

### 2. Plan along the six-stage lifecycle
1. **Problem statement:** the formulation and the target business metric; the justification for GenAI; a
   description of the expected behavior. Gate: the task is clear, GenAI is justified, behavior is described.
2. **Data and knowledge:** sources, rights, constraints. The key difference from ML — this is not a training
   set but the knowledge fed at query time. Stale and contradictory knowledge is cleaned/labeled BEFORE the
   build, not after. Gate: sources are described, access obtained, constraints known.
3. **Prototype:** a working solution without optimizations, on the strongest model, expensive and slow —
   solely to remove the quality uncertainty (see [[M-genai-prototyping]]). Gate: the customer confirms the
   result in substance.
4. **Quality evaluation:** dissect where the prototype errs; agree on what a "good answer" is (good = moves
   the human closer to solving the task, not "more facts"); build a test set and a reproducible measurement.
5. **Tuning:** raise quality (prompt, context, external knowledge, architecture), cut cost and time, build
   the control loop. The first cost-reduction lever is the cache (does not change quality), then a smaller
   model and context compression (they do change it → a repeated measurement is needed). Gate: cost and speed
   are within limits, quality has not dropped.
6. **Operations:** quality control on live traffic, error triage; the data feeds back into the problem
   statement.

Management consequences: you cannot name a completion date — you can name the deadline for testing a
hypothesis; the budget is allocated by stages, not in full; the decision to continue is made by the
measurement, not by the plan. After the prototype there are three honest outcomes: develop / refine (it is
clear which lever to try) / close — closing before large investments is a success.

### 3. Choose the model by the "criteria → matrix → cascade" algorithm
1. **Set five product criteria and their weights for the scenario:** quality (share of acceptable answers on
   your own task); cost (price per 1k input and output tokens × volume); latency (TTFT/TPOT and the scenario's
   requirement — moderation and inline suggestions cannot wait seconds); privacy (can data be passed to an
   external provider — personal and sensitive data stay inside your own perimeter); stability (version control,
   degradations, rotation; determinism of critical parts).
2. **Fill in the matrix of four axes:** modality (what goes in and out; understanding and generation are
   different abilities); specialization (search/embedder, reranker, moderation classifier, generative answer —
   the pipeline is almost always several models); architecture (encoder — "read it all and issue a verdict":
   classification, search, rerank, embeddings; decoder — text generation; MoE and reasoning mode change
   price/speed at the same "size", so the total parameter count is a poor proxy); openness (closed, via API —
   usually stronger, but data goes to the vendor and there is no version control; open weights — your own
   perimeter, fine-tuning, control, but you need your own hosting and attention to the license).
3. **Take a fast→strong cascade:** on small models (tens of milliseconds, cheap) — classification, routing,
   first-pass filtering; on medium ones — knowledge-base answers, summarization; on large ones (seconds,
   expensive) — complex reasoning, multi-step scenarios, dispute triage. Rule: an "unsolvable" verdict on a
   task is issued only on the strongest available model — otherwise two questions are mixed (the task cannot
   be solved, or the model was not strong enough).
4. **Do not fine-tune until it is proven:** the default path is a ready model + instructions + knowledge in
   context. Fine-tuning is justified when: there is a stable narrow format/domain, the contextual approach
   consistently fails to reach the required quality even with the context squeezed, there are data for
   training and a team for maintenance. A fine-tuned small model can beat a larger one on a narrow task —
   that is a cost-reduction path, not the first step.

## Template / checklist

**Model selection matrix:**
| Scenario | Modality (input→output) | Specialization | Architecture | Open/closed | Criteria: quality / price / latency / privacy / stability |
|---|---|---|---|---|---|
| … | … | classifier / embedder / reranker / generation | encoder / decoder / MoE / reasoning | … | … |

**Viability checklist:** the process is described; the task requires unstructured input/output; the five
criteria are checked and none is a stop factor; volume covers the fixed costs; the deadline is framed as a
"deadline for testing the hypothesis"; the budget is staged; the gate criteria of each stage are written down.

**Feature economics (order of magnitude before the prototype):** `query price ≈ (input_tokens × input_price +
output_tokens × output_price)`; `month = query price × volume × 30`; then the scenarios "+4k tokens of
retrieved fragments", "a larger model", "prefix cache" — to see a range, not a single number.

## Typical mistakes
| Mistake | Why it is bad | How to avoid it |
|---|---|---|
| Using GenAI where code or classic ML suffices | More expensive, slower, needlessly nondeterministic | Step 1 of the algorithm: choose the technology by task type |
| Planning a completion date before the experiment | Whether quality is attainable is unknown until tested on your data | A hypothesis-testing deadline; budget by stages |
| Optimizing cost before quality is confirmed | Optimizing an unproven approach is a double risk | The strongest model on the prototype; cost-cutting at the tuning stage |
| Starting cost-cutting with "a smaller model" | It changes quality → a full repeated measurement is needed | Start with the cache and context compression |
| Choosing a model by parameter count or leaderboard | Parameters ≠ speed/price/quality on your task | The matrix + a measurement on your own sample |
| Sending personal and sensitive data to an external API | Leakage, violation of rights | Privacy as a criterion: your own perimeter or masking before sending |
| Concluding "the task cannot be solved" from a weak model | Unattainability is not proven | The cascade: a verdict only on the strongest model |
| Giving a deterministic verdict (reliability, tolerance) to the model | The answer "flickers" between runs | Verdicts belong to rules; the model gets phrasing and explanations |

## Questions that can change the decision
- What is the cost of one wrong answer, and who is accountable for a statement generated by the product?
- Can the data (personal data, documents, photos) be passed to an external provider — or is your own perimeter required?
- What is the volume of queries/requests per day: will it cover the measurement, the control loop and operations?
- Does the scenario require an instant response? If yes, GenAI either does not fit, or an architecture with
   precomputed results is needed.
- Which parts of the behavior must be deterministic, and which may vary?

## Related maps
[[M-genai-assistant-architecture]], [[M-genai-prototyping]], [[M-ai-in-research]], [[M-mvp-pilots]], [[M-unit-economics]], [[M-risks]], [[M-problem-design]], [[M-source-criticism]], [[M-trends-scenarios]]
