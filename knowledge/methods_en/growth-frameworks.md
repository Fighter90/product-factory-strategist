---
id: M-growth-frameworks
lang: en
title: Growth frameworks: AARRR, HEART, Flywheel, Growth Loops, Growth Model Canvas
course: skills
sources: ["EN mirror of the RU methodology card M-growth-frameworks (knowledge/methods/growth-frameworks.md); original sources are listed in the RU card"]
stages: [options, strategy]
tags: [aarrr, heart, flywheel, growth-loop, virality, funnel, growth-model-canvas, north-star]
related: [M-product-metrics, M-success-metrics, M-goals-drivers-bets, M-business-models, M-traction-model, M-pmf-scaling, M-loyalty-metrics]
---

# Growth frameworks: AARRR, HEART, Flywheel, Growth Loops, Growth Model Canvas

## When to apply
"How will the product grow?", "which framework should we pick — a funnel or a loop?", "design a growth loop / viral cycle", "which metrics to measure at each stage". The choice of growth model is an individual recipe; the main thing is that the math adds up.

## Essence
**A linear funnel (AARRR, HEART):** requires continuously feeding the "top" with external investment in acquisition; at every stage users leave irreversibly.
**A growth loop (Flywheel, Growth Loop):** a closed cycle where the output of the cycle (an acquired user, created content) becomes the cause of acquiring new users in the next cycle — growth "from the inside".

| Product type | Recommended framework (not a hard rule) |
|---|---|
| E-commerce | AARRR |
| SaaS | journey funnel + HEART |
| Games | Growth Loop |
| Social networks | Growth Loop + HEART |
| Media | Growth Loop + HEART |
Selection factors: product stage, business goals, market, product type.

### AARRR (Pirate Metrics), 6 stages in the skill's version
| Stage | Essence | Channels | Metrics |
|---|---|---|---|
| Awareness | people learn about you | SEO, SEM, content, affiliate, PR, social networks, newsletters, ASO | visits, reach, CTR, CPC, CPM, bounce, engagement |
| Acquisition | visitors are identified | blog, white papers, chat widgets, landing pages, webinars, retargeting, quizzes | subscriptions, downloads, Cost per Lead, trial signups |
| Activation | first great experience (the Aha moment) | UX, tutorials, support, onboarding, drip | core feature usage, onboarding success, CAC |
| Retention | users come back | email, push notifications, extra features, lifetime marketing | churn, DAU, MAU, returning customers |
| Revenue | behavior generates income | UX, sales, checkout | CLV, conversion, upsell/cross-sell, average order value, CLV/CAC |
| Referral | users bring new ones | referral mechanics, sharing, ratings, viral campaigns | invites, shares, viral coefficient, NPS |
Drawbacks: constant feeding of the top (expensive, limited scalability), irreversible leakage, no feedback loops.

### HEART (Google) — a UX quality framework
For each dimension: Goal → Signals → Metrics.
- Happiness — store ratings, in-app survey, Customer Effort Score.
- Engagement — DAU, actions per user, number of saved/favorited items.
- Adoption — download rate, Time to Value, onboarding completion.
- Retention — 30-/90-day retention, MAU, churn/uninstall.
- Task Success — task completion time, search success rate, error rate.

### Flywheel: Activate → Adopt → Adore → Advocate
| Stage | Segment | Strategy | Metric |
|---|---|---|---|
| Activate | evaluator | a simple path to the Aha moment, remove barriers | sign-up rate |
| Adopt | newcomer | habit formation, teaching new features | retention rate |
| Adore | regular user | improve the experience, anticipate needs | NPS |
| Advocate | champion | encourage recommending (starts a new cycle) | referrals invited |
Example (the "jobs" vertical of a classifieds board): positive loops — more resumes → more applications → more employers → more vacancies → more job seekers; negative (control) — fewer job seekers → more fraudsters.

### Growth Loop: design
The universal cycle: product growth → more and better resources (people and capital) → solving new meaningful problems → product growth.
- **Observe:** a real behavior scenario; motivation — to look good / to feel good / to help others / to get / to bond / to convince.
- **Design:** what motivates and how to reflect it in the product; which action we expect and how to simplify it; what result the user gets and how to amplify it.
- **Iterate:** the steps of the loop to track and a metric for each step.
Example: doctors share medical content → the product helps find supporting evidence → content with the author's photo and credentials is visible to others → they create their own → metrics: read/saved, shared, arrived via link, registrations with UTM.

### Growth Model Canvas
Target audience (persona) · Value Proposition · North Star Metric · WOW Moment · Product DNA (customers need it and are "hooked") · the 6 stages Awareness…Referral with metrics.

## Procedure
1. Describe the product, stage, growth goal, market; define the NSM ([[M-product-metrics]]).
2. Use the table to pick 1–2 candidates; justify in writing why the others were not chosen.
3. **Verify the math of the chosen model:**
   - funnel: `Result = Input × CR1 × CR2 × …`, channel economics — `LTV > CAC`, payback ([[M-unit-economics]]);
   - loop (the standard formula, not from the skill): loop coefficient `K = i × c` (invitations/created content per user × conversion of invitees into new users); with `K < 1` and a constant external inflow P, the steady-state total is `P / (1 − K)`; with `K ≥ 1` growth is self-sustaining, in practice capped by saturation; cycle time and the quality of new users matter.
4. Design the loop via Observe → Design → Iterate; write down: trigger → action → result → input of the next cycle; leaks and negative loops.
5. Assign a metric to every step and a way to measure it (events, UTM).
6. Fill in the Growth Model Canvas; connect it to the traction model: the loop is the virality driver, the funnel is the acquisition/activation/retention driver ([[M-traction-model]]).
7. Control metrics for every stage + health counter-metrics.

## Template / checklist
Loop:
| Step | What the user does | Motivation | Result | Step metric | Conversion |
|---|---|---|---|---|---|
| 1 | | | | | |
| … | | | | | |
| Cycle output → input of the next | | | | K, cycle time | |
Output artifact: the choice and its justification; a funnel or a loop with metrics; channels by stage; Growth Loop; Canvas; control metrics.

## Typical mistakes
- Copying a framework "as the market leader does" without checking the math.
- Treating HEART (UX quality) as an acquisition model, and AARRR as a quality model.
- Drawing a loop without measurable steps and conversions.
- Ignoring negative loops (fraudsters, abusers, spam).
- Optimizing Referral while Activation/Retention is weak.
- Relying on "virality" without calculating K and cycle time.

## Questions that can change the decision
- Where do >70% of new users come from today (channel) and does it scale ([[M-pmf-scaling]])?
- Is there a natural result of usage visible to others (content, invitation)?
- Do at least some users retain (the curve flattens out)? If not, a loop will amplify the leak.
- What is the cost of one unit of external inflow P in the funnel?
- What is the Aha moment and how many users reach it?

## Related maps
[[M-product-metrics]], [[M-success-metrics]], [[M-goals-drivers-bets]], [[M-business-models]], [[M-traction-model]], [[M-pmf-scaling]], [[M-loyalty-metrics]], [[M-unit-economics]]
