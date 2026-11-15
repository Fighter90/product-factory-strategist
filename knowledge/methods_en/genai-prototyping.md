---
id: M-genai-prototyping
lang: en
title: Designing, building and testing a GenAI prototype — from a scenario to a build decision
course: ai
sources: ["EN mirror of the RU methodology card M-genai-prototyping (knowledge/methods/genai-prototyping.md); original sources are listed in the RU card"]
stages: [options, validation]
tags: [ai, llm, prototype, golden-set, regression, metrics, acceptance-criterion, prototyping-tools, sample]
related: [M-genai-product-development, M-genai-assistant-architecture, M-mvp-pilots, M-quant-methods, M-usability-testing, M-benchmarking, M-unit-economics, M-risks, M-solution-design]
---

# A GenAI prototype: design it, build it, test it

## When to apply
When the solution is designed ([[M-genai-assistant-architecture]]) and you need to check in days, not weeks, the main thing — whether the required quality is achievable on your data — and decide: develop, refine or shut down. A prototype is a source of knowledge about the task, not the first version of the product: "it works for the competitor" does not substitute for the check, because they have different data, load and audience.

## Essence

**The four tasks of a prototype**, one of them the main one: the image of the solution (how this will work — partially replaceable by a mockup); value (does the user need it — verified by interviews and behavior analytics, the prototype gives signals, not statistics); **quality achievability — checked by nothing except a prototype**; the order of magnitude of cost (not a number for the budget: downward, cost falls with optimizations; upward, it grows from long dialogues and repeat contacts).

**Requirements for the check (without them the result cannot be trusted):** validity — the sample is taken at random from real data, the model is the strongest available; interpretability — you can see in which cases and why it failed; speed — days, the deadline named before the start; cost of the check — a fraction of the development cost. The typical failure: three weeks on 15 hand-picked examples and the conclusion "we can launch" — three of the four requirements violated.

**Scope:** the main scenario — in full (the product is being made for its sake); real data — without cleaning (cleaning inflates the result); typical AND hard cases; the strongest model (separates "unsolvable" from "the model is weak"); a simple build tool; no speed optimizations, failure handling or tidy code. Run results are saved — otherwise versions cannot be compared.

**Tools** differ in what you must do to get a result: a chat with the model (feel out the prompt, understand whether the model copes in principle); a sandbox/console (system prompt and parameters separate, tool declarations, code export — but it will not run the function itself); an assistant builder (a standing instruction + your files, an internal helper; cannot be embedded into your own product); an app generator (the image of the solution and checking with live users, but a run over a sample must be built separately); a visual scenario platform (a workflow of blocks, a run over the sample with the history of every step — exactly what is needed to check achievability); code (everything is possible, but edits go through a developer). Selection criteria: is a run over a sample needed, your own interface, speed of learning, who on the team can assemble it.

## Procedure

### 1. Write the prototype task specification (before building)
| # | Section | What is fixed |
|---|---|---|
| 01 | Input | trigger (when it fires), data, user query |
| 02 | Output | format (coherent text for a human / structure for the interface); mandatory elements of every answer — the basis of the acceptance criterion |
| 03 | Data sources | what the system reads in addition to the input (internal services, reference books, the web); the more sources, the harder the build |
| 04 | Behavior rules | what it never asserts; what it does on missing data (say so outright or refuse); what it does not reason about without clarification |
| 05 | Acceptance criterion | a verbal description of an acceptable answer; who accepts (product manager + experts); what counts as failure |

The specification trap: describing form, not substance. "There is a recommendation" is fulfilled literally and uselessly ("take the first one" without an argument). A requirement is worded so that it cannot be fulfilled meaninglessly: "the recommendation rests on the differences named in the answer, every claim is backed by listing data, there are no fabricated facts".

### 2. Build minimally
1. The basic scheme: trigger → model call (system prompt + input) → answer. A scenario adds input validation, a second call or a field-by-field answer; agent logic — per the patterns from [[M-genai-assistant-architecture]].
2. The run over a sample must be built into the tool's mechanics: data between steps is passed as a list of items — every node processes every item, no loop needs writing. The prompt is assembled from expressions over table fields.
3. Roles (even in a group of 3–4 people): the builder (workflow, screen), the prompt author, the tester (brings varied examples and notices bad answers), the presenter. Build errors are visible immediately (it crashes / it is silent), quality errors — only on varied examples.
4. Technical hygiene of the run: a single item's failure does not stop the run (error handling "continue"); the run history keeps the input and output of every node; the answer is written back into the sample's row (run column), the score — into the neighboring one (eval column); the sample does not change between measurements.

### 3. Test: the algorithm
1. **Scenarios:** extract from the specification the main scenario and hard cases (missing data, contradictory data, incomparable pairs) — these are the test situations.
2. **Golden set:** a fixed sample of real examples (hundreds, not a handful), taken at random, not cleaned, with hard cases; stored and unchanged between runs.
3. **Regression run:** full processing of the golden set by the current version; answers and step histories saved. Any change of prompt/model/architecture = a rerun of the same set.
4. **Quality annotation** (read first, count later):
   - free-text notes — always first, on the first 20–30 answers: what is wrong in your own words ("invented a characteristic that does not exist", not "bad");
   - checklist — yes/no questions, items taken from the notes (are the differences backed by data? does the recommendation rest on the differences? are there no fabricated facts?); gives a picture of "what to fix", not a single number;
   - binary annotation "acceptable/not" — once the acceptance criterion is formulated; the threshold is named BEFORE the run (a share set after viewing = fitting);
   - paired blind comparison — "did it get better" against the current user experience or the previous version; the better of two may still be bad.
5. **Metrics of three kinds:** quality (the share of acceptable by binary annotation + the breakdown by checklist items + zero inadmissible errors); cost (the price of an answer by input/output tokens and number of calls; the check "does it also work out on the cheapest model at the same volume?"); latency (answer time on the sample, TTFT/TPOT from observable figures).
6. **Find the source of every bad error** — questions in order, from the cheap check to the expensive one:
   | Question | Where to look | If no |
   |---|---|---|
   | Did the data reach the model? | run history, the model call's input | assembly (expressions, field parsing) |
   | Is the answer in the data themselves? | the original example | data (the missing-data rule, an external source) |
   | Does the prompt ask for what the user needs? | the prompt read literally | specification (requirements, rules for hard cases) |
   | All of the above is fine and the answer is still bad | — | model (simplify/split the task, an example of a good answer, a verification step, a stronger model) |
   Frequent traps: rewriting the prompt when the model simply did not receive the data; demanding from the model an answer that is not in the data (it will invent one); changing the model when the prompt is fulfilled literally; declaring the task unsolvable on a weak model.
7. **Decide the prototype's fate** — questions in order:
   - the acceptance criterion is met (the share of acceptable ≥ the threshold, no inadmissible errors)? → **develop**: engineering with the lessons learned, the remaining errors handed over as known risks;
   - among the errors there are fixable ones (assembly, data, specification)? → **refine**: a plan "what we change / how we check / when we stop" — one error source per iteration, the same run on the same sample, the threshold and the iteration limit named before the first run;
   - the errors are only model-level, checked on the strongest model and with a changed architecture? → **shut down**: record why. This is a completed answer about achievability obtained in weeks, not a failure.
   Economics decides independently of quality: if even on the cheapest model an answer costs more than the product is willing to pay — shut down. If it works out — the price is cut during refinement; it does not change the decision. The threshold is not raised after the run.

## Template / checklist

**Prototype specification:** trigger; input data; output format + mandatory elements; sources; behavior rules on missing data; the verbal acceptance criterion; who accepts; what counts as failure; the deadline (in days).

**Run checklist:** the sample is random from real data; hard cases included; the model is the strongest available; a failure does not stop the run; answers saved into the run column; step history available for analysis; the sample unchanged between runs.

**Decision checklist:** annotation done after reading the answers; the threshold named before the run; error sources classified (assembly/data/specification/model); cost counted, including on the cheapest model; latency measured; the decision (develop/refine/shut down) recorded with grounds.

## Typical mistakes
| Mistake | Why it is bad | How to avoid |
|---|---|---|
| A prototype as the first version of the product | Three weeks of work get dragged to production together with the crutches | The prototype is thrown away; engineering starts with the lessons learned |
| Hand-picking "nice" examples | The result cannot be trusted | A random sample from real data |
| Cleaning data before the run | Inflates the result: in production the data will be dirty | A run on the data as they are |
| "It works for the competitor" as proof | Different data, load, audience | Your own prototype on your own data |
| Computing a metric before reading the answers | They measure what is easy to count, not what breaks | Text notes → checklist → binary annotation |
| An acceptance threshold set after viewing results | Fitting to the result | The threshold and iteration limit named before the run |
| One number "82 out of 100 acceptable" | It does not say what to fix | A breakdown by checklist items + classification of error sources |
| Fixing everything at once | It is unclear what worked | One error source per iteration, the same run |
| Polishing the prototype beyond the acceptance criterion "to perfection" | Prompt refinement does not carry into the product: it has a different architecture | Criterion met → develop; the remainder — known risks |
| The conclusion "unsolvable" on a budget model | "The task is unsolvable" and "the model is weak" are mixed | A verdict of unachievability — only on the strongest model |

## Questions that can change the decision
- Can the process be described in a specification (input/output/rules/criterion)? If not — building is premature; task design first.
- What is the sample size, and are there hard cases in the data? Dozens of examples do not answer the achievability question.
- Does the economics work out on the cheapest model at full volume? If not — quality will not save it.
- Which errors are inadmissible in principle (a fabricated fact, a wrong verdict) and is there zero of them in the run?
- How does the prototype differ from the future product (architecture, data volume, load), and what of the lessons carries over?

## Related maps
[[M-genai-product-development]], [[M-genai-assistant-architecture]], [[M-mvp-pilots]], [[M-quant-methods]], [[M-usability-testing]], [[M-benchmarking]], [[M-unit-economics]], [[M-risks]], [[M-solution-design]]
