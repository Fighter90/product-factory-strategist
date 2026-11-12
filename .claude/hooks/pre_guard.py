"""PreToolUse: реестры проекта правятся только через pfs; чтение — только внутри репозитория (PRO-58).

Bash/Edit/Write с записью в projects/*/{claims,sources,decisions}.jsonl или state.json
блокируется (deny) с подсказкой нужной команды pfs. Чтение вне репозитория требует
подтверждения человека (ask): Read/Grep/Glob — любой путь вне репо, Bash — пути в
домашней папке пользователя вне репо (чужие проекты `~/Projects/…`, dot-файлы
`~/.config/…`), как нарушения из задачи; системные и временные пути (/tmp, /usr)
не шумят. В OpenCode ту же роль играет permission `external_directory` (opencode.json).
"""
from __future__ import annotations

import re
from pathlib import Path

from _common import ROOT, emit, guard, read_input

# Реестр → подсказка, каким командом pfs его править (показывается при deny).
REGISTRIES = {
    "claims.jsonl": "Реестр утверждений правится только через pfs: python3 -m tools.pfs claim add|list|retract|supersede|rebase. "
                    "Перенумерация тегов в документах — одной командой: python3 -m tools.pfs claim retag --from C003 --to C059",
    "sources.jsonl": "Реестр источников правится только через pfs: python3 -m tools.pfs source add|fetch|refresh. "
                     "Целостность реестра: python3 -m tools.pfs doctor",
    "decisions.jsonl": "Реестр решений правится только через pfs: python3 -m tools.pfs decision add|done|rebase",
    "state.json": "Состояние шагов правится только через pfs: python3 -m tools.pfs step <шаг> in_progress|done --next \"…\"",
}

# Признаки записи в файл внутри сегмента команды. Сегмент пайплайна, где упомянут
# реестр и есть такой признак, блокируется; pfs-команды пропускаются всегда
# (pfs claim add-batch claims.jsonl легитимно называет файл реестра).
WRITERS = (r"\bsed\b.*(?:\s-i\b|--in-place)", r"\bperl\s+-(?:i|pe)\b", r"\bpython3?\s+-c\b",
           r"(?<![\d&])>(?!&)", r"\btee\b", r"\brm\b", r"\bmv\b", r"\bcp\b",
           r"\btruncate\b", r"\bdd\b", r"\bgit\s+(?:checkout|restore)\b")

# Пути в домашней папке пользователя: `~/…`, `$HOME/…` и развёрнутый абсолютный путь.
# Кавычки, пробелы, `;`, `|` и символы перенаправления границу пути не включают.
HOME_PATH = (r"(?:~/|\$HOME/)[^\s'\";|<>]+",)


def _home() -> Path:
    return Path.home()


def outside_path(raw: str) -> str | None:
    """Канонический путь, если он вне репозитория; иначе None."""
    if not raw or raw.startswith(("http://", "https://")):
        return None
    rp = Path(raw).expanduser()
    if not rp.is_absolute():
        rp = Path.cwd() / rp
    rp = rp.resolve()
    return None if (rp == ROOT or ROOT in rp.parents) else str(rp)


def home_outside_paths(command: str) -> list[str]:
    """Пути в домашней папке пользователя вне репозитория, упомянутые в команде.

    Чужие проекты и dot-файлы (`~/Projects/…`, `~/.config/…`) — то, что ловим;
    сама домашняя папка и системные пути (/tmp, /usr) не считаются.
    """
    home = _home()
    raw = [m.group(0).replace("$HOME", str(home)) for pat in HOME_PATH
           for m in re.finditer(pat, command)]
    raw += re.findall(re.escape(str(home)) + r"/[^\s'\";|<>]+", command)
    hits, seen = [], set()
    for token in raw:
        rp = Path(token).expanduser().resolve()
        if rp == ROOT or ROOT in rp.parents:
            continue  # внутри репозитория
        if rp == home or home not in rp.parents:
            continue  # не в домашней папке или сама домашняя
        if str(rp) not in seen:
            seen.add(str(rp))
            hits.append(str(rp))
    return hits


def _ask_outside(paths: list[str]) -> None:
    shown = paths[0] + (f" (+{len(paths) - 1})" if len(paths) > 1 else "")
    emit({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "ask",
                                 "permissionDecisionReason":
                                 f"[pfs] {shown} вне репозитория — требуется подтверждение. "
                                 "Чтение разрешено только внутри проекта: открытые источники и материалы, "
                                 "которые пользователь передал явно (правила 5 и 9 AGENTS.md)."}})


def _registry_hit(text: str) -> str | None:
    for name in REGISTRIES:
        if name in text:
            return name
    return None


def bash_guard(command: str) -> str | None:
    """Имя реестра, если команда записывает в него; иначе None."""
    for seg in command.split("|"):
        hit = _registry_hit(seg)
        if not hit:
            continue
        if seg.strip().startswith("python3 -m tools.pfs"):
            continue  # сам pfs пишет в реестры легитимно
        if any(re.search(pat, seg) for pat in WRITERS):
            return hit
    return None


def main():
    data = read_input()
    tool = data.get("tool_name", "")
    inp = data.get("tool_input") or {}
    if tool == "Bash":
        command = inp.get("command", "")
        hit = bash_guard(command)
        if hit:
            emit({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                         "permissionDecisionReason": f"[pfs] Прямая запись в {hit} запрещена. {REGISTRIES[hit]}"}})
            return
        outs = home_outside_paths(command)
        if outs:
            _ask_outside(outs)
    elif tool in ("Edit", "Write", "MultiEdit"):
        path = str(inp.get("file_path") or inp.get("notebook_path") or "")
        hit = _registry_hit(Path(path).name) if re.search(r"(^|/)projects(/|\\)", path) else None
        if hit:
            emit({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                         "permissionDecisionReason": f"[pfs] Прямая правка {hit} запрещена. {REGISTRIES[hit]}"}})
    elif tool in ("Read", "Grep", "Glob"):
        outside = outside_path(str(inp.get("file_path") or inp.get("path") or ""))
        if outside:
            _ask_outside([outside])


guard(main)
