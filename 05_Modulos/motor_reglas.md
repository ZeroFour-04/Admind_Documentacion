---
resumen: "Motor de reglas: reglas del sistema, alfa (del conjunto) y beta (de la zona), con parámetros y descripciones. Definición del 2026-10-06: lo de las áreas con reserva ya está en el código (sin commit ni `migrate` al 2026-10-06); lo del ingreso, sin construir."
tipo: modulo
modulo: reglas
hu: [HU-10, HU-13]
origen: "definición con Alejo en chat (2026-10-06) + maestro v1.4 (2026-09-14) §5.10 + guía de estructura §5.6 (2026-09-30)"
actualizado: 2026-10-06
---

# Motor de reglas

> [!IMPORTANT] Redefinido el 2026-10-06; construido ese día para las áreas con reserva
> - Lo vigente es la sección *Definición vigente*. La decidió Alejo en chat; falta contárselo a Camilo.
> - **Alfa y beta cambiaron de significado.** Antes: alfa = fija en el código, beta = configurable. Ahora: alfa = regla del conjunto, beta = regla de la zona, y las fijas se llaman reglas del sistema.
> - **Construido** con [Plan_Motor_De_Reglas](../07_Planes/activos/Plan_Motor_De_Reglas.md): niveles, una sola regla por tipo, descripciones fijas, aforo obligatorio en el área, días que no abre con motivo y el tablero. Al 2026-10-06 está **sin commit** y las migraciones **sin aplicar en `admind_db`**: las corre Alejo, y cierran las reglas que había.
> - **Sin construir:** todo lo del ingreso (modo de uso, permanencia máxima, acompañantes, un ingreso abierto por persona), que no tiene plan, y *día límite de pago*, que llega con pagos.
> - El texto del maestro §5.10 queda al final, como antecedente.

## Definición vigente (2026-10-06)

Una **zona** es un área común del catálogo (`Area` en el código). Las zonas de paso libre, como parques o zonas verdes, no entran al sistema.

### Tres niveles

| Nivel | Quién la fija | Dónde vale |
|---|---|---|
| **Sistema** | El código. Nadie la configura ni la apaga | Toda la plataforma |
| **Alfa** | Administración, una vez por conjunto | Todas las zonas del conjunto |
| **Beta** | Administración, una vez por zona | Esa zona |

- Cada regla vive en **un solo nivel** y existe **una sola vez** por conjunto o por zona. Así no hay choque entre niveles ni dos reglas del mismo tipo que se anulen.
- Se conserva lo anterior: todas restringen, se evalúan en Y, y la respuesta trae **todos** los motivos.
- Cada regla lleva un nombre, una **descripción fija** con ejemplo, que escribe el sistema y se muestra junto al campo, y la frase con sus valores («Máximo 25 asistentes»).

### Modo de uso de una zona

| Modo | Ejemplos | Cómo funciona |
|---|---|---|
| **Con reserva** | Salón, BBQ, jacuzzi | Se aparta una franja con anticipación: [reservas](reservas.md) |
| **Con ingreso** | Gimnasio, piscina | No se aparta: vigilancia registra a quien entra y no se pasa del aforo: [ingresos](ingresos.md) |

### Reglas del sistema

1. **Residencia.** Solo reserva o ingresa quien reside en el conjunto. En una reserva, además, reside en la vivienda a cuyo nombre pide.
2. **Zona disponible.** Está activa y no está en mantenimiento.
3. **Dentro del horario.** La franja o el ingreso caen en el horario de la zona y en un día que abre.
4. **No en el pasado.** La franja que se reserva todavía no ha empezado.
5. **Un ingreso abierto por persona** en el conjunto *(supuesto)*.

### Reglas alfa (del conjunto)

| Regla | Parámetros | Aplica a | Descripción para el administrador |
|---|---|---|---|
| **Anticipación mínima** | Horas, entero desde 0 (0 = sin mínimo) | Reserva, igual para todas las zonas | Cuántas horas antes, como mínimo, se pide una reserva. Con 24, nadie reserva para hoy mismo. Con 0 no hay mínimo |
| **Anticipación máxima** | Días, entero desde 1 | Reserva, igual para todas las zonas | Hasta cuántos días hacia adelante se puede reservar. Con 30, hoy se puede pedir cualquier fecha de los próximos 30 días y ninguna posterior |
| **Paz y salvo** | Sí o no | Reserva e ingreso, con un solo interruptor *(supuesto)* | Si la activas, una vivienda en mora con la administración no reserva ni ingresa a las zonas comunes hasta ponerse al día |
| **Acompañantes** | ¿Se permiten? Sí o no. Si es sí: máximo por vivienda a la vez, entero desde 1 | Ingreso | Si los residentes pueden entrar con invitados a las zonas con ingreso, y cuántos puede tener adentro una misma vivienda a la vez. Cada acompañante ocupa un puesto del aforo |
| **Día límite de pago** | Día del mes, de 1 a 28 *(supuesto: el tope)* | No la evalúa el motor: la lee pagos | El día del mes hasta el que se paga la administración sin entrar en mora. Con 10, quien no tenga el pago confirmado el 11 queda en mora |

### Reglas beta (de la zona)

| Regla | Parámetros | Aplica a | Descripción para el administrador |
|---|---|---|---|
| **Modo de uso** | Reserva o ingreso. Se elige al crear la zona y no cambia *(supuesto)* | — | Cómo se usa la zona. Con reserva, se aparta una franja con anticipación (salón, BBQ). Con ingreso, no se aparta: vigilancia registra a quien entra (gimnasio, piscina) |
| **Horario** | Hora de apertura y hora de cierre; el cierre va después de la apertura | Los dos modos | Desde qué hora y hasta qué hora presta servicio. Fuera de ese horario no se reserva ni se registra ingreso |
| **Días que no abre** | Lista de renglones, cada uno con motivo obligatorio | Los dos modos | Días de la semana, fechas o periodos en que la zona no presta servicio. Cada uno lleva su motivo, que es lo que lee el residente |
| **Aforo máximo** | Personas, entero desde 1. Obligatorio | Los dos modos | Cuántas personas caben. Con reserva, es el máximo de asistentes de cada reserva. Con ingreso, es el máximo de personas adentro al mismo tiempo |
| **Duración de la franja** | Minutos; hoy el mínimo es 120 | Reserva | Cuánto dura cada franja que se puede reservar. Con 180 minutos y horario de 8:00 a 20:00, la zona ofrece cuatro al día |
| **Permanencia máxima** | Minutos *(supuesto: la unidad)* | Ingreso | Cuánto tiempo puede quedarse una persona desde que entra. Al cumplirse, el sistema registra su salida y avisa al residente y a vigilancia |
| **Límite de reservas por vivienda** | Máximo de reservas y cada cuántos días | Reserva | Cuántas reservas de esta zona puede tener una misma vivienda en un periodo. Con 2 cada 30 días, una vivienda no aparta el salón todos los fines de semana |

**Días que no abre.** Un renglón es de una de tres clases, todas con motivo: día de la semana («lunes — limpieza»), fecha suelta («25 de diciembre — Navidad») o periodo con desde y hasta, sin tope de duración («1 al 30 de noviembre — cambio del piso»). *En mantenimiento* sigue aparte: es el cierre inmediato y sin fecha que ya tiene el área. Agregar un cierre no cancela las reservas ya aprobadas de esos días; qué hace el sistema con ellas está sin decidir ([abiertas](../06_Decisiones/abiertas.md) 12.10). Se descartó una regla alfa que solo encendiera esta beta: dejar la lista vacía ya significa que abre todos los días.

**Acompañantes.** Se cumple si los acompañantes de esa vivienda que ya están adentro, más los que entran, no pasan del máximo. Solo se guarda cuántos son. No aplica a las reservas: ahí los invitados ya son los asistentes.

**La mora.** El motor solo le pregunta al módulo de pagos si la vivienda está en mora; el punto de conexión ya existe (`apps/reglas/mora.py`) y hoy responde siempre que no. La única fuente, por ahora, es el pago de la administración. Las sanciones no lo son: el sistema no impone sanciones ni guarda multas ([legal](../01_Contexto/legal.md) §4.2). Hasta que pagos exista (HU-16, HU-35), *paz y salvo* y *día límite de pago* quedan definidas pero sin efecto.

### Supuestos del agente, por confirmar

Alejo no los ha objetado ni confirmado:

- Un solo interruptor de paz y salvo para reservas e ingresos.
- El modo de uso no cambia después de crear la zona: para cambiarlo, se desactiva y se crea otra.
- La permanencia máxima va en minutos; la salida prevista no pasa de la hora de cierre; si se cambia la permanencia, los ingresos abiertos conservan la que tenían.
- El día límite de pago llega hasta 28, para que exista en todos los meses.
- Un ingreso abierto por persona en el conjunto.

Lo que sigue sin decidir está en [abiertas](../06_Decisiones/abiertas.md) 12.10.

## Cómo está construido (verificado el 2026-10-06, sin commit)

El código tiene el modelo por niveles para las áreas con reserva, con pruebas (HU-09, HU-10 y HU-13).

Cuando un residente envía una solicitud, `reglas/evaluador.py` → `evaluar(solicitud)` revisa **todas** las reglas y devuelve un resultado por cada una (no se detiene en la primera que falla, para poder decirle a la persona **todos** los motivos). El orden es: reglas del sistema, aforo del área, reglas del conjunto y reglas del área. Cada resultado dice su `nivel`: `sistema`, `alfa` o `beta`.

- **Reglas del sistema** (`sistema.py`, antes `alfa.py`): están en el código, siempre activas, nadie las apaga. Son tres: quien solicita reside en la unidad, la franja no está en el pasado, y el área está activa y sin mantenimiento. «Dentro del horario» no está ahí: lo garantiza tomar el bloqueo, que rechaza una franja fuera del horario.
- **El aforo** es un campo obligatorio del área, `Area.aforo_maximo` (de 1 a 10 000). Se evalúa siempre, como resultado de nivel `beta` y sin id de regla.
- **Reglas alfa y beta** (`catalogo.py` + modelo `Regla`): las define Administración. Una regla **sin área** es del conjunto (alfa); **con área**, de esa área (beta). El nivel no lo escoge quien la crea: lo dice `NIVEL_POR_TIPO`.

  | Tipo | Nivel | Parámetros |
  |---|---|---|
  | `ANTICIPACION_MINIMA` | alfa | `horas`, desde 0 |
  | `ANTICIPACION_MAXIMA` | alfa | `dias`, desde 1 |
  | `REQUIERE_PAZ_Y_SALVO` | alfa | ninguno: definirla es activarla. Lleva la nota «todavía no restringe» |
  | `DIAS_QUE_NO_ABRE` | beta | `renglones`: cada uno es `{dia_semana, motivo}` o `{desde, hasta, motivo}`. Hasta 60, motivo de hasta 120 caracteres, un día de la semana no se repite |
  | `CUPO_POR_UNIDAD` | beta | `reservas` y `dias`, desde 1 |

- **Una sola abierta por tipo.** Una regla *abierta* es la que tiene `vigencia_hasta` vacía. Definir una segunda del mismo tipo (en el conjunto, o en la misma área) responde `409`. El servicio lo revisa y la base lo impide con dos índices únicos parciales; un `CHECK` impide además una regla abierta en el nivel equivocado ([restricciones_bd](../02_Arquitectura/restricciones_bd.md)).
- **Tipos retirados:** `AFORO`, `FRANJA_HORARIA` y `DIAS_NO_RESERVABLES` siguen en `TipoDeRegla` para poder leer el historial. No se crean ni se editan, y el evaluador no los mira.
- Siguen **versionadas**: cambiar una la cierra y crea otra que la reemplaza. Agregar o quitar un día que no abre también es una versión nueva, con la lista completa; quitar el último retira la regla.
- **Descripción fija:** el nombre, la descripción y la nota de cada tipo viven en `catalogo.py` y llegan al front por `GET /reglas/catalogo/`. El front no los repite.
- Todas **restringen**, ninguna permite, así que se combinan con **Y** sin conflictos.
- El resultado se **copia** en `Solicitud.evaluacion` (JSON), para que la explicación siga siendo cierta aunque la regla cambie mañana.
- **Un cierre sobre reservas ya apartadas** no las toca: las reglas se evalúan al pedir. Cada regla de días que no abre responde `reservas_afectadas`, cuántas solicitudes apartadas o reservadas, de hoy en adelante, caen en sus renglones, y el tablero lo avisa con enlace a las solicitudes del área.
- El horario (`hora_apertura`, `hora_cierre`) y `duracion_franja_minutos` no son reglas: son campos de `Area`.
- **La pantalla** (`/reglas/` en el front) es un tablero: arriba las reglas del conjunto y debajo un bloque por área, con una fila por cada regla posible, su descripción y lo que vale hoy o «Sin definir». El paso de reglas del asistente es el mismo tablero.
- El requisito `reglas_beta` para quedar operativo no cambió: se cumple con al menos una regla vigente, de cualquier nivel ([abiertas](../06_Decisiones/abiertas.md) 12.10 e).

**Las migraciones** son `areas/0004_aforo_maximo` (las áreas que existían reciben aforo 1) y `reglas/0002` a `0004`. La `0003` es de datos: cierra **todas** las reglas abiertas del modelo anterior, sin borrarlas, y pasa a cada área el aforo de su regla `AFORO` (el menor si había varias). Las reglas se vuelven a definir en el tablero.

### Qué cambió al construir la definición

Construido el 2026-10-06, salvo lo que la última fila marca como pendiente.

| Antes | Con la definición |
|---|---|
| `alfa.py` = reglas fijas | Pasan a llamarse reglas del sistema |
| Anticipación mínima y máxima, y paz y salvo: una regla por área | Una sola por conjunto. Hoy una regla no puede existir sin área |
| Aforo: regla opcional | Dato obligatorio de la zona |
| `FRANJA_HORARIA` | Sale: el horario ya es campo del área y los días los cubre *días que no abre* |
| `DIAS_NO_RESERVABLES`: días de la semana y fechas, sin motivo | Gana el motivo obligatorio y los periodos |
| `CUPO_POR_UNIDAD` | Se conserva por zona, como *límite de reservas por vivienda* |
| Varias reglas del mismo tipo por área | Una sola por tipo |
| — | Construidas las descripciones fijas. **Sin construir:** acompañantes y día límite de pago (llegan con el ingreso y con pagos), modo de uso y permanencia máxima (son del ingreso) |

El versionado y la copia de la evaluación en la solicitud no se discutieron: siguen como están.

## Diseño anterior (maestro §5.10)

> [!WARNING] Decisiones posteriores al texto del maestro (2026-09-27)
> - Catálogo beta vigente: **7 tipos** que solo restringen (anticipación mínima, anticipación máxima, cupo por apartamento, aforo, franja horaria, días no reservables y paz y salvo), sin duración máxima ni depósito (D4 a). Provisional hasta validarlo con un reglamento real.
> - El *punto abierto* de versionado se resolvió por reemplazo: editar una regla crea una versión nueva y la evaluación se copia en la solicitud (D4 a, P10).
> - `unidad_en_mora()` devuelve `False` hasta que exista HU-35 (D5 b).
>
> Detalle en [construccion](../06_Decisiones/construccion.md).

**Nivel 0 — Invariantes del sistema.** No son evaluables ni configurables; se garantizan estructuralmente. No hay dos solicitudes bloqueantes sobre la misma franja; no se reserva en el pasado; ninguna consulta cruza `conjunto_id`; no existen dos personas con el mismo documento.

**Nivel 1 — Reglas alfa.** El sistema jamás las ignora y el administrador no las desactiva. Semilla propuesta, **pendiente de cerrar**:

- Solo quien tenga vínculo vigente con `reside = true` puede solicitar a nombre de esa unidad
- Toda decisión queda trazada
- Una regla beta nunca puede relajar una alfa
- El cobro por un bien común solo procede si el reglamento lo autoriza
- ~~La restricción por mora solo aplica a bienes comunes **no esenciales**~~ — retirada el 2026-10-05: las áreas ya no tienen clasificación, así que no hay forma de marcar una como esencial ([construccion](../06_Decisiones/construccion.md))
- Piscina: menores de 12 años requieren acompañante adulto; salvavidas en los supuestos exigidos

**Nivel 2 — Reglas beta.** Configuradas por el administrador al crear el conjunto, tomadas de su reglamento. **Catálogo de tipos parametrizados, no DSL de texto libre** — un DSL es un proyecto de semestre por sí solo.

Cada regla = tipo + parámetros + área + vigencia + `conjunto_id`. Catálogo inicial, **pendiente de validar contra un reglamento real**: anticipación mínima/máxima · duración máxima · cupo de reservas confirmadas por unidad en ventana móvil · franja horaria permitida por área y día · aforo · requiere paz y salvo · requiere depósito o pago · días no reservables.

**Todas las reglas beta son restrictivas.** Si solo restringen, se evalúan en AND y **el conflicto no existe** — el mismo criterio que llevó a que los permisos sean puramente aditivos.

Los mensajes de rechazo reportan **todas** las reglas que fallaron, no la primera.

**Punto abierto:** vigencia y versionado. Los reglamentos se reforman en asamblea, y una reserva creada bajo la versión 1 no debe romperse cuando entra la versión 2. ¿Snapshot de la versión aplicada en cada decisión?

## Ver también

- [reservas](reservas.md) — dónde se llama al evaluador
- [ingresos](ingresos.md) — el modo de uso con ingreso
- [construccion](../06_Decisiones/construccion.md) — las decisiones del 2026-10-06
