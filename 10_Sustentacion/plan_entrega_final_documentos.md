---
titulo: "Entrega final · tres documentos adicionales (metodología ágil, código y despliegue)"
alcance: "Estructura y prompts para que Sonnet arme tres Word: Metodología Ágil (Notion), Entrega del código y Despliegue (entrega final)"
punto_de_partida: "Notion leído el 2026-11-18 (página editada por última vez el 14-nov; filas de sprints revisadas el 17-nov). GitHub: Backend main 2dd5c44 (18 PR fundidos, 1 cerrado), Frontend main 10e2d04 (11 PR fundidos). VPS revisado por SSH en modo solo lectura el 2026-11-18: lo desplegado es igual a main en los dos repos."
resumen: "Plan de los tres documentos de la entrega final, con los datos ya investigados y un prompt para Sonnet por documento."
estado: activo
---

# Plan: tres documentos de la entrega final

Los tres Word salen con el **mismo estilo** que los de la F0 ([estilo_entregables](estilo_entregables.md)), con dos cambios que pidió Alejo:

- **Sin fechas**, ni en la portada ni en el texto. Los sprints se nombran por número, sin fechas.
- El **título** de cada documento es exactamente el que dio Alejo.

| N | Título (exacto) | Archivo | Largo |
|---|---|---|---|
| 1 | Entrega Documentación Metodología Ágil | `Entrega_Documentacion_Metodologia_Agil.docx` / `.pdf` | 8 páginas como máximo |
| 2 | Entrega del Código del Proyecto | `Entrega_Codigo_del_Proyecto.docx` / `.pdf` | 3 páginas como máximo |
| 3 | Despliegue de Aplicaciones Empresariales - Entrega Final Proyecto de Curso | `Despliegue_Entrega_Final_Proyecto.docx` / `.pdf` | 10 a 14 páginas |

**Salida:** `C:\Users\Alejandro\Documents\A D M I N D\Entregables_Sustentacion\Entrega_Final\` (crearla si no existe).

**Integrantes** (en mayúsculas, uno por línea): MANUEL ALEJANDRO ALDANA RINCON y ANDERSON CAMILO REMISO NIÑO.

**Cómo se arma el Word:** igual que el Manual Técnico. El generador propio está en `Entregables_Sustentacion\_generador_manual_tecnico\` (`ooxml.py`, con la clase `Doc`: `h1`, `h2`, `p`, `vinetas`, `tabla`, `nota`, `indice`, imágenes e hipervínculos). El PDF se exporta con `exportar.ps1` (Word por COM). No hay `python-docx` y **no se instala nada**.

---

## Antes de empezar (lo hace Alejo)

1. **Ordenar Notion antes de las capturas.** Hoy el tablero tiene cosas que se ven raras en un informe:
   - El Sprint 5 dice *En curso* y los Sprints 6, 7 y 8 dicen *Planificado*. Los Sprints 5, 6 y 7 deberían quedar *Cerrados* y el 8 *En curso* o *Cerrado*.
   - Hay dos historias numeradas **HU-40** («Mejorar Visual en General» en el Sprint 7 y «Implementar accesibilidad» en el Sprint 8).
   - Hay una fila de prueba llamada **«Prueba»**, sin sprint.
   - En el Sprint 8, HU-48 (procedimientos y triggers) y HU-49 (reportes) siguen en *En progreso*, pero ya están en `main` y desplegadas.
   - Las HU del Sprint 8 no tienen story points.
2. **Tomar las capturas** del tablero (lista en el documento 1) y guardarlas en `Entregables_Sustentacion\Entrega_Final\capturas\`.
3. **El QR** ya está copiado en `Entregables_Sustentacion\capturas\qr_admind.png`. Escanearlo con el celular para confirmar que abre `https://admind.detkor.com`.

---

## Documento 1 · Entrega Documentación Metodología Ágil

### Datos investigados (Notion, leído el 2026-11-18)

**Tablero público:** https://useful-vest-416.notion.site/Seguimiento-Scrum-2-0-AdMind-3f1739efa3338109b3f1e256d441de64

**Cómo está armado:** tres bases de datos relacionadas.
- **Historias de Usuario** (el Product Backlog): migrado del Excel V11.1 con 38 historias y sus story points del *poker planning*. Cada HU tiene prioridad, rol, story points, sprint, responsable, «Depende de» (relación con otras HU), avance calculado desde sus tareas, alerta y las dos casillas de la DoD.
- **Tareas**: cada HU se parte en tareas con estado (Sin empezar, En progreso, Bloqueada, Finalizada) y capa (Backend, Frontend o Pruebas). El responsable de la HU se hereda a sus tareas. Hay un kanban de tareas.
- **Sprints**: SP comprometidos, SP completados, % de cumplimiento, avance de tareas y la velocidad para planear el siguiente.

**Reglas del tablero:**
- Una HU solo suma SP en *Finalizado*, y solo llega ahí con la DoD marcada.
- **DoD humana:** PR `desarrollo → pruebas` revisado por el otro integrante y prueba manual hecha por quien no la programó.
- Lo que no se termina vuelve al backlog con sus SP intactos.
- **Velocidad:** el Sprint 1 se planeó con una base teórica de 81,7 SP (26,43 min/SP sobre 2160 min de capacidad); de ahí en adelante, con el promedio de SP completados de los sprints anteriores.
- La capa de cada tarea muestra si alguien se queda solo en backend o solo en frontend, para rotar.
- Una vista de alertas muestra solo lo incoherente.

**Sprints** (SP sumados de las HU; revisarlos contra el tablero ya ordenado):

| Sprint | HU | SP comprometidos | Estado de las HU hoy |
|---|---|---|---|
| 1 | HU-01, 02, 03, 04, 05, 26 | 25 | Todas finalizadas |
| 2 | HU-06, 07, 08, 09 | 20 | Todas finalizadas |
| 3 | HU-10, 11, 12, 13 | 26 | Todas finalizadas |
| 4 | HU-14, 15, 16, 17, 18, 19 | 28 | Todas finalizadas |
| 5 | HU-20, 21, 25, 27, 28, 29 y la mini HU «Tipos de zona (con y sin reserva)» | 33 | Finalizadas todas menos HU-20 (sin empezar): 28 SP |
| 6 | HU-22, 23, 24, 30, 31, 32, 33, 34 | 38 | Finalizadas HU-24, 30 y 34 (11 SP); HU-22, 23, 31 y 33 en progreso; HU-32 sin empezar |
| 7 | HU-35, 36, 37, 38 y HU-40 «Mejorar Visual en General» (agregada) | 31 | Finalizadas HU-35 y HU-40 (12 SP); HU-36, 37 y 38 sin empezar |
| 8 | 19 HU: HU-39, HU-40 accesibilidad, HU-41 a HU-57 | Sin SP en las nuevas | Finalizadas HU-41 (pruebas, 94 % de cobertura), HU-42 (GitHub Actions) y HU-56 (manuales y diccionario); el resto en progreso o en revisión |

**Lo que pasó** (lo cuenta Alejo; el tablero lo respalda):
- Al principio costó avanzar y cerrar HU al 100 %. En el Sprint 1 el trabajo técnico terminó, pero quedó en 0 de 25 SP porque ninguna HU cumplía la DoD (faltaban el PR revisado y la prueba del otro; la rama `pruebas` ni existía en el backend).
- Las HU estaban **interrelacionadas**: por ejemplo, HU-03 (el asistente para crear un conjunto) cumplía 3 de 5 criterios porque dependía de áreas, reglamento, reglas beta y auditoría, que eran de otros sprints. Por eso el tablero tiene el campo «Depende de».
- Solo hacia el **Sprint 3** quedaron completas todas las HU del Sprint 1.
- Se **redistribuyeron** las HU y desde los **Sprints 4 y 5** fue mejor: el 4 cerró sus 6 HU y el 5, 6 de 7.
- Con lo nuevo del **PGC** (Proyecto de Gestión del Conocimiento: lo hace la universidad cada tres semestres, y este semestre pidió una sustentación de negocio del proyecto) y de la **sustentación técnica**, el **Sprint 7 creció** (entró HU-40, lo visual) y **apareció un Sprint 8** con 13 HU nuevas (HU-45 a HU-57): Sonar, despliegue, ajustes de producción, procedimientos y triggers, reportes, JWT, CORS, Swagger, correo en HTML, pantallas, bug de casos, documentación y presentación.

### Estructura (8 páginas como máximo)

0. **Portada** e índice corto.
1. **Introducción** (media página): Scrum con HU en story points, sprints y DoD; Notion como herramienta de seguimiento; el enlace público del tablero como hipervínculo.
2. **Cómo está organizado el tablero** (1 página): las tres bases y cómo se relacionan, con un esquema simple (tabla de tres columnas o diagrama de cajas). Captura **M01** (vista general).
3. **Reglas de trabajo y Definition of Done** (media página): las reglas de arriba en viñetas. Captura **M02** (una HU abierta con sus tareas y las casillas de la DoD).
4. **Planeación**: backlog, poker planning y velocidad (media página). Captura **M03** (el backlog).
5. **Desarrollo por sprint** (2 a 3 páginas): la tabla de sprints y un párrafo por etapa:
   - Sprints 1 a 3: arranque difícil, HU interrelacionadas, la DoD que no se cumplía y el Sprint 1 completo solo hacia el Sprint 3.
   - Ajuste: redistribución de las HU.
   - Sprints 4 y 5: mejora.
   - Sprints 6 a 8: el crecimiento del Sprint 7 y el Sprint 8 por el PGC y la sustentación.
   - Capturas **M04** (vista de sprints con SP comprometidos y completados) y **M05** (kanban de tareas o el Sprint 8).
6. **Lecciones aprendidas** (media página): qué cambiamos y qué haríamos distinto. Por ejemplo, partir las HU para que no dependan de otro sprint, marcar las dependencias desde la planeación y hacer la DoD humana al cierre de cada HU y no al final del sprint.
7. **Enlace al tablero**: el link otra vez, como hipervínculo, en un recuadro.

**Capturas que toma Alejo** (en `Entrega_Final\capturas\`):

| N | Qué | Archivo |
|---|---|---|
| M01 | La página del tablero completa: el recuadro «Cómo se usa» y las bases | `M01_tablero.png` |
| M02 | Una HU abierta (por ejemplo HU-14), con tareas, avance y las dos casillas de la DoD | `M02_historia.png` |
| M03 | La tabla de Historias de Usuario con SP, sprint y estado | `M03_backlog.png` |
| M04 | La base de Sprints con SP comprometidos, completados y % de cumplimiento | `M04_sprints.png` |
| M05 | El kanban de tareas, o las HU del Sprint 8 | `M05_kanban.png` |

---

## Documento 2 · Entrega del Código del Proyecto

### Datos investigados (GitHub, 2026-11-18)

| Enlace | Qué es |
|---|---|
| https://github.com/ZeroFour-04/Admind_Backend | API REST. Django 5.2 + Django REST Framework 3.18 + PostgreSQL. 22 apps de dominio en `apps/` (cuentas, permisos, personas, conjuntos, unidades, áreas, reglas, reservas, triage, casos, citas, anuncios, documentos, infracciones, ingresos, visitantes, parqueaderos, pagos, notificaciones, reportes, auditoría…). Flujo por capas controlador → servicio → repositorio. 823 pruebas con 94 % de cobertura; funciones, un procedimiento y triggers de PostgreSQL en migraciones; reportes en PDF (reportlab) y Excel (openpyxl); correo en HTML; segundo factor (TOTP). Rama `main` en `2dd5c44`; 18 PR fundidos. |
| https://github.com/ZeroFour-04/Admind_Front-End | Interfaz web. Django con plantillas + Alpine.js, con el sistema de diseño de AdMind (componentes `am-*` y color por conjunto). No toca la base: habla con la API desde el servidor por `cliente_api`. Pantallas por rol (Superusuario, Administración, Secretaría, Residente y Vigilancia), menú según permisos y páginas de error propias. 523 pruebas. Rama `main` en `10e2d04`; 11 PR fundidos. |
| https://admind.detkor.com | La aplicación desplegada. |
| Pestaña *Actions* de cada repo | CI con GitHub Actions: en cada PR y cada `push` a `main` o `desarrollo` corre toda la suite (el back con PostgreSQL de verdad y la cobertura mínima del 70 %). |
| https://sonarcloud.io/project/overview?id=ZeroFour-04_Admind_Backend y `…id=ZeroFour-04_Admind_Front-End` | Análisis de calidad en SonarCloud (proyectos públicos). |

El repositorio de documentación (`ZeroFour-04/Admind_Documentacion`, público) **no va**, como en la F0, salvo que Alejo diga otra cosa.

### Estructura (3 páginas como máximo)

1. **Portada** (página 1).
2. **Página 2: Repositorios.** Una ficha por repositorio (Backend y Frontend): nombre, enlace como hipervínculo, tecnologías y un mini resumen de 4 a 6 líneas.
3. **Página 3: Otros enlaces y forma de trabajo.** Tabla corta con la app desplegada, *Actions* y SonarCloud, y un párrafo con el flujo de Git: ramas `main`, `desarrollo` y `pruebas`, una rama corta por cambio que entra por PR y el CI en verde antes de fundir.

Sin capturas: el límite es de 3 páginas.

---

## Documento 3 · Despliegue de Aplicaciones Empresariales - Entrega Final Proyecto de Curso

Debe cubrir lo que pide la entrega: **documentación final según la metodología, documento de sustentación, enlace de despliegue y fuente del proyecto**. Lo más largo es el despliegue.

### Datos investigados (VPS por SSH, solo lectura, 2026-11-18)

**Infraestructura**
- Máquina virtual en **Oracle Cloud**: Ubuntu 24.04.4 LTS, x86_64, 2 vCPU, ~1 GB de RAM y disco de 96 GB.
- Python 3.12.3 en el servidor (en local se desarrolla con 3.14).
- **PostgreSQL 16** en la misma máquina.

**Cómo corre cada proyecto** (servicios de `systemd`, usuario sin privilegios, `UMask=0077`, reinicio automático si falla):

| Servicio | Qué corre | Dónde escucha |
|---|---|---|
| `admind-backend` | gunicorn 27.0.1 con 2 workers, `config.wsgi`; arranca después de PostgreSQL | `127.0.0.1:8000`, solo dentro del servidor |
| `admind-front` | gunicorn 27.0.1 con 2 workers; estáticos con whitenoise 6.12 (comprimidos) | `127.0.0.1:8001` |
| `cloudflared` | Cloudflare Tunnel | Sale del servidor hacia Cloudflare; no abre puertos de entrada |
| `admind-webhook` | Receptor de webhooks de GitHub (Python estándar) | `127.0.0.1:8010` |
| `admind-deploy-queue` (`.path` + `.service`) | Procesa la cola de despliegues | — |

**Cómo llega una petición:** navegador → `https://admind.detkor.com` → Cloudflare (DNS, HTTPS y certificado en el borde) → túnel cifrado de `cloudflared` → gunicorn del front en `127.0.0.1:8001` → el front llama a la API en `127.0.0.1:8000` → PostgreSQL. **La API no se publica en internet**: solo el front la llama, desde dentro del servidor.

**Configuración de producción**, sin tocar los repos: cada servicio usa un módulo de settings propio en `/etc/admind/py/` que importa los settings del repo y sobrescribe:
- Front: `DEBUG = False`, `ALLOWED_HOSTS` con `admind.detkor.com`, `CSRF_TRUSTED_ORIGINS = https://admind.detkor.com`, `SECURE_PROXY_SSL_HEADER` con `X-Forwarded-Proto`, `SECURE_SSL_REDIRECT`, cookies de sesión y CSRF seguras, whitenoise y `STATIC_ROOT`.
- Back: `DEBUG = False`, `ALLOWED_HOSTS` solo `127.0.0.1` y `localhost`, y `STATIC_ROOT`.
- Las claves (base de datos, correo, `SECRET_KEY`) viven en el servidor, fuera de los repositorios.

**Despliegue continuo con cada `push` a `main`:**
1. GitHub manda un webhook a `https://deploy-admind.detkor.com/github`, que entra por el mismo túnel.
2. `server.py` valida la firma **HMAC SHA-256** con un secreto compartido. Solo acepta eventos `push` a `refs/heads/main` de los dos repos, descarta entregas repetidas, valida el commit y deja un trabajo en la cola (64 como máximo). Corre como un usuario dedicado (`admind-hook`) con el aislamiento de `systemd` (`ProtectSystem`, `NoNewPrivileges`…).
3. Una unidad `.path` de `systemd` detecta el trabajo y lanza `deploy_queue.py`, que corre el script del proyecto:
   - **Backend:** `git pull --ff-only origin main` → `pip install -r requirements.txt` → `migrate` → reinicio del servicio.
   - **Frontend:** `git pull --ff-only origin main` → `pip install` → `collectstatic` → reinicio del servicio.
4. Lo desplegado hoy es igual a `main`: back `2dd5c44`, front `10e2d04`.

**Acceso para el profesor**
- URL: https://admind.detkor.com, más el QR en `Entregables_Sustentacion\capturas\qr_admind.png`.
- Cuentas de demostración (sin segundo factor): `vigilante@gmail.com` (Vigilancia) y `prueba@gmail.com` (rol por confirmar con Alejo). Las contraseñas las da Alejo: no van en la bóveda, que es pública.

**Lo que NO va en el documento:** la IP del VPS, el usuario de SSH, la ruta de la llave ni ningún secreto. Tampoco se afirma nada del firewall que no se haya comprobado (no se pudo leer sin `sudo`).

### Estructura (10 a 14 páginas)

0. **Portada** e índice.
1. **Presentación del proyecto** (media página): qué es AdMind, los 5 roles y el problema que resuelve. Fuente: el Manual Técnico.
2. **Documentación final según la metodología** (1 página): Scrum en Notion (resumen del documento 1, con el link del tablero) y la tabla de entregables de documentación: Manual Técnico, Manual de Usuario, Diccionario de Datos, Metodología Ágil y Entrega del Código.
3. **Documento de sustentación** (1,5 páginas): tabla con los 12 criterios de la rúbrica, cómo se cumple cada uno y su evidencia (Sonar, despliegue, seguridad, base de datos, reportes, CORS y JWT, Swagger, correo, UX/UI y roles, cobertura, CI y documentación). **Lo que no esté hecho se escribe como no implementado, con la explicación técnica.** A la fecha del plan, JWT, CORS y Swagger no están en `main`. La respuesta que se dio: el token de sesión es opaco y vive en una tabla, así que cerrar sesión lo invalida de verdad; el navegador nunca llama a la API (la llama el front desde el servidor), así que CORS no entra en juego.
4. **Despliegue** (5 a 7 páginas, la parte central):
   - 4.1 Arquitectura de despliegue: un **diagrama nuevo** (ver el prompt) y su explicación.
   - 4.2 Infraestructura: tabla de la máquina y del software con sus versiones.
   - 4.3 Servicios del servidor: la tabla de `systemd`.
   - 4.4 Exposición a internet con Cloudflare Tunnel: por qué no se abren el 80 ni el 443, y dónde está el HTTPS.
   - 4.5 Configuración de producción: los módulos de settings y qué cambia frente a desarrollo.
   - 4.6 Despliegue continuo: el flujo webhook → cola → script, en una lista numerada o un diagrama de pasos, más la seguridad del webhook.
   - 4.7 Integración continua y calidad: GitHub Actions y SonarCloud antes de llegar a `main`.
   - 4.8 Seguridad del despliegue: un resumen en viñetas.
5. **Enlace de despliegue y acceso** (1 página): URL como hipervínculo, **el QR grande y centrado** (unos 5 cm), y la tabla de cuentas de demostración.
6. **Fuente del proyecto** (media página): los dos repositorios, como en el documento 2.

---

## Prompts para Sonnet

Se pegan uno por sesión, en orden. Cada uno es completo por sí solo.

### Prompt 1 · Metodología Ágil

```text
Vas a armar un documento Word para AdMind. Trabajas en C:\Users\Alejandro\Documents\A D M I N D.

Lee primero, y solo esto:
1. Documentacion\Admind_Documentacion\10_Sustentacion\plan_entrega_final_documentos.md → la sección "Documento 1" y el encabezado del plan.
2. Documentacion\Admind_Documentacion\10_Sustentacion\estilo_entregables.md → colores, fuentes, portada, encabezado, pie y tablas.
3. Entregables_Sustentacion\_generador_manual_tecnico\ → build.py, parte1.py (la portada) y ooxml.py (la clase Doc). Reutiliza ese generador: copia ooxml.py y exportar.ps1 a una carpeta nueva, Entregables_Sustentacion\Entrega_Final\_generador\, y escribe ahí tu propio build. No instales nada.

Qué hacer:
- Título exacto de la portada: "Entrega Documentación Metodología Ágil". Subtítulo: "AdMind — Plataforma de administración de conjuntos residenciales".
- Integrantes, en mayúsculas, uno por línea: MANUEL ALEJANDRO ALDANA RINCON y ANDERSON CAMILO REMISO NIÑO. Asignatura, docente y universidad como dice el estilo.
- SIN FECHAS en ninguna parte: ni en la portada, ni en el pie, ni en el texto, ni en los sprints. Quita la línea de fecha que trae parte1.py.
- Sigue la estructura del plan (secciones 0 a 7). 8 páginas como máximo, incluida la portada. Si te pasas, recorta texto, no capturas.
- El enlace del tablero de Notion va como hipervínculo en la introducción y otra vez al final, en un recuadro.
- El relato del avance lo cuenta el equipo en primera persona del plural ("al principio tuvimos…"). Tono honesto, no de excusa: hubo problemas al inicio, se entendió por qué (las HU dependían unas de otras y la DoD exigía PR revisado y prueba del otro) y se corrigió redistribuyendo; desde los Sprints 4 y 5 mejoró; el Sprint 7 creció y apareció el Sprint 8 por lo nuevo del PGC y la sustentación técnica. El PGC es el Proyecto de Gestión del Conocimiento de la universidad (se hace cada tres semestres); este semestre pidió una sustentación de negocio de AdMind. Menciónalo de pasada, en una sola frase, como una de las razones de la carga extra: la primera vez, con el nombre completo y la sigla entre paréntesis, y no le dediques una sección.
- La tabla de sprints: usa la del plan. Si en Entregables_Sustentacion\Entrega_Final\capturas\ la captura M04 muestra cifras distintas, mandan las de la captura; avísame cuáles cambiaste.
- Capturas: M01 a M05 en Entregables_Sustentacion\Entrega_Final\capturas\, cada una con un pie de figura que diga qué muestra. Si falta alguna, deja un recuadro ámbar "Captura pendiente: <qué va>" en su lugar y avísame al final.
- Todas las páginas en carta vertical.

Salida: Entregables_Sustentacion\Entrega_Final\Entrega_Documentacion_Metodologia_Agil.docx, y el PDF con el mismo nombre (exportar.ps1). Abre el PDF y confirma: número de páginas (máximo 8), que el enlace de Notion abre y que no aparece ninguna fecha.

No toques Notion, los repositorios ni la bóveda. No hagas commits.
```

### Prompt 2 · Entrega del código

```text
Vas a armar un documento Word corto para AdMind. Trabajas en C:\Users\Alejandro\Documents\A D M I N D.

Lee primero, y solo esto:
1. Documentacion\Admind_Documentacion\10_Sustentacion\plan_entrega_final_documentos.md → la sección "Documento 2" y el encabezado del plan.
2. Documentacion\Admind_Documentacion\10_Sustentacion\estilo_entregables.md.
3. Si ya existe Entregables_Sustentacion\Entrega_Final\_generador\ (del documento de metodología), reutilízalo. Si no, copia ooxml.py y exportar.ps1 desde Entregables_Sustentacion\_generador_manual_tecnico\ a esa carpeta. No instales nada.

Qué hacer:
- Título exacto de la portada: "Entrega del Código del Proyecto". Mismo subtítulo, integrantes (MANUEL ALEJANDRO ALDANA RINCON y ANDERSON CAMILO REMISO NIÑO, en mayúsculas, uno por línea), asignatura, docente y universidad que el estilo. SIN FECHAS.
- 3 páginas como máximo: página 1, la portada; página 2, una ficha por repositorio (Backend y Frontend) con enlace, tecnologías y un mini resumen de 4 a 6 líneas; página 3, otros enlaces (app desplegada, GitHub Actions, SonarCloud) y un párrafo del flujo de Git. Sin índice: con tres páginas no hace falta.
- Usa los datos del plan. Antes de escribir los números, compruébalos con gh:
  gh pr list -R ZeroFour-04/Admind_Backend --state merged --limit 200 --json number -q length
  (y lo mismo con Admind_Front-End), y el último commit de main de cada uno. Si cambiaron, usa los nuevos.
- Todos los enlaces como hipervínculos que se puedan pulsar en el PDF.

Salida: Entregables_Sustentacion\Entrega_Final\Entrega_Codigo_del_Proyecto.docx y su PDF. Confirma que son 3 páginas o menos y que cada enlace abre.

No toques los repositorios ni la bóveda. No hagas commits.
```

### Prompt 3 · Despliegue (entrega final)

```text
Vas a armar el documento de la entrega final de AdMind para la materia Despliegue de Aplicaciones Empresariales. Trabajas en C:\Users\Alejandro\Documents\A D M I N D.

Lee primero, y solo esto:
1. Documentacion\Admind_Documentacion\10_Sustentacion\plan_entrega_final_documentos.md → la sección "Documento 3" completa y el encabezado del plan. Ahí están todos los datos del servidor, ya investigados: no entres al VPS.
2. Documentacion\Admind_Documentacion\10_Sustentacion\estilo_entregables.md.
3. Documentacion\Admind_Documentacion\10_Sustentacion\tareas.md → solo el recuadro "Estado el martes 17-nov a las 10:00" y la tabla de evidencias del final (los 12 criterios).
4. Entregables_Sustentacion\Documentacion_Entregable\AdMind_Manual_Tecnico.pdf → solo la introducción, para la presentación del proyecto.
5. El generador: si existe Entregables_Sustentacion\Entrega_Final\_generador\, reutilízalo; si no, copia ooxml.py y exportar.ps1 desde Entregables_Sustentacion\_generador_manual_tecnico\. No instales nada.

Qué hacer:
- Título exacto de la portada: "Despliegue de Aplicaciones Empresariales - Entrega Final Proyecto de Curso". Mismo subtítulo, integrantes (MANUEL ALEJANDRO ALDANA RINCON y ANDERSON CAMILO REMISO NIÑO, en mayúsculas, uno por línea), asignatura, docente y universidad que el estilo. SIN FECHAS en ninguna parte.
- Sigue la estructura del plan (secciones 0 a 6), entre 10 y 14 páginas, carta vertical.
- La sección 4 (Despliegue) es la más importante: explícala para un profesor técnico. Cada decisión con su porqué (por ejemplo: con Cloudflare Tunnel no hace falta abrir el 80 ni el 443; la API escucha solo en 127.0.0.1 y no se publica; los settings de producción viven fuera del repo para no subir secretos; el webhook valida la firma HMAC antes de desplegar).
- Diagrama de despliegue NUEVO para la sección 4.1: Navegador → Cloudflare (DNS + HTTPS) → túnel cloudflared → VPS Oracle Cloud [gunicorn front :8001 (whitenoise) → gunicorn API :8000 → PostgreSQL 16], y aparte GitHub (push a main) → webhook deploy-admind.detkor.com → cola → scripts de despliegue. Hazlo con el mismo estilo de Sustentacion_2026-10-30\Diagramas\fuentes\componentes.py (SVG a PNG con cairosvg). Si cairosvg no está disponible en ningún venv, NO lo instales: dibuja el flujo como una tabla de pasos en el Word y avísame.
- Sección 3 (sustentación): tabla Criterio | Cómo se cumple | Evidencia. Lo que no está hecho se escribe como "No implementado", con la explicación técnica del plan. Nunca lo marques como hecho. Antes de escribirla, comprueba con gh si en main de los dos repos ya hay algo de JWT (PyJWT), CORS (corsheaders) o Swagger (drf-spectacular), buscando en requirements.txt. Si apareció, márcalo como hecho y dime qué cambió.
- Sección 5: el enlace https://admind.detkor.com como hipervínculo; el QR de Entregables_Sustentacion\capturas\qr_admind.png centrado, de unos 5 cm, con el pie "Escanee para abrir AdMind"; y la tabla de cuentas: vigilante@gmail.com (Vigilancia) y prueba@gmail.com, con las contraseñas que te dé Alejo (pon el rol que te dé Alejo; si no te lo dio, pregúntale antes de exportar).
- PROHIBIDO poner en el documento: la IP del servidor, el usuario o la llave de SSH, rutas de claves, secretos o tokens. No afirmes nada del firewall ni de los puertos de PostgreSQL que no esté en el plan.
- Versiones exactas del plan (Ubuntu 24.04.4, Python 3.12.3 en el servidor, Django 5.2.17, DRF 3.18.1, gunicorn 27.0.1, whitenoise 6.12.0, psycopg 3.3.5, PostgreSQL 16).

Salida: Entregables_Sustentacion\Entrega_Final\Despliegue_Entrega_Final_Proyecto.docx y su PDF. Confirma: número de páginas, que los enlaces abren, que el QR se ve nítido y que no hay fechas ni datos del servidor que no deban estar.

No toques el VPS, los repositorios ni la bóveda. No hagas commits.
```

## Ver también

- [estilo_entregables](estilo_entregables.md) — el estilo común de los Word
- [plan_F0_tablero_y_repos](plan_F0_tablero_y_repos.md) — el entregable de tablero y repositorios de la F0, que este plan amplía
- [tareas](tareas.md) — el estado de los 12 criterios de la rúbrica
