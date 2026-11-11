"""PRO-66: генератор лендинга scripts/build_site.py — RU и EN из данных репозитория.

Проверяются: генерация site/index.html и site/en/index.html, hreflang/OG, палитра v3
«тёплый тёмный» без градиентного текста, контраст WCAG AA, подстановка чисел из
репозитория (карты/навыки/тесты/демо-проект), отсутствие языковых утечек в EN,
цели Метрики, видимость без JS, постер и prefers-reduced-motion у видео.
"""
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
    total = 0
    for p in (ROOT / "tests").glob("test_*.py"):
        total += len(re.findall(r"\bdef test_", p.read_text(encoding="utf-8")))
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
        self.assertIn('property="og:image" content="https://strategyproduct.ru/assets/og/og-ru.jpg"', self.built["ru"])
        self.assertIn('property="og:image" content="https://strategyproduct.ru/assets/og/og-en.jpg"', self.built["en"])
        for lang, page in (("ru", self.built["ru"]), ("en", self.built["en"])):
            self.assertIn('property="og:title"', page, lang)
            self.assertIn('property="og:image:width" content="1200"', page, lang)
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
    def test_committed_pages_match_build(self):
        committed_ru = (ROOT / "site" / "index.html").read_text(encoding="utf-8")
        committed_en = (ROOT / "site" / "en" / "index.html").read_text(encoding="utf-8")
        self.assertEqual(self.built["ru"], committed_ru,
                         "site/index.html не совпадает со сборкой — перезапустите scripts/build_site.py")
        self.assertEqual(self.built["en"], committed_en,
                         "site/en/index.html не совпадает со сборкой — перезапустите scripts/build_site.py")

    def test_referenced_assets_exist(self):
        for rel in ("assets/logo.svg", "assets/hero-poster.webp",
                    "assets/og/og-ru.jpg", "assets/og/og-en.jpg"):
            self.assertTrue((ROOT / "site" / rel).exists(), rel)
        self.assertTrue((ROOT / "site" / "assets" / "hero-swarm-2.mp4").exists())


if __name__ == "__main__":
    unittest.main()
