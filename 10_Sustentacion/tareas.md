---
resumen: "Lista de tareas conjunta de Alejo y Camilo para la sustentación final (era el 17-nov; se movió al lunes 23-nov), lista para pegar en Notion."
tipo: plan
origen: "rúbrica del profesor (clase del 3-nov) contrastada con el código el 2026-11-14 (Backend b89d9f2, Frontend bdcb5c3); lista final de Notion del 2026-11-16, contrastada con GitHub ese día a las 14:16 (Backend main 1d603ba, Frontend main 0d806dc) auditada otra vez a las 20:10 con gh, las pruebas locales y la versión en la nube, y revisada a las 23:45 después de fundir los PR de la noche (Backend main 105e69c, Frontend main 664f960); auditada el 17-nov a las 10:00 con gh y la versión en la nube (Backend main 2dd5c44, Frontend main 10e2d04)"
actualizado: 2026-11-19
revisado: 2026-11-17
---

# Tareas para la sustentación final de AdMind

> Para Notion: copiar desde este título hacia abajo.

**Fechas:** documentación al aula **sábado 14-nov antes de las 18:00** (✅ **entregada el sábado en la tarde**). Sustentación **martes 17-nov desde las 10:15**, unos 15 minutos.

> [!IMPORTANT] La sustentación se movió al lunes 23-nov (dicho por Alejo el 18-nov)
> Esta lista se escribió para el 17-nov: sus «lunes en la noche» y «martes temprano» ya no son esos días, y la hora nueva no está confirmada. Lo vigente sobre la fecha, la rúbrica y el estado está en [sustentacion_tecnica](sustentacion_tecnica.md).

> [!IMPORTANT] Estado el martes 17-nov a las 10:00 (auditado con `gh` y contra la nube)
> - **Se pueden mostrar 10 de 12 criterios:** UX/UI, roles, cobertura, CI, seguridad, correo, despliegue del front, base de datos, reportes y Sonar. **Siguen en cero 2:** CORS y JWT (C8, C9) y Swagger (C10).
> - **Entró a `main` esta mañana** (PR #17 y #18 del back, #10 y #11 del front, todos con el CI en verde):
>   - **C5:** 4 funciones (`fn_ocupacion_areas`, `fn_resumen_casos`, `fn_aforo_actual`, `fn_estado_pagos`), 1 procedimiento (`sp_expirar_bloqueos_vencidos`) y 5 triggers. Cuatro son el mismo `trg_sin_borrado_fisico` en casos, infracciones, pagos y reservas, y el quinto es `trg_infraccion_anulada_inmutable`. No son los del plan de abajo: saber explicar por qué 4 son funciones y 1 es procedimiento.
>   - **C6:** reportes PDF (`reportlab`) y Excel (`openpyxl`) de zonas, pagos y reservas en el back, y la pantalla `/reportes/` en el front (commit `0c05d6f` de Camilo).
>   - **C3:** en los dos repos `DEBUG` y `ALLOWED_HOSTS` salen del entorno, con cookies seguras, `SECURE_PROXY_SSL_HEADER`, `gunicorn`, `whitenoise` y `STATIC_ROOT`. El front manda `never_cache` cuando hay sesión, así que el botón Atrás no debería mostrar datos.
> - **C1:** SonarCloud analiza `main` de los dos repos (el check *SonarCloud Code Analysis* está en verde en el último commit; en el back hubo otro análisis en `105e69c`). No se pudo ver desde aquí cuántas vulnerabilidades marca ni si alguien arregló la suya (A3).
> - **La nube:** `https://admind.detkor.com` corre la versión nueva del front. El 404 es la página propia de A4, sin rastro de Django, y `/reportes/` existe (redirige al ingreso). **`api.admind.detkor.com` no resuelve en el DNS**: la API no es pública y no hay Swagger.
> - **Sin hacer:** C8, C9 y C10 (no hay `PyJWT`, `corsheaders` ni `drf-spectacular` en el código); C12 sin commit visible; ninguna rama protegida; la rama `Desarrollo` del front y las `revert-*` del back siguen en GitHub.
> - **Si el profe pregunta por lo que falta:** el token de sesión es opaco y vive en una tabla, por eso se puede cerrar sesión de verdad (C8 lo iba a volver JWT firmado). El navegador no llama a la API: el front de Django la llama desde el servidor, así que CORS no entra en juego hoy (comprobado: ninguna plantilla ni script del front hace `fetch` a la API).
> - **Ojo:** los PR #10, #11 y #13 del back fueron directo a `main`, fuera de la regla de "nada directo a `main`".

**Estado el lunes 16-nov a las 23:45:** de los 12 criterios de la rúbrica, 4 se pueden mostrar con evidencia (UX/UI, roles, cobertura y CI), 3 están a medias (seguridad, correo y despliegue) y 5 siguen en cero (CORS y JWT, Swagger, reportes, base de datos y Sonar). **Todo lo de Alejo (A2, A4, A7 y A10) y la rama `Desarrollo` del back de Camilo ya están en `main` de los dos repos, con el CI en verde.** Falta redesplegar: la nube sigue con la versión vieja. De C1, C3, C5, C6, C8, C9, C10 y C12 no hay nada en GitHub.

**Ya hay una versión desplegada** en el VPS de Oracle (verificado el 14-nov):
- **La URL es `https://admind.detkor.com`, sin `www`** (decidido el 14-nov). `www.admind.detkor.com` no existe en el DNS y no se va a crear: el QR, las diapositivas y la configuración usan la dirección sin `www`.
- Responde la pantalla de ingreso detrás de Cloudflare, `http` redirige a `https`, y una ruta inexistente da el 404 genérico de Django (`DEBUG` apagado).
- Ojo: en GitHub los `settings.py` todavía dicen `DEBUG = True`. Lo que corre en el servidor tiene cambios que no están en el repo; C3 tiene que subirlos.

> [!WARNING] Lo que hay en GitHub el lunes 16-nov a las 23:45 (auditado con `gh`)
> - **Los PR de la noche, todos fundidos con el CI en verde:**
>   - front: #7 `fix/ci-front` (A10) y #8 `fix/pantallas-sustentacion` (A4) a `desarrollo`, y #9 `desarrollo → main`. `main` del front queda en `664f960`, **en verde**, sin el 500 de `/solicitudes/`;
>   - back: #12 `fix/prueba-ingresos-hora`, #9 `test/cobertura` (A2), #14 `feat/correo-html` (A7) y #15 `Desarrollo` (Camilo: cita futura por conjunto y zona horaria) a `desarrollo`, y #16 `desarrollo → main`. `main` del back queda en `105e69c`, **en verde**, con la cobertura en el CI.
> - **La prueba que fallaba de noche** (`apps/ingresos/tests.py`, la de los motivos del 400) usaba el horario de 05:00 a 22:00 contra la hora real. Después de las 22:00 sumaba un tercer motivo y el CI fallaba. Se arregló en `fix/prueba-ingresos-hora` (`9ef4826`): la zona de esa prueba abre todo el día.
> - **Un tropiezo con `main` del back, ya resuelto:** el arreglo entró primero a `main` por error (#10), se revirtió (#11) y se volvió a poner revirtiendo el revert (#13). Si no se hubiera revertido el revert, al fundir `desarrollo → main` habría ganado el revert y el arreglo habría desaparecido sin aviso.
> - **En *Actions* ya hay historial**: una ejecución por cada PR y cada `push` a `main` o `desarrollo` de la noche.
> - **De Camilo no hay rama, PR ni commit de C1, C3, C5, C6, C8, C9, C10 ni C12.** `main` sigue con `DEBUG = True` y `ALLOWED_HOSTS = []` en los dos repos, y no tiene `gunicorn`, `whitenoise`, `corsheaders`, `PyJWT`, `drf-spectacular`, `reportlab` ni migraciones con triggers. En Notion, C3, C5 y C6 figuran como *Tal vez completada*.
> - **Ramas por limpiar:** `Desarrollo` en los dos repos (la del back ya entró; la del front no se funde, A4 la cubre), `revert-10-fix/prueba-ingresos-hora`, `revert-11-revert-10-fix/prueba-ingresos-hora`, y las ramas cortas ya fundidas. Ninguna rama está protegida.
> - Sonar (C1) sigue sin primer escaneo, así que ya no habrá "antes" con el `main` viejo: el primer escaneo será sobre el `main` de esta noche.
>
> **Pruebas locales a las 23:24:** el backend, en `test/cobertura` con `desarrollo` fundido, pasa las 823 pruebas, con 93,95 % de cobertura.
>
> **La nube a las 21:00:** el ingreso funciona, pero Administración entra a `/solicitudes/`, que da **500** porque corre el `main` viejo del front. Se arregla redesplegando el front desde `main`. `api.admind.detkor.com` no existe en el DNS y `https://admind.detkor.com/api/docs/` da 404. **El SSH al VPS (`143.47.112.182`, puerto 22) no responde desde el PC de Alejo**: ni el ping ni la conexión. Hay que revisar la *security list* de Oracle antes de redesplegar.

**Reglas para todo cambio de código:**
- Una tarea = una rama corta desde `desarrollo` = un PR a `desarrollo`. Nada directo a `main` (el 30/10 se subieron 6 commits del front y 1 del back directo a `main`; no repetirlo).
- Desde que exista el CI (tarea C2), ningún PR se funde con el CI en rojo.
- El lunes en la noche va un único PR `desarrollo → main`, y desde `main` se despliega.

**Orden que importa:**
1. ~~El primer escaneo de Sonar va antes de que algo más llegue a `main`.~~ Ya no aplica: la noche del 16-nov se fundió todo a `main` sin escaneo. El primer escaneo será sobre ese `main`, y la disminución se muestra con lo que se arregle después (C3, A3).
2. ✅ **CI con historial:** los PR de A2, A4, A7 y A10 se abrieron y fundieron la noche del 16-nov, cada uno con su ejecución en verde.
3. **El despliegue** sigue después, porque sin él no hay QR.
4. Lo demás, en el orden de la lista.

## Decisiones de los dos (tomadas el sábado 14-nov)

- [x] **JWT: híbrido.** El token pasa a ser un JWT firmado y la tabla de sesiones se queda para poder cerrar sesión (C8). No se migra a `simplejwt`.
- [x] **Reportes: solo Administración**, entre los roles de un conjunto. El Superusuario también los verá, porque el catálogo le da todos los permisos por diseño (C6).
- [x] **Cuentas demo para el profe:** Residente y Vigilancia, que no piden segundo factor. Superusuario, Administración y Secretaría los muestra el equipo desde su celular. Quedó la propuesta: no hubo objeción.
- [x] **Swagger en la nube: público** (C10). Muestra el contrato de la API, no datos.
- [x] **Nube: el VPS de Oracle**, no Render. La app ya está en `https://admind.detkor.com` (A9).
- [x] **Dirección sin `www`:** `https://admind.detkor.com` en el QR, las diapositivas y la configuración. No se crea el registro `www`.
- [x] **Reparto:**
  - Alejo hizo casi toda la documentación (A1). Toma el correo en HTML (A7), porque su Claude tiene más presente el diseño de AdMind, y el material de estudio (A6).
  - **El despliegue pasa a Alejo** (A9): Camilo no tiene acceso al VPS.
  - **Swagger se queda con Camilo** (C10).
  - **GitHub Actions pasa a Alejo** (A10, decidido el 16-nov). Camilo ya había montado los dos *workflows*; Alejo los lleva desde ahí.
  - Camilo lleva Sonar, los ajustes de producción en el código (C3), la base de datos, los reportes, JWT, CORS y Swagger.

---

## Alejo

> [!TIP] Orden para el martes 17-nov temprano, antes de las 10:15 (revisado a las 23:45 del 16-nov)
> 1. ✅ ~~Abrir y fundir los PR de lo que ya estaba hecho.~~ Hecho la noche del 16-nov: A2, A4, A7, A10 y la `Desarrollo` del back están en `main` de los dos repos, con el CI en verde.
> 2. **Redesplegar desde `main` (A9). Es lo primero:** la nube tiene el 500 de `/solicitudes/`, y Administración no puede entrar. Antes, recuperar el SSH: el puerto 22 de `143.47.112.182` no responde desde el PC de Alejo (revisar la *security list* de Oracle). En el VPS: `git pull` en los dos repos, `pip install -r requirements.txt`, `migrate` en el back, `collectstatic` y reiniciar los dos servicios. Probar entrando con Administración a `/solicitudes/?pestana=casos`.
> 3. **El primer escaneo de Sonar (C1)**, si Camilo no lo ha hecho.
> 4. **La presentación, el guion de la demostración y el plan B (A8).**
> 5. **El estudio (A6)**, con el recorte propuesto.
> 6. Si sobra tiempo: borrar las ramas sobrantes y proteger `desarrollo` y `main` (A10), A3 y A5 sobre la versión redesplegada.
> 7. **Después de la sustentación:** las dos GitHub Actions que se propusieron el 16-nov: el auto-merge hacia `desarrollo` solo con el CI en verde, y el despliegue al VPS con cada `push` a `main` (ver A10).

### A1. Documentación (F0) — ✅ entregada el sábado 14-nov
Fue el sábado entero, de la madrugada a la tarde. Los archivos y sus generadores están en `A D M I N D/Entregables_Sustentacion/`.

**Preparación**
- [x] Leer la rúbrica del profe (clase del 3-nov) y contrastarla criterio por criterio con el código. Resultado: 4 de 12 criterios bien, 1 a medias y 7 sin hacer. De ahí salió esta lista de tareas.
- [x] Definir el estilo común de los documentos: portada con logo, verde de AdMind, fuentes, encabezado y pie (`10_Sustentacion/estilo_entregables.md`).
- [x] Escribir un plan por entregable para ejecutarlo con Sonnet (`10_Sustentacion/plan_F0_*.md`).

**Diccionario de datos**
- [x] Sacarlo de la base real `admind_db`, no de los modelos. Son 42 tablas, 352 columnas, 42 llaves primarias, 111 foráneas, 45 únicas y 63 CHECK, con scripts que lo regeneran.
- [x] Escribir una descripción legible para las columnas del negocio.
- [x] Armarlo en Word (33 páginas) y además en Excel.

**Manual técnico**
- [x] Redactar requerimientos funcionales y no funcionales; arquitectura (dos servidores, capas, recorrido de una petición, aislamiento, concurrencia, motor de reglas, trazabilidad); seguridad; tecnologías; instalación y variables de entorno; pruebas y proceso.
- [x] Anexo con las 97 rutas reales de la API, sacadas del código y descritas una por una.
- [x] Armarlo en Word (40 páginas) y PDF.

**Manual de usuario**
- [x] Cargar datos de demostración en local: conjunto, viviendas, zonas, reglas, reservas, casos, anuncios, pagos, parqueaderos y visitantes.
- [x] Tomar 57 capturas, rol por rol, entrando con cada cuenta y con el segundo factor en las que lo piden.
- [x] Redactarlo por rol para el usuario final: 9 capítulos, 80 páginas y 57 figuras.
- [x] Revisar la app pantalla por pantalla. Salieron 7 fallas, que quedaron en A4, A7 y C12.

**Seguimiento y repositorios**
- [x] Actualizar el tablero de Notion y sacar el PDF de seguimiento Scrum.
- [x] Hacer el PDF con los enlaces a los dos repositorios.

**Entrega**
- [x] Ajustes finales: nombres en las portadas, todas las páginas en tamaño carta vertical y todo exportado a PDF.
- [x] Armar el `.zip` y subirlo al aula antes de las 18:00.

**Pendiente**
- [ ] Cuando entren los procedimientos y triggers (C5), regenerar el diccionario para mostrarlo en la sustentación (`10_Sustentacion/datos/scripts/` y `Entregables_Sustentacion/_generador_diccionario/`).

### A2. Cobertura de pruebas del backend (mínimo 70 %, demostrable) — hecho el 16-nov (rama `test/cobertura`, commit `9645752`, subida)
> **Resultado: 94,0 %** (sentencias y ramas, 823 pruebas sobre `main` `1d603ba`). No hizo falta escribir pruebas. Lo más bajo: `crear_usuarios_prueba` (0 %, comando de desarrollo), `conjuntos/imagenes.py` (71 %) y `citas/servicios.py` (84 %).
- [x] Rama `test/cobertura` desde `origin/main`. `pytest-cov` 7.1.0 y `coverage` 7.17.3 en `requirements.txt`.
- [x] `.coveragerc`: `apps/` sin `migrations/` ni archivos de pruebas, con ramas, y `fail_under = 70`. `config/settings_pruebas.py` no se tocó.
- [x] Corrida con `pytest --cov --cov-report=term --cov-report=html`. Captura en `Entregables_Sustentacion/evidencias/cobertura_back.png`. `htmlcov/` y `.coverage` quedan fuera del repo (`.gitignore`).
- [x] En el mismo commit, el CI del back corre con `--cov-fail-under=70` y sube `htmlcov/` como *artifact* `cobertura-backend` (la parte de A10).
- [x] Comprobado otra vez a las 20:10 del 16-nov: 823 pruebas, 94,0 %.
- [x] PR #9 `test/cobertura → desarrollo`, fundido el 16-nov a las 23:29 y llevado a `main` con el #16. El primer CI falló por la prueba de ingresos que dependía de la hora (ver arriba); con `desarrollo` fundido en la rama (`e5f7e9d`) pasó en verde. El paso de cobertura ya está en *Actions*.

### A3. Una vulnerabilidad de Sonar propia — hecha en código el 19-nov (rama `ci/endurecer-dependencias` en los dos repos, sin push)
> Las dos MAJOR de `ci.yml` (githubactions:S8541 y S8544), en los dos repos: el CI instala desde `requirements.lock` con `--require-hashes --only-binary :all:`. Back `12c2abd`, front `9ba725b`. Falta push, PR a `desarrollo`, llevarlo a `main` y ver el segundo escaneo.
- [x] La rúbrica exige que **cada integrante** corrija al menos una vulnerabilidad alta o media. Tomar una de la lista que deja Camilo en C1, en su propio PR.

### A4. Pantallas a prueba del profe — hecho en código el 16-nov (rama `fix/pantallas-sustentacion` en el front)
> Commit `7cf6863`. **En `main` desde el 16-nov a las 22:19** (PR #8 a `desarrollo` y #9 `desarrollo → main`, CI en verde). Sin revisar a mano en el navegador y **sin desplegar**: la nube sigue con el 404 genérico de Django. La rama `Desarrollo` del front no se fundió (ver A10). Decisiones y huecos al final de la sección.

Lo que encontró el manual de usuario el 14-nov, más lo de la revisión inicial:
- [x] **El Residente ve "Reglas" en el menú** y al abrirlo recibe "No tienes permiso…". La rúbrica dice que un rol no debe ni *ver* vistas de otro. Ocultar el ítem del lateral (`templates/componentes/lateral.html`) a quien no tenga `regla.ver`. Revisar de paso que **ningún** ítem del menú lleve a un "No tienes permiso" con ninguno de los 5 roles.
- [x] **La pestaña Casos del tablero se titula "Dashboard de Gestión de Reservas".** Corregir el título (`apps/triage/`).
- [x] **Las frases de la solicitud terminan en "p.m.."** (doble punto). Quitar el punto sobrante en la plantilla o el filtro que arma la hora.
- [x] **La barra superior dice "Administrador"** y el resto de la app dice "Administración". Unificar.
- [x] **Quitar la etiqueta "Maqueta con datos de ejemplo"** de Inicio (`apps/paneles/templates/paneles/inicio.html`, la primera pantalla después de entrar) y de Registrar persona (`apps/usuarios/templates/usuarios/nuevo.html`). Las dos heredan el bloque `estado_vista` de `templates/base/aplicacion.html`; basta con agregarles `{% block estado_vista %}{% endblock %}`. Inicio, además, está vacío ("Elige una sección en el menú lateral"): decidir si se deja así o se le pone un resumen por rol.
- [x] **Límites de texto:** hoy solo 21 de 113 campos del front tienen `maxlength`. Revisar cada `<input>` de texto y cada `<textarea>`, y ponerle el mismo límite que el serializer del backend.
- [x] **Páginas de error propias:** el front no tiene `403.html`, `404.html` ni `500.html`. Cuando se despliegue con `DEBUG=False` saldrán las genéricas de Django. Hacerlas con el diseño de AdMind y un mensaje claro.
- [x] **Errores de la API que nadie atrapa:** si una vista no atrapa `ErrorDeApi` o `ApiNoDisponible` (`cliente_api/http.py`), hoy termina en un 500. Un middleware que los convierta en la página de error con el mensaje correcto ("No tienes acceso", "No existe", "El servidor no responde, intenta en un momento").
- [x] **Accesibilidad básica:** que todo se pueda usar con el teclado y que los botones de solo ícono tengan `aria-label` (ya hay 60).

**Cómo quedó, y lo que sigue abierto:**
- **Menú por permiso:** Reglas solo con `regla.ver`; Usuarios solo con `usuario.gestionar` (Secretaría lo veía y recibía 403); Zonas comunes solo con `area.ver` o `area.gestionar`. Se revisó leyendo el permiso que exige la API de cada ítem contra el catálogo de roles, no abriendo las pantallas con los 5 roles.
- **Decisión pendiente (Vigilancia):** ya no ve "Zonas comunes", porque el calendario pide las áreas y la API exige `area.ver`, que Vigilancia no tiene. La otra salida es darle `area.ver` en el catálogo del backend.
- **Rol en pantalla:** la barra y el lateral muestran "Administración" (filtro `rol_visible`); la API sigue mandando "Administrador" y los menús siguen preguntando por él.
- **Límites:** añadidos en correo (254), contraseñas (128), descripción del área (1000), cuatro buscadores (100) y nombres de agrupaciones (2000). **Hueco en el backend:** `descripcion` del área no tiene límite en su serializer; el del front no se puede igualar a nada.
- **Errores:** `403.html`, `404.html`, `500.html` y `403_csrf.html` en `templates/`, y `ErroresDeApiMiddleware` (`apps/cuentas/errores.py`): API caída → 503, 401 → cierra sesión y vuelve al ingreso, 403/404 → su página, otros → el mensaje que ya trae el error.
- **Accesibilidad:** revisión por script; no hay botón de solo ícono sin nombre ni imagen sin `alt`. No se probó a mano con teclado.
- **Inicio sigue vacío** ("Elige una sección en el menú lateral") y su texto dice "Cuando existan reservas…", ya viejo. Falta decidir si se deja o se le pone un resumen por rol.

### A5. Prueba de romper la app — lunes, sobre la versión desplegada
La hace quien no programó. Lo que va a intentar el profe:
- [ ] Cerrar sesión y darle **Atrás** al navegador: no debe verse ninguna pantalla con datos (depende de C3).
- [ ] Copiar la URL de una pantalla de Administración y abrirla con una cuenta de Residente.
- [ ] Cambiar en la URL el id de una reserva, un caso o un anuncio por uno de otro conjunto.
- [ ] Pegar 5.000 caracteres en cada campo de texto.
- [ ] Mandar formularios con datos erróneos: el mensaje debe decir qué está mal, nunca un error crudo.
- [ ] Dejar que venza la sesión (1 hora) y seguir navegando.

### A6. Material de estudio para la sustentación (F2) — hecho el 19-nov
> Alejo eligió «guía + artefacto» (sin el banco de 60 a 80 preguntas ni el prompt evaluador). La guía es [Admind_Guia_Sustentacion_Final](../Guias/Admind_Guia_Sustentacion_Final.md) y el artefacto «Repaso de AdMind» está en https://claude.ai/artifact/73Ndy5mB9VvXgxC9rLTvn4 (47 tarjetas, quiz de 28, recorrido de 12 pasos y simulacro). Es privado: compartirlo con Camilo desde *Share*. Se escribieron directo, sin `plan_F2_*`.

**Objetivo:** que los dos puedan explicar cualquier pieza de AdMind y responder lo que pregunte el profe sin leer: cómo está construida, cuál es el flujo de una solicitud, quién le habla a quién y qué validaciones hay.

**Cómo:** igual que en la F0. Opus escribe un plan por pieza en `10_Sustentacion/` (`plan_F2_*.md`) y Sonnet los ejecuta.

**Cuándo:**
- El **domingo**, lo que ya no cambia: arquitectura, roles, seguridad, base de datos y pruebas.
- El **lunes en la noche**, lo que entre en la F1: JWT, CORS, despliegue, CI, Sonar, procedimientos y triggers, reportes, correo y Swagger.

Tareas:
- [ ] **Los planes de la F2** (Opus): uno para la guía, uno para el banco de preguntas y uno para el artefacto.
- [x] **Guía de estudio:** nueva versión de `Guias/Admind_Guia_Sustentacion_Tecnica.md`, que tiene corte del 03/11.
  - Organizada por los 12 criterios de la rúbrica y por lo que el profe dijo que va a preguntar: pruebas unitarias, despliegue, seguridad básica, tokens de sesión, romper la app desde el navegador, mensajes de error, límites de texto y separación de roles.
  - Para cada tema:
    - cómo funciona;
    - quién le habla a quién;
    - qué validaciones hay;
    - en qué archivo está;
    - cómo se demuestra en vivo;
    - y la pregunta difícil con su respuesta.
  - El recorrido completo de una petición, ya con JWT y CORS: navegador → front → `cliente_api` → API → servicio → base de datos → respuesta.
  - Lo que no está hecho y cómo decirlo: el backlog priorizado, con las citas solo en el backend, HU-17, HU-19, la importación por Excel y las demás.
- [ ] **Banco de preguntas para evaluarnos:**
  - Entre 60 y 80 preguntas por criterio, de fáciles a difíciles, en un archivo **sin respuestas**, para contestarlas por escrito.
  - Otro archivo con las **respuestas de referencia**, sacadas del código.
  - Un **prompt evaluador**: a una IA se le dan el banco, las respuestas de referencia y las nuestras. Califica cada respuesta (correcta, incompleta o errada), explica qué faltó y da una nota por criterio.
  - Cada uno contesta por su lado, y se repite con lo que salió mal.
- [x] **Artefacto de estudio en Claude**, una página interactiva para los dos:
  - tarjetas de repaso por criterio;
  - un quiz de opción múltiple que explica cada respuesta;
  - el recorrido de una petición, paso a paso;
  - un **simulacro**: preguntas al azar con temporizador, como el día de la sustentación.

  Se publica como artefacto y se comparte con Camilo.
- [ ] **Reparto del estudio:** cada uno domina a fondo sus secciones de la presentación (A8) y conoce lo básico de las del otro, porque el profe le puede preguntar a cualquiera.
- [ ] **Para la parte de seguridad:** la sesión dura **1 hora contada desde el ingreso**, no "una hora sin uso" (lo verificó el manual de usuario). Saber decirlo así.

### A7. Correo automático en HTML con logo — hecho en código el 16-nov (antes C7; rama `feat/correo-html`)
> Commit `860233d` en el back. **En `main` desde el 16-nov a las 23:39** (PR #14 a `desarrollo` y #16 `desarrollo → main`, CI en verde). Falta redesplegar y la evidencia desde la nube (A9).

**Corrección:** el correo automático no son solo los dos de cuentas. Hay **tres** puntos que mandan correo, todos en texto plano:
- **El principal**: `por_correo` en `apps/notificaciones/canal.py`, con `send_mass_mail`. Lo usan los anuncios, los casos, las infracciones, los ingresos y la decisión de una reserva. **Este es el "envío automático" que pide la rúbrica.**
- `solicitar_recuperacion` (`apps/cuentas/servicios.py`, cerca de la línea 149).
- El de restablecer el segundo factor (`apps/cuentas/dos_factores.py`, cerca de la línea 173).

Tareas:
- [x] **El bug primero:** "Publicar anuncio" muestra "No hay conexión con el servidor" aunque el anuncio sí se publica. `por_correo` corre al confirmar la transacción, dentro de la misma petición, y con SMTP real y varios destinatarios pasa de los 10 segundos que el front espera a la API (`ADMIND_API_TIEMPO_ESPERA`).
  - Arreglo propuesto: mandar el correo en un hilo aparte (`threading.Thread(..., daemon=True)`) desde el `on_commit`, detrás de un ajuste como `CORREO_EN_SEGUNDO_PLANO`, para que las pruebas lo apaguen y sigan leyendo `mail.outbox`.
  - Apagarlo en las pruebas toca `config/settings_pruebas.py`: Alejo da el visto bueno.
- [x] Pasar los tres a `EmailMultiAlternatives`, con texto y HTML.
- [x] Plantillas en `apps/notificaciones/templates/correos/`:
  - `base.html`: encabezado verde `#0E6B5A` con el logo, el nombre del conjunto, el cuerpo y el pie "AdMind · no responder";
  - `aviso.html`, para el canal;
  - `recuperar_contrasena.html`;
  - `restablecer_segundo_factor.html`.

  Maquetación con tablas, CSS en línea y ancho máximo de 600 px.
- [x] El logo va **incrustado** (CID), no por URL. Con el SMTP de siempre: adjuntar un `MIMEImage` con su cabecera `Content-ID` y referenciarlo en el HTML como `cid:...`.
- [x] Prueba: en `mail.outbox`, cada correo trae la alternativa `text/html` y el enlace o el aviso.
- [ ] **Evidencia:** captura del correo en Gmail con el logo, mandado desde la versión en la nube.

### A8. Presentación y ensayo (F3) — lunes
- [ ] Diapositivas en Canva, con una sección para Alejo y otra para Camilo, en el verde de AdMind.
- [ ] Guion base de 15 minutos: qué dice cada uno y cuánto tiempo.
- [ ] **Guion de la demostración en vivo**, en este orden:
  1. QR a `https://admind.detkor.com`.
  2. Entrar con cada rol.
  3. Intentar romperla: la URL, el botón Atrás, abrir pantallas de otro rol.
  4. El reporte, el correo y Swagger.
  5. Las evidencias de CI, Sonar y cobertura.
- [ ] **Plan B:** capturas o un video corto de la demostración, por si la red o el servidor fallan.
- [ ] **Ensayo completo** cronometrado el lunes en la noche, con preguntas del banco (A6) al final.

### A9. Despliegue en el VPS de Oracle (front, back y base) — domingo en la mañana (antes C4)
**Ya hay una versión arriba** en `https://admind.detkor.com`, detrás de Cloudflare. Falta que salga de GitHub, que se pueda repetir y que quede lista para la demostración.

**A las 20:10 del 16-nov** la nube sigue con la versión vieja (404 genérico de Django), `api.admind.detkor.com` no existe en el DNS y no hay nota `02_Arquitectura/despliegue.md`. Ninguna casilla de abajo está hecha.

**A las 23:45 del 16-nov** `main` ya tiene todo lo de Alejo, pero la nube no: Administración entra y cae en el **500 de `/solicitudes/`**, que en `main` ya está arreglado. **El SSH no responde** desde el PC de Alejo (puerto 22 y ping con *timeout* hacia `143.47.112.182`), así que no se pudo revisar el servidor ni redesplegar. Lo primero el martes: recuperar el SSH (la *security list* de Oracle o el firewall del VPS) y redesplegar los dos repos desde `main`.

**Depende de C3 (Camilo):** mientras sus `settings.py` no lean el entorno, el servidor sigue con sus cambios a mano. Cuando C3 entre a `main`, el script de abajo despliega sin tocar nada más.
- [ ] **Anotar cómo está montado**, sin claves, en una nota de la bóveda (`02_Arquitectura/despliegue.md`):
  - qué corre cada proyecto (gunicorn, servicios de `systemd`) y quién recibe las peticiones (nginx);
  - dónde está PostgreSQL;
  - qué commit de cada repo está desplegado.

  El profe va a preguntar por el despliegue y hay que saberlo de memoria.
- [ ] **La dirección de la API:** hoy `https://admind.detkor.com/api/` da 404, así que la API no está publicada en ese dominio. Para el front basta con que la llame por `http://127.0.0.1:8000` dentro del VPS. Pero **Swagger público (C10) y la demostración de CORS (C9) necesitan una dirección pública**. Propuesta: `api.admind.detkor.com` en Cloudflare → nginx → gunicorn del backend.
- [ ] **Sin `www` en todas partes** (decidido el 14-nov): `ADMIND_FRONT_URL`, `DJANGO_ALLOWED_HOSTS` y `CSRF_TRUSTED_ORIGINS` del front, y `CORS_ALLOWED_ORIGINS` de la API, con `admind.detkor.com`. Revisar que ninguna variable del servidor ni ningún correo lleve `www.`.
- [ ] **Desplegar desde `main`**, con un script en el servidor (por ejemplo `~/desplegar.sh`) que en cada repo haga:
  1. `git pull` de `main`.
  2. `pip install -r requirements.txt`.
  3. `migrate` (solo el back).
  4. `collectstatic`.
  5. Reiniciar los servicios.

  Así lo que corre es lo que está en GitHub. Hoy no lo es: el servidor tiene `DEBUG` apagado y el repo no.
- [ ] **Variables del servidor**, en un archivo de entorno fuera de los repos:
  - `DJANGO_DEBUG=False`.
  - `DJANGO_ALLOWED_HOSTS`: el dominio del front en el front; el de la API en el back.
  - `CSRF_TRUSTED_ORIGINS=https://admind.detkor.com`.
  - `DB_*`.
  - `ADMIND_FRONT_URL=https://admind.detkor.com` (lo usan los enlaces de recuperación del correo).
  - `ADMIND_API_URL` (el front hacia el back).
  - `EMAIL_*`.
  - Y, cuando entren C8 y C9, `JWT_SECRET` y `CORS_ALLOWED_ORIGINS`.
- [ ] **HTTPS de punta a punta:** en Cloudflare, el modo SSL debe ser **Full (strict)**, con un certificado de origen o Let's Encrypt en nginx. En *Flexible*, el tramo de Cloudflare al VPS va en HTTP plano, y es lo primero que va a preguntar un profe técnico. nginx debe pasar `X-Forwarded-Proto` para que funcione `SECURE_PROXY_SSL_HEADER` (C3).
- [ ] **Firewall:** en la *Security List* de Oracle y en el `iptables` del VPS, abiertos solo el 80, el 443 y el 22. Ni el 5432 de PostgreSQL ni los puertos de gunicorn hacia internet. Comprobarlo y saber decirlo.
- [ ] **Correo:** Oracle Cloud bloquea por defecto solo el puerto 25 de salida, así que **Gmail por el 587 con contraseña de aplicación debería salir** (no hace falta Brevo). Comprobarlo con un envío real desde el servidor, por ejemplo con "Recuperar contraseña". Es lo que necesita A7 para probar el correo en HTML en la nube.
- [ ] **Datos de demostración:** por SSH en el VPS, `DJANGO_DEBUG=True python manage.py crear_usuarios_prueba`. El `DEBUG` vale solo para ese comando; el comando se niega a correr sin él. Después, desde las pantallas, armar un conjunto creíble: viviendas, zonas, reservas, casos, anuncios y pagos.
- [ ] **Cuentas demo** (decidido): Residente y Vigilancia para el profe. El TOTP de Superusuario, Administración y Secretaría, en el celular de uno de los dos. Las contraseñas van en la diapositiva o por Teams, **nunca en el repo**.
- [ ] **QR** a `https://admind.detkor.com`.
- [ ] **Redesplegar el lunes en la noche**, después del PR `desarrollo → main` de C11, y repetir A5 sobre esa versión.
- [ ] **Evidencia:** la URL funcionando, una captura de la instancia en la consola de Oracle y el `systemctl status` de los servicios.

### A10. GitHub Actions (CI) — lunes, lo primero (antes C2; desde el 16-nov)
**Lo que ya está** (Camilo, 16-nov):
- `.github/workflows/ci.yml` en los dos repos. Corre con `push` y `pull_request` sobre `main`, `desarrollo` y `pruebas`, con Python 3.14.
- El back tiene un PostgreSQL 18 como *service* y revisa `makemigrations --check`.
- El front corre sin base, con `DJANGO_SECRET_KEY` y `ADMIND_API_URL` de mentira.

**Lo que falta, en este orden:**
- [x] **Poner en verde el `main` del front.** Arreglado el 16-nov en la rama `fix/ci-front` (commit `49d7aa9`, sale de `origin/main` `0d806dc`). **En `main` desde las 22:19 (PR #7 y #9), en verde.**
  - [x] `apps/triage/views.py`, líneas 219 y 222: las llamadas de casos y de citas desempacaban 2 valores y `pedir_filas` devuelve 3. Ahora reciben los 3, igual que la de reservas.
    - El error salió al fundir `main` dentro de `pruebas-camilo` (`386a0b1`): se juntaron los filtros de HU-22, que agregaron el tercer valor, con el código de casos y citas de Camilo, que esperaba dos.
    - Arregla las 25 fallas de `tests/test_triage.py` y el 500 de `/solicitudes/`. La línea de citas solo fallaba con el permiso de ver citas.
  - [x] `tests/test_citas.py`: se tomó la versión del commit de Camilo en `Desarrollo` (`861f6c1`), que solo cambia esas dos pruebas.
    - Una esperaba el enlace "Citas" sin `aria-current`, y el lateral ya lo marca.
    - La otra usaba el 2-nov-2026 como día futuro y venció; ahora congela la fecha.
    - En ese archivo es idéntico a lo de Camilo. El resto de su commit sí choca con A4 (ver *Ordenar las ramas*).
  - [x] Toda la suite del front en local: **523 pruebas, todas pasan**.
  - [x] Commit (`49d7aa9`) y push.
  - [x] PR #7 `fix/ci-front → desarrollo`, que de paso puso `desarrollo` al día con `main`.
- [ ] **Antes de hacer `git fetch` en Windows**, borrar la rama `Desarrollo` (mayúscula) en GitHub, o traer solo la rama que se necesite (`git fetch origin main`). El 16-nov un `fetch` la bajó encima de `origin/desarrollo` en el PC de Alejo, porque Windows no distingue mayúsculas en los nombres de archivo; se arregló a mano con `git update-ref`.
- [ ] **Ordenar las ramas**, con Camilo:
  1. [x] Poner `desarrollo` al día con `main`: en el front con el PR #7; en el back con el #12, que trajo los commits de `main` junto con el arreglo de la prueba de ingresos.
  2. [x] **Back:** la `Desarrollo` (mayúscula) entró a `desarrollo` con el PR #15 y a `main` con el #16, CI en verde.
  3. [ ] **Front: no fundir `Desarrollo`.** Su único commit (`861f6c1`) choca con A4 en `lateral.html`, `_enlaces_gestion.html` y `tests/test_identidad.py`, y como sale de una versión vieja quita el logo y los íconos del lateral. Revisado otra vez el 16-nov a las 22:30: A4 ya hace lo mismo (`usuario.gestionar`, `area.ver`, `regla.ver`), así que no se pierde nada. Confirmarlo con Camilo antes de descartarla.
  4. [ ] Borrar `Desarrollo` en los dos repos, las dos ramas `revert-*` del back y las ramas cortas ya fundidas.

  Desde ahí, todo PR va a `desarrollo` y no a `main`. **Ojo al crear un PR:** GitHub pone `main` como base por defecto. El 16-nov el #10 entró a `main` por eso, y se resolvió con un revert y un revert del revert (#11 y #13).
- [x] **Cobertura en el CI del back**: `pytest -q --cov --cov-report=term --cov-report=html --cov-fail-under=70`, y `htmlcov/` subido como *artifact* `cobertura-backend` (`actions/upload-artifact@v4`). Entró con el PR #9 de A2 y está en `main`.
- [x] **Prueba que dependía de la hora** (`apps/ingresos/tests.py`, la de los motivos del 400): fallaba después de las 22:00 porque la zona usaba el horario de 05:00 a 22:00 contra la hora real. Arreglada en `fix/prueba-ingresos-hora` (`9ef4826`, PR #12). Las 823 pruebas pasan a las 23:24.
- [ ] **Proteger `desarrollo` y `main`** en *Settings → Branches* de cada repo: exigir el check `CI / test` en verde antes de fundir. Lo hace quien administra la organización `ZeroFour-04`.
- [x] El aviso de Node 20: `checkout`, `setup-python` y `upload-artifact` en v6 (Node 24), con `permissions: contents: read` y la instalación por hashes de A3. Rama `ci/endurecer-dependencias` en los dos repos, sin push (19-nov).
- [ ] **Evidencia:** captura de la pestaña *Actions* de los dos repos. Desde la noche del 16-nov hay una ejecución por cada PR y cada `push` a `main` y `desarrollo`, con el `main` de los dos en verde. Las rojas de esa noche (el front antes de A10, la prueba de ingresos y el revert #11) sirven para mostrar que el CI sí detiene lo roto.
- [ ] **Después de la sustentación, dos Actions nuevas** (propuestas el 16-nov, sin hacer):
  - **Auto-merge hacia `desarrollo`**, solo con el CI en verde y sin conflictos. Se hace con lo que trae GitHub: activar *Allow auto-merge*, proteger la rama exigiendo el check `test`, y un *workflow* corto que encienda el auto-merge en cada PR a `desarrollo`. `desarrollo → main` lo sigue fundiendo Alejo a mano: es lo que se despliega, y una fusión hecha por el bot de GitHub no dispara el despliegue.
  - **Despliegue al VPS** con cada `push` a `main`, más un botón para lanzarlo a mano: `git pull`, dependencias, `migrate`, `collectstatic` y reinicio de los servicios. Falta decidir cómo entra al VPS: por SSH desde GitHub, con el puerto 22 abierto solo con llave, o con un *runner* instalado en el VPS. Los repos son públicos, y GitHub desaconseja *runners* propios en repos públicos. Antes hay que recuperar el SSH para conocer las carpetas y los servicios del servidor.
- **Para defenderlo:**
  - Cada `push` y cada PR levanta un Ubuntu limpio, instala las dependencias, crea un PostgreSQL 18 de verdad para el back, revisa que no falten migraciones y corre toda la suite.
  - Si algo falla, el PR se ve en rojo y, con la protección de rama, no se puede fundir.
  - El historial queda en *Actions*.

---

## Camilo

> [!WARNING] Al 16-nov a las 20:10 no hay en GitHub nada de Camilo posterior a los *workflows* del CI (07:02): ninguna rama, PR ni commit de C1, C3, C5, C6, C8, C9, C10 ni C12.
> **Orden sugerido para la noche**, por lo que aporta a la rúbrica contra lo que cuesta:
> 1. C1, porque tarda 15 minutos y es un criterio entero.
> 2. Subir C3, C5 y C6. C3 primero, porque A9 depende de ella.
> 3. C10 y C9, que son rápidos.
> 4. C8, el más largo, porque toca unas 25 pruebas.
> 5. C12. No está en la rúbrica, pero si el profe responde un caso en la demostración, cae en "Page not found".

### C1. Primer escaneo de SonarQube — URGENTE: ya entraron cambios a `main` el 16-nov; hacerlo antes de C3
- [ ] Entrar a https://sonarcloud.io con GitHub e importar la organización `ZeroFour-04` con los dos repos. Es gratis para repos públicos.
- [ ] Activar **Automatic Analysis** (no necesita CI) y dejar que analice `main` de los dos repos.
- [ ] **Evidencia:** captura del resumen de cada repo (bugs, vulnerabilidades, *security hotspots*, *code smells* y notas de la A a la E), guardada en `A D M I N D/Entregables_Sustentacion/evidencias/sonar_1_back.png` y `sonar_1_front.png`.
- [ ] Hacer la lista de vulnerabilidades altas y medias y repartirlas: al menos una para Camilo y una para Alejo (A3), cada una en su PR. Ya se sabe que va a marcar `DEBUG = True` y `ALLOWED_HOSTS = []` fijos en los `settings.py`: C3 los corrige.
- [ ] El segundo escaneo sale solo cuando se funda `desarrollo → main` el lunes. La pestaña *Activity* de SonarCloud muestra la curva de las dos mediciones.
- Si después se quiere ver la cobertura en Sonar, hay que cambiar a análisis desde el CI. No lo pide la rúbrica.

### C2. GitHub Actions → la montó Camilo el 16-nov y desde ahí la lleva Alejo (A10)
- [x] *Workflows* del back (PR #8) y del front (PR #6), fundidos a `main` el 16-nov. El back corre verde; el front quedó rojo por el PR #5 (ver A10).
- [ ] La prueba nocturna de `apps/ingresos`: el commit "Zona horaria" de Camilo la toca, pero está en la rama `Desarrollo` y no se ha fundido (A10, ordenar ramas).
- Lo que falta del CI (el rojo del front, las ramas, la cobertura y la protección) está en **A10**.

### C3. Ajustes de producción y seguridad — sábado en la noche (rama `fix/ajustes-produccion` en los dos repos)
> [!WARNING] En Notion, Camilo la marcó hecha el 16-nov; desde las 20:10 figura allí como *Tal vez completada*. En GitHub no hay rama ni PR con esto, y `main` sigue con `DEBUG = True` y `ALLOWED_HOSTS = []` en los dos repos, sin `gunicorn` ni `whitenoise` (verificado el 16-nov a las 14:16 y a las 20:10). Falta subirla por PR. A9 depende de ella.
- [ ] `DEBUG = os.environ.get("DJANGO_DEBUG", "False") == "True"` y `ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")` en los dos `config/settings.py`.
- [ ] Backend: `HOST` y `PORT` de la base desde `DB_HOST` y `DB_PORT`, con `localhost` y `5432` por defecto (hoy están fijos).
- [ ] Con `DEBUG` apagado: `SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")`, `SESSION_COOKIE_SECURE = True`, `CSRF_COOKIE_SECURE = True` y `CSRF_TRUSTED_ORIGINS` desde una variable de entorno.
- [ ] `gunicorn` y `whitenoise` en `requirements.txt`, `STATIC_ROOT` y el middleware de WhiteNoise en los dos proyectos. El front sirve `static/` y `design-system/`.
- [ ] Agregar `DJANGO_DEBUG=True` al `.env` local de los dos y a `.env _ejemplo`. Si no, lo local deja de funcionar, y `crear_usuarios_prueba` se niega a correr sin `DEBUG`.
- [ ] **El botón Atrás:** en `SesionRequeridaMiddleware.__call__` (`Frontend/apps/cuentas/sesion.py`), si la petición trae token y la respuesta no trae su propio `Cache-Control`, aplicarle `django.utils.cache.add_never_cache_headers`. No pisar las vistas de imágenes de `anuncios`, `conjuntos` y `casos`, que ya mandan el suyo.
  - Prueba: con sesión, la respuesta trae `no-store`. Después de cerrar sesión, la misma URL redirige al ingreso.
- Esto corrige las vulnerabilidades de Sonar de `DEBUG` y `ALLOWED_HOSTS`, y puede contar como la de Camilo.

### C4. Despliegue → pasó a Alejo (A9) el 14-nov
Camilo no tiene acceso al VPS. Lo único que le toca es **C3**, en el código: que los `settings.py` lean todo del entorno y que `gunicorn` y `whitenoise` estén en `requirements.txt`. Así A9 puede desplegar desde `main` sin editar nada a mano en el servidor.

### C5. 5 procedimientos almacenados y 5 triggers — domingo (rama `feat/bd-procedimientos-triggers`)
> [!WARNING] En Notion, Camilo la marcó hecha el 16-nov; desde las 20:10 figura allí como *Tal vez completada*. En GitHub no hay rama, PR ni migración con esto (verificado el 16-nov a las 14:16 y a las 20:10). Falta subirla por PR para que llegue al VPS con el `migrate` (A9) y se pueda regenerar el diccionario (A1).
**Cómo:**
- Cada objeto va en una migración con `migrations.RunSQL(sql, reverse_sql)` dentro de la app de su módulo, para que viaje con el esquema y llegue al VPS con el `migrate` del script de despliegue (A9).
- Cada función recibe `p_conjunto uuid` y filtra por él. Es el aislamiento entre conjuntos, y el profe lo puede preguntar.
- Desde Django se llaman en la capa de repositorio (el Manager o una función en `models.py`) con `connection.cursor()`, nunca desde la vista.
- Pruebas en `tests/esquema/`, con el camino feliz y el error.

**Triggers propuestos.** Llevan a la base reglas que hoy solo están en Python; esa es la defensa ("defensa en profundidad"):
- [ ] `trg_auditoria_inmutable`: `BEFORE UPDATE OR DELETE` en `auditoria_registro` → `RAISE EXCEPTION`. Hoy solo lo impide `RegistroQuerySet` en Python; con SQL directo se podía.
- [ ] `trg_sin_borrado_fisico`: `BEFORE DELETE` en `reservas_solicitud`, `pagos_pagodeadministracion`, `casos_caso` e `infracciones_registrodeinfraccion` → `RAISE EXCEPTION` (regla de `03_Reglas/eliminacion.md`). Correr toda la suite: si alguna prueba borra filas de esas tablas, revisarla.
- [ ] `trg_usuario_correo_normalizado`: `BEFORE INSERT OR UPDATE` en `cuentas_usuario` → `NEW.correo := lower(btrim(NEW.correo))`. Es lo mismo que ya hace el servicio al iniciar sesión.
- [ ] `trg_persona_documento_normalizado`: `BEFORE INSERT OR UPDATE` en `personas_persona` → la misma normalización de `normalizar_documento` (`apps/personas/models.py:15`). Copiarla, no inventar otra. Además `actualizado_en := now()` en cada `UPDATE`.
- [ ] `trg_infraccion_anulada_inmutable`: `BEFORE UPDATE` en `infracciones_registrodeinfraccion` → si `OLD.anulado`, `RAISE EXCEPTION`. El servicio ya lo rechaza (`apps/infracciones/servicios.py:129`).

**Procedimientos y funciones propuestos.** Dos alimentan los reportes de C6, y así queda demostrada su utilidad:
- [ ] `fn_ocupacion_areas(p_conjunto, p_desde date, p_hasta date)` → por zona: reservas en estado `RESERVADA` y horas reservadas en el rango. Alimenta el reporte PDF.
- [ ] `fn_estado_pagos(p_conjunto, p_periodo date)` → por vivienda: `CONFIRMADO`, `REPORTADO` o `SIN_REPORTE` en el mes (`periodo` siempre es día 1). Alimenta el reporte Excel. Es informativo: la mora legal sigue en `apps/pagos/mora.py`.
- [ ] `fn_resumen_casos(p_conjunto)` → total por estado y prioridad. Puede alimentar el dashboard de gestión.
- [ ] `fn_aforo_actual(p_conjunto, p_area uuid)` → personas `ADENTRO` más sus acompañantes en una zona con ingreso.
- [ ] `sp_expirar_bloqueos_vencidos(p_conjunto)`: un `PROCEDURE` de verdad, que se llama con `CALL`. Pasa a `EXPIRADA` las solicitudes `EN_SOLICITUD` con `bloqueo_vence_en` vencido. Revisar que deje lo mismo que el servicio (`apps/reservas/servicios.py`, cerca de la línea 491).

- [ ] **Evidencia:** la salida de `\df` y de `select * from information_schema.triggers where trigger_schema='public'`. Después, avisarle a Alejo para regenerar el diccionario de datos (`10_Sustentacion/datos/scripts/`).

### C6. Reportes PDF y Excel con formato profesional — domingo (rama `feat/reportes`)
> [!WARNING] En Notion, Camilo la marcó hecha el 16-nov; desde las 20:10 figura allí como *Tal vez completada*. En GitHub no hay rama ni PR con esto, ni `reportlab` ni `openpyxl` en `requirements.txt` (verificado el 16-nov a las 14:16 y a las 20:10). Falta subirla por PR. La pantalla "Reportes" la ven Administración y el Superusuario.
- [ ] Instalar `reportlab` (PDF), `openpyxl` (Excel) y `Pillow` (el logo en el Excel).
- [ ] **PDF "Uso de zonas comunes"** con `fn_ocupacion_areas`: encabezado con el logo (`Frontend/static/img/logo-marca.png`, copiarlo al backend), nombre del conjunto, rango de fechas y fecha de generación; tabla con filas alternas en el verde de AdMind; número de página al pie.
- [ ] **Excel "Estado de pagos del mes"** con `fn_estado_pagos`: logo, título, encabezados en verde con letra blanca, anchos de columna, primera fila fija y totales por estado.
- [ ] Endpoints en el backend, por ejemplo `GET /api/reportes/zonas.pdf?desde=&hasta=` y `GET /api/reportes/pagos.xlsx?periodo=2026-11`, con `Content-Disposition: attachment`. Permiso nuevo `reporte.ver` en `apps/permisos/catalogo.py`, **solo para Administración** (decidido el 14-nov; el Superusuario lo recibe solo porque el catálogo le da todos los permisos).
- [ ] Front: pantalla "Reportes" en el menú, solo para quien tenga el permiso, con los filtros. La descarga va por `pedir_archivo` de `cliente_api/http.py`, como los comprobantes.
- [ ] Pruebas: con permiso devuelve el archivo con su `Content-Type`; sin permiso, 403; de otro conjunto, 404. La prueba del intruso recoge las rutas nuevas sola y debe seguir en verde.

### C7. Correo en HTML → pasó a Alejo (A7), confirmado el 14-nov
- Ya no le toca nada a Camilo: el SMTP del servidor lo deja Alejo en A9.

### C12. Bug de casos — domingo (rama `fix/casos-redirigidos`)
Lo encontró el manual de usuario el 14-nov:
- [ ] La lista de Casos de **Administración** no muestra los casos que **Secretaría redirigió**. Revisar el filtro de la lista en `apps/casos/` (back y front) contra los estados `REDIRIGIDO` y `CITADO`.
- [ ] Después de **responder** un caso, la pantalla cae en "Page not found". Revisar a dónde redirige la vista del front tras la acción `responder` (`apps/casos/views.py` del front, ruta `<uuid:caso_id>/<slug:accion>/`).
- [ ] Pruebas de las dos cosas, en el back y en el front.

### C8. JWT — lunes (rama `feat/jwt`)
**Decidido el 14-nov: híbrido.** El token que entrega el ingreso pasa a ser un **JWT firmado** (HS256), y la tabla `TokenDeSesion` se queda para revocar. JWT puro no permite cerrar sesión ni cerrar las sesiones al cambiar la contraseña, y eso ya funciona hoy.
- [ ] Instalar `PyJWT`. Nueva variable `JWT_SECRET`, distinta de `DJANGO_SECRET_KEY`.
- [ ] En `iniciar_sesion` (`apps/cuentas/servicios.py`, cerca de la línea 49), en vez de `secrets.token_urlsafe(32)`: `jwt.encode({"sub": <id del usuario>, "jti": <aleatorio>, "iat": ahora, "exp": <vencimiento de la sesión>}, JWT_SECRET, "HS256")`. La `huella` sigue siendo el SHA-256 del token, así que la búsqueda de la sesión no cambia.
- [ ] En `AutenticacionPorToken` (`apps/cuentas/autenticacion.py`):
  - Leer `Authorization: Bearer <jwt>`.
  - Validar firma y vencimiento con `jwt.decode(..., algorithms=["HS256"])`. `ExpiredSignatureError` o `InvalidTokenError` → `AuthenticationFailed("Token inválido o vencido.")`.
  - Luego `sesion_vigente` como hoy.
  - `authenticate_header` devuelve `Bearer`.
- [ ] Front: `cliente_api/http.py:89` pasa a `f"Bearer {token}"`.
- [ ] Ajustar las ~25 pruebas del backend que arman la cabecera `Token …`.
- [ ] Pruebas nuevas: JWT vencido → 401; firma alterada → 401; JWT válido de una sesión cerrada → 401.
- **Para defenderlo:** el JWT viaja firmado y con vencimiento; la tabla permite revocarlo. El token nunca llega al navegador: vive en la sesión del servidor del front, detrás de una cookie `HttpOnly`, así que JavaScript no lo puede robar.

### C9. CORS — hecho en código el 19-nov por Alejo (rama `feat/cors` del back, `ad9eb07`, sin push)
> Va encima de `ci/endurecer-dependencias` (trae `requirements.lock` con `django-cors-headers`): fundir primero el CI. En el VPS falta `CORS_ALLOWED_ORIGINS=https://admind.detkor.com` en el entorno del back.
- [x] Instalar `django-cors-headers`: `corsheaders` en `INSTALLED_APPS` y `CorsMiddleware` lo más arriba posible, antes de `CommonMiddleware`.
- [x] `CORS_ALLOWED_ORIGINS` desde una variable de entorno, con **solo** el origen del front (`http://127.0.0.1:8001` en local, `https://admind.detkor.com` en la nube). `CORS_ALLOW_CREDENTIALS = False`.
- [x] Prueba (`tests/seguridad/test_cors.py`, 5 pruebas): un *preflight* `OPTIONS` con `Origin` del front recibe `Access-Control-Allow-Origin`; con `Origin: https://otro-sitio.example`, no.
- **Para defenderlo:** el navegador nunca llama a la API. Las pantallas las arma el servidor del front, que habla con la API de servidor a servidor, y CORS no aplica ahí. CORS es una política del navegador: la lista blanca impide que el JavaScript de otro sitio llame a la API desde el navegador de una víctima.
  - Demostración: en la consola de cualquier página, `fetch("<url de la API>")` queda bloqueado por CORS.

### C10. Documentación de la API con Swagger — lunes (rama `feat/swagger`)
- [ ] Instalar `drf-spectacular`:
  - `REST_FRAMEWORK["DEFAULT_SCHEMA_CLASS"] = "drf_spectacular.openapi.AutoSchema"`.
  - `SPECTACULAR_SETTINGS` con título "AdMind API", versión y descripción.
  - Rutas `api/schema/` y `api/docs/` (`SpectacularSwaggerView`).
- [ ] Una `OpenApiAuthenticationExtension` para `AutenticacionPorToken`, para que el botón *Authorize* mande el token (`Bearer`, si C8 ya entró).
- [ ] Una etiqueta (*tag*) por app, para que se vea la estructura de la API.
- [ ] **Ojo con la prueba transversal de rutas** de `tests/aislamiento/test_intruso.py`: recorre todas las rutas, y las de Swagger son públicas. Hay que declararlas como excepción explícita y justificada.
- [ ] Revisar `python manage.py spectacular --validate` y corregir los avisos que dejen endpoints sin esquema (`@extend_schema` en las `APIView` sin serializer).
- [ ] Hacerlo **después** de que C8 se funda, o rebasar sobre él: los dos tocan `config/settings.py`.
- [ ] **Público** (decidido el 14-nov): `/api/docs/` y `/api/schema/` se abren sin sesión. Eso no abre ningún endpoint: cada uno sigue pidiendo su token. En la nube quedan en la dirección pública de la API (A9).

### C11. Cierre — lunes en la noche
- [ ] PR `desarrollo → main` con el CI en verde, redespliegue y segundo escaneo de Sonar (captura `sonar_2_*.png`).
- [ ] Prueba de romper la app (A5) sobre la nube, junto con Alejo.

---

## Dónde queda cada evidencia (para las diapositivas)

| Criterio | Evidencia |
|---|---|
| Pruebas 70 % | Captura de `htmlcov/index.html` y el paso de cobertura en Actions (A2, A10) |
| CI | Pestaña *Actions* de los dos repos, con ejecuciones desde el 16-nov (A10) |
| SonarQube | `sonar_1_*` y `sonar_2_*` más la pestaña *Activity* (C1, C11) |
| Despliegue | QR a `https://admind.detkor.com`, la instancia en la consola de Oracle y `systemctl status` (A9) |
| BD | `\df`, `information_schema.triggers` y el diccionario regenerado (C5) |
| Reporte | El PDF y el Excel descargados desde la nube (C6) |
| Correo | Captura del correo en Gmail, con el logo (A7) |
| JWT y CORS | El token decodificado en jwt.io y la consola del navegador bloqueada por CORS (C8, C9) |
| API | `/api/docs/` desplegado (C10) |
| Roles | La prueba del intruso (97 rutas) y A5 en vivo |

## Ver también

- [plan_F0_manual_tecnico](plan_F0_manual_tecnico.md), [plan_F0_manual_usuario](plan_F0_manual_usuario.md), [plan_F0_diccionario](plan_F0_diccionario.md) y [plan_F0_tablero_y_repos](plan_F0_tablero_y_repos.md): los planes de la documentación de hoy
- [pruebas_y_ejecucion](../02_Arquitectura/pruebas_y_ejecucion.md): comandos de pruebas y la prueba nocturna de ingresos
- [eliminacion](../03_Reglas/eliminacion.md): la regla que respalda el trigger sin borrado físico
- [git](../03_Reglas/git.md): ramas y PR
