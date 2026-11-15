---
id: M-interview-analysis
lang: en
title: Analysis and presentation of in-depth interview results
course: ux
sources: ["EN mirror of the RU methodology card M-interview-analysis (knowledge/methods/interview-analysis.md); original sources are listed in the RU card"]
stages: [research, options, validation]
tags: [interview-analysis, coding, categories, insights, evidence-strength, report, socialization, synthetic-respondents]
related: [M-in-depth-interviews, M-audience-research, M-brief-hypotheses, M-quant-methods, M-jtbd, M-cjm, M-problem-design, M-customers, M-ai-in-research, M-synthetic-respondents, M-source-criticism]
---

# Analysis and presentation of in-depth interview results

## When to apply
A series of interviews has been conducted (or there is other qualitative data: open-ended answers, diaries, support tickets) and you need to turn them into an explanatory model, insights and recommendations without losing information and without promising the team what qualitative data cannot deliver.

## Essence
**Analysis is not a formality.** A set of interviews without analysis is a set of stories: the conclusions can easily be dismissed. Analysis creates an explanatory model from which the product moves forward, and protects against the loss of insights and against fitting to expectations.

**The source materials after interviews:** the recording, the transcript, the notes (protocol). We work with all three; recordings are turned on having warned the respondent in advance.

**The stages of analysis.**
1. *Immersion:* reread the notes and transcripts, relisten to the interviews, go through each respondent and mark what matters; build the full picture of the series.
2. *Coding:* mark up the fragments with short labels (codes) so that similar thoughts of different respondents can be matched. A code reflects meaning ("distrust of small banks"), not retelling.
3. *Category extraction:* combine the codes into more general themes/patterns that explain the behaviour or values of a group (e.g., codes about the sellers' attitude to a credit buyer → the category "varying seller attitudes toward a buyer who takes credit"; codes about handing over cash at an ATM → "fears in the deal process"). Keep the contradictory categories too (they praise the simplicity / they complain about the complexity).
4. *Interpretation and conclusions:* link the categories to each other and explain why users behave this way; formulate the insights and research conclusions.

**An example of a code and a category from the course (car deals on credit):**
| Quote (meaning) | Code | Category |
|---|---|---|
| "credit buyers can be asked to pay more" | the sellers' negative attitude toward selling on credit | varying seller attitudes toward a buyer with credit |
| "I don't care where the money comes from, the transfer is what matters" | a neutral attitude | varying seller attitudes… |
| "the rate depends on which bank you use more often" | incorrect beliefs about how the rate is calculated | myths and low financial literacy |
| "the money was deposited at the ATM, then the sale contract was signed" | handing over cash at the ATM | fears in the deal process |
| "I don't want small banks — what if they close" | distrust of small banks | fears in the deal process |

## Strength of evidence: what N interviews give
Principles: (1) qualitative data describe *variety and mechanisms*, not frequencies; (2) the homogeneity of the sample matters more than its size; (3) a conclusion is stronger if confirmed by an independent source (triangulation).
| Volume and source | What can be claimed | What cannot |
|---|---|---|
| 1–4 interviews | individual stories, examples of barriers, hypotheses to test | "a pattern", "typical" |
| 5–9 interviews of one segment | the first recurring themes; a list of behaviour variants; the customers' language | shares, ranking by frequency, segment comparison |
| ~10–15 interviews of a homogeneous audience (the course benchmark) | stable themes within the group; when new interviews stop bringing new themes (saturation) — a sign of sufficiency for a *qualitative* goal | prevalence in the population |
| Interviews + behavioural data / desk research / support | a hypothesis with confirmation from an independent channel (triangulation) | the effect size |
| Interviews → a survey / A/B with a threshold set in advance | prevalence, segment size, the significance of differences | — |
A gradation of insight convenient for a report: **L0** — an individual observation; **L1** — recurs across a series within a segment; **L2** — confirmed by an independent source; **L3** — confirmed quantitatively. Decisions with a high cost of error rest on L2–L3.

**Wording.** Never present interview results in percentages ("80% said…") — the team gets a false sense of statistics. We write: "almost everyone…", "some…", "two distinct approaches: … and …", "not encountered in this series…". If a count is given, then only as "x of n" and only to show breadth, with a note that this is not prevalence.

## Procedure
1. **Return to the goals, hypotheses and the plan for using the results** — otherwise you will get lost in the volume. Write out the research questions and hypotheses, what they were meant to confirm and refute.
2. **Prepare the materials (a transcription pipeline within 24 hours):** export the recordings → auto-transcription → cleanup (filler words, masking of personal data) → time-code synchronization (quote ↔ time) → upload to the team's shared storage. Plus notes and recordings; respondent labels (no personal data). The double recording (local + cloud) is checked right after the session: a lost file = a lost insight.
3. **Immerse:** go through all the interviews, mark the vivid and contentious spots, make "hot" summaries for each (three questions: what surprised; what matched or diverged from the hypothesis; what to refine in the guide tomorrow).
4. **Code:** for each interview, extract the meaningful fragments and assign codes (if an interview is long, first quotes, then codes). Same meaning — same code. Keep the codebook (a list of codes with a definition, an example quote and the conditions of application) in a table: quote — code — respondent — time. Code the contentious/"strange" answers too — sometimes that is an unexpected segment. Do not inflate the codebook at the start: 6–8 top categories, detail as you go.
5. **Consolidate into categories:** group the codes; name the categories; single out the competing ones; keep 2–3 strong quotes per category as evidence (the density benchmark: 3–5 quotes per code — fewer means a "lonely code", more means oversaturation). For work with the team — a board (Miro, FigJam) with cards.
5a. **Check the reliability of coding:** code part of the material in pairs (one reads aloud, the other independently names the codes) and compare; if the inter-coder agreement is below ~0.7 on Cohen's kappa — rewrite the code definitions and recode the contentious ones. Solo coding without a cross-check is a frequent source of subjectivity.
6. **Interpret:** link the categories ("the fear of X explains behaviour Y at stage Z"); map onto the segments and journey stages; test against the original hypotheses (confirmed / refuted / no data); separately write out the unplanned findings.
7. **Estimate the strength of each conclusion** (L0–L3), state which data are needed to strengthen it (a survey, A/B, a behavioural export).
8. **Formulate the insights and recommendations** (the template below): "observation → interpretation → implication for the product → how to verify".
9. **Assemble the artifact:** the introduction (goal, tasks, hypotheses, sample, method); the main part (behaviour, stories, quotes, answers to the questions); the conclusions (the main points, briefly). The format — a board, a presentation or a framework (JTBD, CJM, personas, service blueprint).
10. **Socialize:** put the report in the shared base; tell the team in person; run a workshop or a meeting on "how to embed it in the work"; keep the protocols and recordings (by the storage rules); return to the conclusions within 2–4 weeks, before the team forgets.
11. **Hand off:** hypotheses for quantitative testing ([[M-quant-methods]]), segments and personas ([[M-audience-research]]), inputs for JTBD and CJM ([[M-jtbd]], [[M-cjm]]).

**Analysis health metrics (a mini-dashboard for a PM):** coverage — 100% of the planned interviews transcribed; tag density — 3–5 quotes per code; the time "session → transcript" ≤ 24 h; personal data masked at the cleanup stage. Shown to the product owner — a signal that the analysis is on schedule.

## How to formulate an insight
A good insight: (a) about a cause or a mechanism, not a fact; (b) specific (segment, situation, barrier); (c) not obvious; (d) leads to action; (e) has an explicit strength of evidence.
The template: *[Segment] in the situation of [context] does/avoids [behaviour], because [motive/barrier], and expects [outcome]. Implication for the product: [solution hypothesis]. Strength: L1, 8 interviews (one audience); needs testing: [survey / A/B / analytics].*
Example: "Buyers who take a car on credit hedge when handing over the money (cash at an ATM), because they distrust small banks. Implication: a guarantee of a safe settlement scheme will remove the barrier. Strength: L1; estimate the share with a survey".

## Template / checklist
**The report artifact:**
| Section | Content |
|---|---|
| Introduction | the goal, tasks, hypotheses, a description of the sample (who, how many, how recruited), the method and limitations |
| Main part | categories with quotes and stories; the differences between segments; the answers to the research questions |
| Conclusions | 3–7 insights with a level of evidence; the confirmed and refuted hypotheses; unexpected findings |
| Recommendations and next steps | what to change; what to verify quantitatively; which decisions we postpone until the data |
| Appendices | the codebook, the protocols (de-identified), the guide |

**The checklist of good analysis:** the goal and hypotheses stated up front; the sample and method described, including the weak sides; no percentages and "majority" without explanation; every conclusion backed by quotes and tied to categories; contradictory opinions present; the conclusions not fitted to expectations; the unexpected findings marked; the strength of evidence stated; the next steps defined; the report available in the base, a socialization meeting scheduled.

## AI and synthetic respondents in analysis
- **Permissible with human verification:** transcription, the draft grouping of quotes by theme, finding contradictions, suggesting code wordings. The researcher checks every category and conclusion against the original quotes; "model conclusions" must not be accepted without links to fragments. Do not upload personal data to external services without the respondents' consent and storage rules.
- **Synthetic respondents** (an AI imitation of customers, [[M-synthetic-respondents]]): use *only* for generating hypotheses and preparing the guide. Their answers are not customer data: they are not coded together with real interviews, not included in the "n" count, and do not serve as evidence of demand, barriers or preferences. Any fragment of synthetic origin in the materials is labelled ("synthetic data"), and the hypotheses from it go through validation on real respondents (L0 until such validation). Details: [[M-ai-in-research]].

## Typical mistakes
- Skipping the analysis: "it's all clear anyway" — only the most vivid quotes and memories remain.
- Percentages and statistics out of interviews; a conclusion about a share from a series of 8–10 conversations.
- A "wall" of quotes without structure; a presentation where quotes are read out one after another.
- Confirming one's own hypothesis: taking only the fitting fragments, ignoring the contradictory ones (confirmation seeking).
- The goal and hypotheses forgotten — the conclusions do not answer the research question.
- A too subjective interpretation or fitting to stakeholder expectations; the fear of delivering an unpleasant result.
- Relying only on vivid statements, not on recurring patterns.
- No separation of segments (professionals and private sellers mixed together).
- The report not socialized and not stored: two weeks later it is forgotten.
- Analysis for analysis's sake: wasted time (the balance of detail and the task's context — time to market).

## Questions that can change the decision
- Which decision does the result influence and what strength of evidence does it need (L1 suffices for a hypothesis, L3 — for an investment)?
- Is the sample homogeneous; how many interviews per segment; has saturation been reached?
- Is there an independent source for triangulation (analytics, support, reviews)?
- Which alternative explanations are not excluded?
- Which data are needed for quantitative testing and who will collect them?
- To whom and in what format should the results be presented so that they make it into the backlog?

## Related maps
[[M-in-depth-interviews]], [[M-audience-research]], [[M-brief-hypotheses]], [[M-quant-methods]], [[M-jtbd]], [[M-cjm]], [[M-problem-design]], [[M-ai-in-research]], [[M-synthetic-respondents]], [[M-source-criticism]]
