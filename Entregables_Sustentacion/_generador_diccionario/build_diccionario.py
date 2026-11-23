# -*- coding: utf-8 -*-
"""Arma AdMind_Diccionario_de_Datos.docx a partir de diccionario_datos.md.

Escribe el OOXML a mano (sin librerias externas): solo biblioteca estandar.
Uso: python -I build_diccionario.py <salida.docx> [integrantes separados por |] [--sin-seccion5]
"""
import json
import os
import re
import sys
import zipfile
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
MD = r"C:\Users\Alejandro\Documents\A D M I N D\Documentacion\Admind_Documentacion\10_Sustentacion\datos\diccionario_datos.md"
LOGO = os.path.join(HERE, "logo-marca.png")
OVERRIDES = os.path.join(HERE, "descripciones.json")  # opcional (paso 5 del plan)

args = [a for a in sys.argv[1:] if not a.startswith("--")]
flags = [a for a in sys.argv[1:] if a.startswith("--")]
OUT = args[0]
INTEGRANTES = args[1].split("|") if len(args) > 1 else ["MANUEL ALEJANDRO ALDANA RINCON", "ANDERSON CAMILO REMISO NIÑO"]
SECCION5 = "--sin-seccion5" not in flags

# ---------------------------------------------------------------- estilo
V600, V700, V900, V50 = "0E6B5A", "0B5546", "06302A", "EEF5F2"
G950, G500, G200 = "14201D", "64706C", "D6DCDA"
AMB_BG, AMB_TX = "FBF0DC", "6B4A05"
BODY, CODE = "Calibri", "Consolas"  # Archivo e Inter no estan instaladas
TITULO_DOC = "Diccionario de Datos"
SUBTITULO = "AdMind \u2014 Plataforma de administraci\u00f3n de conjuntos residenciales"
FECHA = "14 de noviembre de 2026"

# Geometria (DXA). Todo el documento es carta vertical.
PW, PH = 12240, 15840
MARG_V = 1440
TW_P = PW - 2 * MARG_V            # 9360 texto vertical
TW_L = TW_P                       # ya no hay paginas horizontales: todo es carta vertical


# ---------------------------------------------------------------- lectura
def parse(path):
    lines = open(path, encoding="utf-8").read().split("\n")
    i = lines.index("---", 1) + 1 if lines[0].strip() == "---" else 0
    doc = {"facts": [], "conv": [], "modules": [], "anexo": None}
    section = None
    module = table = None
    in_restr = False
    for line in lines[i:]:
        s = line.rstrip()
        if s.startswith("# "):
            section = "facts"
            continue
        if s.startswith("## "):
            name = s[3:].strip()
            in_restr, table = False, None
            if name == "Convenciones":
                section = "conv"
            else:
                module = {"name": name, "desc": "", "tables": []}
                if name.startswith("Anexo"):
                    doc["anexo"] = module
                else:
                    doc["modules"].append(module)
                section = "module"
            continue
        if s.startswith("### "):
            table = {"name": s[4:].strip().strip("`"), "desc": [], "model": None,
                     "cols": [], "restr": []}
            module["tables"].append(table)
            in_restr = False
            continue
        if not s:
            continue
        if section == "facts" and s.startswith("- "):
            doc["facts"].append(s[2:])
        elif section == "conv" and s.startswith("- "):
            doc["conv"].append(s[2:])
        elif section == "module":
            if table is None:
                module["desc"] = (module["desc"] + " " + s).strip()
            elif s.startswith("|"):
                cells = [c.strip() for c in s.strip().strip("|").split("|")]
                if cells[0] == "Columna" or set(cells[0]) <= set("-: "):
                    continue
                assert len(cells) == 5, s
                table["cols"].append({"name": cells[0].strip("`"), "type": cells[1],
                                      "null": cells[2], "key": cells[3], "desc": cells[4]})
            elif s.startswith("Modelo de Django:"):
                table["model"] = s.split("`")[1]
            elif s.startswith("**Restricciones"):
                in_restr = True
            elif in_restr and s.startswith("- "):
                table["restr"].append(s[2:])
            else:
                table["desc"].append(s)
    return doc


def limpiar_desc(t):
    """Retoques de forma (no de datos): marcas de Sphinx y el punto doble."""
    t = re.sub(r":(?:class|func|meth|mod):`~?", "`", t)
    t = t.replace(".. Valores:", ". Valores:")
    return t


# ---------------------------------------------------------------- XML basico
NS = ('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
      'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
      'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
      'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
      'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"')
HEAD = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'


def rpr(font=None, size=None, bold=False, italic=False, color=None, caps=False, spacing=None):
    p = []
    if font:
        p.append(f'<w:rFonts w:ascii="{font}" w:hAnsi="{font}" w:eastAsia="{font}" w:cs="{font}"/>')
    if bold:
        p.append("<w:b/><w:bCs/>")
    if italic:
        p.append("<w:i/><w:iCs/>")
    if caps:
        p.append("<w:caps/>")
    if color:
        p.append(f'<w:color w:val="{color}"/>')
    if spacing:
        p.append(f'<w:spacing w:val="{spacing}"/>')
    if size:
        p.append(f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>')
    return "<w:rPr>" + "".join(p) + "</w:rPr>" if p else ""


def run(text, **kw):
    return f'<w:r>{rpr(**kw)}<w:t xml:space="preserve">{escape(text)}</w:t></w:r>'


TOKEN = re.compile(r"(\*\*[^*]+\*\*|`[^`]+`)")


def inline(text, size=22, code_size=None, color=None, bold=False, italic=False):
    code_size = code_size or size
    out = []
    for part in TOKEN.split(text):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**") and len(part) > 4:
            out.append(run(part[2:-2], size=size, bold=True, color=color, italic=italic))
        elif part.startswith("`") and part.endswith("`") and len(part) > 2:
            out.append(run(part[1:-1], font=CODE, size=code_size, color=color, bold=bold))
        else:
            out.append(run(part, size=size, bold=bold, color=color, italic=italic))
    return "".join(out)


def para(content="", style=None, jc=None, keep_next=False, keep_lines=False, before=None,
         after=None, line=None, line_rule=None, ind_left=None, ind_right=None, hanging=None,
         num=None, shd=None, bdr_bottom=None, bdr_top=None, page_break=False, sect=None,
         tabs=None):
    p = []
    if style:
        p.append(f'<w:pStyle w:val="{style}"/>')
    if keep_next:
        p.append("<w:keepNext/>")
    if keep_lines:
        p.append("<w:keepLines/>")
    if page_break:
        p.append("<w:pageBreakBefore/>")
    if num is not None:
        p.append(f'<w:numPr><w:ilvl w:val="0"/><w:numId w:val="{num}"/></w:numPr>')
    if bdr_bottom or bdr_top:
        b = ""
        if bdr_top:
            b += f'<w:top w:val="single" w:sz="{bdr_top[0]}" w:space="4" w:color="{bdr_top[1]}"/>'
        if bdr_bottom:
            b += f'<w:bottom w:val="single" w:sz="{bdr_bottom[0]}" w:space="4" w:color="{bdr_bottom[1]}"/>'
        p.append(f"<w:pBdr>{b}</w:pBdr>")
    if shd:
        p.append(f'<w:shd w:val="clear" w:color="auto" w:fill="{shd}"/>')
    if tabs:
        p.append("<w:tabs>" + "".join(
            f'<w:tab w:val="{v}" w:pos="{pos}"/>' for v, pos in tabs) + "</w:tabs>")
    sp = ""
    if before is not None:
        sp += f' w:before="{before}"'
    if after is not None:
        sp += f' w:after="{after}"'
    if line is not None:
        sp += f' w:line="{line}" w:lineRule="{line_rule or "auto"}"'
    if sp:
        p.append(f"<w:spacing{sp}/>")
    ind = ""
    if ind_left is not None:
        ind += f' w:left="{ind_left}"'
    if ind_right is not None:
        ind += f' w:right="{ind_right}"'
    if hanging is not None:
        ind += f' w:hanging="{hanging}"'
    if ind:
        p.append(f"<w:ind{ind}/>")
    if jc:
        p.append(f'<w:jc w:val="{jc}"/>')
    if sect:
        p.append(sect)
    ppr = "<w:pPr>" + "".join(p) + "</w:pPr>" if p else ""
    return f"<w:p>{ppr}{content}</w:p>"


def h1(text, page_break=False):
    return para(run(text), style="Heading1", page_break=page_break)


def h2(text):
    return para(run(text), style="Heading2")


def h3_code(text):
    return para(run(text, font=CODE), style="Heading3")


def bullet(content, size=22):
    return para(content, style="Vineta", num=1)


def drawing(rid, cx, cy, did, name):
    return (
        f'<w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0">'
        f'<wp:extent cx="{cx}" cy="{cy}"/><wp:docPr id="{did}" name="{name}" descr="Logo de AdMind"/>'
        f'<wp:cNvGraphicFramePr><a:graphicFrameLocks noChangeAspect="1"/></wp:cNvGraphicFramePr>'
        f'<a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        f'<pic:pic><pic:nvPicPr><pic:cNvPr id="{did}" name="{name}"/><pic:cNvPicPr/></pic:nvPicPr>'
        f'<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
        f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
        f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic>'
        f'</a:graphicData></a:graphic></wp:inline></w:drawing></w:r>')


def field(instr, cached="1", **kw):
    r = rpr(**kw)
    return (f'<w:r>{r}<w:fldChar w:fldCharType="begin"/></w:r>'
            f'<w:r>{r}<w:instrText xml:space="preserve"> {instr} </w:instrText></w:r>'
            f'<w:r>{r}<w:fldChar w:fldCharType="separate"/></w:r>'
            f'<w:r>{r}<w:t>{cached}</w:t></w:r>'
            f'<w:r>{r}<w:fldChar w:fldCharType="end"/></w:r>')


# ---------------------------------------------------------------- tablas
def borders_xml(color=G200, sz=4, inside=True):
    names = ["top", "left", "bottom", "right"] + (["insideH", "insideV"] if inside else [])
    return "<w:tblBorders>" + "".join(
        f'<w:{n} w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>' for n in names
    ) + "</w:tblBorders>"


def tcell(width, content, fill=None, valign="center", borders=None, mar=None):
    pr = f'<w:tcW w:w="{width}" w:type="dxa"/>'
    if borders:
        pr += f"<w:tcBorders>{borders}</w:tcBorders>"
    if fill:
        pr += f'<w:shd w:val="clear" w:color="auto" w:fill="{fill}"/>'
    if mar:
        pr += ("<w:tcMar>" + "".join(
            f'<w:{k} w:w="{v}" w:type="dxa"/>' for k, v in mar) + "</w:tcMar>")
    pr += f'<w:vAlign w:val="{valign}"/>'
    return f"<w:tc><w:tcPr>{pr}</w:tcPr>{content}</w:tc>"


def trow(cells, header=False):
    pr = "<w:cantSplit/>" + ("<w:tblHeader/>" if header else "")
    return f"<w:tr><w:trPr>{pr}</w:trPr>{''.join(cells)}</w:tr>"


def table(widths, rows, cell_mar=(40, 100, 40, 100), borders=None):
    top, left, bottom, right = cell_mar
    grid = "".join(f'<w:gridCol w:w="{w}"/>' for w in widths)
    return (
        f'<w:tbl><w:tblPr><w:tblW w:w="{sum(widths)}" w:type="dxa"/>'
        f'{borders if borders is not None else borders_xml()}'
        f'<w:tblLayout w:type="fixed"/>'
        f'<w:tblCellMar><w:top w:w="{top}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tblCellMar>'
        f'<w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" w:firstColumn="1" '
        f'w:lastColumn="0" w:noHBand="0" w:noVBand="1"/></w:tblPr>'
        f"<w:tblGrid>{grid}</w:tblGrid>{''.join(rows)}</w:tbl>")


COLS_W = [2350, 1600, 620, 1550, 3240]  # suma 9360 = TW_P
COLS_H = ["Columna", "Tipo", "Nulo", "Llave", "Descripci\u00f3n y valores permitidos"]


def cols_table(cols, compact=False):
    sz = 16 if compact else 17           # Consolas
    sb = 16 if compact else 18           # Calibri
    mar = (20, 90, 20, 90) if compact else (40, 100, 40, 100)
    head = trow([
        tcell(w, para(run(h, size=sb, bold=True, color="FFFFFF"), keep_next=True, after=0,
                      line=240, jc="center" if h == "Nulo" else None), fill=V600)
        for w, h in zip(COLS_W, COLS_H)], header=True)
    rows = [head]
    for i, c in enumerate(cols):
        fill = V50 if i % 2 == 1 else None
        kn = i == 0  # el primer renglon se queda pegado al encabezado

        def cp(content, jc=None):
            return para(content, keep_next=kn, after=0, line=240, jc=jc)
        cells = [
            tcell(COLS_W[0], cp(run(c["name"], font=CODE, size=sz)), fill),
            tcell(COLS_W[1], cp(run(c["type"], font=CODE, size=sz)), fill),
            tcell(COLS_W[2], cp(run(c["null"], font=CODE, size=sz), jc="center"), fill),
            tcell(COLS_W[3], cp(inline(c["key"], size=sb, code_size=sz)), fill),
            tcell(COLS_W[4], cp(inline(c["desc"], size=sb, code_size=sz)), fill),
        ]
        rows.append(trow(cells))
    return table(COLS_W, rows, cell_mar=mar)


RE_R = re.compile(r"^(\u00danica|CHECK|\u00cdndice|Llave for\u00e1nea compuesta) `([^`]+)`: (.*)$")


def restr_par(line):
    m = RE_R.match(line)
    assert m, line
    kind, name, rest = m.groups()
    if rest.startswith("`") and rest.endswith("`"):
        rest = rest[1:-1]
    runs = (run(kind + " ", size=18, bold=True, color=V900)
            + run(name, font=CODE, size=16, color=V700)
            + run(": ", size=18)
            + run(rest, font=CODE, size=16))
    return para(runs, style="Vineta", num=1, after=20, line=252)


def table_block(t, compact=False):
    out = [h3_code(t["name"])]
    desc = limpiar_desc(" ".join(t["desc"])).strip()
    if desc:
        out.append(para(inline(desc, size=20 if not compact else 18,
                               color=None if not compact else G500),
                        keep_next=True, after=40, line=252))
    if t["model"]:
        out.append(para(run("Modelo de Django: ", size=20 if not compact else 18, bold=True,
                            color=V900) + run(t["model"], font=CODE, size=18 if not compact else 16),
                        keep_next=True, after=80, line=252))
    out.append(cols_table(t["cols"], compact))
    if t["restr"]:
        out.append(para(run("Restricciones de la tabla", size=18, bold=True, color=V700),
                        keep_next=True, before=100, after=30))
        for r in t["restr"]:
            out.append(restr_par(r))
    else:
        out.append(para("", after=0, line=120, line_rule="exact"))
    return out


def callout(width, title, body_runs, fill, bar, title_color, size=21):
    border = (f'<w:top w:val="nil"/><w:left w:val="single" w:sz="36" w:space="0" w:color="{bar}"/>'
              f'<w:bottom w:val="nil"/><w:right w:val="nil"/>')
    content = (para(run(title, size=size, bold=True, color=title_color), keep_next=True,
                    after=60, keep_lines=True)
               + para(body_runs, after=0, keep_lines=True))
    cell = tcell(width, content, fill=fill, valign="top", borders=border,
                 mar=[("top", 120), ("left", 200), ("bottom", 120), ("right", 200)])
    return table([width], [trow([cell])],
                 borders='<w:tblBorders><w:top w:val="nil"/><w:left w:val="nil"/><w:bottom w:val="nil"/>'
                         '<w:right w:val="nil"/></w:tblBorders>', cell_mar=(0, 0, 0, 0))


def cifras(items, width):
    n = len(items)
    w = width // n
    widths = [w] * n
    widths[-1] += width - w * n
    white = ('<w:top w:val="single" w:sz="24" w:space="0" w:color="FFFFFF"/>'
             '<w:left w:val="single" w:sz="24" w:space="0" w:color="FFFFFF"/>'
             '<w:bottom w:val="single" w:sz="24" w:space="0" w:color="FFFFFF"/>'
             '<w:right w:val="single" w:sz="24" w:space="0" w:color="FFFFFF"/>')
    cells = []
    for wd, (num, label) in zip(widths, items):
        c = (para(run(str(num), size=44, bold=True, color=V900), jc="center", after=0, line=240,
                  keep_next=True)
             + para(run(label, size=17, color=G500), jc="center", after=0, line=240))
        cells.append(tcell(wd, c, fill=V50, borders=white,
                           mar=[("top", 120), ("left", 60), ("bottom", 120), ("right", 60)]))
    return table(widths, [trow(cells)], cell_mar=(0, 0, 0, 0),
                 borders='<w:tblBorders><w:top w:val="nil"/><w:left w:val="nil"/>'
                         '<w:bottom w:val="nil"/><w:right w:val="nil"/></w:tblBorders>')


# ---------------------------------------------------------------- secciones
def sect(kind, hdr, ftr, title_pg=False):
    """sectPr. kind: 'p' o 'l' (ambas carta vertical, con el mismo margen), 'c' portada."""
    refs = (f'<w:headerReference w:type="default" r:id="{hdr}"/>'
            f'<w:footerReference w:type="default" r:id="{ftr}"/>')
    size = f'<w:pgSz w:w="{PW}" w:h="{PH}"/>'
    mar = (f'<w:pgMar w:top="{MARG_V}" w:right="{MARG_V}" w:bottom="1300" w:left="{MARG_V}" '
           f'w:header="454" w:footer="454" w:gutter="0"/>')
    if kind == "c":
        mar = (f'<w:pgMar w:top="{MARG_V}" w:right="{MARG_V}" w:bottom="{MARG_V}" '
               f'w:left="{MARG_V}" w:header="0" w:footer="0" w:gutter="0"/>')
    return (f'<w:sectPr>{refs}<w:type w:val="nextPage"/>{size}{mar}'
            f'<w:cols w:space="708"/></w:sectPr>')


def band(fill, exact, left=-MARG_V, right=-MARG_V):
    return para("", shd=fill, before=0, after=0, line=exact, line_rule="exact",
                ind_left=left, ind_right=right)


def build(doc):
    mods = doc["modules"]
    anexo = doc["anexo"]
    n_neg = sum(len(m["tables"]) for m in mods)
    n_fw = len(anexo["tables"])
    n_cols = sum(len(t["cols"]) for m in mods + [anexo] for t in m["tables"])
    n_pk = sum(1 for m in mods + [anexo] for t in m["tables"] for c in t["cols"]
               if re.match(r"^PK\b", c["key"]))

    facts = " ".join(doc["facts"])
    m = re.search(r"(\d+) en total: (\d+) del negocio y (\d+) del framework", facts)
    assert (int(m[1]), int(m[2]), int(m[3])) == (n_neg + n_fw, n_neg, n_fw), (m.groups(), n_neg, n_fw)
    m = re.search(r"(\d+) llaves primarias, (\d+) llaves for\u00e1neas, (\d+) \u00fanicas y (\d+) CHECK", facts)
    pk, fk, uq, ck = (int(x) for x in m.groups())
    assert pk == n_pk == n_neg + n_fw, (pk, n_pk)
    m = re.search(r"backend en `main` `(\w+)`", facts)
    commit = m.group(1)
    m = re.search(r"PostgreSQL ([\d.]+)", facts)
    pgver = m.group(1)
    tot_tablas = n_neg + n_fw
    assert (tot_tablas, n_cols) == (42, 352), (tot_tablas, n_cols)
    assert re.search(r"Triggers:\*\* 0", facts) and re.search(r"funciones:\*\* 0", facts)

    body = []

    # ---- Portada (seccion 1)
    cover = []
    cover.append(para(drawing("rIdLogo", 1800000, 1800000, 1, "logo-marca.png"), jc="center",
                      before=900, after=0))
    cover.append(para(run(TITULO_DOC, size=80, bold=True, color=V900), jc="center",
                      before=420, after=120, line=240))
    cover.append(para("", ind_left=3300, ind_right=3300, bdr_bottom=(18, V600), after=240,
                      line=120, line_rule="exact", jc="center"))
    cover.append(para(run(SUBTITULO, size=28, color=V700), jc="center", after=0,
                      ind_left=700, ind_right=700))

    def bloque(label, lineas, before):
        out = [para(run(label, size=18, bold=True, color=G500, caps=True, spacing=40),
                    jc="center", before=before, after=60)]
        for txt, size, bold, color in lineas:
            out.append(para(run(txt, size=size, bold=bold, color=color), jc="center", after=20))
        return out
    cover += bloque("Integrantes", [(n, 28, True, V900) for n in INTEGRANTES], 1500)
    cover += bloque("Asignatura", [("Ingenier\u00eda de Software II", 26, False, G950),
                                   ("Docente: Oscar G\u00f3mez", 24, False, G950),
                                   ("Universidad de Cundinamarca", 24, False, G950)], 500)
    cover += bloque("Fecha", [(FECHA, 26, False, G950)], 500)
    # ultimo parrafo de la portada lleva el sectPr de la seccion 1
    cover.append(para("", after=0, line=120, line_rule="exact", sect=sect("c", "rIdHdrC", "rIdFtrC")))
    body += cover

    # ---- Seccion 2 (vertical): TOC, introduccion, convenciones
    body.append(para(run("Tabla de contenido"), style="TOCTitulo"))
    toc = (f'<w:r><w:fldChar w:fldCharType="begin"/></w:r>'
           f'<w:r><w:instrText xml:space="preserve"> TOC \\o "1-2" \\h \\z \\u </w:instrText></w:r>'
           f'<w:r><w:fldChar w:fldCharType="separate"/></w:r>'
           f'<w:r><w:t>Abra el documento en Word y actualice el campo para ver la tabla de contenido.</w:t></w:r>'
           f'<w:r><w:fldChar w:fldCharType="end"/></w:r>')
    body.append(para(toc))

    body.append(h1("1. Introducci\u00f3n", page_break=True))
    body.append(para(
        inline("Este documento describe las tablas de la base de datos de AdMind: para cada una, sus "
               "columnas con el tipo de dato, si admiten nulos y qu\u00e9 llaves tienen, y las "
               "restricciones que la propia base aplica. Sirve para entender c\u00f3mo se guardan los "
               "datos del sistema sin abrir el c\u00f3digo.")))
    body.append(para(
        inline(f"El motor es PostgreSQL {pgver} y la base se llama `admind_db`. El contenido no se "
               "escribi\u00f3 a mano: se gener\u00f3 consultando `information_schema` y `pg_catalog` de la "
               "base real y cruzando el resultado con los modelos de Django, de donde salen los "
               "nombres legibles y las descripciones. Por eso coincide con la base de datos y no con "
               f"una descripci\u00f3n aparte. El corte es del 14 de noviembre de 2026, con el backend en la "
               f"rama `main`, commit `{commit}`.")))
    body.append(para(inline("En cifras:"), keep_next=True, after=80))
    body.append(cifras([(tot_tablas, "tablas"), (n_cols, "columnas"), (pk, "llaves primarias"),
                        (fk, "llaves for\u00e1neas"), (uq, "\u00fanicas"), (ck, "CHECK")], TW_P))
    body.append(para("", after=0, line=160, line_rule="exact"))
    body.append(para(
        inline(f"De las {tot_tablas} tablas, {n_neg} son del negocio, repartidas en {len(mods)} m\u00f3dulos "
               f"(secci\u00f3n 3), y {n_fw} son del framework (anexo, secci\u00f3n 4). La base no tiene "
               "triggers ni procedimientos almacenados (secci\u00f3n 5).")))

    body.append(h1("2. Convenciones"))
    for c in doc["conv"]:
        body.append(bullet(inline(c)))
    body.append(para("", after=0, line=120, line_rule="exact"))
    body.append(callout(
        TW_P, "La llave for\u00e1nea compuesta (id, conjunto_id)",
        inline("Las tablas de cada conjunto tienen una \u00fanica sobre `(id, conjunto_id)` y sus hijas "
               "apuntan a esa pareja, no solo al `id`. As\u00ed la base de datos rechaza por s\u00ed sola "
               "cualquier fila que mezcle datos de dos conjuntos, aunque la aplicaci\u00f3n fallara; en "
               "cada tabla aparece como \u00abLlave for\u00e1nea compuesta\u00bb.", size=21, color=V900),
        V50, V600, V900))
    body.append(para("", after=0, line=20, line_rule="exact",
                     sect=sect("p", "rIdHdrP", "rIdFtrP")))

    # ---- Seccion 3 (horizontal): tablas por modulo
    body.append(h1("3. Tablas por m\u00f3dulo"))
    body.append(para(inline(
        f"Las {n_neg} tablas del negocio est\u00e1n agrupadas en {len(mods)} m\u00f3dulos. De cada una se "
        "muestran sus columnas y, debajo, las restricciones que la base le aplica.")))
    for mi, mod in enumerate(mods, 1):
        body.append(h2(f"3.{mi} {mod['name']}"))
        if mod["desc"]:
            body.append(para(inline(mod["desc"]), keep_next=True, after=60))
        for t in mod["tables"]:
            body += table_block(t)

    # ---- Anexo
    body.append(h1("4. Anexo: tablas del framework", page_break=True))
    body.append(para(inline(limpiar_desc(anexo["desc"])), after=60))
    body.append(para(run("Las descripciones de estas tablas vienen de la documentaci\u00f3n de cada "
                         "librer\u00eda y se dejan en su idioma original.", size=20, italic=True,
                         color=G500), after=60))
    for t in anexo["tables"]:
        body += table_block(t, compact=True)
    body.append(para("", after=0, line=20, line_rule="exact",
                     sect=sect("l", "rIdHdrL", "rIdFtrL")))

    # ---- Seccion 5 (vertical, final)
    if SECCION5:
        body.append(h1("5. Objetos programados en la base"))
        body.append(para(inline(
            "Hoy `admind_db` no tiene triggers, procedimientos almacenados ni funciones propias. La "
            "integridad de los datos la sostienen las restricciones de cada tabla: llaves for\u00e1neas "
            "compuestas, \u00fanicas, \u00edndices \u00fanicos parciales y CHECK (secci\u00f3n 3). El resto de las "
            "reglas corre en el backend.")))
        body.append(para("", after=0, line=120, line_rule="exact"))
        body.append(callout(
            TW_P, "En implementaci\u00f3n",
            inline("5 procedimientos almacenados y 5 triggers (tarea C5), que se documentar\u00e1n en la "
                   "versi\u00f3n de la sustentaci\u00f3n.", size=21, color=AMB_TX),
            AMB_BG, AMB_TX, AMB_TX))
        body.append(para("", after=0, line=20, line_rule="exact"))
        final_sect = sect("p", "rIdHdrP", "rIdFtrP")
    else:
        # sin seccion 5: el ultimo sectPr (horizontal) pasa a ser el del cuerpo
        final_sect = sect("l", "rIdHdrL", "rIdFtrL")
        # quitar el sectPr del ultimo parrafo del anexo
        body[-1] = para("", after=0, line=20, line_rule="exact")
    return "".join(body), final_sect


# ---------------------------------------------------------------- partes
def styles_xml():
    def rfont(f):
        return f'<w:rFonts w:ascii="{f}" w:hAnsi="{f}" w:eastAsia="{f}" w:cs="{f}"/>'

    def heading(i, sz, color, before, after, outline, border=False):
        bdr = (f'<w:pBdr><w:bottom w:val="single" w:sz="8" w:space="4" w:color="{V600}"/></w:pBdr>'
               if border else "")
        return (f'<w:style w:type="paragraph" w:styleId="Heading{i}"><w:name w:val="heading {i}"/>'
                f'<w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:uiPriority w:val="9"/><w:qFormat/>'
                f'<w:pPr><w:keepNext/><w:keepLines/>{bdr}<w:spacing w:before="{before}" w:after="{after}"/>'
                f'<w:outlineLvl w:val="{outline}"/></w:pPr>'
                f'<w:rPr>{rfont(BODY)}<w:b/><w:bCs/><w:color w:val="{color}"/>'
                f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/></w:rPr></w:style>')
    return (
        HEAD + f'<w:styles {NS}>'
        f'<w:docDefaults><w:rPrDefault><w:rPr>{rfont(BODY)}<w:color w:val="{G950}"/>'
        f'<w:sz w:val="22"/><w:szCs w:val="22"/><w:lang w:val="es-CO" w:eastAsia="es-CO" w:bidi="ar-SA"/>'
        f'</w:rPr></w:rPrDefault><w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="276" '
        f'w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>'
        '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/></w:style>'
        '<w:style w:type="character" w:default="1" w:styleId="DefaultParagraphFont">'
        '<w:name w:val="Default Paragraph Font"/><w:uiPriority w:val="1"/><w:semiHidden/><w:unhideWhenUsed/></w:style>'
        '<w:style w:type="table" w:default="1" w:styleId="TableNormal"><w:name w:val="Normal Table"/>'
        '<w:uiPriority w:val="99"/><w:semiHidden/><w:unhideWhenUsed/><w:tblPr><w:tblInd w:w="0" w:type="dxa"/>'
        '<w:tblCellMar><w:top w:w="0" w:type="dxa"/><w:left w:w="108" w:type="dxa"/>'
        '<w:bottom w:w="0" w:type="dxa"/><w:right w:w="108" w:type="dxa"/></w:tblCellMar></w:tblPr></w:style>'
        '<w:style w:type="numbering" w:default="1" w:styleId="NoList"><w:name w:val="No List"/>'
        '<w:uiPriority w:val="99"/><w:semiHidden/><w:unhideWhenUsed/></w:style>'
        + heading(1, 40, V600, 360, 160, 0, border=True)
        + heading(2, 30, V700, 300, 100, 1)
        + heading(3, 24, V700, 260, 60, 2)
        + f'<w:style w:type="paragraph" w:customStyle="1" w:styleId="TOCTitulo"><w:name w:val="TOC Titulo"/>'
          f'<w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/>'
          f'<w:pPr><w:keepNext/><w:pBdr><w:bottom w:val="single" w:sz="8" w:space="4" w:color="{V600}"/></w:pBdr>'
          f'<w:spacing w:before="0" w:after="200"/></w:pPr>'
          f'<w:rPr><w:b/><w:bCs/><w:color w:val="{V600}"/><w:sz w:val="40"/><w:szCs w:val="40"/></w:rPr></w:style>'
        + f'<w:style w:type="paragraph" w:styleId="TOC1"><w:name w:val="toc 1"/><w:basedOn w:val="Normal"/>'
          f'<w:next w:val="Normal"/><w:autoRedefine/><w:uiPriority w:val="39"/><w:unhideWhenUsed/>'
          f'<w:pPr><w:tabs><w:tab w:val="right" w:leader="dot" w:pos="{TW_P - 10}"/></w:tabs>'
          f'<w:spacing w:before="160" w:after="40"/></w:pPr>'
          f'<w:rPr><w:b/><w:bCs/><w:color w:val="{V900}"/></w:rPr></w:style>'
        + f'<w:style w:type="paragraph" w:styleId="TOC2"><w:name w:val="toc 2"/><w:basedOn w:val="Normal"/>'
          f'<w:next w:val="Normal"/><w:autoRedefine/><w:uiPriority w:val="39"/><w:unhideWhenUsed/>'
          f'<w:pPr><w:tabs><w:tab w:val="right" w:leader="dot" w:pos="{TW_P - 10}"/></w:tabs>'
          f'<w:spacing w:before="0" w:after="20" w:line="252" w:lineRule="auto"/><w:ind w:left="240"/></w:pPr>'
          f'<w:rPr><w:sz w:val="21"/><w:szCs w:val="21"/></w:rPr></w:style>'
        + f'<w:style w:type="paragraph" w:styleId="Header"><w:name w:val="header"/><w:basedOn w:val="Normal"/>'
          f'<w:uiPriority w:val="99"/><w:unhideWhenUsed/><w:pPr><w:spacing w:after="0" w:line="240" '
          f'w:lineRule="auto"/></w:pPr><w:rPr><w:color w:val="{G500}"/><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr></w:style>'
        + f'<w:style w:type="paragraph" w:styleId="Footer"><w:name w:val="footer"/><w:basedOn w:val="Normal"/>'
          f'<w:uiPriority w:val="99"/><w:unhideWhenUsed/><w:pPr><w:spacing w:after="0" w:line="240" '
          f'w:lineRule="auto"/></w:pPr><w:rPr><w:color w:val="{G500}"/><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr></w:style>'
        + f'<w:style w:type="paragraph" w:customStyle="1" w:styleId="Vineta"><w:name w:val="Vineta AdMind"/>'
          f'<w:basedOn w:val="Normal"/><w:qFormat/><w:pPr><w:numPr><w:numId w:val="1"/></w:numPr>'
          f'<w:spacing w:after="60"/><w:ind w:left="360" w:hanging="240"/></w:pPr></w:style>'
        + f'<w:style w:type="character" w:styleId="Hyperlink"><w:name w:val="Hyperlink"/>'
          f'<w:basedOn w:val="DefaultParagraphFont"/><w:uiPriority w:val="99"/><w:unhideWhenUsed/>'
          f'<w:rPr><w:color w:val="{V700}"/></w:rPr></w:style>'
        + '</w:styles>')


def numbering_xml():
    return (HEAD + f'<w:numbering {NS}><w:abstractNum w:abstractNumId="0"><w:multiLevelType w:val="hybridMultilevel"/>'
            f'<w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="\u2022"/>'
            f'<w:lvlJc w:val="left"/><w:pPr><w:ind w:left="360" w:hanging="240"/></w:pPr>'
            f'<w:rPr><w:rFonts w:ascii="{BODY}" w:hAnsi="{BODY}" w:cs="{BODY}" w:hint="default"/>'
            f'<w:color w:val="{V600}"/></w:rPr></w:lvl></w:abstractNum>'
            f'<w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num></w:numbering>')


def settings_xml():
    return (HEAD + f'<w:settings {NS}><w:zoom w:percent="100"/><w:defaultTabStop w:val="708"/>'
            '<w:characterSpacingControl w:val="doNotCompress"/><w:compat><w:compatSetting '
            'w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" w:val="15"/>'
            '</w:compat></w:settings>')


def hdr_cover():
    return (HEAD + f'<w:hdr {NS}>' + band(V600, 1000) + band(V900, 140) + "</w:hdr>")


def ftr_cover():
    return (HEAD + f'<w:ftr {NS}>' + band(V900, 140) + band(V600, 500) + "</w:ftr>")


def hdr_main(width, did):
    p = para(
        drawing("rIdLogo", 360000, 360000, did, "logo-marca.png") + '<w:r><w:tab/></w:r>'
        + run("AdMind \u2014 " + TITULO_DOC, size=18, color=G500),
        style="Header", bdr_bottom=(8, V600), tabs=[("right", width)])
    return HEAD + f'<w:hdr {NS}>{p}</w:hdr>'


def ftr_main(width):
    p = para(
        run("AdMind \u00b7 Ingenier\u00eda de Software II \u00b7 2026", size=18, color=G500)
        + '<w:r><w:tab/></w:r>' + run("P\u00e1gina ", size=18, color=G500)
        + field("PAGE", size=18, color=G500) + run(" de ", size=18, color=G500)
        + field("NUMPAGES", "1", size=18, color=G500),
        style="Footer", bdr_top=(4, G200), tabs=[("right", width)])
    return HEAD + f'<w:ftr {NS}>{p}</w:ftr>'


def rels(items):
    return (HEAD + '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            + "".join(f'<Relationship Id="{i}" Type="{t}" Target="{g}"/>' for i, t, g in items)
            + "</Relationships>")


R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/"


def main():
    doc = parse(MD)
    # paso 5: descripciones de las columnas del negocio (salen de los modelos de Django).
    # Se conserva tal cual el sufijo "Valores: ..." que viene de la base.
    sys.path.insert(0, HERE)
    from desc_negocio import DESC, GEN
    sufijo = re.compile(r"\s*Valores:.*$")
    for m in doc["modules"]:
        for t in m["tables"]:
            for c in t["cols"]:
                nuevo = DESC.get(t["name"], {}).get(c["name"]) or GEN.get(c["name"])
                if nuevo:
                    suf = sufijo.search(c["desc"])
                    c["desc"] = nuevo + (" " + suf.group(0).strip() if suf else "")
    # control: cada clave de DESC apunta a una tabla y columna reales (sin errores de dedo)
    reales = {t["name"]: {c["name"] for c in t["cols"]} for m in doc["modules"] for t in m["tables"]}
    for tabla, cols in DESC.items():
        assert tabla in reales, f"tabla inexistente en DESC: {tabla}"
        for col in cols:
            assert col in reales[tabla], f"columna inexistente en DESC: {tabla}.{col}"
    sin_cambio = [f"{t['name']}.{c['name']}" for m in doc["modules"] for t in m["tables"]
                  for c in t["cols"]
                  if not (DESC.get(t["name"], {}).get(c["name"]) or GEN.get(c["name"]))]
    print("columnas del negocio sin descripcion nueva:", len(sin_cambio), sin_cambio)
    for m in doc["modules"] + [doc["anexo"]]:
        for t in m["tables"]:
            for c in t["cols"]:
                c["desc"] = limpiar_desc(c["desc"])

    body, final_sect = build(doc)
    document = (HEAD + f'<w:document {NS}><w:body>{body}{final_sect}</w:body></w:document>')

    logo = open(LOGO, "rb").read()
    ct = (HEAD + '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          '<Default Extension="xml" ContentType="application/xml"/>'
          '<Default Extension="png" ContentType="image/png"/>'
          '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
          '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
          '<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>'
          '<Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>'
          + "".join(f'<Override PartName="/word/{n}.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/>'
                    for n in ("headerC", "headerP", "headerL"))
          + "".join(f'<Override PartName="/word/{n}.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>'
                    for n in ("footerC", "footerP", "footerL"))
          + '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
          '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>'
          '</Types>')
    core = (HEAD + '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            f'<dc:title>AdMind \u2014 {TITULO_DOC}</dc:title><dc:creator>AdMind</dc:creator>'
            '<dc:language>es-CO</dc:language>'
            '<dcterms:created xsi:type="dcterms:W3CDTF">2026-11-14T00:00:00Z</dcterms:created>'
            '</cp:coreProperties>')
    app = (HEAD + '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">'
           '<Application>Microsoft Office Word</Application></Properties>')

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    if os.path.exists(OUT):
        os.remove(OUT)
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", ct)
        z.writestr("_rels/.rels", rels([
            ("rId1", R + "officeDocument", "word/document.xml"),
            ("rId2", "http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties", "docProps/core.xml"),
            ("rId3", R + "extended-properties", "docProps/app.xml")]))
        z.writestr("docProps/core.xml", core)
        z.writestr("docProps/app.xml", app)
        z.writestr("word/document.xml", document)
        z.writestr("word/_rels/document.xml.rels", rels([
            ("rIdSty", R + "styles", "styles.xml"),
            ("rIdNum", R + "numbering", "numbering.xml"),
            ("rIdSet", R + "settings", "settings.xml"),
            ("rIdLogo", R + "image", "media/logo-marca.png"),
            ("rIdHdrC", R + "header", "headerC.xml"), ("rIdFtrC", R + "footer", "footerC.xml"),
            ("rIdHdrP", R + "header", "headerP.xml"), ("rIdFtrP", R + "footer", "footerP.xml"),
            ("rIdHdrL", R + "header", "headerL.xml"), ("rIdFtrL", R + "footer", "footerL.xml")]))
        z.writestr("word/styles.xml", styles_xml())
        z.writestr("word/numbering.xml", numbering_xml())
        z.writestr("word/settings.xml", settings_xml())
        z.writestr("word/headerC.xml", hdr_cover())
        z.writestr("word/footerC.xml", ftr_cover())
        z.writestr("word/headerP.xml", hdr_main(TW_P, 2))
        z.writestr("word/footerP.xml", ftr_main(TW_P))
        z.writestr("word/headerL.xml", hdr_main(TW_L, 3))
        z.writestr("word/footerL.xml", ftr_main(TW_L))
        for n in ("headerP", "headerL"):
            z.writestr(f"word/_rels/{n}.xml.rels", rels([("rIdLogo", R + "image", "media/logo-marca.png")]))
        z.writestr("word/media/logo-marca.png", logo)
    print("ok:", OUT)


if __name__ == "__main__":
    main()
