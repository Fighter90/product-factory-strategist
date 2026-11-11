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

from . import calc, check, core, docx, export


def run(pdir: Path, no_deck: bool = False, en: bool = False) -> dict:
    """Собрать финальный пакет в правильном порядке.

    Затвор строгий: перед сборкой выполняется pfs check, и ЛЮБАЯ его ошибка
    останавливает сборку (эквивалент `pfs check --strict`, где --strict — это
    «ошибки → ненулевой код выхода»; отдельного флага strict у check.run нет,
    предупреждения сборке не мешают). Пакет из невалидного реестра не собираем.
    Возвращает {check, artifacts, missing_docs, stale_warnings, stale_facts} —
    stale_facts это факты «что в реестре изменилось ДО пересборки» (свежая сборка их
    снимает), stale_warnings — те же факты в виде предупреждения с советом «пересоберите».
    """
    stale_facts = export.freshness_facts(pdir)  # предупреждение о несвежих основаниях — до сборки
    stale = export.freshness_warnings(pdir)
    qc = check.run(pdir)
    if qc["errors"]:  # строгий затвор: любая ошибка check останавливает сборку (см. докстрингу)
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
    return {"check": qc, "artifacts": artifacts, "missing_docs": missing,
            "stale_warnings": stale, "stale_facts": stale_facts}


def summary_text(res: dict) -> str:
    """Сводка «что собрано + что устарело»: артефакты, недостающие документы, несвежие основания.
    Только факты: пересборка уже случилась — совет «пересоберите» здесь противоречил бы строке
    «снято свежей пересборкой» (PRO-63)."""
    lines = ["Собрано ({}):".format(len(res["artifacts"]))
             + "".join(f"\n- {p}" for p in res["artifacts"])]
    if res["missing_docs"]:
        lines.append("Нет документов (заглушки в six-pager/REPORT): "
                     + ", ".join(res["missing_docs"]))
    else:
        lines.append("Документы 00–07: все на месте")
    facts = res.get("stale_facts")
    if facts is None:  # совместимость: словарь без stale_facts — вычислить по фактам предупреждений
        facts = [w.split(": ", 1)[1].split(" — приложения", 1)[0] for w in res["stale_warnings"]]
    if facts:
        lines.append("До сборки реестр менялся — снято свежей пересборкой: "
                     + ", ".join(facts))
    return "\n".join(lines)
