---
resumen: "Catálogo fijo de roles y permisos, permisos sensibles, el Superusuario y cómo está construido (un rol por conjunto)."
tipo: modulo
modulo: permisos
hu: [HU-06]
origen: "maestro v1.4 (2026-09-14) §5.3 + guía de estructura §5.4 (2026-09-30)"
actualizado: 2026-10-13
revisado: 2026-10-13
---

# Roles y permisos

> [!WARNING] Decisiones posteriores al texto del maestro (2026-09-29, Alejo)
> - **Un solo rol vigente por persona y conjunto**: se cambia, no se suma. En otro conjunto puede tener otro, y Superusuario más un rol de conjunto sigue siendo posible. Donde el diseño diga *unión de los roles*, lo vigente es esto.
> - El rol **Consejo se eliminó**: el catálogo tiene 5 roles. No se repone aunque el plan de los Sprints 2 y 3 o los avances viejos lo mencionen.
> - El **Superusuario tiene todos los permisos** del catálogo.
> - **La Secretaría no aprueba** (2026-10-13, Alejo): su rol perdió `reserva.aprobar` y `reserva.rechazar`, que Camilo le había dado con HU-14. Tiene `area.ver`, `reserva.ver_todas`, `solicitud.bandeja_ver`, `solicitud.priorizar`, `solicitud.rechazar_formal` (descartar una reserva), `caso.ver_todos` y `caso.gestionar` (tomar, descartar y redirigir un caso; permiso de Camilo, del 12/10), más anuncios y `pago.ver`. El código volvió a coincidir con el diseño de abajo.
> - **`conjunto.activar` también lo tiene Administración** (2026-10-06, Alejo, D1 b del plan del asistente): quien administra deja operativo su conjunto al terminar el asistente. Sigue en el grupo Plataforma, igual que `conjunto.crear`, que Administración ya tenía.
> - **Dos permisos nuevos en el catálogo** (2026-10-08, Alejo; construidos con [Plan_Zonas_Con_Ingreso](../07_Planes/hechos/Plan_Zonas_Con_Ingreso.md), ya con commit): `ingreso.registrar` para Vigilancia e `ingreso.ver_historico` para Administración, sensible. El Superusuario los recibe porque su rol tiene todo el catálogo. Falta contárselo a Camilo.
> - **`conjunto.crear` se evalúa por persona, no por conjunto activo** (2026-10-11, Alejo): quien es Administración en cualquiera de sus conjuntos activos puede crear otro apenas inicia sesión, sin entrar a ninguno. Lo calcula `puede_crear_conjuntos` en `apps/permisos/servicios.py` y la API lo manda como `puede_crear_conjunto`, aparte de `permisos`. Antes solo valía dentro de un conjunto activo. Falta contárselo a Camilo.
>
> Detalle en [construccion](../06_Decisiones/construccion.md).

## Diseño (maestro §5.3)

**Ni los permisos ni los roles se editan desde la interfaz.** Ambos catálogos viven en código. El administrador solo **asigna**.

Un conjunto residencial no necesita inventar cargos; necesita que la portería no vea los registros de infracción. Si un conjunto real necesita algo que los cinco roles no cubren, **el equipo lo ajusta en código y despliega**. No es una limitación pendiente: es dónde se decidió poner la palanca.

**Seis roles: cinco de conjunto y uno de plataforma.**

|Rol|Alcance|Qué agrupa|
|---|---|---|
|**Superusuario**|Plataforma|El equipo de desarrollo. Crea y desactiva conjuntos, restaura gobierno, anula registros, ve auditoría técnica, opera el sistema. **Lee datos de residentes sin procedimiento previo**|
|**Administración**|Conjunto|Gestión del conjunto, reglas, áreas, personas, reservas, infracciones, documentos, parqueaderos, respaldo|
|**Secretaría**|Conjunto|Triage de solicitudes, prioridad, rechazo formal, anuncios. **No aprueba nada**|
|**Vigilancia**|Conjunto|Registro de visitantes, **registro de ingresos a zonas con aforo**, consulta de reservas del día, registro de hechos|
|**Residente**|Conjunto|Solicitar reservas, ver las propias, cancelar, abrir casos, ver anuncios y documentos|

```
Permiso     (catálogo fijo en código)                      -- GLOBAL
Rol         (código, nombre, alcance, [permisos])          -- GLOBAL
Persona     (identidad única por documento)                -- GLOBAL (R12)
Asignación  (persona_id, rol_codigo, conjunto_id)          -- conjunto_id nulo solo para Superusuario
```

**Catálogo de permisos:**

|Grupo|Permisos|
|---|---|
|Plataforma|`conjunto.crear` · `conjunto.activar` · `gobierno.restaurar` · `auditoria_tecnica.ver` · `registro.anular` · `sistema.operar`|
|Conjunto|`conjunto.editar` · `conjunto.branding`|
|Personas|`persona.buscar` · `persona.vincular`|
|Reglas|`regla.ver` · `regla.configurar`|
|Áreas|`area.ver` · `area.gestionar`|
|Reservas|`reserva.solicitar` · `reserva.ver_todas` · `reserva.aprobar` · `reserva.rechazar` · `reserva.cancelar_ajena` · `reserva.declarar_pago` (desde el 10/10: solo Administración y Superusuario; Secretaría no aprueba ni declara el pago; no es sensible)|
|Usuarios|`usuario.gestionar` · `rol.asignar` · `vinculo.gestionar`|
|Visitantes|`visitante.registrar` · `visitante.ver_historico`|
|Ingresos a zonas|`ingreso.registrar` · `ingreso.ver_historico`|
|Casos|`caso.crear` · `caso.ver_todos` · `caso.responder`|
|Triage|`solicitud.bandeja_ver` · `solicitud.priorizar` · `solicitud.rechazar_formal`|
|Infracciones|`infraccion.registrar` · `infraccion.ver` · `infraccion.cerrar`|
|Comunicación|`anuncio.publicar` · `anuncio.dirigir`|
|Citas|`cita.agendar_propia` · `cita.gestionar_horario` · `cita.ver_todas`|
|Documentos|`documento.subir` · `documento.ver` · `documento.descargar`|
|Datos|`importacion.ejecutar` · `respaldo.generar` · `auditoria.ver`|
|Pagos|`pago.ver` (sensible: Administración y Secretaría) · `pago.confirmar` (Administración) · `pago.reportar` (Residente). Desde el 10/10|
|Parqueaderos|`parqueadero.ver` · `parqueadero.asignar` · `parqueadero.gestionar` (desde el 10/10, solo Administración y Superusuario: crea y retira parqueaderos del catálogo; `asignar` queda para HU-34; no es sensible)|

**Permisos sensibles (exigen 2FA):** `visitante.ver_historico`, `ingreso.ver_historico`, `documento.descargar`, `respaldo.generar`, `usuario.gestionar`, `rol.asignar`, `auditoria.ver`, `persona.buscar`, `persona.vincular`, `infraccion.*`, `solicitud.bandeja_ver` y **todos los de plataforma**.

Los nombres dicen la verdad de la operación: `reserva.solicitar` porque un residente **solicita**, no crea. `solicitud.rechazar_formal` y no `rechazar` porque el rechazo es **de forma**, y ese matiz es el rol entero.

**Lo que deliberadamente no existe:** ningún permiso de aprobación para la Secretaría. `reserva.aprobar` es del Administrador y no es concedible a ningún otro rol de conjunto.

### El Superusuario — el equipo de desarrollo

Existe por tres razones: el administrador se equivoca y el diseño no perdona (no hay borrado ni edición de registros cerrados); darle esa facultad al propio administrador destruiría el valor probatorio de todo el registro; y alguien tiene que crear el primer conjunto.

**Qué significa anular.** No es borrar y no es editar. La fila permanece, se marca `anulado = true` con `motivo_anulacion`, `anulado_por` y `fecha_anulacion`. Sigue consultable, tachada y con su motivo a la vista. **El error queda documentado, no desaparecido.**

**Lo que NO puede:**

- Alterar la auditoría — el usuario de BD de la aplicación no tiene `UPDATE` ni `DELETE` sobre esas tablas
- Anular sin motivo — el campo no admite vacío
- **Operar dentro de un conjunto** — no aprueba reservas, no publica anuncios, no registra infracciones. Para un rol de plataforma esas operaciones **no existen**

**Guardarraíles:** una cuenta por integrante, nunca compartida · 2FA sin excepción · toda acción marcada `via_superusuario = true` · toda anulación notifica al administrador del conjunto afectado · no aparece en el directorio de ningún conjunto · no puede revocarse a sí mismo el último rol de Superusuario.

> [!WARNING] La honestidad que hay que llevar a la sustentación Con el _break-glass_ eliminado, la respuesta defendible pasó de _"no puede leer datos personales sin dejar aviso al administrador"_ a _"puede leerlos, y queda registrado que lo hizo"_. Es más débil. Se aceptó a cambio de eliminar un módulo entero (motivo, vigencia, expiración, notificación y aviso permanente) de un proyecto de dos personas. Está documentado en **R10** y conviene llegar sabiéndolo en vez de descubrirlo en una pregunta.

## Cómo está construido (2026-09-30)

- **Catálogo fijo en código** (`catalogo.py`): 5 roles (Superusuario, Administración, Secretaría, Vigilancia, Residente) y la lista de permisos de cada uno (`"reserva.solicitar"`, `"area.gestionar"`…). No se editan desde la interfaz: un cambio se hace en el código. El reparto es provisional hasta validarlo con un administrador real. **Consejo se eliminó el 29/09**: no hay que reponerlo aunque el plan de sprints o el avance lo mencionen. El **Superusuario** tiene todos los permisos del catálogo.
- **`Asignacion`**: "la persona X tiene el rol Y en el conjunto Z desde tal fecha hasta tal fecha". El Superusuario tiene `conjunto` nulo (es de plataforma).
- **Un solo rol por persona y conjunto** (decisión de Alejo, 29/09). La restricción de la base `asignacion_un_rol_por_conjunto` (persona + conjunto, solo entre las asignaciones abiertas) lo hace cumplir; en otro conjunto la persona puede tener otro rol. Si ya tiene uno, **no se suma otro: se cambia**.
- **Los servicios** (`permisos/servicios.py`): `asignar_rol` (si ya tiene rol → `RolYaAsignado`), `cambiar_rol` (cierra el actual hoy y abre el nuevo **en la misma transacción**, así nunca queda con dos ni con ninguno; auditoría `rol.cambiar`), `retirar_rol` y `retirar_roles_del_conjunto` (la base del "Eliminar usuario"). Retirar nunca borra: solo cierra la vigencia.
- **`exigir_permiso(request, "reserva.solicitar")`** (`permisos/views.py`): la primera línea de cada vista. Si falta el permiso → 403.
- **"Nunca cero Administración"**: el servicio impide retirar o cambiar el último rol de Administración de un conjunto (`UltimaAdministracion`).

> [!WARNING] Choca con el maestro
> El maestro (§3.1, línea de permisos efectivos, y R5) y el criterio de HU-06 todavía dicen que una persona puede tener **varios roles** y que sus permisos son la unión. Lo vigente es un solo rol por conjunto.

## Ver también

- [riesgos](../06_Decisiones/riesgos.md) — R5, R10 y R12
- [cuentas](cuentas.md) — sesión, token y segundo factor
- [personas](personas.md) — a quién se le asigna el rol
- [unidades](unidades.md) — propietario y arrendatario no son roles: son vínculos
- [triage](triage.md) — qué hace la Secretaría
- [cerradas](../06_Decisiones/cerradas.md) — decisiones 8, 9, 22 y 26
- [invariantes](../03_Reglas/invariantes.md) — cómo exige una vista su permiso
- [frontend](../02_Arquitectura/frontend.md) — qué ve cada rol en el lateral
- [historias](../08_Estado/historias.md) — HU-06
- `Backend/Admind_Backend/apps/permisos/catalogo.py` — el catálogo vigente
