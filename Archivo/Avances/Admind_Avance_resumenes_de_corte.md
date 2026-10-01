---
resumen: "Resúmenes de corte del 15/09 y del 27/09 del antiguo Admind_Avance.md."
tipo: archivo
origen: "avance §1"
actualizado: 2026-09-27
---

# Resúmenes de corte del antiguo `Admind_Avance.md`

El resto de ese archivo se repartió el 2026-09-30 en `08_Estado/` y `06_Decisiones/construccion.md`.

**Corte: 2026-09-27, 17:35.** Un agente ejecutó `Guias/Admind_Plan_Sprints_2_3.md` de la Fase 0 a la 10, con las decisiones D1 a D12 en su opción recomendada (Alejo, 2026-09-27).

| Frente | Estado al 2026-09-27 |
|---|---|
| **Backend** | `desarrollo` en `66f8897`: 15 commits locales sobre `3c70e3a`, **sin subir**. Apps nuevas `auditoria`, `areas`, `reglas` y `reservas`, API de `personas` y `apps/comun/bloqueo/`. Migraciones nuevas aplicadas en `admind_db` (§2.5) |
| **Frontend** | `desarrollo` en `c1d8f6b`: 9 commits locales sobre `b42ce93`, **sin subir**. Pantallas reales de áreas, apartamentos, roles, registrar persona, reglas y reservas; Alpine.js 3.17.4 autoalojado (§2.5) |
| **Historias** | HU-06 a HU-13 con todos sus criterios en código y con prueba (§5.3). **Ninguna Terminada**: les falta la DoD humana (PR `desarrollo → pruebas` revisado y prueba manual de quien no la programó) |
| **Pruebas automáticas** | Backend: **300, todas pasan** (eran 171). Front: **109, todas pasan** (eran 51). `makemigrations --check` sin cambios |

> [!WARNING] Filas que esta sesión no tocó
> Lo que sigue de este archivo quedó en el corte del 2026-09-15 salvo las historias HU-06 a HU-13, la §2.5, la bitácora del 2026-09-27, las decisiones del plan y los pendientes marcados con esa fecha. Entre el 2026-09-15 y el 2026-09-25 se construyeron otras piezas (HU-01, HU-02, HU-03, HU-21, HU-25, HU-26…) que aquí siguen con su estado viejo. El punto de partida verificado de esta sesión está en el plan, §1.

**Corte anterior: 2026-09-15, 10:35.** Segundo día de desarrollo real dentro del plazo de un mes (entrega cerca del 2026-10-14, fecha exacta por confirmar; maestro §11).

| Frente | Estado |
|---|---|
| **Backend** | Django sobre PostgreSQL con `Persona`, `Usuario`, `Conjunto`, `Asignacion` y `TokenDeSesion`, el catálogo de roles y permisos en código y el aislamiento por conjunto. **Primeros endpoints:** inicio y cierre de sesión con token (`0b0c4f8`) y selector de conjunto activo con la prueba del intruso (`d9b6271`). Todo en el remoto |
| **Frontend** | Proyecto Django con **ingreso y salida funcionales** contra la API y maquetas del resto de pantallas, a partir del borrador de Alejo. En `557bc9f`, en el remoto (§2.4) |
| **Historias** | **0 de 38 terminadas (0 de 188 SP).** Siete en progreso: HU-04 y HU-05 con todas sus tareas (les falta la DoD); HU-01 con 4 de 5; HU-06 y HU-26 con 3 de 5; HU-02 y HU-03 con 1 de 5 |
| **Plan técnico del Sprint 1** | Pasos 1 a 6 de 8 hechos (§4), el último en `d9b6271`. Sigue el paso 7, HU-03 mínima, con el alcance por decidir (§6) |
| **Sprint 1** | Sin iniciar formalmente. Qué entra en el mes y en cuántos sprints sigue abierto (maestro §12.8) |
| **Pruebas automáticas** | Backend: **69, todas pasan** (`pytest` sobre `d9b6271`, corrido el 2026-09-15 09:25). En `0b0c4f8` eran 48. Front: **ninguna en el repositorio**; el login se verificó con un script aparte (§3) |

> [!NOTE] Por qué 0 SP con siete historias avanzadas
> El método de velocidad acordado con el docente (maestro §11.3) solo cuenta lo terminado: una historia al 80 % aporta 0 SP.
> Los mensajes de commit dicen *"HU 04 completada"* (`dc6a414`), *"[HU-03] [HU-05] [HU-06] hechos"* (`531e854`) y *"Token de inicio de sesion y HU1"* (`0b0c4f8`). **Ninguna historia cumple la DoD** (maestro §8.1). HU-04 y HU-05 tienen todas sus tareas, pero les falta el PR `desarrollo → pruebas` revisado por Camilo y la prueba manual de quien no las programó; a HU-04 además le falta el criterio de la API. Detalle en §5.3.
