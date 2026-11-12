"""PRO-52: русский язык в выводе — нормализация названия проекта, стайлгайд STYLE_RU.md,
субагент editor и языковой линтер (banned_terms в quality_gate.json).

Запуск: python3 -m unittest tests.test_editor_style -v
"""
import os
import tempfile
import unittest
from pathlib import Path

TMP = tempfile.mkdtemp(prefix="pfs-test-pro52-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from tools.pfs import check, core, models, project  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
RAW_REQUEST = "Как вывести проекта на европейский рынок cvstart.org"
RAW_TITLE_MD = "Как вывести **проекта** на европейский рынок [cvstart.org](http://cvstart.org)"


class TitleNormalizationTests(unittest.TestCase):
    def test_illiterate_title_is_normalized_and_request_kept_verbatim(self):
        pdir = project.create(RAW_TITLE_MD, RAW_REQUEST, slug="pro52")
        meta = core.read_json(pdir / "project.json")
        title = meta["title"]
        # грамматика: «вывести проекта» → «вывести проект», без markdown
        self.assertNotIn("проекта", title)
        self.assertNotIn("**", title)
        self.assertNotIn("](http", title)
        self.assertIn("Как вывести проект на европейский рынок cvstart.org", title)
        # исходный запрос сохранён дословно — и в project.json, и в 00_brief
        self.assertEqual(meta["question"], RAW_REQUEST)
        brief = (pdir / "outputs" / "00_brief.md").read_text(encoding="utf-8")
        self.assertIn(RAW_REQUEST, brief)
        self.assertIn(f"# Бриф: {title}", brief)

    def test_clean_title_is_not_mangled(self):
        self.assertEqual(project.normalize_title("Вывод проекта на рынок Европы"),
                         "Вывод проекта на рынок Европы")
        self.assertEqual(project.normalize_title("какой-то  запрос   с пробелами"),
                         "Какой-то запрос с пробелами")
        self.assertEqual(project.normalize_title(""), "")


class StyleGuideTests(unittest.TestCase):
    def test_style_guide_exists_with_glossary_of_40_plus_terms(self):
        guide = REPO / "knowledge" / "templates" / "STYLE_RU.md"
        self.assertTrue(guide.is_file(), "нет knowledge/templates/STYLE_RU.md")
        text = guide.read_text(encoding="utf-8")
        rows = [l for l in text.splitlines()
                if l.startswith("|") and "---" not in l and set(l.strip()) != {"|"}]
        self.assertGreaterEqual(len(rows) - 1, 40,  # -1 строка заголовка таблицы
                                f"в глоссарии меньше 40 терминов: {len(rows) - 1}")
        for term in ("SERP", "гейт", "trial-trap", "answer-first", "BYOK", "тоннальность"):
            self.assertIn(term, text, f"{term}: нет в глоссарии STYLE_RU.md")


class EditorAgentTests(unittest.TestCase):
    def test_editor_agent_files_exist_and_are_cheap(self):
        claude = REPO / ".claude" / "agents" / "editor.md"
        opencode = REPO / ".opencode" / "agent" / "editor.md"
        self.assertTrue(claude.is_file(), "нет .claude/agents/editor.md")
        self.assertTrue(opencode.is_file(), "нет .opencode/agent/editor.md")
        for f in (claude, opencode):
            text = f.read_text(encoding="utf-8")
            self.assertIn("STYLE_RU", text, f"{f}: нет ссылки на стайлгайд")
            self.assertIn("check", text, f"{f}: нет повторного pfs check")
        self.assertIn("editor", models.AGENT_TASKS, "editor не в AGENT_TASKS (pfs models sync)")
        self.assertEqual(models.pick("editor")["tier"], "fast", "editor должен быть дешёвой моделью")


class LanguageLintTests(unittest.TestCase):
    DIRTY = "\n".join([
        "# Тест: six-pager",
        "**Запрос:** Как вывести проекта на рынок",
        "",
        "Тоннальность кампании позитивная. Гейт волны 1 пройден.",
        "Позиции в SERP выросли, а в OSS-ядре нет.",
        "SEO даёт трафик.",
    ])
    CLEAN = "\n".join([
        "# Тест: six-pager",
        "**Запрос:** Как вывести проект на рынок",
        "",
        "Тональность кампании позитивная. Контрольная точка волны 1 пройдена.",
        "Позиции в SERP (страница результатов поиска) выросли, а в открытом коде нет.",
        "SEO (поисковое продвижение) даёт трафик.",
    ])

    def lint(self, text: str) -> list[str]:
        pdir = project.create("Тест PRO-52 лингтер", "Почему падает удержание?", slug=f"lint{abs(hash(text)) % 10**8}")
        (pdir / "outputs" / "SIX_PAGER.md").write_text(text, encoding="utf-8")
        res = check.run(pdir)
        return res["warnings"]

    def test_dirty_sixpager_flags_banned_terms_and_undecoded_abbreviations(self):
        warns = self.lint(self.DIRTY)
        joined = " ".join(warns)
        self.assertIn("тоннальность", joined.lower())
        self.assertIn("гейт", joined.lower())
        self.assertIn("SERP", joined)
        self.assertIn("SEO", joined)
        self.assertIn("расшифровк", joined)

    def test_clean_sixpager_has_no_language_warnings(self):
        warns = self.lint(self.CLEAN)
        self.assertEqual([w for w in warns if "STYLE_RU" in w or "расшифров" in w], [],
                         f"языковые предупреждения на чистом документе: {warns}")

    def test_en_project_skips_russian_lint(self):
        pdir = project.create("EN lint test", "Why is retention dropping?", slug="lint-en", lang="en")
        (pdir / "outputs" / "SIX_PAGER.md").write_text(self.DIRTY, encoding="utf-8")
        res = check.run(pdir)
        self.assertEqual([w for w in res["warnings"] if "STYLE_RU" in w], [],
                         "RU-линтер не должен работать на EN-проекте")


if __name__ == "__main__":
    unittest.main()
