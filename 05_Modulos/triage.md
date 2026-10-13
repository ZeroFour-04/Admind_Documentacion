---
resumen: "La Secretaría clasifica y no decide: prioridad, rechazo formal, bandeja y anuncios con alcance."
tipo: modulo
modulo: triage
hu: [HU-22, HU-23, HU-24, HU-25, HU-29]
origen: "maestro v1.4 (2026-09-14) §5.7 + plan de anuncios con fotos (2026-10-05)"
actualizado: 2026-10-13
revisado: 2026-10-13
---

# Secretaría, triage y anuncios

> [!NOTE] Qué hay construido (verificado el 2026-10-13)
> - **Anuncios (HU-25):** construidos, con fotos. Sección *Cómo está construido*, abajo.
> - **Casos (HU-29) y el dashboard de gestión:** construidos el 13/10 sobre lo que Camilo subió el 12/10. Sección *Cómo está construido: el dashboard y los casos*, abajo.
> - **De la bandeja de triage (HU-22 a HU-24) hay una parte:** las pestañas por tipo, la prioridad sobre casos y el descarte por causal formal de reservas y casos. No hay vista combinada (decisión de Alejo del 13/10), ni nada sobre citas, que no existen. En el backend `apps/triage/` sigue con solo README: el dashboard es una pantalla del front que le pide las filas a cada módulo.
> - **La Secretaría ya no aprueba reservas** (Alejo, 13/10): el código volvió a coincidir con este diseño. Y una diferencia a propósito: el diseño dice que la bandeja no tiene respuesta de fondo; aquí el administrador responde desde el detalle del caso, al que se llega por la fila.

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

## Cómo está construido: el dashboard y los casos (2026-10-13)

**El dashboard** (`/solicitudes/`, «Dashboard de Gestión de Reservas») es de quien tiene `solicitud.bandeja_ver`: Administración, Secretaría y Superusuario. Tiene una pestaña por tipo, cada una con su tabla y cuántas hay pendientes. Las pestañas no se mezclan y cada una le pide las filas a su módulo. El detalle de las pantallas está en `Frontend/Admind_Front-End/apps/triage/README.md`.

| Pestaña | Orden | La fila lleva a |
|---|---|---|
| Reservas | La que más lleva esperando primero. Sin prioridad | La tarjeta de la solicitud en la pantalla de su zona ([reservas](reservas.md)) |
| Casos | Abiertos primero, por prioridad y luego antigüedad. «Por antigüedad» ignora la prioridad | El detalle del caso |
| Citas | — | Un estado vacío: el módulo no existe |

**Quién hace qué sobre un caso.** La Secretaría clasifica y la Administración decide; Administración puede atender un caso sin que nadie se lo redirija, porque el sistema tiene que funcionar con cero secretarías.

| Estado | Quién lo produce | Sale hacia |
|---|---|---|
| Por revisar (`ABIERTO`) | El residente, al abrirlo | En revisión, Redirigido, Rechazado, Resuelto |
| En revisión | Quien lo toma. Es opcional: avisa al residente que ya lo ven | Redirigido, Rechazado, Resuelto |
| Redirigido | Secretaría, con una nota interna opcional | Resuelto, Rechazado |
| Citado | Nadie todavía: depende de citas | Resuelto, Rechazado |
| Resuelto | Administración, con respuesta escrita obligatoria | Terminal |
| Rechazado | Secretaría (descarte: causal de lista cerrada y comentario) o Administración (motivo) | Terminal |

| Regla | Dónde se cumple |
|---|---|
| Un caso no se cierra sin algo escrito para el residente | El serializer, el servicio y dos `CHECK`: `caso_resuelto_con_respuesta` y `caso_rechazado_con_motivo` |
| `NORMAL` la pone el sistema | `default` y `db_default` en `Caso.prioridad` |
| `URGENTE` exige justificación | El serializer y el `CHECK` `caso_urgente_con_justificacion` |
| La prioridad tiene historia | `caso.priorizar` en la auditoría, con el valor anterior y el nuevo. No avisa al residente |
| Cada cambio de estado avisa al residente, por la aplicación y por correo | `servicios.avisar`, dentro de la transacción. No dice quién actuó |
| Dos personas a la vez no se pisan | `servicios._pasar` bloquea la fila; la segunda recibe 409 |
| El residente no ve la nota interna, la justificación ni quién actuó | Dos serializers: `CasoSerializer` y `CasoParaGestionSerializer` |
| El descarte de la Secretaría no tiene «otro» | `CausalDeDescarte`: no es competencia, duplicado o información insuficiente. Lo que no cabe se redirige |

Las rutas están en `Backend/Admind_Backend/apps/casos/README.md`. El caso no guarda la vivienda: se deduce de dónde reside hoy quien lo abrió.

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

- [riesgos](../06_Decisiones/riesgos.md) — R9, R13 y R14
- [unidades](unidades.md) — el enrutamiento por vínculos del anuncio a una vivienda
- [reservas](reservas.md) — el Evento: la solicitud de reserva
- [citas](citas.md) e [infracciones](infracciones.md) — los otros módulos que pasan por la Secretaría
- [Plan_Anuncios_Con_Fotos](../07_Planes/hechos/Plan_Anuncios_Con_Fotos.md) — el plan de las fotos
- [historias](../08_Estado/historias.md) — HU-22 a HU-25 y HU-29
- `Backend/Admind_Backend/apps/anuncios/README.md`
