---
id: M-interview-analysis
lang: en
title: Analysis and presentation of in-depth interview results
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [research, options, validation]
tags: [interview-analysis, coding, categories, insights, evidence-strength, reporting, socialization, synthetic-respondents]
related: [M-in-depth-interviews, M-audience-research, M-brief-hypotheses, M-quant-methods, M-jtbd, M-cjm, M-problem-design, M-customers, M-ai-in-research, M-synthetic-respondents, M-source-criticism]
---

# Analysis and presentation of in-depth interview results

## When to apply
A series of interviews has been conducted (or other qualitative data is available: open-ended survey answers, diaries, support tickets), and it needs to be turned into an explanatory model, insights and recommendations — without losing information and without promising the team what qualitative data cannot deliver.

## Core idea
**Analysis is not a formality.** A set of interviews without analysis is just a set of stories: its conclusions are easy to dismiss. Analysis creates an explanatory model that the product moves forward on, and it protects against lost insights and against fitting the data to expectations.

**Source data after the interviews:** the recording, the transcript, the notes (protocol). Work with all three; recordings are made with the respondent warned in advance.

**Stages of analysis.**
1. *Immersion:* re-read the notes and transcripts, re-listen to the interviews, go through each respondent and mark what matters; build the complete picture of the series.
2. *Coding:* label fragments with short tags (codes) so that similar thoughts of different respondents can be compared. A code captures the meaning ("distrust of small banks"), not a retelling.
3. *Building categories:* group the codes into broader themes/patterns that explain the behavior or values of the group (for example, codes about sellers' attitudes toward credit buyers → the category "sellers treat a buyer with a loan differently"; codes about handing over cash at an ATM → "fears during the transaction"). Keep opposing categories too (praise for simplicity / complaints about complexity).
4. *Interpretation and conclusions:* connect the categories with each other and explain why users behave this way; formulate insights and research findings.

**Example of a code and a category from the course (car deals bought on credit):**
| Quote (meaning) | Code | Category |
|---|---|---|
| "you can ask buyers with a loan to pay more" | sellers' negative attitude toward selling on credit | sellers treat a buyer with a loan differently |
| "I don't care where the money comes from, the transfer is what matters" | neutral attitude | sellers treat a buyer with a loan differently… |
| "the rate depends on which bank you use most often" | wrong beliefs about how the rate is computed | myths and low financial literacy |
| "the money was deposited at an ATM, then the sale contract was signed" | handing over cash at an ATM | fears during the transaction |
| "I don't want small banks — what if they close" | distrust of small banks | fears during the transaction |

## Evidence strength: what N interviews give
Principles: (1) qualitative data describes *variety and mechanisms*, not frequencies; (2) sample homogeneity matters more than its size; (3) a conclusion is stronger if confirmed by an independent source (triangulation).
| Volume and source | What you can claim | What you cannot |
|---|---|---|
| 1–4 interviews | individual stories, examples of barriers, hypotheses to test | "a pattern", "typical" |
| 5–9 interviews of one segment | the first recurring themes; a list of behavior variants; the clients' language | shares, ranking by frequency, segment comparison |
| ~10–15 interviews on a homogeneous audience (course guideline) | stable themes within the group; when new interviews stop bringing new themes (saturation) — a sign of sufficiency for a *qualitative* goal | prevalence in the population |
| Interviews + behavioral data / desk research / support | a hypothesis with confirmation from an independent channel (triangulation) | effect size |
| Interviews → survey / A/B with a pre-set threshold | prevalence, segment size, significance of the differences | — |
A handy grading of insights for the report: **L0** — a single observation; **L1** — recurring within a series inside a segment; **L2** — confirmed by an independent source; **L3** — confirmed quantitatively. Decisions with a high cost of error rest on L2–L3.

**Wording.** Never present interview results in percentages ("80% said…") — the team will get a false sense of statistics. Write: "almost all…", "some…", "two distinct approaches: … and …", "this series did not contain…". If a count is quoted, only as "x out of n" and only to show breadth, with a note that this is not prevalence.

## Procedure
1. **Return to the goals, hypotheses and the plan for using the results** — otherwise you will get lost in the volume. Write out the research questions and hypotheses, and what would confirm or refute them.
2. **Prepare the materials (transcription pipeline within 24 hours):** export the recordings → auto-transcription → cleaning (filler words, masking of personal data) → time-code synchronization (quote ↔ time) → upload to the team's shared storage. Plus notes and recordings; respondent labels (no personal data). Dual recording (local + cloud) is checked right after the session: a lost file = a lost insight.
3. **Immerse:** go through all the interviews, mark the vivid and the debatable moments, write "hot" summaries for each (three questions: what surprised you; what matched or diverged from the hypothesis; what to clarify in tomorrow's guide).
4. **Code:** for each interview, isolate the meaningful fragments and assign codes (if an interview is long, first quotes, then codes). Same meaning — same code. Keep the codebook (a list of codes with a definition, an example quote and usage conditions) in a table: quote — code — respondent — time. Code the debatable/"odd" answers too — sometimes that is an unexpected segment. Don't inflate the codebook at the start: 6–8 top categories, with detail added as the work proceeds.
5. **Group into categories:** cluster the codes; name the categories; single out the competing ones; keep 2–3 strong quotes per category as evidence (density guideline: 3–5 quotes per code — fewer means an "orphan code", more means oversaturation). For working with the team — a board (Miro, FigJam) with cards.
5a. **Check the reliability of coding:** code part of the material in pairs (one reads aloud, the other independently names the codes) and compare; if inter-coder agreement is below ~0.7 on Cohen's kappa — rewrite the code definitions and re-code the disputed fragments. Solo coding without verification is a frequent source of subjectivity.
6. **Interpret:** connect the categories ("fear of X explains behavior Y at stage Z"); map them onto segments and journey stages; check against the original hypotheses (confirmed / refuted / no data); write out the unplanned findings separately.
7. **Grade the strength of each conclusion** (L0–L3) and state what data would strengthen it (a survey, an A/B, a behavioral data pull).
8. **Formulate insights and recommendations** (template below): "observation → interpretation → implication for the product → how to verify".
9. **Assemble the artifact:** introduction (goal, tasks, hypotheses, sample, method); main body (behavior, stories, quotes, answers to the questions); conclusions (the essentials, briefly). Format — a board, a presentation or a framework (JTBD, CJM, personas, service blueprint).
10. **Socialize:** put the report into the shared base; walk the team through it in person; run a workshop or a meeting on "how to embed it into the work"; keep the protocols and recordings (per the storage rules); come back to the findings within 2–4 weeks, before the team forgets.
11. **Hand over downstream:** hypotheses for quantitative testing ([[M-quant-methods]]), segments and personas ([[M-audience-research]]), inputs for JTBD and CJM ([[M-jtbd]], [[M-cjm]]).

**Analysis health metrics (a mini-dashboard for the product manager):** coverage — 100% of the planned interviews transcribed; tag density — 3–5 quotes per code; "session → transcript" time ≤ 24 h; personal data masked at the cleaning stage. Showing it to the product owner is a signal that the analysis is on schedule.

## How to formulate an insight
A good insight: (a) is about a cause or a mechanism, not about a fact; (b) is specific (segment, situation, barrier); (c) is not obvious; (d) leads to action; (e) has an explicit evidence strength.
Template: *[Segment] in the situation [context] does/avoids [behavior], because [motive/barrier], and expects [outcome]. Implication for the product: [solution hypothesis]. Strength: L1, 8 interviews (one audience); verification needed: [survey / A/B / analytics].*
Example: "Car buyers who take a loan hedge when handing over the money (cash at an ATM), because they do not trust small banks. Implication: a guarantee of a safe settlement scheme will remove the barrier. Strength: L1; estimate the share with a survey".

## Template / checklist
**The report artifact:**
| Section | Content |
|---|---|
| Introduction | goal, tasks, hypotheses, sample description (who, how many, how recruited), method and limitations |
| Main body | categories with quotes and stories; differences between segments; answers to the research questions |
| Conclusions | 3–7 insights with evidence levels; confirmed and refuted hypotheses; unexpected findings |
| Recommendations and next steps | what to change; what to verify quantitatively; which decisions we hold off until the data arrives |
| Appendices | codebook, protocols (de-identified), the guide |

**Checklist of a good analysis:** the goal and hypotheses are moved to the front; the sample and method are described, including the weak spots; no percentages and no "majority" without an explanation; every conclusion is backed by quotes and tied to categories; opposing opinions are present; conclusions are not fitted to expectations; unexpected findings are marked; evidence strength is stated; next steps are defined; the report is available in the base and a socialization meeting is scheduled.

## AI and synthetic respondents in analysis
- **Acceptable with human verification:** transcription, draft grouping of quotes by theme, searching for contradictions, suggesting code wording. The researcher verifies every category and conclusion against the original quotes; "model conclusions" cannot be accepted without links to fragments. Do not upload personal data to external services without the respondents' consent and outside the storage rules.
- **Synthetic respondents** (AI-simulated clients, [[M-synthetic-respondents]]): use *only* for hypothesis generation and guide preparation. Their answers are not data about clients: they are not coded together with real interviews, are not counted in the "n", and do not serve as proof of demand, barriers or preferences. Any fragment of synthetic origin in the materials is labeled ("synthetic data"), and the hypotheses derived from it go through testing on real respondents (L0 until that check). Details: [[M-ai-in-research]].

## Typical mistakes
- Skipping the analysis: "everything is clear anyway" — only the most vivid quotes and memories remain.
- Percentages and statistics out of interviews; a conclusion about a share drawn from a series of 8–10 conversations.
- A "bedsheet" of quotes without structure; a presentation where quotes are read out one by one.
- Confirming your own hypothesis: we take only the fitting fragments and ignore the opposing ones (confirmation seeking).
- Goals and hypotheses forgotten — the conclusions do not answer the research question.
- Interpretation that is too subjective, or fitting stakeholder expectations; fear of delivering an unpleasant result.
- Relying only on vivid statements instead of recurring patterns.
- No separation of segments (professionals and consumers blended together).
- The report is not socialized and not preserved: in two weeks it is forgotten.
- Analysis for analysis' sake: wasted time (balance the level of detail against the task context — time to market).

## Questions that can change the decision
- Which decision does the result influence, and what evidence strength does it need (L1 suffices for a hypothesis, L3 — for an investment)?
- Is the sample homogeneous; how many interviews per segment; has saturation been reached?
- Is there an independent source for triangulation (analytics, support, reviews)?
- Which alternative explanations have not been ruled out?
- What data is needed for quantitative verification, and who will collect it?
- To whom, and in what format, should the results be presented so that they reach the backlog?

## Related maps
[[M-in-depth-interviews]], [[M-audience-research]], [[M-brief-hypotheses]], [[M-quant-methods]], [[M-jtbd]], [[M-cjm]], [[M-problem-design]], [[M-ai-in-research]], [[M-synthetic-respondents]], [[M-source-criticism]]
