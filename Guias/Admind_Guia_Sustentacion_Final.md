---
resumen: "Guía de estudio para la sustentación técnica final (lunes 23-nov): los 12 criterios de la rúbrica, lo que el profesor dijo que va a preguntar, el recorrido de una petición, cómo se demuestra cada cosa en vivo y la pregunta difícil de cada tema."
tipo: guia
corte: 2026-11-19
contrastado_con: "Backend origin/desarrollo ddbb773 (más feat/cors y ci/endurecer-dependencias, sin fundir), Frontend origin/desarrollo 1856da9 (más ci/endurecer-dependencias, sin fundir), la nube según el plan de entrega del 18-nov"
---

# Guía para la sustentación técnica final de AdMind

Corte: **2026-11-19**. Reemplaza, para la sustentación final, a la [guía del 3-nov](Admind_Guia_Sustentacion_Tecnica.md), que sigue sirviendo para las cuatro piezas propias (aislamiento, concurrencia, reglas y trazabilidad) con más detalle.

Va con la presentación `Entregables_Sustentacion/AdMind_Sustentacion_Final.pptx` y con el artefacto de repaso (tarjetas, quiz y simulacro), que sale de esta misma guía.

**Cómo estudiarla:**
1. Lee la parte 1 (el recorrido) hasta poder dibujarlo de memoria.
2. Lee los 12 criterios. En cada uno, tapa la respuesta de «La pregunta difícil» y contéstala en voz alta.
3. Repasa la parte 3 (lo que va a intentar el profe) con la app abierta.
4. Haz el simulacro del artefacto hasta pasar del 80 %.

**Reparto sugerido:** Alejo domina a fondo documentación, despliegue, CI, Sonar (lo suyo), correo y UX; Camilo, base de datos, reportes, roles, CORS, JWT y Swagger. Los dos tienen que poder contestar lo básico de todo: el profe le pregunta a cualquiera.

---

## Parte 1. El recorrido de una petición

Es lo que más se pregunta y lo que amarra todo lo demás. Ejemplo: un residente pide la lista de sus reservas.

```
Navegador ──HTTPS──▶ Cloudflare ──túnel cloudflared──▶ VPS Oracle
                                                          │
   gunicorn del FRONT 127.0.0.1:8001 (Django + plantillas)│
     1. SesionRequeridaMiddleware: ¿hay sesión? si no → /ingresar/
     2. La vista llama a cliente_api.reservas.listar(request)
     3. cliente_api/http.py saca el token de la sesión del servidor
        y llama con requests: GET http://127.0.0.1:8000/reservas/
        Authorization: Token <token>     (10 s de espera máximo)
                                                          │
   gunicorn de la API 127.0.0.1:8000 (Django REST Framework)
     4. CorsMiddleware (solo importa si la petición viene de un navegador)
     5. AutenticacionPorToken: SHA-256 del token → busca TokenDeSesion vigente
     6. DosFactoresAlDia: si el rol tiene permisos sensibles, exige el 2FA verificado
     7. VistaDeConjunto: toma el conjunto del token, rechaza "conjunto" en la petición (400)
     8. exigir_permiso(request, "reserva.ver") → 403 si falta
     9. Serializer valida la entrada → servicios.py aplica la regla de negocio
    10. Manager del modelo (repositorio) consulta ya filtrado por conjunto
                                                          │
   PostgreSQL 16 (en el mismo VPS, no expuesto)
    11. FK compuestas, índices únicos parciales, CHECK y triggers
                                                          │
   ◀── JSON ── la API ◀── el front arma el HTML ◀── el navegador lo muestra
```

**Tres frases para decirlo rápido:**
- El navegador **solo habla con el front**. El front habla con la API **de servidor a servidor**, dentro del mismo VPS. La API **no está publicada en internet**.
- El **token nunca llega al navegador**: vive en la sesión del servidor del front; el navegador solo tiene una cookie de sesión `HttpOnly` y `Secure`.
- Las capas son las que pidió el profe: **controlador** (`views.py`) → **servicio** (`servicios.py`) → **repositorio** (Manager de `models.py`). Las flechas solo bajan: la vista no consulta el ORM para decidir y el servicio no sabe de HTTP.

**Códigos que devuelve la API:** 200/201 bien · 400 datos mal formados (con el motivo por campo) · 401 sin token o vencido · 403 sin permiso o sin 2FA · 404 no existe **o es de otro conjunto** (nunca 403, para no confirmar que existe) · 409 el estado no lo permite (franja tomada) · 429 demasiados intentos.

---

## Parte 2. Los 12 criterios de la rúbrica

Estado al 19-nov. «En rama» quiere decir construido y con pruebas, pero sin fundir a `main`: si Alejo lo funde antes del lunes, pasa a «Hecho» y se despliega solo (ver criterio 12).

| # | Criterio | Estado |
|---|---|---|
| 1 | UX/UI | Hecho |
| 2 | Roles en front y back | Hecho |
| 3 | Seguridad | Hecho |
| 4 | API, CORS y JWT | Consumo hecho · **CORS en rama** (`feat/cors`) · **JWT no** |
| 5 | Documentación de la API | **No** (sin Swagger ni Postman) |
| 6 | Correo HTML | Hecho |
| 7 | Reportes | Hecho |
| 8 | Pruebas del back | Hecho |
| 9 | Base de datos | Hecho (4 funciones, 1 procedimiento, 5 triggers) |
| 10 | CI | Hecho · endurecido en rama (`ci/endurecer-dependencias`) |
| 11 | SonarQube | Primer escaneo hecho · la vulnerabilidad de Alejo en rama · falta la de Camilo y el segundo escaneo |
| 12 | Despliegue | Hecho, con despliegue continuo |

### 1. UX/UI — línea gráfica uniforme, navegación intuitiva

- **Cómo funciona:** plantillas de Django con un sistema de componentes propio (`am-*`), sin Bootstrap ni Tailwind. Un esqueleto (`templates/base/aplicacion.html`), una barra, un lateral y componentes de campo y confirmación reutilizados en todas las pantallas. Verde de AdMind `#0E6B5A`; cada conjunto tiene su color de acento y su foto.
- **Validaciones visibles:** confirmación de contenido antes de enviar una reserva («sábado 26 de diciembre de 2026, de 2:00 p. m. a 6:00 p. m.»), mensajes en español por campo, páginas de error propias (403, 404, 500 y CSRF) con el diseño de AdMind.
- **Archivos:** `Frontend/templates/`, `Frontend/static/`, `Frontend/design-system/`.
- **Demo:** entrar con el QR, recorrer dos roles y abrir una URL que no existe: sale la página 404 de AdMind, no la de Django.
- **La pregunta difícil:** *¿Por qué no usaron React?* — La app es sobre todo formularios y tablas. El HTML se genera en el servidor y Alpine.js solo va donde hay interacción real (cuenta regresiva, buscadores, recorte de foto). Sin npm ni compilación, y el token se queda en el servidor, que con React tendría que vivir en el navegador.
- **Lo débil, dicho de frente:** Inicio está vacío («Elige una sección en el menú lateral») y la accesibilidad solo se revisó por script (sin botones de solo ícono sin nombre ni imágenes sin `alt`), no a mano con teclado.

### 2. Roles — mínimo 4, un rol no ve ni accede a lo de otro, CRUD acotado

- **Cómo funciona:** 5 roles: **Superusuario** (plataforma), **Administración**, **Secretaría**, **Vigilancia** y **Residente** (por conjunto). Catálogo fijo en código (`apps/permisos/catalogo.py`): cada rol es una lista de permisos como `reserva.aprobar` o `reporte.ver`. **Un solo rol vigente por persona y conjunto**: se cambia, no se suma, en la misma transacción. Nunca cero Administración en un conjunto.
- **Quién decide:** la **API**, en cada petición: `exigir_permiso(request, "…")` en la primera línea de la vista → 403. El front solo decide **qué se ve**: el menú lateral muestra cada ítem solo a quien tiene el permiso que exige la API para esa pantalla.
- **Archivos:** `Backend/apps/permisos/`, `Frontend/templates/componentes/lateral.html`.
- **La prueba que lo vigila:** `tests/aislamiento/test_intruso.py` recorre **todas las rutas de la API** (97 al 14-nov, más las de reportes) desde otro conjunto y sin permiso, y falla si una ruta nueva no está registrada.
- **Demo:** entrar como Residente, copiar la URL de una pantalla de Administración (por ejemplo `/reportes/`) y pegarla: sale la página 403 de AdMind. El ítem ni siquiera aparece en su menú.
- **La pregunta difícil:** *¿Y si alguien llama a la API directamente, sin el front?* — Da igual: la API exige token y permiso en cada endpoint, y además la API no está publicada en internet. El menú del front es comodidad, no seguridad.

### 3. Seguridad — hash moderno, sin secretos expuestos

- **Contraseñas:** PBKDF2-SHA256 con sal, el de Django por defecto (`settings.py` no cambia `PASSWORD_HASHERS`). El MD5 de `config/settings_pruebas.py` es **solo** para que la suite de pruebas corra rápido; nunca llega al servidor.
- **Secretos:** `SECRET_KEY`, base de datos y correo salen del entorno (`.env` en local, archivos en `/etc/admind/` en el VPS). `DEBUG` y `ALLOWED_HOSTS` también salen del entorno; en la nube `DEBUG=False`.
- **Cookies y HTTPS:** con `DEBUG` apagado, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE` y `SECURE_PROXY_SSL_HEADER` (Cloudflare termina el HTTPS y avisa con `X-Forwarded-Proto`). CSRF de Django en todos los formularios del front.
- **Segundo factor:** TOTP con `django-otp` para los roles con permisos sensibles (Superusuario, Administración, Secretaría). Hasta verificar el código, todo da 403 (`DosFactoresAlDia`).
- **Recuperar contraseña:** enlace de un solo uso, vence en 1 hora, máximo 3 por hora por correo, y la respuesta es igual exista o no la cuenta (no deja enumerar correos).
- **Archivos subidos:** se validan por su firma (los primeros bytes), no por la extensión: PDF, JPG o PNG hasta 5 MB.
- **La pregunta difícil:** *¿Qué pasa si roban la base de datos?* — Las contraseñas están con PBKDF2 y sal, y de los tokens de sesión solo se guarda su SHA-256: con la base no se puede entrar a ninguna sesión.

### 4. API, CORS y JWT

**El consumo de la API (hecho).** Dos proyectos Django: la API (DRF) es la única que toca la base; el front tiene `DATABASES = {}` y le pide todo a la API por `cliente_api/` (un archivo por app, una función por endpoint). Si la API no responde, `ApiNoDisponible`; si responde con error, `ErrorDeApi` con el mensaje en español.

**CORS (construido el 19-nov en la rama `feat/cors` del back, sin fundir).**
- **Qué es:** una política **del navegador**. Cuando el JavaScript de una página quiere leer una respuesta de otro origen (esquema + dominio + puerto), el navegador pregunta al servidor (petición *preflight* `OPTIONS`) y solo entrega la respuesta si el servidor contesta `Access-Control-Allow-Origin` con ese origen.
- **Cómo quedó:** `django-cors-headers` 4.9.0. `CorsMiddleware` va arriba, antes de `CommonMiddleware`, para que hasta los errores lleven la cabecera. `CORS_ALLOWED_ORIGINS` sale del entorno y en local vale `http://127.0.0.1:8001` y `http://localhost:8001`. **Nunca `*`** y `CORS_ALLOW_CREDENTIALS = False` (el token va en la cabecera `Authorization`, no en cookies).
- **Por qué en AdMind casi no entra en juego:** el navegador **nunca** llama a la API. El servidor del front lo hace de servidor a servidor, y ahí no hay navegador que aplique CORS. Comprobado el 17-nov: ninguna plantilla ni script del front hace `fetch` a la API. La lista blanca **cierra la puerta de atrás**: si mañana la API se publica, el JavaScript de otro sitio no puede leerla desde el navegador de una víctima.
- **Pruebas:** `tests/seguridad/test_cors.py`, 5 pruebas: el *preflight* del front recibe permiso; el de `https://otro-sitio.example`, no; un 401 hacia otro sitio no lleva la cabecera; un 401 hacia el front sí; y no hay comodín ni credenciales.
- **Demo:** `./.venv/Scripts/python.exe -m pytest tests/seguridad -v`, o con la API local corriendo:
  ```bash
  curl -i -X OPTIONS http://127.0.0.1:8000/auth/conjuntos/ -H "Origin: http://127.0.0.1:8001" -H "Access-Control-Request-Method: GET"
  curl -i -X OPTIONS http://127.0.0.1:8000/auth/conjuntos/ -H "Origin: https://otro-sitio.example" -H "Access-Control-Request-Method: GET"
  ```
  El primero trae `access-control-allow-origin: http://127.0.0.1:8001`; el segundo no trae ninguna cabecera CORS.
- **En la nube:** al fundirla hay que poner `CORS_ALLOWED_ORIGINS=https://admind.detkor.com` en el entorno del back del VPS (sin la variable queda el valor local, que no hace daño porque la API no es pública, pero no es lo correcto).

**JWT (no implementado).**
- **Lo que hay:** un **token opaco**: 32 bytes aleatorios (`secrets.token_urlsafe(32)`), que viaja en `Authorization: Token …`. En la base (`TokenDeSesion`) solo se guarda su **huella SHA-256**, con el usuario, el conjunto activo, si ya pasó el 2FA y el vencimiento: **1 hora contada desde el ingreso**, no «una hora sin uso».
- **Por qué no es peor que un JWT:** se revoca al instante (cerrar sesión borra la fila y el token deja de valer; cambiar la contraseña cierra todas las sesiones). Un JWT puro es válido hasta que vence y no se puede revocar sin una lista negra, que es justo una tabla como la nuestra.
- **Lo que se decidió y no se construyó (14-nov):** un híbrido: JWT firmado HS256 con `sub`, `jti`, `iat` y `exp`, más la tabla para poder revocarlo. Dilo así: «se decidió, está diseñado, no alcanzó el tiempo».
- **La pregunta difícil:** *¿Dónde guardan el token en el navegador, localStorage?* — En ningún lado del navegador: lo guarda la sesión del servidor del front. El navegador solo tiene la cookie de sesión `HttpOnly`, que JavaScript no puede leer, así que un XSS no lo puede robar.

### 5. Documentación de la API — Swagger u OpenAPI, o colección de Postman

- **Estado:** **no hay.** Ni `drf-spectacular` ni colección de Postman.
- **Lo que sí hay:** las rutas descritas una por una en el anexo del Manual Técnico y en la nota `10_Sustentacion/datos/endpoints_api.md`.
- **Cómo decirlo:** «La API está documentada en el Manual Técnico, ruta por ruta, pero no generamos Swagger. Era la tarea C10 y no alcanzó». No inventar que existe.
- **Si se hace antes del lunes:** lo más rápido es `drf-spectacular` con `/api/schema/` y `/api/docs/` públicos (decidido el 14-nov), declarados como excepción en la prueba del intruso.

### 6. Correo automático en HTML con logo

- **Cómo funciona:** `EmailMultiAlternatives` con versión en texto y en HTML. Plantillas en `apps/notificaciones/templates/correos/`: `base.html` (encabezado verde con el logo, nombre del conjunto, pie «AdMind · no responder»), `aviso.html`, `recuperar_contrasena.html` y `restablecer_segundo_factor.html`. Maquetadas con tablas, CSS en línea y 600 px de ancho, porque los clientes de correo ignoran el CSS moderno.
- **El logo va incrustado** como imagen adjunta con `Content-ID` (`cid:`), no por URL: se ve aunque el cliente bloquee imágenes externas.
- **Qué lo dispara:** el canal de notificaciones (`apps/notificaciones/canal.py`) cuando se publica un anuncio, se mueve un caso, se registra una infracción o un ingreso, o se decide una reserva; además, recuperar la contraseña y restablecer el segundo factor.
- **El detalle técnico que lucir:** el correo sale **después de confirmar la transacción** (`on_commit`) y **en un hilo aparte**. Antes, con SMTP real y varios destinatarios, la API pasaba de los 10 s que espera el front y la pantalla decía «No hay conexión» aunque el anuncio sí se publicaba.
- **Demo:** «Recuperar contraseña» desde la nube y abrir el correo en Gmail.
- **La pregunta difícil:** *¿Y si el correo falla?* — El anuncio ya quedó guardado (el correo sale después del `commit`); el fallo del correo no deshace la operación.

### 7. Reportes PDF y Excel

- **Cómo funciona:** pantalla `/reportes/` del front, solo para quien tenga `reporte.ver` (Administración; el Superusuario lo tiene porque el catálogo le da todo).
  - **PDF «Uso de zonas comunes»** con `reportlab`: `GET /api/reportes/zonas.pdf?desde=&hasta=`. Saca los datos de la función `fn_ocupacion_areas`.
  - **Excel «Estado de pagos del mes»** con `openpyxl`: `GET /api/reportes/pagos.xlsx?periodo=`. Saca los datos de `fn_estado_pagos`.
  - Responden con `Content-Disposition: attachment`; el front los descarga con `pedir_archivo` de `cliente_api/http.py`.
- **Validaciones:** rango de fechas válido (serializer), permiso (403), conjunto del token (404 si es de otro).
- **Archivos:** `Backend/apps/reportes/views.py`, `apps/areas/reportes.py`, `apps/pagos/reportes.py`.
- **Demo:** descargar los dos desde la nube con Administración.
- **La pregunta difícil:** *¿Por qué los datos del reporte salen de una función de PostgreSQL y no del ORM?* — Para que los procedimientos de la rúbrica sirvan de algo real: el reporte es su consumidor. Y la función recibe el conjunto como parámetro y filtra por él, igual que el resto del aislamiento.

### 8. Pruebas del back — 70 % de cobertura, camino feliz y de excepción, con reporte

- **Números:** backend **850 pruebas** en `desarrollo` (855 con las 5 de CORS); frontend **541**. Cobertura del back: **94,1 %** medida el 19-nov sobre `feat/cors` (sentencias y ramas; 94,0 % el 16-nov). Volver a correr la mañana del lunes y usar el número real.
- **Cómo:** `pytest` + `pytest-django`. Cada corrida crea una base PostgreSQL de prueba y la borra. El front se prueba sin API: `mock.patch` sobre las funciones de `cliente_api` y revisión del HTML.
- **Las que más pesan:** la del intruso (todas las rutas desde otro conjunto), la de tablas globales (falla si aparece una tabla sin `conjunto_id` fuera de la lista cerrada), concurrencia (hilos contra PostgreSQL real: N peticiones a la misma franja, un solo bloqueo), y las de esquema (`tests/esquema/test_procedimientos.py` y `test_triggers.py`).
- **Reporte:** el CI corre `pytest --cov --cov-fail-under=70` y sube `htmlcov/` como *artifact* `cobertura-backend`. Si la cobertura baja de 70 %, el CI se pone rojo.
- **Comandos:**
  ```bash
  ./.venv/Scripts/python.exe -m pytest -q --cov --cov-report=term --cov-report=html
  ```
- **La pregunta difícil:** *¿Qué no está probado?* — El JavaScript propio (Alpine) y la prueba manual con usuarios reales. Y 94 % no quiere decir sin errores: quiere decir que el 94 % de las líneas y ramas se ejecutó al menos una vez en una prueba.

### 9. Base de datos — diseño frente al MER inicial, 5 procedimientos y 5 triggers

**El diseño:** 42 tablas en PostgreSQL. Lo que hay que saber defender:
- **Multiconjunto en una sola base:** cada tabla de un conjunto lleva `conjunto_id` y una **FK compuesta** `(x_id, conjunto_id)` que impide físicamente apuntar a una fila de otro conjunto. Django no las soporta: van en `RunSQL` en las migraciones.
- **Índices únicos parciales** para la concurrencia: `UNIQUE (area, fecha, hora_inicio) WHERE estado IN ('EN_SOLICITUD','APARTADA','RESERVADA')`.
- **Sin borrado físico:** se cierra una vigencia o se anula con motivo; ninguna FK con `ON DELETE CASCADE`.
- **Frente al MER inicial:** el MER suponía varios roles por persona y un rol Consejo; quedó un rol vigente por conjunto y 5 roles. El estado de la reserva vive en la solicitud, no en la franja (la franja es una coordenada; el calendario se calcula). Y aparecieron tablas que el MER no tenía: auditoría, tokens de sesión y las del segundo factor.

**Las rutinas** (cada una en una migración con `RunSQL`, con su `reverse_sql`, dentro de la app de su módulo; se llaman desde la capa de repositorio con `connection.cursor()`):

| Rutina | Tipo | Qué hace | Quién la usa |
|---|---|---|---|
| `fn_ocupacion_areas(conjunto, desde, hasta)` | Función | Reservas confirmadas y horas por zona | Reporte PDF |
| `fn_estado_pagos(conjunto, periodo)` | Función | Por vivienda: confirmado, reportado o sin reporte | Reporte Excel |
| `fn_aforo_actual(conjunto, area)` | Función | Personas adentro más acompañantes | Servicio de ingresos (control de aforo) |
| `fn_resumen_casos(conjunto)` | Función | Total de casos por estado y prioridad | Solo las pruebas (pensada para el tablero) |
| `sp_expirar_bloqueos_vencidos(conjunto)` | **Procedimiento** (`CALL`) | Pasa a `EXPIRADA` las solicitudes con el bloqueo de 3 min vencido | Servicio de reservas, al empezar cada acción |

Todas reciben el conjunto, filtran por él, y rechazan un conjunto nulo con `RAISE EXCEPTION`.

**Por qué 4 funciones y 1 procedimiento:** una **función** devuelve datos y se usa dentro de un `SELECT` (`SELECT * FROM fn_estado_pagos(...)`): sirve para consultar. Un **procedimiento** no devuelve nada, se llama con `CALL`, y sirve para **hacer** algo (aquí, un `UPDATE`). Expirar bloqueos es una acción; las otras cuatro son consultas.

**Los triggers:**

| Trigger | Tabla | Qué impide |
|---|---|---|
| `trg_sin_borrado_fisico` | `casos_caso` | Borrar un caso con `DELETE` |
| `trg_sin_borrado_fisico` | `infracciones_registrodeinfraccion` | Borrar una infracción |
| `trg_sin_borrado_fisico` | `pagos_pagodeadministracion` | Borrar un pago |
| `trg_sin_borrado_fisico` | `reservas_solicitud` | Borrar una solicitud de reserva |
| `trg_infraccion_anulada_inmutable` | `infracciones_registrodeinfraccion` | Modificar una infracción ya anulada |

Todos son `BEFORE` y lanzan `RAISE EXCEPTION`. **Son dos triggers distintos**, el primero en cuatro tablas. La defensa es **defensa en profundidad**: esas reglas ya estaban en Python; el trigger las sostiene aunque alguien entre por SQL directo, por el shell o por un script que se salte el código.

- **Demo:** en `psql`, `\df` (lista las funciones y el procedimiento) y `select trigger_name, event_object_table from information_schema.triggers where trigger_schema='public';`. Si quieres lucirte: `delete from casos_caso where id = '…';` → error del trigger.
- **La pregunta difícil:** *La rúbrica pide 5 procedimientos y tienen 1.* — En PostgreSQL lo que en SQL Server se llama *stored procedure* que devuelve datos es una función; el `PROCEDURE` de PostgreSQL existe desde la versión 11 y no devuelve filas. Son 5 rutinas almacenadas: 4 de consulta (funciones) y 1 de acción (procedimiento), cada una con su prueba de camino feliz y de error.

### 10. CI — flujos automáticos, con historial

- **Cómo funciona:** GitHub Actions, `.github/workflows/ci.yml` en los dos repos. Corre con cada `push` y cada PR hacia `main`, `desarrollo` y `pruebas`, en un Ubuntu limpio con Python 3.14.
  - **Back:** levanta un PostgreSQL 18 como servicio, instala, revisa que no falten migraciones (`makemigrations --check`), corre toda la suite con cobertura (falla si baja de 70 %) y sube el reporte.
  - **Front:** instala y corre la suite, sin base ni API.
- **Endurecido el 19-nov (rama `ci/endurecer-dependencias` en los dos repos, sin fundir):**
  - Las dependencias se instalan desde `requirements.lock`, que trae el **SHA-256 de cada wheel**, con `pip install --require-hashes --only-binary :all:`. Así, si alguien cambia un paquete en PyPI, el hash no coincide y no entra; y como solo instala wheels, nunca ejecuta el `setup.py` de un paquete.
  - `scripts/bloquear_dependencias.py` genera el lock desde `requirements.txt`, y el primer paso del CI falla si no coinciden.
  - El `GITHUB_TOKEN` del flujo solo puede leer (`permissions: contents: read`).
  - `checkout`, `setup-python` y `upload-artifact` en v6, que corren en Node 24 (se va el aviso de Node 20).
- **Historial:** pestaña *Actions*. Las ejecuciones rojas de la noche del 16-nov (el front antes del arreglo, la prueba de ingresos que dependía de la hora, el revert #11) sirven para mostrar que el CI **sí detiene lo roto**.
- **La pregunta difícil:** *¿El CI impide fundir algo roto?* — Hoy marca el PR en rojo, pero las ramas **no están protegidas**: GitHub todavía deja fundir. Protegerlas exigiendo el check `CI / test` es un clic en *Settings → Branches* que tiene que hacer quien administra la organización. Si no se ha hecho, decirlo así.

### 11. SonarQube — primer escaneo, una vulnerabilidad por integrante, segundo escaneo

- **Cómo funciona:** SonarCloud (la versión en la nube de SonarQube) con *Automatic Analysis*: analiza `main` y cada PR de los dos repos sin pasar por el CI.
- **Primer escaneo (17-nov):**
  - **Back:** 3 vulnerabilidades MAJOR: dos en `ci.yml` (S8541 y S8544) y una contraseña de ejemplo en `.env _ejemplo` (S2068). Seguridad C.
  - **Front:** 17: las dos de `ci.yml`, una MAJOR en `cliente_api/http.py` (S7044, armar la ruta de la API con datos del usuario) y 14 MINOR (vistas que no declaran los métodos HTTP que aceptan).
- **La de Alejo (A3), en rama:** las dos de `ci.yml` en los dos repos, con el endurecimiento del criterio 10:
  - **S8541**, «los scripts del gestor de paquetes no deberían ejecutarse al instalar»: un paquete con `setup.py` corre código arbitrario al instalarse. Se corrige con `--only-binary :all:`.
  - **S8544**, «las dependencias deberían fijarse a versiones verificadas»: `==` fija la versión, pero no garantiza que el archivo sea el mismo. Se corrige con hashes y `--require-hashes`.
- **La de Camilo:** pendiente. Las candidatas: la contraseña de `.env _ejemplo` (cambiarla por un marcador vacío) o la de `cliente_api/http.py`.
- **Segundo escaneo:** sale solo cuando las correcciones lleguen a `main`. La pestaña *Activity* muestra la curva de las dos mediciones.
- **La pregunta difícil:** *¿Qué es un security hotspot y qué es una vulnerabilidad?* — Una vulnerabilidad es un problema confirmado que hay que corregir; un *hotspot* es código sensible que una persona tiene que revisar y decidir si es seguro. AdMind tiene 0 *hotspots* abiertos.

### 12. Despliegue — 100 % en la nube y operativo

- **Dónde:** `https://admind.detkor.com` (sin `www`). Una máquina virtual de **Oracle Cloud**: Ubuntu 24.04, 2 vCPU, ~1 GB de RAM. **PostgreSQL 16** y Python 3.12 en el servidor (en local y en el CI, PostgreSQL 18 y Python 3.14).
- **Cómo llega una petición:** navegador → Cloudflare (DNS, HTTPS y certificado en el borde) → **túnel cifrado de `cloudflared`** (sale del servidor hacia Cloudflare; no abre puertos de entrada) → gunicorn del front en `127.0.0.1:8001` → la API en `127.0.0.1:8000` → PostgreSQL.
- **Servicios de `systemd`** (usuario sin privilegios, reinicio automático si caen): `admind-backend` y `admind-front` (gunicorn 27 con 2 workers; el front sirve los estáticos con whitenoise), `cloudflared`, `admind-webhook` y `admind-deploy-queue`.
- **Configuración de producción:** cada servicio usa un módulo de settings en `/etc/admind/` que importa el del repo y lo sobrescribe (`DEBUG=False`, hosts, cookies seguras). Las claves viven en el servidor, nunca en el repo.
- **Despliegue continuo con cada `push` a `main`:**
  1. GitHub manda un webhook a `deploy-admind.detkor.com`, por el mismo túnel.
  2. El receptor valida la firma **HMAC SHA-256** con un secreto compartido, solo acepta `push` a `main` de los dos repos y deja un trabajo en una cola.
  3. `systemd` detecta el trabajo y corre el script: `git pull --ff-only`, `pip install`, `migrate` (back) o `collectstatic` (front), y reinicio del servicio.
- **Demo:** el QR (`Entregables_Sustentacion/capturas/qr_admind.png`), la app en vivo, y como respaldo la captura de `systemctl status` y la de la consola de Oracle.
- **La pregunta difícil:** *¿Por qué no se ve el puerto 8000 desde internet?* — Porque la API escucha solo en `127.0.0.1` y no hay ningún puerto de entrada abierto para la web: todo entra por el túnel de Cloudflare hasta el front. La API solo la puede llamar alguien que ya esté dentro del servidor.
- **Lo que no se comprobó:** las reglas del firewall de Oracle y a qué interfaces escucha PostgreSQL (no se pudo leer sin `sudo`). No afirmar nada de eso.

---

## Parte 3. Lo que el profe dijo que va a intentar

| Va a… | Qué pasa | Por qué |
|---|---|---|
| Cerrar sesión y darle **Atrás** | No se ven datos: vuelve al ingreso | El front manda `Cache-Control: no-store` (`add_never_cache_headers`) en toda respuesta con sesión, y al cerrar sesión la API borra el token |
| Pegar la URL de Administración con una cuenta de Residente | Página 403 de AdMind | La API exige el permiso en cada endpoint; el menú ni lo muestra |
| Cambiar en la URL el id de una reserva por uno de otro conjunto | Página 404 | El Manager filtra por el conjunto del token; ids UUID; 404 y no 403 para no confirmar que existe |
| Pegar 5.000 caracteres en un campo | El campo no deja pasar del límite; si lo fuerza, la API responde 400 con el motivo | `maxlength` en el HTML igual al `max_length` del serializer; quien decide es la API |
| Mandar datos erróneos | Mensaje en español por campo, nunca un error crudo | `ErrorDeApi` trae los errores por campo; `ErroresDeApiMiddleware` convierte lo que nadie atrapó en su página (API caída → 503, 401 → vuelve al ingreso, 403/404 → su página) |
| Dejar vencer la sesión | Al siguiente clic vuelve al ingreso | El token vence **1 hora después del ingreso**; la sesión del front vence a la misma hora |
| Preguntar por los tokens de sesión | Ver el criterio 4 | Opaco, SHA-256 en la base, revocable, nunca en el navegador |
| Mirar GitHub | PR para cada cambio desde el 24-oct, CI en cada PR | Los dos primeros meses no hubo PR; el 16-nov tres PR del back fueron directo a `main` por el valor por defecto de GitHub (se arregló con un revert y un revert del revert). Decirlo si pregunta |

---

## Parte 4. Datos para memorizar

- URL: **https://admind.detkor.com**. Oracle Cloud, Ubuntu 24.04, Cloudflare Tunnel.
- **5 roles**, un rol vigente por persona y conjunto. Residente y Vigilancia no piden 2FA (son las cuentas para el profe).
- Token: **opaco, 32 bytes, SHA-256 en la base, 1 hora desde el ingreso**. Bloqueo de reserva: **3 minutos**.
- Contraseñas: **PBKDF2-SHA256** (Django). Recuperación: **3 enlaces por hora**, vence en 1 hora.
- Pruebas: back **850** (855 con CORS), front **541**, cobertura **94,1 %** (el CI exige 70 %).
- Base: **42 tablas**, **4 funciones + 1 procedimiento + 5 triggers** (2 distintos).
- Puertos: API **8000**, front **8001**, ambos solo en `127.0.0.1` en el servidor.
- CI: GitHub Actions en los dos repos; despliegue continuo por webhook firmado con HMAC.
- No hechos: **JWT**, **Swagger** y la protección de ramas. CORS, en rama.

## Parte 5. Lo que no está hecho y cómo decirlo

Regla: **nunca decir que algo existe si no existe.** «Se decidió así, está diseñado, no alcanzó el tiempo» es una respuesta aceptable; inventar no.

- **JWT:** se decidió el híbrido (JWT firmado más la tabla para revocar). Hoy: token opaco con revocación, que resuelve lo mismo sin poder leerse.
- **Swagger:** no hay. Las rutas están en el Manual Técnico.
- **Ramas sin proteger:** el CI marca en rojo, pero GitHub todavía deja fundir.
- **Accesibilidad:** solo revisión por script.
- **Inicio vacío** y el bug de casos redirigidos (C12), sin arreglar.
- **Historias pendientes:** la importación por Excel y algunas HU del tablero de Notion.

## Ver también

- [sustentacion_tecnica](../10_Sustentacion/sustentacion_tecnica.md) — la rúbrica, la fecha y el estado de cada criterio
- [tareas](../10_Sustentacion/tareas.md) — el detalle de cada tarea de Alejo y Camilo
- [Guía del 3-nov](Admind_Guia_Sustentacion_Tecnica.md) — aislamiento, concurrencia, reglas y trazabilidad a fondo, y su banco de 32 preguntas
- [plan_entrega_final_documentos](../10_Sustentacion/plan_entrega_final_documentos.md) — los datos del VPS
