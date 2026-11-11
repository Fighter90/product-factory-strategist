"""PRO-66, раунд 3 ревью: перенос 21 навыка в extras/ (PRO-65) не входит в это изменение.

Ревью вернуло ветку PRO-66 из-за смешанного blast radius: вместе с лендингом
приехала реорганизация навыков (PRO-65) — 21 навык вынесен из .claude/skills/
в extras/skills/. Это меняет поведение агента во всём репозитории и по чеклисту
ревью должно быть отдельным изменением. Лендинг считает «N навыков» из
.claude/skills (scripts/build_site.py), поэтому тест закрепляет разделение:
полный набор навыков на месте, extras/ нет, реестр PRO-65 и его счётчик-скрипт
не упоминаются в документации.
"""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# 21 навык, который PRO-65 переносил в extras/skills/ — должны остаться
# (вернуться) в .claude/skills/, откуда их считает генератор лендинга.
MOVED = (
    "biopython", "board-of-directors", "citation-management", "cold-email",
    "consciousness-council", "dhdna-profiler", "directory-submissions",
    "event-prospecting", "hallmark", "latex-posters", "paper-lookup",
    "pydeseq2", "rdkit", "rea", "scientific-schematics", "scientific-slides",
    "scikit-learn", "seaborn", "shap", "statsmodels", "what-if-oracle",
)


class TestPro65KeptOutOfThisChange(unittest.TestCase):

    def test_moved_skills_present_in_claude_skills(self):
        for name in MOVED:
            self.assertTrue(
                (ROOT / ".claude" / "skills" / name / "SKILL.md").is_file(),
                f"навык {name} отсутствует в .claude/skills — "
                f"PRO-65-перенос остался в ветке PRO-66")

    def test_no_extras_dir(self):
        self.assertFalse(
            (ROOT / "extras").exists(),
            "extras/ (изменение PRO-65) не должно быть в ветке PRO-66")

    def test_skills_registry_doc_has_no_pro65_sections(self):
        text = (ROOT / "docs" / "SKILLS.md").read_text(encoding="utf-8")
        self.assertNotIn("extras/skills", text,
                         "docs/SKILLS.md описывает переносы PRO-65")
        self.assertNotIn("PRO-65", text,
                         "docs/SKILLS.md упоминает PRO-65")

    def test_no_counter_script_and_no_references(self):
        self.assertFalse(
            (ROOT / "scripts" / "update_skill_counts.py").exists(),
            "скрипт счётчиков PRO-65 не должен быть в ветке PRO-66")
        for doc in ("docs/SKILLS.md", "docs/HELP.md", "docs/HELP_EN.md"):
            self.assertNotIn(
                "update_skill_counts",
                (ROOT / doc).read_text(encoding="utf-8"),
                f"{doc} ссылается на скрипт счётчиков PRO-65")


if __name__ == "__main__":
    unittest.main()
