"""Stop: пересчитать стоимость сессии по транскрипту (идемпотентно) и показать пользователю.
PRO-32: проект завершён, а SIX_PAGER.md нет — напоминаем про комитет-пакет."""
from pathlib import Path

from _common import active_pdir, emit, guard, read_input


def main():
    data = read_input()
    pdir = active_pdir()
    if not pdir:
        return
    from tools.pfs import cost, project
    parts = []
    tp = data.get("transcript_path")
    if tp and Path(tp).exists():
        s = cost.record_session(pdir, data.get("session_id") or Path(tp).stem, Path(tp))
        total = cost.summary(pdir)
        # PRO-62: для план-сессий фактическая оплата $0 — показываем и эквивалент по API-ценам
        eq = f" (эквивалент ${total['usd_equivalent']:.2f})" if total.get("plan") else ""
        parts.append(f"pfs: сессия ${s['usd']:.2f}, проект всего ${total['usd']:.2f}{eq} (~{total['rub']:.0f} ₽)")
    if project.six_pager_due(pdir) and project.is_finished(pdir):
        parts.append("проект завершён, а outputs/SIX_PAGER.md нет — соберите комитет-пакет: "
                     "pfs calc scaffold → pfs calc all → pfs export --six-pager "
                     "(spec: knowledge/templates/SIX_PAGER_PROMPT.md)")
    if parts:
        emit({"systemMessage": "pfs: " + "; ".join(parts)})


guard(main)
