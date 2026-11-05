"""SessionStart: вернуть агенту контекст проекта — продолжение работы в новом чате без пересказа."""
from _common import active_pdir, emit, guard, read_input


def main():
    read_input()
    pdir = active_pdir()
    if not pdir:
        ctx = ("[pfs] Активного проекта нет. Если пользователь пришёл с задачей — создайте проект: "
               "python3 -m tools.pfs new \"<название>\" \"<запрос дословно>\" и начните шаг intake (AGENTS.md).")
    else:
        from tools.pfs import decisions, project
        due = decisions.due_text(decisions.due(pdir))
        ctx = ("[pfs] Продолжение работы. Состояние проекта (из файлов, а не из памяти чата):\n"
               + project.status_text(pdir) + "\n\nПоддержка решений:\n" + due
               + "\n\nПрочитайте outputs/ текущего шага перед продолжением; выполненные шаги не повторяйте.")
    emit({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": ctx}})


guard(main)
