"""PRO-60: база знаний как зеркало — kb lint зелёный, EN-карты полные, 8 новых карт, имена=id.

Контракт выпуска:
1. `pfs kb lint` на канонической базе не находит проблем: имя файла = id без префикса,
   id EN без суффикса -en (язык в поле lang), related у EN-карт заполнен, [[ссылки]] не битые,
   дубли тегов и пустые разделы отсутствуют, паритет RU/EN (разделы H2, объём EN ≥ 80% RU).
2. Восемь новых карт существуют в RU и EN: six-pager-etalon, committee-doc-style,
   pricing-ladder, gtm-market-entry, retention-winback, message-house, scenario-modeling,
   weighted-scoring.
3. INDEX.md/INDEX_EN.md перегенерированы: «Двойной алмаз» вместо «Двойной роман»,
   каждая карта достижима по ссылке из индекса.
4. Карта M-six-pager описывает сборку по эталону, а не вставку 02/03/04/06 (PRO-46).

Запуск: python3 -m unittest tests.test_kb_lint -v
"""
import math
import tempfile
import unittest
from pathlib import Path as _P

_KB_METHODS = _P(__file__).resolve().parent.parent / "knowledge" / "methods"
requires_kb = unittest.skipUnless(any(_KB_METHODS.glob("*.md")),
                                   "база знаний не установлена - запустите scripts/install.sh")

from pathlib import Path
from unittest import mock

from tools.pfs import core, kb

REPO = Path(__file__).resolve().parents[1]
KB = REPO / "knowledge"
NEW_MAPS = ["six-pager-etalon", "committee-doc-style", "pricing-ladder", "gtm-market-entry",
            "retention-winback", "message-house", "scenario-modeling", "weighted-scoring"]


def fm(path: Path) -> dict:
    block = path.read_text(encoding="utf-8").split("---", 2)[1]
    meta: dict = {}
    for line in block.splitlines():
        for key in ("id", "lang", "related", "stages"):
            if line.startswith(key + ":"):
                meta[key] = line.split(":", 1)[1].strip()
    return meta


def h2_count(text: str) -> int:
    body = text.split("---", 2)[2]
    return sum(1 for line in body.splitlines() if line.startswith("## "))


@requires_kb
class RealKbLintTests(unittest.TestCase):
    """Каноническая база знаний должна проходить pfs kb lint без единой проблемы."""

    def test_kb_lint_green(self):
        problems = kb.lint()
        self.assertEqual(problems, [],
                         f"pfs kb lint: {len(problems)} проблем; первые: {problems[:6]}")

    def test_ru_files_named_by_id(self):
        bad = [f"{p.name}: id «{fm(p).get('id')}»" for p in sorted((KB / "methods").glob("*.md"))
               if p.stem != (fm(p).get("id") or "")[2:]]
        self.assertEqual(bad, [], f"RU-файлов с именем != id: {len(bad)}; первые: {bad[:6]}")

    def test_en_files_named_by_id_with_lang_and_related(self):
        bad = []
        for p in sorted((KB / "methods_en").glob("*.md")):
            meta = fm(p)
            cid = meta.get("id", "")
            if cid.endswith("-en"):
                bad.append(f"{p.name}: id с суффиксом -en")
            if p.stem != cid[2:]:
                bad.append(f"{p.name}: имя != id «{cid}»")
            if meta.get("lang") != "en":
                bad.append(f"{p.name}: нет lang: en")
            if meta.get("related", "[]").strip() == "[]":
                bad.append(f"{p.name}: related пуст")
        self.assertEqual(bad, [], f"EN-файлов с нарушениями: {len(bad)}; первые: {bad[:6]}")

    def test_eight_new_maps_ru_and_en(self):
        for name in NEW_MAPS:
            ru, en = KB / "methods" / f"{name}.md", KB / "methods_en" / f"{name}.md"
            self.assertTrue(ru.exists(), f"нет RU-карты methods/{name}.md")
            self.assertTrue(en.exists(), f"нет EN-карты methods_en/{name}.md")
            self.assertEqual(fm(ru).get("id"), f"M-{name}", f"{name}: RU id")
            self.assertEqual(fm(en).get("id"), f"M-{name}", f"{name}: EN id")
            self.assertEqual(fm(en).get("lang"), "en", f"{name}: EN lang")

    def test_en_mirrors_have_same_h2_sections_as_ru(self):
        bad = []
        for p in sorted((KB / "methods").glob("*.md")):
            en = KB / "methods_en" / p.name
            if not en.exists():
                bad.append(f"{p.name}: нет EN-зеркала")
                continue
            ru_n, en_n = h2_count(p.read_text(encoding="utf-8")), h2_count(en.read_text(encoding="utf-8"))
            if ru_n and en_n != ru_n:
                bad.append(f"{p.name}: H2 {en_n} против {ru_n}")
        self.assertEqual(bad, [], f"карт с паритетом разделов EN≠RU: {len(bad)}; первые: {bad[:6]}")

    def test_en_volume_at_least_80pct_of_ru(self):
        bad = []
        for p in sorted((KB / "methods").glob("*.md")):
            en = KB / "methods_en" / p.name
            if not en.exists():
                continue  # отсутствие зеркала ловит lint и тест разделов
            ru_len, en_len = len(p.read_text(encoding="utf-8")), len(en.read_text(encoding="utf-8"))
            if en_len < 0.8 * ru_len:
                bad.append(f"{p.name}: EN {en_len} из {ru_len} символов ({round(100 * en_len / ru_len)}%)")
        self.assertEqual(bad, [], f"карт с EN < 80% RU: {len(bad)}; первые: {bad[:6]}")

    def test_index_regenerated_no_double_roman(self):
        ru_idx = (KB / "INDEX.md").read_text(encoding="utf-8")
        en_idx = (KB / "INDEX_EN.md").read_text(encoding="utf-8")
        self.assertNotIn("Двойной роман", ru_idx + en_idx, "в INDEX осталась опечатка «Двойной роман»")
        self.assertIn("Двойной алмаз", ru_idx, "в INDEX.md нет исправленного названия «Двойной алмаз»")
        missing = [p.name for p in sorted((KB / "methods").glob("*.md")) if f"(methods/{p.name})" not in ru_idx]
        self.assertEqual(missing, [], f"RU-карт без ссылки в INDEX.md: {len(missing)}; первые: {missing[:6]}")
        missing_en = [p.name for p in sorted((KB / "methods_en").glob("*.md")) if f"(methods_en/{p.name})" not in en_idx]
        self.assertEqual(missing_en, [], f"EN-карт без ссылки в INDEX_EN.md: {len(missing_en)}; первые: {missing_en[:6]}")

    def test_six_pager_map_points_to_etalon(self):
        p = KB / "methods" / "six-pager.md"
        self.assertTrue(p.exists(), "карта M-six-pager должна называться six-pager.md")
        text = p.read_text(encoding="utf-8")
        self.assertIn("M-six-pager-etalon", text, "карта M-six-pager ссылается на разбор эталона")
        self.assertIn("по эталону", text, "карта M-six-pager описывает сборку по эталону, а не вставку")


class LintSyntheticTests(unittest.TestCase):
    """Правила линтера на синтетической базе: каждое нарушение ловится, чистая пара — нет."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="pfs-test-kblint-"))
        (self.tmp / "methods").mkdir()
        (self.tmp / "methods_en").mkdir()
        patcher = mock.patch.object(core, "KNOWLEDGE", self.tmp)
        patcher.start()
        self.addCleanup(patcher.stop)

    @staticmethod
    def card(dir_name: str, name: str, fm_lines: list[str], body: str) -> None:
        text = "---\n" + "\n".join(fm_lines) + "\n---\n" + body
        (core.KNOWLEDGE / dir_name / f"{name}.md").write_text(text, encoding="utf-8")

    def ok_pair(self, en_body: str = None) -> None:
        ru_body = "## Когда применять\n\nКарта про метод и его шаги применения у агента.\n\n## Суть\n\nСуть метода в нескольких плотных абзацах с формулами и правилами.\n"
        self.card("methods", "alpha", ["id: M-alpha", "title: Альфа", "stages: [options]",
                                       "tags: [метод, альфа]", "related: [M-alpha]"], ru_body)
        en = en_body if en_body is not None else "## When to apply\n\nThe card covers the method and the agent workflow steps.\n\n## Core\n\nThe core of the method in a few dense paragraphs with formulas and rules.\n"
        self.card("methods_en", "alpha", ["id: M-alpha", "lang: en", "title: Alpha", "stages: [options]",
                                          "tags: [method, alpha]", "related: [M-alpha]"], en)

    def test_clean_pair_passes(self):
        self.ok_pair()
        self.assertEqual(kb.lint(), [], "чистая пара RU+EN не должна давать проблем")

    def test_en_id_suffix_and_filename_and_lang_flagged(self):
        self.ok_pair()
        p = core.KNOWLEDGE / "methods_en" / "alpha.md"
        p.write_text(p.read_text(encoding="utf-8").replace("id: M-alpha", "id: M-alpha-en").replace("lang: en\n", ""),
                     encoding="utf-8")
        p.rename(core.KNOWLEDGE / "methods_en" / "M-alpha-en.md")
        problems = " | ".join(kb.lint())
        self.assertIn("-en", problems)
        self.assertIn("lang", problems)
        self.assertIn("имя файла не совпадает", problems)

    def test_service_tags_and_ru_line_flagged(self):
        self.ok_pair()
        p = core.KNOWLEDGE / "methods_en" / "alpha.md"
        text = p.read_text(encoding="utf-8").replace("tags: [method, alpha]", "tags: [en, summary, en]")
        text += "\n**RU-версия:** `knowledge/methods/alpha.md`.\n"
        p.write_text(text, encoding="utf-8")
        problems = " | ".join(kb.lint())
        self.assertIn("служебные теги", problems)
        self.assertIn("дубли тегов", problems)
        self.assertIn("RU-версия", problems)

    def test_broken_wiki_link_and_related_flagged(self):
        self.ok_pair()
        p = core.KNOWLEDGE / "methods" / "alpha.md"
        text = p.read_text(encoding="utf-8").replace("Суть метода", "Связь [[M-nope]] и суть метода")
        text = text.replace("related: [M-alpha]", "related: [M-ghost]")
        p.write_text(text, encoding="utf-8")
        problems = " | ".join(kb.lint())
        self.assertIn("битая [[ссылка]]", problems)
        self.assertIn("M-nope", problems)
        self.assertIn("M-ghost", problems)

    def test_empty_related_in_en_flagged(self):
        self.ok_pair()
        p = core.KNOWLEDGE / "methods_en" / "alpha.md"
        p.write_text(p.read_text(encoding="utf-8").replace("related: [M-alpha]", "related: []"),
                     encoding="utf-8")
        problems = " | ".join(kb.lint())
        self.assertIn("related пуст", problems, "пустой related у EN-карты должен ловиться")

    def test_empty_h2_section_flagged(self):
        self.ok_pair()
        p = core.KNOWLEDGE / "methods" / "alpha.md"
        p.write_text(p.read_text(encoding="utf-8").replace("## Суть\n\nСуть метода", "## Суть\n\n\n### пусто"),
                     encoding="utf-8")
        problems = " | ".join(kb.lint())
        self.assertIn("пустой раздел", problems)

    def test_missing_mirror_and_orphan_flagged(self):
        self.ok_pair()
        (core.KNOWLEDGE / "methods_en" / "alpha.md").unlink()
        problems = " | ".join(kb.lint())
        self.assertIn("нет EN-зеркала", problems)
        self.card("methods_en", "orphan", ["id: M-orphan", "lang: en", "title: Orphan", "related: [M-alpha]"],
                  "## Core\n\nAn EN card without a RU original.\n")
        problems = " | ".join(kb.lint())
        self.assertIn("без RU-оригинала", problems)

    def test_h2_parity_flagged(self):
        self.ok_pair(en_body="## When to apply\n\nThe card covers the method and the agent workflow steps.\n")
        problems = " | ".join(kb.lint())
        self.assertIn("EN зеркалит не все разделы RU", problems)

    def test_volume_boundary_80pct(self):
        ru_body = "## Суть\n\n" + "Метод с плотным текстом и правилами. " * 40 + "\n"
        self.card("methods", "alpha", ["id: M-alpha", "title: Альфа", "related: [M-alpha]"], ru_body)
        ru_len = len((core.KNOWLEDGE / "methods" / "alpha.md").read_text(encoding="utf-8"))
        need = math.ceil(0.8 * ru_len)
        fm_en = ["id: M-alpha", "lang: en", "title: Alpha", "related: [M-alpha]"]
        header = "---\n" + "\n".join(fm_en) + "\n---\n"
        # ровно на границе (>= 80%) — зелёный
        self.card("methods_en", "alpha", fm_en, "x" * max(need - len(header), 1))
        self.assertEqual([p for p in kb.lint() if "80%" in p], [], "объём на границе 80% не флагуется")
        # на один символ меньше — флаг
        text = (core.KNOWLEDGE / "methods_en" / "alpha.md").read_text(encoding="utf-8")[:-1]
        (core.KNOWLEDGE / "methods_en" / "alpha.md").write_text(text, encoding="utf-8")
        self.assertTrue(any("80%" in p for p in kb.lint()), "объём ниже 80% должен флаговаться")


if __name__ == "__main__":
    unittest.main()
