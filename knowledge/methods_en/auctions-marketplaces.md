---
id: M-auctions-marketplaces
lang: en
title: Auctions and marketplaces (mechanics, metrics, market health)
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [options, strategy, validation, after-decision]
tags: [auctions, marketplace, gsp, vcg, gfp, fill-rate, take-rate, liquidity, toxic-revenue, antifraud]
related: [M-monetization, M-unit-economics, M-business-models, M-traction-model, M-benchmarking, M-quant-methods]
---

# Auctions and marketplaces (mechanics, metrics, market health)

## When to apply
"Allocating a scarce resource (search positions, ad slots, leads) among many buyers", "is an auction needed at all, or is a fixed price enough", "which auction type to choose", "how to tell that an auction is healthy and the revenue is not toxic", "how marketplace economics works: liquidity, take rate, the balance of the two sides".

## Core idea
**An auction** is a mechanism for competitively allocating a scarce resource. Three parties: the platform (owns the resource, wants money without losing quality), the buyers of the resource (advertisers/sellers — they bring content and bids), and the matching algorithm. **Score** balances money and quality: `Score = f(Bid, buyer quality, seller quality)` — otherwise the platform "buys" the search results, trust falls, CTR falls, advertisers leave ("lose the buyers — the sellers will follow").

**Advertising ≠ promotion:** advertising is absolute positions with a separate auction and specially created content, obliged to report; promotion is relative re-weighting of real listings in the organic results, and may be a hidden auction.

**Classification:**
```
Open (bids visible to everyone): English (bids rise), Japanese (the leader raises,
  the rest exit once their limit is reached), Dutch (the price falls, the first to
  accept wins)
  → they do not scale in digital (millions of parallel trades per millisecond needed)
Sealed-bid (the basis of digital):
  one lot: First Price (you pay your bid) | Second Price/Vickrey (you pay the second bid)
  many lots: GFP (generalized first price) | GSP (generalized second price) | VCG (you pay
  the marginal harm done to the others)
```
- **FPA/GFP:** easy to explain ("bid 100 — pay 100"), but it breeds **bid inflation** — the runaway of bids in recurring auctions (the real value of a slot is 80, bids climb 100→120→130) and manipulation by large players ("teaching" the market to accept high bids).
- **SPA/GSP:** truthful bidding — it is optimal to state your real valuation; overbidding is pointless (you pay the second price). Harder to explain: load on support, risk of collusion (at a scale of millions — practically impossible).
- **VCG:** theoretically optimal, truthful bidding is a dominant strategy, but "nobody can explain the payment" — professional closed communities only.
- **Hidden auction:** the participant does not know they are taking part (classified search) — complex mechanics can be allowed with nothing explained. Legally it is secured by the platform's right not to explain the position in the results.

**Allocation example (2 slots, 3 players).** Slots: place 1 — 100 clicks, place 2 — 60. Bids per click: A 5, B 4, C 3 ₽. Values: A1=500, B1=400, C1=300; A2=300, B2=240, C2=180. Optimum: A→place 1, B→place 2, C gets nothing; total value 740. Payments: GFP A=5×100=500, B=4×60=240; GSP A=4×100=400, B=3×60=180; VCG — the payment equals the harm done to the others by your presence (A≈340, B≈180, C=0).

**Selection rules:**
- Three conditions for introducing an auction: the resource is limited; demand > supply; willingness to pay differs. If any one of them fails → fixed price. A startup should not build its own auction — take an off-the-shelf SaaS solution.
- **"The more we have to explain, the simpler the auction must be."** Two factors: the professionalism of the market (mass market → GFP; professional market/hidden → GSP; trader communities → VCG) and the obligation to explain (advertising with reports → GFP; hidden search → GSP). Test: "would Maria Petrovna from Rostov-on-Don understand why she paid exactly this amount, without the phrase 'because'?" If not — the mechanics is too complex for a mass market.
- Case references: classifieds advertising — GFP (transparent reports on every impression); search — GSP as a hidden auction; bidding for a car between people — the simplest first price on a single lot (the platform takes a commission on the sale, not on the auction revenue; dealers bid below the market, compensating with speed, "same day").

## Procedure
1. **Check the three conditions** (scarce resource, demand > supply, differing WTP). Otherwise — fixed price.
2. **Define the parties and the balance:** who pays, who consumes the resource, which quality factor enters the score (listing CTR/conversion, seller response speed, relevance).
3. **Choose the mechanics** by the explainability rule (see above); decide whether the auction is open or hidden; fix in the documents the right not to explain the position (for hidden ones).
4. **Calibration:** floor/reserve prices, quality score, anti-domination limits (anti-spilling: one player must not win everything).
5. **Money metrics:** `Revenue = price × outcome (impressions/clicks/leads)`; **ASP** = revenue / units sold (a low ASP = junk traffic or no competition); the average bid (a gap between the bid and the payment is normal for GSP, alarming for GFP); RPA = revenue per auction; revenue per active participant.
6. **Market metrics:** active participants; **participants in each specific auction** (a million parallel auctions: a narrow local one "suffocates" invisibly inside the average); **fill rate** = filled slots / all slots — paradoxically important: an empty slot breaks the habitual UX (banner blindness), and advertisers will come complaining about falling impressions; selling a slot slightly cheaper while keeping the fill rate is sometimes more profitable.
7. **Sustainability metrics:** the share of participants winning at least something; advertiser retention and churn; complaints (an early churn signal). The ad market is narrow — there is direct competition for large clients (banks, retail), and "everyone watches" retention.
8. **The advertiser's economics = the bid ceiling:** `profit per click = (margin per sale × CR click→sale)`; bidding above that is unprofitable for the client (a phone: profit 20,000 ₽ × CR 2% = 400 ₽ — the maximum bid per click).
9. **Toxic revenue (bad revenue)** — revenue growth at the expense of the market: revenue grows while active participants fall, dependence on 1–2 large buyers grows, the fill rate or the quality of the results falls, participants "game the system". Defense: market-health metrics on a par with Revenue, diversity of participants, moderate floor prices.
10. **Antifraud:** bid manipulation and bot traffic kill ASP → the cascade "ASP falls → advertisers leave → Revenue falls". Monitor ASP as a leading indicator.

### Marketplace and liquidity
- **Classified vs marketplace:** a classified connects the sides (the transaction happens off the platform — no commission, lead generation); a marketplace runs the transaction through the platform — higher operational complexity (schedules, documents, logistics), but there is quality control and a commission. The classified→marketplace transition (delivery, booking, escrow) = switching on transactional monetization (see [[M-monetization]]).
- **The value cycle (flywheel):** more sellers → more content → more buyers → more demand for content → sellers again. Liquidity = both sides are present in each specific market (category × geo), not on average across the platform.
- **Take rate** — the platform's share of the deal money; in a digital auction compute the implicit TR (ad spend / client revenue). Take benchmarks by category: auto lead generation ~1% of the price; housing rent 8–20%; food delivery 15–35% (check the grade of the sources, [[M-benchmarking]]).
- Balancing the sides: a private seller needs ~10 contacts per sale; a professional seller with 2,000 items — tens of thousands. Allocate proportionally to budget and need, otherwise the small side churns.

## Template / checklist
| Field | Fill in |
|---|---|
| Scarce resource and its volume | |
| Conditions: demand > supply? Does WTP differ? | |
| Chosen mechanics (GFP/GSP/VCG/fixed) and why (explainability) | |
| Open or hidden auction | |
| Score: bid + quality factors | |
| Metrics: Revenue, ASP, bid vs payment, RPA, fill rate, participants/auction | |
| The client's bid ceiling (profit per click/lead) | |
| Health metrics: advertiser retention, complaints, top-client share | |
| Signs of toxic revenue — reaction thresholds | |

Exit artifact: the justification for needing an auction → the chosen mechanism with its rationale → a map of metrics with thresholds → a calibration and antifraud plan → market-health monitoring.

## Typical mistakes
- Introducing an auction without the three conditions (too few participants — "just let them buy").
- GFP for a professional recurring market: bid inflation eats the value.
- SPA for a mass market with a support team: a stream of "why didn't I pay my own bid" questions.
- Forgetting that fill rate and UX stability matter more than the short-term margin of a single slot.
- Optimizing only Revenue: revenue growth with falling participants and ASP = toxic revenue.
- Bid ≠ payment: comparing the average bid with ASP without adjusting for the auction type.
- Not checking participants in every local auction (category × geo), seeing only the average.
- Ignoring the client's profit per click: bids above their threshold wash advertisers out.

## Questions that can change the decision
- What happens to the quality of the results / the buyers' experience at full monetization of the resource?
- Can the platform explain its payment mechanics — and should it?
- Who are our largest payers, and how dependent is revenue on them?
- Is there enough liquidity in every local market, or do auctions "suffocate" in narrow categories?
- Wouldn't a fixed price or a SaaS auction be simpler at our scale?

## Related maps
[[M-monetization]], [[M-unit-economics]], [[M-business-models]], [[M-traction-model]], [[M-benchmarking]], [[M-quant-methods]], [[M-model-validation]]
