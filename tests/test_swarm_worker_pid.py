"""PRO-73: супервизор срывает свежезапущенного воркера детачем origin/main.

Опасное окно: воркер (`opencode run`) грузится 10–30 с и за это время ещё не сделал
ни одной правки — дерево «чисто», следующий тик оркестратора проходит проверку
чистоты и `git checkout --detach origin/main` срывает ветку воркера (воркер гибнет
за 7–10 с, клейм остаётся, In Progress копится, очередь пустеет).

Контракт оркестратора (вариант 2 из задачи):
1. каждый воркер пишет свой pid в .task-board/worker.pid;
2. тик при живом pid воркера этого репо завершается сразу — до лока, pick и
   detach (не заходит в pick до смерти воркера);
3. guard отличает живого воркера от переиспользованного pid (команда и cwd).

Тесты сверяют scripts/swarm/orchestrator.mjs по исходнику — приём соседних
swarm-тестов (test_swarm_attempts.py): запуск node в unittest не нужен.
"""
import re
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


class WorkerPidContract(unittest.TestCase):
    def test_pid_file_lives_in_task_board(self):
        """Pid-файл воркера — в state-каталоге .task-board (рядом с lock/claimed.json)."""
        self.assertIn("resolve(STATE, 'worker.pid')", ORCH)

    def test_run_reports_spawned_pid(self):
        """run() умеет отдать наружу pid spawn'нутого процесса (onSpawn-хук)."""
        run_body = seg_between("function run(cmd, args_", "const sh = ")
        self.assertIn("onSpawn", run_body, "run() не принимает onSpawn-хук")
        self.assertIn("p.pid", run_body, "run() не отдаёт spawn'нутый pid")

    def test_worker_writes_pid_file_on_spawn(self):
        """Каждый воркер (`opencode run`) пишет свой pid — не только executor."""
        worker_body = seg_between("async function worker(", "const after = ")
        self.assertIn("onSpawn", worker_body, "worker() не передаёт onSpawn в run()")
        self.assertIn("WORKER_PID", worker_body, "worker() не пишет pid воркера в файл")

    def test_tick_guard_checks_pid_command_and_cwd(self):
        """Guard живого воркера: pid жив + это opencode + cwd = корень этого репо
        (иначе переиспользованный pid чужого процесса заблокирует тик навсегда)."""
        guard = seg_between("async function tickWorkerAlive", "async function main()")
        self.assertIn("process.kill(pid, 0)", guard, "guard не проверяет живость pid")
        self.assertIn("opencode", guard, "guard не отличает opencode от чужого процесса")
        self.assertIn("cwd", guard, "guard не сверяет cwd с корнем репо")

    def test_skip_happens_before_lock_and_pick(self):
        """Тик при живом воркере завершается ДО лока и pick — single пропуск целиком,
        без stuck-requeue, detach и pick (пикер не должен видеть очередь вообще)."""
        guard_pos = ORCH.find("await tickWorkerAlive()")
        self.assertGreater(guard_pos, 0, "main() не вызывает guard живого воркера")
        lock_pos = ORCH.find("openSync(lock")
        self.assertGreater(lock_pos, 0)
        pick_pos = ORCH.find("await pickIssue()")
        self.assertGreater(pick_pos, 0)
        self.assertLess(guard_pos, lock_pos, "guard после лока — тик успевает захватить очередь")
        self.assertLess(guard_pos, pick_pos, "guard после pick — тик заходит в pick при живом воркере")

    def test_skip_exits_cleanly_with_code_zero(self):
        """Пропуск тика — не исключение: exit 1 гонит launchd в немедленный рестарт-цикл."""
        seg = seg_between("await tickWorkerAlive()", "const lock = resolve(STATE, 'lock')")
        self.assertIn("return", seg, "живой воркер должен завершать тик через return (код 0)")


def fs_bindings(source: str):
    """Имена, доступные из 'node:fs' (named-импорт); None для default/namespace-импорта."""
    m = re.search(r"import\s*(?:\{([^}]+)\}|(\w+(?:\s+as\s+\w+)?))\s*from\s*['\"]node:fs['\"]", source)
    if not m:
        raise AssertionError("orchestrator.mjs: import из 'node:fs' не найден")
    return None if m.group(1) is None else {b.strip() for b in m.group(1).split(",")}


class FsImportContract(unittest.TestCase):
    """Ревью раунд 2: guard читает worker.pid через readFileSync, worker() пишет его
    через writeFileSync. Если имени нет в import из 'node:fs' — КАЖДЫЙ тик падает с
    ReferenceError ещё до лока, супервизор уходит в бесконечный рестарт, рой лежит.
    Имена объявлены на main и диффом не трогались — тест замыкает контракт."""

    def test_guard_and_worker_fs_names_are_imported(self):
        for name in ("readFileSync", "writeFileSync"):
            with self.subTest(name=name):
                self.assertIn(name, fs_bindings(ORCH),
                              f"{name} нет в import из 'node:fs' — тик умрёт с ReferenceError до лока")

    def test_imported_names_are_the_ones_used(self):
        """Импортируются ровно те имена, что реально вызываются: guard (readFileSync)
        и onSpawn воркера (writeFileSync) — иначе контракт пустой."""
        self.assertIn("readFileSync(WORKER_PID", ORCH, "guard не читает worker.pid через readFileSync")
        self.assertIn("writeFileSync(WORKER_PID", ORCH, "worker() не пишет worker.pid через writeFileSync")

    def test_broken_import_is_caught(self):
        """Тест ловит дефект из отзыва: импорт без readFileSync/writeFileSync → падение."""
        broken = ORCH.replace(
            "import { openSync, writeSync, closeSync, readFileSync, writeFileSync, mkdirSync, existsSync, unlinkSync, appendFileSync } from 'node:fs';",
            "import { openSync, writeSync, closeSync, mkdirSync, existsSync, unlinkSync, appendFileSync } from 'node:fs';",
        )
        self.assertNotEqual(broken, ORCH, "эталонная строка импорта не найдена — тест не описывает реальный import")
        for name in ("readFileSync", "writeFileSync"):
            with self.subTest(name=name):
                self.assertNotIn(name, fs_bindings(broken),
                                 f"сломанный импорт содержит {name} — тест не ловит дефект отзыва")


if __name__ == "__main__":
    unittest.main()
