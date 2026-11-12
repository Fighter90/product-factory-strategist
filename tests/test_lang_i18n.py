"""PRO-57: язык проекта (`pfs new --lang`, `pfs lang`), i18n-сообщения CLI и EN-проверки quality gate.

EN-прогон: project.json → lang=en; сообщения status/next/check на английском;
`pfs check --strict` проходит на EN-заголовках из config/quality_gate.json → "en".
RU-прогон не сломан: по умолчанию lang=ru и строки как раньше.

Запуск: python3 -m unittest tests.test_lang_i18n -v
"""
import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout

TMP = tempfile.mkdtemp(prefix="pfs-test-i18n-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from pathlib import Path  # noqa: E402

from tools.pfs import check, claims, cli, core, i18n, project, sources  # noqa: E402
from tools.pfs.core import PfsError  # noqa: E402


def run_cli(argv):
    buf = io.StringIO()
    args = cli.build_parser().parse_args(argv)
    with redirect_stdout(buf):
        args.f(args)
    return buf.getvalue()


def make_en_registry(pdir: Path) -> None:
    """Минимальный реестр для EN-прогона: источник и активный факт."""
    sources.add(pdir, text="Retention grew 40% after the onboarding change", title="Metrics 2026")
    claims.add(pdir, "Retention grew 40% after the onboarding change [C001]", "fact", ["S001"], quote="40%")


# EN-документы: заголовки в точности как в config/quality_gate.json → "en" и
# knowledge/templates/en/. Каждое число с единицей — с тегом, чтобы не сыпать warnings.
EN_DOCS = {
    "02_situation.md": (
        "# Situation: demo\n\n## Quick answer\n\nRetention is recovering [C001].\n\n"
        "## What we know\n\n- Retention grew 40% [C001] (grade B)\n\n"
        "## What we don't know\n\n| Gap | Why | How to learn |\n|---|---|---|\n\n"
        "## Questions that could change the decision\n\n1. Which cohort?\n"),
    "03_options.md": (
        "# Options: demo\n\n## Option A: Keep as is\n\nEssence: base forecast.\n\n"
        "### Objections\n\n- churn continues\n\n"
        "## Option B: Onboarding bundle\n\n### Objections\n\n- cost\n\n"
        "## Option C: Shut down the direction\n\n### Objections\n\n- none\n"),
    "04_product_strategy.md": (
        "# Product strategy: demo\n\n## Audience\n\n- new users [C001]\n\n"
        "## Alternatives\n\n| Current way | Why chosen |\n|---|---|\n\n"
        "## Chosen direction\n\n- Option B\n\n## Conscious trade-offs\n\n- no push\n\n"
        "## Economics\n\n- LTV 3x CAC [C001]\n"),
    "05_comms_strategy.md": (
        "# Comms strategy: demo\n\n## Audience and situation\n\n- new users\n\n"
        "## Barrier\n\n- distrust\n\n## Key message\n\n- one phrase\n\n"
        "## Proof\n\n| Point | Evidence [C001] |\n|---|---|\n\n"
        "## Role of channels\n\n| Channel | Job |\n|---|---|\n\n"
        "## Promises backed by the product\n\n| Promise | Backing |\n|---|---|\n"
        "| onboarding checklist | shipped feature [C001] |\n"),
    "06_validation_plan.md": (
        "# Validation plan: demo\n\n## Expected change\n\nretention +5pp [C001]\n\n"
        "## Comparison baseline\n\nA/B test\n\n## Observation window\n\n4 weeks\n\n"
        "## Counter-metrics\n\n| Counter-metric | Stop threshold |\n|---|---|\n\n"
        "## Decision criteria\n\n- continue if +3pp\n"),
}


class NewLangTests(unittest.TestCase):
    def test_new_default_lang_ru(self):
        pdir = project.create("Язык по умолчанию", "вопрос", slug="il-ru")
        self.assertEqual(core.read_json(pdir / "project.json").get("lang"), "ru")

    def test_new_lang_en_writes_meta_and_brief(self):
        pdir = project.create("English project", "question", slug="il-en", lang="en")
        self.assertEqual(core.read_json(pdir / "project.json").get("lang"), "en")
        brief = (pdir / "outputs" / "00_brief.md").read_text(encoding="utf-8")
        self.assertIn("Brief", brief)
        self.assertIn("Verbatim request", brief)

    def test_cli_new_with_lang_flag(self):
        run_cli(["new", "CLI en", "question", "--slug", "il-cli", "--lang", "en"])
        meta = core.read_json(core.project_dir("il-cli") / "project.json")
        self.assertEqual(meta["lang"], "en")


class LangCommandTests(unittest.TestCase):
    def test_lang_show_set_and_instruction_pointer(self):
        project.create("Lang cmd", "q", slug="il-cmd")
        core.set_active("il-cmd")
        self.assertIn("ru", run_cli(["lang"]))
        run_cli(["lang", "en"])
        meta = core.read_json(core.project_dir("il-cmd") / "project.json")
        self.assertEqual(meta["lang"], "en")
        out = run_cli(["lang"])
        self.assertIn("en", out)
        self.assertIn("AGENTS_EN.md", out)  # указатель на английские инструкции
        with self.assertRaises(SystemExit):
            run_cli(["lang", "de"])  # только ru|en


class CheckEnglishTests(unittest.TestCase):
    def setUp(self):
        self.pdir = project.create("EN check", "question", slug=f"il-check-{id(self)}", lang="en")
        make_en_registry(self.pdir)
        for name, text in EN_DOCS.items():
            (self.pdir / "outputs" / name).write_text(text, encoding="utf-8")

    def test_check_strict_passes_on_en_headings(self):
        res = check.run(self.pdir)
        self.assertEqual(res["errors"], [], f"ожидали чистый прогон, ошибки: {res['errors']}")
        out = run_cli(["--project", self.pdir.name, "check", "--strict"])  # не должен упасть
        self.assertIn("errors", out)

    def test_check_reports_missing_en_section_in_english(self):
        (self.pdir / "outputs" / "06_validation_plan.md").write_text(
            "# Validation plan\n\nnothing yet\n", encoding="utf-8")
        res = check.run(self.pdir)
        self.assertTrue(any("What we know" not in e and "06_validation_plan.md" in e for e in res["errors"])
                        or any("Expected change" in e for e in res["errors"]),
                        f"нет ошибки про EN-раздел: {res['errors']}")
        report = check.report_text(res, lang="en")
        self.assertIn("errors", report)
        self.assertNotIn("Контроль качества", report)

    def test_report_text_ru_unchanged(self):
        report = check.report_text(check.run(self.pdir), lang="ru")
        self.assertIn("Контроль качества", report)


class StatusNextI18nTests(unittest.TestCase):
    def test_status_next_in_english_for_en_project(self):
        pdir = project.create("EN status", "question", slug="il-status", lang="en")
        st = project.status_text(pdir)
        self.assertIn("PROJECT:", st)
        self.assertNotIn("ПРОЕКТ:", st)
        nt = project.next_text(pdir)
        self.assertIn("WHAT TO DECIDE NOW", nt)
        self.assertNotIn("ЧТО РЕШАТЬ СЕЙЧАС", nt)

    def test_status_next_ru_default_unchanged(self):
        pdir = project.create("RU status", "вопрос", slug="il-status-ru")
        self.assertIn("ПРОЕКТ:", project.status_text(pdir))
        self.assertIn("ЧТО РЕШАТЬ СЕЙЧАС", project.next_text(pdir))

    def test_awaiting_human_line_localized(self):
        pdir = project.create("EN wait", "question", slug="il-wait", lang="en")
        project.ask_human(pdir, "Which option?", ["A", "B"])
        self.assertIn("AWAITING", project.status_text(pdir))


class QualityGateConfigTests(unittest.TestCase):
    def test_gate_has_ru_and_en_blocks(self):
        cfg = json.loads((core.CONFIG / "quality_gate.json").read_text(encoding="utf-8"))
        for lang in ("ru", "en"):
            self.assertIn(lang, cfg, f"нет блока {lang} в quality_gate.json")
            docs = cfg[lang]["documents"]
            for name in ("02_situation.md", "03_options.md", "04_product_strategy.md",
                         "05_comms_strategy.md", "06_validation_plan.md"):
                self.assertIn(name, docs)
        # EN-заголовки согласованы с EN-шаблонами (выборочно)
        en_secs = cfg["en"]["documents"]["02_situation.md"]["required_sections"]
        self.assertIn("What we know", en_secs)
        self.assertIn("What we don't know", en_secs)
        en_opts = cfg["en"]["documents"]["03_options.md"]
        self.assertIn("keep as is", en_opts["status_quo_keywords"])
        self.assertTrue(any("shut down" in k for k in en_opts["exit_keywords"]))


class I18nModuleTests(unittest.TestCase):
    def test_lang_of_defaults_to_ru(self):
        pdir = project.create("lang of", "q", slug="il-langof")
        self.assertEqual(i18n.lang_of(pdir), "ru")
        self.assertEqual(i18n.lang_of(Path(TMP) / "нет-такого"), "ru")
        self.assertEqual(i18n.lang_of(None), "ru")

    def test_t_falls_back_to_ru_and_kwargs(self):
        self.assertEqual(i18n.t("ru", "check_header", score=90, errors=0, warnings=1),
                         "Контроль качества: 90/100 | ошибок 0, предупреждений 1")
        self.assertIn("errors 0", i18n.t("en", "check_header", score=90, errors=0, warnings=1))
        self.assertEqual(i18n.t("en", "нет-такого-ключа"), "нет-такого-ключа")

    def test_active_lang_reads_active_project(self):
        project.create("active lang en", "q", slug="il-active", lang="en")
        core.set_active("il-active")
        self.assertEqual(i18n.active_lang(), "en")


if __name__ == "__main__":
    unittest.main()
