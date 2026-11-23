---
resumen: "Reparto de la sustentación técnica del lunes 23-nov entre Alejo y Camilo: qué diapositivas presenta cada uno, qué decir, qué estudiar, las preguntas probables con su respuesta y quién hace qué en la demostración. Datos verificados el 22-nov."
tipo: guia
origen: "presentación AdMind_Sustentacion_Final.pptx regenerada el 22-nov; CI, SonarCloud, el esquema de Swagger y el VPS leídos el 22-nov; guía de estudio del 19-nov."
actualizado: 2026-11-22
revisado: 2026-11-22
---

# Reparto de la sustentación: Alejo y Camilo

Unos **15 minutos** en total: ~7 cada uno y ~3 de demostración y preguntas. El reparto sigue lo que hizo cada uno: Alejo, la documentación, el despliegue, el CI y el correo; Camilo, el código, CORS, Swagger y la base de datos. Si quieren cambiar una diapositiva de dueño, se cambia en las notas del orador (`Presenta:`) de `build_deck.js`.

| # | Diapositiva | Presenta | Tiempo |
|---|---|---|---|
| 1 | Portada | Alejo | 20 s |
| 2 | Qué vamos a mostrar | Alejo | 30 s |
| 3 | Qué es AdMind | Alejo | 1 min |
| 4 | A · Diseño y experiencia de usuario | Alejo | 1 min |
| 5 | B · Roles: quién es quién | **Camilo** | 1 min |
| 6 | B · Roles: cómo se restringe el acceso | **Camilo** | 1 min |
| 7 | C · Seguridad | **Camilo** | 1 min |
| 8 | D · Consumo de la API, JWT y CORS | **Camilo** | 1,5 min |
| 9 | E · Estructura y documentación de la API (Swagger) | **Camilo** | 1 min |
| 10 | F · Correo y reportes | Alejo el correo, **Camilo** los reportes | 1,5 min |
| 11 | G · Pruebas unitarias y cobertura | Alejo | 1 min |
| 12 | H · Base de datos | **Camilo** | 1,5 min |
| 13 | I · Integración continua | Alejo | 1 min |
| 14 | J · SonarQube | Alejo los pasos y su corrección, **Camilo** la suya | 1,5 min |
| 15 | K · Despliegue en la nube | Alejo | 1 min |
| 16 | Demostración en vivo | Los dos | 3 min |

## Lo que los dos tienen que saber decir

Estos datos los puede preguntar el profesor a cualquiera de los dos:

- **5 roles:** Superusuario (plataforma), Administración, Secretaría, Vigilancia y Residente. El mínimo era 4. Un solo rol vigente por persona y conjunto.
- **La sesión dura 1 hora contada desde el ingreso**, no «una hora sin uso».
- **El token es opaco** (32 bytes aleatorios), viaja en `Authorization: Token …` y en la base solo se guarda su huella SHA-256. Cerrar sesión borra la fila: el token deja de valer de verdad. **El navegador nunca ve el token**: solo tiene la cookie `HttpOnly` del servidor del front.
- **El navegador nunca llama a la API.** Las pantallas las arma el servidor del front, que le habla a la API de servidor a servidor. La API no está publicada en internet: escucha en `127.0.0.1:8000` dentro del VPS.
- **Números del 22-nov:** 854 pruebas en el back con 94,2 % de cobertura (mínimo 70 %); 541 en el front; 101 rutas y 123 operaciones en Swagger; SonarCloud de 3 a 1 vulnerabilidades en el back y de 17 a 15 en el front; 30 y 15 ejecuciones del CI; 21 y 12 PR.
- **Lo único no implementado es JWT.** Se dice de frente (ver la parte de Camilo).

## Alejo

### Qué dice

1. **Portada y recorrido.** Presentarse, decir que la presentación sigue los criterios del profesor en su mismo orden (A a K) y que el QR ya está en pantalla para que vaya abriendo la app.
2. **Qué es AdMind.** Administra conjuntos residenciales bajo la Ley 675 de 2001. Un solo sistema para varios conjuntos, con los datos de cada uno aislados. Dos servidores Django (front y API) y PostgreSQL: el front no toca la base y el navegador no toca la API.
3. **A · Diseño.** Una sola línea gráfica: el verde de AdMind (`#0E6B5A`) con Archivo e Inter. Sistema de diseño propio (componentes `am-*`), sin Bootstrap ni Tailwind. El menú muestra solo lo que el rol puede usar. Páginas 403, 404 y 500 propias y mensajes en español.
4. **F · Correo.** Automático y en HTML, con el logo incrustado (CID), el verde de AdMind y una alternativa en texto. Se envía en los avisos (anuncios, casos, infracciones, ingresos, decisión de una reserva), en la recuperación de contraseña y al restablecer el segundo factor. Le pasa la palabra a Camilo para los reportes.
5. **G · Pruebas.** 854 pruebas y 94,2 %, salida real del CI de `main`. Corren contra PostgreSQL real, así que también prueban los triggers y las funciones. Hay camino feliz y de error: 403, 404 de otro conjunto, datos inválidos y concurrencia de reservas. El CI falla si la cobertura baja del 70 %.
6. **I · CI.** GitHub Actions en los dos repos, en cada push y PR a `main`, `desarrollo` y `pruebas`. El del back levanta PostgreSQL 18, comprueba el lock, instala, revisa que no falten migraciones y corre las pruebas con cobertura. Desde el 22-nov **solo instala paquetes cuyo hash SHA-256 está en `requirements.lock`**, el token del flujo es de solo lectura y las acciones van en Node 24.
7. **J · Sonar, los pasos y su corrección.** Los tres pasos del profesor. Primer escaneo el 17-nov. **Su corrección:** las dos vulnerabilidades MAJOR de `ci.yml` (S8541: pip podía ejecutar el `setup.py` de un paquete; S8544: dependencias sin verificar), en los dos repos (PR #21 y #12). Segundo escaneo el 22-nov: back 3 → 1, front 17 → 15. Le pasa la palabra a Camilo.
8. **K · Despliegue.** Front, API y base en un VPS de Oracle Cloud con Ubuntu 24.04, gunicorn y systemd, detrás de un túnel de Cloudflare que da el HTTPS. Un merge a `main` dispara un webhook firmado con HMAC que despliega solo: pull, dependencias, migraciones y reinicio. Los secretos y los ajustes de producción viven en el servidor, no en el repositorio.

### Qué estudiar

- **Despliegue:** los tres servicios (`admind-backend`, `admind-front`, `admind-webhook`), dónde vive cada cosa (`~/Documents/Admind/Backend` y `Front`, el `.env` del back, `/etc/admind/py/` con `DEBUG=False` y `ALLOWED_HOSTS`) y qué hace el webhook. Tener a mano `systemctl status admind-backend admind-front`.
- **CI:** leer `.github/workflows/ci.yml` del back línea por línea y saber explicar `--require-hashes` y `--only-binary :all:`. Saber contar el error de YAML del 22-nov: los dos puntos de `:all:` seguidos de espacio hacían que YAML leyera una clave; el CI lo detectó y se corrigió en minutos.
- **Cobertura:** qué mide coverage.py (líneas y ramas ejecutadas por las pruebas) y dónde está el reporte (artefacto `cobertura-backend` de cada ejecución).
- **Correo:** `EmailMultiAlternatives`, HTML más texto, logo como imagen incrustada (CID) y envío en segundo plano.
- **SonarCloud:** dónde está la pestaña *Activity* y cómo leer la tabla de la diapositiva 14.

### Preguntas probables

- **«Hay dos ejecuciones en rojo el 22-nov.»** El `ci.yml` nuevo tenía un error de sintaxis YAML. El CI lo detectó, se corrigió en minutos y la ejecución siguiente quedó en verde. Para eso está el CI.
- **«Los primeros dos meses no hay PR.»** Es cierto. Desde el 24-oct todo cambio entra por PR, y el CI existe desde el 16-nov.
- **«¿Por qué el hasher de pruebas es MD5?»** Solo en `config/settings_pruebas.py`, para que las 854 pruebas corran en segundos. Producción usa PBKDF2.
- **«¿La calificación de seguridad sigue en C?»** Sí: la calificación la fija la peor vulnerabilidad abierta. El profesor pide bajar las incidencias, no llegar a A, y bajaron de 20 a 16.
- **«¿Qué pasa si se cae el servidor?»** systemd reinicia los servicios. El plan B son las capturas de la presentación y del Manual de Usuario.

## Camilo

### Qué dice

1. **B · Roles (1).** Los 5 roles con su alcance y lo que puede hacer cada uno. Roles y permisos viven en código (`apps/permisos/catalogo.py`): el administrador solo asigna. Los menús de la captura: Administración ve 17 opciones y Vigilancia 5.
2. **B · Roles (2).** Se valida en tres sitios: el front oculta, la API exige el permiso en cada endpoint (403) y los datos de cada conjunto están aislados. Crear, ver, editar y eliminar son permisos distintos; eliminar es baja lógica. Las acciones sensibles piden el segundo factor. **La prueba del intruso** (`tests/aislamiento/test_intruso.py`) recorre todas las rutas con un usuario sin permiso y con uno de otro conjunto, y falla si aparece una ruta nueva sin registrar.
3. **C · Seguridad.** PBKDF2-SHA256 con sal y 1.000.000 de iteraciones, el de Django. Secretos en variables de entorno, fuera de GitHub. En producción `DEBUG` apagado, solo el dominio permitido y cookies seguras. TOTP para los roles sensibles. Tras cerrar sesión, el botón *Atrás* no muestra nada (`never_cache`).
4. **D · API, CORS y JWT.** El consumo, con el diagrama. **CORS, hecho por él (PR #19):** `django-cors-headers`, `CorsMiddleware` arriba, lista blanca desde `CORS_ALLOWED_ORIGINS` (en la nube `https://admind.detkor.com`), sin comodín ni credenciales, con pruebas en `tests/test_cors.py`. Aclarar que CORS es una política del navegador y que aquí cierra la puerta de atrás. **JWT, no implementado:** decirlo de frente y explicar por qué el token opaco con revocación no es peor.
5. **E · Swagger, hecho por él (PR #20).** Capas vista → servicio → repositorio. `drf-spectacular` genera el esquema OpenAPI 3.0 leyendo las vistas: `/api/schema/` y `/api/docs/`. 101 rutas y 123 operaciones en 18 grupos. La documentación es pública, pero cada operación pide el token.
6. **F · Reportes.** PDF «Uso de zonas comunes» y Excel «Estado de pagos del mes», en `/reportes/`, solo para Administración y Superusuario. Los datos salen de las funciones de la base `fn_ocupacion_areas` y `fn_estado_pagos`.
7. **H · Base de datos.** 42 tablas en PostgreSQL. La base impone reglas por sí misma: llaves foráneas compuestas por conjunto, índices únicos parciales y auditoría de solo inserción. 4 funciones, 1 procedimiento y 5 triggers, todos en migraciones. **Las diferencias frente al MER inicial las tiene que preparar él** (3 o 4 concretas); no están escritas en ninguna parte.
8. **J · Sonar, su corrección.** La que haya hecho, o si no alcanzó, cuál es y cómo se corrige (ver *Pendientes*).

### Qué estudiar

- **Permisos:** `apps/permisos/` y `exigir_permiso(request, "…")` en la primera línea de cada vista; `tests/aislamiento/test_intruso.py`.
- **Sesión y token:** el modelo `TokenDeSesion`, cómo se crea (`secrets.token_urlsafe(32)`), qué se guarda (la huella) y por qué cerrar sesión lo invalida.
- **CORS:** qué es el *preflight* `OPTIONS`, qué es un origen (esquema + dominio + puerto), por qué `CorsMiddleware` va arriba y por qué nunca `*`. Saber correr la prueba con `curl` en el VPS (abajo).
- **Swagger:** `SPECTACULAR_SETTINGS` en `config/settings.py`, `@extend_schema` en las vistas y `apps/cuentas/schema.py` (el esquema del token para el botón *Authorize*).
- **Base de datos:** por qué cuatro rutinas son funciones y una es procedimiento; los dos triggers distintos; cómo listar todo con `\df` y `information_schema.triggers`; las diferencias frente al MER inicial.

### Preguntas probables

- **«¿Y si alguien llama a la API directamente, sin el front?»** La API exige token y permiso en cada endpoint, y además no está publicada en internet. El menú del front es comodidad, no seguridad.
- **«¿Dónde guardan el token, en localStorage?»** En ningún lado del navegador. Lo guarda la sesión del servidor del front; el navegador solo tiene una cookie `HttpOnly`, que JavaScript no puede leer, así que un XSS no lo roba.
- **«¿Por qué no JWT?»** Se decidió un híbrido el 14-nov (JWT firmado HS256 más la tabla para revocar) y no alcanzó el tiempo. El token opaco se revoca al instante; un JWT puro vale hasta que vence y para revocarlo hace falta una lista negra, que es justo una tabla como la nuestra.
- **«Si el navegador no llama a la API, ¿para qué CORS?»** Para cerrar la puerta de atrás: si mañana la API se publica, el JavaScript de otro sitio no puede leerla desde el navegador de una víctima.
- **«¿Por qué cuatro son funciones y una es procedimiento?»** Las cuatro devuelven datos para leer (`SELECT`); el procedimiento modifica datos y no devuelve nada, por eso es `PROCEDURE` y se llama con `CALL`.
- **«El criterio pide 5 triggers distintos.»** Son 5 triggers en la base con dos reglas distintas: `trg_sin_borrado_fisico` protege cuatro tablas (casos, infracciones, pagos y reservas) y `trg_infraccion_anulada_inmutable` es la otra.
- **«¿Por qué no React?»** La app es sobre todo formularios y tablas. El HTML se genera en el servidor y Alpine.js va solo donde hay interacción. Así el token se queda en el servidor; con React tendría que vivir en el navegador.

## La demostración (diapositiva 16)

| Paso | Quién |
|---|---|
| Mostrar el QR y entrar con Residente y con Vigilancia | Alejo |
| Intentar romperla: URL de Administración con sesión de Residente (403), *Atrás* tras salir (vuelve al ingreso), URL inventada (404 propio) | Camilo |
| Descargar los dos reportes con Administración | Camilo |
| Abrir el correo en Gmail enviado desde la nube | Alejo |
| Evidencias: *Actions* de los dos repos, *Activity* de SonarCloud, reporte de cobertura | Alejo |
| Si piden CORS en vivo: el `curl` en el VPS | Camilo |
| Si piden Swagger en vivo: el túnel SSH | Camilo |

**CORS en vivo**, conectado al VPS:

```bash
curl -s -D - -o /dev/null -X OPTIONS -H "Origin: https://admind.detkor.com" -H "Access-Control-Request-Method: GET" http://127.0.0.1:8000/api/ | grep -i access-control-allow-origin
```

Devuelve `access-control-allow-origin: https://admind.detkor.com`. Con `-H "Origin: https://malo.com"` no devuelve nada.

**Swagger en vivo:** abrir el túnel desde el equipo (`ssh -i <llave> -N -L 18000:127.0.0.1:8000 sergio@<IP del VPS>`) y entrar a `http://127.0.0.1:18000/api/docs/`.

**Tener abierto antes de empezar:** la app en el celular y en el portátil, las dos pestañas *Actions*, las dos *Activity* de SonarCloud, una terminal conectada al VPS y el Manual Técnico.

## Pendientes antes de la sustentación

- **Camilo:** su vulnerabilidad de Sonar. La más corta es la del back: quitar la contraseña de ejemplo de `.env _ejemplo` (`secrets:S2068`); al fundirla a `main`, el back queda en 0. Después, pasar el paso 2 de la diapositiva 14 a «Hecho».
- **Camilo:** las 3 o 4 diferencias frente al MER inicial, en las notas de la diapositiva 12.
- **Alejo:** la captura del correo en Gmail enviado desde la nube, para reemplazar el recuadro punteado de la diapositiva 10.
- **Los dos:** un ensayo cronometrado con este reparto y el plan B (las capturas, por si falla la red).

## Ver también

- [sustentacion_tecnica](sustentacion_tecnica.md) — la entrada: fecha, rúbrica y estado de cada criterio
- [tareas](tareas.md) — la lista completa de tareas
- [estudio_alejo](estudio_alejo.md) — la guía de estudio de Alejo, tema por tema, con autoevaluación
- [Guía de la sustentación final](../Guias/Admind_Guia_Sustentacion_Final.md) — el detalle técnico de cada criterio
