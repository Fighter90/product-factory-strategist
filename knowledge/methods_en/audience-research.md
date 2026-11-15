---
id: M-audience-research
lang: en
title: Target audience research, segmentation, personas, and recruiting
course: ux
sources: ["EN mirror of the RU methodology card M-audience-research (knowledge/methods/audience-research.md); original sources are listed in the RU card"]
stages: [research, options, strategy]
tags: [target-audience, segmentation, personas, audience-profile, recruiting, screener, vpc, jtbd]
related: [M-customers, M-jtbd, M-research-types, M-brief-hypotheses, M-in-depth-interviews, M-interview-analysis, M-quant-methods, M-usp, M-market-sizing, M-product-communication, M-synthetic-respondents]
---

# Target audience research, segmentation, personas, and recruiting

## When to use
You need to answer: "for whom are we building the product, which segment do we target first, how do we describe these people so that design, USP, and communication hit a concrete person, and how do we find respondents for the research." This map is the foundation before formulating the USP ([[M-usp]]) and before launching any field research.

## Core idea
**Target audience (TA)** — a group of people or companies for whom the product is intended. "Everyone" is never a target audience: even the most mass products fall apart into niches by barriers, constraints, and values. An error in understanding the TA produces "features in vain," weak adoption, and poor retention. Knowledge of the TA is needed to: build the product around real pains; focus marketing and the USP; make decisions on data; find new segments and niches.

**Types of TA.** Primary and indirect (those who decide on the purchase and those who influence the decision); broad and narrow; B2B (organizations with different needs and roles in the decision) and B2C.

**Segmentation** — grouping homogeneous customers by a shared basis; it lets you size segments and pick the key ones. It consists of a qualitative stage (interviews, focus groups: forming attributes and hypotheses about clusters) and a quantitative one (a survey or behavioral data: estimating sizes and differences).

**Segmentation bases.**
| Basis | Example attributes | Course's assessment | How to measure |
|---|---|---|---|
| Demographics | age, gender, life stage, social group | weak as a standalone basis; always look at it together with others | simple surveys, desk research |
| Value | Basic vs Premium, average order value, turnover, company size | good for B2B, weak for B2C | own analytics, industry data |
| Behavior | purchase frequency, feature engagement, loyalty | good for B2B and B2C | analytics, surveys, statistical methods |
| Attitudes | psychographics, lifestyle, interest, risk appetite | like behavior, closer to B2C | surveys, statistical methods |
| Needs | benefit from the product, choice factors, emotional state (JTBD) | the strongest and the hardest | surveys + statistics (factor, cluster analysis) |
Simple bases (demographics, basic behavior) are covered by analytics and short surveys; complex ones (attitudes, needs) require a well-designed questionnaire and statistics.

**A good segment:** large enough, reachable (it can be found and approached), homogeneous inside, distinct from others by a set of attributes (no complete overlap); it is also useful to check stability over time and fit with strategy/resources.

**TA profile → segment → persona.** A *profile* is the first description after desk research and data about customers (socio-demographics, psychographics, goals, behavior, product specifics); blank spots are normal. A *segment* is a refined profile after the qualitative and quantitative stages (with a size and distinctive attributes). A *persona* is the key segment's profile further refined with quantitative characteristics, interaction scenarios, and quotes; it helps address a concrete person when designing the interface, USP, and communications.

**Strength of evidence.** A profile from 5–10 interviews and analytics is a *hypothesis about segments*. Segment size, shares, and differences by attributes are proven only by the quantitative stage. A persona is a working tool, not a fact about the market: it must be validated with a pilot campaign or an MVP on the chosen segment and revisited as the market moves.

## Procedure
1. **Analyze the market and competitors**: trends, products, positioning, your own position ([[M-research-types]], desk research and benchmarks).
2. **Collect data about the product and customers**: product analytics, UX research results, support tickets, store reviews and other platforms, past desk studies, colleagues' knowledge (sales, support), your own user experience. Put it into a table "source → fact → label (pain, motive, barrier, trigger)".
3. **Draft the profile**: socio-demographics, psychographics (values, lifestyle, pains, motivation), goals and typical behavior, specifics (region, device, payment method). Mark blank spots and hypotheses.
4. **Check that there are several profiles**: if you ended up with 1–2, the segmentation basis is too generic.
5. **Choose the goal and the segmentation basis.** One primary basis (behavior or need) + auxiliary ones (demographics). If unsure which segments exist at all, start with the qualitative stage.
6. **Qualitative stage** (5 steps): goal and basis → interview/focus-group guide ([[M-in-depth-interviews]]) → recruiting TA representatives → running the fieldwork → refining or forming segments ([[M-interview-analysis]]). Result — refined profiles and hypotheses about differences.
7. **Quantitative stage**: choose the method to match the basis (demographics — survey and descriptive stats; value — analytics and reports; behavior — analytics and survey; attitudes and needs — survey and statistics) and compute the sample ([[M-quant-methods]]). To estimate a segment share to ±5 p.p. at 95%, ~385 answers are enough (if the segment is rare, the screener needs a larger reach). Result — segment sizes and the main differentiating factors.
8. **Assemble the segment matrix**: columns — segments; rows — size (% of all buyers), behavior/channel choice, socio-demographic profile, attitudes, willingness to pay, barriers, key needs. The set of rows depends on the basis, CJM stages, and the funnel.
9. **Choose the key segments** by five parameters: size of the potential market (number of customers); ability to generate profit (purchasing power); accessibility (can we work with them effectively); degree of competition inside the segment; compatibility with goals and resources. Explicitly write down whom we *do not* take and why.
10. **Describe personas** for the key segments: demographic profile, motivation, top choice criteria, attitude to the category (quotes), drivers and barriers toward your product, functional needs.
11. **Validate in the field**: pilot campaign, MVP, or advertising targeted at the segment; watch behavior, metrics, feedback; adjust the segments.
12. **Link to the product:** the left side of the Value Proposition Canvas — Jobs-to-be-done, Gains, Pains per segment (see [[M-usp]], [[M-jtbd]]).

## Recruiting respondents
Recruiting quality is the main factor of reliability (in the course: "about 70% of TA research success").
1. Define the profile (from the profile draft, agreed with the product): mandatory and excluding attributes.
2. Screener — a short filter questionnaire with control questions and "traps" (to screen out inattentive and dishonest people); terminate on a key "no"; test it on colleagues.
3. Find respondents (mix at least two independent channels): the customer base (an export by criteria, sales managers and account managers); site/service (embedded surveys, invitation banners); social networks, communities, topical channels; recruiting agencies and online platforms; personal networks and "snowball" (relevance matters more than availability; for rare and B2B profiles).
4. Selection and confirmation: analyze the screener, a call/letter about the time and format, written confirmation.
5. Exclude: marketing and media professionals, recent participants of similar studies, anyone connected with the team or the brand.
6. Motivation (money, gifts, discounts, early access): the amount is proportionate to time and complexity, terms are fixed in advance.
7. Handle people's data under personal data protection rules (in the RU jurisdiction — Federal Law 152): consent, minimization, storage period.

## Template / checklist
**TA profile (draft):**
| Field | Entry | Source / confidence (fact / hypothesis) |
|---|---|---|
| Gender, age, geography, family, profession | | |
| Psychographics (values, lifestyle, attitude to the category) | | |
| Motivation and goals | | |
| Pains and barriers | | |
| Behavior and channels (where they search, what they compare, whose opinion they trust) | | |
| Role in the decision (buyer / influencer / user) | | |

**Persona of the key segment:** segment name-label; size (%) and source; short profile; top-5 choice criteria; 3–4 characteristic quotes; drivers and barriers toward your product; search/purchase scenario; willingness to pay; what they expect from us.

**Mini-checklist before "going into the field":** the segmentation goal and success metric are written down; one primary basis is chosen; the guide covers pain, motivation, barriers, triggers; protection against biases is in place (screener, mixed channels); the questionnaire for the quant stage is ready; the criteria for choosing key segments are agreed.

**Example segments from the course (renovation, needs):** undemanding "do-it-yourselfers"; delegating specialists (do not understand the craft, willing to overpay for support); seekers of simple solutions (minimum money, inexpensive materials); perfectionist controllers (experienced, pay for a perfect result and control of the process). The takeaway: demographics do not distinguish these groups, needs do.

## Common mistakes
- "The TA is everyone" or one broad profile; dividing only by age and gender.
- Segments overlap, there are too many of them (ten or more), or the choice of key ones lacks a business rationale.
- Jumping to the quantitative stage without the qualitative one: measuring segments that do not exist.
- An invented persona: a pretty card without data and without a "hypothesis/fact" label.
- Recruiting "from friends" or only from the loyal base: bias toward friendly and experienced people.
- Segment sizes computed from interviews ("3 out of 8 — hence 40%").
- No testing after segmentation (a pilot campaign) and no revision: segments drift.
- Ignoring the indirect TA (who pays/influences but does not use).
- AI "personas" and synthetic respondents ([[M-synthetic-respondents]]) passed off as segment data: they only work as a source of hypotheses for verification and never estimate segment size or demand.

## Questions that can change the decision
- Who makes the purchase decision, who pays, who uses it: one person or different people?
- Which segmentation basis is best tied to a difference in *product behavior* (rather than descriptive convenience)?
- Is there internal customer data (CRM, analytics) that lets you do part of the work without fieldwork?
- How rare is the respondent profile you need and how long will recruiting take?
- What happens to the product/communication if you choose segment A rather than B (which decision depends on the segmentation)?
- Can the chosen segment be quickly validated with a pilot or advertising?

## Related maps
[[M-customers]], [[M-jtbd]], [[M-research-types]], [[M-brief-hypotheses]], [[M-in-depth-interviews]], [[M-interview-analysis]], [[M-quant-methods]], [[M-usp]], [[M-market-sizing]], [[M-product-communication]]
