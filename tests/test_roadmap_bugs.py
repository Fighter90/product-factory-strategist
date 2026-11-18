#!/usr/bin/env python3
"""QA B-12/B-13: шаблон roadmap --spec и табличный формат этапов в 04."""

import io
import json as _json
import os
import tempfile
import unittest
from contextlib import redirect_stdout

TMP = tempfile.mkdtemp(prefix="pfs-test-road-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from pathlib import Path  # noqa: E402

from tools.pfs import cli, core, project, roadmap  # noqa: E402
from tools.pfs.core import PfsError  # noqa: E402


class SpecTemplateTests(unittest.TestCase):
    def test_missing_spec_creates_template(self):
        """BUG B-12: --spec без файла — создаётся шаблон с примером формата."""
        pdir = project.create("Road spec", "вопрос", slug="rd-spec")
        rel = str(pdir / "outputs" / "my-roadmap.json")
        with self.assertRaises(PfsError) as cm:
            roadmap.load_spec(pdir, rel)
        self.assertIn("шаблон", str(cm.exception))
        tpl = json_load(pdir / rel)
        self.assertIn("projects", tpl)
        self.assertIn("initiative", _json.dumps(tpl, ensure_ascii=False))

    def test_filled_spec_builds(self):
        pdir = project.create("Road fill", "вопрос", slug="rd-fill")
        spec = pdir / "roadmap.json"
        core.atomic_write(spec, __import__("json").dumps({
            "title": "Т", "projects": [{"name": "Этап 1", "initiative": "И",
                                        "start": "2026-Q4", "end": "2027-Q1",
                                        "status": "план", "features": [{"name": "a", "start": "2026-Q4", "end": "2027-Q1"}]}]},
            ensure_ascii=False))
        data, source = roadmap.load_spec(pdir, None)
        self.assertEqual(source, "roadmap.json")


def json_load(p: Path):
    return __import__("json").loads(p.read_text(encoding="utf-8"))


class TableFormatTests(unittest.TestCase):
    def test_table_stages_build(self):
        """BUG B-13: роадмап в 04 таблицей «Инициатива | Outcome | Срок» собирается."""
        pdir = project.create("Road table", "вопрос", slug="rd-table")
        (pdir / "outputs" / "04_product_strategy.md").write_text(
            "# Product strategy\n\n## Роадмап\n\n"
            "| Инициатива | Outcome (результат) | Срок |\n|---|---|---|\n"
            "| Онбординг-ревью | резюме проходит проверки до отправки | 2026-Q4 |\n"
            "| ATS-акценты | +20% к проходимости фильтров | 2027-Q1 |\n",
            encoding="utf-8")
        buf = io.StringIO()
        with redirect_stdout(buf):
            args = cli.build_parser().parse_args(["roadmap"])
            args.f(args)
        self.assertIn("roadmap-", buf.getvalue())
        data, source = roadmap.load_spec(pdir, None)
        self.assertEqual(source, "04_product_strategy.md")
        self.assertEqual(len(data["projects"]), 2)
        self.assertEqual(data["projects"][0]["initiative"], "Онбординг-ревью")

    def test_list_format_still_works(self):
        """Старый список-формат не сломан."""
        pdir = project.create("Road list", "вопрос", slug="rd-list")
        (pdir / "outputs" / "04_product_strategy.md").write_text(
            "# Product strategy\n\n"
            "- **Этап 1 (бета):** онбординг-ревью, подсказки ATS. **Результат:** 80% проходят фильтр.\n",
            encoding="utf-8")
        data, source = roadmap.load_spec(pdir, None)
        self.assertEqual(source, "04_product_strategy.md")
        self.assertEqual(len(data["projects"]), 1)
        self.assertIn("Результат", data["projects"][0]["comment"])

    def test_no_stages_message_names_both_formats(self):
        pdir = project.create("Road none", "вопрос", slug="rd-none")
        (pdir / "outputs" / "04_product_strategy.md").write_text(
            "# Product strategy\n\nНет роадмапа здесь.\n", encoding="utf-8")
        with self.assertRaises(PfsError) as cm:
            roadmap.load_spec(pdir, None)
        self.assertIn("таблица", str(cm.exception))
        self.assertIn("--spec", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
