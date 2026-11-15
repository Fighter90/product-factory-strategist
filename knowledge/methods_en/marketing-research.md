---
id: M-marketing-research
lang: en
title: Marketing research: brand tracking, Kano, MaxDiff, TURF
course: ux
sources: ["EN mirror of the RU methodology card M-marketing-research (knowledge/methods/marketing-research.md); original sources are listed in the RU card"]
stages: [research, options, strategy, after-decision]
tags: [marketing-research, bht, brand-tracking, u-a, kano, maxdiff, turf, feature-prioritization, segmentation, awareness]
related: [M-research-types, M-quant-methods, M-loyalty-metrics, M-audience-research, M-usp, M-competitors, M-product-communication, M-product-metrics, M-pmf-scaling, M-market-sizing, M-brief-hypotheses]
---

# Marketing research: brand tracking, Kano, MaxDiff, TURF

## When to apply
You need to look at the market and potential buyers "from above" (zoom out): how the brand is known and used relative to competitors, how perception changes, which product attributes matter more and what to include in the set to cover the maximum audience. The map helps to choose between regular tracking and a one-off ad hoc project and to read their results correctly.

## Essence
**Marketing research** — a procedure for collecting, analysing and interpreting information about the market, consumers and the competitive environment. It helps forecast demand, understand needs and stand out against competitors. The industry is more than 100 years old.

**Marketing vs product research.** The distinction is conventional: marketing — "zoom out" (the market, potential buyers, preferences, opportunities, strategy); product — "zoom in" (a deep immersion in user needs and the business context to create or improve a product). The tools are shared; the researchers' roles hybridize.

**Two formats.**
| Format | Purpose | Frequency | Examples |
|---|---|---|---|
| Trackings (regular) | dynamics and comparison with competitors | month–quarter–half-year | BHT (Brand Health Tracking), CSAT/CES measurements, channel and advertising tracking |
| Ad hoc (one-off) | answer a specific question or make a choice | as needed | U&A (Usage & Attitude, category penetration, habits and attitudes), segmentation, Kano, MaxDiff, TURF, concept tests |
A good product has an "always-on" tracking, while ad hoc kicks in when something is unclear or a choice is needed.

**Strength of evidence.** Mass survey data describe *stated* attitudes and the awareness of the chosen sample at the moment of measurement. They prove differences and dynamics with a correct sample and methodology, but not causes, not behaviour (purchases) and not future demand. "Importance" ratings from surveys tend toward "everything is important"; for choices you need forced-choice methods (MaxDiff) and anchoring to behaviour (analytics, experiment).

## Brand Health Tracking (BHT)
**What we track.**
- **The brand funnel:** awareness (top-of-mind — the first that came to mind; spontaneous — without prompting; prompted) → usage (consideration, trial, regular, most frequent).
- **Satisfaction:** CSAT, CES, NPS, trust ([[M-loyalty-metrics]]). In tracking, CSAT and CES are often computed as the share of the top-2 out of 5; NPS = % promoters (9–10) − % detractors (0–6).
- **Image:** the functional and emotional attributes of the brand relative to competitors.
- **The market:** the situation, the demand assessment, competitor activity.

**How to build the questionnaire.** The order is fixed and goes from broad to specific: screening → top-of-mind (open) → spontaneous awareness → prompted awareness → usage → image attributes (an agreement scale) → CSAT/NPS. Prompts come *after* the spontaneous questions, otherwise the funnel is distorted. The same questionnaire in every wave, otherwise comparison is impossible.

**The sample:** for shares at ±5 p.p. and 95% ≈ 385 respondents per wave (per each analysed segment); with an adjustment for stratification/the design effect and a 10–15% buffer for discards — about 450–500; quality control (traps, a timer, repeats). The calculation and errors: [[M-quant-methods]].

**How to use the results.**
1. *Dynamics:* compare with the previous wave — did it confirm the effect of advertising and product decisions, up or down. Read with confidence intervals: a change within the margin of error is not a signal.
2. *Comparison with competitors:* above or below the market at every funnel step? Where does it "leak": high awareness with low usage — a price or trust barrier; low awareness with high usage — a reach problem.
3. *The image gap:* an attribute where a competitor scores significantly higher is a candidate for a USP or a zone of weakness ([[M-usp]]).
4. *The market context:* adjust the plans; a repositioning (e.g., a move to premium/niche restaurants) is verified by the subsequent waves.
5. *The question "CSAT 60% — good or bad?":* impossible without comparison. Look at the dynamics vs the previous wave, the competitors and the segments; then decide what to do about the causes (open questions, interviews).

## Prioritizing attributes
Questions of the "pick the most important" and "rank these" format produce noise ("everything is important"). Three methods solve the task in different ways.

### The Kano model
**Purpose:** how an attribute affects satisfaction. For each attribute — a pair of questions: "How would you feel if X *were present*?" and "How would you feel if X *were absent*?" (the options: very pleased — it should be that way — indifferent — I can live with it — very displeased). You can additionally ask about clarity.
**The answer matrix (standard):** the row is the answer to "present", the column is the answer to "absent".
| Present \\ Absent | pleased | should be | indifferent | can live with | displeased |
|---|---|---|---|---|---|
| pleased | quest. | bonus | bonus | bonus | advantage |
| should be | reverse | unnecessary | unnecessary | unnecessary | necessary |
| indifferent | reverse | unnecessary | unnecessary | unnecessary | necessary |
| can live with | reverse | unnecessary | unnecessary | unnecessary | necessary |
| displeased | reverse | reverse | reverse | reverse | quest. |
Count the share of answers in each category for each attribute; the category with the largest share (with close shares — look at the gap and the segments).
**The categories:** performance (good if present; bad if absent); necessary/hygiene/must-have (expected if present; bad if absent); attractive/bonus (pleasant if present; indifference if absent); unnecessary/indifferent. Reverse — some people do not want the attribute at all.
**The order of work:** (1) add or fix defects in the necessary; (2) develop the performance attributes; (3) add bonuses; (4) do not spend time on the unnecessary. Sample benchmark: from ≈300 respondents; discuss the results with interviews (the method does not explain "why", is sensitive to wording, requires a budget).

### MaxDiff (Maximum Difference Scaling)
The respondent sees several screens of 4–5 attributes each and picks the most and the least important. The algorithm distributes the attributes across the screens so that each meets the others in different combinations. The result is a ranked list with a "share of preference" (utility). Advantages: it forces prioritization, reduces order effects. Limitations: a list of ≤≈25 non-overlapping wordings, 6–10 screens, long lists cause fatigue and drop-out; the sample benchmark is ≥ ≈200 (≥ ≈300 if splitting into segments).

### TURF (Total Unduplicated Reach and Frequency)
An analysis of all possible combinations of attributes from the list (often based on MaxDiff or "top-2" importance) computing the total *unique* reach: which minimal combination attracts the maximum share of the audience. MaxDiff gives a rating, TURF — an optimal set: e.g., a loyalty program is useful to a larger share of users, but a convenient app adds reach the first one lacks. The best pair is not necessarily made of the two highest-rated items, because they may attract the same people.

### A combination for the MVP set
Kano answers "what type of influence" (necessary / performance / bonus / unnecessary); MaxDiff — "how important relative to the others"; TURF — "which set covers more people". The necessary attributes are the baseline condition, they do not compete with the rest for the rating; the choice of the set is made among the performance and bonus attributes by importance (MaxDiff) and reach (TURF), then checked against cost and time ([[M-usp]]: the Value × Effort matrix). If there are many surveys, build a hybrid questionnaire of up to ≈7 minutes (Kano pairs and MaxDiff on the same 6–8 attributes with identical wordings; Kano first, then MaxDiff, then a trap).

## Procedure
1. **Define the decision and the type of question** ([[M-research-types]]): dynamics and standing relative to competitors → tracking; a feature choice → Kano / MaxDiff / TURF; entry into a category → U&A; isolating groups → segmentation ([[M-audience-research]]).
2. **Prepare the attribute list** after a qualitative stage (interviews, [[M-in-depth-interviews]]); remove the overlapping wordings.
3. **Choose the method and calculate the sample** (see the benchmarks and [[M-quant-methods]]); prepare the quotas by gender, age, region, usage.
4. **Design the questionnaire:** a fixed order, identical wordings across waves and methods, attention checks, time ≤ ~7–10 minutes.
5. **Run the pilot and the field;** clean the data by the rules set in advance.
6. **Analysis:** the funnel and dynamics with intervals; the gaps vs competitors; the Kano categories; the MaxDiff rating; the TURF reach; the differences by segment with significance tests.
7. **Conclusions and the plan:** a summary of the main conclusions (what changed, where the gaps are, what it means for positioning), a list of actions with owners, hypotheses for the next wave or a qualitative stage.
8. **Fix the baseline values** for the next wave; set the alert thresholds for the key indicators.

## Template / checklist

**Research type — the choice:**
| Question | Method | Key output |
|---|---|---|
| How do we stand relative to competitors and is it changing | BHT | the awareness → usage funnel, image gaps, CSAT/NPS in dynamics |
| How do people use the category and what do they think | U&A | frequencies, habits, barriers |
| Which customer groups exist | segmentation | the sizes and profiles of segments |
| What is necessary / gives an advantage / is a bonus | Kano | a category per attribute |
| What matters more relative to the rest | MaxDiff | the rating and shares of preference |
| Which set covers the most | TURF | a combination and reach in % |

**The BHT summary (template):** the wave and period; the sample (n, quotas); the funnel (awareness/usage) vs the previous wave and competitors; CSAT/CES/NPS with intervals; the image attributes (strong and weak); the 3 main conclusions; the hypotheses of causes; the action plan (owner, deadline); what to check with the next study.

**The pre-launch BHT checklist:** the question order is fixed; the wordings are unchanged across waves; the quotas and stratification are set; n is calculated per segment; quality control is in place (traps, a timer); the alert thresholds are defined; it is clear who makes decisions based on the results.

## Typical mistakes
- Reading a single number without dynamics and comparison ("is 60% good?").
- Changing wordings or the order between waves; prompts before spontaneous awareness.
- Ignoring confidence intervals: a 2–3 p.p. difference on a sample of 400 is noise.
- Using an "importance rating" instead of a forced choice; taking MaxDiff's TOP-3 straight into a set without TURF (duplicated reach).
- Kano questions in the "would you like X?" style (without the pair) and overlapping wordings.
- Interpreting Kano/MaxDiff as future demand or willingness to pay.
- Mixing the necessary and bonus attributes in one rating.
- Relying on marketing tracking for interface decisions: product methods are needed for that ([[M-usability-testing]]).
- No action plan: a brand health report without owners.

## Questions that can change the decision
- Which decision will be made on the results: the communication budget, positioning, the feature set, entry into a category?
- Is comparison with competitors and dynamics needed (hence tracking), or a one-off choice?
- Which attributes (≤ 8–25) are already supported by qualitative data?
- How big is the audience and are there enough respondents for the subgroups?
- Is there behavioural data (sales, usage) to verify the stated?
- Who owns the indicators and how often should they be re-measured?

## Related maps
[[M-research-types]], [[M-quant-methods]], [[M-loyalty-metrics]], [[M-audience-research]], [[M-usp]], [[M-competitors]], [[M-product-communication]], [[M-product-metrics]], [[M-pmf-scaling]], [[M-market-sizing]]
