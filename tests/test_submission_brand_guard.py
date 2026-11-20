"""PRO-128: REGRESS-FINAL — охрана контрольных точек финального регресса подачи.

Требование кейса: бренды в материалах подачи запрещены. Демо подачи — «Связь
для близких и собственных устройств» (учебный рынок мобильного оператора);
прежнее демо с брендом заказчика (CVStart) из README/README_EN/SUBMISSION убрано.

Закреплённые контрольные точки (issue PRO-128):
1. README.md, README_EN.md, docs/SUBMISSION.md — упоминаний бренда CVStart
   и брендов конкурентов резюме-рынка нет (grep = 0).
2. README и README_EN — демо-разделы про одно и то же демо: видео
   svyaz-overview-RU.mp4 / svyaz-overview-EN.mp4 и карта пакета DEMO_README.md.
3. Относительные ссылки в README/README_EN/SUBMISSION живы (цели существуют).
4. Демо-проект в коммите завершён: все 12 шагов done/skipped, D001 accepted.
5. Обзорные видео RU/EN закоммичены и длятся ≤ 10 минут (ffprobe, если есть).
6. BRIEF_RESPONSE: 5 частей; каждая строка с числами несёт тег источника
   ([C###]/[S###] или указатель раздела [NN]) — «все числа с тегами».

Запуск: python3 -m unittest tests.test_submission_brand_guard -v
"""
import json
import re
import shutil
import subprocess
import time
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DEMO = REPO / "projects" / "связь-для-близких-и-собственных-устройств"

# Документы подачи: бренды запрещены требованием кейса
SUBMISSION_DOCS = [REPO / "README.md", REPO / "README_EN.md", REPO / "docs" / "SUBMISSION.md"]

# Запрещённые бренды прежнего демо (регистронезависимо; короткие токены — по границе слова)
FORBIDDEN_BRANDS = [
    "cvstart", "career-ops", "cv_landing",
    "Zety", "Novoresume", "Kickresume", "Enhancv", "Rezi", "resume.io",
]

# Демо подачи: маркеры, обязанные быть в README RU и EN одновременно
DEMO_MARKERS_RU = ["projects/связь-для-близких-и-собственных-устройств", "DEMO_README.md"]
DEMO_MARKERS_EN = DEMO_MARKERS_RU  # одни и те же ссылки на карту пакета в обеих версиях README

# Тег источника/раздела: [C003], [S001,C009], [03,C], [06] — но не [15] ударов red team
_TAG = re.compile(r"\[(?=[^\]]*(?:[CS]\d{3}))([^\]]*)\]")

def _brand_hits(text: str) -> list[str]:
    hits = []
    low = text.lower()
    for brand in FORBIDDEN_BRANDS:
        if len(brand) <= 5:
            if re.search(r"\b" + re.escape(brand.lower()), low):
                hits.append(brand)
        elif brand.lower() in low:
            hits.append(brand)
    return hits


class SubmissionBrandGuardTests(unittest.TestCase):
    """Бренды в материалах подачи запрещены (PRO-128)."""

    def test_no_forbidden_brands_in_submission_docs(self):
        offenders = []
        for doc in SUBMISSION_DOCS:
            hits = _brand_hits(doc.read_text(encoding="utf-8"))
            if hits:
                offenders.append(f"{doc.name}: {', '.join(sorted(set(hits)))}")
        self.assertEqual(offenders, [],
                         "бренды в материалах подачи запрещены: " + "; ".join(offenders))

    def test_readme_demo_sections_are_about_the_svyaz_demo(self):
        for name, markers in (("README.md", DEMO_MARKERS_RU), ("README_EN.md", DEMO_MARKERS_EN)):
            text = (REPO / name).read_text(encoding="utf-8")
            missing = [m for m in markers if m not in text]
            self.assertEqual(missing, [],
                             f"{name}: демо-раздел должен вести на демо «Связь для близких», нет: {missing}")
            self.assertIn("DEMO_README.md", text, f"{name}: нет ссылки на карту пакета демо")


class SubmissionLinksAliveTests(unittest.TestCase):
    """Относительные ссылки материалов подачи живы (PRO-128)."""

    def test_relative_markdown_links_resolve(self):
        dead = []
        for doc in SUBMISSION_DOCS:
            base = doc.parent
            for m in re.finditer(r"\[[^\]]*\]\(([^)]+)\)", doc.read_text(encoding="utf-8")):
                target = m.group(1).split("#")[0].split("?")[0].strip()
                if not target or target.startswith(("http://", "https://", "mailto:")):
                    continue
                if not (base / target).exists():
                    dead.append(f"{doc.name} -> {target}")
        self.assertEqual(dead, [], "битые относительные ссылки: " + "; ".join(dead))


class DemoProjectFinishedTests(unittest.TestCase):
    """Демо-проект в коммите завершён: 12/12 шагов, D001 accepted (PRO-128)."""

    def test_demo_state_all_12_steps_done(self):
        from tools.pfs.core import STAGE_IDS
        state = json.loads((DEMO / "state.json").read_text(encoding="utf-8"))
        steps = state.get("steps", {})
        not_done = [sid for sid in STAGE_IDS
                    if steps.get(sid, {}).get("status") not in ("done", "skipped")]
        self.assertEqual(not_done, [],
                         f"демо не 12/12, не завершены шаги: {', '.join(not_done)}")

    def test_demo_decision_d001_accepted(self):
        rows = [json.loads(line) for line in
                (DEMO / "decisions.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
        d001 = [r for r in rows if r.get("id") == "D001"]
        self.assertTrue(d001, "нет D001 в decisions.jsonl демо")
        self.assertEqual(d001[-1].get("status"), "accepted", "D001 не в статусе accepted")


class DemoVideoTests(unittest.TestCase):
    """Обзорные видео RU/EN закоммичены и ≤ 10 минут (PRO-128)."""

    VIDEOS = ["video/svyaz-overview-RU.mp4", "video/svyaz-overview-EN.mp4"]

    def test_overview_videos_exist(self):
        missing = [v for v in self.VIDEOS if not (REPO / v).is_file()]
        self.assertEqual(missing, [], f"нет обзорных видео: {', '.join(missing)}")

    def test_overview_videos_are_tracked(self):
        if shutil.which("git") is None:
            self.skipTest("git недоступен")
        tracked = subprocess.run(["git", "ls-files", *self.VIDEOS], cwd=REPO,
                                 capture_output=True, text=True).stdout.split()
        missing = [v for v in self.VIDEOS if v not in tracked]
        self.assertEqual(missing, [],
                         f"видео не закоммичены (не попадут в свежий клон): {', '.join(missing)}")

    def test_overview_videos_max_10_minutes(self):
        if shutil.which("ffprobe") is None:
            self.skipTest("ffprobe недоступен")
        for v in self.VIDEOS:
            duration = None
            # 3 попытки: файл могут перегенерировать параллельно (mp4 без moov-атома на середине записи)
            for _ in range(3):
                out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                      "-of", "default=noprint_wrappers=1:nokey=1", str(REPO / v)],
                                     capture_output=True, text=True)
                m = re.search(r"(?:duration=)?(\d+(?:\.\d+)?)", out.stdout.strip())
                if m:
                    duration = float(m.group(1))
                    break
                time.sleep(5)
            self.assertIsNotNone(duration, f"{v}: ffprobe не смог прочитать длительность")
            self.assertLessEqual(duration, 600, f"{v}: {duration:.0f} c — длиннее 10 минут")


class BriefResponseGuardTests(unittest.TestCase):
    """BRIEF_RESPONSE: 5 частей, все числа с тегами (PRO-128)."""

    DOC = DEMO / "outputs" / "BRIEF_RESPONSE.md"

    def test_five_parts(self):
        parts = re.findall(r"^## Часть \d", self.DOC.read_text(encoding="utf-8"), flags=re.M)
        self.assertEqual(len(parts), 5, f"частей {len(parts)}, требуется 5")

    def test_every_number_line_is_tagged(self):
        untagged = []
        for i, line in enumerate(self.DOC.read_text(encoding="utf-8").splitlines(), 1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue  # заголовки: «Часть N» — структура, не утверждение
            if re.search(r"(?<![\w./#-])\d+", line) and not _TAG.search(line):
                untagged.append(f"строка {i}: {stripped[:90]}")
        self.assertEqual(untagged, [],
                         "числа без тега источника в BRIEF_RESPONSE:\n" + "\n".join(untagged))


if __name__ == "__main__":
    unittest.main()
