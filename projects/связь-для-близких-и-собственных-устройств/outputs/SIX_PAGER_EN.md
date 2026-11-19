# Connection for loved ones and personal devices: six-pager

> Six-pager for a decision committee. The market and every figure are training numbers from the leader's brief[^1]; the full evidence chain lives in REPORT.md. Assumptions are labeled as assumptions and hypotheses as hypotheses; interviews with AI respondents are sources of hypotheses only, not proof. Scenario calculations: analysis/economics.py; Excel appendices: the Appendices section below.

**Request:** Your team runs the services of a fictional mobile operator. Some customers help loved ones with their connectivity. Others manage several of their own numbers. Decide who to help first, what exactly to change, and why the operator should invest money in it. Prepare a plan for the next year and set a benchmark for the end of year three. The leader faces two decisions: by the end of Q1 — whether to commit people and money to a pilot; by the end of Q2 — whether to expand coverage, change the offer, or keep observing.

## FAQ-1. Current state analysis

### 1.1 Market overview: trends, challenges and opportunities

The market is a training construct; its size is fixed by the brief: 300,000 households and 180,000 owners of several personal numbers need help with connectivity [C004]. Given the operator's current plans and its own acquisition channels, 100,000 households and 40,000 owners are reachable [C004]. The family-group base at the end of the base year: 6,500 enrolled and 4,000 active groups [C001]. Profit dynamics: the base-year plan is RUB 282M against a RUB 275M estimate [C001]; the plan-year "no change" forecast is RUB 279M; the target is at least RUB 285M [C002]. The gap the product must close is RUB 6M — that is, 12,000 additional paid months at RUB 500 of gross profit per number-month [C003].

Forecast by year:

- **Base year (estimate):** profit RUB 275M against a plan of RUB 282M; 4,000 active groups against a plan of 5,000; 14-day activation 42% [C001,S001].
- **Plan year, "no change":** RUB 279M; 8,000 enrolled groups; 5,000 active; 1,000 owners of several numbers; 45% activation [C002].
- **Plan year, target (at least):** RUB 285M; 12,000 enrolled groups; 8,000 active; 2,000 owners; 60% activation [C002].
- **End of year three (benchmark):** at least 25,000 family groups — 25% of the reachable base of 100,000 households — provided retention is confirmed in the pilot and expansion follows in years two and three [C004].

Key trends and what they mean for the product:

- **Family sharing is already built into the plans.** Groups with a shared package and data transfer from the leftover balance work today [C005]. Implication: build the service on ready mechanics, not on a new tariff product.
- **The operator holds the data but sends no timely signal.** Balances and payments are visible to the operator, yet the organizer learns about an outage from a plea for help [C005,C006]. Implication: informing closes the gap; a dashboard redesign does not.
- **Device owners are the second customer group.** The market holds 180,000 owners and 40,000 are reachable; switching between numbers already works in the dashboard, but the owner does not notice when money or data runs out [C004,C006]. Implication: a second wave that carries over proven mechanics [C016].
- **Money comes from activity, not enrollment.** The target requires two-thirds of enrolled groups (66.7%) to take the first action, against 62.5% under "no change" [C008]. Implication: the service must create the reason for the first action itself.
- **Unexplained charges drift into support.** By hypothesis, they are a separate driver of support contacts [C019][^2]. Implication: the charge breakdown belongs inside the alert, not inside a help article.
- **Trust is the price of access to family data.** Rights are split: the member consents, may revoke at any time, and the payer confirms payments [C009]. Implication: granular consents are the entry ticket to this market, not a setting.
- **A paid option will not fly.** Owners' stated willingness to pay is low — RUB 30–50 per month by hypothesis [C020][^3]. Implication: the service ships free within the plan; monetization runs through retention [C003].

Honest data gaps: the mix of outage causes is taken as an assumption of ~50% quota exhaustion / ~30% missed payment / ~20% unexplained charges, and is verified from pilot records [C011]; a specific customer's history can only be reconstructed from operator records during the pilot [C005]; an enrollment pace of ≥100 newly eligible groups per week is an assumption [C012]; the price and composition of a paid option are not set — the decision boundary recalculates at any price via the brief's formula [C003]; consent conversion is a synthetic hypothesis [C019].

### 1.2 Key competitors: growth and promo mechanics

The training market has no operator brands to fight: the competition is the habitual ways customers already solve the job [S001]. The comparison follows the brief's groups of ways.

| | Bank auto-payment | Family chat | Dashboard and device app | Plan with package sharing |
|---|---|---|---|---|
| **Key advantages** | Pays on schedule by itself; familiar; covers non-payment [C020] | Zero cost; "ask a family member directly"; no consents needed [C005] | Everything in one place; switching between numbers already works [C006] | The "help" action is already in the plan: data transfer from the leftover balance [C005] |
| **Growth strategy and promo mechanics** | Banks promote auto-debits and reminders inside their own apps [S001] | Family habit: messages and calls at the moment of the problem [C005] | Self-service: the operator dashboard plus the device's own app [C006] | The operator promotes shared-package plans through its own channels [S001] |
| **Risks for the company** | Misses quota exhaustion and a blocked card; once auto-payment is on, a payment alert reads as noise — risk: Medium [C020,C026] | Learns about the outage only after it happens; today this is precisely the path to lost access — risk: Low [C005] | A dashboard on its own does not solve the moment of finding out; budget spent without a behavior change — risk: Medium [C005,C006] | The "just transfer GB for free" reaction instead of paying cannibalizes paid months — risk: High [C023] |

The growth mechanics in play are the competitor ways already implemented: payment automation at banks, the ask-a-loved-one habit, self-service dashboards, and the in-plan transfer action itself. What none of them offers: a timely proactive signal that connects the moment of risk with a one-step action. Auto-payment pays but does not see quota exhaustion; the chat finds out after the outage; the dashboard shows only if opened; the plan provides the action but not the moment. That is the strategy window: an alert before the outage, with a link to the ready action and granular consents [C005,C009,C017].

> **Conclusion (inference):** no group of ways covers "warn before the outage", while the operator already holds both the data and the mechanics [C005,C006]. The window is bounded by the plan year: without a launch, profit is pinned at RUB 279M and the RUB 285M target is missed [C002]. Therefore a pilot by the end of Q1 and an expansion decision by the end of Q2 [S001] is the minimum pace the window allows.

## FAQ-2. User Persona. Who is the target audience?

### 2.1 Segments

Segments are split by the entry barrier, not by profession. Each segment's job is stated as a job to be done (JTBD); the wording comes from the situation analysis [C005,C006,C009].

| | S1 · Family organizers | S2 · Members and payers | S3 · Owners of several numbers |
|---|---|---|---|
| **Who are they?** | Parents and adult children running a group with a shared package; the plan allows sharing [C005] | A family member with an allocated share; the payer may be neither the organizer nor the number's owner [C009] | A SIM in the phone plus a router or tablet; switching between numbers already works in the dashboard [C006] |
| **What do they use today and why?** | A plea for help and a data transfer from the leftover balance: the signal arrives late, but the action is familiar [C005] | Direct arrangements in chat; they do not hand over access to their own data [C009] | Auto-payment on the router number and the dashboard; they do not notice when money or data runs out [C006,C020] |
| **What difficulties do they face?** | Learns about an outage from a family member; the causes are quota exhaustion, a missed payment, or an unexplained charge [C005] | Fear of "surveillance"; consent to data visibility is the entry barrier [C009,C019] | Cannot see the device's state: battery level requires data from the device itself [C006] |
| **Common difficulties** | The moment of finding out: all three roles learn about the problem later than it happened; "what was this charge for" contacts pull in support [C005,C019] | Distrust of any operator access to family data [C009] | Expectations wider than the first iteration can deliver: battery level and "never think about the router" [C006,C020] |

Prioritization rationale (capacity / competition / acquisition cost):

- **Capacity:** S1 has a reachable base of 100,000 households versus 40,000 owners for S3 — 2.5× larger [C004].
- **Competition of ways:** for families, auto-payment covers only non-payment, and the dominant outage cause is quota exhaustion (assumed at 50% of cases [C011]); for owners, auto-payment already covers most cases [C020] — stronger competition, weaker information trigger.
- **Customer acquisition cost (CAC):** acquisition runs through the operator's own channels without paid advertising [S001]; the family journey and mechanics already work [C005]; the pilot needs about 2 of the 3 development man-months of Q2 [C010].
- **Therefore,** the first customer is S1; S3 follows in the second wave, Q3–Q4, with the mechanics carried over; S2 is not a separate target but the enabling condition: without the member's consents the S1 service cannot switch on [C016,C009].

### 2.2 Barriers at each journey stage

| Journey stage | Barrier today | What the product does |
|---|---|---|
| Acquisition | A cold offer lands wrong: the organizer does not open the dashboard unprompted and learns about an outage from a family member [C005] | Show the offer after the first "outage via plea for help" and at support contacts — at the moment of felt pain [S001] |
| Choice / usage | Distrust of access to a loved one's data: "this is surveillance" [C009,C019] | Three separate consents (balance / payments / pay on my behalf), revocable at any time; no messages and no location [C009,C022] |
| Payment | A missed payment; the right "the payer confirms the payment" conflicts with messaging the organizer [C009] | A reminder to the payer without the word "confirm"; idempotency: a second payment on the same number is blocked until the charge clears [C022,C026] |
| Post-payment experience | "Unexplained charges": the family cannot tell what the money was taken for [C005] | Inside the reminder: number, amount, date, purpose, and payment status; the charge history opens under a separate consent [C005,C009] |

What holds people back from starting or renewing?

| Segment | Blocking factor | How it is removed |
|---|---|---|
| S1 · Family organizers | "I'm fine as is"; fear of a notification flood | Free within the plan [C020]; a cap of ≤2 alerts per week and alert precision ≥80% [C026] |
| S2 · Members and payers | "This is surveillance of a loved one" | Only what the member allows is visible; revocable at any time; the invitation text states the rights outright [C009,C019] |
| S3 · Owners of several numbers | Expectation of device data (battery level) the operator does not hold [C006] | Number-level alerts without device integration; integration is a separate decision after the pilot [C020] |

> **Conclusion (inference):** segmentation follows the entry barrier: S1 — unawareness, S2 — distrust, S3 — fragmented device data. One product serves every barrier: the free alert removes S1's starting barrier, granular consents turn S2's barrier into an operating condition, and number-level alerts serve S3 until device integration lands. Priority follows the capacity, competition, and CAC calculation above; therefore S1 is the first customer, S2 the condition, and S3 the second wave.

## FAQ-3. Strategic initiatives. Justify each one briefly.

The direction was chosen from five meaningfully different options: A — keep as is; B — "alert before the outage"; C — "family dashboard"; D — device owners first; E — shut the line down. B was chosen: it uses data and mechanics that already exist [C005,C006], fits the Q2 budget (3 development man-months, plus 0.5 FTE (full-time equivalent) each for a designer and an analyst) [C010], and hits the recorded gap "the data exists — the alert does not". C was rejected: it does not solve the moment of finding out and needs ≥4–5 man-months, over budget [C010]. D was rejected for the first wave: its base is 2.5× smaller and auto-payment already covers most cases [C004,C020]. A and E remain defensible only if the leadership revises the targets [C002].

An independent red-team attack produced 20 hits (15 objections + 5 hidden assumptions) with the verdict "needs rework before the pilot"; every hit is built into the design as a check or a threshold [C021–C026]: incrementality, cannibalization, consent rights, forecast precision, and pilot power.

### First driver — the "Alert before the outage" service

Key directions: a low-balance trigger (~20% left, 3 days out) and an upcoming-payment trigger (3 days ahead, only for numbers without auto-payment) [C026]; a granular consent screen [C009,C022]; a one-step action from the message — data transfer from the leftover balance [C005].

Effect calculation: the decision boundary is the target of +RUB 6M, which requires 12,000 additional paid months × RUB 500 [C003]. The target scenario is derived from that boundary, not from a funnel: 5,500 numbers × 3 months = 16,500 months; 16,500 × RUB 500 = RUB 8.25M; RUB 8.25M − RUB 1.5M of direct costs = **+RUB 6.75M → RUB 285.8M** — the target is met with margin [C003].

Scenario bounds: a conservative case of 4,000 × 3 months = 12,000 months → +RUB 4.5M → RUB 283.5M — below target, prompting a Q2 decision to rework or pause expansion [C003]; an adverse case of 3,000 × 2 months = 6,000 months → +RUB 1.5M → RUB 280.5M [C003]. The red team's worst cases: "zero" −RUB 1.5M → RUB 277.5M; "minus" with churn −RUB 3.5M → RUB 275.5M — under the effect hypothesis [C013].

The strongest objection — "profit is not a direct effect: if retention does not grow, the contribution is zero". Answer: the pilot's primary metric is additional paid months per group, counted by intention-to-treat (ITT) — every enrolled group stays in the calculation, including non-responders [C025]. The expansion threshold is recorded before any data: an effect of ≥ −3 p.p. on exhaustion-driven cutoffs (12% → 9%), false alerts below 20%, and double charges = 0 [C013]. If paid months do not grow, there is no expansion and costs are cut [S001].

### Second driver — channel and moment of enrollment

Key directions: show the offer after the first "outage via plea for help" (a banner on the group card); offer it at support contacts — the moment of explicit pain; send the member a separate invitation that states the rights in plain words [C005,C019,C009].

Effect calculation: the pilot needs 600 groups over 6 weeks — a pace of ≥100 newly eligible groups per week (an assumption, verified in the first 2 weeks of enrollment) [C012,C018]. Scaling to 12,000 groups requires a consent rate — the share of enrolled groups with issued consents — of at least 70% [C024]. A show-to-enrollment conversion of ~35% is a funnel assumption [C011,C024].

The strongest objection — "the consents may not come: financial data is sensitive". Answer: the consent rate is the pilot's primary funnel: below 50% in the first 4 weeks — rework the invitation; below 30% — rework the mechanic and test option D in a small loop [C024,C019]. A consent revoked mid-pilot does not remove the group from the calculation [C024].

### Third driver — honest retention economics

Key directions: incrementality measured by payment dates against control with a 90-day cannibalization window; a separate reaction log of "transfer / pay / nothing"; contribution counted only on paid months; a seasonal adjustment when extrapolating the 600 pilot groups to scale [C021,C023,C025].

Effect calculation: if the share of shifted payments exceeds 30%, the effect is nullified and expansion is cancelled [C021]. GB transfers (zero revenue) stay out of the contribution [C023]. The target scenario's margin: 16,500 − 12,000 = 4,500 months (~27% above the required volume) absorbs adverse adjustments until they eat the effect itself [C003,C015].

The strongest objection — "600 groups cannot prove the effect for a 12,000 scale". Answer: pre-registration before launch: the primary metric, the minimum detectable effect (MDE), and power ≥80% at α=5%; if the MDE exceeds the expected effect, either enlarge the sample or honestly declare the pilot uninformative [C025]. Randomization is clustered by families; spillover is measured with control-group surveys [C025].

### Fourth driver — device owners in the second wave (Q3–Q4)

Key directions: carry the alert mechanics to owner numbers (a shorter path — no invitations needed) [C016]; a small loop inside the same pilot, randomized by owners [S001]; device integration (battery level) is a separate decision after the pilot [C006].

Effect calculation: the 40,000-owner base is 2.5× smaller than the family base; at equal retention the contribution shrinks proportionally [C004]. Five-line forecast: 1,200 owners by the end of the plan year versus 1,000 under "no change" [C002].

The strongest objection — "auto-payment already covers owners". Answer: it does not cover a blocked card and does not see quota exhaustion; willingness to pay is low (RUB 30–50 per month — a hypothesis), so the service is free within the plan and monetizes through retention [C020]. If family consents go poorly while owner interest runs high, D swaps places with B — the same small loop supplies the data [C024].

Five-line forecast:

| Metric | "No change" [C002] | Target scenario | Adverse case | Link to action and assumption |
|---|---|---|---|---|
| Gross profit, RUB M | 279 | 285.8 [C003] | 280.5 [C003] | target: 5,500 numbers × 3 months − RUB 1.5M direct; adverse: 3,000 × 2 months [C013] |
| Enrolled groups, year-end | 8,000 | 11,500 | 9,500 | in-app and support promotion plus fewer departures; assumption on the enrollment share of shows [C011] |
| Active groups, last month | 5,000 | 7,600 | 6,400 | the alert is the reason for the first action; share ~66% [C007,C008] |
| Owners of several numbers, year-end | 1,000 | 1,200 | 1,000 | second wave — Q3–Q4; until Q3 — no change [C016] |
| 14-day activation (last quarter) | 45% | 60% | 50% | the alert pushes the first action [C007] |

Gaps in the adverse case: profit RUB 2.5M short of target — expand only after the pilot effect is confirmed; 1,600 active groups short — activation work or a target revision by the leader [C002].

> **Conclusion (inference):** the four drivers close the FAQ-2 barriers: the moment of finding out is solved by the product itself (driver 1), distrust by the consent screen and the invitation (drivers 1–2), unexplained charges by the in-message charge breakdown, and weak evidence by driver 3. Every initiative builds on existing assets: balance and payment data [C005,C006] and the transfer mechanics [C005]; no new tariff product is required. This means the risk sits not in development but in customer behavior — precisely what the pilot tests.

## FAQ-4. Tactics. Detail each initiative into concrete tactics.

| Strategic initiative | Focus | User needs and expectations | Solutions (tactics) |
|---|---|---|---|
| Driver 1 · Balance trigger | Pre-empt quota exhaustion | Organizer: learn in advance that a loved one is running out of data, without polling the family [C005] | A "~20% left, 3 days out" rule; a message with a link to transfer data from the leftover balance [C005] |
| Driver 1 · Payment trigger | Pre-empt a suspension for non-payment | Payer: know the amount and date in advance; organizer: never pay for someone else without permission [C009,C019] | A reminder 3 days ahead, only for numbers without auto-payment, with a payment-status check at send time; the word "confirm" removed from the text [C022,C026] |
| Driver 1 · Access rights | The member's trust | Member: control exactly what is visible about their number [C009] | A screen of three separate consents (balance / payments / pay on my behalf), revocable at any time; alerts go to the member first, then escalate to the organizer [C009,C022] |
| Driver 2 · Offer moment | Acquisition without paid channels | Organizer: an offer at the moment of felt pain, not a cold pitch [S001] | Show after the first "outage via plea for help" (a banner on the group card) and at support contacts [C005,C019] |
| Driver 2 · Member invitation | Consent conversion | Member: understand what is being opened and how to revoke it [C019] | Invitation text stating the rights in plain words; consent rate measured over the first 4 weeks of the pilot; wording tested on the pilot group [C009,C024] |
| Driver 3 · Incrementality | Proof of contribution | Leader: the contribution must not be payments merely shifted forward [C021] | Payment dates compared against control with a 90-day cannibalization window; shifts >30% — the effect is nullified, expansion cancelled [C021] |
| Driver 3 · Reactions to the alert | Cannibalization guard | Family: choose — transfer, pay, or do nothing [C023] | A separate log of "transfer / pay / nothing"; contribution counted only on paid months [C023] |
| Driver 4 · Carry-over to owners | Second wave | Owner: a signal on the router number without device data [C006,C020] | A small loop in the pilot, randomized by owners; the Q3–Q4 decision follows the result [S001,C016] |
| Driver 4 · Expectation boundary | Honest promises | Owner: device state (battery level) — the operator holds no device data [C006] | Vendor integration is a separate decision after the pilot; not claimed in first-wave promises [C006,C020] |

## FAQ-5. High-level implementation plan

Expected distribution of the initiatives' contribution to the overall result (sums to 100%):

- 70% — Driver 1 "Alert before the outage": the only direct source of additional paid months; 16,500 months in the target scenario against 12,000 required [C003];
- 15% — Driver 2 "Channel and moment of enrollment": delivers reach — a consent rate ≥70% — without which driver 1's contribution is zero [C024];
- 10% — Driver 4 "Device owners": +200 owners over "no change" (1,200 versus 1,000 by year-end) [C002];
- 5% — Driver 3 "Honest retention economics": no direct monetary contribution, but it protects the whole result from a false expansion — the nullification rule at shifts >30% [C021].

Order of tactics: **high priority — Q1**: trigger rules, reminder templates, consent screen, payment idempotency, pilot pre-registration; about 2 of the 3 Q2 development man-months plus a 0.5 FTE analyst [C010,C022,C025,C026]. **Medium priority — Q2**: enroll 600 groups over 6 weeks, observe the last enrollees for up to 14 days, report to the leader: effect, retention, decision [C018,S001]. **Base priority — Q3–Q4**: carry the mechanics to device owners, revise the yearly targets against actual data [C016,C002].

Timing: the package data shows no pronounced seasonal peaks — an honest gap. Timing is tied to the billing cycle (recurring charges, for example on the 5th of the month — a standing trigger of "unexplained charges" [C005]) and to the leader's decisions: the pilot by the end of Q1, the report by the end of Q2 [S001]. A seasonal adjustment is mandatory when extrapolating the 600 groups to scale [C025].

Parallel tracks (off the main line): a usability check before the A/B — the same "help a loved one" task by the old and the new way: time, errors, who succeeded unaided [S001]; a support cost estimate before pilot start (the verification specialist is a separate leader decision) [C010]; invitation and consent-screen wording tested on the pilot group — synthetic hypotheses [C019]. There are no partnership tracks: no agreements with external brands exist and no paid advertising is used — only the operator's own contact points [S001].

**Decision D001** — Launch the "Alert before the outage" pilot (option B). Mid-course review 2027-04-30. Triggers: consent withdrawals >15% [C022]; double charges ≥1 [C026]; alert precision <80% [C026]; enrollment pace <50 groups/week for 2 consecutive weeks [C012]; payment shifts >30% (incrementality) [C021]. Owner — direction lead; grounds: [C013], [C016], [C017], [C003], [C015], [C018].

## FAQ-6. Success metrics. KPIs in two dimensions

KPIs — key performance indicators — are set in two dimensions: business (money and base) and product (activation, time to first value, churn, satisfaction). Each metric: baseline → target by the deadline → action threshold.

| Dimension | Metric | Baseline | Target by deadline | Action threshold |
|---|---|---|---|---|
| Business | Plan-year gross profit | RUB 279M ("no change") [C002] | ≥RUB 285M by the end of the plan year [C002] | actual <RUB 285M with a confirmed pilot effect — revise the target with the finance team [S001] |
| Business | Additional paid months | 0 — the service is not launched [C003] | ≥12,000 by year-end; target scenario 16,500 [C003] | <12,000 by year-end — cut coverage or costs [S001] |
| Business | Enrolled groups, year-end | 6,500 [C001] | 12,000 [C002] | <11,500 — audit the acquisition funnel and the consent rate [C024] |
| Business | Active groups (last month) | 4,000 [C001] | 8,000 [C002] | <7,600 — activation work or a target revision by the leader [C008] |
| Business | 14-day activation (last quarter) | 42–45% [C001,S001] | 60% [C002] | <50% (the adverse-case level) — rework group onboarding |
| Product | Exhaustion-driven cutoffs after a low-balance event | 12% [C013] | −3 p.p., to 9%, by the end of the pilot [C013] | an effect of −1 to −3 p.p. — extend observation; ≈0 — stop or change [S001] |
| Product | Consent rate of enrolled groups | not measured [C024] | ≥70% in the first 4 weeks of the pilot [C024] | <50% — rework the invitation; <30% — rework the mechanic [C024] |
| Product | Alert precision | not measured [C026] | ≥80% before any expansion [C026] | >20% false alerts — stop expansion [C026] |
| Product | Additional paid months per group (pilot primary metric) | not measured [C025] | ITT effect by the end of the pilot [C025] | MDE above the expected effect — enlarge the sample or declare the pilot uninformative [C025] |
| Product | Time to first value | not measured | share of groups with ≥1 fired alert per month — first measured in the pilot | no threshold until the first measurement — an honest gap |

The product dimension in the first cycle goes without a classic satisfaction survey: CSAT — customer satisfaction score — and NPS — net promoter score — are not measured in the pilot and have no baseline; both move to the post-pilot cycle. The nearest proxy is the count of "what was this charge for" contacts, which must fall [C019].

Counter-metrics — one per red-team hit, thresholds recorded before any data:

| Counter-metric (red-team hit) | Alarm threshold | Action |
|---|---|---|
| Consent withdrawals | >15% [C022] | stop metric: rework consent texts and mechanics before any expansion |
| Double charges | ≥1 confirmed case [C026] | stop the disputed operation, reconcile, fix before resuming [S001] |
| False alerts | >20% of fired alerts [C026] | retune thresholds; no expansion |
| Opt-outs | >10% of enrolled within 4 weeks | investigate causes; revise the frequency and tone of messages |
| Payment shifts (incrementality) | >30% in the 90-day window [C021] | effect nullified; expansion cancelled |
| Pilot enrollment pace | <50 groups/week for 2 consecutive weeks [C012] | narrow the verification question or extend enrollment |
| Outages after a data transfer | growth versus control [S001] | review balance rules; suspend the operation |
| "What was this charge for" contacts | no decline over 6 weeks [C019] | rework message wording; support cost estimate before launch [C010] |

> **Synthetic material — hypotheses, not proof:** [C019] and [C020] derive from interviews with AI respondents [S002], [S003] at evidence grade D. They do not prove demand or how widespread the need is; each hypothesis is verified on live groups in the A/B pilot.

## Sources (footnotes)

[^1]: **S001** — leader's material — brief "Connection for loved ones and personal devices" (training figures) — 2026-11-19 — sources/raw/brief.md — grade A.
[^2]: **S002** — synthetic AI respondent — interview, "family organizer" — 2026-11-19 — interviews/synthetic — grade D — hypotheses, not proof.
[^3]: **S003** — synthetic AI respondent — interview, "owner of several numbers" — 2026-11-19 — interviews/synthetic — grade D — hypotheses, not proof.

## Appendices (Excel)

> Appendices are built by `pfs calc all` into outputs/attachments/: unit_economics.xlsx, growth_model.xlsx, cohort_retention.xlsx, market_sizing.xlsx. Formulas recalculate on open (Excel / Numbers / LibreOffice); the input sheet inside each workbook carries RU labels — edit the values there.

| File | Sheets | What to edit |
|---|---|---|
| cohort_retention.xlsx | Input · Cohorts · Retention metrics | cohort sizes, retention curve |
| growth_model.xlsx | Input · 12-month model | MAU (monthly active users), growth, conversion, AOV (average order value), take rate |
| market_sizing.xlsx | Input · Funnel · PESTEL | PAM (potential addressable market), funnel shares, environment factors |
| unit_economics.xlsx | Input · Unit economics · LTV and CAC sensitivity | ARPU (average revenue per number), VC (variable costs), CAC (customer acquisition cost), churn |

Notation: LTV — customer lifetime value. Derived LTV/CAC ratios stay out of the strategy in this training model: the economics are computed as additional paid months × RUB 500 [C003].

> Formulas recalculate on open (Excel / Numbers / LibreOffice). Detailing per the spec: knowledge/templates/SIX_PAGER_PROMPT_EN.md. Full evidence version — REPORT.md.
