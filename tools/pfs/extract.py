"""Извлечение текста из сайтов, PDF, DOCX, XLSX, CSV, Markdown. Только stdlib (+ pdftotext/pypdf, если есть)."""
from __future__ import annotations

import csv
import io
import ipaddress
import re
import socket
import shutil
import subprocess
import urllib.request
import zipfile
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree as ET

from .core import PfsError

UA = "Mozilla/5.0 (compatible; pfs-research-agent/0.1; +https://github.com/Fighter90/product-factory-strategist)"


class _HTMLText(HTMLParser):
    SKIP = {"script", "style", "noscript", "svg", "head", "nav", "footer", "form"}
    BLOCK = {"p", "div", "br", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6", "section", "article", "table"}

    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.skip = 0
        self.title = ""
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skip += 1
        if tag == "title":
            self._in_title = True
        if tag in self.BLOCK:
            self.parts.append("\n")
        if tag in ("h1", "h2", "h3"):
            self.parts.append("#" * int(tag[1]) + " ")
        if tag == "li":
            self.parts.append("- ")

    def handle_endtag(self, tag):
        if tag in self.SKIP and self.skip:
            self.skip -= 1
        if tag == "title":
            self._in_title = False
        if tag in ("td", "th"):
            self.parts.append(" | ")

    def handle_data(self, data):
        if self._in_title:
            self.title += data.strip()
        if not self.skip:
            self.parts.append(data)


def html_to_text(html: str) -> tuple[str, str]:
    p = _HTMLText()
    p.feed(html)
    text = "".join(p.parts)
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    return p.title, text.strip()


def assert_public_url(url: str) -> None:
    """Защита от SSRF: только http(s) и только публичные адреса (каждый резолв хоста)."""
    from urllib.parse import urlparse
    if not re.match(r"^https?://", url, re.IGNORECASE):
        raise PfsError("Поддерживаются только http(s)-ссылки")
    host = (urlparse(url).hostname or "").rstrip(".").lower()
    if not host or host == "localhost" or host.endswith(".localhost") or host.endswith(".local"):
        raise PfsError(f"Адрес {host or url} не публичный — загрузка запрещена")
    try:
        infos = socket.getaddrinfo(host, None)
    except socket.gaierror as exc:
        raise PfsError(f"Не удалось разрешить имя {host}: {exc}") from exc
    for info in infos:
        ip = ipaddress.ip_address(info[4][0])
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast or ip.is_unspecified:
            raise PfsError(f"{host} указывает на непубличный адрес {ip} — загрузка запрещена")


class _SafeRedirect(urllib.request.HTTPRedirectHandler):
    """Каждый редирект проверяется так же, как исходная ссылка."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        assert_public_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch_url(url: str, timeout: int = 30, max_bytes: int = 20_000_000) -> tuple[bytes, str]:
    assert_public_url(url)
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "ru,en;q=0.8"})
    opener = urllib.request.build_opener(_SafeRedirect)
    try:
        with opener.open(req, timeout=timeout) as resp:  # noqa: S310 — адрес проверен assert_public_url
            return resp.read(max_bytes), resp.headers.get_content_type() or ""
    except PfsError:
        raise
    except Exception as exc:  # сеть недоступна, 403, таймаут — сообщаем явно, не молчим
        raise PfsError(f"Не удалось загрузить {url}: {exc}. Сохраните страницу вручную или передайте текст через --text-file") from exc


def pdf_to_text(path: Path) -> str:
    if shutil.which("pdftotext"):
        res = subprocess.run(["pdftotext", "-layout", str(path), "-"], capture_output=True, text=True, timeout=120)
        if res.returncode == 0 and res.stdout.strip():
            return res.stdout
    try:
        import pypdf  # type: ignore
    except ImportError as exc:
        raise PfsError("Для PDF нужен pdftotext (brew install poppler / apt install poppler-utils) или pip install pypdf") from exc
    reader = pypdf.PdfReader(str(path))
    return "\n\n".join(f"[стр. {i + 1}]\n{page.extract_text() or ''}" for i, page in enumerate(reader.pages))


W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
S = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"


def docx_to_text(path: Path) -> str:
    with zipfile.ZipFile(path) as z:
        root = ET.fromstring(z.read("word/document.xml"))
    paras = []
    for p in root.iter(W + "p"):
        txt = "".join(t.text or "" for t in p.iter(W + "t"))
        style = p.find(f"{W}pPr/{W}pStyle")
        if style is not None and "Heading" in (style.get(W + "val") or ""):
            txt = "## " + txt
        if txt.strip():
            paras.append(txt)
    return "\n\n".join(paras)


def _col_index(ref: str) -> int:
    letters = re.match(r"[A-Z]+", ref).group(0)
    n = 0
    for ch in letters:
        n = n * 26 + ord(ch) - 64
    return n - 1


def xlsx_rows(path: Path) -> dict[str, list[list[str]]]:
    """Возвращает {лист: строки} без внешних библиотек."""
    with zipfile.ZipFile(path) as z:
        shared = []
        if "xl/sharedStrings.xml" in z.namelist():
            for si in ET.fromstring(z.read("xl/sharedStrings.xml")).iter(S + "si"):
                shared.append("".join(t.text or "" for t in si.iter(S + "t")))
        wb = ET.fromstring(z.read("xl/workbook.xml"))
        rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        rmap = {r.get("Id"): r.get("Target") for r in rels}
        sheets = {}
        for sh in wb.iter(S + "sheet"):
            rid = sh.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
            target = rmap.get(rid, "")
            target = target.lstrip("/")
            target = target if target.startswith("xl/") else "xl/" + target
            rows = []
            for row in ET.fromstring(z.read(target)).iter(S + "row"):
                vals: dict[int, str] = {}
                for c in row.iter(S + "c"):
                    v = c.find(S + "v")
                    t = c.get("t")
                    if t == "inlineStr":
                        val = "".join(x.text or "" for x in c.iter(S + "t"))
                    elif v is None:
                        continue
                    elif t == "s":
                        val = shared[int(v.text)]
                    else:
                        val = v.text or ""
                    vals[_col_index(c.get("r", "A1"))] = val
                if vals:
                    rows.append([vals.get(i, "") for i in range(max(vals) + 1)])
            sheets[sh.get("name")] = rows
    return sheets


def rows_to_md(rows: list[list[str]], limit: int = 500) -> str:
    if not rows:
        return "(пусто)"
    width = max(len(r) for r in rows)
    norm = [[(c or "").replace("|", "/").replace("\n", " ") for c in r] + [""] * (width - len(r)) for r in rows[:limit]]
    out = ["| " + " | ".join(norm[0]) + " |", "|" + "---|" * width]
    out += ["| " + " | ".join(r) + " |" for r in norm[1:]]
    if len(rows) > limit:
        out.append(f"\n… ещё {len(rows) - limit} строк в исходном файле")
    return "\n".join(out)


def file_to_text(path: Path) -> tuple[str, str]:
    """(тип, текст) для локального файла."""
    ext = path.suffix.lower()
    if ext == ".pdf":
        return "pdf", pdf_to_text(path)
    if ext == ".docx":
        return "docx", docx_to_text(path)
    if ext in (".xlsx", ".xlsm"):
        sheets = xlsx_rows(path)
        return "xlsx", "\n\n".join(f"## Лист: {n}\n\n{rows_to_md(r)}" for n, r in sheets.items())
    if ext in (".csv", ".tsv"):
        raw = path.read_text(encoding="utf-8-sig", errors="replace")
        dialect = csv.excel_tab if ext == ".tsv" else csv.Sniffer().sniff(raw[:4096], delimiters=",;\t")
        return "table", rows_to_md(list(csv.reader(io.StringIO(raw), dialect)))
    if ext in (".html", ".htm"):
        title, text = html_to_text(path.read_text(encoding="utf-8", errors="replace"))
        return "html", (f"# {title}\n\n" if title else "") + text
    if ext in (".md", ".txt", ".json", ".vtt", ".srt"):
        return "text", path.read_text(encoding="utf-8", errors="replace")
    if ext in (".png", ".jpg", ".jpeg", ".gif", ".webp", ".mp3", ".mp4", ".wav", ".m4a", ".mov"):
        return "media", (f"[Медиафайл {path.name}. Текст не извлекается автоматически: агент описывает только то, "
                         f"что видит/слышит (мультимодальная модель или расшифровка), и добавляет описание через --text-file]")
    raise PfsError(f"Формат {ext} не поддерживается. Поддерживаются: pdf, docx, xlsx, csv, tsv, html, md, txt, изображения/аудио/видео (как медиа)")
