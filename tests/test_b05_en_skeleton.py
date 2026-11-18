#!/usr/bin/env python3
"""QA B-05: EN-каркас six-pager без кириллицы — note и тарифы calcs.json не протекают."""

import os
import tempfile
import unittest
import re

TMP = tempfile.mkdtemp(prefix="pfs-test-b05-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from pathlib import Path  # noqa: E402

from tools.pfs import core, export, project  # noqa: E402

CYR = re.compile(r"[а-яА-ЯёЁ]")


class EnSkeletonNoCyrillicTests(unittest.TestCase):
    def test_en_skeleton_econ_block_no_cyrillic(self):
        """EN-скелет: RU-note и имена тарифов из calcs.json → EN-плейсхолдеры (BUG B-05)."""
        pdir = project.create("B05 en skeleton", "Growth stalled question", slug="b05-en", lang="en")
        core.atomic_write(pdir / "calcs.json", __import__("json").dumps({
            "unit_econ": {
                "note": "Модельные допущения из брифа: ARPU 29, churn 4% в месяц",
                "arpu": 29, "vc_share": 0.25, "cac": 450, "churn_month": 0.04,
                "tiers": [{"name": "Тариф «Защита близких»", "price": 29, "share": 1.0}],
            }}, ensure_ascii=False))
        out = export.build_six_pager(pdir, with_calcs=False, lang="en")
        text = out.read_text(encoding="utf-8")
        self.assertIn("Unit economics — step-by-step:", text,
                      "блок экономики должен попасть в скелет")
        self.assertFalse(CYR.search(text),
                         "кириллица в EN-скелете: %s" % CYR.search(text).group(0) if CYR.search(text) else "")
        self.assertIn("[describe assumptions]", text)

    def test_ru_skeleton_keeps_note(self):
        """RU-скелет не сломан: note из calcs.json дословно (обратная совместимость)."""
        pdir = project.create("B05 ru skeleton", "вопрос про рост", slug="b05-ru")
        core.atomic_write(pdir / "calcs.json", __import__("json").dumps({
            "unit_econ": {
                "note": "Модельные допущения из брифа: ARPU 29, churn 4%",
                "arpu": 29, "vc_share": 0.25, "cac": 450, "churn_month": 0.04,
            }}, ensure_ascii=False))
        out = export.build_six_pager(pdir, with_calcs=False, lang="ru")
        text = out.read_text(encoding="utf-8")
        self.assertIn("Допущения: Модельные допущения из брифа", text)


if __name__ == "__main__":
    unittest.main()
