"""Сборка итогового отчёта: документы + реестр утверждений + источники + решения + стоимость."""
from __future__ import annotations

import html as html_mod
import re
from pathlib import Path

from . import calc, check, claims as claims_mod, core, cost, decisions, sources as src_mod

ORDER = ["00_brief.md", "01_research_plan.md", "02_situation.md", "03_options.md", "04_product_strategy.md",
         "05_comms_strategy.md", "06_validation_plan.md", "07_quality_review.md"]


def build(pdir: Path) -> Path:
    meta = core.read_json(pdir / "project.json", {})
    parts = [f"# {meta.get('title')}: стратегия и обоснование", "",
             f"> Собрано {core.now()[:16]} командой `pfs export`. Теги [C###] — утверждения, [S###] — источники, [D###] — решения (см. приложения).", ""]
    outs = pdir / "outputs"
    for name in ORDER + sorted(p.name for p in outs.glob("*.md") if p.name not in ORDER and p.name != "REPORT.md"):
        p = outs / name
        if p.exists():
            body = p.read_text(encoding="utf-8")
            parts += [body.replace("\n# ", "\n## ") if not body.startswith("# ") else "#" + body, "", "---", ""]
    active = [c for c in claims_mod.load(pdir)]
    parts += ["# Приложение A. Реестр утверждений", "", claims_mod.table(active), ""]
    parts += ["# Приложение B. Источники", "", "| ID | Название | Ссылка / файл | Происхождение | Получено |", "|---|---|---|---|---|"]
    for s in src_mod.load(pdir):
        parts.append(f"| {s['id']} | {s['title'].replace('|', '/')} | {s.get('url') or s.get('path') or '—'} | {s['origin']} | {s['retrieved'][:10]} |")
    decs = decisions.load(pdir)
    if decs:
        parts += ["", "# Приложение C. Решения и обязательства", "", decisions.table(decs)]
    att = attachments_table(pdir)
    if att:
        parts += ["", "# Приложение E. Excel-расчёты", "", att]
    qc = check.run(pdir)
    parts += ["", "# Приложение D. Прозрачность", "", "```", cost.summary_text(pdir), check.report_text(qc), "```"]
    path = outs / "REPORT.md"
    core.atomic_write(path, "\n".join(parts) + "\n")
    core.log(pdir, "action", "Собран outputs/REPORT.md", tool="pfs export")
    return path


# ---------- six-pager (FAQ-1…FAQ-6) с Excel-приложениями ----------

ATTACHMENTS = [
    ("unit_economics.xlsx", "Ввод · Юнит-экономика · Чувствительность", "ARPU, VC, CAC, отток"),
    ("growth_model.xlsx", "Ввод · Модель 12 мес", "MAU, рост, конверсия, AOV, take rate"),
    ("cohort_retention.xlsx", "Ввод · Когорты · Метрики удержания", "размеры когорт, кривая удержания"),
    ("market_sizing.xlsx", "Ввод · Воронка · PESTEL", "PAM, доли воронки, факторы среды"),
]


def attachments_table(pdir: Path) -> str | None:
    """Маркдаун-таблица приложений или None, если ничего не собрано."""
    att = pdir / "outputs" / "attachments"
    rows = [f"| {fname} | {sheets} | {edit} |" for fname, sheets, edit in ATTACHMENTS
            if (att / fname).exists()]
    if not rows:
        return None
    return "| Файл | Листы | Что редактировать |\n|---|---|---|\n" + "\n".join(rows)


def _grab(pdir: Path, fname: str, sections: tuple[str, ...], cap: int = 6000) -> str | None:
    """Секции документа по заголовкам; без совпадений — весь документ; нет файла — None."""
    path = pdir / "outputs" / fname
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    parts = []
    for nm in sections:
        if check._has_section(text, nm):
            body = check._section_body(text, nm).strip()
            if body:
                parts.append(f"### {nm}\n\n{body}")
    body = "\n\n".join(parts) if parts else text.strip()
    if len(body) > cap:
        body = body[:cap] + f"\n\n… обрезано, полностью — `{fname}`"
    return body


def build_six_pager(pdir: Path, with_calcs: bool = True) -> Path:
    """Six-pager в структуре референса (FAQ-1…FAQ-6) + Excel-приложения (outputs/attachments)."""
    if with_calcs:
        calc.run(pdir, "all")
    meta = core.read_json(pdir / "project.json", {})
    parts = [f"# {meta.get('title')}: six-pager", "",
             f"> Собрано {core.now()[:16]} командой `pfs export --six-pager`. Теги [C###]/[S###] — "
             "происхождение чисел (полный реестр в REPORT.md).", "",
             f"**Запрос:** {meta.get('question', '')}", ""]
    faq1 = _grab(pdir, "02_situation.md", ("Короткий ответ", "Что известно", "Противоречия", "Чего не знаем"))
    parts += ["## FAQ-1. Анализ текущего состояния", "",
              faq1 or "> Раздел появится после шага «situation» (02_situation.md).", ""]
    faq2 = _grab(pdir, "02_situation.md", ("Сегменты", "Персоны", "Аудитория"), 3000)
    if not faq2 or len(faq2) < 120:
        faq2 = _grab(pdir, "04_product_strategy.md", ("Аудитория",), 3000)
    parts += ["## FAQ-2. Пользователи: сегменты и персоны", "",
              faq2 or "> Добавьте сегменты/персоны в 02_situation.md.", ""]
    faq3 = _grab(pdir, "03_options.md", (), 7000)
    parts += ["## FAQ-3. Стратегические инициативы (варианты и возражения)", "",
              faq3 or "> Раздел появится после шага «options» (03_options.md).", ""]
    faq4 = _grab(pdir, "04_product_strategy.md", ("Тактики", "Инициативы"), 4000) \
        or _grab(pdir, "03_options.md", ("Тактики",), 4000)
    parts += ["## FAQ-4. Тактики", "",
              faq4 or "> Добавьте тактики по каждой инициативе в 04_product_strategy.md.", ""]
    faq5 = _grab(pdir, "06_validation_plan.md", (), 5000)
    parts += ["## FAQ-5. План реализации и проверки", "",
              faq5 or "> Раздел появится после шага «validation» (06_validation_plan.md).", ""]
    faq6 = _grab(pdir, "04_product_strategy.md", ("Метрики", "Показатели"), 3000)
    if not faq6 or len(faq6) < 80:
        faq6 = _grab(pdir, "06_validation_plan.md", ("Ожидаемое изменение", "Критерии решения"), 3000)
    parts += ["## FAQ-6. Метрики успеха", "", faq6 or "> Добавьте метрики успеха в 04/06 документы.", ""]
    parts += ["## Приложения (Excel)", "", attachments_table(pdir) or "> Ещё нет: `pfs calc all`.", "",
              "", "> Формулы пересчитываются при открытии (Excel / Numbers / LibreOffice). "
                  "Полная версия с доказательствами — REPORT.md."]
    path = pdir / "outputs" / "SIX_PAGER.md"
    core.atomic_write(path, "\n".join(parts) + "\n")
    core.log(pdir, "action", "Собран outputs/SIX_PAGER.md", tool="pfs export --six-pager")
    return path


# ---------- HTML-дека 16:9 из six-pager ----------

_MAX_POINTS = 6   # тезисов на слайд
_POINT_CAP = 160  # символов на тезис

_DECK_CSS = """
  :root { --bg: #070b13; --fg: #e8eef8; --a1: #4fd1c5; --a2: #8b7bff; --dim: #9aa7bd; }
  * { box-sizing: border-box; }
  html { scroll-snap-type: y mandatory; }
  body { margin: 0; background: var(--bg); color: var(--fg);
         font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; }
  section.slide { width: 100vw; height: auto; aspect-ratio: 16/9; min-height: 100vh;
                  max-height: 100vh; scroll-snap-align: start; scroll-snap-stop: always;
                  display: flex; flex-direction: column; justify-content: center; gap: .6em;
                  padding: clamp(24px, 6vw, 80px); overflow: hidden;
                  border-bottom: 1px solid rgba(139, 123, 255, .18); }
  h1, h2 { margin: 0; line-height: 1.15; font-weight: 700;
           background: linear-gradient(90deg, var(--a1), var(--a2));
           -webkit-background-clip: text; background-clip: text; color: transparent; }
  h1 { font-size: clamp(28px, 5vw, 56px); }
  h2 { font-size: clamp(22px, 3.6vw, 40px); }
  ul { margin: 0; padding-left: 1.2em; display: flex; flex-direction: column; gap: .45em;
       font-size: clamp(15px, 2vw, 24px); }
  li::marker { color: var(--a1); }
  p { margin: 0; font-size: clamp(15px, 2vw, 24px); color: var(--fg); }
  .query { color: var(--dim); font-size: clamp(16px, 2.2vw, 26px); }
  .query b { color: var(--a1); }
"""


def _points(body: str) -> list[str]:
    """Тезисы слайда: маркеры списков и первые предложения абзацев (≤6, ≤160 символов)."""
    pts: list[str] = []
    for raw in body.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or set(line) <= set("-|: "):
            continue
        if line.startswith("|"):  # строка таблицы — первый столбец
            line = [c.strip() for c in line.strip("|").split("|")][0]
        line = re.sub(r"^[-*+]\s+", "", line)
        line = re.sub(r"^>\s?", "", line)
        sentence = re.split(r"(?<=[.!?…])\s+", line)[0]
        if len(sentence) > _POINT_CAP:
            sentence = sentence[:_POINT_CAP - 1].rstrip() + "…"
        if sentence and (not pts or sentence != pts[-1]):
            pts.append(sentence)
        if len(pts) >= _MAX_POINTS:
            break
    return pts


def _slide(title: str, points: list[str], cls: str = "") -> str:
    """Секция-слайд: заголовок + один тезис — один пункт."""
    body = ""
    if points:
        items = "".join(f"<li>{html_mod.escape(p)}</li>" for p in points)
        body = f"<ul>{items}</ul>"
    k = f' class="{cls}"' if cls else ""
    return f'<section class="slide"{k}>\n<h2>{html_mod.escape(title)}</h2>\n{body}\n</section>'


def build_deck(pdir: Path) -> Path:
    """HTML-дека 16:9 из outputs/SIX_PAGER.md (тёмная тема, один тезис на слайд)."""
    src = pdir / "outputs" / "SIX_PAGER.md"
    if not src.exists():
        raise core.PfsError("Сначала соберите six-pager: pfs export --six-pager")
    text = src.read_text(encoding="utf-8")
    meta = core.read_json(pdir / "project.json", {})
    q = re.search(r"^\*\*Запрос:\*\*\s*(.+)$", text, flags=re.M)
    query = q.group(1).strip() if q else meta.get("question", "")
    h1 = re.search(r"^#\s+(.+)$", text, flags=re.M)
    title = h1.group(1).strip() if h1 else meta.get("title", "Six-pager")
    sections = re.split(r"^##\s+", text, flags=re.M)[1:]
    slides = ['<section class="slide title-slide">\n'
              f"<h1>{html_mod.escape(title)}</h1>\n"
              f'<p class="query"><b>Запрос:</b> {html_mod.escape(query)}</p>\n</section>']
    for sec in sections:
        head, _, body = sec.partition("\n")
        head = head.strip()
        if head:
            slides.append(_slide(head, _points(body)))
    doc = ("<!doctype html>\n<html lang=\"ru\">\n<head>\n<meta charset=\"utf-8\">\n"
           f"<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
           f"<title>{html_mod.escape(title)}</title>\n<style>{_DECK_CSS}</style>\n"
           f"</head>\n<body>\n" + "\n".join(slides) + "\n</body>\n</html>\n")
    path = pdir / "outputs" / "presentations" / "deck.html"
    core.atomic_write(path, doc)
    core.log(pdir, "action", "Собран outputs/presentations/deck.html", tool="pfs export --deck")
    return path
