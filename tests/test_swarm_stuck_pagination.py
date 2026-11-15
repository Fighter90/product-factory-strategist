"""PRO-72 (факт из лога .task-board/log/cycle-*.log, 2026-11-14 13:50–13:57): очередь
роя расклинилась — 13 задач висели In Progress с меткой swarm после смерти воркеров,
а stuckIssues() в scripts/swarm/orchestrator.mjs запрашивал first: 10 без пагинации.
Хвост из 3 задач (PRO-48/47/46, клеймы 110+ мин) не попадал в выборку → requeue по
порогу STUCK_MIN для них не срабатывал никогда; очередь пустела («queue empty»),
задачи зависали навсегда. Порядок возврата Linear не гарантирован — сортировка не спасает.

Тесты сверяют scripts/swarm/orchestrator.mjs по исходнику (приём как в
test_swarm_attempts.py для не-Python-кода), а production-код дополнительно исполняют
под node с заглушенным gql (Linear API):

1. источник: запрос stuckIssues пагинируется (pageInfo { hasNextPage endCursor },
   page size ≥ 50), никаких bare first: 10;
2. поведение: production stuckIssues() вытаскивает ВСЕ страницы через after-курсор
   (63 задачи → ≥2 запроса → 63 узла, без потерь и дублей);
3. поведение (инцидент PRO-72): при 13 зависших In Progress production-цикл requeue
   в секции pick за ОДИН проход возвращает все 13 в Todo с ♻️-комментарием и стирает
   их клеймы; свежий клейм не трогается (защита от перехвата чужой работы, PRO-68).

node нужен оркестратору и swarm-машине; если node недоступен, поведенческие тесты
пропускаются, а проверки по исходнику остаются обязательными.
"""
import json
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORCH_PATH = ROOT / "scripts" / "swarm" / "orchestrator.mjs"
ORCH = ORCH_PATH.read_text(encoding="utf-8")

NODE = shutil.which("node")


def seg_between(start: str, stop: str, src: str = ORCH) -> str:
    """Текст от первого вхождения start до ближайшего stop после него."""
    i = src.find(start)
    if i < 0:
        raise AssertionError(f"orchestrator.mjs: маркер не найден: {start!r}")
    j = src.find(stop, i + len(start))
    if j < 0:
        raise AssertionError(f"orchestrator.mjs: маркер не найден: {stop!r}")
    return src[i:j]


STUCK_START = "const stuckIssues = async () => {"
STUCK_STOP = "\n};"


def stuck_src() -> str:
    return seg_between(STUCK_START, STUCK_STOP)


# --- источник --------------------------------------------------------------

class StuckQueryPaginates(unittest.TestCase):
    """Выборка зависших не ограничена первой страницей (PRO-72)."""

    def test_no_bare_first_10_in_stuck_query(self):
        seg = stuck_src()
        self.assertNotIn("first: 10", seg,
                         "stuckIssues по-прежнему ограничен first: 10 — хвост зависших "
                         "In Progress невидим для requeue (PRO-72)")

    def test_page_size_at_least_50(self):
        m = re.search(r"first:\s*(\d+)", stuck_src())
        self.assertIsNotNone(m, "в запросе stuckIssues нет аргумента first")
        self.assertGreaterEqual(int(m.group(1)), 50,
                                "page size запроса stuckIssues меньше 50 — при 13+ "
                                "зависших хвост снова может не влезть (PRO-72)")

    def test_query_walks_pages_via_cursor(self):
        seg = stuck_src()
        self.assertIn("pageInfo { hasNextPage endCursor }", seg,
                      "запрос не берёт pageInfo — пройти страницы невозможно")
        self.assertIn("after: $after", seg, "запрос не принимает after-курсор")
        self.assertIn("hasNextPage", seg, "нет остановки по hasNextPage")
        self.assertIn("endCursor", seg, "курсор следующей страницы не берётся из endCursor")


class StuckLoopConsumesEverything(unittest.TestCase):
    """Цикл requeue обрабатывает весь список, а не срез."""

    def test_requeue_loop_iterates_full_list(self):
        self.assertIn("for (const n of await stuckIssues())", ORCH,
                      "цикл requeue не обходит результат stuckIssues целиком")

    def test_no_slice_limit_in_stuck_path(self):
        seg = stuck_src() + seg_between(
            "for (const n of await stuckIssues())", "// задачи с 2 проваленными попытками")
        self.assertNotIn(".slice(", seg, "выборка или цикл requeue обрезают список зависших")


# --- поведение (node, production-код исполняется как есть) -----------------

HARNESS = r"""
// Исполнитель production-кода orchestrator.mjs с заглушенным gql (Linear API).
// Сценарий в argv[3]: 'stuck' — пагинация stuckIssues (63 задачи → 2 страницы);
// 'requeue' — инцидент PRO-72: 13 зависших + 1 свежий клейм, один проход цикла pick.
const fs = require('fs');
const src = fs.readFileSync(process.argv[2], 'utf8');
const mode = process.argv[3];

function seg(start, stop) {
  const i = src.indexOf(start);
  if (i < 0) throw new Error('маркер не найден: ' + start);
  const j = src.indexOf(stop, i + start.length);
  if (j < 0) throw new Error('маркер не найден: ' + stop);
  return src.slice(i, j);
}

// production-константы фильтра (заглушка сверяет, что именно они ушли в Linear)
const TEAM_KEY = 'PRO';
const LABEL = 'swarm';

const issues = []; // доска зависших; заполняется сценарием
const requests = [];
const gql = async (query, variables) => { // видна production-функции из eval
  requests.push({ query, variables });
  const first = Number((query.match(/first:\s*(\d+)/) || [])[1] || variables.first || 10);
  const offset = variables.after ? Number(variables.after) : 0;
  const nodes = issues.slice(offset, offset + first).map((s) => ({
    id: s, identifier: s, title: 'fake ' + s,
    state: { name: 'In Progress' }, labels: { nodes: [{ name: 'swarm' }] },
  }));
  return { issues: { nodes, pageInfo: {
    hasNextPage: offset + nodes.length < issues.length,
    endCursor: String(offset + nodes.length),
  } } };
};

// production-функция stuckIssues — исполняется как есть, без правок
// (seg-inclusive: stop-маркер '\n};' входит в вырезку, иначе тело без закрывающей скобки)
const fnText = (() => {
  const i = src.indexOf('const stuckIssues = async () => {');
  const j = src.indexOf('\n};', i);
  if (i < 0 || j < 0) throw new Error('маркер stuckIssues не найден');
  return src.slice(i, j + '\n};'.length);
})();
const stuckIssues = eval('(' + fnText.slice(0, fnText.lastIndexOf(';')).slice('const stuckIssues = '.length) + ')');

(async () => {
  if (mode === 'stuck') {
    for (let k = 0; k < 63; k++) issues.push('PRO-' + (100 + k));
    const nodes = await stuckIssues();
    console.log(JSON.stringify({ ids: nodes.map((n) => n.identifier), requests }));
    return;
  }
  // 'requeue': инцидент PRO-72 — 13 зависших (клеймы 110 мин назад, порог
  // STUCK_MIN=90) + 1 свежий клейм (5 мин назад)
  for (let k = 0; k < 13; k++) issues.push('PRO-' + (100 + k));
  issues.push('PRO-FRESH');
  const now = Date.now();
  const claims = {};
  for (const s of issues) if (s !== 'PRO-FRESH') claims[s] = now - 110 * 60_000;
  claims['PRO-FRESH'] = now - 5 * 60_000;
  const STUCK_MIN = 90;
  const log = () => {};
  const setStates = []; const comments = [];
  const setState = async (id, name) => { setStates.push({ id, name }); };
  const comment = async (id, body) => { comments.push({ id, body }); };
  const forgetClaim = (id) => { delete claims[id]; };
  // production-цикл requeue из секции pick — исполняется как есть
  const loop = seg('for (const n of await stuckIssues()) {',
                   '\n\n      // задачи с 2 проваленными попытками');
  await eval('(async () => {\n' + loop + '\n})()');
  console.log(JSON.stringify({ setStates, comments, claimsLeft: Object.keys(claims) }));
})().catch((e) => { console.error(String(e)); process.exit(1); });
"""


def run_node(mode: str) -> dict:
    with tempfile.TemporaryDirectory() as td:
        harness = Path(td) / "harness.cjs"
        harness.write_text(HARNESS, encoding="utf-8")
        r = subprocess.run([NODE, str(harness), str(ORCH_PATH), mode],
                           capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        raise AssertionError(f"harness ({mode}) упал: {r.stderr.strip()[:500]}")
    return json.loads(r.stdout.strip().splitlines()[-1])


@unittest.skipIf(NODE is None, "node недоступен — исполняемая проверка не может запуститься")
class StuckIssuesFetchesAllPages(unittest.TestCase):
    """production stuckIssues() вытаскивает все страницы (PRO-72)."""

    def test_63_issues_two_pages_all_returned(self):
        out = run_node("stuck")
        self.assertEqual(len(out["ids"]), 63,
                         "stuckIssues потерял часть зависших — пагинация не работает")
        self.assertEqual(len(set(out["ids"])), 63, "дубли в выборке зависших")
        self.assertGreaterEqual(len(out["requests"]), 2, "страницы не проходятся курсором")
        self.assertIsNone(out["requests"][0]["variables"]["after"],
                          "первый запрос не должен передавать after")
        self.assertEqual(out["requests"][1]["variables"]["after"], "50",
                         "второй запрос не продолжает с endCursor первой страницы")

    def test_filter_unchanged_team_label_state(self):
        out = run_node("stuck")
        for r in out["requests"]:
            m = re.search(r"first:\s*(\d+)", r["query"])
            self.assertIsNotNone(m, "в запросе нет first")
            self.assertGreaterEqual(int(m.group(1)), 50)
            f = r["variables"]["f"]
            self.assertEqual(f["team"]["key"]["eq"], "PRO")
            self.assertEqual(f["labels"]["name"]["eq"], "swarm")
            self.assertEqual(f["state"]["name"]["eq"], "In Progress")


@unittest.skipIf(NODE is None, "node недоступен — исполняемая проверка не может запуститься")
class Incident13StuckRequeuedInOneCycle(unittest.TestCase):
    """Инцидент PRO-72: 13 зависших In Progress — все 13 получают ♻️-комментарий
    и возврат в Todo за один проход цикла; свежий клейм не трогается."""

    def test_all_13_stale_requeued_fresh_untouched(self):
        out = run_node("requeue")
        stale = sorted(f"PRO-{100 + k}" for k in range(13))
        todo = sorted(s["id"] for s in out["setStates"])
        self.assertEqual(todo, stale,
                         "не все зависшие возвращены в Todo за один цикл "
                         f"(вернулось {len(todo)} из 13)")
        self.assertTrue(all(s["name"] == "Todo" for s in out["setStates"]))
        flagged = sorted(c["id"] for c in out["comments"] if "♻️" in c["body"])
        self.assertEqual(flagged, stale,
                         "не всем зависшим поставлен ♻️-комментарий")
        self.assertEqual(out["claimsLeft"], ["PRO-FRESH"],
                         "клейм свежей работы затёрт или клеймы зависших не стёрты")


if __name__ == "__main__":
    unittest.main()
