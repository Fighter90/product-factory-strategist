"""PRO-50: `pfs check --strict` — «серьёзное расхождение» чисел утверждения с
источником и выдуманные цитаты («числа из цитаты отсутствуют в тексте источника»)
становятся ошибками (без --strict — предупреждения, как и раньше). Даты (25.09,
2026-11-08), ID с ведущим нулём (041), годы и номера версий (v1.267.1) — не числа
утверждения: они раньше давали ложные расхождения с заголовками источников.
Плюс `pfs claim fix-source` — перепривязка утверждения к верному источнику
с перепроверкой цитаты ДО записи.

Кейс из аудита: на проекте «98% Fortune 500 используют ATS» было привязано к
отчёту о рынке онлайн-рекрутинга — проверка видела расхождение, но пропускала,
а дата проверки 2026-11-08 считалась «числами утверждения».

Запуск: python3 -m unittest tests/test_check_strict.py -v
"""
import os
import tempfile
import unittest

TMP = tempfile.mkdtemp(prefix="pfs-test-strict-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from tools.pfs import check, claims, core, project, sources  # noqa: E402

M_SERIOUS = "серьёзное расхождение"
M_QUOTE = "числа из цитаты"


class CheckStrictTests(unittest.TestCase):
    def setUp(self):
        self.pdir = project.create(f"Strict {id(self)}", "Почему падает удержание подписчиков?",
                                   slug=f"strict{id(self)}")

    def _claim(self, text, quote=None, title="Отчёт о рынке: 37,97 млрд", body="Рынок растёт на 7,1% в год. " * 6):
        sources.add(self.pdir, text=body, title=title)
        return claims.add(self.pdir, text, "fact", ["S001"], grade="B", quote=quote)

    def test_strict_serious_mismatch_is_error(self):
        """Критерий приёмки: числа утверждения отсутствуют и в заголовке, и в тексте
        источника → без --strict предупреждение, с --strict ошибка (упоминание C###/S###)."""
        c = self._claim("ATS используют 98% компаний Fortune 500")
        res = check.run(self.pdir)
        self.assertEqual(res["errors"], [], res["errors"])
        self.assertTrue(any(M_SERIOUS in w and c["id"] in w for w in res["warnings"]), res["warnings"])
        sres = check.run(self.pdir, strict=True)
        self.assertTrue(any(M_SERIOUS in e and c["id"] in e for e in sres["errors"]), sres["errors"])
        self.assertFalse(any(M_SERIOUS in w for w in sres["warnings"]), sres["warnings"])

    def test_strict_fabricated_quote_is_error(self):
        """Критерий приёмки: числа цитаты отсутствуют в тексте источника — цитата могла
        быть выдумана → без --strict предупреждение, с --strict ошибка."""
        c = self._claim("Цены конкурентов", quote="Zety: $23,70/мес; resume.io: $29,95 каждые 4 недели")
        res = check.run(self.pdir)
        self.assertEqual(res["errors"], [], res["errors"])
        self.assertTrue(any(M_QUOTE in w and c["id"] in w for w in res["warnings"]), res["warnings"])
        sres = check.run(self.pdir, strict=True)
        self.assertTrue(any(M_QUOTE in e and c["id"] in e for e in sres["errors"]), sres["errors"])
        self.assertFalse(any(M_QUOTE in w for w in sres["warnings"]), sres["warnings"])

    def test_soft_title_mismatch_stays_warning_in_strict(self):
        """Число подтверждено телом источника, но не заголовком — разные показатели,
        не расхождение: предупреждение остаётся предупреждением и в --strict."""
        sources.add(self.pdir, text="Продукт доступен на 17 локалях. " * 6, title="Продукт: 20 локалей")
        claims.add(self.pdir, "Поддержка 17 локалей", "fact", ["S001"], grade="B")
        sres = check.run(self.pdir, strict=True)
        self.assertEqual([e for e in sres["errors"] if "S001" in e], [], sres["errors"])
        self.assertTrue(any("не совпадают" in w for w in sres["warnings"]), sres["warnings"])

    def test_dates_ids_versions_are_not_claim_numbers(self):
        """Критерий приёмки: даты (25.09, 2026-11-08), ID с ведущим нулём (041),
        годы и версии (v1.267.1) не считаются числами утверждения."""
        self.assertEqual(check._numbers("проверка 25.09"), {})
        self.assertEqual(check._numbers("проверка 2026-11-08"), {})
        self.assertEqual(check._numbers("выгрузка S041"), {})
        self.assertEqual(check._numbers("релиз v1.267.1"), {})
        self.assertEqual(check._numbers("релиз 1.271.2 готов"), {})
        self.assertEqual(check._numbers("Рынок $37,97 млрд (2025)"), {37.97: "37,97"})
        self.assertEqual(check._numbers("98,4% компаний"), {98.4: "98,4"})
        self.assertEqual(check._numbers("оценка 0.0–5.0"), {0.0: "0.0", 5.0: "5.0"})

    def test_date_in_title_does_not_mismatch(self):
        """Кейс C076/C077: дата в заголовке источника («Сводка за 25.09») не даёт
        ложного расхождения с числами утверждения."""
        sources.add(self.pdir, text="Выгрузка консоли за сентябрь без показателей. " * 6,
                    title="Сводка за 25.09")
        claims.add(self.pdir, "Проверка поисковой выдачей 2026-11-08, выгрузка S041",
                   "fact", ["S001"], grade="B")
        for strict in (False, True):
            res = check.run(self.pdir, strict=strict)
            self.assertFalse(any(M_SERIOUS in w or M_QUOTE in w or "не совпадают" in w
                                 for w in res["errors"] + res["warnings"]), res)

    def test_real_numbers_still_checked(self):
        """Исключения не глушат правило: настоящие числа утверждения, которых нет
        ни в заголовке, ни в тексте источника, по-прежнему серьёзное расхождение."""
        c = self._claim("Рынок 99,9 млрд и 40 млн пользователей")
        sres = check.run(self.pdir, strict=True)
        self.assertTrue(any(M_SERIOUS in e and c["id"] in e for e in sres["errors"]), sres["errors"])


class FixSourceTests(unittest.TestCase):
    def setUp(self):
        self.pdir = project.create(f"Fixsrc {id(self)}", "Почему падает удержание подписчиков?",
                                   slug=f"fixsrc{id(self)}")
        self.bad = sources.add(self.pdir, text="Отчёт о рынке онлайн-рекрутинга: 37,97 млрд. " * 4,
                               title="Рынок онлайн-рекрутинга 37,97 млрд")[0]
        self.jobscan = sources.add(self.pdir, text="In 2024, 98.4% of Fortune 500 companies "
                                                   "used a detectable ATS. " * 4,
                                   title="Jobscan: 98% Fortune 500 используют ATS")[0]

    def _claim(self, quote="2024: 98.4% of Fortune 500 companies used a detectable ATS"):
        return claims.add(self.pdir, "98% компаний Fortune 500 используют ATS (Jobscan)",
                          "fact", [self.bad["id"]], grade="B", quote=quote)

    def test_rebinds_and_verifies_quote(self):
        """Перепривязка на верный источник: список источников заменён, цитата
        перепроверена против тела нового источника, check --strict чист."""
        c = self._claim()
        rec = claims.fix_source(self.pdir, c["id"], [self.jobscan["id"]])
        self.assertEqual(rec["sources"], [self.jobscan["id"]])
        self.assertIn("fix_source", (rec.get("history") or [{}])[-1])
        sres = check.run(self.pdir, strict=True)
        self.assertFalse(any(c["id"] in e for e in sres["errors"]), sres["errors"])

    def test_verifies_new_quote_before_write(self):
        """--quote: новая дословная цитата проверяется против тела нового источника."""
        c = self._claim(quote=None)
        rec = claims.fix_source(self.pdir, c["id"], [self.jobscan["id"]],
                                quote="98.4% of Fortune 500 companies used a detectable ATS")
        self.assertEqual(rec["quote"], "98.4% of Fortune 500 companies used a detectable ATS")
        self.assertEqual(rec["sources"], [self.jobscan["id"]])

    def test_rejects_quote_numbers_missing_from_new_body(self):
        """Перепроверка ДО записи: числа цитаты, которых нет в новом источнике,
        отменяют правку — реестр не меняется."""
        c = self._claim()
        with self.assertRaises(core.PfsError) as cm:
            claims.fix_source(self.pdir, c["id"], [self.jobscan["id"]],
                              quote="2024: 99.2% of Fortune 500 companies")
        self.assertIn("Перепроверка цитаты", str(cm.exception))
        self.assertEqual(claims.get(self.pdir, c["id"])["sources"], [self.bad["id"]])
        self.assertEqual(claims.get(self.pdir, c["id"])["quote"],
                         "2024: 98.4% of Fortune 500 companies used a detectable ATS")

    def test_rejects_same_source_and_unknown_source(self):
        c = self._claim()
        with self.assertRaises(core.PfsError):
            claims.fix_source(self.pdir, c["id"], [self.bad["id"]])
        with self.assertRaises(core.PfsError):
            claims.fix_source(self.pdir, c["id"], ["S999"])

    def test_rejects_synthetic_source_for_fact(self):
        """Факт не может опираться на синтетику — как в claim add: понизьте до гипотезы."""
        syn = sources.add(self.pdir, text="Синтетическое интервью: 98 из 100. " * 4,
                          title="ИИ-респондент: Sarah, 32 (US)", origin="synthetic")[0]
        c = self._claim()
        with self.assertRaises(core.PfsError):
            claims.fix_source(self.pdir, c["id"], [syn["id"]])


if __name__ == "__main__":
    unittest.main()
