"""Реестр утверждений (evidence ledger): факт / гипотеза / прогноз / допущение / вывод.

Главное правило памяти: вывод агента (inference) никогда не становится фактом — у него нет
собственного источника, только derived_from. Устаревшее не удаляется, а отзывается (retracted)
или замещается (superseded), чтобы было видно, что изменилось и почему.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from . import core, sources as src_mod
from .core import PfsError

LOCK_NAME = ".claims.lock"  # файл блокировки реестра: батчевая валидация + запись идут под core.file_lock (PRO-33)
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


def _as_list(value) -> list[str]:
    """Строка «a,b» или список → список строк (поля source/from/tags в JSONL-строке батча)."""
    if value is None:
        return []
    if isinstance(value, str):
        return [x.strip() for x in value.split(",") if x.strip()]
    if isinstance(value, list):
        return [str(x).strip() for x in value if str(x).strip()]
    raise PfsError("ожидался список или строка через запятую")


def _batch_items(path: Path) -> list[dict]:
    """Прочитать JSONL-файл батча: JSON-объект на строку, пустые строки пропускаются."""
    if not path.exists():
        raise PfsError(f"Файл не найден: {path}")
    items = []
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise PfsError(f"Строка {n}: не JSON ({exc.msg})") from None
        if not isinstance(row, dict):
            raise PfsError(f"Строка {n}: ожидался JSON-объект {{\"text\": …, \"kind\": …}}")
        items.append(row)
    if not items:
        raise PfsError("Файл не содержит строк с утверждениями")
    return items


def add_batch(pdir: Path, path: Path) -> dict:
    """Массовая регистрация утверждений из JSONL-файла (PRO-33).

    Строка файла: {"text": "…", "kind": "fact", "source": "S001", "grade": "B",
    "quote": "…", "from": "C004", "confidence": "high", "note": "…", "tags": "a,b"} —
    source/from/tags можно списком или строкой через запятую. Все строки валидируются
    ДО записи: невалидная строка отменяет весь батч (атомарность). Дубликаты по тексту
    (реестр и сам батч) пропускаются. В журнал пишется одна запись на батч, а не по
    записи на каждое утверждение.
    """
    items = _batch_items(path)
    with core.file_lock(pdir / LOCK_NAME):
        rows = load(pdir)
        active_texts = {r["text"].strip() for r in rows if r["status"] == "active"}
        recs, skipped, seen = [], 0, set()
        for n, item in enumerate(items, 1):
            try:
                text = str(item.get("text") or "").strip()
                if not text:
                    raise PfsError("пустой text")
                if text in active_texts or text in seen:
                    skipped += 1
                    seen.add(text)
                    continue
                seen.add(text)
                kind, grade = item.get("kind"), item.get("grade")
                if grade is not None and grade not in GRADES:
                    raise PfsError(f"grade: {', '.join(GRADES)}")
                confidence = item.get("confidence") or "medium"
                sources_list = _as_list(item.get("source") or item.get("sources"))
                derived = _as_list(item.get("from") or item.get("derived_from"))
                basis = _validate(pdir, kind, sources_list, derived, confidence)
                recs.append({"id": core.next_id("C", rows + recs), "text": text, "kind": kind,
                             "sources": sources_list, "derived_from": derived, "confidence": confidence,
                             "basis": basis, "quote": item.get("quote"), "tags": _as_list(item.get("tags")),
                             "grade": grade, "status": "active", "created": core.now(), "note": item.get("note")})
            except PfsError as exc:
                raise PfsError(f"Строка {n}: {exc}") from None
        if recs:  # вся пачка одной записью: обрыв посреди батча не оставляет полреестра
            payload = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in recs)
            target = pdir / "claims.jsonl"
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("a", encoding="utf-8") as fh:
                fh.write(payload)
    if recs:
        core.log(pdir, "claim", f"add-batch: создано {len(recs)}, дубликаты пропущены {skipped}")
    return {"created": [r["id"] for r in recs], "skipped": skipped, "total": len(items)}


def retag(pdir: Path, from_id: str, to_id: str) -> dict:
    """Перенумерация тегов утверждений во всех outputs/*.md одной командой (PRO-58).

    Кейс: агент правил теги вручную через sed по всем документам. Здесь замена
    [C003] → [C059] идёт по всем документам разом, с валидацией ДО записи (не найдён
    ни один тег — ничего не пишется) и одной записью в журнал. Реестр claims.jsonl
    не меняется: переносятся только ссылки в документах.
    """
    shape = re.compile(r"^C\d{3,}$")
    for x in (from_id, to_id):
        if not shape.match(x or ""):
            raise PfsError(f"retag: ожидаются ID утверждений C###, получено «{x}»")
    if from_id == to_id:
        raise PfsError("retag: --from и --to совпадают — заменять нечего")
    get(pdir, to_id)  # цель должна быть в реестре: иначе в документах останутся висячие теги
    docs = sorted((pdir / "outputs").glob("*.md"))
    tag = re.compile(r"\[" + re.escape(from_id) + r"\]")
    planned = []
    replacements = 0
    for doc in docs:
        text = doc.read_text(encoding="utf-8")
        n = len(tag.findall(text))
        if n:
            planned.append((doc, tag.sub(f"[{to_id}]", text)))
            replacements += n
    if not planned:
        raise PfsError(f"retag: тег [{from_id}] не найден ни в одном документе outputs/ — править нечего")
    for doc, text in planned:  # запись только после успешной валидации всех документов
        core.atomic_write(doc, text)
    names = [doc.name for doc, _ in planned]
    core.log(pdir, "claim", f"retag: [{from_id}] → [{to_id}] — файлов {len(planned)}, вхождений {replacements} ({', '.join(names)})")
    return {"from": from_id, "to": to_id, "files": len(planned), "replacements": replacements, "docs": names}


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
              confidence: str | None = None, reason: str = "", derived_from: list[str] | None = None,
              grade: str | None = None) -> dict:
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
                  base, confidence or old["confidence"], note=f"замещает {cid}: {reason}",
                  grade=grade or old.get("grade"))  # сила доказательства не теряется при замещении
    except PfsError:
        _update(pdir, cid, status="active", superseded_at=None, supersede_reason=None)
        raise
    _update(pdir, cid, superseded_by=new["id"])
    core.log(pdir, "claim", f"{cid} замещено {new['id']}: {reason}")
    return new


def rebase(pdir: Path, cid: str) -> list[str]:
    """Перенаправить замещённые основания вывода на их замены (текст вывода не меняется).

    Отозванные (retracted) основания не перенаправляются — такой вывод нужно пересмотреть по существу.
    """
    rows = load(pdir)
    by_id = {r["id"]: r for r in rows}
    target = by_id.get(cid)
    if not target:
        raise PfsError(f"Утверждение {cid} не найдено")
    changes, new_base = [], []
    for d in target["derived_from"]:
        cur = d
        while by_id.get(cur, {}).get("status") == "superseded" and by_id[cur].get("superseded_by"):
            cur = by_id[cur]["superseded_by"]
        if by_id.get(cur, {}).get("status") == "retracted":
            raise PfsError(f"Основание {cur} отозвано — пересмотрите {cid} по существу (supersede/retract)")
        if cur != d:
            changes.append(f"{d}→{cur}")
        new_base.append(cur)
    if changes:
        target["derived_from"] = list(dict.fromkeys(new_base))
        target.setdefault("history", []).append({"ts": core.now(), "rebase": changes})
        core.write_jsonl(pdir / "claims.jsonl", rows)
        core.log(pdir, "claim", f"{cid}: основания перенаправлены {', '.join(changes)}")
    return changes


def table(rows: list[dict]) -> str:
    out = ["| ID | Тип | Утверждение | Источники / основания | Сила | Статус |", "|---|---|---|---|---|---|"]
    for c in rows:
        basis = ", ".join(c["sources"] + [f"←{d}" for d in c["derived_from"]]) or "—"
        status = c["status"] + (f" → {c['superseded_by']}" if c.get("superseded_by") else "")
        out.append(f"| {c['id']} | {KIND_RU[c['kind']]} | {c['text'].replace('|', '/')} | {basis} | {c.get('grade') or c['confidence']} | {status} |")
    return "\n".join(out)
