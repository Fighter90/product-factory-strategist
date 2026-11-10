"""Атомарный pfs source add: lock вокруг выделения ID, retry при коллизии, аудит реестра (PRO-34).

Кейс S020: два параллельных вызова source add получили один ID — Eurostat был перезаписан
XING, реестр чинили вручную. Здесь: 10 параллельных процессов дают 10 уникальных ID;
занятый файл не переиспользуется (retry с новым ID); pfs doctor находит дубли ID/URL,
потерянные файлы и файлы-сироты.

Запуск: python3 -m unittest tests.test_source_atomic -v
"""
import argparse
import contextlib
import io
import os
import re
import subprocess
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parents[1]
TMP = tempfile.mkdtemp(prefix="pfs-test-atomic-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from tools.pfs import cli, core, project, sources  # noqa: E402


class AtomicAddTests(unittest.TestCase):
    """Выделение S### при параллельных записях (межпроцессная гонка — кейс S020)."""

    def setUp(self):
        self.pdir = project.create(f"Атомарность {id(self)}", "Почему падает удержание?",
                                   slug=f"atomic{id(self)}")

    def test_parallel_cli_adds_unique_ids(self):
        """10 параллельных процессов `pfs source add` → 10 уникальных ID, реестр и файлы согласованы."""
        files = []
        for i in range(10):
            f = Path(TMP) / f"report_{id(self)}_{i}.md"
            f.write_text(f"Уникальный отчёт №{i} про рынок и удержание подписчиков. " * 5, encoding="utf-8")
            files.append(f)

        def run(f):
            return subprocess.run(
                [sys.executable, "-m", "tools.pfs", "--project", self.pdir.name,
                 "source", "add", "--text-file", str(f), "--title", f.stem],
                capture_output=True, text=True, cwd=REPO, env=os.environ.copy(), timeout=120)

        with ThreadPoolExecutor(max_workers=10) as ex:
            results = list(ex.map(run, files))
        ids = []
        for f, r in zip(files, results):
            self.assertEqual(r.returncode, 0, f"{f.name}: stderr={r.stderr}")
            m = re.search(r"(?:Добавлен|Уже есть): (S\d+)", r.stdout)
            self.assertIsNotNone(m, f"{f.name}: нет ID в выводе: {r.stdout!r}")
            ids.append(m.group(1))
        self.assertEqual(len(set(ids)), 10, f"гонка выдала дубль ID: {sorted(ids)}")
        rows = core.read_jsonl(self.pdir / "sources.jsonl")
        self.assertEqual(len(rows), 10)
        self.assertEqual(len({r["id"] for r in rows}), 10)
        for r in rows:  # биекция: у каждой записи есть свой файл, ни один не перезаписан чужим
            self.assertTrue((self.pdir / "sources" / f"{r['id']}.md").exists())

    def test_orphan_file_retry_new_id(self):
        """Файл S001.md занят, записи в реестре нет (осиротевший файл прошлой гонки):
        новый источник не переиспользует S001 — retry со следующим свободным ID."""
        orphan = self.pdir / "sources" / "S001.md"
        orphan_text = "# S001. Файл прошлой гонки без записи в реестре"
        orphan.write_text(orphan_text, encoding="utf-8")
        rec, created = sources.add(self.pdir, text="Свежий отчёт про удержание подписчиков. " * 10,
                                   title="fresh")
        self.assertTrue(created)
        self.assertEqual(rec["id"], "S002", "ID S001 занят файлом — должен быть взят следующий")
        self.assertTrue((self.pdir / "sources" / "S002.md").exists())
        self.assertEqual(orphan.read_text(encoding="utf-8"), orphan_text)  # чужой файл не перезаписан
        self.assertNotIn("fresh", (self.pdir / "sources" / "S001.md").read_text(encoding="utf-8"))

    def test_register_web_dedups_by_url_under_lock(self):
        """Тот же URL при другом тексте не создаёт второй источник (уникальность url перед записью)."""
        r1, created1 = sources.add(self.pdir, text="Первый отчёт про рынок Европы. " * 10,
                                   url="https://example.org/report", title="r1")
        self.assertTrue(created1)
        r2, created2 = sources._register_web(self.pdir, url="https://example.org/report", kind="text",
                                             body="Совершенно другой текст отчёта про Азию. " * 10, title="r2",
                                             origin="public", note=None, published=None)
        self.assertFalse(created2)
        self.assertEqual(r1["id"], r2["id"])
        self.assertEqual(len(core.read_jsonl(self.pdir / "sources.jsonl")), 1)


class DoctorAuditTests(unittest.TestCase):
    """pfs doctor: биекция sources.jsonl ↔ sources/*.md, дубли ID/URL."""

    def setUp(self):
        self.pdir = project.create(f"Аудит {id(self)}", "Что делать?", slug=f"audit{id(self)}")

    def test_clean_registry_passes(self):
        sources.add(self.pdir, text="Отчёт первый про рынок. " * 10, title="a")
        sources.add(self.pdir, text="Отчёт второй про конкуренцию. " * 10, title="b")
        self.assertEqual(sources.audit(self.pdir), [])

    def test_audit_finds_duplicate_ids_urls_and_lost_orphan_files(self):
        """Итог гонки из кейса S020: дубль ID в реестре, дубль URL, файл потерян, файл-сирота."""
        rec = sources.add(self.pdir, text="Отчёт про рынок. " * 10, title="a")[0]
        dup_id = dict(rec)  # та же строка реестра дважды — результат гонки двух процессов
        d1 = dict(rec, id="S101", sha256="a" * 64, url="https://eurostat.example/x")
        d2 = dict(rec, id="S102", sha256="b" * 64, url="https://eurostat.example/x")
        core.write_jsonl(self.pdir / "sources.jsonl", [rec, dup_id, d1, d2])
        (self.pdir / "sources" / "S999.md").write_text("# S999. Файл без записи в реестре", encoding="utf-8")
        text = "\n".join(sources.audit(self.pdir))
        self.assertIn("дубль ID", text)
        self.assertIn("дубль URL", text)
        self.assertIn("нет файла sources/S101.md", text)   # запись есть — файл потерян
        self.assertIn("S999", text)                        # файл-сирота без записи

    def test_doctor_reports_registry_problems(self):
        """`pfs doctor` печатает проблемы реестров источников всех проектов."""
        (self.pdir / "sources" / "S999.md").write_text("# S999. Сирота", encoding="utf-8")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            cli.cmd_doctor(argparse.Namespace())
        self.assertIn("S999", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
