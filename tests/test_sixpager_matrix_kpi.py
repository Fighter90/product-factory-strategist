"""PRO-48: six-pager FAQ-4 и FAQ-6 — матрица тактик группируется по инициативам
(на каждую 2–4 строки: фокус — короткое направление, не повтор решений;
потребности — барьер пользователя из JTBD, не прочерк; тактики — по одной
исполняемой в строке) и KPI в двух плоскостях из ЯВНОЙ таблицы 06_validation_plan.md
со столбцом «Плоскость» (плоскость задаётся явно, а не угадывается по словам
метрики; база и цель — раздельные ячейки: дата+источник и срок, порог, контр-метрика).
Проверки на синтетических каркасах и на реальных проектах демо и cvstart-EU.
Запуск: python3 -m unittest tests.test_sixpager_matrix_kpi -v
"""
import os
import re
import tempfile
import unittest
from pathlib import Path

TMP = tempfile.mkdtemp(prefix="pfs-test-mk-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from tools.pfs import export, project  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
DEMO = REPO / "projects" / "демо"
CVSTART = REPO / "projects" / "вывод-проекта-на-европейский-рынок-cvstart-org"

MATRIX_HEAD = ("| Стратегическая инициатива | Фокус | Потребности и ожидания "
               "пользователя | Решения (тактики) |")
KPI_HEAD = ("| Метрика | Формула | База (дата, источник) | Цель к сроку | "
            "Порог действия (остановить) | Контр-метрика |")


def table_rows(block: str) -> list[list[str]]:
    """Строки markdown-таблиц блока без шапок и разделителей |---|."""
    rows = []
    for ln in block.splitlines():
        if not ln.startswith("|"):
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if all(set(c) <= set("-: ") for c in cells):
            continue
        if "Формула" in cells or cells and cells[0] in ("Метрика", "Плоскость",
                                                        "Стратегическая инициатива"):
            continue  # шапки таблиц
        rows.append(cells)
    return rows


class MatrixUnitTests(unittest.TestCase):
    """Синтетический каркас: группировка по инициативам, кап 4 тактики,
    фокус — направление из заголовка без тайминга, потребности из JTBD 02."""

    @classmethod
    def setUpClass(cls):
        cls.pdir = project.create("Матрица PRO-48", "Как растить удержание?", slug="pro48-matrix")
        out = cls.pdir / "outputs"
        (out / "02_situation.md").write_text(
            "# Ситуация\n## Сегменты (discovery)\n"
            "JTBD: «Когда я готовлю резюме, хочу сделать его за один вечер — "
            "без ручной рутины и подписных ловушек»\n", encoding="utf-8")
        (out / "04_product_strategy.md").write_text(
            "# Стратегия\n## Выбранное направление\nOutcome-роадмап (результаты, не фичи):\n"
            "- **Инициатива 1 — онбординг за один вечер (мес 0–2):** шаблон на локальных "
            "конвенциях; импорт CV одним файлом. **Результат к дню 60:** активация ≥ 40%.\n"
            "- **Инициатива 2 — канал комьюнити (мес 2–4):** Show HN; answer-first Reddit; "
            "звёздный трекер в release notes; еженедельный дайджест; ежемесячный repack. "
            "**Результат к дню 120:** звёзды 300+.\n"
            "## Метрики\nактивация 40% [C001]\n", encoding="utf-8")
        cls.matrix = export._tactics_matrix(cls.pdir)

    def test_rows_grouped_2_to_4_per_initiative(self):
        groups: dict[str, int] = {}
        for r in table_rows(self.matrix):
            groups[r[0]] = groups.get(r[0], 0) + 1
        self.assertEqual(sorted(groups), ["Инициатива 1", "Инициатива 2"])
        for name, n in groups.items():
            self.assertTrue(2 <= n <= 4, f"у «{name}» {n} строк (эталон: 2–4)")

    def test_tactics_capped_at_4_overflow_merged(self):
        init2 = [r for r in table_rows(self.matrix) if r[0] == "Инициатива 2"]
        self.assertEqual(len(init2), 4)
        self.assertIn("repack", init2[-1][3], "излишек тактик теряется")
        self.assertIn("**Результат:** звёзды 300+", init2[-1][3], "гейт не у последней тактики")
        self.assertNotIn("**Результат:**", init2[0][3], "гейт не на первой тактике")

    def test_initiative_without_gate_has_no_dangling_result(self):
        # У инициативы без «Результат …:» гейта нет — « **Результат:** » с пустым
        # значением в последнюю строку не приписывается; у инициативы с гейтом —
        # приписывается, как раньше.
        pdir = project.create("Матрица без гейта у тира", "Что делать?", slug="pro48-dangling")
        out = pdir / "outputs"
        (out / "02_situation.md").write_text(
            "# Ситуация\n## Сегменты (discovery)\n"
            "JTBD: «Когда я готовлю резюме, хочу сделать его за один вечер — "
            "без ручной рутины»\n", encoding="utf-8")
        (out / "04_product_strategy.md").write_text(
            "# Стратегия\n## Выбранное направление\n"
            "- **Инициатива 1 — активация (мес 0–2):** шаблон; импорт файла. "
            "**Результат к дню 60:** активация 40%.\n"
            "- **Инициатива 2 — канал (мес 2–4):** Show HN; Reddit.\n", encoding="utf-8")
        rows = table_rows(export._tactics_matrix(pdir))
        g1 = [r for r in rows if r[0] == "Инициатива 1"]
        g2 = [r for r in rows if r[0] == "Инициатива 2"]
        self.assertIn("**Результат:** активация 40%", g1[-1][3], "гейт потерялся")
        for r in g2:
            self.assertNotIn("**Результат:**", r[3], f"висячий результат: {r}")

    def test_focus_short_direction_without_timing(self):
        for r in table_rows(self.matrix):
            self.assertNotEqual(r[1], r[0], "фокус повторяет имя инициативы")
            self.assertNotIn(r[1], r[3], "фокус повторяет тактику")
            self.assertNotIn("мес", r[1], "тайминг попал в фокус")
        r1 = [r for r in table_rows(self.matrix) if r[0] == "Инициатива 1"][0]
        self.assertEqual(r1[1], "онбординг за один вечер")

    def test_needs_user_words_from_jtbd_not_dash(self):
        needs = {r[2] for r in table_rows(self.matrix)}
        self.assertEqual(needs, {"без ручной рутины и подписных ловушек"})


class MatrixGuardsTests(unittest.TestCase):
    """Честные заглушки: нет задачи пользователя или меньше двух инициатив
    с 2+ тактиками — матрицы нет (пустых и повторных ячеек не будет)."""

    @staticmethod
    def _write(pdir: Path, roadmap: str, jtbd: bool) -> None:
        out = pdir / "outputs"
        seg = ("## Сегменты (discovery)\n"
               "JTBD: «Когда я готовлю резюме, хочу уложиться в вечер — без рутины»\n"
               ) if jtbd else "## Сегменты (discovery)\n- абоненты 55+\n"
        (out / "02_situation.md").write_text("# Ситуация\n" + seg, encoding="utf-8")
        (out / "04_product_strategy.md").write_text(
            "# Стратегия\n## Выбранное направление\n" + roadmap + "\n", encoding="utf-8")

    def test_no_jtbd_returns_none(self):
        pdir = project.create("Матрица без JTBD", "Что делать?", slug="pro48-nojtbd")
        self._write(pdir,
                    "- **Инициатива 1 — активация (мес 0–2):** шаблон; импорт файла.\n"
                    "- **Инициатива 2 — канал (мес 2–4):** Show HN; Reddit.\n", jtbd=False)
        self.assertIsNone(export._tactics_matrix(pdir))

    def test_single_initiative_returns_none(self):
        pdir = project.create("Матрица одной инициативы", "Что делать?", slug="pro48-one")
        self._write(pdir,
                    "- **Инициатива 1 — активация (мес 0–2):** шаблон; импорт файла.\n", jtbd=True)
        self.assertIsNone(export._tactics_matrix(pdir))

    def test_legacy_stage_labels_still_build_rows(self):
        # Старый формат «Этап N (мес …)» без «—»: строки строятся, фокус — из
        # гейта-результата и ни в одной строке не повторяет ни имя этапа,
        # ни решения (гейт уже показан в Фокусе — в Решения не дублируется).
        pdir = project.create("Матрица этапов", "Что делать?", slug="pro48-stages")
        self._write(pdir,
                    "- **Этап 1 (мес 0–3), волна DE:** семейный пакет; уведомления. "
                    "**Результат к дню 90:** удержание +5 п.п.\n"
                    "- **Этап 2 (мес 3–6):** гейт лояльности; пересмотр цен. "
                    "**Результат к дню 180:** ARPU +10%.\n", jtbd=True)
        rows = table_rows(export._tactics_matrix(pdir))
        self.assertTrue(rows)
        self.assertEqual(rows[0][0], "Этап 1 (мес 0–3), волна DE")
        for r in rows:
            self.assertTrue(r[1], f"пустой фокус: {r}")
            self.assertNotEqual(r[1], r[0], f"фокус повторяет имя этапа: {r}")
            self.assertNotIn(r[1], r[3], f"фокус повторяет решения: {r}")

    def test_legacy_stage_without_dash_or_gate_returns_none(self):
        # «Этап N» без «—» и без гейта: фокус взять неоткуда — fallback на первую
        # тактику давал бы Фокус, идентичный «Решения» (повтор ячеек). Честная
        # заглушка вместо кривой матрицы (ревью PRO-48).
        pdir = project.create("Матрица без гейта", "Что делать?", slug="pro48-nogate")
        self._write(pdir,
                    "- **Этап 1 (мес 0–3), волна DE:** семейный пакет; уведомления. "
                    "**Результат к дню 90:** удержание +5 п.п.\n"
                    "- **Этап 2 (мес 3–6):** гейт лояльности; пересмотр цен.\n", jtbd=True)
        self.assertIsNone(export._tactics_matrix(pdir))

    def test_initiative_with_single_tactic_not_silently_dropped(self):
        # Инициатива с одной тактикой не выбрасывается из матрицы молча:
        # «на каждую инициативу FAQ-3 от 2 до 4 строк» — либо у всех, либо
        # честная заглушка (ревью PRO-48).
        pdir = project.create("Матрица с дыркой", "Что делать?", slug="pro48-hole")
        self._write(pdir,
                    "- **Инициатива 1 — активация (мес 0–2):** шаблон; импорт файла.\n"
                    "- **Инициатива 2 — канал (мес 2–4):** Show HN; Reddit.\n"
                    "- **Инициатива 3 — прайсинг (мес 4–6):** годовой тариф.\n", jtbd=True)
        self.assertIsNone(export._tactics_matrix(pdir))


class KpiUnitTests(unittest.TestCase):
    """Явная таблица «KPI» со столбцом «Плоскость»: плоскость задаётся явно,
    а не словами метрики; битые строки и чужие плоскости пропускаются;
    гипотезы H1…H5 KPI не подменяют; нет таблицы — None."""

    @classmethod
    def setUpClass(cls):
        cls.pdir = project.create("KPI PRO-48", "Как растить выручку?", slug="pro48-kpi")
        out = cls.pdir / "outputs"
        (out / "06_validation_plan.md").write_text(
            "# План проверки\n## Ожидаемое изменение (сводно)\n\n"
            "| # | Гипотеза | Метрика | Ожидание к решению |\n|---|---|---|---|\n"
            "| H1 | пакет удерживает [C001] | удержание M1 | 38% → 45% |\n\n"
            "## KPI (две плоскости)\n\n"
            "| Плоскость | Метрика | Формула | База (дата, источник) | Цель к сроку | "
            "Порог действия (остановить) | Контр-метрика |\n"
            "|---|---|---|---|---|---|---|\n"
            "| Бизнес | Доля годовых подписок | годовые / все платящие | "
            "0% (2026-11-01, запуска нет [C001]) | ≥ 30% к дню 90 | < 10% → пересмотр тиров | churn |\n"
            "| Продукт | Ценность первой сессии | клики до первого экспорта | "
            "12 шагов (2026-11-01, ручной путь [S001]) | ≤ 7 шагов к дню 90 | "
            "> 10 шагов → упрощение воронки | конверсия |\n"
            "| Бизнес |  | формула | база (2026-11-01, [C001]) | цель к дню 90 | порог | контр |\n"
            "| Валюта | Мимо плоскости | формула | база (2026-11-01, [C001]) | цель к дню 90 | "
            "порог | контр |\n", encoding="utf-8")
        cls.kpi = export._kpi_table(cls.pdir)

    def test_planes_explicit_not_word_guessed(self):
        # «Доля годовых подписок» без слов-триггеров — в Бизнесе, потому что так
        # в 06; «Ценность…» со словом «цен» — в Продукте, а не в Бизнесе.
        biz = table_rows(self.kpi.split("**Продукт**")[0])
        prod = table_rows(self.kpi.split("**Продукт**")[1])
        self.assertEqual([r[0] for r in biz], ["Доля годовых подписок"])
        self.assertEqual([r[0] for r in prod], ["Ценность первой сессии"])

    def test_two_tables_with_split_base_and_target(self):
        self.assertIn("**Бизнес**", self.kpi)
        self.assertIn("**Продукт**", self.kpi)
        self.assertEqual(self.kpi.count(KPI_HEAD), 2)
        for r in table_rows(self.kpi):
            self.assertEqual(len(r), 6, f"строка KPI не 6-колоночная: {r}")
            self.assertNotIn("→", r[2], "база склеена с целью")
            self.assertNotIn("→", r[3], "цель склеена с базой")

    def test_malformed_and_unknown_plane_rows_skipped(self):
        self.assertEqual(len(table_rows(self.kpi)), 2)

    def test_hypothesis_table_alone_is_not_kpi(self):
        # Явной таблицы нет — гипотезы H1…H5 KPI не подменяют (честная заглушка).
        pdir2 = project.create("KPI без таблицы", "Как?", slug="pro48-kpi-none")
        (pdir2 / "outputs" / "06_validation_plan.md").write_text(
            "# План\n## Ожидаемое изменение (сводно)\n\n"
            "| # | Гипотеза | Метрика | Ожидание к решению |\n|---|---|---|---|\n"
            "| H1 | пакет удерживает | удержание M1 | 38% → 45% |\n", encoding="utf-8")
        self.assertIsNone(export._kpi_table(pdir2))

    def test_missing_06_returns_none(self):
        pdir2 = project.create("KPI без 06", "Как?", slug="pro48-kpi-missing")
        self.assertIsNone(export._kpi_table(pdir2))


class RealProjectMatrixTests(unittest.TestCase):
    """FAQ-4 на демо и cvstart-EU: группировка по инициативам FAQ-3 (2–4 строки),
    без пустых и повторяющихся ячеек, потребности — словами пользователя."""

    @classmethod
    def setUpClass(cls):
        cls.matrices = {slug: export._tactics_matrix(REPO / "projects" / slug)
                        for slug in ("демо",
                                     "вывод-проекта-на-европейский-рынок-cvstart-org")}

    def test_matrix_built_for_both_projects(self):
        for slug, m in self.matrices.items():
            self.assertIsNotNone(m, f"{slug}: матрица тактик не собралась")

    def test_rows_grouped_2_to_4_per_initiative(self):
        for slug, m in self.matrices.items():
            groups: dict[str, int] = {}
            for r in table_rows(m):
                groups[r[0]] = groups.get(r[0], 0) + 1
            self.assertGreaterEqual(len(groups), 2, f"{slug}: инициатив меньше двух")
            for name, n in groups.items():
                self.assertTrue(2 <= n <= 4, f"{slug}: у «{name}» {n} строк (эталон: 2–4)")

    def test_no_empty_or_placeholder_cells(self):
        for slug, m in self.matrices.items():
            for r in table_rows(m):
                for c in r:
                    self.assertTrue(c and c not in ("—", "…"), f"{slug}: пустая ячейка {r}")

    def test_focus_is_direction_not_duplicate(self):
        for slug, m in self.matrices.items():
            for r in table_rows(m):
                self.assertNotEqual(r[1], r[0], f"{slug}: фокус повторяет инициативу: {r}")
                self.assertNotIn(r[1], r[3], f"{slug}: фокус повторяет тактику: {r}")
                self.assertFalse(re.search(r"\bмес\b", r[1]), f"{slug}: тайминг в фокусе: {r}")

    def test_needs_user_words_not_dash(self):
        for slug, m in self.matrices.items():
            needs = {r[2] for r in table_rows(m)}
            self.assertEqual(len(needs), 1, f"{slug}: потребности разнятся по строкам")
            (need,) = needs
            self.assertNotEqual(need, "—", f"{slug}: потребности — прочерк")
            self.assertGreater(len(need), 30, f"{slug}: потребности подозрительно коротки")
            self.assertIn("без", need, f"{slug}: потребности не барьером словами пользователя")


class RealProjectKpiTests(unittest.TestCase):
    """FAQ-6 на демо и cvstart-EU: две таблицы (Бизнес/Продукт) из явной таблицы
    06, ≥4 метрик в каждой плоскости, у каждой — база с датой и источником,
    цель со сроком, порог действия, контр-метрика; метрики — не гипотезы H#."""

    @classmethod
    def setUpClass(cls):
        cls.kpis = {slug: export._kpi_table(REPO / "projects" / slug)
                    for slug in ("демо",
                                 "вывод-проекта-на-европейский-рынок-cvstart-org")}

    def test_two_plane_tables_with_enough_metrics(self):
        for slug, k in self.kpis.items():
            self.assertIsNotNone(k, f"{slug}: KPI-таблицы не собрались")
            self.assertIn("**Бизнес**", k, slug)
            self.assertIn("**Продукт**", k, slug)
            self.assertEqual(k.count(KPI_HEAD), 2, slug)
            biz = table_rows(k.split("**Продукт**")[0])
            prod = table_rows(k.split("**Продукт**")[1])
            self.assertGreaterEqual(len(biz), 4, f"{slug}: бизнес-метрик меньше 4")
            self.assertGreaterEqual(len(prod), 4, f"{slug}: продуктовых метрик меньше 4")

    def test_every_row_complete(self):
        for slug, k in self.kpis.items():
            for r in table_rows(k):
                self.assertEqual(len(r), 6, f"{slug}: строка KPI не 6-колоночная: {r}")
                for c in r:
                    self.assertTrue(c and c not in ("—", "…"), f"{slug}: пустая ячейка KPI {r}")

    def test_base_has_date_and_source(self):
        for slug, k in self.kpis.items():
            for r in table_rows(k):
                self.assertRegex(r[2], r"\d{4}-\d{2}-\d{2}", f"{slug}: нет даты базы: {r[0]}")
                self.assertIn("[", r[2], f"{slug}: нет источника базы: {r[0]}")
                self.assertNotIn("→", r[2], f"{slug}: база склеена с целью: {r[0]}")

    def test_target_has_deadline(self):
        for slug, k in self.kpis.items():
            for r in table_rows(k):
                self.assertRegex(r[3], r"(дн|ден|нед|мес)\S*\s*\d",
                                 f"{slug}: нет срока у цели: {r[0]}")

    def test_metrics_not_hypotheses(self):
        for slug, k in self.kpis.items():
            for r in table_rows(k):
                self.assertIsNone(re.match(r"H\d", r[0]), f"{slug}: KPI подменён гипотезой: {r[0]}")


class DemoSixPagerAssemblyTests(unittest.TestCase):
    """Сборка six-pager демо-проекта в копию: абзац-инструкция удалён, KPI-таблицы
    в FAQ-6 без дублей из целевой вставки 06 в FAQ-5, матрица тактик на месте."""

    @classmethod
    def setUpClass(cls):
        base = project.create("Демо-копия PRO-48", "Как вывести проект на рынок?",
                              slug="pro48-demo-copy")
        for name in ("project.json", "calcs.json", "sources.jsonl", "claims.jsonl"):
            src = DEMO / name
            if src.exists():
                (base / name).write_bytes(src.read_bytes())
        (base / "outputs").mkdir(parents=True, exist_ok=True)
        for name in ("02_situation.md", "03_options.md", "04_product_strategy.md",
                     "06_validation_plan.md"):
            src = DEMO / "outputs" / name
            if src.exists():
                (base / "outputs" / name).write_bytes(src.read_bytes())
        cls.text = export.build_six_pager(base, with_calcs=False).read_text(encoding="utf-8")

    def test_instruction_paragraph_removed(self):
        self.assertNotIn("KPI в двух направлениях", self.text)

    def test_kpi_tables_once_without_source_plane_column(self):
        self.assertEqual(self.text.count(KPI_HEAD), 2, "таблиц KPI должно быть две")
        self.assertNotIn("| Плоскость |", self.text, "столбец-источник 06 не вставляется")
        self.assertNotIn("#### KPI", self.text, "секция KPI дублируется целевой вставкой 06")

    def test_matrix_present_in_faq4(self):
        self.assertIn(MATRIX_HEAD, self.text)
        self.assertIn("Матрица тактик (из Outcome-роадмапа 04_product_strategy.md):", self.text)
        self.assertNotIn("Матрица тактик (заполните)", self.text)


if __name__ == "__main__":
    unittest.main()
