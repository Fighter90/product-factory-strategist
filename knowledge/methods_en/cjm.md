---
id: M-cjm
lang: en
title: Customer Journey Map (CJM) — as-is and to-be, barriers and opportunities
course: ux
sources: ["EN mirror of the RU methodology card M-cjm (knowledge/methods/cjm.md); original sources are listed in the RU card"]
stages: [research, options, strategy, validation]
tags: [cjm, journey-map, as-is, to-be, barriers, drivers, touchpoints, emotions, pains, opportunities]
related: [M-ux-frameworks, M-jtbd, M-usability-testing, M-dogfooding, M-ux-backlog, M-workshops, M-design-thinking, M-interview-analysis, M-product-metrics, M-solution-design]
---

# Customer Journey Map: as-is, to-be, finding barriers and opportunities

## When to use
When you need to see at which stage of the journey the client loses the outcome and why: before choosing what to fix or build;
to tie metrics (CSAT, drop-rate) to concrete steps; to give the team a shared language. Without a map the team sees the product
in fragments, and ideas "smear" across the surface instead of hitting the bottlenecks.

## Core idea
A **CJM** is a visual map of the client's journey from the emergence of the need to repeated use. Do not confuse:
- **User Flow** — steps inside an interface (clicks, fields, screens), no emotions;
- **BPMN** — a process with roles, systems, and waiting times; the user there is one of the "players";
- **CJM** — a person's experience: goals, expectations, thoughts, emotions, barriers. Without the emotional line it is just a chronology.

**As-is** — how the experience is arranged now, built strictly on facts. **To-be** — the target experience after changes; until it is tested
on people, all of its statements are hypotheses.

Layers of the map (course template):

| Layer | What we record | Where it comes from |
|---|---|---|
| Lifecycle stage | Major phases (awareness → search → comparison → choice → purchase → use → loyalty) | Interviews, analytics |
| Client actions | What they do (without atomic clicks) | Sessions, observation, logs |
| Touchpoints | Channel/interface: site, app, push, support | Logs, marketing plan |
| Goals and expectations | Why and what they expect | Interviews, JTBD |
| Thoughts and questions | What they keep in mind, what they lack | In-depths, support |
| Emotions | State (a word or a smiley — the point is the feeling) | Quotes, observation |
| Barriers / drivers | What prevents / helps reaching the goal | Interviews, complaints, NPS comments |
| Step importance | How critical it is for the goal | Interviews, survey |
| Experience (fact) | What actually happened: fast/slow/inconvenient | Metrics, observation |
| Stage metric | CSAT, drop-rate, Time-to-X | Analytics |
| Recommendations | Improvement ideas next to the pain | Team workshop |
| Illustrations | Screenshot/photo of the step | Prototypes, video |

Course rule: **one fact — one link to a source.** An emotion without a quote or a metric is a "fake pain."

## Procedure

### A. CJM as-is
1. **Frame:** which segment, which scenario, which client job ([[M-jtbd]]), where the journey starts and ends. One role per map.
2. **Data:** in-depth interviews, questionnaires, behavioral analytics, support tickets, diaries, observation and
   dogfooding ([[M-dogfooding]]). At least two types of sources: "what people say" + "what people do."
3. **Macro-stages:** no more than 6–7 (at 10+ the map turns into a list). Do not write atomic actions unless necessary.
4. **Fill the layers for each stage:** actions → touchpoints → thoughts/questions → emotions → barriers/drivers. Every cell
   carries a source tag: [quote n=…], [metric], [support], [observation]; no source — [hypothesis] (allowed, but visually distinct).
5. **A metric under each barrier:** stage CSAT, drop-rate, time; without a number the map stays a poster.
6. **Highlight the pains:** mark the stages where at least two signals coincide (a metric drop, negativity in quotes, an error/stop
   during observation, calls to support).
7. **Prioritization:** scoring Pain × Importance (× segment reach). In the workshop — silent dot voting (3 dots per person).
8. **Hypotheses for the top-3 barriers:** Job Story + metric (baseline → target shift) + owner + a rough effort estimate.
9. **Version and date:** date, owner (usually the product owner). The course's recommendation — review quarterly or after a major release.

### B. A 40-minute express workshop (when a quick diagnosis is needed)
Roles: facilitator, product manager, analyst, designer, developer. Input: 2–3 fresh interviews, a dashboard over key stages, the top-10 support tickets.

| Minutes | Action | Output |
|---|---|---|
| 0–5 | Goal, key metric, rules | Focus |
| 5–15 | Stages + 1–2 actions per stage | Skeleton |
| 15–25 | Pains and emotions | Red/blue sticky notes |
| 25–30 | Silent dot voting | Top pains |
| 30–35 | A hypothesis for each: Job Story, metric, shift | 2–3 hypotheses |
| 35–40 | Owner, rough estimate, verification date | Plan |

More on running the session — [[M-workshops]].

### C. How to find barriers and opportunities
- **A barrier** = a step where the path breaks: conversion drop, going back, a pause >3 s, a question out loud ("is this really where I should be?"),
  an error without explanation, a workaround, a call to support.
- **Anxiety** = an emotional dip with normal actions (the client did everything but is not sure it worked — a typical
  example: no confirmation or status).
- **An opportunity** = a step important to the goal with a low experience score (importance high, experience low); a mass workaround (people
  invented their own replacement); an underserved job from an importance×satisfaction survey; a step where a competitor gives a noticeably better experience ([[M-competitors]]).
- **A pattern, not an accident:** one observation is a case; repetition by two or more people is a pattern candidate; confirm with a metric.
- **Recording a barrier:** Stage | Description (what is seen/heard) | Source and n | Metric | Impact | Hypothesis of the cause | What to check.

### D. CJM to-be
1. Take the as-is top barriers. For each — 1–3 variants of change (ideas — [[M-design-thinking]], [[M-solution-design]]).
2. Redraw the affected stages: new touchpoints/steps, the **expected** emotion, the **expected** metric. Label all
   cells "hypothesis" until tested.
3. Verify the key changes on a prototype ([[M-usability-testing]]) and/or with an experiment ([[M-mvp-pilots]]).
4. Update the map with facts after verification; close the hypotheses with a status "confirmed / refuted" ([[M-ux-backlog]]).

### E. Connection with metrics
CSAT per stage (a short survey after the action); process metrics (Time-to-X, drop-rate); alerts on deviations;
the key value stage is tied to the product's main metric ([[M-product-metrics]]). Compare the effect of a change before/after
within one window and segment.

## Template / checklist

**A barrier row for the backlog:**
`Stage | Barrier (fact) | Source/n | Metric (baseline) | Job Story | Solution hypothesis | Target shift | Owner | Status (hypothesis/confirmed/refuted)`

**Readiness of the map for use:**
- Stages cover the journey "need → outcome/loyalty"; no more than 6–7.
- Every stage has actions, thoughts, emotions.
- Barriers and drivers have a source; without one they are labeled as hypotheses.
- For the top-3 barriers there is a Job Story, a metric, and a backlog entry.
- Version, date, owner are stated; a review date is scheduled.
- The map is built for one role and one scenario.

## Common mistakes
| Mistake | Outcome | Right move |
|---|---|---|
| The map is drawn inside the team from assumptions | Confirming one's own hypotheses | Rely on user stories and data, quotes |
| Roles mixed (client + courier + warehouse) | You got a BPMN | One person — one map |
| No emotions | A checklist of actions, not an experience | Add the emotional line with quotes |
| Steps too fine-grained | 100 cells, no insight | Macro-stages; details go to the User Flow |
| "Annoying but minor" moments skipped | People leave exactly there | Record those too |
| No metrics | "A pretty picture" | A stage metric under every top barrier |
| The map lives apart from the backlog | It dies after the release race | Link pain → ticket |
| To-be presented as fact | False confidence | All to-be cells are hypotheses until tested |
| The map is stale (>6 months) | It reflects the past product | Regular review |

## Questions that can change the decision
- For which segment and scenario is the map built? Do novices and experienced users have different paths?
- Which data is really available (logs, interviews, support)? If only the team's opinion — the map will be a hypothesis entirely.
- Where does the product's responsibility end (delivery, support, offline)? Those are CX problems, not interface ([[M-ux-backlog]]).
- Is there a metric that shows the stage (an event in analytics)? If not — set up measurement first.
- Is a full as-is needed, or is a narrow stretch enough (then a User Flow)?

## Related maps
[[M-ux-frameworks]], [[M-jtbd]], [[M-usability-testing]], [[M-dogfooding]], [[M-ux-backlog]], [[M-workshops]], [[M-design-thinking]], [[M-interview-analysis]], [[M-product-metrics]], [[M-solution-design]], [[M-competitors]], [[M-mvp-pilots]]
