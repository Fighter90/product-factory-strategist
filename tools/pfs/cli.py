"""Командная строка pfs. Все команды работают с активным проектом (projects/.active) или --project."""
from __future__ import annotations

import argparse
import importlib.metadata
import json
import os
import re
import shutil
import sys
from pathlib import Path

from . import (ab, calc, check, claims, core, cost, data, decisions, docx, export, finish, gaps, i18n, impact,
               kb, models, participate, project, review, route, sources)
from .core import PfsError


def _p(args) -> Path:
    return core.project_dir(getattr(args, "project", None))


def _p_or_hint(args) -> Path | None:
    """Каталог проекта для status/next: без проекта — подсказка вместо ошибки (PRO-67).

    На чистом клоне указателя нет вовсе, а в старых клонах лежит закоммиченный
    битый .active — оба случая не ошибка: печатаем доступные проекты и как
    начать, битый указатель сбрасываем. Явный --project с ошибкой остаётся ошибкой.
    """
    explicit = getattr(args, "project", None)
    if explicit:
        return core.project_dir(explicit)
    try:
        return core.project_dir(None)
    except core.PfsError:
        stale = core.active_slug()
        if stale:
            core.clear_active()
        available = ", ".join(p["slug"] for p in project.list_projects()) or "нет"
        stale_note = f" ({stale})" if stale else ""
        print(f"Активный проект не найден{stale_note}, доступные: {available}.")
        print("Создайте новый: pfs new \"<название>\" \"<запрос>\" или выберите: pfs use <slug>")
        return None


def _split(v: str | None) -> list[str]:
    return [x.strip() for x in (v or "").split(",") if x.strip()]


def cmd_new(a):
    pdir = project.create(a.title, a.question, a.slug, lang=getattr(a, "lang", "ru"))
    lang = i18n.lang_of(pdir)
    print(i18n.t(lang, "new_created", slug=pdir.name, agents=i18n.pointers(lang)["agents"]))


def cmd_lang(a):
    """Показать/переключить язык проекта (PRO-57): pfs lang | pfs lang en [--project slug]."""
    pdir = _p(a)
    if getattr(a, "value", None):
        meta = core.read_json(pdir / "project.json", {})
        old = meta.get("lang", "ru")
        meta["lang"] = a.value
        core.write_json(pdir / "project.json", meta)
        print(i18n.t(a.value, "lang_set", lang=a.value, old=old, **i18n.pointers(a.value)))
        return
    lang = i18n.lang_of(pdir)
    print(i18n.t(lang, "lang_current", lang=lang, **i18n.pointers(lang)))


def cmd_use(a):
    core.project_dir(a.slug)
    core.set_active(a.slug)
    print(project.status_text(core.project_dir(a.slug)))


def cmd_list(a):
    for p in project.list_projects():
        mark = "*" if p["slug"] == core.active_slug() else " "
        print(f"{mark} {p['slug']:<40} шаг: {p['stage']:<12} {p['title']}")


def cmd_status(a):
    pdir = _p_or_hint(a)
    if pdir is None:
        return
    print(project.status_text(pdir, brief=a.brief))


def cmd_step(a):
    pdir = _p(a)
    st = project.set_step(pdir, a.step, a.status, a.note, a.next)
    lang = i18n.lang_of(pdir)
    print(i18n.t(lang, "step_marked", step=a.step, status=a.status, stage=st["stage"],
                 next=st.get("next_action")))
    cards = kb.cards_for(a.step)
    if cards:
        print(i18n.t(lang, "step_cards", cards=", ".join(cards)))


def cmd_next(a):
    pdir = _p_or_hint(a)
    if pdir is None:
        return
    print(project.next_text(pdir))


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
        text_path = core.resolve_input(a.text_file, pdir) if a.text_file else None
        text = sources.assert_safe_local(text_path).read_text(encoding="utf-8") if text_path else None
        rec, new = sources.add(pdir, target, text=text, url=a.url, title=a.title, origin=a.origin or "public",
                               note=a.note, published=a.published, force=a.force, text_path=text_path)
        flag = f" ⚠ подозрительных фраз: {len(rec['injection_flags'])}" if rec.get("injection_flags") else ""
        print(f"{'Добавлен' if new else 'Уже есть (повтор пропущен)'}: {rec['id']} — {rec['title']} ({rec['chars']} зн.){flag}")
        if rec.get("external_path"):
            print(f"⚠ Файл лежал вне проекта ({rec['external_path']}) — копия сохранена в {rec['path']}. "
                  "Материал должен быть явно передан пользователем.")
        if (text_path or (not is_url and target)) and rec.get("path"):
            print(f"Файл: {(pdir / rec['path']).resolve()}")  # копия в sources/raw/ — след в проекте (PRO-58)
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
        c = claims.add(pdir, a.text, a.kind, _split(a.source), _split(a.from_ref), a.confidence, a.note, a.quote, grade=a.grade)
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
    elif a.action == "retag":
        res = claims.retag(pdir, a.from_ref, a.to)
        print(f"Перенумерация тегов: [{res['from']}] → [{res['to']}] — файлов {res['files']}, вхождений {res['replacements']}")
        print("Сверка ссылок и реестра: pfs check · влияние: pfs impact " + res["to"])
    elif a.action == "supersede":
        new = claims.supersede(pdir, a.id, a.text, a.kind, _split(a.source) or None, a.confidence, a.reason or "",
                               _split(a.from_ref) if a.from_ref else None, grade=a.grade)
        print(f"{a.id} замещено {new['id']}")
        print(impact.impact_text(impact.impact(pdir, a.id)))


def cmd_check(a):
    pdir = _p(a)
    res = check.run(pdir)
    print(json.dumps(res, ensure_ascii=False, indent=2) if a.json else check.report_text(res, i18n.lang_of(pdir)))
    if a.strict and res["errors"]:
        sys.exit(1)


def cmd_review(a):
    snap = review.lock(_p(a))
    docs = sum(1 for sha in snap["documents"].values() if sha)
    print(f"Вердикт review зафиксирован: снимок реестра в outputs/{review.STATE} "
          f"(claims, sources, документов на месте: {docs}/8). Правки реестра после lock "
          "будут помечены «вердикт review устарел» в check/status/export — "
          "после повторной ревизии зафиксируйте снова: pfs review lock.")


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
    if getattr(a, "plan_month", None):
        cost.set_plan_tariff(pdir, a.plan_month)  # PRO-62: тариф подписки → доля подписки в отчёте
        print(f"Тариф подписки: ${a.plan_month:g}/мес")
    if a.window:
        print(f"Окно учёта: {cost.set_window(pdir, a.since, a.until)}")
    if a.transcript:
        s = cost.record_session(pdir, a.session or Path(a.transcript).stem, Path(a.transcript), a.since, a.until)
        print(_session_line(s))
    elif a.session is not None:  # алиас --transcript с авто-детектом транскрипта в корне проекта (PRO-30)
        path = cost.find_transcript(pdir, a.session)
        s = cost.record_session(pdir, path.stem, path, a.since, a.until)
        print(f"Транскрипт: {path.name}")
        print(_session_line(s))
    print(cost.summary_text(pdir, i18n.lang_of(pdir)))


def _session_line(s: dict) -> str:
    """«Сессия учтена…»: фактическая оплата; для план-сессий — и эквивалент по API-ценам,
    когда он отличается от факта (у обычных сессий он равен факту — хвост не дублируем) (PRO-62)."""
    mark = " (plan)" if any(t.get("plan") for t in s["models"].values()) else ""
    line = f"Сессия учтена{mark}: ${s['usd']:.4f}"
    if mark or s.get("usd_equivalent") != s.get("usd"):
        line += f" · эквивалент по API-ценам ${s['usd_equivalent']:.2f}"
    return line


def cmd_kb(a):
    if a.action == "search":
        pdir = core.project_dir(a.project) if (a.with_project and core.active_slug()) else None
        for r in kb.search(a.query, pdir, a.k):
            print(f"{r['score']:>6}  {r['id']} › {r['section']}  ({r['path']})\n        {r['snippet']}")
    elif a.action == "index":
        _, problems = kb.build_index()
        kb.build_index_en()
        print(f"knowledge/INDEX.md и knowledge/INDEX_EN.md обновлены; карт RU: {len(kb.cards())}; битых связей: {len(problems)}")
        for p in problems[:30]:
            print("  - " + p)
    elif a.action == "show":
        print(kb.card_path(a.query, lang=getattr(a, "lang", "ru")).read_text(encoding="utf-8"))
    elif a.action == "lint":
        problems = kb.lint()
        en = len(list(core.KNOWLEDGE.joinpath("methods_en").glob("*.md")))
        if problems:
            print(f"pfs kb lint: проблем: {len(problems)} (карт RU: {len(kb.cards())}, EN: {en})")
            for p in problems:
                print("  - " + p)
            sys.exit(1)
        print(f"pfs kb lint: OK — карт RU: {len(kb.cards())}, EN: {en}; проблем нет")


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


def cmd_ab(a):
    """Дизайн A/B-теста (PRO-71): документ по M-ab-test-design-template + чек-лист
    M-ab-test-checklist + контекст AI-ревьюера M-ai-experiment-review-context."""
    pdir = _p(a)
    lang = i18n.lang_of(pdir)
    res = ab.design(pdir, hypothesis=a.hypothesis, metric=a.metric, proxy=a.proxy, guardrail=a.guardrail,
                    baseline=a.baseline, mde=a.mde, alpha=a.alpha, power=a.power,
                    traffic=a.traffic, share=a.share, rules=a.rules, split_system=a.split_system)
    for key, label in (("design", "Дизайн A/B-теста (M-ab-test-design-template)"),
                       ("checklist", "Чек-лист запуска (M-ab-test-checklist)"),
                       ("ai_review", "Контекст AI-ревьюера (M-ai-experiment-review-context)")):
        print(f"{label}: {res[key]}")
    if not ab.claim_hypotheses(pdir):
        print(i18n.t(lang, "ab_no_hypothesis"))


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
    # снимки сравниваются ДО сборки; «⚠ » для review-пометки — на месте вывода
    for w in export.freshness_warnings(pdir) + [f"⚠ {w}" for w in review.stale_warnings(pdir)]:
        print(w)
    if a.deck:
        print(f"Дека: {export.build_deck(_p(a))}")
        return
    if a.six_pager:
        print(f"Six-pager: {export.build_six_pager(pdir, with_calcs=not a.no_calcs)}")
        if a.en:  # EN-версия в одном вызове: каркас на английском, секции пишет writer (PRO-53)
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
    # предупреждения о несвежем реестре печатает summary_text (PRO-41: без дублей)
    print(check.report_text(res["check"], i18n.lang_of(pdir)))
    print(finish.summary_text(res, i18n.lang_of(pdir)))


DIST_NAME = "product-factory-strategist"  # имя пакета в importlib.metadata (PRO-44)
_DEFAULT = object()  # маркер «не передано» для параметров install_lines


def _dist_info(name: str = DIST_NAME) -> tuple[str | None, Path | None]:
    """Версия и путь до dist-info установленного пакета; (None, None), если пакет не установлен."""
    try:
        dist = importlib.metadata.distribution(name)
    except importlib.metadata.PackageNotFoundError:
        return None, None
    path = getattr(dist, "_path", None)  # PathDistribution: каталог dist-info в site-packages
    if path is None:  # нестандартный Distribution — ищем dist-info по sys.path
        norm = re.sub(r"[^A-Za-z0-9.]+", "_", name)
        for entry in sys.path:
            if entry and os.path.isdir(entry):
                hits = sorted(Path(entry).glob(f"{norm}-*.dist-info"))
                if hits:
                    path = hits[0]
                    break
    return dist.version, (Path(path) if path else None)


def install_mode(dist_path: Path | None, mod_file: Path) -> str:
    """Способ установки: editable (код вне site-packages), venv (код рядом с dist-info), source (без dist-info)."""
    if dist_path is None:
        return "source"
    mod_root = Path(mod_file).resolve().parents[2]  # tools/pfs/cli.py → корень пакета или site-packages
    return "venv" if mod_root == Path(dist_path).resolve().parent else "editable"


def install_lines(mod_file=_DEFAULT, dist_path=_DEFAULT, version=_DEFAULT,
                  pfs_path=_DEFAULT, projects_dir=_DEFAULT) -> list[str]:
    """Строки блока «Установка» для pfs doctor (PRO-44): режим, which pfs, PATH, projects dir, версия."""
    if mod_file is _DEFAULT:
        mod_file = Path(__file__).resolve()
    if dist_path is _DEFAULT or version is _DEFAULT:
        version_, dist_path_ = _dist_info()
        if dist_path is _DEFAULT:
            dist_path = dist_path_
        if version is _DEFAULT:
            version = version_
    if pfs_path is _DEFAULT:
        pfs_path = shutil.which("pfs")
    if projects_dir is _DEFAULT:
        projects_dir = core.projects_dir()
    mode = install_mode(dist_path, mod_file)
    lines = [
        f"Установка: {mode}; версия: {version or 'нет (пакет не установлен)'}",
        f"  pfs: {pfs_path or 'нет в PATH'}",
    ]
    if pfs_path:
        lines.append("  PATH: ok (каталог с pfs есть в PATH)")
    else:
        hint = Path(sys.executable).resolve().parent
        lines.append(f"  PATH: pfs не найден — проверьте, что bin-каталог окружения есть в PATH ({hint})")
        local = Path.home() / ".local" / "bin"
        if (local / "pfs").exists():
            lines.append(f"  PATH: pfs есть в {local}, но каталог не в PATH — добавьте его в PATH")
    lines += [f"  Python: {sys.executable}", f"  Projects dir: {projects_dir}"]
    return lines


def cmd_doctor(a):
    ok = sys.version_info >= (3, 9)
    print(f"Python {sys.version.split()[0]}: {'ok' if ok else 'нужен 3.9+'}")
    for line in install_lines():
        print(line)
    print(f"pdftotext: {'есть' if shutil.which('pdftotext') else 'нет (PDF: pip install pypdf или brew install poppler)'}")
    try:
        import pypdf  # type: ignore  # noqa: F401
        print("pypdf: есть")
    except ImportError:
        print("pypdf: нет (необязательно)")
    projects = project.list_projects()
    active = core.active_slug()
    print(f"Карт в базе знаний: {len(kb.cards())}; проектов: {len(projects)}; активный: {active}")
    if active and active not in {p["slug"] for p in projects}:
        # PRO-67: закоммиченный .active с чужим slug'ом ломал чистый клон
        print(f"⚠ Активный проект '{active}' не найден в {core.projects_dir()} — указатель projects/.active битый")
        if getattr(a, "fix", False):
            core.clear_active()
            print("  исправлено: указатель сброшен — создайте проект (pfs new) или выберите (pfs use <slug>)")
        else:
            print("  исправление: pfs doctor --fix")
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

    s = sp.add_parser("new", help="создать проект | create a project"); s.add_argument("title"); s.add_argument("question")
    s.add_argument("--slug")
    s.add_argument("--lang", choices=["ru", "en"], default="ru",
                   help="язык проекта (PRO-57): messages, templates and quality-gate headings; ru по умолчанию")
    s.set_defaults(f=cmd_new)
    s = sp.add_parser("lang", help="язык проекта: показать или переключить ru|en (PRO-57)")
    s.add_argument("value", nargs="?", choices=["ru", "en"], help="без значения — показать текущий")
    s.set_defaults(f=cmd_lang)
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
    s.add_argument("action", choices=["add", "add-batch", "list", "retract", "supersede", "rebase", "retag"],
                   help="add-batch — пачка из JSONL-файла (text/kind/source/grade/quote/from); "
                        "невалидная строка отменяет весь батч; retag — перенумерация тегов [C###] "
                        "во всех outputs одной командой (--from C003 --to C059) с журналом")
    s.add_argument("text", nargs="?"); s.add_argument("--id"); s.add_argument("--kind", choices=claims.KINDS)
    s.add_argument("--source"); s.add_argument("--from", dest="from_ref"); s.add_argument("--to")
    s.add_argument("--confidence", default="medium")
    s.add_argument("--note"); s.add_argument("--quote"); s.add_argument("--reason"); s.add_argument("--all", action="store_true")
    s.add_argument("--grade", choices=claims.GRADES, help="сила доказательства A–D")
    s.set_defaults(f=cmd_claim)

    s = sp.add_parser("check", help="контроль качества"); s.add_argument("--json", action="store_true")
    s.add_argument("--strict", action="store_true"); s.set_defaults(f=cmd_check)
    s = sp.add_parser("review", help="lock вердикта review: снимок реестра после ревизии (PRO-27)")
    s.add_argument("action", choices=["lock"],
                   help="lock — sha256 claims/sources и документов 00–07 в outputs/.review_state.json; "
                        "правки реестра после lock дают «⚠ вердикт review устарел» в check/status/export; "
                        "повторный lock после ревизии снимает предупреждение")
    s.set_defaults(f=cmd_review)
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
    s.add_argument("--plan-month", type=float, help="фактический тариф подписки, USD/мес — отдельно показать долю подписки проекта (PRO-62)")
    s.add_argument("--session", nargs="?", const="", default=None,
                   help="ID сессии (при --transcript) или транскрипт: путь/часть имени "
                        "(*_session.json / *.jsonl в корне проекта; без --transcript — алиас с авто-детектом, "
                        "без значения — самый свежий)")
    s.add_argument("--since", help="ISO-время начала задачи (UTC), учитывать сообщения после него")
    s.add_argument("--until", help="ISO-время окончания задачи (UTC)")
    s.add_argument("--window", action="store_true", help="сохранить --since/--until в project.json (хук Stop будет их соблюдать)")
    s.set_defaults(f=cmd_cost)

    s = sp.add_parser("kb", help="база знаний"); s.add_argument("action", choices=["search", "index", "show", "lint"]); s.add_argument("query", nargs="?")
    s.add_argument("-k", type=int, default=8); s.add_argument("--with-project", action="store_true")
    s.add_argument("--lang", choices=["ru", "en"], default="ru"); s.set_defaults(f=cmd_kb)

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

    s = sp.add_parser("ab", help="дизайн A/B-теста: документ по шаблону + чек-лист запуска + контекст AI-ревьюера")
    s.add_argument("--hypothesis", help="C### — гипотеза из реестра (по умолчанию первая активная гипотеза/прогноз или «Гипотеза 1» из 06)")
    s.add_argument("--metric", help="целевая метрика (для доли и ratio — числитель/знаменатель)")
    s.add_argument("--proxy", help="прокси-метрика — помогает заметить эффект раньше")
    s.add_argument("--guardrail", help="защитная метрика и порог недопустимого вреда")
    s.add_argument("--baseline", type=float, help="базовое значение целевой метрики, доля 0<p<1, напр. 0.018")
    s.add_argument("--mde", type=float, help="минимальный обнаружимый эффект в абсолютных долях, напр. 0.01")
    s.add_argument("--alpha", type=float, default=0.05, help="уровень значимости (по умолчанию 0.05)")
    s.add_argument("--power", type=float, default=0.8, help="мощность (по умолчанию 0.8)")
    s.add_argument("--traffic", type=float, help="суточный трафик подходящей аудитории (для расчёта длительности)")
    s.add_argument("--share", type=float, default=0.5, help="доля трафика на тестовую группу (по умолчанию 0.5)")
    s.add_argument("--rules", help="правила решения: порог успеха; отказ; неясный результат")
    s.add_argument("--split-system", help="система сплитования и идентификатор, напр. «Experimentus, ID=user_id»")
    s.set_defaults(f=cmd_ab)

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
                   help="вместе с --six-pager собрать EN-версию (SIX_PAGER_EN.md): каркас на английском, "
                        "секции пишет six-pager-writer из того же пакета данных (spec: SIX_PAGER_PROMPT_EN.md)")
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
    s = sp.add_parser("next", help="что решать сейчас: шаг, обязательства, устаревшие источники (с командой refresh), пересмотры, открытые вопросы")
    s.set_defaults(f=cmd_next)
    s = sp.add_parser("questions", help="вопросные блоки шага (настраиваемость стратегии)")
    s.add_argument("block", nargs="?", default=None, help="шаг или id блока, напр. options-criteria; без аргумента — обзор всех шагов")
    s.set_defaults(f=cmd_questions)
    s = sp.add_parser("finish", help="собрать финальный пакет одной цепочкой: Excel → REPORT → six-pager → DOCX → deck")
    s.add_argument("--no-deck", action="store_true", help="не собирать HTML-деку")
    s.add_argument("--en", action="store_true", help="дополнительно EN-версия six-pager (SIX_PAGER_EN.md + DOCX)")
    s.set_defaults(f=cmd_finish)
    s = sp.add_parser("doctor", help="проверка установки, окружения и реестров источников")
    s.add_argument("--fix", action="store_true",
                   help="автоисправление: сбросить битый указатель активного проекта (PRO-67)")
    s.set_defaults(f=cmd_doctor)
    return ap


def main(argv: list[str] | None = None) -> int:
    if argv is None and len(sys.argv) == 1:
        # дружелюбный запуск без аргументов: краткая шпаргалка вместо usage-ошибки
        import importlib.metadata
        ver = "?"

        try:
            ver = importlib.metadata.version("product-factory-strategist")
        except Exception:
            pass
        print(f"Strategist CLI (pfs) v{ver} — стратег-агент для цифровых продуктов")
        print()
        print("Быстрый старт:")
        print("  pfs new \"<название>\" \"<запрос дословно>\"   # новый проект")
        print("  pfs list / status / next                  # где остановились, что решать")
        print("  pfs finish                                # финальный пакет одной цепочкой")
        print()
        print("Полная справка: pfs --help | Сценарий под задачу: pfs route \"<запрос>\"")
        return 0
    args = build_parser().parse_args(argv)
    try:
        args.f(args)
    except PfsError as exc:
        # PRO-57: язык активного проекта, если определим — иначе ru (сообщение об ошибке без трейсбека)
        try:
            lang = i18n.active_lang()
        except Exception:
            lang = "ru"
        print(i18n.t(lang, "error_prefix", msg=exc), file=sys.stderr)
        return 2
    return 0
