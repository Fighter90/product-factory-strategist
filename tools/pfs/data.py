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


def funnel(path: Path, steps: list[str] | str, user: str = "user_id", date: str | None = None,
           sheet: str | None = None) -> dict:
    """Воронка: уникальные пользователи на каждом шаге. Режим по заголовку: столбец event/stage (журнал событий)
    или флаги-колонки шагов (0/1). date — столбец даты для проверки порядка шагов (только в режиме событий)."""
    if isinstance(steps, str):
        steps = [s.strip() for s in steps.split(",") if s.strip()]
    if not steps:
        raise PfsError("Не заданы шаги воронки")
    rows = read_table(path, sheet)
    if not rows:
        raise PfsError("В таблице нет строк")
    if user not in rows[0]:
        raise PfsError(f"Нет столбца пользователя {user!r}. Есть: {list(rows[0])}")
    warnings: list[str] = []
    head = {c.lower(): c for c in rows[0]}
    event_col = head.get("event") or head.get("stage")
    counts: list[int] = []
    if event_col is not None:
        # Режим журнала событий: уникальные пользователи по значению event
        pairs = [((r[user] or "").strip(), (r[event_col] or "").strip().lower()) for r in rows]
        dup = len(pairs) - len(set(pairs))
        if dup:
            warnings.append(f"Дубликаты user+event: {dup} лишних строк — пользователь на шаге учтён один раз")
        for s in steps:
            counts.append(len({u for u, e in pairs if e == s.lower() and u}))
        if date:
            if date not in rows[0]:
                raise PfsError(f"Нет столбца даты {date!r}. Есть: {list(rows[0])}")
            first_dt: dict[tuple[str, str], datetime] = {}
            for r in rows:
                d, u = _date(r[date]), (r[user] or "").strip()
                if d and u:
                    key = (u, (r[event_col] or "").strip().lower())
                    if key not in first_dt or d < first_dt[key]:
                        first_dt[key] = d
            broken = 0
            for u in {u for u, _ in first_dt}:
                ds = [d for d in (first_dt.get((u, s.lower())) for s in steps) if d]
                broken += sum(1 for a, b in zip(ds, ds[1:]) if b < a)
            if broken:
                warnings.append(f"Нарушений порядка шагов по дате: {broken} (у пользователя событие более позднего шага раньше раннего)")
    elif all(s in rows[0] for s in steps):
        # Режим флагов-колонок: непустые значения 1/true/да считаются достигнутым шагом
        for s in steps:
            reached = {(r[user] or "").strip() for r in rows if _truthy(r.get(s, ""))}
            counts.append(len(reached - {""}))
    else:
        missing = [s for s in steps if s not in rows[0]]
        raise PfsError(f"Нет ни столбца event/stage, ни колонок шагов. Отсутствуют: {missing}. Есть: {list(rows[0])}")
    for i, c in enumerate(counts):
        if c == 0:
            warnings.append(f"Шаг «{steps[i]}»: нет данных (0 пользователей)")
        elif i and c > counts[i - 1]:
            warnings.append(f"Шаг «{steps[i]}»: пользователей {c} больше, чем на предыдущем шаге ({counts[i - 1]}) — воронка не возрастает")
    conv = [100.0] + [round(100 * c / prev, 1) if prev else None for c, prev in zip(counts[1:], counts[:-1])]
    users = len({(r[user] or "").strip() for r in rows if (r[user] or "").strip()})
    return {"steps": steps, "counts": counts, "conv_pct": conv, "warnings": warnings,
            "mode": "event" if event_col is not None else "columns", "users": users}


def funnel_text(res: dict) -> str:
    out = [f"Воронка (режим: {res.get('mode', '?')}, пользователей в файле: {res.get('users', '?')})",
           "| Шаг | Пользователей | Конверсия |", "|---|---|---|"]
    for i, s in enumerate(res["steps"]):
        conv = res["conv_pct"][i]
        out.append(f"| {s} | {res['counts'][i]} | {'—' if conv is None else f'{conv}%'} |")
    if res["warnings"]:
        out.append("\nПредупреждения:")
        out += [f"- {w}" for w in res["warnings"]]
    return "\n".join(out)


def _truthy(v: str) -> bool:
    v = (v or "").strip().lower()
    if not v:
        return False
    n = _num(v)
    if n is not None:
        return n != 0
    return v in ("true", "yes", "y", "да", "истина")


def _pctl(xs: list[float], p: float) -> float:
    """Персентиль p (0–100) по отсортированному списку с линейной интерполяцией."""
    if len(xs) == 1:
        return xs[0]
    pos = (len(xs) - 1) * p / 100
    lo = int(pos)
    if lo + 1 >= len(xs):
        return xs[-1]
    return xs[lo] + (pos - lo) * (xs[lo + 1] - xs[lo])


def _stats_of(xs: list[float]) -> dict:
    xs = sorted(xs)
    stdev = statistics.stdev(xs) if len(xs) >= 2 else 0.0
    return {"n": len(xs),
            "mean": round(statistics.fmean(xs), 4),
            "median": round(float(statistics.median(xs)), 4),
            "stdev": round(stdev, 4),
            "p05": round(_pctl(xs, 5), 4), "p50": round(_pctl(xs, 50), 4), "p95": round(_pctl(xs, 95), 4),
            "min": xs[0], "max": xs[-1],
            "ci95": round(1.96 * stdev / len(xs) ** 0.5, 4) if len(xs) >= 2 else 0.0}


def stats(path: Path, col: str, group: str | None = None, sheet: str | None = None) -> dict:
    """Описательная статистика столбца (n, среднее, медиана, stdev, перцентили, ci95); с group — по группам."""
    rows = read_table(path, sheet)
    if not rows:
        raise PfsError("В таблице нет строк")
    if col not in rows[0]:
        raise PfsError(f"Нет столбца {col!r}. Есть: {list(rows[0])}")
    if group and group not in rows[0]:
        raise PfsError(f"Нет столбца группы {group!r}. Есть: {list(rows[0])}")
    warnings: list[str] = []
    vals = [(r.get(col, "") or "").strip() for r in rows]
    xs = [n for n in (_num(v) for v in vals) if n is not None]
    skipped = len(vals) - len(xs)
    if skipped:
        warnings.append(f"«{col}»: пропущено или нечисловое: {skipped} из {len(vals)} — исключены из расчёта")
    if not xs:
        raise PfsError(f"В столбце «{col}» нет числовых значений")
    out = {"col": col, "warnings": warnings, **_stats_of(xs)}
    if group:
        buckets: dict[str, list[float]] = defaultdict(list)
        seen: dict[str, int] = defaultdict(int)
        for r in rows:
            g = (r.get(group, "") or "").strip() or "(пусто)"
            seen[g] += 1
            n = _num(r.get(col, ""))
            if n is not None:
                buckets[g].append(n)
        for g, cnt in seen.items():
            if g not in buckets:
                warnings.append(f"Группа «{g}» ({cnt} строк): нет числовых значений в «{col}» — пропущена")
        out["groups"] = {g: _stats_of(v) for g, v in sorted(buckets.items())}
    return out


def stats_text(res: dict) -> str:
    head = "| Выборка | n | среднее | медиана | stdev | p05 | p50 | p95 | min … max | ci95 (±) |"
    sep = "|---|---|---|---|---|---|---|---|---|---|"

    def row(name: str, s: dict) -> str:
        return (f"| {name} | {s['n']} | {s['mean']} | {s['median']} | {s['stdev']} | {s['p05']} | "
                f"{s['p50']} | {s['p95']} | {s['min']} … {s['max']} | ±{s['ci95']} |")

    out = [f"Столбец: {res['col']}", head, sep, row("все", res)]
    for g, s in (res.get("groups") or {}).items():
        out.append(row(g, s))
    if res["warnings"]:
        out.append("\nПредупреждения:")
        out += [f"- {w}" for w in res["warnings"]]
    return "\n".join(out)


def save_analysis(pdir: Path, name: str, text: str, command: str) -> Path:
    path = pdir / "analysis" / f"{name}.md"
    core.atomic_write(path, f"<!-- воспроизвести: {command} -->\n# {name}\n\nКоманда: `{command}`\n\n{text}\n")
    core.log(pdir, "analysis", f"Анализ сохранён: analysis/{name}.md", tool=command)
    return path
