"""Минимальный DOCX-писатель на стандартной библиотеке: Markdown → Word.

Поддерживает: заголовки H1–H4, абзацы, **жирный**, `код`, маркированные и
нумерованные списки, таблицы, блоки кода, цитаты, изображения `![alt](путь)`
(PNG/JPEG/GIF вшиваются в word/media, ширина отображения до ~600 px; путь
относительно исходного .md). Зачем: docx-версии документации и six-pager
без сторонних пакетов.
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
_R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
_A = "http://schemas.openxmlformats.org/drawingml/2006/main"
_WP = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
_PIC = "http://schemas.openxmlformats.org/drawingml/2006/picture"

_IMG_RE = re.compile(r"^!\[([^\]]*)\]\(([^)\s]+)\)\s*$")
_IMG_CT = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg", "gif": "image/gif"}

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
<w:style w:type="paragraph" w:styleId="FootnoteText"><w:name w:val="footnote text"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:after="40"/></w:pPr><w:rPr><w:sz w:val="18"/></w:rPr></w:style>
<w:style w:type="character" w:styleId="FootnoteReference"><w:name w:val="footnote reference"/><w:rPr><w:vertAlign w:val="superscript"/></w:rPr></w:style>
</w:styles>""" % _W


_FN_REF_RE = re.compile(r"\[\^(\d+)\]")           # ссылка на сноску в тексте: [^1]
_FN_DEF_RE = re.compile(r"\[\^(\d+)\]:\s*(.*)$")  # определение сноски: [^1]: текст


def _fn_ref_run(fid: str) -> str:
    return (f'<w:r><w:rPr><w:rStyle w:val="FootnoteReference"/></w:rPr>'
            f'<w:footnoteReference w:id="{fid}"/></w:r>')


def _runs(text: str, fn_ids: set[int] | None = None) -> str:
    """Абзацный текст с **жирным**, `кодом` и сносками [^N] → набор w:r.
    fn_ids — номера определённых в документе сносок: только они становятся
    w:footnoteReference (PRO-49); без набора или для неизвестного номера маркер
    остаётся литеральным текстом — ссылка на несуществующую сноску делает DOCX
    невалидным (Word предлагает «восстановить»)."""
    out = []
    for part in re.split(r"(\*\*.+?\*\*|`[^`]+`|\[\^\d+\])", text):
        if not part:
            continue
        m_fn = _FN_REF_RE.fullmatch(part)
        if m_fn and fn_ids is not None and int(m_fn.group(1)) in fn_ids:
            out.append(_fn_ref_run(m_fn.group(1)))
        elif part.startswith("**") and part.endswith("**") and len(part) > 4:
            out.append(f'<w:r><w:rPr><w:b/></w:rPr><w:t xml:space="preserve">{escape(part[2:-2])}</w:t></w:r>')
        elif part.startswith("`") and part.endswith("`") and len(part) > 2:
            out.append(f'<w:r><w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/>'
                       f'<w:shd w:val="clear" w:fill="F2F2F2"/></w:rPr>'
                       f'<w:t xml:space="preserve">{escape(part[1:-1])}</w:t></w:r>')
        else:
            out.append(f'<w:r><w:t xml:space="preserve">{escape(part)}</w:t></w:r>')
    return "".join(out)


def _p(text: str, style: str | None = None, fn_ids: set[int] | None = None) -> str:
    ppr = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>' if style else ""
    return f"<w:p>{ppr}{_runs(text, fn_ids)}</w:p>"


def _dims(data: bytes, ext: str) -> tuple[int, int]:
    """(ширина, высота) изображения в пикселях из байтов PNG/JPEG/GIF."""
    if ext == "png" and data[:8] == b"\x89PNG\r\n\x1a\n" and len(data) >= 24:
        return int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")
    if ext == "gif" and data[:6] in (b"GIF87a", b"GIF89a") and len(data) >= 10:
        return int.from_bytes(data[6:8], "little"), int.from_bytes(data[8:10], "little")
    if ext in ("jpg", "jpeg") and data[:2] == b"\xff\xd8":
        i = 2
        while i + 9 < len(data):
            if data[i] != 0xFF:
                i += 1
                continue
            marker = data[i + 1]
            if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
                i += 2
                continue
            seg = int.from_bytes(data[i + 2:i + 4], "big")
            if seg < 2:
                break
            if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
                h = int.from_bytes(data[i + 5:i + 7], "big")
                w = int.from_bytes(data[i + 7:i + 9], "big")
                return w, h
            i += 2 + seg
    return 0, 0


def _drawing(rid: str, doc_id: int, cx: int, cy: int) -> str:
    """Абзац с инлайн-изображением (EMU = px × 9525 при 96 dpi)."""
    return (f'<w:p><w:pPr><w:keepNext/><w:jc w:val="center"/></w:pPr><w:r><w:drawing>'
            f'<wp:inline distT="0" distB="0" distL="0" distR="0" xmlns:wp="{_WP}">'
            f'<wp:extent cx="{cx}" cy="{cy}"/><wp:effectExtent l="0" t="0" r="0" b="0"/>'
            f'<wp:docPr id="{doc_id}" name="Picture {doc_id}"/>'
            f'<wp:cNvGraphicFramePr><a:graphicFrameLocks xmlns:a="{_A}" noChangeAspect="1"/>'
            f"</wp:cNvGraphicFramePr>"
            f'<a:graphic xmlns:a="{_A}"><a:graphicData uri="{_PIC}">'
            f'<pic:pic xmlns:pic="{_PIC}"><pic:nvPicPr>'
            f'<pic:cNvPr id="{doc_id}" name="Picture {doc_id}"/><pic:cNvPicPr/></pic:nvPicPr>'
            f'<pic:blipFill><a:blip xmlns:r="{_R}" r:embed="{rid}"/>'
            f"<a:stretch><a:fillRect/></a:stretch></pic:blipFill>"
            f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
            f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
            f"</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>")


def _tbl(rows: list[list[str]], fn_ids: set[int] | None = None) -> str:
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
                tcs.append(f"<w:tc><w:tcPr/><w:p>{_runs(cell, fn_ids)}</w:p></w:tc>")
        trs.append(f"<w:tr>{''.join(tcs)}</w:tr>")
    borders = "<w:tblBorders>" + "".join(
        f'<w:{side} w:val="single" w:sz="4" w:color="BFBFBF"/>'
        for side in ("top", "left", "bottom", "right", "insideH", "insideV")) + "</w:tblBorders>"
    return (f'<w:tbl><w:tblPr><w:tblW w:w="5000" w:type="pct"/>{borders}</w:tblPr>'
            f"<w:tblGrid>{grid}</w:tblGrid>{''.join(trs)}</w:tbl>")


def _footnotes_xml(footnotes: list[tuple[int, str]]) -> str:
    """word/footnotes.xml: разделители + сноски как настоящие footnotes Word (PRO-49).
    id сноски = номер из markdown-определения [^N]: текст."""
    items = ['<w:footnote w:type="separator" w:id="-1"><w:p><w:r><w:separator/></w:r></w:p></w:footnote>',
             '<w:footnote w:type="continuationSeparator" w:id="0">'
             "<w:p><w:r><w:continuationSeparator/></w:r></w:p></w:footnote>"]
    for fid, text in footnotes:
        items.append(f'<w:footnote w:id="{fid}">'
                     f'<w:p><w:pPr><w:pStyle w:val="FootnoteText"/></w:pPr>'
                     f'<w:r><w:rPr><w:rStyle w:val="FootnoteReference"/></w:rPr><w:footnoteRef/></w:r>'
                     # текст сноски — через инлайн-форматтер тела: «**S001**» из
                     # _footnote_line становится жирным w:b-run, а не литеральными «**»
                     f'<w:r><w:t xml:space="preserve"> </w:t></w:r>'
                     f"{_runs(text)}</w:p></w:footnote>")
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            f"<w:footnotes {_W}>{''.join(items)}</w:footnotes>")


def md_to_docx_xml(md_text: str, base_dir: Path | None = None,
                   media: list[tuple[str, bytes]] | None = None,
                   footnotes: list[tuple[int, str]] | None = None) -> str:
    """Markdown → XML тела документа (word/document.xml).

    media — список, куда складываются (имя_файла, байты) найденных изображений;
    save() вшивает их в word/media и прописывает связи.
    footnotes — список, куда складываются (id, текст) сносок из определений [^N]:
    текст; save() собирает из них word/footnotes.xml (PRO-49), строки определений
    в тело документа не попадают. Сбор двухпроходный: сначала все определения
    (дедуп — первое определение побеждает), затем ссылки [^N] становятся
    w:footnoteReference только для определённых номеров; ссылка без определения
    остаётся литеральным текстом (иначе невалидный DOCX). Без footnotes-коллектора
    ссылки не эмиттятся вовсе — footnotes.xml никто не соберёт.
    """
    body: list[str] = []
    media = media if media is not None else []
    lines = md_text.splitlines()
    defs: dict[int, str] = {}
    for ln in lines:  # проход 1: все определения, до любой ссылки в тексте
        m_fn = _FN_DEF_RE.match(ln.strip())
        if m_fn:
            defs.setdefault(int(m_fn.group(1)), m_fn.group(2).strip())
    fn_ids: set[int] | None = set(defs) if footnotes is not None else None
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
        if _FN_DEF_RE.match(s):  # определение [^N]: собрано проходом 1 → word/footnotes.xml, из тела прочь
            i += 1
            continue
        m_img = _IMG_RE.match(s)
        if m_img:
            src = Path(m_img.group(2))
            if base_dir is not None and not src.is_absolute():
                src = base_dir / src
            data = src.read_bytes() if src.is_file() else b""
            if data:
                ext = src.suffix.lstrip(".").lower()
                media.append((f"image_{len(media) + 1}.{ext or 'png'}", data))
                w_px, h_px = _dims(data, ext)
                w_px = w_px or 600
                h_px = h_px or max(1, round(w_px * 0.6))
                scale = min(1.0, 600 / w_px)
                cx, cy = int(w_px * scale * 9525), int(h_px * scale * 9525)
                body.append(_drawing(f"rId{len(media) + 10}", len(media), cx, cy))
            else:
                body.append(_p(m_img.group(1) or m_img.group(2), fn_ids=fn_ids))
            i += 1
            continue
        m = re.match(r"^(#{1,4})\s+(.*)", s)
        if m:
            body.append(_p(m.group(2), f"Heading{len(m.group(1))}", fn_ids=fn_ids))
            i += 1
            continue
        if s.startswith("|") and i + 1 < n and re.match(r"^\s*\|[\s:|-]+\|?\s*$", lines[i + 1]):
            rows = [[c.strip() for c in s.strip("|").split("|")]]
            i += 2
            while i < n and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            body.append(_tbl(rows, fn_ids))
            continue
        if s.startswith(">"):
            body.append(f'<w:p><w:pPr><w:pStyle w:val="Quote"/></w:pPr>{_runs(s.lstrip("> "), fn_ids)}</w:p>')
            i += 1
            continue
        if re.match(r"^[-*•]\s+", s):
            body.append(_p("• " + re.sub(r"^[-*•]\s+", "", s), fn_ids=fn_ids))
            i += 1
            continue
        if not s or s in ("---", "***", "___"):
            i += 1
            continue
        body.append(_p(s, fn_ids=fn_ids))
        i += 1
    if footnotes is not None:
        footnotes.extend(defs.items())  # порядок первого определения; дубли уже отброшены
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            f'<w:document {_W}><w:body>{"".join(body)}'
            '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
            '<w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134"/>'
            "</w:sectPr></w:body></w:document>")


def save(path: Path, md_text: str, base_dir: Path | None = None) -> Path:
    """Собрать .docx из markdown-текста (атомарно, без зависимостей).

    base_dir — каталог для разрешения относительных путей изображений.
    Сноски [^N] в тексте и определения [^N]: текст собираются в word/footnotes.xml
    (настоящие footnotes Word, PRO-49); без сносок часть не создаётся. Ссылка [^N]
    без определения остаётся литеральным текстом — невалидных ссылок на
    несуществующие сноски не возникает; повторные определения дедуплицируются.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    media: list[tuple[str, bytes]] = []
    footnotes: list[tuple[int, str]] = []
    doc_xml = md_to_docx_xml(md_text, base_dir=base_dir, media=media, footnotes=footnotes)
    exts = sorted({n.rsplit(".", 1)[1] for n, _ in media})
    parts = {
        "[Content_Types].xml":
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.'
            'wordprocessingml.document.main+xml"/>'
            '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.'
            'wordprocessingml.styles+xml"/>'
            + (f'<Override PartName="/word/footnotes.xml" ContentType="application/vnd.openxmlformats-officedocument.'
               f'wordprocessingml.footnotes+xml"/>' if footnotes else "")
            + "".join(f'<Default Extension="{e}" ContentType="{_IMG_CT[e]}"/>' for e in exts) + "</Types>",
        "_rels/.rels":
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            f'<Relationship Id="rId1" Type="{_R}/'
            'officeDocument" Target="word/document.xml"/></Relationships>',
        "word/document.xml": doc_xml,
        "word/styles.xml": _STYLES,
        "word/_rels/document.xml.rels":
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            + (f'<Relationship Id="rId9" Type="{_R}/footnotes" Target="footnotes.xml"/>' if footnotes else "")
            + "".join(f'<Relationship Id="rId{idx + 10}" Type="{_R}/image" Target="media/{name}"/>'
                      for idx, (name, _) in enumerate(media, 1))
            + "</Relationships>",
    }
    if footnotes:
        parts["word/footnotes.xml"] = _footnotes_xml(footnotes)
    for name, data in media:
        parts[f"word/media/{name}"] = data
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
    return save(out, md_path.read_text(encoding="utf-8"), base_dir=md_path.parent)
