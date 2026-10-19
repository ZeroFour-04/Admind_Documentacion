---
resumen: "El asistente de creación (siete pasos, seis requisitos para quedar operativo, el reglamento en PDF), la identidad del conjunto (acento o color propio y foto 1:1) y la baja del conjunto."
tipo: modulo
modulo: conjuntos
hu: [HU-03, HU-21, HU-33]
origen: "guía de estructura §5.7 (2026-09-30); la baja, del código al 2026-10-13"
actualizado: 2026-10-13
revisado: 2026-10-13
---

# Conjuntos: asistente de creación e identidad

Qué es un conjunto operativo y cómo se crea está en [alcance](../01_Contexto/alcance.md) (3.1, Multiconjunto).

## El asistente de creación (HU-03), como quedó el 2026-10-06

Cada paso se guarda apenas se completa: se puede salir y volver.

| Paso | Qué pide | Dónde |
|---|---|---|
| 1. Datos básicos | Nombre, dirección y color | `conjuntos` |
| 2. Viviendas | Cómo es el conjunto; genera las viviendas en lote, con vista previa | `conjuntos` en el front, `unidades` en la API ([unidades](unidades.md)) |
| 3. Administración | La cuenta de quien administra | `conjuntos`, con `POST /auth/usuarios/` |
| 4. Áreas | Cada área con su horario, franja y aforo. Tres áreas típicas (Salón comunal, BBQ, Cancha) llenan el formulario con valores de partida: son enlaces `?plantilla=…` y la vista los pasa como `initial` | `conjuntos` y `areas` |
| 5. Reglas | El tablero de reglas, dentro del asistente | `reglas` ([motor_reglas](motor_reglas.md)) |
| 6. Reglamento | El PDF del reglamento | `conjuntos` en el front, `documentos` en la API |
| 7. Resumen | Los requisitos y «Dejar operativo» | `conjuntos` |

**Los seis requisitos** salen de `servicios.requisitos_para_operar(conjunto)`, que es una lista: `activar()` y el Resumen del front la recorren sin saber qué hay en ella.

| Clave | Se cumple con |
|---|---|
| `datos_basicos` | Nombre y dirección |
| `administracion` | Al menos una persona con rol Administración vigente |
| `viviendas` | Al menos una `Unidad` |
| `areas` | Al menos un área activa |
| `reglas_del_conjunto` | La **anticipación máxima** del conjunto vigente (una `Regla` sin área). El límite de reservas de un área no cuenta |
| `reglamento` | Al menos un `Reglamento` cargado |

**Quién lo deja operativo.** `POST /conjuntos/actual/activar/` exige `conjunto.activar`, que tienen el Superusuario y, desde el 2026-10-06, Administración. Si falta algo responde 400 con la lista de `faltantes`.

**El reglamento** (lo mínimo de HU-33) vive en `apps/documentos`. `servicios.guardar()` revisa, en orden: que no esté vacío, que pese hasta 10 MB y que empiece por `%PDF-` (la firma, no el nombre). Se guarda en la base con `BinaryField`, con su huella SHA-256, quién lo subió y cuándo. **Subir otro no borra el anterior:** se agrega una fila y el vigente es el más reciente. Las consultas que no necesitan el archivo lo dejan fuera con `defer("contenido")`. En el front, el navegador nunca habla con la API: el servidor del front recibe el PDF y lo reenvía con el token de la sesión, y de vuelta lo entrega él mismo (`conjuntos:reglamento-archivo`).

> [!WARNING] Lo que no hace todavía
> Dejar operativo un conjunto no queda en la auditoría. Un conjunto operativo no se vuelve a revisar si después deja de cumplir un requisito. Y reservar no exige que el conjunto esté operativo (plan D7 a del 27/09). Los tres están en [pendientes](../08_Estado/pendientes.md).

## Dar de baja un conjunto (2026-10-13, de Camilo)

Lo subió Camilo en `7eb5b5a` (backend) y `8279616` (front), sin que hubiera historia ni plan.

- **API:** `DELETE /conjuntos/actual/` llama a `servicios.eliminar(conjunto)`. En una sola transacción deja `activo = false` y `operativo = false` y pone en `None` el conjunto activo de **todas** las sesiones que lo tenían. No borra ninguna fila: es baja lógica ([eliminacion](../03_Reglas/eliminacion.md)). Responde 204; si ya estaba dado de baja, 400 «Este conjunto ya fue eliminado.».
- **Quién:** solo el Superusuario, dentro del conjunto. La vista pregunta `es_superusuario(request.user.persona)`; **no es un permiso del catálogo** (no existe `conjunto.eliminar`).
- **Front:** en el bloque «Datos básicos» del resumen, el Superusuario ve «Eliminar conjunto»; un diálogo pregunta «¿Está seguro de eliminar el conjunto …?» con «Sí, eliminar» y «No». Al confirmar, la vista limpia el conjunto activo y los permisos de la sesión y lleva al selector. Quien no es Superusuario no ve el botón, y si manda el `POST` a mano, la pantalla responde «No tienes permiso para eliminar este conjunto.» sin llamar a la API.
- **El selector cambió con esto.** `permisos.servicios.conjuntos_disponibles` ya no filtra por `activo` para el Superusuario: ve **todos** los conjuntos, también los dados de baja y los que todavía no son operativos (prueba `test_superusuario_ve_todos_los_conjuntos_creados_incluidos_los_inactivos`). Quien no es Superusuario sigue viendo solo los activos donde tiene un rol vigente. Como `puede_operar_en` usa esa misma consulta, el Superusuario puede **volver a entrar** a un conjunto dado de baja, y el selector no lo marca.

> [!WARNING] Contra lo diseñado
> [eliminacion](../03_Reglas/eliminacion.md) pide para desactivar un conjunto una **doble confirmación escrita** (el nombre exacto) y que sea reversible 30 días. Lo construido pide un «Sí / No» en el front y nada en la API; no hay cómo reactivarlo, y la baja **no deja fila en la auditoría**. Está anotado en [pendientes](../08_Estado/pendientes.md) (sección 5) para que Alejo decida; la nota de diseño no se tocó.

## Identidad: color y foto (HU-21)

**El color.** `Acento` suma una novena opción, `personalizado`, y `Conjunto` un campo `color_personalizado` (hex `#rrggbb` en minúsculas). La regla se cumple en tres capas:

| Capa | Dónde | Qué hace |
|---|---|---|
| Serializer | `serializers.py` → `validar_color()` | Personalizado sin color → 400 "Elige el color del conjunto". Color con un acento del catálogo → 400. Al volver a uno del catálogo, **borra** el color viejo |
| Vista | `ConjuntoActualView.patch()` | Mandar `color` exige el mismo permiso que el acento (`conjunto.branding` o `conjunto.activar`) |
| Base | `CHECK conjunto_color_personalizado_valido` | Personalizado ⇔ hay un hex válido. Nadie guarda un estado a medias ni por fuera de la API |

El backend **no calcula** la paleta ni el contraste: guarda el hex y ya. Pintarlo es trabajo del front ([implementacion](../04_Diseno/implementacion.md)).

**La foto.** Sigue guardándose como el "logo" (`LogoDeConjunto`, con su huella SHA-256 en `Conjunto.logo_huella`), pero ahora **debe ser cuadrada**. `servicios.guardar_logo()` revisa, en orden: que no esté vacía, que pese hasta 512 KB, que sea de verdad PNG, JPG o WebP (por su firma, no por la extensión) y que ancho = alto. Si no → `LogoInvalido` → 400 "La foto debe ser cuadrada (1:1). Esta mide 800 × 600 px".

¿Cómo sabe el tamaño sin instalar una librería de imágenes? `apps/conjuntos/imagenes.py` → `dimensiones()` **lee solo la cabecera** del archivo: cada formato guarda el ancho y el alto en bytes conocidos (el bloque `IHDR` del PNG, el marcador de inicio de cuadro del JPG, el fragmento `VP8`/`VP8L`/`VP8X` del WebP). No se decodifica ningún píxel.

> [!WARNING] Choca con lo decidido antes
> El 22/09 HU-21 se construyó con "solo los 8 acentos, sin hex libre" (maestro §6.3). El color propio lo pidió Alejo el 29/09 y **revierte** esa decisión. El maestro todavía no lo dice.

## Ver también

- [unidades](unidades.md) — el generador de viviendas del paso 2
- [motor_reglas](motor_reglas.md) — el tablero del paso 5
- [implementacion](../04_Diseno/implementacion.md) — cómo pinta el front el color y la foto
- [sistema_visual](../04_Diseno/sistema_visual.md) — el catálogo de 8 acentos y sus cuatro sitios
- [permisos](permisos.md) — `conjunto.crear` y `conjunto.activar`
- [eliminacion](../03_Reglas/eliminacion.md) — la baja lógica y la doble confirmación que pide el diseño
- [alcance](../01_Contexto/alcance.md) — qué es un conjunto operativo (3.1)
- [Plan_Asistente_De_Creacion](../07_Planes/hechos/Plan_Asistente_De_Creacion.md) — el plan del asistente completo
- [historias](../08_Estado/historias.md) — HU-03, HU-21 y HU-33
- `Backend/Admind_Backend/apps/conjuntos/README.md` y `apps/documentos/README.md`
