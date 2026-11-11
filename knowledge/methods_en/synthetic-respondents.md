---
id: M-synthetic-respondents
lang: en
title: Synthetic respondents (AI simulation) — permitted use, persona specification, mandatory labeling
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [intake, research, options, validation]
tags: [synthetic-respondents, ai, personas, hypotheses, labeling, limitations, guide-pilot]
related: [M-ai-in-research, M-brief-hypotheses, M-audience-research, M-in-depth-interviews, M-interview-analysis, M-usability-testing, M-quant-methods, M-ux-backlog, M-source-criticism]
---

# Synthetic respondents: rules of use

## When to apply
When the team has an idea or an interview guide but no live respondents yet, and needs cheap "draft" thinking: generate hypotheses, objections, wordings, traps hidden in questions — and then verify all of it on real people. The card protects against the main mistake: using invented AI respondents as proof of demand or prevalence.

## Core idea
A **synthetic respondent** is a language model given the role of a person ("a cat owner, 35 years old…"), which answers the researcher's questions. Its answer is **generated text, not an observation**: it reflects training data, the wording of the request, and the expectations embedded in the prompt — not the life of a real segment. Strict rules follow from this:

1. Synthetic data is a **source of ideas and a training simulator**, but **not a source of evidence**. It does not know your market and it does not show how often something occurs.
2. Any conclusion drawn from synthetic data is a **hypothesis with "unverified" status** until it is confirmed on real people/data ([[M-source-criticism]]).
3. Everything synthetic is **labeled** everywhere it is visible: in text, in a table, in a quote, in a report.
4. The course (session 10) gives the basic principle: an AI answer is checked against your own data; for the analysis of real interviews the model must cite the uploaded files rather than fantasize.

**Allowed (low risk):**
- generating and expanding a list of hypotheses about barriers, motives, and objections (for subsequent verification);
- piloting an interview/test guide: find unclear, leading, and ambiguous questions; estimate the timing (but a pilot with at least one real human is still mandatory);
- checking the wording of tasks: "how else could this be understood?";
- devil's advocate: objections to the value proposition, client fears, alternatives ([[M-jtbd]]);
- interview preparation: warming up the interviewer, practicing probing questions;
- draft personas/scenarios for a workshop — as inspiration, with a label.

**Not allowed:**
- "we surveyed 100 AI respondents, 72% are ready to buy" — shares, percentages, segment sizes, NPS/CSAT, willingness to pay, probability of churn;
- substituting a usability test ("the model said the button is noticeable");
- synthetic quotes in a report presented as the client's voice;
- making investment or launch decisions on the basis of synthetic data;
- validating your own hypothesis: the model tends to agree and to adapt to the implied answer.

## Procedure
1. **Define the purpose** of using it: hypotheses / guide pilot / objections. If the purpose is "get the market's opinion" — stop and return to real data ([[M-research-types]]).
2. **Collect the input facts** about the segment from real sources: interviews, support, analytics, reviews. Every fact gets a source. Anything known only by assumption is labeled "assumption".
3. **Write the persona specification** (the template below). Do not invent numbers or quotes; do not build the desired answer into the role.
4. **Prompt frame:** the model is reminded that it is a simulation; it answers briefly, in the first person, and may say "I don't know / I haven't used it"; it is not obliged to agree; it relies only on the given specification.
5. **Run several independent runs** (different personas within the segment, different wordings, repeats). If the answers are identical and too rational or too smooth, that is a sign of an artifact, not of segment unanimity.
6. **Ask for divergences:** "what would change your decision", "what about this doesn't suit you", "what are your alternatives", "what are you unsure about".
7. **Record the result in the registry** with the label `[SYNTHETIC, unverified]`, the model, the date, and the prompt version.
8. **Turn it into testable hypotheses** (the format below) and choose a verification method on real people ([[M-in-depth-interviews]], [[M-usability-testing]], a survey — [[M-quant-methods]]).
9. **Calibrate** (if real interviews exist): check whether the simulation reproduces known real answers; if not — lower your trust and do not use it for that segment.
10. **Update the statuses** after verification: confirmed / refuted / needs refinement; the synthetic originals stay in the archive as "a source of ideas", not "a source of facts".

## Template / checklist

**Persona specification:**
| Field | Content | Source |
|---|---|---|
| Label | `SYNTHETIC RESPONDENT — not a real person` | — |
| Segment | Who, where, experience with the product/category | interviews/analytics/assumption |
| Situation (trigger) | When and why they turn to it | interviews/assumption |
| Job (JTBD) | Functional, emotional, social | interviews/assumption |
| Alternatives | How they solve it now | interviews/assumption |
| Constraints | Time, money, skills, device | assumption/data |
| Known facts | Only confirmed ones, with a reference | source |
| Unknown | What the persona does not know / may not remember | — |
| Answer style | Short, conversational, with doubts | — |

**A registry row for a synthetic conclusion:**
`ID | The model's statement | [SYNTHETIC] | Model/date/prompt version | Persona | Why it might be false | Hypothesis (testable wording) | Verification method | Threshold/failure criterion | Status`

**The wording of a testable hypothesis:** `If <segment> in situation <trigger>, then <observable behavior/answer> at a share ≥ X% / among at least N of M participants;
verify with <method>; refuted if <criterion>.` The numbers X and N are set by the researcher by decision, not by the model.

**Labeling a conclusion (mandatory):** at the top of the block — "What follows is the result of a simulation, not respondent data"; every quote gets a `[SYN]` tag; in summaries, percentages and the words "clients believe" are forbidden. In the final document the synthetic material is separated from the evidence by a dedicated section, "Hypotheses to verify".

**Admissibility checklist:** the purpose is hypotheses/pilot/objections; the input comes from real facts; there is labeling; nothing is called "data" or "market research"; there are no numbers about prevalence; a plan for verification on real people is in place; the decision does not depend on synthetic data alone.

## Typical mistakes
| Mistake | Why it is bad | How to avoid it |
|---|---|---|
| Presenting a share of "AI respondents" as a market share | No sample, no representativeness | Ban percentages; qualitative hypotheses only |
| Asking "would you like this?" | Adjustment to the expectation, a polite answer | Ask for objections, alternatives, refusal conditions |
| One persona, one run | Smoothness ≠ the segment's opinion | Several runs and divergences |
| A persona invented "from the head" without facts | Amplification of stereotypes | Rely on real interviews and mark assumptions |
| The desired answer leaking into the prompt | Confirmation of your own hypothesis | Neutral wording, red team |
| Mixing synthetic and real quotes in one table | Loss of provenance | Separate columns/labels, source status |
| Accepting synthetic output instead of a pilot | Real misunderstandings are missed | At least one real pilot of the guide |
| Using it to evaluate an interface | The model does not see and does not use it like a human | Heuristics + a real test ([[M-ux-heuristics]]) |
| Using it as "the voice" on sensitive topics (health, finances) | Risk of harm and false conclusions | Real respondents only |

## Questions that can change the decision
- Is there access to real respondents within the required timeframe? If yes, synthetic data is needed only to pilot the guide.
- What will be done with the result: does it go into hypotheses, or does it affect money/launch? In the second case, synthetic data is inadmissible as a basis.
- Are there real data available to calibrate the personas?
- How well does the model know the segment (a mass consumer or a narrow B2B/professional role)? For narrow roles, trust is minimal.
- Is confirmation by another method needed (analytics, an experiment)? Then restrict the synthetic data to generating variants for A/B.

## Related maps
[[M-ai-in-research]], [[M-brief-hypotheses]], [[M-audience-research]], [[M-in-depth-interviews]], [[M-interview-analysis]], [[M-usability-testing]], [[M-quant-methods]], [[M-ux-backlog]], [[M-source-criticism]], [[M-jtbd]], [[M-research-types]], [[M-ux-heuristics]]
