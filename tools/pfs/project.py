"""Создание проекта, состояние шагов, продолжение после перерыва."""
from __future__ import annotations

import re
from pathlib import Path

from . import core, i18n
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

# PRO-57: EN-бриф для проектов с project.json → lang=en (`pfs new --lang en`)
BRIEF_TEMPLATE_EN = """# Brief: {title}

> Filled in at the intake step. Fields with "?" are open questions to the product leader.

| Field | Value |
|---|---|
| Verbatim request | {question} |
| Refined question | ? |
| Decision to be made from this work | ? |
| Goal and success criterion | ? |
| Recipient of the result and format | ? |
| Constraints (deadline, budget, regulation, brand) | ? |
| Available data and materials | ? |
| Permitted sources | open sources + materials provided by the user |
| What is out of scope | ? |
| Deadline | ? |
"""


# PRO-52: сырой запрос больше не доезжает до title в неизменном виде. Markdown-разметка
# («**проекта**», «[cvstart.org](http://cvstart.org)») вычищается, типовые падежные огрехи
# («вывести проекта» вместо «вывести проект») исправляются по списку глаголов, управляющих
# винительным падежом. Исходный запрос при этом хранится дословно: project.json → question
# и строка «Исходный запрос (дословно)» в 00_brief.md — правку формулировки фиксирует intake.
_MD_NOISE = [
    (re.compile(r"\[([^\]]+)\]\([^)]*\)"), r"\1"),  # [текст](url) → текст
    (re.compile(r"\*\*([^*]+)\*\*"), r"\1"),        # **жирный** → текст
    (re.compile(r"`([^`]+)`"), r"\1"),              # `код` → текст
]
_ACC_VERBS = ("вывести", "запустить", "выпустить", "продвинуть", "масштабировать", "создать",
              "собрать", "найти", "проверить", "оценить", "улучшить", "увеличить", "повысить",
              "показать", "построить")
_CASE_SLIP = re.compile(rf"\b({'|'.join(_ACC_VERBS)})\s+проекта\b", re.IGNORECASE)


def normalize_title(title: str) -> str:
    """Название проекта: без markdown, лишних пробелов и типовых падежных огрехей."""
    t = title or ""
    for pat, repl in _MD_NOISE:
        t = pat.sub(repl, t)
    t = _CASE_SLIP.sub(r"\1 проект", t)
    t = re.sub(r"\s+", " ", t).strip()
    return (t[:1].upper() + t[1:]) if t else t


def create(title: str, question: str, slug: str | None = None, owner_role: str = "руководитель продукта",
           lang: str = "ru") -> Path:
    lang = lang if lang in i18n.LANGS else "ru"
    title = normalize_title(title)
    slug = slug or core.slugify(title)
    pdir = core.projects_dir() / slug
    if (pdir / "project.json").exists():
        tr = lambda key, **kw: i18n.t(lang, key, **kw)
        raise PfsError(tr("err_project_exists", slug=slug))
    for sub in ("sources/raw", "outputs", "interviews/real", "interviews/synthetic", "analysis"):
        (pdir / sub).mkdir(parents=True, exist_ok=True)
    core.write_json(pdir / "project.json", {
        "slug": slug, "title": title, "question": question, "owner_role": owner_role, "lang": lang,
        "created": core.now(),
        "allowed_sources": {"domains": [], "deny_domains": [], "note": "пусто = любые открытые источники"},
        "stale_after_days": 180,
    })
    next_intake = ("Уточнить запрос: вопрос, решение, получатель, ограничения, данные (шаг intake)"
                   if lang == "ru" else
                   "Clarify the request: question, decision, recipient, constraints, data (intake step)")
    core.write_json(pdir / "state.json", {
        "stage": "intake",
        "steps": {sid: {"status": "pending"} for sid in STAGE_IDS},
        "next_action": next_intake,
        "open_questions": [], "awaiting_human": None, "updated": core.now(),
    })
    tpl = BRIEF_TEMPLATE if lang == "ru" else BRIEF_TEMPLATE_EN
    core.atomic_write(pdir / "outputs" / OUTPUT_FILES["intake"], tpl.format(title=title, question=question))
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
    tr = lambda key, **kw: i18n.t(i18n.lang_of(pdir), key, **kw)
    if step not in STAGE_IDS:
        raise PfsError(tr("err_unknown_step", step=step, stages=", ".join(STAGE_IDS)))
    if status not in ("pending", "in_progress", "done", "skipped"):
        raise PfsError(tr("err_bad_status"))
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
    """Сводка для продолжения работы: где остановились и что делать дальше.
    Язык — от проекта (project.json → lang, PRO-57)."""
    from . import claims as claims_mod, cost as cost_mod
    tr = lambda key, **kw: i18n.t(i18n.lang_of(pdir), key, **kw)
    meta = core.read_json(pdir / "project.json", {})
    state = load_state(pdir)
    lines = [tr("status_project", title=meta.get("title"), slug=meta.get("slug")),
             tr("status_question", question=meta.get("question"))]
    marks = {"done": "✔", "in_progress": "▶", "skipped": "–", "pending": "·"}
    bar = " ".join(f"{marks.get(state['steps'].get(s['id'], {}).get('status', 'pending'), '·')}{s['id']}"
                   for s in STAGES)
    lines.append(tr("status_steps", bar=bar))
    lines.append(tr("status_stage", stage=state.get("stage"), next=state.get("next_action")))
    if state.get("awaiting_human"):
        ah = state["awaiting_human"]
        opts = tr("status_options", options=" / ".join(ah["options"])) if ah.get("options") else ""
        lines.append(tr("status_awaiting", question=ah["question"], options=opts))
    if state.get("open_questions"):
        lines.append(tr("status_open_questions", items="; ".join(state["open_questions"][:6])))
    srcs = core.read_jsonl(pdir / "sources.jsonl")
    cl = claims_mod.load(pdir)
    active = [c for c in cl if c.get("status") == "active"]
    by_kind: dict[str, int] = {}
    for c in active:
        by_kind[c["kind"]] = by_kind.get(c["kind"], 0) + 1
    decs = core.read_jsonl(pdir / "decisions.jsonl")
    lines.append(tr("status_counts", sources=len(srcs), claims=len(active), by_kind=by_kind,
                    decisions=len(decs)))
    from . import export as export_mod, review as review_mod
    lines += export_mod.freshness_warnings(pdir)
    # PRO-27: вердикт review устарел после правок реестра; префикс — здесь, на месте вывода
    lines += [f"⚠ {w}" for w in review_mod.stale_warnings(pdir)]
    total = cost_mod.summary(pdir)
    if total.get("plan"):
        # PRO-62: $0.00 при миллионах токенов выглядит как ошибка учёта — показываем эквивалент
        lines.append(tr("status_cost_plan", usd=total["usd"], usd_eq=total["usd_equivalent"],
                        rub_eq=total["rub_equivalent"], tokens=f"{total['tokens']:,}".replace(",", " ")))
    else:
        lines.append(tr("status_cost", usd=total["usd"], rub=total["rub"],
                        tokens=f"{total['tokens']:,}".replace(",", " ")))
    if not brief:
        logs = core.read_jsonl(pdir / "log.jsonl")[-8:]
        if logs:
            lines.append(tr("status_recent"))
            lines += [f"  {r['ts'][:16]} [{r['kind']}] {r['msg'][:110]}" for r in logs]
        outs = sorted(p.name for p in (pdir / "outputs").glob("*.md"))
        lines.append(tr("status_documents", docs=", ".join(outs)))
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
    """«Что решать сейчас»: шаг, ожидания человека, обязательства, пересмотры, открытые вопросы.
    Язык — от проекта (project.json → lang, PRO-57)."""
    from . import decisions as decisions_mod
    tr = lambda key, **kw: i18n.t(i18n.lang_of(pdir), key, **kw)
    state = load_state(pdir)
    meta = core.read_json(pdir / "project.json", {})
    lang = i18n.lang_of(pdir)
    lines = [tr("next_header", title=meta.get("title"), slug=meta.get("slug"))]
    lines.append(tr("next_stage", stage=state.get("stage"), next=state.get("next_action")))
    if six_pager_due(pdir):
        # PRO-32: six-pager собирают на review — напоминаем первым пунктом, пока его нет.
        lines.append(tr("next_sixpager", spec=i18n.SIX_PAGER_SPEC[lang]))
    if state.get("awaiting_human"):
        ah = state["awaiting_human"]
        opts = f" ({' / '.join(ah['options'])})" if ah.get("options") else ""
        lines.append(tr("next_waiting", question=ah["question"], options=opts))
    due = decisions_mod.due(pdir)
    if due.get("overdue"):
        lines.append(tr("next_overdue", n=len(due["overdue"])))
        for o in due["overdue"][:3]:
            label = o.get("commitment") or o.get("text") or str(o) if isinstance(o, dict) else str(o)
            lines.append(f"  · {str(label)[:120]}")
    if due.get("stale_sources"):
        # PRO-28: источники в основаниях решений, не проверявшиеся дольше нормы, — с готовой командой
        lines.append(tr("next_stale_sources", days=due.get("stale_days", 180)))
        lines += ["  · " + decisions_mod.stale_source_line(s) for s in due["stale_sources"][:6]]
    if due.get("stale_grounds"):
        lines.append(tr("next_stale_grounds", n=len(due["stale_grounds"])))
    if due.get("review_now"):
        ids = [d.get("id", d) if isinstance(d, dict) else str(d) for d in due["review_now"]]
        lines.append(tr("next_review_now", ids=", ".join(map(str, ids[:3]))))
    if due.get("review_soon"):
        lines.append(tr("next_review_soon", items="; ".join(map(str, due["review_soon"][:3]))))
    oq = state.get("open_questions", [])
    if oq:
        lines.append(tr("next_open_questions", n=len(oq)))
        lines += ["  · " + q[:120] for q in oq[:3]]
    if len(lines) == 2:
        lines.append(tr("next_clear"))
    lines.append(tr("next_refresh"))
    return "\n".join(lines)


def list_projects() -> list[dict]:
    out = []
    for p in sorted(core.projects_dir().glob("*/project.json")):
        meta = core.read_json(p, {})
        st = core.read_json(p.parent / "state.json", {})
        out.append({"slug": meta.get("slug"), "title": meta.get("title"), "stage": st.get("stage")})
    return out
