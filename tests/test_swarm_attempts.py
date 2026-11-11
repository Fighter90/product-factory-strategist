"""PRO-64 (раунд 3, отзыв reviewer'а): attempts.json фактически не писался — saveAttempts
не вызывался в ветке провала гейтов, а try/catch вокруг чтения/записи глотал все ошибки;
auto-stash до выбора задачи молча уносил WIP человека (tracked + весь untracked) там, где
по контракту безопасности должен быть аборт. Тесты сверяют scripts/swarm/orchestrator.mjs
по исходнику (приём как в test_swarm_roles.py для не-Python-кода):

1. грязное дерево до pick → аборт, никакого stash;
2. каждая ветка провала задачи (gates и review) инкрементирует и сохраняет счётчик;
3. счётчик затухает (TTL), иначе задача с двумя старыми провалами навсегда паркуется
   в Backlog; legacy-записи без ts считаются истёкшими;
4. ошибки чтения/записи счётчика логируются, а не глотаются молча;
5. успех сбрасывает счётчик задачи.
"""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORCH = (ROOT / "scripts" / "swarm" / "orchestrator.mjs").read_text(encoding="utf-8")


def seg_between(start: str, stop: str) -> str:
    """Текст от первого вхождения start до ближайшего stop после него."""
    i = ORCH.find(start)
    if i < 0:
        raise AssertionError(f"orchestrator.mjs: маркер не найден: {start!r}")
    j = ORCH.find(stop, i + len(start))
    if j < 0:
        raise AssertionError(f"orchestrator.mjs: маркер не найден: {stop!r}")
    return ORCH[i:j]


class DirtyTreePolicy(unittest.TestCase):
    def test_pick_aborts_on_dirty_tree_without_stash(self):
        """Грязное дерево до выбора задачи → безопасный аборт; auto-stash (уносит WIP
        человека: tracked-правки и весь untracked) не возвращается в секцию pick."""
        seg = seg_between("дерево: сбросить типовой чурн", "git fetch origin")
        self.assertIn(
            "working tree is not clean — aborting before pick", seg,
            "pick не абортит на грязном дереве — нарушен контракт безопасности README",
        )
        self.assertNotIn("git stash push", seg,
                         "auto-stash вернулся в секцию pick (уносит WIP человека)")

    def test_header_still_documents_abort(self):
        self.assertIn("отказ при грязном дереве", ORCH)


class AttemptsCounter(unittest.TestCase):
    def test_both_failure_branches_bump_and_save(self):
        """Провал задачи должен и инкрементировать счётчик, и сохранять attempts.json:
        в round 3 saveAttempts не вызывался в ветке гейтов — файл никогда не писался."""
        gates = seg_between("failIssue(issue, 'gates'", "devStatus = 'gates-failed'")
        self.assertIn("bumpAttempts(issue.identifier)", gates,
                      "ветка провала гейтов не пишет счётчик попыток")
        review = seg_between("failIssue(issue, 'review'", "continue;")
        self.assertIn("bumpAttempts(issue.identifier)", review,
                      "ветка провала ревью не пишет счётчик попыток")
        self.assertEqual(ORCH.count("bumpAttempts(issue.identifier)"), 2,
                         "bumpAttempts должен вызываться ровно в двух ветках провала")

    def test_failure_at_limit_does_not_requeue(self):
        """На 2-й провал задача не возвращается в Todo — пик-луп следующего запуска
        запаркует её в Backlog (человек разбирает вручную)."""
        for name, seg in (("gates", seg_between("failIssue(issue, 'gates'", "devStatus = 'gates-failed'")),
                          ("review", seg_between("failIssue(issue, 'review'", "continue;"))):
            self.assertIn("if (tr < 2)", seg, f"ветка {name}: задача возвращается в Todo и на 2-м провале")

    def test_pick_loop_skips_parked_issues(self):
        self.assertIn("triesOf(issue.identifier) >= 2", ORCH,
                      "пик-луп не пропускает задачи с исчерпанными попытками")

    def test_counter_has_ttl_decay(self):
        """Записи счётчика затухают: запись с ts старше TTL не загружается, иначе задача
        с двумя провалами в любом прошлом прогоне паркуется навсегда."""
        self.assertRegex(ORCH, r"ATTEMPT_TTL_DAYS\s*=\s*\d+", "нет TTL-константы затухания")
        self.assertIn("now - ts < ATTEMPT_TTL_MS", ORCH, "загрузка не отбрасывает истёкшие записи")
        self.assertIn("typeof v.ts === 'number') ? v.ts : 0", ORCH,
                      "legacy-записи без ts не считаются истёкшими")

    def test_success_resets_counter(self):
        seg = seg_between("await doneIssue(issue, evidence)", "log(`=== DONE")
        self.assertIn("attempts.delete(issue.identifier); saveAttempts();", seg,
                      "успешный шип не сбрасывает счётчик задачи")

    def test_io_errors_logged_not_swallowed(self):
        """Ошибки чтения/записи счётчика логируются — пустые catch скрывали потерю
        attempts.json (замечание reviewer'а round 3)."""
        load = seg_between("const loadAttempts", "const attempts = loadAttempts()")
        self.assertIn("log(", load, "loadAttempts глотает ошибки чтения/парсинга молча")
        self.assertIn("ENOENT", load, "отсутствие файла должно отличаться от ошибки чтения")
        save = seg_between("const saveAttempts", "const bumpAttempts")
        self.assertIn("log(", save, "saveAttempts глотает ошибки записи молча")


if __name__ == "__main__":
    unittest.main()
