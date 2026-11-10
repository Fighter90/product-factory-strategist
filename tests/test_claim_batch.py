"""pfs claim add-batch: массовая регистрация утверждений из JSONL (PRO-33).

Кейс сессии 2026-11-08: 21 утверждение регистрировалось 21 вызовом `pfs claim add`
подряд — медленно и шумно в log.jsonl. Здесь: батч из 21 строки регистрируется одним
вызовом; дубликат по тексту пропускается; невалидная строка отменяет весь батч
(атомарность — в реестре ничего не появляется); в журнал пишется одна запись на батч;
pfs check после батча не добавляет новых ошибок.

Запуск: python3 -m unittest tests.test_claim_batch -v
"""
import contextlib
import json
import os
import tempfile
import unittest
from io import StringIO
from pathlib import Path

TMP = tempfile.mkdtemp(prefix="pfs-test-batch-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from tools.pfs import check, claims, cli, core, project, sources  # noqa: E402
from tools.pfs.core import PfsError  # noqa: E402


def write_batch(name: str, items: list[dict]) -> Path:
    path = Path(TMP) / name
    path.write_text("".join(json.dumps(it, ensure_ascii=False) + "\n" for it in items), encoding="utf-8")
    return path


def run_cli(argv):
    out, err = StringIO(), StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = cli.main(argv)
    return rc, out.getvalue(), err.getvalue()


class BatchTests(unittest.TestCase):
    def setUp(self):
        self.pdir = project.create(f"Батч {id(self)}", "Почему падает удержание подписчиков?",
                                   slug=f"batch{id(self)}")
        sources.add(self.pdir, text="Отчёт о рынке: отток подписчиков 12% в месяц. " * 5, title="Отчёт")

    def test_batch_of_21_in_one_call(self):
        """21 утверждение — одним вызовом; IDs уникальны; одна запись в журнале, а не 21."""
        items = [ {"text": f"Утверждение про удержание №{i}", "kind": "fact", "source": "S001", "grade": "B"}
                  for i in range(1, 22) ]
        res = claims.add_batch(self.pdir, write_batch("batch21.jsonl", items))
        self.assertEqual(res["created"], [f"C{i:03d}" for i in range(1, 22)])
        self.assertEqual(res["skipped"], 0)
        rows = claims.load(self.pdir)
        self.assertEqual(len(rows), 21)
        self.assertEqual(len({r["id"] for r in rows}), 21)
        self.assertEqual({r["kind"] for r in rows}, {"fact"})
        self.assertEqual({r["grade"] for r in rows}, {"B"})
        log_entries = [r for r in core.read_jsonl(self.pdir / "log.jsonl") if r["kind"] == "claim"]
        self.assertEqual(len(log_entries), 1, "батч должен писать одну запись в журнал, а не по записи на утверждение")

    def test_duplicates_skipped(self):
        """Дубликат по тексту (в реестре и внутри самого батча) пропускается, новое — создаётся."""
        claims.add(self.pdir, "Уже зарегистрировано", "fact", ["S001"])
        items = [
            {"text": "Уже зарегистрировано", "kind": "fact", "source": "S001"},
            {"text": "Новое утверждение", "kind": "fact", "source": "S001", "grade": "A"},
            {"text": "Новое утверждение", "kind": "fact", "source": "S001"},  # дубль внутри батча
            {"text": "Ещё одно новое", "kind": "hypothesis", "source": "S001"},
        ]
        res = claims.add_batch(self.pdir, write_batch("dup.jsonl", items))
        self.assertEqual(res["created"], ["C002", "C003"])
        self.assertEqual(res["skipped"], 2)
        texts = [r["text"] for r in claims.load(self.pdir)]
        self.assertEqual(texts.count("Новое утверждение"), 1)

    def test_invalid_line_aborts_whole_batch(self):
        """Невалидная строка — PfsError с номером строки, в реестре ничего не появляется."""
        items = [
            {"text": "Валидное утверждение", "kind": "fact", "source": "S001", "grade": "B"},
            {"text": "Ещё валидное", "kind": "hypothesis", "source": "S001"},
            {"text": "Невалидное: нет такого типа", "kind": "guess"},
        ]
        before = claims.load(self.pdir)
        with self.assertRaises(PfsError) as ctx:
            claims.add_batch(self.pdir, write_batch("bad.jsonl", items))
        self.assertIn("Строка 3", str(ctx.exception))
        self.assertEqual(claims.load(self.pdir), before, "невалидный батч не должен ничего записать")
        self.assertEqual([r for r in core.read_jsonl(self.pdir / "log.jsonl") if r["kind"] == "claim"], [])

    def test_invalid_fact_without_source_aborts(self):
        """Правила реестра действуют и в батче: факт без источника отменяет весь батч."""
        items = [
            {"text": "Гипотеза без оснований", "kind": "hypothesis"},
            {"text": "Факт без источника", "kind": "fact"},
        ]
        before = claims.load(self.pdir)
        with self.assertRaises(PfsError) as ctx:
            claims.add_batch(self.pdir, write_batch("nosrc.jsonl", items))
        self.assertIn("Строка 2", str(ctx.exception))
        self.assertEqual(claims.load(self.pdir), before)

    def test_quote_from_note_fields(self):
        """Остальные поля строки (quote/from/confidence/note/tags) попадают в запись."""
        base = claims.add(self.pdir, "Основание", "fact", ["S001"])
        items = [{"text": "Вывод из основания", "kind": "inference", "from": base["id"],
                  "quote": "рынок 40 млрд", "confidence": "high", "note": "из выписки S001",
                  "tags": "рынок, объём"}]
        res = claims.add_batch(self.pdir, write_batch("fields.jsonl", items))
        rec = claims.get(self.pdir, res["created"][0])
        self.assertEqual(rec["derived_from"], [base["id"]])
        self.assertEqual(rec["quote"], "рынок 40 млрд")
        self.assertEqual(rec["confidence"], "high")
        self.assertEqual(rec["note"], "из выписки S001")
        self.assertEqual(rec["tags"], ["рынок", "объём"])

    def test_check_no_new_errors_after_batch(self):
        """Критерий приёмки: pfs check после батча — без новых ошибок."""
        items = [
            {"text": "Факт из отчёта", "kind": "fact", "source": "S001", "grade": "B"},
            {"text": "Гипотеза из отчёта", "kind": "hypothesis", "source": "S001"},
        ]
        errors_before = check.run(self.pdir)["errors"]
        claims.add_batch(self.pdir, write_batch("chk.jsonl", items))
        self.assertEqual(check.run(self.pdir)["errors"], errors_before)

    def test_missing_file(self):
        with self.assertRaises(PfsError):
            claims.add_batch(self.pdir, Path(TMP) / "no-such-file.jsonl")


class BatchCliTests(unittest.TestCase):
    def setUp(self):
        self.pdir = project.create(f"Батч CLI {id(self)}", "Почему падает удержание?",
                                   slug=f"batchcli{id(self)}")
        sources.add(self.pdir, text="Отчёт о рынке: отток подписчиков 12% в месяц. " * 5, title="Отчёт")

    def test_cli_add_batch(self):
        """pfs claim add-batch claims.jsonl: код 0, сводка в stdout, утверждения в реестре."""
        path = write_batch(f"cli_{id(self)}.jsonl",
                           [{"text": f"CLI утверждение №{i}", "kind": "fact", "source": "S001", "grade": "C"}
                            for i in range(1, 4)])
        rc, out, err = run_cli(["--project", self.pdir.name, "claim", "add-batch", str(path)])
        self.assertEqual(rc, 0, err)
        self.assertIn("создано 3", out)
        self.assertIn("дубликаты пропущены 0", out)
        self.assertEqual(len(claims.load(self.pdir)), 3)

    def test_cli_relative_path_resolved_from_project_dir(self):
        """Относительный путь резолвится от каталога проекта (как у source add, PRO-36)."""
        (self.pdir / "claims_batch.jsonl").write_text(
            json.dumps({"text": "Из файла в проекте", "kind": "hypothesis", "source": "S001"},
                       ensure_ascii=False) + "\n", encoding="utf-8")
        rc, out, err = run_cli(["--project", self.pdir.name, "claim", "add-batch", "claims_batch.jsonl"])
        self.assertEqual(rc, 0, err)
        self.assertIn("создано 1", out)

    def test_cli_invalid_batch_exit_code(self):
        path = write_batch(f"bad_{id(self)}.jsonl", [{"text": "x", "kind": "guess"}])
        rc, out, err = run_cli(["--project", self.pdir.name, "claim", "add-batch", str(path)])
        self.assertEqual(rc, 2)
        self.assertIn("Строка 1", err)


if __name__ == "__main__":
    unittest.main()
