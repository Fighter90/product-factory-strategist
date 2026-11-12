"""PRO-57: паритет RU/EN — шаблоны knowledge/templates, AGENTS.md ↔ AGENTS_EN.md,
двуязычные SKILL.md навыков процесса.

Запуск: python3 -m unittest tests.test_docs_parity -v
"""
import json
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TEMPLATES_RU = REPO / "knowledge" / "templates"
TEMPLATES_EN = TEMPLATES_RU / "en"
SKILLS = REPO / ".claude" / "skills"
CONFIG = REPO / "config" / "quality_gate.json"

# Навыки процесса, обязанные быть двуязычными (issue PRO-57, пункт 5)
PROCESS_SKILLS = ["strategist", "intake", "research", "situation", "options",
                  "strategy", "validation-plan", "six-pager", "decision-support"]

# Документ quality gate → шаблон, по которому он пишется
DOC_TO_TEMPLATE = {
    "02_situation.md": "situation.md",
    "03_options.md": "options.md",
    "04_product_strategy.md": "product_strategy.md",
    "05_comms_strategy.md": "comms_strategy.md",
    "06_validation_plan.md": "validation_plan.md",
}


class TemplatesParityTests(unittest.TestCase):
    def test_every_ru_template_has_en_counterpart(self):
        # STYLE_RU.md — стайлгайд русского языка (PRO-52); SIX_PAGER_PROMPT_EN.md и
        # STYLE_EN.md — EN-only артефакты (PRO-31/PRO-53), EN-пар им не заводят
        missing = [p.name for p in sorted(TEMPLATES_RU.glob("*.md"))
                   if p.name not in ("SIX_PAGER_PROMPT_EN.md", "STYLE_RU.md", "STYLE_EN.md")
                   and not (TEMPLATES_EN / p.name).is_file()]
        self.assertEqual(missing, [], f"нет EN-версий шаблонов: {missing}")

    def test_en_only_templates_are_nonempty_markdown(self):
        for name in ("SIX_PAGER_PROMPT_EN.md", "STYLE_EN.md"):
            p = TEMPLATES_RU / name
            self.assertTrue(p.is_file(), f"нет EN-only шаблона {name}")
            text = p.read_text(encoding="utf-8")
            self.assertGreater(len(text), 200, f"{name}: шаблон подозрительно короткий")
            self.assertTrue(text.lstrip().startswith("#"), f"{name}: нет заголовка")

    def test_en_templates_are_nonempty_markdown(self):
        for p in sorted(TEMPLATES_EN.glob("*.md")):
            text = p.read_text(encoding="utf-8")
            self.assertGreater(len(text), 200, f"{p.name}: EN-шаблон подозрительно короткий")
            self.assertTrue(text.lstrip().startswith("#"), f"{p.name}: нет заголовка")

    def test_templates_match_quality_gate_sections(self):
        cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
        for lang, root in (("ru", TEMPLATES_RU), ("en", TEMPLATES_EN)):
            for doc, rules in cfg[lang]["documents"].items():
                tpl = root / DOC_TO_TEMPLATE[doc]
                text = tpl.read_text(encoding="utf-8").lower()
                for sec in rules.get("required_sections", []):
                    self.assertIn(sec.lower(), text, f"{lang}/{tpl.name}: нет раздела «{sec}»")

    def test_options_template_matches_gate_regex(self):
        cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
        for lang, root in (("ru", TEMPLATES_RU), ("en", TEMPLATES_EN)):
            rules = cfg[lang]["documents"]["03_options.md"]
            text = (root / "options.md").read_text(encoding="utf-8")
            heads = [l for l in text.splitlines() if re.match(rules["option_heading_regex"], l)]
            self.assertGreaterEqual(len(heads), rules["min_options"],
                                    f"{lang}/options.md: меньше {rules['min_options']} вариантов")
            low = text.lower()
            self.assertTrue(any(k in low for k in rules["status_quo_keywords"]),
                            f"{lang}/options.md: нет ключей «оставить как есть»")
            self.assertTrue(any(k in low for k in rules["exit_keywords"]),
                            f"{lang}/options.md: нет ключей выхода")


class AgentsParityTests(unittest.TestCase):
    """AGENTS_EN.md синхронизирован с AGENTS.md: те же разделы, правила и команды,
    разница объёма (в символах, не в байтах — кириллица в UTF-8 двухбайтная) ≤ 15%."""

    @classmethod
    def setUpClass(cls):
        cls.ru = (REPO / "AGENTS.md").read_text(encoding="utf-8")
        cls.en = (REPO / "AGENTS_EN.md").read_text(encoding="utf-8")

    def test_same_sections(self):
        secs = lambda t: re.findall(r"^## .+$", t, re.M)
        self.assertEqual(len(secs(self.ru)), len(secs(self.en)),
                         f"разделов RU {len(secs(self.ru))} против EN {len(secs(self.en))}")

    def test_same_numbered_rules(self):
        rules = lambda t: re.findall(r"^\d+\. \*\*", t, re.M)
        self.assertEqual(len(rules(self.ru)), len(rules(self.en)))

    def test_same_cheatsheet_commands(self):
        cmds = lambda t: sorted(set(re.findall(r"^pfs [a-z-]+", t, re.M)))
        self.assertEqual(cmds(self.ru), cmds(self.en), "шпаргалки команд разошлись")

    def test_volume_difference_within_15_percent(self):
        ru, en = len(self.ru), len(self.en)
        self.assertLessEqual(abs(ru - en) / max(ru, en), 0.15,
                             f"объём AGENTS разошёлся: RU {ru} симв., EN {en} симв.")

    def test_language_rule_present_in_both(self):
        for text, marker in ((self.ru, "pfs lang"), (self.en, "pfs lang")):
            self.assertIn(marker, text, "нет правила о языке проекта (pfs lang / --lang)")


class SkillsBilingualTests(unittest.TestCase):
    def test_process_skills_have_english_section(self):
        missing = [s for s in PROCESS_SKILLS
                   if "## English" not in (SKILLS / s / "SKILL.md").read_text(encoding="utf-8")]
        self.assertEqual(missing, [], f"нет EN-раздела в навыках: {missing}")


if __name__ == "__main__":
    unittest.main()
