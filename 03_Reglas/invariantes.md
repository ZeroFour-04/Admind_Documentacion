---
resumen: "Lo que toda pieza nueva de código respeta, y cómo se hace en este código (herencias, funciones y pruebas concretas)."
tipo: regla
origen: "plan de los Sprints 2 y 3 §0.3 (2026-09-27)"
actualizado: 2026-09-27
---

# Invariantes que toda pieza nueva respeta

Se lee antes de crear una tabla, un endpoint o una pantalla. El porqué de cada uno está en [aislamiento](aislamiento.md) y [eliminacion](eliminacion.md).

| Invariante | Cómo, en este código |
|---|---|
| Toda tabla nueva tiene `conjunto_id` NOT NULL | Hereda `ModeloDeConjunto` (`apps/comun/modelos_base/modelos.py`). Si declara `class Meta`, hereda `ModeloDeConjunto.Meta` y repite `*ModeloDeConjunto.Meta.constraints` |
| FK entre tablas de conjunto = FK compuesta | En la migración, después del `CreateModel`: `fk_compuesta("<tabla>", "<columna>_id", "<tabla_referida>")` de `apps/comun/aislamiento/migraciones.py`. Nombre de la restricción ≤ 63 caracteres |
| Ninguna vista acepta el conjunto | Toda vista con datos de un conjunto hereda `VistaDeConjunto`. El conjunto activo sale de `request.auth.conjunto_activo_id` |
| Todo permiso se exige | `exigir_permiso(request, "permiso.x", ...)` de `apps/permisos/views.py` (403). Todo permiso que uses **ya existe** en el catálogo |
| Otro conjunto = 404, nunca 403 | Busca a través del manager (ya filtra por conjunto) y responde `NotFound()` sin detalle |
| Sin borrado físico | Sin `DELETE` en la API, FK con `PROTECT`, bajas por `activo=False` o por `vigencia_hasta` |
| Toda ruta nueva de la API se registra en la prueba del intruso | `tests/aislamiento/test_intruso.py`: `DETALLES` (GET por id → 404), `LISTADOS` (GET → 200 sin el id ajeno) o `ACCIONES` (POST con `conjunto` en el cuerpo → 400 y el otro conjunto intacto). Si no, falla `test_toda_ruta_de_la_api_esta_cubierta` |
| Índices encabezados por `conjunto` | `models.Index(fields=["conjunto", ...], name="...")` |
| `update()` y `bulk_create()` se saltan `save()` | Si los usas, fija el conjunto a mano, como `apps/notificaciones/canal.py` |
| Front: nunca manda el conjunto, ningún hex, todo autoalojado | Guía §4.3. Cada pantalla real sobreescribe `{% block estado_vista %}{% endblock %}`; si no, sale la pastilla "Maqueta con datos de ejemplo" |

*Guía §4.3* es hoy [reglas_frontend](reglas_frontend.md).

## Ver también

- [capas](capas.md) — qué va en la vista, el serializer, el servicio y el modelo
- [convenciones](convenciones.md) — estilo, nombres y lo que no se toca
- [lista_de_salida](lista_de_salida.md) — antes de decir *terminé*
