---
id: M-ux-frameworks
lang: en
title: UX research frameworks — the brief, JTBD, Job Stories and choosing an artifact
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [intake, research, options]
tags: [ux, frameworks, brief, jtbd, job-stories, user-stories, user-flow, bpmn, stage-metrics, versioning]
related: [M-cjm, M-jtbd, M-brief-hypotheses, M-research-types, M-in-depth-interviews, M-interview-analysis, M-design-thinking, M-ux-backlog, M-product-metrics]
---

# UX research frameworks: the brief, JTBD, Job Stories, choosing an artifact

## When to apply
When the request is vague ("understand why the feature isn't catching on", "improve onboarding") and two things must be decided: whether research is needed at all, and which artifact (a journey map, the client's "jobs", a flow, a process) will turn scattered facts into a basis for a decision. The map is needed at intake and at the options stage: it defines which data to collect and in what form to hand it to the team.

## Core idea
A framework is a skeleton of the process, not a "pretty slide". It gives repeatability (a new person reads the artifact and understands the logic), saves time (we don't invent a format), ties the work to metrics, and protects against the "broken telephone" between the researcher, the designer and the developer. Each framework answers its own question:

| Artifact | Answers the question | Data basis | What it does NOT give |
|---|---|---|---|
| "Star" brief (7 rays) | Whether it's worth researching and what happens to the result | The sponsor's decision | The facts themselves |
| CJM (journey map) | WHERE on the journey the experience breaks | Interviews, logs, support, observation | The "why" motivation |
| JTBD (the "job") | WHY the person takes on the task and what counts as success | In-depth interviews + an importance×satisfaction survey | Position on the journey |
| Job Story | IN WHICH SITUATION and for what outcome | Verbatim stories of real people | Role, implementation |
| User Story | WHAT to implement (role + feature) | A Job Story, an agreement with engineering | The reason for the choice |
| User Flow | Which STEPS inside the interface, how many clicks/fields | A prototype, mockups | Emotions and context |
| BPMN | Who and which system participates, where the expectations and SLAs are | A back-office process | UX emotions; the user is just one of the "players" |
| CJM × JTBD hybrid | Which "job" is broken by which barrier at which stage | All of the above | — |

The course's selection rule: first the CJM as the panorama, then a User Flow is pulled out of it for a narrow section; BPMN is brought in when UX runs into internal services. Do not mix emotions and processes in one artifact.

**JTBD.** People "hire" a product for a job in a specific life situation and "fire" it when a better performer exists. Three layers of a job: functional (what to get done), emotional (what to feel), social (how to look in the eyes of others). The difference from the traditional approach: context, motivation and usage situations instead of demographics and a feature list. Myths: JTBD is only about functions (no — the emotional and social layers are critical); churned users can be ignored (no — their reasons expose weak spots); it is a rigid template (no — it is a lens).

**Job Story vs User Story.** A User Story ("As a <role>, I want <feature>, so that…") is convenient for estimation and planning, but it limits the understanding of motivation. A Job Story ("When <situation/trigger>, I want <action>, so that <outcome/feeling>") is born from interviews and answers "why"; a User Story is its "operational" offspring and answers "what to implement". Usually you need both.

## Procedure
1. **The "star" brief.** Fill in the 7 rays (the table below). If at least one ray is empty — do not launch the research; first close the gap with the sponsor. This is protection from expensive but useless interviews.
2. **Check whether research is needed.** Is the answer already in analytics or past research (see [[M-ux-backlog]])? Has the decision already been made and does it not change with the result? Then research is not needed — say so plainly.
3. **Choose the artifact** using the table above (question → artifact). For a complex question — a chain: JTBD (why) → CJM (where) → a hybrid.
4. **Collect the data** (in-depth interviews, [[M-in-depth-interviews]]; analytics; support; observation — [[M-dogfooding]]). Attach a source to every fact. Without a source — it's a hypothesis.
5. **A 12-minute JTBD sprint** (when an idea needs to be quick-tested): context/trigger → a Job Story (≤25 words) → 2–3 alternatives (including offline, Excel, "ask a friend", "do nothing") → barriers → a success KPI.
6. **Clustering the jobs** (if there are transcripts): fragments → tags (context, trigger, obstacle, desired outcome) → 3–6 JTBD clusters.
7. **Importance × satisfaction** (if prioritization is needed): a survey on a 5-point scale — "How important is it to get the job done?" and "How satisfied are you with the current solution?" — strictly within one segment. Quadrants: important + unsatisfied = an underserved job (priority); important + satisfied = everything is fine; unimportant + unsatisfied = low priority; unimportant + satisfied = over-served.
8. **Translate into metrics** (the table below): one headline metric + 2–3 guardrails.
9. **Translate into the backlog:** Job Story → User Story → an Epic with a KPI in the "Definition of Done"; link it with [[M-cjm]] and [[M-ux-backlog]].
10. **Lifetime.** Revisit the map and the Job Stories regularly (in the course — once a quarter / every ~90 days) and after major releases. Artifact versioning: a version number + an update date (for example, `CJM-2.3 · date`); major — a rebuild of the stages, minor — new barriers/metrics, patch — wording edits. Keep the map, Job Stories and metrics files together (a shared base/Git), otherwise the artifact turns into a "museum exhibit".

**The artifact "viability" checklist:** the map was updated no later than ~90 days ago; every stage has a metric and an owner; every JTBD cluster is described by a Job Story and linked to the backlog; the files are versioned; the map, the Job Stories and the metrics live in one accessible place. Wiring in alerts: a drop in a stage's CSAT (for example, > 5 pp) or a rising drop-rate is a signal into the team's shared channel, not only onto a dashboard.

## Template / checklist

**The "star" brief (7 rays):**

| Ray | Question | Example wording |
|---|---|---|
| Need | Why are the new data needed? | "The conversion of step X is falling — there is a barrier" |
| Hypothesis / Decision | Which hypothesis or decision is at stake? | "Suspicion that the document upload step is difficult" |
| Audience | Who are we researching? | New users of segment Y |
| Context & Stage | At which stage of the journey is the problem? | "Sign-up → document upload" |
| Method & Evidence | How will we confirm it? | N interviews + Time-to-X logs |
| Impact / KPI | Which metric do we move? | Step conversion: baseline → target |
| Next Action | What will we do with the conclusions? | Redesign the flow, run an A/B test |

**Mini-JTBD (5 blocks):** Context | Job Story | Alternatives | Barriers | Success KPI.
Quality criteria: the context is specific ("at night", "on the road", not "when there is a task"); the Job Story is understandable to a newcomer without explanations; there is at least one "unfair" alternative (offline, a friend); the barrier is phrased in the user's language; the KPI is measurable and connected to a data source.

**Job layer → metric:**

| Layer | Metric | Formula / period |
|---|---|---|
| Functional | Time-to-Job; Success Rate | the median time from trigger to result; successful / valid attempts, per period |
| Emotional | Stage CSAT, CES | in the course, CSAT is shown as a 0–100 score; always record the calculation method and the window |
| Social | Referral rate, NPS | the share of those who recommended / respondents, per period |

**Job Story — check:** there is a situation/trigger; there is no solution inside the wording; an outcome or a feeling is stated; ≤25 words; the words of real users (verbatim quotes), not invented personas.

**Evidence for every statement:** a source label [quote, n=…], [metric, period], [support], [observation]; otherwise — [a team hypothesis].

## Typical mistakes
| Mistake | Consequence | How to fix |
|---|---|---|
| Asking about features, not about the situation | The true motivation is invisible | Start with "tell us how you solved this task before" |
| A vague Job Story ("buy fast and cheap") | The design solves "everything" and nothing | Add a trigger, place, time, feeling |
| An importance×satisfaction survey without segmentation | An averaged "average temperature" | Compute per segment |
| Digital-only alternatives | Offline and "do nothing" are ignored | Add real-life substitutes |
| An emotional-only KPI (CSAT) | The effect on the business is invisible | Add a functional one (CR, Time-to-Job) |
| A Job Story replacing the User Story in the dev backlog (or vice versa) | The "why" or the "what" is lost | Keep both, linked by a reference |
| Roles mixed (buyer + courier + warehouse) in one artifact | You got a BPMN instead of a CJM | Split the artifacts |
| Users who quit the product are ignored | A blind spot of weak places | Include them in the recruit |
| A brief with an empty ray, but the research is launched | Expensive useless research | Stop before filling it in |

## Questions that can change the decision
- Which decision will the sponsor make depending on the result? If none — the research is not needed.
- Are there already data (logs, support, past interviews), so we don't collect them anew?
- Is this a new customer job (JTBD, discovery) or an optimization of a known path (CJM, usability)?
- Do several roles/systems participate in the experience (then you need BPMN, not only a CJM)?
- Can we get access to real customers and to those who quit? Without this, the evidence falls to the level of hypotheses.
- How many segments with different jobs are there? They must not be averaged.

A note on boundaries: the course does not separately cover HEART, Kano surveys and other UX metric frameworks (Kano is only mentioned as a prioritization method in the session on ethnography). If they are needed — mark them as knowledge outside the course.

## Related maps
[[M-cjm]], [[M-jtbd]], [[M-brief-hypotheses]], [[M-in-depth-interviews]], [[M-interview-analysis]], [[M-design-thinking]], [[M-ux-backlog]], [[M-product-metrics]], [[M-research-types]]
