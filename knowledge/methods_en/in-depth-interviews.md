---
id: M-in-depth-interviews
lang: en
title: In-depth interviews: preparation, conducting, ethics
course: ux
sources: ["EN mirror of the RU methodology card M-in-depth-interviews (knowledge/methods/in-depth-interviews.md); original sources are listed in the RU card"]
stages: [research, validation]
tags: [in-depth-interviews, guide, recruiting, questions, ethics, consent, moderation, custdev, jtbd-interviews, synthetic-respondents]
related: [M-interview-analysis, M-audience-research, M-brief-hypotheses, M-research-types, M-jtbd, M-customers, M-quant-methods, M-ai-in-research, M-synthetic-respondents, M-usability-testing]
---

# In-depth interviews: preparation, conducting, ethics

## When to apply
You need to understand the motives, behaviour, barriers and language of customers, and to form or refine hypotheses (about the problem, segments, solution) before expensive development. Not suitable for estimating shares ("how many such people exist") or for a reliable demand forecast — those questions belong to the quantitative stage ([[M-quant-methods]]).

## Essence
**An in-depth interview (IDI)** — a structured 1-on-1 conversation following a semi-structured guide; 40–60 minutes; 5–15 quality conversations with relevant respondents (the course team's informal rule: at least 10 per audience; if several services are compared, fewer is acceptable with an explicit risk of under-recruitment).

**Four kinds of interviews.**
| Kind | Purpose | What we listen for |
|---|---|---|
| Discovery | the picture of behaviour, the reasons for decisions, goals and the desired outcome | context, situations, values |
| Problem | the real pain, the true motives, how the problem is solved now | real cases, workarounds, the cost of the problem |
| Solution (a concept test) | whether our offering solves an already-understood problem | the reaction to the concept, barriers, comparison with the current solution |
| A JTBD interview | the "job" for which the customer "hires" the product | the trigger, context, alternatives, outcome ([[M-jtbd]]) |

**Are hypotheses needed?** Yes, even for pure discovery: without goals and hypotheses you get "a heart-to-heart talk". Hypotheses set what to listen for but must not lead the respondent.

**What interviews can and cannot prove.**
- Can: uncover the reasons, the mechanisms of decisions, the customer's language, barriers and triggers, the contentious spots in hypotheses; formulate hypotheses for testing.
- Cannot: prove prevalence ("most people want X"), the segment size, willingness to pay as a number, future behaviour. People are bad at predicting their behaviour and prone to socially desirable answers; that is why we ask about *past behaviour* and specific cases, not intentions.
- The result of an interview is a hypothesis with vivid examples, not a conclusion about the market ([[M-interview-analysis]]).

## Procedure
### 1. Preparation
1. Define the goal and hypotheses of the interview ([[M-brief-hypotheses]]); the decision the results will influence.
2. Desk research: open and internal information (analytics, support, reviews, past studies, [[M-research-types]]).
3. Expert interviews inside the team (support, sales, managers): especially important if the respondents are rare or expensive.
4. The respondent profile and recruiting ([[M-audience-research]]): a screener with traps, mixed channels, exclusions (marketing professionals, recent participants, people connected to the team), motivation, confirmation of the time and format. Recruiting is the foundation of quality.
5. Write the guide (see the template). Trial-run it on the first interviews: check the duration and the clarity of the questions; record the edits.
6. Prepare the consent, the recording equipment, the note format, the data storage rules (see "Ethics and consent").

### 2. Conducting
**Recruit-to-execution (show-up ≥ 80%):** a reminder a day before the session (an email + a calendar invitation) and a second one ~2 hours ahead (a messenger/SMS with the link and the moderator's contact); recruit with a +20% buffer for no-shows; the time-box and format communicated in advance; the incentive is paid on the day of the session — this builds the willingness to participate again. The screener constructor (≤ 5 minutes to fill, otherwise the drop-off grows): (1) a kill filter — one question by which the candidate is definitely OUT; (2) a behavioural block — frequency, scenario, time/money spent; (3) motive/barrier — how they solve the task now; (4) a control trap ("choose option No. 3"); (5) contact + consent to recording. The metrics to watch: a no-show above 20–30% — double reminders and a waiting list; a screener longer than 5 minutes — cut it down to "must-know".

**Pre-flight (24 hours before the first session):** the brief is final (the goal, hypotheses, the target audience, the method); the respondent list n + 20% and the slots; the guide in two forms (print + digital) with time codes; recording — dual (local + cloud), the free space checked; the stakeholders have received the link to the schedule and the observation rules ("do not prompt"). The "working bag": a webcam, a lavalier microphone, a second screen/tablet for notes (no switching between windows during the conversation), a time tracker for the real duration of the blocks.

**The session structure:** warm-up → main part → closing.
- *Warm-up:* introductions, a little off-topic talk (icebreaking), the format and purpose of the meeting, the terms of recording and confidentiality, "programming" (setting the context: answer in detail, there are no right answers). Online: a check of audio/video; offline: the respondent's comfort.
- *Main part:* blocks by the guide's topics, one question at a time, no interrupting, use the pause and clarifications. The "warm — deep — warm" pattern for 40 minutes: 0–3 icebreakers, 3–10 context and habitual processes, 10–25 the deep "whys" (motivation, barriers), 25–35 the concept/prototype (if any), 35–40 closing.
- *Closing* (a checklist): warn ~5 minutes ahead; the "magic question" — what important thing we failed to ask; specific gratitude; what will happen next with the results; the clear terms and timing of the incentive; permission for a follow-up contact.

**Question types:** open ("how do you solve X?"), neutral ("what do you think about…?"), clarifying ("why did you decide that?"), projective ("imagine the ideal process…"), evaluative (a rating + "why that rating"). *The stop-list:* hypothetical, closed, leading, statement-confirmation questions, several questions in one, professional jargon; do not answer for the respondent, do not teach, do not fear looking unprofessional.

**Techniques.**
| Technique | How | Why |
|---|---|---|
| The pause | after a question or a short answer, stay silent for 5–7 seconds | the respondent adds details themselves; do not help them "pull themselves together" |
| The echo | repeat the last 2–3 words with a questioning intonation | deepen the thought without a new question |
| Paraphrasing | "Did I understand correctly that…" | verify understanding, help structure |
| Step-by-step reconstruction | "Let's return to the moment: you opened the app… what did you see, what did you do, what did you think?" (you can sketch the stages together) | bypass the distortions of memory, get specifics instead of a general assessment |
| The 5 whys | ask "why" on each answer down to the root cause | find the root cause |
| "A five-year-old child" | ask "obvious" questions | do not fill in for the respondent; be careful in B2B and with the respondent's expensive time |
| Verification questions | "Do you always do this in similar situations?", "You said it matters, but you didn't do it — why?" | separate the stated from the actual behaviour |

**Delicate topics.**
- *The attitude to price:* come at it "from the side". Not "how much are you ready to pay?", but "tell me about the last service you paid for: what was it, why did you decide to pay, what do you say about a paid subscription?".
- *Failures and the sensitive:* normalization ("in the past interviews everyone gave different answers, how about you?"), projection ("why do you think many people find it hard to finish a course?"), self-disclosure (share a similar experience of your own).

**Difficult respondents.**
| Situation | What to do |
|---|---|
| Doesn't understand the question (often non-professional sellers) | name what you see ("you paused — what put you off?"), rephrase in the respondent's slang |
| Is negative and trashes everything | name the emotion, show that you heard and recorded it; switch to the positive and come back; offer to reschedule or end |
| Talks without stopping | move to a more directive style, join in and bring back ("this matters, but the question of… matters more"), summarize briefly, remind about the time, move to the guide's key topics |
| Is silent, answers briefly | give an example of other people's opinions, remind about the goal and that any opinion is needed, that nothing is being judged |
| B2B / an "expensive" respondent | respect the time, phrase clearly, explain that you need exactly their experience |

**Capturing.** The interview recording (with consent) is the primary source; the notes are the second brain: warn about the notes, capture quotes and observations, not interpretations (mark an interpretation separately). Labels: "?" — to clarify, "!" — a vivid insight, "//" — an own comment. A three-column template (fact/quote, observation, comment); auto-timestamping for quick search. Review the notes within 15–30 minutes after the interview.

### 3. Right after
- Back up the recording (cloud + local) immediately, while the file is "warm"; a lost recording = a lost insight.
- A metadata table: the respondent id (no personal data), the segment, the slot, the key insight in one line — it saves hours at the analysis stage.
- A hot summary (15 minutes): the 3 main observations, the unexpected, what to change in the guide.
- Transcription within 24 hours and the hand-off to analysis ([[M-interview-analysis]]).
- The "field stage closed" checklist: the recordings and notes uploaded, the access rights verified; the interview counter ≥ the brief's minimum; the incentives paid, the consents stored; the team sent a short "first impressions" digest.

## Ethics and consent
The basic principles of research practice (the course fixes recording with a warning, the incentive and the permission for a follow-up contact; the rest is the profession's standard and the requirements of the law):
1. **Informed consent before the start:** who conducts it, the purpose, the duration, what will be recorded, who will see the materials, how the results will be used, that participation is voluntary and one can stop or skip a question without consequences. Record the consent (in writing or on the recording).
2. **Consent to recording and storage** obtained explicitly; the storage period and the circle of access defined in advance.
3. **Personal data:** collect the minimum, store separately from the transcripts, de-identify in the reports (in Russia the requirements of Federal Law 152 apply; for international data — also the local legislation).
4. **Confidentiality:** do not reveal the participant to colleagues and clients; quotes in the report without identifying details; honour the NDA, do not ask for the confidential information of the respondent's employer.
5. **No deception and no pressure:** do not make promises that cannot be kept (including "your words will directly change the product"); do not use the interview for selling.
6. **The incentive:** state the terms and the timing of payment before the interview and deliver; proportionate to the time, no incentive to "give the right answers".
7. **Vulnerable groups and sensitive topics:** minors (parental consent), health, finances — only when necessary and with heightened care; the right not to answer.
8. **Independence:** do not bend the interview to the client's expectations; report the results "as they are".

## Synthetic respondents and AI
Language models "playing" respondents generate plausible but *fictional* answers: they draw on generalized texts, not on the experience and context of real customers. Acceptable uses: a *guide rehearsal* (will the questions be understood), *inventing hypotheses and counterexamples*, *expanding the list of barriers* for subsequent validation on living people. Rules: (1) label any such result "synthetic data — not customer data"; (2) do not use it as evidence of demand, willingness to pay, segment size or the causes of behaviour; (3) do not mix it in one report with real quotes without labelling; (4) test all hypotheses on real respondents. More: [[M-synthetic-respondents]], [[M-ai-in-research]]. AI can also be used for the transcription and draft grouping of real transcripts, provided there is human verification and confidentiality is honoured (do not upload personal data to external services without consent).

## Template / checklist

**The interview guide (a frame for 45–60 minutes):**
| Block | Time | Content |
|---|---|---|
| 0. Opening | 3–5 min | introductions, the purpose, the format, recording and confidentiality, consent, "there are no right answers" |
| 1. Warm-up | 5 min | who you are, your experience in the topic, a typical day, easy questions |
| 2. Context and the latest case | 10–15 min | "recall the last time when…" — a step-by-step reconstruction, the trigger, the alternatives |
| 3. Choice and barriers | 10–15 min | why you chose this solution, what got in the way, what you remained unhappy with, what would be ideal |
| 4. Hypotheses / concept | 5–10 min | the reaction to the concept or scenario (after the spontaneous part, so as not to lead), "what put you off", the comparison with the current solution |
| 5. Closing | 3–5 min | "what didn't I ask?", gratitude, the next step, the incentive, a follow-up contact |
A guide is good if: there is a logic; all the questions are open; every question works for the goal; the key topics have spare clarifications; one can deviate from the plan when a valuable insight appears.

**The interviewer's checklist:** stated the goal, format and consent; kept the structure but stayed flexible; did not interrupt, judge or teach; captured the quotes and emotions; one question at a time; tested the stated with questions about the real behaviour; processed the notes within 30 minutes; wrote the hot summary.

## Typical mistakes
- No goal and hypotheses; a guide made of "general topics" or of closed questions.
- Leading questions ("it's convenient for you, isn't it?"), several questions in a row, hinting at the answers.
- The interview as a sale or a demonstration; defending one's idea against criticism.
- Asking about the future ("would you buy it?") instead of past behaviour; taking the stated for the real.
- Recruiting "our own people": colleagues, loyal customers, professional respondents.
- The fear of looking unprofessional and skipping the "obvious" questions.
- Recording "by ear" without quotes; recording only what confirms the hypothesis.
- No consent and no clear storage terms; a leakage of personal data.
- Interpreting "on the fly" and labelling before the analysis.
- A conclusion about prevalence from a small series.

## Questions that can change the decision
- Do we need the cause (quality) or the scale (quantity)? If scale — interviews only as a first stage.
- How homogeneous is the audience: how many separate groups must be surveyed (10 per each)?
- How to reach the rare and expensive respondents (B2B, professional sellers)?
- Which information is confidential and which consents are needed (recording, data, NDA)?
- Is observation or a test in context needed instead of a story (if people "don't remember" or are used to enduring)?
- Are there enough resources for a quality analysis ([[M-interview-analysis]]): without it the interviews lose their meaning.

## Related maps
[[M-interview-analysis]], [[M-audience-research]], [[M-brief-hypotheses]], [[M-research-types]], [[M-jtbd]], [[M-customers]], [[M-quant-methods]], [[M-ai-in-research]], [[M-synthetic-respondents]], [[M-usability-testing]]
