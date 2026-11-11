"""PRO-66: генератор лендинга scripts/build_site.py — RU и EN из данных репозитория.

Проверяются: генерация site/index.html и site/en/index.html, hreflang/OG, палитра v3
«тёплый тёмный» без градиентного текста, контраст WCAG AA, подстановка чисел из
репозитория (карты/навыки/тесты/демо-проект), отсутствие языковых утечек в EN,
цели Метрики, видимость без JS, постер и prefers-reduced-motion у видео.
"""
from __future__ import annotations

import html as html_mod
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


# ---------- независимый вывод чисел из репозитория ----------

def n_maps() -> int:
    return len(list((ROOT / "knowledge" / "methods").glob("*.md")))


def n_maps_en() -> int:
    return len(list((ROOT / "knowledge" / "methods_en").glob("*.md")))


def n_skills() -> int:
    return len(list((ROOT / ".claude" / "skills").glob("*/SKILL.md")))


def n_agents() -> int:
    return len(list((ROOT / ".claude" / "agents").glob("*.md")))


def n_hooks() -> int:
    return len(list((ROOT / ".claude" / "hooks").glob("*.py")))


def n_tests() -> int:
    """Число тестовых функций по AST — тот же способ, что в build_site._count_tests."""
    import ast

    total = 0
    for p in (ROOT / "tests").glob("test_*.py"):
        tree = ast.parse(p.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test"):
                total += 1
    return total


def _jsonl(path: Path) -> list[dict]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def demo_claims() -> dict:
    rows = _jsonl(ROOT / "projects" / "демо" / "claims.jsonl")
    kinds: dict[str, int] = {}
    for r in rows:
        kinds[r.get("kind", "?")] = kinds.get(r.get("kind", "?"), 0) + 1
    return {"total": len(rows), "facts": kinds.get("fact", 0), "rows": rows}


def demo_sources() -> int:
    return len(list((ROOT / "projects" / "демо" / "sources").glob("S*.md")))


def demo_options() -> list[str]:
    text = (ROOT / "projects" / "демо" / "outputs" / "03_options.md").read_text(encoding="utf-8")
    return re.findall(r"^## Вариант ([A-ZА-Я])\.", text, flags=re.M)


def demo_objections() -> int:
    text = (ROOT / "projects" / "демо" / "outputs" / "03_options.md").read_text(encoding="utf-8")
    total = 0
    for line in text.splitlines():
        if line.lstrip("- ").startswith("Возражения red team"):
            nums = [int(x) for x in re.findall(r"\((\d)\)", line)]
            total += max(nums) if nums else 0
    return total


def demo_assumptions() -> int:
    text = (ROOT / "projects" / "демо" / "outputs" / "03_options.md").read_text(encoding="utf-8")
    return sum(1 for line in text.splitlines() if "Скрытое допущение" in line)


def d001() -> dict:
    for r in _jsonl(ROOT / "projects" / "демо" / "decisions.jsonl"):
        if r.get("id") == "D001":
            m = re.search(r"вариант ([A-ZА-Я])\b", r.get("decision", ""))
            return {"letter": m.group(1) if m else "", "review": r["review"]["date"]}
    raise AssertionError("D001 не найден")


def chain_claim(cid: str = "C011") -> dict:
    for r in demo_claims()["rows"]:
        if r.get("id") == cid:
            return r
    raise AssertionError(f"{cid} не найден")


def chain_source(sid: str) -> dict:
    for r in _jsonl(ROOT / "projects" / "демо" / "sources.jsonl"):
        if r.get("id") == sid:
            return r
    raise AssertionError(f"{sid} не найден")


def chain_usage(faq_file: str) -> str:
    """Метка ближайшего '## FAQ-…' над строкой с C011 в six-pager."""
    text = (ROOT / "projects" / "демо" / "outputs" / faq_file).read_text(encoding="utf-8")
    label = ""
    for line in text.splitlines():
        if "C011" in line and label:
            return label
        m = re.match(r"^## (FAQ-\d+)\.?\s*(.*)$", line)
        if m:
            title = m.group(2).split(".")[0].split(":")[0].strip()
            label = f"{m.group(1)} · {title}"
    raise AssertionError("C011 не найден в " + faq_file)


def _lum(hexcolor: str) -> float:
    r, g, b = (int(hexcolor[i:i + 2], 16) / 255 for i in (1, 3, 5))

    def lin(c: float) -> float:
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def _ratio(fg: str, bg: str) -> float:
    l1, l2 = _lum(fg), _lum(bg)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def _strip_css_comments(css: str) -> str:
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def _css_vars(page: str) -> dict:
    css = _strip_css_comments(page)
    return {m.group(1): m.group(2) for m in re.finditer(r"--([a-z0-9-]+):(?P<v>#[0-9A-Fa-f]{6})", css)}


def _visible_text(page: str) -> str:
    body = re.sub(r"<script\b.*?</script>", " ", page, flags=re.S)
    body = re.sub(r"<style\b.*?</style>", " ", body, flags=re.S)
    body = re.sub(r"<[^>]+>", " ", body)
    return html_mod.unescape(body)


# ---------- сборка ----------

class SiteBuildBase(unittest.TestCase):
    built: dict[str, str] = {}

    @classmethod
    def setUpClass(cls) -> None:
        tmp = Path(tempfile.mkdtemp(prefix="pfs-site-build-"))
        r = subprocess.run([sys.executable, str(SCRIPT), "--out", str(tmp)],
                           cwd=ROOT, capture_output=True, text=True)
        assert r.returncode == 0, f"build_site.py упал:\n{r.stdout}\n{r.stderr}"
        cls.built["ru"] = (tmp / "index.html").read_text(encoding="utf-8")
        cls.built["en"] = (tmp / "en" / "index.html").read_text(encoding="utf-8")
        for key, rel in (("ru_demo", Path("demo.html")), (Path("en").name + "_demo", Path("en") / "demo.html"),
                         ("ru_help", Path("help.html")), ("en_help", Path("en") / "help.html"),
                         ("ru_mat", Path("materials.html")), ("en_mat", Path("en") / "materials.html")):
            cls.built[key] = (tmp / rel).read_text(encoding="utf-8")
        cls.tmp = tmp


class TestGeneration(SiteBuildBase):
    def test_pages_generated(self):
        self.assertTrue((self.tmp / "index.html").exists(), "нет RU-страницы")
        self.assertTrue((self.tmp / "en" / "index.html").exists(), "нет EN-страницы")
        self.assertIn("<!doctype html>", self.built["ru"].lower())

    def test_lang_and_canonical(self):
        self.assertIn('<html lang="ru">', self.built["ru"])
        self.assertIn('<html lang="en">', self.built["en"])
        self.assertIn('<link rel="canonical" href="https://strategyproduct.ru/">', self.built["ru"])
        self.assertIn('<link rel="canonical" href="https://strategyproduct.ru/en/">', self.built["en"])

    def test_hreflang_pair_and_xdefault(self):
        for lang, page in (("ru", self.built["ru"]), ("en", self.built["en"])):
            self.assertIn('hreflang="ru" href="https://strategyproduct.ru/"', page, lang)
            self.assertIn('hreflang="en" href="https://strategyproduct.ru/en/"', page, lang)
            self.assertIn('hreflang="x-default" href="https://strategyproduct.ru/"', page, lang)

    def test_og_per_language(self):
        # ТЗ PRO-66: OG-картинки по языкам, каждая — своё фото и размеры
        for lang, page in (("ru", self.built["ru"]), ("en", self.built["en"])):
            self.assertIn(f'property="og:image" content="https://strategyproduct.ru/assets/og/og-{lang}.jpg"',
                          page, lang)
            self.assertIn('property="og:title"', page, lang)
            self.assertIn('property="og:image:width" content="1800"', page, lang)
            self.assertIn('property="og:image:height" content="1012"', page, lang)
            self.assertIn('name="twitter:card" content="summary_large_image"', page, lang)

    def test_structure_sections(self):
        for sec in ("how", "features", "process", "proof", "demo", "arch", "install", "faq"):
            self.assertIn(f'id="{sec}"', self.built["ru"], sec)
            self.assertIn(f'id="{sec}"', self.built["en"], sec)

    def test_inter_font_only(self):
        for lang, page in self.built.items():
            self.assertIn("family=Inter:wght@400;500;600", page, lang)


class TestDesignRules(SiteBuildBase):
    def test_no_gradient_text(self):
        for lang, page in self.built.items():
            self.assertNotIn("background-clip", page, lang)
            self.assertNotIn("background-clip:text", page, lang)

    def test_warm_dark_palette(self):
        for lang, page in self.built.items():
            self.assertIn("--bg:#0B0A09", page, lang)
            self.assertIn("--accent:#EE8A3C", page, lang)
            for bad in ("#2dd4bf", "#818cf8", "#f472b6"):
                self.assertNotIn(bad, page.lower(), f"{lang}: старый цвет {bad}")

    def test_contrast_aa(self):
        v = _css_vars(self.built["ru"])
        self.assertGreaterEqual(_ratio(v["muted"], v["bg"]), 4.5, "вторичный на фоне")
        self.assertGreaterEqual(_ratio(v["muted"], v["card"]), 4.5, "вторичный на карточке")
        self.assertGreaterEqual(_ratio(v["accent-ink"], v["accent"]), 4.5, "текст на акцентной кнопке")
        self.assertGreaterEqual(_ratio(v["text"], v["bg"]), 4.5, "основной текст на фоне")
        self.assertGreaterEqual(_ratio("#0A0908", v["pill"]), 4.5, "текст на pill-кнопке")

    def test_reduced_motion_and_video(self):
        for lang, page in self.built.items():
            self.assertIn("@media (prefers-reduced-motion:reduce)", page, lang)
            m = re.search(r"<video\b[^>]*>", page)
            self.assertIsNotNone(m, lang)
            tag = m.group(0)
            self.assertIn("poster=", tag, lang)
            self.assertIn(".webp", tag, lang)
            self.assertIn('preload="metadata"', tag, lang)
            self.assertIn("muted", tag, lang)
            self.assertIn("playsinline", tag, lang)
        self.assertIn("video{display:none}", self.built["ru"].replace(" ", ""))

    def test_tap_targets_44(self):
        for lang, page in self.built.items():
            self.assertGreaterEqual(page.count("min-height:44px"), 3, lang)

    def test_skip_link_and_focus(self):
        for lang, page in self.built.items():
            self.assertIn('class="skip" href="#main"', page, lang)
            self.assertIn(":focus-visible{outline:2pxsolidvar(--accent)", page.replace(" ", ""), lang)

    def test_bento_variety(self):
        for lang, page in self.built.items():
            n_cards = len(re.findall(r'<article class="card', page))
            self.assertGreaterEqual(n_cards, 6, lang)
            self.assertIn('class="card w8"', page, lang)
            self.assertIn('class="card w6"', page, lang)

    def test_no_js_numbers_and_faq(self):
        for lang, page in self.built.items():
            self.assertNotIn("data-target", page, lang)
            self.assertIn("<details>", page, lang)


class TestRepoNumbers(SiteBuildBase):
    def test_hero_maps_count(self):
        ru, en = self.built["ru"], self.built["en"]
        self.assertIn(f"<b>{n_maps()}</b> методических карт", ru)
        self.assertIn(f"<b>{n_maps()}</b> method cards", en)

    def test_architecture_layers_counts(self):
        ru, en = self.built["ru"], self.built["en"]
        self.assertIn(f"навыков: {n_skills()}", ru)
        self.assertIn(f"субагентов: {n_agents()}", ru)
        self.assertIn(f"хуков: {n_hooks()}", ru)
        self.assertIn(f"({n_tests()})", ru)
        self.assertIn(f"skills: {n_skills()}", en)
        self.assertIn(f"subagents: {n_agents()}", en)
        self.assertIn(f"hooks: {n_hooks()}", en)
        self.assertIn(f"({n_tests()})", en)
        self.assertIn(f"{n_maps_en()}", ru)
        self.assertIn(f"{n_maps_en()}", en)

    def test_demo_stats_from_repo(self):
        claims, src = demo_claims(), demo_sources()
        ru, en = self.built["ru"], self.built["en"]
        self.assertIn(f"<b>{src}</b>", ru)
        self.assertIn(f"<b>{claims['total']}</b>", ru)
        self.assertIn(f"из них факты — {claims['facts']}", ru)
        self.assertIn(f"<b>{src}</b>", en)
        self.assertIn(f"<b>{claims['total']}</b>", en)
        self.assertIn(f"of them facts — {claims['facts']}", en)

    def test_options_and_redteam_counts(self):
        letters, obj, asm = demo_options(), demo_objections(), demo_assumptions()
        ru = self.built["ru"]
        self.assertIn("вариантов A–" + letters[-1], ru)
        self.assertIn(f"<b>{obj} + {asm}</b>", ru)
        en = self.built["en"]
        self.assertIn(f"<b>{obj} + {asm}</b>", en)

    def test_decision_tile(self):
        d = d001()
        ru, en = self.built["ru"], self.built["en"]
        self.assertIn(f"<b>{d['letter']}</b>", ru)
        rev = d["review"]  # ISO
        y, m, day = rev.split("-")
        self.assertIn(f"<b>{day}.{m}.{y[2:]}</b>", ru)   # 10.02.27
        self.assertIn(f"<b>{rev}</b>", en)                # 2027-02-10

    def test_evidence_chain_real(self):
        c = chain_claim("C011")
        src = chain_source(c["sources"][0])
        dom = re.sub(r"^https?://(www\.)?", "", src["url"] or "").split("/")[0]
        ru, en = self.built["ru"], self.built["en"]
        # реальное утверждение с его источником
        self.assertIn("C011", ru)
        self.assertIn(c["sources"][0], ru)
        self.assertIn(dom, ru)
        self.assertNotIn("Bitkom", ru, "выдуманного источника быть не должно")
        self.assertIn(c["sources"][0], en)
        self.assertIn(dom, en)
        self.assertNotIn("Bitkom", en)
        # текст реального утверждения на RU-странице
        self.assertIn(c["text"][:40], ru)
        # использование в six-pager вычисляется из обоих документов
        self.assertIn(chain_usage("SIX_PAGER.md").split(" · ")[0], ru)
        self.assertIn(chain_usage("SIX_PAGER_EN.md").split(" · ")[0], en)

    def test_no_placeholder_tokens(self):
        for lang, page in self.built.items():
            self.assertNotIn("{{", page, lang)


class TestLanguage(SiteBuildBase):
    def test_no_cyrillic_leaks_in_en(self):
        text = _visible_text(self.built["en"])
        leaks = CYR.findall(text)
        self.assertEqual(leaks, [], f"кириллица в EN-версии: {''.join(leaks[:20])}")

    def test_ru_page_has_russian(self):
        self.assertGreater(len(CYR.findall(_visible_text(self.built["ru"]))), 100)


class TestAnalytics(SiteBuildBase):
    GOALS = ("cta_install_click", "cta_demo_click", "github_click", "lang_switch",
             "copy_command", "faq_open")

    def test_goals_marked(self):
        for lang, page in self.built.items():
            for goal in self.GOALS:
                self.assertIn(goal, page, f"{lang}: {goal}")
        # переключатель языка помечен целью
        for lang, page in self.built.items():
            self.assertIn('data-goal="lang_switch"', page, lang)

    def test_copy_buttons(self):
        for lang, page in self.built.items():
            self.assertIn('class="copy"', page, lang)
            self.assertGreaterEqual(page.count("data-copy="), 4, lang)

    def test_ym_loader_optional(self):
        for lang, page in self.built.items():
            self.assertNotIn("mc.yandex.ru", page, "без --ym-id счётчика быть не должно")
        tmp2 = Path(tempfile.mkdtemp(prefix="pfs-site-ym-"))
        r = subprocess.run([sys.executable, str(SCRIPT), "--out", str(tmp2), "--ym-id", "41813321"],
                           cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        ru = (tmp2 / "index.html").read_text(encoding="utf-8")
        self.assertIn("ym(41813321", ru)
        self.assertIn("window.YM_ID=41813321", ru)
        self.assertIn("mc.yandex.ru/metrika/tag.js", ru)


class TestCommittedOutput(SiteBuildBase):
    PAGES = {  # ключ → относительный путь закоммиченной страницы
        "ru": Path("index.html"), "en": Path("en") / "index.html",
        "ru_demo": Path("demo.html"), "en_demo": Path("en") / "demo.html",
        "ru_help": Path("help.html"), "en_help": Path("en") / "help.html",
        "ru_mat": Path("materials.html"), "en_mat": Path("en") / "materials.html",
    }

    def test_committed_pages_match_build(self):
        for key, rel in self.PAGES.items():
            committed = (ROOT / "site" / rel).read_text(encoding="utf-8")
            self.assertEqual(self.built[key], committed,
                             f"site/{rel} не совпадает со сборкой — перезапустите scripts/build_site.py")

    def test_referenced_assets_exist(self):
        for rel in ("assets/logo.svg", "assets/hero-poster.webp",
                    "assets/og/og-ru.jpg", "assets/og/og-en.jpg",
                    "assets/dark-double-diamond.webp",
                    "assets/dark-double-diamond.avif", "assets/dossier-dark.webp",
                    "assets/dossier-dark.avif", "assets/dark-hero-paper.webp",
                    "assets/dark-hero-paper.avif"):
            self.assertTrue((ROOT / "site" / rel).exists(), rel)
        self.assertTrue((ROOT / "site" / "assets" / "hero-swarm-2.mp4").exists())


# ---------- раунд 2 (ревью PRO-66): favicon, бейдж «вы», громкие числа демо ----------

def _load_build_module():
    """Импорт scripts/build_site.py как модуля — для юнит-тестов demo_numbers/claim_facts."""
    import importlib.util

    spec = importlib.util.spec_from_file_location("build_site_under_test", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def write_unit_economics_xlsx(path: Path, values: list[str]) -> None:
    """Минимальный xlsx: worksheets с <v>-значениями — достаточно для сверки excel_numbers()."""
    import zipfile

    with zipfile.ZipFile(path, "w") as z:
        cells = "".join(f'<c r="B{i}"><v>{v}</v></c>' for i, v in enumerate(values, 2))
        z.writestr("xl/worksheets/sheet1.xml",
                   f"<worksheet><sheetData>{cells}</sheetData></worksheet>")


# значения книги соответствуют экономике из OPT_RU_LABEL: «$272» ↔ 271.88 в книге
XLSX_OK = ["29", "0.25", "21.75", "271.88", "4.53"]


def _fixture_demo(tmp: Path, *, options_md: str, claims: list[dict],
                  letter: str = "A") -> Path:
    """Мини-проект демо с той же структурой, что projects/демо, в tmp-каталоге.

    letter — выбранный в D001 вариант; должен существовать среди заголовков 03_options.md.
    """
    demo = tmp / "demo"
    (demo / "outputs").mkdir(parents=True)
    (demo / "sources").mkdir()
    (demo / "claims.jsonl").write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in claims) + "\n", encoding="utf-8")
    (demo / "sources.jsonl").write_text(
        json.dumps({"id": "S001", "url": "https://example.com/a", "retrieved": "2026-01-15"},
                   ensure_ascii=False) + "\n", encoding="utf-8")
    (demo / "decisions.jsonl").write_text(
        json.dumps({"id": "D001", "decision": f"Запустить вариант {letter}: hosted freemium SaaS",
                    "review": {"date": "2027-02-10"}}, ensure_ascii=False) + "\n", encoding="utf-8")
    (demo / "outputs" / "03_options.md").write_text(options_md, encoding="utf-8")
    for name in ("SIX_PAGER.md", "SIX_PAGER_EN.md"):
        (demo / "outputs" / name).write_text("## FAQ-1. Market\nMention of [C011] here.\n",
                                             encoding="utf-8")
    att = demo / "outputs" / "attachments"
    att.mkdir(parents=True, exist_ok=True)
    write_unit_economics_xlsx(att / "unit_economics.xlsx", XLSX_OK)
    return demo


OPT_OK = ("## Вариант A. Оставить как есть — бесплатный OSS\n"
          "- Возражения red team: (1) первое возражение; (2) второе; (3) третье\n"
          "- Скрытое допущение: что-то предполагается\n"
          "## Сравнение по оси ARR\n"
          "- Проза: здесь видно Скрытое допущение варианта B — но это не строка опции.\n")


# ---------- раунд ревью: юнит-тесты excel_numbers/_sixpager_usage/render ----------

OPT_XL = ("## Вариант B. Hosted freemium SaaS\n"
          "- Экономика: paid $29/мес; переменные 25% → CM $21,75; "
          "LTV ≈ $272; LTV/CAC ≈ 4,5\n")


class TestExcelNumbers(unittest.TestCase):
    """Юнит-тесты excel_numbers: извлечение экономики варианта, громкий отказ."""

    def setUp(self):
        self.mod = _load_build_module()

    def _demo(self, md: str) -> None:
        tmp = Path(tempfile.mkdtemp(prefix="pfs-excel-"))
        demo = tmp / "demo"
        (demo / "outputs" / "attachments").mkdir(parents=True)
        (demo / "outputs" / "03_options.md").write_text(md, encoding="utf-8")
        write_unit_economics_xlsx(demo / "outputs" / "attachments" / "unit_economics.xlsx",
                                  XLSX_OK)
        self.mod.DEMO = demo

    def test_extracts_unit_economics(self):
        self._demo(OPT_XL)
        self.assertEqual(self.mod.excel_numbers(),
                         {"XL_PRICE": "29", "XL_CM": "21,75",
                          "XL_LTV": "272", "XL_RATIO": "4,5"})

    def test_missing_price_is_loud(self):
        self._demo("## Вариант B. Hosted freemium SaaS\n"
                   "- CM $21,75; LTV ≈ $272; LTV/CAC ≈ 4,5\n")
        with self.assertRaisesRegex(self.mod.BuildError, "цена Pro"):
            self.mod.excel_numbers()

    def test_missing_cm_is_loud(self):
        self._demo("## Вариант B. Hosted freemium SaaS\n"
                   "- paid $29/мес; LTV ≈ $272; LTV/CAC ≈ 4,5\n")
        with self.assertRaisesRegex(self.mod.BuildError, "вклад на покрытие"):
            self.mod.excel_numbers()

    def test_missing_ltv_ratio_is_loud(self):
        self._demo("## Вариант B. Hosted freemium SaaS\n- paid $29/мес; CM $21,75\n")
        with self.assertRaisesRegex(self.mod.BuildError, "LTV"):
            self.mod.excel_numbers()


class TestSixpagerUsage(unittest.TestCase):
    """Юнит-тесты _sixpager_usage: ближайший FAQ-заголовок над упоминанием C011."""

    def setUp(self):
        self.mod = _load_build_module()

    def _page(self, md: str) -> Path:
        tmp = Path(tempfile.mkdtemp(prefix="pfs-usage-"))
        p = tmp / "SIX_PAGER.md"
        p.write_text(md, encoding="utf-8")
        return p

    def test_nearest_header_wins(self):
        p = self._page("## FAQ-1. Рынок\nтекст\n## FAQ-5. План реализации\nупоминание [C011]\n")
        self.assertEqual(self.mod._sixpager_usage(p), "FAQ-5 · План реализации")

    def test_title_cut_on_colon(self):
        p = self._page("## FAQ-2. Юнит-экономика: сходится\n[C011] в тексте\n")
        self.assertEqual(self.mod._sixpager_usage(p), "FAQ-2 · Юнит-экономика")

    def test_no_faq_header_is_loud(self):
        p = self._page("Проза без заголовков, [C011]\n")
        with self.assertRaisesRegex(self.mod.BuildError, "FAQ"):
            self.mod._sixpager_usage(p)

    def test_mention_without_header_above_is_loud(self):
        p = self._page("[C011] до заголовка\n## FAQ-1. Рынок\n")
        with self.assertRaisesRegex(self.mod.BuildError, "не найден под заголовком FAQ"):
            self.mod._sixpager_usage(p)


class TestRenderEscaping(unittest.TestCase):
    """render(): динамические подстановки экранируются html.escape;
    без экранирования — только служебные сырые ключи (CSS/JS/YM/BRAND)."""

    def setUp(self):
        self.mod = _load_build_module()

    def test_dynamic_tokens_escaped(self):
        out = self.mod.render(
            "a{{TEXT}}b{{SEG}}c{{C_DOM}}d{{D_LABEL}}e{{USAGE}}f{{REVIEW}}g{{KIND}}",
            {"TEXT": "<b>&\"x", "SEG": "<i>", "C_DOM": "<script>alert(1)</script>",
             "D_LABEL": "a&b", "USAGE": "FAQ-5 · План", "REVIEW": "10.02.27",
             "KIND": "факт"})
        self.assertNotIn("<b>", out)
        self.assertNotIn("<i>", out)
        self.assertNotIn("<script>", out)
        self.assertIn("&lt;b&gt;&amp;&quot;x", out)
        self.assertIn("&lt;i&gt;", out)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", out)
        self.assertIn("a&amp;b", out)
        # простой текст без спецсимволов проходит без изменений
        self.assertIn("FAQ-5 · План", out)
        self.assertIn("10.02.27", out)
        self.assertIn("факт", out)

    def test_raw_keys_pass_through(self):
        raw = {"CSS": "<style>a{b:c}</style>", "JS": "<script>1<2</script>",
               "YM": "<noscript><img></noscript>", "BRAND": "<svg></svg>"}
        out = self.mod.render("{{CSS}}{{JS}}{{YM}}{{BRAND}}", dict(raw))
        self.assertEqual(out, raw["CSS"] + raw["JS"] + raw["YM"] + raw["BRAND"])


# ---------- раунд ревью: мобильное меню, один OG-файл, тёмные ассеты ----------

class TestMobileMenu(SiteBuildBase):
    """≤980px .links скрыты — нужна доступная с клавиатуры замена (details/summary)."""

    def test_details_menu_with_links(self):
        for lang, page in self.built.items():
            m = re.search(r'<details class="mlink">.*?</details>', page, flags=re.S)
            self.assertIsNotNone(m, f"{lang}: нет мобильного меню")
            block = m.group(0)
            self.assertIn("<summary", block, lang)
            for anchor in ("#how", "#features", "#demo", "#install", "#faq"):
                self.assertIn(f'href="{anchor}"', block, f"{lang}: {anchor}")

    def test_menu_labelled_per_language(self):
        self.assertIn('aria-label="Меню разделов"', self.built["ru"])
        self.assertIn('aria-label="Sections menu"', self.built["en"])

    def test_menu_hidden_on_desktop_shown_on_mobile(self):
        for lang, page in self.built.items():
            css = _strip_css_comments(page)
            self.assertRegex(css, r"\.mlink\{display:none", lang)
            mobile = css.split("@media (max-width:980px){")[1].split("@media")[0]
            self.assertIn(".links{display:none}", mobile, lang)
            self.assertRegex(mobile, r"\.mlink\{display:(block|inline-block)", lang)


class TestOgPerLanguage(SiteBuildBase):
    """ТЗ PRO-66: OG-картинки по языкам. og-ru и og-en — разные фото, не байтовые дубли.

    Раунд ревью 2: один общий og.jpg заменён на пару по языкам (замечание ревью):
    og-ru — фото-частицы из hero (dark-hero-paper), og-en — стопка документов из
    финального CTA (dossier-dark). Текста на фото нет, язык карточки даёт og:title.
    """

    def test_pages_point_to_own_og(self):
        for lang, page in self.built.items():
            refs = set(re.findall(r'property="og:image" content="([^"]+)"', page))
            self.assertEqual(refs, {f"https://strategyproduct.ru/assets/og/og-{lang}.jpg"}, lang)

    def test_og_files_exist_are_jpeg_and_differ(self):
        og_dir = ROOT / "site" / "assets" / "og"
        blobs = {}
        for lang in ("ru", "en"):
            p = og_dir / f"og-{lang}.jpg"
            self.assertTrue(p.exists(), f"нет {p.name}")
            blobs[lang] = p.read_bytes()
            self.assertEqual(blobs[lang][:3], b"\xff\xd8\xff", f"{p.name} — не JPEG")
        self.assertNotEqual(blobs["ru"], blobs["en"],
                            "og-ru и og-en — одинаковые файлы, дубликат не нужен")

    def test_no_shared_og_left(self):
        self.assertFalse((ROOT / "site" / "assets" / "og" / "og.jpg").exists(),
                         "общий og.jpg заменён парой og-ru/og-en")


class TestDarkAssetsUsed(SiteBuildBase):
    """Тёмные фото подключены к генерируемым страницам: picture, avif/webp, размеры.

    Раунд ревью 3: dark-hero-paper — обложка страницы demo (замечание ревью:
    откладывать страницы demo/help/materials было нельзя), остальные — на лендинге.
    """

    PAIRS = {"dark-double-diamond": (1800, 1350), "dossier-dark": (1800, 1012)}
    DEMO_COVER = ("dark-hero-paper", 1800, 1012)

    def test_shipped(self):
        for name in self.PAIRS:
            for ext in (".webp", ".avif"):
                self.assertTrue((ROOT / "site" / "assets" / f"{name}{ext}").exists(),
                                name + ext)

    def test_referenced_with_dimensions(self):
        for lang, page in self.built.items():
            for name, (w, h) in self.PAIRS.items():
                m = re.search(rf"<picture>.*?{name}.*?</picture>", page, flags=re.S)
                self.assertIsNotNone(m, f"{lang}: {name} не подключён")
                block = m.group(0)
                self.assertIn(f"{name}.avif", block, lang)
                self.assertIn(f"{name}.webp", block, lang)
                self.assertIn(f'width="{w}"', block, lang)
                self.assertIn(f'height="{h}"', block, lang)

    def test_demo_cover_referenced_with_dimensions(self):
        for key in ("ru_demo", "en_demo"):
            page = self.built[key]
            name, w, h = self.DEMO_COVER
            m = re.search(rf"<picture>.*?{name}.*?</picture>", page, flags=re.S)
            self.assertIsNotNone(m, f"{key}: {name} не подключён")
            block = m.group(0)
            self.assertIn(f"{name}.avif", block, key)
            self.assertIn(f"{name}.webp", block, key)
            self.assertIn(f'width="{w}"', block, key)
            self.assertIn(f'height="{h}"', block, key)

    def test_no_dead_dark_assets(self):
        for p in sorted((ROOT / "site" / "assets").glob("dark-*.webp")):
            used = [key for key, page in self.built.items() if p.stem in page]
            self.assertTrue(used, f"{p.name} лежит без использования")


class TestCommittedEnNoCyrillic(unittest.TestCase):
    """Критерий PRO-61/PRO-66: в закоммиченном site/en/index.html — ноль кириллицы."""

    def test_zero_cyrillic_in_committed_en(self):
        page = (ROOT / "site" / "en" / "index.html").read_text(encoding="utf-8")
        leaks = CYR.findall(_visible_text(page))
        self.assertEqual(leaks, [], f"кириллица в закоммиченной EN-странице: {''.join(leaks[:20])}")


class TestRound2Pages(SiteBuildBase):
    """Замечания ревью к страницам: favicon на /en/ и бейдж «вы» на процессе."""

    def test_favicon_asset_prefix(self):
        self.assertIn('<link rel="icon" href="assets/logo.svg"', self.built["ru"])
        self.assertIn('<link rel="icon" href="../assets/logo.svg"', self.built["en"])

    def test_favicon_resolves_from_page_dir(self):
        for lang, page_dir in (("ru", "site"), ("en", "site/en")):
            m = re.search(r'<link rel="icon" href="([^"]+)"', self.built[lang])
            self.assertIsNotNone(m, lang)
            self.assertTrue((ROOT / page_dir / m.group(1)).exists(),
                            f"{lang}: favicon {m.group(1)} не существует от {page_dir}")

    def test_process_badge_per_language(self):
        ru_flat = self.built["ru"].replace(" ", "")
        en_flat = self.built["en"].replace(" ", "")
        self.assertIn('content:"вы"', ru_flat, "RU: бейдж «вы» у шагов 1/7/11")
        self.assertIn('content:"you"', en_flat, "EN: бейдж «you» у шагов 1/7/11")
        # кириллица не должна попасть в отрисовываемый CSS EN-страницы
        # (комментарии не рендерятся — проверяем CSS без них)
        style_en = re.search(r"<style>(.*?)</style>", self.built["en"], flags=re.S)
        self.assertIsNotNone(style_en)
        self.assertEqual(CYR.findall(_strip_css_comments(style_en.group(1))), [],
                         "кириллица в отрисовываемом CSS EN-страницы")


class TestRound2DemoNumbers(unittest.TestCase):
    """Числа демо считаются громко: расхождение = BuildError, не тихий ноль."""

    def setUp(self):
        self.mod = _load_build_module()

    def _demo(self, options_md: str, claims: list[dict] | None = None,
              letter: str = "A") -> None:
        import tempfile
        tmp = Path(tempfile.mkdtemp(prefix="pfs-demo-numbers-"))
        self.mod.DEMO = _fixture_demo(tmp, options_md=options_md, letter=letter,
                                      claims=claims or [{"id": "C001", "kind": "fact",
                                                         "grade": "B", "text": "т",
                                                         "sources": ["S001"]}])

    def test_two_digit_objections_counted(self):
        self._demo(OPT_OK.replace("(1) первое возражение; (2) второе; (3) третье",
                                  "(10) десятое; (11) одиннадцатое; (12) двенадцатое"))
        nums = self.mod.demo_numbers()
        self.assertEqual(nums["D_OBJ"], 12, "двузначные «(10)…(12)» должны считаться, не тихий 0")
        self.assertEqual(nums["D_ASM"], 1, "упоминание «Скрытое допущение» в прозе не считается")

    def test_missing_red_team_line_is_loud(self):
        self._demo("## Вариант A. Закрыть проект\n- Скрытое допущение: что-то\n")
        with self.assertRaisesRegex(self.mod.BuildError, "Возражения red team"):
            self.mod.demo_numbers()

    def test_red_team_without_numbered_items_is_loud(self):
        self._demo("## Вариант B. Hosted freemium SaaS\n"
                   "- Возражения red team: возражения перечислены без нумерации\n"
                   "- Скрытое допущение: что-то\n", letter="B")
        with self.assertRaisesRegex(self.mod.BuildError, "нумерованных"):
            self.mod.demo_numbers()

    def test_missing_assumption_line_is_loud(self):
        self._demo("## Вариант A. Оставить как есть\n"
                   "- Возражения red team: (1) а; (2) б; (3) в\n")
        with self.assertRaisesRegex(self.mod.BuildError, "Скрытое допущени"):
            self.mod.demo_numbers()

    def test_num_tokens_normalizes_ru_and_en(self):
        f = self.mod._num_tokens
        self.assertEqual(
            f("$37,97 млрд (2025), CAGR 7,1% до 2033; 685 млн профилей; 60+ стран; 59+ млн"),
            sorted(["37.97", "2025", "7.1", "2033", "685", "60", "59"]))
        self.assertEqual(
            f("$37.97B in 2025 with a 7.1% CAGR to 2033; 60+ countries, 28 languages, "
              "685M profiles; 59M+ profiles"),
            sorted(["37.97", "2025", "7.1", "2033", "60", "28", "685", "59"]))

    def test_text_en_numbers_must_match_registry(self):
        claims = [{"id": "C011", "kind": "fact", "grade": "B",
                   "text": "Мировой рынок: $40 млрд (2025), CAGR 8% до 2033; Indeed — 60 стран",
                   "sources": ["S001"]}]
        self._demo(OPT_OK, claims=claims)
        with self.assertRaisesRegex(self.mod.BuildError, "TEXT_EN"):
            self.mod.claim_facts()

    def test_text_en_matches_registry_passes(self):
        real = ("Мировой рынок онлайн-рекрутинга: $37,97 млрд (2025), CAGR 7,1% до 2033; "
                "Indeed — 60+ стран, 28 языков, 685 млн профилей; Bayt (MENA) — 59+ млн профилей")
        claims = [{"id": "C011", "kind": "fact", "grade": "B", "text": real,
                   "sources": ["S001"]}]
        self._demo(OPT_OK, claims=claims)
        facts = self.mod.claim_facts()
        self.assertEqual(facts["SEG_EN"], facts["TEXT_EN"].split(";")[0].strip())


# ---------- раунд ревью: перенесённые строки «Возражения red team» ----------

OPT_WRAPPED = ("## Вариант A. Оставить как есть — бесплатный OSS\n"
               "- Возражения red team: (1) первое возражение\n"
               "  продолжается на строке переноса; (2) второе возражение\n"
               "  тоже перенесено; (3) третье — целиком на строке переноса\n"
               "- Скрытое допущение: что-то предполагается\n")


class TestWrappedObjections(unittest.TestCase):
    """«Возражения red team» — пункт списка, а не одна строка.

    Ревью PRO-66: жёсткий перенос длинной строки кладёт пункты (2)…(N) на строки
    продолжения; захват только первой строки молча занижал D_OBJ (max() по
    сопоставленной строке), а сборка оставалась зелёной.
    """

    def setUp(self):
        self.mod = _load_build_module()

    def _demo(self, md: str) -> None:
        tmp = Path(tempfile.mkdtemp(prefix="pfs-wrap-"))
        self.mod.DEMO = _fixture_demo(tmp, options_md=md, claims=[{"id": "C001",
                                                                   "kind": "fact",
                                                                   "grade": "B",
                                                                   "text": "т",
                                                                   "sources": ["S001"]}])

    def test_wrapped_objections_counted(self):
        self._demo(OPT_WRAPPED)
        nums = self.mod.demo_numbers()
        self.assertEqual(nums["D_OBJ"], 3,
                         "пункты (2) и (3) на строках продолжения должны считаться")
        self.assertEqual(nums["D_ASM"], 1)

    def test_capture_stops_at_next_bullet(self):
        # числа в скобках в следующих пунктах не приписываются возражениям
        md = ("## Вариант A. Оставить как есть — бесплатный OSS\n"
              "- Возражения red team: (1) первое возражение\n"
              "  продолжение первого пункта без пометок\n"
              "- Скрытое допущение: срок пересмотра (2027-02-10) помечен в скобках\n")
        self._demo(md)
        nums = self.mod.demo_numbers()
        self.assertEqual(nums["D_OBJ"], 1, "(2027…) из «Скрытого допущения» — не возражение")
        self.assertEqual(nums["D_ASM"], 1)

    def test_wrapped_without_numbers_is_loud(self):
        md = ("## Вариант A. Оставить как есть — бесплатный OSS\n"
              "- Возражения red team: возражения есть,\n"
              "  но нумерации нет ни на одной строке переноса\n"
              "- Скрытое допущение: что-то\n")
        self._demo(md)
        with self.assertRaisesRegex(self.mod.BuildError, "нумерованных"):
            self.mod.demo_numbers()


# ---------- раунд ревью: EN-метка выбранного варианта (D_LABEL) ----------

# Вариант с русской меткой + экономика для excel_numbers(): имитирует выбор
# кириллического варианта A — ровно тот случай, когда RU-текст утекал бы на EN.
OPT_RU_LABEL = ("## Вариант A. Оставить как есть — бесплатный OSS\n"
                "- Возражения red team: (1) первое; (2) второе; (3) третье\n"
                "- Скрытое допущение: что-то предполагается\n"
                "- Экономика: paid $29/мес; переменные 25% → CM $21,75; "
                "LTV ≈ $272; LTV/CAC ≈ 4,5\n")

REAL_C011_TEXT = ("Мировой рынок онлайн-рекрутинга: $37,97 млрд (2025), CAGR 7,1% до 2033; "
                  "Indeed — 60+ стран, 28 языков, 685 млн профилей; "
                  "Bayt (MENA) — 59+ млн профилей")


class TestDLabelEn(unittest.TestCase):
    """Метка выбранного варианта из русского 03_options.md не утекает на EN-страницу.

    Ревью PRO-66: D_LABEL берётся из русскоязычного документа; на EN-странице
    должна подставляться EN-метка из карты с громкой сверкой.
    """

    def setUp(self):
        self.mod = _load_build_module()

    def _demo(self, options_md: str, letter: str = "A",
              claims: list[dict] | None = None) -> None:
        tmp = Path(tempfile.mkdtemp(prefix="pfs-dlabel-"))
        self.mod.DEMO = _fixture_demo(tmp, options_md=options_md, letter=letter,
                                      claims=claims or [{"id": "C001", "kind": "fact",
                                                         "grade": "B", "text": "т",
                                                         "sources": ["S001"]}])

    def test_returns_en_label_for_cyrillic_choice(self):
        self._demo(OPT_RU_LABEL)
        nums = self.mod.demo_numbers()
        self.assertEqual(nums["D_LABEL"], "Оставить как есть")
        self.assertEqual(nums["D_LABEL_EN"], "Keep as is")

    def test_unknown_label_is_loud(self):
        self._demo(OPT_RU_LABEL.replace("Оставить как есть", "Продавать приложение"))
        with self.assertRaisesRegex(self.mod.BuildError, "EN-перевода"):
            self.mod.demo_numbers()

    def test_en_label_must_be_cyrillic_free(self):
        # защита от самой карты: RU-значение в ней не должно пройти на EN-страницу
        self.mod.D_LABEL_EN_MAP = {"Метка": "Метка по-русски"}
        self._demo(OPT_RU_LABEL.replace("Оставить как есть", "Метка"))
        with self.assertRaisesRegex(self.mod.BuildError, "кириллиц"):
            self.mod.demo_numbers()

    def test_build_puts_en_label_on_en_page_and_ru_on_ru(self):
        claims = [{"id": "C011", "kind": "fact", "grade": "B",
                   "text": REAL_C011_TEXT, "sources": ["S001"]}]
        tmp = Path(tempfile.mkdtemp(prefix="pfs-dlabel-build-"))
        self.mod.DEMO = _fixture_demo(tmp, options_md=OPT_RU_LABEL, letter="A",
                                      claims=claims)
        out = tmp / "out"
        self.mod.build(out, None)
        en = _visible_text((out / "en" / "index.html").read_text(encoding="utf-8"))
        ru = _visible_text((out / "index.html").read_text(encoding="utf-8"))
        self.assertIn("chosen: Keep as is", en)
        self.assertNotIn("Оставить как есть", en, "RU-метка утекла на EN-страницу")
        self.assertIn("выбор: Оставить как есть", ru)


class TestDLabelOnLivePages(SiteBuildBase):
    """На живых данных демо-проекта EN-плитка показывает EN-метку из карты."""

    def test_en_demo_tile_uses_en_label(self):
        mod = _load_build_module()
        nums = mod.demo_numbers()
        self.assertIn(f"chosen: {nums['D_LABEL_EN']}", self.built["en"])
        self.assertIn(f"выбор: {nums['D_LABEL']}", self.built["ru"])


class TestRound3Review(SiteBuildBase):
    """Правки ревью раунда 3: мобильная шапка, бенто без пустых колонок,
    faq_open только у FAQ-аккордеона, зоны нажатия 44 px у навигации и футера."""

    def _rule(self, page: str, selector: str) -> str:
        css = _strip_css_comments(page)
        m = re.search(re.escape(selector) + r"\{([^}]*)\}", css)
        self.assertIsNotNone(m, f"нет правила {selector}")
        return m.group(1)

    def test_mlink_panel_anchored_to_bar(self):
        # панель мобильного меню шириной с капсулу шапки, а не с 44-px бургер
        for lang, page in self.built.items():
            self.assertIn("position:relative", self._rule(page, ".nav .bar"), lang)
            self.assertNotIn("position:relative", self._rule(page, ".mlink"), lang)
            self.assertIn("position:absolute", self._rule(page, ".mlink-panel"), lang)

    def test_bar_row_fits_narrow_screens(self):
        # 360px: бренд + RU/EN + бургер — CTA в шапке убирается, текст бренда не переносится
        for lang, page in self.built.items():
            self.assertIn("white-space:nowrap", self._rule(page, ".brand"), lang)
            narrow = page.split("@media (max-width:640px){")[1].split("@media")[0]
            self.assertIn(".bar .pill{display:none}", narrow, lang)

    def test_details_border_scoped_to_faq(self):
        # без глобальной рамки details под бургером не появляется лишняя линия
        for lang, page in self.built.items():
            css = _strip_css_comments(page)
            self.assertIn(".faq details{border-bottom", css, lang)
            self.assertNotIn("details{border-bottom",
                             css.replace(".faq details{border-bottom", ""), lang)

    def test_faq_goal_ignores_mobile_menu(self):
        for lang, page in self.built.items():
            self.assertIn("querySelectorAll('details:not(.mlink)')", page, lang)
            self.assertNotIn("querySelectorAll('details')", page, lang)

    def test_bento_rows_fill_twelve_columns(self):
        # десктоп: карточки бенто не оставляют пустых колонок в ряду
        for lang, page in self.built.items():
            block = re.search(r'<div class="grid">(.*?)</section>', page, flags=re.S).group(1)
            widths = [int(m.group(1) or 4)
                      for m in re.finditer(r'<article class="card(?: w(\d+))?"', block)]
            self.assertGreaterEqual(len(widths), 7, lang)
            row = 0
            for w in widths:
                if row + w > 12:
                    self.fail(f"{lang}: карточка w{w} не влезает в ряд (заполнено {row})")
                row = 0 if row + w == 12 else row + w
            self.assertEqual(row, 0, f"{lang}: последний ряд не заполнен (свободно {row})")

    def test_nav_and_footer_links_are_44(self):
        for lang, page in self.built.items():
            self.assertIn("min-height:44px", self._rule(page, ".links a"), lang)
            self.assertIn("min-height:44px", self._rule(page, "footer nav a"), lang)


if __name__ == "__main__":
    unittest.main()
