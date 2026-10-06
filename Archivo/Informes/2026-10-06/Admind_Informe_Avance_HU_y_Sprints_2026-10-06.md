---
titulo: AdMind — Informe de avance por historias de usuario y sprints
fecha_corte: 2026-10-06
tipo: informe
fuentes:
  - "Lista de 38 HU de Notion (Gestión Scrum — AdMind → Historias de Usuario), entregada por Alejo el 2026-10-06"
  - "08_Estado/historias.md, estado_actual.md e historias_evidencia.md de esta bóveda"
tags:
  - informe
  - avance
---

# AdMind — Avance por historias de usuario y sprints

**Corte: 6 de octubre de 2026** · Entrega prevista: cerca del 14 de octubre (quedan 8 días; la fecha exacta sigue sin confirmar) · Total del backlog: **38 historias, 188 story points (SP)**.

> [!warning] Cómo leer los porcentajes
> El porcentaje de cada historia mide **cuánto del trabajo ya está construido y probado en el código**. No es lo mismo que "Terminada" según la Definition of Done (DoD) del equipo, que además exige un PR `desarrollo → pruebas` revisado y la prueba manual de quien no programó la historia. **Con ese criterio estricto, ninguna HU está terminada hoy** (ver sección 4).

## 1. Resumen

| Medida | Resultado |
|---|---|
| HU construidas por completo (código + pruebas, falta la DoD) | **16 de 38 (42 %)** |
| HU parciales | **2 de las 38**: HU-27 y HU-33 (más HU-39, que está fuera del backlog de Notion) |
| HU sin empezar | **20 de 38 (53 %)** |
| SP de las HU construidas por completo | **81 de 188 (43,1 %)** |
| SP contando también el avance parcial (estimado) | **≈ 83,9 de 188 (≈ 44,6 %)** |
| HU "Terminadas" con la DoD completa | **0 de 38 (0 %)** |
| Subtareas técnicas de HU-01 a HU-10 | **50 de 50 hechas (100 %)** |
| Sprints 1, 2 y 3 | **100 % construidos** (sin DoD) |
| Sprints 4, 6, 7 y condicional | **0 %** |
| Sprint 5 | **≈ 43 %** (adelantó HU-21, HU-25 y parte de HU-27) |

```
Sprint 1  ████████████████████ 100 %   25 SP
Sprint 2  ████████████████████ 100 %   20 SP
Sprint 3  ████████████████████ 100 %   26 SP
Sprint 4  ░░░░░░░░░░░░░░░░░░░░   0 %   28 SP
Sprint 5  ████████░░░░░░░░░░░░  43 %   28 SP
Sprint 6  ░░░░░░░░░░░░░░░░░░░░   2 %   38 SP
Sprint 7  ░░░░░░░░░░░░░░░░░░░░   0 %   16 SP
Condic.   ░░░░░░░░░░░░░░░░░░░░   0 %    7 SP
Total     █████████░░░░░░░░░░░  45 %  188 SP
```

## 2. Avance por sprint

El reparto es el previsto en el Excel V11.1. Con el plazo de un mes ya no se cumple por fechas: las historias se construyeron por tandas (Sprint 1 entre el 15 y el 21/09; Sprints 2 y 3 el 27/09; adelantos y ampliaciones hasta el 06/10). El porcentaje del sprint es **ponderado por SP**.

| Sprint | Historias | SP | HU completas | HU parciales | Sin empezar | SP completos | Avance del sprint |
|---|---|---|---|---|---|---|---|
| **1** | HU-01 a HU-05, HU-26 | 25 | 6 de 6 | 0 | 0 | 25 | **100 %** |
| **2** | HU-06 a HU-09 | 20 | 4 de 4 | 0 | 0 | 20 | **100 %** |
| **3** | HU-10 a HU-13 | 26 | 4 de 4 | 0 | 0 | 26 | **100 %** |
| **4** | HU-14 a HU-19 | 28 | 0 de 6 | 0 | 6 | 0 | **0 %** |
| **5** | HU-20, 21, 25, 27, 28, 29 | 28 | 2 de 6 (HU-21, HU-25) | 1 (HU-27) | 3 | 10 | **≈ 43 %** (35,7 % sin contar HU-27) |
| **6** | HU-22 a 24, HU-30 a 34 | 38 | 0 de 8 | 1 (HU-33) | 7 | 0 | **≈ 2 %** |
| **7** | HU-35, 36, 37 | 16 | 0 de 3 | 0 | 3 | 0 | **0 %** |
| **Condicional** | HU-38 | 7 | 0 de 1 | 0 | 1 | 0 | **0 %** |
| **Total** | 38 (+ HU-39 sin SP) | **188** | **16** | **2** (+ HU-39) | **20** | **81** | **≈ 44,6 %** |

Notas de cálculo:
- El avance parcial usa porcentajes **estimados** para HU-27 (40 %) y HU-33 (30 %). Con solo las HU completas el total es 43,1 %.
- HU-39 no entra en las sumas porque todavía no tiene SP ni sprint asignado en Notion.

### Estado de cada sprint frente a la DoD

| Sprint | Código | Prueba automática | Prueba manual de quien no lo programó | PR `desarrollo → pruebas` revisado | ¿Terminado con DoD? |
|---|---|---|---|---|---|
| 1 | Sí | Sí | Pendiente | Pendiente | No |
| 2 | Sí | Sí | Pendiente (guion en el plan de Sprints 2 y 3, §6) | Pendiente | No |
| 3 | Sí | Sí (HU-12: 3 de 5 criterios; los otros 2 son manuales) | Pendiente | Pendiente | No |

## 3. Avance por historia de usuario

Leyenda: ✅ construida por completo (falta la DoD) · 🟡 parcial · ⬜ sin empezar.

### Sprint 1 — 25 SP · 100 %

| HU | Historia | SP | Avance | Qué hay y qué falta |
|---|---|---|---|---|
| HU-01 | Inicio de sesión con correo y contraseña | 3 | ✅ **100 %** (5/5 tareas) | Login, token, recuperación de contraseña por correo (límite de 3 enlaces por hora y SMTP real desde el 05/10), pantalla y pruebas. Falta la DoD |
| HU-02 | Segundo factor (TOTP) | 5 | ✅ **100 %** (5/5) | TOTP con QR, 10 códigos de respaldo y, desde el 05/10, enlace por correo para quitarlo si se pierde la aplicación. Falta recorrerlo a mano con un correo real y la DoD |
| HU-03 | Asistente para crear un conjunto | 6 | ✅ **100 %** (5/5) | Completa el 06/10 (**sin commit**): siete pasos (datos, viviendas, administración, áreas, reglas, reglamento y resumen); un conjunto ya queda operativo. Falta la DoD y actualizar sus criterios en Notion, que describen el asistente anterior. Dejar operativo un conjunto aún no queda en la auditoría |
| HU-04 | Persona global única por documento | 3 | ✅ **100 %** (5/5) | Falta la DoD |
| HU-05 | Aislamiento de datos entre conjuntos | 2 | ✅ **100 %** (5/5) | Ya lo usan las tablas reales desde el 27/09. Falta la DoD |
| HU-26 | Selector de conjunto activo | 6 | ✅ **100 %** (5/5) | Conectado a la API. Falta la DoD |

### Sprint 2 — 20 SP · 100 %

| HU | Historia | SP | Avance | Qué hay y qué falta |
|---|---|---|---|---|
| HU-06 | Asignación de roles del catálogo fijo | 6 | ✅ **100 %** (5/5) | Desde el 29/09 es **un solo rol por conjunto**; su criterio en Notion y el Excel aún dicen varios roles. Falta la DoD |
| HU-07 | Vincular persona por documento | 3 | ✅ **100 %** (5/5) | Límite de 20 búsquedas por hora, contado por conjunto (falta decidir si debe ser global). Falta la DoD |
| HU-08 | Vínculos de unidad y notificaciones | 7 | ✅ **100 %** (5/5) | Falta la DoD |
| HU-09 | Catálogo de áreas comunes | 4 | ✅ **100 %** (5/5) | Desde el 06/10 el aforo máximo es obligatorio (**sin commit**). El modo de uso de la zona sigue sin construir. Falta la DoD |

### Sprint 3 — 26 SP · 100 %

| HU | Historia | SP | Avance | Qué hay y qué falta |
|---|---|---|---|---|
| HU-10 | Reglas beta de reserva | 9 | ✅ **100 %** (5/5) | Reconstruida el 06/10 por niveles (reglas del conjunto y del área), **sin commit**. Sus criterios en Notion describen el modelo anterior. Falta la DoD |
| HU-11 | Bloqueo exclusivo de 3 minutos | 7 | ✅ **100 %** | 5 de 5 criterios con prueba, incluida concurrencia con 10 hilos. Falta probar a mano el `sendBeacon` al cerrar la pestaña, y la DoD |
| HU-12 | Confirmación antes de enviar | 2 | ✅ **100 % construida** · 60 % probada automáticamente | 3 de 5 criterios con prueba automática; "corregir sin perder lo escrito" y "el reloj no se detiene" requieren prueba manual. La alta demanda depende de PB-24, que no existe |
| HU-13 | Envío de solicitud y motor alfa/beta | 8 | ✅ **100 %** | 6 de 6 criterios con prueba. La mora da siempre `False` hasta que exista HU-35; las reglas de piscina y cobro quedan fuera. Desde el 06/10 el evaluador junta reglas del sistema, aforo, y reglas del conjunto y del área (**sin commit**) |

### Sprint 4 — 28 SP · 0 %

| HU | Historia | SP | Avance |
|---|---|---|---|
| HU-14 | Bandeja del administrador: aprobar o rechazar | 8 | ⬜ **0 %** — es la que cierra el ciclo de la reserva: hoy una solicitud llega a `APARTADA` y ahí se queda |
| HU-15 | Condiciones del alquiler congeladas y versionadas | 4 | ⬜ **0 %** |
| HU-16 | Registro de pago declarado y comprobante | 4 | ⬜ **0 %** |
| HU-17 | Cancelación de reservas en firme | 3 | ⬜ **0 %** |
| HU-18 | Aviso de disponibilidad de franja (campana) | 6 | ⬜ **0 %** |
| HU-19 | Dos oportunidades por franja y aviso de última | 3 | ⬜ **0 %** |

### Sprint 5 — 28 SP · ≈ 43 %

| HU | Historia | SP | Avance | Qué hay y qué falta |
|---|---|---|---|---|
| HU-20 | Anulación de registros por el Superusuario | 5 | ⬜ **0 %** | |
| HU-21 | Identidad visual del conjunto: color y logo | 4 | ✅ **100 %** | Construida el 22/09; el 29/09 se amplió con color propio y foto 1:1. Falta la DoD |
| HU-25 | Anuncios con alcance de conjunto o vivienda | 6 | ✅ **100 %** | Construida el 22/09; el 05/10 se amplió con hasta 4 fotos por anuncio (**sin commit**). Falta la DoD |
| HU-27 | Registro de visitantes y vehículos | 5 | 🟡 **≈ 40 %** (estimado) | Hecho por Camilo el 01/10: registra el ingreso y lista los visitantes (solo Vigilancia registra). **Falta:** la salida, finalidad y retención de datos (Ley 1581), aviso a los residentes, capa de servicio y auditoría. No se comparó contra los criterios de Notion |
| HU-28 | Parqueadero de visitantes atado a la visita | 3 | ⬜ **0 %** | |
| HU-29 | Tablero de casos con respuesta obligatoria | 5 | ⬜ **0 %** | |

### Sprint 6 — 38 SP · ≈ 2 %

| HU | Historia | SP | Avance |
|---|---|---|---|
| HU-22 | Bandeja de triage de la Secretaría | 7 | ⬜ **0 %** |
| HU-23 | Prioridad sobre citas y casos | 5 | ⬜ **0 %** |
| HU-24 | Rechazo por causal formal de la Secretaría | 3 | ⬜ **0 %** |
| HU-30 | Registro y comunicación de infracciones | 4 | ⬜ **0 %** |
| HU-31 | Agendar cita dentro del horario de atención | 4 | ⬜ **0 %** |
| HU-32 | Cambio de horario con alternativas | 8 | ⬜ **0 %** |
| HU-33 | Repositorio de documentos vigentes | 3 | 🟡 **≈ 30 %** (estimado) — solo el reglamento del conjunto en PDF (06/10, **sin commit**), que es lo que exige HU-03. Falta: otros documentos, las actas y que el residente descargue |
| HU-34 | Asignación de parqueaderos de residentes | 4 | ⬜ **0 %** |

### Sprint 7 y condicional — 23 SP · 0 %

| HU | Historia | SP | Avance |
|---|---|---|---|
| HU-35 | Reporte de pago de administración | 4 | ⬜ **0 %** |
| HU-36 | Importación masiva con dry-run e idempotencia | 7 | ⬜ **0 %** |
| HU-37 | Respaldo de información por conjunto | 5 | ⬜ **0 %** |
| HU-38 | Registro de actividades sobre la auditoría (condicional) | 7 | ⬜ **0 %** |

### Historia fuera del backlog de Notion

| HU | Historia | SP | Avance |
|---|---|---|---|
| HU-39 | Estructura de viviendas: agrupaciones y generación en lote | Por estimar | 🟡 **≈ 70 %** (estimado: 6 de 9 criterios más el generador del 6) — primera parte construida el 06/10, **sin commit**. Falta la segunda parte: que las pantallas usen las palabras del conjunto (hoy "Apartamento" está fijo en unas 70 menciones de 12 plantillas), la confirmación al retirar y registrar a mano dentro de una agrupación. Nace de la retroalimentación del docente sobre HU-03 y HU-08; no está en Notion |

## 4. Tres formas de contar lo "completado"

| Criterio | HU completas | SP | % de los 188 SP |
|---|---|---|---|
| **Definition of Done completa** (PR revisado + prueba manual de otra persona) | 0 | 0 | **0 %** |
| **Como se reportó al docente el 29/09** (Sprints 1 y 2, HU-21 y HU-25; el Sprint 3, "en revisión") | 12 | 55 | **29,3 %** |
| **Construido en código y con pruebas** (este informe) | 16 | 81 | **43,1 %** (≈ 44,6 % con parciales) |

El método de velocidad acordado con el docente dice que **solo cuenta lo terminado** (una HU al 80 % aporta 0 SP). Con ese método, la velocidad medida hoy sería 0 SP; las cifras de esta tabla solo sirven para conocer el avance real de construcción.

## 5. Subtareas técnicas de Notion (HU-01 a HU-10)

Solo estas diez historias tienen subtareas cargadas en Notion: **50 de 50 hechas** (5 por historia).

| HU | Subtareas hechas | HU | Subtareas hechas |
|---|---|---|---|
| HU-01 | 5 / 5 | HU-06 | 5 / 5 |
| HU-02 | 5 / 5 | HU-07 | 5 / 5 |
| HU-03 | 5 / 5 | HU-08 | 5 / 5 |
| HU-04 | 5 / 5 | HU-09 | 5 / 5 |
| HU-05 | 5 / 5 | HU-10 | 5 / 5 |

Las casillas de Notion de HU-01, HU-02, HU-03 y HU-26 se marcaron el 15/09, cuando solo había parte hecha; conviene revisarlas contra el estado de arriba. De HU-11 a HU-38 la relación de tareas está vacía en esa base, así que su avance se midió contra los criterios de aceptación y las pruebas, no contra tareas.

## 6. Calidad y pruebas (reportado, no vuelto a ejecutar)

| Repositorio | Pruebas | Resultado |
|---|---|---|
| Backend (API) | 415 | 414 pasan, **1 falla** (`test_toda_ruta_de_la_api_esta_cubierta`: 5 rutas sin registrar en `tests/aislamiento/test_intruso.py`) |
| Frontend (pantallas) | 206 | Todas pasan |

Migraciones nuevas sin aplicar en `admind_db`: `areas/0004`, `reglas/0002` a `0004`, `unidades/0002_estructura` y `documentos/0001_initial`.

## 7. Qué frena cerrar historias

1. **Todo el trabajo del 06/10 está sin commit** (asistente completo de HU-03, estructura de viviendas de HU-39, reglamento de HU-33, aforo de HU-09 y fotos de HU-25). Hasta que se haga el commit y se suba, el avance real no está en GitHub.
2. **Arreglar la prueba que falla** del backend; hoy `desarrollo` sube con una prueba en rojo.
3. **Aplicar `migrate`** en `admind_db` y avisarle a Camilo (esta vez incluye un cambio al catálogo de permisos).
4. **Subir la rama `pruebas` del backend** a GitHub: existe solo en local y sin ella no se pueden abrir los PR `desarrollo → pruebas` que pide la DoD.
5. **Prueba manual** de HU-06 a HU-13 por quien no las programó.
6. **Decidir qué se entrega** antes del 14/10. El siguiente paso natural es **HU-14** (aprobar o rechazar), que cierra el ciclo de la reserva.
7. **Criterios en Notion desactualizados:** HU-03, HU-06, HU-09, HU-10 y HU-13 describen un modelo anterior al código actual.

## 8. Qué no se verificó

- **No se ejecutó nada en el código**: los repositorios de backend y frontend no están en este entorno. Los estados vienen de las notas `08_Estado/` (corte 05/10 y actualización del 06/10) y de la lista de Notion que entregó Alejo; las cifras de pruebas son las que esas notas registran.
- Los porcentajes de **HU-27, HU-33 y HU-39** son estimaciones de este informe, no un conteo de criterios de Notion.
- No se consultaron las tareas de la base "Tareas de Seguimiento Scrum 2.0", a donde las páginas de varias HU dicen que se migraron el 06/10.
- `historias_evidencia.md` conserva filas viejas (HU-01, 02, 03 y 26 al corte del 15/09); en este informe mandan `historias.md` y `estado_actual.md`.
