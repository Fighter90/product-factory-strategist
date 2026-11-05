"""Анализ данных: профиль таблицы (типы, пропуски, единицы, периоды) и когортное удержание. Воспроизводимо."""
from __future__ import annotations

import csv
import io
import statistics
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from . import core, extract
from .core import PfsError

DATE_FORMATS = ("%Y-%m-%d", "%d.%m.%Y", "%Y-%m", "%Y/%m/%d", "%d/%m/%Y", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S")


def read_table(path: Path, sheet: str | None = None) -> list[dict]:
    if path.suffix.lower() in (".xlsx", ".xlsm"):
        sheets = extract.xlsx_rows(path)
        rows = sheets.get(sheet) if sheet else next(iter(sheets.values()), [])
        if not rows:
            raise PfsError("Пустой лист")
        head = [h or f"col{i}" for i, h in enumerate(rows[0])]
        return [dict(zip(head, r + [""] * (len(head) - len(r)))) for r in rows[1:]]
    raw = path.read_text(encoding="utf-8-sig", errors="replace")
    dialect = csv.Sniffer().sniff(raw[:4096], delimiters=",;\t")
    return list(csv.DictReader(io.StringIO(raw), dialect=dialect))


def _num(v: str) -> float | None:
    v = (v or "").strip().replace(" ", "").replace(" ", "").replace(",", ".").rstrip("%")
    try:
        return float(v)
    except ValueError:
        return None


def _date(v: str) -> datetime | None:
    v = (v or "").strip()
    for f in DATE_FORMATS:
        try:
            return datetime.strptime(v[:19], f)
        except ValueError:
            continue
    return None


def profile(path: Path, sheet: str | None = None) -> dict:
    rows = read_table(path, sheet)
    if not rows:
        raise PfsError("В таблице нет строк")
    cols = list(rows[0].keys())
    out = {"file": str(path), "rows": len(rows), "columns": [], "warnings": []}
    seen, dups = set(), 0
    for r in rows:
        key = tuple(r.values())
        dups += key in seen
        seen.add(key)
    if dups:
        out["warnings"].append(f"Полных дублей строк: {dups}")
    for c in cols:
        vals = [r.get(c, "") for r in rows]
        empty = sum(1 for v in vals if not (v or "").strip())
        filled = [v for v in vals if (v or "").strip()]
        nums = [_num(v) for v in filled]
        dates = [_date(v) for v in filled]
        info = {"name": c, "missing": empty, "missing_pct": round(100 * empty / len(vals), 1), "unique": len(set(filled))}
        if filled and sum(n is not None for n in nums) >= 0.9 * len(filled):
            xs = [n for n in nums if n is not None]
            info.update(type="number", min=min(xs), max=max(xs), mean=round(statistics.fmean(xs), 4),
                        median=statistics.median(xs))
            if "%" in c or "доля" in c.lower() or "rate" in c.lower():
                if max(xs) <= 1:
                    info["unit_hint"] = "доля 0–1"
                elif max(xs) <= 100:
                    info["unit_hint"] = "проценты 0–100"
                else:
                    out["warnings"].append(f"«{c}»: в названии процент, но значения > 100 — проверьте единицы")
            if any(v.strip().endswith("%") for v in filled) and not all(v.strip().endswith("%") for v in filled):
                out["warnings"].append(f"«{c}»: смешаны значения со знаком % и без — разные единицы?")
        elif filled and sum(d is not None for d in dates) >= 0.9 * len(filled):
            ds = sorted(d for d in dates if d)
            months = sorted({(d.year, d.month) for d in ds})
            gaps = []
            for (y1, m1), (y2, m2) in zip(months, months[1:]):
                if (y2 * 12 + m2) - (y1 * 12 + m1) > 1:
                    gaps.append(f"{y1}-{m1:02d}→{y2}-{m2:02d}")
            info.update(type="date", min=ds[0].date().isoformat(), max=ds[-1].date().isoformat(), months=len(months))
            if gaps:
                out["warnings"].append(f"«{c}»: пропущенные месяцы {', '.join(gaps[:6])}")
        else:
            info.update(type="text", top=sorted(set(filled), key=filled.count, reverse=True)[:5])
        if info["missing_pct"] > 5:
            out["warnings"].append(f"«{c}»: пропусков {info['missing_pct']}%")
        out["columns"].append(info)
    return out


def profile_text(res: dict) -> str:
    out = [f"Файл: {res['file']} | строк: {res['rows']} | столбцов: {len(res['columns'])}",
           "| Столбец | Тип | Пропуски | Уникальных | Диапазон / топ |", "|---|---|---|---|---|"]
    for c in res["columns"]:
        if c["type"] == "number":
            rng = f"{c['min']} … {c['max']} (медиана {c['median']}, среднее {c['mean']})" + (f"; {c['unit_hint']}" if c.get("unit_hint") else "")
        elif c["type"] == "date":
            rng = f"{c['min']} … {c['max']} ({c['months']} мес.)"
        else:
            rng = ", ".join(str(x)[:20] for x in c.get("top", []))
        out.append(f"| {c['name']} | {c['type']} | {c['missing']} ({c['missing_pct']}%) | {c['unique']} | {rng} |")
    if res["warnings"]:
        out.append("\nПредупреждения:")
        out += [f"- {w}" for w in res["warnings"]]
    return "\n".join(out)


def cohort_retention(path: Path, user_col: str, date_col: str, sheet: str | None = None, max_periods: int = 12) -> dict:
    """Месячные когорты: доля пользователей когорты, активных в месяц N после первого события."""
    rows = read_table(path, sheet)
    if not rows or user_col not in rows[0] or date_col not in rows[0]:
        raise PfsError(f"Нужны столбцы {user_col!r} и {date_col!r}. Есть: {list(rows[0]) if rows else []}")
    events: dict[str, set[int]] = defaultdict(set)
    bad = 0
    for r in rows:
        d = _date(r[date_col])
        if not d or not r[user_col].strip():
            bad += 1
            continue
        events[r[user_col].strip()].add(d.year * 12 + d.month - 1)
    cohorts: dict[int, list[set[int]]] = defaultdict(list)
    for months in events.values():
        cohorts[min(months)].append(months)
    last = max(m for ms in events.values() for m in ms)
    table = []
    for start in sorted(cohorts):
        users = cohorts[start]
        row = {"cohort": f"{start // 12}-{start % 12 + 1:02d}", "size": len(users), "retention": []}
        for k in range(0, min(max_periods, last - start) + 1):
            row["retention"].append(round(100 * sum(1 for ms in users if start + k in ms) / len(users), 1))
        table.append(row)
    return {"cohorts": table, "users": len(events), "skipped_rows": bad,
            "method": f"Месячные когорты по первому событию; активность = хотя бы одно событие в месяце; столбцы {user_col}, {date_col}"}


def cohort_text(res: dict) -> str:
    width = max(len(r["retention"]) for r in res["cohorts"])
    out = [res["method"], f"Пользователей: {res['users']}; пропущено строк без даты/ID: {res['skipped_rows']}",
           "| Когорта | Размер | " + " | ".join(f"M{k}" for k in range(width)) + " |", "|---|---|" + "---|" * width]
    for r in res["cohorts"]:
        cells = [f"{v}%" for v in r["retention"]] + [""] * (width - len(r["retention"]))
        out.append(f"| {r['cohort']} | {r['size']} | " + " | ".join(cells) + " |")
    return "\n".join(out)


def save_analysis(pdir: Path, name: str, text: str, command: str) -> Path:
    path = pdir / "analysis" / f"{name}.md"
    core.atomic_write(path, f"<!-- воспроизвести: {command} -->\n# {name}\n\nКоманда: `{command}`\n\n{text}\n")
    core.log(pdir, "analysis", f"Анализ сохранён: analysis/{name}.md", tool=command)
    return path
