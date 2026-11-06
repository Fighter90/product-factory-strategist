"""Доп. тесты export: REPORT целиком, приложения, _grab, тезисы и экранирование слайдов.

Запуск: python3 -m unittest discover -s tests -v
"""
import os
import tempfile
import unittest
from pathlib import Path

TMP = tempfile.mkdtemp(prefix="pfs-test-xexp-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from tools.pfs import claims, decisions, export, project, sources  # noqa: E402


def fresh(slug):
    return project.create(f"Отчёт {slug}", "Почему падает удержание подписчиков?", slug=slug)


class ReportBuildTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pdir = fresh("xrep")
        pdir = cls.pdir
        sources.add(pdir, text="Публичный отчёт о рынке 40 млрд", title="Рынок")
        cls.claim = claims.add(pdir, "Рынок 40 млрд", "fact", ["S001"], grade="B")
        cls.dec = decisions.add(pdir, "Фокус на регионе", "Пилот в одном регионе", "CPO", [cls.claim["id"]],
                                metrics=["Удержание M1: 38% -> 45% @2027-03-01"],
                                review_date="2027-01-01", commitments=["Запустить пилот|PM|2027-02-01"])
        (pdir / "outputs" / "99_extra.md").write_text("# Дополнение\nЗаметки команды.\n", encoding="utf-8")
        cls.report = export.build(pdir)
        cls.text = cls.report.read_text(encoding="utf-8")

    def test_report_name_and_header(self):
        self.assertEqual(self.report, self.pdir / "outputs" / "REPORT.md")
        self.assertTrue(self.text.startswith("# Отчёт xrep: стратегия и обоснование"))
        self.assertIn("Почему падает удержание подписчиков?", self.text)  # бриф вошёл в отчёт

    def test_report_applications(self):
        self.assertIn("# Приложение A. Реестр утверждений", self.text)
        self.assertIn(self.claim["id"], self.text)
        self.assertIn("# Приложение B. Источники", self.text)
        self.assertIn("| S001 | Рынок | — | public |", self.text)
        self.assertIn("# Приложение C. Решения и обязательства", self.text)
        self.assertIn(self.dec["id"], self.text)
        self.assertIn("38%→45% к 2027-03-01", self.text)  # показатели решения в таблице
        self.assertIn("# Приложение D. Прозрачность", self.text)
        self.assertIn("## Дополнение", self.text)         # не-ORDER документ попал после основных
        self.assertIn("Заметки команды", self.text)
        self.assertNotIn("Приложение E", self.text)       # Excel ещё не собраны — приложения нет

    def test_attachments_appendix_e(self):
        self.assertIsNone(export.attachments_table(self.pdir))
        att = self.pdir / "outputs" / "attachments"
        att.mkdir(parents=True, exist_ok=True)
        (att / "unit_economics.xlsx").write_bytes(b"PK\x03\x04 dummy")
        table = export.attachments_table(self.pdir)
        self.assertIn("| Файл | Листы | Что редактировать |", table)
        self.assertIn("unit_economics.xlsx", table)
        self.assertNotIn("growth_model.xlsx", table)
        text = export.build(self.pdir).read_text(encoding="utf-8")
        self.assertIn("# Приложение E. Excel-расчёты", text)


class GrabAndDeckHelpersTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pdir = fresh("xgrab")
        (cls.pdir / "outputs" / "02_situation.md").write_text(
            "# Ситуация\n## Короткий ответ\nОтток растёт третий месяц подряд.\n"
            "## Что известно\n- рынок 40 млрд\n", encoding="utf-8")

    def test_grab_extracts_named_sections_only(self):
        body = export._grab(self.pdir, "02_situation.md", ("Короткий ответ",))
        self.assertTrue(body.startswith("### Короткий ответ"))
        self.assertIn("Отток растёт третий месяц подряд", body)
        self.assertNotIn("рынок 40 млрд", body)  # соседняя секция не затянута

    def test_grab_without_sections_returns_whole_doc(self):
        body = export._grab(self.pdir, "02_situation.md", ("Нет такого раздела",))
        self.assertIn("## Короткий ответ", body)
        self.assertIn("- рынок 40 млрд", body)
        self.assertIsNone(export._grab(self.pdir, "нет_файла.md", ()))

    def test_grab_truncates_long_body(self):
        long_doc = "# Длинный\n" + "очень длинный абзац про удержание и драйверы " * 20
        (self.pdir / "outputs" / "08_long.md").write_text(long_doc, encoding="utf-8")
        body = export._grab(self.pdir, "08_long.md", (), cap=60)
        self.assertTrue(body.endswith("обрезано, полностью — `08_long.md`"))
        self.assertLessEqual(len(body), 60 + len("\n\n… обрезано, полностью — `08_long.md`"))

    def test_points_rules_and_slide_escaping(self):
        pts = export._points("- один\n> два\n| три | четыре |\n\nПервое предложение. Второе предложение.")
        self.assertEqual(pts, ["один", "два", "три", "Первое предложение."])  # списки, цитаты, 1-й столбец таблицы
        self.assertEqual(export._points("повтор\nповтор"), ["повтор"])         # дубль подряд схлопывается
        self.assertEqual(len(export._points("\n".join(f"- п{i}" for i in range(9)))), 6)  # максимум 6
        long = export._points("ж" * 300)[0]
        self.assertEqual(len(long), 160)
        self.assertTrue(long.endswith("…"))
        slide = export._slide("Титул", ["<b>жир</b>"])
        self.assertIn("<h2>Титул</h2>", slide)
        self.assertIn("&lt;b&gt;жир&lt;/b&gt;", slide)  # HTML в тезисах экранируется
        self.assertNotIn("<li><b>", slide)
        self.assertNotIn("<ul>", export._slide("Пусто", []))


if __name__ == "__main__":
    unittest.main()
