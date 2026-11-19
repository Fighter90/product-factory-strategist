"""Охрана скрипта сквозного прогона: клон обязан тестировать проверяемое состояние (PRO-128).

Дефект 2026-11-20: scripts/e2e_opencode.sh делает `git clone -q "$REPO"` — git
клонирует ветку по умолчанию (main), а не текущий HEAD репозитория. Финальный
регресс «после ВСЕХ доработок» тестировал устаревший код всякий раз, когда HEAD
уходил вперёд main (норма во время цикла «дефект → фикс-коммит → повторный
прогон»: исполнители коммитят на detached HEAD, main обновляет оркестратор).
Охрана: после клонирования скрипт ставит клон на коммит HEAD исходного репозитория.

Запуск: python3 -m unittest discover -s tests -v
"""
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "e2e_opencode.sh"


class E2eScriptClonePinnedToHeadTests(unittest.TestCase):
    def test_clone_is_pinned_to_repo_head(self):
        text = SCRIPT.read_text(encoding="utf-8")
        m = re.search(r'git clone -q "\$REPO" "\$CLONE"\n', text)
        self.assertIsNotNone(m, "в scripts/e2e_opencode.sh нет строки клонирования")
        tail = text[m.end():]
        self.assertRegex(
            tail,
            r'git -C "\$CLONE" checkout -q "\$\(git -C "\$REPO" rev-parse HEAD\)"',
            "scripts/e2e_opencode.sh: после клонирования нет checkout на HEAD "
            "исходного репозитория — прогон тестирует ветку по умолчанию (main), "
            "а не проверяемое состояние (комментарий в шапке скрипта обязан это "
            "объяснять)")

    def test_clone_comment_explains_pinning(self):
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("HEAD", text,
                      "в scripts/e2e_opencode.sh нет пояснения о привязке клона к HEAD")


if __name__ == "__main__":
    unittest.main()
