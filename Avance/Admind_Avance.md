---
titulo: "AdMind — Avance del proyecto"
proyecto: "Proyecto de Ingeniería de Software II — Universidad de Cundinamarca, Facatativá"
creado: 2026-09-14
actualizado: "2026-09-27 17:35 (hora de Colombia)"
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

**Corte: 2026-09-27, 17:35.** Un agente ejecutó `Guias/Admind_Plan_Sprints_2_3.md` de la Fase 0 a la 10, con las decisiones D1 a D12 en su opción recomendada (Alejo, 2026-09-27).

| Frente | Estado al 2026-09-27 |
|---|---|
| **Backend** | `desarrollo` en `66f8897`: 15 commits locales sobre `3c70e3a`, **sin subir**. Apps nuevas `auditoria`, `areas`, `reglas` y `reservas`, API de `personas` y `apps/comun/bloqueo/`. Migraciones nuevas aplicadas en `admind_db` (§2.5) |
| **Frontend** | `desarrollo` en `c1d8f6b`: 9 commits locales sobre `b42ce93`, **sin subir**. Pantallas reales de áreas, apartamentos, roles, registrar persona, reglas y reservas; Alpine.js 3.17.4 autoalojado (§2.5) |
| **Historias** | HU-06 a HU-13 con todos sus criterios en código y con prueba (§5.3). **Ninguna Terminada**: les falta la DoD humana (PR `desarrollo → pruebas` revisado y prueba manual de quien no la programó) |
| **Pruebas automáticas** | Backend: **300, todas pasan** (eran 171). Front: **109, todas pasan** (eran 51). `makemigrations --check` sin cambios |

> [!WARNING] Filas que esta sesión no tocó
> Lo que sigue de este archivo quedó en el corte del 2026-09-15 salvo las historias HU-06 a HU-13, la §2.5, la bitácora del 2026-09-27, las decisiones del plan y los pendientes marcados con esa fecha. Entre el 2026-09-15 y el 2026-09-25 se construyeron otras piezas (HU-01, HU-02, HU-03, HU-21, HU-25, HU-26…) que aquí siguen con su estado viejo. El punto de partida verificado de esta sesión está en el plan, §1.

**Corte anterior: 2026-09-15, 10:35.** Segundo día de desarrollo real dentro del plazo de un mes (entrega cerca del 2026-10-14, fecha exacta por confirmar; maestro §11).

| Frente | Estado |
|---|---|
| **Backend** | Django sobre PostgreSQL con `Persona`, `Usuario`, `Conjunto`, `Asignacion` y `TokenDeSesion`, el catálogo de roles y permisos en código y el aislamiento por conjunto. **Primeros endpoints:** inicio y cierre de sesión con token (`0b0c4f8`) y selector de conjunto activo con la prueba del intruso (`d9b6271`). Todo en el remoto |
| **Frontend** | Proyecto Django con **ingreso y salida funcionales** contra la API y maquetas del resto de pantallas, a partir del borrador de Alejo. En `557bc9f`, en el remoto (§2.4) |
| **Historias** | **0 de 38 terminadas (0 de 188 SP).** Siete en progreso: HU-04 y HU-05 con todas sus tareas (les falta la DoD); HU-01 con 4 de 5; HU-06 y HU-26 con 3 de 5; HU-02 y HU-03 con 1 de 5 |
| **Plan técnico del Sprint 1** | Pasos 1 a 6 de 8 hechos (§4), el último en `d9b6271`. Sigue el paso 7, HU-03 mínima, con el alcance por decidir (§6) |
| **Sprint 1** | Sin iniciar formalmente. Qué entra en el mes y en cuántos sprints sigue abierto (maestro §12.8) |
| **Pruebas automáticas** | Backend: **69, todas pasan** (`pytest` sobre `d9b6271`, corrido el 2026-09-15 09:25). En `0b0c4f8` eran 48. Front: **ninguna en el repositorio**; el login se verificó con un script aparte (§3) |

> [!NOTE] Por qué 0 SP con siete historias avanzadas
> El método de velocidad acordado con el docente (maestro §11.3) solo cuenta lo terminado: una historia al 80 % aporta 0 SP.
> Los mensajes de commit dicen *"HU 04 completada"* (`dc6a414`), *"[HU-03] [HU-05] [HU-06] hechos"* (`531e854`) y *"Token de inicio de sesion y HU1"* (`0b0c4f8`). **Ninguna historia cumple la DoD** (maestro §8.1). HU-04 y HU-05 tienen todas sus tareas, pero les falta el PR `desarrollo → pruebas` revisado por Camilo y la prueba manual de quien no las programó; a HU-04 además le falta el criterio de la API. Detalle en §5.3.

---

## 2. Qué existe en el código

### 2.1 Repositorios

| Repositorio | Rama | Último commit | En el remoto |
|---|---|---|---|
| Backend | `desarrollo` | `d9b6271` — selector de conjunto activo y aislamiento por endpoint (2026-09-15 09:11) | Sí |
| Frontend | `desarrollo` | `1a4e7d1` — merge con dos commits de Camilo, sobre `557bc9f`: proyecto Django, login y maquetas (2026-09-15 10:14) | Sí |
| Documentación | `main` | `c556285` — este archivo al corte de las 09:00 (2026-09-15 09:13) | Sí. Las actualizaciones de las 09:25, las 10:13 y las 10:35 de este archivo, sin commit, y cambios sin commit en otros dos archivos |

### 2.2 Backend, pieza por pieza

| Pieza | Estado | Dónde |
|---|---|---|
| Django 5.2.17, Django REST Framework 3.18, psycopg 3.3, pytest-django 4.14 | Instalado; `rest_framework` en `INSTALLED_APPS` | `requirements.txt`, `config/settings.py` |
| Proyecto Django (`startproject config .`) | Hecho | `config/` |
| Clave secreta y conexión a la base por variables de entorno | Hecho | `config/settings.py` + `.env` (fuera del repositorio) |
| `TIME_ZONE = 'America/Bogota'` y `LANGUAGE_CODE = 'es-co'` (mensajes de Django y DRF en español) | Hecho | `config/settings.py` |
| PostgreSQL 18 local, base `admind_db`, usuario `admind_user` con `CREATEDB` | Hecho, en la máquina de Alejo | — |
| App `personas` con el modelo `Persona` | Hecho | `apps/personas/models.py` |
| App `cuentas` con el modelo `Usuario` y `AUTH_USER_MODEL` | Hecho | `apps/cuentas/models.py` |
| App `conjuntos` con el modelo `Conjunto` (UUID, `nombre`, `direccion`, `activo`, `operativo`) | Hecho. `operativo` nace en falso; sin campo de color | `apps/conjuntos/models.py` |
| Catálogo fijo en código: 6 roles, 46 permisos, 18 sensibles y el reparto por rol | Hecho. **El reparto por rol es provisional** | `apps/permisos/catalogo.py` |
| Modelo `Asignacion` (persona, rol, conjunto, vigencias) | Hecho | `apps/permisos/models.py` |
| `Asignacion.objects.vigentes()`: empezaron y no han terminado | Hecho | `apps/permisos/models.py`, `d9b6271` |
| Servicios de permisos: conjuntos disponibles de una persona, `puede_operar_en` y permisos efectivos | Hecho | `apps/permisos/servicios.py`, `d9b6271` |
| Conjunto activo de la operación (`ContextVar`): `usar_conjunto()` para fijarlo a mano; `contexto_limpio()` y `fijar_conjunto_activo()` para las peticiones | Hecho; los dos últimos en `d9b6271` | `apps/comun/aislamiento/contexto.py` |
| Modelo base `ModeloDeConjunto` con `ManagerDeConjunto` (filtra toda consulta por el conjunto activo) | Hecho. **Ningún modelo del producto lo usa todavía** | `apps/comun/modelos_base/modelos.py`, `apps/comun/aislamiento/managers.py` |
| `fk_compuesta()`: FK `(x_id, conjunto_id)` escrita en la migración | Hecho. Probada solo con tablas de apoyo | `apps/comun/aislamiento/migraciones.py` |
| `VistaDeConjunto`: vista base de DRF que fija el conjunto activo desde el token, rechaza `conjunto` o `conjunto_id` en la ruta, la URL o el cuerpo (400) y exige conjunto activo (403). Hace el papel del middleware del maestro (§4) | Hecho | `apps/comun/aislamiento/vistas.py`, `d9b6271` |
| Modelo `TokenDeSesion`: huella SHA-256 del token, usuario, conjunto activo, 2FA verificado y vencimiento | Hecho | `apps/cuentas/models.py`, `0b0c4f8` |
| Autenticación de DRF por `Authorization: Token <token>`. Toda vista exige token, salvo las que lo declaren | Hecho | `apps/cuentas/autenticacion.py`, `config/settings.py` |
| Duración del token: 1 hora fija | Hecho | `DURACION_TOKEN_DE_SESION` en `config/settings.py` |
| `POST /auth/login/` y `POST /auth/logout/` | Hecho (`0b0c4f8`). Desde el paso 6 el login también devuelve `conjunto_activo` y `permisos` | `apps/cuentas/` |
| `GET /auth/conjuntos/` y `POST /auth/conjunto-activo/` | Hecho (`d9b6271`) | `apps/cuentas/` |
| Capa de servicios (flujo controlador → servicio → repositorio que pide el profesor) | Hecho en `cuentas` y `permisos`. `apps/README.md` todavía no la declara | `apps/*/servicios.py` |
| Migraciones: `0001` de `personas`, `conjuntos` y `permisos`; `0001` y `0002` de `cuentas`. Todas aplicadas en `admind_db` | Hecho. El paso 6 no trae migraciones | `apps/*/migrations/` |
| Pruebas con `pytest` y `pytest-django`: 69 (10 de personas, 17 de cuentas, 2 de conjuntos, 20 de permisos, 7 del filtro por conjunto, 10 del intruso y de rutas, 3 de tablas globales) | Hecho, todas pasan. 21 son del paso 6 (`d9b6271`) | `pytest.ini`, `apps/*/tests.py`, `tests/` |
| Configuración de pruebas: app de apoyo `tests.aislamiento` (`Area`, `Reserva` y dos endpoints), URLs de pruebas y cifrado rápido de contraseñas | Hecho; las URLs de pruebas, en `d9b6271` | `config/settings_pruebas.py`, `config/urls_pruebas.py`, `tests/aislamiento/` |
| Plantilla de variables de entorno | Hecho | `.env _ejemplo` |
| Recuperación de contraseña por correo, 2FA TOTP y clase de permiso por vista | **No hay** | — |
| `ALLOWED_HOSTS` para desplegar | **No hay**, tampoco en el front | — |
| Resto de apps (`unidades`, `areas`, `reservas`, …) | Solo carpeta con README | `apps/` |

### 2.3 Restricciones verificadas en PostgreSQL

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

### 2.4 Frontend, pieza por pieza

En `557bc9f` (2026-09-15 10:14), en la rama `desarrollo` de `Admind_Front-End` y en el remoto. Construido a partir del borrador de Alejo (`C:\Users\Alejandro\Desktop\Pagina`, seis páginas HTML) y adaptado al sistema de diseño (§4).

| Pieza | Estado | Dónde |
|---|---|---|
| Proyecto Django del servidor web: Django 5.2.17, requests 2.34, python-dotenv | Hecho | `config/`, `manage.py`, `requirements.txt` |
| Sin base de datos (`DATABASES = {}`). Las sesiones de este servidor se guardan en archivos de la carpeta temporal del sistema | Hecho | `config/settings.py` |
| Clave secreta y dirección de la API por variables de entorno (`DJANGO_SECRET_KEY`, `ADMIND_API_URL`), con plantilla | Hecho | `.env` (fuera del repositorio), `.env _ejemplo` |
| `.gitignore` con `.venv`, `.env` y cachés | Hecho | `.gitignore` |
| `pedir()`: el único punto que llama a la API. Agrega `Authorization: Token`, convierte un 400 en errores por campo, da texto a 401, 403 y 404 ("No encontrado.") y avisa si la API no responde | Hecho | `cliente_api/http.py` |
| `iniciar_sesion` (`POST /auth/login/`) y `cerrar_sesion` (`POST /auth/logout/`) | Hecho | `cliente_api/cuentas.py` |
| **Ingreso funcional**: errores bajo cada campo, mensaje genérico de la API, token guardado en la sesión del servidor, sesión que vence con el token e id de sesión nuevo al entrar | Hecho | `apps/cuentas/` |
| Salir (`POST /salir/`): llama al logout de la API y vacía la sesión aunque la API falle | Hecho | `apps/cuentas/views.py` |
| `SesionRequeridaMiddleware`: toda pantalla exige sesión, salvo las marcadas con `@publica` | Hecho | `apps/cuentas/sesion.py` |
| Plantillas base (`base`, `sin_sesion`, `aplicacion`) y los componentes `BarraSuperior` y `Lateral`, sobre las clases de `design-system/` | Hecho | `templates/` |
| CSS propio, solo con variables del sistema de diseño | Hecho | `static/css/estructura.css`, `static/css/reservas.css` |
| **Maquetas** con datos de ejemplo y sin llamadas a la API: recuperar contraseña, selector de conjunto, inicio, calendario de zonas comunes, reglas y anuncios. Solicitudes y apartamentos y parqueaderos, como estado vacío | Hecho | `apps/cuentas`, `conjuntos`, `paneles`, `reservas`, `reglas`, `anuncios`, `triage`, `unidades` |
| Pruebas automáticas del front | **No hay**. El login se verificó con un script fuera del repositorio (§3) | `tests/` solo tiene README |
| Selector conectado a la API, recuperación de contraseña real, 2FA y Alpine.js | **No hay** | — |
| `index.html` y `apps/Administrador/Home.html`: dos HTML de prueba de Camilo (`57a45c0`, `fd6a03d`, 2026-09-14) que llegaron con el merge `1a4e7d1`. Quedan fuera de la estructura de Django y ninguna vista los sirve | Por decidir con Camilo (§6) | Raíz y `apps/Administrador/` del front |

Las maquetas **no cuentan como avance** de las historias de esas pantallas (HU-08, HU-10, HU-11, HU-22, HU-25, HU-26): no llaman a la API ni cumplen sus criterios.

### 2.5 Construido en los Sprints 2 y 3 (2026-09-27)

**Backend** (`3c70e3a..66f8897`). Toda tabla nueva hereda `ModeloDeConjunto`, sus FK entre tablas de conjunto son compuestas y toda ruta nueva está en la prueba del intruso.

| Pieza | Dónde |
|---|---|
| Auditoría de solo inserción: tabla `auditoria_registro` (actor, acción, entidad, antes, después, detalle, `via_superusuario`). Modificar o borrar una fila lanza `RegistroInmutable`, también por el queryset. Quitarle `UPDATE` y `DELETE` al usuario de base de datos queda para después (D8 a) | `apps/auditoria/` |
| Áreas comunes: clasificación cerrada (`comun`, `comun_esencial`, `comun_uso_exclusivo`), `es_esencial` derivado, horario con bloques fijos (D1 a), mantenimiento y desactivar sin borrar. `franjas_del_dia()` | `apps/areas/`, rutas `/areas/` |
| Unidades y vínculos: crear unidad, detalle con vigentes e históricos, registrar y cerrar vínculos (solo para quien ya tiene rol en el conjunto, P3), `unidades_para_solicitar()` | `apps/unidades/`, rutas `/unidades/<id>/…` |
| Roles: `asignar_rol` y `retirar_rol` con auditoría; retirar al último de Administración responde 409, con `select_for_update` sobre las asignaciones de Administración | `apps/permisos/servicios.py`, rutas `/auth/usuarios/<id>/roles/…` |
| `UsuarioResumenSerializer` gana `persona` y `asignaciones` (P2) | `apps/cuentas/serializers.py` |
| Búsqueda por documento exacto (POST) con auditoría y límite de 20 por hora, 429 al pasarse (D6); vincular reutiliza `asignar_rol` | `apps/personas/`, rutas `/personas/buscar/` y `/personas/vincular/` |
| Reglas beta: catálogo de 7 tipos que solo restringen (D4 a), validador de parámetros, descripción en palabras, versionado al editar (`reemplaza`) y retirar por vigencia | `apps/reglas/catalogo.py`, `models.py`, `servicios.py`, rutas `/reglas/` |
| Motor de reglas: alfas `RESIDE`, `NO_EN_EL_PASADO` y `AREA_DISPONIBLE`; un evaluador por tipo; AND sin detenerse en la primera falla. `unidad_en_mora()` provisional en `False` hasta HU-35 (D5 b) | `apps/reglas/alfa.py`, `evaluador.py`, `mora.py` |
| Mecanismo compartido de bloqueo (R1): `tomar()` traduce el índice único parcial en `RecursoOcupado`; `expirar_vencidos()` es un solo `UPDATE` idempotente | `apps/comun/bloqueo/bloqueo.py` |
| Reservas: `Solicitud` con 7 estados (`LIBERADA` nuevo, D2 a), índices únicos parciales por franja y por persona (D3 a); franjas, tomar el bloqueo de 3 minutos, liberar, avisos del panel, enviar con evaluación guardada (P10) y aviso a la Administración | `apps/reservas/`, rutas `/reservas/…` |
| `requisitos_para_operar`: `areas` y `reglas_beta` pasan a disponibles. El reglamento sigue en construcción, así que ningún conjunto queda operativo | `apps/conjuntos/servicios.py` |
| Pruebas de concurrencia obligatorias del maestro §5.1 (10 hilos con barrera sobre la misma franja) | `tests/concurrencia/test_bloqueo_de_franjas.py` |
| Migraciones nuevas, **aplicadas en `admind_db`**: `auditoria 0001`, `areas 0001`, `reglas 0001`, `reservas 0001` | `apps/*/migrations/` |

**Frontend** (`b42ce93..c1d8f6b`)

| Pieza | Dónde |
|---|---|
| Áreas comunes: lista, alta con clasificación obligatoria, edición con mantenimiento, desactivar; ítem "Áreas comunes" en el lateral con `area.gestionar` | `apps/areas/`, `cliente_api/areas.py` |
| Asistente de HU-03 en cinco pasos: 1 Datos, 2 Administración, 3 Áreas, 4 Reglas, 5 Resumen | `apps/conjuntos/` |
| Apartamentos: lista con vínculos vigentes, registrar apartamento, detalle con vigentes e históricos, agregar y cerrar vínculos. Reemplaza la maqueta | `apps/unidades/`, `cliente_api/unidades.py` |
| Roles en el detalle del usuario: retirar y asignar los que no tiene; el 409 del último administrador como alerta | `apps/usuarios/`, `cliente_api/cuentas.py` |
| Registrar persona: buscar por documento, vincular si existe, o pasar al alta con el documento por la sesión, nunca por la URL (P4) | `apps/usuarios/`, `cliente_api/personas.py` |
| Reglas: lista agrupada por área, alta en dos pasos sin JavaScript con un formulario por tipo, edición que avisa la versión nueva. Reemplaza la maqueta | `apps/reglas/`, `cliente_api/reglas.py` |
| Reservas: selector de área, franjas del día con su estado en texto, Reservar, solicitud con cuenta regresiva, Cancelar y `sendBeacon` al salir, panel de confirmación y envío | `apps/reservas/`, `cliente_api/reservas.py`, `static/js/reservas.js` |
| Fragmento de confirmación del contenido, solo con clases existentes (P7) | `templates/componentes/confirmacion_de_contenido.html` |
| Alpine.js 3.17.4 autoalojado, con versión y SHA-256 anotados; se carga solo donde se usa (P13) | `static/js/vendor/`, `templates/base/base.html` |
| Mensajes de 409 y 429 en el cliente de la API (P12) | `cliente_api/http.py` |

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
| 2026-09-15 05:45 | Documentación | `1c11335` — actualización de este archivo con los dos commits de la madrugada |
| 2026-09-15 05:52 | Documentación | `81f6298` — este archivo con las historias en progreso en Notion. Sin subir al corte |
| 2026-09-15 05:55 | Notion | HU-01, HU-03, HU-04, HU-05 y HU-06 pasan de "Sin empezar" a "En progreso" en `Historias de Usuario`. Son las únicas que no están en "Sin empezar" |
| 2026-09-15 08:40 | Backend | `0b0c4f8` — paso 5: `TokenDeSesion`, autenticación de DRF por token, `POST /auth/login/` y `/auth/logout/`, token obligatorio por defecto, `LANGUAGE_CODE = 'es-co'` y cifrado rápido de contraseñas en las pruebas. 11 pruebas nuevas, 48 en total. Subido a `origin/desarrollo`. Migración `cuentas 0002` aplicada en `admind_db`. El mensaje dice "HU1"; HU-01 sigue en progreso (§5.3) |
| 2026-09-15 08:59 | Backend | Paso 6 construido, **sin commit al corte**: selector de conjunto activo (`/auth/conjuntos/`, `/auth/conjunto-activo/`), `VistaDeConjunto`, permisos efectivos, prueba del intruso por endpoint y prueba transversal de rutas. 21 pruebas nuevas, 69 en total, todas pasan. Sin migraciones |
| 2026-09-15 09:00 | Notion | Tareas técnicas marcadas según el código: HU-01 (3), HU-02 (1), HU-03 (1), HU-04 (5), HU-05 (5), HU-06 (3) y HU-26 (3). HU-02 y HU-26 pasan a "En progreso". La tarea de tipos de documento de HU-04 queda con la lista vigente. Ninguna pasa a "En revisión" ni a "Finalizado" |
| 2026-09-15 09:11 | Backend | `d9b6271` — commit del paso 6: selector de conjunto activo, `VistaDeConjunto`, permisos efectivos, prueba del intruso por endpoint y prueba transversal de rutas. 15 archivos, sin migraciones. Subido a `origin/desarrollo`. El mensaje no lleva el ID de historia (maestro §8.4); lo construido avanza HU-05, HU-06 y HU-26 |
| 2026-09-15 09:13 | Documentación | `c556285` — este archivo al corte de las 09:00. Al corte siguiente, `81f6298` y `c556285` están en `origin/main` |
| 2026-09-15 09:25 | Backend | `pytest` sobre `d9b6271` con el árbol de trabajo limpio: 69 pruebas, todas pasan |
| 2026-09-15 10:02 | Frontend | Proyecto Django del servidor web creado a partir del borrador de Alejo (`Desktop\Pagina`) y adaptado al sistema de diseño: ingreso y salida funcionales contra la API, sesión exigida en toda pantalla y maquetas del resto (§2.4). **Sin commit** |
| 2026-09-15 10:03 | Frontend | Verificación con un script fuera del repositorio, 34 comprobaciones en verde. Contra el backend real: credenciales malas, correo mal escrito, campos vacíos y CSRF. Contra una API falsa: ingreso, token solo en el servidor, vencimiento, salida y calendario. Revisado en el navegador en escritorio y a 375px |
| 2026-09-15 10:07 | Base de datos | Usuario de prueba en `admind_db`, aprobado por Alejo: `Persona` CC 1000000001 (Prueba AdMind) y `Usuario` `prueba@example.com`, sin `is_staff` ni asignaciones. La contraseña no se escribe en la documentación |
| 2026-09-15 10:08 | Frontend y backend | Ingreso y salida por el front contra el backend real con el usuario de prueba: llega al selector, la sesión vence una hora después y al salir no queda ningún `TokenDeSesion` en `admind_db` |
| 2026-09-15 10:14 | Frontend | `557bc9f` — commit del front: proyecto, login y maquetas (63 archivos), sin `.env` ni `.venv`. El mensaje ("Estructura inicial Admind") no lleva el ID de historia (maestro §8.4); lo construido avanza HU-01 |
| 2026-09-15 10:14 | Frontend | `1a4e7d1` — merge de `origin/desarrollo`, que traía dos commits de Camilo del 2026-09-14 (`57a45c0`, `fd6a03d`): `index.html` y `apps/Administrador/Home.html`, HTML de prueba. Subido a `origin/desarrollo` |
| 2026-09-15 10:34 | Notion | HU-01: marcada la tarea "Pantalla de login y manejo de errores (frontend)", 4 de 5. Sigue en "En progreso". HU-26 revisada: coincide con este archivo (3 de 5) |
| 2026-09-27 16:30 | Backend y frontend | Fase 0 del plan de los Sprints 2 y 3: los dos repos limpios en `desarrollo`, `pull --ff-only` sin cambios, 171 y 51 pruebas en verde. Alejo responde "Recomendada" a D1–D12 y autoriza descargar Alpine |
| 2026-09-27 16:41 | Backend | `08f4126` — auditoría de solo inserción. Migración aplicada en `admind_db` |
| 2026-09-27 16:43–16:48 | Backend y frontend | HU-09: `f933349` modelo `Area`, `ff24541` servicio y API, `daf56af` pantalla y paso de áreas del asistente. Migración aplicada |
| 2026-09-27 16:51–16:53 | Backend y frontend | HU-08: `89e793c` API de unidades y vínculos (y P2), `a9350c2` pantalla de apartamentos |
| 2026-09-27 16:56–16:57 | Backend y frontend | HU-06: `b5003af` asignar y retirar roles, `25132e8` roles en el detalle del usuario |
| 2026-09-27 16:59–17:01 | Backend y frontend | HU-07: `37aeb85` buscar y vincular, `f4da065` registrar persona |
| 2026-09-27 17:04–17:09 | Backend y frontend | HU-10: `bb5586f` catálogo y modelo, `a8be0ae` servicio y API, `2e11201` pantalla y paso de reglas. Migración aplicada |
| 2026-09-27 17:10–17:19 | Backend y frontend | HU-11: `ddac827` bloqueo compartido, `05c621c` modelo `Solicitud`, `9d99568` servicio y API, `06f2340` concurrencia (pasó 5 de 5 corridas), `d7b04a8` Alpine 3.17.4, `6aa1a3d` pantallas. Migración aplicada |
| 2026-09-27 17:21–17:23 | Backend y frontend | HU-12: `000c335` avisos, `f6b8fef` panel de confirmación |
| 2026-09-27 17:27–17:30 | Backend y frontend | HU-13: `a8e6ca5` alfas y evaluador, `66f8897` envío, `c1d8f6b` pantalla del envío |
| 2026-09-27 17:32 | Backend y frontend | Cierre: 300 y 109 pruebas en verde, `makemigrations --check` sin cambios, `git status` limpio en los dos repos. Nada subido. El recorrido en el navegador no se hizo: pide iniciar sesión con las cuentas de prueba, cuya contraseña no tiene el agente; queda en el guion manual del plan §6 |
| 2026-09-27 17:50 | Notion | A pedido de Alejo: HU-06 a HU-13 pasan a "En revisión" (HU-06 estaba otra vez en "Finalizado"). Casillas de tareas marcadas y nota de revisión en cada página. En HU-06 se restauran las tareas 4 y 5 del Excel. En HU-12 quedan dos tareas sin marcar: alta demanda (PB-24) y el reuso del panel en citas y alternativas (HU-31, HU-32). Ninguna a "Finalizado" |

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
| 2026-09-15 | **Autenticación por token con registro en la base**, no por sesión de Django ni por JWT. Resuelve el maestro §12.7 b. El token es un texto aleatorio; la base guarda solo su huella SHA-256, y la fila guarda usuario, conjunto activo, 2FA verificado y vencimiento. El servidor web guarda el token en su propia sesión y lo reenvía en cada llamada; el navegador no lo ve. **Falta llevarlo al maestro** (§6) | Alejo, con la recomendación del agente | `apps/cuentas/models.py`, `apps/cuentas/autenticacion.py` |
| 2026-09-15 | El token dura **1 hora fija** y no se renueva con el uso | Alejo (el agente había puesto 8 horas) | `DURACION_TOKEN_DE_SESION` en `config/settings.py` |
| 2026-09-15 | Toda vista de DRF exige token por defecto (`IsAuthenticated`); solo el login lo declara a propósito | Agente, a pedido de Alejo | `config/settings.py` |
| 2026-09-15 | El login responde lo mismo (401, "Correo o contraseña incorrectos.") si el correo no existe, la contraseña es mala o la cuenta está desactivada. Desactivar la persona también corta el acceso, al entrar y en cada petición | Agente, a pedido de Alejo (criterio de HU-01 y maestro §5.11) | `apps/cuentas/servicios.py` |
| 2026-09-15 | `LANGUAGE_CODE` pasa de `en-us` a `es-co` | Alejo | `config/settings.py` |
| 2026-09-15 | Cifrado rápido de contraseñas (`MD5PasswordHasher`) **solo en las pruebas y provisional**: la suite había subido a 33 s. Antes de volver a tocarlo se le consulta a Alejo | Alejo | `config/settings_pruebas.py` |
| 2026-09-15 | `cuentas_tokendesesion` entra a la lista cerrada de tablas globales: el conjunto activo cambia dentro de la misma sesión | Alejo aprobó la propuesta del agente | `tests/esquema/test_tablas_globales.py` |
| 2026-09-15 | Lo que el maestro §5.4 llama middleware es `VistaDeConjunto`, una vista base de DRF: DRF revisa el token dentro de la vista, cuando los middleware de Django ya corrieron. Suelta el conjunto activo al terminar cada petición, aunque haya error | Agente, a pedido de Alejo | `apps/comun/aislamiento/vistas.py` |
| 2026-09-15 | Con un solo conjunto disponible, el token nace con ese conjunto activo; con varios o ninguno, nace sin conjunto. Si al usuario le retiran el rol o le desactivan el conjunto, pierde el conjunto activo en su siguiente petición | Agente, a pedido de Alejo (criterios de HU-26) | `apps/cuentas/servicios.py` |
| 2026-09-15 | Los endpoints del selector quedan en `cuentas`, bajo `/auth/`, porque cambian la sesión. El README de `apps/conjuntos` decía que el cambio de conjunto iría allí | Agente, a pedido de Alejo | `apps/cuentas/urls.py` |
| 2026-09-15 | Elegir un conjunto sin asignación vigente responde 404, exista o no el conjunto | Agente, a pedido de Alejo (maestro §5.4) | `apps/cuentas/views.py` |
| 2026-09-15 | Registro de la prueba del intruso: toda ruta de conjunto se registra con su caso, y toda ruta que no sea de conjunto se declara aparte. Una ruta nueva sin registrar hace fallar la suite. Los endpoints de apoyo solo existen en las URLs de pruebas | Agente, a pedido de Alejo | `tests/aislamiento/test_intruso.py`, `config/urls_pruebas.py` |
| 2026-09-15 | El front toma las pantallas y la navegación del borrador de Alejo, pero con las clases y tokens de `design-system/`: sin sus colores, la fuente Arial ni el símbolo ⌂, y con el menú superior pasado a `Lateral` y `BarraSuperior` | Agente (Alejo pidió basarse en el borrador) | `templates/`, `apps/*/templates/` del front |
| 2026-09-15 | Solo el login es funcional; el resto de pantallas son maquetas marcadas "Maqueta con datos de ejemplo" | Alejo | `apps/` del front |
| 2026-09-15 | El login incluye **cerrar sesión** (`POST /salir/`), que ya existía en la API | Agente, como lectura del pedido | `apps/cuentas/views.py` del front |
| 2026-09-15 | El token vive en la **sesión del servidor web**, guardada en archivos porque el front no tiene base de datos. El navegador solo recibe la cookie `sessionid` (HttpOnly). La sesión vence a la hora de `vence_en` y cambia de id al entrar. Es el lado del front de la decisión del token | Agente | `config/settings.py`, `apps/cuentas/sesion.py` del front |
| 2026-09-15 | Toda pantalla del front exige sesión por defecto (`SesionRequeridaMiddleware`); solo el ingreso y recuperar contraseña se declaran `@publica`. Es el mismo criterio que `IsAuthenticated` en la API | Agente | `apps/cuentas/sesion.py` del front |
| 2026-09-15 | `pedir()` es el único punto del front que llama a la API, con `requests`. Los campos del formulario se llaman igual que en la API (`correo`, `contrasena`) para que un 400 caiga en su campo | Agente | `cliente_api/http.py`, `apps/cuentas/forms.py` |
| 2026-09-15 | El calendario se arma en el servidor, con enlaces y recarga, sin JavaScript. Por eso todavía no se trajo Alpine.js | Agente | `apps/reservas/` del front |
| 2026-09-15 | Las apps del front se crean a mano, sin `startapp`: no llevan `models.py`, `admin.py` ni `migrations/` | Agente | `apps/*/apps.py` del front |
| 2026-09-15 | Textos del borrador: "Avisos" pasa a **Anuncios** (término del maestro) y "Zona común" a **Zonas comunes**. Se quita **"Eliminar"** de Reglas y Anuncios hasta decidir si esas entidades se borran (maestro §5.10, §5.11) | Agente, **por confirmar** (§6) | Plantillas de `reglas` y `anuncios` del front |
| 2026-09-15 | El día elegido del calendario no usa el acento, porque no es uno de sus cuatro sitios (maestro §6.1): lleva fondo hundido y borde oscuro | Agente | `static/css/reservas.css` del front |
| 2026-09-15 | Después del ingreso siempre se va al selector maqueta, aunque la API diga que la persona tiene un solo conjunto. Provisional hasta conectar el selector | Agente | `apps/cuentas/views.py` del front |
| 2026-09-27 | **D1 a**: franjas en bloques fijos por área (`hora_apertura`, `hora_cierre`, `duracion_franja_minutos`) | Alejo (recomendada) | `apps/areas/` |
| 2026-09-27 | **D2 a**: estado nuevo no bloqueante `LIBERADA` con `motivo_liberacion` `voluntaria` o `reglas`. **Falta llevarlo al maestro §5.1** | Alejo (recomendada) | `apps/reservas/models.py` |
| 2026-09-27 | **D3 a**: un solo bloqueo activo **por conjunto**, índice único parcial `(conjunto, persona)`. **Falta corregir la redacción del maestro §5.1 y §12.7 c** | Alejo (recomendada) | `apps/reservas/models.py` |
| 2026-09-27 | **D4 a**: catálogo beta de 7 tipos (sin duración máxima ni depósito) y versionado por reemplazo, con copia de la evaluación en la solicitud. Provisional hasta un reglamento real. **Falta llevarlo al maestro §5.10** | Alejo (recomendada) | `apps/reglas/` |
| 2026-09-27 | **D5 b**: `unidad_en_mora()` devuelve `False` hasta HU-35 | Alejo (recomendada) | `apps/reglas/mora.py` |
| 2026-09-27 | **D6**: 20 búsquedas por documento por hora y administrador, contadas sobre la auditoría; 429 al pasarse. Se cuentan en el conjunto activo | Alejo (recomendada) | `apps/personas/servicios.py` |
| 2026-09-27 | **D7 a**: se reserva aunque el conjunto no esté operativo, hasta HU-33 | Alejo (recomendada) | `apps/reservas/servicios.py` |
| 2026-09-27 | **D8 a**: auditoría de solo inserción en código; los dos usuarios de BD quedan para después | Alejo (recomendada) | `apps/auditoria/` |
| 2026-09-27 | **D9 a**: el panel resalta menos de 24 h, límite de anticipación y otra solicitud; alta demanda llega con PB-24 | Alejo (recomendada) | `apps/reservas/servicios.py` |
| 2026-09-27 | **D10 a**: una persona sin cuenta se vincula igual; la respuesta dice `tiene_cuenta` | Alejo (recomendada) | `apps/personas/` |
| 2026-09-27 | **D11 a**: un commit local por paso, sin push; migraciones aplicadas en `admind_db` al cerrar cada fase | Alejo (recomendada) | Git de los dos repos |
| 2026-09-27 | **D12 a**: Alpine.js 3.17.4 autoalojado, descargado de npm por el agente con autorización | Alejo (recomendada) | `static/js/vendor/` del front |
| 2026-09-27 | **P1 a P15** del plan (§3), aplicadas tal cual: FK de `Area` redeclarada, `persona` y `asignaciones` en el usuario, vincular solo a quien tiene rol, búsqueda por POST, cierres con `vigencia_hasta = hoy`, códigos 409/429/400 con `motivos`, fragmento de confirmación, residir para tomar el bloqueo, `mora.py`, evaluación en la solicitud, `DURACION_BLOQUEO`, mensajes 409/429 en el front, bloque `scripts`, solo solicitudes propias y `via_superusuario` como parámetro | Plan, aprobado por Alejo | Ver el plan §3 |
| 2026-09-27 | `RegistroInmutable` vive en `apps/auditoria/models.py` y no en `servicios.py`: el modelo lo lanza y el servicio importa el modelo | Agente | `apps/auditoria/models.py` |
| 2026-09-27 | Desactivar un área ya inactiva responde 409; una regla que todavía no empieza se cierra en su fecha de inicio | Agente (el plan no lo decía) | `apps/areas/`, `apps/reglas/servicios.py` |
| 2026-09-27 | El evaluador aplica las reglas beta **vigentes el día en que se evalúa**, no las del día de la franja | Agente (el plan no lo decía) | `apps/reglas/evaluador.py` |
| 2026-09-27 | `Resultado` vive en `apps/reglas/alfa.py` para no crear un archivo más; lo usan las alfas y el evaluador | Agente | `apps/reglas/alfa.py` |
| 2026-09-27 | El botón "Añadir usuario" de la lista pasa a "Registrar persona", que busca primero por documento | Agente (lo pide el plan F5) | `apps/usuarios/` del front |
| 2026-09-27 | El horario del panel se escribe "2:00 p. m.", como el maestro §5.1; el formato de Django daría "p.m." | Agente | `apps/reservas/views.py` del front |

---

## 5. Historias de usuario

### 5.1 Por sprint previsto

Sprint previsto según Notion (reparto del Excel V11.1). Con el plazo de un mes este reparto ya no se cumple tal cual (maestro §12.8), pero se conserva como referencia.

| Sprint previsto | Historias | SP | Terminadas | En progreso |
|---|---|---|---|---|
| 1 | HU-01 a HU-05, HU-26 | 25 | 0 | 6 |
| 2 | HU-06 a HU-09 | 20 | 0 | 4 |
| 3 | HU-10 a HU-13 | 26 | 0 | 4 |
| 4 | HU-14 a HU-19 | 28 | 0 | 0 |
| 5 | HU-20, HU-21, HU-25, HU-27, HU-28, HU-29 | 28 | 0 | 0 |
| 6 | HU-22, HU-23, HU-24, HU-30 a HU-34 | 38 | 0 | 0 |
| 7 | HU-35, HU-36, HU-37 | 16 | 0 | 0 |
| Condicional | HU-38 | 7 | 0 | 0 |
| **Total** | **38** | **188** | **0** | **14** |

### 5.2 Todas las historias

Avance: **Sin empezar** · **En progreso** (con tareas técnicas hechas sobre el total de Notion) · **Terminada** (solo si cumple la DoD, maestro §8.1).

| HU | Historia | Sprint | SP | Prioridad | Avance |
|---|---|---|---|---|---|
| HU-01 | Inicio de sesión con correo y contraseña | 1 | 3 | Alta | **En progreso** (4/5) |
| HU-02 | Segundo factor (TOTP) para permisos sensibles | 1 | 5 | Alta | **En progreso** (1/5) |
| HU-03 | Asistente por pasos para crear un conjunto | 1 | 6 | Alta | **En progreso** (1/5) |
| HU-04 | Persona global única por documento | 1 | 3 | Alta | **En progreso** (5/5, falta la DoD) |
| HU-05 | Aislamiento de datos entre conjuntos | 1 | 2 | Alta | **En progreso** (5/5, falta la DoD) |
| HU-26 | Selector de conjunto activo | 1 | 6 | Alta | **En progreso** (3/5) |
| HU-06 | Asignación de roles del catálogo fijo | 2 | 6 | Alta | **En progreso** (5/5, falta la DoD) |
| HU-07 | Vincular persona existente por búsqueda de documento | 2 | 3 | Alta | **En progreso** (criterios en código, falta la DoD) |
| HU-08 | Vínculos de unidad y enrutamiento de notificaciones | 2 | 7 | Alta | **En progreso** (criterios en código, falta la DoD) |
| HU-09 | Catálogo de áreas comunes del conjunto | 2 | 4 | Alta | **En progreso** (criterios en código, falta la DoD) |
| HU-10 | Configuración de reglas beta de reserva | 3 | 9 | Alta | **En progreso** (criterios en código, falta la DoD) |
| HU-11 | Bloqueo exclusivo de 3 minutos sobre una franja | 3 | 7 | Alta | **En progreso** (criterios en código, falta la DoD) |
| HU-12 | Confirmación de contenido antes de enviar | 3 | 2 | Alta | **En progreso** (criterios en código, falta la DoD) |
| HU-13 | Envío de solicitud y motor de reglas alfa/beta | 3 | 8 | Alta | **En progreso** (criterios en código, falta la DoD) |
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

Las tareas y criterios salen de Notion, que coincide con la copia local del Excel V11.1 (hoja `HU`). Las casillas de las tareas en Notion se marcaron el 2026-09-15 09:00 con lo que se describe aquí, y la pantalla de login de HU-01 a las 10:34, con su commit.

#### HU-04 · Persona global única por documento — 5 de 5 tareas, falta la DoD

| Tarea técnica (Notion) | Estado | Evidencia |
|---|---|---|
| Modelo Persona con PK UUID y campos `tipo_documento` y `numero_documento` | Hecha | `apps/personas/models.py`, `962853f` |
| Restricción `UNIQUE (tipo_documento, numero_documento)` en base de datos | Hecha | `persona_documento_unico`, verificada en PostgreSQL |
| Catálogo cerrado de tipos de documento | Hecha, con la lista revisada | `TipoDocumento` + `persona_tipo_documento_valido`. Notion ya dice `CC, TI, CE, PAS, PPT` (corregido el 2026-09-15) |
| Normalización del número al guardar | Hecha | `normalizar_documento()` en `save()` + `persona_documento_normalizado` |
| Pruebas: dos altas con el mismo documento producen una sola Persona | Hecha | `apps/personas/tests.py`, 10 pruebas, `dc6a414` |

| Criterio de aceptación | Estado |
|---|---|
| Un documento que ya existe no crea un segundo registro | Hecho y probado, también cuando el segundo se escribe con puntos |
| El mismo número con distinto tipo es otra persona | Hecho y probado |
| En la API o en una URL la persona se identifica por UUID, nunca por documento | La llave es UUID y hay prueba de eso; **todavía no hay endpoint que exponga personas** |
| Un número escrito con puntos o espacios queda normalizado | Hecho y probado. La base además rechaza un número sin normalizar aunque se salte `save()` |
| Una persona con roles en dos conjuntos es un solo registro con dos asignaciones | Hecho y probado en `apps/permisos/tests.py` (`531e854`) |

Para pasar a Terminada (maestro §8.1) le falta: el criterio de la API, el PR `desarrollo → pruebas` revisado por Camilo y la prueba manual de quien no la programó. "El endpoint está documentado" aplica cuando exista el endpoint.

#### HU-05 · Aislamiento de datos entre conjuntos — 5 de 5 tareas, falta la DoD

| Tarea técnica (Notion) | Estado | Evidencia |
|---|---|---|
| Llaves foráneas compuestas `(id, conjunto_id)` e índices encabezados por `conjunto_id` | Hecha | `fk_compuesta()` + `UNIQUE (id, conjunto)` en `ModeloDeConjunto`, probada con las tablas de apoyo. Cada tabla que hereda de `ModeloDeConjunto` recibe un índice sobre `conjunto_id` por su FK (verificado en la migración de apoyo). Los índices compuestos para consultas concretas se agregan con cada tabla |
| Lista cerrada de tablas globales exenta del `conjunto_id` | Hecha | `TABLAS_GLOBALES` en `tests/esquema/test_tablas_globales.py`. No coincide del todo con el maestro §5.4 (§6) |
| Middleware que resuelve el conjunto activo desde la sesión, como contexto de solo lectura | Hecha (`d9b6271`) | `VistaDeConjunto` en `apps/comun/aislamiento/vistas.py`: toma el conjunto activo de la sesión del token (§4) |
| Repositorio base que inyecta `WHERE conjunto_id` en toda consulta | Hecha | `ManagerDeConjunto` + `ModeloDeConjunto`, `531e854`. "Sin SQL crudo fuera de ahí" queda como convención: nada lo impide |
| Prueba del intruso por endpoint + prueba transversal de rutas y tablas registradas | Hecha; la parte de rutas y del intruso, en `d9b6271` | `tests/aislamiento/test_intruso.py` y `tests/esquema/test_tablas_globales.py` |

| Criterio de aceptación | Estado |
|---|---|
| Un usuario del conjunto A pide un recurso del B por su identificador y recibe 404, no 403 | Hecho y probado por endpoint, con los endpoints de apoyo |
| Una petición con `conjunto_id` en la URL o el cuerpo se rechaza | Hecho y probado: 400 con `conjunto_id` en la URL y con `conjunto` en el cuerpo |
| Una reserva del conjunto 3 que apunta a un área del conjunto 8 la rechaza la base por la FK compuesta | Hecho y probado con las tablas de apoyo, también por `bulk_create`, que se salta `save()` |
| Una tabla nueva fuera de la lista de globales sin `conjunto_id` hace fallar la suite | Hecho y probado, incluida una prueba de que la revisión detecta la tabla nueva |
| Un endpoint nuevo sin prueba del intruso hace fallar la prueba transversal | Hecho y probado, incluida una prueba de que la revisión detecta la ruta nueva |

Todo se prueba con las tablas y endpoints de apoyo, porque todavía no existen áreas ni reservas reales. Para pasar a Terminada le falta el PR revisado por Camilo y la prueba manual. Cuando exista el PR, puede pasar a "En revisión" en Notion.

#### HU-26 · Selector de conjunto activo — 3 de 5 tareas

| Tarea técnica (Notion) | Estado | Evidencia |
|---|---|---|
| Consulta de los conjuntos con asignación vigente de la persona autenticada (backend) | Hecha (`d9b6271`) | `conjuntos_disponibles()` en `apps/permisos/servicios.py` y `GET /auth/conjuntos/` |
| Escritura del conjunto activo en la sesión como contexto de solo lectura, nunca como parámetro de la petición | Hecha (`d9b6271`) | `POST /auth/conjunto-activo/` escribe en `TokenDeSesion.conjunto_activo`; `VistaDeConjunto` rechaza el conjunto en cualquier otra petición |
| Selección automática y sin pantalla cuando la persona pertenece a un solo conjunto | Hecha (`d9b6271`) | `iniciar_sesion()` en `apps/cuentas/servicios.py` |
| Pantalla de selección con nombre, logo y color base de cada conjunto (frontend) | Pendiente | Hay una **maqueta** con datos de ejemplo que no llama a la API (§2.4). El backend solo entrega `id` y `nombre`: logo y color están fuera de v1 (maestro §6.3, §12.3) |
| Cambio de conjunto activo desde la barra superior, con recálculo de permisos efectivos | **A medias** | El backend cambia el conjunto y devuelve los permisos del nuevo. La barra superior del front ya tiene "Cambiar de conjunto", pero lleva al selector maqueta sin llamar a la API |

| Criterio de aceptación | Estado |
|---|---|
| Con asignaciones vigentes en tres conjuntos, al iniciar sesión los ve y debe elegir uno antes de continuar | Hecho y probado: entra sin conjunto activo, ve los tres y una vista de conjunto responde 403 hasta que elija |
| Con un solo conjunto entra directo, sin pantalla de selección | Hecho y probado |
| Con un conjunto activo, cualquier módulo muestra solo datos de ese conjunto | Hecho y probado con los endpoints de apoyo, también al cambiar de conjunto |
| Al cambiar de conjunto, los permisos pasan a ser los de sus roles en el nuevo y ninguno del anterior | Hecho y probado (Administración en un conjunto, Residente en otro) |
| Un conjunto desactivado o sin asignación vigente no aparece en la lista | Hecho y probado. Un conjunto no operativo sí aparece (§6) |

#### HU-06 · Asignación de roles del catálogo fijo — 5 de 5 tareas, falta la DoD

Actualizado el 2026-09-27 con `b5003af` (API) y `25132e8` (pantalla). Las pruebas nuevas están en `apps/permisos/test_roles.py`.

| Criterio de aceptación | Prueba | Pasa |
|---|---|---|
| Al asignar un rol, la persona obtiene la unión de permisos de todos sus roles | `test_asignar_un_rol_suma_los_permisos_de_todos_sus_roles` | Sí |
| Nadie puede crear ni editar un rol desde la interfaz o la API | `test_no_existe_crear_ni_editar_roles`: solo existen `usuario-roles` y `usuario-rol-retirar`; `"operador"` y `"superusuario"` → 400 | Sí |
| Un rol asignado en el conjunto A no da permisos en el B | `test_rol_de_un_conjunto_no_da_permisos_en_otro` (ya existía) | Sí |
| El rol de plataforma no incluye `reserva.aprobar`, `anuncio.publicar` ni `infraccion.registrar` | `test_rol_de_plataforma_no_opera_dentro_de_un_conjunto` (ya existía) | Sí |
| Retirar el rol al último usuario con Administración falla | `test_retirar_el_rol_al_ultimo_de_administracion_falla`, `test_con_dos_administradores_se_retira_uno` y `test_dos_retiros_a_la_vez_no_dejan_el_conjunto_sin_administracion` (dos hilos) | Sí |
| Auditoría de asignaciones (tarea) | `test_asignar_y_retirar_quedan_en_la_auditoria` | Sí |

Extras: retirar quita los permisos de inmediato; asignar un rol vigente → 409; sin `rol.asignar` → 403. En el front, `tests/test_usuarios.py`: sin `rol.asignar` no hay botones, el 409 se muestra y asignar vuelve al detalle.

#### HU-07 · Vincular persona existente por búsqueda de documento — criterios en código, falta la DoD

`37aeb85` (API) y `f4da065` (pantalla). Pruebas en `apps/personas/test_busqueda.py`.

| Criterio de aceptación | Prueba | Pasa |
|---|---|---|
| Documento existente → se vincula sin crear un registro nuevo | `test_documento_existente_se_vincula_sin_crear_otra_persona` | Sí |
| Documento inexistente → se ofrece crear | API: `test_documento_inexistente_no_encuentra_a_nadie`. Front: `test_no_encontrada_lleva_al_alta_con_el_documento_y_sin_ponerlo_en_la_url` | Sí |
| Cada búsqueda queda en la auditoría con quién y qué documento | `test_cada_busqueda_queda_en_la_auditoria_con_quien_y_que_documento` | Sí |
| Pasar el límite de búsquedas se rechaza | `test_pasar_el_limite_de_busquedas_se_rechaza`: 20 en la última hora → 429; una de hace 2 h no cuenta | Sí |
| Vinculada a dos conjuntos, sus roles del otro no dan permisos | `test_vinculada_a_dos_conjuntos_sus_roles_del_otro_no_dan_permisos` | Sí |

Extras: con puntos y espacios encuentra igual, un número parcial no; la respuesta no trae teléfono, correo ni datos de otros conjuntos; vincular un rol vigente → 409. En el front, el documento nunca aparece en una URL.

#### HU-08 · Vínculos de unidad y enrutamiento de notificaciones — criterios en código, falta la DoD

`89e793c` (API) y `a9350c2` (pantalla). Pruebas en `apps/unidades/tests.py`.

| Criterio de aceptación | Prueba | Pasa |
|---|---|---|
| Propietario y arrendatario vigentes coexisten | `test_propietario_y_arrendatario_vigentes_coexisten` | Sí |
| Al cerrar el vínculo del arrendatario, el histórico se conserva | `test_al_cerrar_el_vinculo_del_arrendatario_el_historico_se_conserva` (sin `DELETE`: 405) | Sí |
| Convocatoria a asamblea → al propietario aunque no resida | `test_cada_hecho_llega_a_quien_corresponde_segun_el_vinculo` (ya existía) | Sí |
| Infracción → propietario y arrendatario | La misma prueba (ya existía) | Sí |
| Propietario no residente con rol Residente no puede reservar | `test_un_propietario_que_no_vive_ahi_no_puede_reservar` (tomar → 400) y `test_sin_vivir_en_la_unidad_elegida_la_alfa_lo_impide` (alfa `RESIDE`), en `apps/reservas/tests.py` | Sí |

Extras: vincular a una persona sin rol en el conjunto → 400 (P3); vínculo duplicado → 409; cerrar dos veces → 409; cierre antes del inicio → 400; auditoría de unidad y vínculo.

#### HU-09 · Catálogo de áreas comunes del conjunto — criterios en código, falta la DoD

`f933349`, `ff24541` (API) y `daf56af` (pantalla y paso del asistente). Pruebas en `apps/areas/tests.py`.

| Criterio de aceptación | Prueba | Pasa |
|---|---|---|
| Al crear un área hay que elegir la clasificación de la lista cerrada | `test_al_crear_un_area_hay_que_elegir_la_clasificacion_de_la_lista_cerrada` | Sí |
| Un área común esencial tiene `es_esencial` verdadero | `test_solo_un_area_comun_esencial_es_esencial` | Sí |
| Un área en mantenimiento no admite solicitudes | `test_un_area_en_mantenimiento_no_admite_solicitudes` (tomar → 409), en `apps/reservas/tests.py` | Sí |
| Sin `area.gestionar`, editar → 403 | `test_sin_area_gestionar_no_se_crea_ni_se_edita_y_solo_se_ven_las_activas` | Sí |
| Un área retirada se desactiva, no se borra | `test_un_area_retirada_se_desactiva_y_no_se_borra` | Sí |
| Regla alfa de mora sobre áreas esenciales | `test_una_unidad_en_mora_no_pide_un_area_no_esencial_pero_si_una_esencial`, en `apps/reservas/tests.py` | Sí |

Extras: el requisito `areas` de `requisitos_para_operar` se cumple con un área activa; nombre repetido → 400; cierre antes de la apertura → 400; auditoría de crear, editar, mantenimiento y desactivar.

#### HU-10 · Configuración de reglas beta de reserva — criterios en código, falta la DoD

`bb5586f`, `a8be0ae` (API) y `2e11201` (pantalla y paso del asistente). Pruebas en `apps/reglas/tests.py`.

| Criterio de aceptación | Prueba | Pasa |
|---|---|---|
| Sin reglas, el conjunto no puede quedar operativo | `test_sin_reglas_el_conjunto_no_puede_quedar_operativo` | Sí |
| Una regla exige tipo, parámetros, área y vigencia | `test_una_regla_exige_tipo_parametros_area_y_vigencia` (cuatro casos) | Sí |
| Una regla permisiva se rechaza | `test_una_regla_permisiva_se_rechaza` | Sí |
| Una regla beta no relaja una alfa | `test_una_regla_beta_no_relaja_una_alfa` | Sí |
| Se aplican en AND sin precedencias | `test_el_evaluador_no_se_detiene_en_la_primera_falla` y `test_si_incumple_tres_reglas_ve_los_tres_motivos_y_se_libera_el_bloqueo` | Sí |
| Una regla editada deja autor y fecha | `test_una_regla_editada_deja_version_autor_y_fecha` | Sí |

Extras: cada tipo se crea y se describe en palabras; parámetros de más o equivocados → 400; área de otro conjunto → 400; retirar cierra la vigencia y la conserva.

#### HU-11 · Bloqueo exclusivo de 3 minutos sobre una franja — criterios en código, falta la DoD

`ddac827`, `05c621c`, `9d99568`, `06f2340` (backend) y `d7b04a8`, `6aa1a3d` (front). Pruebas en `apps/reservas/tests.py` y `tests/concurrencia/`.

| Criterio de aceptación | Prueba | Pasa |
|---|---|---|
| Franja libre + Reservar → `EN_SOLICITUD` y reloj de 3 minutos | `test_franja_libre_y_reservar_deja_la_solicitud_en_tramite_con_3_minutos` | Sí |
| Otra persona sobre una franja en trámite → aviso inmediato | `test_otra_persona_sobre_una_franja_en_tramite_recibe_el_aviso_de_inmediato` y `test_n_residentes_sobre_la_misma_franja_producen_exactamente_un_bloqueo` (10 hilos) | Sí |
| Bloqueo vencido + acceso → `EXPIRADA` y franja libre | `test_un_bloqueo_vencido_expira_al_siguiente_acceso_y_la_franja_queda_libre` y `test_un_bloqueo_vencido_no_bloquea` | Sí |
| Con un bloqueo activo no toma otro en ninguna área | `test_con_un_bloqueo_activo_no_se_toma_otro_en_ninguna_area` | Sí |
| Al cerrar el formulario, el bloqueo se libera sin esperar | `test_al_cerrar_el_formulario_el_bloqueo_se_libera_sin_esperar` y `test_uno_liberado_a_mano_no_expira_dos_veces`. El `sendBeacon` al cerrar la pestaña va al guion manual | Sí (el beacon, pendiente de prueba manual) |

Extras: cada quien ve la franja propia como "Tuya" y la ajena sin saber de quién es; una franja que ya empezó no se toma; solo se ven las solicitudes propias.

#### HU-12 · Confirmación de contenido antes de enviar — criterios en código, falta la DoD

`000c335` (avisos) y `f6b8fef` (panel). Pruebas en `apps/reservas/tests.py` y `tests/test_reservas.py` del front.

| Criterio de aceptación | Prueba | Pasa |
|---|---|---|
| Ve el área, el día de la semana en letras, la fecha y el horario | `test_el_panel_dice_el_area_el_dia_de_la_semana_en_letras_la_fecha_y_el_horario` (front) | Sí |
| Corregir vuelve sin perder lo escrito | Guion manual (JavaScript). En código: el formulario se oculta con `x-show`, no se destruye | Pendiente de prueba manual |
| Una fecha atípica se resalta sin impedir el envío | Tres pruebas de `avisos` en el backend y `test_los_avisos_se_muestran_con_texto_y_no_deshabilitan_el_envio` (front). Alta demanda llega con PB-24 | Sí |
| El panel abierto no detiene ni extiende el reloj | Guion manual. En código: el reloj vive en el mismo `x-data` y no se reinicia | Pendiente de prueba manual |
| Un envío que salta la interfaz se evalúa igual | `test_un_envio_que_salta_la_interfaz_se_evalua_igual` | Sí |

#### HU-13 · Envío de solicitud y motor de reglas alfa/beta — criterios en código, falta la DoD

`a8e6ca5`, `66f8897` (backend) y `c1d8f6b` (front). Pruebas en `apps/reservas/tests.py` y `apps/reglas/tests.py`.

| Criterio de aceptación | Prueba | Pasa |
|---|---|---|
| Una solicitud válida pasa a `APARTADA` y se avisa a la Administración | `test_una_solicitud_valida_queda_apartada_y_se_avisa_a_la_administracion` (Consejo no recibe el aviso) | Sí |
| Si incumple tres reglas, ve los tres motivos y se libera el bloqueo | `test_si_incumple_tres_reglas_ve_los_tres_motivos_y_se_libera_el_bloqueo` | Sí |
| Sin vínculo vigente con `reside`, la alfa lo impide | `test_sin_vivir_en_la_unidad_elegida_la_alfa_lo_impide` | Sí |
| Una unidad en mora no puede pedir un área no esencial | `test_una_unidad_en_mora_no_pide_un_area_no_esencial_pero_si_una_esencial` y `test_paz_y_salvo_solo_restringe_areas_no_esenciales` | Sí |
| Queda registrado qué reglas se evaluaron y con qué resultado | `test_queda_registrado_que_reglas_se_evaluaron_y_con_que_resultado` | Sí |
| Pruebas por cada tipo de regla | `test_cada_tipo_cumple_o_no_segun_sus_parametros` (5 tipos), `test_el_cupo_por_unidad_cuenta_las_apartadas_de_la_ventana` y la de paz y salvo | Sí |

Extras: enviar vencida → `EXPIRADA` y 409; la de otra persona → 404; dos veces → 409; sin motivo o con 0 asistentes → 400. Las alfas de piscina y de cobro quedan fuera: no hay datos con qué evaluarlas.

#### HU-01 · Inicio de sesión con correo y contraseña — 4 de 5 tareas

| Tarea técnica (Notion) | Estado | Evidencia |
|---|---|---|
| Modelo Usuario y hash de contraseña (backend) | Hecha | `apps/cuentas/models.py`, `962853f`. Contraseña con el hash de Django, login por correo sin distinguir mayúsculas |
| Endpoint `POST /auth/login` con emisión de token de sesión | Hecha | `POST /auth/login/`, `0b0c4f8` |
| Flujo de recuperación de contraseña por SMTP | Pendiente | — |
| Pantalla de login y manejo de errores (frontend) | Hecha | `557bc9f`. `apps/cuentas/` y `cliente_api/` del front: errores por campo, mensaje genérico y aviso si la API no responde. Verificada contra el backend real con el usuario de prueba |
| Pruebas unitarias de autenticación y expiración de token | Hecha | 11 pruebas en `apps/cuentas/tests.py`, `0b0c4f8` |

| Criterio de aceptación | Estado |
|---|---|
| Con credenciales válidas accede y ve el selector de conjunto activo | Entra por la pantalla del front y llega al selector, pero **el selector es maqueta**: no usa `GET /auth/conjuntos/` ni el `conjunto_activo` del login |
| Con credenciales inválidas ve un mensaje genérico sin revelar si el correo existe | Hecho y probado en la API; la pantalla muestra ese mismo mensaje (verificado, `557bc9f`) |
| Un usuario desactivado no puede entrar | Hecho y probado, también si se desactiva la persona o se desactiva con la sesión abierta |
| Quien olvidó la contraseña recibe un enlace de un solo uso por correo | Pendiente |
| Con un token vencido el sistema exige iniciar sesión de nuevo | Hecho y probado en la API (401). En el front la sesión vence a la misma hora que el token y vuelve al ingreso (verificado, `557bc9f`) |

#### HU-03 · Asistente por pasos para crear un conjunto — 1 de 5 tareas

| Tarea técnica (Notion) | Estado | Evidencia |
|---|---|---|
| Modelo Conjunto con campo `activo` y `conjunto_id NOT NULL` en toda tabla salvo las globales declaradas | Hecha | `apps/conjuntos/models.py` (`activo`, y `operativo`, que nace en falso). El `NOT NULL` lo imponen `ModeloDeConjunto` y la prueba transversal |
| Endpoints del asistente por pasos con guardado parcial | Pendiente | — |
| Validación de mínimos para marcar el conjunto como operativo | Pendiente | — |
| Asistente multipaso en frontend con resumen final | Pendiente | — |
| Pruebas del invariante: conjunto incompleto no queda operativo | Pendiente | Solo hay prueba de que un conjunto nuevo nace no operativo |

Ningún criterio de aceptación se cumple todavía: todos dependen del asistente, de áreas, reglamento, reglas beta o auditoría. El permiso `conjunto.crear` ya existe en el catálogo. En el plan del Sprint 1 entra como "HU-03 mínima" (paso 7), con el alcance por decidir (§6).

#### HU-02 · Segundo factor (TOTP) para permisos sensibles — 1 de 5 tareas

| Tarea técnica (Notion) | Estado | Evidencia |
|---|---|---|
| Marcar permisos sensibles en el catálogo fijo (backend) | Hecha | `PERMISOS_SENSIBLES` en `apps/permisos/catalogo.py`, `531e854`: 18 permisos, todos los de plataforma incluidos |
| Generación de secreto TOTP y código QR de vinculación | Pendiente | — |
| Verificación del código en el login y códigos de respaldo | Pendiente | `TokenDeSesion` ya tiene el campo `dos_factores_verificado`, sin uso |
| Pantallas de activación y de verificación (frontend) | Pendiente | — |
| Pruebas: usuario con permiso sensible no puede operar sin 2FA activo | Pendiente | — |

| Criterio de aceptación | Estado |
|---|---|
| Con un permiso sensible y sin 2FA configurado, debe configurarlo antes de continuar | Pendiente |
| Con 2FA activo y un código válido, accede | Pendiente |
| Un código expirado o repetido se rechaza | Pendiente |
| Un usuario solo con rol Residente no necesita 2FA | Preparado: hay prueba de que Residente no tiene permisos sensibles. Falta el flujo de 2FA |
| Un Superusuario siempre necesita 2FA | Preparado: todos los permisos de plataforma son sensibles. Falta el flujo de 2FA |

---

## 6. Lo que frena el avance

**Decisiones de equipo:**
- [ ] Fecha exacta de entrega y qué historias entran en el mes (maestro §12.8). Sin esto no se puede planear el Sprint 1
- [ ] Stack del frontend (maestro §12.1). Desde el 2026-09-15 el front ya está construido sobre plantillas de Django; si el equipo cierra por otro camino, se rehace
- [ ] ¿Reglas y anuncios se pueden eliminar? Las maquetas quitaron "Eliminar" del borrador hasta decidirlo (§4)
- [ ] Alcance de "HU-03 mínima" (paso 7). Propuesta del agente: crear el conjunto con sus datos básicos y asignarle administrador, dejando la validación completa de activación para cuando existan áreas, reglamento y reglas
- [ ] Confirmar que `vigencia_hasta` es **el primer día sin el rol** (así está en `Asignacion.objects.vigentes()`): con la fecha de hoy, el rol se pierde de inmediato
- [ ] ¿Se ocultan del selector los conjuntos no operativos? Hoy el selector solo excluye los desactivados, como dice HU-26
- [ ] Pasar HU-05 a "En revisión" en Notion cuando exista el PR `desarrollo → pruebas`

**Choques entre el esquema de diseño (base `admind`) y el maestro**, a decidir antes de construir la app que los toca:
- [x] `asignacion.conjunto_id` es `NOT NULL`, pero el maestro lo deja nulo para el Superusuario (§5.3) — resuelto el 2026-09-15 a favor del maestro (§4)
- [x] Roles y permisos como tablas, contra "catálogos fijos en código" (§5.3) — resuelto el 2026-09-15 a favor del maestro (§4)
- [ ] Estados de `reserva` con nombres distintos a los del maestro — app `reservas`
- [ ] `area_comun` sin `clasificacion` (§3.1) — app `areas`
- [ ] No hay tablas de reglas (§5.10) ni de notificaciones
- [ ] Columnas `registrado_por`, `decidido_por`, `priorizado_por` y `anulado_por` sin FK ni destino claro (¿persona o usuario?). Mientras tanto `Asignacion` se creó sin `registrado_por`
- [ ] `auditoria` sin `via_superusuario` (§5.3)

**Diferencias entre el código y el maestro**, a llevar al maestro o corregir en el código:
- [ ] Lista cerrada de tablas globales: el código agrega `conjuntos_conjunto`, `cuentas_tokendesesion`, `cuentas_usuario_groups` y `cuentas_usuario_user_permissions`, y admite `conjunto_id` nulo en `permisos_asignacion`. El maestro §5.4 solo nombra `Persona`, `Usuario` y los catálogos de roles y permisos, y su R12 todavía dice "falta escribir la lista cerrada"
- [ ] Reparto de permisos por rol en `catalogo.py`: interpretado del maestro §5.3, provisional hasta validarlo con un administrador real (maestro §11.4)
- [ ] Maestro §12.7 b (token contra sesión): resuelto en el código a favor del token con registro en la base (§4). Falta cerrarlo en el maestro y en los README de `cliente_api/` y `config/` del front, que lo siguen teniendo como pendiente aunque el front ya lo implementa
- [ ] El maestro §5.4 y §7.2 hablan de "middleware"; en el código es `VistaDeConjunto` (§4)
- [ ] El README de `apps/conjuntos` dice que ahí va el cambio de conjunto activo; quedó en `apps/cuentas`
- [ ] HU-26 pide logo y color en el selector; están fuera de v1 (maestro §6.3, ya registrado en §12.3)
- [ ] Quedaron desactualizados el README raíz del front ("Todavía no hay código") y la Guía de desarrollo §13 ("el proyecto Django del frontend no existe")

**Del plan de los Sprints 2 y 3 (2026-09-27):**
- [ ] Revisar los 15 commits del backend y los 9 del front, y subirlos (el agente no hace push)
- [ ] Volver a crear la rama `pruebas` del backend en GitHub y abrir los PR `desarrollo → pruebas`, revisados por quien no programó (plan §5)
- [ ] Prueba manual de HU-06 a HU-13 con el guion del plan §6, por quien no las programó. El agente no pudo recorrerlas en el navegador: pide iniciar sesión con las cuentas de prueba
- [ ] Llevar al maestro D2 (`LIBERADA`), D3 (bloqueo por conjunto) y D4 (catálogo beta y versionado): §5.1, §5.10 y §12.7 c
- [x] Notion: HU-06 a HU-13 en "En revisión", con casillas y nota de revisión; tareas 4 y 5 de HU-06 restauradas — hecho el 2026-09-27 17:50
- [ ] `alpine.min.js` se versionó con `core.autocrlf=true`: en otra máquina con Windows el archivo puede quedar con CRLF y su SHA-256 no coincidir con el del README de `vendor/`. Un `.gitattributes` con `*.js -text` para `vendor/` lo evitaría
- [ ] El límite de búsquedas cuenta por conjunto: un administrador de dos conjuntos puede hacer 20 en cada uno. Decidir si debe ser global
- [ ] Fuera del plan, sin hacer: la lista, el detalle y el alta de usuarios del front no sobreescribían `estado_vista` y mostraban "Maqueta"; se corrigió en la lista y el detalle porque el plan las tocaba, pero `usuarios/nuevo.html` sigue mostrándola

**Técnicos:**
- [x] Commit del paso 6 del backend (selector, `VistaDeConjunto`, permisos efectivos, prueba del intruso) — `d9b6271`
- [x] Subir `81f6298` y la actualización de las 09:00 del repositorio de documentación — `c556285`, en `origin/main`
- [ ] Commit y subida de las actualizaciones de las 09:25, las 10:13 y las 10:35 de este archivo
- [x] Commit del front (proyecto, login y maquetas) — `557bc9f`, en `origin/desarrollo`. El mensaje no lleva `[HU-01]`
- [ ] Pruebas automáticas del front en `tests/` (`pytest-django` con la API simulada). Hoy solo existe un script fuera del repositorio
- [x] En Notion: marcar la tarea "Pantalla de login y manejo de errores" de HU-01 — hecho el 2026-09-15 10:34
- [ ] Conectar el selector a la API (`GET /auth/conjuntos/`, `POST /auth/conjunto-activo/`) y mostrar el conjunto activo real en la barra. Para probarlo, el usuario de prueba necesita un conjunto y una asignación
- [ ] Camilo: crear el `.venv` del front, instalar `requirements.txt` y armar su `.env` a partir de `.env _ejemplo`
- [ ] Decidir con Camilo qué pasa con `index.html` y `apps/Administrador/Home.html` del front: HTML de prueba fuera de la estructura (§2.4)
- [ ] **Contraseñas en los repositorios**: `.env _ejemplo` del backend trae un valor en `DB_PASSWORD`, y el repositorio de documentación versiona `Credenciales/`. Quitarlas no las borra del historial: hay que cambiar la contraseña
- [x] Subir a `origin/desarrollo` los commits del backend — `desarrollo` al día hasta `d9b6271`
- [x] Instalar `pytest` y `pytest-django` y escribir las pruebas de HU-04 — `dc6a414`
- [ ] Declarar la capa de servicios en `apps/README.md`, que todavía describe el flujo vista → modelo. Ya hay `servicios.py` en `cuentas` y `permisos`
- [x] Commit de este archivo y de los cambios del maestro en el repositorio de documentación — `b08754f`
- [x] En Notion: pasar a "En progreso" las historias con avance (ninguna a Terminada, aunque los mensajes de commit digan "completada" o "hechos") — HU-01, HU-03, HU-04, HU-05 y HU-06 a las 05:55; HU-02 y HU-26 a las 09:00
- [x] En Notion: corregir la lista de tipos de documento de HU-04 — hecho el 2026-09-15
- [x] En Notion: marcar las tareas técnicas hechas — hecho el 2026-09-15 09:00
- [ ] Darle `CREATEDB` al `admind_user` de Camilo y correr `migrate` en su máquina: sin eso `pytest` no puede crear la base de pruebas
- [ ] Clase de permiso por vista ("esta vista exige `reserva.aprobar`"): hoy ninguna vista exige un permiso concreto (HU-06)
- [ ] Recuperación de contraseña por correo (HU-01; en el front es maqueta) y flujo de 2FA (HU-02)
- [ ] Comando que borre los tokens vencidos: dejan de servir, pero se acumulan en `cuentas_tokendesesion`
- [ ] Índices compuestos `(conjunto_id, …)` para consultas concretas, con cada tabla del producto que herede de `ModeloDeConjunto`
- [x] Paso 5 del plan del Sprint 1: login con token — `0b0c4f8`

**Límites conocidos del aislamiento** (no son errores, pero hay que tenerlos presentes):
- `bulk_create()` y `update()` se saltan `save()`, así que no validan que la fila sea del conjunto activo. La FK compuesta sigue impidiendo apuntar a otro conjunto, pero no protege el `conjunto_id` de la propia fila
- `Asignacion` no hereda de `ModeloDeConjunto` (su conjunto puede ser nulo): sus consultas no se filtran solas por el conjunto activo
- `ManagerDeConjunto` falla sin conjunto activo. En una petición lo fija `VistaDeConjunto`; el admin de Django, el `shell` o un script necesitan `usar_conjunto()`
- Una vista con datos de un conjunto que no herede de `VistaDeConjunto` falla con error 500 (no hay conjunto activo), y la prueba transversal de rutas la marca como no registrada
- `reserva.area` y demás relaciones hacia adelante no pasan por el filtro (Django usa su manager interno); la FK compuesta garantiza que son del mismo conjunto

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
