---
resumen: "Contradicciones abiertas entre documentos (12.1 a 12.8) y vacíos sin decidir sobre las viviendas (12.9) y sobre el motor de reglas y las zonas con ingreso (12.10). Ningún agente las resuelve por su cuenta."
tipo: decision
origen: "maestro v1.4 (2026-09-14) §12; 12.9 y 12.10 agregadas el 2026-10-06"
actualizado: 2026-10-10
---

# Contradicciones abiertas entre documentos

> [!NOTE] Cómo va cada una al 2026-09-30
> - **12.1 (stack del front):** en el código, plantillas de Django + Alpine desde el 2026-09-13. Falta cerrarlo por escrito con Camilo.
> - **12.3 (personalización visual):** superada por la decisión del 2026-09-29 (color propio y foto 1:1).
> - **12.7 b (token o sesión):** resuelta el 2026-09-15 con token registrado en la base.
> - **12.7 c (un solo bloqueo):** resuelta el 2026-09-27: un bloqueo por persona y conjunto (D3 a).
> - **12.8 (qué entra en el mes):** sigue abierta.
> - **12.9 (quién vive en una vivienda y cómo se retira):** a) resuelta el 2026-10-06 con el vínculo `habitante`; b), c) y d) siguen abiertas.
> - **12.10 (motor de reglas y zonas con ingreso):** a) resuelta el 2026-10-06 (el tablero avisa) y e) resuelta el 2026-10-06 (la anticipación máxima del conjunto); c) resuelta el 2026-10-08 (dos permisos nuevos); d) resuelta el 2026-10-08 (D7 a: las palabras quedan como están); **b) sigue abierta**: las zonas con ingreso se construyeron el 2026-10-08 con salvaguardas, sin verificar lo legal (D3 a).
>
> Las resoluciones están en [construccion](construccion.md). Lo que no aparece en esta lista sigue como está escrito abajo.

> [!CAUTION] Ningún agente debe resolver estas por su cuenta Cada punto está sostenido por dos documentos vigentes que dicen cosas distintas.

## 12.1 · El stack de frontend está definido de dos formas incompatibles — **crítica**

|Documento|Qué dice|
|---|---|
|**Ruta de aprendizaje**|**Vue 3 + Vite + Vue Router + Pinia + Axios** contra una API de **DRF**. Dos repositorios separados. Incluye una Fase 2 completa de JavaScript y Vue|
|**Definición visual v1**|_"Dos servidores Python"_, con **`admind-web` renderizando plantillas de Django**, **CSS propio con variables** y **Alpine.js** para lo interactivo. Explícitamente: _"No hay Tailwind, Bootstrap ni framework de componentes"_|

La Definición visual es posterior y referencia a la ruta, así que probablemente el stack **cambió** y la ruta quedó sin actualizar. Arrastra cinco cosas:

- La **Fase 2** de la ruta (dos semanas de estudio de JS + Vue) sobra o no
- La **Definition of Done** exige _"endpoint documentado"_, lo que presupone API separada
- El **checklist de arranque** manda crear `admind-frontend` y levantar Vite
- La convención de ramas y repositorios asume dos repos con contrato de API congelado
- Las tareas marcadas _(frontend)_ en las HU cambian de naturaleza

**Consideración de equipo:** con plantillas de Django + Alpine desaparecen el segundo repo, CORS, el contrato de API congelado y toda la Fase 2 de JavaScript. Para un equipo donde uno de los dos apenas arranca, eso elimina buena parte de los puntos donde se pueden bloquear mutuamente. Con Vue, Camilo tiene que aprender JavaScript, Vue y Git en paralelo. No es solo una elección técnica: es cuánta superficie de fricción se ponen encima.

## 12.2 · El total de story points no cuadra

- **Seguimiento de velocidad:** 188 SP en 38 historias; 181 comprometidos en sprints
- **HU faltantes V11.1:** las nuevas suman 74 SP y _"el backlog completo (HU-01 a HU-38) suma 203"_

Diferencia de **15 SP**. Uno de los dos números está desactualizado y ambos se usan para planear.

## 12.3 · La personalización visual cambió y la propuesta no lo refleja

|Documento|Qué dice|
|---|---|
|**Propuesta V11**|_"Un color base del que se deriva la paleta, más el logo"_|
|**Definición visual v1**|**Catálogo cerrado de 8 acentos por slug**, sin selector libre. **Logo por conjunto fuera del alcance de v1**|
|**HU-26**|La pantalla de selección muestra _"nombre, logo y color base de cada conjunto"_|

El sistema visual es el más reciente y el más razonado — mantiene la forma del principio de no-configurabilidad, cambiando solo quién elige la fila. Falta propagarlo a la propuesta y a los criterios de aceptación de HU-26.

## 12.4 · PB-08, canal de notificaciones: núcleo sin trabajo estimado

El canal es un **componente explícito del núcleo** que debe construirse **antes** que sus seis consumidores (enrutamiento por vínculos, bandeja del administrador, registro de pago, campana, anulaciones del Superusuario, tablón). No tiene HU propia ni story points en ningún sprint; se asume absorbido por otras historias. El propio seguimiento de velocidad marca la duda: _vale la pena confirmar que su costo está realmente absorbido y no simplemente omitido._

## 12.5 · Sprint 6 sobrecargado con dependencia cruzada

38 SP contra un promedio de 26, y concentra las tres historias de Secretaría. **HU-22 (bandeja de triage) depende de HU-29 (Casos, Sprint 5) y HU-31 (Citas, Sprint 6)** — HU-31 tiene que cerrarse antes que HU-22 dentro del mismo sprint.

## 12.6 · Menores

- **Escala de puntos lineal (2–9), no Fibonacci**, mientras el documento de proceso enseña Fibonacci. Funciona, pero hay que tener la justificación lista por si el jurado pregunta
- **PB-06, PB-16, PB-19 y PB-24** siguen sin HU propia por decisión del equipo, cubiertos dentro de otras historias
- La ruta de aprendizaje nombra al compañero como **"Sergio"**; es **Camilo**
- Existían dos copias idénticas de la Propuesta V11 (`Propuesta_V11.md` y `claude_Propuesta_V11.md`), diferenciadas solo por el formato de los callouts. Conservar una sola

## 12.7 · Detectadas el 2026-09-11, cruzando este documento con la ruta de aprendizaje

_Sin confirmar por el equipo. Se listan para que no se pierdan, no como hechos._

**a) El modelo de ramas del curso contra la DoD y la ruta.** La DoD (§8.1) dice `develop` y la ruta enseña una rama por historia con PR; el profesor fijó `main`, `desarrollo` y `pruebas` sin ramas por historia (§8.5). Falta decidir qué PR cuenta como la revisión que exige la DoD, y dónde queda el "ambiente de pruebas".

**b) Token contra sesión.** La ruta enseña autenticación por token con un interceptor de Axios (Fase 2), pero su propia Fase 3.1 y el §5.4 de este documento dicen que el conjunto activo **sale de la sesión** y que ningún controlador acepta `conjunto_id`. Con un token sin estado hay que decidir dónde vive el conjunto activo; si viaja en una cabecera, es un parámetro con otro nombre. **Pesa directamente en §12.1:** con plantillas de Django la sesión es nativa; con Vue hay que diseñarlo (por ejemplo, autenticación por sesión de DRF en lugar de token).

**c) "Un solo bloqueo activo en todo el sistema" contra "toda clave única incluye `conjunto_id`".** El §5.1 dice que un residente solo puede tener un bloqueo activo en todo el sistema; el §5.4 exige que toda clave única lleve `conjunto_id`. Una persona puede tener rol de Residente en dos conjuntos. Si la frase es literal, esa restricción cruza conjuntos y es una excepción al aislamiento que no está en la lista cerrada de tablas globales (R12); si no lo es, hay que corregir la redacción.

## 12.8 · Detectada el 2026-09-14: el plan del semestre contra el plazo de un mes

_El plazo es un hecho. Lo abierto es qué hacer con él, y ningún agente recorta alcance por su cuenta._

|Fuente|Qué dice|
|---|---|
|**§8.1 y §11.2**|Siete sprints de dos semanas, 38 historias, la misma duración en todos los sprints|
|**Plazo comunicado el 2026-09-14**|Un mes para entregar, sin exigir el proyecto completo|

Falta decidir:

- **Qué historias entran.** El §3 da el orden (Núcleo, Comprometido, Condicional), pero no dice cuánto del Núcleo cabe en un mes
- **Cuántos sprints y de qué duración.** La regla de duración fija (§8.1) existe para medir velocidad, y el §11.3 dejaba que el Sprint 1 calibrara la cifra
- **Qué evidencias de Scrum del §8.1 se alcanzan a producir**, porque el jurado las va a pedir igual

## 12.9 · Detectadas el 2026-10-06, al definir HU-39: quién vive en una vivienda y cómo se retira

_No son contradicciones entre documentos: son vacíos que Alejo preguntó y que nadie ha decidido. Lo que se afirma del código se comprobó ese día._

**a) Las personas de una vivienda que no son propietario ni arrendatario — resuelta el 2026-10-06.** Alejo decidió el tercer tipo de vínculo, `habitante`: está en [construccion](construccion.md) y sigue sin construir. Lo que sigue es el vacío como se detectó. Hoy una persona llega a una vivienda así: se crea con su cuenta y un rol en el conjunto (`registrar_usuario` crea las tres cosas juntas), y después se le registra un vínculo, que solo puede ser `propietario` o `arrendatario`, con `reside` sí o no. El cónyuge o el hijo adulto que vive ahí no cabe en ninguno de los dos tipos, así que no puede reservar, porque el derecho a reservar nace del vínculo ([unidades](../05_Modulos/unidades.md)). [personas](../05_Modulos/personas.md) prevé una persona sin cuenta («un menor con TI registrado por sus padres»), pero no existe la operación que la cree. Falta decidir si se registran, y cómo: nada más que los titulares (como hoy), un tercer tipo de vínculo para quien solo habita, o un censo sin identidad. Tocaría `VinculoUnidad` y quizá `Persona`.

**Esto bloquea las zonas con ingreso** ([ingresos](../05_Modulos/ingresos.md)). Ahí el vigilante busca el documento solo entre quienes residen según sus vínculos, así que la familia de un propietario o de un arrendatario sale como «no encontrado» y solo podría entrar como acompañante de un titular que esté presente. Las reservas no se afectan: la familia asiste como parte del aforo de la reserva. Propuesta del agente del 2026-10-06, sin decidir: un tercer tipo de vínculo, `habitante`, siempre con `reside`, para una persona que puede no tener cuenta ni rol. Obliga a volver explícitos los dos enrutamientos que hoy toman «todos los vínculos» (el anuncio a la vivienda y la infracción, `VINCULOS_POR_HECHO` en `apps/unidades/servicios.py`) y a crear la operación que registra una persona sin cuenta.

**b) Persona principal de la vivienda.** No existe. Una vivienda puede tener varios propietarios y varios arrendatarios vigentes, todos iguales, y a quién se avisa lo decide el hecho, no un «principal». Falta decidir si el equipo quiere un contacto principal y para qué.

**c) Qué datos se piden de quienes se mudan.** La bóveda solo fija la regla general: toda captura de documento exige finalidad declarada, autorización y plazo de retención (Ley 1581, [legal](../01_Contexto/legal.md) §4.2). No hay un requisito escrito sobre el registro de residentes. Por verificar contra la guía legal v1.0 y con el docente, antes de programar nada: que la Ley 675 (art. 51, num. 2) encarga al administrador el registro de propietarios y residentes sin decir qué campos lleva, y el trato que la Ley 1581 da a los datos de menores y a los datos sensibles. Con duda legal no se implementa. El 2026-10-06 Alejo decidió que los habitantes, menores incluidos, se registran con su documento. Lo que falta definir antes de construir esa pantalla es cómo cumple los tres requisitos: qué finalidad se declara, quién autoriza (el adulto responsable, si es un menor) y cuánto tiempo se conserva.

**d) Retirar varias viviendas a la vez.** [eliminacion](../03_Reglas/eliminacion.md) dice que ninguna operación borra ni desactiva por filtro, siempre por identificador, y Alejo decidió que una vivienda se retira una por una. Si una generación sale mal (por ejemplo, dos pisos de más en seis torres son 48 viviendas), corregirla es lento. Falta decidir si una lista explícita de viviendas marcadas, con confirmación que las nombre, cuenta como «por identificador». La vista previa de HU-39 existe para que esto casi no pase.

## 12.10 · Detectadas el 2026-10-06, al redefinir el motor de reglas y las zonas con ingreso

_Tampoco son contradicciones entre documentos: son vacíos que quedaron al definir [motor_reglas](../05_Modulos/motor_reglas.md) e [ingresos](../05_Modulos/ingresos.md)._

**a) Un cierre que cae sobre reservas ya aprobadas.** *Días que no abre* admite periodos sin tope, y las reglas se evalúan al pedir, así que un cierre nuevo no toca las reservas aprobadas de esos días. Falta decidir qué hace el sistema al guardarlo: avisar cuántas quedan dentro y dejar que Administración las cancele (la que recomendó el agente), no dejar guardar mientras existan, o cancelarlas todas con aviso a cada residente. **Resuelta el 2026-10-06:** Alejo eligió avisar (D2 a del plan del motor). El tablero de reglas dice cuántas reservas apartadas o aprobadas caen en los días que el área no abre y enlaza a las solicitudes del área; cancelarlas sigue siendo decisión de Administración, caso por caso.

**b) Lo legal, por verificar antes de programar.** Con duda legal no se implementa. **El 2026-10-08 Alejo decidió primero no construir hasta verificar estos puntos y después, en la misma fecha, construir con salvaguardas (D3 a), sin haberlos verificado.** Las salvaguardas están en [ingresos](../05_Modulos/ingresos.md): el texto del aviso de finalidad sigue pendiente y de él depende cerrar este punto. Es la D3 de [Plan_Zonas_Con_Ingreso](../07_Planes/hechos/Plan_Zonas_Con_Ingreso.md), que queda detenido. **El 2026-10-10 Alejo decidió además conectar la mora real con *paz y salvo*** (D3 b de [Plan_Pago_De_Administracion](../07_Planes/hechos/Plan_Pago_De_Administracion.md), fase F5, sin construir), otra vez sin verificar el primer punto de abajo.

- **Actualización del 2026-10-10:** la mora **ya es real**. Alejo eligió conectarla con los pagos (D3 b de [Plan_Pago_De_Administracion](../07_Planes/hechos/Plan_Pago_De_Administracion.md)) y la reconfirmó al empezar F5, sin haber verificado esto. Las salvaguardas: *paz y salvo* está apagada por defecto, la enciende Administración a conciencia y su descripción advierte que se aplique solo si el reglamento lo permite; sin *día límite de pago* no hay mora; y la mora solo toca reservas e ingresos a zonas comunes.
- Que restringir por mora el ingreso al gimnasio o a la piscina procede. El agente citó **de memoria** que el art. 59 de la Ley 675 nombra las zonas de recreación y deporte como bienes no esenciales; [legal](../01_Contexto/legal.md) §4.2 solo trae la referencia. Sigue vigente el aviso del 2026-10-05: nada impide crear una zona que sea un bien esencial y exigirle paz y salvo.
- Que registrar quién entra a una zona, y cuándo, es un dato personal: la Ley 1581 pide finalidad declarada, autorización y plazo de retención. No se definió ninguno de los tres.
- Las reglas de piscina de la Ley 1209 (menores de 12 años con un adulto, salvavidas) no se definieron para el modo con ingreso.

**c) El permiso y el rol de quien registra el ingreso.** Alejo eligió Vigilancia «por ahora» y dudó si debía ser un rol aparte. Hace falta un permiso nuevo en el catálogo; el agente propuso `ingreso.registrar`. El catálogo de roles y permisos es de equipo. **Resuelta el 2026-10-08:** Alejo eligió dos permisos, como en visitantes: `ingreso.registrar` para Vigilancia e `ingreso.ver_historico` para Administración, sensible. Sin construir; falta contárselo a Camilo ([construccion](construccion.md)).

**d) Las palabras en pantalla.** La definición dice *zona* y el código y los textos actuales dicen *área*; las descripciones se escribieron una vez con *turno* y el glosario dice *franja*. Falta quedarse con un solo par. **Resuelta el 2026-10-08:** Alejo eligió D7 a: las palabras quedan como están («área» en gestión, «Zonas comunes» para el residente) y el modo se dice «Con reserva» y «Con ingreso». Pasar todo a «zona» tocaría unas 15 plantillas más y sería un plan aparte.

**e) Cómo entran las reglas al asistente de creación.** Qué paso llena las alfa, cuáles son obligatorias y qué reemplaza al requisito actual de «al menos una regla beta vigente» para quedar operativo. Es lo siguiente por definir con Alejo. **Decidido en parte el 2026-10-06:** el paso de reglas es el tablero del plan del motor; para quedar operativo se exigen al menos un área activa y las reglas del conjunto, en vez de «al menos una regla beta vigente». Falta precisar qué cuenta como reglas del conjunto definidas: es la D3 de [Plan_Asistente_De_Creacion](../07_Planes/activos/Plan_Asistente_De_Creacion.md). **Resuelta el 2026-10-06:** Alejo eligió D3 a: cuenta tener vigente la anticipación máxima del conjunto. Ya está construido ([construccion](construccion.md)).

## Ver también

- [alcance](../01_Contexto/alcance.md) — maestro §3
- [aislamiento](../03_Reglas/aislamiento.md) — maestro §5.4
- [git](../03_Reglas/git.md) — maestro §8.5
- [scrum_y_dod](../03_Reglas/scrum_y_dod.md) — maestro §8.1
- [reservas](../05_Modulos/reservas.md) — maestro §5.1
- [backlog_y_plazo](../08_Estado/backlog_y_plazo.md) — maestro §11.2, §11.3
- [riesgos](riesgos.md) — R12
