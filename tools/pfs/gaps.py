"""Гэп-трекинг: закрытие пробелов синхронно в 01_research_plan.md и 02_situation.md.

Пробел живёт в двух местах:
  02_situation.md — строка в таблице раздела «Чего мы не знаем»;
  01_research_plan.md — пункт в разделе «Пробелы…» и/или строка вопроса со столбцом «Статус».
`pfs gap close <номер> --claim C###` помечает пробел закрытым в обоих файлах сразу;
повтор с тем же --claim, когда 02 уже закрыта этим утверждением, идемпотентен и
синхронизирует 01 (исправление рассинхрона),
`pfs gap list` показывает пробелы с номерами, а `pfs check` предупреждает, если 02
говорит «закрыто», но строка 01 всё ещё «открыт» (рассинхрон после ручных правок).

Маркер закрытия — «закрыто»/«закрыты»/«закрыт» (без «частично» и «не»): «закрыть»,
«закрытые данные», «частично закрыто» считаются открытыми, чтобы ложных тревог не было.
"""
from __future__ import annotations

import re
from pathlib import Path

from . import claims as claims_mod, core
from .core import PfsError

CLOSED_RE = re.compile(r"закрыт(?:о|ы)?(?![а-яё])", re.IGNORECASE)
SEP_RE = re.compile(r"\|[\s\-:|]*\|")
PLACEHOLDERS = {"", "—", "…", "-"}


def _is_closed(text: str) -> bool:
    t = text.lower()
    if "частично" in t or "не закрыт" in t:
        return False
    return bool(CLOSED_RE.search(t))


def _norm(s: str) -> str:
    s = s.replace("ё", "е").lower()
    s = re.sub(r"[*~_`()\"'«»\[\]]", "", s)
    return re.sub(r"\s+", " ", s).strip(" \t.;:!?,—–-")


def _tok_hit(tok: str, tokens: list[str]) -> bool:
    """Слово найдено: точно (короткие) или по началу слова (русское словоизменение)."""
    if len(tok) < 5:
        return tok in tokens
    return any(t[:5] == tok[:5] for t in tokens)


def _matches(title: str, other: str) -> bool:
    """Пробел найден в строке 01: подстрока или все значимые слова (по 5 первым буквам)."""
    a, b = _norm(title), _norm(other)
    if len(a) < 4 or len(b) < 4:
        return False
    if a in b or b in a:
        return True
    ta, tb = a.split(), b.split()
    hard = [t for t in ta if len(t) >= 5]
    return len(hard) >= 2 and all(_tok_hit(t, tb) for t in hard)


def _section_span(text: str, name: str) -> tuple[int, int] | None:
    """Границы тела раздела [start, end) по номерам строк; None, если раздела нет."""
    lines = text.splitlines()
    start = end = None
    level = 0
    for i, l in enumerate(lines):
        if l.startswith("#"):
            lvl = len(l) - len(l.lstrip("#"))
            if start is not None and lvl <= level:
                end = i
                break
            if name.lower() in l.lower():
                start, level = i + 1, lvl
    if start is not None and end is None:
        end = len(lines)
    return (start, end) if start is not None else None


def _cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def _table_rows(lines: list[str]) -> list[tuple[int, list[str]]]:
    rows = []
    for i, l in enumerate(lines):
        s = l.strip()
        if not s.startswith("|") or SEP_RE.fullmatch(s):
            continue
        rows.append((i, _cells(s)))
    return rows


def _gaps02(text: str) -> list[dict]:
    """Пробелы из таблицы «Чего мы не знаем»: номер, заголовок, закрыт ли, строка."""
    span = _section_span(text, "не знаем")
    if not span:
        return []
    body = text.splitlines()[span[0]:span[1]]
    out, n = [], 0
    for i, cells in _table_rows(body):
        if len(cells) < 2 or cells[0].lower() == "пробел":  # шапка таблицы
            continue
        n += 1
        out.append({"n": n, "title": cells[0], "cells": cells, "line": span[0] + i + 1,
                    "closed": _is_closed(" ".join(cells))})
    return out


def _gap_items01(text: str) -> list[dict]:
    """Нумерованные пункты раздела «Пробелы…» из 01."""
    span = _section_span(text, "пробел")
    if not span:
        return []
    out = []
    for i, l in enumerate(text.splitlines()[span[0]:span[1]]):
        m = re.match(r"\s*(\d+)\.\s+(.*\S)", l)
        if m:
            out.append({"n": int(m.group(1)), "text": m.group(2), "line": span[0] + i + 1})
    return out


def _status_rows(text: str) -> list[dict]:
    """Строки таблиц 01 со столбцом «Статус»: вопрос, текущий статус, индекс столбца."""
    out, col, qcol = [], None, None
    for i, l in enumerate(text.splitlines()):
        s = l.strip()
        if not s.startswith("|"):
            col = qcol = None
            continue
        if SEP_RE.fullmatch(s):
            continue
        cells = _cells(s)
        low = [c.lower() for c in cells]
        if col is None:
            if "статус" in low:
                col = low.index("статус")
                qcol = 1 if len(cells) > 1 else 0
            continue
        if len(cells) <= max(col, qcol) or cells[qcol] in PLACEHOLDERS:
            continue  # строка-шаблон без вопроса
        out.append({"question": cells[qcol], "status": cells[col], "col": col,
                    "line": i + 1, "cells": cells})
    return out


def _write(path: Path, old_text: str, lines: list[str]) -> None:
    core.atomic_write(path, "\n".join(lines) + ("\n" if old_text.endswith("\n") else ""))


def close(pdir: Path, num: int, claim_id: str, note: str = "") -> dict:
    """Пометить пробел №num закрытым: строка 02 + пункт/статус в 01 — одним действием.

    Повтор с тем же --claim, когда строка 02 уже помечена закрытой этим утверждением,
    идемпотентен: 02 не переписывается, но 01 синхронизируется (исправление рассинхрона
    после ручных правок). Повтор с другим --claim или по строке без [C###] — отказ.
    """
    claim_id = (claim_id or "").strip().upper()
    if claim_id not in {c["id"] for c in claims_mod.load(pdir)}:
        raise PfsError(f"Утверждение {claim_id or '—'} не найдено в реестре — "
                       f"сначала pfs claim add --kind fact --source S###")
    sit_path = pdir / "outputs" / "02_situation.md"
    if not sit_path.exists():
        raise PfsError("02_situation.md не найден — таблицы «Чего мы не знаем» нет")
    sit = sit_path.read_text(encoding="utf-8")
    gs = _gaps02(sit)
    g = next((x for x in gs if x["n"] == num), None)
    if g is None:
        raise PfsError(f"Пробел №{num} не найден в 02_situation.md (всего {len(gs)}) — см. pfs gap list")
    already_closed = g["closed"]
    marker = f"**закрыто {core.today()} [{claim_id}]**" + (f": {note}" if note else "")
    if already_closed:
        row_ids = {m.upper() for m in re.findall(r"\[(C\d+)\]", " ".join(g["cells"]), re.IGNORECASE)}
        if claim_id not in row_ids:
            who = ", ".join(sorted(row_ids)) if row_ids else "без [C###] в строке"
            raise PfsError(f"Пробел №{num} «{g['title']}» уже помечен закрытым в 02_situation.md "
                           f"({who}) — повторное закрытие с {claim_id} не требуется")
    else:
        lines = sit.splitlines()
        cells = list(g["cells"])
        reason = cells[1]
        cells[1] = (reason + " " if reason not in PLACEHOLDERS else "") + marker
        lines[g["line"] - 1] = "| " + " | ".join(cells) + " |"
        _write(sit_path, sit, lines)

    touched: list[str] = []
    plan_path = pdir / "outputs" / "01_research_plan.md"
    if plan_path.exists():
        plan = plan_path.read_text(encoding="utf-8")
        plines = plan.splitlines()
        changed = False
        for it in _gap_items01(plan):
            if _matches(g["title"], it["text"]) and not _is_closed(it["text"]):
                plines[it["line"] - 1] = plines[it["line"] - 1].rstrip() + " " + marker
                touched.append(f"пункт {it['n']}")
                changed = True
        for r in _status_rows(plan):
            st = r["status"].lower()
            if _matches(g["title"], r["question"]) and ("открыт" in st or "пробел" in st) \
                    and not _is_closed(r["status"]):
                cells = list(r["cells"])
                cells[r["col"]] = f"отвечен [{claim_id}]"
                plines[r["line"] - 1] = "| " + " | ".join(cells) + " |"
                touched.append(f"строка {r['line']} (статус → отвечен)")
                changed = True
        if changed:
            _write(plan_path, plan, plines)
    core.log(pdir, "gap", f"Пробел №{num} «{g['title']}» закрыт ({claim_id}) в 01/02")
    msg = (f"Пробел №{num} «{g['title']}» уже был помечен закрытым в 02_situation.md [{claim_id}]"
           if already_closed else
           f"Пробел №{num} «{g['title']}» закрыт в 02_situation.md [{claim_id}]")
    if touched:
        msg += "; 01_research_plan.md — " + ", ".join(touched)
    else:
        msg += "; в 01_research_plan.md совпадений по названию не найдено — сверьте вручную"
    return {"n": num, "title": g["title"], "claim": claim_id, "touched": touched, "message": msg}


def list_text(pdir: Path) -> str:
    """Список пробелов с номерами для `pfs gap close <номер>`."""
    sit = pdir / "outputs" / "02_situation.md"
    if not sit.exists():
        return "02_situation.md ещё не создан — пробелов нет."
    gs = _gaps02(sit.read_text(encoding="utf-8"))
    if not gs:
        return "В 02_situation.md нет таблицы пробелов («Чего мы не знаем»)."
    out = ["Пробелы (02_situation.md, «Чего мы не знаем»):"]
    for g in gs:
        row = " ".join(g["cells"]).lower()
        mark = "закрыт" if g["closed"] else ("частично" if "частично" in row else "открыт")
        out.append(f"  {g['n']}. [{mark}] {g['title']}")
    out.append('Закрыть: pfs gap close <номер> --claim C### [--note "чем закрыт"]')
    return "\n".join(out)


def sync_warnings(pdir: Path) -> list[str]:
    """Рассинхрон 01/02: в 02 пробел закрыт, а строка 01 всё ещё открытая.

    Открытые статусы строки вопроса — «открыт» и «пробел» (те же, что правит close).
    Подсказка должна быть исполнимой: если в закрытой строке 02 есть [C###], рекомендуем
    `pfs gap close <номер> --claim <этот C###>` (повтор с тем же claim идемпотентен и
    синхронизирует 01); если claim в строке нет — советуем правку строки 01 вручную.
    """
    sit, plan = pdir / "outputs" / "02_situation.md", pdir / "outputs" / "01_research_plan.md"
    if not (sit.exists() and plan.exists()):
        return []
    plan_text = plan.read_text(encoding="utf-8")
    items, rows = _gap_items01(plan_text), _status_rows(plan_text)
    out = []
    for g in _gaps02(sit.read_text(encoding="utf-8")):
        if not g["closed"]:
            continue
        ids = re.findall(r"\[(C\d+)\]", " ".join(g["cells"]), re.IGNORECASE)
        remedy = (f"выполните pfs gap close {g['n']} --claim {ids[0].upper()}" if ids else
                  "отметьте закрытие в строке 01_research_plan.md вручную — "
                  "в строке 02 нет [C###], команде нечем сверить")
        for it in items:
            if _matches(g["title"], it["text"]) and "открыт" in it["text"].lower() \
                    and not _is_closed(it["text"]):
                out.append(f"01_research_plan.md:{it['line']}: пробел «{g['title']}» закрыт в 02_situation.md, "
                           f"но в плане числится «открыт» — {remedy}")
        for r in rows:
            st = r["status"].lower()
            if _matches(g["title"], r["question"]) and ("открыт" in st or "пробел" in st) \
                    and not _is_closed(r["status"]):
                out.append(f"01_research_plan.md:{r['line']}: статус вопроса «{r['question'][:60]}» — "
                           f"«{r['status']}», хотя пробел закрыт в 02_situation.md — {remedy}")
    return out
