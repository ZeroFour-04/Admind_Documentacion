---
resumen: "Restricciones que hace cumplir PostgreSQL: las verificadas en la base y las que sostienen la concurrencia de reservas."
tipo: arquitectura
origen: "avance §2.3 (2026-09-15) + guía de estructura §4.4 (2026-09-30)"
actualizado: 2026-10-06
---

# Restricciones en PostgreSQL

## Las que sostienen reservas y el aislamiento (2026-09-30)

AdMind no confía solo en Python para las reglas importantes: las repite como **restricciones en la base**, porque la base es la única que ve todas las peticiones a la vez. Tres ejemplos reales:

| Restricción | Dónde | Qué impide |
|---|---|---|
| Índice único parcial `solicitud_franja_bloqueante_unica` | `reservas/models.py` | Que dos personas tengan la misma franja en trámite, apartada o reservada, **aunque hagan clic en el mismo milisegundo** |
| Índice único parcial `solicitud_un_bloqueo_por_persona` | ídem | Que una persona tenga dos bloqueos a la vez |
| FK compuesta `(x_id, conjunto_id)` | `apps/comun/aislamiento/migraciones.py` → `fk_compuesta()` | Que una fila apunte a algo de **otro conjunto** |

"Índice único **parcial**" significa: "único, pero solo entre las filas que cumplen una condición" (por ejemplo, solo las solicitudes en estado `EN_SOLICITUD`, `APARTADA` o `RESERVADA`). Las solicitudes expiradas o liberadas no cuentan, y por eso la franja vuelve a quedar libre.

## Áreas y reglas (2026-10-06)

Llegaron con el motor de reglas por niveles. Están en el modelo y en las migraciones `areas/0004` y `reglas/0004`, y tienen prueba que escribe directo en la base. En `admind_db` existen desde que se corra `migrate`.

| Restricción | Dónde | Qué impide |
|---|---|---|
| `CHECK` `area_aforo_maximo_valido` | `areas/models.py` | Un área con aforo menor que 1. El campo es obligatorio |
| `CHECK` `regla_nivel_coherente` | `reglas/models.py` | Una regla **abierta** en el nivel equivocado: una del conjunto con área, o una de un área sin ella. Las cerradas son historial y no se revisan |
| Índice único parcial `regla_alfa_unica_abierta` | ídem | Dos reglas abiertas del mismo tipo en el conjunto |
| Índice único parcial `regla_beta_unica_abierta` | ídem | Dos reglas abiertas del mismo tipo en la misma área |

Una regla *abierta* es la que tiene `vigencia_hasta` vacía. La FK compuesta `(area_id, conjunto_id)` de `Regla` no cambió: PostgreSQL no la revisa cuando `area_id` es nulo, que es el caso de las reglas del conjunto.

## Verificadas en `admind_db` (2026-09-14 y 2026-09-15)

Faltan aquí las de las tablas creadas después (áreas, reglas, reservas, auditoría, unidades): están en el `models.py` de cada app.

Revisadas directamente en `admind_db`, no solo en el código de Python: las de `personas` y `cuentas_usuario` el 2026-09-14, las de `permisos` y `cuentas_tokendesesion` el 2026-09-15. La FK compuesta de HU-05 todavía no existe en `admind_db` porque ninguna tabla del producto la usa; se verifica en la base de pruebas (§5.3).

| Tabla | Restricción | Qué impide |
|---|---|---|
| `personas_persona` | `persona_documento_unico` | Dos personas con el mismo tipo y número de documento |
| `personas_persona` | `persona_tipo_documento_valido` | Un tipo de documento fuera de `CC`, `TI`, `CE`, `PAS`, `PPT` |
| `personas_persona` | `persona_documento_normalizado` | Guardar un número con puntos, espacios o ceros a la izquierda |
| `personas_persona` | `persona_telefono_valido` | Un teléfono con letras o de largo inválido |
| `cuentas_usuario` | `UNIQUE (correo)` | Dos cuentas con el mismo correo |
| `cuentas_usuario` | `UNIQUE (persona_id)` + FK a `personas_persona` | Dos cuentas para la misma persona, o una cuenta sin persona |
| `permisos_asignacion` | `asignacion_conjunto_segun_alcance` (CHECK) | Un Superusuario atado a un conjunto, un rol de conjunto sin conjunto, o un rol fuera del catálogo |
| `permisos_asignacion` | `asignacion_vigencia_coherente` (CHECK) | Una vigencia que termina antes de empezar |
| `permisos_asignacion` | `asignacion_vigente_unica` (índice único parcial, `NULLS NOT DISTINCT`) | La misma persona con el mismo rol vigente dos veces en el mismo conjunto. `NULLS NOT DISTINCT` hace que también aplique al Superusuario, cuyo conjunto es nulo |
| `permisos_asignacion` | FK a `personas_persona` y a `conjuntos_conjunto` | Una asignación a una persona o a un conjunto que no existe |
| `cuentas_tokendesesion` | `UNIQUE (huella)` | Dos sesiones con el mismo token |
| `cuentas_tokendesesion` | FK a `cuentas_usuario` y a `conjuntos_conjunto` | Una sesión de un usuario que no existe, o con un conjunto activo que no existe |
