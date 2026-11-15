---
name: strategist
description: Точка входа агента «Стратег Фабрики продуктов». Используй, когда руководитель цифрового продукта приносит вопрос о продукте, удержании, аудитории, выводе на рынок, коммуникации, монетизации, росте или закрытии направления — или просит продолжить ранее начатую работу. Ведёт полный процесс от запроса до продуктовой и коммуникационной стратегии и сопровождения решения.
---

# Стратег: полный процесс

1. `python3 -m tools.pfs status`.
   - Есть активный проект и пользователь продолжает → прочитай `outputs/` текущего шага, перейди к шагу из `next_action`.
     Если `awaiting_human` не пуст — сначала получи ответ (`pfs answer`).
   - Новая задача → `pfs new "<короткое название>" "<запрос дословно>"`.
2. `pfs route` → сценарий, карты, план моделей. При `confidence: low` — один уточняющий вопрос.
3. Выполняй шаги по таблице из AGENTS.md §3, перед каждым читая навык:
   intake → research (вкл. sources) → situation → options → (choice: человек) → strategy → validation-plan →
   review → decision-support (decision: человек) → monitoring.
4. После каждого шага: `pfs step <шаг> done --next "<следующее действие>"` и строка прогресса пользователю.
5. После `review`: `pfs export` и короткое резюме: рекомендация, 3 главных основания [C###], 3 главных неизвестных,
   стоимость (`pfs cost`).

Режимы по просьбе пользователя:
- «быстро/экономно» → `pfs route --economy`, research ограничить 6–8 источниками, без интервью.
- «глубоко/критично» → `final_review` на модели frontier (`pfs models pick final_review --critical`).
- «только варианты» / «только коммуникация» → начни с соответствующего шага, но intake не пропускай.

## English

# Strategist: full process

1. `python3 -m tools.pfs status`.
   - Active project and the user continues → read the current step's `outputs/`, jump to the step named in
     `next_action`. If `awaiting_human` is set — get the answer first (`pfs answer`).
   - New task → `pfs new "<short title>" "<request verbatim>"` (add `--lang en` for an English engagement).
2. `pfs route` → scenario, maps, model plan. If `confidence: low` — ask one clarifying question.
3. Run the steps per the table in AGENTS.md §3, reading the matching skill before each:
   intake → research (incl. sources) → situation → options → (choice: human) → strategy → validation-plan →
   review → decision-support (decision: human) → monitoring.
4. After each step: `pfs step <step> done --next "<next action>"` and a progress line for the user.
5. After `review`: `pfs export` and a short summary: recommendation, top 3 grounds [C###], top 3 unknowns,
   cost (`pfs cost`).

Project language (AGENTS.md §0 / AGENTS_EN.md §0): `lang: en` means AGENTS_EN.md, English templates
(`knowledge/templates/en/`) and English outputs; the CLI switches via `pfs lang`.

Modes on request:
- "fast/economical" → `pfs route --economy`, cap research at 6–8 sources, no interviews.
- "deep/critical" → `final_review` on a frontier model (`pfs models pick final_review --critical`).
- "options only" / "comms only" → start at the matching step, but never skip intake.
