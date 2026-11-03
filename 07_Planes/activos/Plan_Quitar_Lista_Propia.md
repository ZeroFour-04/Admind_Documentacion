---
resumen: "Quitar del todo la opción «Los escribo yo» del paso Viviendas del asistente de creación de conjuntos (solo el front)."
titulo: "AdMind — Plan para quitar «Los escribo yo»"
tipo: plan
estado: activo
hu: [HU-39]
fecha: 2026-10-30
para: "Gemini Flash ejecuta; Alejo decide y revisa. No es guiado: el agente construye"
alcance: "Frontend: plantilla asistente_viviendas.html, static/js/viviendas.js y una prueba nueva. El backend no se toca"
punto_de_partida: "Frontend 734a8f7 (= main = desarrollo), 495 pruebas en verde, sin cambios pendientes. Validado el 2026-10-30 en una copia: queda en 496 pruebas"
---

# AdMind — Plan para quitar «Los escribo yo»

> [!IMPORTANT]
> **Alejo: no hay decisiones que llenar.** El plan se puede ejecutar tal cual. Sale en un solo commit y un solo PR.

## 0. Instrucciones para el agente

### 0.1 Qué leer antes de tocar código

1. Este plan completo.
2. `Frontend/Admind_Front-End/apps/conjuntos/README.md` (solo para ubicarte).
3. No hace falta leer más: las ediciones de abajo ya traen el texto exacto.

### 0.2 Reglas propias de este plan

- **Solo lo que dice el plan.** No «mejores» nada alrededor, no reformatees archivos, no toques el backend.
- Cada edición trae el texto **viejo** y el **nuevo**. El texto viejo tiene que aparecer **una sola vez** en el archivo; si aparece cero veces o más de una, **detente y avisa a Alejo**.
- **Nada de commits ni de `push`.** Los cambios se quedan en el árbol de trabajo. Alejo hace el commit y el PR.
- Nada se instala ni se descarga.
- Terminal: Git Bash. La carpeta del proyecto tiene espacios, las rutas van entre comillas.

## 1. Punto de partida

Verificado el 2026-10-30:

- `Frontend/Admind_Front-End` está en `desarrollo`, igual a `main` (`734a8f7`), con el árbol limpio.
- La opción se llama «Los escribo yo» en pantalla y `lista` por dentro. Vive en **dos archivos**:
  - `apps/conjuntos/templates/conjuntos/asistente_viviendas.html` (una opción de radio, un campo de texto y tres condiciones `patron !== 'lista'`).
  - `static/js/viviendas.js` (el estado `lista`, `numerosPropios` y cuatro ramas `patron === "lista"`).
- Ninguna prueba existente menciona la opción.
- **El backend sigue aceptando `patron: "lista"`** (`apps/unidades/estructura.py`, `serializers.py` y sus pruebas). Este plan no lo toca: ver *Fuera de este plan*.

## 2. Decisiones que toma Alejo

Ninguna.

## 3. Decisiones menores que el plan ya fija

| ID | Decisión |
|---|---|
| P1 | Solo se quita del front. Con la opción fuera, el navegador nunca manda `patron: "lista"` |
| P2 | `enLineas()` en `viviendas.js` **se queda**: la usa «Con nombre propio» |
| P3 | No se agrega ninguna defensa para un estado viejo con `patron: "lista"`: el estado solo viaja de una vista previa a la siguiente pantalla del mismo servidor |

## 4. Orden y dependencias

F0 → F1 → F2 → F3 → F4 → F5. Es independiente de los planes de estilo visual: se puede hacer antes, después o en paralelo (no comparten archivos).

## F0 · Comprobar el punto de partida

Desde `Frontend/Admind_Front-End`:

```bash
git status --short
git log -1 --format=%h -- apps/conjuntos/templates/conjuntos/asistente_viviendas.html static/js/viviendas.js tests/test_asistente_viviendas.py
./.venv/Scripts/python.exe -m pytest -q
```

Se espera: `git status` vacío; el último commit de esos archivos es `1f624b5` o `6e0c628`; `495 passed`. Si algo difiere, **detente y avisa**.

## F1 · La plantilla

Archivo: `apps/conjuntos/templates/conjuntos/asistente_viviendas.html`. Cinco ediciones.

**1.1** Quitar la opción de radio. Viejo:

```html
    <label class="opciones-alcance__opcion">
      <input type="radio" name="patron" value="lista" x-model="patron">
      <span><b>Los escribo yo</b> <span class="am-campo__ayuda">Para lo que no sigue un patrón, como PH o 1A.</span></span>
    </label>
```

Nuevo: *(nada; se borran esas 4 líneas)*.

**1.2** Viejo: `x-show="iguales && patron !== 'lista'"` → Nuevo: `x-show="iguales"`

**1.3** Quitar el campo de texto. Viejo:

```html
    <div class="am-campo" x-show="patron === 'lista'" style="display:none">
      <label class="am-campo__etiqueta" for="lista-de-numeros">Un número por línea</label>
      <textarea class="am-campo__control campo-texto-largo" id="lista-de-numeros" x-model="lista"></textarea>
    </div>
```

Nuevo: *(nada; se borran esas 4 líneas)*.

**1.4** Viejo: `x-show="agrupa && filas.length > 1 && patron !== 'lista'"` → Nuevo: `x-show="agrupa && filas.length > 1"`

**1.5** Viejo: `x-show="!iguales && patron !== 'lista'"` → Nuevo: `x-show="!iguales"`

**Se comprueba:** `grep -n "lista" apps/conjuntos/templates/conjuntos/asistente_viviendas.html` no devuelve nada.

## F2 · El JavaScript

Archivo: `static/js/viviendas.js`. Siete ediciones.

**2.1** Viejo: `"iguales", "pisos", "porPiso", "primerPiso", "cantidad", "filas", "patron", "desde", "lista"];` → Nuevo: `"iguales", "pisos", "porPiso", "primerPiso", "cantidad", "filas", "patron", "desde"];`

**2.2** Viejo:

```js
    desde: 1,
    lista: "",
```

Nuevo:

```js
    desde: 1,
```

**2.3** Quitar el getter. Viejo:

```js
    get numerosPropios() {
      return enLineas(this.lista);
    },
```

Nuevo: *(nada; se borran esas 3 líneas, y la línea en blanco que quedaba debajo se queda como está)*.

**2.4** Viejo: `        if (this.patron === "lista") return { nombre };` *(una línea con 8 espacios de sangría)* → Nuevo: *(nada; se borra la línea entera)*.

**2.5** Viejo: `      if (this.patron === "lista") return this.numerosPropios.length * this.agrupaciones.length;` → Nuevo: *(nada; se borra la línea entera)*.

**2.6** Viejo: `      if (this.patron === "lista") datos.numeros = this.numerosPropios;` → Nuevo: *(nada; se borra la línea entera)*.

**2.7** Viejo: `if (!this.iguales || this.patron === "lista") return` → Nuevo: `if (!this.iguales) return`

**Se comprueban dos cosas:**

```bash
grep -n "lista\|numerosPropios" static/js/viviendas.js   # no devuelve nada
node --check static/js/viviendas.js                       # sin salida = sintaxis correcta
```

## F3 · La prueba

Archivo: `tests/test_asistente_viviendas.py`.

**3.1** Agregar el import. Viejo:

```python
from unittest import mock

from cliente_api.http import ErrorDeApi
```

Nuevo:

```python
from unittest import mock

from django.conf import settings

from cliente_api.http import ErrorDeApi
```

**3.2** Agregar al **final** del archivo (dejando dos líneas en blanco antes):

```python
def test_el_paso_ofrece_tres_patrones_y_ninguno_pide_escribir_los_numeros_a_mano():
    cliente = cliente_con_sesion(permisos=ADMINISTRACION)
    with mock.patch("cliente_api.unidades.agrupaciones", return_value=SIN_VIVIENDAS):
        html = cliente.get("/conjuntos/asistente/viviendas/").content.decode()

    for patron in ("piso_consecutivo", "consecutivo", "corrido"):
        assert f'name="patron" value="{patron}"' in html
    assert 'value="lista"' not in html
    assert "Los escribo yo" not in html and "Un número por línea" not in html
    assert "lista" not in (settings.BASE_DIR / "static" / "js" / "viviendas.js").read_text(encoding="utf-8")
```

## F4 · Verificación

```bash
./.venv/Scripts/python.exe -m pytest -q
```

Se espera **496 passed**. Si algo falla, no sigas: léelo, corrige solo lo que el plan toca o avisa a Alejo.

Prueba manual (la hace Alejo o el agente con la API en el puerto 8000 y el front en el 8001): entrar como administrador, **Crear conjunto → paso 2, Viviendas**. Elegir «Apartamentos» y «Torres»: debe mostrar **solo tres** formas de numeración (*Piso y consecutivo*, *Consecutivo*, *Consecutivo corrido*), sin «Los escribo yo» ni el campo «Un número por línea». Con «Piso y consecutivo» y los valores de partida, la frase debe decir *1 torre de 5 pisos con 4 apartamentos por piso: 20 apartamentos* y **Ver cómo queda** debe habilitarse.

## F5 · Documentación (cierre)

Sigue [actualizar_contexto](../../09_Protocolos/actualizar_contexto.md). Solo lo que cambió:

- `Documentacion/Admind_Documentacion/05_Modulos/unidades.md`, línea de los *cuatro patrones de numeración*: agregar al final de esa viñeta: «Desde el 2026-10-30 el asistente del front **ya no ofrece `lista`** (decisión de Alejo: en la práctica no servía); la API la sigue aceptando».
- `06_Decisiones/construccion.md`: una fila nueva al final: fecha 2026-10-30; «El asistente de creación deja de ofrecer *Los escribo yo* (patrón `lista`); solo se quitó del front, la API sigue aceptándolo»; quién decidió: Alejo, en chat; dónde quedó: `unidades.md` y este plan.
- `08_Estado/bitacora.md`: una fila con la fecha y qué pasó (sin hash: no hay commit todavía).
- `02_Arquitectura/pruebas_y_ejecucion.md` y `08_Estado/estado_actual.md`: el conteo de pruebas del front pasa de 495 a **496**.
- En cada nota tocada, `actualizado:` y `revisado:` con `2026-10-30`.
- Mover este plan a `07_Planes/hechos/`, con `estado: hecho` y `ejecutado: 2026-10-30` en su frontmatter, y cambiar su fila en `07_Planes/planes.md`.

## Cierre del agente

Comandos finales (desde `Frontend/Admind_Front-End`): `git status --short` debe listar **solo** `asistente_viviendas.html`, `viviendas.js` y `test_asistente_viviendas.py`; `pytest` en **496 passed**. Después, decir en el chat qué notas se tocaron, una línea por nota.

## Lo que el agente no puede hacer

La parte humana de la Definition of Done ([scrum_y_dod](../../03_Reglas/scrum_y_dod.md)): **commit, rama y PR los hace Alejo** ([git](../../03_Reglas/git.md)). Comandos sugeridos para él:

```bash
cd "Frontend/Admind_Front-End"
git switch desarrollo
git pull
git switch -c fix/quitar-lista-propia
git add apps/conjuntos/templates/conjuntos/asistente_viviendas.html static/js/viviendas.js tests/test_asistente_viviendas.py
git commit -m "fix(conjuntos): quitar la opción «Los escribo yo» del paso de viviendas [HU-39]"
git push -u origin fix/quitar-lista-propia
```

Después abre el PR hacia `desarrollo` desde GitHub. Y la prueba manual de quien no programó el cambio.

## Guiones de prueba manual

Ver F4.

## Informe final que entrega el agente

En el chat: qué ediciones se hicieron (F1 a F3), pruebas antes (495) y después (496), notas tocadas y cualquier desvío.

## Fuera de este plan

- **El backend sigue aceptando `patron: "lista"`.** Está en `Backend/Admind_Backend/apps/unidades/estructura.py` (`Patron.LISTA` y su rama), `serializers.py` (la validación de `numeros`) y `test_estructura.py` (`test_con_lista_los_numeros_son_los_que_se_escriben`). Quitarlo del todo es un cambio de backend, aparte, que Alejo decide.
- La nota histórica `07_Planes/hechos/Plan_Estructura_De_Viviendas.md` sigue hablando de `lista`: un plan hecho no se edita.
