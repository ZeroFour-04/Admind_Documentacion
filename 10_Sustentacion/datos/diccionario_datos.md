---
resumen: "Diccionario de datos de admind_db generado del esquema real de PostgreSQL y de los modelos de Django."
tipo: estado
origen: "information_schema y pg_catalog de admind_db, cruzados con los modelos del backend (main b89d9f2), 2026-11-14"
actualizado: 2026-11-14
revisado: 2026-11-14
---

# Diccionario de datos de AdMind

- **Base de datos:** `admind_db`, PostgreSQL 18.4 on x86_64-windows.
- **Corte:** 2026-11-14, backend en `main` `b89d9f2`, sin migraciones pendientes.
- **Tablas:** 42 en total: 32 del negocio y 10 del framework (Django y django-otp).
- **Restricciones:** 42 llaves primarias, 111 llaves foráneas, 45 únicas y 63 CHECK.
- **Triggers:** 0. **Procedimientos y funciones:** 0.

## Convenciones

- **Nombre de tabla:** `<app>_<modelo>`, como lo crea Django.
- **Llave:** `PK` llave primaria, `FK → tabla.columna` llave foránea, `UQ` valor único.
- **Nulo:** `No` significa que la columna es obligatoria (`NOT NULL`).
- **Aislamiento entre conjuntos:** las tablas de cada conjunto llevan `conjunto_id` y una única `(id, conjunto_id)`. Sus hijas apuntan a esa pareja con una **llave foránea compuesta**, así la base impide que una fila de un conjunto quede ligada a una de otro.
- **Sin borrado físico:** las filas no se borran; se cierran con una vigencia, un estado o una anulación.
- **Archivos:** fotos, logos y comprobantes se guardan dentro de la base, en columnas `bytea`.

## Personas

Identidad global de cada persona, independiente de los conjuntos.

### `personas_persona`

Modelo de Django: `personas.Persona`.

| Columna | Tipo | Nulo | Llave | Descripción y valores permitidos |
|---|---|---|---|---|
| `id` | uuid | No | PK | Id |
| `tipo_documento` | varchar(3) | No |  | Tipo documento. Valores: `CC`, `TI`, `CE`, `PAS`, `PPT` |
| `numero_documento` | varchar(20) | No |  | Numero documento |
| `nombres` | varchar(30) | No |  | Nombres |
| `apellidos` | varchar(30) | No |  | Apellidos |
| `telefono` | varchar(10) | No |  | Telefono |
| `activo` | boolean | No |  | Activo |
| `creado_en` | timestamp with time zone | No |  | Creado en |
| `actualizado_en` | timestamp with time zone | No |  | Actualizado en |

**Restricciones de la tabla**

- Única `persona_documento_unico`: UNIQUE (tipo_documento, numero_documento)
- CHECK `persona_documento_normalizado`: `CHECK (((numero_documento) ~ '^[A-Z1-9][A-Z0-9]*$'))`
- CHECK `persona_telefono_valido`: `CHECK ((((telefono) = '') OR ((telefono) ~ '^\+?[0-9]{7,10}$')))`
- CHECK `persona_tipo_documento_valido`: `CHECK (((tipo_documento) = ANY ((ARRAY['CC', 'TI', 'CE', 'PAS', 'PPT']))))`

## Cuentas y sesión

Usuarios que inician sesión y sus tokens de sesión en la API.

### `cuentas_tokendesesion`

La sesión de un usuario en la API (maestro §12.7 b).

Modelo de Django: `cuentas.TokenDeSesion`.

| Columna | Tipo | Nulo | Llave | Descripción y valores permitidos |
|---|---|---|---|---|
| `id` | uuid | No | PK | Id |
| `huella` | varchar(64) | No | UQ | Huella |
| `dos_factores_verificado` | boolean | No |  | Dos factores verificado |
| `creado_en` | timestamp with time zone | No |  | Creado en |
| `vence_en` | timestamp with time zone | No |  | Vence en |
| `conjunto_activo_id` | uuid | Sí | FK → `conjuntos_conjunto.id` | Conjunto activo |
| `usuario_id` | uuid | No | FK → `cuentas_usuario.id` | Usuario |

### `cuentas_usuario`

Modelo de Django: `cuentas.Usuario`.

| Columna | Tipo | Nulo | Llave | Descripción y valores permitidos |
|---|---|---|---|---|
| `password` | varchar(128) | No |  | Contraseña |
| `last_login` | timestamp with time zone | Sí |  | Último inicio de sesión |
| `is_superuser` | boolean | No |  | Indica que este usuario tiene todos los permisos sin asignárselos explícitamente. |
| `id` | uuid | No | PK | Id |
| `correo` | varchar(254) | No | UQ | Correo |
| `is_active` | boolean | No |  | Is active |
| `is_staff` | boolean | No |  | Is staff |
| `creado_en` | timestamp with time zone | No |  | Creado en |
| `persona_id` | uuid | No | FK → `personas_persona.id` · UQ | Persona |

### `cuentas_usuario_groups`

Tabla intermedia creada por Django: relación usuario-group.

Modelo de Django: `cuentas.Usuario_groups`.

| Columna | Tipo | Nulo | Llave | Descripción y valores permitidos |
|---|---|---|---|---|
| `id` | bigint | No | PK | ID |
| `usuario_id` | uuid | No | FK → `cuentas_usuario.id` | Usuario |
| `group_id` | integer | No | FK → `auth_group.id` | Group |

**Restricciones de la tabla**

- Única `cuentas_usuario_groups_usuario_id_group_id_f5ef6c73_uniq`: UNIQUE (usuario_id, group_id)

### `cuentas_usuario_user_permissions`

Tabla intermedia creada por Django: relación usuario-permission.

Modelo de Django: `cuentas.Usuario_user_permissions`.

| Columna | Tipo | Nulo | Llave | Descripción y valores permitidos |
|---|---|---|---|---|
| `id` | bigint | No | PK | ID |
| `usuario_id` | uuid | No | FK → `cuentas_usuario.id` | Usuario |
| `permission_id` | integer | No | FK → `auth_permission.id` | Permission |

**Restricciones de la tabla**

- Única `cuentas_usuario_user_per_usuario_id_permission_id_26c0acea_uniq`: UNIQUE (usuario_id, permission_id)

## Conjuntos

Cada conjunto residencial que administra la plataforma.

### `conjuntos_conjunto`

Modelo de Django: `conjuntos.Conjunto`.

| Columna | Tipo | Nulo | Llave | Descripción y valores permitidos |
|---|---|---|---|---|
| `id` | uuid | No | PK | Id |
| `nombre` | varchar(30) | No |  | Nombre |
| `direccion` | varchar(200) | No |  | Direccion |
| `activo` | boolean | No |  | Activo |
| `operativo` | boolean | No |  | Operativo |
| `creado_en` | timestamp with time zone | No |  | Creado en |
| `acento` | varchar(16) | No |  | Acento. Valores: `verde`, `azul`, `indigo`, `purpura`, `vino`, `terracota`, `ocre`, `pizarra`, `personalizado` |
| `logo_huella` | varchar(64) | No |  | Logo huella |
| `color_personalizado` | varchar(7) | No |  | Color personalizado |

**Restricciones de la tabla**

- CHECK `conjunto_acento_valido`: `CHECK (((acento) = ANY ((ARRAY['verde', 'azul', 'indigo', 'purpura', 'vino', 'terracota', 'ocre', 'pizarra', 'personalizado']))))`
- CHECK `conjunto_color_personalizado_valido`: `CHECK (((((acento) = 'personalizado') AND ((color_personalizado) ~ '^#[0-9a-f]{6}$')) OR ((NOT ((acento) = 'personalizado')) AND ((color_personalizado) = ''))))`
- CHECK `conjunto_logo_huella_valida`: `CHECK ((((logo_huella) = '') OR ((logo_huella) ~ '^[0-9a-f]{64}$')))`

### `conjuntos_logodeconjunto`

La imagen del logo (HU-21). Va en su propia tabla para que cargar un Conjunto no traiga la imagen.

Modelo de Django: `conjuntos.LogoDeConjunto`.

| Columna | Tipo | Nulo | Llave | Descripción y valores permitidos |
|---|---|---|---|---|
| `id` | uuid | No | PK | Id |
| `contenido` | bytea (archivo binario) | No |  | Contenido |
| `tipo` | varchar(20) | No |  | Tipo |
| `subido_en` | timestamp with time zone | No |  | Subido en |
| `conjunto_id` | uuid | No | FK → `conjuntos_conjunto.id` · UQ | Conjunto |

**Restricciones de la tabla**

- Única `conjuntos_logodeconjunto_id_conjunto`: UNIQUE (id, conjunto_id)

## Roles y permisos

El rol vigente de una persona en un conjunto.

### `permisos_asignacion`

El rol del catálogo de una persona en un conjunto. Retirarlo es cerrar la vigencia, no borrar.

Modelo de Django: `permisos.Asignacion`.

| Columna | Tipo | Nulo | Llave | Descripción y valores permitidos |
|---|---|---|---|---|
| `id` | uuid | No | PK | Id |
| `rol` | varchar(30) | No |  | Rol. Valores: `superusuario`, `administracion`, `secretaria`, `vigilancia`, `residente` |
| `vigencia_desde` | date | No |  | Vigencia desde |
| `vigencia_hasta` | date | Sí |  | Vigencia hasta |
| `creado_en` | timestamp with time zone | No |  | Creado en |
| `conjunto_id` | uuid | Sí | FK → `conjuntos_conjunto.id` | Conjunto |
| `persona_id` | uuid | No | FK → `personas_persona.id` | Persona |

**Restricciones de la tabla**

- Índice `asignacion_un_rol_por_conjunto`: único (persona_id, conjunto_id) cuando (vigencia_hasta IS NULL)
- CHECK `asignacion_conjunto_segun_alcance`: `CHECK ((((conjunto_id IS NULL) AND ((rol) = 'superusuario')) OR ((conjunto_id IS NOT NULL) AND ((rol) = ANY ((ARRAY['administracion', 'residente', 'secretaria', 'vigilancia']))))))`
- CHECK `asignacion_vigencia_coherente`: `CHECK (((vigencia_hasta IS NULL) OR (vigencia_hasta >= vigencia_desde)))`

## Viviendas

Agrupaciones (torres, bloques), viviendas y vínculos de las personas con ellas.

### `unidades_agrupacion`

Lo que junta viviendas dentro del conjunto: una torre, un bloque, una manzana (HU-39).

Modelo de Django: `unidades.Agrupacion`.

| Columna | Tipo | Nulo | Llave | Descripción y valores permitidos |
|---|---|---|---|---|
| `id` | uuid | No | PK | Id |
| `etiqueta` | varchar(30) | No |  | Etiqueta |
| `nombre` | varchar(40) | No |  | Nombre |
| `clave` | varchar(80) | No |  | Clave |
| `tipo_vivienda` | varchar(12) | No |  | Tipo vivienda. Valores: `apartamento`, `casa` |
| `orden` | integer | No |  | Orden |
| `creado_en` | timestamp with time zone | No |  | Creado en |
| `conjunto_id` | uuid | No | FK → `conjuntos_conjunto.id` | Conjunto |

**Restricciones de la tabla**

- Única `agrupacion_clave_unica_en_conjunto`: UNIQUE (conjunto_id, clave)
- Única `unidades_agrupacion_id_conjunto`: UNIQUE (id, conjunto_id)
- CHECK `agrupacion_tipo_vivienda_valido`: `CHECK (((tipo_vivienda) = ANY ((ARRAY['apartamento', 'casa']))))`
- CHECK `unidades_agrupacion_orden_check`: `CHECK ((orden >= 0))`

### `unidades_unidad`

Una vivienda del conjunto, apartamento o casa (maestro §5.5, HU-39).

Modelo de Django: `unidades.Unidad`.

| Columna | Tipo | Nulo | Llave | Descripción y valores permitidos |
|---|---|---|---|---|
| `id` | uuid | No | PK | Id |
| `nombre` | varchar(100) | No |  | Nombre |
| `creado_en` | timestamp with time zone | No |  | Creado en |
| `conjunto_id` | uuid | No | FK → `conjuntos_conjunto.id` | Conjunto |
| `numero` | varchar(12) | No |  | Numero |
| `piso` | smallint | Sí |  | Piso |
| `tipo` | varchar(12) | No |  | Tipo. Valores: `apartamento`, `casa` |
| `agrupacion_id` | uuid | Sí | FK → `unidades_agrupacion.id` | Agrupacion |

**Restricciones de la tabla**

- Llave foránea compuesta `unidades_unidad_agrupacion_id_conjunto_fk`: (agrupacion_id, conjunto_id) → unidades_agrupacion(id, conjunto_id) ON DELETE RESTRICT
- Única `unidad_nombre_unico_en_conjunto`: UNIQUE (conjunto_id, nombre)
- Única `unidades_unidad_id_conjunto`: UNIQUE (id, conjunto_id)
- CHECK `unidad_tipo_valido`: `CHECK (((tipo) = ANY ((ARRAY['apartamento', 'casa']))))`
- CHECK `unidades_unidad_piso_check`: `CHECK ((piso >= 0))`

### `unidades_vinculounidad`

La posición jurídica de una persona sobre una unidad (maestro §5.5). No es un rol.

Modelo de Django: `unidades.VinculoUnidad`.

| Columna | Tipo | Nulo | Llave | Descripción y valores permitidos |
|---|---|---|---|---|
| `id` | uuid | No | PK | Id |
| `tipo` | varchar(12) | No |  | Tipo. Valores: `propietario`, `arrendatario` |
| `reside` | boolean | No |  | Reside |
| `vigencia_desde` | date | No |  | Vigencia desde |
| `vigencia_hasta` | date | Sí |  | Vigencia hasta |
| `creado_en` | timestamp with time zone | No |  | Creado en |
| `conjunto_id` | uuid | No | FK → `conjuntos_conjunto.id` | Conjunto |
| `persona_id` | uuid | No | FK → `personas_persona.id` | Persona |
| `unidad_id` | uuid | No | FK → `unidades_unidad.id` | Unidad |

**Restricciones de la tabla**

- Llave foránea compuesta `unidades_vinculounidad_unidad_id_conjunto_fk`: (unidad_id, conjunto_id) → unidades_unidad(id, conjunto_id) ON DELETE RESTRICT
- Única `unidades_vinculounidad_id_conjunto`: UNIQUE (id, conjunto_id)
- Índice `vinculo_vigente_unico`: único (unidad_id, persona_id, tipo) cuando (vigencia_hasta IS NULL)
- CHECK `vinculo_tipo_valido`: `CHECK (((tipo) = ANY ((ARRAY['propietario', 'arrendatario']))))`
- CHECK `vinculo_vigencia_coherente`: `CHECK (((vigencia_hasta IS NULL) OR (vigencia_hasta >= vigencia_desde)))`

## Zonas comunes

Áreas comunes del conjunto, con reserva o con ingreso.

### `areas_area`

Un área común del conjunto (HU-09), con reserva o con ingreso.

Modelo de Django: `areas.Area`.

| Columna | Tipo | Nulo | Llave | Descripción y valores permitidos |
|---|---|---|---|---|
| `id` | uuid | No | PK | Id |
| `nombre` | varchar(80) | No |  | Nombre |
| `descripcion` | text | No |  | Descripcion |
| `hora_apertura` | time | No |  | Hora apertura |
| `hora_cierre` | time | No |  | Hora cierre |
| `duracion_franja_minutos` | smallint | Sí |  | Duracion franja minutos |
| `en_mantenimiento` | boolean | No |  | En mantenimiento |
| `activo` | boolean | No |  | Activo |
| `creado_en` | timestamp with time zone | No |  | Creado en |
| `conjunto_id` | uuid | No | FK → `conjuntos_conjunto.id` | Conjunto |
| `aforo_maximo` | smallint | No |  | Aforo maximo |
| `modo_uso` | varchar(10) | No |  | Modo uso. Valores: `reserva`, `ingreso` |
| `permanencia_maxima_minutos` | smallint | Sí |  | Permanencia maxima minutos |
| `condiciones_alquiler` | text | No |  | Condiciones alquiler |

**Restricciones de la tabla**

- Única `area_nombre_unico_en_conjunto`: UNIQUE (conjunto_id, nombre)
- Única `areas_area_id_conjunto`: UNIQUE (id, conjunto_id)
- CHECK `area_aforo_maximo_valido`: `CHECK ((aforo_maximo >= 1))`
- CHECK `area_duracion_franja_minima`: `CHECK ((duracion_franja_minutos >= 120))`
- CHECK `area_horario_coherente`: `CHECK ((hora_cierre > hora_apertura))`
- CHECK `area_modo_coherente`: `CHECK ((((duracion_franja_minutos IS NOT NULL) AND ((modo_uso) = 'reserva') AND (permanencia_maxima_minutos IS NULL)) OR ((duracion_franja_minutos IS NULL) AND ((modo_uso) = 'ingreso') AND (permanencia_maxima_minutos IS NOT NULL))))`
- CHECK `areas_area_aforo_maximo_check`: `CHECK ((aforo_maximo >= 0))`
- CHECK `areas_area_duracion_franja_minutos_check`: `CHECK ((duracion_franja_minutos >= 0))`
- CHECK `areas_area_permanencia_maxima_minutos_check`: `CHECK ((permanencia_maxima_minutos >= 0))`

## Motor de reglas

Reglas del conjunto (alfa) y de cada zona (beta).

### `reglas_regla`

Una regla del conjunto (alfa, sin área) o de un área (beta): tipo + parámetros + vigencia (HU-10).

Modelo de Django: `reglas.Regla`.

| Columna | Tipo | Nulo | Llave | Descripción y valores permitidos |
|---|---|---|---|---|
| `id` | uuid | No | PK | Id |
| `tipo` | varchar(30) | No |  | Tipo. Valores: `ANTICIPACION_MINIMA`, `ANTICIPACION_MAXIMA`, `REQUIERE_PAZ_Y_SALVO`, `DIA_LIMITE_DE_PAGO`, `DIAS_QUE_NO_ABRE`, `CUPO_POR_UNIDAD`, `ACOMPANANTES`, `UNA_RESERVA_POR_DIA`, `SIN_FRANJAS_SEGUIDAS`, `PARQUEADEROS_POR_VIVIENDA`, `AFORO`, `FRANJA_HORARIA`, `DIAS_NO_RESERVABLES` |
| `parametros` | jsonb | No |  | Parametros |
| `vigencia_desde` | date | No |  | Vigencia desde |
| `vigencia_hasta` | date | Sí |  | Vigencia hasta |
| `creada_en` | timestamp with time zone | No |  | Creada en |
| `area_id` | uuid | Sí | FK → `areas_area.id` | Area |
| `conjunto_id` | uuid | No | FK → `conjuntos_conjunto.id` | Conjunto |
| `creada_por_id` | uuid | No | FK → `personas_persona.id` | Creada por |
| `reemplaza_id` | uuid | Sí | FK → `reglas_regla.id` | Reemplaza |

**Restricciones de la tabla**

- Llave foránea compuesta `reglas_regla_area_id_conjunto_fk`: (area_id, conjunto_id) → areas_area(id, conjunto_id) ON DELETE RESTRICT
- Llave foránea compuesta `reglas_regla_reemplaza_id_conjunto_fk`: (reemplaza_id, conjunto_id) → reglas_regla(id, conjunto_id) ON DELETE RESTRICT
- Única `reglas_regla_id_conjunto`: UNIQUE (id, conjunto_id)
- Índice `regla_alfa_unica_abierta`: único (conjunto_id, tipo) cuando ((area_id IS NULL) AND (vigencia_hasta IS NULL))
- Índice `regla_beta_unica_abierta`: único (conjunto_id, area_id, tipo) cuando ((area_id IS NOT NULL) AND (vigencia_hasta IS NULL))
- CHECK `regla_nivel_coherente`: `CHECK (((vigencia_hasta IS NOT NULL) OR ((area_id IS NULL) AND ((tipo) = ANY ((ARRAY['ANTICIPACION_MINIMA', 'ANTICIPACION_MAXIMA', 'REQUIERE_PAZ_Y_SALVO', 'DIA_LIMITE_DE_PAGO', 'ACOMPANANTES', 'PARQUEADEROS_POR_VIVIENDA'])))) OR ((area_id IS NOT NULL) AND ((tipo) = ANY ((ARRAY['DIAS_QUE_NO_ABRE', 'CUPO_POR_UNIDAD', 'UNA_RESERVA_POR_DIA', 'SIN_FRANJAS_SEGUIDAS']))))))`
- CHECK `regla_tipo_valido`: `CHECK (((tipo) = ANY ((ARRAY['ANTICIPACION_MINIMA', 'ANTICIPACION_MAXIMA', 'REQUIERE_PAZ_Y_SALVO', 'DIA_LIMITE_DE_PAGO', 'DIAS_QUE_NO_ABRE', 'CUPO_POR_UNIDAD', 'ACOMPANANTES', 'UNA_RESERVA_POR_DIA', 'SIN_FRANJAS_SEGUIDAS', 'PARQUEADEROS_POR_VIVIENDA', 'AFORO', 'FRANJA_HORARIA', 'DIAS_NO_RESERVABLES']))))`
- CHECK `regla_vigencia_coherente`: `CHECK (((vigencia_hasta IS NULL) OR (vigencia_hasta >= vigencia_desde)))`

## Reservas

Solicitudes de reserva, avisos de franja libre y comprobantes de pago de reservas.

### `reservas_campana`

Suscripción a una franja concreta: si vuelve a quedar libre, avisa a la persona.

Modelo de Django: `reservas.Campana`.

| Columna | Tipo | Nulo | Llave | Descripción y valores permitidos |
|---|---|---|---|---|
| `id` | uuid | No | PK | Id |
| `fecha` | date | No |  | Fecha |
| `hora_inicio` | time | No |  | Hora inicio |
| `hora_fin` | time | No |  | Hora fin |
| `activa` | boolean | No |  | Activa |
| `creada_en` | timestamp with time zone | No |  | Creada en |
| `notificada_en` | timestamp with time zone | Sí |  | Notificada en |
| `area_id` | uuid | No | FK → `areas_area.id` | Area |
| `conjunto_id` | uuid | No | FK → `conjuntos_conjunto.id` | Conjunto |
| `persona_id` | uuid | No | FK → `personas_persona.id` | Persona |

**Restricciones de la tabla**

- Llave foránea compuesta `reservas_campana_area_id_conjunto_fk`: (area_id, conjunto_id) → areas_area(id, conjunto_id) ON DELETE RESTRICT
- Única `reservas_campana_id_conjunto`: UNIQUE (id, conjunto_id)
- Índice `campana_activa_unica_por_franja`: único (conjunto_id, persona_id, area_id, fecha, hora_inicio, hora_fin) cuando activa

### `reservas_comprobantedepago`

Un comprobante del pago de una reserva, guardado dentro de la base (HU-16, plan D5 a).

Modelo de Django: `reservas.ComprobanteDePago`.

| Columna | Tipo | Nulo | Llave | Descripción y valores permitidos |
|---|---|---|---|---|
| `id` | uuid | No | PK | Id |
| `contenido` | bytea (archivo binario) | No |  | Contenido |
| `tipo` | varchar(20) | No |  | Tipo |
| `nombre` | varchar(120) | No |  | Nombre |
| `peso` | integer | No |  | Peso |
| `huella` | varchar(64) | No |  | Huella |
| `subido_en` | timestamp with time zone | No |  | Subido en |
| `conjunto_id` | uuid | No | FK → `conjuntos_conjunto.id` | Conjunto |
| `solicitud_id` | uuid | No | FK → `reservas_solicitud.id` | Solicitud |
| `subido_por_id` | uuid | No | FK → `personas_persona.id` | Subido por |

**Restricciones de la tabla**

- Llave foránea compuesta `reservas_comprobantedepago_solicitud_id_conjunto_fk`: (solicitud_id, conjunto_id) → reservas_solicitud(id, conjunto_id) ON DELETE RESTRICT
- Única `reservas_comprobantedepago_id_conjunto`: UNIQUE (id, conjunto_id)
- CHECK `reservas_comprobantedepago_peso_check`: `CHECK ((peso >= 0))`

### `reservas_solicitud`

Una solicitud de reserva sobre una franja `(área, fecha, hora_inicio, hora_fin)` (maestro §5.1, HU-11).

Modelo de Django: `reservas.Solicitud`.

| Columna | Tipo | Nulo | Llave | Descripción y valores permitidos |
|---|---|---|---|---|
| `id` | uuid | No | PK | Id |
| `fecha` | date | No |  | Fecha |
| `hora_inicio` | time | No |  | Hora inicio |
| `hora_fin` | time | No |  | Hora fin |
| `estado` | varchar(20) | No |  | Estado. Valores: `EN_SOLICITUD`, `APARTADA`, `RESERVADA`, `RECHAZADA`, `CANCELADA`, `EXPIRADA`, `LIBERADA` |
| `bloqueo_vence_en` | timestamp with time zone | No |  | Bloqueo vence en |
| `motivo_liberacion` | varchar(12) | No |  | Motivo liberacion. Valores: `voluntaria`, `reglas` |
| `motivo` | varchar(200) | No |  | Motivo |
| `asistentes` | integer | Sí |  | Asistentes |
| `observaciones` | text | No |  | Observaciones |
| `evaluacion` | jsonb | Sí |  | Evaluacion |
| `evaluada_en` | timestamp with time zone | Sí |  | Evaluada en |
| `creada_en` | timestamp with time zone | No |  | Creada en |
| `enviada_en` | timestamp with time zone | Sí |  | Enviada en |
| `area_id` | uuid | No | FK → `areas_area.id` | Area |
| `conjunto_id` | uuid | No | FK → `conjuntos_conjunto.id` | Conjunto |
| `persona_id` | uuid | No | FK → `personas_persona.id` | Persona |
| `unidad_id` | uuid | Sí | FK → `unidades_unidad.id` | Unidad |
| `decidida_en` | timestamp with time zone | Sí |  | Decidida en |
| `decidida_por_id` | uuid | Sí | FK → `personas_persona.id` | Decidida por |
| `motivo_decision` | text | No |  | Motivo decision |
| `pago_declarado_en` | timestamp with time zone | Sí |  | Pago declarado en |
| `pago_declarado_por_id` | uuid | Sí | FK → `personas_persona.id` | Pago declarado por |
| `categoria_rechazo` | varchar(30) | No |  | Categoria rechazo. Valores: `NO_DISPONIBLE`, `CONDICIONES_NO_CUMPLIDAS`, `DOCUMENTACION_INCOMPLETA`, `INCUMPLE_REGLAMENTO`, `OTRO`, `DATOS_INCOMPLETOS`, `SOLICITUD_DUPLICADA`, `VIVIENDA_NO_CORRESPONDE` |

**Restricciones de la tabla**

- Llave foránea compuesta `reservas_solicitud_area_id_conjunto_fk`: (area_id, conjunto_id) → areas_area(id, conjunto_id) ON DELETE RESTRICT
- Llave foránea compuesta `reservas_solicitud_unidad_id_conjunto_fk`: (unidad_id, conjunto_id) → unidades_unidad(id, conjunto_id) ON DELETE RESTRICT
- Única `reservas_solicitud_id_conjunto`: UNIQUE (id, conjunto_id)
- Índice `solicitud_franja_bloqueante_unica`: único (conjunto_id, area_id, fecha, hora_inicio) cuando ((estado) = ANY ((ARRAY['EN_SOLICITUD', 'APARTADA', 'RESERVADA'])))
- Índice `solicitud_un_bloqueo_por_persona`: único (conjunto_id, persona_id) cuando ((estado) = 'EN_SOLICITUD')
- CHECK `reservas_solicitud_asistentes_check`: `CHECK ((asistentes >= 0))`
- CHECK `solicitud_categoria_de_rechazo_valida`: `CHECK ((((categoria_rechazo) = '') OR ((categoria_rechazo) = ANY ((ARRAY['NO_DISPONIBLE', 'CONDICIONES_NO_CUMPLIDAS', 'DOCUMENTACION_INCOMPLETA', 'INCUMPLE_REGLAMENTO', 'OTRO', 'DATOS_INCOMPLETOS', 'SOLICITUD_DUPLICADA', 'VIVIENDA_NO_CORRESPONDE'])))))`
- CHECK `solicitud_estado_valido`: `CHECK (((estado) = ANY ((ARRAY['EN_SOLICITUD', 'APARTADA', 'RESERVADA', 'RECHAZADA', 'CANCELADA', 'EXPIRADA', 'LIBERADA']))))`
- CHECK `solicitud_horario_coherente`: `CHECK ((hora_fin > hora_inicio))`
- CHECK `solicitud_pago_declarado_completo`: `CHECK ((((pago_declarado_en IS NULL) AND (pago_declarado_por_id IS NULL)) OR ((pago_declarado_en IS NOT NULL) AND (pago_declarado_por_id IS NOT NULL))))`
- CHECK `solicitud_rechazada_con_categoria`: `CHECK (((NOT ((estado) = 'RECHAZADA')) OR (NOT ((categoria_rechazo) = ''))))`
- CHECK `solicitud_unidad_desde_apartada`: `CHECK ((((estado) = ANY ((ARRAY['EN_SOLICITUD', 'EXPIRADA', 'LIBERADA']))) OR (unidad_id IS NOT NULL)))`

## Ingresos a zonas

Registro de entrada y salida de personas en zonas con aforo.

### `ingresos_ingreso`

Una persona adentro de una zona con ingreso (plan P7). No guarda el documento: solo la referencia a la persona.

Modelo de Django: `ingresos.Ingreso`.

| Columna | Tipo | Nulo | Llave | Descripción y valores permitidos |
|---|---|---|---|---|
| `id` | uuid | No | PK | Id |
| `acompanantes` | smallint | No |  | Acompanantes |
| `estado` | varchar(10) | No |  | Estado. Valores: `ADENTRO`, `SALIO`, `VENCIDO` |
| `entrada_en` | timestamp with time zone | No |  | Entrada en |
| `salida_prevista_en` | timestamp with time zone | No |  | Salida prevista en |
| `salida_en` | timestamp with time zone | Sí |  | Salida en |
| `evaluacion` | jsonb | Sí |  | Evaluacion |
| `area_id` | uuid | No | FK → `areas_area.id` | Area |
| `conjunto_id` | uuid | No | FK → `conjuntos_conjunto.id` | Conjunto |
| `persona_id` | uuid | No | FK → `personas_persona.id` | Persona |
| `registrado_por_id` | uuid | No | FK → `personas_persona.id` | Registrado por |
| `salida_registrada_por_id` | uuid | Sí | FK → `personas_persona.id` | Salida registrada por |
| `unidad_id` | uuid | No | FK → `unidades_unidad.id` | Unidad |

**Restricciones de la tabla**

- Llave foránea compuesta `ingresos_ingreso_area_id_conjunto_fk`: (area_id, conjunto_id) → areas_area(id, conjunto_id) ON DELETE RESTRICT
- Llave foránea compuesta `ingresos_ingreso_unidad_id_conjunto_fk`: (unidad_id, conjunto_id) → unidades_unidad(id, conjunto_id) ON DELETE RESTRICT
- Única `ingresos_ingreso_id_conjunto`: UNIQUE (id, conjunto_id)
- Índice `ingreso_uno_abierto_por_persona`: único (conjunto_id, persona_id) cuando ((estado) = 'ADENTRO')
- CHECK `ingreso_estado_valido`: `CHECK (((estado) = ANY ((ARRAY['ADENTRO', 'SALIO', 'VENCIDO']))))`
- CHECK `ingreso_salida_prevista_coherente`: `CHECK ((salida_prevista_en > entrada_en))`
- CHECK `ingreso_salida_segun_estado`: `CHECK (((((estado) = 'ADENTRO') AND (salida_en IS NULL)) OR ((NOT ((estado) = 'ADENTRO')) AND (salida_en IS NOT NULL))))`
- CHECK `ingresos_ingreso_acompanantes_check`: `CHECK ((acompanantes >= 0))`

## Parqueaderos

Puestos de parqueo y su asignación a viviendas.

### `parqueaderos_asignacionparqueadero`

Un parqueadero de residentes destinado a una vivienda, desde cuándo y hasta cuándo (HU-34).

Modelo de Django: `parqueaderos.AsignacionParqueadero`.

| Columna | Tipo | Nulo | Llave | Descripción y valores permitidos |
|---|---|---|---|---|
| `id` | uuid | No | PK | Id |
| `vigencia_desde` | date | No |  | Vigencia desde |
| `vigencia_hasta` | date | Sí |  | Vigencia hasta |
| `registrado_en` | timestamp with time zone | No |  | Registrado en |
| `cerrado_por_id` | uuid | Sí | FK → `personas_persona.id` | Cerrado por |
| `conjunto_id` | uuid | No | FK → `conjuntos_conjunto.id` | Conjunto |
| `parqueadero_id` | uuid | No | FK → `parqueaderos_parqueadero.id` | Parqueadero |
| `registrado_por_id` | uuid | No | FK → `personas_persona.id` | Registrado por |
| `unidad_id` | uuid | No | FK → `unidades_unidad.id` | Unidad |

**Restricciones de la tabla**

- Llave foránea compuesta `parqueaderos_asignacionparqueadero_parqueadero_id_conjunto_fk`: (parqueadero_id, conjunto_id) → parqueaderos_parqueadero(id, conjunto_id) ON DELETE RESTRICT
- Llave foránea compuesta `parqueaderos_asignacionparqueadero_unidad_id_conjunto_fk`: (unidad_id, conjunto_id) → unidades_unidad(id, conjunto_id) ON DELETE RESTRICT
- Única `parqueaderos_asignacionparqueadero_id_conjunto`: UNIQUE (id, conjunto_id)
- Índice `asignacion_parqueadero_vigente_unica`: único (conjunto_id, parqueadero_id) cuando (vigencia_hasta IS NULL)
- CHECK `asignacion_parqueadero_vigencia_coherente`: `CHECK (((vigencia_hasta IS NULL) OR (vigencia_hasta >= vigencia_desde)))`

### `parqueaderos_parqueadero`

Un puesto de parqueo del conjunto, con su código (HU-28; HU-34 asigna los de residentes).

Modelo de Django: `parqueaderos.Parqueadero`.

| Columna | Tipo | Nulo | Llave | Descripción y valores permitidos |
|---|---|---|---|---|
| `id` | uuid | No | PK | Id |
| `codigo` | varchar(20) | No |  | Codigo |
| `tipo` | varchar(12) | No |  | Tipo. Valores: `residentes`, `visitantes` |
| `accesible` | boolean | No |  | Accesible |
| `notas` | varchar(200) | No |  | Notas |
| `activo` | boolean | No |  | Activo |
| `creado_en` | timestamp with time zone | No |  | Creado en |
| `conjunto_id` | uuid | No | FK → `conjuntos_conjunto.id` | Conjunto |
| `creado_por_id` | uuid | No | FK → `personas_persona.id` | Creado por |
| `vehiculo` | varchar(10) | No |  | Vehiculo. Valores: `carro`, `moto`, `bicicleta` |

**Restricciones de la tabla**

- Única `parqueadero_codigo_unico`: UNIQUE (conjunto_id, codigo)
- Única `parqueaderos_parqueadero_id_conjunto`: UNIQUE (id, conjunto_id)
- CHECK `parqueadero_tipo_valido`: `CHECK (((tipo) = ANY ((ARRAY['residentes', 'visitantes']))))`
- CHECK `parqueadero_vehiculo_valido`: `CHECK (((vehiculo) = ANY ((ARRAY['carro', 'moto', 'bicicleta']))))`

## Visitantes

Visitas registradas en portería.

### `visitantes_visitante`

Una visita en portería. La salida se agrega como dato: la fila no se borra ni se reemplaza (HU-28).

Modelo de Django: `visitantes.Visitante`.

| Columna | Tipo | Nulo | Llave | Descripción y valores permitidos |
|---|---|---|---|---|
| `id` | uuid | No | PK | Id |
| `nombre` | varchar(120) | No |  | Nombre |
| `cedula` | varchar(20) | No |  | Cedula |
| `placa_vehiculo` | varchar(10) | No |  | Placa vehiculo |
| `tipo_vehiculo` | varchar(40) | No |  | Tipo vehiculo |
| `hora_entrada` | timestamp with time zone | No |  | Hora entrada |
| `conjunto_id` | uuid | No | FK → `conjuntos_conjunto.id` | Conjunto |
| `unidad_id` | uuid | No | FK → `unidades_unidad.id` | Unidad |
| `hora_salida` | timestamp with time zone | Sí |  | Hora salida |
| `salida_registrada_por_id` | uuid | Sí | FK → `personas_persona.id` | Salida registrada por |
| `parqueadero_id` | uuid | Sí | FK → `parqueaderos_parqueadero.id` | Parqueadero |

**Restricciones de la tabla**

- Llave foránea compuesta `visitantes_visitante_parqueadero_id_conjunto_fk`: (parqueadero_id, conjunto_id) → parqueaderos_parqueadero(id, conjunto_id) ON DELETE RESTRICT
- Única `visitantes_visitante_id_conjunto`: UNIQUE (id, conjunto_id)
- Índice `visitante_parqueadero_ocupado_unico`: único (conjunto_id, parqueadero_id) cuando ((hora_salida IS NULL) AND (parqueadero_id IS NOT NULL))
- CHECK `visitante_salida_despues_de_entrada`: `CHECK (((hora_salida IS NULL) OR (hora_salida >= hora_entrada)))`

## Pagos de administración

Pago mensual de la administración por vivienda y sus comprobantes.

### `pagos_comprobante`

Un comprobante de un pago de administración, guardado dentro de la base (HU-35, plan P6).

Modelo de Django: `pagos.Comprobante`.

| Columna | Tipo | Nulo | Llave | Descripción y valores permitidos |
|---|---|---|---|---|
| `id` | uuid | No | PK | Id |
| `contenido` | bytea (archivo binario) | No |  | Contenido |
| `tipo` | varchar(20) | No |  | Tipo |
| `nombre` | varchar(120) | No |  | Nombre |
| `peso` | integer | No |  | Peso |
| `huella` | varchar(64) | No |  | Huella |
| `subido_en` | timestamp with time zone | No |  | Subido en |
| `conjunto_id` | uuid | No | FK → `conjuntos_conjunto.id` | Conjunto |
| `pago_id` | uuid | No | FK → `pagos_pagodeadministracion.id` | Pago |
| `subido_por_id` | uuid | No | FK → `personas_persona.id` | Subido por |

**Restricciones de la tabla**

- Llave foránea compuesta `pagos_comprobante_pago_id_conjunto_fk`: (pago_id, conjunto_id) → pagos_pagodeadministracion(id, conjunto_id) ON DELETE RESTRICT
- Única `pagos_comprobante_id_conjunto`: UNIQUE (id, conjunto_id)
- CHECK `pagos_comprobante_peso_check`: `CHECK ((peso >= 0))`

### `pagos_pagodeadministracion`

Los hechos del pago de la administración de una vivienda en un mes (HU-35).

Modelo de Django: `pagos.PagoDeAdministracion`.

| Columna | Tipo | Nulo | Llave | Descripción y valores permitidos |
|---|---|---|---|---|
| `id` | uuid | No | PK | Id |
| `periodo` | date | No |  | Periodo |
| `reportado_en` | timestamp with time zone | Sí |  | Reportado en |
| `confirmado_en` | timestamp with time zone | Sí |  | Confirmado en |
| `confirmado_por_id` | uuid | Sí | FK → `personas_persona.id` | Confirmado por |
| `conjunto_id` | uuid | No | FK → `conjuntos_conjunto.id` | Conjunto |
| `reportado_por_id` | uuid | Sí | FK → `personas_persona.id` | Reportado por |
| `unidad_id` | uuid | No | FK → `unidades_unidad.id` | Unidad |

**Restricciones de la tabla**

- Llave foránea compuesta `pagos_pagodeadministracion_unidad_id_conjunto_fk`: (unidad_id, conjunto_id) → unidades_unidad(id, conjunto_id) ON DELETE RESTRICT
- Única `pago_unico_por_vivienda_y_mes`: UNIQUE (conjunto_id, unidad_id, periodo)
- Única `pagos_pagodeadministracion_id_conjunto`: UNIQUE (id, conjunto_id)
- CHECK `pago_confirmado_completo`: `CHECK ((((confirmado_en IS NULL) AND (confirmado_por_id IS NULL)) OR ((confirmado_en IS NOT NULL) AND (confirmado_por_id IS NOT NULL))))`
- CHECK `pago_periodo_es_dia_uno`: `CHECK ((EXTRACT(day FROM periodo) = (1)))`
- CHECK `pago_reportado_completo`: `CHECK ((((reportado_en IS NULL) AND (reportado_por_id IS NULL)) OR ((reportado_en IS NOT NULL) AND (reportado_por_id IS NOT NULL))))`

## Documentos

Reglamento y manual de convivencia del conjunto.

### `documentos_documento`

Un documento del conjunto en PDF: su reglamento o su manual de convivencia (HU-33).

Modelo de Django: `documentos.Documento`.

| Columna | Tipo | Nulo | Llave | Descripción y valores permitidos |
|---|---|---|---|---|
| `id` | uuid | No | PK | Id |
| `contenido` | bytea (archivo binario) | No |  | Contenido |
| `nombre` | varchar(120) | No |  | Nombre |
| `peso` | integer | No |  | Peso |
| `huella` | varchar(64) | No |  | Huella |
| `subido_en` | timestamp with time zone | No |  | Subido en |
| `conjunto_id` | uuid | No | FK → `conjuntos_conjunto.id` | Conjunto |
| `subido_por_id` | uuid | No | FK → `personas_persona.id` | Subido por |
| `tipo` | varchar(20) | No |  | Tipo. Valores: `reglamento`, `manual` |

**Restricciones de la tabla**

- Única `documentos_documento_id_conjunto`: UNIQUE (id, conjunto_id)
- CHECK `documento_tipo_valido`: `CHECK (((tipo) = ANY ((ARRAY['reglamento', 'manual']))))`
- CHECK `documentos_reglamento_peso_check`: `CHECK ((peso >= 0))`

## Anuncios

Anuncios del conjunto y sus fotos.

### `anuncios_anuncio`

Modelo de Django: `anuncios.Anuncio`.

| Columna | Tipo | Nulo | Llave | Descripción y valores permitidos |
|---|---|---|---|---|
| `id` | uuid | No | PK | Id |
| `titulo` | varchar(120) | No |  | Titulo |
| `cuerpo` | text | No |  | Cuerpo |
| `alcance` | varchar(10) | No |  | Alcance. Valores: `conjunto`, `vivienda` |
| `publicado_en` | timestamp with time zone | No |  | Publicado en |
| `editado_en` | timestamp with time zone | Sí |  | Editado en |
| `autor_id` | uuid | No | FK → `personas_persona.id` | Autor |
| `conjunto_id` | uuid | No | FK → `conjuntos_conjunto.id` | Conjunto |
| `unidad_id` | uuid | Sí | FK → `unidades_unidad.id` | Unidad |

**Restricciones de la tabla**

- Llave foránea compuesta `anuncios_anuncio_unidad_id_conjunto_fk`: (unidad_id, conjunto_id) → unidades_unidad(id, conjunto_id) ON DELETE RESTRICT
- Única `anuncios_anuncio_id_conjunto`: UNIQUE (id, conjunto_id)
- CHECK `anuncio_unidad_segun_alcance`: `CHECK (((((alcance) = 'conjunto') AND (unidad_id IS NULL)) OR (((alcance) = 'vivienda') AND (unidad_id IS NOT NULL))))`

### `anuncios_fotodeanuncio`

Una foto del anuncio (HU-25). Va en su propia tabla para que leer un Anuncio no traiga la imagen.

Modelo de Django: `anuncios.FotoDeAnuncio`.

| Columna | Tipo | Nulo | Llave | Descripción y valores permitidos |
|---|---|---|---|---|
| `id` | uuid | No | PK | Id |
| `contenido` | bytea (archivo binario) | No |  | Contenido |
| `tipo` | varchar(20) | No |  | Tipo |
| `orden` | smallint | No |  | Orden |
| `anuncio_id` | uuid | No | FK → `anuncios_anuncio.id` | Anuncio |
| `conjunto_id` | uuid | No | FK → `conjuntos_conjunto.id` | Conjunto |

**Restricciones de la tabla**

- Llave foránea compuesta `anuncios_fotodeanuncio_anuncio_id_conjunto_fk`: (anuncio_id, conjunto_id) → anuncios_anuncio(id, conjunto_id) ON DELETE RESTRICT
- Única `anuncios_fotodeanuncio_id_conjunto`: UNIQUE (id, conjunto_id)
- Única `foto_orden_unico_por_anuncio`: UNIQUE (anuncio_id, orden)
- CHECK `anuncios_fotodeanuncio_orden_check`: `CHECK ((orden >= 0))`
- CHECK `foto_orden_dentro_del_tope`: `CHECK ((orden < 4))`

## Notificaciones

Bandeja de avisos de cada persona.

### `notificaciones_notificacion`

Un aviso en la bandeja de una persona: la salida «aplicación» del canal.

Modelo de Django: `notificaciones.Notificacion`.

| Columna | Tipo | Nulo | Llave | Descripción y valores permitidos |
|---|---|---|---|---|
| `id` | uuid | No | PK | Id |
| `titulo` | varchar(120) | No |  | Titulo |
| `cuerpo` | text | No |  | Cuerpo |
| `origen` | varchar(30) | No |  | Origen |
| `referencia` | uuid | No |  | Referencia |
| `creada_en` | timestamp with time zone | No |  | Creada en |
| `conjunto_id` | uuid | No | FK → `conjuntos_conjunto.id` | Conjunto |
| `persona_id` | uuid | No | FK → `personas_persona.id` | Persona |

**Restricciones de la tabla**

- Única `notificacion_una_por_hecho`: UNIQUE (persona_id, origen, referencia)
- Única `notificaciones_notificacion_id_conjunto`: UNIQUE (id, conjunto_id)

## Casos (PQRS)

Casos reportados por los residentes y sus fotos.

### `casos_caso`

Modelo de Django: `casos.Caso`.

| Columna | Tipo | Nulo | Llave | Descripción y valores permitidos |
|---|---|---|---|---|
| `id` | uuid | No | PK | Id |
| `titulo` | varchar(120) | No |  | Titulo |
| `cuerpo` | text | No |  | Cuerpo |
| `estado` | varchar(20) | No |  | Estado. Valores: `ABIERTO`, `EN_REVISION`, `REDIRIGIDO`, `CITADO`, `RESUELTO`, `RECHAZADO` |
| `prioridad` | varchar(10) | No |  | Prioridad. Valores: `BAJA`, `NORMAL`, `ALTA`, `URGENTE` |
| `creado_en` | timestamp with time zone | No |  | Creado en |
| `autor_id` | uuid | No | FK → `personas_persona.id` | Autor |
| `conjunto_id` | uuid | No | FK → `conjuntos_conjunto.id` | Conjunto |
| `motivo_rechazo` | text | No |  | Motivo rechazo |
| `causal_rechazo` | varchar(30) | No |  | Causal rechazo. Valores: `NO_ES_COMPETENCIA`, `DUPLICADO`, `INFORMACION_INSUFICIENTE` |
| `cerrado_en` | timestamp with time zone | Sí |  | Cerrado en |
| `cerrado_por_id` | uuid | Sí | FK → `personas_persona.id` | Cerrado por |
| `justificacion_prioridad` | text | No |  | Justificacion prioridad |
| `nota_redireccion` | text | No |  | Nota redireccion |
| `respuesta` | text | No |  | Respuesta |

**Restricciones de la tabla**

- Única `casos_caso_id_conjunto`: UNIQUE (id, conjunto_id)
- CHECK `caso_estado_valido`: `CHECK (((estado) = ANY ((ARRAY['ABIERTO', 'EN_REVISION', 'REDIRIGIDO', 'CITADO', 'RESUELTO', 'RECHAZADO']))))`
- CHECK `caso_prioridad_valida`: `CHECK (((prioridad) = ANY ((ARRAY['BAJA', 'NORMAL', 'ALTA', 'URGENTE']))))`
- CHECK `caso_rechazado_con_motivo`: `CHECK (((NOT ((estado) = 'RECHAZADO')) OR (NOT (motivo_rechazo = ''))))`
- CHECK `caso_resuelto_con_respuesta`: `CHECK (((NOT ((estado) = 'RESUELTO')) OR (NOT (respuesta = ''))))`
- CHECK `caso_urgente_con_justificacion`: `CHECK (((NOT ((prioridad) = 'URGENTE')) OR (NOT (justificacion_prioridad = ''))))`

### `casos_fotodecaso`

Modelo de Django: `casos.FotoDeCaso`.

| Columna | Tipo | Nulo | Llave | Descripción y valores permitidos |
|---|---|---|---|---|
| `id` | uuid | No | PK | Id |
| `contenido` | bytea (archivo binario) | No |  | Contenido |
| `tipo` | varchar(20) | No |  | Tipo |
| `caso_id` | uuid | No | FK → `casos_caso.id` · UQ | Caso |
| `conjunto_id` | uuid | No | FK → `conjuntos_conjunto.id` | Conjunto |

**Restricciones de la tabla**

- Llave foránea compuesta `casos_fotodecaso_caso_id_conjunto_fk`: (caso_id, conjunto_id) → casos_caso(id, conjunto_id) ON DELETE RESTRICT
- Única `casos_fotodecaso_id_conjunto`: UNIQUE (id, conjunto_id)

## Infracciones

Registro y comunicación de infracciones a una vivienda.

### `infracciones_registrodeinfraccion`

El registro de que se comunicó una infracción a la vivienda (HU-30; maestro §5.8).

Modelo de Django: `infracciones.RegistroDeInfraccion`.

| Columna | Tipo | Nulo | Llave | Descripción y valores permitidos |
|---|---|---|---|---|
| `id` | uuid | No | PK | Id |
| `descripcion_hecho` | text | No |  | Descripcion hecho |
| `fecha_hecho` | date | No |  | Fecha hecho |
| `registrado_en` | timestamp with time zone | No |  | Registrado en |
| `fecha_notificacion` | timestamp with time zone | No |  | Fecha notificacion |
| `cierre_fecha` | timestamp with time zone | Sí |  | Cierre fecha |
| `cierre_comentario` | text | Sí |  | Cierre comentario |
| `anulado` | boolean | No |  | Anulado |
| `anulacion_motivo` | text | No |  | Anulacion motivo |
| `anulado_en` | timestamp with time zone | Sí |  | Anulado en |
| `anulado_por_id` | uuid | Sí | FK → `personas_persona.id` | Anulado por |
| `caso_id` | uuid | Sí | FK → `casos_caso.id` | Caso |
| `cerrado_por_id` | uuid | Sí | FK → `personas_persona.id` | Cerrado por |
| `conjunto_id` | uuid | No | FK → `conjuntos_conjunto.id` | Conjunto |
| `registrado_por_id` | uuid | No | FK → `personas_persona.id` | Registrado por |
| `unidad_id` | uuid | No | FK → `unidades_unidad.id` | Unidad |

**Restricciones de la tabla**

- Llave foránea compuesta `infracciones_registrodeinfraccion_caso_id_conjunto_fk`: (caso_id, conjunto_id) → casos_caso(id, conjunto_id) ON DELETE RESTRICT
- Llave foránea compuesta `infracciones_registrodeinfraccion_unidad_id_conjunto_fk`: (unidad_id, conjunto_id) → unidades_unidad(id, conjunto_id) ON DELETE RESTRICT
- Única `infracciones_registrodeinfraccion_id_conjunto`: UNIQUE (id, conjunto_id)
- CHECK `infraccion_anulacion_completa`: `CHECK (((NOT anulado) OR ((NOT (anulacion_motivo = '')) AND (anulado_por_id IS NOT NULL) AND (anulado_en IS NOT NULL))))`
- CHECK `infraccion_cierre_completo`: `CHECK ((((cierre_fecha IS NULL) AND (cierre_comentario IS NULL)) OR ((cierre_fecha IS NOT NULL) AND (cierre_comentario IS NOT NULL) AND (NOT ((cierre_comentario = '') AND (cierre_comentario IS NOT NULL))))))`
- CHECK `infraccion_hecho_descrito`: `CHECK ((NOT (descripcion_hecho = '')))`

## Citas

Horario de atención de la administración y citas agendadas.

### `citas_cita`

Franja de dos horas agendada por un residente.

Modelo de Django: `citas.Cita`.

| Columna | Tipo | Nulo | Llave | Descripción y valores permitidos |
|---|---|---|---|---|
| `id` | uuid | No | PK | Id |
| `fecha` | date | No |  | Fecha |
| `hora_inicio` | time | No |  | Hora inicio |
| `hora_fin` | time | No |  | Hora fin |
| `estado` | varchar(12) | No |  | Estado. Valores: `AGENDADA`, `ATENDIDA` |
| `vence_en` | timestamp with time zone | No |  | Vence en |
| `creada_en` | timestamp with time zone | No |  | Creada en |
| `conjunto_id` | uuid | No | FK → `conjuntos_conjunto.id` | Conjunto |
| `persona_id` | uuid | No | FK → `personas_persona.id` | Persona |

**Restricciones de la tabla**

- Única `citas_cita_id_conjunto`: UNIQUE (id, conjunto_id)
- Índice `cita_franja_activa`: único (conjunto_id, fecha, hora_inicio) cuando ((estado) = 'AGENDADA')
- Índice `cita_unica_por_persona`: único (conjunto_id, persona_id) cuando ((estado) = 'AGENDADA')

### `citas_horariodeatencion`

Configuración semanal de atención del administrador (HU-31).

Modelo de Django: `citas.HorarioDeAtencion`.

| Columna | Tipo | Nulo | Llave | Descripción y valores permitidos |
|---|---|---|---|---|
| `id` | uuid | No | PK | Id |
| `dias` | jsonb | No |  | Dias |
| `actualizado_en` | timestamp with time zone | No |  | Actualizado en |
| `actualizado_por_id` | uuid | No | FK → `personas_persona.id` | Actualizado por |
| `conjunto_id` | uuid | No | FK → `conjuntos_conjunto.id` · UQ | Conjunto |

**Restricciones de la tabla**

- Única `citas_horariodeatencion_id_conjunto`: UNIQUE (id, conjunto_id)

## Auditoría

Registro inmutable de quién hizo qué y cuándo.

### `auditoria_registro`

Quién hizo qué, cuándo, y cómo estaba antes y después (maestro §5.3, §5.11).

Modelo de Django: `auditoria.Registro`.

| Columna | Tipo | Nulo | Llave | Descripción y valores permitidos |
|---|---|---|---|---|
| `id` | uuid | No | PK | Id |
| `accion` | varchar(60) | No |  | Accion |
| `entidad` | varchar(60) | No |  | Entidad |
| `entidad_id` | uuid | Sí |  | Entidad id |
| `antes` | jsonb | Sí |  | Antes |
| `despues` | jsonb | Sí |  | Despues |
| `detalle` | jsonb | Sí |  | Detalle |
| `via_superusuario` | boolean | No |  | Via superusuario |
| `creado_en` | timestamp with time zone | No |  | Creado en |
| `actor_id` | uuid | No | FK → `personas_persona.id` | Actor |
| `conjunto_id` | uuid | No | FK → `conjuntos_conjunto.id` | Conjunto |

**Restricciones de la tabla**

- Única `auditoria_registro_id_conjunto`: UNIQUE (id, conjunto_id)

## Anexo: tablas del framework

Las crean Django (usuarios, permisos internos, sesiones, migraciones) y django-otp (segundo factor). AdMind no las modifica.

### `django_admin_log`

Modelo de Django: `admin.LogEntry`.

| Columna | Tipo | Nulo | Llave | Descripción y valores permitidos |
|---|---|---|---|---|
| `id` | integer | No | PK | ID |
| `action_time` | timestamp with time zone | No |  | Hora de la acción |
| `object_id` | text | Sí |  | Id del objeto |
| `object_repr` | varchar(200) | No |  | Repr del objeto |
| `action_flag` | smallint | No |  | Marca de acción. Valores: `1`, `2`, `3` |
| `change_message` | text | No |  | Mensaje de cambio |
| `content_type_id` | integer | Sí | FK → `django_content_type.id` | Tipo de contenido |
| `user_id` | uuid | No | FK → `cuentas_usuario.id` | Usuario |

### `auth_group`

Groups are a generic way of categorizing users to apply permissions, or some other label, to those users. A user can belong to any number of groups.

Modelo de Django: `auth.Group`.

| Columna | Tipo | Nulo | Llave | Descripción y valores permitidos |
|---|---|---|---|---|
| `id` | integer | No | PK | ID |
| `name` | varchar(150) | No | UQ | Nombre |

### `auth_group_permissions`

Tabla intermedia creada por Django: relación group-permission.

Modelo de Django: `auth.Group_permissions`.

| Columna | Tipo | Nulo | Llave | Descripción y valores permitidos |
|---|---|---|---|---|
| `id` | bigint | No | PK | ID |
| `group_id` | integer | No | FK → `auth_group.id` | Group |
| `permission_id` | integer | No | FK → `auth_permission.id` | Permission |

### `auth_permission`

The permissions system provides a way to assign permissions to specific users and groups of users.

Modelo de Django: `auth.Permission`.

| Columna | Tipo | Nulo | Llave | Descripción y valores permitidos |
|---|---|---|---|---|
| `id` | integer | No | PK | ID |
| `name` | varchar(255) | No |  | Nombre |
| `content_type_id` | integer | No | FK → `django_content_type.id` | Tipo de contenido |
| `codename` | varchar(100) | No |  | Nombre en código |

### `django_content_type`

Modelo de Django: `contenttypes.ContentType`.

| Columna | Tipo | Nulo | Llave | Descripción y valores permitidos |
|---|---|---|---|---|
| `id` | integer | No | PK | ID |
| `app_label` | varchar(100) | No |  | App label |
| `model` | varchar(100) | No |  | Nombre de la clase modelo de python |

### `django_migrations`

| Columna | Tipo | Nulo | Llave | Descripción y valores permitidos |
|---|---|---|---|---|
| `id` | bigint | No | PK |  |
| `app` | varchar(255) | No |  |  |
| `name` | varchar(255) | No |  |  |
| `applied` | timestamp with time zone | No |  |  |

### `otp_static_staticdevice`

A static :class:`~django_otp.models.Device` simply consists of random tokens shared by the database and the user.

Modelo de Django: `otp_static.StaticDevice`.

| Columna | Tipo | Nulo | Llave | Descripción y valores permitidos |
|---|---|---|---|---|
| `id` | integer | No | PK | ID |
| `name` | varchar(64) | No |  | The human-readable name of this device. |
| `confirmed` | boolean | No |  | Is this device ready for use? |
| `user_id` | uuid | No | FK → `cuentas_usuario.id` | The user that this device belongs to. |
| `throttling_failure_count` | integer | No |  | Number of successive failed attempts. |
| `throttling_failure_timestamp` | timestamp with time zone | Sí |  | A timestamp of the last failed verification attempt. Null if last attempt succeeded. |
| `created_at` | timestamp with time zone | Sí |  | The date and time when this device was initially created in the system. |
| `last_used_at` | timestamp with time zone | Sí |  | The most recent date and time this device was used. |

### `otp_static_statictoken`

A single token belonging to a :class:`StaticDevice`.

Modelo de Django: `otp_static.StaticToken`.

| Columna | Tipo | Nulo | Llave | Descripción y valores permitidos |
|---|---|---|---|---|
| `id` | integer | No | PK | ID |
| `token` | varchar(16) | No |  | Token |
| `device_id` | integer | No | FK → `otp_static_staticdevice.id` | Device |

### `otp_totp_totpdevice`

A generic TOTP :class:`~django_otp.models.Device`. The model fields mostly correspond to the arguments to :func:`django_otp.oath.totp`. They all have sensible defaults, including the key, which is randomly generated.

Modelo de Django: `otp_totp.TOTPDevice`.

| Columna | Tipo | Nulo | Llave | Descripción y valores permitidos |
|---|---|---|---|---|
| `id` | integer | No | PK | ID |
| `name` | varchar(64) | No |  | The human-readable name of this device. |
| `confirmed` | boolean | No |  | Is this device ready for use? |
| `key` | varchar(80) | No |  | A hex-encoded secret key of up to 40 bytes. |
| `step` | smallint | No |  | The time step in seconds. |
| `t0` | bigint | No |  | The Unix time at which to begin counting steps. |
| `digits` | smallint | No |  | The number of digits to expect in a token.. Valores: `6`, `8` |
| `tolerance` | smallint | No |  | The number of time steps in the past or future to allow. |
| `drift` | smallint | No |  | The number of time steps the prover is known to deviate from our clock. |
| `last_t` | bigint | No |  | The t value of the latest verified token. The next token must be at a higher time step. |
| `user_id` | uuid | No | FK → `cuentas_usuario.id` | The user that this device belongs to. |
| `throttling_failure_count` | integer | No |  | Number of successive failed attempts. |
| `throttling_failure_timestamp` | timestamp with time zone | Sí |  | A timestamp of the last failed verification attempt. Null if last attempt succeeded. |
| `created_at` | timestamp with time zone | Sí |  | The date and time when this device was initially created in the system. |
| `last_used_at` | timestamp with time zone | Sí |  | The most recent date and time this device was used. |

### `django_session`

Django provides full support for anonymous sessions. The session framework lets you store and retrieve arbitrary data on a per-site-visitor basis. It stores data on the server side and abstracts the sending and receiving of cookies. Cookies contain a session ID -- not the data itself.

Modelo de Django: `sessions.Session`.

| Columna | Tipo | Nulo | Llave | Descripción y valores permitidos |
|---|---|---|---|---|
| `session_key` | varchar(40) | No | PK | Clave de sesión |
| `session_data` | text | No |  | Datos de sesión |
| `expire_date` | timestamp with time zone | No |  | Fecha de caducidad |

