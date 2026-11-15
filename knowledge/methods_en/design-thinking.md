---
id: M-design-thinking
lang: en
title: Design Thinking and user experience design
course: ux
sources: ["EN mirror of the RU methodology card M-design-thinking (knowledge/methods/design-thinking.md); original sources are listed in the RU card"]
stages: [research, options, strategy, validation]
tags: [design-thinking, double-diamond, empathy, point-of-view, hmw, brainstorm, prototype, hallway-test, ux-design]
related: [M-cjm, M-jtbd, M-usability-testing, M-workshops, M-dogfooding, M-in-depth-interviews, M-solution-design, M-problem-design, M-mvp-pilots, M-ux-frameworks]
---

# Design Thinking and user experience design

## When to use
When the solution is not obvious, the product is new or being rethought, success depends on understanding the user, uncertainty is high, and there is access
to people and a willingness to experiment. It helps avoid "building the product for ourselves." It does not fit when the decision is already made, the task is routine, strict quantitative
calculations or scientific research are needed, there is no access to users, the deadline was "yesterday," or the system is rigidly regulated by standards.

## Core idea
**Design thinking** — a human-centered systemic approach to complex problems: it starts with empathy for the user, and ideas are validated through
quick prototypes and tests. It is not one method but a **framework** — a sequence of work with expanding and narrowing. Five stages (Stanford d.school):
Empathize → Define → Ideate → Prototype → Test, but the process is **non-linear**: tests surface new problems, prototyping generates ideas, and we loop back.

**Double Diamond:** two "diamonds," each with a divergent phase (thinking wide: generation, the whole field of possibilities) and a convergent one (narrowing:
analysis, selection). The first diamond: empathy → analysis and synthesis (defining the problem). The second: idea generation → prototype and test (the solution). In the broad
sense, teams that ran interviews, distilled jobs, and tested prototypes were already working by design thinking.

**Choosing the artifact for describing the experience (lesson 11):** CJM — the panorama and the emotional line ("why was the cart abandoned"); User Flow — the steps inside the
interface and the number of clicks/fields ("simplify signup to one screen"); BPMN — roles, systems, SLAs ("align the warehouse and the courier").
Start with the CJM, then extract a User Flow from it for a narrow section; do not mix roles and processes with emotions in one artifact. Artifacts into the roadmap:
CJM → the UX backlog (what to fix), User Flow → frontend tasks, point of view + HMW → an idea sprint.

## Procedure

### 1. Empathy (divergence)
Tools: living the experience ("step into their shoes" — walk the path yourself), observation without hints or judgment (what the person does, how and why;
an example signal: an employee's desk covered in sticky-note reminders — the process is probably painful), listening (interviews with open
questions, stories, a chain of "whys", [[M-in-depth-interviews]]). The data is raw, with context, without interpretations. Mistakes: interviewing colleagues
instead of users; a questionnaire instead of an interview; proposing a solution right away. Sources: [[M-dogfooding]].

### 2. Analysis and synthesis (convergence) → Define
*Analysis* — we narrow the field: looking for patterns and tensions in the raw data. *Synthesis* — we package what was found into a workable problem statement (point of view, HMW). Stages:
1. Re-read the interviews, extract quotes and facts (without conclusions).
2. Mark the unexpected, the tense, the contradictory.
3. Group the recurring or the acute.
4. Package into an insight: observation + explanation + why it matters.
5. Choose a synthesis format: point of view, empathy map, personas, a Venn diagram, CJM ([[M-cjm]]), HMW.

**Point of View — 4 sticky notes:** (1) **We met…** a specific person/role; (2) **And we were surprised to find…**
a real tension-fact; (3) **We think that…** the need as a job, not a solution; (4) **It would be amazing to help…** a sketch of a direction.
A good point of view: a specific person, genuine surprise, the need as a job ([[M-jtbd]]), the solution only sketched, the insight not too broad.
Then HMW: `How might we <desired outcome> for <segment>, avoiding <constraint>?` — several phrasings of one barrier.

### 3. Idea generation (divergence)
Brainstorm rules: do not criticize; welcome the "wild"; build on others' ideas; keep the problem in mind; write everything down; quantity breeds quality;
brainwriting (silent, so that introverts get heard); no interruptions. Practice: 8 ideas in 8 minutes against the chosen point of view.

### 4. Choosing an idea (convergence)
Dot-voting (3 dots each), ICE (Impact–Confidence–Ease, 1–10), the owner's "golden vote" when time is short; a timebox of about 5 minutes; do not choose by discussion —
a dominator will push through. More tools — [[M-workshops]].

### 5. Prototype and test
A prototype is a way to fail cheaply, **it is not a presentation**: paper + markers, FigJam blocks, Figma, the "Wizard of Oz" (a human plays the system — good for
AI, voice, assistants). Low-fi in ~20 minutes: one or two key screens, no color, no "pixel perfect". An express ("hallway") test: 3 respondents, 3 questions, ~15 minutes: show
the prototype, ask them to complete the task, ask "what was unclear," record the quote and the moment of hesitation. If 2–3 people stumble in the same place — return to the idea or rebuild the prototype.
One important hypothesis, a legend and tasks, observation without leading questions. Do not test on colleagues who know the task. Full-scale tests — [[M-usability-testing]].

### 6. Apply it in parts
If the data already exists, you can start at Ideate → Prototype → Test. Think about the problem, not about the checkbox of having completed every step. If there is no access to users —
honestly mark that empathy was substituted with assumptions, and the conclusions are hypotheses.

### 7. A "start tomorrow" checklist (6 steps, ~2.5 hours)
2 users × 30 min → 5 quotes that surprised you → one point of view → Crazy-8 → dot-vote and a draft → show it to 3 people, ask what is unclear.

## Template / checklist

**Point of view:** `We met [who, context] → And we were surprised to find [a contradicting fact, source] → We think that [the need/job] → It would be amazing to help [a direction]`.

**The HMW set:** 3–5 phrasings of one barrier from different angles (speed it up, remove a step, remove anxiety, turn it into a pleasant experience).

**Idea card:** Name | Which point of view/HMW it solves | Why it is better than the current one | Risk | ICE (I, C, E) | What to validate with a prototype | Metric.

**Express-test record:** `Prototype | Task | Participant | Where they stumbled (time) | Quote | Conclusion | What we change`.

**Quality check:** real users at the foundation; insights with sources; ideas tied to a specific problem; the choice not made by argument; the prototype tested
on the target audience; the result landed in the backlog/roadmap ([[M-ux-backlog]]).

## Typical mistakes
| Mistake | Result | Fix |
|---|---|---|
| Skipping empathy | A product "for ourselves" | At least several real observations/interviews |
| Interpreting before the facts are written down | Confirming hypotheses | Facts → oddities → insight |
| Ignoring "small" oddities | A strong insight is lost | Record them separately |
| Too broad an insight/point of view | No concrete ideas | Narrow it to a specific person and situation |
| Criticism at the idea stage | The flow is blocked | Criticism only at convergence |
| A pretty mockup instead of a prototype | Wasted time | Low-fi |
| Testing on colleagues | Barriers invisible | The target audience |
| Mixing roles and emotions in one artifact | "Mush" | CJM, User Flow, and BPMN separately |
| Applying the method when the decision is already made | Imitation | Honestly choose a different format |
| Taking a test on three people for statistics | False confidence | It is a signal, not proof |

## Questions that can change the decision
- Is there access to users and time for empathy? If not — the results can only count as hypotheses.
- Is the decision predetermined by the leadership? Then validation is needed, not generation.
- Are there existing studies or analytics to start from at the Define/Ideate stage?
- Are internal systems and roles involved (is BPMN needed)?
- What counts as success: an insight, a prototype, a validated hypothesis, a finished solution? The depth of the cycle depends on this.

## Related cards
[[M-cjm]], [[M-jtbd]], [[M-usability-testing]], [[M-workshops]], [[M-dogfooding]], [[M-in-depth-interviews]], [[M-solution-design]], [[M-problem-design]], [[M-mvp-pilots]], [[M-ux-frameworks]], [[M-ux-backlog]]
