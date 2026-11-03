---
resumen: "El estilo visual del selector de conjuntos (una tarjeta con portada del color de cada conjunto) y del asistente de creación (pasos como píldoras y opciones elegidas con el acento), solo con CSS."
titulo: "AdMind — Plan del estilo visual: selector de conjuntos y asistente"
tipo: plan
estado: activo
hu: [HU-26, HU-03]
fecha: 2026-10-30
para: "Gemini Flash ejecuta; Alejo decide y revisa. No es guiado: el agente copia un archivo ya probado y agrega un enlace"
alcance: "Solo el front: una hoja nueva (static/css/conjuntos.css) y un enlace en base.html. Ninguna plantilla de conjuntos cambia"
punto_de_partida: "Frontend 734a8f7 (= main = desarrollo) más el plan del estilo base ya aplicado. Validado el 2026-10-30 en una copia: sin pruebas nuevas, la suite sigue en verde"
---

# AdMind — Plan del estilo visual: selector de conjuntos y asistente

> [!IMPORTANT]
> **Alejo: no hay decisiones que llenar.** Pero este plan **exige** que [Plan_Estilo_Visual_Base](Plan_Estilo_Visual_Base.md) ya esté hecho (en la rama o fundido). Sin él, no empieces.

## 0. Instrucciones para el agente

### 0.1 Qué leer antes de tocar código

1. Este plan completo.
2. `Frontend/Admind_Front-End/static/css/README.md`.
3. **No leas ni edites `Plan_Estilo_Visual_Recursos/conjuntos.css`**: es definitivo y se copia tal cual.

### 0.2 Reglas propias de este plan

- `conjuntos.css` se copia con `cp`; no se reescribe ni se «mejora». Fue probado el 2026-10-30 con seis conjuntos de seis acentos distintos (uno con color propio).
- La edición de `base.html` trae texto **viejo** y **nuevo**; el viejo debe aparecer **una sola vez**. Si no, **detente y avisa**.
- **Ninguna plantilla de conjuntos se toca.** La tarjeta del selector se restila solo con CSS sobre el HTML que ya existe, para no romper las pruebas de identidad.
- **Nada de commits ni de `push`.** Alejo hace la rama, el commit y el PR. Nada se instala.
- Terminal: Git Bash, rutas con espacios entre comillas. `RECURSOS` = `../../Documentacion/Admind_Documentacion/07_Planes/activos/Plan_Estilo_Visual_Recursos` desde `Frontend/Admind_Front-End`.

## 1. Punto de partida

- Antes de este plan: `static/css/estructura.css` ya tiene `.tarjeta-conjunto` (con una franja de 4 px arriba) y los estilos del asistente (`.pasos-asistente`, `.opciones-vivienda__opcion`, `.opciones-alcance__opcion`, `.frase-estructura`…). La elección de opciones se marcaba con neutros porque el diseño v1 reservaba el acento a cuatro sitios; la decisión de Alejo del 2026-10-30 lo relaja ([Plan_Estilo_Visual_Base](Plan_Estilo_Visual_Base.md), sección 1).
- La tarjeta de cada conjunto en el selector ya lleva `data-acento` (o el color propio en su `style`): por eso todo lo de `conjuntos.css` sale de `--acento-*` y toma **el color de su conjunto**, no el de la sesión.
- Las pruebas de `tests/test_identidad.py` miran el HTML del selector (`class="foto-conjunto foto-conjunto--tarjeta"` una vez, etc.): es otra razón para no tocar plantillas.

## 2. Decisiones que toma Alejo

Ninguna.

## 3. Decisiones menores que el plan ya fija

| ID | Decisión |
|---|---|
| P1 | La franja de 4 px de la tarjeta pasa a ser una **portada de 96 px** con degradado del color del conjunto; la foto (o las iniciales) monta sobre la portada y el nombre queda debajo, a su lado, y crece hacia abajo si ocupa dos líneas |
| P2 | Las iniciales sin foto se tiñen con el acento del conjunto (`--acento-100` con texto `--acento-900`, que siempre se lee) |
| P3 | El botón «Entrar al conjunto» ocupa todo el ancho y lleva una flecha hecha con CSS (`::after`), sin cambiar su texto |
| P4 | Los siete pasos del asistente se ven como píldoras; el paso actual, con el acento; los pasos aún no disponibles, apagados. El texto y `aria-current="step"` no cambian |
| P5 | Las opciones elegidas del asistente (tipo de vivienda, agrupación, numeración y las del alcance de anuncios, que comparten clase) se marcan con el acento del conjunto en vez de neutros |

## 4. Orden y dependencias

F0 → F1 → F2 → F3. Después del plan base. Es independiente del de Zonas comunes.

## F0 · Comprobar el punto de partida

Desde `Frontend/Admind_Front-End`:

```bash
git status --short
ls static/css/apariencia.css templates/componentes/_iconos.html design-system/tokens/efectos.css
grep -n "css/apariencia.css" templates/base/base.html
./.venv/Scripts/python.exe -m pytest -q
```

Se espera: `git status` solo con los cambios del plan base (o vacío si ya se fundió); los tres archivos existen; `base.html` ya enlaza `apariencia.css`; la suite en verde. **Si falta alguno de los tres archivos, el plan base no está hecho: detente y avisa a Alejo.**

## F1 · La hoja nueva y su enlace

```bash
R="../../Documentacion/Admind_Documentacion/07_Planes/activos/Plan_Estilo_Visual_Recursos"
cp "$R/conjuntos.css" static/css/conjuntos.css
```

Una edición en `templates/base/base.html`. Viejo:

```html
  <link rel="stylesheet" href="{% static 'css/apariencia.css' %}">
```

Nuevo:

```html
  <link rel="stylesheet" href="{% static 'css/apariencia.css' %}">
  <link rel="stylesheet" href="{% static 'css/conjuntos.css' %}">
```

**Se comprueba:** `grep -c "conjuntos.css" templates/base/base.html` devuelve `1`.

## F2 · Pruebas

No se agregan pruebas: `tests/test_apariencia.py` (del plan base) ya recorre `conjuntos.css` cuando existe y comprueba que **no tenga colores hex** ni use `--acento` en reglas de estado.

```bash
./.venv/Scripts/python.exe -m pytest -q
```

Se espera la misma cantidad de pruebas que antes de este plan, todas en verde (503 o 504).

## F3 · Verificación visual (la API en el 8000 y el front en el 8001)

La hace Alejo, o el agente si tiene un navegador. Necesita un usuario con **varios conjuntos** de acentos distintos (el Superusuario ve todos).

| Dónde | Qué debe verse |
|---|---|
| **Elige un conjunto** (`/conjuntos/`) | Una tarjeta por conjunto con **portada de degradado del color de ese conjunto**, foto o iniciales montadas sobre la portada, nombre y dirección debajo, botón del mismo color a todo el ancho con una flecha. Al pasar el mouse la tarjeta sube y gana sombra |
| Nombre largo | «Conjunto Los Almendros» ocupa dos líneas **debajo** de la portada, sin pisarla |
| Conjunto sin dirección | La tarjeta sigue ordenada |
| **Crear conjunto → asistente** | Los siete pasos como píldoras; el actual resaltado con el acento; los que aún no se pueden abrir, apagados |
| Paso 2, **Viviendas** | La opción elegida (apartamentos, torres, numeración…) con borde y fondo del acento |
| Pantalla angosta (≈ 375 px) | Las tarjetas en una columna; las píldoras bajan de línea; sin barra horizontal |

## F4 · Documentación (cierre)

Sigue [actualizar_contexto](../../09_Protocolos/actualizar_contexto.md):

- `04_Diseno/implementacion.md`: en la sección *La capa «con vida»* (la dejó el plan base) agregar `static/css/conjuntos.css` y qué restila (selector y asistente).
- `static/css/README.md` del front: agregar `conjuntos.css`.
- `05_Modulos/conjuntos.md`: en *Identidad: color y foto*, una línea: «En el selector, cada tarjeta lleva una portada con el degradado del color del conjunto (CSS en `conjuntos.css`)».
- `08_Estado/bitacora.md` (una fila); `actualizado:` y `revisado:` con `2026-10-30` en cada nota tocada.
- Al cerrar los **tres** planes de estilo, mover los planes y la carpeta de recursos a `07_Planes/hechos/` (ver el plan base, F6).

## Cierre del agente

`git status --short` debe listar **solo** `static/css/conjuntos.css` y `templates/base/base.html` (además de lo del plan base si todavía no se fundió). Suite en verde. Decir en el chat qué notas se tocaron.

## Lo que el agente no puede hacer

**Rama, commit y PR los hace Alejo.** Sugerido (después de fundir el plan base en `desarrollo`):

```bash
cd "Frontend/Admind_Front-End"
git switch desarrollo
git pull
git switch -c feat/estilo-visual-conjuntos
git add static/css/conjuntos.css templates/base/base.html
git commit -m "feat(diseno): selector de conjuntos con portada del color de cada conjunto y asistente con píldoras [HU-26]"
git push -u origin feat/estilo-visual-conjuntos
```

Y la prueba manual de F3 por alguien que no haya programado el cambio, con al menos tres acentos y un color propio.

## Guiones de prueba manual

La tabla de F3.

## Informe final que entrega el agente

En el chat: lo copiado y editado, pruebas antes y después, notas tocadas y desvíos.

## Fuera de este plan

- Cambiar el texto o el orden de las pantallas del asistente, o agregar pasos.
- Estilar otras pantallas que usan `.opciones-alcance` (el alcance de los anuncios) más allá de la marca de la opción elegida, que se comparte por la clase.
