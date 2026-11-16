"""Извлечение текста из сайтов, PDF, DOCX, XLSX, CSV, Markdown. Только stdlib (+ pdftotext/pypdf, если есть)."""
from __future__ import annotations

import csv
import io
import ipaddress
import re
import socket
import shutil
import ssl
import subprocess
import sys
import time
import urllib.request
import urllib.error
import zipfile
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
from xml.etree import ElementTree as ET

from .core import PfsError

UA = "Mozilla/5.0 (compatible; pfs-research-agent/0.1; +https://github.com/Fighter90/product-factory-strategist-agent)"


# ---------- PRO-59: цепочка доверия TLS ----------

def build_ssl_context() -> ssl.SSLContext:
    """TLS-контекст с максимальной цепочкой доверия (PRO-59); проверка сертификатов не отключается никогда:
    1) хранилище по умолчанию — учитывает SSL_CERT_FILE/SSL_CERT_DIR;
    2) + certifi, если установлен (питон с python.org на macOS без «Install Certificates.command»);
    3) системное хранилище через truststore, если certifi нет, а хранилище по умолчанию пусто.
    """
    ctx = ssl.create_default_context()  # SSL_CERT_FILE/SSL_CERT_DIR учитываются сами
    try:
        import certifi  # type: ignore
        ctx.load_verify_locations(certifi.where())
    except ImportError:
        pass
    if not ctx.get_ca_certs():  # корневых сертификатов нет — пробуем системное хранилище через truststore
        try:
            import truststore  # type: ignore
            ctx = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        except ImportError:
            pass
    return ctx


def cert_fix_hint() -> str:
    """Готовая команда исправления отсутствующих корневых сертификатов (PRO-59)."""
    hint = (f"Python не доверяет корневым сертификатам — TLS-проверка не отключается. "
            f"Готовое исправление: {sys.executable} -m pip install certifi")
    if sys.platform == "darwin":
        hint += "; на macOS также: «Install Certificates.command» из /Applications/Python <версия>/"
    return hint


def is_cert_error(exc: Exception) -> bool:
    """CERTIFICATE_VERIFY_FAILED — напрямую или обёрнутым (URLError → SSLError)."""
    reason = getattr(exc, "reason", None)
    return (isinstance(exc, ssl.SSLCertVerificationError) or isinstance(reason, ssl.SSLCertVerificationError)
            or "CERTIFICATE_VERIFY_FAILED" in str(exc))


def _opener() -> urllib.request.OpenerDirector:
    """Opener с безопасными редиректами и TLS-контекстом из build_ssl_context (PRO-59)."""
    return urllib.request.build_opener(_SafeRedirect, urllib.request.HTTPSHandler(context=build_ssl_context()))


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


def fetch_url(url: str, timeout: int = 30, max_bytes: int = 20_000_000, attempts: int = 3) -> tuple[bytes, str]:
    """Загрузка с повторами: до 3 попыток с паузами 1с/2с при сетевых сбоях (URLError/OSError/таймаут)
    и HTTP 429/5xx. SSRF-проверка выполняется до запросов; при неудаче — прежнее сообщение об ошибке.
    TLS-контекст — из build_ssl_context (PRO-59): certifi → truststore → SSL_CERT_FILE, без отключения проверки."""
    assert_public_url(url)
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "ru,en;q=0.8"})
    opener = _opener()
    last: Exception | None = None
    for attempt in range(attempts):
        try:
            with opener.open(req, timeout=timeout) as resp:  # noqa: S310 — адрес проверен assert_public_url
                return resp.read(max_bytes), resp.headers.get_content_type() or ""
        except PfsError:
            raise
        except Exception as exc:  # сеть недоступна, 429/5xx, таймаут — повторяем; прочее сообщаем явно, не молчим
            last = exc
            if isinstance(exc, urllib.error.HTTPError):
                retry = exc.code == 429 or exc.code >= 500
            else:
                retry = isinstance(exc, OSError)  # URLError/OSError/таймаут — сеть
            if not retry or attempt == attempts - 1:
                break
            time.sleep(2 ** attempt)  # 1с, 2с
    tail = cert_fix_hint() if last is not None and is_cert_error(last) else \
        "Сохраните страницу вручную или передайте текст через --text-file"
    raise PfsError(f"Не удалось загрузить {url}: {last}. {tail}") from last


def fetch_via_browser(url: str, timeout_ms: int = 45_000) -> str:
    """Отрендерить JS-страницу через Playwright (если установлен) и вернуть HTML (PRO-59).
    Playwright — опциональная зависимость: нет — PfsError с командой установки и фолбэком --excerpt.
    SSRF-проверка та же, что у fetch_url."""
    assert_public_url(url)
    try:
        from playwright.sync_api import sync_playwright  # type: ignore
    except ImportError as exc:
        raise PfsError(f"Playwright не установлен — JS-страницу из среды не отрендерить. "
                       f"Установка: {sys.executable} -m pip install playwright && {sys.executable} -m playwright install chromium; "
                       "либо сохраните текст вручную: pfs source add --text-file <файл> --url <ссылка> --excerpt") from exc
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            try:
                page = browser.new_page(user_agent=UA)
                page.goto(url, timeout=timeout_ms, wait_until="domcontentloaded")
                try:  # networkidle не всегда наступает (маятники аналитики) — берём то, что уже отрендерилось
                    page.wait_for_load_state("networkidle", timeout=15_000)
                except Exception:
                    pass
                html = page.content()
            finally:
                browser.close()
        return html
    except PfsError:
        raise
    except Exception as exc:
        raise PfsError(f"Браузерный рендер {url} не удался: {exc}. Сохраните текст вручную: "
                       "pfs source add --text-file <файл> --url <ссылка> --excerpt") from exc


# ---------- PRO-59: HTTPS-проверка окружения для pfs doctor ----------

HTTPS_PROBE_URLS = ("https://pypi.org/simple/", "https://www.python.org/", "https://example.com/")


def https_get(url: str, timeout: int = 6) -> str:
    """Статус HTTPS-ответа: ok | http <код> | ssl | net (PRO-59, pfs doctor).
    Любой HTTP-ответ — TLS-рукопожатие прошло, сертификаты в порядке."""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=build_ssl_context()) as resp:  # noqa: S310
            return "ok" if getattr(resp, "status", 200) < 400 else f"http {resp.status}"
    except urllib.error.HTTPError as exc:
        return f"http {exc.code}"
    except Exception as exc:
        if isinstance(exc, ssl.SSLError) or isinstance(getattr(exc, "reason", None), ssl.SSLError) \
                or is_cert_error(exc):
            return "ssl"
        return "net"


def https_probe(urls: tuple[str, ...] = HTTPS_PROBE_URLS, timeout: int = 6, get=None) -> list[tuple[str, str]]:
    """HTTPS-проверка окружения для pfs doctor (PRO-59): 2–3 домена через текущую TLS-цепочку.
    Возвращает [(домен, статус)] — ok | http <код> | ssl | net; ssl = нужен Install Certificates.command."""
    get = get or https_get
    return [((urlparse(u).hostname or u), get(u, timeout)) for u in urls]


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


MAX_XML_PART = 50_000_000  # байт после распаковки: защита от zip-бомб


def _safe_xml(z: zipfile.ZipFile, name: str):
    """Безопасный разбор части OOXML: без DTD/ENTITY (billion laughs, XXE) и с лимитом размера."""
    if z.getinfo(name).file_size > MAX_XML_PART:
        raise PfsError(f"Часть {name} больше {MAX_XML_PART // 1_000_000} МБ после распаковки — файл отклонён")
    raw = z.read(name)
    head = raw.upper()
    if b"<!DOCTYPE" in head or b"<!ENTITY" in head:
        raise PfsError(f"Часть {name} содержит DTD/ENTITY — такие документы не обрабатываются")
    return ET.fromstring(raw)


W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
S = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"


def docx_to_text(path: Path) -> str:
    with zipfile.ZipFile(path) as z:
        root = _safe_xml(z, "word/document.xml")
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
            for si in _safe_xml(z, "xl/sharedStrings.xml").iter(S + "si"):
                shared.append("".join(t.text or "" for t in si.iter(S + "t")))
        wb = _safe_xml(z, "xl/workbook.xml")
        rels = _safe_xml(z, "xl/_rels/workbook.xml.rels")
        rmap = {r.get("Id"): r.get("Target") for r in rels}
        sheets = {}
        for sh in wb.iter(S + "sheet"):
            rid = sh.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
            target = rmap.get(rid, "")
            target = target.lstrip("/")
            target = target if target.startswith("xl/") else "xl/" + target
            rows = []
            for row in _safe_xml(z, target).iter(S + "row"):
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
