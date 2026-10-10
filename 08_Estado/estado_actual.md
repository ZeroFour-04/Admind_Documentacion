---
resumen: "Dónde está el proyecto hoy: commits, pruebas, historias por grupo y lo que frena para cerrarlas."
tipo: estado
corte: 2026-10-05
origen: "guía de estructura §1 y §10 (2026-09-30)"
actualizado: 2026-10-08
---

# Estado actual

> [!IMPORTANT] Dos formas de contar
> - **Con la Definition of Done** ([scrum_y_dod](../03_Reglas/scrum_y_dod.md)): ninguna historia está terminada, porque ninguna ha pasado por un PR `desarrollo → pruebas` revisado ni por la prueba manual de quien no la programó.
> - **En los informes al docente:** en el informe 3 (2026-09-29), Sprints 1 y 2 terminados con HU-21 y HU-25: 12 historias, 55 de 188 SP. En el **informe 4 (2026-10-06)**, con un criterio menos estricto pedido por Alejo, Sprints 1 a 3, HU-14, HU-21 y HU-25: **17 historias, 89 SP**; HU-27 y HU-33 en progreso.

## Resumen (corte 2026-10-05)

| Qué | Estado al 2026-10-05 |
|---|---|
| **Cambio del 2026-10-08, sin commit** | **Las zonas con ingreso** ([ingresos](../05_Modulos/ingresos.md), [Plan_Zonas_Con_Ingreso](../07_Planes/hechos/Plan_Zonas_Con_Ingreso.md)), construidas por el agente sobre Backend `279e963` y Frontend `f5b3d08`, con salvaguardas legales y **sin haber verificado lo legal** (D3 a). Backend: **478 pruebas, 477 pasan y 1 falla** (la misma, por las mismas cinco rutas); tres migraciones nuevas (`areas/0005`, `reglas/0005`, `ingresos/0001`) **sin aplicar en `admind_db`**. Frontend: **246 pruebas, todas pasan**. Antes del cambio eran 416 (415 pasan) y 210. Falta el texto del aviso de finalidad, la prueba manual y avisarle a Camilo ([pendientes](pendientes.md)) |
| **Verificado el 2026-10-08, al abrir el plan de zonas con ingreso** | Backend sigue en `279e963`: 416 pruebas, 415 pasan y 1 falla, la misma. Frontend avanzó a `f5b3d08` («responsive»): **210 pruebas, todas pasan**. Los dos limpios y sin migraciones pendientes en `admind_db`. Es el punto de partida del cambio de arriba |
| **Verificado el 2026-10-06, al hacer el informe 4** | **Todo tiene commit y está subido:** Backend `desarrollo` en `279e963`, Frontend en `fff4651`, los dos limpios e iguales a GitHub. **Todas las migraciones están aplicadas en `admind_db`** y `makemigrations --check` no encuentra cambios. Backend: **416 pruebas, 415 pasan y 1 falla**, la misma; Frontend: **208, todas pasan**. **HU-14 (aprobar y rechazar) está construida** desde el 05/10 por Camilo y no estaba en esta nota. Las filas de abajo que dicen «sin commit» o «sin aplicar» quedaron atrás |
| **Cambio del 2026-10-06, sin commit** | **El asistente de creación completo (HU-03) y la estructura de viviendas (HU-39, primera parte)**, sobre Backend `9b3b231` y Frontend `b5d96df`. El asistente tiene siete pasos, genera las viviendas en lote, sube el reglamento en PDF (app nueva `documentos`) y **un conjunto ya puede quedar operativo**; lo activa el Superusuario o Administración. Backend: **415 pruebas, 414 pasan y 1 falla**, la misma de antes; dos migraciones nuevas (`unidades/0002_estructura` y `documentos/0001_initial`) **sin aplicar en `admind_db`**. Frontend: **206 pruebas, todas pasan**. Antes del cambio eran 378 (377 pasan) y 196 |
| **Motor de reglas (2026-10-06), ya con commit** | El **motor de reglas por niveles** ([motor_reglas](../05_Modulos/motor_reglas.md)) está construido en los dos repositorios, sobre Backend `2d11dbe` y Frontend `a3792d7`; entró a `desarrollo` en Backend `9b3b231` y Frontend `b5d96df`. Backend: **378 pruebas, 377 pasan y 1 falla**, la misma de antes; cuatro migraciones nuevas (`areas/0004`, `reglas/0002` a `0004`) **sin aplicar en `admind_db`**. Frontend: **193 pruebas, todas pasan**. Antes del cambio eran 368 (367 pasan) y 188. El resto de esta tabla es del corte del 05/10 y no se volvió a revisar |
| **Backend** (la API) | Rama `desarrollo` en `5ed32a5`, **subida a GitHub**: ya incluye quitar la clasificación de las áreas (HU-09) y el enlace por correo para quitar el segundo factor (HU-02). **Sin commit** hay un cambio de hoy: las fotos de los anuncios (HU-25), con su migración `anuncios/0002_fotos` ya aplicada en `admind_db`. Siguen sin aplicar ahí `areas.0002` y `visitantes.0001`. 12 apps con código más `comun`: la nueva es `visitantes`, de Camilo. En el último commit, 344 pruebas (343 pasan y 1 falla); con las fotos sin commit, **362: 361 pasan y 1 falla** (verificado hoy, 35 s). La que falla es `test_toda_ruta_de_la_api_esta_cubierta` ([pruebas_y_ejecucion](../02_Arquitectura/pruebas_y_ejecucion.md)). `makemigrations --check` no encuentra cambios |
| **Frontend** (las pantallas) | Rama `desarrollo` en `ea0e9e5`, **subida a GitHub**. **Sin commit**, las fotos de los anuncios. 12 apps con pantallas: la nueva es `visitantes`. En el último commit, 169 pruebas; con las fotos, **180, todas pasan** (verificado hoy, 7 s) |
| **Historias de usuario** | HU-01 a HU-13, HU-21, HU-25 y HU-26 tienen código, y HU-27 va **parcial** (solo el ingreso del visitante). **Ninguna está "Terminada"**: a todas les falta la parte humana de la DoD (PR `desarrollo → pruebas` revisado y prueba manual de quien no la programó) |
| **Lo que sigue sin empezar** | HU-14 en adelante (bandeja del administrador, pagos, casos, citas, documentos…), salvo HU-21, HU-25 y HU-27 |
| **Plazo** | Entrega cerca del 2026-10-14 (fecha exacta sin confirmar). No hay que entregar las 38 historias |

## Historias por grupo

| Grupo | Historias | Qué hay |
|---|---|---|
| **Sprint 1** | HU-01 login y recuperación · HU-02 segundo factor · HU-03 asistente de conjunto · HU-04 persona única · HU-05 aislamiento · HU-26 selector | Todo construido y commiteado ("sprint 1 terminado", 21–22/09). HU-03 quedó **parcial** (sin reglamento) hasta el 06/10, cuando se construyó completa (sin commit). [historias_evidencia](historias_evidencia.md) todavía muestra fracciones viejas para HU-01, 02, 03 y 26 |
| **Sprints 2 y 3** | HU-06 roles · HU-07 vincular persona · HU-08 unidades · HU-09 áreas · HU-10 reglas beta · HU-11 bloqueo · HU-12 confirmación · HU-13 envío y reglas | Todos sus criterios en código y con prueba (27/09). En Notion, "En revisión". El 06/10, HU-09, HU-10 y HU-13 cambiaron con el motor de reglas por niveles (sin commit); sus criterios en Notion describen el modelo anterior. HU-06 cambió el 29/09: **un solo rol por conjunto** (se cambia, no se suma) y sin rol Consejo; su criterio en Notion y en el Excel aún dice varios roles |
| **Adelantadas del Sprint 5** | HU-21 color y foto · HU-25 anuncios | Construidas el 22/09 (HU-25 con lo mínimo de notificaciones). HU-21 se amplió el 29/09 con el color propio y la foto 1:1, ya commiteado. HU-25 se amplió el 05/10 con hasta 4 fotos por anuncio ([triage](../05_Modulos/triage.md)), sin commit |
| **Parcial, de Camilo** | HU-27 visitantes | Registrar el ingreso y consultar el listado (commit del 01/10, en `desarrollo` desde el 05/10). Sin salida, sin parqueadero de visitantes (HU-28) y sin lo de la Ley 1581. Detalle en [historias](historias.md) |
| **Sin empezar** | HU-14 a HU-20, HU-22 a HU-24, HU-28 a HU-38 | Solo el README de su app |

## Lo que frena para cerrar historias

- [ ] **Arreglar la prueba que falla** del backend: agregar `usuario-perfil` (ruta sin conjunto) a `RUTAS_SIN_CONJUNTO` y `usuario-eliminar` (ruta de conjunto) a la prueba del intruso, en `tests/aislamiento/test_intruso.py`. Hoy `desarrollo` sube con un test en rojo. Al 06/10 la prueba lista **5 rutas** sin registrar (entre ellas `usuario-perfil` y `solicitud-decision`); ninguna es del motor de reglas.
- [ ] **Motor de reglas (06/10):** falta la prueba manual y avisarle a Camilo ([pendientes](pendientes.md)). Los commits y el `migrate` en `admind_db` ya están (verificado el 06/10).
- [ ] **Asistente y viviendas (06/10):** falta la prueba manual y avisarle a Camilo, que esta vez incluye un cambio al catálogo de permisos ([pendientes](pendientes.md)). Los commits y el `migrate` ya están (verificado el 06/10).
- [ ] **HU-14 (05/10, Camilo):** registrar `solicitudes-bandeja`, `solicitudes-area` y `solicitud-decision` en la prueba del intruso, y decidir si entra el aviso al residente y la causal de lista cerrada. Cambió el catálogo de permisos: Secretaría ahora ve, aprueba y rechaza reservas.
- [ ] **Notion** no refleja el informe 4: HU-14 y el Sprint 3 siguen sin pasar a «Finalizado» y HU-39 no existe allí. Lo cambia el equipo, no un agente.
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
