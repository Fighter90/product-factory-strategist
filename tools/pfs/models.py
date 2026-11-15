"""Маршрутизация моделей: задача → уровень → конкретная модель активного профиля."""
from __future__ import annotations

import re
from pathlib import Path

from . import core
from .core import PfsError

TIER_ORDER = ("fast", "balanced", "deep", "frontier")


def load() -> dict:
    return core.read_json(core.CONFIG / "models.json", {})


def profile(cfg: dict | None = None, name: str | None = None) -> dict:
    cfg = cfg or load()
    name = name or cfg.get("active_profile", "claude")
    if name not in cfg.get("profiles", {}):
        raise PfsError(f"Профиль '{name}' не найден. Есть: {', '.join(cfg.get('profiles', {}))}")
    return cfg["profiles"][name]


def pick(task: str, *, economy: bool = False, critical: bool = False, cfg: dict | None = None) -> dict:
    cfg = cfg or load()
    tasks = cfg.get("tasks", {})
    if task not in tasks:
        raise PfsError(f"Задача '{task}' не описана в config/models.json. Есть: {', '.join(tasks)}")
    t = tasks[task]
    if t.get("optional") and not critical:
        task, t = "strategy", tasks["strategy"]
    tier = t["tier"]
    if economy and tier == "deep" and task not in ("red_team",):
        tier = "balanced"
    m = profile(cfg)["tiers"][tier]
    return {"task": task, "tier": tier, "model": m["model"], "alias": m["alias"], "effort": t.get("effort"),
            "why": t.get("why"), "escalate_to": t.get("escalate_to")}


def escalate(pdir: Path | None, task: str, reason: str) -> dict:
    cur = pick(task)
    idx = TIER_ORDER.index(cur["tier"])
    if idx == len(TIER_ORDER) - 1:
        raise PfsError("Уже максимальный уровень")
    tier = TIER_ORDER[idx + 1]
    m = profile()["tiers"][tier]
    res = dict(cur, tier=tier, model=m["model"], alias=m["alias"], why=f"эскалация: {reason}")
    if pdir:
        core.log(pdir, "route", f"Эскалация {task}: {cur['model']} → {m['model']} ({reason})", step=task)
    return res


def table() -> str:
    cfg = load()
    prof = profile(cfg)
    out = [f"Профиль: {cfg.get('active_profile')} — {prof.get('description', '')}",
           "| Задача | Уровень | Модель | Effort | Почему |", "|---|---|---|---|---|"]
    for name, t in cfg.get("tasks", {}).items():
        out.append(f"| {name} | {t['tier']} | {prof['tiers'][t['tier']]['model']} | {t.get('effort', '')} | {t.get('why', '')} |")
    return "\n".join(out)


# Какой задаче соответствует субагент (имя файла в .claude/agents без .md).
AGENT_TASKS = {
    "researcher": "desk_research", "evidence-auditor": "judge", "red-team": "red_team",
    "synthetic-respondent": "synthetic_respondent", "data-analyst": "data_analysis",
    "ux-analyst": "ux_analysis", "comms-strategist": "comms_copy", "router": "route",
    "editor": "editor",
}


def sync_agents(agents_dir: Path | None = None) -> list[str]:
    """Прописать model: в frontmatter субагентов по config/models.json."""
    agents_dir = agents_dir or core.ROOT / ".claude" / "agents"
    changed = []
    for f in sorted(agents_dir.glob("*.md")):
        task = AGENT_TASKS.get(f.stem)
        if not task:
            continue
        alias = pick(task)["alias"]
        text = f.read_text(encoding="utf-8")
        new = re.sub(r"(?m)^model:.*$", f"model: {alias}", text, count=1)
        if new != text:
            core.atomic_write(f, new)
            changed.append(f"{f.stem} → {alias}")
    return changed


def use_profile(name: str) -> None:
    cfg = load()
    profile(cfg, name)
    cfg["active_profile"] = name
    core.write_json(core.CONFIG / "models.json", cfg)
