---
resumen: "Lista de planes de trabajo: cuáles están activos y cuáles ya se ejecutaron, con la historia que cubre cada uno y la nota donde quedó lo vigente."
tipo: plan
origen: "reorganización del 2026-09-30; revisada contra el código el 2026-10-11"
actualizado: 2026-10-13
revisado: 2026-10-13
---

# Planes

Cómo se escribe y se cierra uno: [abrir_y_cerrar_un_plan](../09_Protocolos/abrir_y_cerrar_un_plan.md).

## Activos

**Ninguno.** `activos/` está vacía: los once planes escritos están ejecutados.

Los diez primeros tienen commit y sus migraciones aplicadas en `admind_db`; al del dashboard (13/10) le faltan las dos cosas.

Lo que sigue sin plan está en [pendientes](../08_Estado/pendientes.md), sección 9. Qué entra antes de la entrega sigue sin decidir ([abiertas](../06_Decisiones/abiertas.md), 12.8).

## Hechos

Un plan hecho es histórico y no se edita: menciona el rol Consejo, alfa y beta con el sentido anterior y otras cosas que cambiaron después. **Lo vigente está en la nota de la última columna** y en [construccion](../06_Decisiones/construccion.md). A todos les falta lo mismo: la prueba manual con el guion que trae cada uno ([pendientes](../08_Estado/pendientes.md), sección 2).

| Plan | Ejecutado | Historia | Qué cubrió | Lo vigente |
|---|---|---|---|---|
| [Admind_Plan_Sprints_2_3](hechos/Admind_Plan_Sprints_2_3.md) | 2026-09-27 | HU-06 a HU-13 | Roles, vínculos, áreas, reglas, bloqueo, confirmación y envío, más la auditoría mínima. Fases F0 a F10. Trae las decisiones D1 a D12, las menores P1 a P15 y el guion de prueba manual (§6) | [permisos](../05_Modulos/permisos.md), [unidades](../05_Modulos/unidades.md), [reservas](../05_Modulos/reservas.md), [invariantes](../03_Reglas/invariantes.md) |
| [Plan_Recuperacion_Contrasena](hechos/Plan_Recuperacion_Contrasena.md) | 2026-10-05 | HU-01 | Límite de 3 enlaces por hora y correo, correo real por SMTP y pruebas del front de las dos pantallas. F0 a F4, D1 a D6. Mixto: F0, F1 y F4 guiadas | [cuentas](../05_Modulos/cuentas.md) |
| [Plan_Anuncios_Con_Fotos](hechos/Plan_Anuncios_Con_Fotos.md) | 2026-10-05 | HU-25 | Publicar un anuncio con texto y hasta 4 fotos, y verlas en el tablón. F0 a F4, D1 a D8 y las menores P1 a P16. No fue guiado | [triage](../05_Modulos/triage.md) |
| [Plan_Estructura_De_Viviendas](hechos/Plan_Estructura_De_Viviendas.md) | 2026-10-06 | HU-39, primera parte | Agrupaciones, generador de viviendas con vista previa, su API y el paso «Viviendas» del asistente, con conjuntos mixtos y el requisito para quedar operativo. F0 a F4, D1 a D5 en a | [unidades](../05_Modulos/unidades.md) |
| [Plan_Motor_De_Reglas](hechos/Plan_Motor_De_Reglas.md) | 2026-10-06 | HU-09, HU-10, HU-13 | El motor por niveles para las áreas con reserva: aforo obligatorio en el área, reglas del conjunto (alfa) y del área (beta) una sola vez por tipo, descripción fija, días que no abre con motivo y el tablero de reglas. F0 a F5, D1 a D4 en a | [motor_reglas](../05_Modulos/motor_reglas.md) |
| [Plan_Asistente_De_Creacion](hechos/Plan_Asistente_De_Creacion.md) | 2026-10-06 | HU-03 y lo mínimo de HU-33 | El paso del reglamento en PDF, los requisitos para quedar operativo y el resumen de siete pasos. Dice en qué orden iban los tres planes del 06/10. F0 a F3; D1 en b, D2 a D5 en a | [conjuntos](../05_Modulos/conjuntos.md) |
| [Plan_Zonas_Con_Ingreso](hechos/Plan_Zonas_Con_Ingreso.md) | 2026-10-08 | Sin historia | El segundo modo de uso de una zona: modo de uso y permanencia en el área, regla de acompañantes, registro de entrada y salida por Vigilancia con aforo simultáneo, cupos a la vista y pantallas por rol. F0 a F7, D1 a D9. No fue guiado. Construido sin verificar lo legal (D3 a) | [ingresos](../05_Modulos/ingresos.md) |
| [Plan_Pago_De_Reserva](hechos/Plan_Pago_De_Reserva.md) | 2026-10-10 | HU-16 | Administración declara el pago de una reserva, con comprobante opcional; el residente puede subir el suyo; el archivo se valida por su firma y se sirve por una ruta validada. F0 a F4, D1 a D7 | [reservas](../05_Modulos/reservas.md) |
| [Plan_Parqueadero_De_Visitantes](hechos/Plan_Parqueadero_De_Visitantes.md) | 2026-10-10 | HU-28 y parte de HU-27 | Catálogo de parqueaderos con código, ocupación atada a la visita y liberación al registrar la salida; incluye la salida del visitante y la capa de servicio de `visitantes`. F0 a F5, D1 a D8 | [parqueaderos](../05_Modulos/parqueaderos.md) |
| [Plan_Pago_De_Administracion](hechos/Plan_Pago_De_Administracion.md) | 2026-10-10 | HU-35 | Tabla por vivienda y mes con buscador, check que pone Administración, comprobante que sube el residente y la mora que alimenta *paz y salvo* (F5, construida sin verificar lo legal). F0 a F5, D1 a D10 | [pagos](../05_Modulos/pagos.md) |
| [Plan_Dashboard_De_Solicitudes](hechos/Plan_Dashboard_De_Solicitudes.md) | 2026-10-13 | HU-14 y HU-29 | El dashboard de gestión con pestañas (Reservas, Casos y Citas sin función): categoría de rechazo, descarte de Secretaría, aviso al residente y orden por antigüedad; el ciclo completo de los casos sobre lo que subió Camilo; y la Secretaría deja de aprobar. F0 a F5, D1 a D9. Lo construyó el agente | [reservas](../05_Modulos/reservas.md), [triage](../05_Modulos/triage.md), [permisos](../05_Modulos/permisos.md) |

Los seis planes del 06/10 y del 10/10 se escribieron como guiados y Alejo pidió en todos que **los construyera el agente**; el de zonas con ingreso (08/10) no era guiado.

## Si se abre uno nuevo

Dos planes en dos chats a la vez se pisan en `config/`, `apps/permisos/catalogo.py`, el lateral del front y `tests/aislamiento/test_intruso.py`. La validación de un archivo por su firma ya existe en `apps/comun/archivos/comprobantes.py`: se reutiliza, no se crea otra.

## Ver también

- [abrir_y_cerrar_un_plan](../09_Protocolos/abrir_y_cerrar_un_plan.md) — cómo se abre, se ejecuta y se cierra
- [Inicio](../Inicio.md) — el arranque de un chat de planeación
- [historias](../08_Estado/historias.md) — de la historia a su plan
- [pendientes](../08_Estado/pendientes.md) — las pruebas manuales de cada plan y lo que sigue sin plan
