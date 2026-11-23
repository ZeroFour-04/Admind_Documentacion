# -*- coding: utf-8 -*-
"""Diccionario de datos de AdMind en Excel, minimalista y en blanco y negro.

Usa los mismos datos que el Word (diccionario_datos.md, sacado de admind_db) y las descripciones
de desc_negocio.py. Uso: python -I build_xlsx.py <salida.xlsx>
"""
import os
import re
import sys

SALIDA = sys.argv[1]
sys.argv = ["x", "sin_uso"]  # build_diccionario lee sys.argv al importarse
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import build_diccionario as b  # noqa: E402
from desc_negocio import DESC, GEN  # noqa: E402
from openpyxl import Workbook  # noqa: E402
from openpyxl.styles import Alignment, Border, Font, Side  # noqa: E402
from openpyxl.worksheet.properties import PageSetupProperties  # noqa: E402

# ---------------------------------------------------------------- datos
doc = b.parse(b.MD)
for m in doc["modules"]:
    for t in m["tables"]:
        for c in t["cols"]:
            nuevo = DESC.get(t["name"], {}).get(c["name"]) or GEN.get(c["name"])
            if nuevo:
                suf = re.search(r"\s*Valores:.*$", c["desc"])
                c["desc"] = nuevo + (" " + suf.group(0).strip() if suf else "")
for m in doc["modules"] + [doc["anexo"]]:
    for t in m["tables"]:
        for c in t["cols"]:
            c["desc"] = b.limpiar_desc(c["desc"])


def sin_refs_internas(texto):
    """Quita 'maestro §..', 'plan Xn' y 'legal §..' de los parentesis; deja las HU-NN."""
    def paren(m):
        partes = [p for p in re.split(r"\s*[,;]\s*", m.group(1).strip()) if p]
        buenas = [p for p in partes if not re.match(r"^(maestro|plan|legal)\b|^§", p)]
        if len(buenas) == len(partes):
            return m.group(0)  # nada que quitar: el parentesis queda igual
        return "(" + ", ".join(buenas) + ")" if buenas else ""
    texto = re.sub(r"\(([^()]*)\)", paren, texto)
    texto = re.sub(r"\s+([.,;:])", r"\1", texto)
    return re.sub(r"\s{2,}", " ", texto).strip()


FRAMEWORK = "Framework (Django y django-otp)"
hoja_tablas, hoja_cols, hoja_restr = [], [], []
cambios_desc = []
for mod in doc["modules"] + [doc["anexo"]]:
    nombre_mod = FRAMEWORK if mod is doc["anexo"] else mod["name"]
    for t in mod["tables"]:
        d0 = b.limpiar_desc(" ".join(t["desc"])).strip()
        d1 = sin_refs_internas(d0).replace("`", "")  # en Excel las comillas invertidas sobran
        if d1 != d0:
            cambios_desc.append((t["name"], d0, d1))
        hoja_tablas.append([nombre_mod, t["name"], t["model"] or "", len(t["cols"]), d1])
        for c in t["cols"]:
            tokens = [x.strip() for x in c["key"].split("·")] if c["key"] else []
            llave, ref = [], ""
            for tk in tokens:
                if tk.startswith("FK"):
                    llave.append("FK")
                    ref = tk.split("`")[1] if "`" in tk else ""
                else:
                    llave.append(tk)
            desc, valores = c["desc"], ""
            m = re.search(r"\s*Valores:\s*(.*)$", desc)
            if m:
                desc = desc[:m.start()].strip()
                valores = ", ".join(re.findall(r"`([^`]*)`", m.group(1)))
            hoja_cols.append([t["name"], c["name"], c["type"], c["null"], " · ".join(llave),
                              ref, desc.replace("`", ""), valores])
        for r in t["restr"]:
            mm = b.RE_R.match(r)
            assert mm, r
            kind, name, rest = mm.groups()
            if rest.startswith("`") and rest.endswith("`"):
                rest = rest[1:-1]
            hoja_restr.append([t["name"], kind, name, rest])

facts = " ".join(doc["facts"])
n_tablas = len(hoja_tablas)
n_neg = sum(len(m["tables"]) for m in doc["modules"])
n_cols = len(hoja_cols)
assert (n_tablas, n_cols) == (42, 352), (n_tablas, n_cols)
pk, fk, uq, ck = (int(x) for x in re.search(
    r"(\d+) llaves primarias, (\d+) llaves foráneas, (\d+) únicas y (\d+) CHECK", facts).groups())
commit = re.search(r"`main` `(\w+)`", facts).group(1)
pgver = re.search(r"PostgreSQL ([\d.]+)", facts).group(1)

# ---------------------------------------------------------------- formato
NEGRO = "FF000000"
lado = Side(style="thin", color=NEGRO)
borde = Border(left=lado, right=lado, top=lado, bottom=lado)
f_normal = Font(name="Calibri", size=11, color=NEGRO)
f_negrita = Font(name="Calibri", size=11, bold=True, color=NEGRO)
f_titulo = Font(name="Calibri", size=14, bold=True, color=NEGRO)
al_enc = Alignment(vertical="center", wrap_text=True)
al_cuerpo = Alignment(vertical="top", wrap_text=True)
al_centro = Alignment(vertical="top", horizontal="center", wrap_text=True)

wb = Workbook()


def hoja_info(ws):
    ws.title = "Info"
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 26
    ws.column_dimensions["B"].width = 92
    ws["A1"] = "Diccionario de Datos — AdMind"
    ws["A1"].font = f_titulo
    filas = [
        ("Base de datos", f"admind_db (PostgreSQL {pgver})"),
        ("Corte", f"14 de noviembre de 2026 (backend en main, commit {commit})"),
        ("Tablas", f"{n_tablas}: {n_neg} del negocio y {n_tablas - n_neg} del framework"),
        ("Columnas", n_cols),
        ("Restricciones", f"{pk} llaves primarias, {fk} foráneas, {uq} únicas y {ck} CHECK. "
                          f"La hoja Restricciones lista las de las {n_neg} tablas del negocio."),
        ("Triggers y procedimientos", 0),
        None,
        ("Nulo", "No = la columna es obligatoria (NOT NULL)."),
        ("Llave", "PK llave primaria · FK llave foránea (a qué columna apunta, en Referencia a) · UQ valor único."),
        ("Llave foránea compuesta", "Las tablas de cada conjunto tienen una única (id, conjunto_id) y sus hijas apuntan a esa "
                                        "pareja: la base impide ligar filas de dos conjuntos."),
        None,
    ]
    filas += [("Integrantes" if i == 0 else "", n) for i, n in enumerate(b.INTEGRANTES)]
    filas += [("Asignatura", "Ingeniería de Software II"), ("Docente", "Oscar Gómez"),
              ("Universidad", "Universidad de Cundinamarca")]
    r = 3
    for fila in filas:
        if fila:
            ws.cell(r, 1, fila[0]).font = f_negrita
            ws.cell(r, 1).alignment = al_cuerpo
            ws.cell(r, 2, fila[1]).font = f_normal
            ws.cell(r, 2).alignment = Alignment(vertical="top", horizontal="left", wrap_text=True)
        r += 1


def hoja_datos(nombre, encabezado, filas, anchos, centradas=()):
    ws = wb.create_sheet(nombre)
    ws.sheet_view.showGridLines = False
    for i, (h, w) in enumerate(zip(encabezado, anchos), 1):
        c = ws.cell(1, i, h)
        c.font, c.border, c.alignment = f_negrita, borde, al_enc
        ws.column_dimensions[c.column_letter].width = w
    for r, fila in enumerate(filas, 2):
        for i, v in enumerate(fila, 1):
            c = ws.cell(r, i, v)
            c.font, c.border = f_normal, borde
            c.alignment = al_centro if i in centradas else al_cuerpo
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:{ws.cell(1, len(encabezado)).column_letter}{len(filas) + 1}"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr = PageSetupProperties(fitToPage=True)
    ws.print_title_rows = "1:1"
    return ws


hoja_info(wb.active)
hoja_datos("Tablas", ["Módulo", "Tabla", "Modelo de Django", "Columnas", "Descripción"],
           hoja_tablas, [30, 36, 34, 10, 80], centradas=(4,))
hoja_datos("Columnas", ["Tabla", "Columna", "Tipo", "Nulo", "Llave", "Referencia a", "Descripción",
                        "Valores permitidos"],
           hoja_cols, [36, 30, 26, 7, 12, 36, 70, 46], centradas=(4,))
hoja_datos("Restricciones", ["Tabla", "Tipo", "Nombre", "Definición"],
           hoja_restr, [36, 24, 56, 110])

wb.properties.title = "AdMind — Diccionario de Datos"
wb.properties.creator = "AdMind"
os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
wb.save(SALIDA)
print("ok:", SALIDA, "| tablas", n_tablas, "columnas", n_cols, "restricciones", len(hoja_restr))
print("descripciones de tabla sin referencias internas:", len(cambios_desc))
for t, a, c in cambios_desc:
    print(" -", t, "\n     antes:", a, "\n     ahora:", c)
