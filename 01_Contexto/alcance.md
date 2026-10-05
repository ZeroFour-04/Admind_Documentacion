---
resumen: "Alcance en cuatro niveles: Núcleo, Comprometido, Condicional y Fuera de alcance."
tipo: contexto
origen: "maestro v1.4 (2026-09-14) §3"
actualizado: 2026-09-14
---

# Alcance, en cuatro niveles

> [!WARNING] Decisiones posteriores a este texto
> - **Plazo:** entrega cerca del 2026-10-14 y no se entrega completo. Qué entra sigue abierto ([abiertas](../06_Decisiones/abiertas.md), §12.8); ningún agente recorta alcance por su cuenta.
> - **Roles (2026-09-29):** una persona tiene un solo rol vigente por conjunto. Donde 3.1 dice *unión de todos los roles*, ver [permisos](../05_Modulos/permisos.md).
> - **Logo por conjunto (3.3):** desde el 2026-09-29 existe la foto 1:1 del conjunto (HU-21). Ver [conjuntos](../05_Modulos/conjuntos.md).

El alcance es el instrumento de control de riesgo del proyecto. Está escrito así a propósito: **si solo el Núcleo funciona, el proyecto se sustenta igual.**

## 3.1 Núcleo — esto _es_ el proyecto

**Multiconjunto**

- El permiso `conjunto.crear` es del rol de plataforma Superusuario, no del administrador
- Creación por asistente. El conjunto **no queda operativo** hasta completar: datos básicos, catálogo de áreas, al menos un usuario con rol Administración, y reglamento cargado
- **Las reglas beta se configuran al crear el conjunto**, no después. Un conjunto sin reglas acepta cualquier reserva
- Selector de conjunto activo. Todo lo que se ve y se escribe pertenece al conjunto activo

**Identidad de personas**

- `Persona` es **global a la plataforma**, única por `(tipo_documento, numero_documento)`
- Tipos de lista cerrada: `CC`, `TI`, `CE`, `PAS`, `PPT` (revisada el 2026-09-14, ver §5.2)
- **La llave primaria es un UUID**, no el documento
- El número se **normaliza al guardar**: sin puntos, sin espacios, sin ceros a la izquierda
- Aplica a todos: residentes, vigilancia, secretaría y administración

**Reserva de zonas comunes**

- Salón comunal, piscina, gimnasio, y catálogo de áreas ampliable por conjunto
- Ciclo: bloquear 3 min → llenar → confirmar contenido → solicitar → validar reglas → revisión del administrador → aprobar o rechazar → cancelar
- Un área se identifica por su nombre dentro del conjunto: no lleva tipo ni clasificación (decisión del 2026-10-05)

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

## 3.2 Comprometido — segunda prioridad

Gestión de visitantes · Casos · Infracciones (registro) · Citas con el administrador · Bandeja de triage de Secretaría · Comunicación con residentes (tablón + notificaciones) · Repositorio de documentos · Parqueaderos de residentes · Pago de administración (reporte + confirmación) · Importación masiva CSV/Excel y respaldo

> [!WARNING] Aceptado de entrada **Comprometido puede quedar parcial.** Un proyecto con el núcleo sólido y tres módulos sin empezar se defiende. Uno con doce módulos a medias, no.

## 3.3 Condicional — solo si sobra tiempo

Registro de actividades (vista sobre la auditoría) · Vista consolidada de novedades entre conjuntos · Cobro a visitantes por parqueadero · Mapa de parqueaderos · Plantillas de conjunto · Modo oscuro · Logo por conjunto

## 3.4 Fuera de alcance — fronteras, no pendientes

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

## Ver también

- [personas](../05_Modulos/personas.md) — maestro §5.2
- [riesgos](../06_Decisiones/riesgos.md) — R10
