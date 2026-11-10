"""Lock вердикта review (PRO-27): снимок реестра после ревизии и предупреждение об устаревании.

Кейс из аудита: 07_quality_review сказал «готово 21/22», после чего в реестр добавили
источники и утверждения и правили документы — повторная проверка не проводилась, а
вердикт продолжал считаться действительным. `pfs review lock` фиксирует снимок реестра
(sha256 claims.jsonl/sources.jsonl и документов 00–07) в outputs/.review_state.json;
пока реестр меняется после lock, `pfs check` и `pfs status` показывают пометку
«вердикт review устарел — реестр изменился после ревизии; повторите evidence-auditor»
(символ «⚠ » добавляют места текстового вывода, чтобы warnings в `--json` — хуки,
MCP pfs_check — оставались однородными), а `pfs export` включает пометку в Приложение D
(через отчёт check). Повторный lock после повторной ревизии снимает предупреждение.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

from . import core, project

STATE = ".review_state.json"


def _file_sha(path: Path) -> str | None:
    """sha256 файла или None, если файла нет."""
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None


def snapshot(pdir: Path) -> dict:
    """Снимок реестра на момент lock: sha256 claims/sources и документов 00–07."""
    return {"at": core.now(),
            "claims_sha": _file_sha(pdir / "claims.jsonl"),
            "sources_sha": _file_sha(pdir / "sources.jsonl"),
            "documents": {name: _file_sha(pdir / "outputs" / name)
                          for name in project.OUTPUT_FILES.values()}}


def read_state(pdir: Path) -> dict | None:
    """Снимок из последнего lock или None, если lock ещё не выполнялся."""
    snap = core.read_json(pdir / "outputs" / STATE)
    return snap if isinstance(snap, dict) else None


def lock(pdir: Path) -> dict:
    """Зафиксировать снимок реестра (после ревизии evidence-auditor или повторной)."""
    snap = snapshot(pdir)
    core.write_json(pdir / "outputs" / STATE, snap)
    core.log(pdir, "action", "Вердикт review зафиксирован: снимок реестра в outputs/" + STATE,
             tool="pfs review lock")
    return snap


def changed(pdir: Path) -> list[str]:
    """Что изменилось после lock: [] — lock не было или реестр не менялся.
    Хеш ловит и правки на месте (retract/rebase/supersede, source refresh), и правки
    документов, и появление файла, которого при lock не было."""
    snap = read_state(pdir)
    if not snap:
        return []
    out = []
    if _file_sha(pdir / "claims.jsonl") != snap.get("claims_sha"):
        out.append("claims.jsonl")
    if _file_sha(pdir / "sources.jsonl") != snap.get("sources_sha"):
        out.append("sources.jsonl")
    for name, sha in (snap.get("documents") or {}).items():
        if _file_sha(pdir / "outputs" / name) != sha:
            out.append(name)
    return out


def stale_warnings(pdir: Path) -> list[str]:
    """[«вердикт review устарел — реестр изменился после ревизии; повторите
    evidence-auditor»] — реестр изменился после lock; [] — нет. Сообщение сырое,
    без «⚠ » (ревью 2): префикс добавляют места текстового вывода
    (check.report_text, project.status_text, cli.cmd_export), чтобы warnings
    в `--json` (хуки, MCP pfs_check) были однородными."""
    ch = changed(pdir)
    if not ch:
        return []
    return ["вердикт review устарел — реестр изменился после ревизии; повторите evidence-auditor "
            f"(изменилось: {', '.join(ch)}); после повторной ревизии зафиксируйте снова: pfs review lock"]
