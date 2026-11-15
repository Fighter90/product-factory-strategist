---
name: decision-support
description: Шаги 9–10 и работа после решения — фиксация решения с основаниями, ответственными, показателями и условиями пересмотра; контроль обязательств; пересмотр выводов при новых данных. Используй после выбора стратегии, при возвращении к проекту, при появлении новых сведений.
---

# Поддержка решения и пересмотр

Карты: `M-decision-daci`, `M-outcome-roadmap`, `M-risks`, `M-success-metrics`.

## Фиксация (decision)
1. `pfs decision add --title "…" --decision "…" --owner "<роль>" --grounds C###,… --option B --rejected A,C,D
   --metric "<метрика>: <база> -> <цель> @<дата>" --review <дата> --trigger "<условие пересмотра>"
   --commit "<что>|<кто>|<когда>"` — по одному `--commit` на обязательство.
   Основания — только активные C###; условия пересмотра — наблюдаемые («удержание M1 < 40% два месяца подряд»).
2. Покажи запись человеку на утверждение (`pfs ask`). `pfs step decision done`.

## Сопровождение (monitoring) — при каждом возвращении к проекту
3. `pfs decision due` → что решать сейчас, просроченные обязательства, устаревшие основания. Начни ответ с этого.
4. Выполнено → `pfs decision done --id D001 --commitment K1`.

## Новые данные
5. Зарегистрируй источник → выпиши утверждения.
6. Если новое противоречит старому: `pfs claim supersede --id C### "…" --reason "…"` (или `retract`).
   Инструмент покажет затронутые выводы, строки документов и решения (`pfs impact`).
7. Выводы на замещённых основаниях: `pfs claim rebase` (текст не меняется) или `supersede --from …` (если меняется смысл).
   Решение на замещённых основаниях: `pfs decision rebase --id D### --note "почему вывод не меняется"`.
8. Обнови только затронутые места (`pfs check` укажет на ссылки на отозванные C###). Если затронуто основание
   решения — `pfs decision status --id D### --status revisit --note "…"` и сообщи владельцу решения.
9. Прошлые ответы агента — не факты: перепроверяй их по C###/S###, а не по памяти чата.

## English

# Decision support and revision

Maps: `M-decision-daci`, `M-outcome-roadmap`, `M-risks`, `M-success-metrics`.

## Recording (decision)
1. `pfs decision add --title "…" --decision "…" --owner "<role>" --grounds C###,… --option B --rejected A,C,D
   --metric "<metric>: <baseline> -> <target> @<date>" --review <date> --trigger "<review condition>"
   --commit "<what>|<who>|<when>"` — one `--commit` per commitment. Grounds — active C###s only; review conditions
   must be observable ("M1 retention < 40% for two months in a row").
2. Show the record to the human for approval (`pfs ask`). `pfs step decision done`.

## Monitoring — every time you return to the project
3. `pfs decision due` → what to decide now, overdue commitments, stale grounds. Start the reply with this.
4. Done → `pfs decision done --id D001 --commitment K1`.

## New data
5. Register the source → extract the claims.
6. If the new contradicts the old: `pfs claim supersede --id C### "…" --reason "…"` (or `retract`).
   The tool shows the affected conclusions, document lines and decisions (`pfs impact`).
7. Conclusions on superseded grounds: `pfs claim rebase` (the text stays) or `supersede --from …` (if the meaning
   changes). A decision on superseded grounds: `pfs decision rebase --id D### --note "why the conclusion stands"`.
8. Update only the affected places (`pfs check` flags links to retracted C###). If a decision's ground is affected —
   `pfs decision status --id D### --status revisit --note "…"` and tell the decision owner.
9. The agent's past answers are not facts: re-verify them against C###/S###, not against chat memory.
