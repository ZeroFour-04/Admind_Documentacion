---
resumen: "Contradicciones abiertas entre documentos (12.1 a 12.8). Ningún agente las resuelve por su cuenta."
tipo: decision
origen: "maestro v1.4 (2026-09-14) §12"
actualizado: 2026-09-30
---

# Contradicciones abiertas entre documentos

> [!NOTE] Cómo va cada una al 2026-09-30
> - **12.1 (stack del front):** en el código, plantillas de Django + Alpine desde el 2026-09-13. Falta cerrarlo por escrito con Camilo.
> - **12.3 (personalización visual):** superada por la decisión del 2026-09-29 (color propio y foto 1:1).
> - **12.7 b (token o sesión):** resuelta el 2026-09-15 con token registrado en la base.
> - **12.7 c (un solo bloqueo):** resuelta el 2026-09-27: un bloqueo por persona y conjunto (D3 a).
> - **12.8 (qué entra en el mes):** sigue abierta.
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

## Ver también

- [alcance](../01_Contexto/alcance.md) — maestro §3
- [aislamiento](../03_Reglas/aislamiento.md) — maestro §5.4
- [git](../03_Reglas/git.md) — maestro §8.5
- [scrum_y_dod](../03_Reglas/scrum_y_dod.md) — maestro §8.1
- [reservas](../05_Modulos/reservas.md) — maestro §5.1
- [backlog_y_plazo](../08_Estado/backlog_y_plazo.md) — maestro §11.2, §11.3
- [riesgos](riesgos.md) — R12
