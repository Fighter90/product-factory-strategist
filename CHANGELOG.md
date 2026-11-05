# Changelog

Формат — Keep a Changelog; версионирование — SemVer.

## 1.0.1 — 2026-11-05 (вечер)

### Added
- Workflow v2: шаг discovery (персоны/JTBD), библиотека вопросных блоков (`pfs questions`, `config/question_blocks.json`),
  обязательные карты шага (`pfs step` печатает `kb.cards_for`).
- 27 скилов product-skills + новые sdd/deck/deep-research — всего 41; docs/SKILLS.md.
- База знаний 72 карты: Double Diamond, Lean Canvas, обзор фреймворков (RICE/ICE/WSJF, HADI, AARRR/HEART/Кано),
  Feynman deep-research skill.
- Домен strategyproduct.ru (cname + site/CNAME), GitHub Release v1.0.0 с whl/sdist assets.
- README RU/EN v2 (mermaid-архитектура, модель данных, research framework), лендинг site/ RU/EN (параллакс,
  i18n-переключатель), Lovable-проект документации.
- kids-guard: второй сквозной прогон (5 вариантов A–E, red team, D001, six-pager, аудит 20/22).

## 1.0.0 — 2026-11-05

### Added
- **База знаний из 7 учебных курсов** — 69 методических карт (`knowledge/methods/`): стратегии роста, юнит-экономика
  и traction-модели, продуктовый менеджмент, UX и клиентские метрики, анализ данных (A/B, SQL, дашборды,
  прогнозирование, ML), платформенные решения, Gen AI в продуктах; только методики и алгоритмы, без брендов.
- **Six-pager отчёт** `pfs export --six-pager` — FAQ-1…FAQ-6 (состояние, персоны, инициативы, тактики, план,
  метрики) + таблица Excel-приложений; собирается из документов 02/03/04/06.
- **Excel-приложения на формулах** `pfs calc [all|unit-econ|growth|cohort|market]` — юнит-экономика
  (CM/LTV/CAC/пейбек + чувствительность), модель роста 12 мес, когортное удержание, PAM→TAM→SAM→SOM + PESTEL;
  лист «Ввод» + формулы, параметры в `calcs.json`, расчёты идут фоном (субагент data-analyst).
- **XLSX-писатель на stdlib** (`tools/pfs/xlsx.py`) — формулы, процентный формат, стили, кэш значений; ноль зависимостей.
- **Markdown → DOCX конвертер** `pfs docx` и docx-версии документации: HELP и README на русском и английском (`docs/docx/`).
- **Сайт документации** `site/index.html` (RU/EN, переключатель языка, раздел «Справка») + GitHub Pages workflow.
- **Linear-интеграция**: MCP-сервер `mcp-server-linear` из `.env` (ключ не коммитится); рабочая программа — задачи PRO-5…PRO-16.
- **GitLab CI** `.gitlab-ci.yml` (unittest + doctor) и GitHub Pages workflow.
- **Пакет**: `pyproject.toml`, entry point `pfs`, Python ≥ 3.9, ноль runtime-зависимостей.
- Тесты six-pager, Excel-писателя и docx-конвертера (21 тест).

### Base (до 1.0)
- 10-шаговый процесс с человеком в контуре (intake/choice/decision); реестр утверждений C###/S### с силой A–D;
  автопроверка `pfs check --strict`; влияние изменений `impact`; замещение/отзыв `supersede/retract/rebase`;
  решения и мониторинг `decision due`; маршрутизация моделей `config/models.json`; 12 навыков, 8 субагентов, 4 хука;
  MCP-сервер pfs (10 инструментов); демо-проект `demo-antispam` (19 источников, 42 активных утверждения, $18,79).
