"""PRO-59, round 2 (правки ревью): транзитивная опора на выписки через derived_from,
сырые ответы каналов fetch в sources/raw/, параллельная HTTPS-проверка doctor
и отсутствие повреждённых символов (U+FFFD) в коде pfs.

Запуск: python3 -m unittest tests.test_pro59_round2 -v
"""
import hashlib
import io
import os
import sys
import tempfile
import time
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

TMP = tempfile.mkdtemp(prefix="pfs-test-r2-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from tools.pfs import check, claims, extract, project, sources  # noqa: E402
from tools.pfs.core import PfsError  # noqa: E402

URL = "https://example.org/pricing"
EXCERPT_TEXT = "Выписка: CX22 shared vCPU стоит 3,79 евро в месяц по прайсу поставщика. " * 4
PUBLIC_TEXT = "Публичный прайс: CX22 стоит 3,79 евро в месяц. " * 4


def page(text: str) -> bytes:
    return f"<html><head><title>Прайс</title></head><body><p>{text}</p></body></html>".encode("utf-8")


ERR = PfsError("Не удалось загрузить: сеть недоступна")


def fetch_map(direct, reader, archive):
    def side(url):
        if url == URL:
            v = direct
        elif url.startswith("https://r.jina.ai/"):
            v = reader
        elif url.startswith("https://web.archive.org/web/"):
            v = archive
        else:
            raise AssertionError(f"неожиданный URL запроса: {url}")
        if isinstance(v, Exception):
            raise v
        return v
    return mock.patch("tools.pfs.extract.fetch_url", side_effect=side)


def raw_name(url: str, ext: str) -> str:
    return f"sources/raw/{hashlib.sha1(url.encode()).hexdigest()[:10]}{ext}"


class TransitiveExcerptCapTests(unittest.TestCase):
    """Вывод, построенный только на фактах-выписках (derived_from), ограничивается так же:
    сила не выше C, пока первоисточник не перепроверен (ревью round 2, замечание 2)."""

    def setUp(self):
        self.pdir = project.create(f"Транзитивные выписки {id(self)}", "Почему падает удержание?",
                                   slug=f"tc{id(self)}")
        self.src, _ = sources.add(self.pdir, text=EXCERPT_TEXT, url=URL, origin="excerpt",
                                  title="Прайс (выписка)")
        self.fact = claims.add(self.pdir, "CX22 — 3,79 евро в месяц по выписке", "fact",
                               [self.src["id"]], grade="C")

    def test_inference_on_excerpt_fact_rejected_for_grade_b(self):
        with self.assertRaises(PfsError) as cm:
            claims.add(self.pdir, "Вывод: цена ниже рынка", "inference", derived_from=[self.fact["id"]],
                       grade="B")
        msg = str(cm.exception)
        self.assertIn("не выше C", msg)
        self.assertIn("derived_from", msg)  # в сообщении назван транзитивный путь опоры

    def test_inference_on_excerpt_fact_allows_grade_c(self):
        c = claims.add(self.pdir, "Вывод: цена ниже рынка", "inference",
                       derived_from=[self.fact["id"]], grade="C")
        self.assertEqual(c["grade"], "C")

    def test_cap_reaches_through_two_inference_hops(self):
        mid = claims.add(self.pdir, "Промежуточный вывод", "inference", derived_from=[self.fact["id"]])
        with self.assertRaises(PfsError):
            claims.add(self.pdir, "Вывод через два шага", "inference", derived_from=[mid["id"]],
                       grade="A")

    def test_mixed_basis_keeps_high_grade(self):
        pub, _ = sources.add(self.pdir, text=PUBLIC_TEXT, title="Публичный прайс")
        c = claims.add(self.pdir, "Вывод с публичной опорой", "inference", [pub["id"]],
                       derived_from=[self.fact["id"]], grade="B")
        self.assertEqual(c["grade"], "B")

    def test_cycle_in_derived_from_does_not_hang(self):
        """Защита от цикла в derived_from (ручная правка реестра): не зависаем, не падаем."""
        c = claims.add(self.pdir, "Вывод с циклом в основаниях", "inference",
                       derived_from=[self.fact["id"]], grade="C")
        rows = claims.load(self.pdir)
        rows[0]["derived_from"] = [c["id"]]  # вручную замкнули цикл: fact → inference → fact
        core_write = self.pdir / "claims.jsonl"
        import json
        core_write.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows),
                              encoding="utf-8")
        c2 = claims.add(self.pdir, "Ещё вывод поверх цикла", "inference", derived_from=[c["id"]],
                        grade="C")
        self.assertEqual(c2["grade"], "C")


class CheckTransitiveExcerptWarningTests(unittest.TestCase):
    """check предупреждает и для выводов, опирающихся на выписки транзитивно (derived_from)."""

    def setUp(self):
        self.pdir = project.create(f"Check транзит {id(self)}", "Почему падает удержание?",
                                   slug=f"ct{id(self)}")

    def test_warning_for_inference_on_excerpt_fact(self):
        src, _ = sources.add(self.pdir, text=EXCERPT_TEXT, url=URL, origin="excerpt",
                             title="Прайс (выписка)")
        fact = claims.add(self.pdir, "CX22 — 3,79 евро в месяц", "fact", [src["id"]], grade="C")
        claims.add(self.pdir, "Вывод: цена ниже рынка", "inference", derived_from=[fact["id"]])
        res = check.run(self.pdir)
        hit = [w for w in res["warnings"] if "выписки" in w and src["id"] in w]
        self.assertTrue(hit, f"нет предупреждения о транзитивных выписках: {res['warnings']}")

    def test_no_warning_when_ancestor_is_public(self):
        pub, _ = sources.add(self.pdir, text=PUBLIC_TEXT, title="Публичный прайс")
        fact = claims.add(self.pdir, "Публично подтверждённый прайс", "fact", [pub["id"]], grade="B")
        claims.add(self.pdir, "Вывод на публичном факте", "inference", derived_from=[fact["id"]])
        res = check.run(self.pdir)
        self.assertFalse([w for w in res["warnings"] if "выписки" in w])


class BrowserRawHtmlTests(unittest.TestCase):
    """Сырой HTML каналов fetch сохраняется в sources/raw/ (ревью round 2, замечание 3):
    браузерный рендер — как direct/reader/archive."""

    def setUp(self):
        self.pdir = project.create(f"Raw каналы {id(self)}", "Кому продавать сервис?", slug=f"rw{id(self)}")
        self.html = ("<html><head><title>Рендер</title></head><body><p>Загружено через браузер: "
                     "CX22 shared vCPU стоит 3,79 евро в месяц по прайсу поставщика. " * 8 + "</p></body></html>")

    def test_fetch_via_browser_saves_raw_html(self):
        with mock.patch.object(extract, "fetch_via_browser", return_value=self.html):
            rec, created, _ = sources.fetch(self.pdir, URL, via_browser=True)
        self.assertTrue(created)
        self.assertEqual(rec["path"], raw_name(URL, ".html"))
        raw = self.pdir / rec["path"]
        self.assertTrue(raw.exists())
        self.assertEqual(raw.read_text(encoding="utf-8"), self.html)

    def test_reader_channel_saves_raw_text(self):
        reader_text = ("Title: Прайс\n\nMarkdown Content:\n\n"
                       + "Текст через reader: CX22 стоит 3,79 евро в месяц. " * 20)
        with fetch_map(ERR, (reader_text.encode("utf-8"), "text/plain"), ERR):
            rec, created, channel = sources.fetch(self.pdir, URL)
        self.assertTrue(created)
        self.assertEqual(channel, "reader")
        self.assertEqual(rec["path"], raw_name(URL, ".txt"))
        self.assertIn("Markdown Content", (self.pdir / rec["path"]).read_text(encoding="utf-8"))

    def test_archive_channel_saves_raw_html(self):
        long_public = "Публичный прайс поставщика: CX22 стоит 3,79 евро в месяц по счётчику. " * 6
        with fetch_map(ERR, ERR, (page(long_public), "text/html")):
            rec, created, channel = sources.fetch(self.pdir, URL)
        self.assertTrue(created)
        self.assertEqual(channel, "archive")
        self.assertEqual(rec["path"], raw_name(URL, ".html"))

    def test_add_url_saves_raw_html(self):
        with mock.patch.object(extract, "fetch_url", return_value=(page(EXCERPT_TEXT), "text/html")):
            rec, _ = sources.add(self.pdir, URL)
        self.assertEqual(rec["path"], raw_name(URL, ".html"))
        self.assertTrue((self.pdir / rec["path"]).exists())


class ProbeParallelTests(unittest.TestCase):
    """HTTPS-проверка doctor: домены опрашиваются параллельно — офлайн doctor не ждёт
    3×timeout последовательно (ревью round 2, замечание 4)."""

    def test_probe_runs_domains_in_parallel(self):
        def slow_get(url, timeout):
            time.sleep(0.5)
            return "ok"

        t0 = time.monotonic()
        res = extract.https_probe(get=slow_get, timeout=1)
        elapsed = time.monotonic() - t0
        self.assertEqual([st for _, st in res], ["ok", "ok", "ok"])
        self.assertLess(elapsed, 1.4, f"зонды отработали последовательно ({elapsed:.2f}с вместо ≤1.4с)")

    def test_probe_preserves_order_and_statuses(self):
        def get(url, timeout):
            return {"https://pypi.org/simple/": "ok", "https://www.python.org/": "ssl",
                    "https://example.com/": "net"}[url]

        res = extract.https_probe(get=get, timeout=1)
        self.assertEqual(res, [("pypi.org", "ok"), ("www.python.org", "ssl"), ("example.com", "net")])


class NoCorruptedCharsTests(unittest.TestCase):
    """Ревью round 2, замечание 1: U+FFFD (повреждённые символы, кейс «перепроверка»)
    не появляются в коде pfs — регрессионная защита на все файлы пакета."""

    def test_no_replacement_chars_in_pfs_code(self):
        pkg = Path(sources.__file__).parent
        bad = sorted(p.name for p in pkg.glob("*.py") if "\ufffd" in p.read_text(encoding="utf-8"))
        self.assertEqual(bad, [])

    def test_refresh_docstring_word_is_intact(self):
        doc = (Path(sources.__file__).read_text(encoding="utf-8"))
        self.assertIn("перепроверка", doc)
        self.assertNotIn("\ufffd", doc)


if __name__ == "__main__":
    unittest.main()
