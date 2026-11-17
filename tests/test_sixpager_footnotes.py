"""PRO-49: сноски six-pager и настоящие DOCX-footnotes.

Сквозные сноски [^N] в порядке первого упоминания: читатель идёт от числа к источнику
(издатель, название, дата, URL, сила A–D). В списке — только процитированные источники;
синтетика — отдельным блоком с пометкой «гипотезы, не доказательство»; теги C### остаются
в REPORT.md (Приложение A — реестр утверждений); `pfs docx` собирает word/footnotes.xml.

Запуск: python3 -m unittest discover -s tests -p "test_sixpager_footnotes.py" -v
"""
import os
import tempfile
import unittest
import zipfile
from pathlib import Path

TMP = tempfile.mkdtemp(prefix="pfs-test-fn-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from tools.pfs import claims, docx, export, project, sources  # noqa: E402


def fresh(slug):
    return project.create(f"Сноски {slug}", "Почему падает удержание?", slug=slug)


_PDIR = None


def fixture():
    """Общий проект-фикстура (лениво, один раз): источники, утверждения, 02_situation.md."""
    global _PDIR
    if _PDIR is not None:
        return _PDIR
    pdir = fresh("fn")
    out = pdir / "outputs"
    sources.add(pdir, text="Отчёт о рынке труда: 109 000 вакансий, динамика. " * 5,
                title="Рынок вакансий", url="https://hh.ru/article/1", published="2026-05-01")  # S001
    sources.add(pdir, text="Отчёт о динамике удержания абонентов. " * 5,
                title="Динамика удержания", url="https://example.org/report")                   # S002
    sources.add(pdir, text="Никем не процитированный источник, лишний. " * 5,
                title="Неиспользуемый", url="https://unused.example.com/x")                     # S003
    sources.add(pdir, text="Синтетическое интервью с ИИ-респондентом Markus. " * 5,
                title="Персона Markus (ИИ-респондент)", origin="synthetic")                     # S004
    claims.add(pdir, "На рынке 109 000 вакансий", "fact", ["S001"], grade="B")                      # C001
    claims.add(pdir, "Отток растёт третий месяц", "assumption")                                     # C002 — без источников
    claims.add(pdir, "Источники расходятся в динамике", "hypothesis", ["S002", "S001"], grade="A")  # C003
    claims.add(pdir, "Сегмент реагирует на напоминания", "hypothesis", ["S004"], grade="C")         # C004
    (out / "02_situation.md").write_text(
        "# Ситуация\n## Короткий ответ\nНа рынке 109 000 вакансий [C001], отток растёт третий месяц [C002]\n"
        "## Противоречия\n- источники расходятся в динамике [C003]; внешний ориентир — отраслевой бенчмарк [S002]\n"
        "## Сегменты\n- абоненты 55+: сегмент реагирует на напоминания о подозрительных звонках; "
        "персона Markus из синтетического интервью готова платить за семейный пакет и уведомления близким [C004]\n",
        encoding="utf-8")
    # PRO-46: после отказа от вставки документов теги в каркасе живут в расчётных
    # артефактах — явной KPI-таблице 06 (PRO-48); сноски собираются из её ячеек.
    (out / "06_validation_plan.md").write_text(
        "# План\n## KPI\n"
        "| Плоскость | Метрика | Формула | База (дата, источник) | Цель к сроку | "
        "Порог действия (остановить) | Контр-метрика |\n"
        "|---|---|---|---|---|---|---|\n"
        "| Бизнес | Отток платящих | 1 − удержание 30 дней | рынок 109 000 вакансий "
        "(2026-05-01, [S001]) | отток 8% → 5% к 90 дн | отток выше 10% → стоп | жалобы на фильтр |\n"
        "| Продукт | Удержание M1 | доля активных на 30-й день | источники расходятся в динамике "
        "(2026-05-01, [C003]) | 38% → 45% к 90 дн | ниже 41% → гейт 30 дней | активация |\n"
        "| Продукт | Реакция сегмента 55+ | доля ответивших на напоминание | 12% (2026-05-01, [S004]) "
        "| ≥ 20% к 60 дн | ниже 8% → сегмент закрыт | конверсия в оплату |\n",
        encoding="utf-8")
    export.build_six_pager(pdir, with_calcs=False)
    _PDIR = pdir
    return pdir


class SixPagerFootnotesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pdir = fixture()
        cls.text = (cls.pdir / "outputs" / "SIX_PAGER.md").read_text(encoding="utf-8")
        cls.src_dates = {r["id"]: (r.get("published") or r["retrieved"])[:10]
                         for r in sources.load(cls.pdir)}

    def test_tags_replaced_by_sequential_footnotes(self):
        # порядок первого упоминания: S001=1 (KPI-база), S002=2 (через C003 → [^2][^1]),
        # S004=3 (синтетика); сырых тегов в каркасе не остаётся (реестр — REPORT.md)
        self.assertIn("109 000 вакансий (2026-05-01, [^1])", self.text)
        self.assertIn("источники расходятся в динамике (2026-05-01, [^2][^1])", self.text)
        self.assertIn("12% (2026-05-01, [^3])", self.text)
        for tag in ("[C001]", "[C002]", "[C003]", "[C004]", "[S001]", "[S002]", "[S004]"):
            self.assertNotIn(tag, self.text)

    def test_only_cited_sources_listed(self):
        self.assertNotIn("S003", self.text)  # неиспользуемый источник не попадает в список
        self.assertIn("[^1]: **S001** — hh.ru — Рынок вакансий — 2026-05-01 — "
                      "https://hh.ru/article/1 — сила A", self.text)  # худший grade: C003 (A) тоже цитирует S001
        self.assertIn("[^2]: **S002** — example.org — Динамика удержания — "
                      f"{self.src_dates['S002']} — https://example.org/report — сила A", self.text)
        self.assertNotIn("[^4]:", self.text)

    def test_synthetic_block_separate_and_marked(self):
        self.assertIn("## Источники (сноски)", self.text)
        self.assertIn("Синтетические материалы", self.text)
        self.assertIn("гипотезы, не доказательство", self.text)
        # в каркас попадает только явная KPI-таблица 06: тег [C004] остаётся в 02,
        # поэтому сила у синтетической сноски не выводится (реестр тегов — REPORT.md)
        self.assertIn("[^3]: **S004** — Персона Markus (ИИ-респондент) — "
                      f"{self.src_dates['S004']}", self.text)
        # сквозная нумерация: реальные источники раньше синтетического блока
        main, syn = self.text.find("[^2]: **S002**"), self.text.find("[^3]: **S004**")
        self.assertLess(main, syn)

    def test_report_keeps_claim_tags(self):
        # теги C### переезжают в REPORT.md (Приложение A — реестр доказательств)
        report = export.build(self.pdir).read_text(encoding="utf-8")
        self.assertIn("# Приложение A. Реестр утверждений", report)
        self.assertIn("| C001 |", report)

    def test_deck_theses_without_footnote_markers(self):
        # дека строится из six-pager: маркеры [^N] и определения сносок в тезисы не попадают
        html = export.build_deck(self.pdir).read_text(encoding="utf-8")
        self.assertNotIn("[^", html)


class SixPagerWithoutCitedSourcesTests(unittest.TestCase):
    def test_no_cited_sources_hint(self):
        pdir = fresh("fn-empty")
        sources.add(pdir, text="Зарегистрированный, но не процитированный источник. " * 5, title="Никто")
        (pdir / "outputs" / "02_situation.md").write_text(
            "# Ситуация\n## Короткий ответ\nОтток растёт, тегов нет.\n", encoding="utf-8")
        text = export.build_six_pager(pdir, with_calcs=False).read_text(encoding="utf-8")
        self.assertIn("## Источники (сноски)", text)
        self.assertNotIn("**S001**", text)  # непроцитированный не выводится
        self.assertNotIn("[^1]:", text)


class DocxFootnotesTests(unittest.TestCase):
    DOCX_MD = ("# Отчёт\n\nРынок 109 000 вакансий[^1], гипотеза о сегменте[^2].\n\n"
               "## Источники (сноски)\n\n"
               "[^1]: **S001** — hh.ru — Рынок вакансий — 2026-05-01 — https://hh.ru/article/1 — сила B\n"
               "[^2]: **S004** — Персона Markus — 2026-11-01 — сила C\n")

    @classmethod
    def setUpClass(cls):
        cls.pdir = fixture()

    def test_docx_writes_real_footnotes(self):
        src = Path(TMP) / "six_fn.md"
        src.write_text(self.DOCX_MD, encoding="utf-8")
        out = docx.convert(src)
        with zipfile.ZipFile(out) as z:
            self.assertIsNone(z.testzip())
            doc = z.read("word/document.xml").decode("utf-8")
            fn = z.read("word/footnotes.xml").decode("utf-8")
            ct = z.read("[Content_Types].xml").decode("utf-8")
            rels = z.read("word/_rels/document.xml.rels").decode("utf-8")
        self.assertIn('<w:footnoteReference w:id="1"/>', doc)
        self.assertIn('<w:footnoteReference w:id="2"/>', doc)
        self.assertIn("Рынок 109 000 вакансий", doc)
        self.assertNotIn("[^1]", doc)   # маркер не остался текстом в теле
        self.assertNotIn("[^2]:", doc)  # определения не ушли в тело абзацами
        self.assertIn('<w:footnote w:id="1">', fn)
        self.assertIn("https://hh.ru/article/1", fn)
        self.assertIn('w:type="separator"', fn)
        self.assertIn("footnotes+xml", ct)
        self.assertIn("footnotes.xml", rels)

    def test_docx_footnote_text_bold_markup_not_literal(self):
        # текст сноски «**S001** — …» прогоняется через инлайн-форматтер тела (_runs):
        # в footnotes.xml литеральных «**» нет, S001 — настоящий жирный w:b-run
        src = Path(TMP) / "fn_bold.md"
        src.write_text(self.DOCX_MD, encoding="utf-8")
        out = docx.convert(src)
        with zipfile.ZipFile(out) as z:
            fn = z.read("word/footnotes.xml").decode("utf-8")
        self.assertNotIn("**", fn, "markdown-разметка ** не должна попадать в footnotes.xml")
        self.assertIn("<w:b/>", fn, "S001 выводится жирным w:b-run, а не звёздочками")
        self.assertIn("S001", fn)

    def test_docx_without_footnotes_has_no_part(self):
        src = Path(TMP) / "plain_fn.md"
        src.write_text("# Простой\nАбзац без сносок.\n", encoding="utf-8")
        out = docx.convert(src)
        with zipfile.ZipFile(out) as z:
            self.assertNotIn("word/footnotes.xml", z.namelist())
            doc = z.read("word/document.xml").decode("utf-8")
        self.assertIn("Абзац без сносок", doc)
        self.assertNotIn("footnoteReference", doc)

    def test_docx_unref_and_duplicate_defs_stay_valid(self):
        # ссылка [^3] без определения [^3]: не превращается в w:footnoteReference на
        # несуществующий id (иначе невалидный DOCX — Word предлагает «восстановить»):
        # она остаётся литеральным текстом; повторное [^1]: отбрасывается — двойное
        # w:id="1" в footnotes.xml тоже невалидно
        src = Path(TMP) / "fn_bad.md"
        src.write_text("# Отчёт\n\nОпределённая сноска[^1] и ссылка без определения[^3].\n\n"
                       "[^1]: **S001** — hh.ru — Рынок вакансий — 2026-05-01 — сила B\n"
                       "[^1]: Дубль определения — должен быть отброшен\n", encoding="utf-8")
        out = docx.convert(src)
        with zipfile.ZipFile(out) as z:
            self.assertIsNone(z.testzip(), "zip валиден: Word не предлагает «восстановить»")
            doc = z.read("word/document.xml").decode("utf-8")
            fn = z.read("word/footnotes.xml").decode("utf-8")
        self.assertIn('<w:footnoteReference w:id="1"/>', doc)     # определённая — настоящая сноска
        self.assertNotIn('<w:footnoteReference w:id="3"/>', doc)  # без определения — не ссылка
        self.assertIn("[^3]", doc)                                # …а литеральный текст в теле
        self.assertEqual(fn.count('<w:footnote w:id="1">'), 1)    # дубль определения отброшен
        self.assertIn("Рынок вакансий", fn)                       # первое определение побеждает
        self.assertNotIn("Дубль", fn)
        self.assertNotIn('<w:footnote w:id="3">', fn)

    def test_pfs_docx_on_six_pager(self):
        path = export.build_six_pager(self.pdir, with_calcs=False)
        out = docx.convert(path, Path(TMP) / "SIX_PAGER.docx")
        with zipfile.ZipFile(out) as z:
            doc = z.read("word/document.xml").decode("utf-8")
            fn = z.read("word/footnotes.xml").decode("utf-8")
        self.assertIn("<w:footnoteReference", doc)
        self.assertIn("S001", fn)          # сноска реального источника
        self.assertIn("https://hh.ru/article/1", fn)
        self.assertNotIn("[^", doc)        # ни маркеров, ни определений в теле: всё — сноски Word


if __name__ == "__main__":
    unittest.main()
