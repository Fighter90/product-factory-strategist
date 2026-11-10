"""Создание проекта, состояние шагов, продолжение после перерыва."""
from __future__ import annotations

from pathlib import Path

from . import core
from .core import PfsError, STAGES, STAGE_IDS

OUTPUT_FILES = {
    "intake": "00_brief.md",
    "research": "01_research_plan.md",
    "situation": "02_situation.md",
    "options": "03_options.md",
    "strategy": "04_product_strategy.md",
    "comms": "05_comms_strategy.md",
    "validation": "06_validation_plan.md",
    "review": "07_quality_review.md",
}

BRIEF_TEMPLATE = """# Бриф: {title}

> Заполняется на шаге intake. Поля с «?» — открытые вопросы к руководителю продукта.

| Поле | Значение |
|---|---|
| Исходный запрос (дословно) | {question} |
| Уточнённый вопрос | ? |
| Решение, которое будет принято по результату | ? |
| Цель и критерий успеха | ? |
| Получатель результата и формат | ? |
| Ограничения (сроки, бюджет, регуляторика, бренд) | ? |
| Доступные данные и материалы | ? |
| Разрешённые источники | открытые источники + материалы, переданные пользователем |
| Что считаем вне рамок | ? |
| Дедлайн | ? |
"""


def create(title: str, question: str, slug: str | None = None, owner_role: str = "руководитель продукта") -> Path:
    slug = slug or core.slugify(title)
    pdir = core.projects_dir() / slug
    if (pdir / "project.json").exists():
        raise PfsError(f"Проект '{slug}' уже существует — продолжите его: pfs use {slug} && pfs status")
    for sub in ("sources/raw", "outputs", "interviews/real", "interviews/synthetic", "analysis"):
        (pdir / sub).mkdir(parents=True, exist_ok=True)
    core.write_json(pdir / "project.json", {
        "slug": slug, "title": title, "question": question, "owner_role": owner_role,
        "created": core.now(),
        "allowed_sources": {"domains": [], "deny_domains": [], "note": "пусто = любые открытые источники"},
        "stale_after_days": 180,
    })
    core.write_json(pdir / "state.json", {
        "stage": "intake",
        "steps": {sid: {"status": "pending"} for sid in STAGE_IDS},
        "next_action": "Уточнить запрос: вопрос, решение, получатель, ограничения, данные (шаг intake)",
        "open_questions": [], "awaiting_human": None, "updated": core.now(),
    })
    core.atomic_write(pdir / "outputs" / OUTPUT_FILES["intake"], BRIEF_TEMPLATE.format(title=title, question=question))
    for name in ("sources.jsonl", "claims.jsonl", "decisions.jsonl", "log.jsonl"):
        (pdir / name).touch()
    core.set_active(slug)
    core.log(pdir, "action", f"Создан проект «{title}»", step="intake")
    return pdir


def load_state(pdir: Path) -> dict:
    return core.read_json(pdir / "state.json", {})


def save_state(pdir: Path, state: dict) -> None:
    state["updated"] = core.now()
    core.write_json(pdir / "state.json", state)


def set_step(pdir: Path, step: str, status: str, note: str | None = None, next_action: str | None = None) -> dict:
    if step not in STAGE_IDS:
        raise PfsError(f"Неизвестный шаг '{step}'. Шаги: {', '.join(STAGE_IDS)}")
    if status not in ("pending", "in_progress", "done", "skipped"):
        raise PfsError("Статус: pending | in_progress | done | skipped")
    state = load_state(pdir)
    entry = state["steps"].setdefault(step, {})
    if entry.get("status") == "done" and status == "done":
        # Идемпотентность: повторная отметка не дублирует запись в журнале.
        return state
    entry.update({"status": status, "ts": core.now()})
    if note:
        entry["note"] = note
    if status == "in_progress":
        state["stage"] = step
    if status in ("done", "skipped"):
        nxt = next((s for s in STAGE_IDS if state["steps"].get(s, {}).get("status") not in ("done", "skipped")), None)
        state["stage"] = nxt or "monitoring"
    if next_action:
        state["next_action"] = next_action
    save_state(pdir, state)
    core.log(pdir, "step", f"{step} → {status}" + (f": {note}" if note else ""), step=step)
    return state


def ask_human(pdir: Path, question: str, options: list[str] | None = None) -> None:
    state = load_state(pdir)
    state["awaiting_human"] = {"question": question, "options": options or [], "asked": core.now()}
    save_state(pdir, state)
    core.log(pdir, "human", f"Вопрос руководителю: {question}", step=state.get("stage"))


def answer_human(pdir: Path, answer: str) -> None:
    state = load_state(pdir)
    q = (state.get("awaiting_human") or {}).get("question", "")
    state["awaiting_human"] = None
    state.setdefault("answers", []).append({"question": q, "answer": answer, "ts": core.now()})
    save_state(pdir, state)
    core.log(pdir, "human", f"Ответ руководителя: {answer}", step=state.get("stage"))


def add_open_question(pdir: Path, text: str, close: bool = False) -> None:
    state = load_state(pdir)
    qs = state.setdefault("open_questions", [])
    if close:
        state["open_questions"] = [q for q in qs if q != text]
    elif text not in qs:
        qs.append(text)
    save_state(pdir, state)


def status_text(pdir: Path, brief: bool = False) -> str:
    """Сводка для продолжения работы: где остановились и что делать дальше."""
    from . import claims as claims_mod, cost as cost_mod
    meta = core.read_json(pdir / "project.json", {})
    state = load_state(pdir)
    lines = [f"ПРОЕКТ: {meta.get('title')}  [{meta.get('slug')}]",
             f"Запрос: {meta.get('question')}"]
    marks = {"done": "✔", "in_progress": "▶", "skipped": "–", "pending": "·"}
    bar = " ".join(f"{marks.get(state['steps'].get(s['id'], {}).get('status', 'pending'), '·')}{s['id']}"
                   for s in STAGES)
    lines.append(f"Шаги: {bar}")
    lines.append(f"Текущий шаг: {state.get('stage')} | Следующее действие: {state.get('next_action')}")
    if state.get("awaiting_human"):
        ah = state["awaiting_human"]
        opts = f" Варианты: {' / '.join(ah['options'])}" if ah.get("options") else ""
        lines.append(f"⏸ ЖДЁМ РЕШЕНИЯ РУКОВОДИТЕЛЯ: {ah['question']}.{opts}")
    if state.get("open_questions"):
        lines.append("Открытые вопросы: " + "; ".join(state["open_questions"][:6]))
    srcs = core.read_jsonl(pdir / "sources.jsonl")
    cl = claims_mod.load(pdir)
    active = [c for c in cl if c.get("status") == "active"]
    by_kind: dict[str, int] = {}
    for c in active:
        by_kind[c["kind"]] = by_kind.get(c["kind"], 0) + 1
    decs = core.read_jsonl(pdir / "decisions.jsonl")
    lines.append(f"Источники: {len(srcs)} | Утверждения: {len(active)} {by_kind} | Решения: {len(decs)}")
    from . import export as export_mod
    lines += export_mod.freshness_warnings(pdir)
    total = cost_mod.summary(pdir)
    lines.append(f"Стоимость: ${total['usd']:.2f} (~{total['rub']:.0f} ₽), токенов {total['tokens']:,}".replace(",", " "))
    if not brief:
        logs = core.read_jsonl(pdir / "log.jsonl")[-8:]
        if logs:
            lines.append("Последние действия:")
            lines += [f"  {r['ts'][:16]} [{r['kind']}] {r['msg'][:110]}" for r in logs]
        outs = sorted(p.name for p in (pdir / "outputs").glob("*.md"))
        lines.append("Документы: " + ", ".join(outs))
    return "\n".join(lines)


def is_finished(pdir: Path) -> bool:
    """Проект завершён: все шаги процесса отмечены done/skipped."""
    steps = load_state(pdir).get("steps", {})
    return all(steps.get(sid, {}).get("status") in ("done", "skipped") for sid in STAGE_IDS)


def six_pager_due(pdir: Path) -> bool:
    """Комитет-пакет нужен: шаг review пройден, а outputs/SIX_PAGER.md ещё не собран."""
    if (pdir / "outputs" / "SIX_PAGER.md").exists():
        return False
    st = load_state(pdir).get("steps", {}).get("review", {})
    return st.get("status") == "done"


def next_text(pdir: Path) -> str:
    """«Что решать сейчас»: шаг, ожидания человека, обязательства, пересмотры, открытые вопросы."""
    from . import decisions as decisions_mod
    state = load_state(pdir)
    meta = core.read_json(pdir / "project.json", {})
    lines = [f"ЧТО РЕШАТЬ СЕЙЧАС — {meta.get('title')} [{meta.get('slug')}]"]
    lines.append(f"Шаг: {state.get('stage')} · Далее: {state.get('next_action')}")
    if six_pager_due(pdir):
        # PRO-32: six-pager собирают на review — напоминаем первым пунктом, пока его нет.
        lines.append("📋 Собрать комитет-пакет: pfs calc scaffold → pfs calc all → pfs export "
                     "--six-pager (spec: knowledge/templates/SIX_PAGER_PROMPT.md)")
    if state.get("awaiting_human"):
        ah = state["awaiting_human"]
        opts = f" ({' / '.join(ah['options'])})" if ah.get("options") else ""
        lines.append(f"⏸ Ждём вашего ответа: {ah['question']}{opts}")
    due = decisions_mod.due(pdir)
    if due.get("overdue"):
        lines.append(f"⏰ Просроченные обязательства: {len(due['overdue'])}")
        for o in due["overdue"][:3]:
            label = o.get("commitment") or o.get("text") or str(o) if isinstance(o, dict) else str(o)
            lines.append(f"  · {str(label)[:120]}")
    if due.get("review_now"):
        ids = [d.get("id", d) if isinstance(d, dict) else str(d) for d in due["review_now"]]
        lines.append(f"🔎 К пересмотру решений: {', '.join(map(str, ids[:3]))}")
    if due.get("stale_grounds"):
        lines.append(f"⚠ Устаревшие основания: {len(due['stale_grounds'])} — pfs decision rebase / claim supersede")
    oq = state.get("open_questions", [])
    if oq:
        lines.append(f"❓ Открытые вопросы: {len(oq)}")
        lines += ["  · " + q[:120] for q in oq[:3]]
    if len(lines) == 2:
        lines.append("Долгов нет. Текущий шаг процесса — см. pfs status.")
    lines.append("Обновить источники после изменений: pfs source refresh <S###>")
    return "\n".join(lines)


def list_projects() -> list[dict]:
    out = []
    for p in sorted(core.projects_dir().glob("*/project.json")):
        meta = core.read_json(p, {})
        st = core.read_json(p.parent / "state.json", {})
        out.append({"slug": meta.get("slug"), "title": meta.get("title"), "stage": st.get("stage")})
    return out
