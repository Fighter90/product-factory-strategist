"""PRO-129: REGRESS-SITE strategyproduct.ru — проверки сайта из основного репо.

Сайт живёт в отдельном git-репо `site/` (product-factory-strategist-site,
деплой на GitHub Pages, CNAME strategyproduct.ru). Он git-игнорируется основным
репо, поэтому без `site/` (CI GitLab клонирует только основной репо) тесты
скипаются; локально с сайтом — гоняются.

Контрольные точки (issue PRO-129):
1. `site/scripts/check_site.py` — скрипт проверки href/src: битых внутренних
   ссылок и фрагментов нет, html сбалансирован.
2. Вьюпорт на каждой странице; статические риски «разъезда» на 375px
   (фиксированные ширины вне min()/процентов, отсутствие брейкпоинтов) = 0.
3. Запрещённые бренды (мегафон, магистрат, ВШЭ, НИУ, авито) = 0; секретов
   (ключи/токены, id счётчика, личные пути) = 0.
4. Счётчики (карты, EN-зеркала, навыки, субагенты, хуки, тесты) на страницах
   = vendor/meta.json = реальность основного репо.
5. Все страницы отдаются локальным сервером с кодом 200.
6. Механика чекера: на синтетическом сайте с битой ссылкой/секретом/пропавшим
   вьюпортом/расходящимся счётчиком — ненулевой код выхода и находка в JSON.

Демо-раздел «Связь для близких» — отдельная большая правка контента
(шагающий разбор demo.html, материалы, скриншоты); чекер репортит её
отдельным предупреждением, чтобы не потерять при следующих прогонах.

Запуск: python3 -m unittest tests.test_site_regress -v
"""
import json
import subprocess
import sys
import unittest
import http.server
import http.client
import threading
import tempfile
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SITE = REPO / "site"
CHECKER = SITE / "scripts" / "check_site.py"
VENDOR = SITE / "vendor" / "meta.json"

PAGES = ["index.html", "demo.html", "help.html", "materials.html"]


def run_checker(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(CHECKER), *args],
        capture_output=True, text=True, timeout=120, cwd=str(REPO))


class CheckerMechanicsTests(unittest.TestCase):
    """Чекер ловит дефекты на синтетическом сайте (без site/ — тоже работает)."""

    @classmethod
    def setUpClass(cls):
        if not CHECKER.exists():
            raise unittest.SkipTest("нет site/scripts/check_site.py")
        cls.tmp = tempfile.mkdtemp(prefix="pfs-check-site-")
        cls.good_root = cls._make_site("good")
        cls.dirty_root = cls._make_site("dirty")

    @classmethod
    def _make_site(cls, kind: str) -> Path:
        root = Path(cls.tmp) / kind
        (root / "en").mkdir(parents=True)
        (root / "vendor").mkdir()
        (root / "vendor" / "meta.json").write_text(
            json.dumps({"N_MAPS": 3, "N_MAPS_EN": 3, "N_SKILLS": 4,
                        "N_AGENTS": 1, "N_HOOKS": 1, "N_TESTS": 5, "N_MCP": 2}),
            encoding="utf-8")
        if kind == "good":
            body = ('<a href="demo.html#top">d</a><span id="top"></span>'
                    '<b>3</b> методических карт · Автотесты CLI (5) · навыков: 4')
        else:
            body = ('<a href="missing.html">x</a><a href="#nope">y</a>'
                    ' тарифы МегаФона api_key="sk-abcdef1234567890"'
                    ' <div style="width:1200px">w</div>'
                    '<b>2</b> методических карт · Автотесты CLI (4) · навыков: 9')
        head = ('<!doctype html><html lang="ru"><head><meta charset="utf-8">'
                '<meta name="viewport" content="width=device-width, initial-scale=1">'
                '<style>@media (max-width:980px){.links{display:none}}'
                '@media (max-width:640px){.stats{grid-template-columns:1fr}}</style>'
                '</head><body>')
        (root / "index.html").write_text(head + body + '</body></html>', encoding="utf-8")
        demo_head = head if kind == "good" else (
            '<!doctype html><html lang="ru"><head><meta charset="utf-8"></head><body>')
        (root / "demo.html").write_text(demo_head + body + '</body></html>', encoding="utf-8")
        return root

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_clean_site_passes(self):
        r = run_checker("--root", str(self.good_root), "--json")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        data = json.loads(r.stdout)
        self.assertEqual(data["broken_links"], [])
        self.assertEqual(data["forbidden"], [])
        self.assertEqual(data["secrets"], [])
        self.assertEqual(data["missing_viewport"], [])
        self.assertEqual(data["css_issues"], [])
        self.assertEqual(data["counter_mismatches"], [])

    def test_broken_link_secret_brand_width_counter_detected(self):
        r = run_checker("--root", str(self.dirty_root), "--json")
        self.assertNotEqual(r.returncode, 0, r.stdout + r.stderr)
        data = json.loads(r.stdout)
        urls = {b["url"] for b in data["broken_links"]}
        self.assertIn("missing.html", urls)
        self.assertTrue(any(b["why"] == "fragment" for b in data["broken_links"]))
        self.assertTrue(any("мегафон" in f["match"].lower() for f in data["forbidden"]))
        self.assertTrue(data["secrets"], "секрет не обнаружен")
        self.assertIn("demo.html", data["missing_viewport"])
        self.assertTrue(any(i.get("why") == "fixed-width" for i in data["css_issues"]))
        kinds = {m["name"] for m in data["counter_mismatches"]}
        self.assertTrue({"N_MAPS", "N_TESTS", "N_SKILLS"} <= kinds,
                        f"ожидались N_MAPS/N_TESTS/N_SKILLS, получено: {kinds}")

    def test_escaping_link_detected(self):
        # ссылка, выходящая за корень сайта, — битая по определению
        (self.dirty_root / "esc.html").write_text(
            '<!doctype html><html><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width"></head>'
            '<body><a href="../../outside.html">x</a></body></html>', encoding="utf-8")
        try:
            r = run_checker("--root", str(self.dirty_root), "--json")
            data = json.loads(r.stdout)
            self.assertTrue(any(b["why"] == "escapes-root" and b["url"] == "../../outside.html"
                                for b in data["broken_links"]), data["broken_links"])
        finally:
            (self.dirty_root / "esc.html").unlink()


@unittest.skipUnless(SITE.exists() and VENDOR.exists(),
                     "нет локального клона site/ (GitLab CI клонирует только основной репо)")
class SiteRegressTests(unittest.TestCase):
    """Реальный сайт: ссылки, бренды, секреты, вьюпорт, счётчики, 200."""

    @classmethod
    def setUpClass(cls):
        if not CHECKER.exists():
            raise unittest.SkipTest("нет site/scripts/check_site.py")
        cls.data = json.loads(run_checker("--root", str(SITE), "--repo", str(REPO),
                                          "--json").stdout)

    def test_no_broken_links(self):
        self.assertEqual(self.data["broken_links"], [],
                         f"битые ссылки: {self.data['broken_links'][:5]}")

    def test_viewport_everywhere(self):
        self.assertEqual(self.data["missing_viewport"], [])

    def test_no_forbidden_brands(self):
        self.assertEqual(self.data["forbidden"], [],
                         f"запрещённые бренды: {self.data['forbidden'][:5]}")

    def test_no_secrets(self):
        self.assertEqual(self.data["secrets"], [],
                         f"секреты: {self.data['secrets'][:5]}")

    def test_no_css_375_risks(self):
        self.assertEqual(self.data["css_issues"], [],
                         f"риски 375px: {self.data['css_issues'][:5]}")

    def test_counters_match_vendor_and_repo(self):
        vendor = json.loads(VENDOR.read_text(encoding="utf-8"))
        repo_avail = self.data.get("repo_counters") or {}
        for name, shown_list in self.data["counters"].items():
            for shown in shown_list:
                self.assertEqual(int(shown), int(vendor[name]),
                                 f"{name}: на сайте {shown}, в vendor {vendor[name]}")
                if name in repo_avail:
                    self.assertEqual(int(shown), int(repo_avail[name]),
                                     f"{name}: на сайте {shown}, в репо {repo_avail[name]}")

    def test_counter_mismatches_empty(self):
        self.assertEqual(self.data["counter_mismatches"], [])

    def test_all_pages_served_200(self):
        root = SITE

        class QuietHandler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *a, **k):
                super().__init__(*a, directory=str(root), **k)

            def log_message(self, *a):  # тишина: Broken pipe при закрытии не шумит
                pass

        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), QuietHandler)
        server.handle_error = lambda *a: None
        t = threading.Thread(target=server.serve_forever, daemon=True)
        t.start()
        try:
            host, port = server.server_address
            for rel in PAGES + [f"en/{p}" for p in PAGES] + [
                    "assets/logo.svg", "assets/og/og.jpg"]:
                conn = http.client.HTTPConnection(host, port, timeout=15)
                try:
                    conn.request("GET", "/" + rel)
                    resp = conn.getresponse()
                    body = resp.read()
                    self.assertEqual(resp.status, 200, rel)
                    self.assertTrue(body, rel)
                finally:
                    conn.close()
        finally:
            server.shutdown()
            server.server_close()

    def test_demo_section_expected_project_reported(self):
        # Демо-раздел сайта: сейчас — CVStart, целевой — «Связь для близких».
        # Перевод демо-раздела — большая правка контента (шагающий разбор,
        # материалы, справка, README/COMPLIANCE в основном репо) — отдельный
        # шаг; здесь фиксируем, что чекер не теряет этот пробел (warning
        # с именем проекта), чтобы он не забылся при следующих прогонах.
        self.assertIn("title", self.data["demo"])
        if "Связь для близких" not in self.data["demo"]["title"]:
            self.assertTrue(self.data["demo"].get("pending", False),
                            "чекер должен помечать pending-проект демо")


if __name__ == "__main__":
    unittest.main()


class Pro133ContentGate(unittest.TestCase):
    """PRO-133: EN-страницы без кириллицы (вне whitelist: пути/цитаты), RU без «100/100»."""

    def _read(self, rel):
        p = SITE / rel
        self.assertTrue(p.exists(), f"{rel} не собран")
        return p.read_text(encoding="utf-8")

    def test_en_pages_no_cyrillic_outside_whitelist(self):
        import re
        wl = re.compile(r"projects/связь|lang=\"ru\"|<code|<!--")
        cyr = re.compile(r"[А-Яа-яЁё][А-Яа-яЁё ]{6,}")
        for rel in ("site/en/demo.html", "site/en/help.html",
                    "site/en/materials.html", "site/en/index.html"):
            frags = set()
            for line in self._read(rel).splitlines():
                if wl.search(line):
                    continue
                frags.update(m.group(0) for m in cyr.finditer(line))
            frags = {w for w in frags if len(w) >= 4 and w.lower() != "ru"}
            self.assertEqual(frags, set(), f"{rel}: кириллица на EN: {sorted(frags)[:5]}")

    def test_ru_pages_no_invented_score_or_stale_numbers(self):
        for rel in ("site/demo.html", "site/help.html", "site/materials.html", "site/index.html"):
            t = self._read(rel)
            self.assertNotIn("100/100", t, f"{rel}: выдуманная оценка 100/100")
            self.assertNotIn("18,444", t, f"{rel}: EN-формат числа на RU")
            self.assertNotIn("Три порога", t, f"{rel}: ложное утверждение полноты порогов")

    def test_demo_thresholds_honest(self):
        t = self._read("site/demo.html")
        self.assertIn("−3 п.п.", t, "порог −3 п.п. отсутствует")
        self.assertIn("12 000", t, "граница 12 000 мес отсутствует")
