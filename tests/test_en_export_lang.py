"""PRO-79: язык six-pager = язык проекта — EN-проект получает EN-каркас
без флага --en; RU-проект не меняется."""
import os
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from tools.pfs import cli, export, project, sources  # noqa: E402
from tools.pfs import i18n  # noqa: E402


class EnProjectSixPagerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import tempfile
        cls.projects = Path(tempfile.mkdtemp(prefix="en-export-"))
        cls._old_pd = os.environ.get("PFS_PROJECTS_DIR")
        os.environ["PFS_PROJECTS_DIR"] = str(cls.projects)
        cls.pdir_en = project.create("QA EN project", "Why is retention dropping?",
                                     slug="qa-en-exp", lang="en")
        sources.add(cls.pdir_en, text="Public report: market 40B, growth 12%", title="Market")
        cls.pdir_ru = project.create("QA RU", "Почему падает удержание?", slug="qa-ru-exp")

    @classmethod
    def tearDownClass(cls):
        if cls._old_pd is None:
            os.environ.pop("PFS_PROJECTS_DIR", None)
        else:
            os.environ["PFS_PROJECTS_DIR"] = cls._old_pd
        import shutil
        shutil.rmtree(cls.projects, ignore_errors=True)

    def test_en_project_builds_en_skeleton_by_default(self):
        cli.main(["--project", self.pdir_en.name, "export", "--six-pager"])
        en = (self.pdir_en / "outputs" / "SIX_PAGER.md").read_text(encoding="utf-8")
        self.assertIn("## FAQ-1. Current state analysis", en)
        self.assertNotIn("## FAQ-1. Анализ текущего состояния", en)
        # RU-проект не изменился
        cli.main(["--project", self.pdir_ru.name, "export", "--six-pager"])
        ru = (self.pdir_ru / "outputs" / "SIX_PAGER.md").read_text(encoding="utf-8")
        self.assertIn("## FAQ-1. Анализ текущего состояния", ru)


if __name__ == "__main__":
    unittest.main()
