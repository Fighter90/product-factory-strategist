#!/usr/bin/env python3
"""Генератор видео «интерактивная консоль» для демо-прогонов (PRO-124).

Стиль: посимвольный набор текста в окне macOS Terminal (PIL-рендер кадров),
озвучка `say` (RU: Milena rate 178, EN: Samantha rate 180), сборка ffmpeg.

Использование:
  python3 scripts/video_gen.py --scenario video/scenarios/overview-ru.json --out video/product-factory-strategist-связь-RU.mp4

Сценарий (JSON): {"lang":"ru","title":"...","beats":[
   {"speaker":"pfs","text":"…"},                 // вывод агента (набор посимвольно, построчно)
   {"speaker":"human","text":"…"},               // ввод руководителя (prompt $ с курсором)
   {"cmd":"python3 -m tools.pfs status","out":"…"} // команда + вывод
]}

Каждый beat: аудио = say(text), кадры = терминал, где текст появляется посимвольно
со скоростью чтения; затем пауза 0.4с на beat. Итог: mp4 h264 + aac.
"""
import argparse, json, os, subprocess, tempfile, sys
from pathlib import Path

FPS = 30
CHARS_PER_SEC = 42          # скорость «набора»
LINE_HOLD = 0.45            # пауза после блока
W, H = 1280, 800
MARGIN = 46
BG = (12, 12, 14); FG = (232, 232, 236); GREEN = (78, 201, 130); BLUE = (97, 158, 240)
YELLOW = (229, 192, 123); DIM = (120, 120, 128); REDBAR = (60, 60, 64)

FONTS = {
    "ru": "/System/Library/Fonts/SFNSMono.ttf",
    "en": "/System/Library/Fonts/SFNSMono.ttf",
}
VOICE = {"ru": ["-v", "Milena", "-r", "178"], "en": ["-v", "Samantha", "-r", "180"]}

def font(size, lang):
    from PIL import ImageFont
    return ImageFont.truetype(FONTS[lang], size)

def say_wav(text, lang, out_wav):
    subprocess.run(["say"] + VOICE[lang] + ["-o", out_wav, "--data-format=LEI16@22050", text], check=True)

def wav_duration(path):
    r = subprocess.run(["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
                        "-of", "csv=p=0", path], capture_output=True, text=True)
    try: return float(r.stdout.strip())
    except ValueError: return 1.0

def wrap(draw, text, f, width):
    lines, cur = [], ""
    for word in text.split(" "):
        test = (cur + " " + word).strip()
        if draw.textlength(test, font=f) <= width: cur = test
        else:
            if cur: lines.append(cur)
            cur = word
    if cur: lines.append(cur)
    return lines or [""]

def render_frame(draw_lines, cursor_at=None, title=""):
    from PIL import Image, ImageDraw
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # заголовок окна терминала
    d.rectangle([0, 0, W, 38], fill=REDBAR)
    for i, c in enumerate([(255,95,86),(255,189,46),(39,201,63)]):
        d.ellipse([16+i*26, 11, 32+i*26, 27], fill=c)
    f_t = font(15, "ru")
    d.text((W//2-260, 10), (title or "pfs — Стратег Фабрики продуктов")[:64], font=f_t, fill=(200,200,204))
    y = MARGIN
    f_b = font(19, "ru"); f_s = font(16, "ru")
    # развёртка строк с типами и скролл-окно (последние MAX_LINES видны)
    flat = []
    for kind, text, color in draw_lines:
        f = f_b if kind in ("out", "cmd") else f_s
        for ln in wrap(d, text, f, W - 2*MARGIN):
            flat.append((ln, color, f))
        flat.append(("", color, f))  # отступ после блока
    MAX_LINES = 26
    visible = flat[-MAX_LINES:]
    for ln, color, f in visible:
        d.text((MARGIN, y), ln, font=f, fill=color)
        y += 27
    if cursor_at is not None:
        d.rectangle([MARGIN + cursor_at, y - 2, MARGIN + cursor_at + 11, y + 20], fill=GREEN)
    d.text((MARGIN, H-34), "pfs · 12 шагов · факт/допущение/гипотеза/вывод · стоимость $0 CLI", font=f_s, fill=DIM)
    return img

def build_video(scen_path, out_path):
    scen = json.load(open(scen_path, encoding="utf-8"))
    lang = scen.get("lang", "ru"); title = scen.get("title", "")
    tmp = Path(tempfile.mkdtemp(prefix="videogen_"))
    beats = scen["beats"]
    print(f"beats: {len(beats)}; синтез речи...")
    audio_files, durations, rendered = [], [], []   # rendered: list[list[(kind,text,color)]]
    lines = []
    for i, b in enumerate(beats):
        text = b.get("text") or b.get("out") or b.get("cmd", "")
        wav = str(tmp / f"a{i:03}.wav")
        say_wav(text, lang, wav)
        dur = wav_duration(wav)
        audio_files.append(wav); durations.append(dur)
        if "cmd" in b:
            lines.append(("cmd", "$ " + b["cmd"], BLUE))
            if b.get("out"): lines.append(("out", b["out"], FG))
        elif b.get("speaker") == "human":
            lines.append(("cmd", "> " + text, YELLOW))
        else:
            lines.append(("out", text, GREEN if b.get("accent") == "ok" else FG))
        rendered.append([l for l in lines])
        print(f"  beat {i+1}/{len(beats)}: {dur:.1f}s  {text[:60]}")
    # кадры: для каждого beat — dur*FPS кадров; текст последней строки «набирается» первые 80% времени
    print("рендер кадров...")
    frame_paths = []
    for i, (lines_snapshot, dur) in enumerate(zip(rendered, durations)):
        total_frames = max(int((dur + LINE_HOLD) * FPS), 8)
        typing_frames = int(total_frames * 0.8)
        last = lines_snapshot[-1][1] if lines_snapshot else ""
        for fi in range(total_frames):
            if fi < typing_frames and len(last) > 0:
                shown = last[: int(len(last) * (fi + 1) / typing_frames)]
                fr = lines_snapshot[:-1] + [(lines_snapshot[-1][0], shown, lines_snapshot[-1][2])]
            else:
                fr = lines_snapshot
            img = render_frame(fr, title=title)
            fp = str(tmp / f"f_{len(frame_paths):05}.png"); img.save(fp); frame_paths.append(fp)
    # аудио: склейка с паузами
    print("аудио...")
    concat_list = str(tmp / "audio.txt")
    with open(concat_list, "w") as f:
        for w in audio_files:
            f.write(f"file '{w}'\n")
            f.write(f"file '{str(tmp / 'sil.wav')}'\n") if False else None
    # проще: ffmpeg concat без пауз (say уже с паузами)
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list,
                    "-ar", "22050", "-ac", "1", str(tmp / "audio.m4a")], check=True, capture_output=True)
    total = sum(durations)
    print(f"итого: {total:.0f}s аудио, кадров {len(frame_paths)}")
    # видео: слайдшоу из кадров по 1/FPS + подмешать аудио
    subprocess.run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(tmp / "f_%05d.png"),
                    "-i", str(tmp / "audio.m4a"), "-c:v", "libx264", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-shortest", out_path], check=True, capture_output=True)
    print("OK:", out_path)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--scenario", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    build_video(a.scenario, a.out)
