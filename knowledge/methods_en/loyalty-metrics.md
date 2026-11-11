---
id: M-loyalty-metrics
title: Loyalty research and customer metrics (NPS, CSAT, CES, SUS, UMUX, SUPR-Q)
course: pm-approaches-en
sources: ["EN mirror of RU card M-loyalty-metrics (knowledge/methods/loyalty-metrics.md); original sources are listed in the RU card"]
stages: [validation, after-decision]
tags: [nps, csat, ces, sus, umux, supr-q, loyalty, satisfaction, cx, surveys, trigger-surveys]
related: [M-product-metrics, M-success-metrics, M-quant-methods, M-marketing-research, M-research-types, M-usability-testing, M-cjm, M-ux-heuristics, M-brief-hypotheses, M-pmf-scaling]
lang: en
---

# Loyalty research and customer metrics (NPS, CSAT, CES, SUS, UMUX, SUPR-Q)

## When to use

You need to measure how customers perceive the product: how satisfied they are with a specific step, how easy it is to complete a task, how willing they are to recommend, how convenient the interface is. This card picks the metric to fit the question, and shows formulas, collection methods, benchmarks, and interpretation pitfalls.

## Core

**Why experience metrics.** They are an early signal for money: investment in customer experience raises revenue over time, customers return more willingly and are ready to pay for a good experience. Metric value ⇔ success criterion ⇔ product management. Experience metrics belong to the *relational* layer (what people feel and rate) and complement *behavioral* metrics (DAU/MAU, conversion, retention, load time): behavior says *what* is happening, the rating — *why* and how much it hurts.

**Metric groups across the lifecycle:** Acquisition, Activation, Engagement, Retention, Loyalty and satisfaction, plus additional (niche) ones. This card is about the fifth group; the links to the rest are in [[M-product-metrics]].

**Three questions before launching any metric:** which business KPI does it explain; what will we do if it drops or rises; are there enough resources to react at the required frequency. If at least one has no answer — pick a different metric or lower the frequency.

### Summary table

| Metric | What it measures | Scale | Formula (result, units) | When to use |
|---|---|---|---|---|
| **CSAT** (Customer Satisfaction Score) | satisfaction with a specific interaction, stage, or feature | 1–5 (also 1–7, 1–10) | CSAT, % = number of 4–5 ratings / number of all responses × 100; or the average score | after a purchase, a support request, payment; rating a stage of the journey; new features, A/B tests |
| **CES** (Customer Effort Score) | how easy it is to complete a specific action | 1–5 (also 1–7); as labeled in the course: 1 = "extremely easy" … 5 = "very difficult" | CES = share of "easy" responses (in the course — ratings 1–2) / all responses × 100; or the average score (the lower, the better) | onboarding, payment, listing placement, self-service, long forms (KYC, questionnaires); survey immediately after the action |
| **NPS** (Net Promoter Score) | willingness to recommend the product/company | 0–10 | NPS = % promoters (9–10) − % detractors (0–6), points from −100 to +100; passives 7–8 are excluded | regular tracking of overall loyalty, benchmark, retention programs |
| **SUS** (System Usability Scale) | overall perceived usability | 1–5, 10 statements | odd-numbered item: response − 1; even-numbered: 5 − response; sum × 2.5 → 0–100 points (not %) | comparing versions and competitors, after a usability test, A/B tests |
| **UMUX** | usability, a short version oriented to requirements | 1–7, 4 statements | by SUS logic (positive items − 1, negative items 7 − response), sum, rescaled to 0–100 | quick monitoring, prototypes |
| **UMUX-LITE** | the same, 2 statements (requirements/capabilities + ease) | 1–7 | sum − 2, divided by 12, × 100 → 0–100 | where you cannot burden the respondent |
| **SUPR-Q** | convenience, trust/reliability, appearance, loyalty — for a site/app | 7 items 1–5 + 1 NPS item (0–10) | sum of the 7 items + (NPS item / 2), all / 8; or by subscales | site/app diagnostics, benchmark against the market (percentiles required) |

**Reading benchmarks (from the course; norms depend on the industry and the country — compare primarily with your own history and competitors):**
- CSAT: 0–40% low (urgent changes needed), 40–60% medium (there are risks), 60–80% good, 80%+ excellent. Three zones from practice: for a mass B2C service red < 70%, gray 70–80%, green > 80%; for financial and insurance services the bar is higher (75 / 75–85 / 85+).
- CES: share of "easy" — red < 50%, gray 50–65%, green > 65%; average score (1–5 scale) — red > 3.0, gray 2.5–3.0, green < 2.5.
- NPS: red < 0 (more detractors than promoters), gray 0…+30 (the norm without a wow effect), green > +30; for financial and premium services the bar is often raised to +40.
- SUS: 68 is the average usability level (more precisely: via percentiles and ranks); the minimum sample is ≈ 20 respondents, otherwise the interval is too wide. For UMUX-LITE in fast iteration the guideline is ≈ 12; for SUPR-Q ≈ 100 responses or ≥ 5% of the active base, and the result must be converted into percentiles for benchmarking (a raw score cannot be compared with someone else's percentile).

**Strengths and weaknesses.**
- CSAT: simple, tied to a stage, automatable; does not reflect long-term loyalty, depends on in-the-moment mood, requires regularity to see dynamics.
- CES: finds bottlenecks, correlates with retention; explains nothing without an open question, measures only one interaction, requires segmentation.
- NPS: universal, segments customers, allows comparison with the market; susceptible to gaming and distortion, to cultural and regional specifics, does not evaluate individual steps.
- SUS/UMUX/SUPR-Q: give a standardized comparison; show a "snapshot of the state", not the causes — combine with qualitative methods.

**Strength of evidence.** An experience metric is a *measurement of opinion* on a specific sample and in a specific channel. It shows the level and the dynamics, but not the cause, and it does not guarantee behavior. Conclusions about the cause require an open question "what influenced your rating?", interviews, or linking with behavioral data. A rating drop that coincides with a product change is a hypothesis until seasonality, a change in the composition of respondents, and the channel have been ruled out.

## Procedure

1. **Formulate the question and the metric.** Stage of the journey / event → CSAT or CES; overall loyalty → NPS; usability of the interface / versions → SUS, UMUX(-LITE); comprehensive diagnosis of a site → SUPR-Q. One survey — one goal.
2. **Define the trigger and the moment.** For CSAT/CES — immediately after the event (if possible within the next few hours, while the emotion has not faded) and *after a successful pass*, not after an error; for NPS — on a schedule (for example, quarterly) and after significant incidents; do not ask "about every little thing".
3. **Choose the channel** (see below) and the sampling strategy: a random share of events (about 5–10% of traffic, to avoid fatigue), full coverage only for rare events.
4. **Write the question.** One question — one thought; the direction of the scale is explicitly labeled; the context of the event is named ("order", "listing placement"). After the rating — the open question "What influenced your rating?".
5. **Fix before launch:** the alarm threshold, the owner of the reaction, the reaction deadline, the action upon a drop, the analysis segments (newcomers/experienced users, device, region, channel).
6. **Collect data with an identifier** (user-id/session) to link it with behavior.
7. **Compute and present with a confidence interval**, dynamics, and segmentation; compare with the previous wave and a competitor, not with an "abstract norm".
8. **Link to the backlog:** red zone → a ticket with an owner → verification after the release → closure / re-examination. A metric without an owner and a reaction plan is a "report filed into a drawer".
9. **Metrics retro (quarterly):** update thresholds, frequency, channels; measure the load on respondents (open rate, completion rate, opt-outs).

### Collection channels

| Channel | Pros | Cons | Suitable for |
|---|---|---|---|
| In-app/on-site survey (UX Feedback, pop-up) | at the point of contact, auto-segmentation | only active users, annoying | CSAT, CES after an action |
| E-mail | longer questionnaires, cheap | low open and completion rates, delay | NPS, SUPR-Q, SUS |
| Chat/chatbot | right after the dialogue | only those who reached out | support CSAT |
| Push/SMS | fast coverage | expensive, restrictions and consent requirements | critical scenarios |
| Phone survey | depth of the "why" | does not scale, expensive | NPS after incidents, qualitative insights |
| Review analytics (app stores, social media) and behavior | no questions required | self-selection, no representativeness | a supplement, topic discovery |

The channel changes both the sample and the number: the same question via push and over the phone gives different results. For key metrics use two channels and record the channel in the data.
Tools from the course: SurveyMonkey, Typeform, Survio, UserTesting, Hotjar, Qualtrics, Sprig, Usabilla, Testograf, Lyssna, Pathway, Fabuza, Optimal Workshop.

**Sampling and schedule ("rolling sample").** For CSAT/CES — randomly 5–10% of completed operations daily, not 100% of traffic (the "survey fatigue" refinement); full coverage — only for rare events. For NPS — on a schedule (for example, once a quarter among active users), plus a separate wave among "dormant" users (for example, no actions for > 90 days) via e-mail to understand the barriers to return, and a measurement after critical incidents. Cooldown between repeated surveys of the same user ≈ 14 days; if opt-outs grow among "veterans" — stratified sampling (ask newcomers more often).

### Survey health and reaction plan

**Mini-dashboard of channel health:**
| KPI | Benchmark | If worse |
|---|---|---|
| Open rate (e-mail) | > 25% | the subject line and timing are not working |
| Completion rate | > 60% pop-up / > 40% e-mail | too long or does not fit into the flow — shorten (for example, UMUX-LITE instead of SUS) |
| Opt-outs/fatigue (survey fatigue) | < 2% | cut the frequency, set a cooldown |
| Share of alerts followed through to action | ≥ 70% | a metric without a reaction = noise |

Additionally for CSAT, track the share of "detractors" (ratings 1–2): a growing share of negativity is an earlier signal than a falling average.

**Reaction SLA (an example from the course — substitute your own owners):**
| Metric | Alarm threshold | Owner | Reaction deadline |
|---|---|---|---|
| Stage CSAT | below the red zone (3-day rolling) | service owner | ticket to the backlog ≤ 8 h |
| Form CES | average score > 3.0 | UX researcher + form development team | analysis and a quick-fix prototype ≤ 3 days |
| Quarterly NPS | −5 p.p. against the previous quarter | product manager + marketing | cause and plan at the quarterly review |

**Quarterly metrics retro session (30 minutes; product manager, researcher, analyst, support lead):** metric dynamics → "alert → ticket → fix" chains → link to money (correlation of Δ CSAT/NPS/CES with repeat orders, CAC, activation; if the correlation is < 0.3 — reconsider the metric or the measurement point) → channel health → revision of thresholds. Change a threshold slowly so as not to "rock" the trend: `new threshold = min(3-month average − ½·σ; current threshold + 3 p.p.)`.

## Template / checklist

**Measurement plan:**
| Field | Fill in |
|---|---|
| The business KPI the metric explains | |
| Metric, scale, formula | |
| Trigger event, survey moment | |
| Channel and share of respondents | |
| Question wording + the open "why" | |
| Analysis segments and fields for linking (user-id) | |
| Alarm threshold, owner, reaction deadline | |
| Source of comparison (previous wave, competitor) | |
| Reaction plan for the red zone | |

**Required precision.** For a proportion (CSAT/CES "satisfied/easy") the 95% confidence interval is ≈ ±9.8 p.p. at n=100, ±5.7 p.p. at n=300, ±3.1 p.p. at n=1000 (worst case p=0.5). NPS has a wider spread because two proportions are added together: at 40% promoters and 30% detractors the interval is ≈ ±9–10 points for n=300, ≈ ±16 for n=100. A change in NPS of 3–5 points on a small sample is not a signal. For the calculation see [[M-quant-methods]].

**SUS (10 statements, 1–5):** I would like to use it frequently; unnecessarily complex; easy to use; I would need the help of a technical specialist; the functions are well integrated; too much inconsistency; most people would learn quickly; very cumbersome; felt confident; needed to learn a lot before starting. Odd-numbered items are positive, even-numbered ones are negative.

**Sample questions.** CSAT: "How satisfied are you with [the order/the support]?". CES: "How easy was it to [request a refund / place an ad]?". NPS: "On a scale of 0–10, how likely is it that you would recommend [the product] to a friend or colleague?" + "What influenced your rating?". For the product, adapt the wording to the scenario ("would you recommend X for …").

**Setup checklist:** the trigger is chosen; the question is a single one; the scale and its direction are clear; the open "why" is added; the threshold and the owner are written down; the data is stored according to personal data rules (consent, retention period); segmentation is in place; the reaction plan is realistic.

## Typical mistakes

- **A metric for the metric's sake:** no KPI, threshold, owner, or reaction plan.
- **Metric confusion:** NPS (loyalty to the brand) is compared with CSAT (satisfaction with a point of contact); CSAT is used for "the whole app in general" (for that, SUS/UMUX); NPS is placed on every micro-moment.
- **No open "why" question:** the number rises or falls, and the cause is unknown (for example, a promo code temporarily "painted over" the pain of delivery — after the campaign NPS came back).
- **Scale direction:** in the CES lesson the scale is labeled 1 = "extremely easy", and "easy" counts as ratings 1–2; in a number of platforms and sources "easy" sits at the top of the scale. Before computing, verify the scale labels and fix the interpretation in the metric passport — otherwise comparing waves and comparing with third-party data loses its meaning.
- **Surveying after an error or before completing the scenario:** everyone answers "difficult"; CES — after a successful pass.
- **Sample bias:** only active or only satisfied users are surveyed; a single channel "covers everyone"; the share of respondents is not tracked.
- **An average without segments:** the hospital-wide average hides where it hurts.
- **The average score on an ordinal scale treated as an "exact number"** and comparisons on small samples without intervals.
- **Gaming and fatigue:** surveying 100% of traffic, too frequent repeats, incentivized answers (bonuses, pressure).
- **A single NPS value without a benchmark:** "is +30 good?" depends on the industry and the segment; look at the dynamics and the competitors.
- **Transferring Western norms (SUS 68, NPS 50) to the local market without adjustments.**

## Questions that can change the decision

- Which business KPI should the metric explain, and is there data to link it with behavior?
- What action will follow a red zone, and who is responsible for it? Are there enough resources?
- At which point of the journey and at which moment after the event is it best to ask, so as not to get noise?
- Are there enough active users for the required precision in every segment?
- Are there competitors/market data for comparison (brand health tracking, industry reports)? See [[M-marketing-research]].
- Has the composition of the audience or the channel changed between waves (otherwise the dynamics cannot be read)?

## Related cards

[[M-product-metrics]], [[M-success-metrics]], [[M-quant-methods]], [[M-marketing-research]], [[M-research-types]], [[M-usability-testing]], [[M-cjm]], [[M-ux-heuristics]], [[M-pmf-scaling]]
