"""PRO-57 (раунд 2): REPORT.md и сводные сводки — по языку проекта.

Пункты ревью: заголовки приложений и блок стоимости в REPORT.md локализуются
по `i18n.lang_of(pdir)`; сводные `cost.summary_text`/`finish.summary_text` —
через ключи i18n; PfsError-сообщения `participate.guide` — на языке проекта;
EN-путь ошибки «проект существует» (pfs new с занятым slug).
RU-строки дословно прежние (дефолт lang=ru).

Запуск: python3 -m unittest tests.test_report_i18n -v
"""
import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout

TMP = tempfile.mkdtemp(prefix="pfs-test-report-i18n-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from pathlib import Path  # noqa: E402

from tools.pfs import cli, cost, export, finish, participate, project  # noqa: E402
from tools.pfs.core import PfsError  # noqa: E402


def run_cli(argv):
    buf = io.StringIO()
    args = cli.build_parser().parse_args(argv)
    with redirect_stdout(buf):
        args.f(args)
    return buf.getvalue()


class ReportBuildLangTests(unittest.TestCase):
    def setUp(self):
        self.ru = project.create("RU отчёт", "вопрос", slug=f"ri-ru-{id(self)}")
        self.en = project.create("EN report", "question", slug=f"ri-en-{id(self)}", lang="en")

    def test_en_report_localized(self):
        text = export.build(self.en).read_text(encoding="utf-8")
        self.assertIn("# Appendix A. Claims registry", text)
        self.assertIn("# Appendix B. Sources", text)
        self.assertIn("| ID | Title | Link / file | Origin | Retrieved |", text)
        self.assertIn("# Appendix D. Transparency", text)
        self.assertIn("strategy and rationale", text)
        self.assertIn("Total:", text)  # блок стоимости переведён
        self.assertNotIn("Приложение", text)
        self.assertNotIn("Итого:", text)
        self.assertNotIn("стратегия и обоснование", text)

    def test_ru_report_unchanged(self):
        text = export.build(self.ru).read_text(encoding="utf-8")
        self.assertIn("# Приложение A. Реестр утверждений", text)
        self.assertIn("# Приложение B. Источники", text)
        self.assertIn("| ID | Название | Ссылка / файл | Происхождение | Получено |", text)
        self.assertIn("# Приложение D. Прозрачность", text)
        self.assertIn("стратегия и обоснование", text)
        self.assertIn("Итого:", text)


class CostSummaryLangTests(unittest.TestCase):
    def setUp(self):
        self.en = project.create("EN cost", "question", slug=f"ri-cost-en-{id(self)}", lang="en")

    def test_en_cost_summary(self):
        s = cost.summary_text(self.en, "en")
        self.assertIn("Total:", s)
        self.assertNotIn("Итого:", s)

    def test_default_ru_unchanged(self):
        self.assertIn("Итого:", cost.summary_text(self.en))

    def test_cli_cost_follows_project_lang(self):
        out = run_cli(["--project", self.en.name, "cost"])
        self.assertIn("Total:", out)
        self.assertNotIn("Итого:", out)


class FinishSummaryLangTests(unittest.TestCase):
    def setUp(self):
        self.ru = project.create("RU finish", "вопрос", slug=f"ri-fin-ru-{id(self)}")
        self.en = project.create("EN finish", "question", slug=f"ri-fin-en-{id(self)}", lang="en")

    @staticmethod
    def _res(pdir: Path) -> dict:
        return {"artifacts": [pdir / "outputs" / "REPORT.md"],
                "missing_docs": ["01_research_plan.md"],
                "stale_warnings": ["⚠ registry changed"]}

    def test_en_finish_summary(self):
        s = finish.summary_text(self._res(self.en), "en")
        self.assertIn("Assembled (1):", s)
        self.assertIn("Missing documents", s)
        self.assertNotIn("Собрано", s)

    def test_default_ru_unchanged(self):
        s = finish.summary_text(self._res(self.ru))
        self.assertIn("Собрано (1):", s)
        self.assertIn("Нет документов", s)


class ParticipateGuideLangTests(unittest.TestCase):
    def setUp(self):
        self.ru = project.create("RU guide", "вопрос", slug=f"ri-g-ru-{id(self)}")
        self.en = project.create("EN guide", "question", slug=f"ri-g-en-{id(self)}", lang="en")

    def test_guide_errors_in_project_lang(self):
        with self.assertRaises(PfsError) as cm:
            participate.guide(self.en, "  ", "topic")
        self.assertIn("persona", str(cm.exception))
        with self.assertRaises(PfsError) as cm:
            participate.guide(self.ru, "  ", "тема")
        self.assertIn("персону", str(cm.exception))

    def test_en_guide_wrapper_localized(self):
        text = participate.guide(self.en, "Ops lead", "churn").read_text(encoding="utf-8")
        self.assertIn("# Interview guide: churn", text)
        self.assertIn("- Persona: Ops lead", text)
        self.assertNotIn("Гайд интервью", text)
        self.assertNotIn("Персона:", text)

    def test_ru_guide_wrapper_unchanged(self):
        text = participate.guide(self.ru, "Руководитель", "отток").read_text(encoding="utf-8")
        self.assertIn("# Гайд интервью: отток", text)
        self.assertIn("- Персона: Руководитель", text)


class ProjectExistsLangTests(unittest.TestCase):
    def test_new_existing_slug_en_message(self):
        slug = f"ri-dup-en-{id(self)}"
        project.create("First", "q", slug=slug, lang="en")
        with self.assertRaises(PfsError) as cm:
            run_cli(["new", "Second", "q", "--slug", slug, "--lang", "en"])
        self.assertIn("already exists", str(cm.exception))

    def test_new_existing_slug_ru_unchanged(self):
        slug = f"ri-dup-ru-{id(self)}"
        project.create("Первый", "в", slug=slug)
        with self.assertRaises(PfsError) as cm:
            run_cli(["new", "Второй", "в", "--slug", slug])
        self.assertIn("уже существует", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
