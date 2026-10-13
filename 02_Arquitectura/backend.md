---
resumen: "El backend por dentro: anatomía de una app (capas y patrón de errores) y las piezas compartidas de apps/comun y auditoría."
tipo: arquitectura
origen: "guía de estructura §5.1 y §5.2 (2026-09-30)"
actualizado: 2026-10-11
revisado: 2026-10-11
---

# El backend por dentro

## Anatomía de una app

Todas las apps con código siguen la misma forma. Con `reservas` como ejemplo:

| Archivo | Capa (profesor) | Qué contiene en `reservas` |
|---|---|---|
| `urls.py` | Controller (rutas) | 12 rutas: franjas, solicitudes, detalle, liberar y enviar (HU-11 a HU-13); bandeja, solicitudes del área y decisión (HU-14); pago, retirar el pago, comprobantes y el archivo de un comprobante (HU-16) |
| `views.py` | Controller | Una clase por ruta. Exige el permiso, valida con un serializer, llama al servicio y traduce cada excepción a un código HTTP (400, 404, 409) |
| `serializers.py` | DTO | Forma de la entrada (`TomarBloqueoSerializer`) y de la salida (`DetalleDeSolicitudSerializer`) |
| `servicios.py` | Service | Las reglas: `franjas()`, `tomar_bloqueo()`, `liberar()`, `enviar()` y `decidir_solicitud()`; el pago declarado va aparte, en `pago.py`. Lanza excepciones con nombre (`FranjaOcupada`, `BloqueoVencido`, `IncumpleReglas`…) |
| `models.py` | Repository (con el Manager) | `Solicitud`, sus estados y sus restricciones |
| `migrations/` | — | Cómo se crea la tabla |
| `tests.py` | — | Pruebas de la app |
| `README.md` | — | Para qué existe |

Fíjate en el patrón de errores: el **servicio** dice *qué* pasó con una excepción con nombre de negocio (`FranjaOcupada`); la **vista** decide *cómo* se dice por HTTP (`409 "Otra persona está tramitando esta franja"`). Así el servicio no sabe nada de HTTP.

## `apps/comun/` y la auditoría

El aislamiento entre conjuntos (`apps/comun/aislamiento/` y `modelos_base/`) tiene su propia nota: [aislamiento](../03_Reglas/aislamiento.md).

### b) El bloqueo (`apps/comun/bloqueo/`, HU-11)

Resuelve: *"si 50 residentes pulsan «Reservar» en la misma franja a la vez, solo uno la obtiene"*.

- `tomar(crear)`: intenta el `INSERT` dentro de una transacción. **No pregunta antes si está libre** (entre la pregunta y el INSERT otro podría ganar). Si el índice único parcial lo rechaza, lanza `RecursoOcupado`. La base decide, y decide una sola vez.
- `expirar_vencidos(...)`: pasa a `EXPIRADA` todo lo vencido con un solo `UPDATE`. No hay proceso en segundo plano: se llama **al principio de cada consulta o acción** de reservas.

`tests/concurrencia/test_bloqueo_de_franjas.py` lanza N hilos contra la misma franja y comprueba que queda un solo bloqueo.

### c) La auditoría (`apps/auditoria/`)

Un registro de **solo inserción**: `Registro` prohíbe `update()` y `delete()`. `auditoria.servicios.registrar(actor, accion, entidad, …)` se llama, por ejemplo, al asignar o retirar un rol.

### d) Los archivos (`apps/comun/archivos/`, HU-16)

`comprobantes.py` valida un archivo **por su firma** (PDF, JPG o PNG, de hasta 5 MB), no por su nombre ni por el tipo que declara el navegador, y calcula su SHA-256. Lo usan `reservas` y `pagos`. Los archivos se guardan dentro de la base, igual que la foto del conjunto, el reglamento y las fotos de los anuncios.

## Ver también

- [mapa_codigo](mapa_codigo.md) — todas las apps, sus endpoints y su HU
- [capas](../03_Reglas/capas.md) e [invariantes](../03_Reglas/invariantes.md) — lo que respeta toda pieza nueva
- [cuentas](../05_Modulos/cuentas.md), [permisos](../05_Modulos/permisos.md), [motor_reglas](../05_Modulos/motor_reglas.md), [conjuntos](../05_Modulos/conjuntos.md), [unidades](../05_Modulos/unidades.md), [reservas](../05_Modulos/reservas.md), [ingresos](../05_Modulos/ingresos.md), [pagos](../05_Modulos/pagos.md), [parqueaderos](../05_Modulos/parqueaderos.md) — cada módulo construido
- [restricciones_bd](restricciones_bd.md) — lo que hace cumplir PostgreSQL
- [pruebas_y_ejecucion](pruebas_y_ejecucion.md) — qué prueba cubre cada app
