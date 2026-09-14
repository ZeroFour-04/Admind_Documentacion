---
titulo: "AdMind — Seguimiento del lab"
proyecto: "Proyecto de Ingeniería de Software II — Universidad de Cundinamarca, Facatativá"
actualizado: 2026-09-14
proposito: "Estado vivo de la Fase 0. Lo lee un agente nuevo para retomar el trabajo sin volver a preguntar lo ya decidido."
---

# AdMind — Seguimiento del lab

> [!IMPORTANT] Si eres un agente de IA que acaba de abrir un chat nuevo
>
> 1. Lee `Admind_Lab.md` completo y después `Admin_Master.md`. Los dos están en esta carpeta.
> 2. **Este archivo no explica el proyecto ni el método.** Solo dice dónde quedó el trabajo. Si contradice a los otros dos, mandan ellos.
> 3. **Desde el 2026-09-14 construyes lo que Alejo pida, y solo eso** (Lab §2.1). La tutoría con pistas por niveles queda para los ejercicios del lab (Lab §2.4).
> 4. Antes de terminar la sesión, actualiza este archivo. Las instrucciones están en la §7.

---

## 1. Dónde quedó el trabajo

**Corte: 2026-09-14.** Sprint 1 sin iniciar.

> [!IMPORTANT] Cambio de planes del 2026-09-14
> El plazo de entrega se redujo a **un mes** (fecha exacta por confirmar) y no hay que entregar el proyecto completo. Cambió el modo de trabajo: el agente construye lo que Alejo pide, con alcance exacto (Lab §2). **Los ejercicios del lab pasan a ser opcionales**: se hacen si hay tiempo.

**Retomar aquí:** no hay un ejercicio a medias. Lo siguiente es lo que Alejo pida construir. Recortar alcance o repartir el mes en sprints no le toca al agente: son las decisiones 8 y 9 de la §3.

### 1.1 El lab, tal como quedó (corte 2026-09-12)

Ejercicio 0.2 **cerrado completo** — los tres bloques, `pytest` en verde (8/8) y las preguntas de jurado de la §5 respondidas. El detalle está en la §4.1.

**Una cosa suelta de esa sesión:**
- **La bitácora de errores del Lab §7 ya tiene archivo (`Admind_Bitacora_Errores.md`), pero ninguna entrada**, y la sesión del 0.2 dejó material real para la primera (ver el aviso en la §4.1). La escribe Alejo, no el agente — es la prueba de autoría.

**Ya resuelto en esa sesión:** `.gitignore` creado (`.venv/`, `__pycache__/`, `*.pyc`, `.pytest_cache/`) y dos commits en `lab`, todo local, sin push:
```
928a4ea feat(lab): resolver ejercicio 0.2 - Persona, Conjunto y Asignacion en POO pura
3423040 chore(lab): agregar .gitignore para venv y cache de Python
```

**Si Alejo retoma el lab:** por el orden del Lab §10, sigue el 0.3 (SQL, FK compuesta — "el de mayor rendimiento de la ruta"). El 0.1 (conflicto de Git) se va a dar solo en el primer `pull` compartido con Camilo, no hay que forzarlo.

---

## 2. Repositorios y ramas

Tres clones hermanos bajo `C:\Users\Alejandro\Documents\A D M I N D\`. La terminal de trabajo es **Git Bash**, no PowerShell — el Lab §4 y el maestro §7.1 todavía dicen lo contrario y están desactualizados en ese punto.

| Repositorio | Carpeta local | Remoto |
| --- | --- | --- |
| Backend | `Backend/Admind_Backend` | `ZeroFour-04/Admind_Backend` |
| Frontend | `Frontend/Admind_Front-End` | `ZeroFour-04/Admind_Front-End` |
| Documentación | `Documentacion/Admind_Documentacion` | `ZeroFour-04/Admind_Documentacion` |

**Ramas creadas el 2026-09-11** en backend y frontend:

| Rama | Remoto | Nota |
| --- | --- | --- |
| `main` | sí | Lo entregado. Recibe de `pruebas` al cerrar sprint |
| `desarrollo` | sí | Integración. Los dos integrantes trabajan aquí |
| `pruebas` | sí | Lo terminado, listo para probar |
| `lab` | **no — solo local** | Práctica de Alejo. No sube mientras el profesor no confirme |

Las cuatro nacieron del mismo commit. El repositorio de documentación se quedó **solo con `main`**; no se ha decidido si el modelo de ramas también aplica ahí.

**Posición al cierre de la sesión:** backend en `lab`, frontend en `desarrollo`.

> [!WARNING] El lab vive en la rama `lab`, no en `desarrollo`
> Cada ejercicio va en su carpeta dentro de esa rama (`laboratorio/01-poo-persona/`, `laboratorio/02-sql-fk-compuesta/`, …). `desarrollo` puede bajar al lab; el lab **nunca** sube, ni por merge, ni por cherry-pick, ni copiando y pegando (Lab §3).

> [!NOTE] `.gitignore` resuelto el 2026-09-12
> El backend tenía `.venv/` escondido de `git status` por pura suerte (el propio venv trae un `.gitignore` interno que se ignora a sí mismo) y `__pycache__/` ya había aparecido sin cubrir. Se creó `.gitignore` en la raíz del backend con `.venv/`, `__pycache__/`, `*.pyc` y `.pytest_cache/`, commiteado aparte del código del ejercicio. Este archivo de seguimiento sigue sin commitear (vive en el repo de documentación, no en el de backend).

Pendiente de infraestructura: **tampoco hay `.gitattributes` en ningún repo.** Con dos personas en Windows compartiendo `desarrollo`, la diferencia CRLF/LF produce archivos marcados como modificados sin haberlos tocado y conflictos falsos. Es decisión de equipo con Camilo.

---

## 3. Decisiones pendientes que bloquean

Ninguna se resuelve por cuenta del agente. Son las del Lab §9 con su estado.

| # | Pregunta | Para quién | Estado |
| --- | --- | --- | --- |
| 1 | ¿La rama `lab` se sube al remoto? | Profesor | **Abierta.** Mientras tanto, local |
| 2 | ¿Qué significa exactamente `pruebas` para el profesor? | Profesor | Abierta |
| 3 | ¿Qué fecha arranca el Sprint 1? | Equipo | Abierta. Desde el 2026-09-14 depende de la 9 |
| 4 | ¿Se cerró el stack de frontend (§12.1 del maestro)? | Equipo | Abierta. **No bloquea la Fase 0** |
| 5 | ¿Manda `design-system/` o el §6 del maestro? | Equipo | Abierta. Por ahora, un solo acento |
| 6 | `.gitattributes` para CRLF/LF | Camilo | Abierta |
| 7 | El 2026-09-14 el profesor pidió la estructura de capas de su plantilla ASP.NET (`Controllers`, `Dtos`, `Services`, `Repositories`, `Utilities`) "o una similar". ¿Acepta nombres y ubicaciones distintos? | Profesor | **Cerrada por el profesor el 2026-09-14:** le dan igual el nombre y la ubicación mientras el flujo de la API sea el mismo. **Queda un hueco:** `apps/README.md` no declara la capa de servicios ni la regla de quién llama a quién; hoy el flujo escrito es vista → modelo. Lo corrige Alejo o se lo pide al agente |
| 8 | ¿Cuál es la fecha exacta de entrega? | Profesor | Abierta. Se sabe que es un mes desde el 2026-09-14 |
| 9 | ¿Qué se entrega en el mes y en cuántos sprints? (maestro §12.8) | Equipo | Abierta. **Bloquea planear**; no bloquea construir lo que Alejo pida |

---

## 4. Bitácora de ejercicios

Criterios de salida completos en el Lab §6. Aquí solo el estado. **Desde el 2026-09-14 los pendientes son opcionales**: se hacen si hay tiempo, y lo que no se ensaye se construye directamente en el producto.

| #   | Ejercicio                                                | Estado                                                                                                                 | Dónde vive                                          |
| --- | -------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| 0.1 | Git — provocar un conflicto y resolverlo                 | **Parcial.** Ramas creadas; el conflicto deliberado sigue sin hacerse. Se va a dar solo en el primer `pull` compartido | —                                                   |
| 0.2 | POO — `Persona`, `Conjunto`, `Asignacion` en Python puro | **Cerrado.** `pytest` en verde (8/8), preguntas de jurado respondidas — ver §4.1                                       | `laboratorio/01-poo-persona/` (rama `lab`, backend) |
| 0.3 | SQL — FK compuesta que la base rechace                   | Pendiente. Es el de mayor rendimiento de la ruta                                                                       | Postgres local                                      |
| 0.4 | HTTP — `curl`, provocar 404 y 400                        | Pendiente                                                                                                              | —                                                   |
| 0.5 | HTML y CSS — pantalla de confirmación de contenido       | Pendiente                                                                                                              | rama `lab`, frontend                                |
| —   | **Spike de concurrencia** (M3 y M4)                      | Pendiente. Es el ejercicio que importa                                                                                 | rama `lab`, backend                                 |

### 4.1 Ejercicio 0.2 — estado detallado

**Cerrado el 2026-09-12.** El enunciado completo (tres clases a la vez) lo bloqueó al principio, así que se partió en tres bloques cortos. **El orden importa: sin el bloque 1 resuelto, el plan del §2.1 no le sale.**

| Bloque | Qué es | Estado |
| --- | --- | --- |
| 1 | Normalizar el número en el intérprete, sin clases | **Cerrado** |
| 2 | Envolverlo en una función, en su propio archivo | **Cerrado** |
| 3 | Clases `Persona`, `Conjunto`, `Asignacion` en Python puro | **Cerrado** |

**Entorno ya montado:** `.venv` en la raíz del backend y `pytest` instalado.

**Lo que hay escrito:**
- `laboratorio/01-poo-persona/ej1.py` — las seis variables de prueba (`a` a `f`) y un loop que compara `cedula(i)` contra el valor esperado con `==`
- `laboratorio/01-poo-persona/ej1_aux.py` — la función `cedula(variable)`

Las tres transformaciones que pide el maestro §5.2 —sin puntos, sin espacios, sin ceros a la izquierda— **las tres resueltas**, con `variable.strip().replace(".", "").lstrip("0")`:

- **Puntos y espacios:** `.strip()` (espacios, ambos lados) + `.replace(".", "")`
- **Ceros a la izquierda:** `.lstrip("0")` — no `.strip("0")`. Alejo llegó a la diferencia después de que `strip("0")` le mordiera el cero final de `f = "1032456780"` (documento que **termina** en cero, no solo empieza)

Verificado por Alejo corriendo `ej1.py`: **las seis variables (`a`–`f`) dan `True`.**

> [!IMPORTANT] Patrón que se repitió tres veces — reconocerlo si vuelve a pasar
> Alejo aplicaba la transformación final **dentro del `print()`** (`print(x.strip())`, `print(x.strip("0"))`) sin guardarla en la variable. Al comparar la variable con `==` después, daba `False`, porque la variable nunca había cambiado. Lo resolvió encadenando **todas** las operaciones en una sola asignación. Es la misma familia del error de abajo (verificar mirando la salida en vez de comparar con `==`), en una forma más sutil.

> [!NOTE] Lo más valioso que pasó antes de esta sesión, y ya lo aplica solo
> Verificaba con `print` y la salida le mintió: los espacios de `"  1032456789  "` son invisibles en la terminal. Se le mostró `repr()` y comparar con `==` en vez de mirar la salida.

> [!WARNING] Pistas ya entregadas sobre los ceros a la izquierda — el punto ya se cerró, no repetirlas si algo parecido reaparece
> Nivel 1 (antes de esta sesión): que `strip` tiene dos hermanos en `dir(str)` y que la diferencia es de qué lado muerden, más la pregunta de qué le pasaría a `"1032456780"` si se le quitan ceros de ambos lados. Nivel 2 (esta sesión): señalar que `strip("0")` corta por los dos extremos y pedirle que corriera exactamente ese caso. **Encontró `lstrip` por su cuenta.**

**Resuelto en sesiones anteriores:**
1. ~~El archivo se llama `ej 1.py`~~ → renombrado a `ej1.py`; la función se movió a `ej1_aux.py`, importable con `from ej1_aux import cedula`

**Sigue pendiente, no adelantarlo si algún día se reabre este código:**
1. Quitar los ceros de la izquierda a un número que sea todo ceros devuelve cadena vacía. Es buen caso límite para pruebas nuevas y para pregunta de jurado; **no regalarlo antes de que las pruebas lo saquen**

#### Bloque 3 — el plan y las clases

**El plan que se cuestionó antes de escribir código** (Lab §2.1, paso 1), después de varias rondas de preguntas del agente:

- `Persona(tipo_documento, numero_documento, nombre, correo)` — normaliza `numero_documento` al construirse (reutiliza `cedula()` de `ej1_aux.py`, no la reescribe), genera `id_persona` **sola**, con `uuid.uuid4()`, sin recibirlo como parámetro, e inicia `asignaciones = []`
- `Conjunto(id_conjunto, nombre, direccion, ciudad, departamento, tipo)` — solo guarda, sin lógica
- `Asignacion(persona, conjunto, rol)` — valida `rol` contra `roles_permitidos` (atributo de **clase** en `Asignacion`, compartido por todas las instancias, no uno por objeto), guarda `persona` y `conjunto` como **objetos**, no como IDs (decisión explícita: en Python puro ya se tienen los objetos en memoria, no hay por qué buscarlos por identificador), y se registra sola en `persona.asignaciones` dentro de su propio `__init__` — para que esa relación bidireccional no dependa de que quien usa las clases se acuerde de mantenerla

**Archivos:**
- `laboratorio/01-poo-persona/entidades.py` — las tres clases
- `laboratorio/01-poo-persona/test_entidades.py` — 8 pruebas, escritas por el agente antes de que existiera una sola clase (Lab §2.3), especificación ejecutable del plan de arriba

> [!IMPORTANT] Errores reales de esta sesión — material crudo para la bitácora del Lab §7, todavía sin escribir
> - `id_persona` pasó por una versión intermedia como parámetro opcional (`id_persona=None`) en vez de generarse sola; se quedaba en `None` porque nadie se lo pasaba. Quedó resuelto, y de paso respondió por qué esa responsabilidad no puede ser de quien llama al constructor (pregunta de jurado 8)
> - `roles_permitidos` tenía `"vigilante"` mientras las pruebas y el catálogo del maestro §5.3 usan `"vigilancia"` — mismatch de nombre, no de lógica. Costó varias vueltas porque el mensaje de error (`DID NOT RAISE ValueError`, luego `ValueError` a secas) no señala qué palabra falló; hubo que leer el traceback completo para ubicar la llamada exacta
> - `asignaciones=None` seguido de `asignaciones if asignaciones is not None else []` evitó correctamente la trampa clásica de Python del argumento por defecto mutable (`def __init__(self, ..., asignaciones=[])` comparte la misma lista entre todas las instancias). No se le preguntó a Alejo por qué lo hizo así — vale la pena que la explique de todas formas si sale en la sustentación
> - Un `git status --untracked-files=all` durante la sesión confirmó que `__pycache__/` ya apareció (por correr `pytest`) y sigue sin `.gitignore` que lo cubra — ver aviso en la §2

**Pendiente, no de este ejercicio:** la bitácora de errores del Lab §7 ya tiene archivo, pero sigue sin entradas. El callout de arriba es material crudo para ella, pero **la escribe Alejo, no el agente** — es la prueba de autoría que pide el maestro §8.4, y una bitácora generada por IA no prueba nada.

**Recordatorio del Lab §3:** nada de `entidades.py` ni `test_entidades.py` sube a `desarrollo`. Cuando el Sprint 1 llegue a la historia que necesite `Persona`, se construye de nuevo en Django. Desde el 2026-09-14 no hace falta que Alejo la reescriba sin mirar: puede pedírsela al agente (Lab §3, regla 2).

---

## 5. Preguntas de jurado abiertas

Un ejercicio no se cierra sin que Alejo las responda en voz alta (Lab §2.1).

**Del 0.1 — Git:**

1. Después de `git branch desarrollo`, ¿en qué rama queda parado HEAD? ¿Por qué?
2. En `git push -u origin desarrollo pruebas`, ¿qué hace exactamente el `-u`?
3. Si las cuatro ramas apuntan al mismo commit, ¿qué **es** una rama en Git, en una frase?
4. Camilo clona el repositorio mañana. ¿Ve `lab`? ¿Por qué?
5. El commit `728dedb` del backend se llama `Elimicacion Archivos basura`. ¿Qué convención de mensajes fija el maestro §8.4, y qué costaría cambiarle el mensaje ahora que ya es la punta de cuatro ramas y está en el remoto?

**Del 0.2 — POO.** Todas respondidas el 2026-09-12. Ejercicio cerrado.

6. ¿Por qué la normalización ocurre al escribir y no al leer? — **Respondida.** Sin normalizar, el `UNIQUE (tipo_documento, numero_documento)` del maestro §5.2 trataría `"123456"` y `"0123456"` como valores distintos, y la restricción dejaría de cumplir su función.
7. ¿Por qué `print` no sirve para verificar y `==` sí? — **Respondida.** `print` deja la evaluación al ojo humano (y los espacios invisibles mienten); `==` es una comprobación que resuelve el propio intérprete, sin margen para que algo se pase por alto.
8. ¿Por qué `Persona` genera `id_persona` sola, con `uuid.uuid4()`, en vez de recibirlo como parámetro del constructor? — **Respondida.** Garantiza que toda `Persona` tenga un id sin depender de que quien la construye se acuerde de pasarlo — el mismo bug que apareció en esta sesión cuando por un momento sí fue parámetro opcional y se quedaba en `None`.
9. ¿Por qué `Asignacion` se registra sola en `persona.asignaciones` en vez de esperar que quien la usa lo haga a mano? — **Respondida.** Pone la relación bidireccional dentro del sistema, no como responsabilidad externa que alguien puede olvidar.
10. ¿Por qué `roles_permitidos` es atributo de la clase `Asignacion` y no de cada instancia? — **Respondida.** Todas las instancias comparten la misma lista; para ampliar el catálogo de roles se edita en un solo lugar, no en cada objeto por separado.

---

## 6. Entorno

Detalle completo y verificado en el Lab §4. Lo que un agente necesita saber para no dar órdenes que fallen:

- **Git Bash.** Rutas POSIX (`/c/Users/...`) y comillas obligatorias: `A D M I N D` lleva espacios
- **Python 3.14.3**, el único instalado. Django 5.2 LTS lo soporta desde el parche 5.2.8
- **PostgreSQL 18** nativo como servicio de Windows, puerto 5432. **Nunca se sustituye por SQLite**
- **Docker no instalado.** No bloquea la Fase 0

---

## 7. Cómo se actualiza este archivo

Al cerrar una sesión de trabajo, el agente actualiza **solo** lo que cambió:

1. La fecha del frontmatter y el corte de la §1, con el punto exacto donde se retoma
2. El renglón del ejercicio en la §4 y su detalle — no "terminado" si faltan las preguntas de jurado
3. **Las pistas ya entregadas**, para que el siguiente agente no repita una de nivel 1 sobre algo ya pistado y le robe el ejercicio
4. Las decisiones que se hayan cerrado en la §3, con quién las cerró
5. Las preguntas de jurado nuevas o respondidas en la §5

**Lo que no va aquí:** contenido de producto, diseño, reglas de negocio ni método de trabajo. Todo eso vive en `Admin_Master.md` y `Admind_Lab.md`, y duplicarlo crea una segunda fuente de verdad que nadie va a actualizar (maestro §8.2).
