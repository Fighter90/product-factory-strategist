"""PRO-45: release.yml — GitHub Release из CHANGELOG на тег + бэкфилл v1.2.1–v1.2.13.

Кейс: 13 тегов v1.2.1–v1.2.13 существуют, но объектов GitHub Release нет. Воркфлоу
.github/workflows/release.yml на push тега v* создаёт Release с секцией этой версии
из CHANGELOG.md; ручной прогон (workflow_dispatch) делает идемпотентный бэкфилл по
всем существующим тегам. Извлечение секции и план бэкфилда вынесены в stdlib-модуль
tools/release_notes.py, чтобы их можно было проверить тестами без сети и gh.

Особенности реального CHANGELOG, которые обязаны быть покрыты:
  - заголовки секций: «## 1.2.13 — дата · название» (без префикса v) и «## v…»;
  - точное сравнение версий: 1.2.1 не матчится на заголовок 1.2.13;
  - дубли заголовков (1.2.9, 1.1.0) — берём первое вхождение;
  - у v1.2.8 секции нет — используется fallback-текст, Release не ломается;
  - ANSI-мусор («[0m») из CHANGELOG не попадает в описание Release.

Запуск: python3 -m unittest tests.test_release_workflow -v
"""
import contextlib
import io
import os
import re
import subprocess
import sys
import tempfile
import unittest

from tools.release_notes import (
    backfill_plan,
    cmd_backfill,
    extract_section,
    fallback_notes,
    normalize_tag,
    parse_version,
    section_for_tag,
    sorted_version_tags,
)

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKFLOW = os.path.join(REPO, ".github", "workflows", "release.yml")

SAMPLE = """# Changelog

Вступительный текст до первой секции.

## 1.2.1 — 2026-01-01 · первая

### Added
- фича 1.2.1

## 1.2.2 — 2026-01-02 · вторая

### Fixed
- фикс 1.2.2
- ещё фикс

## 1.2.13 — 2026-01-03 · тринадцатая

### Added
- фича 1.2.13
"""


class ExtractSectionTests(unittest.TestCase):
    def test_middle_section_bounded_by_next_heading(self):
        """Секция 1.2.2: от заголовка до следующего «## », без соседних секций."""
        s = extract_section(SAMPLE, "1.2.2")
        self.assertIn("## 1.2.2", s)
        self.assertIn("фикс 1.2.2", s)
        self.assertNotIn("фича 1.2.1", s)
        self.assertNotIn("## 1.2.13", s)
        self.assertNotIn("фича 1.2.13", s)

    def test_first_and_last_sections(self):
        self.assertIn("фича 1.2.1", extract_section(SAMPLE, "1.2.1"))
        self.assertIn("фича 1.2.13", extract_section(SAMPLE, "1.2.13"))
        self.assertNotIn("фикс 1.2.2", extract_section(SAMPLE, "1.2.13"))

    def test_exact_version_no_prefix_match(self):
        """1.2.1 не матчится на заголовок 1.2.13 (строковый startswith сломал бы это)."""
        self.assertIsNone(extract_section(SAMPLE, "1.2.3"))
        self.assertIsNone(extract_section(SAMPLE, "1.2"))
        self.assertIn("фича 1.2.13", extract_section(SAMPLE, "1.2.13"))

    def test_duplicate_heading_takes_first_occurrence(self):
        dup = "## 1.2.9 — d1 · первый\n\n- а\n\n## 1.2.9 — d2 · второй\n\n- б\n"
        s = extract_section(dup, "1.2.9")
        self.assertIn("первый", s)
        self.assertNotIn("второй", s)

    def test_v_prefix_heading_form(self):
        s = extract_section("## v1.2.4 — дата · заголовок с v\n\n- тело\n", "1.2.4")
        self.assertIn("тело", s)

    def test_ansi_garbage_stripped(self):
        dirty = "## 1.2.5 — d · x\n\n[0m\x1b[31m- красная строка\x1b[0m\n[0m\n"
        s = extract_section(dirty, "1.2.5")
        self.assertNotIn("[0m", s)
        self.assertNotIn("\x1b[", s)
        self.assertIn("- красная строка", s)

    def test_missing_version_returns_none(self):
        self.assertIsNone(extract_section(SAMPLE, "9.9.9"))
        self.assertIsNone(extract_section("", "1.0.0"))

    def test_tag_forms_accepted(self):
        """С тегом v… и без — одно и то же: normalize_tag срезает префикс."""
        self.assertEqual(normalize_tag("v1.2.13"), "1.2.13")
        self.assertEqual(normalize_tag("1.2.13"), "1.2.13")
        self.assertIn("фича 1.2.13", extract_section(SAMPLE, normalize_tag("v1.2.13")))


class VersionParsingTests(unittest.TestCase):
    def test_parse_version(self):
        self.assertEqual(parse_version("v1.2.13"), (1, 2, 13))
        self.assertEqual(parse_version("1.2"), (1, 2))
        self.assertIsNone(parse_version("vnext"))
        self.assertIsNone(parse_version("main"))

    def test_sorted_version_tags_numeric_not_lexicographic(self):
        tags = ["v1.2.10", "v1.2.2", "v1.0.0", "v1.2.9", "vnext"]
        self.assertEqual(
            sorted_version_tags(tags),
            ["v1.0.0", "v1.2.2", "v1.2.9", "v1.2.10"],
        )


class BackfillPlanTests(unittest.TestCase):
    def test_plan_sorted_and_skips_existing_releases(self):
        plan = backfill_plan(
            ["v1.2.2", "v1.2.10", "v1.0.0"],
            SAMPLE,
            existing_releases={"v1.0.0"},
        )
        planned = [p["tag"] for p in plan]
        self.assertEqual(planned, ["v1.2.2", "v1.2.10"])
        # v1.2.2 есть в SAMPLE — секция; v1.2.10 секции не имеет — fallback.
        self.assertTrue(plan[0]["from_changelog"])
        self.assertIn("фикс 1.2.2", plan[0]["notes"])
        self.assertFalse(plan[1]["from_changelog"])

    def test_plan_fallback_for_missing_section(self):
        plan = backfill_plan(["v1.2.8"], SAMPLE, existing_releases=set())
        self.assertEqual(len(plan), 1)
        self.assertFalse(plan[0]["from_changelog"])
        self.assertTrue(plan[0]["notes"].strip())
        self.assertIn("v1.2.8", plan[0]["notes"])

    def test_fallback_notes_nonempty_for_any_tag(self):
        for tag in ("v1.2.8", "v9.9.9"):
            self.assertIn(tag, fallback_notes(tag))

    def test_non_version_tags_ignored(self):
        plan = backfill_plan(["main", "vnext", "v1.2.2"], SAMPLE, existing_releases=set())
        self.assertEqual([p["tag"] for p in plan], ["v1.2.2"])


class RepoChangeelogIntegrationTests(unittest.TestCase):
    """Реальный CHANGELOG.md репозитория: секции v1.2.1–v1.2.13 извлекаются."""

    @classmethod
    def setUpClass(cls):
        with open(os.path.join(REPO, "CHANGELOG.md"), encoding="utf-8") as f:
            cls.changelog = f.read()

    def test_v1_2_13(self):
        s = section_for_tag(self.changelog, "v1.2.13")
        self.assertIn("1.2.13", s)
        self.assertIn("PRO-26", s)
        self.assertNotIn("## 1.2.12", s)

    def test_v1_2_1(self):
        s = section_for_tag(self.changelog, "v1.2.1")
        self.assertIn("гэп-трекинг", s)
        self.assertNotIn("## 1.2.0", s)

    def test_v1_2_12(self):
        self.assertIn("review lock", section_for_tag(self.changelog, "v1.2.12"))

    def test_no_ansi_garbage_in_real_sections(self):
        for tag in ("v1.2.13", "v1.2.12", "v1.2.1"):
            self.assertNotIn("[0m", section_for_tag(self.changelog, tag))

    def test_v1_2_8_has_no_section(self):
        """У v1.2.8 в CHANGELOG секции нет — бэкфилл уходит в fallback, не падает."""
        self.assertIsNone(section_for_tag(self.changelog, "v1.2.8"))
        plan = backfill_plan(["v1.2.8"], self.changelog, existing_releases=set())
        self.assertEqual(len(plan), 1)
        self.assertFalse(plan[0]["from_changelog"])

    def test_all_target_tags_planned(self):
        """Критерий приёмки: для каждого из v1.2.1–v1.2.13 бэкфилл даёт Release с описанием."""
        tags = ["v1.2.%d" % i for i in range(1, 14)]
        plan = backfill_plan(tags, self.changelog, existing_releases=set())
        self.assertEqual({p["tag"] for p in plan}, set(tags))
        for p in plan:
            self.assertTrue(p["notes"].strip(), p["tag"])


class CliTests(unittest.TestCase):
    def test_cli_prints_section_for_tag(self):
        out = subprocess.run(
            [sys.executable, os.path.join("tools", "release_notes.py"), "v1.2.13"],
            cwd=REPO, capture_output=True, text=True,
        )
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("1.2.13", out.stdout)
        self.assertIn("PRO-26", out.stdout)
        self.assertNotIn("## 1.2.12", out.stdout)

    def test_cli_backfill_dry_run_lists_target_tags(self):
        """Бэкфилл-план печатается по инъекция тегов, а не по реальному `git tag`.

        Ревью note 1: в CI actions/checkout по умолчанию не фетчит теги, поэтому
        тест не имеет права зависеть от тегов чекаута — cmd_backfill принимает
        tags= и changelog_path= (прокинут из --changelog, note 2).
        """
        fixture = SAMPLE + "\n## 1.2.8 — 2026-01-08 · восьмая\n\n- фича 1.2.8\n"
        tags = ["v1.2.%d" % i for i in range(1, 14)]
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = cmd_backfill(True, changelog_path=os.path.join(REPO, "CHANGELOG.md"),
                              tags=tags)
        self.assertEqual(rc, 0)
        out = buf.getvalue()
        for i in range(1, 14):
            self.assertIn("v1.2.%d" % i, out)
        self.assertIn("DRY-RUN", out)

    def test_cli_backfill_honors_changelog_option(self):
        """Ревью note 2: --changelog не игнорируется с --backfill.

        У v1.2.8 в реальном CHANGELOG секции нет (будет «fallback»), а в
        фикстуре секция есть — если cmd_backfill читает реальный CHANGELOG
        вместо переданного пути, в выводе будет «fallback», а не «секция CHANGELOG».
        """
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "CHANGELOG-fixture.md")
            with open(path, "w", encoding="utf-8") as f:
                f.write("# Changelog\n\n## 1.2.8 — d · фикстурная секция\n\n"
                        "- фича из фикстуры\n")
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = cmd_backfill(True, changelog_path=path, tags=["v1.2.8"])
        self.assertEqual(rc, 0)
        self.assertIn("секция CHANGELOG", buf.getvalue())
        self.assertNotIn("fallback", buf.getvalue())

    def test_cli_backfill_missing_changelog_fails(self):
        """--backfill с несуществующим --changelog — ошибка выхода 1 (не молчаливый
        игнор пути в пользу CHANGELOG_PATH по умолчанию)."""
        out = subprocess.run(
            [sys.executable, os.path.join("tools", "release_notes.py"),
             "--backfill", "--dry-run", "--changelog",
             os.path.join(tempfile.gettempdir(), "no-such-changelog-pro45.md")],
            cwd=REPO, capture_output=True, text=True,
        )
        self.assertEqual(out.returncode, 1)
        self.assertIn("не найден", out.stderr)
        self.assertIn("no-such-changelog-pro45.md", out.stderr)

    def test_cli_backfill_injected_tags_missing_section_fallback(self):
        """Инъекция тегов без секции в CHANGELOG — план использует fallback-текст."""
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = cmd_backfill(True, changelog_path=os.path.join(REPO, "CHANGELOG.md"),
                              tags=["v1.2.8"])
        self.assertEqual(rc, 0)
        self.assertIn("v1.2.8", buf.getvalue())
        self.assertIn("fallback", buf.getvalue())


class WorkflowFileTests(unittest.TestCase):
    """Workflow проверяем текстовыми утверждениями — pyyaml в зависимостях нет."""

    @classmethod
    def setUpClass(cls):
        assert os.path.exists(WORKFLOW), (
            ".github/workflows/release.yml отсутствует: воркфлоу Release не создан"
        )
        with open(WORKFLOW, encoding="utf-8") as f:
            cls.text = f.read()

    def test_triggers_on_version_tags(self):
        self.assertRegex(self.text, r"tags:")
        self.assertRegex(self.text, r"v\*")

    def test_manual_dispatch_for_backfill(self):
        self.assertIn("workflow_dispatch", self.text)

    def test_creates_release_from_changelog_script(self):
        self.assertIn("release_notes.py", self.text)
        self.assertIn("gh release create", self.text)

    def test_tag_step_guards_existing_release(self):
        """Ревью note 3: повторный прогон по тегу не падает и не дублирует Release —
        перед `gh release create` проверяется `gh release view` (как в бэкфилле)."""
        self.assertIn('gh release view "$GITHUB_REF_NAME"', self.text)

    def test_step_conditions_use_event_name(self):
        """Ревью note 4: шаги разделяются по github.event_name (push/workflow_dispatch),
        а не по github.ref_type (последний может быть 'tag' и при dispatch)."""
        self.assertIn("github.event_name == 'push'", self.text)
        self.assertIn("github.event_name == 'workflow_dispatch'", self.text)
        self.assertNotIn("github.ref_type", self.text)

    def test_contents_write_permission(self):
        self.assertIn("contents: write", self.text)


if __name__ == "__main__":
    unittest.main()
