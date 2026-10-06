---
resumen: "Las 38 historias de usuario y HU-39 (nueva, 2026-10-06): sprint previsto, story points y avance de cada una, con lo que le falta a las construidas."
tipo: estado
corte: 2026-09-29
origen: "avance §5.2 (2026-09-27) actualizado con el informe por sprints del 2026-09-29 y la guía de estructura del 2026-09-30"
actualizado: 2026-10-06
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
|**5**|HU-20, 21, 25, 27, 28, 29|28|2 (HU-21, HU-25, 10 SP) y HU-27 parcial|3|
|**6**|HU-22 a 24, HU-30 a 34|38|0|8|
|**7**|HU-35, 36, 37|16|0|3|
|Condicional|HU-38|7|0|1|
|**Total**|**38**|**188**|**16 (81 SP)** y HU-27 parcial (5 SP)|**21 (102 SP)**|

*Actualización del 2026-10-05:* HU-27 pasó de sin empezar a parcial con el commit de Camilo. Lo demás sigue como el 29/09.

*Actualización del 2026-10-06 (corte del informe 4):* **HU-14 está construida** (8 SP, Sprint 4), así que la tabla de arriba queda corta: son 17 historias construidas (89 SP), HU-27 y HU-33 parciales (8 SP) y 19 sin empezar (91 SP). Todo lo que las filas de abajo marcan como «sin commit» **ya tiene commit y está subido** (Backend hasta `279e963`, Frontend hasta `fff4651`), y sus migraciones están aplicadas en `admind_db`.

## Todas las historias

| HU | Historia | Sprint | SP | Prioridad | Avance |
|---|---|---|---|---|---|
| HU-01 | Inicio de sesión con correo y contraseña | 1 | 3 | Alta | **Construida** (5/5 tareas y criterios, con recuperación de contraseña; falta la DoD) |
| HU-02 | Segundo factor (TOTP) para permisos sensibles | 1 | 5 | Alta | **Construida** (5/5; TOTP con QR, códigos de respaldo y, desde el 05/10, enlace por correo para quitarlo si se pierde la aplicación; falta la DoD) |
| HU-03 | Asistente por pasos para crear un conjunto | 1 | 6 | Alta | **Construida completa el 06/10, sin commit**: siete pasos (datos, viviendas, administración, áreas, reglas, reglamento y resumen) y seis requisitos; un conjunto ya puede quedar operativo y lo activa el Superusuario o Administración. Falta la parte humana de la DoD. Sus criterios en Notion describen el asistente anterior. Tres planes: [planes](../07_Planes/planes.md) |
| HU-04 | Persona global única por documento | 1 | 3 | Alta | **Construida** (5/5, falta la DoD) |
| HU-05 | Aislamiento de datos entre conjuntos | 1 | 2 | Alta | **Construida** (5/5, falta la DoD) |
| HU-26 | Selector de conjunto activo | 1 | 6 | Alta | **Construida** (5/5, conectada a la API; falta la DoD) |
| HU-06 | Asignación de roles del catálogo fijo | 2 | 6 | Alta | **Construida** (criterios en código, falta la DoD). Desde el 29/09, un solo rol por conjunto |
| HU-07 | Vincular persona existente por búsqueda de documento | 2 | 3 | Alta | **Construida** (criterios en código, falta la DoD) |
| HU-08 | Vínculos de unidad y enrutamiento de notificaciones | 2 | 7 | Alta | **Construida** (criterios en código, falta la DoD) |
| HU-09 | Catálogo de áreas comunes del conjunto | 2 | 4 | Alta | **Construida** (criterios en código, falta la DoD). Desde el 06/10 cada área lleva **aforo máximo obligatorio** (sin commit). El modo de uso de la zona sigue sin construir |
| HU-10 | Configuración de reglas beta de reserva | 3 | 9 | Alta | **Construida** (criterios en código, falta la DoD). El 06/10 se redefinió y se **reconstruyó por niveles**, sin commit: reglas del conjunto y del área, una sola por tipo, con descripción fija y días que no abre con motivo ([motor_reglas](../05_Modulos/motor_reglas.md)). Sus criterios en Notion describen el modelo anterior |
| HU-11 | Bloqueo exclusivo de 3 minutos sobre una franja | 3 | 7 | Alta | **Construida** (criterios en código, falta la DoD) |
| HU-12 | Confirmación de contenido antes de enviar | 3 | 2 | Alta | **Construida** (criterios en código, falta la DoD) |
| HU-13 | Envío de solicitud y motor de reglas alfa/beta | 3 | 8 | Alta | **Construida** (criterios en código, falta la DoD). Desde el 06/10 el evaluador junta reglas del sistema, aforo del área, reglas del conjunto y reglas del área (sin commit) |
| HU-14 | Bandeja del administrador: aprobar o rechazar | 4 | 8 | Alta | **Construida** el 05/10 por Camilo (Backend `2d11dbe`, Frontend `d76ac0f` y `fff4651`): solicitudes por área y bandeja del conjunto, aceptar o rechazar con motivo obligatorio, auditoría y 409 si ya se decidió; Administración, Secretaría y Superusuario. Falta la DoD, el aviso al residente al decidir, la causal de lista cerrada, las condiciones del alquiler (HU-15) y registrar sus tres rutas en la prueba del intruso. No se comparó contra sus criterios de Notion |
| HU-15 | Condiciones del alquiler congeladas y versionadas | 4 | 4 | Alta | Sin empezar |
| HU-16 | Registro de pago declarado y comprobante | 4 | 4 | Media | Sin empezar |
| HU-17 | Cancelación de reservas en firme | 4 | 3 | Media | Sin empezar |
| HU-18 | Aviso de disponibilidad de franja (campana) | 4 | 6 | Media | Sin empezar |
| HU-19 | Dos oportunidades por franja y aviso de última | 4 | 3 | Media | Sin empezar |
| HU-20 | Anulación de registros por el Superusuario | 5 | 5 | Media | Sin empezar |
| HU-21 | Identidad visual del conjunto: color y logo | 5 | 4 | Baja | **Construida** el 22/09 y ampliada el 29/09 con color propio y foto 1:1 (falta la DoD) |
| HU-25 | Anuncios con alcance de conjunto o vivienda | 5 | 6 | Media | **Construida** el 22/09, con lo mínimo del canal de notificaciones (falta la DoD). El 05/10 se amplió: hasta 4 fotos por anuncio, sin commit |
| HU-27 | Registro de visitantes y vehículos | 5 | 5 | Media | **Parcial** desde el 01/10 (Camilo): registra el ingreso y lista los visitantes; sin salida |
| HU-28 | Parqueadero de visitantes atado a la visita | 5 | 3 | Media | Sin empezar |
| HU-29 | Tablero de casos con respuesta obligatoria | 5 | 5 | Media | Sin empezar |
| HU-22 | Bandeja de triage de la Secretaría | 6 | 7 | Media | Sin empezar |
| HU-23 | Prioridad sobre citas y casos | 6 | 5 | Media | Sin empezar |
| HU-24 | Rechazo por causal formal de la Secretaría | 6 | 3 | Media | Sin empezar |
| HU-30 | Registro y comunicación de infracciones | 6 | 4 | Media | Sin empezar |
| HU-31 | Agendar cita dentro del horario de atención | 6 | 4 | Media | Sin empezar |
| HU-32 | Cambio de horario con alternativas a los afectados | 6 | 8 | Media | Sin empezar |
| HU-33 | Repositorio de documentos vigentes | 6 | 3 | Media | **Parcial** (06/10, sin commit): solo el reglamento del conjunto en PDF, que es lo que exige HU-03. Falta el resto: otros documentos, las actas y que el residente lo descargue |
| HU-34 | Asignación de parqueaderos de residentes | 6 | 4 | Media | Sin empezar |
| HU-35 | Reporte de pago de administración | 7 | 4 | Baja | Sin empezar |
| HU-36 | Importación masiva con dry-run e idempotencia | 7 | 7 | Baja | Sin empezar |
| HU-37 | Respaldo de información por conjunto | 7 | 5 | Baja | Sin empezar |
| HU-38 | Registro de actividades sobre la auditoría | Condicional | 7 | Baja | Sin empezar |
| HU-39 | Estructura de viviendas del conjunto: agrupaciones y generación en lote | Por definir | Por estimar | Por definir | **Primera parte construida el 06/10, sin commit** (criterios 1 a 5 y 9, y el generador del 6). Falta la segunda parte (criterios 7 y 8, y registrar a mano dentro de una agrupación). Historia nueva tras la retroalimentación del docente; **no está en Notion**. [Plan_Estructura_De_Viviendas](../07_Planes/activos/Plan_Estructura_De_Viviendas.md) |

## Detalle de las construidas (corte 2026-09-29)

### Sprint 1: todo construido entre el 15/09 y el 21/09 (commits "sprint 1 terminado", `eab833e` y `c796773`)

|HU|SP|Estado|Qué le falta|
|---|---|---|---|
|HU-01 Login con correo y contraseña|3|5/5 tareas y 5/5 criterios. Incluye la recuperación de contraseña por enlace de un solo uso|La DoD. Además queda un hueco: `send_mail` es síncrono y sin `try` (con SMTP real, un fallo da 500 solo si la cuenta existe). El límite de 3 enlaces por hora y el SMTP real quedaron hechos el 2026-10-05|
|HU-02 Segundo factor (TOTP)|5|5/5 y 5/5. TOTP con QR y 10 códigos de respaldo. Desde el 2026-10-05, enlace por correo para quitarlo y configurarlo de nuevo (sin commit)|La DoD, y recorrer el enlace a mano con la API encendida y un correo real|
|HU-03 Asistente para crear un conjunto|6|Completa en código desde el 06/10 (sin commit): siete pasos, con Viviendas y Reglamento, y un conjunto que ya queda operativo|La parte humana de la DoD y actualizar sus criterios en Notion. Dejar operativo un conjunto **no queda en la auditoría**, y sigue sin verificarse si queda quién lo creó. Reservar todavía no exige que el conjunto esté operativo|
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
|HU-09 Áreas comunes|4|Todos los criterios con prueba|Franjas por bloques fijos (D1 a). Aforo máximo obligatorio desde el 06/10|
|HU-10 Reglas beta|9|Todos los criterios con prueba|Desde el 06/10: 5 tipos vigentes en dos niveles (3 del conjunto y 2 del área), una sola abierta por tipo, con versionado; 3 tipos retirados quedan para el historial|
|HU-11 Bloqueo de 3 minutos|7|Todos los criterios con prueba, incluida la de concurrencia con 10 hilos|Falta probar a mano el `sendBeacon` que libera el bloqueo al cerrar la pestaña|
|HU-12 Confirmación antes de enviar|2|3 de 5 criterios con prueba automática|"Corregir sin perder lo escrito" y "el reloj no se detiene" necesitan prueba manual. La alta demanda depende de PB-24, que no existe|
|HU-13 Envío y motor de reglas|8|Todos los criterios con prueba|La mora siempre da `False` hasta que exista HU-35 (D5 b). Las reglas de piscina y de cobro quedan fuera|

### Adelantadas del Sprint 5

| HU                           | SP  | Estado                                                                                                                                                                                                                                                       |
| ---------------------------- | --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| HU-21 Identidad del conjunto | 4   | Construida el 22/09 (8 acentos y logo). **Hoy se amplió** con color propio en hex y foto cuadrada 1:1, commiteado y subido (`f053d31` y `96a30b4`). Esto **revierte** la decisión de "solo 8 acentos, sin hex libre", y el maestro §6.3 todavía no lo recoge |
| HU-25 Anuncios               | 6   | Construida el 22/09, con lo mínimo del canal de notificaciones (bandeja y correo) y de HU-08. El 05/10 se amplió con hasta 4 fotos por anuncio (sin commit)                                                                                                                                                                 |

### HU-27, parcial (Camilo, commits del 2026-10-01)

Verificado en el código el 2026-10-05. No se comparó contra los criterios de Notion.

| Qué hay | Qué no hay |
|---|---|
| `Visitante`: nombre, cédula, placa y tipo de vehículo (opcionales), apartamento visitado y hora de entrada, que pone el servidor | Registro de la **salida** |
| `POST /visitantes/`: solo el rol Vigilancia, con `visitante.registrar` | Finalidad declarada, autorización y plazo de retención (Ley 1581, R2), que pide el README de la app |
| `GET /visitantes/`: los de hoy para quien solo registra; todo el histórico con `visitante.ver_historico` | Parqueadero de visitantes (HU-28) y aviso a quienes residen en el apartamento |
| Pantalla con el formulario (Vigilancia) y el listado; 6 pruebas en el back, 7 en el front y su listado en la prueba del intruso | Capa de servicio y registro en la auditoría: la vista usa el ORM directo |

### HU-39, definida el 2026-10-06; primera parte construida ese día

*Como Administración, quiero describir cómo está organizado mi conjunto y que el sistema cree sus viviendas, para empezar a usar la plataforma sin registrarlas una por una.* Sale de la retroalimentación del docente sobre HU-03 y HU-08; lo decidido está en [construccion](../06_Decisiones/construccion.md). Sprint, puntos y prioridad los pone el equipo en Notion.

| # | Criterio | Plan |
|---|---|---|
| 1 | El asistente tiene un paso «Viviendas» que pregunta: apartamentos, casas o las dos cosas; si se agrupan y con qué palabra (torre, bloque, manzana, otra, o no se agrupan); cómo se identifican las agrupaciones (números, letras o nombres propios); cuántas viviendas tiene cada una, iguales o distintas; y cómo se numeran | Primera parte |
| 2 | Antes de crear, el sistema muestra la vista previa: cuántas viviendas, en qué agrupaciones y con qué nombres. Nada se guarda sin confirmar | Primera parte |
| 3 | Las viviendas se crean todas o ninguna, con el nombre armado con las palabras del conjunto. Las que ya existen se omiten y se informa cuántas | Primera parte |
| 4 | Un conjunto mixto registra apartamentos y casas, cada grupo con su agrupación | Primera parte |
| 5 | Un conjunto sin viviendas no puede quedar operativo | Primera parte |
| 6 | Después de creado, se pueden agregar agrupaciones y viviendas (ampliaciones), con el generador o a mano | El generador, en la primera parte; a mano con agrupación, en la segunda |
| 7 | Las pantallas usan las palabras del conjunto: Apartamentos, Casas o Viviendas, y Torre, Manzana… Hoy «Apartamento» está fijo en unas 70 menciones de 12 plantillas | Segunda parte |
| 8 | Retirar una vivienda o una agrupación pide siempre confirmación. Es baja lógica y una por una; no hay borrado | Segunda parte |
| 9 | Aislamiento por conjunto y registro en la auditoría, como toda pieza nueva | Primera parte |

### Sin empezar

- **Sprint 4:** HU-15 a HU-19.
- **Sprint 5:** HU-20, HU-28 y HU-29.
- **Sprints 6 y 7:** todas.
- **Condicional:** HU-38.

**HU-14 (aprobar o rechazar, 8 SP)** ya está construida (05/10): una solicitud `APARTADA` pasa a `RESERVADA` o `RECHAZADA`. Del ciclo de la reserva falta la cancelación en firme (HU-17).

## Ver también

- [historias_evidencia](historias_evidencia.md) — tarea por tarea y criterio por criterio, con el commit de cada una
- [pendientes](pendientes.md) — lo que falta para que cuenten SP
