"""pfs doctor: блок «Установка» — режим (editable/venv/source), which pfs, PATH, projects dir, версия (PRO-44).

Запуск: python3 -m unittest tests.test_doctor_install -v
"""
import argparse
import io
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parents[1]
SP = Path("/site-packages")  # синтетический site-packages
DIST = SP / "product_factory_strategist-1.2.14.dist-info"


class InstallModeTests(unittest.TestCase):
    def test_editable_when_module_outside_dist_site_packages(self):
        # uv tool install -e: dist-info в site-packages, код — в репозитории
        from tools.pfs import cli
        self.assertEqual(cli.install_mode(DIST, Path("/repo/tools/pfs/cli.py")), "editable")

    def test_venv_when_module_alongside_dist_info(self):
        # обычная установка: и код, и dist-info лежат в одном site-packages
        from tools.pfs import cli
        self.assertEqual(cli.install_mode(DIST, SP / "tools" / "pfs" / "cli.py"), "venv")

    def test_source_when_no_dist_info(self):
        from tools.pfs import cli
        self.assertEqual(cli.install_mode(None, Path("/repo/tools/pfs/cli.py")), "source")


class InstallLinesTests(unittest.TestCase):
    def test_editable_block_names_pfs_path_version_and_projects_dir(self):
        from tools.pfs import cli
        lines = cli.install_lines(mod_file=Path("/repo/tools/pfs/cli.py"), dist_path=DIST,
                                  version="9.9.9", pfs_path="/Users/u/.local/bin/pfs",
                                  projects_dir=Path("/data/projects"))
        text = "\n".join(lines)
        self.assertIn("Установка: editable", text)
        self.assertIn("9.9.9", text)
        self.assertIn("/Users/u/.local/bin/pfs", text)
        self.assertIn("PATH", text)
        self.assertIn("/data/projects", text)

    def test_block_reports_source_run_and_missing_pfs_on_path(self):
        from tools.pfs import cli
        lines = cli.install_lines(mod_file=Path("/repo/tools/pfs/cli.py"), dist_path=None,
                                  version=None, pfs_path="", projects_dir=Path("/data/projects"))
        text = "\n".join(lines)
        self.assertIn("source", text)
        self.assertIn("нет (пакет не установлен)", text)
        self.assertIn("нет в PATH", text)
        self.assertIn("/data/projects", text)

    def test_dist_info_missing_package_is_none(self):
        from tools.pfs import cli
        version, dist_path = cli._dist_info("pfs-no-such-package-xyz")
        self.assertIsNone(version)
        self.assertIsNone(dist_path)


class DoctorOutputTests(unittest.TestCase):
    def test_doctor_prints_install_block(self):
        from tools.pfs import cli
        buf = io.StringIO()
        with redirect_stdout(buf):
            cli.cmd_doctor(argparse.Namespace())
        out = buf.getvalue()
        self.assertIn("Установка:", out)
        self.assertIn("pfs:", out)
        self.assertIn("Projects dir:", out)


if __name__ == "__main__":
    unittest.main()
