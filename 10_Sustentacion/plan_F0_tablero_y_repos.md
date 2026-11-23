---
titulo: "F0 · Tablero de seguimiento y enlaces a los repositorios"
fecha: 2026-11-14
alcance: "Documento corto con el tablero Scrum de Notion (enlace y capturas) y los enlaces a los repositorios de backend y frontend"
punto_de_partida: "Tablero público de Notion; repos públicos ZeroFour-04/Admind_Backend (7 PR) y ZeroFour-04/Admind_Front-End (5 PR) al 2026-11-14"
resumen: "Plan del entregable de tablero y repositorios; se hace al final de la F0, después de que Alejo actualice Notion."
estado: activo
ejecutado:
hu:
---

# Plan F0 · Tablero de seguimiento y repositorios

**Entregable:** `Entregables_Sustentacion\AdMind_Tablero_y_Repositorios.docx` (y su PDF).
**Tiempo estimado:** 45 minutos, después de actualizar Notion.
**Antes de empezar:** leer [estilo_entregables](estilo_entregables.md).

> [!WARNING] Orden
> Alejo actualiza Notion a mediodía del sábado 14. **Este plan se ejecuta después**, y antes de las 18:00. El agente no edita Notion: solo lo lee para comprobar el enlace, si Alejo se lo pide.

## Paso 1. Capturas del tablero (Alejo)

Tablero público: https://useful-vest-416.notion.site/Seguimiento-Scrum-2-0-AdMind-3f1739efa3338109b3f1e256d441de64

Guardar en `Entregables_Sustentacion\capturas\tablero\`:

| N | Qué capturar | Archivo |
|---|---|---|
| T01 | La vista general del tablero, con las columnas por estado | `T01_tablero.png` |
| T02 | El backlog con las historias (código, nombre, puntos, sprint y estado) | `T02_backlog.png` |
| T03 | La vista por sprint, o el filtro de un sprint | `T03_sprint.png` |
| T04 | Una historia abierta, con sus tareas y criterios de aceptación (por ejemplo HU-11 o HU-14) | `T04_historia.png` |
| T05 | Si existe: el gráfico de avance o de puntos por sprint | `T05_avance.png` |

Abrir el enlace en una ventana de incógnito para confirmar que se ve sin sesión.

## Paso 2. Capturas de GitHub (Alejo o el agente con el navegador)

Guardar en `Entregables_Sustentacion\capturas\repos\`:

| N | Qué capturar | Archivo |
|---|---|---|
| R01 | La portada del repo del backend | `R01_backend.png` |
| R02 | La pestaña *Pull requests → Closed* del backend | `R02_backend_pr.png` |
| R03 | La portada del repo del frontend | `R03_frontend.png` |
| R04 | La pestaña *Pull requests → Closed* del frontend | `R04_frontend_pr.png` |

## Paso 3. Armar el Word (agente)

1. **Portada** según el estilo común. Título: "Tablero de Seguimiento y Repositorios".
2. **1. Metodología** (media página): Scrum con historias de usuario (HU) estimadas en puntos, sprints y Definition of Done. **Fuente:** [scrum_y_dod](../03_Reglas/scrum_y_dod.md), solo las primeras secciones. Escribirlo en tres o cuatro frases.
3. **2. Tablero de seguimiento:**
   - el enlace (como hipervínculo) y un **código QR** al enlace, generado con la librería `qrcode` que ya está en el venv del backend;
   - las capturas T01 a T05, con un pie que explique qué muestra cada una;
   - un párrafo con las cifras del avance, **leídas del tablero ya actualizado** (no de la bóveda).
4. **3. Repositorios:** una tabla Repositorio | Enlace | Qué contiene | Tecnología:
   - **Backend (API):** https://github.com/ZeroFour-04/Admind_Backend — Django + Django REST Framework + PostgreSQL.
   - **Frontend:** https://github.com/ZeroFour-04/Admind_Front-End — Django con plantillas + Alpine.js.

   El repositorio de documentación no va (decisión de Alejo: el profesor quiere ver código).
5. **3.1 Flujo de trabajo en Git:**
   - ramas `main`, `desarrollo` y `pruebas`, más una rama corta por cambio que entra a `desarrollo` por PR;
   - el número de PR cerrados en cada repo, **contados el mismo día con** `gh pr list -R ZeroFour-04/Admind_Backend --state all` (y lo mismo para el front);
   - las capturas R01 a R04.

   **Fuente:** [git](../03_Reglas/git.md), solo la sección de ramas.
6. Exportar a PDF y probar desde el PDF que los tres enlaces abren.

## Ver también

- [estilo_entregables](estilo_entregables.md) — colores, fuentes, portada y salida
- [tareas](tareas.md) — A1, la lista de entregables de hoy
- [repositorios](../02_Arquitectura/repositorios.md) — los tres repositorios y por qué no son submódulos
