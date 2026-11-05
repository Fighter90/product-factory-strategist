"""Тесты DOCX-конвертера. Запуск: python3 -m unittest discover -s tests"""
import os
import tempfile
import unittest
import zipfile
from pathlib import Path

TMP = tempfile.mkdtemp(prefix="pfs-test-docx-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from tools.pfs import docx  # noqa: E402

MD = """# Заголовок 1

Абзац с **жирным** и `кодом`.

## Заголовок 2

- пункт один
- пункт два

1. шаг раз
2. шаг два

| Колонка A | Колонка B |
|---|---|
| знач 1 | знач 2 |

> Цитата-примечание

```bash
pfs status --brief
```
"""


class DocxTests(unittest.TestCase):
    def test_convert_creates_valid_docx(self):
        src = Path(TMP) / "sample.md"
        src.write_text(MD, encoding="utf-8")
        out = docx.convert(src)
        self.assertEqual(out.suffix, ".docx")
        with zipfile.ZipFile(out) as z:
            self.assertIsNone(z.testzip())
            xml = z.read("word/document.xml").decode("utf-8")
            styles = z.read("word/styles.xml").decode("utf-8")
        self.assertIn('w:val="Heading1"', xml)
        self.assertIn('w:val="Heading2"', xml)
        self.assertIn("<w:tbl>", xml)
        self.assertIn('w:val="CodeBlock"', xml)
        self.assertIn('w:val="Quote"', xml)
        self.assertIn("<w:b/>", xml)
        self.assertIn("Heading1", styles)

    def test_cyrillic_and_custom_out(self):
        src = Path(TMP) / "ru.md"
        src.write_text("# Отчёт\nТекст на русском с «кавычками» и тире —.", encoding="utf-8")
        out = docx.convert(src, Path(TMP) / "custom" / "отчёт.docx")
        with zipfile.ZipFile(out) as z:
            xml = z.read("word/document.xml").decode("utf-8")
        self.assertIn("Отчёт", xml)
        self.assertIn("«кавычками»", xml)


if __name__ == "__main__":
    unittest.main()
