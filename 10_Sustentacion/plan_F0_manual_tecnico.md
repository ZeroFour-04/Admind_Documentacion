---
titulo: "F0 · Manual técnico en Word"
fecha: 2026-11-14
alcance: "Manual técnico de AdMind: arquitectura, requerimientos, configuración y tecnologías, con el estado real del código"
punto_de_partida: "Backend main b89d9f2 y Frontend main bdcb5c3 (iguales a GitHub el 2026-11-14); guía de sustentación del 03/11 contrastada con esos mismos commits"
resumen: "Plan para que Sonnet arme el manual técnico en Word desde la bóveda y el código, marcando lo que está en implementación."
estado: activo
ejecutado:
hu:
---

# Plan F0 · Manual técnico

**Entregable:** `Entregables_Sustentacion\AdMind_Manual_Tecnico.docx` (y su PDF).
**Tiempo estimado:** 2 a 3 horas. Extensión orientativa: 20 a 30 páginas sin los anexos.
**Antes de empezar:** leer [estilo_entregables](estilo_entregables.md).

## Reglas de este plan

- **La fuente principal es la guía** [Admind_Guia_Sustentacion_Tecnica](../Guias/Admind_Guia_Sustentacion_Tecnica.md). Su corte es el 03/11, pero se contrastó con `b89d9f2` y `bdcb5c3`, que siguen siendo el código de hoy. Lo que diga la guía se puede usar tal cual, reescrito en tono de manual (sin "el jurado preguntará").
- La guía y las notas de `02_Arquitectura/` se leen **por secciones**, solo la que necesita cada capítulo. No se recorre la bóveda.
- **Si una nota y el código no coinciden, manda el código.** Se usa lo del código y se le avisa a Alejo al final.
- Lo que la rúbrica pide y **todavía no existe** (JWT, CORS, Swagger, despliegue, CI, SonarQube, cobertura, procedimientos y triggers, reportes, correo HTML) va en un recuadro ámbar **"En implementación"** de una o dos frases que diga qué se va a hacer, según [tareas](tareas.md). Nunca se describe como hecho.
- Nada de contraseñas, claves ni valores del `.env`: solo los **nombres** de las variables.

## Capítulos

Cada capítulo dice de dónde sale su contenido.

### 1. Introducción (1 página)
- Propósito del manual, a quién va dirigido (un desarrollador que va a instalar, mantener o evaluar AdMind) y alcance.
- Qué es AdMind en un párrafo. **Fuente:** guía §1 y [que_es_admind](../01_Contexto/que_es_admind.md), solo el primer apartado.

### 2. Requerimientos
- **2.1 Funcionales:** una tabla con las historias **construidas y parciales**, agrupadas por módulo (Código | Historia | Estado).
  - **Fuente:** la tabla *Todas las historias* de [historias](../08_Estado/historias.md).
  - Después de la tabla, una frase: "Las historias restantes del backlog quedan fuera de esta entrega" y cuántas son. Sin listarlas.
- **2.2 No funcionales**, cada uno con una o dos frases y dónde se cumple:
  - **Seguridad:** contraseñas con PBKDF2-SHA256 de Django, segundo factor y sesión de una hora.
  - **Aislamiento entre conjuntos**, por la Ley 1581 de protección de datos.
  - **Concurrencia:** una sola reserva por franja aunque 50 personas pulsen a la vez.
  - **Trazabilidad:** auditoría de solo inserción y sin borrado físico.
  - **Cumplimiento legal:** Ley 675 de 2001 y Ley 1581 de 2012.
  - **Usabilidad y accesibilidad:** sistema de diseño propio con contraste verificado.
  - **Mantenibilidad:** capas y pruebas automáticas.
  - **Fuentes:** guía §4 y §5 y [legal](../01_Contexto/legal.md) §4.1 y §4.2.
- **2.3 Requisitos para instalar:**
  - Windows, Linux o macOS; Python 3.14; PostgreSQL 18; Git.
  - Un navegador actual (Chrome, Edge o Firefox).
  - 4 GB de RAM son suficientes para los dos servidores y la base.

### 3. Arquitectura
- **3.1 Vista general:** dos proyectos Django separados: la API (puerto 8000), única que toca la base, y el front (puerto 8001), con `DATABASES = {}`.
  - **Diagrama** de cuatro cajas (Navegador → Frontend → API → PostgreSQL), con lo que viaja en cada flecha (HTML y formularios; JSON con el token; SQL). Hacerlo como imagen o con formas de Word, en los colores del estilo.
  - Por qué dos servidores.
  - **Fuente:** guía §2 y [vision_general](../02_Arquitectura/vision_general.md).
- **3.2 Capas:** la tabla de equivalencia ASP.NET ↔ AdMind (Controllers = `urls.py` + `views.py`, Dtos = `serializers.py`, Services = `servicios.py`, Repositories = `models.py` + `ManagerDeConjunto`, Utilities = `apps/comun/`) y la regla de que las llamadas solo bajan. El patrón de errores: el servicio lanza una excepción de negocio y la vista la traduce a HTTP. **Fuente:** guía §2 y [capas](../03_Reglas/capas.md).
- **3.3 Estructura del código:** una tabla por proyecto con cada app y para qué sirve. **Fuente:** [mapa_codigo](../02_Arquitectura/mapa_codigo.md).
- **3.4 Recorrido de una petición:** un residente envía una solicitud de reserva, paso a paso:
  1. Formulario en el navegador.
  2. Vista del front.
  3. `cliente_api/http.py`, con el token sacado de la sesión.
  4. Vista de la API: autentica el token, revisa el permiso y fija el conjunto activo (`VistaDeConjunto`).
  5. `servicios.py`: motor de reglas y bloqueo.
  6. Manager filtrado por conjunto.
  7. PostgreSQL, con el índice único parcial.
  8. La respuesta de vuelta, con su código HTTP.

  **Fuente:** guía §2, §4.2 y §4.3, y [frontend](../02_Arquitectura/frontend.md).
- **3.5 Piezas propias del diseño:** aislamiento multiconjunto (tres líneas de defensa), concurrencia (bloqueo de 3 minutos con índice único parcial), motor de reglas (sistema, alfa y beta) y trazabilidad. Una subsección por pieza, con el problema, la solución y la prueba que la vigila. **Fuente:** guía §4.1 a §4.5. Se puede incluir uno o dos fragmentos de código cortos de la guía, en Consolas.
- **3.6 Modelo de datos:**
  - 42 tablas (32 del negocio), llaves UUID y FK compuestas por conjunto.
  - Archivos guardados en la base (`bytea`).
  - Las restricciones que hace cumplir PostgreSQL.
  - Remitir al Diccionario de Datos para el detalle.
  - **Fuente:** el encabezado de [datos/diccionario_datos.md](datos/diccionario_datos.md) y [restricciones_bd](../02_Arquitectura/restricciones_bd.md).
  - Recuadro ámbar: procedimientos almacenados y triggers (C5).

### 4. Seguridad
- **Autenticación:**
  - Ingreso con correo y contraseña.
  - Token aleatorio del que la base guarda solo la huella SHA-256.
  - Sesión de 1 hora, que se revoca al cerrar sesión o al cambiar la contraseña.
  - **Fuente:** guía §5 y `Backend/Admind_Backend/apps/cuentas/autenticacion.py`.
  - Recuadro ámbar: el token pasa a ser un JWT firmado, conservando la revocación (C8).
- **Segundo factor:** TOTP con QR y códigos de respaldo. Lo exigen los roles con permisos sensibles: **Superusuario, Administración y Secretaría**. Vigilancia y Residente no lo exigen (verificado en el código el 2026-11-14).
- **Contraseñas:**
  - Hash PBKDF2-SHA256, el de Django por defecto, con sal y muchas iteraciones; nunca texto plano.
  - Los cuatro validadores de Django (similitud con los datos, longitud mínima, contraseñas comunes, solo números).
  - Recuperación con enlace de un solo uso, que vence en 1 hora, con un máximo de 3 por hora.
- **Autorización:**
  - Catálogo fijo de 5 roles y sus permisos.
  - `exigir_permiso` en la primera línea de cada vista.
  - El front solo decide qué se muestra; la API decide en cada petición.
  - Lo de otro conjunto responde 404 (nunca 403, para no confirmar que existe).
  - La **prueba del intruso** recorre todas las rutas de la API.
- **Sesión del front:** la cookie es `HttpOnly` y el token nunca llega al JavaScript del navegador.
- **Secretos:** van en `.env`, que está en `.gitignore`. El repositorio solo trae `.env _ejemplo` sin valores.
- **Códigos HTTP:** la tabla de la guía §2.
- Recuadro ámbar: CORS con lista blanca del front (C9), con la explicación de que el navegador no llama a la API directamente (guía o [tareas](tareas.md), C9).

### 5. La API
- Estilo REST con JSON, autenticación por cabecera, 97 rutas agrupadas por módulo.
- Un ejemplo de petición y respuesta (ingreso o lista de anuncios), escrito a partir del serializer correspondiente.
- La tabla completa va en el Anexo A.
- Recuadro ámbar: documentación interactiva con Swagger en `/api/docs/` (C10).

### 6. Tecnologías
- La tabla de versiones y para qué sirve cada una. **Fuente:** guía §3 o [stack](../02_Arquitectura/stack.md), la tabla *Versiones en uso*. Comparar las versiones con `Backend/Admind_Backend/requirements.txt` y `Frontend/Admind_Front-End/requirements.txt`; mandan los `requirements`.
- Por qué cada decisión grande: Django y no FastAPI, Django 5.2 LTS, PostgreSQL y no SQLite, plantillas con Alpine.js y no React, sin Docker. **Fuente:** guía §3.

### 7. Configuración e instalación
- **7.1 Repositorios y ramas:** los dos enlaces de GitHub; ramas `main`, `desarrollo` y `pruebas`, más una rama corta por cambio que entra por PR.
- **7.2 Instalación local, paso a paso, para cada proyecto:**
  1. Clonar.
  2. `python -m venv .venv`.
  3. `pip install -r requirements.txt`.
  4. Crear el `.env` a partir de `.env _ejemplo`.
  5. Crear la base `admind_db` y su usuario en PostgreSQL.
  6. `python manage.py migrate`.
  7. `python manage.py crear_usuarios_prueba`.
  8. `runserver 8000` y `runserver 8001`.

  **Fuente:** la sección *Correr todo en el PC* de [pruebas_y_ejecucion](../02_Arquitectura/pruebas_y_ejecucion.md) y los comandos de `AGENTS.md`. Mostrar los comandos de forma genérica (sin la ruta del PC de Alejo).
- **7.3 Variables de entorno:** tabla Variable | Proyecto | Para qué | Obligatoria.
  - Backend: `DJANGO_SECRET_KEY`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `ADMIND_FRONT_URL`, `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` y `DEFAULT_FROM_EMAIL`. Sin `EMAIL_HOST`, los correos salen por la consola.
  - Frontend: `DJANGO_SECRET_KEY` y `ADMIND_API_URL`.
  - **Comprobarlas** en los dos `config/settings.py`.
- **7.4 Despliegue:** recuadro ámbar con el plan de C4 (Render, dos servicios web y PostgreSQL, gunicorn y WhiteNoise) y la nota de que el correo en la nube va por la API HTTP de Brevo, porque el plan gratis bloquea SMTP.

### 8. Pruebas
- **Correr las dos suites antes de escribir este capítulo** y usar los números de hoy (los de la bóveda son del 24/10: 723 en el backend y 435 en el front). Desde cada proyecto: `./.venv/Scripts/python.exe -m pytest -q`.
  - Si falla `apps/ingresos/tests.py::test_un_registro_que_no_cumple_responde_400_con_todos_los_motivos_y_no_deja_fila` y es de noche (entre las 22:00 y las 05:00), es la falla conocida que depende de la hora: anotarlo y seguir.
- Tipos de prueba: unitarias por app, prueba del intruso (aislamiento), concurrencia con hilos sobre PostgreSQL real y pruebas del esquema. **Fuente:** guía §6 *Pruebas* y [pruebas_y_ejecucion](../02_Arquitectura/pruebas_y_ejecucion.md), la sección *Qué cubre cada archivo*.
- Recuadro ámbar: reporte de cobertura con `pytest-cov`, mínimo 70 % (A2).

### 9. Proceso de desarrollo
- Scrum con tablero en Notion (enlace público en [tareas](tareas.md)).
- Ramas y PR: el backend tiene 7 PR y el front 5 (verificado en GitHub el 2026-11-14); desde el 24/10 todo cambio entra por PR.
- Recuadros ámbar: CI con GitHub Actions (C2) y análisis con SonarQube (C1).

### Anexo A. Endpoints de la API
- Pasar [datos/endpoints_api.md](datos/endpoints_api.md): 97 rutas reales, con sus métodos y su vista. Una tabla por módulo, en carta vertical como el resto del documento.
- 74 rutas no tienen descripción, porque su vista no tiene *docstring*. Escribir una frase corta para cada una a partir del nombre de la vista y, si hace falta, de su código en `Backend/Admind_Backend/apps/<app>/views.py`.
  - Ejemplo: `ConjuntosDisponiblesView` → "Lista los conjuntos a los que puede entrar quien inició sesión".
  - Si no queda claro, dejarla en blanco antes que inventar.
- Corregir la frase de arriba de la tabla: las rutas sin token son las de ingreso, recuperación de contraseña y restablecimiento. Verificarlas en `apps/cuentas/views.py` (las que tengan `permission_classes` abiertas).
- Para regenerar la lista, el script `10_Sustentacion/datos/scripts/endpoints.py` se corre igual que el del diccionario ([plan_F0_diccionario](plan_F0_diccionario.md)), con la variable `ENDPOINTS_SALIDA`.

### Anexo B. Glosario
- Diez a quince términos del proyecto: conjunto activo, franja, bloqueo, regla alfa, regla beta, FK compuesta, huella del token, TOTP, prueba del intruso, auditoría, etc. **Fuente:** [glosario](../01_Contexto/glosario.md); elegir solo los técnicos.

## Al terminar
- Exportar a PDF y revisar:
  - la tabla de contenido;
  - que ningún recuadro "En implementación" diga algo como hecho;
  - que no aparezca ningún valor secreto;
  - que el diagrama se lea en el PDF.
- Decirle a Alejo qué notas de la bóveda no coincidían con el código, si encontró alguna.

## Ver también

- [estilo_entregables](estilo_entregables.md) — colores, fuentes, portada y salida
- [tareas](tareas.md) — lo que está en implementación y quién lo hace
- [Admind_Guia_Sustentacion_Tecnica](../Guias/Admind_Guia_Sustentacion_Tecnica.md) — la fuente principal
