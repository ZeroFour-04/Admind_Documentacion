---
resumen: "Zonas con ingreso: vigilancia registra a quien entra, el aforo es simultáneo y la salida es manual o por tiempo. Definición del 2026-10-06, sin historia y sin construir."
tipo: modulo
modulo: ingresos
hu: []
origen: "definición con Alejo en chat (2026-10-06)"
actualizado: 2026-10-06
---

# Ingreso a zonas con aforo

> [!IMPORTANT] Funcionalidad nueva, sin historia y sin construir
> Ninguna historia, de HU-01 a HU-39, la cubre, y no existe ninguna app para ella. Alejo decidió el 2026-10-06 que se construye antes de la entrega. Falta crear la historia, contárselo a Camilo y escribir el plan. Dónde vive el código se decide al planear.

## Qué es

Hay zonas que no se reservan con anticipación pero tampoco son de paso libre: el gimnasio, una piscina grande. Piden dos cosas: que quien entre quede registrado, y que nunca haya adentro más personas que el aforo.

Es el segundo **modo de uso** de una zona. El primero, con reserva, es el flujo de [reservas](reservas.md). Las zonas de paso libre (parques, zonas verdes) no entran al sistema.

## El recorrido

1. El vigilante elige la zona, escribe el número de documento del residente y cuántos acompañantes entran.
2. El sistema busca a esa persona **solo entre los residentes del conjunto activo** y muestra su nombre y su vivienda, para que el vigilante confirme.
3. El sistema valida todo junto y, si algo falla, dice **todos** los motivos: las reglas del sistema, las alfa y las beta de [motor_reglas](motor_reglas.md).
4. Si pasa, guarda el ingreso con su hora de salida prevista: la entrada más la permanencia máxima de la zona.
5. La salida la marca el vigilante cuando la persona se va, o la da el sistema al cumplirse el tiempo.

## Lo decidido

| Tema | Decisión |
|---|---|
| **Quién registra** | El rol Vigilancia, por ahora. Alejo dudó si debía ser un rol aparte |
| **Cómo se identifica** | Por número de documento. Si no es de un residente del conjunto activo, la respuesta es «no encontrado», exista o no esa persona en otro conjunto: la tabla de personas es global y no puede volverse un directorio |
| **Aforo** | Simultáneo: las personas adentro, más el residente y sus acompañantes que entran, no lo superan |
| **Acompañantes** | Los permite o no una regla alfa del conjunto, con un máximo **por vivienda a la vez**. Se asume que son visitantes. Solo se guarda cuántos son, sin enlazarlos con los visitantes de portería (HU-27) |
| **Salida** | Híbrida: manual por el vigilante, o automática al cumplirse la permanencia máxima |
| **Aviso al cumplirse el tiempo** | Al residente y a vigilancia |
| **Cuándo sale el aviso** | Al siguiente acceso al módulo, no en el minuto exacto. El conteo del aforo sí es exacto |
| **Paz y salvo** | Si el conjunto la activa, una vivienda en mora no ingresa |

## Límites que se aceptan

- **El sistema niega el registro, no la entrada física.** Que nadie pase del aforo depende de que alguien verifique el registro en la puerta.
- **La salida automática puede dejar a alguien adentro.** Si se le acaba el tiempo y no sale, el sistema libera su puesto y admite a otro. El aviso a vigilancia es lo que lo corrige.
- **Sin procesos en segundo plano.** El proyecto calcula los vencimientos al siguiente acceso, como el bloqueo de 3 minutos (`apps/comun/bloqueo/`, `expirar_vencidos`). Una tarea programada sería infraestructura nueva; Alejo aceptó no agregarla.
- **Las reglas de piscina de la Ley 1209 no se evalúan.** Menores de 12 años con un adulto y salvavidas no se definieron para este modo.

## Con qué se conecta

- **El último puesto es un caso de concurrencia.** Dos registros a la vez por el último lugar es el mismo problema que resuelve el bloqueo de reservas.
- `apps/visitantes/` (HU-27, de Camilo): también registra ingresos en portería con el rol Vigilancia y todavía no tiene salida.
- `apps/permisos/`: Vigilancia tiene hoy `visitante.registrar` y `reserva.ver_todas`. Hace falta un permiso nuevo; el agente propuso `ingreso.registrar`. El catálogo es de equipo.
- `apps/notificaciones/`: el canal que ya usan las reservas (`canal.py`, `notificar`).
- `apps/unidades/`: quién reside en el conjunto sale de los vínculos vigentes. Hoy solo hay vínculos de propietario y arrendatario, así que **la familia no aparecería**. Alejo decidió el 2026-10-06 un tercer tipo, `habitante`, todavía sin construir: tiene que existir antes que este módulo, o solo ingresan los titulares ([unidades](unidades.md), [construccion](../06_Decisiones/construccion.md)).

## Supuestos del agente, por confirmar

- Una persona tiene un solo ingreso abierto a la vez en el conjunto.
- Los acompañantes entran y salen con su residente.
- Al cumplirse el tiempo, la persona puede volver a entrar si hay puesto.
- Si la persona vive en dos viviendas del conjunto, el vigilante elige a nombre de cuál entra.
- El aviso a vigilancia aparece en su pantalla de control, no por correo.

## Sin decidir

En [abiertas](../06_Decisiones/abiertas.md) 12.10: lo legal por verificar (mora sobre estas zonas, y el registro de quién entra como dato personal) y el permiso y el rol de quien registra.

## Ver también

- [motor_reglas](motor_reglas.md) — las reglas que se evalúan al ingresar
- [reservas](reservas.md) — el otro modo de uso
- [construccion](../06_Decisiones/construccion.md) — las decisiones del 2026-10-06
