---
resumen: "El plan original: reparto del backlog en 7 sprints, velocidad, el plazo de un mes, el bloqueante único y los pendientes para la sustentación."
tipo: estado
origen: "maestro v1.4 (2026-09-14) §11"
actualizado: 2026-10-11
revisado: 2026-10-11
---

# Backlog, velocidad y plazo

El avance real del desarrollo está en [estado_actual](estado_actual.md) e [historias](historias.md). Esta nota conserva el plan.

**Corte del seguimiento de velocidad: 2026-09-04.** Sin sprint iniciado.

> [!TIP] El avance del desarrollo vive en las otras notas de esta carpeta
> Desde el 2026-09-14 hay código. Qué existe y qué historias avanzan está en [estado_actual](estado_actual.md) e [historias](historias.md); qué se decidió al construir, en [construccion](../06_Decisiones/construccion.md). Esta nota conserva el plan; aquellas, lo que ya pasó.

> [!CAUTION] El plazo de entrega se redujo a un mes (2026-09-14)
> Comunicado por Alejo el 2026-09-14: la entrega queda cerca del **14 de octubre de 2026**, con la fecha exacta por confirmar, y **no hay que entregar el proyecto completo**. Consecuencias:
> - El reparto de siete sprints de dos semanas (§11.2) no cabe: un mes da para dos sprints de esa duración
> - Qué se entrega es decisión del equipo y sigue abierta (§12.8). El §3 ya da el criterio: si solo el Núcleo funciona, el proyecto se sustenta igual
> - Cambió el modo de trabajo con IA (§8.4) y la Fase 0 pasa a ser opcional (§7.3)

> [!NOTE] La demo descartada (2026-09-11)
> En septiembre se construyó una demo navegable en Django —ingreso, panel e unidades— para un entregable de clase. **Se descartó:** estaba hecha por completo con IA y el equipo no podía explicarla. Quedó comprimida en `Backend.zip`, **no se usa como referencia**, y el repositorio volvió a quedar sin código de producto.
>
> No conviene esconderlo: es §8.4 aplicada, y es exactamente el tipo de reversión que §9 manda registrar con su razón. Si el docente vio esa demo, la historia la cuenta el equipo antes de que la pregunten.

## 11.1 Dónde vive cada artefacto

|Artefacto|Ubicación|
|---|---|
|Backlog + HU con story points|Notion → `Gestión Scrum — AdMind` → base **Historias de Usuario**|
|Seguimiento de sprints|Notion → misma página → base **Sprints**|
|Excel V11.1 (entregable que el docente ya conoce, **congelado**)|Drive → `V11.1 Plantilla Product Backlog y HU BORRADOR.xlsx`|
|Plantilla de velocidad|Drive → `Plantilla_Calculo_Velocidad_Scrum.xlsx`|
|Documentación de diseño|`admind-docs` (Git)|
|Avance del desarrollo, por historia y por commit|`08_Estado/`, en el repositorio de documentación|

## 11.2 Reparto del backlog

|Sprint|HU|SP|
|---|---|---|
|1|HU-01 a HU-05, HU-26|25|
|2|HU-06 a HU-09|20|
|3|HU-10 a HU-13|26|
|4|HU-14 a HU-19|28|
|5|HU-20, HU-21, HU-25, HU-27, HU-28, HU-29|28|
|6|HU-22, HU-23, HU-24, HU-30 a HU-34|38|
|7|HU-35, HU-36, HU-37|16|
|Condicional|HU-38|7|

**38 historias.** Sprint 1 = identidad, autenticación y conjunto activo. En Django es mayoritariamente configuración y modelos.

## 11.3 Velocidad

- Historia de referencia: **HU-11 · Bloqueo exclusivo de 3 minutos**, 7 SP
- Suma de tareas técnicas: 185 min → **26,43 min por SP**
- Capacidad: 2160 min por sprint → **velocidad teórica de 81,7 SP**
- Pero el reparto implica **≈27 SP por sprint**

**Contradicción reconocida y aceptada.** El punto débil son los 185 minutos: implican resolver una historia de 7 SP en poco más de 3 horas entre dos personas, incluyendo transacción en base de datos, expiración de bloqueo y pruebas de concurrencia. Si toma 9–10 horas, el minuto por SP sube a ≈80 y la velocidad aterriza cerca de 27 SP.

**Decisión: no se corrige antes de arrancar.** El Sprint 1 dirá cuál cifra se parece a la realidad.

**Método de recálculo acordado con el docente** — velocidad empírica con promedio móvil:

1. Solo cuenta lo terminado. Una HU al 80 % aporta **0 SP**; lo inconcluso vuelve al backlog con sus SP intactos
2. Los SP **no se reestiman** porque una historia resulte más difícil: esa información entra por la velocidad
3. Se registran comprometidos y completados; el ratio es la evidencia de mejora para la sustentación
4. El Sprint 1 suele ser atípico (montaje de repos y entorno); si queda muy bajo se marca como caso aparte

> [!WARNING] Factor que todavía no está en ningún Excel **Los sprints 1 y 2 van a rendir menos**, porque además de programar se está aprendiendo el lenguaje del framework. Es normal y es medible. Registrarlo en la retrospectiva del Sprint 1 es dato empírico, es lo que Scrum pide, y ante el jurado **explica** la velocidad baja en vez de esconderla.

## 11.4 Bloqueante único

> [!CAUTION] Conseguir un reglamento de propiedad horizontal real + entrevista con el administrador de contacto
> 
> Es el bloqueante más antiguo del proyecto y hoy alimenta **tres catálogos**:
> 
> 1. Las **reglas beta** de reservas
> 2. Las **tres listas de causales formales** de rechazo (Evento, Caso, Cita)
> 3. La **asignación de permisos** de los cinco roles fijos — con **Secretaría como el caso más urgente**, porque es el único rol cuyos permisos se definieron desde el diseño y no desde la observación

## 11.5 Pendientes que afectan la sustentación

> [!NOTE] Cómo van al 2026-10-11
> La lista de abajo es del 2026-09-14 y se conserva como estaba. Desde entonces:
> - **Resueltos en el código:** el stack del frontend (plantillas de Django y Alpine; falta cerrarlo por escrito), la lista cerrada de tablas globales con su prueba, el límite de búsquedas por documento (20 por hora, por conjunto), el versionado del motor de reglas (cada cambio es una versión nueva y la evaluación se copia en la solicitud) y `expensa_mensual` (HU-35 registra si el mes se pagó, no cuánto).
> - **Cambió de forma:** la lista de reglas alfa y beta se redefinió el 2026-10-06 ([motor_reglas](../05_Modulos/motor_reglas.md)); sigue sin validarse contra un reglamento real (11.4).
> - **Siguen abiertos:** la fecha exacta y el alcance, las entrevistas documentadas, las consultas del Superusuario en la auditoría (R10), la retención de datos (R2), quién es PO y quién SM, la DoD frente a las ramas del curso, el ambiente de pruebas y los dos usuarios de la base de datos.
>
> Lo que falta hoy, completo: [pendientes](pendientes.md).

- [ ] **Confirmar la fecha exacta de entrega y decidir qué se entrega en ese mes** (§12.8). Añadido el 2026-09-14; condiciona el orden de todo lo demás en esta lista
- [ ] **Cerrar la decisión del stack de frontend** (§12.1). Bloquea el arranque del Sprint 1
- [ ] **Documentar formalmente las entrevistas a residentes**: guion, número de entrevistados, hallazgos y cómo cada hallazgo cambió el diseño. Sin esto, el flujo de reserva parece preferencia técnica y no decisión con evidencia
- [ ] **Decidir si las consultas del Superusuario a datos personales quedan en auditoría** (R10)
- [ ] **Escribir la lista cerrada de tablas globales** y la prueba transversal que la impone (R12)
- [ ] Definir el **límite de búsquedas por documento** por administrador y ventana de tiempo (R12)
- [ ] Definir **plazo de retención y purga** de datos de visitantes; justificación escrita de la captura de documento ampliada a toda persona (R2)
- [ ] **Cerrar la lista de reglas alfa** y el catálogo de reglas beta contra un reglamento real
- [ ] Resolver **vigencia y versionado** del motor de reglas: ¿snapshot de la versión aplicada en cada decisión?
- [ ] **Instanciar el Scrum del equipo**: quién es PO, quién es SM, stakeholder externo confirmado
- [ ] Definir de dónde sale `expensa_mensual` por unidad

_Los cuatro siguientes se detectaron el 2026-09-11 al cruzar este documento con la ruta de aprendizaje. Sin confirmar por el equipo._

- [ ] **Alinear la Definition of Done con el modelo de ramas del curso** (§8.1, §8.5 y §12.7 a)
- [ ] **Definir el ambiente de pruebas.** La DoD lo exige desde HU-01 y no hay ninguno definido en ningún documento: tal como está escrita, hoy ninguna historia puede darse por terminada
- [ ] **Decidir los dos usuarios de base de datos** que exige la auditoría de solo inserción: uno dueño, que corre las migraciones, y otro de aplicación sin `UPDATE`, `DELETE` ni DDL. Afecta también cómo `pytest-django` crea la base de pruebas
- [ ] **Ubicar la Fase 0 en el calendario.** La ruta la sitúa en un "Sprint 0" que no existe en el reparto de §11.2, y cuesta 25–30 horas por persona. _Pierde peso desde el 2026-09-14: la Fase 0 es opcional (§7.3)._

## 11.6 Pendientes menores con recomendación ya escrita

¿El documento es obligatorio desde el alta? _(exigirlo bloquea la importación masiva)_ · ¿Qué pasa en un cambio TI → CC? _(actualizar el par en la misma fila, cambio en auditoría; el UUID no se mueve)_ · ¿Un visitante recurrente se vuelve `Persona`? _(no — es un registro de portería con su propia purga)_ · ¿El administrador puede reversar un rechazo formal? _(no; el solicitante vuelve a solicitar)_ · ¿El anuncio a una vivienda alcanza al propietario no residente? _(sí, todo vínculo vigente)_ · ¿Se puede desactivar un conjunto sin borrarlo? _(sí, campo `activo`)_ · ¿Acuse de lectura en anuncios? _(campo, no bloqueo)_ · ¿El residente ve su propia actividad en el registro? _(sí, solo la suya)_ · ¿Se implementa reloj de vencimiento para Casos? _(reevaluar: habría que construirlo entero para un solo módulo)_ · ¿Qué pasa si un visitante se va sin registrar salida? _(liberación manual por vigilancia + listado de ocupaciones abiertas de más de N horas)_

## Ver también

- [alcance](../01_Contexto/alcance.md) — maestro §3
- [git](../03_Reglas/git.md) — maestro §8.5
- [scrum_y_dod](../03_Reglas/scrum_y_dod.md) — maestro §8.1
- [trabajo_con_ia](../03_Reglas/trabajo_con_ia.md) — maestro §8.4
- [abiertas](../06_Decisiones/abiertas.md) — maestro §12.1, §12.7, §12.8
- [cerradas](../06_Decisiones/cerradas.md) — maestro §9
- [Maestro_7.3_rama_lab](../Archivo/Lab/Maestro_7.3_rama_lab.md) — maestro §7.3
- [riesgos](../06_Decisiones/riesgos.md) — R2, R10, R12
