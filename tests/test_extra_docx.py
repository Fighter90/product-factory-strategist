"""Доп. тесты DOCX-писателя: экранирование, структура XML, уровни заголовков, перезапись.

Запуск: python3 -m unittest discover -s tests -v
"""
import os
import tempfile
import unittest
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

TMP = tempfile.mkdtemp(prefix="pfs-test-xdocx-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from tools.pfs import docx  # noqa: E402

MD = """# Док

Цена & доля < 40% > 10% в **сегменте** и `код`.

#### Подраздел

- пункт первый

---

| A | B | C |
|---|---|---|
| один | два |
"""


class DocxXmlTests(unittest.TestCase):
    def test_escaping_headings_table_and_hr(self):
        xml = docx.md_to_docx_xml(MD)
        ET.fromstring(xml)  # XML корректен: спецсимволы экранированы, документ well-formed
        self.assertIn("Цена &amp; доля &lt; 40% &gt; 10%", xml)
        self.assertIn('w:val="Heading1"', xml)
        self.assertIn('w:val="Heading4"', xml)
        self.assertIn("<w:b/>", xml)            # **жирный** и шапка таблицы
        self.assertIn(">код<", xml)             # инлайн-код отдельным раном
        self.assertIn("• пункт первый", xml)    # маркер списка нормализован
        self.assertNotIn("<w:t xml:space=\"preserve\">---</w:t>", xml)  # горизонтальная черта пропущена
        self.assertEqual(xml.count("<w:gridCol/>"), 3)  # сетка по широкой шапке
        self.assertEqual(xml.count("<w:tr>"), 2)
        self.assertEqual(xml.count("<w:tc>"), 6)  # короткая строка дополнена пустой ячейкой

    def test_save_overwrites_and_nests_dirs(self):
        out = Path(TMP) / "глубоко" / "вложено" / "report.docx"
        p1 = docx.save(out, "# Черновик один")
        self.assertEqual(p1, out)
        with zipfile.ZipFile(out) as z:
            self.assertIn("Черновик один", z.read("word/document.xml").decode("utf-8"))
        docx.save(out, "# Черновик два")  # повторная сборка перезаписывает, а не падает
        with zipfile.ZipFile(out) as z:
            xml = z.read("word/document.xml").decode("utf-8")
        self.assertIn("Черновик два", xml)
        self.assertNotIn("Черновик один", xml)


if __name__ == "__main__":
    unittest.main()
