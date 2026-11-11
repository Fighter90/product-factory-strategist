---
id: M-marketing-research
lang: en
title: Marketing research: brand tracking, Kano, MaxDiff, TURF
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [research, options, strategy, after-decision]
tags: [marketing-research, bht, brand-tracking, u-a, kano, maxdiff, turf, feature-prioritization, segmentation, awareness]
related: [M-research-types, M-quant-methods, M-loyalty-metrics, M-audience-research, M-usp, M-competitors, M-product-communication, M-product-metrics, M-pmf-scaling, M-market-sizing, M-brief-hypotheses]
---

# Marketing research: brand tracking, Kano, MaxDiff, TURF

## When to apply
You need to look at the market and potential buyers "from a height" (zoom out): how the brand is known and used relative to competitors, how perception is changing, which product attributes matter more, and what to include in the set so that it covers the maximum share of the audience. The map helps you choose between recurring tracking and a one-off ad hoc project, and read their results correctly.

## Core idea
**Marketing research** — a procedure for collecting, analyzing and interpreting information about the market, consumers and the competitive environment. It helps forecast demand, understand needs and stand out against competitors. The industry is more than 100 years old.

**Marketing vs product research.** The distinction is conditional: marketing research is "zoom out" (the market, potential buyers, preferences, opportunities, strategy); product research is "zoom in" (a deep dive into user needs and the business context in order to create or improve a product). The tools are shared; researcher roles are hybridizing.

**Two formats.**
| Format | Purpose | Frequency | Examples |
|---|---|---|---|
| Tracking (recurring) | dynamics and comparison with competitors | month–quarter–half-year | BHT (Brand Health Tracking), CSAT/CES measures, channel and advertising tracking |
| Ad hoc (one-off) | answer a specific question or make a choice | as needed | U&A (Usage & Attitude: category penetration, habits and attitudes), segmentation, Kano, MaxDiff, TURF, concept tests |
A good product has an "always-on" tracker, and ad hoc joins in when something is unclear or a choice has to be made.

**Evidence strength.** Mass-survey data describe the *declared* attitudes and awareness of the chosen sample at the moment of measurement. They prove differences and dynamics given a correct sample and methodology, but not causes, not behavior (purchases), and not future demand. "Importance" ratings from surveys tend toward "everything is important"; to make choices you need forced-choice methods (MaxDiff) and anchoring to behavior (analytics, experiments).

## Brand Health Tracking (BHT)
**What we track.**
- **Brand funnel:** awareness (top-of-mind — the first name that comes to mind; spontaneous — without prompting; prompted) → usage (consideration, trial, regular, most frequently used).
- **Satisfaction:** CSAT, CES, NPS, trust ([[M-loyalty-metrics]]). In tracking, CSAT and CES are often computed as the share of the top-2 out of 5; NPS = % promoters (9–10) − % detractors (0–6).
- **Image:** functional and emotional attributes of the brand relative to competitors.
- **Market:** the situation, the assessment of demand, competitor activity.

**How to build the questionnaire.** The order is fixed and goes from broad to narrow: screening → top-of-mind (open) → spontaneous awareness → prompted awareness → usage → image attributes (agreement scale) → CSAT/NPS. Prompts are placed *after* the spontaneous questions, otherwise the funnel is distorted. The same questionnaire in every wave, otherwise comparison is impossible.

**Sample:** for shares at ±5 pp and 95% ≈ 385 respondents per wave (per each analyzed segment); with an adjustment for stratification/design effect and a 10–15% buffer for discards — around 450–500; quality control (traps, timer, duplicates). Calculation and errors: [[M-quant-methods]].

**How to use the results.**
1. *Dynamics:* compare with the previous wave — did the growth or decline confirm the effect of advertising and product decisions? Read with confidence intervals: a change inside the margin of error is not a signal.
2. *Comparison with competitors:* above or below the market at each step of the funnel? Where does it "leak": high awareness with low usage — a price or trust barrier; low awareness with high usage — a reach problem.
3. *Image gap:* an attribute on which the competitor's score is significantly higher is a candidate for a USP or a zone of weakness ([[M-usp]]).
4. *Market context:* adjust plans; a change of positioning (for example, moving upmarket into premium niche restaurants) is verified by the following waves.
5. *The question "CSAT 60% — is that good or bad?":* it cannot be answered without comparison. Look at the dynamics versus the previous wave, at competitors and segments; then decide what to do about the causes (open questions, interviews).

## Feature prioritization
Questions of the "pick the most important" and "rank these" format produce noise ("everything is important"). Three methods solve the task in different ways.

### The Kano model
**Goal:** how an attribute affects satisfaction. For each attribute — a pair of questions: "How would you feel if X *were there*?" and "How would you feel if X *were not there*?" (options: very pleased — it should be so — indifferent — I can live with it — very displeased). Additionally, you can ask about clarity.
**Answer matrix (standard):** row — the answer to "is there", column — the answer to "is not there".
| Is there \\ Is not there | pleased | must-be | indifferent | I can live with it | displeased |
|---|---|---|---|---|---|
| pleased | doubtful | bonus | bonus | bonus | advantage |
| must-be | reverse | unnecessary | unnecessary | unnecessary | necessary |
| indifferent | reverse | unnecessary | unnecessary | unnecessary | necessary |
| I can live with it | reverse | unnecessary | unnecessary | unnecessary | necessary |
| displeased | reverse | reverse | reverse | reverse | doubtful |
Count the share of answers in each category for each attribute; the category with the largest share wins (with close shares — look at the split and at segments).
**Categories:** advantages/performance (good if present; bad if absent); necessary/hygiene/must-have (expected if present; bad if absent); bonuses/attractive (nice if present; indifference if absent); unnecessary/indifferent. Reverse — a part of people does not want the attribute at all.
**Order of work:** (1) add or fix defects among the necessary; (2) develop the advantages; (3) add bonuses; (4) do not waste time on the unnecessary. Sample guideline: from ≈300 respondents; discuss the results with interviews (the method does not explain "why", is sensitive to wording, requires budget).

### MaxDiff (Maximum Difference Scaling)
The respondent sees several screens of 4–5 attributes each and picks the most and the least important one. The algorithm distributes the attributes across screens so that each one meets the others in different combinations. The result is a ranked list with a "share of preference" (utility). Advantages: it forces prioritization and reduces order effects. Limitations: a list of ≤≈25 non-overlapping statements, 6–10 screens, long lists cause fatigue and drop-out; sample guideline ≥ ≈200 (≥ ≈300 if you split into segments).

### TURF (Total Unduplicated Reach and Frequency)
An analysis of all possible combinations of attributes from the list (often based on MaxDiff or "top-2" importance) with a calculation of the total *unique* reach: which minimal combination attracts the maximum share of the audience. MaxDiff gives a rating, TURF an optimal set: for example, a loyalty program is useful to a larger share of users, but a convenient app adds reach that the first one does not have. The best pair is not necessarily made of the two top positions of the rating, because they may attract the same people.

### A combination for the MVP set
Kano answers "what type of influence" (necessary / advantage / bonus / unnecessary); MaxDiff — "how important relative to the others"; TURF — "which set covers more people". Necessary attributes are a baseline condition — they do not compete with the rest for a place in the rating; the choice of the set is made among advantages and bonuses by importance (MaxDiff) and reach (TURF), and then passes a check on cost and timelines ([[M-usp]]: the Value × Effort matrix). If there are many surveys, build a hybrid questionnaire of up to ≈7 minutes (Kano pairs and MaxDiff over the same 6–8 attributes with identical wording; Kano first, then MaxDiff, then a trap).

## Procedure
1. **Define the decision and the type of question** ([[M-research-types]]): dynamics and standing versus competitors → tracking; a feature choice → Kano / MaxDiff / TURF; category entry → U&A; identifying groups → segmentation ([[M-audience-research]]).
2. **Prepare the attribute list** after the qualitative stage (interviews, [[M-in-depth-interviews]]); remove overlapping statements.
3. **Choose the method and compute the sample** (see the guidelines and [[M-quant-methods]]); prepare quotas by gender, age, region, usage.
4. **Design the questionnaire:** a fixed order, identical wording across waves and methods, attention control, ≤ ~7–10 minutes.
5. **Run the pilot and the field;** clean the data by rules set in advance.
6. **Analysis:** the funnel and dynamics with intervals; gaps versus competitors; Kano categories; the MaxDiff ranking; TURF reach; segment differences with significance tests.
7. **Conclusions and plan:** a summary of the main findings (what changed, where the gaps are, what it means for positioning), a list of actions with owners, hypotheses for the next wave or a qualitative stage.
8. **Fix the baseline values** for the next wave; set alert thresholds for the key indicators.

## Template / checklist

**Research type — the choice:**
| Question | Method | Key output |
|---|---|---|
| Where do we stand versus competitors and is it changing | BHT | the awareness → usage funnel, image gaps, CSAT/NPS in dynamics |
| How people use the category and what they think | U&A | frequencies, habits, barriers |
| Which customer groups exist | segmentation | segment sizes and profiles |
| What is necessary / gives an advantage / is a bonus | Kano | a category per attribute |
| What matters more relative to the rest | MaxDiff | a rating and preference shares |
| Which set covers the most | TURF | a combination and reach in % |

**BHT summary (template):** wave and period; sample (n, quotas); the funnel (awareness/usage) vs the previous wave and competitors; CSAT/CES/NPS with intervals; image attributes (strong and weak); the 3 main conclusions; hypotheses of the causes; an action plan (owner, deadline); what to check with the next study.

**Checklist before starting a BHT:** the question order is fixed; the wording is unchanged between waves; quotas and stratification are set; n is computed per segment; quality control is in place (traps, timer); alert thresholds are defined; it is clear who makes decisions based on the results.

## Typical mistakes
- Reading a single number without dynamics and comparison ("60% — is that good?").
- Changing wording or order between waves; prompts before spontaneous awareness.
- Ignoring confidence intervals: a 2–3 pp difference on a sample of 400 is noise.
- Using an "importance rating" instead of forced choice; taking the MaxDiff TOP-3 directly without TURF (duplicated reach).
- Kano questions in the "would you like X?" style (without the pair) and overlapping statements.
- Interpreting Kano/MaxDiff as future demand or willingness to pay.
- Mixing necessary and bonus attributes in one ranking.
- Relying on marketing tracking for interface decisions: product methods are needed for that ([[M-usability-testing]]).
- No action plan: a brand-health report without owners.

## Questions that can change the decision
- Which decision will be made based on the results: the communication budget, positioning, a feature set, entering a category?
- Are comparison with competitors and dynamics needed (hence a tracker), or a one-off choice?
- Which attributes (≤ 8–25) are already supported by qualitative data?
- How large is the audience, and are there enough respondents for subgroups?
- Is there behavioral data (sales, usage) to verify the declared attitudes?
- Who owns the indicators, and how often do they need to be re-measured?

## Related maps
[[M-research-types]], [[M-quant-methods]], [[M-loyalty-metrics]], [[M-audience-research]], [[M-usp]], [[M-competitors]], [[M-product-communication]], [[M-product-metrics]], [[M-pmf-scaling]], [[M-market-sizing]]
