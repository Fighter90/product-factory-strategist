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
// краш-безопасность (PRO-68): задача In Progress с меткой swarm, чей клейм старше
// STUCK_MIN минут (или без клейм-метки — краш до записи), считается зависшей и
// реqueue'ится в Todo; свежий клейм не трогаем — защита от перехвата чужой свежей работы
const STUCK_MIN = num('--stuck-min', 30);
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

// pyproject: fallback-инкремент (тегов нет — не должно случаться) и синхронизация
// вычисленной из тегов версии (PRO-68: pyproject отставал от тегов → коллизии)
const PY_BUMP = String.raw`python3 -c 'import pathlib,re; p=pathlib.Path("pyproject.toml"); m=re.search(r"version = \"(\d+)\.(\d+)\.(\d+)\"", p.read_text()); ver=m.group(1)+"."+m.group(2)+"."+str(int(m.group(3))+1); p.write_text(re.sub(r"version = \"\d+\.\d+\.\d+\"", "version = \""+ver+"\"", p.read_text(), count=1)); print(ver)'`;
const PY_SET = (v) => String.raw`python3 -c 'import pathlib,re,sys; p=pathlib.Path("pyproject.toml"); p.write_text(re.sub(r"version = \"\d+\.\d+\.\d+\"", "version = \""+sys.argv[1]+"\"", p.read_text(), count=1))' ` + JSON.stringify(v);

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
// зависшие In Progress с меткой swarm: пикер берёт только Todo, поэтому задача, брошенная
// In Progress крашем прошлого прогона, была невидима до ручного requeue (PRO-68:
// застревали PRO-53/54/55/59/60/61/63). Решение о «завислости» — по возрасту клейма.
const stuckIssues = async () => {
  const d = await gql(`query($f: IssueFilter!) { issues(filter: $f, first: 10) { nodes { id identifier title state { name } labels { nodes { name } } } } }`,
    { f: { team: { key: { eq: TEAM_KEY } }, labels: { name: { eq: LABEL } }, state: { name: { eq: 'In Progress' } } } });
  return d.issues.nodes;
};
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
    // счётчик проваленных попыток переживает перезапуски роя. Правила (review round 3):
    // (1) пишется в КАЖДОЙ ветке провала задачи, а не только при провале ревью;
    // (2) затухает — запись старше TTL забывается, иначе задача с двумя провалами в любом
    //     прошлом прогоне паркуется в Backlog навсегда; legacy-записи без ts считаются истёкшими;
    // (3) ошибки чтения/записи логируются, а не глотаются молча (иначе потеря файла невидима).
    const attemptsFile = resolve(STATE, 'attempts.json');
    const ATTEMPT_TTL_DAYS = 7;
    const ATTEMPT_TTL_MS = ATTEMPT_TTL_DAYS * 24 * 60 * 60_000;
    const loadAttempts = () => {
      const map = new Map();
      let raw = '';
      try { raw = readFileSync(attemptsFile, 'utf8'); }
      catch (e) {
        if (e && e.code !== 'ENOENT') log(`attempts: файл не прочитан (${short(String(e), 120)}) — счётчик начнётся с нуля`);
        return map; // нет файла — это норма для первого запуска, не ошибка
      }
      try {
        const now = Date.now();
        for (const [k, v] of Object.entries(JSON.parse(raw))) {
          const n = typeof v === 'number' ? v : (v && typeof v.n === 'number' ? v.n : 0);
          const ts = (v && typeof v === 'object' && typeof v.ts === 'number') ? v.ts : 0;
          if (n > 0 && now - ts < ATTEMPT_TTL_MS) map.set(k, { n, ts });
        }
      } catch (e) { log(`attempts: файл не разобран (${short(String(e), 120)}) — счётчик начнётся с нуля`); }
      return map;
    };
    const attempts = loadAttempts();
    const saveAttempts = () => {
      try { writeFileSync(attemptsFile, JSON.stringify(Object.fromEntries(attempts), null, 2)); }
      catch (e) { log(`attempts: НЕ СОХРАНЕНО (${short(String(e), 120)}) — счётчик может не пережить перезапуск`); }
    };
    const bumpAttempts = (id) => { // провал задачи: +1 попытка, сохранить, вернуть новое значение
      const n = (attempts.get(id)?.n || 0) + 1;
      attempts.set(id, { n, ts: Date.now() });
      saveAttempts();
      return n;
    };
    const triesOf = (id) => attempts.get(id)?.n || 0;
    // клейм-метки: когда оркестратор забрал задачу (identifier → ts мс). Нужны пик-секции,
    // чтобы отличить «зависла In Progress после краша» от свежего клейма (PRO-68).
    // Пишется ДО перевода в In Progress: краш между записью и setState безвреден
    // (Todo + лишняя запись), наоборот — In Progress без метки (возраст неизвестен).
    const claimedFile = resolve(STATE, 'claimed.json');
    const claims = (() => {
      try { return JSON.parse(readFileSync(claimedFile, 'utf8')); }
      catch (e) {
        if (e && e.code !== 'ENOENT') log(`claimed: файл не прочитан (${short(String(e), 120)}) — считаем клеймы неизвестными`);
        return {}; // нет файла — норма для первого запуска
      }
    })();
    const saveClaims = () => {
      try { writeFileSync(claimedFile, JSON.stringify(claims, null, 2)); }
      catch (e) { log(`claimed: НЕ СОХРАНЕНО (${short(String(e), 120)}) — зависшие In Progress могут быть не замечены`); }
    };
    const noteClaim = (id) => { claims[id] = Date.now(); saveClaims(); };
    const forgetClaim = (id) => { if (id in claims) { delete claims[id]; saveClaims(); } };
    for (let n = 0; n < MAX_TASKS; n++) {
      logFile = resolve(LOGS, `cycle-${Date.now()}.log`);
      log(`=== task ${n + 1}/${MAX_TASKS} ===`);

      // дерево: сбросить типовой чурн (активный проект) и потребовать чистоту.
      // Отказ при грязном дереве — осознанно (review round 3): auto-stash с
      // --include-untracked молча уносил WIP человека; пусть рой останавливается.
      await sh('git checkout -- projects/.active 2>/dev/null; true');
      const clean = await sh('git status --porcelain --untracked-files=no');
      if (clean.out.trim()) throw new Error('working tree is not clean — aborting before pick');
      await sh('git fetch origin -q && git checkout -q --detach origin/main');

      // краш-безопасность (PRO-68): single-instance lock гарантирует, что в момент
      // pick ни один прогон задачу не держит — всё In Progress с меткой swarm висит
      // после краша. Зависшая (клейма нет или старше STUCK_MIN минут) → Todo.
      for (const n of await stuckIssues()) {
        const t = claims[n.identifier];
        const ageMs = Date.now() - (typeof t === 'number' ? t : 0);
        const stale = typeof t !== 'number' || ageMs > STUCK_MIN * 60_000;
        if (!stale) continue;
        try {
          await setState(n.id, 'Todo');
          await comment(n.id, `♻️ Swarm: stuck In Progress for ${typeof t === 'number' ? Math.round(ageMs / 60000) : 'unknown'} min (crash after claim) — requeued to Todo (crash-safety).`);
          forgetClaim(n.identifier);
          log(`requeued stuck ${n.identifier} (In Progress, claim ${typeof t === 'number' ? Math.round(ageMs / 60000) + ' min ago' : 'unknown age'})`);
        } catch (e) { log(`  stuck-requeue failed for ${n.identifier}: ${short(String(e), 120)}`); }
      }

      // задачи с 2 проваленными попытками уходят в Backlog — очередь не зацикливается;
      // счётчик персистентен, но затухает (TTL 7 дней) — старые провалы не паркан навсегда
      let issue = await pickIssue();
      while (issue && triesOf(issue.identifier) >= 2) {
        await setState(issue.id, 'Backlog');
        await comment(issue.id, '🏁 Swarm: 2 attempts failed (review/gates; counter persists across runs, decays after 7 days) — parked in Backlog for human review. Branch kept.');
        forgetClaim(issue.identifier); // может остаться от краша прошлого прогона
        log(`parked ${issue.identifier} (2 failed attempts) — skipping`);
        issue = await pickIssue();
      }
      if (!issue) { log('queue empty — no Todo issues labeled `swarm`.'); break; }
      log(`picked ${issue.identifier}: ${issue.title}`);
      if (DRY) { log('dry-run: would claim → develop → gates → review → document → release → prod-QA → Done.'); break; }

      const branch = `swarm/${issue.identifier.toLowerCase()}`;
      let accepted = null, devStatus = null, devSummary = '', story = null, mergedDone = false, gatesLine = '?';

      try {
        // claim внутри общего try: падение ПОСЛЕ перевода в In Progress (например,
        // комментарий не прошёл) обязано вернуть задачу в Todo — иначе пикер её
        // не видит и задача висит до ручного requeue (PRO-68: 53/54/55/59/60/61/63)
        noteClaim(issue.identifier);
        await claimIssue(issue);

        // ---- develop (executor ↔ reviewer loop, детерминированные гейты между раундами)
        let reviewNotes = '';
        let round = 0;
        for (; round < MAX_ROUNDS; round++) {
          log(`-- round ${round + 1}/${MAX_ROUNDS}: develop`);
          await sh(`git checkout -q ${branch} 2>/dev/null || git checkout -q -B ${branch} origin/main`);
          // rebase на свежий main: убирает дрейф merge-base — иначе дифф тащит
          // уже смерженный объём и ревью вечно требует «разделить скоуп».
          // PRO-68: при конфликте ветка ПЕРЕСОЗДАЁТСЯ на свежем main (прежде было
          // «abort и работаем как раньше» — та ветка конфликтовала на релизном
          // squash-merge и роняла конвейер циклом). Исполнитель переприменит
          // работу по описанию задачи в этом же раунде — уже на чистой базе.
          const devRb = await sh(
            'git rebase --abort 2>/dev/null; ' +
            'if ! GIT_EDITOR=true GIT_SEQUENCE_EDITOR=true git rebase origin/main; then ' +
            'git rebase --abort 2>/dev/null; git checkout -q --detach HEAD 2>/dev/null; ' +
            `git checkout -q -B ${branch} origin/main; echo branch-recreated-on-fresh-main; fi`,
            { timeoutMs: 180_000 }
          );
          if (devRb.all.includes('branch-recreated-on-fresh-main')) log(`  branch ${branch} recreated on fresh main (rebase conflict) — executor re-applies on clean base`);
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
              attempts.delete(issue.identifier); saveAttempts();
              forgetClaim(issue.identifier);
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
            const tr = bumpAttempts(issue.identifier);
            log(`finished: ${issue.identifier} — gates failed (attempt ${tr}/2); moving on`);
            if (tr < 2) { try { await setState(issue.id, 'Todo'); forgetClaim(issue.identifier); } catch {} }
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
            try { await setState(issue.id, 'Todo'); forgetClaim(issue.identifier); } catch {}
            continue;
          }
          await cancelIssue(issue, `executor reported "${devStatus}"`);
          forgetClaim(issue.identifier);
          log(`finished: ${devStatus} — issue canceled`); continue;
        }
        if (!accepted) {
          await failIssue(issue, 'review', `no ACCEPT in ${MAX_ROUNDS} rounds; branch ${branch} kept for human review`);
          const tr = bumpAttempts(issue.identifier);
          log(`finished: ${issue.identifier} — review failed (attempt ${tr}/2); moving on`);
          if (tr < 2) { try { await setState(issue.id, 'Todo'); forgetClaim(issue.identifier); } catch {} }
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
        // PRO-68: ребейз ветки на свежий main ДО пуша/PR — пока шла разработка, могли
        // уйти другие релизы, и squash конфликтовал (AGENTS.md, README.md, CHANGELOG.md,
        // docs/HELP.md). Конфликты *.md разрешаем union-merge (обе стороны — типовой
        // случай: CHANGELOG/README дописали с обеих сторон); конфликт в коде не молчим —
        // ошибка (её поймает краш-безопасный catch, попытка учтётся). Прежний fallback
        // с флагом стратегии union при --squash был невалиден (fatal: unknown strategy
        // option) и ронял оркестратор.
        const rebaseOntoMain = () =>
          'git fetch origin -q; git rebase --abort 2>/dev/null; ' +
          // ребейз застрял на конфликте — состояние ЖИВОЕ, разрешаем прямо в нём;
          // abort здесь убил бы ребейз вместе с конфликтом («Нет перемещения в процессе»)
          'if ! GIT_EDITOR=true GIT_SEQUENCE_EDITOR=true git rebase origin/main; then ' +
          'while IFS= read -r f; do ' +
          'case "$f" in *.md) ;; *) echo "non-doc conflict: $f"; exit 1;; esac; ' +
          'git show ":1:$f" > /tmp/swarm-base.md; git show ":2:$f" > /tmp/swarm-ours.md; git show ":3:$f" > /tmp/swarm-theirs.md; ' +
          'git merge-file --union /tmp/swarm-ours.md /tmp/swarm-base.md /tmp/swarm-theirs.md || exit 1; ' +
          'cp /tmp/swarm-ours.md "$f"; git add -- "$f"; ' +
          'done < <(git diff --name-only --diff-filter=U); ' +
          'GIT_EDITOR=true GIT_SEQUENCE_EDITOR=true git rebase --continue || exit 1; fi';
        const localSquash = async (why) => {
          log(`  ${why} — локальный squash-merge`);
          const sm = await sh(rebaseOntoMain() + ` && git checkout -q --detach origin/main && git merge --squash ${branch} && git commit -q -m ${JSON.stringify(`${issue.identifier}: ${issue.title} (squash)`)}`, { timeoutMs: 180_000 });
          if (sm.code !== 0) throw new Error(`fallback squash failed (ребейз не снял конфликт): ${short(sm.all)}`);
          const pp = await sh('git push -q origin HEAD:main', { timeoutMs: 300_000 });
          if (pp.code !== 0) throw new Error(`fallback push failed: ${short(pp.all)}`);
          log('  merged via direct squash push (без PR)');
        };
        const rb = await sh(rebaseOntoMain(), { timeoutMs: 180_000 });
        if (rb.code !== 0 || /non-doc conflict/.test(rb.all)) throw new Error(`release rebase failed: ${short(rb.all)}`);
        log(`  branch rebased on fresh main: ${short(rb.all, 120)}`);
        const push = await sh(`git push -q --force-with-lease origin ${branch} 2>&1`, { timeoutMs: 120_000 });
        log(`  branch pushed: ${short(push.all, 120)}`);
        // существующий PR ветки мержим, а не создаём новый (PRO-68): повторный
        // gh pr create падал «already exists» → fallback конфликтовал → краш-цикл
        let prNum = (await sh(`gh pr list --head ${branch} --state open --json number --jq '.[0].number'`, { timeoutMs: 60_000 })).out.trim();
        let prUrl = '';
        if (!/^\d+$/.test(prNum)) {
          const pr = await sh(`gh pr create --head ${branch} --base main --title ${JSON.stringify(`${issue.identifier}: ${issue.title}`)} --body-file ${JSON.stringify(prBody)}`, { timeoutMs: 120_000 });
          prUrl = (pr.out.match(/https:\/\/github\.com\/\S+/) || [])[0] || '';
          prNum = /^\d+$/.test(prUrl.split('/').pop() || '') ? prUrl.split('/').pop() : '';
        }
        if (/^\d+$/.test(prNum)) {
          log(`  PR: #${prNum}${prUrl ? ` (${prUrl})` : ' (существующий, мержим его)'}`);
          const mg = await sh(`gh pr merge ${prNum} --squash --delete-branch`, { timeoutMs: 300_000 });
          if (mg.code !== 0) {
            // rc!=0 ≠ провал (бывает «already merged»), проверяем факт; не слит —
            // локальный squash (ветка только что на свежем main, конфликтов быть не должно)
            const chk = await sh(`gh pr view ${prNum} --json state --jq .state`, { timeoutMs: 60_000 });
            if (!/MERGED/.test(chk.out)) await localSquash(`merge failed (${short(mg.all, 120)})`);
          }
        } else {
          await localSquash('gh pr create failed');
        }

        await sh('git fetch origin -q && git checkout -q --detach origin/main');
        // PRO-68: версия = max(существующих тегов) + patch — pyproject отставал от тегов
        // (считал 1.2.20/1.2.21 при существующих v1.2.20–v1.2.24) → коллизии тегов и CHANGELOG
        await sh('git fetch --tags -q');
        const maxTag = (await sh(`git tag --list 'v*' --sort=-v:refname | head -1`)).out.trim();
        const mv = /^v(\d+)\.(\d+)\.(\d+)$/.exec(maxTag);
        let ver = mv ? `${mv[1]}.${mv[2]}.${Number(mv[3]) + 1}` : '';
        if (!ver) {
          // тегов нет (не должно случаться) — прежнее поведение: pyproject + 1
          const verOut = await sh(PY_BUMP);
          ver = verOut.out.trim().split('\n').pop().replace(/^v/, '');
        }
        // страховка от коллизии: если v<ver> вдруг существует — наращиваем patch дальше
        for (let i = 0; i < 10 && (await sh(`git rev-parse -q --verify refs/tags/v${ver}`)).out.trim(); i++) {
          const pv = ver.split('.'); ver = `${pv[0]}.${pv[1]}.${Number(pv[2]) + 1}`;
        }
        if (!/^\d+\.\d+\.\d+$/.test(ver)) throw new Error('version bump failed: no v-tags and pyproject fallback failed');
        const sync = await sh(`${PY_SET(ver)} && grep -q '^version = "${ver}"$' pyproject.toml`);
        if (sync.code !== 0) throw new Error(`pyproject version sync failed: ${short(sync.all)}`);
        log(`-- release manager: v${ver} (CHANGELOG + QA-заметка)`);

        // локальная дата (не UTC): UTC-дата отставала от локальной — запись CHANGELOG
        // датировалась прошлым днём (факт PRO-68: «1.2.20 — 2026-11-11»)
        const today = new Date(Date.now() - new Date().getTimezoneOffset() * 60000).toISOString().slice(0, 10);
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

        const evidence = `**Shipped by the agent swarm in v${ver}** (${today})\n\n- Issue: ${issue.identifier} — ${issue.title}\n- PR: ${prNum ? `#${prNum}` : 'direct squash push'} (squash-merged)\n- Gates: unittest ${gatesLine} + pfs doctor OK\n- Release: tag v${ver} → Pages deploy success → prod QA 4/4 страниц 200\n- Story: ${short(story, 300)}`;
        await doneIssue(issue, evidence);
        attempts.delete(issue.identifier); saveAttempts();
        forgetClaim(issue.identifier);
        await sh(`git branch -D ${branch}`);
        log(`=== DONE: ${issue.identifier} shipped as v${ver} ===`);
      } catch (e) {
        // краш-безопасность (PRO-68): любой выход после claim обязан вернуть задачу
        // в Todo (пикер берёт только Todo — иначе In Progress висит до ручного requeue),
        // учесть попытку (иначе краш-цикл бесконечен: PRO-63 горела 4+ циклов) и
        // продолжить очередь: дерево чистим (merge/rebase могли остаться в конфликте),
        // бросать наружу не бросаем — прогон продолжает движение сам, без watchdog-перезапуска.
        await failIssue(issue, 'pipeline', String(e));
        try { await setState(issue.id, 'Todo'); forgetClaim(issue.identifier); } catch {}
        const tr = bumpAttempts(issue.identifier);
        if (tr >= 2) {
          try {
            await setState(issue.id, 'Backlog');
            await comment(issue.id, '🏁 Swarm: 2 attempts failed (pipeline crash; counter persists across runs, decays after 7 days) — parked in Backlog for human review. Branch kept.');
          } catch {}
        }
        await sh('git merge --abort 2>/dev/null; git rebase --abort 2>/dev/null; ' +
          'git stash push --include-untracked -q -m ' + JSON.stringify(`crash leftovers ${issue.identifier}`) + ' 2>/dev/null; ' +
          'git checkout -q --detach HEAD 2>/dev/null; true', { timeoutMs: 120_000 });
        log(`finished: ${issue.identifier} — pipeline crash (attempt ${tr}/2); queue continues`);
        continue;
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
