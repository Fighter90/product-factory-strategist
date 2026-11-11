"""PRO-65: в `.claude/skills` только навыки продуктовой стратегии.

21 навык вне рамок агент-стратега (биоинформатика, химия, ML-инструментарий,
научные постеры/слайды, reverse-engineering, холодные письма и директории,
ИИ-советы общего назначения) удалён — полный список в REMOVED. Тесты держат:

1. каталоги удалённых навыков отсутствуют в `.claude/skills/`;
2. документация агента и сайт не упоминают удалённые (жюри не увидит химию);
3. docs/SKILLS.md покрывает каждый оставшийся навык (шаг/сценарий, зачем, кто вызывает);
4. счётчики сайта и SUBMISSION под контролем scripts/update_counters.py —
   расширение форматов из PRO-63: трио `data-target="N"`, «Навыки (N)»,
   «Skills (N)», SVG «>skills N<», mermaid «skills: N» / «subagents: N».

Запуск: python3 -m unittest tests.test_skills_cleanup -v
"""
from __future__ import annotations

import importlib.util
import re
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".claude" / "skills"

# 21 навык, удалённый в PRO-65 (не привязаны к шагам процесса стратега).
REMOVED = ["biopython", "pydeseq2", "rdkit", "scikit-learn", "shap", "statsmodels",
           "seaborn", "latex-posters", "scientific-slides", "scientific-schematics",
           "paper-lookup", "citation-management", "consciousness-council", "dhdna-profiler",
           "what-if-oracle", "hallmark", "board-of-directors", "rea", "event-prospecting",
           "cold-email", "directory-submissions"]

# Документация и сайт, которые смотрит жюри: без упоминаний удалённых навыков.
AGENT_DOCS = ["AGENTS.md", "AGENTS_EN.md", "README.md", "README_EN.md",
              "docs/HELP.md", "docs/HELP_EN.md", "docs/SKILLS.md",
              "docs/SUBMISSION.md", "site/index.html", "site/help.html"]


def _load_counters():
    spec = importlib.util.spec_from_file_location(
        "update_counters", ROOT / "scripts" / "update_counters.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class RemovedSkillsGone(unittest.TestCase):
    """Каталоги 21 удалённого навыка отсутствуют в .claude/skills."""

    def test_removed_skill_dirs_absent(self):
        for name in REMOVED:
            self.assertFalse((SKILLS / name).exists(), f"{name} должен быть удалён")

    def test_remaining_count_is_100(self):
        self.assertEqual(sum(1 for p in SKILLS.iterdir() if p.is_dir()), 100)


class AgentDocsDoNotMentionRemoved(unittest.TestCase):
    """README×2, HELP×2, SKILLS, SUBMISSION, сайт — без имён удалённых навыков."""

    def test_no_removed_names_in_docs(self):
        for rel in AGENT_DOCS:
            text = (ROOT / rel).read_text(encoding="utf-8")
            for name in REMOVED:
                self.assertNotRegex(text, rf"\b{re.escape(name)}\b",
                                    f"{rel} упоминает удалённый навык {name}")


class SkillsMdCoversRemaining(unittest.TestCase):
    """docs/SKILLS.md — реестр: каждый оставшийся навык упомянут, у таблицы
    есть колонки «Шаг/сценарий», «Зачем», «Кто вызывает»."""

    def test_every_remaining_skill_listed(self):
        text = (ROOT / "docs" / "SKILLS.md").read_text(encoding="utf-8")
        for column in ("Шаг/сценарий", "Зачем", "Кто вызывает"):
            self.assertIn(column, text, f"в SKILLS.md нет колонки «{column}»")
        listed = {p.name for p in SKILLS.iterdir() if p.is_dir()}
        missing = sorted(n for n in listed if n not in text)
        self.assertEqual(missing, [], f"SKILLS.md не покрывает навыки: {missing}")


class CounterScriptCoversSiteAndSubmission(unittest.TestCase):
    """Расширение PRO-63: счётчики навыков на сайте и в SUBMISSION правит скрипт."""

    def test_files_include_site_and_submission(self):
        mod = _load_counters()
        for rel in ("site/index.html", "site/help.html", "docs/SUBMISSION.md"):
            self.assertIn(rel, mod.FILES, f"{rel} не под контролем update_counters")


class SiteCounterFormats(unittest.TestCase):
    """Новые форматы счётчиков подставляются, соседние числа не задеваются."""

    C = {"tests": 400, "skills": 100, "cards_ru": 89, "cards_en": 89, "subagents": 8}

    def setUp(self):
        self.mod = _load_counters()

    def _apply(self, text: str) -> str:
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "site.html"
            p.write_text(text, encoding="utf-8")
            out, _n = self.mod.update_file(p, self.C)
            return out

    def test_data_target_trio_on_stats_line(self):
        line = ('<div class="stat"><b><span class="cnt" data-target="121">0</span>/'
                '<span class="cnt" data-target="8">0</span>/<span class="cnt" '
                'data-target="4">0</span></b><span lang="ru">навыков / субагентов / хуков</span>'
                '<span lang="en">skills / subagents / hooks</span></div>\n')
        out = self._apply(line)
        self.assertIn(f'data-target="{self.C["skills"]}"', out)
        self.assertIn(f'data-target="{self.C["subagents"]}"', out)
        self.assertIn('data-target="4"', out)  # хуки не считаются — не тронуты

    def test_data_target_outside_stats_line_untouched(self):
        # Чужие data-target (шаги, карты, проценты) не подменяются.
        line = ('<div class="stat"><b><span class="cnt" data-target="12">0</span></b>'
                '<span lang="ru">шагов процесса</span></div>\n'
                '<div class="stat"><b><span class="cnt" data-target="100">0</span></b>%'
                '<span lang="ru">чисел подтверждены</span></div>\n')
        self.assertEqual(self._apply(line), line)

    def test_bare_heading_counters_ru_and_en(self):
        out = self._apply('<a lang="ru">Навыки (120)</a><a lang="en">Skills (120)</a>\n')
        self.assertIn(f"Навыки ({self.C['skills']})", out)
        self.assertIn(f"Skills ({self.C['skills']})", out)

    def test_svg_number_after_skills(self):
        out = self._apply('<text>skills 121</text>\n')
        self.assertIn(f"<text>skills {self.C['skills']}</text>", out)

    def test_word_tail_is_not_matched(self):
        # Ловушка на хвост слова: «product-skills 27» — это ЧИСЛО ГРУППЫ, не счётчик.
        src = '<t>product-skills 27</t>\n'
        self.assertEqual(self._apply(src), src)

    def test_mermaid_colon_form(self):
        out = self._apply('AG --> SK["skills: 120<br/>(базовые 13)"]\n'
                          'AG --> SUB["subagents: 8<br/>researcher"]\n')
        self.assertIn(f"skills: {self.C['skills']}", out)
        self.assertIn(f"subagents: {self.C['subagents']}", out)

    def test_submission_ru_word_form(self):
        out = self._apply("| Навыки, хуки, субагенты | 121 навык / 4 хука / 8 субагентов |\n")
        self.assertIn(f"{self.C['skills']} навык", out)
        self.assertIn(f"{self.C['subagents']} субагентов", out)


class RealFilesCurrent(unittest.TestCase):
    """Гейт PRO-63 на реальных файлах, включая сайт и SUBMISSION: --check зелёный."""

    def test_check_passes(self):
        self.assertEqual(_load_counters().main(["--check"]), 0)


if __name__ == "__main__":
    unittest.main()
