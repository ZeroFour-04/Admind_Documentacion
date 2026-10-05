---
resumen: "Las 38 historias de usuario: sprint previsto, story points y avance de cada una, con lo que le falta a las construidas."
tipo: estado
corte: 2026-09-29
origen: "avance §5.2 (2026-09-27) actualizado con el informe por sprints del 2026-09-29 y la guía de estructura del 2026-09-30"
actualizado: 2026-10-05
---

# Historias de usuario

Títulos, story points y sprint previsto salen de Notion (`Gestión Scrum — AdMind` → `Historias de Usuario`). Aquí va el avance verificado en el código.

**Construida** = el código y sus pruebas existen, pero falta la parte humana de la DoD. Para cómo se reportan al docente, ver [estado_actual](estado_actual.md).

## Por sprint (corte 2026-09-29)

La columna "Sprint" es el reparto previsto en el Excel V11.1, que ya no se cumple con el plazo de un mes.

|Sprint|Historias|SP|Construido (sin DoD)|Sin empezar|
|---|---|---|---|---|
|**1**|HU-01 a HU-05, HU-26|25|6 de 6 (HU-03 parcial)|—|
|**2**|HU-06 a HU-09|20|4 de 4|—|
|**3**|HU-10 a HU-13|26|4 de 4|—|
|**4**|HU-14 a HU-19|28|0|6|
|**5**|HU-20, 21, 25, 27, 28, 29|28|2 (HU-21, HU-25, 10 SP)|4|
|**6**|HU-22 a 24, HU-30 a 34|38|0|8|
|**7**|HU-35, 36, 37|16|0|3|
|Condicional|HU-38|7|0|1|
|**Total**|**38**|**188**|**16 (81 SP)**|**22 (107 SP)**|

## Todas las historias

| HU | Historia | Sprint | SP | Prioridad | Avance |
|---|---|---|---|---|---|
| HU-01 | Inicio de sesión con correo y contraseña | 1 | 3 | Alta | **Construida** (5/5 tareas y criterios, con recuperación de contraseña; falta la DoD) |
| HU-02 | Segundo factor (TOTP) para permisos sensibles | 1 | 5 | Alta | **Construida** (5/5; TOTP con QR y códigos de respaldo; falta la DoD) |
| HU-03 | Asistente por pasos para crear un conjunto | 1 | 6 | Alta | **Parcial**: los pasos de Áreas y Reglas son reales desde el 27/09; bloqueada por el reglamento (HU-33) |
| HU-04 | Persona global única por documento | 1 | 3 | Alta | **Construida** (5/5, falta la DoD) |
| HU-05 | Aislamiento de datos entre conjuntos | 1 | 2 | Alta | **Construida** (5/5, falta la DoD) |
| HU-26 | Selector de conjunto activo | 1 | 6 | Alta | **Construida** (5/5, conectada a la API; falta la DoD) |
| HU-06 | Asignación de roles del catálogo fijo | 2 | 6 | Alta | **Construida** (criterios en código, falta la DoD). Desde el 29/09, un solo rol por conjunto |
| HU-07 | Vincular persona existente por búsqueda de documento | 2 | 3 | Alta | **Construida** (criterios en código, falta la DoD) |
| HU-08 | Vínculos de unidad y enrutamiento de notificaciones | 2 | 7 | Alta | **Construida** (criterios en código, falta la DoD) |
| HU-09 | Catálogo de áreas comunes del conjunto | 2 | 4 | Alta | **Construida** (criterios en código, falta la DoD) |
| HU-10 | Configuración de reglas beta de reserva | 3 | 9 | Alta | **Construida** (criterios en código, falta la DoD) |
| HU-11 | Bloqueo exclusivo de 3 minutos sobre una franja | 3 | 7 | Alta | **Construida** (criterios en código, falta la DoD) |
| HU-12 | Confirmación de contenido antes de enviar | 3 | 2 | Alta | **Construida** (criterios en código, falta la DoD) |
| HU-13 | Envío de solicitud y motor de reglas alfa/beta | 3 | 8 | Alta | **Construida** (criterios en código, falta la DoD) |
| HU-14 | Bandeja del administrador: aprobar o rechazar | 4 | 8 | Alta | Sin empezar |
| HU-15 | Condiciones del alquiler congeladas y versionadas | 4 | 4 | Alta | Sin empezar |
| HU-16 | Registro de pago declarado y comprobante | 4 | 4 | Media | Sin empezar |
| HU-17 | Cancelación de reservas en firme | 4 | 3 | Media | Sin empezar |
| HU-18 | Aviso de disponibilidad de franja (campana) | 4 | 6 | Media | Sin empezar |
| HU-19 | Dos oportunidades por franja y aviso de última | 4 | 3 | Media | Sin empezar |
| HU-20 | Anulación de registros por el Superusuario | 5 | 5 | Media | Sin empezar |
| HU-21 | Identidad visual del conjunto: color y logo | 5 | 4 | Baja | **Construida** el 22/09 y ampliada el 29/09 con color propio y foto 1:1 (falta la DoD) |
| HU-25 | Anuncios con alcance de conjunto o vivienda | 5 | 6 | Media | **Construida** el 22/09, con lo mínimo del canal de notificaciones (falta la DoD) |
| HU-27 | Registro de visitantes y vehículos | 5 | 5 | Media | Sin empezar |
| HU-28 | Parqueadero de visitantes atado a la visita | 5 | 3 | Media | Sin empezar |
| HU-29 | Tablero de casos con respuesta obligatoria | 5 | 5 | Media | Sin empezar |
| HU-22 | Bandeja de triage de la Secretaría | 6 | 7 | Media | Sin empezar |
| HU-23 | Prioridad sobre citas y casos | 6 | 5 | Media | Sin empezar |
| HU-24 | Rechazo por causal formal de la Secretaría | 6 | 3 | Media | Sin empezar |
| HU-30 | Registro y comunicación de infracciones | 6 | 4 | Media | Sin empezar |
| HU-31 | Agendar cita dentro del horario de atención | 6 | 4 | Media | Sin empezar |
| HU-32 | Cambio de horario con alternativas a los afectados | 6 | 8 | Media | Sin empezar |
| HU-33 | Repositorio de documentos vigentes | 6 | 3 | Media | Sin empezar |
| HU-34 | Asignación de parqueaderos de residentes | 6 | 4 | Media | Sin empezar |
| HU-35 | Reporte de pago de administración | 7 | 4 | Baja | Sin empezar |
| HU-36 | Importación masiva con dry-run e idempotencia | 7 | 7 | Baja | Sin empezar |
| HU-37 | Respaldo de información por conjunto | 7 | 5 | Baja | Sin empezar |
| HU-38 | Registro de actividades sobre la auditoría | Condicional | 7 | Baja | Sin empezar |

## Detalle de las construidas (corte 2026-09-29)

### Sprint 1: todo construido entre el 15/09 y el 21/09 (commits "sprint 1 terminado", `eab833e` y `c796773`)

|HU|SP|Estado|Qué le falta|
|---|---|---|---|
|HU-01 Login con correo y contraseña|3|5/5 tareas y 5/5 criterios. Incluye la recuperación de contraseña por enlace de un solo uso|La DoD. Además queda un hueco: `send_mail` es síncrono y sin `try` (con SMTP real, un fallo da 500 solo si la cuenta existe). El límite de 3 enlaces por hora y el SMTP real quedaron hechos el 2026-10-05|
|HU-02 Segundo factor (TOTP)|5|5/5 y 5/5. TOTP con QR y 10 códigos de respaldo|La DoD|
|HU-03 Asistente para crear un conjunto|6|Parcial. Desde el 27/09 los pasos de Áreas y Reglas son reales|**Está bloqueada**: el reglamento no tiene módulo (HU-33) y cuenta como no cumplido, así que **ningún conjunto puede quedar operativo**. Tampoco verifiqué si registra en la auditoría quién creó el conjunto|
|HU-04 Persona única por documento|3|5/5 y 5/5|La DoD|
|HU-05 Aislamiento entre conjuntos|2|5/5 y 5/5. Desde el 27/09 ya lo usan tablas reales (áreas, reservas y demás)|La DoD|
|HU-26 Selector de conjunto activo|6|5/5 y 5/5, conectado a la API|La DoD|

### Sprints 2 y 3: construidos el 27/09 con el plan F0–F10 (15 commits en el backend y 9 en el front)

Cada criterio de aceptación tiene una prueba automática con nombre propio.

|HU|SP|Estado|Observaciones|
|---|---|---|---|
|HU-06 Asignar y retirar roles|6|Todos los criterios con prueba|"Nunca cero Administración" responde 409 y hay una prueba con dos hilos a la vez|
|HU-07 Vincular persona por documento|3|Todos los criterios con prueba|Máximo 20 búsquedas por hora, contadas **por conjunto** (falta decidir si el límite debe ser global)|
|HU-08 Unidades y vínculos|7|Todos los criterios con prueba|Solo se vincula a quien ya tiene un rol en el conjunto|
|HU-09 Áreas comunes|4|Todos los criterios con prueba|Franjas por bloques fijos (D1 a)|
|HU-10 Reglas beta|9|Todos los criterios con prueba|7 tipos de regla que solo restringen, con versionado|
|HU-11 Bloqueo de 3 minutos|7|Todos los criterios con prueba, incluida la de concurrencia con 10 hilos|Falta probar a mano el `sendBeacon` que libera el bloqueo al cerrar la pestaña|
|HU-12 Confirmación antes de enviar|2|3 de 5 criterios con prueba automática|"Corregir sin perder lo escrito" y "el reloj no se detiene" necesitan prueba manual. La alta demanda depende de PB-24, que no existe|
|HU-13 Envío y motor de reglas|8|Todos los criterios con prueba|La mora siempre da `False` hasta que exista HU-35 (D5 b). Las alfas de piscina y de cobro quedan fuera|

### Adelantadas del Sprint 5

| HU                           | SP  | Estado                                                                                                                                                                                                                                                       |
| ---------------------------- | --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| HU-21 Identidad del conjunto | 4   | Construida el 22/09 (8 acentos y logo). **Hoy se amplió** con color propio en hex y foto cuadrada 1:1, commiteado y subido (`f053d31` y `96a30b4`). Esto **revierte** la decisión de "solo 8 acentos, sin hex libre", y el maestro §6.3 todavía no lo recoge |
| HU-25 Anuncios               | 6   | Construida el 22/09, con lo mínimo del canal de notificaciones (bandeja y correo) y de HU-08                                                                                                                                                                 |

### Sin empezar

- **Sprint 4:** HU-14 a HU-19.
- **Sprint 5:** HU-20, HU-27, HU-28 y HU-29.
- **Sprints 6 y 7:** todas.
- **Condicional:** HU-38.

**HU-14 (aprobar o rechazar, 8 SP)** es la que cierra el ciclo de la reserva: hoy una solicitud llega a `APARTADA` y ahí se queda.

## Ver también

- [historias_evidencia](historias_evidencia.md) — tarea por tarea y criterio por criterio, con el commit de cada una
- [pendientes](pendientes.md) — lo que falta para que cuenten SP
