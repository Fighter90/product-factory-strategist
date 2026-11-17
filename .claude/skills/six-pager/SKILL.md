---
name: six-pager
description: Шести-страничный стратегический отчёт (FAQ-1…FAQ-6) с Excel-приложениями. Используй на шаге review или когда руководитель просит «собери six-pager», «отчёт для комитета», «как в примере стратегии».
---

# Six-pager с Excel-приложениями

Цель — отчёт в структуре референса (см. `knowledge/templates/six_pager.md` и карту M-six-pager),
в котором числа считаются в Excel-приложениях на формулах. Инструмент собирает **пакет данных
и каркас**, текст по слотам пишет субагент `six-pager-writer` по эталону — работа идёт в фоне,
не блокируя диалог (PRO-46).

## Процедура

1. **Готовность.** Проверь, что есть `02_situation.md`, `03_options.md`, `04_product_strategy.md`,
   `06_validation_plan.md`. Чего-то нет — сначала доделай соответствующий шаг процесса, six-pager не собирать.
2. **Числа из реестра.** Собери параметры расчётов из утверждений и создай/обнови
   `projects/<slug>/calcs.json` (секции `unit_econ`, `growth`, `cohort`, `market`).
   Каждое значение должно прослеживаться до C### — пометь это в поле `note` секции.
   Чего в реестре нет — бери пример из `tools/pfs/calc.py: DEFAULTS` и явно помечай «ПРИМЕР — заменить».
3. **Расчёт в фоне.** Запусти субагентом (data-analyst) команду
   `python3 -m tools.pfs calc all --project <slug>` — он создаст 4 книги в `outputs/attachments/`.
   Не жди результата в основном диалоге: субагент вернёт список файлов.
4. **Пакет данных и каркас.** `python3 -m tools.pfs export --six-pager` соберёт:
   - `outputs/six_pager_pack.json` + читаемая версия `six_pager_pack.md` — утверждения с силой A–D,
     источники, расчёты из calcs, варианты, выбор руководителя, инициативы, KPI, решения;
   - `outputs/SIX_PAGER.md` — каркас FAQ-1…6 со слотами `> **Слот (заполните):** …` и расчётными
     артефактами (юнит-экономика, матрица тактик, KPI-таблицы, решение D###).
   Рабочие документы 02/03/04/06 **не вставляются** в six-pager: полная версия с доказательствами — REPORT.md.
5. **Текст — субагентом six-pager-writer (модель уровня deep).** Запусти субагента `six-pager-writer`:
   он пишет каждый раздел по слотам ТОЛЬКО из пакета данных, без вставки рабочих документов,
   по спецификации `knowledge/templates/SIX_PAGER_PROMPT.md` (RU) или `SIX_PAGER_PROMPT_EN.md` (EN,
   стиль `knowledge/templates/STYLE_EN.md`). Запускай в фоне, результат — перезаписанный
   `SIX_PAGER.md` (+ `SIX_PAGER_EN.md` для EN-версии, если её собирали).
6. **Обязательный цикл проверки (пропустить нельзя).** После записи текста:
   `python3 -m tools.pfs check --six-pager` → передать ошибки субагенту `six-pager-writer` на правку →
   повторять, пока **0 ошибок**. Каркас со слотами и недописанный текст линтер держит в ошибках —
   «готово» можно объявлять только при 0 ошибок (затем `pfs check` без новых ошибок).
7. **Самопроверка.** В каждом FAQ-разделе есть содержимое (не заглушка и не слот); числа в тексте
   совпадают с Excel-приложениями; таблица приложений заполнена.
8. **Показ руководителю.** Путь к `SIX_PAGER.md`; список Excel с пояснением «лист Ввод — что редактировать»;
   напомни: формулы пересчитываются при открытии (Excel / Numbers / LibreOffice), предпросмотр показывает
   кэш значения на момент генерации.

## Ограничения

- Книги генерируются без внешних пакетов (stdlib): простые стили, без диаграмм. Диаграммы руководитель добавит сам в Excel.
- Числа в SIX_PAGER.md и в Excel должны совпадать: если обновил `calcs.json` — перезапусти `pfs calc`,
  `export` (свежий пакет данных) и цикл из шага 6.
- Excel-приложения не заменяют реестр утверждений: источник каждого параметра — C###/S### в реестре и в `note`.
- `pfs export --six-pager` пересобирает каркас и затирает написанный текст — пересобирай только
  вместе с новым проходом six-pager-writer и циклом из шага 6.

## English

# Six-pager with Excel appendices

Goal — a report in the reference structure (see `knowledge/templates/six_pager.md` / `en/six_pager.md` and the
M-six-pager map) where the numbers are computed in formula-driven Excel appendices. The tool assembles the
**data package and the skeleton**; the prose is written per the reference by the `six-pager-writer` subagent —
in the background, without blocking the dialogue (PRO-46).

## Procedure

1. **Readiness.** Check that `02_situation.md`, `03_options.md`, `04_product_strategy.md`, `06_validation_plan.md`
   exist. If something is missing — finish that process step first; do not assemble the six-pager.
2. **Numbers from the registry.** Collect calculation parameters from the claims and create/update
   `projects/<slug>/calcs.json` (sections `unit_econ`, `growth`, `cohort`, `market`). Every value must trace back to
   a C### — note it in the section's `note` field. Anything missing from the registry — take the sample from
   `tools/pfs/calc.py: DEFAULTS` and mark it explicitly "EXAMPLE — replace".
3. **Background calculation.** Run via a subagent (data-analyst): `python3 -m tools.pfs calc all --project <slug>` —
   it creates 4 workbooks in `outputs/attachments/`. Don't wait in the main dialogue: the subagent returns the file list.
4. **Data package and skeleton.** `python3 -m tools.pfs export --six-pager` produces:
   - `outputs/six_pager_pack.json` (+ human-readable `six_pager_pack.md`) — claims with grades A–D, sources,
     calculations, options, the leader's choice, initiatives, KPI, decisions;
   - `outputs/SIX_PAGER.md` — the FAQ-1…6 skeleton with `> **Слот (заполните):** …` slots plus the computed
     artifacts (unit economics, tactics matrix, KPI tables, the D### decision).
   Working documents 02/03/04/06 are **never pasted** into the six-pager: the full evidence version lives in REPORT.md.
5. **Prose — the `six-pager-writer` subagent (deep-tier model).** Launch it: it fills every slot from the
   data package ONLY, pasting no working documents, per `knowledge/templates/SIX_PAGER_PROMPT_EN.md`
   (EN) or `SIX_PAGER_PROMPT.md` (RU). Run in the background; the result overwrites `SIX_PAGER.md`
   (+ `SIX_PAGER_EN.md` when the EN version was assembled).
6. **Mandatory check loop (cannot be skipped).** After the prose is written:
   `python3 -m tools.pfs check --six-pager` → hand the errors back to `six-pager-writer` → repeat until
   **0 errors**. The skeleton and unfinished prose keep the linter red — "done" may only be declared at 0 errors
   (then `pfs check` with no new errors).
7. **Self-check.** Every FAQ section has real content (no stubs, no slots left); numbers match the Excel
   appendices; the appendices table is filled.
8. **Show the leader.** The path to `SIX_PAGER.md`; the Excel list with "the Input sheet — what to edit";
   remind them: formulas recompute on open (Excel / Numbers / LibreOffice), previews show cached values
   from generation time.

## Constraints

- Workbooks are generated without external packages (stdlib): simple styles, no charts. The leader can add charts in Excel.
- Numbers in SIX_PAGER.md and in Excel must match: if you updated `calcs.json` — re-run `pfs calc`,
  `export` (a fresh data package) and the step-6 loop.
- Excel appendices do not replace the claim registry: the source of every parameter is a C###/S### in the registry and in `note`.
- `pfs export --six-pager` rebuilds the skeleton and overwrites the written prose — re-run it only together
  with a fresh six-pager-writer pass and the step-6 loop.
