---
resumen: "Plan de los anuncios con hasta 4 fotos y su galería en el tablón."
titulo: "AdMind — Plan de anuncios con fotos"
tipo: plan
estado: hecho
ejecutado: 2026-10-05
hu: [HU-25]
fecha: 2026-10-05
para: "Un agente que construye (no es un plan guiado); Alejo decide y revisa"
alcance: "HU-25, ampliación: un anuncio se publica con solo texto o con texto y hasta 4 fotos, y las fotos se ven en el tablón"
punto_de_partida: "Backend 39d66b1 (344 pruebas: 343 pasan y 1 falla, la conocida), Frontend afcd6e6 (169 pruebas). Los dos con cambios sin commit de otro trabajo. En admind_db faltan por aplicar areas.0002 y visitantes.0001"
---

# AdMind — Plan de anuncios con fotos

> [!IMPORTANT]
> **Plan terminado el 2026-10-05.** Es histórico: lo vigente está en [construccion](../../06_Decisiones/construccion.md) y [triage](../../05_Modulos/triage.md). D1 a D8 las respondió Alejo ese día, todas con la recomendada, y el agente lo construyó de F0 a F4. Lo que cambió al ejecutarlo está al final, en *Desviaciones al ejecutar*.

## 0. Instrucciones para el agente

### 0.1 Qué leer antes de tocar código

1. Este plan completo. Las secciones 2 y 3 son decisiones ya tomadas.
2. Notas: [triage](../../05_Modulos/triage.md) (sección *Anuncios con alcance*), [invariantes](../../03_Reglas/invariantes.md), [capas](../../03_Reglas/capas.md), [reglas_frontend](../../03_Reglas/reglas_frontend.md), [pruebas_y_ejecucion](../../02_Arquitectura/pruebas_y_ejecucion.md) y [conjuntos](../../05_Modulos/conjuntos.md), porque la foto del conjunto es el modelo de esta funcionalidad.
3. Los `README.md` de `Backend/Admind_Backend/apps/anuncios/`, `Frontend/Admind_Front-End/apps/anuncios/` y `Frontend/Admind_Front-End/cliente_api/`.
4. Como modelo de estilo, el código que ya existe: en el back, `apps/conjuntos/` (`LogoDeConjunto`, `guardar_logo`, `LogoDelConjuntoView`, `ImagenDelLogoView`); en el front, `apps/conjuntos/views.py` (`identidad` y `logo`), `cliente_api/conjuntos.py` y `tests/test_identidad.py`.

### 0.2 Reglas propias de este plan

- **Los dos repositorios tienen cambios sin commit que no son de este plan** (áreas, segundo factor y reglas). No se revierten ni se "arreglan". Prohibido `git add -A`, `git stash`, `git restore` y `git checkout --`. `tests/aislamiento/test_intruso.py` está entre los modificados: se vuelve a leer justo antes de editarlo.
- **No se toca:** `config/` de ningún repositorio, `apps/comun/`, `apps/conjuntos/`, `apps/notificaciones/`, `apps/permisos/catalogo.py`, `design-system/` ni `requirements.txt`. Si un paso parece necesitarlo, es una desviación: se para y se pregunta.
- **Sin paquetes nuevos y sin JavaScript nuevo.** No se instala Pillow ni nada.
- **Commits:** según D8. Nunca `git push`.
- **Migración en `admind_db`:** según D7, y siempre `migrate anuncios`, nunca `migrate` a secas: hay dos migraciones ajenas sin aplicar (`areas.0002_quitar_clasificacion` y `visitantes.0001_initial`).
- **La prueba roja conocida no se arregla aquí.** `test_toda_ruta_de_la_api_esta_cubierta` falla por `usuario-perfil` y `usuario-eliminar`. Tiene que seguir fallando solo por esas dos: si aparece `anuncio-foto` en el mensaje, la fase F2 no está cerrada.
- Si el código real difiere del plan en un nombre o una ruta, manda el código: se adapta y se anota en el informe final. Si difiere en una regla, se para y se pregunta.

## 1. Punto de partida

Medido el 2026-10-05, ramas `desarrollo`.

| Dónde | Qué hay |
|---|---|
| Backend `39d66b1` | 344 pruebas: 343 pasan y 1 falla (la conocida). `makemigrations --check --dry-run`: sin cambios |
| Frontend `afcd6e6` | 169 pruebas, todas pasan |
| `Backend/…/apps/anuncios/` | **HU-25 construida con solo texto.** `Anuncio` (`titulo`, `cuerpo`, `alcance`, `unidad`, `autor`, `publicado_en`, `editado_en`), migración `0001_initial`. Servicios: `publicar`, `destinatarios`, `editar`, `tablon`, `puede_editar`, `PERMISO_POR_ALCANCE`. Vistas: `AnunciosView` (GET, POST) y `DetalleDeAnuncioView` (GET, PATCH). Rutas `anuncios` y `anuncio-detalle`. 11 pruebas en `tests.py` |
| `Backend/…/apps/conjuntos/` | El patrón de imagen: `LogoDeConjunto` (`BinaryField` en tabla propia), `tipo_real_de_imagen()` y `FIRMAS_DE_IMAGEN` en `servicios.py`, la vista que lee el tope más un byte y la que sirve los bytes con su tipo |
| `Backend/…/config/settings.py` | No declara `DEFAULT_PARSER_CLASSES`: DRF ya acepta JSON y `multipart/form-data` |
| `Frontend/…/apps/anuncios/` | Vistas `lista`, `nuevo` y `editar`; `AnuncioForm` y `EditarAnuncioForm`; plantillas `lista.html`, `nuevo.html`, `editar.html` y `_campo_cuerpo.html` |
| `Frontend/…/cliente_api/` | `anuncios.py`: `listar`, `publicar`, `obtener`, `editar`. `http.py`: `pedir(..., archivos=)` ya manda multipart y `pedir_archivo()` descarga una imagen |
| `Frontend/…/tests/test_anuncios.py` | 14 pruebas. Dos leen `publicar_en_api.call_args.args[1]` y esperan ahí solo `titulo`, `cuerpo`, `alcance` y `unidad` |
| Permisos | Administración y Secretaría ya tienen `anuncio.publicar` y `anuncio.dirigir`. No cambia nada del catálogo |

Sin diferencias entre las notas y el código en lo que este plan toca.

## 2. Decisiones que toma Alejo

| ID | Decisión | Opciones | Recomendada | Respuesta |
|---|---|---|---|---|
| D1 | Cuántas fotos lleva un anuncio | a) hasta 4 b) solo 1 c) hasta 8 | a | **a** (chat, 2026-10-05) |
| D2 | ¿Las fotos cambian después de publicar? | a) quedan fijas, como el alcance b) se pueden agregar c) agregar y quitar | a | **a** (chat, 2026-10-05) |
| D3 | Dónde se guardan | a) en la base, tabla propia b) en disco | a | **a** (chat, 2026-10-05) |
| D4 | Peso de cada foto | a) tope de 5 MB, sube tal cual b) reducir en el navegador c) tope de 2 MB | a | **a** (chat, 2026-10-05) |
| D5 | Qué dice el aviso (bandeja y correo) cuando el anuncio lleva fotos | a) nada nuevo: solo el texto b) una línea al final: *"Este anuncio tiene 2 fotos. Míralas en AdMind."* c) fotos adjuntas al correo (obliga a tocar el canal: quedaría fuera de este plan) | b | **b** (chat, 2026-10-05) |
| D6 | Aviso junto al campo de fotos sobre datos personales (Ley 1581) | a) sí: *"Una foto donde se reconoce a una persona es un dato personal: publícala solo con su permiso."* b) sí, con otro texto (escríbelo) c) sin aviso | a | **a** (chat, 2026-10-05) |
| D7 | Quién aplica la migración nueva en `admind_db` | a) el agente, con `migrate anuncios`, al cerrar F1 b) Alejo | a | **a** (chat, 2026-10-05) |
| D8 | Commits | a) el agente no hace commits: deja por fase el mensaje sugerido y la lista de archivos b) el agente hace un commit por fase, solo con los archivos del plan (`git add` por ruta), sin `push` | a | **a** (chat, 2026-10-05) |

## 3. Decisiones menores que el plan ya fija

| ID | Decisión |
|---|---|
| P1 | Modelo nuevo `FotoDeAnuncio(ModeloDeConjunto)` en `apps/anuncios/models.py`: `anuncio` (FK con `PROTECT`, `related_name="fotos"`), `contenido` (`BinaryField`), `tipo` (el real, 20 caracteres) y `orden`. Tabla propia para que leer un anuncio no traiga la imagen, igual que `LogoDeConjunto` |
| P2 | `MAXIMO_DE_FOTOS = 4` vive en `models.py`, porque lo usa una restricción. `TAMANO_MAXIMO_FOTO = 5 * 1024 * 1024` vive en `servicios.py`, como `TAMANO_MAXIMO_LOGO` |
| P3 | El tope lo hace cumplir también la base: `UNIQUE (anuncio, orden)` más `CHECK (orden < 4)`. Con eso un quinto registro es imposible aunque alguien se salte el código |
| P4 | Formatos: PNG, JPG y WebP, por la firma del archivo. Se reutiliza `tipo_real_de_imagen` importándola de `apps.conjuntos.servicios`; no se mueve a `comun`. No hay proporción fija, así que no se leen dimensiones |
| P5 | Cada regla en su capa ([capas](../../03_Reglas/capas.md)): el serializer cuenta las fotos; el servicio valida cada una (vacía, peso, firma) y levanta `FotoInvalida`; la base guarda el tope. La vista lee de cada archivo el tope más un byte, como `LogoDelConjuntoView` |
| P6 | Todo o nada: se validan todas las fotos antes de crear nada, y anuncio, fotos y aviso van en la misma transacción. Con una foto inválida no se publica ni se avisa |
| P7 | La imagen se pide en `GET /anuncios/<anuncio_id>/fotos/<foto_id>/` (ruta `anuncio-foto`, `VistaDeConjunto`). Se entrega solo si el anuncio está en el `tablon()` de la persona; si no, 404. No exige permiso, igual que leer el tablón |
| P8 | Ninguna lectura del tablón trae `contenido`: las fotos se precargan con `defer("contenido")`. Esa consulta se arma dentro de la función y no como constante del módulo, porque `ManagerDeConjunto` filtra por conjunto en el momento de llamarlo |
| P9 | `PATCH` con `fotos` responde 400 *"Las fotos de un anuncio no cambian después de publicarlo."* La pantalla de editar las muestra y no ofrece cambiarlas |
| P10 | Las fotos se crean una por una con `objects.create()`, no con `bulk_create()`: así `save()` fija el conjunto |
| P11 | En el front, la imagen la pide este servidor con el token y se la pasa al navegador, como `conjuntos.views.logo`: solo entrega PNG, JPG o WebP y responde con `Cache-Control: private, max-age=31536000, immutable`, porque la foto de un id no cambia (D2) |
| P12 | El formulario del front revisa el número y el peso antes de llamar a la API, como `LogoForm`. El tipo real lo decide solo la API |
| P13 | `cliente_api.anuncios.publicar(request, datos, fotos=())`: sin fotos sigue mandando JSON; con fotos manda multipart con el campo `fotos` repetido. `datos` no lleva las fotos. En `cliente_api/http.py` solo cambia el docstring de `pedir` |
| P14 | Galería: una lista de miniaturas dentro de la tarjeta del anuncio; cada una enlaza a la foto completa en otra pestaña. CSS en `static/css/estructura.css`, solo con variables. No es un componente nuevo ni lleva JavaScript |
| P15 | Texto alternativo genérico: *"Foto 1 de 3 del anuncio Corte de agua"*. No hay descripción por foto |
| P16 | Mensajes de la API, bajo el campo `fotos`: *"Un anuncio lleva hasta 4 fotos."*, *"La foto 2 está vacía."*, *"La foto 2 pesa más de 5 MB."* y *"La foto 2 no es una imagen PNG, JPG o WebP."* |

## 4. Orden y dependencias

F0 → F1 → F2 → F3 → F4. El back va completo antes del front. Cada fase termina con las suites como dice su cierre.

### Contrato de la API

| Petición | Cambio | Respuesta |
|---|---|---|
| `POST /anuncios/` | Además de JSON acepta `multipart/form-data` con `titulo`, `cuerpo`, `alcance`, `unidad` y `fotos` (0 a 4 archivos, campo repetido) | 201 con `"fotos": ["<uuid>", …]` en orden · 400 `{"fotos": ["…"]}` |
| `GET /anuncios/` y `GET /anuncios/<id>/` | Cada anuncio trae `"fotos"`: los ids en orden, o `[]` | 200 |
| `GET /anuncios/<id>/fotos/<foto_id>/` | Nueva | 200 con los bytes y su `Content-Type` real · 404 |
| `PATCH /anuncios/<id>/` | Rechaza `fotos` | 400 |

## F0 · Punto de partida

Confirmar el `git status` y el último commit de los dos repositorios y correr las suites. Se espera lo de la sección 1. Si los conteos cambiaron por trabajo ajeno, se anota y se sigue. Si falla una prueba de anuncios o `makemigrations` detecta cambios, se para.

## F1 · Backend: la tabla de fotos

**Archivos:** `apps/anuncios/models.py`, `apps/anuncios/migrations/0002_fotos.py`, `apps/anuncios/tests.py`.

**Construye:** `MAXIMO_DE_FOTOS` y `FotoDeAnuncio` (P1 a P3), con `Meta` que hereda `ModeloDeConjunto.Meta`, repite `*ModeloDeConjunto.Meta.constraints`, ordena por `orden` y trae un índice encabezado por `conjunto`. La migración se genera con `makemigrations anuncios` y al final de `operations` se agrega a mano `fk_compuesta("anuncios_fotodeanuncio", "anuncio_id", "anuncios_anuncio")`.

**Pruebas que la dan por hecha:**
- La base rechaza dos fotos con el mismo `orden` en un anuncio.
- La base rechaza una foto con `orden` 4 o mayor.
- La base rechaza una foto que apunta a un anuncio de otro conjunto.

**Cierre:** suite del back (las 3 nuevas en verde y la única roja es la conocida) y `makemigrations --check --dry-run` sin cambios. Con D7 = a, `migrate anuncios`.

**Commit sugerido (Backend):** `feat(anuncios): agregar la tabla de fotos del anuncio [HU-25]`

## F2 · Backend: publicar con fotos y servir la imagen

**Archivos:** `apps/anuncios/serializers.py`, `servicios.py`, `views.py`, `urls.py`, `tests.py`, `README.md` y `tests/aislamiento/test_intruso.py`.

**Construye:**
- `PublicarAnuncioSerializer`: campo `fotos`, opcional, lista de archivos; valida el número (P16). `EditarAnuncioSerializer` rechaza `fotos` (P9). `AnuncioSerializer` agrega `fotos` con los ids en orden.
- `servicios.py`: `TAMANO_MAXIMO_FOTO`, la excepción `FotoInvalida` con su mensaje, la validación de cada foto, `publicar(..., fotos=())` con P6 y P10, la precarga sin `contenido` en `tablon()` (P8) y una función que devuelve la foto solo si su anuncio es visible para la persona (P7). `publicar` devuelve el anuncio de forma que serializarlo no cargue `contenido`. Con D5 = b, el cuerpo del aviso lleva la línea final, en singular o plural.
- `views.py`: `AnunciosView.post` saca las fotos de los datos validados, lee de cada una el tope más un byte y traduce `FotoInvalida` a 400 bajo `fotos`. Vista nueva para la imagen, que no usa el ORM: llama al servicio y responde 404 si no hay foto.
- `urls.py`: la ruta `anuncio-foto`.
- `test_intruso.py`: `anuncio-foto` entra en `DETALLES` con una función que crea un anuncio con una foto en el otro conjunto.
- `README.md` de la app: la tabla de la API con el contrato de la sección 4.

**Pruebas que la dan por hecha** (por la API, en `apps/anuncios/tests.py`):
- Publicar con dos fotos las guarda en orden y la respuesta trae sus ids.
- Publicar solo texto por JSON sigue funcionando y responde `fotos: []`.
- Con cinco fotos: 400, y no queda anuncio ni aviso.
- Un archivo de texto con nombre `.png`: 400, y no queda anuncio ni aviso.
- Una foto que pasa el tope de peso: 400.
- PNG, JPG y WebP se guardan con su tipo real aunque la petición declare otro.
- Quien ve el anuncio recibe la imagen con su `Content-Type`.
- El vecino de otra vivienda recibe 404 al pedir la foto de un anuncio dirigido.
- Una foto pedida con el id de otro anuncio responde 404.
- `PATCH` con `fotos` responde 400 y las fotos siguen igual.
- Leer el tablón no consulta la columna `contenido` (se revisa el SQL capturado).
- Con D5 = b: el aviso de un anuncio con fotos termina con la línea; el de uno sin fotos no cambia.

**Cierre:** suite del back y `makemigrations --check --dry-run`. La roja sigue nombrando solo `usuario-perfil` y `usuario-eliminar`.

**Commit sugerido (Backend):** `feat(anuncios): publicar con fotos y servir la imagen [HU-25]`

## F3 · Frontend: subir fotos al publicar

**Archivos:** `cliente_api/anuncios.py`, `cliente_api/http.py` (solo el docstring), `apps/anuncios/forms.py`, `views.py`, `templates/anuncios/nuevo.html` y `tests/test_anuncios.py`.

**Construye:**
- `AnuncioForm`: campo `fotos`, opcional y múltiple, con el patrón de Django para varios archivos (un widget con `allow_multiple_selected = True` y un campo que limpia cada archivo). Revisa número y peso (P12), con las mismas constantes que la API.
- `nuevo`: recibe `request.FILES`, separa las fotos de los datos y llama a `api_anuncios.publicar(request, datos, fotos)` (P13).
- `nuevo.html`: el formulario pasa a `enctype="multipart/form-data"`; campo de archivo con `multiple`, el mismo `accept` y las mismas clases que el de `conjuntos/identidad.html`, con su `label`, su ayuda (*"Opcional. Hasta 4 fotos PNG, JPG o WebP, de hasta 5 MB cada una."*) y su error. Con D6 = a o b, el aviso va como texto de ayuda de ese campo.

**Pruebas que la dan por hecha:**
- El formulario es multipart y ofrece el campo de fotos múltiple.
- Publicar con fotos se las pasa a `cliente_api` aparte, y `datos` sigue trayendo solo los cuatro campos de siempre.
- Con cinco fotos no se llama a la API.
- Con una foto que pasa el tope no se llama a la API.
- El rechazo de la API por tipo real se muestra junto al campo de fotos.
- `cliente_api.anuncios.publicar` sin fotos manda JSON y con fotos manda multipart con `fotos` repetido (simulando `cliente_api.http.requests.request`, como `test_el_logo_viaja_a_la_api_como_formulario_multipart`).
- Las 14 pruebas que ya existen siguen en verde sin relajar lo que comprueban.

**Cierre:** suite del front.

**Commit sugerido (Frontend):** `feat(anuncios): subir fotos al publicar un anuncio [HU-25]`

## F4 · Frontend: ver las fotos

**Archivos:** `cliente_api/anuncios.py`, `apps/anuncios/urls.py`, `views.py`, `templates/anuncios/lista.html`, `editar.html`, `README.md`, `static/css/estructura.css` y `tests/test_anuncios.py`.

**Construye:**
- `cliente_api.anuncios.foto(request, anuncio_id, foto_id)` con `pedir_archivo`.
- Ruta `anuncios:foto` y su vista (P11).
- `lista.html`: la galería (P14, P15) entre el texto y las acciones, solo si el anuncio trae fotos. `editar.html`: las mismas miniaturas y, en la guía, que las fotos tampoco se cambian.
- CSS de la galería en el bloque *Anuncios y notificaciones* de `estructura.css`: cuadrícula que se acomoda sola al ancho, miniaturas recortadas con `object-fit`, borde y radio con variables.

**Pruebas que la dan por hecha:**
- El tablón muestra una miniatura por foto, con su enlace y su `alt`; un anuncio sin fotos no pinta la lista.
- La vista de la foto entrega la imagen de la API con caché privada.
- Si la API responde 404, o un tipo que no es PNG, JPG ni WebP, la vista responde 404.
- Editar muestra las fotos y no trae campo de archivo.

**Cierre:** suite del front. Con los dos servidores arriba, recorrer el guion de abajo y revisar la galería a 360 px de ancho y a 200 % de zoom ([lista_de_salida](../../03_Reglas/lista_de_salida.md)).

**Commit sugerido (Frontend):** `feat(anuncios): mostrar las fotos en el tablón [HU-25]`

## Cierre del agente

1. Comandos de verificación de [pruebas_y_ejecucion](../../02_Arquitectura/pruebas_y_ejecucion.md) en los dos repositorios.
2. Repasar [lista_de_salida](../../03_Reglas/lista_de_salida.md).
3. [actualizar_contexto](../../09_Protocolos/actualizar_contexto.md). Como mínimo: una fila en [bitacora](../../08_Estado/bitacora.md); una fila en [construccion](../../06_Decisiones/construccion.md) con D1 a D8; la fila de HU-25 en [historias](../../08_Estado/historias.md); la sección de anuncios de [triage](../../05_Modulos/triage.md) con un recuadro que diga que ahora llevan fotos, sin reescribir el texto de diseño; la ruta nueva en [mapa_codigo](../../02_Arquitectura/mapa_codigo.md); los conteos en [pruebas_y_ejecucion](../../02_Arquitectura/pruebas_y_ejecucion.md) y [estado_actual](../../08_Estado/estado_actual.md).
4. Mover este archivo a `07_Planes/hechos/` y cambiar su fila en [planes](../planes.md).

## Lo que el agente no puede hacer

- El PR `desarrollo → pruebas` revisado y la prueba manual de quien no programó (Camilo). Van a [pendientes](../../08_Estado/pendientes.md).
- Avisarle a Camilo: hay una migración nueva en `anuncios`, y la respuesta de `/anuncios/` ahora trae `fotos`.
- Mover HU-25 en Notion.

## Guiones de prueba manual

Con los dos servidores arriba y los usuarios de `crear_usuarios_prueba`.

1. Como Administración, publicar un anuncio solo con texto: sale en el tablón sin fotos.
2. Publicar para todo el conjunto con un JPG y un PNG: salen dos miniaturas, y cada una abre la foto completa en otra pestaña.
3. Elegir cinco fotos: el formulario lo rechaza y no se publica nada.
4. Subir un `.txt` renombrado a `.png`: el error sale junto al campo.
5. Subir una foto de más de 5 MB: el error sale junto al campo.
6. Como Secretaría, publicar para una vivienda con una foto.
7. Como residente de esa vivienda: ve el anuncio con su foto, y el aviso está en Notificaciones (con la línea de las fotos si D5 = b).
8. Como residente de otra vivienda: no ve el anuncio, y al pegar la dirección de la foto recibe *No encontrado*.
9. Como quien lo publicó, editar: se ven las fotos, solo cambia el texto y no llega un aviso nuevo.
10. Recorrer el formulario con `Tab` y revisar el tablón a 360 px.

## Informe final que entrega el agente

Qué se construyó por fase; archivos tocados; pruebas antes y después en cada repositorio; commits hechos o mensajes sugeridos (D8); si la migración quedó aplicada (D7); desviaciones del plan; lo que quedó fuera; las notas actualizadas; y tres preguntas de jurado sobre este código, con su respuesta corta.

## Fuera de este plan

- Agregar o quitar fotos después de publicar (D2) y eliminar anuncios, que sigue abierto en [pendientes](../../08_Estado/pendientes.md).
- Visor ampliado dentro de la página, reducir la foto en el navegador (D4) y adjuntar las fotos al correo (D5 c).
- Mover `tipo_real_de_imagen` a `apps/comun/` para que no dependa de `conjuntos`.
- Auditoría de la publicación: `apps/anuncios/` no registra en `apps/auditoria/` hoy.
- El acuse de lectura que nombra el `README.md` de la app: no está construido.
- Arreglar la prueba roja del intruso (`usuario-perfil`, `usuario-eliminar`) y hacer commit de los cambios ajenos.

## Desviaciones al ejecutar

- **F0.** Entre escribir el plan y ejecutarlo, Alejo hizo commit de los cambios ajenos: Backend `5ed32a5` y Frontend `ea0e9e5`, con los árboles limpios. Los conteos eran los mismos (343 de 344 y 169).
- **F2.** Quedaron 14 pruebas de fotos en `apps/anuncios/tests.py` y un caso nuevo en la prueba del intruso; la foto vacía y la pesada van en una sola prueba. Resultado: Backend 362 pruebas (361 pasan y falla la conocida, solo por `usuario-perfil` y `usuario-eliminar`).
- **F4.** Se agregó un archivo que el plan no nombraba, `templates/anuncios/_fotos.html`: la galería, que usan el tablón y la pantalla de editar. Resultado: Frontend 180 pruebas.
- **Cierre de F4.** El guion manual con usuarios reales no lo recorrió el agente: no tiene la contraseña ni el segundo factor de los usuarios de prueba, y publicar en `admind_db` manda correo real por SMTP. En su lugar corrió un recorrido desechable con el front y la API de verdad sobre la base de pruebas (publicar con 4 fotos, con 1 y sin fotos; el rechazo de la API junto al campo; 5 fotos; cada foto devuelta igual a como subió; 404; editar), y revisó la galería en el navegador a 360 px y a 1280 px, con el foco de teclado. La prueba manual queda en [pendientes](../../08_Estado/pendientes.md).
- **D7.** La migración `anuncios/0002_fotos` quedó aplicada en `admind_db` con `migrate anuncios`. `areas.0002` y `visitantes.0001` siguen sin aplicar.
- **D8.** Sin commits del agente. Los mensajes sugeridos son los de cada fase.
