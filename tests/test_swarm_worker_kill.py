"""PRO-69 (факт из лога 2026-11-12, PRO-54 round 1): таймаут воркера не убивал процесс.

Ревьюер стартовал 20:41:34 (timeoutMs = 12 × 60_000), закончился 22:05:16 code=-1 —
83.7 мин вместо 12: group-kill `process.kill(-p.pid, 'SIGKILL')` «прошёл» без
исключения, но цель не достиг (процесс вне группы), а прямой kill был только в
catch-ветке и не выполнялся; run() не резолвился, цикл стоял 84 мин. Ранее —
обратный случай: shell-процесс умер по лимиту, а воркеры с timeout жили дольше него.

Контракт (три слоя защиты):

1. run() спавнит воркера в НОВОЙ ГРУППЕ (detached: true) — group-kill возможен;
2. killTree на таймауте: снапшот поддерева по ps ДО убийства (после смерти корня
   сироты переродятся на init и связь потеряется), затем group-kill + прямой
   p.kill('SIGKILL') БЕЗУСЛОВНО (не только в catch), затем эскалация по живым
   потомкам из снапшота с проверкой живости (poll kill(0)); run() резолвится
   гарантированно (finish(-1) после killTree) — ревьюер не живёт дольше timeout + 5 с;
3. воркер не переживает оркестратор: живые воркеры получают SIGKILL при выходе
   (exit + SIGINT/SIGTERM/SIGHUP), pid-файл записывает владельца, а guard следующего
   тика убивает сироту (владелец мёртв) тем же killTree — осиротевшие воркеры
   больше не воюют за дерево (инциденты 19:0x/19:2x).

Тесты сверяют scripts/swarm/orchestrator.mjs по исходнику (приём как в
test_swarm_attempts.py), а слои 1–2 дополнительно исполняют под node с реальными
процессами («тест-пингвин»: sleep 600 + timeoutMs 2000 — смерть ≤ 5 с, процесса
нет в ps; инцидент-репродукция: воркер, породивший отвязанного внука, — умирают
оба). node нужен оркестратору и swarm-машине; если node недоступен, поведенческие
тесты пропускаются, а проверки по исходнику остаются обязательными.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORCH_PATH = ROOT / "scripts" / "swarm" / "orchestrator.mjs"
ORCH = ORCH_PATH.read_text(encoding="utf-8")

NODE = shutil.which("node")
POSIX = sys.platform != "win32"


def seg_between(start: str, stop: str, src: str = ORCH) -> str:
    """Текст от первого вхождения start до ближайшего stop после него."""
    i = src.find(start)
    if i < 0:
        raise AssertionError(f"orchestrator.mjs: маркер не найден: {start!r}")
    j = src.find(stop, i + len(start))
    if j < 0:
        raise AssertionError(f"orchestrator.mjs: маркер не найден: {stop!r}")
    return src[i:j]


RUN_SEG = seg_between("function run(cmd, args_", "const sh = async")
KILL_SEG = seg_between("async function descendants(", "function run(cmd, args_")
WORKER_SEG = seg_between("async function worker(", "const after = ")
GUARD_SEG = seg_between("async function tickWorkerAlive", "async function main()")


# --- источник: слой 1 — новая группа ---------------------------------------


class SpawnContract(unittest.TestCase):
    def test_run_spawns_in_new_group(self):
        """Воркер спавнится detached (новая группа, pgid == pid) — иначе
        group-kill `kill(-pid)` бьёт в пустоту или чужую группу."""
        self.assertIn("detached: true", RUN_SEG,
                      "run() спавнит воркера без detached — группа не создаётся")

    def test_group_kill_target_is_child_group(self):
        """Group-kill целяется в ГРУППУ ребёнка (-pid) через killTree."""
        self.assertIn("killTree(p.pid, p)", RUN_SEG,
                      "таймаут run() не передаёт pid ребёнка в killTree")
        self.assertIn("process.kill(-rootPid, 'SIGKILL')", KILL_SEG,
                      "killTree не делает group-kill по группе ребёнка")


# --- источник: слой 2 — killTree с проверкой и эскалацией -------------------


class KillTreeContract(unittest.TestCase):
    def test_timeout_uses_killtree_not_bare_group_kill(self):
        """Таймаут run() вызывает killTree — прежний однослойный паттерн
        (group-kill, прямой kill только в catch) не возвращается."""
        self.assertIn("killTree(p.pid, p)", RUN_SEG,
                      "таймаут run() не вызывает killTree — убить должен многослойный killer")
        self.assertNotIn(
            "catch { try { p.kill('SIGKILL'); } catch {} }", RUN_SEG,
            "прямой kill остался только в catch-ветке group-kill — при «успешном» "
            "но не достигшем group-kill fallback не выполняется (форма инцидента PRO-69)",
        )

    def test_killtree_kills_group_and_direct(self):
        """killTree бьёт и по группе (-rootPid), и напрямую по процессу — группа
        могла не достать (процесс вне группы)."""
        self.assertIn("process.kill(-rootPid, 'SIGKILL')", KILL_SEG,
                      "killTree не делает group-kill")
        self.assertIn("kill('SIGKILL')", KILL_SEG,
                      "killTree не делает прямого kill — единственный слой group-kill ненадёжен")

    def test_killtree_snapshots_tree_before_kill(self):
        """Снапшот поддерева по ps берётся ДО убийства: после смерти корня сироты
        перерождаются на init (ppid 1) — связь теряется, эскалация их не найдёт."""
        snap = KILL_SEG.find("await descendants(rootPid)")
        kill = KILL_SEG.find("process.kill(-rootPid, 'SIGKILL')")
        self.assertGreater(snap, 0, "killTree не строит снапшот поддерева по ps")
        self.assertGreater(kill, 0)
        self.assertLess(snap, kill, "снапшот после group-kill — потомки-сироты потеряны")

    def test_killtree_descendants_walk_uses_ps(self):
        """Поддерево собирается из ps (pid+ppid обходом), а не из догадок."""
        self.assertIn("ps", KILL_SEG, "снапшот поддерева не через ps")
        self.assertIn("ppid", KILL_SEG, "обход поддерева не по ppid — потомков не найти")

    def test_killtree_polls_liveness(self):
        """Эскалация с проверкой живости (poll kill(pid, 0); EPERM = жив чужой процесс),
        а не выстрел вслепую: по живым из снапшота бьём повторно, с паузами."""
        self.assertIn("process.kill(pid, 0)", KILL_SEG,
                      "killTree не проверяет живость цели")
        self.assertIn("EPERM", KILL_SEG,
                      "EPERM не считается живостью — чужой процесс сочтётся мёртвым")
        poll = KILL_SEG.find("process.kill(pid, 0)")
        rest = KILL_SEG[poll:]
        self.assertIn("for (const pid of alive)", rest,
                      "после проверки живости нет повторного SIGKILL по живым")
        self.assertIn("await sleep(", rest,
                      "эскалация без паузы — poll вырождается в спин-цикл")

    def test_run_resolves_after_timeout_guaranteed(self):
        """run() резолвится гарантированно даже при отказе killTree: finish(-1) в
        обработчике таймаута — ревьюер не подвешивает цикл на 84 мин (инцидент)."""
        t_start = RUN_SEG.find("const t = setTimeout(")
        self.assertGreater(t_start, 0, "в run() нет таймера таймаута")
        t_seg = RUN_SEG[t_start:RUN_SEG.find("}, timeoutMs)")]
        self.assertIn("finish(-1)", t_seg,
                      "таймаут не резолвит промис принудительно — run() может висеть вечно")

    def test_killtree_reports_outcome(self):
        """killTree сообщает, убил ли: неудача эскалации не глотается молча."""
        self.assertIn("return", KILL_SEG, "killTree не возвращает результат эскалации")


# --- источник: слой 3 — воркер не переживает оркестратор --------------------


class OutlivesContract(unittest.TestCase):
    def test_worker_pid_file_records_owner(self):
        """pid-файл воркера записывает pid владельца (оркестратора) — по нему guard
        следующего тика отличает сироту от воркера живого владельца."""
        self.assertIn("${p} ${process.pid}", WORKER_SEG,
                      "в worker.pid нет pid владельца — сироту не отличить")

    def test_worker_tracked_in_active_set(self):
        """Живой воркер регистрируется на время работы и снимается с учёта после."""
        self.assertIn("activeWorkers.add", WORKER_SEG,
                      "воркер не регистрируется как живой")
        self.assertIn("activeWorkers.delete", WORKER_SEG,
                      "воркер не снимается с учёта после завершения run()")

    def test_exit_reaps_active_workers(self):
        """При выходе оркестратора живые воркеры получают SIGKILL — воркер не
        переживает родителя (осиротевшие воркеры воевали за дерево, 19:0x/19:2x)."""
        self.assertIn("process.on('exit'", ORCH, "нет exit-хука реапа воркеров")
        reap_pos = ORCH.find("const activeWorkers")
        reap_seg = ORCH[reap_pos:ORCH.find("async function main()")]
        self.assertIn("activeWorkers", reap_seg,
                      "exit-хук не убивает зарегистрированных воркеров")
        self.assertIn("-pid, 'SIGKILL'", reap_seg,
                      "exit-хук бьёт только по одиночному pid — группа может не умереть")

    def test_signals_reap_before_exit(self):
        """SIGINT/SIGTERM/SIGHUP сначала реапят воркеров, потом завершают процесс."""
        for sig in ("SIGINT", "SIGTERM", "SIGHUP"):
            with self.subTest(sig=sig):
                self.assertIn(sig, ORCH, f"{sig} не обрабатывается — воркер переживёт сигнал")

    def test_guard_kills_orphan_of_dead_owner(self):
        """Guard следующего тика: воркер с живым pid, но мёртвым владельцем — сирота;
        убивается тем же killTree, pid-файл стирается, тик продолжается (return 0),
        а не ждёт остаток жизни сироты (прежде guard «держал очередь пустой»)."""
        self.assertIn("killTree(pid)", GUARD_SEG,
                      "guard не убивает сироту — осиротевший воркер воюет за дерево")
        self.assertIn("unlinkSync(WORKER_PID)", GUARD_SEG,
                      "guard не стирает pid-файл сироты — следующий тик убивает повторно")
        self.assertIn("orphan worker", GUARD_SEG,
                      "хвосты убитого сироты не упаковываются в stash с опознаваемой меткой")

    def test_orphan_kill_only_after_identity_checks(self):
        """Сироту убиваем только ПОСЛЕ опознания (это opencode этого репо по cwd):
        переиспользованный pid чужого процесса не должен получить SIGKILL."""
        oc = GUARD_SEG.find("/opencode/.test")
        cwd_ok = GUARD_SEG.find("(dir === ROOT || dir.startsWith(ROOT + '/')")
        orphan = GUARD_SEG.find("killTree(pid)")
        self.assertGreater(oc, 0, "guard потерял проверку команды (opencode)")
        self.assertGreater(cwd_ok, 0, "guard потерял сверку cwd с корнем репо")
        self.assertGreater(orphan, 0)
        self.assertLess(oc, orphan, "сирота убивается до проверки команды — риск чужого pid")
        self.assertLess(cwd_ok, orphan, "сирота убивается до сверки cwd — риск чужого pid")

    def test_orphan_path_proceeds_tick(self):
        """После убийства сироты тик продолжается (return 0), а живой владелец —
        как прежде (guard-skip PRO-73 через return pid)."""
        orphan = GUARD_SEG.find("killTree(pid)")
        self.assertGreater(orphan, 0)
        tail = GUARD_SEG[orphan:]
        self.assertIn("return 0", tail, "убийство сироты не продолжило тик")
        self.assertIn("return pid;", tail, "guard-skip живого владельца (PRO-73) потерян")


# --- поведение (node, production-код исполняется как есть) ------------------

HARNESS = r"""
// Исполнитель production-блока orchestrator.mjs (sleep + descendants + killTree + run)
// с реальными процессами. Сценарий argv[3]:
//   'plain'  — воркер `sleep 600`, timeoutMs 2000 («тест-пингвин»);
//   'escape' — воркер (node) порождает ОТВЯЗАННОГО внука (detached → новая сессия,
//              переживёт group-kill) и виснет — инцидент-форма PRO-69.
const fs = require('fs');
const { spawn } = require('child_process');
const src = fs.readFileSync(process.argv[2], 'utf8');
const mode = process.argv[3];

function seg(start, stop) {
  const i = src.indexOf(start);
  if (i < 0) throw new Error('маркер не найден: ' + start);
  const j = src.indexOf(stop, i + start.length);
  if (j < 0) throw new Error('маркер не найден: ' + stop);
  return src.slice(i, j);
}

// production-код — исполняется как есть, без правок
const block = seg('const sleep = ', 'const sh = async');

(async () => {
  const ROOT = process.cwd();
  await eval(block + `
    (async () => {
      const t0 = Date.now();
      let wpid = 0;
      const opts = { timeoutMs: 2000, onSpawn: (pid) => { wpid = pid; } };
      let r;
      if (mode === 'escape') {
        r = await run(process.execPath, ['-e', process.env.WORKER_SCRIPT], opts);
      } else {
        r = await run('sleep', ['600'], opts);
      }
      console.log(JSON.stringify({ elapsedMs: Date.now() - t0, code: r.code, pid: wpid }));
    })().catch((e) => { console.error('HARNESS: ' + String(e)); process.exit(1); });
  `);
})().catch((e) => { console.error(String(e)); process.exit(1); });
"""

WORKER_SCRIPT = (
    "const { spawn } = require('child_process');const fs = require('fs');"
    "const gc = spawn(process.execPath, ['-e', 'setInterval(()=>{},1000)'],"
    " { detached: true, stdio: 'ignore' });"
    "fs.writeFileSync(process.env.GC_FILE, String(gc.pid));"
    # воркер «завис» после порождения внука — как ревьюер из инцидента PRO-69
    "setInterval(() => {}, 1000);"
)


def run_node(mode: str, extra_env: dict | None = None) -> dict:
    env = dict(os.environ)
    env.update(extra_env or {})
    with tempfile.TemporaryDirectory() as td:
        harness = Path(td) / "harness.cjs"
        harness.write_text(HARNESS, encoding="utf-8")
        r = subprocess.run([NODE, str(harness), str(ORCH_PATH), mode],
                           capture_output=True, text=True, timeout=60, env=env,
                           cwd=td)
    if r.returncode != 0:
        raise AssertionError(f"harness ({mode}) упал: {r.stderr.strip()[:500]}")
    return json.loads(r.stdout.strip().splitlines()[-1])


def pid_alive(pid: int) -> bool:
    r = subprocess.run(["ps", "-p", str(pid), "-o", "pid="],
                       capture_output=True, text=True)
    return r.returncode == 0 and r.stdout.strip() != ""


@unittest.skipIf(NODE is None or not POSIX, "node/ps недоступны — исполняемая проверка не может запуститься")
class PenguinTestSleep600(unittest.TestCase):
    """Тест-пингвин (приёмка PRO-69): воркер sleep 600 + timeoutMs 2000 умирает,
    run() резолвится < 5 с, процесса нет в ps."""

    def test_sleep600_killed_within_bound(self):
        out = run_node("plain")
        self.assertLess(out["elapsedMs"], 5000,
                        f"воркер прожил {out['elapsedMs']} мс при таймауте 2000 — убить не удалось")
        self.assertNotEqual(out["code"], 0, "убитый воркер отчитался нулевым кодом")
        self.assertFalse(pid_alive(out["pid"]),
                         f"воркер pid {out['pid']} жив после таймаута — kill не достиг цели")


@unittest.skipIf(NODE is None or not POSIX, "node/ps недоступны — исполняемая проверка не может запуститься")
class EscapedGrandchildKilled(unittest.TestCase):
    """Инцидент-репродукция PRO-69: воркер-«ревьюер» с зависшим ответом и отвязанным
    внуком (вне группы) не живёт дольше timeout + 5 с; умирают И воркер, И внук."""

    def test_worker_and_detached_grandchild_die(self):
        with tempfile.TemporaryDirectory() as td:
            gc_file = Path(td) / "gc.pid"
            out = run_node("escape", {"WORKER_SCRIPT": WORKER_SCRIPT, "GC_FILE": str(gc_file)})
            gc_pid = int(gc_file.read_text().strip())
        self.assertLess(out["elapsedMs"], 2000 + 5000,
                        f"воркер прожил {out['elapsedMs']} мс — дольше timeout + 5 с (форма инцидента)")
        self.assertFalse(pid_alive(out["pid"]),
                         f"воркер pid {out['pid']} пережил таймаут")
        self.assertFalse(pid_alive(gc_pid),
                         f"отвязанный внук pid {gc_pid} пережил воркера — воюет за ресурсы (19:0x/19:2x)")


if __name__ == "__main__":
    unittest.main()
