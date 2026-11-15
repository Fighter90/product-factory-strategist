"""PRO-28: мониторинг-напоминания в `pfs next` — источники в основаниях принятых решений,
не проверявшиеся дольше stale_after_days, с готовой командой `pfs source refresh S###`,
просроченные обязательства и даты пересмотра в ближайшие 14 дней.

После refresh напоминание об источнике снимается (даже если текст страницы не изменился).

Запуск: python3 -m unittest tests.test_next_monitoring -v
"""
import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import date, timedelta
from unittest import mock

TMP = tempfile.mkdtemp(prefix="pfs-test-nxmon-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from tools.pfs import claims, core, decisions, project, sources  # noqa: E402


def page(text: str) -> bytes:
    return f"<html><head><title>Отчёт</title></head><body><p>{text}</p></body></html>".encode("utf-8")


PAGE = page("Регулятор обновил рекомендации по согласию пользователей. " * 12)
URL = "https://example.org/edpb-guidelines"


def run_cli(argv):
    buf = io.StringIO()
    args = cli_build_parser().parse_args(argv)
    with redirect_stdout(buf):
        args.f(args)
    return buf.getvalue()


def cli_build_parser():
    from tools.pfs import cli
    return cli.build_parser()


def fetch(page_bytes):
    return mock.patch("tools.pfs.extract.fetch_url", return_value=(page_bytes, "text/html"))


def backdate(pdir, sid: str, days: int) -> None:
    """Сдвинуть retrieved источника на days дней назад — имитация «источник не проверялся»."""
    rows = core.read_jsonl(pdir / "sources.jsonl")
    old = (date.today() - timedelta(days=days)).isoformat() + "T00:00:00+03:00"
    for r in rows:
        if r["id"] == sid:
            r["retrieved"] = old
    core.write_jsonl(pdir / "sources.jsonl", rows)


class NextMonitoringTests(unittest.TestCase):
    def setUp(self):
        self.pdir = project.create(f"Мониторинг {id(self)}", "Почему падает удержание?", slug=f"nxmon{id(self)}")

    def _decision_with_web_source(self) -> str:
        """Web-источник → активное утверждение → принятое решение с review через 10 дней."""
        with fetch(PAGE):
            rec, created = sources.add(self.pdir, URL)
        self.assertTrue(created)
        c = claims.add(self.pdir, "Регулятор требует баннер согласия", "fact", [rec["id"]], grade="B")
        decisions.add(self.pdir, "Консент-баннер", "Пилот на EU-трафике", "PM", [c["id"]],
                      review_date=(date.today() + timedelta(days=10)).isoformat())
        return rec["id"]

    # --- устаревшие источники в основаниях решений -----------------------------

    def test_stale_source_listed_with_refresh_command(self):
        sid = self._decision_with_web_source()
        backdate(self.pdir, sid, days=200)
        out = run_cli(["next"])
        self.assertIn(f"pfs source refresh {sid}", out)
        self.assertIn("200 дн.", out)
        self.assertNotIn("Долгов нет", out)

    def test_due_lists_stale_sources_with_commands(self):
        sid = self._decision_with_web_source()
        backdate(self.pdir, sid, days=200)
        res = decisions.due(self.pdir)
        self.assertEqual([s["sid"] for s in res["stale_sources"]], [sid])
        self.assertEqual(res["stale_sources"][0]["age"], 200)
        text = decisions.due_text(res)
        self.assertIn(f"pfs source refresh {sid}", text)
        # в stale_grounds остаются только проблемы статуса утверждений, без дублей по источникам
        self.assertFalse(any("возрастом" in s for s in res["stale_grounds"]))

    def test_fresh_source_not_listed(self):
        sid = self._decision_with_web_source()
        out = run_cli(["next"])
        self.assertNotIn(f"pfs source refresh {sid} —", out)
        self.assertNotIn("Устаревшие источники", out)

    def test_refresh_clears_reminder_even_without_changes(self):
        sid = self._decision_with_web_source()
        backdate(self.pdir, sid, days=200)
        with fetch(PAGE):  # страница не изменилась
            res = sources.refresh(self.pdir, sid)
        self.assertFalse(res["changed"])
        self.assertNotIn(f"pfs source refresh {sid}", run_cli(["next"]))
        self.assertEqual(decisions.due(self.pdir)["stale_sources"], [])

    def test_non_web_source_gets_manual_hint(self):
        rec, _ = sources.add(self.pdir, text="локальная выписка из отчёта", title="выписка")
        c = claims.add(self.pdir, "Выписка подтверждает сегмент", "fact", [rec["id"]], grade="C")
        decisions.add(self.pdir, "Фокус", "Пилот", "PM", [c["id"]])
        backdate(self.pdir, rec["id"], days=200)
        out = run_cli(["next"])
        self.assertNotIn(f"pfs source refresh {rec['id']}", out)
        self.assertIn(rec["id"], out)
        self.assertIn("обновите вручную", out)

    # --- ближайшие даты пересмотра ---------------------------------------------

    def test_review_within_14_days_shown(self):
        self._decision_with_web_source()  # review через 10 дней
        out = run_cli(["next"])
        self.assertIn("Пересмотр в ближайшие 14 дней", out)

    def test_review_far_or_past_not_in_soon_block(self):
        c = claims.add(self.pdir, "Сегмент растёт", "hypothesis", [], grade="D")
        decisions.add(self.pdir, "Фокус", "Пилот", "PM", [c["id"]],
                      review_date=(date.today() + timedelta(days=40)).isoformat())
        out = run_cli(["next"])
        self.assertNotIn("Пересмотр в ближайшие 14 дней", out)
        self.assertNotIn("К пересмотру решений", out)
        res = decisions.due(self.pdir)
        self.assertEqual(res["review_soon"], [])
        self.assertEqual(res["review_now"], [])


if __name__ == "__main__":
    unittest.main()
