---
id: M-synthetic-respondents
lang: en
title: Synthetic respondents (AI simulation) — permitted use, persona specification, mandatory labeling
course: ux
sources: ["EN mirror of the RU methodology card M-synthetic-respondents (knowledge/methods/synthetic-respondents.md); original sources are listed in the RU card"]
stages: [intake, research, options, validation]
tags: [synthetic-respondents, ai, personas, hypotheses, labeling, limitations, interview-guide-pilot]
related: [M-ai-in-research, M-brief-hypotheses, M-audience-research, M-in-depth-interviews, M-interview-analysis, M-usability-testing, M-quant-methods, M-ux-backlog, M-source-criticism]
---

# Synthetic respondents: rules of use

## When to apply
When the team has an idea or a discussion guide but no live respondents yet, and cheap "draft" thinking is needed: generate hypotheses, objections, phrasings, traps in questions — and then verify everything on real people. This card protects against the main mistake: using invented AI respondents as proof of demand or prevalence.

## Essence
A **synthetic respondent** is a language model given the role of a person ("a cat owner, 35 years old…") that answers the researcher's questions. Its answer is **generated text, not an observation**: it reflects training data, the wording of the request and the expectations embedded in the prompt, but not the life of a real segment. This implies hard rules:

1. Synthetic output is a **source of ideas and a training ground**, but **not a source of evidence**. It does not know your market and does not show how often something occurs.
2. Any conclusion from synthetic output is a **hypothesis with an "unverified" status** until confirmed on real people/data ([[M-source-criticism]]).
3. Everything synthetic is **labeled** everywhere it is visible: in text, a table, a quote, a report.
4. The course (session 10) gives the basic principle: an AI answer is checked against your own data; for analyzing real interviews the model must cite the uploaded files, not fantasize.

**Permitted (low risk):**
- generating and extending a list of hypotheses about barriers, motives, objections (for subsequent verification);
- piloting an interview/usability guide: find unclear, leading, ambiguous questions; estimate timing (but a pilot with at least one real person is mandatory);
- checking task phrasings: "how else could this be understood?";
- "devil's advocate": objections to the value proposition, fears, customer alternatives ([[M-jtbd]]);
- interview preparation: warming up the interviewer, practicing probing questions;
- draft personas/scenarios for a workshop — as inspiration, with a note.

**Not permitted:**
- "we surveyed 100 AI respondents, 72% are ready to buy" — shares, percentages, segment sizes, NPS/CSAT, willingness to pay, probability of churn;
- substituting a usability test ("the model said the button is noticeable");
- synthetic quotes in a report as the voice of the customer;
- making an investment or launch decision based on synthetic output;
- validating your own hypothesis: the model tends to agree and adapt to the implied answer.

## Procedure
1. **Define the purpose** of use: hypotheses / guide pilot / objections. If the purpose is "get the market's opinion" — stop and return to real data ([[M-research-types]]).
2. **Assemble input facts** about the segment from real sources: interviews, support, analytics, reviews. Each fact — with a source. What is known only by assumption — mark as "assumption".
3. **Write the persona specification** (template below). Do not invent numbers and quotes; do not put the desired answer into the role.
4. **Prompt frame:** the model is reminded that it is a simulation; it answers briefly, in the first person, allows "I don't know / I haven't used it"; it is not obliged to agree; it relies only on the given specification.
5. **Run several independent passes** (different personas within the segment, different wordings, repetition). If the answers are identical and too rational/smooth — that is a signal of an artifact, not segment unanimity.
6. **Ask for discrepancies:** "what would change your decision", "what doesn't suit you about this", "what alternatives do you have", "what are you unsure about".
7. **Record the result in the register** with the tag `[SYNTHETIC, unverified]`, the model, the date, the prompt version.
8. **Turn it into testable hypotheses** (format below) and choose a verification method on real people ([[M-in-depth-interviews]], [[M-usability-testing]], a survey — [[M-quant-methods]]).
9. **Calibrate** (if real interviews exist): check whether the simulation reproduces known real answers; if not — lower trust and do not use it for this segment.
10. **Update statuses** after verification: confirmed / refuted / needs clarification; the synthetic originals stay in the archive as a "source of ideas", not a "source of facts".

## Template / checklist

**Persona specification:**
| Field | Content | Source |
|---|---|---|
| Label | `SYNTHETIC RESPONDENT — not a real person` | — |
| Segment | Who, where, experience with the product/category | interviews/analytics/assumption |
| Situation (trigger) | When and why they turn to the product | interviews/assumption |
| Job (JTBD) | Functional, emotional, social | interviews/assumption |
| Alternatives | How they solve it now | interviews/assumption |
| Constraints | Time, money, skills, device | assumption/data |
| Known facts | Only confirmed ones, with a reference | source |
| Unknown | What the persona does not know/may not remember | — |
| Answer style | Short, conversational, with doubts | — |

**Register row for a synthetic conclusion:**
`ID | Model statement | [SYNTHETIC] | Model/date/prompt version | Persona | Why it might be false | Hypothesis (testable formulation) | Verification method | Threshold/rejection criterion | Status`

**Formulating a testable hypothesis:** `If <segment> in a situation <trigger>, then <observable behavior/answer> with a share ≥ X% / at least N of M participants; we test with <method>; refuted if <criterion>.` The numbers X and N are set by the researcher by decision, not by the model.

**Labeling the output (mandatory):** at the top of the block — "Below is the result of a simulation, not respondent data"; next to each quote `[SYN]`; in summaries, percentages and the phrase "customers believe" are forbidden. In the final document, synthetic output is separated from evidence in a dedicated section "Hypotheses for verification".

**Admissibility checklist:** the purpose — hypotheses/pilot/objections; input from real facts; labeling; nothing is called "data" or "market research"; no numbers about prevalence; a plan for verification on people is set; the decision does not depend only on synthetic output.

## Typical mistakes
| Mistake | Why it is bad | How to avoid |
|---|---|---|
| Presenting a share of "AI respondents" as a market share | No sample, no representativeness | Forbid percentages; only qualitative hypotheses |
| Asking "would you like it?" | Adapting to the expectation, a polite answer | Ask for objections, alternatives, conditions of refusal |
| One persona, one pass | Smoothness ≠ the segment's opinion | Several passes and discrepancies |
| A persona invented "from the head" without facts | Reinforcing stereotypes | Rely on real interviews and mark assumptions |
| Leaking the desired answer into the prompt | Confirming your own hypothesis | Neutral phrasings, red teaming |
| Mixing synthetic and real quotes in one table | Loss of provenance | Separate columns/labels, source status |
| Accepting synthetic output instead of a pilot | Real misunderstandings are missed | At least one real pilot of the guide |
| Using it to evaluate an interface | The model does not see and does not use it like a human | Heuristics + a real test ([[M-ux-heuristics]]) |
| Using it for sensitive topics (health, finance) as a "voice" | Risk of harm and false conclusions | Only real respondents |

## Questions that can change the decision
- Is there access to real respondents within the required timeframe? If yes, synthetic output is needed only for the guide pilot.
- What will be done with the result: does it go into hypotheses or will it influence money/launch? In the second case, synthetic output is inadmissible as a basis.
- Are there real data for calibrating the personas?
- How well does the model know the segment (a mass consumer or a narrow B2B/professional role)? For narrow roles, trust is minimal.
- Is confirmation by another method needed (analytics, an experiment)? Then restrict synthetic output to generating variants for A/B.

## Related cards
[[M-ai-in-research]], [[M-brief-hypotheses]], [[M-audience-research]], [[M-in-depth-interviews]], [[M-interview-analysis]], [[M-usability-testing]], [[M-quant-methods]], [[M-ux-backlog]], [[M-source-criticism]], [[M-jtbd]], [[M-research-types]], [[M-ux-heuristics]]
