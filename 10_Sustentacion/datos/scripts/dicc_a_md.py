"""Convierte diccionario.json (esquema real de admind_db) en el diccionario de datos en Markdown."""
import json
import re
import sys

entrada, salida = sys.argv[1], sys.argv[2]
d = json.load(open(entrada, encoding="utf-8"))

MODULOS = [
    ("personas", "Personas", "Identidad global de cada persona, independiente de los conjuntos."),
    ("cuentas", "Cuentas y sesión", "Usuarios que inician sesión y sus tokens de sesión en la API."),
    ("conjuntos", "Conjuntos", "Cada conjunto residencial que administra la plataforma."),
    ("permisos", "Roles y permisos", "El rol vigente de una persona en un conjunto."),
    ("unidades", "Viviendas", "Agrupaciones (torres, bloques), viviendas y vínculos de las personas con ellas."),
    ("areas", "Zonas comunes", "Áreas comunes del conjunto, con reserva o con ingreso."),
    ("reglas", "Motor de reglas", "Reglas del conjunto (alfa) y de cada zona (beta)."),
    ("reservas", "Reservas", "Solicitudes de reserva, avisos de franja libre y comprobantes de pago de reservas."),
    ("ingresos", "Ingresos a zonas", "Registro de entrada y salida de personas en zonas con aforo."),
    ("parqueaderos", "Parqueaderos", "Puestos de parqueo y su asignación a viviendas."),
    ("visitantes", "Visitantes", "Visitas registradas en portería."),
    ("pagos", "Pagos de administración", "Pago mensual de la administración por vivienda y sus comprobantes."),
    ("documentos", "Documentos", "Reglamento y manual de convivencia del conjunto."),
    ("anuncios", "Anuncios", "Anuncios del conjunto y sus fotos."),
    ("notificaciones", "Notificaciones", "Bandeja de avisos de cada persona."),
    ("casos", "Casos (PQRS)", "Casos reportados por los residentes y sus fotos."),
    ("infracciones", "Infracciones", "Registro y comunicación de infracciones a una vivienda."),
    ("citas", "Citas", "Horario de atención de la administración y citas agendadas."),
    ("auditoria", "Auditoría", "Registro inmutable de quién hizo qué y cuándo."),
]
DEL_FRAMEWORK = {"auth", "admin", "contenttypes", "sessions", "django", "otp_static", "otp_totp"}

tablas_por_app = {}
for t in d["tablas"]:
    tablas_por_app.setdefault(t["app"], []).append(t)

FK = re.compile(r"FOREIGN KEY \(([^)]+)\) REFERENCES (\w+)\(([^)]+)\)(.*)")
COLS = re.compile(r"\(([^)]+)\)")


def limpiar(defn):
    defn = re.sub(r"::(text|character varying|bpchar|integer|bigint|numeric)(\[\])?", "", defn)
    defn = defn.replace(" DEFERRABLE INITIALLY DEFERRED", "")
    return defn


def llaves(tabla):
    pk, fk, uq = set(), {}, set()
    compuestas, checks, unicas = [], [], []
    for r in tabla["restricciones"]:
        if r["tipo"] == "p":
            pk |= {c.strip() for c in COLS.search(r["definicion"]).group(1).split(",")}
        elif r["tipo"] == "f":
            m = FK.match(r["definicion"])
            cols = [c.strip() for c in m.group(1).split(",")]
            if len(cols) == 1:
                fk[cols[0]] = f"{m.group(2)}.{m.group(3)}"
            else:
                compuestas.append((r["nombre"], f"({m.group(1)}) → {m.group(2)}({m.group(3)})"
                                   + (" ON DELETE RESTRICT" if "RESTRICT" in m.group(4) else "")))
        elif r["tipo"] == "u":
            cols = [c.strip() for c in COLS.search(r["definicion"]).group(1).split(",")]
            if len(cols) == 1:
                uq.add(cols[0])
            else:
                unicas.append((r["nombre"], "UNIQUE (" + ", ".join(cols) + ")"))
        elif r["tipo"] == "c":
            checks.append((r["nombre"], limpiar(r["definicion"])))
    parciales = []
    nombres_restr = {r["nombre"] for r in tabla["restricciones"]}
    for i in tabla["indices"]:
        if i["nombre"] in nombres_restr:
            continue
        if "UNIQUE" in i["definicion"]:
            cols = COLS.search(i["definicion"].split("USING btree", 1)[-1]).group(1)
            donde = ""
            if " WHERE " in i["definicion"]:
                donde = " cuando " + limpiar(i["definicion"].split(" WHERE ", 1)[1])
            parciales.append((i["nombre"], f"único ({cols}){donde}"))
    return pk, fk, uq, compuestas, checks, unicas, parciales


def celda(texto):
    return str(texto).replace("|", "\\|").replace("\n", " ")


def tabla_md(t, breve=False):
    pk, fk, uq, compuestas, checks, unicas, parciales = llaves(t)
    out = [f"### `{t['tabla']}`", ""]
    if t["descripcion"]:
        out += [celda(t["descripcion"]), ""]
    if t["modelo"]:
        out += [f"Modelo de Django: `{t['app']}.{t['modelo']}`.", ""]
    out += ["| Columna | Tipo | Nulo | Llave | Descripción y valores permitidos |",
            "|---|---|---|---|---|"]
    for c in t["columnas"]:
        k = []
        if c["columna"] in pk:
            k.append("PK")
        if c["columna"] in fk:
            k.append(f"FK → `{fk[c['columna']]}`")
        if c["columna"] in uq:
            k.append("UQ")
        desc = c["descripcion"][:1].upper() + c["descripcion"][1:] if c["descripcion"] else ""
        if c["opciones"]:
            desc += (". " if desc else "") + "Valores: " + ", ".join(f"`{o}`" for o in c["opciones"] if o != "")
        out.append(f"| `{c['columna']}` | {c['tipo_legible']} | {'Sí' if c['nulo'] else 'No'} | "
                   f"{' · '.join(k)} | {celda(desc)} |")
    out.append("")
    if not breve and (compuestas or checks or unicas or parciales):
        out += ["**Restricciones de la tabla**", ""]
        for nombre, defn in compuestas:
            out.append(f"- Llave foránea compuesta `{nombre}`: {celda(defn)}")
        for nombre, defn in unicas:
            out.append(f"- Única `{nombre}`: {celda(defn)}")
        for nombre, defn in parciales:
            out.append(f"- Índice `{nombre}`: {celda(defn)}")
        for nombre, defn in checks:
            out.append(f"- CHECK `{nombre}`: `{celda(defn)}`")
        out.append("")
    return out


n_neg = sum(len(tablas_por_app.get(a, [])) for a, _, _ in MODULOS)
n_fw = sum(len(v) for k, v in tablas_por_app.items() if k in DEL_FRAMEWORK)
tipos = {}
for t in d["tablas"]:
    for r in t["restricciones"]:
        tipos[r["tipo"]] = tipos.get(r["tipo"], 0) + 1

md = [
    "---",
    'resumen: "Diccionario de datos de admind_db generado del esquema real de PostgreSQL y de los modelos de Django."',
    "tipo: estado",
    'origen: "information_schema y pg_catalog de admind_db, cruzados con los modelos del backend (main b89d9f2), 2026-11-14"',
    "actualizado: 2026-11-14",
    "revisado: 2026-11-14",
    "---",
    "",
    "# Diccionario de datos de AdMind",
    "",
    f"- **Base de datos:** `{d['base']}`, {d['version'].split(',')[0]}.",
    "- **Corte:** 2026-11-14, backend en `main` `b89d9f2`, sin migraciones pendientes.",
    f"- **Tablas:** {len(d['tablas'])} en total: {n_neg} del negocio y {n_fw} del framework (Django y django-otp).",
    f"- **Restricciones:** {tipos.get('p', 0)} llaves primarias, {tipos.get('f', 0)} llaves foráneas, "
    f"{tipos.get('u', 0)} únicas y {tipos.get('c', 0)} CHECK.",
    f"- **Triggers:** {len(d['disparadores'])}. **Procedimientos y funciones:** {len(d['procedimientos'])}.",
    "",
    "## Convenciones",
    "",
    "- **Nombre de tabla:** `<app>_<modelo>`, como lo crea Django.",
    "- **Llave:** `PK` llave primaria, `FK → tabla.columna` llave foránea, `UQ` valor único.",
    "- **Nulo:** `No` significa que la columna es obligatoria (`NOT NULL`).",
    "- **Aislamiento entre conjuntos:** las tablas de cada conjunto llevan `conjunto_id` y una única `(id, conjunto_id)`. "
    "Sus hijas apuntan a esa pareja con una **llave foránea compuesta**, así la base impide que una fila de un conjunto "
    "quede ligada a una de otro.",
    "- **Sin borrado físico:** las filas no se borran; se cierran con una vigencia, un estado o una anulación.",
    "- **Archivos:** fotos, logos y comprobantes se guardan dentro de la base, en columnas `bytea`.",
    "",
]
for app, titulo, desc in MODULOS:
    ts = tablas_por_app.get(app, [])
    if not ts:
        continue
    md += [f"## {titulo}", "", desc, ""]
    for t in ts:
        md += tabla_md(t)
md += ["## Anexo: tablas del framework", "",
       "Las crean Django (usuarios, permisos internos, sesiones, migraciones) y django-otp (segundo factor). "
       "AdMind no las modifica.", ""]
for app in sorted(DEL_FRAMEWORK):
    for t in tablas_por_app.get(app, []):
        md += tabla_md(t, breve=True)
faltan = [a for a in tablas_por_app if a not in DEL_FRAMEWORK and a not in {m[0] for m in MODULOS}]
if faltan:
    print("APPS SIN SECCION:", faltan)
open(salida, "w", encoding="utf-8").write("\n".join(md) + "\n")
print("ok", len(md), "lineas")
