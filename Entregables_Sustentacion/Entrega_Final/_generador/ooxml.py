# -*- coding: utf-8 -*-
"""Generador mínimo de .docx (WordprocessingML) con la biblioteca estándar.

No depende de paquetes externos: escribe el XML a mano y lo empaqueta con zipfile.
"""
import re
import zipfile
from xml.sax.saxutils import escape

# Paleta de AdMind (estilo_entregables.md)
V600 = "0E6B5A"
V700 = "0B5546"
V900 = "06302A"
V50 = "EEF5F2"
G950 = "14201D"
G500 = "64706C"
G200 = "D6DCDA"
AMBAR_BG = "FBF0DC"
AMBAR_TX = "6B4A05"
AMBAR_BORDE = "C28A1A"
BLANCO = "FFFFFF"

FUENTE = "Calibri"
MONO = "Consolas"

ANCHO_VERTICAL = 9360      # 12240 - 2 * 1440
ANCHO_HORIZONTAL = 13680   # 15840 - 2 * 1080

NS = (
    'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
    'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
    'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
    'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"'
)


def esc(texto):
    return escape(texto, {'"': "&quot;"})


# ---------------------------------------------------------------- runs

def rpr(bold=False, italic=False, color=None, size=None, mono=False, underline=False, caps=False):
    partes = []
    if mono:
        partes.append(f'<w:rFonts w:ascii="{MONO}" w:hAnsi="{MONO}" w:cs="{MONO}"/>')
    if bold:
        partes.append("<w:b/><w:bCs/>")
    if italic:
        partes.append("<w:i/><w:iCs/>")
    if caps:
        partes.append("<w:caps/>")
    if color:
        partes.append(f'<w:color w:val="{color}"/>')
    if size:
        partes.append(f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>')
    if underline:
        partes.append('<w:u w:val="single"/>')
    return f"<w:rPr>{''.join(partes)}</w:rPr>" if partes else ""


def run(texto, **kw):
    """Un run con saltos de línea (\\n) convertidos en <w:br/>."""
    pr = rpr(**kw)
    lineas = texto.split("\n")
    contenido = []
    for i, linea in enumerate(lineas):
        if i:
            contenido.append("<w:br/>")
        if linea:
            contenido.append(f'<w:t xml:space="preserve">{esc(linea)}</w:t>')
    return f"<w:r>{pr}{''.join(contenido)}</w:r>"


_TOKENS = re.compile(r"(`[^`]+`|\*\*.+?\*\*|\*[^*\s][^*]*?\*)")


def rich(texto, color=None, size=None, bold=False, italic=False, code_size=None, code_color=V900):
    """Texto con marcas: **negrita**, *cursiva* y `código`."""
    runs = []
    for trozo in _TOKENS.split(texto):
        if not trozo:
            continue
        if trozo.startswith("`") and trozo.endswith("`") and len(trozo) > 2:
            runs.append(run(trozo[1:-1], mono=True, color=code_color if color in (None, G950) else color,
                            size=code_size or size or 20, bold=bold))
        elif trozo.startswith("**") and trozo.endswith("**") and len(trozo) > 4:
            runs.append(run(trozo[2:-2], bold=True, italic=italic, color=color, size=size))
        elif trozo.startswith("*") and trozo.endswith("*") and len(trozo) > 2:
            runs.append(run(trozo[1:-1], italic=True, bold=bold, color=color, size=size))
        else:
            runs.append(run(trozo, bold=bold, italic=italic, color=color, size=size))
    return "".join(runs)


# ---------------------------------------------------------------- párrafos

def ppr(estilo=None, keep_next=False, keep_lines=False, page_break_before=False, num=None,
        borde=None, sombra=None, tabs=None, antes=None, despues=None, linea=None, sangria=None,
        alinear=None, contextual=False):
    partes = []
    if estilo:
        partes.append(f'<w:pStyle w:val="{estilo}"/>')
    if keep_next:
        partes.append("<w:keepNext/>")
    if keep_lines:
        partes.append("<w:keepLines/>")
    if page_break_before:
        partes.append("<w:pageBreakBefore/>")
    if num:
        partes.append(f'<w:numPr><w:ilvl w:val="{num[1]}"/><w:numId w:val="{num[0]}"/></w:numPr>')
    if borde:
        partes.append(f"<w:pBdr>{borde}</w:pBdr>")
    if sombra:
        partes.append(f'<w:shd w:val="clear" w:color="auto" w:fill="{sombra}"/>')
    if tabs:
        partes.append(f"<w:tabs>{tabs}</w:tabs>")
    if antes is not None or despues is not None or linea is not None:
        attrs = ""
        if antes is not None:
            attrs += f' w:before="{antes}"'
        if despues is not None:
            attrs += f' w:after="{despues}"'
        if linea is not None:
            attrs += f' w:line="{linea[0]}" w:lineRule="{linea[1]}"'
        partes.append(f"<w:spacing{attrs}/>")
    if sangria:
        izq, colg = sangria
        partes.append(f'<w:ind w:left="{izq}" w:hanging="{colg}"/>' if colg else f'<w:ind w:left="{izq}"/>')
    if contextual:
        partes.append("<w:contextualSpacing/>")
    if alinear:
        partes.append(f'<w:jc w:val="{alinear}"/>')
    return f"<w:pPr>{''.join(partes)}</w:pPr>" if partes else ""


def parrafo(contenido, **kw):
    """`contenido`: texto con marcas o XML de runs ya armado (si empieza con '<w:')."""
    if contenido.startswith("<w:"):
        runs = contenido
    else:
        runs = rich(contenido)
    return f"<w:p>{ppr(**kw)}{runs}</w:p>"


# ---------------------------------------------------------------- tablas

def borde_xml(lado, val="single", sz=4, color=G200, space=0):
    return f'<w:{lado} w:val="{val}" w:sz="{sz}" w:space="{space}" w:color="{color}"/>'


def bordes_tc(color=G200, sz=4, lados=("top", "left", "bottom", "right"), nulos=()):
    xml = []
    for lado in ("top", "left", "bottom", "right"):
        if lado in nulos:
            xml.append(f'<w:{lado} w:val="nil"/>')
        elif lado in lados:
            xml.append(borde_xml(lado, sz=sz, color=color))
    return f"<w:tcBorders>{''.join(xml)}</w:tcBorders>"


def celda(ancho, parrafos, fill=None, bordes=None, span=1, valign=None, margenes=None):
    pr = [f'<w:tcW w:w="{ancho}" w:type="dxa"/>']
    if span > 1:
        pr.append(f'<w:gridSpan w:val="{span}"/>')
    if bordes:
        pr.append(bordes)
    if fill:
        pr.append(f'<w:shd w:val="clear" w:color="auto" w:fill="{fill}"/>')
    if margenes:
        pr.append(margenes)
    if valign:
        pr.append(f'<w:vAlign w:val="{valign}"/>')
    return f"<w:tc><w:tcPr>{''.join(pr)}</w:tcPr>{parrafos}</w:tc>"


def fila(celdas, header=False, no_partir=True, alto=None):
    pr = []
    if no_partir:
        pr.append("<w:cantSplit/>")
    if alto:
        pr.append(f'<w:trHeight w:val="{alto}" w:hRule="atLeast"/>')
    if header:
        pr.append("<w:tblHeader/>")
    trpr = f"<w:trPr>{''.join(pr)}</w:trPr>" if pr else ""
    return f"<w:tr>{trpr}{''.join(celdas)}</w:tr>"


def tabla(filas, anchos, bordes_tabla=True, jc=None, margen_celda=(70, 110)):
    total = sum(anchos)
    arriba, lado = margen_celda
    bordes = ""
    if bordes_tabla:
        bordes = "<w:tblBorders>" + "".join(
            borde_xml(l, sz=4, color=G200) for l in ("top", "left", "bottom", "right", "insideH", "insideV")
        ) + "</w:tblBorders>"
    else:
        bordes = "<w:tblBorders>" + "".join(
            f'<w:{l} w:val="nil"/>' for l in ("top", "left", "bottom", "right", "insideH", "insideV")
        ) + "</w:tblBorders>"
    tblpr = (
        f'<w:tblPr><w:tblW w:w="{total}" w:type="dxa"/>'
        + (f'<w:jc w:val="{jc}"/>' if jc else "")
        + bordes
        + '<w:tblLayout w:type="fixed"/>'
        + f'<w:tblCellMar><w:top w:w="{arriba}" w:type="dxa"/><w:left w:w="{lado}" w:type="dxa"/>'
        f'<w:bottom w:w="{arriba}" w:type="dxa"/><w:right w:w="{lado}" w:type="dxa"/></w:tblCellMar></w:tblPr>'
    )
    grid = "<w:tblGrid>" + "".join(f'<w:gridCol w:w="{a}"/>' for a in anchos) + "</w:tblGrid>"
    return f"<w:tbl>{tblpr}{grid}{''.join(filas)}</w:tbl>"


# ---------------------------------------------------------------- imágenes

def imagen(rid, cx, cy, nombre, ident, descr=""):
    return (
        "<w:r><w:drawing>"
        f'<wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="{cx}" cy="{cy}"/>'
        f'<wp:docPr id="{ident}" name="{esc(nombre)}" descr="{esc(descr)}"/>'
        '<wp:cNvGraphicFramePr><a:graphicFrameLocks noChangeAspect="1"/></wp:cNvGraphicFramePr>'
        '<a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        f'<pic:pic><pic:nvPicPr><pic:cNvPr id="{ident}" name="{esc(nombre)}"/><pic:cNvPicPr/></pic:nvPicPr>'
        f'<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
        f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic>'
        "</a:graphicData></a:graphic></wp:inline></w:drawing></w:r>"
    )


def campo(instruccion, resultado="1", **kw):
    pr = rpr(**kw)
    return (
        f'<w:r>{pr}<w:fldChar w:fldCharType="begin"/></w:r>'
        f'<w:r>{pr}<w:instrText xml:space="preserve"> {instruccion} </w:instrText></w:r>'
        f'<w:r>{pr}<w:fldChar w:fldCharType="separate"/></w:r>'
        f'<w:r>{pr}<w:t>{esc(resultado)}</w:t></w:r>'
        f'<w:r>{pr}<w:fldChar w:fldCharType="end"/></w:r>'
    )


def hipervinculo(url, texto):
    """Enlace clicable (campo HYPERLINK) con el estilo Hyperlink."""
    pr = '<w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr>'
    return (
        '<w:r><w:fldChar w:fldCharType="begin"/></w:r>'
        f'<w:r><w:instrText xml:space="preserve"> HYPERLINK "{esc(url)}" </w:instrText></w:r>'
        '<w:r><w:fldChar w:fldCharType="separate"/></w:r>'
        f'<w:r>{pr}<w:t xml:space="preserve">{esc(texto)}</w:t></w:r>'
        '<w:r><w:fldChar w:fldCharType="end"/></w:r>'
    )


# ---------------------------------------------------------------- estilos

def _estilo_parrafo(sid, nombre, base="Normal", siguiente=None, ppr_xml="", rpr_xml="", q=True, ui=None):
    return (
        f'<w:style w:type="paragraph" w:styleId="{sid}"><w:name w:val="{nombre}"/>'
        + (f'<w:basedOn w:val="{base}"/>' if base else "")
        + (f'<w:next w:val="{siguiente}"/>' if siguiente else "")
        + (f'<w:uiPriority w:val="{ui}"/>' if ui is not None else "")
        + ("<w:qFormat/>" if q else "")
        + (f"<w:pPr>{ppr_xml}</w:pPr>" if ppr_xml else "")
        + (f"<w:rPr>{rpr_xml}</w:rPr>" if rpr_xml else "")
        + "</w:style>"
    )


def estilos_xml():
    def fuente(n=FUENTE):
        return f'<w:rFonts w:ascii="{n}" w:hAnsi="{n}" w:eastAsia="{n}" w:cs="{n}"/>'

    def tam(pt):
        return f'<w:sz w:val="{int(pt * 2)}"/><w:szCs w:val="{int(pt * 2)}"/>'

    partes = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        f"<w:styles {NS}>",
        "<w:docDefaults><w:rPrDefault><w:rPr>"
        + fuente()
        + f'<w:color w:val="{G950}"/>'
        + tam(11)
        + '<w:lang w:val="es-CO" w:eastAsia="es-CO" w:bidi="ar-SA"/>'
        + "</w:rPr></w:rPrDefault>"
        '<w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="276" w:lineRule="auto"/></w:pPr></w:pPrDefault>'
        "</w:docDefaults>",
        '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/></w:style>',
        '<w:style w:type="character" w:default="1" w:styleId="DefaultParagraphFont">'
        '<w:name w:val="Default Paragraph Font"/><w:uiPriority w:val="1"/><w:semiHidden/><w:unhideWhenUsed/></w:style>',
        '<w:style w:type="table" w:default="1" w:styleId="TableNormal"><w:name w:val="Normal Table"/>'
        '<w:uiPriority w:val="99"/><w:semiHidden/><w:unhideWhenUsed/><w:tblPr><w:tblInd w:w="0" w:type="dxa"/>'
        '<w:tblCellMar><w:top w:w="0" w:type="dxa"/><w:left w:w="108" w:type="dxa"/>'
        '<w:bottom w:w="0" w:type="dxa"/><w:right w:w="108" w:type="dxa"/></w:tblCellMar></w:tblPr></w:style>',
        '<w:style w:type="numbering" w:default="1" w:styleId="NoList"><w:name w:val="No List"/>'
        '<w:uiPriority w:val="99"/><w:semiHidden/><w:unhideWhenUsed/></w:style>',
        _estilo_parrafo(
            "Heading1", "heading 1", siguiente="Normal", ui=9,
            ppr_xml='<w:keepNext/><w:keepLines/><w:pageBreakBefore/>'
                    f'<w:pBdr><w:bottom w:val="single" w:sz="8" w:space="4" w:color="{V600}"/></w:pBdr>'
                    '<w:spacing w:before="0" w:after="240" w:line="240" w:lineRule="auto"/><w:outlineLvl w:val="0"/>',
            rpr_xml=f"<w:b/><w:bCs/><w:color w:val=\"{V600}\"/>{tam(22)}",
        ),
        _estilo_parrafo(
            "Heading2", "heading 2", siguiente="Normal", ui=9,
            ppr_xml='<w:keepNext/><w:keepLines/><w:spacing w:before="320" w:after="120" w:line="240" w:lineRule="auto"/>'
                    '<w:outlineLvl w:val="1"/>',
            rpr_xml=f"<w:b/><w:bCs/><w:color w:val=\"{V700}\"/>{tam(15)}",
        ),
        _estilo_parrafo(
            "Heading3", "heading 3", siguiente="Normal", ui=9,
            ppr_xml='<w:keepNext/><w:keepLines/><w:spacing w:before="220" w:after="80" w:line="240" w:lineRule="auto"/>'
                    '<w:outlineLvl w:val="2"/>',
            rpr_xml=f"<w:b/><w:bCs/><w:color w:val=\"{V700}\"/>{tam(12.5)}",
        ),
        _estilo_parrafo(
            "Title", "Title", siguiente="Normal", ui=10,
            ppr_xml='<w:spacing w:before="0" w:after="120" w:line="240" w:lineRule="auto"/><w:jc w:val="center"/>',
            rpr_xml=f"<w:b/><w:bCs/><w:color w:val=\"{V600}\"/>{tam(36)}",
        ),
        _estilo_parrafo(
            "Subtitle", "Subtitle", siguiente="Normal", ui=11,
            ppr_xml='<w:spacing w:before="0" w:after="120" w:line="276" w:lineRule="auto"/><w:jc w:val="center"/>',
            rpr_xml=f"<w:color w:val=\"{V900}\"/>{tam(14)}",
        ),
        _estilo_parrafo(
            "TituloContenido", "Titulo del contenido", siguiente="Normal",
            ppr_xml=f'<w:keepNext/><w:pBdr><w:bottom w:val="single" w:sz="8" w:space="4" w:color="{V600}"/></w:pBdr>'
                    '<w:spacing w:before="0" w:after="240" w:line="240" w:lineRule="auto"/>',
            rpr_xml=f"<w:b/><w:bCs/><w:color w:val=\"{V600}\"/>{tam(22)}",
        ),
        _estilo_parrafo(
            "TOC1", "toc 1", siguiente="Normal", ui=39, q=False,
            ppr_xml=f'<w:tabs><w:tab w:val="right" w:leader="dot" w:pos="{ANCHO_VERTICAL}"/></w:tabs>'
                    '<w:spacing w:before="140" w:after="40" w:line="240" w:lineRule="auto"/>',
            rpr_xml=f"<w:b/><w:bCs/><w:color w:val=\"{V900}\"/>",
        ),
        _estilo_parrafo(
            "TOC2", "toc 2", siguiente="Normal", ui=39, q=False,
            ppr_xml=f'<w:tabs><w:tab w:val="right" w:leader="dot" w:pos="{ANCHO_VERTICAL}"/></w:tabs>'
                    '<w:spacing w:before="0" w:after="20" w:line="240" w:lineRule="auto"/><w:ind w:left="320"/>',
            rpr_xml=tam(10.5),
        ),
        _estilo_parrafo(
            "Header", "header", ui=99, q=False,
            ppr_xml=f'<w:tabs><w:tab w:val="right" w:pos="{ANCHO_VERTICAL}"/></w:tabs>'
                    '<w:spacing w:after="0" w:line="240" w:lineRule="auto"/>',
            rpr_xml=f"<w:color w:val=\"{G500}\"/>{tam(9.5)}",
        ),
        _estilo_parrafo(
            "Footer", "footer", ui=99, q=False,
            ppr_xml=f'<w:tabs><w:tab w:val="right" w:pos="{ANCHO_VERTICAL}"/></w:tabs>'
                    '<w:spacing w:after="0" w:line="240" w:lineRule="auto"/>',
            rpr_xml=f"<w:color w:val=\"{G500}\"/>{tam(9)}",
        ),
        _estilo_parrafo(
            "Codigo", "Codigo", ui=20,
            ppr_xml=f'<w:keepLines/><w:pBdr><w:top w:val="single" w:sz="4" w:space="3" w:color="{G200}"/>'
                    f'<w:left w:val="single" w:sz="24" w:space="6" w:color="{V600}"/>'
                    f'<w:bottom w:val="single" w:sz="4" w:space="3" w:color="{G200}"/>'
                    f'<w:right w:val="single" w:sz="4" w:space="6" w:color="{G200}"/></w:pBdr>'
                    f'<w:shd w:val="clear" w:color="auto" w:fill="{V50}"/>'
                    '<w:spacing w:before="0" w:after="0" w:line="252" w:lineRule="auto"/><w:ind w:left="200" w:right="120"/>'
                    '<w:contextualSpacing/>',
            rpr_xml=f'<w:rFonts w:ascii="{MONO}" w:hAnsi="{MONO}" w:cs="{MONO}"/><w:color w:val="{V900}"/>{tam(10)}',
        ),
        _estilo_parrafo(
            "Pie", "Pie de figura", ui=21,
            ppr_xml='<w:spacing w:before="60" w:after="200" w:line="240" w:lineRule="auto"/>',
            rpr_xml=f"<w:i/><w:iCs/><w:color w:val=\"{G500}\"/>{tam(9.5)}",
        ),
        _estilo_parrafo(
            "Lista", "List Paragraph", ui=34,
            ppr_xml='<w:spacing w:after="60"/><w:contextualSpacing w:val="0"/>',
        ),
        '<w:style w:type="character" w:styleId="Hyperlink"><w:name w:val="Hyperlink"/>'
        '<w:uiPriority w:val="99"/><w:unhideWhenUsed/>'
        f'<w:rPr><w:color w:val="{V700}"/><w:u w:val="single"/></w:rPr></w:style>',
        "</w:styles>",
    ]
    return "".join(partes)


def numeracion_xml(instancias_numeradas):
    def nivel(i, fmt, texto, izq, colg, fuente=None):
        rf = ""
        if fuente:
            rf = f'<w:rPr><w:rFonts w:ascii="{fuente}" w:hAnsi="{fuente}" w:cs="{fuente}" w:hint="default"/></w:rPr>'
        return (
            f'<w:lvl w:ilvl="{i}"><w:start w:val="1"/><w:numFmt w:val="{fmt}"/><w:lvlText w:val="{texto}"/>'
            f'<w:lvlJc w:val="left"/><w:pPr><w:ind w:left="{izq}" w:hanging="{colg}"/></w:pPr>{rf}</w:lvl>'
        )

    viñetas = "".join([
        nivel(0, "bullet", "•", 500, 280, FUENTE),
        nivel(1, "bullet", "–", 900, 280, FUENTE),
        nivel(2, "bullet", "•", 1300, 280, FUENTE),
    ])
    numeros = "".join([
        nivel(0, "decimal", "%1.", 500, 360),
        nivel(1, "lowerLetter", "%2)", 900, 320),
        nivel(2, "lowerRoman", "%3.", 1300, 320),
    ])
    xml = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        f"<w:numbering {NS}>",
        f'<w:abstractNum w:abstractNumId="0"><w:multiLevelType w:val="hybridMultilevel"/>{viñetas}</w:abstractNum>',
        f'<w:abstractNum w:abstractNumId="1"><w:multiLevelType w:val="hybridMultilevel"/>{numeros}</w:abstractNum>',
        '<w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num>',
    ]
    for num_id in instancias_numeradas:
        xml.append(
            f'<w:num w:numId="{num_id}"><w:abstractNumId w:val="1"/>'
            '<w:lvlOverride w:ilvl="0"><w:startOverride w:val="1"/></w:lvlOverride></w:num>'
        )
    xml.append("</w:numbering>")
    return "".join(xml)


# ---------------------------------------------------------------- documento

class Doc:
    def __init__(self, titulo, autor, nombre_encabezado, logo_png):
        self.titulo = titulo
        self.autor = autor
        self.nombre_encabezado = nombre_encabezado
        self.logo = logo_png
        self.cuerpo = []
        self._num_ids = []
        self._siguiente_num = 2
        self._ident = 10
        self.secciones_cerradas = 0

    # --- utilidades
    def ident(self):
        self._ident += 1
        return self._ident

    def add(self, xml):
        self.cuerpo.append(xml)

    # --- bloques de texto
    def h1(self, texto):
        self.add(parrafo(texto, estilo="Heading1"))

    def h2(self, texto):
        self.add(parrafo(texto, estilo="Heading2"))

    def h3(self, texto):
        self.add(parrafo(texto, estilo="Heading3"))

    def p(self, texto, **kw):
        self.add(parrafo(texto, **kw))

    def pie(self, texto):
        self.add(parrafo(texto, estilo="Pie"))

    def vinetas(self, items, nivel=0):
        for item in items:
            if isinstance(item, (list, tuple)):
                self.vinetas(item, nivel + 1)
            else:
                self.add(parrafo(item, estilo="Lista", num=(1, nivel)))

    def numerada(self, items):
        num_id = self._siguiente_num
        self._siguiente_num += 1
        self._num_ids.append(num_id)
        for item in items:
            self.add(parrafo(item, estilo="Lista", num=(num_id, 0)))

    def codigo(self, lineas):
        if isinstance(lineas, str):
            lineas = lineas.split("\n")
        for i, linea in enumerate(lineas):
            contenido = run(linea if linea else " ", mono=True, color=V900, size=20)
            junto = len(lineas) <= 28 and i < len(lineas) - 1
            self.add(f"<w:p>{ppr(estilo='Codigo', keep_next=junto)}{contenido}</w:p>")
        self.add(parrafo(" ", despues=60, linea=(120, "exact")))

    def espacio(self, twips=120):
        self.add(parrafo(" ", despues=0, antes=0, linea=(twips, "exact")))

    def salto_de_pagina(self):
        self.add('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')

    # --- tablas
    def tabla(self, encabezados, filas, anchos, mono=(), centro=(), tam=20, tam_codigo=18, cebra=True,
              ancho_total=None, junta=False):
        """`filas`: listas de celdas (texto con marcas; '\\n' separa párrafos).
        Una fila puede ser ('grupo', 'Título') para una fila que abarca todas las columnas."""
        ncols = len(anchos)
        total = sum(anchos)
        celdas_enc = []
        for i, enc in enumerate(encabezados):
            par = parrafo(
                run(enc, bold=True, color=BLANCO, size=tam),
                alinear="center" if i in centro else None, antes=0, despues=0, linea=(240, "auto"),
                keep_next=True,
            )
            celdas_enc.append(celda(anchos[i], par, fill=V600, bordes=bordes_tc(color=V600), valign="center"))
        filas_xml = [fila(celdas_enc, header=True)]
        n = 0
        for idx, f in enumerate(filas):
            junto = junta and idx < len(filas) - 1
            if isinstance(f, tuple) and f[0] == "grupo":
                par = parrafo(run(f[1], bold=True, color=V900, size=tam), antes=0, despues=0, linea=(240, "auto"),
                              keep_next=True)
                filas_xml.append(fila([celda(total, par, fill=V50, span=ncols)]))
                n = 0
                continue
            fill = V50 if (cebra and n % 2 == 1) else None
            n += 1
            celdas = []
            for i, texto in enumerate(f):
                pars = []
                for parte in str(texto).split("\n"):
                    if i in mono and "`" not in parte and parte:
                        runs = run(parte, mono=True, color=V900, size=tam_codigo)
                    else:
                        runs = rich(parte, size=tam, code_size=tam_codigo)
                    pars.append(parrafo(runs, alinear="center" if i in centro else None, antes=0, despues=0,
                                        linea=(247, "auto"), keep_next=junto))
                celdas.append(celda(anchos[i], "".join(pars), fill=fill, valign="top"))
            filas_xml.append(fila(celdas))
        self.add(tabla(filas_xml, anchos))
        self.espacio(160)

    # --- recuadros
    def _recuadro(self, titulo, texto, fondo, color_texto, color_borde, ancho):
        parrafos = []
        if titulo:
            parrafos.append(parrafo(run(titulo, bold=True, color=color_texto, size=21), antes=0, despues=40,
                                    keep_next=True))
        if isinstance(texto, str):
            texto = [texto]
        for t in texto:
            parrafos.append(parrafo(rich(t, color=color_texto, size=21, code_color=color_texto), antes=0,
                                    despues=60, linea=(252, "auto")))
        bordes = (
            "<w:tcBorders>"
            + borde_xml("top", sz=4, color=color_borde)
            + borde_xml("left", sz=36, color=color_borde)
            + borde_xml("bottom", sz=4, color=color_borde)
            + borde_xml("right", sz=4, color=color_borde)
            + "</w:tcBorders>"
        )
        c = celda(ancho, "".join(parrafos), fill=fondo, bordes=bordes,
                  margenes='<w:tcMar><w:top w:w="110" w:type="dxa"/><w:left w:w="200" w:type="dxa"/>'
                           '<w:bottom w:w="70" w:type="dxa"/><w:right w:w="160" w:type="dxa"/></w:tcMar>')
        self.add(tabla([fila([c])], [ancho], bordes_tabla=False))
        self.espacio(160)

    def implementacion(self, texto, ancho=ANCHO_VERTICAL):
        """Recuadro ámbar «En implementación»: lo previsto que todavía no existe."""
        self._recuadro("En implementación", texto, AMBAR_BG, AMBAR_TX, AMBAR_BORDE, ancho)

    def nota(self, texto, titulo=None, ancho=ANCHO_VERTICAL):
        self._recuadro(titulo, texto, V50, V900, V600, ancho)

    # --- índice y secciones
    def indice(self):
        self.add(parrafo("Contenido", estilo="TituloContenido"))
        self.add(
            "<w:p>"
            '<w:r><w:fldChar w:fldCharType="begin"/></w:r>'
            '<w:r><w:instrText xml:space="preserve"> TOC \\o "1-2" \\h \\z \\u </w:instrText></w:r>'
            '<w:r><w:fldChar w:fldCharType="separate"/></w:r>'
            + run("El índice se genera al abrir el documento en Word.", italic=True, color=G500)
            + '<w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>'
        )

    def _sect(self, horizontal, portada):
        if horizontal:
            refs = ('<w:headerReference w:type="default" r:id="rIdHdrH"/>'
                    '<w:footerReference w:type="default" r:id="rIdFtrH"/>')
            tam_pag = '<w:pgSz w:w="15840" w:h="12240" w:orient="landscape"/>'
            margenes = ('<w:pgMar w:top="1300" w:right="1080" w:bottom="1134" w:left="1080" '
                        'w:header="567" w:footer="567" w:gutter="0"/>')
        else:
            refs = ('<w:headerReference w:type="default" r:id="rIdHdrV"/>'
                    '<w:footerReference w:type="default" r:id="rIdFtrV"/>')
            if portada:
                refs += ('<w:headerReference w:type="first" r:id="rIdHdrV1"/>'
                         '<w:footerReference w:type="first" r:id="rIdFtrV1"/>')
            tam_pag = '<w:pgSz w:w="12240" w:h="15840"/>'
            margenes = ('<w:pgMar w:top="1440" w:right="1440" w:bottom="1296" w:left="1440" '
                        'w:header="567" w:footer="567" w:gutter="0"/>')
        # El orden de los hijos de sectPr importa: referencias, tipo, tamaño, márgenes, titlePg.
        return (f'<w:sectPr>{refs}<w:type w:val="nextPage"/>{tam_pag}{margenes}'
                + ("<w:titlePg/>" if portada else "") + "</w:sectPr>")

    def cerrar_seccion(self, horizontal=False, portada=False):
        """Cierra la sección en curso: la última sección va al final del cuerpo."""
        self.add(f"<w:p><w:pPr>{self._sect(horizontal, portada)}</w:pPr></w:p>")

    # --- encabezado y pie
    def _encabezado(self, ancho, con_contenido=True):
        if not con_contenido:
            return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:hdr {NS}>'
                    f'{parrafo(" ", estilo="Header")}</w:hdr>')
        logo = imagen("rIdLogo", 360000, 360000, "Logo AdMind", 900, "Logo de AdMind")
        borde = f'<w:bottom w:val="single" w:sz="6" w:space="4" w:color="{V600}"/>'
        tabs = None if ancho == ANCHO_VERTICAL else (
            f'<w:tab w:val="clear" w:pos="{ANCHO_VERTICAL}"/><w:tab w:val="right" w:pos="{ancho}"/>')
        p = (f"<w:p>{ppr(estilo='Header', borde=borde, tabs=tabs)}{logo}"
             f'<w:r><w:tab/></w:r>{run(self.nombre_encabezado, color=G500, size=19)}</w:p>')
        return f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:hdr {NS}>{p}</w:hdr>'

    def _pie(self, ancho, con_contenido=True):
        if not con_contenido:
            return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:ftr {NS}>'
                    f'{parrafo(" ", estilo="Footer")}</w:ftr>')
        borde = f'<w:top w:val="single" w:sz="4" w:space="6" w:color="{G200}"/>'
        tabs = None if ancho == ANCHO_VERTICAL else (
            f'<w:tab w:val="clear" w:pos="{ANCHO_VERTICAL}"/><w:tab w:val="right" w:pos="{ancho}"/>')
        contenido = (
            run("AdMind · Ingeniería de Software II · 2026", color=G500, size=18)
            + '<w:r><w:tab/></w:r>'
            + run("Página ", color=G500, size=18)
            + campo("PAGE", "1", color=G500, size=18)
            + run(" de ", color=G500, size=18)
            + campo("NUMPAGES", "1", color=G500, size=18)
        )
        p = f"<w:p>{ppr(estilo='Footer', borde=borde, tabs=tabs)}{contenido}</w:p>"
        return f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:ftr {NS}>{p}</w:ftr>'

    # --- empaquetado
    def guardar(self, ruta, ultima_horizontal=False, ultima_portada=False):
        ultimo = self._sect(ultima_horizontal, ultima_portada)
        documento = (
            f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document {NS}><w:body>'
            + "".join(self.cuerpo) + ultimo + "</w:body></w:document>"
        )
        rel_tipo = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
        rels_doc = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            f'<Relationship Id="rIdSty" Type="{rel_tipo}/styles" Target="styles.xml"/>'
            f'<Relationship Id="rIdNum" Type="{rel_tipo}/numbering" Target="numbering.xml"/>'
            f'<Relationship Id="rIdSet" Type="{rel_tipo}/settings" Target="settings.xml"/>'
            f'<Relationship Id="rIdLogo" Type="{rel_tipo}/image" Target="media/logo.png"/>'
            f'<Relationship Id="rIdHdrV" Type="{rel_tipo}/header" Target="header1.xml"/>'
            f'<Relationship Id="rIdHdrV1" Type="{rel_tipo}/header" Target="header2.xml"/>'
            f'<Relationship Id="rIdHdrH" Type="{rel_tipo}/header" Target="header3.xml"/>'
            f'<Relationship Id="rIdFtrV" Type="{rel_tipo}/footer" Target="footer1.xml"/>'
            f'<Relationship Id="rIdFtrV1" Type="{rel_tipo}/footer" Target="footer2.xml"/>'
            f'<Relationship Id="rIdFtrH" Type="{rel_tipo}/footer" Target="footer3.xml"/>'
            "</Relationships>"
        )
        rels_hdr = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            f'<Relationship Id="rIdLogo" Type="{rel_tipo}/image" Target="media/logo.png"/></Relationships>'
        )
        tipos = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Default Extension="png" ContentType="image/png"/>'
            '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
            '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
            '<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>'
            '<Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>'
            + "".join(
                f'<Override PartName="/word/header{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/>'
                f'<Override PartName="/word/footer{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>'
                for i in (1, 2, 3)
            )
            + '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
            '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>'
            "</Types>"
        )
        raiz = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
            '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>'
            "</Relationships>"
        )
        ajustes = (
            f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:settings {NS}>'
            '<w:zoom w:percent="100"/><w:defaultTabStop w:val="720"/><w:characterSpacingControl w:val="doNotCompress"/>'
            '<w:compat><w:compatSetting w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" w:val="15"/>'
            "</w:compat>"
            '<w:themeFontLang w:val="es-CO"/></w:settings>'
        )
        core = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            f"<dc:title>{esc(self.titulo)}</dc:title><dc:creator>{esc(self.autor)}</dc:creator>"
            '<dcterms:created xsi:type="dcterms:W3CDTF">2026-11-14T08:00:00Z</dcterms:created>'
            "</cp:coreProperties>"
        )
        app = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">'
            "<Application>Microsoft Office Word</Application></Properties>"
        )
        with zipfile.ZipFile(ruta, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("[Content_Types].xml", tipos)
            z.writestr("_rels/.rels", raiz)
            z.writestr("word/document.xml", documento)
            z.writestr("word/_rels/document.xml.rels", rels_doc)
            z.writestr("word/styles.xml", estilos_xml())
            z.writestr("word/numbering.xml", numeracion_xml(self._num_ids))
            z.writestr("word/settings.xml", ajustes)
            z.writestr("word/header1.xml", self._encabezado(ANCHO_VERTICAL))
            z.writestr("word/header2.xml", self._encabezado(ANCHO_VERTICAL, con_contenido=False))
            z.writestr("word/header3.xml", self._encabezado(ANCHO_HORIZONTAL))
            z.writestr("word/footer1.xml", self._pie(ANCHO_VERTICAL))
            z.writestr("word/footer2.xml", self._pie(ANCHO_VERTICAL, con_contenido=False))
            z.writestr("word/footer3.xml", self._pie(ANCHO_HORIZONTAL))
            for i in (1, 3):
                z.writestr(f"word/_rels/header{i}.xml.rels", rels_hdr)
            z.writestr("word/media/logo.png", self.logo)
            z.writestr("docProps/core.xml", core)
            z.writestr("docProps/app.xml", app)
