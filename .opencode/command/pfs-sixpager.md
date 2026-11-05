---
description: Собрать six-pager отчёт для комитета (FAQ-1…6 + Excel-приложения)
agent: build
---
Прочитай AGENTS.md и skill .claude/skills/six-pager/SKILL.md. Для активного проекта:
1) проверь готовность outputs/02–06; 2) собери calcs.json из утверждений C###;
3) запусти субагентом `python3 -m tools.pfs calc all`; 4) `python3 -m tools.pfs export --six-pager`;
5) `pfs check --strict`; покажи путь к SIX_PAGER.md, список Excel и что редактировать на листе «Ввод».
