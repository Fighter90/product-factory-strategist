---
id: M-mvp-pilots
lang: en
title: MVP, MLP and pilots — choosing the validation format, metrics, success criteria, conclusions
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [validation, options, after-decision]
tags: [mvp, mlp, pilot, prototype, traction-model, success-criteria, input-output, counter-metrics, fake-door]
related: [M-solution-design, M-pmf-scaling, M-traction-model, M-product-metrics, M-usability-testing, M-usp, M-risks, M-roadmap, M-delivery, M-decision-daci]
---

# MVP, MLP and pilots

## When to apply
A prioritized solution hypothesis exists; you need to choose the minimal validation format (prototype, pilot, MVP, MLP), assign metrics and success criteria before launch, and then interpret the result honestly (scale / rework / shut down).

## Core idea

| Format | Goal | Implementation | Does the user know it's a test? | Where in the cycle |
|---|---|---|---|---|
| Prototype | Check the idea, the scenario, comprehensibility | A non-working mockup (Figma) | Yes | Discovery |
| Pilot | Check the base hypotheses in the fastest, cheapest way | Manual implementation, mailings, fake door, solution interviews, marketing | Often no | After Discovery, before development |
| MVP | Check the product/business on live users | A minimal working product | No — it works for real | After a successful pilot |
| MLP | Make the product loved, check retention and NPS | Working + emotion, "wow" | No | After MVP, Growth |

- **Pilot** — "check the base": if the base assumptions don't hold, there is no point in developing further. Metrics — the key **input** metrics; duration is usually 1 month (1–4 weeks for online); involvement — discovery and, pointwise, delivery. The key difference from a prototype: the user doesn't know it's a test, so the behavior is real.
- **MVP** — the minimum viable version: it covers a specific need **in the same way the final product will**. The task is real feedback: behavior "in production" can differ critically from interviews and prototypes. The composition is determined through user story mapping, JTBD, Kano, RICE/ICE.
- **MLP** — beyond the base function it delivers primary benefit/delight (example: a delivery MVP — "brought the food"; MLP — order tracking, push notifications, promos).
- **Types of MVP:** single-feature (WhatsApp 2009 — statuses; messaging appeared when they noticed users were communicating through statuses), "cobbled together" from ready-made pieces (Groupon: WordPress + PDF + email), pre-order (Okko — ordering movies), "concierge" (a human does it manually, the client knows — freelancer search), "Wizard of Oz" (a human does it manually, the client doesn't know — restaurant booking automation, scooter rentals), someone else's product ("the electronic Muscovite"). An MVP can also be a non-IT product: the Skillbox/Skyeng EdTech cases — thousands of landing pages instead of a course.
- **The MVP limitation:** it works poorly for revolutionary solutions and new niches (the audience isn't ready / won't give you data) and for super-standard products — there you may go almost straight to the final version. Don't apply it where you cannot "under-build" (the example from the lecture — classifieds delivery).
- **The "right path" order:** functionality → reliability → convenience → perfect design; not the reverse — first the value hypothesis, then comfort, then beauty. If an already launched product pleases everyone — you are late.
- **Who works on it:** the PM (the process), the researcher (scope and prototype), designer, editor, team lead and team, project manager, analyst (experiment design and analysis), business leader and lawyers/finance as needed, marketer when the product needs to be "sold". The PM's goal at the MVP stage is to maximize awareness of user problems and needs, not to control compliance with the spec.
- **8 steps to build an MVP:** problem → segment → competitors → needs/USP/key hypotheses → CJM and user story mapping, feature selection → development and coordination → testing and refinement → decision about the product's future.

### Metrics
- **Input** (controllable): reach, the share of those who saw/clicked/activated; more important at the MVP/pilot stage — they change fast and are easier to control. **Output** (result): conversion to purchase, revenue/AOV, retention, registrations — they matter when you test monetization, LTV, retention, scale. **Qualitative/counter-metrics**: CSAT, NPS, CSI, the number of bugs and complaints, interview feedback — always needed to understand the causes of success or failure.
- **The metric is directly tied to the hypothesis:** if the hypothesis is about conversion — measure conversion, not "page open rate". The **traction model** links input and output. Trade-In funnel example: segment 10,000 → saw the button 3,000 (30%) → clicked 600 (20%) → filled in the application 180 (30%) → deal 54 (30%); the output metric is deals. For a pilot you choose input values whose achievement tests the hypothesis; you don't dump the whole backlog — only the key results moving you toward traction ([[M-traction-model]]).
- **Success criteria — before launch.** Example: ≥ 3% of buyers use Trade-In within 2 weeks; comparison with an internal/industry benchmark (3% is typical → target 5%).

### Testing
- The segment is defined at the first stage of preparation; start with the "core" — where the pain is sharpest; don't launch on everyone.
- Start — when all the features without which the test is impossible are implemented and all approvals are obtained (legal, security, finance, marketing).
- Duration — as long as needed for a statistically significant result; end by data volume, not by date; account for the purchase cycle (once a month → longer), seasonality, external promotions.
- Log every change during the test; otherwise it's unclear what produced the effect.
- Move from the MVP through milestones, closing whole jobs step by step.
- **"Failing correctly":** failure is an investment in knowledge; record the steps, metrics, decisions and conclusions (retrospective); share learnings with the team and other products of the company; in the review, localize where the error was — in the hypothesis, the segment, the implementation or the timing; convert feedback into new hypotheses or a pivot.

## Procedure
1. Formulate the hypothesis: problem and segment → solution → expected change in the metric → success criterion → validation tool. Source — [[M-solution-design]].
2. Choose the cheapest format that removes the **main** uncertainty: comprehensibility → prototype; demand → fake door/pilot/mailing; usability → usability test; monetization/behavior → MVP; emotion/retention → MLP.
3. Select the base hypotheses of the pilot (without which there is no point in going further). Each with the value being tested, the MDE and a threshold. The ideal list: an input → output linkage, 1–3 hypotheses, measurable within the pilot's term.
4. Define the segment, channel, volume, duration, counter-metrics with thresholds and stop conditions.
5. Fix the plan and criteria (date, author). Get the approvals agreed.
6. Launch, keep the change log, watch the counter-metrics.
7. Analyze the result: the funnel (where the drops are), comparison against the criteria, checking each assumption, unexpected usage scenarios, qualitative feedback.
8. Make the decision and record it: **success** (metrics met, users return/recommend/pay → scale, automate); **partial success** (some thresholds met, a bottleneck exists → rework and retest, segmentation); **failure** (critical metrics missed → shut down or radically rethink, record the causes).
9. Transition conditions: prototype → pilot (the scenario is clear, interest in interviews); pilot → MVP (first payers/minimal traction, no blockers); MVP → MLP (the first "fans", retention, reviews); MLP → scale ([[M-pmf-scaling]]).

## Template / checklist
| Hypothesis (if… then…) | Validation format | Metric (input/output) | Baseline | Success criterion | Failure/kill criterion | Counter-metrics (threshold) | Duration & sample | Why so |
|---|---|---|---|---|---|---|---|---|
Course practice: fill in the table "hypothesis → validation method → success criteria", explain the choice, prioritize 1–2 hypotheses for the pilot launch.

Pre-launch checklist: the goal and testable hypotheses · metrics and thresholds set · segment and share chosen · duration/volume sufficient for significance · counter-metrics · a change log · approvals obtained · a plan for "what we do on success/partial success/failure" · owners defined.

## Typical mistakes
- The MVP doesn't cover the key need or communicates the USP poorly; an "ideal product" instead of a minimum, or too few functions.
- No clear goal, metrics or criteria; thresholds "adjusted" after the test.
- Launching "on everyone" → noise; stopping too early/too late ("two days is enough").
- Only the final metric without process metrics; ignoring qualitative data; comparing against benchmarks of mature Big Tech products.
- Not using the MVP conclusions; not collecting feedback; weak control of timing.
- Applying MVP everywhere or nowhere; taking on an MVP without prototyping.
- Scaling on unconvincing results; explaining failure by external causes without data.
- Not involving critical participants (the analyst, lawyers), so the test gets "wrapped up" after the start.

## Questions that can change the decision
- Which main uncertainty are we removing: value, usability, economics, technical feasibility?
- Can the hypothesis be checked manually/without development (a pilot) before building an MVP?
- Is there enough traffic in the target segment for a significant conclusion within the term?
- Is emotion (MLP) needed, or is the base function enough to validate the value?
- What exactly should be shut down/rethought if the thresholds are only partially met?

## Related maps
[[M-solution-design]], [[M-pmf-scaling]], [[M-traction-model]], [[M-product-metrics]], [[M-usability-testing]], [[M-usp]], [[M-risks]], [[M-roadmap]], [[M-delivery]], [[M-decision-daci]]
