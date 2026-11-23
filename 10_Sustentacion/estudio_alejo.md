---
resumen: "Guía de estudio de Alejo para la sustentación técnica del lunes 23-nov: su guion diapositiva por diapositiva, cada tema suyo explicado desde cero (diseño, correo, pruebas, CI, SonarCloud y despliegue), las preguntas difíciles con su respuesta, su parte de la demostración y una autoevaluación."
tipo: guia
origen: "reparto_sustentacion y guía de la sustentación final (19-nov), con los datos verificados el 22-nov: CI de main, SonarCloud, los dos ci.yml, apps/notificaciones, la protección de ramas en GitHub y el VPS."
actualizado: 2026-11-22
revisado: 2026-11-22
---

# Estudio de Alejo para la sustentación

Presentas las diapositivas 1, 2, 3, 4, 10 (el correo), 11, 13, 14 (los pasos y tu corrección), 15 y tu parte de la 16: unos 7 minutos, sin contar la demostración. El reparto completo y la parte de Camilo están en [reparto_sustentacion](reparto_sustentacion.md).

Para ver la arquitectura completa con diagramas, abre los dos artefactos: *Arquitectura de AdMind* (cómo está hecho el software) y *AdMind en producción* (pruebas, CI, SonarCloud y despliegue). Los enlaces están en *Ver también*, al final.

## Cómo estudiar esta guía (unas 2 horas)

1. **20 min:** *La arquitectura en un minuto*. Si la cuentas sin mirar, todo lo demás se apoya en ella.
2. **60 min:** tus seis temas. En cada uno lee *La idea*, luego *En AdMind*, y al final tapa las respuestas de *Si te preguntan* e intenta contestarlas.
3. **20 min:** la *Autoevaluación*, en voz alta.
4. **20 min:** tu guion con cronómetro. La meta es 7 minutos.

## La arquitectura en un minuto

Lo dices en la diapositiva 3, y casi todas las preguntas salen de aquí.

- **Dos servidores Django y una base.** El front (puerto 8001) arma las páginas HTML. La API (puerto 8000, Django REST Framework) tiene las reglas y es la única que toca PostgreSQL. El front tiene `DATABASES = {}`: no puede tocar la base aunque quiera.
- **El navegador solo habla con el front.** El front le habla a la API de servidor a servidor, dentro del mismo VPS. La API escucha en `127.0.0.1` y no está publicada en internet.
- **El token nunca llega al navegador.** La API entrega un token opaco al iniciar sesión. El front lo guarda en su sesión del servidor, y el navegador solo tiene una cookie `HttpOnly`.
- **Capas, como pidió el profesor:**
  - vista (`views.py`): el controlador;
  - servicio (`servicios.py`): las reglas del negocio;
  - repositorio: el Manager del modelo, que filtra solo por conjunto;
  - PostgreSQL.

  Las flechas solo bajan.
- **Varios conjuntos en una sola base, aislados.** Toda consulta sale filtrada por el conjunto activo de la sesión. Además, las llaves foráneas compuestas impiden físicamente cruzar datos. Un recurso de otro conjunto responde 404, no 403, para no confirmar que existe.

**El recorrido de una petición**, por si te lo piden. Ejemplo: un residente abre sus reservas.

1. Navegador → `https://admind.detkor.com` → Cloudflare (HTTPS) → túnel `cloudflared` → gunicorn del front en `127.0.0.1:8001`.
2. El front revisa la sesión (`SesionRequeridaMiddleware`). Su vista llama a `cliente_api`, que pone el token en `Authorization: Token …` y llama a la API en `127.0.0.1:8000`.
3. En la API, en este orden:
   1. CORS.
   2. Autentica el token, buscando su huella SHA-256.
   3. Exige el segundo factor si el rol lo pide.
   4. Fija el conjunto activo (`VistaDeConjunto`).
   5. `exigir_permiso` (403 si falta).
   6. Serializer, luego el servicio, luego el Manager filtrado.
   7. PostgreSQL.
4. Vuelve JSON al front, el front arma el HTML y el navegador lo muestra.

## Tu guion, diapositiva por diapositiva

Frases cortas para decir en voz alta. No las leas: apréndete la idea y el dato.

### 1 · Portada (20 s)

«Buenos días. Somos Alejandro y Camilo, y les presentamos AdMind. Vamos a seguir la rúbrica en su mismo orden, de la A a la K. El QR los lleva a la aplicación desplegada, para que la vayan abriendo.»

### 2 · Qué vamos a mostrar (30 s)

«Primero qué es AdMind y cómo está hecho. Después cada criterio con su evidencia, y al final una demostración en vivo en la nube.»

### 3 · Qué es AdMind (1 min)

- Administra conjuntos residenciales bajo la Ley 675 de 2001: reservas de zonas comunes, casos, anuncios, visitantes, parqueaderos, pagos de administración e ingresos.
- Un solo sistema para muchos conjuntos, con los datos de cada uno aislados.
- Dos servidores Django y PostgreSQL. El front no toca la base y el navegador no toca la API.

### 4 · A · Diseño y experiencia de usuario (1 min)

- Una sola línea gráfica: el verde de AdMind (`#0E6B5A`), Archivo para títulos e Inter para el texto.
- Sistema de diseño propio con componentes `am-*` (botones, campos, pastillas, tablas), sin Bootstrap ni Tailwind. Cada conjunto elige su color de acento y su foto.
- El menú lateral muestra solo lo que el rol puede usar.
- Confirmación antes de enviar una reserva, mensajes en español por campo y páginas 403, 404 y 500 propias.

### 10 · F · Correo (45 s, y le das la palabra a Camilo)

- Correo automático en HTML, con el logo incrustado, el verde de AdMind y una versión en texto plano.
- Sale en los avisos (anuncios, casos, infracciones, ingresos y la decisión de una reserva), al recuperar la contraseña y al restablecer el segundo factor.
- «Camilo les muestra los reportes.»

### 11 · G · Pruebas unitarias y cobertura (1 min)

- 854 pruebas en el back con 94,2 % de cobertura: es la salida real del CI de `main`. En el front, 541.
- Corren contra PostgreSQL real, así que también prueban las funciones, el procedimiento y los triggers.
- Camino feliz y de error: 403 sin permiso, 404 de otro conjunto, datos inválidos y concurrencia de reservas.
- El CI se pone rojo si la cobertura baja del 70 %.

### 13 · I · Integración continua (1 min)

- GitHub Actions en los dos repos, con cada push y cada PR a `main`, `desarrollo` y `pruebas`.
- El del back:
  1. levanta PostgreSQL 18;
  2. comprueba el lock;
  3. instala;
  4. revisa que no falten migraciones;
  5. corre las pruebas con cobertura.
- Desde el 22-nov:
  - solo instala paquetes cuyo hash SHA-256 está en `requirements.lock`;
  - el token del flujo es de solo lectura;
  - las acciones corren en Node 24.
- 30 ejecuciones en el back y 15 en el front; 21 y 12 PR.

### 14 · J · SonarQube: los pasos y tu corrección (45 s, y le das la palabra a Camilo)

- Los tres pasos del profesor: primer escaneo, una corrección por integrante y segundo escaneo.
- El primer escaneo fue el 17-nov.
- Tu corrección: las dos vulnerabilidades MAJOR de `ci.yml` (S8541 y S8544), en los dos repos (PR #21 del back y #12 del front).
- Segundo escaneo el 22-nov: back de 3 a 1, front de 17 a 15.
- «Camilo les cuenta la suya.»

### 15 · K · Despliegue en la nube (1 min)

- Front, API y base en una máquina virtual de Oracle Cloud con Ubuntu 24.04, con gunicorn y systemd.
- Detrás de un túnel de Cloudflare que da el HTTPS. No hay puertos de entrada abiertos para la web.
- Un merge a `main` dispara un webhook firmado con HMAC que despliega solo: pull, dependencias, migraciones y reinicio.
- Los secretos y los ajustes de producción viven en el servidor, no en el repositorio.

## Tus temas, desde cero

### A · Diseño (UX/UI)

**La idea.** Toda la app se ve y se usa igual: los mismos colores, tipografías y componentes en cada pantalla. Y cada rol ve solo lo que puede usar.

**En AdMind:**

- `Frontend/design-system/` tiene los tokens (paleta, tipografía, espaciado) y los componentes CSS `am-*`.
- `templates/base/aplicacion.html` es el esqueleto de toda página.
- `templates/componentes/` tiene la barra superior, el lateral, el campo de formulario y la confirmación.
- Alpine.js va solo donde hay interacción real: la cuenta regresiva de la reserva, los buscadores y el recorte de la foto.
- Páginas de error propias: 403, 404, 500 y CSRF.

**Si te preguntan:**

- *¿Por qué no React?* La app es sobre todo formularios y tablas. El HTML se genera en el servidor y Alpine.js va solo donde hay interacción. No hace falta npm ni compilación, y el token se queda en el servidor; con React tendría que vivir en el navegador.
- *¿Revisaron la accesibilidad?* Solo por script (botones sin nombre, imágenes sin `alt`), no a mano con teclado. Decirlo así.
- *¿Por qué el Inicio está vacío?* Dice «Elige una sección en el menú lateral». Es lo débil, y se dice de frente.

### F · Correo automático

**La idea.** El sistema le escribe solo al usuario cuando pasa algo que le importa. Gmail y Outlook ignoran el CSS moderno, así que el HTML de un correo se maqueta con tablas, CSS en línea y 600 px de ancho.

**En AdMind** (`Backend/apps/notificaciones/`):

- `correo.py` arma un `EmailMultiAlternatives` con el texto plano y el HTML (`attach_alternative`).
- El logo va como imagen adjunta (`MIMEImage`) con el encabezado `Content-ID: <logo>`, y el HTML lo muestra con `src="cid:logo"`. Así se ve aunque el cliente bloquee imágenes externas.
- Las plantillas están en `templates/correos/`: `base.html`, `aviso.html`, `recuperar_contrasena.html` y `restablecer_segundo_factor.html`.
- `canal.py` guarda el aviso en la bandeja de la app y programa el correo con `transaction.on_commit`: sale solo si la operación quedó confirmada en la base.
- El envío va en un hilo aparte (`threading.Thread`). Antes, con SMTP real y varios destinatarios, la API pasaba de los 10 s que espera el front. La pantalla decía «No hay conexión» aunque el anuncio sí se publicaba.

**Si te preguntan:**

- *¿Y si el correo falla?* La operación ya quedó guardada: el correo sale después del commit y su fallo no deshace nada. El aviso sigue en la bandeja de la app.
- *¿Por qué el logo incrustado y no un enlace?* Gmail y Outlook bloquean por defecto las imágenes externas. La incrustada viaja dentro del correo.
- *¿Cómo lo prueban?* Con `mailoutbox` de pytest-django: la prueba revisa que el correo traiga el HTML y que el adjunto sea el logo con su `Content-ID`.

### G · Pruebas y cobertura

**La idea.** Una prueba automática ejecuta un pedazo del código y comprueba el resultado. La cobertura mide qué parte del código ejecutaron las pruebas: líneas y ramas (cada lado de un `if`). Un 94,2 % no quiere decir «sin errores»: quiere decir que el 94,2 % se ejecutó al menos una vez en una prueba.

**En AdMind:**

- Herramientas: pytest, pytest-django y pytest-cov (coverage.py). Cada corrida crea una base PostgreSQL de prueba y la borra al final.
- Las que más pesan:
  - la del intruso (`tests/aislamiento/test_intruso.py`): todas las rutas, desde otro conjunto y sin permiso;
  - la de tablas globales: falla si aparece una tabla sin `conjunto_id`;
  - la de concurrencia: varios hilos piden la misma franja y solo uno la obtiene;
  - las de esquema: `tests/esquema/test_procedimientos.py` y `test_triggers.py`.
- El front se prueba sin API: `mock.patch` sobre las funciones de `cliente_api`, y se revisa el HTML.
- El CI sube `htmlcov/` como artefacto `cobertura-backend` en cada ejecución.
- Comando, desde `Backend/Admind_Backend`:

  ```bash
  ./.venv/Scripts/python.exe -m pytest -q --cov --cov-report=term --cov-report=html
  ```

**Si te preguntan:**

- *¿Qué no está probado?* El JavaScript propio (Alpine) y la prueba manual con usuarios reales.
- *¿Por qué el hasher de las pruebas es MD5?* Solo en `config/settings_pruebas.py`, para que las 854 pruebas corran en segundos. Producción usa PBKDF2-SHA256.
- *¿Por qué contra PostgreSQL y no SQLite?* Las reglas que más importan las hace cumplir PostgreSQL: FK compuestas, índices únicos parciales y triggers. En SQLite esas pruebas no probarían nada.
- *¿Unitarias o de integración?* De las dos:
  - la unitaria prueba una función sola, como el generador de viviendas, que es puro;
  - la de integración prueba varias piezas juntas, como una petición que pasa por la vista, el servicio y la base.

  La mayoría son de integración contra la API.

### I · Integración continua

**La idea.** Cada vez que alguien sube un cambio, una máquina limpia instala y prueba el proyecto. Así se sabe antes de fundir si algo se rompió.

**En AdMind**, el `.github/workflows/ci.yml` del back, paso a paso:

1. Corre con `push` y `pull_request` a `main`, `desarrollo` y `pruebas`.
2. `permissions: contents: read`: el token del flujo solo lee.
3. `services: postgres` levanta `postgres:18`, con un chequeo de salud (`pg_isready`).
4. `actions/checkout@v6` y `actions/setup-python@v6`, con Python 3.14.
5. *Check dependency lock:* `scripts/bloquear_dependencias.py --check` falla si `requirements.lock` no corresponde a `requirements.txt`.
6. *Install dependencies:* `pip install --require-hashes --only-binary :all: -r requirements.lock`.
7. *Check migrations:* `makemigrations --check --dry-run` falla si alguien cambió un modelo y olvidó la migración.
8. *Run tests with coverage:* `pytest -q --cov … --cov-fail-under=70`.
9. *Upload coverage report* (`if: always()`): sube `htmlcov/` aunque fallen las pruebas.

El del front tiene el lock, la instalación y `pytest -q`, sin PostgreSQL ni migraciones.

Las dos banderas que tienes que saber explicar:

- **`--require-hashes`:** pip compara el SHA-256 de cada archivo con el del lock. Si alguien cambia un paquete en PyPI, el hash no coincide y no se instala.
- **`--only-binary :all:`:** solo instala *wheels*, es decir, paquetes ya construidos. Así nunca ejecuta el `setup.py` de un paquete, que puede correr cualquier código al instalarse.

El lock lo genera `scripts/bloquear_dependencias.py`: lee `requirements.txt` y le pide a PyPI el SHA-256 de cada wheel.

**Si te preguntan:**

- *¿Por qué hay dos ejecuciones en rojo el 22-nov?* El `ci.yml` nuevo tenía un error de sintaxis YAML: en `:all: `, los dos puntos seguidos de espacio hacían que YAML leyera una clave. Se corrigió poniendo la línea entre comillas (commits `b4d5c7c` y `a0feaf4`) y la ejecución siguiente quedó en verde. Para eso está el CI.
- *¿El CI impide fundir algo roto?* Marca el PR en rojo, pero `main` no está protegida en ninguno de los dos repos (verificado en GitHub el 22-nov): GitHub todavía deja fundir. Protegerla exigiendo el check es un ajuste de *Settings → Branches*. Decirlo así.
- *¿Por qué los primeros dos meses no hay PR?* Es cierto. Desde el 24-oct todo cambio entra por PR, y el CI existe desde el 16-nov.
- *¿Qué es un artefacto?* Un archivo que la ejecución guarda para descargarlo después. Aquí, el reporte de cobertura en HTML.
- *¿Por qué Node 24?* Las acciones de GitHub corren en Node. Las versiones v6 usan Node 24 y quitan el aviso de que Node 20 se retira.

### J · SonarQube

**La idea.** Es análisis estático: SonarCloud lee el código sin ejecutarlo y busca bugs, vulnerabilidades, *code smells* y duplicación.

- Una **vulnerabilidad** es un problema de seguridad confirmado.
- Un **security hotspot** es código sensible que una persona tiene que revisar y decidir si es seguro.
- La **calificación de seguridad** (de A a E) la fija la peor vulnerabilidad abierta: con una MAJOR abierta, queda en C.

**En AdMind:**

- SonarCloud funciona con *Automatic Analysis*: analiza `main` y cada PR de los dos repos sin pasar por el CI.
- Los proyectos son públicos: `ZeroFour-04_Admind_Backend` y `ZeroFour-04_Admind_Front-End`.

Tu corrección fueron las dos de `ci.yml`, en los dos repos:

- **S8541**, «los scripts del gestor de paquetes no deberían ejecutarse al instalar». Se corrige con `--only-binary :all:`.
- **S8544**, «las dependencias deberían fijarse a versiones verificadas». El `==` fija la versión, pero no garantiza que el archivo sea el mismo. Se corrige con el lock con hashes y `--require-hashes`.

La tabla de la diapositiva 14:

| | Back 17-nov | Back 22-nov | Front 17-nov | Front 22-nov |
|---|---|---|---|---|
| Vulnerabilidades | 3 | 1 | 17 | 15 |
| Calificación de seguridad | C | C | C | C |
| Bugs | 0 | 0 | 3 | 3 |
| Duplicación | 0,9 % | 0,9 % | 0,2 % | 0,2 % |

Lo que queda abierto:

- en el back, `secrets:S2068`: la contraseña de ejemplo de `.env _ejemplo` (MAJOR);
- en el front, `pythonsecurity:S7044` en `cliente_api/http.py` (MAJOR) y 14 MINOR `python:S3752`, vistas que no declaran sus métodos HTTP.

La corrección de Camilo sale de esa lista. Si la funde antes del lunes, el back queda en 0: revisa SonarCloud esa mañana y di el número real.

**Si te preguntan:**

- *¿Por qué sigue en C?* La calificación la fija la peor vulnerabilidad abierta. El profesor pide bajar las incidencias, no llegar a A, y bajaron de 20 a 16.
- *¿SonarQube o SonarCloud?* SonarCloud es SonarQube en la nube, con el mismo motor de reglas. No hubo que montar un servidor.
- *¿Qué es S8541, en palabras simples?* Un paquete de Python puede traer un `setup.py`, que es un programa que se ejecuta al instalarlo. Si alguien publica un paquete malicioso, ese código correría en el CI. Con solo *wheels*, no se ejecuta nada al instalar.

### K · Despliegue

**La idea.** La aplicación corre en un servidor en internet, siempre encendida y con HTTPS, y se actualiza sola cuando se funde un cambio.

**En AdMind:**

- Una máquina virtual de Oracle Cloud: Ubuntu 24.04, 2 vCPU y ~1 GB de RAM.
- En el servidor corren PostgreSQL 16 y Python 3.12. En local y en el CI son 18 y 3.14.
- **gunicorn** es el servidor de aplicaciones de producción para Django; `runserver` es solo para desarrollar.
- **systemd** es el gestor de servicios de Linux: arranca los servicios con la máquina y los reinicia si fallan.

Los servicios corren con un usuario sin privilegios:

| Servicio | Qué corre | Dónde escucha |
|---|---|---|
| `admind-backend` | gunicorn con 2 workers: la API | `127.0.0.1:8000` |
| `admind-front` | gunicorn con 2 workers; los estáticos con whitenoise | `127.0.0.1:8001` |
| `cloudflared` | El túnel de Cloudflare | Sale hacia Cloudflare; no abre puertos |
| `admind-webhook` | El receptor de webhooks de GitHub | `127.0.0.1:8010` |
| `admind-deploy-queue` | La cola de despliegues | — |

**Cloudflare Tunnel.** `cloudflared` abre una conexión saliente y cifrada desde el VPS hasta Cloudflare, y las peticiones a `admind.detkor.com` entran por ahí. Por eso no hace falta abrir el 80 ni el 443, y el certificado HTTPS lo pone Cloudflare en el borde.

**Configuración de producción.** Cada servicio usa un módulo de settings en `/etc/admind/py/` que importa el del repo y lo sobrescribe:

- `DEBUG = False`;
- `ALLOWED_HOSTS`: en el front, `admind.detkor.com`; en el back, solo `127.0.0.1` y `localhost`;
- cookies seguras y `CSRF_TRUSTED_ORIGINS`.

Las claves (base, correo, `SECRET_KEY`) están en el `.env` del servidor. Ahí también vive `CORS_ALLOWED_ORIGINS` del back.

**Despliegue continuo**, paso a paso:

1. Se funde un PR a `main` y GitHub manda un webhook a `deploy-admind.detkor.com`, por el mismo túnel.
2. `server.py` valida la firma HMAC SHA-256 con un secreto compartido. Solo acepta `push` a `refs/heads/main` de los dos repos, descarta entregas repetidas y deja un trabajo en la cola.
3. Una unidad `.path` de systemd ve el trabajo y corre `deploy_queue.py`, que lanza el script del proyecto:
   - back: `git pull --ff-only`, `pip install`, `migrate` y reinicio;
   - front: `git pull --ff-only`, `pip install`, `collectstatic` y reinicio.

Hoy lo desplegado es igual a `main`: back `b4d5c7c`, front `a0feaf4`.

**Si te preguntan:**

- *¿Por qué no se ve el puerto 8000 desde internet?* La API escucha solo en `127.0.0.1` y no hay ningún puerto de entrada abierto para la web. Todo entra por el túnel de Cloudflare hasta el front, y la API solo la puede llamar alguien que ya esté dentro del servidor.
- *¿Qué es HMAC y para qué sirve aquí?* Es una firma. GitHub calcula un SHA-256 del cuerpo con un secreto que solo conocen GitHub y el servidor. El servidor lo recalcula y, si no coincide, descarta la petición. Sin eso, cualquiera que conociera la URL podría disparar despliegues.
- *¿Qué pasa si se cae el servidor?* systemd reinicia los servicios. El plan B son las capturas de la presentación y del Manual de Usuario.
- *¿Qué pasa si un despliegue sale mal?* No hay vuelta atrás automática: se vuelve al commit anterior a mano y se reinicia. Por eso el CI va antes de fundir.
- *¿Por qué no Docker?* Los servicios corren directamente con systemd. Para un solo servidor y dos personas, fue lo más simple.

## Tu parte de la demostración

| Paso | Qué haces | Qué dices | Si falla |
|---|---|---|---|
| 1 | Mostrar el QR y abrir `https://admind.detkor.com` | «Está en la nube; la pueden abrir ya.» | Las capturas de la presentación |
| 2 | Entrar con Residente y después con Vigilancia | «Cada rol ve un menú distinto.» | El Manual de Usuario |
| — | *Camilo intenta romperla y descarga los reportes* | — | — |
| 3 | Abrir en Gmail el correo enviado desde la nube | «Correo en HTML, con el logo incrustado y el verde de AdMind.» | La captura de la diapositiva 10 |
| 4 | *Actions* de los dos repos | «Cada push corre el CI.» | La captura de la diapositiva 13 |
| 5 | *Activity* de SonarCloud | «Las dos mediciones: de 3 a 1 y de 17 a 15.» | La tabla de la diapositiva 14 |
| 6 | El reporte de cobertura (artefacto `cobertura-backend`) | «94,2 %; el CI exige 70.» | La salida de la diapositiva 11 |
| 7 | Si lo piden: `systemctl status` en el VPS | «Los servicios corren y se reinician solos.» | La captura del Manual Técnico |

El correo del paso 3 conviene pedirlo unos minutos antes, con «Recuperar contraseña» desde la nube, para que ya esté en la bandeja.

**Antes de empezar, ten abierto:**

- la app en el celular y en el portátil;
- las dos pestañas *Actions* y las dos *Activity* de SonarCloud;
- Gmail;
- una terminal conectada al VPS;
- el Manual Técnico.

**Comandos en el VPS** (la llave y la IP no van en la bóveda):

```bash
systemctl status admind-backend admind-front --no-pager
git -C ~/Documents/Admind/Backend log --oneline -1
git -C ~/Documents/Admind/Front log --oneline -1
curl -s -o /dev/null -w "%{http_code}\n" https://admind.detkor.com/
```

## Datos para memorizar

- **URL:** `https://admind.detkor.com`. Oracle Cloud, Ubuntu 24.04, Cloudflare Tunnel.
- **Pruebas:** 854 en el back con 94,2 % y 541 en el front. El CI exige 70 %.
- **CI:** 30 ejecuciones en el back y 15 en el front; 21 y 12 PR. Python 3.14 y PostgreSQL 18.
- **SonarCloud:** de 3 a 1 y de 17 a 15 (de 20 a 16), con calificación C. Tus reglas son S8541 y S8544, en los PR #21 y #12.
- **Puertos:** 8000 la API, 8001 el front y 8010 el webhook, todos en `127.0.0.1`.
- **Servidor:** PostgreSQL 16, Python 3.12, gunicorn con 2 workers por servicio.
- **Diseño:** verde `#0E6B5A`, Archivo e Inter, componentes `am-*`.
- **Correo:** `EmailMultiAlternatives`, logo por CID, `on_commit` y un hilo aparte.
- **Token:** opaco, de 32 bytes, guardado como SHA-256, vence 1 hora después del ingreso.
- **Lo que no está hecho:** JWT, y la protección de `main` en GitHub.

## Lo que no debes decir

- Que JWT está hecho. Lo explica Camilo: no está implementado.
- Que el CI bloquea el merge. Lo marca en rojo, pero `main` no está protegida.
- Nada del firewall de Oracle ni de a qué interfaces escucha PostgreSQL: no se pudo leer sin `sudo`.
- La IP del VPS, el usuario de SSH, la llave ni ninguna contraseña. Ni siquiera en pantalla: cuidado al compartir la terminal.
- Números viejos: 850 pruebas, 94,1 % o 97 rutas. Los de hoy son 854, 94,2 % y 101 rutas.

## Autoevaluación

Responde en voz alta antes de abrir cada respuesta.

> [!question]- ¿Por qué el navegador nunca ve el token?
> Porque el navegador no llama a la API. El token lo guarda la sesión del servidor del front, y el navegador solo tiene una cookie `HttpOnly`, que JavaScript no puede leer. Un XSS no lo roba.

> [!question]- ¿Qué hace `--require-hashes`? ¿Y `--only-binary :all:`?
> `--require-hashes` compara el SHA-256 de cada paquete con el de `requirements.lock`: si cambió en PyPI, no entra. `--only-binary :all:` instala solo wheels, así que nunca se ejecuta el `setup.py` de un paquete.

> [!question]- ¿Qué pasa si alguien cambia un modelo y olvida la migración?
> El paso *Check migrations* (`makemigrations --check --dry-run`) falla y el CI se pone rojo.

> [!question]- ¿Qué mide la cobertura y qué no?
> Mide qué líneas y ramas se ejecutaron en las pruebas. No mide si el resultado es correcto en todos los casos: 94,2 % no quiere decir sin errores.

> [!question]- ¿Por qué las pruebas corren contra PostgreSQL y no SQLite?
> Porque las reglas clave las impone PostgreSQL (FK compuestas, índices únicos parciales, triggers). En SQLite no existirían y la prueba no probaría nada.

> [!question]- ¿Por qué el correo sale con `on_commit` y en un hilo aparte?
> `on_commit`: para que solo salga si la operación quedó guardada. El hilo: para que el SMTP lento no haga pasar a la API de los 10 s que espera el front.

> [!question]- ¿Por qué el logo va como CID?
> Porque los clientes de correo bloquean las imágenes externas. El logo incrustado viaja dentro del correo y se ve siempre.

> [!question]- ¿Qué es una vulnerabilidad y qué es un security hotspot?
> La vulnerabilidad es un problema confirmado que hay que corregir. El hotspot es código sensible que una persona revisa y decide si es seguro.

> [!question]- ¿Por qué la calificación de seguridad sigue en C?
> La fija la peor vulnerabilidad abierta, y queda una MAJOR en cada repo. Las incidencias bajaron de 20 a 16.

> [!question]- ¿Cómo llega una petición del navegador a la base en la nube?
> Navegador → Cloudflare (HTTPS) → túnel `cloudflared` → front en `127.0.0.1:8001` → API en `127.0.0.1:8000` (token, segundo factor, conjunto activo, permiso, servicio, Manager) → PostgreSQL. La respuesta vuelve como JSON y el front arma el HTML.

> [!question]- ¿Por qué no hay puertos de entrada abiertos?
> Porque el túnel lo abre el servidor hacia Cloudflare, de salida. La web entra por ahí, y la API y la base solo escuchan dentro del servidor.

> [!question]- ¿Qué valida el webhook antes de desplegar?
> La firma HMAC SHA-256 con el secreto compartido, que sea un `push` a `main` de uno de los dos repos y que la entrega no esté repetida.

> [!question]- ¿Dónde viven los secretos de producción?
> En el servidor: el `.env` y los módulos de settings de `/etc/admind/py/`. En los repositorios solo está `.env _ejemplo`.

> [!question]- ¿Qué hace el despliegue del back y qué hace el del front?
> Back: `git pull --ff-only`, `pip install`, `migrate` y reinicio. Front: `git pull --ff-only`, `pip install`, `collectstatic` y reinicio.

> [!question]- ¿El CI impide fundir algo roto?
> No del todo. Marca el PR en rojo, pero `main` no está protegida en GitHub y todavía deja fundir.

> [!question]- ¿Por qué un recurso de otro conjunto responde 404 y no 403?
> Porque un 403 confirma que el recurso existe, y esa confirmación ya es información filtrada.

## Ver también

- [reparto_sustentacion](reparto_sustentacion.md): quién presenta qué y la parte de Camilo
- [sustentacion_tecnica](sustentacion_tecnica.md): la rúbrica y el estado de cada criterio
- [Guía de la sustentación final](../Guias/Admind_Guia_Sustentacion_Final.md): el detalle técnico de los 12 criterios (con cifras del 19-nov)
- [vision_general](../02_Arquitectura/vision_general.md) y [aislamiento](../03_Reglas/aislamiento.md): la arquitectura en la bóveda
- [Arquitectura de AdMind](https://claude.ai/artifact/AtvFRZoD7oBgqei1JWTgip) y [AdMind en producción](https://claude.ai/artifact/QhrGRo5HGwQ3qK122vsgQJ): los dos artefactos, con diagramas y modo repaso (privados; sus fuentes están en `Entregables_Sustentacion/_artefactos_arquitectura/`)
