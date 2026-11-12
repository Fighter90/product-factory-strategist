"""PreToolUse: реестры проекта правятся только через pfs; чтение — только внутри репозитория (PRO-58).

Bash/Edit/Write с записью в projects/*/{claims,sources,decisions}.jsonl или state.json
блокируется (deny) с подсказкой нужной команды pfs. Чтение вне репозитория (Read) требует
подтверждения человека (ask): только открытые источники и явно переданные материалы.
"""
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
        hit = bash_guard(inp.get("command", ""))
        if hit:
            emit({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                         "permissionDecisionReason": f"[pfs] Прямая запись в {hit} запрещена. {REGISTRIES[hit]}"}})
    elif tool in ("Edit", "Write", "MultiEdit"):
        path = str(inp.get("file_path") or inp.get("notebook_path") or "")
        hit = _registry_hit(Path(path).name) if re.search(r"(^|/)projects(/|\\)", path) else None
        if hit:
            emit({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                         "permissionDecisionReason": f"[pfs] Прямая правка {hit} запрещена. {REGISTRIES[hit]}"}})
    elif tool == "Read":
        raw = str(inp.get("file_path") or "")
        if not raw or raw.startswith(("http://", "https://")):
            return
        rp = Path(raw).expanduser()
        if not rp.is_absolute():
            rp = Path.cwd() / rp
        rp = rp.resolve()
        inside = rp == ROOT or ROOT in rp.parents
        if not inside:
            emit({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "ask",
                                         "permissionDecisionReason":
                                         f"[pfs] {rp} вне репозитория — требуется подтверждение. "
                                         "Чтение разрешено только внутри проекта: открытые источники и материалы, "
                                         "которые пользователь передал явно (правило 5 AGENTS.md)."}})


guard(main)
