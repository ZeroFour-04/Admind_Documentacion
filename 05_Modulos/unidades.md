---
resumen: "Vínculos de unidad (propietario, arrendatario, reside) y enrutamiento de notificaciones por vínculo."
tipo: modulo
modulo: unidades
hu: [HU-08]
origen: "maestro v1.4 (2026-09-14) §5.5"
actualizado: 2026-10-06
---

# Unidades y vínculos

> [!WARNING] Decisión del 2026-10-06 (HU-39), sin construir
> Las viviendas dejan de registrarse solo una por una con nombre libre. El asistente las va a generar en lote, y cada una pertenece, si el conjunto las agrupa, a una **agrupación** (torre, bloque, manzana). Una unidad puede ser apartamento o casa. Lo decidido está en [construccion](../06_Decisiones/construccion.md) y el trabajo en [Plan_Estructura_De_Viviendas](../07_Planes/activos/Plan_Estructura_De_Viviendas.md). Mientras no se construya, el código sigue como dice esta nota.
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
