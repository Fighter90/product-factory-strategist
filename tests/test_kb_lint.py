"""PRO-60: pfs kb lint — контроль базы знаний (frontmatter, ссылки, теги, пустые разделы,
паритет RU/EN по разделам и объёму, совпадение id) и единообразие имён файлов.

Запуск: python3 -m unittest tests.test_kb_lint -v
"""
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

TMP = tempfile.mkdtemp(prefix="pfs-test-lint-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from tools.pfs import core, kb  # noqa: E402  # после установки env
from tools.pfs.core import PfsError  # noqa: E402


def _card(slug: str, *, lang: str = "ru", cid: str | None = None, body: str | None = None,
          related: str = "[]", tags: str | None = None, stages: str = "[intake]") -> str:
    cid = cid if cid is not None else ("M-" + slug)
    if tags is None:
        tags = '["тег-раз", "тег-два"]' if lang == "ru" else '["tag-one", "tag-two"]'
    if body is None:
        body = ("# Заголовок\n\n## Когда применять\nТекст первого раздела.\n\n"
                "## Суть\nТекст второго раздела.\n")
    fm = [f"id: {cid}", "title: Карта", "course: strategy", f"stages: {stages}",
          f"tags: {tags}", f"related: {related}"]
    if lang == "en":
        fm.append("lang: en")
    return f"---\n" + "\n".join(fm) + f"\n---\n{body}"


def _repo(ru: dict[str, str], en: dict[str, str] | None = None) -> Path:
    root = Path(tempfile.mkdtemp(prefix="pfs-test-lint-kb-"))
    (root / "methods").mkdir()
    for slug, text in ru.items():
        (root / "methods" / f"{slug}.md").write_text(text, encoding="utf-8")
    if en:
        (root / "methods_en").mkdir()
        for slug, text in en.items():
            (root / "methods_en" / f"{slug}.md").write_text(text, encoding="utf-8")
    return root


GOOD_RU = _card("alpha", related="[M-beta]")
GOOD_EN = _card("alpha", lang="en", related="[M-beta]",
                body="# Heading\n\n## When to use\nText of the first section.\n\n"
                     "## Core\nText of the second section.\n")
RU_BETA = _card("beta", related="[M-alpha]")


class LintSyntheticTests(unittest.TestCase):
    """Мини-репозиторий: каждая проверка lint ловит свой дефект."""

    def _lint(self, ru, en=None):
        with mock.patch.object(core, "KNOWLEDGE", _repo(ru, en)):
            return kb.lint()

    def test_clean_repo_no_problems(self):
        problems = self._lint({"alpha": GOOD_RU, "beta": RU_BETA},
                              {"alpha": GOOD_EN, "beta": _card("beta", lang="en", related="[M-alpha]",
                                                               body="# H\n\n## When to use\nText.\n\n## Core\nText.\n")})
        self.assertEqual(problems, [])

    def test_en_id_must_not_carry_en_suffix(self):
        bad = _card("alpha", lang="en", cid="M-alpha-en", related="[M-beta]",
                    body="# H\n\n## When to use\nText.\n\n## Core\nText.\n")
        problems = self._lint({"alpha": GOOD_RU, "beta": RU_BETA}, {"alpha": bad})
        self.assertTrue(any("M-alpha-en" in p for p in problems), problems)

    def test_en_card_requires_lang_field(self):
        bad = GOOD_EN.replace("lang: en\n", "")
        problems = self._lint({"alpha": GOOD_RU, "beta": RU_BETA}, {"alpha": bad})
        self.assertTrue(any("lang" in p for p in problems), problems)

    def test_filename_must_match_id_without_prefix(self):
        root = _repo({"alpha": GOOD_RU, "beta": RU_BETA}, {"alpha": GOOD_EN})
        (root / "methods" / "M-beta.md").write_text(RU_BETA, encoding="utf-8")
        (root / "methods" / "beta.md").unlink()
        with mock.patch.object(core, "KNOWLEDGE", root):
            problems = kb.lint()
        self.assertTrue(any("M-beta" in p and "имя" in p for p in problems), problems)

    def test_broken_wiki_link_detected(self):
        bad = GOOD_RU.replace("[[", "[[").replace("related: [M-beta]", "related: [M-beta]") + \
            "\n## Связанные карты\n[[M-ghost]]\n"
        problems = self._lint({"alpha": bad, "beta": RU_BETA}, {"alpha": GOOD_EN})
        self.assertTrue(any("M-ghost" in p for p in problems), problems)

    def test_related_pointing_to_missing_card(self):
        bad = GOOD_RU.replace("related: [M-beta]", "related: [M-nope]")
        problems = self._lint({"alpha": bad, "beta": RU_BETA}, {"alpha": GOOD_EN})
        self.assertTrue(any("M-nope" in p for p in problems), problems)

    def test_duplicate_tags(self):
        bad = GOOD_RU.replace('["тег-раз", "тег-два"]', '["тег-раз", "тег-раз"]')
        problems = self._lint({"alpha": bad, "beta": RU_BETA}, {"alpha": GOOD_EN})
        self.assertTrue(any("тег-раз" in p for p in problems), problems)

    def test_empty_h2_section(self):
        bad = GOOD_RU + "\n## Пустой раздел\n"
        problems = self._lint({"alpha": bad, "beta": RU_BETA}, {"alpha": GOOD_EN})
        self.assertTrue(any("Пустой раздел" in p or "пуст" in p.lower() for p in problems), problems)

    def test_ru_en_id_parity(self):
        problems = self._lint({"alpha": GOOD_RU, "beta": RU_BETA}, {"alpha": GOOD_EN})
        self.assertTrue(any("M-beta" in p for p in problems), problems)

    def test_en_volume_below_80_percent(self):
        thin = GOOD_EN.replace(
            "# Heading\n\n## When to use\nText of the first section.\n\n## Core\nText of the second section.\n",
            "# H\n\n## When to use\nx\n\n## Core\nx\n")
        problems = self._lint({"alpha": GOOD_RU, "beta": RU_BETA}, {"alpha": thin})
        self.assertTrue(any("объём" in p for p in problems), problems)

    def test_en_section_count_must_mirror_ru(self):
        fewer = _card("alpha", lang="en", related="[M-beta]",
                      body="# H\n\n## When to use\nSingle section while RU has two.\n")
        problems = self._lint({"alpha": GOOD_RU, "beta": RU_BETA}, {"alpha": fewer})
        self.assertTrue(any("раздел" in p for p in problems), problems)

    def test_no_ru_version_line_in_en(self):
        bad = GOOD_EN + "\n**RU-версия:** `knowledge/methods/alpha.md`.\n"
        problems = self._lint({"alpha": GOOD_RU, "beta": RU_BETA}, {"alpha": bad})
        self.assertTrue(any("RU-версия" in p for p in problems), problems)

    def test_en_tags_en_summary_forbidden(self):
        bad = GOOD_EN.replace('["tag-one", "tag-two"]', "[en, summary]")
        problems = self._lint({"alpha": GOOD_RU, "beta": RU_BETA}, {"alpha": bad})
        self.assertTrue(any("summary" in p or "en" in p for p in problems), problems)


class LintRealRepoTests(unittest.TestCase):
    """Реальная база: паритет, имена файлов, отсутствие «RU-версии» в EN."""

    def test_real_kb_lint_clean(self):
        problems = kb.lint()
        self.assertEqual(problems, [], "\n".join(problems[:20]))

    def test_real_kb_filenames_uniform(self):
        for d in ("methods", "methods_en"):
            for p in (core.KNOWLEDGE / d).glob("*.md"):
                self.assertFalse(p.stem.startswith("M-"), p)
                self.assertFalse(p.stem.endswith("-en"), p)

    def test_real_kb_no_double_roman_typo(self):
        for p in (core.KNOWLEDGE / "methods").glob("*.md"):
            self.assertNotIn("Двойной роман", p.read_text(encoding="utf-8"), p)


class CardPathLangTests(unittest.TestCase):
    def test_card_path_en_by_lang_flag(self):
        p = kb.card_path("M-jtbd", lang="en")
        self.assertTrue(p.exists())
        self.assertEqual(p.parent.name, "methods_en")
        self.assertIn("lang: en", p.read_text(encoding="utf-8"))

    def test_card_path_legacy_en_suffix(self):
        p = kb.card_path("M-jtbd-en")
        self.assertEqual(p.parent.name, "methods_en")

    def test_card_path_en_missing_raises(self):
        with self.assertRaises(PfsError):
            kb.card_path("M-totally-absent", lang="en")


class IndexEnTests(unittest.TestCase):
    def test_build_index_en_writes_file(self):
        with mock.patch.object(core, "KNOWLEDGE",
                               _repo({"alpha": GOOD_RU, "beta": RU_BETA},
                                     {"alpha": GOOD_EN, "beta": _card("beta", lang="en", related="[M-alpha]",
                                                                      body="# H\n\n## When to use\nText.\n\n## Core\nText.\n")})):
            text = kb.build_index_en()
        self.assertIn("INDEX EN", text)
        self.assertIn("methods_en/alpha.md", text)
        self.assertIn("`M-alpha`", text)


if __name__ == "__main__":
    unittest.main()
