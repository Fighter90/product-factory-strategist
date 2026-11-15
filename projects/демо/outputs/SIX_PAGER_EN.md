# CVStart: Six-pager (EN)

> **Commercial version & global go-to-market strategy for cvstart.org** — a complete 12-step run of
> the "Product Factory Strategist" agent (Nov 6–7, 2026). Every section follows the chain
> "data → reasoning → calculation → conclusion"; screenshots are deliberately excluded. Evidence
> base: claims C001–C020, sources S001–S011 (footnotes at the bottom), decision D001. Assembly
> method: knowledge/templates/SIX_PAGER_PROMPT.md. Full registry — REPORT.md.

## FAQ-1: Current state analysis

### 1.1 Market overview: resume & job-search tools — trends, challenges and opportunities

The resume-tools market, per aggregator estimates, stood at $1.2–2.4B in 2024–2025; the AI
sub-segment grew from $1.3B to $1.47B (13.1% CAGR)¹ [C005]. Online recruitment overall: $37.97B
in 2025, 7.1% CAGR to 2033² [C011]. The AI sub-segment is expected to keep growing at double digits:

- AI sub-segment volume: +13%/yr through 2026–2030;
- share of job seekers using AI: 31–74% across 2025–2026 surveys, +7 p.p. year over year³ [C009];
  1.2M+ job seekers used Kickresume's AI features in 2025 [C010].

Key trends in the job-search tools market:

- **The ATS gate has become the hiring standard.** 98% of Fortune 500 companies use an ATS⁴ [C008] — a
  resume that fails machine screening devalues the candidate before a human ever sees it. "Check my
  resume against ATS" has moved from feature to hygiene minimum, and transparent scoring criteria
  became a trust argument.
- **Subscription fatigue and auto-renewals.** Every mass-market competitor (Zety, resume.io,
  Novoresume, Kickresume, Enhancv, Teal, Rezi) runs freemium with paid tiers at $8–40/mo and
  aggressive auto-renewals⁵ [C006]. The "trial $2–3 → auto-renewal $24–40" pattern generates a steady stream
  of complaints and opens a verifiable window for honest pricing.
- **Generative AI drove the cost of text generation to zero.** Bare "AI writes text" is no longer a
  differentiator — value shifted to data (scanning real vacancies), context (resume against a
  specific JD) and process (scoring → tuning → application → tracking in one pipeline).
- **The multilingual gap.** Direct competitors' language coverage is EN+5 (Kickresume — 6
  languages)⁵, while the global labor market is multilingual; local resume conventions (EU, JA, ZH)
  are ignored by mass tools.
- **Privacy and data sovereignty.** A resume is a concentrated PII package; part of the audience
  refuses to upload it to someone else's cloud. A local mode with BYOK is a growing niche
  (including GDPR-sensitive Europe).
- **Inference economics.** Generation cost forces competitors to strangle their free tiers; the BYOK
  model (users bring their own LLM key) dissolves that conflict — a unique advantage of an open
  product.

### 1.2 Key competitors and analysis of their growth strategies and promo mechanics

| | **Mass-market SaaS** — Zety, resume.io, Novoresume | **ATS/AI-specialists** — Jobscan, Teal, Rezi, Enhancv, Kickresume | **Open-source / local** — CVStart (core), self-built pipelines |
|---|---|---|---|
| **Key advantages** | Big marketing budgets and SEO dominance; instant "pick a template → download PDF"; brand awareness. Strategy is scaling, not optimization | Depth in the niche: ATS comparison, keyword optimization, AI tuning; strong content SEO ("ATS checker", "resume vs CV") | Full data control (local); zero price for the core; open code = trust and auditability; 129 vacancy sources in one pipeline |
| **Growth strategy & promo mechanics** | Landing funnels and "trial $2–3 → auto-renewal $24–40"; template A/B landing pages per search query; package upsells | Freemium with hard limits (Teal: free unlimited resumes, paid AI at $29); Rezi: $149 lifetime tier as one-time cash capture; credit-based generation model | Organic GitHub/word-of-mouth; "curl install" distribution; no monetization — "$0 forever" |
| **Risks for CVStart** | SEO and budget war in EN — **Medium** (we do not compete on budget, we compete on niche) | They capture "hosted + easy" before us — **High** (the window: 2–3 quarters) | A fork monetizing on top of MIT — **Medium** (mitigation: hosted speed from the same vendor) |

Growth mechanics are initiatives aimed at growing conversion, the paying base and retention.
Competitors have already shipped: free generation limits (credit models), lifetime tiers (Rezi
$149) as one-time cash capture, discounted annual plans, content SEO around "ATS checker" queries,
AI features as a paid upsell. What nobody has: 19+ locale coverage, a local mode with BYOK,
pricing without auto-renewals, an open scoring methodology.

**Conclusion (inference).** The market grows at double digits precisely in the AI sub-segment;
competitors occupy the EN mass market and the ATS niche, leaving three angles open —
multilingualism, privacy, honest pricing. Therefore CVStart's window is "a hosted version of an
open product with a BYOK-free tier and honest pricing", and it is time-boxed (2–3 quarters before
the specialists react).

## FAQ-2: User Persona. Who is the target audience of CVStart?

### 2.1 Job seekers

| Job-seeker types | **Active tech job seeker** (core) | **Mass non-tech job seeker** | **Non-EN job seeker** (wave 2) |
|---|---|---|---|
| **Who are they?** | 25–40, US/EU, engineers/analysts/PMs; searching 1–6 months; technically literate, value open source | Any profession, wants "a resume fast"; does not understand ATS; will pay for "do it for me" | DE, ES, PT-BR, JA, ZH; thinks about the resume in their native language; GDPR-sensitive; local format conventions |
| **What do they use today, and why?** | ChatGPT manually (free, but no vacancies or tracking); Jobscan/Teal (but "AI slop" and subscriptions); self-built scripts | Zety/resume.io via SEO ads — template + PDF for a trial with auto-renewal | Nothing specialized: local Word templates + manual translation; EN tools ignore conventions |
| **What difficulties do they face?** | "AI slop" with no vacancy context; manual switching across 5 tools; subscription traps; resume fails ATS | Hidden trial pricing; templates fail ATS; no idea why they get rejected | No tools with a native interface and local conventions; fear of uploading PII to a cloud |
| **Common difficulties** | The resume must be tailored to every vacancy manually; application tracking lives in a spreadsheet; no feedback on why the resume was rejected | — | — |

**Segment reasoning.** The tech core chooses tools deliberately and pays for search automation, not
for text (synthetic: Sarah accepts $10–15, and $29 only "if it actually finds jobs"⁷ — the
willingness-to-pay hypothesis [C017] under test in the beta); it is also
the source of the first organic reviews (GitHub/HN). Wave 2 is a multiplier on ready-made locales:
the interface is already translated [C004], competitors are absent [C007], and the payment model is
annual plans without auto-renewals (Markus: €100–120/yr, categorically against monthly traps⁸).

### 2.2 Barriers at every stage of the job-seeker journey

| Journey stage | Barrier today | What CVStart does |
|---|---|---|
| **Job search** | 30+ job-board tabs, duplicates, no unified search; relevance unclear | Scan of ~129 boards into one feed + AI scoring 0.0–5.0 against the user's resume |
| **Selection** | Unclear where to spend applications | Scoring with open criteria + deduplication + prioritization |
| **Resume/application** | 1–2 hours of manual tailoring per JD; generic text fails ATS | CV Studio: JD-specific tuning, humanize, ATS bullets, PDF/DOCX in minutes |
| **Post-payment experience** | No application tracking; renewal = auto-charge | Tracker with follow-up cadence; honest renewal, one-click cancel |

**What blocks them from starting/renewing a subscription?**

| Segment | Blocking factor | Removed by |
|---|---|---|
| Tech core | "Yet another subscription trap"; installation via a repo | BYOK-free tier: try without a card and without cost to us; hosted version in one click |
| Mass market | Distrust of "AI magic"; fear of auto-charges | Open scoring methodology; pricing without auto-renewals, one-click cancel |
| Wave 2 | Competitors' EN-only interfaces; GDPR | 19 locales already in the product [C004]; local mode and data minimization |

**Conclusion (inference).** The audience segments not by profession but by entry barrier: the tech
core pays immediately for search automation, the mass market pays for "done for you", wave 2 pays
for language and privacy. Therefore the tier model (Free BYOK → Pro → Unlimited) serves all three
barriers with one ladder, and the sequence is EN-first with locale waves.

## FAQ-3: Strategic initiatives. Briefly justify each.

Mass-market competitors control the EN segment with budget and SEO; competing as "yet another text
generator" is a losing strategy. Of the five options considered (status quo, hosted SaaS, B2B
white-label, dual-license, shutting down commerce — analysis with red team in 03_options.md),
**option B — hosted freemium SaaS, global** was selected (decision D001): the only option that
grows the "paying users and ARR" axis with a solo developer's resources while respecting the
constraints (MIT core, trust of the local mode). The strategy rests on three initiative-drivers:

### 3.1 Honest monetization and a zero-friction entry

**The first driver** — capture the dissatisfaction with subscription traps: none of the competitors
lets you "try without a card". **The second driver** — BYOK turns the free tier from a cost center
into a zero: the user brings their own LLM key, free-tier inference costs nothing, and the upper
tiers monetize convenience (hosted scan + pipeline) instead of text generation.

Key directions:

- Three tiers: Free (BYOK, 3 resumes/mo) / Pro $12 / Unlimited $29 — a ladder answering the three barriers of FAQ-2.
- Pricing without auto-renewals, one-click cancel, discounted annual plan (the Markus segment) —
  the honest-pricing-as-differentiator hypothesis [C014] under test in the beta.
- A public Methodology page: ATS-scoring criteria are open (transparency as trust against the
  98%-ATS reality [C008]).

Unit economics calculation (assumptions [C016]): CM = $29 × 0.75 = **$21.75**; LTV = $21.75 / 0.08 =
**$271.88**; LTV/CAC = $271.88 / $60 = **4.53**; CAC payback = $60 / $21.75 = **2.8 months**;
break-even = $1,500 / $21.75 ≈ **69 paying users** — reachable on organic traffic (0.21% of
week-12 visitors in the funnel model).

**Beta funnel calculation — step by step** (model [S008], seed=7; starting base 3,000 visitors, 22%/wk growth):

| Step | Calculation | Week-12 result |
|---|---|---|
| Visitors | 3,000 × 1.22¹² | **32,603** |
| Signups | 32,603 × 5.5% | **1,793** |
| Activation (first resume) | 1,793 × 62% | **1,111** |
| Payment | 1,111 × 4.8% (2.8% × 1.72 uplift) | **53 paying** |
| MRR | 53 × $29 | **$1,537** |
| Run-rate | $1,537 × 12 | **$18,444 ARR/yr** |

### 3.2 Accelerating the "vacancy → ATS-ready resume" path

**The first driver** — compress the path from "found a vacancy" to "sent a tailored resume" from
hours of manual work to minutes of one pipeline: this directly grows Unlimited conversion.
**The second driver** — trust in the result: open scoring criteria and ATS bullets remove the
"AI slop" fear.

Key directions:

- Scan of ~129 boards + AI scoring 0.0–5.0 in one feed with deduplication.
- CV Studio: JD-specific tuning, humanize, ATS bullets, PDF/DOCX in one click.
- Application tracker with follow-up cadence — retention inside the product, not in the user's spreadsheet.

### 3.3 Global coverage on ready-made locales and OSS-driven distribution

**The first driver** — 19 locales already exist in the product [C004]: enabling a locale is an
operational decision, not development; competitors cover EN+5 [C007]. **The second driver** — the
OSS core as a distribution channel: the GitHub audience is a free funnel top for the hosted version
(conversion "local user → cloud payer").

Key directions:

- Locale waves: EN (US/EU) → DE/ES/PT-BR → JA/ZH; the next wave opens only after the previous one's conversion is confirmed.
- Local payment models: annual plans (the €100–120 segment [C018]) without auto-renewals.
- OSS track: the MIT version keeps evolving in parallel; hosted is opt-in — "the cloud is a choice,
  not a requirement": the local-mode promise stays intact [C001][C019].

**Conclusion (inference).** The three initiatives close the three barriers of FAQ-2 (price trust,
result trust, language/privacy) and rely only on existing product assets — therefore the plan is
feasible by a solo developer within a 12-month horizon.

## FAQ-4: Tactics. Detail each initiative into specific tactics

| Strategic initiative | Focus | User's needs & desires | Solutions (tactics) |
|---|---|---|---|
| **Honest monetization** | BYOK-free launch | Try without a card or auto-charge; understand what they pay for | Free tier with a BYOK key (zero cost to us); 3 resumes/mo limit with an honest "what unlocks" upgrade screen |
| | Pricing page | Price without fine print; fear of auto-charges [C006] | A tariff table with explicit price and term; one-click cancel; annual −20% |
| | Launch positioning | "Why are you better than Jobscan at $49.95?" [C002] | The message "Open source. Local-first. Honest pricing."; a competitor price comparison table on the landing |
| **"Vacancy → resume" path** | Scan + scoring | Not wasting applications on irrelevant roles | A 129-board feed with 0.0–5.0 scoring and filters; deduplication |
| | CV Studio | A JD-specific resume in minutes that passes ATS | JD tuning + humanize + ATS bullets; PDF/DOCX; open scoring methodology |
| | Tracker | Not losing applications and follow-ups | Kanban + follow-up cadence + reminders; funnel statistics |
| **Global coverage** | Locale waves | Native-language interface and resume conventions | DE/ES/PT-BR after the EN conversion threshold; JA/ZH as wave three |
| | Local payments | Annual plan without auto-charges | Discounted annual plans; local payment methods per wave |
| | OSS distribution | "I can check the code myself" | README funnel into hosted; stars/forks as social proof; HN/PH launch |

## FAQ-5: High-level implementation plan

To hit the targets (FAQ-6), each initiative gets a dedicated focus block from the solo developer
with a weekly funnel review; the community track (MIT version) runs in parallel without pause.

Expected contribution split by week 12:

- 50% — "Vacancy → resume" path (Unlimited conversion: the primary monetized value);
- 30% — Honest monetization (BYOK-free + the pricing page: the funnel entrance);
- 20% — Global coverage (preparing the DE/ES/PT-BR wave; enabling it after the threshold).

Within each initiative, high-priority tactics ship first (tiers, BYOK-free, scan+scoring), then
medium (tracker, methodology), then basic (local payments, JA/ZH). **Timing is tied to the hiring
season**: the beta launches into the December lull so the January hiring peak is met with
accumulated statistics; locale waves — into the next peak.

Decision D001 [C019]: beta in 3 EN geos by 2026-12-15 · 90 days of observation · review 2027-02-10 ·
continue branch: paid ≥ 40 by week 12 with activation ≥ 50% → scale channels, open the DE/ES/PT-BR
wave · change branch: paid 20–40 → rebuild the tier/price ($19?), strengthen activation onboarding ·
stop trigger: paid < 20 with activation < 35% → close the commercial branch, the project stays OSS.

## FAQ-6: Success metrics. KPIs for evaluating the strategy

KPIs are set in two directions:

**1) Business**

- MRR by week 12: **≥ $1,500** (funnel model: 53 paying × $29 [S008]; continue threshold — ≥ 40 paying);
- Signup → paid conversion: **≥ 4%** (freemium benchmark 2–5% [C020]);
- Annual-plan share among payers: **≥ 30%** (testing the Markus hypothesis [C018]);
- Non-EN wave share of new payers after locales open: **≥ 20%**;
- Actual LTV/CAC: **≥ 3** (model: 4.53) — below 3, paid channels stay closed.

**2) Product**

- Activation (first resume): **≥ 50%** of signups;
- Time to first resume: **≤ 15 minutes** from signup (event-measured);
- Clicks from "vacancy" to "sent resume": **−50%** vs the manual path;
- Paying churn: **≤ 10%/mo** (the dominant LTV parameter — step 3 of the FAQ-3 calculation);
- Trust counter-metrics: GitHub stars (drop < 30%), GDPR complaints (≤ 5), beta NPS ≥ 30.

Counter-metrics are early signals of the "local and honest" promise breaking: each maps to a
specific red-team hit and has a pre-written action (06_validation_plan.md).

---

**Sources**

(The registry holds 10 sources S001–S011 — S003 was merged into S006 during deduplication.)

1. WiseGuy Reports — Resume Builder Market; MarketSizeAndTrends — Resume Builder Market ($1.2–2.4B range) — [S006]
2. SkyQuest — Online Recruitment Market $37.97B (2025) — [S007]
3. Employ Inc. / Resume Now / Novoresume / Greenhouse — AI-usage surveys 31–74%; Kickresume — 1.2M AI users in 2025 — [S005]
4. Jobscan — 98% of Fortune 500 use ATS — [S007]
5. Rezi/Kickresume/Teal/Enhancv/Zety/resume.io pricing pages; Kickresume — 6 UI languages — [S004]
6. Product site and README, cvstart.org / career-ops-ui — [S001][S002]
7. Synthetic interview, Sarah (US) — hypothesis [S009]
8. Synthetic interview, Markus (Berlin) — hypothesis [S010]

> Synthetic interviews are flagged origin=synthetic and serve as hypotheses to validate, not proof
> of demand. The full evidence-backed version — REPORT.md; the document assembly method —
> knowledge/templates/SIX_PAGER_PROMPT.md.
