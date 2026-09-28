---
titulo: "AdMind — Plan de ejecución de los Sprints 2 y 3"
fecha: 2026-09-27
para: "Un agente de IA (Claude Sonnet) que construye; Alejo decide y revisa"
alcance: "HU-06, HU-07, HU-08, HU-09 (Sprint 2) y HU-10, HU-11, HU-12, HU-13 (Sprint 3), más la auditoría mínima que piden"
punto_de_partida: "Backend 3c70e3a (171 pruebas), Frontend b42ce93 (51 pruebas), migraciones aplicadas en admind_db, sin cambios pendientes"
---

# AdMind — Plan de ejecución de los Sprints 2 y 3

> [!IMPORTANT]
> **Alejo: antes de dárselo al agente, llena la columna "Respuesta" de la §2.** Cada decisión trae una recomendación; si estás de acuerdo, escribe "Recomendada". El agente no empieza una fase cuya decisión esté vacía.

---

## 0. Instrucciones para el agente

### 0.1 Qué leer antes de tocar código

1. Este plan completo, incluida la §3: son decisiones ya tomadas.
2. `Admin_Master.md`: §5.1 (reserva), §5.3 (roles), §5.4 (blindaje de datos), §5.5 (vínculos), §5.10 (motor de reglas) y §5.11 (invariantes de eliminación).
3. `Guias/Admind_Guia_Desarrollo.md`: §3 (capas), §3.5 (códigos de respuesta), §4.3 (reglas del front), §9 (lista de salida) y §11 (cuándo parar).
4. El `README.md` de cada carpeta que vayas a tocar, en los dos repos.
5. Como modelo de estilo, el código que ya existe. Es la referencia principal:
   - backend: `apps/anuncios/`, `apps/unidades/`, `apps/conjuntos/servicios.py`, `tests/aislamiento/test_intruso.py`;
   - front: `apps/anuncios/`, `cliente_api/anuncios.py`, `tests/test_anuncios.py`.

### 0.2 Reglas duras

1. **Construye solo lo de este plan.** Nada "de paso": ni archivos, ni refactors, ni arreglos. Si ves algo que falta fuera del plan, anótalo en el informe final (§7) y sigue.
2. **No decides.** Si un paso choca con el maestro §12, con una decisión de la §2 o con el código real de una forma que el plan no previó, detente y pregunta. Si solo cambia un nombre o una ruta, manda el código real: adáptate y anótalo en el informe.
3. **No toques:**
   - `config/settings_pruebas.py`: el cifrado rápido de contraseñas es decisión de Alejo;
   - `ModeloDeConjunto`, `Persona`, `Usuario` y el catálogo de `apps/permisos/catalogo.py`;
   - `design-system/`;
   - `Backend.zip`.
4. **Git:** la política de commits es la de D11. **Nunca** `git push`, nunca ramas nuevas, nunca `--no-verify`. Trabaja en `desarrollo`.
5. **Nada se descarga ni se instala** sin confirmación de Alejo en el chat. Eso incluye Alpine (D12) y cualquier paquete de `requirements.txt`. No agregues dependencias nuevas (ni `freezegun`, ni `factory_boy`).
6. **Terminal Git Bash**, rutas POSIX entre comillas: la carpeta raíz tiene espacios (`A D M I N D`).
7. **No sigas con la suite en rojo.** Al cerrar cada fase corre lo de §0.4; si algo falla, se arregla antes de seguir.
8. **Estilo:**
   - todo en español: nombres, docstrings y mensajes;
   - el archivo de servicios se llama `servicios.py`, no `services.py`;
   - la vista valida, exige su permiso y llama al servicio; el servicio no conoce HTTP; las excepciones de dominio viven en `servicios.py`;
   - docstrings cortos que citan el maestro o la HU (`(maestro §5.1, HU-11)`);
   - misma densidad de comentarios que el código vecino.

### 0.3 Invariantes que toda pieza nueva respeta

| Invariante | Cómo, en este código |
|---|---|
| Toda tabla nueva tiene `conjunto_id` NOT NULL | Hereda `ModeloDeConjunto` (`apps/comun/modelos_base/modelos.py`). Si declara `class Meta`, hereda `ModeloDeConjunto.Meta` y repite `*ModeloDeConjunto.Meta.constraints` |
| FK entre tablas de conjunto = FK compuesta | En la migración, después del `CreateModel`: `fk_compuesta("<tabla>", "<columna>_id", "<tabla_referida>")` de `apps/comun/aislamiento/migraciones.py`. Nombre de la restricción ≤ 63 caracteres |
| Ninguna vista acepta el conjunto | Toda vista con datos de un conjunto hereda `VistaDeConjunto`. El conjunto activo sale de `request.auth.conjunto_activo_id` |
| Todo permiso se exige | `exigir_permiso(request, "permiso.x", ...)` de `apps/permisos/views.py` (403). Todo permiso que uses **ya existe** en el catálogo |
| Otro conjunto = 404, nunca 403 | Busca a través del manager (ya filtra por conjunto) y responde `NotFound()` sin detalle |
| Sin borrado físico | Sin `DELETE` en la API, FK con `PROTECT`, bajas por `activo=False` o por `vigencia_hasta` |
| Toda ruta nueva de la API se registra en la prueba del intruso | `tests/aislamiento/test_intruso.py`: `DETALLES` (GET por id → 404), `LISTADOS` (GET → 200 sin el id ajeno) o `ACCIONES` (POST con `conjunto` en el cuerpo → 400 y el otro conjunto intacto). Si no, falla `test_toda_ruta_de_la_api_esta_cubierta` |
| Índices encabezados por `conjunto` | `models.Index(fields=["conjunto", ...], name="...")` |
| `update()` y `bulk_create()` se saltan `save()` | Si los usas, fija el conjunto a mano, como `apps/notificaciones/canal.py` |
| Front: nunca manda el conjunto, ningún hex, todo autoalojado | Guía §4.3. Cada pantalla real sobreescribe `{% block estado_vista %}{% endblock %}`; si no, sale la pastilla "Maqueta con datos de ejemplo" |

### 0.4 Comandos de verificación

```bash
cd "/c/Users/Alejandro/Documents/A D M I N D/Backend/Admind_Backend"
./.venv/Scripts/python.exe -m pytest -q
./.venv/Scripts/python.exe manage.py makemigrations --check --dry-run
```
```bash
cd "/c/Users/Alejandro/Documents/A D M I N D/Frontend/Admind_Front-End"
./.venv/Scripts/python.exe -m pytest -q
```

- **Crear migraciones:** `./.venv/Scripts/python.exe manage.py makemigrations <app>`. Revisa el archivo y agrega a mano las `fk_compuesta(...)` al final de `operations`.
- **Aplicar en `admind_db`:** solo si D11 lo autoriza.

---

## 1. Punto de partida (verificado el 2026-09-25)

| Pieza | Estado |
|---|---|
| Backend `desarrollo` | `3c70e3a`, limpio, 171 pruebas pasan, `makemigrations --check` sin cambios, todo migrado en `admind_db` |
| Frontend `desarrollo` | `b42ce93`, limpio, 51 pruebas pasan |
| Ya existe y se reutiliza | `Unidad`, `VinculoUnidad`, `destinatarios(unidad, Hecho)` (`apps/unidades/`); canal `notificar(Aviso, persona_ids)` (`apps/notificaciones/canal.py`); `Asignacion` con `vigentes()` y `permisos_efectivos()` (`apps/permisos/`); `registrar_usuario()` (`apps/cuentas/servicios.py`); `requisitos_para_operar()` (`apps/conjuntos/servicios.py`); comando `crear_usuarios_prueba` |
| No existe | `apps/auditoria`, `apps/areas`, `apps/reglas`, `apps/reservas` (solo README), `apps/comun/bloqueo` (solo README), `static/js/vendor/alpine*.js`, `{% block scripts %}` en `templates/base/base.html` |
| Maquetas del front que se reemplazan | `apps/unidades/templates/unidades/lista.html`, `apps/reglas/views.py` (`REGLAS_DE_EJEMPLO`), `apps/reservas/` (calendario sin franjas) |

**Fase 0, antes de empezar:**
1. En los dos repos: `git status` limpio, rama `desarrollo`, y `git pull --ff-only`. Si el pull falla o trae commits de Camilo que tocan lo mismo que este plan, **detente y avisa**.
2. Corre §0.4 y confirma 171 y 51 pruebas en verde.

---

## 2. Decisiones que toma Alejo (llenar antes de ejecutar)

| ID | Pregunta | Opciones | Recomendación | Bloquea | Respuesta |
|---|---|---|---|---|---|
| **D1** | ¿Cómo se forman las franjas reservables de un área? El maestro dice que la franja es `(área, fecha, hora_inicio, hora_fin)` y que el calendario no se guarda, pero no dice cómo se generan las opciones que ve el residente | **a)** Bloques fijos por área: el área guarda `hora_apertura`, `hora_cierre` y `duracion_franja_minutos`; las franjas de un día son los bloques consecutivos. **b)** Horario libre: el residente elige inicio y fin; hay que impedir traslapes con una restricción de exclusión (`btree_gist`) | **a)**: la unicidad por franja exacta es un índice único parcial simple y la concurrencia queda fácil de defender | F2, F7 | Recomendada (Alejo, 2026-09-27) |
| **D2** | ¿Qué estado toma una solicitud cuando el residente la libera a propósito, o cuando las reglas la rechazan al enviarla? Los 6 estados no lo cubren, y R9 (HU-19) necesita distinguirlo de `EXPIRADA`, porque solo el vencimiento gasta oportunidad | **a)** Estado nuevo no bloqueante `LIBERADA` con campo `motivo_liberacion ∈ {voluntaria, reglas}`. **b)** Reusar `CANCELADA` (en el maestro es "deshacer una reserva en firme") | **a)**, y corregir el §5.1 del maestro | F7, F9 | Recomendada (Alejo, 2026-09-27) |
| **D3** | "Un solo bloqueo activo" (maestro §12.7 c): ¿en todo el sistema o por conjunto? | **a)** Por conjunto: índice único parcial `(conjunto, persona)` con `estado = EN_SOLICITUD`, como exige el §5.4. **b)** Global `(persona)`: una excepción al aislamiento que no está en la lista cerrada | **a)**, y corregir la redacción del §5.1 | F7 | Recomendada (Alejo, 2026-09-27) |
| **D4** | Catálogo de reglas beta y versionado. §11.4: todavía no hay reglamento real | **Catálogo a)** el provisional del §5.10 menos dos tipos: `duración máxima` (con D1 a, cada franja ya es un bloque) y `requiere depósito o pago` (se decide al aprobar, HU-15 y HU-16, Sprint 4). Quedan: `ANTICIPACION_MINIMA`, `ANTICIPACION_MAXIMA`, `CUPO_POR_UNIDAD`, `AFORO`, `FRANJA_HORARIA`, `DIAS_NO_RESERVABLES`, `REQUIERE_PAZ_Y_SALVO`. **b)** Otro. **Versionado a)** editar = cerrar la regla (`vigencia_hasta = hoy`) y crear una nueva que apunta a la anterior; cada evaluación guarda copia de las reglas aplicadas. **b)** Editar en sitio con auditoría | Catálogo **a)** y versionado **a)**, marcados como provisionales hasta validar contra un reglamento real | F6, F9 | Recomendada (Alejo, 2026-09-27) |
| **D5** | La regla `REQUIERE_PAZ_Y_SALVO` sin módulo de pagos (HU-35 es del Sprint 7): ¿qué evalúa ahora? | **a)** Campo `en_mora` en `Unidad`, que el administrador marca a mano (alcance nuevo). **b)** Función `unidad_en_mora(unidad)` que devuelve `False` hasta HU-35; las pruebas la simulan. **c)** Sacar el tipo del catálogo hasta HU-35 | **b)**: la regla y la alfa "la mora solo aplica a áreas no esenciales" quedan probadas; en uso real nadie aparece en mora hasta HU-35 | F6, F9 | Recomendada (Alejo, 2026-09-27) |
| **D6** | Límite de búsquedas por documento (HU-07, R12, maestro §11.5) | Número de búsquedas por administrador y ventana de tiempo | **20 por hora**, contadas sobre la auditoría (sin tabla nueva); al pasarse, 429 | F5 | Recomendada (Alejo, 2026-09-27) |
| **D7** | ¿Se puede reservar en un conjunto que no está operativo? Ninguno puede quedar operativo hasta HU-33 (reglamento, Sprint 6) | **a)** Sí, por ahora; se revisa al llegar HU-33. **b)** No: nada es reservable hasta el Sprint 6 | **a)**, porque si no, los Sprints 3 y 4 no se pueden demostrar | F7 | Recomendada (Alejo, 2026-09-27) |
| **D8** | Auditoría de solo inserción | **a)** Ahora: tabla `auditoria_registro` que hereda `ModeloDeConjunto` y se niega en código a actualizar o borrar. Queda para después quitarle `UPDATE` y `DELETE` al usuario de base de datos, con dos usuarios de BD (§11.5). **b)** Todo ahora, incluidos los dos usuarios de BD | **a)**: es lo que piden estas HU y no toca la configuración de la base | F1 | Recomendada (Alejo, 2026-09-27) |
| **D9** | Criterios que dependen de sprints posteriores | HU-12 pide resaltar "fechas de alta demanda", pero marcar esas fechas es PB-24 (Sprint 4). **a)** Resaltar ahora solo "menos de 24 h", "límite de anticipación" y "ya tienes otra solicitud"; alta demanda llega con PB-24. **b)** Crear ya un modelo mínimo de fechas de alta demanda | **a)** | F8 | Recomendada (Alejo, 2026-09-27) |
| **D10** | HU-07: la persona encontrada no tiene cuenta (hoy no pasa, porque todo alta crea la cuenta; pasará con la importación, HU-36) | **a)** Se vincula igual y la respuesta dice `tiene_cuenta: false`; crearle cuenta a una persona existente queda fuera. **b)** Ofrecer crear la cuenta en el mismo paso | **a)** | F5 | Recomendada (Alejo, 2026-09-27) |
| **D11** | ¿Cómo trabaja el agente con Git y con la base local? | **Commits: a)** un commit local por paso con sentido, formato `tipo(app): descripción [HU-XX]`, sin push. **b)** Sin commits: Alejo revisa y commitea. **Migrate: a)** aplicar las migraciones nuevas en `admind_db` al cerrar cada fase. **b)** No aplicar; se listan al final | Commits **a)**, migrate **a)** | Todas | Recomendada (Alejo, 2026-09-27) |
| **D12** | Alpine.js no está en `static/js/vendor/` (solo el README) y hace falta para la cuenta regresiva y el panel de confirmación | **a)** Autoalojar la última versión 3.x estable (`alpinejs/dist/cdn.min.js` de npm) en `static/js/vendor/alpine.min.js`. El agente lo descarga cuando Alejo lo confirme en el chat, o lo copia Alejo. **b)** JavaScript sin Alpine | **a)**: es el stack elegido el 2026-09-13 | F7, F8 | Recomendada (Alejo, 2026-09-27) |

---

## 3. Decisiones menores que el plan ya fija

Alejo puede cambiarlas antes de ejecutar; el agente las sigue tal cual y las menciona en su informe.

| ID | Decisión | Por qué |
|---|---|---|
| **P1** | El `Area` real redeclara su FK: `conjunto = models.ForeignKey("conjuntos.Conjunto", on_delete=models.PROTECT, related_name="areas")` | La app de pruebas `tests/aislamiento` ya tiene un modelo `Area`, y los dos chocarían en `Conjunto.area_set` (error `fields.E304`). Así no se toca `ModeloDeConjunto` ni la app de pruebas |
| **P2** | `UsuarioResumenSerializer` gana dos campos: `persona` (UUID de la Persona) y `asignaciones` (`[{id, rol, nombre, desde}]` vigentes en el conjunto activo). `roles` sigue igual | HU-06 y HU-08 necesitan la Persona y cada asignación. El cambio solo agrega campos y no rompe el front |
| **P3** | Solo se registra un vínculo de unidad para una persona que ya tiene una asignación vigente en el conjunto activo; si no, 400 "Primero vincula a la persona al conjunto" | Así no se pueden sondear personas de otros conjuntos por UUID; el camino para traerla es HU-07 |
| **P4** | La búsqueda por documento va por `POST`, nunca en la URL. El front pasa el documento buscado al formulario de alta a través de la sesión, no de la query string | Maestro §5.2: el documento no viaja en URLs ni en logs |
| **P5** | Retirar un rol o cerrar un vínculo = `vigencia_hasta = hoy` por defecto | Mismo criterio que `Asignacion.objects.vigentes()`: `vigencia_hasta` es el primer día sin el rol |
| **P6** | Códigos: **409** para conflictos de estado (rol ya asignado, último administrador, franja ocupada, ya tienes un bloqueo, bloqueo vencido, vínculo ya cerrado); **429** para el límite de búsquedas; **400 con `motivos`** cuando la solicitud incumple reglas | Guía §3.5. Precedente: activar un conjunto responde 400 con `faltantes` |
| **P7** | El panel de confirmación es un fragmento de plantilla, `templates/componentes/confirmacion_de_contenido.html`, armado **solo con clases que ya existen** (`am-tarjeta`, `am-btn`, `am-pastilla`), sin tokens ni estilos visuales nuevos | El maestro §5.1 pide "un componente, tres usos"; la Guía §4.3 cierra el inventario visual. Esto no es un componente visual nuevo, es reutilizar marcado |
| **P8** | Tomar el bloqueo ya exige que la persona tenga al menos una unidad con vínculo vigente y `reside = true` (la misma regla alfa de HU-13) | Si no, alguien que no reside podría bloquear franjas 3 minutos sin derecho a reservarlas |
| **P9** | Con D5 b: `apps/reglas/mora.py` con `unidad_en_mora(unidad) -> False` y un comentario que remite a HU-35 | Se reemplaza sin tocar el evaluador |
| **P10** | La evaluación se guarda en la solicitud: `evaluacion` (JSON, copia de cada regla evaluada con id, tipo, parámetros, resultado y motivo) y `evaluada_en`. Además, un registro en la auditoría | Responde "qué reglas se evaluaron y con qué resultado" (HU-13) y deja la copia de versión de D4 |
| **P11** | `DURACION_BLOQUEO = timedelta(minutes=3)` es una constante de `apps/reservas/servicios.py` | Maestro §5.1: constante del sistema, no regla beta |
| **P12** | `cliente_api/http.py` agrega a `MENSAJES_POR_ESTADO` el 409 (usa el `detail` de la API) y el 429 ("Hiciste demasiadas búsquedas. Espera un rato e intenta de nuevo.") | Hoy el 409 solo lee `detail` si el cuerpo trae campos; el 429 no existe |
| **P13** | `templates/base/base.html` gana `{% block scripts %}{% endblock %}` antes de `</body>`; Alpine se carga solo en las pantallas que lo usan, con `defer` | Nada de JavaScript en las pantallas que no lo necesitan |
| **P14** | `GET /reservas/solicitudes/` lista solo las solicitudes propias. La bandeja del administrador es HU-14 | Es el mínimo de HU-11 y HU-13 |
| **P15** | `registrar()` de la auditoría recibe `via_superusuario` como parámetro (por defecto `False`); no lo calcula | `apps/README.md`: `auditoria` no importa ninguna app de negocio. En estas HU ningún actor es Superusuario |

---

## 4. Orden y dependencias

```
F0 Preparación ─► F1 Auditoría ─┬─► F2 HU-09 Áreas ─┬─► F6 HU-10 Reglas ─┐
                                │                   └─► F7 HU-11 Bloqueo ├─► F8 HU-12 ─► F9 HU-13 ─► F10 Cierre
                                ├─► F3 HU-08 Unidades y vínculos ────────┘
                                ├─► F4 HU-06 Roles ─► F5 HU-07 Buscar y vincular
```

- F3 va antes que F7: la toma del bloqueo exige residir en una unidad (P8).
- F4 va antes que F5: vincular crea una asignación y reutiliza la validación de roles.
- Si una decisión de la §2 está vacía, sáltate las fases que bloquea y sigue con las que no dependan de ella.

---

## F1 · Auditoría mínima (transversal)

**Objetivo:** un registro de solo inserción que usan HU-06, HU-07, HU-08, HU-10 y HU-13. **Decisión:** D8.

**Backend**
- `apps/auditoria/` con `__init__.py`, `apps.py` (`name = "apps.auditoria"`), `models.py`, `servicios.py`, `tests.py` y `migrations/`. Agregar `"apps.auditoria"` a `INSTALLED_APPS`.
- Modelo `Registro(ModeloDeConjunto)`:
  - `actor`: FK `personas.Persona`, `PROTECT`, `related_name="registros_de_auditoria"`;
  - `accion`: `CharField(60)`, por ejemplo `"rol.asignar"`;
  - `entidad`: `CharField(60)`, por ejemplo `"Asignacion"`;
  - `entidad_id`: `UUIDField(null=True)`;
  - `antes`, `despues`, `detalle`: `JSONField(null=True, encoder=DjangoJSONEncoder)`;
  - `via_superusuario`: `BooleanField(default=False)`;
  - `creado_en`: `DateTimeField(auto_now_add=True)`.
  - Índices: `["conjunto", "-creado_en"]` y `["conjunto", "actor", "accion", "creado_en"]`.
- Solo inserción, en código:
  - `save()` lanza `RegistroInmutable` si la fila ya existe (`not self._state.adding`);
  - `delete()` lanza lo mismo;
  - un `RegistroQuerySet` cuyos `update()` y `delete()` lanzan;
  - manager: `ManagerDeConjunto.from_queryset(RegistroQuerySet)()`.
- `servicios.py`:
  - `registrar(actor, accion, entidad, entidad_id=None, *, antes=None, despues=None, detalle=None, via_superusuario=False)`: crea la fila en el conjunto activo;
  - `contar(actor, accion, desde)`: la usa el límite de HU-07.
- **No importa ninguna app de negocio** (P15).

**Pruebas** (`apps/auditoria/tests.py`)
- Registrar crea la fila en el conjunto activo.
- Modificar una fila guardada lanza el error; borrarla también; `update()` y `delete()` sobre el queryset también.
- Desde otro conjunto no se ve el registro.
- `test_tablas_globales` sigue en verde sin tocar sus listas: la tabla tiene `conjunto_id` NOT NULL.

**Hecho cuando:** §0.4 en verde. **Commit:** `feat(auditoria): registro de solo inserción`. Sin HU propia: se cita en el cuerpo del commit que la piden HU-06, 07, 08, 10 y 13.

---

## F2 · HU-09 — Catálogo de áreas comunes (4 SP)

**Depende de:** F1. **Decisiones:** D1. **Permisos:** `area.ver` (Residente, Administración) y `area.gestionar` (Administración).

**Backend: `apps/areas/`** (nueva; agregar a `INSTALLED_APPS` y montar `path("areas/", include("apps.areas.urls"))` en `config/urls.py`)
- `models.py`:
  - `Clasificacion(TextChoices)`: `COMUN = "comun"`, `COMUN_ESENCIAL = "comun_esencial"`, `COMUN_USO_EXCLUSIVO = "comun_uso_exclusivo"`. Los nombres para la pantalla, en español.
  - `Area(ModeloDeConjunto)` con la FK de P1 y estos campos:
    - `nombre` (80), `descripcion` (texto, opcional);
    - `clasificacion` (obligatoria, sin valor por defecto);
    - con D1 a: `hora_apertura` y `hora_cierre` (`TimeField`) y `duracion_franja_minutos` (`PositiveSmallIntegerField`);
    - `en_mantenimiento` (bool, `False`), `activo` (bool, `True`), `creado_en`.
  - Propiedad `es_esencial` = `clasificacion == COMUN_ESENCIAL`. Es el flag derivado: no se guarda.
  - Restricciones (repitiendo las de `ModeloDeConjunto.Meta`):
    - nombre único por conjunto;
    - `CHECK` de clasificación válida;
    - `CHECK hora_cierre > hora_apertura`;
    - `CHECK duracion_franja_minutos > 0`.
- `servicios.py`:
  - `areas_visibles(persona, conjunto_id)`: con `area.gestionar`, todas; si no, solo las activas;
  - `crear(actor, **datos)`, `editar(actor, area, **datos)`, `poner_en_mantenimiento(actor, area, bool)`, `desactivar(actor, area)`. Desactivar deja `activo = False` y nunca borra;
  - `franjas_del_dia(area, fecha)` → lista de `(hora_inicio, hora_fin)`: bloques consecutivos desde la apertura mientras el bloque termine antes o justo al cierre. La consume F7;
  - toda escritura llama a `auditoria.registrar(...)` con `antes` y `despues` de los campos cambiados.
- `serializers.py`, `views.py`, `urls.py`:
  - `GET /areas/` y `POST /areas/`, `name="areas"`: listar con `area.ver` o `area.gestionar`; crear con `area.gestionar`;
  - `GET` y `PATCH /areas/<uuid:area_id>/`, `name="area-detalle"`: el `PATCH` edita nombre, descripción, horario y mantenimiento con `area.gestionar`;
  - `POST /areas/<uuid:area_id>/desactivar/`, `name="area-desactivar"`.
  - La clasificación es `ChoiceField` obligatorio: sin ella, 400.
- `apps/conjuntos/servicios.py` → `requisitos_para_operar`: el requisito `"areas"` pasa a `disponible=True`, y se cumple si hay al menos un área activa. Ajusta las pruebas de HU-03 que asumían `disponible=False` **sin cambiar su intención**: el conjunto sigue sin poder quedar operativo mientras falten reglamento y reglas.
- `tests/aislamiento/test_intruso.py`: registrar `"areas"` en `LISTADOS`, `"area-detalle"` en `DETALLES` y `"area-desactivar"` en `ACCIONES`.

**Frontend**
- `apps/areas/` (hoy solo README): `__init__.py`, `apps.py`, `urls.py` (`app_name = "areas"`), `views.py`, `forms.py` y las plantillas `templates/areas/lista.html`, `nueva.html` y `editar.html`. Agregar `"apps.areas"` a `INSTALLED_APPS` y `path("areas/", include("apps.areas.urls"))` a `config/urls.py`.
- `cliente_api/areas.py`: `listar`, `crear`, `obtener`, `editar`, `desactivar`, con docstrings como los de `cliente_api/anuncios.py`.
- **Lista:** tabla con nombre, clasificación, "Esencial" como pastilla, horario, estado ("En mantenimiento", "Inactiva") y acciones solo si hay `area.gestionar`. Si no hay áreas, estado vacío que invita a crear la primera.
- **Formulario:** la clasificación es radio o select sin opción por defecto, con una línea de ayuda por opción.
- **Lateral:** ítem "Áreas comunes" visible con `area.gestionar`.
- **Asistente de HU-03:**
  - paso nuevo `asistente/areas/` (`name="asistente-areas"`) con la lista y el alta del conjunto activo;
  - `_pasos.html` pasa a 5 pasos: 1 Datos básicos, 2 Administración, 3 Áreas, 4 Reglas, 5 Resumen;
  - el paso 4 queda como enlace deshabilitado hasta F6;
  - `administracion` redirige a `asistente-areas`.
- **Pruebas** (`tests/test_areas.py`, API simulada con `mock.patch`): sin `area.gestionar` no se ven acciones; la clasificación es obligatoria en el formulario; el 400 de la API cae en su campo; la pantalla no dice "Maqueta".

**Criterio → prueba (backend, `apps/areas/tests.py`)**

| Criterio | Prueba |
|---|---|
| Al crear un área hay que elegir la clasificación de la lista cerrada | `POST` sin clasificación → 400; con un valor fuera de la lista → 400 |
| Un área común esencial tiene `es_esencial` verdadero | Propiedad verdadera solo para `comun_esencial` |
| Un área en mantenimiento no admite solicitudes | Aquí: `franjas_del_dia` sigue funcionando, pero el área queda marcada. **La prueba del criterio va en F7**: tomar un bloqueo sobre un área en mantenimiento → 409 |
| Sin `area.gestionar`, editar → 403 | Residente: `POST` y `PATCH` → 403; `GET` → 200 solo con activas |
| Un área retirada se desactiva, no se borra | `desactivar` → la fila sigue con `activo=False`; no existe `DELETE` (405) |
| Regla alfa de mora sobre áreas esenciales | Se prueba en F9 (D5) |

**Commits:** modelo y migración → servicio y API → pantalla y asistente, cada uno con `[HU-09]`.

---

## F3 · HU-08 — Vínculos de unidad y enrutamiento (7 SP)

**Depende de:** F1. **Permiso:** `vinculo.gestionar` (Administración). Ya existen el modelo, `destinatarios()` y sus pruebas: no los rehagas.

**Backend: `apps/unidades/`**
- `servicios.py`, además de lo que ya tiene:
  - `crear_unidad(actor, nombre)`. Nombre único por conjunto; si se repite, 400.
  - `detalle_de_unidad(unidad)` → vínculos vigentes y vínculos históricos (cerrados o futuros), con persona, tipo, reside y fechas.
  - `registrar_vinculo(actor, unidad, persona_id, tipo, reside, vigencia_desde=hoy)`:
    - aplica P3 (la persona debe tener asignación vigente en el conjunto);
    - si ya hay uno vigente igual, `VinculoDuplicado` → 409.
  - `cerrar_vinculo(actor, vinculo, vigencia_hasta=hoy)`:
    - si ya está cerrado, `VinculoYaCerrado` → 409;
    - si `vigencia_hasta < vigencia_desde`, 400.
  - Cada escritura se registra en la auditoría.
  - Agregar `unidades_para_solicitar(persona)` → unidades con vínculo vigente y `reside=True`. La consumen F7 y F9.
- Vistas y URLs:
  - `GET /unidades/` existe; se le agrega `POST` (crear, con `vinculo.gestionar`);
  - `GET /unidades/<uuid:unidad_id>/`, `name="unidad-detalle"`;
  - `POST /unidades/<uuid:unidad_id>/vinculos/`, `name="unidad-vinculos"`;
  - `POST /unidades/<uuid:unidad_id>/vinculos/<uuid:vinculo_id>/cerrar/`, `name="vinculo-cerrar"`.
- `apps/cuentas/serializers.py`: aplicar P2, con `persona` y `asignaciones`.
- Intruso: `"unidad-detalle"` en `DETALLES`; `"unidad-vinculos"` y `"vinculo-cerrar"` en `ACCIONES`.

**Frontend: `apps/unidades/`** (reemplaza la maqueta)
- `cliente_api/unidades.py`: agregar `crear`, `obtener`, `registrar_vinculo` y `cerrar_vinculo`.
- **Lista:** tabla de unidades con cuántos vínculos vigentes tiene cada una, y formulario "Registrar apartamento" (con `vinculo.gestionar`). Estado vacío con esa acción.
- **Detalle de unidad:**
  - tabla "Vigentes": persona, Propietario o Arrendatario, "Vive aquí" o "No vive aquí", desde;
  - tabla "Históricos": lo mismo más la fecha "hasta";
  - formulario "Agregar vínculo": select de personas del conjunto, de `GET /auth/usuarios/` usando `persona` (P2); tipo; casilla "Vive en la unidad";
  - botón "Cerrar vínculo" por fila, con fecha que por defecto es hoy.
- Pruebas del front: la lista y el detalle se pintan con la API simulada; el 409 de un vínculo duplicado se muestra; sin `vinculo.gestionar` no se ven formularios.

**Criterio → prueba (backend)**

| Criterio | Prueba |
|---|---|
| Propietario y arrendatario vigentes coexisten | Por la API: registrar los dos sobre la misma unidad → ambos en "vigentes" |
| Al cerrar el vínculo del arrendatario, el histórico se conserva | Cerrar → sale de vigentes, aparece en históricos, la fila existe; no existe `DELETE` |
| Convocatoria a asamblea → al propietario aunque no resida | **Ya existe** (`test_cada_hecho_llega_a_quien_corresponde_segun_el_vinculo`). No duplicar; citarla en el informe |
| Infracción → propietario y arrendatario | Ídem |
| Propietario no residente con rol Residente no puede reservar | **Se prueba en F7 y F9** (P8 y regla alfa de residencia) |
| Extra del plan | Vincular a una persona sin asignación en el conjunto → 400 (P3); vínculo duplicado → 409; cerrar dos veces → 409 |

**Commits:** API y serializer → pantalla, con `[HU-08]`.

---

## F4 · HU-06 — Asignar y retirar roles (6 SP, ~65 % hecho)

**Depende de:** F1. **Permiso:** `rol.asignar` (Administración; es sensible, así que la 2FA ya la exige `DosFactoresAlDia`).

**Backend**
- `apps/permisos/servicios.py`:
  - `asignar_rol(actor, persona, rol, conjunto_id)`:
    - solo roles de `ROLES_DE_CONJUNTO`;
    - si ya lo tiene vigente, `RolYaAsignado` (409);
    - registra en la auditoría.
  - `retirar_rol(actor, asignacion, conjunto_id)`, en `transaction.atomic()`:
    - si la asignación es de Administración, bloquear con `select_for_update()` las asignaciones **vigentes de Administración del conjunto** y evaluar la lista con `list(...)`. Un `.count()` no bloquea;
    - si es la única, `UltimaAdministracion` (409): "El conjunto no puede quedar sin Administración.";
    - si no, `vigencia_hasta = hoy` (P5) y auditoría con `antes` y `despues`.
- `apps/cuentas/`, en vistas y URLs (reutiliza `usuarios_del_conjunto` para encontrar al usuario: si es de otro conjunto, 404):
  - `POST /auth/usuarios/<uuid:usuario_id>/roles/` con `{rol}`, `name="usuario-roles"`;
  - `POST /auth/usuarios/<uuid:usuario_id>/roles/<uuid:asignacion_id>/retirar/`, `name="usuario-rol-retirar"`.
  - Las dos responden el usuario actualizado (`UsuarioResumenSerializer`).
- Intruso: las dos en `ACCIONES`.

**Frontend: `apps/usuarios/`**
- `cliente_api/cuentas.py`: `asignar_rol(request, usuario_id, rol)` y `retirar_rol(request, usuario_id, asignacion_id)`.
- En el detalle del usuario, con `rol.asignar`:
  - sección "Roles en este conjunto" con cada asignación y su botón "Retirar";
  - formulario "Asignar rol" con los roles de conjunto que todavía no tiene;
  - el 409 del último administrador se muestra como alerta.
- Pruebas del front: sin `rol.asignar` no hay botones; el 409 se muestra; asignar redirige al detalle.

**Criterio → prueba**

| Criterio | Prueba |
|---|---|
| Asignar un rol → la unión de permisos de todos sus roles | Por la API: residente + asignar Consejo → `permisos_efectivos` incluye los de ambos |
| No existe crear ni editar roles | Recorrer las rutas: ninguna crea o edita roles; `POST` con `rol` fuera del catálogo → 400; `"superusuario"` → 400 |
| Un rol del conjunto A no da permisos en B | Ya existe (`test_rol_de_un_conjunto_no_da_permisos_en_otro`); citarla |
| El rol de plataforma no incluye `reserva.aprobar`, `anuncio.publicar` ni `infraccion.registrar` | Ya existe (`test_rol_de_plataforma_no_opera_dentro_de_un_conjunto`); citarla |
| Retirar el rol al último de Administración falla | `retirar` sobre la única → 409 y la asignación sigue vigente; con dos, la primera se retira |
| Auditoría de asignaciones | Asignar y retirar dejan `Registro` con acción, actor, `antes` y `despues` |
| Extra | Retirar quita los permisos de inmediato; asignar un rol ya vigente → 409 |

**Commits:** servicio y API → pantalla, con `[HU-06]`.

---

## F5 · HU-07 — Buscar por documento y vincular (3 SP)

**Depende de:** F1 y F4. **Decisiones:** D6 y D10. **Permisos:** `persona.buscar` y `persona.vincular` (los dos sensibles).

**Backend: `apps/personas/`** (agregar `servicios.py`, `serializers.py` y `urls.py`; montar `path("personas/", include("apps.personas.urls"))`)
- `buscar(actor, tipo_documento, numero_documento)`:
  1. Si `auditoria.contar(actor, "persona.buscar", ahora − 1 h) >= 20` (D6), lanza `LimiteDeBusquedas`, que la vista responde con 429.
  2. Normaliza con `normalizar_documento` y busca **coincidencia exacta** de tipo y número; nunca búsqueda parcial.
  3. Registra en la auditoría: `accion="persona.buscar"`, `detalle={"tipo_documento": ..., "numero_documento": ...}`, `entidad_id` = la persona si se encontró.
  4. Devuelve la persona o `None`.
- Respuesta mínima:
  - `{encontrada: true, persona: {id, nombre, tiene_cuenta, roles_en_el_conjunto: [...]}}`;
  - o `{encontrada: false}`.
  - Sin teléfono, sin correo, **sin datos de otros conjuntos**.
- `vincular(actor, persona_id, rol)`: reutiliza `asignar_rol` de F4 (409 si ya tiene ese rol vigente) y responde `tiene_cuenta` (D10 a).
- Rutas, las dos por `POST` (P4):
  - `POST /personas/buscar/`, `name="persona-buscar"`, con `persona.buscar`;
  - `POST /personas/vincular/`, `name="persona-vincular"`, con `persona.vincular`.
  - Intruso: las dos en `ACCIONES`. En `intacto`, que no se creó ninguna asignación ni ningún registro en el otro conjunto.

**Frontend: `apps/usuarios/`**
- `cliente_api/personas.py`: `buscar` y `vincular`. `cliente_api/http.py`: P12.
- Pantalla nueva `usuarios/registrar/` (`name="registrar"`): el botón "Registrar persona" de la lista lleva aquí.
  - **Paso 1:** tipo y número de documento.
  - **Si la encuentra:** tarjeta con el nombre, "Ya tiene cuenta" o "Sin cuenta", los roles que ya tiene aquí, un select de rol y el botón "Vincular al conjunto".
  - **Si no la encuentra:** guarda el documento en `request.session["documento_buscado"]` (P4) y redirige a `usuarios:nuevo`, que lo precarga y lo borra de la sesión.
  - El 429 se muestra como alerta.
- Pruebas del front: encontrada → se ofrece vincular; no encontrada → redirige y el formulario trae el documento; **el documento nunca aparece en una URL** (revisar `Location` y los enlaces).

**Criterio → prueba**

| Criterio | Prueba |
|---|---|
| Documento existente → se vincula sin crear un registro nuevo | Buscar y vincular → el número de `Persona` no cambia y la asignación existe en el conjunto activo |
| Documento inexistente → se ofrece crear | `buscar` → `encontrada: false`. La parte de "ofrecer" se prueba en el front |
| Cada búsqueda queda en la auditoría con quién y qué documento | Un `Registro` por búsqueda, encontrada o no, con el documento en `detalle` |
| Pasar el límite → se rechaza | Con 20 registros en la última hora → 429; uno de hace 2 h no cuenta |
| Vinculada a dos conjuntos, sus roles del otro no dan permisos | Persona con rol en Mirador, vinculada como Residente en Torres → en Torres solo tiene los permisos de Residente |
| Extra | Con puntos y espacios encuentra igual (normalización); un número parcial no encuentra nada; la respuesta no trae teléfono ni correo |

**Commits:** API → pantalla, con `[HU-07]`.

---

## F6 · HU-10 — Reglas beta de reserva (9 SP)

**Depende de:** F1 y F2. **Decisiones:** D4 y D5. **Permisos:** `regla.ver` y `regla.configurar` (Administración).

**Backend: `apps/reglas/`** (nueva; `INSTALLED_APPS` y `path("reglas/", include("apps.reglas.urls"))`)
- `catalogo.py`: `TipoDeRegla(TextChoices)` con los tipos de D4, y para cada tipo su validador de parámetros y su descripción en palabras. Solo tipos que restringen: **no existe ningún tipo que permita algo**.

  | Tipo | Parámetros | Se rechaza si |
  |---|---|---|
  | `ANTICIPACION_MINIMA` | `{"horas": int}` | `horas < 0` (relajaría "no reservar en el pasado") |
  | `ANTICIPACION_MAXIMA` | `{"dias": int}` | `dias < 1` |
  | `CUPO_POR_UNIDAD` | `{"reservas": int, "dias": int}` | alguno `< 1` |
  | `AFORO` | `{"maximo": int}` | `< 1` |
  | `FRANJA_HORARIA` | `{"dias_semana": [0..6], "desde": "HH:MM", "hasta": "HH:MM"}` | lista vacía, día fuera de 0–6, o `desde >= hasta` |
  | `DIAS_NO_RESERVABLES` | `{"dias_semana": [...], "fechas": ["AAAA-MM-DD"]}` | las dos vacías |
  | `REQUIERE_PAZ_Y_SALVO` | `{}` | el área es esencial: la alfa dice que la mora solo aplica a áreas no esenciales |

  Parámetros de más o de tipo equivocado → 400. Tipo fuera del catálogo → 400.
- `models.py` → `Regla(ModeloDeConjunto)`:
  - `area`: FK con `fk_compuesta` en la migración, obligatoria;
  - `tipo`, `parametros` (JSON);
  - `vigencia_desde` (fecha, por defecto hoy) y `vigencia_hasta` (nula);
  - `reemplaza`: FK a sí misma, nula, `PROTECT`, también con `fk_compuesta`;
  - `creada_por` (FK `Persona`, `PROTECT`) y `creada_en`.
  - `CHECK` de tipo válido y `CHECK` de vigencia coherente.
  - `QuerySet.vigentes(fecha)`, mismo criterio que `Asignacion`.
- `servicios.py`:
  - `crear(actor, area_id, tipo, parametros, vigencia_desde)`;
  - `editar(actor, regla, parametros)`, con D4 versionado a: cierra la regla con `vigencia_hasta = hoy` y crea la nueva con `reemplaza = regla` y `creada_por = actor`, en una transacción;
  - `retirar(actor, regla)`, que cierra la vigencia.
  - Todo se registra en la auditoría.
  - `reglas_vigentes(area, fecha)`, que la consume F9.
- Rutas:
  - `GET` y `POST /reglas/`, `name="reglas"`;
  - `GET` y `PATCH /reglas/<uuid:regla_id>/`, `name="regla-detalle"` (el `PATCH` es editar = versión nueva);
  - `POST /reglas/<uuid:regla_id>/retirar/`, `name="regla-retirar"`.
  - La respuesta de cada regla incluye `descripcion`, por ejemplo "Máximo 25 asistentes", `area`, vigencias, `creada_por` y `creada_en`.
- `requisitos_para_operar`: `"reglas_beta"` pasa a `disponible=True` y se cumple con al menos una regla vigente en el conjunto. Ajusta las pruebas de HU-03 como en F2.
- Intruso: `"reglas"` en `LISTADOS`, `"regla-detalle"` en `DETALLES`, `"regla-retirar"` en `ACCIONES`.

**Frontend: `apps/reglas/`** (reemplaza la maqueta: borra `REGLAS_DE_EJEMPLO`)
- `cliente_api/reglas.py`.
- **Lista de reglas vigentes** agrupadas por área, con descripción, "desde", autor y acciones "Editar" y "Retirar" si hay `regla.configurar`.
- **Alta en dos pasos, sin JavaScript:**
  1. `reglas/nueva/` → elegir área y tipo;
  2. `reglas/nueva/<tipo>/` → un `Form` de Django por tipo, en un diccionario `FORMULARIO_POR_TIPO`.
- **Editar** reutiliza el formulario del tipo y avisa: "Al guardar se crea una versión nueva; la anterior queda en el historial."
- **Asistente:** paso 4 `asistente/reglas/` con la misma alta; se habilita en `_pasos.html`.
- Pruebas del front: cada tipo muestra sus campos; el 400 de la API cae en el campo; sin `regla.configurar` no hay acciones; ya no aparece "Maqueta".

**Criterio → prueba**

| Criterio | Prueba |
|---|---|
| Sin reglas, el conjunto no puede quedar operativo | `requisitos_para_operar` → `reglas_beta` no cumplido; con una regla vigente, cumplido |
| Una regla exige tipo, parámetros, área y vigencia | Falta cualquiera → 400 |
| Una regla permisiva se rechaza | `ANTICIPACION_MINIMA` con `horas=-1` → 400; tipo `"PERMITIR_X"` → 400 |
| Una regla beta no relaja una alfa | `REQUIERE_PAZ_Y_SALVO` sobre un área `comun_esencial` → 400 |
| Se aplican en AND sin precedencias | **Se prueba en F9** (dos reglas incumplidas → dos motivos) |
| Una regla editada deja autor y fecha | `PATCH` → la anterior cerrada, la nueva con `reemplaza`, `creada_por` y `creada_en`, y un `Registro` en la auditoría |

**Commits:** catálogo, modelo y migración → servicio y API → pantalla y paso del asistente, con `[HU-10]`.

---

## F7 · HU-11 — Bloqueo exclusivo de 3 minutos (7 SP)

**Depende de:** F2 y F3. **Decisiones:** D1, D2, D3, D7 y D12. **Permisos:**
- `reserva.solicitar` (Residente) para tomar el bloqueo;
- para ver franjas, `reserva.solicitar` o `reserva.ver_todas`.

**Backend: `apps/comun/bloqueo/`** (el mecanismo compartido R1; **no importa apps de negocio**)
- `bloqueo.py`:
  - `class RecursoOcupado(Exception)`;
  - `tomar(crear)`: corre `crear()` dentro de `transaction.atomic()` y convierte el `IntegrityError` del índice único parcial en `RecursoOcupado`;
  - `expirar_vencidos(queryset, *, campo_vence, estado_activo, estado_expirado, ahora)`: un solo `UPDATE ... WHERE estado = activo AND vence <= ahora`. Es idempotente y no usa ningún proceso en segundo plano.
- Actualiza su README con lo que quedó.

**Backend: `apps/reservas/`** (nueva; `INSTALLED_APPS` y `path("reservas/", include("apps.reservas.urls"))`)
- `models.py`:
  - `EstadoSolicitud`: `EN_SOLICITUD`, `APARTADA`, `RESERVADA`, `RECHAZADA`, `CANCELADA`, `EXPIRADA` y, con D2 a, `LIBERADA`.
  - `BLOQUEANTES = {EN_SOLICITUD, APARTADA, RESERVADA}`.
  - `Solicitud(ModeloDeConjunto)`:
    - `area`, con `fk_compuesta`;
    - `unidad`, nula mientras está `EN_SOLICITUD`, con `fk_compuesta`;
    - `persona` (FK `Persona`, `PROTECT`);
    - `fecha`, `hora_inicio`, `hora_fin`, `estado`;
    - `bloqueo_vence_en`, `motivo_liberacion` (vacío o `voluntaria` / `reglas`);
    - `motivo` (200), `asistentes` (nulo), `observaciones`;
    - `evaluacion` (JSON, nulo) y `evaluada_en` (P10);
    - `creada_en` y `enviada_en`.
  - Restricciones:
    - `UniqueConstraint(fields=["conjunto", "area", "fecha", "hora_inicio"], condition=Q(estado__in=BLOQUEANTES), name="solicitud_franja_bloqueante_unica")`;
    - con D3 a: `UniqueConstraint(fields=["conjunto", "persona"], condition=Q(estado=EstadoSolicitud.EN_SOLICITUD), name="solicitud_un_bloqueo_por_persona")`;
    - `CHECK hora_fin > hora_inicio`;
    - `CHECK` de estado válido;
    - `CHECK` de que un estado de `APARTADA` en adelante lleva unidad.
  - Índices: `["conjunto", "area", "fecha"]` y `["conjunto", "estado", "bloqueo_vence_en"]`.
- `servicios.py` (P11):
  - `expirar_vencidas(ahora)` usa `expirar_vencidos` sobre `Solicitud.objects` (ya filtrado por conjunto). **Se llama al principio de cada consulta y cada acción** de este módulo.
  - `franjas(persona, area, fecha)`:
    - un área de otro conjunto o inexistente → `NotFound` en la vista;
    - arma las franjas con `areas.servicios.franjas_del_dia`;
    - marca cada una: `libre`, `en_solicitud`, `apartada`, `reservada`, `pasada` o `propia`;
    - un área en mantenimiento o inactiva devuelve todas `no_disponible`.
    - **Nunca expone quién tiene una franja.**
  - `tomar_bloqueo(persona, area, fecha, hora_inicio)`, en este orden:
    1. `expirar_vencidas`;
    2. P8: sin unidades para solicitar → `SinUnidadParaSolicitar` (400);
    3. área inactiva o en mantenimiento → `AreaNoDisponible` (409);
    4. franja que no existe en `franjas_del_dia` o que ya pasó → 400;
    5. crea la solicitud `EN_SOLICITUD` con `bloqueo_vence_en = now + 3 min` dentro de `bloqueo.tomar`;
    6. `RecursoOcupado` se traduce según el índice que falló: la franja → `FranjaOcupada` (409, "Otra persona está tramitando esta franja en este momento."); la persona → `YaTienesUnBloqueo` (409, con el id de su solicitud en curso).
  - `liberar(persona, solicitud)`:
    - solo la dueña y solo en `EN_SOLICITUD`; si no, 409;
    - pasa a `LIBERADA` con `motivo_liberacion="voluntaria"`;
    - liberar dos veces responde 409 sin cambiar nada.
  - `solicitudes_de(persona)` (P14) y `detalle(persona, solicitud_id)` (solo las propias; si no, 404).
  - El detalle incluye `segundos_restantes`, calculados en el servidor, y `unidades_para_solicitar`.
- Rutas:
  - `GET /reservas/franjas/?area=<uuid>&fecha=AAAA-MM-DD`, `name="franjas"`;
  - `GET` y `POST /reservas/solicitudes/`, `name="solicitudes"`: el `GET` lista las propias; el `POST` toma el bloqueo con `{area, fecha, hora_inicio}` y responde 201 con el detalle;
  - `GET /reservas/solicitudes/<uuid:solicitud_id>/`, `name="solicitud-detalle"`;
  - `POST /reservas/solicitudes/<uuid:solicitud_id>/liberar/`, `name="solicitud-liberar"`.
- Intruso:
  - `"franjas"` en `DETALLES`: la función devuelve la URL con `?area=<id de un área del otro conjunto>&fecha=...` → 404;
  - `"solicitudes"` en `LISTADOS`;
  - `"solicitud-detalle"` en `DETALLES`;
  - `"solicitud-liberar"` en `ACCIONES`.
- **D7 a:** no se revisa `conjunto.operativo`. Deja un comentario en el servicio que remite a D7.

**Pruebas de concurrencia: `tests/concurrencia/test_bloqueo_de_franjas.py`** (y `__init__.py` si hace falta)
- `@pytest.mark.django_db(transaction=True)`.
- 10 hilos con `threading.Barrier(10)`: cada uno con su residente (vínculo `reside=True`) llama a `tomar_bloqueo` sobre la misma franja.
- Cada hilo hace `with usar_conjunto(...)` **dentro** del hilo: el `ContextVar` no se hereda. Y cierra su conexión (`connection.close()`) al terminar.
- Asserts: exactamente 1 éxito y 9 `FranjaOcupada`; una sola solicitud bloqueante en la base.
- Un bloqueo vencido no bloquea: se fuerza `bloqueo_vence_en` al pasado con `update()` → otra persona toma la franja; la primera queda `EXPIRADA`.
- Uno liberado no expira dos veces: liberar y luego `expirar_vencidas` dos veces → sigue `LIBERADA`.
- "La apertura de la ventana con N residentes en el mismo segundo no duplica": es el primer caso; cítalo así en el docstring.

**Frontend: `apps/reservas/`**
- **D12:** con Alpine en `static/js/vendor/alpine.min.js`, agregar su versión al README de `vendor/` y P13 en `base.html`.
- `cliente_api/reservas.py`: `franjas`, `tomar`, `obtener`, `liberar` y `mis_solicitudes`.
- **Calendario:**
  - arriba, un selector de área (`GET ?area=`), con las áreas de `cliente_api.areas.listar`;
  - al elegir un día, la lista de franjas de ese día con su estado como **pastilla con texto** ("Libre", "En trámite", "Apartada", "Reservada", "Ya pasó", "Tuya");
  - en cada franja libre, un formulario `POST` "Reservar" hacia `reservas/tomar/`, solo con `reserva.solicitar`;
  - un 409 se muestra como alerta sobre la lista.
- **`reservas/solicitudes/<id>/`:**
  - con `EN_SOLICITUD`, el formulario (que termina en F9);
  - con cualquier otro estado, un mensaje y un enlace al calendario.
- **Cuenta regresiva:** `x-data` que arranca de `segundos_restantes`, se muestra en cifras tabulares (`am-num`) y al llegar a 0 muestra "Se venció el tiempo. La franja quedó libre." y deshabilita el envío.
- **Liberación:**
  - el botón "Cancelar" es un `POST` a `reservas/solicitudes/<id>/liberar/` (vista del front → API);
  - en `pagehide`, `navigator.sendBeacon` a esa misma ruta con `FormData` que lleva `csrfmiddlewaretoken`;
  - no se envía si el formulario se está enviando (bandera `enviando`).
- Pruebas del front: las franjas muestran su estado en texto; el 409 se muestra; la pantalla de solicitud trae `segundos_restantes` y el botón "Cancelar"; la vista de liberar llama a la API.

**Criterio → prueba**

| Criterio | Prueba |
|---|---|
| Franja libre + Reservar → `EN_SOLICITUD` y reloj de 3 minutos | `POST /reservas/solicitudes/` → 201, estado `EN_SOLICITUD`, `bloqueo_vence_en ≈ now + 3 min` |
| Otra persona sobre una franja `EN_SOLICITUD` → aviso inmediato | Segundo residente → 409 con el mensaje; y la prueba de concurrencia |
| Bloqueo vencido + acceso → `EXPIRADA` en ese momento y franja libre | Forzar el vencimiento, pedir las franjas → la solicitud queda `EXPIRADA` y la franja `libre` |
| Residente con un bloqueo activo no toma otro en ninguna área | Segundo `POST` sobre otra área → 409 |
| Al cerrar el formulario, el bloqueo se libera sin esperar | `liberar` → `LIBERADA` y la franja libre. En el front, la vista de liberar; el `sendBeacon` va al guion manual |
| HU-09: área en mantenimiento no admite solicitudes | Tomar sobre un área en mantenimiento → 409 |
| HU-08: propietario no residente no puede reservar | Solo con vínculo `reside=False` → 400 `SinUnidadParaSolicitar` |

**Commits:** `comun/bloqueo` → modelo y migración → servicio y API → concurrencia → pantalla, con `[HU-11]`.

---

## F8 · HU-12 — Confirmación del contenido (2 SP)

**Depende de:** F7. **Decisiones:** D9 y D12. **Casi todo es front.**

**Backend** (pequeño, en `apps/reservas/servicios.py`): el detalle de una solicitud `EN_SOLICITUD` agrega `avisos`, una lista de textos que resaltan sin bloquear (D9 a):
- `"menos_de_24h"`: la franja empieza en menos de 24 horas;
- `"limite_de_anticipacion"`: hay una regla `ANTICIPACION_MAXIMA` vigente y la fecha cae en el último día permitido;
- `"otra_solicitud"`: la persona ya tiene otra solicitud `APARTADA` o `RESERVADA` desde hoy en adelante.

Pruebas de los tres.

**Frontend**
- `templates/componentes/confirmacion_de_contenido.html` (P7). Recibe `area`, `fecha` y `horario` ya formateados en el servidor, y los campos que llena la persona se enlazan con Alpine (`x-text`).
- El texto sigue al maestro §5.1: "Vas a solicitar el **Salón comunal** para el **sábado 26 de diciembre de 2026**, de **2:00 p. m. a 6:00 p. m.**, para **40** asistentes."
- **La fecha se formatea en el servidor** con `{{ fecha|date:"l j \d\e F \d\e Y" }}` (`LANGUAGE_CODE = "es-co"` ya da "sábado"). El día de la semana en letras es el punto entero de la HU.
- **Flujo, en el mismo `x-data` que la cuenta regresiva:**
  - "Revisar solicitud" muestra el panel y oculta el formulario, **sin ninguna petición**;
  - "Corregir" vuelve con los datos intactos: el formulario se oculta con `x-show`, no se destruye;
  - "Enviar solicitud" hace el `POST` real, que termina en F9;
  - el reloj no se detiene ni se extiende.
- Los `avisos` se muestran dentro del panel como pastillas de advertencia **con texto**. No deshabilitan el envío.
- El fragmento queda listo para reutilizarse en citas (HU-31) y alternativas (HU-32); aquí solo lo usa la reserva.
- Pruebas del front (`tests/test_reservas.py`):
  - con la API simulada, el HTML trae "sábado 26 de diciembre de 2026", los botones "Corregir" y "Enviar solicitud" y el texto de cada aviso;
  - no hay ninguna ruta del front para "revisar" (el panel no pide nada al servidor).
  - Lo que depende del navegador (Corregir conserva lo escrito, el reloj sigue) va al guion manual (§6).

**Criterio → prueba**

| Criterio | Prueba |
|---|---|
| Ve el área, el día de la semana en letras, la fecha y el horario | Prueba del HTML |
| Corregir vuelve sin perder lo escrito | Guion manual (JavaScript) |
| Una fecha atípica se resalta sin impedir el envío | Prueba de `avisos` en el backend y del HTML en el front. "Alta demanda" queda para PB-24 (D9) |
| El panel abierto no detiene ni extiende el reloj | Guion manual; en el código, el reloj vive en el mismo `x-data` y no se reinicia |
| Un envío que salta la interfaz se evalúa igual | **Se prueba en F9** (`POST` directo a la API) |

**Commit:** `feat(reservas): confirmación del contenido antes de enviar [HU-12]`.

---

## F9 · HU-13 — Envío de la solicitud y motor de reglas (8 SP)

**Depende de:** F6, F7 y F8. **Decisiones:** D2, D4 y D5.

**Backend: `apps/reglas/`**
- `alfa.py`: reglas en código, siempre activas. Cada una devuelve `Resultado(clave, descripcion, cumple, motivo)`:
  - `RESIDE`: la persona tiene un vínculo vigente con `reside=True` sobre la unidad elegida;
  - `NO_EN_EL_PASADO`: la franja empieza después de ahora, en hora de `America/Bogota`;
  - `AREA_DISPONIBLE`: el área está activa y no está en mantenimiento.
  - "La mora solo aplica a áreas no esenciales" vive dentro de `REQUIERE_PAZ_Y_SALVO` y en la validación de F6.
  - Las alfas de piscina y cobro quedan fuera: no hay datos para evaluarlas. Anótalo en el informe.
- `evaluador.py` → `evaluar(solicitud) -> list[Resultado]`:
  - recorre **todas** las alfas y **todas** las beta vigentes del área, en AND, sin detenerse en la primera falla;
  - hay un evaluador por tipo de D4;
  - `CUPO_POR_UNIDAD` cuenta las solicitudes `APARTADA` y `RESERVADA` de la misma unidad y la misma área cuya fecha cae en los `dias` días anteriores a la franja, incluida esta;
  - `REQUIERE_PAZ_Y_SALVO` usa `mora.unidad_en_mora` (P9) y no aplica si el área es esencial.
- Mensajes en la voz del §6.5, por ejemplo: "Este salón admite máximo 25 asistentes y la solicitud dice 40."

**Backend: `apps/reservas/servicios.py`** → `enviar(persona, solicitud, *, unidad_id, motivo, asistentes, observaciones)`, en `transaction.atomic()` con `select_for_update()` sobre la solicitud:
1. `expirar_vencidas`. Si es de otra persona → 404. Si no está `EN_SOLICITUD` → 409. Si ya venció → queda `EXPIRADA` y 409 "Se venció el tiempo".
2. Guarda unidad, motivo, asistentes y observaciones.
3. `evaluar()` → guarda `evaluacion` y `evaluada_en` (P10).
4. **Si todo cumple:**
   - la solicitud pasa a `APARTADA` con `enviada_en`;
   - `notificar(Aviso("Nueva solicitud de reserva", "<área> el <día en letras>…", origen="reserva", referencia=solicitud.id), <personas con Administración vigente>)`;
   - auditoría `reserva.enviar`.
5. **Si algo falla:**
   - la solicitud pasa a `LIBERADA` con `motivo_liberacion="reglas"` (D2 a), porque el bloqueo se libera;
   - auditoría;
   - lanza `IncumpleReglas(motivos)`, que la vista responde con **400** `{"detail": "La solicitud no cumple las reglas del conjunto.", "motivos": [...]}` (P6).
   - Ojo: el cambio de estado debe **persistir** aunque se lance la excepción. Lanza después del `atomic` o devuelve un resultado; no dejes que el rollback deshaga la liberación.
- Ruta: `POST /reservas/solicitudes/<uuid:solicitud_id>/enviar/`, `name="solicitud-enviar"` → `ACCIONES` en el intruso.
- Serializer de envío: `unidad` (UUID), `motivo` (texto obligatorio, 200), `asistentes` (entero ≥ 1), `observaciones` (opcional, 1000).

**Frontend**
- Formulario de la solicitud:
  - campos unidad (de `unidades_para_solicitar`; si hay una sola, fija), motivo, asistentes y observaciones;
  - si la persona no tiene unidades para solicitar, lo dice y no muestra el formulario.
- El botón "Enviar solicitud" del panel (F8) hace el `POST` a `reservas/solicitudes/<id>/enviar/` → API.
  - **Éxito:** pantalla "Tu solicitud quedó apartada. La administración la revisará y te avisará."
  - **400 con `motivos`:** lista **completa** de motivos, "La franja quedó libre" y enlace al calendario.
  - **409:** su mensaje.

**Criterio → prueba** (`apps/reservas/tests.py` y `apps/reglas/tests.py`)

| Criterio | Prueba |
|---|---|
| Una solicitud válida pasa a `APARTADA` y se avisa a la Administración | `enviar` → `APARTADA`; `Notificacion` para cada persona con Administración vigente y para nadie más |
| Si incumple tres reglas, ve los tres motivos y se libera el bloqueo | Con tres reglas incumplidas (aforo, anticipación mínima, día no reservable) → 400 con 3 motivos; la solicitud queda `LIBERADA` y la franja libre. Esto también prueba el AND de HU-10 |
| Sin vínculo vigente con `reside`, la alfa lo impide | Unidad elegida donde la persona no reside → motivo de `RESIDE`. También cierra el criterio 5 de HU-08 |
| Una unidad en mora no puede pedir un área no esencial | `monkeypatch` de `unidad_en_mora → True`: área no esencial → rechazada; área esencial → no aplica (cierra el criterio de mora de HU-09) |
| Queda registrado qué reglas se evaluaron y con qué resultado | `evaluacion` trae cada regla con su id, tipo, parámetros y resultado; hay `Registro` en la auditoría |
| HU-12: un envío que salta la interfaz se evalúa igual | `POST` directo a la API con 40 asistentes y `AFORO` 25 → 400 |
| Pruebas por cada tipo de regla | Una prueba que cumple y una que no por cada tipo de D4 (parametrizadas) |
| Extra | Enviar vencida → `EXPIRADA` y 409; enviar la de otra persona → 404; enviar dos veces → 409 |

**Commits:** alfa y evaluador → envío y API → pantalla, con `[HU-13]`.

---

## F10 · Cierre del agente

1. §0.4 en verde en los dos repos y `makemigrations --check` sin cambios.
2. `git status` sin `.env` ni `.venv`.
3. Actualizar `Documentacion/Admind_Documentacion/Avance/Admind_Avance.md` **según su propia §7**: qué existe, avance por HU y decisiones tomadas al construir (las de la §2 con su respuesta y las P1–P15). **No crear** un "Documento Avance" nuevo ni tocar los informes.
4. Notion solo si Alejo lo pide en el chat. Si lo pide:
   - casillas de tareas de cada HU;
   - estado "En revisión" para las que cumplen sus criterios en código, **nunca "Finalizado"**: eso lo da la DoD humana (§5);
   - restaurar en HU-06 las tareas 4 y 5 del Excel.
5. Entregar el informe de la §7.

---

## 5. Lo que el agente no puede hacer (DoD humana)

| Paso | Quién |
|---|---|
| Volver a crear la rama `pruebas` en el backend de GitHub | Alejo |
| PR `desarrollo → pruebas` por repositorio, revisado por el integrante que no programó | Alejo y Camilo |
| Prueba manual de cada HU por quien no la programó (guiones en la §6) | Camilo o Alejo |
| Actualizar el maestro con D1, D2, D3 y D4 (§5.1 estados, §5.10 catálogo, §12.7 c) | Alejo, o el agente si se le pide aparte |
| Pasar cada HU a "Finalizado" en Notion | Alejo |

---

## 6. Guiones de prueba manual

**Preparación:**
1. Levantar la API (`python manage.py runserver 8000`) y el front (`python manage.py runserver 8001`).
2. En la API, `python manage.py crear_usuarios_prueba`: crea "Conjunto de prueba" y un usuario por rol.

| HU | Pasos | Esperado |
|---|---|---|
| HU-09 | Como `administracion@example.com`: Áreas comunes → crear "Salón comunal" sin clasificación; luego con "Común"; poner en mantenimiento; desactivar | El primer intento pide la clasificación; el área aparece con su estado; desactivada, sigue en la lista como "Inactiva" |
| HU-08 | Apartamentos → registrar "Torre 1 – 101" → agregar a Residente como propietario que vive ahí → agregar a Consejo como arrendatario → cerrar el vínculo del arrendatario | Los dos coexisten; al cerrar, el arrendatario pasa a "Históricos" |
| HU-06 | Usuarios → Consejo → asignar "Residente" → retirar "Residente" → intentar retirar "Administración" a `administracion@` | Aparece y desaparece; el último administrador no se puede retirar, con un mensaje claro |
| HU-07 | Usuarios → Registrar persona → documento de Vigilancia (CC 9000000005) con puntos → Vincular como Residente. Luego un documento inexistente. Luego 21 búsquedas | Se encuentra y se vincula sin duplicar; el inexistente lleva al alta con el documento cargado y **sin el documento en la barra de direcciones**; la búsqueda 21 se rechaza |
| HU-10 | Reglas → nueva → Aforo 25 en "Salón comunal"; editarla a 30; intentar "Requiere paz y salvo" sobre un área esencial | La edición deja una versión nueva; la de paz y salvo se rechaza con su motivo |
| HU-11 | Como `residente@` (con vínculo que reside, de HU-08): Zonas comunes → Salón → un día → Reservar. En otra ventana, con otro residente, reservar la misma franja. Esperar 3 minutos sin enviar. Repetir y cerrar la pestaña | Cuenta regresiva visible; el segundo ve "Otra persona está tramitando esta franja"; al vencer queda libre; al cerrar la pestaña, libre de inmediato |
| HU-12 | Llenar el formulario → Revisar solicitud → Corregir → cambiar asistentes → Revisar → mirar el reloj | El panel dice el día de la semana en letras; Corregir conserva lo escrito; el reloj no se reinició |
| HU-13 | Enviar con 40 asistentes y aforo 25 en un día no reservable. Luego enviar una válida y entrar como `administracion@` | Se ven todos los motivos y la franja queda libre; la válida queda "Apartada" y la administración tiene la notificación |

---

## 7. Informe final que entrega el agente

1. **Fases hechas y no hechas**, y por qué (decisión vacía, bloqueo, choque con el código).
2. **Por HU:** tabla de criterio → prueba → pasa o no, y las tareas técnicas cubiertas.
3. **Archivos tocados por repo**, con una línea de qué hace cada uno.
4. **Commits creados** (hash y mensaje) y migraciones nuevas (aplicadas o no, según D11).
5. **Números:** pruebas antes y después en los dos repos.
6. **Adaptaciones:** dónde el código real obligó a desviarse del plan.
7. **Cosas vistas fuera del plan**, sin hacerlas.
8. **Preguntas que podría hacer el jurado** sobre lo construido, como mínimo:
   - por qué un índice único parcial y no un `SELECT` antes del `INSERT`;
   - por qué la expiración se evalúa al siguiente acceso;
   - por qué el evaluador no se detiene en la primera falla;
   - por qué una regla editada se versiona;
   - por qué la búsqueda por documento va por `POST` y queda en la auditoría.

---

## 8. Fuera de este plan

Se listan para que nadie las construya "de paso":

- **HU-03:** criterio de auditoría de quién creó el conjunto. Es del Sprint 1; se puede pedir aparte ahora que existe la auditoría.
- **HU-14 a HU-19:** aprobar o rechazar, condiciones del alquiler, pago, cancelación de reservas en firme, campana y dos oportunidades (R9). `LIBERADA` frente a `EXPIRADA` deja lista la base de R9.
- **PB-24:** fechas de alta demanda.
- **HU-33:** reglamento. El requisito sigue `disponible=False` y ningún conjunto queda operativo.
- **HU-35:** pagos y mora real, que reemplaza el `unidad_en_mora` provisional.
- **Base de datos:** quitarle `UPDATE` y `DELETE` sobre la auditoría al usuario de aplicación, con dos usuarios de BD.
- **Alfas de piscina y cobro.**
- **Actualizar el maestro, Notion y la rama `pruebas`** (§5).
