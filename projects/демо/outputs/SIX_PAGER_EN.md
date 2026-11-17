# CVStart: six-pager

> Committee document: the commercial version of CVStart (hosted freemium SaaS) and the global go-to-market strategy; the evidence version with the full claim registry lives in REPORT.md.

**Request:** Build the commercial version of cvstart.org (open-source AI resume builder and job-search tool: scan of 129 job boards, AI scoring, CV Studio, local pipeline, 19 locales) — resume creation and job search — and the go-to-market strategy for the whole world. Product: https://cvstart.org/, repository: https://github.com/Fighter90/career-ops-ui

## FAQ-1. Current state analysis

### 1.1 Market overview: trends, challenges and opportunities

The resume-builder market is estimated at $1.2–2.4 billion (2024–2025); its AI sub-segment grew from $1.3 to $1.47 billion at a 13.1% CAGR [^1]. The adjacent online-recruitment market reached $37.97 billion in 2025 with a 7.1% CAGR to 2033; the ATS segment stands at $2.5–3.3 billion, growing 12.3% a year [^2]. Year-by-year forecast (extrapolation of the AI sub-segment at a 13.1% CAGR [^1], conservative bound):

- 2026 — ≈ $1.66 billion;
- 2027 — ≈ $1.88 billion;
- 2028 — ≈ $2.13 billion.

Model assumption (market_sizing.xlsx appendix): with a $1.8 billion pool and an access funnel of 30% → 40% → 5%, the realistically reachable volume is ≈ $10.8 million a year.

Key trends:

- **The ATS filter has become the norm of hiring.** 98% of Fortune 500 companies use an ATS [^7]. What it means for the product: a resume that fails the automatic filter never reaches a human — ATS optimization and transparent scoring become the core value, not an add-on.
- **AI help for job seekers has gone mainstream.** 31–74% of job seekers use AI in the job search (2025–2026 surveys), and 84% say AI made the search easier [^3]. Implication: demand is formed; competition shifts from "has AI or not" to quality and trust.
- **Subscription fatigue is the strongest marketing lever.** All 7 direct competitors run freemium with a paid tier at $8–40/month and aggressive auto-renewals [^6]. Implication: honest pricing without auto-renewals is a working differentiator [C014].
- **Language blind spots of the market.** Direct competitors cover EN+5: Kickresume ships 6 interface languages, Enhancv/Teal/Rezi are English-only [^6], while CVStart already ships 19 locales [^5]; even LinkedIn has 36 [^2]. Implication: non-EN job seekers are underserved — an unoccupied entry angle [C013].
- **Hiring money sits next to candidate tools.** Indeed lists 685 million profiles across 60+ countries and 28 languages; Bayt (MENA) holds 59+ million profiles [^2]. Implication: career tools ride a constant demand flow — the capacity lets a niche leader grow.
- **The AI segment grows faster than the market.** 13.1% CAGR versus 7.1% [^1][^2]; one competitor, Kickresume, served 1.2+ million users of its AI features in 2025 [^3]. Implication: the leaders have not consolidated — the window for a new brand is open.
- **Privacy is a choice factor.** The "resume in someone else's cloud" barrier shows up among the technical audience (synthetic interviews — hypotheses) [C017]; CVStart runs 100% locally with bring-your-own-key (BYOK) [C001]. Implication: an opt-in cloud on top of a local core takes the product to the web without breaking trust [C019].

> **Conclusion (inference):** therefore, the opportunity window is 12–24 months: the AI segment grows at 13.1% a year [^1] while competitors are locked into auto-renewals and EN+5 language coverage [^6]; without revenue, the assets (129 scrapers, 18 providers) age out over the same horizon — this means entering the market now [C015].

### 1.2 Key competitors: growth and promo mechanics

Comparative table of competitor groups:

| | Freemium builders (Zety, resume.io, Novoresume, Kickresume, Enhancv, Teal, Rezi) | ATS optimizers (Jobscan, Huntr) | Job platforms with profiles (LinkedIn, Indeed, Bayt) |
|---|---|---|---|
| **Key advantages** | Marketing budgets and polished freemium funnels; AI features are already table stakes — Kickresume served 1.2+ million AI users in 2025 [^6][^3] | Mono-focus on ATS: 98% of Fortune 500 filter resumes; years of reverse-engineering career pages [^7] | Closing the whole hiring funnel: LinkedIn — 1 billion+ members in 200+ countries, 36 languages [^2]; Indeed — 685 million profiles, 60+ countries [^2] |
| **Growth and promo mechanics** | Freemium with a paid tier at $8–40/month and aggressive auto-renewals [^6]; upsell into AI features | Subscription at $49.95/month (Jobscan) [^6]; before/after demos on ATS checks | Premium subscriptions: LinkedIn Premium Career $39.99/month for new subscribers (US, 2026) [^2]; monetizing the candidate–employer contact |
| **Risks for the company** | **High** — a head-on fight on price ($8–40 [^6]) and on the SEO channel; their weakness is EN+5 language coverage | **Medium** — an expensive narrow tool with no job-board scan; a price umbrella over us: $49.95 versus $29 [^6] | **Low** — not a direct competitor in candidate tools; the risk is audiences locked inside their ecosystems [^2] |

Growth mechanics are freemium funnels with AI upsells, auto-renewals as a revenue source, and premium subscriptions on profile platforms. What nobody has: (1) multilingual parity — 19 locales in CVStart versus EN+5 among competitors [^5][^6]; (2) a private local mode with BYOK [C001]; (3) honest pricing without auto-renewals [C014]; (4) open code under MIT [C001]. Nobody reproduces all four together — this is the strategy window [C013].

> **Conclusion (inference):** this means the strategy window is the intersection of four elements (languages, privacy, honest price, open code); the window lasts 12–24 months (see 1.1) — after that competitors close it or the asset ages out.

## FAQ-2. User Persona. Who is the target audience?

### 2.1 Segments

Segments are split by the entry barrier, not by profession: the journey is the same for everyone (find relevant vacancies → make a resume that passes the ATS → get an offer); the barriers along it differ.

| | Active EN job seeker | Non-EN job seeker | Technical privacy-first user |
|---|---|---|---|
| **Who are they?** | Tech and digital professionals aged 25–40, US/EU/remote, actively searching for 1–6 months, EN resumes [C017] | Job seekers on DE/ES/PT-BR/JA/ZH markets; interface language and local conventions matter more than price [C018] | US technical audience: locality, privacy, open source; ready to pay $10–15/month for an honest OSS (open-source) tool [C017] |
| **What do they use today and why?** | Freemium builders with auto-renewals and manual ChatGPT — habit and availability [^6][^3] | EN tools "through translation" or manual templates: no alternative exists, competitors cover EN+5 [^6] | Local tools and their own scripts: distrust of clouds holding personal data [C001][C017] |
| **What difficulties do they face?** | Pay $29–40/month "for magic" with no job-board scan, get auto-renewed; resumes filtered out by the ATS [^6][^7] | Interface not in the native language, foreign resume conventions [^6][C018] | Installation requires a parent repository; Windows only via WSL [C003]; the entry barrier is installation — a web option is needed [C017] |
| **Common difficulties** | Manual tuning for every vacancy and distrust of subscriptions [^7][C017] | Plus distrust of monthly auto-renewals: an annual €100–120 plan is accepted, a monthly one is not [C018] | Auto-renewals and "a resume in someone else's cloud" are the main turn-offs [C017] |

Segment prioritization (capacity / CAC (customer acquisition cost) / competition):

- **Capacity:** segment 1 is confirmed by numbers — 31–74% of job seekers use AI [^3], and one competitor served 1.2+ million AI users in 2025 [^3]; segment 2 is a hypothesis with unmeasured capacity (a data gap) [C013]; segment 3 is narrow: fewer than 1% of OSS users contribute [C020].
- **CAC (customer acquisition cost):** the model assumes $60 via SEO (search engine promotion), Product Hunt and communities [C016]; in non-EN segments click competition is minimal [^6] — actual CAC should land below the model's.
- **Competition:** segment 1 — 7 direct competitors [^6]; segment 2 — practically zero [^6][C013]; segment 3 — low, but so is the monetization ceiling [C020].

> **Conclusion (inference):** therefore the launch core is segment 1 (confirmed capacity), wave 2 is the non-EN segments (zero competition, the capacity hypothesis is tested by an experiment), and segment 3 is a trust perimeter without a revenue bet; this means the tier ladder must serve the barriers of all three segments.

### 2.2 Barriers at each journey stage

| Journey stage | Barrier today | What the product does |
|---|---|---|
| Acquisition | "yet another subscription builder" — fatigue with auto-renewals [^6] | positioning "open-source, local, BYOK — against auto-renewals"; MIT open code [C001][C014] |
| Choice / usage | installation requires a parent repository; Windows only via WSL [C003] | a hosted browser version with no installation; the local mode stays for privacy-first users [C019] |
| Payment | distrust of monthly auto-renewals [C017][C018] | honest pricing: no auto-renewals, one-click cancellation, discounted annual plan [C014] |
| Post-payment experience | "did the resume pass the ATS?" — the result is invisible [^7] | the open scoring methodology and ATS bullets in CV Studio [C001] |

What holds back signup or renewal:

| Segment | Blocking factor | How it is removed |
|---|---|---|
| Active EN job seeker | installation and setup of a local pipeline [C003] | hosted version: entry without installation, import of an existing resume [C019] |
| Non-EN job seeker | interface and conventions not in the native language [C018] | 19 ready locales, waves of DE/ES/PT-BR → JA/ZH enablement [C004] |
| Technical privacy-first user | "the resume lands in someone else's cloud" [C017] | opt-in cloud over a local MIT core; BYOK — data never touches our keys [C001][C019] |

> **Conclusion (inference):** segmentation by the entry barrier; the tier ladder (Free on the user's own key → Pro → Unlimited) serves all three barriers — installation, language, trust; prioritization follows capacity/CAC/competition (the calculation is in 2.1).

## FAQ-3. Strategic initiatives. Justify each one briefly.

The direction was chosen from five options (A — keep as is, B — hosted freemium SaaS, C — B2B white-label, D — open-core dual-license, E — shut the commercial line down). The red team (an internal attack on the decision) rejected: C — sales out of scale for a solo developer; D — legally impossible on top of MIT; A/E — abandoning the axis at the moment of the widest window. B was chosen — hosted freemium SaaS with built-in mitigations: a BYOK Free tier (zero inference cost on the free tier), an opt-in cloud over the local core, honest pricing without auto-renewals [C019][C014]. Validity condition: the free tier runs on the user's own key, paid tiers on infrastructure keys; the beta threshold comes from the validation plan.

### 3.1 First driver — the hosted beta on three tiers

**First driver** — the hosted beta: a cloud version of the product with three tiers, removing the installation barrier (the main entry barrier of the core and privacy-first segments).

Key directions:

- the Free tier runs on the user's key (BYOK): zero inference cost, 3 resumes/month, watermarked PDF [C019];
- the Pro tier at $12 — cloud AI, unlimited resumes; the Unlimited tier at $29 — the 129-board scan, auto-pipeline, tracker [C019];
- the opt-in cloud: the local MIT mode stays forever — the product's promise is not broken [C001][C019].

Effect calculation: the synthetic beta funnel (a demonstration of the method, not a forecast) [^11]: 1,793 sign-ups over 12 weeks → 53 paying users → MRR (monthly recurring revenue) ≈ $1.5 thousand at a conversion of ≈ 3%. Break-even: fixed costs of ≈ $1.5 thousand/month (hosting and basic support) are covered by ≈ 69 paying users on the Unlimited tier [C016] — the beta checkpoint coincides with the self-sustainability point.

### 3.2 Second driver — honest pricing as positioning

**Second driver** — honest pricing: no auto-renewals, one-click cancellation, a transparent methodology [C014].

Key directions:

- plans without auto-renewals and a discounted annual tier [C014][C019];
- a competitor price comparison right on the landing page [C002];
- a public scoring-methodology page [C008][^4].

Effect calculation: the price gap = $49.95 (Jobscan) − $29 (Unlimited) = $20.95/month → Unlimited is 42% cheaper than the ATS-check leader [^6]; against the direct-competitor band of $8–40 [^6] the tier sits in the middle of the range — with more functionality (the 129-board scan included [C001]). Hypothesis: subscription fatigue converts into choice [C014]; the check is the beta conversion (FAQ-6).

### 3.3 Third driver — language waves: EN → DE/ES/PT-BR → JA/ZH

**Third driver** — language waves: enabling ready-made languages in sequence, each wave only after the previous wave's conversion is confirmed [C019].

Key directions:

- 19 locales already exist in the app and on the site [C004][^5];
- wave 2 (DE/ES/PT-BR) — after the review on 2027-02-10 [C019];
- annual billing for the EU: €100–120 is accepted, monthly auto-renewals are not [C018].

Effect calculation: language coverage = 19 locales [C004] versus 6 at the closest competitor [^6] = 3.2×; competition in non-EN segments is practically zero [C013], so the actual CAC should land below the model's ($60 assumption [C016]). Capacity (market_sizing.xlsx appendix): with a $1.8 billion pool and a 30% → 40% → 5% funnel, the reachable volume is ≈ $10.8 million a year.

### 3.4 Fourth driver — launch channels and methodology transparency

**Fourth driver** — launch channels and transparency: a free start on communities and a public proof of the method [C013].

Key directions:

- Product Hunt and Hacker News on beta launch day [C013];
- the SEO core "open-source Jobscan alternative" [C013];
- a community perimeter around the open core — a trust loop, not a revenue bet (fewer than 1% of OSS users contribute [C020]).

Effect calculation: the paid channel does not pay back at the model's 5.5% conversion — the paying-user CAC is ≈ $1,091 against an LTV of ≈ $176 (the table below) [C016]; this means that until conversion is confirmed the launch runs only on free channels (communities, Product Hunt, Hacker News, SEO), and the stop threshold comes from FAQ-6.

Unit economics — step-by-step:

Assumptions (EXAMPLE, demo): the weighted-average ARPU — Pro $12 × 60% + Unlimited $29 × 40% = $18.80 (the paying-share mix is an assumption, not the top-tier price); freemium: the free → paid conversion of 5.5% (the same conv_order as in growth) → paying-user CAC = 60/0.055 ≈ $1,090.91; paying-user LTV/CAC ≈ 0.16 — an illustration of the tier-profiling method: the paid channel does not pay back at this conversion
Tier-weighted ARPU: Pro 12.00 × 60.00% + Unlimited 29.00 × 40.00% = **18.80**.

| Formula | Calculation | Result |
|---|---|---|
| CM = ARPU × (1 − variable share) | 18.80 × (1 − 0.25) = 18.80 × 0.75 | **CM = 14.10** |
| Average paying lifetime = 1 / churn | 1 / 0.08 | **12.50 mo** |
| Paying-user CAC = CAC / free → paid conversion | 60.00 / 0.055 | **1,090.91** |
| LTV = CM / churn | 14.10 / 0.08 | **LTV = 176.25** |
| LTV/CAC | 176.25 / 1,090.91 | **0.16** (target ≥ 3) |
| CAC payback = CAC / CM | 1,090.91 / 14.10 | **77.37 mo** |

**Conclusion (inference):** the LTV/CAC ≥ 3 bar is not met: actual 0.16 at a paying-user CAC of 1,090.91 — to reach ≥ 3, the paying-user CAC must be ≤ 58.75 at this LTV (scenarios and grid — the Scenarios and Sensitivity sheets of unit_economics.xlsx). This means the beta's money comes from organic traffic, not bought traffic; paid channels switch on only when the actual conversion exceeds the model's.

> **Conclusion (inference):** therefore the initiatives close the barriers of FAQ-2 (installation → trust → language → post-payment) and build on existing assets: 19 ready locales [C004], the 129-board scan and 18 BYOK providers [C001], the public methodology page [^4] — the new work stands on what exists.

## FAQ-4. Tactics. Detail each initiative into concrete tactics.

The matrix ties every tactic to a user need: what exactly is built and changed — executable decisions, not slogans.

| Strategic initiative | Focus | User needs and expectations | Solutions (tactics) |
|---|---|---|---|
| Hosted beta (3.1) — tiers | Three tiers by beta launch — the commitment of the recorded decision (FAQ-5) | Try the product with no installation and no risk; see the price before signing up | The Free tier on the user's own key (BYOK): zero inference cost, 3 resumes/month, watermarked PDF [C019]; the Pro tier at $12 (cloud AI, unlimited resumes); the Unlimited tier at $29 (the 129-board scan + auto-pipeline + tracker) [C019] |
| Hosted beta (3.1) — activation | The first finished resume in one session | A result with no manual routine; a resume that passes the ATS [C008] | Import of an existing resume; tuning to a specific vacancy in CV Studio; ATS bullets; PDF/DOCX export [C001] |
| Honest pricing (3.2) — plans | The plans and methodology page by beta launch | A clear price with no traps; proof that the method works | Plans without auto-renewals, one-click cancellation, a discounted annual tier [C014][C019]; the public scoring-methodology page [C008][^4] |
| Honest pricing (3.2) — positioning | The "against auto-renewals" message in every channel | Trust: the audience is tired of auto-renewals [^6][C017] | A price comparison on the landing page ($29 versus $49.95 [C002]); the wording "open-source, local, BYOK — against auto-renewals" [C013][C014] |
| Language waves (3.3) — wave 2 | Enabling DE/ES/PT-BR after the EN conversion is confirmed, review on 2027-02-10 | An interface in the native language and local resume conventions [C018] | Enabling ready languages from the existing 19 [C004]; SEO pages for local queries [C013] |
| Language waves (3.3) — EU billing | Annual billing for non-EN waves | An annual plan instead of monthly auto-renewals [C018] | The annual plan at €100–120 (accepted by the EU segment [C018]); monthly auto-renewals are not offered [C014] |
| Launch channels (3.4) — start | Product Hunt and Hacker News on beta launch day | Find an honest tool through a clear query | The "open-source Jobscan alternative" positioning [C013]; the MIT open license as a trust argument [C001] |
| Launch channels (3.4) — transparency | A public proof of passing the ATS | Knowing in advance which criteria the resume is scored on [C008] | A public description of the ATS scoring criteria; before/after breakdowns on real vacancies [^4] |

## FAQ-5. High-level implementation plan

Expected contribution of initiatives to the outcome (must sum to 100%):

- 40% — The hosted beta launch (3.1): the monetization core; without the hosted version nothing else is testable — the largest contribution and the largest risk, hence the largest weight [C019];
- 25% — Language waves (3.3): coverage of 19 locales versus 6 at the closest competitor opens segments with minimal competition [C004][C013];
- 20% — Honest pricing (3.2): the main free → paid conversion lever, a differentiator against auto-renewals [C014][^6];
- 15% — Channels and transparency (3.4): the launch channels are free and serve the first three initiatives; the standalone contribution is capped by the solo-developer constraint [C015][C013].

Tactic order: high priority — the hosted beta and the tiers by 2026-12-15; medium — the plans and methodology page by beta launch; base — language wave 2 after the 2027-02-10 review.

Timing against market seasons: the beta ships before the January hiring peak — the season of mass applications after the New Year holidays; by the peak the funnel is already running and accumulating statistics instead of starting. The DE/ES/PT-BR wave follows confirmation of the EN conversion at the 2027-02-10 review [C019].

Parallel tracks: the community around the open core (GitHub stars, contributions, language feedback) runs off the commercial line — a trust loop and a feedback channel, not a revenue source: fewer than 1% of OSS users contribute [C020]. No partnerships in the first 90 days — the solo-developer constraint [C015].

**Decision D001** — The commercial version of CVStart: hosted freemium SaaS, globally. Commitment: ship the beta (Free BYOK / Pro $12 / Unlimited $29) with the opt-in cloud and honest pricing; a 90-day beta with stop thresholds from FAQ-6 (owner — the CVStart solo developer). Interim review on 2027-02-10; stop trigger: fewer than 20 paying users by week 12 with activation below 35% → shut the commercial line down (option E); a GitHub star drop of more than 30% after the cloud announcement → rework the opt-in communication [C019][^10].

## FAQ-6. Success metrics. KPIs in two dimensions

KPIs (key performance indicators) in two dimensions — business (money and base) and product (activation, retention, trust): MAU — monthly active users; NPS — net promoter score. Every metric carries a baseline → target by deadline → action threshold; a counter-metric guards every red-team hit.

**Business**

| Metric | Formula | Baseline (date, source) | Target by deadline | Action threshold (stop) | Counter-metric |
|---|---|---|---|---|---|
| MRR | paying × ARPU | $0 (2026-11-16, no monetization yet [^4] [^5]) | ≥ $1,500 by week 12 [^11] | fewer than 20 paying users by week 12 → shut the commercial line down (option E) | free-tier inference cost |
| Paying users | Σ active paying users at week end | 0 (2026-11-16, no hosted beta yet [^5]) | 50–60 by week 12 [^11] | fewer than 20 paying users by week 12 → option E | OSS community churn (stars/forks) |
| Paid conversion | paying / registrations | 3% by the model: 53 of 1,793 (2026-11-16, [^11]) | ≥ 3% by week 12 [^11] | 20–40 paying users → rebuild the tier and the price | activation (first resume) |
| Paying-user LTV/CAC | (ARPU × (1 − variable share) / churn) / CAC | 0.16 for the paid channel: LTV ≈ $176 at a CAC of ≈ $1,091 (2026-11-16, assumptions [C016]) | ≥ 3 by month 6 on the organic channel | paying-user acquisition price above $90 → organic channels only (unit_economics.xlsx sensitivity) | paid conversion |

**Product**

| Metric | Formula | Baseline (date, source) | Target by deadline | Action threshold (stop) | Counter-metric |
|---|---|---|---|---|---|
| Activation (first resume) | activations / registrations | 62% by the model: 1,111 of 1,793 (2026-11-16, [^11]) | ≥ 50% by week 12 [^11] | activation below 35% with fewer than 20 paying users → stop | privacy complaints (GDPR requests) |
| Paying churn | leavers per month / payers at month start | no data (2026-11-16, no hosted beta yet [^5]) | ≤ 10%/month by week 12 | churn above 10%/month → rebuild onboarding | paid conversion |
| Beta NPS | % promoters − % detractors | no data (2026-11-16, no hosted beta yet [^5]) | ≥ 30 by week 12 | below 30 while registrations grow → "growing into garbage", stop pushes | star drop |
| OSS community churn | Δ stars/forks over 30 days after the announcement | the pre-announcement trend — GitHub (2026-11-16, [^5]) | ≥ 0 by week 12 after the cloud announcement | a star/fork drop → rework the announcement (the red-team "trust collapse" hit) | MRR |

Counter-metrics — one per red-team hit:

- PII and scraping jurisdiction → personal-data deletion requests and privacy complaints; sustained growth — freeze the expansion and finish the opt-in architecture [C019].
- Trust collapse of "100% local" → GitHub stars; a drop of more than 30% after the cloud announcement — rework the opt-in communication: the local MIT core stays forever [C001].
- Freemium economics → conversion below 2% (the lower bound of the band [C020]) while registrations grow — rebuild the tier and the price; the stop thresholds follow the recorded decision (FAQ-5).

## Sources (footnotes)

[^1]: **S006** — wiseguyreports.com — Resume builder market: the $1.2–2.4 billion corridor; AI segment CAGR 13% — 2026-11-06 — https://www.wiseguyreports.com/reports/resume-builder-market — grade C
[^2]: **S007** — skyquestt.com — Job boards $37.97 billion (2025); ATS $2.5–3.3 billion; LinkedIn/Indeed/Bayt — 2026-11-06 — https://www.skyquestt.com/report/online-recruitment-market — grade B
[^3]: **S005** — kickresume.com — AI in the job search 2025–2026: 31–74% of job seekers; 1.2 million Kickresume AI users — 2026-11-06 — https://www.kickresume.com/en/press/ai-job-search-data/ — grade B
[^4]: **S001** — cvstart.org — CVStart — the product site: concept, positioning, limitations — 2026-11-06 — https://cvstart.org/ — grade B
[^5]: **S002** — career-ops-ui — the repository README (features, stack, ~7,602 automated tests) — 2026-11-06 — sources/raw/cvs_readme.md
[^6]: **S004** — rezi.ai — Competitors and prices: Kickresume/Rezi/Teal/Enhancv/Novoresume/Zety/resume.io — 2026-11-06 — https://www.rezi.ai/pricing — grade B
[^7]: **S012** — jobscan.co — Jobscan: 98% of Fortune 500 use ATS (2023–2024 report) — 2026-11-14 — https://www.jobscan.co/blog/fortune-500-use-applicant-tracking-systems/ — grade B
[^8]: **S009** — AI respondent: Sarah, 32, software engineer (US) — EN-segment hypotheses — 2026-11-06 — sources/raw/persona-sarah.md
[^9]: **S010** — AI respondent: Markus, 35, PM (Berlin) — EU/non-EN segment hypotheses — 2026-11-06 — sources/raw/persona-markus.md
[^10]: **S011** — The leader's answer (demo): option B — hosted freemium SaaS with red-team mitigations — 2026-11-06

**Synthetic material** (hypotheses, not evidence):

[^11]: **S008** — Synthetic funnel of the CVStart hosted beta (12 weeks, seed=7) — a demonstration of data analysis — 2026-11-06 — sources/raw/synthetic_funnel.csv

## Appendices (Excel)

| File | Sheets | What to edit |
|---|---|---|
| cohort_retention.xlsx | Input · Cohorts · Retention metrics | cohort sizes, retention curve |
| growth_model.xlsx | Input · 12-month model | MAU, growth, conversion, AOV, take rate |
| market_sizing.xlsx | Input · Funnel · PESTEL | PAM, funnel shares, environment factors |
| unit_economics.xlsx | Input · Unit economics · LTV/CAC sensitivity · Scenarios | ARPU, VC, CAC, churn |


> Formulas recalculate on open (Excel / Numbers / LibreOffice). Sheet labels inside the workbooks are in Russian (the demo's source language) — edit the values on the Input sheet; detailing per the spec: knowledge/templates/SIX_PAGER_PROMPT_EN.md. Full evidence version — REPORT.md.
