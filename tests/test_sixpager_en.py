"""PRO-29/PRO-53: pfs export --six-pager --en — EN-версия six-pager.

Контракт после PRO-53 («EN-версия пишется, а не переводится»):
1. одним вызовом CLI собирается SIX_PAGER_EN.md — каркас на английском;
2. секции из документов 00–07 НЕ вставляются (RU-текст — вход писателя): каркас
   содержит pending-строки «> EN draft — pending: …» и остаётся чистым по линтеру;
3. check предупреждает, если дописанный EN-документ отстал от RU по источникам
   сносок S### и маркерам [^n] (PRO-49; сырые теги C### в EN не ждутся —
   реестр тегов в REPORT.md); каркас-черновик — не «отстал».

Запуск: python3 -m unittest tests.test_sixpager_en -v
"""
import os
import tempfile
import unittest

TMP = tempfile.mkdtemp(prefix="pfs-test-spen-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from pathlib import Path  # noqa: E402

from tools.pfs import check, claims, cli, core, export, project, sources  # noqa: E402

MARK = core.RU_SOURCE_MARK  # запрещённый артефакт старого каркаса-на-перевод
DRAFT = core.EN_DRAFT_MARK


def make_docs(pdir: Path) -> None:
    out = pdir / "outputs"
    (out / "02_situation.md").write_text(
        "# 02 · Ситуация\n\n## Короткий ответ\n\nРынок 40 млрд [C001].\n\n"
        "## Что известно\n\n- Рынок 40 млрд [C001].\n\n"
        "## Сегменты\n\n- соискатели 55+: страх мошеннических звонков\n\n"
        "## Конкуренты\n\n- оператор X: семейные тарифы\n",
        encoding="utf-8")
    (out / "03_options.md").write_text(
        "# 03 · Варианты\n\n## Рекомендация\n\nВариант B: семейный пакет [C001].\n\n"
        "## Вариант A: оставить как есть\n\n### Возражения\n\n- отток продолжится\n\n"
        "## Вариант B: семейный пакет\n\n## Вариант C: закрыть направление\n",
        encoding="utf-8")
    (out / "04_product_strategy.md").write_text(
        "# 04 · Стратегия\n\n## Аудитория\n\nсоискатели 55+ [C001].\n\n"
        "## Тактики\n\n- семейный пакет с уведомлениями\n",
        encoding="utf-8")
    (out / "06_validation_plan.md").write_text(
        "# 06 · План проверки\n\n## Ожидаемое изменение\n\nудержание M1 с 38% до 45% [C001].\n\n"
        "## Критерии решения\n\nпродолжаем, если +3 п.п.\n",
        encoding="utf-8")


def build_pair(pdir: Path) -> tuple[Path, Path]:
    ru = export.build_six_pager(pdir, with_calcs=False)
    en = export.build_six_pager(pdir, with_calcs=False, lang="en")
    return ru, en


class SixPagerEnTests(unittest.TestCase):
    def setUp(self):
        slug = "spen-" + self.id().rsplit(".", 1)[-1][:40]
        self.pdir = project.create("EN каркас", "Почему падает удержание?", slug=slug)
        sources.add(self.pdir, text="Публичный отчёт: рынок 40 млрд", title="Рынок")
        claims.add(self.pdir, "Рынок 40 млрд", "fact", ["S001"], grade="B")
        make_docs(self.pdir)

    def test_export_cli_en_flag_builds_en_in_one_call(self):
        rc = cli.main(["--project", self.pdir.name, "export", "--six-pager", "--en", "--no-calcs"])
        self.assertEqual(rc, 0)
        ru = self.pdir / "outputs" / "SIX_PAGER.md"
        en = self.pdir / "outputs" / "SIX_PAGER_EN.md"
        self.assertTrue(en.exists(), "один вызов собрал EN-версию")
        self.assertTrue(ru.exists(), "RU-версия не потерялась")
        entext = en.read_text(encoding="utf-8")
        self.assertIn("# Six-pager (EN)", entext)
        self.assertIn(DRAFT, entext, "каркас помечен pending-строками для writer'а")
        self.assertIn("## FAQ-1. Current state analysis", entext)
        self.assertIn("## Appendices (Excel)", entext)

    def test_en_skeleton_carries_package_pointers(self):
        """EN-каркас не вставляет RU-контент, но показывает writer'у вход — пакет данных;
        RU-каркас — слоты для six-pager-writer, тоже без вставки документов (PRO-46)."""
        ru, en = build_pair(self.pdir)
        rutext, entext = ru.read_text(encoding="utf-8"), en.read_text(encoding="utf-8")
        self.assertNotIn("Рынок 40 млрд", entext, "RU-контент не вставляется в EN")
        self.assertNotIn(MARK, entext, "маркер перевода не вставляется")
        self.assertIn("six_pager_pack.md", entext, "вход writer'а — пакет данных")
        self.assertIn("SIX_PAGER_PROMPT_EN.md", entext)
        self.assertNotIn("Рынок 40 млрд", rutext, "PRO-46: RU-каркас не вставляет документы")
        self.assertIn(export.SLOT_MARK, rutext, "RU-каркас — слоты для six-pager-writer")
        self.assertEqual(rutext.count(MARK), 0, "RU-версия без маркеров перевода")

    def test_en_skeleton_is_linter_clean_with_docs(self):
        _, en = build_pair(self.pdir)
        warns = [w for w in check.run(self.pdir)["warnings"] if "SIX_PAGER_EN.md" in w]
        self.assertEqual(warns, [], "собранный каркас чист: кириллицы/запятых/маркеров нет")
        self.assertIn(DRAFT, en.read_text(encoding="utf-8"))

    def test_en_without_docs_has_pending_lines(self):
        pdir2 = project.create("EN пустой", "Что делать?", slug=slug_unique())
        _, en = build_pair(pdir2)
        entext = en.read_text(encoding="utf-8")
        self.assertIn(DRAFT, entext, "pending-строки есть и без документов")
        self.assertIn("## FAQ-1. Current state analysis", entext)


def slug_unique() -> str:
    import uuid
    return "spen-empty-" + uuid.uuid4().hex[:8]


class CheckEnSyncTests(unittest.TestCase):
    def setUp(self):
        slug = "spen-sync-" + self.id().rsplit(".", 1)[-1][:40]
        self.pdir = project.create("EN сверка", "Почему падает удержание?", slug=slug)
        sources.add(self.pdir, text="Публичный отчёт: рынок 40 млрд", title="Рынок")
        claims.add(self.pdir, "Рынок 40 млрд", "fact", ["S001"], grade="B")
        make_docs(self.pdir)
        build_pair(self.pdir)

    def _warnings(self) -> list[str]:
        return [w for w in check.run(self.pdir)["warnings"] if "SIX_PAGER_EN" in w]

    def test_skeleton_draft_not_flagged(self):
        # каркас-черновик (pending-строки) — не «отставшая» версия: его допишет writer
        self.assertEqual(self._warnings(), [])

    def test_written_en_lags_ru_after_new_source_added(self):
        # writer дописал EN в формате PRO-49: сноски [^n] с источниками S###, сырых
        # тегов C### нет (реестр — REPORT.md) — сверка активна, «отставания» нет
        en_path = self.pdir / "outputs" / "SIX_PAGER_EN.md"
        en_path.write_text("# Six-pager (EN)\n\nThe market is large[^1].\n\n"
                           "## Sources (footnotes)\n\n"
                           "[^1]: S001 — Example — Market report — https://example.org/r — grade B\n",
                           encoding="utf-8")
        self.assertEqual(self._warnings(), [])
        # в RU добавили источник (драйвер C002 на S002), EN не переписан — check предупреждает.
        # PRO-46: тег в каркас попадает через расчётный артефакт — явную KPI-таблицу 06.
        sources.add(self.pdir, text="Публичный отчёт: удержание 92% при семейном пакете",
                    title="Удержание", url="https://example.org/churn")
        claims.add(self.pdir, "Драйвер: семейный пакет даёт +5 п.п. удержания",
                   "hypothesis", ["S002"], grade="C")
        out = self.pdir / "outputs" / "06_validation_plan.md"
        out.write_text(out.read_text(encoding="utf-8")
                       + "\n## KPI\n\n"
                         "| Плоскость | Метрика | Формула | База (дата, источник) | Цель к сроку | "
                         "Порог действия (остановить) | Контр-метрика |\n"
                         "|---|---|---|---|---|---|---|\n"
                         "| Продукт | Удержание M1 | доля активных на 30-й день | 38% (2026-11-01, [C002]) "
                         "| 45% к 90 дн | ниже 41% → гейт 30 дней | активация |\n", encoding="utf-8")
        export.build_six_pager(self.pdir, with_calcs=False)  # пересобрали только RU
        warns = self._warnings()
        self.assertTrue(warns, "check предупреждает, что дописанный EN отстал от RU")
        self.assertIn("S002", warns[0], "сигнал свёрки — источник S###")
        self.assertNotIn("C002", warns[0], "теги C### — не сигнал свёрки: реестр в REPORT.md")
        self.assertIn("SIX_PAGER_PROMPT_EN.md", warns[0], "подсказка — EN-спецификация")
        # пересборка EN даёт каркас-черновик — предупреждение снято (EN переделывают)
        export.build_six_pager(self.pdir, with_calcs=False, lang="en")
        self.assertEqual(self._warnings(), [])

    def test_no_warning_when_en_absent(self):
        (self.pdir / "outputs" / "SIX_PAGER_EN.md").unlink()
        self.assertEqual(self._warnings(), [])


if __name__ == "__main__":
    unittest.main()
