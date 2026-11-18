"""PRO-76: дистилляция методологии из внешних материалов — пакет 1 (продуктовое ядро).

Контракт выпуска:
1. Одиннадцать карт пакета 1 существуют в RU (knowledge/methods/) и в EN-зеркалах
   (knowledge/methods_en/): b2b-validation, competitor-teardown, evidence-design,
   guerrilla-research, hypothesis-testing, mvp-ds-assembly, pnl-product-finance,
   case-solving, impact-uncertainty, metric-drop-diagnosis, ux-prototyping.
2. Каждая карта методическая: «Когда применять», «Суть», процедура/шаги, «Критерии
   качества», «Типичные ошибки»; разделы непустые; EN-зеркала структурно параллельны RU.
3. В картах нет брендов ни в одном регистре и падеже: ни вузов, ни преподавателей,
   ни компаний-заказчиков (правило knowledge/inbox/magistratura/README.md);
   сравнение регистронезависимое, фамилии — с падежными формами.
4. Счётчики карт в README/README_EN/COMPLIANCE/HELP/HELP_EN равны реальному числу
   карт базы знаний — знание растёт, документация следует за ним.
5. Единая схема имён для всей базы (отклонение от буквы issue задокументировано):
   issue формулирует пути «knowledge/methods/M-<id>.md» и «methods_en/M-<id>-en.md» —
   это конвенция id карты (M-cjm и т.п.), а не имени файла. Инструмент kb lint
   (tools/pfs/kb.py::_lint_card) для ВСЕХ карт базы (включая существовавшие до пакета
   100) требует: id начинается с «M-», не содержит суффикса «-en» (язык живёт в поле
   frontmatter «lang») и stem файла равен id без префикса «M-». Файлы M-<id>.md /
   <id>-en.md сломали бы kb lint (DoD требует зелёный) и создали бы второй ярус имён
   рядом со 100 существующими картами <id>.md. Поэтому для карт пакета 1 действует та
   же единая схема: RU — knowledge/methods/<id>.md, EN-зеркало —
   knowledge/methods_en/<id>.md (тот же stem), id — M-<id> в обоих файлах, «lang: en»
   в EN. Проверки NamingSchemeTests закрепляют эту схему; двухъярусной схемы имён
   в базе нет и быть не должно (test_kb_has_no_two_tier_filenames).
6. Свежесть индекса как след поставки: каждый id пакета 1 присутствует в INDEX.md
   (ссылка methods/<id>.md) и INDEX_EN.md (ссылка methods_en/<id>.md) — IndexFreshnessTests.
7. В проверяемых документах (README RU/EN, COMPLIANCE, HELP RU/EN, lovable-brief)
   нет забытых старых счётчиков («100 карт по категориям», «670 тестов»,
   «89 method cards» и их EN-варианты): presence-only проверка
   test_docs_state_actual_map_count пропускает устаревшие числа, оставшиеся рядом
   с новыми. lovable-brief повторяет статистику README и проверяется отдельно.

Запуск: python3 -m unittest tests.test_kb_magistratura -v
"""
import unittest
from pathlib import Path as _P

_KB_METHODS = _P(__file__).resolve().parent.parent / "knowledge" / "methods"
requires_kb = unittest.skipUnless(any(_KB_METHODS.glob("*.md")),
                                   "база знаний не установлена - запустите scripts/install.sh")

from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
KB = REPO / "knowledge"

# Пакет 1 — продуктовое ядро (карты в клоне knowledge/, ветка main приватного -base).
# Имена = id карты без префикса M-; файлы: methods/<id>.md и methods_en/<id>.md
# (единая схема всей базы, см. пункт 5 докстринга).
MAGISTRATURA_MAPS = [
    "b2b-validation", "competitor-teardown", "evidence-design", "guerrilla-research",
    "hypothesis-testing", "mvp-ds-assembly", "pnl-product-finance", "case-solving",
    "impact-uncertainty", "metric-drop-diagnosis", "ux-prototyping",
]

# Запрещённые бренды: вузы, преподаватели, компании-заказчики и их продукты.
# Сравнение регистронезависимое (brand.lower() in text.lower()); фамилии — с
# падежными формами: номинатив-стем («») сам покрывает «а/у»,
# но «Дмитренко», «Путилова», «Царьков» при склонении меняют окончание —
# формы перечислены явно.
BRANDS = [
    # литералы собираются из частей: сам гардов-файл без брендов
    "В" + "ШЭ", "H" + "SE", "Вы" + "сшей школы", "ун" + "иверситет", "Ун" + "иверситет", "ма" + "гистратур", "ст" + "удент", "пр" + "еподават", "Ав" + "ито", "Av" + "ito", "Oz" + "on", "Оз" + "он", "Ян" + "декс", "Ya" + "ndex", "Сб" + "ер", "Sb" + "er", "Ти" + "нькофф", "Ti" + "nkoff", "ЦИ" + "АН", "CI" + "AN", "Ме" + "гаФон", "No" + "dul", "n" + "8n", "Re" + "sumeCraft", "Ви" + "нокуров", "Ви" + "нокурова", "Ви" + "нокурову", "Ав" + "етисян", "Ав" + "етисяна", "Ав" + "етисяну", "Дм" + "итренко", "Дм" + "итренку", "Дм" + "итренком", "Дм" + "итренке", "Пу" + "тилова", "Пу" + "тиловой", "Пу" + "тилову", "Ца" + "рьков", "Ца" + "рькова", "Ца" + "рькову", "Ца" + "рьковым",
]

RU_REQUIRED = ["Когда применять", "Суть", "Процедура", "Критерии качества", "Типичные ошибки"]
EN_REQUIRED = ["When to use", "Core idea", "Procedure", "Quality criteria"]
EN_ERRORS = ["Typical mistakes", "Common mistakes"]  # два равноправных варианта заголовка


def body(path: Path) -> str:
    """Тело карты без frontmatter."""
    return path.read_text(encoding="utf-8").split("---", 2)[2]


def frontmatter(path: Path) -> str:
    """Frontmatter карты (между первой и второй строкой «---»)."""
    return path.read_text(encoding="utf-8").split("---", 2)[1]


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


@requires_kb
class MagistraturaMapsTests(unittest.TestCase):
    """Карты пакета 1 полные, методические и без брендов."""

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
                    if brand.lower() in text.lower():
                        found.append(f"{sub}/{name}.md: «{brand}»")
        self.assertEqual(found, [], "бренды в картах пакета: " + ", ".join(found))

    def test_new_maps_sections_not_empty(self):
        short = []
        for name in MAGISTRATURA_MAPS:
            for sub in ("methods", "methods_en"):
                for title, content in h2_sections(body(KB / sub / f"{name}.md")):
                    if len(content.strip()) < 30:
                        short.append(f"{sub}/{name}.md: «{title}» — {len(content.strip())} символов")
        self.assertEqual(short, [], "пустые/короткие разделы: " + ", ".join(short))


@requires_kb
class NamingSchemeTests(unittest.TestCase):
    """Единая схема имён всей базы: methods/<id>.md + methods_en/<id>.md, id M-<id>.

    Закрепляет отклонение от буквы issue (пункт 5 докстринга): файлы M-<id>.md /
    <id>-en.md запрещены — kb lint требует stem == id без «M-», язык EN живёт в
    поле «lang», а не в суффиксе. Двухъярусной схемы имён в базе быть не должно.
    """

    def test_new_maps_follow_single_naming_scheme(self):
        bad = []
        for name in MAGISTRATURA_MAPS:
            ru, en = KB / "methods" / f"{name}.md", KB / "methods_en" / f"{name}.md"
            if not ru.exists() or not en.exists():
                bad.append(f"{name}: нет пары methods/{name}.md + methods_en/{name}.md")
                continue
            ru_id = en_id = None
            for line in frontmatter(ru).splitlines():
                if line.startswith("id:"):
                    ru_id = line.split(":", 1)[1].strip()
            for line in frontmatter(en).splitlines():
                if line.startswith("id:"):
                    en_id = line.split(":", 1)[1].strip()
            if ru_id != f"M-{name}":
                bad.append(f"RU {name}.md: id «{ru_id}» вместо M-{name}")
            if en_id != f"M-{name}":
                bad.append(f"EN {name}.md: id «{en_id}» вместо M-{name}")
            if en_id and en_id.endswith("-en"):
                bad.append(f"EN {name}.md: суффикс -en в id запрещён (язык — в поле lang)")
            if "lang: en" not in frontmatter(en):
                bad.append(f"EN {name}.md: нет «lang: en» во frontmatter")
        self.assertEqual(bad, [], "нарушение единой схемы имён: " + "; ".join(bad))

    def test_kb_has_no_two_tier_filenames(self):
        """Во всей базе нет второго яруса имён: ни M-*.md, ни *-en.md в обеих папках."""
        two_tier = sorted(
            p.relative_to(KB).as_posix()
            for sub in ("methods", "methods_en")
            for pattern in ("M-*.md", "*-en.md")
            for p in (KB / sub).glob(pattern)
        )
        self.assertEqual(
            two_tier, [],
            "второй ярус имён (M-*.md / *-en.md): " + ", ".join(two_tier),
        )


@requires_kb
class IndexFreshnessTests(unittest.TestCase):
    """Каждая карта пакета 1 присутствует в INDEX.md и INDEX_EN.md — индекс свежий."""

    def test_new_maps_listed_in_indexes(self):
        missing = []
        for name in MAGISTRATURA_MAPS:
            ru_index = (KB / "INDEX.md").read_text(encoding="utf-8")
            en_index = (KB / "INDEX_EN.md").read_text(encoding="utf-8")
            if f"](methods/{name}.md)" not in ru_index or f"`M-{name}`" not in ru_index:
                missing.append(f"INDEX.md: нет methods/{name}.md / M-{name}")
            if f"](methods_en/{name}.md)" not in en_index or f"`M-{name}`" not in en_index:
                missing.append(f"INDEX_EN.md: нет methods_en/{name}.md / M-{name}")
        self.assertEqual(missing, [], "индекс не содержит карт пакета 1: " + "; ".join(missing))


@requires_kb
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

    def test_docs_free_of_stale_counters(self):
        """В проверяемых документах нет забытых старых счётчиков.

        До пакета 1 в базе было 100 карт RU (+89/100 EN-зеркал) и 670 тестов;
        presence-only проверка выше не ловит старое число, оставшееся рядом
        с новым. lovable-brief повторяет статистику README — тоже проверяем.
        """
        stale = [
            (REPO / "README.md",
             ["100 карт по категориям", "100 EN-зеркал", "670 тест", "(670)"]),
            (REPO / "README_EN.md",
             ["100 cards across categories", "100 EN mirrors", "670 tests"]),
            (REPO / "docs" / "COMPLIANCE.md",
             ["| Карты знаний | 100", "100 карт RU", "100 EN-зеркал", "| Тесты | 670"]),
            (REPO / "docs" / "HELP.md", ["100 карт методов", "100 EN-зеркал"]),
            (REPO / "docs" / "HELP_EN.md",
             ["89 method cards", "89 EN mirrors", "100 method cards", "100 EN mirrors"]),
            (REPO / "docs" / "lovable-brief.md", ["100 карт", "100 EN-зеркал"]),
        ]
        found = [f"{p.relative_to(REPO).as_posix()} ← «{needle}»"
                 for p, needles in stale for needle in needles
                 if needle in p.read_text(encoding="utf-8")]
        self.assertEqual(found, [], "забытые старые счётчики: " + "; ".join(found))


if __name__ == "__main__":
    unittest.main()
