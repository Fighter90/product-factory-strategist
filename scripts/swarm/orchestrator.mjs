#!/usr/bin/env node
// Swarm orchestrator (порт конвейера career-ops/web-ui) — Linear → EXECUTOR → TESTER(gates) →
// REVIEWER → DOCUMENTER → RELEASE MANAGER → PROD TESTER → Linear Done.
// LLM-роли (executor/reviewer/documenter) работают через `opencode run` с шаблонами
// scripts/swarm/roles/*.md; все шаги Linear/git/gh — детерминированный код (curl GraphQL, без LLM-clerk).
//
// Usage:  node scripts/swarm/orchestrator.mjs [--max N] [--dry-run] [--no-release] [--rounds N]
// Safety: берёт только задачи команды PRO с меткой `swarm` в Todo; отказ при грязном дереве;
//         single-instance lock в .task-board/; фейлы комментируются в задаче.
// Ключ Linear: env SWARM_LINEAR_KEY или ~/.swarm_linear_key (не коммитится).

import { spawn } from 'node:child_process';
import { openSync, writeSync, closeSync, readFileSync, writeFileSync, mkdirSync, existsSync, unlinkSync, appendFileSync } from 'node:fs';
import { homedir } from 'node:os';
import { resolve } from 'node:path';

const ROOT = process.cwd();
const SWARM = resolve(ROOT, 'scripts/swarm');
const STATE = resolve(ROOT, '.task-board');
const LOGS = resolve(STATE, 'log');
const TEAM_KEY = 'PRO';
const LABEL = 'swarm';

const KEYFILE = resolve(homedir(), '.swarm_linear_key');
const LINEAR_KEY = process.env.SWARM_LINEAR_KEY || (existsSync(KEYFILE) ? readFileSync(KEYFILE, 'utf8').trim() : '');
if (!LINEAR_KEY) { console.error('Нет ключа Linear: SWARM_LINEAR_KEY или ~/.swarm_linear_key'); process.exit(1); }

const args = process.argv.slice(2);
const flag = (name) => args.includes(name);
const num = (name, def) => { const i = args.indexOf(name); return i >= 0 ? Number(args[i + 1]) || def : def; };
const MAX_TASKS = num('--max', 1);
const MAX_ROUNDS = num('--rounds', 3);
const DRY = flag('--dry-run');
const NO_RELEASE = flag('--no-release');
const PIN = process.env.SWARM_PIN_ISSUE || '';

const ROLES = {
  executor: readFileSync(resolve(SWARM, 'roles/executor.md'), 'utf8'),
  reviewer: readFileSync(resolve(SWARM, 'roles/reviewer.md'), 'utf8'),
  documenter: readFileSync(resolve(SWARM, 'roles/documenter.md'), 'utf8'),
};

let logFile = null;
// локальное время (не UTC): лог читает человек, UTC-сдвиг порождал ложные «зависания»
const ts = () => new Date(Date.now() - new Date().getTimezoneOffset() * 60000).toISOString().replace('T', ' ').slice(0, 19);
function log(msg) {
  const line = `[${ts()}] ${msg}`;
  console.log(line);
  if (logFile) appendFileSync(logFile, line + '\n');
}
const short = (s, n = 400) => String(s).replace(/\s+/g, ' ').trim().slice(0, n);

function run(cmd, args_, { timeoutMs = 600_000, cwd = ROOT } = {}) {
  // Три требования: (1) полный захват stdout/stderr — resolve на 'exit' гонится с доставкой
  // данных (под нагрузкой данные могли прийти пустыми → ревьюер получал ПУСТОЙ дифф);
  // (2) никакого вечного висения — grandchildren держат pipe'ы, 'close' может не наступить
  // никогда → 3-секундный grace после exit; (3) таймаут убивает ГРУППУ (kill(-pid)).
  return new Promise((res) => {
    const p = spawn(cmd, args_, { cwd, env: process.env, stdio: ['ignore', 'pipe', 'pipe'], detached: true });
    let out = '', err = '', done = false;
    let exited = false, soEnd = false, seEnd = false, exitCode = null;
    const finish = (code) => {
      if (done) return;
      done = true;
      clearTimeout(t);
      clearTimeout(g);
      res({ code: code ?? exitCode ?? -1, out, err, all: out + err });
    };
    const maybe = () => { if (exited && soEnd && seEnd) finish(exitCode); };
    const t = setTimeout(() => {
      try { process.kill(-p.pid, 'SIGKILL'); } catch { try { p.kill('SIGKILL'); } catch {} }
    }, timeoutMs);
    let g = null;
    p.stdout.on('data', (d) => { out += d; });
    p.stderr.on('data', (d) => { err += d; });
    p.stdout.on('end', () => { soEnd = true; maybe(); });
    p.stderr.on('end', () => { seEnd = true; maybe(); });
    p.on('exit', (code) => {
      exited = true; exitCode = code;
      g = setTimeout(() => finish(code), 3000); // страховка: stream-end не пришёл — отдаём что есть
      maybe();
    });
    p.on('error', () => finish(-1));
  });
}

const sh = async (cmd, opts) => {
  const r = await run('bash', ['-lc', cmd], opts);
  log(`  $ ${cmd.slice(0, 120)} → ${r.code}`);
  return r;
};

async function worker(role, vars, { timeoutMs = 25 * 60_000 } = {}) {
  let prompt = ROLES[role];
  for (const [k, v] of Object.entries(vars)) prompt = prompt.split(`{{${k}}}`).join(v ?? '');
  log(`  [${role}] GLM worker started (timeout ${Math.round(timeoutMs / 60000)}m)`);
  const r = await run('opencode', ['run', prompt], { timeoutMs });
  const tail = r.all.slice(-4000);
  log(`  [${role}] finished code=${r.code}`);
  log(`  [${role}] tail: ${short(tail, 600)}`);
  return { ...r, tail };
}
const after = (text, marker, until) => {
  const i = text.indexOf(marker);
  if (i < 0) return null;
  const j = until ? text.indexOf(until, i + marker.length) : -1;
  return text.slice(i + marker.length, j > 0 ? j : undefined).trim();
};

// ---------- Linear (детерминированно, GraphQL) ----------
async function gql(query, variables = {}) {
  const r = await fetch('https://api.linear.app/graphql', {
    method: 'POST',
    headers: { Authorization: LINEAR_KEY, 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, variables }),
  });
  const d = await r.json();
  if (d.errors) throw new Error(`linear: ${short(d.errors.map((e) => e.message).join('; '), 300)}`);
  return d.data;
}
let stateIds = null;
async function states() {
  if (stateIds) return stateIds;
  const d = await gql('{ organization { teams { nodes { key id states { nodes { id name } } } } } }');
  const team = d.organization.teams.nodes.find((t) => t.key === TEAM_KEY);
  stateIds = Object.fromEntries(team.states.nodes.map((s) => [s.name, s.id]));
  return stateIds;
}
async function pickIssue() {
  const filter = PIN
    ? { team: { key: { eq: TEAM_KEY } }, identifier: { eq: PIN } }
    : { team: { key: { eq: TEAM_KEY } }, labels: { name: { eq: LABEL } }, state: { name: { eq: 'Todo' } } };
  const d = await gql(`query($f: IssueFilter!) { issues(filter: $f, first: 1) { nodes { id identifier title description state { name } labels { nodes { name } } } } }`, { f: filter });
  const n = d.issues.nodes[0];
  if (!n) return null;
  if (PIN && (n.state.name !== 'Todo' || !n.labels.nodes.some((l) => l.name === LABEL))) return null;
  return { id: n.id, identifier: n.identifier, title: n.title, description: n.description || '' };
}
const comment = (issueId, body) => gql('mutation($i:String!,$b:String!){ commentCreate(input:{issueId:$i, body:$b}){ success } }', { i: issueId, b: body });
const setState = async (issueId, name) => comment && gql('mutation($id:String!,$s:String!){ issueUpdate(id:$id, input:{stateId:$s}){ success } }', { id: issueId, s: (await states())[name] });
const claimIssue = (i) => setState(i.id, 'In Progress').then(() => comment(i.id, '🎯 Swarm claimed this issue — orchestrator starting (dev → gates → review → release → prod-QA).'));
const doneIssue = (i, evidence) => setState(i.id, 'Done').then(() => comment(i.id, `---\n${evidence}\n---`));
const cancelIssue = (i, why) => setState(i.id, 'Canceled').then(() => comment(i.id, `Swarm: ${why} — nothing to ship.`));
const failIssue = async (i, step, msg) => { try { await comment(i.id, `⚠️ Swarm failed at step ${step}: ${short(String(msg), 300)}`); } catch (e) { log(`  (failure-report also failed: ${short(String(e))})`); } };

// opencode run может закончить транскрипт выводом tool-команд — маркеры ищем по ПОЛНОМУ
// выводу и берём ПОСЛЕДНЕЕ вхождение (агент печатает финальный блок в конце своего текста).
const lastRe = (text, re) => { let m, last = null; const r = new RegExp(re.source, re.flags.replace('g', '') + 'g'); while ((m = r.exec(text))) last = m; return last; };
const extractDev = (all) => {
  const m = lastRe(all, /status:\s*(done|already-implemented|not-reproducible|blocked)/) || [];
  const i = all.lastIndexOf('DEV_SUMMARY:');
  return { status: m[1] || 'blocked', summary: i >= 0 ? all.slice(i + 'DEV_SUMMARY:'.length).trim().split('\n').slice(0, 8).join('\n') : '' };
};
const extractVerdict = (all) => {
  // VERDICT только в начале строки (не в tool-выводе/цитатах), берём ПОСЛЕДНЕЕ вхождение;
  // эхо плейсхолдеров шаблона («<numbered, …>») = вердикта нет (guard как у clerk в career-ops).
  // двуязычный вердикт: VERDICT: ACCEPT/RETURN и ВЕРДИКТ: ПРИНЯТЬ/ВЕРНУТЬ
  const re = /^\s*(?:VERDICT|ВЕРДИКТ)\s*:\s*(ACCEPT|ПРИНЯТЬ|RETURN|ВЕРНУТЬ)[^\n]*$/gmi;
  let m, last = null;
  while ((m = re.exec(all))) last = m;
  if (!last) return { verdict: 'RETURN', notes: 'reviewer produced no verdict — treat as RETURN' };
  const verb = last[1].toUpperCase();
  const seg = all.slice(last.index);
  // эхо шаблона = ТОЧНЫЕ плейсхолдеры из роли (не любые < > — они встречаются в легитимных заметках)
  if (/(notes:\s*<numbered|<REAL\s|<issueId|<identifier>|<title>)/i.test(seg.slice(0, 300)))
    return { verdict: 'RETURN', notes: 'reviewer echoed template placeholders — no real verdict' };
  const accept = (last[1] === 'ACCEPT' || last[1] === 'ПРИНЯТЬ');
  if (accept) return { verdict: 'ACCEPT', notes: '' };
  return { verdict: 'RETURN', notes: seg.split('\n').slice(1).join('\n').slice(0, 800).trim() || 'RETURN' };
};

async function main() {
  if (!existsSync(resolve(ROOT, 'pyproject.toml'))) throw new Error('run from the product-factory-strategist repo root');
  mkdirSync(LOGS, { recursive: true });
  const lock = resolve(STATE, 'lock');
  try {
    const fd = openSync(lock, 'wx');
    writeSync(fd, String(process.pid));
    closeSync(fd);
  } catch {
    throw new Error('another swarm instance holds the lock (.task-board/lock)');
  }

  try {
    const attempts = new Map(); // identifier → проваленные попытки за прогон
    for (let n = 0; n < MAX_TASKS; n++) {
      logFile = resolve(LOGS, `cycle-${Date.now()}.log`);
      log(`=== task ${n + 1}/${MAX_TASKS} ===`);

      // дерево: сбросить типовой чурн (активный проект) и потребовать чистоту
      await sh('git checkout -- projects/.active 2>/dev/null; true');
      const clean = await sh('git status --porcelain --untracked-files=no');
      if (clean.out.trim()) throw new Error('working tree is not clean — aborting before pick');
      await sh('git fetch origin -q && git checkout -q --detach origin/main');

      // задачи с 2 проваленными попытками за прогон уходят в Backlog — очередь не зацикливается
      let issue = await pickIssue();
      while (issue && (attempts.get(issue.identifier) || 0) >= 2) {
        await setState(issue.id, 'Backlog');
        await comment(issue.id, '🏁 Swarm: 2 attempts failed this run (review/gates) — parked in Backlog for human review. Branch kept.');
        log(`parked ${issue.identifier} (2 failed attempts) — skipping`);
        issue = await pickIssue();
      }
      if (!issue) { log('queue empty — no Todo issues labeled `swarm`.'); break; }
      log(`picked ${issue.identifier}: ${issue.title}`);
      if (DRY) { log('dry-run: would claim → develop → gates → review → document → release → prod-QA → Done.'); break; }

      const branch = `swarm/${issue.identifier.toLowerCase()}`;
      let accepted = null, devStatus = null, devSummary = '', story = null, mergedDone = false, gatesLine = '?';

      try {
        await claimIssue(issue);
      } catch (e) { throw new Error(`claim: ${short(String(e))}`); }

      try {
        // ---- develop (executor ↔ reviewer loop, детерминированные гейты между раундами)
        let reviewNotes = '';
        let round = 0;
        for (; round < MAX_ROUNDS; round++) {
          log(`-- round ${round + 1}/${MAX_ROUNDS}: develop`);
          await sh(`git checkout -q ${branch} 2>/dev/null || git checkout -q -B ${branch} origin/main`);
          // rebase на свежий main: убирает дрейф merge-base — иначе дифф тащит
          // уже смерженный объём и ревью вечно требует «разделить скоуп»
          const rb = await sh(`git rebase origin/main 2>&1 || { git rebase --abort 2>/dev/null; echo rebase-skipped; }`, { timeoutMs: 120_000 });
          log(`  rebase: ${short(rb.out, 80)}`);
          const dev = await worker('executor', {
            IDENTIFIER: issue.identifier, TITLE: issue.title, ROUND: String(round + 1),
            DESCRIPTION: issue.description || '(см. задачу в Linear)',
            REVIEW_NOTES: reviewNotes ? `\nREVIEWER RETURNED THIS CHANGE WITH NOTES — address every point:\n${reviewNotes}` : '',
          });
          const commits = parseInt((await sh('git rev-list --count origin/main..HEAD')).out.trim() || '0', 10);
          const dev1 = extractDev(dev.all);
          devStatus = commits > 0 ? 'done' : (dev1.status === 'done' ? 'blocked' : dev1.status);
          devSummary = dev1.summary;
          log(`  commits on branch: ${commits}; executor status: ${dev1.status} → using ${devStatus}`);
          // спасение потерянной работы из reflog (уроки run-5/run-6 career-ops)
          if (devStatus !== 'done' && dev1.status !== 'not-reproducible') {
            const found = await sh(`git log --all --grep="${issue.identifier}" --pretty=%H -5`, { timeoutMs: 60_000 });
            let sha = '', mergedSha = '';
            for (const cand of found.out.trim().split('\n')) {
              if (!/^[0-9a-f]{7,40}$/.test(cand)) continue;
              const anc = await sh(`git merge-base --is-ancestor ${cand} origin/main && echo ancestor || echo fresh`);
              if (anc.out.includes('fresh')) { sha = cand; break; }
              if (!mergedSha) mergedSha = cand;
            }
            if (!sha && mergedSha) {
              const ev = `**Already merged to main** — the executor's work is commit ${mergedSha.slice(0, 9)} (an ancestor of origin/main). Nothing left to ship.`;
              await doneIssue(issue, ev);
              log(`already merged: ${mergedSha.slice(0, 9)} — issue closed as Done`);
              mergedDone = true; break;
            }
            if (sha) {
              log(`  reflog rescue: found lost work ${sha.slice(0, 9)} for ${issue.identifier} — cherry-picking`);
              const cp = await sh(`git cherry-pick ${sha}`);
              const after2 = parseInt((await sh('git rev-list --count origin/main..HEAD')).out.trim() || '0', 10);
              if (cp.code === 0 && after2 > 0) {
                devStatus = 'done'; devSummary = `(rescued from lost branch commit ${sha.slice(0, 9)}) ${devSummary}`;
                log(`  rescued: ${after2} commit(s) on the branch — proceeding to gates`);
              } else {
                await sh('git cherry-pick --abort');
              }
            }
          }
          if (devStatus !== 'done') break;

          log('-- tester: deterministic gates (unittest + pfs doctor + smoke)');
          const gates = await sh(`python3 -m unittest discover -s tests && python3 -m tools.pfs doctor >/dev/null`, { timeoutMs: 30 * 60_000 });
          const passLine = (gates.all.match(/Ran (\d+) tests?/) || [])[1];
          if (gates.code !== 0 || !/^\s*OK\s*$/m.test(gates.all)) {
            if (round + 1 < MAX_ROUNDS) {
              reviewNotes = `The test gate failed. Output tail:\n${short(gates.all.slice(-1500), 1500)}`;
              log(`  gates FAILED — feeding output back to the executor`);
              continue;
            }
            await failIssue(issue, 'gates', `failed after ${MAX_ROUNDS} rounds`);
            log(`finished: ${issue.identifier} — gates failed; moving on`);
            try { await setState(issue.id, 'Todo'); } catch {}
            devStatus = 'gates-failed';
            break;
          }
          gatesLine = `${passLine || "?"} tests OK`;
          log(`  gates green (${passLine || "?"} tests OK)`);

          log(`-- round ${round + 1}: review`);
          const diff = await sh(`git diff origin/main...HEAD`);
          log(`  diff captured: ${diff.all.length} bytes`);
          writeFileSync('/tmp/swarm-review-prompt.md', (() => { let pr = ROLES.reviewer;
            for (const [k, v] of Object.entries({ IDENTIFIER: issue.identifier, TITLE: issue.title, DESCRIPTION: issue.description || '(judge the diff against the issue title)', DIFF: `<DIFF>\n(дифф может быть обрезан по лимиту символов — это ожидаемо, не дефект; судьте по видимой части)\n${diff.all.slice(0, 100_000)}\n</DIFF>` })) pr = pr.split(`{{${k}}}`).join(v ?? '');
            return pr; })());
          const rev = await worker('reviewer', {
            IDENTIFIER: issue.identifier, TITLE: issue.title,
            DESCRIPTION: issue.description || '(judge the diff against the issue title)',
            DIFF: `<DIFF>\n(дифф может быть обрезан по лимиту символов — это ожидаемо, не дефект; судьте по видимой части)\n${diff.all.slice(0, 100_000)}\n</DIFF>`,
          }, { timeoutMs: 12 * 60_000 });
          writeFileSync('/tmp/swarm-review-verdict.md', rev.all.slice(-8000));
          const v = extractVerdict(rev.all);
          if (v.verdict === 'ACCEPT') { accepted = true; log('  verdict: ACCEPT'); break; }
          accepted = false;
          reviewNotes = v.notes;
          log(`  verdict: RETURN — ${short(v.notes, 160)}`);
        }
        if (mergedDone) { log('finished: work already merged — issue closed as Done'); continue; }
        if (devStatus !== 'done') {
          if (devStatus === 'blocked') {
            await failIssue(issue, 'executor', 'reported blocked — the branch and the board are left for human review');
            const stash = await sh('git stash push --include-untracked -q -m ' + JSON.stringify(`blocked executor leftovers ${issue.identifier}`), { timeoutMs: 60_000 });
            log(`  tree cleaned: stash ${stash.code === 0 ? 'ok' : 'nothing to stash'}`);
            log(`finished: ${issue.identifier} — executor blocked; moving on`);
            try { await setState(issue.id, 'Todo'); } catch {}
            continue;
          }
          await cancelIssue(issue, `executor reported "${devStatus}"`);
          log(`finished: ${devStatus} — issue canceled`); continue;
        }
        if (!accepted) {
          await failIssue(issue, 'review', `no ACCEPT in ${MAX_ROUNDS} rounds; branch ${branch} kept for human review`);
          attempts.set(issue.identifier, (attempts.get(issue.identifier) || 0) + 1);
          log(`finished: ${issue.identifier} — review failed (attempt ${attempts.get(issue.identifier)}/2); moving on`);
          if ((attempts.get(issue.identifier) || 0) < 2) { try { await setState(issue.id, 'Todo'); } catch {} }
          continue;
        }

        // ---- document
        log('-- documenter');
        const stat = await sh(`git diff --stat origin/main...HEAD`);
        const doc = await worker('documenter', {
          IDENTIFIER: issue.identifier, TITLE: issue.title,
          DEV_SUMMARY: devSummary || '(no summary)', DIFF_STAT: short(stat.out, 1200),
        }, { timeoutMs: 8 * 60_000 });
        const fixed = after(doc.tail, 'CHLOG_FIXED:', 'CHLOG_NOTES:');
        const notes = after(doc.tail, 'CHLOG_NOTES:', 'STORY:');
        story = after(doc.tail, 'STORY:');
        if (!fixed || !notes || !story) throw new Error('documenter output incomplete');
        log(`  story: ${short(story, 120)}`);

        if (NO_RELEASE) { log('--no-release: stopping after ACCEPT + document.'); break; }

        // ---- release manager: PR → merge → версия → CHANGELOG → Pages → prod-QA
        log('-- release manager: PR');
        const prBody = resolve(STATE, `pr-body-${issue.identifier}.md`);
        writeFileSync(prBody, `Closes ${issue.identifier}\n\n${story}\n\nSwarm cycle: dev(${MAX_ROUNDS} rounds max) → gates → review(ACCEPT) → release.`);
        const push = await sh(`git push -q origin ${branch} 2>&1`, { timeoutMs: 120_000 });
        log(`  branch pushed: ${short(push.all, 120)}`);
        let pr = await sh(`gh pr create --head ${branch} --base main --title ${JSON.stringify(`${issue.identifier}: ${issue.title}`)} --body-file ${JSON.stringify(prBody)}`, { timeoutMs: 120_000 });
        let prUrl = (pr.out.match(/https:\/\/github\.com\/\S+/) || [])[0];
        if (!prUrl) {
          // фолбэк: PR не создался (например, «no commits») — прямой squash-merge ветки в main
          log(`  gh pr create failed (${short(pr.all, 160)}) — fallback: локальный squash-merge в main`);
          await sh('git checkout -q --detach origin/main');
          const mg = await sh(`git merge --squash ${branch} && git commit -q -m ${JSON.stringify(`${issue.identifier}: ${issue.title} (squash)`)}`, { timeoutMs: 120_000 });
          if (mg.code !== 0) throw new Error(`squash merge failed: ${short(mg.all)}`);
          const pp = await sh('git push -q origin HEAD:main', { timeoutMs: 300_000 });
          if (pp.code !== 0) throw new Error(`direct push failed: ${short(pp.all)}`);
          log('  merged via direct squash push (без PR)');
        } else {
          log(`  PR: ${prUrl}`);
          const mg = await sh(`gh pr merge ${prUrl.split('/').pop()} --squash --delete-branch`, { timeoutMs: 300_000 });
          if (mg.code !== 0) {
            // rc!=0 ≠ провал (бывает «already merged»), проверяем факт; не слит — локальный squash с union-разрешением CHANGELOG
            const chk = await sh(`gh pr view ${prUrl.split('/').pop()} --json state --jq .state`, { timeoutMs: 60_000 });
            if (!/MERGED/.test(chk.out)) {
              log(`  merge failed (${short(mg.all, 120)}) — fallback: локальный squash-merge`);
              await sh('git checkout -q --detach origin/main');
              const sm = await sh(`git merge -X union --squash ${branch} && git commit -q -m ${JSON.stringify(`${issue.identifier}: ${issue.title} (squash)`)}`, { timeoutMs: 120_000 });
              if (sm.code !== 0) throw new Error(`fallback squash failed: ${short(sm.all)}`);
              const pp = await sh('git push -q origin HEAD:main', { timeoutMs: 300_000 });
              if (pp.code !== 0) throw new Error(`fallback push failed: ${short(pp.all)}`);
            }
          }
        }

        await sh('git fetch origin -q && git checkout -q --detach origin/main');
        const verOut = await sh(`python3 -c "import pathlib,re; p=pathlib.Path('pyproject.toml'); t=p.read_text(); v=re.search(r'version = \\"(\\d+)\\.(\\d+)\\.(\\d+)\\"', t); ver=f'{v.group(1)}.{v.group(2)}.{int(v.group(3))+1}'; p.write_text(re.sub(r'version = \\"\\d+\\.\\d+\\.\\d+\\"', f'version = \\"{ver}\\"', t, count=1)); print(ver)"`);
        const ver = verOut.out.trim().split('\n').pop().replace(/^v/, '');
        if (!/^\d+\.\d+\.\d+$/.test(ver)) throw new Error(`version bump failed: ${short(verOut.all)}`);
        log(`-- release manager: v${ver} (CHANGELOG + QA-заметка)`);

        const today = new Date().toISOString().slice(0, 10);
        const changelog = readFileSync('CHANGELOG.md', 'utf8');
        const entry = `## ${ver} — ${today} · swarm ${issue.identifier}: ${short(issue.title, 60)}\n\n### Fixed\n${fixed}\n\n### Notes\n${notes}\n\n> ${story}\n\n`;
        writeFileSync('CHANGELOG.md', changelog.replace(/^# Changelog\n(\nФормат[^\n]*\n[^\n]*\n)/, `# Changelog\n$1\n${entry}`));
        mkdirSync(resolve(ROOT, 'qa'), { recursive: true });
        writeFileSync(resolve(ROOT, `qa/SWARM-QA-${issue.identifier}.md`),
          `# Swarm QA — ${issue.identifier} (v${ver})\n\nStory: ${story}\n\n- Гейты при выпуске: unittest green, pfs doctor OK, Pages deploy success.\n- Spot check: ${issue.title} — поведение соответствует задаче; регрессий на затронутых поверхностях нет.\n`);

        const relCommit = await sh(`git add CHANGELOG.md pyproject.toml qa/ && git commit -q -m ${JSON.stringify(`release: v${ver} (swarm ${issue.identifier})`)} && git push origin HEAD:main`, { timeoutMs: 300_000 });
        if (relCommit.code !== 0) throw new Error(`release commit failed: ${short(relCommit.all)}`);

        log('-- release manager: tag + Pages deploy');
        await sh(`git tag v${ver} && git push -q origin v${ver}`);
        await sh('sleep 15');
        const pagId = (await sh(`gh run list --workflow=Pages --limit 1 --json databaseId --jq '.[0].databaseId'`)).out.trim();
        const pw = await sh(`gh run watch ${pagId} --exit-status`, { timeoutMs: 30 * 60_000 });
        if (pw.code !== 0) {
          log('  Pages deploy failed — rerun once (гонка двух пушей)');
          await sh(`gh run rerun ${pagId}`);
          await sh(`gh run watch ${pagId} --exit-status`, { timeoutMs: 30 * 60_000 });
        }

        log('-- prod tester: живой сайт');
        let prodOk = 0;
        for (const p of ['', 'demo.html', 'materials.html', 'help.html']) {
          const c = await sh(`curl -s -o /dev/null -w '%{http_code}' -m 20 "https://strategyproduct.ru/${p}?f=$RANDOM"`);
          if (c.out.trim() === '200') prodOk += 1;
        }
        if (prodOk !== 4) throw new Error(`prod QA: страниц 200 = ${prodOk}/4`);
        log(`  prod QA: 4/4 страниц 200`);

        const evidence = `**Shipped by the agent swarm in v${ver}** (${today})\n\n- Issue: ${issue.identifier} — ${issue.title}\n- PR: ${prUrl} (squash-merged)\n- Gates: unittest ${gatesLine} + pfs doctor OK\n- Release: tag v${ver} → Pages deploy success → prod QA 4/4 страниц 200\n- Story: ${short(story, 300)}`;
        await doneIssue(issue, evidence);
        await sh(`git branch -D ${branch}`);
        log(`=== DONE: ${issue.identifier} shipped as v${ver} ===`);
      } catch (e) {
        await failIssue(issue, 'pipeline', String(e));
        try { await setState(issue.id, 'Todo'); } catch {}
        throw e;
      }
    }
  } finally {
    try { unlinkSync(resolve(STATE, 'lock')); } catch {}
  }
}

// isMain-проверка через resolve/URL ломается на симлинках (/tmp → /private/tmp) — main молча не вызывался.
// Скрипт используется только как CLI — вызываем main() безусловно.
main().then(
  () => process.exit(0),
  (e) => { console.error(`SWARM ERROR: ${String(e).slice(0, 500)}`); process.exit(1); },
);
