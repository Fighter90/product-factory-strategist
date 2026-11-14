"""PRO-50: `pfs check --strict` — «серьёзное расхождение» числа с источником и числа
цитаты, которых нет в тексте источника (цитата могла быть выдумана моделью), — ошибки;
без --strict — предупреждения, как раньше. Нейтральное «заголовок может нести другую
метрику» остаётся предупреждением и под --strict.

Ложные срабатывания исключены: даты (DD.MM и YYYY-MM-DD), годы, номера версий (v1.2.3)
и ID с ведущим нулём («041», ссылка «S041») — не числа утверждения.

Запуск: python3 -m unittest tests.test_strict_numeric -v
"""
import os
import tempfile
import unittest

TMP = tempfile.mkdtemp(prefix="pfs-test-strictnum-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from tools.pfs import check, claims, project, sources  # noqa: E402

BODY_17 = "Продукт доступен на 17 локалях. " * 6
M_SERIOUS = "серьёзное расхождение"
M_QUOTE = "числа из цитаты"
M_SOFT = "возможно, разные показатели"


class StrictPromotionTests(unittest.TestCase):
    def setUp(self):
        self.pdir = project.create(f"Strict {id(self)}", "Почему падает удержание подписчиков?",
                                   slug=f"strict{id(self)}")

    def test_quote_numbers_promoted_to_error_under_strict(self):
        """Критерий приёмки: числа цитаты нет в тексте источника → без --strict warning,
        с --strict ошибка (и её нет среди предупреждений)."""
        sources.add(self.pdir, text=BODY_17, title="Продукт")
        c = claims.add(self.pdir, "Покрытие продукта", "fact", ["S001"], grade="B",
                       quote="доступен на 19 локалях")
        pair = f"{c['id']}/S001"
        plain = check.run(self.pdir)
        self.assertTrue(any(pair in w and M_QUOTE in w for w in plain["warnings"]), plain)
        self.assertFalse(plain["errors"], plain)
        strict = check.run(self.pdir, strict=True)
        self.assertTrue(any(pair in e and M_QUOTE in e for e in strict["errors"]), strict)
        self.assertFalse(any(M_QUOTE in w for w in strict["warnings"]), strict)

    def test_serious_mismatch_promoted_to_error_under_strict(self):
        """«Серьёзное расхождение» (чисел утверждения нет ни в заголовке, ни в тексте
        источника) → без --strict warning, с --strict ошибка."""
        sources.add(self.pdir, text="Отчёт без чисел о рынке. " * 6, title="Сводка 3 сегментов")
        c = claims.add(self.pdir, "Рынок 40 млрд и рост 12%", "fact", ["S001"], grade="B")
        pair = f"{c['id']}/S001"
        plain = check.run(self.pdir)
        self.assertTrue(any(pair in w and M_SERIOUS in w for w in plain["warnings"]), plain)
        strict = check.run(self.pdir, strict=True)
        self.assertTrue(any(pair in e and M_SERIOUS in e for e in strict["errors"]), strict)

    def test_title_mismatch_stays_warning_under_strict(self):
        """Нейтральное расхождение «заголовок может нести другую метрику» (число
        подтверждено телом источника) — предупреждение и под --strict, не ошибка."""
        sources.add(self.pdir, text=BODY_17, title="Продукт: 20 локалей")
        c = claims.add(self.pdir, "Поддержка 17 локалей и 3 языка справки", "fact", ["S001"], grade="B")
        pair = f"{c['id']}/S001"
        strict = check.run(self.pdir, strict=True)
        self.assertTrue(any(pair in w and M_SOFT in w for w in strict["warnings"]), strict)
        self.assertFalse(strict["errors"], strict)


class FalsePositiveTests(unittest.TestCase):
    """Даты, годы, версии и ID — не числа утверждения (кейсы C065, C076, C077, C066)."""

    def setUp(self):
        self.pdir = project.create(f"FP {id(self)}", "Почему падает удержание подписчиков?",
                                   slug=f"fp{id(self)}")

    def _w(self):
        return check.run(self.pdir)["errors"] + check.run(self.pdir)["warnings"]

    def test_iso_date_in_claim_not_numbers(self):
        """C065: «…выдачей 2026-11-08…» — ISO-дата целиком не число: «11», «08» не
        порождают «серьёзное расхождение» с заголовком источника."""
        sources.add(self.pdir, text=BODY_17, title="Сайт: 19 локалей")
        claims.add(self.pdir, "Сайт индексируется (проверка поисковой выдачей 2026-11-08, proxy)",
                   "fact", ["S001"], grade="B")
        self.assertFalse(any(M_SERIOUS in x for x in self._w()), self._w())

    def test_dd_mm_date_in_title_not_numbers(self):
        """C076/C077: заголовок «обновлено 25.09.2026» — дата, а не показатель: ложного
        «числа заголовка (25,09)» нет."""
        sources.add(self.pdir, text=BODY_17, title="Keyword DB (обновлено 25.09.2026)")
        claims.add(self.pdir, "17 локалей в выдаче", "fact", ["S001"], grade="B")
        self.assertFalse(any("25,09" in x or M_SOFT in x or M_SERIOUS in x for x in self._w()), self._w())

    def test_leading_zero_id_and_tag_ref_not_numbers(self):
        """C077: «S041» и standalone «041» — идентификаторы с ведущим нулём, не числа."""
        sources.add(self.pdir, text=BODY_17, title="Free-выдача keyword-базы")
        claims.add(self.pdir, "Строки кластера отсутствуют в free-выдаче S041 (страница 041 отчёта)",
                   "fact", ["S001"], grade="B")
        self.assertFalse(any(M_SERIOUS in x or M_SOFT in x for x in self._w()), self._w())

    def test_version_in_claim_and_quote_not_numbers(self):
        """C066: «v1.267.1» — версия релиза, не число: ни в утверждении, ни в цитате."""
        sources.add(self.pdir, text="Release notes сайта. " * 6 + "Бейдж v1.271.2 на главной.",
                    title="Сайт: бейдж релиза")
        claims.add(self.pdir, "Текущий релиз v1.267.1 показан бейджем на сайте", "fact", ["S001"],
                   grade="B", quote="Check it out on Product Hunt … v1.267.1")
        self.assertFalse(any(M_SERIOUS in x or M_QUOTE in x or M_SOFT in x for x in self._w()), self._w())

    def test_decimal_comma_and_plain_numbers_survive(self):
        """Чердак от перестраховки: «0,5» и «17» — по-прежнему числа, кросс-чек работает."""
        sources.add(self.pdir, text="Рынок вырос на 0,5 п.п. до 17 млн. " * 6, title="Рынок: 17 млн")
        claims.add(self.pdir, "Рынок 0,5 п.п. и 17 млн", "fact", ["S001"], grade="B",
                   quote="вырос на 0,5 п.п.")
        self.assertFalse(any(M_SERIOUS in x or M_QUOTE in x for x in self._w()), self._w())


if __name__ == "__main__":
    unittest.main()
