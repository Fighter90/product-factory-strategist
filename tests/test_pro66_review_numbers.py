"""PRO-66, раунд ревью: числа генератора не должны «случайно сходиться».

1. build_site._xlsx_values: у строковых ячеек Excel <c t="s"> в <v> лежит
   индекс общего списка строк (sharedStrings), не число. Раньше <v> брали
   подряд и float(индекса) попадал в сверку: юнит-экономика могла «сойтись»
   на случайном индексе. Теперь числовыми считаются только ячейки без t или
   с t="n" (строковые t="s"/t="str", булевы t="b" и inlineStr — нет).
2. build_site._count_tests: «def test*» по AST ловит помощников, вложенные
   функции и методы не-TestCase классов — это не то измерение, которое
   запускает `python3 -m unittest discover -s tests`. Счётчик считает методы
   «test_*» только в TestCase-классах (прямо или через базовые классы файла)
   и обязан совпадать с настоящим discovery — равенство закреплено тестом.
"""
from __future__ import annotations

import importlib.util
import re
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_site.py"

OPT_XL = ("## Вариант B. Hosted freemium SaaS\n"
          "- Экономика: paid $29/мес; переменные 25% → CM $21,75; "
          "LTV ≈ $272; LTV/CAC ≈ 4,5\n")

SHEET_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"


def load_module():
    """Импорт scripts/build_site.py как модуля без установки пакета."""
    spec = importlib.util.spec_from_file_location("build_site_review_num", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def write_sheet(path: Path, cells: str) -> Path:
    """Минимальный xlsx с одной страницей из готовых <c>-узлов."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w") as z:
        z.writestr(
            "xl/worksheets/sheet1.xml",
            f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<worksheet xmlns="{SHEET_NS}"><sheetData><row r="1">{cells}</row></sheetData></worksheet>')
    return path


class TestXlsxNumericCellsOnly(unittest.TestCase):
    """_xlsx_values читает только числовые ячейки (t отсутствует или t="n")."""

    @classmethod
    def setUpClass(cls):
        cls.mod = load_module()

    def test_string_index_boolean_and_formula_string_are_skipped(self):
        tmp = Path(tempfile.mkdtemp(prefix="pfs-xlsx-nums-"))
        xlsx = write_sheet(tmp / "unit_economics.xlsx", (
            '<c r="A1" t="s"><v>3</v></c>'          # индекс sharedStrings — не число
            '<c r="A2" t="b"><v>1</v></c>'          # булево — не число
            '<c r="A3" t="str"><v>271.88</v></c>'   # строковый результат формулы — не число
            '<c r="A4" t="inlineStr"><is><t>29</t></is></c>'  # текст без <v>
            '<c r="A5"><v>271.88</v></c>'           # число (t нет) — берём
            '<c r="A6" t="n"><v>21.75</v></c>'      # явное число — берём
        ))
        vals = self.mod._xlsx_values(xlsx)
        self.assertEqual(vals, [271.88, 21.75],
                         "в сверку попадают только числовые ячейки, в порядке документа")

    def test_shared_strings_index_alone_cannot_false_pass(self):
        """«$29» находит только индекс строковой ячейки — сверки быть не должно."""
        tmp = Path(tempfile.mkdtemp(prefix="pfs-xlsx-false-"))
        demo = tmp / "demo"
        (demo / "outputs" / "attachments").mkdir(parents=True)
        (demo / "outputs" / "03_options.md").write_text(OPT_XL, encoding="utf-8")
        # 29 встречается в книге только как индекс sharedStrings (t="s"):
        # старый код парсил <v> подряд, float("29") сходился с ценой Pro.
        write_sheet(demo / "outputs" / "attachments" / "unit_economics.xlsx",
                    '<c r="A1" t="s"><v>29</v></c>')
        self.mod.DEMO = demo
        # старый код «находил» цену 29 в индексе строковой ячейки и падал
        # дальше по CM; новый — громко отказывается сверки без чисел.
        with self.assertRaisesRegex(self.mod.BuildError, "нет чисел для сверки"):
            self.mod.excel_numbers()


TESTS_FIXTURE = '''\
import unittest


def test_helper():
    return 1


class NotCase:
    def test_fake(self):
        pass


class Base(unittest.TestCase):
    def setUp(self):
        pass


class Child(Base):
    def test_real(self):
        pass

    def helper_test(self):
        pass


class Outer:
    class Inner(unittest.TestCase):
        def test_nested(self):
            pass
'''


class TestCountTestsOneMethod(unittest.TestCase):
    """_count_tests измеряет то же, что `python3 -m unittest discover -s tests`."""

    @classmethod
    def setUpClass(cls):
        cls.mod = load_module()

    def test_only_test_case_methods_with_test_prefix_are_counted(self):
        tmp = Path(tempfile.mkdtemp(prefix="pfs-count-tests-"))
        (tmp / "test_fixture.py").write_text(TESTS_FIXTURE, encoding="utf-8")
        # discovery запускает только Child.test_real: помощник test_helper,
        # test_fake из не-TestCase класса и вложенный test_nested не собираются;
        # helper_test не имеет префикса test_.
        self.assertEqual(self.mod._count_tests(tmp), 1)

    def test_counter_equals_real_unittest_discovery(self):
        """Единое измерение: счётчик генератора == настоящий unittest discovery."""
        import unittest as ut

        suite = ut.TestLoader().discover(str(ROOT / "tests"))
        self.assertEqual(self.mod._count_tests(ROOT / "tests"),
                         suite.countTestCases())

    def test_fixture_class_via_base_is_counted_once_per_class(self):
        """Наследник через базовый класс того же файла считается; база без test_ — нет."""
        tmp = Path(tempfile.mkdtemp(prefix="pfs-count-tests2-"))
        (tmp / "test_via_base.py").write_text(
            "import unittest\n"
            "class B(unittest.TestCase):\n"
            "    def setUp(self):\n"
            "        pass\n"
            "class C1(B):\n"
            "    def test_a(self):\n"
            "        pass\n"
            "class C2(B):\n"
            "    def test_b(self):\n"
            "        pass\n",
            encoding="utf-8")
        self.assertEqual(self.mod._count_tests(tmp), 2)


if __name__ == "__main__":
    unittest.main()
