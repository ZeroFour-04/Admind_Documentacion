---
resumen: "Restricciones que hace cumplir PostgreSQL: las verificadas en la base y las que sostienen la concurrencia de reservas."
tipo: arquitectura
origen: "avance §2.3 (2026-09-15) + guía de estructura §4.4 (2026-09-30)"
actualizado: 2026-10-10
---

# Restricciones en PostgreSQL

## Las que sostienen reservas y el aislamiento (2026-09-30)

AdMind no confía solo en Python para las reglas importantes: las repite como **restricciones en la base**, porque la base es la única que ve todas las peticiones a la vez. Tres ejemplos reales:

| Restricción | Dónde | Qué impide |
|---|---|---|
| Índice único parcial `solicitud_franja_bloqueante_unica` | `reservas/models.py` | Que dos personas tengan la misma franja en trámite, apartada o reservada, **aunque hagan clic en el mismo milisegundo** |
| Índice único parcial `solicitud_un_bloqueo_por_persona` | ídem | Que una persona tenga dos bloqueos a la vez |
| `UNIQUE` `pago_unico_por_vivienda_y_mes` | `pagos/models.py` (`pagos/0001`) | Dos filas de pago para la misma vivienda y el mismo mes (HU-35), aunque dos clics lleguen a la vez |
| `CHECK` `pago_periodo_es_dia_uno`, `pago_confirmado_completo` y `pago_reportado_completo` | ídem | Un periodo que no sea el día 1, un check sin fecha o sin quién lo puso, un reporte sin persona o sin fecha |
| `CHECK` `regla_tipo_valido` y `regla_nivel_coherente` | `reglas/models.py` (`reglas/0007`) | Se rehicieron para el tipo nuevo `DIA_LIMITE_DE_PAGO` (alfa): un tipo de regla nuevo pide migración |
| Índice único parcial `visitante_parqueadero_ocupado_unico` | `visitantes/models.py` (`visitantes/0003`) | Que dos visitas **sin salida** tengan el mismo parqueadero de visitantes. Al poner `hora_salida` la fila sale del índice y el puesto queda libre; las visitas sin parqueadero no cuentan (HU-28) |
| `CHECK` `visitante_salida_despues_de_entrada` | `visitantes/models.py` (`visitantes/0002`) | Una salida anterior a la entrada |
| `UNIQUE` `parqueadero_codigo_unico` y `CHECK` `parqueadero_tipo_valido` | `parqueaderos/models.py` | Dos parqueaderos con el mismo código en un conjunto (se guarda en mayúsculas, así que «v-01» y «V-01» chocan) o un tipo que no sea `residentes` ni `visitantes` |
| `CHECK` `solicitud_pago_declarado_completo` | ídem (`reservas/0003`) | Que un pago quede «declarado» sin fecha o con fecha y sin quién lo declaró: `pago_declarado_por` y `pago_declarado_en` van los dos o ninguno (HU-16). Se probó con un `UPDATE` directo, que se salta el código de Python |
| FK compuesta `(x_id, conjunto_id)` | `apps/comun/aislamiento/migraciones.py` → `fk_compuesta()` | Que una fila apunte a algo de **otro conjunto** |

"Índice único **parcial**" significa: "único, pero solo entre las filas que cumplen una condición" (por ejemplo, solo las solicitudes en estado `EN_SOLICITUD`, `APARTADA` o `RESERVADA`). Las solicitudes expiradas o liberadas no cuentan, y por eso la franja vuelve a quedar libre.

## Áreas y reglas (2026-10-06)

Llegaron con el motor de reglas por niveles. Están en el modelo y en las migraciones `areas/0004` y `reglas/0004`, y tienen prueba que escribe directo en la base. En `admind_db` existen desde que se corra `migrate`.

| Restricción | Dónde | Qué impide |
|---|---|---|
| `CHECK` `area_aforo_maximo_valido` | `areas/models.py` | Un área con aforo menor que 1. El campo es obligatorio |
| `CHECK` `area_modo_coherente` | `areas/models.py` | Un área con reserva sin duración de franja o con permanencia, o una con ingreso sin permanencia o con duración (2026-10-08) |
| `CHECK` `regla_nivel_coherente` | `reglas/models.py` | Una regla **abierta** en el nivel equivocado: una del conjunto con área, o una de un área sin ella. Las cerradas son historial y no se revisan |
| Índice único parcial `regla_alfa_unica_abierta` | ídem | Dos reglas abiertas del mismo tipo en el conjunto |
| Índice único parcial `regla_beta_unica_abierta` | ídem | Dos reglas abiertas del mismo tipo en la misma área |

Los `CHECK` `regla_tipo_valido` y `regla_nivel_coherente` listan los tipos del catálogo, así que **un tipo de regla nuevo pide migración**: `reglas/0005` (acompañantes) y `reglas/0006` (una reserva al día y sin franjas seguidas, 2026-10-10, sin aplicar en `admind_db`).

Una regla *abierta* es la que tiene `vigencia_hasta` vacía. La FK compuesta `(area_id, conjunto_id)` de `Regla` no cambió: PostgreSQL no la revisa cuando `area_id` es nulo, que es el caso de las reglas del conjunto.

## Viviendas y documentos (2026-10-06)

Las trae `unidades/0002_estructura`; el reglamento solo lleva las de toda tabla de conjunto. Sin aplicar todavía en `admind_db`.

| Restricción | Dónde | Qué impide |
|---|---|---|
| `UNIQUE (conjunto, clave)` = `agrupacion_clave_unica_en_conjunto` | `unidades/models.py` | Dos agrupaciones iguales en el conjunto. `clave` es la etiqueta y el nombre sin tildes ni mayúsculas: «Torre 1» y «TORRE 1» son la misma |
| `CHECK` `agrupacion_tipo_vivienda_valido` y `unidad_tipo_valido` | ídem | Un tipo de vivienda que no sea `apartamento` o `casa` |
| FK compuesta `(agrupacion_id, conjunto_id)` | migración `unidades/0002_estructura` | Que una vivienda apunte a una agrupación de otro conjunto. Con `agrupacion_id` nulo no aplica |

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

## Ingresos a zonas (2026-10-08)

Llegaron con la app `ingresos` (`ingresos/0001_initial`, sin aplicar en `admind_db`) y tienen prueba que escribe directo en la base.

| Restricción | Dónde | Qué impide |
|---|---|---|
| Índice único parcial `ingreso_uno_abierto_por_persona` | `ingresos/models.py` | Que una persona tenga dos ingresos `ADENTRO` en el conjunto, **aunque dos zonas la registren a la vez** |
| `CHECK` `ingreso_estado_valido` | ídem | Un estado que no sea `ADENTRO`, `SALIO` o `VENCIDO` |
| `CHECK` `ingreso_salida_prevista_coherente` | ídem | Una salida prevista que no sea posterior a la entrada |
| `CHECK` `ingreso_salida_segun_estado` | ídem | Un ingreso `ADENTRO` con hora de salida, o uno que ya salió sin ella |
| FK compuesta `(area_id, conjunto_id)` y `(unidad_id, conjunto_id)` | migración `ingresos/0001` | Un ingreso que apunte a un área o a una vivienda de otro conjunto |

**El aforo no está aquí.** Es una suma de filas, no una fila única, así que ningún índice lo custodia: lo decide el servicio, que toma la fila del área con `select_for_update` ([ingresos](../05_Modulos/ingresos.md)).
