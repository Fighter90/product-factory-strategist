---
id: M-landscapes
lang: en
title: Adjacent landscapes — marketing, technology, business model and business functions
course: strategy
sources: ["EN mirror of the RU methodology card M-landscapes (knowledge/methods/landscapes.md); original sources are listed in the RU card"]
stages: [research, options, strategy, validation]
tags: [business-model, marketing, technology, sales, three-lenses, desirability, feasibility, viability, investment-committee, asset-light, landscape]
related: [M-strategy-growth, M-monetization, M-unit-economics, M-goals-drivers-bets, M-risks, M-team, M-outcome-roadmap, M-usp, M-product-communication]
---

# Adjacent landscapes — marketing, technology, business model and business functions

## When to apply
When a product growth strategy must survive the question "and together with the rest of the business?": can the product actually be built and delivered (technology, marketing, sales), does it make money (business model) and does the customer need it. The map helps to complement product bets with a picture of the internal environment, choose or revise the business model and prepare the case for the investment committee.

## Essence
**The product is a value-creation mechanism, but the business is a system of functions.** Value must be delivered, monetized and repeated (retention/expansion). Functions:
| Function | Purpose | How it affects the product | What it gives the product |
|---|---|---|---|
| Product / Tech | feasibility, speed, quality, security, scaling | architecture, tech debt and platforms constrain or accelerate; they determine the cost of development and operational risks | data, experiments, stability of value delivery |
| Marketing | create demand and the right expectations, bring in the "right customer" at an acceptable price | packaging: message, pricing tiers, segmentation | signals about the market, JTBD, comparison with competitors, channel quality |
| Sales | turn demand into contracts and predictable revenue | walks the customer through a complex decision (why change, why us, why now) | signals about barriers, decision-maker requirements |
| Support / success | deliver the promised value, retain | response to complaints, procedures | feedback, retention |
| Finance / operations | business sustainability | budget, unit economics | guardrails for decisions |

**The three lenses of innovation** — an initiative succeeds only if, simultaneously: it is desirable for the user (desirability), feasible technologically and operationally (feasibility), and viable for the business (viability).
| Lens | Questions |
|---|---|
| Desirability | who is the primary user, for which segments is the value maximal; which need do we serve; what makes people come back |
| Feasibility | is there expertise and who are the key people; is there enough capacity; which external systems do we depend on |
| Viability | who pays, for what and when; what are the fixed and variable costs and does the economics add up; which customers are the most profitable and are we attracting exactly them; why now |

**Marketing**: four areas — performance (measurable acquisition; CPA, CPC, ROAS; days–weeks), brand (awareness and trust; months–years), product marketing (positioning, launch), growth (experiments: referrals, SEO, A/B). Funnel: awareness → interest → consideration → conversion → retention → referral. Acquisition metrics: CPA = spend / target actions; CPC = spend / clicks; CPM = spend / (impressions / 1000); ROAS = revenue from advertising / advertising spend; CAC = (marketing + sales) / new customers in the period; K-factor = invitations per user × invitation conversion. Marketing is not advertising, but a system for shaping demand and meaning.

**Sales**: three questions — why the customer should change (the risk of "doing nothing"), why with us (the value proposition and an ROI model per customer), why now (the decision-maker, the budget cycle, approvals). Types: self-service (minutes, low CAC), inside sales (days/weeks), field sales (months, high CAC), channel sales (through partners). The translation "feature → benefit → outcome" (a dashboard → visibility of metrics → faster decisions).

**Tech**: roles — development, QA, analytics, design, technical lead; rules of engagement: discuss the "why", not the "how", respect estimates, involve engineers in discovery early, budget for tech debt, align the roadmap and priorities.

**Business model** — the mechanism by which the company makes money: who pays, for what, and how the price is formed. It is not the type of business (a marketplace, SaaS — are types). A large business is always a set of models. Choosing or switching the model can be the main driver of growth.
| Model | When applicable | How it makes money (formula, unit and period) | Examples |
|---|---|---|---|
| Retail | physical goods, logistics | margin = selling price − purchase price, ₽/unit | M.Video, Magnit |
| Subscription | recurring value, recurring costs | revenue per period = subscribers × ARPU; MRR/ARR; condition LTV > CAC | Yandex Plus, SaaS |
| Freemium | low marginal cost, scale needed, product-led | revenue = free users × conversion to paying × paying ARPU | VK Music, Telegram Premium |
| Pay-per-use | high variability of consumption, high variable cost | revenue = price per unit × consumption volume | clouds, APIs, carsharing |
| Advertising | large traffic and engagement | CPM/CPC/CPA: revenue = impressions × CPM / 1000 × fill rate | search engines, social networks |
| Commission | intermediation, an expensive deal | revenue = GMV × take rate | realtors, brokers, taxi aggregators |
| Revenue share | the service is delivered by a partner, the platform brings the customer | platform revenue = total revenue × platform share | app stores, financial products at partners |
Others: white label, licensing, franchising, "razor and blades", data monetization, retainer. A classifieds listings business as asset-light (does not own physical goods) uses almost all models except retail; classifieds have two basic schemes — payment for a listing and payment for the result (a buyer/a deal). Signals for revising the model (from the lecture notes): falling LTV/CAC, rising churn with a stable product, a competitor growing faster with a different model, an unserved segment appears, an opportunity to control the transaction appears (a commission can be added), "free" users create costs.

**Subscription — metrics and the main risk.** MRR decomposes into components: New + Expansion − Churned − Contraction (it shows the source of growth: acquisition or expansion among existing customers); alongside it ARR, Churn, LTV, CAC, ARPU, Payback. Subscription types: fixed, tiered, usage-based, all-you-can-eat. The main risk is churn: at 5% monthly churn more than half of the base is lost within a year, so a subscription is justified only with a long-term need and recurring value.

**Freemium — the free-to-paid conversion multiplier is key.** Benchmarks: SaaS ~2–5%, games ~1–5%, highly engaging products ~10–15%. Freemium is the main instrument of product-led growth: the free tier must create value by itself (a collection, a network), while the paid tier removes a constraint. Risk: a generous free tier "feeds" users who will never pay but do create costs.

**Commission model — the economics in one chain** (figures are illustrative): `active sellers (10,000) × transactions per seller/month (5) × average order value (3,000 ₽) = 50,000 transactions/month`; `GMV = transactions × order value = 150M ₽/month`; `revenue = GMV × take rate (8%) = 12M ₽/month`; `minus COGS per transaction (payments + delivery) = gross profit`; margin shows what growth comes from: raise the take rate (the risk of sellers leaving and disintermediation), reduce COGS (logistics, payments) or raise the order value (recommendations, cross-sell). Marketplace liquidity = `completed deals / published listings` — the basic metric of "does the market add up". Two structural risks: **disintermediation** (the parties agree directly, bypassing the platform — the commission bypasses it too) and **chicken-and-egg** (buyers need sellers, sellers need buyers; launching a two-sided market requires concentrating on one side). Comparison with revenue share: commission — a % of the deal (one side pays, the platform is an intermediary, benchmark 5–30% of GMV); revenue share — a % of total revenue (both sides are partners, benchmark 30–70%, examples: App Store 70/30, video platforms 55/45). The take rate grows with the added value of the deal: classifieds ~3–10%, e-commerce marketplaces ~10–25% (logistics, fulfilment), services ~10–20% (verification, guarantees), delivery and taxi ~20–35% (logistics, payments, traffic), hotels ~15–25% (global traffic), app distribution ~15–30% (monopoly on the channel).

**Investment committee** — a formalized "internal pitch": resources are always limited, there are more ideas than hands. The defence structure: the problem (for whom and how big), the solution, metrics and deadline, resources, risks, alternatives (including "what happens if we don't do it" and a cheaper option). Prioritization: ICE, RICE (Reach × Impact × Confidence / Effort), MoSCoW, the Value/Effort matrix.

## Procedure
1. **Run the chosen bet through the three lenses**; for each lens question, give an answer with the type of data (fact / assumption / gap).
2. **Describe the current and the target business model**: who pays, for what, the revenue formula, unit and period, unit economics (`M-unit-economics`). If the bet changes the model (e.g., from classifieds to transactional), assess the impact on each side of the market and write out the risks.
3. **Check model compatibility** (subscription and advertising can conflict, freemium and commission require caution): do the revenue sources cannibalize each other.
4. **Describe the marketing landscape**: channels, CAC by channel, the role of brand, dependence on paid traffic, season windows.
5. **Describe the technology landscape**: platforms and data to lean on; dependencies on other teams; tech debt; constraints on the speed of testing hypotheses.
6. **Describe the business landscape**: legal and financial guardrails, partners, the role of sales and support.
7. **Assemble the conclusion**: which functions become the bottleneck of the bet and what must be done before the start.
8. **Prepare the committee pitch** in six sections and prioritize the portfolio (ICE/RICE or Value/Effort), stating what is deferred.

## Template / checklist
**The bet's landscape map**
| Landscape | What exists | Bottleneck | Dependency / owner | What to do before the start |
|---|---|---|---|---|
| Marketing | | | | |
| Technology | | | | |
| Sales / support | | | | |
| Business model and finance | | | | |
| Legal / compliance | | | | |

**The committee pitch** (six blocks): problem — solution — metrics and deadline — resources — risks — alternatives. Numbers and sources in every block.

**Checklist**
- [ ] The bet passes the three lenses; the weak lens is named
- [ ] The business model is described by a formula with units and a period
- [ ] Shown who pays and when
- [ ] Dependencies on Tech, marketing, sales and support are stated with owners
- [ ] The alternatives include "do nothing" and a cheaper validation

## Typical mistakes
- "The product is everything": it is ignored that the business rests on the cost structure, resources, partners, distribution and the monetization model.
- Marketing treated as advertising; sales as a "call department".
- One model for everything: the business model does not match customer behaviour.
- Skipping a lens: desirable but infeasible or unprofitable; feasible but needed by no one.
- No answer to "why now".
- Planning on development estimates without buffer and without dependencies.
- A pitch without alternatives and risks.

## Questions that can change the decision
- If the bet changes the business model, do we lose a revenue source that feeds the current business?
- Which lens is the weakest, and can it be strengthened with a cheap validation?
- Does the competitor have a different business model that gives it a structural advantage (costs, distribution)?
- Which functions (legal, support, moderation) cannot be connected quickly, and how much would that shift the timeline?
- Who pays and when: does the moment of payment coincide with the moment of receiving value?
- What happens if the committee says no: what does the minimal option look like?

## Related maps
[[M-strategy-growth]], [[M-monetization]], [[M-unit-economics]], [[M-goals-drivers-bets]], [[M-risks]], [[M-team]], [[M-outcome-roadmap]], [[M-usp]], [[M-product-communication]]
