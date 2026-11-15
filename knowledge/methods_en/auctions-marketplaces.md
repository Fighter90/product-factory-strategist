---
id: M-auctions-marketplaces
lang: en
title: Auctions and marketplaces (mechanics, metrics, marketplace health)
course: strategy
sources: ["EN mirror of the RU methodology card M-auctions-marketplaces (knowledge/methods/auctions-marketplaces.md); original sources are listed in the RU card"]
stages: [options, strategy, validation, after-decision]
tags: [auction, gsp, vcg, gfp, first-price, second-price, fill-rate, take-rate, liquidity, marketplace, bad-revenue, antifraud]
related: [M-monetization, M-unit-economics, M-business-models, M-traction-model, M-benchmarking, M-quant-methods]
---

# Auctions and marketplaces (mechanics, metrics, marketplace health)

## When to use
"Distributing a limited resource (search positions, ad slots, leads) among many buyers," "is an auction needed or will a fixed price do," "which auction type to choose," "how to tell that an auction is healthy and the revenue is not toxic," "how the economics of a marketplace work: liquidity, take rate, balancing the two sides."

## Core idea
An **auction** is a mechanism for the competitive distribution of a limited resource. Three parties: the platform (owns the resource, wants money without losing quality), the buyers of the resource (advertisers/sellers — they bring content and bids), and the matching algorithm. The **Score** balances money and quality: `Score = f(Bid, buyer quality, seller quality)` — otherwise the platform "buys" its search results, trust falls, CTR falls, and advertisers leave ("lose the buyers — the sellers follow").

**Advertising ≠ promotion:** advertising is absolute positions with a separate auction and specially created content; it must be reported. Promotion is a relative re-weighting of real listings in the organic results; it can be a hidden auction.

**Classification:**
```
Open (bids visible to everyone): English (bids rise), Japanese (the host raises,
  bidders drop out when hitting their limit), Dutch (price falls, the first to
  accept wins)
  → do not scale in digital (millions of parallel trades per millisecond needed)
Sealed-bid (the basis of digital):
  one lot: First Price (you pay your bid) | Second Price/Vickrey (you pay the
  second bid)
  many lots: GFP (generalized first price) | GSP (generalized second price) |
  VCG (you pay the marginal loss of the others)
```
- **FPA/GFP:** easy to explain ("you bid 100 — you pay 100"), but it breeds **bid inflation** — bids run up in recurring auctions (the real value of a position is 80, bids climb 100→120→130) and manipulation by large players ("teaching" the market to accept high bids).
- **SPA/GSP:** truthful bidding — bidding your true valuation is optimal; there is no point in overbidding (you pay the second price). Harder to explain: support load, risk of collusion (at the scale of millions — practically impossible).
- **VCG:** theoretically optimal, honest bidding is the dominant strategy, but "nobody can explain" the payments — professional closed communities only.
- **Hidden auction:** participants do not know they are participating (a classified search) — you can afford complex mechanics without explaining anything. Legally it is secured by the platform's right not to explain the position in the results.

**Distribution example (2 lots, 3 players).** Lots: position 1 — 100 clicks, position 2 — 60. Bids per click: A 5, B 4, C 3 ₽. Values: A1=500, B1=400, C1=300; A2=300, B2=240, C2=180. Optimum: A→position 1, B→position 2, C gets nothing; total value 740. Payments: GFP A=5×100=500, B=4×60=240; GSP A=4×100=400, B=3×60=180; VCG — payment = the harm to the others from your presence (A≈340, B≈180, C=0).

**Choice rules:**
- Three conditions for introducing an auction: the resource is limited; demand > supply; willingness to pay differs. If even one fails → fixed price. A startup should not build its own auction — take a SaaS solution.
- **"The more we have to explain, the simpler the auction must be."** Two factors: how professional the market is (mass market → GFP; professional market/hidden → GSP; trader communities → VCG) and whether you are obliged to explain (advertising with reports → GFP; hidden search → GSP). Test: "can Maria from down the street understand why she paid exactly this much, without the phrase 'because'?" If not — the mechanics are too complex for a mass market.
- Case references: classified advertising — GFP (transparent reports for every impression); search — GSP as a hidden auction; people bidding for a car — the simplest first price on a single lot (the platform charges a commission on the sale, not on auction revenue; dealers bid below market, compensating with same-day speed).

## Procedure
1. **Check the three conditions** (limited resource, demand > supply, differing WTP). Otherwise — fixed price.
2. **Define the sides and the balance:** who pays, who consumes the resource, which quality factor enters the score (ad CTR/conversion, seller response speed, relevance).
3. **Choose the mechanics** by the explainability rule (see above); decide whether the auction is open or hidden; fix in the documents the right not to explain the position (for hidden ones).
4. **Calibration:** floor/reserve prices, quality score, limiting dominance (anti-spilling: one player must not win everything).
5. **Money metrics:** `Revenue = price × outcome (impressions/clicks/leads)`; **ASP** = revenue / sold units (low ASP = junk traffic or no competition); average bid (a gap between bid and payment is normal for GSP, alarming for GFP); RPA = revenue per auction; revenue per active participant.
6. **Market metrics:** active participants; **participants per specific auction** (a million parallel auctions: a narrow local one "suffocating" is invisible in the average); **fill rate** = filled slots / all slots — paradoxically crucial: an empty slot breaks the familiar UX (banner blindness), and advertisers will come complaining about falling impressions; selling a slot slightly cheaper while keeping the fill rate can be more profitable.
7. **Sustainability metrics:** the share of participants who win anything; advertiser retention and churn; complaints (an early churn signal). The advertising market is narrow — direct competition for large clients (banks, retail), and everyone watches retention.
8. **Advertiser economics = the bid ceiling:** `profit per click = (margin per sale × CR click→sale)`; bidding above that is loss-making for the client (a phone: profit 20,000 ₽ × CR 2% = 400 ₽ — the maximum bid per click).
9. **Toxic revenue (bad revenue)** — income growth at the expense of market degradation: revenue grows while active participants fall, dependence on 1–2 large buyers grows, fill rate or result quality falls, "gaming the system" spreads. Protection: marketplace health metrics equal in weight to Revenue, diversity of participants, moderate floor prices.
10. **Antifraud:** bid manipulation and bot traffic kill ASP → cascade "ASP falls → advertisers leave → Revenue falls." Monitor ASP as a leading indicator.

### Marketplace and liquidity
- **Classified vs marketplace:** a classified connects the sides (the transaction happens off-platform — no commission, lead generation instead); a marketplace runs the transaction through the platform — higher operational complexity (schedules, documents, logistics) but quality control and a commission. The transition classified→marketplace (delivery, booking, escrow) = switching on transactional monetization (see [[M-monetization]]).
- **The value cycle (flywheel):** more sellers → more content → more buyers → more demand for content → sellers again. Liquidity = both sides are present in each specific market (category × geo), not on average across the platform.
- **Take rate** — the platform's share of the transaction money; in a digital auction compute the implicit TR (ad spend / client revenue). Take benchmarks by category: auto lead generation ~1% of price; housing rent 8–20%; food delivery 15–35% (check the evidence grade of sources, [[M-benchmarking]]).
- Balancing the sides: a private seller needs ~10 contacts per sale; a professional with 2,000 listings needs tens of thousands. Distribute proportionally to budget and need, otherwise the small side churns.

## Template / checklist
| Field | Fill in |
|---|---|
| Limited resource and its volume | |
| Conditions: demand > supply? WTP differs? | |
| Chosen mechanics (GFP/GSP/VCG/fixed) and why (explainability) | |
| Open or hidden auction | |
| Score: bid + quality factors | |
| Metrics: Revenue, ASP, bid vs payment, RPA, fill rate, participants/auction | |
| Client's bid ceiling (profit per click/lead) | |
| Health metrics: advertiser retention, complaints, top-client share | |
| Signs of toxic revenue — reaction thresholds | |

Exit artifact: justification of the auction's necessity → the chosen mechanism with argumentation → a metric map with thresholds → a calibration and antifraud plan → marketplace health monitoring.

## Common mistakes
- Introducing an auction without the three conditions (few participants — "let them just buy").
- GFP for a professional recurring market: bid inflation eats the value.
- SPA for a mass market with a support team: a stream of "why am I not paying my bid" questions.
- Forgetting that fill rate and UX stability matter more than the short-term margin of a single slot.
- Optimizing only Revenue: revenue growth while participants and ASP fall = toxic revenue.
- Bid ≠ payment: comparing the average bid with ASP without adjusting for the auction type.
- Not checking participants in every local auction (category × geo), seeing only the average.
- Ignoring the client's profit per click: bids above their threshold wash advertisers out.

## Questions that can change the decision
- What happens to result quality / buyer experience if the resource is fully monetized?
- Can the platform explain its payment mechanics — and should it?
- Who are our largest payers and how dependent is revenue on them?
- Is there enough liquidity in every local market, or do auctions "suffocate" in narrow categories?
- Would a fixed price or a SaaS auction be simpler at our scale?

## Related maps
[[M-monetization]], [[M-unit-economics]], [[M-business-models]], [[M-traction-model]], [[M-benchmarking]], [[M-quant-methods]], [[M-model-validation]]
