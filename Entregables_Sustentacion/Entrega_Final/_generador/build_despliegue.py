# -*- coding: utf-8 -*-
"""Arma 'Despliegue de Aplicaciones Empresariales - Entrega Final Proyecto de Curso'.

Uso: python build_despliegue.py <salida.docx>
Sin fechas en ninguna parte. Sin datos del servidor (IP, usuario o llave de SSH, secretos).
"""
import os
import struct
import sys

from ooxml_desp import (
    G500, V600, V900, Doc, hipervinculo, imagen, parrafo, ppr, run,
)

AQUI = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(AQUI, "logo-marca.png")
QR = os.path.join(AQUI, "..", "..", "capturas", "qr_admind.png")

TITULO = "Despliegue de Aplicaciones Empresariales - Entrega Final Proyecto de Curso"
NOMBRES = ["MANUEL ALEJANDRO ALDANA RINCON", "ANDERSON CAMILO REMISO NIÑO"]

URL_APP = "https://admind.detkor.com"
URL_BACK = "https://github.com/ZeroFour-04/Admind_Backend"
URL_FRONT = "https://github.com/ZeroFour-04/Admind_Front-End"
URL_SONAR_B = "https://sonarcloud.io/project/overview?id=ZeroFour-04_Admind_Backend"
URL_SONAR_F = "https://sonarcloud.io/project/overview?id=ZeroFour-04_Admind_Front-End"
URL_NOTION = "https://useful-vest-416.notion.site/Seguimiento-Scrum-2-0-AdMind-3f1739efa3338109b3f1e256d441de64"

ROL_PRUEBA = "Residente"  # confirmado por Alejo


def enlace(etiqueta, url):
    """Párrafo: etiqueta en texto y la URL como hipervínculo."""
    return run(etiqueta) + hipervinculo(url, url)


def portada(d):
    d.add(parrafo(" ", antes=0, despues=0, linea=(240, "exact")))
    d.add(f"<w:p>{ppr(alinear='center', antes=0, despues=360)}"
          f"{imagen('rIdLogo', 1800000, 1800000, 'Logo AdMind', 800, 'Logo de AdMind')}</w:p>")
    banda = parrafo(run(" ", size=8), sombra=V600, antes=0, despues=0, linea=(300, "exact"))
    d.add(banda)
    d.add(parrafo(TITULO, estilo="Title", antes=480, despues=160))
    d.add(parrafo("AdMind — Plataforma de administración de conjuntos residenciales",
                  estilo="Subtitle", despues=480))
    d.add(banda)

    def dato(etiqueta, valor, antes=400):
        valores = valor if isinstance(valor, (list, tuple)) else [valor]
        d.add(parrafo(run(etiqueta.upper(), color=G500, size=19, bold=True), alinear="center", antes=antes,
                      despues=20, linea=(240, "auto"), keep_next=True))
        for v in valores:
            d.add(parrafo(run(v, color=V900, size=28, bold=True), alinear="center", antes=0, despues=0,
                          linea=(260, "auto")))

    dato("Integrantes", NOMBRES, antes=560)
    dato("Asignatura", "Ingeniería de Software II")
    dato("Docente", "Oscar Gómez")
    dato("Universidad", "Universidad de Cundinamarca")
    # El salto va en el título del índice: un párrafo de salto aparte desbordaba la portada.
    d.add(parrafo("Contenido", estilo="TituloContenido", page_break_before=True))
    d.add(
        "<w:p>"
        '<w:r><w:fldChar w:fldCharType="begin"/></w:r>'
        '<w:r><w:instrText xml:space="preserve"> TOC \\o "1-2" \\h \\z \\u </w:instrText></w:r>'
        '<w:r><w:fldChar w:fldCharType="separate"/></w:r>'
        + run("El índice se genera al abrir el documento en Word.", italic=True, color=G500)
        + '<w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>'
    )


# ------------------------------------------------------------------ 1
def seccion_1(d):
    d.h1("1. Presentación del proyecto")
    d.p("AdMind es una aplicación web para administrar conjuntos residenciales en Colombia, regidos por la "
        "Ley 675 de 2001 de propiedad horizontal. Reemplaza los grupos de WhatsApp y las hojas de cálculo con las "
        "que hoy se administra la mayoría de los conjuntos: reservas de zonas comunes, casos y solicitudes, "
        "anuncios, visitantes, parqueaderos, pagos de administración e infracciones, cada uno con sus permisos "
        "por rol.")
    d.p("Una **sola base de datos** guarda a muchos conjuntos, y ese es el reto técnico central: que ningún "
        "conjunto vea ni toque los datos de otro. El sistema son dos proyectos de Django: una **API** (Django REST "
        "Framework y PostgreSQL) y un **frontend** de plantillas con Alpine.js que habla con la API desde el "
        "servidor. Los roles son cinco:", keep_next=True)
    d.tabla(
        ["Rol", "Qué hace"],
        [
            ["Superusuario", "Opera la plataforma: crea conjuntos y anula registros"],
            ["Administración", "Configura reglas, áreas y personas, y aprueba reservas"],
            ["Secretaría", "Clasifica casos y solicitudes y publica anuncios; no aprueba"],
            ["Vigilancia", "Registra visitantes e ingresos a zonas comunes"],
            ["Residente", "Reserva zonas, abre casos y ve anuncios y documentos"],
        ],
        [2200, 7160], junta=True,
    )


# ------------------------------------------------------------------ 2
def seccion_2(d):
    d.h1("2. Documentación final según la metodología")
    d.h2("2.1 Scrum con seguimiento en Notion")
    d.p("El equipo trabajó con Scrum: un backlog de historias de usuario (HU) estimadas en story points con "
        "*poker planning*, ocho sprints y una definición de terminado (DoD) con revisión cruzada. El seguimiento "
        "está en un tablero público de Notion con tres bases relacionadas: **Historias de Usuario** (el "
        "backlog), **Tareas** (cada HU se parte en tareas de backend, frontend y pruebas) y **Sprints** "
        "(puntos comprometidos y completados, y la velocidad para planear el siguiente).", keep_next=True)
    d.p(enlace("Tablero: ", URL_NOTION))
    d.vinetas([
        "Una HU suma puntos solo en *Finalizado*, y solo debe llegar ahí con la DoD marcada: el pull request "
        "revisado por el otro integrante y la prueba manual hecha por quien no programó la HU.",
        "Lo que no se termina vuelve al backlog con sus puntos intactos.",
        "Las HU dependen unas de otras, así que el tablero tiene el campo «Depende de». Al principio costó cerrar "
        "HU al 100 % por esas dependencias; se redistribuyeron y el avance mejoró desde los sprints 4 y 5.",
        "Los requisitos nuevos de la universidad y de la sustentación técnica hicieron crecer el sprint 7 y "
        "dieron origen al sprint 8 (Sonar, despliegue, procedimientos y triggers, reportes, correo, documentación).",
    ])
    d.h2("2.2 Avance por sprint")
    d.p("Los puntos son los que suma el tablero: una HU cuenta como completada solo cuando está en "
        "*Finalizado*.", keep_next=True)
    d.tabla(
        ["Sprint", "Historias", "SP comprometidos", "SP completados", "Cumplimiento"],
        [
            ["1", "6", "25", "25", "100 %"],
            ["2", "4", "20", "20", "100 %"],
            ["3", "4", "26", "26", "100 %"],
            ["4", "6", "28", "28", "100 %"],
            ["5", "7", "33", "28", "85 %"],
            ["6", "8", "38", "30", "79 %"],
            ["7", "5", "31", "12", "39 %"],
            ["8", "19", "86", "38", "44 %"],
            ["**Total**", "**59**", "**287**", "**207**", "**72 %**"],
        ],
        [1400, 1700, 2200, 2160, 1900], centro=(0, 1, 2, 3, 4), tam=19, junta=True,
    )
    d.p("Los sprints 1 a 7 están cerrados y el 8 sigue en curso. Los sprints 1 a 4 cerraron con todos sus puntos. "
        "En los sprints 5 a 7 quedaron sin empezar HU-20, HU-32, HU-36, HU-37 y HU-38. El sprint 8 sigue con HU "
        "abiertas: HU-45, HU-46 y HU-47 (Sonar, despliegue y ajustes de producción) en progreso, HU-50 y HU-51 (JWT "
        "y CORS) en progreso pero sin código en `main`, HU-52 (Swagger) y HU-55 (bug de casos) sin empezar, y "
        "HU-39, HU-40 de accesibilidad y HU-43 en revisión. El detalle de los sprints, las reglas y las lecciones "
        "aprendidas está en el documento de metodología ágil.")
    d.h2("2.3 Entregables de documentación")
    d.tabla(
        ["Documento", "Qué contiene", "Archivo"],
        [
            ["Manual Técnico", "Requerimientos, arquitectura, seguridad, API, tecnologías, instalación, pruebas y "
                               "proceso de desarrollo", "AdMind_Manual_Tecnico.pdf"],
            ["Manual de Usuario", "Uso de las pantallas de AdMind, explicado por rol", "AdMind_Manual_Usuario_vf.pdf"],
            ["Diccionario de Datos", "Cada tabla de la base de datos, sus columnas y su significado de negocio",
             "AdMind_Diccionario_de_Datos.xlsx y .pdf"],
            ["Metodología Ágil", "Scrum en Notion: tablero, reglas, planeación, sprints y lecciones",
             "Entrega_Documentacion_Metodologia_Agil.pdf"],
            ["Entrega del Código", "Los repositorios, las herramientas de calidad y el flujo de Git",
             "Entrega_Codigo_del_Proyecto.pdf"],
        ],
        [2000, 4160, 3200], mono=(2,), junta=True,
    )


# ------------------------------------------------------------------ 3
def seccion_3(d):
    d.h1("3. Documento de sustentación", salto=False)
    d.p("La tabla recorre los 12 criterios de la rúbrica del curso: cómo se cumple cada uno y dónde se ve. Lo "
        "que no está hecho se escribe como **No implementado**, con su explicación técnica.")
    d.tabla(
        ["Criterio", "Cómo se cumple", "Evidencia"],
        [
            ["1. UX/UI",
             "Sistema de diseño propio (componentes `am-*` y color de acento por conjunto), pantallas por rol, menú "
             "que solo muestra lo que el rol puede usar y páginas de error propias.",
             "Manual de Usuario y la aplicación desplegada"],
            ["2. Roles y permisos",
             "Catálogo fijo de 5 roles. Cada vista de la API exige su permiso en la primera línea y responde 403 si "
             "falta; el frontend solo decide qué mostrar. Una prueba recorre todas las rutas como usuario de otro "
             "conjunto y comprueba que no ve ni toca sus datos.",
             "`tests/aislamiento/test_intruso.py` y Manual Técnico (Autorización)"],
            ["3. Pruebas y cobertura (70 %)",
             "Backend: 823 pruebas con 94 % de cobertura. Frontend: 523 pruebas. El CI falla si la cobertura del "
             "backend baja del 70 %.",
             "Pestaña *Actions* de cada repositorio (el informe `htmlcov` se guarda como artefacto)"],
            ["4. Integración continua",
             "GitHub Actions corre en cada pull request y en cada `push` a `main`, `desarrollo` y `pruebas`: "
             "instala dependencias, revisa migraciones y corre las pruebas.",
             "Pestaña *Actions* de cada repositorio; sección 4.7"],
            ["5. Seguridad",
             "Token de sesión opaco guardado en una tabla (cerrar sesión lo invalida de verdad), segundo factor "
             "TOTP para los roles con permisos sensibles, HTTPS en el borde de Cloudflare, cookies de sesión y CSRF "
             "seguras, `DEBUG` apagado, API sin publicar y secretos fuera de los repositorios.",
             "Sección 4.8 y Manual Técnico (Seguridad)"],
            ["6. Correo automático",
             "Los avisos de anuncios, casos, infracciones, ingresos y la decisión de una reserva salen por correo en "
             "HTML con el logo de AdMind, desde un único canal (`por_correo`, con `send_mass_mail`).",
             "Correo recibido en una bandeja de Gmail"],
            ["7. Despliegue",
             "Máquina virtual en Oracle Cloud con servicios de `systemd`, Cloudflare Tunnel y despliegue continuo "
             "con cada `push` a `main`.",
             "Sección 4 y enlace de la sección 5"],
            ["8. Base de datos",
             "PostgreSQL con 4 funciones (`fn_ocupacion_areas`, `fn_resumen_casos`, `fn_aforo_actual`, "
             "`fn_estado_pagos`), 1 procedimiento (`sp_expirar_bloqueos_vencidos`) y 5 triggers en migraciones: "
             "cuatro `trg_sin_borrado_fisico` (casos, infracciones, pagos y reservas) y "
             "`trg_infraccion_anulada_inmutable`. Las funciones devuelven datos para consultar; el procedimiento "
             "ejecuta una acción que modifica filas.",
             "Diccionario de Datos; `\\df` e `information_schema.triggers` en `psql`"],
            ["9. Reportes",
             "Reportes en PDF (reportlab) y Excel (openpyxl) de zonas, pagos y reservas, desde la pantalla "
             "`/reportes/`.",
             "Archivos descargados desde la aplicación desplegada"],
            ["10. SonarQube",
             "SonarCloud analiza los pull requests y `main` de los dos repositorios; su resultado es un check más de "
             "GitHub. **Pendiente:** corregir las vulnerabilidades que marca y hacer el segundo escaneo.",
             "Enlaces de SonarCloud, sección 6"],
            ["11. JWT y CORS",
             "**No implementado.** Hoy el token de sesión es opaco: una cadena aleatoria guardada en una tabla que "
             "el servidor consulta en cada petición. Por eso cerrar sesión lo invalida al instante; un JWT firmado "
             "sigue siendo válido hasta que expira, salvo que se agregue una lista de revocación. CORS no entra en "
             "juego: el navegador nunca llama a la API, la llama el frontend de Django desde el servidor "
             "(`cliente_api`), y ninguna plantilla ni script del frontend hace `fetch` a la API.",
             "Manual Técnico (Seguridad y API)"],
            ["12. Swagger",
             "**No implementado.** `drf-spectacular` no está en el proyecto. La API no se publica en internet "
             "(escucha solo en `127.0.0.1` y no tiene nombre público), así que una página interactiva no tendría "
             "desde dónde abrirse. Los endpoints se documentan en el Manual Técnico.",
             "Manual Técnico (API)"],
        ],
        [1700, 5260, 2400], junta=False, tam=19,
    )
    d.nota("En los `requirements.txt` de `main` de los dos repositorios no hay PyJWT, django-cors-headers ni "
           "drf-spectacular, y en el código no hay nada de JWT, CORS ni Swagger. Por eso los criterios 11 y 12 "
           "figuran como no implementados.", titulo="Comprobación")


# ------------------------------------------------------------------ 4
def seccion_4(d):
    d.h1("4. Despliegue")
    d.p("AdMind corre en una sola máquina virtual de Oracle Cloud. Esta sección explica cómo llega una petición "
        "desde el navegador hasta la base de datos, cómo se publica cada cambio de `main` y, en cada paso, por "
        "qué se decidió así.")

    # ---- 4.1
    d.h2("4.1 Arquitectura de despliegue")
    d.p("El despliegue tiene dos recorridos independientes. Se muestran como pasos numerados: la primera tabla "
        "es el camino de una petición del usuario y la segunda, el camino de un cambio desde GitHub hasta el "
        "servidor.", keep_next=True)
    d.p("**Recorrido 1 · Una petición del usuario**", keep_next=True)
    d.tabla(
        ["Paso", "Componente", "Qué ocurre", "Dónde escucha"],
        [
            ("grupo", "Fuera del servidor"),
            ["1", "Navegador", "La persona abre `https://admind.detkor.com`.", "—"],
            ["2", "Cloudflare", "Resuelve el DNS, termina el HTTPS (el certificado está en el borde) y entrega "
                                "la petición al túnel.", "Borde de Cloudflare"],
            ("grupo", "Dentro del VPS en Oracle Cloud (Ubuntu 24.04.4 LTS)"),
            ["3", "`cloudflared`\n(Cloudflare Tunnel)", "Mantiene una conexión cifrada **saliente** hacia "
                                                         "Cloudflare y por ella recibe las peticiones.",
             "Solo salida; sin puertos de entrada"],
            ["4", "gunicorn del frontend\n(con whitenoise)", "Django con plantillas atiende la pantalla y sirve "
                                                              "los estáticos comprimidos.", "`127.0.0.1:8001`"],
            ["5", "gunicorn de la API", "Django REST Framework. El frontend la llama desde el servidor; el "
                                        "navegador nunca la ve.", "`127.0.0.1:8000`"],
            ["6", "PostgreSQL 16", "Guarda los datos de todos los conjuntos.", "Misma máquina"],
        ],
        [700, 2300, 4260, 2100], centro=(0,), tam=19,
    )
    d.pie("Recorrido 1. De arriba abajo: cada paso entrega la petición al siguiente.")
    d.p("**Recorrido 2 · Un cambio que llega a main**", keep_next=True)
    d.tabla(
        ["Paso", "Componente", "Qué ocurre", "Dónde escucha"],
        [
            ("grupo", "GitHub"),
            ["1", "`push` a `main`", "Un pull request se funde en `main` del backend o del frontend.", "—"],
            ["2", "Webhook de GitHub", "GitHub envía el evento a `https://deploy-admind.detkor.com/github`.", "—"],
            ("grupo", "Dentro del VPS"),
            ["3", "Cloudflare y túnel", "El webhook entra por el mismo túnel de la aplicación.",
             "Solo salida; sin puertos de entrada"],
            ["4", "`admind-webhook`", "Valida la firma HMAC SHA-256, acepta solo `push` a `main` de los dos "
                                      "repositorios y deja un trabajo en la cola.", "`127.0.0.1:8010`"],
            ["5", "`admind-deploy-queue`", "`systemd` detecta el trabajo y lanza `deploy_queue.py`.", "—"],
            ["6", "Scripts de despliegue", "Backend: actualizar código, dependencias, migraciones y reinicio. "
                                           "Frontend: actualizar código, dependencias, estáticos y reinicio.",
             "—"],
        ],
        [700, 2300, 4260, 2100], centro=(0,), tam=19,
    )
    d.pie("Recorrido 2. El detalle de cada paso está en las secciones 4.4 y 4.6.")
    d.p("Tres decisiones definen esta forma, y cada una se explica más adelante:", keep_next=True)
    d.vinetas([
        "**Una sola máquina, con la base de datos incluida:** el proyecto es de dos personas y no necesita más "
        "piezas que operar.",
        "**La API no se publica.** Escucha solo en `127.0.0.1` y el único cliente es el frontend, dentro del "
        "servidor.",
        "**Entrada por un túnel saliente** en lugar de abrir puertos (sección 4.4).",
    ])

    # ---- 4.2
    d.h2("4.2 Infraestructura")
    d.tabla(
        ["Componente", "Versión o valor", "Nota"],
        [
            ["Máquina virtual", "Oracle Cloud · x86_64", "2 vCPU, cerca de 1 GB de RAM y 96 GB de disco"],
            ["Sistema operativo", "Ubuntu 24.04.4 LTS", "Versión de soporte extendido"],
            ["Python", "3.12.3", "En el servidor. Se desarrolla con 3.14"],
            ["Base de datos", "PostgreSQL 16", "En la misma máquina"],
            ["Django", "5.2.17", "Backend y frontend"],
            ["Django REST Framework", "3.18.1", "Solo backend"],
            ["gunicorn", "27.0.1", "Servidor de aplicación de los dos proyectos"],
            ["whitenoise", "6.12.0", "Sirve los estáticos desde gunicorn"],
            ["psycopg", "3.3.5", "Conexión del backend con PostgreSQL"],
            ["Cloudflare Tunnel", "`cloudflared`", "Publica el sitio sin abrir puertos de entrada"],
        ],
        [2800, 2700, 3860], tam=19, junta=True,
    )
    d.p("Los `requirements.txt` fijan cada dependencia con una versión exacta (`==`), de modo que el servidor "
        "instala lo mismo que se probó. Con 2 vCPU y cerca de 1 GB de RAM, dos *workers* de gunicorn por "
        "servicio es una configuración ajustada al tamaño de la máquina.")

    # ---- 4.3
    d.h2("4.3 Servicios del servidor")
    d.p("Cada pieza es un servicio de `systemd`. Los servicios de AdMind corren con un usuario sin privilegios, "
        "con `UMask=0077` (lo que crean solo lo puede leer su dueño) y se reinician solos si fallan.",
        keep_next=True)
    d.tabla(
        ["Servicio", "Qué corre", "Dónde escucha"],
        [
            ["`admind-backend`", "gunicorn 27.0.1 con 2 workers y `config.wsgi`. Arranca después de PostgreSQL.",
             "`127.0.0.1:8000`, solo dentro del servidor"],
            ["`admind-front`", "gunicorn 27.0.1 con 2 workers. Estáticos con whitenoise 6.12, comprimidos.",
             "`127.0.0.1:8001`"],
            ["`cloudflared`", "Cloudflare Tunnel.", "Sale hacia Cloudflare; no abre puertos de entrada"],
            ["`admind-webhook`", "Receptor de los webhooks de GitHub, escrito con la biblioteca estándar de Python.",
             "`127.0.0.1:8010`"],
            ["`admind-deploy-queue`\n(`.path` + `.service`)", "Procesa la cola de despliegues.", "—"],
        ],
        [2600, 4260, 2500], tam=19, junta=True,
    )
    d.vinetas([
        "**Por qué `systemd`:** reinicia lo que falla, ordena el arranque (la API espera a PostgreSQL) y permite "
        "aislar cada proceso con un usuario sin privilegios, sin instalar nada adicional.",
        "**Por qué `127.0.0.1`:** un servicio que escucha solo en el bucle local no es alcanzable desde fuera de "
        "la máquina, haya o no un firewall delante.",
    ])

    # ---- 4.4
    d.h2("4.4 Exposición a internet con Cloudflare Tunnel")
    d.p("Un sitio web normal abre el puerto 80 o el 443 en el servidor y publica su IP. AdMind hace lo "
        "contrario: `cloudflared` abre una conexión **saliente** hacia Cloudflare y las peticiones de los "
        "usuarios regresan por esa misma conexión.")
    d.vinetas([
        "**No hace falta abrir el 80 ni el 443.** La web no necesita ningún puerto de entrada: el tráfico "
        "llega por la conexión que el propio servidor abrió hacia Cloudflare.",
        "**El HTTPS está en el borde.** Cloudflare pone el DNS y el certificado; `http` se redirige a `https`. El "
        "tramo entre `cloudflared` y gunicorn es HTTP por el bucle local, dentro de la máquina.",
        "**Django sabe que el cliente usó HTTPS** porque Cloudflare envía la cabecera `X-Forwarded-Proto`, que "
        "los settings de producción declaran como `SECURE_PROXY_SSL_HEADER`. Sin eso, `SECURE_SSL_REDIRECT` y las "
        "cookies seguras no funcionarían detrás del túnel.",
        "**Dos nombres, un túnel.** `admind.detkor.com` lleva al frontend y `deploy-admind.detkor.com` al receptor "
        "de webhooks. La API no tiene nombre público.",
        "**Costo:** el sitio depende de Cloudflare. Es una dependencia aceptada a cambio de no operar certificados "
        "ni puertos expuestos.",
    ])

    # ---- 4.5
    d.h2("4.5 Configuración de producción")
    d.p("Los repositorios son públicos, así que ningún valor de producción puede vivir en ellos. Cada servicio "
        "usa un módulo de settings propio, guardado en el servidor en `/etc/admind/py/`, que **importa los "
        "settings del repositorio y sobrescribe solo lo que cambia**. El repositorio queda con valores de "
        "desarrollo y pruebas, y producción no tiene que modificar el código.", keep_next=True)
    d.tabla(
        ["Ajuste", "Frontend", "Backend"],
        [
            ["`DEBUG`", "`False`", "`False`"],
            ["`ALLOWED_HOSTS`", "`admind.detkor.com`", "Solo `127.0.0.1` y `localhost`"],
            ["`CSRF_TRUSTED_ORIGINS`", "`https://admind.detkor.com`", "—"],
            ["`SECURE_PROXY_SSL_HEADER`", "Cabecera `X-Forwarded-Proto`", "—"],
            ["`SECURE_SSL_REDIRECT`", "Activado", "—"],
            ["Cookies de sesión y CSRF", "Marcadas como seguras", "—"],
            ["Estáticos", "whitenoise y `STATIC_ROOT`", "`STATIC_ROOT`"],
        ],
        [3000, 3360, 3000], tam=19, junta=True,
    )
    d.vinetas([
        "**`DEBUG = False`** evita que un error muestre código, variables o configuración al visitante.",
        "**`ALLOWED_HOSTS` en el backend** acepta solo el bucle local: aunque la API fuera alcanzable, rechazaría "
        "cualquier otro nombre.",
        "**Las claves** (base de datos, correo y `SECRET_KEY`) viven en el servidor, fuera de los repositorios.",
    ])

    # ---- 4.6
    d.h2("4.6 Despliegue continuo")
    d.p("Cada `push` a `main` en el backend o en el frontend publica el cambio sin intervención humana:",
        keep_next=True)
    d.numerada([
        "**GitHub envía un webhook** a `https://deploy-admind.detkor.com/github`, que entra por el mismo túnel.",
        "**El receptor valida y encola.** `server.py` comprueba la firma **HMAC SHA-256** con un secreto "
        "compartido, acepta solo eventos `push` a `refs/heads/main` de los dos repositorios, descarta entregas "
        "repetidas, valida el commit y deja un trabajo en la cola (64 como máximo).",
        "**`systemd` lanza el despliegue.** Una unidad `.path` detecta el trabajo y arranca `deploy_queue.py`, que "
        "ejecuta el script del proyecto.",
        "**Backend:** `git pull --ff-only origin main`, `pip install -r requirements.txt`, `migrate` y reinicio "
        "del servicio.",
        "**Frontend:** `git pull --ff-only origin main`, `pip install`, `collectstatic` y reinicio del servicio.",
    ])
    d.p("Por qué se hizo así:", keep_next=True)
    d.vinetas([
        "**La firma HMAC se valida antes de hacer nada.** Sin el secreto compartido nadie más puede disparar un "
        "despliegue, aunque conozca la dirección del webhook.",
        "**Receptor y ejecutor están separados.** El receptor solo escribe un trabajo en la cola y corre con un "
        "usuario dedicado y el aislamiento de `systemd` (`ProtectSystem`, `NoNewPrivileges` y similares); quien "
        "ejecuta el despliegue es otro proceso, que `systemd` arranca al ver el trabajo.",
        "**La cola tiene tope y descarta repetidos:** una ráfaga de entregas no encadena despliegues "
        "sin límite.",
        "**`--ff-only`:** el servidor solo avanza en línea recta con `main`. Si su historia llegara a divergir, "
        "el despliegue falla en vez de mezclar o reescribir código en producción.",
        "**Orden de los pasos:** las migraciones corren antes del reinicio del backend, para que el código nuevo "
        "arranque con el esquema que espera; `collectstatic` corre antes del reinicio del frontend, para que "
        "whitenoise encuentre los archivos nuevos.",
    ])
    d.p("En el momento de redactar este documento, lo desplegado es igual a `main`: backend `2dd5c44` y "
        "frontend `10e2d04`.")

    # ---- 4.7
    d.h2("4.7 Integración continua y calidad")
    d.p("Antes de que un cambio llegue a `main`, GitHub Actions corre en cada pull request y en cada `push` a "
        "`main`, `desarrollo` y `pruebas`:", keep_next=True)
    d.vinetas([
        "**Backend:** levanta un PostgreSQL real, instala las dependencias, revisa que no falten migraciones "
        "(`makemigrations --check`) y corre `pytest` con cobertura. El paso falla si la cobertura baja del 70 %, "
        "y el informe `htmlcov` se guarda como artefacto.",
        "**Frontend:** instala las dependencias y corre `pytest`.",
        "**SonarCloud** analiza `main` de los dos repositorios, y su resultado aparece como un check más en "
        "GitHub.",
    ])
    d.p("La regla del equipo es no fundir ningún pull request con el CI en rojo. Como `main` es lo que se "
        "despliega solo, esa revisión es la puerta de entrada a producción.")
    d.nota("El CI usa las versiones de desarrollo (Python 3.14 y PostgreSQL 18); el servidor tiene Python 3.12.3 y "
           "PostgreSQL 16. Es una diferencia conocida entre la prueba y producción.",
           titulo="Diferencia entre CI y servidor")

    # ---- 4.8
    d.h2("4.8 Seguridad del despliegue")
    d.vinetas([
        "La **API no se publica** y escucha solo en `127.0.0.1`; el frontend es la única puerta.",
        "**Sin puertos de entrada:** el túnel es una conexión saliente.",
        "**HTTPS** en el borde de Cloudflare, con redirección de `http`, cookies de sesión y CSRF seguras.",
        "**`DEBUG` apagado** y `ALLOWED_HOSTS` restringido en los dos proyectos.",
        "**Claves y valores de producción fuera de los repositorios**, en módulos de settings del servidor.",
        "**Servicios sin privilegios**, con `UMask=0077` y reinicio automático.",
        "**Webhook con firma HMAC SHA-256**, solo `push` a `main` de los dos repositorios, sin entregas repetidas "
        "y con cola acotada; el receptor corre aislado con `systemd`.",
        "**Despliegue solo hacia adelante** con `git pull --ff-only`.",
        "**Sin datos en caché del navegador:** el frontend manda `never_cache` cuando hay una sesión abierta, "
        "para que el botón Atrás no muestre información.",
    ])


# ------------------------------------------------------------------ 5
def seccion_5(d):
    d.h1("5. Enlace de despliegue y acceso")
    d.p("AdMind está publicado y se puede abrir desde cualquier navegador:", keep_next=True)
    d.add(parrafo(run("Dirección: ", bold=True) + hipervinculo(URL_APP, URL_APP), alinear="center",
                  antes=120, despues=240, keep_next=True))
    datos = open(QR, "rb").read()
    ancho_px, alto_px = struct.unpack(">II", datos[16:24])
    cx = 1800000  # 5 cm
    cy = round(cx * alto_px / ancho_px)
    rid = d.registrar_imagen(datos)
    d.add(f"<w:p>{ppr(alinear='center', antes=0, despues=60, keep_next=True)}"
          f"{imagen(rid, cx, cy, 'QR de AdMind', 901, 'Código QR que abre AdMind')}</w:p>")
    d.add(parrafo("Escanee para abrir AdMind", estilo="Pie", alinear="center", despues=240))
    d.h2("Cuentas de demostración")
    d.p("Las cuentas no tienen segundo factor, así que se puede entrar directamente con el correo y la "
        "contraseña.", keep_next=True)
    d.tabla(
        ["Correo", "Contraseña", "Rol"],
        [
            ["`vigilante@gmail.com`", "`<contraseña>`", "Vigilancia"],
            ["`prueba@gmail.com`", "`<contraseña>`", ROL_PRUEBA],
        ],
        [3800, 2800, 2760], tam=20, junta=True,
    )


# ------------------------------------------------------------------ 6
def seccion_6(d):
    d.h1("6. Fuente del proyecto")
    d.p("El código está en dos repositorios públicos de GitHub, uno por proyecto.", keep_next=True)
    d.p(run("Backend", bold=True, color=V900), keep_next=True)
    d.p(enlace("", URL_BACK), keep_next=True)
    d.p("API REST con Django 5.2, Django REST Framework 3.18 y PostgreSQL. Está organizada en apps de dominio "
        "(cuentas, permisos, conjuntos, reservas, casos, pagos, reportes y más), con el flujo controlador, "
        "servicio y repositorio. Rama `main` en el commit `2dd5c44`.")
    d.p(run("Frontend", bold=True, color=V900), keep_next=True)
    d.p(enlace("", URL_FRONT), keep_next=True)
    d.p("Interfaz web con plantillas de Django y Alpine.js, y el sistema de diseño de AdMind. No toca la base de "
        "datos: habla con la API desde el servidor. Rama `main` en el commit `10e2d04`.")
    d.p(run("Calidad y seguimiento", bold=True, color=V900), keep_next=True)
    d.p(enlace("Aplicación desplegada: ", URL_APP), despues=60)
    d.p(enlace("SonarCloud, backend: ", URL_SONAR_B), despues=60)
    d.p(enlace("SonarCloud, frontend: ", URL_SONAR_F), despues=60)
    d.p(enlace("Tablero Scrum en Notion: ", URL_NOTION), despues=60)
    d.p("Integración continua: pestaña *Actions* de cada repositorio.")


def main():
    salida = sys.argv[1]
    with open(LOGO, "rb") as f:
        logo = f.read()
    d = Doc(
        titulo=TITULO,
        autor="Equipo AdMind",
        nombre_encabezado="Despliegue de Aplicaciones Empresariales · Entrega Final",
        logo_png=logo,
    )
    portada(d)
    seccion_1(d)
    seccion_2(d)
    seccion_3(d)
    seccion_4(d)
    seccion_5(d)
    seccion_6(d)
    d.guardar(salida, ultima_portada=True)
    print("guardado:", salida)


if __name__ == "__main__":
    main()
