"""PRO-83: детект «битых» источников — страниц 404/403. Прокси-каналы (r.jina.ai и другие)
отдают тело страницы ошибки с HTTP 200: каналы fetch валидируют контент, а не только код
ответа; при регистрации ставится пометка «битый источник», pfs check предупреждает.

Запуск: python3 -m unittest tests.test_source_404 -v
"""
import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest import mock

TMP = tempfile.mkdtemp(prefix="pfs-test-404-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from tools.pfs import check, cli, core, extract, project, sources  # noqa: E402
from tools.pfs.core import PfsError  # noqa: E402

URL = "https://www.jobscan.co/blog/ATS-resume-check/"
BROKEN_MARK = "БИТЫЙ ИСТОЧНИК"


def page(text: str, title: str = "Прайс") -> bytes:
    return f"<html><head><title>{title}</title></head><body><p>{text}</p></body></html>".encode("utf-8")


ERR_404 = PfsError("Не удалось загрузить " + URL + ": HTTP Error 404: Not Found")
ERR_NET = PfsError("Не удалось загрузить: сеть недоступна")

# r.jina.ai отдаёт тело 404-страницы с HTTP 200 (кейс PRO-83: ~6,7К знаков, валидный код ответа)
READER_404 = ("Title: Page not found - Jobscan\n\nMarkdown Content:\n\n"
              + "Ошибка 404: страница не найдена. Проверьте адрес или перейдите на главную. " * 12)
READER_404_BYTES = (READER_404.encode("utf-8"), "text/plain")
READER_OK = ("Title: Hetzner Cloud Pricing\n\nMarkdown Content:\n\n"
             + "CX22 shared vCPU стоит 3,79 евро в месяц по прайсу поставщика. " * 8)
READER_OK_BYTES = (READER_OK.encode("utf-8"), "text/plain")
GOOD_PAGE = (page("Прямой текст прайса: CX22 shared vCPU 3,79 евро в месяц, объём данных 20 ТБ. " * 8), "text/html")
ARCHIVE_404 = (page("404 Not Found — страница не найдена. Проверьте адрес ссылки. " * 12,
                    title="Page not found"), "text/html")
SOFT_404_PAGE = (page("К сожалению, такой страницы не существует. Ошибка 404: страница не найдена. " * 10,
                      title="Page not found - Jobscan"), "text/html")


def fetch_map(direct, reader, archive):
    """Патчит extract.fetch_url так, что каждый канал получает свой ответ/ошибку."""
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


class Detect404Tests(unittest.TestCase):
    """Детектор заголовка/тела 404-страницы: маркеры ловим, обычные заголовки не трогаем."""

    def test_titles_of_error_pages_detected(self):
        for t in ("Page not found - Jobscan", "404 Not Found", "Not Found", "403 Forbidden",
                  "Ошибка 404", "404 | This page could not be found", "Страница не найдена"):
            self.assertTrue(sources.is_404_title(t), f"404-заголовок не распознан: {t}")

    def test_normal_titles_not_flagged(self):
        for t in ("Прайс Hetzner Cloud", "How we cut 404s by 95%", "Chapter 66: Route 66",
                  "Метрики 2026", "Error handling in Python"):
            self.assertFalse(sources.is_404_title(t), f"обычный заголовок помечен как 404: {t}")

    def test_reader_body_with_title_404_detected(self):
        self.assertTrue(sources.is_404_body(READER_404))

    def test_reader_body_normal_not_flagged(self):
        self.assertFalse(sources.is_404_body(READER_OK))


class Fetch404Tests(unittest.TestCase):
    def setUp(self):
        self.pdir = project.create(f"Тест 404 {id(self)}", "Кому продавать новый сервис?", slug=f"nf{id(self)}")

    def rows(self):
        return core.read_jsonl(self.pdir / "sources.jsonl")

    def test_reader_404_body_falls_through_to_archive(self):
        """r.jina.ai отдал тело 404-страницы с HTTP 200 → канал валидирует контент:
        берём web.archive.org, а не регистрируем страницу ошибки как источник (PRO-83)."""
        with fetch_map(ERR_404, READER_404_BYTES, GOOD_PAGE):
            rec, created, channel = sources.fetch(self.pdir, URL)
        self.assertTrue(created)
        self.assertEqual(channel, "archive")
        self.assertEqual(rec["via"], "archive")
        self.assertNotIn("broken_404", rec)
        md = (self.pdir / "sources" / f"{rec['id']}.md").read_text(encoding="utf-8")
        self.assertIn("3,79 евро", md)  # живой текст, не страница ошибки
        self.assertNotIn("Page not found", md)
        self.assertNotIn(BROKEN_MARK, md)

    def test_all_channels_404_registers_broken_source_with_warning(self):
        """Все каналы вернули только тело 404-страницы: источник регистрируется с пометкой
        «битый» и предупреждением при регистрации (PRO-83) — не как валидный без слов."""
        with fetch_map(ERR_404, READER_404_BYTES, ARCHIVE_404):
            rec, created, channel = sources.fetch(self.pdir, URL)
        self.assertTrue(created)
        self.assertTrue(rec.get("broken_404"))
        self.assertEqual(rec["via"], "archive")  # последний битый канал — не записан как успех
        md = (self.pdir / "sources" / f"{rec['id']}.md").read_text(encoding="utf-8")
        self.assertIn(BROKEN_MARK, md)  # предупреждение в шапке файла источника
        self.assertIn("404", md)
        log = [r for r in core.read_jsonl(self.pdir / "log.jsonl") if r.get("tool") == "pfs source fetch"]
        self.assertTrue(log and "404" in log[-1].get("msg", ""))

    def test_cli_fetch_prints_broken_warning(self):
        args = cli.build_parser().parse_args(["--project", self.pdir.name, "source", "fetch", URL])
        out = io.StringIO()
        with fetch_map(ERR_404, READER_404_BYTES, ARCHIVE_404), redirect_stdout(out):
            args.f(args)
        self.assertIn(BROKEN_MARK, out.getvalue())

    def test_add_url_soft404_registers_broken(self):
        """add по URL: сайт сам отдал 404-страницу с HTTP 200 (soft 404) — пометка «битый источник»."""
        with mock.patch("tools.pfs.extract.fetch_url", return_value=SOFT_404_PAGE):
            rec, created = sources.add(self.pdir, URL)
        self.assertTrue(created)
        self.assertTrue(rec.get("broken_404"))
        self.assertIn(BROKEN_MARK, (self.pdir / "sources" / f"{rec['id']}.md").read_text(encoding="utf-8"))

    def test_add_url_good_page_not_flagged(self):
        with mock.patch("tools.pfs.extract.fetch_url", return_value=GOOD_PAGE):
            rec, _ = sources.add(self.pdir, URL)
        self.assertNotIn("broken_404", rec)

    def test_refresh_refuses_broken_404_update(self):
        """refresh при умершей ссылке не затирает живой источник телом 404-страницы."""
        with fetch_map(GOOD_PAGE, ERR_NET, ERR_NET):
            rec, _, _ = sources.fetch(self.pdir, URL)
        old_md = (self.pdir / "sources" / f"{rec['id']}.md").read_text(encoding="utf-8")
        with fetch_map(ERR_404, READER_404_BYTES, ARCHIVE_404):
            with self.assertRaises(PfsError) as cm:
                sources.refresh(self.pdir, rec["id"])
        self.assertIn("404", str(cm.exception))
        self.assertEqual((self.pdir / "sources" / f"{rec['id']}.md").read_text(encoding="utf-8"), old_md)
        self.assertNotIn("broken_404", [r for r in self.rows() if r["id"] == rec["id"]][0])

    def test_check_warns_on_broken_and_404_title(self):
        """pfs check: предупреждение на источник-пометку broken_404 и на записи с 404-заголовком."""
        with fetch_map(ERR_404, READER_404_BYTES, ARCHIVE_404):
            rec, _, _ = sources.fetch(self.pdir, URL)
        # «легаси»-запись без пометки, но с заголовком страницы ошибки
        legacy, _ = sources.add(self.pdir, text="Текст выписки про 404-страницу сайта. " * 6,
                                title="Page not found - Example")
        res = check.run(self.pdir)
        hits = [w for w in res["warnings"] if "404" in w]
        self.assertTrue(any(rec["id"] in w for w in hits), f"нет предупреждения о битом источнике: {hits}")
        self.assertTrue(any(legacy["id"] in w for w in hits), f"нет предупреждения о 404-заголовке: {hits}")

    def test_check_silent_for_normal_sources(self):
        with fetch_map(GOOD_PAGE, ERR_NET, ERR_NET):
            sources.fetch(self.pdir, URL)
        res = check.run(self.pdir)
        self.assertFalse([w for w in res["warnings"] if "404" in w])


if __name__ == "__main__":
    unittest.main()
