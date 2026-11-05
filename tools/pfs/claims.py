"""Реестр утверждений (evidence ledger): факт / гипотеза / прогноз / допущение / вывод.

Главное правило памяти: вывод агента (inference) никогда не становится фактом — у него нет
собственного источника, только derived_from. Устаревшее не удаляется, а отзывается (retracted)
или замещается (superseded), чтобы было видно, что изменилось и почему.
"""
from __future__ import annotations

from pathlib import Path

from . import core, sources as src_mod
from .core import PfsError

KINDS = ("fact", "hypothesis", "forecast", "assumption", "inference")
KIND_RU = {"fact": "факт", "hypothesis": "гипотеза", "forecast": "прогноз", "assumption": "допущение", "inference": "вывод"}
CONFIDENCE = ("high", "medium", "low")
# Шкала силы доказательств (knowledge/methods/source-criticism.md): вывод не сильнее самого слабого критичного входа.
GRADES = ("A", "B", "C", "D")


def load(pdir: Path) -> list[dict]:
    return core.read_jsonl(pdir / "claims.jsonl")


def get(pdir: Path, cid: str) -> dict:
    for c in load(pdir):
        if c["id"] == cid:
            return c
    raise PfsError(f"Утверждение {cid} не найдено")


def _validate(pdir: Path, kind: str, sources: list[str], derived_from: list[str], confidence: str) -> str:
    if kind not in KINDS:
        raise PfsError(f"kind: {', '.join(KINDS)}")
    if confidence not in CONFIDENCE:
        raise PfsError(f"confidence: {', '.join(CONFIDENCE)}")
    src_rows = {s["id"]: s for s in src_mod.load(pdir)}
    for sid in sources:
        if sid not in src_rows:
            raise PfsError(f"Источник {sid} не зарегистрирован (pfs source add …)")
    claim_ids = {c["id"]: c for c in load(pdir)}
    for cid in derived_from:
        if cid not in claim_ids:
            raise PfsError(f"Утверждение {cid} не найдено")
        if claim_ids[cid]["status"] != "active":
            raise PfsError(f"{cid} отозвано/замещено — на него нельзя опираться")
    origins = {src_rows[s]["origin"] for s in sources}
    if kind == "fact":
        if not sources:
            raise PfsError("Факт без источника недопустим. Укажите --source S### или запишите как hypothesis/assumption")
        if origins <= {"synthetic", "agent"}:
            raise PfsError("Синтетические материалы и выводы агента не могут подтверждать факт — только гипотезу")
    if kind == "inference" and not derived_from:
        raise PfsError("Вывод (inference) должен ссылаться на утверждения: --from C001,C002")
    if kind in ("hypothesis", "forecast", "assumption") and not (sources or derived_from):
        # Допустимо, но помечаем как «из головы» — проверка покажет это как пробел.
        pass
    if origins and origins <= {"synthetic"}:
        return "synthetic"
    return "agent" if kind == "inference" else ("source" if sources else "agent")


def add(pdir: Path, text: str, kind: str, sources: list[str] | None = None, derived_from: list[str] | None = None,
        confidence: str = "medium", note: str | None = None, quote: str | None = None, tags: list[str] | None = None, grade: str | None = None) -> dict:
    if grade and grade not in GRADES:
        raise PfsError(f"grade: {', '.join(GRADES)}")
    sources, derived_from = sources or [], derived_from or []
    basis = _validate(pdir, kind, sources, derived_from, confidence)
    rows = load(pdir)
    for r in rows:  # повторный вызов с тем же текстом не плодит дубли
        if r["text"].strip() == text.strip() and r["status"] == "active":
            return r
    rec = {"id": core.next_id("C", rows), "text": text.strip(), "kind": kind, "sources": sources,
           "derived_from": derived_from, "confidence": confidence, "basis": basis, "quote": quote,
           "tags": tags or [], "grade": grade, "status": "active", "created": core.now(), "note": note}
    core.append_jsonl(pdir / "claims.jsonl", rec)
    core.log(pdir, "claim", f"{rec['id']} [{KIND_RU[kind]}] {text[:90]}", sources=sources or None)
    return rec


def _update(pdir: Path, cid: str, **fields) -> dict:
    rows = load(pdir)
    found = None
    for r in rows:
        if r["id"] == cid:
            r.update(fields)
            found = r
    if not found:
        raise PfsError(f"Утверждение {cid} не найдено")
    core.write_jsonl(pdir / "claims.jsonl", rows)
    return found


def retract(pdir: Path, cid: str, reason: str) -> dict:
    rec = _update(pdir, cid, status="retracted", retracted=core.now(), retract_reason=reason)
    core.log(pdir, "claim", f"{cid} отозвано: {reason}")
    return rec


def supersede(pdir: Path, cid: str, text: str, kind: str | None = None, sources: list[str] | None = None,
              confidence: str | None = None, reason: str = "", derived_from: list[str] | None = None) -> dict:
    old = get(pdir, cid)
    if old["status"] != "active":
        raise PfsError(f"{cid} уже не активно ({old['status']})")
    # Сначала снимаем активность, иначе валидация не даст сослаться на новое.
    _update(pdir, cid, status="superseded", superseded_at=core.now(), supersede_reason=reason)
    try:
        # Основания, которые сами уже замещены/отозваны, не переносятся: их нужно указать заново (--from).
        alive = {c["id"] for c in load(pdir) if c["status"] == "active"}
        base = derived_from if derived_from is not None else [d for d in old["derived_from"] if d in alive]
        new = add(pdir, text, kind or old["kind"], sources if sources is not None else old["sources"],
                  base, confidence or old["confidence"], note=f"замещает {cid}: {reason}")
    except PfsError:
        _update(pdir, cid, status="active", superseded_at=None, supersede_reason=None)
        raise
    _update(pdir, cid, superseded_by=new["id"])
    core.log(pdir, "claim", f"{cid} замещено {new['id']}: {reason}")
    return new


def table(rows: list[dict]) -> str:
    out = ["| ID | Тип | Утверждение | Источники / основания | Сила | Статус |", "|---|---|---|---|---|---|"]
    for c in rows:
        basis = ", ".join(c["sources"] + [f"←{d}" for d in c["derived_from"]]) or "—"
        status = c["status"] + (f" → {c['superseded_by']}" if c.get("superseded_by") else "")
        out.append(f"| {c['id']} | {KIND_RU[c['kind']]} | {c['text'].replace('|', '/')} | {basis} | {c.get('grade') or c['confidence']} | {status} |")
    return "\n".join(out)
