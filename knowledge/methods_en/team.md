---
id: M-team
lang: en
title: Team and people — composition by stage, hiring, org structure, stakeholders and neighboring teams
course: strategy
sources: ["EN mirror of the RU methodology card M-team (knowledge/methods/team.md); original sources are listed in the RU card"]
stages: [strategy, validation, after-decision]
tags: [team, hiring, outsourcing, stakeholders, org-structure, two-pizza-team, gates, neighboring-teams, budget-cycle, timelines]
related: [M-strategy-growth, M-outcome-roadmap, M-risks, M-landscapes, M-traction-model, M-decision-daci, M-pmf-scaling, M-mvp-pilots]
---

# Team and people — composition by stage, hiring, org structure, stakeholders and neighboring teams

## When to apply
When the strategy is ready "on paper" and you need to check who will build it and in what time. The "Team and resources" block of the final work requires: to assume the team composition and work distribution, and given the organization's size and the product's stage, compile a list of stakeholders with whom agreements are needed. Even with AI development, launching something new without people is still hard: a model without people is a fantasy.

## Essence
**The company's stage determines the team structure.**
| Parameter | Startup (0→1, searching for PMF) | Scale (1→10) | Platform / ecosystem (10→100) |
|---|---|---|---|
| Focus | speed, insight | reproducibility, unit economics | structure, governance, platform-ness, AI |
| Composition | founder-PM, full-stack engineer, growth generalist, "light" analytics; 5–8 people (another source says 3–7), T-shaped skills | head of growth, performance marketing, product teams, data/BI, financial controller | CPO/CPTO, platform team, data science, international operations, legal/compliance |
| Decision speed | instant | days | weeks–months |
| Role of finance and lawyers | minimal | growing | critical (investment cases, approvals) |
| Examples | Airbnb 2009: the founders photographed listings themselves, did support, grew | Uber: city operations teams + central product | Mercado Libre: marketplace + fintech as a separate growth engine |
Signs of readiness to scale: PMF confirmed (retention is stable), unit economics positive or a path is visible, a reproducible acquisition channel exists, the team is "suffocating", data exists. At the scale stage — the transition from "heroes" to a system.

**The minimal startup team and what happens without a role** (the role map from the course practice):
| Role | What it does | What happens without it | Can AI replace it |
|---|---|---|---|
| Founder/PM | decisions, strategy, priorities | no steering wheel — chaotic movement | no |
| Full-stack engineer | prototype, MVP | no product | partially (vibe coding) |
| Growth generalist | GTM, channels, first users | the product is invisible to the market | no |
| "Light" analyst | MAU, retention, conversion | decisions in the blind | partially (AI dashboards) |
Rule of practice: every role seems optional until it is needed (a lawyer is needed for licenses, a marketer for market entry, a CTO for scaling). At the startup stage, the go-to-market role is forgotten most often: a product without a channel does not exist.

**The limits of vibe coding / AI development**: sufficient for internal tools (an audience of 10–100 people, limited liability, days to build) and insufficient for external user-facing services, where data, UX, anti-fraud, legal requirements and support are mandatory. The question for the team map is not "can AI write code" but "who bears responsibility to the external user".

Two paradigms: Netflix — a high density of strong performers and minimal bureaucracy; Amazon — "two-pizza teams" (6–8 people) with full accountability and P&L.

**Org structures**
| Structure | Plus | Risk |
|---|---|---|
| Functional | effective at an early stage, fast decisions | many customers, all ideas "the most important", resource switching |
| Product-based | accountability for P&L, autonomy | duplication across departments, competition for resources |
| Matrix | strong expertise | dual reporting, priority conflicts (business "capture the market" vs product "fit the strategy") |

**Learn the rules of the game.** In any company, find out: who the key stakeholders are (without whose approval or review the project does not move forward); who manages priorities over a shared resource; to whom to bring ideas; who the "neighbors" are doing something similar or competing for a stretch of the journey/budget; whom not to forget to ask (lawyers, support, moderation); who will give feedback. Decision culture varies widely: PROFI.RU 2013 — decisions by the co-founder/CTO; Yandex.Market 2021 — development is run by project managers; a large marketplace 2025 — teams propose initiatives, resources are allocated via re-prioritization and agreements with adjacent teams at the quarter level; a startup 2026 — developers do not write code but create agents. Launches shift from one week to a quarter because of invisible blockers.

**Hiring is a hidden variable.** Traction is often drawn as if the team were complete from day one; in reality "there is no one to do the work yet". Build hiring timelines into the traction plan: for example, a team of 2 → 3 → 4 → 6 people yields 50% → 70% → 85% → 100% of the target pace by month (an illustration, not a norm). Options under scarcity: wait for hiring (slow, high quality), outsource (1–2 months faster than a tender, harder to manage), vibe coding/AI for simple tasks, resource reallocation (conflict-prone).
| Criterion | Hiring | Outsourcing |
|---|---|---|
| Speed | 3–6 months | 1–2 months (tender + contract) |
| Cost | higher due to payroll | lower at the start, higher in the long run |
| Quality / control | high | medium |
| Flexibility | low | high |
The course's timelines are not SLAs. Team growth must go together with revenue/metrics: inflated headcount without results is a red flag for financial control.

**Launch gates in a corporation**: investment case → legal/compliance → stakeholders → budget → launch. Each one takes days to months. Budget windows: in the course example requests are possible in specific months of the cycle (4, 7 and 11), other companies differ — learn the calendar on site.

**Hidden costs of neighboring teams**
| Team | What is needed | Timeline (benchmark) | If forgotten |
|---|---|---|---|
| Support | procedures, training, FAQ | 2–4 weeks | growth of tickets, falling CSAT |
| Moderation | rules, ML models | 1–3 months | fraud, complaints |
| Marketing | budget, channels | planning 3–6 months ahead | no traffic for the MVP |
| Partners (supply) | onboarding, integration | 1–6 months | no supply |
| Finance | budget within the cycle window | per calendar | no money |
| IT infrastructure | servers, load capacity | 2–4 weeks | outage |
Traffic inside a super-app (placement on the main screen) — a separate resource; without it the service is invisible.

**The realistic-timeline formula**: Real timeline = T_development + T_hiring (3–6 mo) + T_approvals (2–8 wk) + T_neighbors (2–4 wk) + T_buffer (20–30%). A tentative launch template: discovery (2 wk) → team and resources (4–8 wk) → approvals (in parallel, 2–6 wk) → preparing neighbors (in parallel with development, 2–4 wk) → soft launch and full launch (2–4 wk): in total 10–22 weeks + a 20% buffer. This is an illustration of the logic, not standards.

## Procedure
1. **Define the product and company stage**, the org structure and the decision-making culture.
2. **Describe the target team** for each bet: roles, FTE, who is already there, who is missing; a benchmark — a team of 6–8 people with ownership of a metric.
3. **For each missing role choose a path**: hiring / outsourcing / AI tools / reallocation; estimate the timeline and the impact on traction and phases (`M-outcome-roadmap`). Make two scenarios: "hired" and "not hired".
4. **Compile the stakeholder map**: who, goals (OKR/KPI), influence (high/medium/low), attitude to the project, action; priority — high influence: a personal meeting, a check that the project does not conflict with their KPIs; for competitors over a resource — look for a win-win; update once a quarter.
5. **Check the gates** (investment case, legal, compliance, budget, traffic placement) and the budget calendar; put them on the timeline.
6. **Prepare neighboring teams**: support, moderation, marketing, partners, finance, infrastructure — owner, timeline, status.
7. **Compute the real timeline** with the formula and compare with the desired one; if it does not fit — change the scope, the phase or the expectations, not "speed up hiring".
8. **Fix the agreements** (DACI + the table from `M-risks`) and the human and organizational risks.

## Template / checklist
**Team and resources**
| Role | FTE needed | Available now | Way to close | Timeline | Impact on phase/traction | Alternative |
|---|---|---|---|---|---|---|

**Stakeholder map**
| Stakeholder | Role | Goals (OKR/KPI) | Influence | Attitude | What needs to be obtained | Action and deadline |
|---|---|---|---|---|---|---|

**Checklist**
- [ ] Stage and org structure are defined
- [ ] Team composition matches the stage and the size of the bet
- [ ] Hiring and onboarding are embedded in the timelines and the traction plan
- [ ] Every missing role has an alternative scenario
- [ ] The stakeholder map is compiled in the first week and is updated
- [ ] Gates and budget windows are placed on the timeline
- [ ] Preparing neighboring teams has owners
- [ ] Timelines include a 20–30% buffer

## Typical mistakes
- Traction with a full team from day one; "freeze everything until hiring" or "plan as if everyone were already hired".
- Hiring before PMF and inflating headcount without revenue.
- A hidden blocker: lawyers, support, moderation, the owner of traffic were not consulted.
- Underestimating the outsourcing tender (1–2 months) and dependence on shared resources (a designer, an architect).
- Applying one company's experience to another without learning the rules of the game.
- Ruining relationships in a fight over resources: people remember the tone, not the content.
- Ignoring the dual-reporting conflict in a matrix.
- At scale: inflating headcount without a link to metrics (financial control will ask "why" — every role is justified by contribution), keeping a "startup" process without documentation (duplication, conflicts), not investing in data/BI before scaling (decisions in the blind).
- On a platform: starting a launch without checking for duplication with existing functionality — the governance gate will send the project back to the start.

## Questions that can change the decision
- Is there a budget and an approved headcount, or will everything have to be fought for in the nearest window?
- Which roles can be closed with AI tools or outsourcing without losing quality and accountability?
- Who in the company can block the launch, and what are their goals?
- What stage is the product at — are platform-level gates needed, or is startup speed enough?
- What happens to the bet if a key person does not start on time (scope reduction, phase shift)?
- Which neighboring teams are overloaded and may fail to prepare in time?

## Related cards
[[M-strategy-growth]], [[M-outcome-roadmap]], [[M-risks]], [[M-landscapes]], [[M-traction-model]], [[M-decision-daci]], [[M-pmf-scaling]], [[M-mvp-pilots]]
