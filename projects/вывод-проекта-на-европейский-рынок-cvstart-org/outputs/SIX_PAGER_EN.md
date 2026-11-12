# Taking cvstart.org to the European market: six-pager

> Assembled 2026-11-10T00:00 by the `pfs export --six-pager` tool per the specification `knowledge/templates/SIX_PAGER_PROMPT_EN.md` (growth-strategy reference format: FAQ-1…6 with numbered subpoints, a tactics matrix, and KPIs in two dimensions). The [C###]/[S###] tags trace the origin of every number; source footnotes are at the end of the document.

**Request:** How to take the cvstart.org project to the European market

## FAQ-1. Analysis of the current state

### 1.1 Market overview: trends, challenges, and opportunities

### Short answer

The European resume-tool market is large and densely monetized: DE has ~109k unfilled IT vacancies [C011] (B); local clones sell at €21–23/mo with auto-renewal [C022][C024] (B); global players sell at €24.95 per 4 weeks after a €2.95 trial [C026] (B). The unoccupied corner for CVStart: multilingualism (19 locales [C007], A) + an honest free tier + privacy against competitors' trial-trap schemes. The main entry constraints: mandatory localization for DE/FR/ES [C017–C019] (A), the GDPR minimum [C036][C037][C062] (A/B), and solo resources with no budget [C059]. What we know least: real SEO volumes of the local keywords and willingness to pay in PL/ES — neither gap blocks the direction choice, but both affect the wave ordering and channel selection.

### What we know

#### Q1 — labor market sizes (answered)

- EU: 10+ million ICT specialists (2024), 5.0% of employment; Sweden leads at 8.6% [C010] (A)
- DE: 109,000 unfilled IT vacancies (2025), down from the 149k peak (2023) [C011] (B)
- NL: 15.1k open ICT vacancies (late 2025); 622,000 ICT specialists [C012] (A)
- FR: a shortage indicator of 1.1 for "IT engineers"; 42,635 hiring projects for a single profession [C013] (A)
- ES: ~120,000 unfilled tech vacancies; tech employment >1 million [C014] (B)
- SE: +18,000 tech specialists per year through 2028 [C015] (B)
- PL: +44% tech vacancies year over year (2025) [C016] (C)

#### Q2 — competitors and EUR prices (answered)

- Local clones: CVMaker €21.99/mo after a €1.99 trial [C022] (B); LiveCareer PL 99 zł/4 weeks [C024] (B); CVDesignR FR €9.99 [C023] (B)
- XING DE offers a free Lebenslauf + AI-Anschreiben [C021] (B)
- Global: resume.io €2.95/7 days → €24.95/4 weeks [C026] (B); resume.io and Teal bill in USD even on localized sites [C025] (A) [C027] (A)
- DE clones self-report 1+ million resumes — paying local demand [C028] (C)

#### Q3 — willingness to pay (partial)

- The Nordics pay +28% over the US price; local currencies add +5–25% to conversion [C029] (B, Paddle data)
- DE: 77% prefer PayPal over cards [C030] (B)
- PL/ES — no data (gap, see below)

#### Q4 — SEO (partial)

- "resume builder"/"cv maker" ~673k queries/mo each, globally [C031] (C)
- The DE/NL SERP is densely occupied by paid clones and government tools (researcher observation, D)

#### Q5 — OSS channels (answered)

- Reactive Resume — 45,485 stars (the niche ceiling) [C032] (A); Show HN 656/240 points [C075] (A)
- r/cscareerquestionsEU ~179,000 subscribers, +15.5%/yr [C074] (C); heise.de 5.68 million UU [C035] (B)

#### Q6 — GDPR/VAT/hosting (answered)

- US LLM APIs → SCC 2021/914 + TIA [C036] (A); VAT: Non-Union OSS from the first sale [C037] (A)
- EU hosting from €3.79/mo [C062] (B)

#### Q7 — resume language (answered)

- DE/FR/ES: the local language is mandatory for resumes and cover letters [C017][C018][C019] (A)
- SE: the job-posting language decides; IT works in English [C020] (A)

### Contradictions between sources

- Bitkom reports 109k while alternative aggregators report lower totals of unfilled vacancies (methodological differences: Bitkom counts all IT vacancies, job portals count only active listings) [C011]. Left open: the decision needs only the order of magnitude (tens of thousands) — the contradiction does not change the conclusion.
- XING's free Lebenslauf [C021] vs CVStart monetization: reconcilable — the free tier becomes a competitive requirement, not an option; the paid tier sits above features XING lacks (board scanning, tracker) [C004].
- Paddle's "Nordics +28%" [C029] vs CVDesignR FR €9.99 [C023]: different regions and products — not a contradiction within one conclusion; WTP is heterogeneous across countries, which supports regional pricing.

### What we don't know

| Gap | Why unknown | How to find out | Cost/timeline | Affects the decision? |
|---|---|---|---|---|
| Active job seekers by country | ~~Eurostat LFS does not break out IT professions~~ **closed by a 2026-11-08 proxy**: ranking by vacancy stocks and ICT employment — the result does not change [C069] | not required | €0 | no — the ranking by vacancies stayed the same |
| Local SEO volumes | ~~Keyword Planner requires an Ads account~~ **partially closed 2026-11-08**: the head cluster is verified (S041): "lebenslauf erstellen" — KD 57, CPC €4.97; the 49,500/mo volume is recorded for the no-space variant "lebenslauferstellen" [C076]; the cluster's "kostenlos" rows sit behind the free funnel of S041 — confirm via Search Console after launch [C077] | Keyword Surfer (exact data) / Search Console after launch | €0–30 | closed in favor of the SEO channel: the head volume is material |
| WTP PL/ES | closed payment-platform data | A/B of regional prices via an MoR at the validation stage | €0, during validation | yes — the ordering of waves 2–3 |
| Number of IT vacancies in PL (absolute) | ~~NFJ publishes dynamics without a total~~ **closed 2026-11-08**: justjoin.it — 110,996 vacancies in 2025 (+8.42% y/y) [C067] | not required | €0 | no — the PL wave 2 is confirmed [C070] |

### 1.2 Key competitors and analysis of their growth strategies and promo mechanics

Comparative table of competitor groups (per 02, Q2):

| | **Local clones** (CVMaker, LiveCareer PL, CVDesignR FR) | **Global players** (resume.io, Teal, Rezi) | **XING + government tools** |
|---|---|---|---|
| **Key advantages** | native language, local conventions, SEO dominance in their home SERP; paying demand confirmed (1+ million resumes at DE clones [C028]) | brand, product polish, scale; EUR prices on the surface (€24.95/4 weeks at resume.io [C026]) | free of charge; distribution via an ecosystem (jobs+CV at XING [C021]) |
| **Growth strategy and promo mechanics** | trial-trap (€1.99 → €21.99/mo [C022]), auto-renewals, long-tail SEO, LiveCareer PL 99 zł/4 weeks [C024] | paid search, a discount funnel (€2.95/7 days → €24.95 [C026]), USD billing even on localized sites [C025][C027] | an ecosystem bundle: a free Lebenslauf + AI-Anschreiben keeps users in the platform [C021] |
| **Risks for the company** | Medium — their trial-trap reputation is our opening (an honest free tier without auto-renewals); the conventions are already covered on their side | High — budgets for paid search; but USD billing and the absence of job scanning are their vulnerability | Medium — XING sets the bar of "the basics must be free" [C021]; weaknesses — outdated UX, no multi-source vacancy filtering |

> **Conclusion (inference):** the window of opportunity is ≈ 6–9 months, until the global players close the EUR-billing and job-scan gaps and the local clones abandon trial-trap. The only unoccupied combination is "an honest free tier without auto-renewals + filtering of real vacancies from all sources + local DE conventions" [C073][C062]. Consolidation — the 180-day gate of wave 1; a launch lag of more than 2 quarters reduces the odds of entry (see the risks in 04).

## FAQ-2. User Persona. Who is the target audience?

### 2.1 Segments

### Segments (discovery)

**Segment A — the core of wave 1: tech job seekers in DE/NL/SE, EN professionals.**
25–40 years old, job hunting for 1–6 months, international companies; in SE English is the IT-sector norm [C020] (A), in NL tech operates in English (hypothesis [C043]). JTBD: "When I look for a job in Europe, I want to filter the real vacancies from all sources and quickly produce a resume for each one that passes ATS — without manual routine, auto-renewals, or sending my data to someone else's cloud." Hypotheses from synthetic research (Markus, Berlin): local conventions matter more than price [S007] — not proven, to be tested by experiment.

**Segment B — local-language job seekers in DE/FR/ES (waves 2–3).**
Non-IT and junior job seekers; the local language and conventions are mandatory for them: the tabular Lebenslauf with a photo [C017], lettre de motivation [C018], the Spanish CV [C019] (all A). They pay competitors €9.99–23/mo [C022][C023][C024]. For this segment, XING's free offering in DE sets the bar: the basic function must be free [C021].

**Segment C — the OSS/self-host audience (already present; a channel for wave 1).**
Privacy-first developers; the niche ceiling is 45.5k Reactive Resume stars [C032] (A); channels: Show HN (656/240 points for analogues [C075], A), GitHub, r/cscareerquestionsEU ~179,000 subscribers [C074] (C). This audience delivers the first installs, stars, and content proof for waves A/B.

Persona table (segments A/B/C from 02):

| | **A — tech job seekers DE/NL/SE (EN professionals), wave 1** | **B — local-language job seekers DE/FR/ES, waves 2–3** | **C — OSS/self-host audience (channel)** |
|---|---|---|---|
| **Who are they?** | 25–40 years old, searching for 1–6 months, international companies; in SE English is the IT norm [C020], in NL tech runs in English (hypothesis [C043]) | non-IT and junior; the local language and conventions are mandatory: the tabular Lebenslauf with a photo [C017], lettre de motivation [C018], the Spanish CV [C019] | privacy-first developers; the niche ceiling is 45.5k Reactive Resume stars [C032] |
| **What do they use today and why?** | LinkedIn/Indeed + Word templates; global builders when necessary — but USD billing [C025] is irritating | the local clones CVMaker €21.99 [C022] / CVDesignR €9.99 [C023] / LiveCareer PL 99 zł [C024]; XING free [C021] | Reactive Resume/self-host; they filter vacancies manually — no filtering product exists in the niche |
| **What difficulties do they face?** | noise of irrelevant vacancies; ATS rejections without explanation; auto-renewals after trial-trap | interface language and conventions (photo, tabular format); fear of auto-charges | a manual process; no server-side hosted filtering |
| **Shared difficulty** | distrust of "yet another builder" because of the trial-trap experience (€1.99 → €21.99 [C022]) — shared across A/B | | |

### 2.2 Barriers at each journey stage

| Journey stage | Barrier today | What the product does |
|---|---|---|
| Acquisition | the DE/NL SERP is densely occupied by clones and government tools [02, Q4] | OSS distribution (Show HN/GitHub) for C→A; long-tail DE SEO "kostenlos/ohne Abo" [C076] |
| Choice / usage | fear of auto-renewals and of sending data to someone else's cloud | an honest free tier without a card; local-first; transparent prices, one-click cancellation |
| Payment | DE: 77% prefer PayPal [C030]; PL/ES methods — no data (gap) | PayPal + local methods via an MoR; regional price A/B at validation [06] |
| Post-payment experience | value drops after hiring; seasonality of job search | vacancy→resume→application tracker in one loop; a renewal reminder, no auto-charges |

What holds users back from starting or renewing? (by segment):

| Segment | Deterring factor | How it is removed |
|---|---|---|
| A (tech EN) | distrust of subscriptions after trial-trap; "why pay, Word exists" | free without a card; job scanning (value beyond a template); open source |
| B (local-language) | the competitors' price of €9.99–23/mo against the XING-free bar [C021]; our conventions absent at launch | a free tier with basic conventions; Pro €9–12 — below the clones; wave 2 after the DE conventions |
| C (OSS) | "self-host is enough" | hosted value: server-side filtering of 129+ boards, updates, zero setup |

Prioritization by capacity / CAC / competition (the calculation behind the conclusion below):

| Segment | Capacity | CAC (cash) | Competition | Verdict |
|---|---|---|---|---|
| A | DE 109k unfilled IT vacancies [C011] + NL 15.1k ICT [C012] + SE 8.6% ICT employment [C010] | ≈ 0 — organic (OSS, EN SEO, Reddit ~179k [C074]) | medium (global builders without job scanning) | **wave 1** |
| B | FR 42.6k hiring projects [C013] + ES ~120k tech [C014] | paid SEO + MoR fees | high locally (clones with conventions) | **waves 2–3** — after the conventions |
| C | niche ≤ 45.5k stars [C032] | ≈ 0 | low (OSS builders without filtering) | **already present** — a channel for A |

> **Conclusion (inference):** segmentation by entry barrier; the tier ladder serves every barrier; prioritization — by capacity/CAC/competition (the calculation is above): wave 1 = segment A (maximum capacity at zero cash CAC and incomplete competition), C — the product-validation channel, B — after the local conventions are covered.

## FAQ-3. Strategic initiatives. Briefly justify each.

### Options: Taking cvstart.org to the European market

> 5 substantively different options. Numbers carry [C###] tags. Context: a solo developer, no budget, ~5–10 hrs/wk [C059]; the product is free MIT, there is no hosted version [C005][C006]; 19 locales [C007]; the goal — audience growth in Europe, then monetization (a continuation of the global option B — a hosted freemium SaaS).

#### Option A: Keep things as they are

**The gist.** No targeted European entry: the OSS project grows through global channels (GitHub, occasional HN), Europe arrives passively via hreflang across the 19 locales [C007].
**What must be true.** Global EN traffic converts to installs without local actions; the locales are already indexed.
**Effect.** (forecast, low precision) Stars 96 → ~150–400 in a year (a comparable OSS grew to 45k in 6 years with major Show HN hits [C032][C075] — without effort the pace is orders of magnitude lower); revenue 0.
**Costs and revenue.** ~€0; maintaining the status quo; no revenue.
**Risks.** The "honest free" niche in DE will be taken: XING is already free [C021] (B); the SEO windows hold the clones [C022][C026]; the window before monetization narrows.

##### Objections

- "19 locales without local promotion are dead weight": hreflang brings impressions, but the DE/NL SERPs are occupied by paid SaaS and government tools.
- "The owner's request is not fulfilled": this is not an answer to "how do we enter the European market" but a refusal to answer it.
**What would falsify the option.** Search Console data: organic traffic from DE/FR/ES grows faster than global traffic without any action — then entry happens on its own.

#### Option B: "Light entry" — the OSS community of EN Europe (NL/SE/PL-tech)

**The gist.** Focus only on the EN audience: a Show HN launch, answer-first in r/cscareerquestionsEU (~179k, +15.5%/yr [C074]), GitHub trending. No convention localization, no monetization now.
**What must be true.** [C075] (A) Show HN provides the start (656/240 points for analogues); NL/SE tech works in English as the norm [C020] (A); [C043] the EN interface is sufficient.
**Effect.** (forecast) Stars 96 → 500–1500 over 6 months with 1–2 successful HN/Reddit waves; the first "Hired" cases; monetization is not launched.
**Costs and revenue.** ~5 hrs/wk, €0; revenue 0.
**Risks.** The ceiling of the EN-tech segment; the Nordics +28% WTP [C029] goes unused (nothing to sell); the "Europe" question is half-answered.

##### Objections

- "This is not a European strategy but a global EN strategy with a European accent" — for the DE/FR/ES segments (the local language is mandatory [C017–C019]) it does nothing.
- "Community channels do not grow without a product story": without "Hired" stories the content for Reddit/HN is thin.
**What would falsify the option.** The HN/Reddit waves deliver no sustained lift (a spike → back to the baseline) — the channel does not work.

#### Option C: Three-wave entry with an "honest free" tier and deferred monetization (recommendation)

**The gist.** Wave 1 = DE+NL+SE: OSS channels (B) + DE SEO for "Lebenslauf erstellen" positioned as "free, no auto-renewals" against trial-trap [C022][C024][C026]; the local conventions of the DE template (the tabular Lebenslauf, Anschreiben [C017]); a GDPR-ready cloud architecture is built in from the start (EU hosting from €3.79/mo [C062], SCC for US LLM APIs [C036]). Wave 2 = PL (growth +44% [C016], the regional price set by A/B). Wave 3 = FR/ES (the language is mandatory [C018][C019]). Hosted monetization in EUR — the gate after wave 1: launch only with confirmed conversions (the 180-day gate); Pro €9–12 / Unlimited €25–29 prices (the CVDesignR €9.99 [C023] ↔ resume.io €24.95 [C026] corridor), VAT via Non-Union OSS or an MoR [C037].
**What must be true.** [C048] the trial-trap backdrop makes "free + honest" a differentiator; [C043] EN is enough for NL/SE; the SEO volume of the DE keywords is material (a gap — verify with Keyword Surfer before launch); the DE local conventions are implementable within the 19-locale architecture [C007].
**Effect.** (forecast) W1 (6 months): stars 96 → 400–1000; DE-SEO organic from a zero DR — a lower bound of 500–2000 visits/mo by month 6 with good content (low confidence, D); launching the hosted version in months 6–8 → by month 12, per the global model, ~50–80 paying users (MRR €1.3–2k) at organic CAC (low confidence — a carry-over of demo assumptions).
**Costs and revenue.** Time 5–10 hrs/wk; infra €5–20/mo; revenue 0 until the hosted gate; afterwards — per the model.
**Risks.** SEO against clones with budgets — a low probability of top-3 in DE; overextension across 3 waves on solo resources; the hosted version may never get built (the main execution risk); an early check on day 90 would produce a false negative for the SEO channel (see the red-team objections).

##### Objections

- "SEO against resume.io/livecareer — losing on DR": most likely long-tail and comparison pages ("a free alternative to CVMaker"), not head keywords; meanwhile the "honest free" promise is invisible at top-of-funnel — a searcher for "Lebenslauf erstellen" does not yet know about trial-trap, and the free slot is taken by XING [C021] → lean on the "kostenlos/ohne Abo/Alternativ" modifiers and comparison pages; verify the volume with Keyword Surfer before launch.
- "5–10 hrs/wk cannot cover 3 countries, or even wave 1": the wave-1 budget is ≈ 160+ hours (DE templates ~40 hrs, content ~50 hrs at a realistic output of 1–2 articles/mo, community ~50 hrs, GDPR architecture ~30 hrs) against 130–260 hours available over 6 months → a WBS with a fixed cutting priority: cut content volume first, then the FR/ES groundwork, never the DE local conventions (without them traffic does not convert [C017]).
- "The 90-day gate kills our own SEO channel": by day 90 at DR≈0 there will be neither 1,000 visits nor rankings → the wave-1 gate is redefined: a 180-day window, the metrics — Search Console indexing and impressions + exported CVs/mo (the NSM in audience units, not stars); conversion is secondary.
- "MRR requires an auto-renewing subscription — the trial-trap mechanics we stand against": the monetization model is compatible with the positioning — no auto-charges: an annual subscription with an end-of-term reminder and/or credits/one-off packs; the price corridor [C023][C026] is recalculated in a single unit (per month at honest renewal).
- "The PL/ES data are hypotheses [C044]": hence PL as wave 2 with an A/B price, FR/ES as wave 3.
**What would falsify the option.** Over 180 days, no indexing and no impression growth on the DE/NL/SE pages despite an executed content plan; or exported CVs/mo < 50 at 500+ visits → the channel and the positioning are rebuilt (fall back to option B/E).

#### Option D: Commerce-first — hosted in EUR right away

**The gist.** Build the hosted version as the first step and launch the paid wave in the EU immediately: Free BYOK / Pro €12 / Unlimited €29, an MoR handles VAT [C037], GDPR from day one, PayPal payments for DE [C030].
**What must be true.** We can build hosted solo and fast; the "$0 forever" trust [C005] survives the change; an organic base accumulates before the commercial launch.
**Effect.** (forecast) Faster to MRR (months 4–6 instead of 8–12), but with CAC and no audience — paid traffic is ruled out by budget [C059], so growth = the same organic traffic with a paid paywall on top of a cold audience.
**Costs and revenue.** 15–25 hrs/wk on hosted (the realism for a solo dev is in question); infra €10–40/mo.
**Risks.** Breaks OSS trust at the start (cloud announcements at 96 stars); no base for conversions; the technical debt of LLM inference.

##### Objections

- "96 stars — no audience to launch to": conversion to paying users from cold traffic is near zero, and MoR fees will eat the micro-flows.
- "Building hosted before demand is confirmed inverts validation": the global plan gates the beta first, then the waves.
**What would falsify the option.** The appearance of a hosting partner/funding — then the solo-time constraint is lifted.

#### Option E: Close / wind down the European direction — focus on global EN (US)

**The gist.** Redirect the 5–10 hrs/wk to the US global segment (the same OSS mechanics as B, without the European focus); Europe stays passive. This is the "closing" of the European direction as a priority.
**What must be true.** The US segment is more accessible at the same effort (a single EN, a larger volume [C031] ~673k/mo globally).
**Effect.** (forecast) Global EN traffic grows faster per unit of effort; the European request is postponed.
**Costs and revenue.** the same 5–10 hrs/wk, €0.
**Risks.** US competition is denser (all 7 global players are there); abandoning the DE/PL windows where competitors are less localized [C009].

##### Objections

- "Our non-EN locales are an asset that does not work at all under a US focus": abandoning a differentiator [C007][C009].
- "The 19 locales get indexed without us" — but there is no conversion without the local conventions [C017].
**What would falsify the option.** If the US channels deliver ≤ the global baseline without focus, the option loses its meaning; and if the owner treats Europe as a strategic goal (the brief), the option contradicts it.

#### Comparison

| Criterion (from the brief) | Weight | A | B | C | D | E |
|---|---|---|---|---|---|---|
| Growth of the European audience over 12 months | high (owner goal C [C060]) | 1 | 3 | 5 | 3 | 1 |
| The path to EUR monetization | high (goal C) | 1 | 2 | 4 | 5 | 2 |
| Solo feasibility at 5–10 hrs/wk | critical [C059] | 5 | 5 | 3 | 1 | 5 |
| Risk to OSS trust/community | high (the product's core [C005]) | 5 | 5 | 4 | 2 | 5 |
| Fit with the "Europe" request | high (the brief) | 1 | 3 | 5 | 4 | 1 |
| Sum (unweighted — the weights are qualitative) | — | 13 | 18 | 21 | 15 | 14 |

Scale 1–5: 5 — good. The weights are not numeric: "feasibility" and "trust risk" are filters (an option scoring 1–2 is screened out), the rest are ranking criteria.

#### Red-team objections that changed the options

**A.** The MIT license turns passivity into subsidizing competitors (a fork + hosted + trial-trap on your code); 19 thin locales are maintenance debt and a Google scaled-content penalty risk; even the DE/FR/ES traffic that does arrive does not convert without local conventions [C017–C019] — traffic growth without product = zero and negative behavioral signals.
**B.** Show HN is a lottery with reposts banned; the star forecast is conditioned on uncontrollable success; retention after the spike is unverified; EN-tech NL/SE is a LinkedIn-centric market where the CV is secondary (the JTBD is "get a referral"); segment B's audience structurally does not pay: everyone has a free self-host, and the Nordics +28% WTP [C029] is a consumer metric, not OSS enthusiasts.
**C.** The 90-day gate would shoot at our own SEO channel → redefined (180 days, impressions/indexing/CV exports). The "honest free" promise is invisible at top-of-funnel, and XING already offers free in DE [C021] → lean on the "kostenlos/ohne Abo" modifiers and comparison pages. The hour budget of wave 1 was contradictory → a WBS with a fixed cutting priority. The MRR model is incompatible with the anti-trial-trap stance → monetization without auto-charges (annual/credits), prices in a single unit.
**D.** A solo operator of EU citizens' PII carries personal liability (Art. 82 GDPR); cheap shared hosting from €3.79 [C062] is not PII-grade; at an honest 5–10 hrs/wk a hosted MVP is 300–500 hours ≈ 30–50 weeks, "speed" evaporates and D becomes C without gates (strictly dominated); Free BYOK filters out non-IT payers — D has no viable free tier for its own paying segment.
**E.** The EN position is taken by Reactive Resume (45k stars [C032], the same MIT, hosted free) — E competes for what is left after the leader; the US has a surplus of job seekers and AI autofill, the worst pain/competition ratio against DE with its 109k unfilled [C011]; the US also requires template work on conventions, which E was specifically avoiding.

##### Hidden assumptions of the panel (verify before/at launch)

1. **Stars ≠ job seekers.** The whole panel measured success in GitHub stars — a vanity metric: developers give stars, a German job seeker pays. The NSM is fixed in audience units: exported CVs/mo per locale. [C052]
2. **Content throughput.** Realistically 1–2 articles/mo at 5–10 hrs/wk alongside code and support; DE requires native German (machine translation is down-ranked by Google). Workflow: an AI draft + human review by a native speaker.
3. **Are "free forever" and a paid hosted version compatible?** Changing the public OSS contract triggers revolts/forks; the risk is expert-judged. Mitigation: an analysis of the transitions of Reactive Resume/Cal.com/Plausible + preemptive positioning of "OSS free forever, hosted — paid convenience" and a test of it on the current core (96 stars) before monetization launches. [C053]

#### Recommendation

Option C (as revised after the red team), because: (1) it is the only option that simultaneously grows the European audience and keeps the path to EUR monetization with realistic gates; (2) it rests on confirmed facts: the trial-trap backdrop [C022][C024][C026], the DE/FR/ES languages [C017–C019], cheap EU hosting [C062]; (3) it fits the solo resource thanks to the waves, a WBS with a fixed cutting priority, and the 180-day gate on impressions/CV exports [C052]. Conditions for changing the recommendation: Keyword Surfer shows negligible DE/NL/SE volumes (SEO drops out → a B+C hybrid with SEO moved to wave 2); the owner demands monetization immediately (then D, with full awareness of the PII risk and dominatedness); the 180-day gate of wave 1 fails (fall back to option B/E). Mandatory pre-checks before launch: a test of "OSS free forever + hosted for money" on the current community and an audit of locale non-indexing in Search Console.

### Initiatives of the chosen direction (drivers)

**First driver — OSS launch** (Show HN + GitHub + DE landing): zero cash CAC, the C→A starter flow. Comparable launches scored 656/240 points on Show HN [C075]; niche ceiling 45.5k stars [C032]. Effect: 1,000+ installs/month and content proof by day 60 (milestone M2).

**Second driver — long-tail DE SEO** ("kostenlos/ohne Abo" against the trial-trap): head cluster "lebenslauf erstellen" KD 57, 49,500 on the no-space variant [C076]; 6–12 articles (WBS P2). Effect: 5,000+ impressions/mo by day 150 (gate H2), ~3% CTR → ~150 visits/mo.

**Third driver — DE conventions + GDPR architecture**: tabular Lebenslauf with photo [C017], EU hosting from €3.79/mo [C062][C073]. Effect: unlocks segment B (wave 2–3: FR 42.6k [C013], ES ~120k [C014]) — a market opener, not a direct wave-1 traffic driver.

**Fourth driver — 180-day hosted gate**: NSM ≥ 50 CV exports/mo [C052] + indexation. Effect: insurance for decision D001 — if the gate fails, roll back to B/E without spending on monetization.

**Step-by-step effect calculation (wave 1):** start — OSS channel: 1,000 visits/mo × 5% activation = 50 CV exports → NSM target for months 1–3 met organically; SEO accumulation by day 150: +5,000 impressions → +150 visits/mo → ≥ 50 CV/mo with headroom from a single channel; by day 180 the gate: NSM ≥ 50 (base 50 from OSS + SEO cushion) → decision on stage 2 (hosted EUR).

> **Inference:** the four drivers cover the entire wave-1 path: OSS gives a fast start at zero CAC, SEO a scalable compounding flow, conventions the ticket to wave 2, the gate decision discipline. No driver requires budget; risk concentrates in activation conversion, which H1 tests before major time investments.

Unit economics — the step-by-step calculation:

Assumptions: unit assumptions [C057]: ARPU €25 (Unlimited; the CVDesignR €9.99 [C023] ↔ resume.io €24.95 [C026] corridor); variable costs 25%; churn 8%/mo. CAC €30 — an assumption for the sensitivity of the paid scenario; the cash CAC of organic ≈ 0 [04_product_strategy]. Not confirmed for the EU — to be verified at validation [06_validation_plan]

| Formula | Calculation | Result |
|---|---|---|
| CM = ARPU × (1 − variable share) | 25.00 × (1 − 0.25) = 25.00 × 0.75 | **CM = 18.75** |
| Average paying lifetime = 1 / churn | 1 / 0.08 | **12.50 months** |
| LTV = CM / churn | 18.75 / 0.08 | **LTV = 234.38** |
| LTV/CAC | 234.38 / 30.00 | **7.81** (criterion ≥ 3) |
| CAC payback = CAC / CM | 30.00 / 18.75 | **1.60 months** |

**Conclusion (inference):** LTV/CAC ≥ 3 holds up to churn ≈ 20.83%/mo, up to CAC ≈ €78.12, and up to a variable-cost share ≈ 61.60% (each threshold — all else equal; the grid is on the "Sensitivity" sheet).

## FAQ-4. Tactics. Detail each initiative down to specific tactics.

### Product strategy: Taking cvstart.org to the European market (option C)

> Basis: the owner's choice — the three-wave entry [03_options]; the market's trial-trap backdrop [C022][C024][C026]; the DE/FR/ES languages [C017–C019]; solo resources [C059].

#### Audience and its job

**The core of wave 1 — tech job seekers in DE/NL/SE (EN professionals), 25–40 years old.**
Size: DE — 109,000 unfilled IT vacancies (2025) [C011] (B); NL — 622,000 ICT specialists [C012] (A); SE — 200,000+ employed in tech, +18,000/yr [C015] (B). In SE English is the IT norm [C020] (A), in NL it is the working norm (hypothesis [C043]).

JTBD: "When I look for a job in Europe, I want to filter the real vacancies from all sources and quickly produce a resume for each one that passes ATS — without manual routine, auto-renewals, or sending my data to someone else's cloud." The job is done when the job seeker has an exported resume for a specific vacancy and understands why the application is relevant.

**The second circle of wave 1 — the OSS/self-host audience (a growth channel, not the monetization focus)**: a niche potential of 45k stars [C032] (A), the Show HN/Reddit channels [C075][C074].

**Waves 2–3 — PL, then FR/ES**: local-language job seekers paying competitors €9.99–23/mo [C023][C024]; PL — vacancy growth +44% [C016] (C).

#### Alternatives

| How it is solved today | Why chosen | Weakness | Source |
|---|---|---|---|
| XING Lebenslauf (DE) | free, built into a familiar service | only the Lebenslauf: no vacancy scanning, tracker, or multiboard | [C021] (B) |
| Local clones (CVMaker, LiveCareer PL) | the local language, SEO visibility | a €1.99–2.95 trial → a €21–25/4-weeks auto-renewal | [C022][C024][C026] (B) |
| Global (resume.io, Teal, Zety) | brand, templates | USD billing [C025][C027], trial-trap, thin locales [C009] | (A/B) |
| Europass (government, EU) | free, multilingual | a universal template that fails local ATS conventions, no AI | observation (C) |
| ChatGPT manually | free, flexible | no job scans, tracker, or format-specific templates | [C004] |
| Nothing (a Word template) | habit | manual routine, no vacancy scoring | — |

#### Chosen direction (option C from 03_options)

The bet: **occupy the "free, honest, local" corner in wave 1 (DE+NL+SE) through the OSS community + long-tail DE SEO, with a 180-day gate before EUR monetization without auto-charges.** Why: the only option that grows the audience while preserving the path to EUR revenue on solo resources; it rests on the confirmed trial-trap backdrop and the unoccupied honest-free slot (except XING, which has no job scanning) [C048].

Outcome roadmap (outcomes, not features):
- **Stage 1 (months 0–6), the DE+NL+SE wave:** DE templates of local conventions (the tabular Lebenslauf + Anschreiben) [C017]; 10–12 long-tail articles ("kostenlos", "ohne Abo", "Alternative zu CVMaker/resume.io"); an OSS launch (Show HN, answer-first Reddit, GitHub). **The result by day 180:** indexed DE/NL/SE pages, growing Search Console impressions, NSM ≥ 50 exported CVs/mo, stars 400–1000. Gate passed → stage 2; failed → fall back to option B/E.
- **Stage 2 (months 6–12):** a community test of "OSS free forever + hosted for money" on the current core [C053] → launch the hosted version: Free (BYOK) / Pro €9–12 / Unlimited €25–29 — a subscription without auto-charges: annual with a renewal reminder and one-click cancellation (or monthly cancel-anytime with the same reminder); one-off credits as an alternative [C052][C053]; an MoR or Non-Union OSS [C037]; EU hosting [C062]; a regional price A/B + the start of the PL wave (the PL locale exists [C007]).
- **Stage 3 (months 12+):** the FR/ES wave after the PL conversion is confirmed; the local conventions lettre de motivation / CV español [C018][C019]; content scaling.

#### Deliberate non-goals

- **No paid promotion** — there is no budget [C059].
- **No auto-renewals in any form** — that is the competitors' mechanics we stand against; it burns the positioning [C052][C053].
- **No FR/ES in wave 1** — the language is mandatory [C018][C019], the conventions are expensive; queuing by gates.
- **No US focus** — the EN position is taken by Reactive Resume [C032], a surplus of job seekers; the locales do not work in the US.
- **No B2B/white-label or dual licensing** — rejected by the global plan's red team (no sales competency; legally unsound on top of MIT).
- **No promising an "ATS-pass guarantee"** — we promise transparency of methodology, not outcomes.
- **No building hosted before the stage-1 gate and the community test** — an inversion of validation and a trust risk [C053].

#### Economics (forecast; the ranges carry over global-model assumptions, low confidence)

- **Before monetization (months 0–6):** costs = time 5–10 hrs/wk [C059] + infra from €3.79/mo [C062]. Revenue 0.
- **After hosted (months 6–12):** revenue = paying users × ARPU. Unit assumptions [C057] (carried over from the global plan, not confirmed for the EU): ARPU €25 (Unlimited), variable costs (inference+infra+MoR) ~25% → CM ≈ €18.75; fixed costs ~€150/mo → break-even ≈ 8 paying users against fixed costs; at ARPU €12 (Pro-only) CM ≈ €9 → ≈ 17 paying users. Churn 8%/mo (assumption [C057]) → LTV ≈ €234 at ARPU €25. The cash CAC ≈ 0 (organic); the real cost is time.
- **The forecast by month 12:** 50–80 paying users, MRR €1.3–2k (low confidence: global assumptions carried over to the EU; the PL/ES WTP is unconfirmed [C044]). Sensitivity analysis is mandatory in the validation plan.
- **Honest units:** prices are compared in a single unit (€/mo at honest renewal), without mixing the 4-week subscription and one-off packs [C052].

#### Metrics

- **NSM: exported CVs/mo per locale** [C052] — units of the target audience, not stars.
- Tree: visit → install/signup → activation (the first CV import) → CV export → (after hosted) payment.
- Channel metrics: Search Console impressions/indexing (SEO), stars/forks (the OSS channel — vanity, auxiliary), 30-day retention after the HN/Reddit waves.
- Counter-metrics: star/fork churn after the monetization announcement; GDPR requests > 5; DE-page bounce > 80%; free-tier inference costs > €200/mo; NPS < 30 [C057].

#### Risks and mitigation

| Risk | Probability | Impact | Mitigation | Early signal |
|---|---|---|---|---|
| DE SEO volumes negligible / the Domain Rating is too low to rank | medium | high | a Keyword Surfer pre-check before launch; a shift to community and PR (heise [C035]) | zero indexing within 60 days |
| Solo overload (the hour budget: 160+ hours against 130–260 hours available [C056]) | high | high | a WBS with a fixed cutting priority: content → the FR/ES groundwork → never the DE conventions | the weekly plan missed twice in a row |
| A community revolt at monetization | medium | high | a preemptive positioning test on the core [C053]; the OSS core stays MIT/free [C005] | −10% stars / negativity in issues |
| A GDPR incident on hosted | low | critical | SCC+TIA for US LLM APIs [C036], EU hosting [C062], a 72-hour incident plan before the first user | GDPR requests, complaints |
| Hosted never gets built | medium | high | the stage-2 scope fixed before launch (MVP: auth+payment+inference), 15–20 hrs/wk for 8 weeks | 2 sprints late |
| The PL/ES WTP below the model | unknown | medium | a regional price A/B [C044]; waves 2–3 launch only after wave 1 | PL conversion < 50% of DE |

Tactics matrix (from the outcome roadmap, 04_product_strategy.md):

| Strategic initiative | Focus | User needs and expectations | Solutions (tactics) |
|---|---|---|---|
| Stage 1 (months 0–6), the DE+NL+SE wave | DE templates of local conventions (the tabular Lebenslauf + Anschreiben) [C017] | — | DE templates of local conventions (the tabular Lebenslauf + Anschreiben) [C017]; 10–12 long-tail articles ("kostenlos", "ohne Abo", "Alternative zu CVMaker/resume.io"); an OSS launch (Show HN, answer-first Reddit, GitHub). **Result:** indexed DE/NL/SE pages, growing Search Console impressions, NSM ≥ 50 exported CVs/mo, stars 400–1000. Gate passed → stage 2; failed → fall back to option B/E. |
| Stage 2 (months 6–12) | a community test of "OSS free forever + hosted for money" on the current core [C053] → launch the hosted version: Free (BYOK) / Pro €9–12 / Unlimited €25–29 — a subscription without auto-charges: annual with a renewal reminder and one-click cancellation (or monthly cancel-anytime with the same reminder) | — | a community test of "OSS free forever + hosted for money" on the current core [C053] → launch the hosted version: Free (BYOK) / Pro €9–12 / Unlimited €25–29 — a subscription without auto-charges: annual with a renewal reminder and one-click cancellation (or monthly cancel-anytime with the same reminder); one-off credits as an alternative [C052][C053]; an MoR or Non-Union OSS [C037]; EU hosting [C062]; a regional price A/B + the start of the PL wave (the PL locale exists [C007]). |
| Stage 3 (months 12+) | the FR/ES wave after the PL conversion is confirmed | — | the FR/ES wave after the PL conversion is confirmed; the local conventions lettre de motivation / CV español [C018][C019]; content scaling. |

## FAQ-5. High-level plan

### 06 · Validation plan — Taking cvstart.org to the European market (option C)

> The riskiest hypotheses go first. All checks are budget-free: time + the existing product.

#### Expected change (summary)

| # | Hypothesis | Metric | Expectation at the decision point |
|---|---|---|---|
| H1 | The "honest free" tier converts against trial-trap [C051] | NSM: exported CVs/mo | ≥ 50/mo by day 180 |
| H2 | The DE SEO channel works at DR≈0 [C052] | SC impressions/indexing | > 5,000 impressions/mo by day 150; indexing ≥ 80% |
| H3 | EN is enough for NL/SE [C043] | the NL/SE vs DE conversion | EN ≥ 50% of DE |
| H4 | The community will accept monetization [C054] | sentiment/star churn | churn < 10%/mo |
| H5 | Regional prices PL/ES [C044] | revenue/visitor PL | ≥ +20% vs a single price |

#### Comparison base (summary)

- H1: the base is ~0 (no telemetry → an opt-in export counter or release statistics as a proxy); an external anchor — the 2–5% freemium conversion [C051]; a passive control — the DE/FR/ES locales without content. Before/after.
- H2: base 0; the internal control — NL/SE pages without content (the passive hreflang effect).
- H3: a rotational A/B/C of the nl/sv/en pages from the 19 locales [C007].
- H4: the external base — the star trends of Reactive Resume/Cal.com/Plausible around monetization announcements.
- H5: a geo-price A/B via an MoR; the base — PL conversion at a single price (the first 30 days of wave 2).

#### H1. The "honest free" tier converts against the market's trial-trap (the main wave-1 hypothesis)

- **Expected change** [C051]: the NSM — exported CVs — from ~0 to **≥ 50/mo by day 180** summed across DE/NL/SE; the visit → first export conversion ≥ 5–10%. Why expected: the trial-trap backdrop [C022][C024][C026] and a free competitor without vacancy scanning [C021].
- **Comparison**: the base — current telemetry is absent → first implement privacy-friendly export counting (a local opt-in option for an anonymous counter, or GitHub release statistics as a proxy); the external anchor — the 2–5% freemium conversion (a niche benchmark, hypothesis [C051]). Before/after: the DE/FR/ES locales as a "passive control" (their content is untouched in wave 1).
- **Window**: 180 days (the wave-1 gate) with early signals at 60/90/120 days. Sample: at 1,000 visits/mo and a 5% expectation, 50 exports/mo is enough to read the trend; statistical rigor is not required — decisions are made on thresholds.
- **Counter-metrics** [C057]: DE-page bounce > 80%; GDPR requests > 5; NPS < 30 — a stop-and-adjust signal, not growth at any cost.
- **Criteria**: **continue** NSM ≥ 50/mo by day 180 → stage 2 (the hosted gate); **adjust** 20–50/mo → rebuild the channels (SEO ↔ community) and the message (a headline A/B), extend the gate by 90 days once; **stop** < 20/mo at 500+ visits/mo → fall back to option B/E, the SEO content is mothballed.
- **Type**: an MVP wave (real product + content), cost €0, owner — the founder.

#### H2. The DE SEO channel works at DR≈0 (the channel hypothesis)

- **Expected change** [C052]: DE-page Search Console impressions from 0 to **> 5,000/mo by day 150**, indexing ≥ 80% of the published pages (10–12 long-tail: "kostenlos", "ohne Abo", "Alternative zu …").
- **Comparison**: base 0 (a new channel); the internal control — NL/SE pages without content (do they grow passively from hreflang).
- **Window**: 60 days — an early signal (indexing), 150 days — impressions, 180 — clicks.
- **Counter-metrics**: the "Crawled – not indexed" share > 50% → thin content (a scaled-content risk [red team A]); no top-30 positions on long-tail by day 150.
- **Criteria**: **continue** indexing ≥ 80% and impressions growing; **adjust** indexing present, no impressions → rebuild the semantics (Keyword Surfer) and headlines; **stop** no indexing within 60 days despite an executed plan → close the channel, shift the hours to community/PR (heise [C035]).
- **Type**: a content pilot, cost €0 (time), owner — the founder.

#### H3. EN sufficiency for NL/SE (hypothesis [C043])

- **Expected change**: the NL/SE conversion of the EN landing ≥ 50% of the DE conversion (EN is no worse than local for these markets).
- **Comparison**: A/B/C — the NL (nl) / SE (sv) pages from the 19 locales [C007] against EN — rotating headlines and hreflang priority weekly; seasonality is not critical (job-search periods are stable within 90 days).
- **Window**: 90 days, a 3×30 rotation.
- **Counter-metrics**: the NL/SE bounce > 85% — a signal that the issue is not language but conventions.
- **Criteria**: **continue** EN ≥ 50% of DE → wave 1 proceeds without NL/SE convention localization; **adjust** 30–50% → add NL/SE local templates before scaling; **stop** < 30% → NL/SE moves to wave 2 with localization.
- **Type**: a rotational A/B on the live site, €0, the founder.

#### H4. The community will accept future monetization (checked BEFORE hosted)

- **Expected change** [C054]: a Discussions post — "the OSS stays free forever (MIT), hosted is paid convenience, no auto-renewals" — the core's reaction (96 stars): ≥ 0 aggregate sentiment, star churn < 10%/mo after the announcement, a minimal number of "unstars".
- **Comparison**: the transition cases of Reactive Resume / Cal.com / Plausible (an analysis of their star trends around announcements) as the external base.
- **Window**: 2 weeks for the reaction + 30 days for churn.
- **Counter-metrics**: > 3 harsh negative issues / a fork wave → rebuild the monetization positioning before code.
- **Criteria**: **continue** a neutral/positive reaction → stage 2 starts; **adjust** mixed → change the contract wording (credits vs subscription) and repeat; **stop** a revolt → monetization is postponed, OSS-first continues (option B).
- **Type**: a public-contract test, €0, the founder.

#### H5. Regional prices PL/ES (wave 2, after the H1 gate)

- **Expected change** [C044 hypothesis]: a regional price (PL ≈ 60–70% of the base EUR) raises PL conversion ≥ 1.3× against a single price.
- **Comparison**: an A/B via an MoR (two prices by geo); the base — PL conversion at a single price in the first 30 days of wave 2.
- **Window**: 60 days (a billing cycle of a month + renewal).
- **Counter-metrics**: ARPU falls faster than conversion grows (revenue/visitor declines) — roll back the price.
- **Criteria**: **continue** PL revenue/visitor grows ≥ 20%; **adjust** conversion grows, revenue does not — price in between; **stop** no difference — a single EUR price.
- **Type**: a pricing A/B, €0 (the MoR charges per transaction), the founder.

#### Observation window (summary)

| Check | Window | Why it is enough |
|---|---|---|
| H1 "free+honest" conversion | 180 days (the gate) + signals at 60/90/120 | the "visit → install → export" cycle is days; organic accumulation is months |
| H2 DE SEO | 60–180 days | indexing ~2–3 months, long-tail positions 3–6 months at DR≈0 |
| H3 EN NL/SE | 90 days, a 3×30 rotation | search seasonality is stable within a quarter |
| H4 community test | 2 weeks reaction + 30 days churn | the OSS-community reaction cycle |
| H5 PL prices | 60 days | a 1-month billing cycle + renewal |

#### Unintended consequences (stop thresholds) [C057]

- DE-page bounce > 80% or GDPR requests > 5 → stop scaling content, review quality.
- "Crawled – not indexed" > 50% → a scaled-content signal, rebuild the content to native DE.
- Star churn ≥ 10%/mo or > 3 harsh negative issues after the monetization announcement → rebuild the public contract before code.
- PL ARPU falls faster than conversion grows (revenue/visitor ↓) → roll back the regional price.
- Free-tier inference costs > €200/mo → the free economics break, revisit the BYOK limits.

#### Decision criteria (summary)

| Check | Continue | Adjust | Stop |
|---|---|---|---|
| H1 | NSM ≥ 50 exports/mo by day 180 → stage 2 | 20–50/mo → rebuild the channels/message, the gate +90 days (once) | < 20/mo at 500+ visits → fall back to option B/E |
| H2 | indexing ≥ 80%, impressions growing | indexing present, no impressions → rebuild the semantics | no indexing within 60 days → hours to community/PR |
| H3 | EN ≥ 50% of the DE conversion | 30–50% → local NL/SE templates | < 30% → NL/SE to wave 2 |
| H4 | a neutral/positive reaction | mixed → a different contract wording | a revolt → monetization postponed (B) |
| H5 | PL revenue/visitor ≥ +20% | conversion ↑, revenue flat → price in between | no difference → a single EUR price |

#### Review rule

Any counter-metric crosses its threshold [C057] → review the affected conclusions (`pfs impact`), a debrief in the weekly wave-1 rhythm. New data (Keyword Surfer volumes, WTP facts) → `pfs source add` + a rebuild of waves 2–3 without changing wave 1.

Expected contribution of the initiatives to the overall result (sums to 100%; an expert judgment by the drivers of 04, hours — the wave-1 WBS, revisited at the M2/M4 milestones):

- **35% — Long-tail DE SEO content** (16–48 hrs, WBS P2): the largest organic channel ("lebenslauf erstellen" KD 57, 49,500 for the no-space variant [C076]); the effect is cumulative, ramping from month 3.
- **25% — OSS launch** (Show HN + GitHub + a DE landing page, ~20 hrs, WBS P3): zero cash CAC, the first installs and content proof [C075]; the effect is a one-off spike + a long tail of links.
- **20% — DE conventions + GDPR architecture** (~50 hrs, WBS P1): a precondition for segment B (the tabular Lebenslauf with a photo [C017], EU hosting from €3.79 [C062][C073]); its contribution is that of the wave-2 "opener".
- **20% — Hosted gate and analytics** (the 180-day gate, the H1–H2 metrics, ~100 hrs of other WBS packages): without the gate there is no transition to monetization; its contribution is the "insurance" of decision D001.

Order of tactics: high → medium → base priority (see the WBS: P1 "never cut" → P2 → P3). Timing follows the market seasons: the January hiring peak in DE/SE — content accumulation by December, the hosted announcement in early January. Parallel tracks: community/partnerships — off the main line.

**Decision D002** — Pre-checks before the wave-1 launch (€0, 2 weeks). Interim review 2026-11-22; trigger: the SEO volumes are negligible → the SEO channel drops out, a B+C hybrid.

## FAQ-6. Success metrics. KPIs in two dimensions

| Plane | Hypothesis | Metric | Base → target by deadline | Action threshold (stop) |
|---|---|---|---|---|
| Product | H1 — The "honest free" tier converts against trial-trap [C051] | NSM: exported CVs/mo | base ~0 (no telemetry → an opt-in export counter or release statistics as a proxy) → ≥ 50/mo by day 180 | < 20/mo at 500+ visits → fall back to option B/E |
| Product | H2 — The DE SEO channel works at DR≈0 [C052] | SC impressions/indexing | base 0; the internal control — NL/SE pages without content (the passive hreflang effect). → > 5,000 impressions/mo by day 150; indexing ≥ 80% | no indexing within 60 days → hours to community/PR |
| Product | H3 — EN is enough for NL/SE [C043] | the NL/SE vs DE conversion | a rotational A/B/C of the nl/sv/en pages from the 19 locales [C007]. → EN ≥ 50% of DE | < 30% → NL/SE to wave 2 |
| Product | H4 — The community will accept monetization [C054] | sentiment/star churn | the external base — the star trends of Reactive Resume/Cal.com/Plausible around monetization announcements. → churn < 10%/mo | a revolt → monetization postponed (B) |
| Business | H5 — Regional prices PL/ES [C044] | revenue/visitor PL | a geo-price A/B via an MoR → ≥ +20% vs a single price | no difference → a single EUR price |

KPIs in two directions: **1) Business** — money and base (revenue/MRR, paying users, conversion to payment, the plan mix, the actual LTV/CAC); **2) Product** — activation, time to first value, the number of actions to result, churn, CSAT/NPS. Every KPI: base → target by deadline → action threshold. One counter-metric per red-team hit.

## Sources (footnotes)

1. **S001** — CVStart — the product site (the career-ops-ui landing): free OSS, a local mode, 19 locales — https://cvstart.org — 2026-11-08
2. **S002** — Competitors and prices: Kickresume/Rezi/Teal/Enhancv/Novoresume/Zety/resume.io — https://www.rezi.ai/pricing
3. **S003** — AI in job search 2025–2026: 31–74% of job seekers use AI — https://www.kickresume.com/en/press/ai-job-search-data/
4. **S004** — The resume builders market: a $1.2–2.4 billion corridor; the AI segment CAGR 13% — https://www.wiseguyreports.com/reports/resume-builder-market
5. **S005** — Online recruitment $37.97 billion (2025); ATS $2.5–3.3 billion — https://www.skyquestt.com/report/online-recruitment-market
6. **S006** — career-ops-ui README: features, stack, autotests, 19 locales — sources/raw/cvs_readme.md
7. **S007** — AI respondent: Markus, 35, PM (Berlin) — hypotheses of the EU/DE segment — sources/raw/persona-markus.md
8. **S008** — AI respondent: Sarah, 32, software engineer (US) — hypotheses of the EN segment — sources/raw/persona-sarah.md
9. **S009** — A synthetic hosted-beta funnel (12 weeks) — an illustration of the method — sources/raw/synthetic_funnel.csv
10. **S010** — Bitkom: 109,000 unfilled IT vacancies in Germany (2025) — https://www.bitkom.org/sites/main/files/2026-01/bitkom-studienbericht-it-fachkraefte-2025.pdf — 2025-12-15
11. **S011** — CBS (NL): 15.1k open ICT vacancies at the end of 2025; 622,000 ICT specialists — https://www.cbs.nl/nl-nl/longread/rapportages/2026/digitalisering-en-kenniseconomie-2025/2-ict-en-economie — 2026-01-01
12. **S012** — Insee (FR): the IT-engineer shortage indicator 1.1; 42,635 hiring projects — https://www.insee.fr/fr/statistiques/8616805?sommaire=8616883 — 2025-10-14
13. **S013** — DigitalES×COIT (ES): ~120,000 unfilled tech vacancies — https://www.coit.es/sites/default/files/digitales_anatomia_brecha_talento_tecnologico.pdf — 2024-06-01
14. **S014** — TechSverige (SE): +18,000 tech specialists per year through 2028 — https://techsverige.se/kompetensbehoven-inom-tech — 2024-01-01
15. **S015** — No Fluff Jobs (PL): +44% tech vacancies year over year — https://nofluffjobs.com/insights/raport-rynek-pracy-it — 2025-12-01
16. **S016** — EURES Germany: resumes and cover letters in German — https://eures.europa.eu/living-and-working/living-and-working-conditions-europe/living-and-working-conditions-germany_en
17. **S017** — EURES France: a CV and lettre de motivation in French — https://eures.europa.eu/living-and-working/living-and-working-conditions-europe/living-and-working-conditions-france_en
18. **S018** — EURES Spain: a CV and a letter in Spanish, A4 — https://eures.europa.eu/living-and-working/living-and-working-conditions-europe/living-and-working-conditions-spain_en
19. **S019** — EURES Sweden: the job-posting language decides; IT works in English as the norm — https://eures.europa.eu/living-and-working/living-and-working-conditions-europe/living-and-working-conditions-sweden_en
20. **S020** — XING Lebenslauf (DE): a free Lebenslauf builder + AI-Anschreiben — https://xing.com/lebenslauf — 2026-11-01
21. **S021** — CVDesignR (FR): Premium €9.99/mo with ATS analysis and AI — https://cvdesignr.com/fr/premium — 2026-10-01
22. **S022** — resume.io: USD billing, the local currency — display only — https://help.resume.io/en/articles/3785664 — 2026-11-01
23. **S023** — Teal: all prices in USD ($13 weekly/$29 monthly/$179 yearly) — https://help.tealhq.com/en/articles/9530153 — 2026-11-01
24. **S024** — resume.io EU prices: €2.95 for 7 days → €24.95 every 4 weeks — https://aivario.com/tools/resume-io — 2026-10-01
25. **S025** — Paddle: the Nordics pay +28% over the US price; local currencies add +5–25% to conversion — https://www.paddle.com/blog/saas-pricing-models-strategies-fltr — 2026-03-01
26. **S026** — Paddle: in Germany 77% prefer PayPal over cards — https://www.paddle.com/blog/average-revenue-per-paying-user-arppu-fltr — 2026-03-01
27. **S027** — Seopital: resume builder/cv maker ~673,000 queries/mo globally — https://www.seopital.co/blog/the-best-resume-builder-seo-keywords
28. **S028** — Reactive Resume (OSS MIT): 45,485 GitHub stars — https://api.github.com/repos/reactive-resume/reactive-resume — 2026-11-08
29. **S029** — Show HN: Open Resume — 656 points, 198 comments (2023) — https://hn.algolia.com/api/v1/items/36470297 — 2023-06-25
30. **S030** — Show HN: RxResume — 240 points (2020) — https://hn.algolia.com/api/v1/items/22709183 — 2020-03-28
31. **S031** — r/cscareerquestionsEU: ~179k subscribers, +15.5%/yr — https://www.gummysearch.com/r/cscareerquestionsEU — 2026-08-10
32. **S032** — EDPB: transfers outside the EEA require SCC 2021/914 (+TIA) — https://edpb.europa.eu/sme/be-compliant/international-data-transfers_en — 2025-01-01
33. **S033** — Stripe: a non-EU seller — Non-Union OSS from the first sale; the EU threshold is €10k — https://docs.stripe.com/tax/use-stripe-to-register/non-union-oss — 2025-01-01
34. **S034** — Hetzner CX22 €3.79/mo (DE/FI, a GDPR-compliant DC) — https://hetzner.com/pressroom/new-cx-plans — 2024-06-06
35. **S035** — Eurostat: 10+ million ICT specialists in the EU (2024), 5.0% of employment; SE 8.6% — https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20250708-2 — 2025-07-08
36. **S036** — CVMaker DE: €21.99/mo after €1.99 for 14 days (auto-renewal) — https://cvmaker.de/preise — 2026-11-01
37. **S037** — LiveCareer PL: 9.95 zł for 14 days → 99 zł every 4 weeks — https://livecareer.pl/cennik — 2026-11-01
38. **S038** — meinperfekterlebenslauf.de (DE): a local clone, "1+ million Lebensläufe" — https://www.meinperfekterlebenslauf.de — 2026-11-01
39. **S039** — heise.de: 5.68 million unique users (agma DNA, June–August 2026) — 2026-10-19
40. **S040** — Jobscan: 97.8–98% of the Fortune 500 use ATS (career-page reverse engineering) — https://www.jobscan.co/blog/fortune-500-use-applicant-tracking-systems/ — 2018-05-01
41. **S041** — Performance Suite keyword DB (updated 25.09.2026): DE query volumes of the Lebenslauf cluster — https://www.performance-suite.io/keyword-db/de-de/lebenslauf-erstellen/ — 2026-09-25
42. **S042** — Just Join IT 2026 report: 110,996 IT vacancies on the platform in 2025 (+8.42% y/y) — https://justjoin.it/raport-wynagrodzen/ogloszenia-o-prace-w-liczbach — 2026-01-08
43. **S043** — Speednet, a PL IT market review 2025/2026: NFJ +44%, applications per listing −45% y/y — https://speednetsoftware.com/pl/przeglad-rynku-it-2025-2026 — 2026-03-05

## Appendices (Excel)

| File | Sheets | What to edit |
|---|---|---|
| cohort_retention.xlsx | Input · Cohorts · Retention metrics | cohort sizes, the retention curve |
| growth_model.xlsx | Input · The 12-month model | MAU, growth, conversion, AOV, take rate |
| market_sizing.xlsx | Input · Funnel · PESTEL | PAM, funnel shares, environment factors |
| unit_economics.xlsx | Input · Unit economics · LTV CAC sensitivity | ARPU, VC, CAC, churn |


> Formulas recalculate on open (Excel / Numbers / LibreOffice). Details per the specification — knowledge/templates/SIX_PAGER_PROMPT_EN.md. The full version with evidence — REPORT.md.
