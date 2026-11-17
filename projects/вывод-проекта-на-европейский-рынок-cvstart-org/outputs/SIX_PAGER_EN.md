# Taking cvstart.org to the European market: six-pager

> Committee document: the three-wave European entry strategy for cvstart.org (option C) with deferred EUR monetization; the evidence version with the claim registry lives in REPORT.md.

**Request:** How do we take cvstart.org to the European market?

## FAQ-1. Current state analysis

### 1.1 Market overview: trends, challenges and opportunities

The European IT labor market is large and undersupplied: the EU employs over 10 million ICT specialists (2024, 5.0% of employment); Sweden leads the IT share (8.6%) [^11]. By country: Germany — 109,000 open IT vacancies (2025, down from the 149,000 peak of 2023, the shortage persists) [^12]; the Netherlands — 15.1 thousand open ICT vacancies at the end of 2025 and 622 thousand ICT specialists [^13]; France — an IT-engineer tension index of 1.1 and 42,635 hiring projects for a single profession [^14]; Spain — around 120,000 open tech vacancies with tech employment above 1 million [^15]; Sweden — plus 18,000 tech specialists a year until 2028 [^16]; Poland — plus 44% tech vacancies year over year (2025) [^17]. The resume-builder market the product belongs to is estimated at $1.2–2.4 billion with an AI segment CAGR of 13.1% [^18]; the adjacent online-recruitment market is $37.97 billion (2025) [^19]. Volume model assumption (market_sizing.xlsx): Europe ≈ 25% of the global market → a pool of ≈ $0.48 billion; the SOM is refined by the wave-1 checkpoint.

Year-by-year forecast (conservative):

- 2026 — the shortage persists: DE ≈ 100 thousand open vacancies, down from the peak [^12];
- 2027 — Poland keeps growing (+8.4% absolute vacancies in 2025) [C067];
- 2028 — Sweden accumulates +54 thousand tech specialists toward the 2028 goal [^16].

Key trends:

- **Trial-trap has become the dominant monetization mechanic in the EU.** CVMaker — €21.99/month after a €1.99 trial [^20], LiveCareer PL — 99 zł every 4 weeks [^21], resume.io — €2.95 for 7 days, then €24.95 [^2]. Implication: "free + honest, no auto-charges" positioning is a direct contrast with the market's pain [C048].
- **The local language is mandatory for DE/FR/ES.** Resumes and cover letters in Germany are written in German [^4], in France in French [^7], in Spain in Spanish, A4 format [^8]; in SE/NL English is the IT norm [C020]. Implication: entry waves follow the language threshold; template conventions are mandatory work, not an option [C050].
- **XING sets the free bar in DE.** XING offers a Lebenslauf builder and AI cover letters for free [^24]. Implication: the product's base function must be free; paid tiers sit on top of what XING lacks (a 129-board scan, a tracker) [C004].
- **Billing in a foreign currency is the global players' weakness.** resume.io bills in USD even on localized sites [^23]; Teal sells only in USD [^22]. Implication: EUR pricing and local payment methods are an extra differentiator; Nordics pay on average +28% over the US price, local currencies add 5–25% to conversion [C029].
- **Paying local demand is confirmed.** German clones self-report over 1 million created resumes [^25]. Implication: the niche pays; the question is honesty of terms, not the existence of money.
- **GDPR and taxes are an entry ticket a solo developer can clear.** Transfers of applicant data to US LLM APIs require SCC 2021/914 + a TIA [^6]; selling digital goods in the EU means Non-Union OSS from the first sale [^9]; EU hosting starts at €3.79/month [^5]. Implication: the GDPR minimum takes 1–2 weeks of work [C073] — hygiene, not a blocker.
- **The OSS channel provides a start with proven mechanics.** Show HN launches of similar projects scored 656 and 240 points [^30][^31]; the niche ceiling is Reactive Resume's 45,485 stars [C032]; r/cscareerquestionsEU has about 179,000 subscribers growing +15.5% a year [^29]. Implication: the community is the starting source of audience and trust with no ad budget [C059].

> **Conclusion (inference):** therefore the opportunity window is 12–18 months: the DE shortage persists [^12], the honest-free slot in DE is held only by XING (with no job-board scan or tracker) [^24], and competitors' trial-trap pain keeps growing [^20][^21]; this means entering now, with "free, honest, local" positioning [C048].

### 1.2 Key competitors: growth and promo mechanics

Comparative table of competitor groups:

| | Local clones (CVMaker DE, CVDesignR FR, LiveCareer PL) | Global freemium (resume.io, Teal, Zety, Kickresume) | Free alternatives (XING, Europass, OSS builders) |
|---|---|---|---|
| **Key advantages** | Local language and SEO visibility; CVDesignR — Premium €9.99/month with ATS analysis and AI, 5 million users (self-reported) [^1]; 1+ million resumes at DE clones [^25] | Brand and templates; 7 direct competitors at $8–40/month [C008]; English plus 5–6 locales [C009] | XING — a free Lebenslauf inside a familiar service [^24]; Europass — a free multilingual government template; Reactive Resume — 45k stars [C032] |
| **Growth and promo mechanics** | Local-key SEO ("lebenslauf erstellen" — KD 57, CPC €4.97, a cluster with volumes up to 201,000/month [^27]); trial-trap: a €1.99–2.95 trial → €21–25 auto-renewal every 4 weeks [^20][^21] | Global SEO ("resume builder" ≈ 673,000 queries/month [C031]); USD billing over localized sites [^23][^22]; aggressive auto-renewals [C008] | Ecosystem integration (XING), government status (Europass), community and open code (OSS) |
| **Risks for the company** | **High** — they hold the local SERP and budgets; their weakness is trial-trap pain and no job-board scan [^20][^21] | **Medium** — a price umbrella of €24.95 per 4 weeks [^2]; their weakness is USD billing [^23][^22] and narrow locales [C009] | **Medium** — XING takes the "free" slot in DE [^24]; Europass fails local ATS conventions; OSS is the same audience |

Competitors' growth mechanics are local-key SEO plus trial-auto-renewal at the clones, global SEO with USD billing at the international players, and ecosystem-backed freeness at XING. What nobody has: a 129-board scan with an application tracker [C004], an honest free tier with no auto-charges [C048], 19 ready locales [C007], and a private BYOK mode [C004] — nobody reproduces the combination; this is the strategy window.

> **Conclusion (inference):** this means the window is "honest free + multi-board" on local markets: competitors monetize pain (trial-trap) or offer only the base (XING); the window lasts 12–18 months before the clones take the honesty positioning.

## FAQ-2. User Persona. Who is the target audience?

### 2.1 Segments

Segments are split by the entry barrier (language and trust), not by profession.

| | Tech job seeker DE/NL/SE (EN professional) | Local-language job seeker DE/FR/ES | OSS/self-host developer |
|---|---|---|---|
| **Who are they?** | 25–40 years old, searching for 1–6 months, international companies; DE — 109 thousand open vacancies [^12], SE — 200 thousand+ employed in tech [C015] | Non-IT and junior seekers in DE/FR/ES: local language and conventions are mandatory [^4][^7][^8] | Privacy-first developers; the niche ceiling is 45.5 thousand stars [C032]; channels — Show HN, GitHub, Reddit [^29] |
| **What do they use today and why?** | Global freemium builders and manual ChatGPT — habit and brand [^23]; in DE — the free XING Lebenslauf [^24] | Local clones: they pay €9.99–23/month for local language and templates [^1][^21] | Self-hosted OSS tools and their own scripts: privacy and control [C004] |
| **What difficulties do they face?** | They pay €24.95 per 4 weeks after a €2.95 trial [^2]; resumes are filtered out by the ATS (98% of Fortune 500 use an ATS [^26]) | Trial-trap: a €1.99–2.95 trial turns into a €21–25 auto-renewal [^20][^21]; templates fail local ATS conventions | Installation requires a parent repository; Windows only via WSL [C006]; there is no hosted version [C006] |
| **Common difficulties** | Manual routine per vacancy; auto-renewals; "a resume in someone else's cloud" [C017] | Plus the language barrier of the tools: global players offer EN+5 [C009] | Distrust of freeness: switching "free forever" to a paid subscription risks a revolt [C054] |

Segment prioritization (capacity / CAC (customer acquisition cost) / competition):

- **Capacity:** segment 1 is confirmed by labor-market numbers [^12][^13][^16]; segment 2's paying demand is visible in clone prices and self-reports [^25]; segment 3 is a niche capped at 45k stars [C032].
- **CAC (customer acquisition cost):** there is no advertising budget [C059] — organic only (the OSS community, long-tail SEO); the monetary CAC is ≈ 0, the real price is time (5–10 h/week).
- **Competition:** in DE the SERP is densely held by clones and government tools — entry runs through long-tail and the "kostenlos/ohne Abo" modifiers [^27]; in NL/SE EN tools face weak competition (hypothesis [C043]).

> **Conclusion (inference):** therefore wave 1 is DE+NL+SE (the largest demand plus EN sufficiency), wave 2 is PL (vacancy growth with falling competition), wave 3 is FR/ES (a higher language threshold); this means the product must serve all three segments' barriers: language, honest price, privacy.

### 2.2 Barriers at each journey stage

| Journey stage | Barrier today | What the product does |
|---|---|---|
| Acquisition | the DE SERP is held by funded clones [^27]; "yet another builder" | "free, no auto-renewals, open-source" positioning against the trial-trap [C048]; long-tail SEO "kostenlos/ohne Abo" |
| Choice / usage | installation requires a parent repository [C006]; DE/FR/ES need local template conventions [^4] | the DE template: a tabular Lebenslauf + Anschreiben [^4]; 19 interface locales [C007]; a hosted version after the checkpoint |
| Payment | distrust of auto-renewals (the clones' trial-trap [^20][^2]) | monetization without auto-charges: an annual plan with a renewal reminder, monthly cancel-anytime, or one-off credits [C053] |
| Post-payment experience | "did the resume pass the ATS?" — the result is invisible [^26] | the open scoring methodology, ATS bullets, the application tracker [C004] |

What holds back signup or renewal:

| Segment | Blocking factor | How it is removed |
|---|---|---|
| Tech job seeker DE/NL/SE | installation and setup of a local pipeline [C006] | a hosted version after the wave-1 checkpoint; the local mode stays [C060] |
| Local-language job seeker | tools and templates not in the native language [^4][^7][^8] | DE conventions (a tabular Lebenslauf), then FR/ES (lettre de motivation, CV español) in waves 2–3 [C050] |
| OSS developer | "free forever will turn into a paid subscription" [C054] | the OSS core stays MIT and free [C005]; a public-contract test on the core before monetization [C053] |

> **Conclusion (inference):** segmentation by the entry barrier; the tier ladder — a free tier, Pro, Unlimited — serves every segment's barriers; prioritization follows capacity/CAC/competition (the calculation is in 2.1).

## FAQ-3. Strategic initiatives. Justify each one briefly.

The direction was chosen from five options: A — keep as is (passive growth via hreflang), B — a "light entry" into the EN-only audience of NL/SE/PL, C — a three-wave entry with an honest free tier and deferred monetization (the recommendation), D — commerce-first (a paid hosted launch in EUR right away), E — shut the European direction down and focus on the US. The red team changed the options: option C's 90-day checkpoint was redefined as a 180-day window measured on impressions and CV exports (otherwise the SEO channel was killed by its own criterion); D was shown to be strictly dominated by C (a solo operator of others' PII carries personal liability under Art. 82 GDPR; a hosted MVP is 300–500 hours); A was rejected as "sponsoring competitors" (MIT allows a fork with trial-trap on your code); B is not a European strategy; E abandons the axis of the request [C060]. C was chosen: the only option that grows the European audience while keeping a path to EUR monetization within solo resources [C047].

### 3.1 First driver — the OSS launch of wave DE+NL+SE

**First driver** — the OSS launch of wave 1: community channels deliver the starting audience and trust with no budget [C059].

Key directions:

- a Show HN launch positioned as "open-source, local, BYOK — against auto-renewals" (comparable projects scored 656 and 240 points [^30][^31]);
- an answer-first tactic in r/cscareerquestionsEU (about 179 thousand subscribers [^29]) — direct self-promotion earns a ban [C045];
- GitHub releases with release statistics as a proxy for exports [^3].

Effect calculation: the goal is stars 96 → 400–1,000 over 6 months with 1–2 successful HN/Reddit waves (a forecast, low confidence); the wave-1 checkpoint is a 180-day window: indexing, Search Console impressions, and an NSM (exported CVs per month) ≥ 50 [C052]. Passed → stage 2; failed → fall back to B/E.

### 3.2 Second driver — long-tail DE SEO

**Second driver** — DE SEO on long-tail: entering against the clones not on head keys but on honesty modifiers.

Key directions:

- 10–12 articles on "kostenlos", "ohne Abo", "Alternative zu CVMaker/resume.io" (the "lebenslauf erstellen" head cluster: KD 57, CPC €4.97; free cluster rows up to 201,000/month [^27]);
- a Keyword Surfer pre-check of volumes before the start (the data gap is recorded honestly) [C077];
- re-building semantics when "Crawled – not indexed" exceeds 50%.

Effect calculation: at a domain rating of zero the realistic upper bound is 500–2,000 visits/month by month 6 with good content (a forecast, low confidence); the checkpoint is ≥ 80% indexing of DE/NL/SE pages and Search Console impressions above 5,000/month by day 150. Implication: SEO amplifies wave 1 rather than replacing the community; if volumes are negligible the hours move to community/PR [C035].

### 3.3 Third driver — DE conventions and the GDPR architecture

**Third driver** — local conventions and GDPR: without the first, traffic does not convert [^4]; without the second, hosted does not launch [^6].

Key directions:

- a tabular Lebenslauf + Anschreiben for the DE wave [^4]; then lettre de motivation (FR) [^7] and the CV español (ES) [^8] in waves 2–3 [C050];
- EU hosting from €3.79/month [^5]; SCC 2021/914 + a TIA for US LLM APIs [^6]; a 72-hour incident plan before the first user;
- Non-Union OSS from the first EUR sale [^9].

Effect calculation: the GDPR minimum is 1–2 weeks of work and ≈ €4–20/month of infrastructure [C073]; this removes the main legal risk of the hosted stage in advance, before monetization — not after the first incident.

### 3.4 Fourth driver — the hosted checkpoint and EUR monetization without auto-charges

**Fourth driver** — monetization compatible with the positioning: a hosted launch after the wave-1 checkpoint and the community test [C053].

Key directions:

- a community test of "OSS free forever + hosted for money" on the current core (96 stars) before monetization starts [C053][C054];
- the Free (BYOK) / Pro €9–12 / Unlimited €25–29 tiers — a corridor between CVDesignR's €9.99 [^1] and resume.io's €24.95 [^2]; a subscription without auto-charges: an annual plan with a pre-renewal reminder and one-click cancellation, a monthly cancel-anytime plan, or one-off credits [C052][C053];
- a merchant of record or Non-Union OSS for VAT [^9]; for DE — PayPal (77% of German buyers prefer PayPal to cards [C030]).

Effect calculation: the unit assumptions (carried over from the global model, unconfirmed for the EU [C057]): an ARPU of €25, a 25% variable share, 8%/month churn → break-even on fixed costs of ≈ €150/month at about 8 paying users; the month-12 forecast is 50–80 paying users and an MRR of €1.3–2 thousand (low confidence; verified by the monetization checkpoint). Wave 2 (PL) starts after wave 1: vacancies grew +8.4% (110,996 in 2025 [^34]) while competition fell 45% per application [^35]; regional pricing for PL/ES is an A/B test during validation [C044].

Unit economics — step-by-step:

Assumptions (carried over from the global plan, unconfirmed for the EU [C057]): an ARPU of €25 (Unlimited; the CVDesignR €9.99 [^1] ↔ resume.io €24.95 [^2] corridor); a 25% variable share; churn of 8%/month. The CAC of €30 is an assumption for the paid-scenario sensitivity; the monetary CAC of the organic channel is ≈ 0. Verified during validation — the validation plan owns the check.

| Formula | Calculation | Result |
|---|---|---|
| CM = ARPU × (1 − variable share) | 25.00 × (1 − 0.25) = 25.00 × 0.75 | **CM = 18.75** |
| Average paying lifetime = 1 / churn | 1 / 0.08 | **12.50 mo** |
| LTV = CM / churn | 18.75 / 0.08 | **LTV = 234.38** |
| LTV/CAC | 234.38 / 30.00 | **7.81** (target ≥ 3) |
| CAC payback = CAC / CM | 30.00 / 18.75 | **1.60 mo** |

**Conclusion (inference):** LTV/CAC ≥ 3 holds up to churn ≈ 20.83 %/mo, a CAC of ≈ €78.12, and a variable-cost share of ≈ 61.60 % (each threshold — all else equal; the grid is on the Sensitivity sheet). This means the model is resilient under organic acquisition; every assumption is carried over from the global plan and is verified during validation.

> **Conclusion (inference):** therefore the initiatives close the barriers of FAQ-2 (a crowded SERP → trust → language → auto-renewals) and build on existing assets: 19 ready locales [C007], the 129-board scan [C004], the MIT open code [C005] — the new work stands on what exists.

## FAQ-4. Tactics. Detail each initiative into concrete tactics.

The matrix ties a tactic to a user need: what is built and changed — executable decisions, not slogans.

| Strategic initiative | Focus | User needs and expectations | Solutions (tactics) |
|---|---|---|---|
| OSS launch of wave 1 (3.1) — community | Show HN + Reddit in the first weeks of the DE+NL+SE wave | Find an honest tool with no subscription traps | The Show HN launch "open-source, local, BYOK — against auto-renewals" [^3]; answer-first in r/cscareerquestionsEU [^29]; GitHub releases with statistics [C045] |
| OSS launch of wave 1 (3.1) — checkpoint | The 180-day wave-1 window: NSM and indexing | See a real result, not stars | NSM ≥ 50 exported CVs/month by locale (an opt-in counter) [C052]; 400–1,000 stars as a secondary metric; a failure → fall back to B/E [C052] |
| Long-tail DE SEO (3.2) — content | 10–12 articles on the "kostenlos/ohne Abo" modifiers | A free tool found through a clear local query | Articles for the "lebenslauf erstellen" cluster [^27]; comparison pages "Alternative zu CVMaker/resume.io"; a Keyword Surfer pre-check [C077] |
| Long-tail DE SEO (3.2) — technical loop | Indexing ≥ 80%, impressions > 5,000/month by day 150 | Pages that are actually found in the DE SERP | Search Console monitoring; re-building semantics when "Crawled – not indexed" exceeds 50%; hreflang across 19 locales [C007] |
| DE conventions + GDPR (3.3) — templates | A tabular Lebenslauf + Anschreiben by the DE wave | A resume in the local format that employers accept [^4] | The DE template per EURES conventions [^4]; the FR (lettre de motivation [^7]) and ES (CV español [^8]) waves after PL conversion is confirmed [C050] |
| DE conventions + GDPR (3.3) — architecture | A GDPR-ready cloud before the first user | Resume data never leaks into another jurisdiction | EU hosting from €3.79/month [^5]; SCC 2021/914 + a TIA for US LLM APIs [^6]; a 72-hour incident plan [C073] |
| Hosted and EUR monetization (3.4) — contract test | A community test on the core before monetization | Keep the trust in "free forever" [C054] | A public breakdown of the Reactive Resume/Cal.com/Plausible transitions [C053]; proactive positioning "OSS free forever, hosted is convenience for money"; a test on the current core [C053] |
| Hosted and EUR monetization (3.4) — tiers and billing | Free BYOK / Pro €9–12 / Unlimited €25–29 with no auto-charges | An honest EUR price with no renewal traps | A price corridor between CVDesignR €9.99 [^1] and resume.io €24.95 [^2]; an annual plan with a reminder or one-off credits [C053]; a merchant of record or Non-Union OSS [^9]; PayPal for DE [C030] |

## FAQ-5. High-level implementation plan

Expected contribution of initiatives to the outcome (must sum to 100%):

- 35% — The OSS launch of wave DE+NL+SE (3.1): the starting audience and trust; without it neither SEO nor monetization works — the largest weight [C047];
- 25% — Long-tail DE SEO (3.2): a scalable organic channel at zero budget [C059];
- 20% — DE conventions and the GDPR architecture (3.3): without conventions traffic does not convert [C050], without GDPR hosted does not launch [C073];
- 20% — The hosted checkpoint and EUR monetization (3.4): the path to revenue, started only after the wave-1 checkpoint [C052].

Tactic order: high priority — the Show HN/Reddit launch, the DE template conventions, the SEO volume pre-check; medium — the SEO content plan, the GDPR architecture; base — the PL wave (after the checkpoint), then FR/ES.

Timing against market seasons: wave 1 starts ahead of the January hiring peak — January–March brings the largest application wave in DE/SE; the launch lands 6–8 weeks before the peak so indexing and community waves accumulate statistics in time. The wave-1 checkpoint is a 180-day window [C052]; wave 2 (PL) follows it.

Parallel tracks: the OSS community (GitHub, Discussions) runs off the commercial line — a trust and feedback loop; PR/media (heise.de — 5.68 million readers [C035]) amplifies release news. The wave-1 hour budget is 160+ hours against 130–260 available [C056]: a cutting priority is fixed — content volume first, then the FR/ES groundwork, never the DE local conventions [C050].

**Decision D001** — Taking cvstart.org to the European market — option C (three waves). Commitment: wave 1 DE+NL+SE — OSS channels plus DE long-tail SEO "kostenlos/ohne Abo" against the trial-trap, local Lebenslauf conventions; a 180-day checkpoint (NSM ≥ 50 exported CVs/month plus indexing and impressions); stage 2 — the community test and hosted in EUR without auto-charges (Pro €9–12 / Unlimited €25–29); wave 2 PL with an A/B price; wave 3 FR/ES (owner — the founder). **Decision D002** — pre-checks before wave 1 starts (€0, 2 weeks): Keyword Surfer on DE/NL/SE keys; a Search Console indexing audit of the locales; a draft WBS for wave 1 with a fixed cutting priority (owner — the founder). Grounds: [C051][C052][C053][C056][C047].

## FAQ-6. Success metrics. KPIs in two dimensions

KPIs (key performance indicators) in two dimensions — business (money and base) and product (audience, activation, trust): the NSM is exported CVs per month, in the units of the target audience, not stars. Every metric carries a baseline → target by deadline → action threshold; a counter-metric guards every red-team hit.

**Business**

| Metric | Formula | Baseline (date, source) | Target by deadline | Action threshold (stop) | Counter-metric |
|---|---|---|---|---|---|
| MRR (monthly recurring revenue) | paying × ARPU | €0 (2026-11-16, no hosted version [C057]) | €1.3–2 thousand by day 360 (the stage-2 plan) | revenue €0 after the wave-1 checkpoint fails → fall back to B/E | free-tier inference cost above €200/month |
| Paying users | Σ active paying users at month end | 0 (2026-11-16, no hosted version [C057]) | 50–80 by day 360 (the stage-2 plan) | NSM below 20 at 500+ visits → fall back to B/E (the validation plan) | paying churn |
| Paid conversion | paying / registrations | the freemium benchmark of 2–5% (2026-11-16, [C051]) | ≥ 2% by day 360 — the lower bound of the benchmark [C051] | zero conversion at 500+ visits → rebuild the tier | beta NPS |
| Paying-user LTV/CAC | (ARPU × (1 − variable share) / churn) / CAC | 7.81 by the model: an LTV of ≈ €234 at a CAC of ≈ €30 (2026-11-16, assumptions [C057]) | ≥ 3 by day 360 (the stage-2 plan) | below 3 on the paid channel → organic only | revenue/visitor |
| PL revenue/visitor | PL revenue / PL visitors | none (2026-11-16, measured from the first 30 days of wave 2 [C044]) | ≥ +20% by day 60 of wave 2 (the validation plan) | no difference → a single EUR price (the validation plan) | PL ARPU |

**Product**

| Metric | Formula | Baseline (date, source) | Target by deadline | Action threshold (stop) | Counter-metric |
|---|---|---|---|---|---|
| NSM: exported CVs/month | Σ CV exports by locale (an opt-in counter) | 0 (2026-11-16, no telemetry; the counter is a pre-check [C052]) | ≥ 50 by day 180 (the validation plan) | below 20 at 500+ visits/month → fall back to B/E (the validation plan) | DE-page bounce above 80% |
| Activation (the first CV export) | visitors with a first export / all visitors | no telemetry (2026-11-16, an opt-in counter [C052]) | ≥ 5% by day 90 (the validation plan) | activation falls while impressions grow → rebuild onboarding | more than 5 GDPR requests |
| DE-page indexing | indexed / published (Search Console) | 0 (2026-11-16, the channel has not started [C052]) | ≥ 80% by day 60 (the validation plan) | no indexing in 60 days → close the channel, hours go to community/PR (the validation plan) | "Crawled – not indexed" above 50% |
| EN conversion NL/SE | EN landing conversion / DE landing conversion | a rotating A/B/C of the nl/sv/en pages from 19 locales (rotation starts 2026-12-01, [^10]) | EN ≥ 50% of DE by day 90 (the validation plan) | below 30% → NL/SE move to wave 2 with localization (the validation plan) | NL/SE bounce above 85% |
| Star drop after the monetization announcement | Δ stars over 30 days after the announcement | the star trends of Reactive Resume / Cal.com / Plausible around announcements (reviewed 2026-11-16, [C054]) | a drop below 10%/month by day 30 after the announcement (the validation plan) | a drop of ≥ 10%/month or more than 3 hard issues → rebuild the public contract before code (the validation plan) | the tone of Discussions |

Counter-metrics — one per red-team hit:

- "SEO against funded clones" → zero indexing in 60 days; the channel closes and the hours move to community/PR (the volume pre-check runs before the start [C077]).
- "Solo overload" → a weekly plan missed twice in a row; the WBS cutting priority switches on [C056].
- "A community revolt at monetization" → star drops and negative issues; the announcement is rolled back and the public contract rebuilt [C053][C054].
- "A GDPR incident" → regulator requests; the 72-hour incident plan is in place before the first user [^6].

## Sources (footnotes)

[^1]: **S021** — cvdesignr.com — CVDesignR (FR): Premium €9.99/month with ATS analysis and AI — 2026-10-01 — https://cvdesignr.com/fr/premium — grade B
[^2]: **S024** — aivario.com — resume.io EU prices: €2.95 for 7 days → €24.95 every 4 weeks — 2026-10-01 — https://aivario.com/tools/resume-io — grade B
[^3]: **S001** — cvstart.org — CVStart — the product site (the career-ops-ui landing): free OSS, a local mode, 19 locales — 2026-11-08 — https://cvstart.org
[^4]: **S016** — eures.europa.eu — EURES Germany: resumes and cover letters in German — 2026-11-08 — https://eures.europa.eu/living-and-working/living-and-working-conditions-europe/living-and-working-conditions-germany_en — grade A
[^5]: **S034** — hetzner.com — Hetzner CX22 €3.79/month (DE/FI, a GDPR-compliant DC) — 2024-06-06 — https://hetzner.com/pressroom/new-cx-plans — grade B
[^6]: **S032** — edpb.europa.eu — EDPB: transfers to non-EEA services require SCC 2021/914 (+ a TIA) — 2025-01-01 — https://edpb.europa.eu/sme/be-compliant/international-data-transfers_en — grade A
[^7]: **S017** — eures.europa.eu — EURES France: CVs and lettre de motivation in French — 2026-11-08 — https://eures.europa.eu/living-and-working/living-and-working-conditions-europe/living-and-working-conditions-france_en — grade A
[^8]: **S018** — eures.europa.eu — EURES Spain: the CV and the letter in Spanish, A4 — 2026-11-08 — https://eures.europa.eu/living-and-working/living-and-working-conditions-europe/living-and-working-conditions-spain_en — grade A
[^9]: **S033** — docs.stripe.com — Stripe: a non-EU seller registers for Non-Union OSS from the first sale; the EU threshold is €10k — 2025-01-01 — https://docs.stripe.com/tax/use-stripe-to-register/non-union-oss — grade A
[^10]: **S006** — the career-ops-ui README: features, stack, automated tests, 19 locales — 2026-11-08 — sources/raw/cvs_readme.md — grade A
[^11]: **S035** — ec.europa.eu — Eurostat: 10+ million ICT specialists in the EU (2024), 5.0% of employment; SE 8.6% — 2025-07-08 — https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20250708-2 — grade A
[^12]: **S010** — bitkom.org — Bitkom: 109,000 open IT vacancies in Germany (2025) — 2025-12-15 — https://www.bitkom.org/sites/main/files/2026-01/bitkom-studienbericht-it-fachkraefte-2025.pdf — grade B
[^13]: **S011** — cbs.nl — CBS (NL): 15.1 thousand open ICT vacancies at the end of 2025; 622 thousand ICT specialists — 2026-01-01 — https://www.cbs.nl/nl-nl/longread/rapportages/2026/digitalisering-en-kenniseconomie-2025/2-ict-en-economie — grade A
[^14]: **S012** — insee.fr — Insee (FR): the IT-engineer tension index of 1.1; 42,635 hiring projects — 2025-10-14 — https://www.insee.fr/fr/statistiques/8616805?sommaire=8616883 — grade A
[^15]: **S013** — coit.es — DigitalES×COIT (ES): around 120,000 open tech vacancies — 2024-06-01 — https://www.coit.es/sites/default/files/digitales_anatomia_brecha_talento_tecnologico.pdf — grade B
[^16]: **S014** — techsverige.se — TechSverige (SE): +18,000 tech specialists a year until 2028 — 2024-01-01 — https://techsverige.se/kompetensbehoven-inom-tech — grade B
[^17]: **S015** — nofluffjobs.com — No Fluff Jobs (PL): +44% tech vacancies year over year — 2025-12-01 — https://nofluffjobs.com/insights/raport-rynek-pracy-it — grade C
[^18]: **S004** — wiseguyreports.com — The resume-builder market: the $1.2–2.4 billion corridor; the AI segment CAGR 13% — 2026-11-08 — https://www.wiseguyreports.com/reports/resume-builder-market — grade C
[^19]: **S005** — skyquestt.com — Online recruitment $37.97 billion (2025); ATS $2.5–3.3 billion — 2026-11-08 — https://www.skyquestt.com/report/online-recruitment-market — grade B
[^20]: **S036** — cvmaker.de — CVMaker DE: €21.99/month after a €1.99 14-day trial (auto-renewal) — 2026-11-01 — https://cvmaker.de/preise — grade B
[^21]: **S037** — livecareer.pl — LiveCareer PL: 9.95 zł for 14 days → 99 zł every 4 weeks — 2026-11-01 — https://livecareer.pl/cennik — grade B
[^22]: **S023** — tealhq.com — Teal: all prices in USD ($13 week/$29 month/$179 year) — 2026-11-01 — https://help.tealhq.com/en/articles/9530153 — grade A
[^23]: **S022** — resume.io — resume.io: billing in USD, the local currency is display-only — 2026-11-01 — https://help.resume.io/en/articles/3785664 — grade A
[^24]: **S020** — xing.com — XING Lebenslauf (DE): a free Lebenslauf builder + AI cover letters — 2026-11-01 — https://xing.com/lebenslauf — grade B
[^25]: **S038** — meinperfekterlebenslauf.de — a local DE clone, "1+ million Lebensläufe" — 2026-11-01 — https://www.meinperfekterlebenslauf.de — grade C
[^26]: **S040** — jobscan.co — Jobscan: 97.8–98% of Fortune 500 use an ATS — 2018-05-01 — https://www.jobscan.co/blog/fortune-500-use-applicant-tracking-systems/ — grade B
[^27]: **S041** — performance-suite.io — the Keyword DB: volumes of the DE Lebenslauf query cluster — 2026-09-25 — https://www.performance-suite.io/keyword-db/de-de/lebenslauf-erstellen/ — grade C
[^29]: **S031** — gummysearch.com — r/cscareerquestionsEU: about 179 thousand subscribers, +15.5%/year — 2026-08-10 — https://www.gummysearch.com/r/cscareerquestionsEU — grade C
[^30]: **S029** — hn.algolia.com — Show HN: Open Resume — 656 points, 198 comments (2023) — 2023-06-25 — https://hn.algolia.com/api/v1/items/36470297 — grade A
[^31]: **S030** — hn.algolia.com — Show HN: RxResume — 240 points (2020) — 2020-03-28 — https://hn.algolia.com/api/v1/items/22709183 — grade A
[^32]: **S025** — paddle.com — Paddle: Nordics pay +28% over the US price; local currencies add 5–25% to conversion — 2026-03-01 — https://www.paddle.com/blog/saas-pricing-models-strategies-fltr — grade B
[^33]: **S026** — paddle.com — Paddle: in Germany 77% prefer PayPal to cards — 2026-03-01 — https://www.paddle.com/blog/average-revenue-per-paying-user-arppu-fltr — grade B
[^34]: **S042** — justjoin.it — the Just Join IT 2026 report: 110,996 IT vacancies on the platform in 2025 (+8.42% y/y) — 2026-01-08 — https://justjoin.it/raport-wynagrodzen/ogloszenia-o-prace-w-liczbach — grade B
[^35]: **S043** — speednetsoftware.com — the Speednet review of the PL IT market 2025/2026: NFJ +44%, applications per listing −45% y/y — 2026-03-05 — https://speednetsoftware.com/pl/przeglad-rynku-it-2025-2026 — grade B

**Synthetic material** (hypotheses, not evidence):

[^28]: **S007** — AI respondent: Markus, 35, PM (Berlin) — EU/DE segment hypotheses — 2026-11-08 — sources/raw/persona-markus.md

## Appendices (Excel)

| File | Sheets | What to edit |
|---|---|---|
| cohort_retention.xlsx | Input · Cohorts · Retention metrics | cohort sizes, retention curve |
| growth_model.xlsx | Input · 12-month model | MAU, growth, conversion, AOV, take rate |
| market_sizing.xlsx | Input · Funnel · PESTEL | PAM, funnel shares, environment factors |
| unit_economics.xlsx | Input · Unit economics · LTV/CAC sensitivity | ARPU, VC, CAC, churn |


> Formulas recalculate on open (Excel / Numbers / LibreOffice). Sheet labels inside the workbooks are in Russian (the project's source language) — edit the values on the Input sheet; detailing per the spec: knowledge/templates/SIX_PAGER_PROMPT_EN.md. Full evidence version — REPORT.md.
