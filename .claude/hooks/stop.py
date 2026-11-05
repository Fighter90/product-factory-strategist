"""Stop: пересчитать стоимость сессии по транскрипту (идемпотентно) и показать пользователю."""
from pathlib import Path

from _common import active_pdir, emit, guard, read_input


def main():
    data = read_input()
    pdir = active_pdir()
    tp = data.get("transcript_path")
    if not pdir or not tp or not Path(tp).exists():
        return
    from tools.pfs import cost
    s = cost.record_session(pdir, data.get("session_id") or Path(tp).stem, Path(tp))
    total = cost.summary(pdir)
    emit({"systemMessage": f"pfs: сессия ${s['usd']:.2f}, проект всего ${total['usd']:.2f} (~{total['rub']:.0f} ₽)"})


guard(main)
