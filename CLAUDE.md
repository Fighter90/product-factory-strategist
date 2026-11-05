@AGENTS.md

## Особенности Claude Code

- Навыки (`.claude/skills/*`) вызываются через Skill tool или `/имя`: `/strategist` — полный процесс или продолжение.
- Субагенты (`.claude/agents/*`) запускаются через Agent tool по имени; модель каждого прописана во frontmatter
  из `config/models.json` (`python3 -m tools.pfs models sync`).
- Хуки (`.claude/settings.json`): SessionStart — состояние проекта; PreToolUse(WebFetch) — разрешённые домены;
  PostToolUse — журнал, проверка на внедрённые инструкции, автопроверка документов; Stop — стоимость сессии.
- MCP-сервер `pfs-strategist` (`.mcp.json`) дублирует ключевые команды CLI.
