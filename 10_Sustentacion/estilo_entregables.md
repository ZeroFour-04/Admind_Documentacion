---
resumen: "Estilo común de los Word de la sustentación final: carpeta de salida, portada, colores, fuentes, logo y forma de entrega."
tipo: plan
origen: "tokens del design system del front (paleta.css, tipografia.css) y pedido de Alejo, 2026-11-14"
actualizado: 2026-11-14
revisado: 2026-11-14
---

# Estilo de los entregables de la sustentación

Todos los planes F0 remiten aquí. Los cuatro documentos tienen que verse de la misma familia.

## Herramienta y salida

- Se arman con el skill **`anthropic-skills:docx`** (Word). Si la sesión no lo tiene, se pregunta a Alejo antes de seguir.
- **Carpeta de salida:** `C:\Users\Alejandro\Documents\A D M I N D\Entregables_Sustentacion\`, fuera de los tres repositorios. Si no existe, se crea.
- **Nombres:** `AdMind_Manual_Tecnico.docx`, `AdMind_Manual_Usuario.docx`, `AdMind_Diccionario_de_Datos.docx` y `AdMind_Tablero_y_Repositorios.docx`.
- Al terminar cada Word se exporta también a **PDF** con el mismo nombre: el PDF se ve igual en cualquier PC. Alejo decide cuál sube al aula.
  - Si el skill no exporta a PDF y Word está instalado, se puede hacer desde PowerShell: `$w = New-Object -ComObject Word.Application; $d = $w.Documents.Open("<ruta>.docx"); $d.SaveAs([ref]"<ruta>.pdf", [ref]17); $d.Close(); $w.Quit()`.
  - Si tampoco hay Word, se deja el `.docx` y se le avisa a Alejo.
- Las capturas que haga falta tomar van en `Entregables_Sustentacion\capturas\`.

## Portada (igual en los cuatro)

1. Logo de AdMind centrado, unos 5 cm de ancho: `C:\Users\Alejandro\Documents\A D M I N D\Frontend\Admind_Front-End\static\img\logo-marca.png` (PNG de 256 × 256 px con transparencia).
2. Título del documento (por ejemplo, "Manual Técnico").
3. Subtítulo: "AdMind — Plataforma de administración de conjuntos residenciales".
4. Integrantes, uno por línea y en mayúsculas, como los dio Alejo el 2026-11-14: **MANUEL ALEJANDRO ALDANA RINCON** y **ANDERSON CAMILO REMISO NIÑO**.
5. Asignatura: Ingeniería de Software II. Docente: Oscar Gómez. Universidad de Cundinamarca.
6. Fecha: 14 de noviembre de 2026.

Después de la portada: tabla de contenido automática (de los títulos 1 y 2) y luego el cuerpo.

## Colores

Son los del verde base de AdMind (`design-system/tokens/paleta.css` del front). AdMind deja que cada conjunto elija su acento, pero la identidad de la marca es este verde.

| Uso | Color |
|---|---|
| Títulos 1, franjas de portada, encabezado de tablas (con letra blanca) | `#0E6B5A` (verde 600) |
| Títulos 2 y 3, enlaces | `#0B5546` (verde 700) |
| Texto sobre fondos claros de marca, cifras destacadas | `#06302A` (verde 900) |
| Fondo de filas alternas de tablas, recuadros de nota | `#EEF5F2` (verde 50) |
| Texto del cuerpo | `#14201D` (gris 950) |
| Texto secundario (pies de figura, notas) | `#64706C` (gris 500) |
| Bordes de tablas | `#D6DCDA` (gris 200) |
| Avisos o advertencias | fondo `#FBF0DC`, texto `#6B4A05` (ámbar) |

## Fuentes

- **Títulos:** Archivo. **Cuerpo:** Inter. Son las de la plataforma.
- Si no están instaladas en Windows (revisarlo), usar **Calibri** para todo; no mezclar más de dos familias.
- Cuerpo en 11 pt con interlineado de 1,15. Código y nombres técnicos (rutas, tablas, endpoints) en **Consolas** de 10 pt.

## Encabezado y pie de página (desde la página 2)

- **Encabezado:** logo pequeño (1 cm) a la izquierda y el nombre del documento a la derecha, en gris 500, con una línea fina verde 600 debajo.
- **Pie:** "AdMind · Ingeniería de Software II · 2026" a la izquierda y "Página X de Y" a la derecha.

## Tablas

Encabezado en verde 600 con letra blanca en negrita, filas alternas en verde 50, bordes en gris 200 y la fila de encabezado repetida en cada página. **Todas las páginas de los cuatro documentos son carta vertical (612 × 792 pt), sin secciones horizontales** (Alejo, 2026-11-14): las tablas anchas se acomodan al ancho útil de 9360 DXA y las celdas largas se parten en renglones.

## Voz

Español claro, en presente y sin relleno. Se describe lo que el sistema **hace hoy**. Lo que esté planeado para antes de la sustentación y todavía no exista se marca como "En implementación" (recuadro ámbar), nunca como hecho.

## Ver también

- [tareas](tareas.md) — la lista de tareas de la sustentación
- [sistema_visual](../04_Diseno/sistema_visual.md) — principios y tokens del diseño de AdMind
