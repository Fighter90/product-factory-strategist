# Матрица соответствия заданию «Стратег Фабрики продуктов»

> Дата проверки: 06.11.2026. **Правило:** каждая строка — проверяемое доказательство (файл или команда),
> а не декларация. Счётчики репозитория сверены командами из раздела «Как проверить».

## Точные счётчики репозитория (сверено 06.11.2026)

| Счётчик | Значение | Проверка |
|---|---|---|
| Тесты | 521 (`OK`) | `python3 -m unittest discover -s tests` |
| Карты знаний | 89 RU (`knowledge/methods/`) + 89 EN-зеркал — полная двуязычная база (`knowledge/methods_en/`) + `knowledge/INDEX_EN.md` | `ls knowledge/methods \| wc -l` → 89; `ls knowledge/methods_en \| wc -l` → 89 |
| Навыки | 100 | `ls .claude/skills \| wc -l` → 100 |
| Субагенты | 8 | `ls .claude/agents \| wc -l` → 8 |
| Хуки | 6 (`session_start`, `pre_web`, `pre_guard`, `post_tool`, `stop`, `_common`) | `ls .claude/hooks \| wc -l` → 6 |
| MCP-инструменты | 18 | `tools/pfs/mcp_server.py` |
| Внешние зависимости | 0 (Python stdlib) | `pyproject.toml`, `pip` не нужен |

---

## 1. Обязательный минимум задания

| Требование | Статус | Доказательство (файл/команда) |
|---|---|---|
| Поставить задачу, ≤3 вопроса | ✓ | `.claude/skills/intake/`, `pfs ask`/`pfs answer`; демо: `projects/демо/outputs/00_brief.md` |
| Собрать материалы, источник у каждого сведения | ✓ | `tools/pfs/sources.py` + `tools/pfs/extract.py`: URL/PDF/DOCX/XLSX/CSV/медиа, дедуп по URL/SHA-256, SSRF-защита; демо: 10 источников S001–S011 (`pfs source list`) |
| Провести исследование (план от вопросов, меняющих решение) | ✓ | `projects/демо/outputs/01_research_plan.md`; реестр `projects/демо/claims.jsonl` — 20 утверждений C001–C020 с типами (fact/hypothesis/forecast/assumption/inference) и силой A–D (`tools/pfs/claims.py`) |
| ≥3 содержательно разных варианта, вкл. «оставить как есть» и «закрыть» | ✓ | `projects/демо/outputs/03_options.md` — варианты A–E; `config/quality_gate.json` → `min_options: 3`, `status_quo_keywords`, `exit_keywords` |
| Возражения по каждому варианту | ✓ | субагент `.claude/agents/red-team.md`; демо: 20 ударов (15 возражений + 5 скрытых допущений), встроены порогами в `06_validation_plan.md` |
| Факты ≠ гипотезы (и ≠ синтетика) | ✓ | `tools/pfs/claims.py` — факт без источника не записывается, синтетика фактами не считается; тест: `python3 -m unittest tests.test_pfs` |
| Продуктовая стратегия | ✓ | `projects/демо/outputs/04_product_strategy.md`; обязательные разделы в `config/quality_gate.json` |
| Коммуникационная стратегия | ✓ | `projects/демо/outputs/05_comms_strategy.md`; таблица «обещание → подтверждение» (`promise_table_section` в quality_gate.json) |
| План проверки | ✓ | `projects/демо/outputs/06_validation_plan.md` — 5 обязательных разделов, проверяются `pfs check` |
| Workflow с паузами человека | ✓ | 12 шагов в `tools/pfs/core.py` + `AGENTS.md` (таблица шагов с воротами); паузы на шагах 0/6/10 |
| Порядок в знаниях (инструкции ≠ знания ≠ материалы ≠ состояние) | ✓ | `AGENTS.md`, `knowledge/`, `projects/<slug>/`, `state.json` — раздельно; `docs/ARCHITECTURE.md` §3 |
| Продолжение после перерыва | ✓ | `.claude/hooks/session_start.py` подаёт `pfs status` при новом чате; состояние в `projects/демо/state.json` |
| Прозрачность | ✓ | `projects/демо/log.jsonl` (что сделано), `claims.jsonl` (на чём основано), `decisions.jsonl`, `pfs impact C###`, `pfs cost` |

## 2. Дополнительный уровень

| Возможность | Реализация | Доказательство |
|---|---|---|
| Интервью и модельные респонденты | `tools/pfs/participate.py` (`guide`, `save`), skill `interviews`, субагент `synthetic-respondent`; `--origin synthetic` → только hypothesis | демо: 2 ИИ-персоны — `projects/демо/interviews/synthetic/` (Sarah, Markus) → S009–S010 |
| Медиа-источники (изображения/аудио/видео) | `pfs media add` — описание «только видимое/слышимое» становится источником | `tools/pfs/participate.py` (`media`); тест: `python3 -m unittest tests.test_participate` |
| UX-анализ | skill `ux-review`, `pfs ux scaffold` — каркас 10 эвристик | демо: скриншоты RU/EN — `projects/демо/outputs/img/` |
| Анализ данных | `pfs data profile/cohort/funnel/stats`, `--save` для воспроизводимости | демо: `projects/демо/analysis/gen_synthetic.py` → `synthetic_funnel.csv` (источник S008) |
| Поддержка решений | `pfs decision add/due/done/status/rebase`: основания C###, ответственный, метрика «X→Y @дата», обязательства | демо: D001 — `projects/демо/decisions.jsonl` (1 запись), `pfs decision due` |
| Пересмотр при новых данных | `pfs claim supersede/retract/rebase` + `pfs impact` (источник → утверждение → вывод → строка → решение); `check` ловит ссылки на отозванное | `python3 -m tools.pfs --project демо impact C016` |
| Маршрутизация сценариев и моделей | `pfs route` (сценарий → карты → план моделей), `config/models.json` (fast/balanced/deep, эскалация, `--economy`) | `python3 -m tools.pfs route "запрос"` |
| Навыки / хуки / субагенты | `.claude/skills/` (100), `.claude/hooks/` (4 события + `_common.py`), `.claude/agents/` (8) | `ls`-команды из шапки файла |
| MCP + CLI | CLI `python3 -m tools.pfs` (25+ подкоманд); MCP `tools/pfs/mcp_server.py` — 18 инструментов (stdio JSON-RPC) | `python3 -m tools.pfs --help`; `.mcp.json` → pfs-strategist |
| База знаний с поиском | 89 карт RU + 89 EN-зеркал — полная двуязычная база + `INDEX_EN.md`; BM25 с русским стеммингом (`pfs kb search`), связи `related` проверяет `pfs kb index` | `python3 -m tools.pfs doctor` — число карт |
| Excel-приложения на формулах | `pfs calc all` → 4 книги (лист «Ввод» + формулы, пересчёт при открытии) | `projects/демо/outputs/attachments/` — 4 файла xlsx |
| Six-pager для комитета | `pfs export --six-pager` (FAQ-1…6) | демо: SIX_PAGER_RU и SIX_PAGER_EN, каждый в трёх форматах (MD/PDF/DOCX) |
| Отчёты и конвертация | `pfs export` (REPORT.md), `pfs export --deck`, `pfs docx` (Markdown → Word, без зависимостей) | `projects/демо/outputs/REPORT.md`, `docs/docx/` |
| Устойчивость к сбоям | атомарная запись (`tools/pfs/core.py`), идемпотентные команды, `--text-file` для JS-сайтов | `python3 -m unittest discover -s tests` → OK |
| Переносимость | состояние — файлы (JSON/JSONL/MD); AGENTS.md + CLAUDE.md + `.cursor/rules/` + `.mcp.json` | `git ls-files .cursor .claude .mcp.json` |

## 3. Демо: CVStart

Проект `projects/демо` — полный 12-шаговый прогон: **коммерческая версия + глобальный GTM для
[cvstart.org](https://cvstart.org/) ([github.com/Fighter90/career-ops-ui](https://github.com/Fighter90/career-ops-ui))** —
открытый (MIT) AI-конструктор резюме и поиска вакансий: скан ~129 джоб-бордов, AI-скоринг 0.0–5.0, CV Studio,
PDF/DOCX, cover letters, трекер, карта вакансий; 100% локально; 18 LLM-провайдеров BYOK; 19 языков;
~7 602 автотеста; монетизации нет.

- **Задание:** «Разработать коммерческую версию cvstart.org и стратегию вывода на рынок на весь мир»;
  ось — платящие подписчики и ARR; ограничения: MIT core, соло-разработчик, сохранить доверие локального режима.
- **Рынок** [S004–S007]: resume builders $1,2–2,4 млрд (диапазон — агрегаторы расходятся ×2); AI-сегмент
  CAGR 13,1%; онлайн-рекрутинг $37,97 млрд (2025); ATS у 98% F500; 7 конкурентов $8–40/мес с автопродлениями
  (Zety, resume.io, Novoresume, Kickresume, Enhancv, Teal, Rezi), языки EN+5.
- **Варианты A–E** (`03_options.md`), выбран **B — hosted freemium SaaS**: Free BYOK / Pro $12 / Unlimited $29;
  opt-in облако при локальном MIT-core; честный прайсинг без автопродлений; волны локалей
  EN → DE/ES/PT-BR → JA/ZH. Red team: 15 возражений + 5 скрытых допущений (20 ударов), интегрированы.
- **Экономика** [C016]: ARPU $29, CM $21,75, LTV ≈ $271,88, LTV/CAC ≈ 4,5, брейк-евен ≈ 69 платящих;
  синтетическая воронка [S008]: к нед. 12 — 53 платящих, MRR $1 537 (метод, не прогноз).
- **Проверка** (`06_validation_plan.md`): 90 дней, продолжить ≥ 40 платящих / изменить 20–40 / остановить < 20
  при activation < 35%; контр-метрики: звёзды GitHub, GDPR-жалобы, NPS ≥ 30, инференс free ≤ $200/мес.
- **Решение D001** (`decisions.jsonl`): бета в 3 EN-гео к 2026-12-15; пересмотр 2027-02-10; основания
  C019/C013/C014/C016/C005/C006.
- **Счётчики прогона:** 12 шагов · 10 источников S001–S011 · 20 утверждений C001–C020 (12 фактов, 4 гипотезы,
  4 допущения) · 5 вариантов · 20 ударов red team · 4 книги Excel · `check --strict` 100/100 · решение D001.
- **Синтетика помечена** `origin=synthetic` (S008–S010) — гипотезы и метод, не факты; инструмент не даёт
  записать на неё факт.
- **Артефакты:** `outputs/00…07_*.md`, `REPORT.md`, `SIX_PAGER_RU.md/.pdf/.docx` + `SIX_PAGER_EN.md/.pdf/.docx`
  (детальный текст комитета: выводы, обоснования, расчёты — без скриншотов), `outputs/attachments/` (4 xlsx), `outputs/img/` (скриншоты RU/EN),
  `interviews/synthetic/` (2 ИИ-интервью), `analysis/` (gen_synthetic.py, synthetic_funnel.csv, md_to_pdf.py).

## 4. Как проверить

```bash
# 1. Тесты инструментов (521, без установки пакетов)
python3 -m unittest discover -s tests

# 2. Quality gate демо-проекта (100/100)
python3 -m tools.pfs --project демо check --strict

# 3. Состояние демо (12-й шаг — monitoring) и счётчики
python3 -m tools.pfs --project демо status

# 4. Счётчики репозитория
ls .claude/skills | wc -l          # 100
ls .claude/agents | wc -l          # 8
ls .claude/hooks | wc -l           # 6
ls knowledge/methods | wc -l       # 89
ls knowledge/methods_en | wc -l    # 89

# 5. Сайт документации (RU/EN) — открыть локально
open site/index.html
```
