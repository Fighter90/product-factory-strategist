"""Командная строка pfs. Все команды работают с активным проектом (projects/.active) или --project."""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from . import (check, claims, core, cost, data, decisions, export, impact, kb, models, project, route, sources)
from .core import PfsError


def _p(args) -> Path:
    return core.project_dir(getattr(args, "project", None))


def _split(v: str | None) -> list[str]:
    return [x.strip() for x in (v or "").split(",") if x.strip()]


def cmd_new(a):
    pdir = project.create(a.title, a.question, a.slug)
    print(f"Создан проект {pdir.name}. Следующий шаг: intake — уточнить запрос (см. AGENTS.md).")


def cmd_use(a):
    core.project_dir(a.slug)
    core.set_active(a.slug)
    print(project.status_text(core.project_dir(a.slug)))


def cmd_list(a):
    for p in project.list_projects():
        mark = "*" if p["slug"] == core.active_slug() else " "
        print(f"{mark} {p['slug']:<40} шаг: {p['stage']:<12} {p['title']}")


def cmd_status(a):
    print(project.status_text(_p(a), brief=a.brief))


def cmd_step(a):
    st = project.set_step(_p(a), a.step, a.status, a.note, a.next)
    print(f"Шаг {a.step} → {a.status}. Текущий: {st['stage']}. Далее: {st.get('next_action')}")


def cmd_ask(a):
    project.ask_human(_p(a), a.question, _split(a.options))
    print("Вопрос записан. Агент ждёт ответа руководителя (pfs answer \"…\").")


def cmd_answer(a):
    project.answer_human(_p(a), a.answer)
    print("Ответ записан.")


def cmd_question(a):
    project.add_open_question(_p(a), a.text, close=a.close)
    print("Открытый вопрос " + ("закрыт" if a.close else "добавлен"))


def cmd_source(a):
    pdir = _p(a)
    if a.action == "add":
        text = sources.assert_safe_local(Path(a.text_file)).read_text(encoding="utf-8") if a.text_file else None
        rec, new = sources.add(pdir, a.target, text=text, url=a.url, title=a.title, origin=a.origin,
                               note=a.note, published=a.published, force=a.force)
        flag = f" ⚠ подозрительных фраз: {len(rec['injection_flags'])}" if rec.get("injection_flags") else ""
        print(f"{'Добавлен' if new else 'Уже есть (повтор пропущен)'}: {rec['id']} — {rec['title']} ({rec['chars']} зн.){flag}")
    elif a.action == "list":
        for s in sources.load(pdir):
            print(f"{s['id']} [{s['origin']}/{s['kind']}] {s['title'][:70]} — {s.get('url') or s.get('path') or ''}")
    elif a.action == "show":
        print(sources.show(pdir, a.target, a.max_chars))


def cmd_claim(a):
    pdir = _p(a)
    if a.action == "add":
        c = claims.add(pdir, a.text, a.kind, _split(a.source), _split(a.derived_from), a.confidence, a.note, a.quote, grade=a.grade)
        print(f"{c['id']} [{claims.KIND_RU[c['kind']]}] записано")
    elif a.action == "list":
        rows = [c for c in claims.load(pdir) if (a.all or c["status"] == "active") and (not a.kind or c["kind"] == a.kind)]
        print(claims.table(rows))
    elif a.action == "retract":
        claims.retract(pdir, a.id, a.reason)
        print(impact.impact_text(impact.impact(pdir, a.id)))
    elif a.action == "supersede":
        new = claims.supersede(pdir, a.id, a.text, a.kind, _split(a.source) or None, a.confidence, a.reason or "",
                               _split(a.derived_from) if a.derived_from else None)
        print(f"{a.id} замещено {new['id']}")
        print(impact.impact_text(impact.impact(pdir, a.id)))


def cmd_check(a):
    res = check.run(_p(a))
    print(json.dumps(res, ensure_ascii=False, indent=2) if a.json else check.report_text(res))
    if a.strict and res["errors"]:
        sys.exit(1)


def cmd_impact(a):
    print(impact.impact_text(impact.impact(_p(a), a.id)))


def cmd_decision(a):
    pdir = _p(a)
    if a.action == "add":
        d = decisions.add(pdir, a.title, a.decision, a.owner, _split(a.grounds), a.option, a.metric, a.review,
                          a.trigger, a.commit, _split(a.rejected))
        print(f"{d['id']} записано")
    elif a.action == "list":
        print(decisions.table(decisions.load(pdir)))
    elif a.action == "due":
        print(decisions.due_text(decisions.due(pdir, a.on)))
    elif a.action == "done":
        decisions.update_commitment(pdir, a.id, a.commitment, "done", a.note)
        print("Обязательство выполнено")
    elif a.action == "status":
        decisions.set_status(pdir, a.id, a.status, a.note or "")
        print("Статус решения обновлён")


def cmd_log(a):
    pdir = _p(a)
    if a.usd or a.human_minutes:
        cost.add_manual(pdir, a.message, a.usd, a.human_minutes)
    else:
        core.log(pdir, a.kind, a.message, step=a.step)
    print("Записано в журнал")


def cmd_cost(a):
    pdir = _p(a)
    if a.transcript:
        s = cost.record_session(pdir, a.session or Path(a.transcript).stem, Path(a.transcript), a.since)
        print(f"Сессия учтена: ${s['usd']:.4f}")
    print(cost.summary_text(pdir))


def cmd_kb(a):
    if a.action == "search":
        pdir = core.project_dir(a.project) if (a.with_project and core.active_slug()) else None
        for r in kb.search(a.query, pdir, a.k):
            print(f"{r['score']:>6}  {r['id']} › {r['section']}  ({r['path']})\n        {r['snippet']}")
    elif a.action == "index":
        _, problems = kb.build_index()
        print(f"knowledge/INDEX.md обновлён; карт: {len(kb.cards())}; битых связей: {len(problems)}")
        for p in problems[:30]:
            print("  - " + p)
    elif a.action == "show":
        print(kb.card_path(a.query).read_text(encoding="utf-8"))


def cmd_data(a):
    pdir = _p(a) if core.active_slug() or a.project else None
    path = Path(a.file)
    if a.action == "profile":
        text = data.profile_text(data.profile(path, a.sheet))
        cmd = f"python3 -m tools.pfs data profile {a.file}" + (f" --sheet {a.sheet}" if a.sheet else "")
    else:
        text = data.cohort_text(data.cohort_retention(path, a.user, a.date, a.sheet))
        cmd = f"python3 -m tools.pfs data cohort {a.file} --user {a.user} --date {a.date}"
    print(text)
    if pdir and a.save:
        print(f"Сохранено: {data.save_analysis(pdir, a.save, text, cmd)}")


def cmd_route(a):
    pdir = core.project_dir(a.project) if core.active_slug() or a.project else None
    req = a.request or (core.read_json(pdir / "project.json", {}).get("question") if pdir else "")
    res = route.route(req, a.override, a.economy, pdir)
    print(json.dumps(res, ensure_ascii=False, indent=2) if a.json else route.route_text(res))


def cmd_models(a):
    if a.action == "show":
        print(models.table())
    elif a.action == "pick":
        print(json.dumps(models.pick(a.task, economy=a.economy, critical=a.critical), ensure_ascii=False, indent=2))
    elif a.action == "escalate":
        pdir = core.project_dir(a.project) if core.active_slug() else None
        print(json.dumps(models.escalate(pdir, a.task, a.reason or "повторная ошибка проверки"), ensure_ascii=False, indent=2))
    elif a.action == "use":
        models.use_profile(a.task)
        print(f"Активный профиль: {a.task}. Синхронизация субагентов: {models.sync_agents() or 'без изменений'}")
    elif a.action == "sync":
        print(models.sync_agents() or "Модели субагентов уже соответствуют config/models.json")


def cmd_export(a):
    print(f"Отчёт: {export.build(_p(a))}")


def cmd_doctor(a):
    ok = sys.version_info >= (3, 9)
    print(f"Python {sys.version.split()[0]}: {'ok' if ok else 'нужен 3.9+'}")
    print(f"pdftotext: {'есть' if shutil.which('pdftotext') else 'нет (PDF: pip install pypdf или brew install poppler)'}")
    try:
        import pypdf  # type: ignore  # noqa: F401
        print("pypdf: есть")
    except ImportError:
        print("pypdf: нет (необязательно)")
    print(f"Карт в базе знаний: {len(kb.cards())}; проектов: {len(project.list_projects())}; активный: {core.active_slug()}")
    print(f"Профиль моделей: {models.load().get('active_profile')}")


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="pfs", description="Инструменты агента «Стратег Фабрики продуктов»")
    ap.add_argument("--project", help="slug проекта (по умолчанию активный)")
    sp = ap.add_subparsers(dest="cmd", required=True)

    s = sp.add_parser("new", help="создать проект"); s.add_argument("title"); s.add_argument("question"); s.add_argument("--slug"); s.set_defaults(f=cmd_new)
    s = sp.add_parser("use", help="сделать проект активным"); s.add_argument("slug"); s.set_defaults(f=cmd_use)
    sp.add_parser("list", help="список проектов").set_defaults(f=cmd_list)
    s = sp.add_parser("status", help="где остановились"); s.add_argument("--brief", action="store_true"); s.set_defaults(f=cmd_status)
    s = sp.add_parser("step", help="отметить шаг"); s.add_argument("step"); s.add_argument("status")
    s.add_argument("--note"); s.add_argument("--next", help="следующее действие"); s.set_defaults(f=cmd_step)
    s = sp.add_parser("ask", help="вопрос руководителю (пауза)"); s.add_argument("question"); s.add_argument("--options"); s.set_defaults(f=cmd_ask)
    s = sp.add_parser("answer", help="ответ руководителя"); s.add_argument("answer"); s.set_defaults(f=cmd_answer)
    s = sp.add_parser("question", help="открытый вопрос/пробел"); s.add_argument("text"); s.add_argument("--close", action="store_true"); s.set_defaults(f=cmd_question)

    s = sp.add_parser("source", help="источники"); s.add_argument("action", choices=["add", "list", "show"]); s.add_argument("target", nargs="?")
    s.add_argument("--text-file"); s.add_argument("--url"); s.add_argument("--title"); s.add_argument("--origin", default="public")
    s.add_argument("--note"); s.add_argument("--published"); s.add_argument("--force", action="store_true")
    s.add_argument("--max-chars", type=int, default=4000); s.set_defaults(f=cmd_source)

    s = sp.add_parser("claim", help="утверждения"); s.add_argument("action", choices=["add", "list", "retract", "supersede"])
    s.add_argument("text", nargs="?"); s.add_argument("--id"); s.add_argument("--kind", choices=claims.KINDS)
    s.add_argument("--source"); s.add_argument("--from", dest="derived_from"); s.add_argument("--confidence", default="medium")
    s.add_argument("--note"); s.add_argument("--quote"); s.add_argument("--reason"); s.add_argument("--all", action="store_true")
    s.add_argument("--grade", choices=claims.GRADES, help="сила доказательства A–D")
    s.set_defaults(f=cmd_claim)

    s = sp.add_parser("check", help="контроль качества"); s.add_argument("--json", action="store_true")
    s.add_argument("--strict", action="store_true"); s.set_defaults(f=cmd_check)
    s = sp.add_parser("impact", help="что затронет изменение"); s.add_argument("id"); s.set_defaults(f=cmd_impact)

    s = sp.add_parser("decision", help="решения"); s.add_argument("action", choices=["add", "list", "due", "done", "status"])
    s.add_argument("--id"); s.add_argument("--title"); s.add_argument("--decision"); s.add_argument("--owner"); s.add_argument("--grounds")
    s.add_argument("--option"); s.add_argument("--rejected"); s.add_argument("--metric", action="append")
    s.add_argument("--review"); s.add_argument("--trigger", action="append"); s.add_argument("--commit", action="append")
    s.add_argument("--commitment"); s.add_argument("--status"); s.add_argument("--note"); s.add_argument("--on")
    s.set_defaults(f=cmd_decision)

    s = sp.add_parser("log", help="запись в журнал / ручная стоимость"); s.add_argument("message")
    s.add_argument("--kind", default="action"); s.add_argument("--step"); s.add_argument("--usd", type=float, default=0.0)
    s.add_argument("--human-minutes", type=float, default=0.0); s.set_defaults(f=cmd_log)
    s = sp.add_parser("cost", help="стоимость"); s.add_argument("--transcript"); s.add_argument("--session")
    s.add_argument("--since", help="ISO-время начала задачи (UTC), учитывать сообщения после него"); s.set_defaults(f=cmd_cost)

    s = sp.add_parser("kb", help="база знаний"); s.add_argument("action", choices=["search", "index", "show"]); s.add_argument("query", nargs="?")
    s.add_argument("-k", type=int, default=8); s.add_argument("--with-project", action="store_true"); s.set_defaults(f=cmd_kb)

    s = sp.add_parser("data", help="анализ таблиц"); s.add_argument("action", choices=["profile", "cohort"]); s.add_argument("file")
    s.add_argument("--sheet"); s.add_argument("--user"); s.add_argument("--date"); s.add_argument("--save", help="имя файла в analysis/")
    s.set_defaults(f=cmd_data)

    s = sp.add_parser("route", help="выбор сценария и моделей"); s.add_argument("request", nargs="?")
    s.add_argument("--override"); s.add_argument("--economy", action="store_true"); s.add_argument("--json", action="store_true")
    s.set_defaults(f=cmd_route)
    s = sp.add_parser("models", help="модели под задачи"); s.add_argument("action", choices=["show", "pick", "escalate", "use", "sync"], nargs="?", default="show")
    s.add_argument("task", nargs="?"); s.add_argument("--economy", action="store_true"); s.add_argument("--critical", action="store_true")
    s.add_argument("--reason"); s.set_defaults(f=cmd_models)

    sp.add_parser("export", help="собрать REPORT.md").set_defaults(f=cmd_export)
    sp.add_parser("doctor", help="проверка окружения").set_defaults(f=cmd_doctor)
    return ap


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        args.f(args)
    except PfsError as exc:
        print(f"Ошибка: {exc}", file=sys.stderr)
        return 2
    return 0
