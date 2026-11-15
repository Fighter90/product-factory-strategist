---
name: six-pager
description: Шести-страничный стратегический отчёт (FAQ-1…FAQ-6) с Excel-приложениями. Используй на шаге review или когда руководитель просит «собери six-pager», «отчёт для комитета», «как в примере стратегии».
---

# Six-pager с Excel-приложениями

Цель — отчёт в структуре референса (см. `knowledge/templates/six_pager.md` и карту M-six-pager),
в котором числа считаются в Excel-приложениях на формулах, а агент собирает его в фоне, не блокируя диалог.

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
4. **Сборка.** `python3 -m tools.pfs export --six-pager` → `outputs/SIX_PAGER.md` + таблица приложений.
   (Флаг `--no-calcs` — пересобрать текст без перегенерации Excel.)
5. **Самопроверка.** В каждом FAQ-разделе есть содержимое (не заглушка); числа в тексте с [C###]/[S###];
   таблица приложений заполнена; `pfs check` без новых ошибок.
6. **Показ руководителю.** Путь к `SIX_PAGER.md`; список Excel с пояснением «лист Ввод — что редактировать»;
   напомни: формулы пересчитываются при открытии (Excel / Numbers / LibreOffice), предпросмотр показывает
   кэш значения на момент генерации.

## Ограничения

- Книги генерируются без внешних пакетов (stdlib): простые стили, без диаграмм. Диаграммы руководитель добавит сам в Excel.
- Числа в SIX_PAGER.md и в Excel должны совпадать: если обновил `calcs.json` — перезапусти `pfs calc` и `export`.
- Excel-приложения не заменяют реестр утверждений: источник каждого параметра — C###/S### в реестре и в `note`.

## English

# Six-pager with Excel appendices

Goal — a report in the reference structure (see `knowledge/templates/six_pager.md` / `en/six_pager.md` and the
M-six-pager map) where the numbers are computed in formula-driven Excel appendices; the agent assembles it in the
background without blocking the dialogue.

## Procedure

1. **Readiness.** Check that `02_situation.md`, `03_options.md`, `04_product_strategy.md`, `06_validation_plan.md`
   exist. If something is missing — finish that process step first; do not assemble the six-pager.
2. **Numbers from the registry.** Collect calculation parameters from the claims and create/update
   `projects/<slug>/calcs.json` (sections `unit_econ`, `growth`, `cohort`, `market`). Every value must trace back to
   a C### — note it in the section's `note` field. Anything missing from the registry — take the sample from
   `tools/pfs/calc.py: DEFAULTS` and mark it explicitly "EXAMPLE — replace".
3. **Background calculation.** Run via a subagent (data-analyst): `python3 -m tools.pfs calc all --project <slug>` —
   it creates 4 workbooks in `outputs/attachments/`. Don't wait in the main dialogue: the subagent returns the file list.
4. **Assembly.** `python3 -m tools.pfs export --six-pager` → `outputs/SIX_PAGER.md` + the appendices table.
   (`--no-calcs` — rebuild the text without regenerating Excel.)
5. **Self-check.** Every FAQ section has real content (not a stub); numbers in the text carry [C###]/[S###];
   the appendices table is filled; `pfs check` with no new errors.
6. **Show the leader.** The path to `SIX_PAGER.md`; the Excel list with "the Input sheet — what to edit";
   remind them: formulas recompute on open (Excel / Numbers / LibreOffice), previews show cached values
   from generation time.

## Constraints

- Workbooks are generated without external packages (stdlib): simple styles, no charts. The leader can add charts in Excel.
- Numbers in SIX_PAGER.md and in Excel must match: if you updated `calcs.json` — re-run `pfs calc` and `export`.
- Excel appendices do not replace the claim registry: the source of every parameter is a C###/S### in the registry and in `note`.
