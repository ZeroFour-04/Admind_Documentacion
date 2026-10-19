---
resumen: "Dónde está el proyecto hoy: commits, pruebas, migraciones, historias por grupo y lo que frena para cerrarlas."
tipo: estado
corte: 2026-10-13
origen: "verificado en los tres repositorios y en admind_db el 2026-10-13"
actualizado: 2026-10-13
revisado: 2026-10-13
---

# Estado actual

Esta nota dice **cómo está hoy**. Cómo se llegó aquí, día por día, está en [bitacora](bitacora.md).

> [!IMPORTANT] Dos formas de contar
> - **Con la Definition of Done** ([scrum_y_dod](../03_Reglas/scrum_y_dod.md)): ninguna historia está terminada, porque ninguna ha pasado por un PR `desarrollo → pruebas` revisado ni por la prueba manual de quien no la programó.
> - **En los informes al docente:** el informe 4 (2026-10-06), con un criterio menos estricto pedido por Alejo, cuenta Sprints 1 a 3, HU-14, HU-21 y HU-25: **17 historias, 89 SP**. Está en `Archivo/Informes/2026-10-06/`.

## Resumen (corte 2026-10-13)

| Qué | Cómo está |
|---|---|
| **Backend** (la API) | Rama `desarrollo` en **`7eb5b5a`** («boton eliminar conjunto», 13/10, de Camilo), igual a `origin/desarrollo`. Sobre `0b627d1` de Camilo (12/10) van el modo de uso de un área (`287621c`), los límites de texto (`87d67c5`), el dashboard de gestión (`85f9f23`, «Dashboard beta») y la baja del conjunto con el teléfono a 15 (`7eb5b5a`). 17 apps con código más `comun`; 4 solo con README (`citas`, `infracciones`, `triage`, `importacion_respaldo`). **84 rutas de la API**, todas en la prueba del intruso |
| **Frontend** (las pantallas) | Rama `desarrollo` en **`8279616`** («boton eliminar conjunto», 13/10, de Camilo), igual a `origin/desarrollo`. Sobre `7cd762c` de Camilo (12/10) van el modo de uso (`6c61ac4`), los límites de texto (`7121d94`), el menú de Vigilancia (`0adf5eb`), el dashboard (`d0e4af7`) y el botón «Eliminar conjunto» (`8279616`). 15 apps con pantallas, más `casos` |
| **Sin commit** | Nada: los tres repositorios están limpios y alineados con GitHub |
| **Documentación** | Rama `main` en `e08a958` («Dashboard beta», 13/10), igual a `origin/main`, más las notas de la revisión del 13/10 (la baja del conjunto, el teléfono y el cuadro de pantallas del front), sin commit |
| **Base de datos** | **Ninguna migración sin aplicar en `admind_db`** (`showmigrations`, 13/10): `reservas/0006` y `casos/0004`, las del dashboard, ya están. **Pero** `makemigrations --check` ya no sale limpio: pide `personas/0003` porque Camilo editó la `personas/0002` después de aplicada y la restricción del teléfono del modelo no la acompañó. La base conserva `telefono` en `varchar(10)` y la restricción de 7 a 10 dígitos ([personas](../05_Modulos/personas.md)) |
| **Pruebas del backend** | **708, todas pasan** (47 s). La prueba del intruso sigue en verde ([pruebas_y_ejecucion](../02_Arquitectura/pruebas_y_ejecucion.md)) |
| **Pruebas del frontend** | **417, todas pasan** (9 s) |
| **Historias con código** | **21 construidas (105 SP)**, 2 parciales (HU-27 y HU-33, 8 SP) y **15 sin empezar (75 SP)**, de 38 historias y 188 SP. Aparte: HU-39 (primera parte construida, sin puntos) y HU-40 (solo en Notion). Detalle en [historias](historias.md). Lo que Camilo subió el 12/10 de HU-15 y HU-18 no se ha comparado con sus criterios |
| **Sin historia** | El ingreso a zonas con aforo ([ingresos](../05_Modulos/ingresos.md)) está construido y no tiene historia ni número |
| **Planes** | Ninguno activo. Los once escritos están ejecutados, con commit y migraciones aplicadas ([planes](../07_Planes/planes.md)) |
| **Plazo** | Entrega cerca del 2026-10-21: el profesor la amplió una semana (Alejo, 2026-10-13); antes era cerca del 14/10. Fecha exacta sin confirmar. No hay que entregar las 38 historias ([backlog_y_plazo](backlog_y_plazo.md)) |

## Historias por grupo

La columna *Sprint* es el reparto previsto en el Excel V11.1, que ya no se cumple con el plazo de un mes.

| Sprint | Historias | SP | Con código | Sin empezar |
|---|---|---|---|---|
| **1** | HU-01 a HU-05, HU-26 | 25 | 6 de 6 | — |
| **2** | HU-06 a HU-09 | 20 | 4 de 4 | — |
| **3** | HU-10 a HU-13 | 26 | 4 de 4 | — |
| **4** | HU-14 a HU-19 | 28 | HU-14 y HU-16 (12 SP) | HU-15, HU-17, HU-18, HU-19 |
| **5** | HU-20, 21, 25, 27, 28, 29 | 28 | HU-21, HU-25, HU-28 y HU-29 (18 SP); HU-27 parcial | HU-20 |
| **6** | HU-22 a HU-24, HU-30 a HU-34 | 38 | HU-33 parcial | HU-22 a HU-24, HU-30 a HU-32, HU-34 |
| **7** | HU-35, 36, 37 | 16 | HU-35 (4 SP) | HU-36, HU-37 |
| Condicional | HU-38 | 7 | — | HU-38 |

Lo que cambió respecto a lo que dice Notion o el Excel:

- **HU-06:** un solo rol por conjunto desde el 29/09, y sin rol Consejo ([permisos](../05_Modulos/permisos.md)). Su criterio todavía dice varios roles.
- **HU-09, HU-10 y HU-13:** el motor de reglas por niveles del 06/10 ([motor_reglas](../05_Modulos/motor_reglas.md)). Sus criterios describen el modelo anterior.
- **HU-03:** siete pasos y seis requisitos desde el 06/10 ([conjuntos](../05_Modulos/conjuntos.md)).
- **HU-14:** Camilo la construyó el 05/10 y el 13/10 se completó: comparada con sus cinco criterios de Notion, los cumple todos. La Secretaría dejó de aprobar ([reservas](../05_Modulos/reservas.md)).
- **HU-29:** Camilo subió los casos el 12/10 y el 13/10 se les dio el ciclo completo. En Notion la tarea del tablero de tres columnas ya no describe lo construido: es una tabla con pestañas ([triage](../05_Modulos/triage.md)).

## Lo que frena para cerrar historias

La lista completa, ordenada por tipo, está en [pendientes](pendientes.md). Lo que más pesa:

- [ ] **El teléfono quedó a medias** (Camilo, 13/10): el campo y la migración dicen 15, la restricción del modelo y el formulario del front siguen en 7 a 10, y `makemigrations --check` falla. Alejo había pedido 10 el mismo día ([pendientes](pendientes.md), secciones 3 y 8).
- [ ] **La baja del conjunto** que subió Camilo el 13/10 no deja auditoría, no pide la doble confirmación escrita del diseño y el Superusuario sigue viendo y puede volver a entrar a un conjunto dado de baja ([pendientes](pendientes.md), sección 5).
- [ ] **El backend no tiene rama `pruebas` en GitHub** (existe solo en local). Sin ella no se abre ningún PR `desarrollo → pruebas`.
- [ ] **Ninguna prueba manual está hecha.** Cada plan trae su guion; le toca a quien no programó.
- [ ] **Avisarle a Camilo** de los cambios del 06/10 al 11/10: migraciones, permisos nuevos, apps nuevas y su app `visitantes`, que cambió. En la bóveda no consta que se haya hecho.
- [ ] **Lo legal sin verificar** de las zonas con ingreso y de la mora ([abiertas](../06_Decisiones/abiertas.md) 12.10 b). La pantalla de Vigilancia sigue con el aviso de finalidad como marcador.
- [ ] **Decidir el alcance** que entra antes de la entrega ([abiertas](../06_Decisiones/abiertas.md) 12.8).
- [ ] **Notion:** HU-21 y HU-25 figuran «Finalizado» sin la DoD, y los estados de los sprints no coinciden con el código.
- [ ] **Llevar al texto de diseño** las decisiones tomadas al construir, que hoy solo están avisadas al inicio de cada nota.

## Ver también

- [historias](historias.md) — las historias una por una, con su módulo y su plan
- [pendientes](pendientes.md) — todo lo que falta, por tipo
- [bitacora](bitacora.md) — qué pasó y cuándo
- [mapa_codigo](../02_Arquitectura/mapa_codigo.md) — qué hay en cada app
- [backlog_y_plazo](backlog_y_plazo.md) — el plan original, la velocidad y el plazo
