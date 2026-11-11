---
id: M-team
lang: en
title: Team and people — composition by stage, hiring, org structure, stakeholders and neighboring teams
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [strategy, validation, after-decision]
tags: [team, hiring, outsourcing, stakeholders, org-structure, two-pizza-team, gates, neighboring-teams, budget-cycle, timelines]
related: [M-strategy-growth, M-outcome-roadmap, M-risks, M-landscapes, M-traction-model, M-decision-daci, M-pmf-scaling, M-mvp-pilots]
---

# Team and people — composition by stage, hiring, org structure, stakeholders and neighboring teams

## When to apply
When the strategy is ready "on paper" and you need to check who will build it, and in what time. The "Team and resources" block of the final work requires: assuming the team composition and the distribution of the work, and — given the size of the organization and the stage of the product — drawing up the list of stakeholders you need to reach agreements with. Even with AI advancing, launching something new without people is still hard: a model without people is a fantasy.

## Core idea
**The stage of the company defines the team structure.**
| Parameter | Startup (0→1, PMF search) | Scale (1→10) | Platform / ecosystem (10→100) |
|---|---|---|---|
| Focus | speed, insight | reproducibility, unit economics | structure, governance, platform thinking, AI |
| Composition | founder-PM, full-stack engineer, growth generalist, "light" analytics; 5–8 people (another source says 3–7), T-shaped skills | head of growth, performance marketing, product teams, data/BI, financial controller | CPO/CPTO, platform team, data science, international operations, legal/compliance |
| Decision speed | instant | days | weeks–months |
| Role of finance and lawyers | minimal | growing | critical (investment cases, approvals) |
| Examples | Airbnb 2009: the founders photographed listings themselves, ran support, grew | Uber: city operations teams + a central product team | Mercado Libre: marketplace + fintech as a separate growth engine |
Signs of scale readiness: PMF confirmed (retention is stable), unit economics positive or the path to it is visible, a reproducible acquisition channel exists, the team is "suffocating", data exists. At the scale stage — a transition from "heroes" to a system.

**The minimal startup team and what happens without each role** (the role map from the course practice):
| Role | What it does | What happens without it | Can AI replace it |
|---|---|---|---|
| Founder/PM | decisions, strategy, priorities | no steering wheel — chaotic motion | no |
| Full-stack engineer | prototype, MVP | no product | partially (vibe coding) |
| Growth generalist | GTM, channels, first users | the product is invisible to the market | no |
| "Light" analyst | MAU, retention, conversion | decisions made blind | partially (AI dashboards) |
The rule of practice: every role seems optional until it is needed (a lawyer is needed for licenses, a marketer for entering the market, a CTO for scaling). At the startup stage, the go-to-market role is forgotten most often: a product without a channel does not exist.

**The boundaries of vibe coding / AI development**: it is sufficient for internal tools (an audience of 10–100 people, limited liability, days to build) and insufficient for external user-facing services, where data, UX, anti-fraud, legal requirements and support are mandatory. The question for the team map is not "can AI write code" but "who carries responsibility toward the external user".

Two paradigms: Netflix — density of strong performers and a minimum of bureaucracy; Amazon — "two-pizza teams" (6–8 people) with full ownership and P&L.

**Org structures**
| Structure | Plus | Risk |
|---|---|---|
| Functional | effective at an early stage, fast decisions | many requesters, every idea is "the most important", resources get switched around |
| Product | P&L ownership, autonomy | duplication between departments, competition for resources |
| Matrix | strong expertise | dual subordination, a priority conflict (the business says "capture the market" vs the product says "fit into the strategy") |

**Learn the rules of the game.** In any company, find out: who the main stakeholders are (without whose approval or review the project goes no further); who manages priorities on a shared resource; whom to bring ideas to; who the "neighbors" are — those doing something similar or competing for a stretch of the journey/budget; whom not to forget to ask (lawyers, support, moderation); who will give feedback. Decision cultures differ widely: PROFI.RU 2013 — decisions rest with the co-founder/CTO; Yandex.Market 2021 — development is managed by project managers; a large marketplace 2025 — teams propose initiatives, resources are distributed through reprioritization and agreements with adjacent teams at the quarterly level; a startup 2026 — developers do not write code, they create agents. Launches shift by anywhere from one week to a quarter because of invisible blockers.

**Hiring is a hidden variable.** Traction is often drawn as if the team were complete from day one; in reality there is "work that nobody can do yet". Put the hiring timelines into the traction model: for example, a team growing 2 → 3 → 4 → 6 people delivers 50% → 70% → 85% → 100% of the target pace month by month (an illustration, not a norm). Options under a deficit: wait for the hire (slow, but quality), outsource (faster by 1–2 months of tender, harder to manage), vibe coding/AI for simple tasks, redistribution of resources (conflict-prone).
| Criterion | Hiring | Outsourcing |
|---|---|---|
| Speed | 3–6 months | 1–2 months (tender + contract) |
| Cost | higher cost of maintaining staff | lower at the start, higher in the long run |
| Quality / control | high | medium |
| Flexibility | low | high |
The timing benchmarks in the course are not SLAs. Team growth must go together with revenue/metrics: an inflated headcount without results is a red flag for financial control.

**Launch gates in a corporation**: investment case → legal/compliance → stakeholders → budget → launch. Each one takes anywhere from days to months. Budget windows: in the course example, requests are possible only in specific months of the cycle (4, 7 and 11); other companies differ — learn the calendar on the ground.

**The hidden costs of neighboring teams**
| Team | What is needed | Timeline (benchmark) | If forgotten |
|---|---|---|---|
| Support | procedures, training, FAQ | 2–4 weeks | rising ticket volume, falling CSAT |
| Moderation | rules, ML models | 1–3 months | fraud, complaints |
| Marketing | budget, channels | planned 3–6 months ahead | no traffic to the MVP |
| Partners (supply) | onboarding, integration | 1–6 months | no supply |
| Finance | budget in a cycle window | per the calendar | no money |
| IT infrastructure | servers, load capacity | 2–4 weeks | an outage |
Traffic inside a super-app (placement on the main screen) is a separate resource; without it the service is invisible.

**The formula for a realistic timeline**: Realistic timeline = T_development + T_hiring (3–6 mo.) + T_approvals (2–8 wk.) + T_neighbors (2–4 wk.) + T_buffer (20–30%). A conditional launch template: discovery (2 wk.) → team and resources (4–8 wk.) → approvals (in parallel, 2–6 wk.) → preparing the neighbors (in parallel with development, 2–4 wk.) → soft launch and full launch (2–4 wk.): 10–22 weeks in total + a 20% buffer. This illustrates the logic; it is not a set of norms.

## Procedure
1. **Determine the stage of the product and the company**, the org structure and the decision-making culture.
2. **Describe the target team** for each bet: roles, FTE, who is in place now, who is missing; the guideline is a team of 6–8 people owning its metric.
3. **For each missing role, choose a path**: hire / outsource / AI tools / redistribution; estimate the timeline and the impact on traction and phases (`M-outcome-roadmap`). Build two scenarios: "hired" and "not hired".
4. **Build the stakeholder map**: who, goals (OKR/KPI), influence (high/medium/low), attitude toward the project, action; priority for high influence: a personal meeting, verifying that the project does not conflict with their KPIs; for those competing for the resource — look for a win-win; update quarterly.
5. **Check the gates** (investment case, legal, compliance, budget, traffic placement) and the budget calendar; put them on the timeline.
6. **Prepare the neighboring teams**: support, moderation, marketing, partners, finance, infrastructure — owner, deadline, status.
7. **Compute the realistic timeline** using the formula and compare it with the desired one; if it does not converge — change the scope, the phase or the expectations, not "speed up hiring".
8. **Fix the agreements** (DACI + the table from `M-risks`) and the risks of a human and organizational nature.

## Template / checklist
**Team and resources**
| Role | FTE needed | In place now | How to close the gap | Deadline | Impact on phase/traction | Alternative |
|---|---|---|---|---|---|---|

**Stakeholder map**
| Stakeholder | Role | Goals (OKR/KPI) | Influence | Attitude | What they need to get | Action and deadline |
|---|---|---|---|---|---|---|

**Checklist**
- [ ] The stage and the org structure are defined
- [ ] The team composition matches the stage and the size of the bet
- [ ] Hiring and onboarding are built into the timelines and the traction model
- [ ] Every missing role has an alternative scenario
- [ ] The stakeholder map is drawn up in the first week and kept updated
- [ ] The gates and the budget windows are on the timeline
- [ ] Preparing the neighboring teams has owners
- [ ] The timelines include a 20–30% buffer

## Typical mistakes
- A traction model with a full team from day one; "freeze everything until the hire" or "plan as if everyone were already hired".
- Hiring before PMF and inflating headcount with no revenue.
- A hidden blocker: lawyers, support, moderation and the traffic owner were never consulted.
- Underestimating the outsourcing tender (1–2 months) and the dependencies on shared resources (a designer, an architect).
- Applying one company's experience to another without learning the rules of the game.
- Spoiling relationships in a fight over resources: people remember the tone, not the content.
- Ignoring the dual-subordination conflict in a matrix.
- At scale: inflating headcount with no link to metrics (financial control will ask "why" — every role must justify its contribution), keeping the "startup" process undocumented (duplication, conflicts), not investing in data/BI before scaling (decisions made blind).
- At the platform stage: starting a launch without a duplication check against existing functionality — the governance gate will send the project back to the start.

## Questions that can change the decision
- Is there a budget and an approved headcount, or will everything have to be fought for in the next window?
- Which roles can be covered by AI tools or outsourcing without losing quality or accountability?
- Who in the company can block the launch, and what are their goals?
- What stage is the product at — are platform-level gates needed, or is startup speed enough?
- What happens to the bet if a key person does not start on time (a smaller scope, a shifted phase)?
- Which neighboring teams are overloaded and may fail to get ready in time?

## Related maps
[[M-strategy-growth]], [[M-outcome-roadmap]], [[M-risks]], [[M-landscapes]], [[M-traction-model]], [[M-decision-daci]], [[M-pmf-scaling]], [[M-mvp-pilots]]
