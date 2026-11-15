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


class StaleActivePointerTests(unittest.TestCase):
    """PRO-67: закоммиченный projects/.active ломал каждый чистый клон.

    Свежий клон (битый или отсутствующий указатель): pfs status / next работают
    с кодом 0 и подсказкой вместо ошибки; битый указатель сбрасывается, новый
    в рабочий каталог не пишется (продолжение смоук-теста установки PRO-44).
    """

    def _run(self, argv, projects_dir):
        env = {"PATH": os.environ.get("PATH", ""),
               "PYTHONPATH": str(REPO), "PFS_PROJECTS_DIR": str(projects_dir)}
        return subprocess.run([sys.executable, "-m", "tools.pfs", *argv],
                              cwd=projects_dir, env=env,
                              capture_output=True, text=True, timeout=120)

    def test_status_exit_zero_on_fresh_clone_with_committed_stale_pointer(self):
        # сценарий из багрепорта: в клоне лежит .active с slug'ом, которого нет в projects/
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / ".active").write_text("смоук-установки\n", encoding="utf-8")
            r = self._run(["status"], tmp)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn("Активный проект не найден", r.stdout)
            self.assertIn("смоук-установки", r.stdout)
            self.assertIn("pfs new", r.stdout)

    def test_stale_pointer_reset_after_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / ".active").write_text("смоук-установки\n", encoding="utf-8")
            self._run(["status"], tmp)
            self.assertFalse((Path(tmp) / ".active").exists(), "битый указатель должен сбрасываться")

    def test_next_exit_zero_on_clean_clone_without_active(self):
        # после удаления .active из git свежий клон его вообще не содержит
        with tempfile.TemporaryDirectory() as tmp:
            r = self._run(["next"], tmp)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn("Активный проект не найден", r.stdout)
            self.assertIn("pfs new", r.stdout)

    def test_status_does_not_write_active_pointer(self):
        # PRO-44 (продолжение): установка не должна писать .active в рабочий каталог
        with tempfile.TemporaryDirectory() as tmp:
            r = self._run(["status"], tmp)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertFalse((Path(tmp) / ".active").exists())

    def test_doctor_warns_on_stale_pointer_and_fix_resets_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / ".active").write_text("смоук-установки\n", encoding="utf-8")
            r = self._run(["doctor"], tmp)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn("Активный проект", r.stdout)  # предупреждение (не строка «активный: …»)
            r2 = self._run(["doctor", "--fix"], tmp)
            self.assertEqual(r2.returncode, 0, r2.stderr)
            self.assertFalse((Path(tmp) / ".active").exists(), "doctor --fix сбрасывает битый указатель")

    def test_active_pointer_ignored_and_not_tracked(self):
        gitignore = (REPO / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("projects/.active", gitignore)
        try:
            tracked = subprocess.run(["git", "ls-files", "projects/.active"], cwd=REPO,
                                     capture_output=True, text=True, timeout=30).stdout.strip()
        except FileNotFoundError:
            self.skipTest("git недоступен")
        self.assertEqual(tracked, "", "projects/.active не должен отслеживаться git")


if __name__ == "__main__":
    unittest.main()
