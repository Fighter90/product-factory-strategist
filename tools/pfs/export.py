"""Сборка итогового отчёта: документы + реестр утверждений + источники + решения + стоимость."""
from __future__ import annotations

import hashlib
import html as html_mod
import json
import re
from pathlib import Path
from urllib.parse import urlparse

from . import calc, check, claims as claims_mod, core, cost, decisions, i18n, sources as src_mod
from .xlsx import sheet_names

ORDER = ["00_brief.md", "01_research_plan.md", "02_situation.md", "03_options.md", "04_product_strategy.md",
         "05_comms_strategy.md", "06_validation_plan.md", "07_quality_review.md"]

STATE = ".export_state.json"


# ---------- свежесть экспорта: снимок реестра на момент сборки ----------

def _registry_snapshot(pdir: Path) -> dict:
    """Снимок реестра на момент экспорта: числа строк, sha256 содержимого реестров
    и расчётов (calcs.json, outputs/attachments/*.xlsx). Хеш ловит правки на месте
    (retract/rebase/supersede, source refresh), которые число строк не меняют.
    PRO-63: расчёты сравниваются по СОДЕРЖИМОМУ, а не по mtime — время изменения
    файлов невоспроизводимо при git clone (чистый клон давал ложное «Excel
    пересобран»). mtime-поля сохраняются для совместимости со старыми снимками."""
    calcs = pdir / "calcs.json"
    att_mtime = max((p.stat().st_mtime for p in (pdir / "outputs" / "attachments").glob("*.xlsx")),
                    default=None)
    return {"at": core.now(),
            "claims": len(core.read_jsonl(pdir / "claims.jsonl")),
            "sources": len(core.read_jsonl(pdir / "sources.jsonl")),
            "claims_sha": _file_sha(pdir / "claims.jsonl"),
            "sources_sha": _file_sha(pdir / "sources.jsonl"),
            "calcs_sha": _file_sha(calcs),
            "att_shas": {p.name: _file_sha(p)
                         for p in sorted((pdir / "outputs" / "attachments").glob("*.xlsx"))},
            "calcs_mtime": calcs.stat().st_mtime if calcs.exists() else None,
            "attachments_mtime": att_mtime}


def _file_sha(path: Path) -> str | None:
    """sha256 файла реестра или None, если файла нет."""
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None


def read_state(pdir: Path) -> dict | None:
    """Снимок из последнего экспорта или None, если экспорта ещё не было."""
    snap = core.read_json(pdir / "outputs" / STATE)
    return snap if isinstance(snap, dict) else None


def save_state(pdir: Path) -> dict:
    """Зафиксировать снимок реестра в outputs/.export_state.json (после успешной сборки)."""
    snap = _registry_snapshot(pdir)
    core.write_json(pdir / "outputs" / STATE, snap)
    return snap


def _excel_changed(pdir: Path, snap: dict) -> bool:
    """calcs.json или книги в outputs/attachments изменились после последнего экспорта.
    Снимки нового формата (PRO-63) сравниваются по sha256 — воспроизводимо на чистом
    клоне; старые снимки (только mtime) — по mtime, как раньше."""
    calcs = pdir / "calcs.json"
    if "calcs_sha" in snap or "att_shas" in snap:  # снимок нового формата
        if snap.get("calcs_sha") != _file_sha(calcs):
            return True
        cur = {p.name: _file_sha(p)
               for p in sorted((pdir / "outputs" / "attachments").glob("*.xlsx"))}
        return cur != (snap.get("att_shas") or {})
    if (calcs.stat().st_mtime if calcs.exists() else None) != snap.get("calcs_mtime"):
        return True
    att_mtime = max((p.stat().st_mtime for p in (pdir / "outputs" / "attachments").glob("*.xlsx")),
                    default=None)
    return att_mtime != snap.get("attachments_mtime")


def freshness_warnings(pdir: Path) -> list[str]:
    """Предупреждение об устаревшем отчёте: реестр изменился после последнего экспорта
    (по числу строк ИЛИ по содержимому — отзыв/замещение/refresh пишут файл на месте).
    [] — снимка нет или с момента сборки ничего не поменялось."""
    snap = read_state(pdir)
    if not snap:
        return []
    parts = []
    d_claims = len(core.read_jsonl(pdir / "claims.jsonl")) - int(snap.get("claims") or 0)
    d_sources = len(core.read_jsonl(pdir / "sources.jsonl")) - int(snap.get("sources") or 0)
    if d_claims:
        parts.append(f"{d_claims:+d} claims")
    elif snap.get("claims_sha") and _file_sha(pdir / "claims.jsonl") != snap["claims_sha"]:
        parts.append("изменено содержимое claims.jsonl")
    if d_sources:
        parts.append(f"{d_sources:+d} sources")
    elif snap.get("sources_sha") and _file_sha(pdir / "sources.jsonl") != snap["sources_sha"]:
        parts.append("изменено содержимое sources.jsonl")
    if _excel_changed(pdir, snap):
        parts.append("Excel пересобран")
    if not parts:
        return []
    return ["⚠ Реестр изменился после последнего экспорта: " + ", ".join(parts)
            + " — приложения REPORT/SIX_PAGER устарели. Пересоберите: `pfs export`."]


def build(pdir: Path) -> Path:
    lang = i18n.lang_of(pdir)
    tr = lambda key, **kw: i18n.t(lang, key, **kw)
    meta = core.read_json(pdir / "project.json", {})
    parts = [tr("report_title", title=meta.get("title")), "",
             tr("report_built", ts=core.now()[:16]), ""]
    outs = pdir / "outputs"
    for name in ORDER + sorted(p.name for p in outs.glob("*.md")
                               if p.name not in ORDER and p.name != "REPORT.md"
                               and not p.name.startswith("six_pager_pack")):  # PRO-46: пакет — рабочий вход писателя
        p = outs / name
        if p.exists():
            body = p.read_text(encoding="utf-8")
            note = tr("report_sixpager_note", spec=i18n.SIX_PAGER_SPEC[lang]) if p.name == "SIX_PAGER.md" else ""
            parts += [note + body.replace("\n# ", "\n## ") if not body.startswith("# ") else "#" + body, "", "---", ""]
    active = [c for c in claims_mod.load(pdir)]
    parts += [tr("appx_a_claims"), "", claims_mod.table(active), ""]
    parts += [tr("appx_b_sources"), "", tr("appx_sources_header"), "|---|---|---|---|---|"]
    for s in src_mod.load(pdir):
        parts.append(f"| {s['id']} | {s['title'].replace('|', '/')} | {s.get('url') or s.get('path') or '—'} | {s['origin']} | {s['retrieved'][:10]} |")
    decs = decisions.load(pdir)
    if decs:
        parts += ["", tr("appx_c_decisions"), "", decisions.table(decs)]
    qc = check.run(pdir)
    parts += ["", tr("appx_d_transparency"), "", "```", cost.summary_text(pdir, lang),
              check.report_text(qc, lang), "```"]
    att = attachments_table(pdir)
    if att:
        parts += ["", tr("appx_e_excel"), "", att]
    path = outs / "REPORT.md"
    core.atomic_write(path, "\n".join(parts) + "\n")
    core.log(pdir, "action", "Собран outputs/REPORT.md", tool="pfs export")
    return path


# ---------- six-pager (FAQ-1…FAQ-6) с Excel-приложениями ----------

ATTACHMENTS = [
    ("unit_economics.xlsx", "ARPU, VC, CAC, отток"),
    ("growth_model.xlsx", "MAU, рост, конверсия, AOV, take rate"),
    ("cohort_retention.xlsx", "размеры когорт, кривая удержания"),
    ("market_sizing.xlsx", "PAM, доли воронки, факторы среды"),
]


def attachments_table(pdir: Path) -> str | None:
    """Маркдаун-таблица ВСЕХ книг из outputs/attachments/*.xlsx или None, если пусто.
    Листы читаются из самих книг; для стандартных расчётов — подсказка, что править."""
    books = sorted((pdir / "outputs" / "attachments").glob("*.xlsx"))
    if not books:
        return None
    hints = dict(ATTACHMENTS)
    rows = []
    for p in books:
        try:
            sheets = " · ".join(sheet_names(p)) or "—"
        except Exception:
            sheets = "—"
        rows.append(f"| {p.name} | {sheets} | {hints.get(p.name, '—')} |")
    return "| Файл | Листы | Что редактировать |\n|---|---|---|\n" + "\n".join(rows)


def _split_sections(text: str) -> list[dict]:
    """Markdown → блоки по строкам-заголовкам ^#+ ({level, title, lines}); текст до первого
    заголовка — блок уровня 0. Вложенные секции — отдельные блоки, поэтому дерево
    собирается функцией _subtree, а не вложенностью lines."""
    blocks: list[dict] = [{"level": 0, "title": "", "lines": []}]
    for line in text.splitlines():
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            blocks.append({"level": len(m.group(1)), "title": m.group(2).strip(), "lines": []})
        else:
            blocks[-1]["lines"].append(line)
    return blocks


def _subtree(blocks: list[dict], i: int) -> list[int]:
    """Блок i и вложенные в него секции (глубже по уровню, до такой же/выше)."""
    out, lvl = [i], blocks[i]["level"]
    for j in range(i + 1, len(blocks)):
        if blocks[j]["level"] <= lvl:
            break
        out.append(j)
    return out


def _norm_title(s: str) -> str:
    """Нормализация заголовка/колонки: без «(…)», регистра и знаков — только слова/числа."""
    s = re.sub(r"\([^)]*\)", " ", s.lower())
    return re.sub(r"[^a-zа-яё0-9+]+", " ", s).strip()


def _json(data) -> str:
    """Компактный JSON для читаемой версии пакета данных (контекст писателя)."""
    return json.dumps(data, ensure_ascii=False, separators=(", ", ": "))


def _section_bodies(path: Path) -> list[dict]:
    """Секции ВЕРХНЕГО уровня документа (ровно ##) как ДАННЫЕ пакета: [{title, text}] —
    заголовок и текст секции с вложенными (вложенные заголовки сохраняются в тексте).
    Рабочие документы читаются только сюда; в six-pager их текст не вставляется (PRO-46)."""
    if not path.exists():
        return []
    blocks = _split_sections(path.read_text(encoding="utf-8"))
    out: list[dict] = []
    for i, b in enumerate(blocks):
        if b["level"] != 2:  # вложенные ### — часть текста родителя, не отдельная секция
            continue
        lines: list[str] = []
        for j in _subtree(blocks, i):
            bb = blocks[j]
            if j != i:
                lines.append(f"{'#' * bb['level']} {bb['title']}")
            lines.extend(bb["lines"])
        out.append({"title": b["title"], "text": "\n".join(lines).strip()})
    return out


def build_six_pager_pack(pdir: Path) -> dict:
    """PRO-46: пакет данных six-pager — единственный вход текста для six-pager-writer.
    Пишется в `outputs/six_pager_pack.json` и читаемую версию `six_pager_pack.md`:
    утверждения с типом и силой A–D, источники, расчёты из calcs (с производными той же
    математикой, что Excel и кросс-чек), варианты из 03, выбор руководителя (ответы
    из state.json), инициативы Outcome-роадмапа 04, KPI из явной таблицы 06, решения.
    Рабочие документы целиком не включаются — их секции входят как данные «Ситуации»
    и «Вариантов»; полная версия с доказательствами — REPORT.md."""
    meta = core.read_json(pdir / "project.json", {})
    state = core.read_json(pdir / "state.json", {})
    ue = core.read_json(pdir / "calcs.json", {})
    unit = {k: v for k, v in (ue.get("unit_econ") or {}).items()
            if not k.startswith("_") and v is not None}
    pack: dict = {
        "meta": {"title": meta.get("title"), "question": meta.get("question"),
                 "spec": "knowledge/templates/SIX_PAGER_PROMPT.md", "generated": core.now()},
        "situation": {"sections": _section_bodies(pdir / "outputs" / "02_situation.md"),
                      "user_barrier": _user_needs(pdir)},
        "claims": [{"id": c["id"], "kind": c["kind"], "grade": c.get("grade"),
                    "text": c["text"], "sources": c["sources"]}
                   for c in claims_mod.load(pdir) if c["status"] == "active"],
        "sources": [{"id": s["id"], "title": s["title"], "origin": s.get("origin"),
                     "link": s.get("url") or s.get("path") or "",
                     "date": (s.get("published") or s.get("retrieved") or "")[:10]}
                    for s in src_mod.load(pdir)],
        "calcs": {"sections": ue, "derived": calc.unit_metrics(unit) if unit else {}},
        "options": _section_bodies(pdir / "outputs" / "03_options.md"),
        "strategy": _section_bodies(pdir / "outputs" / "04_product_strategy.md"),
        "choice": {"answers": [a.get("answer") for a in state.get("answers", [])],
                   "choice_ts": (state.get("steps", {}).get("choice") or {}).get("ts")},
        "initiatives": {"groups": _initiative_groups(pdir), "user_barrier": _user_needs(pdir)},
        "kpi": _kpi_rows(pdir),
        "decisions": decisions.load(pdir),
    }
    core.atomic_write(pdir / "outputs" / "six_pager_pack.json", _json(pack))
    core.atomic_write(pdir / "outputs" / "six_pager_pack.md", _pack_md(pack))
    return pack


def _pack_md(pack: dict) -> str:
    """Читаемая версия пакета данных: те же разделы, таблицы утверждений/источников/KPI.
    Это рабочий вход писателя, не документ комитета — в REPORT.md не попадает."""
    p = [f"# Пакет данных six-pager — {pack['meta'].get('title')}", "",
         f"> Собран {pack['meta']['generated'][:16]}. Единственный вход текста six-pager-writer: "
         "пишите по слотам `outputs/SIX_PAGER.md` из этого пакета по спецификации "
         "`knowledge/templates/SIX_PAGER_PROMPT.md`. Рабочие документы 02–07 не вставляются: "
         "полная версия с доказательствами — REPORT.md. Чего в пакете нет — честный пробел.", ""]
    p += ["## Запрос", "", str(pack["meta"].get("question") or ""), ""]
    p += ["## Ситуация", ""]
    for s in pack["situation"]["sections"]:
        p += [f"### {s['title']}", "", s["text"], ""]
    if pack["situation"].get("user_barrier"):
        p += [f"Барьер пользователя (JTBD): {pack['situation']['user_barrier']}", ""]
    p += ["## Утверждения (сила A–D)", "",
          "| ID | Тип | Сила | Утверждение | Источники |", "|---|---|---|---|---|"]
    p += [f"| {c['id']} | {c['kind']} | {c.get('grade') or '—'} | {c['text'].replace('|', '/')} "
          f"| {', '.join(c['sources']) or '—'} |" for c in pack["claims"]] or ["—"]
    p += ["", "## Источники", "",
          "| ID | Название | Где | Происхождение | Дата |", "|---|---|---|---|---|"]
    p += [f"| {s['id']} | {s['title'].replace('|', '/')} | {s['link'] or '—'} "
          f"| {s['origin']} | {s['date'] or '—'} |" for s in pack["sources"]] or ["—"]
    p += ["", "## Расчёты (calcs)", ""]
    for name, sec in (pack["calcs"]["sections"] or {}).items():
        p.append(f"- **{name}:** {_json({k: v for k, v in sec.items() if not k.startswith('_')})}")
    if pack["calcs"]["derived"]:
        p.append("- **производные:** " + _json(pack["calcs"]["derived"]))
    p += ["", "## Варианты", ""]
    for o in pack["options"]:
        p += [f"### {o['title']}", "", o["text"], ""]
    if pack.get("strategy"):
        p += ["## Продуктовая стратегия (выписка)", ""]
        for s in pack["strategy"]:
            p += [f"### {s['title']}", "", s["text"], ""]
    p += ["## Выбор руководителя", ""]
    for a in pack["choice"]["answers"]:
        p.append(f"- {a}")
    p += ["", "## Инициативы (Outcome-роадмап)", ""]
    if pack["initiatives"].get("user_barrier"):
        p += [f"Потребности пользователя: {pack['initiatives']['user_barrier']}", ""]
    for g in pack["initiatives"]["groups"]:
        tactics = "; ".join(g["tactics"])
        gate = f" Гейт: {g['gate']}." if g["gate"] else ""
        p.append(f"- **{g['name']}** — фокус: {g['focus']}. Тактики: {tactics}.{gate}")
    p += ["", "## KPI", ""]
    for plane, rows in pack["kpi"].items():
        p += [f"**{plane}**", "", _KPI_HEAD, "|---|---|---|---|---|---|"]
        p += ["| " + " | ".join(c.replace("|", "/") for c in r) + " |" for r in rows]
        p.append("")
    p += ["## Решения", ""]
    for d in pack["decisions"]:
        line = f"- **{d['id']}** — {d.get('title')}: {d.get('decision')} (отв. {d.get('owner')})"
        grounds = ", ".join(d.get("grounds") or [])
        if grounds:
            line += f"; основания: {grounds}"
        p.append(line)
    return "\n".join(p) + "\n"


def _flat(v) -> str:
    """Любое значение → компактная строка (строки как есть; dict → 'k: x'; None/пустое → '')."""
    if v is None:
        return ""
    if isinstance(v, str):
        return v.strip()
    if isinstance(v, dict):
        return ", ".join(f"{k}: {x}" for k, x in v.items() if x not in (None, "", []))
    if isinstance(v, (list, tuple)):
        return ", ".join(_flat(x) for x in v if x not in (None, "", []))
    return str(v)


_FN_TAG = re.compile(r"\[([CS]\d{3,})\]")
_GRADE_RANK = {"A": 1, "B": 2, "C": 3, "D": 4}
_SYNTH_NOTE = "**Синтетические материалы** (гипотезы, не доказательство):"


def _publisher(s: dict) -> str:
    """Издатель для сноски: домен из URL; у файла издателя нет — пусто."""
    url = _flat(s.get("url"))
    return (urlparse(url).hostname or "") if url else ""


def _footnote_line(n: int, s: dict, grade: str | None) -> str:
    """[^N]: S### — издатель — название — дата (published, иначе retrieved) — URL/файл — сила X.
    Поля без значения пропускаются; в сноске всегда есть S### и название."""
    parts = [f"**{s.get('id', 'S###')}**"]
    pub = _publisher(s)
    if pub:
        parts.append(pub)
    parts.append(_flat(s.get("title")))
    date = (_flat(s.get("published")) or _flat(s.get("retrieved")))[:10]
    if date:
        parts.append(date)
    link = _flat(s.get("url")) or _flat(s.get("path"))
    if link:
        parts.append(link)
    line = f"[^{n}]: " + " — ".join(parts)
    if grade:
        line += f" — сила {grade}"
    return line


def _footnote_plan(pdir: Path, body: str) -> tuple[str, str | None]:
    """PRO-49: теги [C###]/[S###] в собранном six-pager → сквозные сноски [^N] в порядке
    первого упоминания. Связка C → S — реестр утверждений (поле sources); прямые теги
    [S###] цитируются напрямую. В сносках — только процитированные источники; синтетика
    (origin=synthetic) — отдельным блоком с пометкой «гипотезы, не доказательство».
    Сила A–D — худший grade утверждений, цитирующих источник (вывод не сильнее слабейшего
    входа). Тег без источника (неизвестный C###/S###, утверждение без sources) исчезает:
    полный реестр тегов — REPORT.md, приложение «Реестр утверждений».
    Возвращает (текст со сносками, блок сносок | None — не процитировано ничего)."""
    claims = {c["id"]: c for c in claims_mod.load(pdir)}
    srcs = {s["id"]: s for s in src_mod.load(pdir)}
    cited: list[str] = []               # источники в порядке первого упоминания
    claim_srcs: dict[str, list[str]] = {}
    for m in _FN_TAG.finditer(body):
        tid = m.group(1)
        if tid.startswith("C"):
            c = claims.get(tid)
            sids = [s for s in c.get("sources", []) if s in srcs] if c else []
            claim_srcs[tid] = sids
        elif tid in srcs:
            sids = [tid]
        else:
            sids = []
        for sid in sids:
            if sid not in cited:
                cited.append(sid)
    if not cited:
        return body, None
    num = {sid: i for i, sid in enumerate(cited, 1)}
    grades: dict[str, list[str]] = {}
    for cid, sids in claim_srcs.items():
        g = claims[cid].get("grade") if cid in claims else None
        if g in _GRADE_RANK:
            for sid in sids:
                grades.setdefault(sid, []).append(g)
    worst = {sid: max(gs, key=_GRADE_RANK.get) for sid, gs in grades.items()}
    syn = [sid for sid in cited if srcs[sid].get("origin") == "synthetic"]

    def sub(m: re.Match) -> str:
        tid = m.group(1)
        sids = claim_srcs.get(tid) or ([tid] if tid in srcs else [])
        markers = "".join(f"[^{num[sid]}]" for sid in sids if sid in num)
        return f" {markers}" if markers else ""  # пробел до тега возвращаем при маркерах

    body = re.sub(r" ?\[([CS]\d{3,})\]", sub, body)
    lines = [_footnote_line(num[sid], srcs[sid], worst.get(sid))
             for sid in cited if sid not in syn]
    out = "\n".join(lines)
    if syn:
        out += ("\n\n" + _SYNTH_NOTE + "\n\n"
                + "\n".join(_footnote_line(num[sid], srcs[sid], worst.get(sid)) for sid in syn))
    return body, out


# ---------- i18n скелета six-pager (RU по умолчанию; EN — черновик, PRO-31) ----------
# Переводятся только фиксированные строки-скелет, которые генерирует инструмент.
# Содержимое документов 00–07 остаётся на языке автора — полный синхронный перевод
# по спецификации SIX_PAGER_PROMPT.md делает агент, не CLI (вне возможностей stdlib).

_EN: dict[str, str] = {
    "CAC платящего = CAC / конверсия free → paid":
        "Paying-user CAC = CAC / free → paid conversion",
    "ARPU средневзвешенный по тарифам": "Tier-weighted ARPU",
    "**Вывод (умозаключение):** критерий LTV/CAC ≥ 3 не выполняется: фактический "
    "{ratio} при CAC платящего {cac} — для ≥ 3 нужен CAC платящего ≤ {cap} при этом LTV "
    "(сценарии и сетка — листы «Сценарии» и «Чувствительность» unit_economics.xlsx).":
        "**Conclusion (inference):** the LTV/CAC ≥ 3 bar is not met: actual {ratio} at a "
        "paying-user CAC of {cac} — to reach ≥ 3, paying-user CAC must be ≤ {cap} at this LTV "
        "(scenarios and grid — the Scenarios and Sensitivity sheets of unit_economics.xlsx).",
    "# {title}: six-pager": "# Six-pager (EN)",
    "> Каркас и пакет данных собраны {ts} командой `pfs export --six-pager`. "
    "Текст по слотам пишет субагент `six-pager-writer` из пакета данных "
    "(`outputs/six_pager_pack.json`, читаемая версия — `six_pager_pack.md`) "
    "по спецификации `knowledge/templates/SIX_PAGER_PROMPT.md`; рабочие "
    "документы 02–07 не вставляются — полная версия с доказательствами "
    "в REPORT.md. Обязательный цикл: написать → `pfs check --six-pager` → "
    "исправить до 0 ошибок. Числа — со сносками; теги C###/S### и полный "
    "реестр доказательств — REPORT.md.":
        core.EN_DRAFT_MARK + " the EN six-pager is written in plain English by the "
        "six-pager-writer from the SAME data package outputs/six_pager_pack.md "
        "(claims, sources, calculations; documents 00–07 are RU inputs — never pasted "
        "verbatim), per the spec `knowledge/templates/SIX_PAGER_PROMPT_EN.md`, style "
        "guide `knowledge/templates/STYLE_EN.md` (plain English, numbers 1,234.5, no "
        "calque). Restate the project title and question in English (project.json: "
        "title, question). Mandatory loop: write → `pfs check --six-pager` → fix until "
        "0 errors. Assembled {ts} by `pfs export --six-pager`. Numbers carry sequential "
        "footnotes in the same order and numbering as RU SIX_PAGER.md; each footnote "
        "names its source ID: S### — publisher — title — date — URL — grade A–D. Raw "
        "C###/S### tags stay out of the six-pager; the full evidence registry lives "
        "in REPORT.md.",
    "**Запрос:** {q}": "**Request:** — write in English; RU source: project.json → question.",
    "## FAQ-1. Анализ текущего состояния": "## FAQ-1. Current state analysis",
    "### 1.1 Обзор рынка: тренды, вызовы и возможности":
        "### 1.1 Market overview: trends, challenges and opportunities",
    "### 1.2 Ключевые конкуренты и анализ их стратегий роста и промо-механик":
        "### 1.2 Key competitors: growth and promo mechanics",
    "Сравнительная таблица групп конкурентов (заполните после конкурентного анализа):":
        "Comparative table of competitor groups (fill in after competitive analysis):",
    "| | Группа 1 | Группа 2 | Группа 3 |": "| | Group 1 | Group 2 | Group 3 |",
    "| **Ключевые преимущества** | … | … | … |": "| **Key advantages** | … | … | … |",
    "| **Стратегия роста и промо-механики** | … | … | … |":
        "| **Growth and promo mechanics** | … | … | … |",
    "| **Риски для компании** | … — Высокий/Средний/Низкий | … | … |":
        "| **Risks for the company** | … — High/Medium/Low | … | … |",
    "> **Вывод (умозаключение):** окно возможностей и его срок — заполните по данным 1.1–1.2.":
        "> **Conclusion (inference):** the opportunity window and its horizon — fill from 1.1–1.2.",
    "## FAQ-2. User Persona. Кто является целевой аудиторией?":
        "## FAQ-2. User Persona. Who is the target audience?",
    "### 2.1 Сегменты": "### 2.1 Segments",
    "Таблица персон (заполните):": "Persona table (fill in):",
    "| | Сегмент 1 | Сегмент 2 | Сегмент 3 |": "| | Segment 1 | Segment 2 | Segment 3 |",
    "| **Кто они?** | … | … | … |": "| **Who are they?** | … | … | … |",
    "| **Что используют сегодня и почему?** | … | … | … |":
        "| **What do they use today and why?** | … | … | … |",
    "| **С какими трудностями сталкиваются?** | … | … | … |":
        "| **What difficulties do they face?** | … | … | … |",
    "| **Общие трудности** | … | … |": "| **Common difficulties** | … | … |",
    "### 2.2 Барьеры на каждом этапе пути": "### 2.2 Barriers at each journey stage",
    "| Этап пути | Барьер сегодня | Что делает продукт |":
        "| Journey stage | Barrier today | What the product does |",
    "| Привлечение | … | … |": "| Acquisition | … | … |",
    "| Выбор / использование | … | … |": "| Choice / usage | … | … |",
    "| Оплата | … | … |": "| Payment | … | … |",
    "| Постоплатный опыт | … | … |": "| Post-payment experience | … | … |",
    "Что сдерживает от старта или продления? (заполните по сегментам):":
        "What holds back signup or renewal? (fill in per segment):",
    "| Сегмент | Сдерживающий фактор | Чем снимается |":
        "| Segment | Blocking factor | How it is removed |",
    "| Сегмент 1 | … | … |": "| Segment 1 | … | … |",
    "> **Вывод (умозаключение):** сегментация по барьеру входа; лестница тиров "
    "обслуживает все барьеры; приоритизация — по ёмкости/CAC/конкуренции (расчёт — выше).":
        "> **Conclusion (inference):** segment by the entry barrier; the tier ladder serves "
        "all barriers; prioritize by capacity/CAC/competition (calculation above).",
    "## FAQ-3. Стратегические инициативы. Кратко обоснуйте каждую.":
        "## FAQ-3. Strategic initiatives. Justify each one briefly.",
    "### Инициативы выбранного направления (драйверы)":
        "### Initiatives of the chosen direction (drivers)",
    "Сформулируйте 3–4 инициативы по схеме: «**Первый драйвер** — …», «**Второй драйвер** — …», "
    "далее «Ключевые направления» (буллеты) и пошаговый расчёт эффекта. Данные — разделы "
    "«Варианты», «Выбор руководителя» и «Инициативы» пакета. Закройте "
    "выводом-умозаключением.":
        "Formulate 3–4 initiatives as: «**First driver** — …», «**Second driver** — …», then "
        "«Key directions» (bullets) and a step-by-step effect calculation. Data — the pack "
        "sections options, leader's choice and initiatives. Close with an inference-conclusion.",
    "Юнит-экономика — расчёт пошагово:": "Unit economics — step-by-step:",
    "## FAQ-4. Тактики. Детализируйте каждую инициативу до конкретных тактик.":
        "## FAQ-4. Tactics. Detail each initiative into concrete tactics.",
    "Матрица тактик (раздел «Инициативы» пакета данных):":
        "Tactics matrix (the pack's initiatives section):",
    "Матрица тактик (заполните):": "Tactics matrix (fill in):",
    "| Инициатива 1 | … | … | … |": "| Initiative 1 | … | … | … |",
    "| Инициатива 2 | … | … | … |": "| Initiative 2 | … | … | … |",
    "## FAQ-5. Высокоуровневый план реализации": "## FAQ-5. High-level implementation plan",
    "Ожидаемое распределение вклада инициатив в общий результат (сумма 100%):":
        "Expected contribution of initiatives to the outcome (must sum to 100%):",
    "- __% — Инициатива 1;": "- __% — Initiative 1;",
    "- __% — Инициатива 2;": "- __% — Initiative 2;",
    "- __% — Инициатива 3.": "- __% — Initiative 3.",
    "Порядок тактик: высокий → средний → базовый приоритет. Тайминг — к сезонам рынка. "
    "Параллельные треки: комьюнити/партнёрства — вне основной линии.":
        "Tactic order: high → medium → base priority. Timing follows market seasons. Parallel "
        "tracks: community/partnerships — off the main line.",
    "## FAQ-6. Метрики успеха. KPI в двух плоскостях":
        "## FAQ-6. Success metrics. KPIs in two dimensions",
    "> Добавьте метрики успеха в 04/06 документы: явная таблица «KPI» "
    "(Плоскость | Метрика | Формула | База | Цель к сроку | Порог | "
    "Контр-метрика) в 06_validation_plan.md — две таблицы (Бизнес/Продукт) "
    "соберутся автоматически.":
        "> Add success metrics to the 04/06 documents: the explicit KPI table "
        "(Plane | Metric | Formula | Baseline | Target by deadline | Threshold | "
        "Counter-metric) in 06_validation_plan.md assembles the two tables "
        "(Business/Product) automatically.",
    "## Источники (сноски)": "## Sources (footnotes)",
    "## Приложения (Excel)": "## Appendices (Excel)",
    "> Ещё нет: `pfs calc all`.":
        "> Appendices are built by `pfs calc all` into outputs/attachments/: unit_economics.xlsx, "
        "growth_model.xlsx, cohort_retention.xlsx, market_sizing.xlsx. Formulas recalculate on "
        "open (Excel / Numbers / LibreOffice); the input sheet inside each workbook carries RU "
        "labels — edit the values there.",
    "> Формулы пересчитываются при открытии (Excel / Numbers / LibreOffice). "
    "Детализация по спецификации — knowledge/templates/SIX_PAGER_PROMPT.md. "
    "Полная версия с доказательствами — REPORT.md.":
        "> Formulas recalculate on open (Excel / Numbers / LibreOffice). Detailing per the "
        "spec: knowledge/templates/SIX_PAGER_PROMPT_EN.md. Full evidence version — REPORT.md.",
    # юнит-экономика — все записи ниже живые: их читает _unit_econ_block (таблица формул
    # и чувствительность); записей-синонимов (ключ → тот же ключ) здесь нет.
    "Допущения: {note}": "Assumptions: {note}",
    "Допущения [укажите теги]: ARPU, переменные, CAC, churn — лист «Ввод» unit_economics.xlsx.":
        "Assumptions [add C-tags]: ARPU, variable costs, CAC, churn — the input sheet of "
        "unit_economics.xlsx.",
    "| Формула | Расчёт | Результат |": "| Formula | Calculation | Result |",
    "CM = ARPU × (1 − доля переменных)": "CM = ARPU × (1 − variable share)",
    "Средняя жизнь платящего = 1 / churn": "Average paying lifetime = 1 / churn",
    "**{x} мес**": "**{x} mo**",
    "**{x}** (критерий ≥ 3)": "**{x}** (target ≥ 3)",
    "Окупаемость CAC = CAC / CM": "CAC payback = CAC / CM",
    "**Вывод (умозаключение):** LTV/CAC ≥ 3 держится до churn ≈ {churn} %/мес, "
    "до CAC ≈ €{cac}, до доли переменных расходов ≈ {vc} % "
    "(каждый порог — при прочих равных; сетка — лист «Чувствительность»).":
        "**Conclusion (inference):** LTV/CAC ≥ 3 holds up to churn ≈ {churn} %/mo, "
        "CAC ≈ €{cac}, variable-cost share ≈ {vc} % "
        "(each threshold — all else equal; grid — the sensitivity sheet).",
    "**Вывод (умозаключение):** запас прочности модели — какой допуск выдерживает "
    "каждое допущение (см. лист «Чувствительность»).":
        "**Conclusion (inference):** safety margin — which deviation each assumption survives "
        "(see the sensitivity sheet).",
    # решение
    "**Решение {did}** — {title}.": "**Decision {did}** — {title}.",
    " Обязательство: {commit}.": " Commitment: {commit}.",
    "промежуточный пересмотр {date}; триггер: {trig}": "interim review {date}; trigger: {trig}",
    "промежуточный пересмотр {date}": "interim review {date}",
    # матрица тактик и KPI
    "| Стратегическая инициатива | Фокус | Потребности и ожидания пользователя | Решения (тактики) |":
        "| Strategic initiative | Focus | User needs and expectations | Solutions (tactics) |",
    " **Результат:** {gate}": " **Outcome:** {gate}",
    "| Метрика | Формула | База (дата, источник) | Цель к сроку | "
    "Порог действия (остановить) | Контр-метрика |":
        "| Metric | Formula | Baseline (date, source) | Target by deadline | "
        "Action threshold (stop) | Counter-metric |",
    "Бизнес": "Business",
    "Продукт": "Product",
}


def _t(s: str, lang: str = "ru") -> str:
    """Строка скелета six-pager: RU как есть, EN — из словаря _EN (нет записи — RU как есть)."""
    return _EN.get(s, s) if lang == "en" else s


RU_SOURCE = core.RU_SOURCE_MARK


def _en_pending(what: str) -> str:
    """PRO-53: pending-строка EN-каркаса. EN-версия six-pager пишется, а не переводится:
    секцию составляет six-pager-writer на английском из пакета данных
    (outputs/six_pager_pack.md: утверждения, источники, расчёты); документы 00–07 —
    RU-вход пакета, в EN не вставляется. Префикс EN_DRAFT_MARK распознаёт черновик
    в линтере и сверке тегов RU↔EN."""
    return (f"{core.EN_DRAFT_MARK}: write this section in English from the data package "
            f"outputs/six_pager_pack.md ({what}); spec: knowledge/templates/SIX_PAGER_PROMPT_EN.md, "
            f"style: knowledge/templates/STYLE_EN.md.")


def _unit_econ_block(pdir: Path, lang: str = "ru") -> str | None:
    """Пошаговая юнит-экономика из calcs.json (unit_econ): CM, LTV, LTV/CAC, окупаемость.
    PRO-51: расчёт из того же unit_metrics, что и Excel, — ARPU средневзвешенный по tiers,
    freemium учитывает CAC платящего; числа six-pager обязаны совпадать с приложением."""
    cfg = core.read_json(pdir / "calcs.json", {}).get("unit_econ") or {}
    ue = {k: v for k, v in cfg.items() if not k.startswith("_") and v is not None}
    m = calc.unit_metrics(ue)
    arpu, vc = m.get("arpu"), ue.get("vc_share")
    cac, churn = m.get("cac"), ue.get("churn_month")
    if not all(isinstance(v, (int, float)) for v in (arpu, vc, cac, churn)) \
            or not arpu or not churn or not cac:
        return None

    def n(x: float) -> str:
        # RU: десятичная запятая; EN (PRO-53): 1,234.5 — точка-разделитель, запятая — тысячи
        return f"{x:,.2f}" if lang == "en" else f"{x:.2f}".replace(".", ",")

    cr = m.get("cr_free_paid")
    cac_eff = m["cac_paying"] if cr else cac
    cm, ltv = m["cm"], m["ltv"]
    ratio, payback, life = m["ltv_cac"], m["payback"], m["life"]
    rows = [
        (_t("CM = ARPU × (1 − доля переменных)", lang),
         f"{n(arpu)} × (1 − {n(vc)}) = {n(arpu)} × {n(1 - vc)}", f"**CM = {n(cm)}**"),
        (_t("Средняя жизнь платящего = 1 / churn", lang), f"1 / {n(churn)}",
         _t("**{x} мес**", lang).format(x=n(life))),
    ]
    if cr is not None:  # PRO-51: freemium — конверсия free→paid реально применяется
        rows.append((_t("CAC платящего = CAC / конверсия free → paid", lang),
                     f"{n(cac)} / {n(cr)}", f"**{n(cac_eff)}**"))
    rows += [
        (_t("LTV = CM / churn", lang), f"{n(cm)} / {n(churn)}", f"**LTV = {n(ltv)}**"),
        (_t("LTV/CAC", lang), f"{n(ltv)} / {n(cac_eff)}",
         _t("**{x}** (критерий ≥ 3)", lang).format(x=n(ratio))),
        (_t("Окупаемость CAC = CAC / CM", lang), f"{n(cac_eff)} / {n(cm)}",
         _t("**{x} мес**", lang).format(x=n(payback))),
    ]
    table = _t("| Формула | Расчёт | Результат |", lang) + "\n|---|---|---|\n" + \
        "\n".join(f"| {f} | {c} | {r} |" for f, c, r in rows)
    note = _flat(cfg.get("note"))
    head = (_t("Допущения: {note}", lang).format(note=note) if note else
            _t("Допущения [укажите теги]: ARPU, переменные, CAC, churn — лист «Ввод» unit_economics.xlsx.", lang))
    tiers = [t for t in (ue.get("tiers") or []) if isinstance(t, dict)]
    if tiers:  # PRO-51: объяснённый микс тарифов вместо цены топ-тарифа
        mix = " + ".join(f"{t.get('name')} {n(t.get('price') or 0)} × {n((t.get('share') or 0) * 100)}%"
                         for t in tiers)
        head += "\n" + _t("ARPU средневзвешенный по тарифам", lang) + f": {mix} = **{n(arpu)}**."
    # Чувствительность к критерию LTV/CAC ≥ 3: порог по каждому допущению при прочих равных.
    if cm > 0 and ltv > 0 and ratio is not None and ratio >= 3:
        sens = _t("**Вывод (умозаключение):** LTV/CAC ≥ 3 держится до churn ≈ {churn} %/мес, "
                  "до CAC ≈ €{cac}, до доли переменных расходов ≈ {vc} % "
                  "(каждый порог — при прочих равных; сетка — лист «Чувствительность»).",
                  lang).format(churn=n(cm / (3 * cac_eff) * 100), cac=n(ltv / 3),
                               vc=n((1 - 3 * cac_eff / ltv) * 100))
    elif ratio is not None:  # PRO-51: честный вывод, когда критерий не выполняется
        sens = _t("**Вывод (умозаключение):** критерий LTV/CAC ≥ 3 не выполняется: фактический "
                  "{ratio} при CAC платящего {cac} — для ≥ 3 нужен CAC платящего ≤ {cap} при этом LTV "
                  "(сценарии и сетка — листы «Сценарии» и «Чувствительность» unit_economics.xlsx).",
                  lang).format(ratio=n(ratio), cac=n(cac_eff), cap=n(ltv / 3))
    else:
        sens = _t("**Вывод (умозаключение):** запас прочности модели — какой допуск выдерживает "
                  "каждое допущение (см. лист «Чувствительность»).", lang)
    return f"{head}\n\n{table}\n\n{sens}"


def _decision_block(pdir: Path, lang: str = "ru") -> str | None:
    """Последнее зафиксированное решение D### — обязательство, срок, пересмотр."""
    rows = core.read_jsonl(pdir / "decisions.jsonl")
    if not rows:
        return None
    d = rows[-1]
    did = d.get("id", "D###")
    title = _flat(d.get("title"))
    commit = _flat(d.get("commitment"))
    rv = d.get("review")
    if isinstance(rv, dict):
        date = _flat(rv.get("date"))
        trig = _flat(rv.get("triggers") or rv.get("trigger"))
        review = _t("промежуточный пересмотр {date}; триггер: {trig}", lang).format(date=date, trig=trig) \
            if trig else _t("промежуточный пересмотр {date}", lang).format(date=date)
    else:
        review = _flat(rv)
    out = _t("**Решение {did}** — {title}.", lang).format(did=did, title=title)
    if commit:
        out += _t(" Обязательство: {commit}.", lang).format(commit=commit)
    if review:
        out += f" {review[0].upper() + review[1:]}."
    return out


def _table_rows(text: str, headers: tuple[str, ...]) -> list[list[str]]:
    """Строки markdown-таблицы, чья шапка содержит колонки headers подряд и по порядку.
    Разделитель |---| пропускается; строка с другим числом колонок заканчивает таблицу."""
    want = [_norm_title(h) for h in headers]
    rows: list[list[str]] = []
    header_seen, width = False, 0
    for ln in text.splitlines():
        if not ln.strip().startswith("|"):
            if header_seen and rows:
                break
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if all(set(c) <= set("-: ") for c in cells):
            continue
        if not header_seen:
            norm = [_norm_title(c) for c in cells]
            for k in range(len(norm) - len(want) + 1):
                if norm[k:k + len(want)] == want:
                    header_seen, width = True, len(cells)
                    break
            continue
        if len(cells) != width:
            break
        rows.append(cells)
    return rows


_KPI_COLS = ("Плоскость", "Метрика", "Формула", "База", "Цель к сроку",
             "Порог действия", "Контр-метрика")
_KPI_HEAD = ("| Метрика | Формула | База (дата, источник) | Цель к сроку | "
             "Порог действия (остановить) | Контр-метрика |")


def _kpi_rows(pdir: Path) -> dict[str, list[list[str]]]:
    """Строки ЯВНОЙ сводной таблицы «KPI» 06_validation_plan.md без столбца-источника
    «Плоскость»: {плоскость: строки}. Плоскость задаётся автором таблицы, а не
    угадывается по словам метрики (PRO-48). Таблицы нет — {}."""
    fname = "06_validation_plan.md"
    path = pdir / "outputs" / fname
    if not path.exists():
        return {}
    rows = [r for r in _table_rows(path.read_text(encoding="utf-8"), _KPI_COLS)
            if len(r) == len(_KPI_COLS) and all(c.strip() for c in r)]
    planes = {p: [r[1:] for r in rows if _norm_title(r[0]) == _norm_title(p)]
              for p in ("Бизнес", "Продукт")}
    return {p: rs for p, rs in planes.items() if rs}


def _kpi_table(pdir: Path, lang: str = "ru") -> str | None:
    """KPI в двух плоскостях (Бизнес/Продукт) из ЯВНОЙ сводной таблицы «KPI»
    06_validation_plan.md (строки — _kpi_rows): плоскость задаётся автором,
    а не угадывается по словам метрики (PRO-48). У каждой метрики — формула, база
    с датой и источником, цель со сроком, порог действия и контр-метрика; база и
    цель — раздельные ячейки. Вывод — две таблицы без столбца-источника; битые
    строки и чужие плоскости пропускаются. Таблицы нет — None: гипотезы H1…H5
    KPI не подменяют."""
    planes = _kpi_rows(pdir)
    if not planes:
        return None

    def cell(s: str) -> str:
        return s.replace("|", "/")

    sep = "|---|---|---|---|---|---|"
    out: list[str] = []
    for plane, rs in planes.items():
        out += [f"**{_t(plane, lang)}**", "", _t(_KPI_HEAD, lang), sep]
        out += ["| " + " | ".join(cell(c) for c in r) + " |" for r in rs]
        out.append("")
    while out and not out[-1]:
        out.pop()
    return "\n".join(out)


_INITIATIVE = re.compile(r"^-\s*\*\*(.+?):\*\*\s*(.+)$")
_INITIATIVE_WORDS = ("инициатив", "драйвер")
_JTBD = re.compile(r"JTBD[:\s]*«([^»]+)»")


def _user_needs(pdir: Path) -> str | None:
    """Барьер пользователя словами пользователя — хвост JTBD после «—»
    («… резюме, которое пройдёт ATS — без ручной рутины и доверия данным облаку»);
    02_situation.md, затем 04_product_strategy.md. Нет JTBD или барьера — None."""
    for fname in ("02_situation.md", "04_product_strategy.md"):
        path = pdir / "outputs" / fname
        if not path.exists():
            continue
        m = _JTBD.search(path.read_text(encoding="utf-8"))
        if not m:
            continue
        parts = [p.strip(" .") for p in re.split(r"\s*—\s*", m.group(1)) if p.strip(" .")]
        if len(parts) > 1 and parts[-1]:
            return parts[-1]
    return None


def _initiative_groups(pdir: Path) -> list[dict]:
    """Инициативы Outcome-роадмапа 04_product_strategy.md как ДАННЫЕ пакета: буллеты вида
    «- **Инициатива N — фокус (тайминг):** тактика; тактика. **Результат …:** гейт»
    → [{name, focus, tactics, gate}]. Сырые данные без валидации полноты — её делает
    _tactics_matrix; пакет несёт всё, что удалось разобрать (PRO-46)."""
    path = pdir / "outputs" / "04_product_strategy.md"
    if not path.exists():
        return []
    groups: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = _INITIATIVE.match(line.strip())
        if not m:
            continue
        label, body = m.group(1).strip(), m.group(2).strip()
        norm = _norm_title(label)
        if not (norm.startswith("этап") or any(w in norm for w in _INITIATIVE_WORDS)):
            continue
        parts = re.split(r"\*\*Результат[^*]*\*\*:?\s*", body, maxsplit=1)
        gate = parts[1].strip() if len(parts) > 1 else ""
        tactics = [t.strip(" .") for t in parts[0].split(";") if t.strip(" .")]
        if "—" in label:
            name, _, tail = label.partition("—")
            name, focus = name.strip(), re.sub(r"\([^)]*\)", "", tail).strip(" .")
        elif gate:  # «Этап N» без «—»: фокус — результат-гейт
            name, focus = label, re.sub(r"^Результат[^:]*:\s*", "", gate).strip(" .")
        else:
            # Ни «—» в заголовке, ни гейта — фокус взять неоткуда; fallback на
            # первую тактику давал бы Фокус, идентичный «Решения» (ревью PRO-48).
            name, focus = label, ""
        groups.append({"name": name, "focus": focus, "tactics": tactics, "gate": gate})
    return groups


def _tactics_matrix(pdir: Path, lang: str = "ru") -> str | None:
    """Матрица тактик FAQ-4 из групп _initiative_groups (Outcome-роадмапа
    04_product_strategy.md): канонические колонки «Инициатива | Фокус | Потребности |
    Решения» (эталон FAQ-4): одна исполняемая тактика в строке, 2–4 строки на
    инициативу (излишек склеивается в четвёртую строку, гейт-результат — в последнюю,
    если он ещё не показан в Фокусе). Фокус — направление из заголовка без тайминга;
    у «Этап N» без «—» — результат-гейт. Потребности — барьер из JTBD (02, затем 04)
    словами пользователя. Честные заглушки (ревью PRO-48): нет JTBD, меньше двух
    инициатив, у какой-то инициативы нет фокуса (ни «—» в заголовке, ни гейта) или
    меньше двух тактик — None: дырявую матрицу, где инициатива пропала молча,
    не собираем."""
    needs = _user_needs(pdir)
    if not needs:
        return None
    groups = _initiative_groups(pdir)
    if len(groups) < 2:
        return None
    # Ревью PRO-48: дырявую матрицу не собираем. Инициатива без фокуса или с
    # одной тактикой не выбрасывается молча — «на каждую инициативу FAQ-3
    # от 2 до 4 строк» либо у всех инициатив, либо честная заглушка.
    if any(not g["focus"].strip(" .") or len(g["tactics"]) < 2 for g in groups):
        return None

    def cell(s: str) -> str:
        return s.replace("|", "/")

    out = [_t("| Стратегическая инициатива | Фокус | Потребности и ожидания пользователя | Решения (тактики) |", lang),
           "|---|---|---|---|"]
    for g in groups:
        name, focus, tactics, gate = g["name"], g["focus"], g["tactics"], g["gate"]
        shown = tactics if len(tactics) <= 4 else tactics[:3] + ["; ".join(tactics[3:])]
        tail_gate = bool(gate) and gate.strip(" .") != focus.strip(" .")  # пустой гейт и гейт = фокус — не дублируем
        for i, tactic in enumerate(shown):
            solutions = tactic
            if tail_gate and i == len(shown) - 1:
                solutions += _t(" **Результат:** {gate}", lang).format(gate=gate)
            out.append(f"| {cell(name)} | {cell(focus)} | {cell(needs)} | {cell(solutions)} |")
    return "\n".join(out)


# PRO-46: слот каркаса — один маркер на репозиторий (core.SIX_PAGER_SLOT_MARK):
# его же ищет сверка RU↔EN в check.py — пока RU не написан, «отставание» EN бессмысленно.
SLOT_MARK = core.SIX_PAGER_SLOT_MARK


def _slot(what: str) -> str:
    """Слот каркаса RU six-pager (PRO-46): раздел дописывает субагент six-pager-writer
    из пакета данных. «заполните» — не небрежность, а маркер: линтер (`pfs check
    --six-pager`) держит каркас со слотами в ошибках, поэтому цикл «написать →
    исправить до 0 ошибок» нельзя пропустить. Рабочие документы в six-pager
    не вставляются — их данные уже в пакете."""
    return (f"{SLOT_MARK} {what} Данные — разделы пакета `outputs/six_pager_pack.md`; "
            "спецификация — `knowledge/templates/SIX_PAGER_PROMPT.md`; рабочие документы "
            "не вставляются.")


def build_six_pager(pdir: Path, with_calcs: bool = True, lang: str = "ru") -> Path:
    """PRO-46: six-pager собирается в два шага. Шаг инструмента — пакет данных и каркас:
    `outputs/six_pager_pack.json` (читаемая версия `six_pager_pack.md`,
    build_six_pager_pack) — утверждения с силой A–D, источники, расчёты из calcs,
    варианты, выбор руководителя, инициативы, KPI, решения; `outputs/SIX_PAGER.md` —
    каркас FAQ-1…6 со слотами (_slot) и расчётными артефактами: юнит-экономика из
    calcs, матрица тактик из Outcome-роадмапа, KPI-таблицы из явной таблицы 06,
    решение D### с обязательством. Рабочие документы 02/03/04/06 НЕ вставляются —
    полная версия с доказательствами в REPORT.md. Текст по слотам пишет субагент
    six-pager-writer (модель уровня deep) по спецификации
    knowledge/templates/SIX_PAGER_PROMPT.md, затем обязательный цикл:
    `pfs check --six-pager` → правки → 0 ошибок. Сноски-источники (PRO-49) —
    теги [C###]/[S###] расчётных артефактов заменяются сквозными [^N]; полный
    реестр тегов — REPORT.md.
    lang="en" (PRO-53) — EN-версия пишется, а не переводится: каркас на английском
    с pending-строками (_en_pending); секции составляет six-pager-writer
    на английском из того же пакета данных (спецификация SIX_PAGER_PROMPT_EN.md,
    стиль STYLE_EN.md), RU-контент не вставляется,
    числа — EN-формат (1,234.5) → outputs/SIX_PAGER_EN.md."""
    if with_calcs:
        calc.run(pdir, "all")
    meta = core.read_json(pdir / "project.json", {})
    build_six_pager_pack(pdir)  # пакет данных — вход писателя (RU и EN — один пакет)
    parts = [_t("# {title}: six-pager", lang).format(title=meta.get("title")), "",
             _t("> Каркас и пакет данных собраны {ts} командой `pfs export --six-pager`. "
                "Текст по слотам пишет субагент `six-pager-writer` из пакета данных "
                "(`outputs/six_pager_pack.json`, читаемая версия — `six_pager_pack.md`) "
                "по спецификации `knowledge/templates/SIX_PAGER_PROMPT.md`; рабочие "
                "документы 02–07 не вставляются — полная версия с доказательствами "
                "в REPORT.md. Обязательный цикл: написать → `pfs check --six-pager` → "
                "исправить до 0 ошибок. Числа — со сносками; теги C###/S### и полный "
                "реестр доказательств — REPORT.md.",
                lang).format(ts=core.now()[:16]), "",
             _t("**Запрос:** {q}", lang).format(q=meta.get("question", "")), ""]
    faq1 = _en_pending("pack sections: situation (market, known facts, contradictions, "
                       "unknowns) plus the claims and sources lists") if lang == "en" else \
        _slot("Обзор рынка: объём и динамика — диапазонами со сноской, прогноз буллетами "
              "по годам, 5–7 ключевых трендов буллетами с жирными заголовками и следствием "
              "для продукта.")
    parts += [_t("## FAQ-1. Анализ текущего состояния", lang), "",
              _t("### 1.1 Обзор рынка: тренды, вызовы и возможности", lang), "",
              faq1, "",
              _t("### 1.2 Ключевые конкуренты и анализ их стратегий роста и промо-механик", lang), "",
              (_en_pending("pack situation — competitor groups; risks rated High/Medium/Low")
               if lang == "en" else
               _slot("Таблица групп конкурентов: ключевые преимущества, стратегии роста "
                     "и промо-механики, риски с оценкой Высокий/Средний/Низкий; ниже — "
                     "абзац «чего не хватает никому» (пробел = окно стратегии).")), "",
              _t("Сравнительная таблица групп конкурентов (заполните после конкурентного анализа):", lang), "",
              _t("| | Группа 1 | Группа 2 | Группа 3 |", lang),
              "|---|---|---|---|",
              _t("| **Ключевые преимущества** | … | … | … |", lang),
              _t("| **Стратегия роста и промо-механики** | … | … | … |", lang),
              _t("| **Риски для компании** | … — Высокий/Средний/Низкий | … | … |", lang), "",
              _t("> **Вывод (умозаключение):** окно возможностей и его срок — заполните по данным 1.1–1.2.", lang), ""]
    faq2 = _en_pending("pack situation — segments/personas and the JTBD user barrier") \
        if lang == "en" else \
        _slot("Таблица персон по барьеру входа (не по профессии) и обоснование "
              "приоритизации сегментов с расчётом (ёмкость/CAC/конкуренция).")
    parts += [_t("## FAQ-2. User Persona. Кто является целевой аудиторией?", lang), "",
              _t("### 2.1 Сегменты", lang), "",
              faq2, "",
              _t("Таблица персон (заполните):", lang), "",
              _t("| | Сегмент 1 | Сегмент 2 | Сегмент 3 |", lang),
              "|---|---|---|---|",
              _t("| **Кто они?** | … | … | … |", lang),
              _t("| **Что используют сегодня и почему?** | … | … | … |", lang),
              _t("| **С какими трудностями сталкиваются?** | … | … | … |", lang),
              _t("| **Общие трудности** | … | … |", lang), "",
              _t("### 2.2 Барьеры на каждом этапе пути", lang), "",
              (_en_pending("pack situation — barriers per journey stage, hold-backs per segment")
               if lang == "en" else
               _slot("Барьеры на каждом этапе пути (привлечение → выбор → оплата → "
                     "постоплатный опыт) и «что сдерживает от старта или продления» "
                     "по каждому сегменту: фактор → чем снимается.")), "",
              _t("| Этап пути | Барьер сегодня | Что делает продукт |", lang),
              "|---|---|---|",
              _t("| Привлечение | … | … |", lang),
              _t("| Выбор / использование | … | … |", lang),
              _t("| Оплата | … | … |", lang),
              _t("| Постоплатный опыт | … | … |", lang), "",
              _t("Что сдерживает от старта или продления? (заполните по сегментам):", lang), "",
              _t("| Сегмент | Сдерживающий фактор | Чем снимается |", lang),
              "|---|---|---|",
              _t("| Сегмент 1 | … | … |", lang), "",
              _t("> **Вывод (умозаключение):** сегментация по барьеру входа; лестница тиров "
                 "обслуживает все барьеры; приоритизация — по ёмкости/CAC/конкуренции (расчёт — выше).", lang), ""]
    faq3 = _en_pending("pack sections options, leader's choice and initiatives: chosen "
                       "direction, red-team objections, 3–4 driver initiatives") \
        if lang == "en" else \
        _slot("Вводная: из каких вариантов выбрано направление и почему (с разбором "
              "сильных возражений red team); затем 3–4 инициативы-драйвера — подпункт "
              "3.N на каждую: «**Первый драйвер** — …», ключевые направления, расчёт "
              "эффекта, ответ на самое сильное возражение.")
    parts += [_t("## FAQ-3. Стратегические инициативы. Кратко обоснуйте каждую.", lang), "",
              faq3, "",
              _t("### Инициативы выбранного направления (драйверы)", lang), "",
              _t("Сформулируйте 3–4 инициативы по схеме: «**Первый драйвер** — …», «**Второй драйвер** — …», "
                 "далее «Ключевые направления» (буллеты) и пошаговый расчёт эффекта. Данные — разделы "
                 "«Варианты», «Выбор руководителя» и «Инициативы» пакета. Закройте "
                 "выводом-умозаключением.", lang), ""]
    ue = _unit_econ_block(pdir, lang)
    if ue:
        parts += [_t("Юнит-экономика — расчёт пошагово:", lang), "", ue, ""]
    faq4 = _en_pending("pack initiatives (focus, tactics, gates) — the tactics matrix") \
        if lang == "en" else \
        _slot("Матрица тактик: на каждую инициативу 2–4 строки — фокус → потребности "
              "пользователя → исполняемые тактики (что именно строится/меняется, "
              "не лозунги).")
    matrix = None if lang == "en" else _tactics_matrix(pdir, lang)
    parts += [_t("## FAQ-4. Тактики. Детализируйте каждую инициативу до конкретных тактик.", lang), "",
              faq4, ""]
    if matrix:
        parts += [_t("Матрица тактик (раздел «Инициативы» пакета данных):", lang), "", matrix, ""]
    else:
        parts += [_t("Матрица тактик (заполните):", lang), "",
                  _t("| Стратегическая инициатива | Фокус | Потребности и ожидания пользователя | Решения (тактики) |", lang),
                  "|---|---|---|---|",
                  _t("| Инициатива 1 | … | … | … |", lang),
                  _t("| Инициатива 2 | … | … | … |", lang), ""]
    kpi = None if lang == "en" else _kpi_table(pdir, lang)
    faq5 = _en_pending("pack sections decisions, leader's choice and initiatives — "
                       "order, season timing, parallel tracks") \
        if lang == "en" else \
        _slot("Порядок реализации тактик (высокий → средний → базовый приоритет), "
              "тайминг к сезонам рынка (запуск встречает сезон с накопленной "
              "статистикой), параллельные треки — вне основной линии.")
    parts += [_t("## FAQ-5. Высокоуровневый план реализации", lang), "",
              faq5, "",
              _t("Ожидаемое распределение вклада инициатив в общий результат (сумма 100%):", lang), "",
              _t("- __% — Инициатива 1;", lang),
              _t("- __% — Инициатива 2;", lang),
              _t("- __% — Инициатива 3.", lang), "",
              _t("Порядок тактик: высокий → средний → базовый приоритет. Тайминг — к сезонам рынка. "
                 "Параллельные треки: комьюнити/партнёрства — вне основной линии.", lang), ""]
    dec = None if lang == "en" else _decision_block(pdir, lang)
    if dec:
        parts += [dec, ""]
    faq6 = _en_pending("pack sections KPI and calculations — business and product planes, "
                       "counter-metrics per red-team hit") \
        if lang == "en" else \
        _slot("KPI в двух плоскостях (бизнес — деньги и база; продукт — активация, "
              "время до ценности, churn, CSAT/NPS): у каждой метрики база → цель "
              "к сроку → порог действия; контр-метрики по ударам red team с порогами "
              "тревоги и записанным действием.")
    parts += [_t("## FAQ-6. Метрики успеха. KPI в двух плоскостях", lang), "",
              faq6, ""]
    if kpi:
        parts += [kpi, ""]
    elif lang != "en":
        parts += [_t("> Добавьте метрики успеха в 04/06 документы: явная таблица «KPI» "
                     "(Плоскость | Метрика | Формула | База | Цель к сроку | Порог | "
                     "Контр-метрика) в 06_validation_plan.md — две таблицы (Бизнес/Продукт) "
                     "соберутся автоматически.", lang), ""]
    body = "\n".join(parts)
    foot = None
    if lang != "en":  # PRO-49: в RU six-pager теги → сквозные сноски; EN-версию пишет writer
        body, foot = _footnote_plan(pdir, body)
    parts = [body, "", _t("## Источники (сноски)", lang), ""]
    if lang == "en":
        parts += [_en_pending("source footnotes by first mention: publisher, title, "
                              "date, URL, grade A–D; cited sources only; synthetic listed "
                              "separately (hypotheses, not evidence)"), ""]
    else:
        parts += [foot or _t("> Нет процитированных источников: проставьте теги [C###] в документах "
                             "00–07 и пересоберите six-pager.", lang), ""]
    appendix = attachments_table(pdir) if lang != "en" else None
    parts += [_t("## Приложения (Excel)", lang), "",
              appendix or _t("> Ещё нет: `pfs calc all`.", lang), "",
              "", _t("> Формулы пересчитываются при открытии (Excel / Numbers / LibreOffice). "
                     "Детализация по спецификации — knowledge/templates/SIX_PAGER_PROMPT.md. "
                     "Полная версия с доказательствами — REPORT.md.", lang)]
    path = pdir / "outputs" / ("SIX_PAGER_EN.md" if lang == "en" else "SIX_PAGER.md")
    core.atomic_write(path, "\n".join(parts) + "\n")
    core.log(pdir, "action", f"Собран outputs/{path.name} и пакет данных six_pager_pack "
                             "(PRO-46: каркас со слотами, документы не вставляются)",
             tool="pfs export --six-pager")
    return path


_MAX_POINTS = 6   # тезисов на слайд
_POINT_CAP = 160  # символов на тезис

_DECK_CSS = """
  :root { --bg: #070b13; --fg: #e8eef8; --a1: #4fd1c5; --a2: #8b7bff; --dim: #9aa7bd; }
  * { box-sizing: border-box; }
  html { scroll-snap-type: y mandatory; }
  body { margin: 0; background: var(--bg); color: var(--fg);
         font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; }
  section.slide { width: 100vw; height: auto; aspect-ratio: 16/9; min-height: 100vh;
                  max-height: 100vh; scroll-snap-align: start; scroll-snap-stop: always;
                  display: flex; flex-direction: column; justify-content: center; gap: .6em;
                  padding: clamp(24px, 6vw, 80px); overflow: hidden;
                  border-bottom: 1px solid rgba(139, 123, 255, .18); }
  h1, h2 { margin: 0; line-height: 1.15; font-weight: 700;
           background: linear-gradient(90deg, var(--a1), var(--a2));
           -webkit-background-clip: text; background-clip: text; color: transparent; }
  h1 { font-size: clamp(28px, 5vw, 56px); }
  h2 { font-size: clamp(22px, 3.6vw, 40px); }
  ul { margin: 0; padding-left: 1.2em; display: flex; flex-direction: column; gap: .45em;
       font-size: clamp(15px, 2vw, 24px); }
  li::marker { color: var(--a1); }
  p { margin: 0; font-size: clamp(15px, 2vw, 24px); color: var(--fg); }
  .query { color: var(--dim); font-size: clamp(16px, 2.2vw, 26px); }
  .query b { color: var(--a1); }
"""


def _slide(title: str, points: list[str], cls: str = "") -> str:
    """Секция-слайд: заголовок + один тезис — один пункт."""
    body = ""
    if points:
        items = "".join(f"<li>{html_mod.escape(p)}</li>" for p in points)
        body = f"<ul>{items}</ul>"
    k = f' class="{cls}"' if cls else ""
    return f'<section class="slide"{k}>\n<h2>{html_mod.escape(title)}</h2>\n{body}\n</section>'


def _points(body: str) -> list[str]:
    """Тезисы слайда: маркеры списков и первые предложения абзацев (≤6, ≤160 символов)."""
    pts: list[str] = []
    for raw in body.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or set(line) <= set("-|: "):
            continue
        if line.startswith("|"):  # строка таблицы — первый столбец
            line = [c.strip() for c in line.strip("|").split("|")][0]
        line = re.sub(r"^[-*+]\s+", "", line)
        line = re.sub(r"^>\s?", "", line)
        if line.startswith("[^"):  # PRO-49: определения сносок — не тезисы
            continue
        line = re.sub(r"\[\^\d+\]", "", line)  # PRO-49: маркеры сносок — не тезисы
        sentence = re.split(r"(?<=[.!?…])\s+", line)[0]
        if len(sentence) > _POINT_CAP:
            sentence = sentence[:_POINT_CAP - 1].rstrip() + "…"
        if sentence and (not pts or sentence != pts[-1]):
            pts.append(sentence)
        if len(pts) >= _MAX_POINTS:
            break
    return pts



def build_deck(pdir: Path) -> Path:
    """HTML-дека 16:9 из outputs/SIX_PAGER.md (тёмная тема, один тезис на слайд)."""
    src = pdir / "outputs" / "SIX_PAGER.md"
    if not src.exists():
        raise core.PfsError("Сначала соберите six-pager: pfs export --six-pager")
    text = src.read_text(encoding="utf-8")
    meta = core.read_json(pdir / "project.json", {})
    q = re.search(r"^\*\*Запрос:\*\*\s*(.+)$", text, flags=re.M)
    query = q.group(1).strip() if q else meta.get("question", "")
    h1 = re.search(r"^#\s+(.+)$", text, flags=re.M)
    title = h1.group(1).strip() if h1 else meta.get("title", "Six-pager")
    sections = re.split(r"^##\s+", text, flags=re.M)[1:]
    slides = ['<section class="slide title-slide">\n'
              f"<h1>{html_mod.escape(title)}</h1>\n"
              f'<p class="query"><b>Запрос:</b> {html_mod.escape(query)}</p>\n</section>']
    for sec in sections:
        head, _, body = sec.partition("\n")
        head = head.strip()
        if head:
            slides.append(_slide(head, _points(body)))
    doc = ("<!doctype html>\n<html lang=\"ru\">\n<head>\n<meta charset=\"utf-8\">\n"
           f"<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
           f"<title>{html_mod.escape(title)}</title>\n<style>{_DECK_CSS}</style>\n"
           f"</head>\n<body>\n" + "\n".join(slides) + "\n</body>\n</html>\n")
    path = pdir / "outputs" / "presentations" / "deck.html"
    core.atomic_write(path, doc)
    core.log(pdir, "action", "Собран outputs/presentations/deck.html", tool="pfs export --deck")
    return path
