# Стратег Фабрики продуктов

**[RU](README.md) · [EN](README_EN.md)**

ИИ-агент для руководителя цифрового продукта: от размытого запроса («почему падает удержание», «кому продавать
новый сервис», «что сказать аудитории») — к **проверяемой** картине ситуации, содержательно разным вариантам
и согласованным продуктовой и коммуникационной стратегиям. После решения агент хранит его основания, следит
за обязательствами и пересматривает выводы при новых данных.

Это папка-репозиторий: инструкции, методическая база из 7 учебных курсов, 45 навыков, 8 субагентов, 4 хука
и CLI/MCP-инструменты на чистом Python (ноль зависимостей). Работает в Claude Code, Cursor, Codex, OpenCode,
Windsurf, Copilot.

**Ссылки:** [Сайт документации RU/EN](https://strategyproduct.ru) · [HELP на русском](docs/HELP.md) ·
[HELP in English](docs/HELP_EN.md) · [Реестр навыков](docs/SKILLS.md) · [CHANGELOG](CHANGELOG.md) ·
[Release v1.0.0](https://github.com/Fighter90/product-factory-strategist/releases/tag/v1.0.0)

---

## Быстрый старт (5 минут)

```bash
git clone https://github.com/Fighter90/product-factory-strategist.git
cd product-factory-strategist
python3 -m tools.pfs doctor                    # окружение: Python, pdftotext, база знаний
python3 -m unittest discover -s tests          # 55 тестов
# в Claude Code (команда claude в папке) напишите задачу:
# «Платная защита от спама теряет подписчиков. Что делать и что говорить абонентам?»
```

Агент сам создаст проект, пройдёт блоки вопросов, построит исследование и покажет прогресс строкой
`Шаг N/12 · …`. «Стоп» — пауза, «уточни: …» — корректировка, «собери six-pager» — отчёт для комитета,
«сделай презентацию» — дека из six-pager. После перерыва откройте новый чат: состояние подастся автоматически.

---

## Как агент работает: 12 шагов

На каждом шаге агент **читает обязательные карты базы знаний** (печатаются в `pfs step`), проходит
**вопросный блок** (`pfs questions <шаг>` — минимум 1–3 вопроса руководителю, пропуск — только через журнал)
и упирается в **ворота качества**. Фазы двойного романа: Discover (0–3) → Define (4–6) → Develop (7–9) →
Deliver (10–12).

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
    AG["AGENTS.md — процесс 12 шагов, правила"] --> SK["skills: 45<br/>(базовые + product-skills 27 + интеграции: sdd · deck · deep-research · premortem · board-of-directors · hallmark)"]
    AG --> SUB["subagents: 8<br/>researcher · red-team · evidence-auditor · synthetic-respondent · data-analyst · ux-analyst · comms-strategist · router"]
    AG --> HK["hooks: 4<br/>SessionStart · PreWeb-домены · PostTool-журнал · Stop-стоимость"]
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
  KB["knowledge/ — 72 карты из 7 курсов<br/>+ фреймворки: Double Diamond · Lean Canvas · RICE/ICE/WSJF · AARRR/HEART/Кано"]
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

### 2. База знаний (72 карты, 7 курсов + фреймворки)
Дистилляция курсов продуктовой магистратуры: стратегии роста · юнит-экономика и traction-модели ·
продуктовый менеджмент · UX и клиентские метрики · анализ данных (A/B c формулами MDE, SQL, дашборды,
прогнозирование, ML) · платформенные решения · Gen AI в продуктах. Только методики — без брендов.
Фреймворковый слой: **Double Diamond** (маппинг на 12 шагов), **Lean Canvas** (9 ячеек с C###),
**обзор фреймворков** (RICE/ICE/WSJF, HADI, AARRR/HEART/Кано — «фаза → инструмент»). Поиск: `pfs kb search`
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
| `pfs next` | «что решать сейчас»: шаг, обязательства, пересмотры |
| `pfs step <шаг> in_progress\|done [--note --next]` | отметка шага + обязательные карты |
| `pfs ask / answer / question` | паузы с человеком |
| `pfs source add/list/show [--text-file --url --origin --force]` | источники S### |
| `pfs source refresh S###` | обновить web-источник: sha256-дельта, бэкап, impact |
| `pfs claim add/list/supersede/retract/rebase [--kind --source --from --grade]` | реестр C### |
| `pfs check [--strict --json] · pfs impact C###` | качество и влияние изменений |
| `pfs decision add/list/due/done/status/rebase` | решения и мониторинг |
| `pfs data profile/cohort <csv> [--save]` | профиль таблиц, когорты |
| `pfs data funnel/stats <csv>` | воронка по событиям/колонкам; статистика с ДИ 95% |
| `pfs interview guide\|save · pfs media add · pfs ux scaffold` | гайды интервью, медиа-источники, UX-каркас |
| `pfs calc [all\|unit-econ\|growth\|cohort\|market]` | Excel-приложения |
| `pfs export [--six-pager --no-calcs]` | REPORT.md / SIX_PAGER.md |
| `pfs export --deck` | HTML-дека 16:9 из six-pager |
| `pfs docx <file.md> [--out]` | Markdown → Word |
| `pfs kb search/show/index` | поиск по базе знаний |
| `pfs models [show/pick/use/sync/escalate]` | маршрутизация моделей |
| `pfs cost [--transcript --window] · pfs log --usd` | стоимость |
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
AGENTS.md CLAUDE.md README.md README_EN.md CHANGELOG.md pyproject.toml
.claude/skills/ (45)  .claude/agents/ (8)  .claude/hooks/ (4)  .claude/settings.json
.cursor/rules/  .github/ (Pages workflow)  .mcp.json (pfs · linear · lovable)
config/   models.json · pricing.json · quality_gate.json · question_blocks.json
knowledge/ methods/ (72 карты) · templates/ · rubrics/ · INDEX.md
tools/pfs/ core · project · route · sources · claims · check · impact · decisions
           data · calc · xlsx · docx · export · cost · kb · models · mcp_server · cli
projects/<slug>/ sources/ · claims.jsonl · decisions.jsonl · log.jsonl · costs.json
                 state.json · outputs/ (00…07, REPORT, SIX_PAGER) · outputs/attachments/*.xlsx
site/index.html (RU/EN) · docs/ (HELP×2, ARCHITECTURE, SKILLS, SUBMISSION, VERIFICATION…)
tests/ (55) · demos: demo-antispam (готов), kids-guard (сквозной прогон)
```

## Прозрачность и стоимость

Журнал `log.jsonl` — что сделано; реестры — на чём основаны выводы; `pfs cost` — токены и деньги
(демо-проект: $18,79 ≈ 1 785 ₽; проверяемость чисел 87% против 0% у обычного чата; независимая рубрика
19/22). Подробно — `docs/demo/comparison.md`.

## Roadmap и ограничения

Дальше: паритет OpenCode (хуки → события), публикация на PyPI, живые прогоны Feynman, авто-дека PPTX.
Ограничения: качество зависит от модели среды; сайты на JS сохраняются через `--text-file`; авто-стоимость
— только по транскриптам Claude Code; Excel без диаграмм (stdlib); новые субагенты — после перезапуска.
