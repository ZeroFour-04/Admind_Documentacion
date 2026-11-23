# -*- coding: utf-8 -*-
"""Parte 3: capítulos 4 (Seguridad), 5 (La API) y 6 (Tecnologías)."""
import re

ENDPOINTS_MD = ("C:/Users/Alejandro/Documents/A D M I N D/Documentacion/Admind_Documentacion/"
                "10_Sustentacion/datos/endpoints_api.md")

# Prefijo de cada módulo en la API y qué ofrece (para la tabla del capítulo 5)
MODULOS_API = {
    "anuncios": ("/anuncios/", "Tablón de anuncios del conjunto o de una vivienda, con fotos"),
    "areas": ("/areas/", "Áreas comunes del conjunto"),
    "casos": ("/casos/", "Casos del residente y su gestión"),
    "citas": ("/citas/", "Horario de atención y agenda de citas"),
    "conjuntos": ("/conjuntos/", "Creación, activación e identidad visual del conjunto"),
    "cuentas": ("/auth/", "Ingreso, sesión, conjunto activo, segundo factor, recuperación y usuarios"),
    "documentos": ("/documentos/", "Reglamento y manual con versiones y descarga auditada"),
    "infracciones": ("/infracciones/", "Registro, cierre y anulación de infracciones"),
    "ingresos": ("/ingresos/", "Ingreso a zonas con aforo y su salida"),
    "notificaciones": ("/notificaciones/", "Bandeja de avisos de cada persona"),
    "pagos": ("/pagos/administracion/", "Pagos de administración, comprobantes y confirmación"),
    "parqueaderos": ("/parqueaderos/", "Puestos y asignación a viviendas"),
    "personas": ("/personas/", "Búsqueda por documento y vinculación de personas"),
    "reglas": ("/reglas/", "Reglas de reserva alfa y beta"),
    "reservas": ("/reservas/", "Franjas, bloqueo, solicitudes, decisión y pago declarado"),
    "unidades": ("/unidades/", "Viviendas, agrupaciones y vínculos"),
    "visitantes": ("/visitantes/", "Visitantes, vehículos y salida"),
}


def contar_rutas():
    """Rutas por módulo, leídas de endpoints_api.md (generado de las rutas reales)."""
    conteo, actual = {}, None
    for linea in open(ENDPOINTS_MD, encoding="utf-8"):
        m = re.match(r"^## (\w+)\s*$", linea)
        if m:
            actual = m.group(1)
            conteo[actual] = 0
        elif actual and linea.startswith("| `/"):
            conteo[actual] += 1
    return conteo


def capitulo_4(d):
    d.h1("4. Seguridad")

    # ---- 4.1
    d.h2("4.1 Autenticación")
    d.numerada([
        "`POST /auth/login/` recibe el correo y la contraseña. La API crea una sesión (`TokenDeSesion`) y "
        "devuelve un token aleatorio. **En la base solo se guarda la huella SHA-256 del token**, de modo que la "
        "base no contiene ningún token utilizable.",
        "La sesión dura **1 hora** y guarda el usuario, el **conjunto activo** y si el segundo factor ya se "
        "verificó.",
        "Si la persona pertenece a un solo conjunto, se elige solo; si pertenece a varios, pasa por el selector "
        "(`POST /auth/conjunto-activo/`).",
        "En cada petición, `AutenticacionPorToken` lee `Authorization: Token <token>`, busca la sesión vigente por "
        "su huella y devuelve `(usuario, sesión)`. La sesión es `request.auth`, y de ahí sale el conjunto activo.",
    ])
    d.codigo([
        "class AutenticacionPorToken(BaseAuthentication):",
        "    palabra = b\"token\"",
        "",
        "    def authenticate(self, request):",
        "        ...",
        "        sesion = servicios.sesion_vigente(token)   # busca por la huella",
        "        if sesion is None:",
        "            raise AuthenticationFailed(\"Token inválido o vencido.\")",
        "        return sesion.usuario, sesion",
    ])
    d.p("**Revocación.** Cerrar sesión (`POST /auth/logout/`) elimina la sesión, y cambiar la contraseña elimina "
        "todas las sesiones abiertas de esa cuenta. Además, si a la persona le retiran el rol o desactivan el "
        "conjunto, la sesión pierde el conjunto activo de inmediato.")
    d.p("**Por qué un token opaco y no un JWT.** Un token opaco se revoca al instante (cerrar sesión borra la "
        "sesión) y guarda estado: el conjunto activo y el segundo factor. Un JWT es válido hasta que vence y no se "
        "puede revocar sin una lista negra.")
    d.implementacion(
        "JWT. Hoy el token es opaco. Está previsto que el ingreso entregue un JWT firmado (HS256) con "
        "vencimiento, conservando la tabla de sesiones para poder revocarlo al cerrar sesión o cambiar la "
        "contraseña. La firma y el vencimiento se validarían antes de consultar la sesión.")

    # ---- 4.2
    d.h2("4.2 Segundo factor")
    d.p("El segundo factor es un código TOTP de 6 dígitos, como el de Google Authenticator, que se configura "
        "escaneando un código QR. Se implementa con `django-otp` y también genera **códigos de respaldo**.")
    d.vinetas([
        "**Quién lo exige:** los roles que tienen permisos sensibles: **Superusuario, Administración y "
        "Secretaría**. Vigilancia y Residente no lo exigen (verificado en `PERMISOS_SENSIBLES` de "
        "`apps/permisos/catalogo.py`).",
        "**Cómo se hace cumplir:** `DosFactoresAlDia` está en los permisos por defecto de DRF. Con algún permiso "
        "sensible, la persona no puede hacer nada (403) hasta verificar el código. Las vistas necesarias para "
        "configurarlo y verificarlo se marcan con `permitida_sin_segundo_factor = True`.",
        "**Si pierde el teléfono:** la API envía al correo un enlace firmado que incluye el id del dispositivo "
        "TOTP. Al confirmarlo se borra el dispositivo y el enlace deja de valer, sin necesidad de una tabla "
        "nueva. El costo aceptado es que el segundo factor protege tanto como el buzón de correo. Se limita a 3 "
        "enlaces por hora.",
    ])

    # ---- 4.3
    d.h2("4.3 Contraseñas")
    d.vinetas([
        "**Almacenamiento:** hash **PBKDF2-SHA256**, el de Django por defecto, con sal y muchas iteraciones. Nunca "
        "se guarda en texto plano. Solo la configuración de pruebas (`config/settings_pruebas.py`) usa un cifrado "
        "más rápido, para que la suite corra en menos tiempo.",
        "**Validación:** se aplican los cuatro validadores de Django: similitud con los datos del usuario, "
        "longitud mínima, contraseñas comunes y contraseñas solo numéricas.",
        "**Recuperación:** un enlace de un solo uso enviado por correo, que **vence en 1 hora**, con un máximo de "
        "**3 enlaces por hora** por correo. Es de un solo uso porque el token depende de la contraseña: al "
        "cambiarla deja de servir. La API responde lo mismo exista o no la cuenta, para no revelar qué correos "
        "están registrados.",
    ])

    # ---- 4.4
    d.h2("4.4 Autorización")
    d.p("Hay un **catálogo fijo de 5 roles**, definido en código (`apps/permisos/catalogo.py`). El administrador "
        "solo asigna roles; si un conjunto necesita otro cargo, el equipo lo ajusta en el código.", keep_next=True)
    d.tabla(
        ["Rol", "Alcance", "Qué hace"],
        [
            ["Superusuario", "Plataforma (sin conjunto)", "Crea conjuntos, anula registros y opera el sistema"],
            ["Administración", "Conjunto", "Reglas, áreas, personas y aprobación de reservas"],
            ["Secretaría", "Conjunto", "Triage, prioridad, rechazo formal y anuncios. **No aprueba**"],
            ["Vigilancia", "Conjunto", "Visitantes e ingresos a zonas"],
            ["Residente", "Conjunto", "Reserva, abre casos, ve anuncios y documentos"],
        ],
        [2000, 2600, 4760], junta=True,
    )
    d.vinetas([
        "**exigir_permiso en la primera línea de cada vista:** `exigir_permiso(request, \"reserva.aprobar\")` "
        "responde 403 si la persona no tiene el permiso.",
        "**El frontend solo decide qué se muestra.** Oculta botones y secciones según los permisos de la sesión, "
        "pero quien decide de verdad es la API, en cada petición.",
        "**Lo de otro conjunto responde 404**, nunca 403, para no confirmar que el recurso existe.",
        "**Un solo rol vigente** por persona y conjunto: se cambia, no se suma. Cambiarlo cierra el actual y abre "
        "el nuevo en la misma transacción. Un conjunto nunca se queda sin Administración (`UltimaAdministracion`).",
        "**La prueba del intruso** (`tests/aislamiento/test_intruso.py`) recorre todas las rutas de la API actuando "
        "desde otro conjunto.",
    ])

    # ---- 4.5
    d.h2("4.5 Sesión del frontend")
    d.p("El token **nunca llega al JavaScript del navegador**. El frontend lo guarda en la sesión del servidor "
        "(`SESSION_ENGINE` en archivos) y al navegador solo le entrega una cookie `HttpOnly` con el identificador "
        "de esa sesión, que JavaScript no puede leer. La sesión del frontend vence a la misma hora que el token.")
    d.p("`SesionRequeridaMiddleware` (`apps/cuentas/sesion.py`) exige sesión en toda pantalla salvo las marcadas "
        "con `@publica` (ingreso, recuperar contraseña y el enlace del correo que quita el segundo factor). Con el "
        "segundo factor pendiente, solo deja abrir las pantallas para completarlo. Los formularios llevan "
        "protección CSRF de Django.")

    # ---- 4.6
    d.h2("4.6 Secretos")
    d.p("Las claves y contraseñas van en un archivo `.env` que está en `.gitignore`, así que nunca se sube al "
        "repositorio. El backend trae una plantilla, `.env _ejemplo`, con los nombres de las variables; el "
        "frontend no trae plantilla. Las variables de los dos proyectos están en la sección 7.3. El código las "
        "lee con `python-dotenv` y `os.environ`, y no hay ningún valor secreto escrito en los `settings.py`.")

    # ---- 4.7
    d.h2("4.7 Códigos HTTP")
    d.tabla(
        ["Código", "Cuándo"],
        [
            ["200 / 201", "Lectura correcta / se creó algo"],
            ["400", "El JSON no tiene la forma correcta, o la petición trae `conjunto`"],
            ["401", "Sin token, o token vencido"],
            ["403", "Sin permiso, sin conjunto activo, o falta el segundo factor"],
            ["404", "No existe **o es de otro conjunto** (nunca 403)"],
            ["409", "El estado no permite la operación (por ejemplo, la franja ya está tomada)"],
            ["429", "Demasiados intentos (recuperar contraseña, búsquedas)"],
        ],
        [1600, 7760], centro=(0,), junta=True,
    )

    # ---- 4.8
    d.h2("4.8 CORS")
    d.p("El navegador no llama a la API directamente: las pantallas las arma el servidor del frontend, que habla "
        "con la API de servidor a servidor, y CORS no aplica en esa conexión. CORS es una política del "
        "navegador: una lista blanca de orígenes impide que el JavaScript de otro sitio llame a la API desde el "
        "navegador de una víctima.")
    d.implementacion(
        "CORS con lista blanca. Hoy la API no configura CORS. Está previsto instalar `django-cors-headers` y "
        "permitir **solo** el origen del frontend, tomado de una variable de entorno (`http://127.0.0.1:8001` en "
        "local), sin credenciales, con una prueba de que un origen distinto no recibe la cabecera "
        "`Access-Control-Allow-Origin`.")


def capitulo_5(d):
    d.h1("5. La API")
    d.p("La API sigue un estilo REST con intercambio en JSON. Toda ruta exige la cabecera "
        "`Authorization: Token <token>`, salvo las de ingreso, recuperación de contraseña y restablecimiento del "
        "segundo factor. Hoy son **97 rutas**, agrupadas en 17 módulos:", keep_next=True)
    conteo = contar_rutas()
    filas = []
    total = 0
    for modulo, (prefijo, texto) in MODULOS_API.items():
        n = conteo.get(modulo, 0)
        total += n
        filas.append([f"`{modulo}`", f"`{prefijo}`", str(n), texto])
    filas.append(["**Total**", "", f"**{total}**", ""])
    d.tabla(["Módulo", "Prefijo", "Rutas", "Qué ofrece"], filas, [1800, 2500, 800, 4260], centro=(2,))
    assert total == 97, total

    d.h2("5.1 Convenciones")
    d.vinetas([
        "**El conjunto no viaja en la petición.** Sale de la sesión; si llega `conjunto` o `conjunto_id` en la URL, "
        "la consulta o el cuerpo, la API responde 400. La única ruta que recibe un conjunto es la que sirve para "
        "elegirlo: `POST /auth/conjunto-activo/`.",
        "**Identificadores UUID** en las rutas (`<uuid:solicitud_id>`).",
        "**Errores:** un objeto con `detail` y el mensaje en español, o un objeto con una lista de errores por campo.",
        "**Archivos** (fotos, logos, comprobantes y documentos) se entregan solo por la ruta propia de cada uno. "
        "Los comprobantes y las fotos responden 404 a quien no puede verlos.",
    ])

    d.h2("5.2 Ejemplo: iniciar sesión")
    d.p("Petición (`IniciarSesionSerializer`: `correo` y `contrasena`):", keep_next=True)
    d.codigo([
        "POST /auth/login/",
        "Content-Type: application/json",
        "",
        "{ \"correo\": \"residente@example.com\", \"contrasena\": \"<contraseña>\" }",
    ])
    d.p("Respuesta `200` (abreviada; los permisos son los del rol Residente):", keep_next=True)
    d.codigo([
        "{",
        "  \"token\": \"<token aleatorio>\",",
        "  \"vence_en\": \"2026-11-14T15:30:00-05:00\",",
        "  \"conjunto_activo\": {",
        "    \"id\": \"<uuid>\", \"nombre\": \"Conjunto de prueba\",",
        "    \"acento\": \"<acento>\", \"color\": null, \"logo\": null",
        "  },",
        "  \"permisos\": [\"area.ver\", \"caso.crear\", \"cita.agendar_propia\", \"documento.ver\",",
        "               \"pago.reportar\", \"reserva.solicitar\"],",
        "  \"puede_crear_conjunto\": false,",
        "  \"roles\": [\"Residente\"],",
        "  \"tipo_usuario\": \"Residente\",",
        "  \"dos_factores\": { \"requerido\": false, \"configurado\": false, \"verificado\": false }",
        "}",
    ])
    d.p("Con credenciales incorrectas responde `401` con `{\"detail\": \"Correo o contraseña incorrectos.\"}` y "
        "la cabecera `WWW-Authenticate: Token`.")

    d.h2("5.3 Ejemplo: lista de anuncios")
    d.p("Petición y respuesta (`AnuncioSerializer`). El conjunto sale del token:", keep_next=True)
    d.codigo([
        "GET /anuncios/",
        "Authorization: Token <token>",
    ])
    d.codigo([
        "[",
        "  {",
        "    \"id\": \"<uuid>\",",
        "    \"titulo\": \"Mantenimiento de ascensores\",",
        "    \"cuerpo\": \"El lunes se revisarán los ascensores de la torre 1.\",",
        "    \"fotos\": [\"<uuid de la foto>\"],",
        "    \"alcance\": \"conjunto\",",
        "    \"unidad\": null,",
        "    \"autor\": \"<nombre de quien lo publicó>\",",
        "    \"publicado_en\": \"2026-11-12T09:00:00-05:00\",",
        "    \"editado_en\": \"2026-11-12T09:00:00-05:00\",",
        "    \"puede_editar\": false",
        "  }",
        "]",
    ])
    d.p("`alcance` es `conjunto` o `vivienda`; con `vivienda`, `unidad` trae `{ \"id\": …, \"nombre\": … }`. "
        "`fotos` lista solo los ids: cada imagen se pide aparte, en `/anuncios/<id>/fotos/<foto>/`.")
    d.p("La tabla completa de rutas, con sus métodos y su vista, está en el **Anexo A**.")
    d.implementacion(
        "Documentación interactiva con Swagger. Hoy la API no la tiene. Está previsto publicarla en `/api/docs/` "
        "con `drf-spectacular`, con una etiqueta por módulo y el botón *Authorize* para enviar el token.")
    d.implementacion(
        "Reportes en PDF y Excel. Están previstos dos reportes con formato profesional (uso de zonas comunes y "
        "estado de pagos del mes), que se descargarían desde la API con un permiso nuevo. Todavía no existen.")


def capitulo_6(d):
    d.h1("6. Tecnologías")
    d.p("Versiones tomadas de los archivos `requirements.txt` de cada proyecto, que son las que mandan:",
        keep_next=True)
    d.tabla(
        ["Tecnología", "Versión", "Proyecto", "Para qué sirve"],
        [
            ["Python", "3.14", "Ambos", "Lenguaje de todo el proyecto (entorno virtual `.venv`)"],
            ["Django", "5.2.17 (LTS)", "Ambos", "Rutas, ORM, migraciones, plantillas y sesiones"],
            ["Django REST Framework", "3.18.1", "Backend", "`APIView`, serializers, autenticación y permisos"],
            ["PostgreSQL", "18 (nativo)", "Backend", "La base de datos; hace cumplir las restricciones"],
            ["psycopg", "3.3.5", "Backend", "Conector entre Django y PostgreSQL"],
            ["django-otp", "1.7.3", "Backend", "Segundo factor TOTP y códigos de respaldo"],
            ["qrcode", "8.2", "Backend", "Código QR para configurar el segundo factor"],
            ["requests", "2.34.2", "Frontend", "Llamadas del frontend a la API"],
            ["Alpine.js", "3.17.4", "Frontend", "Interactividad puntual dentro del HTML"],
            ["python-dotenv", "1.2.3", "Ambos", "Lee el archivo `.env`: los secretos quedan fuera del código"],
            ["pytest", "9.1.1", "Ambos", "Ejecutor de las pruebas"],
            ["pytest-django", "4.14.0", "Ambos", "Base de datos de prueba y utilidades de Django para pytest"],
        ],
        [2300, 1500, 1300, 4260], mono=(), junta=True,
    )

    d.h2("6.1 Por qué estas decisiones")
    d.vinetas([
        "**Django y no FastAPI.** Autenticación, hash de contraseñas, sesiones, permisos, migraciones y segundo "
        "factor vienen de fábrica. FastAPI es más rápido y asíncrono, pero la latencia de AdMind la decide la "
        "transacción en PostgreSQL, que es igual en los dos.",
        "**Django 5.2 y no 6.x.** Es una versión LTS, con soporte hasta abril de 2028, y tiene más material de "
        "consulta.",
        "**PostgreSQL desde el primer día y no SQLite.** SQLite no ofrece índices únicos parciales con la misma "
        "garantía, ni claves foráneas compuestas contra claves únicas compuestas, ni privilegios por tabla. Las "
        "cuatro piezas propias de la sección 3.5 dependen de ellos.",
        "**Plantillas de Django con Alpine.js y no React.** La aplicación es sobre todo formularios y tablas: el "
        "HTML se genera en el servidor y JavaScript solo se usa donde hay interacción real. No hay npm ni paso de "
        "compilación.",
        "**Sin Docker.** PostgreSQL 18 corre como un servicio del sistema operativo. Docker quedó como deseable, "
        "no como requisito.",
    ])


def construir(d):
    capitulo_4(d)
    capitulo_5(d)
    capitulo_6(d)
