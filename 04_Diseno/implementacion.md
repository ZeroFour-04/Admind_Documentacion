---
resumen: "Cómo está implementado el sistema de diseño en el front: tokens, componentes am-*, acento por conjunto y foto."
tipo: diseno
origen: "guía de estructura §4.7 (2026-09-30)"
actualizado: 2026-10-11
revisado: 2026-10-11
---

# El sistema de diseño en el código

Vive en `Frontend/…/design-system/` y se importó del proyecto de Claude Design "AdMind Design System".

- **Tokens** (`tokens/*.css`): variables CSS con nombre de significado, no de color. Por ejemplo `--texto-fuerte`, `--superficie-tarjeta`, `--acento-600`. Cada par de colores trae anotado su contraste.
- **Componentes** (`tokens/componentes.css`): clases con prefijo `am-`: `am-btn`, `am-btn--primario`, `am-tarjeta`, `am-pastilla`, `am-campo`, `am-alerta`, `am-lateral`…
- **Acento por conjunto** (HU-21/HU-26): cada conjunto elige uno de **8 acentos** o, desde el 29/09, un **color propio**. El acento solo toca cuatro sitios: botón primario, ítem activo del lateral, anillo de foco y franja del conjunto.
  - Con uno de los 8, `base.html` pone `data-acento="azul"` en `<html>` y `colores.css` reapunta las variables `--acento-*` a esa rampa.
  - Con el propio no hay rampa hecha: `apps/conjuntos/colores.py` → `rampa(hex)` saca del color elegido los mismos cinco tonos (`--acento-50`, `-600`, `-700`, `-900` y el anillo) mezclándolo con blanco o negro, y la etiqueta `{% atributos_de_acento %}` (`apps/conjuntos/templatetags/conjuntos.py`) los escribe en el `style` de `<html>`, donde ganan sobre los de `:root`. El color **no se corrige** aunque sea poco legible: solo se advierte.
- **Foto del conjunto** (HU-21): `conjuntos/_foto.html` pinta la foto cuadrada en cuatro tamaños (barra, tarjeta, resumen, grande). Sin foto muestra un **marcador con las iniciales** (filtro `iniciales`: "Torres del Río" → "TR") en colores neutros.
- **Ícono de la pestaña** (`<link rel="icon">` en `templates/base/base.html`): si el conjunto activo tiene foto, la pestaña usa esa misma foto (`conjuntos:logo`, la URL con huella); si no, o si no hay sesión ni conjunto activo, usa el de AdMind en `static/img/` (`favicon.ico` de 16, 32 y 48 px, `favicon.png` y `apple-touch-icon.png`).
- **Estilos propios** de la estructura y de pantallas concretas en `static/css/` (`estructura.css`, `reservas.css`, `unidades.css` y `usuarios.css`).

> [!WARNING]
> Los acentos se agregaron a la copia local de `design-system/`. Si alguien re-sincroniza desde Claude Design sin llevarlos allá primero, se borran.

## Ver también

- [sistema_visual](sistema_visual.md) — los principios y el porqué
- [conjuntos](../05_Modulos/conjuntos.md) — color propio y foto 1:1 en el backend
- `Frontend/Admind_Front-End/design-system/README.md` — el inventario completo de tokens y componentes
