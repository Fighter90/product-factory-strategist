"""Реестр навыков: только релевантные, полный docs/SKILLS.md, актуальные счётчики (PRO-65).

Запуск: python3 -m unittest tests.test_skills_registry -v
"""
import importlib.util
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SKILLS_DIR = REPO / ".claude" / "skills"
EXTRAS_DIR = REPO / "extras" / "skills"

# 21 нерелевантный навык (PRO-65): биоинформатика, химия, ML-статистика, научные
# документы, режимы мышления вне процесса, outbound-продажи, reverse engineering.
REMOVED = [
    "biopython", "pydeseq2", "rdkit", "scikit-learn", "shap", "statsmodels", "seaborn",
    "latex-posters", "scientific-slides", "scientific-schematics", "paper-lookup",
    "citation-management", "consciousness-council", "dhdna-profiler", "what-if-oracle",
    "hallmark", "board-of-directors", "rea", "event-prospecting", "cold-email",
    "directory-submissions",
]


def loaded_skills():
    """Навыки, загружаемые средой: папки .claude/skills с SKILL.md (как в scripts/build_site.py)."""
    return sorted(p.parent.name for p in SKILLS_DIR.glob("*/SKILL.md"))


def load_counts_script():
    spec = importlib.util.spec_from_file_location(
        "update_skill_counts", REPO / "scripts" / "update_skill_counts.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class RemovedSkillsTests(unittest.TestCase):
    def test_removed_skills_not_loaded_but_kept_in_extras(self):
        loaded = loaded_skills()
        leftovers = [s for s in REMOVED if s in loaded]
        self.assertEqual(
            leftovers, [],
            f"нерелевантные навыки остаются загружаемыми в .claude/skills: {leftovers}")
        missing = [s for s in REMOVED if not (EXTRAS_DIR / s / "SKILL.md").is_file()]
        self.assertEqual(
            missing, [],
            f"навыки не перенесены в extras/skills (ожидался перенос, не безвозвратное удаление): {missing}")

    def test_extras_have_readme_with_disclaimer(self):
        readme = (REPO / "extras" / "README.md")
        self.assertTrue(readme.is_file(), "нет extras/README.md с пояснением")
        text = readme.read_text(encoding="utf-8")
        for name in REMOVED:
            self.assertIn(name, text, f"extras/README.md не упоминает {name}")

    def test_no_dangling_references_in_code_and_agent_config(self):
        """Тесты, инструменты pfs, субагенты, хуки и скрипты не ссылаются на удалённые навыки."""
        targets = sorted(
            list((REPO / "tools").rglob("*.py"))
            + [p for p in (REPO / "tests").rglob("*.py") if p.name != Path(__file__).name]
            + list((REPO / ".claude" / "agents").glob("*.md"))
            + list((REPO / ".claude" / "hooks").glob("*.py"))
            + list((REPO / "scripts").glob("*.py"))
            + [REPO / ".claude" / "settings.json"]
        )
        offenders = []
        for path in targets:
            text = path.read_text(encoding="utf-8", errors="replace")
            for name in REMOVED:
                if re.search(rf"\b{re.escape(name)}\b", text):
                    offenders.append(f"{path.relative_to(REPO)}: {name}")
        self.assertEqual(offenders, [], "упоминания удалённых навыков: " + "; ".join(offenders))


class SkillsDocTests(unittest.TestCase):
    def test_doc_covers_every_loaded_skill(self):
        doc = (REPO / "docs" / "SKILLS.md").read_text(encoding="utf-8")
        missing = [s for s in loaded_skills() if f"`{s}`" not in doc]
        self.assertEqual(
            missing, [],
            f"docs/SKILLS.md не обосновывает навыки (нет строки с `имя`): {missing}")

    def test_doc_states_actual_total(self):
        doc = (REPO / "docs" / "SKILLS.md").read_text(encoding="utf-8")
        m = re.search(r"Итого: \*\*(\d+)\*\* навыков", doc)
        self.assertIsNotNone(m, "в docs/SKILLS.md нет строки «Итого: **N** навыков»")
        self.assertEqual(int(m.group(1)), len(loaded_skills()),
                         "число в docs/SKILLS.md расходится с .claude/skills")

    def test_extras_section_lists_removed(self):
        doc = (REPO / "docs" / "SKILLS.md").read_text(encoding="utf-8")
        for name in REMOVED:
            self.assertIn(name, doc, f"docs/SKILLS.md не объясняет судьбу {name}")


class SkillCountersTests(unittest.TestCase):
    """Счётчики в README/HELP/SUBMISSION/COMPLIANCE/help.html обновлены скриптом."""

    def test_all_known_counters_fresh(self):
        script = load_counts_script()
        findings = script.stale_findings()
        self.assertEqual(findings, [], "устаревшие счётчики навыков: " + "; ".join(findings))

    def test_ru_plural_forms(self):
        script = load_counts_script()
        plural = script.ru_plural
        self.assertEqual(plural(121, "навык", "навыка", "навыков"), "навык")
        self.assertEqual(plural(100, "навык", "навыка", "навыков"), "навыков")
        self.assertEqual(plural(103, "навык", "навыка", "навыков"), "навыка")
        self.assertEqual(plural(11, "навык", "навыка", "навыков"), "навыков")
        self.assertEqual(plural(3, "интеграция", "интеграции", "интеграций"), "интеграции")

    def test_generated_site_pages_match_actual_count(self):
        site_ru = (REPO / "site" / "index.html").read_text(encoding="utf-8")
        site_en = (REPO / "site" / "en" / "index.html").read_text(encoding="utf-8")
        n = len(loaded_skills())
        self.assertIn(f"навыков: {n}", site_ru)
        self.assertIn(f"skills: {n}", site_en)


if __name__ == "__main__":
    unittest.main()
