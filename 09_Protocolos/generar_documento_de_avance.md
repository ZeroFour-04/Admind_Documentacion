---
resumen: "Pasos para hacer un Documento Avance: la foto fechada del proyecto para el equipo y los agentes, solo texto."
tipo: protocolo
origen: "Avance 22092026 §11 (2026-09-22)"
actualizado: 2026-10-11
revisado: 2026-10-11
---

# Protocolo: generar un Documento Avance

## Qué es

Una **foto fija** del proyecto en una fecha. Es para el equipo y para agentes de IA. No se entrega al docente: para eso está el [informe de avance](generar_informe_de_avance.md). No reemplaza a `08_Estado/`, que es el registro vivo.

## Qué produce

- **Archivo:** `Archivo/Avances/Avance DDMMAAAA.md`. Un archivo nuevo por corte. Los anteriores no se editan, salvo para corregir una errata.
- **Plantilla:** [documento_de_avance](Plantillas/documento_de_avance.md). El primero de la serie, como ejemplo lleno, es `Archivo/Avances/Avance 22092026.md`.

## Pasos

1. **Verificar en el corte.** Todo lo que se afirme del código se comprueba ese día:
   - `git fetch` y `git log --oneline -1` en los tres repositorios;
   - `pytest` en backend y frontend;
   - `showmigrations` en el backend;
   - los estados de las historias en Notion, si Alejo pide consultarlo.
2. **Copiar la plantilla** con el nombre del corte y llenar el frontmatter: fecha y hora, el avance anterior en `avance_anterior` y los commits de los tres repositorios.
3. **Llenar las secciones en el mismo orden**, para que dos cortes se puedan comparar lado a lado. La sección 1.2 se llama *Qué cambió desde el Avance DDMMAAAA* y enlaza el anterior.
4. **Decir en la sección 1.3 qué no se volvió a verificar**: lo que se tomó de otra nota sin comprobarlo ese día.
5. **Actualizar `08_Estado/`** con [actualizar_contexto](actualizar_contexto.md) si el corte encontró algo que las notas vivas no tenían.

## Reglas

- **Solo texto.** Nada de capturas, imágenes ni diagramas renderizados. Si algo necesita un diagrama, va como árbol o tabla en texto.
- **Sin contraseñas, tokens ni valores de `.env`.** Si hace falta decir que un secreto está expuesto, se dice dónde, nunca cuál es.
- Si una historia cambia de estado, se cambia también en Notion y en [historias](../08_Estado/historias.md): este documento no reemplaza a ninguno de los dos.
- Si el documento y el código no coinciden después, manda el código: pudo cambiar tras el corte.

## Ver también

- [documento_de_avance](Plantillas/documento_de_avance.md) — la plantilla
- [generar_informe_de_avance](generar_informe_de_avance.md) — el entregable para el docente
- [estado_actual](../08_Estado/estado_actual.md) — el registro vivo, que este documento no reemplaza
- [actualizar_contexto](actualizar_contexto.md) — si el corte encuentra algo nuevo
