# CVStart · Six-pager (EN)

> **Commercial version & global go-to-market strategy for cvstart.org** — a complete 12-step run of the
> "Product Factory Strategist" agent (Nov 6–7, 2026). Committee format: every section follows the chain
> **"data → reasoning → calculation → conclusion"**. Screenshots are deliberately excluded — only
> verifiable logic, formulas and origin-tagged numbers. Evidence base: claims C001–C020, sources
> S001–S011, decision D001 (full registry — REPORT.md). Model figures rely on assumptions [C016][C020];
> market figures are ranges from aggregators [S006].

## FAQ-1. Current state

**Data — product.** CVStart (career-ops UI) is an open-source (MIT) AI resume builder and job-search
dashboard: scanning ~129 job boards (124 EN + 5 RU: hh.ru, Habr Career, GeekJob, GetMatch, Trudvsem),
AI fit-scoring of every vacancy 0.0–5.0 against the user's resume, CV Studio (JD-targeted tuning,
humanize, ATS bullets), PDF/DOCX export, cover letters, an auto pipeline, an application tracker with
follow-up cadence, a job map, mock interviews; 100% local (data stays with the user), 18 BYOK LLM
providers + keyless mode, 19 UI languages, ~7,602 automated tests [C001][C004]. No monetization yet:
"$0 forever", no public hosting [C002][C003].

**Data — market.** Resume builders: a $1.2–2.4B estimate range; the AI sub-segment $1.3 → 1.47B,
13.1% CAGR [C005]. Online recruitment: $37.97B in 2025, 7.1% CAGR to 2033 [C011]. 31–74% of job
seekers already use AI (2025–2026 surveys); 84% say AI made the search easier [C009]; 1.2M+ AI users
at Kickresume in 2025 [C010].

**Data — competitors.** 7 direct players — Zety, resume.io, Novoresume, Kickresume, Enhancv, Teal,
Rezi: freemium, paid tiers $8–40/mo, aggressive auto-renewals [C006]; language coverage EN+5 [C007];
ATS is used by 98% of the Fortune 500 [C008].

**Reasoning.**
1. **Engineering maturity ≠ commercial maturity.** The engineering asset exists (129 adapters,
   19 locales, 7,602 tests) but monetization is not switched on — meaning the asset is subsidized
   with no return; any commercial option must first pay back this support debt, not "earn on top".
2. **Market estimates diverge ×2** ($1.2B vs $2.35B across aggregators) — therefore every market
   conclusion below uses the **conservative floor of $1.2B**: if the case closes on the conservative
   number, it closes even harder on the optimistic one.
3. **AI has become a hygiene factor.** When 31–74% of job seekers already use AI, "having AI features"
   is not a differentiator — the differentiators are output quality, honest terms, and privacy.
4. **ATS-compatibility is purchase factor #1.** With 98% of the Fortune 500 on ATS, a resume that
   "fails ATS" devalues everything else; an open ATS-check methodology is a trust argument, not a
   marketing promise.
5. **All 7 competitors run the same model — a subscription trap.** This creates a verifiable
   positioning window of "honest pricing without auto-renewals": dissatisfaction with the pattern is
   supported by synthetic interviews [C017][C018] and testable in the beta.

**Capacity calculation (PAM→SOM funnel, Excel market_sizing).**
PAM 1.8B economically active job seekers → **TAM** = 1.8B × 30% (digital professions, EN-first
markets) = 540M → **SAM** = 540M × 40% (actively searching for 1–6 months) = 216M → **SOM** =
216M × 5% (a realistic 12-month share for a new entrant) = **10.8M users**. Sanity check: even
0.01% of SOM = 1,080 paying × $29 ≈ $31K MRR — the order of magnitude confirms the market is large
enough for a niche player without aggressive share-grabbing.

**Tension and its resolution.** "100% local" is a public promise [C001] — against a commercial
cloud. Resolution: an opt-in hybrid — the local core stays forever, the cloud is a choice; the
tension becomes a testable beta hypothesis (FAQ-5).

**Conclusion (inference).** The product is engineering-mature and commercially dormant; the market
grows at double digits in the AI sub-segment; competitors have opened the "honest pricing" window.
Therefore the commercial version is justified, and the main risk is not demand but the trust of the
local community; it is managed by product architecture (BYOK + opt-in) and measured by
counter-metrics (FAQ-5).

## FAQ-2. Users: segments and personas

| Segment | Who | Job to be done | Basis |
|---|---|---|---|
| Core (EN-first) | tech job seekers 25–40, US/EU, actively searching 1–6 months | "Find relevant openings across all sources and quickly tailor a resume for each one that passes ATS — without subscription traps or handing my data to someone's cloud" | [C017] |
| Wave 2 | non-EN segments: DE, ES, PT-BR, JA, ZH | "Think about my resume in my native language; local conventions matter more than price" | [C004][C018] |

**Persona hypotheses (synthetic [S009][S010] — testable hypotheses, not proof of demand).**
**Sarah, 32, software engineer (Austin):** tried Zety/Teal; furious about auto-renewals ("cancelled —
they charged me again"); refuses to keep her resume in someone else's cloud; would pay $10–15/mo,
$29 only if the tool actually finds jobs. **Inference:** $29 will not be paid "for text generation" —
it is justified only by the bundle "job scan + scoring + tracker", i.e. what is sold is the *search*
function, not generation; this confirms the tier model (FAQ-4).
**Markus, 35, product manager (Berlin):** existing tools are US-centric; interface and local
conventions matter more than price; GDPR-sensitive; accepts an annual €100–120 plan, categorically
against monthly auto-renewals. **Inference:** in non-EN segments willingness to pay is not lower, and
the persuasion levers differ — an annual plan and local communities work better than a monthly
subscription and paid targeting.

**Segment prioritization calculation.** Core EN-first: higher capacity (US/EU is the bulk of the
540M TAM), lower CAC (English-language Product Hunt / HN / SEO), higher competition (all 7
competitors are EN+5 [C007]). Wave 2: lower competition (narrow competitor language coverage),
higher readiness for annual payments [C018], but costlier channels and support. Hence — **waves in
sequence, not in parallel**: EN validates conversion and unit economics, then locales scale the
proven model without product changes (19 locales already exist [C004] — zero switching cost, only
operational).

**Conclusion (inference).** The core is EN-market tech job seekers with the "subscription trap + ATS"
pain; wave 2 is a deferred multiplier on ready-made locales. Therefore the product launches
EN-first with honest pricing as the headline message, and locales are switched on in waves after
conversion is confirmed (criterion — FAQ-5).

## FAQ-3. Strategic options: 5 variants + red team

| Option | Essence | ARR in 12 mo (model) | Sharpest red-team hit | Hidden assumption | Verdict |
|---|---|---|---|---|---|
| A. Status quo | free local OSS | $0 | $0 ARR on the "paying growth" axis; domain/CI/129 integrations subsidized forever; MIT lets a fork monetize your work (WordPress/WP Engine precedent) | locality is a mass-market selection driver | fails the brief |
| **B. Hosted freemium SaaS** | cloud, global: Free BYOK / Pro $12 / Unlimited $29 | $35–105K [C016][S008] | PII/GDPR liability and ToS-hostile scraping; "$0 forever" is a public promise; freemium conversion 2–5% [C020]; episodic product (landed a job — churned) | the OSS crowd will buy hosted | **selected** — with mitigations below |
| C. B2B white-label | licenses to universities and career centers | $24–60K [C020] | tenders/RFP/SOC2, 6–18-month cycles; a different product is needed (SSO, cohorts, reporting); vertical vendors own the niche | unmet white-label demand exists | postponed until presence |
| D. Dual-license | enterprise self-host + ATS integrations | $10–50K [C020] | legally void on top of MIT — rights already granted to everyone forever; Greenhouse/Workday serve employers, not candidates | enterprise will pay for what is already free | rejected |
| E. Shut down commerce | stays a non-commercial OSS | $0 | abandoning the asset at the widest market window; "non-commercial forever" blocks the future with backlash | the community will sustain itself (a myth — the Heartbleed effect) | the stop-loss path |

**Why B — the inference chain.**
1. The leader's axis is paying subscribers and ARR. A and E produce $0 by construction → excluded as
   growth strategies (E remains as the stop path).
2. C requires a sales motion (tenders, security review) that a solo founder does not have → the
   probability of closing a cycle within 12 months is ~0 → postponed, not rejected.
3. D is legally impossible on top of MIT without relicensing (fork risk + community loss) → rejected.
4. B is the only option that directly grows the axis; its risks (PII, trust, conversion) are
   **manageable**: PII → DPA and data minimization; trust → opt-in cloud on top of the local core;
   conversion → the BYOK-free tier removes both the barrier and the inference cost.
5. Therefore B with built-in mitigations dominates on "axis growth / risk controllability"; the
   leader's choice is recorded in D001 [C019].

**Red team → mitigations (20 hits: 15 objections + 5 hidden assumptions).**

| Red-team hit | Mitigation built into B |
|---|---|
| LLM inference eats the free-tier economics | BYOK-free tier: users bring their own key — free-tier variable cost ≈ 0 |
| "$0 forever" is a public promise; bait-and-switch | opt-in cloud; the MIT version stays; the local mode is never switched off |
| hosted GDPR/PII liability | data minimization, DPA, EU hosting in wave 2 |
| freemium conversion 2–5% [C020] | stop-loss thresholds (FAQ-5): if actuals fall below the model, the branch closes |
| a PH/HN spike that fades in days | the "open-source Jobscan alternative" SEO strategy — a long channel with no budget |

## FAQ-4. Tactics and unit economics (every calculation, step by step)

**Tactics** (each is a conclusion from FAQ-1–3):
1. **Three tiers** — Free (user's BYOK key, 3 resumes/mo) / Pro $12 (cloud AI) / Unlimited $29
   (129-board scan + auto pipeline + tracker). Reasoning: Sarah accepts $10–15, and $29 only for
   *search* [C017] → generation and search are separated across tiers.
2. **Opt-in cloud on top of the local MIT core** — the cloud is a choice, not a requirement.
   Reasoning: resolves the FAQ-1 tension while preserving the core asset — trust [C001][C019].
3. **Honest pricing**: no auto-renewals, one-click cancel, discounted annual plan. Reasoning: all
   competitors run auto-renewals [C006] → a differentiator with confirmed demand [C014].
4. **Language waves** EN (US/EU) → DE/ES/PT-BR → JA/ZH. Reasoning: 19 locales already exist [C004],
   competitors cover EN+5 [C007]; the next wave opens only after the previous one's conversion is
   confirmed.
5. **Open scoring methodology** — a public description of the ATS criteria. Reasoning: 98% of the
   F500 run ATS [C008]; transparency removes the "black magic" fear [C009].

**Unit economics — step-by-step calculation** (assumptions [C016]: ARPU $29; variable costs 25%;
CAC $60; churn 8%/mo; fixed costs ~$1,500/mo):

| # | Formula | Calculation | Result |
|---|---|---|---|
| 1 | CM = ARPU × (1 − variable share) | $29 × (1 − 0.25) = $29 × 0.75 | **CM = $21.75** |
| 2 | Average paying lifetime = 1 / churn | 1 / 0.08 | **12.5 months** |
| 3 | LTV = CM × lifetime (equivalent to CM / churn) | $21.75 / 0.08 | **LTV = $271.88** |
| 4 | LTV/CAC | $271.88 / $60 | **4.53** (health criterion ≥ 3) |
| 5 | CAC payback = CAC / CM | $60 / $21.75 | **2.76 ≈ 2.8 months** |
| 6 | Break-even = fixed costs / CM | $1,500 / $21.75 = 68.97 | **≈ 69 paying users** |

**Beta funnel calculation** (synthetic model [S008], seed=7, week-1 base = 3,000 visitors, 22%/wk
growth — a method illustration, not a forecast):
week-12 visitors = 3,000 × 1.22¹¹ ≈ **26,700** → signups = × 5.5% ≈ **1,470** →
activation (first resume) = × 62% ≈ **910** → payment = × 3.3% with a 6%/wk uplift ≈ **53 paying** →
MRR = 53 × $29 = **$1,537** → run-rate = $1,537 × 12 = **$18,444 ARR/yr**.
Cross-check vs break-even: 53 < 69 — the beta does not yet cover fixed costs, which is exactly what
the "continue at ≥ 40" criterion encodes, with scaling only after confirmation.

**Sensitivity** (Excel unit_economics — what happens when an assumption deviates):

| Scenario | Calculation | LTV | LTV/CAC | Interpretation |
|---|---|---|---|---|
| Base [C016] | 21.75 / 0.08 | $271.88 | 4.53 | green zone |
| Churn 10%/mo | 21.75 / 0.10 | $217.50 | 3.63 | acceptable |
| Churn 12%/mo | 21.75 / 0.12 | $181.25 | 3.02 | red zone — below the 3 criterion |
| ARPU $19 (tier rebuild) | $19 × 0.75 = $14.25; / 0.08 | $178.13 | 2.97 | requires a lower CAC |
| CAC $90 (paid channels) | 271.88 / 90 | $271.88 | 3.02 | only organic channels stay healthy |

**Sensitivity inference:** the model survives a deviation of any **single** assumption (churn up to
12% or CAC up to $90) but not two at once; hence the channel rule — organic first (PH/HN/SEO,
CAC ≈ $60), paid channels only after churn ≤ 10% is confirmed by actuals.

**Conclusion (inference).** At base assumptions the unit economics are healthy (4.53 ≥ 3, payback
< 3 months) and break-even is reachable on organic traffic (69 paying ≈ 0.23% of the model funnel's
signups); the safety margin is one parameter. Therefore: Unlimited $29 is the anchor tier, Pro $12
is the downgrade-retention path, and the annual plan (from [C018]) is the churn-reduction instrument
switched on in wave 2.

## FAQ-5. Implementation & validation plan (90 days)

**Plan logic.** 90 days ≈ 2 full job-seeker decision cycles (average active search is 1–6 months,
core 1–3 months): the beta sees both the first arrival and the first natural churn — it measures
both parameters of the unit model (conversion and retention), not just signups.

**Expectation by week 12** [S008]: 50–60 paying (model: 53), MRR ≥ $1,500, activation ≥ 50% of
signups. **Comparison base:** the funnel model + public freemium-conversion benchmarks of 2–5%
[C020] — there is no real history, so the comparison is weekly "model vs actual" with the gap
recorded.

**Decision thresholds (stop-loss logic):**
- **Continue** — paid ≥ 40, activation ≥ 50%, churn ≤ 10%/mo → scale channels, open the
  DE/ES/PT-BR wave (the next multiplier on a proven model).
- **Change** — paid 20–40 → rebuild tiers/pricing (the $19 hypothesis from sensitivity), strengthen
  activation onboarding; paid channels stay closed.
- **Stop** — paid < 20 with activation < 35% → the value hypothesis is unconfirmed: the commercial
  branch closes, the project stays OSS (option E), resources go to the community.

**Counter-metrics** (each proxies a specific red-team hit): GitHub stars/forks (a > 30% drop = the
community reads bait-and-switch) · GDPR complaints > 5 (the jurisdictional risk materializes) ·
free-tier inference > $200/mo (the free economics break) · beta NPS < 30 while signups grow
("growing trash").

**Decision D001** [C019]: grounds C019/C013/C014/C016/C005/C006 · commitment "hosted beta in
3 EN geos by 2026-12-15" · review 2027-02-10 · stop trigger — the "Stop" threshold above.

**Conclusion (inference).** The plan tests not "do they like it" but three numbers of the unit model
(conversion, activation, churn) on real money; every threshold has a pre-written action — this turns
the "success/failure" debate into arithmetic.

## FAQ-6. Success metrics

| Metric | Baseline | Target by week 12 | Type | Why this metric |
|---|---|---|---|---|
| Paying subscribers | 0 | ≥ 40 (model: 53) | NSM proxy | a direct money vote for the "scan+scoring" value — signups without payment prove nothing |
| MRR | $0 | ≥ $1,500 | revenue | MRR = paying × $29 — a derivative, but a discrete trigger for operational decisions |
| Activation (first resume) | — | ≥ 50% of signups | product | if generation never reaches a first result, the paid upgrade is impossible |
| Paying churn | — | ≤ 10%/mo | retention | the dominant LTV parameter (step 3 of FAQ-4); product episodicity makes it critical |
| LTV/CAC | model 4.53 | ≥ 3 actual | unit economics | the healthy-model boundary; below 3, growth via paid channels is forbidden |
| GitHub stars (counter) | current level | drop < 30% | OSS trust | an early signal that "$0 forever / local" is being read as bait-and-switch |
| Beta NPS (counter) | — | ≥ 30 | quality | growing signups at low NPS = burning the channel |

**Target-point calculation:** 40 paying × $29 = $1,160 MRR by week 12; at the 10% retention target
the same 40 payers carry an LTV base of $217.50 × 40 = $8,700 per cohort — against organic CAC spend
of ~40 × $60 = $2,400; the 3.63 ratio means scaling is justified only when both targets hold at once.

**Conclusion (inference).** The metric system closes the unit model: paying users prove value,
activation explains conversion, churn and LTV/CAC hold the economics, counter-metrics guard the
trust asset. No metric is vanity — each has a threshold and a pre-written action.

## Appendices (Excel workbooks, `outputs/attachments/`)

| File | Editable inputs (the "Input" sheet) | Recalculated |
|---|---|---|
| unit_economics.xlsx | ARPU, variable costs, CAC, churn | CM, LTV, LTV/CAC, payback, break-even, sensitivity |
| growth_model.xlsx | MAU, growth, conversion, AOV | the 12-month model |
| cohort_retention.xlsx | cohort sizes, retention curve | M1/M3/M6 retention |
| market_sizing.xlsx | PAM, funnel shares | TAM/SAM/SOM, environment factors |

Every "Input"-sheet value traces to a claim C###; formulas recalculate on open (Excel / Numbers /
LibreOffice). The full evidence-backed version — REPORT.md; the method for assembling this document —
knowledge/templates/SIX_PAGER_PROMPT.md.

> Inferences are marked "Conclusion"/"Inference" and rest only on C###/S### tags or the explicit
> assumptions [C016][C020] — no number in this document appeared without provenance.
