---
titulo: "AdMind — Avance del proyecto"
proyecto: "Proyecto de Ingeniería de Software II — Universidad de Cundinamarca, Facatativá"
creado: 2026-09-14
actualizado: "2026-09-14 23:45 (hora de Colombia)"
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

**Corte: 2026-09-14, 23:45.** Primer día de desarrollo real y primer día del plazo de un mes (entrega cerca del 2026-10-14, fecha exacta por confirmar; maestro §11).

| Frente | Estado |
|---|---|
| **Backend** | Proyecto Django conectado a PostgreSQL, con los modelos `Persona` y `Usuario` migrados. Tres commits en `desarrollo`, **dos sin subir** al remoto |
| **Frontend** | Solo estructura de carpetas con README (commit `764425c`, 2026-09-13). Sin código |
| **Historias** | **0 de 38 terminadas (0 de 188 SP).** Dos en progreso: HU-04 (4 de 5 tareas) y HU-01 (1 de 5) |
| **Sprint 1** | Sin iniciar formalmente. Qué entra en el mes y en cuántos sprints sigue abierto (maestro §12.8) |
| **Pruebas automáticas** | Ninguna en el repositorio |

> [!NOTE] Por qué 0 SP con dos historias avanzadas
> El método de velocidad acordado con el docente (maestro §11.3) solo cuenta lo terminado: una historia al 80 % aporta 0 SP. HU-04 tiene casi todo, pero le faltan las pruebas y dos criterios que dependen de piezas que no existen.

---

## 2. Qué existe en el código

### 2.1 Repositorios

| Repositorio | Rama | Último commit | En el remoto |
|---|---|---|---|
| Backend | `desarrollo` | `962853f` — modelos Persona y Usuario (2026-09-14 23:37) | **No**: va 2 commits adelante de `origin/desarrollo` |
| Frontend | `desarrollo` | `764425c` — estructura de carpetas (2026-09-13 01:01) | Sí |
| Documentación | `main` | `2813ee2` — tipos de documento en el maestro (2026-09-14 22:31) | Sí |

### 2.2 Backend, pieza por pieza

| Pieza | Estado | Dónde |
|---|---|---|
| Django 5.2.17, Django REST Framework 3.18, psycopg 3.3 | Instalado | `requirements.txt` |
| Proyecto Django (`startproject config .`) | Hecho | `config/` |
| Clave secreta y conexión a la base por variables de entorno | Hecho | `config/settings.py` + `.env` (fuera del repositorio) |
| PostgreSQL 18 local, base `admind_db`, usuario `admind_user` | Hecho, en la máquina de Alejo | — |
| App `personas` con el modelo `Persona` | Hecho | `apps/personas/models.py` |
| App `cuentas` con el modelo `Usuario` y `AUTH_USER_MODEL` | Hecho | `apps/cuentas/models.py` |
| Migraciones `0001` de las dos apps, aplicadas | Hecho | `apps/*/migrations/` |
| Pruebas (`pytest`, `pytest-django`) | **No hay** | — |
| Endpoints de la API | **No hay** | — |
| Capa de servicios (flujo controlador → servicio → repositorio que pide el profesor) | **No hay** | — |
| Resto de apps (`conjuntos`, `permisos`, `unidades`, …) | Solo carpeta con README | `apps/` |

### 2.3 Restricciones verificadas en PostgreSQL

Revisadas directamente en `admind_db` el 2026-09-14, no solo en el código de Python:

| Tabla | Restricción | Qué impide |
|---|---|---|
| `personas_persona` | `persona_documento_unico` | Dos personas con el mismo tipo y número de documento |
| `personas_persona` | `persona_tipo_documento_valido` | Un tipo de documento fuera de `CC`, `TI`, `CE`, `PAS`, `PPT` |
| `personas_persona` | `persona_documento_normalizado` | Guardar un número con puntos, espacios o ceros a la izquierda |
| `personas_persona` | `persona_telefono_valido` | Un teléfono con letras o de largo inválido |
| `cuentas_usuario` | `UNIQUE (correo)` | Dos cuentas con el mismo correo |
| `cuentas_usuario` | `UNIQUE (persona_id)` + FK a `personas_persona` | Dos cuentas para la misma persona, o una cuenta sin persona |

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

---

## 5. Historias de usuario

### 5.1 Por sprint previsto

Sprint previsto según Notion (reparto del Excel V11.1). Con el plazo de un mes este reparto ya no se cumple tal cual (maestro §12.8), pero se conserva como referencia.

| Sprint previsto | Historias | SP | Terminadas | En progreso |
|---|---|---|---|---|
| 1 | HU-01 a HU-05, HU-26 | 25 | 0 | 2 |
| 2 | HU-06 a HU-09 | 20 | 0 | 0 |
| 3 | HU-10 a HU-13 | 26 | 0 | 0 |
| 4 | HU-14 a HU-19 | 28 | 0 | 0 |
| 5 | HU-20, HU-21, HU-25, HU-27, HU-28, HU-29 | 28 | 0 | 0 |
| 6 | HU-22, HU-23, HU-24, HU-30 a HU-34 | 38 | 0 | 0 |
| 7 | HU-35, HU-36, HU-37 | 16 | 0 | 0 |
| Condicional | HU-38 | 7 | 0 | 0 |
| **Total** | **38** | **188** | **0** | **2** |

### 5.2 Todas las historias

Avance: **Sin empezar** · **En progreso** (con tareas técnicas hechas sobre el total de Notion) · **Terminada** (solo si cumple la DoD, maestro §8.1).

| HU | Historia | Sprint | SP | Prioridad | Avance |
|---|---|---|---|---|---|
| HU-01 | Inicio de sesión con correo y contraseña | 1 | 3 | Alta | **En progreso** (1/5) |
| HU-02 | Segundo factor (TOTP) para permisos sensibles | 1 | 5 | Alta | Sin empezar |
| HU-03 | Asistente por pasos para crear un conjunto | 1 | 6 | Alta | Sin empezar |
| HU-04 | Persona global única por documento | 1 | 3 | Alta | **En progreso** (4/5) |
| HU-05 | Aislamiento de datos entre conjuntos | 1 | 2 | Alta | Sin empezar |
| HU-26 | Selector de conjunto activo | 1 | 6 | Alta | Sin empezar |
| HU-06 | Asignación de roles del catálogo fijo | 2 | 6 | Alta | Sin empezar |
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

#### HU-04 · Persona global única por documento — 4 de 5 tareas

| Tarea técnica (Notion) | Estado | Evidencia |
|---|---|---|
| Modelo Persona con PK UUID y campos `tipo_documento` y `numero_documento` | Hecha | `apps/personas/models.py`, `962853f` |
| Restricción `UNIQUE (tipo_documento, numero_documento)` en base de datos | Hecha | `persona_documento_unico`, verificada en PostgreSQL |
| Catálogo cerrado de tipos de documento | Hecha, con la lista revisada | `TipoDocumento` + `persona_tipo_documento_valido`. Notion todavía dice `CC, CE, PA, PEP, TI` |
| Normalización del número al guardar | Hecha | `normalizar_documento()` en `save()` + `persona_documento_normalizado` |
| Pruebas: dos altas con el mismo documento producen una sola Persona | **Pendiente** | Se probó a mano en una copia aparte; no hay pruebas en el repositorio |

| Criterio de aceptación | Estado |
|---|---|
| Un documento que ya existe no crea un segundo registro | Lo impide la base; falta la prueba automática |
| El mismo número con distinto tipo es otra persona | Lo permite el `UNIQUE` compuesto; falta la prueba |
| En la API o en una URL la persona se identifica por UUID, nunca por documento | La llave es UUID; **no hay API todavía** |
| Un número escrito con puntos o espacios queda normalizado | Hecho; falta la prueba |
| Una persona con roles en dos conjuntos es un solo registro con dos asignaciones | **Depende de `Asignacion` (HU-06)**, que no existe |

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
- [ ] `asignacion.conjunto_id` es `NOT NULL`, pero el maestro lo deja nulo para el Superusuario (§5.3) — app `permisos`
- [ ] Roles y permisos como tablas, contra "catálogos fijos en código" (§5.3) — app `permisos`
- [ ] Estados de `reserva` con nombres distintos a los del maestro — app `reservas`
- [ ] `area_comun` sin `clasificacion` (§3.1) — app `areas`
- [ ] No hay tablas de reglas (§5.10) ni de notificaciones
- [ ] Columnas `registrado_por`, `decidido_por`, `priorizado_por` y `anulado_por` sin FK ni destino claro (¿persona o usuario?)
- [ ] `auditoria` sin `via_superusuario` (§5.3)

**Técnicos:**
- [ ] Subir a `origin/desarrollo` los commits `6021bb9` y `962853f` del backend
- [ ] Instalar `pytest` y `pytest-django` y escribir las pruebas de HU-04 (cierra su última tarea)
- [ ] Declarar la capa de servicios en `apps/README.md`, que todavía describe el flujo vista → modelo
- [ ] Commit de este archivo y de los cambios del maestro en el repositorio de documentación
- [ ] En Notion: pasar HU-01 y HU-04 a "En progreso" y corregir la lista de tipos de documento de HU-04

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
