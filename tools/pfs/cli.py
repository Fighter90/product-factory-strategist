"""Командная строка pfs. Все команды работают с активным проектом (projects/.active) или --project."""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

from . import (calc, check, claims, core, cost, data, decisions, docx, export, finish, gaps, impact,
               kb, models, participate, project, route, sources)
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
    cards = kb.cards_for(a.step)
    if cards:
        print("Карты шага: " + ", ".join(cards))


def cmd_next(a):
    print(project.next_text(_p(a)))


def cmd_questions(a):
    blocks = core.read_json(core.CONFIG / "question_blocks.json", {})
    key = a.block
    if key is None:
        print("Вопросные блоки по шагам:")
        for stage, items in blocks.items():
            if stage.startswith("_"):
                continue
            ids = ", ".join(b["id"] for b in items) if isinstance(items, list) else ""
            print(f"  {stage}: {ids}")
        print("Подсказка: pfs questions <шаг|id>")
        return
    rows = []
    for stage, items in blocks.items():
        if stage.startswith("_"):
            continue
        if stage == key:
            rows.extend((stage, b) for b in items)
        elif isinstance(items, list):
            rows.extend((stage, b) for b in items if b.get("id") == key)
    if not rows:
        keys = [k for k in blocks if not k.startswith("_")]
        raise core.PfsError(f"Блок не найден: {key}. Шаги: {', '.join(keys)}")
    for stage, b in rows:
        opts = " · ".join(
            f"{i + 1}) {o}" + (" ←рекомендуется" if i == b.get("recommended") else "")
            for i, o in enumerate(b.get("options", [])))
        print(f"[{stage}/{b['id']}] {b['q']}\n   {opts}\n   Зачем: {b.get('why', '')}\n")
    print("Задать руководителю: pfs ask \"<вопрос>\" --options \"A,B,C\"")


def cmd_ask(a):
    project.ask_human(_p(a), a.question, _split(a.options))
    print("Вопрос записан. Агент ждёт ответа руководителя (pfs answer \"…\").")


def cmd_answer(a):
    project.answer_human(_p(a), a.answer)
    print("Ответ записан.")


def cmd_question(a):
    project.add_open_question(_p(a), a.text, close=a.close)
    print("Открытый вопрос " + ("закрыт" if a.close else "добавлен"))


def cmd_gap(a):
    pdir = _p(a)
    if a.action == "list":
        print(gaps.list_text(pdir))
        return
    if a.num is None or not (a.claim or "").strip():
        raise core.PfsError("gap close: укажите номер пробела и --claim C### (список: pfs gap list)")
    print(gaps.close(pdir, a.num, a.claim, a.note or "")["message"])
    print("Сверка синхронности: pfs check")


def cmd_source(a):
    pdir = _p(a)
    if a.action == "add":
        # относительные пути резолвятся от каталога проекта, если файла там нет — от cwd (PRO-36)
        is_url = bool(a.target and re.match(r"^https?://", a.target))
        target = a.target if is_url else (str(core.resolve_input(a.target, pdir)) if a.target else None)
        text_file = str(core.resolve_input(a.text_file, pdir)) if a.text_file else None
        text = sources.assert_safe_local(Path(text_file)).read_text(encoding="utf-8") if text_file else None
        rec, new = sources.add(pdir, target, text=text, url=a.url, title=a.title, origin=a.origin or "public",
                               note=a.note, published=a.published, force=a.force)
        flag = f" ⚠ подозрительных фраз: {len(rec['injection_flags'])}" if rec.get("injection_flags") else ""
        print(f"{'Добавлен' if new else 'Уже есть (повтор пропущен)'}: {rec['id']} — {rec['title']} ({rec['chars']} зн.){flag}")
        if text_file or (not is_url and target):
            print(f"Файл: {Path(text_file or target).resolve()}")
    elif a.action == "fetch":
        rec, new, channel = sources.fetch(pdir, a.target, title=a.title, origin=a.origin,
                                          note=a.note, published=a.published, force=a.force)
        flag = f" ⚠ подозрительных фраз: {len(rec['injection_flags'])}" if rec.get("injection_flags") else ""
        via = sources.VIA_LABELS.get(channel, channel)
        print(f"{'Добавлен' if new else 'Уже есть (повтор пропущен)'}: {rec['id']} — {rec['title']} "
              f"({rec['chars']} зн.); канал: {via}; origin: {rec['origin']}{flag}")
    elif a.action == "list":
        for s in sources.load(pdir):
            print(f"{s['id']} [{s['origin']}/{s['kind']}] {s['title'][:70]} — {s.get('url') or s.get('path') or ''}")
    elif a.action == "show":
        print(sources.show(pdir, a.target, a.max_chars))
    elif a.action == "refresh":
        res = sources.refresh(pdir, a.target, a.max_chars)
        if not res["changed"]:
            print(f"{a.target}: не изменился")
            return
        old = res["old_chars"] if res["old_chars"] is not None else "?"
        print(f'{res["sid"]} обновлён: chars {old}→{res["new_chars"]} '
              f'(sha {res["old_sha8"]}→{res["new_sha8"]}), флагов-инъекций: {res["flags"]}')
        print("```")
        print(res["preview"])
        print("```")
        print(impact.impact_text(impact.impact(pdir, res["sid"])))


def cmd_claim(a):
    pdir = _p(a)
    if a.action == "add":
        c = claims.add(pdir, a.text, a.kind, _split(a.source), _split(a.derived_from), a.confidence, a.note, a.quote, grade=a.grade)
        print(f"{c['id']} [{claims.KIND_RU[c['kind']]}] записано")
    elif a.action == "add-batch":
        res = claims.add_batch(pdir, core.resolve_input(a.text, pdir))
        print(f"Батч: создано {len(res['created'])}, дубликаты пропущены {res['skipped']}")
        if res["created"]:
            print("Новые: " + ", ".join(res["created"]))
    elif a.action == "list":
        rows = [c for c in claims.load(pdir) if (a.all or c["status"] == "active") and (not a.kind or c["kind"] == a.kind)]
        print(claims.table(rows))
    elif a.action == "retract":
        claims.retract(pdir, a.id, a.reason)
        print(impact.impact_text(impact.impact(pdir, a.id)))
    elif a.action == "rebase":
        ids = [a.id] if a.id else [c["id"] for c in claims.load(pdir) if c["status"] == "active"]
        for cid in ids:
            ch = claims.rebase(pdir, cid)
            if ch:
                print(f"{cid}: {', '.join(ch)}")
    elif a.action == "supersede":
        new = claims.supersede(pdir, a.id, a.text, a.kind, _split(a.source) or None, a.confidence, a.reason or "",
                               _split(a.derived_from) if a.derived_from else None, grade=a.grade)
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
    elif a.action == "rebase":
        print(", ".join(decisions.rebase(pdir, a.id, a.note or "")) or "Основания актуальны")
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
    if a.window:
        print(f"Окно учёта: {cost.set_window(pdir, a.since, a.until)}")
    if a.transcript:
        s = cost.record_session(pdir, a.session or Path(a.transcript).stem, Path(a.transcript), a.since, a.until)
        mark = " (plan)" if any(t.get("plan") for t in s["models"].values()) else ""
        print(f"Сессия учтена{mark}: ${s['usd']:.4f}")
    elif a.session is not None:  # алиас --transcript с авто-детектом транскрипта в корне проекта (PRO-30)
        path = cost.find_transcript(pdir, a.session)
        s = cost.record_session(pdir, path.stem, path, a.since, a.until)
        mark = " (plan)" if any(t.get("plan") for t in s["models"].values()) else ""
        print(f"Транскрипт: {path.name}")
        print(f"Сессия учтена{mark}: ${s['usd']:.4f}")
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
    elif a.action == "cohort":
        text = data.cohort_text(data.cohort_retention(path, a.user, a.date, a.sheet))
        cmd = f"python3 -m tools.pfs data cohort {a.file} --user {a.user} --date {a.date}"
    elif a.action == "funnel":
        if not (a.steps or "").strip():
            raise core.PfsError("funnel: укажите шаги --steps шаг1,шаг2,шаг3")
        text = data.funnel_text(data.funnel(path, a.steps, a.user or "user_id", a.date, a.sheet))
        cmd = f"python3 -m tools.pfs data funnel {a.file} --steps {a.steps}"
        if a.user and a.user != "user_id":
            cmd += f" --user {a.user}"
        if a.date:
            cmd += f" --date {a.date}"
        if a.sheet:
            cmd += f" --sheet {a.sheet}"
    else:
        if not (a.col or "").strip():
            raise core.PfsError("stats: укажите столбец --col имя_столбца")
        text = data.stats_text(data.stats(path, a.col, a.group, a.sheet))
        cmd = f"python3 -m tools.pfs data stats {a.file} --col {a.col}"
        if a.group:
            cmd += f" --group {a.group}"
        if a.sheet:
            cmd += f" --sheet {a.sheet}"
    print(text)
    if pdir and a.save:
        print(f"Сохранено: {data.save_analysis(pdir, a.save, text, cmd)}")


def cmd_interview(a):
    pdir = _p(a)
    if a.action == "guide":
        if not (a.topic or "").strip():
            raise core.PfsError("interview guide: укажите тему --topic")
        print(f"Гайд: {participate.guide(pdir, a.persona, a.topic)}")
    else:
        if not a.file:
            raise core.PfsError("interview save: укажите файл транскрипта/выжимки")
        rec = participate.save_synthetic(pdir, Path(a.file), a.persona, a.title)
        print(f'{rec["id"]} [синтетика] зарегистрирован — только гипотезы '
              "(facts на синтетике инструмент не примет)")


def cmd_media(a):
    pdir = _p(a)
    path = core.resolve_input(a.file, pdir)
    rec = participate.media(pdir, path, a.desc, a.title, a.origin)
    print(f'{rec["id"]} [{rec["kind"]}] зарегистрирован: raw-файл и описание добавлены')
    print(f"Файл: {path.resolve()}")


def cmd_ux(a):
    pdir = _p(a)
    path = participate.ux_scaffold(pdir, a.source_id, a.focus or "")
    print(f"Каркас разбора: {path} (выводы — только по материалу {a.source_id})")


def cmd_route(a):
    pdir = core.project_dir(a.project) if core.active_slug() or a.project else None
    req = a.request or (core.read_json(pdir / "project.json", {}).get("question") if pdir else "")
    res = route.route(req, a.override, a.economy, pdir)
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return
    print(route.route_text(res))
    print("Карты по шагам:")
    for stage in kb.STAGE_CARDS:
        print(f"  {stage}: {', '.join(kb.cards_for(stage))}")


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
    pdir = _p(a)
    for w in export.freshness_warnings(pdir):  # снимок сравнивается ДО сборки: предыдущий отчёт устарел
        print(w)
    if a.deck:
        print(f"Дека: {export.build_deck(_p(a))}")
        return
    if a.six_pager:
        print(f"Six-pager: {export.build_six_pager(pdir, with_calcs=not a.no_calcs)}")
        if a.en:  # EN-каркас в одном вызове: те же структура/числа/теги, скелет на английском
            print(f"Six-pager EN: {export.build_six_pager(pdir, with_calcs=not a.no_calcs, lang='en')}")
    else:
        print(f"Отчёт: {export.build(pdir)}")
    export.save_state(pdir)  # реестр попадает в REPORT/SIX_PAGER — фиксируем снимок после сборки


def cmd_calc(a):
    if a.which == "scaffold":
        _, found, total = calc.scaffold(_p(a))
        print(f"Каркас calcs.json: {found}/{total} чисел найдено в 02/04/06/07; "
              f"null-поля допишите вручную, затем pfs calc all")
        return
    for p in calc.run(_p(a), a.which):
        print(f"Excel-приложение: {p}")


def cmd_docx(a):
    pdir = core.project_dir(a.project) if (core.active_slug() or a.project) else None
    src = core.resolve_input(a.file, pdir)
    if not src.exists():
        raise core.PfsError(f"Файл не найден: {src.resolve()}")
    out = docx.convert(src, Path(a.out) if a.out else None)
    print(f"DOCX: {out.resolve()}")


def cmd_finish(a):
    pdir = _p(a)
    res = finish.run(pdir, no_deck=a.no_deck, en=a.en)
    for w in res["stale_warnings"]:  # несвежие основания ДО сборки — свежая сборка их сняла
        print(w)
    print(check.report_text(res["check"]))
    print(finish.summary_text(res))


def cmd_doctor(a):
    ok = sys.version_info >= (3, 9)
    print(f"Python {sys.version.split()[0]}: {'ok' if ok else 'нужен 3.9+'}")
    print(f"pdftotext: {'есть' if shutil.which('pdftotext') else 'нет (PDF: pip install pypdf или brew install poppler)'}")
    try:
        import pypdf  # type: ignore  # noqa: F401
        print("pypdf: есть")
    except ImportError:
        print("pypdf: нет (необязательно)")
    projects = project.list_projects()
    print(f"Карт в базе знаний: {len(kb.cards())}; проектов: {len(projects)}; активный: {core.active_slug()}")
    print(f"Профиль моделей: {models.load().get('active_profile')}")
    problems = 0
    for meta in projects:
        issues = sources.audit(core.projects_dir() / meta["slug"])
        if issues:
            problems += len(issues)
            print(f"⚠ Реестр источников [{meta['slug']}]:")
            for i in issues:
                print(f"  - {i}")
    if problems:
        print(f"Реестры источников: проблем {problems} — записи без файла пересоздайте (pfs source add), "
              "файлы-сироты и дубли ID/URL разберите вручную (см. выше)")
    else:
        print(f"Реестры источников: ok ({len(projects)} проектов)")


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
    s = sp.add_parser("gap", help="пробелы исследования: list / close"); s.add_argument("action", choices=["list", "close"])
    s.add_argument("num", nargs="?", type=int, help="номер пробела (pfs gap list)")
    s.add_argument("--claim", help="утверждение C###, закрывающее пробел")
    s.add_argument("--note", help="чем закрыт: короткое пояснение")
    s.set_defaults(f=cmd_gap)

    s = sp.add_parser("source", help="источники (add/fetch/list/show/refresh)")
    s.add_argument("action", choices=["add", "fetch", "list", "show", "refresh"],
                   help="fetch — недоступный URL (403/SSL/JS/таймаут): прямой запрос → r.jina.ai → web.archive.org; "
                        "полный фейл — предложение --text-file")
    s.add_argument("target", nargs="?",
                   help="URL или файл; относительный путь: сначала каталог проекта, затем cwd")
    s.add_argument("--text-file", help="файл с текстом выписки (путь: каталог проекта → cwd)")
    s.add_argument("--url"); s.add_argument("--title")
    s.add_argument("--origin", help="public | excerpt (выписка, первоисточник недоступен) | own | interview | synthetic | agent; "
                                    "для fetch по умолчанию: public при прямом успехе, excerpt при фолбэке (reader/архив)")
    s.add_argument("--note"); s.add_argument("--published"); s.add_argument("--force", action="store_true")
    s.add_argument("--max-chars", type=int, default=4000, help="лимит знаков превью (show/refresh)")
    s.set_defaults(f=cmd_source)

    s = sp.add_parser("claim", help="утверждения")
    s.add_argument("action", choices=["add", "add-batch", "list", "retract", "supersede", "rebase"],
                   help="add-batch — пачка из JSONL-файла (text/kind/source/grade/quote/from); "
                        "невалидная строка отменяет весь батч")
    s.add_argument("text", nargs="?"); s.add_argument("--id"); s.add_argument("--kind", choices=claims.KINDS)
    s.add_argument("--source"); s.add_argument("--from", dest="derived_from"); s.add_argument("--confidence", default="medium")
    s.add_argument("--note"); s.add_argument("--quote"); s.add_argument("--reason"); s.add_argument("--all", action="store_true")
    s.add_argument("--grade", choices=claims.GRADES, help="сила доказательства A–D")
    s.set_defaults(f=cmd_claim)

    s = sp.add_parser("check", help="контроль качества"); s.add_argument("--json", action="store_true")
    s.add_argument("--strict", action="store_true"); s.set_defaults(f=cmd_check)
    s = sp.add_parser("impact", help="что затронет изменение"); s.add_argument("id"); s.set_defaults(f=cmd_impact)

    s = sp.add_parser("decision", help="решения"); s.add_argument("action", choices=["add", "list", "due", "done", "status", "rebase"])
    s.add_argument("--id"); s.add_argument("--title"); s.add_argument("--decision"); s.add_argument("--owner"); s.add_argument("--grounds")
    s.add_argument("--option"); s.add_argument("--rejected"); s.add_argument("--metric", action="append")
    s.add_argument("--review"); s.add_argument("--trigger", action="append"); s.add_argument("--commit", action="append")
    s.add_argument("--commitment"); s.add_argument("--status"); s.add_argument("--note"); s.add_argument("--on")
    s.set_defaults(f=cmd_decision)

    s = sp.add_parser("log", help="запись в журнал / ручная стоимость"); s.add_argument("message")
    s.add_argument("--kind", default="action"); s.add_argument("--step"); s.add_argument("--usd", type=float, default=0.0)
    s.add_argument("--human-minutes", type=float, default=0.0); s.set_defaults(f=cmd_log)
    s = sp.add_parser("cost", help="стоимость"); s.add_argument("--transcript", help="транскрипт Claude Code (jsonl) или сессия OpenCode (session.json)")
    s.add_argument("--session", nargs="?", const="", default=None,
                   help="ID сессии (при --transcript) или транскрипт: путь/часть имени "
                        "(*_session.json / *.jsonl в корне проекта; без --transcript — алиас с авто-детектом, "
                        "без значения — самый свежий)")
    s.add_argument("--since", help="ISO-время начала задачи (UTC), учитывать сообщения после него")
    s.add_argument("--until", help="ISO-время окончания задачи (UTC)")
    s.add_argument("--window", action="store_true", help="сохранить --since/--until в project.json (хук Stop будет их соблюдать)")
    s.set_defaults(f=cmd_cost)

    s = sp.add_parser("kb", help="база знаний"); s.add_argument("action", choices=["search", "index", "show"]); s.add_argument("query", nargs="?")
    s.add_argument("-k", type=int, default=8); s.add_argument("--with-project", action="store_true"); s.set_defaults(f=cmd_kb)

    s = sp.add_parser("data", help="анализ таблиц (profile/cohort/funnel/stats)")
    s.add_argument("action", choices=["profile", "cohort", "funnel", "stats"],
                   help="profile — паспорт таблицы; cohort — удержание; funnel — воронка; stats — статистика столбца")
    s.add_argument("file")
    s.add_argument("--sheet", help="лист Excel")
    s.add_argument("--user", help="столбец пользователя (cohort/funnel)")
    s.add_argument("--date", help="столбец даты (cohort/funnel)")
    s.add_argument("--steps", help="шаги воронки через запятую: visit,signup,pay")
    s.add_argument("--col", help="числовой столбец для stats")
    s.add_argument("--group", help="столбец группировки для stats")
    s.add_argument("--save", help="имя файла в analysis/")
    s.set_defaults(f=cmd_data)

    s = sp.add_parser("interview", help="гайд интервью и синтетические респонденты")
    s.add_argument("action", choices=["guide", "save"],
                   help="guide — каркас вопросов; save — транскрипт ИИ-респондента как источник")
    s.add_argument("file", nargs="?", help="файл транскрипта/выжимки (для save)")
    s.add_argument("--persona", required=True, help="персона ИИ-респондента, напр. «Родитель 7–12»")
    s.add_argument("--topic", help="тема интервью (для guide)")
    s.add_argument("--title", help="заголовок источника (для save)")
    s.set_defaults(f=cmd_interview)

    s = sp.add_parser("media", help="медиа-файл как источник: raw-копия + описание")
    s.add_argument("action", choices=["add"], help="add — зарегистрировать")
    s.add_argument("file", help="путь к изображению/аудио/видео (относительный: каталог проекта → cwd)")
    s.add_argument("--desc", required=True, help="что видно/слышимо, без домыслов")
    s.add_argument("--title", help="заголовок источника")
    s.add_argument("--origin", default="own", help="public | own | interview | synthetic | agent")
    s.set_defaults(f=cmd_media)

    s = sp.add_parser("ux", help="каркас UX-разбора источника")
    s.add_argument("action", choices=["scaffold"], help="scaffold — создать analysis/ux_<S###>.md")
    s.add_argument("source_id", help="S### — источник с материалом разбора")
    s.add_argument("--focus", help="фокус разбора, напр. «онбординг»")
    s.set_defaults(f=cmd_ux)

    s = sp.add_parser("route", help="выбор сценария и моделей"); s.add_argument("request", nargs="?")
    s.add_argument("--override"); s.add_argument("--economy", action="store_true"); s.add_argument("--json", action="store_true")
    s.set_defaults(f=cmd_route)
    s = sp.add_parser("models", help="модели под задачи"); s.add_argument("action", choices=["show", "pick", "escalate", "use", "sync"], nargs="?", default="show")
    s.add_argument("task", nargs="?"); s.add_argument("--economy", action="store_true"); s.add_argument("--critical", action="store_true")
    s.add_argument("--reason"); s.set_defaults(f=cmd_models)

    s = sp.add_parser("export", help="собрать REPORT.md, SIX_PAGER.md или deck.html")
    s.add_argument("--deck", action="store_true", help="HTML-дека 16:9 из SIX_PAGER.md")
    s.add_argument("--six-pager", action="store_true", help="six-pager FAQ-1…6 + Excel-приложения")
    s.add_argument("--en", action="store_true",
                   help="вместе с --six-pager собрать EN-каркас (SIX_PAGER_EN.md): скелет на английском, "
                        "секции из документов — с пометкой «[RU source — translate]»")
    s.add_argument("--no-calcs", action="store_true", help="не перегенерировать Excel")
    s.set_defaults(f=cmd_export)
    s = sp.add_parser("calc", help="Excel-приложения: юнит-экономика, модель роста, когорты, рынок")
    s.add_argument("which", nargs="?", default="all",
                   choices=["all", "unit-econ", "growth", "cohort", "market", "scaffold"],
                   help="scaffold — каркас calcs.json из 02/04/06/07 (null — дописать вручную)")
    s.set_defaults(f=cmd_calc)
    s = sp.add_parser("docx", help="Markdown → DOCX (без зависимостей)")
    s.add_argument("file", help=".md файл (относительный путь: каталог проекта → cwd)"); s.add_argument("--out")
    s.set_defaults(f=cmd_docx)
    s = sp.add_parser("next", help="что решать сейчас: шаг, обязательства, пересмотры, открытые вопросы")
    s.set_defaults(f=cmd_next)
    s = sp.add_parser("questions", help="вопросные блоки шага (настраиваемость стратегии)")
    s.add_argument("block", nargs="?", default=None, help="шаг или id блока, напр. options-criteria; без аргумента — обзор всех шагов")
    s.set_defaults(f=cmd_questions)
    s = sp.add_parser("finish", help="собрать финальный пакет одной цепочкой: Excel → REPORT → six-pager → DOCX → deck")
    s.add_argument("--no-deck", action="store_true", help="не собирать HTML-деку")
    s.add_argument("--en", action="store_true", help="дополнительно EN-черновик six-pager (SIX_PAGER_EN.md + DOCX)")
    s.set_defaults(f=cmd_finish)
    sp.add_parser("doctor", help="проверка окружения и реестров источников").set_defaults(f=cmd_doctor)
    return ap


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        args.f(args)
    except PfsError as exc:
        print(f"Ошибка: {exc}", file=sys.stderr)
        return 2
    return 0
