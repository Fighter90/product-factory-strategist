"""PRO-58: перенумерация тегов (pfs claim retag), защита реестров от ручной правки
и правило «чтение только внутри репозитория».

Покрывает: claims.retag — атомарная замена тегов [C###] во всех outputs/*.md с одной
записью в журнал; файл-выписку для source add --text-file — копию в sources/raw/ с
пометкой external_path, если файл лежал вне проекта; PreToolUse-хук .claude/hooks/
pre_guard.py (deny записи в claims/sources/decisions.jsonl и state.json с подсказкой
нужной команды pfs, ask для чтения вне репозитория); журнал ручных правок outputs
через Bash в post_tool.py.

Запуск: python3 -m unittest tests.test_guard_retag -v
"""
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TMP = tempfile.mkdtemp(prefix="pfs-test-guard-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from tools.pfs import claims, core, project, sources  # noqa: E402
from tools.pfs.core import PfsError  # noqa: E402


def fresh(slug):
    return project.create(f"Охрана {slug}", "Почему падает удержание?", slug=slug)


def run_hook(script: str, payload: dict) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(REPO / ".claude" / "hooks" / script)],
                          input=json.dumps(payload), capture_output=True, text=True,
                          cwd=REPO, env=os.environ.copy(), timeout=60)


class RetagTests(unittest.TestCase):
    """pfs claim retag: замена тегов [C###] во всех outputs одной командой, с журналом."""

    def setUp(self):
        self.pdir = fresh(f"retag{id(self)}")
        self.c1 = claims.add(self.pdir, "Рынок достаточен", "hypothesis")["id"]
        self.c2 = claims.add(self.pdir, "Сегмент стоит входа", "hypothesis")["id"]
        self.c3 = claims.add(self.pdir, "Фокус на семье", "inference", derived_from=[self.c1])["id"]
        (self.pdir / "outputs").mkdir(parents=True, exist_ok=True)
        self.doc = self.pdir / "outputs" / "04_product_strategy.md"
        # [C004] — висячий тег (утверждения C004 в реестре нет): retag правит теги, а не реестр.
        self.doc.write_text("Стратегия: рынок [C003], повтор [C003], фон [C004].\n", encoding="utf-8")

    def test_retag_replaces_and_logs(self):
        res = claims.retag(self.pdir, "C003", "C001")
        self.assertEqual(res["replacements"], 2)
        self.assertEqual(res["files"], 1)
        text = self.doc.read_text(encoding="utf-8")
        self.assertNotIn("[C003]", text)
        self.assertEqual(text.count("[C001]"), 2)
        self.assertIn("[C004]", text)  # чужие теги не тронуты
        rows = core.read_jsonl(self.pdir / "log.jsonl")
        self.assertTrue(any("retag" in r["msg"] and "C003" in r["msg"] and "C001" in r["msg"] for r in rows))

    def test_retag_across_documents(self):
        second = self.pdir / "outputs" / "02_situation.md"
        second.write_text("Ситуация отсылает к [C003].\n", encoding="utf-8")
        res = claims.retag(self.pdir, "C003", "C001")
        self.assertEqual(res["files"], 2)
        self.assertIn("[C001]", second.read_text(encoding="utf-8"))

    def test_retag_cli(self):
        r = subprocess.run([sys.executable, "-m", "tools.pfs", "--project", self.pdir.name,
                            "claim", "retag", "--from", "C003", "--to", "C001"],
                           capture_output=True, text=True, cwd=REPO, env=os.environ.copy(), timeout=120)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("[C003] → [C001]", r.stdout)
        self.assertNotIn("[C003]", self.doc.read_text(encoding="utf-8"))

    def test_retag_rejections(self):
        with self.assertRaises(PfsError):
            claims.retag(self.pdir, "C003", "C003")  # from == to
        with self.assertRaises(PfsError):
            claims.retag(self.pdir, "C003", "C099")  # цель не в реестре
        with self.assertRaises(PfsError):
            claims.retag(self.pdir, "C3", "C001")  # не формат C###
        with self.assertRaises(PfsError):
            claims.retag(self.pdir, "S001", "C001")  # тег утверждений, не источник
        with self.assertRaises(PfsError):
            claims.retag(self.pdir, "C002", "C001")  # в outputs нет ни одного [C002]
        before = self.doc.read_text(encoding="utf-8")
        self.assertEqual(self.doc.read_text(encoding="utf-8"), before)  # документ не тронут


class SourceExcerptTests(unittest.TestCase):
    """Выписка --text-file: копия в sources/raw/, файл вне проекта — с пометкой external_path."""

    def setUp(self):
        self.pdir = fresh(f"exc{id(self)}")
        self.body = "Выписка из отчёта Eurostat про рынок рекрутинга. " * 5

    def test_outside_file_copied_with_external_note(self):
        f = Path(TMP) / f"выписка_{id(self)}.md"
        f.write_text(self.body, encoding="utf-8")
        rec, created = sources.add(self.pdir, text=self.body, title="Eurostat", text_path=f)
        self.assertTrue(created)
        self.assertEqual(rec["external_path"], str(f.resolve()))  # resolve: /var → /private/var на macOS
        raw = self.pdir / "sources" / "raw" / f.name
        self.assertTrue(raw.exists())
        self.assertEqual(raw.read_text(encoding="utf-8"), self.body)
        md = (self.pdir / "sources" / f"{rec['id']}.md").read_text(encoding="utf-8")
        self.assertIn("вне проекта", md)
        self.assertIn(str(f.resolve()), md)

    def test_inside_raw_file_no_note_no_copy(self):
        d = self.pdir / "sources" / "raw"
        d.mkdir(parents=True, exist_ok=True)
        f = d / "note.md"
        f.write_text(self.body, encoding="utf-8")
        rec, created = sources.add(self.pdir, text=self.body, title="Заметка", text_path=f)
        self.assertTrue(created)
        self.assertNotIn("external_path", rec)
        self.assertEqual(rec["path"], "sources/raw/note.md")
        self.assertEqual(sorted(p.name for p in d.iterdir()), ["note.md"])  # копия не плодится

    def test_inside_project_other_folder_copied_without_note(self):
        d = self.pdir / "analysis"
        d.mkdir(parents=True, exist_ok=True)
        f = d / "конспект.md"
        f.write_text(self.body, encoding="utf-8")
        rec, _ = sources.add(self.pdir, text=self.body, title="Конспект", text_path=f)
        self.assertNotIn("external_path", rec)
        self.assertTrue((self.pdir / "sources" / "raw" / "конспект.md").exists())

    def test_cli_add_text_file_outside_marks_external(self):
        f = Path(TMP) / f"cli_out_{id(self)}.md"
        f.write_text(self.body, encoding="utf-8")
        r = subprocess.run([sys.executable, "-m", "tools.pfs", "--project", self.pdir.name,
                            "source", "add", "--text-file", str(f), "--title", "CLI-выписка"],
                           capture_output=True, text=True, cwd=REPO, env=os.environ.copy(), timeout=120)
        self.assertEqual(r.returncode, 0, r.stderr)
        last = core.read_jsonl(self.pdir / "sources.jsonl")[-1]
        self.assertEqual(last["external_path"], str(f.resolve()))
        self.assertIn("вне проекта", r.stdout)


class HookGuardTests(unittest.TestCase):
    """pre_guard.py: deny записи в реестры с подсказкой pfs; ask для чтения вне репозитория."""

    def test_bash_sed_on_claims_denied_with_hint(self):
        cmd = "sed -i '' 's/\\[C003\\]/[C059]/g' projects/demo/claims.jsonl"
        out = run_hook("pre_guard.py", {"tool_name": "Bash", "tool_input": {"command": cmd}}).stdout
        decision = json.loads(out)["hookSpecificOutput"]
        self.assertEqual(decision["permissionDecision"], "deny")
        self.assertIn("claim retag", decision["permissionDecisionReason"])

    def test_bash_python_inline_on_sources_denied(self):
        cmd = "python3 -c \"import json; rows=json.load(open('projects/demo/sources.jsonl'))\""
        out = run_hook("pre_guard.py", {"tool_name": "Bash", "tool_input": {"command": cmd}}).stdout
        decision = json.loads(out)["hookSpecificOutput"]
        self.assertEqual(decision["permissionDecision"], "deny")
        self.assertIn("source", decision["permissionDecisionReason"])

    def test_bash_redirect_to_decisions_denied(self):
        cmd = "echo '{}' > projects/demo/decisions.jsonl"
        out = run_hook("pre_guard.py", {"tool_name": "Bash", "tool_input": {"command": cmd}}).stdout
        self.assertEqual(json.loads(out)["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_bash_other_writers_denied(self):
        for cmd in ("echo x | tee projects/demo/state.json",
                    "git checkout -- projects/demo/claims.jsonl",
                    "perl -i -pe 's/a/b/' projects/demo/sources.jsonl",
                    "mv projects/demo/decisions.jsonl /tmp/backup.jsonl"):
            out = run_hook("pre_guard.py", {"tool_name": "Bash", "tool_input": {"command": cmd}}).stdout
            decision = json.loads(out)["hookSpecificOutput"]
            self.assertEqual(decision["permissionDecision"], "deny", cmd)

    def test_bash_readonly_and_pfs_allowed(self):
        for cmd in ("grep -rn claims.jsonl tools/",
                    "cat projects/demo/state.json",
                    "python3 -m tools.pfs claim add 'Рынок' --kind hypothesis",
                    "grep -rn claims.jsonl tools/ 2>&1",
                    "python3 -m tools.pfs check --json > /tmp/check.json"):
            r = run_hook("pre_guard.py", {"tool_name": "Bash", "tool_input": {"command": cmd}})
            self.assertEqual(r.stdout, "", cmd)

    def test_bash_redirect_with_registry_in_segment_denied(self):
        # перенаправление в сегменте с реестром блокируется консервативно:
        # cat … > копию ничем не лучше echo … > реестр для наивного парсера
        out = run_hook("pre_guard.py", {"tool_name": "Bash",
                                        "tool_input": {"command": "cat projects/demo/claims.jsonl > /tmp/copy.jsonl"}}).stdout
        self.assertEqual(json.loads(out)["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_edit_and_write_registry_denied(self):
        for tool in ("Edit", "Write", "MultiEdit"):
            out = run_hook("pre_guard.py", {"tool_name": tool,
                                            "tool_input": {"file_path": "projects/demo/state.json"}}).stdout
            decision = json.loads(out)["hookSpecificOutput"]
            self.assertEqual(decision["permissionDecision"], "deny", tool)
            self.assertIn("pfs step", decision["permissionDecisionReason"])

    def test_edit_regular_file_allowed(self):
        for tool, path in (("Edit", "projects/demo/outputs/04_product_strategy.md"),
                           ("Write", "tools/pfs/new_module.py"),
                           ("MultiEdit", "README.md")):
            r = run_hook("pre_guard.py", {"tool_name": tool, "tool_input": {"file_path": path}})
            self.assertEqual(r.stdout, "", path)

    def test_read_outside_repo_asks(self):
        out = run_hook("pre_guard.py", {"tool_name": "Read",
                                        "tool_input": {"file_path": "~/Projects/другой-проект/README.md"}}).stdout
        decision = json.loads(out)["hookSpecificOutput"]
        self.assertEqual(decision["permissionDecision"], "ask")
        self.assertIn("репозитори", decision["permissionDecisionReason"])

    def test_read_inside_repo_silent(self):
        for p in ("tools/pfs/cli.py", str(REPO / "AGENTS.md")):
            r = run_hook("pre_guard.py", {"tool_name": "Read", "tool_input": {"file_path": p}})
            self.assertEqual(r.stdout, "", p)

    def test_hooks_py39_compatible(self):
        """Хуки запускаются интерпретатором среды (бывает 3.9): PEP 604-аннотации
        (`str | None`) вычисляются при определении функции и падают с TypeError
        до guard() — пустой stdout ломает парсинг решения. Файл с такими
        аннотациями обязан иметь `from __future__ import annotations` (паттерн
        tools/pfs). Кроме того: пустых решений не бывает — хук либо молчит,
        либо отвечает валидным JSON."""
        hook_dir = REPO / ".claude" / "hooks"
        for hook in sorted(hook_dir.glob("*.py")):
            src = hook.read_text(encoding="utf-8")
            if re.search(r"(?::|->)\s*\w+(?:\[[^\]]*\])?\s*\|\s*None", src):
                self.assertIn("from __future__ import annotations", src,
                              f"{hook.name}: PEP 604 аннотации без future-import падают на Python 3.9")

    def test_hook_never_empty_stdout_on_decision(self):
        """Хук с решением отвечает валидным JSON, а не пустой строкой
        (регрессия: TypeError на Python 3.9 до guard() → пустой stdout)."""
        cases = [("Bash", {"command": "sed -i x projects/demo/claims.jsonl"}),
                 ("Edit", {"file_path": "projects/demo/state.json"}),
                 ("Read", {"file_path": "~/Projects/other/README.md"})]
        for tool, inp in cases:
            r = run_hook("pre_guard.py", {"tool_name": tool, "tool_input": inp})
            self.assertEqual(r.stderr, "", tool)  # TypeError до guard() виден в stderr
            decision = json.loads(r.stdout)  # пустой stdout → JSONDecodeError
            self.assertIn("permissionDecision", decision["hookSpecificOutput"])


class JournalTests(unittest.TestCase):
    """post_tool.py: ручная правка outputs через Bash фиксируется в журнале проекта."""

    def setUp(self):
        self.pdir = fresh(f"jrnl{id(self)}")
        (self.pdir / "outputs").mkdir(parents=True, exist_ok=True)
        (self.pdir / "outputs" / "04_product_strategy.md").write_text("текст\n", encoding="utf-8")

    def _log_len(self):
        return len(core.read_jsonl(self.pdir / "log.jsonl"))

    def test_bash_edit_of_outputs_is_journaled(self):
        doc = str(self.pdir / "outputs" / "04_product_strategy.md")
        before = self._log_len()
        run_hook("post_tool.py", {"tool_name": "Bash", "tool_input": {"command": f"sed -i '' 's/а/б/g' '{doc}'"}})
        rows = core.read_jsonl(self.pdir / "log.jsonl")
        self.assertEqual(len(rows), before + 1)
        self.assertIn("ручная правка outputs", rows[-1]["msg"])
        self.assertIn("sed -i", rows[-1]["msg"])

    def test_bash_read_of_outputs_not_journaled(self):
        doc = str(self.pdir / "outputs" / "04_product_strategy.md")
        before = self._log_len()
        run_hook("post_tool.py", {"tool_name": "Bash", "tool_input": {"command": f"cat '{doc}'"}})
        self.assertEqual(self._log_len(), before)


if __name__ == "__main__":
    unittest.main()
