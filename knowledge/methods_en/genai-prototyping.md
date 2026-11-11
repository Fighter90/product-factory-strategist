---
id: M-genai-prototyping
lang: en
title: Designing, building and testing a GenAI prototype — from the problem statement to the launch decision
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [options, validation]
tags: [ai, llm, prototyping, golden-set, regression-testing, acceptance-criteria, tooling, sampling]
related: [M-genai-product-development, M-genai-assistant-architecture, M-mvp-pilots, M-quant-methods, M-usability-testing, M-benchmarking, M-unit-economics, M-risks, M-solution-design]
---

# GenAI Prototype: Design, Build, Test

## When to apply
The solution has already been designed ([[M-genai-assistant-architecture]]) and you need, in days rather than weeks, to check the main thing — whether the required quality is achievable on your data — and then decide: develop it, refine it, or close it. A prototype is a source of knowledge about the task, not the first version of the product: "it works for the competitor" is no substitute for your own check, because they have different data, load and audience.

## Core idea

**The four jobs of a prototype**, only one of which is decisive: an image of the solution (how this will work — partially replaceable with a mockup); value (does the user need it — checked through interviews and behavioral analytics, the prototype gives signals, not statistics); **quality achievability — nothing but a prototype can check it**; the order of magnitude of the cost (not a figure for the budget: downward, the cost is reduced by optimizations; upward, it grows from long dialogs and repeat visits).

**The requirements for the check (without them the result cannot be trusted):** validity — the sample is taken at random from real data, the model is the strongest available; interpretability — you can see in which cases and why it did not work; speed — days, with the deadline named before the start; the cost of the check — a fraction of the development cost. The typical failure: three weeks on 15 hand-picked examples and a conclusion "we can launch" — three of the four requirements are violated.

**The scope:** the main scenario — in full (the product is being made for it); real data — without cleaning (cleaning inflates the result); typical AND hard cases; the strongest model (it separates "unsolvable" from "the model is weak"); a simple build tool; no optimizations of speed, error handling, or tidy code. The results of the run are saved — otherwise the versions cannot be compared.

**The tools** differ in what you have to do to get a result: a chat with the model (feel out the prompt, understand whether the model can cope in principle); a sandbox/console (the system prompt and the parameters separately, declarations of tools, code export — but it will not execute the function itself); an assistant builder (a persistent instruction plus your own files, an internal helper; it cannot be embedded into your own product); an app generator (an image of the solution and a check on live users, but the run over a sample you will have to build separately); a platform of visual scenarios (a workflow of blocks, a run over a sample with the history of every step — exactly what the achievability check needs); code (everything is possible, but edits go through a developer). The choice criteria: is a run over a sample needed, an interface of your own, the speed of learning, who on the team can build it.

## Procedure

### 1. Write the problem statement for the prototype (before building)
| # | Section | What is fixed |
|---|---|---|
| 01 | Input | the trigger (when it fires), the data, the user's request |
| 02 | Output | the format (connected text for a human / a structure for the interface); the mandatory elements of every answer — the basis of the acceptance criterion |
| 03 | Data sources | what the system reads in addition to the input (internal services, reference books, the web); the more sources, the harder the build |
| 04 | Rules of behavior | what it never asserts; what it does when the data is missing (say so directly or refuse); what it does not reason about without a clarification |
| 05 | Acceptance criterion | a verbal description of an acceptable answer; who accepts it (the product manager + experts); what counts as a failure |

The trap of the problem statement: describing the form, not the content. "There is a recommendation" is fulfilled literally and uselessly ("take the first one", with no justification). The requirement is phrased so that it cannot be fulfilled meaninglessly: "the recommendation rests on the differences named in the answer, every point is backed by the data of the listing, there are no invented facts".

### 2. Build minimally
1. The base scheme: trigger → model call (system prompt + input) → answer. A scenario adds a validation of the input, a second call, or an answer field by field; the agent logic — following the patterns from [[M-genai-assistant-architecture]].
2. The run over the sample must be built into the mechanics of the tool: the data moves between the steps as a list of items — every node processes every item, and no loop needs to be written. The prompt is assembled from expressions over the fields of the table.
3. The roles (even in a group of 3–4 people): the builder (the workflow, the screen), the author of the prompt, the tester (brings varied examples and notices the bad answers), the presenter. Build mistakes are visible immediately (it crashed / it stayed silent); quality mistakes show up only on varied examples.
4. The technical hygiene of the run: the failure of one item does not stop the run (the error handling is "continue"); the history of the runs stores the input and the output of every node; the answer is written back into the row of the sample (the run column), the grade — into the neighboring one (the eval column); the sample does not change between measurements.

### 3. Test: the algorithm
1. **Scenarios:** from the problem statement, write out the main scenario and the hard cases (missing data, contradictory data, incomparable pairs) — they are the test situations.
2. **The golden set:** a fixed sample of real examples (hundreds, not a handful), taken at random, uncleaned, with the hard cases included; it is stored and not changed between runs.
3. **The regression run:** the full processing of the golden set by the current version; the answers and the history of the steps are saved. Any edit to the prompt/model/architecture = a repeated run of the same set.
4. **Quality labeling** (first you read, then you count):
   - free-text notes always come first, on the first 20–30 answers: what is wrong, in your own words ("it invented a characteristic that does not exist", not "bad");
   - a checklist — yes/no questions, with the items taken from the notes (are the differences backed by the data? does the recommendation rest on the differences? are there no invented facts?); it gives a picture of "what to fix", not a single number;
   - a binary labeling "acceptable / not" — when the acceptance criterion has already been formulated; the threshold is named BEFORE the run (a share decided after looking = fitting);
   - a blind pairwise comparison — "is it better now" against the user's current experience or the previous version; the better of the two may still be bad.
5. **Metrics of three kinds:** quality (the share of acceptable answers under the binary labeling + a breakdown by the checklist items + zero unacceptable errors); cost (the price of an answer by the input/output tokens and the number of calls; the check "does it also hold on the cheapest model at the same volume?"); latency (the response time on the sample, TTFT/TPOT from the observable figures).
6. **Find the source of every bad error** — questions in order, from the cheapest check to the most expensive:
   | Question | Where to look | If no |
   |---|---|---|
   | Did the data reach the model? | the run history, the input of the model call | the build (expressions, field parsing) |
   | Is the answer present in the data itself? | the original example | the data (a rule of behavior for missing data, an external source) |
   | Does the prompt ask for what the user needs? | the prompt, read literally | the problem statement (requirements, rules for the hard cases) |
   | Everything above is in order, and the answer is still bad | — | the model (simplify/split the task, an example of a good answer, a verification step, a stronger model) |
   Frequent traps: rewriting the prompt when the model simply never received the data; demanding from the model an answer that is not in the data (it will invent one); changing the model when the prompt is being fulfilled literally; declaring the task unsolvable on the basis of a weak model.
7. **Decide the fate of the prototype** — questions in order:
   - is the acceptance criterion met (the share of acceptable ≥ the threshold, no unacceptable errors)? → **develop**: the product is built with account for what was learned, and the remaining errors are handed over as known risks;
   - among the errors, are there fixable ones (the build, the data, the problem statement)? → **iterate**: a plan of "what we change / how we check / when we stop" — one source of errors per iteration, the same run on the same sample, the threshold and the limit of iterations named before the first run;
   - are the errors model-only, checked on the strongest model and with a changed architecture? → **close**: record why. This is a finished answer about achievability, obtained in weeks, not a failure.
   The economics decide independently of quality: if even on the cheapest model an answer costs more than the product is ready to pay — close it. If it holds, the price is brought down during the refinement; it does not change the decision. The threshold is not raised after the run.

## Template / checklist

**The problem statement for the prototype:** the trigger; the input data; the format of the output + the mandatory elements; the sources; the rules of behavior when the data is missing; the verbal acceptance criterion; who accepts; what counts as a failure; the deadline (in days).

**The run checklist:** the sample is random and taken from real data; the hard cases are included; the model is the strongest available; a failure does not stop the run; the answers are saved into the run column; the history of the steps is available for review; the sample did not change between the runs.

**The decision checklist:** the labeling was done after reading the answers; the threshold was named before the run; the sources of the errors are classified (build/data/problem statement/model); the cost is computed, including on the cheapest model; the latency is measured; the decision (develop/iterate/close) is recorded with its grounds.

## Typical mistakes
| Mistake | Why it is bad | How to avoid it |
|---|---|---|
| The prototype as the first version of the product | Three weeks of work get dragged into production together with the hacks | The prototype is thrown away; development starts with account for what was learned |
| The hand-picking of "nice" examples | The result cannot be trusted | A random sample from real data |
| Cleaning the data before the run | It inflates the result: in production the data will be dirty | A run on the data as it is |
| "It works at the competitor" as proof | Different data, load, audience | Your own prototype on your own data |
| Counting the metric before reading the answers | You measure what is easy to count, not what breaks | Text notes → checklist → binary labeling |
| An acceptance threshold set after viewing the results | Fitting to the result | The threshold and the limit of iterations are named before the run |
| A single figure "82 out of 100 acceptable" | It says nothing about what to fix | A breakdown by the checklist items + a classification of the error sources |
| Fixing everything at once | It is unclear what worked | One source of errors per iteration, the same run |
| Polishing the prototype beyond the acceptance threshold "to perfection" | The prompt tuning does not carry over into the product: the architecture there is different | The criterion is met → develop; the leftovers are known risks |
| An "unsolvable" verdict on a budget model | "The task is unsolvable" and "the model is weak" are mixed up | An infeasibility verdict — only on the strongest model |

## Questions that can change the decision
- Can the process be described in a problem statement (input/output/rules/criterion)? If not, it is too early to build — first, the design of the task.
- What is the size of the sample, and are there hard cases in the data? Dozens of examples do not answer the question of achievability.
- Does the economics hold on the cheapest model at the full volume? If not, quality will not save it.
- Which errors are unacceptable in principle (an invented fact, a wrong verdict), and is their count zero in the run?
- How does the prototype differ from the future product (architecture, volume of data, load), and which of the learnings carry over?

## Related maps
[[M-genai-product-development]], [[M-genai-assistant-architecture]], [[M-mvp-pilots]], [[M-quant-methods]], [[M-usability-testing]], [[M-benchmarking]], [[M-unit-economics]], [[M-risks]], [[M-solution-design]]
