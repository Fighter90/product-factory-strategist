---
id: M-usability-testing
lang: en
title: Usability testing — prototypes, moderated and unmoderated tests, metrics
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [options, validation, after-decision]
tags: [usability, ux-testing, prototype, moderated, unmoderated, rite, first-click, card-sorting, ux-metrics, severity]
related: [M-ux-heuristics, M-cjm, M-ux-backlog, M-design-thinking, M-mvp-pilots, M-quant-methods, M-product-metrics, M-in-depth-interviews, M-solution-design, M-brief-hypotheses]
---

# Usability testing: prototypes, moderated and unmoderated tests, metrics

## When to apply
When you need to check with real people whether an interface or scenario is understandable, and to see where and why people
make mistakes — before development (on a prototype) or after launch. A UX test answers "how" and "why", not "what will change
in the metric": a button color or an order-page variant chosen for conversion can only be settled by an experiment (A/B);
a UX test gives hypotheses and causes.

## Core idea
- **Moderated test** (qualitative): the researcher watches how the participant solves realistic tasks and probes "why".
  Needed for anything new, complex, branching, or a first concept; gives emotions and the mental model. Downsides: observer
  effect, social desirability, more expensive.
- **Unmoderated test** (quantitative "what" and "how much"): the participant follows a link on their own; the platform records
  clicks, time, answers. Fast, cheap, scalable; no way to probe, a flawed task ruins all the data, no context.
- **RITE**: after 2–3 sessions a critical problem is fixed immediately and the next participants see the new version.
  For prototypes only; requires an engaged designer.
- **Field / contextual** format — when the environment is critical (a courier on the move, poor signal, sun on the screen).
- Heuristics (inside the team, without users) — a quick filter before tests: [[M-ux-heuristics]].

**Method selection (by goal):**

| Question | Method |
|---|---|
| Will the block be noticed, will its value be understood, will it be used (a new block on a card) | Moderated |
| Why do people abandon the process halfway (statistics exist, the cause is unclear) | Moderated (analytics shows where, the test shows why) |
| Ease of use in real conditions (a courier: driving, sunlight, signal) | Field moderated / contextual interview |
| Do people understand the terms ("carbon footprint") | Interpretation test on a sample; moderated if you need to understand the thinking |
| Is an element noticeable, do people find the section | First click / 5-second test |
| Which of 2–3 variants is preferred | Preference (subjective); behavior — A/B only |
| How people group sections | Card sorting (open/closed) and tree testing |
| A simple linear scenario across 2–5 screens | Scenario-based unmoderated |
| Quick feedback on a prototype in progress | RITE, micro-checks (5–10 min) |
| Impact on conversion | Experiment only (A/B) |

## Procedure

### 1. Prototype preparation
1. A prototype is a way to fail cheaply, not a presentation: clickable screens, connected transitions, all scenario states
   (error, empty, loading, success). Tools: Figma (frames, auto-layout, design-system components, links between screens),
   a paper prototype, "Wizard of Oz" (a human imitates the system — for assistants, voice interfaces).
2. Fidelity follows the goal: checking comprehension of meaning — static frames are enough; checking the flow — a clickable path.
3. The "3-S" rule for a task: one path, a short task, a concrete goal; the scenario runs without dead ends.
4. Safety net: PNG slides of all states, the link checked in incognito mode, a dry run with a colleague.
5. Course example (one-click resume, lecture data): the test showed that participants didn't understand the resume needed to be
   published in the chat and thought it had already been sent to one employer; a separate "draft → publish" screen was perceived
   more easily, and for the A/B the lecture reports the resume base grew +158% and purchases +142%. Conclusion: the test found
   the cause, the experiment measured the effect.

### 2. Moderated test
1. **Brief:** which question, which decision depends on it, which flow, which segments. Break the user flow into stages with
   checkpoints.
2. **Hypotheses** (format: problem + place in the scenario + expected observable behavior; not "the user will understand the
   interface" but "notices the filters button within the first 5 s", "chooses the pickup point in ≤20 s without backtracking").
   No more than three per session; one hypothesis — one task.
3. **Guide:** hypotheses → intro interview (experience, habits, context) → task wording → success criteria (measurable, set
   before the test) → probe questions for the hypotheses → closing questions. Map "task → steps → visible result".
4. **Task wording:** context ("you decided to take up running…") + motive + constraints; the goal contains no names of interface
   elements ("click 'Checkout'" is forbidden); identical text for all participants; don't invent the context, don't lose it.
   Bad: "Buy sneakers in the app." Better: the situation, why, budget/preferences, the result.
5. **Recruiting:** segment and behavioral profile, the right device; exclude UX/IT professionals unless they are the target
   audience; a +20% no-show buffer; consent to recording and personal-data processing. Sample: 5 people per segment (Nielsen's
   estimate ~80% of problems); 5–8 for a first test of a complex interface; more for a 10–15-screen scenario or several segments.
6. **Pilot** on a colleague / one respondent: typos, timing, links, terminology. Session ≤45 min, task ≤10 min, ≤3 scenarios.
7. **Session** (structure): greeting and role ("we test the product, not you") 2–3 min → explaining the process and the recording
   1 min → intro interview 3–5 min → task → execution with think-aloud → follow-up "why" questions → difficulty scale (SEQ) +
   the open question "what would you change first" → thanks.
8. **Moderator behavior (the course's 10 rules):** talk ~20% of the time — listen a lot; don't hint; don't ask leading questions;
   hold a pause (~5 s after an action); ask for think-aloud; neutral face and voice (no "great!", no frowning at mistakes);
   don't defend the interface ("it's by design" is a hint); manage the pace (don't rush, don't drag); don't cut off final
   impressions (the last emotions are the most valuable); always record. Probing without hinting: "what did you expect to see?",
   "what would help here?", "what other options come to mind?"; questions about a **specific interface element only if the
   participant mentioned it themselves**; third-person questions ("what do you think others would do?") reduce social
   desirability; with a broken prototype, show the PNG and ask "what would you do next?", and mark it as a technical glitch.
   **Probing techniques:** "soft echo" (repeat the last words with a questioning intonation); "clarifying chain" (a series of
   short "whys", one step at a time); "looping back" (return to something said earlier and compare it with the current action);
   "removing guilt" ("this spot confuses many people — you're not alone"); "mirroring emotions" (name what is observable:
   "you paused / frowned — what happened?").
   **Nonverbal friction signals** (record as an observation, not as a cause-fact): leaning closer to the screen, the cursor
   hovering in one spot for a long time, a nervous smile, frequent glances at the moderator, "holding one's breath" before a click.
9. **Capturing in the moment:** `time | step | action/quote | mark (red — failure, yellow — friction, green — "wow") | severity`.
   Record words and behavior, emotions, nonverbals, participant questions.
10. **Same-day analysis:** time-coded matrix → grouping identical problems → prioritization → patterns (≥2 participants —
    a candidate, 3 — a pattern) → cause → business effect.
11. **Decision after the test:** (A) refine and repeat if critical problems remain; (B) proceed to development if the hypotheses
    are confirmed and errors are minimal; (C) rebuild the scenario if the concept itself is unclear / the mental model doesn't match.
12. **Retest** after fixes; the date and the owner are assigned immediately.

**Four "pain zones" of a moderated test and defenses against them:**
| Risk zone | What happens | Damage control |
|---|---|---|
| Laboratory feel | A home laptop instead of the real environment | Go "into the field" where possible; otherwise model contextual pressure (time, noise, parallel tasks) |
| Prototype technical failure | The mockup "breaks" — the participant mistakes a prototype bug for a UX bug | Atomic paths, check every link before the session, a PNG backup and the question "what would you do next?" |
| Social desirability | "Everything is clear, great product" | The setup "we test the interface, not you"; third-person questions |
| Observer effect | Fewer mistakes in the researcher's presence | A remote session, the moderator silent ~80% of the time, reminding only about think-aloud |

**"Anti-blunder" — 5 steps before every session:** (1) a check-run of the prototype (all links and animations, 5 minutes);
(2) a control timer (task ≤10 minutes, otherwise split it); (3) a control question in the guide (an attention trap);
(4) the observation sheet `time | step | action | mark | severity` already open; (5) plan "B" — a folder with PNGs and a short
script in case of a failure. Check the prototype link in incognito mode.

### 3. Unmoderated methods

| Method | Goal | What we measure | Key rules |
|---|---|---|---|
| Interpretation test | Understanding the meaning of a text/icon/badge | Share of correct readings from coding open answers (correct / partial / incorrect / didn't understand) | Ask "what does … mean", not "what does the button do"; short exposure; a "whitelist" of readings prepared in advance |
| First click | Noticeability / findability of an element | Success (first click in the target zone), time to click (median/mean), misses, click map | No element name in the task; when comparing screens, compute significance |
| 5-second test | First impression, readability | What was recalled, how the message was understood, whether the CTA was remembered | Don't warn that they should memorize; ≤3–5 questions; 10–20 s for complex screens |
| Preference (side-by-side) | Which variant is subjectively liked / clearer / more trustworthy | Share of choosers, significance of the difference | Variants differ in one noticeable detail; one criterion per question; random order; 2–3 variants; don't compare against a third-party service; result ≠ behavior (A/B may disagree) |
| Card sorting open / closed / reverse (tree test) | How people group entities; checking the hierarchy | Similarity matrix, dendrogram; for tree test — findability success | 200–300 respondents for mass audiences per the course; open — when the structure is unknown |
| Scenario-based | A short simple flow | Success rate, time, dropout, subjective ease | Preferably a finished clickable prototype; the more branching, the more sense a moderated test makes |

General rules: greeting and context, the task, a thank-you screen, description of the audience and quotas; a **honeypot /
control question** and a minimum completion time to filter out the inattentive; branch logic (routing by answers) and display
logic (showing/hiding questions on the screen); when comparing variants — a significance test (chi-square / z-test for shares)
before drawing conclusions. Volume: the course's "working number" for mass segments is about 300 responses; fewer for narrow
B2B segments. The 95% confidence interval of a share: `±1.96·√(p(1−p)/n)` (at n=300, p=0.5 — about ±5.7 pp).

Course threshold benchmarks (calibrate per product; these are not laws): interpretation ≥80% correct; first click ≥80% success
and time ≲2 s, ≤60% — poorly noticeable; 5-second ≥70% named the product correctly; preference — a difference >10 pp at p≤0.05
is decisive, <5 pp is a tie.

### 4. Test metrics (formulas)
| Group | Metric | How to compute |
|---|---|---|
| Effectiveness | Task success | Scale 0 — failed, 1 — with errors, 2 — first try; Success Rate = completers / valid participants |
| Productivity | Time on task | Median over the valid ones (the mean is distorted by outliers); number of steps, backtracks, wrong attempts |
| Satisfaction | Subjective difficulty | Expected (before) and actual (after) on a scale; SEQ (7 points) — mean over the valid ones; the "expectation − actual" gap |
| Overall score | SUS (after the session) | 0–100 scale from the standard questionnaire |

Validity: exclude records faster than the minimum time and those failing the trap question; compute on the valid ones and state
n. Target values (e.g., Success ≥80%, SEQ ≥5, median ≤60 s) are set **before launch** for the specific scenario.

### 5. Problem prioritization
A problem is not only a failed task: confusion despite success, an extra step/backtrack, a pause >3 s, a participant question,
a break of a habitual pattern. Severity (shared scale with [[M-ux-heuristics]]): 0 — cosmetic (the font jumps on focus);
1 — slows down, doesn't break (scroll longer than expected); 2 — friction (a noticeable share takes a wrong path, e.g. ~30% of
clicks off-target); 3 — blocks part of the users (~50% don't see the target action); 4 — blocks the task/revenue/release.
Rule: severity ≥3 or frequency ≥50% first; below that — the "gray tail". Course formula: Severity = Impact × Frequency ×
Business risk (normalize to 0–4).

**Test replicability:** the same guide, identical task wording and the same order for all participants — otherwise results are
not reproducible and version/before-after comparisons lose meaning.

### 6. One-slide report
The feature and the test goal → metrics fact vs target (state n) → top problems (severity ≥3) with participant counts and a
quote with a timecode → fixes, owner, deadline → retest date. Executive summary: 5–7 problems with impact and recommendations;
details and videos in the appendix. Every claim is tied to an observation/quote/metric.

## Template / checklist

**Guide (skeleton):** goal and decision | hypotheses (≤3) | segment and recruiting | intro questions | tasks verbatim |
expected path and success signals | post-action questions | closing questions | plan "B" (PNGs) | timecode table.

**Observation record:** `Participant | Time | Step | What they did/said (verbatim) | Mark | Severity | Cause hypothesis
(kept separate from the fact)`.

**Before launch:** hypotheses are measurable; tasks without UI terms; the prototype passed a dry run; recording and consent;
pilot; the notes template is open; a control question (unmoderated); metric thresholds fixed.

## Typical mistakes
| Mistake | Effect | How to avoid |
|---|---|---|
| Hints and leading questions ("what about via search?") | Distorted behavior | "What other options come to mind?" |
| Button/section names in the task | Tests reading, not findability | Describe the goal and the context |
| Questions about elements the participant never mentioned | Imposing | Ask only about what was said/done |
| Conclusions from the respondent's words only | Words and behavior diverge | Words + actions + metrics |
| Not recording / not probing causes | Conclusions can't be proven | Recording, timecodes, a "why" after a step |
| Too many hypotheses/tasks | Fatigue, shallowness | ≤3 scenarios, ≤45 min |
| No trap question in an unmoderated test | Bots and the inattentive ruin the data | Control question, minimum time |
| Preference test with similar variants and no significance | False winner | One noticeable difference, compute significance |
| Testing on colleagues / your own team | Real barriers invisible | Recruit the target audience |
| Treating a UX-test result as a conversion effect | False confidence | Confirm with an experiment |
| A 30-slide report with no owner and no retest date | No decisions get made | One-pager + owners + a retest date |

## Questions that can change the decision
- The decision that depends on the test: go to development, redraw, or kill the idea? What result threshold changes it?
- Is the scenario simple and linear (unmoderated is enough) or with many branches (moderated needed)?
- Is there a ready prototype, or is a [[M-ux-heuristics]] review and a cheap paper version needed first?
- Does the real context matter (street, warehouse, signal)? If yes — a lab session will distort.
- Is the target audience reachable for recruiting within the deadline? Otherwise the result is a hypothesis.
- Is a quantitative estimate of the effect on the metric needed? Then after the test — [[M-mvp-pilots]] / an experiment.

## Related maps
[[M-ux-heuristics]], [[M-cjm]], [[M-ux-backlog]], [[M-design-thinking]], [[M-mvp-pilots]], [[M-quant-methods]], [[M-product-metrics]], [[M-in-depth-interviews]], [[M-solution-design]], [[M-brief-hypotheses]]
