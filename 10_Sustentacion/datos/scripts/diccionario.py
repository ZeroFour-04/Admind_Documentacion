# Se ejecuta dentro de `manage.py shell -c "exec(open(...).read())"` del backend.
# Lee el esquema real de admind_db y lo cruza con los modelos de Django (descripciones y opciones).
import inspect
import json
import os
from collections import defaultdict

from django.apps import apps
from django.db import connection

SALIDA = os.environ["DICC_SALIDA"]

modelo_de_tabla = {}
for m in apps.get_models(include_auto_created=True):
    modelo_de_tabla[m._meta.db_table] = m

with connection.cursor() as c:
    c.execute("select current_database(), version()")
    base, version = c.fetchone()
    c.execute("""select table_name from information_schema.tables
                 where table_schema='public' and table_type='BASE TABLE' order by table_name""")
    tablas = [r[0] for r in c.fetchall()]
    c.execute("""select table_name, column_name, data_type, udt_name, character_maximum_length,
                        numeric_precision, numeric_scale, is_nullable, column_default
                 from information_schema.columns where table_schema='public'
                 order by table_name, ordinal_position""")
    columnas = c.fetchall()
    c.execute("""select rel.relname, con.conname, con.contype, pg_get_constraintdef(con.oid)
                 from pg_constraint con join pg_class rel on rel.oid=con.conrelid
                 join pg_namespace n on n.oid=rel.relnamespace
                 where n.nspname='public' order by rel.relname, con.contype, con.conname""")
    restricciones = c.fetchall()
    c.execute("""select tablename, indexname, indexdef from pg_indexes
                 where schemaname='public' order by tablename, indexname""")
    indices = c.fetchall()
    c.execute("""select event_object_table, trigger_name, action_timing, event_manipulation
                 from information_schema.triggers where trigger_schema='public'""")
    disparadores = c.fetchall()
    c.execute("""select p.proname, p.prokind from pg_proc p join pg_namespace n on n.oid=p.pronamespace
                 where n.nspname='public'""")
    procedimientos = c.fetchall()

cols_por_tabla = defaultdict(list)
for t, col, dt, udt, largo, prec, esc, nulo, defecto in columnas:
    cols_por_tabla[t].append(dict(columna=col, tipo=dt, udt=udt, largo=largo, precision=prec,
                                  escala=esc, nulo=nulo == "YES", defecto=defecto))

res_por_tabla = defaultdict(list)
for t, nombre, tipo, definicion in restricciones:
    res_por_tabla[t].append(dict(nombre=nombre, tipo=tipo, definicion=definicion))

idx_por_tabla = defaultdict(list)
for t, nombre, definicion in indices:
    idx_por_tabla[t].append(dict(nombre=nombre, definicion=definicion))


def tipo_legible(c):
    udt = c["udt"]
    if udt == "varchar":
        return f"varchar({c['largo']})" if c["largo"] else "varchar"
    if udt == "bpchar":
        return f"char({c['largo']})"
    if udt == "numeric" and c["precision"]:
        return f"numeric({c['precision']},{c['escala']})"
    return {"int8": "bigint", "int4": "integer", "int2": "smallint", "bool": "boolean",
            "timestamptz": "timestamp with time zone", "bytea": "bytea (archivo binario)",
            "float8": "double precision"}.get(udt, udt)


resultado = dict(base=base, version=version, tablas=[], disparadores=disparadores,
                 procedimientos=procedimientos)

for t in tablas:
    modelo = modelo_de_tabla.get(t)
    campos = {}
    descripcion = ""
    app = t.split("_")[0]
    if modelo is not None:
        app = modelo._meta.app_label
        doc = inspect.getdoc(modelo) or ""
        if doc and not doc.startswith(modelo.__name__ + "("):
            descripcion = doc.split("\n\n")[0].replace("\n", " ")
        if not descripcion and modelo._meta.auto_created:
            descripcion = f"Tabla intermedia creada por Django: {modelo._meta.verbose_name}."
        for f in modelo._meta.concrete_fields:
            campos[f.column] = f
    filas = []
    for c in cols_por_tabla[t]:
        f = campos.get(c["columna"])
        desc, opciones, rel, largo_modelo = "", [], None, None
        if f is not None:
            desc = str(f.help_text or "") or str(f.verbose_name)
            if f.choices:
                opciones = [str(k) for k, _ in f.flatchoices]
            if f.is_relation and f.related_model is not None:
                rel = f.related_model._meta.db_table
        filas.append(dict(c, tipo_legible=tipo_legible(c), descripcion=desc, opciones=opciones,
                          referencia=rel))
    resultado["tablas"].append(dict(tabla=t, app=app, modelo=modelo.__name__ if modelo else None,
                                    descripcion=descripcion, columnas=filas,
                                    restricciones=res_por_tabla[t], indices=idx_por_tabla[t]))

with open(SALIDA, "w", encoding="utf-8") as fh:
    json.dump(resultado, fh, ensure_ascii=False, indent=1, default=str)
print("tablas:", len(tablas), "columnas:", len(columnas), "restricciones:", len(restricciones),
      "indices:", len(indices), "triggers:", len(disparadores), "funciones:", len(procedimientos))
