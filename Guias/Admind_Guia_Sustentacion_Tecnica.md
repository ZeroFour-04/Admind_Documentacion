---
resumen: "Guía de estudio para la sustentación técnica: arquitectura, stack, piezas propias, recorrido de una petición y banco de preguntas del jurado con respuesta."
tipo: guia
corte: 2026-11-03
contrastado_con: "Backend b89d9f2, Frontend bdcb5c3"
---

# Guía para la sustentación técnica de AdMind

Corte: **2026-11-03**, contrastada con el código (Backend `b89d9f2`, Frontend `bdcb5c3`). Va junto con la presentación de 27 diapositivas; cada diapositiva tiene notas del orador con lo que hay que decir.

**Cómo estudiarla:** lee las secciones 1 a 6 una vez de corrido. Después tapa las respuestas de la sección 7 e intenta contestarlas en voz alta. Lo que no te salga, vuelve a la sección correspondiente.

---

## 1. AdMind en 60 segundos

AdMind es una aplicación web para administrar conjuntos residenciales en Colombia (Ley 675 de 2001). Una **sola base de datos** guarda a muchos conjuntos, y el reto técnico es que ningún conjunto vea los datos de otro.

Lo que se defiende no es un CRUD. Son **cuatro piezas que no salen de un tutorial**, y cada una tiene una prueba automática que la vigila:

| Pieza | Problema que resuelve | Dónde vive | Prueba que la vigila |
|---|---|---|---|
| Aislamiento multiconjunto | Que A nunca vea ni toque datos de B | `apps/comun/aislamiento/` | `tests/aislamiento/test_intruso.py` |
| Concurrencia | Que 50 clics simultáneos den una sola reserva | `apps/comun/bloqueo/` + índices únicos parciales | `tests/concurrencia/` |
| Motor de reglas | Que cada conjunto configure sus reglas | `apps/reglas/` | `apps/reglas/tests.py` |
| Trazabilidad | Que nada se borre y todo quede registrado | `apps/auditoria/` | `apps/auditoria/tests.py` |

---

## 2. Arquitectura general

### Dos proyectos Django separados

```
Navegador ──HTML/forms──▶ Frontend :8001 ──JSON + Token──▶ API :8000 ──SQL──▶ PostgreSQL 18
                          (plantillas,                      (DRF: views,
                           cliente_api,                      serializers,
                           DATABASES = {})                   servicios, models)
```

- **Backend (API):** Django + Django REST Framework. Es el **único** que toca la base. Habla JSON.
- **Frontend:** Django con plantillas + Alpine.js. Tiene `DATABASES = {}`: **no puede** tocar la base. Cada pantalla llama a la API.
- **Por qué separados:** el contrato es la API. Otra interfaz (app móvil) podría usarla sin tocar el backend, y el front no puede saltarse las reglas porque no tiene base.
- **El costo:** cada pantalla se traduce a llamadas HTTP. Eso hace `cliente_api/`.

### La analogía del restaurante (sirve para explicarlo rápido)

| Restaurante | AdMind |
|---|---|
| Comedor | Las pantallas (front) |
| Mesero | `cliente_api/` |
| Ventanilla de la cocina | Vistas y serializers de la API |
| Chef | `servicios.py` |
| Despensero | El Manager del modelo |
| Despensa | PostgreSQL |

Tres reglas: el mesero nunca entra a la despensa; el de la ventanilla no cocina; el despensero siempre usa la lista del conjunto correcto.

### Las capas que pidió el profesor

El profesor pidió **controlador → servicio → repositorio** (su plantilla de ASP.NET). La equivalencia:

| ASP.NET | AdMind | Qué hace |
|---|---|---|
| Controllers | `urls.py` + `views.py` | Exige permiso, valida, llama al servicio, traduce a HTTP |
| Dtos | `serializers.py` | Forma de la entrada y de la salida |
| Services | `servicios.py` | Reglas de negocio. **No sabe nada de HTTP** |
| Repositories | `models.py` + `ManagerDeConjunto` | Buscar y guardar, ya filtrado por conjunto |
| Utilities | `apps/comun/` | Aislamiento, bloqueo, archivos |

**Lo que se evalúa es la dirección de las llamadas:** las flechas solo bajan. Señales de error: `Area.objects` dentro de una vista (se salta dos capas) o `request`/`Response` dentro de un servicio (ya sabe de HTTP).

**Patrón de errores:** el servicio dice *qué* pasó con una excepción de negocio (`FranjaOcupada`, `BloqueoVencido`); la vista decide *cómo* se dice en HTTP (`409`).

### Códigos HTTP

| Código | Cuándo |
|---|---|
| 200 / 201 | Lectura correcta / se creó algo |
| 400 | El JSON no tiene la forma correcta, o mandaron `conjunto` en la petición |
| 401 | Sin token, o token vencido |
| 403 | Sin permiso, sin conjunto activo, o falta el segundo factor |
| 404 | No existe **o es de otro conjunto** (nunca 403) |
| 409 | El estado no permite la operación (la franja ya está tomada) |
| 429 | Demasiados intentos (recuperar contraseña, búsquedas) |

---

## 3. Stack y por qué

| Tecnología | Versión | Para qué |
|---|---|---|
| Python | 3.14 | Todo el proyecto |
| Django | 5.2.17 LTS | Rutas, ORM, migraciones, plantillas, sesiones |
| Django REST Framework | 3.18 | `APIView`, serializers, autenticación, permisos |
| PostgreSQL | 18, nativo | La base; hace cumplir restricciones |
| psycopg | 3.3 | Conector Django ↔ PostgreSQL |
| django-otp + qrcode | 1.7 / 8.2 | Segundo factor TOTP y su QR |
| requests | 2.34 | Llamadas del front a la API |
| Alpine.js | 3.17 | Interactividad puntual en el HTML |
| pytest + pytest-django | 9.1 / 4.14 | Pruebas |
| python-dotenv | 1.2 | Leer `.env` (secretos fuera del código) |

- **Django y no FastAPI:** autenticación, hash, sesiones, permisos, migraciones y 2FA vienen de fábrica. FastAPI es más rápido y async, pero la latencia de AdMind la decide la transacción en PostgreSQL, igual en los dos.
- **Django 5.2 y no 6.x:** es LTS (soporte hasta abril de 2028) y tiene más material.
- **PostgreSQL desde el día 1, nunca SQLite:** SQLite no da índices únicos parciales con la misma garantía, ni FK compuestas contra claves únicas compuestas que hagan falta aquí, ni privilegios por tabla.
- **Plantillas + Alpine y no React:** la app es sobre todo formularios y tablas; el HTML se genera en el servidor y JavaScript solo va donde hay interacción real. Sin npm ni compilación.
- **Sin Docker:** PostgreSQL 18 corre como servicio de Windows. Docker quedó como deseable, no como requisito.

---

## 4. Las cuatro piezas propias, a fondo

### 4.1 Aislamiento multiconjunto

**El problema:** las reservas de dos conjuntos están en la misma tabla, separadas por una columna. Si una consulta olvida filtrar, nada se rompe: simplemente se filtran datos. Eso es tratamiento no autorizado bajo la Ley 1581.

**Tres líneas de defensa independientes:**

1. **`VistaDeConjunto`** (`apps/comun/aislamiento/vistas.py`): clase base de toda vista con datos de un conjunto. En `initial()`, después de autenticar:
   - si llega `conjunto` o `conjunto_id` en URL, query o cuerpo → **400**;
   - si la sesión no tiene conjunto activo → **403**;
   - fija el conjunto del token en una **ContextVar**.
   - `dispatch()` corre dentro de `contexto_limpio()`, así que al terminar la petición la variable se suelta aunque haya error.
2. **`ManagerDeConjunto`** (`managers.py`): reemplaza `Modelo.objects`. Su `get_queryset()` agrega `filter(conjunto_id=conjunto_activo_id())`. **Sin conjunto activo lanza `SinConjuntoActivo`**: falla a propósito, no devuelve todo.
3. **FK compuesta** en PostgreSQL (`migraciones.py` → `fk_compuesta()`): `FOREIGN KEY (area_id, conjunto_id) REFERENCES areas_area (id, conjunto_id)`. La base **rechaza físicamente** una fila que apunte a otro conjunto.

**`ModeloDeConjunto`** (`apps/comun/modelos_base/modelos.py`) es la base de toda tabla de conjunto: id UUID, campo `conjunto` con `on_delete=PROTECT`, `UniqueConstraint(id, conjunto)` (lo que permite la FK compuesta), el Manager filtrado y un `save()` que lanza `EscrituraEnOtroConjunto` si la fila es de otro conjunto.

**ContextVar en una frase:** una variable "por petición"; aunque dos peticiones corran a la vez, cada una ve su propio valor.

**Por qué no es un middleware de Django:** los middleware corren antes de que DRF autentique el token, así que todavía no se sabe quién es ni qué conjunto tiene.

**Por qué 404 y no 403:** un 403 confirma que el recurso existe. Por eso los mensajes son «No encontrado» y los ids son UUID.

**Row Level Security se descartó:** obliga a fijar una variable de sesión en cada conexión; mantener eso cuesta más que las FK compuestas.

**Tablas globales (la lista cerrada):** `Persona`, `Usuario`, `Conjunto`, `TokenDeSesion`, los catálogos de permisos y `Asignacion` (su conjunto es nulo para el Superusuario). `tests/esquema/test_tablas_globales.py` falla si aparece otra tabla sin `conjunto_id`.

**Límites conocidos:** `bulk_create()` y `update()` se saltan `save()`; `Asignacion` no se filtra sola; el admin de Django y el shell necesitan `usar_conjunto()`; las relaciones hacia adelante (`reserva.area`) no pasan por el Manager, pero la FK compuesta garantiza que son del mismo conjunto.

### 4.2 Concurrencia: el bloqueo de 3 minutos

**El problema:** 50 residentes pulsan «Reservar» en la misma franja en el mismo milisegundo.

**La solución no es preguntar primero.** Si se consulta «¿está libre?» y luego se inserta, dos peticiones pueden ver «libre» a la vez (*check-then-act*). AdMind **intenta el INSERT directamente**:

```python
def tomar(crear):
    try:
        with transaction.atomic():
            return crear()            # INSERT de la solicitud
    except IntegrityError as error:
        raise RecursoOcupado(nombre_de_la_restriccion(error))
```

Lo que impide el duplicado es un **índice único parcial**:

```sql
UNIQUE (area, fecha, hora_inicio) WHERE estado IN ('EN_SOLICITUD','APARTADA','RESERVADA')
```

- "Parcial" = solo cuenta las filas bloqueantes. Una expirada o liberada sale del índice y la franja queda libre **sin borrar nada**.
- Hay un segundo índice, `solicitud_un_bloqueo_por_persona`: una persona no puede tener dos bloqueos a la vez en un conjunto. Con el nombre de la restricción que devuelve psycopg se sabe cuál falló y se responde distinto.
- **Expiración sin proceso en segundo plano:** `expirar_vencidos()` hace un solo `UPDATE` al principio de cada consulta o acción de reservas. Es idempotente: lo que ya no está activo no se toca.
- **Mecanismo compartido (R1):** reservas, parqueadero de visitantes y citas usan el mismo `apps/comun/bloqueo/`.
- **El aforo es distinto:** es una suma de filas, no una fila única, así que ningún índice lo custodia. El servicio de ingresos toma la fila del área con `select_for_update` (bloqueo de fila en PostgreSQL) y cuenta dentro de la transacción.
- **Prueba:** `tests/concurrencia/test_bloqueo_de_franjas.py` lanza N hilos contra la misma franja en PostgreSQL real y verifica que queda un solo bloqueo.

### 4.3 Flujo de estados de una reserva

```
EN_SOLICITUD ──enviar y cumple──▶ APARTADA ──aprobar──▶ RESERVADA
     │                                │                     │
     ├─ vencen 3 min → EXPIRADA       └─ rechazar →         └─ cancelar →
     └─ la suelta o incumple reglas      RECHAZADA              CANCELADA
        → LIBERADA
```

- **Bloqueantes:** `EN_SOLICITUD`, `APARTADA`, `RESERVADA`. **No bloqueantes:** `EXPIRADA`, `LIBERADA`, `RECHAZADA`, `CANCELADA`.
- **El estado vive en la solicitud, no en la franja.** La franja es una coordenada `(área, fecha, hora inicio, hora fin)`; el calendario se calcula, no se guarda.
- **Principio:** el orden de llegada decide quién puede pedir; una persona (Administración) decide quién obtiene.
- **Confirmación de contenido:** antes de enviar se repite «sábado 26 de diciembre de 2026, de 2:00 p. m. a 6:00 p. m.». El día de la semana en letras atrapa el error típico de oprimir la casilla equivocada.
- **Rechazo:** categoría obligatoria de lista cerrada; con `OTRO`, texto libre obligatorio.
- **Dos oportunidades por franja (R9):** dejar vencer el bloqueo gasta una oportunidad; soltarlo a propósito no.
- **Pago:** el sistema no valida dinero. Guarda quién declaró el pago y cuándo, y el comprobante si lo subieron. Solo Administración declara.

### 4.4 Motor de reglas

**Tres niveles:**

| Nivel | Quién la fija | Ejemplos |
|---|---|---|
| Sistema | El código, nadie la apaga | Residencia, zona disponible, dentro del horario, no en el pasado |
| Alfa | Administración, una por conjunto | Anticipación mínima y máxima, paz y salvo, acompañantes, día límite de pago |
| Beta | Administración, una por zona | Horario, días que no abre, aforo, duración de franja, límite por vivienda, una reserva al día, sin franjas seguidas |

- Cada regla vive en **un solo nivel** y existe **una sola vez** por conjunto o zona (índice único parcial entre las abiertas). Así no hay choques.
- **Todas en AND** y la respuesta trae **todos** los motivos, no solo el primero.
- **Versionadas:** cambiar una regla cierra la vigente (`vigencia_hasta`) y abre una nueva.
- **Todas restringen:** ninguna regla "permite" algo. Por eso «una reserva al día» está escrita en negativo.
- **Un tipo nuevo exige migración:** un `CHECK` en la base lista los tipos válidos.
- **Dos modos de zona:** con reserva (salón, BBQ: este flujo) y con ingreso (gimnasio, piscina: Vigilancia registra y se controla el aforo simultáneo).
- **Cuándo se evalúan:** al enviar. Si cumple todas → `APARTADA`; si no → `LIBERADA` con motivo «reglas» y 400 con la lista de motivos.

```python
def evaluar(solicitud):
    resultados = [regla(solicitud) for regla in sistema.REGLAS_DEL_SISTEMA]
    resultados.append(aforo(solicitud))
    for regla in reglas_vigentes(solicitud.area, hoy):
        resultados.append(EVALUADOR_POR_TIPO[regla.tipo](solicitud, regla.parametros))
    return resultados   # un Resultado por regla, cumpla o no
```

### 4.5 Trazabilidad

- **Auditoría de solo inserción:** `Registro` prohíbe `update()` y `delete()` en el modelo y en su QuerySet (`RegistroInmutable`). Los servicios llaman a `auditoria.servicios.registrar(actor, accion, entidad, …)`.
- **Sin borrado físico:** un vínculo se cierra con `vigencia_hasta`; un rol se retira cerrando su vigencia; ninguna FK tiene `ON DELETE CASCADE`.
- **Anulación:** solo el Superusuario. La fila queda, marcada con motivo, autor y fecha. El error queda documentado, no desaparecido.
- **Honestidad:** el diseño pide además quitarle a la aplicación el privilegio de `UPDATE`/`DELETE` sobre la auditoría en PostgreSQL (`REVOKE`). En el código actual no hay esa migración; la protección está en Python.

---

## 5. Identidad, permisos y segundo factor

### Sesión y token

1. `POST /auth/login/` con correo y contraseña → se crea un `TokenDeSesion` y se devuelve un token aleatorio. **En la base solo se guarda su huella SHA-256.**
2. La sesión dura **1 hora** y guarda usuario, **conjunto activo** y si el 2FA ya se verificó.
3. Si la persona tiene un conjunto, se elige solo; si tiene varios, pasa por el selector (`POST /auth/conjunto-activo/`).
4. En cada petición, `AutenticacionPorToken` lee `Authorization: Token …`, busca la sesión vigente y devuelve `(usuario, sesion)`. La sesión es `request.auth`, y de ahí sale el conjunto activo.

**Por qué token opaco y no JWT:** se revoca al instante (logout borra la sesión) y guarda estado (conjunto activo, 2FA). Un JWT es válido hasta que vence y no se puede revocar sin una lista negra.

**Permisos por defecto de DRF** (`config/settings.py`): `IsAuthenticated` + `DosFactoresAlDia`.

### Segundo factor (HU-02)

- Con `django-otp`: código de 6 dígitos tipo Google Authenticator, con QR para configurarlo.
- Quien tiene **algún permiso sensible** no puede hacer nada (403) hasta verificarlo; las vistas necesarias para verificar se marcan con `permitida_sin_segundo_factor = True`.
- Si se pierde el teléfono: enlace firmado al correo que incluye el id del dispositivo TOTP; al borrar el dispositivo el enlace deja de valer, sin tabla nueva. Costo aceptado: el 2FA protege tanto como el buzón.

### Recuperar contraseña (HU-01)

Enlace de un solo uso por correo, vence en 1 hora, **máximo 3 por hora** por correo (throttling de DRF). Responde lo mismo exista o no la cuenta, para no revelar qué correos están registrados.

### Roles y permisos (HU-06)

| Rol | Alcance | Qué hace |
|---|---|---|
| Superusuario | Plataforma (conjunto nulo) | Crea conjuntos, anula registros, opera el sistema |
| Administración | Conjunto | Reglas, áreas, personas, aprueba reservas |
| Secretaría | Conjunto | Triage, prioridad, rechazo formal, anuncios. **No aprueba** |
| Vigilancia | Conjunto | Visitantes, ingresos a zonas |
| Residente | Conjunto | Reserva, abre casos, ve anuncios y documentos |

- **Catálogo fijo en código** (`apps/permisos/catalogo.py`). El administrador solo asigna; si un conjunto necesita otro cargo, el equipo lo ajusta en código.
- **Un solo rol vigente** por persona y conjunto: se cambia, no se suma. Cambiar cierra el actual y abre el nuevo **en la misma transacción**.
- **Nunca cero Administración** en un conjunto (`UltimaAdministracion`).
- Primera línea de cada vista: `exigir_permiso(request, "reserva.aprobar")` → 403 si falta.
- **Los permisos del front solo deciden qué se ve.** Quien decide es la API en cada petición.

---

## 6. Frontend, base de datos, pruebas y proceso

### Frontend

- **`cliente_api/http.py` → `pedir(request, método, ruta, datos)`:** saca el token de la sesión, llama con `requests` (10 s), y convierte fallas en `ApiNoDisponible` (la API no respondió) o `ErrorDeApi` (respondió con error), con el mensaje en español y los errores por campo. Un archivo por app del backend, una función por endpoint.
- **`apps/cuentas/sesion.py`:** guarda token, conjunto activo, permisos, rol y estado del 2FA; la sesión vence a la misma hora que el token. `SesionRequeridaMiddleware` exige sesión salvo en vistas `@publica`.
- **Sesión en archivo** con cookie `HttpOnly`: el JavaScript del navegador no puede leer el token.
- **Plantillas:** `templates/base/` (esqueleto) y `templates/componentes/` (barra, lateral, campo, confirmación). CSS propio con componentes `am-*`, sin Tailwind ni Bootstrap.
- **Alpine.js** solo en la cuenta regresiva de la reserva, buscadores, el paso de viviendas, el recortador de foto. La cuenta regresiva **solo muestra**: el vencimiento lo decide la API.

### Restricciones en PostgreSQL (las que hay que saber)

| Restricción | Tipo | Qué impide |
|---|---|---|
| `solicitud_franja_bloqueante_unica` | Único parcial | Dos trámites sobre la misma franja |
| `solicitud_un_bloqueo_por_persona` | Único parcial | Dos bloqueos de una persona |
| `asignacion_un_rol_por_conjunto` | Único parcial | Dos roles vigentes en un conjunto |
| `ingreso_uno_abierto_por_persona` | Único parcial | Estar adentro de dos zonas a la vez |
| `pago_unico_por_vivienda_y_mes` | UNIQUE | Dos pagos del mismo mes |
| `persona_documento_normalizado` | CHECK | Documento con puntos o espacios |
| FK compuesta `(x_id, conjunto_id)` | FK | Apuntar a otro conjunto |

Regla general: **la base es la única que ve todas las peticiones a la vez.** Lo que tiene que ser imposible aunque alguien se salte el código va también como restricción.

### Pruebas

| Suite | Cuántas (conteo de funciones, 03/11) | Cómo |
|---|---|---|
| Backend | ~735 | pytest-django crea y borra una base de prueba; `config/settings_pruebas.py` |
| Frontend | ~450 | Sin base ni API real: `mock.patch("cliente_api.reservas.franjas", …)` |

Las que más pesan: **intruso** (todas las rutas desde otro conjunto), **tablas globales** (el esquema) y **concurrencia** (hilos contra PostgreSQL real). Lo que no cubren: el JavaScript propio y la prueba manual con usuarios reales.

> Antes de sustentar corre las dos suites y usa el número real:
> `./.venv/Scripts/python.exe -m pytest -q` en cada repositorio.

### Proceso

- **Tres repositorios** separados (no submódulos): backend, frontend y documentación (bóveda de Obsidian).
- **Ramas** fijadas por el profesor: `main`, `pruebas`, `desarrollo`; desde el 24/10, una rama corta por cambio que entra a `desarrollo` con PR.
- **Commits:** `feat(app): descripción [HU-NN]`.
- **Scrum:** 40 historias en 7 sprints con puntos de historia. Definition of Done: pruebas en verde, prueba del intruso, y prueba manual de quien no programó.
- **Migraciones:** `makemigrations` y, a mano, `fk_compuesta(...)` al final de cada migración. `makemigrations --check` comprueba que el modelo y las migraciones coinciden.

---

## 7. Banco de preguntas del jurado

**Arquitectura**

1. **¿Por qué dos servidores y no uno?** Para que back y front se comuniquen solo por una API: el front no puede saltarse reglas (no tiene base) y otra interfaz podría usar la misma API. El costo es traducir cada pantalla a llamadas HTTP.
2. **¿Dónde está el patrón controlador-servicio-repositorio?** `views.py` es el controlador, `serializers.py` el DTO, `servicios.py` el servicio y el Manager del modelo el repositorio. La vista no consulta el ORM para decidir y el servicio no devuelve respuestas HTTP.
3. **¿Por qué el servicio no puede saber de HTTP?** Porque la misma regla la usan otras entradas (importación masiva, scripts, pruebas) y porque así se prueba llamando una función, sin servidor.
4. **¿Qué pasa si la API está caída?** `cliente_api` lanza `ApiNoDisponible` y la pantalla muestra «No hay conexión con el servidor de AdMind…».

**Aislamiento**

5. **¿Cómo garantizan que un administrador de A no vea datos de B?** Tres capas independientes: `VistaDeConjunto` toma el conjunto del token y rechaza cualquier `conjunto` en la petición; `ManagerDeConjunto` filtra toda consulta; y la FK compuesta en PostgreSQL impide filas cruzadas. Lo vigila la prueba del intruso sobre todas las rutas.
6. **¿Y si un programador olvida heredar de `VistaDeConjunto`?** El Manager falla sin conjunto activo (error 500, no una fuga), y la prueba del intruso marca la ruta como no registrada.
7. **¿Por qué 404 y no 403?** Un 403 confirma que el recurso existe; eso ya es información filtrada.
8. **¿Por qué no Row Level Security?** Obliga a fijar una variable de sesión en cada conexión; mantenerlo cuesta más que las FK compuestas, que ya hacen imposible el dato cruzado.
9. **¿Por qué no un esquema o una base por conjunto?** No se discutió como alternativa formal en la documentación; si lo preguntan: una base compartida con columna `conjunto_id` permite que una `Persona` exista en varios conjuntos y simplifica migraciones (una sola), a cambio de tener que blindar el filtro, que es justo lo que hacen las tres capas.
10. **¿Cómo hacen la FK compuesta si Django no la soporta?** FK normal + `UniqueConstraint(id, conjunto)` en el padre + `RunSQL` en la migración. Django no sabe que existe; PostgreSQL sí, y la impone. No se usó `CompositePrimaryKey` porque la PK sigue siendo UUID.
11. **¿Qué es una ContextVar y por qué no una variable global?** Una variable por contexto de ejecución: cada petición ve su valor aunque corran a la vez. Una global se mezclaría entre peticiones.

**Concurrencia**

12. **¿Cómo evitan que dos personas reserven la misma franja?** No preguntan si está libre: intentan el INSERT y un índice único parcial lo rechaza para el segundo. La base decide una sola vez.
13. **¿Por qué parcial?** Para que solo cuenten los estados bloqueantes; al expirar o liberarse, la fila sale del índice y la franja queda libre sin borrar.
14. **¿Quién expira los bloqueos vencidos?** Nadie en segundo plano: cada consulta empieza con un `UPDATE` que expira lo vencido. Es idempotente y no depende de un proceso corriendo.
15. **¿Y el aforo?** Es una suma, no una fila: el servicio bloquea la fila del área con `select_for_update` y cuenta dentro de la transacción.
16. **¿Cómo lo probaron?** Con hilos contra PostgreSQL real (`tests/concurrencia/`): N peticiones simultáneas, un solo bloqueo.
17. **¿Por qué 3 minutos y no configurable?** Es el tiempo para llenar y enviar, no el de la reserva. Si cada conjunto lo cambia, deja de haber una sola explicación posible.

**Reglas**

18. **¿Qué es alfa y beta?** Alfa: regla del conjunto (vale para todas sus zonas). Beta: regla de una zona. Además están las del sistema, fijas en código.
19. **¿Por qué devolver todos los motivos?** Para que el residente corrija todo de una vez y no a punta de intentos.
20. **¿Cómo agregarían un tipo de regla nuevo?** Su evaluador en `evaluador.py`, su descripción en el catálogo y una migración que actualiza el `CHECK` de tipos válidos.

**Seguridad e identidad**

21. **¿Por qué token opaco y no JWT?** Se revoca al instante y guarda estado (conjunto activo, 2FA). En la base solo se guarda su SHA-256.
22. **¿Dónde vive el token en el navegador?** No vive en el navegador: está en la sesión del servidor del front, en archivo; el navegador solo tiene la cookie de sesión `HttpOnly`.
23. **¿Cómo funciona el 2FA?** TOTP con `django-otp`. Quien tiene un permiso sensible recibe 403 en todo hasta verificar el código (`DosFactoresAlDia`).
24. **¿Qué impide enumerar correos en la recuperación?** La respuesta es la misma exista o no la cuenta, y hay un límite de 3 enlaces por hora.
25. **¿Cómo validan los archivos subidos?** Por su firma (los primeros bytes), no por el nombre ni por el tipo que dice el navegador; PDF, JPG o PNG hasta 5 MB, con SHA-256. Se guardan en la base y se entregan por un endpoint validado.
26. **¿Quién controla al Superusuario?** Solo la auditoría: puede leer datos de residentes y queda registrado que lo hizo (R10). Es el riesgo abierto más caro, y se aceptó para no construir un módulo de acceso de emergencia.

**Base de datos y ley**

27. **¿Por qué PostgreSQL y no SQLite?** Índices únicos parciales, FK compuestas y privilegios por tabla, que sostienen los invariantes principales.
28. **¿Por qué no borran nada?** Valor probatorio: un registro que el administrador puede borrar no prueba nada. Se cierra la vigencia o se anula con motivo.
29. **¿Cómo implementan una prohibición legal?** No como permiso denegado: la operación no existe. No hay permiso `sancionar` ni campo de multa.

**Pruebas y proceso**

30. **¿Cómo prueban el front sin la API?** Simulando cada función de `cliente_api` con `mock.patch` y revisando el HTML que sale.
31. **¿Qué no está probado?** El JavaScript propio y la prueba manual con usuarios reales de la DoD.
32. **¿Cómo usaron la IA?** Como asistente con planes guiados por historia; las decisiones están registradas con fecha y autor en la bóveda.

---

## 8. Datos para memorizar

- Puertos: **API 8000**, **front 8001**. Base: **admind_db**, PostgreSQL 18.
- Token: **1 hora**, se guarda solo su **SHA-256**. Bloqueo de reserva: **3 minutos**.
- **5 roles** (sin Consejo). **Un rol vigente** por persona y conjunto.
- Recuperación: **3 enlaces por hora**. Archivos: **PDF/JPG/PNG, 5 MB**, validados por firma.
- Estados bloqueantes: **EN_SOLICITUD, APARTADA, RESERVADA**.
- Reglas: **sistema, alfa (conjunto), beta (zona)**, todas en AND.
- Cerca de **100 rutas** en la API, todas en la prueba del intruso.

---

## 9. Lo que la documentación y el código no dicen igual (al 03/11)

Conviene saberlo para no contradecirse delante del jurado. **Manda el código.**

- **Citas e infracciones:** la nota de estado (corte 13/10) las da como "sin código", pero hoy `apps/citas/` (horario de atención y agenda) y `apps/infracciones/` tienen modelos, servicios, vistas y pruebas. `apps/triage/` del backend sigue solo con README.
- **Pruebas:** la nota dice 723 y 435; el conteo de funciones de prueba hoy da ~735 y ~451. Correr las suites antes de sustentar.
- **Auditoría por privilegios:** el diseño habla de `REVOKE` en PostgreSQL; no hay ninguna migración con `REVOKE`. La protección es el modelo.
- **Middleware de aislamiento:** el documento maestro dice middleware; lo construido es `VistaDeConjunto` (explicado en 4.1).
- **Roles:** el maestro dice varios roles por persona y un rol Consejo; lo vigente es un rol por conjunto y 5 roles.

## Ver también

- [vision_general](../02_Arquitectura/vision_general.md), [backend](../02_Arquitectura/backend.md), [frontend](../02_Arquitectura/frontend.md)
- [aislamiento](../03_Reglas/aislamiento.md), [capas](../03_Reglas/capas.md), [restricciones_bd](../02_Arquitectura/restricciones_bd.md)
- [reservas](../05_Modulos/reservas.md), [motor_reglas](../05_Modulos/motor_reglas.md), [cuentas](../05_Modulos/cuentas.md), [permisos](../05_Modulos/permisos.md)
- [riesgos](../06_Decisiones/riesgos.md), [legal](../01_Contexto/legal.md)
