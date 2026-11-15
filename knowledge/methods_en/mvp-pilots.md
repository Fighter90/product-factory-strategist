---
id: M-mvp-pilots
lang: en
title: MVP, MLP and pilots — choosing a validation format, metrics, success criteria, conclusions
course: pm
sources: ["EN mirror of the RU methodology card M-mvp-pilots (knowledge/methods/mvp-pilots.md); original sources are listed in the RU card"]
stages: [validation, options, after-decision]
tags: [mvp, mlp, pilot, prototype, traction-model, success-criteria, input-output, counter-metrics, fake-door]
related: [M-solution-design, M-pmf-scaling, M-traction-model, M-product-metrics, M-usability-testing, M-usp, M-risks, M-roadmap, M-delivery, M-decision-daci]
---

# MVP, MLP and Pilots

## When to apply
There is a prioritized solution hypothesis; you need to choose the minimal validation format (a prototype, pilot, MVP, MLP), assign metrics and success criteria before launch, and then honestly interpret the result (scale / refine / shut down).

## Essence

| Format | Goal | Implementation | Does the user know it is a test? | Where in the cycle |
|---|---|---|---|---|
| Prototype | Test the idea, scenario, clarity | A non-working mock (Figma) | Yes | Discovery |
| Pilot | Check the base hypotheses the fastest and cheapest way | Manual implementation, mailings, a fake door, solution interviews, marketing | Often not | After Discovery, before development |
| MVP | Test the product/business on live users | A minimal working product | No, it works for real | After a successful pilot |
| MLP | Make the product loved, test retention and NPS | Working + emotion, a "wow" | No | After MVP, Growth |

- **A pilot** — "check the base": if the base assumptions fail, there is no point developing further. Metrics — the key **input** metrics; the duration is usually 1 month (1–4 weeks for online); involvement — discovery and targeted delivery. The key difference from a prototype — the user does not know it is a test, so the behavior is real.
- **An MVP** — the minimal viable version: it closes a specific need **the same way the final product will**. The task is real feedback: behavior "in production" can differ critically from interviews and prototypes. The scope is defined through user story mapping, JTBD, Kano, RICE/ICE.
- **An MLP** — beyond the base function it brings primary benefit/delight (example: a delivery MVP — "the food arrived"; an MLP — order tracking, push notifications, promos).
- **MVP types:** single-function (WhatsApp 2009 — statuses; messaging appeared when they noticed users communicating via statuses); "patchwork"/from ready-made parts (Groupon: WordPress + PDF + email); pre-order (Okko — ordering movies); a "concierge" (a human manually, the client knows — freelancer search); the "Wizard of Oz" (a human manually, the client does not know — table-booking automation, scooters); someone else's product (the "e-Muscovite" city-services case). An MVP can also be a non-IT product: the Skillbox/Skyeng EdTech cases — thousands of landing pages instead of a course.
- **The MVP limitation:** it works poorly for revolutionary solutions and new niches (the audience is not ready / will not give data) and for super-standard products — there it may be possible to go almost straight to the final version. Do not apply it where you cannot "under-deliver" (the lecture example — classifieds delivery).
- **The "right path" order:** functionality → reliability → usability → perfect design; not the other way around — first the value hypothesis, then comfort, then beauty. If an already-launched product pleases you — you are late.
- **Who works:** the PM (the process), a researcher (the scope and prototype), a designer, an editor, the team lead and the team, a project manager, an analyst (experiment design and analysis), a business leader and lawyers/finance as needed, a marketer when "selling" is needed. The PM's goal at the MVP stage is to maximize awareness of user problems and needs, not to police spec compliance.
- **MVP creation steps (8):** problem → segment → competitors → needs/USP/key hypotheses → CJM and user story mapping, choosing functions → development and coordination → testing and refinement → the decision about the product's future.

### Metrics
- **Input** (controllable): reach, the share of those who saw/clicked/activated; more important on an MVP/pilot — they change fast and are easier to control. **Output** (result): conversion to purchase, revenue/AOV, retention, sign-ups — these matter when testing monetization, LTV, retention, scale. **Qualitative/counter-metrics**: CSAT, NPS, CSI, the number of bugs and complaints, interview feedback — always needed to understand the causes of success/failure.
- **The metric is directly tied to the hypothesis:** if the hypothesis is about conversion — measure conversion, not the "page open rate". The **traction model** links input and output. A Trade-In funnel example: segment 10,000 → saw the button 3,000 (30%) → clicked 600 (20%) → filled the application 180 (30%) → deal 54 (30%); the output metric — deals. For a pilot, choose input values whose achievement tests the hypothesis; do not carry out the whole backlog, but the key results that move toward traction ([[M-traction-model]]).
- **Success criteria — before launch.** Example: ≥ 3% of buyers use Trade-In within 2 weeks; a comparison with an internal/industry benchmark (3% is typical → a target of 5%).

### Testing
- The segment is defined at the first preparation stage; start with the "core" — where the pain is sharpest; do not launch on everyone.
- The start — when all the features without which the test is impossible are implemented and all approvals are obtained (legal, security, finance, marketing).
- The duration — as long as needed for a statistically significant result; end by data volume, not by date; account for the purchase cycle (once a month → longer), seasonality, external promotions.
- Log all changes during the test; otherwise it is unclear what produced the effect.
- Move from the MVP through milestones, gradually closing jobs entirely.
- **"Failing correctly":** failure is an investment in knowledge; log the steps, metrics, decisions and conclusions (a retrospective); share the learnings with the team and other products of the company; in the debrief, localize where the error was — in the hypothesis, segment, implementation or timing; convert feedback into new hypotheses or a pivot.

## Procedure
1. Formulate the hypothesis: problem and segment → solution → the expected metric change → success criterion → validation tool. Source: [[M-solution-design]].
2. Choose the cheapest format that removes the **main** uncertainty: clarity → prototype; demand → fake door/pilot/mailing; usability → usability testing; monetization/behavior → MVP; emotion/retention → MLP.
3. Select the pilot's base hypotheses (without which there is no point going further). Each — with the value being tested, an MDE and a threshold. The ideal list: an input → output link, 1–3 hypotheses, measurable within the pilot's duration.
4. Define the segment, channel, volume, duration, counter-metrics with thresholds and stop conditions.
5. Fix the plan and criteria (date, author). Get the approvals.
6. Launch, keep a change log, watch the counter-metrics.
7. Debrief the result: the funnel (where the drops are), a comparison with the criteria, a verification of every assumption, unexpected usage scenarios, qualitative feedback.
8. Make and record the decision: **success** (metrics achieved, users return/recommend/pay → scale, automate); **partial success** (some thresholds met, there is a bottleneck → refinement and a re-test, segmentation); **failure** (critical metrics not met → shut down or radically revise, record the causes).
9. Transition conditions: prototype → pilot (the scenario is clear, interest in interviews); pilot → MVP (the first payers/minimal traction, no blockers); MVP → MLP (the first "fans", retention, reviews); MLP → scale ([[M-pmf-scaling]]).

## Template / checklist
| Hypothesis (if… then…) | Validation format | Metric (input/output) | Baseline | Success criterion | Failure/kill criterion | Counter-metrics (threshold) | Duration and sample | Why so |
|---|---|---|---|---|---|---|---|---|
Course practice: fill in the "hypothesis → validation method → success criteria" table, explain the choice, prioritize 1–2 hypotheses for the pilot launch.

A pre-launch checklist: the goal and testable hypotheses · metrics and thresholds set · the segment and share chosen · the duration/volume sufficient for significance · counter-metrics · a change log · approvals obtained · a plan for "what we do on success/partial/failure" · owners defined.

## Typical mistakes
- The MVP does not close the key need or poorly communicates the USP; an "ideal product" instead of a minimum, or too few functions.
- No clear goal, metrics and criteria; thresholds "adjusted" after the test.
- Launching "on everyone" → noise; stopping too early/late ("two days is enough").
- Only the final metric without process metrics; ignoring qualitative data; comparing against the benchmarks of mature Big Tech products.
- Not using the MVP's conclusions; not collecting feedback; weak control of timelines.
- Applying MVP everywhere or nowhere; taking on an MVP without prototyping.
- Scaling on unconvincing results; explaining failure by external causes without data.
- Not involving critical participants (an analyst, lawyers), so the test gets "shut down" after the start.

## Questions that can change the decision
- Which main uncertainty are we removing: value, usability, economics, technical feasibility?
- Can the hypothesis be tested manually/without development (a pilot) before building an MVP?
- Is the traffic in the target segment sufficient for a significant conclusion within the time frame?
- Is emotion needed (an MLP), or is the base function enough to test value?
- What exactly to close/revise if the thresholds are only partially met?

## Related cards
[[M-solution-design]], [[M-pmf-scaling]], [[M-traction-model]], [[M-product-metrics]], [[M-usability-testing]], [[M-usp]], [[M-risks]], [[M-roadmap]], [[M-delivery]], [[M-decision-daci]]
