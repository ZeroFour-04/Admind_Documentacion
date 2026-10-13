---
resumen: "Cómo se escribe un plan de trabajo para que lo ejecute un agente, y qué se hace al terminarlo."
tipo: protocolo
origen: "forma del plan de los Sprints 2 y 3 (2026-09-27)"
actualizado: 2026-10-11
revisado: 2026-10-11
---

# Protocolo: abrir y cerrar un plan

## Cuándo se abre un plan

Cuando el trabajo es largo (varias historias o varias sesiones) o lo va a ejecutar un agente distinto del que lo pensó. Para una pieza suelta no hace falta: se pide y se construye.

## Abrir

1. **Medir el punto de partida** el mismo día: commits de `desarrollo` en los dos repositorios, pruebas en verde, migraciones aplicadas.
2. **Copiar la plantilla** [plan](Plantillas/plan.md) a `07_Planes/activos/` con un nombre que diga qué cubre, por ejemplo `Plan_HU-14.md`.
3. **Separar las decisiones.** Lo que solo puede decidir Alejo va en una tabla con opciones, una recomendación y una columna *Respuesta* vacía. Lo menor lo fija el plan y queda escrito. Un agente no empieza una fase cuya decisión esté vacía.
4. **Escribir cada fase** con: qué archivos toca, qué construye, qué prueba la da por hecha y qué commit deja.
5. **Agregar el plan** a la lista de [planes](../07_Planes/planes.md).

El plan cita las reglas en vez de copiarlas: [invariantes](../03_Reglas/invariantes.md), [convenciones](../03_Reglas/convenciones.md), [capas](../03_Reglas/capas.md) y [trabajo_con_ia](../03_Reglas/trabajo_con_ia.md).

## Ejecutar

- Solo lo que dice el plan. Lo que falte fuera de él se anota para el informe final.
- Al cerrar cada fase se corren los comandos de verificación ([pruebas_y_ejecucion](../02_Arquitectura/pruebas_y_ejecucion.md)). No se sigue con la suite en rojo.
- Si un paso choca con una decisión abierta o con el código real de una forma que el plan no previó, se detiene y se pregunta.

## Cerrar

1. **Informe final** en el chat: qué se construyó por fase, commits, pruebas antes y después, qué se desvió del plan y qué quedó fuera.
2. **Actualizar el contexto** con [actualizar_contexto](actualizar_contexto.md). Las decisiones que Alejo respondió en el plan pasan a [construccion](../06_Decisiones/construccion.md).
3. **Mover el archivo** de `07_Planes/activos/` a `07_Planes/hechos/` y cambiar su fila en [planes](../07_Planes/planes.md). En su frontmatter, `estado: hecho` y `ejecutado:` con la fecha; se corrigen los enlaces que apuntaban a `activos/` y se llena la columna *Plan* de [historias](../08_Estado/historias.md). Un plan hecho no se edita. La parte humana que falte no lo deja en `activos/`: va a pendientes (paso 4).
4. **Dejar escrito lo que el agente no puede hacer:** la parte humana de la DoD (PR `desarrollo → pruebas` revisado y prueba manual de quien no programó) va a [pendientes](../08_Estado/pendientes.md).

## Plan guiado

Cuando el plan lo ejecuta Alejo con un agente que guía en vez de construir, cambian tres cosas. Lo escribe un chat de planeación siguiendo [Inicio](../Inicio.md). Usa la plantilla [plan_guiado](Plantillas/plan_guiado.md), que trae la sección de seguimiento. Y se ejecuta con [ejecutar_plan_guiado](ejecutar_plan_guiado.md), solo si Alejo lo aprueba cuando el agente le pregunta; si prefiere que el agente construya, vale *Ejecutar* de arriba. Abrir y cerrar no cambian.

## Ver también

- [planes](../07_Planes/planes.md) — la lista de planes
- [plan](Plantillas/plan.md) y [plan_guiado](Plantillas/plan_guiado.md) — las plantillas
- [Inicio](../Inicio.md) — el chat que escribe un plan guiado
- [ejecutar_plan_guiado](ejecutar_plan_guiado.md) — cómo se ejecuta uno guiado
- [actualizar_contexto](actualizar_contexto.md) — lo que se actualiza al cerrar
