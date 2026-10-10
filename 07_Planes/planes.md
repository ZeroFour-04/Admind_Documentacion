---
resumen: "Lista de planes de trabajo: cuáles están activos y cuáles ya se ejecutaron."
tipo: plan
origen: "reorganización del 2026-09-30"
actualizado: 2026-10-08
---

# Planes

Cómo se escribe y se cierra uno: [abrir_y_cerrar_un_plan](../09_Protocolos/abrir_y_cerrar_un_plan.md).

## Activos

| Plan | Qué cubre | Abierto | Estado |
|---|---|---|---|
| [Plan_Estructura_De_Viviendas](activos/Plan_Estructura_De_Viviendas.md) | HU-39, primera parte: agrupaciones, generador de viviendas con vista previa, su API y el paso «Viviendas» del asistente, con conjuntos mixtos y el requisito para quedar operativo. Fases F0 a F4, guiado | 2026-10-06 | **Construido por el agente el 2026-10-06** (F0 a F4, D1 a D5 en a), sin commit. Falta de Alejo: `migrate` en `admind_db` (`unidades/0002_estructura`), los commits, la prueba manual y los avisos a Camilo; con eso se cierra y pasa a *Hechos* |
| [Plan_Motor_De_Reglas](activos/Plan_Motor_De_Reglas.md) | El motor de reglas de la definición del 2026-10-06, para las áreas con reserva: aforo obligatorio en el área, reglas del conjunto (alfa) y del área (beta) una sola vez por tipo, descripción fija de cada una, días que no abre con motivo y el tablero de reglas. Fases F0 a F5, guiado. No incluye el ingreso a zonas | 2026-10-06 | **Construido por el agente el 2026-10-06** (F0 a F5, D1 a D4 en a), sin commit. Falta B3.6, `migrate` en `admind_db`, que corre Alejo; con eso se cierra y pasa a *Hechos* |
| [Plan_Asistente_De_Creacion](activos/Plan_Asistente_De_Creacion.md) | El asistente de creación completo (HU-03): dice en qué orden van los tres planes y construye lo que faltaba, que es el paso del reglamento en PDF (lo mínimo de HU-33), los requisitos para quedar operativo y el resumen de siete pasos. Fases F0 a F3, guiado | 2026-10-06 | **Construido por el agente el 2026-10-06** (F0 a F3; D1 en b, D2 a D5 en a), sin commit. Falta de Alejo: `migrate` en `admind_db` (`documentos/0001_initial`), los commits, la prueba manual y los avisos a Camilo; con eso se cierra y pasa a *Hechos* |

**Orden de los tres planes del asistente:** viviendas; F1 y F2 del asistente (con eso un conjunto ya puede quedar operativo); motor de reglas; F3 del asistente. Lo único fijo es que viviendas va antes del asistente y el motor antes de su F3.

El siguiente paso natural del núcleo es HU-14 (aprobar o rechazar una solicitud), pero qué entra antes de la entrega sigue sin decidir ([abiertas](../06_Decisiones/abiertas.md), 12.8).

## Hechos

| Plan | Qué cubrió | Ejecutado |
|---|---|---|
| [Admind_Plan_Sprints_2_3](hechos/Admind_Plan_Sprints_2_3.md) | HU-06 a HU-13 y la auditoría mínima, en las fases F0 a F10. Trae las decisiones D1 a D12, las menores P1 a P15 y el guion de prueba manual (§6) | 2026-09-27 |
| [Plan_Recuperacion_Contrasena](hechos/Plan_Recuperacion_Contrasena.md) | La recuperación de contraseña de HU-01: límite de 3 enlaces por hora y correo, correo real por SMTP y pruebas del front de las dos pantallas. Fases F0 a F4, decisiones D1 a D6 | 2026-10-05 |
| [Plan_Anuncios_Con_Fotos](hechos/Plan_Anuncios_Con_Fotos.md) | HU-25, ampliación: publicar un anuncio con texto y hasta 4 fotos, y verlas en el tablón. Fases F0 a F4, decisiones D1 a D8 y las menores P1 a P16; no fue guiado. Trae el guion de prueba manual, que sigue pendiente | 2026-10-05 |
| [Plan_Zonas_Con_Ingreso](hechos/Plan_Zonas_Con_Ingreso.md) | El segundo modo de uso de una zona, con ingreso: modo de uso y permanencia en el área, regla de acompañantes, registro de entrada y salida por Vigilancia con aforo simultáneo, cupos a la vista antes de reservar y pantallas separadas por rol. Fases F0 a F7 y decisiones D1 a D9; no fue guiado, sin commits. Construido por el agente, sin commit ni `migrate`; trae el guion de prueba manual, que sigue pendiente | 2026-10-08 |

Un plan hecho es histórico: menciona el rol Consejo y otras cosas que cambiaron después. Lo vigente está en [construccion](../06_Decisiones/construccion.md).
