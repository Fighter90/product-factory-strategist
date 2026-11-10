"""Доп. тесты cost: парсер OpenCode session.json (PRO-40).

Формат OpenCode: единый JSON-объект {info, messages}; итог по info.tokens
(input/output/reasoning/cache.read), модель из info.model. Подписочные провайдеры
(zai-coding-plan) — токены с ценой $0 и пометкой «plan».

Запуск: python3 -m unittest discover -s tests -v
"""
import json
import os
import tempfile
import unittest
from pathlib import Path

TMP = tempfile.mkdtemp(prefix="pfs-test-ocost-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from tools.pfs import cost, export, project  # noqa: E402


def fresh(slug):
    return project.create(f"Тест {slug}", "Почему падает удержание подписчиков?", slug=slug)


def opencode_session(created_ms=1794167147966, updated_ms=1794171267158,
                     provider="zai-coding-plan", model_id="glm-5.3-flash"):
    return {
        "info": {
            "id": "ses_e434df26cffes9JKqfClzSQIad",
            "projectID": "e490e295e79c03feb6c5a2ed752e33cb7889e13a",
            "agent": "build",
            "model": {"id": model_id, "providerID": provider, "variant": "max"},
            "cost": 0,
            "tokens": {"input": 1000, "output": 500, "reasoning": 200,
                       "cache": {"read": 4000, "write": 0}},
            "outcome": "succeeded",
            "time": {"created": created_ms, "updated": updated_ms},
            "title": "Продолжение решения задачи",
        },
        "messages": [
            {"id": "msg_u", "time": {"created": created_ms}, "text": "продолжи решать", "type": "user"},
            {"id": "msg_a1", "type": "assistant", "agent": "build",
             "model": {"id": model_id, "providerID": provider}, "content": []},
            {"id": "msg_a2", "type": "assistant", "agent": "build",
             "model": {"id": model_id, "providerID": provider}, "content": []},
        ],
    }


class OpenCodeCostTests(unittest.TestCase):
    def setUp(self):
        self.pdir = fresh(f"oc{id(self)}")
        self.f = Path(TMP) / f"op{id(self)}_session.json"
        self.f.write_text(json.dumps(opencode_session()), encoding="utf-8")

    def test_parse_tokens_positive_and_plan(self):
        pm = cost.parse_transcript(self.f)
        t = pm["glm-5.3-flash"]
        self.assertEqual(t["input"], 1000)
        self.assertEqual(t["output"], 700)  # output + reasoning (тарифицируется как output)
        self.assertEqual(t["cache_read"], 4000)
        self.assertEqual(t["cache_write"], 0)
        self.assertEqual(t["messages"], 2)  # только assistant-сообщения
        self.assertEqual(t["plan"], 1)      # подписочный провайдер — пометка «plan»
        self.assertGreater(t["input"] + t["output"] + t["cache_read"], 0)  # критерий: токены > 0

    def test_record_session_plan_zero_usd_and_appendix_d(self):
        s = cost.record_session(self.pdir, "op1", self.f, since="2026-01-01T00:00:00Z")
        self.assertEqual(s["usd"], 0.0)  # план: токены бесплатны
        summ = cost.summary(self.pdir)
        self.assertEqual(summ["sessions"], 1)
        self.assertGreater(summ["tokens"], 0)
        self.assertEqual(summ["usd"], 0.0)
        text = export.build(self.pdir).read_text(encoding="utf-8")
        self.assertIn("# Приложение D. Прозрачность", text)
        self.assertIn("сессий 1", text)  # критерий: сессии ≥ 1
        self.assertIn("glm-5.3-flash (plan)", text)

    def test_record_session_idempotent(self):
        cost.record_session(self.pdir, "op1", self.f, since="2026-01-01T00:00:00Z")
        before = (self.pdir / "costs.json").read_text(encoding="utf-8")
        cost.record_session(self.pdir, "op1", self.f, since="2026-01-01T00:00:00Z")  # повтор не удваивает
        self.assertEqual((self.pdir / "costs.json").read_text(encoding="utf-8"), before)

    def test_window_excludes_out_of_window_session(self):
        self.assertEqual(cost.parse_transcript(self.f, since="2999-01-01T00:00:00Z"), {})
        self.assertEqual(cost.parse_transcript(self.f, until="2001-01-01T00:00:00Z"), {})
        self.assertNotEqual(cost.parse_transcript(self.f, since="2026-01-01T00:00:00Z"), {})

    def test_fallback_to_message_tokens_when_info_tokens_empty(self):
        # Частичный экспорт без итога info.tokens — считаем по tokens из assistant-сообщений
        sess = opencode_session()
        del sess["info"]["tokens"]
        for m in sess["messages"]:
            if m.get("type") == "assistant":
                m["tokens"] = {"input": 400, "output": 100, "reasoning": 50, "cache": {"read": 800, "write": 10}}
        f = Path(TMP) / f"fb{id(self)}_session.json"
        f.write_text(json.dumps(sess), encoding="utf-8")
        pm = cost.parse_transcript(f)
        t = pm["glm-5.3-flash"]
        self.assertEqual(t["input"], 800)       # 2 сообщения × 400
        self.assertEqual(t["output"], 300)      # (output 100 + reasoning 50) × 2
        self.assertEqual(t["cache_read"], 1600)
        self.assertEqual(t["cache_write"], 20)
        self.assertEqual(t["messages"], 2)      # сообщения с tokens
        self.assertEqual(t["plan"], 1)          # провайдер берётся из message.model
        self.assertGreater(t["input"] + t["output"] + t["cache_read"], 0)

    def test_info_tokens_preferred_over_message_sum(self):
        # Итог и по-сообщные tokens есть оба: берём итог сессии один раз, без двойного счёта
        sess = opencode_session()
        for m in sess["messages"]:
            if m.get("type") == "assistant":
                m["tokens"] = {"input": 10, "output": 10, "reasoning": 0, "cache": {"read": 10, "write": 0}}
        f = Path(TMP) / f"pr{id(self)}_session.json"
        f.write_text(json.dumps(sess), encoding="utf-8")
        t = cost.parse_transcript(f)["glm-5.3-flash"]
        self.assertEqual(t["input"], 1000)
        self.assertEqual(t["output"], 700)
        self.assertEqual(t["cache_read"], 4000)
        self.assertEqual(t["messages"], 2)

    def test_non_plan_provider_is_priced(self):
        f2 = Path(TMP) / f"np{id(self)}_session.json"
        f2.write_text(json.dumps(opencode_session(provider="anthropic", model_id="claude-sonnet-5-5")),
                      encoding="utf-8")
        pm = cost.parse_transcript(f2)
        self.assertNotIn("plan", pm["claude-sonnet-5-5"])
        s = cost.record_session(self.pdir, "np1", f2, since="2026-01-01T00:00:00Z")
        self.assertGreater(s["usd"], 0.0)

    def test_claude_jsonl_still_parsed(self):
        tr = Path(TMP) / f"cc{id(self)}.jsonl"
        rows = [{"message": {"id": "m1", "model": "claude-opus-5-5",
                             "usage": {"input_tokens": 100, "output_tokens": 50}}}]
        tr.write_text("\n".join(json.dumps(r) for r in rows) + "\n")
        pm = cost.parse_transcript(tr)
        self.assertEqual(pm["claude-opus-5-5"]["input"], 100)
        self.assertEqual(pm["claude-opus-5-5"]["output"], 50)


if __name__ == "__main__":
    unittest.main()
