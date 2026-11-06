"""Доп. тесты базы знаний: BM25-поиск RU/EN, INDEX.md, карты по шагам.

Запуск: python3 -m unittest discover -s tests -v
"""
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

TMP = tempfile.mkdtemp(prefix="pfs-test-xkb-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from tools.pfs import core, kb, project, sources  # noqa: E402
from tools.pfs.core import PfsError  # noqa: E402


class KbTokenTests(unittest.TestCase):
    def test_stem_and_tokens(self):
        self.assertEqual(kb.stem("Ёжик"), "ежик")           # ё → е
        self.assertEqual(kb.stem("УДЕРЖАНИЕ"), "удержа")    # нижний регистр + грубый стемминг до 6
        self.assertEqual(kb.stem("клиентов"), "клиент")
        self.assertEqual(kb.stem("код"), "код")             # короткие слова не режутся
        toks = kb.tokens("Ёжик, и УДЕРЖАНИЕ клиентов: 5 раз!")
        self.assertEqual(toks, ["ежик", "удержа", "клиент"])  # стоп-слова и одиночные символы выброшены
        self.assertEqual(kb.tokens("the of and to"), [])      # английские стоп-слова тоже

    def test_frontmatter_parses_scalars_and_lists(self):
        fm = kb.frontmatter('---\nid: M-x\ntitle: "Кавычки тут"\nstages: [intake, research]\ncourse: strategy\n---\nТело')
        self.assertEqual(fm["id"], "M-x")
        self.assertEqual(fm["title"], "Кавычки тут")
        self.assertEqual(fm["stages"], ["intake", "research"])
        self.assertEqual(fm["course"], "strategy")
        self.assertEqual(kb.frontmatter("Без фронтматтера"), {})
        real = kb.frontmatter((core.KNOWLEDGE / "methods" / "ab-testing.md").read_text(encoding="utf-8"))
        self.assertEqual(real["id"], "M-ab-testing")
        self.assertIn("options", real["stages"])


class KbSearchTests(unittest.TestCase):
    def test_search_ru_and_en_rank_unit_economics(self):
        for query in ("юнит экономика LTV CAC", "unit economics LTV CAC"):
            res = kb.search(query)
            self.assertTrue(res)
            for r in res:  # структура результата единая
                self.assertGreater(r["score"], 0)
                self.assertTrue(r["path"])
                self.assertTrue(r["id"])
                self.assertTrue(r["snippet"])
            self.assertIn("M-unit-economics", [r["id"] for r in res[:3]], query)

    def test_search_project_scope_finds_outputs(self):
        pdir = project.create("КБ скоуп", "Почему падает удержание?", slug="xkbscope")
        (pdir / "outputs" / "99_extra.md").write_text(
            "## Экзотермин\n\nКсилотрон-прок проявляется в падении удержания.\n", encoding="utf-8")
        res = kb.search("ксилотрон прок", project=pdir)
        self.assertTrue(any(r["section"] == "Экзотермин" and r["path"].endswith("99_extra.md")
                            and "Ксилотрон" in r["snippet"] for r in res))
        self.assertEqual(kb.search("зззззз qwzzzz"), [])  # мусорный запрос — пусто


class KbIndexTests(unittest.TestCase):
    def test_build_index_reports_broken_links_and_writes_file(self):
        root = Path(tempfile.mkdtemp(prefix="pfs-test-xkb-knowledge-"))
        (root / "methods").mkdir()
        (root / "methods" / "m1.md").write_text(
            "---\nid: M-x-one\ntitle: Карта один\nstages: [intake, research]\n"
            "tags: [тег-раз, тег-два]\nrelated: [M-x-two]\ncourse: strategy\n---\n# Один\n", encoding="utf-8")
        (root / "methods" / "m2.md").write_text(
            "---\nid: M-x-two\ntitle: Карта два\nstages: [research]\nrelated: [M-x-missing]\n---\n# Два\n", encoding="utf-8")
        (root / "methods" / "m3.md").write_text("---\ntitle: Без id\n---\n# Три\n", encoding="utf-8")
        with mock.patch.object(core, "KNOWLEDGE", root):
            text, problems = kb.build_index()
        self.assertEqual(problems, ["M-x-two → M-x-missing: карты нет", "m3.md: нет id во frontmatter"])
        written = (root / "INDEX.md").read_text(encoding="utf-8")
        self.assertEqual(text, written)  # возвращённый текст совпадает с записанным файлом
        self.assertIn("# Навигация по методическим картам", written)
        self.assertIn("## Постановка задачи (`intake`)", written)
        self.assertIn("[Карта один](methods/m1.md) `M-x-one` — тег-раз, тег-два", written)
        self.assertIn("## Исследование (`research`)", written)
        self.assertIn("[Карта два](methods/m2.md)", written)
        self.assertIn("## Все карты по курсам", written)
        self.assertIn("**strategy**: [M-x-one](methods/m1.md)", written)
        self.assertIn("## Битые связи", written)
        self.assertIn("- M-x-two → M-x-missing: карты нет", written)
        self.assertIn("- m3.md: нет id во frontmatter", written)

    def test_card_path_found_and_missing(self):
        p = kb.card_path("M-jtbd")
        self.assertTrue(p.exists())
        self.assertEqual(p.parent.name, "methods")
        self.assertIn("id: M-jtbd", p.read_text(encoding="utf-8"))
        with self.assertRaises(PfsError):
            kb.card_path("M-totally-absent")

    def test_cards_for_stage(self):
        self.assertEqual(kb.cards_for("intake"), kb.STAGE_CARDS["intake"])
        self.assertIn("M-jtbd", kb.cards_for("intake"))
        self.assertEqual(kb.cards_for("не-шаг"), [])
        for stage in core.STAGE_IDS:  # у каждого шага процесса описаны карты
            self.assertTrue(kb.cards_for(stage), stage)


if __name__ == "__main__":
    unittest.main()
