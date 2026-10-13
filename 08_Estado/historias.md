---
resumen: "Las 40 historias de usuario: sprint previsto, story points, estado en el código, la nota de su módulo, su plan y lo que le falta a cada una."
tipo: estado
corte: 2026-10-13
origen: "Notion (títulos, puntos y sprint) + código verificado el 2026-10-11"
actualizado: 2026-10-13
revisado: 2026-10-13
---

# Historias de usuario

Títulos, story points y sprint previsto salen de Notion (`Gestión Scrum — AdMind` → `Historias de Usuario`). El estado es el del código, verificado el 2026-10-11 sobre Backend `d4e98e5` y Frontend `a946880`: todo lo que aparece aquí como construido **tiene commit, está subido y migrado**.

| Estado | Significa |
|---|---|
| **Construida** | El código y sus pruebas existen. Falta la parte humana de la DoD: PR `desarrollo → pruebas` revisado y prueba manual de quien no la programó |
| **Parcial** | Hay código, pero no cubre todos sus criterios |
| **Sin empezar** | Solo el README de su app, o nada |

Con la DoD **ninguna está Terminada**. Cómo se reportan al docente: [estado_actual](estado_actual.md).

## Totales (corte 2026-10-13)

| | Historias | SP |
|---|---|---|
| Construidas | 21 | 105 |
| Parciales (HU-27, HU-33) | 2 | 8 |
| Sin empezar | 15 | 75 |
| **Las 38 del backlog** | **38** | **188** |
| Nuevas, sin puntos (HU-39, HU-40) | 2 | — |

El reparto por sprint está en [estado_actual](estado_actual.md).

## Todas las historias

*Sprint* es el reparto previsto en el Excel V11.1, que ya no se cumple con el plazo de un mes. *Módulo* enlaza la nota con sus reglas de negocio; la app del código está en [mapa_codigo](../02_Arquitectura/mapa_codigo.md).

| HU | Historia | Sprint | SP | Prioridad | Estado | Módulo | Plan |
|---|---|---|---|---|---|---|---|
| HU-01 | Inicio de sesión con correo y contraseña | 1 | 3 | Alta | Construida | [cuentas](../05_Modulos/cuentas.md) | [Recuperacion_Contrasena](../07_Planes/hechos/Plan_Recuperacion_Contrasena.md) |
| HU-02 | Segundo factor (TOTP) para permisos sensibles | 1 | 5 | Alta | Construida | [cuentas](../05_Modulos/cuentas.md) | — |
| HU-03 | Asistente por pasos para crear un conjunto | 1 | 6 | Alta | Construida | [conjuntos](../05_Modulos/conjuntos.md) | [Asistente_De_Creacion](../07_Planes/hechos/Plan_Asistente_De_Creacion.md) |
| HU-04 | Persona global única por documento | 1 | 3 | Alta | Construida | [personas](../05_Modulos/personas.md) | — |
| HU-05 | Aislamiento de datos entre conjuntos | 1 | 2 | Alta | Construida | [aislamiento](../03_Reglas/aislamiento.md) | — |
| HU-26 | Selector de conjunto activo | 1 | 6 | Alta | Construida | [cuentas](../05_Modulos/cuentas.md) | — |
| HU-06 | Asignación de roles del catálogo fijo | 2 | 6 | Alta | Construida | [permisos](../05_Modulos/permisos.md) | [Sprints_2_3](../07_Planes/hechos/Admind_Plan_Sprints_2_3.md) |
| HU-07 | Vincular persona existente por búsqueda de documento | 2 | 3 | Alta | Construida | [personas](../05_Modulos/personas.md) | [Sprints_2_3](../07_Planes/hechos/Admind_Plan_Sprints_2_3.md) |
| HU-08 | Vínculos de unidad y enrutamiento de notificaciones | 2 | 7 | Alta | Construida | [unidades](../05_Modulos/unidades.md) | [Sprints_2_3](../07_Planes/hechos/Admind_Plan_Sprints_2_3.md) |
| HU-09 | Catálogo de áreas comunes del conjunto | 2 | 4 | Alta | Construida | [motor_reglas](../05_Modulos/motor_reglas.md) (modo de uso y aforo) | [Sprints_2_3](../07_Planes/hechos/Admind_Plan_Sprints_2_3.md), [Motor_De_Reglas](../07_Planes/hechos/Plan_Motor_De_Reglas.md) |
| HU-10 | Configuración de reglas beta de reserva | 3 | 9 | Alta | Construida | [motor_reglas](../05_Modulos/motor_reglas.md) | [Sprints_2_3](../07_Planes/hechos/Admind_Plan_Sprints_2_3.md), [Motor_De_Reglas](../07_Planes/hechos/Plan_Motor_De_Reglas.md) |
| HU-11 | Bloqueo exclusivo de 3 minutos sobre una franja | 3 | 7 | Alta | Construida | [reservas](../05_Modulos/reservas.md) | [Sprints_2_3](../07_Planes/hechos/Admind_Plan_Sprints_2_3.md) |
| HU-12 | Confirmación de contenido antes de enviar | 3 | 2 | Alta | Construida | [reservas](../05_Modulos/reservas.md) | [Sprints_2_3](../07_Planes/hechos/Admind_Plan_Sprints_2_3.md) |
| HU-13 | Envío de solicitud y motor de reglas alfa/beta | 3 | 8 | Alta | Construida | [reservas](../05_Modulos/reservas.md), [motor_reglas](../05_Modulos/motor_reglas.md) | [Sprints_2_3](../07_Planes/hechos/Admind_Plan_Sprints_2_3.md), [Motor_De_Reglas](../07_Planes/hechos/Plan_Motor_De_Reglas.md) |
| HU-14 | Bandeja del administrador: aprobar o rechazar | 4 | 8 | Alta | Construida | [reservas](../05_Modulos/reservas.md) | [Plan_Dashboard_De_Solicitudes](../07_Planes/hechos/Plan_Dashboard_De_Solicitudes.md) |
| HU-15 | Condiciones del alquiler congeladas y versionadas | 4 | 4 | Alta | Sin empezar | [reservas](../05_Modulos/reservas.md) | — |
| HU-16 | Registro de pago declarado y comprobante | 4 | 4 | Media | Construida | [reservas](../05_Modulos/reservas.md) | [Pago_De_Reserva](../07_Planes/hechos/Plan_Pago_De_Reserva.md) |
| HU-17 | Cancelación de reservas en firme | 4 | 3 | Media | Sin empezar | [reservas](../05_Modulos/reservas.md) | — |
| HU-18 | Aviso de disponibilidad de franja (campana) | 4 | 6 | Media | Sin empezar | [reservas](../05_Modulos/reservas.md) | — |
| HU-19 | Dos oportunidades por franja y aviso de última | 4 | 3 | Media | Sin empezar | [reservas](../05_Modulos/reservas.md) | — |
| HU-20 | Anulación de registros por el Superusuario | 5 | 5 | Media | Sin empezar | [eliminacion](../03_Reglas/eliminacion.md) | — |
| HU-21 | Identidad visual del conjunto: color y logo | 5 | 4 | Baja | Construida | [conjuntos](../05_Modulos/conjuntos.md) | — |
| HU-25 | Anuncios con alcance de conjunto o vivienda | 5 | 6 | Media | Construida | [triage](../05_Modulos/triage.md) | [Anuncios_Con_Fotos](../07_Planes/hechos/Plan_Anuncios_Con_Fotos.md) |
| HU-27 | Registro de visitantes y vehículos | 5 | 5 | Media | Parcial (Camilo) | [parqueaderos](../05_Modulos/parqueaderos.md) | [Parqueadero_De_Visitantes](../07_Planes/hechos/Plan_Parqueadero_De_Visitantes.md) |
| HU-28 | Parqueadero de visitantes atado a la visita | 5 | 3 | Media | Construida | [parqueaderos](../05_Modulos/parqueaderos.md) | [Parqueadero_De_Visitantes](../07_Planes/hechos/Plan_Parqueadero_De_Visitantes.md) |
| HU-29 | Tablero de casos con respuesta obligatoria | 5 | 5 | Media | Construida | [triage](../05_Modulos/triage.md) | [Plan_Dashboard_De_Solicitudes](../07_Planes/hechos/Plan_Dashboard_De_Solicitudes.md) |
| HU-22 | Bandeja de triage de la Secretaría | 6 | 7 | Media | Sin empezar | [triage](../05_Modulos/triage.md) | — |
| HU-23 | Prioridad sobre citas y casos | 6 | 5 | Media | Sin empezar | [triage](../05_Modulos/triage.md) | — |
| HU-24 | Rechazo por causal formal de la Secretaría | 6 | 3 | Media | Sin empezar | [triage](../05_Modulos/triage.md) | — |
| HU-30 | Registro y comunicación de infracciones | 6 | 4 | Media | Sin empezar | [infracciones](../05_Modulos/infracciones.md) | — |
| HU-31 | Agendar cita dentro del horario de atención | 6 | 4 | Media | Sin empezar | [citas](../05_Modulos/citas.md) | — |
| HU-32 | Cambio de horario con alternativas a los afectados | 6 | 8 | Media | Sin empezar | [citas](../05_Modulos/citas.md) | — |
| HU-33 | Repositorio de documentos vigentes | 6 | 3 | Media | Parcial | [conjuntos](../05_Modulos/conjuntos.md) (el reglamento) | [Asistente_De_Creacion](../07_Planes/hechos/Plan_Asistente_De_Creacion.md) |
| HU-34 | Asignación de parqueaderos de residentes | 6 | 4 | Media | Sin empezar | [parqueaderos](../05_Modulos/parqueaderos.md) | — |
| HU-35 | Reporte de pago de administración | 7 | 4 | Baja | Construida | [pagos](../05_Modulos/pagos.md) | [Pago_De_Administracion](../07_Planes/hechos/Plan_Pago_De_Administracion.md) |
| HU-36 | Importación masiva con dry-run e idempotencia | 7 | 7 | Baja | Sin empezar | [alcance](../01_Contexto/alcance.md) 3.2 | — |
| HU-37 | Respaldo de información por conjunto | 7 | 5 | Baja | Sin empezar | [alcance](../01_Contexto/alcance.md) 3.2 | — |
| HU-38 | Registro de actividades sobre la auditoría | Condicional | 7 | Baja | Sin empezar | [alcance](../01_Contexto/alcance.md) 3.3 | — |
| HU-39 | Estructura de viviendas del conjunto: agrupaciones y generación en lote | Por definir | Por estimar | Por definir | Parcial (primera parte) | [unidades](../05_Modulos/unidades.md) | [Estructura_De_Viviendas](../07_Planes/hechos/Plan_Estructura_De_Viviendas.md) |
| HU-40 | Implementar accesibilidad | Por definir | Por estimar | Por definir | Solo existe en Notion | — | — |

**Sin historia:** el ingreso a zonas con aforo ([ingresos](../05_Modulos/ingresos.md), [Plan_Zonas_Con_Ingreso](../07_Planes/hechos/Plan_Zonas_Con_Ingreso.md)) está construido desde el 08/10 y no tiene historia ni número en Notion.

## Qué hay y qué le falta a cada una

A todas las construidas les falta la parte humana de la DoD; aquí va lo demás.

### Sprint 1

| HU | Qué hay | Qué le falta |
|---|---|---|
| HU-01 | 5 de 5 tareas y criterios. Recuperación de contraseña por enlace de un solo uso, con límite de 3 enlaces por hora y correo real por SMTP (05/10) | `send_mail` es síncrono y sin `try`: con SMTP real, un fallo da 500 solo si la cuenta existe. `/auth/login/` no limita los intentos |
| HU-02 | 5 de 5. TOTP con QR, 10 códigos de respaldo y, desde el 05/10, enlace por correo para quitarlo si se pierde la aplicación | Recorrer el enlace a mano con la API encendida y un correo real |
| HU-03 | Completa desde el 06/10: siete pasos (datos, viviendas, administración, áreas, reglas, reglamento y resumen) y seis requisitos. Un conjunto ya puede quedar operativo y lo activa el Superusuario o Administración. Desde el 11/10 Administración ve «Crear conjunto» en el selector | Sus criterios en Notion describen el asistente anterior. Dejar operativo un conjunto no queda en la auditoría, y reservar no exige que el conjunto esté operativo |
| HU-04 | 5 de 5 | — |
| HU-05 | 5 de 5. Desde el 27/09 lo usan tablas reales | Cinco rutas sin registrar en la prueba del intruso ([estado_actual](estado_actual.md)) |
| HU-26 | 5 de 5, conectada a la API | — |

### Sprints 2 y 3

Construidos el 27/09 con el plan F0 a F10. Cada criterio de aceptación tiene una prueba automática con nombre propio; el detalle está en [historias_evidencia](historias_evidencia.md).

| HU | Qué hay | Qué le falta u observaciones |
|---|---|---|
| HU-06 | Todos los criterios con prueba. «Nunca cero Administración» responde 409 y tiene prueba con dos hilos. Desde el 29/09, **un solo rol por conjunto**; desde el 11/10, al registrar a alguien el rol marcado es Residente | Su criterio en Notion y en el Excel todavía dice varios roles |
| HU-07 | Todos los criterios con prueba | El máximo de 20 búsquedas por hora se cuenta **por conjunto**; falta decidir si debe ser global |
| HU-08 | Todos los criterios con prueba. Solo se vincula a quien ya tiene un rol en el conjunto. Desde el 11/10, en el detalle de la vivienda se busca a la persona y se puede crear un residente | — |
| HU-09 | Todos los criterios con prueba. Franjas por bloques fijos (D1 a). Desde el 06/10, **aforo máximo obligatorio**; desde el 08/10, **modo de uso** (con reserva o con ingreso), que desde el 13/10 se puede cambiar al editar | Sus criterios en Notion describen el modelo anterior |
| HU-10 | Reconstruida por niveles el 06/10: reglas del conjunto (alfa) y del área (beta), una sola abierta por tipo, con descripción fija, versionado y días que no abre con motivo. El 10/10 ganó dos reglas de área, *una reserva al día* y *sin franjas seguidas* | Sus criterios en Notion describen el modelo anterior y no traen las dos reglas nuevas |
| HU-11 | Todos los criterios con prueba, incluida la de concurrencia con 10 hilos | Probar a mano el `sendBeacon` que libera el bloqueo al cerrar la pestaña |
| HU-12 | 3 de 5 criterios con prueba automática | «Corregir sin perder lo escrito» y «el reloj no se detiene» necesitan prueba manual. La alta demanda depende de PB-24, que no existe |
| HU-13 | Todos los criterios con prueba. El evaluador junta reglas del sistema, aforo del área, reglas del conjunto y reglas del área. Desde el 10/10 la mora la responde `pagos` con el día límite de pago | Las reglas de piscina y de cobro quedan fuera |

### Sprint 4

| HU | Qué hay | Qué le falta |
|---|---|---|
| HU-14 | Camilo, 05/10: solicitudes por área y bandeja del conjunto, aceptar o rechazar, auditoría y 409 si ya se decidió. Agente, 13/10: la bandeja trae primero la que más lleva esperando; rechazar exige categoría y, con «Otro motivo», el texto (lo exige también la base); la Secretaría ya no aprueba, solo descarta por causal formal; aprobar, rechazar y descartar avisan al residente por la aplicación y por correo; las rutas están en la prueba del intruso; y gestión entra por la pestaña Reservas del dashboard. La campana al liberarse la franja la subió Camilo el 12/10 | **Contra sus cinco criterios de Notion (13/10): se cumplen los cinco.** Fuera quedan el hilo de mensajes y las condiciones congeladas y versionadas (HU-15). Sin commit, y falta `migrate` de `reservas/0006`. En Notion sigue «En progreso» |
| HU-16 | Agente, 10/10. Es el pago del **alquiler de una reserva**, declarado por Administración (`reserva.declarar_pago`); el pago de administración es HU-35. Declarar guarda quién y cuándo, con auditoría. El comprobante es opcional (PDF, JPG o PNG de hasta 5 MB, validado por su firma, dentro de la base) y solo se sirve por una ruta validada. El residente puede subir el suyo sin declarar nada. Administración puede retirar una declaración con motivo | En Notion: «En revisión», 4 de 5 tareas. La de «almacenamiento fuera de la base» contradice lo construido. Sus tareas se compararon con el código; sus criterios, no |

Del ciclo de la reserva falta la cancelación en firme (HU-17).

### Sprint 5

| HU | Qué hay | Qué le falta |
|---|---|---|
| HU-21 | Construida el 22/09 con 8 acentos y logo; ampliada el 29/09 con color propio en hex y foto cuadrada 1:1. Revierte «solo 8 acentos, sin hex libre» | El texto de diseño (maestro §6.3) todavía no lo recoge. En Notion figura «Finalizado» sin la DoD |
| HU-25 | Construida el 22/09 con lo mínimo del canal de notificaciones (bandeja y correo). Desde el 05/10, hasta 4 fotos por anuncio | La prueba manual del plan de fotos. En Notion figura «Finalizado» sin la DoD |
| HU-27 | Camilo, 01/10: registra el ingreso y lista los visitantes. Agente, 10/10: capa de servicio, auditoría y **salida**. Quien solo registra ve los de hoy y los que siguen adentro; con `visitante.ver_historico`, todo | Sin la Ley 1581 (finalidad, autorización y retención), sin el aviso al apartamento y sin bicicleta sin placa. **Contra sus cinco criterios de Notion (11/10):** tres se cumplen, uno es parcial (el vigilante del ingreso queda en la auditoría, no en el listado) y uno no (el tipo de vehículo no es obligatorio). En Notion: «En progreso» |
| HU-28 | Agente, 10/10: catálogo de parqueaderos con código (`parqueadero.gestionar`), el vigilante elige uno de los libres al registrar una visita con vehículo, la salida lo libera, y diez registros simultáneos sobre un puesto dejan a una sola visita con él | En Notion: «En revisión», 5 de 5 tareas |
| HU-29 | Camilo, 12/10: crear un caso con foto opcional, la lista, y que la Secretaría rechace o redirija. Agente, 13/10: el ciclo completo (Por revisar, En revisión, Redirigido, Resuelto, Rechazado; Citado existe y nada lo produce), prioridad con justificación obligatoria para Urgente, respuesta escrita obligatoria que también exige la base, aviso al residente en cada cambio, auditoría, el detalle con las acciones de cada rol y la pestaña Casos del dashboard. Administración atiende un caso sin que nadie se lo redirija | **Contra sus cinco criterios de Notion (13/10):** cuatro se cumplen; el de la infracción que nace de un caso depende de HU-30. El caso no guarda la vivienda: se deduce de dónde reside quien lo abrió. Sin commit, y falta `migrate` de `casos/0004`. En Notion: «En progreso», y la tarea «Tablero de tres columnas» ya no describe lo construido |

### Sprints 6 y 7

| HU | Qué hay | Qué le falta |
|---|---|---|
| HU-33 | Solo el reglamento del conjunto en PDF (06/10), que es lo que exige HU-03 | Otros documentos, las actas y que el residente lo descargue. **Contra sus cinco criterios de Notion (11/10):** uno se cumple (rechaza por su firma un archivo que no es PDF), uno es parcial (subir otro no borra el anterior, pero no hay vista de versiones) y tres no (`documento.descargar` es de Administración, no hay actas ni manual, y la descarga no se audita). En Notion: «En progreso» |
| HU-35 | Agente, 10/10: el residente sube el comprobante de un mes de su vivienda; Administración confirma con un check por vivienda y mes (Secretaría ve y busca); el buscador filtra en el servidor y ninguna fila trae la cédula; el pago confirmado alimenta la mora de *paz y salvo* con el *día límite de pago* | La mora se construyó **sin haber verificado lo legal** ([abiertas](../06_Decisiones/abiertas.md) 12.10 b). En Notion: «En revisión», 4 de 5 tareas; la de «almacenamiento fuera de la base» contradice lo construido |

### HU-39, definida el 2026-10-06

*Como Administración, quiero describir cómo está organizado mi conjunto y que el sistema cree sus viviendas, para empezar a usar la plataforma sin registrarlas una por una.* Sale de la retroalimentación del docente sobre HU-03 y HU-08; lo decidido está en [construccion](../06_Decisiones/construccion.md). Desde el 11/10 está en Notion («En progreso»); sprint, puntos y prioridad los pone el equipo.

| # | Criterio | Estado |
|---|---|---|
| 1 | El asistente tiene un paso «Viviendas» que pregunta: apartamentos, casas o las dos cosas; si se agrupan y con qué palabra (torre, bloque, manzana, otra, o no se agrupan); cómo se identifican las agrupaciones (números, letras o nombres propios); cuántas viviendas tiene cada una, iguales o distintas; y cómo se numeran | Construido |
| 2 | Antes de crear, el sistema muestra la vista previa: cuántas viviendas, en qué agrupaciones y con qué nombres. Nada se guarda sin confirmar | Construido |
| 3 | Las viviendas se crean todas o ninguna, con el nombre armado con las palabras del conjunto. Las que ya existen se omiten y se informa cuántas | Construido |
| 4 | Un conjunto mixto registra apartamentos y casas, cada grupo con su agrupación | Construido |
| 5 | Un conjunto sin viviendas no puede quedar operativo | Construido |
| 6 | Después de creado, se pueden agregar agrupaciones y viviendas (ampliaciones), con el generador o a mano | El generador, construido; a mano con agrupación, falta |
| 7 | Las pantallas usan las palabras del conjunto: Apartamentos, Casas o Viviendas, y Torre, Manzana… «Apartamento» está fijo en unas 70 menciones de 12 plantillas (contadas el 06/10) | Falta |
| 8 | Retirar una vivienda o una agrupación pide siempre confirmación. Es baja lógica y una por una; no hay borrado | Falta |
| 9 | Aislamiento por conjunto y registro en la auditoría, como toda pieza nueva | Construido |

La segunda parte (criterios 7 y 8, y registrar a mano dentro de una agrupación) no tiene plan.

### HU-40

Solo existe en Notion: se creó el 07/10 como «HU 39 - Implementar accesibilidad» y se renumeró a HU-40 el 11/10, porque HU-39 ya era la de viviendas. Sin estado, puntos, criterios, código ni plan.

## Ver también

- [estado_actual](estado_actual.md) — el resumen y el reparto por sprint
- [pendientes](pendientes.md) — lo que falta para que cuenten SP
- [historias_evidencia](historias_evidencia.md) — tarea por tarea y criterio por criterio de HU-01 a HU-13 y HU-26
- [mapa_codigo](../02_Arquitectura/mapa_codigo.md) — de la historia a la app del código
- [planes](../07_Planes/planes.md) — los planes con que se construyeron
