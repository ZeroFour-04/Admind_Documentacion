---
resumen: "Pasos para hacer el informe de avance que se entrega al docente, con capturas, a partir de la plantilla."
tipo: protocolo
origen: "estructura de los informes 1 a 3 (2026-09-15, 2026-09-21 y 2026-09-29)"
actualizado: 2026-10-11
revisado: 2026-10-11
---

# Protocolo: generar un informe de avance

## Qué es

El **entregable para el docente**. Cuenta qué es AdMind, cómo está armado y cuánto avanzó desde el informe anterior, con capturas del sistema funcionando. Hay cuatro: 15/09, 21/09, 29/09 y 06/10 (el cuarto quedó con las capturas por pegar; en la bóveda no consta si ya se entregó).

## Qué produce

- **Carpeta:** `Archivo/Informes/AAAA-MM-DD/`, con la fecha de corte.
- **Archivo:** `Admind_Informe_Avance_AAAA-MM-DD.md` dentro de esa carpeta. Las capturas van al lado, en `Capturas/`.
- **Plantilla:** [informe_de_avance](Plantillas/informe_de_avance.md). No hace falta leer un informe anterior completo para copiar el formato.

## Pasos

1. **Preguntarle a Alejo qué historias se reportan como terminadas.** En el informe 3 decidió reportar los Sprints 1 y 2 como terminados aunque les faltara la parte humana de la DoD. En el informe 4 (06/10) pidió repartirlas según lo que hay en el código, con un criterio menos estricto que la DoD. Esa decisión es suya en cada informe ([estado_actual](../08_Estado/estado_actual.md)).
2. **Verificar en el corte:**
   - `git fetch` y `git log` en los tres repositorios, para la tabla de commits desde el informe anterior;
   - `pytest` en backend y frontend, con el número de pruebas que pasan y las que fallan;
   - `showmigrations` en el backend;
   - Notion solo si Alejo pide consultarlo.
3. **Reunir lo que cambió** desde el informe anterior. Sale de [bitacora](../08_Estado/bitacora.md), [construccion](../06_Decisiones/construccion.md) e [historias](../08_Estado/historias.md). Del informe anterior basta leer su resumen inicial y su sección 9.
4. **Copiar la plantilla** a la carpeta del corte y llenarla en el mismo orden de secciones. Las secciones 1 a 5 cambian poco entre informes: se ajusta solo lo nuevo.
5. **Capturas:** el agente no las toma. Deja cada una como un recuadro con su número, su título, una línea que dice qué debe verse y el marcador `*(pega aquí la captura)*`. Alejo las pega en Obsidian.
6. **Avisar** al terminar cuántas capturas faltan por pegar y qué datos no se pudieron verificar.

## Reglas

- **Es para el docente:** frases completas, sin jerga interna y sin identificadores sin explicar (D3, P10). La equivalencia con la plantilla ASP.NET de clase va siempre, porque es lo que el docente conoce.
- **Sin contraseñas, tokens ni valores de `.env`.**
- Lo que se afirme del código se verifica el día del corte.
- Un informe entregado no se edita. El siguiente es un archivo nuevo.
- Los informes ya entregados usan `[[enlaces]]` de Obsidian para el índice y las imágenes. En los nuevos, el índice va con enlaces markdown a los títulos y las imágenes como las pegue Obsidian.

> [!NOTE] Por definir con Alejo
> En qué formato se entrega al docente (PDF exportado desde Obsidian u otro) y si lleva una portada distinta. Los informes anteriores no lo dejan escrito.

## Ver también

- [informe_de_avance](Plantillas/informe_de_avance.md) — la plantilla
- [generar_documento_de_avance](generar_documento_de_avance.md) — la foto para el equipo, que no es este informe
- [estado_actual](../08_Estado/estado_actual.md) e [historias](../08_Estado/historias.md) — de dónde salen los números
- [vision_general](../02_Arquitectura/vision_general.md) — la equivalencia con la plantilla del profesor
