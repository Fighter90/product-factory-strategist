"""Контракт установки: entry point, пути от __file__, работа из чужого cwd.

Запуск: python3 -m unittest tests.test_install -v
"""
import os
import tempfile
import unittest

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


class InstallContractTests(unittest.TestCase):
    def test_pyproject_entry_point_maps_to_cli_main(self):
        pyproject = (REPO / "pyproject.toml").read_text(encoding="utf-8")
        self.assertIn('[project.scripts]', pyproject)
        self.assertIn('pfs = "tools.pfs.cli:main"', pyproject)

    def test_packages_include_tools_and_pfs(self):
        pyproject = (REPO / "pyproject.toml").read_text(encoding="utf-8")
        self.assertIn('packages = ["tools", "tools.pfs"]', pyproject)

    def test_core_paths_resolve_from_file_location(self):
        # ROOT/KNOWLEDGE/CONFIG derive from __file__ — не зависят от cwd
        from tools.pfs import core
        self.assertTrue((core.ROOT / "pyproject.toml").exists())
        self.assertTrue((core.KNOWLEDGE / "INDEX.md").exists())
        self.assertTrue((core.CONFIG / "models.json").exists())

    def test_pfs_module_importable_from_foreign_cwd(self):
        # главный сценарий «не работает»: запуск из каталога вне репо
        with tempfile.TemporaryDirectory() as tmp:
            r = subprocess.run(
                [sys.executable, "-m", "tools.pfs", "--help"],
                cwd=tmp, env={"PATH": os.environ.get("PATH", ""),
                              "PYTHONPATH": str(REPO), "PFS_PROJECTS_DIR": tmp},
                capture_output=True, text=True, timeout=60)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn("pfs", r.stdout)


if __name__ == "__main__":
    unittest.main()
