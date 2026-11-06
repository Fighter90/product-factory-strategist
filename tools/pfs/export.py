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
    qc = check.run(pdir)
    parts += ["", "# Приложение D. Прозрачность", "", "```", cost.summary_text(pdir), check.report_text(qc), "```"]
    att = attachments_table(pdir)
    if att:
        parts += ["", "# Приложение E. Excel-расчёты", "", att]
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


def _grab(pdir: Path, fname: str, sections: tuple[str, ...], cap: int = 6000,
          require_section: bool = False) -> str | None:
    """Секции документа по заголовкам; без совпадений — весь документ (или None при
    require_section=True); нет файла — None."""
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
    if require_section and not parts:
        return None
    body = "\n\n".join(parts) if parts else text.strip()
    if len(body) > cap:
        body = body[:cap] + f"\n\n… обрезано, полностью — `{fname}`"
    return body


def _flat(v) -> str:
    """Любое значение → компактная строка (строки как есть; dict → 'k: x'; None/пустое → '')."""
    if v is None:
        return ""
    if isinstance(v, str):
        return v.strip()
    if isinstance(v, dict):
        return ", ".join(f"{k}: {x}" for k, x in v.items() if x not in (None, "", []))
    if isinstance(v, (list, tuple)):
        return ", ".join(_flat(x) for x in v if x not in (None, "", []))
    return str(v)


def _sources_footnotes(pdir: Path, cap: int = 14) -> str | None:
    """Сноски-источники: нумерованный список S### — название — URL (как в референсе)."""
    rows = core.read_jsonl(pdir / "sources.jsonl")
    if not rows:
        return None
    lines = []
    for i, r in enumerate(rows[:cap], 1):
        rid = r.get("id", f"S{i:03d}")
        title = _flat(r.get("title"))
        url = _flat(r.get("url"))
        tail = f" — {url}" if url else ""
        lines.append(f"{i}. **{rid}** — {title}{tail}")
    if len(rows) > cap:
        lines.append(f"… ещё {len(rows) - cap} источников — sources.jsonl")
    return "\n".join(lines)


def _unit_econ_block(pdir: Path) -> str | None:
    """Пошаговая юнит-экономика из calcs.json (unit_econ): CM, LTV, LTV/CAC, окупаемость."""
    cfg = core.read_json(pdir / "calcs.json", {}).get("unit_econ") or {}
    arpu, vc = cfg.get("arpu"), cfg.get("vc_share")
    cac, churn = cfg.get("cac"), cfg.get("churn_month")
    vals = (arpu, vc, cac, churn)
    if not all(isinstance(v, (int, float)) for v in vals) or not arpu or not churn or not cac:
        return None

    def n(x: float) -> str:
        return f"{x:.2f}".replace(".", ",")

    cm = arpu * (1 - vc)
    ltv = cm / churn
    ratio = ltv / cac
    payback = cac / cm
    life = 1 / churn
    rows = [
        ("CM = ARPU × (1 − доля переменных)", f"{n(arpu)} × (1 − {n(vc)}) = {n(arpu)} × {n(1 - vc)}", f"**CM = {n(cm)}**"),
        ("Средняя жизнь платящего = 1 / churn", f"1 / {n(churn)}", f"**{n(life)} мес**"),
        ("LTV = CM / churn", f"{n(cm)} / {n(churn)}", f"**LTV = {n(ltv)}**"),
        ("LTV/CAC", f"{n(ltv)} / {n(cac)}", f"**{n(ratio)}** (критерий ≥ 3)"),
        ("Окупаемость CAC = CAC / CM", f"{n(cac)} / {n(cm)}", f"**{n(payback)} мес**"),
    ]
    table = "| Формула | Расчёт | Результат |\n|---|---|---|\n" + \
        "\n".join(f"| {f} | {c} | {r} |" for f, c, r in rows)
    return ("Допущения [укажите теги]: ARPU, переменные, CAC, churn — лист «Ввод» unit_economics.xlsx.\n\n"
            + table)


def _decision_block(pdir: Path) -> str | None:
    """Последнее зафиксированное решение D### — обязательство, срок, пересмотр."""
    rows = core.read_jsonl(pdir / "decisions.jsonl")
    if not rows:
        return None
    d = rows[-1]
    did = d.get("id", "D###")
    title = _flat(d.get("title"))
    commit = _flat(d.get("commitment"))
    rv = d.get("review")
    if isinstance(rv, dict):
        date = _flat(rv.get("date"))
        trig = _flat(rv.get("triggers") or rv.get("trigger"))
        review = f"промежуточный пересмотр {date}" + (f"; триггер: {trig}" if trig else "")
    else:
        review = _flat(rv)
    out = f"**Решение {did}** — {title}."
    if commit:
        out += f" Обязательство: {commit}."
    if review:
        out += f" {review[0].upper() + review[1:]}."
    return out


def build_six_pager(pdir: Path, with_calcs: bool = True) -> Path:
    """Six-pager в структуре референса стратегии роста: FAQ-1…FAQ-6 с нумерованными
    подпунктами (1.1/1.2 обзор рынка и конкуренты; 2.1/2.2 персоны и барьеры по этапам),
    инициативами-драйверами, матрицей тактик, планом с распределением вклада и KPI в двух
    плоскостях (бизнес/продукт). Сноски-источники — автоматически из sources.jsonl.
    Спецификация детализации: knowledge/templates/SIX_PAGER_PROMPT.md."""
    if with_calcs:
        calc.run(pdir, "all")
    meta = core.read_json(pdir / "project.json", {})
    parts = [f"# {meta.get('title')}: six-pager", "",
             f"> Собрано {core.now()[:16]} командой `pfs export --six-pager` по спецификации "
             "`knowledge/templates/SIX_PAGER_PROMPT.md` (формат референса стратегии роста: "
             "FAQ-1…6 с нумерованными подпунктами, матрицей тактик и KPI в двух плоскостях). "
             "Теги [C###]/[S###] — происхождение чисел; сноски-источники — в конце документа.", "",
             f"**Запрос:** {meta.get('question', '')}", ""]
    faq1 = _grab(pdir, "02_situation.md", ("Короткий ответ", "Что известно", "Рынок", "Тренды", "Противоречия", "Чего не знаем"))
    parts += ["## FAQ-1. Анализ текущего состояния", "",
              "### 1.1 Обзор рынка: тренды, вызовы и возможности", "",
              faq1 or "> Раздел появится после шага «situation» (02_situation.md): объём и динамика "
                      "рынка диапазонами, ключевые тренды буллетами с жирными заголовками.", "",
              "### 1.2 Ключевые конкуренты и анализ их стратегий роста и промо-механик", "",
              _grab(pdir, "02_situation.md", ("Конкуренты", "Конкурентный анализ"), 3000,
                    require_section=True)
              or "Сравнительная таблица групп конкурентов (заполните после конкурентного анализа):", "",
              "| | Группа 1 | Группа 2 | Группа 3 |",
              "|---|---|---|---|",
              "| **Ключевые преимущества** | … | … | … |",
              "| **Стратегия роста и промо-механики** | … | … | … |",
              "| **Риски для компании** | … — Высокий/Средний/Низкий | … | … |", "",
              "> **Вывод (умозаключение):** окно возможностей и его срок — заполните по данным 1.1–1.2.", ""]
    faq2 = _grab(pdir, "02_situation.md", ("Сегменты", "Персоны", "Аудитория"), 3000)
    if not faq2 or len(faq2) < 120:
        faq2 = _grab(pdir, "04_product_strategy.md", ("Аудитория",), 3000)
    parts += ["## FAQ-2. User Persona. Кто является целевой аудиторией?", "",
              "### 2.1 Сегменты", "",
              faq2 or "> Добавьте сегменты/персоны в 02_situation.md.", "",
              "Таблица персон (заполните):", "",
              "| | Сегмент 1 | Сегмент 2 | Сегмент 3 |",
              "|---|---|---|---|",
              "| **Кто они?** | … | … | … |",
              "| **Что используют сегодня и почему?** | … | … | … |",
              "| **С какими трудностями сталкиваются?** | … | … | … |",
              "| **Общие трудности** | … | … |", "",
              "### 2.2 Барьеры на каждом этапе пути", "",
              "| Этап пути | Барьер сегодня | Что делает продукт |",
              "|---|---|---|---|",
              "| Привлечение | … | … |",
              "| Выбор / использование | … | … |",
              "| Оплата | … | … |",
              "| Постоплатный опыт | … | … |", "",
              "Что сдерживает от старта или продления? (заполните по сегментам):", "",
              "| Сегмент | Сдерживающий фактор | Чем снимается |",
              "|---|---|---|",
              "| Сегмент 1 | … | … |", "",
              "> **Вывод (умозаключение):** сегментация по барьеру входа; лестница тиров "
              "обслуживает все барьеры; приоритизация — по ёмкости/CAC/конкуренции (расчёт — выше).", ""]
    faq3 = _grab(pdir, "03_options.md", (), 7000)
    parts += ["## FAQ-3. Стратегические инициативы. Кратко обоснуйте каждую.", "",
              faq3 or "> Раздел появится после шага «options» (03_options.md).", "",
              "### Инициативы выбранного направления (драйверы)", "",
              "Сформулируйте 3–4 инициативы по схеме: «**Первый драйвер** — …», «**Второй драйвер** — …», "
              "далее «Ключевые направления» (буллеты) и пошаговый расчёт эффекта. Закройте "
              "выводом-умозаключением.", ""]
    ue = _unit_econ_block(pdir)
    if ue:
        parts += ["Юнит-экономика — расчёт пошагово:", "", ue, "",
                  "**Вывод (умозаключение):** запас прочности модели — какой допуск выдерживает "
                  "каждое допущение (см. лист «Чувствительность»).", ""]
    faq4 = _grab(pdir, "04_product_strategy.md", ("Тактики", "Инициативы"), 4000) \
        or _grab(pdir, "03_options.md", ("Тактики",), 4000)
    parts += ["## FAQ-4. Тактики. Детализируйте каждую инициативу до конкретных тактик.", "",
              faq4 or "> Добавьте тактики по каждой инициативе в 04_product_strategy.md.", "",
              "Матрица тактик (заполните):", "",
              "| Стратегическая инициатива | Фокус | Потребности и ожидания пользователя | Решения (тактики) |",
              "|---|---|---|---|",
              "| Инициатива 1 | … | … | … |",
              "| Инициатива 2 | … | … | … |", ""]
    faq5 = _grab(pdir, "06_validation_plan.md", (), 5000)
    parts += ["## FAQ-5. Высокоуровневый план реализации", "",
              faq5 or "> Раздел появится после шага «validation» (06_validation_plan.md).", "",
              "Ожидаемое распределение вклада инициатив в общий результат (сумма 100%):", "",
              "- __% — Инициатива 1;",
              "- __% — Инициатива 2;",
              "- __% — Инициатива 3.", "",
              "Порядок тактик: высокий → средний → базовый приоритет. Тайминг — к сезонам рынка. "
              "Параллельные треки: комьюнити/партнёрства — вне основной линии.", ""]
    dec = _decision_block(pdir)
    if dec:
        parts += [dec, ""]
    faq6 = _grab(pdir, "04_product_strategy.md", ("Метрики", "Показатели"), 3000)
    if not faq6 or len(faq6) < 80:
        faq6 = _grab(pdir, "06_validation_plan.md", ("Ожидаемое изменение", "Критерии решения"), 3000)
    parts += ["## FAQ-6. Метрики успеха. KPI в двух плоскостях", "",
              faq6 or "> Добавьте метрики успеха в 04/06 документы.", "",
              "KPI в двух направлениях: **1) Бизнес** — деньги и база (выручка/MRR, платящие, "
              "конверсия в оплату, доля тарифов, фактический LTV/CAC); **2) Продукт** — активация, "
              "время до первой ценности, число действий до результата, churn, CSAT/NPS. "
              "У каждого KPI: база → цель к сроку → порог действия. Контр-метрики — по одной "
              "на удар red team.", ""]
    src = _sources_footnotes(pdir)
    if src:
        parts += ["## Источники (сноски)", "", src, ""]
    parts += ["## Приложения (Excel)", "", attachments_table(pdir) or "> Ещё нет: `pfs calc all`.", "",
              "", "> Формулы пересчитываются при открытии (Excel / Numbers / LibreOffice). "
                  "Детализация по спецификации — knowledge/templates/SIX_PAGER_PROMPT.md. "
                  "Полная версия с доказательствами — REPORT.md."]
    path = pdir / "outputs" / "SIX_PAGER.md"
    core.atomic_write(path, "\n".join(parts) + "\n")
    core.log(pdir, "action", "Собран outputs/SIX_PAGER.md (формат референса)", tool="pfs export --six-pager")
    return path


_MAX_POINTS = 6   # тезисов на слайд
_POINT_CAP = 160  # символов на тезис

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
