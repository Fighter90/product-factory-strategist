"""Контроль качества (quality gate): проверяемость, разделение фактов и гипотез, полнота стратегии."""
from __future__ import annotations

import re
from pathlib import Path

from . import claims as claims_mod, core, sources as src_mod
from .impact import TAG


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
