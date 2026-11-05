"""Тесты расширения data (funnel, stats) и повторных попыток fetch_url. Запуск: python3 -m unittest discover -s tests -v"""
import io
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock
from urllib.error import HTTPError

TMP = tempfile.mkdtemp(prefix="pfs-test-")
os.environ.setdefault("PFS_PROJECTS_DIR", TMP)

from tools.pfs import data, extract  # noqa: E402
from tools.pfs.core import PfsError  # noqa: E402


class FunnelTests(unittest.TestCase):
    def test_funnel_by_event_column(self):
        f = Path(TMP) / "funnel_events.csv"
        f.write_text("user_id,event\nu1,visit\nu2,visit\nu3,visit\nu1,signup\nu1,pay\nu1,visit\n", encoding="utf-8")
        res = data.funnel(f, ["visit", "signup", "pay"])
        self.assertEqual(res["steps"], ["visit", "signup", "pay"])
        self.assertEqual(res["counts"], [3, 1, 1])  # уникальные пользователи, дубль u1+visit не удваивает
        self.assertEqual(res["conv_pct"], [100.0, 33.3, 100.0])
        self.assertTrue(any("Дубликаты" in w for w in res["warnings"]))

    def test_funnel_by_flag_columns(self):
        f = Path(TMP) / "funnel_flags.csv"
        f.write_text("user_id,visit,signup,pay\nu1,1,1,0\nu2,1,0,0\nu3,1,1,1\n", encoding="utf-8")
        res = data.funnel(f, ["visit", "signup", "pay"])
        self.assertEqual(res["counts"], [3, 2, 1])
        self.assertEqual(res["conv_pct"], [100.0, 66.7, 50.0])
        self.assertFalse(res["warnings"])

    def test_funnel_warnings_and_text(self):
        f = Path(TMP) / "funnel_bad.csv"
        # signup пустой, pay больше visit: невозрастание
        f.write_text("user_id,event\nu1,visit\nu1,pay\nu2,pay\nu3,pay\n", encoding="utf-8")
        res = data.funnel(f, ["visit", "signup", "pay"])
        self.assertEqual(res["counts"], [1, 0, 3])
        self.assertIsNone(res["conv_pct"][2])  # деление на нулевой шаг
        self.assertTrue(any("нет данных" in w for w in res["warnings"]))
        self.assertTrue(any("не возрастает" in w for w in res["warnings"]))
        text = data.funnel_text(res)
        self.assertIn("visit", text)
        self.assertIn("—", text)  # None в таблице

    def test_funnel_unknown_steps_error(self):
        f = Path(TMP) / "funnel_flags.csv"
        # нет столбца event/stage и нет колонки unknown_step — ошибка
        with self.assertRaises(PfsError):
            data.funnel(f, ["visit", "unknown_step"])


class StatsTests(unittest.TestCase):
    def test_stats_basic(self):
        f = Path(TMP) / "stats.csv"
        f.write_text("id,val\n1,1\n2,2\n3,3\n4,4\n5,10\n", encoding="utf-8")
        res = data.stats(f, "val")
        self.assertEqual(res["n"], 5)
        self.assertAlmostEqual(res["mean"], 4.0, places=3)
        self.assertAlmostEqual(res["median"], 3.0, places=3)
        self.assertAlmostEqual(res["stdev"], 3.5355, places=3)
        self.assertAlmostEqual(res["p05"], 1.2, places=3)
        self.assertAlmostEqual(res["p50"], 3.0, places=3)
        self.assertAlmostEqual(res["p95"], 8.8, places=3)
        self.assertEqual(res["min"], 1)
        self.assertEqual(res["max"], 10)
        self.assertAlmostEqual(res["ci95"], 3.099, places=3)  # 1.96 * 3.5355 / sqrt(5)
        self.assertIn("среднее", data.stats_text(res))

    def test_stats_group(self):
        f = Path(TMP) / "stats_group.csv"
        f.write_text("seg,val\na,1\na,3\nb,5\nb,7\n", encoding="utf-8")
        res = data.stats(f, "val", group="seg")
        self.assertEqual(res["n"], 4)
        self.assertEqual(res["groups"]["a"]["n"], 2)
        self.assertAlmostEqual(res["groups"]["a"]["mean"], 2.0, places=3)
        self.assertAlmostEqual(res["groups"]["b"]["mean"], 6.0, places=3)
        self.assertIn("a", data.stats_text(res))

    def test_stats_missing_and_non_numeric(self):
        f = Path(TMP) / "stats_missing.csv"
        f.write_text("id,note,val\n1,x,2\n2,y,\n3,z,abc\n4,w,6\n", encoding="utf-8")
        res = data.stats(f, "val")
        self.assertEqual(res["n"], 2)  # пропуск и «abc» исключены
        self.assertEqual(len(res["warnings"]), 1)
        self.assertIn("2", res["warnings"][0])  # оба мусорных значения упомянуты
        with self.assertRaises(PfsError):  # столбец без числовых значений
            data.stats(f, "note")


class FetchRetryTests(unittest.TestCase):
    @staticmethod
    def _fake_opener(errors: list[Exception]):
        """Первые попытки бросают errors по порядку, затем успех. Возвращает (opener, calls)."""
        calls = []

        class Resp:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def read(self, n):
                return b"ok"

            headers = type("H", (), {"get_content_type": staticmethod(lambda: "text/html")})()

        class Opener:
            def open(self, req, timeout=None):
                calls.append(1)
                i = len(calls) - 1
                if i < len(errors):
                    raise errors[i]
                return Resp()

        return Opener(), calls

    def _fetch(self, op):
        with mock.patch.object(extract, "assert_public_url"), \
             mock.patch("urllib.request.build_opener", return_value=op), \
             mock.patch.object(extract.time, "sleep"):
            return extract.fetch_url("https://example.org/x")

    def test_retry_on_5xx_three_attempts(self):
        op, calls = self._fake_opener([HTTPError("https://example.org/x", 503, "err", {}, io.BytesIO(b"")),
                                       HTTPError("https://example.org/x", 503, "err", {}, io.BytesIO(b""))])
        body, ctype = self._fetch(op)
        self.assertEqual(body, b"ok")
        self.assertEqual(ctype, "text/html")
        self.assertEqual(len(calls), 3)  # основная + 2 повторные

    def test_retry_on_network_error(self):
        op, calls = self._fake_opener([OSError("connection reset")])
        body, _ = self._fetch(op)
        self.assertEqual(body, b"ok")
        self.assertEqual(len(calls), 2)

    def test_no_retry_on_403(self):
        op, calls = self._fake_opener([HTTPError("https://example.org/x", 403, "err", {}, io.BytesIO(b""))])
        with self.assertRaises(PfsError):
            self._fetch(op)
        self.assertEqual(len(calls), 1)  # 403 не повторяем


if __name__ == "__main__":
    unittest.main()
