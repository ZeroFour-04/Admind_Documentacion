---
resumen: "Rediseño de la pantalla «Zonas comunes»: cada zona como una tarjeta con su estado, su horario y su medidor de cupos, y el calendario con las franjas del día lado a lado. Cambia la plantilla, la hoja de la pantalla y cinco aserciones de pruebas."
titulo: "AdMind — Plan del estilo visual: Zonas comunes"
tipo: plan
estado: activo
hu: [HU-11]
fecha: 2026-10-30
para: "Gemini Flash ejecuta; Alejo decide y revisa. No es guiado: el agente copia dos archivos ya probados y hace cinco ediciones exactas en una prueba"
alcance: "Solo el front: apps/reservas/templates/reservas/calendario.html, static/css/reservas.css y tests/test_reservas.py. La vista (views.py), la API y las demás pantallas de reservas no se tocan"
punto_de_partida: "Frontend 734a8f7 (= main = desarrollo) más el plan del estilo base ya aplicado. Validado el 2026-10-30 en una copia: la suite completa sigue en verde"
---

# AdMind — Plan del estilo visual: Zonas comunes

> [!IMPORTANT]
> **Alejo: no hay decisiones que llenar.** Este plan **exige** que [Plan_Estilo_Visual_Base](Plan_Estilo_Visual_Base.md) ya esté hecho. Sin él, no empieces: la plantilla usa sus íconos (`i-puerta`, `i-calendario`, `i-flecha-izq`, `i-flecha-der`) y sus tokens.

## 0. Instrucciones para el agente

### 0.1 Qué leer antes de tocar código

1. Este plan completo.
2. `Frontend/Admind_Front-End/apps/reservas/README.md` (la primera viñeta describe la pantalla de hoy).
3. **No leas ni edites `calendario.html` ni `reservas.css` de `Plan_Estilo_Visual_Recursos/`**: son definitivos y se copian tal cual.

### 0.2 Reglas propias de este plan

- `calendario.html` y `reservas.css` se copian con `cp`; no se reescriben ni se «mejoran». Fueron probados el 2026-10-30 con datos de zonas con reserva y con ingreso, en seis acentos y a 375 px.
- **No se toca `apps/reservas/views.py`.** La plantilla recibe exactamente el mismo contexto de antes.
- Las cinco ediciones de `tests/test_reservas.py` traen texto **viejo** y **nuevo**. El viejo debe aparecer **una sola vez**; si no, **detente y avisa**.
- **Nada de commits ni de `push`.** Alejo hace la rama, el commit y el PR. Nada se instala.
- Terminal: Git Bash, rutas con espacios entre comillas. `RECURSOS` = `../../Documentacion/Admind_Documentacion/07_Planes/activos/Plan_Estilo_Visual_Recursos` desde `Frontend/Admind_Front-End`.

## 1. Punto de partida

Verificado el 2026-10-30:

- «Zonas comunes» (`/reservas/`) abre con **una tabla** de todas las zonas (nombre, cómo se usa, horario, cupos, estado, acción) y debajo el selector de área, el calendario y las franjas del día **en una lista**. La vista `pantalla_del_calendario` arma `zonas` (con `fila_de_zona`), `areas`, `semanas`, `franjas`, etc.
- Las pruebas de `tests/test_reservas.py` fijan **qué** debe decir la pantalla, y algunas **cómo está armada**. La plantilla nueva respeta todo eso, salvo cinco aserciones que miraban la tabla (`<td>…</td>`) y se actualizan en F2:
  - `"selector-area"` aparece **antes** que `class="am-tarjeta calendario"`.
  - `name="area" data-envio-al-cambiar`, `js/calendario-reservas.js`, `class="franjas"`, `Horario para reservas: 08:00 a 22:00.`, las pastillas `class="am-pastilla am-pastilla--error">Apartada</span>`, `>Reservar</button>` (una sola vez) y el aviso `role="alert">\n    <p>…` **antes** de las franjas.
  - Textos de las zonas: «Con reserva», «Con ingreso», «12 de 30 libres», «Abierta», «puedes quedarte hasta 60 min», «Sin cupo», «Cerrada», el motivo del cierre, «En mantenimiento», «Sin información», `>Reservar</a>` (y ninguna palabra «Reservar» en una zona con ingreso), «Los cupos se actualizan al recargar la página.» y `>Actualizar</a>`.
- Último commit de los archivos: `calendario.html` → `74883d3`, `reservas.css` → `721efae`, `tests/test_reservas.py` → `d0e4af7`.

## 2. Decisiones que toma Alejo

Ninguna.

## 3. Decisiones menores que el plan ya fija

| ID | Decisión |
|---|---|
| P1 | La tabla de zonas pasa a **tarjetas**: ícono (puerta para zonas con ingreso, calendario para las de reserva), nombre, cómo se usa, **pastilla de estado** (con sus colores fijos y su texto), horario, permanencia o duración de cada franja, y el botón **Reservar** en las zonas con reserva. El texto de cada dato no cambia |
| P2 | Las zonas con ingreso muestran un **medidor** de cupos libres (`{% widthratio %}`), además del texto «12 de 30 libres». El medidor usa el acento solo como adorno: el estado lo sigue diciendo la pastilla |
| P3 | El botón **Reservar** de una tarjeta lleva a `?area=…&mes=…#reservar`: elige el área y baja a la sección de reservar. La tarjeta del área elegida se resalta |
| P4 | «Reserva tu espacio» pone el **calendario** (con el selector de área encima) a la izquierda y las **franjas del día** a la derecha, en una tarjeta fija al bajar; bajo 900 px van una debajo de la otra. Cada franja es una tarjetita con su hora, su pastilla y su botón |
| P5 | El día elegido del calendario se marca con borde y fondo del acento, y los días disponibles se levantan al pasar el mouse |
| P6 | El aviso de error (409, áreas que no cargan…) sale **entre** las zonas y «Reserva tu espacio», con el mismo HTML de antes |
| P7 | Se renombran dos pruebas que decían «tabla»: pasan a decir «tarjetas» y «zonas». Es solo el nombre |

## 4. Orden y dependencias

F0 → F1 → F2 → F3 → F4. Después del plan base. Es independiente del de conjuntos.

## F0 · Comprobar el punto de partida

Desde `Frontend/Admind_Front-End`:

```bash
git status --short
ls static/css/apariencia.css templates/componentes/_iconos.html
grep -c 'id="i-puerta"\|id="i-calendario"\|id="i-flecha-izq"\|id="i-flecha-der"' templates/componentes/_iconos.html
for f in apps/reservas/templates/reservas/calendario.html static/css/reservas.css tests/test_reservas.py; do echo "$f  $(git log -1 --format=%h -- $f)"; done
./.venv/Scripts/python.exe -m pytest -q
```

Se espera: los dos archivos existen; el `grep -c` devuelve `4`; los últimos commits son `74883d3`, `721efae` y `d0e4af7`; la suite en verde. **Si falta un ícono o un archivo, el plan base no está hecho: detente y avisa a Alejo. Si un archivo tiene otro último commit, alguien lo cambió: avisa antes de reemplazarlo.**

## F1 · La plantilla y la hoja (copiar)

```bash
R="../../Documentacion/Admind_Documentacion/07_Planes/activos/Plan_Estilo_Visual_Recursos"
cp "$R/calendario.html" apps/reservas/templates/reservas/calendario.html
cp "$R/reservas.css" static/css/reservas.css
```

**Se comprueba:** `grep -c "zona-tarjeta" apps/reservas/templates/reservas/calendario.html` devuelve un número mayor que 5, y `git diff --stat` solo lista esos dos archivos.

## F2 · Las cinco aserciones de las pruebas

Archivo: `tests/test_reservas.py`. Cinco ediciones, cada una con el texto viejo exacto.

**2.1** Viejo:

```python
def fila(html, nombre):
    return html.split(f"<td>{nombre}</td>")[1].split("</tr>")[0]
```

Nuevo:

```python
def fila(html, nombre):
    """La tarjeta de una zona: desde su nombre hasta el cierre de su <li>."""
    return html.split(f'<h3 class="zona-tarjeta__nombre">{nombre}</h3>')[1].split("</li>")[0]
```

**2.2** Viejo: `def test_la_tabla_dice_como_se_usa_cada_zona_y_la_de_ingreso_muestra_sus_cupos_sin_reservar():` → Nuevo: `def test_las_tarjetas_dicen_como_se_usa_cada_zona_y_la_de_ingreso_muestra_sus_cupos_sin_reservar():`

**2.3** Viejo: `assert "<td>Con reserva</td>" in fila(html, "Salón comunal")` → Nuevo: `assert ">Con reserva</p>" in fila(html, "Salón comunal")`

**2.4** Viejo: `assert "<td>Con ingreso</td>" in gimnasio` → Nuevo: `assert ">Con ingreso</p>" in gimnasio`

**2.5** Viejo: `def test_la_tabla_invita_a_recargar_para_ver_los_cupos_nuevos():` → Nuevo: `def test_las_zonas_invitan_a_recargar_para_ver_los_cupos_nuevos():`

**Se comprueba:**

```bash
grep -n "<td>" tests/test_reservas.py    # no debe quedar ninguna mención a <td>{nombre}</td> ni <td>Con …
./.venv/Scripts/python.exe -m pytest tests/test_reservas.py -q
./.venv/Scripts/python.exe -m pytest -q
```

Se espera: todo en verde, **la misma cantidad de pruebas que antes de este plan** (503 o 504). Si falla una prueba que este plan no nombra, **no la cambies**: avisa a Alejo con su nombre y el error (significa que la plantilla nueva rompió algo que el plan no previó).

## F3 · Verificación visual (la API en el 8000 y el front en el 8001)

La hace Alejo, o el agente si tiene un navegador. Necesita un conjunto con al menos **una zona con reserva** y **una con ingreso** (el Superusuario las crea en *Áreas comunes*).

| Dónde | Qué debe verse |
|---|---|
| **Zonas comunes** (`/reservas/`) | «Cómo se usa cada zona» como **tarjetas** (la elegida, resaltada con el color del conjunto). Cada una: ícono, nombre, «Con reserva» o «Con ingreso», pastilla de estado, horario y duración o permanencia |
| Zona con ingreso | «12 de 30 libres» (o los que sean) **y** una barra de cupos que se llena al cargar. Sin botón «Reservar» |
| Zona con reserva | Botón **Reservar** a todo el ancho. Al tocarlo la página baja a «Reserva tu espacio» con esa área elegida y su tarjeta resaltada |
| **Reserva tu espacio** | A la izquierda, el selector de área y el calendario; a la derecha, «Elige un área y un día del calendario» (o las franjas si ya hay área y día) |
| Elegir un día | El día queda con borde del acento; a la derecha aparece el panel con la fecha en letras, el horario y **una tarjetita por franja** (hora, pastilla Libre / En trámite / Apartada / Reservada, y «Reservar» solo en las libres) |
| Tomar una franja libre | Lleva a la solicitud en trámite como antes (cuenta regresiva de 3 minutos): **el flujo no cambió** |
| Un 409 (franja ocupada) | La alerta roja aparece **sobre** «Reserva tu espacio», con su mensaje |
| API de ingresos caída | Aviso azul «No pudimos consultar los cupos…»; las zonas con reserva siguen mostrando «Reservar» |
| Sin zonas | El estado vacío invita a registrarlas |
| Pantalla angosta (≈ 375 px) | Tarjetas en una columna; calendario y franjas una debajo de la otra; los botones «Mes anterior / siguiente» caben; sin barra horizontal |
| Los tres fondos | Se ve bien con Liso, Color y Cristal, y con otro conjunto (otro acento) |

## F4 · Documentación (cierre)

Sigue [actualizar_contexto](../../09_Protocolos/actualizar_contexto.md):

- `Frontend/Admind_Front-End/apps/reservas/README.md`: la primera viñeta de *Qué va aquí* pasa de «abre con una tabla de todas las zonas» a «abre con **una tarjeta por zona** (nombre, cómo se usa, horario y, en las de ingreso, los cupos con su medidor)» y agregar que el calendario y las franjas del día van lado a lado.
- `05_Modulos/reservas.md`: donde diga «tabla» de zonas, cambiarlo a tarjetas (si no lo dice, no tocar la nota).
- `04_Diseno/implementacion.md`: en la sección *La capa «con vida»* agregar que `reservas.css` quedó con las tarjetas de zona, el medidor y las franjas en tarjetas.
- `06_Decisiones/construccion.md`: una fila nueva: 2026-10-30; «Zonas comunes pasa de tabla a tarjetas por zona, con el calendario y las franjas del día lado a lado. Alejo permitió cambiar la estructura de esta pantalla; el contexto de la vista y el flujo de reserva no cambian. Cinco aserciones de `test_reservas.py` se actualizaron porque miraban la tabla»; quién: Alejo, en chat; dónde: este plan.
- `08_Estado/bitacora.md` (una fila); `actualizado:` y `revisado:` con `2026-10-30` en cada nota tocada.
- Al cerrar los **tres** planes de estilo, mover los planes y la carpeta de recursos a `07_Planes/hechos/` (ver el plan base, F6).

## Cierre del agente

`git status --short` debe listar **solo** `apps/reservas/templates/reservas/calendario.html`, `static/css/reservas.css` y `tests/test_reservas.py` (además de lo del plan base si todavía no se fundió). Suite en verde. Decir en el chat qué notas se tocaron.

## Lo que el agente no puede hacer

**Rama, commit y PR los hace Alejo.** Sugerido (después de fundir el plan base en `desarrollo`):

```bash
cd "Frontend/Admind_Front-End"
git switch desarrollo
git pull
git switch -c feat/estilo-visual-zonas-comunes
git add apps/reservas/templates/reservas/calendario.html static/css/reservas.css tests/test_reservas.py
git commit -m "feat(reservas): zonas comunes como tarjetas, con calendario y franjas del día lado a lado [HU-11]"
git push -u origin feat/estilo-visual-zonas-comunes
```

Y la prueba manual de F3 por alguien que no haya programado el cambio, con un residente (que reserva) y con Vigilancia o Administración (que ven las zonas con ingreso).

## Guiones de prueba manual

La tabla de F3.

## Informe final que entrega el agente

En el chat: lo copiado y editado, pruebas antes y después (deben ser las mismas), notas tocadas y desvíos.

## Fuera de este plan

- «Áreas comunes» (`/areas/`, la lista de administración) y el detalle de una solicitud: heredan los estilos de la base, pero su estructura no cambia.
- Cambiar la lógica de cupos, de franjas o de reservas, o el contexto que arma `views.py`.
- Íconos distintos por tipo de zona (piscina, cancha, salón…): la API no entrega un tipo de zona, solo el modo de uso.
