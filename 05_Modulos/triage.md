---
resumen: "La Secretaría clasifica y no decide: prioridad, rechazo formal, bandeja y anuncios con alcance."
tipo: modulo
modulo: triage
hu: [HU-22, HU-23, HU-24, HU-25]
origen: "maestro v1.4 (2026-09-14) §5.7 + plan de anuncios con fotos (2026-10-05)"
actualizado: 2026-10-05
---

# Secretaría, triage y anuncios

## Diseño (maestro §5.7)

Hasta hace poco `Secretaría` era una fila del catálogo que ningún flujo nombraba. Un rol así no sobrevive a la primera pregunta del jurado: _¿qué hace esta persona que no pueda hacer el administrador?_

**La respuesta: la Secretaría no decide, clasifica.** Recibe todo lo que entra, lo pone en condiciones de ser decidido, y le devuelve al administrador una bandeja donde lo primero es lo primero.

**El triage separa la forma del fondo.**

- **La forma** — _"¿esto está en condiciones de tramitarse?"_ — es de la Secretaría
- **El fondo** — _"¿esto se concede?"_ — es del Administrador, y no se delega

Sin esa frontera, el filtro se vuelve una segunda instancia decisoria sin responsable.

**Las tres solicitudes** comparten un contrato de triage de tres campos, pero **no son una entidad con subtipos**: cada una tiene su módulo, su ciclo y sus reglas.

|Solicitud|¿Prioridad?|Rechazo formal|Orden en la bandeja|
|---|---|---|---|
|**Cita** con el administrador|Sí|Sí|Prioridad, luego antigüedad|
|**Caso** de un residente|Sí|Sí|Prioridad, luego antigüedad|
|**Evento** (reserva de zona común)|**No**|Sí|**Solo antigüedad**|

**Por qué el Evento no lleva prioridad — esto hay que saber responderlo.** En una cita o un caso el orden es **conveniencia de gestión**: nadie pierde nada porque la fuga del 302 se atienda antes que la queja por ruido del 105. En una reserva el orden es **la promesa de equidad sobre un bien escaso**: hay un solo salón el 31 de diciembre y el sistema prometió que el primero que llega es el primero que puede pedirlo. **Una prioridad sobre eventos convertiría a la secretaría en la asignadora del salón comunal.**

Que el sistema tenga dos disciplinas de cola no es inconsistencia: es que las dos colas existen por razones distintas.

**La prioridad.** Cuatro niveles fijos en código: `BAJA · NORMAL · ALTA · URGENTE`.

- **`NORMAL` lo pone el sistema al crear**, no una persona. Una solicitud sin clasificar entra a la cola igual
- **`URGENTE` exige justificación escrita.** Es el único nivel que cuesta algo escribir, y es el que se iba a inflar
- Todo cambio queda en auditoría con valor anterior, nuevo, actor y fecha. **La prioridad es un campo con historia**
- El administrador puede re-priorizar
- Orden: `prioridad DESC, fecha_creacion ASC`, **no configurable**. No existe la pantalla que lo cambie
- **La vista por antigüedad pura está a un clic** e ignora la prioridad por completo — es la salida de emergencia si algo quedó enterrado
- Sobre Eventos la operación **no existe**: el campo no está en la entidad y el endpoint devuelve 400

**El rechazo por causal formal.** Cierra una solicitud que no está en condiciones de tramitarse, con categoría de **lista cerrada** y explicación escrita. **No existe la categoría `OTRO`** — sería la puerta por la que "no está en condiciones" se convierte en cualquier cosa. (El rechazo del administrador sí tiene `OTRO`, porque él decide de fondo y el fondo no cabe en una lista.)

Es **terminal**: no se reversa, no se edita, el solicitante vuelve a solicitar. En un Caso, cuenta como la respuesta obligatoria. En un Evento, libera la franja y avisa a los suscritos — pero **no consume oportunidad de R9**, porque el residente no dejó vencer nada: le devolvieron la solicitud.

**La bandeja** es una vista, no una entidad. Tres pestañas más vista combinada, filtros, columnas fijas con la **antigüedad siempre visible**. Deliberadamente **no** tiene aprobación, respuesta de fondo, reasignación ni exportación.

**El triage es opcional.** El sistema opera con **cero secretarías**: la prioridad nace en `NORMAL` y la bandeja se ordena sola. Es obligatorio que funcione así, porque en un conjunto pequeño el administrador **es** la secretaría.

**Anuncios con alcance.** Dos modos, y **ninguno es una lista de personas**:

| Alcance              | Quién lo recibe                                                                  | Cómo se resuelve                      |
| -------------------- | -------------------------------------------------------------------------------- | ------------------------------------- |
| **Todo el conjunto** | Toda persona con asignación vigente                                              | Consulta por `conjunto_id`            |
| **Una vivienda**     | Todo vínculo vigente sobre esa unidad — propietario y arrendatario, residan o no | Servicio de enrutamiento por vínculos |

**No existe el alcance "persona"**: entre una vivienda y una persona está la frontera de lo que todavía se puede llamar anuncio. Sigue siendo unidireccional: sin respuesta, sin hilo, sin tiempo real.

> [!NOTE] Ampliación del 2026-10-05: los anuncios llevan fotos
> El maestro §5.7 describe el anuncio como texto. Alejo pidió que pueda llevar fotos; los alcances y la vía única no cambian. Cómo quedó, abajo.

## Cómo está construido: fotos en los anuncios (2026-10-05)

Un anuncio se publica solo con texto o con texto y **hasta 4 fotos** (PNG, JPG o WebP, de hasta 5 MB cada una). El detalle de la API está en `Backend/Admind_Backend/apps/anuncios/README.md`.

| Regla | Dónde se cumple |
|---|---|
| Hasta 4 fotos | El serializer las cuenta y la base lo guarda: `UNIQUE (anuncio, orden)` y `CHECK (orden < 4)` en `FotoDeAnuncio` |
| Solo imágenes de verdad, de hasta 5 MB | `servicios.tipos_de_las_fotos()` lee la firma de cada archivo; el nombre y el tipo que declara el navegador no cuentan |
| Todo o nada | Se revisan todas antes de guardar: con una que no sirve no se publica ni se avisa |
| Quedan fijas | Se suben al publicar. `PATCH` con `fotos` responde 400, igual que con el alcance |
| Las ve quien ve el anuncio | `GET /anuncios/<id>/fotos/<foto_id>/` pasa por el mismo `tablon()`: la foto de un anuncio dirigido responde 404 al vecino |
| No viajan en el aviso | El texto de la bandeja y del correo termina diciendo cuántas fotos tiene |

Las fotos van en una tabla aparte, con `BinaryField`, para que listar anuncios no traiga las imágenes; es el mismo patrón de la foto del conjunto ([conjuntos](conjuntos.md)). En el front, la imagen la pide el servidor web con el token y se la pasa al navegador. Junto al campo de fotos hay una advertencia: una foto donde se reconoce a una persona es un dato personal (Ley 1581).

## Ver también

- [riesgos](../06_Decisiones/riesgos.md) — R9
