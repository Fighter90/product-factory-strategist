---
id: M-loyalty-metrics
lang: en
title: Loyalty research and customer metrics (NPS, CSAT, CES, SUS, UMUX, SUPR-Q)
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [validation, after-decision]
tags: [nps, csat, ces, sus, umux, supr-q, loyalty, satisfaction, customer-experience, surveys]
related: [M-product-metrics, M-success-metrics, M-quant-methods, M-marketing-research, M-research-types, M-usability-testing, M-cjm, M-ux-heuristics, M-brief-hypotheses, M-pmf-scaling]
---

# Loyalty research and customer metrics (NPS, CSAT, CES, SUS, UMUX, SUPR-Q)

## When to apply
You need to measure how customers perceive the product: whether they are satisfied with a specific step, how easy it is to complete a task, whether they are willing to recommend, how usable the interface is. The map picks the metric that fits the question and shows formulas, collection methods, benchmarks and interpretation traps.

## Core idea
**Why experience metrics matter.** They are an early signal for money: investment in customer experience raises revenue over time, customers come back more willingly and are ready to pay for a good experience. Metric value ⇔ success criterion ⇔ product management. Experience metrics belong to the *attitudinal* layer (what people feel and rate) and complement the *behavioral* ones (DAU/MAU, conversion, retention, load time): behavior says *what* is happening, the rating says *why* and how much it hurts.

**Metric groups across the lifecycle:** Acquisition, Activation, Engagement, Retention, Loyalty and satisfaction, plus additional (niche) ones. This map is about the fifth group; the connection with the rest is in [[M-product-metrics]].

**Three questions before launching any metric:** which business KPI does it explain; what will we do if it falls or rises; do we have the resources to react at the required frequency. If at least one has no answer — pick another metric or lower the frequency.

### Summary table
| Metric | What it measures | Scale | Formula (result, units) | When to use |
|---|---|---|---|---|
| **CSAT** (Customer Satisfaction Score) | satisfaction with a specific interaction, stage or feature | 1–5 (also 1–7, 1–10) | CSAT, % = number of 4–5 ratings / number of all responses × 100; or the mean score | after a deal, a support contact, a payment; rating a journey stage; new features, A/B tests |
| **CES** (Customer Effort Score) | how easy it is to complete a specific action | 1–5 (also 1–7); labeled in the session: 1 = "extremely easy" … 5 = "very hard" | CES = share of "easy" answers (in the session — ratings 1–2) / all answers × 100; or the mean score (the lower, the better) | onboarding, payment, listing placement, self-service, long forms (KYC, questionnaires); survey right after the action |
| **NPS** (Net Promoter Score) | willingness to recommend the product/company | 0–10 | NPS = % promoters (9–10) − % critics (0–6), points from −100 to +100; passives (7–8) are not included | regular tracking of overall loyalty, benchmarking, retention programs |
| **SUS** (System Usability Scale) | overall perceived usability | 1–5, 10 statements | odd item: response − 1; even item: 5 − response; sum × 2.5 → 0–100 points (not %) | comparing versions and competitors, after a usability test, A/B tests |
| **UMUX** | usability, a short version oriented to requirements | 1–7, 4 statements | by SUS logic (positive items: response − 1, negative: 7 − response), sum, normalized to 0–100 | quick monitoring, prototypes |
| **UMUX-LITE** | the same, 2 statements (requirements/capabilities + ease) | 1–7 | (sum − 2) / 12, × 100 → 0–100 | where the respondent cannot be loaded |
| **SUPR-Q** | convenience, trust/reliability, appearance, loyalty of a site/app | 7 items 1–5 + 1 NPS item (0–10) | sum of the 7 items + (NPS item / 2), all divided by 8; or by subscales | site/app diagnostics, benchmarking against the market (percentiles needed) |

**Reading benchmarks (from the course; norms depend on the industry and the country — compare first of all with your own history and competitors):**
- CSAT: 0–40% low (urgent changes needed), 40–60% medium (risks present), 60–80% good, 80%+ excellent. Three zones from practice: for a mass B2C service red < 70%, grey 70–80%, green > 80%; for financial and insurance services the bar is higher (75 / 75–85 / 85+).
- CES: share of "easy" — red < 50%, grey 50–65%, green > 65%; mean score (on a 1–5 scale) — red > 3.0, grey 2.5–3.0, green < 2.5.
- NPS: red < 0 (more critics than promoters), grey 0…+30 (normal, no wow), green > +30; for financial and premium services the bar is often raised to +40.
- SUS: 68 — average usability (more precisely: via percentiles and ranks); minimum sample ≈ 20 respondents, otherwise the confidence interval is too wide. For UMUX-LITE in fast iteration the benchmark is ≈ 12; for SUPR-Q ≈ 100 responses or ≥ 5% of the active base, and the result must be converted into percentiles for benchmarking (a raw score cannot be compared against someone else's percentile).

**Strengths and weaknesses.**
- CSAT: simple, tied to a stage, automatable; does not reflect long-term loyalty, depends on the mood "in the moment", needs regularity to show dynamics.
- CES: finds friction points, correlates with retention; explains nothing without an open question, measures only a single interaction, requires segmentation.
- NPS: universal, segments customers, allows comparison with the market; vulnerable to inflation and distortion, to cultural and regional specifics, does not assess individual steps.
- SUS/UMUX/SUPR-Q: give standardized comparison; show a "snapshot of the state", not the causes — combine with qualitative methods.

**Evidence strength.** An experience metric is a *measurement of opinion* on a specific sample and in a specific channel. It shows the level and the dynamics, but not the cause, and it does not guarantee behavior. Conclusions about the cause require an open question "what influenced the rating?", interviews, or pairing with behavioral data. A rating drop that coincides with a product change remains a hypothesis until seasonality, a change in the composition of respondents and of the channel are ruled out.

## Procedure
1. **Formulate the question and the metric.** Journey stage/event → CSAT or CES; overall loyalty → NPS; usability of the interface/versions → SUS, UMUX(-LITE); comprehensive site diagnosis → SUPR-Q. One survey — one goal.
2. **Define the trigger and the moment.** For CSAT/CES — immediately after the event (if possible within the next few hours, before the emotion fades) and *after a successful pass*, not after an error; for NPS — on a schedule (for example, quarterly) and after significant incidents; do not ask "about every little thing".
3. **Choose the channel** (see below) and a sampling strategy: a random share of events (around 5–10% of traffic, to avoid fatigue), full coverage only for rare events.
4. **Write the question.** One question — one thought; the scale direction is explicitly labeled; the event context is named ("order", "listing placement"). After the rating — an open question "What influenced your rating?".
5. **Fix before launch:** the alarm threshold, the reaction owner, the reaction deadline, the action on a drop, the analysis segments (novices/experienced, device, region, channel).
6. **Collect data with an identifier** (user-id/session) to link it with behavior.
7. **Compute and report with a confidence interval**, dynamics and segmentation; compare with the previous wave and a competitor, not with an "abstract norm".
8. **Link to the backlog:** red zone → a ticket with an owner → re-check after the release → closed / studied again. A metric without an owner and a reaction plan is a "report written into a drawer".
9. **Metrics retro (quarterly):** update thresholds, frequency, channels; measure the load on respondents (open rate, completion rate, refusals).

### Collection channels
| Channel | Pros | Cons | Suitable for |
|---|---|---|---|
| In-app/on-site survey (UX Feedback, pop-up) | at the point of contact, auto-segmentation | only active users, irritating | CSAT, CES after an action |
| E-mail | longer questionnaires, cheap | low open and completion rates, delay | NPS, SUPR-Q, SUS |
| Chat/chatbot | right after the dialog | only those who contacted | support CSAT |
| Push/SMS | fast reach | expensive, restrictions and consents | critical scenarios |
| Phone survey | depth of the "why" | does not scale, expensive | NPS after incidents, qualitative insights |
| Review analytics (app stores, social media) and behavior analytics | no questions required | self-selection, no representativeness | a supplement, topic discovery |
The channel changes both the sample and the number: the same question via push and by phone gives different results. For key metrics use two channels and record the channel in the data.
Tools from the course: SurveyMonkey, Typeform, Survio, UserTesting, Hotjar, Qualtrics, Sprig, Usabilla, Testograf, Lyssna, Pathway, Fabuza, Optimal Workshop.

**Sampling and schedule ("rolling sample").** For CSAT/CES — a random 5–10% of completed operations daily, not 100% of traffic (this is the "survey fatigue" refinement); full coverage only for rare events. For NPS — on a schedule (for example, once a quarter among active users), plus a separate wave among "dormant" users (for example, no actions for > 90 days) via e-mail, to understand the barriers to returning, and a measurement after critical incidents. Cooldown between repeated surveys of the same user ≈ 14 days; if refusals grow among "veterans" — stratified sampling (ask novices more often).

### Survey health and reaction plan
**Mini-dashboard of channel health:**
| KPI | Benchmark | If worse |
|---|---|---|
| Open rate (e-mail) | > 25% | the subject line and timing don't work |
| Completion rate | > 60% pop-up / > 40% e-mail | too long or does not fit the flow — shorten (for example, UMUX-LITE instead of SUS) |
| Refusals/fatigue (survey fatigue) | < 2% | cut the frequency, set a cooldown |
| Share of alarms driven to action | ≥ 70% | a metric without a reaction = noise |
Additionally for CSAT, track the share of "critics" (ratings 1–2): a growing share of negativity is an earlier signal than a falling average.

**Reaction SLA (an example from the course — substitute your own owners):**
| Metric | Alarm threshold | Owner | Reaction deadline |
|---|---|---|---|
| Stage CSAT | below the red zone (3-day rolling) | service owner | backlog ticket ≤ 8 h |
| Form CES | mean score > 3.0 | UX researcher + form developers | analysis and a quick-fix prototype ≤ 3 days |
| Quarterly NPS | −5 pp versus the previous quarter | product manager + marketing | cause and plan at the quarterly review |

**Quarterly metrics retro session (30 minutes; product manager, researcher, analyst, support lead):** metric dynamics → "alert → ticket → fix" chains → the link with money (correlation of Δ CSAT/NPS/CES with repeat orders, CAC, activation; if the correlation < 0.3 — reconsider the metric or the measurement point) → channel health → threshold revision. Move thresholds slowly so as not to "swing" the trend: `new threshold = min(3-month mean − ½·σ; current threshold + 3 pp)`.

## Template / checklist

**Measurement plan:**
| Field | Fill in |
|---|---|
| The business KPI the metric explains | |
| Metric, scale, formula | |
| Trigger event, survey moment | |
| Channel and share of respondents | |
| Question wording + the open "why" | |
| Analysis segments and linking fields (user-id) | |
| Alarm threshold, owner, reaction deadline | |
| Source of comparison (previous wave, competitor) | |
| Reaction plan for the red zone | |

**Required precision.** For a share (CSAT/CES "satisfied/easy") the 95% confidence interval is ≈ ±9.8 pp at n=100, ±5.7 pp at n=300, ±3.1 pp at n=1000 (worst case p=0.5). NPS has a wider spread, since two shares are combined: at 40% promoters and 30% critics, for n=300 the interval is ≈ ±9–10 points, for n=100 ≈ ±16. A 3–5-point NPS change on a small sample is not a signal. For the calculation see [[M-quant-methods]].

**SUS (10 statements, 1–5):** I would like to use it frequently; unnecessarily complex; easy to use; I would need the help of a technical specialist; the functions are well integrated; too much inconsistency; most people would learn it quickly; very cumbersome; I felt confident using it; a lot to learn before getting started. Odd items are positive, even items are negative.

**Sample questions.** CSAT: "How satisfied are you with [the order / the support]?" CES: "How easy was it to [request a return / place a listing]?" NPS: "On a scale of 0–10, how likely is it that you would recommend [the product] to someone you know?" + "What influenced your rating?" For your product, adapt the wording to the scenario ("would you recommend X for …").

**Setup checklist:** the trigger is chosen; there is one question; the scale and its direction are clear; the open "why" is added; the threshold and the owner are written down; the data is stored according to personal-data rules (consent, retention period); there is segmentation; the reaction plan is realistic.

## Typical mistakes
- **A metric for the sake of a metric:** no KPI, no threshold, no owner and no reaction plan.
- **Mixing up metrics:** NPS (loyalty to the brand) is compared with CSAT (satisfaction with a touchpoint); CSAT is used for "the app as a whole" (that is what SUS/UMUX are for); NPS is attached to every micro-moment.
- **No open "why" question:** the number rises or falls, and the cause is unknown (for example, a promo code temporarily "masked" the pain of delivery — after the promotion NPS came back).
- **Scale direction:** in the session the CES scale is labeled 1 = "extremely easy", and "easy" means ratings 1–2; on many platforms and in many sources "easy" sits at the top of the scale. Before computing, check the scale labels and fix the interpretation in the metric passport — otherwise comparing waves, and comparing with external data, loses meaning.
- **Surveying after an error or before the scenario is complete:** everyone answers "hard"; CES — after a successful pass.
- **Sample bias:** only active users or only happy ones are surveyed, one channel "covers everyone"; the response rate is not tracked.
- **An average without segments:** the hospital average hides where it hurts.
- **A mean score on an ordinal scale treated as "an exact number"** and small-sample comparisons without intervals.
- **Inflation and fatigue:** surveying 100% of traffic, too frequent repeats, incentivized answers (bonuses, pressure).
- **A lone NPS value without a benchmark:** "is +30 good?" depends on the industry and the segment; look at dynamics and competitors.
- **Transferring western norms (SUS 68, NPS 50) to the local market without adjustments.**

## Questions that can change the decision
- Which business KPI should the metric explain, and is there data to link it with behavior?
- What action happens in the red zone and who is responsible for it? Are there enough resources?
- At which point of the journey and at which moment after the event is it best to ask, so as not to get noise?
- Are there enough active users for the required precision in each segment?
- Are there competitors/market data for comparison (brand health tracking, industry reports)? See [[M-marketing-research]].
- Has the composition of the audience or the channel changed between waves (otherwise the dynamics cannot be read)?

## Related maps
[[M-product-metrics]], [[M-success-metrics]], [[M-quant-methods]], [[M-marketing-research]], [[M-research-types]], [[M-usability-testing]], [[M-cjm]], [[M-ux-heuristics]], [[M-pmf-scaling]]
