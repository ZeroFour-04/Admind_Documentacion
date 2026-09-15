---
titulo: "AdMind — Avance del proyecto"
proyecto: "Proyecto de Ingeniería de Software II — Universidad de Cundinamarca, Facatativá"
creado: 2026-09-14
actualizado: "2026-09-15 05:45 (hora de Colombia)"
proposito: "Cómo va el desarrollo: qué existe en el código, cómo avanza cada historia de usuario y qué se decidió al construir. Se actualiza al cerrar cada sesión de trabajo."
---

# AdMind — Avance del proyecto

> [!IMPORTANT] Qué es este archivo y qué no
> - **Registra lo que ya pasó en el código**: commits, historias en curso, decisiones tomadas al construir y lo que frena el avance.
> - **No explica el producto ni el diseño.** Eso vive en `Admin_Master.md`, que manda si hay contradicción.
> - **No es el seguimiento del lab.** Los ejercicios de práctica van en `Admind_Seguimiento_Lab.md`.
> - **Títulos, story points y sprint previsto de cada historia salen de Notion** (`Gestión Scrum — AdMind` → `Historias de Usuario`). Aquí se registra el avance técnico verificado en el repositorio.
> - Cómo actualizarlo: §7.

---

## 1. Resumen al corte

**Corte: 2026-09-15, 05:45.** Segundo día de desarrollo real dentro del plazo de un mes (entrega cerca del 2026-10-14, fecha exacta por confirmar; maestro §11).

| Frente | Estado |
|---|---|
| **Backend** | Django sobre PostgreSQL con `Persona`, `Usuario`, `Conjunto` y `Asignacion` migrados, el catálogo de roles y permisos en código y la base del aislamiento por conjunto. `desarrollo` al día con el remoto (último commit `531e854`) |
| **Frontend** | Solo estructura de carpetas con README (commit `764425c`, 2026-09-13). Sin código |
| **Historias** | **0 de 38 terminadas (0 de 188 SP).** Cinco en progreso: HU-04 (5 de 5 tareas, falta la DoD), HU-05 (2 de 5 y dos a medias), HU-06 (2 de 5 y una a medias), HU-03 (1 de 5) y HU-01 (1 de 5) |
| **Plan técnico del Sprint 1** | Pasos 1 a 4 de 8 hechos (§4). Sigue el paso 5: login, decidiendo entre token y sesión |
| **Sprint 1** | Sin iniciar formalmente. Qué entra en el mes y en cuántos sprints sigue abierto (maestro §12.8) |
| **Pruebas automáticas** | **37, todas pasan** (`pytest`, corrido el 2026-09-15 05:40) |

> [!NOTE] Por qué 0 SP con cinco historias avanzadas
> El método de velocidad acordado con el docente (maestro §11.3) solo cuenta lo terminado: una historia al 80 % aporta 0 SP.
> Los mensajes de commit dicen *"HU 04 completada"* (`dc6a414`) y *"[HU-03] [HU-05] [HU-06] hechos"* (`531e854`). **Ninguna cumple la DoD** (maestro §8.1): HU-04 tiene todas sus tareas, pero le falta un criterio que necesita la API, el PR `desarrollo → pruebas` y la prueba manual de quien no la programó; HU-03, HU-05 y HU-06 solo tienen la capa de datos. Detalle en §5.3.

---

## 2. Qué existe en el código

### 2.1 Repositorios

| Repositorio | Rama | Último commit | En el remoto |
|---|---|---|---|
| Backend | `desarrollo` | `531e854` — conjuntos, permisos y aislamiento (2026-09-15 00:54) | Sí |
| Frontend | `desarrollo` | `764425c` — estructura de carpetas (2026-09-13 01:01) | Sí |
| Documentación | `main` | `f1b0110` — `Admind_Guia_Desarrollo.md` (2026-09-15 00:30); esta actualización va en el commit siguiente | Sí |

### 2.2 Backend, pieza por pieza

| Pieza | Estado | Dónde |
|---|---|---|
| Django 5.2.17, Django REST Framework 3.18, psycopg 3.3 | Instalado | `requirements.txt` |
| Proyecto Django (`startproject config .`) | Hecho | `config/` |
| Clave secreta y conexión a la base por variables de entorno | Hecho | `config/settings.py` + `.env` (fuera del repositorio) |
| PostgreSQL 18 local, base `admind_db`, usuario `admind_user` | Hecho, en la máquina de Alejo | — |
| App `personas` con el modelo `Persona` | Hecho | `apps/personas/models.py` |
| App `cuentas` con el modelo `Usuario` y `AUTH_USER_MODEL` | Hecho | `apps/cuentas/models.py` |
| App `conjuntos` con el modelo `Conjunto` (UUID, `nombre`, `direccion`, `activo`, `operativo`) | Hecho. `operativo` nace en falso; sin campo de color | `apps/conjuntos/models.py` |
| Catálogo fijo en código: 6 roles, 46 permisos, 18 sensibles y el reparto por rol | Hecho. **El reparto por rol es provisional** | `apps/permisos/catalogo.py` |
| Modelo `Asignacion` (persona, rol, conjunto, vigencias) | Hecho | `apps/permisos/models.py` |
| Conjunto activo de la operación (`ContextVar`) y `usar_conjunto()` para fijarlo a mano | Hecho | `apps/comun/aislamiento/contexto.py` |
| Modelo base `ModeloDeConjunto` con `ManagerDeConjunto` (filtra toda consulta por el conjunto activo) | Hecho. **Ningún modelo del producto lo usa todavía** | `apps/comun/modelos_base/modelos.py`, `apps/comun/aislamiento/managers.py` |
| `fk_compuesta()`: FK `(x_id, conjunto_id)` escrita en la migración | Hecho. Probada solo con tablas de apoyo | `apps/comun/aislamiento/migraciones.py` |
| Migraciones `0001` de `personas`, `cuentas`, `conjuntos` y `permisos`, aplicadas en `admind_db` | Hecho | `apps/*/migrations/` |
| Pruebas con `pytest` y `pytest-django`: 37 (10 de personas, 2 de conjuntos, 15 de permisos, 7 de aislamiento, 3 de tablas globales) | Hecho, todas pasan. Corren con `config/settings_pruebas.py` | `pytest.ini`, `apps/*/tests.py`, `tests/` |
| `TIME_ZONE = 'America/Bogota'` | Hecho | `config/settings.py` |
| Plantilla de variables de entorno | Hecho | `.env _ejemplo` |
| Middleware que fija el conjunto activo desde la sesión | **No hay** | — |
| Endpoints de la API | **No hay** | — |
| Capa de servicios (flujo controlador → servicio → repositorio que pide el profesor) | **No hay** | — |
| Resto de apps (`unidades`, `areas`, `reservas`, …) | Solo carpeta con README | `apps/` |

### 2.3 Restricciones verificadas en PostgreSQL

Revisadas directamente en `admind_db`, no solo en el código de Python: las de `personas` y `cuentas` el 2026-09-14, las de `permisos` el 2026-09-15. La FK compuesta de HU-05 todavía no existe en `admind_db` porque ninguna tabla del producto la usa; se verifica en la base de pruebas (§5.3).

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

---

## 3. Bitácora

Lo más reciente abajo. Solo hechos; los errores con su aprendizaje van en `Admind_Bitacora_Errores.md`, que escribe Alejo.

| Fecha y hora | Dónde | Qué pasó |
|---|---|---|
| 2026-09-11 | Backend y frontend | Ramas `main`, `desarrollo` y `pruebas` creadas. La demo de septiembre se descarta (maestro §11) |
| 2026-09-13 01:00 | Backend | `91c561f` — estructura de carpetas con un README por carpeta |
| 2026-09-13 01:01 | Frontend | `764425c` — estructura de carpetas con un README por carpeta |
| 2026-09-14 | Equipo | El plazo de entrega se reduce a un mes; la IA pasa a construir a pedido (maestro §8.4) |
| 2026-09-14 19:24 | Backend | `8600244` — `.gitignore` en `desarrollo` |
| 2026-09-14 21:32 | Backend | `6021bb9` — proyecto Django creado y conectado a PostgreSQL |
| 2026-09-14 | Base de datos | Se corrió `migrate` antes de tener usuario propio; como no había datos, `admind_db` se borró y se volvió a crear antes del primer `migrate` real |
| 2026-09-14 22:31 | Documentación | `2813ee2` — lista de tipos de documento revisada en el maestro |
| 2026-09-14 | Backend | `apps/personas/models.py` se sobrescribió sin commit; se restauró desde la copia usada para verificarlo |
| 2026-09-14 23:37 | Backend | `962853f` — modelos `Persona` y `Usuario`, migraciones aplicadas y restricciones verificadas en PostgreSQL |
| 2026-09-14 23:45 | Documentación | Maestro §5.2 actualizado (datos de `Persona`, correo en `Usuario`) y creación de este archivo. Sin commit al corte |
| 2026-09-14 23:56 | Backend | `5505673` — plantilla `.env _ejemplo` con los nombres de las variables de entorno |
| 2026-09-14 23:56 | Documentación | `b08754f` — commit del maestro §5.2, este archivo y las guías de inicialización e instalación del backend |
| 2026-09-15 00:27 | Backend | `dc6a414` — `pytest-django`, `pytest.ini` y 10 pruebas de HU-04. Cierra su última tarea técnica. El mensaje dice "completada", pero la historia aún no cumple la DoD (§5.3) |
| 2026-09-15 00:30 | Documentación | `f1b0110` — `Admind_Guia_Desarrollo.md` |
| 2026-09-15 00:54 | Backend | `531e854` — apps `conjuntos` y `permisos`, base del aislamiento en `apps/comun/`, app de apoyo `tests/aislamiento/` y prueba transversal de tablas globales. 27 pruebas nuevas, 37 en total. Son los pasos 2, 3 y 4 del plan del Sprint 1 en un solo commit porque se construyeron entrelazados. El mensaje dice "[HU-03] [HU-05] [HU-06] hechos"; son avances parciales (§5.3) |
| 2026-09-15 | Backend | Commits `5505673`, `dc6a414` y `531e854` subidos a `origin/desarrollo`. Migraciones de `conjuntos` y `permisos` aplicadas en `admind_db` |
| 2026-09-15 05:45 | Documentación | Actualización de este archivo con los dos commits de la madrugada |

---

## 4. Decisiones tomadas al construir

Las que cambian el diseño quedan también en el maestro; las técnicas, solo aquí.

| Fecha | Decisión | Quién | Dónde quedó |
|---|---|---|---|
| 2026-09-14 | El esquema diseñado a mano en DBeaver (base `admind`) se usa **como plano**: las tablas las crean los modelos y migraciones de Django, no `inspectdb`. Así Camilo recrea la base con un `migrate`, y las FK compuestas y los privilegios viajan en las migraciones (maestro §7.1) | Alejo | Aquí |
| 2026-09-14 | La base de diseño (`admind`) no se toca; el desarrollo usa una base aparte, `admind_db` | Alejo | Aquí |
| 2026-09-14 | Tipos de documento: `CC`, `TI`, `CE`, `PAS`, `PPT`, con códigos sin puntos | Alejo | Maestro §5.2 |
| 2026-09-14 | `Persona` con `nombres`, `apellidos` y `telefono`; el correo vive solo en `Usuario` | Alejo | Maestro §5.2 |
| 2026-09-14 | Usuario propio desde el primer `migrate`, con inicio de sesión por correo (`AbstractBaseUser` + `PermissionsMixin`). `is_active` e `is_staff` se quedan en inglés porque Django los busca por ese nombre | Propuesta del agente, aplicada por Alejo | `apps/cuentas/models.py` |
| 2026-09-14 | Las restricciones de la base se declaran en el modelo (`Meta.constraints`) para que viajen en las migraciones; la normalización del documento y del correo ocurre en `save()` | Propuesta del agente, aplicada por Alejo | `apps/personas/models.py`, `apps/cuentas/models.py` |
| 2026-09-15 | Plan técnico del Sprint 1 en 8 pasos: 1 pruebas de HU-04 → 2 `conjuntos` y modelo base → 3 `permisos` (catálogo y `Asignacion`, adelantados de HU-06) → 4 HU-05 en la base → 5 login, decidiendo entre token y sesión → 6 HU-26 y middleware → 7 HU-03 mínima → 8 HU-02 | Propuesta del agente, aprobada por Alejo | Aquí |
| 2026-09-15 | **Roles y permisos viven en código**, sin tablas `rol` ni `permiso`. Resuelve el choque con el esquema de diseño a favor del maestro. Por eso el catálogo no necesita migración | Alejo | `apps/permisos/catalogo.py`; ya lo decía el maestro §5.3 |
| 2026-09-15 | **`Asignacion.conjunto` es nulo solo para el Superusuario**, forzado con un CHECK en la base. Resuelve el otro choque a favor del maestro | Alejo | `apps/permisos/models.py`; ya lo decía el maestro §5.3 |
| 2026-09-15 | Retirar un rol es cerrar su vigencia (`vigencia_hasta`), no borrar la fila. Solo puede haber una asignación vigente por persona, rol y conjunto | Agente, a pedido de Alejo | `apps/permisos/models.py` |
| 2026-09-15 | Aislamiento en tres capas: `ManagerDeConjunto` filtra toda consulta por el conjunto activo y **falla** si no hay uno; `ModeloDeConjunto.save()` toma el conjunto activo y rechaza escribir en otro; la base rechaza la fila cruzada con la FK compuesta, que se escribe con `fk_compuesta()` (`RunSQL`, `ON DELETE RESTRICT`) porque Django no la maneja | Agente, a pedido de Alejo | `apps/comun/` |
| 2026-09-15 | El conjunto activo se guarda en un `ContextVar`. En una petición lo fijará el middleware (pendiente); en pruebas y procesos de plataforma se fija con `usar_conjunto()` | Agente, a pedido de Alejo | `apps/comun/aislamiento/contexto.py` |
| 2026-09-15 | Las pruebas corren con `config/settings_pruebas.py`, que agrega la app de apoyo `tests.aislamiento` (modelos `Area` y `Reserva` que solo existen en la base de pruebas). Así HU-05 se prueba sin crear todavía las apps reales de áreas y reservas | Agente, a pedido de Alejo | `pytest.ini`, `tests/aislamiento/` |
| 2026-09-15 | Lista cerrada de tablas globales escrita en la prueba transversal. Además de lo que nombra el maestro §5.4 incluye `conjuntos_conjunto` y las dos tablas que crea `PermissionsMixin`, y admite `conjunto_id` nulo en `permisos_asignacion`. **Falta llevarlo al maestro** (§6) | Agente, a pedido de Alejo | `tests/esquema/test_tablas_globales.py` |
| 2026-09-15 | `TIME_ZONE` pasa de `UTC` a `America/Bogota` | Alejo | `config/settings.py` |
| 2026-09-15 | `Conjunto` se crea sin campo de color: se aplica la decisión de un solo acento por ahora (2026-09-11). El campo llega con HU-21 | Alejo | `apps/conjuntos/models.py` |

---

## 5. Historias de usuario

### 5.1 Por sprint previsto

Sprint previsto según Notion (reparto del Excel V11.1). Con el plazo de un mes este reparto ya no se cumple tal cual (maestro §12.8), pero se conserva como referencia.

| Sprint previsto | Historias | SP | Terminadas | En progreso |
|---|---|---|---|---|
| 1 | HU-01 a HU-05, HU-26 | 25 | 0 | 4 |
| 2 | HU-06 a HU-09 | 20 | 0 | 1 |
| 3 | HU-10 a HU-13 | 26 | 0 | 0 |
| 4 | HU-14 a HU-19 | 28 | 0 | 0 |
| 5 | HU-20, HU-21, HU-25, HU-27, HU-28, HU-29 | 28 | 0 | 0 |
| 6 | HU-22, HU-23, HU-24, HU-30 a HU-34 | 38 | 0 | 0 |
| 7 | HU-35, HU-36, HU-37 | 16 | 0 | 0 |
| Condicional | HU-38 | 7 | 0 | 0 |
| **Total** | **38** | **188** | **0** | **5** |

### 5.2 Todas las historias

Avance: **Sin empezar** · **En progreso** (con tareas técnicas hechas sobre el total de Notion) · **Terminada** (solo si cumple la DoD, maestro §8.1).

| HU | Historia | Sprint | SP | Prioridad | Avance |
|---|---|---|---|---|---|
| HU-01 | Inicio de sesión con correo y contraseña | 1 | 3 | Alta | **En progreso** (1/5) |
| HU-02 | Segundo factor (TOTP) para permisos sensibles | 1 | 5 | Alta | Sin empezar |
| HU-03 | Asistente por pasos para crear un conjunto | 1 | 6 | Alta | **En progreso** (1/5) |
| HU-04 | Persona global única por documento | 1 | 3 | Alta | **En progreso** (5/5, falta la DoD) |
| HU-05 | Aislamiento de datos entre conjuntos | 1 | 2 | Alta | **En progreso** (2/5, dos a medias) |
| HU-26 | Selector de conjunto activo | 1 | 6 | Alta | Sin empezar |
| HU-06 | Asignación de roles del catálogo fijo | 2 | 6 | Alta | **En progreso** (2/5, una a medias) |
| HU-07 | Vincular persona existente por búsqueda de documento | 2 | 3 | Alta | Sin empezar |
| HU-08 | Vínculos de unidad y enrutamiento de notificaciones | 2 | 7 | Alta | Sin empezar |
| HU-09 | Catálogo de áreas comunes del conjunto | 2 | 4 | Alta | Sin empezar |
| HU-10 | Configuración de reglas beta de reserva | 3 | 9 | Alta | Sin empezar |
| HU-11 | Bloqueo exclusivo de 3 minutos sobre una franja | 3 | 7 | Alta | Sin empezar |
| HU-12 | Confirmación de contenido antes de enviar | 3 | 2 | Alta | Sin empezar |
| HU-13 | Envío de solicitud y motor de reglas alfa/beta | 3 | 8 | Alta | Sin empezar |
| HU-14 | Bandeja del administrador: aprobar o rechazar | 4 | 8 | Alta | Sin empezar |
| HU-15 | Condiciones del alquiler congeladas y versionadas | 4 | 4 | Alta | Sin empezar |
| HU-16 | Registro de pago declarado y comprobante | 4 | 4 | Media | Sin empezar |
| HU-17 | Cancelación de reservas en firme | 4 | 3 | Media | Sin empezar |
| HU-18 | Aviso de disponibilidad de franja (campana) | 4 | 6 | Media | Sin empezar |
| HU-19 | Dos oportunidades por franja y aviso de última | 4 | 3 | Media | Sin empezar |
| HU-20 | Anulación de registros por el Superusuario | 5 | 5 | Media | Sin empezar |
| HU-21 | Identidad visual del conjunto: color y logo | 5 | 4 | Baja | Sin empezar |
| HU-25 | Anuncios con alcance de conjunto o vivienda | 5 | 6 | Media | Sin empezar |
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

### 5.3 Historias en progreso, en detalle

Las tareas y criterios de HU-03, HU-05 y HU-06 se tomaron de la copia local del Excel V11.1 (hoja `HU`).

#### HU-04 · Persona global única por documento — 5 de 5 tareas, falta la DoD

| Tarea técnica (Notion) | Estado | Evidencia |
|---|---|---|
| Modelo Persona con PK UUID y campos `tipo_documento` y `numero_documento` | Hecha | `apps/personas/models.py`, `962853f` |
| Restricción `UNIQUE (tipo_documento, numero_documento)` en base de datos | Hecha | `persona_documento_unico`, verificada en PostgreSQL |
| Catálogo cerrado de tipos de documento | Hecha, con la lista revisada | `TipoDocumento` + `persona_tipo_documento_valido`. Notion todavía dice `CC, CE, PA, PEP, TI` |
| Normalización del número al guardar | Hecha | `normalizar_documento()` en `save()` + `persona_documento_normalizado` |
| Pruebas: dos altas con el mismo documento producen una sola Persona | Hecha | `apps/personas/tests.py`, 10 pruebas, `dc6a414` |

| Criterio de aceptación | Estado |
|---|---|
| Un documento que ya existe no crea un segundo registro | Hecho y probado, también cuando el segundo se escribe con puntos |
| El mismo número con distinto tipo es otra persona | Hecho y probado |
| En la API o en una URL la persona se identifica por UUID, nunca por documento | La llave es UUID y hay prueba de eso; **no hay API todavía** |
| Un número escrito con puntos o espacios queda normalizado | Hecho y probado. La base además rechaza un número sin normalizar aunque se salte `save()` |
| Una persona con roles en dos conjuntos es un solo registro con dos asignaciones | Hecho y probado en `apps/permisos/tests.py` (`531e854`) |

Para pasar a Terminada (maestro §8.1) le falta: el criterio de la API, el PR `desarrollo → pruebas` revisado por Camilo y la prueba manual de quien no la programó. "El endpoint está documentado" aplica cuando exista el endpoint.

#### HU-05 · Aislamiento de datos entre conjuntos — 2 de 5 tareas, dos a medias

| Tarea técnica (Excel V11.1) | Estado | Evidencia |
|---|---|---|
| Llaves foráneas compuestas `(id, conjunto_id)` e índices encabezados por `conjunto_id` | **A medias** | FK compuesta lista: `fk_compuesta()` + `UNIQUE (id, conjunto)` en `ModeloDeConjunto`, probada con las tablas de apoyo. Faltan los índices encabezados por `conjunto_id` |
| Lista cerrada de tablas globales exenta del `conjunto_id` | Hecha | `TABLAS_GLOBALES` en `tests/esquema/test_tablas_globales.py`. No coincide del todo con el maestro §5.4 (§6) |
| Middleware que resuelve el conjunto activo desde la sesión, como contexto de solo lectura | **Pendiente** | Existe el contexto donde lo guardará (`contexto.py`), no el middleware. Va con HU-26, paso 6 del plan |
| Repositorio base que inyecta `WHERE conjunto_id` en toda consulta | Hecha | `ManagerDeConjunto` + `ModeloDeConjunto`, `531e854`. "Sin SQL crudo fuera de ahí" queda como convención: nada lo impide |
| Prueba del intruso por endpoint + prueba transversal de rutas y tablas registradas | **A medias** | La transversal de tablas está hecha; la de rutas y la del intruso esperan a que haya endpoints |

| Criterio de aceptación | Estado |
|---|---|
| Un usuario del conjunto A pide un recurso del B por su identificador y recibe 404, no 403 | En la capa de datos la fila no aparece (`DoesNotExist`, probado). Falta el endpoint que responda 404 |
| Una petición con `conjunto_id` en la URL o el cuerpo se rechaza | Pendiente: no hay API |
| Una reserva del conjunto 3 que apunta a un área del conjunto 8 la rechaza la base por la FK compuesta | Hecho y probado con las tablas de apoyo, también por `bulk_create`, que se salta `save()` |
| Una tabla nueva fuera de la lista de globales sin `conjunto_id` hace fallar la suite | Hecho y probado, incluida una prueba de que la revisión detecta la tabla nueva |
| Un endpoint nuevo sin prueba del intruso hace fallar la prueba transversal | Pendiente: no hay endpoints |

#### HU-06 · Asignación de roles del catálogo fijo — 2 de 5 tareas, una a medias

| Tarea técnica (Excel V11.1) | Estado | Evidencia |
|---|---|---|
| Sembrar el catálogo fijo de 6 roles y sus permisos en código (migración) | Hecha, sin migración | `apps/permisos/catalogo.py`. No hay tablas que sembrar (§4). El reparto por rol es provisional |
| Modelo Asignación (persona, rol, conjunto) con `conjunto_id` nulo solo para el rol de plataforma | Hecha | `apps/permisos/models.py`, tres restricciones verificadas en PostgreSQL (§2.3) |
| Cálculo de permisos efectivos como unión aditiva, sin denegaciones | **Pendiente** | — |
| Pantalla de asignación de roles por persona (frontend) | Pendiente | — |
| Pruebas de los invariantes de rol y de auditoría de asignaciones | **A medias** | 15 pruebas del catálogo y de `Asignacion`. Faltan la de "nunca cero Administración" y la de auditoría, que no existe todavía |

| Criterio de aceptación | Estado |
|---|---|
| Al asignar un rol, la persona obtiene la unión de permisos de todos sus roles | Pendiente: falta el cálculo de permisos efectivos |
| Nadie puede crear ni editar un rol desde la interfaz o la API | Se cumple por diseño (catálogo en código, sin tabla). Se verifica cuando haya API |
| Un rol asignado en el conjunto A no da permisos en el B | Pendiente: depende del cálculo de permisos efectivos |
| El rol de plataforma no incluye `reserva.aprobar`, `anuncio.publicar` ni `infraccion.registrar` | Hecho y probado |
| Retirar el rol al último usuario con Administración falla | Pendiente |

#### HU-03 · Asistente por pasos para crear un conjunto — 1 de 5 tareas

| Tarea técnica (Excel V11.1) | Estado | Evidencia |
|---|---|---|
| Modelo Conjunto con campo `activo` y `conjunto_id NOT NULL` en toda tabla salvo las globales declaradas | Hecha | `apps/conjuntos/models.py` (`activo`, y `operativo`, que nace en falso). El `NOT NULL` lo imponen `ModeloDeConjunto` y la prueba transversal |
| Endpoints del asistente por pasos con guardado parcial | Pendiente | — |
| Validación de mínimos para marcar el conjunto como operativo | Pendiente | — |
| Asistente multipaso en frontend con resumen final | Pendiente | — |
| Pruebas del invariante: conjunto incompleto no queda operativo | Pendiente | Solo hay prueba de que un conjunto nuevo nace no operativo |

Ningún criterio de aceptación se cumple todavía: todos dependen del asistente, de áreas, reglamento, reglas beta o auditoría. El permiso `conjunto.crear` ya existe en el catálogo. En el plan del Sprint 1 entra como "HU-03 mínima" (paso 7).

#### HU-01 · Inicio de sesión con correo y contraseña — 1 de 5 tareas

| Tarea técnica (Notion) | Estado | Evidencia |
|---|---|---|
| Modelo Usuario y hash de contraseña (backend) | Hecha | `apps/cuentas/models.py`, `962853f`. Contraseña con el hash de Django, login por correo sin distinguir mayúsculas |
| Endpoint `POST /auth/login` con emisión de token de sesión | Pendiente | — |
| Flujo de recuperación de contraseña por SMTP | Pendiente | — |
| Pantalla de login y manejo de errores (frontend) | Pendiente | — |
| Pruebas unitarias de autenticación y expiración de token | Pendiente | — |

Adelanto: el modelo ya cubre el criterio de que un usuario desactivado no puede entrar (`is_active`), pero falta el endpoint que lo aplique. El criterio "accede y ve el selector de conjunto activo" depende de HU-26.

---

## 6. Lo que frena el avance

**Decisiones de equipo:**
- [ ] Fecha exacta de entrega y qué historias entran en el mes (maestro §12.8). Sin esto no se puede planear el Sprint 1
- [ ] Stack del frontend (maestro §12.1)

**Choques entre el esquema de diseño (base `admind`) y el maestro**, a decidir antes de construir la app que los toca:
- [x] `asignacion.conjunto_id` es `NOT NULL`, pero el maestro lo deja nulo para el Superusuario (§5.3) — resuelto el 2026-09-15 a favor del maestro (§4)
- [x] Roles y permisos como tablas, contra "catálogos fijos en código" (§5.3) — resuelto el 2026-09-15 a favor del maestro (§4)
- [ ] Estados de `reserva` con nombres distintos a los del maestro — app `reservas`
- [ ] `area_comun` sin `clasificacion` (§3.1) — app `areas`
- [ ] No hay tablas de reglas (§5.10) ni de notificaciones
- [ ] Columnas `registrado_por`, `decidido_por`, `priorizado_por` y `anulado_por` sin FK ni destino claro (¿persona o usuario?). Mientras tanto `Asignacion` se creó sin `registrado_por`
- [ ] `auditoria` sin `via_superusuario` (§5.3)

**Diferencias entre el código y el maestro**, a llevar al maestro o corregir en el código:
- [ ] Lista cerrada de tablas globales: el código agrega `conjuntos_conjunto`, `cuentas_usuario_groups` y `cuentas_usuario_user_permissions`, y admite `conjunto_id` nulo en `permisos_asignacion`. El maestro §5.4 solo nombra `Persona`, `Usuario` y los catálogos de roles y permisos, y su R12 todavía dice "falta escribir la lista cerrada"
- [ ] Reparto de permisos por rol en `catalogo.py`: interpretado del maestro §5.3, provisional hasta validarlo con un administrador real (maestro §11.4)

**Técnicos:**
- [x] Subir a `origin/desarrollo` los commits del backend — hecho el 2026-09-15, `desarrollo` al día hasta `531e854`
- [x] Instalar `pytest` y `pytest-django` y escribir las pruebas de HU-04 — `dc6a414`
- [ ] Declarar la capa de servicios en `apps/README.md`, que todavía describe el flujo vista → modelo
- [x] Commit de este archivo y de los cambios del maestro en el repositorio de documentación — `b08754f`
- [ ] En Notion: pasar HU-01, HU-03, HU-04, HU-05 y HU-06 a "En progreso" (ninguna a Terminada, aunque los mensajes de commit digan "completada" o "hechos") y corregir la lista de tipos de documento de HU-04
- [ ] Darle `CREATEDB` al `admind_user` de Camilo: sin eso `pytest` no puede crear la base de pruebas
- [ ] Índices encabezados por `conjunto_id` cuando nazca la primera tabla del producto que herede de `ModeloDeConjunto` (HU-05)
- [ ] Paso 5 del plan del Sprint 1: login, decidiendo entre token y sesión

**Límites conocidos del aislamiento** (no son errores, pero hay que tenerlos presentes):
- `bulk_create()` y `update()` se saltan `save()`, así que no validan que la fila sea del conjunto activo. La FK compuesta sigue impidiendo apuntar a otro conjunto, pero no protege el `conjunto_id` de la propia fila
- `Asignacion` no hereda de `ModeloDeConjunto` (su conjunto puede ser nulo): sus consultas no se filtran solas por el conjunto activo
- `ManagerDeConjunto` falla sin conjunto activo: el admin de Django, el `shell` o un script que consulte una tabla de conjunto necesitan `usar_conjunto()` o el middleware

---

## 7. Cómo se actualiza este archivo

Al cerrar cada sesión de trabajo, quien la cierre (persona o agente) actualiza **solo lo que cambió**:

1. `actualizado` en el frontmatter y el corte de la §1, con fecha y hora
2. Filas nuevas al final de la bitácora (§3), con el hash del commit cuando exista
3. El avance de las historias tocadas en §5.2 y su detalle en §5.3. Una historia que se termina sale de §5.3 y suma sus SP en §5.1
4. Decisiones nuevas en §4, con quién decidió y dónde quedaron
5. Marcar o agregar pendientes en §6

**Reglas:**
- Una historia es **Terminada** solo si cumple la Definition of Done (maestro §8.1). Al 80 % aporta 0 SP (maestro §11.3)
- Lo que se afirme del código se verifica en el repositorio o en la base antes de escribirlo
- Si una historia cambia de estado aquí, también se cambia en Notion
- No va aquí: diseño ni reglas de negocio (maestro), ejercicios del lab (`Admind_Seguimiento_Lab.md`), errores con su aprendizaje (`Admind_Bitacora_Errores.md`)
