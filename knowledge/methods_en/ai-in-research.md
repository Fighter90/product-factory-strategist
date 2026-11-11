---
id: M-ai-in-research
lang: en
title: AI in research — what to delegate, risks, validation and tool categories
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [intake, research, options, validation]
tags: [ai, llm, prompting, rag, context-engineering, assistants, hallucinations, validation, tools]
related: [M-synthetic-respondents, M-interview-analysis, M-in-depth-interviews, M-ux-backlog, M-research-types, M-source-criticism, M-brief-hypotheses, M-quant-methods]
---

# AI in research

## When to apply
When you need to speed up research routine (transcription, first-pass coding, drafts of guides and hypotheses, search across the interview base) while keeping the quality of the conclusions. The session's main takeaway: AI answers must be checked against your own data, otherwise it is just pretty text. The course deliberately places AI after the topics on session design and data storage: without a basic understanding of the method you cannot judge the quality of a model's output.

## Core idea
LLMs demonstrate three "intelligence" abilities: seeing patterns, predicting, building models — but without facts in the context window they fill the gaps with plausible fiction. Hence the key practice — **context engineering**: feed the model the source data and constrain it with that data.

- **Base prompt:** `[Role] + [Task] + [Context/details] + [Format/constraints]`. Seven rules: clarity and brevity; role; context (goal, constraints, audience); output format; step-by-step instructions for complex tasks; examples; delimiters and structure.
- **Reasoning models:** "think" through steps internally, go out to external sources, and show what they relied on. The prompt for them is shorter and more precise; long role instructions and "first do this, then that" can get in the way. The advantage: the chain of reasoning and the sources show why an answer went wrong, and you can remove an unsuitable source or fix the query.
- **Three layers of context:** System (role and rules, read first), Session (the task and clarifications), Extended (extracts from the interview base, tickets, metrics).
- **RAG (retrieval-augmented generation):** retrieve relevant chunks → pass them into the prompt → generate the answer from them. Example parameters from the session: chunks of about 800 tokens, embeddings, similarity threshold ~0.75, top-5 chunks; a chunk over 2000 tokens gets truncated; without metadata search pulls in irrelevant content; scanned PDFs without a text layer yield nothing. "Context costs more than tokens": it is better to spend an hour cleaning the data.
- **Assistant:** model + system prompt + knowledge base (+ tools). For analyzing specific interviews, web access is better switched off (otherwise "outliers"); for a market overview — switched on. Do not upload internal company data to external services without the security team's approval.

## Procedure

### 1. Decide what to delegate
| Task | Delegate to AI? | Condition |
|---|---|---|
| Audio/video transcription | Yes | Spot-check against the recording; verify names and terminology |
| First-pass coding of open answers | Yes, with a closed tag list | Forbid new tags; "no fitting tag" is an allowed answer; a human re-checks part of the answers |
| Interview summarization | Yes | Every thesis with a quote and a timecode/file reference |
| Draft of an interview/test guide, hypotheses, research questions | Yes | The researcher edits it; check for leading questions |
| Converting a vague request ("improve onboarding") into research questions and hypotheses | Yes, as a draft | The team checks completeness: are all the "where it breaks — why" points covered |
| Pattern search across the corpus | Yes, as assistance | A claim is supported in at least N quotes and verified manually |
| Clustering ideas/sticky notes | Yes | A human approves the groups |
| Market and competitor overview | Yes, with web access | Links to sources, verification of key facts ([[M-source-criticism]]) |
| Formulating the final insight and recommendation | No — draft only | The decision and the responsibility stay with a human |
| Estimating prevalence, demand, willingness to pay, segment size | **No** | Only data from real respondents and statistics |
| Playing the respondent (synthetic users) | Only per [[M-synthetic-respondents]] | Labeled, never used as proof |
| Judging emotions "from text" as fact | With care | An emotion is a hypothesis until there is video/voice/observation |
| Working with personal data | Internal perimeter only | Consent, anonymization |

### 2. Choose the model and mode
A short precise task → a reasoning model with a simple prompt. To compare quality — run one task on a reasoning model and the same task on a regular LLM, then compare (the course's teaching device: two cases — "low engagement of a new feature" and "a vague onboarding" — are solved on different models so you can see the difference in research planning). Switch web access on and off deliberately; check the context limits (tokens, file size) in the service's documentation — a reliable trick: ask the model itself about its limits or look at the official table. In assistant builders, distinguish the UI wrapper (quick to assemble and share) from programmatic access via API (versioning, logs, control) — the latter is needed when the assistant is part of a process, not a one-off toy.

### 3. Assemble the context
Prepare the sources: clean texts (not scans), metadata (date, segment, method, respondent without PII). Split large files into parts. A minimum of three heterogeneous sources for an assistant (interviews, tickets, analytics). System prompt: the role, a ban on stepping outside CONTEXT, the answer format, the requirement of quotes with the file name.

### 4. Request output in an evidence format
Require: thesis → verbatim quote → file/position → confidence level; "if the data is insufficient — say so"; keep "fact from the source" and "model interpretation" separate.

### 5. Verify (validation is mandatory)
1. Every quote exists in the source (search the text).
2. Human re-check of a sample (the card's guideline: 10–20% of theses, more for critical conclusions).
3. Rerun with a different phrasing/model; reconcile the discrepancies.
4. For coding — double-code part of the answers and compare (the share of matches).
5. Inspect the "reasoning" and the source list; find and remove the irrelevant source.
6. Conclusions the model stated without a quote — downgrade to hypotheses.

### 6. Save the result with provenance
In the knowledge base ([[M-ux-backlog]]) record what was produced with AI involvement: model, date, prompt version, source files, who verified.

## Template / checklist

**Prompt template for tagging (from the session, adapted):**
```
### TASK
Tag the open answer, choosing tags ONLY from the list. If nothing fits — "no fitting tags".
### CONTEXT
You are a feedback-analysis assistant. Rely only on the text of the answer.
### ANSWER STRUCTURE
Table: answer | tag | short rationale (a quote from the answer)
### TAG LIST
["interface","bugs","price","discount"]
```

**Tool categories (from the course list; the names are examples as of the time of compilation — check current relevance and regional availability):**
general-purpose chat LLMs (ChatGPT, Claude, Gemini, Qwen, DeepSeek, GigaChat, YandexGPT); LLMs with web search and sources (Perplexity); image generation and
editing; "chat with tables/data" (CSV/Excel); presentations; diagrams and mind maps (Napkin, Mermaid, draw.io, Markmap); video avatars;
no-code automation (n8n, Activepieces); AI-powered IDEs; transcribers (Fireflies, tl;dv, Russian services); assistant builders with a knowledge
base (GPTs, Gems, Dify, NotebookLM, Spaces). An assistant = system prompt + (optionally) a knowledge base + (optionally) tools.

**Checklist "can an AI output be used":** there are links to the sources; quotes have been verified; it contains no prevalence estimates without data; the discrepancies across reruns have been explained; the "produced with AI" label has been kept; no PII has left the perimeter.

## Typical mistakes
| Mistake | Consequence | Fix |
|---|---|---|
| Accepting output without sources | Fiction in the report | Require quotes and verify them |
| Loading 50 pages into the window | Costly and gets truncated | Chunking, search over the base |
| Chunks too large, no metadata | Facts lost, noise | Slicing, tags, metadata |
| Indexing scans | Empty text | Text recognition in advance |
| Web access enabled while analyzing your own interviews | "Outliers" from the outside world | Disable it |
| Long role prompts for reasoning models | Worse result | Short and specific |
| Open tags instead of a closed list | Impossible to aggregate | Closed list |
| AI as a "respondent" without a label | Evidence substitution | See [[M-synthetic-respondents]] |
| Internal data in an external service | Leak | Internal perimeter or anonymization |
| Presenting a model's output as the research result | Lost responsibility | A human signs off the conclusion |

## Questions that can change the decision
- Which data (interviews, tickets, metrics) exists, and can it be passed to the model? If not — drafts and templates only.
- What should count as evidence in the final document? If only respondent data — AI is limited to a supporting role.
- What is the price of an error in a conclusion (a marketing hypothesis or an investment decision)? It determines the share of manual verification.
- Is a reproducible process needed (prompt version, model, date) for audit?
- Which tools are allowed in the organization?

## Related maps
[[M-synthetic-respondents]], [[M-interview-analysis]], [[M-in-depth-interviews]], [[M-ux-backlog]], [[M-research-types]], [[M-source-criticism]], [[M-brief-hypotheses]], [[M-quant-methods]]
