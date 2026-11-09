"""PRO-39: гэп-трекинг — `pfs gap close` синхронно правит 01 и 02; `pfs check` ловит рассинхрон."""
import os
import tempfile
import unittest
from pathlib import Path

TMP = tempfile.mkdtemp(prefix="pfs-test-gaps-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from tools.pfs import check, claims, core, gaps, project, sources  # noqa: E402
from tools.pfs.core import PfsError  # noqa: E402

# 01: таблица вопросов со столбцом «Статус» + нумерованный список пробелов
PLAN = """# 01 · План исследования — Тест

| # | Вопрос | Гипотеза | Метод | Источник | Что считается ответом | Цена/время | Статус |
|---|---|---|---|---|---|---|---|
| Q1 | Сколько активных соискателей по странам? | DE и PL крупнейшие | desk | Eurostat | Ранжирование с числом и годом | 2 ч | открыт |
| Q2 | Готовы ли платить PL/ES? | PL чувствительны к цене | desk | отчёты | Оценка WTP | 2 ч | пробел |

## Пробелы (записаны как открытые вопросы)

1. Активные соискатели по странам — Eurostat LFS не даёт по ИТ-профессии.
2. WTP PL/ES — закрытые данные платёжных платформ.

## База для утверждений

- S001 — открытые данные.
"""

# 02: таблица «Чего мы не знаем» в том же порядке, что список пробелов в 01
SITUATION = """# Картина ситуации: Тест

## Что известно

### Сколько активных соискателей по странам?
- Рынок растёт [C001] (сила B)

## Чего мы не знаем

| Пробел | Почему не знаем | Как узнать | Стоимость/срок | Влияет на решение? |
|---|---|---|---|---|
| Активные соискатели по странам | Eurostat LFS не даёт по ИТ-профессии | прокси по вакансиям | 2 ч | да |
| WTP PL/ES | закрытые данные платёжных платформ | A/B на валидации | 0 € | да |

## Вопросы, которые могут изменить решение

1. Ранжирование стран.
"""


def fresh(slug):
    return project.create(f"Тест {slug}", "Почему падает удержание подписчиков?", slug=slug)


class GapTests(unittest.TestCase):
    def setUp(self):
        self.pdir = fresh(f"gap{id(self)}")
        sources.add(self.pdir, text="публичные данные рынка", title="d")
        self.c = claims.add(self.pdir, "Рынок вакансий вырос", "fact", ["S001"], grade="B")
        (self.pdir / "outputs" / "01_research_plan.md").write_text(PLAN, encoding="utf-8")
        (self.pdir / "outputs" / "02_situation.md").write_text(SITUATION, encoding="utf-8")

    def _sit_row(self):
        sit = (self.pdir / "outputs" / "02_situation.md").read_text(encoding="utf-8")
        return [l for l in sit.splitlines() if l.startswith("| Активные соискатели")][0]

    def test_close_syncs_both_files(self):
        res = gaps.close(self.pdir, 1, self.c["id"], note="прокси по стокам вакансий")
        self.assertIn(self.c["id"], res["message"])
        # 02: строка пробела помечена закрытой, старая причина сохранена
        row = self._sit_row()
        self.assertIn("закрыто", row)
        self.assertIn(self.c["id"], row)
        self.assertIn("Eurostat LFS не даёт по ИТ-профессии", row)
        # 01: пункт списка пробелов помечен закрытым
        plan = (self.pdir / "outputs" / "01_research_plan.md").read_text(encoding="utf-8")
        item = [l for l in plan.splitlines() if l.startswith("1. Активные соискатели")][0]
        self.assertIn("закрыто", item)
        self.assertIn(self.c["id"], item)
        # 01: статус вопроса в таблице «открыт» → «отвечен [C###]»
        qrow = [l for l in plan.splitlines() if l.startswith("| Q1 |")][0]
        self.assertIn(f"отвечен [{self.c['id']}]", qrow)
        self.assertNotIn("| открыт |", qrow)
        # второй пробел не тронут
        qrow2 = [l for l in plan.splitlines() if l.startswith("| Q2 |")][0]
        self.assertIn("| пробел |", qrow2)

    def test_close_then_check_is_quiet(self):
        gaps.close(self.pdir, 1, self.c["id"])
        warns = [w for w in check.run(self.pdir)["warnings"]
                 if "01_research_plan" in w and "открыт" in w]
        self.assertEqual(warns, [])

    def test_check_catches_desync(self):
        sit = (self.pdir / "outputs" / "02_situation.md").read_text(encoding="utf-8")
        sit = sit.replace(
            "| Активные соискатели по странам | Eurostat LFS не даёт по ИТ-профессии | прокси по вакансиям | 2 ч | да |",
            f"| Активные соискатели по странам | закрыто вчера [{self.c['id']}] | не требуется | 0 | нет |")
        (self.pdir / "outputs" / "02_situation.md").write_text(sit, encoding="utf-8")
        warns = check.run(self.pdir)["warnings"]
        self.assertTrue(any("01_research_plan" in w and "открыт" in w and "02_situation.md" in w
                            for w in warns), warns)
        # «частично закрыто» — не полное закрытие, ложной тревоги быть не должно
        sit2 = sit.replace(f"закрыто вчера [{self.c['id']}]", "частично закрыто вчера")
        (self.pdir / "outputs" / "02_situation.md").write_text(sit2, encoding="utf-8")
        self.assertFalse(any("Активные соискатели" in w for w in check.run(self.pdir)["warnings"]))

    def test_close_validation(self):
        with self.assertRaises(PfsError):  # неизвестное утверждение
            gaps.close(self.pdir, 1, "C999")
        with self.assertRaises(PfsError):  # нет такого номера
            gaps.close(self.pdir, 7, self.c["id"])
        gaps.close(self.pdir, 1, self.c["id"])
        with self.assertRaises(PfsError):  # уже закрыт — повтор не дублирует пометку
            gaps.close(self.pdir, 1, self.c["id"])
        self.assertEqual(self._sit_row().count("закрыто"), 1)

    def test_list(self):
        text = gaps.list_text(self.pdir)
        self.assertIn("Активные соискатели по странам", text)
        self.assertIn("WTP PL/ES", text)
        self.assertIn("открыт", text)

    def test_without_docs_is_safe(self):
        pdir = fresh(f"gapempty{id(self)}")
        sources.add(pdir, text="данные", title="d")
        c = claims.add(pdir, "Факт для проверки", "fact", ["S001"])
        self.assertEqual(gaps.sync_warnings(pdir), [])
        with self.assertRaises(PfsError):
            gaps.close(pdir, 1, c["id"])
        self.assertIn("ещё не создан", gaps.list_text(pdir))
        # 02 есть, но таблицы пробелов ещё нет
        (pdir / "outputs" / "02_situation.md").write_text("# Картина ситуации\n\n## Что известно\n", encoding="utf-8")
        self.assertIn("нет таблицы пробелов", gaps.list_text(pdir))
        self.assertEqual(gaps.sync_warnings(pdir), [])


if __name__ == "__main__":
    unittest.main()
