---
resumen: "Vínculos de unidad (propietario, arrendatario, reside) y enrutamiento de notificaciones por vínculo."
tipo: modulo
modulo: unidades
hu: [HU-08, HU-39]
origen: "maestro v1.4 (2026-09-14) §5.5"
actualizado: 2026-10-06
---

# Unidades y vínculos

> [!NOTE] Decisión del 2026-10-06 (HU-39): primera parte construida ese día, sin commit
> Las viviendas dejan de registrarse solo una por una con nombre libre. El asistente las genera en lote, y cada una pertenece, si el conjunto las agrupa, a una **agrupación** (torre, bloque, manzana). Una unidad puede ser apartamento o casa. Lo decidido está en [construccion](../06_Decisiones/construccion.md) y cómo quedó, en *Estructura de viviendas: cómo está construida*, más abajo. Falta la segunda parte: las palabras del conjunto en las pantallas, registrar a mano dentro de una agrupación y retirar viviendas.
>
> Si hay una persona principal de la vivienda sigue sin decidir: [abiertas](../06_Decisiones/abiertas.md) 12.9.

> [!WARNING] Decisión del 2026-10-06: tercer tipo de vínculo, `habitante`, sin construir
> El diseño de abajo dice `tipo ∈ {propietario, arrendatario}`. Alejo decidió un tercero, **`habitante`**: quien vive en la vivienda sin ser dueño ni arrendatario (la familia, un conviviente). Siempre lleva `reside = true` y puede no tener cuenta ni rol; los menores se registran con su documento.
>
> | Hecho | ¿Le llega al habitante? |
> |---|---|
> | Reserva, anuncio operativo, visitante en portería (`reside = true`) | Sí |
> | Anuncio dirigido a su vivienda | Sí |
> | Convocatoria de asamblea, mora | No: solo al propietario |
> | Comunicación de infracción | No: solo a propietario y arrendatario (C-318/02) |
>
> Un habitante con cuenta puede reservar a nombre de su vivienda, y en las zonas con ingreso se le encuentra por su documento ([ingresos](ingresos.md)). Los anuncios de todo el conjunto llegan por rol, no por vínculo: sin cuenta no recibe ninguno. En el código, hoy `VINCULOS_POR_HECHO` toma «todos los vínculos» para la infracción; al construir pasa a nombrar los dos tipos. Detalle en [construccion](../06_Decisiones/construccion.md).

## Estructura de viviendas: cómo está construida (HU-39, 2026-10-06)

- **Dos niveles, el primero opcional.** `Agrupacion` guarda la palabra del conjunto (`etiqueta`: Torre, Manzana…), su `nombre` (1, A, Esmeralda), el `tipo_vivienda` y el `orden` de creación, con el que «Torre 2» va antes que «Torre 10». `Unidad` suma `tipo` (apartamento o casa), `agrupacion` (puede faltar), `numero` y `piso`; su `nombre` sigue siendo el texto completo ya armado («Torre 1 – Apto 101»), que es lo que muestran visitantes, anuncios y reservas.
- **Comparar sin tildes ni mayúsculas.** `Agrupacion.clave` es la etiqueta y el nombre pasados por `estructura.clave()`. La restricción única va sobre ella, así que «Torre 1» y «TORRE 1» no conviven; «Torre 1» y «Manzana 1», sí.
- **El generador es una función pura.** `apps/unidades/estructura.py` → `generar(descripcion)` recibe la descripción de una **tanda** (un grupo de viviendas del mismo tipo) y devuelve las viviendas con su nombre. No importa modelos ni toca la base, y por eso la vista previa y la creación usan el mismo cálculo. Un conjunto mixto son dos tandas; una ampliación es otra tanda más adelante.
- **Cuatro patrones de numeración:** `piso_consecutivo` (101, 102… solo apartamentos), `consecutivo` (reinicia en cada agrupación), `corrido` (sigue de una a la siguiente) y `lista` (los números que escriba el administrador).
- **Guardar es todo o nada.** `servicios.generar_estructura()` crea en una transacción las agrupaciones que falten y las viviendas nuevas con `bulk_create` (el conjunto se fija a mano, porque `bulk_create` se salta `save()`), y deja **un** registro `unidad.generar` en la auditoría. Las viviendas que ya existen se omiten y se informa cuántas. Si una agrupación existe con otro tipo de vivienda, o si otra persona generó lo mismo a la vez, responde `409`.
- **Topes por tanda,** en el serializer: 60 agrupaciones, 60 pisos, 40 apartamentos por piso, 500 viviendas por agrupación y 2 000 en total.
- **API,** las tres con `vinculo.gestionar`: `POST /unidades/estructura/previsualizar/` (no guarda), `POST /unidades/estructura/` (201 si creó algo, 200 si todo existía) y `GET /unidades/agrupaciones/`. `GET /unidades/` ordena por agrupación, piso y número.
- **En el front,** el paso «2. Viviendas» del asistente. Alpine (`static/js/viviendas.js`) solo arma la descripción y la frase que la resume; la descripción viaja en un campo oculto y la API la valida y calcula.
- **Lo registrado a mano** (`POST /unidades/`) queda como apartamento, sin agrupación y sin número.

## Diseño (maestro §5.5)

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
