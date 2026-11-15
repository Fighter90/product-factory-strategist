---
id: M-dogfooding
lang: en
title: Ethnography, diary studies, and dogfooding
course: ux
sources: ["EN mirror of the RU methodology card M-dogfooding (knowledge/methods/dogfooding.md); original sources are listed in the RU card"]
stages: [research, options, validation]
tags: [ethnography, observation, contextual-interview, shadowing, diaries, dogfooding, insights, as-is]
related: [M-cjm, M-research-types, M-in-depth-interviews, M-interview-analysis, M-usability-testing, M-ux-backlog, M-design-thinking, M-workshops, M-audience-research]
---

# Ethnography, diary studies, and dogfooding

## When to use
When you need to see what people **do**, not what they say: when creating a new experience, redesigning, hunting for hidden problems and growth
points, studying competitors through real usage, or when the product cannot be reproduced in a laboratory. Dogfooding is a fast,
cheap way to align the team and catch obvious problems before going out to users. None of these methods replaces research with real customers.

## Core idea
- **Ethnography:** a qualitative method in which the researcher immerses themselves in the environment and the context of users' lives and observes behavior and
  interaction with the product in real life. Pros: deep context, hidden needs, team empathy, capturing real
  actions. Cons: heavy on resources, a small sample, the influence of the observer's presence, the risk of interpreting through one's own experience,
  and access to the real environment is not always possible.
- **Types of observation** (axes): field (natural setting) / laboratory (controlled); participant (the observer tries it themselves) /
  non-participant; overt (the participant knows) / covert (the purpose is not disclosed — requires ethical and legal vetting).
- **Forms:** passive observation; moderated (rare non-leading questions: "what did you just think?"); provoked ("imagine
  the courier is 20 minutes late"); the contextual interview (the person demonstrates and explains as they go — "memory lies, behavior does not");
  shadowing (accompanying someone through a shift or a day); diaries.
- **The diary study:** the participant records their own experience over time (text, screenshots, video, voice notes, short surveys). It fits
  habits, usage triggers, learning and adaptation, changing attitudes toward the product. Variants: capturing in the moment
  (more detail, but it influences the situation) and "snippets" with a detailed debrief at the end of the day (fewer distortions, possible omissions).
- **Dogfooding (eat your own dog food):** the team uses its own product as an end user. It is needed when there is a
  prototype that users have not yet seen; after UX tests before rollout; to align understanding and empathy. Types: field
  (a real, live need) and laboratory (assigned scenarios, an artificial need); team and individual.
- **Limitations of dogfooding:** employees ≠ real users (they know the product, have different motivation, get used to bugs); there is not enough
  depth for expert tools (you cannot "pretend to be a doctor"); without structure it is ineffective.

## Procedure

### A. Field observation
1. A goal phrased as a question and an observable behavior: "how do sellers photograph and publish an item," not "see what they do".
2. Format: field/laboratory, participant or not, overt or not. Rules: do not prompt, minimal interference, do not hunt
   for confirmation of the hypothesis, watch the non-verbal signals.
3. Segment and sample: usually 5–7 people per segment; recruit people who actually live with the task.
4. Ethics and law: voluntary participation, consent to recording and to personal-data processing, confidentiality, the
   researcher's safety, non-intrusiveness. Do not record without consent.
5. Scenario (45–90 min): warm-up → surveying the environment → observing real actions → rare contextual questions → debriefing.
6. Recording form (an adaptation of the course's "ad account" sample) — a table by CJM stage:
   `Stage | User task | Stops (count) | Thoughts aloud (verbatim) | Errors/what went wrong | Insight`.
   Add photos/screenshots, quotes, a description of the environment, the devices, the distractions.
7. Check the equipment: recording, permissions, charged devices, a notes template.

### B. Team dogfooding
1. The goal and the critical scenarios (what we are testing and what counts as success).
2. Composition: different roles (PMs, designers, engineers, analysts, QA, content), at most 7–8 people per group.
3. Roles: moderator, executor, observer/recorder. Walk the scenarios in real time, without discussing as you go.
4. Debrief: for each issue — is it a bug or UX; what to improve. Template: problem — insight — idea — priority.
5. "Grounding": create the tickets, pin down the agreements, surface the hypotheses that need to be tested on real users.

### C. Individual dogfooding
The goal and the scenarios → instructions (where to test, where to send feedback and why) → a form/sheet for feedback → analysis (groups,
points of confusion, frequency, severity, position on the CJM) → close the loop: thank the participants and share the results.

### D. The diary
The goal and the format (text, voice, a survey, video) → the tool → recruit 7–15 people (some will drop out) with a short briefing at the kickoff
session → reminders and follow-up questions, for a long study pay the incentives in installments → a closing interview, feedback on the format, the reward.

### E. Analysis (shared by observation, dogfooding, and diaries)
1. **Bring everything into one place:** notes, feedback, diaries, video/audio.
2. **The first pass:** where something went wrong, where people got confused or stopped, emotions, repetitions, surprises, deviations from the intended flow, questions.
3. **Coding:** each observation → one heading/theme (sticky notes: take one, check the next — does it fit, otherwise a new heading; a sheet: quote/observation + theme);
   re-read with fresh eyes, check whether themes can be merged. Record the observation "as if on camera," without interpretation.
4. **Insight = observation + explanation + why it matters** (for example, the person completed the order but sat in silence — there was no confirmation
   — confidence drops and repeated actions grow).
5. **Hypothesis:** if the cause is known — what to change; if unknown — how to find out.
6. **Prioritization:** frequency, severity for the user, severity for the business; Kano, ICE/RICE, cost, simple voting.
   Important for dogfooding: separate professional noise ("we know how it should be done") from a genuine need.
7. **Patterns:** one observation is an incident; a repeat across ≥2–3 people is a candidate regularity. Distinguish behavioral, emotional,
   contextual, social, and instrumental patterns.
8. **Output:** update [[M-cjm]] (as-is) and record the insights into [[M-ux-backlog]]; to validate hypotheses — [[M-usability-testing]] with real users.

### F. The double loop (the recommended combination)
Ethnography (the outer loop, real context) → dogfooding (the inner one, fast and regular) → a UX test (verification) →
quantitative validation (A/B, analytics). The blind spots of dogfooding (ideal conditions, one everyday context) are closed
by ethnography; the blind spots of ethnography (small scale, speed) — by dogfooding.

## Template / checklist

**The dogfooding record (unified):** `Scenario step | What the participant did | Expectation | Fact | Emotion | Severity | Preliminary recommendation | Link to the recording/screenshot`.

**What to record:** where friction arose; what triggered an emotion; where they "hung"; where I distrust the interface; what was expected and what happened
(cognitive dissonance); what was done differently from the plan; what to improve right away.

**Health benchmarks for the practice (from the course notes, not the slides — calibrate them):** 80–100% of the team participating; 2–6 issues per person
per session on active functionality; ≥70% of what is found lands in the backlog; regularity (once a week/before every release).

**The kickoff checklist:** the goal and the critical scenarios; the composition and roles; consents and ethics; the recording tool; the template; the analysis plan; who
creates the tickets; how to close the feedback loop with the participants.

## Typical mistakes
| Mistake | Consequence | What to do |
|---|---|---|
| Interference, advice, questions asked in advance | The behavior changes | Minimal interference, neutral questions |
| Interpreting before the facts are recorded | Confirming one's own hypothesis | Raw data first, "as if on camera" |
| Short observation, one day, one context | Random conclusions | Plan several contexts and repeats |
| Focus only on the product, not the environment | The causes outside the interface are lost | Record the environment, distractions, tools, people around |
| Averaging "all users" | A false portrait | Work with segments and stories |
| Dogfooding under ideal conditions (fast internet, two monitors) | No real friction | Include field and "extreme" conditions |
| Dogfooding once "for the checkbox" with no tickets in the backlog | No change | Regularity, an owner, mandatory ticket creation |
| Treating the team as the target audience | Blind spots | Use it as a filter, not as a substitute for respondents |
| Covert observation without legal vetting | Ethical and legal risk | Informed consent or legal sign-off |

## Questions that can change the decision
- Is a new experience and context needed (ethnography), or a validation of a finished scenario (a UX test, dogfooding)?
- Is there access to the real environment and the participants' consent? If not — diaries or a laboratory format with simulated context.
- Does the team's experience match the audience's? If not, dogfooding will yield only a filter for obvious problems.
- Are there resources for the analysis (coding time and owners)? Otherwise there will be more data than decisions.
- What exactly will change if the insight is confirmed: the interface, the copy, the service, a process outside the product?

## Related cards
[[M-cjm]], [[M-research-types]], [[M-in-depth-interviews]], [[M-interview-analysis]], [[M-usability-testing]], [[M-ux-backlog]], [[M-design-thinking]], [[M-workshops]], [[M-audience-research]]
