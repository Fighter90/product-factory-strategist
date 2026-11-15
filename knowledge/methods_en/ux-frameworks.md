---
id: M-ux-frameworks
lang: en
title: UX research frameworks — the brief, JTBD, Job Stories, and artifact selection
course: ux
sources: ["EN mirror of the RU methodology card M-ux-frameworks (knowledge/methods/ux-frameworks.md); original sources are listed in the RU card"]
stages: [intake, research, options]
tags: [ux, frameworks, brief, jtbd, job-stories, user-stories, user-flow, bpmn, stage-metrics, versioning]
related: [M-cjm, M-jtbd, M-brief-hypotheses, M-research-types, M-in-depth-interviews, M-interview-analysis, M-design-thinking, M-ux-backlog, M-product-metrics]
---

# UX research frameworks: the brief, JTBD, Job Stories, artifact selection

## When to apply
When the request is vague ("understand why the feature is not taking off", "improve onboarding") and two things need to be decided: whether research is needed at all,
and which artifact (a journey map, the customer's "jobs", a flow, a process) will turn scattered facts into a basis for a decision.
The map is needed at intake and at the options stage: it determines which data to collect and in what form to hand it to the team.

## Essence
A framework is the frame of a process, not a "pretty slide". It gives repeatability (a new person reads the artifact and
understands the logic), time savings (we do not invent a format), a link to metrics, and protection against "broken telephone"
between the researcher, the designer and the developer. Each framework answers its own question:

| Artifact | Answers the question | Data basis | What it does NOT give |
|---|---|---|---|
| Brief-"star" (7 rays) | Whether to research and what will happen to the result | The client's decision | The facts themselves |
| CJM (journey map) | WHERE on the journey the experience breaks | Interviews, logs, support, observation | The motivation "why" |
| JTBD ("job", Job) | WHY a person takes on the task, what they count as success | In-depth interviews + an importance×satisfaction survey | Position on the journey |
| Job Story | IN WHICH SITUATION and for the sake of which outcome | Verbatim stories of real people | Role, implementation |
| User Story | WHAT to implement (role + function) | Job Story, an agreement with development | The reason for choosing |
| User Flow | Which STEPS inside the interface, how many clicks/fields | Prototype, mockups | Emotions and context |
| BPMN | Who and which system participates, where the waits and SLAs are | The back-office process | UX emotions; the user is one of the "players" |
| CJM × JTBD hybrid | Which "job" is broken by which barrier at which stage | All of the above | — |

The selection rule from the course: first the CJM as the panorama, then the User Flow for a narrow section is pulled out of it; BPMN is brought in
when UX runs into internal services. Do not mix emotions and processes in one artifact.

**JTBD.** People "hire" a product for a job in a specific life situation and "fire" it when there is a better performer.
Three layers of the job: functional (what to do), emotional (what to feel), social (how to look in the eyes of others).
The difference from the traditional approach: instead of demographics and a list of features — context, motivation, usage situations.
Myths: JTBD is only about functions (no — the emotional and social layers are critical); those who rejected the product can be ignored (no — their reasons
expose weak spots); it is a rigid template (no — it is a lens).

**Job Story vs User Story.** The User Story ("As a <role>, I want <function>, so that…") is convenient for estimation and planning, but
it limits the understanding of motivation. The Job Story ("When <situation/trigger>, I want <action>, so that <outcome/feeling>")
is born from interviews and answers "why"; the User Story is its "operational" descendant and answers "what to implement". Usually both are needed.

## Procedure
1. **Brief-"star".** Fill in the 7 rays (the table below). If even one ray is empty — do not launch the research; first
   close the gap with the client. This is protection against expensive but useless interviews.
2. **Check whether research is needed.** Is the answer already in analytics or in past studies (see [[M-ux-backlog]])? Has the decision already
   been made and does it not change with the result? Then research is not needed — say so directly.
3. **Choose the artifact** using the table above (question → artifact). For a complex question — a chain: JTBD (why) → CJM (where) → the hybrid.
4. **Collect the data** (in-depth interviews, [[M-in-depth-interviews]]; analytics; support; observation — [[M-dogfooding]]).
   Attach a source to every fact. Without a source — a hypothesis.
5. **A 12-minute JTBD sprint** (when an idea needs to be quickly "fired"): context/trigger → Job Story (≤25 words) →
   2–3 alternatives (including offline, Excel, "ask a friend", "do nothing") → barriers → the success KPI.
6. **Clustering of jobs** (if there are transcripts): fragments → tags (context, trigger, obstacle, desired outcome) →
   3–6 JTBD clusters.
7. **Importance × satisfaction** (if prioritization is needed): a survey on a 5-point scale "How important is it to get the job done?"
   and "How satisfied are you with the current solution?", strictly inside the segment. Quadrants: important + not satisfied = an underserved job
   (priority); important + satisfied = everything is fine; unimportant + not satisfied = low priority; unimportant + satisfied = over-served.
8. **Translation into metrics** (the table below): one main metric + 2–3 guardrails.
9. **Translation into the backlog:** Job Story → User Story → Epic with the KPI in the "Definition of Done"; link to [[M-cjm]] and [[M-ux-backlog]].
10. **Shelf life.** The map and Job Stories are reviewed regularly (in the course — once a quarter / every ~90 days) and after major releases. Versioning of artifacts: a version number + the update date (for example, `CJM-2.3 · date`); major — restructuring of the stages, minor — new barriers/metrics, patch — wording edits. Keep the map, Job Stories and metrics files together (a shared repository/Git), otherwise the artifact turns into a "museum exhibit".

**The artifact "viability" checklist:** the map was updated no later than ~90 days ago; every stage has a metric and an owner; every JTBD cluster is described by a Job Story and linked to the backlog; the files are versioned; the map, Job Stories and metrics live in one accessible place. The link with alerts: a drop in the stage CSAT (for example, > 5 p.p.) or a rise in the drop-rate — a signal into the team's shared channel, not only onto a dashboard.

## Template / checklist

**Brief-"star" (7 rays):**

| Ray | Question | Example wording |
|---|---|---|
| Need | Why are the new data needed? | "Conversion of step X is falling — we need the barrier" |
| Hypothesis / Decision | Which hypothesis or decision is at stake? | "A suspicion of a complicated document-upload step" |
| Audience | Who are we studying? | New users of segment Y |
| Context & Stage | At which stage of the journey is the problem? | "Sign-up → document upload" |
| Method & Evidence | What will confirm it? | N interviews + Time-to-X logs |
| Impact / KPI | Which metric are we moving? | Step conversion: baseline → target |
| Next Action | What will be done with the findings? | Redesign the flow, run an A/B test |

**Mini-JTBD (5 blocks):** Context | Job Story | Alternatives | Barriers | Success KPI.
Quality criteria: the context is specific ("at night", "on the road", not "when there is a task"); the Job Story is understandable to a newcomer without
explanations; there is at least one "dishonest" alternative (offline, a friend); the barrier is in the user's language; the KPI is measurable and connected to a data source.

**Job layer → metric:**

| Layer | Metric | Formula / period |
|---|---|---|
| Functional | Time-to-Job; Success Rate | the median time from trigger to outcome; successful / valid attempts, per period |
| Emotional | Stage CSAT, CES | in the course CSAT is shown as a score of 0–100; always fix the calculation method and the window |
| Social | Referral rate, NPS | the share of those who recommended / respondents per period |

**Job Story — check:** there is a situation/trigger; there is no solution inside the wording; the outcome or feeling is stated; ≤25 words;
the words of real users (verbatim quotes), not invented personas.

**Evidence for every claim:** a source label [quote, n=…], [metric, period], [support], [observation], otherwise — [team hypothesis].

## Typical mistakes
| Mistake | Consequence | How to fix |
|---|---|---|
| Asking about functions, not about the situation | The true motivation is invisible | Start with "tell us how you solved the task before" |
| A vague Job Story ("buy quickly and cheaply") | Design solves "everything" and nothing | Add a trigger, a place, a time, a feeling |
| An importance×satisfaction survey without segmentation | An averaged "mean temperature" | Compute by segments |
| Only digital alternatives | Offline and "do nothing" are ignored | Add life substitutes |
| A KPI that is only emotional (CSAT) | The business effect is invisible | Add a functional one (CR, Time-to-Job) |
| A Job Story replaces the User Story in the development backlog (or vice versa) | The "why" or the "what" is lost | Keep both, linked by a reference |
| Roles mixed (buyer + courier + warehouse) in one artifact | You get BPMN instead of CJM | Split the artifacts |
| Those who rejected the product are ignored | A blind spot on weak spots | Include them in the recruit |
| A brief with an empty ray, but the research is launched | Expensive useless research | Stop before filling it in |

## Questions that can change the decision
- Which decision will the client make depending on the result? If none — the research is not needed.
- Is there already data (logs, support, past interviews) so that we do not collect it anew?
- Is this a new customer job (JTBD, discovery) or an optimization of a known path (CJM, usability)?
- Do several roles/systems participate in the experience (then BPMN is needed, not only the CJM)?
- Can we get access to real customers and to those who rejected the product? Without this the evidence falls back to hypotheses.
- How many segments with different jobs? They must not be averaged.

A note on boundaries: the course does not separately cover HEART, Kano surveys and other UX-metrics frameworks (Kano is only mentioned
as a prioritization method in the session on ethnography). If such frameworks are needed, mark them as knowledge outside the course.

## Related cards
[[M-cjm]], [[M-jtbd]], [[M-brief-hypotheses]], [[M-in-depth-interviews]], [[M-interview-analysis]], [[M-design-thinking]], [[M-ux-backlog]], [[M-product-metrics]], [[M-research-types]]
