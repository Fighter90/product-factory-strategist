"""Контроль качества (quality gate): проверяемость, разделение фактов и гипотез, полнота стратегии."""
from __future__ import annotations

import re
from pathlib import Path

from . import claims as claims_mod, core, gaps, i18n, review, sources as src_mod
from .impact import TAG

# PRO-26: числовой кросс-чек. Число — целое или десятичное (в т.ч. русская запятая: «8,5»);
# годы 1900–2099 — даты, а не показатели: без этого исключения любой заголовок
# «Отчёт за 2025 год» давал бы ложную тревогу с каждым числовым утверждением.
NUM_TOKEN = re.compile(r"\d+(?:[.,]\d+)?")
YEAR_TOKEN = re.compile(r"^(?:19|20)\d{2}$")


def _sections(text: str) -> list[str]:
    return [l.lstrip("#").strip().lower() for l in text.splitlines() if l.startswith("#")]


def _has_section(text: str, name: str) -> bool:
    return any(name.lower() in h for h in _sections(text))


def _section_body(text: str, name: str) -> str:
    lines, out, on, level = text.splitlines(), [], False, 0
    for l in lines:
        if l.startswith("#"):
            lvl = len(l) - len(l.lstrip("#"))
            if on and lvl <= level:
                break
            if name.lower() in l.lower():
                on, level = True, lvl
                continue
        if on:
            out.append(l)
    return "\n".join(out)


def en_sync_warnings(pdir: Path) -> list[str]:
    """Сверка тегов RU↔EN: обе версии six-pager собраны, но в RU появились теги
    (C###/S###/D###), которых в EN ещё нет — дописанный EN-документ отстал от RU и
    подлежит переписыванию (EN пишется агентом из того же пакета данных, PRO-53).
    EN нет, теги совпадают или EN — каркас-черновик (EN_DRAFT_MARK, его допишет
    writer) — предупреждений нет."""
    ru, en = pdir / "outputs" / "SIX_PAGER.md", pdir / "outputs" / "SIX_PAGER_EN.md"
    if not (ru.exists() and en.exists()):
        return []
    en_text = en.read_text(encoding="utf-8")
    if core.EN_DRAFT_MARK in en_text:
        return []
    missing = sorted(set(TAG.findall(ru.read_text(encoding="utf-8")))
                     - set(TAG.findall(en_text)),
                     key=lambda t: (t[0], int(t[1:])))
    if not missing:
        return []
    return [i18n.t(i18n.lang_of(pdir), "warn_en_sync", tags=", ".join(missing))]


# PRO-53: EN-линтер. Кириллица — любой русский символ; русская десятичная запятая —
# цифра, запятая и 1–2 цифры НЕ в составе тысячного разряда: «8,5» — нарушение,
# «42,635» (тысячи) и «1,234.5» (EN-формат) — нет.
_CYRILLIC = re.compile(r"[а-яёА-ЯЁ]")
_RU_DECIMAL = re.compile(r"\d,\d{1,2}(?!\d)")


def en_style_warnings(pdir: Path) -> list[str]:
    """PRO-53: линтер EN-вывода — в SIX_PAGER_EN.md нет кириллицы, русских десятичных
    запятых и маркера «[RU source — translate]»: EN-версия пишется по-английски из того
    же пакета данных, а не переводится (правила — knowledge/templates/STYLE_EN.md).
    Файла нет — проверять нечего; [] — чисто."""
    path = pdir / "outputs" / "SIX_PAGER_EN.md"
    if not path.exists():
        return []
    tr = lambda key, **kw: i18n.t(i18n.lang_of(pdir), key, **kw)
    lines = path.read_text(encoding="utf-8").splitlines()
    out: list[str] = []

    def hit(regex: re.Pattern, key: str) -> None:
        found = [i for i, ln in enumerate(lines, 1) if regex.search(ln)]
        if not found:
            return
        shown = ", ".join(map(str, found[:5])) + (", …" if len(found) > 5 else "")
        sample = lines[found[0] - 1].strip()[:90]
        out.append(tr(key, lines=shown, n=len(found), sample=sample))

    hit(_CYRILLIC, "warn_en_cyrillic")
    hit(_RU_DECIMAL, "warn_en_dec_comma")
    hit(re.compile(re.escape(core.RU_SOURCE_MARK)), "warn_en_translate_marker")
    return out


def _numbers(text: str) -> dict[float, str]:
    """Числа текста: {значение: как написано}. Годы исключаются (см. NUM_TOKEN)."""
    out: dict[float, str] = {}
    for m in NUM_TOKEN.finditer(text):
        raw = m.group(0)
        if not YEAR_TOKEN.match(raw):
            out.setdefault(float(raw.replace(",", ".")), raw)
    return out


def _fmt(nums: dict[float, str]) -> str:
    return ", ".join(nums[k] for k in sorted(nums))


def _source_body(pdir: Path, sid: str) -> str:
    """Тело источника sources/S###.md без служебной шапки (шапка кончается «---»):
    числа цитат сверяются с текстом источника, а не с заголовком из шапки."""
    text = (pdir / "sources" / f"{sid}.md").read_text(encoding="utf-8")
    head = text.find("\n---\n")
    return text[head:] if head != -1 else text


def numeric_warnings(pdir: Path, claims: dict[str, dict], srcs: dict[str, dict]) -> list[str]:
    """PRO-26: числовой кросс-чек реестра — ловит расхождение «заголовок 17 vs утверждение 19»,
    которое иначе доживает до финального аудита. Сообщения — на языке проекта (PRO-57).
    1) числа активного утверждения против чисел заголовка источника, на который оно ссылается:
       оба набора непусты и не пересекаются → warning с парой C###/S### (пересечение хотя бы
       по одному числу расхождением не считается — утверждение вправе содержать числа сверх заголовка);
    2) числа цитаты (quote) против текста sources/S###.md: числа, которых в тексте нет → warning."""
    tr = lambda key, **kw: i18n.t(i18n.lang_of(pdir), key, **kw)
    out: list[str] = []
    bodies: dict[str, set[float]] = {}
    for c in claims.values():
        if c["status"] != "active":
            continue
        cnums = _numbers(c["text"])
        for sid in c["sources"]:
            s = srcs.get(sid)
            if not s:
                continue
            # синтетические интервью-источники: заголовок несёт метаданные персоны
            # (возраст, город), а не числа утверждения — claim-vs-title не проверяем
            if s.get("origin") == "synthetic":
                continue
            if sid not in bodies and (pdir / "sources" / f"{sid}.md").exists():
                bodies[sid] = set(_numbers(_source_body(pdir, sid)))
            body = bodies.get(sid, set())
            tnums = _numbers(s.get("title") or "")
            if tnums and cnums and not (set(tnums) & set(cnums)):
                if set(cnums) & body:
                    # числа подтверждены текстом источника — заголовок может нести
                    # другую метрику (кейс C004/S002: звёзды vs локали), это не устаревание
                    out.append(tr("warn_num_title_mismatch", cid=c["id"], sid=sid,
                                  tnums=_fmt(tnums), cnums=_fmt(cnums)))
                else:
                    out.append(tr("warn_num_serious", cid=c["id"], sid=sid,
                                  tnums=_fmt(tnums), cnums=_fmt(cnums)))
            quote = c.get("quote")
            if quote:
                if sid in bodies:
                    missing = {v: raw for v, raw in _numbers(quote).items() if v not in bodies[sid]}
                    if missing:
                        out.append(tr("warn_quote_numbers", cid=c["id"], sid=sid, nums=_fmt(missing)))
    return out


def run(pdir: Path) -> dict:
    cfg_all = core.read_json(core.CONFIG / "quality_gate.json", {})
    # PRO-57: язык проекта выбирает блок проверок; EN-заголовки — quality_gate.json → "en".
    lang = i18n.lang_of(pdir)
    block = cfg_all.get(lang) if isinstance(cfg_all.get(lang), dict) and "documents" in cfg_all.get(lang, {}) \
        else cfg_all.get("ru", cfg_all)
    tr = lambda key, **kw: i18n.t(lang, key, **kw)
    kind_label = lambda kind: tr(f"kind_{kind}") if f"kind_{kind}" in i18n.STR.get(lang, {}) else kind
    errors: list[str] = []
    warnings: list[str] = []
    passed: list[str] = []
    claims = {c["id"]: c for c in claims_mod.load(pdir)}
    srcs = {s["id"]: s for s in src_mod.load(pdir)}
    decisions = {d["id"] for d in core.read_jsonl(pdir / "decisions.jsonl")}
    num_re = re.compile(block.get("number_regex", r"\d+%"), re.IGNORECASE)
    exempt = block.get("exempt_line_markers", [])

    # 1. Реестр утверждений
    for c in claims.values():
        if c["status"] != "active":
            continue
        if c["kind"] == "fact" and not c["sources"]:
            errors.append(tr("err_fact_no_source", cid=c["id"]))
        if c["kind"] == "fact" and c["sources"] and all(srcs.get(s, {}).get("origin") == "synthetic" for s in c["sources"]):
            errors.append(tr("err_fact_synthetic", cid=c["id"]))
        if c["kind"] == "fact" and c.get("grade") == "D":
            errors.append(tr("err_fact_grade_d", cid=c["id"]))
        stale = [d for d in c["derived_from"] if claims.get(d, {}).get("status") != "active"]
        if stale:
            warnings.append(tr("warn_stale_grounds", cid=c["id"], stale=", ".join(stale)))
        if c["kind"] in ("hypothesis", "forecast", "assumption") and not (c["sources"] or c["derived_from"]):
            warnings.append(tr("warn_no_grounds", cid=c["id"], kind=kind_label(c["kind"])))
    flagged = [s["id"] for s in srcs.values() if s.get("injection_flags")]
    if flagged:
        warnings.append(tr("warn_injection", ids=", ".join(flagged)))

    # 2. Документы
    for name, rules in block.get("documents", {}).items():
        path = pdir / "outputs" / name
        if not path.exists():
            warnings.append(tr("warn_doc_missing", name=name))
            continue
        text = path.read_text(encoding="utf-8")
        for sec in rules.get("required_sections", []):
            if not _has_section(text, sec):
                errors.append(tr("err_no_section", name=name, sec=sec))
        for i, line in enumerate(text.splitlines(), 1):
            for m in TAG.finditer(line):
                tid = m.group(1)
                if tid.startswith("C"):
                    if tid not in claims:
                        errors.append(tr("err_unknown_claim", name=name, i=i, tid=tid))
                    elif claims[tid]["status"] != "active":
                        by = f" ({tr('err_claim_superseded_by', by=claims[tid]['superseded_by'])})" \
                            if claims[tid].get("superseded_by") else ""
                        errors.append(tr("err_claim_status", name=name, i=i, tid=tid,
                                         status=claims[tid]["status"]) + by)
                elif tid.startswith("S") and tid not in srcs:
                    errors.append(tr("err_unknown_source", name=name, i=i, tid=tid))
                elif tid.startswith("D") and tid not in decisions:
                    errors.append(tr("err_unknown_decision", name=name, i=i, tid=tid))
            if rules.get("numbers_need_tags") and not line.startswith("#") and num_re.search(line) \
                    and not TAG.search(line) and not any(mk in line for mk in exempt):
                warnings.append(tr("warn_number_no_tag", name=name, i=i, line=line.strip()[:90]))
        if "min_options" in rules:
            heads = [l for l in text.splitlines() if re.match(rules["option_heading_regex"], l)]
            if len(heads) < rules["min_options"]:
                errors.append(tr("err_too_few_options", name=name, n=len(heads), m=rules["min_options"]))
            low = text.lower()
            if not any(k in low for k in rules.get("status_quo_keywords", [])):
                errors.append(tr("err_no_status_quo", name=name))
            if not any(k in low for k in rules.get("exit_keywords", [])):
                warnings.append(tr("warn_no_exit_option", name=name))
            chunks = re.split(rules["option_heading_regex"], text, flags=re.MULTILINE)[1:]
            for idx, chunk in enumerate(chunks, 1):
                for sec in rules.get("per_option_sections", []):
                    if sec.lower() not in chunk.lower():
                        errors.append(tr("err_option_section", name=name, idx=idx, sec=sec))
        if rules.get("promise_table_section"):
            body = _section_body(text, rules["promise_table_section"])
            rows = [l for l in body.splitlines() if l.startswith("|") and not l.startswith("|---")][1:]
            if not rows:
                errors.append(tr("err_promise_table_empty", name=name))
            for r in rows:
                if not TAG.search(r):
                    errors.append(tr("err_promise_no_tag", name=name, row=r[:80]))
        if not errors or all(not e.startswith(name) for e in errors):
            passed.append(name)

    # 3. Гэп-трекинг: пробел закрыт в 02, но строка 01 всё ещё «открыт»
    for w in gaps.sync_warnings(pdir):
        warnings.append(w)
    # 4. Сверка тегов RU↔EN: дописанный EN six-pager отстал от RU после правок документов
    warnings.extend(en_sync_warnings(pdir))
    # 4a. PRO-53: линтер EN-вывода — кириллица, русские десятичные запятые, маркер перевода
    warnings.extend(en_style_warnings(pdir))
    # 5. PRO-27: реестр изменился после lock вердикта review — вердикт устарел
    warnings.extend(review.stale_warnings(pdir))
    # 6. PRO-26: числовой кросс-чек — числа активных утверждений против заголовков источников,
    #    числа цитат против текста источников (sources/S###.md)
    warnings.extend(numeric_warnings(pdir, claims, srcs))
    # 7. PRO-52: языковой линтер документа комитета — запрещённые англицизмы, жаргон
    #    и аббревиатуры без расшифровки (quality_gate.json → banned_terms)
    warnings.extend(language_warnings(pdir, block, tr))
    score = max(0, 100 - 10 * len(errors) - 2 * len(warnings))
    return {"errors": errors, "warnings": warnings, "passed": passed, "score": score}


def language_warnings(pdir: Path, block: dict, tr) -> list[str]:
    """PRO-52: языковой линтер документа комитета — запрещённые англицизмы, жаргон
    и аббревиатуры без расшифровки. Список — quality_gate.json → banned_terms:
    «replace» — всегда заменяем (термин → как писать по-русски), «decode» — допустимо
    только с расшифровкой при первом упоминании: «SERP (страница результатов поиска)»
    или «SERP — страница результатов поиска». Сканируется outputs/SIX_PAGER.md
    (то, что читает комитет); инлайн-код и формулы не язык документа."""
    banned = block.get("banned_terms") if isinstance(block.get("banned_terms"), dict) else None
    page = pdir / "outputs" / "SIX_PAGER.md"
    if not banned or not page.exists():
        return []
    text = re.sub(r"`[^`]*`", " ", page.read_text(encoding="utf-8"))
    out: list[str] = []
    for term, instead in (banned.get("replace") or {}).items():
        if re.search(rf"(?<![\w-]){re.escape(term)}\w*", text, re.IGNORECASE):
            out.append(tr("warn_banned_term", name=page.name, term=term, instead=instead))
    for abbr, hint in (banned.get("decode") or {}).items():
        if not re.search(rf"(?<![A-Za-z]){re.escape(abbr)}(?![A-Za-z])", text):
            continue
        if not re.search(rf"{re.escape(abbr)}\s*(?:\(|—|–)\s*\S", text):
            out.append(tr("warn_abbrev_undecoded", name=page.name, term=abbr, hint=hint))
    return out


def report_text(res: dict, lang: str = "ru") -> str:
    tr = lambda key, **kw: i18n.t(lang, key, **kw)
    out = [tr("check_header", score=res["score"], errors=len(res["errors"]),
              warnings=len(res["warnings"]))]
    if res["passed"]:
        out.append(tr("check_passed", names=", ".join(res["passed"])))
    out += [f"✖ {e}" for e in res["errors"]]
    out += [f"⚠ {w}" for w in res["warnings"][:40]]
    if len(res["warnings"]) > 40:
        out.append(tr("check_more_warnings", n=len(res["warnings"]) - 40))
    return "\n".join(out)
