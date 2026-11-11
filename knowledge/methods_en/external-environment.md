---
id: M-external-environment
lang: en
title: External environment analysis — market types, PESTEL, trend or hype, potential calculation
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [intake, research, options, strategy]
tags: [pestel, trends, hype, market-sizing, market-types, b2b, b2c, c2c, opportunities-threats]
related: [M-strategy-growth, M-customers, M-competitors, M-market-sizing, M-risks, M-source-criticism, M-research-types, M-traction-model]
---

# External environment analysis: market types, PESTEL, trend or hype, potential

## When to apply
Use when you need to understand the conditions in which the product will grow: which market we play on, which external forces will help or hinder, and whether the market is big enough for the growth goal. The output is the "current state analysis" section of the strategy: trends, challenges, opportunities and market size, with sources. The card separates **facts** (measured values with a source and a date), **forecasts** (someone else's estimate of the future) and the agent's **hypotheses about impact** on the product.

## Core idea
A **market** is all potential customers of the product. The market type determines the approach to acquisition and monetization:

| Type | Essence | What it changes for the strategy |
|---|---|---|
| B2C | the value goes to the end consumer | mass acquisition; product- or marketing-led |
| B2B | a product for an organization; there is often a sales function | the client is specific decision-making people; sales-led |
| B2E | a B2B subtype for large clients with customization | few clients, large deals, consulting and implementation; measure the market in money and contracts |
| B2G | the client is the state, usually through procurement | a social function, tenders, legal requirements |
| C2C | users create value for each other; an intermediary is needed (a classifieds platform) | two sides, liquidity, trust |
| B2B2C | a business works with small businesses for the sake of end consumers | marketplaces: supply and demand have to be grown together |

**PESTEL** — six areas of external factors; collect only what affects *this* product (an unemployment service does not need real-estate trends).

| Area | What we look at | Example of impact on the product |
|---|---|---|
| Political | alliances and conflicts, sanctions, borders, visas, taxes, subsidies, elections | flight-ticket service: borders and visas; marketplace: countries' trade relations; messenger: the emergence of a state messenger |
| Economic | growth, inflation, exchange rates, interest rates and credit availability, unemployment, purchasing power | real-estate search: mortgages; marketplace: purchasing power; freelance exchange: unemployment |
| Social | demographics, lifestyle, education, migration, inclusion | real estate: the birth rate; marketplace: lifestyle changes |
| Technological | new technologies, automation, protocols, cybersecurity, R&D | marketplace: LLMs in ranking and hyper-personalization; freelance: automation of self-employment |
| Environmental | climate, recycling, carbon footprint, environmental policy | marketplace: the eco-friendliness trend |
| Legal | data protection, labor, intellectual property, consumer rights, platform regulation | marketplace: platform-economy law; messenger: storing correspondence |

**Concrete "factor → product" links** (for calibrating the search): the central bank's key rate hits high-ticket goods (real estate, cars, premium products) — the higher the ticket, the stronger the dependence on the cost of money; unemployment drives demand for job boards (the lowest unemployment in ten years means a growing business can become a non-growing one); the shift to the stories-based model of content consumption affects social networks and promotion; the appearance of a simple tax tool (like "My Tax") legalizes the "gray" segment and feeds it into freelance exchanges; patent blocking can freeze a release for years (the browser-tabs lawsuit ran for about 1.5 years); turnover-based fines for personal-data leaks are a direct financial risk for services holding user profiles; climate affects things non-obviously: a warm winter cuts demand for dachas in warm regions but lengthens the courier season. Regulatory factors often have an effective date — write it into the registry explicitly.

**Working format of the PESTLE registry** (as in the course's worksheets): the document header — the product, the research goal, the date and the assessment horizon (for example, 5 years), and the research summary (the conclusion: are there more opportunities or threats, and which factors are the main ones). Then a table sorted by descending significance:

| Group (P/E/S/T/E/L) | Factor (a formulation with a number) | Opportunity / threat | Impact 1–10 | Probability 1–10 | Significance = Impact × Probability | Decision (a specific product action) | Source link |
|---|---|---|---|---|---|---|---|

How it differs from a "list of trends": each factor has a numeric formulation ("85% of tourists book independently", not "people increasingly book online"), a link and, most importantly, a decision — otherwise the factor never made it into the strategy. The research summary is a mandatory block: "opportunities prevail (5 of the 7 top factors), the main drivers are …, the main threats are …".

**Any trend can be both a threat and an opportunity**: falling purchasing power is a threat to a marketplace, but also an opportunity to bet on the budget segment. Subsidies are a "dangerous opportunity": you receive them, but not your suppliers — they will raise prices and the economics break.

**Hype and trend.** Hype is a short-term spike of attention; a trend rests on the values of a large number of people and reaches a plateau of adoption. Criteria of a trend: it spreads across at least 3 countries and several industries, and lasts several years. The Gartner curve (trigger → peak of inflated expectations → trough of disillusionment → slope of enlightenment → plateau) shows the phase of a technology; "Moore's chasm" is the gap between early adopters and the majority, who need a stable product. A contrast example: computer vision (medicine, retail, security, agriculture) is a trend; augmented reality has episodic applications — hype. External events can accelerate trends quickly (remote work after the pandemic).

**Market structure (per the lecture)**

| Level | Definition | Sources |
|---|---|---|
| PAM (potential available) | everyone who could become a customer now and in the foreseeable future; used to validate the lower levels | reviews, World Bank open data, UN Comtrade, Statista |
| TAM (total addressable) | customers with the need, not necessarily ready to pay | Rosstat statistics, the tax service, agency data, VTsIOM/FOM surveys |
| SAM (serviceable available) | the part of TAM that already uses your product and competitors' products | public companies' filings, SensorTower, Similarweb, Google Trends, Mediascope, Crunchbase |
| SOM (serviceable obtainable) | the share of SAM that can be captured given channels, conversions, budgets and capacities | your own assumptions and benchmarks |

Definitions of TAM/SAM may differ in other sources (in `M-market-sizing` SAM is broader) — the document must always state explicitly how each level is defined.

Units: users (B2C), money (universal, mandatory for B2E), product units (manufacturing), contracts (B2E). It is best to measure both in people and in money.

## Procedure
1. **Define the market type** and the sides (who pays, who uses). For B2B, name the specific decision-making people (`M-customers`).
2. **Collect macro-trends across PESTEL** — 10–15 of them, only ones relevant to the product. Tag each one: threat / opportunity / both.
3. **For each trend, record**: the essence, the source and date (fact), the forecast and who issued it, and the hypothesis of impact on the product's metrics (explicitly marked as a hypothesis).
4. **Prioritize**: assess the importance for the product and the probability of occurrence (a 1–3 scale; score = importance × probability) and select the top 5–6. The rest go to the watch list. Example for a messenger: the correspondence-storage law 3×3=9 (a threat, must be accounted for); correspondence secrecy 3×1=3 (solved by infrastructure); the foreign-messengers law 1×2=2 (defer).
5. **Check hype vs trend** for each technological hypothesis (criteria above; plus signals: are real users paying, is there a business model, has it held for more than 2 years). If the trend is confirmed: find existing cases and their impact on the business model/service/product, the needs it rests on, the acceleration/deceleration factors, and applicability ("what we are actually ready to implement").
6. **For significant trends** — a mitigation plan (threat) or a way to use it in the product and the USP (opportunity); pass it into `M-risks` and `M-goals-drivers-bets`.
7. **Measure the market**: first visualize the segments ("who are the customers we are counting?"), then PAM → TAM → SAM → SOM in money and in people.
8. **Compute SOM** from an analogue/competitor of comparable capacity:
   SOM, ₽/year = downloads (new users, people/month) × 12 × purchase conversion × frequency (orders/person/year) × average ticket, ₽ × buyout share.
   Then overlay capacity constraints (production, service, the number of salespeople × deal duration × the number of parallel projects).
9. **Validate the calculation**: the levels differ by at least ~10×; SOM is noticeably smaller than SAM; two methods (top-down and bottom-up) give a comparable order of magnitude; parameters are taken from data, not "eyeballed".
10. **Draw the conclusion for the strategy**: is the market enough for Goal B? If SOM is smaller than the goal, that is an argument for revising the goal or the segment, or for closing the direction. For complex calculations — `M-market-sizing`.

## Template / checklist
**Trend registry**
| Area | Trend | Fact / forecast / hypothesis | Source, date | Threat / opportunity | Importance 1–3 | Probability 1–3 | Score | Hype or trend | Action |
|---|---|---|---|---|---|---|---|---|---|

**SOM calculation (example from the course)**
| Parameter | Value | Source | Type (fact / assumption) |
|---|---|---|---|
| New users, people/year | 120,000 (the level of a comparable app) | app stores | fact, estimate |
| Purchase conversion | 2% | benchmark | assumption |
| Orders per customer per year | 5 | assumption | assumption |
| Average ticket | 2,000 ₽ | open data | fact, estimate |
| SOM | 120,000 × 2% × 5 × 2,000 = 24M ₽/year | — | calculation |

Another example: apparel — 170,000 downloads/month × 12 × 1% × 1 order × 5,000 ₽ × 60% buyout ≈ 61M ₽/year; for the restaurant-delivery market in the lecture example: Russia's food-service turnover of 3.44 trillion ₽/year → restaurant delivery of 664 billion ₽/year → the SOM of one's own service of 24M ₽/year. Always re-check the arithmetic: on the apparel-chain slide, 50 thousand downloads × 1% × 12 months = 6,000 customers (not 500), and then 6,000 × 2,000 ₽ × 2 orders = 24M ₽.

**Checklist**
- [ ] For every figure, the source, date, unit and period are stated
- [ ] Forecasts are not passed off as facts
- [ ] The registry contains both threats and opportunities
- [ ] No more than 5–6 priority trends; the rest are on the watch list
- [ ] Hype is separated from trend using the criteria
- [ ] PAM/TAM/SAM/SOM are defined explicitly and measured in money and in people
- [ ] SOM is validated with capacity constraints and a second method

## Typical mistakes
- **Collecting "all the trends in the world"** instead of the ones affecting the product.
- **Only threats** (or only opportunities) — a trend is almost always two-sided.
- **"Number magic"**: small inflations at each step (a conversion of 2.3% instead of ~1%, 2 purchases instead of 1, a buyout of 50% instead of 80%) produce a market 4–10× larger than reality.
- **SOM ≈ SAM** is a sign of an error; **SOM ≠ a traction model** (SOM is potential under conditions; it is needed for the "do or don't do" decision).
- **A single estimator** — blind spots; estimates are subjective, but the discussion is more valuable than the numbers themselves and must be recorded (the estimation logic, the review date).
- **A frozen snapshot**: the estimates are never revisited (remote work was "monitor, probability 3" right up to the pandemic).
- **Confusing FOMO with a trend**: wait for confirmation by real usage and money; do not invest resources in what has not passed the check.
- **The market is measured to confirm the idea**; most often the calculation is needed to see "don't do it" — and that is a valuable result.
- **Units don't match the business model** (users for a B2E business with four large clients).
- **A factor without a decision and without a source**: the trend is described in words, but the registry has neither a link nor a specific action — it does not affect the strategy.
- **No "research summary"**: factors are listed, but nothing says which prevail (opportunities or threats), which are the main ones, or what that means for the product.

## Questions that can change the decision
- Will the market sustain Goal B (in money and in people): is SOM ≥ the goal with a margin?
- Which of the priority trends is regulatory with a hard deadline? It can change the timeline and budget.
- Is the market growing through new users or through frequency among existing ones (in the course example the leaders' traffic is comparable — growth comes only from frequency)?
- Which calculation assumptions (conversion, frequency, ticket) are most sensitive, and is there data to replace them with facts?
- What happens if a priority threat materializes ahead of schedule (the stop scenario)?
- What will change in the market over 2–3 years because of a technological trend with low probability but high importance?

## Related maps
[[M-strategy-growth]], [[M-customers]], [[M-competitors]], [[M-market-sizing]], [[M-risks]], [[M-source-criticism]], [[M-research-types]], [[M-traction-model]]
