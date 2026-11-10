"""PRO-29: pfs export --six-pager --en — каркас EN-версии six-pager.

Три требования выпуска:
1. одним вызовом CLI собирается SIX_PAGER_EN.md (скелет на английском, числа/теги — как в RU);
2. секции, взятые из документов 00–07 дословно, помечены «[RU source — translate]»;
3. check предупреждает, если EN-каркас отстал от RU (драйверы/теги добавлены в RU после сборки EN).

Запуск: python3 -m unittest tests.test_sixpager_en -v
"""
import os
import tempfile
import unittest

TMP = tempfile.mkdtemp(prefix="pfs-test-spen-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from pathlib import Path  # noqa: E402

from tools.pfs import check, claims, cli, export, project, sources  # noqa: E402

MARK = "[RU source — translate]"


def section_markers(text: str) -> list[str]:
    """Строки-маркеры секций («> [RU source — translate] 02_situation.md»); упоминание
    маркера в шапке-скелете не считается."""
    return [ln for ln in text.splitlines() if ln.startswith(f"> {MARK} ")]


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
        self.assertTrue(en.exists(), "один вызов собрал EN-каркас")
        self.assertTrue(ru.exists(), "RU-версия не потерялась")
        entext = en.read_text(encoding="utf-8")
        self.assertIn("Six-pager (EN draft)", entext)
        self.assertIn("## FAQ-1. Current state analysis", entext)
        self.assertIn("## Appendices (Excel)", entext)

    def test_en_tags_and_numbers_match_ru(self):
        ru, en = build_pair(self.pdir)
        rutext, entext = ru.read_text(encoding="utf-8"), en.read_text(encoding="utf-8")
        # теги: множества совпадают (EN собирается из того же реестра и тех же документов)
        from tools.pfs.impact import TAG
        self.assertEqual(sorted(set(TAG.findall(rutext))), sorted(set(TAG.findall(entext))))
        self.assertIn("C001", entext)
        # числа: контент документов вставлен дословно — числа совпадают с RU
        self.assertIn("Рынок 40 млрд [C001]", entext)
        self.assertIn("с 38% до 45%", entext)

    def test_en_marks_document_sections_with_translate_marker(self):
        _, en = build_pair(self.pdir)
        entext = en.read_text(encoding="utf-8")
        # каждая секция из документов помечена; рядом — имя файла-источника
        marks = "\n".join(section_markers(entext))
        self.assertIn(f"{MARK} 02_situation.md", marks)
        self.assertIn(f"{MARK} 03_options.md", marks)
        self.assertIn(f"{MARK} 04_product_strategy.md", marks)
        self.assertIn(f"{MARK} 06_validation_plan.md", marks)
        # маркер стоит выше вставленного контента
        marker_pos = entext.index(f"> {MARK}")
        content_pos = entext.index("Рынок 40 млрд [C001]")
        self.assertLess(marker_pos, content_pos)
        # RU-версия без маркеров перевода
        ru = export.build_six_pager(self.pdir, with_calcs=False).read_text(encoding="utf-8")
        self.assertEqual(section_markers(ru), [])

    def test_en_without_docs_has_no_markers(self):
        pdir2 = project.create("EN пустой", "Что делать?", slug=slug_unique())
        _, en = build_pair(pdir2)
        entext = en.read_text(encoding="utf-8")
        self.assertEqual(section_markers(entext), [], "заглушки-скелет без маркеров")
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

    def test_in_sync_no_warning(self):
        self.assertEqual(self._warnings(), [])

    def test_en_lags_ru_after_driver_added(self):
        # драйвер добавлен в RU после сборки EN — check предупреждает
        claims.add(self.pdir, "Драйвер: семейный пакет даёт +5 п.п. удержания", "hypothesis", ["S001"], grade="C")
        out = self.pdir / "outputs" / "03_options.md"
        out.write_text(out.read_text(encoding="utf-8")
                       + "\n## Драйверы выбранного направления\n\n"
                         "- **Первый драйвер:** семейный пакет [C002]\n", encoding="utf-8")
        export.build_six_pager(self.pdir, with_calcs=False)  # пересобрали только RU
        warns = self._warnings()
        self.assertTrue(warns, "check предупреждает, что EN отстал от RU")
        self.assertIn("C002", warns[0])
        self.assertIn("pfs export --six-pager --en", warns[0])
        # пересборка EN снимает предупреждение
        export.build_six_pager(self.pdir, with_calcs=False, lang="en")
        self.assertEqual(self._warnings(), [])

    def test_no_warning_when_en_absent(self):
        (self.pdir / "outputs" / "SIX_PAGER_EN.md").unlink()
        self.assertEqual(self._warnings(), [])


if __name__ == "__main__":
    unittest.main()
