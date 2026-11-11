---
id: M-design-thinking
lang: en
title: Design thinking and user experience design
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [research, options, strategy, validation]
tags: [design-thinking, double-diamond, empathy, point-of-view, hmw, brainstorm, prototype, corridor-test, ux-design]
related: [M-cjm, M-jtbd, M-usability-testing, M-workshops, M-dogfooding, M-in-depth-interviews, M-solution-design, M-problem-design, M-mvp-pilots, M-ux-frameworks]
---

# Design thinking and user experience design

## When to apply
When the solution is not obvious, the product is new or being rethought, success depends on understanding the user, uncertainty
is high, and there is access to people and readiness to experiment. It helps avoid "building the product for ourselves".
Not suitable when the decision is already made, the task is procedural, strict quantitative calculations or scientific research
are needed, there is no access to users, the deadline is "yesterday", or the system is rigidly standardized.

## Core idea
**Design thinking** — a human-centered systemic approach to complex tasks: it starts with empathy for the user, and ideas are
validated through fast prototypes and tests. It is not one method but a **framework** — a sequence of work with expanding and
narrowing. Five stages (Stanford d.school): Empathize → Define → Ideate → Prototype → Test, but the process is **nonlinear**:
tests expose new problems, prototyping sparks ideas, you loop back.

**Double Diamond:** two "diamonds", each with a divergent phase (thinking wide: generation, the whole field of possibilities)
and a convergent one (narrowing: analysis, selection). The first diamond: empathy → analysis and synthesis (defining the
problem). The second: idea generation → prototype and test (the solution). In the broad sense, teams that ran interviews,
extracted jobs and tested prototypes were already doing design thinking.

**Choosing the experience artifact (session 11):** CJM — the panorama and the emotional line ("why is the cart abandoned");
User Flow — the steps inside an interface and the number of clicks/fields ("simplify signup to one screen"); BPMN — roles,
systems, SLA ("coordinate the warehouse and the courier"). CJM first, then pull a User Flow for the narrow section out of it;
don't mix roles and processes with emotions in one artifact. Artifacts into the roadmap: CJM → the UX backlog (what to fix),
User Flow → front-end tasks, point of view + HMW → an idea brainstorm.

## Procedure

### 1. Empathy (divergence)
Tools: living the experience ("step into the shoes" — walk the journey yourself), observation without prompts or judgment
(what they do, how and why; an example signal: an employee's desk covered with sticky-note reminders — the process is probably
painful), listening (interviews with open questions, stories, a chain of "why", [[M-in-depth-interviews]]). Data is raw, with
context, without interpretations. Mistakes: interviewing colleagues instead of users; a questionnaire instead of an interview;
jumping straight to a solution. Sources: [[M-dogfooding]].

### 2. Analysis and synthesis (convergence) → Define
*Analysis* — narrowing the field: looking for patterns and tensions in the raw data. *Synthesis* — packaging what was found
into a working problem statement (point of view, HMW). Stages:
1. Reread the interviews, extract quotes and facts (no conclusions).
2. Mark the unexpected, the tense, the contradictory.
3. Group the recurring or the acute.
4. Package into an insight: observation + explanation + why it matters.
5. Choose the form of synthesis: point of view, empathy map, personas, a Venn diagram, CJM ([[M-cjm]]), HMW.

**Point of View — 4 stickies:** (1) **We met…** a specific person/role; (2) **And we were surprised to discover…** a real
tension-fact; (3) **We think…** the need as a job, not a solution; (4) **It would be amazing to help…** a sketch of a direction.
A good point of view: a specific person, genuine surprise, the need as a job ([[M-jtbd]]), the solution only sketched, the
insight not too broad. Then HMW: `How might we <desired outcome> for <segment>, avoiding <constraint>?` — several formulations
of one barrier.

### 3. Idea generation (divergence)
Brainstorming rules: don't criticize; welcome the "wild"; build on others' ideas; keep the problem in mind; write everything
down; quantity breeds quality; brainwriting (silently, so introverts are heard); don't interrupt. Practice: 8 ideas in
8 minutes on the chosen point of view.

### 4. Idea selection (convergence)
Dot-voting (3 dots each), ICE (Impact–Confidence–Ease, 1–10), the owner's "golden voice" when time is short; a timebox of about
5 minutes; never select by open discussion — the dominator wins. More tools — [[M-workshops]].

### 5. Prototype and test
A prototype is a way to fail cheaply, **not a presentation**: paper + markers, FigJam blocks, Figma, "Wizard of Oz" (a human
plays the system — good for AI, voice, assistants). Low-fi in ~20 minutes: one or two key screens, no color and no
"pixel-perfection". Express ("corridor") test: 3 respondents, 3 questions, ~15 minutes: show the prototype, ask them to do the
task, ask "what is unclear", write down the quote and the moment of the stall. If 2–3 people stumble in the same place — go
back to the idea or redo the prototype. One important hypothesis, a legend and tasks, observation without leading questions.
Don't test on colleagues who know the task. Full-scale tests — [[M-usability-testing]].

### 6. Apply in parts
If the data already exists, you can start at Ideate → Prototype → Test. Think about the problem, not about "checking the box"
of having gone through all the steps. If there is no access to users — honestly mark that empathy was replaced by assumptions,
and the conclusions are hypotheses.

### 7. "Start tomorrow" checklist (6 steps, ~2.5 hours)
2 users × 30 min → 5 quotes that surprised you → one point of view → Crazy-8 → dot-vote and a draft → show it to 3 people,
ask what is unclear.

## Template / checklist

**Point of view:** `We met [who, context] → And we were surprised to discover [a contradicting fact, source] → We think
[a need/job] → It would be amazing to help [direction]`.

**HMW set:** 3–5 formulations of one barrier from different angles (speed it up, remove a step, remove anxiety, turn it into
a pleasant experience).

**Idea card:** Name | Which point of view/HMW it solves | Why it is better than the current one | Risk | ICE (I, C, E) |
What to verify with a prototype | Metric.

**Express-test record:** `Prototype | Task | Participant | Where they stalled (time) | Quote | Conclusion | What we change`.

**Quality check:** real users at the foundation; insights with sources; ideas tied to a specific problem; selection not by
argument; the prototype tested on the target audience; the result landed in the backlog/roadmap ([[M-ux-backlog]]).

## Typical mistakes
| Mistake | Outcome | Fix |
|---|---|---|
| Skipping empathy | A product "for ourselves" | At least several real observations/interviews |
| Interpreting before extracting facts | Confirming your own hypotheses | Facts → oddities → insight |
| Ignoring "small" oddities | A strong insight is lost | Record them separately |
| An insight/point of view too broad | No concrete ideas | Narrow it to a specific person and situation |
| Criticism during the ideation stage | The flow blocks | Criticism only at convergence |
| A beautiful mockup instead of a prototype | Time lost | Low-fi |
| Testing on colleagues | Barriers invisible | The target audience |
| Mixing roles and emotions in one artifact | "Mush" | CJM, User Flow and BPMN separately |
| Running the method when the solution is predetermined | Imitation | Honestly choose another format |
| Treating a test on three people as statistics | False confidence | It is a signal, not proof |

## Questions that can change the decision
- Is there access to users and time for empathy? If not — the result can only be treated as hypotheses.
- Is the decision predetermined by the leadership? Then validation is needed, not generation.
- Are there existing studies or analytics to start from the Define/Ideate stage?
- Do internal systems and roles participate (is BPMN needed)?
- What counts as success: an insight, a prototype, a tested hypothesis, a ready solution? This determines the depth of the cycle.

## Related maps
[[M-cjm]], [[M-jtbd]], [[M-usability-testing]], [[M-workshops]], [[M-dogfooding]], [[M-in-depth-interviews]], [[M-solution-design]], [[M-problem-design]], [[M-mvp-pilots]], [[M-ux-frameworks]], [[M-ux-backlog]]
