---
id: M-external-environment
lang: en
title: External environment analysis — market types, PESTEL, trend or hype, calculating potential
course: strategy
sources: ["EN mirror of the RU methodology card M-external-environment (knowledge/methods/external-environment.md); original sources are listed in the RU card"]
stages: [intake, research, options, strategy]
tags: [pestel, trends, hype, market, pam, tam, sam, som, b2b, b2c, c2c, threats-opportunities]
related: [M-strategy-growth, M-customers, M-competitors, M-market-sizing, M-risks, M-source-criticism, M-research-types, M-traction-model]
---

# External environment analysis — market types, PESTEL, trend or hype, calculating potential

## When to apply
When you need to understand the conditions under which the product will grow: which market we are playing on, which external forces will help or hinder us, whether the market is big enough for the growth target. The result is the "Analysis of the current state" section of the strategy: trends, challenges, opportunities and market size with sources. The map separates **facts** (measured, with a source and date), **forecasts** (someone else's estimate of the future) and **the agent's hypotheses about the impact** on the product.

## Essence
**Market** — all potential customers of the product. The market type determines the approach to acquisition and monetization:
| Type | Essence | What changes for strategy |
|---|---|---|
| B2C | the value goes to the end consumer | mass acquisition, product- or marketing-led |
| B2B | a product for organizations; often there is sales | the client is specific decision-making people; sales-led |
| B2E | a subtype of B2B for large clients with customization | few clients, large deal size, consulting and implementation; size the market in money and contracts |
| B2G | the client is the government, more often via procurement | a social function, tenders, legal requirements |
| C2C | users create value for each other, an intermediary is needed (classifieds) | two sides, liquidity, trust |
| B2B2C | a business works with small businesses for the sake of end consumers | marketplaces: supply and demand must be grown together |

**PESTEL** — six domains of external factors; collect only what affects *this* product (an unemployment-benefits service does not need real-estate trends).
| Domain | What we look at | Example impact on the product |
|---|---|---|
| Political | unions and conflicts, sanctions, borders, visas, taxes, subsidies, elections | flight-ticket service: borders and visas; marketplace: trade relations between countries; messenger: the emergence of a state messenger |
| Economic | growth, inflation, exchange rates, interest rates and credit availability, unemployment, purchasing power | real-estate search: mortgages; marketplace: purchasing power; freelance exchange: unemployment |
| Social | demographics, lifestyle, education, migration, inclusion | real estate: birth rate; marketplace: lifestyle changes |
| Technological | new technologies, automation, protocols, cybersecurity, R&D | marketplace: LLMs in ranking and hyper-personalization; freelance: automation of self-employment |
| Environmental | climate, recycling, carbon footprint, eco-policy | marketplace: the sustainability trend |
| Legal | data protection, labor, intellectual property, consumer rights, platform regulation | marketplace: platform-economy law; messenger: message storage |

**Concrete "factor → product" links** (for calibrating the search): the central bank's key rate hits high-ticket goods (real estate, cars, premium) — the higher the ticket, the stronger the dependence on the cost of money; unemployment — demand on job boards (the lowest unemployment in 10 years means a growing business can stop growing); the shift to the stories model of content consumption — social networks and promotion; the appearance of a simple tax tool (like "My Tax") legalizes the "gray" segment and pours it into freelance exchanges; a patent block can freeze a release for years (the browser "tabs" lawsuit dragged on for about 1.5 years); turnover fines for personal-data leaks — a direct financial risk for services with user profiles; climate affects non-obviously: a warm winter cuts demand for dachas in warm regions but lengthens the couriers' season. Regulatory factors often have an effective date — it must be written into the register explicitly.

**The working format of a PESTLE register** (as in the course's calculation spreadsheets): document header — product, research goal, date and assessment horizon (e.g. 5 years), research conclusions (the verdict: are there more opportunities or threats, and which factors are the main ones). Then a table sorted by descending significance:
| Group (P/E/S/T/E/L) | Factor (a wording with a number) | Opportunity / threat | Impact 1–10 | Probability 1–10 | Significance = Impact × Probability | Decision (a concrete product action) | Link to source |
|---|---|---|---|---|---|---|---|
Differences from a "list of trends": each factor has a numeric wording ("85% of tourists book on their own", not "people increasingly book online"), a link and, most importantly, a decision — otherwise the factor never made it into the strategy. Research conclusions are a mandatory block: "opportunities prevail (5 of the top 7 factors), the main drivers are …, the main threats are …".

**Any trend can be both a threat and an opportunity**: falling purchasing power is a threat for a marketplace, but also a chance to bet on the cheap segment. Subsidies are a "dangerous opportunity": you get them, but not your suppliers — they will raise prices, and the economics break.

**Hype and trend.** Hype is a short-term spike of attention; a trend rests on the values of a large number of people and reaches an adoption plateau. Criteria of a trend: it spans at least 3 countries, several industries, and lasts several years. The Gartner curve (trigger → peak of expectations → trough of disillusionment → slope of enlightenment → plateau) shows the phase of a technology; Moore's "chasm" — the gap between early adopters and the majority, which needs a stable product. An example of contrast: computer vision (medicine, retail, security, agriculture) — a trend; augmented reality — episodic applications, hype. External events can rapidly accelerate trends (remote work after the pandemic).

**Market structure (per the lecture)**
| Level | Definition | Sources |
|---|---|---|
| PAM (potential available) | everyone who could become a customer now and in the foreseeable future; used to sanity-check the lower levels | industry reviews, open World Bank data, UN Comtrade, Statista |
| TAM (total addressable) | customers with the need, not necessarily ready to pay | Rosstat statistics, tax and departmental data, VCIOM/FOM polls |
| SAM (serviceable available) | the part of TAM already using your product and competitors' products | public-company reports, SensorTower, Similarweb, Google Trends, Mediascope, Crunchbase |
| SOM (serviceable obtainable) | the share of SAM you can take given channels, conversions, budgets and capacity | your own assumptions and benchmarks |
TAM/SAM definitions in other sources may differ (in `M-market-sizing` SAM is broader) — always record in the document how each level is defined.

Units: users (B2C), money (universal, mandatory for B2E), units of output (manufacturing), contracts (B2E). It is best to count both in people and in money.

## Procedure
1. **Determine the market type** and the sides (who pays, who uses). For B2B, name the specific decision-making people (`M-customers`).
2. **Collect macro-trends across PESTEL** — 10–15 of them, only ones relevant to the product. Assign each a type: threat / opportunity / both.
3. **For each trend record**: the essence, source and date (fact), the forecast and who made it, the hypothesis of impact on product metrics (explicitly labeled as a hypothesis).
4. **Prioritize**: score importance for the product and probability of occurrence (scale 1–3; rating = importance × probability), pick the top 5–6. The rest go into a watch list. Example for a messenger: message-storage law 3×3=9 (threat, must be addressed); correspondence privacy 3×1=3 (solved by infrastructure); law on foreign messengers 1×2=2 (postpone).
5. **Check hype/trend** for every technology hypothesis (criteria above; plus signs: are real users paying, is there a business model, has it held for more than 2 years). If the trend is confirmed: find existing cases and their impact on the business model/service/product, the needs it rests on, acceleration/deceleration factors, and applicability ("what we are actually ready to implement").
6. **For significant trends** — a mitigation plan (threat) or a way to use it in the product and the USP (opportunity); pass to `M-risks` and `M-goals-drivers-bets`.
7. **Size the market**: first visualize the segments ("who are the customers we are counting?"), then PAM → TAM → SAM → SOM in money and in people.
8. **Compute SOM** from an analog/competitor of comparable scale:
   SOM, RUB/year = downloads (new users, people/month) × 12 × conversion to purchase × frequency (orders/person/year) × average order value, RUB × redemption share.
   Then overlay capacity constraints (production, service capacity, number of salespeople × deal duration × number of parallel projects).
9. **Sanity-check the calculation**: the levels differ by at least ~10×; SOM is noticeably smaller than SAM; two methods (top-down and bottom-up) give a comparable order of magnitude; the parameters come from data, not "gut feeling".
10. **Draw the conclusion for strategy**: is the market sufficient for goal B? If SOM is smaller than the target — that is an argument for revising the target, the segment, or for shutting the direction down. For complex calculations — `M-market-sizing`.

## Template / checklist
**Trend register**
| Domain | Trend | Fact / forecast / hypothesis | Source, date | Threat / opportunity | Importance 1–3 | Probability 1–3 | Rating | Hype or trend | Action |
|---|---|---|---|---|---|---|---|---|---|

**SOM calculation (course example)**
| Parameter | Value | Source | Type (fact / assumption) |
|---|---|---|---|
| New users, people/year | 120,000 (level of a comparable app) | app stores | fact, estimate |
| Conversion to purchase | 2% | benchmark | assumption |
| Orders per customer per year | 5 | assumption | assumption |
| Average order value | 2,000 RUB | open data | fact, estimate |
| SOM | 120,000 × 2% × 5 × 2,000 = 24 million RUB/year | — | calculation |
Another example: apparel — 170,000 downloads/month × 12 × 1% × 1 order × 5,000 RUB × 60% redemption ≈ 61 million RUB/year; for the restaurant-delivery market in the lecture's example: catering turnover of 3.44 trillion RUB/year → restaurant delivery 664 billion RUB/year → SOM of one's own service 24 million RUB/year. Always re-check the arithmetic: in the slide about an apparel chain 50 thousand downloads × 1% × 12 months = 6,000 customers (not 500), and then 6,000 × 2,000 RUB × 2 orders = 24 million RUB.

**Checklist**
- [ ] Every number has a source, date, unit and period
- [ ] Forecasts are not passed off as facts
- [ ] The register contains both threats and opportunities
- [ ] No more than 5–6 priority trends; the rest on a watch list
- [ ] Hype is separated from trend by the criteria
- [ ] PAM/TAM/SAM/SOM are explicitly defined, counted in money and in people
- [ ] SOM is verified with capacity constraints and a second method

## Typical mistakes
- **Collecting "every trend in the world"** instead of ones affecting the product.
- **Only threats** (or only opportunities) — a trend is almost always two-sided.
- **"Number magic"**: small inflations at every step (conversion 2.3% instead of ~1%, 2 purchases instead of 1, redemption 50% instead of 80%) yield a market 4–10 times bigger than reality.
- **SOM ≈ SAM** — a sign of an error; **SOM is not the traction model** (SOM is the potential under conditions; it is needed for the "build or not" decision).
- **A single estimator** — blind spots; estimates are subjective, but the discussion is more valuable than the numbers themselves and must be recorded (estimation logic, review date).
- **A freeze-frame**: the estimates are never revisited (remote work was "to watch, probability 3" right up until the pandemic).
- **Confusing FOMO with a trend**: wait for confirmation by real usage and money; do not invest resources in what has not passed the check.
- **The market is sized to confirm an idea**; most often the calculation is needed to see "we should not do it" — that is a valuable result.
- **Units do not match the business model** (users for a B2E business with four large clients).
- **A factor without a decision and without a source**: the trend is described in words, but the register has neither a link nor a concrete action — it does not affect the strategy.
- **No "research conclusions"**: factors are listed, but nothing says whether there are more opportunities or threats, which are the main ones, and what that means for the product.

## Questions that can change the decision
- Will the market sustain goal B (in money and people): is SOM ≥ the target with headroom?
- Which priority trend is regulatory, with a hard date? It can change the timeline and budget.
- Does the market grow through new users or through frequency among existing ones (in the course example the leaders' traffic is comparable — growth comes only from frequency)?
- Which calculation assumptions (conversion, frequency, order value) are most sensitive, and is there data to replace them with facts?
- What happens if a priority threat materializes early (the stop scenario)?
- What will change in the market over 2–3 years because of a low-probability but high-importance technology trend?

## Related maps
[[M-strategy-growth]], [[M-customers]], [[M-competitors]], [[M-market-sizing]], [[M-risks]], [[M-source-criticism]], [[M-research-types]], [[M-traction-model]]
