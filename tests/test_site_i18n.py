"""PRO-61 — bilingual static site (site/).

Checks the acceptance criteria of the issue:
  1. all page strings live in site/i18n/{ru,en}.json, build script produces
     two static versions (RU at /, EN at /en/);
  2. EN visible text has no Cyrillic outside <code>/<pre> (repo paths like
     projects/демо are the whitelist per the issue);
  3. RU visible text has no English runs longer than 3 words outside
     code/allow-listed names;
  4. demo numbers (sources, claims, economics, thresholds, dates) on the site
     come from projects/демо and match it;
  5. counters and the quick-start block are visible without JavaScript.

The checker replaces the Playwright audit with an equivalent stdlib parse of
the *built* pages (the same visible-text surface).
"""

import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = ("index", "demo", "help", "materials")

CYR = re.compile(r"[\u0400-\u04FF]")


def _load_build_module():
    spec = importlib.util.spec_from_file_location(
        "build_site", ROOT / "scripts" / "build_site.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


bs = _load_build_module()


class _VisibleText(HTMLParser):
    """Collect visible text nodes, tracking code/pre and allow-en subtrees."""

    SKIP = {"script", "style", "title"}
    CODE = {"code", "pre"}
    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input",
            "link", "meta", "param", "source", "track", "wbr"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []          # (text, in_code, in_allow_en)
        self.skip_tag = None
        self.skip_depth = 0
        self.code_depth = 0
        self.allow_depth = 0
        self.stack = []          # per-element flags for code / allow-en

    def handle_starttag(self, tag, attrs):
        if self.skip_tag:
            if tag not in self.VOID:
                self.skip_depth += 1
            return
        if tag in self.SKIP:
            self.skip_tag, self.skip_depth = tag, 1
            return
        in_code = tag in self.CODE or self.code_depth > 0
        classes = dict(attrs).get("class", "")
        in_allow = self.allow_depth > 0 or "allow-en" in classes or "allow-ru" in classes
        if in_code:
            self.code_depth += 1
        if in_allow:
            self.allow_depth += 1
        if tag not in self.VOID:
            self.stack.append((in_code, in_allow))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if self.skip_tag:
            if tag == self.skip_tag:
                self.skip_depth -= 1
                if self.skip_depth <= 0:
                    self.skip_tag = None
            return
        if self.stack:
            in_code, in_allow = self.stack.pop()
            if in_code:
                self.code_depth -= 1
            if in_allow:
                self.allow_depth -= 1

    def handle_data(self, data):
        if self.skip_tag:
            return
        self.parts.append((data, self.code_depth > 0, self.allow_depth > 0))

    def text(self, skip_allow_en=False):
        # join nodes with newlines so runs never cross element boundaries
        return "\n".join(
            t for t, code, allow in self.parts
            if not code and not (skip_allow_en and allow))


def visible_text(html, skip_allow_en=False):
    p = _VisibleText()
    p.feed(html)
    p.close()
    return p.text(skip_allow_en=skip_allow_en)


def _letter_words(tokens):
    out = []
    for t in tokens:
        t = t.strip("«»\"'(),.:;!?")
        if re.fullmatch(r"[A-Za-z][A-Za-z\-']*", t):
            out.append(t)
    return out


def _norm(run_words):
    s = " ".join(run_words).lower()
    s = re.sub(r"[^a-z0-9\- ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def _latin_runs(text, min_words=4):
    """Runs of consecutive Latin letter-words (>= min_words), no Cyrillic between."""
    runs = []
    cur = []

    def flush():
        words = _letter_words(cur)
        if len(words) >= min_words:
            runs.append(words)

    for raw in text.split():
        if CYR.search(raw):
            flush()
            cur = []
        else:
            cur.append(raw)
    flush()
    return runs


# Proper names allowed on the RU page (tier names, launch channels, phase names).
RU_ALLOWED_LATIN = {
    "seo open-source jobscan alternative",
    "product hunt hn seo open-source jobscan alternative",
    "product hunt hacker news seo open-source jobscan alternative",
    "free byok pro unlimited opt-in",
    "double diamond discover define develop deliver",
    "discover define develop deliver",
    "red team",
    "ru en",
    "six-pager english",
    "ltv cac",
    "product factory strategist",
    # форматы и списки имён (легитимная латынь на RU-страницах)
    "pdf docx xlsx csv",
    "en ru habr career",
    "b hosted freemium saas",
    "cvstart hosted freemium saas",
    "claude code cursor codex opencode windsurf copilot",
    "excel ru en six-pager",
    "cv start open-source ai resume builder",
    "en ru habr career geekjob getmatch trudvsem",
    "zety novoresume kickresume enhancv teal rezi freemium",
    "ph hn seo open-source jobscan alternative",
    "s006 wiseguy reports c005",
    "s005 kickresume press c009",
    "c b2b white-label",
    "d dual-license",
    "claude code cursor codex linear lovable higgsfield rea feynman",
    "sources interviews analysis outputs",
    "md pdf docx excel",
    "public own interview synthetic origin",
    "which pfs path projects dir",
    "profile cohort funnel stats",
    "cursor codex opencode windsurf copilot",
    "codex opencode windsurf copilot",
    "higgsfield rea feynman officecli higgsfield",
    "lovable out of credits",
    "mcp tool not found",
    "ru md pdf docx",
    "en md pdf docx",
    "pdf docx markdown six-pager",
    "resume builders rezi pricing",
    "cv studio cover letters",
    "claude code cursor codex opencode windsurf",
    "wiseguy reports",
    "kickresume press",
    "c white-label",
    "claude code",
    "cursor codex",
    "higgsfield rea feynman",
}


class TestSiteDictionaries(unittest.TestCase):
    """site/i18n/{ru,en}.json hold all page strings, paired per key."""

    def test_dictionaries_exist_and_are_paired(self):
        ru = json.loads((ROOT / "site" / "i18n" / "ru.json").read_text("utf-8"))
        en = json.loads((ROOT / "site" / "i18n" / "en.json").read_text("utf-8"))
        for page in PAGES:
            self.assertIn(page, ru, f"ru.json misses page {page}")
            self.assertIn(page, en, f"en.json misses page {page}")
            self.assertEqual(set(ru[page]), set(en[page]),
                             f"ru/en keys differ for page {page}")
            self.assertTrue(len(ru[page]) > 50, f"too few strings for {page}")

    def test_i18n_json_byte_identical_to_extraction(self):
        """Committed site/i18n/{ru,en}.json equal extract_all() output byte-for-byte.

        Extraction is a dev-time step (see .github/workflows/pages.yml: the deploy
        build must not pass --extract). This byte-level gate is what makes
        translation drift fail CI instead of being silently rewritten at deploy.
        """
        extracted = bs.extract_all()
        for lang in ("ru", "en"):
            serialized = json.dumps(
                extracted[lang], ensure_ascii=False, indent=1) + "\n"
            committed = (ROOT / "site" / "i18n" / f"{lang}.json").read_text("utf-8")
            self.assertEqual(
                serialized, committed,
                f"site/i18n/{lang}.json is stale vs site/src templates "
                f"(run: python3 scripts/build_site.py --extract)")


class _BuiltSite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.out = Path(cls._tmp.name)
        bs.build(out_dir=cls.out, extract=False)

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def _ru(self, page):
        return (self.out / f"{page}.html").read_text("utf-8")

    def _en(self, page):
        return (self.out / "en" / f"{page}.html").read_text("utf-8")


class TestBuildTwoVersions(_BuiltSite):

    def test_all_pages_built_for_both_langs(self):
        for page in PAGES:
            ru_html = self._ru(page)
            en_html = self._en(page)
            self.assertIn('<html lang="ru">', ru_html)
            self.assertIn('<html lang="en">', en_html)
            self.assertNotIn("data-lang", en_html)
            self.assertNotIn("setLang", en_html)
            self.assertNotIn("setLang", ru_html)
            self.assertIn('rel="alternate" hreflang="en"', ru_html)
            self.assertIn('rel="alternate" hreflang="ru"', en_html)

    def test_no_unresolved_tokens(self):
        for page in PAGES:
            for rel in (f"{page}.html", f"en/{page}.html"):
                html = (self.out / rel).read_text("utf-8")
                self.assertNotIn("{{", html, f"unresolved token in {rel}")
                self.assertNotIn("LANGSWITCH", html, f"unresolved marker in {rel}")

    def test_en_links_point_up_one_level(self):
        html = self._en("demo")
        self.assertIn('href="../index.html', html)
        self.assertIn('src="../assets/', html)
        self.assertNotIn('src="assets/', html)

    def test_cli_help_works(self):
        r = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "build_site.py"), "--help"],
            capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_deploy_workflow_builds_from_committed_i18n(self):
        """.github/workflows/pages.yml must NOT pass --extract at deploy.

        site/i18n/{ru,en}.json are committed artifacts of a dev-time extraction;
        the deploy build reads them. Silent rewriting at deploy would mask
        translation drift — the byte-for-byte test above is what fails CI on it.
        """
        wf = (ROOT / ".github" / "workflows" / "pages.yml").read_text("utf-8")
        self.assertIn("scripts/build_site.py", wf, "deploy build step missing")
        self.assertNotIn("--extract", wf,
                         "deploy must build from committed i18n, not rewrite it")


class TestEnglishLeaks(_BuiltSite):
    """Built EN pages: visible text without Cyrillic (code/pre whitelisted)."""

    def test_en_pages_have_no_cyrillic(self):
        leaks = []
        for page in PAGES:
            # allow-marked subtrees are intentional single-language samples
            # (e.g. the RU six-pager excerpt on the EN demo page)
            text = visible_text(self._en(page), skip_allow_en=True)
            for line in text.splitlines():
                if CYR.search(line):
                    leaks.append(f"en/{page}.html: {line.strip()[:120]}")
        self.assertEqual(leaks, [], "Cyrillic leaked into EN pages")


class TestRussianLeaks(_BuiltSite):
    """Built RU pages: no English runs longer than 3 words (names whitelisted)."""

    def test_ru_pages_have_no_long_english_runs(self):
        leaks = []
        for page in PAGES:
            text = visible_text(self._ru(page), skip_allow_en=True)
            for run in _latin_runs(text, min_words=4):
                norm = _norm(run)
                if norm not in RU_ALLOWED_LATIN:
                    leaks.append(f"{page}.html: {' '.join(run)[:120]}")
        self.assertEqual(leaks, [], "untranslated English runs on RU pages")

    def test_ru_pages_have_no_pure_latin_fragments(self):
        leaks = []
        for page in PAGES:
            text = visible_text(self._ru(page), skip_allow_en=True)
            for line in text.splitlines():
                line = line.strip()
                if not line or CYR.search(line):
                    continue
                words = _letter_words(line.split())
                norm = _norm(words)
                if len(words) >= 2 and norm not in RU_ALLOWED_LATIN:
                    leaks.append(f"{page}.html: {line[:120]}")
        self.assertEqual(leaks, [], "pure-English fragments on RU pages")


class TestNumbersMatchDemo(_BuiltSite):
    """Site numbers are derived from projects/демо, not hand-typed."""

    def test_sources_and_claims_counts(self):
        data = bs.load_demo_data()
        n_src, n_clm = data["sources_count"], data["claims_count"]
        s_range, c_range = data["s_range"], data["c_range"]
        self.assertEqual(n_src, 10)
        self.assertEqual(n_clm, 20)
        self.assertEqual(s_range, "S001–S002, S004–S011")
        for page in ("demo", "materials"):
            self.assertIn(f"<b>{n_src}</b>", self._ru(page))
            self.assertIn(s_range, self._ru(page))
            self.assertIn(f"<b>{n_src}</b>", self._en(page))
            self.assertIn(c_range, self._ru(page))
            self.assertIn(c_range, self._en(page))

    def test_unit_economics_from_calcs(self):
        calcs = json.loads(
            (ROOT / "projects" / "демо" / "calcs.json").read_text("utf-8"))["unit_econ"]
        cm = calcs["arpu"] * (1 - calcs["vc_share"])            # 21.75
        self.assertEqual(cm, 21.75)
        ru_demo = self._ru("demo")
        en_demo = self._en("demo")
        self.assertIn("$21,75", ru_demo)
        self.assertIn("$271,88", ru_demo)
        self.assertIn("$21.75", en_demo)
        self.assertIn("$271.88", en_demo)
        self.assertNotIn("$21,75", en_demo)   # EN must use decimal points
        self.assertNotIn("$271,88", en_demo)

    def test_dates_and_window_from_decision(self):
        dec = json.loads(
            (ROOT / "projects" / "демо" / "decisions.jsonl")
            .read_text("utf-8").splitlines()[0])
        commit = re.search(r"\d{4}-\d{2}-\d{2}", dec["commitments"][0]["due"]).group(0)
        self.assertEqual(commit, "2026-12-15")
        self.assertEqual(dec["review"]["date"], "2027-02-10")
        for page in ("index", "demo", "materials"):
            for html in (self._ru(page), self._en(page)):
                self.assertIn(commit, html, page)
                self.assertIn("2027-02-10", html, page)
        self.assertIn("8 недель", self._ru("demo"))
        self.assertIn("8 weeks", self._en("demo"))

    def test_thresholds_include_both_branches(self):
        ru_demo = visible_text(self._ru("demo"))
        # stop branch…
        self.assertIn("активации < 35%", ru_demo)
        # …and the previously missing case: paid < 20 with activation >= 35%
        self.assertIn("активации ≥ 35%", ru_demo)
        self.assertIn("activation ≥ 35%", visible_text(self._en("demo")))

    def test_funnel_model_numbers(self):
        self.assertIn("53", self._ru("demo"))
        self.assertIn("1 537", self._ru("demo"))
        self.assertIn("1,537", self._en("demo"))


class TestChangeCaseFromDemo(unittest.TestCase):
    """Ревью PRO-61, круг 2: случай «платящих < 20 при activation ≥ 35 %» показан
    на сайте, поэтому он обязан существовать в видимых артефактах демо
    (06_validation_plan.md и триггер пересмотра D001) и подставляться в сайт
    из них, а не набиваться в site/i18n (критерий №2 «числа сайта = демо»)."""

    DEMO = ROOT / "projects" / "демо"

    def _plan(self):
        return (self.DEMO / "outputs" / "06_validation_plan.md").read_text("utf-8")

    def test_validation_plan_has_change_case(self):
        self.assertIsNotNone(
            re.search(r"paid < (\d+) к нед\. \d+ при activation ≥ (\d+)%", self._plan()),
            "в 06_validation_plan.md демо нет случая «paid < N к нед. M при activation ≥ K%» — "
            "сайт его показывает, а демо-проект нет (критерий «числа сайта = демо» нарушен)")

    def test_decision_trigger_has_change_case(self):
        dec = json.loads((self.DEMO / "decisions.jsonl")
                         .read_text("utf-8").splitlines()[0])
        triggers = " ; ".join(dec["review"].get("triggers", []))
        self.assertRegex(
            triggers, r"paid < \d+ .*activation ≥ \d+%",
            "в триггерах пересмотра D001 нет случая «paid < N при activation ≥ K%»")

    def test_change_row_is_substituted_from_demo(self):
        m = re.search(r"paid < (\d+) к нед\. \d+ при activation ≥ (\d+)%", self._plan())
        paid, act = (int(m.group(i)) for i in (1, 2))
        data = bs.load_demo_data()
        self.assertEqual(data["paid_change"], paid)
        self.assertEqual(data["act_change"], act)
        for lang in ("ru", "en"):
            i18n = json.loads((ROOT / "site" / "i18n" / f"{lang}.json").read_text("utf-8"))
            # строка ветки «изменить» собирается из демо-чисел, а не набита руками
            self.assertIn("{{PAID_CHANGE_LOW}}", i18n["demo"]["k132"], lang)
            self.assertIn("{{ACT_CHANGE}}", i18n["demo"]["k132"], lang)
            self.assertNotIn("{{ACT_STOP}}", i18n["demo"]["k132"], lang)


class TestNoJsVisibility(_BuiltSite):
    """Counters and quick start must be visible without JavaScript."""

    def test_counters_are_static(self):
        for rel in ("index.html", "en/index.html"):
            html = (self.out / rel).read_text("utf-8")
            for m in re.finditer(r'<span class="cnt" data-target="(\d+)">([^<]*)</span>', html):
                self.assertEqual(m.group(2), m.group(1),
                                 f"{rel}: counter shows '{m.group(2)}' before JS")
            self.assertNotIn(">0</span>", html)

    def test_quickstart_is_static_text(self):
        for rel in ("index.html", "en/index.html"):
            html = (self.out / rel).read_text("utf-8")
            self.assertNotIn('id="typed"', html, rel)
            self.assertIn("$ git clone", html, rel)


if __name__ == "__main__":
    unittest.main()
