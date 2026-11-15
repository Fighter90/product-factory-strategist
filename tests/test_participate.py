"""Тесты модуля participate: гайды интервью, синтетика, медиа, UX-каркас.

Запуск: python3 -m unittest discover -s tests -v
"""
import json
import os
import tempfile
import unittest
from pathlib import Path

TMP = tempfile.mkdtemp(prefix="pfs-test-part-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from tools.pfs import core, participate, project, sources  # noqa: E402


def fresh(slug):
    return project.create(f"Тест участие {slug}", "Почему падает удержание подписчиков?", slug=slug)


class GuideTests(unittest.TestCase):
    def test_guide_created_and_idempotent(self):
        pdir = fresh(f"g1{id(self)}")
        path = participate.guide(pdir, "Мама двоих детей", "онлайн-покупки детской одежды")
        self.assertTrue(path.exists())
        self.assertEqual(path.parent, pdir / "interviews" / "synthetic")
        self.assertIn("guide_", path.name)
        text = path.read_text(encoding="utf-8")
        self.assertIn("Мама двоих детей", text)
        self.assertIn("онлайн-покупки детской одежды", text)
        self.assertIn(core.today(), text)
        # разделы — каркас из шаблона, шаблон не тронут
        self.assertIn("Последний случай", text)
        self.assertIn("Что ищем", text)
        self.assertIn("заполните агентом", text)
        # повтор: тот же файл, содержимое не перезаписывается
        text_after = text + "\n<!-- правка агента -->"
        path.write_text(text_after, encoding="utf-8")
        again = participate.guide(pdir, "Мама двоих детей", "онлайн-покупки детской одежды")
        self.assertEqual(again, path)
        self.assertIn("правка агента", path.read_text(encoding="utf-8"))
        # пользовательская правка гайда не потеряна — файл не дублируется
        self.assertEqual(len(list((pdir / "interviews" / "synthetic").glob("guide_*.md")), ), 1)


class SyntheticTests(unittest.TestCase):
    def test_save_synthetic_origin_and_warning(self):
        pdir = fresh(f"syn{id(self)}")
        src = Path(pdir) / "interviews" / "synthetic" / "transcript.md"
        src.parent.mkdir(parents=True, exist_ok=True)
        src.write_text("Респондент R1: покупаю одежду детям раз в месяц, раздражает доставка.", encoding="utf-8")
        rec = participate.save_synthetic(pdir, src, "Мама двоих детей")
        self.assertEqual(rec["origin"], "synthetic")
        md = (pdir / "sources" / f"{rec['id']}.md").read_text(encoding="utf-8")
        self.assertIn("СИНТЕТИЧЕСКИЙ", md)
        self.assertIn("не доказывает спрос", md)
        # в логе — персона без содержимого транскрипта
        log_text = (pdir / "log.jsonl").read_text(encoding="utf-8")
        self.assertIn("Мама двоих детей", log_text)
        self.assertNotIn("раздражает доставка", log_text)
        # повтор с тем же содержимым — дедуп источника
        rec2 = participate.save_synthetic(pdir, src, "Мама двоих детей")
        self.assertEqual(rec2["id"], rec["id"])


class MediaTests(unittest.TestCase):
    def setUp(self):
        self.pdir = fresh(f"md{id(self)}")
        self.img = Path(TMP) / f"screen_{id(self)}.png"
        self.img.write_bytes(b"\x89PNG\r\n\x1a\n fake-bytes")

    def test_media_raw_file_and_single_record(self):
        rec = participate.media(self.pdir, self.img, "На скриншоте воронка: 40% уходят на шаге доставки")
        raw = self.pdir / "sources" / "raw" / self.img.name
        self.assertTrue(raw.exists())
        rows = core.read_jsonl(self.pdir / "sources.jsonl")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["kind"], "media")
        self.assertEqual(rows[0]["path"], f"sources/raw/{self.img.name}")
        self.assertEqual(rows[0]["origin"], "own")
        self.assertEqual(rows[0]["title"], self.img.name)  # спека: title = имя файла
        md = (self.pdir / "sources" / f"{rec['id']}.md").read_text(encoding="utf-8")
        self.assertIn(f"Файл: raw/{self.img.name}", md)
        self.assertIn("Описание медиа", md)
        self.assertTrue(rows[0]["injection_flags"] == [] or isinstance(rows[0]["injection_flags"], list))

    def test_media_dedup_and_custom_title(self):
        rec = participate.media(self.pdir, self.img, "На скриншоте воронка", title="Воронка онбординга")
        self.assertEqual(rec["title"], "Воронка онбординга")
        rec2 = participate.media(self.pdir, self.img, "На скриншоте воронка", title="Воронка онбординга")
        self.assertEqual(rec2["id"], rec["id"])
        self.assertEqual(len(core.read_jsonl(self.pdir / "sources.jsonl")), 1)

    def test_media_missing_file(self):
        from tools.pfs.core import PfsError
        with self.assertRaises(PfsError):
            participate.media(self.pdir, Path(TMP) / "no_such.png", "описание")


class UxScaffoldTests(unittest.TestCase):
    def test_ux_scaffold_created_and_idempotent(self):
        pdir = fresh(f"ux{id(self)}")
        s, _ = sources.add(pdir, text="скриншот и записи юзабилити-сессии", title="UX-материалы")
        path = participate.ux_scaffold(pdir, s["id"], focus="чек-аут")
        self.assertTrue(path.exists())
        self.assertEqual(path.parent, pdir / "analysis")
        self.assertEqual(path.name, f"ux_{s['id']}.md")
        text = path.read_text(encoding="utf-8")
        self.assertIn(s["id"], text)
        self.assertIn("чек-аут", text)
        self.assertIn("Не знаем", text)
        self.assertIn("только по материалу", text)
        # чек-лист из 8–10 пунктов
        items = [ln for ln in text.splitlines() if ln.strip().startswith(("- [ ]", "1."))]
        self.assertGreaterEqual(len(items), 8)
        self.assertLessEqual(len(items), 10)
        # idempotent: повтор возвращает тот же файл
        text2 = text + "\n<!-- заметки -->"
        path.write_text(text2, encoding="utf-8")
        again = participate.ux_scaffold(pdir, s["id"])
        self.assertEqual(again, path)
        self.assertIn("заметки", path.read_text(encoding="utf-8"))

    def test_ux_scaffold_unknown_source(self):
        from tools.pfs.core import PfsError
        pdir = fresh(f"uxb{id(self)}")
        with self.assertRaises(PfsError):
            participate.ux_scaffold(pdir, "S999")


if __name__ == "__main__":
    unittest.main()
