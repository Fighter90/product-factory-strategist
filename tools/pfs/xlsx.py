"""Минимальный XLSX-писатель на стандартной библиотеке (zipfile + XML).

Зачем: Excel-приложения к six-pager и роудмапы без сторонних пакетов — сохраняем
принцип «ноль зависимостей». Поддерживает: несколько листов, текст, числа, формулы
(=A1*B2, с необязательным кэшированным значением для предпросмотра), жирный
шрифт, процентный формат и сплошные заливки (стили статусов роудмапа, PRO-70).
Открывается Excel / Numbers / Google Sheets / LibreOffice.
"""
from __future__ import annotations

import os
import re
import tempfile
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

NS_MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
NS_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS_PKG_REL = "http://schemas.openxmlformats.org/package/2006/relationships"

# Заливки статусов роудмапа (PRO-70): палитра Excel «хорошо/нейтрально/плохо» + синий/серый.
STYLE_FILLS = {"green": "FFC6EFCE", "yellow": "FFFFEB9C", "red": "FFC7CE",
               "blue": "FFBDD7EE", "gray": "FFD9D9D9"}


def _fill_style(fill: str, bold: bool) -> int:
    """Индекс стиля заливки: 0–3 заняты базовыми (обычный/жирный/процент/жирный %),
    дальше по 2 комбинации (обычная/жирная) на цвет — базовые книги не меняются."""
    return 4 + list(STYLE_FILLS).index(fill) * 2 + (1 if bold else 0)


def _styles_xml() -> str:
    """styleSheet с базовыми стилями и заливками STYLE_FILLS (индексы 4…3+2·N)."""
    extra_fills = "".join('<fill><patternFill patternType="solid">'
                          f'<fgColor rgb="{rgb}"/><bgColor indexed="64"/></patternFill></fill>'
                          for rgb in STYLE_FILLS.values())
    fill_xfs = "".join(f'<xf fillId="{i + 2}" applyFill="1"/>'
                       f'<xf fillId="{i + 2}" fontId="1" applyFill="1" applyFont="1"/>'
                       for i in range(len(STYLE_FILLS)))
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="{NS_MAIN}">
<numFmts count="1"><numFmt numFmtId="164" formatCode="0.0%"/></numFmts>
<fonts count="2"><font><sz val="11"/><name val="Calibri"/></font><font><b/><sz val="11"/><name val="Calibri"/></font></fonts>
<fills count="{2 + len(STYLE_FILLS)}"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill>{extra_fills}</fills>
<borders count="1"><border/></borders>
<cellStyleXfs count="1"><xf/></cellStyleXfs>
<cellXfs count="{4 + 2 * len(STYLE_FILLS)}"><xf/><xf fontId="1" applyFont="1"/><xf numFmtId="164" applyNumberFormat="1"/><xf fontId="1" numFmtId="164" applyFont="1" applyNumberFormat="1"/>{fill_xfs}</cellXfs>
<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>
</styleSheet>"""


_STYLES = _styles_xml()


def col_letter(n: int) -> str:
    """1 → A, 26 → Z, 27 → AA."""
    out = ""
    while n:
        n, rem = divmod(n - 1, 26)
        out = chr(65 + rem) + out
    return out


def _safe_name(name: str) -> str:
    cleaned = re.sub(r"[\[\]:*?/\\]", " ", name).strip() or "Лист"
    return cleaned[:31]


def _fmt_number(v) -> str:
    return "%.10g" % v


class Sheet:
    """Строки листа. Ячейка: None | str | int/float | dict
    dict: {"v": значение} или {"f": "=формула без =", "cached": число},
    флаги "bold", "pct" (процентный формат), "fill" (имя из STYLE_FILLS:
    green|yellow|red|blue|gray — заливка роудмапа, с "bold" совместима,
    с "pct" не совмещается)."""

    def __init__(self, name: str, widths: dict[int, float] | None = None):
        self.name = _safe_name(name)
        self.rows: list[list] = []
        self.widths = widths or {}

    def row(self, *cells) -> "Sheet":
        self.rows.append(list(cells))
        return self

    def _cell_xml(self, value, row_i: int, col_i: int) -> str:
        ref = f"{col_letter(col_i)}{row_i}"
        if value is None:
            return ""
        bold = pct = False
        formula = cached = fill = None
        if isinstance(value, dict):
            bold, pct = bool(value.get("bold")), bool(value.get("pct"))
            formula, cached, fill = value.get("f"), value.get("cached"), value.get("fill")
            value = value.get("v")
        if fill:
            if fill not in STYLE_FILLS:
                raise ValueError(f"Неизвестная заливка: {fill}; доступные: {', '.join(STYLE_FILLS)}")
            s_attr = f' s="{_fill_style(fill, bold)}"'
        else:
            style = (1 if bold else 0) + (2 if pct else 0)
            s_attr = f' s="{style}"' if style else ""
        if formula is not None:
            f = formula[1:] if formula.startswith("=") else formula
            v = f"<v>{_fmt_number(cached)}</v>" if cached is not None else ""
            return f'<c r="{ref}"{s_attr}><f>{escape(f)}</f>{v}</c>'
        if isinstance(value, (int, float)):
            return f'<c r="{ref}"{s_attr}><v>{_fmt_number(value)}</v></c>'
        if isinstance(value, str) and value.startswith("="):
            return f'<c r="{ref}"{s_attr}><f>{escape(value[1:])}</f></c>'
        text = escape(str(value))
        return f'<c r="{ref}" t="inlineStr"{s_attr}><is><t xml:space="preserve">{text}</t></is></c>'

    def xml(self) -> str:
        rows_xml = []
        for r, cells in enumerate(self.rows, 1):
            inner = "".join(self._cell_xml(v, r, c) for c, v in enumerate(cells, 1))
            rows_xml.append(f'<row r="{r}">{inner}</row>')
        cols = "".join(f'<col min="{c}" max="{c}" width="{w}" customWidth="1"/>'
                       for c, w in sorted(self.widths.items()))
        col_xml = f"<cols>{cols}</cols>" if cols else ""
        return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                f'<worksheet xmlns="{NS_MAIN}">{col_xml}<sheetData>{"".join(rows_xml)}</sheetData></worksheet>')


class Workbook:
    def __init__(self):
        self.sheets: list[Sheet] = []

    def sheet(self, name: str, widths: dict[int, float] | None = None) -> Sheet:
        sh = Sheet(name, widths)
        self.sheets.append(sh)
        return sh

    def save(self, path: Path) -> Path:
        if not self.sheets:
            raise ValueError("Пустая книга: добавьте хотя бы один лист")
        path.parent.mkdir(parents=True, exist_ok=True)
        sheet_tags = "".join(
            f'<sheet name="{escape(s.name)}" sheetId="{i}" r:id="rId{i}"/>'
            for i, s in enumerate(self.sheets, 1))
        n = len(self.sheets)
        rels = "".join(
            f'<Relationship Id="rId{i}" Type="{NS_REL}/worksheet" Target="worksheets/sheet{i}.xml"/>'
            for i in range(1, n + 1))
        rels += f'<Relationship Id="rId{n + 1}" Type="{NS_REL}/styles" Target="styles.xml"/>'
        overrides = "".join(
            f'<Override PartName="/xl/worksheets/sheet{i}.xml" '
            f'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
            for i in range(1, n + 1))
        parts = {
            "[Content_Types].xml":
                '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
                '<Default Extension="xml" ContentType="application/xml"/>'
                '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
                f'{overrides}'
                '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
                '</Types>',
            "_rels/.rels":
                f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                f'<Relationships xmlns="{NS_PKG_REL}">'
                f'<Relationship Id="rId1" Type="{NS_REL}/officeDocument" Target="xl/workbook.xml"/>'
                '</Relationships>',
            "xl/workbook.xml":
                f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                f'<workbook xmlns="{NS_MAIN}" xmlns:r="{NS_REL}"><sheets>{sheet_tags}</sheets></workbook>',
            "xl/_rels/workbook.xml.rels":
                f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                f'<Relationships xmlns="{NS_PKG_REL}">{rels}</Relationships>',
            "xl/styles.xml": _STYLES,
        }
        for i, sh in enumerate(self.sheets, 1):
            parts[f"xl/worksheets/sheet{i}.xml"] = sh.xml()
        # атомарная запись: обрыв посреди сохранения не оставляет битый файл
        fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".tmp-", suffix=".xlsx")
        with os.fdopen(fd, "wb") as fh:
            with zipfile.ZipFile(fh, "w", zipfile.ZIP_DEFLATED) as z:
                for name, content in parts.items():
                    z.writestr(name, content)
        os.chmod(tmp, 0o644)
        os.replace(tmp, path)
        return path


def sheet_names(path: Path) -> list[str]:
    """Имена листов книги (для тестов и проверок)."""
    import re as _re
    with zipfile.ZipFile(path) as z:
        xml = z.read("xl/workbook.xml").decode("utf-8")
    return _re.findall(r'<sheet name="([^"]+)"', xml)
