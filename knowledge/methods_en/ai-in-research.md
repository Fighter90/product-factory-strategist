---
id: M-ai-in-research
lang: en
title: AI in research — what to delegate, risks, validation, and categories of tools
course: ux
sources: ["EN mirror of the RU methodology card M-ai-in-research (knowledge/methods/ai-in-research.md); original sources are listed in the RU card"]
stages: [intake, research, options, validation]
tags: [ai, llm, prompting, rag, context-engineering, assistants, hallucinations, validation, tools]
related: [M-synthetic-respondents, M-interview-analysis, M-in-depth-interviews, M-ux-backlog, M-research-types, M-source-criticism, M-brief-hypotheses, M-quant-methods]
---

# AI in research

## When to use
When you need to speed up research routine (transcription, first-pass coding, drafts of guides and hypotheses, search across the interview base),
but keep the quality of conclusions. The main takeaway of the lesson: AI answers must be checked against your own data, otherwise it is just
beautiful text. The course deliberately places AI after the topics on session design and data storage: without a basic understanding of the
method you cannot evaluate the quality of a model's output.

## Core idea
LLMs demonstrate three abilities of "intelligence": seeing patterns, predicting, building models — but without facts in the context window
they fill the gaps with plausible fiction. Hence the key practice is **context engineering**: feeding the model source data and constraining
it by that data.

- **Basic prompt:** `[Role] + [Task] + [Context/details] + [Format/constraints]`. Seven rules: clarity and brevity; a role; context
  (goal, constraints, audience); the format of the result; step-by-step instructions for complex tasks; examples; delimiters and structure.
- **Reasoning models:** they "think" through steps internally, go to external sources, and show what they relied on. The prompt for them is
  shorter and more precise; long role instructions and "first do this, then that" can get in the way. The advantage: from the chain of
  reasoning and the sources you can see the cause of an error and remove an unsuitable source or fix the query.
- **Three layers of context:** System (role and rules, read first), Session (the task and clarifications), Extended (excerpts from the
  interview base, tickets, metrics).
- **RAG (retrieval-augmented generation):** find relevant chunks → pass them into the prompt → generate the answer based on them. Example
  parameters from the lesson: chunks of about 800 tokens, embeddings, similarity threshold ~0.75, top-5 chunks; a chunk over 2000 tokens is
  truncated; without metadata the search pulls in irrelevant material; PDF scans without a text layer yield nothing. "Context is more
  expensive than tokens": better to spend an hour cleaning the data.
- **Assistant:** model + system prompt + knowledge base (+ tools). For analyzing specific interviews, web access is better disabled
  (otherwise "outliers" from the outside world); for a market overview — enabled. Internal company data must not be uploaded to external
  services without the security team's permission.

## Procedure

### 1. Decide what to delegate
| Task | Delegate to AI? | Condition |
|---|---|---|
| Audio/video transcription | Yes | Spot-check against the recording; verify names and terms |
| First-pass coding of open-ended answers | Yes, with a closed tag list | Forbid new tags; "no suitable tag" is an allowed answer; a person re-checks part of the answers |
| Summarizing interviews | Yes | Every claim with a quote and a timecode/file reference |
| Draft of the interview/test guide, hypotheses, research questions | Yes | The researcher edits; check for leading questions |
| Turning a vague request ("let's improve onboarding") into research questions and hypotheses | Yes, as a draft | The team checks completeness: is every "where it breaks — why" covered |
| Finding patterns in a corpus | Yes, as assistance | A claim is confirmed in at least N quotes, verified manually |
| Clustering ideas/sticky notes | Yes | A human approves the groups |
| Market and competitor overview | Yes, with web access | Links to sources, verification of key facts ([[M-source-criticism]]) |
| Formulating the final insight and recommendation | No — draft only | The decision and responsibility stay with a human |
| Estimating prevalence, demand, willingness to pay, segment size | **No** | Only data from real respondents and statistics |
| Playing the role of a respondent (synthetic users) | Only per [[M-synthetic-respondents]] | Labeled as such, never as proof |
| Judging emotions "from text" as fact | Carefully | An emotion is a hypothesis until there is video/voice/observation |
| Working with personal data | Only inside the internal perimeter | Consent, anonymization |

### 2. Choose the model and mode
A short precise task → a reasoning model with a simple prompt. To compare quality — run one task on a reasoning model and the same task on a
regular LLM and compare (the course's teaching technique: two cases — "low engagement with a new feature" and "a vague onboarding" — are
solved on different models to see the difference in research planning). Turn web access on/off consciously; check the context limits (tokens,
file size) in the service documentation — a reliable trick: ask the model itself about its limits or look at the official table. In assistant
builders, distinguish the UI wrapper (quickly assemble and share) from programmatic access via API (versioning, logs, control) — the latter is
needed when the assistant is part of a process, not a one-off toy.

### 3. Assemble the context
Prepare the sources: clean texts (not scans), metadata (date, segment, method, respondent without PII). Split large files into parts.
At least three heterogeneous sources for an assistant (interviews, tickets, analytics). System prompt: role, a prohibition on going beyond
CONTEXT, the answer format, and the requirement of quotes with the file name.

### 4. Request with an evidence format
Require: claim → verbatim quote → file/position → confidence level; "if the data is insufficient — say so"; keep "fact from the source" and
"the model's interpretation" separate.

### 5. Verify (validation is mandatory)
1. Every quote exists in the source (search the text).
2. A human re-checks a sample (the card's guideline: 10–20% of claims, more for critical conclusions).
3. Re-run with a different wording/model; analyze the discrepancies.
4. For coding — double-coding of part of the answers and a comparison (the share of matches).
5. Look at the "reasoning" and the list of sources; find and remove an irrelevant source.
6. Conclusions the model stated without a quote — downgrade to hypotheses.

### 6. Save the result with provenance
In the knowledge base ([[M-ux-backlog]]) record what was produced with AI involvement: model, date, prompt version, source files, who verified.

## Template / checklist

**Prompt template for tagging (from the lesson, adapted):**
```
### TASK
Tag the open-ended answer, choosing tags ONLY from the list. If nothing fits — "no matching tags".
### CONTEXT
You are a feedback analysis assistant. Rely only on the text of the answer.
### ANSWER STRUCTURE
Table: answer | tag | brief justification (quote from the answer)
### TAG LIST
["interface","bugs","price","discount"]
```

**Tool categories (from the course list; names are examples as of the date of compilation — check current availability and regional access):**
general-purpose chat LLMs (ChatGPT, Claude, Gemini, Qwen, DeepSeek, GigaChat, YandexGPT); LLMs with web search and sources (Perplexity);
image generation and editing; "chat with tables/data" (CSV/Excel); presentations; diagrams and mind maps (Napkin, Mermaid, draw.io, Markmap);
video avatars; no-code automation (n8n, Activepieces); AI-enabled IDEs; transcribers (Fireflies, tl;dv, local services); assistant builders
with a knowledge base (GPTs, Gems, Dify, NotebookLM, Spaces). An assistant = system prompt + (optionally) a knowledge base + (optionally) tools.

**Checklist "can this AI output be used":** links to sources exist; quotes verified; no prevalence estimates without data; discrepancies across
re-runs explained; the "produced with AI" note preserved; no PII left the perimeter.

## Common mistakes
| Mistake | Consequence | Fix |
|---|---|---|
| Accepting an output without sources | Fiction in the report | Require quotes and verify them |
| Loading 50 pages into the window | Expensive and gets truncated | Chunking, search over the base |
| Chunks too large, no metadata | Facts lost, noise | Slicing, tags, metadata |
| Indexing scans | Empty text | Text recognition beforehand |
| Web access enabled while analyzing your own interviews | "Outliers" from the external world | Disable it |
| Long role prompts for reasoning models | Worse results | Keep it short and specific |
| Open tags instead of a closed list | Impossible to aggregate | Closed list |
| AI as a "respondent" without a label | Substituting evidence | See [[M-synthetic-respondents]] |
| Internal data in an external service | Leak | Internal perimeter or anonymization |
| Presenting a model's output as the result of the research | Loss of responsibility | A human signs the conclusion |

## Questions that can change the decision
- What data (interviews, tickets, metrics) exists, and can it be passed to the model? If not — drafts and templates only.
- What counts as evidence in the final document? If only respondent data — AI is limited to an auxiliary role.
- What is the cost of an error in the conclusion (a marketing hypothesis or an investment decision)? That determines the share of manual verification.
- Is a reproducible process needed (prompt version, model, date) for audit purposes?
- Which tools are allowed in the organization?

## Related maps
[[M-synthetic-respondents]], [[M-interview-analysis]], [[M-in-depth-interviews]], [[M-ux-backlog]], [[M-research-types]], [[M-source-criticism]], [[M-brief-hypotheses]], [[M-quant-methods]]
