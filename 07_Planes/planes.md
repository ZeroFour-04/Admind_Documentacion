---
resumen: "Lista de planes de trabajo: cuáles están activos y cuáles ya se ejecutaron."
tipo: plan
origen: "reorganización del 2026-09-30"
actualizado: 2026-10-11
---

# Planes

Cómo se escribe y se cierra uno: [abrir_y_cerrar_un_plan](../09_Protocolos/abrir_y_cerrar_un_plan.md).

## Activos

| Plan | Qué cubre | Abierto | Estado |
|---|---|---|---|
| [Plan_Estructura_De_Viviendas](activos/Plan_Estructura_De_Viviendas.md) | HU-39, primera parte: agrupaciones, generador de viviendas con vista previa, su API y el paso «Viviendas» del asistente, con conjuntos mixtos y el requisito para quedar operativo. Fases F0 a F4, guiado | 2026-10-06 | **Construido por el agente el 2026-10-06** (F0 a F4, D1 a D5 en a), ya con commit y migrado (verificado el 2026-10-11). Falta de Alejo: la prueba manual y los avisos a Camilo; con eso se cierra y pasa a *Hechos* |
| [Plan_Motor_De_Reglas](activos/Plan_Motor_De_Reglas.md) | El motor de reglas de la definición del 2026-10-06, para las áreas con reserva: aforo obligatorio en el área, reglas del conjunto (alfa) y del área (beta) una sola vez por tipo, descripción fija de cada una, días que no abre con motivo y el tablero de reglas. Fases F0 a F5, guiado. No incluye el ingreso a zonas | 2026-10-06 | **Construido por el agente el 2026-10-06** (F0 a F5, D1 a D4 en a), ya con commit y migrado (verificado el 2026-10-11). Falta la prueba manual; con eso se cierra y pasa a *Hechos* |
| [Plan_Asistente_De_Creacion](activos/Plan_Asistente_De_Creacion.md) | El asistente de creación completo (HU-03): dice en qué orden van los tres planes y construye lo que faltaba, que es el paso del reglamento en PDF (lo mínimo de HU-33), los requisitos para quedar operativo y el resumen de siete pasos. Fases F0 a F3, guiado | 2026-10-06 | **Construido por el agente el 2026-10-06** (F0 a F3; D1 en b, D2 a D5 en a), ya con commit y migrado (verificado el 2026-10-11). Falta de Alejo: la prueba manual y los avisos a Camilo; con eso se cierra y pasa a *Hechos* |

Los tres planes del 2026-10-10 no dependían uno del otro y ya se ejecutaron los tres, el de la reserva, el del parqueadero y el pago de administración. Tocan archivos distintos, salvo `config/`, `apps/permisos/catalogo.py`, el lateral del front y `tests/aislamiento/test_intruso.py`: si se ejecutan en dos chats a la vez, se pisan ahí. Los dos de pagos comparten además la validación del comprobante (`apps/comun/archivos/comprobantes.py`): **ya existe** desde que se construyó el de reserva, y [Plan_Pago_De_Administracion](hechos/Plan_Pago_De_Administracion.md) la reutiliza en vez de crearla.

**Orden de los tres planes del asistente:** viviendas; F1 y F2 del asistente (con eso un conjunto ya puede quedar operativo); motor de reglas; F3 del asistente. Lo único fijo es que viviendas va antes del asistente y el motor antes de su F3.

El siguiente paso natural del núcleo es HU-14 (aprobar o rechazar una solicitud), pero qué entra antes de la entrega sigue sin decidir ([abiertas](../06_Decisiones/abiertas.md), 12.8).

## Hechos

| Plan | Qué cubrió | Ejecutado |
|---|---|---|
| [Admind_Plan_Sprints_2_3](hechos/Admind_Plan_Sprints_2_3.md) | HU-06 a HU-13 y la auditoría mínima, en las fases F0 a F10. Trae las decisiones D1 a D12, las menores P1 a P15 y el guion de prueba manual (§6) | 2026-09-27 |
| [Plan_Recuperacion_Contrasena](hechos/Plan_Recuperacion_Contrasena.md) | La recuperación de contraseña de HU-01: límite de 3 enlaces por hora y correo, correo real por SMTP y pruebas del front de las dos pantallas. Fases F0 a F4, decisiones D1 a D6 | 2026-10-05 |
| [Plan_Anuncios_Con_Fotos](hechos/Plan_Anuncios_Con_Fotos.md) | HU-25, ampliación: publicar un anuncio con texto y hasta 4 fotos, y verlas en el tablón. Fases F0 a F4, decisiones D1 a D8 y las menores P1 a P16; no fue guiado. Trae el guion de prueba manual, que sigue pendiente | 2026-10-05 |
| [Plan_Zonas_Con_Ingreso](hechos/Plan_Zonas_Con_Ingreso.md) | El segundo modo de uso de una zona, con ingreso: modo de uso y permanencia en el área, regla de acompañantes, registro de entrada y salida por Vigilancia con aforo simultáneo, cupos a la vista antes de reservar y pantallas separadas por rol. Fases F0 a F7 y decisiones D1 a D9; no fue guiado. Construido por el agente; ya con commit y migrado (verificado el 2026-10-11); trae el guion de prueba manual, que sigue pendiente | 2026-10-08 |
| [Plan_Pago_De_Administracion](hechos/Plan_Pago_De_Administracion.md) | HU-35, como submódulo Pagos / Pago de administración: tabla por vivienda y mes con buscador para Administración y Secretaría, check que pone Administración, comprobante que sube el residente y la mora que alimenta la regla de paz y salvo (F5, construida sin haber verificado lo legal: D3 b). Fases F0 a F5 y decisiones D1 a D10 (D5 a D10 en a). Plan guiado que Alejo pidió **construir al agente**; ya con commit y migrado (`pagos/0001`, `pagos/0002` y `reglas/0007`); trae el guion de prueba manual, que sigue pendiente | 2026-10-10 |
| [Plan_Parqueadero_De_Visitantes](hechos/Plan_Parqueadero_De_Visitantes.md) | HU-28: catálogo de parqueaderos con código, ocupación de un parqueadero de visitantes atada a la visita y liberación al registrar la salida; incluye la salida del visitante y la capa de servicio de `visitantes`, que le faltaban a HU-27. Fases F0 a F5 y decisiones D1 a D8 (D3 a D8 en a). Plan guiado que Alejo pidió **construir al agente**; ya con commit y migrado (`parqueaderos/0001`, `visitantes/0002` y `0003`); trae el guion de prueba manual, que sigue pendiente | 2026-10-10 |
| [Plan_Pago_De_Reserva](hechos/Plan_Pago_De_Reserva.md) | HU-16: Administración declara el pago de una reserva desde la tarjeta de la solicitud, con comprobante opcional; el residente puede subir el suyo; el archivo se valida por su firma y se sirve por una ruta validada. Todo en `reservas`. Fases F0 a F4 y decisiones D1 a D7 (D5 a, D6 a, D7 a). Plan guiado que Alejo pidió **construir al agente**; ya con commit y migrado (`reservas/0003` y `0004`); trae el guion de prueba manual, que sigue pendiente | 2026-10-10 |

Un plan hecho es histórico: menciona el rol Consejo y otras cosas que cambiaron después. Lo vigente está en [construccion](../06_Decisiones/construccion.md).
