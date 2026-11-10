"""PRO-36: пути source add / docx / media add резолвятся от каталога проекта, затем от cwd.

Агент в сессиях пишет пути от каталога проекта (raw/…, sources/raw/…), а pfs запускается
из корня репозитория — раньше относительный путь искался только от cwd и давал ложный
«Файл не найден». Теперь: сначала кандидат от каталога проекта, если файла там нет — от cwd;
resolved-путь печатается в выводе.
"""
import contextlib
import os
import tempfile
import unittest
from io import StringIO
from pathlib import Path

TMP = tempfile.mkdtemp(prefix="pfs-test-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from tools.pfs import cli, core, project  # noqa: E402
from tools.pfs.core import PfsError  # noqa: E402


def _run(argv):
    out, err = StringIO(), StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = cli.main(argv)
    return rc, out.getvalue(), err.getvalue()


class ResolveInputTests(unittest.TestCase):
    """Юнит-тесты резолвера core.resolve_input."""

    def test_absolute_and_tilde_untouched(self):
        self.assertEqual(core.resolve_input("/tmp/x.md"), Path("/tmp/x.md"))
        self.assertEqual(core.resolve_input("~/Downloads/r.pdf"),
                         Path("~/Downloads/r.pdf").expanduser())

    def test_prefers_project_dir_then_cwd(self):
        pdir = Path(TMP) / "ri-pref"
        (pdir / "sources" / "raw").mkdir(parents=True, exist_ok=True)
        (pdir / "sources" / "raw" / "x.md").write_text("в проекте", encoding="utf-8")
        outside = Path(TMP) / "ri-cwd"
        (outside / "sources" / "raw").mkdir(parents=True, exist_ok=True)
        (outside / "sources" / "raw" / "x.md").write_text("не отсюда", encoding="utf-8")
        old = os.getcwd()
        os.chdir(outside)  # файл с тем же относительным путём есть и от cwd — берётся из проекта
        try:
            self.assertEqual(core.resolve_input("sources/raw/x.md", pdir),
                             pdir / "sources" / "raw" / "x.md")
            self.assertEqual(core.resolve_input("sources/raw/absent.md", pdir),
                             Path("sources/raw/absent.md"))  # нет в проекте — от cwd
            self.assertEqual(core.resolve_input("sources/raw/absent.md"),  # pdir не задан — cwd
                             Path("sources/raw/absent.md"))
        finally:
            os.chdir(old)


class CliPathResolutionTests(unittest.TestCase):
    """Кли-level: source add / docx / media add находят файл в каталоге проекта и печатают resolved-путь."""

    def setUp(self):
        self.pdir = project.create(f"Пути {id(self)}", "Почему падает удержание подписчиков?",
                                   slug=f"ri{id(self)}")
        core.set_active(self.pdir.name)
        # рабочий каталог без искомых файлов: путь обязателен к резолву от каталога проекта
        self.empty = Path(TMP) / f"ri-cwd-{id(self)}"
        self.empty.mkdir(exist_ok=True)

    def test_source_add_resolves_relative_to_project_dir(self):
        # критерий приёмки: `pfs source add raw/x.md` из repo root находит файл в каталоге проекта
        (self.pdir / "raw").mkdir()
        (self.pdir / "raw" / "x.md").write_text("выписка из отчёта", encoding="utf-8")
        old = os.getcwd(); os.chdir(self.empty)
        try:
            rc, out, err = _run(["--project", self.pdir.name, "source", "add", "raw/x.md"])
        finally:
            os.chdir(old)
        self.assertEqual(rc, 0)
        self.assertIn(str((self.pdir / "raw" / "x.md").resolve()), out)
        rows = (self.pdir / "sources.jsonl").read_text(encoding="utf-8").splitlines()
        self.assertTrue(any('"path": "sources/raw/x.md"' in r for r in rows))

    def test_source_add_text_file_falls_back_to_cwd(self):
        # файла нет в каталоге проекта — берётся от cwd, resolved-путь в выводе
        (self.empty / "doc.md").write_text("текст страницы для --text-file", encoding="utf-8")
        old = os.getcwd(); os.chdir(self.empty)
        try:
            rc, out, _err = _run(["--project", self.pdir.name, "source", "add",
                                  "--text-file", "doc.md", "--url", "https://example.org/ri"])
        finally:
            os.chdir(old)
        self.assertEqual(rc, 0)
        self.assertIn(str((self.empty / "doc.md").resolve()), out)

    def test_docx_resolves_relative_to_project_dir(self):
        (self.pdir / "notes").mkdir()
        (self.pdir / "notes" / "report.md").write_text("# Отчёт\n\nТекст.", encoding="utf-8")
        old = os.getcwd(); os.chdir(self.empty)
        try:
            rc, out, _err = _run(["--project", self.pdir.name, "docx", "notes/report.md"])
        finally:
            os.chdir(old)
        self.assertEqual(rc, 0)
        self.assertIn(str((self.pdir / "notes" / "report.docx").resolve()), out)
        self.assertTrue((self.pdir / "notes" / "report.docx").exists())

    def test_docx_missing_file_is_clean_error(self):
        old = os.getcwd(); os.chdir(self.empty)
        try:
            rc, _out, err = _run(["--project", self.pdir.name, "docx", "absent.md"])
        finally:
            os.chdir(old)
        self.assertEqual(rc, 2)
        self.assertIn("Файл не найден", err)

    def test_media_add_resolves_relative_to_project_dir(self):
        (self.pdir / "screens").mkdir()
        (self.pdir / "screens" / "shot.png").write_bytes(b"\x89PNG\r\n\x1a\nstub")
        old = os.getcwd(); os.chdir(self.empty)
        try:
            rc, out, _err = _run(["--project", self.pdir.name, "media", "add", "screens/shot.png",
                                  "--desc", "что видно на скриншоте"])
        finally:
            os.chdir(old)
        self.assertEqual(rc, 0)
        self.assertIn(str((self.pdir / "screens" / "shot.png").resolve()), out)
        self.assertTrue((self.pdir / "sources" / "raw" / "shot.png").exists())

    def test_media_add_missing_file_is_clean_error(self):
        old = os.getcwd(); os.chdir(self.empty)
        try:
            rc, _out, err = _run(["--project", self.pdir.name, "media", "add", "absent.png",
                                  "--desc", "что видно"])
        finally:
            os.chdir(old)
        self.assertEqual(rc, 2)
        self.assertIn("Файл не найден", err)
