"""pfs finish — командная цепочка до финального пакета (PRO-31).

Проблема: пакет собирали вручную шестью разрозненными вызовами, и порядок легко
нарушить — REPORT экспортировали ДО Excel, Приложение E оставалось пустым, а
реестр утверждений в отчёте обрезался до свежих правок. Одна команда фиксирует
порядок: check --strict → calc all → REPORT → SIX_PAGER → снимок реестра →
DOCX → deck (→ EN-черновик six-pager) → сводка «что собрано + что устарело».
Повторный вызов идемпотентен: те же файлы пересобираются из текущего реестра.
"""
from __future__ import annotations

from pathlib import Path

from . import calc, check, core, docx, export


def run(pdir: Path, no_deck: bool = False, en: bool = False) -> dict:
    """Собрать финальный пакет в правильном порядке.

    Ошибки автопроверки (pfs check --strict) останавливают сборку: пакет из
    невалидного реестра не собираем. Возвращает {check, artifacts, missing_docs,
    stale_warnings} — stale_warnings это предупреждения о несвежих основаниях
    ДО пересборки (свежая сборка их снимает).
    """
    stale = export.freshness_warnings(pdir)  # предупреждение о несвежих основаниях — до сборки
    qc = check.run(pdir)
    if qc["errors"]:  # авто pfs check --strict: с ошибками в реестре пакет не собираем
        raise core.PfsError("pfs finish: автопроверка нашла ошибки — пакет не собран:\n- "
                            + "\n- ".join(qc["errors"])
                            + "\nИсправьте (pfs check) и повторите: pfs finish")
    artifacts: list[Path] = list(calc.run(pdir, "all"))            # 1. Excel — до REPORT
    artifacts.append(export.build(pdir))                           # 2. REPORT: Приложение E уже полно
    artifacts.append(export.build_six_pager(pdir, with_calcs=False))  # 3. SIX_PAGER
    export.save_state(pdir)  # 4. снимок реестра ПОСЛЕ сборки — свежесть считается от неё
    for name in ("REPORT.md", "SIX_PAGER.md"):
        artifacts.append(docx.convert(pdir / "outputs" / name))
    if en:  # 5. EN-черновик six-pager (скелет на английском, содержимое — как написано)
        en_path = export.build_six_pager(pdir, with_calcs=False, lang="en")
        artifacts += [en_path, docx.convert(en_path)]
    if not no_deck:  # 6. дека из готового SIX_PAGER
        artifacts.append(export.build_deck(pdir))
    missing = [name for name in export.ORDER if not (pdir / "outputs" / name).exists()]
    core.log(pdir, "action", "Собран финальный пакет: " + ", ".join(p.name for p in artifacts),
             tool="pfs finish")
    return {"check": qc, "artifacts": artifacts, "missing_docs": missing, "stale_warnings": stale}


def summary_text(res: dict, pdir: Path) -> str:
    """Сводка «что собрано + что устарело»: артефакты, недостающие документы, несвежие основания."""
    lines = ["Собрано ({}):".format(len(res["artifacts"]))
             + "\n".join(f"\n- {p}" for p in res["artifacts"])]
    if res["missing_docs"]:
        lines.append("Нет документов (заглушки в six-pager/REPORT): "
                     + ", ".join(res["missing_docs"]))
    else:
        lines.append("Документы 00–07: все на месте")
    if res["stale_warnings"]:
        lines.append("До сборки реестр менялся — снято свежей пересборкой: "
                     + " ".join(res["stale_warnings"]))
    return "\n".join(lines)
