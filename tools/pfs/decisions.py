"""Поддержка решений: основания, ответственные, показатели, условия пересмотра, обязательства."""
from __future__ import annotations

from datetime import date, datetime
from pathlib import Path

from . import claims as claims_mod, core, sources as src_mod
from .core import PfsError


def load(pdir: Path) -> list[dict]:
    return core.read_jsonl(pdir / "decisions.jsonl")


def _parse_metric(s: str) -> dict:
    # "Удержание M1: 38% -> 45% @2027-03-01"
    name, _, rest = s.partition(":")
    target_part, _, by = rest.partition("@")
    base, _, target = target_part.partition("->")
    return {"name": name.strip(), "baseline": base.strip(), "target": target.strip(), "by": by.strip() or None}


def _parse_commitment(s: str, idx: int) -> dict:
    what, owner, due = (s.split("|") + ["", ""])[:3]
    return {"id": f"K{idx}", "what": what.strip(), "owner": owner.strip() or None, "due": due.strip() or None, "status": "open"}


def add(pdir: Path, title: str, decision: str, owner: str, grounds: list[str], option: str | None = None,
        metrics: list[str] | None = None, review_date: str | None = None, triggers: list[str] | None = None,
        commitments: list[str] | None = None, rejected: list[str] | None = None) -> dict:
    for cid in grounds:
        c = claims_mod.get(pdir, cid)
        if c["status"] != "active":
            raise PfsError(f"{cid} не активно — решение нельзя основывать на отозванном утверждении")
    rows = load(pdir)
    rec = {"id": core.next_id("D", rows), "title": title, "decision": decision, "option": option, "owner": owner,
           "grounds": grounds, "rejected_options": rejected or [], "status": "accepted", "created": core.now(),
           "metrics": [_parse_metric(m) for m in (metrics or [])], "review": {"date": review_date, "triggers": triggers or []},
           "commitments": [_parse_commitment(c, i + 1) for i, c in enumerate(commitments or [])]}
    core.append_jsonl(pdir / "decisions.jsonl", rec)
    core.log(pdir, "decision", f"{rec['id']} принято: {title} (отв. {owner})", step="decision")
    return rec


def update_commitment(pdir: Path, did: str, kid: str, status: str, note: str | None = None) -> None:
    rows = load(pdir)
    for d in rows:
        if d["id"] == did:
            for k in d["commitments"]:
                if k["id"] == kid:
                    k["status"], k["updated"] = status, core.now()
                    if note:
                        k["note"] = note
                    core.write_jsonl(pdir / "decisions.jsonl", rows)
                    core.log(pdir, "decision", f"{did}/{kid} → {status}")
                    return
    raise PfsError(f"Не найдено {did}/{kid}")


def set_status(pdir: Path, did: str, status: str, reason: str) -> None:
    rows = load(pdir)
    for d in rows:
        if d["id"] == did:
            d["status"] = status
            d.setdefault("history", []).append({"ts": core.now(), "status": status, "reason": reason})
            core.write_jsonl(pdir / "decisions.jsonl", rows)
            core.log(pdir, "decision", f"{did} → {status}: {reason}")
            return
    raise PfsError(f"Решение {did} не найдено")


def rebase(pdir: Path, did: str, note: str = "") -> list[str]:
    """Перенести основания решения на замены замещённых утверждений; история сохраняется в решении."""
    cl = {c["id"]: c for c in claims_mod.load(pdir)}
    rows = load(pdir)
    for d in rows:
        if d["id"] != did:
            continue
        changes, base = [], []
        for g in d["grounds"]:
            cur = g
            while cl.get(cur, {}).get("status") == "superseded" and cl[cur].get("superseded_by"):
                cur = cl[cur]["superseded_by"]
            if cl.get(cur, {}).get("status") == "retracted":
                raise PfsError(f"Основание {cur} отозвано — решение {did} нужно пересмотреть по существу (decision status --status revisit)")
            if cur != g:
                changes.append(f"{g}→{cur}")
            base.append(cur)
        if changes:
            d["grounds"] = list(dict.fromkeys(base))
            d.setdefault("history", []).append({"ts": core.now(), "rebase": changes, "note": note})
            core.write_jsonl(pdir / "decisions.jsonl", rows)
            core.log(pdir, "decision", f"{did}: основания обновлены {', '.join(changes)}. {note}")
        return changes
    raise PfsError(f"Решение {did} не найдено")


def _days_since(iso: str | None) -> int | None:
    if not iso:
        return None
    try:
        return (date.today() - datetime.fromisoformat(iso[:10]).date()).days
    except ValueError:
        return None


def due(pdir: Path, on: str | None = None) -> dict:
    """Что решать сейчас: просроченные обязательства, наступившие даты пересмотра, устаревшие основания."""
    today = on or core.today()
    meta = core.read_json(pdir / "project.json", {})
    stale_days = meta.get("stale_after_days", 180)
    claims = {c["id"]: c for c in claims_mod.load(pdir)}
    srcs = {s["id"]: s for s in src_mod.load(pdir)}
    out = {"overdue": [], "review_now": [], "stale_grounds": [], "awaiting_human": None}
    for d in load(pdir):
        if d["status"] not in ("accepted", "revisit"):
            continue
        for k in d["commitments"]:
            if k["status"] == "open" and k.get("due") and k["due"] <= today:
                out["overdue"].append(f"{d['id']}/{k['id']} «{k['what']}» — отв. {k['owner']}, срок {k['due']}")
        if d["review"].get("date") and d["review"]["date"] <= today:
            out["review_now"].append(f"{d['id']} «{d['title']}»: дата пересмотра {d['review']['date']}; триггеры: "
                                     + "; ".join(d["review"]["triggers"]))
        for cid in d["grounds"]:
            c = claims.get(cid)
            if not c:
                continue
            if c["status"] != "active":
                out["stale_grounds"].append(f"{d['id']}: основание {cid} {c['status']}"
                                            + (f" → {c.get('superseded_by')}" if c.get("superseded_by") else ""))
                continue
            weak = [d2 for d2 in c.get("derived_from", []) if claims.get(d2, {}).get("status") != "active"]
            if weak:
                out["stale_grounds"].append(f"{d['id']}: основание {cid} опирается на неактивные {', '.join(weak)}")
            for sid in c["sources"]:
                age = _days_since(srcs.get(sid, {}).get("published") or srcs.get(sid, {}).get("retrieved"))
                if age is not None and age > stale_days:
                    out["stale_grounds"].append(f"{d['id']}: {cid} опирается на {sid} возрастом {age} дн. (> {stale_days})")
    out["awaiting_human"] = core.read_json(pdir / "state.json", {}).get("awaiting_human")
    return out


def due_text(res: dict) -> str:
    out = []
    if res["awaiting_human"]:
        out.append(f"РЕШИТЬ СЕЙЧАС: {res['awaiting_human']['question']}")
    for key, title in (("overdue", "Просроченные обязательства"), ("review_now", "Пора пересмотреть"),
                       ("stale_grounds", "Устаревшие основания")):
        if res[key]:
            out.append(title + ":")
            out += [f"  - {x}" for x in res[key]]
    return "\n".join(out) or "Нет просроченных обязательств, пересмотров и устаревших оснований."


def table(rows: list[dict]) -> str:
    out = ["| ID | Решение | Ответственный | Основания | Показатели | Пересмотр | Статус |", "|---|---|---|---|---|---|---|"]
    for d in rows:
        mets = "; ".join(
            (f"{m['name']}: {m['baseline']}" + (f" → {m['target']}" if m.get("target") else ""))
            + (f" к {m['by']}" if m.get("by") else "")
            for m in d["metrics"]
        )
        rev = (d["review"].get("date") or "") + ("; " + "; ".join(d["review"]["triggers"]) if d["review"]["triggers"] else "")
        out.append(f"| {d['id']} | {d['title']}: {d['decision']} | {d['owner']} | {', '.join(d['grounds'])} | {mets} | {rev} | {d['status']} |")
    return "\n".join(out)
