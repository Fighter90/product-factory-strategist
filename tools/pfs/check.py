"""Контроль качества (quality gate): проверяемость, разделение фактов и гипотез, полнота стратегии."""
from __future__ import annotations

import re
from pathlib import Path

from . import claims as claims_mod, core, gaps, review, sources as src_mod
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
    (C###/S###/D###), которых в EN ещё нет — EN-каркас отстал от RU (типовой случай:
    драйверы добавили в 03/04 после сборки EN) и подлежит пересборке. EN нет или
    теги совпадают — предупреждений нет (EN-черновик опционален)."""
    ru, en = pdir / "outputs" / "SIX_PAGER.md", pdir / "outputs" / "SIX_PAGER_EN.md"
    if not (ru.exists() and en.exists()):
        return []
    missing = sorted(set(TAG.findall(ru.read_text(encoding="utf-8")))
                     - set(TAG.findall(en.read_text(encoding="utf-8"))),
                     key=lambda t: (t[0], int(t[1:])))
    if not missing:
        return []
    return [f"SIX_PAGER_EN.md отстал от RU: нет тегов {', '.join(missing)} — "
            "пересоберите пару: pfs export --six-pager --en"]


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
    которое иначе доживает до финального аудита.
    1) числа активного утверждения против чисел заголовка источника, на который оно ссылается:
       оба набора непусты и не пересекаются → warning с парой C###/S### (пересечение хотя бы
       по одному числу расхождением не считается — утверждение вправе содержать числа сверх заголовка);
    2) числа цитаты (quote) против текста sources/S###.md: числа, которых в тексте нет → warning."""
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
                    out.append(f"{c['id']}/{sid}: числа заголовка источника ({_fmt(tnums)}) не совпадают "
                               f"с числами утверждения ({_fmt(cnums)}); число подтверждено текстом "
                               f"sources/{sid}.md — возможно, разные показатели")
                else:
                    out.append(f"{c['id']}/{sid}: числа утверждения ({_fmt(cnums)}) не совпадают с числами "
                               f"заголовка источника ({_fmt(tnums)}) и отсутствуют в его тексте — "
                               f"серьёзное расхождение, сверьте утверждение с источником")
            quote = c.get("quote")
            if quote:
                if sid in bodies:
                    missing = {v: raw for v, raw in _numbers(quote).items() if v not in bodies[sid]}
                    if missing:
                        out.append(f"{c['id']}/{sid}: числа из цитаты ({_fmt(missing)}) отсутствуют "
                                   f"в тексте источника — проверьте цитату против sources/{sid}.md")
    return out


def run(pdir: Path) -> dict:
    cfg = core.read_json(core.CONFIG / "quality_gate.json", {})
    errors: list[str] = []
    warnings: list[str] = []
    passed: list[str] = []
    claims = {c["id"]: c for c in claims_mod.load(pdir)}
    srcs = {s["id"]: s for s in src_mod.load(pdir)}
    decisions = {d["id"] for d in core.read_jsonl(pdir / "decisions.jsonl")}
    num_re = re.compile(cfg.get("number_regex", r"\d+%"), re.IGNORECASE)
    exempt = cfg.get("exempt_line_markers", [])

    # 1. Реестр утверждений
    for c in claims.values():
        if c["status"] != "active":
            continue
        if c["kind"] == "fact" and not c["sources"]:
            errors.append(f"{c['id']}: факт без источника")
        if c["kind"] == "fact" and c["sources"] and all(srcs.get(s, {}).get("origin") == "synthetic" for s in c["sources"]):
            errors.append(f"{c['id']}: факт опирается только на синтетические ответы")
        if c["kind"] == "fact" and c.get("grade") == "D":
            errors.append(f"{c['id']}: сила D не может быть фактом — переведите в допущение")
        stale = [d for d in c["derived_from"] if claims.get(d, {}).get("status") != "active"]
        if stale:
            warnings.append(f"{c['id']}: основания {', '.join(stale)} замещены/отозваны — пересмотрите вывод (pfs claim supersede --from …)")
        if c["kind"] in ("hypothesis", "forecast", "assumption") and not (c["sources"] or c["derived_from"]):
            warnings.append(f"{c['id']}: {claims_mod.KIND_RU[c['kind']]} без оснований — укажите, откуда она")
    flagged = [s["id"] for s in srcs.values() if s.get("injection_flags")]
    if flagged:
        warnings.append(f"Источники с фразами-инструкциями (проигнорированы как команды): {', '.join(flagged)}")

    # 2. Документы
    for name, rules in cfg.get("documents", {}).items():
        path = pdir / "outputs" / name
        if not path.exists():
            warnings.append(f"{name}: документа ещё нет")
            continue
        text = path.read_text(encoding="utf-8")
        for sec in rules.get("required_sections", []):
            if not _has_section(text, sec):
                errors.append(f"{name}: нет раздела «{sec}»")
        for i, line in enumerate(text.splitlines(), 1):
            for m in TAG.finditer(line):
                tid = m.group(1)
                if tid.startswith("C"):
                    if tid not in claims:
                        errors.append(f"{name}:{i}: ссылка на несуществующее {tid}")
                    elif claims[tid]["status"] != "active":
                        errors.append(f"{name}:{i}: {tid} {claims[tid]['status']} — обновите формулировку"
                                      + (f" (замена: {claims[tid].get('superseded_by')})" if claims[tid].get("superseded_by") else ""))
                elif tid.startswith("S") and tid not in srcs:
                    errors.append(f"{name}:{i}: ссылка на несуществующий источник {tid}")
                elif tid.startswith("D") and tid not in decisions:
                    errors.append(f"{name}:{i}: ссылка на несуществующее решение {tid}")
            if rules.get("numbers_need_tags") and not line.startswith("#") and num_re.search(line) \
                    and not TAG.search(line) and not any(mk in line for mk in exempt):
                warnings.append(f"{name}:{i}: число без ссылки на C###/S###: «{line.strip()[:90]}»")
        if "min_options" in rules:
            heads = [l for l in text.splitlines() if re.match(rules["option_heading_regex"], l)]
            if len(heads) < rules["min_options"]:
                errors.append(f"{name}: вариантов {len(heads)}, нужно не меньше {rules['min_options']}")
            low = text.lower()
            if not any(k in low for k in rules.get("status_quo_keywords", [])):
                errors.append(f"{name}: нет варианта «оставить как есть»")
            if not any(k in low for k in rules.get("exit_keywords", [])):
                warnings.append(f"{name}: не рассмотрен вариант «закрыть/свернуть направление»")
            chunks = re.split(rules["option_heading_regex"], text, flags=re.MULTILINE)[1:]
            for idx, chunk in enumerate(chunks, 1):
                for sec in rules.get("per_option_sections", []):
                    if sec.lower() not in chunk.lower():
                        errors.append(f"{name}: у варианта №{idx} нет раздела «{sec}»")
        if rules.get("promise_table_section"):
            body = _section_body(text, rules["promise_table_section"])
            rows = [l for l in body.splitlines() if l.startswith("|") and not l.startswith("|---")][1:]
            if not rows:
                errors.append(f"{name}: таблица «обещание → чем подтверждено в продукте» пуста")
            for r in rows:
                if not TAG.search(r):
                    errors.append(f"{name}: обещание без подтверждения (нет C###/S###): «{r[:80]}»")
        if not errors or all(not e.startswith(name) for e in errors):
            passed.append(name)

    # 3. Гэп-трекинг: пробел закрыт в 02, но строка 01 всё ещё «открыт»
    for w in gaps.sync_warnings(pdir):
        warnings.append(w)
    # 4. Сверка тегов RU↔EN: EN-каркас six-pager отстал от RU после правок документов
    warnings.extend(en_sync_warnings(pdir))
    # 5. PRO-27: реестр изменился после lock вердикта review — вердикт устарел
    warnings.extend(review.stale_warnings(pdir))
    # 6. PRO-26: числовой кросс-чек — числа активных утверждений против заголовков источников,
    #    числа цитат против текста источников (sources/S###.md)
    warnings.extend(numeric_warnings(pdir, claims, srcs))
    score = max(0, 100 - 10 * len(errors) - 2 * len(warnings))
    return {"errors": errors, "warnings": warnings, "passed": passed, "score": score}


def report_text(res: dict) -> str:
    out = [f"Контроль качества: {res['score']}/100 | ошибок {len(res['errors'])}, предупреждений {len(res['warnings'])}"]
    if res["passed"]:
        out.append("✔ Без ошибок: " + ", ".join(res["passed"]))
    out += [f"✖ {e}" for e in res["errors"]]
    out += [f"⚠ {w}" for w in res["warnings"][:40]]
    if len(res["warnings"]) > 40:
        out.append(f"… ещё {len(res['warnings']) - 40} предупреждений")
    return "\n".join(out)
