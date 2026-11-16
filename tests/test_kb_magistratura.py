"""PRO-76: дистилляция методологии из материалов магистратуры — пакет 1 (продуктовое ядро).

Контракт выпуска:
1. Одиннадцать карт пакета 1 существуют в RU (knowledge/methods/) и в EN-зеркалах
   (knowledge/methods_en/): b2b-validation, competitor-teardown, evidence-design,
   guerrilla-research, hypothesis-testing, mvp-ds-assembly, pnl-product-finance,
   case-solving, impact-uncertainty, metric-drop-diagnosis, ux-prototyping.
2. Каждая карта методическая: «Когда применять», «Суть», процедура/шаги, «Критерии
   качества», «Типичные ошибки»; разделы непустые; EN-зеркала структурно параллельны RU.
3. В картах нет брендов: ни вузов, ни преподавателей, ни компаний-заказчиков
   (правило knowledge/inbox/magistratura/README.md).
4. Счётчики карт в README/README_EN/COMPLIANCE/HELP/HELP_EN равны реальному числу
   карт базы знаний — знание растёт, документация следует за ним.

Запуск: python3 -m unittest tests.test_kb_magistratura -v
"""
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
KB = REPO / "knowledge"

# Пакет 1 — продуктовое ядро (карты в клоне knowledge/, ветка main приватного -base)
MAGISTRATURA_MAPS = [
    "b2b-validation", "competitor-teardown", "evidence-design", "guerrilla-research",
    "hypothesis-testing", "mvp-ds-assembly", "pnl-product-finance", "case-solving",
    "impact-uncertainty", "metric-drop-diagnosis", "ux-prototyping",
]

# Запрещённые бренды: вузы, преподаватели, компании-заказчики и их продукты
BRANDS = ["ВШЭ", "HSE", "Высшей школы", "университет", "Университет", "магистратур",
          "студент", "преподават", "Авито", "Avito", "Ozon", "Озон", "Яндекс", "Yandex",
          "Сбер", "Sber", "Тинькофф", "Tinkoff", "ЦИАН", "CIAN", "МегаФон", "Nodul",
          "n8n", "ResumeCraft", "Винокуров", "Аветисян", "Дмитренко", "Путилова", "Царьков"]

RU_REQUIRED = ["Когда применять", "Суть", "Процедура", "Критерии качества", "Типичные ошибки"]
EN_REQUIRED = ["When to use", "Core idea", "Procedure", "Quality criteria"]
EN_ERRORS = ["Typical mistakes", "Common mistakes"]  # два равноправных варианта заголовка


def body(path: Path) -> str:
    """Тело карты без frontmatter."""
    return path.read_text(encoding="utf-8").split("---", 2)[2]


def h2_titles(text: str) -> list[str]:
    return [line[3:].strip() for line in text.splitlines() if line.startswith("## ")]


def h2_sections(text: str) -> list[tuple[str, str]]:
    """Пары (заголовок H2, текст раздела до следующего H2) — H3 не режет раздел."""
    sections: list[tuple[str, str]] = []
    title, chunk = None, []
    for line in text.splitlines():
        if line.startswith("## "):
            if title is not None:
                sections.append((title, "\n".join(chunk)))
            title, chunk = line[3:].strip(), []
        elif title is not None:
            chunk.append(line)
    if title is not None:
        sections.append((title, "\n".join(chunk)))
    return sections


class MagistraturaMapsTests(unittest.TestCase):
    """Карты пакета 1 (магистратура) полные, методические и без брендов."""

    def test_new_maps_exist_in_ru_and_en(self):
        missing = []
        for name in MAGISTRATURA_MAPS:
            for sub in ("methods", "methods_en"):
                p = KB / sub / f"{name}.md"
                if not p.exists():
                    missing.append(p.relative_to(REPO).as_posix())
        self.assertEqual(missing, [], "нет карт: " + ", ".join(missing))

    def test_new_maps_carry_method_sections(self):
        bad = []
        for name in MAGISTRATURA_MAPS:
            ru_titles = [t.lower() for t in h2_titles(body(KB / "methods" / f"{name}.md"))]
            en_titles = [t.lower() for t in h2_titles(body(KB / "methods_en" / f"{name}.md"))]
            for section in RU_REQUIRED:
                if not any(t.startswith(section.lower()) for t in ru_titles):
                    bad.append(f"RU {name}.md: нет раздела «{section}»")
            if not any(t.startswith("типичные ошибки") for t in ru_titles):
                bad.append(f"RU {name}.md: нет типовых ошибок")
            for section in EN_REQUIRED:
                if not any(t.startswith(section.lower()) for t in en_titles):
                    bad.append(f"EN {name}.md: no section «{section}»")
            if not any(any(t.startswith(e.lower()) for e in EN_ERRORS) for t in en_titles):
                bad.append(f"EN {name}.md: no typical mistakes section")
        self.assertEqual(bad, [], "карты без обязательных разделов: " + "; ".join(bad))

    def test_new_maps_free_of_brands(self):
        found = []
        for name in MAGISTRATURA_MAPS:
            for sub in ("methods", "methods_en"):
                text = (KB / sub / f"{name}.md").read_text(encoding="utf-8")
                for brand in BRANDS:
                    if brand in text:
                        found.append(f"{sub}/{name}.md: «{brand}»")
        self.assertEqual(found, [], "бренды в картах магистратуры: " + ", ".join(found))

    def test_new_maps_sections_not_empty(self):
        short = []
        for name in MAGISTRATURA_MAPS:
            for sub in ("methods", "methods_en"):
                for title, content in h2_sections(body(KB / sub / f"{name}.md")):
                    if len(content.strip()) < 30:
                        short.append(f"{sub}/{name}.md: «{title}» — {len(content.strip())} символов")
        self.assertEqual(short, [], "пустые/короткие разделы: " + ", ".join(short))


class KnowledgeCountersTests(unittest.TestCase):
    """Счётчики карт в README/COMPLIANCE/HELP равны реальному числу карт базы знаний."""

    def test_docs_state_actual_map_count(self):
        n_ru = len(list((KB / "methods").glob("*.md")))
        n_en = len(list((KB / "methods_en").glob("*.md")))
        self.assertEqual(n_ru, n_en, "RU и EN-зеркала разошлись по числу карт")
        checks = [
            (REPO / "README.md", f"{n_ru} карт"),
            (REPO / "README.md", f"{n_en} EN-зеркал"),
            (REPO / "README_EN.md", f"{n_ru} cards"),
            (REPO / "README_EN.md", f"{n_en} EN mirrors"),
            (REPO / "docs" / "COMPLIANCE.md", f"{n_ru} карт RU"),
            (REPO / "docs" / "COMPLIANCE.md", f"{n_en} EN-зеркал"),
            (REPO / "docs" / "HELP.md", f"{n_ru} карт"),
            (REPO / "docs" / "HELP.md", f"{n_en} EN-зеркал"),
            (REPO / "docs" / "HELP_EN.md", f"{n_ru} method cards"),
            (REPO / "docs" / "HELP_EN.md", f"{n_en} EN mirrors"),
        ]
        missing = [f"{p.relative_to(REPO).as_posix()} ← «{needle}»"
                   for p, needle in checks if needle not in p.read_text(encoding="utf-8")]
        self.assertEqual(missing, [], f"счётчики карт устарели (в базе {n_ru}): " + "; ".join(missing))


if __name__ == "__main__":
    unittest.main()
