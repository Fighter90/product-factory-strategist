# Стратег Фабрики продуктов

**[RU](README.md) · [EN](README_EN.md)**

ИИ-агент для руководителя цифрового продукта: от размытого запроса («почему падает удержание», «кому продавать
новый сервис», «что сказать аудитории») — к **проверяемой** картине ситуации, содержательно разным вариантам
и согласованным продуктовой и коммуникационной стратегиям. После решения агент хранит его основания, следит
за обязательствами и пересматривает выводы при новых данных.

Это папка-репозиторий: инструкции, наборы знаний по категориям (стратегия · экономика · продукт · UX ·
данные · платформы · Gen AI), 121 навык, 8 субагентов, 4 хука
и CLI/MCP-инструменты на чистом Python (ноль зависимостей). Работает в Claude Code, Cursor, Codex, OpenCode,
Windsurf, Copilot.

**Ссылки:** [Сайт документации RU/EN](https://strategyproduct.ru) · [HELP на русском](docs/HELP.md) ·
[HELP in English](docs/HELP_EN.md) · [Реестр навыков](docs/SKILLS.md) · [CHANGELOG](CHANGELOG.md) ·
[Release v1.0.0](https://github.com/Fighter90/product-factory-strategist/releases/tag/v1.0.0)

---

## Быстрый старт (5 минут)

### Установка

```bash
git clone https://github.com/Fighter90/product-factory-strategist.git
cd product-factory-strategist
./scripts/install.sh                            # uv tool install -e . (или venv+symlink)
pfs --help                                      # CLI установлен: работает из любой папки
python3 -m tools.pfs doctor                     # установка и окружение: Python, pdftotext, база знаний
python3 -m unittest discover -s tests           # 396 тестов
```

Детали, PEP 668, обновление, удаление, тестирование и troubleshooting — [docs/INSTALL.md](docs/INSTALL.md).
Вне папки репозитория работает только установленный `pfs`; `python3 -m tools.pfs` — только из папки
репозитория (модуль `tools` ищется относительно текущего каталога).

Запуск в Claude Code (команда `claude` в папке репозитория) — напишите задачу: «Платная защита от спама
теряет подписчиков. Что делать и что говорить абонентам?»

Агент сам создаст проект, пройдёт блоки вопросов, построит исследование и покажет прогресс строкой
`Шаг N/12 · …`. «Стоп» — пауза, «уточни: …» — корректировка, «собери six-pager» — отчёт для комитета,
«сделай презентацию» — дека из six-pager. После перерыва откройте новый чат: состояние подастся автоматически.

---

## Демонстрационный проект: CVStart — полный разбор

Живой пример сквозного прогона: реальная задача руководителя, 12 шагов агента, пять вариантов с атакой red team, обе стратегии, six-pager на двух языках (формат референса стратегии роста: подпункты 1.1/1.2 и 2.1/2.2, матрица тактик, KPI в двух плоскостях, сноски; черновик собирает `pfs export --six-pager`, спецификация — `knowledge/templates/SIX_PAGER_PROMPT.md`) с Excel-моделью. Проект лежит в `projects/демо/`, скриншоты продукта — в `projects/демо/outputs/img/` и `site/assets/`.

### Задача и продукт

**Запрос руководителя (дословно):** «Разработать коммерческую версию cvstart.org и стратегию вывода на рынок на весь мир».

**Продукт:** [cvstart.org](https://cvstart.org/) ([github.com/Fighter90/career-ops-ui](https://github.com/Fighter90/career-ops-ui)) — открытый (MIT) AI-конструктор резюме и поиска вакансий: скан ~129 джоб-бордов, AI-скоринг 0.0–5.0, CV Studio, PDF/DOCX, cover letters, трекер, карта вакансий; 100% локально; 18 LLM-провайдеров BYOK; 19 языков; ~7 602 автотеста; монетизации нет.

Ось сравнения вариантов — платящие подписчики и ARR; ограничения: MIT-core остаётся бесплатным и открытым, соло-разработчик, сохранить доверие локального/приватного режима.

Сайт и README продукта зарегистрированы первыми источниками (S001–S002, origin=own).

![Лендинг CVStart](site/assets/cv_landing_ru.jpg)

### Как агент работал: 12 шагов

| Шаг | Что происходило | Команды / факты |
|---|---|---|
| 0 · Бриф | ≤3 вопроса руководителю: решение (стратегия коммерциализации + GTM), ось (платящие/ARR), ограничения (MIT-core, соло, локальный режим). Человек подтвердил бриф | `pfs new`, `pfs answer`, `00_brief.md` |
| 1 · Источники | 10 источников (S001–S002, S004–S011 — S003 объединён с S006 при дедупликации): сайт и README продукта, рынок resume builders, цены конкурентов, рекрутинг/ATS, синтетическая воронка, 2 ИИ-респондента, выбор руководителя | `pfs source add` ×10 |
| 2 · Исследование | 20 утверждений с типами (12 фактов, 4 гипотезы, 4 допущения) и силой A–D: resume builders $1,2–2,4 млрд (диапазон — агрегаторы расходятся ×2), AI-сегмент CAGR 13,1%, онлайн-рекрутинг $37,97 млрд (2025), ATS у 98% F500 | `pfs claim add` ×20 |
| 3 · Дискавери | 2 синтетические персоны (Sarah 32, EN-сегмент; Markus 35, Берлин) — честно помечены origin=synthetic, дали только гипотезы; 7 конкурентов $8–40/мес с автопродлениями (Zety, resume.io, Novoresume, Kickresume, Enhancv, Teal, Rezi) | `pfs interview save`, S009–S010 |
| 4 · Ситуация | Известно / не знаем / противоречия: внутренних метрик hosted-версии нет (её ещё не существует) — честный пробел; рыночные оценки — диапазонами | `02_situation.md` |
| 5 · Варианты | 5 содержательно разных A–E, включая «оставить как есть» (A) и «закрыть коммерческую ветку» (E) | `03_options.md` |
| 5 · Red team | Отдельный субагент атаковал каждый вариант: **15 возражений + 5 скрытых допущений** (20 ударов) — все встроены порогами плана проверки | субагент red-team |
| 6 · Выбор | Пауза человека: руководитель выбрал **B — hosted freemium SaaS** (записано источником S011) | `pfs answer`, S011 |
| 7 · Стратегии | Продуктовая (Free BYOK / Pro $12 / Unlimited $29; opt-in облако при локальном MIT-core; честный прайсинг без автопродлений; волны локалей EN → DE/ES/PT-BR → JA/ZH) + коммуникационная с таблицей «обещание → подтверждение» | `04/05` |
| 8 · Проверка | 90 дней: продолжить ≥40 платящих / изменить 20–40 / остановить <20 при activation <35%; контр-метрики: звёзды GitHub, GDPR-жалобы, NPS ≥30, инференс free ≤$200/мес | `06_validation_plan.md` |
| 9 · Review | Автопроверка `check --strict` = **100/100**; six-pager RU/EN (MD · PDF · DOCX) + 4 книги Excel; экономика [C016]: ARPU $29, CM $21,75, LTV ≈ $271,88, LTV/CAC ≈ 4,5, брейк-евен ≈ 69 платящих; синтетическая воронка [S008] — метод, не прогноз | `pfs calc all`, `pfs export --six-pager` |
| 10 · Решение | D001: бета в 3 EN-гео к 2026-12-15, пересмотр 2027-02-10, основания C019/C013/C014/C016/C005/C006 | `pfs decision add` |
| 11 · Мониторинг | Открыт: `pfs decision due` следит за бета-обязательством и датой пересмотра | шаг in_progress |

Синтетика (персоны и воронка) зарегистрирована с `origin=synthetic` — инструмент не даёт записать на неё
факты: это метод и гипотезы, не доказательство спроса.

### Что получилось

- **Рекомендация: вариант B — hosted freemium SaaS**: Free BYOK / Pro $12 / Unlimited $29, opt-in облако
  при локальном MIT-core, честный прайсинг без автопродлений, волны локалей EN → DE/ES/PT-BR → JA/ZH.
  B2B-лицензии (D), open-core-переход (C) и статус-кво (A) — осознанные отказы.
- **Экономика [C016]**: ARPU $29 → контрибуция $21,75; LTV ≈ $271,88; LTV/CAC ≈ 4,5; брейк-евен ≈ 69 платящих
  (чувствительность — в Excel).
- **Синтетическая воронка [S008]** (метод, не прогноз): к нед. 12 — 53 платящих, MRR $1 537; воспроизводится
  скриптом `analysis/gen_synthetic.py` → `synthetic_funnel.csv`.

### Что посмотреть

| Артефакт | Путь |
|---|---|
| Бриф и план исследования | `projects/демо/outputs/00_brief.md`, `01_research_plan.md` |
| Ситуация и сегменты | `projects/демо/outputs/02_situation.md` |
| 5 вариантов + red team | `projects/демо/outputs/03_options.md` |
| Обе стратегии | `projects/демо/outputs/04_product_strategy.md`, `05_comms_strategy.md` |
| План проверки (90 дней) | `projects/демо/outputs/06_validation_plan.md` |
| Ревью качества | `projects/демо/outputs/07_quality_review.md` |
| **Six-pager RU** (MD · **PDF** · DOCX) — вычитанный комитетский документ | `projects/демо/outputs/SIX_PAGER_RU.md` · `.pdf` · `.docx` |
| **Six-pager EN** (MD · **PDF** · DOCX) — вычитанный комитетский документ | `projects/демо/outputs/SIX_PAGER_EN.md` · `.pdf` · `.docx` |
| Six-pager автосборки (`pfs export --six-pager`; его читает deck) | `projects/демо/outputs/SIX_PAGER.md` |
| Полный отчёт | `projects/демо/outputs/REPORT.md` |
| Excel-модель (4 книги) | `projects/демо/outputs/attachments/` (unit_economics · growth_model · cohort_retention · market_sizing) |
| Скриншоты продукта | `projects/демо/outputs/img/`, `site/assets/` |
| Синтетические интервью (2 персоны) | `projects/демо/interviews/synthetic/` |
| Синтетика + анализ данных | `projects/демо/analysis/` (gen_synthetic.py, synthetic_funnel.csv, md_to_pdf.py) |
| Реестр и журнал | `projects/демо/claims.jsonl`, `decisions.jsonl`, `log.jsonl` |
| Deck-презентация | `projects/демо/outputs/presentations/deck.html` |

### Сверка с заданием — где что в демо

| Требование задания | Где доказательство |
|---|---|
| **Обязательный минимум** | |
| Поставить задачу, ≤3 вопроса | `00_brief.md`; вопросы intake — только важное |
| Материалы + источник каждого сведения | 10 источников S001–S011 без S003 (`pfs source list`; S003 объединён с S006 при дедупликации); дедуп SHA-256; 20 утверждений C001–C020 с тегами типов и силы A–D |
| План от вопросов, меняющих решение; пробелы | `01_research_plan.md`; честные пробелы в `02_situation.md` (нет внутренних метрик hosted-версии) |
| ≥3 варианта, вкл. «оставить как есть» и «закрыть»; возражения | `03_options.md`: A–E; red team — 20 ударов (15 возражений + 5 скрытых допущений) |
| Продуктовая + коммуникационная стратегия | `04_product_strategy.md`, `05_comms_strategy.md`, таблица «обещание → подтверждение» |
| План проверки | `06_validation_plan.md`: 90 дней, пороги 40 / 20–40 / <20, контр-метрики, критерии решения |
| Workflow с паузами человека | 12 шагов, паузы на брифе (0), выборе B (6) и утверждении D001 (10) |
| Порядок в знаниях | инструкции / knowledge / projects/демо / state.json — раздельно |
| Продолжение после перерыва | состояние в state.json; `pfs status` восстанавливает контекст |
| Прозрачность | log.jsonl; цепочка C### → S###; `pfs impact` |
| **Дополнительный уровень** | |
| Интервью и синтетика | 2 ИИ-персоны (S009–S010), origin=synthetic — только гипотезы, чекер факты на них не пускает |
| Изображения и медиа | скриншоты продукта RU/EN в `outputs/img/` и `site/assets/`; сайт и README — источниками S001–S002 |
| Анализ данных | синтетическая воронка [S008]: `analysis/synthetic_funnel.csv`, воспроизводится скриптом |
| Поддержка решений и пересмотр | D001 + `pfs decision due`; `pfs impact` показывает затронутые выводы |
| Маршрутизация, skills/hooks/subagents | `pfs route` → сценарий вывода на рынок; red-team субагент |
| MCP и CLI | CLI `pfs` (25+ команд) + MCP 18 инструментов |
| Six-pager для комитета | RU и EN, каждый в трёх форматах (MD/PDF/DOCX) + 4 книги Excel |
| Качество | `pfs check --strict` = 100/100 |

### Как повторить

```bash
python3 -m tools.pfs use демо                        # переключиться на демо
python3 -m tools.pfs status                          # где остановились (шаг monitoring)
python3 -m tools.pfs next                            # что решать сейчас
python3 -m tools.pfs --project демо check --strict   # quality gate: 100/100
# своя задача:
python3 -m tools.pfs new "Название" "Запрос дословно"
```

## Как агент работает: 12 шагов

На каждом шаге агент **читает обязательные карты базы знаний** (печатаются в `pfs step`), проходит
**вопросный блок** (`pfs questions <шаг>` — 1–3 вопроса руководителю, пропуск — только через журнал)
и упирается в **ворота качества**. Фазы двойного романа: Discover (0–3) → Define (4–6) → Develop (7–9) →
Deliver (10–11).

```mermaid
flowchart TD
  Q["запрос руководителя"] --> R["route: сценарий · карты · модели"]
  R --> S0["0 intake: бриф"] --> S1["1 sources: источники"] --> S2["2 research: исследование"] --> S3["3 discovery: персоны/JTBD"] --> S4["4 situation: ситуация"] --> S5["5 options: варианты + red team"] --> S6{{"6 choice: выбор — ЧЕЛОВЕК"}} --> S7["7 strategy: стратегии"] --> S8["8 validation: проверка"] --> S9["9 review: ревью + six-pager"] --> S10{{"10 decision: решение — ЧЕЛОВЕК"}} --> S11["11 monitoring: мониторинг"]
  S6 -.->|"pfs questions"| QB["вопросные блоки"]
  S9 --> DECK["six-pager + 4 Excel"]
  S11 -->|"новые данные"| REF["impact → supersede → rebase"]
```

| # | Шаг | Что делает агент | Карты (обязательные) | Вопросный блок | Ворота |
|---|---|---|---|---|---|
| 0 | intake | ≤3 вопроса, бриф, допущения | M-brief-hypotheses, M-customers, M-jtbd | intake-* | **человек подтверждает** |
| 1 | sources | Сайты/PDF/DOCX/XLSX/CSV → S###, дедуп, защита | M-source-criticism, M-research-types | intake-constraints | домены разрешены |
| 2 | research | План от вопросов, меняющих решение; расчёты; интервью | M-research-types, M-quant-methods, M-ab-testing, M-sql-for-pm | discovery-jtbd | вопросы закрыты или пробел назван |
| 3 | discovery | Персоны, JTBD, альтернативы пользователя | M-jtbd, M-audience-research, M-customers | discovery-segment | сегмент+персоны зафиксированы |
| 4 | situation | Известно/не знаем/противоречия | M-source-criticism, M-external-environment, M-competitors | situation-gaps | `pfs check` |
| 5 | options | ≥3 варианта + red team + фальсификаторы | M-goals-drivers-bets, M-risks, M-double-diamond, M-lean-canvas | options-criteria | check + red team |
| 6 | choice | Сравнение и рекомендация | M-decision-daci | choice-reversibility | **человек выбирает** |
| 7 | strategy | Продуктовая + коммуникационная | M-usp, M-product-communication, M-monetization, M-unit-economics | strategy-promise | обещания ↔ продукт |
| 8 | validation | Метрика, база, срок, контрметрики | M-ab-testing, M-success-metrics | validation-metric | 5 разделов |
| 9 | review | check + рубрика + six-pager с Excel | M-six-pager, M-source-criticism | — | рубрика ≥ порога |
| 10 | decision | Основания, ответственные, обязательства | M-decision-daci, M-model-validation | decision-commitments | **человек утверждает** |
| 11 | monitoring | Сроки, новые данные, пересмотр | M-loyalty-metrics | — | `pfs decision due` пуст |

---

## Архитектура

```mermaid
flowchart TB
  U["Руководитель продукта"] -->|"запрос · ответы на блоки вопросов"| ENV
  subgraph ENV["LLM-среда (Claude Code / Cursor / OpenCode / Codex…)"]
    AG["AGENTS.md — процесс 12 шагов, правила"] --> SK["skills: 120<br/>(базовые 13 + product-skills 27 + личная 74 + интеграции 6: sdd · deck · premortem · board-of-directors · hallmark · rea)"]
    AG --> SUB["subagents: 8<br/>researcher · red-team · evidence-auditor · synthetic-respondent · data-analyst · ux-analyst · comms-strategist · router"]
    AG --> HK["hooks: 5<br/>SessionStart · PreWeb-домены · PostTool-журнал · Stop-стоимость (+ общий модуль)"]
  end
  ENV -->|"CLI: pfs … · MCP: pfs-strategist"| TOOLS
  subgraph TOOLS["tools/pfs — детерминированные гарантии (stdlib only)"]
    P["projects/&lt;slug&gt;<br/>state · outputs · calcs.json"] --> S["sources S###<br/>дедуп · SSRF · инъекции"]
    S --> CL["claims C###<br/>fact/hypothesis/forecast/assumption/inference · сила A–D"]
    CL --> CH["check --strict<br/>quality gate по рубрике"]
    CAL["calc → 4 книги Excel<br/>лист «Ввод» + формулы"] --> EX["export<br/>REPORT.md · SIX_PAGER.md (FAQ-1…6)"]
    CH --> EX
    DEC["decisions D###<br/>основания · обязательства"] --> MON["decision due<br/>что решать сейчас"]
  end
  KB["knowledge/ — 89 карт по категориям (RU) + 89 EN-зеркал — полная двуязычная база (methods_en/) + INDEX_EN.md<br/>+ фреймворки: Double Diamond · Lean Canvas · RICE/ICE/WSJF · AARRR/HEART/Кано"]
  ENV -->|kb search / route| KB
  FEY["Feynman (feynman.is)<br/>deepresearch · lit · compare"] -->|"provenance → первоисточники → S###"| S
  SUB -->|"отчёты"| ENV
  EX --> ATT["outputs/attachments/*.xlsx<br/>пересчитываются при открытии"]
```

Четыре слоя, которые нельзя перепутать: **инструкции** (AGENTS.md, skills) ≠ **знания** (knowledge/) ≠
**материалы проекта** (projects/`<slug>`) ≠ **состояние** (state.json, *.jsonl). Прежний ответ агента не
становится фактом: он хранится как `inference` с основаниями; при отзыве основания `pfs check` помечает
все места, где на него ссылаются.

---

## Навыки: структура и как их вызывать

```mermaid
flowchart TB
  SK["121 навык"] --> B["Базовые 13: по шагам процесса<br/>intake · research · situation · options · strategy · validation · decision-support · data-analysis · interviews · ux-review · six-pager · deep-research · strategist"]
  SK --> P["Product-skills 27: процедуры методов<br/>market-sizing · unit-economics · traction-modeling · solution-design · problem-design · …"]
  SK --> L["Личная библиотека 75<br/>дизайн · маркетинг · наука · документы/медиа · режимы мышления · мета"]
  SK --> INT["Интеграции 6<br/>hallmark · board-of-directors · premortem · rea · sdd · deck"]
  B & P & L & INT --> INV["Вызов: авто по триггерам · явно «используй skill X» · по шагам процесса"]
```

**Структура (121):** четыре группы.
- **Базовые 13** — шаги процесса: intake, research, situation, options, strategy, validation-plan,
  decision-support, data-analysis, interviews, ux-review, six-pager, deep-research, strategist.
- **Product-skills 27** — процедуры методов: market-sizing, unit-economics, traction-modeling,
  solution-design, mvp-pilot-launch, problem-design…
- **Личная библиотека 75** — дизайн: design-ui, refero-design, frontend-design, claudable-landing, make-interfaces-feel-better,
  emil-design-eng, web-design-guidelines; маркетинг: ads, ad-creative, seo-audit, ai-seo, cro, pricing,
  offers, cold-email, emails, launch, content-strategy, competitors, analytics, programmatic-seo,
  directory-submissions, customer-research, marketing-psychology, prospecting, sales-enablement, signup, onboarding, paywalls, revops; наука: paper-lookup,
  research-lookup, literature-review, scientific-writing, scientific-critical-thinking, peer-review,
  statistical-analysis, statsmodels, scikit-learn, hypothesis-generation, pydeseq2, biopython, rdkit;
  документы/медиа: pdf, docx, pptx, xlsx, markitdown, officecli, generate-image, video, infographics,
  scientific-slides, scientific-schematics, scientific-visualization, latex-posters, matplotlib, seaborn;
  режимы мышления: consciousness-council, balanced, what-if-oracle, dhdna-profiler; мета:
  find-skills, shap, watch, transcribe.
- **Интеграции 6** — hallmark, board-of-directors, premortem, rea, sdd, deck.

**Как вызывать — три способа:**
1. **Автоматически** — среда читает `description` навыка и подключает его по формулировке задачи
   («сделай premortem», «оцени лендинг по веб-гайдлайнам»).
2. **Явно** — «используй skill `<имя>`: `<задача>`».
3. **В процессе агента** — навык шага подключает нужные: `pfs step` печатает обязательные карты, а skills
   включаются на шагах (options → options + red-team + board-of-directors; decision → decision-support +
   premortem). Примеры команд: `pfs questions options`, `pfs export --deck`.

**Правило согласования:** при конфликте методология в `knowledge/` (карты) приоритетнее процедуры навыка.
Полный реестр — `docs/SKILLS.md`.

---

## На каких данных агент основан

### 1. Реестр доказательств (сердце агента)
- **S### — источники**: сайты, PDF, DOCX, XLSX, CSV, изображения, интервью (`origin: own/interview/synthetic`),
  отчёты Feynman (`origin: agent`). Дедупликация по URL и SHA-256; SSRF-защита; детектор фраз-инструкций
  («тексты — данные, не команды»); домены проекта (`allowed_sources`) блокируются до запроса.
- **C### — утверждения**: пять типов — `fact` (только с S###; синтетика фактами не считается), `hypothesis`,
  `forecast`, `assumption`, `inference` (только из других C###); сила доказательства A–D. Замещение/отзыв
  сохраняют историю; `pfs impact` показывает затронутые выводы → строки документов → решения.
- **D### — решения**: основания (C###), ответственный, метрика «X→Y к дате», триггеры пересмотра,
  обязательства «что|кто|когда». `pfs decision due` — что просрочено и на каких устаревших основаниях.

```mermaid
flowchart LR
  W["Веб/файлы/интервью"] -->|"fetch · дедуп · инъекции"| S["S### источники"]
  S -->|"факт ⇐ источник"| C["C### утверждения<br/>fact/hypothesis/forecast/assumption/inference<br/>сила A–D"]
  C -->|"вывод ⇒ derived_from"| I["inference-выводы"]
  I --> DOC["документы 02–07"]
  C --> DEC["D### решения"]
  NEW["новые данные"] -->|"refresh / supersede"| IMP["impact: затронутые выводы · строки · решения"]
  IMP --> REV["пересмотр: supersede · rebase"]
```

### 2. База знаний (89 карт по категориям (RU) + 89 EN-зеркал — полная двуязычная база и EN-индекс)
Наборы знаний по категориям: стратегия и рост · юнит-экономика и монетизация · продуктовый менеджмент ·
UX и клиентские метрики · анализ данных и A/B · платформенные решения · Gen AI в продукте. Поверх —
фреймворки: Double Diamond, Lean Canvas, RICE/ICE/WSJF, HADI, AARRR/HEART/Кано. Только методики —
без брендов. Фреймворковый слой: **Double Diamond** (маппинг на 12 шагов), **Lean Canvas**
(9 ячеек с C###), **обзор фреймворков** («фаза → инструмент»). Поиск: `pfs kb search`
(BM25, русский стемминг); на каждом шаге агент получает обязательный список карт.

### 3. Framework для исследований (Feynman, feynman.is)
Для сложных вопросов плана агент запускает опенсорсный research-агент: `feynman deepresearch|lit|compare`
(AlphaXiv, Semantic Scholar, OpenAlex, arXiv, PubMed, Crossref, веб; проверка цитат; provenance-файл).
Правила переноса результатов в агент: provenance → **первоисточники регистрируются как S###**; цифры —
факты только из первоисточников; сам отчёт Feynman — `origin: agent`, опираться на него можно только
гипотезами (инструмент не даст записать факт). Телеметрия выключается; ключи OpenAlex/S2 — в `.env`.
Навык: `deep-research`. Плюс 27 процедур product-skills и вопросные блоки `config/question_blocks.json`.

### 4. Числа — из расчётов, не «из головы»
`pfs calc` строит 4 книги Excel на формулах (юнит-экономика с LTV/CAC/пейбеком и чувствительностью,
модель роста 12 мес, когортное удержание, PAM→TAM→SAM→SOM + PESTEL): лист «Ввод» — редактируемые
параметры из `calcs.json` (каждое значение — C###), кэш значений для предпросмотра, пересчёт при открытии.
Каркас `calcs.json` собирает `pfs calc scaffold` из документов 02/04/06/07: найденные числа — со своим
C/S-тегом в `_notes`, ненайденные — null + подсказка в `_hints` (ручная дописка — только null-поля).

---

## Six-pager для комитета

`pfs export --six-pager` собирает отчёт в структуре стратегического референса: FAQ-1 состояние ·
FAQ-2 персоны · FAQ-3 инициативы и возражения · FAQ-4 тактики · FAQ-5 план и проверка · FAQ-6 метрики ·
таблица Excel-приложений. Числа в тексте совпадают с книгами; полные доказательства — REPORT.md
(приложения A–E: реестр утверждений, источники, решения, стоимость, Excel). Презентация: навык `deck`
(officecli → PPTX, HTML-fallback, визуалы Higgsfield, web-версия Lovable).

---

## CLI (полный список)

| Команда | Назначение |
|---|---|
| `pfs new / list / use / status [--brief]` | проекты и состояние |
| `pfs route "<запрос>" [--override --economy --json]` | сценарий, карты, план моделей |
| `pfs questions <шаг\|блок>` | вопросные блоки для настраиваемости |
| `pfs next` | «что решать сейчас»: шаг, обязательства, устаревшие источники с командой refresh, пересмотры |
| `pfs step <шаг> in_progress\|done [--note --next]` | отметка шага + обязательные карты |
| `pfs ask / answer / question` | паузы с человеком |
| `pfs source add/list/show [--text-file --url --origin --force]` | источники S### |
| `pfs source refresh S###` | обновить web-источник: sha256-дельта, бэкап, impact |
| `pfs claim add/list/supersede/retract/rebase [--kind --source --from --grade]` | реестр C### |
| `pfs check [--strict --json] · pfs impact C###` | качество и влияние изменений |
| `pfs review lock` | lock вердикта review; правки реестра после lock → «вердикт review устарел» в check/status/export |
| `pfs decision add/list/due/done/status/rebase` | решения и мониторинг |
| `pfs data profile/cohort <csv> [--save]` | профиль таблиц, когорты |
| `pfs data funnel/stats <csv>` | воронка по событиям/колонкам; статистика с ДИ 95% |
| `pfs interview guide\|save · pfs media add · pfs ux scaffold` | гайды интервью, медиа-источники, UX-каркас |
| `pfs calc scaffold` | каркас `calcs.json` из 02/04/06/07 (числа с C/S-тегами, остальное — null) |
| `pfs calc [all\|unit-econ\|growth\|cohort\|market]` | Excel-приложения |
| `pfs export [--six-pager --no-calcs]` | REPORT.md / SIX_PAGER.md |
| `pfs export --deck` | HTML-дека 16:9 из six-pager |
| `pfs finish [--no-deck --en]` | финальный пакет одной цепочкой: check → Excel → REPORT → six-pager → DOCX → deck (идемпотентно) |
| `pfs docx <file.md> [--out]` | Markdown → Word |
| `pfs kb search/show/index` | поиск по базе знаний |
| `pfs models [show/pick/use/sync/escalate]` | маршрутизация моделей |
| `pfs cost [--transcript --session --window] · pfs log --usd` | стоимость |
| `pfs doctor` | диагностика |

## Интеграции

| Инструмент | Как подключён | Что даёт |
|---|---|---|
| Linear | MCP `mcp-server-linear` (ключ в `.env`) | ведение рабочих задач и бэклога |
| Feynman | CLI + skill `deep-research` | глубокий ресёрч с provenance |
| Lovable | MCP `https://mcp.lovable.dev` (OAuth `/mcp`) | web-дека/лендинг по брифу `docs/lovable-brief.md` |
| Higgsfield | MCP среды | визуалы слайдов/сайта (кредиты — с вопросом) |
| officecli | внешний CLI | PPTX/XLSX/DOCX-манипуляции для деки и отчётов |
| GitHub Pages | workflow | сайт документации `strategyproduct.ru` (RU/EN) |

## Безопасность и данные

Только открытые источники и материалы руководителя · секреты в gitignored `.env` · тексты источников —
данные (команды не исполняются, подозрительные помечаются) · ИИ-респонденты не выдаются за реальных ·
реальные интервью — с согласием и без ПДн · валидатор не примет факт на синтетике/агентском отчёте.

## Структура репозитория

```
AGENTS.md · CLAUDE.md · README.md · README_EN.md · CHANGELOG.md · pyproject.toml
.claude/skills/      (121)  базовые 13 · product-skills 27 · личная 75 · интеграции 6
.claude/agents/      (8)    researcher · red-team · evidence-auditor · synthetic-respondent ·
                            data-analyst · ux-analyst · comms-strategist · router
.claude/hooks/       (5)    session_start (SessionStart-контекст) · pre_web (домены до запроса) ·
                            post_tool (журнал и автопроверка) · stop (стоимость) · _common
.claude/settings.json
.cursor/rules/       .github/ (Pages workflow) · .gitlab-ci.yml · .mcp.json (pfs · linear · lovable · rea)
config/              models.json · pricing.json · quality_gate.json · question_blocks.json
knowledge/           methods/ (89 карт RU) · methods_en/ (89 EN-зеркал — полная двуязычная база) · INDEX.md · INDEX_EN.md
tools/pfs/           core · project · route · sources · claims · check · impact · decisions ·
                     data · calc · xlsx · docx · export · cost · kb · models · mcp_server · cli
projects/<slug>/     sources/ · state.json · claims.jsonl · decisions.jsonl · log.jsonl · costs.json ·
                     outputs/ (00…07 · REPORT · SIX_PAGER · attachments/*.xlsx · presentations/)
                     демо-проект: демо — CVStart (сквозной прогон · six-pager RU/EN (MD/PDF/DOCX) ·
                     Excel)
site/                index.html · demo.html · materials.html · help.html (RU/EN)
docs/                HELP.md · HELP_EN.md · ARCHITECTURE · SKILLS · COMPLIANCE · SUBMISSION ·
                     VERIFICATION · docx/ · demo/ · lovable-brief…
tests/               (396)
```
