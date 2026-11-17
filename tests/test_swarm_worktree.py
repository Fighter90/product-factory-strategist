"""PRO-81: рой писал в общий чекаут — executor изолируется worktree'ом.

Факт сквозного QA (тело задачи): supervisor запускает executor'ов в ЕДИНОМ
чекауте ~/Projects/product-factory-strategist — параллельный прогон сюиты в
чекауте гонится с пишущим воркером (тесты мигают), финальная верификация
возможна только в изолированном клоне; зомби-циклы оставляют полу-фичи в
рабочем дереве (гибрид export.py с NameError), supervisor-stash таскает их
туда-сюда.

Контракт (labourer-паттерн, как в ручных worktree .task-board/wt-*):
1. executor получает отдельный `git worktree add` от свежего origin/main в
   gitignored-каталоге .task-board/wt-<id>; ветка прошлой попытки
   переиспользуется (продолжение работы), протухший worktree (краш/таймаут)
   сносится до add;
2. executor-воркер, гейты, счётчик коммитов, дифф ревьюера и cherry-pick
   спасения работают ВНУТРИ worktree (cwd / git -C WT) — общий чекаут
   остаётся супервизору, его HEAD всегда на origin/main;
3. релизный rebase и fallback squash тоже исполняются в worktree (cwd: WT) —
   merge/PR «оттуда», как сформулировано в задаче;
4. knowledge/ (gitignored, приватный -base) доступен в worktree симлинком —
   без него падают kb-тесты гейтов (test_kb_lint, test_docs_parity);
5. по завершении (успех, blocked, cancel, review-fail, already-merged, краш)
   worktree сносится — stash-цепочки «blocked leftovers» исчезают;
6. guard живого воркера (PRO-73) признаёт cwd ПОД ROOT (worktree исполнителя),
   а не только точное равенство ROOT — иначе тик срывает ветку живого воркера.

Тесты сверяют scripts/swarm/orchestrator.mjs по исходнику — приём соседних
swarm-тестов (test_swarm_attempts.py): запуск node в unittest не нужен
(кроме синтакс-проверки, она скипается без node).
"""
import shutil
import subprocess
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


class WorktreeContract(unittest.TestCase):
    """Executor работает в отдельном git worktree от свежего origin/main."""

    def test_worktree_path_is_per_issue_under_task_board(self):
        """Worktree — per-issue каталог в gitignored .task-board (не в корне репо:
        незарегистрированные каталоги-«вт» в корне мусорили git status)."""
        self.assertIn("const wtDir = (id) => resolve(STATE, `wt-${id.toLowerCase()}`);", ORCH)

    def test_worktree_created_from_fresh_main(self):
        """Свежая ветка — `worktree add -B <branch> <WT> origin/main` (создаёт/сбрасывает
        ветку на свежий main), а не checkout в общем чекауте."""
        self.assertIn("git worktree add -B ${branch} ${JSON.stringify(WT)} origin/main", ORCH)

    def test_existing_attempt_branch_is_reused(self):
        """Ветка прошлой попытки переиспользуется (add без -B по show-ref, --force
        против чужого протухшего registration) — попытка 2 продолжает работу
        попытки 1, как прежний `git checkout ${branch}`."""
        self.assertIn("git show-ref --verify -q refs/heads/${branch}", ORCH)
        self.assertIn("git worktree add --force ${JSON.stringify(WT)} ${branch}", ORCH)

    def test_stale_worktree_dropped_before_add(self):
        """Протухший worktree прошлой попытки/краша сносится ДО add — иначе add падает
        «already exists», а зомби-хвосты живут вечно."""
        seg = seg_between("// ---- worktree исполнителя", "let reviewNotes = ''")
        self.assertIn("await dropWorktree();", seg, "перед add не сносится протухший worktree")
        self.assertLess(seg.index("await dropWorktree();"), seg.index("worktree add"),
                        "снос worktree должен быть до worktree add")


class SharedCheckoutContract(unittest.TestCase):
    """Общий чекаут остаётся только супервизору: его HEAD всегда на origin/main."""

    def test_round_loop_never_checks_out_branch_in_shared_tree(self):
        """Цикл разработки не переключает общий чекаут на ветку исполнителя —
        прежний `git checkout -q ${branch}` в ROOT исчез (источник гонок и срывов)."""
        self.assertNotIn("git checkout -q ${branch}", ORCH)

    def test_worker_supports_cwd(self):
        """worker() принимает cwd (дефолт ROOT) и передаёт его в run() —
        reviewer/documenter остаются в общем чекауте, executor уходит в worktree."""
        worker_body = seg_between("async function worker(", "const after = ")
        self.assertIn("cwd = ROOT", worker_body, "worker() без cwd-опции")
        self.assertIn("{ timeoutMs, cwd, onSpawn", worker_body,
                      "worker() не передаёт cwd в run() — опция молча теряется")

    def test_executor_runs_in_worktree(self):
        """Вызов executor-воркера передаёт cwd worktree."""
        self.assertIn("}, { cwd: WT });", ORCH, "executor не получает cwd worktree")

    def test_gates_run_in_worktree(self):
        """Гейты (unittest + doctor) гоняются в worktree исполнителя: на его коде и
        без гонки с пишущим воркером в общем чекауте."""
        gates = seg_between("const gates = await sh(", "const passLine")
        self.assertIn("cwd: WT", gates, "гейты не в worktree исполнителя")

    def test_dev_rebase_runs_in_worktree(self):
        """Ребейз цикла разработки — внутри worktree (git -C WT), не в ROOT."""
        dev_rb = seg_between("const devRb = await sh(", "if (devRb.all.includes")
        self.assertIn("gwt('rebase origin/main')", dev_rb, "ребейз разработки не в worktree")
        self.assertNotIn("git rebase origin/main", dev_rb,
                         "голый `git rebase` в сегменте разработки — операция ушла в общий чекаут")

    def test_dev_commit_count_from_worktree(self):
        """Счётчик коммитов ветки — по HEAD worktree (в ROOT HEAD = origin/main,
        старый счёт по HEAD супервизора всегда давал бы 0)."""
        self.assertIn("gwt('rev-list --count origin/main..HEAD')", ORCH)
        self.assertNotIn("sh(`git rev-list --count origin/main..HEAD`)", ORCH,
                         "счётчик коммитов по HEAD общего чекаута")

    def test_rescue_cherry_pick_lands_in_worktree(self):
        """Reflog-спасение: cherry-pick потерянного коммита — в worktree исполнителя."""
        self.assertIn("gwt(`cherry-pick ${sha}`)", ORCH)
        self.assertNotIn("sh(`git cherry-pick ${sha}`)", ORCH,
                         "cherry-pick в общий чекаут — потерянная работа ушла не туда")

    def test_review_diff_taken_from_worktree(self):
        """Дифф для ревьюера — из worktree (в ROOT против HEAD супервизора дифф пуст)."""
        self.assertIn("gwt('diff origin/main...HEAD')", ORCH)
        self.assertNotIn("sh(`git diff origin/main...HEAD`)", ORCH,
                         "дифф ревьюера по HEAD общего чекаута — всегда пустой")


class ReleaseFromWorktreeContract(unittest.TestCase):
    """«По завершении — merge/PR оттуда»: релизный rebase/squash исполняются в worktree."""

    def test_release_rebase_runs_in_worktree(self):
        self.assertIn("{ timeoutMs: 180_000, cwd: WT }", ORCH,
                      "релизный rebaseOntoMain не в worktree исполнителя")

    def test_fallback_squash_runs_in_worktree(self):
        seg = seg_between("const localSquash = async", "const rb = await")
        self.assertIn("cwd: WT", seg, "fallback squash-merge не в worktree исполнителя")

    def test_success_removes_worktree_before_branch_delete(self):
        """git branch -D ветки, держимой worktree, падает «used by worktree» —
        worktree сносится до удаления ветки."""
        pos_rm = ORCH.find("log('-- release manager: PR')")
        pos_del = ORCH.find("await sh(`git branch -D ${branch}`)")
        self.assertGreater(pos_del, 0, "нет удаления ветки после успеха")
        pos_drop = ORCH.rfind("await dropWorktree();", 0, pos_del)
        self.assertGreater(pos_drop, pos_rm,
                           "перед branch -D не сносится worktree исполнителя")


class CleanupContract(unittest.TestCase):
    """Зомби-хвосты не живут вне worktree: stash-цепочки «blocked leftovers» исчезают."""

    def test_blocked_leftovers_stash_chain_is_gone(self):
        self.assertNotIn("blocked executor leftovers", ORCH,
                         "stash-цепочка «blocked leftovers» осталась — хвосты теперь в worktree")

    def test_blocked_path_drops_worktree(self):
        seg = seg_between("devStatus === 'blocked'", "executor blocked; moving on")
        self.assertIn("await dropWorktree();", seg, "blocked-путь не чистит worktree исполнителя")
        self.assertNotIn("git stash push", seg, "blocked-путь тащит хвосты в stash общего чекаута")

    def test_crash_cleans_worktree(self):
        """Краш-безопасность (PRO-68): ребейз/merge в worktree абортятся, сам worktree
        сносится — следующий тик не наследует зомби-дерево."""
        catch = seg_between("} catch (e) {", "queue continues")
        self.assertIn("gwt('merge --abort')", catch, "merge в worktree не абортится при краше")
        self.assertIn("gwt('rebase --abort')", catch, "rebase в worktree не абортится при краше")
        self.assertIn("await dropWorktree();", catch, "краш-путь не сносит worktree исполнителя")

    def test_review_fail_keeps_branch_but_drops_worktree(self):
        """Ревью вернуло работу: ветка (коммиты) остаётся для попытки 2,
        worktree сносится — попытка 2 начнёт с чистого дерева той же ветки."""
        seg = seg_between("if (!accepted) {", "continue;")
        self.assertIn("await dropWorktree();", seg, "review-fail не чистит worktree исполнителя")
        self.assertNotIn("branch -D", seg, "review-fail не должен удалять ветку попытки")

    def test_no_release_stop_drops_worktree(self):
        """--no-release (стоп после ACCEPT + документ): ветка остаётся человеку,
        worktree исполнителя не зомби."""
        seg = seg_between("if (NO_RELEASE)", "break; }")
        self.assertIn("await dropWorktree();", seg, "--no-release не чистит worktree исполнителя")


class KnowledgeSymlinkContract(unittest.TestCase):
    """knowledge/ (gitignored, приватный -base) в worktree — симлинком на общий клон."""

    def test_worktree_gets_knowledge_symlink(self):
        seg = seg_between("// ---- worktree исполнителя", "let reviewNotes = ''")
        self.assertIn("ln -sfn", seg, "нет симлинка knowledge в worktree")
        self.assertIn("resolve(ROOT, 'knowledge')", seg,
                      "симлинк должен указывать на общий клон knowledge супервизора")


class GuardContract(unittest.TestCase):
    """Interplay с PRO-73 (ревью раунд 2): guard узнаёт воркеров роя по их
    ФАКТИЧЕСКИМ местам — ROOT (reviewer/documenter, дефолт cwd) и .task-board/
    (worktree исполнителя .task-board/wt-<id>), а не по любому подкаталогу ROOT."""

    def test_guard_accepts_executor_worktree_cwd(self):
        """Worktree исполнителя — .task-board/wt-<id>: guard узнаёт его по префиксу
        STATE (.task-board), иначе тик срывает ветку живого воркера."""
        guard = seg_between("async function tickWorkerAlive", "async function main()")
        self.assertIn("dir === ROOT", guard,
                      "guard не признаёт reviewer/documenter в общем чекауте (cwd = ROOT)")
        self.assertIn("startsWith(STATE + '/')", guard,
                      "guard не признаёт worktree исполнителя (.task-board/wt-<id>) — "
                      "тик срывает ветку живого воркера")
        self.assertIn("!dir", guard, "консервативный fallback PRO-73 (пустой cwd) должен остаться")

    def test_guard_does_not_claim_every_subdir_of_root(self):
        """Широкий префикс ROOT+'/' убран: интерактивная сессия opencode человека
        в ROOT/projects/<slug> — не воркер роя; прежний guard при мёртвом владельце
        оркестратора убивал её как «сироту» (killTree)."""
        guard = seg_between("async function tickWorkerAlive", "async function main()")
        self.assertNotIn("startsWith(ROOT + '/')", guard,
                         "широкий префикс ROOT+'/' остался — сессии opencode в "
                         "ROOT/projects/<slug> осиротевают и убиваются")


class CwdForwardingContract(unittest.TestCase):
    """Ревью раунд 2: cwd реально доходит до spawn(). Call-site тесты («cwd: WT»)
    молчащий no-op не ловят: если run() строит spawn-параметры без cwd, вся
    изоляция исполнителя — фикция на бумаге. Контракт замыкается по исходнику."""

    def test_run_accepts_and_forwards_cwd_to_spawn(self):
        """run() принимает cwd (дефолт ROOT) и пересылает его в spawn()."""
        run_body = seg_between("function run(cmd, args_", "const sh = ")
        self.assertIn("cwd = ROOT", run_body, "run() не принимает cwd-опцию с дефолтом ROOT")
        self.assertIn("spawn(cmd, args_, { cwd,", run_body,
                      "run() не пересылает cwd в spawn() — опция теряется молча")

    def test_sh_forwards_opts_with_cwd_into_run(self):
        """sh() пересылает opts (включая cwd) в run() — иначе `sh(..., { cwd: WT })`
        гейтов и релиза исполнялись бы в общем чекауте."""
        sh_body = seg_between("const sh = async", "const activeWorkers")
        self.assertIn("await run('bash', ['-lc', cmd], opts)", sh_body,
                      "sh() не пересылает opts с cwd в run()")


class OrchestratorParses(unittest.TestCase):
    """Изоляция не должна ломать синтаксис: node --check как smoke-гейт."""

    def test_node_syntax_check(self):
        if not shutil.which("node"):
            self.skipTest("node недоступен — синтаксис не проверить")
        r = subprocess.run(["node", "--check", str(ROOT / "scripts" / "swarm" / "orchestrator.mjs")],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, f"orchestrator.mjs не парсится: {r.stderr[:300]}")


if __name__ == "__main__":
    unittest.main()
