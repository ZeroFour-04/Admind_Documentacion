---
resumen: "Plan de las zonas con ingreso: modo de uso, permanencia, acompañantes y registro de entrada y salida por Vigilancia con aforo simultáneo."
titulo: "AdMind — Plan de zonas con ingreso"
tipo: plan
estado: hecho
ejecutado: 2026-10-08
hu: []
fecha: 2026-10-08
para: "Un agente que construye (no es un plan guiado); Alejo decide y revisa. Sin commits"
alcance: "El segundo modo de uso de una zona: con ingreso. Modo de uso y permanencia máxima en el área, regla de acompañantes, registro de entrada y salida por Vigilancia con aforo simultáneo, cupos a la vista antes de reservar y pantallas separadas por rol. Sin historia todavía. No incluye el vínculo habitante"
punto_de_partida: "Backend 279e963 (416 pruebas: 415 pasan y 1 falla, la conocida), Frontend f5b3d08 (210 pruebas, todas pasan). Los dos limpios, sin migraciones pendientes en admind_db"
---

# AdMind — Plan de zonas con ingreso

> [!NOTE] Plan ejecutado el 2026-10-08, sin commit
> Las decisiones D1 a D9 quedaron respondidas el 2026-10-08 (D3 pasó de c a a) y el agente construyó las fases F0 a F7 el mismo día. Quedan para Alejo: el texto del aviso de finalidad (hoy es un marcador visible), `migrate` en `admind_db`, los commits, la prueba manual y avisarle a Camilo ([pendientes](../../08_Estado/pendientes.md)). Lo construido está en [ingresos](../../05_Modulos/ingresos.md).

## 0. Instrucciones para el agente

### 0.1 Qué leer antes de tocar código

1. Este plan completo. Las secciones 2 y 3 son decisiones ya tomadas.
2. Notas: [ingresos](../../05_Modulos/ingresos.md), [motor_reglas](../../05_Modulos/motor_reglas.md) (*Definición vigente* y *Cómo está construido*), [invariantes](../../03_Reglas/invariantes.md), [capas](../../03_Reglas/capas.md), [reglas_frontend](../../03_Reglas/reglas_frontend.md), [pruebas_y_ejecucion](../../02_Arquitectura/pruebas_y_ejecucion.md) y [legal](../../01_Contexto/legal.md) §4.2.
3. En [pendientes](../../08_Estado/pendientes.md), la sección *Motor de reglas y zonas con ingreso*: si trae una condición previa que este plan no nombra, se para y se pregunta.
4. Los `README.md` de `Backend/Admind_Backend/apps/` (`areas`, `reglas`, `reservas`, `permisos`, `comun/bloqueo`, `unidades`) y de `Frontend/Admind_Front-End/apps/` (`areas`, `reglas`, `reservas`, `visitantes`) y `cliente_api/`.
5. Como modelo de estilo: en el back, `apps/reservas/servicios.py` (`decidir_solicitud` por el `select_for_update`, `expirar_vencidas`, `enviar` por guardar el estado antes de lanzar el error) y `apps/reglas/evaluador.py`; en el front, `apps/reglas/views.py` (`cargar_tablero`) y `tests/test_reglas.py`. **`apps/visitantes/` no es modelo de capas:** su vista usa el ORM y revisa el rol por nombre.

### 0.2 Reglas propias de este plan

- **Sin commits y sin `push`.** Alejo lo pidió así. Al cierre de cada fase queda el mensaje sugerido y la lista de archivos.
- **`config/` se toca en un solo punto por repositorio:** una línea en `INSTALLED_APPS` y una en `urls.py` para la app `ingresos`. `config/settings_pruebas.py` no se toca. Nada más de `config/`, ni `apps/comun/`, ni `design-system/`, ni `requirements.txt`.
- **Sin paquetes, sin componentes, tokens ni colores nuevos.** Solo `am-tabla`, `am-pastilla`, `am-campo`, `am-btn`, `am-alerta`, `am-vacio` y las clases que ya están en `static/css/estructura.css` y `reservas.css`. Si una pantalla parece pedir un componente, se para y se pregunta.
- **Puede haber otro chat trabajando en los mismos repositorios.** Se vuelve a leer cada archivo justo antes de editarlo. Prohibido `git add -A`, `git stash`, `git restore` y `git checkout --`.
- **La prueba roja conocida no se arregla aquí.** `test_toda_ruta_de_la_api_esta_cubierta` falla por cinco rutas (`usuario-perfil`, `usuario-eliminar`, `solicitudes-bandeja`, `solicitudes-area` y `solicitud-decision`). Tiene que seguir fallando solo por esas cinco: si aparece una ruta de `ingresos`, F4 no está cerrada.
- **Migraciones en `admind_db`:** según D6.
- Si el código real difiere del plan en un nombre o una ruta, manda el código: se adapta y se anota. Si difiere en una regla, se para y se pregunta.

## 1. Punto de partida

Medido el 2026-10-08, ramas `desarrollo`, los dos árboles limpios.

| Dónde | Qué hay |
|---|---|
| Backend `279e963` | 416 pruebas: 415 pasan y 1 falla (la conocida). `makemigrations --check --dry-run`: sin cambios. Sin migraciones pendientes en `admind_db` |
| Frontend `f5b3d08` | 210 pruebas, todas pasan |
| `apps/areas/` (back) | `Area` no tiene modo de uso. `duracion_franja_minutos` es obligatoria, con `CHECK area_duracion_franja_minima` (≥ 120). `aforo_maximo` obligatorio. `servicios.CAMPOS_EDITABLES` y `franjas_del_dia`. Última migración: `0004_aforo_maximo` |
| `apps/reglas/` (back) | `catalogo.py` con cinco tipos vigentes (`NIVEL_POR_TIPO`, `PARAMETROS_POR_TIPO`, `DESCRIPCION_POR_TIPO`, `tipos_vigentes`). `evaluador.evaluar(solicitud)` recibe una `Solicitud` e importa `apps.reservas.models`; salta los tipos sin evaluador. `sistema.Resultado` es reutilizable; las tres reglas del sistema reciben una solicitud. `mora.unidad_en_mora` responde siempre que no. Última migración: `0004_niveles_y_unicidad` |
| `apps/reservas/` (back) | `franjas` y `tomar_bloqueo` no distinguen modos |
| `apps/comun/bloqueo/` | `tomar(crear)` traduce un choque de índice único a `RecursoOcupado`. `expirar_vencidos` hace un solo `UPDATE` de estado: no sirve tal cual, porque la salida automática también fija la hora y avisa |
| `apps/permisos/catalogo.py` | Vigilancia tiene `visitante.registrar` y `reserva.ver_todas`. **No tiene `area.ver`** |
| `apps/unidades/` | `VinculoUnidad.objects.vigentes()` y `unidades_para_solicitar(persona)`. `TipoVinculo` solo tiene propietario y arrendatario |
| `apps/personas/` | `normalizar_documento`. La persona es única por **tipo y número** de documento |
| `apps/notificaciones/canal.py` | `Aviso` y `notificar(aviso, persona_ids)`: no repite un aviso con el mismo `origen` y `referencia` |
| `apps/areas/` y `apps/reglas/` (front) | `AreaForm`, `EditarAreaForm`, `_campos_area.html` y `_tabla_areas.html` (los usa también el paso de áreas del asistente). El tablero de reglas cruza catálogo, reglas y áreas en `cargar_tablero` |
| `apps/reservas/` (front) | «Zonas comunes» es `reservas:calendario`: un selector con todas las áreas activas y el calendario. No dice cómo se usa cada una |
| `templates/componentes/lateral.html` | «Zonas comunes» y «Reglas» salen para todos los roles. `tests/test_visitantes.py::test_vigilancia_solo_ve_las_secciones_permitidas_en_el_lateral` fija lo que ve Vigilancia |

**Diferencias entre las notas y el código:**

- [ingresos](../../05_Modulos/ingresos.md) dice que se identifica «por número de documento». En el código dos personas pueden compartir número con distinto tipo (CC y TI): lo resuelve P11.
- A Vigilancia, hoy «Zonas comunes» y «Reglas» le responden «No tienes permiso para hacer esto»: `GET /areas/` y `GET /reglas/` exigen permisos que su rol no tiene. Lo decide D5.
- [pruebas_y_ejecucion](../../02_Arquitectura/pruebas_y_ejecucion.md) dice que la prueba roja falla por dos rutas; son cinco.

## 2. Decisiones que toma Alejo

| ID | Decisión | Opciones | Recomendada | Respuesta |
|---|---|---|---|---|
| D1 | ¿El vínculo `habitante` entra en este plan? | a) fuera: se busca entre quienes tienen vínculo vigente con `reside`; hoy son los titulares y la familia entra como acompañante b) primera fase del plan | a | **a** (chat, 2026-10-08) |
| D2 | Permisos nuevos | a) `ingreso.registrar` para Vigilancia e `ingreso.ver_historico` para Administración, sensible b) solo `ingreso.registrar` c) reusar los de visitantes | a | **a** (chat, 2026-10-08) |
| D3 | Lo legal de 12.10 b, sin verificar | a) construir con salvaguardas: aviso de finalidad en la pantalla de Vigilancia, no se copia el documento, historial solo con permiso sensible, paz y salvo conectado al mismo interruptor de reservas (hoy sin efecto), piscinas fuera b) igual, pero el ingreso no evalúa paz y salvo c) no construir todavía | a | **a** (chat, 2026-10-08; antes estaba en c). El texto del aviso de finalidad queda como marcador hasta que salga de la verificación legal |
| D4 | Supuestos de las dos notas | Confirmar o cambiar: el modo de uso no cambia después de crear la zona; un ingreso abierto por persona en el conjunto; los acompañantes entran y salen con su residente; la permanencia va en minutos y la salida prevista no pasa del cierre; el aviso a vigilancia va en su pantalla, no por correo; si la persona vive en dos viviendas, el vigilante elige cuál | confirmar | **Confirmados todos** (chat, 2026-10-08) |
| D5 | Qué ve Vigilancia en el menú | a) gana «Ingreso a zonas» y dejan de salirle «Zonas comunes» y «Reglas», que hoy le responden sin permiso; cambia la prueba del lateral de `test_visitantes.py`, que es de Camilo b) solo gana «Ingreso a zonas» | a | **b** (chat, 2026-10-08) |
| D6 | Quién aplica las migraciones en `admind_db` | a) Alejo, al final b) el agente, al cerrar cada fase del back | a | **a** (chat, 2026-10-08) |
| D7 | Palabras en pantalla ([abiertas](../../06_Decisiones/abiertas.md) 12.10 d) | a) como hoy: «área» en gestión y «Zonas comunes» para el residente; el modo se dice «Con reserva» y «Con ingreso» b) pasar todo a «zona» (toca unas 15 plantillas más; quedaría como plan aparte) | a | **a** (chat, 2026-10-08) |
| D8 | Acompañantes cuando la regla no está definida | a) entran, con el aforo como único tope; la regla lleva `maximo` desde 0, y 0 es «no se permiten». Así todas las reglas siguen solo restringiendo b) no entran; definir la regla los permite. Sería la primera regla que permite algo | a | **a** (chat, 2026-10-08) |
| D9 | Supuestos que faltó preguntar | Al cumplirse el tiempo, la persona puede volver a entrar si hay cupo; un ingreso abierto conserva su hora de salida aunque cambie la permanencia del área; paz y salvo es un solo interruptor para reservas e ingresos (solo aplica con D3 = a). a) confirmar los tres b) cambios | a | **a**: los tres confirmados (chat, 2026-10-08) |

## 3. Decisiones menores que el plan ya fija

| ID | Decisión |
|---|---|
| P1 | App nueva `ingresos` en los dos repositorios. Una tabla nueva, `Ingreso`, de conjunto. Ninguna tabla global |
| P2 | `Area` gana `modo_uso` (`reserva` o `ingreso`; las que existen quedan en `reserva`) y `permanencia_maxima_minutos` (de 15 a 1 440, vacía en las de reserva). `duracion_franja_minutos` pasa a admitir vacío. `CHECK area_modo_coherente`: con reserva hay duración y no hay permanencia; con ingreso, al revés. `area_duracion_franja_minima` se conserva |
| P3 | El modo se elige al crear y no cambia (D4): `PATCH /areas/<id>/` con `modo_uso` responde 400 «El modo de uso no cambia después de crear el área.» La permanencia se edita solo en un área con ingreso; la duración, solo en una con reserva |
| P4 | Un área con ingreso no se reserva: `franjas_del_dia` devuelve una lista vacía y `tomar_bloqueo` lanza una excepción propia, que la vista traduce a 409 «Esta área no se reserva: el ingreso se registra en portería.» |
| P5 | `catalogo.MODOS_POR_TIPO` dice a qué modo aplica cada regla: anticipación mínima, máxima y límite por vivienda, a reserva; acompañantes, a ingreso; paz y salvo y días que no abre, a los dos. `GET /reglas/catalogo/` lo entrega en `modos`. Definir una regla de área en un área de otro modo responde 400 bajo `area` |
| P6 | Tipo nuevo `ACOMPANANTES`, alfa, con `{"maximo": entero desde 0}` (D8 a). En palabras: «Máximo 2 acompañantes por vivienda a la vez» o «No se permiten acompañantes». El evaluador de reservas ya salta los tipos que no conoce: no cambia |
| P7 | `Ingreso(ModeloDeConjunto)`: `area`, `persona`, `unidad`, `acompanantes`, `estado` (`ADENTRO`, `SALIO`, `VENCIDO`), `entrada_en`, `salida_prevista_en`, `salida_en`, `registrado_por`, `salida_registrada_por` y `evaluacion` (copia de las reglas evaluadas, como en `Solicitud`). No guarda el documento: solo la referencia a la persona. FK con `PROTECT` y FK compuestas a `areas_area` y `unidades_unidad` |
| P8 | En la base: índice único parcial `ingreso_uno_abierto_por_persona` sobre `(conjunto, persona)` con `estado = ADENTRO`; `CHECK` de estado válido, de salida prevista posterior a la entrada y de que `salida_en` está vacía solo mientras está `ADENTRO`; índices encabezados por `conjunto` |
| P9 | **El último cupo.** El aforo es una suma, no una fila única, así que no lo puede decidir un índice. `registrar` abre una transacción, toma la fila del área con `select_for_update` (dos registros a la misma zona pasan de a uno), da salida a los vencidos, cuenta y, si cabe, inserta con `bloqueo.tomar`. Prueba de concurrencia propia |
| P10 | Ocupación = por cada ingreso `ADENTRO` del área, uno más sus acompañantes. Cupos = aforo menos ocupación, nunca menos de 0 |
| P11 | **Buscar al residente:** `POST`, para que el documento no viaje en la URL. La consulta vive en `apps/unidades/servicios.py`: personas con ese número normalizado **y** vínculo vigente con `reside` en el conjunto activo, cada una con sus viviendas. Sin resultado responde 404 «No encontrado», exista o no la persona en otro conjunto. Si dos personas comparten número, llegan las dos y el vigilante elige. Responde nombre y viviendas: sin teléfono, correo ni tipo de documento. Cada búsqueda queda en la auditoría |
| P12 | Salida prevista = entrada más la permanencia del área, sin pasar de la hora de cierre de ese día (D4). Queda guardada en el ingreso (D9) |
| P13 | **Salida automática al siguiente acceso**, sin procesos en segundo plano: toda lectura y toda acción del módulo empieza por `dar_salida_a_vencidos()`, que pasa a `VENCIDO` los `ADENTRO` cuya salida prevista ya pasó, les pone esa hora como `salida_en` y avisa al residente por el canal (`origen="ingreso"`). A Vigilancia no le llega correo: los ve en su pantalla (D4) |
| P14 | El evaluador del ingreso es un módulo propio, `apps/ingresos/evaluador.py`, que reutiliza `reglas.sistema.Resultado`, `reglas.servicios.reglas_vigentes`, `catalogo.motivos_del_dia` y `mora.unidad_en_mora`. `reglas` no importa `ingresos`. Orden: sistema (reside en esa vivienda; área activa, sin mantenimiento y con ingreso; dentro del horario; sin otro ingreso abierto), aforo, acompañantes, paz y salvo (solo con D3 = a) y días que no abre. Todas en Y, y la respuesta trae todos los motivos |
| P15 | Un registro rechazado no crea fila: responde 400 con `motivos`. Uno aceptado deja `ingreso.registrar` en la auditoría, y la salida manual, `ingreso.salida`. La salida automática no tiene actor: queda en el propio ingreso |
| P16 | Las vistas exigen el permiso y nada más: no revisan el rol por nombre. Las pantallas deciden qué mostrar con `tiene_permiso` |
| P17 | Los cupos son un conteo, sin nombres: los ve quien tenga `area.ver`, `area.gestionar`, `ingreso.registrar` o `ingreso.ver_historico`. Quién está adentro lo ve solo quien registra; el historial, solo `ingreso.ver_historico` |
| P18 | «Zonas comunes» abre con una tabla de todas las zonas: nombre, cómo se usa, horario y cupos ahora. El modo va como texto en su columna; la pastilla queda para el estado («Abierta», «Cerrada», «Sin cupo», «En mantenimiento»). El selector del calendario lista solo las áreas con reserva. Sin JavaScript: los cupos se refrescan al recargar, con un enlace «Actualizar» |
| P19 | La pantalla de Vigilancia registra en dos pasos, sin JavaScript: buscar (documento y acompañantes) y confirmar (nombre y vivienda a la vista, con la vivienda a elegir si hay más de una) |
| P20 | El formulario de área muestra el modo como dos opciones al crear, con los campos de cada modo rotulados («Solo para áreas con reserva», «Solo para áreas con ingreso»). Al editar, el modo se lee y no se cambia. Sin JavaScript |
| P21 | Un área con ingreso también cuenta para el requisito de áreas del asistente: `requisitos_para_operar` no cambia |
| P22 | Los mensajes sugeridos de commit llevan `[HU-??]`: Alejo pone el número cuando cree la historia |

## 4. Orden y dependencias

F0 → F1 → F2 → F3 → F4 → F5 → F6 → F7. El back va completo antes del front. Cada fase cierra con las suites.

### Qué ve cada rol

| Rol | Pantalla | Qué ve y qué hace | Permiso |
|---|---|---|---|
| Residente | Zonas comunes | Cómo se usa cada zona antes de reservar. En las de ingreso, los cupos de este momento, el horario y cuánto se puede quedar. En las de reserva, el calendario y «Reservar» | `area.ver`, `reserva.solicitar` |
| Vigilancia | Ingreso a zonas | Los cupos de cada zona, registrar una entrada, quién está adentro, registrar una salida y a quién se le cumplió el tiempo hoy | `ingreso.registrar` |
| Administración | Áreas, Reglas, Zonas comunes, Ingresos | Crea el área con su modo y su permanencia; define acompañantes; ve los cupos; consulta el historial de ingresos, sin registrar | `area.gestionar`, `regla.configurar`, `ingreso.ver_historico` |
| Secretaría | Zonas comunes, Áreas | Cómo se usa cada zona y sus cupos, en lectura | `area.ver` |

El Superusuario recibe los dos permisos nuevos porque su rol tiene todo el catálogo, como hoy.

### Contrato de la API

| Petición | Cambio | Respuesta |
|---|---|---|
| `GET /areas/` y `GET /areas/<id>/` | Traen `modo_uso` y `permanencia_maxima_minutos`. `duracion_franja_minutos` llega vacía en un área con ingreso | 200 |
| `POST /areas/` | Acepta `modo_uso` (si falta, `reserva`). Con reserva exige la duración y rechaza la permanencia; con ingreso, al revés | 201 · 400 por campo |
| `PATCH /areas/<id>/` | Rechaza `modo_uso` (P3) | 200 · 400 |
| `GET /reservas/franjas/` y `POST /reservas/solicitudes/` | Sobre un área con ingreso: sin franjas, y 409 (P4) | 200 · 409 |
| `GET /reglas/catalogo/` | Cada tipo trae `modos`; aparece `ACOMPANANTES` | 200 |
| `GET /ingresos/zonas/` | Nueva (ruta `ingresos-zonas`). Por cada área activa con ingreso: datos del área, `adentro`, `cupos`, `abierta_ahora` y `motivo_cierre` | 200 |
| `POST /ingresos/residentes/buscar/` | Nueva (`ingreso-residentes-buscar`). `{numero_documento}` | 200 `[{persona, nombre, unidades: [{id, nombre}]}]` · 404 |
| `POST /ingresos/` | Nueva (`ingresos`). `{area, persona, unidad, acompanantes}` | 201 · 400 `{"motivos": […]}` · 404 · 409 si el área no es con ingreso |
| `GET /ingresos/` | Nueva. Con `ingreso.registrar`: quién está adentro y a quién se le cumplió el tiempo hoy. Con `ingreso.ver_historico`: además `?area=` y `?fecha=` | 200 |
| `POST /ingresos/<id>/salida/` | Nueva (`ingreso-salida`) | 200 · 409 si ya había salido |

## F0 · Punto de partida

Confirmar que D3 es **a** o **b** y que D5 a D9 tienen respuesta. `git status` y último commit de los dos repositorios, y las dos suites. Se espera lo de la sección 1; si los conteos cambiaron por trabajo ajeno, se anota y se sigue. Si falla una prueba de áreas, reglas o reservas, o `makemigrations` detecta cambios, se para.

## F1 · Backend: el modo de uso en el área

**Archivos:** `apps/areas/models.py`, `migrations/0005_modo_de_uso.py`, `serializers.py`, `servicios.py`, `tests.py`, `README.md`; `apps/reservas/servicios.py`, `views.py`, `tests.py`.

**Construye:** `ModoDeUso` y los dos campos con su `CHECK` (P2). Los serializers validan los campos de cada modo y `EditarAreaSerializer` rechaza `modo_uso` (P3). `AreaSerializer` entrega los dos campos nuevos. En reservas, P4.

**Pruebas que la dan por hecha:**
- Un área existente sigue siendo con reserva y se comporta igual.
- Se crea un área con ingreso, con permanencia y sin duración; sin permanencia responde 400; con duración, 400.
- La base rechaza un área con ingreso sin permanencia y una con reserva sin duración.
- `PATCH` con `modo_uso` responde 400 y el área no cambia.
- Pedir las franjas de un área con ingreso devuelve una lista vacía; tomar un bloqueo sobre ella responde 409 y no crea solicitud.

**Cierre:** suite del back y `makemigrations --check --dry-run`.

**Commit sugerido (Backend):** `feat(areas): agregar el modo de uso y la permanencia máxima [HU-??]`

## F2 · Backend: las reglas saben de modos y de acompañantes

**Archivos:** `apps/reglas/catalogo.py`, `servicios.py`, `migrations/0005_acompanantes.py`, `tests.py`, `README.md`.

**Construye:** `MODOS_POR_TIPO` y `modos` en `tipos_vigentes()` (P5). El tipo `ACOMPANANTES` con su nivel, su validación, su descripción fija y su frase (P6). `crear` rechaza una regla de área en un área de otro modo. La migración recoge los dos `CHECK` que cambian (`regla_tipo_valido` y `regla_nivel_coherente`). Con D3 = a, la descripción de paz y salvo pasa a decir «no reserva ni ingresa».

**Pruebas que la dan por hecha:**
- El catálogo trae `modos` en cada tipo y el tipo nuevo como alfa.
- Acompañantes se define una sola vez por conjunto; con área responde 400; con `maximo` negativo o sin él, 400.
- El límite de reservas por vivienda no se define en un área con ingreso; días que no abre, sí.
- Una reserva en un conjunto con acompañantes definidos se evalúa igual que antes.

**Cierre:** suite del back y `makemigrations --check --dry-run`.

**Commit sugerido (Backend):** `feat(reglas): agregar la regla de acompañantes y el modo de cada regla [HU-??]`

## F3 · Backend: permisos, la tabla de ingresos y sus reglas

**Archivos:** `apps/permisos/catalogo.py`, `apps/permisos/tests.py`; `apps/unidades/servicios.py`, `tests.py`; app nueva `apps/ingresos/` (`__init__.py`, `apps.py`, `models.py`, `migrations/0001_initial.py`, `evaluador.py`, `servicios.py`, `tests.py`, `README.md`); `config/settings.py` (una línea); `tests/concurrencia/test_aforo_de_ingresos.py`.

**Construye:**
- Los dos permisos (D2): `ingreso.registrar` a Vigilancia; `ingreso.ver_historico` a Administración y a `PERMISOS_SENSIBLES`.
- `unidades.servicios.residentes_por_documento(numero)` (P11).
- `Ingreso` con sus restricciones (P7, P8). En la migración, después del `CreateModel`, las dos `fk_compuesta`.
- `evaluador.evaluar(ingreso, ocupacion)` (P14).
- `servicios.py`, sin HTTP: `dar_salida_a_vencidos`, `ocupacion`, `zonas`, `buscar_residente`, `registrar`, `registrar_salida`, `adentro` e `historial`. `registrar` sigue P9; como `enviar` de reservas, no lanza el error dentro de la transacción si con eso deshace una salida automática.

**Pruebas que la dan por hecha** (servicios y base):
- Entra un residente y la ocupación sube en uno más sus acompañantes.
- Con el aforo lleno no entra, y el motivo lo dice. Con un cupo y un acompañante, tampoco.
- Fuera del horario, en un día que no abre, en mantenimiento o en un área con reserva: no entra, con su motivo.
- Con dos motivos a la vez, llegan los dos.
- Quien no reside en esa vivienda no entra. Quien ya está adentro de otra zona, tampoco; la base rechaza el segundo ingreso abierto aunque se salte el servicio.
- Acompañantes: se respeta el máximo por vivienda sumando los que ya tiene adentro; con máximo 0 no entra ninguno; sin regla, según D8.
- La salida prevista no pasa del cierre.
- Al cumplirse el tiempo: el ingreso queda `VENCIDO` con su hora, el cupo se libera, al residente le llega un aviso y, si se vuelve a consultar, no llega otro.
- La salida manual libera el cupo; repetirla responde con el error de «ya salió».
- Un ingreso abierto conserva su salida aunque cambie la permanencia del área.
- La búsqueda: encuentra con puntos y espacios; no encuentra a quien solo es de otro conjunto, ni a un propietario que no reside; no trae teléfono ni correo.
- La base rechaza un ingreso que apunta a un área o a una vivienda de otro conjunto.
- Concurrencia: diez registros a la vez sobre el último cupo dejan uno solo adentro.

**Cierre:** suite del back y `makemigrations --check --dry-run`.

**Commit sugerido (Backend):** `feat(ingresos): registrar entradas y salidas con aforo simultáneo [HU-??]`

## F4 · Backend: la API de ingresos

**Archivos:** `apps/ingresos/serializers.py`, `views.py`, `urls.py`, `tests.py`, `README.md`; `config/urls.py` (una línea); `tests/aislamiento/test_intruso.py`.

**Construye:** las cinco rutas del contrato sobre `VistaDeConjunto`, cada una con `exigir_permiso` y sin tocar el ORM (P16, P17). `test_intruso.py`: `ingresos` e `ingresos-zonas` en `LISTADOS`; `ingreso-residentes-buscar` e `ingreso-salida` en `ACCIONES`. El `README.md` de la app, con la tabla de la API.

**Pruebas que la dan por hecha** (por la API):
- Vigilancia busca, registra, ve quién está adentro y registra la salida.
- Un residente y Secretaría ven los cupos y reciben 403 al buscar, registrar o listar.
- Administración ve los cupos y el historial con filtros, y recibe 403 al registrar.
- Un registro que no cumple responde 400 con todos los `motivos` y no deja fila.
- El área, la persona o la vivienda de otro conjunto responden 404.
- `conjunto` en el cuerpo responde 400.
- La respuesta de los cupos no trae nombres.

**Cierre:** suite del back. La roja sigue nombrando solo las cinco rutas de 0.2.

**Commit sugerido (Backend):** `feat(ingresos): exponer la API de ingreso a zonas [HU-??]`

## F5 · Frontend: áreas y reglas con modo

**Archivos:** `apps/areas/forms.py`, `views.py`, `templates/areas/_campos_area.html`, `_tabla_areas.html`, `README.md`; `apps/reglas/forms.py`, `views.py`, `templates/reglas/lista.html`; `tests/test_areas.py`, `tests/test_reglas.py`.

**Construye:** el modo y la permanencia en el formulario de área (P20), que también usa el paso de áreas del asistente; la columna «Cómo se usa» en la tabla. En el tablero, cada área muestra solo las reglas de su modo (`modos` del catálogo), la frase de cabecera cambia en las de ingreso, y entra `AcompanantesForm`.

**Pruebas que la dan por hecha:**
- Crear un área con ingreso manda `modo_uso` y la permanencia, sin duración.
- Editar no ofrece cambiar el modo.
- La tabla dice cómo se usa cada área.
- En el tablero, un área con ingreso no muestra el límite de reservas, y acompañantes sale entre las reglas del conjunto.
- Un 400 de la API cae en su campo.

**Cierre:** suite del front.

**Commit sugerido (Frontend):** `feat(areas): elegir el modo de uso al crear un área [HU-??]`

## F6 · Frontend: el tipo y los cupos antes de reservar

**Archivos:** `cliente_api/ingresos.py` (nuevo), `cliente_api/README.md`; `apps/reservas/views.py`, `templates/reservas/calendario.html`, `README.md`; `static/css/reservas.css` (solo si hace falta, con variables); `tests/test_reservas.py`.

**Construye:** P18. `pantalla_del_calendario` cruza las áreas con `GET /ingresos/zonas/`. Si la API de ingresos no responde, la tabla sale sin cupos y con su aviso, y reservar sigue funcionando.

**Pruebas que la dan por hecha:**
- La tabla dice cómo se usa cada zona; una con ingreso muestra «12 de 30 libres» y no ofrece «Reservar».
- Sin cupo sale «Sin cupo»; fuera de horario, «Cerrada»; en mantenimiento, «En mantenimiento».
- El selector del calendario no lista las áreas con ingreso, y `?area=` de una de ellas no pinta franjas.
- Con la API de ingresos caída, la pantalla carga y las áreas con reserva se pueden reservar.

**Cierre:** suite del front.

**Commit sugerido (Frontend):** `feat(reservas): mostrar el modo de uso y los cupos de cada zona [HU-??]`

## F7 · Frontend: la pantalla de Vigilancia, el historial y el menú

**Archivos:** app nueva `apps/ingresos/` (`__init__.py`, `apps.py`, `forms.py`, `views.py`, `urls.py`, `templates/ingresos/`, `README.md`); `config/settings.py` y `config/urls.py` (una línea cada uno); `templates/componentes/lateral.html`; `tests/test_ingresos.py` (nuevo); con D5 = a, `tests/test_visitantes.py`.

**Construye:**
- Con `ingreso.registrar`: «Ingreso a zonas», en este orden: cupos por zona, registrar en dos pasos (P19), «Adentro ahora» con «Registrar salida» y «Se les cumplió el tiempo hoy». Con D3 = a o b, el aviso de finalidad junto al formulario; su texto sale de la verificación legal.
- Con `ingreso.ver_historico`: «Ingresos», el historial con filtro por zona y por fecha, sin formulario.
- Sin ninguno de los dos: vuelve al inicio.
- El menú: «Ingreso a zonas» o «Ingresos», según el permiso; con D5 = a, Vigilancia deja de ver «Zonas comunes» y «Reglas».

**Pruebas que la dan por hecha:**
- Vigilancia ve su pantalla; un residente es devuelto al inicio; Administración ve el historial sin formulario.
- Buscar un documento muestra nombre y vivienda antes de registrar; «No encontrado» sale junto al campo.
- Un registro rechazado muestra todos los motivos y conserva lo escrito.
- «Registrar salida» llama a la API y vuelve a la pantalla.
- El menú de cada rol, según D5.

**Cierre:** suite del front. Con los dos servidores arriba, el guion de abajo, a 360 px de ancho y a 200 % de zoom ([lista_de_salida](../../03_Reglas/lista_de_salida.md)).

**Commit sugerido (Frontend):** `feat(ingresos): registrar el ingreso a zonas desde portería [HU-??]`

## Cierre del agente

1. Comandos de verificación de [pruebas_y_ejecucion](../../02_Arquitectura/pruebas_y_ejecucion.md) en los dos repositorios, y [lista_de_salida](../../03_Reglas/lista_de_salida.md).
2. [actualizar_contexto](../../09_Protocolos/actualizar_contexto.md). Como mínimo: [bitacora](../../08_Estado/bitacora.md); [construccion](../../06_Decisiones/construccion.md) con D5 a D9; *Cómo está construido* en [ingresos](../../05_Modulos/ingresos.md) y [motor_reglas](../../05_Modulos/motor_reglas.md); el catálogo en [permisos](../../05_Modulos/permisos.md); la app y las rutas en [mapa_codigo](../../02_Arquitectura/mapa_codigo.md) y [frontend](../../02_Arquitectura/frontend.md); [restricciones_bd](../../02_Arquitectura/restricciones_bd.md); [estado_actual](../../08_Estado/estado_actual.md), [pendientes](../../08_Estado/pendientes.md) y [abiertas](../../06_Decisiones/abiertas.md) 12.10.
3. Mover este archivo a `07_Planes/hechos/` y cambiar su fila en [planes](../planes.md).

## Lo que el agente no puede hacer

- Verificar lo legal (D3) ni redactar por su cuenta el aviso de finalidad.
- Crear la historia en Notion y ponerle número.
- Los commits, el PR `desarrollo → pruebas` revisado y la prueba manual de quien no programó.
- Avisarle a Camilo: dos permisos nuevos; migraciones en `areas`, `reglas` e `ingresos`; `GET /areas/` trae dos campos más y la duración puede llegar vacía; una línea nueva en `config/` de cada repositorio; y, con D5 = a, cambia su prueba del lateral.

## Guiones de prueba manual

Con los dos servidores arriba y los usuarios de `crear_usuarios_prueba`.

1. Como Administración, crear «Gimnasio» con ingreso, aforo 3 y permanencia de 60 minutos. En Áreas dice «Con ingreso».
2. En Reglas, definir acompañantes con máximo 1. El gimnasio no muestra el límite de reservas por vivienda.
3. Como residente, abrir Zonas comunes: el salón dice «Con reserva»; el gimnasio, «Con ingreso» y «3 de 3 libres», sin «Reservar».
4. Como Vigilancia, abrir «Ingreso a zonas». Buscar un documento que no es del conjunto: «No encontrado».
5. Buscar el de un residente: salen su nombre y su vivienda. Registrar con un acompañante: queda en «Adentro ahora» y el gimnasio pasa a «1 de 3 libres».
6. Registrar al mismo residente otra vez: lo rechaza y dice por qué.
7. Registrar a otro residente con un acompañante: lo rechaza por aforo.
8. Como residente, recargar Zonas comunes: el gimnasio muestra los cupos nuevos.
9. Como Vigilancia, «Registrar salida»: los cupos vuelven a 3.
10. Registrar una entrada y esperar a que pase el tiempo (con una permanencia corta): al recargar aparece en «Se les cumplió el tiempo hoy» y al residente le llega el aviso.
11. Como Administración, abrir «Ingresos»: el historial del día, sin formulario.
12. Como Vigilancia, revisar el menú según D5.

## Informe final que entrega el agente

Qué se construyó por fase, las pruebas antes y después, los archivos tocados por repositorio para que Alejo arme los commits, las desviaciones del plan y lo que quedó fuera.

## Fuera de este plan

- **El vínculo `habitante`** (D1): mientras no exista, la familia entra como acompañante de un titular. Al construirlo, el ingreso lo encuentra sin cambios.
- **Las reglas de piscina de la Ley 1209** (menores de 12 años, salvavidas).
- **Depurar el historial** al cumplirse el plazo de retención: depende de lo que salga de D3.
- **Que el vigilante confirme** que quien venció de verdad salió.
- **Cambiar el modo** de un área ya creada.
- **Cupos que se actualizan solos**, sin recargar.
- **Áreas típicas con ingreso** (gimnasio, piscina) en el paso de áreas del asistente.
- **El panel de Vigilancia** como bento, y la consulta de reservas del día que su rol ya tiene permitida.
- **Enlazar los acompañantes** con los visitantes de portería (HU-27).
- **La prueba roja** del intruso y sus cinco rutas.
