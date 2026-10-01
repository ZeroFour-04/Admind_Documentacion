---
resumen: "Qué notas actualizar al terminar una tarea que cambió código, decisiones o estado, y con qué reglas."
tipo: protocolo
origen: "antiguo Admind_Avance.md §7, adaptado a las notas del 2026-09-30"
actualizado: 2026-09-30
---

# Protocolo: actualizar el contexto

## Cuándo

Al cerrar una tarea o una sesión de trabajo en la que cambió el código, se tomó una decisión o cambió el estado de una historia. No en cada mensaje, y no si solo se respondió una pregunta.

## Qué se actualiza

Solo lo que cambió. Cada fila es independiente:

| Si… | Actualiza |
|---|---|
| Pasó algo (commit, migración aplicada, prueba corrida, cambio en Notion) | Una fila al final de [bitacora](../08_Estado/bitacora.md): fecha y hora, dónde, qué pasó y el hash del commit si existe |
| Cambió el avance de una historia | Su fila en [historias](../08_Estado/historias.md). El detalle tarea por tarea, en [historias_evidencia](../08_Estado/historias_evidencia.md) |
| Se tomó una decisión | Una fila al final de [construccion](../06_Decisiones/construccion.md): fecha, decisión, quién decidió y dónde quedó. Si contradice una nota de diseño, un aviso al inicio de esa nota; el texto de diseño no se reescribe sin que el equipo lo pida |
| Se resolvió o apareció un pendiente | [pendientes](../08_Estado/pendientes.md): marcar o agregar |
| Cambiaron los commits de `desarrollo`, el número de pruebas o lo que frena | [estado_actual](../08_Estado/estado_actual.md), con la fecha de corte nueva |
| Hay una app, una ruta de la API o una pantalla nueva | [mapa_codigo](../02_Arquitectura/mapa_codigo.md) o [frontend](../02_Arquitectura/frontend.md), y el `README.md` de esa carpeta en el repositorio de código |
| Cambió cómo funciona un módulo | La sección *Cómo está construido* de su nota en `05_Modulos/` |
| Se creó una nota | Una línea en `README.md` |

En cada nota tocada se actualiza también `actualizado:` en el frontmatter.

## Reglas

- Una historia es **Terminada** solo si cumple la Definition of Done ([scrum_y_dod](../03_Reglas/scrum_y_dod.md)). Al 80 % aporta 0 SP.
- Lo que se afirme del código se verifica en el repositorio o en la base antes de escribirlo.
- Resumen conciso. Nunca un volcado de código.
- Si una historia cambia de estado, también cambia en Notion. Un agente no toca Notion por su cuenta: avisa.
- No se editan las fotos ni los informes de `Archivo/`.
- No va aquí: ejercicios del lab (`Archivo/Lab/Admind_Seguimiento_Lab.md`) ni errores con su aprendizaje (`Archivo/Lab/Admind_Bitacora_Errores.md`, que escribe Alejo).
- Sin commit ni `push` en el repositorio de documentación salvo que se pida.
- Obsidian tiene que estar abierto si se crean, mueven o borran archivos ([documentacion](../03_Reglas/documentacion.md)).

## Al terminar

Decir en el chat qué notas se tocaron y qué cambió en cada una, en una línea por nota.
