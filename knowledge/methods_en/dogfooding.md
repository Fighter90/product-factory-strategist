---
id: M-dogfooding
lang: en
title: Ethnography, diary studies and dogfooding
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [research, options, validation]
tags: [ethnography, observation, contextual-interview, shadowing, diary-studies, dogfooding, insights, as-is]
related: [M-cjm, M-research-types, M-in-depth-interviews, M-interview-analysis, M-usability-testing, M-ux-backlog, M-design-thinking, M-workshops, M-audience-research]
---

# Ethnography, diary studies and dogfooding

## When to apply
When you need to see what people **do**, not what they say: when creating a new experience, redesigning, hunting for hidden problems and growth points, studying competitors through real use, or when the product cannot be reproduced in a lab. Dogfooding is a fast, cheap way to align the team and catch obvious problems before you go out to users. None of these methods replaces research with real customers.

## Core idea
- **Ethnography:** a qualitative method in which the researcher immerses themselves in the environment and life context of users and observes behavior and interaction with the product in real life. Pros: deep context, hidden needs, team empathy, real actions captured. Cons: resource-heavy, small samples, the observer's presence affects behavior, the risk of interpreting through one's own experience, and access to the real environment is not always available.
- **Types of observation** (axes): field (a natural setting) / lab (controlled); participant (the observer tries it themselves) / non-participant; overt (the participant knows) / covert (the purpose is not disclosed — requires ethical and legal review).
- **Forms:** passive observation; moderated (rare non-leading questions: "what did you just think?"); provoked ("imagine the courier is 20 minutes late"); a contextual interview (the person shows and explains as they go — "memory lies, behavior doesn't"); shadowing (accompanying a person through a shift or a day); diaries.
- **Diary study:** the participant records their own experience over time (text, screenshots, video, voice notes, short surveys). Fits habits, usage triggers, learning and adaptation, and changes in attitude toward the product. Variants: capture in the moment (more detail, but it affects the situation) and "snippets" with a detailed review at the end of the day (fewer distortions, gaps are possible).
- **Dogfooding (eat your own dog food):** the team uses its own product as an end user. Needed when there is a prototype that users have not seen yet; after UX tests before rollout; for aligning understanding and empathy. Kinds: field (a real, living need) and lab (scripted cases, an artificial need); team and individual.
- **Limits of dogfooding:** employees ≠ real users (they know the product, have different motivation, and get habituated to bugs); there is not enough depth for expert tools (you cannot "pretend to be a doctor"); without structure it is ineffective.

## Procedure

### A. Field observation
1. A goal phrased as a question and an observable behavior: "how do sellers photograph and publish an item", not "go see what they do".
2. Format: field/lab, participant or not, overt or not. Rules: do not prompt, minimal interference, do not hunt for confirmation of the hypothesis, watch non-verbal cues.
3. Segment and sample: usually 5–7 people per segment; recruit people who actually live with the task.
4. Ethics and law: voluntary participation, consent to recording and to the processing of personal data, confidentiality, the researcher's safety, unobtrusiveness. Without consent — do not record.
5. Scenario (45–90 min): warm-up → a tour of the environment → observation of real actions → rare contextual questions → debriefing.
6. Recording form (an adaptation of the course's "ad cabinet" sample) — a table by CJM stage:
   `Stage | User task | Stops (count) | Think-aloud (verbatim) | Errors / what went wrong | Insight`.
   Add photos/screenshots, quotes, and a description of the environment, devices and interruptions.
7. Check the equipment: recording, permission, charged devices, a note template.

### B. Team dogfooding
1. The goal and the critical scenarios (what we are testing and what counts as success).
2. Composition: different roles (PMs, designers, developers, analysts, QA, content), no more than 7–8 people per group.
3. Roles: moderator, executor, observer/note-taker. Run the scenarios in real time, without discussing them along the way.
4. Debrief: for each problem — is it a bug or UX; what to improve. Template: problem — insight — idea — priority.
5. "Grounding": file the tasks, lock in the agreements, extract the hypotheses that need to be tested on real users.

### C. Individual dogfooding
The goal and scenarios → instructions (where to test, where to send feedback and why) → a feedback form/table → analysis (groups, confusion, frequency, criticality, position on the CJM) → close the loop: thank the participants and share the results.

### D. Diary
The goal and format (text, voice, a survey, video) → the tool → recruit 7–15 people (some will drop out) with a short briefing at the kickoff meeting → reminders and follow-up questions; for a long study, pay in installments → a closing interview, feedback on the format, the reward.

### E. Analysis (shared by observation, dogfooding and diaries)
1. **Collect everything in one place:** notes, feedback, diaries, video/audio.
2. **First pass:** where something went wrong, where people got confused or stopped, emotions, repetitions, surprises, deviations from the plan, questions.
3. **Coding:** each observation → one headline/theme (sticky notes: take one, check the next one — does it fit, otherwise a new headline; a table: quote/observation + theme); reread with fresh eyes, check whether the themes can be merged. Record the observation "as on camera", without interpretation.
4. **Insight = observation + explanation + why it matters** (for example, the person completed the order but sat in silence — there was no confirmation — confidence drops and repeated actions increase).
5. **Hypothesis:** if the cause is known — what to change; if it is unknown — how to find out.
6. **Prioritization:** frequency, criticality for the user, criticality for the business; Kano, ICE/RICE, cost, simple voting. Important for dogfooding: distinguish professional noise ("we know how it should be done") from a real need.
7. **Patterns:** one observation is an accident; a repeat across ≥2–3 people is a candidate for a regularity. Distinguish behavioral, emotional, contextual, social and instrumental patterns.
8. **Output:** update [[M-cjm]] (as-is) and write the insights into [[M-ux-backlog]]; to test the hypotheses — [[M-usability-testing]] with real users.

### F. The double loop (the recommended combination)
Ethnography (the outer loop, real context) → dogfooding (the inner one, fast and regular) → a UX test (verification) → quantitative validation (A/B, analytics). Dogfooding's blind spots (ideal conditions, a single everyday context) are closed by ethnography; ethnography's blind spots (small scale, speed) — by dogfooding.

## Template / checklist

**Unified dogfooding record:** `Scenario step | What the participant did | Expectation | Fact | Emotion | Severity | Preliminary recommendation | Link to the recording/screenshot`.

**What to record:** where friction appeared; what triggered an emotion; where the person "got stuck"; where I don't trust the interface; what I expected and what actually happened (cognitive dissonance); what I did differently from the plan; what to improve right away.

**Health benchmarks of the practice (from the course notes, not the slides — calibrate them):** 80–100% of the team participating; 2–6 problems per person per session on active functionality; ≥70% of what is found makes it into the backlog; regularity (once a week / before each release).

**Launch checklist:** the goal and critical scenarios; composition and roles; consents and ethics; the recording tool; the template; the analysis plan; who files the tasks; how to close the feedback loop with the participants.

## Typical mistakes
| Mistake | Consequence | What to do |
|---|---|---|
| Interference, advice, asking questions ahead | The behavior changes | Minimal interference, neutral questions |
| Interpretation before recording the facts | Confirmation of your own hypothesis | Raw data first, "as on camera" |
| A short observation, one day, one context | Random conclusions | Plan several contexts and repeats |
| Focus only on the product, not the environment | Causes outside the interface are lost | Record the environment, interruptions, tools, people around |
| Averaging "all users" | A false portrait | Work with segments and stories |
| Dogfooding in ideal conditions (fast internet, two monitors) | No real friction | Include field and "extreme" conditions |
| One-off dogfooding "for show" with no tasks in the backlog | No change | Regularity, an owner, mandatory task filing |
| Treating the team as the target audience | Blind spots | Use it as a filter, not as a substitute for respondents |
| Covert observation without legal review | Ethical and legal risk | Informed consent or a legal sign-off |

## Questions that can change the decision
- Do you need a new experience and context (ethnography) or a check of a ready-made scenario (a UX test, dogfooding)?
- Is there access to the real environment and the participants' consent? If not — diaries or a lab format with simulated context.
- Does the team match the audience in experience? If not, dogfooding will provide only a filter of obvious problems.
- Are there resources for the analysis (time for coding and the owners)? Otherwise there will be more data than decisions.
- What exactly changes if the insight is confirmed: the interface, the text, the service, a process outside the product?

## Related maps
[[M-cjm]], [[M-research-types]], [[M-in-depth-interviews]], [[M-interview-analysis]], [[M-usability-testing]], [[M-ux-backlog]], [[M-design-thinking]], [[M-workshops]], [[M-audience-research]]
