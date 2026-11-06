# Матрица соответствия заданию «Стратег Фабрики продуктов»

> **Обновление 06.11.2026:** демонстрационный проект — ROSE (`projects/демо`, закрытый клуб ужинов, rosedate.ru): полный прогон 12 шагов, 5 вариантов + red team, обе стратегии, six-pager (MD/PDF/DOCX) + 4 книги Excel, check --strict 100/100. Прежние демо (demo-antispam, kids-guard) удалены из репозитории — история в git.

> Дата: 5 ноября 2026 · Источники проверки: AGENTS.md, docs/HELP.md, docs/SKILLS.md, docs/demo/comparison.md,
> docs/VERIFICATION.md, docs/ARCHITECTURE.md, docs/SUBMISSION.md, README.md, `projects/демо/outputs` (ROSE),
> `tools/pfs/*.py`, `config/*.json` (+ живые прогоны `pfs doctor`, `pfs check`,
> `unittest` на рабочей копии).
> **Правило:** каждая строка — проверяемое доказательство (файл, команда или тест), а не декларация.
> Каждая строка таблицы проверена чтением файла или запуском команды 05.11.2026.

---

## 1. Обязательный минимум

| Требование | Где реализовано (файл/команда) | Доказательство (команда или тест) | Статус | Что доделать (для ⚠) |
|---|---|---|---|---|
| Поставить задачу | Шаг `intake`: skill `.claude/skills/intake`, ≤3 вопроса через `pfs ask`/`pfs answer`; `pfs new "Название" "Запрос"`; `config/question_blocks.json` (вопросные блоки) | `python3 -m tools.pfs new "t" "q"` создаёт проект; `projects/демо/outputs/00_brief.md` существует (ROSE); ответы руководителя — в state.json | ✓ | — |
| Собрать материалы | `tools/pfs/sources.py`, `tools/pfs/extract.py`: URL/PDF/DOCX/XLSX/CSV/HTML/медиа, дедуп по URL и SHA-256, SSRF-защита, `allowed_sources` (project.json), `--text-file` для JS-сайтов | `pfs source list` → в демо ROSE 12 источников, из них 2 синтетических (`pfs source list`); VERIFICATION: «форматы материалов ✅, повтор не создаёт дубль» | ✓ | — |
| Провести исследование | Шаг `research`: `01_research_plan.md`, реестр `claims.jsonl` с 5 типами (fact/hypothesis/forecast/assumption/inference) и силой A–D (`tools/pfs/claims.py`), субагент `researcher` | `pfs claim list --kind fact`; в демо ROSE 24 утверждения (18 активных), 5 типов, силы A–D | ✓ | — |
| ≥3 варианта + возражения + факты≠гипотезы | `03_options.md`; `config/quality_gate.json` → `min_options: 3`, `status_quo_keywords`, `exit_keywords`, `per_option_sections: ["Возражения"]`; субагент `.claude/agents/red-team.md`; синтетика ≠ факт — правило в `claims.py` | `pfs check --strict` (демо ROSE: 100/100, ошибок 0 и предупреждений 0); 5 вариантов, 20 возражений red team | ✓ | — |
| Продуктовая стратегия | `04_product_strategy.md`; обязательные разделы в `config/quality_gate.json`: Аудитория · Альтернативы · Выбранное направление · Осознанные отказы · Экономика | Файл есть в обоих демо-проектах; `pfs check` падает при пропуске раздела (проверка VERIFICATION) | ✓ | — |
| Коммуникационная стратегия | `05_comms_strategy.md`; разделы: Аудитория и ситуация · Барьер · Ключевое сообщение · Подтверждение · Роль каналов · таблица «Соответствие обещаний продукту» (`promise_table_section` в quality_gate.json) | Файл есть в демо ROSE; `pfs check` 100/100, таблица обещаний заполнена | ✓ | — |
| План проверки | `06_validation_plan.md`; 5 обязательных разделов (Ожидаемое изменение · С чем сравниваем · Срок наблюдения · Нежелательные последствия · Критерии решения) | Файл есть в обоих проектах; sections проверяются `pfs check` по quality_gate.json | ✓ | — |
| Workflow | 12 шагов: `tools/pfs/core.py` (intake…monitoring + discovery + route), state.json, `pfs step`, ворота в README (таблица шагов с картами и вопросными блоками) | `python3 -m tools.pfs step --help`; `grep discovery tools/pfs/core.py`; `pfs questions <шаг>` | ✓ | — (исправлено 05.11 вечер: AGENTS.md переведён на 12-шаговую таблицу с discovery, маркер «Шаг N/12») |
| Порядок в знаниях | `knowledge/methods/` (80 карт RU + methods_en/ EN-зеркала и INDEX_EN.md), `knowledge/templates/` (9), `knowledge/rubrics/strategy_quality.md`, `INDEX.md`; поиск BM25 `pfs kb search`; разделение слоёв (ARCHITECTURE §3) | `ls knowledge/methods \| wc -l` → 72; `pfs kb index` → 0 битых связей (VERIFICATION, вечер 05.11) | ✓ | — |
| Продолжение после перерыва | Хук `.claude/hooks/session_start.py` (SessionStart подаёт `status` + `decision due`), состояние в state.json/log.jsonl; «прочитай AGENTS.md и `pfs status`» для сред без хуков | Доказательство демо: `docs/demo/resume_after_break.txt`; VERIFICATION: «работа продолжается после перерыва ✅» | ✓ | — |
| Прозрачность | `log.jsonl` (что сделано), `claims.jsonl` (на чём основано), `decisions.jsonl`, `costs.json` + `pfs cost`, `pfs impact` (граф до строки документа) | `pfs log` демо ROSE: 96+ записей; `pfs cost` поддерживается Stop-хуком в Claude Code | ✓ | — |

---

## 2. Дополнительный уровень

| Возможность | Где реализовано | Доказательство | Статус | Что доделать (для ⚠) |
|---|---|---|---|---|
| Интервью и модельные респонденты | `tools/pfs/participate.py` (`guide`, `save_synthetic`); skill `interviews`, субагент `synthetic-respondent`; `--origin synthetic` → только hypothesis (claims.py) | `python3 -m unittest tests.test_participate` — зелёный; демо: 3 синт. интервью в реестре (SUBMISSION §5: C033–C035) | ✓ | — |
| Изображения/аудио/видео (в заявленных границах) | Медиа-команда: `pfs source add <файл.png/.mp4/.mp3>` → `kind="media"` (`extract.py`, MEDIA-расширения) + `participate.media()` (копия в sources/raw, assert_safe_local, детектор инструкций, sha256-дедуп). Правило описания: «описывай только видимое/слышимое» (AGENTS.md §4) и заголовок источника «⚠ Описание — то, что видно/слышимо; интерпретации — отдельными утверждениями» | `python3 -m unittest tests.test_participate` (описание обязательно, дедуп, отказ на чужой путь); граница задана: инструменты хранят описание, распознавание — мультимодальность среды (SUBMISSION, «Ограничения») | ✓ | — |
| UX-анализ | Skill `ux-review`, субагент `ux-analyst`, `participate.ux_scaffold()` — каркас из 10 эвристик, правило «выводы только по материалу источника» | `python3 -m unittest tests.test_participate` (ux_scaffold: создание, идемпотентность, отказ на S999) | ✓ | — |
| Анализ данных | `pfs data profile` (типы, пропуски, дубли, единицы, пропущенные периоды), `pfs data cohort` (когортное удержание), `--save` для воспроизводимости; скрипты в `analysis/` | `python3 -m tools.pfs data profile --help`; VERIFICATION: «когорты и сегменты на модельных данных ✅» | ✓ | — |
| Поддержка решений | `pfs decision add/due/done/status/rebase`: основания C###, ответственный, метрика «X→Y @дата», триггер, обязательства «что\|кто\|когда» | `pfs decision list` → D001 в обоих проектах (`wc -l projects/*/decisions.jsonl` = 1/1) | ✓ | — |
| Пересмотр при новых данных | `pfs claim supersede/retract/rebase` + `pfs impact` (источник → утверждение → вывод → строка документа → решение); `check` ловит ссылки на отозванное | `pfs impact C005`; демо: 14 из 56 утверждений замещены/отозваны (docs/demo/comparison.md); образец вывода `docs/demo/impact_S005.txt` | ✓ | — |
| Routing | `pfs route` — 6 сценариев, карты и план моделей, `--override`, `--economy`, `--json`; `config/models.json` — 3 профиля, 19 задач, эскалация (`pfs models escalate`) | `python3 -m tools.pfs route "запрос"`; VERIFICATION: «7 формулировок — верный сценарий ✅» | ✓ | — |
| Skills / hooks / subagents | `.claude/skills/` (45 на диске), `.claude/hooks/` (4 события + _common.py), `.claude/agents/` (8) | `ls .claude/skills \| wc -l` → 45; `ls .claude/agents \| wc -l` → 8 | ✓ | — |
| MCP + CLI | CLI `python3 -m tools.pfs` (25 подкоманд); MCP `tools/pfs/mcp_server.py` (10 инструментов, stdio JSON-RPC); `.mcp.json` → pfs-strategist + linear + lovable | `python3 -m tools.pfs --help`; VERIFICATION: «MCP-сервер (10 инструментов) ✅» | ✓ | — |
| База знаний | 80 карт (RU) + 8 EN-зеркал, BM25 с русским стеммингом (`pfs kb search`), INDEX.md, связи `related` проверяются `pfs kb index` | `pfs doctor` → «Карт в базе знаний: 80»; kb index: «80 карт, 0 битых связей ✅» (06.11) | ✓ | — |
| Устойчивость к сбоям | Атомарная запись (core.atomic_write), идемпотентность команд, хуки не роняют сессию, окно стоимости `cost_window` | VERIFICATION: «найдено и исправлено 4 дефекта… каждое исправление закреплено тестом»; ARCHITECTURE §6 | ✓ | — |
| Переносимость | Состояние — файлы (JSON/JSONL/MD); AGENTS.md + CLAUDE.md + `.cursor/rules/strategist.mdc` + `.mcp.json`; профили моделей `cursor-mixed`, `ru-local` | `git ls-files .cursor .claude .mcp.json`; ARCHITECTURE §7 | ✓ | — |
| Сравнение с исходным способом | `docs/demo/comparison.md`, скрипт `docs/demo/compare.py`, базовый ответ `docs/demo/baseline_plain_chat.md` | `python3 docs/demo/compare.py` → проверяемость чисел 87% vs 0%, возражения 7 vs 0, контрметрики да vs нет | ✓ | — |

---

## 3. Требования к работе

| Требование | Где реализовано | Доказательство | Статус | Что доделать (для ⚠) |
|---|---|---|---|---|
| Среды | Claude Code (полно), Cursor (`.cursor/rules` + MCP), Codex/OpenCode/Copilot/Windsurf (AGENTS.md), Lovable/Feynman/officecli как интеграции | Таблица сред в HELP §10; `ls .cursor/rules` → strategist.mdc | ✓ | — |
| Запуск по инструкции | `git clone` → `python3 -m tools.pfs doctor` → `python3 -m unittest discover -s tests`; Python 3.9+ без pip install | Живая проверка 06.11: `doctor` ok (80 карт); unittest → 55 тестов, все зелёные | ✓ | — (числа сверены 06.11: тесты 55, навыки 120, карты 80 + EN-индекс — HELP/README/SKILLS синхронизированы) |
| Экономичность | `config/models.json`: fast/balanced/deep/frontier по 19 задачам; `pfs route --economy`; длинные источники — extract на fast; `pfs kb search` вместо чтения всей базы; фоновые субагенты | `python3 -m tools.pfs models` → таблица; escalation_rules в models.json | ✓ | — |
| Удобство | `pfs status --brief`, `pfs next` («что решать сейчас»), `pfs ask/answer`, хуки-автоматика, HELP RU/EN + troubleshooting (HELP §12), docx-версии документации | `python3 -m tools.pfs next --help`; `ls docs/docx/` → 5 файлов docx | ✓ | — |
| Данные и безопасность | `allowed_sources` + блок домена до запроса (`.claude/hooks/pre_web.py`), SSRF-защита, отказ от `.ssh`/секретов/XML-бомб, детектор фраз-инструкций, `.env` вне git | `git check-ignore .env` → игнорируется; VERIFICATION: «Безопасность и ПДн ✅» (ключей, e-mail, телефонов, ФИО нет) | ✓ | — |

---

## 4. Что отправить

| Артефакт | Статус | Доказательство | Что доделать (для ⚠/❌) |
|---|---|---|---|
| Репозиторий | ✓ public | `git remote -v` → github.com/Fighter90/product-factory-strategist; README RU/EN, Release v1.0.0 | — |
| Демо-проекты | ✓✓ | демо ROSE: outputs 00–07 + REPORT.md + SIX_PAGER.md/.pdf/.docx + 4 xlsx + материалы (4 PDF) + синтетика, 12 S / 24 C / D001, check 100/100; red team: 15 возражений + 5 допущений | — |
| Видео | ❌ — на команде | Сценарий готов: docs/VIDEO_SCRIPT.md (≤10 мин, по шагам с командами) | Записать по сценарию |
| Описание работы | ✓ docx готов; PDF собирается из него | docs/SUBMISSION.md + docs/docx/SUBMISSION.docx; конвертация — `pandoc docs/SUBMISSION.md -o submission.pdf` или «Печать → PDF» | Собрать PDF и добавить скриншоты |
| Сайт strategyproduct.ru | ⚠ | VERIFICATION (вечер 05.11): GitHub Pages настроен (`site/CNAME`), DNS: апекс NXDOMAIN, `www` — заглушка регистратора | Прописать у регистратора A 185.199.108–111.153, AAAA 2606:50c0:8000–8003::153, CNAME www → fighter90.github.io |
| Рабочая копия перед отправкой | ✓ | deck-export (`export.build_deck`, `pfs export --deck`) завершён и закоммичен 05.11 вечер вместе с `data funnel/stats`, `source refresh`, `participate` и их тестами; unittest: 55 тестов — все зелёные | — |

---

## 5. Итог

**Сильные стороны.** Репозиторий проходит проверку «свежим clone» без установки пакетов: doctor, 55 зелёных
тестов, сквозной путь от размытого запроса до D001 в демо ROSE (projects/демо — REPORT, six-pager MD/PDF/DOCX, 4 книги Excel, check 100/100).. Ядро ценности —
детерминированные гарантии: факт без источника не записать, синтетика не станет фактом, отзыв основания
подсвечивает затронутые строки документов и решения; red team в демо нашёл круговое обоснование и привёл к
отзыву 14 утверждений. Продолжение после перерыва, прозрачность (журнал, стоимость $18,79, окно учёта),
безопасность (домены до запроса, SSRF, секреты вне git) подтверждены VERIFICATION; сравнение с обычным чатом —
87% против 0% проверяемых чисел.

**Известные ограничения** (из VERIFICATION/SUBMISSION, не дефекты): качество рассуждений зависит от модели
среды — детерминированы только инструменты `pfs`; часть сайтов блокирует автозагрузку (текст добавляется
вручную через `--text-file`); синтетические интервью дают гипотезы, а не доказательство спроса;
автоучёт стоимости — только по транскриптам Claude Code; мультимодальность средствами модели среды
(инструменты хранят описание); `numbers_need_tags` — эвристика с возможными ложными предупреждениями;
роутер сценариев — по ключевым словам; субагенты подхватываются после перезапуска сессии. К сдаче осталось:
видео (на команде), PDF описания и DNS сайта.
