---
resumen: "Identidad del conjunto: acento o color propio y foto 1:1, con sus validaciones en tres capas."
tipo: modulo
modulo: conjuntos
hu: [HU-03, HU-21]
origen: "guía de estructura §5.7 (2026-09-30)"
actualizado: 2026-09-30
---

# Conjuntos: identidad (color y foto)

Qué es un conjunto operativo y cómo se crea está en [alcance](../01_Contexto/alcance.md) (3.1, Multiconjunto). El asistente de creación (HU-03) está parcial: falta el reglamento (HU-33).

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

- [implementacion](../04_Diseno/implementacion.md) — cómo pinta el front el color y la foto
- [sistema_visual](../04_Diseno/sistema_visual.md) — el catálogo de 8 acentos y sus cuatro sitios
