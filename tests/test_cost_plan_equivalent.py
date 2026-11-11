"""PRO-62: стоимость $0.00 при миллионах токенов — эквивалент по API-ценам для подписочных планов.

Проблема: pfs status проекта cvstart-EU показывает «Стоимость: $0.00 (~0 ₽数), токенов 19 735 031» —
сессия на glm-5.3-flash (zai-coding-plan) тарифицируется планом, pfs записывает $0 и выглядит
как ошибка учёта. Теперь:
- config/pricing.json содержит цены GLM (zai) и других моделей OpenCode с датой сверки;
- план-сессии получают «эквивалент по API-ценам» (фактическая оплата остаётся $0) и пометку
  «подписочный план»; при указанном тарифе — отдельно фактическая доля подписки;
- pfs cost и Приложение D six-pager: разбивка по шагам (intake…monitoring), по моделям
  с кэшем, время сессий и минуты человека, стоимость повторов.

Запуск: python3 -m unittest tests.test_cost_plan_equivalent -v
"""
from __future__ import annotations

import contextlib
import json
import os
import tempfile
import time
import unittest
from io import StringIO
from pathlib import Path

TMP = tempfile.mkdtemp(prefix="pfs-test-planeq-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from tools.pfs import cli, cost, export, project  # noqa: E402


def _run(argv):
    out, err = StringIO(), StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = cli.main(argv)
    return rc, out.getvalue(), err.getvalue()


# Токены сессии ×1000 от базовых, чтобы эквивалент не терялся при округлении до 4 знаков:
# input 1 000 000 × $0.15 = $0.15; output 700 000 × $0.50 = $0.35; cache_read 4 000 000 × $0.03 = $0.12.
TOK = 1000


def opencode_session(provider="zai-coding-plan", model_id="glm-5.3-flash",
                     created_ms=None, aggregate=True):
    created = created_ms if created_ms is not None else int(time.time() * 1000)
    sess = {
        "info": {"id": "ses_plan62", "model": {"id": model_id, "providerID": provider},
                 "time": {"created": created, "updated": created + 60_000}},
        "messages": [{"id": "msg_u", "type": "user", "text": "продолжи",
                      "time": {"created": created}},
                     {"id": "msg_a", "type": "assistant",
                      "model": {"id": model_id, "providerID": provider}, "content": [],
                      "time": {"created": created + 30_000}}],
    }
    if aggregate:
        sess["info"]["tokens"] = {"input": 1_000_000, "output": 500_000, "reasoning": 200_000,
                                  "cache": {"read": 4_000_000, "write": 0}}
    else:
        # частичный экспорт: токены известны только по assistant-сообщениям
        sess["messages"][1]["tokens"] = {"input": 1_000_000, "output": 500_000, "reasoning": 200_000,
                                         "cache": {"read": 4_000_000, "write": 0}}
    return sess


class PlanEquivalentTests(unittest.TestCase):
    def setUp(self):
        self.pdir = project.create(f"planeq-{id(self)}", "Почему падает удержание?")
        self.slug = self.pdir.name

    def _session_file(self, name, data):
        f = self.pdir / name
        f.write_text(json.dumps(data), encoding="utf-8")
        return f

    # --- 1. парсер OpenCode (PRO-40) с полем plan ---

    def test_parser_marks_plan_and_provider(self):
        f = self._session_file("ses_p1_session.json", opencode_session())
        pm = cost.parse_transcript(f)
        t = pm["glm-5.3-flash"]
        self.assertEqual(t["plan"], 1)                      # подписочный провайдер — план
        self.assertEqual(t.get("plan_provider"), "zai-coding-plan")
        self.assertEqual(t["input"], 1_000_000)             # токены посчитаны
        self.assertEqual(t["output"], 700_000)              # output + reasoning
        self.assertEqual(t["cache_read"], 4_000_000)        # кэш виден отдельно
        self.assertNotIn("plan", pm.get("nothing", {}))

    def test_parser_non_plan_has_no_plan_field(self):
        f = self._session_file("ses_p2_session.json",
                               opencode_session(provider="anthropic", model_id="claude-sonnet-5-5"))
        pm = cost.parse_transcript(f)
        self.assertNotIn("plan", pm["claude-sonnet-5-5"])

    # --- 2. эквивалент по API-ценам GLM из config/pricing.json ---

    def test_equivalent_uses_glm_api_price(self):
        f = self._session_file("ses_p3_session.json", opencode_session())
        s = cost.record_session(self.pdir, "p3", f)
        self.assertEqual(s["usd"], 0.0)                     # фактическая оплата — план
        expected = round((1_000_000 * 0.15 + 700_000 * 0.50 + 4_000_000 * 0.03) / 1e6, 4)
        self.assertEqual(s["usd_equivalent"], expected)     # $0.62 — не ноль
        self.assertGreater(s["usd_equivalent"], 0.0)

    def test_pricing_config_has_glm_and_plans_with_date(self):
        p = cost.pricing()
        self.assertEqual(p["models"]["glm-5.3-flash"]["input"], 0.15)
        self.assertEqual(p["models"]["glm-5.3-flash"]["output"], 0.50)
        self.assertEqual(p["models"]["glm-5.3-flash"]["cache_read"], 0.03)
        self.assertIn("glm-5.3", p["models"])               # старшие модели семейства
        self.assertIn("gpt-5", "".join(k for k in p["models"]))   # другие модели OpenCode
        self.assertIn("gemini", "".join(k for k in p["models"]))
        plans = p["plans"]["zai-coding-plan"]
        self.assertEqual(plans["equivalent"], "api_price")
        self.assertTrue(plans.get("prices_checked"))        # дата сверки цен зафиксирована

    # --- 3. сводка и текст `pfs cost`: ненулевой эквивалент + пометка «подписочный план» ---

    def test_summary_equivalent_and_plan_flag(self):
        f = self._session_file("ses_p4_session.json", opencode_session())
        cost.record_session(self.pdir, "p4", f)
        s = cost.summary(self.pdir)
        self.assertTrue(s["plan"])                          # пометка план-сессии
        self.assertEqual(s["usd"], 0.0)                     # фактически не платили
        self.assertGreater(s["usd_equivalent"], 0.0)        # эквивалент ненулевой
        self.assertGreater(s["rub_equivalent"], 0.0)

    def test_cost_output_marks_plan_and_equivalent(self):
        f = self._session_file("ses_p5_session.json", opencode_session())
        cost.record_session(self.pdir, "p5", f)
        rc, out, err = _run(["--project", self.slug, "cost"])
        self.assertEqual(rc, 0, err)
        self.assertIn("подписочный план", out)              # критерий: пометка «подписочный план»
        self.assertIn("эквивалент", out)
        self.assertNotIn("Итого: $0.00 (~0 ₽数)", out)      # ноль больше не единственная цифра
        self.assertIn("glm-5.3-flash (plan)", out)
        text = export.build(self.pdir).read_text(encoding="utf-8")   # Приложение D six-pager
        self.assertIn("подписочный план", text)
        self.assertIn("эквивалент", text)

    def test_status_shows_equivalent_not_bare_zero(self):
        f = self._session_file("ses_p6_session.json", opencode_session())
        cost.record_session(self.pdir, "p6", f)
        text = project.status_text(self.pdir)
        self.assertIn("подписочный план", text)             # $0.00 в pfs status больше не вводит в заблуждение
        self.assertIn("эквивалент", text)

    # --- 4. разбивка по шагам (intake…finish) ---

    def test_by_step_from_message_timestamps(self):
        t_before = int((time.time() - 10) * 1000)
        project.set_step(self.pdir, "intake", "in_progress")
        project.set_step(self.pdir, "intake", "done")
        project.set_step(self.pdir, "research", "in_progress")
        t_after = int((time.time() + 10) * 1000)
        sess = opencode_session(aggregate=False, created_ms=t_before)
        msgs = sess["messages"]
        msgs[0]["time"]["created"] = t_before
        msgs.append({"id": "msg_u2", "type": "user", "text": "ещё", "time": {"created": t_after}})
        msgs.append({"id": "msg_a2", "type": "assistant",
                     "model": {"id": "glm-5.3-flash", "providerID": "zai-coding-plan"},
                     "tokens": {"input": 500_000, "output": 100_000, "reasoning": 0,
                                "cache": {"read": 0, "write": 0}},
                     "time": {"created": t_after}})
        # токены первого assistant-сообщения — до первой отметки шага (intake)
        msgs[1]["tokens"] = {"input": 400_000, "output": 50_000, "reasoning": 0,
                             "cache": {"read": 0, "write": 0}}
        msgs[1]["time"] = {"created": t_before}
        f = self._session_file("ses_p7_session.json", sess)
        s = cost.record_session(self.pdir, "p7", f)
        self.assertIn("intake", s["by_step"])
        self.assertIn("research", s["by_step"])
        self.assertEqual(s["by_step"]["intake"]["glm-5.3-flash"]["input"], 400_000)
        self.assertEqual(s["by_step"]["research"]["glm-5.3-flash"]["input"], 500_000)
        summ = cost.summary(self.pdir)
        self.assertGreater(summ["by_step"]["intake"]["glm-5.3-flash"]["input"], 0)
        rc, out, err = _run(["--project", self.slug, "cost"])
        self.assertIn("По шагам", out)
        self.assertIn("intake", out)
        self.assertIn("research", out)

    def test_by_step_aggregate_attributed_to_step_at_session_end(self):
        created = int((time.time() - 10) * 1000)
        project.set_step(self.pdir, "intake", "in_progress")
        project.set_step(self.pdir, "intake", "done")
        project.set_step(self.pdir, "research", "in_progress")
        sess = opencode_session(created_ms=created)          # агрегат info.tokens — разбивки по сообщениям нет
        f = self._session_file("ses_p8_session.json", sess)
        s = cost.record_session(self.pdir, "p8", f)
        self.assertEqual(list(s["by_step"]), ["research"])   # сессия целиком — к шагу на конец сессии
        self.assertEqual(s["by_step"]["research"]["glm-5.3-flash"]["input"], 1_000_000)

    def test_legacy_record_without_by_step_falls_back_to_stage(self):
        # старые costs.json (до PRO-62) — сводка не падает, сессия относится к своему шагу
        (self.pdir / "costs.json").write_text(json.dumps({
            "sessions": {"old": {"models": {"glm-5.3-flash": {
                "input": 100, "output": 50, "cache_write": 0, "cache_read": 0,
                "messages": 1, "plan": 1}},
                "usd": 0.0, "updated": "2026-11-01T10:00:00+03:00", "stage": "situation",
                "since": None, "until": None}},
            "manual": []}), encoding="utf-8")
        s = cost.summary(self.pdir)
        self.assertEqual(s["tokens"], 150)                   # plan_provider в токены не попадает
        self.assertEqual(s["by_step"]["situation"]["glm-5.3-flash"]["input"], 100)

    # --- 5. повторы, время сессий, минуты человека ---

    def test_retries_counted_and_priced(self):
        created = int(time.time() * 1000)
        sess = opencode_session(aggregate=False, created_ms=created)
        msgs = sess["messages"]
        msgs.append({"id": "msg_a_r1", "type": "assistant",
                     "model": {"id": "glm-5.3-flash", "providerID": "zai-coding-plan"},
                     "tokens": {"input": 100_000, "output": 10_000, "reasoning": 0,
                                "cache": {"read": 0, "write": 0}},
                     "time": {"created": created + 1_000}})   # подряд без user-сообщения — повтор
        msgs.append({"id": "msg_a_r2", "type": "assistant",
                     "model": {"id": "glm-5.3-flash", "providerID": "zai-coding-plan"},
                     "tokens": {"input": 100_000, "output": 10_000, "reasoning": 0,
                                "cache": {"read": 0, "write": 0}},
                     "time": {"created": created + 2_000}})
        f = self._session_file("ses_p9_session.json", sess)
        s = cost.record_session(self.pdir, "p9", f)
        self.assertEqual(s["retries"]["messages"], 2)        # две лишние подряд assistant-ответа
        self.assertGreater(s["retries"]["usd_equivalent"], 0.0)
        rc, out, err = _run(["--project", self.slug, "cost"])
        self.assertIn("Повторы", out)

    def test_session_time_and_human_minutes(self):
        f = self._session_file("ses_p10_session.json", opencode_session())  # 60 секунд сессии
        cost.record_session(self.pdir, "p10", f)
        cost.add_manual(self.pdir, "правка отчёта", human_minutes=25)
        s = cost.summary(self.pdir)
        self.assertAlmostEqual(s["time_minutes"], 1.0, places=1)   # 60 c → 1 мин
        self.assertEqual(s["human_minutes"], 25)
        rc, out, err = _run(["--project", self.slug, "cost"])
        self.assertIn("время человека 25 мин", out)
        self.assertIn("время сессий", out)

    # --- 6. фактическая доля подписки при указанном тарифе ---

    def test_plan_share_when_tariff_specified(self):
        f = self._session_file("ses_p11_session.json", opencode_session())
        cost.record_session(self.pdir, "p11", f)
        s = cost.summary(self.pdir)
        self.assertEqual(s.get("plan_share"), {})            # тариф не указан — доля не считается
        cost.set_plan_tariff(self.pdir, 18.0)                # GLM Coding Plan Lite
        s = cost.summary(self.pdir)
        self.assertEqual(s["plan_share"]["month_usd"], 18.0)
        self.assertEqual(s["plan_share"]["tier"], "lite")
        self.assertGreater(s["plan_share"]["usd"], 0.0)      # минимум один день подписки
        rc, out, err = _run(["--project", self.slug, "cost"])
        self.assertIn("доля подписки", out)

    def test_plan_month_cli_flag(self):
        rc, out, err = _run(["--project", self.slug, "cost", "--plan-month", "80"])
        self.assertEqual(rc, 0, err)
        meta = json.loads((self.pdir / "project.json").read_text(encoding="utf-8"))
        self.assertEqual(meta.get("plan_month_usd"), 80.0)
        s = cost.summary(self.pdir)
        self.assertEqual(s["plan_share"]["tier"], "pro")     # 80 — тариф Pro по прайсу планов

    def test_plan_share_absent_without_tariff_or_sessions(self):
        self.assertEqual(cost.summary(self.pdir).get("plan_share"), {})


if __name__ == "__main__":
    unittest.main()
