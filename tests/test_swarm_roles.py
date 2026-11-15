"""PRO-39 (round 2, отзыв reviewer'а): полезная нагрузка DIFF отсутствовала в prompt-review —
reviewer.md не содержал плейсхолдера {{DIFF}}, и worker() в orchestrator.mjs молча терял дифф.
Тест сверяет: каждая переменная, которую orchestrator передаёт роли, имеет плейсхолдер в шаблоне,
и подстановка реально кладёт payload в prompt (regression-тест «пустого ревью»)."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORCH = (ROOT / "scripts" / "swarm" / "orchestrator.mjs").read_text(encoding="utf-8")


def role_vars(role: str) -> set[str]:
    """Переменные, которые orchestrator передаёт worker('role', {...}) — по литералам ключей."""
    m = re.search(rf"worker\('{role}',\s*\{{(.*?)\}}\s*[,)]", ORCH, re.DOTALL)
    if not m:
        raise AssertionError(f"orchestrator.mjs: вызов worker('{role}', ...) не найден")
    return set(re.findall(r"([A-Z_]+):", m.group(1)))


class SwarmRoleTemplates(unittest.TestCase):
    def test_every_role_var_has_placeholder(self):
        """Каждый ключ из worker('<role>', {KEY: ...}) присутствует как {{KEY}} в roles/<role>.md."""
        for role in ("executor", "reviewer", "documenter"):
            tpl = (ROOT / "scripts" / "swarm" / "roles" / f"{role}.md").read_text(encoding="utf-8")
            have = set(re.findall(r"\{\{([A-Z_]+)\}\}", tpl))
            want = role_vars(role)
            self.assertEqual(want - have, set(),
                             f"roles/{role}.md: нет плейсхолдера(ов) {sorted(want - have)} — "
                             f"payload молча теряется (prompt уходит без данных)")
            self.assertEqual(have - want, set(),
                             f"roles/{role}.md: мёртвые плейсхолдеры {sorted(have - want)}")

    def test_diff_payload_reaches_reviewer_prompt(self):
        """Подстановка как в worker(): payload DIFF реально попадает в текст prompt reviewer'а."""
        tpl = (ROOT / "scripts" / "swarm" / "roles" / "reviewer.md").read_text(encoding="utf-8")
        payload = "<DIFF>\ndiff --git a/x b/x\n+closed sync\n</DIFF>"
        prompt = tpl.replace("{{DIFF}}", payload)  # та же подстановка, что в worker() orchestrator'а
        self.assertIn(payload, prompt, "дифф не вошёл в prompt — reviewer судит вслепую")
        self.assertNotIn("{{DIFF}}", prompt, "неподставленный плейсхолдер остался в prompt")


if __name__ == "__main__":
    unittest.main()
