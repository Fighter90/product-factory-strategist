---
id: M-usability-testing
lang: en
title: Usability testing — prototypes, moderated and unmoderated tests, metrics
course: ux
sources: ["EN mirror of the RU methodology card M-usability-testing (knowledge/methods/usability-testing.md); original sources are listed in the RU card"]
stages: [options, validation, after-decision]
tags: [usability, ux-test, prototype, moderated, unmoderated, rite, first-click, card-sorting, ux-metrics, severity]
related: [M-ux-heuristics, M-cjm, M-ux-backlog, M-design-thinking, M-mvp-pilots, M-quant-methods, M-product-metrics, M-in-depth-interviews, M-solution-design, M-brief-hypotheses]
---

# Usability testing: prototypes, moderated and unmoderated tests, metrics

## When to apply
When you need to check with real people whether an interface or a scenario is understandable, and see where and why people make mistakes — before development (on a prototype) or after launch. A UX test answers "how" and "why", not "what will change in the metric": choosing a button color or a checkout page variant for the sake of conversion can only be done with an experiment (A/B), while a UX test gives hypotheses and causes.

## Essence
- **A moderated test** (qualitative): the researcher watches how a participant solves realistic tasks and probes "why". Needed for new, complex, branching, first-concept things; yields emotions and the mental model. Downsides: the observer effect, social desirability, more expensive.
- **An unmoderated test** (quantitative "what" and "how much"): the participant follows a link on their own; the platform records clicks, time, answers. Fast, cheap, scalable; you cannot probe; a flawed task ruins all the data; no context.
- **RITE**: after 2–3 sessions a critical problem is fixed immediately and the next participants see the new version. Only for prototypes; requires the designer's involvement.
- **Field / contextual** format — when the environment is critical (a courier in motion, poor connection, sun on the screen).
- Heuristics (inside the team, without users) — a quick filter before tests: [[M-ux-heuristics]].

**Choosing a method (by goal):**

| Question | Method |
|---|---|
| Will the block be noticed, will the value be understood, will it be used (a new block on a card) | Moderated |
| Why do people abandon the process midway (the statistics exist, the cause is unclear) | Moderated (analytics — where, a test — why) |
| Usability in real conditions (a courier: driving, light, connection) | Field moderated / contextual interview |
| Do people understand the terms ("carbon footprint") | An interpretation test on a sample; moderated — if thinking needs to be understood |
| Is an element noticeable, is a section found | First click / 5-second test |
| Which of 2–3 variants is preferred | Preference (subjective); behavior — only A/B |
| How people group sections | Card sorting (open/closed) and tree testing |
| A simple linear scenario in 2–5 screens | Scenario-based unmoderated |
| Quick feedback on a prototype in progress | RITE, micro-checks (5–10 min) |
| Impact on conversion | Only an experiment (A/B) |

## Procedure

### 1. Preparing the prototype
1. A prototype is a way to fail cheaply, not a presentation: clickable screens, linked transitions, all states of the scenario (error, empty, loading, success). Tools: Figma (frames, auto layout, design system components, links between screens), a paper prototype, the "Wizard of Oz" (a human imitates the system — for assistants, voice interfaces).
2. Fidelity by goal: checking the understanding of meaning — static frames suffice; checking the flow — a clickable path.
3. The "3-S" rule for a task: one path, a short task, a concrete goal; the scenario completes without dead ends.
4. Backup: PNG slides of all states, the link checked in incognito mode, a dry run with a colleague.
5. A course example (one-click resume submission, lecture data): the test showed that participants did not understand that the resume needed to be published in the chat, and thought it had already been sent to one employer; a separate "draft → publish" screen was perceived more easily, and per the A/B results the lecture cites a +158% growth of the resume base and +142% in purchases. Conclusion: the test found the cause, the experiment measured the effect.

### 2. Moderated test
1. **Brief:** which question, which decision depends on it, which flow, which segments. Decompose the user flow into stages with checkpoints.
2. **Hypotheses** (format: problem + place in the scenario + the expected observable behavior; not "the user will understand the interface" but "notices the filters button within the first 5 seconds", "chooses a pickup point in ≤20 seconds without going back"). No more than three per session; one hypothesis — one task.
3. **Guide:** hypotheses → opening interview (experience, habits, context) → task wordings → success criteria (measurable, set before the test) → questions for checking hypotheses → closing questions. A map "task → steps → visible result".
4. **Task wording:** context ("you decided to take up running…") + motive + constraints; the goal without naming interface elements ("click 'Checkout'" is not allowed); identical text for all participants; do not invent context, do not lose it. Bad: "Buy sneakers in the app". Better: the situation, why, budget/preferences, the result.
5. **Recruiting:** the segment and behavioral profile, the device; exclude UX/IT professionals unless they are the target audience; a +20% buffer for no-shows; consent to recording and to personal data processing. Sample: 5 people per segment (the Nielsen estimate, ~80% of problems); 5–8 for first-time testing of a complex interface; more for a 10–15 screen scenario or several segments.
6. **Pilot** with a colleague/one respondent: typos, timing, links, terms. A session ≤45 min, a task ≤10 min, ≤3 scenarios.
7. **Session** (structure): greeting and the role ("we are testing the product, not you") 2–3 min → explaining the process and the recording 1 min → opening interview 3–5 min → the task → execution with think-aloud → follow-up "why" questions → a difficulty scale (SEQ) + the open question "what would you change first" → thanks.
8. **Moderator behavior (the course's 10 rules):** speak ~20% of the time — listen a lot; do not prompt; do not ask leading questions; hold the pause (~5 seconds after an action); ask to think aloud; a neutral face and voice (no "great!", no frowning at mistakes); do not justify the interface ("it's by design" — a hint); manage the pace (don't rush, don't drag); do not cut off the final impression (the last emotions are the most valuable); always record. Probing without hints: "what did you expect to see?", "what would help here?", "what other options come to mind?"; questions about **a specific interface element only if the participant mentioned it themselves**; questions in the third person ("how, in your opinion, would others act?") reduce social desirability; with a broken prototype, show the PNG and ask "what would you do next?", marking it as a technical failure.
   **Probing techniques:** "repeat with a soft phrase" (echo the last words with a questioning intonation); "a probing chain" (a series of short "whys", one step at a time); "a loop into the past" (return to something said earlier and compare with the current action); "removing the sense of guilt" ("this place confuses many people — you are not alone"); "mirroring emotions" (name what is observable: "you paused/frowned — what happened?").
   **Non-verbal signs of friction** (record as an observation, not as a fact-cause): leaning closer to the screen, the cursor hanging in one place for a long time, a nervous smile, frequent glances at the moderator, "holding one's breath" before a click.
9. **Capturing in the moment:** `time | step | action/quote | tag (red — failure, yellow — friction, green — "wow") | severity`. Record words and behavior, emotions, non-verbals, the participant's questions.
10. **Analysis the same day:** a time-coded matrix → grouping identical problems → prioritization → patterns (≥2 participants — a candidate, 3 — a regularity) → the cause → the business effect.
11. **The decision after the test:** (A) refine and repeat if there are critical problems; (B) go to development if the hypotheses are confirmed and errors are minimal; (C) rebuild the scenario if the very concept is unclear/the mental model does not match.
12. **Retest** after fixes; the date and the owner are assigned immediately.

**Four "pain zones" of a moderated test and protection against them:**
| Risk zone | What happens | Reducing the damage |
|---|---|---|
| Laboratory feel | A home laptop instead of the real environment | Where possible go "into the field"; otherwise model contextual pressure (time, noise, parallel tasks) |
| Prototype technical failure | The mock "breaks" — the participant confuses a prototype bug with a UX bug | Atomic paths, checking every link before the session, a PNG backup and the question "what would you do next?" |
| Social desirability | "Everything is clear, great product" | The framing "we are testing the interface, not you"; third-person questions |
| Observer effect | Fewer mistakes in the researcher's presence | A remote session, the moderator silent ~80% of the time, reminding only about think-aloud |

**The "anti-screw-up" — 5 steps before every session:** (1) a check-run of the prototype (all links and animations, 5 minutes); (2) a control timer (a task ≤ 10 minutes, otherwise cut it); (3) a control question in the guide (an attention trap); (4) the observation sheet `time | step | action | tag | severity` already open; (5) plan "B" — a folder with PNGs and a short script for the case of a failure. Check the prototype link in incognito mode.

### 3. Unmoderated methods

| Method | Goal | What we measure | Key rules |
|---|---|---|---|
| Interpretation test | Understanding the meaning of a text/icon/badge | The share of correct interpretations via coding open answers (correct / partial / incorrect / didn't understand) | The question "what does … mean", not "what does the button do"; a short display; a "white list" of interpretations prepared in advance |
| First click | Visibility/findability of an element | Success (the first click in the target zone), time to click (median/mean), misses, a click map | No element name in the task; when comparing screens, compute significance |
| 5-second test | First impression, readability | What was recalled, how the message was understood, whether the CTA was memorized | Do not warn that memorization is tested; ≤3–5 questions; 10–20 s for complex screens |
| Preference (side-by-side) | Which variant is subjectively liked/clearer/more trustworthy | The share of choosers, the significance of the difference | The variants differ in one noticeable detail; one criterion per question; random order; 2–3 variants; do not compare against a third-party service; the result ≠ behavior (A/B may disagree) |
| Card sorting open / closed / reverse (tree test) | How people group entities; checking the hierarchy | A similarity matrix, a dendrogram; for tree test — the success of finding an item | 200–300 respondents for a mass audience per the course; open — when the structure is unknown |
| Scenario-based | A short simple flow | Success rate, time, drop-off, subjective ease | A finished clickable prototype is desirable; the more forks, the more sense a moderated test makes |

General rules: a greeting and context, the task, a thank-you screen, a description of the audience and quotas; a **honeypot/control question** and a minimum completion time to filter out inattentive respondents; branching logic (branching by answers) and display logic (showing/hiding questions on screen); when comparing variants — a significance test (chi-square / a z-test for proportions) before conclusions. Volume: the course's "working number" for mass segments — about 300 responses; fewer for narrow B2B segments. The confidence interval of a proportion at 95%: `±1.96·√(p(1−p)/n)` (at n=300, p=0.5 — about ±5.7 pp).

Threshold benchmarks named in the course (calibrate to the product; these are not laws): interpretation ≥80% correct; first click ≥80% success and time ≲2 s, ≤60% — poorly noticeable; 5-second test ≥70% correctly named the product; preference — a difference >10 pp at p≤0.05 is decisive, <5 pp — a tie.

### 4. Test metrics (formulas)
| Group | Metric | How to compute |
|---|---|---|
| Effectiveness | Task success | A scale 0 — not completed, 1 — with errors, 2 — on the first try; Success Rate = those who completed / valid participants |
| Efficiency | Time on task | The median over valid participants (the mean is distorted by outliers); the number of steps, going back, wrong attempts |
| Satisfaction | Subjective difficulty | Expected (before) and actual (after) on a scale; SEQ (7 points) — the mean over valid ones; the gap "expectation − fact" |
| Overall score | SUS (after the session) | A 0–100 scale per the standard questionnaire |

Validity: exclude records faster than the minimum time and failing the trap; compute on valid ones, state n.
Target values (e.g., Success ≥80%, SEQ ≥5, median ≤60 s) are set **before launch** for a specific scenario.

### 5. Prioritizing problems
A problem is not only a failed task: confusion despite success, an extra step/going back, a pause >3 s, a participant's question, a violation of a habitual pattern.
Severity (a shared scale with [[M-ux-heuristics]]): 0 — cosmetic (a font jumps on focus); 1 — slows down, doesn't break (a scroll longer than expected); 2 — friction (a noticeable share takes a false path, e.g. ~30% of clicks miss); 3 — blocks part of the users (~50% don't see the target action); 4 — blocks the task/revenue/release. Rule: first of all severity ≥3 or frequency ≥50%; below that — the "gray tail". The course's formula: Severity = Impact × Frequency × Business risk (normalize to 0–4).

**Replicability of the test:** the same guide, identical task wordings and the same order for all participants — otherwise the results are not reproducible and comparing versions/before-after loses meaning.

### 6. One-slide report
The feature and the test's goal → metrics fact vs target (state n) → top problems (severity ≥3) with the number of participants and a quote with a time code → solutions, owner, deadline → the retest date. Executive summary: 5–7 problems with impact and recommendations; details and video — in the appendix. Every statement is tied to an observation/a quote/a metric.

## Template / checklist

**Guide (skeleton):** the goal and the decision | hypotheses (≤3) | segment and recruiting | opening questions | tasks verbatim | the expected path and success signals | questions after an action | closing questions | plan "B" (PNG) | a time-code table.

**Observation record:** `Participant | Time | Step | What they did/said (verbatim) | Tag | Severity | Cause hypothesis (separate from the fact)`.

**Before launch:** hypotheses are measurable; tasks without UI terms; the prototype passed a dry run; recording and consent; a pilot; the notes template is open; a control question (unmoderated); metric thresholds fixed.

## Typical mistakes
| Mistake | Effect | How to avoid |
|---|---|---|
| Prompts and leading questions ("what about via search?") | Distorted behavior | "What other options come to mind?" |
| Button/section names in the task | The test checks reading, not findability | Describe the goal and the context |
| Questions about elements the participant did not mention | Imposing | Ask only about what was said/done |
| Conclusions only from the respondent's words | A mismatch of word and behavior | Words + actions + metrics |
| Not recording/not probing causes | Conclusions cannot be proven | Recording, time codes, a "why" after a step |
| Too many hypotheses/tasks | Fatigue, superficiality | ≤3 scenarios, ≤45 min |
| No trap in an unmoderated test | Bots and inattentive respondents ruin the data | A control question, a minimum completion time |
| A preference test with similar variants and no significance | A false winner | One noticeable difference, compute significance |
| Testing on colleagues/your own team | Real barriers are invisible | Recruit the target audience |
| Equating a UX test result with a conversion effect | False confidence | Confirm with an experiment |
| A 30-slide report without an owner and a retest date | No decisions are made | A one-pager + owners + a retest |

## Questions that can change the decision
- The decision that depends on the test: go to development, redraw, or close the idea? Which result threshold changes it?
- Is the scenario simple and linear (unmoderated suffices) or full of forks (moderated needed)?
- Is there a ready prototype, or is a [[M-ux-heuristics]] review and a cheap paper version needed first?
- Does the real context matter (a street, a warehouse, connection)? If yes — a lab will distort.
- Is the target audience reachable for recruiting within the deadline? Otherwise the result is a hypothesis.
- Is a quantitative estimate of the effect on a metric needed? Then after the test — [[M-mvp-pilots]] / an experiment.

## Related cards
[[M-ux-heuristics]], [[M-cjm]], [[M-ux-backlog]], [[M-design-thinking]], [[M-mvp-pilots]], [[M-quant-methods]], [[M-product-metrics]], [[M-in-depth-interviews]], [[M-solution-design]], [[M-brief-hypotheses]]
