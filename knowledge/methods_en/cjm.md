---
id: M-cjm
lang: en
title: Customer Journey Map (CJM) — as-is and to-be, barriers and opportunities
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [research, options, strategy, validation]
tags: [cjm, journey-map, as-is, to-be, barriers, drivers, touchpoints, emotions, pains, opportunities]
related: [M-ux-frameworks, M-jtbd, M-usability-testing, M-dogfooding, M-ux-backlog, M-workshops, M-design-thinking, M-interview-analysis, M-product-metrics, M-solution-design]
---

# Customer Journey Map: as-is, to-be, finding barriers and opportunities

## When to apply
When you need to see at which stage of the journey the client loses the result and why: before choosing what to fix or build; for attaching metrics (CSAT, drop-rate) to concrete steps; for building a common team language. Without a map the team sees the product in fragments, and ideas "smear over the surface" instead of hitting the bottlenecks.

## Core idea
**CJM** — a visual map of the client's path from the moment a need arises to repeated use. Don't confuse:
- **User Flow** — steps inside an interface (clicks, fields, screens), no emotions;
- **BPMN** — a process with roles, systems and wait times; the user there is just one of the "players";
- **CJM** — the human experience: goals, expectations, thoughts, emotions, barriers. Without the emotional line it's just a chronology.

**As-is** — how the experience works today, built strictly on facts. **To-be** — the target experience after changes; until it has been tested on people, all of its claims are hypotheses.

Layers of the map (course template):

| Layer | What we record | Where to get it |
|---|---|---|
| Lifecycle stage | Major phases (awareness → search → comparison → choice → purchase → usage → loyalty) | Interviews, analytics |
| Client actions | What they do (no atomic clicks) | Sessions, observation, logs |
| Touchpoints | Channel/interface: website, app, push, support | Logs, marketing plan |
| Goals and expectations | Why, and what they expect | Interviews, JTBD |
| Thoughts and questions | What they keep in mind, what is missing | In-depth interviews, support |
| Emotions | The state (a word or a smiley — the feeling is what matters) | Quotes, observation |
| Barriers / drivers | What prevents / helps reaching the goal | Interviews, complaints, NPS comments |
| Step importance | How critical the step is for the goal | Interviews, survey |
| Experience (fact) | What actually happened: fast/long/inconvenient | Metrics, observation |
| Stage metric | CSAT, drop-rate, Time-to-X | Analytics |
| Recommendations | Improvement ideas placed next to the pain | Team workshop |
| Illustrations | Screenshot/photo of the step | Prototypes, video |

Course rule: **one fact — one link to a source.** An emotion without a quote or metric is a "fake pain".

## Procedure

### A. CJM as-is
1. **Frame:** which segment, which scenario, which client job ([[M-jtbd]]), where the path starts and ends. One role per map.
2. **Data:** in-depth interviews, questionnaires, behavioral analytics, support tickets, diaries, observation and dogfooding ([[M-dogfooding]]). At least two types of sources: "what they say" + "what they do".
3. **Macro-stages:** no more than 6–7 (at 10+ the map turns into a list). Don't write atomic actions unless necessary.
4. **Fill the layers for each stage:** actions → touchpoints → thoughts/questions → emotions → barriers/drivers. Every cell carries a source tag: [quote n=…], [metric], [support], [observation]; no source — [hypothesis] (allowed, but visually distinct).
5. **A metric under the barrier:** stage CSAT, drop-rate, time; without a number the map remains a poster.
6. **Highlight the pains:** mark the stages where at least two signals coincide (a metric drop, negativity in quotes, an error/stop during observation, calls to support).
7. **Prioritization:** scoring Pain × Importance (× segment reach). In a workshop — silent dot voting (3 dots per person).
8. **Hypotheses for the top-3 barriers:** Job Story + metric (baseline → target shift) + owner + rough effort estimate.
9. **Version and deadline:** date, owner (usually the product owner). The course recommendation is a revision once a quarter or after a major release.

### B. A 40-minute express workshop (when a quick diagnosis is needed)
Roles: facilitator, PM, analyst, designer, developer. Input: 2–3 fresh interviews, a dashboard on the key stages, the top-10 support tickets.

| Minutes | Action | Output |
|---|---|---|
| 0–5 | Goal, key metric, rules | Focus |
| 5–15 | Stages + 1–2 actions per stage | Skeleton |
| 15–25 | Pains and emotions | Red/blue stickers |
| 25–30 | Silent dot voting | Top pains |
| 30–35 | A hypothesis for each: Job Story, metric, shift | 2–3 hypotheses |
| 35–40 | Owner, rough estimate, check deadline | Plan |

For more on running the session — [[M-workshops]].

### C. How to find barriers and opportunities
- **Barrier** = a step where the path breaks: a conversion drop, going back, a pause >3 s, a question out loud ("is this really where?"), an error without an explanation, a workaround, a call to support.
- **Anxiety** = an emotional dip with normal actions (the client did everything but isn't sure it worked — a typical example: no confirmation or status).
- **Opportunity** = a step important for the goal with low experience (high importance, low experience); a mass workaround (people invented their own replacement); an underserved job from an importance×satisfaction survey; a step where a competitor gives a noticeably better experience ([[M-competitors]]).
- **A pattern, not an accident:** one observation is an incident; repetition by two or more people is a pattern candidate; confirm with a metric.
- **Barrier record:** Stage | Description (what is seen/heard) | Source and n | Metric | Impact | Cause hypothesis | What to check.

### D. CJM to-be
1. Take the as-is top barriers. For each one — 1–3 options for change (ideas — [[M-design-thinking]], [[M-solution-design]]).
2. Redraw the affected stages: new touchpoints/steps, the **expected** emotion, the **expected** metric. Label all cells "hypothesis" until they are checked.
3. Verify the key changes on a prototype ([[M-usability-testing]]) and/or with an experiment ([[M-mvp-pilots]]).
4. Update the map with facts after verification; close the hypotheses with the status "confirmed / refuted" ([[M-ux-backlog]]).

### E. Link with metrics
CSAT per stage (a short survey after the action); process metrics (Time-to-X, drop-rate); alerts on deviations; the key value stage is tied to the product's main metric ([[M-product-metrics]]). Compare the effect of a change before/after within one window and one segment.

## Template / checklist

**Barrier row for the backlog:**
`Stage | Barrier (fact) | Source/n | Metric (baseline) | Job Story | Solution hypothesis | Target shift | Owner | Status (hypothesis/confirmed/refuted)`

**Map readiness for use:**
- The stages cover the path "need → result/loyalty"; no more than 6–7.
- Every stage has actions, thoughts, emotions.
- Barriers and drivers have a source; without one they are marked as hypotheses.
- The top-3 barriers have a Job Story, a metric and a backlog entry.
- Version, date and owner are stated; a review deadline is set.
- The map is built for one role and one scenario.

## Typical mistakes
| Mistake | Result | Right move |
|---|---|---|
| The map is drawn inside the team from assumptions | Confirmation of one's own hypotheses | Rely on user stories and data, on quotes |
| Roles are mixed (client + courier + warehouse) | What you got is a BPMN | One person — one map |
| No emotions | A checklist of actions, not an experience | Add the emotional line with quotes |
| Steps too granular | 100 cells, no insight | Macro-stages, details go into a User Flow |
| "Annoying but minor" moments are missed | People leave exactly there | Record those too |
| No metrics | "A pretty picture" | A stage metric under every top barrier |
| The map lives apart from the backlog | It dies after the release race | Link pain → ticket |
| To-be presented as fact | False confidence | All to-be cells are hypotheses until checked |
| The map is stale (>6 months) | It reflects a past product | Regular revision |

## Questions that can change the decision
- For which segment and scenario is the map built? Do novices and experienced users have different paths?
- Which data is actually available (logs, interviews, support)? If only team opinion — the map will be a hypothesis as a whole.
- Where does the product's responsibility end (delivery, support, offline)? Those are CX problems, not interface ones ([[M-ux-backlog]]).
- Is there a metric that makes the stage visible (an event in analytics)? If not — set up measurement first.
- Is a full as-is needed, or is a narrow stretch enough (then a User Flow)?

## Related maps
[[M-ux-frameworks]], [[M-jtbd]], [[M-usability-testing]], [[M-dogfooding]], [[M-ux-backlog]], [[M-workshops]], [[M-design-thinking]], [[M-interview-analysis]], [[M-product-metrics]], [[M-solution-design]], [[M-competitors]], [[M-mvp-pilots]]
