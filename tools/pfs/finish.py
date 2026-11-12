"""pfs finish — командная цепочка до финального пакета (PRO-31).

Проблема: пакет собирали вручную шестью разрозненными вызовами, и порядок легко
нарушить — REPORT экспортировали ДО Excel, Приложение E оставалось пустым, а
реестр утверждений в отчёте обрезался до свежих правок. Одна команда фиксирует
порядок: автопроверка check → calc all → REPORT → SIX_PAGER → снимок реестра →
DOCX → deck (→ EN-черновик six-pager) → сводка «что собрано + что устарело».
Повторный вызов идемпотентен: те же файлы пересобираются из текущего реестра.
"""
from __future__ import annotations

from pathlib import Path

from . import calc, check, core, docx, export, i18n


def run(pdir: Path, no_deck: bool = False, en: bool = False) -> dict:
    """Собрать финальный пакет в правильном порядке.

    Затвор строгий: перед сборкой выполняется pfs check, и ЛЮБАЯ его ошибка
    останавливает сборку (эквивалент `pfs check --strict`, где --strict — это
    «ошибки → ненулевой код выхода»; отдельного флага strict у check.run нет,
    предупреждения сборке не мешают). Пакет из невалидного реестра не собираем.
    Возвращает {check, artifacts, missing_docs, stale_warnings} — stale_warnings
    это предупреждения о несвежих основаниях ДО пересборки (свежая сборка их снимает).
    """
    stale = export.freshness_warnings(pdir)  # предупреждение о несвежих основаниях — до сборки
    qc = check.run(pdir)
    if qc["errors"]:  # строгий затвор: любая ошибка check останавливает сборку (см. докстрингу)
        tr = lambda key, **kw: i18n.t(i18n.lang_of(pdir), key, **kw)
        raise core.PfsError(tr("finish_gate_error",
                               errs="\n- ".join(qc["errors"])))
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


def summary_text(res: dict, lang: str = "ru") -> str:
    """Сводка «что собрано + что устарело»: артефакты, недостающие документы, несвежие основания.
    Язык — параметр (по умолчанию ru; PRO-57: сводка pfs finish — по языку проекта)."""
    tr = lambda key, **kw: i18n.t(lang, key, **kw)
    lines = [tr("finish_built", n=len(res["artifacts"]))
             + "".join(f"\n- {p}" for p in res["artifacts"])]
    if res["missing_docs"]:
        lines.append(tr("finish_missing_docs") + ", ".join(res["missing_docs"]))
    else:
        lines.append(tr("finish_all_docs"))
    if res["stale_warnings"]:
        lines.append(tr("finish_stale") + " ".join(res["stale_warnings"]))
    return "\n".join(lines)
