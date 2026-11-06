#!/usr/bin/env python3
"""Markdown → печатный HTML (A4) → PDF через headless Chrome. Без зависимостей.

Запуск: python3 md_to_pdf.py input.md output.pdf ["Заголовок вкладки"]
Картинки ![alt](относительный путь) разрешаются относительно input.md.
"""
import html
import pathlib
import re
import subprocess
import sys
import tempfile

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

CSS = """
@page { size: A4; margin: 16mm 15mm 18mm; }
* { box-sizing: border-box; }
body { font: 10.5pt/1.55 -apple-system, "Helvetica Neue", "Segoe UI", Arial, sans-serif;
       color: #16211c; margin: 0; }
h1 { font-size: 21pt; letter-spacing: -0.4px; margin: 0 0 6pt; color: #0d1b12;
     border-bottom: 2.5pt solid #10b981; padding-bottom: 8pt; }
h2 { font-size: 13.5pt; color: #064e3b; margin: 20pt 0 6pt; break-after: avoid; }
h3 { font-size: 11pt; color: #1f2937; margin: 12pt 0 4pt; break-after: avoid; }
p { margin: 4pt 0; }
strong { color: #06281c; }
blockquote { margin: 8pt 0; padding: 7pt 12pt; background: #f0faf5; border-left: 3pt solid #10b981;
             color: #33413a; font-size: 9.5pt; }
blockquote p { margin: 2pt 0; }
table { width: 100%; border-collapse: collapse; margin: 8pt 0; font-size: 9pt; break-inside: avoid; }
th { background: #0d1b12; color: #ecfdf5; text-align: left; padding: 5pt 7pt; font-weight: 600; }
td { border-bottom: 0.5pt solid #d7e2dc; padding: 5pt 7pt; vertical-align: top; }
tr:nth-child(even) td { background: #f6faf8; }
figure { margin: 10pt 0 14pt; text-align: center; break-inside: avoid; }
figure img { max-width: 100%; max-height: 165mm; border: 0.5pt solid #cbd5d1; border-radius: 5pt; }
figcaption { font-size: 8.5pt; color: #5b6b63; margin-top: 4pt; }
ul, ol { margin: 5pt 0 5pt 14pt; padding: 0; }
li { margin: 2.5pt 0; }
code { font: 8.5pt "SF Mono", Menlo, Consolas, monospace; background: #eef3f0; padding: 0.5pt 3pt;
       border-radius: 2pt; }
hr { border: none; border-top: 0.5pt solid #d7e2dc; margin: 12pt 0; }
footer { margin-top: 16pt; border-top: 0.5pt solid #d7e2dc; padding-top: 6pt;
         font-size: 8pt; color: #6b7a72; }
"""


def inline(t: str) -> str:
    t = html.escape(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r'<a href="\2">\1</a>', t)
    return t


def md_to_html(md_text: str) -> str:
    out: list[str] = []
    lines = md_text.splitlines()
    i, n = 0, len(lines)
    while i < n:
        s = lines[i].rstrip()
        if not s.strip():
            i += 1
            continue
        m = re.match(r"^(#{1,4})\s+(.*)", s)
        if m:
            lvl = len(m.group(1))
            out.append(f"<h{lvl}>{inline(m.group(2))}</h{lvl}>")
            i += 1
            continue
        if s.startswith("|") and i + 1 < n and re.match(r"^\s*\|[\s:|-]+\|?\s*$", lines[i + 1]):
            rows = [s]
            i += 2
            while i < n and lines[i].strip().startswith("|"):
                rows.append(lines[i].rstrip())
                i += 1
            head = [c.strip() for c in rows[0].strip("|").split("|")]
            body = [[c.strip() for c in r.strip("|").split("|")] for r in rows[1:]]
            out.append("<table><thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in head)
                       + "</tr></thead><tbody>"
                       + "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body)
                       + "</tbody></table>")
            continue
        m = re.match(r"^!\[([^\]]*)\]\(([^)\s]+)\)", s.strip())
        if m:
            out.append(f'<figure><img src="{html.escape(m.group(2))}" alt="{html.escape(m.group(1))}">'
                       f"<figcaption>{html.escape(m.group(1))}</figcaption></figure>")
            i += 1
            continue
        if s.startswith(">"):
            out.append("<blockquote>" + inline(s.lstrip("> ").strip()) + "</blockquote>")
            i += 1
            continue
        if re.match(r"^[-*]\s+", s.strip()):
            items = []
            while i < n and re.match(r"^[-*]\s+", lines[i].strip()):
                items.append("<li>" + inline(re.sub(r"^[-*]\s+", "", lines[i].strip())) + "</li>")
                i += 1
            out.append("<ul>" + "".join(items) + "</ul>")
            continue
        if re.match(r"^\d+\.\s+", s.strip()):
            items = []
            while i < n and re.match(r"^\d+\.\s+", lines[i].strip()):
                items.append("<li>" + inline(re.sub(r"^\d+\.\s+", "", lines[i].strip())) + "</li>")
                i += 1
            out.append("<ol>" + "".join(items) + "</ol>")
            continue
        if s.strip() in ("---", "***", "___"):
            out.append("<hr>")
            i += 1
            continue
        para = [s.strip()]
        i += 1
        while i < n and lines[i].strip() and not re.match(r"^(#{1,4}\s|\||>|\!\[|[-*]\s|\d+\.\s|---$)", lines[i].strip()):
            para.append(lines[i].strip())
            i += 1
        out.append("<p>" + inline(" ".join(para)) + "</p>")
    return "\n".join(out)


def main() -> None:
    src = pathlib.Path(sys.argv[1]).resolve()
    dst = pathlib.Path(sys.argv[2]).resolve()
    title = sys.argv[3] if len(sys.argv) > 3 else src.stem
    doc = md_to_html(src.read_text(encoding="utf-8"))
    page = (f"<!doctype html><html><head><meta charset='utf-8'><title>{html.escape(title)}</title>"
            f"<style>{CSS}</style></head><body>{doc}"
            f"<footer>CVStart · {html.escape(title)} · собрано агентом «Стратег Фабрики продуктов», 06.11.2026 · "
            f"доказательная база: REPORT.md</footer></body></html>")
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(page)
        tmp_html = f.name
    # base href → картинки по относительным путям от src
    page = page.replace("<head>", f"<head><base href='{src.parent.as_uri()}/'>")
    with open(tmp_html, "w", encoding="utf-8") as f:
        f.write(page)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={dst}", pathlib.Path(tmp_html).as_uri()], check=True,
                   capture_output=True)
    pathlib.Path(tmp_html).unlink(missing_ok=True)
    print(f"PDF: {dst} ({dst.stat().st_size} байт)")


if __name__ == "__main__":
    main()
