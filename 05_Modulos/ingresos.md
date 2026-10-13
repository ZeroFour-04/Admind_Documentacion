---
resumen: "Zonas con ingreso: vigilancia registra a quien entra, el aforo es simultáneo y la salida es manual o por tiempo. Construido el 2026-10-08 con salvaguardas legales (D3 a), sin historia y ya con commit; lo legal sigue sin verificar."
tipo: modulo
modulo: ingresos
hu: []
origen: "definición con Alejo en chat (2026-10-06) + Plan_Zonas_Con_Ingreso (2026-10-08)"
actualizado: 2026-10-13
revisado: 2026-10-11
---

# Ingreso a zonas con aforo

> [!IMPORTANT] Construido el 2026-10-08, sin historia y ya con commit
> Ninguna historia, de HU-01 a HU-39, la cubre. Alejo decidió el 2026-10-06 que se construye antes de la entrega; falta crear la historia y contárselo a Camilo.
>
> **Lo construyó el agente** con [Plan_Zonas_Con_Ingreso](../07_Planes/hechos/Plan_Zonas_Con_Ingreso.md), después de que Alejo eligió **D3 a**: construir con salvaguardas, **sin haber verificado** lo legal ([abiertas](../06_Decisiones/abiertas.md) 12.10 b). El texto del aviso de finalidad quedó como un marcador visible, porque no lo redacta el agente. Las migraciones están aplicadas en `admind_db` (verificado el 2026-10-11); falta la prueba manual.

## Qué es

Hay zonas que no se reservan con anticipación pero tampoco son de paso libre: el gimnasio, una piscina grande. Piden dos cosas: que quien entre quede registrado, y que nunca haya adentro más personas que el aforo.

Es el segundo **modo de uso** de una zona. El primero, con reserva, es el flujo de [reservas](reservas.md). Las zonas de paso libre (parques, zonas verdes) no entran al sistema.

## El recorrido

1. El vigilante elige la zona, escribe el número de documento del residente y cuántos acompañantes entran.
2. El sistema busca a esa persona **solo entre los residentes del conjunto activo** y muestra su nombre y su vivienda, para que el vigilante confirme (y elija la vivienda si vive en más de una).
3. El sistema valida todo junto y, si algo falla, dice **todos** los motivos: las reglas del sistema, las alfa y las beta de [motor_reglas](motor_reglas.md).
4. Si pasa, guarda el ingreso con su hora de salida prevista: la entrada más la permanencia máxima de la zona, sin pasar de la hora de cierre.
5. La salida la marca el vigilante cuando la persona se va, o la da el sistema al cumplirse el tiempo.

## Lo decidido

| Tema | Decisión |
|---|---|
| **Quién registra** | El rol Vigilancia, por ahora. Dos permisos (2026-10-08): `ingreso.registrar` para Vigilancia e `ingreso.ver_historico` para Administración, sensible |
| **Cómo se identifica** | Por número de documento. Si no es de un residente del conjunto activo, la respuesta es «no encontrado», exista o no esa persona en otro conjunto: la tabla de personas es global y no puede volverse un directorio. En el código una persona es única por tipo **y** número, así que dos pueden compartir número: llegan las dos y el vigilante elige |
| **Aforo** | Simultáneo: las personas adentro, más el residente y sus acompañantes que entran, no lo superan |
| **Acompañantes** | Los limita una regla alfa del conjunto, con un máximo **por vivienda a la vez** (`ACOMPANANTES`, desde 0; 0 es «no se permiten»). **Sin regla definida entran y el aforo es el único tope** (D8 a). Se asume que son visitantes. Solo se guarda cuántos son, sin enlazarlos con los visitantes de portería (HU-27) |
| **Salida** | Híbrida: manual por el vigilante, o automática al cumplirse la permanencia máxima |
| **Aviso al cumplirse el tiempo** | Al residente, por el canal de notificaciones; a vigilancia, en su pantalla («Se les cumplió el tiempo hoy»), no por correo |
| **Cuándo sale el aviso** | Al siguiente acceso al módulo, no en el minuto exacto. El conteo del aforo sí es exacto |
| **Paz y salvo** | Un solo interruptor para reservas e ingresos (D9): si el conjunto lo activa, una vivienda en mora no reserva ni ingresa. Sin efecto hasta que exista pagos (`mora.unidad_en_mora` responde siempre que no) |
| **Reingreso** | Al cumplirse el tiempo la persona puede volver a entrar si hay cupo (D9) |
| **La salida prevista** | Queda guardada: cambiar la permanencia del área no mueve la de un ingreso abierto (D9) |

## Cómo está construido (2026-10-08, ya con commit)

Una app `ingresos` en cada repositorio. Una sola tabla nueva.

- **`Ingreso`** (de conjunto): área, persona, vivienda, acompañantes, estado (`ADENTRO`, `SALIO`, `VENCIDO`), entrada, salida prevista, salida, quién registró la entrada y la salida, y la copia de la evaluación. **No guarda el documento**, solo la referencia a la persona. Un registro rechazado no deja fila. FK compuestas a área y vivienda.
- **Restricciones en la base** ([restricciones_bd](../02_Arquitectura/restricciones_bd.md)): índice único parcial `ingreso_uno_abierto_por_persona`, y tres `CHECK` (estado válido, salida prevista posterior a la entrada, salida vacía solo mientras está adentro).
- **El último cupo.** El aforo es una suma, no una fila única, así que no lo decide un índice: `registrar` toma la fila del área con `select_for_update`, da salida a los vencidos, cuenta y, si cabe, inserta. Dos registros a la misma zona pasan de a uno. Prueba propia en `tests/concurrencia/test_aforo_de_ingresos.py` (diez registros sobre el último cupo dejan uno solo adentro; la misma persona en dos zonas a la vez queda en una).
- **Reglas** (`apps/ingresos/evaluador.py`, propio): del sistema (vive en esa vivienda; zona con ingreso, activa y sin mantenimiento; dentro del horario; sin otro ingreso abierto), aforo, y las del conjunto y del área que aplican al modo (acompañantes, paz y salvo, días que no abre). Todas en AND, con todos los motivos. `reglas` no importa `ingresos`.
- **Salida automática al siguiente acceso**, sin procesos en segundo plano: toda lectura y toda acción empieza por `dar_salida_a_vencidos`, que pasa a `VENCIDO`, fija la salida prevista como `salida_en` y avisa al residente (`origen="ingreso"`, sin repetir). La salida automática no tiene actor.
- **La búsqueda** vive en `unidades.servicios.residentes_por_documento` y va por `POST`, para que el documento no viaje en la URL. Responde nombre y viviendas, sin teléfono, correo ni tipo de documento. Cada búsqueda queda en la auditoría, **sin el documento**.
- **La API** (`/ingresos/zonas/`, `/ingresos/residentes/buscar/`, `/ingresos/`, `/ingresos/<id>/salida/`): las vistas piden el permiso y nada más, sin revisar el rol por nombre. Los cupos son un conteo sin nombres. Quién está adentro lo ve solo quien registra; el historial, solo `ingreso.ver_historico`. Tabla completa en el `README.md` de la app.
- **Las pantallas:** «Ingreso a zonas» para Vigilancia (cupos por zona, registrar en dos pasos, «Adentro ahora» y «Se les cumplió el tiempo hoy»); «Ingresos» para Administración, con el historial filtrable por zona y por día y sin formulario; y, en «Zonas comunes», la tabla de todas las zonas con sus cupos antes de reservar. Sin JavaScript: los cupos se refrescan al recargar. Detalle en [frontend](../02_Arquitectura/frontend.md).
- **El área** gana `modo_uso` (`reserva` o `ingreso`) y `permanencia_maxima_minutos` (de 15 a 1 440). Un área con ingreso no se reserva: sin franjas y `409` al intentar tomar el bloqueo.
- **El modo se puede cambiar al editar el área** (2026-10-13, sin commit; antes era fijo). Si un área con ingreso pasa a ser con reserva, quien está adentro sigue adentro: «Adentro ahora», la salida manual y la salida por tiempo no miran el modo del área, y el área deja de aparecer en los cupos y de admitir registros nuevos. El detalle está en [motor_reglas](motor_reglas.md).

## Salvaguardas legales (D3 a)

El plan se construyó con estas salvaguardas, **sin** que lo legal estuviera verificado:

- Aviso de finalidad junto al formulario de Vigilancia. **Su texto está pendiente**: la pantalla dice «Aviso de finalidad pendiente de la verificación legal» y se reemplaza en `AVISO_DE_FINALIDAD`, de `apps/ingresos/views.py` del front.
- El documento no se copia: ni en `Ingreso`, ni en la auditoría, ni en la URL.
- El historial lo ve solo quien tiene `ingreso.ver_historico`, que es sensible.
- Paz y salvo conectado al mismo interruptor de reservas, sin efecto hasta que exista pagos.
- Las reglas de piscina de la Ley 1209 quedan fuera.

## Límites que se aceptan

- **El sistema niega el registro, no la entrada física.** Que nadie pase del aforo depende de que alguien verifique el registro en la puerta.
- **La salida automática puede dejar a alguien adentro.** Si se le acaba el tiempo y no sale, el sistema libera su puesto y admite a otro. El aviso a vigilancia es lo que lo corrige.
- **Sin procesos en segundo plano.** El proyecto calcula los vencimientos al siguiente acceso, como el bloqueo de 3 minutos (`apps/comun/bloqueo/`). Una tarea programada sería infraestructura nueva; Alejo aceptó no agregarla.
- **Las reglas de piscina de la Ley 1209 no se evalúan.** Menores de 12 años con un adulto y salvavidas no se definieron para este modo.
- **Los cupos no se actualizan solos:** se ven al recargar.
- **El vínculo `habitante` no existe todavía.** Hasta que se construya, solo ingresan los titulares con `reside` y la familia entra como acompañante de uno. Al construirlo, el ingreso lo encuentra sin cambios.

## Con qué se conecta

- **El último puesto es un caso de concurrencia.** Es el mismo problema que resuelve el bloqueo de reservas, con otra herramienta: aquí la fila del área.
- `apps/visitantes/` (HU-27, de Camilo): también registra ingresos en portería con el rol Vigilancia; desde el 2026-10-10 tiene salida y parqueadero de visitantes ([parqueaderos](parqueaderos.md)).
- `apps/permisos/`: `ingreso.registrar` e `ingreso.ver_historico`. Vigilancia no tiene `area.ver`: la lista de zonas con sus cupos se la da el propio módulo.
- `apps/notificaciones/`: el canal que ya usan las reservas (`canal.py`, `notificar`).
- `apps/unidades/`: quién reside en el conjunto sale de los vínculos vigentes.
- `apps/areas/` y `apps/reglas/`: el modo de uso, la permanencia, el aforo y las reglas.

## Sin decidir o por hacer

- Lo legal por verificar ([abiertas](../06_Decisiones/abiertas.md) 12.10 b): la mora sobre estas zonas, el registro de quién entra como dato personal (finalidad, autorización y plazo de retención) y las reglas de piscina. De ahí sale el texto del aviso de finalidad y qué hacer con el historial al cumplirse el plazo.
- El vínculo `habitante`.
- Que el vigilante confirme que quien venció de verdad salió, y que los cupos se actualicen solos.
- Enlazar los acompañantes con los visitantes de portería (HU-27).
- La historia y su número en Notion.

## Ver también

- [motor_reglas](motor_reglas.md) — las reglas que se evalúan al ingresar
- [reservas](reservas.md) — el otro modo de uso
- [construccion](../06_Decisiones/construccion.md) — las decisiones del 2026-10-06 y del 2026-10-08
- [Plan_Zonas_Con_Ingreso](../07_Planes/hechos/Plan_Zonas_Con_Ingreso.md) — el plan con el que se construyó
- [pagos](pagos.md) — la mora de paz y salvo, que impide ingresar
- [unidades](unidades.md) — quién reside, y el vínculo `habitante` que falta
- [parqueaderos](parqueaderos.md) — el otro registro de portería: visitantes
- [legal](../01_Contexto/legal.md) y [abiertas](../06_Decisiones/abiertas.md) 12.10 b — lo legal, sin verificar
- [restricciones_bd](../02_Arquitectura/restricciones_bd.md) — un ingreso abierto por persona, en la base
- `Backend/Admind_Backend/apps/ingresos/README.md`
