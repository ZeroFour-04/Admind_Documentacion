# Se ejecuta dentro de `manage.py shell -c "exec(open(...).read())"` del backend.
# Lista las rutas de la API con sus métodos HTTP, la vista y su primera línea de documentación.
import inspect
import os

from django.urls import URLPattern, URLResolver, get_resolver

SALIDA = os.environ["ENDPOINTS_SALIDA"]
METODOS = ["get", "post", "put", "patch", "delete"]
filas = []


def recorrer(patrones, prefijo=""):
    for p in patrones:
        if isinstance(p, URLResolver):
            recorrer(p.url_patterns, prefijo + str(p.pattern))
        elif isinstance(p, URLPattern):
            ruta = "/" + prefijo + str(p.pattern)
            vista = getattr(p.callback, "view_class", None) or getattr(p.callback, "cls", None)
            if vista is None or ruta.startswith("/admin"):
                continue
            metodos = [m.upper() for m in METODOS if hasattr(vista, m)]
            # Solo la documentación propia de la vista: la heredada de VistaDeConjunto o APIView no dice nada.
            doc = inspect.cleandoc(vista.__dict__.get("__doc__") or "").split("\n")[0]
            app = vista.__module__.split(".")[1] if vista.__module__.startswith("apps.") else vista.__module__
            filas.append((app, ruta.replace("^", "").replace("$", ""), ", ".join(metodos), vista.__name__, doc))


recorrer(get_resolver().url_patterns)
filas.sort()
lineas = ["# Endpoints de la API de AdMind", "",
          f"Generado de las rutas reales del backend (`main` `b89d9f2`), 2026-11-14. Total: **{len(filas)} rutas**.", "",
          "Toda ruta exige `Authorization: Token <token>` salvo las de ingreso y recuperación de contraseña.", ""]
app_actual = None
for app, ruta, metodos, vista, doc in filas:
    if app != app_actual:
        lineas += ["", f"## {app}", "", "| Ruta | Métodos | Vista | Qué hace |", "|---|---|---|---|"]
        app_actual = app
    lineas.append(f"| `{ruta}` | {metodos} | `{vista}` | {doc.replace('|', '/')} |")
open(SALIDA, "w", encoding="utf-8").write("\n".join(lineas) + "\n")
print("rutas:", len(filas))
