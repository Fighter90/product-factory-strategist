---
id: M-in-depth-interviews
lang: en
title: In-depth interviews: preparation, conduct, ethics
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [research, validation]
tags: [in-depth-interviews, interview-guide, recruiting, interview-questions, research-ethics, consent, moderation, custdev, jtbd-interviews, synthetic-respondents]
related: [M-interview-analysis, M-audience-research, M-brief-hypotheses, M-research-types, M-jtbd, M-customers, M-quant-methods, M-ai-in-research, M-synthetic-respondents, M-usability-testing]
---

# In-depth interviews: preparation, conduct, ethics

## When to apply
You need to understand customer motives, behavior, barriers and language, or form and refine hypotheses (about the problem, about segments, about the solution) before expensive development. It is not suitable for estimating shares ("how many people are like this") or for a reliable demand forecast — those questions belong to the quantitative stage ([[M-quant-methods]]).

## Core idea
**An in-depth interview (IDI)** is a structured one-on-one conversation guided by a semi-structured guide; 40–60 minutes; 5–15 quality conversations with relevant respondents (informal team rule from the course: at least 10 per audience; if several services are being compared, fewer is acceptable with an explicit under-recruitment risk).

**Four types of interviews.**
| Type | Goal | What we listen for |
|---|---|---|
| Discovery | the picture of behavior, the causes behind decisions, goals and the desired outcome | context, situations, values |
| Problem | the real pain, true motives, how the problem is solved today | concrete cases, workarounds, the cost of the problem |
| Solution (concept test) | whether our offer solves an already-understood problem | reaction to the concept, barriers, comparison with the current solution |
| JTBD interview | the "job" for which the client "hires" the product | trigger, context, alternatives, outcome ([[M-jtbd]]) |

**Are hypotheses needed?** Yes, even for pure discovery: without goals and hypotheses you end up with a "heart-to-heart chat". Hypotheses set what to listen for but must not lead the respondent.

**What interviews can and cannot prove.**
- Can: reveal causes and mechanisms of decisions, client language, barriers and triggers, contested points of hypotheses; formulate hypotheses for testing.
- Cannot: prove prevalence ("most people want X"), segment size, willingness to pay as a number, or future behavior. People predict their own behavior poorly and tend to give socially desirable answers; therefore ask about *past behavior* and concrete cases, not about intentions.
- The outcome of an interview is a hypothesis with living examples, not a conclusion about the market ([[M-interview-analysis]]).

## Procedure
### 1. Preparation
1. Define the interview goal and hypotheses ([[M-brief-hypotheses]]); the decision the results will influence.
2. Desk research: open and internal information (analytics, support tickets, reviews, past research, [[M-research-types]]).
3. Internal expert interviews within the team (support, sales, account managers): especially important when respondents are rare or expensive.
4. Respondent profile and recruiting ([[M-audience-research]]): a screener with traps, mixed channels, exclusions (marketing professionals, recent study participants, people connected to the team), motivation, confirmation of time and format. Recruiting is the foundation of quality.
5. Write the guide (see the template). Pilot it on the first interviews: check duration and how clear the questions are; record the edits.
6. Prepare consent, recording equipment, the note format and data-retention rules (see "Ethics and consent").

### 2. Conduct
**Recruit-to-execution (show-up ≥ 80 %):** a reminder a day before the session (email + calendar invitation) and a second one about 2 hours before (messenger/SMS with the link and the moderator's contact); overbook by +20 % for no-shows; timebox and format communicated in advance; the incentive is paid on the day of the session — this builds willingness to participate again. Screener constructor (≤ 5 minutes to fill in, otherwise drop-off grows): (1) a kill-filter — one question on which the candidate is definitely OUT; (2) a behavioral block — frequency, scenario, time/money spend; (3) motivation/barrier — how they solve the task now; (4) a control trap ("choose option No. 3"); (5) contact + consent to recording. Metrics to watch: no-show above 20–30 % — double reminders and a waiting list; screener longer than 5 minutes — cut it down to "must-know" items.

**Pre-flight (24 hours before the first session):** the brief is final (goal, hypotheses, target audience, method); the respondent list n + 20 % and the slots; the guide in two forms (print + digital) with timecodes; recording — dual (local + cloud), free space checked; stakeholders have received the link to the schedule and the observation rules ("no prompting"). "Working bag": webcam, lavalier microphone, a second screen/tablet for notes (do not switch between windows during the conversation), a time tracker for the real duration of the blocks.

**Session structure:** warm-up → main part → close.
- *Warm-up:* introductions, a short off-topic conversation (icebreaking), format and purpose of the meeting, recording and confidentiality terms, "programming" (setting the context: answer in detail, there are no right answers). Online: sound/video check; offline: respondent comfort.
- *Main part:* blocks following the guide's topics, one question at a time, no interruptions, use pauses and probes. The "warm — deep — warm" arc for a 40-minute session: 0–3 icebreakers, 3–10 context and habitual processes, 10–25 deep "whys" (motivation, barriers), 25–35 concept/prototype (if there is one), 35–40 close.
- *Close* (checklist): warn about 5 minutes ahead; the "magic question" — what important thing did we fail to ask; specific thanks; what happens next with the results; clear terms and timing of the incentive; permission for re-contact.

**Question types:** open ("how do you solve X?"), neutral ("what do you think about…?"), probing ("why did you decide that?"), projective ("imagine the ideal process…"), evaluative (a rating + "why that rating"). *Stop-list:* hypothetical questions, closed questions, leading questions, statement-type questions, several questions in one, professional jargon; never answer for the respondent, never teach them, and don't be afraid of looking unprofessional.

**Techniques.**
| Technique | How | Why |
|---|---|---|
| Pause | after a question or a short answer, stay silent for 5–7 seconds | the respondent adds details on their own; do not help them "pull themselves together" |
| Echo | repeat the last 2–3 words with a questioning intonation | deepen the thought without asking a new question |
| Paraphrasing | "Did I get it right that…" | check understanding, help them structure the thought |
| Step-by-step reconstruction | "Let's go back to the moment: you opened the app… what did you see, what did you do, what did you think?" (you can sketch the stages together) | bypass memory distortions, get specifics instead of a general assessment |
| 5 whys | ask "why" after every answer until you reach the root cause | find the root cause |
| "Five-year-old child" | ask "obvious" questions | don't fill in for the respondent; be careful in B2B and with respondents whose time is expensive |
| Verification questions | "Do you always do this in similar situations?", "You said this was important but didn't do it — why?" | separate stated claims from actual behavior |

**Sensitive topics.**
- *Attitude to price:* approach "from the side". Not "how much would you be ready to pay?" but "tell me about the last service you paid for: what was it, why did you decide to pay, what do you think about paid subscriptions?".
- *Failures and sensitive matters:* normalization ("in previous interviews everyone gave different answers — how about you?"), projection ("why do you think many people find it hard to finish a course?"), self-disclosure (share a similar experience of your own).

**Difficult respondents.**
| Situation | What to do |
|---|---|
| Doesn't understand the question (often non-professional sellers) | name what you see ("you went quiet — what puzzled you?"), rephrase in the respondent's own slang |
| A negativist who criticizes everything | name the emotion, show that you heard it and recorded it; switch to something positive and come back to it later; offer to reschedule or end the session |
| Talks without stopping | move to a more directive style, join in and redirect ("this is important, but the next question matters even more…"), summarize briefly, remind them about the time, move on to the guide's key topics |
| Silent, answers in short phrases | give an example of other people's opinions, remind them of the purpose and that any opinion is valuable, that you are not evaluating them |
| B2B / "expensive" respondent | respect their time, phrase questions clearly, explain that you need exactly their experience |

**Capturing.** Recording the interview (with consent) is the primary source; notes are the second brain: warn the respondent about note-taking, capture quotes and observations, not interpretations (mark interpretations separately). Marks: "?" — to clarify later, "!" — a bright insight, "//" — your own comment. A three-column template (fact/quote, observation, comment); automatic time-stamping for quick lookup. Go through the notes within 15–30 minutes after the interview.

### 3. Right after
- Back up the recording (cloud + local) immediately, while the file is still "warm"; a lost recording = a lost insight.
- A metadata table: respondent id (no personal data), segment, slot, key insight in one line — this saves hours at the analysis stage.
- A hot summary (15 minutes): the 3 main observations, the unexpected, what to change in the guide.
- Transcription within 24 hours and hand-off to analysis ([[M-interview-analysis]]).
- The "field stage is closed" checklist: recordings and notes uploaded, access rights verified; the interview counter ≥ the minimum from the brief; incentives paid, consents stored; the team has received a short "first impressions" digest.

## Ethics and consent
Basic principles of research practice (the course fixed three of them explicitly: recording with a warning, the incentive, and permission for re-contact; the rest is the professional standard and legal requirements):
1. **Informed consent before the start:** who is running the interview, the purpose, the duration, what will be recorded, who will see the materials, how the results will be used, and that participation is voluntary — one can stop or skip a question without consequences. Record the consent (in writing or in the recording itself).
2. **Consent to recording and storage** must be obtained explicitly; the retention period and the circle of people with access are defined in advance.
3. **Personal data:** collect the minimum, store it separately from transcripts, anonymize it in reports (in Russia the requirements of Federal Law No. 152-FZ apply; for international data — local legislation as well).
4. **Confidentiality:** do not disclose the participant to colleagues or clients; quotes in the report carry no identifying details; honor NDAs and do not ask for confidential information about the respondent's employer.
5. **No deception or pressure:** do not make promises you cannot keep (including "your words will directly change the product"); never use an interview for sales.
6. **Incentive:** announce the terms and the payout date before the interview and honor them; the amount should be proportionate to the time and should not create an incentive to "give the right answers".
7. **Vulnerable groups and sensitive topics:** minors (parental consent), health, finances — only when necessary and with heightened caution; the right not to answer.
8. **Independence:** do not bend the interview to the customer's expectations; report the results "as is".

## Synthetic respondents and AI
Language models "playing" respondents generate plausible but *fictional* answers: they rely on generalized texts, not on the experience and context of real customers. Acceptable uses: *rehearsing the guide* (will the questions be understood), *inventing hypotheses and counterexamples*, *expanding the list of barriers* for subsequent checking with live people. Rules: (1) mark any such output "synthetic data — not customer data"; (2) never use it as evidence of demand, willingness to pay, segment size, or causes of behavior; (3) do not mix it with real quotes in a single report without labeling; (4) test every hypothesis with real respondents. More: [[M-synthetic-respondents]], [[M-ai-in-research]]. AI can also be used to transcribe and draft-cluster real transcripts, provided a human verifies the result and confidentiality is preserved (do not upload personal data to external services without consent).

## Template / checklist

**Interview guide (a skeleton for 45–60 minutes):**
| Block | Time | Content |
|---|---|---|
| 0. Introduction | 3–5 min | introductions, purpose, format, recording and confidentiality, consent, "there are no right answers" |
| 1. Warm-up | 5 min | who you are, your experience with the topic, a typical day, easy questions |
| 2. Context and the last case | 10–15 min | "recall the last time when…" — step-by-step reconstruction, trigger, alternatives |
| 3. Choice and barriers | 10–15 min | why they chose this solution, what got in the way, what they are unhappy with, what would be ideal |
| 4. Hypotheses / concept | 5–10 min | reaction to the concept or scenario (only after the spontaneous part, to avoid leading), "what puzzled you", comparison with the current solution |
| 5. Close | 3–5 min | "what did I fail to ask?", thanks, the next step, the incentive, re-contact |
A guide is good if: it has internal logic; every question is open; every question serves the goal; the key topics have backup probes; you can deviate from the plan when a valuable insight appears.

**Interviewer checklist:** stated the purpose, format and consent; kept the structure but stayed flexible; did not interrupt, evaluate or teach; captured quotes and emotions; asked one question at a time; checked stated claims with questions about real behavior; processed the notes within 30 minutes; wrote the hot summary.

## Typical mistakes
- No goals or hypotheses; a guide made of "general topics" or of closed questions.
- Leading questions ("it's convenient for you, right?"), several questions in a row, hinting at answers.
- The interview as a sale or a demo; defending your own idea from criticism.
- Asking about the future ("would you buy it?") instead of past behavior; taking stated claims for reality.
- Recruiting "your own people": colleagues, loyal customers, professional respondents.
- Fear of looking unprofessional and skipping "obvious" questions.
- Recording "by ear" without quotes; recording only what confirms the hypothesis.
- Missing consent and clear storage terms; leaks of personal data.
- On-the-fly interpretation and labels applied before analysis.
- A conclusion about prevalence drawn from a small series of interviews.

## Questions that can change the decision
- Do we need the cause (quality) or the scale (quantity)? If it is scale — interviews only as the first stage.
- How homogeneous is the audience: how many separate groups will need to be surveyed (10 respondents each)?
- How do we reach rare and expensive respondents (B2B, professional sellers)?
- What information is confidential and which consents are needed (recording, data, NDA)?
- Do we need observation or an in-context test instead of a retelling (if people "don't remember" or have grown used to putting up with the problem)?
- Are there enough resources for quality analysis ([[M-interview-analysis]]): without it, the interviews lose their meaning.

## Related maps
[[M-interview-analysis]], [[M-audience-research]], [[M-brief-hypotheses]], [[M-research-types]], [[M-jtbd]], [[M-customers]], [[M-quant-methods]], [[M-ai-in-research]], [[M-synthetic-respondents]], [[M-usability-testing]]
