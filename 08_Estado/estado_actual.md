---
resumen: "Dónde está el proyecto hoy: commits, pruebas, migraciones, historias por grupo y lo que frena para cerrarlas."
tipo: estado
corte: 2026-10-11
origen: "verificado en los tres repositorios y en admind_db el 2026-10-11"
actualizado: 2026-10-13
revisado: 2026-10-11
---

# Estado actual

Esta nota dice **cómo está hoy**. Cómo se llegó aquí, día por día, está en [bitacora](bitacora.md).

> [!IMPORTANT] Dos formas de contar
> - **Con la Definition of Done** ([scrum_y_dod](../03_Reglas/scrum_y_dod.md)): ninguna historia está terminada, porque ninguna ha pasado por un PR `desarrollo → pruebas` revisado ni por la prueba manual de quien no la programó.
> - **En los informes al docente:** el informe 4 (2026-10-06), con un criterio menos estricto pedido por Alejo, cuenta Sprints 1 a 3, HU-14, HU-21 y HU-25: **17 historias, 89 SP**. Está en `Archivo/Informes/2026-10-06/`.

## Resumen (corte 2026-10-11)

| Qué | Cómo está |
|---|---|
| **Backend** (la API) | Rama `desarrollo` en **`87d67c5`** («limitar nombre de conjunto, nombres, apellidos y teléfono», 13/10), igual a `origin/desarrollo`. Sobre `0b627d1` de Camilo («sprint 4,5 y casos», 12/10) van el cambio de modo de uso de un área (`287621c`) y los límites de texto (`87d67c5`). 17 apps con código más `comun`; 4 solo con README (`citas`, `infracciones`, `triage`, `importacion_respaldo`). El conteo de rutas (71) es anterior a `casos` y a las campañas de reserva |
| **Frontend** (las pantallas) | Rama `desarrollo` en **`0adf5eb`** («ocultar «Reglas» del menú de Vigilancia», 13/10), igual a `origin/desarrollo`. Sobre `7cd762c` de Camilo («Sprint 4,5 y casos», 12/10) van el cambio de modo de uso (`6c61ac4`), los límites de texto (`7121d94`) y el menú de Vigilancia (`0adf5eb`). 15 apps con pantallas, más `casos` |
| **Documentación** | Rama `main` en `7566556`, igual a `origin/main`. La reorganización del 11/10 ([bitacora](bitacora.md)) está sin commit |
| **Base de datos** | **Cinco migraciones sin aplicar en `admind_db`**, todas de Camilo: `areas/0006_area_condiciones_alquiler`, `reservas/0005_campana` y `casos/0001` a `0003`. Hasta correr `migrate`, el área sin la columna `condiciones_alquiler` rompe en tiempo de ejecución. Los límites de texto (`conjuntos/0005`, `personas/0002`) sí están aplicados. `makemigrations --check` no encuentra cambios |
| **Pruebas del backend** | **672: 670 pasan y 2 fallan** (85 s). Las dos ya fallaban en `origin/desarrollo` `0b627d1` sola, es decir, vienen del commit de Camilo: `test_el_detalle_de_solicitud_incluye_condiciones_de_renta_de_su_area` (`reservas/tests.py` hace `salon.save()` sin conjunto activo) y `test_toda_ruta_de_la_api_esta_cubierta` (rutas nuevas sin registrar en la prueba del intruso) ([pruebas_y_ejecucion](../02_Arquitectura/pruebas_y_ejecucion.md)) |
| **Pruebas del frontend** | **397, todas pasan** (14 s) |
| **Historias con código** | **20 construidas (100 SP)**, 2 parciales (HU-27 y HU-33, 8 SP) y **16 sin empezar (80 SP)**, de 38 historias y 188 SP. Aparte: HU-39 (primera parte construida, sin puntos) y HU-40 (solo en Notion). Detalle en [historias](historias.md) |
| **Sin historia** | El ingreso a zonas con aforo ([ingresos](../05_Modulos/ingresos.md)) está construido y no tiene historia ni número |
| **Planes** | Ninguno activo. Los diez escritos están ejecutados ([planes](../07_Planes/planes.md)) |
| **Plazo** | Entrega cerca del 2026-10-21: el profesor la amplió una semana (Alejo, 2026-10-13); antes era cerca del 14/10. Fecha exacta sin confirmar. No hay que entregar las 38 historias ([backlog_y_plazo](backlog_y_plazo.md)) |

## Historias por grupo

La columna *Sprint* es el reparto previsto en el Excel V11.1, que ya no se cumple con el plazo de un mes.

| Sprint | Historias | SP | Con código | Sin empezar |
|---|---|---|---|---|
| **1** | HU-01 a HU-05, HU-26 | 25 | 6 de 6 | — |
| **2** | HU-06 a HU-09 | 20 | 4 de 4 | — |
| **3** | HU-10 a HU-13 | 26 | 4 de 4 | — |
| **4** | HU-14 a HU-19 | 28 | HU-14 y HU-16 (12 SP) | HU-15, HU-17, HU-18, HU-19 |
| **5** | HU-20, 21, 25, 27, 28, 29 | 28 | HU-21, HU-25 y HU-28 (13 SP); HU-27 parcial | HU-20, HU-29 |
| **6** | HU-22 a HU-24, HU-30 a HU-34 | 38 | HU-33 parcial | HU-22 a HU-24, HU-30 a HU-32, HU-34 |
| **7** | HU-35, 36, 37 | 16 | HU-35 (4 SP) | HU-36, HU-37 |
| Condicional | HU-38 | 7 | — | HU-38 |

Lo que cambió respecto a lo que dice Notion o el Excel:

- **HU-06:** un solo rol por conjunto desde el 29/09, y sin rol Consejo ([permisos](../05_Modulos/permisos.md)). Su criterio todavía dice varios roles.
- **HU-09, HU-10 y HU-13:** el motor de reglas por niveles del 06/10 ([motor_reglas](../05_Modulos/motor_reglas.md)). Sus criterios describen el modelo anterior.
- **HU-03:** siete pasos y seis requisitos desde el 06/10 ([conjuntos](../05_Modulos/conjuntos.md)).
- **HU-14:** construida por Camilo el 05/10, pero comparada el 11/10 con sus cinco criterios de Notion no cumple ninguno entero.
- **HU-29:** en Notion lleva dos tareas finalizadas y no hay código suyo en el repositorio.

## Lo que frena para cerrar historias

La lista completa, ordenada por tipo, está en [pendientes](pendientes.md). Lo que más pesa:

- [ ] **La prueba que falla.** `desarrollo` sube con un test en rojo. Faltan en `tests/aislamiento/test_intruso.py` cinco rutas: `usuario-perfil` y `usuario-eliminar` (29/09) y `solicitudes-bandeja`, `solicitudes-area` y `solicitud-decision` (HU-14).
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
