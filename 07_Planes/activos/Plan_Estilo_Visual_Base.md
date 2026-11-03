---
resumen: "La base del nuevo estilo visual del front: tokens de efectos, degradados y sombras teñidas con el acento de cada conjunto, íconos en el lateral, animación de entrada y un fondo elegible (liso, color o cristal)."
titulo: "AdMind — Plan del estilo visual: la base"
tipo: plan
estado: activo
hu: []
fecha: 2026-10-30
para: "Gemini Flash ejecuta; Alejo decide y revisa. No es guiado: el agente copia archivos ya probados y hace unas pocas ediciones exactas"
alcance: "Solo el front. Archivos nuevos de CSS, JS y plantillas parciales; ediciones pequeñas en base.html, barra_superior.html, lateral.html, _enlaces_gestion.html y styles.css; una prueba nueva y una aserción corregida"
punto_de_partida: "Frontend 734a8f7 (= main = desarrollo), 495 pruebas en verde, sin cambios pendientes. Validado el 2026-10-30 en una copia: 504 pruebas con este plan y los otros tres aplicados (503 sin el de «Los escribo yo»)"
---

# AdMind — Plan del estilo visual: la base

> [!IMPORTANT]
> **Alejo: lee la sección 2 antes de dárselo al agente.** Trae mi recomendación ya escrita en la columna *Respuesta*; cámbiala si prefieres otra. Este plan es **el primero** de tres: [Plan_Estilo_Visual_Conjuntos](Plan_Estilo_Visual_Conjuntos.md) y [Plan_Estilo_Visual_Zonas_Comunes](Plan_Estilo_Visual_Zonas_Comunes.md) lo necesitan hecho.

## 0. Instrucciones para el agente

### 0.1 Qué leer antes de tocar código

1. Este plan completo.
2. [implementacion](../../04_Diseno/implementacion.md) (cómo está hoy el sistema de diseño) y `Frontend/Admind_Front-End/static/css/README.md`.
3. **No leas ni edites los archivos de `Plan_Estilo_Visual_Recursos/`**: son definitivos y se copian tal cual.

### 0.2 Reglas propias de este plan

- **Los archivos de `Plan_Estilo_Visual_Recursos/` se copian con `cp`, no se reescriben ni se «mejoran».** Fueron probados el 2026-10-30 (suite en verde, capturas en seis acentos y tres fondos, contraste medido).
- Cada edición trae el texto **viejo** y el **nuevo**. El viejo tiene que aparecer **una sola vez**; si aparece cero veces o más de una, **detente y avisa a Alejo**.
- **Nada de commits ni de `push`.** Alejo hace la rama, el commit y el PR.
- Nada se instala ni se descarga. Ninguna librería de CSS ni fuente externa.
- No toques ningún archivo que el plan no nombre. Tampoco el backend.
- Terminal: Git Bash. Las rutas con espacios van entre comillas.
- En este plan, `RECURSOS` significa `Documentacion/Admind_Documentacion/07_Planes/activos/Plan_Estilo_Visual_Recursos` y `FRONT` significa `Frontend/Admind_Front-End`. Desde `FRONT`, `RECURSOS` queda en `../../Documentacion/Admind_Documentacion/07_Planes/activos/Plan_Estilo_Visual_Recursos`.

## 1. Punto de partida

Verificado el 2026-10-30:

- Front en `desarrollo` = `main` = `734a8f7`, árbol limpio, 495 pruebas.
- El sistema de diseño está en `design-system/` (tokens en `tokens/*.css`, `styles.css` los importa) y los estilos propios en `static/css/`. `templates/base/base.html` carga `design-system/styles.css` y `css/estructura.css`.
- **Regla vigente que este plan relaja** (decisión de Alejo, 2026-10-30): el diseño v1 reservaba el acento a cuatro sitios, una sola sombra para lo que flota y ninguna animación de entrada ([sistema_visual](../../04_Diseno/sistema_visual.md) 6.1 y 6.2). Ahora el acento también es adorno (degradados, sombras teñidas, íconos, tarjetas). **Lo que no cambia:** los neutros y los cinco estados fijos; `--acento-*` no entra en ninguna regla que comunique estado; el color de cada conjunto (8 acentos o color propio) manda sobre todo lo nuevo.
- Hay **tres pruebas** que miran la forma exacta del HTML y condicionan el diseño: `tests/test_identidad.py` (`<header class="am-barra am-barra--con-menu">`, `<nav class="am-lateral" id="menu-lateral"`, `<div class="am-lateral__pie">` y `href="/conjuntos/">Cambiar de conjunto</a>`), las que buscan `>Texto</a>` en el lateral y `tests/test_acentos.py` (lee la primera regla de `colores.css`). Por eso los íconos van **delante** del texto y **no** en «Cambiar de conjunto», y los tokens nuevos van en un archivo aparte.

## 2. Decisiones que toma Alejo

| ID | Decisión | Opciones | Recomendada | Respuesta |
|---|---|---|---|---|
| D1 | Fondo que ve quien no ha elegido uno | a) **Cristal** (manchas desenfocadas con el color del conjunto y tarjetas de vidrio) b) Color (degradado suave, tarjetas blancas) c) Liso (como hasta hoy) | a | a |
| D2 | Dónde se guarda el fondo elegido | a) En el navegador de cada persona (`localStorage`; no hay backend) b) En la sesión del servidor del front | a | a |

Con D2 a, el fondo **no viaja entre dispositivos**: cada navegador recuerda el suyo. Con D2 b habría que tocar vistas y plantillas de sesión; no se recomienda para esto.

## 3. Decisiones menores que el plan ya fija

| ID | Decisión |
|---|---|
| P1 | Los tonos nuevos (`--acento-100`, `-200`, `-400`, `--acento-vecino`, degradados, sombras, vidrio) se **derivan** de `--acento-600` con `color-mix()`. Así funcionan igual con los 8 acentos y con el color propio, sin tocar el backend ni `colores.py` |
| P2 | Los tokens nuevos viven en **un archivo nuevo**, `design-system/tokens/efectos.css`, importado al final de `styles.css`. Volver al aspecto de antes = quitar ese `@import` y los `<link>` nuevos de `base.html` |
| P3 | Los estilos de componentes viven en `static/css/apariencia.css`, que se carga **después** de `estructura.css` y **antes** de la hoja de cada pantalla |
| P4 | Tres fondos: **liso** (el de hoy), **color** y **cristal**. Se eligen en un botón de paleta en la barra superior (también en el selector de conjuntos y las pantallas con barra). Lo aplica `static/js/apariencia.js`, que va en el `<head>` **sin `defer`** para que no haya parpadeo. Sin JavaScript queda liso |
| P5 | Íconos: un conjunto de símbolos SVG (`_iconos.html`) que se incluye **una vez** en `base.html`; se usan con `<svg class="am-icono"><use href="#i-…"></use></svg>`. Sin librería externa |
| P6 | Los íconos del lateral los pone un script (`agregar_iconos.py`) que **no adivina**: si encuentra un enlace de un módulo que no conoce, se detiene y lo dice |
| P7 | La animación de entrada (`aparecer`) y las manchas del fondo respetan `prefers-reduced-motion` (`base.css` ya acorta las duraciones; las manchas se detienen) |
| P8 | El vidrio **no** se apaga con `prefers-reduced-transparency` (Windows lo reporta aunque «Efectos de transparencia» esté apagado). Es casi opaco: el texto más claro de una tarjeta mide ≥ 4.6:1 sobre cualquier mancha con azul, vino, pizarra, terracota, verde y un color propio |
| P9 | Un solo cambio en una prueba existente: en `tests/test_unidades.py`, la aserción `'aria-current="page">Unidades</a>'` pasa a una expresión regular que admite el ícono delante |

## 4. Orden y dependencias

F0 → F1 → F2 → F3 → F4 → F5 → F6. Va **primero**. El plan de «Los escribo yo» es independiente.

## F0 · Comprobar el punto de partida

Desde `FRONT`:

```bash
git status --short
for f in templates/base/base.html templates/componentes/barra_superior.html templates/componentes/lateral.html templates/componentes/_enlaces_gestion.html design-system/styles.css tests/test_unidades.py; do echo "$f  $(git log -1 --format=%h -- $f)"; done
./.venv/Scripts/python.exe -m pytest -q
```

Se espera: `git status` vacío; últimos commits `2af7114` (base.html), `f5b3d08` (barra_superior), `734a8f7` (lateral), `6200f12` (_enlaces_gestion), `8d0bedb` (styles.css) y `a946880` (test_unidades); `495 passed` (o `496` si ya se hizo el plan de «Los escribo yo»). Si un archivo tiene otro último commit, **alguien lo cambió**: detente y avisa a Alejo antes de seguir.

Comprueba también que existen en `RECURSOS` los siete archivos que este plan usa: `efectos.css`, `apariencia.css`, `apariencia.js`, `_iconos.html`, `_apariencia.html`, `agregar_iconos.py` y `test_apariencia.py`. (`conjuntos.css`, `reservas.css` y `calendario.html`, que también están ahí, son de los otros planes.)

## F1 · Los archivos nuevos (copiar)

Desde `FRONT`:

```bash
R="../../Documentacion/Admind_Documentacion/07_Planes/activos/Plan_Estilo_Visual_Recursos"
cp "$R/efectos.css" design-system/tokens/efectos.css
cp "$R/apariencia.css" static/css/apariencia.css
cp "$R/apariencia.js" static/js/apariencia.js
cp "$R/_iconos.html" templates/componentes/_iconos.html
cp "$R/_apariencia.html" templates/componentes/_apariencia.html
```

Después, **una edición** en `design-system/styles.css`. Viejo:

```css
@import url("tokens/componentes.css");
```

Nuevo:

```css
@import url("tokens/componentes.css");
@import url("tokens/efectos.css");
```

**Se comprueba:** `ls design-system/tokens/efectos.css static/css/apariencia.css static/js/apariencia.js templates/componentes/_iconos.html templates/componentes/_apariencia.html` lista los cinco.

## F2 · Enganchar en la base y en la barra

**2.1** `templates/base/base.html`. Viejo (tres líneas seguidas):

```html
  <link rel="stylesheet" href="{% static 'css/estructura.css' %}">
  {% block estilos %}{% endblock %}
</head>
<body>
```

Nuevo:

```html
  <link rel="stylesheet" href="{% static 'css/estructura.css' %}">
  <link rel="stylesheet" href="{% static 'css/apariencia.css' %}">
  {% block estilos %}{% endblock %}
  {# Pone el fondo elegido en <html> antes de pintar: va sin defer, a propósito. #}
  <script src="{% static 'js/apariencia.js' %}"></script>
</head>
<body>
  {% include "componentes/_iconos.html" %}
```

**2.2** `templates/componentes/barra_superior.html`. Viejo (una línea):

```html
    <div class="am-barra__derecha">
```

Nuevo:

```html
    <div class="am-barra__derecha">
      {% include "componentes/_apariencia.html" %}
```

No cambies nada más de la barra (el `<header class="am-barra…">` debe quedar idéntico).

## F3 · Íconos en el lateral

Desde `FRONT`, con el Python del proyecto:

```bash
./.venv/Scripts/python.exe "../../Documentacion/Admind_Documentacion/07_Planes/activos/Plan_Estilo_Visual_Recursos/agregar_iconos.py" templates/componentes/lateral.html templates/componentes/_enlaces_gestion.html
```

Se espera exactamente: `lateral.html: 17 iconos puestos` y `_enlaces_gestion.html: 3 iconos puestos`. Si dice otro número o se detiene con un mensaje, **no sigas**: avisa a Alejo con el mensaje.

**Se comprueba:**

```bash
grep -c 'class="am-icono"' templates/componentes/lateral.html templates/componentes/_enlaces_gestion.html   # 17 y 3
grep -n "Cambiar de conjunto" templates/componentes/lateral.html   # el enlace del pie sigue SIN svg: ...">Cambiar de conjunto</a>
git diff --stat templates/componentes/lateral.html templates/componentes/_enlaces_gestion.html   # solo líneas de enlaces cambiadas
```

## F4 · Pruebas

**4.1** Copiar la prueba nueva:

```bash
cp "../../Documentacion/Admind_Documentacion/07_Planes/activos/Plan_Estilo_Visual_Recursos/test_apariencia.py" tests/test_apariencia.py
```

**4.2** `tests/test_unidades.py` (el archivo ya importa `re`). Viejo (una línea):

```python
    assert 'aria-current="page">Unidades</a>' in html
```

Nuevo:

```python
    assert re.search(r'aria-current="page">(?:<svg.*?</svg>)?Unidades</a>', html)
```

**4.3** Correr toda la suite:

```bash
./.venv/Scripts/python.exe -m pytest -q
```

Se espera: **503 passed** si no se hizo el plan de «Los escribo yo», **504** si ya está. (495 o 496 de antes + 8 pruebas nuevas.) Si falla alguna otra prueba, lee el error: casi seguro es una aserción sobre la forma exacta de un enlace del lateral. **No cambies pruebas fuera de la de `test_unidades.py`**: avisa a Alejo con el nombre de la prueba y el error.

## F5 · Verificación visual (la API en el 8000 y el front en el 8001)

El agente no puede ver la pantalla; esto lo mira Alejo (o el agente si tiene un navegador). Con sesión iniciada y un conjunto activo:

| Qué mirar | Debe verse |
|---|---|
| Fondo por defecto | Manchas desenfocadas con el color del conjunto, tarjetas translúcidas, barra y lateral de vidrio |
| Botón de paleta (barra, arriba a la derecha) | Abre un panel con **Liso / Color / Cristal**; al elegir cambia al instante y **se recuerda al recargar** |
| Lateral | Un ícono delante de cada sección; el activo con fondo de acento suave y barra a la izquierda; al pasar el mouse el ícono se agranda |
| Barra | Franja de color con degradado, marca con cuadrito de color, sombra suave; queda fija al bajar |
| Encabezado de cada vista | Banda con degradado suave del color del conjunto |
| Contenido al cargar | Los bloques suben y aparecen uno tras otro (≈ medio segundo) |
| Botón primario | Degradado del color del conjunto con sombra; sube un pixel al pasar el mouse |
| Pastillas de estado | **Siguen con sus colores fijos** (verde, ámbar, rojo, gris, azul), ahora con un punto delante. Ninguna toma el color del conjunto |
| Otro conjunto | Entrar a un conjunto con otro acento (o color propio) cambia **todo** lo nuevo a ese color |
| Pantalla angosta (≈ 375 px) | El menú sale como panel; el botón de paleta cabe en la barra; no hay barra de desplazamiento horizontal |
| Ingreso (`/`) | Tarjeta redondeada con sombra y la marca nueva |

Si Alejo prefiere otro fondo por defecto, cambia `var PREDETERMINADO = "cristal";` en `static/js/apariencia.js` (y el texto de `test_apariencia.py`, que lo comprueba).

## F6 · Documentación (cierre)

Sigue [actualizar_contexto](../../09_Protocolos/actualizar_contexto.md). Solo lo que cambió:

- `04_Diseno/sistema_visual.md`: **un aviso nuevo** dentro del cuadro *Decisiones posteriores a este texto* (al inicio): «**2026-10-30:** capa visual «con vida» (solo front): el acento deja de limitarse a cuatro sitios y las tarjetas, botones y encabezados llevan sombras y degradados teñidos con el acento; hay animación de entrada y un fondo elegible (liso, color o cristal). **Siguen vigentes:** estados con colores fijos, `--acento-*` fuera de toda regla de estado, contraste de 4.5:1 y `prefers-reduced-motion`». **No se reescribe** el texto de 6.1 y 6.2.
- `04_Diseno/implementacion.md`: una sección *La capa «con vida»* con: `tokens/efectos.css` (derivados del acento, formas, sombras, vidrio), `static/css/apariencia.css`, `static/js/apariencia.js` (fondo en `localStorage`, clave `admind.fondo`), `templates/componentes/_iconos.html` y `_apariencia.html`, y cómo volver atrás (P2).
- `03_Reglas/reglas_frontend.md`: en la fila de `templates/componentes/` («el inventario es cerrado») agregar que `_iconos.html` y `_apariencia.html` son parciales de apoyo, no componentes nuevos del inventario.
- `06_Decisiones/construccion.md`: una fila nueva al final: 2026-10-30; «Capa visual «con vida» solo en el front: más color y personalidad sin perder el color de cada conjunto (todo se deriva de `--acento-*`). **Relaja** sistema_visual 6.1 y 6.2 (cuatro sitios del acento, una sola sombra, sin animación de entrada). Fondo elegible por persona (liso, color o cristal) guardado en su navegador; el vidrio no se apaga con `prefers-reduced-transparency` (P8)»; quién: Alejo, en chat; dónde: este plan y `implementacion.md`.
- READMEs del front: `design-system/README.md` (agregar `tokens/efectos.css`), `static/css/README.md` (agregar `apariencia.css` y, en *Lo que no va*, aclarar que los tonos derivados del acento van en `tokens/efectos.css`), `static/js/README.md` (agregar `apariencia.js`), `templates/componentes/README.md` (agregar `_iconos.html` y `_apariencia.html`).
- `08_Estado/bitacora.md` (una fila), `02_Arquitectura/pruebas_y_ejecucion.md` y `08_Estado/estado_actual.md` (el conteo de pruebas del front sube en 8).
- En cada nota tocada, `actualizado:` y `revisado:` con `2026-10-30`.
- Cuando **los tres** planes de estilo estén hechos, mover los tres y la carpeta `Plan_Estilo_Visual_Recursos/` a `07_Planes/hechos/`, con `estado: hecho` y `ejecutado:` en el frontmatter, y cambiar sus filas en `07_Planes/planes.md`. Mientras falte alguno, la carpeta de recursos se queda en `activos/`.

## Cierre del agente

Desde `FRONT`: `git status --short` debe listar **solo** estos archivos: `design-system/styles.css`, `design-system/tokens/efectos.css`, `static/css/apariencia.css`, `static/js/apariencia.js`, `templates/base/base.html`, `templates/componentes/_apariencia.html`, `_iconos.html`, `barra_superior.html`, `lateral.html`, `_enlaces_gestion.html`, `tests/test_apariencia.py` y `tests/test_unidades.py`. La suite en verde (503 o 504). Después, decir en el chat qué notas se tocaron, una línea por nota.

## Lo que el agente no puede hacer

**Rama, commit y PR los hace Alejo** ([git](../../03_Reglas/git.md)). Comandos sugeridos:

```bash
cd "Frontend/Admind_Front-End"
git switch desarrollo
git pull
git switch -c feat/estilo-visual-base
git add design-system/styles.css design-system/tokens/efectos.css static/css/apariencia.css static/js/apariencia.js templates/base/base.html templates/componentes tests/test_apariencia.py tests/test_unidades.py
git commit -m "feat(diseno): capa visual con vida: degradados y sombras del acento, íconos, animación de entrada y fondo elegible"
git push -u origin feat/estilo-visual-base
```

Después el PR hacia `desarrollo`, y la prueba manual de la tabla de F5 por alguien que no haya programado el cambio.

## Guiones de prueba manual

La tabla de F5. Falta probar además: **cada uno de los 8 acentos** y un color propio claro (por ejemplo `#f5d90a`): con un color muy claro el texto blanco de los botones se lee mal; eso ya lo avisa la pantalla de identidad y **no se corrige**.

## Informe final que entrega el agente

En el chat: archivos copiados y editados por fase, el resultado de `agregar_iconos.py`, pruebas antes y después, notas tocadas y cualquier desvío.

## Fuera de este plan

- Los otros dos planes de estilo (selector y asistente; Zonas comunes).
- Restilar cada pantalla una por una (Usuarios, Unidades, Reglas, Casos…): heredan la base (tarjetas, botones, tablas, pastillas, campos), pero su estructura no cambia.
- **Modo oscuro:** no se hace. Los tokens quedaron listos para agregarlo después.
- Fondos con foto propia (un fondo de imagen elegido por la persona): no se hace; el fondo «cristal» usa solo el color del conjunto.
- Cambiar el backend o el modelo del conjunto.
