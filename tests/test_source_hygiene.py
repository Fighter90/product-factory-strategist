#!/usr/bin/env python3
"""QA B-01/B-02/B-04: гигиена источников — weak_content, пустая выписка,
указатели media/interview, refresh text-источника, max-ID при сбоях счётчика."""

import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout

TMP = tempfile.mkdtemp(prefix="pfs-test-src-hyg-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from pathlib import Path  # noqa: E402

from tools.pfs import cli, core, project, sources  # noqa: E402
from tools.pfs.core import PfsError  # noqa: E402


def run_cli(argv):
    buf = io.StringIO()
    args = cli.build_parser().parse_args(argv)
    with redirect_stdout(buf):
        args.f(args)
    return buf.getvalue()


class WeakContentTests(unittest.TestCase):
    def test_nav_shell_detected(self):
        menu = "\n".join(["Главная", "О компании", "Услуги", "Контакты", "Вход",
                          "Регистрация", "Подробнее", "Читать далее", "Меню",
                          "Все новости", "Ещё раздел", "И ещё раздел"] + ["—"] * 6)
        self.assertTrue(sources.weak_content(menu))
        self.assertFalse(sources.weak_content("Обычная статья с длинным осмысленным " * 10))
        self.assertFalse(sources.weak_content("короткий текст"))

    def test_empty_excerpt_warns(self):
        pdir = project.create("Src hygiene", "вопрос", slug="sh-empty")
        core.set_active(pdir.name)
        f = Path(TMP) / "empty.md"
        f.write_text("коротко", encoding="utf-8")
        out = run_cli(["source", "add", str(f), "--origin", "excerpt"])
        self.assertIn("почти пуст", out)


class MediaInterviewPointerTests(unittest.TestCase):
    def test_fetch_media_flag_points_to_media_add(self):
        pdir = project.create("Media ptr", "q", slug="sh-media")
        core.set_active(pdir.name)
        with self.assertRaises(PfsError) as cm:
            run_cli(["source", "fetch", "https://example.com/video", "--media"])
        self.assertIn("pfs media add", str(cm.exception))

    def test_fetch_interview_flag_points_to_interview_save(self):
        pdir = project.create("Interview ptr", "q", slug="sh-int")
        core.set_active(pdir.name)
        with self.assertRaises(PfsError) as cm:
            run_cli(["source", "fetch", "https://example.com/talk", "--interview"])
        self.assertIn("pfs interview save", str(cm.exception))


class RefreshTextTests(unittest.TestCase):
    def test_refresh_text_source_rereads_file(self):
        """BUG B-04: text-источник с path перечитывается refresh'ем, а не «обновите вручную»."""
        pdir = project.create("Refresh text", "q", slug="sh-ref")
        core.set_active(pdir.name)
        f = Path(TMP) / "digest.md"
        f.write_text("# Страница\n\nСтарое содержимое: конверсия 2%.\n", encoding="utf-8")
        run_cli(["source", "add", str(f)])
        f.write_text("# Страница\n\nНовое содержимое: конверсия 3,5% и рынок 13,195 млн.\n", encoding="utf-8")
        out = run_cli(["source", "refresh", "S001"])
        self.assertNotIn("не перезагружается", out)
        body = (pdir / "sources" / "S001.md").read_text(encoding="utf-8")
        self.assertIn("конверсия 3,5%", body)

    def test_source_update_edits_title(self):
        """BUG B-04: правка метаданных без ручного редактирования jsonl."""
        pdir = project.create("Src update", "q", slug="sh-upd")
        core.set_active(pdir.name)
        f = Path(TMP) / "three.md"
        f.write_text("материал три с достаточным объёмом текста для источника\n" * 3, encoding="utf-8")
        run_cli(["source", "add", str(f)])
        run_cli(["source", "update", "S001", "--title", "Новое название источника"])
        rec = sources.get(pdir, "S001")
        self.assertEqual(rec["title"], "Новое название источника")


class RegistrySanityTests(unittest.TestCase):
    def test_free_id_takes_max_existing(self):
        """BUG B-03: даже при дырах/ручных правках счётчик берёт max(S###)+1."""
        pdir = project.create("Registry ids", "q", slug="sh-ids")
        f = Path(TMP) / "one.md"
        f.write_text("материал один с достаточным объёмом текста для источника\n" * 3, encoding="utf-8")
        for _ in range(3):
            run_cli(["source", "add", str(f)])
        # имитируем «сброс счётчика»: в реестре появляется источник с большим ID
        rows = sources.load(pdir)
        extra = dict(rows[-1], id="S042", sha256="manual" + "0" * 56, url=None)
        with open(pdir / "sources.jsonl", "a", encoding="utf-8") as fh:
            fh.write(json.dumps(extra, ensure_ascii=False) + "\n")
        nxt = sources.free_id(pdir, sources.load(pdir))
        self.assertEqual(nxt, "S043")

    def test_doctor_reports_registry_gaps(self):
        """Валидатор реестра: дыры и битые ссылки видны в doctor/check."""
        pdir = project.create("Registry gaps", "q", slug="sh-gap")
        f = Path(TMP) / "two.md"
        f.write_text("материал два с достаточным объёмом текста для источника\n" * 3, encoding="utf-8")
        run_cli(["source", "add", str(f)])
        (pdir / "sources" / "S001.md").unlink()  # битая ссылка файл ↔ реестр
        problems = sources.audit(pdir)
        self.assertTrue(any("S001" in p and "нет файла" in p for p in problems),
                         str(problems))


class WeakContentV2Tests(unittest.TestCase):
    """Вечерний аудит B-01/B-04: меню без предложений, «мало текста», update --text-file."""

    def test_menu_without_sentences_is_weak(self):
        menu = "\n".join(["Электронный документооборот", "Учет и отчетность", "Проверка контрагентов",
                          "Тарифы и услуги", "Контакты", "О компании", "Новости", "Поддержка"]
                         + ["Раздел %d" % i for i in range(8)])
        self.assertTrue(sources.weak_content(menu))

    def test_low_sentence_text_is_weak(self):
        body = " - пункт " + "\n - пункт ".join(str(i) for i in range(20))
        self.assertTrue(sources.weak_content(body))

    def test_real_article_not_weak(self):
        article = ("Обзор рынка труда. Зарплаты выросли на 12%. ATS-фильтры отсекают большинство откликов. "
                   "Компании внедряют автоматический скрининг. Кандидаты ищут обходные пути. ") * 10
        self.assertFalse(sources.weak_content(article))

    def test_check_warns_weak_content(self):
        pdir = project.create("Weak check", "q", slug="sh-wcheck2")
        sources.add(pdir, text="короткий пункт без предложений " * 30, title="thin")
        rows = sources.load(pdir)
        rows[0]["weak_content"] = True
        core.write_jsonl(pdir / "sources.jsonl", rows)
        from tools.pfs import check as _c
        res = _c.run(pdir)
        self.assertTrue(any("мало содержательного" in w for w in res["warnings"]), res["warnings"][:3])

    def test_update_replaces_text(self):
        pdir = project.create("Upd text v2", "q", slug="sh-uptext2")
        core.set_active(pdir.name)
        f1 = Path(TMP) / "u1.md"; f1.write_text("первая версия текста источника\n" * 3, encoding="utf-8")
        run_cli(["source", "add", str(f1)])
        f2 = Path(TMP) / "u2.md"; f2.write_text("вторая версия: рынок 13,195 млн и конверсия 3,5%\n" * 3, encoding="utf-8")
        out = run_cli(["source", "update", "S001", "--text-file", str(f2)])
        self.assertIn("обновлено", out)
        body = (pdir / "sources" / "S001.md").read_text(encoding="utf-8")
        self.assertIn("13,195 млн", body)
        self.assertTrue(list((pdir / "sources" / "raw").glob("S001_old_*.txt")), "нет бэкапа")


if __name__ == "__main__":
    unittest.main()
