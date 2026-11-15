"""Роудмапы в xlsx: «по проектам» и «по фичам/по проектам» (PRO-70).

Формат — по быстрым гибким роудмапам из Google Sheets (примеры сообщества,
docs.google.com: 1_5JfMrDrB6ck3ktg2AQ3xdZhH0AV54GiuAeFtDZkbXI, 1fHx2KaTBlwK-Uf3hL6czCwSzsKxEF9cso8X19XavQw0):
- лист «Проекты» (по проектам): строки — проекты/этапы; колонки Проект | Инициатива |
  Команда | Старт | Завершение | Периоды | Описание | Приоритет | Фаза | Статус |
  Комментарий, справа — колонки периодов (кварталы по умолчанию; --granularity
  week|month|quarter), где отрезок задачи отмечен заливкой-баром;
- лист «Фичи по проектам»: строки — фичи, сгруппированные по проектам (аналог
  «Initiative Sprint | Breakdown | Primary Team | … | Status | Risk»); те же бары,
  длительность в неделях считается из дат.

Как отмечаются задачи: заливка периода цветом статуса (зелёный — сделано,
жёлтый — в работе, синий — запланировано, красный — риск, серый — неизвестный
статус) плюс колонка «Статус». Лист «Легенда» расшифровывает цвета и источник.

Данные берутся из pfs-проекта, не руками:
- сначала projects/<slug>/roadmap.json — простая спецификация:
  {"granularity": "quarter", "projects": [{"name": …, "start": "2026-Q1",
   "end": "2026-Q2", "status": "в работе", "features": [{"name": …, "status": …}]}]};
  фичи наследуют проект (team/status/phase/даты), даты: YYYY-QN, YYYY-MM-DD,
  YYYY-MM, YYYY, DD.MM.YYYY;
- иначе — outputs/04_product_strategy.md: этапы outcome-роадмапа
  («- **Этап 1 (…):** тактики … **Результат …:** …») становятся проектами,
  тактики внутри этапа — фичами; дат в 04 нет, поэтому по умолчанию этапы
  раскладываются по последовательным кварталам от текущего со статусом «план».

Запуск: pfs roadmap [--spec FILE] [--granularity week|month|quarter]
→ outputs/roadmap-<slug>.xlsx. Писатель — tools/pfs/xlsx.py (stdlib, ноль зависимостей).
"""
from __future__ import annotations

import calendar
import datetime as dt
import re
from pathlib import Path

from . import core
from .xlsx import Workbook

GRANULARITIES = ("week", "month", "quarter")

# Статус → цвет заливки; нормализация — нижний регистр, пробелы/подчёркивания схлопнуты.
STATUS_FILL = {
    "done": "green", "completed": "green", "сделано": "green", "готово": "green",
    "завершено": "green", "выполнено": "green",
    "in progress": "yellow", "in-progress": "yellow", "в работе": "yellow",
    "идёт": "yellow", "идет": "yellow",
    "planned": "blue", "not started": "blue", "not-started": "blue", "запланировано": "blue",
    "не начато": "blue", "план": "blue", "discovery": "blue", "design": "blue", "дизайн": "blue",
    "risk": "red", "at risk": "red", "potential risk": "red", "риск": "red",
}

_DATE_RES = (
    re.compile(r"^(\d{4})-Q([1-4])$", re.IGNORECASE),
    re.compile(r"^(\d{4})-(\d{1,2})-(\d{1,2})$"),
    re.compile(r"^(\d{4})-(\d{1,2})$"),
    re.compile(r"^(\d{4})$"),
    re.compile(r"^(\d{1,2})\.(\d{1,2})\.(\d{4})$"),
)

# Этап outcome-роадмапа в 04: «- **Этап 1 (бета):** тактики … **Результат …:** …»
_STAGE_RE = re.compile(r"^-\s*\*\*(.+?):\*\*\s*(.+)$")
_RESULT_RE = re.compile(r"\*\*Результат[^*]*\*\*:?\s*", re.IGNORECASE)
_STAGE_PREFIX = ("этап", "инициатив", "драйвер", "фаза")

MAX_PERIODS = 120  # предохранитель: шире — опечатка в датах, а не роудмап


def _norm_status(value) -> str:
    return re.sub(r"[\s_]+", " ", str(value or "").strip().lower())


def fill_of(status: str) -> str:
    """Цвет заливки статуса; неизвестный статус — серый."""
    return STATUS_FILL.get(_norm_status(status), "gray")


def parse_date(value, as_end: bool = False) -> dt.date:
    """YYYY-QN | YYYY-MM-DD | YYYY-MM | YYYY | DD.MM.YYYY → дата.
    as_end=True: неполная дата — конец периода («2026-03» → 31 марта), не 1-е число:
    отрезок задачи до «марта» должен покрывать весь месяц."""
    s = str(value).strip()
    m = _DATE_RES[0].match(s)
    if m:
        q = int(m.group(2))
        if as_end:
            y = int(m.group(1))
            return _eom(y, q * 3)
        return dt.date(int(m.group(1)), q * 3 - 2, 1)
    for i, rx in enumerate(_DATE_RES[1:4], 1):
        m = rx.match(s)
        if m:
            y = int(m.group(1))
            if len(m.groups()) == 1:  # только год: «2026»
                return dt.date(y, 12, 31) if as_end else dt.date(y, 1, 1)
            mo = int(m.group(2))
            if i == 1:
                d = int(m.group(3))
                if 1 <= mo <= 12 and 1 <= d <= 31:
                    return dt.date(y, mo, d)
                break
            if not 1 <= mo <= 12:
                break
            if as_end:
                return _eom(y, mo) if i == 2 else dt.date(y, 12, 31)
            return dt.date(y, mo, 1)
    m = _DATE_RES[4].match(s)
    if m:
        d, mo, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if 1 <= mo <= 12 and 1 <= d <= 31:
            return dt.date(y, mo, d)
    raise core.PfsError(f"не разобрать дату роудмапа: {s!r} "
                        "(форматы: YYYY-QN, YYYY-MM-DD, YYYY-MM, YYYY, DD.MM.YYYY)")


def _month_add(y: int, m: int, k: int) -> tuple[int, int]:
    t = y * 12 + m - 1 + k
    return t // 12, t % 12 + 1


def _eom(y: int, m: int) -> dt.date:
    return dt.date(y, m, calendar.monthrange(y, m)[1])


def make_periods(start: dt.date, end: dt.date, granularity: str) -> list[tuple[str, dt.date, dt.date]]:
    """Периоды (метка, первый день, последний день) от start до end:
    week — ISO-недели (понедельник–воскресенье), month — календарные месяцы,
    quarter — кварталы. Горизонт шире MAX_PERIODS — ошибка (опечатка в датах)."""
    if start > end:
        raise core.PfsError(f"диапазон роудмапа перевёрнут: {start} позже {end}")
    gran = (granularity or "").lower()
    out: list[tuple[str, dt.date, dt.date]] = []
    if gran == "quarter":
        y, m = start.year, (start.month - 1) // 3 * 3 + 1
        while True:
            qy, qm = _month_add(y, m, 2)
            p_end = _eom(qy, qm)
            out.append((f"Q{(m - 1) // 3 + 1} {y}", dt.date(y, m, 1), p_end))
            if p_end >= end:
                break
            y, m = _month_add(y, m, 3)
    elif gran == "month":
        y, m = start.year, start.month
        while True:
            p_end = _eom(y, m)
            out.append((f"{y}-{m:02d}", dt.date(y, m, 1), p_end))
            if p_end >= end:
                break
            y, m = _month_add(y, m, 1)
    elif gran == "week":
        cur = start - dt.timedelta(days=start.isoweekday() - 1)  # понедельник недели старта
        while cur <= end:
            iso = cur.isocalendar()
            out.append((f"{iso[0]}-W{iso[1]:02d}", cur, cur + dt.timedelta(days=6)))
            cur += dt.timedelta(days=7)
    else:
        raise core.PfsError(f"granularity: неделя/месяц/квартал — {', '.join(GRANULARITIES)}")
    if len(out) > MAX_PERIODS:
        raise core.PfsError(f"слишком широкий горизонт: {len(out)} периодов — проверьте даты")
    return out


def _covered(s: dt.date | None, e: dt.date | None, periods) -> set[int]:
    """Индексы периодов, пересекающихся с отрезком [s, e]."""
    if not s or not e:
        return set()
    return {i for i, (_, a, b) in enumerate(periods) if a <= e and b >= s}


def _clean(s: str) -> str:
    """Маркдаун-жирный снять, края почистить (точки/тире — оформление списка, не имя)."""
    return re.sub(r"\*\*", "", s).strip(" \t.;,–—-").strip()


def _features_from_tactics(blob: str) -> list[dict]:
    return [{"name": t, "status": "план"} for t in (t for t in map(_clean, blob.split(";")) if t)]


def spec_from_strategy(pdir: Path) -> dict:
    """Спецификация из 04: этапы outcome-роадмапа → проекты, тактики → фичи.
    Дат в 04 нет: этапы раскладываются по последовательным кварталам от текущего,
    статус «план» (уточняйте в roadmap.json — см. Легенду в книге)."""
    path = pdir / "outputs" / "04_product_strategy.md"
    if not path.exists():
        raise core.PfsError(f"нет входных данных роудмапа: нет {path} и нет roadmap.json "
                            "— создайте roadmap.json (pfs roadmap --spec) или заполните outcome-роадмап в 04")
    meta = core.read_json(pdir / "project.json", {})
    title = str(meta.get("title") or "Стратегия")
    today = dt.date.today()
    projects = []
    for ln in path.read_text(encoding="utf-8").splitlines():
        m = _STAGE_RE.match(ln.strip())
        if not m:
            continue
        label, body = m.group(1).strip(), m.group(2).strip()
        if not _norm_status(label).startswith(_STAGE_PREFIX):
            continue
        parts = _RESULT_RE.split(body, maxsplit=1)
        blob, gate = parts[0].strip(), (parts[1].strip() if len(parts) > 1 else "")
        k = len(projects)
        projects.append({
            "name": label,
            "initiative": title,
            "start": _q_label(today, k), "end": _q_label(today, k),
            "status": "план",
            "description": _clean(re.split(r"[.]", blob)[0]) if blob else "",
            "comment": f"Результат: {_clean(gate)}" if gate else "",
            "features": _features_from_tactics(blob),
        })
    if not projects:
        raise core.PfsError("в 04_product_strategy.md нет этапов outcome-роадмапа "
                            "(«- **Этап 1 (…):** тактики… **Результат …:** …») — "
                            "заполните роадмап в 04 или дайте pfs roadmap --spec roadmap.json")
    return {"projects": projects}


def _q_label(d: dt.date, k: int) -> str:
    t = d.year * 12 + d.month - 1 + 3 * k
    return f"{t // 12}-Q{t % 12 // 3 + 1}"


def normalize_spec(data: dict) -> dict:
    """Нормализация спецификации: наследование фичами проекта (team/status/phase/
    даты), даты проекта — min/max по фичам, статусы и имена обязательны."""
    projects = data.get("projects")
    if not isinstance(projects, list) or not projects:
        raise core.PfsError("в спецификации роудмапа нет projects: "
                            '[{"name": …, "start": …, "end": …, "features": [{"name": …}]}]')
    out = []
    for pr in projects:
        if not isinstance(pr, dict) or not str(pr.get("name") or "").strip():
            raise core.PfsError("у каждого проекта в спецификации роудмапа должно быть имя (name)")
        feats = []
        for f in pr.get("features") or []:
            if not isinstance(f, dict) or not str(f.get("name") or "").strip():
                raise core.PfsError(f"у фич проекта «{pr['name']}» должно быть имя (name)")
            feats.append({
                "name": str(f["name"]).strip(),
                "team": str(f.get("team") or pr.get("team") or ""),
                "start": f.get("start") or pr.get("start"),
                "end": f.get("end") or pr.get("end"),
                "status": str(f.get("status") or pr.get("status") or "план"),
                "risk": str(f.get("risk") or ""),
                "phase": str(f.get("phase") or pr.get("phase") or ""),
                "comment": str(f.get("comment") or ""),
            })
        f_starts = [parse_date(f["start"]) for f in feats if f.get("start")]
        f_ends = [parse_date(f["end"], as_end=True) for f in feats if f.get("end")]
        p_start = pr.get("start") or (str(min(f_starts)) if f_starts else None)
        p_end = pr.get("end") or (str(max(f_ends)) if f_ends else None)
        out.append({
            "name": str(pr["name"]).strip(),
            "initiative": str(pr.get("initiative") or "").strip(),
            "team": str(pr.get("team") or ""),
            "priority": str(pr.get("priority") or ""),
            "phase": str(pr.get("phase") or ""),
            "status": str(pr.get("status") or (feats[0]["status"] if feats else "план")),
            "description": str(pr.get("description") or ""),
            "comment": str(pr.get("comment") or ""),
            "start": p_start,
            "end": p_end,
            "features": feats,
        })
    return {"title": str(data.get("title") or ""), "granularity": data.get("granularity"), "projects": out}


def load_spec(pdir: Path, spec: str | Path | None = None) -> tuple[dict, str]:
    """Вход роудмапа: --spec файл (путь: каталог проекта → cwd), затем
    projects/<slug>/roadmap.json, иначе этапы 04. → (нормализованная спецификация, источник)."""
    path = core.resolve_input(spec, pdir) if spec else pdir / "roadmap.json"
    if path.exists():
        data = core.read_json(path)
        if not isinstance(data, dict):
            raise core.PfsError(f"{path}: спецификация роудмапа — JSON-объект, а не список")
        return normalize_spec(data), "roadmap.json"
    return normalize_spec(spec_from_strategy(pdir)), "04_product_strategy.md"


def _span_row(pr: dict, periods) -> tuple[dt.date | None, dt.date | None, str, str]:
    """Даты проекта, метка covered-диапазона, цвет статуса."""
    s = parse_date(pr["start"]) if pr.get("start") else None
    e = parse_date(pr["end"], as_end=True) if pr.get("end") else None
    cov = _covered(s, e, periods)
    label = f"{periods[min(cov)][0]}–{periods[max(cov)][0]}" if cov else ""
    return s, e, label, fill_of(pr["status"])


def _gantt(periods, cov: set[int], fill: str) -> list:
    """Колонки-периоды: заливка на покрытых, None на пустых."""
    return [{"fill": fill} if i in cov else None for i in range(len(periods))]


def _weeks(s: dt.date | None, e: dt.date | None):
    """Длительность в неделях (ceil), без дат — пустая строка."""
    if not s or not e:
        return ""
    return max(1, -((s - e).days // 7))


def build_workbook(spec: dict, granularity: str | None = None) -> Workbook:
    """Книга роудмапа: «Проекты», «Фичи по проектам», «Легенда»."""
    gran = (granularity or spec.get("granularity") or "quarter").lower()
    projects = spec["projects"]
    spans = []
    for pr in projects:
        if pr.get("start") and pr.get("end"):
            spans.append((parse_date(pr["start"]), parse_date(pr["end"], as_end=True)))
        for f in pr["features"]:
            if f.get("start") and f.get("end"):
                spans.append((parse_date(f["start"]), parse_date(f["end"], as_end=True)))
    if not spans:
        raise core.PfsError("в спецификации роудмапа нет дат (start/end) — нечем построить колонки периодов")
    periods = make_periods(min(a for a, _ in spans), max(b for _, b in spans), gran)

    wb = Workbook()
    labels = [lbl for lbl, _, _ in periods]
    sh = wb.sheet("Проекты", widths={1: 22, 2: 22, 3: 12, 4: 12, 5: 12, 6: 18, 7: 36,
                                     8: 10, 9: 12, 10: 12, 11: 26,
                                     **{11 + i: 11 for i in range(1, len(periods) + 1)}})
    sh.row(*[{"v": h, "bold": True} for h in
             ["Проект", "Инициатива", "Команда", "Старт", "Завершение", "Периоды", "Описание",
              "Приоритет", "Фаза", "Статус", "Комментарий"] + labels])
    for pr in projects:
        s, e, span, fill = _span_row(pr, periods)
        cov = _covered(s, e, periods)
        sh.row(pr["name"], pr.get("initiative") or "", pr.get("team") or "",
               str(s) if s else "", str(e) if e else "", span,
               pr.get("description") or "", pr.get("priority") or "", pr.get("phase") or "",
               {"v": pr["status"], "fill": fill, "bold": True}, pr.get("comment") or "",
               *_gantt(periods, cov, fill))

    fsh = wb.sheet("Фичи по проектам", widths={1: 20, 2: 36, 3: 12, 4: 12, 5: 12, 6: 10,
                                               7: 12, 8: 12, 9: 26,
                                               **{9 + i: 11 for i in range(1, len(periods) + 1)}})
    fsh.row(*[{"v": h, "bold": True} for h in
              ["Проект", "Фича", "Команда", "Старт", "Завершение", "Длительность (нед)",
               "Статус", "Риск", "Комментарий"] + labels])
    for pr in projects:
        for f in pr["features"]:
            s = parse_date(f["start"]) if f.get("start") else None
            e = parse_date(f["end"], as_end=True) if f.get("end") else None
            fill = fill_of(f["status"])
            fsh.row(pr["name"], f["name"], f.get("team") or "",
                    str(s) if s else "", str(e) if e else "", _weeks(s, e),
                    {"v": f["status"], "fill": fill, "bold": True}, f.get("risk") or "",
                    f.get("comment") or "", *_gantt(periods, _covered(s, e, periods), fill))

    lg = wb.sheet("Легенда", widths={1: 18, 2: 70})
    lg.row({"v": "Роудмап — как читать и править", "bold": True})
    lg.row("Формат", "гибкий роудмап из Google Sheets: лист «Проекты» — по проектам, "
                     "«Фичи по проектам» — фичи, сгруппированные по проектам; отрезки задач "
                     "отмечены заливкой в колонках периодов справа")
    lg.row("Периоды", f"шаг колонок: {gran}; меняется флагом pfs roadmap --granularity week|month|quarter")
    lg.row("Данные", "источник: projects/<slug>/roadmap.json или этапы outcome-роадмапа из "
                     "04_product_strategy.md; для этапов из 04 даты — раскладка по кварталам (план)")
    lg.row({"v": "план", "fill": "blue", "bold": True}, "синий — запланировано (not started / planned)")
    lg.row({"v": "в работе", "fill": "yellow", "bold": True}, "жёлтый — в работе (in progress)")
    lg.row({"v": "сделано", "fill": "green", "bold": True}, "зелёный — сделано (done / completed)")
    lg.row({"v": "риск", "fill": "red", "bold": True}, "красный — риск (at risk / potential risk); серый — неизвестный статус")
    lg.row("Правка", "проекты/фичи/даты/статусы — projects/<slug>/roadmap.json "
                     '({"projects": [{"name", "start", "end", "status", "features": [...]}]}), затем pfs roadmap; '
                     "пересобирается поверх — ручные правки xlsx не сохраняйте")
    return wb


def run(pdir: Path, spec: str | Path | None = None, granularity: str | None = None) -> Path:
    """Собрать outputs/roadmap-<slug>.xlsx и записать в журнал."""
    data, source = load_spec(pdir, spec)
    wb = build_workbook(data, granularity)
    out = wb.save(pdir / "outputs" / f"roadmap-{pdir.name}.xlsx")
    n_feats = sum(len(p["features"]) for p in data["projects"])
    core.log(pdir, "action", f"Роудмап: outputs/roadmap-{pdir.name}.xlsx "
             f"(проектов: {len(data['projects'])}, фич: {n_feats}; источник: {source})",
             tool="pfs roadmap")
    return out
