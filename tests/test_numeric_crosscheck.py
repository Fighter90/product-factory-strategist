"""PRO-26: числовой кросс-чек — `pfs check` сверяет числа активных утверждений
с числами заголовков источников и числа цитат (quote) с текстом источников
(sources/S###.md).

Кейс из аудита: утверждение C007 и документы говорили «19 локалей», а заголовки
источников S001/S006 в реестре оставались «17 локалей» — противоречие дожило
до финального аудита. Теперь расхождение ловится автоматически.

Запуск: python3 -m unittest tests.test_numeric_crosscheck -v
"""
import os
import tempfile
import unittest

TMP = tempfile.mkdtemp(prefix="pfs-test-numcross-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from tools.pfs import check, claims, project, sources  # noqa: E402

TITLE_17 = "Продукт: 17 локалей"
BODY_17 = "Продукт доступен на 17 локалях. " * 6
M_TITLE = "числа утверждения"
M_QUOTE = "числа из цитаты"


class NumericCrosscheckTests(unittest.TestCase):
    def setUp(self):
        self.pdir = project.create(f"Числа {id(self)}", "Почему падает удержание подписчиков?",
                                   slug=f"num{id(self)}")

    def _warns(self):
        return check.run(self.pdir)["warnings"]

    def test_claim_vs_title_mismatch_warns(self):
        """Критерий приёмки: «17 в заголовке vs 19 в утверждении» → warning
        с парой C###/S### и обоими числами."""
        sources.add(self.pdir, text=BODY_17, title=TITLE_17)
        c = claims.add(self.pdir, "Продукт поддерживает 19 локалей", "fact", ["S001"], grade="B")
        pair = f"{c['id']}/S001"
        w = [x for x in self._warns() if pair in x and M_TITLE in x]
        self.assertTrue(w, self._warns())
        self.assertIn("19", w[0])
        self.assertIn("17", w[0])

    def test_claim_matches_title_is_quiet(self):
        """Критерий приёмки: чистый проект (числа совпадают) — новых предупреждений нет."""
        sources.add(self.pdir, text=BODY_17, title=TITLE_17)
        claims.add(self.pdir, "Продукт поддерживает 17 локалей", "fact", ["S001"], grade="B")
        self.assertFalse(any(M_TITLE in x or M_QUOTE in x for x in self._warns()), self._warns())

    def test_intersecting_numbers_are_quiet(self):
        """Пересечение хотя бы по одному числу — расхождения нет (консервативно:
        утверждение вправе содержать числа сверх заголовка)."""
        sources.add(self.pdir, text=BODY_17, title=TITLE_17)
        claims.add(self.pdir, "17 локалей и рост конверсии на 12%", "fact", ["S001"], grade="B")
        self.assertFalse(any(M_TITLE in x for x in self._warns()), self._warns())

    def test_claim_numbers_without_title_numbers_quiet(self):
        """В утверждении числа, в заголовке нет — сверять не с чем, тревоги нет."""
        sources.add(self.pdir, text=BODY_17, title="Продукт: локали")
        claims.add(self.pdir, "Продукт поддерживает 19 локалей", "fact", ["S001"], grade="B")
        self.assertFalse(any(M_TITLE in x for x in self._warns()), self._warns())

    def test_years_ignored(self):
        """Годы 1900–2099 — даты, а не показатели: заголовок «Отчёт за 2025 год»
        против утверждения «Рынок 40 млрд» ложной тревоги не даёт."""
        sources.add(self.pdir, text="Годовой отчёт о рынке. " * 6, title="Отчёт за 2025 год")
        claims.add(self.pdir, "Рынок 40 млрд", "fact", ["S001"], grade="B")
        self.assertFalse(any(M_TITLE in x or M_QUOTE in x for x in self._warns()), self._warns())

    def test_decimal_comma_is_one_number(self):
        """«8,5» — одно число (русская десятичная запятая), а не «8» и «5»."""
        sources.add(self.pdir, text="Рынок 8,5 млрд евро. " * 6, title="Рынок 8,5 млрд")
        claims.add(self.pdir, "Рынок 8,5 млрд", "fact", ["S001"], grade="B")
        self.assertFalse(any(M_TITLE in x or M_QUOTE in x for x in self._warns()), self._warns())

    def test_inactive_claim_not_checked(self):
        """Отозванное/замещённое утверждение кросс-чек не проверяет."""
        sources.add(self.pdir, text=BODY_17, title=TITLE_17)
        c = claims.add(self.pdir, "Продукт поддерживает 19 локалей", "fact", ["S001"], grade="B")
        claims.retract(self.pdir, c["id"], "ошибка в данных")
        self.assertFalse(any(M_TITLE in x or M_QUOTE in x for x in self._warns()), self._warns())

    def test_quote_vs_body_mismatch_warns(self):
        """Число из цитаты отсутствует в тексте sources/S###.md → warning с парой."""
        sources.add(self.pdir, text=BODY_17, title="Продукт")
        c = claims.add(self.pdir, "Покрытие продукта", "fact", ["S001"], grade="B",
                       quote="доступен на 19 локалях")
        pair = f"{c['id']}/S001"
        w = [x for x in self._warns() if pair in x and M_QUOTE in x]
        self.assertTrue(w, self._warns())
        self.assertIn("19", w[0])

    def test_quote_verbatim_is_quiet(self):
        """Дословная цитата: все её числа есть в тексте источника — тревоги нет."""
        sources.add(self.pdir, text=BODY_17, title="Продукт")
        claims.add(self.pdir, "Покрытие продукта", "fact", ["S001"], grade="B",
                   quote="доступен на 17 локалях")
        self.assertFalse(any(M_QUOTE in x for x in self._warns()), self._warns())

    def test_quote_checked_against_body_not_header(self):
        """Число из цитаты сверяется с телом источника, а не со служебной шапкой:
        в шапке стоит заголовок реестра — совпадение только с ним тревогу не снимает."""
        sources.add(self.pdir, text=BODY_17, title="Цена 99 евро")
        claims.add(self.pdir, "Покрытие продукта", "fact", ["S001"], grade="B", quote="цена 99 евро")
        self.assertTrue(any(M_QUOTE in x for x in self._warns()), self._warns())

    def test_clean_project_without_numbers_is_silent(self):
        """Критерий приёмки: чистый проект без чисел — кросс-чек молчит."""
        pdir = project.create("Чистый", "Почему падает удержание подписчиков?", slug=f"clean{id(self)}")
        self.assertEqual(check.numeric_warnings(pdir, {}, {}), [])
        sources.add(pdir, text="данные без чисел", title="Отчёт")
        claims.add(pdir, "Рынок растёт", "fact", ["S001"], grade="B")
        self.assertFalse(any(M_TITLE in x or M_QUOTE in x for x in check.run(pdir)["warnings"]))


if __name__ == "__main__":
    unittest.main()
