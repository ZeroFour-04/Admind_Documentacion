---
resumen: "Bitácora del proyecto: una fila por hecho, con fecha, hora, repositorio y commit. Lo más reciente abajo."
tipo: estado
origen: "avance §3"
actualizado: 2026-10-05
---

# Bitácora

Lo más reciente abajo. Solo hechos; los errores con su aprendizaje van en `Archivo/Lab/Admind_Bitacora_Errores.md`, que escribe Alejo.

En las filas anteriores al 2026-09-30, *este archivo* es el antiguo `Admind_Avance.md`, *el plan* es `07_Planes/hechos/Admind_Plan_Sprints_2_3.md` y las citas *§N* a secas son de ese archivo ([pendientes](pendientes.md) es su §6; [historias_evidencia](historias_evidencia.md), su §5.3).

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
| 2026-09-30 | Documentación | La bóveda se reorganiza en carpetas numeradas con routers (`AGENTS.md`, `CLAUDE.md`), índice (`README.md`) y protocolos. El maestro y `Admind_Avance.md` se parten en notas cortas; lo histórico pasa a `Archivo/` |
| 2026-10-04 | Frontend | Ícono de la pestaña: el de AdMind por defecto (`static/img/`) y la foto del conjunto activo cuando la tiene (`base.html`). 3 pruebas nuevas, 150 en verde. Sin commit |
| 2026-10-05 | Backend y Frontend | HU-01: `/auth/recuperar/` limita a 3 enlaces por hora por correo (429 igual exista o no la cuenta, `apps/cuentas/limites.py`); el front muestra el `detail` de un 429 y tiene 10 pruebas de las dos pantallas de recuperación; el correo llegó a una bandeja real por SMTP. Back 334 pruebas (333 pasan, 1 falla la conocida), Front 160. Sin commit |
