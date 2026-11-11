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


# Упоминания этих имён в оставшихся навыках допустимы только как библиотеки pip
# (импорты, `pip install`, имена стилей matplotlib), а не как указатели на навык.
# Файлы и каталоги, где такие упоминания легитимны:
LIBRARY_MENTION_ALLOWLIST = (
    ".claude/skills/exploratory-data-analysis/",
    ".claude/skills/statistical-analysis/",
    ".claude/skills/matplotlib/",
    ".claude/skills/scientific-visualization/",
    ".claude/skills/scientific-writing/references/figures_tables.md",
)


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


class NoDanglingSkillPointersTests(unittest.TestCase):
    """Оставшиеся навыки не ссылаются на удалённые: «см. X», «навык X» — висячие указатели.

    Исключения: упоминания как библиотек pip (импорты, pip install, имена стилей) —
    LIBRARY_MENTION_ALLOWLIST; неоднозначные слова («hallmark», «rea») — только в
    контексте указателя на навык («см. X», «X skill», `X`), обычное слово допустимо.
    """

    AMBIGUOUS_WORDS = {"hallmark", "rea"}
    POINTER_CONTEXT = (
        r"`{name}`",            # `имя`
        r"\*\*{name}\*\*",      # **имя**
        r"{name} skill",        # «имя skill»
        r"skills/{name}\b",     # путь внутрь навыка
        r"см\. {name}\b", r"see {name}\b",  # явный указатель
    )

    def _mentions(self, text, name):
        escaped = re.escape(name)
        pattern = (rf"\b{escaped}\b" if name not in self.AMBIGUOUS_WORDS
                   else "|".join(p.format(name=escaped) for p in self.POINTER_CONTEXT))
        return re.findall(pattern, text, re.IGNORECASE)

    def test_no_skill_pointers_to_removed_skills(self):
        offenders = []
        for path in sorted(SKILLS_DIR.rglob("*")):
            if not path.is_file() or path.suffix not in (".md", ".json", ".py"):
                continue
            rel = path.relative_to(REPO).as_posix()
            if any(rel == p or rel.startswith(p) for p in LIBRARY_MENTION_ALLOWLIST):
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            for name in REMOVED:
                if self._mentions(text, name):
                    offenders.append(f"{rel}: {name}")
        self.assertEqual(
            offenders, [],
            "оставшиеся навыки ссылаются на удалённые: " + "; ".join(offenders))


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


# Каноничная схема шагов процесса AGENTS.md (`pfs step`): 0 intake · 1 sources ·
# 2 research · 3 discovery · 4 situation · 5 options · 6 choice · 7 strategy ·
# 8 validation · 9 review · 10 decision · 11 monitoring.
STEP_NUMBERS = {
    "intake": 0, "sources": 1, "research": 2, "discovery": 3, "situation": 4,
    "options": 5, "choice": 6, "strategy": 7, "validation": 8, "review": 9,
    "decision": 10, "monitoring": 11,
}

# Базовые навыки → каноничные шаги (таблица «Шаг (`pfs step`)» из AGENTS.md).
CANONICAL_BASE_STEPS = {
    "strategist": "все",
    "intake": "0",
    "research": "1–2",
    "data-analysis": "2",
    "interviews": "2",
    "ux-review": "2",
    "deep-research": "2",
    "situation": "4",
    "options": "5",
    "strategy": "7",
    "validation-plan": "8",
    "six-pager": "9",
    "decision-support": "10–11",
}


def doc_rows(text, section_prefix):
    """Строки таблиц раздела «## <section_prefix>…»: (имя, колонка шагов, кто вызывает)."""
    rows = []
    in_section = False
    for line in text.splitlines():
        if line.startswith("## "):
            in_section = line.startswith(f"## {section_prefix}")
            continue
        if in_section and line.startswith("| `"):
            cols = [c.strip() for c in line.split("|")]
            rows.append((cols[1].strip("`"), cols[2], cols[4]))
    return rows


def step_numbers(text):
    """Числа шагов из ссылки: «2», «1–2», «7, 9–11», «10 (decision)», «8+», «реклама (7–8)»."""
    nums = set()
    for m in re.finditer(r"(\d+)\s*[–—]\s*(\d+)", text):
        nums.update(range(int(m.group(1)), int(m.group(2)) + 1))
    without_ranges = re.sub(r"\d+\s*[–—]\s*\d+", " ", text)
    nums.update(int(m.group()) for m in re.finditer(r"\d+", without_ranges))
    return nums


class SkillCountersTests(unittest.TestCase):
    """Счётчики в README/HELP/SUBMISSION/COMPLIANCE/help.html обновлены скриптом."""

    def test_all_known_counters_fresh(self):
        script = load_counts_script()
        findings = script.stale_findings()
        self.assertEqual(findings, [], "устаревшие счётчики навыков: " + "; ".join(findings))

    def test_spaced_group_counters_recognized(self):
        """Счётчики с пробелом перед числом («Личная библиотека 75») скрипт распознаёт."""
        script = load_counts_script()
        c = script.counts()
        rules = script.build_rules(c)
        stale_value = c["personal"] + 18
        new_text, findings = script._process_text(
            f'SK --> L["Личная библиотека {stale_value}<br/>дизайн · мета"]', rules)
        self.assertIn(f"Личная библиотека {c['personal']}", new_text,
                      "скрипт не обновляет счётчик группы с пробелом перед числом")
        self.assertTrue(findings, "скрипт не сообщает об устаревшем счётчике с пробелом")
        ok_text, ok_findings = script._process_text(
            f'Личная библиотека {c["personal"]}<br/>', rules)
        self.assertEqual(ok_text, f'Личная библиотека {c["personal"]}<br/>')
        self.assertEqual(ok_findings, [], "актуальный счётчик помечен как устаревший")

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


class MermaidGroupTests(unittest.TestCase):
    """Mermaid-схема «Навыки»: суммы групп = фактическое число, убранные категории отсутствуют."""

    def _block(self, path):
        text = (REPO / path).read_text(encoding="utf-8")
        m = re.search(r'SK\["100 (?:навыков|skills)"\]', text)
        self.assertIsNotNone(m, f"в {path} нет узла SK[\"100 …\"] второго mermaid-блока")
        end = text.find("```", m.end())
        self.assertNotEqual(end, -1, f"в {path} не найдено закрытие mermaid-блока")
        return text[m.start():end]

    def test_group_numbers_sum_to_actual_total(self):
        c = load_counts_script().counts()
        ru = self._block("README.md")
        en = self._block("README_EN.md")
        for block, groups in (
            (ru, [("Базовые", c["base"]), ("Product-skills", c["product"]),
                  ("Личная библиотека", c["personal"]), ("Интеграции", c["integrations"])]),
            (en, [("Base", c["base"]), ("Product-skills", c["product"]),
                  ("Personal library", c["personal"]), ("Integrations", c["integrations"])]),
        ):
            found = {}
            for name, expected in groups:
                m = re.search(rf"{name} (\d+)", block)
                self.assertIsNotNone(m, f"в mermaid-блоке нет группы «{name} N»")
                found[name] = int(m.group(1))
                self.assertEqual(
                    found[name], expected,
                    f"группа «{name}»: в mermaid {found[name]}, фактически {expected}")
            self.assertEqual(
                sum(found.values()), c["total"],
                f"сумма групп в mermaid-блоке ({sum(found.values())}) ≠ числу навыков ({c['total']})")

    def test_no_thinking_modes_category(self):
        self.assertNotIn("режимы мышления", self._block("README.md"),
                         "категория «режимы мышления» удалена (слилась с «мета»)")
        self.assertNotIn("thinking modes", self._block("README_EN.md"),
                         "категория «thinking modes» удалена (merged into «meta»)")


class HelpGroupHeaderTests(unittest.TestCase):
    """«Личная библиотека» в HELP — самостоятельная группа-родитель с актуальным числом."""

    def test_ru_header_is_own_group_with_actual_count(self):
        text = (REPO / "docs" / "HELP.md").read_text(encoding="utf-8")
        m = re.search(r"^- \*\*Личная библиотека \((\d+)\):\*\*\s*$", text, re.M)
        self.assertIsNotNone(
            m, "в docs/HELP.md нет заголовка группы «- **Личная библиотека (N):**» — "
               "подкатегории висят без родителя")
        self.assertEqual(int(m.group(1)), load_counts_script().counts()["personal"])

    def test_en_header_is_own_group_with_actual_count(self):
        text = (REPO / "docs" / "HELP_EN.md").read_text(encoding="utf-8")
        m = re.search(r"^- \*\*Personal library \((\d+)\)\*\* — imported packs by category:",
                      text, re.M)
        self.assertIsNotNone(
            m, "в docs/HELP_EN.md нет заголовка группы «Personal library (N)»")
        self.assertEqual(int(m.group(1)), load_counts_script().counts()["personal"])


class StepSchemeTests(unittest.TestCase):
    """Колонка шагов docs/SKILLS.md соответствует одной каноничной схеме AGENTS.md (`pfs step`)."""

    def setUp(self):
        self.doc = (REPO / "docs" / "SKILLS.md").read_text(encoding="utf-8")

    def test_base_table_matches_canonical_scheme(self):
        rows = doc_rows(self.doc, "Базовые — шаги процесса")
        actual = {name: step for name, step, _ in rows}
        self.assertEqual(actual, CANONICAL_BASE_STEPS)

    def test_named_step_invokers_point_to_declared_steps(self):
        """«навык шага `X`» в «Кто вызывает» согласован с числами колонки шагов."""
        rows = []
        for prefix in ("Базовые — шаги процесса", "Product-skills", "Интеграции"):
            rows.extend(doc_rows(self.doc, prefix))
        offenders = []
        for name, step, invoker in rows:
            m = re.search(r"навык шага `([\w-]+)`", invoker)
            if not m:
                continue
            expected = STEP_NUMBERS.get(m.group(1))
            if expected is None:
                offenders.append(f"`{name}`: «{m.group(1)}» — не шаг схемы AGENTS.md")
            elif expected not in step_numbers(step):
                offenders.append(
                    f"`{name}`: колонка «{step}» не содержит шаг {expected} ({m.group(1)})")
        self.assertEqual(
            offenders, [],
            "«навык шага `X`» расходится с колонкой шагов: " + "; ".join(offenders))

    def test_all_step_references_within_canonical_range(self):
        rows = []
        for prefix in ("Базовые — шаги процесса", "Product-skills", "Интеграции",
                       "Личная библиотека"):
            rows.extend(doc_rows(self.doc, prefix))
        offenders = [
            f"`{name}`: «{step}»" for name, step, _ in rows
            if not step_numbers(step) <= set(STEP_NUMBERS.values())
        ]
        self.assertEqual(
            offenders, [],
            "числа вне каноничной схемы шагов 0–11 (AGENTS.md): " + "; ".join(offenders))


# Подраздел реестра docs/SKILLS.md → метка категории в README.md (RU) / README_EN.md (EN).
README_LIST_LABELS = [
    ("UX и дизайн", "дизайн", "Design"),
    ("Маркетинг и рост", "маркетинг", "Marketing"),
    ("Ресёрч и данные", "наука и данные", "Science and data"),
    ("Документы и медиа", "документы/медиа", "Docs/media"),
    ("Мета", "мета", "Meta"),
]

# Указатели «X skill» на инструменты вне набора репозитория: pip-библиотеки и навыки
# личной библиотеки автора, которых в .claude/skills нет сознательно. venue-templates
# здесь нет: его упоминания убиты (см. KeptSkillPointerTests).
EXTERNAL_SKILL_POINTERS = {
    "gget", "bioservices",         # pip-библиотеки (literature-review)
    "ab-testing", "copy-editing",  # личная библиотека автора вне набора
    "parallel-web", "social", "scraping", "competitor-profiling", "schema",
}

# Обычные слова, совпадающие с формой указателя («load **one** skill per artifact»).
SKILL_POINTER_STOPWORDS = {"one"}

# Формы указателя «используй навык X» в текстах навыков.
SKILL_POINTER_PATTERNS = (
    r"`([\w-]+)` skill",
    r"skill `([\w-]+)`",
    r"\*\*([\w-]+)\*\* skill",
    r"\*\*([\w-]+) skill\*\*",
)


def registry_personal_library_groups():
    """docs/SKILLS.md, раздел «Личная библиотека»: {подраздел: [имена навыков]}."""
    doc = (REPO / "docs" / "SKILLS.md").read_text(encoding="utf-8")
    section = doc.split("## Личная библиотека", 1)[1].split("\n## ", 1)[0]
    groups, current = {}, None
    for line in section.splitlines():
        m = re.match(r"### (.+?) \(\d+\)\s*$", line)
        if m:
            current = m.group(1)
            groups[current] = []
        elif current and line.startswith("| `"):
            groups[current].append(line.split("|")[1].strip().strip("`"))
    return groups


def readme_personal_library_groups(relpath):
    """Списки имён по категориям из буллета «Личная библиотека» в README: {метка: [имена]}."""
    text = (REPO / relpath).read_text(encoding="utf-8")
    lines = text.splitlines()
    start = next(i for i, l in enumerate(lines)
                 if re.search(r"\*\*(Личная библиотека|personal library) \d+\*\*", l))
    chunk = [lines[start]]
    for line in lines[start + 1:]:
        if not line.startswith((" ", "\t")):
            break
        chunk.append(line)
    joined = " ".join(chunk)
    labels = [ru if relpath.endswith("README.md") else en for _, ru, en in README_LIST_LABELS]
    matches = list(re.finditer("(" + "|".join(re.escape(l) for l in labels) + "):", joined))
    groups = {}
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(joined)
        groups[m.group(1)] = re.findall(r"[a-z0-9][a-z0-9-]+", joined[m.end():end])
    return groups


class PersonalLibraryListSyncTests(unittest.TestCase):
    """Списки личной библиотеки в README/README_EN соответствуют реестру docs/SKILLS.md (ревью PRO-65)."""

    def test_readme_lists_match_registry(self):
        registry = registry_personal_library_groups()
        self.assertIn("Маркетинг и рост", registry, "в docs/SKILLS.md нет подраздела маркетинга")
        for relpath in ("README.md", "README_EN.md"):
            readme = readme_personal_library_groups(relpath)
            for section, ru_label, en_label in README_LIST_LABELS:
                label = ru_label if relpath.endswith("README.md") else en_label
                self.assertIn(label, readme, f"{relpath}: нет категории «{label}»")
                self.assertEqual(
                    sorted(readme[label]), sorted(registry.get(section, [])),
                    f"{relpath}: категория «{label}» расходится с реестром «{section}» docs/SKILLS.md")


class TestCountersTests(unittest.TestCase):
    """Счётчик тестов в README/SUBMISSION/COMPLIANCE/help.html ведёт скрипт счётчиков (ревью PRO-65).

    Один источник: статический подсчёт тестовых методов по tests/test_*.py — тот же
    метод, что в scripts/build_site.py (тут и в docstring ниже нельзя писать
    сигнатуру дословно: статический счётчик считает и строки документации).
    """

    def test_script_counts_tests(self):
        script = load_counts_script()
        self.assertGreater(script.counts()["tests"], 0, "скрипт счётчиков не считает тесты")

    def test_stale_test_counters_recognized(self):
        script = load_counts_script()
        actual = script.counts()["tests"]
        rules = script.build_rules(script.counts())
        stale = str(actual + 7)
        samples = [
            f"tests/               ({stale})",
            f"tests/ ({stale})",
            f"| Тесты | {stale} (`OK`) |",
            f"# 1. Тесты инструментов ({stale}, без установки пакетов)",
            f"| unittest | {stale} тестов инструментов | tests/ |",
            f"$ python3 -m unittest discover -s tests   # {stale} тестов, опционально",
            f"$ python3 -m unittest discover -s tests   # {stale} tests, optional",
        ]
        for sample in samples:
            new_text, findings = script._process_text(sample, rules)
            self.assertIn(str(actual), new_text,
                          f"скрипт не обновляет счётчик тестов: {sample!r}")
            self.assertTrue(findings, f"скрипт не сообщает об устаревшем счётчике: {sample!r}")
            _, ok_findings = script._process_text(sample.replace(stale, str(actual)), rules)
            self.assertEqual(ok_findings, [],
                             f"актуальный счётчик помечен как устаревший: {sample!r}")


class KeptSkillPointerTests(unittest.TestCase):
    """«Use `X` skill» в оставшихся навыках указывает на существующий навык или известный внешний инструмент.

    Ревью PRO-65 (раунд 3): научные навыки ссылались на venue-templates, которого нет ни в
    .claude/skills, ни в extras, а описываемые им файлы (venue_writing_styles.md и др.) не
    поставляются — указатели убиты.
    """

    def test_named_skill_pointers_target_known_skills(self):
        loaded = {s.lower() for s in loaded_skills()}
        offenders = []
        for path in sorted(SKILLS_DIR.rglob("*.md")):
            text = path.read_text(encoding="utf-8", errors="replace")
            for pat in SKILL_POINTER_PATTERNS:
                for name in re.findall(pat, text, re.IGNORECASE):
                    if name.lower() in SKILL_POINTER_STOPWORDS:
                        continue
                    if name.lower() not in loaded and name.lower() not in EXTERNAL_SKILL_POINTERS:
                        offenders.append(f"{path.relative_to(REPO)}: {name}")
        self.assertEqual(
            offenders, [],
            "указатели на несуществующие в наборе навыки: " + "; ".join(offenders))

    def test_scientific_writing_has_no_local_generate_script_calls(self):
        """scientific-writing получает фигуры формулировкой generate-image, а не вызовом локального скрипта."""
        offenders = [
            p.relative_to(REPO).as_posix()
            for p in (SKILLS_DIR / "scientific-writing").rglob("*.md")
            if re.search(r"python scripts/generate_", p.read_text(encoding="utf-8", errors="replace"))
        ]
        self.assertEqual(
            offenders, [],
            "оставшиеся вызовы локальных generate-скриптов: " + "; ".join(offenders))


if __name__ == "__main__":
    unittest.main()
