"""PRO-66, раунд 3 ревью: три правки генератора лендинга.

1. Команда в терминальном фрагменте цепочки доказательств (#proof) берёт тип
   утверждения из реестра через {{CKIND}}: захардкоженное «--kind fact» при
   смене типа C011 противоречило бы карточке утверждения и строке результата.
2. Кнопки копирования: при отказе clipboard показывается состояние неудачи
   (data-fail и выделение команды для ручного копирования), а не «Скопировано».
3. Отдельная секция «Документ для комитета» (FAQ-1…6 и форматы) между
   #proof и #demo на RU- и EN-страницах — не только bento-карточка.
"""
from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_site.py"
CYR = re.compile(r"[\u0400-\u04FF]")


def load_module():
    """Импорт scripts/build_site.py как модуля без установки пакета."""
    spec = importlib.util.spec_from_file_location("build_site_r3", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class Round3Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = load_module()
        tmp = Path(tempfile.mkdtemp(prefix="pfs-site-r3-"))
        r = subprocess.run([sys.executable, str(SCRIPT), "--out", str(tmp)],
                           cwd=ROOT, capture_output=True, text=True)
        assert r.returncode == 0, f"build_site.py упал:\n{r.stdout}\n{r.stderr}"
        cls.built = {
            "ru": (tmp / "index.html").read_text(encoding="utf-8"),
            "en": (tmp / "en" / "index.html").read_text(encoding="utf-8"),
        }


class TestTerminalCommandKind(Round3Base):
    """Точка 1: команда pfs claim add в терминале согласована с реестром."""

    def test_no_hardcoded_kind_in_source(self):
        src = SCRIPT.read_text(encoding="utf-8")
        self.assertNotIn(
            "--kind fact", src,
            "тип утверждения в команде захардкожен — при смене типа C011 сайт "
            "покажет противоречие; подставляйте {{CKIND}} из claim_facts()")

    def test_command_takes_kind_from_registry(self):
        # тела — f-строки: {{{{CKIND}}}} в исходнике превращается в {{CKIND}}
        for name, body in (("RU", self.mod.RU_BODY), ("EN", self.mod.EN_BODY)):
            self.assertIn("--kind {{CKIND}}", body, name)
        self.assertEqual(SCRIPT.read_text(encoding="utf-8").count("--kind {{{{CKIND}}}}"), 2)

    def test_ckind_token_is_the_registry_kind(self):
        facts = self.mod.claim_facts()
        rows = []
        for line in (ROOT / "projects" / "демо" / "claims.jsonl").read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))
        kind = next(r["kind"] for r in rows if r.get("id") == "C011")
        self.assertEqual(facts["CKIND"], kind)
        self.assertIn(facts["CKIND"], self.built["ru"])

    def test_no_leftover_kind_tokens(self):
        for lang, page in self.built.items():
            self.assertNotIn("{{CKIND}}", page, lang)


class TestCopyFailureState(Round3Base):
    """Точка 2: неудачное копирование не рапортует об успехе."""

    def test_promise_rejection_goes_to_fail_state(self):
        js = self.mod.JS
        self.assertNotIn(".then(done,done)", js, "reject показывался как успех")
        self.assertIn(".then(ok,fail)", js)
        self.assertNotIn("catch(e){done()}", js, "исключение показывалось как успех")

    def test_fail_state_selects_the_command(self):
        self.assertIn("selectNodeContents", self.mod.JS,
                      "при неудаче команда выделяется, чтобы скопировать вручную")

    def test_every_button_has_a_fail_label(self):
        for name, body in (("RU_BODY", self.mod.RU_BODY), ("EN_BODY", self.mod.EN_BODY),
                           ("HELP_BODY_RU", self.mod.HELP_BODY_RU),
                           ("HELP_BODY_EN", self.mod.HELP_BODY_EN)):
            self.assertEqual(body.count("data-ok="), body.count("data-fail="), name)
        self.assertIn('data-fail="Не скопировалось"', self.mod.RU_BODY)
        self.assertIn('data-fail="Copy failed"', self.mod.EN_BODY)

    def test_built_pages_carry_fail_labels(self):
        self.assertIn("Не скопировалось", self.built["ru"])
        self.assertIn("Copy failed", self.built["en"])


class TestCommitteeSection(Round3Base):
    """Точка 3: секция «Документ для комитета» между #proof и #demo."""

    def _between(self, page: str) -> str:
        proof = page.index('id="proof"')
        demo = page.index('id="demo"')
        return page[proof:demo]

    def test_section_between_proof_and_demo(self):
        for lang, page in self.built.items():
            self.assertIn('id="sixpager"', page, f"{lang}: нет секции «Документ для комитета»")
            seg = self._between(page)
            self.assertIn('id="sixpager"', seg, f"{lang}: секция не между #proof и #demo")

    def test_six_answers_and_formats_listed(self):
        for lang, page in self.built.items():
            seg = self._between(page)
            for n in range(1, 7):
                self.assertIn(f"FAQ-{n}", seg, f"{lang}: FAQ-{n}")
            for fmt in ("MD", "PDF", "DOCX", "Excel"):
                self.assertIn(fmt, seg, f"{lang}: формат {fmt}")

    def test_en_section_is_english(self):
        seg = self._between(self.built["en"])
        self.assertEqual(CYR.findall(seg), [], "кириллица в EN-секции")

    def test_bento_card_no_longer_carries_the_full_list(self):
        for lang, page in self.built.items():
            self.assertNotIn('class="faqlist"', page,
                             f"{lang}: список FAQ-1…6 дублируется в bento-карточке")


if __name__ == "__main__":
    unittest.main()
