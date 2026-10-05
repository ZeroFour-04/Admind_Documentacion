---
resumen: "Dónde está el proyecto hoy: commits, pruebas, historias por grupo y lo que frena para cerrarlas."
tipo: estado
corte: 2026-09-30
origen: "guía de estructura §1 y §10 (2026-09-30)"
actualizado: 2026-10-05
---

# Estado actual

> [!IMPORTANT] Dos formas de contar
> - **Con la Definition of Done** ([scrum_y_dod](../03_Reglas/scrum_y_dod.md)): ninguna historia está terminada, porque ninguna ha pasado por un PR `desarrollo → pruebas` revisado ni por la prueba manual de quien no la programó.
> - **En los informes al docente** (decisión de Alejo, 2026-09-29): los Sprints 1 y 2 se reportan terminados, junto con HU-21 y HU-25: 12 historias, 55 de 188 SP; el Sprint 3, en revisión.

## Resumen (corte 2026-09-30)

| Qué | Estado al 2026-09-30 |
|---|---|
| **Backend** (la API) | Rama `desarrollo` en `ee256ff`, **subida a GitHub**, sin cambios pendientes. 11 apps con código más `comun`. **330 pruebas: 329 pasan y 1 falla** (verificado hoy, 33 s). *Actualización del 2026-10-05:* con el límite de enlaces de recuperación, **334 pruebas: 333 pasan y 1 falla** (la misma), en `desarrollo` sobre `71ded31` y con el cambio **sin commitear** hasta que Alejo lo haga. La que falla es `test_toda_ruta_de_la_api_esta_cubierta` ([pruebas_y_ejecucion](../02_Arquitectura/pruebas_y_ejecucion.md)) |
| **Frontend** (las pantallas) | Rama `desarrollo` en `7fa88ea`, **subida a GitHub**, sin cambios pendientes. 11 apps con pantallas. **140 pruebas, todas pasan** (verificado hoy, 7 s). *Actualización del 2026-10-05:* el favicon (`2af7114`) lo subió a 150 y las pruebas de la recuperación de contraseña, a **160, todas pasan**; esas 10 están **sin commitear** hasta que Alejo lo haga |
| **Historias de usuario** | HU-01 a HU-13, HU-21, HU-25 y HU-26 tienen código. **Ninguna está "Terminada"**: a todas les falta la parte humana de la DoD (PR `desarrollo → pruebas` revisado y prueba manual de quien no la programó) |
| **Lo que sigue sin empezar** | HU-14 en adelante (bandeja del administrador, pagos, visitantes, casos, citas, documentos…), salvo HU-21 y HU-25 |
| **Plazo** | Entrega cerca del 2026-10-14 (fecha exacta sin confirmar). No hay que entregar las 38 historias |

## Historias por grupo

| Grupo | Historias | Qué hay |
|---|---|---|
| **Sprint 1** | HU-01 login y recuperación · HU-02 segundo factor · HU-03 asistente de conjunto · HU-04 persona única · HU-05 aislamiento · HU-26 selector | Todo construido y commiteado ("sprint 1 terminado", 21–22/09). HU-03 quedó **parcial** (sin reglamento). [historias_evidencia](historias_evidencia.md) todavía muestra fracciones viejas para HU-01, 02, 03 y 26 |
| **Sprints 2 y 3** | HU-06 roles · HU-07 vincular persona · HU-08 unidades · HU-09 áreas · HU-10 reglas beta · HU-11 bloqueo · HU-12 confirmación · HU-13 envío y reglas | Todos sus criterios en código y con prueba (27/09). En Notion, "En revisión". HU-06 cambió el 29/09: **un solo rol por conjunto** (se cambia, no se suma) y sin rol Consejo; su criterio en Notion y en el Excel aún dice varios roles |
| **Adelantadas del Sprint 5** | HU-21 color y foto · HU-25 anuncios | Construidas el 22/09 (HU-25 con lo mínimo de notificaciones). HU-21 se amplió el 29/09 con el color propio y la foto 1:1, ya commiteado |
| **Sin empezar** | HU-14 a HU-20, HU-22 a HU-24, HU-27 a HU-38 | Solo el README de su app |

## Lo que frena para cerrar historias

- [ ] **Arreglar la prueba que falla** del backend: agregar `usuario-perfil` (ruta sin conjunto) a `RUTAS_SIN_CONJUNTO` y `usuario-eliminar` (ruta de conjunto) a la prueba del intruso, en `tests/aislamiento/test_intruso.py`. Hoy `desarrollo` sube con un test en rojo.
- [ ] El backend **no tiene rama `pruebas` en GitHub** (existe solo en local). Hay que subirla para abrir los PR `desarrollo → pruebas`.
- [ ] **Prueba manual** de HU-06 a HU-13 por quien no las programó, con el guion de `07_Planes/hechos/Admind_Plan_Sprints_2_3.md` §6.
- [ ] **Decidir el alcance** que entra antes de la entrega (maestro §12.8). El siguiente paso natural del núcleo es HU-14 (aprobar o rechazar), que cierra el ciclo de la reserva.
- [ ] Llevar al texto de diseño (antes, el maestro) las decisiones tomadas al construir, que hoy solo están avisadas al inicio de cada nota: estado `LIBERADA`, un bloqueo por persona por conjunto, catálogo de reglas beta y versionado, token con registro en la base, stack del front (§12.1), el **color propio y la foto 1:1** de HU-21 (§6.3 todavía dice que el acento está aplazado y sin hex libre), el **rol único por conjunto** (§3.1 y R5 dicen varios) y el **Superusuario con todos los permisos**.
- [ ] [historias_evidencia](historias_evidencia.md) e [inventario_codigo](inventario_codigo.md) tienen filas del 15/09 sin actualizar (lo dice su propio aviso).

## Ver también

- [historias](historias.md) — las 38 historias, una por una
- [pendientes](pendientes.md) — la lista larga de pendientes
- [bitacora](bitacora.md) — qué pasó y cuándo
- [backlog_y_plazo](backlog_y_plazo.md) — el plan original, la velocidad y el plazo
