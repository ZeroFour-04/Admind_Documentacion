---
resumen: "Tabla de equivalencias: en qué nota quedó cada sección del documento maestro y cada documento anterior."
tipo: indice
origen: "maestro v1.4 (2026-09-14), partido en notas el 2026-09-30"
actualizado: 2026-09-30
---

# AdMind — Documento maestro (tabla de equivalencias)

Hasta el 2026-09-30 este archivo era un solo documento de 1.166 líneas. Su contenido vive ahora en notas cortas. Aquí se resuelve cualquier cita del tipo *maestro §5.4*, *R12* o *decisión 24* que aparezca en el código, en los README o en otras notas.

El texto de cada sección se movió tal cual. Cuando una decisión posterior lo contradice, la nota lo avisa al inicio.

## Secciones del maestro

| § | Tema | Nota |
|---|---|---|
| 1 | Qué es AdMind, pilares, diferenciador | [que_es_admind](01_Contexto/que_es_admind.md) |
| 2 | El equipo | [equipo](01_Contexto/equipo.md) |
| 3, 3.1–3.4 | Alcance en cuatro niveles | [alcance](01_Contexto/alcance.md) |
| 4, 4.1–4.3 | Restricciones legales | [legal](01_Contexto/legal.md) |
| 5.1 | Flujo de reserva | [reservas](05_Modulos/reservas.md) |
| 5.2 | Identidad de personas | [personas](05_Modulos/personas.md) |
| 5.3 | Roles y permisos | [permisos](05_Modulos/permisos.md) |
| 5.4 | Blindaje de datos | [aislamiento](03_Reglas/aislamiento.md) |
| 5.5 | Vínculos de unidad | [unidades](05_Modulos/unidades.md) |
| 5.6 | Parqueaderos | [parqueaderos](05_Modulos/parqueaderos.md) |
| 5.7 | Secretaría y triage | [triage](05_Modulos/triage.md) |
| 5.8 | Infracciones | [infracciones](05_Modulos/infracciones.md) |
| 5.9 | Citas con el administrador | [citas](05_Modulos/citas.md) |
| 5.10 | Motor de reglas | [motor_reglas](05_Modulos/motor_reglas.md) |
| 5.11 | Invariantes de eliminación | [eliminacion](03_Reglas/eliminacion.md) |
| 6, 6.1–6.6 | Sistema visual | [sistema_visual](04_Diseno/sistema_visual.md) |
| 7, 7.1, 7.2 | Stack técnico | [stack](02_Arquitectura/stack.md) |
| 7.3 | Proyecto espejo, rama `lab` | [Maestro_7.3_rama_lab](Archivo/Lab/Maestro_7.3_rama_lab.md) |
| 8.1 | Scrum y Definition of Done | [scrum_y_dod](03_Reglas/scrum_y_dod.md) |
| 8.2 | Repositorios y documentación | [repositorios](02_Arquitectura/repositorios.md) |
| 8.3 | Compatibilidad Obsidian ↔ GitHub | [documentacion](03_Reglas/documentacion.md) |
| 8.4 | Disciplina de trabajo con IA | [trabajo_con_ia](03_Reglas/trabajo_con_ia.md) |
| 8.5 | Modelo de ramas | [git](03_Reglas/git.md) |
| 9 | Decisiones cerradas | [cerradas](06_Decisiones/cerradas.md) |
| 10 | Riesgos vivos | [riesgos](06_Decisiones/riesgos.md) |
| 11, 11.1–11.6 | Estado de ejecución y backlog | [backlog_y_plazo](08_Estado/backlog_y_plazo.md) |
| 12, 12.1–12.8 | Contradicciones abiertas | [abiertas](06_Decisiones/abiertas.md) |
| 13 | Decidido y propuesto | [decidido_y_propuesto](06_Decisiones/decidido_y_propuesto.md) |
| 14 | Control de cambios | [Maestro_control_de_cambios](Archivo/Maestro_control_de_cambios.md) |

## Identificadores

| Identificador | Qué es | Nota |
|---|---|---|
| R1 a R14 | Riesgos vivos | [riesgos](06_Decisiones/riesgos.md) |
| Decisión 1 a 30 | Decisiones cerradas de diseño (también citadas como *§9: 11* o *ADR*) | [cerradas](06_Decisiones/cerradas.md) |
| D1 a D12 | Decisiones que Alejo tomó para el plan de los Sprints 2 y 3 | [construccion](06_Decisiones/construccion.md); el texto completo, en `07_Planes/hechos/Admind_Plan_Sprints_2_3.md` §2 |
| P1 a P15 | Decisiones menores que fijó ese plan | `07_Planes/hechos/Admind_Plan_Sprints_2_3.md` §3 |
| F0 a F10 | Fases de ese plan | `07_Planes/hechos/Admind_Plan_Sprints_2_3.md` |
| HU-01 a HU-38 | Historias de usuario | [historias](08_Estado/historias.md) |
| M1 a M6 | Criterios del proyecto espejo | [Maestro_7.3_rama_lab](Archivo/Lab/Maestro_7.3_rama_lab.md) |
| `REQ-<MODULO>-<NN>` | Requisitos de la guía legal v1.0, que no está en esta bóveda | [legal](01_Contexto/legal.md) |

## Documentos anteriores

| Documento | Dónde quedó |
|---|---|
| `Avance/Admind_Avance.md` §1 | [resúmenes de corte](Archivo/Avances/Admind_Avance_resumenes_de_corte.md) |
| `Admind_Avance.md` §2 | [inventario_codigo](08_Estado/inventario_codigo.md); §2.3, en [restricciones_bd](02_Arquitectura/restricciones_bd.md) |
| `Admind_Avance.md` §3 | [bitacora](08_Estado/bitacora.md) |
| `Admind_Avance.md` §4 | [construccion](06_Decisiones/construccion.md) |
| `Admind_Avance.md` §5 | [historias](08_Estado/historias.md) e [historias_evidencia](08_Estado/historias_evidencia.md) |
| `Admind_Avance.md` §6 | [pendientes](08_Estado/pendientes.md); los límites del aislamiento, en [aislamiento](03_Reglas/aislamiento.md) |
| `Admind_Avance.md` §7 | [actualizar_contexto](09_Protocolos/actualizar_contexto.md) |
| `AVANCE.md` (informe por sprints del 29/09) | [copia fechada](Archivo/Avances/Avance_por_sprints_2026-09-29.md); su contenido vigente, en [historias](08_Estado/historias.md) y [pendientes](08_Estado/pendientes.md) |
| `Avance/Avance 22092026.md` | `Archivo/Avances/` |
| `Avance/Informes/` | `Archivo/Informes/` |
| `Lab/Admind_Lab.md` §2, §8 y §9 | [trabajo_con_ia](03_Reglas/trabajo_con_ia.md); §4, en [entorno_local](02_Arquitectura/entorno_local.md); el resto, en `Archivo/Lab/` |
| `Lab/Admind_Seguimiento_Lab.md`, `Bitacora/Admind_Bitacora_Errores.md` | `Archivo/Lab/` |
| `Guias/Admind_Plan_Sprints_2_3.md` | `07_Planes/hechos/`; su §0.3, en [invariantes](03_Reglas/invariantes.md) |
| `Guias/Admind_Guia_Estructura_Actual.md` | Sigue en `Guias/` como tutorial. Sus secciones de referencia se copiaron a `02_Arquitectura/`, `04_Diseno/implementacion.md`, `05_Modulos/` y `08_Estado/estado_actual.md` |
| `Guias/Admind_Guia_Desarrollo.md` | Sigue en `Guias/` como tutorial. Sus reglas se copiaron a `03_Reglas/` (capas, reglas_frontend, lista_de_salida, git, trabajo_con_ia) |
| `Notas/`, `Sin título.md` | `Archivo/Notas/` |
| `Usuarios prueba.md` | `Credenciales/` |
