"""PRO-59: сила выписок не выше C, предупреждение check о выводах только на выписках,
режим --excerpt (origin=excerpt + обязательные URL и дата), --via-browser (Playwright)
и снятие пометки выписки при прямом ответе первоисточника (pfs source refresh).

Запуск: python3 -m unittest tests.test_excerpt_strength -v
"""
import json
import io
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest import mock

TMP = tempfile.mkdtemp(prefix="pfs-test-cap-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from tools.pfs import check, claims, cli, core, extract, project, sources  # noqa: E402
from tools.pfs.core import PfsError  # noqa: E402

URL = "https://example.org/pricing"
EXCERPT_TEXT = "Выписка: CX22 shared vCPU стоит 3,79 евро в месяц по прайсу поставщика. " * 4


def page(text: str) -> bytes:
    return f"<html><head><title>Прайс</title></head><body><p>{text}</p></body></html>".encode("utf-8")


ERR = PfsError("Не удалось загрузить: сеть недоступна")


def fetch_map(direct, reader, archive):
    def side(url):
        if url == URL:
            return _answer(direct)
        if url.startswith("https://r.jina.ai/"):
            return _answer(reader)
        if url.startswith("https://web.archive.org/web/"):
            return _answer(archive)
        raise AssertionError(f"неожиданный URL запроса: {url}")
    return mock.patch("tools.pfs.extract.fetch_url", side_effect=side)


def _answer(v):
    if isinstance(v, Exception):
        raise v
    return v


class GradeCapTests(unittest.TestCase):
    """Утверждение только на выписках (origin=excerpt) — сила не выше C (grade A/B отклоняется)."""

    def setUp(self):
        self.pdir = project.create(f"Сила выписок {id(self)}", "Почему падает удержание?", slug=f"cap{id(self)}")
        self.rec, _ = sources.add(self.pdir, text=EXCERPT_TEXT, url=URL, origin="excerpt", title="Прайс (выписка)")

    def test_grade_b_on_excerpt_only_rejected(self):
        with self.assertRaises(PfsError) as cm:
            claims.add(self.pdir, "Прайс CX22 — 3,79 евро в месяц по выписке поставщика", "fact",
                       [self.rec["id"]], grade="B")
        self.assertIn("не выше C", str(cm.exception))
        self.assertIn("refresh", str(cm.exception))  # путь снятия ограничения подсказан

    def test_grade_c_allowed_on_excerpt(self):
        c = claims.add(self.pdir, "CX22: 3,79 евро в месяц по прайсу", "fact", [self.rec["id"]], grade="C")
        self.assertEqual(c["grade"], "C")

    def test_mixed_sources_keep_high_grade(self):
        pub, _ = sources.add(self.pdir, text="Публичный прайс: CX22 стоит 3,79 евро в месяц. " * 4,
                             title="Публичный прайс")
        c = claims.add(self.pdir, "Прайс подтверждён двумя источниками сразу", "fact",
                       [self.rec["id"], pub["id"]], grade="B")
        self.assertEqual(c["grade"], "B")  # есть непроверенная-выпиской опора — ограничение не действует

    def test_batch_line_rejected_for_excerpt_grade_b(self):
        batch = self.pdir / "batch.jsonl"
        batch.write_text(json.dumps({"text": "Батч-утверждение про 3,79 евро из выписки", "kind": "fact",
                                     "source": self.rec["id"], "grade": "B"}), encoding="utf-8")
        with self.assertRaises(PfsError) as cm:
            claims.add_batch(self.pdir, batch)
        self.assertIn("не выше C", str(cm.exception))
        self.assertEqual(claims.load(self.pdir), [])  # невалидная строка отменяет весь батч


class CheckExcerptWarningTests(unittest.TestCase):
    """check предупреждает, если утверждение опирается только на выписки."""

    def setUp(self):
        self.pdir = project.create(f"Check выписки {id(self)}", "Почему падает удержание?", slug=f"ck{id(self)}")

    def test_warning_when_claim_rests_only_on_excerpts(self):
        rec, _ = sources.add(self.pdir, text=EXCERPT_TEXT, url=URL, origin="excerpt", title="Прайс (выписка)")
        claims.add(self.pdir, "CX22 — 3,79 евро в месяц по выписке", "hypothesis", [rec["id"]])
        res = check.run(self.pdir)
        hit = [w for w in res["warnings"] if "выписки" in w and rec["id"] in w]
        self.assertTrue(hit, f"нет предупреждения о выписках: {res['warnings']}")

    def test_no_warning_for_public_source(self):
        pub, _ = sources.add(self.pdir, text="Публичный текст с наблюдением о прайсе. " * 4, title="Публичный")
        claims.add(self.pdir, "Публично подтверждённое наблюдение", "hypothesis", [pub["id"]])
        res = check.run(self.pdir)
        self.assertFalse([w for w in res["warnings"] if "выписки" in w])


class ExcerptFlagTests(unittest.TestCase):
    """--excerpt: origin=excerpt, обязательны --text-file, --url и --published (дата)."""

    def setUp(self):
        self.pdir = project.create(f"Флаг выписки {id(self)}", "Кому продавать сервис?", slug=f"ef{id(self)}")
        self.text_file = self.pdir / "excerpt_note.md"
        self.text_file.write_text(EXCERPT_TEXT, encoding="utf-8")

    def _run(self, *extra):
        args = cli.build_parser().parse_args(
            ["--project", self.pdir.name, "source", "add",
             "--text-file", str(self.text_file), "--url", URL, "--title", "Прайс (выписка)", *extra])
        with redirect_stdout(io.StringIO()):
            args.f(args)

    def test_excerpt_flag_registers_excerpt_with_url_and_date(self):
        self._run("--excerpt", "--published", "2026-01-15")
        rows = core.read_jsonl(self.pdir / "sources.jsonl")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["origin"], "excerpt")
        self.assertEqual(rows[0]["url"], URL)
        self.assertEqual(rows[0]["published"], "2026-01-15")
        md = (self.pdir / "sources" / f"{rows[0]['id']}.md").read_text(encoding="utf-8")
        self.assertIn("ВЫПИСКА", md)
        self.assertIn("2026-01-15", md)

    def test_excerpt_flag_requires_text_file_url_and_date(self):
        args = cli.build_parser().parse_args(["--project", self.pdir.name, "source", "add",
                                              "--text-file", str(self.text_file), "--excerpt"])
        with self.assertRaises(PfsError) as cm:
            args.f(args)
        msg = str(cm.exception)
        self.assertIn("--url", msg)
        self.assertIn("--published", msg)
        args = cli.build_parser().parse_args(["--project", self.pdir.name, "source", "add",
                                              "--url", URL, "--excerpt", "--published", "2026-01-15"])
        with self.assertRaises(PfsError) as cm:
            args.f(args)
        self.assertIn("--text-file", str(cm.exception))
        self.assertEqual(core.read_jsonl(self.pdir / "sources.jsonl"), [])  # ничего не записано

    def test_excerpt_flag_conflicting_origin_rejected(self):
        with self.assertRaises(PfsError):
            self._run("--excerpt", "--published", "2026-01-15", "--origin", "public")

    def test_excerpt_flag_rejected_on_fetch(self):
        args = cli.build_parser().parse_args(["--project", self.pdir.name, "source", "fetch", URL, "--excerpt"])
        with self.assertRaises(PfsError):
            with redirect_stdout(io.StringIO()):
                args.f(args)


class ViaBrowserTests(unittest.TestCase):
    """--via-browser: рендер JS-страницы через Playwright (если установлен), иначе подсказка и --excerpt."""

    def setUp(self):
        self.pdir = project.create(f"Браузер {id(self)}", "Кому продавать сервис?", slug=f"vb{id(self)}")

    def test_fetch_via_browser_registers_public_source(self):
        html = ("<html><head><title>Рендер</title></head><body><p>Загружено через браузер: "
                "CX22 shared vCPU стоит 3,79 евро в месяц по прайсу поставщика. " * 8 + "</p></body></html>")
        with mock.patch.object(extract, "fetch_via_browser", return_value=html) as m:
            rec, created, channel = sources.fetch(self.pdir, URL, via_browser=True)
        m.assert_called_once_with(URL)
        self.assertTrue(created)
        self.assertEqual((channel, rec["via"], rec["origin"]), ("browser", "browser", "public"))
        md = (self.pdir / "sources" / f"{rec['id']}.md").read_text(encoding="utf-8")
        self.assertIn("Playwright", md)  # канал получения помечен
        self.assertNotIn("ВЫПИСКА", md)  # контент с сайта напрямую — не выписка

    def test_browser_failure_suggests_excerpt(self):
        with mock.patch.object(extract, "fetch_via_browser",
                               side_effect=PfsError("Браузерный рендер не удался. Сохраните текст: --excerpt")):
            with self.assertRaises(PfsError) as cm:
                sources.fetch(self.pdir, URL, via_browser=True)
        self.assertIn("--excerpt", str(cm.exception))

    def test_fetch_via_browser_without_playwright_names_install_command(self):
        """Playwright не установлен (нулевые зависимости): готовая команда установки + фолбэк --excerpt."""
        with mock.patch.object(extract.socket, "getaddrinfo", return_value=[("AF_INET", 1, 6, "", ("93.184.216.34", 0))]), \
             mock.patch.dict(sys.modules, {"playwright": None}):
            with self.assertRaises(PfsError) as cm:
                extract.fetch_via_browser(URL)
        msg = str(cm.exception)
        self.assertIn("pip install playwright", msg)
        self.assertIn("--excerpt", msg)

    def test_add_rejects_via_browser_flag(self):
        args = cli.build_parser().parse_args(["--project", self.pdir.name, "source", "add", URL, "--via-browser"])
        with self.assertRaises(PfsError):
            with redirect_stdout(io.StringIO()):
                args.f(args)


class RefreshVerifyTests(unittest.TestCase):
    """Выписка перепроверена: прямой ответ первоисточника снимает origin=excerpt (открывает силу выше C)."""

    def setUp(self):
        self.pdir = project.create(f"Перепроверка {id(self)}", "Почему падает удержание?", slug=f"rv{id(self)}")
        body = extract.html_to_text(page(EXCERPT_TEXT).decode("utf-8"))[1]
        self.rec, _ = sources.add(self.pdir, text=body, url=URL, origin="excerpt", title="Прайс (выписка)")

    def _row(self):
        return [r for r in core.read_jsonl(self.pdir / "sources.jsonl") if r["id"] == self.rec["id"]][0]

    def test_refresh_unchanged_direct_clears_excerpt_origin(self):
        direct = (page(EXCERPT_TEXT), "text/html")
        with fetch_map(direct, ERR, ERR):
            res = sources.refresh(self.pdir, self.rec["id"])
        self.assertFalse(res["changed"])  # текст тот же — не считаем обновлением
        self.assertTrue(res["verified"])
        self.assertEqual(self._row()["origin"], "public")
        md = (self.pdir / "sources" / f"{self.rec['id']}.md").read_text(encoding="utf-8")
        self.assertNotIn("ВЫПИСКА", md)  # шапка файла согласована с реестром

    def test_refresh_changed_direct_clears_excerpt_origin(self):
        new_page = (page("Обновлённый прайс: цена выросла до 4,19 евро в месяц по новым тарифам. " * 4), "text/html")
        with fetch_map(new_page, ERR, ERR):
            res = sources.refresh(self.pdir, self.rec["id"])
        self.assertTrue(res["changed"])
        self.assertTrue(res["verified"])
        self.assertEqual(self._row()["origin"], "public")

    def test_refresh_via_reader_keeps_excerpt_origin(self):
        reader_text = ("Title: Прайс\n\nMarkdown Content:\n\n"
                       + "Обновлённый текст через reader: CX22 стоит 4,19 евро в месяц. " * 4)
        reader = (reader_text.encode("utf-8"), "text/plain")
        with fetch_map(ERR, reader, ERR):
            res = sources.refresh(self.pdir, self.rec["id"])
        self.assertTrue(res["changed"])
        self.assertFalse(res["verified"])  # первоисточник не отвечал напрямую — пометка остаётся
        self.assertEqual(self._row()["origin"], "excerpt")


if __name__ == "__main__":
    unittest.main()
