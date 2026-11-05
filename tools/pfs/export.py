"""Сборка итогового отчёта: документы + реестр утверждений + источники + решения + стоимость."""
from __future__ import annotations

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
