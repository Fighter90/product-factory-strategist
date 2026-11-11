"""PRO-60: pfs kb lint — целостность базы знаний (frontmatter, [[ссылки]], теги, пустые
разделы, паритет RU/EN по разделам и объёму, совпадение id) и INDEX_EN.md.

Запуск: python3 -m unittest tests.test_kb_lint -v
"""
import os
import re
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

TMP = tempfile.mkdtemp(prefix="pfs-test-kblint-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from tools.pfs import core, kb  # noqa: E402
from tools.pfs.core import PfsError  # noqa: E402

RU_FM = ("---\nid: M-alpha\ntitle: Карта А\nlang: ru\ncourse: strategy\n"
         "stages: [intake]\ntags: [тег-а, тег-б]\nrelated: [M-beta]\n---\n")
EN_FM = ("---\nid: M-alpha\ntitle: Map A\nlang: en\ncourse: strategy\n"
         "stages: [intake]\ntags: [tag-a, tag-b]\nrelated: [M-beta]\n---\n")
RU_BODY = ("# Карта А\n\n## Когда применять\n\nЗачем карта нужна.\n\n"
           "## Суть\n\nСуть метода: правило `UE = LTV - CAC`.\n\n"
           "## Связанные карты\n\n[[M-beta]] и [[M-alpha]].\n")
EN_BODY = ("# Map A\n\n## When to apply\n\nWhy this map exists.\n\n"
           "## Core idea\n\nThe core rule: `UE = LTV - CAC`.\n\n"
           "## Related maps\n\n[[M-beta]] and [[M-alpha]].\n")


def make_pair(root: Path, ru_body: str = RU_BODY, en_body: str = EN_BODY,
              ru_fm: str = RU_FM, en_fm: str = EN_FM, ru_name: str = "alpha.md",
              en_name: str = "alpha.md", en_skip: bool = False) -> None:
    (root / "methods").mkdir(parents=True, exist_ok=True)
    (root / "methods" / ru_name).write_text(ru_fm + ru_body, encoding="utf-8")
    (root / "methods").mkdir(parents=True, exist_ok=True)
    (root / "methods" / "beta.md").write_text(
        "---\nid: M-beta\ntitle: Карта Б\nlang: ru\ncourse: strategy\nstages: [research]\n"
        "tags: [тег-в]\nrelated: [M-alpha]\n---\n# Б\n\n## Когда применять\n\nБ.\n", encoding="utf-8")
    (root / "methods_en").mkdir(parents=True, exist_ok=True)
    (root / "methods_en" / "beta.md").write_text(
        "---\nid: M-beta\ntitle: Map B\nlang: en\ncourse: strategy\nstages: [research]\n"
        "tags: [tag-c]\nrelated: [M-alpha]\n---\n# B\n\n## When to apply\n\nB.\n", encoding="utf-8")
    if not en_skip:
        (root / "methods_en" / en_name).write_text(en_fm + en_body, encoding="utf-8")


class KbLintSyntheticTests(unittest.TestCase):
    def lint(self, **kwargs) -> list[str]:
        root = Path(tempfile.mkdtemp(prefix="pfs-test-kblint-case-"))
        make_pair(root, **kwargs)
        with mock.patch.object(core, "KNOWLEDGE", root):
            return kb.lint()

    def test_clean_pair_has_no_problems(self):
        self.assertEqual(self.lint(), [])

    def test_missing_required_frontmatter_key(self):
        problems = self.lint(ru_fm=RU_FM.replace("lang: ru\n", ""))
        self.assertTrue(any("M-alpha" in p and "lang" in p for p in problems), problems)

    def test_id_without_m_prefix_and_en_id_mismatch(self):
        problems = self.lint(en_fm=EN_FM.replace("id: M-alpha", "id: M-alpha-en"))
        self.assertTrue(any("M-alpha" in p and "-en" in p for p in problems), problems)
        problems = self.lint(ru_fm=RU_FM.replace("id: M-alpha", "id: alpha"))
        self.assertTrue(any("M-" in p and "alpha.md" in p for p in problems), problems)

    def test_duplicate_tags(self):
        problems = self.lint(ru_fm=RU_FM.replace("tags: [тег-а, тег-б]", "tags: [тег-а, тег-а]"))
        self.assertTrue(any("тег-а" in p and "M-alpha" in p for p in problems), problems)

    def test_broken_wikilink_and_related(self):
        problems = self.lint(ru_body=RU_BODY.replace("[[M-beta]]", "[[M-missing]]"))
        self.assertTrue(any("M-missing" in p for p in problems), problems)
        problems = self.lint(ru_fm=RU_FM.replace("related: [M-beta]", "related: [M-ghost]"))
        self.assertTrue(any("M-ghost" in p for p in problems), problems)

    def test_empty_section(self):
        problems = self.lint(ru_body=RU_BODY.replace("Суть метода: правило `UE = LTV - CAC`.\n", ""))
        self.assertTrue(any("Суть" in p and "M-alpha" in p for p in problems), problems)

    def test_missing_en_twin(self):
        problems = self.lint(en_skip=True)
        self.assertTrue(any("alpha.md" in p for p in problems), problems)

    def test_en_volume_below_80_percent(self):
        short = EN_BODY.replace("The core rule: `UE = LTV - CAC`.", "Rule.")
        problems = self.lint(en_body=short)
        self.assertTrue(any("80%" in p and "alpha.md" in p for p in problems), problems)

    def test_en_section_parity_count_order_and_known_headings(self):
        problems = self.lint(en_body=EN_BODY.replace("## Core idea\n\n", "").replace(
            "The core rule: `UE = LTV - CAC`.\n\n", ""))
        self.assertTrue(any("раздел" in p and "M-alpha" in p for p in problems), problems)
        problems = self.lint(en_body=EN_BODY.replace("## Core idea", "## Gist"))
        self.assertTrue(any("Gist" in p for p in problems), problems)

    def test_ru_version_line_forbidden_in_en(self):
        problems = self.lint(en_body=EN_BODY + "\n**RU-версия:** `knowledge/methods/alpha.md`\n")
        self.assertTrue(any("RU-версия" in p for p in problems), problems)

    def test_filename_uniformity(self):
        problems = self.lint(ru_name="M-alpha.md", en_name="M-alpha.md")
        self.assertTrue(any("M-alpha.md" in p and "префикс" in p for p in problems), problems)
        problems = self.lint(en_name="alpha-en.md", en_skip=False)
        self.assertTrue(any("alpha-en.md" in p for p in problems), problems)

    def test_lang_field_values(self):
        problems = self.lint(en_fm=EN_FM.replace("lang: en", "lang: ru"))
        self.assertTrue(any("lang" in p and "alpha.md" in p for p in problems), problems)

    def test_real_knowledge_base_structure_now(self):
        """Единая схема имён уже применена: без M-префикса и без -en-суффикса."""
        for p in (core.KNOWLEDGE / "methods").glob("*.md"):
            self.assertFalse(p.name.startswith("M-"), p.name)
        for p in (core.KNOWLEDGE / "methods_en").glob("*.md"):
            self.assertFalse(p.name.startswith("M-"), p.name)
            self.assertFalse(p.stem.endswith("-en"), p.name)
            self.assertTrue((core.KNOWLEDGE / "methods" / p.name).exists(), p.name)


class KbCardPathEnTests(unittest.TestCase):
    def test_en_suffix_resolves_to_methods_en_twin(self):
        root = Path(tempfile.mkdtemp(prefix="pfs-test-kblint-path-"))
        make_pair(root)
        with mock.patch.object(core, "KNOWLEDGE", root):
            self.assertTrue(kb.card_path("M-alpha").is_relative_to(root / "methods"))
            en = kb.card_path("M-alpha-en")
            self.assertEqual(en.parent.name, "methods_en")
            self.assertEqual(en.name, "alpha.md")
        root2 = Path(tempfile.mkdtemp(prefix="pfs-test-kblint-path2-"))
        make_pair(root2, en_skip=True)
        with mock.patch.object(core, "KNOWLEDGE", root2):
            with self.assertRaises(PfsError):
                kb.card_path("M-alpha-en")

    def test_real_kb_en_cards_share_id_with_ru_and_have_lang(self):
        for p in (core.KNOWLEDGE / "methods_en").glob("*.md"):
            meta = kb.frontmatter(p.read_text(encoding="utf-8"))
            self.assertEqual(meta.get("lang"), "en", p.name)
            self.assertFalse(str(meta.get("id", "")).endswith("-en"), p.name)
            ru = core.KNOWLEDGE / "methods" / p.name
            if ru.exists():
                ru_meta = kb.frontmatter(ru.read_text(encoding="utf-8"))
                self.assertEqual(meta.get("id"), ru_meta.get("id"), p.name)


class KbLintRealKbTests(unittest.TestCase):
    """PRO-60: реальная база знаний зелёная — lint пустой, CLI выходит с 0."""

    def test_lint_clean_on_real_kb(self):
        self.assertEqual(kb.lint(), [])

    def test_cli_kb_lint_exits_zero(self):
        import subprocess
        r = subprocess.run([sys.executable, "-m", "tools.pfs", "kb", "lint"],
                           cwd=core.ROOT, capture_output=True, text=True,
                           env={**os.environ, "PFS_PROJECTS_DIR": tempfile.mkdtemp(prefix="pfs-lint-cli-")})
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("проблем: 0", r.stdout)

    def test_new_strategy_cards_have_en_mirrors(self):
        for cid in ("M-six-pager-etalon", "M-committee-style", "M-tariff-ladder", "M-gtm-new-market",
                    "M-paid-retention", "M-message-house", "M-scenario-modeling", "M-weighted-scoring"):
            p = kb.card_path(cid + "-en")
            meta = kb.frontmatter(p.read_text(encoding="utf-8"))
            self.assertEqual(meta.get("id"), cid, p.name)
            self.assertEqual(meta.get("lang"), "en", p.name)

    def test_stage_cards_reference_existing_ids(self):
        ids = {c.get("id") for c in kb.cards()}
        for stage, cards in kb.STAGE_CARDS.items():
            for cid in cards:
                self.assertIn(cid, ids, f"{stage}: {cid}")


class KbLintStagesAndEncodingTests(unittest.TestCase):
    """PRO-60, раунд 3: stages без шагов процесса, байты U+FFFD в картах и INDEX, счётчики в доках."""

    def lint(self, **kwargs) -> tuple[list[str], Path]:
        root = Path(tempfile.mkdtemp(prefix="pfs-test-kblint3-"))
        make_pair(root, **kwargs)
        with mock.patch.object(core, "KNOWLEDGE", root):
            return kb.lint(), root

    def test_stages_without_process_step_flagged(self):
        problems, _ = self.lint(ru_fm=RU_FM.replace("stages: [intake]", "stages: [review, decision]"))
        self.assertTrue(any("stages" in p and "M-alpha" in p for p in problems), problems)

    def test_stages_with_valid_step_among_extras_pass(self):
        problems, _ = self.lint(ru_fm=RU_FM.replace("stages: [intake]", "stages: [strategy, review, decision]"))
        self.assertFalse(any("stages" in p for p in problems), problems)

    def test_replacement_char_in_card_body_flagged(self):
        problems, _ = self.lint(ru_body=RU_BODY.replace("Зачем карта нужна.", "Позиционир\ufffdвание."))
        self.assertTrue(any("U+FFFD" in p and "alpha" in p for p in problems), problems)

    def test_replacement_char_in_card_title_flagged(self):
        problems, _ = self.lint(ru_fm=RU_FM.replace("title: Карта А", "title: Позиционир\ufffdвание"))
        self.assertTrue(any("U+FFFD" in p for p in problems), problems)

    def test_replacement_char_in_index_flagged(self):
        _, root = self.lint()
        (root / "INDEX.md").write_text(
            "# Навигация\n\n- [Позиционир\ufffdвание по Dunford](methods/alpha.md) `M-alpha`\n",
            encoding="utf-8")
        with mock.patch.object(core, "KNOWLEDGE", root):
            problems = kb.lint()
        self.assertTrue(any("INDEX.md" in p and "U+FFFD" in p for p in problems), problems)

    def test_real_index_files_have_no_replacement_chars(self):
        for name in ("INDEX.md", "INDEX_EN.md"):
            text = (core.KNOWLEDGE / name).read_text(encoding="utf-8")
            self.assertNotIn("\ufffd", text, name)

    def test_committee_style_listed_in_step_sections(self):
        """Карта для комитета есть в шагах INDEX (RU и EN), а не только в списке курсов."""
        with mock.patch.object(core, "KNOWLEDGE", core.KNOWLEDGE):
            text, problems = kb.build_index()
            text_en, problems_en = kb.build_index_en()
        self.assertEqual(problems, [])
        self.assertEqual(problems_en, [])
        self.assertNotIn("\ufffd", text)
        strategy_part = text.split("## Стратегия (`strategy`)")[1].split("## ")[0]
        self.assertIn("`M-committee-style`", strategy_part)
        strategy_part_en = text_en.split("## Strategy (`strategy`)")[1].split("## ")[0]
        self.assertIn("`M-committee-style`", strategy_part_en)


class KbDocsCardCountsTests(unittest.TestCase):
    """PRO-60, раунд 3: счётчики карт в документах — из одного источника (база знаний), не вручную."""

    COUNTS = [  # (файл, [(паттерн числа, "ru" | "en" | "ru_en")])
        ("README.md", [(r"(\d+) карт по категориям", "ru"),
                       (r"\((\d+) карт RU\)", "ru"),
                       (r"(\d+) EN-зеркал", "en")]),
        ("docs/COMPLIANCE.md", [(r"(\d+) карт RU", "ru"), (r"(\d+) EN-зеркал", "en")]),
        ("docs/HELP.md", [(r"(\d+) карт методов \(RU\)", "ru"), (r"(\d+) EN-зеркал", "en")]),
        ("docs/HELP_EN.md", [(r"(\d+) method cards \(RU\)", "ru"), (r"(\d+) EN mirrors", "en")]),
        ("docs/SUBMISSION.md", [(r"(\d+) карт(?: RU| \(RU\))?", "ru"), (r"(\d+) EN-зеркал", "en")]),
        ("docs/lovable-brief.md", [(r"(\d+) карт знаний", "ru"), (r"(\d+)\+(\d+) карт", "ru_en"),
                                   (r"(\d+) карт \(\+", "ru"), (r"(\d+) EN-зеркал", "en")]),
        ("site/help.html", [(r"(\d+) карт[а-яё]*", "ru"), (r"(\d+) cards", "ru")]),
    ]

    def test_claimed_counts_match_knowledge_base(self):
        ru_n = len(list((core.KNOWLEDGE / "methods").glob("*.md")))
        en_n = len(list((core.KNOWLEDGE / "methods_en").glob("*.md")))
        expected = {"ru": ru_n, "en": en_n}
        for rel, pats in self.COUNTS:
            text = (core.ROOT / rel).read_text(encoding="utf-8")
            for pat, kind in pats:
                matches = list(re.finditer(pat, text))
                self.assertTrue(matches, f"{rel}: нет совпадений для {pat}")
                for m in matches:
                    if kind == "ru_en":
                        self.assertEqual(int(m.group(1)), ru_n, f"{rel}: «{m.group(0)}»")
                        self.assertEqual(int(m.group(2)), en_n, f"{rel}: «{m.group(0)}»")
                    else:
                        self.assertEqual(int(m.group(1)), expected[kind],
                                         f"{rel}: «{m.group(0)}» ≠ {expected[kind]}")


class KbIndexEnTests(unittest.TestCase):
    def test_build_index_en_groups_by_stages_and_reports_broken_links(self):
        root = Path(tempfile.mkdtemp(prefix="pfs-test-kblint-idx-"))
        make_pair(root)
        with mock.patch.object(core, "KNOWLEDGE", root):
            text, problems = kb.build_index_en()
        written = (root / "INDEX_EN.md").read_text(encoding="utf-8")
        self.assertEqual(text, written)
        self.assertIn("Problem statement (`intake`)", written)
        self.assertIn("(methods_en/alpha.md)", written)
        self.assertIn("`M-alpha`", written)
        self.assertEqual(problems, [])


if __name__ == "__main__":
    unittest.main()
