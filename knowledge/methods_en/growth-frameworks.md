---
id: M-growth-frameworks
lang: en
title: Growth frameworks: AARRR, HEART, Flywheel, Growth Loops, Growth Model Canvas
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [options, strategy]
tags: [aarrr, heart, flywheel, growth-loop, virality, funnel, growth-model-canvas, north-star-metric]
related: [M-product-metrics, M-success-metrics, M-goals-drivers-bets, M-business-models, M-traction-model, M-pmf-scaling, M-loyalty-metrics]
---

# Growth frameworks: AARRR, HEART, Flywheel, Growth Loops, Growth Model Canvas

## When to apply
"How will the product grow?", "which framework to choose — a funnel or a loop?", "design a growth loop / viral cycle", "which metrics to measure at each stage". Choosing a growth model is a bespoke recipe; the main thing is that the math closes.

## Core idea
**A linear funnel (AARRR, HEART):** requires constantly refilling the "top" with external investment in acquisition; at every stage users leak out irreversibly.
**A growth loop (Flywheel, Growth Loop):** a closed cycle where the cycle's output (an acquired user, created content) becomes the cause of acquiring new users in the next cycle — growth "from inside".

| Product type | Recommended framework (not a hard rule) |
|---|---|
| E-commerce | AARRR |
| SaaS | journey funnel + HEART |
| Games | Growth Loop |
| Social networks | Growth Loop + HEART |
| Media | Growth Loop + HEART |
Choice factors: the stage of the product, business goals, the market, the product type.

### AARRR (Pirate Metrics), 6 stages in the skill's version
| Stage | Essence | Channels | Metrics |
|---|---|---|---|
| Awareness | people learn about you | SEO, SEM, content, affiliate, PR, social networks, mailings, ASO | visits, reach, CTR, CPC, CPM, bounce, engagement |
| Acquisition | visitors identified | blog, white papers, chat widgets, landing pages, webinars, retargeting, quizzes | subscriptions, downloads, Cost per Lead, trial signups |
| Activation | the first great experience (the Aha-moment) | UX, tutorials, support, onboarding, drip | core feature usage, onboarding success, CAC |
| Retention | users come back | email, pushes, extra features, lifetime marketing | churn, DAU, MAU, returning customers |
| Revenue | behavior generates income | UX, sales, checkout | CLV, conversion, upsell/cross-sell, average check, CLV/CAC |
| Referral | users bring in new ones | referral mechanics, sharing, ratings, viral campaigns | invites, shares, viral coefficient, NPS |
Weaknesses: constant top-of-funnel refilling (expensive, limited scalability), irreversible leakage, no feedback loops.

### HEART (Google) — a UX quality framework
For each dimension: Goal → Signals → Metrics.
- Happiness — store ratings, an in-app survey, the Customer Effort Score.
- Engagement — DAU, actions per user, the number of saved/favorited items.
- Adoption — download rate, Time to Value, onboarding completion.
- Retention — 30-/90-day retention, MAU, churn/uninstall.
- Task Success — task completion time, search success rate, error rate.

### Flywheel: Activate → Adopt → Adore → Advocate
| Stage | Segment | Strategy | Metric |
|---|---|---|---|
| Activate | evaluating | an easy path to the Aha-moment, remove barriers | sign-up rate |
| Adopt | novice | habit formation, teaching new features | retention rate |
| Adore | regular user | improve the experience, anticipate needs | NPS |
| Advocate | champion | prompt recommendations (this starts a new cycle) | referrals invited |
Example (the "jobs" vertical of a classifieds site): positive loops — more resumes → more responses → more employers → more vacancies → more job seekers; the negative (control) loop — fewer job seekers → more fraudsters.

### Growth Loop: designing
The universal cycle: product growth → more and better resources (people and capital) → bigger meaningful problems solved → product growth.
- **Observe:** the real behavior scenario; the motivation — to look good / to feel good / to help others / to get / to bond / to convince.
- **Design:** what motivates and how to reflect it in the product; which action we expect and how to simplify it; what result the user gets and how to amplify it.
- **Iterate:** the loop steps to track and a metric for each step.
Example: doctors share medical content → the product helps find supporting evidence → content with the author's photo and credentials is visible to others → they create their own → metrics: read/bookmarked, shared, came via link, registrations with UTM.

### Growth Model Canvas
Target audience (persona) · Value Proposition · North Star Metric · WOW Moment · Product DNA (customers need it and are "hooked") · the 6 stages Awareness…Referral with metrics.

## Procedure
1. Describe the product, the stage, the growth goal, the market; define the NSM ([[M-product-metrics]]).
2. Pick 1–2 candidates from the table; justify in writing why the others were rejected.
3. **Check the math of the chosen model:**
   - funnel: `Result = Input × CR1 × CR2 × …`, channel economics — `LTV > CAC`, payback ([[M-unit-economics]]);
   - loop (the standard formula, not from the skill): the loop coefficient `K = i × c` (invitations / created content per user × the conversion of invitees into new users); at `K < 1` with a constant external inflow P the steady-state total is `P / (1 − K)`; at `K ≥ 1` growth is self-sustaining, capped in practice by saturation; the loop time and the quality of new users matter.
4. Design the loop via Observe → Design → Iterate; write down: trigger → action → result → the input of the next cycle; leaks and negative loops.
5. Assign a metric to every step and a way to measure it (events, UTM).
6. Fill in the Growth Model Canvas; link it to the traction model: the loop is the virality driver, the funnel is the driver of acquisition/activation/retention ([[M-traction-model]]).
7. Control metrics for every stage + health counter-metrics.

## Template / checklist
Loop:
| Step | What the user does | Motivation | Result | Step metric | Conversion |
|---|---|---|---|---|---|
| 1 | | | | | |
| … | | | | | |
| Cycle output → next cycle's input | | | | K, loop time | |
Output artifacts: the choice and its justification; a funnel or a loop with metrics; channels per stage; a Growth Loop; a Canvas; control metrics.

## Typical mistakes
- Copying a framework "just like the market leader's" without checking the math.
- Taking HEART (UX quality) for an acquisition model, and AARRR for a quality model.
- Drawing a loop without measurable steps and conversions.
- Ignoring negative loops (fraudsters, abusers, spam).
- Optimizing Referral while Activation/Retention are weak.
- Leaning on "virality" without computing K and the loop time.

## Questions that can change the decision
- Where do >70% of new users come from today (which channel), and does that channel scale ([[M-pmf-scaling]])?
- Is there a natural result of usage that is visible to others (content, an invitation)?
- Do some users retain (does the curve reach a plateau)? If not, the loop will amplify the leak.
- What is the cost of a unit of external inflow P in the funnel?
- What is the Aha-moment, and how many users reach it?

## Related maps
[[M-product-metrics]], [[M-success-metrics]], [[M-goals-drivers-bets]], [[M-business-models]], [[M-traction-model]], [[M-pmf-scaling]], [[M-loyalty-metrics]], [[M-unit-economics]]
