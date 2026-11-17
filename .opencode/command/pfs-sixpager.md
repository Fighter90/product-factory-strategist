---
description: Собрать six-pager отчёт для комитета (пакет данных + каркас со слотами → текст writer'ом → 0 ошибок)
agent: build
---
Прочитай AGENTS.md и skill .claude/skills/six-pager/SKILL.md. Для активного проекта:
1) проверь готовность outputs/02–06; 2) собери calcs.json из утверждений C###;
3) запусти субагентом `python3 -m tools.pfs calc all`; 4) `python3 -m tools.pfs export --six-pager`
— соберёт пакет данных `outputs/six_pager_pack.md` и каркас `outputs/SIX_PAGER.md` со слотами;
5) запусти субагента `six-pager-writer` — текст по слотам только из пакета (PRO-46);
6) обязательный цикл: `pfs check --six-pager` → правки → 0 ошибок; затем `pfs check --strict`;
покажи путь к SIX_PAGER.md, список Excel и что редактировать на листе «Ввод».
