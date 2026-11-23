# -*- coding: utf-8 -*-
"""Parte 2: capítulos 1 (Introducción), 2 (Requerimientos) y 3 (Arquitectura)."""
from ooxml import (
    BLANCO, G500, V50, V600, V700, V900, ANCHO_VERTICAL,
    bordes_tc, celda, fila, parrafo, run, tabla,
)


# ---------------------------------------------------------------- diagrama de 3.1

def diagrama_arquitectura(d):
    ancho = 6400

    def caja(titulo, detalle, fondo, texto, borde):
        pars = parrafo(run(titulo, bold=True, color=texto, size=25), alinear="center", antes=0, despues=30,
                       linea=(240, "auto"), keep_next=True)
        pars += parrafo(detalle, alinear="center", antes=0, despues=0, linea=(240, "auto"), keep_next=True) \
            if detalle.startswith("<w:") else \
            parrafo(run(detalle, color=texto, size=19), alinear="center", antes=0, despues=0, linea=(240, "auto"),
                    keep_next=True)
        return fila([celda(ancho, pars, fill=fondo, bordes=bordes_tc(color=borde, sz=8), valign="center",
                           margenes='<w:tcMar><w:top w:w="110" w:type="dxa"/><w:left w:w="140" w:type="dxa"/>'
                                    '<w:bottom w:w="110" w:type="dxa"/><w:right w:w="140" w:type="dxa"/></w:tcMar>')])

    def flecha(etiqueta):
        contenido = run("↓", bold=True, color=V600, size=30) + run("   " + etiqueta, italic=True, color=G500,
                                                                   size=19)
        return fila([celda(ancho, parrafo(contenido, alinear="center", antes=40, despues=40, linea=(240, "auto"),
                                          keep_next=True),
                           bordes=bordes_tc(nulos=("top", "left", "bottom", "right")), valign="center")])

    filas = [
        caja("Navegador", "Chrome, Edge o Firefox", V50, V900, V600),
        flecha("HTML y formularios (cookie de sesión HttpOnly)"),
        caja("Frontend · puerto 8001", "Django con plantillas y Alpine.js · cliente_api/ · DATABASES = {}",
             V600, BLANCO, V600),
        flecha("JSON con el token (Authorization: Token …)"),
        caja("API · puerto 8000", "Django REST Framework: vistas, serializers, servicios y modelos",
             V700, BLANCO, V700),
        flecha("SQL (psycopg)"),
        caja("PostgreSQL 18", "Base admind_db: restricciones e índices únicos parciales", V900, BLANCO, V900),
    ]
    d.add(tabla(filas, [ancho], bordes_tabla=False, jc="center"))
    d.pie("Figura 1. Los cuatro componentes de AdMind y lo que viaja en cada conexión. "
          "Solo la API se conecta a la base de datos.")


# ---------------------------------------------------------------- capítulos

def capitulo_1(d):
    d.h1("1. Introducción")
    d.h2("1.1 Propósito del manual")
    d.p("Este manual describe cómo está construido AdMind: sus requerimientos, su arquitectura, las medidas de "
        "seguridad, la API, las tecnologías, la instalación, las pruebas y el proceso de desarrollo. Explica además "
        "las decisiones de diseño, para que quien lo lea pueda entender el sistema, ponerlo a correr y continuar "
        "su desarrollo.")
    d.h2("1.2 A quién va dirigido")
    d.p("A un desarrollador que va a instalar, mantener o evaluar AdMind. Se asume conocimiento básico de Python, "
        "HTTP y bases de datos relacionales. El uso de las pantallas se explica en el Manual de Usuario, y el "
        "detalle de cada tabla, en el Diccionario de Datos.")
    d.h2("1.3 Alcance")
    d.p("El manual describe el sistema tal como está en el código el 14 de noviembre de 2026: backend `b89d9f2` y "
        "frontend `bdcb5c3`, rama `main` de los dos repositorios. Lo que todavía no existe aparece en recuadros "
        "ámbar con el título **«En implementación»** y se presenta como trabajo previsto, nunca como hecho.")
    d.h2("1.4 Qué es AdMind")
    d.p("AdMind es una aplicación web para administrar conjuntos residenciales en Colombia, regidos por la Ley 675 "
        "de 2001 de propiedad horizontal. Reemplaza los grupos de WhatsApp y las hojas de cálculo con las que hoy "
        "se administra la mayoría de los conjuntos: reservas de zonas comunes, casos y solicitudes, anuncios, "
        "visitantes, parqueaderos, pagos de administración e infracciones, cada uno con sus permisos por rol.")
    d.p("Una **sola base de datos** guarda a muchos conjuntos, y ese es el reto técnico central: que ningún "
        "conjunto vea ni toque los datos de otro. Alrededor de él AdMind tiene cuatro piezas propias, cada una "
        "vigilada por una prueba automática: el aislamiento multiconjunto, la concurrencia en las reservas, el "
        "motor de reglas configurable y la trazabilidad. Se explican en la sección 3.5.")


def capitulo_2(d):
    d.h1("2. Requerimientos")
    d.h2("2.1 Requerimientos funcionales")
    d.p("La tabla reúne las historias de usuario del backlog que tienen código, agrupadas por módulo. "
        "*Construida* significa que el código y sus pruebas automáticas existen; *Parcial*, que hay código que no "
        "cubre todos los criterios de la historia. El estado es el del código; la definición de terminado del "
        "equipo exige además una prueba manual de quien no programó la historia.")
    filas = [
        ("grupo", "Cuentas y acceso"),
        ["HU-01", "Inicio de sesión con correo y contraseña", "Construida"],
        ["HU-02", "Segundo factor (TOTP) para permisos sensibles", "Construida"],
        ["HU-26", "Selector de conjunto activo", "Construida"],
        ("grupo", "Conjuntos"),
        ["HU-03", "Asistente por pasos para crear un conjunto", "Construida"],
        ["HU-21", "Identidad visual del conjunto: color y logo", "Construida"],
        ["HU-33", "Repositorio de documentos vigentes", "Parcial"],
        ("grupo", "Personas, roles y aislamiento"),
        ["HU-04", "Persona global única por documento", "Construida"],
        ["HU-05", "Aislamiento de datos entre conjuntos", "Construida"],
        ["HU-06", "Asignación de roles del catálogo fijo", "Construida"],
        ["HU-07", "Vincular persona existente por búsqueda de documento", "Construida"],
        ("grupo", "Viviendas"),
        ["HU-08", "Vínculos de unidad y enrutamiento de notificaciones", "Construida"],
        ["HU-39", "Estructura de viviendas del conjunto: agrupaciones y generación en lote", "Parcial (primera parte)"],
        ("grupo", "Zonas comunes y motor de reglas"),
        ["HU-09", "Catálogo de áreas comunes del conjunto", "Construida"],
        ["HU-10", "Configuración de reglas beta de reserva", "Construida"],
        ("grupo", "Reservas"),
        ["HU-11", "Bloqueo exclusivo de 3 minutos sobre una franja", "Construida"],
        ["HU-12", "Confirmación de contenido antes de enviar", "Construida"],
        ["HU-13", "Envío de solicitud y motor de reglas alfa y beta", "Construida"],
        ["HU-14", "Bandeja del administrador: aprobar o rechazar", "Construida"],
        ["HU-16", "Registro de pago declarado y comprobante", "Construida"],
        ["HU-18", "Aviso de disponibilidad de franja (campana)", "Parcial (solo la API)"],
        ("grupo", "Casos, anuncios y triage"),
        ["HU-22", "Bandeja de triage de la Secretaría", "Parcial"],
        ["HU-24", "Rechazo por causal formal de la Secretaría", "Parcial"],
        ["HU-25", "Anuncios con alcance de conjunto o vivienda", "Construida"],
        ["HU-29", "Tablero de casos con respuesta obligatoria", "Construida"],
        ("grupo", "Visitantes y parqueaderos"),
        ["HU-27", "Registro de visitantes y vehículos", "Parcial"],
        ["HU-28", "Parqueadero de visitantes atado a la visita", "Construida"],
        ["HU-34", "Asignación de parqueaderos de residentes", "Construida"],
        ("grupo", "Infracciones, pagos y citas"),
        ["HU-30", "Registro y comunicación de infracciones", "Construida"],
        ["HU-35", "Reporte de pago de administración", "Construida"],
        ["HU-31", "Agendar cita dentro del horario de atención", "Parcial (solo la API)"],
    ]
    d.tabla(["Código", "Historia", "Estado"], filas, [1000, 6000, 2360], cebra=False, centro=(0,))
    d.p("En total hay **23 historias construidas y 7 parciales**. Las historias restantes del backlog quedan fuera "
        "de esta entrega: son 9 de las 38 (más la HU-40, que solo está definida en el tablero). Además, el ingreso "
        "a zonas con aforo está construido y no tiene número de historia en el backlog.")

    d.h2("2.2 Requerimientos no funcionales")
    d.tabla(
        ["Requisito", "Qué se exige", "Dónde se cumple"],
        [
            ["**Seguridad**",
             "Contraseñas con PBKDF2-SHA256 de Django (con sal, nunca en texto plano), segundo factor para los "
             "roles con permisos sensibles y sesión de una hora con token revocable.",
             "`apps/cuentas/` y `apps/permisos/` (capítulo 4)"],
            ["**Aislamiento entre conjuntos**",
             "Ningún conjunto ve ni toca datos de otro. Protege los datos personales que cubre la Ley 1581 de 2012.",
             "`apps/comun/aislamiento/`, claves foráneas compuestas en PostgreSQL y la prueba del intruso (3.5.1)"],
            ["**Concurrencia**",
             "Una sola reserva por franja aunque 50 personas pulsen a la vez.",
             "`apps/comun/bloqueo/` e índice único parcial en PostgreSQL (3.5.2)"],
            ["**Trazabilidad**",
             "Auditoría de solo inserción y sin borrado físico: lo equivocado se anula, no se borra.",
             "`apps/auditoria/` y la vigencia o anulación de cada fila (3.5.4)"],
            ["**Cumplimiento legal**",
             "Ley 675 de 2001 y Ley 1581 de 2012. El sistema registra y no decide: no impone sanciones ni "
             "restringe el uso de bienes comunes. Lo que la ley prohíbe no se programa como un permiso denegado, "
             "sino como una operación que no existe.",
             "Diseño de los módulos de infracciones, pagos y parqueaderos"],
            ["**Usabilidad y accesibilidad**",
             "Sistema de diseño propio, con contraste de color verificado y un acento de color por conjunto.",
             "`design-system/` y `static/css/` del frontend"],
            ["**Mantenibilidad**",
             "Arquitectura por capas con llamadas que solo bajan, y pruebas automáticas.",
             "Sección 3.2 y capítulo 8"],
        ],
        [2000, 4560, 2800],
    )

    d.h2("2.3 Requisitos para instalar")
    d.vinetas([
        "**Sistema operativo:** Windows, Linux o macOS.",
        "**Python 3.14** y **PostgreSQL 18**, además de **Git**.",
        "**Navegador:** una versión actual de Chrome, Edge o Firefox.",
        "**Memoria:** 4 GB de RAM son suficientes para los dos servidores y la base de datos.",
    ])


def capitulo_3(d):
    d.h1("3. Arquitectura")

    # ---- 3.1
    d.h2("3.1 Vista general")
    d.p("AdMind son **dos proyectos Django independientes**. La **API** (puerto 8000) es el único que toca la base "
        "de datos: habla JSON, autentica cada petición y aplica todas las reglas del negocio. El **frontend** "
        "(puerto 8001) arma las pantallas con plantillas de Django y Alpine.js; tiene `DATABASES = {}`, es decir, "
        "no puede conectarse a la base, y cada pantalla le pide sus datos a la API.")
    diagrama_arquitectura(d)
    d.h3("Por qué dos servidores")
    d.vinetas([
        "**El contrato es la API.** Otra interfaz, como una aplicación móvil, podría usarla sin tocar el backend.",
        "**El frontend no puede saltarse las reglas**, porque no tiene base de datos con la que hacerlo.",
        "**El costo:** cada pantalla se traduce en llamadas HTTP. De eso se encarga `cliente_api/`, el único lugar "
        "del frontend que habla con la API.",
    ])

    # ---- 3.2
    d.h2("3.2 Capas")
    d.p("El curso exige el flujo **controlador → servicio → repositorio**, el de la plantilla de ASP.NET. Esta es "
        "su equivalencia en AdMind:", keep_next=True)
    d.tabla(
        ["ASP.NET", "AdMind", "Qué hace"],
        [
            ["Controllers", "`urls.py` + `views.py`", "Exige el permiso, valida, llama al servicio y traduce el "
                                                       "resultado a HTTP"],
            ["Dtos", "`serializers.py`", "Define la forma de la entrada y de la salida"],
            ["Services", "`servicios.py`", "Reglas de negocio. No sabe nada de HTTP"],
            ["Repositories", "`models.py` + `ManagerDeConjunto`", "Buscar y guardar, ya filtrado por conjunto"],
            ["Utilities", "`apps/comun/`", "Aislamiento, bloqueo y manejo de archivos"],
        ],
        [1700, 3100, 4560], mono=(0, 1), junta=True,
    )
    d.p("**Las llamadas solo bajan:** la vista llama al servicio y el servicio, al repositorio. Hay dos señales de "
        "error: `Area.objects` dentro de una vista (se salta dos capas) y `request` o `Response` dentro de un "
        "servicio (ya sabe de HTTP).")
    d.p("**Patrón de errores.** El servicio dice *qué* pasó lanzando una excepción de negocio (`FranjaOcupada`, "
        "`BloqueoVencido`); la vista decide *cómo* se dice en HTTP (un `409`). Así el servicio no depende de HTTP.")

    # ---- 3.3
    d.h2("3.3 Estructura del código")
    d.h3("Backend: `Backend/Admind_Backend`")
    d.p("Carpetas principales: `config/` (ajustes y rutas), `apps/` (un módulo por tema del negocio), `tests/` "
        "(pruebas transversales de aislamiento, concurrencia, esquema y archivos) y `bd/` (notas sobre la base de "
        "datos). Cada app de `apps/` tiene su `README.md`.")
    d.tabla(
        ["App", "Qué guarda o hace"],
        [
            ["`comun`", "Piezas compartidas: aislamiento multiconjunto, modelo base de las tablas de conjunto, "
                        "bloqueo y concurrencia, y validación de archivos"],
            ["`personas`", "Persona global, única por tipo y número de documento"],
            ["`cuentas`", "Usuario (entra con correo), sesiones con token, segundo factor, recuperación de "
                          "contraseña y usuarios del conjunto"],
            ["`permisos`", "Catálogo fijo de 5 roles, asignaciones (un rol vigente por persona y conjunto) y "
                           "permisos efectivos"],
            ["`conjuntos`", "Conjunto, asistente de creación e identidad visual (color y foto 1:1)"],
            ["`unidades`", "Agrupaciones, viviendas y vínculos de las personas con ellas, con histórico; "
                           "generador de viviendas en lote"],
            ["`documentos`", "Reglamento y manual del conjunto, con versiones (el PDF se guarda en la base)"],
            ["`areas`", "Áreas comunes: modo de uso (con reserva o con ingreso), horario y aforo"],
            ["`reglas`", "Reglas por niveles (sistema, alfa y beta), versionadas, y su evaluador"],
            ["`reservas`", "Solicitudes de reserva: franjas, bloqueo de 3 minutos, envío y evaluación, decisión y "
                           "pago declarado con comprobante"],
            ["`ingresos`", "Ingreso a zonas con aforo simultáneo"],
            ["`casos`", "Casos del residente y su gestión: prioridad, redirección, respuesta y rechazo"],
            ["`anuncios`", "Anuncios del conjunto o de una vivienda, con hasta 4 fotos"],
            ["`notificaciones`", "Bandeja de avisos en la aplicación y por correo"],
            ["`visitantes`", "Registro de visitantes y vehículos, su salida y la ocupación del parqueadero de "
                             "visitantes"],
            ["`parqueaderos`", "Puestos de residentes y de visitantes, y su asignación a viviendas"],
            ["`pagos`", "Reporte de pago de administración por vivienda y mes, comprobante y mora"],
            ["`infracciones`", "Registro de infracciones, su comunicación obligatoria, cierre y anulación. Sin "
                               "sanciones ni multas"],
            ["`citas`", "Horario de atención y agenda de citas (solo API, sin pantalla)"],
            ["`auditoria`", "Registro de solo inserción de las acciones del sistema"],
            ["`triage`, `importacion_respaldo`", "Carpetas reservadas para historias futuras: solo tienen README"],
        ],
        [2300, 7060], mono=(),
    )
    d.h3("Frontend: `Frontend/Admind_Front-End`")
    d.p("Carpetas principales: `config/` (ajustes sin base de datos y rutas), `cliente_api/` (una función por "
        "endpoint de la API, con un archivo por app del backend), `apps/` (una app por sección de la interfaz, con "
        "vistas, formularios y plantillas), `templates/` (`base/` es el esqueleto de toda página y "
        "`componentes/` las piezas reutilizables), `static/` (CSS propio y JavaScript, con Alpine.js en "
        "`static/js/vendor/`), `design-system/` (tokens de color y tipografía, y componentes CSS) y `tests/`.")
    d.tabla(
        ["App", "Sección de la interfaz"],
        [
            ["`cuentas`", "Ingreso, recuperación de contraseña, segundo factor, perfil y la sesión del frontend"],
            ["`conjuntos`", "Selector de conjunto, asistente de creación y color y foto del conjunto"],
            ["`paneles`", "Pantalla de Inicio (hoy es una maqueta con datos de ejemplo)"],
            ["`reservas`", "Zonas comunes: calendario, franjas y solicitud de reserva con su pago"],
            ["`areas`, `reglas`", "Áreas comunes y tablero de reglas de reserva"],
            ["`triage`, `casos`", "Dashboard de gestión «Solicitudes» y casos del residente"],
            ["`anuncios`, `notificaciones`", "Tablón de anuncios y bandeja de avisos"],
            ["`ingresos`, `visitantes`, `parqueaderos`", "Ingreso a zonas, portería con parqueadero y asignación de "
                                                         "puestos"],
            ["`pagos`, `infracciones`, `documentos`", "Pagos de administración, infracciones y documentos del "
                                                      "conjunto"],
            ["`unidades`, `usuarios`", "Viviendas y vínculos, y usuarios del conjunto por rol"],
        ],
        [3300, 6060],
    )

    # ---- 3.4
    d.h2("3.4 Recorrido de una petición")
    d.p("Ejemplo: un residente envía una solicitud de reserva que ya tiene su franja bloqueada. Las rutas y nombres "
        "son los del código.", keep_next=True)
    d.tabla(
        ["Paso", "Dónde", "Qué ocurre"],
        [
            ["1", "Navegador", "El residente completa el formulario y pulsa «Enviar solicitud». El navegador manda "
                               "un `POST` al frontend, a `/reservas/solicitudes/<id>/enviar/`."],
            ["2", "Vista del frontend\n`apps/reservas/views.py`",
             "La función `enviar` valida el formulario con `SolicitudForm` y llama a "
             "`cliente_api.reservas.enviar`."],
            ["3", "`cliente_api/http.py`",
             "`pedir` saca el token de la sesión del servidor, agrega `Authorization: Token …` y hace el `POST` a la "
             "API con `requests`, esperando como máximo 10 segundos."],
            ["4", "Vista de la API\n`EnviarSolicitudView`",
             "`AutenticacionPorToken` valida el token y `DosFactoresAlDia` revisa el segundo factor. "
             "`VistaDeConjunto` fija el conjunto activo de la sesión (y rechaza con 400 si la petición trae "
             "`conjunto`). Después, `exigir_permiso(request, \"reserva.solicitar\")` responde 403 si falta el "
             "permiso y el serializer valida el cuerpo."],
            ["5", "Servicio\n`servicios.enviar`",
             "Expira los bloqueos vencidos, abre una transacción y bloquea con `select_for_update` la fila de la "
             "solicitud y la de su área. Comprueba que la solicitud es de esa persona y que el bloqueo no venció, "
             "y evalúa todas las reglas: si cumple, la solicitud pasa a `APARTADA`; si no, se libera con todos los "
             "motivos."],
            ["6", "Repositorio\n`Solicitud.objects`",
             "El `ManagerDeConjunto` agrega `conjunto_id = <conjunto activo>` a toda consulta. Sin conjunto activo "
             "falla con `SinConjuntoActivo`."],
            ["7", "PostgreSQL",
             "Guarda el cambio en `reservas_solicitud`. El índice único parcial `solicitud_franja_bloqueante_unica` "
             "y las claves foráneas compuestas impiden que haya doble reserva o referencias a otro conjunto."],
            ["8", "Respuesta",
             "La API responde `200` con la solicitud apartada; `400` con la lista de `motivos` si incumple reglas "
             "(la franja queda libre); `409` si el bloqueo venció o la solicitud ya no está en trámite; `404` si no "
             "es suya. El frontend redirige a la pantalla de la solicitud con el resultado, o muestra el mensaje en "
             "español sin perder lo escrito."],
        ],
        [700, 2500, 6160], centro=(0,),
    )

    # ---- 3.5
    d.h2("3.5 Piezas propias del diseño")
    d.p("Estas cuatro piezas son lo que distingue a AdMind de un CRUD. Cada una tiene una prueba automática que la "
        "vigila:", keep_next=True)
    d.tabla(
        ["Pieza", "Problema que resuelve", "Dónde vive", "Prueba que la vigila"],
        [
            ["Aislamiento multiconjunto", "Que A nunca vea ni toque datos de B", "`apps/comun/aislamiento/`",
             "`tests/aislamiento/test_intruso.py`"],
            ["Concurrencia", "Que 50 clics simultáneos den una sola reserva",
             "`apps/comun/bloqueo/` e índices únicos parciales", "`tests/concurrencia/`"],
            ["Motor de reglas", "Que cada conjunto configure sus reglas", "`apps/reglas/`",
             "`apps/reglas/tests.py`"],
            ["Trazabilidad", "Que nada se borre y todo quede registrado", "`apps/auditoria/`",
             "`apps/auditoria/tests.py`"],
        ],
        [1900, 2700, 2500, 2260], mono=(), junta=True,
    )

    # 3.5.1
    d.h3("3.5.1 Aislamiento multiconjunto")
    d.p("**El problema.** Las reservas de dos conjuntos están en la misma tabla, separadas solo por una columna "
        "(`conjunto_id`). Si una consulta olvida filtrar, nada se rompe: simplemente se filtran datos de un "
        "conjunto a otro, lo que sería un tratamiento no autorizado de datos personales bajo la Ley 1581.")
    d.p("**La solución: tres líneas de defensa independientes.**", keep_next=True)
    d.tabla(
        ["Línea", "Dónde", "Qué hace"],
        [
            ["1. `VistaDeConjunto`", "`apps/comun/aislamiento/vistas.py`",
             "Clase base de toda vista con datos de un conjunto. Después de autenticar: responde 400 si llega "
             "`conjunto` o `conjunto_id` en la URL, la consulta o el cuerpo; 403 si la sesión no tiene conjunto "
             "activo; y fija el conjunto del token en una ContextVar que se suelta al terminar la petición, "
             "aunque haya un error."],
            ["2. `ManagerDeConjunto`", "`apps/comun/aislamiento/managers.py`",
             "Reemplaza `Modelo.objects` y agrega `filter(conjunto_id=<conjunto activo>)` a toda consulta. Sin "
             "conjunto activo lanza `SinConjuntoActivo`: falla a propósito en lugar de devolver todo."],
            ["3. Clave foránea compuesta", "`apps/comun/aislamiento/migraciones.py`",
             "`fk_compuesta()` crea `FOREIGN KEY (area_id, conjunto_id) REFERENCES areas_area (id, conjunto_id)`. "
             "La base de datos rechaza físicamente una fila que apunte a otro conjunto."],
        ],
        [2100, 2700, 4560], junta=True,
    )
    d.p("`ModeloDeConjunto` (`apps/comun/modelos_base/modelos.py`) es la base de toda tabla de un conjunto: id "
        "UUID, el campo `conjunto` con `on_delete=PROTECT`, la restricción única `(id, conjunto)` que hace posible "
        "la clave compuesta, el Manager filtrado y un `save()` que lanza `EscrituraEnOtroConjunto` si la fila es "
        "de otro conjunto.")
    d.vinetas([
        "**ContextVar:** una variable «por petición». Aunque dos peticiones corran a la vez, cada una ve su propio "
        "valor.",
        "**Por qué no es un middleware de Django:** los middleware corren antes de que DRF autentique el token, "
        "así que todavía no se sabe quién es ni qué conjunto tiene.",
        "**Por qué 404 y no 403:** un 403 confirmaría que el recurso existe. Por eso lo de otro conjunto responde "
        "«No encontrado», y los ids son UUID.",
        "**Row Level Security se descartó:** obliga a fijar una variable de sesión en cada conexión, y mantenerlo "
        "cuesta más que las claves compuestas.",
        "**Tablas globales:** una lista cerrada (`Persona`, `Usuario`, `Conjunto`, `TokenDeSesion`, los catálogos "
        "de permisos y `Asignacion`, cuyo conjunto es nulo para el Superusuario). La prueba "
        "`tests/esquema/test_tablas_globales.py` falla si aparece otra tabla sin `conjunto_id`.",
    ])
    d.p("**La prueba.** `tests/aislamiento/test_intruso.py` recorre todas las rutas de la API actuando desde otro "
        "conjunto, y `test_filtro_por_conjunto.py` comprueba el filtro del Manager.")
    d.p("**Límites conocidos.** `bulk_create()` y `update()` se saltan `save()`; el admin de Django y el shell "
        "necesitan `usar_conjunto()`; y las relaciones hacia adelante (`reserva.area`) no pasan por el Manager, "
        "aunque la clave compuesta garantiza que sean del mismo conjunto.")

    # 3.5.2
    d.h3("3.5.2 Concurrencia: el bloqueo de 3 minutos")
    d.p("**El problema.** Cincuenta residentes pulsan «Reservar» en la misma franja en el mismo milisegundo. Si el "
        "sistema primero pregunta «¿está libre?» y después inserta, dos peticiones pueden ver «libre» a la vez "
        "(*check-then-act*).")
    d.p("**La solución: no preguntar primero.** AdMind intenta el `INSERT` directamente y deja que la base decida, "
        "una sola vez (`apps/comun/bloqueo/bloqueo.py`):")
    d.codigo([
        "def tomar(crear):",
        "    try:",
        "        with transaction.atomic():",
        "            return crear()            # INSERT de la solicitud",
        "    except IntegrityError as error:",
        "        raise RecursoOcupado(nombre_de_la_restriccion(error)) from error",
    ])
    d.p("Lo que impide el duplicado es un **índice único parcial** declarado en el modelo de `reservas`:")
    d.codigo([
        "-- solicitud_franja_bloqueante_unica",
        "UNIQUE (conjunto_id, area_id, fecha, hora_inicio)",
        "  WHERE estado IN ('EN_SOLICITUD', 'APARTADA', 'RESERVADA')",
    ])
    d.vinetas([
        "**«Parcial»** significa que solo cuentan las filas bloqueantes. Una solicitud expirada o liberada sale "
        "del índice y la franja queda libre **sin borrar nada**. Los estados bloqueantes son `EN_SOLICITUD`, "
        "`APARTADA` y `RESERVADA`; no bloquean `EXPIRADA`, `LIBERADA`, `RECHAZADA` ni `CANCELADA`.",
        "Un segundo índice, `solicitud_un_bloqueo_por_persona`, impide que una persona tenga dos bloqueos a la vez "
        "en un conjunto. El nombre de la restricción que devuelve el conector permite saber cuál falló y "
        "responder distinto.",
        "**Expiración sin proceso en segundo plano:** `expirar_vencidos()` hace un solo `UPDATE` al comienzo de "
        "cada consulta o acción de reservas. Es idempotente: lo que ya no está activo no se toca.",
        "**Mecanismo compartido:** `apps/comun/bloqueo/` lo usan reservas, citas, ingresos y el parqueadero de "
        "visitantes.",
        "**El aforo es distinto:** es una suma de filas, no una fila única, así que ningún índice lo custodia. El "
        "servicio de ingresos toma la fila del área con `select_for_update` y cuenta dentro de la transacción.",
    ])
    d.p("**La prueba.** `tests/concurrencia/test_bloqueo_de_franjas.py` lanza varios hilos contra la misma franja "
        "en PostgreSQL real y verifica que queda un solo bloqueo. Otras dos pruebas hacen lo mismo con el aforo "
        "de los ingresos y con el parqueadero de visitantes.")

    # 3.5.3
    d.h3("3.5.3 Motor de reglas")
    d.p("**El problema.** Cada conjunto tiene su propio reglamento, y las reglas para reservar una zona común "
        "(horarios, anticipación, aforo, límites por vivienda) cambian de un conjunto a otro y de una zona a otra.")
    d.p("**La solución: reglas en tres niveles.**", keep_next=True)
    d.tabla(
        ["Nivel", "Quién la fija", "Ejemplos"],
        [
            ["Sistema", "El código; nadie la apaga",
             "Residencia, zona disponible, dentro del horario, no en el pasado"],
            ["Alfa", "Administración, una por conjunto",
             "Anticipación mínima y máxima, paz y salvo, acompañantes, día límite de pago"],
            ["Beta", "Administración, una por zona",
             "Horario, días que no abre, aforo, duración de la franja, límite por vivienda, una reserva al día, "
             "sin franjas seguidas"],
        ],
        [1500, 3000, 4860], junta=True,
    )
    d.vinetas([
        "Cada regla vive en **un solo nivel** y existe **una sola vez** por conjunto o zona (índice único parcial "
        "entre las abiertas), de modo que no hay choques.",
        "**Todas se evalúan en AND** y la respuesta trae **todos** los motivos de incumplimiento, no solo el primero.",
        "**Son versionadas:** cambiar una regla cierra la vigente (`vigencia_hasta`) y abre una nueva.",
        "**Todas restringen:** ninguna regla «permite» algo. Por eso «una reserva al día» está escrita en negativo.",
        "**Un tipo de regla nuevo exige una migración**, porque un `CHECK` en la base lista los tipos válidos.",
        "**Dos modos de zona:** con reserva (salón, zona de BBQ) y con ingreso (gimnasio, piscina), donde "
        "Vigilancia registra la entrada y se controla el aforo simultáneo.",
        "**Se evalúan al enviar la solicitud:** si cumple todas pasa a `APARTADA`; si no, queda `LIBERADA` con el "
        "motivo «reglas» y la API responde `400` con la lista de motivos.",
    ])
    d.p("El evaluador (`apps/reglas/evaluador.py`) devuelve un resultado por regla, cumpla o no:")
    d.codigo([
        "def evaluar(solicitud):",
        "    resultados = [regla(solicitud) for regla in sistema.REGLAS_DEL_SISTEMA]",
        "    resultados.append(aforo(solicitud))",
        "    for regla in reglas_vigentes(solicitud.area, timezone.localdate()):",
        "        evaluar_tipo = EVALUADOR_POR_TIPO.get(regla.tipo)",
        "        motivo = evaluar_tipo(solicitud, regla.parametros)",
        "        resultados.append(Resultado(regla.tipo, ..., not motivo, motivo, ...))",
        "    return resultados   # un Resultado por regla, cumpla o no",
    ])
    d.p("**La prueba.** `apps/reglas/tests.py` cubre los niveles, la regla única por tipo, el catálogo, las "
        "restricciones de la base y el evaluador.")

    # 3.5.4
    d.h3("3.5.4 Trazabilidad")
    d.p("**El problema.** Una administración debe poder demostrar quién hizo qué y cuándo, y nada de lo registrado "
        "puede desaparecer.")
    d.p("**La solución.**")
    d.vinetas([
        "**Auditoría de solo inserción:** el modelo `Registro` y su QuerySet prohíben `update()` y `delete()` "
        "(`RegistroInmutable`). Los servicios registran con `auditoria.servicios.registrar(actor, accion, "
        "entidad, …)`.",
        "**Sin borrado físico:** un vínculo se cierra con `vigencia_hasta`; un rol se retira cerrando su vigencia; "
        "ninguna clave foránea del negocio usa `ON DELETE CASCADE`.",
        "**Anulación:** solo el Superusuario anula un registro. La fila queda, marcada con el motivo, el autor y la "
        "fecha: el error queda documentado, no desaparecido.",
    ])
    d.p("**Alcance de la protección.** Hoy la inmutabilidad de la auditoría está garantizada en Python, en el "
        "modelo. El diseño contempla además reforzarla en PostgreSQL; esa parte se describe en el recuadro de la "
        "sección 3.6.")
    d.p("**La prueba.** `apps/auditoria/tests.py` verifica el registro de solo inserción.")

    # ---- 3.6
    d.h2("3.6 Modelo de datos")
    d.p("La base `admind_db` tiene **42 tablas**: 32 del negocio y 10 del framework (Django y django-otp). "
        "Las tablas del negocio usan llaves primarias UUID, y las de cada conjunto llevan `conjunto_id` y una "
        "única `(id, conjunto_id)`, a la que apuntan sus hijas con **claves foráneas compuestas**. Hay en total "
        "42 llaves primarias, 111 foráneas, 45 únicas y 63 restricciones `CHECK`.")
    d.p("Las fotos, los logos, los comprobantes y los PDF de los documentos **se guardan dentro de la base**, en "
        "columnas `bytea`. Los comprobantes de pago se validan por su firma y solo admiten PDF, JPG o PNG de hasta "
        "5 MB; las fotos de anuncios y casos tienen el mismo tope de 5 MB.")
    d.p("**Restricciones que hace cumplir PostgreSQL.** La base es la única que ve todas las peticiones a la vez: "
        "lo que tiene que ser imposible aunque alguien se salte el código va también como restricción.", keep_next=True)
    d.tabla(
        ["Restricción", "Tipo", "Qué impide"],
        [
            ["`solicitud_franja_bloqueante_unica`", "Único parcial", "Dos trámites sobre la misma franja"],
            ["`solicitud_un_bloqueo_por_persona`", "Único parcial", "Dos bloqueos de una persona"],
            ["`asignacion_un_rol_por_conjunto`", "Único parcial", "Dos roles vigentes en un conjunto"],
            ["`ingreso_uno_abierto_por_persona`", "Único parcial", "Estar adentro de dos zonas a la vez"],
            ["`pago_unico_por_vivienda_y_mes`", "UNIQUE", "Dos pagos del mismo mes"],
            ["`persona_documento_normalizado`", "CHECK", "Un documento con puntos o espacios"],
            ["`(x_id, conjunto_id)`", "Clave foránea compuesta", "Apuntar a una fila de otro conjunto"],
        ],
        [4000, 2200, 3160], mono=(0,), junta=True,
    )
    d.p("El detalle de cada tabla, columna y restricción está en el **Diccionario de Datos**, que se entrega junto "
        "con este manual.")
    d.implementacion(
        "Procedimientos almacenados y triggers. Hoy la base no tiene ninguno: las reglas se hacen cumplir con "
        "restricciones y desde Python. Está previsto agregar cinco triggers (entre ellos, impedir `UPDATE` y "
        "`DELETE` sobre la tabla de auditoría incluso con SQL directo, y bloquear el borrado físico de "
        "reservas, pagos, casos e infracciones) y cinco procedimientos o funciones (dos de ellas alimentarán los "
        "reportes de uso de zonas y de estado de pagos). Cada uno irá en una migración y filtrará por conjunto.")


def construir(d):
    capitulo_1(d)
    capitulo_2(d)
    capitulo_3(d)
