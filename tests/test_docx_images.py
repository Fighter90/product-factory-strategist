"""Тесты: изображения в DOCX (tools/pfs/docx.py)."""
import struct
import unittest
import zipfile
import zlib
from pathlib import Path
from tempfile import TemporaryDirectory

from tools.pfs import docx


def tiny_png(w: int = 640, h: int = 320) -> bytes:
    """Минимальный валидный PNG: подпись + IHDR."""
    sig = b"\x89PNG\r\n\x1a\n"
    data = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)
    crc = zlib.crc32(b"IHDR" + data) & 0xFFFFFFFF
    return sig + struct.pack(">I", 13) + b"IHDR" + data + struct.pack(">I", crc)


def stub_jpeg(w: int = 64, h: int = 32) -> bytes:
    """Заголовок JPEG с SOF0 для парсера размеров (данные не декодируем)."""
    return (b"\xff\xd8" + b"\xff\xc0" + struct.pack(">H", 11)
            + b"\x08" + struct.pack(">HH", h, w) + b"\x00" * 8)


class TestDocxImages(unittest.TestCase):
    def test_dims_png_and_jpeg(self):
        self.assertEqual(docx._dims(tiny_png(640, 320), "png"), (640, 320))
        self.assertEqual(docx._dims(stub_jpeg(64, 32), "jpg"), (64, 32))
        self.assertEqual(docx._dims(b"garbage", "png"), (0, 0))

    def test_image_embedded_into_package(self):
        with TemporaryDirectory() as td:
            base = Path(td)
            (base / "img.png").write_bytes(tiny_png(640, 320))
            out = base / "out.docx"
            docx.save(out, "# T\n\n![Дашборд](img.png)\n\nТекст после.\n", base_dir=base)
            z = zipfile.ZipFile(out)
            names = z.namelist()
            self.assertIn("word/media/image_1.png", names)
            doc_xml = z.read("word/document.xml").decode("utf-8")
            self.assertIn('r:embed="rId11"', doc_xml)
            self.assertIn("wp:extent", doc_xml)
            rels = z.read("word/_rels/document.xml.rels").decode("utf-8")
            self.assertIn('Target="media/image_1.png"', rels)
            self.assertIn('Id="rId11"', rels)
            root_rels = z.read("_rels/.rels").decode("utf-8")
            self.assertIn('Id="rId1"', root_rels)
            ct = z.read("[Content_Types].xml").decode("utf-8")
            self.assertIn('Extension="png"', ct)
            self.assertIn("Текст после.", doc_xml)

    def test_two_images_get_separate_rids(self):
        with TemporaryDirectory() as td:
            base = Path(td)
            (base / "a.png").write_bytes(tiny_png())
            (base / "b.png").write_bytes(tiny_png(320, 160))
            out = base / "out.docx"
            docx.save(out, "![A](a.png)\n\n![B](b.png)\n", base_dir=base)
            doc_xml = zipfile.ZipFile(out).read("word/document.xml").decode("utf-8")
            self.assertIn('r:embed="rId11"', doc_xml)
            self.assertIn('r:embed="rId12"', doc_xml)

    def test_missing_image_falls_back_to_alt_text(self):
        with TemporaryDirectory() as td:
            base = Path(td)
            out = base / "out.docx"
            docx.save(out, "![Недоступный скриншот](nope.png)\n", base_dir=base)
            z = zipfile.ZipFile(out)
            self.assertFalse([n for n in z.namelist() if n.startswith("word/media/")])
            self.assertIn("Недоступный скриншот", z.read("word/document.xml").decode("utf-8"))

    def test_convert_uses_source_dir(self):
        with TemporaryDirectory() as td:
            base = Path(td)
            (base / "doc.md").write_text("![X](pic.png)\n", encoding="utf-8")
            (base / "pic.png").write_bytes(tiny_png())
            out = docx.convert(base / "doc.md")
            self.assertIn("word/media/image_1.png", zipfile.ZipFile(out).namelist())


if __name__ == "__main__":
    unittest.main()
