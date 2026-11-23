# -*- coding: utf-8 -*-
"""Parte 4: capítulos 7 (Configuración e instalación), 8 (Pruebas) y 9 (Proceso de desarrollo)."""
from ooxml import hipervinculo, parrafo, run

URL_BACK = "https://github.com/ZeroFour-04/Admind_Backend"
URL_FRONT = "https://github.com/ZeroFour-04/Admind_Front-End"
URL_NOTION = "https://useful-vest-416.notion.site/Seguimiento-Scrum-2-0-AdMind-3f1739efa3338109b3f1e256d441de64"

# Resultado de correr las dos suites el 2026-11-14 sobre `main` (backend b89d9f2, frontend bdcb5c3)
PRUEBAS_BACK = ("823", "64 s")
PRUEBAS_FRONT = ("508", "13 s")


def enlace(d, etiqueta, url):
    d.add(parrafo(run(etiqueta + ": ", bold=True) + hipervinculo(url, url), estilo="Lista", num=(1, 0)))


def capitulo_7(d):
    d.h1("7. Configuración e instalación")

    # ---- 7.1
    d.h2("7.1 Repositorios y ramas")
    d.p("El código está en dos repositorios públicos de GitHub, uno por proyecto:", keep_next=True)
    enlace(d, "Backend (API)", URL_BACK)
    enlace(d, "Frontend", URL_FRONT)
    d.p("El modelo de ramas es el que fijó el curso, más una rama corta por cada cambio:", keep_next=True)
    d.tabla(
        ["Rama", "Qué contiene"],
        [
            ["`main`", "Lo entregado. Recibe de `pruebas` al cerrar el sprint"],
            ["`desarrollo`", "Integración: aquí se reúne el trabajo de los dos integrantes"],
            ["`pruebas`", "Lo terminado, listo para probar: es el ambiente de pruebas de la definición de terminado"],
            ["Rama corta", "Una por cambio, creada desde `desarrollo` (por ejemplo `feat/areas-listar`). Entra a "
                           "`desarrollo` con un pull request y se borra al fusionarse. Es la práctica desde el "
                           "24 de octubre"],
        ],
        [2000, 7360], mono=(0,), junta=True,
    )
    d.p("Hoy, en GitHub, el frontend tiene las tres ramas del curso; el backend tiene `main` y `desarrollo`.")

    # ---- 7.2
    d.h2("7.2 Instalación local, paso a paso")
    d.p("Requisitos previos: los de la sección 2.3, con el servicio de PostgreSQL 18 encendido. Los comandos son "
        "los mismos en los dos proyectos salvo donde se indica; los pasos 5 a 7 son solo del backend, porque el "
        "frontend no tiene base de datos.")

    d.h3("Paso 1. Clonar los repositorios")
    d.codigo([
        f"git clone {URL_BACK}.git",
        f"git clone {URL_FRONT}.git",
    ])
    d.h3("Paso 2. Crear el entorno virtual (en cada proyecto)")
    d.codigo([
        "cd Admind_Backend",
        "python -m venv .venv",
        "",
        "# Activarlo, según el sistema:",
        ".venv\\Scripts\\Activate.ps1          # Windows (PowerShell)",
        "source .venv/Scripts/activate        # Windows (Git Bash)",
        "source .venv/bin/activate            # Linux y macOS",
    ])
    d.h3("Paso 3. Instalar las dependencias (en cada proyecto)")
    d.codigo(["pip install -r requirements.txt"])
    d.h3("Paso 4. Crear el archivo .env (en cada proyecto)")
    d.p("El archivo `.env` guarda los secretos y no se sube a Git. En el backend se parte de la plantilla "
        "`.env _ejemplo`; el frontend no trae plantilla, así que se crea. Cada variable se explica en la "
        "sección 7.3. Una clave secreta nueva se genera con:", keep_next=True)
    d.codigo([
        "python -c \"from django.core.management.utils import get_random_secret_key; "
        "print(get_random_secret_key())\"",
    ])
    d.p("Contenido mínimo del `.env` del backend:", keep_next=True)
    d.codigo([
        "DJANGO_SECRET_KEY=<clave secreta>",
        "DB_NAME=admind_db",
        "DB_USER=<usuario de la base>",
        "DB_PASSWORD=<contraseña de la base>",
    ])
    d.p("Contenido mínimo del `.env` del frontend:", keep_next=True)
    d.codigo([
        "DJANGO_SECRET_KEY=<otra clave secreta>",
        "ADMIND_API_URL=http://127.0.0.1:8000",
    ])
    d.h3("Paso 5. Crear la base de datos y su usuario (solo backend)")
    d.p("Desde `psql` o pgAdmin, con un usuario administrador de PostgreSQL. El permiso `CREATEDB` hace falta "
        "porque las pruebas crean y borran su propia base:", keep_next=True)
    d.codigo([
        "CREATE USER <usuario> WITH PASSWORD '<contraseña>' CREATEDB;",
        "CREATE DATABASE admind_db OWNER <usuario>;",
    ])
    d.h3("Paso 6. Crear las tablas (solo backend)")
    d.codigo(["python manage.py migrate"])
    d.h3("Paso 7. Crear usuarios de prueba (solo backend)")
    d.codigo(["python manage.py crear_usuarios_prueba"])
    d.p("El comando crea un «Conjunto de prueba» y un usuario por rol (por ejemplo, `administracion@example.com` y "
        "`residente@example.com`), todos con la contraseña que se escriba cuando la pide. Solo funciona con "
        "`DEBUG` activo.")
    d.h3("Paso 8. Arrancar los dos servidores")
    d.p("Un servidor por terminal, cada uno con su entorno virtual activo y desde la carpeta de su proyecto. "
        "Primero la API:", keep_next=True)
    d.codigo([
        "python manage.py runserver 8000     # backend (API)",
        "python manage.py runserver 8001     # frontend, en otra terminal",
    ])
    d.p("Después se abre `http://127.0.0.1:8001` en el navegador y se ingresa con uno de los usuarios de prueba.")
    d.nota("Para probar una reserva de punta a punta, el residente debe estar vinculado a una vivienda con «reside» "
           "y debe existir un área común activa con reserva. Ambas cosas se crean desde las pantallas de Viviendas "
           "y Áreas comunes, entrando como Administración.", titulo="Para probar una reserva")

    # ---- 7.3
    d.h2("7.3 Variables de entorno")
    d.p("Se leen del archivo `.env` con `python-dotenv`. Estos son los nombres que usan los `settings.py`; los "
        "valores no van en este manual ni en el repositorio.", keep_next=True)
    d.tabla(
        ["Variable", "Proyecto", "Para qué sirve", "Obligatoria"],
        [
            ["`DJANGO_SECRET_KEY`", "Ambos", "Clave secreta de Django (firma de sesiones y enlaces). Cada proyecto "
                                            "usa la suya", "Sí"],
            ["`DB_NAME`", "Backend", "Nombre de la base de datos (`admind_db`)", "Sí"],
            ["`DB_USER`", "Backend", "Usuario de la base de datos", "Sí"],
            ["`DB_PASSWORD`", "Backend", "Contraseña de ese usuario", "Sí"],
            ["`ADMIND_FRONT_URL`", "Backend", "Dirección del frontend a la que apuntan los enlaces de los correos. "
                                            "Por defecto, `http://127.0.0.1:8001`", "No"],
            ["`EMAIL_HOST`", "Backend", "Servidor SMTP. Sin él, los correos salen por la consola del servidor",
             "No"],
            ["`EMAIL_PORT`", "Backend", "Puerto SMTP (587 por defecto). Solo se usa con `EMAIL_HOST`", "No"],
            ["`EMAIL_HOST_USER`", "Backend", "Usuario del servidor SMTP", "No"],
            ["`EMAIL_HOST_PASSWORD`", "Backend", "Contraseña del servidor SMTP", "No"],
            ["`DEFAULT_FROM_EMAIL`", "Backend", "Remitente de los correos. Por defecto, "
                                              "`AdMind <no-responder@admind.local>`", "No"],
            ["`ADMIND_API_URL`", "Frontend", "Dirección de la API (`http://127.0.0.1:8000` en local)", "Sí"],
        ],
        [2400, 1100, 4760, 1100], centro=(1, 3), junta=False,
    )
    d.p("Otros datos de configuración están escritos en `config/settings.py`: la base de datos se busca siempre en "
        "`localhost:5432`, la zona horaria es `America/Bogota` y el idioma, `es-co`. La API envía hoy dos correos, "
        "ambos en texto plano: la recuperación de contraseña y el restablecimiento del segundo factor.")
    d.implementacion(
        "Correo en HTML con el logo de AdMind. Está previsto pasar esos dos correos a texto más HTML, con una "
        "plantilla base (encabezado verde con el logo, cuerpo y pie) y el logo incrustado para que Gmail lo muestre "
        "siempre.")

    # ---- 7.4
    d.h2("7.4 Despliegue")
    d.implementacion([
        "Despliegue en la nube. Hoy AdMind corre solo en local: los dos `settings.py` tienen `DEBUG = True` y "
        "`ALLOWED_HOSTS` vacío, y no hay configuración de producción.",
        "Está previsto desplegar en Render con tres servicios: la API y el frontend como servicios web (con "
        "`gunicorn` y `WhiteNoise` para los archivos estáticos) y una base PostgreSQL. `DEBUG`, `ALLOWED_HOSTS`, "
        "los datos de la base y las cookies seguras se tomarán del entorno. El correo en la nube saldrá por la "
        "API HTTP de Brevo, porque el plan gratuito de Render bloquea SMTP.",
    ])


def capitulo_8(d):
    d.h1("8. Pruebas")
    d.p("Resultado de correr las dos suites completas el 14 de noviembre de 2026 sobre la rama `main` (backend "
        "`b89d9f2`, frontend `bdcb5c3`):", keep_next=True)
    d.tabla(
        ["Suite", "Pruebas", "Resultado", "Tiempo"],
        [
            ["Backend", f"**{PRUEBAS_BACK[0]}**", "Todas pasan", PRUEBAS_BACK[1]],
            ["Frontend", f"**{PRUEBAS_FRONT[0]}**", "Todas pasan", PRUEBAS_FRONT[1]],
        ],
        [2400, 2000, 2960, 2000], centro=(1, 3), junta=True,
    )
    d.p("Se corren desde la carpeta de cada proyecto, con su entorno virtual activo:", keep_next=True)
    d.codigo(["python -m pytest -q"])

    d.h2("8.1 Cómo se escriben")
    d.p("Son funciones `def test_…():` con `assert`. `pytest-django` entrega una base de datos de prueba que se "
        "crea y se borra sola.")
    d.vinetas([
        "**Backend:** usa `config/settings_pruebas.py`, que fija `pytest.ini`. Agrega una app de apoyo "
        "(`tests.aislamiento`) y un cifrado de contraseñas rápido. Las pruebas corren contra PostgreSQL real.",
        "**Frontend:** no tiene base de datos ni API de verdad. Las pruebas simulan la API con "
        "`mock.patch(\"cliente_api.reservas.franjas\", return_value=…)` y revisan el HTML que sale.",
    ])

    d.h2("8.2 Tipos de prueba")
    d.tabla(
        ["Tipo", "Dónde", "Qué verifica"],
        [
            ["Unitarias y de API, por app", "`apps/<app>/tests.py` y `test_*.py`",
             "La lógica de cada módulo: servicios, vistas según el rol y restricciones de la base"],
            ["Prueba del intruso (aislamiento)", "`tests/aislamiento/`",
             "Todas las rutas de la API actuando desde otro conjunto. Una ruta nueva que no se registre pone la "
             "prueba en rojo. También el filtro por conjunto del Manager"],
            ["Concurrencia", "`tests/concurrencia/`",
             "Hilos contra PostgreSQL real: varias personas sobre la misma franja dejan un solo bloqueo; diez "
             "registros sobre el último cupo dejan uno solo adentro; diez sobre el mismo puesto de visitantes "
             "dejan una sola visita con él"],
            ["Esquema", "`tests/esquema/`",
             "La lista cerrada de tablas globales: falla si aparece una tabla sin `conjunto_id`"],
            ["Archivos", "`tests/archivos/`", "La validación de un archivo por su firma, sin tocar la base"],
            ["Pantallas del frontend", "`tests/` del frontend",
             "Cada pantalla con la API simulada: qué muestra, qué oculta sin permiso y cómo presenta los errores"],
        ],
        [2500, 2500, 4360], junta=True,
    )
    d.h2("8.3 Lo que las pruebas automáticas no cubren")
    d.vinetas([
        "**El JavaScript propio** (el recortador de foto, el calendario, los buscadores y el generador de viviendas "
        "del asistente): se prueba a mano.",
        "**La prueba manual de la definición de terminado:** recorrer cada historia en el navegador con usuarios "
        "reales, a cargo de quien no la programó.",
    ])
    d.implementacion(
        "Reporte de cobertura. Hoy no se mide la cobertura. Está previsto agregar `pytest-cov` al backend, medir "
        "`apps/` sin migraciones ni archivos de prueba y exigir un mínimo de 70 %, con el reporte HTML como "
        "evidencia.")


def capitulo_9(d):
    d.h1("9. Proceso de desarrollo")
    d.h2("9.1 Metodología")
    d.p("El equipo, de dos personas, trabaja con **Scrum**: 40 historias de usuario repartidas en 7 sprints, con "
        "puntos de historia (188 puntos en las 38 del backlog). El tablero está en Notion y su enlace público es:",
        keep_next=True)
    d.add(parrafo(hipervinculo(URL_NOTION, URL_NOTION), estilo="Lista", num=(1, 0)))
    d.p("**Definición de terminado:** las pruebas en verde, la prueba del intruso y la prueba manual de quien no "
        "programó la historia.")

    d.h2("9.2 Ramas, commits y pull requests")
    d.vinetas([
        "**Tres repositorios separados** (no submódulos): backend, frontend y documentación, esta última en una "
        "bóveda de Obsidian.",
        "**Desde el 24 de octubre, todo cambio entra por pull request:** una rama corta desde `desarrollo`, un "
        "pull request hacia `desarrollo`. El backend registra 7 pull requests y el frontend 5 (consulta a GitHub "
        "del 14 de noviembre de 2026).",
        "**Mensajes de commit** con el formato `feat(app): descripción [HU-NN]`, que enlaza cada commit con su "
        "historia.",
        "**Migraciones:** `makemigrations` las genera y, a mano, se agrega `fk_compuesta(...)` al final de cada "
        "migración con claves compuestas. `makemigrations --check` compara los modelos con las migraciones.",
    ])
    d.implementacion(
        "Integración continua con GitHub Actions. Hoy las pruebas se corren a mano. Está previsto un flujo que, en "
        "cada `push` y pull request, instale las dependencias, revise las migraciones y corra las pruebas (el "
        "backend con una base PostgreSQL de servicio), y que ningún pull request se funda con la integración en "
        "rojo.")
    d.implementacion(
        "Análisis de calidad con SonarQube (SonarCloud). Hoy el código no se analiza. Está previsto escanear los "
        "dos repositorios antes de cualquier cambio y de nuevo al cerrar, para mostrar la disminución de "
        "vulnerabilidades y problemas, y que cada integrante corrija al menos una vulnerabilidad alta o media.")


def construir(d):
    capitulo_7(d)
    capitulo_8(d)
    capitulo_9(d)
