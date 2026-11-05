"""Анализ влияния: какие выводы, документы и решения затронуты изменением источника или утверждения."""
from __future__ import annotations

import re
from pathlib import Path

from . import claims as claims_mod, core, sources as src_mod

TAG = re.compile(r"\[((?:C|S|D)\d{3,})\]")


def doc_refs(pdir: Path) -> dict[str, list[tuple[str, int, str]]]:
    """ID → [(документ, строка, текст строки)] по всем outputs/*.md."""
    refs: dict[str, list[tuple[str, int, str]]] = {}
    for doc in sorted((pdir / "outputs").glob("*.md")):
        for i, line in enumerate(doc.read_text(encoding="utf-8").splitlines(), 1):
            for m in TAG.finditer(line):
                refs.setdefault(m.group(1), []).append((doc.name, i, line.strip()))
    return refs


def affected_claims(pdir: Path, start_ids: list[str]) -> list[str]:
    """Транзитивное замыкание: источник → утверждения на нём → выводы из них → …"""
    rows = claims_mod.load(pdir)
    hit: list[str] = []
    frontier = list(start_ids)
    seen = set(start_ids)
    while frontier:
        cur = frontier.pop(0)
        for c in rows:
            if c["id"] in seen:
                continue
            if cur in c["sources"] or cur in c["derived_from"]:
                seen.add(c["id"])
                hit.append(c["id"])
                frontier.append(c["id"])
    return hit


def impact(pdir: Path, target: str) -> dict:
    start = [target]
    if target.startswith("S"):
        src_mod.get(pdir, target)
    elif target.startswith("C"):
        claims_mod.get(pdir, target)
    claims = ([target] if target.startswith("C") else []) + affected_claims(pdir, start)
    refs = doc_refs(pdir)
    docs = []
    for cid in [target] + claims:
        for ref in refs.get(cid, []):
            docs.append({"id": cid, "doc": ref[0], "line": ref[1], "text": ref[2][:160]})
    decisions = [d for d in core.read_jsonl(pdir / "decisions.jsonl")
                 if set(d.get("grounds", [])) & set(claims + [target])]
    return {"target": target, "claims": claims, "doc_lines": docs,
            "decisions": [{"id": d["id"], "title": d["title"], "owner": d.get("owner")} for d in decisions]}


def impact_text(res: dict) -> str:
    lines = [f"Влияние изменения {res['target']}:"]
    lines.append(f"  Утверждения ({len(res['claims'])}): {', '.join(res['claims']) or '—'}")
    if res["doc_lines"]:
        lines.append("  Места в документах, которые нужно пересмотреть:")
        lines += [f"    {d['doc']}:{d['line']} [{d['id']}] {d['text']}" for d in res["doc_lines"]]
    else:
        lines.append("  В документах ссылок нет.")
    if res["decisions"]:
        lines.append("  Решения с затронутыми основаниями (нужен пересмотр):")
        lines += [f"    {d['id']} {d['title']} — отв. {d['owner']}" for d in res["decisions"]]
    return "\n".join(lines)
