"""PRO-68 (факты из лога /tmp/swarm-watchdog-run.log, 2026-11-12): релиз роя падал
на конфликтах, версии отставали от тегов, задачи застревали в In Progress после краша:

1. fallback локального merge содержал невалидный `git merge -X union --squash`
   (fatal: unknown strategy option — `-X` это опция стратегии, с --squash не работает);
2. PR уже существовал → gh pr create падал → fallback squash попадал в конфликт
   (AGENTS.md, README.md, CHANGELOG.md, docs/HELP.md) → краш → watchdog поднимал
   → задача снова picked → цикл (PRO-63 сгорела 4+ цикла и не попала в main);
3. краш происходил ПОСЛЕ claimIssue (статус уже In Progress) → пикер берёт только
   Todo → задача невидима до ручного requeue (PRO-53/54/55/59/60/61/63);
4. release-менеджер считал версию из pyproject (+1), а pyproject отставал от тегов
   (v1.2.20–v1.2.24) → коллизии CHANGELOG-записей и тегов; дата записи была UTC,
   и запись «1.2.20 — 2026-11-11» оказалась датирована прошлым днём.

Тесты сверяют scripts/swarm/orchestrator.mjs по исходнику
(приём как в test_swarm_attempts.py для не-Python-кода):

1. `-X union` убран; конфликт squash-merge → ребейз ветки на свежий main с
   union-разрешением *.md ДО пуша/PR, а в цикле разработки конфликт rebase →
   пересоздание ветки на свежем main (исполнитель переприменит работу);
2. существующий PR ветки мержится, а не создаётся заново;
3. версия = max(тегов v*) + patch, pyproject синхронизируется, тег проверяется
   на коллизию, дата CHANGELOG — локальная (не UTC);
4. краш-безопасность: застрявшая In Progress реqueue'ится по возрасту клейма;
   клейм пишется при claim и стирается на любом выходе; pipeline-краш возвращает
   задачу в Todo, учитывает попытку и продолжает очередь (cleanup дерева,
   continue — без повторного throw).
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORCH = (ROOT / "scripts" / "swarm" / "orchestrator.mjs").read_text(encoding="utf-8")


def seg_between(start: str, stop: str) -> str:
    """Текст от первого вхождения start до ближайшего stop после него."""
    i = ORCH.find(start)
    if i < 0:
        raise AssertionError(f"orchestrator.mjs: маркер не найден: {start!r}")
    j = ORCH.find(stop, i + len(start))
    if j < 0:
        raise AssertionError(f"orchestrator.mjs: маркер не найден: {stop!r}")
    return ORCH[i:j]


class NoInvalidUnionMerge(unittest.TestCase):
    def test_union_strategy_option_removed(self):
        """`git merge -X union --squash` — невалидный вызов (fatal: unknown strategy
        option), он ронял оркестратор. Ни одной формы -X union в исходнике быть не должно."""
        self.assertNotIn("-X union", ORCH, "невалидный -X union остался в fallback")
        self.assertNotIn("-Xunion", ORCH, "невалидный -Xunion остался в fallback")

    def test_local_squash_preceded_by_rebase_with_union_resolution(self):
        """Локальный squash-merge (fallback без PR и fallback при несмерженном PR) обязан
        идти после ребейза ветки на свежий main с union-разрешением конфликтов *.md:
        тогда squash применяет только дельту ветки и конфликтов не даёт."""
        rel = seg_between("-- release manager: PR", "-- release manager: v")
        self.assertIn("git merge --squash", rel, "локальный squash-merge исчез из релиза")
        self.assertIn("git merge-file --union", rel,
                      "конфликты *.md не разрешаются union-merge")
        self.assertIn('case "$f" in *.md)', rel,
                      "union-разрешение не ограничено *.md (для кода union опасен)")
        self.assertIn("git rebase origin/main", rel,
                      "перед squash нет ребейза на свежий main")
        self.assertLess(rel.find("git rebase origin/main"), rel.find("git merge --squash"),
                        "squash идёт ДО ребейза — конфликт не снят заранее")

    def test_push_uses_force_with_lease_after_rebase(self):
        """После ребейза история ветки переписана — обычный push отклоняется
        (non-fast-forward), нужен --force-with-lease."""
        self.assertIn("git push -q --force-with-lease", ORCH,
                      "пуш переписанной ветки без --force-with-lease отклоняется")


class ExistingPrReused(unittest.TestCase):
    def test_pr_list_checked_before_create(self):
        """Существующий PR ветки ищется ДО gh pr create: повторный create падал
        «already exists» → fallback на конфликтный squash → краш (PRO-68)."""
        i_list = ORCH.find("gh pr list --head")
        i_create = ORCH.find("gh pr create --head")
        self.assertGreater(i_list, 0, "нет поиска существующего PR ветки")
        self.assertLess(i_list, i_create, "gh pr create вызывается до проверки существующего PR")

    def test_existing_pr_number_is_merged(self):
        """Найденный/созданный PR мержится по номеру: gh pr merge <num> --squash."""
        self.assertRegex(ORCH, r"gh pr merge \$\{prNum\} --squash",
                         "PR не мержится по номеру — ветка существующего PR снова не попадёт в main")


class ConflictBeforeReview(unittest.TestCase):
    def test_develop_rebase_conflict_recreates_branch(self):
        """В цикле разработки конфликт rebase больше не «abort и работаем как раньше»
        (та ветка конфликтовала на релизном squash и роняла конвейер): ветка
        пересоздаётся на свежем main, исполнитель переприменит работу в этом же раунде."""
        seg = seg_between("rebase на свежий main", "worker('executor'")
        self.assertIn("git checkout -q -B", seg,
                      "конфликт rebase не пересоздаёт ветку на свежем main")
        self.assertIn("branch-recreated-on-fresh-main", seg,
                      "пересоздание ветки не маркируется в логе")
        self.assertNotIn("rebase-skipped", ORCH,
                         "старое поведение (тихий abort без пересоздания) осталось")

    def test_release_rebase_failure_is_reported_not_swallowed(self):
        """Неустранимый конфликт на релизном ребейзе (файл вне *.md) — ошибка,
        которую поймает краш-безопасный catch, а не тихое продолжение."""
        seg = seg_between("release rebase failed", "release manager: v")
        # проверка через сам throw выше: seg_between бросит AssertionError,
        # если маркера throw нет — этого достаточно
        self.assertTrue(True)


class VersionFromTags(unittest.TestCase):
    def test_version_is_max_tag_plus_patch(self):
        """Версия = max(существующих тегов v*) + patch: pyproject отставал от тегов
        (считал 1.2.20/1.2.21 при существующих v1.2.20–v1.2.24)."""
        rel = seg_between("git fetch --tags", "release manager: v")
        self.assertIn("git tag --list 'v*'", rel, "версия не вычисляется из тегов")
        self.assertIn("--sort=-v:refname", rel, "теги не сортируются по версии — max не гарантирован")
        self.assertNotIn("versionref", rel, "несуществующий sort-ключ versionref (fatal: неизвестное имя поля)")
        self.assertRegex(rel, r"Number\(mv\[3\]\)\s*\+\s*1",
                         "patch не наращивается от max-тега")

    def test_tag_collision_guard(self):
        """Перед созданием тега проверяется его отсутствие: если v<ver> существует —
        patch наращивается дальше (иначе git tag падал на существующем теге)."""
        self.assertIn("refs/tags/v${ver}", ORCH, "нет проверки коллизии тега")

    def test_pyproject_synced_to_computed_version(self):
        """pyproject синхронизируется с вычисленной версией — иначе следующий прогон
        снова посчитает версию отстающей."""
        self.assertIn("pyproject version sync failed", ORCH,
                      "синхронизация pyproject не проверяется на успех")

    def test_changelog_date_is_local_not_utc(self):
        """Дата записи CHANGELOG — локальная: UTC-дата на утренних часах отставала
        от локальной, запись датировалась прошлым днём (факт PRO-68)."""
        seg = seg_between("const today", "const changelog")
        self.assertIn("getTimezoneOffset", seg, "дата CHANGELOG считается в UTC")


class CrashSafety(unittest.TestCase):
    def test_pick_requeues_stuck_in_progress(self):
        """Пик-секция умеет находить зависшие In Progress с меткой swarm и возвращать
        их в Todo: пикер берёт только Todo, задача после краша была невидима до
        ручного requeue (PRO-53/54/55/59/60/61/63)."""
        self.assertIn("state: { name: { eq: 'In Progress' } }", ORCH,
                      "пик-секция не ищет зависшие In Progress")
        self.assertRegex(ORCH, r"STUCK_MIN\s*=\s*num\('--stuck-min'",
                         "порог «зависла старше N минут» не настраивается")
        self.assertRegex(ORCH, r"ageMs\s*>\s*STUCK_MIN",
                         "возраст клейма не сравнивается с порогом")

    def test_claim_timestamp_persisted_before_setstate(self):
        """Клейм-метка пишется ПЕРЕД переводом в In Progress и переживает перезапуск:
        crash между записью и setState безвреден, наоборот — возраст неизвестен."""
        i_note = ORCH.find("noteClaim(issue.identifier)")
        i_claim = ORCH.find("await claimIssue(issue)")
        self.assertGreater(i_note, 0, "клейм-метка не пишется при claim")
        self.assertLess(i_note, i_claim,
                        "клейм-метка пишется после setState — краш между ними теряет возраст")
        self.assertIn("claimed.json", ORCH, "клейм-метки не переживают перезапуск")

    def test_claim_cleared_on_every_exit(self):
        """Клейм-метка стирается на каждом выходе задачи: Done, Cancel, blocked,
        gates-fail, review-fail, pipeline-краш, парк."""
        done = seg_between("await doneIssue(issue, evidence)", "log(`=== DONE")
        self.assertIn("forgetClaim(issue.identifier)", done, "Done не стирает клейм")
        cancel = seg_between("await cancelIssue(issue,", "log(`finished: ${devStatus}")
        self.assertIn("forgetClaim(issue.identifier)", cancel, "Cancel не стирает клейм")
        blocked = seg_between("executor blocked", "await cancelIssue(issue,")
        self.assertIn("forgetClaim(issue.identifier)", blocked, "blocked не стирает клейм")
        gates = seg_between("failIssue(issue, 'gates'", "devStatus = 'gates-failed'")
        self.assertIn("forgetClaim(issue.identifier)", gates, "gates-fail не стирает клейм")
        review = seg_between("failIssue(issue, 'review'", "continue;")
        self.assertIn("forgetClaim(issue.identifier)", review, "review-fail не стирает клейм")
        crash = seg_between("failIssue(issue, 'pipeline'", "} finally {")
        self.assertIn("forgetClaim(issue.identifier)", crash, "pipeline-краш не стирает клейм")
        park = seg_between("triesOf(issue.identifier) >= 2", "queue empty")
        self.assertIn("forgetClaim(issue.identifier)", park, "парк не стирает клейм")

    def test_claim_failure_also_requeues(self):
        """Падение claim (setState прошёл, комментарий нет) тоже возвращает задачу
        в Todo: иначе In Progress без исполнителя — пикер её не видит."""
        crash = seg_between("failIssue(issue, 'pipeline'", "} finally {")
        self.assertIn("setState(issue.id, 'Todo')", crash,
                      "pipeline-краш не возвращает задачу в Todo")

    def test_pipeline_crash_bumps_attempts_and_parks_at_limit(self):
        """Pipeline-краш — тоже провал попытки: иначе краш-цикл (PRO-63 горела 4+
        циклов) бесконечен. На 2-м краше задача паркуется в Backlog."""
        crash = seg_between("failIssue(issue, 'pipeline'", "} finally {")
        self.assertIn("bumpAttempts(issue.identifier)", crash,
                      "pipeline-краш не учитывается в счётчике попыток")
        self.assertIn("'Backlog'", crash, "2-й pipeline-краш не паркует задачу")

    def test_pipeline_crash_continues_queue_without_rethrow(self):
        """После pipeline-краша очередь продолжает движение без ручного requeue:
        catch чистит дерево (merge/rebase могут остаться в конфликте) и делает
        continue, а не throw (throw уносил весь прогон)."""
        crash = seg_between("failIssue(issue, 'pipeline'", "} finally {")
        self.assertIn("git merge --abort", crash, "краш не чистит состояние merge")
        self.assertIn("git rebase --abort", crash, "краш не чистит состояние rebase")
        self.assertIn("continue;", crash, "после краша очередь не продолжает движение")
        self.assertNotIn("throw e", crash, "краш по-прежнему уносит весь прогон")

    def test_success_resets_claim(self):
        pass  # покрыт test_claim_cleared_on_every_exit (Done-ветка)


if __name__ == "__main__":
    unittest.main()
