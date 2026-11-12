# -*- coding: utf-8 -*-
"""
Gerador do MAN-PYQT6-001 em OOXML puro (WordprocessingML).

- Titulos 1-4 com numeracao multinivel VINCULADA AOS ESTILOS (novos titulos
  criados no Word numeram sozinhos).
- Legendas com campos reais: STYLEREF 1 \\s + SEQ <rotulo> \\s 1  (Figura 3.2).
- Sumario e listas (figuras, tabelas, listagens) como campos TOC reais, com
  entradas pre-calculadas (hyperlink + PAGEREF) para exibicao imediata.
- settings.xml com updateFields=true: o Word atualiza todos os campos ao abrir.

Uso: python build.py <saida.docx> [paginas.json]
"""
import io
import json
import keyword
import os
import re
import sys
import tokenize
import zipfile
from xml.sax.saxutils import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from i18n import LANG, NOTE_COLORS, S  # noqa: E402
if LANG == "en":                     # conteudo em ingles: en/*.py tem precedencia na importacao
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "en"))
import images  # noqa: E402
import outline as O  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, "img")

DOC_CODE = "MAN-PYQT6-001"
DOC_REV = "0"
COMPLETED_STEPS = {1, 2, 3, 4, 5}
REV_DESC = "0 — Emissão inicial (publicação aberta)" if LANG == "pt" else "0 — Initial issue (open publication)"
AUTOR = "Patrick Silva Oliveira"
DOC_DATE = "12/11/2026" if LANG == "pt" else "2026-11-12"
if LANG == "pt":
    DOC_TITLE = "Manual Profissional de Python com Interface Gráfica"
    DOC_SUB = "Desenvolvimento de aplicações desktop com PyQt6 — do zero ao avançado"
else:
    DOC_TITLE = "Professional Python GUI Development Manual"
    DOC_SUB = "Building desktop applications with PyQt6 — from zero to advanced"
REF_VERSION = "Python ≥ 3.10 · PyQt6 6.12.0 · Qt 6.12 LTS"
DOC_YEAR = "2026"
REPO_URL = "https://github.com/ptksilva18/manual-pyqt6"
CC_URL = ("https://creativecommons.org/licenses/by-sa/4.0/deed.pt-br" if LANG == "pt"
          else "https://creativecommons.org/licenses/by-sa/4.0/")
GPL_URL = "https://www.gnu.org/licenses/gpl-3.0.html"
RIVERBANK_URL = "https://www.riverbankcomputing.com/commercial/license-faq"

TEXT_W = 9071           # largura util (twips): A4 11906 - 1701 - 1134
NAVY, BLUE, GREY = "1F3864", "2E75B6", "595959"
LEVEL_NAME = S["levels"]
KF, KT, KL = S["fig"], S["tab"], S["lst"]   # rotulos das legendas (e nomes dos campos SEQ)

NS = ('xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas" '
      'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
      'xmlns:o="urn:schemas-microsoft-com:office:office" '
      'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
      'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" '
      'xmlns:v="urn:schemas-microsoft-com:vml" '
      'xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing" '
      'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
      'xmlns:w10="urn:schemas-microsoft-com:office:word" '
      'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
      'xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" '
      'xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup" '
      'xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk" '
      'xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml" '
      'xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" '
      'mc:Ignorable="w14 wp14"')
XML_HDR = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'


def esc(t):
    return escape(t, {'"': "&quot;"})


# ------------------------------------------------------- realce de sintaxe --
HL = {"kw": "0000FF", "str": "A31515", "com": "008000", "num": "098658", "bi": "795E26",
      "deco": "AF00DB", "self": "1F3864"}
BUILTINS = {"print", "len", "range", "int", "float", "str", "list", "dict", "tuple", "set", "super", "isinstance",
            "type", "object", "enumerate", "zip", "open", "sorted", "sum", "min", "max", "abs", "round", "bool",
            "repr", "hasattr", "getattr", "setattr", "callable", "iter", "next", "map", "filter", "any", "all",
            "staticmethod", "classmethod", "property", "Exception", "ValueError", "TypeError", "RuntimeError",
            "KeyError", "IndexError", "OSError", "ZeroDivisionError", "NotImplementedError", "AttributeError",
            "format", "vars", "id", "hash", "reversed", "divmod", "chr", "ord", "bytes"}
STR_TOKS = {tokenize.STRING} | {getattr(tokenize, n) for n in ("FSTRING_START", "FSTRING_MIDDLE", "FSTRING_END",
                                                               "TSTRING_START", "TSTRING_MIDDLE", "TSTRING_END")
                                if hasattr(tokenize, n)}


def hl_python(lines):
    """Retorna, por linha, lista de (texto, cor|None). Cores no padrao 'VS Light'."""
    n = len(lines)
    segs = [[] for _ in range(n)]
    src = "\n".join(lines) + "\n"

    def emit(text, color, row):
        for i, part in enumerate(text.split("\n")):
            r = row - 1 + i
            if part and 0 <= r < n:
                segs[r].append((part, color))

    def between(a, b):
        (r1, c1), (r2, c2) = a, b
        if r1 == r2:
            return lines[r1 - 1][c1:c2] if r1 - 1 < n else ""
        out = (lines[r1 - 1][c1:] if r1 - 1 < n else "") + "\n"
        for r in range(r1 + 1, r2):
            out += (lines[r - 1] if r - 1 < n else "") + "\n"
        out += lines[r2 - 1][:c2] if r2 - 1 < n else ""
        return out

    try:
        toks = list(tokenize.generate_tokens(io.StringIO(src).readline))
    except (tokenize.TokenError, SyntaxError, IndentationError):
        return [[(ln, None)] for ln in lines]
    cur = (1, 0)
    prev_op = None
    for t in toks:
        if t.type == tokenize.ENDMARKER:
            break
        gap = between(cur, t.start)
        if gap:
            emit(gap, None, cur[0])
        color = None
        if t.type in STR_TOKS:
            color = HL["str"]
        elif t.type == tokenize.COMMENT:
            color = HL["com"]
        elif t.type == tokenize.NUMBER:
            color = HL["num"]
        elif t.type == tokenize.NAME:
            if prev_op == "@":
                color = HL["deco"]
            elif keyword.iskeyword(t.string) or t.string in ("match", "case"):
                color = HL["kw"]
            elif t.string in ("self", "cls"):
                color = HL["self"]
            elif t.string in BUILTINS:
                color = HL["bi"]
        elif t.type == tokenize.OP and t.string == "@":
            color = HL["deco"]
        if t.type not in (tokenize.NEWLINE, tokenize.NL, tokenize.DEDENT):
            emit(t.string, color, t.start[0])
        prev_op = t.string if t.type == tokenize.OP else (None if t.type not in (tokenize.NL, tokenize.NEWLINE) else prev_op)
        cur = t.end
    # sanidade: o texto reconstruido deve ser identico ao original
    for i, ln in enumerate(lines):
        rebuilt = "".join(x for x, _ in segs[i])
        if rebuilt != ln:
            return [[(l2, None)] for l2 in lines]
    return segs


# ----------------------------------------------------------------- runs ----
def rpr(b=False, i=False, color=None, sz=None, font=None, style=None, caps=False, shd=None):
    x = ""
    if style:
        x += f'<w:rStyle w:val="{style}"/>'
    if font:
        x += f'<w:rFonts w:ascii="{font}" w:hAnsi="{font}" w:cs="{font}"/>'
    if b:
        x += "<w:b/><w:bCs/>"
    if i:
        x += "<w:i/><w:iCs/>"
    if caps:
        x += "<w:caps/>"
    if color:
        x += f'<w:color w:val="{color}"/>'
    if sz:
        x += f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/>'
    if shd:
        x += f'<w:shd w:val="clear" w:color="auto" w:fill="{shd}"/>'
    return f"<w:rPr>{x}</w:rPr>" if x else ""


def run(text, rp=""):
    return f'<w:r>{rp}<w:t xml:space="preserve">{esc(text)}</w:t></w:r>'


EXT_LINKS = {}  # url -> rId (relacoes externas do document.xml)


def ext_link(url, text=None, rp_extra=None):
    """Hiperlink externo (relacao TargetMode=External)."""
    rid = EXT_LINKS.setdefault(url, f"rIdExt{len(EXT_LINKS) + 1}")
    return (f'<w:hyperlink r:id="{rid}" w:history="1">'
            f'{run(text or url, rpr(style="Hyperlink", **(rp_extra or {})))}</w:hyperlink>')


def tab_run(rp=""):
    return f"<w:r>{rp}<w:tab/></w:r>"


INLINE_RE = re.compile(r"(\*\*.+?\*\*|`.+?`|\*.+?\*)")


def rich(text, base=None):
    """**negrito**, *italico*, `codigo` -> runs."""
    base = base or {}
    out = []
    for part in INLINE_RE.split(text):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            out.append(run(part[2:-2], rpr(b=True, **base)))
        elif part.startswith("`") and part.endswith("`"):
            out.append(run(part[1:-1], rpr(style="CodigoInline")))
        elif part.startswith("*") and part.endswith("*") and len(part) > 2:
            out.append(run(part[1:-1], rpr(i=True, **base)))
        else:
            out.append(run(part, rpr(**base)))
    return "".join(out)


def field(instr, result_runs, rp=""):
    return (f'<w:r>{rp}<w:fldChar w:fldCharType="begin"/></w:r>'
            f'<w:r>{rp}<w:instrText xml:space="preserve"> {esc(instr)} </w:instrText></w:r>'
            f'<w:r>{rp}<w:fldChar w:fldCharType="separate"/></w:r>'
            f'{result_runs}'
            f'<w:r>{rp}<w:fldChar w:fldCharType="end"/></w:r>')


def para(runs, style=None, ppr_extra="", jc=None, keep_next=False, page_break_before=False,
         spacing=None, numpr=None, ind=None, pbdr=None, shd=None, tabs=None, outline=None, sect="",
         page_break=None):
    """pPr na ordem do schema CT_PPr."""
    x = ""
    if style:
        x += f'<w:pStyle w:val="{style}"/>'
    if keep_next:
        x += "<w:keepNext/>"
    if page_break_before or page_break is True:
        x += "<w:pageBreakBefore/>"
    elif page_break is False:
        x += '<w:pageBreakBefore w:val="0"/>'
    if numpr is not None:
        x += f'<w:numPr><w:ilvl w:val="{numpr[1]}"/><w:numId w:val="{numpr[0]}"/></w:numPr>'
    if pbdr:
        x += f"<w:pBdr>{pbdr}</w:pBdr>"
    if shd:
        x += f'<w:shd w:val="clear" w:color="auto" w:fill="{shd}"/>'
    if tabs:
        x += f"<w:tabs>{tabs}</w:tabs>"
    if spacing:
        x += f"<w:spacing {spacing}/>"
    if ind:
        x += f"<w:ind {ind}/>"
    if jc:
        x += f'<w:jc w:val="{jc}"/>'
    if outline is not None:
        x += f'<w:outlineLvl w:val="{outline}"/>'
    x += ppr_extra
    x += sect
    ppr = f"<w:pPr>{x}</w:pPr>" if x else ""
    return f"<w:p>{ppr}{runs}</w:p>"


def roman(n):
    vals = [(1000, "m"), (900, "cm"), (500, "d"), (400, "cd"), (100, "c"), (90, "xc"), (50, "l"), (40, "xl"),
            (10, "x"), (9, "ix"), (5, "v"), (4, "iv"), (1, "i")]
    out = ""
    for v, s in vals:
        while n >= v:
            out += s
            n -= v
    return out


# --------------------------------------------------------------- tabelas ----
def cell(content_xml, w, fill=None, borders=None, valign=None, mar=None):
    tcpr = f'<w:tcW w:w="{w}" w:type="dxa"/>'
    if borders:
        tcpr += f"<w:tcBorders>{borders}</w:tcBorders>"
    if fill:
        tcpr += f'<w:shd w:val="clear" w:color="auto" w:fill="{fill}"/>'
    if mar:
        tcpr += f"<w:tcMar>{mar}</w:tcMar>"
    if valign:
        tcpr += f'<w:vAlign w:val="{valign}"/>'
    return f"<w:tc><w:tcPr>{tcpr}</w:tcPr>{content_xml}</w:tc>"


def table(rows_xml, widths, borders=True, header_rows=0, jc="center", layout_fixed=True):
    tw = sum(widths)
    b = ""
    if borders:
        b = ("<w:tblBorders>"
             f'<w:top w:val="single" w:sz="8" w:space="0" w:color="{NAVY}"/>'
             '<w:left w:val="nil"/>'
             f'<w:bottom w:val="single" w:sz="8" w:space="0" w:color="{NAVY}"/>'
             '<w:right w:val="nil"/>'
             '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="BFBFBF"/>'
             '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="BFBFBF"/>'
             "</w:tblBorders>")
    else:
        b = ('<w:tblBorders><w:top w:val="nil"/><w:left w:val="nil"/><w:bottom w:val="nil"/><w:right w:val="nil"/>'
             '<w:insideH w:val="nil"/><w:insideV w:val="nil"/></w:tblBorders>')
    tblpr = (f'<w:tblW w:w="{tw}" w:type="dxa"/><w:jc w:val="{jc}"/>{b}'
             + ('<w:tblLayout w:type="fixed"/>' if layout_fixed else "")
             + '<w:tblCellMar><w:top w:w="45" w:type="dxa"/><w:left w:w="85" w:type="dxa"/>'
               '<w:bottom w:w="45" w:type="dxa"/><w:right w:w="85" w:type="dxa"/></w:tblCellMar>'
             + '<w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" w:firstColumn="1" w:lastColumn="0" '
               'w:noHBand="0" w:noVBand="1"/>')
    grid = "".join(f'<w:gridCol w:w="{w}"/>' for w in widths)
    trs = []
    for idx, r in enumerate(rows_xml):
        trpr = "<w:cantSplit/>" + ("<w:tblHeader/>" if idx < header_rows else "")
        trs.append(f"<w:tr><w:trPr>{trpr}</w:trPr>{r}</w:tr>")
    return f"<w:tbl><w:tblPr>{tblpr}</w:tblPr><w:tblGrid>{grid}</w:tblGrid>{''.join(trs)}</w:tbl>"


def data_table(header, rows, widths, font_sz=None):
    assert abs(sum(widths) - TEXT_W) <= 3, (header, sum(widths))
    hdr = "".join(cell(para(rich(h, {"color": "FFFFFF"}), style="TabelaCabecalho"), w, fill=NAVY, valign="center")
                  for h, w in zip(header, widths))
    body = []
    for ri, r in enumerate(rows):
        fill = "F2F6FB" if ri % 2 else None
        cs = []
        for c, w in zip(r, widths):
            base = {"sz": font_sz} if font_sz else {}
            if c == O.TBD:
                runs_ = run(c, rpr(i=True, color="808080", sz=font_sz))
            else:
                runs_ = rich(c, base)
            cs.append(cell(para(runs_, style="TabelaTexto"), w, fill=fill, valign="center"))
        body.append("".join(cs))
    return table([hdr] + body, widths, header_rows=1)


def box(inner_paras, color, fill, w=TEXT_W):
    borders = (f'<w:top w:val="nil"/><w:left w:val="single" w:sz="36" w:space="0" w:color="{color}"/>'
               '<w:bottom w:val="nil"/><w:right w:val="nil"/>')
    mar = ('<w:top w:w="100" w:type="dxa"/><w:left w:w="200" w:type="dxa"/>'
           '<w:bottom w:w="100" w:type="dxa"/><w:right w:w="160" w:type="dxa"/>')
    c = cell("".join(inner_paras), w, fill=fill, borders=borders, mar=mar)
    return table([c], [w], borders=False)


# ---------------------------------------------------------------- imagem ----
class Media:
    def __init__(self):
        self.items = []   # (rid, filename, path)
        self.docpr = 0

    def add(self, path):
        rid = f"rIdImg{len(self.items) + 1}"
        fname = f"image{len(self.items) + 1}.png"
        self.items.append((rid, fname, path))
        return rid

    def inline(self, path, cx_cm, cy_cm, name, descr):
        rid = self.add(path)
        self.docpr += 1
        cx, cy = int(cx_cm * 360000), int(cy_cm * 360000)
        n = self.docpr
        return ('<w:r><w:rPr><w:noProof/></w:rPr><w:drawing>'
                f'<wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="{cx}" cy="{cy}"/>'
                '<wp:effectExtent l="0" t="0" r="0" b="0"/>'
                f'<wp:docPr id="{n}" name="{esc(name)}" descr="{esc(descr)}"/>'
                '<wp:cNvGraphicFramePr><a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/></wp:cNvGraphicFramePr>'
                '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
                '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
                '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
                f'<pic:nvPicPr><pic:cNvPr id="{n}" name="{esc(name)}"/><pic:cNvPicPr/></pic:nvPicPr>'
                f'<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
                f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
                '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic>'
                '</a:graphicData></a:graphic></wp:inline></w:drawing></w:r>')


# ================================================================ BUILDER ====
NUM_HEAD, NUM_ANNEX, NUM_BULLET = 1, 2, 3


class Builder:
    def __init__(self, pages):
        self.pages = pages or {}
        self.body = []
        self.media = Media()
        self.bm_id = 0
        self.toc = []        # (lvl, numtext, title, bm)
        self.caps = {KF: [], KT: [], KL: []}  # (label_text, bm)
        self.order = []      # (bm, search_text) em ordem do documento
        # contadores
        self.h = [0, 0, 0, 0]
        self.annex = [0, 0, 0]
        self.in_annex = False
        self.chapter_label = ""      # "3" ou "A"
        self.seq = {KF: 0, KT: 0, KL: 0}
        self.step = 2
        self.first_in_section = True
        self.num_lists = 0

    # ------------------------------------------------------------ util --
    def bookmark(self, runs, prefix="_Toc"):
        self.bm_id += 1
        name = f"{prefix}{self.bm_id:06d}"
        return (f'<w:bookmarkStart w:id="{self.bm_id}" w:name="{name}"/>{runs}'
                f'<w:bookmarkEnd w:id="{self.bm_id}"/>'), name

    def page_of(self, bm):
        return self.pages.get(bm, "")

    # -------------------------------------------------------- headings --
    def heading(self, lvl, title):
        self.h[lvl - 1] += 1
        for k in range(lvl, 4):
            self.h[k] = 0
        num = ".".join(str(x) for x in self.h[:lvl])
        if lvl == 1:
            self.chapter_label = str(self.h[0])
            for k in self.seq:
                self.seq[k] = 0
        runs, bm = self.bookmark(run(title))
        # numeracao vem do estilo (numPr no estilo Heading N)
        self.body.append(para(runs, style=f"Heading{lvl}"))
        self.toc.append((lvl, num, title, bm))
        self.order.append((bm, f"{num} {title}"))

    def heading_unnumbered(self, title, page_break=True):
        runs, bm = self.bookmark(run(title))
        for k in self.seq:
            self.seq[k] = 0
        self.body.append(para(runs, style="Heading1", numpr=(0, 0), page_break=None if page_break else False))
        self.toc.append((1, "", title, bm))
        self.order.append((bm, title))

    def heading_annex(self, lvl, title):
        self.in_annex = True
        self.annex[lvl - 1] += 1
        for k in range(lvl, 3):
            self.annex[k] = 0
        letter = chr(ord("A") + self.annex[0] - 1)
        if lvl == 1:
            num = f"{S['annex']} {letter} —"
            self.chapter_label = letter
            for k in self.seq:
                self.seq[k] = 0
        else:
            num = ".".join([letter] + [str(x) for x in self.annex[1:lvl]])
        runs, bm = self.bookmark(run(title))
        self.body.append(para(runs, style=f"Heading{lvl}", numpr=(NUM_ANNEX, lvl - 1)))
        self.toc.append((lvl, num, title, bm))
        self.order.append((bm, f"{num} {title}" if lvl > 1 else f"{S['annex']} {letter} — {title}"))

    def part(self, b):
        title = f"{S['part']} {b['roman']} — {b['title']}"
        runs, bm = self.bookmark(run(title))
        for k in self.seq:
            self.seq[k] = 0
        # Titulo 1 sem numero, formatado como divisor de Parte
        first = self.first_in_section
        self.first_in_section = False
        # espacador de altura exata: centraliza o divisor de forma identica no Word e no LibreOffice
        self.body.append(para("", page_break=False if first else True,
                              spacing='w:before="0" w:after="0" w:line="3600" w:lineRule="exact"'))
        self.body.append(para(runs, style="Heading1", numpr=(0, 0), jc="center", page_break=False,
                              spacing='w:before="0" w:after="360"',
                              pbdr='<w:bottom w:val="nil"/>',
                              ppr_extra='<w:rPr><w:sz w:val="52"/><w:szCs w:val="52"/></w:rPr>'))
        # o tamanho do run do titulo
        self.body[-1] = self.body[-1].replace(run(title), run(title, rpr(sz=52, color=NAVY)))
        self.body.append(para(run(b["sub"], rpr(sz=30, color=BLUE)), style="Normal", jc="center",
                              spacing='w:before="0" w:after="600"'))
        self.body.append(para(run(b["hint"], rpr(sz=24, color=GREY)), jc="center", spacing='w:after="120"'))
        self.toc.append((1, "", title, bm))
        self.order.append((bm, title))

    # -------------------------------------------------------- captions --
    def caption(self, kind, title, keep_next):
        self.seq[kind] += 1
        n = self.seq[kind]
        rp = ""
        if self.in_annex or os.environ.get("AUDIT_STATIC_CAPTIONS") == "1":
            # anexos: letra literal | variante de auditoria (LibreOffice nao avalia STYLEREF \s)
            chap_runs = run(self.chapter_label)
        else:
            chap_runs = field("STYLEREF 1 \\s", run(self.chapter_label))
        if os.environ.get("AUDIT_STATIC_CAPTIONS") == "1":
            seq_runs = run(str(n))          # LibreOffice ignora o reinicio \\s 1 do SEQ
        else:
            seq_runs = field(f"SEQ {kind} \\* ARABIC \\s 1", run(str(n)))
        inner = run(f"{kind} ") + chap_runs + run(".") + seq_runs + run(f" — {title}")
        runs, bm = self.bookmark(inner)
        label = f"{kind} {self.chapter_label}.{n} — {title}"
        self.body.append(para(runs, style="Caption", keep_next=keep_next))
        self.caps[kind].append((label, bm))
        self.order.append((bm, label))
        return label

    # ----------------------------------------------------------- blocos --
    def placeholder(self):
        self.body.append(para(run(S["placeholder"]), style="Marcador"))

    def objectives(self, items):
        inner = [para(run(S["objectives"], rpr(b=True, color=NAVY, sz=22)), style="Normal",
                      spacing='w:before="40" w:after="80"', keep_next=True)]
        for it in items:
            inner.append(para(rich(it, {"sz": 20}), style="ListParagraph", numpr=(NUM_BULLET, 0),
                              spacing='w:after="40"'))
        inner.append(para(run(f"{S['level']}: {LEVEL_NAME[self.step]}",
                              rpr(i=True, color=GREY, sz=18)), style="Normal", spacing='w:before="80" w:after="40"'))
        self.body.append(box(inner, BLUE, "EAF1FA"))
        self.body.append(para("", spacing='w:after="60"'))

    def note(self, kind, text):
        c, f = NOTE_COLORS[kind]
        inner = [para(run(kind, rpr(b=True, color=c, sz=20)) + run("  ") + rich(text, {"sz": 20}),
                      style="Normal", spacing='w:before="0" w:after="0"', jc="left")]
        self.body.append(box(inner, c, f))
        self.body.append(para("", spacing='w:after="60"'))

    def figure_real(self, b):
        from PIL import Image
        n_next = self.seq[KF] + 1
        w_px, h_px = Image.open(b["img"]).size
        w_cm = b.get("width", 15.0)
        h_cm = w_cm * h_px / w_px
        if h_cm > 13.0:
            h_cm = 13.0
            w_cm = h_cm * w_px / h_px
        img = self.media.inline(b["img"], round(w_cm, 3), round(h_cm, 3), f"{KF} {self.chapter_label}.{n_next}", b["t"])
        self.body.append(para(img, style="Figura", keep_next=True))
        self.caption(KF, b["t"], keep_next=False)

    def figure(self, title, desc):
        n_next = self.seq[KF] + 1
        label = f"{S['FIG']} {self.chapter_label}.{n_next}"
        fname = os.path.join(IMG, f"fig_{self.chapter_label}_{n_next}.png")
        images.placeholder(fname, label, title, desc, S["placeholder"])
        img = self.media.inline(fname, 15.0, 6.5, f"{KF} {self.chapter_label}.{n_next}", f"{title}. {desc}")
        self.body.append(para(img, style="Figura", keep_next=True))
        self.caption(KF, title, keep_next=False)

    def table_block(self, b):
        self.caption(KT, b["t"], keep_next=True)
        self.body.append(data_table(b["header"], b["rows"], b["widths"], b.get("font")))
        self.body.append(para("", style="AposTabela"))

    def code_lines(self, lines, lang, allow_long=False):
        too_long = [] if allow_long else [ln for ln in lines if len(ln) > 90]
        assert not too_long, f"linha de codigo > 90 caracteres: {too_long[0]!r}"
        segs = hl_python(lines) if lang == "python" else [[(ln, None)] for ln in lines]
        for i, ln in enumerate(lines):
            last = i == len(lines) - 1
            runs_ = "".join(run(t, rpr(color=c)) for t, c in segs[i]) if ln else run(" ")
            sp = None
            if i == 0 and last:
                sp = 'w:before="60" w:after="60"'
            elif i == 0:
                sp = 'w:before="60" w:after="0"'
            elif last:
                sp = 'w:before="0" w:after="60"'
            self.body.append(para(runs_, style="Codigo", keep_next=not last, spacing=sp))

    def code_block(self, b):
        self.caption(KL, b["t"], keep_next=True)
        self.code_lines(b["lines"], b.get("lang", "python"), b.get("allow_long", False))
        if b.get("tested"):
            self.body.append(para(run(S["verified"],
                                      rpr(i=True, sz=16, color="548235")), style="Normal",
                                  spacing='w:before="40" w:after="160"'))
        elif b.get("nota"):
            ok = b["nota"].startswith("✔")
            self.body.append(para(run(b["nota"], rpr(i=True, sz=16, color="548235" if ok else "C55A11")),
                                  style="Normal", spacing='w:before="40" w:after="160"'))
        else:
            self.body.append(para("", spacing='w:after="120"'))

    def snip_block(self, b):
        self.body.append(para("", style="AposTabela", keep_next=True, spacing='w:before="0" w:after="40"'))
        self.code_lines(b["lines"], b.get("lang", "python"))
        self.body.append(para("", spacing='w:after="100"'))

    def out_block(self, b):
        self.body.append(para(run(b["t"], rpr(b=True, sz=17, color=GREY)), style="Normal", keep_next=True,
                              spacing='w:before="60" w:after="20"', jc="left"))
        lines = b["lines"] or [""]
        for i, ln in enumerate(lines):
            self.body.append(para(run(ln if ln else " "), style="Saida", keep_next=i < len(lines) - 1))
        self.body.append(para("", spacing='w:after="100"'))

    def numbered(self, items):
        self.num_lists += 1
        nid = 100 + self.num_lists
        for it in items:
            self.body.append(para(rich(it), style="ListParagraph", numpr=(nid, 0), spacing='w:after="60"'))

    def bullets(self, items):
        for it in items:
            self.body.append(para(rich(it), style="ListParagraph", numpr=(NUM_BULLET, 0), spacing='w:after="60"'))

    # ------------------------------------------------------- catalogo --
    def catalog(self):
        cat = json.load(open(os.path.join(HERE, "data", "pyqt6_catalog.json"), encoding="utf-8"))
        for group, mods in O.CATALOG_GROUPS:
            self.heading_annex(2, group)
            for m in mods:
                v = cat[m]
                cls, fns = v["classes"], v["functions"]
                self.heading_annex(3, m)
                note = S["win_only"] if m == "QAxContainer" else ""
                self.caption(KT, S["cat_caption"].format(m=m, note=note, n=len(cls)), keep_next=True)
                ncol = 3
                widths = [3024, 3024, 3023]
                nrow = -(-len(cls) // ncol)
                rows = []
                for r in range(nrow):
                    cs = []
                    for c in range(ncol):
                        k = c * nrow + r
                        name = cls[k] if k < len(cls) else ""
                        cs.append(cell(para(run(name, rpr(font="Consolas", sz=14)), style="TabelaTexto"),
                                       widths[c], fill="F2F6FB" if r % 2 else None))
                    rows.append("".join(cs))
                self.body.append(table(rows, widths))
                if fns:
                    self.body.append(para(run(S["cat_functions"].format(n=len(fns)), rpr(b=True, sz=18))
                                          + run(", ".join(fns), rpr(font="Consolas", sz=15)),
                                          style="Normal", spacing='w:before="80" w:after="200"', jc="left"))
                else:
                    self.body.append(para("", style="AposTabela"))

    # ---------------------------------------------------------- corpo --
    def render_blocks(self, blocks):
        n = len(blocks)
        for idx, b in enumerate(blocks):
            k = b["k"]
            if k == "part":
                self.in_annex = False
                self.step = b["step"]
                self.part(b)
            elif k == "h":
                if b["lvl"] == 1:
                    self.step = b.get("step", self.step)
                self.heading(b["lvl"], b["t"])
                nxt = blocks[idx + 1] if idx + 1 < n else None
                if nxt is None or nxt["k"] in ("part", "hu", "ha") or (nxt["k"] == "h" and nxt["lvl"] <= b["lvl"]):
                    self.placeholder()
            elif k == "hu":
                self.heading_unnumbered(b["t"])
            elif k == "ha":
                self.heading_annex(b["lvl"], b["t"])
            elif k == "p":
                txt = b["t"]
                if txt.startswith("[") and txt.endswith("]"):
                    self.body.append(para(run(txt), style="Marcador"))
                else:
                    self.body.append(para(rich(txt), style="Normal"))
            elif k == "obj":
                self.objectives(b["items"])
            elif k == "bl":
                self.bullets(b["items"])
            elif k == "fig":
                if b.get("img"):
                    self.figure_real(b)
                else:
                    self.figure(b["t"], b["desc"])
            elif k == "snip":
                self.snip_block(b)
            elif k == "out":
                self.out_block(b)
            elif k == "nl":
                self.numbered(b["items"])
            elif k == "tab":
                self.table_block(b)
            elif k == "code":
                self.code_block(b)
            elif k == "note":
                self.note(b["kind"], b["t"])
            elif k == "catalog":
                self.catalog()
            else:
                raise ValueError(k)


# ============================================================ FRONT MATTER ==
def cover(media):
    out = []
    out.append(para(run(DOC_CODE + f"  ·  {S['revision']} " + DOC_REV, rpr(b=True, color=BLUE, sz=22)), jc="right",
                    spacing='w:before="0" w:after="360"'))
    out.append(para(run(DOC_TITLE.upper(), rpr(b=True, color=NAVY, sz=48)), style="Title", jc="left",
                    spacing='w:before="0" w:after="160"'))
    out.append(para(run(DOC_SUB, rpr(color=BLUE, sz=30)), style="Subtitle", jc="left",
                    spacing='w:before="0" w:after="360"',
                    pbdr=f'<w:bottom w:val="single" w:sz="12" w:space="12" w:color="{BLUE}"/>'))
    img = media.inline(os.path.join(IMG, "cover.png"), 16.0, 8.33, S["cover_alt_t"], S["cover_alt_d"])
    out.append(para(img, jc="center", spacing='w:before="120" w:after="360"'))
    meta = [(S["doc_code"], DOC_CODE), (S["revision"], REV_DESC),
            (S["date"], DOC_DATE), (S["ref_version"], REF_VERSION),
            (S["classification"], S["classification_v"]), (S["author"], AUTOR)]
    rows = []
    for k, v in meta:
        rows.append(cell(para(run(k, rpr(b=True, color=NAVY, sz=19)), style="TabelaTexto"), 3000)
                    + cell(para(run(v, rpr(sz=19, color="808080" if v == "[preencher]" else None,
                                           i=v == "[preencher]")), style="TabelaTexto"), 6071))
    out.append(table(rows, [3000, 6071]))
    return out


def control_sheet():
    out = []
    out.append(para(run(S["control"]), style="TituloLista", page_break=False))
    data = [(S["code"], DOC_CODE), (S["title"], DOC_TITLE), (S["subtitle"], DOC_SUB),
            (S["cur_rev"], REV_DESC),
            (S["status"], S["status_v"]), (S["ref_version"], REF_VERSION),
            (S["prepared"], AUTOR), (S["checked"], S["na"]),
            (S["approved"], S["na"])]
    rows = []
    for k, v in data:
        ph = v == "[preencher]"
        rows.append(cell(para(run(k, rpr(b=True, color=NAVY)), style="TabelaTexto"), 2600, fill="F2F6FB")
                    + cell(para(run(v, rpr(i=ph, color="808080" if ph else None)), style="TabelaTexto"), 6471))
    out.append(table(rows, [2600, 6471]))
    out.append(para(run(S["history"]), style="SubtituloLista"))
    desc = ("Emissão inicial para publicação aberta: Partes I a V, referências, glossário e "
            "Anexos A a D. Texto sob CC BY-SA 4.0 e código sob GPL-3.0-only." if LANG == "pt" else
            "Initial issue for open publication: Parts I to V, references, glossary and Annexes A to D. "
            "Text under CC BY-SA 4.0 and code under GPL-3.0-only.")
    hist = [["0", DOC_DATE, desc, S["issued"]]]
    out.append(data_table(S["hist_head"], hist, [700, 1250, 5871, 1250], 18))
    return out



def _bp(*pieces, jc="both"):  # paragrafo de corpo (justificado por padrao)
    return para("".join(pieces), jc=jc, spacing='w:before="0" w:after="120"')


def _bl(*pieces):  # item de lista com marcador
    return para("".join(pieces), style="ListParagraph", numpr=(NUM_BULLET, 0), spacing='w:after="60"')


def license_page():
    """Licenca e avisos (publicacao aberta), no idioma do documento."""
    return license_page_pt() if LANG == "pt" else license_page_en()


def license_page_en():
    bp, bl = _bp, _bl
    out = [para(run("LICENSE AND NOTICES"), style="TituloLista")]
    out.append(bp(rich(f"© {DOC_YEAR} {AUTOR}. {DOC_CODE} — {DOC_TITLE}.")))

    out.append(para(run("TEXT, FIGURES AND TABLES — CC BY-SA 4.0"), style="SubtituloLista"))
    out.append(bp(rich("The text, figures, diagrams, tables and screenshots of this manual are licensed under the "
                       "Creative Commons **Attribution-ShareAlike 4.0 International** license (CC BY-SA 4.0): "),
                  ext_link(CC_URL), run(". You may copy, redistribute and adapt the material for any purpose, "
                                        "including commercially, provided that:")))
    out.append(bl(rich("**Attribution** — you give credit to the author, provide the license with its link and "
                       "indicate whether changes were made;")))
    out.append(bl(rich("**ShareAlike** — you distribute adaptations under the same license or under a license "
                       "declared compatible by Creative Commons (GPL v3 is one of them).")))
    out.append(bp(rich("Exception: Figure 11.1 shows the user interface of Qt Designer, software by The Qt Company "
                       "distributed under its own terms; the license above covers only the author's contribution "
                       "to that figure.")))

    out.append(para(run("CODE — GPL-3.0-only"), style="SubtituloLista"))
    out.append(bp(rich("The code listings printed in this manual are an exception to the license of the text: they, "
                       "and all code in the repository (examples, capstone project and the generator of this "
                       "document), are licensed under the **GNU General Public License, version 3** "
                       "(GPL-3.0-only) — the same license under which PyQt6 is distributed for open-source "
                       "projects: "), ext_link(GPL_URL), run(".")))

    out.append(para(run("IF YOU DISTRIBUTE AN APPLICATION BUILT WITH PyQt6"), style="SubtituloLista"))
    out.append(bp(rich("PyQt6 is offered by Riverbank Computing under two licenses: GPL v3 or a commercial "
                       "license. It is not offered under the LGPL (unlike Qt). In practice:")))
    out.append(bl(rich("personal use, study and in-house tools that are not distributed to third parties do not "
                       "trigger the GPL's distribution obligations;")))
    out.append(bl(rich("an application distributed to third parties with PyQt6 under the GPL must be distributed "
                       "under a GPL v3-compatible license, with the source code available to whoever receives it;")))
    out.append(bl(rich("to distribute a closed-source application you need the commercial PyQt6 license, and you "
                       "must also comply with the license of the Qt you use. See Riverbank's license FAQ: "),
                  ext_link(RIVERBANK_URL), run(".")))
    out.append(bp(rich("*This summary is for information only and is not legal advice.*")))

    out.append(para(run("DISCLAIMER OF WARRANTY"), style="SubtituloLista"))
    out.append(bp(rich("The content and the code are provided “as is”, without warranty of any kind, under the "
                       "terms of the licenses above. The engineering examples (such as the leak test in Chapter 31) "
                       "are for teaching, use fictitious data and do not replace standards, procedures or "
                       "professional verification.")))

    out.append(para(run("TRADEMARKS"), style="SubtituloLista"))
    out.append(bp(rich("Qt is a registered trademark of The Qt Company Ltd. PyQt is a product of Riverbank "
                       "Computing Limited. Python is a registered trademark of the Python Software Foundation. "
                       "Other trademarks mentioned (for example, Windows and Excel) belong to their owners. This "
                       "manual is an independent work, not affiliated with, sponsored or endorsed by these "
                       "organizations.")))

    out.append(para(run("REPOSITORY AND HOW TO CITE"), style="SubtituloLista"))
    out.append(bp(rich("Source code of the listings, capstone project and document generator: "),
                  ext_link(REPO_URL), run("."), jc="left"))
    out.append(bp(rich(f"OLIVEIRA, P. S. *{DOC_TITLE}* ({DOC_CODE}), Rev. {DOC_REV}. {DOC_YEAR}. Available at: "),
                  ext_link(REPO_URL), run(". License CC BY-SA 4.0."), jc="left"))
    out.append(bp(rich("A Portuguese edition (pt-BR) of this manual is available in the same repository."),
                  jc="left"))
    return out


def license_page_pt():
    bp, bl = _bp, _bl

    out = [para(run("LICENÇA E AVISOS"), style="TituloLista")]
    out.append(bp(rich(f"© {DOC_YEAR} {AUTOR}. {DOC_CODE} — {DOC_TITLE}.")))

    out.append(para(run("TEXTO, FIGURAS E TABELAS — CC BY-SA 4.0"), style="SubtituloLista"))
    out.append(bp(rich("O texto, as figuras, os diagramas, as tabelas e as capturas de tela deste manual são "
                       "licenciados sob a licença Creative Commons **Atribuição-CompartilhaIgual 4.0 Internacional** "
                       "(CC BY-SA 4.0): "), ext_link(CC_URL), run(". Você pode copiar, redistribuir e adaptar o "
                       "material para qualquer finalidade, inclusive comercial, desde que:")))
    out.append(bl(rich("**Atribuição** — dê o crédito ao autor, indique a licença com o link e informe se fez "
                       "alterações;")))
    out.append(bl(rich("**CompartilhaIgual** — distribua as adaptações sob a mesma licença ou sob uma licença "
                       "declarada compatível pela Creative Commons (a GPL v3 é uma delas).")))
    out.append(bp(rich("Exceção: a Figura 11.1 mostra a interface do Qt Designer, software da The Qt Company "
                       "distribuído sob os seus próprios termos; a licença acima cobre apenas a contribuição do "
                       "autor nessa figura.")))

    out.append(para(run("CÓDIGO — GPL-3.0-only"), style="SubtituloLista"))
    out.append(bp(rich("As listagens de código impressas neste manual são uma exceção à licença do texto: elas, e "
                       "todo o código do repositório (exemplos, projeto integrador e o gerador deste documento), "
                       "são licenciadas sob a **GNU General Public License, versão 3** (GPL-3.0-only) — a mesma "
                       "licença sob a qual o PyQt6 é distribuído para projetos de código aberto: "),
                  ext_link(GPL_URL), run(".")))

    out.append(para(run("SE VOCÊ FOR DISTRIBUIR UMA APLICAÇÃO FEITA COM PyQt6"), style="SubtituloLista"))
    out.append(bp(rich("O PyQt6 é oferecido pela Riverbank Computing sob duas licenças: GPL v3 ou licença "
                       "comercial. Ele não é oferecido sob LGPL (ao contrário do Qt). Na prática:")))
    out.append(bl(rich("uso pessoal, estudo e ferramentas internas que não são distribuídas a terceiros não "
                       "disparam as obrigações de distribuição da GPL;")))
    out.append(bl(rich("uma aplicação distribuída a terceiros com o PyQt6 sob GPL deve ser distribuída sob uma "
                       "licença compatível com a GPL v3, com o código-fonte disponível a quem a receber;")))
    out.append(bl(rich("para distribuir uma aplicação de código fechado, é necessária a licença comercial do "
                       "PyQt6, além de respeitar a licença do Qt utilizado. Consulte o FAQ de licenças da "
                       "Riverbank: "), ext_link(RIVERBANK_URL), run(".")))
    out.append(bp(rich("*Este resumo é informativo e não constitui aconselhamento jurídico.*")))

    out.append(para(run("ISENÇÃO DE GARANTIA"), style="SubtituloLista"))
    out.append(bp(rich("O conteúdo e o código são fornecidos “no estado em que se encontram”, sem garantia de "
                       "qualquer tipo, nos termos das licenças acima. Os exemplos de engenharia (como o ensaio de "
                       "estanqueidade do Capítulo 31) são didáticos, usam dados fictícios e não substituem norma, "
                       "procedimento ou verificação profissional.")))

    out.append(para(run("MARCAS"), style="SubtituloLista"))
    out.append(bp(rich("Qt é marca registrada da The Qt Company Ltd. PyQt é um produto da Riverbank Computing "
                       "Limited. Python é marca registrada da Python Software Foundation. As demais marcas citadas "
                       "(por exemplo, Windows e Excel) pertencem aos seus titulares. Este manual é uma obra "
                       "independente, sem afiliação, patrocínio ou endosso dessas organizações.")))

    out.append(para(run("REPOSITÓRIO E COMO CITAR"), style="SubtituloLista"))
    out.append(bp(rich("Código-fonte das listagens, projeto integrador e gerador do documento: "),
                  ext_link(REPO_URL), run("."), jc="left"))
    out.append(bp(rich(f"OLIVEIRA, P. S. *{DOC_TITLE}* ({DOC_CODE}), Rev. {DOC_REV}. {DOC_YEAR}. Disponível em: "),
                  ext_link(REPO_URL), run(". Licença CC BY-SA 4.0."), jc="left"))
    return out

# ================================================================= TOCs ====
TOC_NUMPOS = {1: (0, 567), 2: (567, 1247), 3: (1247, 2155), 4: (2155, 3289)}


def toc_paragraphs(entries, instr, style_for, pages, empty_msg):
    """Gera o campo TOC completo com entradas pre-calculadas."""
    paras = []
    begin = (f'<w:r><w:fldChar w:fldCharType="begin"/></w:r>'
             f'<w:r><w:instrText xml:space="preserve"> {esc(instr)} </w:instrText></w:r>'
             f'<w:r><w:fldChar w:fldCharType="separate"/></w:r>')
    end = '<w:r><w:fldChar w:fldCharType="end"/></w:r>'
    if not entries:
        return [para(begin + run(empty_msg) + end, style="Normal")]
    for i, (style, numtext, text, bm) in enumerate(entries):
        pg = pages.get(bm, "")
        inner = ""
        if numtext:
            inner += run(numtext) + ("<w:r><w:tab/></w:r>" if not numtext.startswith(S["annex"]) else run(" "))
        inner += run(text) + "<w:r><w:tab/></w:r>"
        inner += field(f"PAGEREF {bm} \\h", run(pg))
        link = f'<w:hyperlink w:anchor="{bm}" w:history="1">{inner}</w:hyperlink>'
        pre = begin if i == 0 else ""
        post = end if i == len(entries) - 1 else ""
        paras.append(f'<w:p><w:pPr><w:pStyle w:val="{style}"/></w:pPr>{pre}{link}{post}</w:p>')
    return paras


# =============================================================== estilos ===
def styles_xml():
    def pstyle(sid, name, ppr="", rpr_="", based="Normal", nxt="Normal", qformat=True, ui=None, extra=""):
        b = f'<w:basedOn w:val="{based}"/>' if based else ""
        n = f'<w:next w:val="{nxt}"/>' if nxt else ""
        u = f'<w:uiPriority w:val="{ui}"/>' if ui is not None else ""
        q = "<w:qFormat/>" if qformat else ""
        return (f'<w:style w:type="paragraph" w:styleId="{sid}"><w:name w:val="{name}"/>{b}{n}{u}{q}{extra}'
                f'<w:pPr>{ppr}</w:pPr><w:rPr>{rpr_}</w:rPr></w:style>')

    font = '<w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:eastAsia="Calibri" w:cs="Calibri"/>'
    s = [f'{XML_HDR}<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
         'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
         'xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" mc:Ignorable="w14">',
         '<w:docDefaults><w:rPrDefault><w:rPr>' + font +
         '<w:sz w:val="22"/><w:szCs w:val="22"/><w:lang w:val="' + S["doc_lang"] + '" w:eastAsia="en-US" w:bidi="ar-SA"/></w:rPr></w:rPrDefault>'
         '<w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="276" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>',
         # padroes
         '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/>'
         '<w:pPr><w:spacing w:after="120" w:line="276" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr>'
         f'<w:rPr>{font}<w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:style>',
         '<w:style w:type="character" w:default="1" w:styleId="DefaultParagraphFont"><w:name w:val="Default Paragraph Font"/>'
         '<w:uiPriority w:val="1"/><w:semiHidden/><w:unhideWhenUsed/></w:style>',
         '<w:style w:type="table" w:default="1" w:styleId="TableNormal"><w:name w:val="Normal Table"/><w:uiPriority w:val="99"/>'
         '<w:semiHidden/><w:unhideWhenUsed/><w:tblPr><w:tblInd w:w="0" w:type="dxa"/><w:tblCellMar>'
         '<w:top w:w="0" w:type="dxa"/><w:left w:w="108" w:type="dxa"/><w:bottom w:w="0" w:type="dxa"/>'
         '<w:right w:w="108" w:type="dxa"/></w:tblCellMar></w:tblPr></w:style>',
         '<w:style w:type="numbering" w:default="1" w:styleId="NoList"><w:name w:val="No List"/><w:uiPriority w:val="99"/>'
         '<w:semiHidden/><w:unhideWhenUsed/></w:style>']
    # titulos com numeracao vinculada
    hd = {1: (36, NAVY, 480, 240, True), 2: (28, BLUE, 360, 120, False), 3: (24, NAVY, 280, 100, False),
          4: (22, "404040", 220, 80, False)}
    for lvl, (sz, col, bef, aft, pbb) in hd.items():
        ppr = ("<w:keepNext/><w:keepLines/>" + ("<w:pageBreakBefore/>" if pbb else "")
               + f'<w:numPr><w:ilvl w:val="{lvl - 1}"/><w:numId w:val="{NUM_HEAD}"/></w:numPr>'
               + (f'<w:pBdr><w:bottom w:val="single" w:sz="12" w:space="6" w:color="{BLUE}"/></w:pBdr>' if lvl == 1 else "")
               + f'<w:spacing w:before="{bef}" w:after="{aft}" w:line="240" w:lineRule="auto"/>'
               + '<w:jc w:val="left"/>'
               + f'<w:outlineLvl w:val="{lvl - 1}"/>')
        rp = (font + "<w:b/><w:bCs/>" + ("<w:i/><w:iCs/>" if lvl == 4 else "")
              + f'<w:color w:val="{col}"/><w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/>')
        s.append(pstyle(f"Heading{lvl}", f"heading {lvl}", ppr, rp, ui=9))
    s.append(pstyle("Title", "Title", '<w:spacing w:after="160" w:line="240" w:lineRule="auto"/><w:jc w:val="left"/>',
                    font + f'<w:b/><w:bCs/><w:color w:val="{NAVY}"/><w:kern w:val="28"/><w:sz w:val="48"/><w:szCs w:val="48"/>', ui=10))
    s.append(pstyle("Subtitle", "Subtitle", '<w:spacing w:after="240"/><w:jc w:val="left"/>',
                    font + f'<w:color w:val="{BLUE}"/><w:sz w:val="30"/><w:szCs w:val="30"/>', ui=11))
    s.append(pstyle("Caption", "caption", '<w:spacing w:before="80" w:after="240" w:line="240" w:lineRule="auto"/><w:jc w:val="center"/>',
                    font + f'<w:b/><w:bCs/><w:color w:val="{NAVY}"/><w:sz w:val="19"/><w:szCs w:val="19"/>', ui=35))
    s.append(pstyle("Figura", S["st_fig"], '<w:keepNext/><w:spacing w:before="200" w:after="40" w:line="240" w:lineRule="auto"/><w:jc w:val="center"/>', "", ui=36))
    s.append(pstyle("TituloLista", S["st_titlelist"],
                    '<w:keepNext/><w:pageBreakBefore/><w:pBdr><w:bottom w:val="single" w:sz="12" w:space="6" '
                    f'w:color="{BLUE}"/></w:pBdr><w:spacing w:before="0" w:after="360" w:line="240" w:lineRule="auto"/><w:jc w:val="left"/>',
                    font + f'<w:b/><w:bCs/><w:color w:val="{NAVY}"/><w:sz w:val="36"/><w:szCs w:val="36"/>', ui=39))
    s.append(pstyle("SubtituloLista", S["st_sublist"],
                    '<w:keepNext/><w:spacing w:before="360" w:after="160" w:line="240" w:lineRule="auto"/><w:jc w:val="left"/>',
                    font + f'<w:b/><w:bCs/><w:color w:val="{BLUE}"/><w:sz w:val="26"/><w:szCs w:val="26"/>', ui=39))
    s.append(pstyle("TOCHeading", "TOC Heading", '<w:keepNext/><w:spacing w:before="0" w:after="240"/>',
                    font + f'<w:b/><w:color w:val="{NAVY}"/><w:sz w:val="36"/>', ui=39, based="Normal"))
    for lvl, (npos, tpos) in TOC_NUMPOS.items():
        ppr = (f'<w:tabs><w:tab w:val="left" w:pos="{tpos}"/><w:tab w:val="right" w:leader="dot" w:pos="{TEXT_W}"/></w:tabs>'
               + f'<w:spacing w:before="{120 if lvl == 1 else 0}" w:after="{40 if lvl == 1 else 20}" w:line="240" w:lineRule="auto"/>'
               + f'<w:ind w:left="{tpos}" w:right="567" w:hanging="{tpos - npos}"/><w:jc w:val="left"/>')
        rp = font + ("<w:b/><w:bCs/>" if lvl == 1 else "") + f'<w:sz w:val="{21 if lvl <= 2 else 20}"/>'
        s.append(pstyle(f"TOC{lvl}", f"toc {lvl}", ppr, rp, ui=39, qformat=False, extra="<w:unhideWhenUsed/>"))
    s.append(pstyle("TableofFigures", "table of figures",
                    f'<w:tabs><w:tab w:val="right" w:leader="dot" w:pos="{TEXT_W}"/></w:tabs>'
                    '<w:spacing w:after="40" w:line="240" w:lineRule="auto"/><w:ind w:left="0" w:right="567" w:firstLine="0"/><w:jc w:val="left"/>',
                    font + '<w:sz w:val="21"/>', ui=99, qformat=False, extra="<w:unhideWhenUsed/>"))
    s.append(pstyle("Header", "header", f'<w:pBdr><w:bottom w:val="single" w:sz="6" w:space="4" w:color="{BLUE}"/></w:pBdr>'
                    f'<w:tabs><w:tab w:val="right" w:pos="{TEXT_W}"/></w:tabs>'
                    '<w:spacing w:after="0" w:line="240" w:lineRule="auto"/><w:jc w:val="left"/>',
                    font + f'<w:color w:val="{GREY}"/><w:sz w:val="17"/><w:szCs w:val="17"/>', ui=99, qformat=False))
    s.append(pstyle("Footer", "footer", f'<w:tabs><w:tab w:val="center" w:pos="{TEXT_W // 2}"/><w:tab w:val="right" w:pos="{TEXT_W}"/></w:tabs>'
                    '<w:spacing w:after="0" w:line="240" w:lineRule="auto"/><w:jc w:val="center"/>',
                    font + f'<w:color w:val="{GREY}"/><w:sz w:val="18"/><w:szCs w:val="18"/>', ui=99, qformat=False))
    s.append(pstyle("ListParagraph", "List Paragraph", '<w:spacing w:after="60"/><w:ind w:left="720"/><w:contextualSpacing/><w:jc w:val="left"/>', "", ui=34))
    s.append(pstyle("Codigo", S["st_code"],
                    f'<w:pBdr><w:left w:val="single" w:sz="24" w:space="8" w:color="{BLUE}"/></w:pBdr>'
                    '<w:shd w:val="clear" w:color="auto" w:fill="F3F5F8"/>'
                    '<w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/><w:ind w:left="227" w:right="113"/><w:jc w:val="left"/>',
                    '<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:cs="Consolas"/><w:noProof/><w:color w:val="1E1E1E"/>'
                    '<w:sz w:val="16"/><w:szCs w:val="16"/>', ui=40))
    s.append(pstyle("Saida", S["st_out"],
                    '<w:pBdr><w:left w:val="single" w:sz="24" w:space="8" w:color="70AD47"/></w:pBdr>'
                    '<w:shd w:val="clear" w:color="auto" w:fill="F4F8F0"/>'
                    '<w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/><w:ind w:left="227" w:right="113"/><w:jc w:val="left"/>',
                    '<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:cs="Consolas"/><w:noProof/><w:color w:val="333333"/>'
                    '<w:sz w:val="16"/><w:szCs w:val="16"/>', ui=40))
    s.append(pstyle("Marcador", S["st_marker"],
                    '<w:pBdr><w:left w:val="dashed" w:sz="8" w:space="6" w:color="A6A6A6"/></w:pBdr>'
                    '<w:spacing w:before="40" w:after="160"/><w:ind w:left="170"/><w:jc w:val="left"/>',
                    '<w:i/><w:iCs/><w:color w:val="808080"/><w:sz w:val="20"/><w:szCs w:val="20"/>', ui=41))
    s.append(pstyle("TabelaTexto", S["st_tabtext"], '<w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/><w:jc w:val="left"/>',
                    '<w:sz w:val="19"/><w:szCs w:val="19"/>', ui=42))
    s.append(pstyle("TabelaCabecalho", S["st_tabhead"], '<w:keepNext/><w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/><w:jc w:val="left"/>',
                    '<w:b/><w:bCs/><w:color w:val="FFFFFF"/><w:sz w:val="19"/><w:szCs w:val="19"/>', ui=42))
    s.append(pstyle("AposTabela", S["st_after"], '<w:spacing w:before="0" w:after="200" w:line="240" w:lineRule="auto"/>',
                    '<w:sz w:val="12"/><w:szCs w:val="12"/>', ui=43))
    s.append('<w:style w:type="character" w:styleId="CodigoInline"><w:name w:val="' + S["st_inline"] + '"/><w:uiPriority w:val="40"/><w:qFormat/>'
             '<w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:cs="Consolas"/><w:noProof/><w:color w:val="1F3864"/>'
             '<w:sz w:val="20"/><w:szCs w:val="20"/><w:shd w:val="clear" w:color="auto" w:fill="EEF1F6"/></w:rPr></w:style>')
    s.append('<w:style w:type="character" w:styleId="Hyperlink"><w:name w:val="Hyperlink"/><w:uiPriority w:val="99"/><w:unhideWhenUsed/>'
             f'<w:rPr><w:color w:val="{BLUE}"/><w:u w:val="single"/></w:rPr></w:style>')
    s.append("</w:styles>")
    return "".join(s)


def numbering_xml(n_numbered=0):
    W = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
    head_lvls = ""
    pos = [(0, 567), (0, 680), (0, 851), (0, 1077)]
    for i in range(4):
        txt = ".".join(f"%{k + 1}" for k in range(i + 1))
        left, hang = pos[i][1], pos[i][1]
        head_lvls += (f'<w:lvl w:ilvl="{i}"><w:start w:val="1"/><w:numFmt w:val="decimal"/>'
                      f'<w:pStyle w:val="Heading{i + 1}"/><w:lvlText w:val="{txt}"/><w:lvlJc w:val="left"/>'
                      f'<w:pPr><w:tabs><w:tab w:val="num" w:pos="{left}"/></w:tabs><w:ind w:left="{left}" w:hanging="{hang}"/></w:pPr></w:lvl>')
    for i in range(4, 9):
        head_lvls += (f'<w:lvl w:ilvl="{i}"><w:start w:val="1"/><w:numFmt w:val="decimal"/>'
                      f'<w:lvlText w:val="{".".join(f"%{k + 1}" for k in range(i + 1))}"/><w:lvlJc w:val="left"/>'
                      '<w:pPr><w:ind w:left="1300" w:hanging="1300"/></w:pPr></w:lvl>')
    annex_lvls = (
        '<w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="upperLetter"/><w:suff w:val="space"/><w:lvlText w:val="' + S["annex"] + ' %1 —"/>'
        '<w:lvlJc w:val="left"/><w:pPr><w:ind w:left="0" w:firstLine="0"/></w:pPr></w:lvl>'
        '<w:lvl w:ilvl="1"><w:start w:val="1"/><w:numFmt w:val="decimal"/><w:lvlText w:val="%1.%2"/>'
        '<w:lvlJc w:val="left"/><w:pPr><w:tabs><w:tab w:val="num" w:pos="680"/></w:tabs><w:ind w:left="680" w:hanging="680"/></w:pPr></w:lvl>'
        '<w:lvl w:ilvl="2"><w:start w:val="1"/><w:numFmt w:val="decimal"/><w:lvlText w:val="%1.%2.%3"/>'
        '<w:lvlJc w:val="left"/><w:pPr><w:tabs><w:tab w:val="num" w:pos="851"/></w:tabs><w:ind w:left="851" w:hanging="851"/></w:pPr></w:lvl>')
    for i in range(3, 9):
        annex_lvls += (f'<w:lvl w:ilvl="{i}"><w:start w:val="1"/><w:numFmt w:val="decimal"/>'
                       f'<w:lvlText w:val="{".".join(f"%{k + 1}" for k in range(i + 1))}"/><w:lvlJc w:val="left"/>'
                       '<w:pPr><w:ind w:left="1300" w:hanging="1300"/></w:pPr></w:lvl>')
    bullet_lvls = ""
    chars = ["•", "–", "▪"]
    for i in range(9):
        bullet_lvls += (f'<w:lvl w:ilvl="{i}"><w:start w:val="1"/><w:numFmt w:val="bullet"/>'
                        f'<w:lvlText w:val="{chars[i % 3]}"/><w:lvlJc w:val="left"/>'
                        f'<w:pPr><w:ind w:left="{360 + 360 * i}" w:hanging="283"/></w:pPr>'
                        f'<w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:color w:val="{BLUE}"/></w:rPr></w:lvl>')
    numbered_lvls = ""
    for i in range(9):
        fmt = ["decimal", "lowerLetter", "lowerRoman"][i % 3]
        txt = ["%{}.", "%{})", "%{}."][i % 3].format(i + 1)
        numbered_lvls += (f'<w:lvl w:ilvl="{i}"><w:start w:val="1"/><w:numFmt w:val="{fmt}"/>'
                          f'<w:lvlText w:val="{txt}"/><w:lvlJc w:val="left"/>'
                          f'<w:pPr><w:ind w:left="{397 + 360 * i}" w:hanging="397"/></w:pPr>'
                          f'<w:rPr><w:b/><w:color w:val="{BLUE}"/></w:rPr></w:lvl>')
    return (f'{XML_HDR}<w:numbering {W}>'
            f'<w:abstractNum w:abstractNumId="0"><w:multiLevelType w:val="multilevel"/>{head_lvls}</w:abstractNum>'
            f'<w:abstractNum w:abstractNumId="1"><w:multiLevelType w:val="multilevel"/>{annex_lvls}</w:abstractNum>'
            f'<w:abstractNum w:abstractNumId="2"><w:multiLevelType w:val="hybridMultilevel"/>{bullet_lvls}</w:abstractNum>'
            f'<w:abstractNum w:abstractNumId="3"><w:multiLevelType w:val="hybridMultilevel"/>{numbered_lvls}</w:abstractNum>'
            f'<w:num w:numId="{NUM_HEAD}"><w:abstractNumId w:val="0"/></w:num>'
            f'<w:num w:numId="{NUM_ANNEX}"><w:abstractNumId w:val="1"/></w:num>'
            f'<w:num w:numId="{NUM_BULLET}"><w:abstractNumId w:val="2"/></w:num>'
            + "".join(f'<w:num w:numId="{100 + k}"><w:abstractNumId w:val="3"/>'
                      '<w:lvlOverride w:ilvl="0"><w:startOverride w:val="1"/></w:lvlOverride></w:num>'
                      for k in range(1, n_numbered + 1))
            + '</w:numbering>')


def settings_xml():
    return (f'{XML_HDR}<w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            '<w:zoom w:percent="100"/><w:defaultTabStop w:val="708"/><w:characterSpacingControl w:val="doNotCompress"/>'
            '<w:updateFields w:val="true"/>'
            '<w:compat><w:compatSetting w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" w:val="15"/></w:compat>'
            '<w:themeFontLang w:val="' + S["doc_lang"] + '"/></w:settings>')


def header_xml():
    return (f'{XML_HDR}<w:hdr {NS}>'
            + para(run(f"{DOC_CODE}  ·  Rev. {DOC_REV}", rpr(b=True, color=NAVY)) + tab_run()
                   + run(S["header"]), style="Header")
            + "</w:hdr>")


def footer_xml():
    return (f'{XML_HDR}<w:ftr {NS}>'
            + para(run(S["page"]) + field("PAGE", run("1")), style="Footer")
            + "</w:ftr>")


def sectpr(kind):
    pg = '<w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1701" w:right="1134" w:bottom="1134" w:left="1701" w:header="709" w:footer="567" w:gutter="0"/>'
    hf = '<w:headerReference w:type="default" r:id="rIdHdr1"/><w:footerReference w:type="default" r:id="rIdFtr1"/>'
    if kind == "cover":
        return f'<w:sectPr><w:type w:val="nextPage"/>{pg}<w:cols w:space="708"/><w:docGrid w:linePitch="360"/></w:sectPr>'
    if kind == "front":
        return (f'<w:sectPr>{hf}<w:type w:val="nextPage"/>{pg}<w:pgNumType w:fmt="lowerRoman" w:start="1"/>'
                '<w:cols w:space="708"/><w:docGrid w:linePitch="360"/></w:sectPr>')
    return (f'<w:sectPr>{hf}<w:type w:val="nextPage"/>{pg}<w:pgNumType w:fmt="decimal" w:start="1"/>'
            '<w:cols w:space="708"/><w:docGrid w:linePitch="360"/></w:sectPr>')


# ================================================================ montagem ==
def build(out_path, pages):
    b = Builder(pages)
    # --- corpo (gerado primeiro para conhecer entradas de sumario) ---
    b.step = 2
    front_b = Builder(pages)          # prefacio (front matter)
    front_b.bm_id = 900000            # ids distintos
    front_b.media = b.media
    front_b.render_blocks(O.FRONT_UNNUMBERED)
    b.render_blocks(O.BODY)
    b.render_blocks(O.ANNEXES)

    parts = []
    parts += cover(b.media)
    parts.append(para("", sect=sectpr("cover")))
    parts += control_sheet()
    parts += license_page()
    # Sumario
    parts.append(para(run(S["toc"]), style="TituloLista"))
    toc_entries = [(f"TOC{lvl}", num, title, bm) for (lvl, num, title, bm) in front_b.toc + b.toc]
    parts += toc_paragraphs(toc_entries, 'TOC \\o "1-4" \\h \\z', None, pages, "")
    # Listas
    for kind, title, brk in ((KF, S["lof"], True), (KT, S["lot"], True), (KL, S["lol"], True)):
        parts.append(para(run(title), style="TituloLista"))
        ents = [("TableofFigures", "", label, bm) for (label, bm) in b.caps[kind]]
        parts += toc_paragraphs(ents, f'TOC \\h \\z \\c "{kind}"', None, pages, S["no_entries"])
    parts += front_b.body
    parts.append(para("", sect=sectpr("front")))
    parts += b.body
    body_xml = "".join(parts) + sectpr("body")
    document = f'{XML_HDR}<w:document {NS}><w:body>{body_xml}</w:body></w:document>'

    # --- relacoes / pacote ---
    rels = ['<Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>',
            '<Relationship Id="rIdNum" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>',
            '<Relationship Id="rIdSet" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>',
            '<Relationship Id="rIdHdr1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/header" Target="header1.xml"/>',
            '<Relationship Id="rIdFtr1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/>']
    for rid, fname, _ in b.media.items:
        rels.append(f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/{fname}"/>')
    for url, rid in EXT_LINKS.items():
        rels.append(f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink" '
                    f'Target="{esc(url)}" TargetMode="External"/>')
    doc_rels = (f'{XML_HDR}<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                + "".join(rels) + "</Relationships>")
    ct = (f'{XML_HDR}<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          '<Default Extension="xml" ContentType="application/xml"/>'
          '<Default Extension="png" ContentType="image/png"/>'
          '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
          '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
          '<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>'
          '<Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>'
          '<Override PartName="/word/header1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/>'
          '<Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>'
          '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
          '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>'
          '</Types>')
    root_rels = (f'{XML_HDR}<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                 '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
                 '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
                 '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>'
                 '</Relationships>')
    core = (f'{XML_HDR}<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
            'xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            f'<dc:title>{esc(DOC_TITLE)}</dc:title><dc:subject>{esc(DOC_SUB)}</dc:subject>'
            f'<cp:keywords>{DOC_CODE}; Python; PyQt6; Qt6; GUI</cp:keywords>'
            f'<dc:description>{DOC_CODE} Rev. {esc(REV_DESC)}</dc:description>'
            f'<dc:creator>{esc(AUTOR)}</dc:creator><cp:lastModifiedBy>{esc(AUTOR)}</cp:lastModifiedBy>'
            '<cp:revision>1</cp:revision>'
            '<dcterms:created xsi:type="dcterms:W3CDTF">2026-11-11T12:00:00Z</dcterms:created>'
            '<dcterms:modified xsi:type="dcterms:W3CDTF">2026-11-12T12:00:00Z</dcterms:modified>'
            '</cp:coreProperties>')
    app = (f'{XML_HDR}<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
           'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
           '<Application>Microsoft Office Word</Application><DocSecurity>0</DocSecurity></Properties>')

    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", ct)
        z.writestr("_rels/.rels", root_rels)
        z.writestr("word/document.xml", document)
        z.writestr("word/_rels/document.xml.rels", doc_rels)
        z.writestr("word/styles.xml", styles_xml())
        z.writestr("word/numbering.xml", numbering_xml(b.num_lists))
        z.writestr("word/settings.xml", settings_xml())
        z.writestr("word/header1.xml", header_xml())
        z.writestr("word/footer1.xml", footer_xml())
        z.writestr("docProps/core.xml", core)
        z.writestr("docProps/app.xml", app)
        for _, fname, path in b.media.items:
            z.write(path, f"word/media/{fname}")

    meta = {"order": front_b.order + b.order,
            "toc": [(lvl, num, title, bm) for (lvl, num, title, bm) in front_b.toc + b.toc],
            "caps": b.caps,
            "front_bms": [bm for (_, bm) in front_b.order],
            "lang": LANG, "toc_title": S["toc"],
            "body_start": f"{S['part']} I — {O.BODY[0]['title']}"}
    json.dump(meta, open(out_path + ".meta.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"OK {out_path}: {len(b.toc) + len(front_b.toc)} títulos, "
          f"{len(b.caps[KF])} figuras, {len(b.caps[KT])} tabelas, {len(b.caps[KL])} listagens, "
          f"{len(b.media.items)} imagens")


if __name__ == "__main__":
    out = sys.argv[1]
    pages = json.load(open(sys.argv[2], encoding="utf-8")) if len(sys.argv) > 2 else {}
    build(out, pages)
