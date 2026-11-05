"""Минимальный DOCX-писатель на стандартной библиотеке: Markdown → Word.

Поддерживает: заголовки H1–H4, абзацы, **жирный**, `код`, маркированные и
нумерованные списки, таблицы, блоки кода, цитаты. Картинки и диаграммы не
переносятся. Зачем: docx-версии документации (HELP, README) без сторонних пакетов.
Запуск: pfs docx <файл.md> [--out файл.docx]
"""
from __future__ import annotations

import os
import re
import tempfile
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

_W = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'

_STYLES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles %s>
<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:sz w:val="22"/></w:rPr></w:rPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:styleId="Normal" w:default="1"><w:name w:val="Normal"/><w:pPr><w:spacing w:after="120"/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:pPr><w:keepNext/><w:spacing w:before="280" w:after="160"/><w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:b/><w:sz w:val="32"/><w:color w:val="1F3864"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:pPr><w:keepNext/><w:spacing w:before="240" w:after="120"/><w:outlineLvl w:val="1"/></w:pPr><w:rPr><w:b/><w:sz w:val="27"/><w:color w:val="2E5496"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/><w:basedOn w:val="Normal"/><w:pPr><w:keepNext/><w:spacing w:before="200" w:after="100"/><w:outlineLvl w:val="2"/></w:pPr><w:rPr><w:b/><w:sz w:val="24"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading4"><w:name w:val="heading 4"/><w:basedOn w:val="Normal"/><w:pPr><w:keepNext/><w:outlineLvl w:val="3"/></w:pPr><w:rPr><w:b/><w:i/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="CodeBlock"><w:name w:val="Code Block"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:after="0"/><w:shd w:val="clear" w:fill="F2F2F2"/></w:pPr><w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/><w:sz w:val="18"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Quote"><w:name w:val="Quote"/><w:basedOn w:val="Normal"/><w:pPr><w:ind w:left="400"/><w:shd w:val="clear" w:fill="EEF3FA"/></w:pPr><w:rPr><w:i/><w:color w:val="404040"/></w:rPr></w:style>
</w:styles>""" % _W


def _runs(text: str) -> str:
    """Абзацный текст с **жирным** и `кодом` → набор w:r."""
    out = []
    for part in re.split(r"(\*\*.+?\*\*|`[^`]+`)", text):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**") and len(part) > 4:
            out.append(f'<w:r><w:rPr><w:b/></w:rPr><w:t xml:space="preserve">{escape(part[2:-2])}</w:t></w:r>')
        elif part.startswith("`") and part.endswith("`") and len(part) > 2:
            out.append(f'<w:r><w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/>'
                       f'<w:shd w:val="clear" w:fill="F2F2F2"/></w:rPr>'
                       f'<w:t xml:space="preserve">{escape(part[1:-1])}</w:t></w:r>')
        else:
            out.append(f'<w:r><w:t xml:space="preserve">{escape(part)}</w:t></w:r>')
    return "".join(out)


def _p(text: str, style: str | None = None) -> str:
    ppr = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>' if style else ""
    return f"<w:p>{ppr}{_runs(text)}</w:p>"


def _tbl(rows: list[list[str]]) -> str:
    cols = max(len(r) for r in rows)
    grid = "<w:gridCol/>" * cols
    trs = []
    for ri, row in enumerate(rows):
        tcs = []
        for cell in (row + [""] * (cols - len(row)))[:cols]:
            if ri == 0:
                run = f'<w:r><w:rPr><w:b/></w:rPr><w:t xml:space="preserve">{escape(cell)}</w:t></w:r>'
                tcs.append(f"<w:tc><w:tcPr/><w:p>{run}</w:p></w:tc>")
            else:
                tcs.append(f"<w:tc><w:tcPr/><w:p>{_runs(cell)}</w:p></w:tc>")
        trs.append(f"<w:tr>{''.join(tcs)}</w:tr>")
    borders = "<w:tblBorders>" + "".join(
        f'<w:{side} w:val="single" w:sz="4" w:color="BFBFBF"/>'
        for side in ("top", "left", "bottom", "right", "insideH", "insideV")) + "</w:tblBorders>"
    return (f'<w:tbl><w:tblPr><w:tblW w:w="5000" w:type="pct"/>{borders}</w:tblPr>'
            f"<w:tblGrid>{grid}</w:tblGrid>{''.join(trs)}</w:tbl>")


def md_to_docx_xml(md_text: str) -> str:
    """Markdown → XML тела документа (word/document.xml)."""
    body: list[str] = []
    lines = md_text.splitlines()
    i, n = 0, len(lines)
    while i < n:
        s = lines[i].strip()
        if s.startswith("```"):
            i += 1
            while i < n and not lines[i].strip().startswith("```"):
                body.append(f'<w:p><w:pPr><w:pStyle w:val="CodeBlock"/></w:pPr>'
                            f'<w:r><w:t xml:space="preserve">{escape(lines[i])}</w:t></w:r></w:p>')
                i += 1
            i += 1
            continue
        m = re.match(r"^(#{1,4})\s+(.*)", s)
        if m:
            body.append(_p(m.group(2), f"Heading{len(m.group(1))}"))
            i += 1
            continue
        if s.startswith("|") and i + 1 < n and re.match(r"^\s*\|[\s:|-]+\|?\s*$", lines[i + 1]):
            rows = [[c.strip() for c in s.strip("|").split("|")]]
            i += 2
            while i < n and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            body.append(_tbl(rows))
            continue
        if s.startswith(">"):
            body.append(f'<w:p><w:pPr><w:pStyle w:val="Quote"/></w:pPr>{_runs(s.lstrip("> "))}</w:p>')
            i += 1
            continue
        if re.match(r"^[-*•]\s+", s):
            body.append(_p("• " + re.sub(r"^[-*•]\s+", "", s)))
            i += 1
            continue
        if not s or s in ("---", "***", "___"):
            i += 1
            continue
        body.append(_p(s))
        i += 1
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            f'<w:document {_W}><w:body>{"".join(body)}'
            '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
            '<w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134"/>'
            "</w:sectPr></w:body></w:document>")


def save(path: Path, md_text: str) -> Path:
    """Собрать .docx из markdown-текста (атомарно, без зависимостей)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    parts = {
        "[Content_Types].xml":
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.'
            'wordprocessingml.document.main+xml"/>'
            '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.'
            'wordprocessingml.styles+xml"/></Types>',
        "_rels/.rels":
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/'
            'officeDocument" Target="word/document.xml"/></Relationships>',
        "word/document.xml": md_to_docx_xml(md_text),
        "word/styles.xml": _STYLES,
        "word/_rels/document.xml.rels":
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"/></Relationships>',
    }
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".tmp-", suffix=".docx")
    with os.fdopen(fd, "wb") as fh:
        with zipfile.ZipFile(fh, "w", zipfile.ZIP_DEFLATED) as z:
            for name, content in parts.items():
                z.writestr(name, content)
    os.chmod(tmp, 0o644)
    os.replace(tmp, path)
    return path


def convert(md_path: Path, out: Path | None = None) -> Path:
    """Конвертировать .md файл в .docx (по умолчанию рядом, с суффиксом .docx)."""
    out = out or md_path.with_suffix(".docx")
    return save(out, md_path.read_text(encoding="utf-8"))
