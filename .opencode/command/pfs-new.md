---
description: Создать новый проект стратегии (шаг intake)
agent: build
---
Аргументы: $ARGUMENTS
Прочитай AGENTS.md. Создай проект `python3 -m tools.pfs new "<название>" "<запрос дословно>"`,
затем веди шаг intake по skill .claude/skills/intake/SKILL.md: максимум 3 вопроса руководителю
(через `pfs ask`), бриф в 00_brief.md, `pfs step intake done`. Дальше — по процессу 12 шагов.
