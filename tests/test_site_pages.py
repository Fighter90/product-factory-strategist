"""PRO-61: подстраницы demo/help/materials собираются build_site.py в двух языках.

Красный список из issue PRO-61:
- сборка пишет 8 статических страниц: {index,demo,help,materials}.html × {ru,en};
- видимый текст EN-версии без кириллицы (белый список — пути демо-проекта: «демо»);
- видимый текст RU-версии без английских предложений длиннее 3 слов
  (кроме кода, команд и названий);
- числа демо (источники, утверждения, red team, экономика, даты D001)
  подставляются из projects/демо при сборке, а не набиты руками;
- без JS-переключателя языка: data-lang/onclick=setLang на подстраницах запрещены;
- закоммиченные страницы равны свежей сборке (все 8, не только index).
"""
from __future__ import annotations

import html as html_mod
import importlib.util
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
SUBPAGES = ("demo", "help", "materials")


def load_module():
    spec = importlib.util.spec_from_file_location("build_site_pages", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def visible_text(page: str) -> str:
    body = re.sub(r"<script\b.*?</script>", " ", page, flags=re.S)
    body = re.sub(r"<style\b.*?</style>", " ", body, flags=re.S)
    body = re.sub(r"<[^>]+>", " ", body)
    return html_mod.unescape(body)


def run_build(out: Path) -> None:
    r = subprocess.run([sys.executable, str(SCRIPT), "--out", str(out)],
                       cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, f"build_site.py упал: {r.stdout}\n{r.stderr}"


def base_url() -> str:
    m = re.search(r'hreflang="ru" href="(https://[^"]+?)/"', (ROOT / "site" / "index.html").read_text(encoding="utf-8"))
    assert m, "не нашли BASE в закоммиченном index.html"
    return m.group(1)


def d001() -> dict:
    for line in (ROOT / "projects" / "демо" / "decisions.jsonl").read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        if row.get("id") == "D001":
            return row
    raise AssertionError("D001 не найден")


def ltv_exact() -> tuple[str, str]:
    """Точный LTV из юнит-математики сборки (calcs.json демо-проекта)."""
    ut = load_module().unit_tokens()
    return ut["U_LTV_RU"], ut["U_LTV_EN"]


# ---------- сборка во временную директорию ----------

class SitePagesBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out = Path(tempfile.mkdtemp(prefix="pfs-site-pages-"))
        run_build(cls.out)
        cls.pages = {}
        for lang_dir, prefix in ((cls.out, ""), (cls.out / "en", "en:")):
            for name in ("index",) + SUBPAGES:
                path = lang_dir / f"{name}.html"
                cls.pages[f"{prefix}{name}"] = path.read_text(encoding="utf-8")


class TestEightPages(SitePagesBase):
    def test_all_eight_written(self):
        for key in ("index",) + SUBPAGES:
            for prefix in ("", "en:"):
                self.assertIn(f"{prefix}{key}", self.pages,
                              f"нет страницы {prefix}{key}.html — сборка должна писать "
                              f"«/» и «/en/» для всех страниц сайта")

    def test_lang_attrs(self):
        for key in ("index",) + SUBPAGES:
            self.assertIn('<html lang="ru">', self.pages[key], key)
            self.assertIn('<html lang="en">', self.pages[f"en:{key}"], f"en:{key}")


class TestNoLanguageLeaks(SitePagesBase):
    def test_en_pages_no_cyrillic_outside_demo_paths(self):
        for key in ("index",) + SUBPAGES:
            page = self.pages[f"en:{key}"]
            text = visible_text(page)
            for m in CYR.finditer(text):
                ctx = text[max(0, m.start() - 60):m.end() + 60].lower()
                self.assertIn("демо", ctx,
                              f"en:{key}: кириллица вне белого списка путей демо: …{ctx.strip()[:80]}…")

    def test_ru_pages_no_long_english_runs(self):
        # Названия продуктов и термины оставляем; длинные английские предложения — нет.
        brands = (
            "Product Factory Strategist", "hosted freemium SaaS",
            "mock-интервью", "six-pager", "SIX_PAGER",
        )
        run = re.compile(r"(?:[A-Za-z][A-Za-z'’&\-]+\s+){3,}[A-Za-z][A-Za-z'’&\-]+")
        for key in ("index",) + SUBPAGES:
            page = self.pages[key]
            body = re.sub(r"<script\b.*?</script>", " ", page, flags=re.S)
            body = re.sub(r"<style\b.*?</style>", " ", body, flags=re.S)
            body = re.sub(r"<code\b.*?</code>", " ", body, flags=re.S)
            body = re.sub(r"<pre\b.*?</pre>", " ", body, flags=re.S)
            text = html_mod.unescape(re.sub(r"<[^>]+>", " ", body))
            for brand in brands:
                text = text.replace(brand, " ")
            m = run.search(text)
            self.assertIsNone(m, f"{key}: английское предложение в RU-версии: «{m.group(0) if m else ''}»")


class TestDemoNumbersFromData(SitePagesBase):
    """Числа демо на сайте == данным projects/демо при сборке."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.mod = load_module()
        cls.num = cls.mod.demo_numbers()

    def test_chip_counts_match_registry(self):
        pairs = (
            (f"{self.num['D_SOURCES']} источников", "demo", "materials"),
            (f"{self.num['D_CLAIMS']} утверждений", "demo",),
            (f"{self.num['D_OPT_LAST']}", "demo",),
            (f"{self.num['D_HITS']} ударов red team", "demo",),
        )
        for needle, *keys in pairs:
            for key in keys:
                self.assertIn(needle, visible_text(self.pages[key]),
                              f"{key}: «{needle}» не на странице — число набито руками, "
                              f"а не подставлено из projects/демо")

    def test_ltv_formatted_per_language(self):
        ru, en = ltv_exact()
        self.assertIn(f"${ru}", visible_text(self.pages["demo"]),
                      f"demo: точный LTV из юнит-математики демо (${ru}) не на RU-странице")
        en_text = visible_text(self.pages["en:demo"])
        self.assertIn(f"${en}", en_text, f"en:demo: LTV с точкой (${en}) не на EN-странице")
        self.assertNotIn(f"${ru}", en_text, f"en:demo: русские запятые в числах EN-версии")
        # округление LTV на сайте синхронно документу демо-проекта
        opts = (ROOT / "projects" / "демо" / "outputs" / "03_options.md").read_text(encoding="utf-8")
        rounded = re.search(r"LTV ≈ \$(\d+)", opts).group(1)
        self.assertIn(str(int(float(en))), (rounded, str(int(float(en)) + 1)[:len(rounded)]),
                      "округление LTV из calcs.json расходится с 03_options.md")

    def test_d001_dates_on_demo_and_materials(self):
        review = d001()["review"]["date"]
        commitments = d001().get("commitments") or []
        dues = [re.search(r"\d{4}-\d{2}-\d{2}", c.get("due", "")).group(0)
                for c in commitments if re.search(r"\d{4}-\d{2}-\d{2}", c.get("due", ""))]
        for key in ("demo", "materials"):
            text = visible_text(self.pages[key])
            self.assertIn(review, text, f"{key}: дата пересмотра D001 ({review}) не на странице")
        demo_text = visible_text(self.pages["demo"])
        for due in dues:
            self.assertIn(due, demo_text, f"demo: срок обязательства D001 ({due}) не на странице")

    def test_help_meta_counts_from_repo(self):
        mod = load_module()
        repo = mod.repo_numbers()
        for key in ("help", "en:help"):
            text = visible_text(self.pages[key])
            self.assertIn(str(repo["N_SKILLS"]), text, f"{key}: число навыков не из репозитория")
            self.assertIn(str(repo["N_AGENTS"]), text, f"{key}: число субагентов не из репозитория")
            self.assertIn(str(repo["N_HOOKS"]), text, f"{key}: число хуков не из репозитория")
            self.assertIn(str(repo["N_MAPS"]), text, f"{key}: число карт знаний не из репозитория")


class TestStaticPagesNoJsToggle(SitePagesBase):
    def test_no_data_lang_toggle_on_subpages(self):
        for key in SUBPAGES:
            for prefix in ("", "en:"):
                page = self.pages[f"{prefix}{key}"]
                self.assertNotIn("setLang", page, f"{prefix}{key}: JS-переключатель языка")
                self.assertNotIn("data-lang", page, f"{prefix}{key}: CSS-переключатель body[data-lang]")
                self.assertNotIn("btn-ru", page, f"{prefix}{key}: кнопки RU/EN вместо ссылок")

    def test_lang_switcher_is_link(self):
        for key in SUBPAGES:
            self.assertIn(f'href="en/{key}.html"', self.pages[key],
                          f"{key}: RU-страница должна ссылаться на en/{key}.html")
            self.assertIn(f'href="../{key}.html"', self.pages[f"en:{key}"],
                          f"en:{key}: EN-страница должна ссылаться на ../{key}.html")


class TestSubpageSeo(SitePagesBase):
    def test_hreflang_pairs_on_subpages(self):
        base = base_url()
        for key in SUBPAGES:
            ru_page = self.pages[key]
            en_page = self.pages[f"en:{key}"]
            self.assertIn(f'hreflang="ru" href="{base}/{key}.html"', ru_page, key)
            self.assertIn(f'hreflang="en" href="{base}/en/{key}.html"', ru_page, key)
            self.assertIn(f'hreflang="en" href="{base}/en/{key}.html"', en_page, f"en:{key}")
            self.assertIn(f'hreflang="ru" href="{base}/{key}.html"', en_page, f"en:{key}")


class TestStepLabels(SitePagesBase):
    def test_steps_8_and_9_distinct_in_help(self):
        ru_text = visible_text(self.pages["help"])
        self.assertNotIn("9 · Проверка", ru_text, "help: шаг 9 назван «Проверка»")
        self.assertIn("8 · План проверки", ru_text, "help: у шага 8 нет метки «План проверки»")
        self.assertIn("9 · Ревью", ru_text, "help: у шага 9 нет метки «Ревью»")
        en_text = visible_text(self.pages["en:help"])
        self.assertIn("8 · Validation plan", en_text, "en:help: у шага 8 нет метки «Validation plan»")
        self.assertIn("9 · Review", en_text, "en:help: у шага 9 нет метки «Review»")


class TestCommittedAllPages(SitePagesBase):
    def test_committed_pages_match_build(self):
        for key in ("index",) + SUBPAGES:
            for prefix, rel in (("", Path(f"{key}.html")), ("en:", Path("en") / f"{key}.html")):
                committed_path = ROOT / "site" / rel
                if not committed_path.exists():
                    self.fail(f"site/{rel} не существует — запустите scripts/build_site.py и закоммитьте")
                committed = committed_path.read_text(encoding="utf-8")
                self.assertEqual(self.pages[f"{prefix}{key}"], committed,
                                 f"site/{rel} не совпадает со сборкой — перезапустите scripts/build_site.py")


if __name__ == "__main__":
    unittest.main()
