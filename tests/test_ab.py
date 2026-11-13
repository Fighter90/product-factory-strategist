"""PRO-71: `pfs ab` — дизайн A/B-теста по шаблону M-ab-test-design-template, проход
чек-листа M-ab-test-checklist и контекст AI-ревьюера M-ai-experiment-review-context.
MDE/выборка — формула из M-ab-testing (n = (z_α+z_β)²·2σ²/MDE², σ² = p(1−p)) и M-quant-methods.

Запуск: python3 -m unittest tests.test_ab -v
"""
import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

TMP = tempfile.mkdtemp(prefix="pfs-test-ab-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from tools.pfs import ab, claims, cli, core, kb, project, sources  # noqa: E402
from tools.pfs.core import PfsError  # noqa: E402


def run_cli(argv):
    buf = io.StringIO()
    args = cli.build_parser().parse_args(argv)
    with redirect_stdout(buf):
        args.f(args)
    return buf.getvalue()


def fresh(slug):
    return project.create(f"Тест {slug}", "Почему падает удержание подписчиков?", slug=slug)


def with_hypothesis(pdir):
    """Минимальный контекст: источник, гипотеза стратегии, план проверки (06)."""
    sources.add(pdir, text="Отток подписчиков 12% в месяц за полгода", title="Отчёт по оттоку")
    h = claims.add(pdir, "Если сократить форму отмены до одного шага, отток снизится на 1 п.п., "
                         "потому что сейчас отмена требует шести шагов", "hypothesis", ["S001"])
    (pdir / "outputs" / "06_validation_plan.md").write_text(
        "# План проверки\n\n"
        "## Гипотеза 1: Сокращение формы отмены снизит отток\n\n"
        "### Ожидаемое изменение\n\n- отток минус 1 п.п. за месяц [C001]\n\n"
        "### С чем сравниваем\n\n- A/B-тест, базовый отток 12% [S001]\n\n"
        "### Критерии решения\n\n- продолжаем, если отток снизится не меньше чем на 0,5 п.п.\n",
        encoding="utf-8")
    return h


class SampleSizeTests(unittest.TestCase):
    def test_formula_matches_map_example(self):
        # мини-пример из M-ab-testing: p=1,8%, MDE=1 п.п., α=5%, мощность 80% → ≈2 770 на группу
        self.assertTrue(2700 <= ab.sample_size(0.018, 0.01, 0.05, 0.8) <= 2850,
                        ab.sample_size(0.018, 0.01, 0.05, 0.8))

    def test_more_power_larger_sample(self):
        self.assertGreater(ab.sample_size(0.5, 0.02, 0.05, 0.9), ab.sample_size(0.5, 0.02, 0.05, 0.8))

    def test_smaller_mde_larger_sample(self):
        self.assertGreater(ab.sample_size(0.5, 0.01, 0.05, 0.8), ab.sample_size(0.5, 0.02, 0.05, 0.8))

    def test_invalid_params(self):
        with self.assertRaises(PfsError):
            ab.sample_size(0, 0.01)
        with self.assertRaises(PfsError):
            ab.sample_size(0.5, 1.5)


class DesignTests(unittest.TestCase):
    def setUp(self):
        self.pdir = fresh(f"ab{id(self)}")
        self.h = with_hypothesis(self.pdir)

    def test_creates_three_files(self):
        res = ab.design(self.pdir)
        self.assertEqual(Path(res["design"]).name, "06_ab_design_C001.md")
        self.assertEqual(Path(res["checklist"]).name, "ab_checklist_C001.md")
        self.assertEqual(Path(res["ai_review"]).name, "ab_ai_review_C001.md")
        for key in res:
            self.assertTrue(Path(res[key]).exists(), key)

    def test_design_doc_follows_template_sections_and_maps(self):
        text = Path(ab.design(self.pdir)["design"]).read_text(encoding="utf-8")
        for sec in ("## Бизнес", "## Метрики", "### Целевая", "### Прокси", "### Защитная",
                    "## Механизм принятия решений", "## Реализация теста",
                    "## Проверка гипотез", "## Результаты эксперимента", "## Выводы"):
            self.assertIn(sec, text, sec)
        # ссылки на карты базы знаний
        for card in ("M-ab-test-design-template", "M-ab-testing", "M-quant-methods",
                     "M-ab-test-checklist", "M-ai-experiment-review-context"):
            self.assertIn(card, text, card)
        # гипотеза из реестра с тегом
        self.assertIn("Если сократить форму отмены", text)
        self.assertIn(f"[{self.h['id']}]", text)

    def test_design_doc_pulls_data_from_project(self):
        text = Path(ab.design(self.pdir)["design"]).read_text(encoding="utf-8")
        self.assertIn("Почему падает удержание подписчиков?", text)  # вопрос из project.json
        self.assertIn("продолжаем, если отток снизится", text)       # критерии из 06
        self.assertIn("базовый отток 12%", text)                     # база сравнения из 06

    def test_design_doc_computes_sample_and_duration(self):
        n = ab.sample_size(0.018, 0.01)
        res = ab.design(self.pdir, baseline=0.018, mde=0.01, traffic=500, metric="Отток подписчиков")
        text = Path(res["design"]).read_text(encoding="utf-8")
        self.assertIn(str(n), text)                # выборка на группу
        self.assertIn("α = 0.05", text)
        self.assertIn("Отток подписчиков", text)   # целевая метрика подставлена

    def test_checklist_report_lists_open_items(self):
        text = Path(ab.design(self.pdir)["checklist"]).read_text(encoding="utf-8")
        self.assertIn("M-ab-test-checklist", text)
        for block in ("Блок 1", "Блок 2", "Блок 3", "Блок 4", "Блок 5", "Блок 6", "Блок 7"):
            self.assertIn(block, text, block)
        self.assertIn("Незакрытые пункты", text)   # незакрытое перечислено явно
        self.assertIn("- [ ]", text)

    def test_checklist_closes_items_when_params_given(self):
        text = Path(ab.design(self.pdir, metric="Отток", guardrail="CR до оплаты",
                              rules="успех: отток −1 п.п.", split_system="Experimentus, ID=user_id",
                              baseline=0.12, mde=0.01, traffic=1000)["checklist"]).read_text(encoding="utf-8")
        self.assertIn("- [x]", text)
        self.assertNotIn("- [ ] Система сплитования", text)  # закрыто параметром

    def test_ai_review_context_filled_with_product(self):
        text = Path(ab.design(self.pdir)["ai_review"]).read_text(encoding="utf-8")
        self.assertIn("M-ai-experiment-review-context", text)
        self.assertIn("M-genai-evals", text)
        self.assertIn("Если сократить форму отмены", text)   # гипотеза из проекта
        self.assertIn("S001", text)                          # доступные источники
        self.assertIn("Формат ответа", text)

    def test_idempotent_no_overwrite(self):
        res1 = ab.design(self.pdir)
        before = Path(res1["design"]).read_text(encoding="utf-8")
        Path(res1["design"]).write_text(before + "\n<!-- правка агента -->\n", encoding="utf-8")
        res2 = ab.design(self.pdir)
        self.assertEqual(res1, res2)
        self.assertIn("правка агента", Path(res2["design"]).read_text(encoding="utf-8"))

    def test_explicit_hypothesis_and_unknown(self):
        res = ab.design(self.pdir, hypothesis=self.h["id"])
        self.assertEqual(Path(res["design"]).name, f"06_ab_design_{self.h['id']}.md")
        with self.assertRaises(PfsError):
            ab.design(self.pdir, hypothesis="C999")

    def test_en_project_gets_english_doc(self):
        pdir = project.create("English product", "why is churn rising?", slug="ab-en", lang="en")
        sources.add(pdir, text="Churn 12% monthly", title="Churn report")
        claims.add(pdir, "If we shorten the cancel form, churn drops by 1pp because it takes six steps today",
                   "hypothesis", ["S001"])
        text = Path(ab.design(pdir)["design"]).read_text(encoding="utf-8")
        self.assertIn("## Business", text)
        self.assertIn("### Target", text)
        self.assertNotIn("## Бизнес", text)


class CliTests(unittest.TestCase):
    def test_cli_ab_creates_files(self):
        pdir = fresh(f"abcli{id(self)}")
        with_hypothesis(pdir)
        slug = pdir.name
        out = run_cli(["--project", slug, "ab", "--baseline", "0.12", "--mde", "0.01",
                       "--metric", "Отток", "--traffic", "2000"])
        self.assertIn("06_ab_design_C001.md", out)
        self.assertIn("ab_checklist_C001.md", out)
        self.assertIn("ab_ai_review_C001.md", out)
        self.assertTrue((pdir / "outputs" / "06_ab_design_C001.md").exists())


class StageCardsTests(unittest.TestCase):
    def test_validation_cards_include_ab_maps(self):
        cards = kb.cards_for("validation")
        self.assertIn("M-ab-test-design-template", cards)
        self.assertIn("M-ab-test-checklist", cards)
