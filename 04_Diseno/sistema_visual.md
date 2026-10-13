---
resumen: "Sistema visual v1: los tres principios, tokens, catálogo de acentos, bento, voz de la interfaz y DoD visual."
tipo: diseno
origen: "maestro v1.4 (2026-09-14) §6"
actualizado: 2026-10-11
revisado: 2026-10-11
---

# Sistema visual

> [!WARNING] Decisiones posteriores a este texto
> - **2026-09-21:** el acento por conjunto se reactivó con los 8 del catálogo de 6.3 y `data-acento`. El aviso *Aplazado el 2026-09-11* de 6.3 ya no rige.
> - **2026-09-29:** además de los 8 hay **color propio** (hex libre; si el texto blanco baja de 4.5:1 solo se advierte) y **foto cuadrada 1:1** del conjunto, que reemplaza al logo. Revierte el *sin selector libre de color* de 6.3.
> - **Sigue abierto:** `design-system/` usa Archivo + Inter y `--radio-control: 4px`; este texto dice solo Inter y 6px. El verde por defecto en el código es el de `design-system/` (`#0E6B5A`).
>
> Cómo quedó en el código: [implementacion](implementacion.md) y [conjuntos](../05_Modulos/conjuntos.md).

Definición visual v1. Implementado en la carpeta `design-system/` del repositorio, generada en Claude Design.

**Alcance de v1: solo modo claro.** El modo oscuro es Condicional, y la disciplina de tokens es lo que hace barato agregarlo después.

## 6.1 Los tres principios

**Dos capas: superficie y acento.** La capa base es el 85 % de lo que se ve —fondo `#F8FAFC`, tarjetas blancas, bordes sutiles— y no se personaliza nunca. El acento del conjunto activo se reserva a **cuatro sitios**: botón primario, ítem activo de navegación, anillo de foco y barra identificadora del conjunto. **Si aparece en un quinto sitio, es un error de implementación, no una variante.**

**Acción y estado no comparten forma.** El verde de marca coincide con el verde de "confirmado". Esa colisión no se resuelve con dos verdes, se resuelve con la forma:

||Forma|
|---|---|
|**Acción**|Relleno sólido, radio 6px, texto blanco — `Confirmar reserva`|
|**Estado**|Fondo suave, pastilla completa, texto oscuro del mismo tono — `Confirmada`|

Nunca existe un botón de fondo suave ni una pastilla de relleno sólido.

**El acento nunca toca la semántica.** `--acento-*` no aparece en ninguna regla que comunique estado, resultado o severidad. Si los chips siguieran al acento, un conjunto con acento vino mostraría las confirmaciones en rojo.

## 6.2 Tokens

Viven en `static/css/tokens.css`. **Ningún componente escribe un hex directamente.**

```css
:root {
  --superficie-0: #F8FAFC;  --superficie-1: #FFFFFF;  --superficie-2: #F1F5F9;
  --borde: #E2E8F0;         --borde-fuerte: #CBD5E1;
  --texto-1: #0F172A;       --texto-2: #475569;       --texto-3: #64748B;

  --estado-tramite-bg: #FEF3C7;  --estado-tramite-txt: #78350F;
  --estado-ok-bg:      #E8F5F0;  --estado-ok-txt:      #05372D;
  --estado-error-bg:   #FEE2E2;  --estado-error-txt:   #7F1D1D;
  --estado-neutro-bg:  #F1F5F9;  --estado-neutro-txt:  #334155;
  --info-bg:           #EAF2FA;  --info-txt:           #0C3765;

  --e-1:4px; --e-2:8px; --e-3:12px; --e-4:16px;
  --e-5:24px; --e-6:32px; --e-7:48px; --e-8:64px;
  --radio-sm:6px; --radio:12px; --radio-full:999px;
  --sombra-flotante: 0 4px 16px rgba(15,23,42,0.12);
}
```

Tres niveles de texto y no más: un cuarto no pasaría 4.5:1 sobre blanco.

**Mapeo de estados al flujo de reserva:** En trámite → `tramite` (ámbar, hay reloj) · Confirmada → `ok` · Rechazada → `error` (decisión negativa de una persona) · **Expirada y Anulada → `neutro`**, porque no son errores: son no-eventos.

**Tipografía: Inter, autoalojada.** No se carga desde Google Fonts: servir tipografías desde un tercero envía la IP de cada residente a ese tercero, y eso es un tratamiento que no está en la autorización de la Ley 1581.

Escala: 12 / 13 / 15 / 18 / 24 / 30 px. Pesos: 400 cuerpo, 500 títulos, 600 solo para la cifra grande de una tesela.

> [!TIP] La regla que más se nota Toda columna de números —unidades, documentos, horas— lleva `font-variant-numeric: tabular-nums`. Sin eso una tabla de apartamentos queda desalineada. Es una línea de CSS.

**Una sola sombra en todo el sistema**, y solo para lo que flota: modal, desplegable, popover. Tarjetas y teselas se separan con borde. Ancho máximo de contenido 1100px; línea de texto máximo 75 caracteres.

## 6.3 Catálogo de acentos

**Ocho opciones cerradas en código, sin selector libre de color.** Un hex arbitrario obliga a validar contraste de una elección ajena: complejidad permanente para un caso que ocurre una vez.

|Slug|50|600|700|900|Contraste|
|---|---|---|---|---|---|
|`verde` _(defecto)_|`#E8F5F0`|`#0E7C66`|`#0B5F4E`|`#05372D`|5.1:1|
|`azul`|`#EAF2FA`|`#1D5FA8`|`#164A85`|`#0C3765`|6.5:1|
|`indigo`|`#EEF0FB`|`#4340A8`|`#363385`|`#1F1D52`|8.3:1|
|`purpura`|`#F4ECF8`|`#6B2D8C`|`#55236F`|`#351646`|8.8:1|
|`vino`|`#FAECEF`|`#9B2242`|`#7C1B35`|`#4C1020`|7.8:1|
|`terracota`|`#FBEDE7`|`#A8451E`|`#863718`|`#4F1F0C`|6.0:1|
|`ocre`|`#FAF0DF`|`#8A5A0F`|`#6E4709`|`#422A04`|5.9:1|
|`pizarra`|`#EEF1F5`|`#41586F`|`#334659`|`#1E2A36`|7.4:1|

**Por qué existe la personalización, y no es estética.** Una persona puede pertenecer a varios conjuntos y cambiar entre ellos (HU-26). Que el color cambie al cambiar de conjunto es una señal permanente de dónde estás operando, y **reduce el riesgo de actuar en el conjunto equivocado**. Ese es el argumento que se defiende.

En base de datos se guarda el **slug**, nunca un hex. El elemento raíz lleva `data-acento="{{ slug }}"` y el CSS resuelve el resto. Sin recompilar, sin una hoja por conjunto, sin JavaScript.

> [!IMPORTANT] Aplazado el 2026-09-11 — se arranca con un solo acento
> Hasta nueva orden, la implementación usa **un único acento**. No se implementa el campo de acento por conjunto ni el atributo `data-acento`. El catálogo de ocho queda **aplazado, no eliminado**: la disciplina de tokens es justamente lo que mantiene barato reactivarlo.
>
> Razón: el esfuerzo del arranque va al núcleo —aislamiento, concurrencia, auditoría— y no a la personalización.
>
> **Choque pendiente de resolver.** Según la revisión del 7 de septiembre de 2026, la carpeta `design-system/` generada en Claude Design no coincide con este §6: usa un solo acento, Archivo + Inter en vez de solo Inter, y `--radio-control: 4px` en vez de 6px. Ese choque **no está en §12** y se decide cuando se trabaje el frontend.

## 6.4 Bento grid — dónde sí

El bento es un patrón de **panel heterogéneo**, no de aplicación. Se usa en tres vistas: inicio de Administración, inicio de Residente, panel de Vigilancia. **No se usa** en personas, unidades, bandejas, registro de actividades, reservas, formularios ni detalle de nada.

Rejilla de 12 columnas, gap 16px, altura de fila 140px. **Cuatro tamaños y ninguno más**: `4x1`, `6x1`, `6x2`, `12x1`. Máximo 6 teselas por vista. Bajo 900px colapsan a ancho completo.

Cuatro tamaños fijos es lo que separa un bento de un collage. Si un contenido no cabe en ninguno, no es una tesela: es una vista propia con enlace desde el panel.

## 6.5 Voz de la interfaz

- **Verbo activo y concreto en botones.** `Confirmar reserva`, no `Enviar`
- **La acción conserva su nombre en todo el flujo.** El botón dice `Confirmar reserva`, el resultado dice `Reserva confirmada`
- **Los errores no se disculpan y no son vagos.** Dicen qué pasó y qué hacer
- **Un estado vacío es una invitación**, con la acción que corresponda debajo
- Frase en mayúscula inicial; nunca versalitas ni todo en mayúsculas

## 6.6 Definition of Done visual

- [ ] Todo texto pasa **4.5:1** contra su fondo; textos grandes 3:1
- [ ] Ningún estado se comunica **solo con color**: siempre hay texto
- [ ] El foco de teclado es visible y la vista se recorre con `Tab`
- [ ] Toda área táctil mide al menos 44×44px
- [ ] Usable a 200 % de zoom y a 360px de ancho
- [ ] No hay hex dentro de un componente
- [ ] `--acento-*` no aparece en ninguna regla de estado
- [ ] Los formularios tienen `label` asociado, no solo `placeholder`

## Ver también

- [abiertas](../06_Decisiones/abiertas.md) — maestro §12
- [implementacion](implementacion.md) — cómo quedó en el código
- [reglas_frontend](../03_Reglas/reglas_frontend.md) — lo que una pantalla no rompe
- [conjuntos](../05_Modulos/conjuntos.md) — el color propio y la foto 1:1
- [lista_de_salida](../03_Reglas/lista_de_salida.md) — la DoD visual, al entregar
