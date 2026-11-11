# Справка: как работать с агентом «Стратег Фабрики продуктов»

**[RU](HELP.md) · [EN](HELP_EN.md)**

> Подробное руководство пользователя. Быстрый старт — 5 минут, дальше — все команды, сценарии и разбор частых проблем.

---

## 1. Что это и как устроено

Агент — не программа и не бот, а **папка-репозиторий**, которую вы открываете в LLM-среде
(Claude Code, Cursor, Codex, OpenCode, Windsurf, Copilot). Среда читает `AGENTS.md` (правила и процесс),
`knowledge/` (наборы знаний по категориям: стратегия · экономика · продукт · UX · данные · платформы · Gen AI; только методики — без брендов), а всю «бухгалтерию» исследования
(источники, утверждения, проверки, решения, стоимость) ведёт инструмент `pfs`.

Четыре слоя, которые важно различать:

| Слой | Где | Что там |
|---|---|---|
| Правила и процесс | `AGENTS.md` | 12-шаговый процесс, правила доказательности, шпаргалка команд |
| Методики | `knowledge/methods/` | 89 карт методов (RU) + 89 EN-зеркал — полная двуязычная база и EN-индекс: юнит-экономика, A/B-тесты, платформы, GenAI и др. |
| Материалы задачи | `projects/<slug>/` | источники, реестр утверждений, документы, Excel-расчёты, состояние |
| Инструменты | `python3 -m tools.pfs …` | CLI и MCP-сервер с гарантиями: без источника факт не записать |

Агент сам ведёт процесс и вызывает `pfs`; вам нужно только отвечать на вопросы и принимать решения
в трёх точках: **бриф** (шаг 0), **выбор варианта** (шаг 6), **утверждение решения** (шаг 10).

---

## 2. Требования и установка

Нужно: Python 3.9+ (без пакетов), git, любая среда из списка выше. Опционально `pdftotext` (poppler)
или `pip install pypdf` — для PDF-источников.

```bash
git clone https://github.com/Fighter90/product-factory-strategist.git
cd product-factory-strategist
python3 -m tools.pfs doctor     # проверка окружения
python3 -m unittest discover -s tests   # самопроверка (392 теста)
```

`doctor` показывает: способ установки (editable/venv/source), версию пакета, путь до `pfs` (which), здоровье PATH, расположение projects dir, версию Python, наличие pdftotext/pypdf, число карт в базе знаний, активный проект.
Никаких ключей для работы CLI не нужно. Ключи (например, Linear API) кладите в `.env` — он не коммитится.

---

## 3. Быстрый старт: первая задача

1. Откройте папку репозитория в вашей среде (в Claude Code — команда `claude` в папке).
2. Напишите задачу обычным языком, как руководителю продукта:

   > Платная защита от спама теряет подписчиков. Что делать с продуктом и что говорить абонентам?

3. Агент сам: создаст проект, задаст 1–3 уточняющих вопроса, построит план исследования, соберёт источники,
   предложит варианты и защитит их ред-тимом, сведёт стратегии и покажет прогресс строкой:

   `Шаг 2/12 · research · собраны источники S001–S009 · дальше: discovery`

4. Вы в любой момент можете: **«стоп»** — остановить; **«уточни: …»** — скорректировать задачу;
   **«переделай раздел X»** — переработать только затронутое; **«собери six-pager»** — получить отчёт для комитета.
5. Перерыв/новый чат: откройте новый чат в той же папке — хук SessionStart сам подаст агенту состояние
   (`pfs status` делает то же вручную). Выполненные шаги не повторяются.

---

## 4. Процесс из 12 шагов

| # | Шаг | Что происходит | Ваша роль |
|---|---|---|---|
| 0 | intake | Уточнение вопроса, цели, ограничений, данных → `00_brief.md` | **подтверждаете бриф** |
| 1 | sources | Регистрация ваших файлов и открытых источников → `sources/S###.md` | даёте материалы |
| 2 | research | План от вопросов, меняющих решение; поиск; расчёты; интервью | отвечаете на вопросы |
| 3 | discovery | Персоны, JTBD, альтернативы пользователя → раздел «Сегменты» в 02 | отвечаете на вопросы блока discovery |
| 4 | situation | Что известно/неизвестно, противоречия → `02_situation.md` | — |
| 5 | options | ≥3 разных варианта + возражения (ред-тим) → `03_options.md` | — |
| 6 | choice | Сравнение и рекомендация | **выбираете вариант** |
| 7 | strategy | Продуктовая + коммуникационная стратегии → `04/05_*.md` | — |
| 8 | validation | План проверки: метрика, база, срок, контрметрики → `06_validation_plan.md` | — |
| 9 | review | Автопроверка `pfs check` + оценка по рубрике → `07_quality_review.md`; lock вердикта: `pfs review lock` | — |
| 10 | decision | Основания, ответственные, метрики, обязательства → `decisions.jsonl` | **утверждаете решение** |
| 11 | monitoring | Сроки, новые данные, пересмотр затронутых выводов | получаете напоминания |

После шага 9 (review) можно собрать **six-pager с Excel-приложениями** (раздел 7) — отчёт в структуре референса стратегии роста (детальная спецификация формата — knowledge/templates/SIX_PAGER_PROMPT.md): FAQ-1…FAQ-6 для продуктового комитета.

---

## 5. Все команды `pfs`

Полный список: `python3 -m tools.pfs --help`. Почти всё агент делает сам — команды ниже нужны,
чтобы проверить состояние или сделать что-то вручную.

### Проекты
```bash
pfs new "Название" "Запрос дословно"     # создать проект
pfs list                                 # список проектов
pfs use <slug>                           # сделать проект активным
pfs status [--brief]                     # где остановились, что дальше, стоимость
```
Активный проект хранится в `projects/.active`: переключайтесь `pfs use <slug>` перед работой
с другим проектом — экспортировать переменные окружения не нужно (окружение переопределяется
только в тестах через `PFS_PROJECTS_DIR`). Пути файлов в `source add`, `docx` и `media add`
резолвятся сначала от каталога проекта (`projects/<slug>/…`), а если файла там нет — от текущего
каталога; resolved-путь печатается в выводе.

### Шаги и вопросы
```bash
pfs next                                 # «что решать сейчас»: текущий шаг, ожидание человека,
                                         # просроченные обязательства, источники в основаниях решений
                                         # без проверки дольше 180 дн. (с командой pfs source refresh S###),
                                         # пересмотры (наступившие и в ближайшие 14 дней), открытые вопросы;
                                         # после review без SIX_PAGER.md — первым пунктом сборка
                                         # комитета-пакета (calc scaffold → calc all → export --six-pager)
pfs step <шаг> in_progress|done --note "…" --next "…"
pfs ask "Вопрос?" --options "A,B,C"      # пауза: агент ждёт вашего ответа
pfs answer "Вариант B"                   # ответить
pfs question "Открытый вопрос" [--close]
pfs questions <шаг|блок>                 # вопросные блоки шага для настраиваемости стратегии
                                         # (config/question_blocks.json); `pfs ask` — задать руководителю
```

### Источники (S###)
```bash
pfs source add https://example.ru/report            # сайт: скачивается, чистится, дедуп по URL/SHA-256
pfs source add ~/Downloads/report.pdf               # PDF/DOCX/XLSX/CSV/изображение
pfs source add sources/raw/report.md                # относительный путь: сначала каталог проекта
                                                    # (projects/<slug>/…), затем cwd; резолв-путь — в выводе
pfs source add --text-file doc.md --url <url> --title "…"   # если сайт блокирует автоматическую загрузку
pfs source fetch <url> --title "…"                  # недоступный URL (403/SSL/JS/таймаут) одним вызовом:
                                                    # прямой запрос → r.jina.ai → web.archive.org;
                                                    # origin: public при прямом успехе, excerpt при фолбэке
pfs source add interview.md --origin interview      # ваше интервью (без персональных данных)
pfs source add transcript.md --origin synthetic     # ИИ-респондент: только гипотезы
pfs source list | pfs source show S003
pfs source refresh S003                  # обновить web-источник: дельта sha256 → бэкап старой версии
                                         # в raw/<S###>_old_<sha8>.txt → impact по утверждениям на нём
```
Правила: домены проекта (`project.json → allowed_sources`) проверяются до запроса; файлы-секреты
(`.ssh`, ключи, `.env`) отклоняются; фразы-инструкции в текстах помечаются и не исполняются.

### Утверждения (C###) — сердце агента
```bash
pfs claim add "Рынок 40 млрд ₽ [данные]" --kind fact --source S002 --grade B
pfs claim add "Люди готовы платить за защиту близких" --kind hypothesis --source S005
pfs claim add "Поэтому фокус на семье" --kind inference --from C003,C010
pfs claim add-batch claims.jsonl        # пачка из JSONL (text/kind/source/grade/quote/from):
                                        # одна строка = одно утверждение; невалидная строка
                                        # отменяет весь батч; дубликаты по тексту пропускаются
pfs claim list [--kind fact] [--all]
pfs claim retract --id C005 --reason "ошибка в методике"
pfs claim supersede "Рынок 45 млрд" --id C005 --reason "новый отчёт" [--source S009]
pfs claim rebase [--id C012]            # перенаправить выводы на замены оснований
```
Типы: `fact` (есть источник; синтетика фактами не считается), `hypothesis`, `forecast`,
`assumption`, `inference` (только из других C###). Сила доказательства — `--grade A…D`.

### Проверки и влияние
```bash
pfs check [--strict] [--json]   # quality gate: числа без тегов, мёртвые ссылки, структура документов
                                # числовой кросс-чек (PRO-26): числа активных утверждений против чисел
                                # заголовков их источников и числа цитат против текста sources/S###.md —
                                # расхождение («в утверждении 19, в заголовке 17») даёт warning с парой C###/S###
pfs review lock                 # lock вердикта review: снимок реестра (sha256 claims/sources/документов 00–07)
                                # в outputs/.review_state.json; правки реестра после lock дают в check/status/export
                                # предупреждение «⚠ вердикт review устарел — реестр изменился после ревизии;
                                # повторите evidence-auditor»; после повторной ревизии зафиксируйте снова
pfs gap list                    # пробелы из 02 «Чего мы не знаем»: номера и статус (открыт/частично/закрыт)
pfs gap close 3 --claim C069 --note "чем закрыт"
                                # пометить пробел закрытым СИНХРОННО: строка в 02 + пункт/статус вопроса в 01;
                                # pfs check предупреждает, если 02 говорит «закрыто», а строка 01 ещё «открыт»
pfs impact C005                 # что затронет изменение: выводы → строки документов → решения
```

### Решения (D###) и мониторинг
```bash
pfs decision add --title "…" --decision "…" --owner "CPO" --grounds C001,C007 \
  --metric "Удержание M1: 38% -> 45% @2027-01-01" --review 2027-01-01 \
  --trigger "M1 < 40% два месяца подряд" --commit "Запустить пилот|PM|2026-12-01"
pfs decision due          # что решать сейчас: просроченные обязательства, устаревшие основания,
                          # источники без проверки дольше 180 дн. — с командой pfs source refresh S###
pfs decision done --id D001 --commitment K1
pfs decision list | status | rebase
```

### Данные
```bash
pfs data profile events.csv [--sheet Лист1] --save profile    # профиль таблицы: типы, пропуски, дубли, периоды
pfs data cohort events.csv --user user_id --date dt --save cohorts   # когортное удержание
pfs data funnel events.csv --steps visit,signup,pay --user user_id   # воронка по журналу событий
                                                              # или по флагам-колонкам; --date проверяет порядок
pfs data stats events.csv --col revenue [--group segment]     # базовая статистика столбца
                                                              # (n, среднее, медиана, перцентили, ДИ 95%) по группам
```

### Интервью, медиа и UX
```bash
pfs interview guide --persona "Родитель 7–12" [--topic "…"]   # каркас вопросов интервью в interviews/
pfs interview save transcript.md --persona "…" --title "…"    # транскрипт/выжимка ИИ-респондента
                                                              # → источник с origin synthetic (только гипотезы)
pfs media add скрин.png --desc "что видно на скриншоте"       # медиа в заявленных границах: файл копируется
                                                              # в sources/raw, описание «только видимое/слышимое»
                                                              # становится источником; интерпретации — отдельные C###
                                                              # (путь: каталог проекта → cwd)
pfs ux scaffold S003 --focus "онбординг"                      # UX-каркас из 10 эвристик в analysis/ux_<S###>.md
                                                              # с правилом «выводы только по материалу источника»
```

### Excel-расчёты (приложения к six-pager)
```bash
pfs calc scaffold                      # каркас calcs.json из 02/04/06/07: числа с C/S-тегами
                                       # в _notes; ненайденные — null + подсказка в _hints
pfs calc all                          # 4 книги → projects/<slug>/outputs/attachments/
pfs calc unit-econ | growth | cohort | market
```
Каждая книга: лист **«Ввод»** (редактируемые параметры) + расчётные листы **на формулах** — Excel
пересчитывает при открытии. Параметры агент берёт из `projects/<slug>/calcs.json`; каркас
генерирует `pfs calc scaffold` (ручная дописка — только null-поля):

```json
{
  "unit_econ": {"arpu": 199, "vc_share": 0.2, "cac": 600, "churn_month": 0.08,
                "note": "значения из C010, C014; заменить модельные — см. открытые вопросы"},
  "growth": {"mau_start": 100000, "mau_growth_month": 0.05, "conv_order": 0.02,
             "orders_per_active": 1.5, "aov": 3500, "take_rate": 0.08, "margin": 0.6},
  "cohort": {"sizes": [5000, 6000], "retention": [1.0, 0.55, 0.42]},
  "market": {"pam": 120000000000, "tam_share": 0.6, "sam_share": 0.3, "som_share": 0.05}
}
```
Чего нет в `calcs.json` — подставится пример из `tools/pfs/calc.py: DEFAULTS` с пометкой «ПРИМЕР»
(null-поля из каркаса — тоже). Коридоры чисел («60–70%») scaffold берёт по середине; null внутри
списков (sizes/retention) при сборке книги заполняется примером на своей позиции, а null в хвосте
за пределами примера обрезает список на этом месте — позиции никогда не сдвигаются, размер когорты 8
не становится размером когорты 7. Каждое значение прослеживайте до C###/S###: источник — в реестре,
ссылка — в `note`; найденные каркасом числа несут свой тег в `_notes` секции, повторный запуск
сохраняет `_notes`/`_hints` уже заданных значений.

### Отчёты
```bash
pfs finish                      # финальный пакет одной цепочкой: автопроверка pfs check → calc all → REPORT →
                                # SIX_PAGER → снимок реестра → DOCX → deck → сводка «что собрано + что устарело»;
                                # сборку останавливает любая ошибка check (как pfs check --strict); повторный вызов идемпотентен
pfs finish --no-deck            # то же без HTML-деки
pfs finish --en                 # + EN-черновик six-pager: SIX_PAGER_EN.md + DOCX (скелет на английском,
                                # секции из документов — с пометкой «[RU source — translate]»; check сверяет
                                # теги RU↔EN и предупреждает, если EN отстал от RU)
pfs export                     # REPORT.md: все документы + приложения A–E
                               # снимок реестра в outputs/.export_state.json; если claims/sources/Excel изменились после сборки — ⚠ при `pfs status` и при следующем экспорте
pfs export --six-pager         # SIX_PAGER.md в формате референса (подпункты, матрица тактик, KPI, сноски) + пересборка Excel
pfs export --six-pager --en    # + EN-каркас: SIX_PAGER_EN.md — те же структура/числа/теги, скелет на английском,
                               # секции из документов с пометкой «[RU source — translate]» (перевод — работа агента)
pfs export --six-pager --no-calcs   # пересобрать текст без перегенерации книг
pfs export --deck                   # HTML-дека 16:9 из SIX_PAGER.md
pfs docx <файл.md> [--out]     # Markdown → Word без зависимостей (путь: каталог проекта → cwd)
                               # (docx-версии HELP/README лежат в docs/docx/)
```
Структура six-pager: FAQ-1 состояние рынка и конкуренты · FAQ-2 сегменты и персоны ·
FAQ-3 инициативы и возражения · FAQ-4 тактики · FAQ-5 план и проверка · FAQ-6 метрики успеха ·
таблица Excel-приложений. Полная версия с реестром — REPORT.md.

### База знаний
```bash
pfs kb search "когортный анализ удержания"    # BM25-поиск по картам
pfs kb show M-unit-economics                  # показать карту
pfs kb index                                  # пересобрать INDEX.md, проверить связи
```

### Модели и стоимость
```bash
pfs models                     # таблица: какая модель на какую задачу (config/models.json)
pfs models pick red_team       # план на задачу
pfs models use cursor-mixed    # профиль для другой среды
pfs models sync                # прописать модели в субагентов Claude Code
pfs cost [--transcript session.jsonl] [--session ses_e43_session.json] [--window]   # стоимость по транскриптам Claude Code или сессии OpenCode (session.json; для план-провайдеров типа zai-coding-plan — токены с $0 и пометкой «plan»); --session <файл> без --transcript — алиас с авто-детектом формата в корне проекта (*_session.json / *.jsonl; без значения — самый свежий, реестровые claims/sources/decisions/log.jsonl не считаются); в других средах:
pfs log "Ручная правка" --usd 0.8 --human-minutes 15
```

### Диагностика
```bash
pfs doctor      # окружение + целостность реестров источников: дубли ID/URL, запись без файла, файл-сирота (PRO-34)
```

---

## 6. Фоновая работа (субагенты)

Агент разгружает основной диалог субагентами: `researcher` (чтение длинных источников),
`red-team` (атака вариантов), `evidence-auditor` (оценка по рубрике), `data-analyst` (расчёты,
включая `pfs calc`), `synthetic-respondent` (ИИ-респонденты — только гипотезы), `comms-strategist`,
`ux-analyst`, `router`. Excel-расчёты six-pager собираются **фоном**: пока считается `pfs calc`,
вы можете продолжать диалог. Модель под задачу выбирается по `config/models.json` (дешёвые — на
классификацию и выписки, сильные — на синтез и стратегию), эскалация — `pfs models escalate`.

Глубокий ресёрч — Feynman (feynman.is, skill deep-research): feynman deepresearch/lit/compare с
provenance-файлом. Правила переноса: provenance → первоисточники регистрируются как S###; цифры —
факты только из первоисточников; сам отчёт — origin agent, только гипотезы. Телеметрия:
FEYNMAN_TELEMETRY=off; ключи OPENALEX/SEMANTIC_SCHOLAR_API_KEY — в .env.

---

## Навыки: структура и вызов

У агента 121 навык (skills): базовые 13 по шагам процесса · 27 product-skills · 75 из личной библиотеки · 6 интеграций.
Навыки не заменяют процесс и `pfs` — это библиотека техник, которые подключаются там, где нужны.

**Группы:**

- **Базовые (13)** — по шагам процесса: intake, research, situation, options, strategy, validation-plan, decision-support и др.
- **Product-skills (27)** — продуктовые методики (маркет-сайзинг, юнит-экономика, трекшн-модели, роадмапы…).
- **Личная библиотека (75):**
  - *дизайн*: `design-ui`, `refero-design`, `frontend-design`, `claudable-landing`, `make-interfaces-feel-better`, `emil-design-eng`, `web-design-guidelines`
  - *маркетинг*: `ads`, `ad-creative`, `seo-audit`, `ai-seo`, `cro`, `pricing`, `offers`, `cold-email`, `emails`, `launch`, `content-strategy`, `competitors`, `analytics`, `programmatic-seo`, `directory-submissions`, `customer-research`, `marketing-psychology`, `prospecting` и др.
  - *наука*: `paper-lookup`, `research-lookup`, `literature-review`, `scientific-writing`, `scientific-critical-thinking`, `peer-review`, `statistical-analysis`, `statsmodels`, `scikit-learn`, `hypothesis-generation`, `pydeseq2`, `biopython`, `rdkit`
  - *документы/медиа*: `pdf`, `docx`, `pptx`, `xlsx`, `markitdown`, `officecli`, `generate-image`, `video`, `infographics`, `scientific-slides` / `scientific-schematics` / `scientific-visualization`, `latex-posters`, `matplotlib`, `seaborn`
  - *режимы мышления*: `consciousness-council`, `balanced`, `what-if-oracle`, `dhdna-profiler`
  - *мета*: `find-skills`, `shap`, `watch`, `transcribe`
- **Интеграции:** `hallmark` — anti-slop гейты для страниц; `board-of-directors` — совет из 5 перспектив + Red Team;
  `premortem` — предразбор провала; `rea` — reverse-engineering страниц и форматов; `sdd`; `deck`.

**Как вызывать:**

1. **Автоматически** — по триггерам из описания навыка (агент сам подключит нужный, когда задача совпадает).
2. **Явно** — «используй skill `<имя>`: `<задача>`». Примеры: «сделай premortem по D001»,
   «используй skill hallmark: собери лендинг».
3. **В процессе — по шагам:** `pfs step` печатает обязательные карты шага; options → для дорогих решений
   подключается `board-of-directors`; decision → `decision-support` + `premortem` — ПОСЛЕ черновика D###
   и ДО утверждения; research → для JS-страниц — `deep-research` / `rea`.

**Правило приоритета:** при конфликте методология из `knowledge/` приоритетнее процедуры навыка.
Полный реестр — [`SKILLS.md`](SKILLS.md).

---

## 7. Six-pager за 5 шагов (сценарий)

1. Дождитесь готовности документов 02/03/04/06 (шаги situation…validation).
2. Скажите агенту «собери six-pager» — он заполнит `calcs.json` числами из утверждений
   (каждое значение — с C###), запустит расчёты субагентом в фоне и соберёт отчёт.
3. Получите: `outputs/SIX_PAGER.md` + `outputs/attachments/*.xlsx` (4 книги).
4. Откройте Excel: лист «Ввод» — поменяйте допущения на фактические; формулы пересчитаются.
5. Числа в тексте и в Excel должны совпадать: после правки `calcs.json` повторите `pfs calc all` и `pfs export --six-pager`.

---

## 8. Хуки и автоматика

| Событие | Что делает само |
|---|---|
| Начало чата | подаёт агенту состояние проекта и «что решать сейчас» |
| WebFetch | блокирует домены вне `allowed_sources` проекта **до** запроса |
| После инструментов | пишет журнал, ищет фразы-инструкции в веб-ответах, гоняет автопроверку документа |
| Конец ответа | считает стоимость сессии (идемпотентно) |

Хуки не роняют сессию: ошибки пишутся в `.claude/hooks/hook_errors.log`.

### Сквозной QA-прогон (PRO-64)

Проверка «агент справляется с новыми задачами» — прогоном всей 12-шаговой цепочки на свежем клоне:

```bash
scripts/e2e_opencode.sh ru qa/tasks/antispam-ru.md    # 3 задачи × ru/en в qa/tasks/
# в OpenCode то же самое: команда /pfs-e2e ru | en | all
```

Скрипт делает всё сам: свежий клон во временный каталог → `opencode run --auto --format json`
в режиме автопрогона (вопросы `pfs ask` агент закрывает сам, работа до `pfs finish`, без «продолжи»)
→ разбор лога → отчёт `qa/E2E-<дата>-<задача>-<lang>.md`: шаги, вызовы инструментов, ошибки, токены и стоимость,
время, результат `pfs check --strict` и сборки six-pager, число остановок, языковая консистентность
реплик («Язык реплик» с ⚠️, если заметная часть реплик не на языке прогона). Прогон идёт 20–40 минут.
Сравнение с обычным чатом и ограничения выборки — `docs/demo/comparison.md`.

---

## 9. Пересмотр после новых данных

1. Добавьте источник: `pfs source add <url|файл>`.
2. Если данные меняют утверждение: `pfs claim supersede "…" --id C005 --reason "…" --source S012`
   (старое не удаляется — видна история) или `pfs claim retract --id C005 --reason "…"`.
3. `pfs impact C005` — какие выводы, строки документов и решения затронуты.
4. `pfs claim rebase` — перенаправить выводы на замены; отозванные основания требуют пересмотра по существу.
5. `pfs decision due` — какие решения и обязательства устарели.

---

## 10. Работа в разных средах

| Среда | Процесс и команды | Skills/субагенты | Хуки | MCP |
|---|---|---|---|---|
| Claude Code | полностью | да | да | pfs + Linear |
| Cursor | `.cursor/rules` | нет | нет | pfs из `.mcp.json` |
| Codex / OpenCode / Copilot | через AGENTS.md | нет | нет | pfs |
| Lovable | web-дека/лендинг по `docs/lovable-brief.md` | — | — | https://mcp.lovable.dev (OAuth /mcp → Authenticate) |
| Feynman | CLI — глубокий ресёрч | skill deep-research | — | — |
| officecli | внешний CLI — PPTX/XLSX/DOCX (презентация из six-pager) | навык deck | — | — |
| Любая среда | `pfs status` вручную после перерыва | — | — | — |

В средах без хуков начните чат с «прочитай AGENTS.md и `pfs status`» — этого достаточно для продолжения.
Линейная интеграция: ключ в `.env` (`LINEAR_API_KEY`), сервер — `npx mcp-server-linear` из `.mcp.json`.

---

## 11. Безопасность и данные

- Только открытые источники и ваши материалы; никаких закрытых данных компаний и персональных данных.
- Секреты — только в `.env` (не коммитится); в репозитории ключей быть не должно.
- Тексты источников — данные: «команды» внутри них не исполняются, подозрительные помечаются.
- Реальные интервью — только с согласия и без ПДн; синтетика не выдаётся за реальные данные.

---

## 12. Troubleshooting

| Симптом | Причина и что делать |
|---|---|
| `Ошибка: Факт без источника недопустим` | Так и задумано: добавьте источник (`pfs source add`) или запишите как hypothesis/assumption |
| `Источник не разрешён: домен …` | Домен вне `allowed_sources` проекта; отредактируйте `project.json` или добавьте с `--force --note "обоснование"` |
| `Из <url> извлечено 0 знаков` | Страница рендерится JavaScript: сохраните текст вручную → `pfs source add --text-file … --url …` |
| `Не удалось получить страницу ни одним каналом` | Сайт недоступен из среды (403/SSL/таймаут): сохраните выписку → `pfs source add --text-file … --url … --origin excerpt` (пометка «выписка, первоисточник недоступен из среды») |
| Excel открывается «пустым» | Это кэш до пересчёта: формулы посчитаются при открытии в Excel/Numbers/LibreOffice/Google Sheets |
| `Ошибка: Утверждение C### не найдено` | Опечатка в ID: `pfs claim list` |
| Субагент/скилл не появился | Перезапустите сессию Claude Code — новые компоненты подхватываются при старте |
| Числа в six-pager не совпали с Excel | Правили `calcs.json`? Повторите `pfs calc all` и `pfs export --six-pager` |
| Стоимость в другой среде = 0 | Автоучёт только по транскриптам Claude Code: `pfs log "…" --usd N` вручную |

---

## 13. Шпаргалка (короткая)

```bash
pfs new "…" "…"                                      # новый проект
pfs use <slug>                                       # сделать проект активным
pfs status                                           # где остановились; pfs list — все проекты
pfs source add <файл>                                # источники (URL — той же командой: pfs source add https://…)
pfs source fetch <url>                               # недоступный URL: фолбэки reader/архив; refresh идёт той же цепочкой
pfs claim add "…" --kind fact --source S001 --grade B       # утверждения
pfs claim add-batch claims.jsonl                            # пачка утверждений из JSONL
pfs check --strict                                   # контроль качества
pfs calc all                                         # Excel
pfs export --six-pager                               # отчёт для комитета
pfs decision due                                     # что решать сейчас
pfs kb search "запрос"                               # методики
```

Подробности архитектуры — [`ARCHITECTURE.md`](ARCHITECTURE.md), правила процесса — [`../AGENTS.md`](../AGENTS.md).
