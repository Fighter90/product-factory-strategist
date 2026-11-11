"""PRO-66 (раунд ревью 3): страницы demo/help/materials в системе лендинга v3.

Замечание ревью: раздел структуры задачи требует demo/help/materials «в той же
системе» и dark-hero-paper обложкой страницы demo — откладывать их на будущую
задачу нельзя. Генератор создаёт шесть страниц (RU в корне, EN в /en/) в той же
тёплой тёмной системе, что `/` и `/en/`. Проверяются: генерация всех шести
страниц и соответствие закоммиченных файлов, языковая изоляция (ноль кириллицы
в EN-исходниках), парные переключатели языка, canonical и hreflang каждой пары,
обложка demo (dark-hero-paper webp+avif с размерами), дословный запрос
(терминал = проза = projects/демо/project.json, RU и EN), разрешимость
внутренних ссылок и отсутствие старого JS-переключателя setLang.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_site.py"
CYR = re.compile(r"[\u0400-\u04FF]")

SUBPAGES = {  # ключ → относительный путь RU/EN-варианта
    "ru_demo": Path("demo.html"), "en_demo": Path("en") / "demo.html",
    "ru_help": Path("help.html"), "en_help": Path("en") / "help.html",
    "ru_mat": Path("materials.html"), "en_mat": Path("en") / "materials.html",
}
PAIRS = (("ru_demo", "en_demo"), ("ru_help", "en_help"), ("ru_mat", "en_mat"))


def load_module():
    import importlib.util

    spec = importlib.util.spec_from_file_location("build_site_subpages", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def visible_text(page: str) -> str:
    body = re.sub(r"<script\b.*?</script>", " ", page, flags=re.S)
    body = re.sub(r"<style\b.*?</style>", " ", body, flags=re.S)
    body = re.sub(r"<[^>]+>", " ", body)
    import html as html_mod

    return html_mod.unescape(body)


class SubpagesBase(unittest.TestCase):
    built: dict[str, str] = {}

    @classmethod
    def setUpClass(cls) -> None:
        if cls.built:
            return
        tmp = Path(tempfile.mkdtemp(prefix="pfs-subpages-"))
        r = subprocess.run([sys.executable, str(SCRIPT), "--out", str(tmp)],
                           cwd=ROOT, capture_output=True, text=True)
        assert r.returncode == 0, f"сборка упала:\n{r.stdout}\n{r.stderr}"
        cls.built["ru"] = (tmp / "index.html").read_text(encoding="utf-8")
        cls.built["en"] = (tmp / "en" / "index.html").read_text(encoding="utf-8")
        for key, rel in SUBPAGES.items():
            cls.built[key] = (tmp / rel).read_text(encoding="utf-8")
        cls.tmp = tmp


class TestSubpagesGenerated(SubpagesBase):
    def test_six_pages_written(self):
        for key, rel in SUBPAGES.items():
            self.assertTrue((self.tmp / rel).exists(), f"не сгенерирован {rel}")

    def test_lang_attrs_and_canonical(self):
        expected = {"ru_demo": "demo.html", "en_demo": "en/demo.html",
                    "ru_help": "help.html", "en_help": "en/help.html",
                    "ru_mat": "materials.html", "en_mat": "en/materials.html"}
        for key, page in self.built.items():
            if key not in expected:
                continue
            lang = "ru" if key.startswith("ru") else "en"
            self.assertIn(f'<html lang="{lang}">', page, key)
            self.assertIn(f'<link rel="canonical" '
                          f'href="https://strategyproduct.ru/{expected[key]}">', page, key)

    def test_hreflang_pair_per_page(self):
        for ru_key, en_key in PAIRS:
            ru_rel = SUBPAGES[ru_key].as_posix()
            en_rel = SUBPAGES[en_key].as_posix()
            for key, page, own, other in (
                    (ru_key, self.built[ru_key], ru_rel, en_rel),
                    (en_key, self.built[en_key], en_rel, ru_rel)):
                self.assertIn(f'hreflang="{ "ru" if key.startswith("ru") else "en" }" '
                              f'href="https://strategyproduct.ru/{own}"', page, key)
                self.assertIn(f'hreflang="{"en" if key.startswith("ru") else "ru"}" '
                              f'href="https://strategyproduct.ru/{other}"', page, key)


class TestSubpagesLanguage(SubpagesBase):
    def test_en_subpages_have_no_cyrillic(self):
        for key, page in self.built.items():
            if not key.startswith("en_"):
                continue
            leaks = CYR.findall(page)
            self.assertEqual(leaks, [], f"кириллица в исходнике {key}: {''.join(leaks[:20])}")

    def test_ru_subpages_have_russian(self):
        for key, page in self.built.items():
            if not key.startswith("ru_"):
                continue
            self.assertTrue(CYR.search(visible_text(page)), f"{key}: нет русского текста")

    def test_lang_switch_pairs(self):
        for ru_key, en_key in PAIRS:
            ru_rel, en_rel = SUBPAGES[ru_key], SUBPAGES[en_key]
            self.assertIn(f'href="{en_rel.as_posix()}" hreflang="en" '
                          f'data-goal="lang_switch"', self.built[ru_key], ru_key)
            back = "../" + ru_rel.name
            self.assertIn(f'href="{back}" hreflang="ru" '
                          f'data-goal="lang_switch"', self.built[en_key], en_key)

    def test_old_setlang_switch_is_gone(self):
        for key, page in self.built.items():
            self.assertNotIn("setLang", page, key)
            self.assertNotIn("data-lang", page, key)
            self.assertNotIn("localStorage", page, key)


class TestSubpagesSystem(SubpagesBase):
    """Та же система, что у лендинга: палитра, шапка-пилюля, футер, skip-ссылка."""

    def test_no_leftover_tokens(self):
        for key, page in self.built.items():
            self.assertNotIn("{{", page, key)

    def test_warm_dark_palette_and_inter(self):
        for key, page in self.built.items():
            if key in ("ru", "en"):
                continue
            self.assertIn("--bg:#0B0A09", page, key)
            self.assertIn("--accent:#EE8A3C", page, key)
            self.assertIn("family=Inter:wght@400;500;600", page, key)

    def test_no_gradient_text_and_no_aurora(self):
        for key, page in self.built.items():
            if key in ("ru", "en"):
                continue
            self.assertNotIn("background-clip:text", page, key)
            self.assertNotIn("conic-gradient", page, key)

    def test_skip_link_and_main(self):
        for key, page in self.built.items():
            if key in ("ru", "en"):
                continue
            self.assertIn('class="skip" href="#main"', page, key)
            self.assertIn('<main id="main">', page, key)

    def test_nav_links_to_landing_and_siblings(self):
        for key, page in self.built.items():
            if key in ("ru", "en"):
                continue
            self.assertIn('href="index.html#how"', page, key)
            self.assertIn('href="index.html#install" data-goal="cta_install_click"', page, key)
            self.assertIn('href="demo.html"', page, key)
            self.assertIn('href="help.html"', page, key)
            self.assertIn('href="materials.html"', page, key)

    def test_footer_links_to_siblings_and_github(self):
        for key, page in self.built.items():
            if key in ("ru", "en"):
                continue
            self.assertIn("https://github.com/Fighter90/product-factory-strategist", page, key)


class TestDemoCover(SubpagesBase):
    """dark-hero-paper — обложка страницы demo: picture с avif/webp и размерами."""

    def test_cover_picture_with_dimensions(self):
        for key in ("ru_demo", "en_demo"):
            m = re.search(r"<picture>.*?</picture>", self.built[key], flags=re.S)
            self.assertIsNotNone(m, f"{key}: нет <picture> обложки")
            block = m.group(0)
            self.assertIn("assets/dark-hero-paper.avif", block, key)
            self.assertIn("assets/dark-hero-paper.webp", block, key)
            self.assertIn('width="1800"', block, key)
            self.assertIn('height="1012"', block, key)

    def test_cover_assets_shipped(self):
        for ext in (".webp", ".avif"):
            self.assertTrue((ROOT / "site" / "assets" / f"dark-hero-paper{ext}").exists(),
                            "assets/dark-hero-paper" + ext)

    def test_demo_og_points_to_language_pair(self):
        for key, lang in (("ru_demo", "ru"), ("en_demo", "en")):
            refs = set(re.findall(r'property="og:image" content="([^"]+)"', self.built[key]))
            self.assertEqual(refs, {f"https://strategyproduct.ru/assets/og/og-{lang}.jpg"}, key)


class TestVerbatimRequest(SubpagesBase):
    """Дословный запрос: терминал = проза = projects/демо/project.json."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.request = json.loads(
            (ROOT / "projects" / "демо" / "project.json").read_text(encoding="utf-8")
        )["question"].strip()

    @staticmethod
    def _terminal(page: str) -> str:
        m = re.search(r'pfs new "CVStart[^"]*" "([^"]+)"', page)
        assert m, "в терминале нет pfs new с дословным запросом"
        return m.group(1)

    @staticmethod
    def _prose_ru(page: str) -> str:
        m = re.search(r"дословно: «([^»]+)»", page)
        assert m, "в прозе секции демо нет дословного запроса"
        return m.group(1)

    @staticmethod
    def _prose_en(page: str) -> str:
        m = re.search(r"word for word: “([^”]+)”", page)
        assert m, "EN-проза секции демо без дословного запроса"
        return m.group(1)

    def test_ru_terminal_and_prose_equal_project_json(self):
        for key in ("ru", "ru_demo"):
            page = self.built[key]
            self.assertEqual(self._terminal(page), self.request, key)
            self.assertEqual(self._prose_ru(page), self.request, key)

    def test_en_terminal_and_prose_are_one_translation(self):
        en_term = self._terminal(self.built["en"])
        en_prose = self._prose_en(self.built["en"])
        self.assertEqual(en_term, en_prose, "EN: терминал и проза расходятся")
        self.assertNotIn("на весь мир", en_prose)

    def test_en_translation_numbers_match_repo_request(self):
        def nums(s: str) -> list[str]:
            return sorted(t.replace(",", ".") for t in re.findall(r"\d[\d,.]*", s))

        en = self._terminal(self.built["en"])
        self.assertEqual(nums(en), nums(self.request),
                         "числа EN-перевода дословного запроса расходятся с project.json")

    def test_unit_token_reader(self):
        mod = load_module()
        req = mod.demo_request()
        self.assertEqual(req["RQ_RU"], self.request)
        self.assertEqual(sorted(re.findall(r"\d[\d,.]*", req["RQ_EN"])),
                         sorted(re.findall(r"\d[\d,.]*", self.request)))


class TestDemoPageContent(SubpagesBase):
    """Числа страницы demo — из репозитория, решение D001 — из decisions.jsonl."""

    def test_market_fact_cards_with_sources(self):
        page = visible_text(self.built["ru_demo"])
        for tag in ("C005", "C006", "C008", "C009", "C011"):
            self.assertIn(tag, page, "страница demo без карточки факта " + tag)
        self.assertIn("S006 → C005", page)

    def test_market_fact_numbers_crosschecked_against_registry(self):
        mod = load_module()
        facts = mod.market_facts()
        claims = {}
        for line in (ROOT / "projects" / "демо" / "claims.jsonl").read_text(
                encoding="utf-8").splitlines():
            if line.strip():
                c = json.loads(line)
                claims[c["id"]] = c

        def nums(s):
            return {t.replace(",", ".") for t in re.findall(r"\d[\d,.]*", s)}

        for cid in {k.split("_")[0] for k in facts if k.startswith("MF")}:
            pass  # структура ключей проверяется ниже
        i = 0
        while f"MF{i}_VALUE" in facts:
            ru, en = facts[f"MF{i}_VALUE"], facts[f"MF{i}_VALUE_EN"]
            cid = facts[f"MF{i}_SRC"].split("→")[1].strip()
            allowed = nums(claims[cid]["text"])
            self.assertTrue(nums(ru) <= allowed, f"MF{i} RU {ru!r} нет в {cid}")
            self.assertTrue(nums(en) <= allowed, f"MF{i} EN {en!r} нет в {cid}")
            i += 1
        self.assertGreaterEqual(i, 5, "меньше пяти карточек фактов")

    def test_decision_d001_from_registry(self):
        mod = load_module()
        det = mod.decision_details()
        page = self.built["ru_demo"]
        self.assertIn(det["D_TITLE"], page)
        self.assertIn(det["D_GROUNDS"], page)
        self.assertIn(det["D_DUE_RU"], visible_text(page))
        en_page = self.built["en_demo"]
        self.assertIn(det["D_TITLE_EN"], en_page)
        self.assertIn(det["D_DUE_EN"], visible_text(en_page))

    def test_decision_en_translation_is_cyrillic_free(self):
        mod = load_module()
        det = mod.decision_details()
        for key in ("D_TITLE_EN", "D_METRIC_EN", "D_COMMIT_EN", "D_TRIGGER_EN"):
            self.assertFalse(CYR.search(det[key]), f"{key} содержит кириллицу")

    def test_stats_come_from_repo_tokens(self):
        # числа демо на странице должны совпадать с реестром (как на лендинге)
        claims = sum(1 for line in (ROOT / "projects" / "демо" / "claims.jsonl")
                     .read_text(encoding="utf-8").splitlines() if line.strip())
        for key in ("ru_demo", "en_demo"):
            self.assertIn(f"<b>{claims}</b>", self.built[key], key)


class TestInternalLinks(SubpagesBase):
    """Каждая внутренняя ссылка и картинка собранного сайта должна существовать."""

    SKIP = ("http://", "https://", "#", "data:", "mailto:")

    def _targets(self, page: str, base: Path) -> list[Path]:
        out = []
        for ref in re.findall(r'(?:href|src)="([^"]+)"', page):
            if ref.startswith(self.SKIP):
                continue
            path = ref.split("#", 1)[0]
            if not path:
                continue
            resolved = (base / path).resolve()
            if path.endswith("/"):
                resolved = (base / path / "index.html").resolve()
            out.append(resolved)
        return out

    def test_all_links_resolve(self):
        page_dirs = {"ru": self.tmp, "en": self.tmp / "en"}
        for key, rel in SUBPAGES.items():
            base = self.tmp / rel.parent
            page_dirs[key] = base
        for key, page in self.built.items():
            for target in self._targets(page, page_dirs[key]):
                self.assertTrue(target.exists(), f"{key}: битая ссылка → {target}")


class TestCommittedSubpages(SubpagesBase):
    def test_committed_subpages_match_build(self):
        for key, rel in SUBPAGES.items():
            committed = (ROOT / "site" / rel).read_text(encoding="utf-8")
            self.assertEqual(self.built[key], committed,
                             f"site/{rel} не совпадает со сборкой — "
                             f"перезапустите scripts/build_site.py")


if __name__ == "__main__":
    unittest.main()
