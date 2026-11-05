"""PreToolUse(WebFetch): разрешённые источники проекта. Запрещённый домен блокируется до запроса."""
from _common import active_pdir, emit, guard, read_input


def main():
    data = read_input()
    url = (data.get("tool_input") or {}).get("url", "")
    pdir = active_pdir()
    if not pdir or not url:
        return
    from tools.pfs import sources
    ok, why = sources.check_url_allowed(pdir, url)
    if not ok:
        emit({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                     "permissionDecisionReason": f"[pfs] {why}. Источник не входит в разрешённые для проекта (project.json → allowed_sources)."}})


guard(main)
