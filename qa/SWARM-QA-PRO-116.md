# Swarm QA — PRO-116 (v1.2.37, Lane B)

Story: RU-цикл 12 шагов на живом проекте — `python3 -m tools.pfs` из worktree, глобальный `pfs` не тронут,
`PFS_PROJECTS_DIR` — своя tmp-папка. Плейбук: `pfs new «ATS: резюме джуниора»` + `route growth` +
`source add` + `claim fact/hyp/inference` + шаги 1–12 (ask/answer на choice) + `decision add`;
02–06 по шаблонам `knowledge/templates`; `check --strict` → 0 ошибок; цикл six-pager
(`export --six-pager` → текст по слотам `six_pager_pack.md` → `check --six-pager` → 0); `pfs finish` → 16 артефактов.

> build · glm-5.3-flash · Lane B executor

## Прогон

- Проект: `ats-junior-laneb` (lang=ru) в изолированной папке
  `$TMPDIR/opencode/pro116-projects/` через `PFS_PROJECTS_DIR` — репозиторий не менялся.
- Шаги: intake → sources → research → discovery → situation → options → choice
  (`pfs ask` + `pfs answer`: выбран вариант B «специализация первая работа для джуниора») →
  strategy → validation → review (`review lock`, повтор после правки 06) →
  decision (`decision add`, D001, утверждение через ask/answer) → `finish`.
  Monitoring не запускался (по правилам — только по явному запросу).
- Источники: 2 — S001 Wikipedia ATS (web, затем заменён выпиской через
  `pfs source update --text-file`) и S002 Jobscan «State of the Job Search 2025»
  (выписка `--text-file --url --published`). Утверждения: 9, из них 8 активных
  (5 fact / 2 hypothesis / 1 inference; C001-допущение отозван как дублирующий бриф).
- Документы 00–07 — RU-шаблоны `knowledge/templates/`; роадмап собран из
  outcome-раздела 04 в XLSX; вопросные блоки каждого шага пройдены
  (`pfs questions <шаг>`, фиксация `pfs log --kind questions-skip`).
- PDF-версии REPORT/SIX_PAGER/SIX_PAGER_EN собраны из DOCX (pandoc + tectonic)
  сверх пакета finish — как в референсном прогоне «16 артефактов».

## Счётчики (гейты задачи)

| Гейт | Результат |
|---|---|
| `pfs check` (документы 02–06) | **0 ошибок** (score 98/100, предупреждение 1 — weak-флаг S001, см. «Ограничения») |
| `pfs check --strict` | **0 ошибок**, rc=0 |
| `pfs check --six-pager` | **0 ошибок** (цикл writer: 1 раунд правок — «из 03» (служебная ссылка), расшифровки CAC/LTV/MAU) |
| `pfs finish` | затвор зелёный, «Собрано (11)», «Документы 00–07: все на месте», повторный вызов идемпотентен |
| Артефакты | **25 артефактов**: 16 ядерных (00–07 = 8, REPORT.md+docx = 2, SIX_PAGER RU md+docx = 2, SIX_PAGER EN md+docx = 2, pack json+md = 2) + 5 xlsx (4 attachments + roadmap) + deck.html + 3 PDF (docx→pdf). `find outputs -type f` даёт 27 — сверх артефактов это 2 внутренних файла состояния CLI (`.export_state.json`, `.review_state.json`), не артефакты |
| `pfs status` | шаги 1–11 ✔, текущий 12/12 monitoring, «Следующее действие: finish» (выполнен) |
| `pfs decision due` | «Нет просроченных обязательств, пересмотров и устаревших оснований» |
| Сьют репозитория | `python3 -m unittest discover -s tests` — Ran 918, **OK (skipped=1)**; `pfs doctor` — без новых проблем; `git status` чистый |

## Наблюдения (дефекты вне рамки задачи, не чинились)

1. **`pfs source update --text-file` не пересчитывает флаг `weak_content`.**
   S001 был зарегистрирован по web-URL с почти пустым текстом (2693 знака навигационной
   оболочки) и получил `weak_content=True` при регистрации. Замена текста выпиской через
   `source update` пересчитывает sha256/chars/injection_flags, но флаг остаётся —
   `check` продолжает предупреждать «мало содержательного текста» при полностью
   содержательном новом тексте (`tools/pfs/sources.py::update`, `check.py` читает флаг).
   Предупреждение не блокирует `--strict`/`finish`; для чистого гейта в QA-прогоне принято.
2. **Каркас six-pager содержит служебную ссылку «из 03»** в подставленном тексте решения
   (шаблон FAQ-5 генерирует «пересмотр … из 03» из триггера D001), а линтер ловит «из 0X»
   как ошибку — writer обязан переписывать строку. По замечанию ревьюера — это дефект
   шаблона/линтера продукта (шаблон генерирует строку, которую собственный гейт
   `check --six-pager` считает ошибкой), а не нюанс цикла; вне рамки PRO-116 —
   рекомендуется оформить отдельным issue (PRO-46-слоя), чтобы замечание не потерялось.
3. **EN-версия six-pager из finish — черновик-каркас** (PRO-46: текст EN пишет writer
   отдельно). Счётчик 16 артефактов это учитывает (EN md+docx считаются).

## Ограничения (честно)

- Внутренних метрик продукта в брифе нет: базовые линии конверсии/чека в 06 заданы
  как «замер первой недели пилота», а не числа — это корректная честная модель, не пробел гейта.
- Red team — атака исполнителя (субагент red-team в среде OpenCode отсутствует);
  возражения и их влияние на варианты зафиксированы в 03.
- Проект и весь пакет лежат в tmp-папке по условию задачи; в репозиторий попадает только этот отчёт.
