"""PRO-47: линтер содержания six-pager — документ комитета, а не только теги.

Сломанный six-pager проходил `pfs check --strict` со счётом 100/100, а evidence-auditor
ставил ему 21 из 22: прежняя проверка смотрела на теги [C###] у чисел и обязательные
заголовки рабочих документов, но не на документ, который реально читает комитет.
Этот модуль проверяет содержание outputs/SIX_PAGER.md по эталону
(knowledge/templates/SIX_PAGER_PROMPT.md):
  1. структура эталона — FAQ-1…6 с подпунктами, без лишних заголовков рабочих документов;
  2. объём основного текста — не больше max_words (quality_gate.json);
  3. остатки шаблона — «заполните», «__%», ячейки «…», «Сегмент 1», «Инициатива 1»,
     абзац-инструкция «KPI в двух направлениях…»;
  4. таблицы — пустые ячейки/«—» в столбцах «Потребности» и «Решения», столбец-дубль
     соседнего, склейки «текст. → цель»;
  5. служебные ID без расшифровки — D###, H#, M#, Q#, WBS P#, «[02, Q4]», 0x_*.md, «C→A»;
  6. арифметика — вклад инициатив в FAQ-5 в сумме 100%, одинаковые метрики (ARPU, CAC,
     порог NSM) совпадают между разделами, «формула → подстановка → результат» сходится;
  7. сноски — процитированное есть в списке источников и наоборот;
  8. язык — в EN-версии нет кириллицы; в RU-версии англицизмы только из белого списка
     глоссария (banned_terms → replace);
  9. предупреждения — абзац длиннее 120 слов, таблица шире 6 столбцов.
Пороги, маркеры и паттерны — config/quality_gate.json → "sixpager" (меняйте там, не в коде).

Подключение: check.run(pdir, sixpager=True) — флаг `pfs check --six-pager`,
автоматически в `pfs check --strict` и в затворе `pfs finish`, если файл существует.
"""
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

from . import core, i18n

_CYRILLIC = re.compile(r"[а-яёА-ЯЁ]")
_CODE_SPAN = re.compile(r"`[^`]*`")
_NUM = r"\d+(?:[.,]\d+)?"
_OPS_SKIP = "×·*/−–—+=≈<>≥≤"
_CUR_SKIP = " \t$€₽"


def _cfg() -> dict:
    gate = core.read_json(core.CONFIG / "quality_gate.json", {})
    sp = gate.get("sixpager")
    return sp if isinstance(sp, dict) else {}


def _fmt_num(v: float) -> str:
    return f"{v:g}"


def _is_sep(cells: list[str]) -> bool:
    return bool(cells) and all(re.match(r"^:?-+:?$", c) for c in cells)


def _tables(lines: list[str]) -> list[dict]:
    """Непрерывные блоки строк-таблиц: {start, rows: [(номер строки, ячейки)]}."""
    blocks, cur = [], None
    for i, ln in enumerate(lines, 1):
        if ln.lstrip().startswith("|"):
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if cur is None:
                cur = {"start": i, "rows": []}
            cur["rows"].append((i, cells))
        elif cur is not None:
            blocks.append(cur)
            cur = None
    if cur is not None:
        blocks.append(cur)
    return blocks


def _data_rows(rows: list[tuple[int, list[str]]]) -> list[tuple[int, list[str]]]:
    """Строки данных: разделитель «---» пропускается, заголовок — строка 1."""
    if len(rows) > 1 and _is_sep(rows[1][1]):
        return rows[2:]
    return rows[1:]


def _paragraphs(lines: list[str]) -> list[tuple[int, str]]:
    """Абзацы для проверки длины: сплошные строки сливаются, элемент списка — свой абзац;
    заголовки, таблицы и цитаты — не абзацы."""
    blocks: list[tuple[int, str]] = []
    cur: list[str] = []
    start = None
    for i, l in enumerate(lines, 1):
        s = l.strip()
        bullet = bool(re.match(r"^([-*]|\d+[.)])\s+", s))
        special = (not s) or l.startswith(("#", "|", ">")) or bullet
        if special:
            if cur:
                blocks.append((start, " ".join(cur)))
                cur, start = [], None
            if bullet:
                blocks.append((i, s))
        else:
            if not cur:
                start = i
            cur.append(s)
    if cur:
        blocks.append((start, " ".join(cur)))
    return blocks


def run(pdir: Path) -> dict:
    """Проверить содержание outputs/SIX_PAGER.md. Файла нет — {checked: False}."""
    result = {"errors": [], "warnings": [], "checked": False, "points": {}}
    path = pdir / "outputs" / "SIX_PAGER.md"
    cfg = _cfg()
    if not path.exists() or not cfg:
        return result
    lang = i18n.lang_of(pdir)
    tr = lambda key, **kw: i18n.t(lang, key, **kw)
    sec = (cfg.get("sections") or {}).get(lang) \
        or (cfg.get("sections") or {}).get("ru") or {}
    if not sec:
        return result
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    plain = [_CODE_SPAN.sub(" ", l) for l in lines]  # инлайн-код — не текст документа
    errs: list[tuple[int, str]] = []
    warns: list[str] = []

    def err(point: int, msg: str) -> None:
        errs.append((point, msg))

    # ---------- 1. Структура по эталону ----------
    faq_nums: list[int] = []
    faq_head: dict[int, int] = {}
    for i, l in enumerate(lines, 1):
        m = re.match(r"^##\s+FAQ-(\d)", l)
        if m:
            n = int(m.group(1))
            faq_nums.append(n)  # все вхождения — дубликат вне порядка тоже нарушение
            if n not in faq_head:
                faq_head[n] = i
        elif re.match(r"^##\s+", l) and not any(a in l for a in (sec.get("extra_h2_allowed") or [])):
            err(1, tr("err_sp_extra_h2", i=i, head=l.lstrip("#").strip()[:60]))
    for n in range(1, 7):
        if n not in faq_head:
            err(1, tr("err_sp_no_section", sec=f"FAQ-{n}"))
    if len(faq_nums) > 1 and faq_nums != sorted(faq_nums):
        err(1, tr("err_sp_bad_order", order=", ".join(f"FAQ-{n}" for n in faq_nums)))
    bounds = sorted(faq_head.items()) + [(10 ** 6, len(lines) + 1)]
    for (n, start), (_, stop) in zip(bounds, bounds[1:]):
        body = "\n".join(lines[start - 1:stop - 1])
        for sub in (sec.get("subpoints") or {}).get(f"FAQ-{n}", []):
            if not re.search(rf"^###\s+{re.escape(sub)}\b", body, re.MULTILINE):
                err(1, tr("err_sp_no_subpoint", faq=f"FAQ-{n}", sub=sub))
    wd_patterns = [re.compile(p) for p in (sec.get("working_doc_headings") or [])]
    for i, l in enumerate(lines, 1):
        m = re.match(r"^#{3,}\s+(.*)", l)
        if m and any(p.search(m.group(1)) for p in wd_patterns):
            err(1, tr("err_sp_working_heading", i=i, head=m.group(1)[:60]))

    # ---------- 2. Объём ----------
    # PRO-46: бюджет основного текста — БЕЗ таблиц и сносок (критерий приёмки):
    # таблицы (матрица тактик, KPI, конкуренты) — данные, не проза документа
    cut = len(lines)
    for i, l in enumerate(lines, 1):
        if l.startswith("#") and any(w in l for w in (sec.get("exclude_from_words") or [])):
            cut = i - 1
            break
    prose = [l for l in lines[:cut] if not l.lstrip().startswith("|")]
    body_words = re.findall(r"[0-9A-Za-zА-Яа-яЁё][0-9A-Za-zА-Яа-яЁё'’-]*", "\n".join(prose))
    max_words = cfg.get("max_words", 3500)
    if len(body_words) > max_words:
        err(2, tr("err_sp_words", n=len(body_words), m=max_words))

    # ---------- 3. Остатки шаблона ----------
    for i, l in enumerate(plain, 1):
        low = l.casefold()
        for marker in (sec.get("template_markers") or []):
            if marker.casefold() in low:
                err(3, tr("err_sp_template", i=i, marker=marker))
        for pat in (sec.get("template_regexes") or []):
            m = re.search(pat, l)
            if m:
                err(3, tr("err_sp_template", i=i, marker=m.group(0)))

    # ---------- 4. Таблицы (+ 9: широкие) ----------
    warn_cols = cfg.get("warn_table_cols", 6)
    req_cols = sec.get("needs_solutions_cols") or []
    for block in _tables(lines):
        rows = block["rows"]
        header = rows[0][1]
        data = _data_rows(rows)
        if len(header) > warn_cols:
            warns.append(tr("warn_sp_wide_table", i=block["start"], n=len(header), m=warn_cols))
        req_idx = [j for j, h in enumerate(header)
                   if any(k.casefold() in h.casefold() for k in req_cols)]
        for i, cells in data:
            if len(cells) != len(header):
                err(4, tr("err_sp_ragged", i=i, n=len(cells), m=len(header)))
            if any(c.startswith("…") for c in cells):
                err(3, tr("err_sp_dots_cell", i=i))
            for j in req_idx:
                if j < len(cells) and cells[j] in ("", "—", "–", "-", "…"):
                    err(4, tr("err_sp_empty_required", i=i, col=header[j]))
            for c in cells:
                if re.search(r"\S\.\s*(?:→|->)", c):
                    err(4, tr("err_sp_glue", i=i))
        if len(data) >= 2:
            for j in range(len(header) - 1):
                col = [(c[j], c[j + 1]) for _, c in data if len(c) == len(header)]
                if col and all(a and b.startswith(a) for a, b in col):
                    err(4, tr("err_sp_dup_col", i=block["start"], col=header[j] or str(j + 1)))
                    break

    # ---------- 5. Служебные ID без расшифровки ----------
    id_patterns = [(name, re.compile(p))
                   for name, p in (cfg.get("service_id_patterns") or {}).items()]
    for i, l in enumerate(plain, 1):
        for name, p in id_patterns:
            hits = list(dict.fromkeys(p.findall(l)))
            if hits:
                err(5, tr("err_sp_service_id", i=i, name=name, ids=", ".join(hits)[:60]))

    # ---------- 6. Арифметика ----------
    # 6a. вклад инициатив в общий результат — сумма 100%
    lead = (sec.get("contrib_lead") or "распределение вклада").casefold()
    for idx, l in enumerate(lines):
        if lead not in l.casefold():
            continue
        vals: list[float] = []
        for nxt in lines[idx + 1:]:
            if not nxt.strip():
                continue  # пустая строка между подводкой и списком — не конец списка
            if not re.match(r"^\s*[-*]\s+", nxt):
                break
            m = re.search(rf"({_NUM})\s*%", nxt)
            if not m:
                break
            vals.append(float(m.group(1).replace(",", ".")))
        if vals:
            total = sum(vals)
            if abs(total - 100) > 0.5:
                err(6, tr("err_sp_contrib_sum", n=_fmt_num(total), m=100))
        break
    # 6b. одни и те же метрики совпадают между разделами
    labels = sec.get("metric_labels") or []
    ignore = [w.casefold() for w in (sec.get("metric_ignore") or [])]
    found: dict[str, dict[float, list[int]]] = {}
    if labels:
        label_re = re.compile(rf"(?i)\b({'|'.join(labels)})\b")
        for i, l in enumerate(plain, 1):
            for m in label_re.finditer(l):
                before = l[max(0, m.start() - 14):m.start()].casefold()
                if any(w in before for w in ignore) or l[max(0, m.start() - 1):m.start()] == "/":
                    continue
                window = l[m.end():m.end() + 16]
                nm = re.search(_NUM, window)
                if not nm:
                    continue
                sep = window[:nm.start()]
                if any(w.casefold() in sep for w in ignore) or any(op in sep for op in _OPS_SKIP):
                    continue
                if any(ch not in _CUR_SKIP for ch in sep):
                    continue
                found.setdefault(m.group(1).upper(), {}) \
                    .setdefault(float(nm.group(0).replace(",", ".")), []).append(i)
    for label, by_val in sorted(found.items()):
        lo, hi = min(by_val), max(by_val)
        if len(by_val) > 1 and (lo == 0 or hi / lo > 1.01):
            detail = "; ".join(f"{_fmt_num(v)} (строки {', '.join(map(str, ls[:4]))})"
                               for v, ls in sorted(by_val.items()))
            err(6, tr("err_sp_metric_mismatch", label=label, values=detail))
    # 6c. формула → подстановка → результат
    calc_cols = sec.get("calc_table_cols") or []
    if len(calc_cols) == 2:
        ops = {"×": "*", "·": "*", "*": "*", "x": "*", "÷": "/", ":": "/", "/": "/",
               "−": "-", "–": "-", "—": "-", "-": "-"}
        for block in _tables(lines):
            header = block["rows"][0][1]
            try:
                ci = next(j for j, h in enumerate(header)
                          if calc_cols[0].casefold() in h.casefold())
                ri = next(j for j, h in enumerate(header)
                          if calc_cols[1].casefold() in h.casefold())
            except StopIteration:
                continue
            for i, cells in _data_rows(block["rows"]):
                if len(cells) <= max(ci, ri):
                    continue
                tail = cells[ci].rsplit("=", 1)[-1]
                m = re.search(rf"({_NUM})\s*([×·*x÷:/−–—-])\s*({_NUM})", tail)
                if not m:
                    continue
                a, b = (float(m.group(k).replace(",", ".")) for k in (1, 3))
                op = ops.get(m.group(2))
                if not op:
                    continue
                got = a * b if op == "*" else a / b if op == "/" else a - b
                rm = re.search(_NUM, cells[ri])
                if not rm:
                    continue
                res = float(rm.group(0).replace(",", "."))
                if abs(got - res) > max(0.011, 0.01 * abs(res)):
                    err(6, tr("err_sp_calc_mismatch", i=i,
                              expr=f"{_fmt_num(a)} {m.group(2)} {_fmt_num(b)} = {_fmt_num(got)}",
                              res=_fmt_num(res)))

    # ---------- 7. Сноски ----------
    fn_idx = next((k for k, l in enumerate(lines)
                   if l.startswith("#") and (sec.get("footnotes_heading") or "Источники") in l),
                  None)
    if fn_idx is None:
        cited = set(re.findall(r"\[(S\d{3})\]", text))
        if cited:
            err(7, tr("err_sp_no_footnotes", ids=", ".join(sorted(cited))))
    else:
        # PRO-46: текст six-pager пишет writer по спецификации (PRO-49) — маркеры [^N]
        # в тексте и определения `[^N]: **S###** …` внизу. Источники определений —
        # цитированные наравне с прямыми тегами [S###]: документ комитета проходит
        # пункт 7, когда список источников совпадает с процитированным.
        body_text = "\n".join(lines[:fn_idx])
        cited = set(re.findall(r"\[(S\d{3})\]", body_text)) \
            | set(re.findall(r"\[\^\d+\]:\s*\*{0,2}(S\d{3})\*{0,2}", text))
        listed = set(re.findall(r"\bS\d{3}\b", "\n".join(lines[fn_idx:])))
        if cited - listed:
            err(7, tr("err_sp_footnote_not_listed", ids=", ".join(sorted(cited - listed))))
        if listed - cited:
            err(7, tr("err_sp_footnote_not_cited", ids=", ".join(sorted(listed - cited))))

    # ---------- 8. Язык ----------
    en_name = cfg.get("en_file") or "SIX_PAGER_EN.md"
    lang_targets = [pdir / "outputs" / en_name] if lang == "ru" else [path]
    for tp in lang_targets:
        if not tp.exists():
            continue
        cyr = [(k, l.strip()[:70])
               for k, l in enumerate(tp.read_text(encoding="utf-8").splitlines(), 1)
               if _CYRILLIC.search(l)]
        if cyr:
            shown = ", ".join(str(k) for k, _ in cyr[:5]) + (", …" if len(cyr) > 5 else "")
            err(8, tr("err_sp_cyrillic", name=tp.name, lines=shown, n=len(cyr), sample=cyr[0][1]))
    gate = core.read_json(core.CONFIG / "quality_gate.json", {})
    block = gate.get(lang) if isinstance(gate.get(lang), dict) and "banned_terms" in gate.get(lang, {}) \
        else gate.get("ru", {})
    for term, instead in (((block or {}).get("banned_terms") or {}).get("replace") or {}).items():
        first = next((i for i, l in enumerate(plain, 1)
                      if re.search(rf"(?<![\w-]){re.escape(term)}\w*", l, re.IGNORECASE)), None)
        if first is not None:
            err(8, tr("err_sp_banned_term", i=first, term=term, instead=instead))

    # ---------- 9. Предупреждения: длинные абзацы ----------
    limit = cfg.get("warn_paragraph_words", 120)
    for i, chunk in _paragraphs(lines):
        if chunk.startswith("[^"):  # определения сносок — не проза документа
            continue
        n = len(re.findall(r"\S+", chunk))
        if n > limit:
            warns.append(tr("warn_sp_long_para", i=i, n=n, m=limit))

    result["checked"] = True
    result["errors"] = [msg for _, msg in errs]
    result["warnings"] = warns
    result["points"] = dict(Counter(str(p) for p, _ in errs))
    return result
