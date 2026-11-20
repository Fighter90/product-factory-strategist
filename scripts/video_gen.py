#!/usr/bin/env python3
"""Генератор видео «интерактивная консоль» для демо-прогонов (PRO-124).

Стиль: посимвольный набор текста в окне macOS Terminal (PIL-рендер кадров),
озвучка `say` (RU: Milena rate 178, EN: Samantha rate 180), сборка ffmpeg.

Использование:
  # как есть (числа текущего демо «Связь для близких» зашиты как значения по умолчанию):
  python3 scripts/video_gen.py --scenario video/scenarios/svyaz-overview-ru.json --out video/svyaz-overview-RU.mp4

  # перегенерация под артефакты другого демо-проекта — одна команда (--project):
  python3 scripts/video_gen.py --scenario video/scenarios/svyaz-overview-ru.json \
      --out video/svyaz-overview-RU.mp4 --project projects/<slug>

Сценарий (JSON): {"lang":"ru","title":"...","beats":[
   {"speaker":"pfs","text":"…"},                 // вывод агента (набор посимвольно, построчно)
   {"speaker":"human","text":"…"},               // ввод руководителя (prompt > с курсором)
   {"cmd":"python3 -m tools.pfs status","out":"…"} // команда + вывод
]}

Подстановки {{…}} в текстах beat'ов заполняются из vars: по умолчанию — числа
текущего демо; с --project — из артефактов проекта (claims/decisions/log/outputs,
analysis/economics.py, README, knowledge/INDEX.md). Не заполненные {{…}} —
предупреждение в stdout (плейсхолдеры остаются видны в кадре намеренно).

Каждый beat: аудио = say(text), кадры = терминал, где текст появляется посимвольно
со скоростью чтения; затем пауза. Итог: mp4 h264 + aac.
"""
import argparse, json, os, re, subprocess, sys, tempfile
from pathlib import Path

FPS = 30
CHARS_PER_SEC = 42          # скорость «набора» (док. константа; тайминг ведёт аудио)
LINE_HOLD = 0.45            # пауза после блока
W, H = 1280, 800
MARGIN = 46
MAX_LINES = 26              # видимое окно терминала (последние N строк)
BG = (12, 12, 14); FG = (232, 232, 236); GREEN = (78, 201, 130); BLUE = (97, 158, 240)
YELLOW = (229, 192, 123); DIM = (120, 120, 128); REDBAR = (60, 60, 64)

FONTS = {
    "ru": "/System/Library/Fonts/SFNSMono.ttf",
    "en": "/System/Library/Fonts/SFNSMono.ttf",
}
VOICE = {"ru": ["-v", "Milena", "-r", "178"], "en": ["-v", "Samantha", "-r", "180"]}

FOOTER = {
    "ru": "pfs · 12 шагов · факт/допущение/гипотеза/вывод · стоимость $0 CLI",
    "en": "pfs · 12 steps · fact/assumption/hypothesis/inference · CLI cost $0",
}

# ---------------- vars: демо-специфичные числа ----------------

def _fmt_num(n, lang):
    if lang == "ru":
        return f"{n:,}".replace(",", "\u00a0")      # 12 000 (неразрывный пробел)
    return f"{n:,}"                                  # 12,000

def _fmt_dec(x, lang):
    s = f"{x:.2f}"
    return s.replace(".", ",") if lang == "ru" else s

def default_vars(lang):
    """Значения по умолчанию — проверенные числа демо «Связь для близких» (PRO-125)."""
    ru = {
        "target_mln": "285,75",          # целевой сценар прибыли, млн ₽ (analysis/economics.py)
        "boundary_months": "12 000",     # граница решения [C003]: 12 000 мес × 500 ₽ = +6 млн
        "tests": "962",                  # счётчик автотестов (README)
        "kb_cards": "111",               # карты базы знаний (pfs kb index)
        "artifacts": "11",               # артефактов собирает pfs finish (журнал демо)
        "score": "98/100",               # pfs check --strict (07_quality_review)
        "claims_total": "26",
        "c_fact": "10", "c_assumption": "8", "c_hyp": "4", "c_inf": "4",
        "decision_id": "D001",
    }
    en = {
        "target_mln": "285.75",
        "boundary_months": "12,000",
        "tests": "962",
        "kb_cards": "111",
        "artifacts": "11",
        "score": "98/100",
        "claims_total": "26",
        "c_fact": "10", "c_assumption": "8", "c_hyp": "4", "c_inf": "4",
        "decision_id": "D001",
    }
    return dict(ru if lang == "ru" else en)

def _repo_root_from_project(project_dir: Path) -> Path | None:
    """projects/<slug> → корень репозитория (для README и knowledge/INDEX.md)."""
    for parent in [project_dir, *project_dir.parents]:
        if (parent / "tools" / "pfs").exists() and (parent / "README.md").exists():
            return parent
    return None

def project_vars(project_dir, lang):
    """Вывести vars из артефактов проекта. Чтение реестров — только внутри репозитория."""
    p = Path(project_dir)
    v: dict = {}
    if not p.exists():
        print(f"  ! --project: каталог не найден: {p} — использую значения по умолчанию")
        return v

    # 1) утверждения (только активные) — claims.jsonl
    cf = p / "claims.jsonl"
    if cf.exists():
        counts, total = {}, 0
        for line in cf.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                c = json.loads(line)
            except ValueError:
                continue
            if c.get("status", "active") != "active":
                continue
            total += 1
            k = c.get("kind")
            if k:
                counts[k] = counts.get(k, 0) + 1
        if total:
            v["claims_total"] = _fmt_num(total, lang)
            for key, kind in (("c_fact", "fact"), ("c_assumption", "assumption"),
                              ("c_hyp", "hypothesis"), ("c_inf", "inference")):
                v[key] = _fmt_num(counts.get(kind, 0), lang)

    # 2) решение — decisions.jsonl (первое)
    df = p / "decisions.jsonl"
    if df.exists():
        for line in df.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except ValueError:
                continue
            if d.get("id"):
                v["decision_id"] = str(d["id"])
                break

    # 3) оценка контроля качества — outputs/07_quality_review.md
    q7 = p / "outputs" / "07_quality_review.md"
    if q7.exists():
        m = re.search(r"(\d+\s*/\s*100)", q7.read_text(encoding="utf-8"))
        if m:
            v["score"] = re.sub(r"\s", "", m.group(1))

    # 4) артефакты pfs finish — последняя строка журнала «Собран финальный пакет»
    lf = p / "log.jsonl"
    if lf.exists():
        n = None
        for line in lf.read_text(encoding="utf-8").splitlines():
            if "Собран финальный пакет" not in line:
                continue
            try:
                msg = json.loads(line).get("msg", "")
            except ValueError:
                continue
            tail = msg.split(":", 1)[1] if ":" in msg else ""
            items = [s for s in tail.split(",") if s.strip()]
            if items:
                n = len(items)
        if n:
            v["artifacts"] = _fmt_num(n, lang)

    # 5) экономика целевого сценария и граница решения — analysis/economics.py
    econ = (p / "analysis" / "economics.py").resolve()
    if econ.exists():
        try:
            r = subprocess.run([sys.executable, str(econ)], cwd=str(p.resolve()), capture_output=True,
                               text=True, timeout=60)
            out = r.stdout
            m = re.search(r"прибыль\s+([\d.,]+)\s*млн", out)
            if m:
                v["target_mln"] = m.group(1).rstrip("0").rstrip(".") if "." in m.group(1) else m.group(1)
                if lang == "en":
                    v["target_mln"] = v["target_mln"].replace(",", ".")
                else:
                    v["target_mln"] = v["target_mln"].replace(".", ",")
            m = re.search(r"(\d[\d\s\u00a0,]*)\s*доп\.?\s*оплаченных месяцев", out)
            if m:
                raw = re.sub(r"[\s\u00a0,]", "", m.group(1))
                if raw.isdigit():
                    v["boundary_months"] = _fmt_num(int(raw), lang)
        except (subprocess.SubprocessError, OSError) as e:
            print(f"  ! economics.py не выполнен: {e}")

    # 6) счётчик автотестов и карты базы знаний — по корню репозитория
    root = _repo_root_from_project(p)
    if root:
        m = re.search(r"(\d{3,4})\s*тест", (root / "README.md").read_text(encoding="utf-8"))
        if m:
            v["tests"] = _fmt_num(int(m.group(1)), lang)
        methods = root / "knowledge" / "methods"
        if methods.is_dir():
            n = len(list(methods.glob("*.md")))
            if n:
                v["kb_cards"] = _fmt_num(n, lang)
    return v

def substitute(beats, title, vars_):
    """Заменить {{key}} в текстах beat'ов; вернуть список незаполненных плейсхолдеров."""
    left = set()

    def sub(s):
        def rep(m):
            k = m.group(1)
            if k in vars_:
                return str(vars_[k])
            left.add(k)
            return m.group(0)
        return re.sub(r"\{\{(\w+)\}\}", rep, s)

    out = []
    for b in beats:
        b = dict(b)
        for f in ("text", "out", "cmd"):
            if f in b and isinstance(b[f], str):
                b[f] = sub(b[f])
        out.append(b)
    if title:
        title = sub(title)
    return out, title, sorted(left)

# ---------------- рендер ----------------

def font(size):
    from PIL import ImageFont
    return ImageFont.truetype(FONTS["ru"], size)

def _make_measurer():
    from PIL import Image, ImageDraw
    img = Image.new("RGB", (8, 8))
    return ImageDraw.Draw(img)

def wrap_all(draw, draw_lines):
    """Развёртка блока в плоский список строк (по одному разу на beat, не на кадр)."""
    f_b = font(19); f_s = font(16)
    flat = []
    for kind, text, color in draw_lines:
        f = f_b if kind in ("out", "cmd") else f_s
        cur = ""
        for word in text.split(" "):
            test = (cur + " " + word).strip()
            if draw.textlength(test, font=f) <= W - 2 * MARGIN:
                cur = test
            else:
                if cur:
                    flat.append((cur, color, f))
                cur = word
        if cur:
            flat.append((cur, color, f))
        flat.append(("", color, f))  # отступ после блока
    return flat[-MAX_LINES:]

def render_frame(visible, title="", lang="ru"):
    from PIL import Image, ImageDraw
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 38], fill=REDBAR)
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        d.ellipse([16 + i * 26, 11, 32 + i * 26, 27], fill=c)
    f_t = font(15)
    d.text((W // 2 - 260, 10), (title or "pfs — Стратег Фабрики продуктов")[:64], font=f_t, fill=(200, 200, 204))
    y = MARGIN
    for ln, color, f in visible:
        if ln:
            d.text((MARGIN, y), ln, font=f, fill=color)
        y += 27
    d.text((MARGIN, H - 34), FOOTER.get(lang, FOOTER["ru"]), font=font(16), fill=DIM)
    return img

def say_wav(text, lang, out_wav):
    subprocess.run(["say"] + VOICE[lang] + ["-o", out_wav, "--data-format=LEI16@22050", text], check=True)

def wav_duration(path):
    r = subprocess.run(["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
                        "-of", "csv=p=0", path], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 1.0

def beat_lines(b):
    """Строки терминала для beat'а: (kind, text, color)."""
    if "cmd" in b:
        lines = [("cmd", "$ " + b["cmd"], BLUE)]
        if b.get("out"):
            lines.append(("out", b["out"], FG))
        return lines
    if b.get("speaker") == "human":
        return [("cmd", "> " + b.get("text", ""), YELLOW)]
    return [("out", b.get("text", ""), GREEN if b.get("accent") == "ok" else FG)]

def build_video(scen_path, out_path, project=None):
    scen = json.loads(Path(scen_path).read_text(encoding="utf-8"))
    lang = scen.get("lang", "ru")
    title = scen.get("title", "")
    vars_ = default_vars(lang)
    vars_.update(scen.get("vars", {}))
    if project:
        pv = project_vars(project, lang)
        if pv:
            vars_.update(pv)
            print("vars из проекта:", {k: v for k, v in sorted(pv.items())})
    beats, title, missing = substitute(scen["beats"], title, vars_)
    if missing:
        print(f"  ВНИМАНИЕ: не заполнены плейсхолдеры (останутся видны): {', '.join('{' + m + '}' for m in missing)}")

    tmp = Path(tempfile.mkdtemp(prefix="videogen_"))
    meas = _make_measurer()
    print(f"beats: {len(beats)}; синтез речи...")
    audio_files, durations, visibles = [], [], []
    for i, b in enumerate(beats):
        text = b.get("text") or b.get("out") or b.get("cmd", "")
        wav = str(tmp / f"a{i:03}.wav")
        say_wav(text, lang, wav)
        dur = wav_duration(wav)
        audio_files.append(wav)
        durations.append(dur)
        visibles.append(wrap_all(meas, beat_lines(b)))
        print(f"  beat {i+1}/{len(beats)}: {dur:.1f}s  {text[:60]}")

    print("рендер кадров...")
    frame_paths = []
    for i, (visible, dur) in enumerate(zip(visibles, durations)):
        total_frames = max(int((dur + LINE_HOLD) * FPS), 8)
        typing_frames = int(total_frames * 0.8)
        base = visible[:-1]
        last_color = visible[-1][2] if visible else FG
        static_path = None
        for fi in range(total_frames):
            typing = fi < typing_frames and bool(visible and visible[-1][0])
            if typing:
                shown = visible[-1][0][: int(len(visible[-1][0]) * (fi + 1) / typing_frames)]
                img = render_frame(base + [(shown, last_color, visible[-1][2])], title=title, lang=lang)
                fp = str(tmp / f"f_{len(frame_paths):05}.png")
                img.save(fp)
                static_path = None
                saved = fp
            else:
                # статичная фаза: рендер один раз, остальные кадры — жёсткие ссылки
                if static_path is None:
                    img = render_frame(visible, title=title, lang=lang)
                    static_path = str(tmp / f"f_{len(frame_paths):05}.png")
                    img.save(static_path)
                    saved = static_path
                else:
                    fp = str(tmp / f"f_{len(frame_paths):05}.png")
                    try:
                        os.link(static_path, fp)
                    except OSError:
                        import shutil
                        shutil.copyfile(static_path, fp)
                    saved = fp
            frame_paths.append(saved)
    print(f"кадров: {len(frame_paths)}")

    print("аудио...")
    concat_list = str(tmp / "audio.txt")
    with open(concat_list, "w") as f:
        for w in audio_files:
            f.write(f"file '{w}'\n")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list,
                    "-ar", "22050", "-ac", "1", str(tmp / "audio.m4a")], check=True, capture_output=True)
    print(f"итого: {sum(durations):.0f}s аудио")
    subprocess.run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(tmp / "f_%05d.png"),
                    "-i", str(tmp / "audio.m4a"), "-c:v", "libx264", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-shortest", out_path], check=True, capture_output=True)
    print("OK:", out_path)

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Генератор демо-видео «интерактивная консоль» (PRO-124)")
    ap.add_argument("--scenario", required=True, help="JSON-сценарий (video/scenarios/*.json)")
    ap.add_argument("--out", required=True, help="путь результата .mp4")
    ap.add_argument("--project", default=None,
                    help="ПУТЬ К ПРОЕКТУ (projects/<slug>): перезаполнить {{vars}} из артефактов "
                         "демо-прогона для перегенерации одной командой")
    a = ap.parse_args()
    build_video(a.scenario, a.out, project=a.project)
