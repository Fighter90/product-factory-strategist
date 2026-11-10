"""Тесты pfs source fetch: цепочка попыток прямой → r.jina.ai → web.archive.org. Запуск: python3 -m unittest discover -s tests"""
import os
import tempfile
import unittest
from unittest import mock

TMP = tempfile.mkdtemp(prefix="pfs-test-fetch-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from tools.pfs import core, extract, project, sources  # noqa: E402
from tools.pfs.core import PfsError  # noqa: E402

URL = "https://example.org/pricing"


def page(text: str) -> bytes:
    return f"<html><head><title>Прайс</title></head><body><p>{text}</p></body></html>".encode("utf-8")


ERR_403 = PfsError("Не удалось загрузить https://example.org/pricing: HTTP Error 403: Forbidden")
ERR_SSL = PfsError("Не удалось загрузить https://example.org/pricing: SSL: CERTIFICATE_VERIFY_FAILED")
ERR_TIMEOUT = PfsError("Не удалось загрузить https://example.org/pricing: timed out")

READER_TEXT = ("Title: Hetzner Cloud Pricing\n\n"
               "Markdown Content:\n\n" + "CX22 shared vCPU стоит 3,79 евро в месяц по прайсу поставщика. " * 8)
READER_BYTES = (READER_TEXT.encode("utf-8"), "text/plain")
DIRECT_PAGE = (page("Прямой текст прайса: CX22 shared vCPU 3,79 евро в месяц, объём данных 20 ТБ. " * 8), "text/html")
ARCHIVE_PAGE = (page("Снапшот прайса из архива: CX22 shared vCPU 3,79 евро в месяц, объём данных 20 ТБ. " * 8), "text/html")
DIRECT_BODY = extract.html_to_text(DIRECT_PAGE[0].decode("utf-8"))[1]
ARCHIVE_BODY = extract.html_to_text(ARCHIVE_PAGE[0].decode("utf-8"))[1]
JS_SHELL = (b"<html><head><title>app</title></head><body><div id=app></div><script>render()</script></body></html>",
            "text/html")


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


class FetchTests(unittest.TestCase):
    def setUp(self):
        self.pdir = project.create(f"Тест fetch {id(self)}", "Кому продавать новый сервис?", slug=f"fc{id(self)}")

    def rows(self):
        return core.read_jsonl(self.pdir / "sources.jsonl")

    def logs(self):
        return [r for r in core.read_jsonl(self.pdir / "log.jsonl") if r.get("tool") == "pfs source fetch"]

    def test_403_falls_back_to_reader(self):
        """403 на прямом запросе: один вызов регистрирует источник через r.jina.ai, origin=excerpt."""
        with fetch_map(ERR_403, READER_BYTES, ARCHIVE_PAGE) as m:
            rec, created, channel = sources.fetch(self.pdir, URL, title="Hetzner pricing")
        self.assertTrue(created)
        self.assertEqual(channel, "reader")
        self.assertEqual(rec["url"], URL)
        self.assertEqual(rec["origin"], "excerpt")
        self.assertEqual(rec["kind"], "web")
        self.assertEqual(rec["via"], "reader")
        self.assertEqual(rec["title"], "Hetzner pricing")
        self.assertEqual(len(self.rows()), 1)  # зарегистрирован одним вызовом, без ручных шагов
        text = (self.pdir / "sources" / f"{rec['id']}.md").read_text(encoding="utf-8")
        self.assertIn("Канал получения: r.jina.ai (reader)", text)
        self.assertIn("ВЫПИСКА, первоисточник недоступен из среды", text)
        self.assertEqual(len(self.logs()), 1)

    def test_ssl_timeout_archive_wins(self):
        """SSL-ошибка и фолбэк-reader тоже недоступен: содержимое берётся из web.archive.org."""
        with fetch_map(ERR_SSL, ERR_TIMEOUT, ARCHIVE_PAGE):
            rec, created, channel = sources.fetch(self.pdir, URL)
        self.assertTrue(created)
        self.assertEqual(channel, "archive")
        self.assertEqual(rec["via"], "archive")
        self.assertIn("Снапшот прайса из архива", (self.pdir / "sources" / f"{rec['id']}.md").read_text(encoding="utf-8"))
        # заголовок не задан → берётся из страницы-снапшота
        self.assertEqual(rec["title"], "Прайс")

    def test_reader_title_fallback(self):
        """Без --title заголовок берётся из ответа reader (строка Title: …)."""
        with fetch_map(ERR_403, READER_BYTES, ARCHIVE_PAGE):
            rec, _, _ = sources.fetch(self.pdir, URL)
        self.assertEqual(rec["title"], "Hetzner Cloud Pricing")

    def test_js_shell_on_direct_moves_to_next_channel(self):
        """Прямой запрос вернул JS-пустышку (<200 знаков) → канал считается неудачей, берём reader."""
        with fetch_map(JS_SHELL, READER_BYTES, ARCHIVE_PAGE):
            rec, created, channel = sources.fetch(self.pdir, URL)
        self.assertTrue(created)
        self.assertEqual(channel, "reader")
        self.assertIn("3,79 евро", (self.pdir / "sources" / f"{rec['id']}.md").read_text(encoding="utf-8"))

    def test_direct_success_is_normal_web(self):
        """Прямой запрос удался: обычный web-источник, refresh по-прежнему работает."""
        with fetch_map(DIRECT_PAGE, ERR_TIMEOUT, ARCHIVE_PAGE):
            rec, created, channel = sources.fetch(self.pdir, URL)
        self.assertTrue(created)
        self.assertEqual(channel, "direct")
        self.assertEqual((rec["kind"], rec["via"], rec["origin"]), ("web", "direct", "excerpt"))
        self.assertEqual(rec["title"], "Прайс")
        new_page = (page("Обновлённый прайс: цена выросла до 4,19 евро в месяц по новым тарифам. " * 8), "text/html")
        with fetch_map(new_page, ERR_TIMEOUT, ARCHIVE_PAGE):
            res = sources.refresh(self.pdir, rec["id"])
        self.assertTrue(res["changed"])

    def test_all_fail_suggests_excerpt_text_file(self):
        """Ни один канал не ответил: понятная ошибка с предложением --text-file --origin excerpt, реестр не тронут."""
        with fetch_map(ERR_403, ERR_TIMEOUT, ERR_SSL):
            with self.assertRaises(PfsError) as cm:
                sources.fetch(self.pdir, URL)
        msg = str(cm.exception)
        self.assertIn("--text-file", msg)
        self.assertIn("--origin excerpt", msg)
        self.assertIn("выписка, первоисточник недоступен из среды", msg)
        for ch in ("direct", "reader", "archive"):
            self.assertIn(ch, msg)  # все каналы перечислены с причинами
        self.assertEqual(self.rows(), [])
        self.assertEqual(self.logs(), [])

    def test_dedup_by_url(self):
        with fetch_map(ERR_403, READER_BYTES, ARCHIVE_PAGE):
            rec1, created1, ch1 = sources.fetch(self.pdir, URL)
            rec2, created2, ch2 = sources.fetch(self.pdir, URL)
        self.assertTrue(created1)
        self.assertFalse(created2)
        self.assertEqual(rec1["id"], rec2["id"])
        self.assertEqual(ch2, "existing")
        self.assertEqual(len(self.rows()), 1)

    def test_domain_not_allowed(self):
        core.write_json(self.pdir / "project.json", {"allowed_sources": {"domains": ["example.com"]}})
        with fetch_map(ERR_403, READER_BYTES, ARCHIVE_PAGE) as m:
            with self.assertRaises(PfsError) as cm:
                sources.fetch(self.pdir, URL)
            m.assert_not_called()  # чужой домен отсекается до запросов
        self.assertIn("не входит в разрешённые", str(cm.exception))


class ExcerptOriginTests(unittest.TestCase):
    def setUp(self):
        self.pdir = project.create(f"Тест excerpt {id(self)}", "Почему падает удержание?", slug=f"ex{id(self)}")

    def test_excerpt_origin_registered_and_marked(self):
        """--origin excerpt разрешён и помечает источник выпиской (первоисточник недоступен из среды)."""
        self.assertIn("excerpt", sources.ORIGINS)
        rec, created = sources.add(self.pdir, text="Выписка исследователя: прайс Hetzner CX22 — 3,79 евро в месяц. " * 4,
                                   url=URL, origin="excerpt", title="Hetzner pricing (выписка)")
        self.assertTrue(created)
        self.assertEqual(rec["origin"], "excerpt")
        text = (self.pdir / "sources" / f"{rec['id']}.md").read_text(encoding="utf-8")
        self.assertIn("ВЫПИСКА, первоисточник недоступен из среды", text)
        self.assertIn("выписка", rec["title"].lower())

    def test_bad_origin_still_rejected(self):
        with self.assertRaises(PfsError):
            sources.add(self.pdir, text="текст", origin="github")
