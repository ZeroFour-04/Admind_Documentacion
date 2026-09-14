
Plantillas Django + Alpine
## titulo: "AdMind — Documento maestro de contexto" proyecto: "Proyecto de Ingeniería de Software II" institucion: "Universidad de Cundinamarca — Facatativá" equipo: ["Alejo (Manuel Alejandro Aldana Rincón)", "Camilo"] fecha_corte: 2026-09-11 estado_general: "Fin de planeación. Sprint 1 sin iniciar. Cero líneas de código." proposito: "Contexto completo para que cualquier agente de IA o persona nueva se ubique leyendo un solo archivo."

# AdMind — Documento maestro

> [!IMPORTANT] Cómo leer esto si eres un agente de IA
> 
> 1. Lee este archivo completo antes de proponer nada. Está ordenado de lo general a lo específico.
> 2. La **§12 lista contradicciones abiertas**. Si tu tarea toca alguna, **pregunta; no elijas por tu cuenta**.
> 3. La **§13 separa lo decidido de lo propuesto**. No trates una propuesta como un hecho.
> 4. Las **restricciones legales (§4) están por encima de todo**. Un requisito prohibido no se implementa ni detrás de un permiso de administrador.
> 5. Las **decisiones de arquitectura (§9) están cerradas** con razón escrita. Si tu propuesta contradice una, dilo explícitamente en vez de reabrirla en silencio.
> 6. El criterio de corte del proyecto no es la funcionalidad, es la **defendibilidad en sustentación**. Ante dos soluciones, gana la que el equipo pueda explicar en voz alta.

---

## 1. Qué es AdMind

Aplicación web para administrar **conjuntos residenciales bajo régimen de propiedad horizontal en Colombia**, regidos por la Ley 675 de 2001.

**Problema de origen.** La administración de un conjunto hoy se sostiene sobre grupos de WhatsApp y hojas de cálculo sueltas, con una o dos personas siguiéndole el rastro a 30–100 apartamentos. No es incompetencia: es sobrecarga y repetición. Un familiar de un integrante del equipo administra un conjunto y trabaja exactamente así — de ahí salió el proyecto y de ahí sale el stakeholder externo.

**Contexto académico.** Proyecto de semestre, equipo de dos personas, con sustentación ante jurado como entrega final. Se eligió sobre una propuesta competidora de POS para pequeños negocios, descartada por saturación de mercado y solapamiento con otro proyecto del equipo.

### Los cuatro pilares

|Pilar|Qué significa|
|---|---|
|**Multiconjunto real**|Una sola base para todas las copropiedades, con aislamiento estricto defendido en capas redundantes|
|**Motor de reglas configurable**|Cada copropiedad configura sus reglas de reserva a partir de su propio reglamento|
|**Reserva por orden de llegada**|Bloqueo temporal de 3 minutos, decisión humana y condiciones escritas|
|**El sistema registra, no decide**|En infracciones, en dinero y en lo que la ley reserva a la asamblea|

### El diferenciador, dicho con honestidad

No es un algoritmo llamativo, y conviene decirlo antes de que lo pregunten. Es la combinación de tres cosas defendibles: motor de reglas configurable por copropiedad, flujo de estados con concurrencia real y trazabilidad completa, y aislamiento entre conjuntos diseñado en capas.

Que la competencia por una franja se resuelva por orden de llegada y validación humana —y no por un mecanismo automático— es una decisión tomada a partir de **entrevistas a residentes**. Ante un jurado, _"diseñamos esto porque entrevistamos a residentes"_ vale más que un algoritmo elegante que nadie pidió — **siempre que las entrevistas estén documentadas**, y hoy no lo están (ver §11).

---

## 2. El equipo

Dos personas: **Alejo** y **Camilo**.

- Ambos son Developers siempre. Un rol de PO o SM ocupa 10–15 % del tiempo; el resto es código
- Alejo lidera la documentación y hace la mayoría de las actualizaciones; Camilo crea documentación nueva y edita de vez en cuando
- **Punto de partida técnico desigual**: Alejo parte de Python básico y es quien recorre la ruta de aprendizaje; **Camilo tiene más experiencia escribiendo código** (corregido el 2026-09-11; la versión 1 de este documento decía lo contrario)
- Disponibilidad estimada: 2 personas × 3 h/día × 6 días = 2160 min por sprint

> [!WARNING] Nota de consistencia El documento de ruta de aprendizaje nombra al compañero como **"Sergio"**. Es un error: Sergio es socio de otro proyecto del autor (KOR), no de AdMind. Donde se lea Sergio en ese documento, entiéndase **Camilo**.

> [!WARNING] Consecuencia de la corrección anterior
> La consideración de equipo de §12.1 está escrita sobre la premisa contraria: _"con Vue, Camilo tiene que aprender JavaScript, Vue y Git en paralelo"_. **Ese argumento hay que rehacerlo antes de cerrar la decisión del frontend**, porque quien está en formación es Alejo.
>
> Consecuencia de gestión: el riesgo ya no es que Camilo se atasque, sino que Camilo se quede con todo lo difícil y Alejo no pueda defenderlo. El jurado les pregunta a los dos. La rotación de §8.4 deja de ser una buena práctica y pasa a ser una necesidad.

---

## 3. Alcance, en cuatro niveles

El alcance es el instrumento de control de riesgo del proyecto. Está escrito así a propósito: **si solo el Núcleo funciona, el proyecto se sustenta igual.**

### 3.1 Núcleo — esto _es_ el proyecto

**Multiconjunto**

- El permiso `conjunto.crear` es del rol de plataforma Superusuario, no del administrador
- Creación por asistente. El conjunto **no queda operativo** hasta completar: datos básicos, catálogo de áreas, al menos un usuario con rol Administración, y reglamento cargado
- **Las reglas beta se configuran al crear el conjunto**, no después. Un conjunto sin reglas acepta cualquier reserva
- Selector de conjunto activo. Todo lo que se ve y se escribe pertenece al conjunto activo

**Identidad de personas**

- `Persona` es **global a la plataforma**, única por `(tipo_documento, numero_documento)`
- Tipos de lista cerrada: `CC`, `CE`, `PA`, `PEP`, `TI`
- **La llave primaria es un UUID**, no el documento
- El número se **normaliza al guardar**: sin puntos, sin espacios, sin ceros a la izquierda
- Aplica a todos: residentes, vigilancia, secretaría y administración

**Reserva de zonas comunes**

- Salón comunal, piscina, gimnasio, y catálogo de áreas ampliable por conjunto
- Ciclo: bloquear 3 min → llenar → confirmar contenido → solicitar → validar reglas → revisión del administrador → aprobar o rechazar → cancelar
- Cada área lleva `clasificacion ∈ {comun, comun_esencial, comun_uso_exclusivo}` y el flag derivado `esEsencial`

**Asignación en alta demanda**

- Marcado de fechas de alta demanda (24 y 31 de diciembre, Día de la Madre)
- **FIFO puro** sobre el momento de tomar el bloqueo. Sin prioridades, sin ponderaciones, sin desempates automáticos
- La anticipación máxima es una regla beta, y convierte la apertura del calendario en una **taquilla**: es caso de carga y concurrencia, y entra a las pruebas

**Roles y permisos**

- Catálogos fijos en código. El administrador **asigna**, no crea ni edita
- Permisos efectivos = **unión** de los de todos los roles. Solo aditivo, sin denegaciones

**Vínculos de unidad** — propietario y arrendatario no son roles, son vínculos con una unidad

**Canal de notificaciones** — un componente, dos salidas (app y SMTP). Es infraestructura compartida y **se construye antes que sus consumidores**

**Login** — autenticación propia, recuperación de contraseña, y **2FA TOTP obligatorio para todo usuario con algún permiso sensible**

### 3.2 Comprometido — segunda prioridad

Gestión de visitantes · Casos · Infracciones (registro) · Citas con el administrador · Bandeja de triage de Secretaría · Comunicación con residentes (tablón + notificaciones) · Repositorio de documentos · Parqueaderos de residentes · Pago de administración (reporte + confirmación) · Importación masiva CSV/Excel y respaldo

> [!WARNING] Aceptado de entrada **Comprometido puede quedar parcial.** Un proyecto con el núcleo sólido y tres módulos sin empezar se defiende. Uno con doce módulos a medias, no.

### 3.3 Condicional — solo si sobra tiempo

Registro de actividades (vista sobre la auditoría) · Vista consolidada de novedades entre conjuntos · Cobro a visitantes por parqueadero · Mapa de parqueaderos · Plantillas de conjunto · Modo oscuro · Logo por conjunto

### 3.4 Fuera de alcance — fronteras, no pendientes

|Qué|Por qué|
|---|---|
|WhatsApp como canal|Exige cuenta Meta Business verificada, número dedicado y plantillas aprobadas. Mitigado: el canal es un puerto con adaptadores; el de WhatsApp queda declarado sin implementar|
|Mensajería bidireccional general|Única excepción: el hilo confinado a una solicitud de reserva|
|Pasarela de pagos|Manejar dinero real implica PCI-DSS|
|Procedimiento sancionatorio completo|Corte de **competencia**, no de esfuerzo: requerir es del administrador (art. 59), decidir es de la asamblea o el consejo (art. 60)|
|Impugnación de sanciones|Es judicial y externa|
|Proceso de asamblea|Basta el adjunto del acta más metadatos|
|Sorteo de parqueaderos|Obliga a diseñar la acción afirmativa del 2% para personas con discapacidad (D1538/2005, T-062/18)|
|Regímenes jurídicos de parqueadero|El sistema registra un hecho administrativo, no constituye un derecho|
|Roles personalizados por conjunto|Si un conjunto necesita un cargo nuevo, el equipo ajusta el catálogo en código|
|Rol `Operador`|En un equipo de dos que es soporte y gobierno a la vez, la separación produce dos roles que siempre se asignan juntos|
|Acceso de excepción (_break-glass_)|Cinco piezas para un rol que ya audita todo lo que hace. Se elimina asumiendo el costo (R10)|
|Certificados de residencia|Habeas data desproporcionado frente al valor|
|Subdominio separado para residentes|La separación es por permisos, no por infraestructura|
|Búsqueda libre de personas por nombre|La tabla de Personas es global: un buscador por nombre sobre ella es un directorio de toda la plataforma|
|Denegaciones explícitas de permisos|Los permisos son puramente aditivos|
|IA dentro del producto|No hay un problema definido detrás|

---

## 4. Restricciones legales — jerárquicamente superiores a todo

Fuente completa: guía legal v1.0 (2026-08-20), 116 requisitos con fundamento normativo bajo la convención `REQ-<MODULO>-<NN>`.

**Jerarquía declarada:** Constitución > ley > decreto reglamentario > reglamento de propiedad horizontal > manual de convivencia > configuración del sistema. Ningún requisito legal puede relajarse por configuración del cliente, decisión de asamblea ni permiso de rol.

**Tipos de requisito:** `OBLIGATORIO` (si no se cumple, la operación falla con error explícito) · `PROHIBIDO` (el sistema no expone la funcionalidad, ni siquiera tras un permiso) · `CONFIGURABLE` (parámetro por conjunto, con topes legales como validación dura) · `ADVERTENCIA` (zona discutida: registrar y advertir, nunca decidir).

### 4.1 Marco normativo

La Ley 675 de 2001 es la norma eje —vigente, modificada solo por la Ley 2079 de 2021— pero no basta. El sistema toca además:

|Materia|Norma adicional|
|---|---|
|Visitantes, cámaras, datos personales|Ley 1581 de 2012, Decreto 1074 de 2015|
|Convivencia, ruido, mascotas, policía|Ley 1801 de 2016, Decreto 768 de 2025|
|Piscina|Ley 1209 de 2008, Decreto 554 de 2015|
|Solicitudes / PQR|Ley 1755 de 2015|
|Portería y vigilancia|Decreto Ley 356 de 1994|
|Cobro por uso de zonas comunes|E.T. art. 19-5 y régimen de IVA|

### 4.2 Reglas duras que tocan el núcleo

|Regla|Fundamento|
|---|---|
|El sistema **no impone sanciones**|L675 arts. 59 y 60|
|La comunicación de una infracción va a **propietario y arrendatario**, ambos|C-318/02|
|La convocatoria a asamblea va a **cada propietario**, resida o no|L675 art. 39|
|No existe operación de **restricción de uso** por mora ni como sanción sobre bienes esenciales|SU-509/01, L675 art. 59 §|
|Un parqueadero de visitantes **no se destina** a una unidad; la ocupación temporal sí lo es|L675 art. 22|
|Cobrar por un bien común solo procede si **el reglamento lo autoriza**|L675 art. 19 §2, art. 46 num. 5|
|Toda captura de documento exige **finalidad declarada, autorización y plazo de retención**|Ley 1581|
|No se retiene el documento físico del visitante|Minimización + C. Penal art. 395|
|Las actas de asamblea son solo para propietarios autenticados; el sistema no reemplaza la obligación de entregar copia|L675 art. 47 §|
|Piscina: menores de 12 años requieren acompañante adulto; salvavidas en los supuestos exigidos|L1209/2008, D554/2015|

> [!IMPORTANT] Cómo se implementa una prohibición legal **No como permiso denegado, sino como operación inexistente.** No existe el permiso `sancionar` porque no existe la operación. No hay campo de multa en el registro de infracción. Un parqueadero de visitantes no aparece en el selector de asignación.
> 
> El principio: un rol mal asignado puede ser un problema de privacidad; **nunca puede ser un problema de legalidad**.

### 4.3 Zona de cuidado

Circula contenido de blogs que presenta el **Decreto 768 de 2025** como "la nueva ley de propiedad horizontal", atribuyéndole reglas de videovigilancia, registro digital de visitantes y prohibición de alquiler corto. **Ninguna de esas reglas está en el decreto** — es un decreto de procedimiento único de policía. No usar fuentes secundarias como fundamento normativo.

Hay reformas en trámite (PL 067/2025 Cámara, reforma integral de la Ley 675, aprobada en primer debate el 7 de abril de 2026). **Vigilar, no implementar.**

---

## 5. Diseño de los módulos del núcleo

### 5.1 Flujo de reserva

**Principio: el orden de llegada decide quién puede pedir; una persona decide quién obtiene.** El sistema no sortea, no pondera y no valida dinero. Hace tres cosas: garantizar que solo una persona a la vez tramite una franja, dejar por escrito lo acordado, y registrar cada paso con hora y actor.

**Dónde vive el estado.** En la **solicitud**, no en la franja. La franja es una coordenada `(area, fecha, hora_inicio, hora_fin)` cuya disponibilidad se consulta. El calendario no se materializa en la base.

```
Bloqueantes:     EN_SOLICITUD · APARTADA · RESERVADA
No bloqueantes:  RECHAZADA · CANCELADA · EXPIRADA
```

|Estado|Quién lo produce|Significa|
|---|---|---|
|`EN_SOLICITUD`|Residente, al oprimir "Reservar"|Tiene 3 minutos exclusivos para llenar y enviar|
|`APARTADA`|Residente, al enviar|En manos del administrador. Aún no es reserva|
|`RESERVADA`|Administrador, al aprobar|Reserva en firme, con condiciones escritas|
|`RECHAZADA`|Administrador|Negada con categoría de motivo. Libera la franja|
|`CANCELADA`|Residente o administrador|Deshace una reserva en firme. Libera la franja|
|`EXPIRADA`|Sistema|Vencieron los 3 minutos sin envío. Libera la franja|

**El bloqueo de 3 minutos.** Es el tiempo para **terminar de diligenciar y enviar**, no el tiempo de la reserva ni el del administrador. Es **constante del sistema, no regla beta**: si cada conjunto la ajusta, deja de haber una sola explicación posible. Cuenta regresiva visible. Un residente solo puede tener **un bloqueo activo** en todo el sistema. Salir del formulario libera de inmediato.

**Confirmación antes de enviar — se confirma el contenido, no la intención.** Un _"¿Está seguro?"_ se acepta por reflejo. Lo que funciona es devolverle a la persona el dato que va a comprometer:

> Vas a solicitar el **Salón Comunal** para el **sábado 26 de diciembre de 2026**, de **2:00 p.m. a 6:00 p.m.**, para 40 asistentes.

**El día de la semana en letras es el punto entero.** El error más común no es equivocarse de área ni de hora: es equivocarse de fecha por una casilla del calendario. La persona piensa "el sábado" y oprime el 25. Repetir la fecha en números no atrapa ese error; escribir "viernes 25" sí.

Se usa en tres sitios: solicitud de reserva, agendamiento de cita y aceptación de alternativa tras cambio de horario. Un componente, tres usos. Ocurre dentro de los 3 minutos y no los extiende.

**La aprobación deja contrato.** El campo _condiciones del alquiler_ es **obligatorio y no puede ir vacío**. Queda congelado al aprobar; si se modifica, se guarda como nueva versión con fecha y autor. Se precarga desde plantilla por área. Contenido mínimo: valor, depósito y condición de devolución, horario, aforo, responsable, política de cancelación, estado de entrega del área.

**El dinero lo valida una persona.** El sistema guarda `pago_declarado_por`, `fecha_declaracion` y el comprobante si se subió. Esa frase va en la interfaz, no solo en la documentación.

**El rechazo del administrador.** El texto libre es opcional; la **categoría** no: `NO_DISPONIBLE` · `CONDICIONES_NO_CUMPLIDAS` · `DOCUMENTACION_INCOMPLETA` · `INCUMPLE_REGLAMENTO` · `OTRO` (obliga a texto libre).

**La campana.** Suscripción a una **franja concreta**, no a un área ni a un día. Se notifica a todos los suscritos al mismo tiempo; la suscripción se consume al notificar. **La estampida es intencional**: produce una carrera por el bloqueo, y esa carrera es el mecanismo que el diseño ya tiene resuelto.

**Dos oportunidades por franja (R9).** Si el residente deja vencer el bloqueo, puede volver a tomar esa franja **una sola vez**, avisado de que es la última. No hay tercera. El contador es por par `(residente, franja)` y **solo cuenta el vencimiento**: liberar a propósito no gasta oportunidad.

**Concurrencia (R7).** Restricción de unicidad parcial en base de datos —una sola solicitud bloqueante por franja— más transacción sobre el mecanismo compartido de R1. La **expiración se evalúa al siguiente acceso**: es idempotente y no depende de ningún proceso corriendo.

Pruebas obligatorias: N solicitudes simultáneas producen exactamente un bloqueo; un bloqueo vencido no bloquea; uno liberado manualmente no expira dos veces; la apertura de la ventana de anticipación con N residentes en el mismo segundo no duplica reservas.

### 5.2 Identidad de personas

**Una persona, una fila, en toda la plataforma.** El rol es por conjunto; el vínculo con una unidad es por conjunto; **la identidad no**.

El caso que originó la decisión: un vigilante que trabaja en el conjunto B y vive en el conjunto A, ambos administrados por la misma persona. Modelarlo como dos filas produce exactamente los conflictos que el sistema debe evitar.

```
Persona                       -- TABLA GLOBAL: sin conjunto_id (R12)
  id : UUID                   (PK)
  tipo_documento ∈ {CC, CE, PA, PEP, TI}
  numero_documento
  nombre
  correo
  activo : bool
  UNIQUE (tipo_documento, numero_documento)
```

**Por qué el documento identifica pero no es la llave primaria:**

|Si el documento fuera PK|Consecuencia|
|---|---|
|Viaja a cada FK|Toda tabla que referencie a una persona lleva su cédula adentro|
|Viaja a cada URL|`/residentes/1032456789` publica la cédula en el historial y en los logs|
|El número solo no es único|CC, CE, PA, PEP y TI son numeraciones distintas que pueden coincidir|
|Los documentos cambian|Una TI se vuelve CC a los 18. Con PK documento, cada cambio es cascada — sobre una base que además prohíbe el borrado|

El UUID **referencia**; el par `(tipo, número)` **identifica**. Son decisiones independientes.

**Vincular a alguien que ya existe:** buscar por documento exacto y asignarle rol en el conjunto activo. Un solo paso. Es el punto blando del diseño y está registrado como **R12**.

### 5.3 Roles y permisos

**Ni los permisos ni los roles se editan desde la interfaz.** Ambos catálogos viven en código. El administrador solo **asigna**.

Un conjunto residencial no necesita inventar cargos; necesita que la portería no vea los registros de infracción. Si un conjunto real necesita algo que los cinco roles no cubren, **el equipo lo ajusta en código y despliega**. No es una limitación pendiente: es dónde se decidió poner la palanca.

**Seis roles: cinco de conjunto y uno de plataforma.**

|Rol|Alcance|Qué agrupa|
|---|---|---|
|**Superusuario**|Plataforma|El equipo de desarrollo. Crea y desactiva conjuntos, restaura gobierno, anula registros, ve auditoría técnica, opera el sistema. **Lee datos de residentes sin procedimiento previo**|
|**Administración**|Conjunto|Gestión del conjunto, reglas, áreas, personas, reservas, infracciones, documentos, parqueaderos, respaldo|
|**Consejo**|Conjunto|Lectura de infracciones, actas y auditoría. Existe porque es un órgano real de la Ley 675 (arts. 53 y 55)|
|**Secretaría**|Conjunto|Triage de solicitudes, prioridad, rechazo formal, anuncios. **No aprueba nada**|
|**Vigilancia**|Conjunto|Registro de visitantes, consulta de reservas del día, registro de hechos|
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
|Reservas|`reserva.solicitar` · `reserva.ver_todas` · `reserva.aprobar` · `reserva.rechazar` · `reserva.cancelar_ajena`|
|Usuarios|`usuario.gestionar` · `rol.asignar` · `vinculo.gestionar`|
|Visitantes|`visitante.registrar` · `visitante.ver_historico`|
|Casos|`caso.crear` · `caso.ver_todos` · `caso.responder`|
|Triage|`solicitud.bandeja_ver` · `solicitud.priorizar` · `solicitud.rechazar_formal`|
|Infracciones|`infraccion.registrar` · `infraccion.ver` · `infraccion.cerrar`|
|Comunicación|`anuncio.publicar` · `anuncio.dirigir`|
|Citas|`cita.agendar_propia` · `cita.gestionar_horario` · `cita.ver_todas`|
|Documentos|`documento.subir` · `documento.ver` · `documento.descargar`|
|Datos|`importacion.ejecutar` · `respaldo.generar` · `auditoria.ver`|
|Parqueaderos|`parqueadero.ver` · `parqueadero.asignar`|

**Permisos sensibles (exigen 2FA):** `visitante.ver_historico`, `documento.descargar`, `respaldo.generar`, `usuario.gestionar`, `rol.asignar`, `auditoria.ver`, `persona.buscar`, `persona.vincular`, `infraccion.*`, `solicitud.bandeja_ver` y **todos los de plataforma**.

Los nombres dicen la verdad de la operación: `reserva.solicitar` porque un residente **solicita**, no crea. `solicitud.rechazar_formal` y no `rechazar` porque el rechazo es **de forma**, y ese matiz es el rol entero.

**Lo que deliberadamente no existe:** ningún permiso de aprobación para la Secretaría. `reserva.aprobar` es del Administrador y no es concedible a ningún otro rol de conjunto.

#### El Superusuario — el equipo de desarrollo

Existe por tres razones: el administrador se equivoca y el diseño no perdona (no hay borrado ni edición de registros cerrados); darle esa facultad al propio administrador destruiría el valor probatorio de todo el registro; y alguien tiene que crear el primer conjunto.

**Qué significa anular.** No es borrar y no es editar. La fila permanece, se marca `anulado = true` con `motivo_anulacion`, `anulado_por` y `fecha_anulacion`. Sigue consultable, tachada y con su motivo a la vista. **El error queda documentado, no desaparecido.**

**Lo que NO puede:**

- Alterar la auditoría — el usuario de BD de la aplicación no tiene `UPDATE` ni `DELETE` sobre esas tablas
- Anular sin motivo — el campo no admite vacío
- **Operar dentro de un conjunto** — no aprueba reservas, no publica anuncios, no registra infracciones. Para un rol de plataforma esas operaciones **no existen**

**Guardarraíles:** una cuenta por integrante, nunca compartida · 2FA sin excepción · toda acción marcada `via_superusuario = true` · toda anulación notifica al administrador del conjunto afectado · no aparece en el directorio de ningún conjunto · no puede revocarse a sí mismo el último rol de Superusuario.

> [!WARNING] La honestidad que hay que llevar a la sustentación Con el _break-glass_ eliminado, la respuesta defendible pasó de _"no puede leer datos personales sin dejar aviso al administrador"_ a _"puede leerlos, y queda registrado que lo hizo"_. Es más débil. Se aceptó a cambio de eliminar un módulo entero (motivo, vigencia, expiración, notificación y aviso permanente) de un proyecto de dos personas. Está documentado en **R10** y conviene llegar sabiéndolo en vez de descubrirlo en una pregunta.

### 5.4 Blindaje de datos

**El problema sin jerga.** Una sola base guarda a todos los conjuntos. Las reservas de "Torres del Río" y las del "Mirador" están en la misma tabla, distinguidas por una columna. **Lo único que los separa es que cada consulta se acuerde de filtrar** — y ese "acordarse" es lo que falla en un proyecto de dos personas con prisa. Cuando falla, la aplicación no se rompe: funciona perfectamente y le muestra a un residente de Torres del Río el listado de morosos del Mirador. Eso es tratamiento no autorizado bajo la Ley 1581.

**En la base de datos:**

- `conjunto_id NOT NULL` en toda tabla, sin valores por defecto, con **una lista cerrada de excepciones**: `Persona`, `Usuario` y los catálogos de roles y permisos
- **Llaves foráneas compuestas.** Si `reservas` referencia `areas`, la FK es `(area_id, conjunto_id)` contra una clave única `(id, conjunto_id)`. La base **rechaza físicamente** la fila cruzada
- Toda clave única incluye `conjunto_id` — la torre "1" de A y la de B deben coexistir
- Índices encabezados por `conjunto_id`
- Privilegios del usuario de aplicación: sin `UPDATE` ni `DELETE` sobre auditoría, sin DDL en producción, ninguna FK con `ON DELETE CASCADE`

**En los accesos:**

- El conjunto activo **sale de la sesión**, resuelto en middleware como contexto de solo lectura. **Ningún controlador acepta `conjunto_id` como parámetro**: si aparece en la URL o el cuerpo, se rechaza
- Un repositorio base inyecta `WHERE conjunto_id = :ctx` en toda consulta. Nada de SQL crudo fuera de ahí
- `findById(id, ctx.conjuntoId)`, nunca `findById(id)` a secas. Cuando no aparece se responde **404, no 403** — un 403 confirma que el recurso existe, y esa confirmación ya es información filtrada
- **Identificadores expuestos como UUID**
- Archivos: ruta con el conjunto adentro y nombre aleatorio (`conjunto/{uuid}/documentos/{uuid}.pdf`), almacenamiento no público, descarga por endpoint validado
- Mensajes de error sin datos de la fila que falló: `"No encontrado"`, nunca `"La reserva pertenece al conjunto Mirador"`

**Dos pruebas en la Definition of Done:**

1. **Prueba del intruso.** Usuario de A pide recurso de B por identificador → 404. La misma petición con `conjunto_id` de B en la URL → rechazada. Un listado con datos de A y B devuelve solo los de A
2. **Prueba de tablas globales.** Un recorrido por el esquema **falla** si alguna tabla fuera de la lista cerrada carece de `conjunto_id`

**Row Level Security se evaluó y se descartó.** Es la única defensa que protege contra un error que nadie revisó, pero exige que la conexión lleve una variable de sesión bien puesta en todas partes. Sostener eso cuesta más que las FK compuestas, que ya hacen imposible el dato cruzado en el punto donde nace.

### 5.5 Vínculos de unidad

Un rol responde _"¿qué puede hacer esta persona en el sistema?"_. El vínculo responde _"¿qué posición jurídica tiene sobre ese inmueble?"_. Son ejes independientes; mezclarlos produce el árbol de `IF` que se quiere evitar.

```
VinculoUnidad
  conjunto_id
  persona_id                  -- referencia a la tabla global
  unidad_id
  tipo ∈ {propietario, arrendatario}
  vigencia_desde
  vigencia_hasta   (nullable — abierto = vigente)
  reside : bool
```

|Situación real|Cómo se modela|
|---|---|
|Dueño que vive en su apartamento|`propietario` · `reside = true`|
|Dueño que arrienda y vive en otra parte|`propietario` · `reside = false`|
|Arrendatario|`arrendatario` · `reside = true`|
|Apartamento con dueño y arrendatario|dos vínculos sobre la misma unidad|
|Arrendatario que se va|se cierra `vigencia_hasta`; el vínculo **no se borra**|

> [!NOTE] Sobre el término `arrendatario` La Ley 675 y la C-318/02 usan _tenedor_, que cubre además al usufructuario y al comodatario. El equipo lo renombró a **arrendatario** porque es la palabra que usa un administrador real y la que aparece en pantalla. **La obligación legal de notificar al propietario y al tenedor no cambió de alcance porque el sistema cambiara de palabra**: un usufructuario se registra como `arrendatario` y la notificación llega igual.

**Consecuencia sobre el rol Residente.** El derecho a reservar **no nace del rol**: nace de tener un vínculo vigente con `reside = true`. Un propietario no residente puede tener el rol Residente sin poder reservar. El permiso dice _puede intentarlo_; el vínculo dice _tiene derecho_.

**Enrutamiento de notificaciones** — no es un `IF` sobre roles, es una consulta sobre vínculos según la naturaleza del hecho:

|Hecho|Destinatario|
|---|---|
|Reserva, anuncio operativo, visitante en portería|Vínculos con `reside = true`|
|Convocatoria y acta de asamblea|**Propietario** (art. 39)|
|Comunicación de infracción|**Propietario y arrendatario**, ambos (C-318/02)|
|Mora y paz y salvo|**Propietario** — es el obligado|

El enrutamiento decide **a quién**; el canal decide **por dónde**.

### 5.6 Parqueaderos

**Un parqueadero se asigna a un apartamento.** Sin regímenes jurídicos, sin origen documental, sin advertencias legales. El sistema registra un hecho administrativo, no constituye un derecho.

```
Parqueadero                    AsignacionParqueadero
  conjunto_id                    parqueadero_id
  codigo                         unidad_id
  tipo ∈ {residentes,            vigencia_desde
          visitantes}            vigencia_hasta   (nullable)
  accesible : bool               registrado_por
  notas
```

Un parqueadero de residentes tiene **una asignación vigente a la vez**. Cerrarla es poner `vigencia_hasta`, nunca borrar: el historial responde "¿desde cuándo parquea ahí?" dos años después.

**Parqueaderos de visitantes.** No se asignan a una unidad. Su ocupación es **temporal y pertenece a la visita**, y termina al registrar la salida. `AsignacionParqueadero` no los admite: el tipo no aparece en el selector, **no es un permiso denegado sino una operación inexistente**.

**Límite duro:** no se puede quitar el parqueadero a un residente moroso ni como sanción. El sistema no tiene ninguna operación de restricción de uso, así que no hay dónde escogerlo.

### 5.7 Secretaría y triage

Hasta hace poco `Secretaría` era una fila del catálogo que ningún flujo nombraba. Un rol así no sobrevive a la primera pregunta del jurado: _¿qué hace esta persona que no pueda hacer el administrador?_

**La respuesta: la Secretaría no decide, clasifica.** Recibe todo lo que entra, lo pone en condiciones de ser decidido, y le devuelve al administrador una bandeja donde lo primero es lo primero.

**El triage separa la forma del fondo.**

- **La forma** — _"¿esto está en condiciones de tramitarse?"_ — es de la Secretaría
- **El fondo** — _"¿esto se concede?"_ — es del Administrador, y no se delega

Sin esa frontera, el filtro se vuelve una segunda instancia decisoria sin responsable.

**Las tres solicitudes** comparten un contrato de triage de tres campos, pero **no son una entidad con subtipos**: cada una tiene su módulo, su ciclo y sus reglas.

|Solicitud|¿Prioridad?|Rechazo formal|Orden en la bandeja|
|---|---|---|---|
|**Cita** con el administrador|Sí|Sí|Prioridad, luego antigüedad|
|**Caso** de un residente|Sí|Sí|Prioridad, luego antigüedad|
|**Evento** (reserva de zona común)|**No**|Sí|**Solo antigüedad**|

**Por qué el Evento no lleva prioridad — esto hay que saber responderlo.** En una cita o un caso el orden es **conveniencia de gestión**: nadie pierde nada porque la fuga del 302 se atienda antes que la queja por ruido del 105. En una reserva el orden es **la promesa de equidad sobre un bien escaso**: hay un solo salón el 31 de diciembre y el sistema prometió que el primero que llega es el primero que puede pedirlo. **Una prioridad sobre eventos convertiría a la secretaría en la asignadora del salón comunal.**

Que el sistema tenga dos disciplinas de cola no es inconsistencia: es que las dos colas existen por razones distintas.

**La prioridad.** Cuatro niveles fijos en código: `BAJA · NORMAL · ALTA · URGENTE`.

- **`NORMAL` lo pone el sistema al crear**, no una persona. Una solicitud sin clasificar entra a la cola igual
- **`URGENTE` exige justificación escrita.** Es el único nivel que cuesta algo escribir, y es el que se iba a inflar
- Todo cambio queda en auditoría con valor anterior, nuevo, actor y fecha. **La prioridad es un campo con historia**
- El administrador puede re-priorizar
- Orden: `prioridad DESC, fecha_creacion ASC`, **no configurable**. No existe la pantalla que lo cambie
- **La vista por antigüedad pura está a un clic** e ignora la prioridad por completo — es la salida de emergencia si algo quedó enterrado
- Sobre Eventos la operación **no existe**: el campo no está en la entidad y el endpoint devuelve 400

**El rechazo por causal formal.** Cierra una solicitud que no está en condiciones de tramitarse, con categoría de **lista cerrada** y explicación escrita. **No existe la categoría `OTRO`** — sería la puerta por la que "no está en condiciones" se convierte en cualquier cosa. (El rechazo del administrador sí tiene `OTRO`, porque él decide de fondo y el fondo no cabe en una lista.)

Es **terminal**: no se reversa, no se edita, el solicitante vuelve a solicitar. En un Caso, cuenta como la respuesta obligatoria. En un Evento, libera la franja y avisa a los suscritos — pero **no consume oportunidad de R9**, porque el residente no dejó vencer nada: le devolvieron la solicitud.

**La bandeja** es una vista, no una entidad. Tres pestañas más vista combinada, filtros, columnas fijas con la **antigüedad siempre visible**. Deliberadamente **no** tiene aprobación, respuesta de fondo, reasignación ni exportación.

**El triage es opcional.** El sistema opera con **cero secretarías**: la prioridad nace en `NORMAL` y la bandeja se ordena sola. Es obligatorio que funcione así, porque en un conjunto pequeño el administrador **es** la secretaría.

**Anuncios con alcance.** Dos modos, y **ninguno es una lista de personas**:

| Alcance              | Quién lo recibe                                                                  | Cómo se resuelve                      |
| -------------------- | -------------------------------------------------------------------------------- | ------------------------------------- |
| **Todo el conjunto** | Toda persona con asignación vigente                                              | Consulta por `conjunto_id`            |
| **Una vivienda**     | Todo vínculo vigente sobre esa unidad — propietario y arrendatario, residan o no | Servicio de enrutamiento por vínculos |

**No existe el alcance "persona"**: entre una vivienda y una persona está la frontera de lo que todavía se puede llamar anuncio. Sigue siendo unidireccional: sin respuesta, sin hilo, sin tiempo real.

### 5.8 Infracciones

**El sistema no sanciona y tampoco modela el procedimiento sancionatorio.** Hace dos cosas: **notifica y registra el desenlace**.

El corte no es de esfuerzo, es de **competencia**: requerir es del administrador (art. 59), decidir es de la asamblea o el consejo (art. 60), y ejecutar ocurre fuera del sistema.

```
RegistroDeInfraccion
  conjunto_id
  unidad_id
  caso_id             (nullable — puede nacer de un Caso o abrirse de oficio)
  descripcion_hecho   (obligatorio, texto libre)
  fecha_hecho
  registrado_por
  fecha_notificacion  (obligatorio — sin comunicación no hay registro)
  cierre_fecha        (nullable)
  cierre_comentario   (nullable, texto libre)
  anulado             (bool — solo el Superusuario, con motivo)
```

**No hay campo `estado`.** Está _abierto_ si `cierre_fecha` es nulo y _cerrado_ si no. Cuando quedan dos situaciones y una fecha las distingue, el `enum` sobra.

**No hay campo de sanción, multa ni restricción.** No están denegados por permiso: **no existen**.

**Lo duro:**

- `fecha_notificacion` es obligatoria. Un registro sin comunicación es una anotación privada sobre una persona identificada, y eso es tratamiento sin finalidad legítima
- La notificación alcanza a **propietario y arrendatario** (C-318/02)
- El registro **nunca** llega al tablón de anuncios
- Visibilidad restringida a Administración, Consejo y vínculos vigentes de la unidad
- No hay borrado. Un registro equivocado se **anula** con motivo, y solo el Superusuario

> [!WARNING] El registro no es prueba de debido proceso Demuestra que hubo una comunicación con fecha y destinatario. **No demuestra** que se respetó el derecho de defensa del art. 59, ni que decidió el órgano competente, ni que la decisión quedó en firme. La interfaz tiene que decirlo en el propio registro (R11).

**Consecuencia sobre el motor de reglas:** la regla beta _bloqueo por sanción vigente_ sale del catálogo y **no se reemplaza por una marca manual**. Una casilla que el administrador pueda marcar para impedirle a un residente usar la piscina es, jurídicamente, peor que la máquina de estados que se eliminó. La regla alfa de mora no se toca.

### 5.9 Citas con el administrador

Módulo a la medida, no reutiliza el motor de reservas (R1), pero sí el mecanismo de bloqueo compartido.

**Cambio de horario de atención:**

1. El administrador edita su horario
2. El sistema **detecta las citas que quedan fuera** y las muestra: cuántas, cuáles, de quién
3. Si hay afectadas, el guardado **exige texto de explicación** obligatorio
4. Las afectadas pasan a `CANCELADA_POR_ADMIN` con la explicación adjunta
5. El sistema notifica a cada residente con la explicación y **tres alternativas**

Las alternativas son cercanas en el tiempo, dentro del nuevo horario y libres, y se reparten **sin solaparse** entre afectados. No se bloquean: aceptar una es una reserva normal que puede fallar. El residente puede rechazar las tres y agendar libremente. **El cambio de horario no se bloquea** — bloquearlo obligaría a cancelar cita por cita a mano, que es peor y termina fuera del sistema.

### 5.10 Motor de reglas

**Nivel 0 — Invariantes del sistema.** No son evaluables ni configurables; se garantizan estructuralmente. No hay dos solicitudes bloqueantes sobre la misma franja; no se reserva en el pasado; ninguna consulta cruza `conjunto_id`; no existen dos personas con el mismo documento.

**Nivel 1 — Reglas alfa.** El sistema jamás las ignora y el administrador no las desactiva. Semilla propuesta, **pendiente de cerrar**:

- Solo quien tenga vínculo vigente con `reside = true` puede solicitar a nombre de esa unidad
- Toda decisión queda trazada
- Una regla beta nunca puede relajar una alfa
- El cobro por un bien común solo procede si el reglamento lo autoriza
- La restricción por mora solo aplica a bienes comunes **no esenciales**
- Piscina: menores de 12 años requieren acompañante adulto; salvavidas en los supuestos exigidos

**Nivel 2 — Reglas beta.** Configuradas por el administrador al crear el conjunto, tomadas de su reglamento. **Catálogo de tipos parametrizados, no DSL de texto libre** — un DSL es un proyecto de semestre por sí solo.

Cada regla = tipo + parámetros + área + vigencia + `conjunto_id`. Catálogo inicial, **pendiente de validar contra un reglamento real**: anticipación mínima/máxima · duración máxima · cupo de reservas confirmadas por unidad en ventana móvil · franja horaria permitida por área y día · aforo · requiere paz y salvo · requiere depósito o pago · días no reservables.

**Todas las reglas beta son restrictivas.** Si solo restringen, se evalúan en AND y **el conflicto no existe** — el mismo criterio que llevó a que los permisos sean puramente aditivos.

Los mensajes de rechazo reportan **todas** las reglas que fallaron, no la primera.

**Punto abierto:** vigencia y versionado. Los reglamentos se reforman en asamblea, y una reserva creada bajo la versión 1 no debe romperse cuando entra la versión 2. ¿Snapshot de la versión aplicada en cada decisión?

### 5.11 Invariantes de eliminación

El equipo también se equivoca. Ninguno de estos depende de que alguien recuerde validarlo.

|Invariante|Dónde|Cómo|
|---|---|---|
|**No hay borrado físico** de personas, unidades, reservas, casos, infracciones, actas ni vínculos|BD y Backend|Ninguna FK con `ON DELETE CASCADE`; todas en `RESTRICT`. Esas entidades no exponen operación de borrado: no existe el método ni la ruta|
|**Baja lógica**|Backend|`activo = false` para personas y conjuntos; `vigencia_hasta` para vínculos y asignaciones. Reversible 30 días|
|**Auditoría de solo inserción**|BD|El usuario de aplicación tiene `INSERT` y `SELECT`, no `UPDATE` ni `DELETE`. Es un privilegio, no una convención|
|**No existe borrado masivo**|Backend|Ninguna operación acepta borrar o desactivar por filtro. Siempre por identificador|
|**La anulación no es borrado**|BD y Backend|La fila permanece, tachada y consultable|
|**La aplicación no altera el esquema**|BD|Sin privilegios DDL en producción|
|**Respaldo verificado antes de migración destructiva**|Proceso|Y la restauración probada al menos una vez. Un respaldo que nunca se restauró no es un respaldo|
|**Doble confirmación escrita** para desactivar un conjunto|Backend|Escribir el nombre exacto|
|**Nunca cero gobierno**, en la misma transacción|Backend|La comprobación y el cambio ocurren juntos, o no ocurre ninguno|
|**Desactivar una Persona no la desvincula** de sus conjuntos|Backend|`activo = false` corta el acceso; las asignaciones se cierran una por una con su propio registro|

---

## 6. Sistema visual

Definición visual v1. Implementado en la carpeta `design-system/` del repositorio, generada en Claude Design.

**Alcance de v1: solo modo claro.** El modo oscuro es Condicional, y la disciplina de tokens es lo que hace barato agregarlo después.

### 6.1 Los tres principios

**Dos capas: superficie y acento.** La capa base es el 85 % de lo que se ve —fondo `#F8FAFC`, tarjetas blancas, bordes sutiles— y no se personaliza nunca. El acento del conjunto activo se reserva a **cuatro sitios**: botón primario, ítem activo de navegación, anillo de foco y barra identificadora del conjunto. **Si aparece en un quinto sitio, es un error de implementación, no una variante.**

**Acción y estado no comparten forma.** El verde de marca coincide con el verde de "confirmado". Esa colisión no se resuelve con dos verdes, se resuelve con la forma:

||Forma|
|---|---|
|**Acción**|Relleno sólido, radio 6px, texto blanco — `Confirmar reserva`|
|**Estado**|Fondo suave, pastilla completa, texto oscuro del mismo tono — `Confirmada`|

Nunca existe un botón de fondo suave ni una pastilla de relleno sólido.

**El acento nunca toca la semántica.** `--acento-*` no aparece en ninguna regla que comunique estado, resultado o severidad. Si los chips siguieran al acento, un conjunto con acento vino mostraría las confirmaciones en rojo.

### 6.2 Tokens

Viven en `static/css/tokens.css`. **Ningún componente escribe un hex directamente.**

```css
:root {
  --superficie-0: #F8FAFC;  --superficie-1: #FFFFFF;  --superficie-2: #F1F5F9;
  --borde: #E2E8F0;         --borde-fuerte: #CBD5E1;
  --texto-1: #0F172A;       --texto-2: #475569;       --texto-3: #64748B;

  --estado-tramite-bg: #FEF3C7;  --estado-tramite-txt: #78350F;
  --estado-ok-bg:      #E8F5F0;  --estado-ok-txt:      #05372D;
  --estado-error-bg:   #FEE2E2;  --estado-error-txt:   #7F1D1D;
  --estado-neutro-bg:  #F1F5F9;  --estado-neutro-txt:  #334155;
  --info-bg:           #EAF2FA;  --info-txt:           #0C3765;

  --e-1:4px; --e-2:8px; --e-3:12px; --e-4:16px;
  --e-5:24px; --e-6:32px; --e-7:48px; --e-8:64px;
  --radio-sm:6px; --radio:12px; --radio-full:999px;
  --sombra-flotante: 0 4px 16px rgba(15,23,42,0.12);
}
```

Tres niveles de texto y no más: un cuarto no pasaría 4.5:1 sobre blanco.

**Mapeo de estados al flujo de reserva:** En trámite → `tramite` (ámbar, hay reloj) · Confirmada → `ok` · Rechazada → `error` (decisión negativa de una persona) · **Expirada y Anulada → `neutro`**, porque no son errores: son no-eventos.

**Tipografía: Inter, autoalojada.** No se carga desde Google Fonts: servir tipografías desde un tercero envía la IP de cada residente a ese tercero, y eso es un tratamiento que no está en la autorización de la Ley 1581.

Escala: 12 / 13 / 15 / 18 / 24 / 30 px. Pesos: 400 cuerpo, 500 títulos, 600 solo para la cifra grande de una tesela.

> [!TIP] La regla que más se nota Toda columna de números —unidades, documentos, horas— lleva `font-variant-numeric: tabular-nums`. Sin eso una tabla de apartamentos queda desalineada. Es una línea de CSS.

**Una sola sombra en todo el sistema**, y solo para lo que flota: modal, desplegable, popover. Tarjetas y teselas se separan con borde. Ancho máximo de contenido 1100px; línea de texto máximo 75 caracteres.

### 6.3 Catálogo de acentos

**Ocho opciones cerradas en código, sin selector libre de color.** Un hex arbitrario obliga a validar contraste de una elección ajena: complejidad permanente para un caso que ocurre una vez.

|Slug|50|600|700|900|Contraste|
|---|---|---|---|---|---|
|`verde` _(defecto)_|`#E8F5F0`|`#0E7C66`|`#0B5F4E`|`#05372D`|5.1:1|
|`azul`|`#EAF2FA`|`#1D5FA8`|`#164A85`|`#0C3765`|6.5:1|
|`indigo`|`#EEF0FB`|`#4340A8`|`#363385`|`#1F1D52`|8.3:1|
|`purpura`|`#F4ECF8`|`#6B2D8C`|`#55236F`|`#351646`|8.8:1|
|`vino`|`#FAECEF`|`#9B2242`|`#7C1B35`|`#4C1020`|7.8:1|
|`terracota`|`#FBEDE7`|`#A8451E`|`#863718`|`#4F1F0C`|6.0:1|
|`ocre`|`#FAF0DF`|`#8A5A0F`|`#6E4709`|`#422A04`|5.9:1|
|`pizarra`|`#EEF1F5`|`#41586F`|`#334659`|`#1E2A36`|7.4:1|

**Por qué existe la personalización, y no es estética.** Una persona puede pertenecer a varios conjuntos y cambiar entre ellos (HU-26). Que el color cambie al cambiar de conjunto es una señal permanente de dónde estás operando, y **reduce el riesgo de actuar en el conjunto equivocado**. Ese es el argumento que se defiende.

En base de datos se guarda el **slug**, nunca un hex. El elemento raíz lleva `data-acento="{{ slug }}"` y el CSS resuelve el resto. Sin recompilar, sin una hoja por conjunto, sin JavaScript.

> [!IMPORTANT] Aplazado el 2026-09-11 — se arranca con un solo acento
> Hasta nueva orden, la implementación usa **un único acento**. No se implementa el campo de acento por conjunto ni el atributo `data-acento`. El catálogo de ocho queda **aplazado, no eliminado**: la disciplina de tokens es justamente lo que mantiene barato reactivarlo.
>
> Razón: el esfuerzo del arranque va al núcleo —aislamiento, concurrencia, auditoría— y no a la personalización.
>
> **Choque pendiente de resolver.** Según la revisión del 7 de septiembre de 2026, la carpeta `design-system/` generada en Claude Design no coincide con este §6: usa un solo acento, Archivo + Inter en vez de solo Inter, y `--radio-control: 4px` en vez de 6px. Ese choque **no está en §12** y se decide cuando se trabaje el frontend.

### 6.4 Bento grid — dónde sí

El bento es un patrón de **panel heterogéneo**, no de aplicación. Se usa en tres vistas: inicio de Administración, inicio de Residente, panel de Vigilancia. **No se usa** en personas, unidades, bandejas, registro de actividades, reservas, formularios ni detalle de nada.

Rejilla de 12 columnas, gap 16px, altura de fila 140px. **Cuatro tamaños y ninguno más**: `4x1`, `6x1`, `6x2`, `12x1`. Máximo 6 teselas por vista. Bajo 900px colapsan a ancho completo.

Cuatro tamaños fijos es lo que separa un bento de un collage. Si un contenido no cabe en ninguno, no es una tesela: es una vista propia con enlace desde el panel.

### 6.5 Voz de la interfaz

- **Verbo activo y concreto en botones.** `Confirmar reserva`, no `Enviar`
- **La acción conserva su nombre en todo el flujo.** El botón dice `Confirmar reserva`, el resultado dice `Reserva confirmada`
- **Los errores no se disculpan y no son vagos.** Dicen qué pasó y qué hacer
- **Un estado vacío es una invitación**, con la acción que corresponda debajo
- Frase en mayúscula inicial; nunca versalitas ni todo en mayúsculas

### 6.6 Definition of Done visual

- [ ] Todo texto pasa **4.5:1** contra su fondo; textos grandes 3:1
- [ ] Ningún estado se comunica **solo con color**: siempre hay texto
- [ ] El foco de teclado es visible y la vista se recorre con `Tab`
- [ ] Toda área táctil mide al menos 44×44px
- [ ] Usable a 200 % de zoom y a 360px de ancho
- [ ] No hay hex dentro de un componente
- [ ] `--acento-*` no aparece en ninguna regla de estado
- [ ] Los formularios tienen `label` asociado, no solo `placeholder`

---

## 7. Stack técnico

> [!DANGER] Decisión bloqueada — leer antes de escribir cualquier código **El frontend está definido de dos formas incompatibles en documentos ambos vigentes.** Ver §12.1. Hasta que el equipo cierre esto, ningún agente debe asumir uno u otro.

### 7.1 Lo que sí está cerrado

**Backend: Django 5.2 LTS + Django REST Framework + PostgreSQL 16+.**

Por qué Django y no FastAPI — la comparación no se gana con "cuál es más moderno" sino con qué exige AdMind:

|Lo que el diseño exige|Django|FastAPI|
|---|---|---|
|Autenticación, hash, sesiones, recuperación|De fábrica|Desde cero|
|Catálogo de permisos y comprobación por vista|Sí|Desde cero|
|Migraciones versionadas|`makemigrations`|Alembic a mano|
|Panel para cargar datos semilla|`django-admin`|No existe|
|2FA TOTP|`django-otp`, maduro|Librería suelta|
|ORM con managers personalizables (el filtro por conjunto)|Sí|SQLAlchemy, más manual|

El Sprint 1 completo —login, 2FA, roles, conjunto activo, 25 SP— es en Django mayoritariamente configuración y modelos. En FastAPI es construir autenticación desde cero mientras se aprende POO.

_Contrapunto listo para el jurado:_ FastAPI es más rápido y tiene `async` nativo, pero **nada de eso es el cuello de botella de AdMind** — la latencia la decide la transacción en PostgreSQL, idéntica en ambos. Se eligió por identidad, permisos, auditoría y migraciones, no por benchmarks que no aplican.

**Por qué la 5.2 y no la 6.1:** LTS con soporte hasta abril de 2028 contra abril de 2027, y más de un año de material acumulado. Para aprender, la versión con más material gana a la más nueva.

**Por qué PostgreSQL desde el día 1 y nunca SQLite.** Tres cosas que SQLite no da:

- **Índice único parcial** (`UNIQUE ... WHERE estado IN (...)`) para la solicitud bloqueante — R7
- **Llaves foráneas compuestas** contra claves únicas compuestas — el corazón del blindaje R6
- **Privilegios por tabla** para que la aplicación no tenga `UPDATE` ni `DELETE` sobre auditoría

Desarrollar en SQLite y migrar después es descubrir en el Sprint 5 que la mitad de los invariantes no se pueden implementar.

> [!NOTE] Entorno real de la máquina de desarrollo (verificado el 2026-09-11)
> Python **3.14.3**, el único instalado — Django 5.2 lo soporta desde el parche **5.2.8** · Git 2.53 · **Docker no instalado** · **PostgreSQL 18** corriendo como servicio de Windows `postgresql-x64-18` en el puerto 5432 · terminal por defecto, PowerShell.
>
> El Postgres nativo ya da las tres cosas que el diseño exige, así que **no bloquea el arranque ni la Fase 0**. Docker sigue siendo deseable para que los dos entornos sean idénticos; queda como pendiente de infraestructura, no como requisito previo.

> [!TIP] FK compuestas en Django — el detalle técnico que va a preguntar el jurado `CompositePrimaryKey` de Django 5.2 **no es lo que se necesita y además rompe el admin**. El caso es una FK compuesta contra una **clave única**, con PK UUID normal. Tres piezas:
> 
> 1. FK normal (`area = models.ForeignKey(Area, ...)`) más el campo `conjunto`
> 2. `UniqueConstraint(fields=["id", "conjunto"])` en el modelo padre
> 3. Una migración con `RunSQL` que añade `ALTER TABLE ... ADD CONSTRAINT ... FOREIGN KEY (area_id, conjunto_id) REFERENCES areas (id, conjunto_id)`
> 
> Django no sabe que esa restricción existe; **PostgreSQL sí, y la impone**. Va como ADR.

**Otras piezas cerradas:** pruebas con `pytest` + `pytest-django` y `factory-boy` · entorno con Docker Compose · Git + GitHub + GitHub Projects · correo por **SMTP** con contraseña de aplicación en variables de entorno, nunca en el repositorio · OAuth descartado a favor de usuario/contraseña + TOTP.

### 7.2 Piezas técnicas que solo AdMind necesita

Aquí no hay tutorial que copiar. **Esta parte es el proyecto**, y es lo que se sustenta.

1. **Aislamiento multiconjunto (R6).** Middleware que resuelve el conjunto activo desde la sesión; `Manager` base que inyecta el filtro; ningún controlador acepta `conjunto_id`. Más la prueba transversal de tablas globales (R12)
2. **Transacciones y concurrencia (R1, R7).** `transaction.atomic`, `select_for_update`, índice único parcial como red de seguridad. Prueba obligatoria: N solicitudes simultáneas producen exactamente un bloqueo
3. **Auditoría de solo inserción.** No es código: son **privilegios de PostgreSQL**, en una migración con `RunSQL`, probados intentando un `UPDATE` que debe fallar
4. **2FA para permisos sensibles.** `django-otp` más un permiso de DRF que verifique el 2FA cuando el permiso está marcado como sensible

### 7.3 El proyecto espejo — desde el 2026-09-11, la rama `lab`

**El repositorio aparte se descartó.** Su función la cumple una rama `lab` dentro del repositorio real, que **solo usa Alejo** y que **nunca se fusiona** hacia `desarrollo`. Lo que funciona en el lab no sube: se vuelve a construir en `desarrollo` (hasta el 2026-09-14 lo reescribía Alejo sin mirar, como prueba de que aprendió; ver la nota de abajo). El detalle operativo está en `Admind_Lab.md`, que es además lo que lee un agente de IA antes de trabajar en el proyecto.

La razón original sigue en pie —**aprender es romper cosas**, y romper cosas en el repositorio que se va a sustentar es mala idea—, pero una rama que nunca sube da la misma protección sin un tercer repositorio que mantener. Lo que se pierde: el lab arrastra la estructura del repositorio real, así que no es el lienzo en blanco que era MiniAdmind.

> [!NOTE] Desde el 2026-09-14 el lab es opcional
> Con el plazo reducido a un mes (§11), los ejercicios se hacen solo si hay tiempo. Lo que no se ensaye en el lab se construye directamente en el producto, y ya no hace falta reescribirlo sin mirar (§8.4).

Alcance, y no crece: un conjunto, dos usuarios, un área, franjas de una hora, el ciclo mínimo bloquear → solicitar → aprobar/rechazar. Sin correo, sin 2FA, sin auditoría, sin documentos, sin visitantes.

|#|Debe funcionar|
|---|---|
|M1|El residente ve el calendario con franjas libres y ocupadas|
|M2|"Reservar" toma un bloqueo exclusivo y arranca una cuenta de 3 minutos visible|
|M3|**Con dos navegadores abiertos, solo uno consigue el bloqueo**|
|M4|**Si vencen los 3 minutos, la franja se libera sin ningún proceso en segundo plano**|
|M5|El administrador ve la bandeja por antigüedad y aprueba o rechaza con categoría|
|M6|Aprobar exige escribir las condiciones y el texto queda congelado|

**M3 y M4 son el objetivo real.** Son la historia de 7 SP usada como referencia de velocidad. Si se resuelven en el lab, se resolvió la parte más difícil antes de que el sprint que la contiene llegue. Los demás criterios (M1, M2, M5 y M6) son CRUD corriente: se construyen directamente en el producto y no se ensayan aparte.

---

## 8. Proceso y trabajo colaborativo

### 8.1 Scrum instanciado

**Sprints de 2 semanas**, duración fija. Un semestre de 16 semanas da 6–7 sprints reales. Con sprints de 1 semana se pasa más tiempo en ceremonias que programando.

|Evento|Duración para dos personas|
|---|---|
|Sprint Planning|1–1.5 h|
|Daily|5–10 min, **escrita y asíncrona**|
|Refinement|1 h por sprint|
|Sprint Review|45 min, **demo funcionando, no diapositivas**|
|Retrospective|30 min, **1–2 acciones concretas con responsable**|

**Reglas duras:** la duración no cambia entre sprints (es lo que permite medir velocidad) · **no se agrega alcance a mitad de sprint** — lo urgente entra al backlog para el siguiente.

**La Daily escrita es mejor que la hablada** en este contexto: queda registro y sirve como evidencia ante el jurado.

**Definition of Done** — la misma para todo el proyecto:

```
Una historia está TERMINADA cuando:
- [ ] El código está en la rama `develop`
- [ ] Pasó revisión de código del otro integrante (PR aprobado)
- [ ] Cumple todos sus criterios de aceptación
- [ ] Tiene pruebas unitarias de la lógica crítica y todas pasan
- [ ] El endpoint está documentado
- [ ] No rompe funcionalidad existente
- [ ] Está desplegada en el ambiente de pruebas
- [ ] Fue probada manualmente al menos una vez por quien NO la programó
```

Sin DoD, "terminado" significa cosas distintas para cada uno y el proyecto acumula deuda invisible.

> [!WARNING] La DoD y el modelo de ramas del curso no están alineados (2026-09-11)
> La DoD dice `develop` y la ruta de aprendizaje asume una rama por historia. El modelo que fijó el profesor (§8.5) usa `main`, `desarrollo` y `pruebas`, **sin ramas por historia**.
>
> Traducción provisional, pendiente de confirmar con el profesor: el código vive en `desarrollo`, el PR revisado por el otro integrante es `desarrollo → pruebas`, y _"desplegada en el ambiente de pruebas"_ es lo que está en `pruebas`. Ver §12.7 a.

**Evidencias que se documentan desde el Sprint 1** — reconstruirlas al final es imposible y el jurado lo nota: Product Backlog con criterios y estimaciones · acta de Planning por sprint · registro de dailies · evidencia de Review · acta de Retrospective · gráfico de velocidad · burndown de al menos un sprint · DoD · historial del tablero · commits y PR vinculados a historias.

**Argumento fuerte ante el jurado:** mostrar cómo la retroalimentación de un Review **cambió** el backlog del siguiente sprint. Eso demuestra ciclo empírico, no solo bloques de dos semanas.

**Nota de vocabulario:** la Guía Scrum eliminó "Development Team" en 2020 y ahora habla de _Developers_ dentro de un único Scrum Team. Mencionar la actualización en la sustentación suma puntos.

### 8.2 Arquitectura de repositorios y documentación

**Decidido por el equipo:** toda la documentación se centraliza en Git. **Google Drive queda solo para entregables congelados** que el docente exige en Excel o Word — artefactos, no fuentes.

Razón: una segunda fuente en Drive produce divergencia silenciosa (Drive no resuelve conflictos, crea `archivo (1).md`), pierde el versionado junto al código, y un agente de IA no puede leerla.

**Estructura: tres repositorios hermanos, no submódulos.**

```
AdMind/
├─ admind-api/          repo 1 — backend
├─ admind-web/          repo 2 — frontend
└─ admind-docs/         repo 3 — documentación   [ya creado]
```

Se descartaron los submódulos de Git a pesar de resolver bien la sincronización, por costo operativo: un `pull` **no** actualiza el submódulo (requiere `git submodule update`), editar una línea son cuatro operaciones de Git repetidas en dos repos padre, y los submódulos se clonan en _detached HEAD_, donde un commit hecho sin checkout previo queda huérfano y desaparece. Para un equipo donde uno de los dos apenas arranca con Git, es una trampa.

**Cómo funciona en la práctica:** tres clones hermanos. Actualizar documentación es el mismo flujo que cualquier repo — rama, commit, push. El agente de IA se abre apuntando a `AdMind/` y ve los tres al tiempo.

**Lo que se pierde frente al submódulo:** la documentación no queda clavada a un commit de código. Se resuelve mirando fechas y commits.

**Routers.** `AGENTS.md` en los tres repos: completo en `admind-docs`, y en los otros dos unas líneas que apuntan a `../admind-docs/`. `CLAUDE.md` es una línea que apunta a `AGENTS.md` — no se hace un archivo por herramienta.

**Regla de los routers:** **apuntan, no resumen.** En el momento en que un router contenga contenido de dominio, hay una segunda fuente de verdad que nadie va a actualizar, y el agente le creerá a la que tiene más cerca.

### 8.3 Compatibilidad Obsidian ↔ GitHub

Alejo trabaja la documentación en Obsidian (abriendo `admind-docs` como bóveda); Camilo la lee renderizada en GitHub. Dos incompatibilidades que conviene conocer:

- **Los `[[enlaces]]` de Obsidian no funcionan en GitHub.** Usar referencias por ID (`R12`, `ADR-27`, `HU-22`), que se leen igual en ambos, o enlaces markdown estándar
- **Callouts:** GitHub solo renderiza `[!NOTE]`, `[!TIP]`, `[!IMPORTANT]`, `[!WARNING]` y `[!CAUTION]`. Los demás (`[!ABSTRACT]`, `[!DANGER]`, `[!TODO]`, `[!QUOTE]`) salen como cita normal. No se rompe nada, pero si se quiere paridad visual, limitarse a esos cinco

### 8.4 Disciplina de trabajo con IA

> [!WARNING] Reversión deliberada — 2026-09-14
> Hasta esta fecha regía un **modo tutor estricto**: la IA explicaba, revisaba y ponía ejercicios, pero no escribía código del producto, y el filtro de abajo era de entrada al repositorio. **El plazo de entrega se redujo a un mes** y no hay que entregar el proyecto completo (§11). Con un equipo de dos que apenas está aprendiendo, ese modo no llega a tiempo, así que Alejo decidió que **la IA construya, pero solo lo que se le pide**. Django y las API se aprenden sobre la marcha. El protocolo operativo está en `Admind_Lab.md` §2.

> [!TIP] El filtro de una sola pregunta **¿Puedo explicar esto ante el jurado?** Hasta el 2026-09-14, si la respuesta era no, no entraba al repositorio. Ahora puede entrar, pero lo que se vaya a defender se entiende antes de la sustentación.

- **La IA construye lo que se le pide, con el alcance exacto del pedido.** Lo que haga falta fuera de él lo avisa y no lo hace
- El diseño del motor de reglas se piensa en papel primero; la IA implementa lo ya especificado
- Las pruebas del núcleo las escribe o revisa el equipo línea por línea
- Bitácora de decisiones (ADR): qué se decidió, qué se descartó, por qué
- Commits pequeños con historial coherente. Conventional Commits con el ID de la historia: `feat(reservas): agregar bloqueo de 3 minutos [HU-11]`
- **Congelar el contrato de la API en el Planning**, antes de programar, para que ambos avancen sin bloquearse
- **Rotar** capas por sprint: si uno hace siempre lo mismo, termina el semestre sabiendo la mitad
- Declarar el uso de IA en la documentación si el curso lo permite. Desde el cambio del 2026-09-14 esto pesa más

**Lo que ayuda:** pedir piezas concretas en vez de módulos enteros · preguntar _por qué_ sobre lo que la IA entregó · pedir el concepto explicado de tres formas · pedir preguntas de jurado sobre el código propio. **Lo que lo arruina:** aceptar código que funciona sin abrirlo y seguir. Se siente como avanzar y llega a la sustentación sin poder explicarlo.

**El techo del proyecto no es cuánto código se puede generar, es cuánto se puede defender en la sustentación.**

### 8.5 Modelo de ramas — requisito del curso

**Definido por el profesor y comunicado el 2026-09-11.** Inicialmente hay tres ramas y ninguna más:

|Rama|Qué contiene|
|---|---|
|`main`|Lo entregado. Recibe de `pruebas` al cerrar el sprint|
|`desarrollo`|Integración. **Los dos integrantes trabajan directamente aquí**|
|`pruebas`|Lo terminado, listo para probar. Es el ambiente de pruebas que exige la DoD|

**No hay ramas por historia.** El equipo sabe que son el estándar de la industria; la instrucción del curso manda. La palabra _inicialmente_ deja la puerta abierta a revisarlo más adelante.

**Lo que hay que compensar al compartir una rama** — es la disciplina del desarrollo sobre tronco común, no un modelo peor:

- `pull` antes de empezar y antes de subir, y subir al menos una vez al día. Guardar trabajo local durante días es lo que hace doler este modelo
- **Nunca subir `desarrollo` roto**: las pruebas en verde antes del `push`. Lo que uno rompe, se lo rompe al otro
- **La trazabilidad pasa al mensaje del commit**, que es donde vive el ID de la historia: `feat(reservas): agregar bloqueo de 3 minutos [HU-11]`. La evidencia que pide §8.1 —_commits y PR vinculados a historias_— se sostiene por ahí
- Repartirse por módulo para no tocar los mismos archivos al mismo tiempo, y coordinarlo en la Daily
- **Limitación aceptada:** un PR `desarrollo → pruebas` arrastra todo lo que haya en `desarrollo`, incluido lo que el otro dejó a medias. Por eso a `desarrollo` solo sube lo que no rompe nada, y la promoción se acuerda entre los dos

**Cuarta rama, solo de Alejo: `lab`.** Práctica y ejercicios. Nunca se fusiona hacia arriba; `desarrollo` sí puede bajar al lab. Pendiente confirmar con el profesor si acepta que exista en el remoto. Ver §7.3 y `Admind_Lab.md`.

**Protección sugerida:** `main` y `pruebas` exigen PR con una aprobación; `desarrollo` queda abierta. En repositorios privados esa opción requiere GitHub Pro, gratis con el GitHub Student Developer Pack.

---

## 9. Decisiones cerradas — no se rediscuten

Cada una tiene razón escrita. Están aquí en forma corta para que nadie las reabra por desconocimiento.

|#|Decisión|
|---|---|
|1|Multi-tenancy en el esquema, no en la interfaz|
|2|Mecanismo de bloqueo compartido entre módulos de capacidad limitada|
|3|Catálogo de reglas parametrizado, **no un DSL**|
|4|Notificaciones como puerto con adaptadores; se implementa Email, WhatsApp queda declarado sin implementar|
|5|El sistema notifica infracciones y registra su desenlace; no modela el procedimiento sancionatorio|
|6|La máquina de estados modela el procedimiento, no la presentación|
|7|El parqueadero se asigna a un apartamento; el régimen jurídico queda fuera del modelo|
|8|Catálogos de roles y permisos fijos en código. Lo que la ley prohíbe no es permiso denegado sino operación inexistente|
|9|Permisos puramente aditivos, sin denegaciones explícitas|
|10|Propietario y arrendatario son **vínculos**, no roles|
|11|La competencia por una franja se resuelve por **orden de llegada**, con evidencia de entrevistas|
|12|La decisión final sobre una reserva es humana y el sistema no valida dinero|
|13|El estado vive en la **solicitud**, no en la franja|
|14|El aislamiento se resuelve en la base y en la capa de acceso, no endpoint por endpoint|
|16|La **anulación** es la respuesta al error humano bajo un modelo sin borrado|
|17|La confirmación es **de contenido, no de intención**|
|18|El abuso del bloqueo se corta con **dos oportunidades**, no con parámetros|
|19|El sistema no le pone plazo al administrador; le ordena la bandeja|
|20|El Registro de actividades es una **vista** sobre la auditoría|
|21|Sin borrado físico; auditoría de solo inserción por privilegios de BD|
|22|El nivel de plataforma tiene **un solo rol** (revierte la separación Operador/Superusuario)|
|23|La **identidad es global**; roles y vínculos son por conjunto|
|24|El documento identifica; la **llave primaria UUID referencia**|
|25|La excepción al aislamiento se declara, se cierra y se prueba|
|26|El acceso de excepción se elimina y su lugar lo ocupa la auditoría|
|27|La prioridad existe **donde no hay un bien escaso en disputa**|
|28|El triage filtra la **forma**; el **fondo** no se delega|
|29|El anuncio tiene dos alcances y **ninguno es una lista de personas**|
|30|El triage es **opcional** y el sistema lo prueba|

_(La 15 fue revertida por la 22 y no se conserva como vigente.)_

**Principio transversal: simplicidad sobre configurabilidad.** Seis versiones seguidas eliminaron parámetros ajustables a favor de mecanismos fijos con una persona resolviendo los casos raros. Cuando dudes, esa es la dirección.

**Segundo principio: documentar las reversiones.** Una decisión revertida se registra como reversión deliberada con su razón, no se borra en silencio. Es lo que permite responder _"¿por qué no hicieron X?"_ con _"lo hicimos y lo quitamos, por esto"_.

---

## 10. Riesgos vivos

|ID|Riesgo|Estado|
|---|---|---|
|**R1**|Tres implementaciones independientes del mismo problema (reservas, parqueadero de visitantes, citas son todos "recurso limitado + concurrencia")|Mitigado: reglas de negocio independientes, **mecanismo de bloqueo y transacción compartido**|
|**R2**|Se captura documento de **toda** persona del sistema, no solo visitantes|**Abierto**: falta justificación escrita de finalidad, plazo de retención y purga|
|**R5**|El catálogo fijo de roles puede no encajar con cargos reales|Mitigado: una persona puede tener varios roles; si falta uno, el equipo lo agrega en código|
|**R6**|El multiconjunto multiplica la superficie de fuga|Mitigado en BD y capa de acceso, con prueba del intruso en la DoD|
|**R7**|La franja queda bloqueada desde el primer clic hasta que el administrador responde|Mitigado: unicidad parcial en BD, expiración evaluada al siguiente acceso|
|**R8**|El administrador es cuello de botella y punto de arbitrariedad|Mitigado: orden fijo no configurable, rechazo con categoría, historial completo|
|**R9**|Bloqueo abusivo de franjas|Mitigado: dos oportunidades por franja|
|**R10**|El **Superusuario** concentra facultades sin control interno y lee datos personales sin procedimiento|**Abierto y es el más caro.** Solo lo mitiga la auditoría. Falta decidir si se registran sus **consultas**, no solo sus escrituras|
|**R11**|Un registro de infracción puede leerse como prueba de debido proceso sin serlo|Mitigado: aviso explícito en el registro y en el manual|
|**R12**|`Persona` global perfora el aislamiento por diseño; la búsqueda por documento es canal de fuga|**Parcial**: falta escribir la lista cerrada de tablas globales y definir el tope de búsquedas|
|**R13**|La prioridad **traslada** el punto de arbitrariedad del administrador a la secretaría|**Parcial**: falta cerrar las tres listas de causales formales|
|**R14**|El anuncio dirigido a una vivienda es mensajería unidireccional con otro nombre|Mitigado por diseño; el aviso en pantalla es lo único que separa el uso correcto del atajo|

---

## 11. Estado de ejecución y backlog

**Corte del seguimiento de velocidad: 2026-09-04.** Sin sprint iniciado.

> [!CAUTION] El plazo de entrega se redujo a un mes (2026-09-14)
> Comunicado por Alejo el 2026-09-14: la entrega queda cerca del **14 de octubre de 2026**, con la fecha exacta por confirmar, y **no hay que entregar el proyecto completo**. Consecuencias:
> - El reparto de siete sprints de dos semanas (§11.2) no cabe: un mes da para dos sprints de esa duración
> - Qué se entrega es decisión del equipo y sigue abierta (§12.8). El §3 ya da el criterio: si solo el Núcleo funciona, el proyecto se sustenta igual
> - Cambió el modo de trabajo con IA (§8.4) y la Fase 0 pasa a ser opcional (§7.3)

> [!NOTE] La demo descartada (2026-09-11)
> En septiembre se construyó una demo navegable en Django —ingreso, panel e unidades— para un entregable de clase. **Se descartó:** estaba hecha por completo con IA y el equipo no podía explicarla. Quedó comprimida en `Backend.zip`, **no se usa como referencia**, y el repositorio volvió a quedar sin código de producto.
>
> No conviene esconderlo: es §8.4 aplicada, y es exactamente el tipo de reversión que §9 manda registrar con su razón. Si el docente vio esa demo, la historia la cuenta el equipo antes de que la pregunten.

### 11.1 Dónde vive cada artefacto

|Artefacto|Ubicación|
|---|---|
|Backlog + HU con story points|Notion → `Gestión Scrum — AdMind` → base **Historias de Usuario**|
|Seguimiento de sprints|Notion → misma página → base **Sprints**|
|Excel V11.1 (entregable que el docente ya conoce, **congelado**)|Drive → `V11.1 Plantilla Product Backlog y HU BORRADOR.xlsx`|
|Plantilla de velocidad|Drive → `Plantilla_Calculo_Velocidad_Scrum.xlsx`|
|Documentación de diseño|`admind-docs` (Git)|

### 11.2 Reparto del backlog

|Sprint|HU|SP|
|---|---|---|
|1|HU-01 a HU-05, HU-26|25|
|2|HU-06 a HU-09|20|
|3|HU-10 a HU-13|26|
|4|HU-14 a HU-19|28|
|5|HU-20, HU-21, HU-25, HU-27, HU-28, HU-29|28|
|6|HU-22, HU-23, HU-24, HU-30 a HU-34|38|
|7|HU-35, HU-36, HU-37|16|
|Condicional|HU-38|7|

**38 historias.** Sprint 1 = identidad, autenticación y conjunto activo. En Django es mayoritariamente configuración y modelos.

### 11.3 Velocidad

- Historia de referencia: **HU-11 · Bloqueo exclusivo de 3 minutos**, 7 SP
- Suma de tareas técnicas: 185 min → **26,43 min por SP**
- Capacidad: 2160 min por sprint → **velocidad teórica de 81,7 SP**
- Pero el reparto implica **≈27 SP por sprint**

**Contradicción reconocida y aceptada.** El punto débil son los 185 minutos: implican resolver una historia de 7 SP en poco más de 3 horas entre dos personas, incluyendo transacción en base de datos, expiración de bloqueo y pruebas de concurrencia. Si toma 9–10 horas, el minuto por SP sube a ≈80 y la velocidad aterriza cerca de 27 SP.

**Decisión: no se corrige antes de arrancar.** El Sprint 1 dirá cuál cifra se parece a la realidad.

**Método de recálculo acordado con el docente** — velocidad empírica con promedio móvil:

1. Solo cuenta lo terminado. Una HU al 80 % aporta **0 SP**; lo inconcluso vuelve al backlog con sus SP intactos
2. Los SP **no se reestiman** porque una historia resulte más difícil: esa información entra por la velocidad
3. Se registran comprometidos y completados; el ratio es la evidencia de mejora para la sustentación
4. El Sprint 1 suele ser atípico (montaje de repos y entorno); si queda muy bajo se marca como caso aparte

> [!WARNING] Factor que todavía no está en ningún Excel **Los sprints 1 y 2 van a rendir menos**, porque además de programar se está aprendiendo el lenguaje del framework. Es normal y es medible. Registrarlo en la retrospectiva del Sprint 1 es dato empírico, es lo que Scrum pide, y ante el jurado **explica** la velocidad baja en vez de esconderla.

### 11.4 Bloqueante único

> [!CAUTION] Conseguir un reglamento de propiedad horizontal real + entrevista con el administrador de contacto
> 
> Es el bloqueante más antiguo del proyecto y hoy alimenta **tres catálogos**:
> 
> 1. Las **reglas beta** de reservas
> 2. Las **tres listas de causales formales** de rechazo (Evento, Caso, Cita)
> 3. La **asignación de permisos** de los seis roles fijos — con **Secretaría como el caso más urgente**, porque es el único rol cuyos permisos se definieron desde el diseño y no desde la observación

### 11.5 Pendientes que afectan la sustentación

- [ ] **Confirmar la fecha exacta de entrega y decidir qué se entrega en ese mes** (§12.8). Añadido el 2026-09-14; condiciona el orden de todo lo demás en esta lista
- [ ] **Cerrar la decisión del stack de frontend** (§12.1). Bloquea el arranque del Sprint 1
- [ ] **Documentar formalmente las entrevistas a residentes**: guion, número de entrevistados, hallazgos y cómo cada hallazgo cambió el diseño. Sin esto, el flujo de reserva parece preferencia técnica y no decisión con evidencia
- [ ] **Decidir si las consultas del Superusuario a datos personales quedan en auditoría** (R10)
- [ ] **Escribir la lista cerrada de tablas globales** y la prueba transversal que la impone (R12)
- [ ] Definir el **límite de búsquedas por documento** por administrador y ventana de tiempo (R12)
- [ ] Definir **plazo de retención y purga** de datos de visitantes; justificación escrita de la captura de documento ampliada a toda persona (R2)
- [ ] **Cerrar la lista de reglas alfa** y el catálogo de reglas beta contra un reglamento real
- [ ] Resolver **vigencia y versionado** del motor de reglas: ¿snapshot de la versión aplicada en cada decisión?
- [ ] **Instanciar el Scrum del equipo**: quién es PO, quién es SM, stakeholder externo confirmado
- [ ] Definir de dónde sale `expensa_mensual` por unidad

_Los cuatro siguientes se detectaron el 2026-09-11 al cruzar este documento con la ruta de aprendizaje. Sin confirmar por el equipo._

- [ ] **Alinear la Definition of Done con el modelo de ramas del curso** (§8.1, §8.5 y §12.7 a)
- [ ] **Definir el ambiente de pruebas.** La DoD lo exige desde HU-01 y no hay ninguno definido en ningún documento: tal como está escrita, hoy ninguna historia puede darse por terminada
- [ ] **Decidir los dos usuarios de base de datos** que exige la auditoría de solo inserción: uno dueño, que corre las migraciones, y otro de aplicación sin `UPDATE`, `DELETE` ni DDL. Afecta también cómo `pytest-django` crea la base de pruebas
- [ ] **Ubicar la Fase 0 en el calendario.** La ruta la sitúa en un "Sprint 0" que no existe en el reparto de §11.2, y cuesta 25–30 horas por persona. _Pierde peso desde el 2026-09-14: la Fase 0 es opcional (§7.3)._

### 11.6 Pendientes menores con recomendación ya escrita

¿El documento es obligatorio desde el alta? _(exigirlo bloquea la importación masiva)_ · ¿Qué pasa en un cambio TI → CC? _(actualizar el par en la misma fila, cambio en auditoría; el UUID no se mueve)_ · ¿Un visitante recurrente se vuelve `Persona`? _(no — es un registro de portería con su propia purga)_ · ¿El administrador puede reversar un rechazo formal? _(no; el solicitante vuelve a solicitar)_ · ¿El anuncio a una vivienda alcanza al propietario no residente? _(sí, todo vínculo vigente)_ · ¿Se puede desactivar un conjunto sin borrarlo? _(sí, campo `activo`)_ · ¿Acuse de lectura en anuncios? _(campo, no bloqueo)_ · ¿El residente ve su propia actividad en el registro? _(sí, solo la suya)_ · ¿Se implementa reloj de vencimiento para Casos? _(reevaluar: habría que construirlo entero para un solo módulo)_ · ¿Qué pasa si un visitante se va sin registrar salida? _(liberación manual por vigilancia + listado de ocupaciones abiertas de más de N horas)_

---

## 12. Contradicciones abiertas entre documentos

> [!CAUTION] Ningún agente debe resolver estas por su cuenta Cada punto está sostenido por dos documentos vigentes que dicen cosas distintas.

### 12.1 · El stack de frontend está definido de dos formas incompatibles — **crítica**

|Documento|Qué dice|
|---|---|
|**Ruta de aprendizaje**|**Vue 3 + Vite + Vue Router + Pinia + Axios** contra una API de **DRF**. Dos repositorios separados. Incluye una Fase 2 completa de JavaScript y Vue|
|**Definición visual v1**|_"Dos servidores Python"_, con **`admind-web` renderizando plantillas de Django**, **CSS propio con variables** y **Alpine.js** para lo interactivo. Explícitamente: _"No hay Tailwind, Bootstrap ni framework de componentes"_|

La Definición visual es posterior y referencia a la ruta, así que probablemente el stack **cambió** y la ruta quedó sin actualizar. Arrastra cinco cosas:

- La **Fase 2** de la ruta (dos semanas de estudio de JS + Vue) sobra o no
- La **Definition of Done** exige _"endpoint documentado"_, lo que presupone API separada
- El **checklist de arranque** manda crear `admind-frontend` y levantar Vite
- La convención de ramas y repositorios asume dos repos con contrato de API congelado
- Las tareas marcadas _(frontend)_ en las HU cambian de naturaleza

**Consideración de equipo:** con plantillas de Django + Alpine desaparecen el segundo repo, CORS, el contrato de API congelado y toda la Fase 2 de JavaScript. Para un equipo donde uno de los dos apenas arranca, eso elimina buena parte de los puntos donde se pueden bloquear mutuamente. Con Vue, Camilo tiene que aprender JavaScript, Vue y Git en paralelo. No es solo una elección técnica: es cuánta superficie de fricción se ponen encima.

### 12.2 · El total de story points no cuadra

- **Seguimiento de velocidad:** 188 SP en 38 historias; 181 comprometidos en sprints
- **HU faltantes V11.1:** las nuevas suman 74 SP y _"el backlog completo (HU-01 a HU-38) suma 203"_

Diferencia de **15 SP**. Uno de los dos números está desactualizado y ambos se usan para planear.

### 12.3 · La personalización visual cambió y la propuesta no lo refleja

|Documento|Qué dice|
|---|---|
|**Propuesta V11**|_"Un color base del que se deriva la paleta, más el logo"_|
|**Definición visual v1**|**Catálogo cerrado de 8 acentos por slug**, sin selector libre. **Logo por conjunto fuera del alcance de v1**|
|**HU-26**|La pantalla de selección muestra _"nombre, logo y color base de cada conjunto"_|

El sistema visual es el más reciente y el más razonado — mantiene la forma del principio de no-configurabilidad, cambiando solo quién elige la fila. Falta propagarlo a la propuesta y a los criterios de aceptación de HU-26.

### 12.4 · PB-08, canal de notificaciones: núcleo sin trabajo estimado

El canal es un **componente explícito del núcleo** que debe construirse **antes** que sus seis consumidores (enrutamiento por vínculos, bandeja del administrador, registro de pago, campana, anulaciones del Superusuario, tablón). No tiene HU propia ni story points en ningún sprint; se asume absorbido por otras historias. El propio seguimiento de velocidad marca la duda: _vale la pena confirmar que su costo está realmente absorbido y no simplemente omitido._

### 12.5 · Sprint 6 sobrecargado con dependencia cruzada

38 SP contra un promedio de 26, y concentra las tres historias de Secretaría. **HU-22 (bandeja de triage) depende de HU-29 (Casos, Sprint 5) y HU-31 (Citas, Sprint 6)** — HU-31 tiene que cerrarse antes que HU-22 dentro del mismo sprint.

### 12.6 · Menores

- **Escala de puntos lineal (2–9), no Fibonacci**, mientras el documento de proceso enseña Fibonacci. Funciona, pero hay que tener la justificación lista por si el jurado pregunta
- **PB-06, PB-16, PB-19 y PB-24** siguen sin HU propia por decisión del equipo, cubiertos dentro de otras historias
- La ruta de aprendizaje nombra al compañero como **"Sergio"**; es **Camilo**
- Existían dos copias idénticas de la Propuesta V11 (`Propuesta_V11.md` y `claude_Propuesta_V11.md`), diferenciadas solo por el formato de los callouts. Conservar una sola

### 12.7 · Detectadas el 2026-09-11, cruzando este documento con la ruta de aprendizaje

_Sin confirmar por el equipo. Se listan para que no se pierdan, no como hechos._

**a) El modelo de ramas del curso contra la DoD y la ruta.** La DoD (§8.1) dice `develop` y la ruta enseña una rama por historia con PR; el profesor fijó `main`, `desarrollo` y `pruebas` sin ramas por historia (§8.5). Falta decidir qué PR cuenta como la revisión que exige la DoD, y dónde queda el "ambiente de pruebas".

**b) Token contra sesión.** La ruta enseña autenticación por token con un interceptor de Axios (Fase 2), pero su propia Fase 3.1 y el §5.4 de este documento dicen que el conjunto activo **sale de la sesión** y que ningún controlador acepta `conjunto_id`. Con un token sin estado hay que decidir dónde vive el conjunto activo; si viaja en una cabecera, es un parámetro con otro nombre. **Pesa directamente en §12.1:** con plantillas de Django la sesión es nativa; con Vue hay que diseñarlo (por ejemplo, autenticación por sesión de DRF en lugar de token).

**c) "Un solo bloqueo activo en todo el sistema" contra "toda clave única incluye `conjunto_id`".** El §5.1 dice que un residente solo puede tener un bloqueo activo en todo el sistema; el §5.4 exige que toda clave única lleve `conjunto_id`. Una persona puede tener rol de Residente en dos conjuntos. Si la frase es literal, esa restricción cruza conjuntos y es una excepción al aislamiento que no está en la lista cerrada de tablas globales (R12); si no lo es, hay que corregir la redacción.

### 12.8 · Detectada el 2026-09-14: el plan del semestre contra el plazo de un mes

_El plazo es un hecho. Lo abierto es qué hacer con él, y ningún agente recorta alcance por su cuenta._

|Fuente|Qué dice|
|---|---|
|**§8.1 y §11.2**|Siete sprints de dos semanas, 38 historias, la misma duración en todos los sprints|
|**Plazo comunicado el 2026-09-14**|Un mes para entregar, sin exigir el proyecto completo|

Falta decidir:

- **Qué historias entran.** El §3 da el orden (Núcleo, Comprometido, Condicional), pero no dice cuánto del Núcleo cabe en un mes
- **Cuántos sprints y de qué duración.** La regla de duración fija (§8.1) existe para medir velocidad, y el §11.3 dejaba que el Sprint 1 calibrara la cifra
- **Qué evidencias de Scrum del §8.1 se alcanzan a producir**, porque el jurado las va a pedir igual

---

## 13. Qué está decidido y qué está propuesto

> [!IMPORTANT] Un agente no debe tratar estas dos columnas igual Lo de la izquierda son hechos del proyecto. Lo de la derecha son sugerencias sin confirmar por el equipo.

|Decidido por el equipo|Propuesto, sin confirmar|
|---|---|
|Documentación centralizada en Git; Drive solo para entregables congelados|Nomenclatura numerada por decenas (`01-ESTADO`, `10-PRODUCTO`, …) con la versión fuera del nombre del archivo|
|Tres repositorios hermanos; `admind-docs` **ya creado**|Quitar el prefijo `claude_` de los nombres y llevar el origen al frontmatter|
|Submódulos de Git descartados|Reparto de roles Scrum: Camilo como PO, Alejo como SM|
|Backend Django 5.2 LTS + DRF + PostgreSQL|Reparto de trabajo por **módulos verticales** en vez de por capas|
|Sprints de 2 semanas, 7 sprints, DoD escrita|Regla de revisión de PR: _"el revisor aprueba cuando puede explicar qué hace el PR"_|
|Sistema visual v1; el catálogo de 8 acentos queda **aplazado** y se arranca con uno solo (§6.3)|Monorepo como alternativa a los tres repos, si los dos repositorios no son requisito del curso|
|Todo lo de §3 (alcance), §4 (legal), §5 (diseño) y §9 (ADR)|Referenciar siempre por ID en vez de `[[enlaces]]` de Obsidian|
|**Modelo de ramas del curso**: `main`, `desarrollo` y `pruebas`, sin ramas por historia (§8.5)|Reescribir la DoD con el vocabulario de ramas del curso|
|**El proyecto espejo es la rama `lab`**, no un repositorio aparte (§7.3)|Subir la rama `lab` al remoto, por confirmar con el profesor|
|**Plazo de entrega de un mes**, sin exigir el proyecto completo (comunicado el 2026-09-14, §11)|Recorte de alcance y número de sprints para el plazo nuevo (§12.8)|
|**La IA construye lo que se le pide, con alcance exacto**, y el lab queda opcional (Alejo, 2026-09-14, §8.4 y §7.3)|Declarar formalmente el uso de IA en la documentación del curso (§8.4)|

---

## 14. Control de cambios

|Versión|Fecha|Cambios|
|---|---|---|
|1|2026-09-11|Versión inicial. Consolida Propuesta V11, Guía legal v1.0 (2026-08-20), Definición visual v1, Ruta de aprendizaje, Contexto Scrum, Seguimiento de velocidad (corte 2026-09-04), HU V11.1 y las decisiones de infraestructura documental tomadas en septiembre. Omite el historial de versiones v5–v9 salvo donde explica una decisión vigente|
|1.1|2026-09-11|Corrige el punto de partida técnico de Camilo y su consecuencia sobre §12.1 (§2) · aplaza el catálogo de acentos y deja el choque con `design-system/` anotado (§6.3) · registra el entorno real de la máquina (§7.1) · sustituye el repositorio MiniAdmind por la rama `lab` (§7.3) · añade el modelo de ramas del curso (§8.5) y su desalineación con la DoD (§8.1) · registra la demo descartada (§11) · añade cuatro pendientes (§11.5) y tres contradicciones detectadas (§12.7) · dos filas nuevas en §13. Documento nuevo: `Admind_Lab.md`|
|1.2|2026-09-14|Registra el plazo de entrega reducido a un mes (§11, §11.5) y la contradicción que abre con el plan de siete sprints (§12.8) · revierte el modo tutor estricto: la IA construye lo que se le pide, con alcance exacto (§8.4) · el lab pasa a ser opcional (§7.3) · dos filas nuevas en §13. `Admind_Lab.md` reescribe su §2 y ajusta §3, §6, §8, §9 y §10|