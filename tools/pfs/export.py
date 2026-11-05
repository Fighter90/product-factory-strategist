"""Сборка итогового отчёта: документы + реестр утверждений + источники + решения + стоимость."""
from __future__ import annotations

from pathlib import Path

from . import check, claims as claims_mod, core, cost, decisions, sources as src_mod

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
    path = outs / "REPORT.md"
    core.atomic_write(path, "\n".join(parts) + "\n")
    core.log(pdir, "action", "Собран outputs/REPORT.md", tool="pfs export")
    return path
