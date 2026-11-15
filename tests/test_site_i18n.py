"""PRO-61 gate (see repo tests/test_site_i18n.py)."""
from __future__ import annotations

import html as html_mod
import importlib.util
import json
import math
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_site.py"
SITE = ROOT / "site"
DEMO = ROOT / "projects" / "демо"
CYR = re.compile(r"[\u0400-\u04FF]")

PAGES = ("index", "demo", "help", "materials")
PAGE_URL = {"index": "", "demo": "demo.html", "help": "help.html", "materials": "materials.html"}


def load_module():
    spec = importlib.util.spec_from_file_location("build_site_i18n", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def visible_text(page: str, skip_code: bool = True) -> str:
    """Видимый текст; границы элементов — « | », чтобы английские «предложения»
    не склеивались из соседних узлов (таблиц, чипов, капкandов)."""
    body = re.sub(r"<script\b.*?</script>", " ", page, flags=re.S)
    body = re.sub(r"<style\b.*?</style>", " ", body, flags=re.S)
    if skip_code:
        body = re.sub(r"<code\b.*?</code>", " ", body, flags=re.S)
        body = re.sub(r"<pre\b.*?</pre>", " ", body, flags=re.S)
    body = re.sub(r"<[^>]+>", " | ", body)
    body = html_mod.unescape(body)
    return re.sub(r"(?:\s*\|)+", " | ", body)


NAMES_EN = frozenset("""
ai arr ats byok cac cagr check claude cli core codex cover cursor cvstart de
deck demo docx en enhance enhancv es eu excel faq feynman follow-up free
geekjob getmatch github gdpr hosted hh html humanize ja jobscan json kickresume
linear linkedin lovable llm ltv md mit mock mrr nps open-source opencode opt-in
oss paid pf-s product pro pt-br rezi ru saas sarah seo six-pager strict studio
teal the tracker trudvsem ui unlimited up us white-label windsurf wsl zh zety
bayt indeed hunt builders pfs a b c d e s k n x t v m r io ios
pam tam sam som discover define develop deliver
claims jsonl sources state outputs attachments analysis interviews knowledge
templates rubrics agents changelog readme license python sha256 gdcompliance
compliance cv career ops career-ops-ui images xlsx slug wikilinks
""".split())


def english_runs(text: str, min_len: int = 4) -> list[str]:
    """Английские предложения длиннее min_len-1 слов ВНУТРИ одного текстового
    узла: «|» — границы элементов из visible_text, русское слово обрывает
    английское предложение (соседние термины «BYOK-free ATS UE CM» — это
    названия, а не предложение; они разделены русским текстом или стоят
    по одному)."""
    out: list[str] = []
    word_re = re.compile(r"[A-Za-z][A-Za-z'\u2019\-]*|[\u0400-\u04FF][\u0400-\u04FF\-]*")
    for segment in text.split("|"):
        cur: list[str] = []
        for tok in word_re.findall(segment):
            if tok[0] > "\u0400":  # русское слово — конец английского предложения
                if len(cur) >= min_len:
                    out.append(" ".join(cur))
                cur = []
                continue
            if tok.lower() in NAMES_EN:
                if len(cur) >= min_len:
                    out.append(" ".join(cur))
                cur = []
                continue
            cur.append(tok)
        if len(cur) >= min_len:
            out.append(" ".join(cur))
    return out



def ru_decimal_commas(text: str) -> list[str]:
    bad = []
    for m in re.finditer(r"\d[\d,]*\d|\d", text):
        g = m.group()
        if "," in g and re.search(r"\d,\d", g) \
                and not re.fullmatch(r"\d{1,3}(,\d{3})+", g):
            bad.append(g)
    return sorted(set(bad))


def _jsonl(path: Path) -> list[dict]:
    return [json.loads(l) for l in
            path.read_text(encoding="utf-8").splitlines() if l.strip()]


def demo_claims() -> dict:
    claims = _jsonl(DEMO / ("claims" + ".jsonl"))
    return {"rows": claims, "total": len(claims),
            "facts": sum(1 for c in claims if c.get("kind") == "fact")}


def demo_sources() -> list[dict]:
    return _jsonl(DEMO / ("sources" + ".jsonl"))


def d001() -> dict:
    rows = _jsonl(DEMO / ("decisions" + ".jsonl"))
    return next(d for d in rows if d.get("id") == "D001")


def n_source_files() -> int:
    return len(list((DEMO / "sources").glob("S*.md")))


def ru_date(iso: str) -> str:
    y, m, d = iso.split("-")
    return f"{d}.{m}.{y}"


def en_date(iso: str) -> str:
    return iso



class SiteI18NBase(unittest.TestCase):
    built: dict[tuple[str, str], str] = {}

    @classmethod
    def setUpClass(cls) -> None:
        tmp = Path(tempfile.mkdtemp(prefix="pfs-site-i18n-"))
        r = subprocess.run([sys.executable, str(SCRIPT), "--out", str(tmp)],
                           cwd=ROOT, capture_output=True, text=True)
        assert r.returncode == 0, f"build_site.py упал: {r.stderr[:400]}"
        for page in PAGES:
            cls.built[("ru", page)] = (tmp / f"{page}.html").read_text(encoding="utf-8")
            cls.built[("en", page)] = (tmp / "en" / f"{page}.html").read_text(encoding="utf-8")
        cls.tmp = tmp


class TestStaticVersions(SiteI18NBase):
    def test_all_eight_pages_generated(self):
        for page in PAGES:
            self.assertTrue((self.tmp / f"{page}.html").exists(), page)
            self.assertTrue((self.tmp / "en" / f"{page}.html").exists(), f"en/{page}")

    def test_single_language_per_dom(self):
        """Старая схема body[data-lang] с двумя языками в DOM запрещена."""
        for key, page in self.built.items():
            self.assertNotIn("data-lang", page, f"{key}: двухъязычный DOM")
            self.assertNotIn("[lang=ru]", page, f"{key}: CSS-переключение языков")
            self.assertNotIn("[lang=en]", page, f"{key}: CSS-переключение языков")

    def test_lang_attr_and_canonical_per_page(self):
        for page in PAGES:
            ru, en = self.built[("ru", page)], self.built[("en", page)]
            self.assertIn('<html lang="ru">', ru, page)
            self.assertIn('<html lang="en">', en, page)
            url = PAGE_URL[page]
            self.assertIn(f'<link rel="canonical" href="https://strategyproduct.ru/{url}">', ru, page)
            self.assertIn(f'<link rel="canonical" href="https://strategyproduct.ru/en/{url}">', en, page)

    def test_hreflang_pair_per_page(self):
        for page in PAGES:
            for key in (("ru", page), ("en", page)):
                page_html = self.built[key]
                url = PAGE_URL[page]
                self.assertIn(f'hreflang="ru" href="https://strategyproduct.ru/{url}"',
                              page_html, key)
                self.assertIn(f'hreflang="en" href="https://strategyproduct.ru/en/{url}"',
                              page_html, key)

    def test_en_internal_links_stay_in_en_tree(self):
        """Навигация EN-версии (логотип, «← Landing page», якоря) остаётся в /en/;
        ../ допустим только у ассетов и у переключателя на русскую версию."""
        for page in PAGES:
            page_html = self.built[("en", page)]
            self.assertNotIn('href="../index.html"', page_html,
                             f"en/{page}: ссылка на русскую версию лендинга")
            for m in re.finditer(r'<a\b[^>]*href="\.\./([a-z]+\.html)[^"]*"[^>]*>', page_html):
                self.assertIn('hreflang="ru"', m.group(0),
                              f"en/{page}: ../{m.group(1)} вне переключателя языка")
                self.assertIn("lang_switch", m.group(0),
                              f"en/{page}: ../{m.group(1)} вне переключателя языка")

    def test_internal_links_resolve_in_own_tree(self):
        """Каждая внутренняя ссылка существует в дереве своей language-версии."""
        for page in PAGES:
            for lang in ("ru", "en"):
                prefix = "" if lang == "ru" else "en/"
                for href in re.findall(r'href="((?:index|demo|help|materials)\.html[^"]*)"',
                                       self.built[(lang, page)]):
                    path = href.split("#")[0].split("?")[0]
                    self.assertTrue((self.tmp / (prefix + path)).exists(),
                                    f"{lang}/{page}: битая ссылка {href}")

    def test_no_placeholder_tokens(self):
        for key, page in self.built.items():
            self.assertNotIn("{{", page, key)



class TestCrossLinks(SiteI18NBase):
    """Перекрёстные ссылки: EN-лендинг ведёт на EN-подстраницы, переключатель
    языка — ссылка на пару, ассеты EN-страниц resolv'ятся из /en/."""

    def test_en_landing_links_to_en_subpages(self):
        en = self.built[("en", "index")]
        for href in ("demo.html", "help.html", "materials.html"):
            self.assertIn(f'href="{href}"', en, href)
            self.assertNotIn(f'href="../{href}"', en, href)

    def test_lang_switch_is_a_link_pair(self):
        for name in PAGES:
            en, ru = self.built[("en", name)], self.built[("ru", name)]
            if name == "index":
                self.assertIn('<a href="../" hreflang="ru"', en, name)
                self.assertIn('<a href="en/" hreflang="en"', ru, name)
            else:
                self.assertIn(f'<a href="../{name}.html" hreflang="ru"', en, name)
                self.assertIn(f'<a href="en/{name}.html" hreflang="en"', ru, name)

    def test_single_head_metadata(self):
        """Одна title/description/canonical на страницу — без дублей из исходника."""
        for key, page in self.built.items():
            self.assertEqual(page.count("<title>"), 1, key)
            self.assertEqual(page.count('rel="canonical"'), 1, key)
            self.assertEqual(page.count('name="description"'), 1, key)

    def test_en_assets_resolve_from_subdir(self):
        for name in PAGES:
            page = self.built[("en", name)]
            self.assertNotRegex(page, r'src="assets/', f"en/{name}")
            self.assertNotRegex(page, r'src="\.\./\.\./assets/', f"en/{name}")


class TestLanguageGate(SiteI18NBase):
    def test_en_visible_text_has_no_cyrillic(self):
        """Кириллица на EN-страницах — только в <code>/<pre>: команды и пути демо."""
        for page in PAGES:
            text = visible_text(self.built[("en", page)])
            leaks = CYR.findall(text)
            self.assertEqual(leaks, [], f"en/{page}: {''.join(leaks[:20])}")

    def test_ru_visible_text_has_no_english_sentences(self):
        """RU-страницы: без английских предложений длиннее 3 слов."""
        for page in PAGES:
            text = visible_text(self.built[("ru", page)])
            runs = english_runs(text)
            self.assertEqual(runs, [], f"ru/{page}: {runs[:3]}")

    def test_ru_pages_have_russian(self):
        for page in PAGES:
            self.assertGreater(len(CYR.findall(visible_text(self.built[("ru", page)]))), 100, page)

    def test_en_numbers_no_ru_decimal_comma(self):
        for page in PAGES:
            text = visible_text(self.built[("en", page)])
            bad = ru_decimal_commas(text)
            self.assertEqual(bad, [], f"en/{page}: русские запятые в числах: {bad[:5]}")


class TestI18nDictionaries(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ru = json.loads((SITE / "i18n" / "ru.json").read_text(encoding="utf-8"))
        cls.en = json.loads((SITE / "i18n" / "en.json").read_text(encoding="utf-8"))

    @staticmethod
    def keyset(obj, prefix=""):
        keys = set()
        if isinstance(obj, dict):
            for k, v in obj.items():
                p = f"{prefix}.{k}" if prefix else str(k)
                keys.add(p)
                keys |= TestI18nDictionaries.keyset(v, p)
        return keys

    def test_dictionaries_exist_and_load(self):
        self.assertTrue((SITE / "i18n" / "ru.json").exists())
        self.assertTrue((SITE / "i18n" / "en.json").exists())

    def test_key_parity(self):
        """Одинаковый набор ключей; исключение — demo_data_en (переводы данных
        реестра демо-проекта, сверяются по числам, а не по ключам)."""
        ru_keys = {k for k in self.keyset(self.ru) if not k.startswith("demo_data_en")}
        en_keys = {k for k in self.keyset(self.en) if not k.startswith("demo_data_en")}
        self.assertEqual(ru_keys, en_keys,
                         f"расхождение ключей: {sorted(ru_keys ^ en_keys)[:10]}")

    def test_values_non_empty(self):
        for name, d in (("ru", self.ru), ("en", self.en)):
            def walk(obj, prefix=""):
                if isinstance(obj, dict):
                    for k, v in obj.items():
                        walk(v, f"{prefix}.{k}")
                elif isinstance(obj, str):
                    self.assertTrue(obj.strip(), f"{name}{prefix}: пустое значение")
            walk(d)

    def test_en_values_cyrillic_only_in_paths(self):
        """В EN-словаре кириллица допустима только в путях репозитория."""
        def walk(obj, prefix=""):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    walk(v, f"{prefix}.{k}")
            elif isinstance(obj, str) and CYR.search(obj):
                self.assertIn("/", obj, f"en{prefix}: кириллица вне пути: {obj!r}")
        walk(self.en)

    @staticmethod
    def _plain(value: str) -> str:
        """Значения словаря — HTML-фрагменты: снимаем разметку для сравнения."""
        return html_mod.unescape(re.sub(r"<[^>]+>", " ", value)).split()

    def test_i18n_strings_reach_pages(self):
        """Страницы собираются из словаря: маркерные строки из JSON видны в HTML."""
        ru_demo = visible_text((SITE / "demo.html").read_text(encoding="utf-8"))
        en_help = visible_text((SITE / "en" / "help.html").read_text(encoding="utf-8"))
        ru_lead = " ".join(self._plain(self.ru["demo_page"]["lead"]))
        en_lead = " ".join(self._plain(self.en["help_page"]["lead"]))
        self.assertIn(ru_lead[:40], ru_demo)
        self.assertIn(en_lead[:40], en_help)



class TestDemoNumbersOnSite(SiteI18NBase):
    """Числа демо не набиты руками: сверяются с projects/демо независимо."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.claims = demo_claims()
        cls.sources = demo_sources()
        cls.d = d001()

    def test_registry_counters(self):
        ru = visible_text(self.built[("ru", "demo")])
        en = visible_text(self.built[("en", "demo")])
        self.assertIn(str(n_source_files()), ru)
        self.assertIn(str(self.claims["total"]), ru)
        self.assertIn(str(self.claims["facts"]), ru)
        self.assertIn(str(n_source_files()), en)
        self.assertIn(str(self.claims["total"]), en)
        self.assertIn(str(self.claims["facts"]), en)

    def test_no_fake_source_range(self):
        """Расхождение из задачи («10 источников» против «S001–S011») не должно
        возвращаться: показанный диапазон ID совпадает с реестром."""
        ids = {s["id"] for s in self.sources}
        for page in PAGES:
            text = visible_text(self.built[("ru", page)])
            for m in re.findall(r"S(\d{3})\u2013S(\d{3})", text):
                for n in m:
                    self.assertIn(f"S{n}", ids, f"ru/{page}: ID вне реестра")

    def test_options_letters_and_counts(self):
        options_md = (DEMO / "outputs" / "03_options.md").read_text(encoding="utf-8")
        letters = re.findall(r"^## Вариант ([A-ZА-Я])\.", options_md, flags=re.M)
        ru = visible_text(self.built[("ru", "demo")])
        self.assertIn("A–" + letters[-1], ru)
        self.assertIn(letters[0], ru)

    def test_decision_dates_from_registry(self):
        review = self.d["review"]["date"]
        due = re.search(r"(\d{4}-\d{2}-\d{2})", self.d["commitments"][0]["due"]).group(1)
        ru = visible_text(self.built[("ru", "demo")])
        en = visible_text(self.built[("en", "demo")])
        self.assertIn(ru_date(review), ru, "дата пересмотра D001")
        self.assertIn(ru_date(due), ru, "срок обязательства K1")
        self.assertIn(en_date(review), en)
        self.assertIn(en_date(due), en)

    def test_tiers_from_decision(self):
        m = re.search(r"Pro \$(\d+) / Unlimited \$(\d+)", self.d["decision"])
        self.assertIsNotNone(m, "в D001 нет строки тарифов")
        for lang in ("ru", "en"):
            text = visible_text(self.built[(lang, "demo")])
            self.assertIn(f"Pro ${m.group(1)}", text, lang)
            self.assertIn(f"Unlimited ${m.group(2)}", text, lang)

    def test_funnel_numbers_week12(self):
        v06 = (DEMO / "outputs" / "06_validation_plan.md").read_text(encoding="utf-8")
        m = re.search(r"(\d[\d ]*) посетителей → (\d[\d ]*) регистрации → "
                      r"(\d[\d ]*) активаций → (\d+) платящих \(MRR \$([\d ]+)\)", v06)
        self.assertIsNotNone(m, "в 06_validation_plan.md нет воронки недели 12")
        nums = [g.replace(" ", "") for g in m.groups()]
        ru = visible_text(self.built[("ru", "demo")])
        en = visible_text(self.built[("en", "demo")])
        self.assertIn(nums[0].replace(",", ""), ru.replace("\u00a0", " "))
        self.assertIn(nums[3], ru)
        for raw in (nums[0], nums[1], nums[2]):
            n = int(raw)
            en_form = f"{n:,}" if n >= 1000 else str(n)
            self.assertIn(en_form, en, raw)
        self.assertIn(f"${int(nums[4]):,}", en)

    def test_thresholds_three_branches(self):
        """Продолжить / Изменить / Остановить — включая случай
        «платящих < 20 при activation < 35%» из плана проверки."""
        v06 = (DEMO / "outputs" / "06_validation_plan.md").read_text(encoding="utf-8")
        cont = re.search(r"paid ≥ (\d+) к нед\. (\d+), activation ≥ (\d+)%, "
                         r"churn платящих ≤ (\d+)%/мес", v06)
        adjust = re.search(r"paid (\d+)–(\d+) → пересобрать тир/цену \(\$(\d+)\?\)", v06)
        stop = re.search(r"paid < (\d+) к нед\. \d+ при activation < (\d+)%", v06)
        self.assertIsNotNone(cont, "нет ветки «Продолжить»")
        self.assertIsNotNone(adjust, "нет ветки «Изменить»")
        self.assertIsNotNone(stop, "нет ветки «Остановить»")
        for lang in ("ru", "en"):
            text = visible_text(self.built[(lang, "demo")])
            for n in cont.groups() + adjust.groups() + stop.groups():
                self.assertIn(n, text, f"{lang}: порог {n}")

    def test_beta_days_match_decision_and_plan(self):
        v06 = (DEMO / "outputs" / "06_validation_plan.md").read_text(encoding="utf-8")
        days_plan = re.search(r"\((\d+) дней\)", v06)
        days_dec = re.search(r"(\d+)-дневная бета", self.d["decision"])
        self.assertIsNotNone(days_plan)
        self.assertIsNotNone(days_dec)
        self.assertEqual(days_plan.group(1), days_dec.group(1),
                         "«90 дней беты» и план должны сходиться с решением D001")
        for lang in ("ru", "en"):
            self.assertIn(days_plan.group(1), visible_text(self.built[(lang, "demo")]))

    def test_ground_claims_russian_on_ru_page(self):
        grounds = set(self.d["grounds"])
        rows = {c["id"]: c for c in self.claims["rows"]}
        ru = visible_text(self.built[("ru", "demo")])
        for cid in sorted(grounds):
            self.assertIn(cid, ru, cid)
            self.assertIn(rows[cid]["text"][:40], ru, cid)

    def test_ground_claims_en_translations_match_numbers(self):
        en_json = json.loads((SITE / "i18n" / "en.json").read_text(encoding="utf-8"))
        translations = en_json["demo_data_en"]["claims"]
        grounds = set(self.d["grounds"])
        rows = {c["id"]: c for c in self.claims["rows"]}
        en_page = visible_text(self.built[("en", "demo")])
        mod = load_module()
        for cid in sorted(grounds):
            self.assertIn(cid, translations, f"нет EN-перевода {cid}")
            self.assertIn(translations[cid][:40], en_page, cid)
            self.assertEqual(mod._num_tokens(rows[cid]["text"]),
                             mod._num_tokens(translations[cid]),
                             f"{cid}: числа перевода расходятся с реестром")

    def test_trigger_and_metric_en_translations(self):
        en_json = json.loads((SITE / "i18n" / "en.json").read_text(encoding="utf-8"))
        data = en_json["demo_data_en"]
        en_page = visible_text(self.built[("en", "demo")])
        mod = load_module()
        trigger = "; ".join(self.d["review"]["triggers"])
        tr_en = " ; ".join(data["triggers"])
        self.assertEqual(mod._num_tokens(trigger), mod._num_tokens(tr_en))
        for part in data["triggers"]:
            self.assertIn(part[:30], en_page, part[:30])
        metric = self.d["metrics"][0]
        self.assertEqual(mod._num_tokens(metric["target"] + " " + metric["baseline"]),
                         mod._num_tokens(data["metric_target"]))
        self.assertIn(data["metric_target"], en_page)

    def test_steps_no_duplicates(self):
        """Шаги 8 и 9 оба называли «Проверка» — теперь имена шагов различны."""
        for lang in ("ru", "en"):
            for page in ("demo", "help"):
                page_html = self.built[(lang, page)]
                m = re.search(r'<ol class="steps12">(.*?)</ol>', page_html, flags=re.S)
                self.assertIsNotNone(m, f"{lang}/{page}: нет списка шагов")
                names = re.findall(r'<span class="n">\d+</span>([^<]+)', m.group(1))
                numbers = re.findall(r'<span class="n">(\d+)</span>', m.group(1))
                self.assertEqual(len(names), 12, f"{lang}/{page}: не 12 шагов")
                self.assertEqual(numbers, [str(i) for i in range(1, 13)],
                                 f"{lang}/{page}: нумерация шагов не 1–12")
                self.assertEqual(len(set(names)), len(names),
                                 f"{lang}/{page}: дубли имён шагов: {names}")

    def test_phase_grid_matches_step_numbers(self):
        """Сетка фаз согласована с нумерацией шагов 1–12 (ревью PRO-61):
        раньше сетка говорила «0–3/4–6/7–9/10–11» при шагах 1–12."""
        expected = [("1", "4"), ("5", "7"), ("8", "10"), ("11", "12")]
        for lang in ("ru", "en"):
            page = self.built[(lang, "demo")]
            ranges = re.findall(r'<div class="tl-cell[^"]*"><b>(\d+)–(\d+) · ', page)
            self.assertEqual(ranges, expected,
                             f"{lang}/demo: сетка фаз не согласована с шагами 1–12")

    def test_econ_svg_labels_meaningful(self):
        """Подписи под столбцами экономики — содержательные, а не дубль числа
        над столбцом (ревью PRO-61: «$29»/«~25%» вместо «ARPU платящего / мес»
        и «инференс + инфра ~25%»)."""
        expected0 = {"ru": "ARPU платящего / мес", "en": "payer ARPU / mo"}
        for lang in ("ru", "en"):
            page = self.built[(lang, "demo")]
            labels = re.findall(
                r'<text x="\d+" y="252"[^>]*><tspan lang="%s">([^<]+)</tspan>' % lang, page)
            self.assertEqual(len(labels), 4, f"{lang}/demo: не 4 подписи столбцов")
            self.assertEqual(labels[0], expected0[lang],
                             f"{lang}/demo: подпись ARPU: {labels[0]!r}")
            self.assertIn("инференс" if lang == "ru" else "infra", labels[1],
                          f"{lang}/demo: подпись переменных затрат: {labels[1]!r}")
            for lab in labels:
                self.assertIsNone(re.fullmatch(r"[~$−-]?[\d.,]+%?", lab),
                                  f"{lang}/demo: подпись дублирует число: {lab!r}")

    def test_breakeven_consistent_on_page_and_from_target(self):
        """Брейк-евен на странице — одно число и считается от цели
        «MRR ≥ $N» плана проверки, а не от факта модели недели 12
        (ревью PRO-61: в SVG 71 от $1 537, в цитате six-pager 69 от $1 500)."""
        v06 = (DEMO / "outputs" / "06_validation_plan.md").read_text(encoding="utf-8")
        m = re.search(r"MRR ≥ \$([\d ]+)", v06)
        self.assertIsNotNone(m, "в 06_validation_plan.md нет цели «MRR ≥ $N»")
        target = int(m.group(1).replace(" ", ""))
        ue = json.loads((DEMO / "calcs.json").read_text(encoding="utf-8"))["unit_econ"]
        cm = float(ue["arpu"]) * (1 - float(ue["vc_share"]))
        want = str(math.ceil(target / cm))
        for lang, word in (("ru", "брейк-евен"), ("en", "break-even")):
            text = visible_text(self.built[(lang, "demo")])
            nums = re.findall(rf"{word} [≈ ]*(\d+)", text)
            self.assertEqual(set(nums), {want},
                             f"{lang}/demo: числа брейк-евена на странице расходятся: {nums}")

    def test_beta_expectation_sentence_boundary(self):
        """Фраза «Ожидание беты» не склеена: после скобки «(…12 недель)» —
        точка и новое предложение «Факт модели нед. 12 …» (ревью PRO-61)."""
        ru = visible_text(self.built[("ru", "demo")])
        self.assertNotRegex(ru, r"недель\) факт")
        self.assertRegex(ru, r"недель\)\. Факт модели")
        en = visible_text(self.built[("en", "demo")])
        self.assertNotRegex(en, r"weeks\) the week-")
        self.assertRegex(en, r"weeks\)\. The week-")


class TestNoJsVisibility(SiteI18NBase):
    def test_counters_are_static(self):
        """Счётчики демо — в статическом HTML, а не «0» до загрузки JS."""
        ru = self.built[("ru", "demo")]
        self.assertIn(f"<b>{n_source_files()}</b>", ru)
        self.assertIn(f"<b>{demo_claims()['total']}</b>", ru)
        self.assertNotIn("0 шагов", ru)

    def test_quick_start_static_text(self):
        for lang in ("ru", "en"):
            # команды быстрого старта — это и есть видимый контент <pre>/<code>;
            # без JS они видны, поэтому здесь код не исключаем
            text = visible_text(self.built[(lang, "help")], skip_code=False)
            self.assertIn("git clone", text, lang)
            self.assertIn("./scripts/install.sh", text, lang)
            self.assertIn("pfs doctor", text, lang)

    def test_copy_buttons_have_visible_fallback(self):
        """Текст команды лежит в <code> рядом с кнопкой — без JS команда видна."""
        for lang in ("ru", "en"):
            page = self.built[(lang, "help")]
            self.assertGreaterEqual(page.count("data-copy="), 4, lang)
            self.assertGreaterEqual(page.count("<code>"), 4, lang)


class TestCommittedParity(SiteI18NBase):
    def test_committed_pages_match_build(self):
        for page in PAGES:
            committed_ru = (SITE / f"{page}.html").read_text(encoding="utf-8")
            committed_en = (SITE / "en" / f"{page}.html").read_text(encoding="utf-8")
            self.assertEqual(self.built[("ru", page)], committed_ru,
                             f"site/{page}.html не совпадает со сборкой — "
                             f"перезапустите scripts/build_site.py")
            self.assertEqual(self.built[("en", page)], committed_en,
                             f"site/en/{page}.html не совпадает со сборкой — "
                             f"перезапустите scripts/build_site.py")

    def test_referenced_screenshots_exist(self):
        for name in ("cv_landing_ru.jpg", "cv_dash_ru.jpg",
                     "cv_landing_en.jpg", "cv_dash_en.jpg"):
            self.assertTrue((SITE / "assets" / name).exists(), name)



class TestLoudFailures(unittest.TestCase):
    """Испорченные данные демо-проекта — BuildError, а не тихий ноль на сайте."""

    def setUp(self):
        self.mod = load_module()

    def _demo(self, v06: str | None = None, decision: dict | None = None) -> None:
        tmp = Path(tempfile.mkdtemp(prefix="pfs-i18n-loud-"))
        demo = tmp / "demo"
        (demo / "outputs").mkdir(parents=True)
        v06_default = (
            "# 06 · План проверки — CVStart hosted beta (90 дней)\n"
            "Запуск hosted-беты: нед. 12 — **50–60 платящих (модель: 53), "
            "MRR ≥ $1 500**.\n"
            "**90 дней**. Факт модели нед. 12 [S008]: 32 603 посетителей → "
            "1 793 регистрации → 1 111 активаций → 53 платящих (MRR $1 537).\n"
            "- **Продолжить**: paid ≥ 40 к нед. 12, activation ≥ 50%, "
            "churn платящих ≤ 10%/мес\n"
            "- **Изменить**: paid 20–40 → пересобрать тир/цену ($19?)\n"
            "- **Остановить**: paid < 20 к нед. 12 при activation < 35%\n"
            "## Нежелательные последствия (контрметрики)\n"
            "- Жалобы на приватность/GDPR-запросы > 5 шт\n"
            "- Инференс-затраты free-тира > $200/мес\n"
            "- NPS беты < 30\n")
        (demo / "outputs" / "06_validation_plan.md").write_text(
            v06 if v06 is not None else v06_default, encoding="utf-8")
        d_default = {
            "id": "D001",
            "decision": "Запустить вариант B: hosted freemium SaaS "
                        "(Free BYOK / Pro $12 / Unlimited $29); 90-дневная бета",
            "grounds": ["C005"],
            "metrics": [{"name": "платящие hosted-беты", "baseline": "0",
                         "target": ">=40", "by": "2027-02-10"}],
            "review": {"date": "2027-02-10", "triggers": ["paid < 20"]},
            "commitments": [{"id": "K1", "what": "hosted beta в 3 EN-гео (US/EU)",
                             "due": "к 2026-12-15", "status": "open"}],
        }
        (demo / ("claims" + ".jsonl")).write_text(
            json.dumps({"id": "C005", "kind": "fact", "grade": "C",
                        "text": "Рынок resume builders: коридор оценок $1,2–2,4 млрд (2024–2025); "
                                "AI-подсегмент $1,3→1,47 млрд, CAGR 13,1%",
                        "sources": ["S006"]}, ensure_ascii=False) + "\n", encoding="utf-8")
        (demo / ("decisions" + ".jsonl")).write_text(json.dumps(
            decision if decision is not None else d_default,
            ensure_ascii=False) + "\n", encoding="utf-8")
        self.mod.DEMO = demo

    def test_missing_funnel_is_loud(self):
        self._demo(v06="# 06 · План проверки — бета (90 дней)\nворонки нет\n")
        with self.assertRaisesRegex(self.mod.BuildError, "воронк"):
            self.mod.validation_data()

    def test_missing_expectation_range_is_loud(self):
        self._demo(v06="# 06 · План проверки — бета (90 дней)\n"
                       "32 603 посетителей → 1 793 регистрации → 1 111 активаций → "
                       "53 платящих (MRR $1 537)\n"
                       "- **Продолжить**: paid ≥ 40 к нед. 12, activation ≥ 50%, "
                       "churn платящих ≤ 10%/мес\n"
                       "- **Изменить**: paid 20–40 → пересобрать тир/цену ($19?)\n"
                       "- **Остановить**: paid < 20 к нед. 12 при activation < 35%\n"
                       "## Контрметрики\n"
                       "- GDPR-запросы > 5 шт\n"
                       "- Инференс-затраты free-тира > $200/мес\n"
                       "- NPS беты < 30\n")
        with self.assertRaisesRegex(self.mod.BuildError, "диапазона"):
            self.mod.validation_data()

    def test_missing_counter_metrics_is_loud(self):
        self._demo(v06="# 06 · План проверки — бета (90 дней)\n"
                       "Запуск hosted-беты: нед. 12 — **50–60 платящих (модель: 53)**.\n"
                       "32 603 посетителей → 1 793 регистрации → 1 111 активаций → "
                       "53 платящих (MRR $1 537)\n"
                       "- **Продолжить**: paid ≥ 40 к нед. 12, activation ≥ 50%, "
                       "churn платящих ≤ 10%/мес\n"
                       "- **Изменить**: paid 20–40 → пересобрать тир/цену ($19?)\n"
                       "- **Остановить**: paid < 20 к нед. 12 при activation < 35%\n"
                       "## Контрметрики\n"
                       "- Инференс-затраты free-тира > $200/мес\n")
        with self.assertRaisesRegex(self.mod.BuildError, "контрметрики"):
            self.mod.validation_data()

    def test_missing_mrr_target_is_loud(self):
        """Без цели «MRR ≥ $N» брейк-евен не от чего считать — сборка падает громко
        (ревью PRO-61: BREAKEVEN считали от факта недели 12)."""
        self._demo(v06="# 06 · План проверки — бета (90 дней)\n"
                       "Запуск hosted-беты: нед. 12 — **50–60 платящих (модель: 53)**.\n"
                       "32 603 посетителей → 1 793 регистрации → 1 111 активаций → "
                       "53 платящих (MRR $1 537)\n"
                       "- **Продолжить**: paid ≥ 40 к нед. 12, activation ≥ 50%, "
                       "churn платящих ≤ 10%/мес\n"
                       "- **Изменить**: paid 20–40 → пересобрать тир/цену ($19?)\n"
                       "- **Остановить**: paid < 20 к нед. 12 при activation < 35%\n"
                       "## Контрметрики\n"
                       "- GDPR-запросы > 5 шт\n"
                       "- Инференс-затраты free-тира > $200/мес\n"
                       "- NPS беты < 30\n")
        with self.assertRaisesRegex(self.mod.BuildError, "MRR"):
            self.mod.validation_data()

    def test_missing_threshold_is_loud(self):
        self._demo(v06="# 06 · План проверки — бета (90 дней)\n"
                       "32 603 посетителей → 1 793 регистрации → 1 111 активаций → "
                       "53 платящих (MRR $1 537)\n")
        with self.assertRaisesRegex(self.mod.BuildError, "порог"):
            self.mod.validation_data()

    def test_missing_metrics_is_loud(self):
        self._demo(decision={"id": "D001", "decision": "Запустить вариант B: hosted",
                             "review": {"date": "2027-02-10", "triggers": []},
                             "commitments": []})
        with self.assertRaisesRegex(self.mod.BuildError, "метрик"):
            self.mod.decision_data()

    def test_beta_days_mismatch_is_loud(self):
        self._demo(decision={"id": "D001",
                             "decision": "Запустить вариант B: hosted freemium SaaS "
                             "(Free BYOK / Pro $12 / Unlimited $29); 60-дневная бета",
                             "metrics": [{"name": "m", "baseline": "0", "target": ">=40",
                                          "by": "2027-02-10"}],
                             "review": {"date": "2027-02-10", "triggers": []},
                             "commitments": []})
        with self.assertRaisesRegex(self.mod.BuildError, "дней"):
            self.mod.decision_data()

    def test_missing_claim_translation_is_loud(self):
        self._demo()
        data_en = {"claims": {}, "triggers": [], "metric_target": ">=40",
                   "countermetrics": []}
        grounds = self.mod.decision_data()["grounds"]
        self.assertTrue(grounds)
        with self.assertRaisesRegex(self.mod.BuildError, "перевод"):
            self.mod.ground_claims(data_en)

    def test_translation_numbers_diverge_is_loud(self):
        self._demo()
        data_en = {"claims": {"C005": "Resume builder market: $9B (2024)"},
                   "triggers": [], "metric_target": ">=40", "countermetrics": []}
        with self.assertRaisesRegex(self.mod.BuildError, "расходятся"):
            self.mod.ground_claims(data_en)



class TestValidationCardsFromPlan(SiteI18NBase):
    """Карточки порогов demo собираются из 06_validation_plan.md, включая
    случай «платящих < 20 при activation >= 35%» из задачи PRO-61: раньше
    его не было ни в одном из трёх порогов."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        v06 = (DEMO / "outputs" / "06_validation_plan.md").read_text(encoding="utf-8")
        cont = re.search(r"paid ≥ (\d+) к нед\. (\d+), activation ≥ (\d+)%, "
                         r"churn платящих ≤ (\d+)%/мес", v06)
        adj = re.search(r"paid (\d+)–(\d+) → пересобрать тир/цену \(\$(\d+)\?\)", v06)
        stop = re.search(r"paid < (\d+) к нед\. \d+ при activation < (\d+)%", v06)
        rng = re.search(r"нед\. 12 — \*\*(\d+)–(\d+) платящих", v06)
        gdpr = re.search(r"GDPR-запросы > (\d+)", v06)
        infra = re.search(r"free-тира > \$(\d+)/мес", v06)
        nps = re.search(r"NPS беты < (\d+)", v06)
        assert cont and adj and stop and rng and gdpr and infra and nps, \
            "06_validation_plan.md не разобран тестом"
        cls.paid_ok = cont.group(1)
        cls.act_target = cont.group(3)
        cls.churn_max = cont.group(4)
        cls.adj_lo, cls.adj_hi = adj.group(1), adj.group(2)
        cls.stop_paid = stop.group(1)
        cls.stop_act = stop.group(2)
        cls.lo, cls.hi = rng.groups()
        cls.gdpr, cls.infra, cls.nps = gdpr.group(1), infra.group(1), nps.group(1)

    def test_adjust_card_covers_paid_below_stop_with_good_activation(self):
        """Кейс «paid < 20 при activation >= 35%» — не «стоп» и не «20-40»,
        а пересбор тира с продолжением беты (пробел из задачи PRO-61)."""
        ru = visible_text(self.built[("ru", "demo")])
        en = visible_text(self.built[("en", "demo")])
        self.assertIn(
            f"paid < {self.stop_paid} при activation ≥ {self.stop_act}%", ru)
        self.assertIn(
            f"paid < {self.stop_paid} with activation ≥ {self.stop_act}%", en)

    def test_threshold_lines_follow_plan(self):
        """Три карточки порогов: числа идут из плана проверки, а не набиты руками."""
        cont_line = (f"paid ≥ {self.paid_ok} · activation ≥ {self.act_target}% "
                     f"· churn ≤ {self.churn_max}%")
        adj_ru = (f"paid {self.adj_lo}–{self.adj_hi} · "
                  f"paid < {self.stop_paid} при activation ≥ {self.stop_act}%")
        adj_en = (f"paid {self.adj_lo}–{self.adj_hi} · "
                  f"paid < {self.stop_paid} with activation ≥ {self.stop_act}%")
        stop_ru = f"paid < {self.stop_paid} при activation < {self.stop_act}%"
        stop_en = f"paid < {self.stop_paid} with activation < {self.stop_act}%"
        for lang in ("ru", "en"):
            text = visible_text(self.built[(lang, "demo")])
            self.assertIn(cont_line, text, lang)
            self.assertIn(adj_ru if lang == "ru" else adj_en, text, lang)
            self.assertIn(stop_ru if lang == "ru" else stop_en, text, lang)

    def test_expectation_range_and_counter_metrics_from_plan(self):
        """Ожидание «50-60 платящих» и контрметрики 06 — на странице из реестра."""
        ru = visible_text(self.built[("ru", "demo")])
        en = visible_text(self.built[("en", "demo")])
        self.assertIn(f"{self.lo}–{self.hi}", ru)
        self.assertIn(f"{self.lo}–{self.hi}", en)
        self.assertIn(f"не более {self.gdpr}", ru)
        self.assertIn(f"не дороже ${self.infra}/мес", ru)
        self.assertIn(f"не ниже {self.nps}", ru)
        self.assertIn(f"no more than {self.gdpr}", en)
        self.assertIn(f"${self.infra}/mo", en)
        self.assertIn(f"no lower than {self.nps}", en)


# ---------- раунд 3 (ревью PRO-61): регистр закрывающих тегов, docstring,
# ---------- числа рынка из реестра ----------

class TestEndTagCase(unittest.TestCase):
    """Ревью PRO-61 r3 №1: фильтр языка сохраняет регистр закрывающих тегов.

    HTMLParser отдаёт имена тегов в нижнем регистре; открывающий тег выводится
    через get_starttag_text() с исходным регистром (<linearGradient>), поэтому
    reconstructed закрывающий </lineargradient> ломал парность SVG-тегов.
    """

    def setUp(self):
        self.mod = load_module()

    SVG_SRC = (
        '<!DOCTYPE html><html lang="ru"><head><meta charset="UTF-8"></head><body>'
        '<svg viewBox="0 0 40 40">'
        '<linearGradient id="lg"><stop offset="0" stop-color="#fff"/></linearGradient>'
        '<clipPath id="c"><rect x="1" y="2" width="3" height="4"/></clipPath>'
        '<g lang="en"><text>EN only</text></g>'
        '<text lang="ru">Русский текст</text>'
        '</svg></body></html>')

    def test_end_tags_keep_source_case(self):
        out = self.mod.filter_lang(self.SVG_SRC, "ru")
        self.assertIn('<linearGradient id="lg">', out)
        self.assertIn("</linearGradient>", out)
        self.assertIn('<clipPath id="c">', out)
        self.assertIn("</clipPath>", out)

    def test_no_lowercase_close_leaks(self):
        out = self.mod.filter_lang(self.SVG_SRC, "ru")
        self.assertNotIn("</lineargradient>", out)
        self.assertNotIn("</clippath>", out)

    def test_foreign_lang_block_removed(self):
        out = self.mod.filter_lang(self.SVG_SRC, "ru")
        self.assertNotIn("EN only", out)
        self.assertNotIn('<g lang="en">', out)

    def test_selfclosing_camel_tag_no_phantom_close(self):
        src = ('<html lang="ru"><body>'
               '<svg><feGaussianBlur stdDeviation="2"/></svg></body></html>')
        out = self.mod.filter_lang(src, "ru")
        self.assertIn('<feGaussianBlur stdDeviation="2"/>', out)
        self.assertNotIn("</feGaussianBlur>", out)

    def test_end_tag_case_after_removed_sibling(self):
        # соседний блок чужого языка удалён — парные теги живого блока целы
        src = ('<html lang="ru"><body><div lang="en"><linearGradient id="x">'
               "<text>en</text></linearGradient></div>"
               '<div lang="ru"><linearGradient id="y"><text>ru</text>'
               "</linearGradient></div></body></html>")
        out = self.mod.filter_lang(src, "ru")
        self.assertNotIn('id="x"', out)
        self.assertIn('<linearGradient id="y">', out)
        self.assertEqual(out.count("</linearGradient>"), 1)
        self.assertNotIn("</lineargradient>", out)


class TestEndTagCaseOnPages(SiteI18NBase):
    """Собранные страницы: camelCase-теги из site_src закрываются в том же регистре."""

    def test_camelcase_tags_close_same_case(self):
        # имена берём из исходников site_src, а не из собранных страниц:
        # так проверка не зависит от того, что ещё попадёт в теги страниц
        names = set()
        for src in sorted((ROOT / "site_src").glob("*.html")):
            for m in re.finditer(r"<([A-Za-z][^\s>/]*)[\s>/]",
                                 src.read_text(encoding="utf-8")):
                name = m.group(1)
                if any(c.isupper() for c in name[1:]):
                    names.add(name)
        self.assertTrue(names, "в site_src нет camelCase-тегов — проверка пустая")
        for key, page in self.built.items():
            for name in sorted(names):
                self.assertNotIn(f"</{name.lower()}>", page,
                                 f"{key}: </{name.lower()}> вместо </{name}>")
                self.assertIsNone(
                    re.search(rf"<{name.lower()}[\s>/]", page),
                    f"{key}: открывающий <{name.lower()}> в нижнем регистре")


class TestBuildDocstringScope(unittest.TestCase):
    """Ревью PRO-61 r3 №2: docstring не противоречит сборке — demo/help/materials
    генерируются из site_src + site/i18n, а не «остаются в прежней вёрстке»."""

    def test_docstring_describes_generated_pages(self):
        mod = load_module()
        doc = mod.__doc__ or ""
        self.assertNotIn("остаются в прежней вёрстке", doc,
                         "docstring говорит, что страницы не генерируются, "
                         "хотя PAGES_I18N их строит")
        self.assertIn("site_src", doc,
                      "docstring не описывает источник страниц site_src/")
        self.assertIn("i18n", doc, "docstring не описывает словари site/i18n")

    def test_every_page_in_i18n_has_source_and_dict(self):
        mod = load_module()
        ru = json.loads((ROOT / "site" / "i18n" / "ru.json").read_text(encoding="utf-8"))
        for page in mod.PAGES_I18N:
            self.assertTrue((ROOT / "site_src" / f"{page}.html").exists(),
                            f"нет site_src/{page}.html")
            self.assertIn(mod.PAGE_DICT[page], ru, page)


class TestMarketNumbersFromRegistry(unittest.TestCase):
    """Ревью PRO-61 r3 №3: MARKET_RU/MARKET_EN, AI_CAGR, RECRUIT_MARKET/RECRUIT_CAGR
    берутся из реестра утверждений демо (C005 и C011), а не набиты константами.
    Текст утверждения потерял структуру — сборка падает громко."""

    def setUp(self):
        self.mod = load_module()
        self.claims = _jsonl(DEMO / ("claims" + ".jsonl"))

    def test_values_parsed_from_registry(self):
        mk = self.mod.market_numbers(self.claims)
        self.assertEqual(mk["MARKET_RU"], "$1,2–2,4 млрд")
        self.assertEqual(mk["MARKET_EN"], "$1.2–2.4B")
        self.assertEqual(mk["AI_CAGR"], 13.1)
        self.assertEqual(mk["RECRUIT_MARKET"], 37.97)
        self.assertEqual(mk["RECRUIT_CAGR"], 7.1)

    def test_corridor_follows_registry(self):
        claims = [dict(c, text=c["text"].replace("$1,2–2,4 млрд", "$2,0–3,1 млрд"))
                  if c["id"] == "C005" else c for c in self.claims]
        mk = self.mod.market_numbers(claims)
        self.assertEqual(mk["MARKET_RU"], "$2,0–3,1 млрд")
        self.assertEqual(mk["MARKET_EN"], "$2.0–3.1B")

    def test_missing_c005_is_loud(self):
        with self.assertRaisesRegex(self.mod.BuildError, "C005"):
            self.mod.market_numbers([c for c in self.claims if c["id"] != "C005"])

    def test_missing_c011_is_loud(self):
        with self.assertRaisesRegex(self.mod.BuildError, "C011"):
            self.mod.market_numbers([c for c in self.claims if c["id"] != "C011"])

    def test_broken_c005_structure_is_loud(self):
        claims = [dict(c, text="Рынок resume builders: формулировка изменилась")
                  if c["id"] == "C005" else c for c in self.claims]
        with self.assertRaisesRegex(self.mod.BuildError, "C005"):
            self.mod.market_numbers(claims)

    def test_broken_c011_structure_is_loud(self):
        claims = [dict(c, text="Мировой рынок онлайн-рекрутинга: пересчитан")
                  if c["id"] == "C011" else c for c in self.claims]
        with self.assertRaisesRegex(self.mod.BuildError, "C011"):
            self.mod.market_numbers(claims)

    def test_page_values_reads_market_numbers(self):
        seen = []
        real = self.mod.market_numbers

        def spy(claims):
            seen.append(claims)
            return real(claims)

        self.mod.market_numbers = spy
        try:
            vals = self.mod.page_values()
        finally:
            self.mod.market_numbers = real
        self.assertTrue(seen, "page_values() не читает market_numbers()")
        self.assertEqual(vals["AI_CAGR"], ("pct1", 13.1))
        self.assertEqual(vals["RECRUIT_MARKET"], ("recruit", 37.97))
        self.assertEqual(vals["MARKET_RU"], ("str", "$1,2–2,4 млрд"))

    def test_market_kind_uses_parsed_pair(self):
        pair = ("$2,0–3,1 млрд", "$2.0–3.1B")
        self.assertEqual(self.mod.render_value("market", pair, "ru"), pair[0])
        self.assertEqual(self.mod.render_value("market", pair, "en"), pair[1])


class TestMarketNumbersOnPages(SiteI18NBase):
    """Числа рынка на собранных страницах = числа из реестра утверждений."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        rows = _jsonl(DEMO / ("claims" + ".jsonl"))
        c5 = next(c for c in rows if c["id"] == "C005")
        c11 = next(c for c in rows if c["id"] == "C011")
        cls.corridor_ru = re.search(r"\$[\d,]+–[\d,]+ млрд", c5["text"]).group(0)
        cls.ai_cagr = re.search(r"CAGR ([\d,]+)%", c5["text"]).group(1)
        cls.recruit_ru = re.search(r"\$[\d,]+ млрд", c11["text"]).group(0)
        cls.recruit_cagr = re.search(r"CAGR ([\d,]+)%", c11["text"]).group(1)

    def test_demo_market_tiles(self):
        ru = visible_text(self.built[("ru", "demo")])
        en = visible_text(self.built[("en", "demo")])
        self.assertIn(self.corridor_ru, ru)
        self.assertIn(f"{self.ai_cagr}%", ru)
        self.assertIn(self.recruit_ru, ru)
        self.assertIn(f"{self.recruit_cagr}%", ru)
        en_corridor = self.corridor_ru.replace(",", ".").replace(" млрд", "B")
        en_recruit = self.recruit_ru.replace(",", ".").replace(" млрд", "B")
        self.assertIn(en_corridor, en)
        self.assertIn(f"{self.ai_cagr.replace(',', '.')}%", en)
        self.assertIn(en_recruit, en)
        self.assertIn(f"{self.recruit_cagr.replace(',', '.')}%", en)

    def test_materials_market_mention(self):
        ru = visible_text(self.built[("ru", "materials")])
        self.assertIn(self.corridor_ru, ru)


if __name__ == "__main__":
    unittest.main()
